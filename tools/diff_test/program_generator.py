from __future__ import annotations

import random
from dataclasses import dataclass


# --------- Small source-AST used only for generation ---------


class GExpr:
    def render(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class GLit(GExpr):
    s: str

    def render(self) -> str:
        return self.s


@dataclass(frozen=True)
class GName(GExpr):
    name: str

    def render(self) -> str:
        return self.name


@dataclass(frozen=True)
class GBin(GExpr):
    op: str
    left: GExpr
    right: GExpr

    def render(self) -> str:
        return f"({self.left.render()} {self.op} {self.right.render()})"


@dataclass(frozen=True)
class GCall(GExpr):
    fn: GExpr
    arg: GExpr

    def render(self) -> str:
        return f"{self.fn.render()} . {self.arg.render()}"


@dataclass(frozen=True)
class GLambda(GExpr):
    params: list[str]
    body: GExpr

    def render(self) -> str:
        ps = " ".join(self.params)
        return f"\\({ps}) {self.body.render()}"


@dataclass(frozen=True)
class GBlock(GExpr):
    lines: list[str]

    def render(self) -> str:
        inner = "\n".join(self.lines)
        return "{\n" + inner + "\n}"


@dataclass(frozen=True)
class GVariant(GExpr):
    tag: str
    payload: GExpr

    def render(self) -> str:
        return f"{self.tag}::{self.payload.render()}"


@dataclass(frozen=True)
class GTuple(GExpr):
    items: list[GExpr]

    def render(self) -> str:
        return "(" + " ".join(x.render() for x in self.items) + ")"


@dataclass(frozen=True)
class GList(GExpr):
    items: list[GExpr]

    def render(self) -> str:
        return "[" + " ".join(x.render() for x in self.items) + "]"


@dataclass(frozen=True)
class GMap(GExpr):
    items: list[tuple[GExpr, GExpr]]

    def render(self) -> str:
        inner = ", ".join(f"{k.render()} -> {v.render()}" for k, v in self.items)
        return "[[ " + inner + " ]]"


def _ident(rng: random.Random) -> str:
    base = ["x", "y", "z", "a", "b", "n", "m", "acc", "i", "v", "t"]
    return rng.choice(base) + ("" if rng.random() < 0.7 else str(rng.randint(0, 9)))


def _lit(rng: random.Random) -> GLit:
    r = rng.random()
    if r < 0.25:
        return GLit(str(rng.randint(-5, 20)))
    if r < 0.45:
        return GLit(repr(rng.choice(["a", "b", "hi", "ok", "err", "mext"])))
    if r < 0.60:
        return GLit("#t" if rng.random() < 0.5 else "#f")
    if r < 0.75:
        return GLit("#u")
    return GLit(str(rng.randint(0, 3)) + "." + str(rng.randint(0, 9)))


def _expr(rng: random.Random, *, depth: int, names: list[str]) -> GExpr:
    if depth <= 0:
        if names and rng.random() < 0.6:
            return GName(rng.choice(names))
        return _lit(rng)

    choice = rng.random()
    if choice < 0.18:
        return GBin(rng.choice(["+", "-", "*", "/", "<=", ">=", "!=", "="]), _expr(rng, depth=depth - 1, names=names), _expr(rng, depth=depth - 1, names=names))
    if choice < 0.36:
        return GCall(_expr(rng, depth=depth - 1, names=names), _expr(rng, depth=depth - 1, names=names))
    if choice < 0.50:
        p1 = _ident(rng)
        p2 = _ident(rng)
        return GLambda([p1, p2], _expr(rng, depth=depth - 1, names=names + [p1, p2]))
    if choice < 0.62:
        return GVariant(rng.choice(["Ok", "Err", "Step", "Done"]), _expr(rng, depth=depth - 1, names=names))
    if choice < 0.74:
        return GTuple([_expr(rng, depth=depth - 1, names=names), _expr(rng, depth=depth - 1, names=names)])
    if choice < 0.86:
        return GList([_expr(rng, depth=depth - 1, names=names) for _ in range(rng.randint(0, 3))])
    # Map keys are often text/ints for hashability.
    items: list[tuple[GExpr, GExpr]] = []
    for _ in range(rng.randint(0, 3)):
        k: GExpr = _lit(rng)
        v = _expr(rng, depth=depth - 1, names=names)
        items.append((k, v))
    return GMap(items)


def _size_params(bucket: str) -> tuple[int, int]:
    if bucket == "small":
        return 2, 3
    if bucket == "medium":
        return 4, 6
    if bucket == "large":
        return 6, 9
    raise ValueError(f"Unknown size bucket: {bucket}")


def generate_valid_program(*, seed: int, index: int, size_bucket: str) -> str:
    rng = random.Random((seed * 1_000_003) ^ (index * 97) ^ hash(size_bucket))
    depth, nlines = _size_params(size_bucket)

    names: list[str] = []
    lines: list[str] = []

    # A few bindings, then a final expression.
    for _ in range(max(1, nlines - 1)):
        name = _ident(rng)
        rhs = _expr(rng, depth=depth, names=names).render()
        lines.append(f"{name} <- {rhs}")
        names.append(name)

    # Ensure we exercise dispatch/cycle sometimes.
    tail: str
    if rng.random() < 0.5:
        vname = rng.choice(names) if names else "x"
        tail = (
            f"{vname} |> {{\n"
            f"|> Ok::a => a\n"
            f"|> _ => 0\n"
            f"}}"
        )
    else:
        tail = (
            "~~ (Step::(1 0)) |> {\n"
            "|> Done::acc => << acc\n"
            "|> Step::(i acc) => >> ((i >= 3) |> {\n"
            "|> #t => Done::acc\n"
            "|> #f => Step::(i + 1 acc + i)\n"
            "})\n"
            "}"
        )

    lines.append(tail)
    return "\n".join(lines) + "\n"


_INVALID_MUTATIONS = [
    "drop_last_char",
    "unclosed_block",
    "bad_token",
    "unterminated_string",
    "missing_arrow",
    "undefined_name",
]


def generate_invalid_program(*, seed: int, index: int, size_bucket: str) -> tuple[str, str]:
    """Return (category, source)."""

    rng = random.Random((seed * 999_983) ^ (index * 131) ^ hash(size_bucket))
    base = generate_valid_program(seed=seed, index=index, size_bucket=size_bucket)
    mut = rng.choice(_INVALID_MUTATIONS)

    if mut == "drop_last_char":
        return mut, base[:-1]
    if mut == "unclosed_block":
        # Delete a closing brace if any.
        if "}" in base:
            return mut, base.replace("}", "", 1)
        return mut, base + "{\n"
    if mut == "bad_token":
        # Introduce a clearly invalid character for the lexer.
        return mut, base + "@\n"
    if mut == "unterminated_string":
        return mut, 'x <- "unterminated\n'
    if mut == "missing_arrow":
        return mut, base.replace("<-", " ", 1)
    if mut == "undefined_name":
        return mut, base + "z_undefined\n"

    return "unknown", base
