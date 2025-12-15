from __future__ import annotations

from dataclasses import dataclass

from .tokens import Span


# ---------- Base Nodes ----------


@dataclass(frozen=True)
class Node:
    span: Span


@dataclass(frozen=True)
class Expr(Node):
    pass


@dataclass(frozen=True)
class Pattern(Node):
    pass


# ---------- Program ----------


@dataclass(frozen=True)
class Program(Node):
    items: list[Expr]


# ---------- Expressions ----------


@dataclass(frozen=True)
class Name(Expr):
    value: str


@dataclass(frozen=True)
class UnitLit(Expr):
    pass


@dataclass(frozen=True)
class BoolLit(Expr):
    value: bool


@dataclass(frozen=True)
class IntLit(Expr):
    value: int


@dataclass(frozen=True)
class DecLit(Expr):
    value: float


@dataclass(frozen=True)
class TextLit(Expr):
    value: str


@dataclass(frozen=True)
class TupleExpr(Expr):
    items: list[Expr]


@dataclass(frozen=True)
class ListExpr(Expr):
    items: list[Expr]


@dataclass(frozen=True)
class MapExpr(Expr):
    entries: list[tuple[Expr, Expr]]


@dataclass(frozen=True)
class VariantExpr(Expr):
    tag: str
    payload: Expr


@dataclass(frozen=True)
class Binding(Expr):
    name: str
    value: Expr


@dataclass(frozen=True)
class Mutation(Expr):
    name: str
    value: Expr


@dataclass(frozen=True)
class Block(Expr):
    items: list[Expr]


@dataclass(frozen=True)
class Lambda(Expr):
    params: list[Pattern]
    body: Expr


@dataclass(frozen=True)
class Call(Expr):
    func: Expr
    arg: Expr


@dataclass(frozen=True)
class Unary(Expr):
    op: str
    expr: Expr


@dataclass(frozen=True)
class Binary(Expr):
    op: str
    left: Expr
    right: Expr


@dataclass(frozen=True)
class DispatchArm(Node):
    pattern: Pattern
    expr: Expr


@dataclass(frozen=True)
class Dispatch(Expr):
    value: Expr
    arms: list[DispatchArm]


@dataclass(frozen=True)
class CycleArm(Node):
    pattern: Pattern
    mode: str  # "continue" | "finish"
    expr: Expr


@dataclass(frozen=True)
class Cycle(Expr):
    seed: Expr
    arms: list[CycleArm]


# ---------- Patterns ----------


@dataclass(frozen=True)
class PWildcard(Pattern):
    pass


@dataclass(frozen=True)
class PName(Pattern):
    name: str


@dataclass(frozen=True)
class PUnit(Pattern):
    pass


@dataclass(frozen=True)
class PBool(Pattern):
    value: bool


@dataclass(frozen=True)
class PInt(Pattern):
    value: int


@dataclass(frozen=True)
class PDec(Pattern):
    value: float


@dataclass(frozen=True)
class PText(Pattern):
    value: str


@dataclass(frozen=True)
class PTuple(Pattern):
    items: list[Pattern]


@dataclass(frozen=True)
class PList(Pattern):
    items: list[Pattern]
    tail: Pattern | None  # must be PName or PWildcard in MVP


@dataclass(frozen=True)
class PVariant(Pattern):
    tag: str
    payload: Pattern
