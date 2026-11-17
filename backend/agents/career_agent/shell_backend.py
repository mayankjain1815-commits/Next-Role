"""Virtual-path-aware shell backend used by the career agent.

Lives in its own module (rather than inline in `agents.py`) so tests can
exercise the path-translation logic without triggering the eager
`create_deep_agent()` call at `agents.py` module load.
"""

from __future__ import annotations

import os
import re
import shlex
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from deepagents.backends import LocalShellBackend

if TYPE_CHECKING:
    from deepagents.backends.protocol import ExecuteResponse


def default_shell_env() -> dict[str, str]:
    """Minimal environment for agent shell commands.

    `LocalShellBackend` deliberately spawns with an empty environment so agent
    commands never see provider API keys. But an empty env also empties PATH,
    so `/bin/sh` falls back to its compiled-in default (`/usr/local/bin:...`)
    — which misses virtualenv installs entirely: `rendercv` (and `python -m
    rendercv`) resolve only when deps live in the system interpreter. Passing
    just PATH — with the running interpreter's own bin dir first — makes
    console scripts and `python` resolve to this exact environment wherever it
    lives (`/opt/venv` in the image, `.venv` on a dev host), while keeping
    every secret out of the subprocess.
    """
    interpreter_bin = str(Path(sys.executable).parent)
    inherited = os.environ.get("PATH", os.defpath)
    return {"PATH": f"{interpreter_bin}{os.pathsep}{inherited}"}


# Shell control operators as they survive `shlex.split(..., posix=True)` —
# re-quoting them (what `shlex.join` does to every special char) turns a pipe
# or redirect into a literal argument, so they must be re-emitted raw.
_OPERATOR_RE = re.compile(r"^(?:\|\||&&|\|&|\|>|;;?|&|>>?|<<?|\(|\)|\d*>>?&?\d*|\d*<<?&?\d*)$")

# Tokens made of shell-benign characters (plus glob meta/$, which the agent's
# unquoted form means literally — `*.yaml` must stay an unquoted glob,
# `$HOME` an expansion) need no quoting and are safe to pass through raw.
_RAW_SAFE_RE = re.compile(r"^[A-Za-z0-9_@%+=:,./~?*\[\]{}!^$-]+$")


def _emit_token(token: str) -> str:
    """Render a rewritten token back into the command string.

    `shlex.join` re-quotes *every* token containing a non-identifier
    character — which defuses pipes, redirects, `&&`, globs, and `$VAR`
    expansions that the agent put in the command deliberately. Operators and
    benign tokens pass through verbatim; only tokens whose embedded spaces or
    quotes came from the original quoting are re-quoted.
    """
    if _OPERATOR_RE.match(token) or _RAW_SAFE_RE.match(token):
        return token
    return shlex.quote(token)


class VirtualPathShellBackend(LocalShellBackend):
    """`LocalShellBackend` that rewrites `/virtual/path` tokens to real disk paths.

    With `virtual_mode=True` the filesystem tools speak in virtual paths
    (`/tailored_resume/foo.yaml` maps to `<root_dir>/tailored_resume/foo.yaml`).
    The middleware's `execute` tool forwards the command string verbatim to
    `subprocess.run`, so a virtual path would be misread as a real absolute
    path on container disk. This subclass closes that gap: any `/`-prefixed
    token whose target (or whose parent dir) exists under `root_dir` is
    rewritten to its on-disk absolute form. Real absolute paths like
    `/tmp/foo` or `/usr/bin/python` are left alone because they neither
    exist nor have a parent under `root_dir`.
    """

    def execute(self, command: str, *, timeout: int | None = None) -> ExecuteResponse:
        """Translate virtual paths in `command`, then delegate to the parent backend."""
        return super().execute(self._translate(command), timeout=timeout)

    def _translate(self, command: str) -> str:
        try:
            tokens = shlex.split(command, posix=True)
        except ValueError:
            # Unbalanced quotes — let the shell surface the real error.
            return command
        rewritten = [self._rewrite_token(t) for t in tokens]
        if rewritten == tokens:
            # Nothing to rewrite — return the original string byte-for-byte so
            # all of the caller's quoting (incl. quoted pipes/globs) survives.
            return command
        out = command
        cursor = 0
        for orig, new in zip(tokens, rewritten, strict=True):
            if new == orig:
                continue
            idx = out.find(orig, cursor)
            if idx == -1:
                # Token only survives via escaping/quoting; splice we can't
                # anchor — fall back to the token joiner (still operator-safe).
                return " ".join(_emit_token(t) for t in rewritten)
            # Quoted tokens keep the caller's surrounding quotes (replace the
            # inner text verbatim); bare tokens get re-quoted if needed.
            piece = new if orig != shlex.join([orig]) else _emit_token(new)
            out = out[:idx] + piece + out[idx + len(orig) :]
            # The replacement covers the old token; resume search after it so
            # repeated or prefix-overlapping tokens remap in command order.
            cursor = idx + len(piece)
        return out

    def _rewrite_token(self, token: str) -> str:
        if not token.startswith("/"):
            return token
        root = Path(self.cwd).resolve()
        candidate = (root / token.lstrip("/")).resolve()
        # Reject paths that escape root_dir via `..` — those are real absolute
        # paths the user intends, not virtual paths.
        try:
            candidate.relative_to(root)
        except ValueError:
            return token
        if candidate.exists() or candidate.parent.exists():
            return str(candidate)
        return token
