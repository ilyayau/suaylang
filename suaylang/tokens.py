from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Position:
    offset: int
    line: int
    column: int


@dataclass(frozen=True)
class Span:
    start: Position
    end: Position


class TokenType(str, Enum):
    EOF = "EOF"
    NEWLINE = "NEWLINE"

    IDENT = "IDENT"
    INT = "INT"
    DEC = "DEC"
    STRING = "STRING"

    UNDERSCORE = "UNDERSCORE"  # _ wildcard (also a valid identifier in many langs; reserved for patterns here)

    LPAREN = "LPAREN"  # (
    RPAREN = "RPAREN"  # )
    LBRACK = "LBRACK"  # [
    RBRACK = "RBRACK"  # ]

    LDBRACK = "LDBRACK"  # ⟦
    RDBRACK = "RDBRACK"  # ⟧

    LDBLOCK = "LDBLOCK"  # ⟪
    RDBLOCK = "RDBLOCK"  # ⟫

    COMMA = "COMMA"  # ,

    ARROW_BIND = "ARROW_BIND"  # ←
    ARROW_SET = "ARROW_SET"  # ⇐ (explicit mutation)
    ARROW_MAP = "ARROW_MAP"  # ↦
    FAT_ARROW = "FAT_ARROW"  # ⇒

    DISPATCH = "DISPATCH"  # ▷
    CYCLE = "CYCLE"  # ⟲

    CONTINUE = "CONTINUE"  # ↩
    FINISH = "FINISH"  # ↯

    BULLET = "BULLET"  # •
    ELLIPSIS = "ELLIPSIS"  # ⋯

    LAMBDA = "LAMBDA"  # ⌁

    UNIT = "UNIT"  # ø
    TRUE = "TRUE"  # ⊤
    FALSE = "FALSE"  # ⊥

    NOT = "NOT"  # ¬

    MUL = "MUL"  # ×
    DIV = "DIV"  # ÷
    MOD = "MOD"  # %

    PLUS = "PLUS"  # +
    MINUS = "MINUS"  # − (U+2212)
    CONCAT = "CONCAT"  # ⊞

    EQ = "EQ"  # =
    NEQ = "NEQ"  # ≠
    LT = "LT"  # <
    LTE = "LTE"  # ≤
    GT = "GT"  # >
    GTE = "GTE"  # ≥

    AND = "AND"  # ∧
    OR = "OR"  # ∨

    CALL = "CALL"  # ·


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    span: Span
    value: object | None = None
