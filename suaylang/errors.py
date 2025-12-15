from __future__ import annotations

from dataclasses import dataclass
class SuayError(Exception):
    """Base class for user-facing SuayLang errors."""



def _line_text(source: str, line: int) -> str | None:
    if line <= 0:
        return None
    i = 1
    start = 0
    while i < line and start <= len(source):
        nl = source.find("\n", start)
        if nl == -1:
            return None
        start = nl + 1
        i += 1
    end = source.find("\n", start)
    if end == -1:
        end = len(source)
    return source[start:end]


@dataclass(frozen=True)
class Diagnostic(SuayError):
    error_type: str
    message: str
    line: int
    column: int
    filename: str | None = None
    source: str | None = None
    context_line: str | None = None

    def __str__(self) -> str:
        loc = f"{self.line}:{self.column}"
        prefix = f"{self.filename}:{loc}" if self.filename else loc
        out = f"{prefix}: {self.error_type} error: {self.message}"

        ctx = self.context_line
        if ctx is None and self.source is not None:
            ctx = _line_text(self.source, self.line)
        if ctx is not None:
            caret = " " * (max(self.column, 1) - 1) + "^"
            out += f"\n{ctx}\n{caret}"
        return out
