from __future__ import annotations

from dataclasses import dataclass

from .errors import Diagnostic
from .tokens import Position, Span, Token, TokenType


class LexError(Diagnostic):
    pass


_SYMBOLS: dict[str, TokenType] = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "[": TokenType.LBRACK,
    "]": TokenType.RBRACK,
    ",": TokenType.COMMA,

    "⟦": TokenType.LDBRACK,
    "⟧": TokenType.RDBRACK,
    "⟪": TokenType.LDBLOCK,
    "⟫": TokenType.RDBLOCK,

    "←": TokenType.ARROW_BIND,
    "⇐": TokenType.ARROW_SET,
    "↦": TokenType.ARROW_MAP,
    "⇒": TokenType.FAT_ARROW,

    "▷": TokenType.DISPATCH,
    "⟲": TokenType.CYCLE,

    "↩": TokenType.CONTINUE,
    "↯": TokenType.FINISH,

    "•": TokenType.BULLET,
    "⋯": TokenType.ELLIPSIS,

    "⌁": TokenType.LAMBDA,

    "ø": TokenType.UNIT,
    "⊤": TokenType.TRUE,
    "⊥": TokenType.FALSE,

    "¬": TokenType.NOT,

    "×": TokenType.MUL,
    "÷": TokenType.DIV,
    "*": TokenType.MUL,
    "/": TokenType.DIV,
    "%": TokenType.MOD,

    "+": TokenType.PLUS,
    "−": TokenType.MINUS,
    "-": TokenType.MINUS,
    "⊞": TokenType.CONCAT,

    "=": TokenType.EQ,
    "≠": TokenType.NEQ,
    "<": TokenType.LT,
    "≤": TokenType.LTE,
    ">": TokenType.GT,
    "≥": TokenType.GTE,

    "∧": TokenType.AND,
    "∨": TokenType.OR,

    "·": TokenType.CALL,
}


def _is_ident_start(ch: str) -> bool:
    if ch == "_":
        return True
    # Allow Unicode letters as starts. Exclude most operator/punct chars via a conservative check.
    return ch.isalpha()


def _is_ident_continue(ch: str) -> bool:
    return ch == "_" or ch.isalpha() or ch.isdigit()


@dataclass
class Lexer:
    source: str
    filename: str | None = None

    def __post_init__(self) -> None:
        self._i = 0
        self._line = 1
        self._col = 1
        self._line_start = 0

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        try:
            while True:
                self._skip_ws_and_comments(tokens)
                if self._at_end():
                    tokens.append(self._make_token(TokenType.EOF, "", None))
                    return tokens

                ch = self._peek()

                if ch == "\n":
                    start = self._pos()
                    self._advance()
                    end = self._pos()
                    tokens.append(Token(TokenType.NEWLINE, "\n", Span(start, end)))
                    continue

                if ch == '"':
                    tokens.append(self._lex_string())
                    continue

                if ch.isdigit():
                    tokens.append(self._lex_number())
                    continue

                # Symbols (including alphabetic-looking glyphs like ø/⊤/⊥) must be recognized
                # before identifier lexing.
                if ch in _SYMBOLS:
                    tokens.append(self._lex_symbol())
                    continue

                if _is_ident_start(ch):
                    tokens.append(self._lex_ident_or_underscore())
                    continue

                # Two-character (currently none) could be handled here if added later.

                self._error(f"Unexpected character {ch!r}")
        except LexError:
            raise
        except Exception as e:
            # Defensive: convert internal lexer failures into a user-facing LexError.
            self._error(f"Internal lexer error: {type(e).__name__}: {e}")

    def _skip_ws_and_comments(self, tokens: list[Token]) -> None:
        while not self._at_end():
            ch = self._peek()
            # Spaces/tabs are insignificant separators.
            if ch in (" ", "\t", "\r"):
                self._advance()
                continue
            # Comment: ⍝ ... end of line (but keep newline token).
            if ch == "⍝":
                while not self._at_end() and self._peek() != "\n":
                    self._advance()
                continue
            break

    def _lex_symbol(self) -> Token:
        start = self._pos()
        ch = self._advance()
        end = self._pos()
        return Token(_SYMBOLS[ch], ch, Span(start, end))

    def _lex_ident_or_underscore(self) -> Token:
        start = self._pos()
        s = []
        while not self._at_end() and _is_ident_continue(self._peek()):
            s.append(self._advance())
        lexeme = "".join(s)
        end = self._pos()
        if lexeme == "_":
            return Token(TokenType.UNDERSCORE, lexeme, Span(start, end))
        return Token(TokenType.IDENT, lexeme, Span(start, end), value=lexeme)

    def _lex_number(self) -> Token:
        start = self._pos()
        digits = []
        while not self._at_end() and self._peek().isdigit():
            digits.append(self._advance())

        is_dec = False
        if not self._at_end() and self._peek() == ".":
            # decimal: require at least one digit after '.'
            if self._peek_next().isdigit():
                is_dec = True
                digits.append(self._advance())
                while not self._at_end() and self._peek().isdigit():
                    digits.append(self._advance())

        lexeme = "".join(digits)
        end = self._pos()
        if is_dec:
            return Token(TokenType.DEC, lexeme, Span(start, end), value=float(lexeme))
        return Token(TokenType.INT, lexeme, Span(start, end), value=int(lexeme))

    def _lex_string(self) -> Token:
        start = self._pos()
        self._advance()  # opening quote
        chars: list[str] = []
        while not self._at_end() and self._peek() != '"':
            ch = self._advance()
            if ch == "\\":
                if self._at_end():
                    self._error_at(start, "Unterminated string escape")
                esc = self._advance()
                if esc == "n":
                    chars.append("\n")
                elif esc == "t":
                    chars.append("\t")
                elif esc == '"':
                    chars.append('"')
                elif esc == "\\":
                    chars.append("\\")
                else:
                    self._error_at(start, f"Unknown string escape \\{esc}")
            elif ch == "\n":
                self._error_at(start, "Unterminated string literal")
            else:
                chars.append(ch)

        if self._at_end():
            self._error_at(start, "Unterminated string literal")

        self._advance()  # closing quote
        end = self._pos()
        lexeme = self.source[start.offset : end.offset]
        return Token(TokenType.STRING, lexeme, Span(start, end), value="".join(chars))

    def _error_at(self, pos: Position, message: str) -> None:
        # Produce a LexError anchored at a given source position.
        line_start = pos.offset - (max(pos.column, 1) - 1)
        if line_start < 0:
            line_start = 0
        line_end = self.source.find("\n", line_start)
        if line_end == -1:
            line_end = len(self.source)
        line_text = self.source[line_start:line_end] if self.source else None
        raise LexError(
            error_type="lexical",
            message=message,
            line=pos.line,
            column=pos.column,
            filename=self.filename,
            source=self.source,
            context_line=line_text,
        )

    def _make_token(self, typ: TokenType, lexeme: str, value: object | None) -> Token:
        pos = self._pos()
        return Token(typ, lexeme, Span(pos, pos), value=value)

    def _pos(self) -> Position:
        return Position(self._i, self._line, self._col)

    def _at_end(self) -> bool:
        return self._i >= len(self.source)

    def _peek(self) -> str:
        return self.source[self._i]

    def _peek_next(self) -> str:
        j = self._i + 1
        return self.source[j] if j < len(self.source) else "\0"

    def _advance(self) -> str:
        ch = self.source[self._i]
        self._i += 1
        if ch == "\n":
            self._line += 1
            self._col = 1
            self._line_start = self._i
        else:
            self._col += 1
        return ch

    def _error(self, message: str) -> None:
        line_text = self._current_line_text()
        raise LexError(
            error_type="lexical",
            message=message,
            line=self._line,
            column=self._col,
            filename=self.filename,
            source=self.source,
            context_line=line_text,
        )

    def _current_line_text(self) -> str | None:
        if not self.source:
            return None
        start = self._line_start
        end = self.source.find("\n", start)
        if end == -1:
            end = len(self.source)
        return self.source[start:end]
