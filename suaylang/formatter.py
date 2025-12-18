from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .lexer import Lexer
from .tokens import Token, TokenType


# Canonical spellings for formatter output.
# NOTE: Lexer normalizes many ASCII aliases into Unicode lexemes. The formatter
# is the reverse: it can emit either ASCII-first canonical or Unicode.

ASCII_CANON: dict[TokenType, str] = {
    TokenType.LDBLOCK: "{",
    TokenType.RDBLOCK: "}",
    TokenType.LDBRACK: "[[",
    TokenType.RDBRACK: "]]",
    TokenType.ARROW_BIND: "<-",
    TokenType.ARROW_SET: "<~",
    TokenType.ARROW_MAP: "->",
    TokenType.FAT_ARROW: "=>",
    TokenType.DISPATCH: "|>",
    TokenType.CYCLE: "~~",
    TokenType.CONTINUE: ">>",
    TokenType.FINISH: "<<",
    TokenType.BULLET: "::",
    TokenType.ELLIPSIS: "...",
    TokenType.LAMBDA: "\\",
    TokenType.CALL: ".",
    TokenType.TRUE: "#t",
    TokenType.FALSE: "#f",
    TokenType.UNIT: "#u",
    TokenType.NOT: "!",
    TokenType.MUL: "*",
    TokenType.DIV: "/",
    TokenType.MINUS: "-",
    TokenType.CONCAT: "++",
    TokenType.EQ: "=",
    TokenType.NEQ: "!=",
    TokenType.LTE: "<=",
    TokenType.GTE: ">=",
    TokenType.AND: "&&",
    TokenType.OR: "||",
}

UNICODE_CANON: dict[TokenType, str] = {
    TokenType.LDBLOCK: "⟪",
    TokenType.RDBLOCK: "⟫",
    TokenType.LDBRACK: "⟦",
    TokenType.RDBRACK: "⟧",
    TokenType.ARROW_BIND: "←",
    TokenType.ARROW_SET: "⇐",
    TokenType.ARROW_MAP: "↦",
    TokenType.FAT_ARROW: "⇒",
    TokenType.DISPATCH: "▷",
    TokenType.CYCLE: "⟲",
    TokenType.CONTINUE: "↩",
    TokenType.FINISH: "↯",
    TokenType.BULLET: "•",
    TokenType.ELLIPSIS: "⋯",
    TokenType.LAMBDA: "⌁",
    TokenType.CALL: "·",
    TokenType.TRUE: "⊤",
    TokenType.FALSE: "⊥",
    TokenType.UNIT: "ø",
    TokenType.NOT: "¬",
    TokenType.MUL: "×",
    TokenType.DIV: "÷",
    TokenType.MINUS: "−",
    TokenType.CONCAT: "⊞",
    TokenType.EQ: "=",
    TokenType.NEQ: "≠",
    TokenType.LTE: "≤",
    TokenType.GTE: "≥",
    TokenType.AND: "∧",
    TokenType.OR: "∨",
}


@dataclass(frozen=True)
class FormatOptions:
    unicode: bool = False


def format_source(source: str, *, filename: str = "<fmt>", options: FormatOptions | None = None) -> str:
    """Rewrite a Suay source string into canonical ASCII (default) or Unicode.

    This formatter is intentionally *rewrite-first* (not pretty-print): it preserves
    original whitespace, newlines, and comments, and only canonicalizes token spellings.

    Guarantees:
    - Never rewrites inside string literals.
    - Never rewrites comments except via token replacement around them.
    """

    opts = options or FormatOptions()
    canon = UNICODE_CANON if opts.unicode else ASCII_CANON

    tokens = Lexer(source, filename=filename).tokenize()

    out: list[str] = []
    last = 0
    for tok in tokens:
        if tok.type == TokenType.EOF:
            break

        start = tok.span.start.offset
        end = tok.span.end.offset

        # Preserve original inter-token text (whitespace + comments).
        gap = source[last:start]
        # ASCII-first: also canonicalize the comment marker.
        if not opts.unicode and "⍝" in gap:
            gap = gap.replace("⍝", "//")
        out.append(gap)

        replacement = canon.get(tok.type)
        if replacement is None:
            # Preserve the original spelling for tokens without canonical mapping.
            replacement = source[start:end]

        out.append(replacement)
        last = end

    out.append(source[last:])
    return "".join(out)


def format_file(path: str | Path, *, options: FormatOptions | None = None) -> str:
    p = Path(path)
    src = p.read_text(encoding="utf-8")
    return format_source(src, filename=str(p), options=options)
