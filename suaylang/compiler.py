from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from . import ast
from .bytecode import Code, Instr
from .runtime import UNIT


@dataclass
class _Patch:
    pc: int
    label: str


@dataclass
class _Builder:
    name: str
    instrs: list[Instr]
    labels: dict[str, int]
    patches: list[_Patch]

    def emit(self, op: str, arg: Any = None, *, span=None) -> int:
        self.instrs.append(Instr(op=op, arg=arg, span=span))
        return len(self.instrs) - 1

    def mark(self, label: str) -> None:
        self.labels[label] = len(self.instrs)

    def jmp(self, op: str, label: str, *, span=None) -> None:
        pc = self.emit(op, None, span=span)
        self.patches.append(_Patch(pc=pc, label=label))

    def finalize(self) -> Code:
        for p in self.patches:
            if p.label not in self.labels:
                raise ValueError(f"Unknown label: {p.label}")
            target = self.labels[p.label]
            self.instrs[p.pc] = Instr(op=self.instrs[p.pc].op, arg=target, span=self.instrs[p.pc].span)
        return Code(name=self.name, instrs=self.instrs)


class Compiler:
    """Compile SuayLang AST to a small stack-based bytecode."""

    def __init__(self) -> None:
        self._lambda_counter = 0

    def compile_program(self, program: ast.Program, *, name: str = "<main>") -> Code:
        b = _Builder(name=name, instrs=[], labels={}, patches=[])

        if not program.items:
            b.emit("CONST", UNIT, span=program.span)
            b.emit("HALT", span=program.span)
            return b.finalize()

        for i, item in enumerate(program.items):
            self._compile_expr(b, item)
            if i != len(program.items) - 1:
                b.emit("POP", span=item.span)

        b.emit("HALT", span=program.span)
        return b.finalize()

    # -------- Expressions --------

    def _compile_expr(self, b: _Builder, e: ast.Expr) -> None:
        match e:
            case ast.UnitLit():
                b.emit("CONST", UNIT, span=e.span)
            case ast.BoolLit(value=v):
                b.emit("CONST", bool(v), span=e.span)
            case ast.IntLit(value=v):
                b.emit("CONST", int(v), span=e.span)
            case ast.DecLit(value=v):
                b.emit("CONST", float(v), span=e.span)
            case ast.TextLit(value=v):
                b.emit("CONST", str(v), span=e.span)

            case ast.Name(value=name):
                b.emit("LOAD", name, span=e.span)

            case ast.Binding(name=name, value=value_expr):
                self._compile_expr(b, value_expr)
                b.emit("DEF", name, span=e.span)

            case ast.Mutation(name=name, value=value_expr):
                self._compile_expr(b, value_expr)
                b.emit("SET", name, span=e.span)

            case ast.Block(items=items):
                b.emit("PUSH_ENV", span=e.span)
                for idx, it in enumerate(items):
                    self._compile_expr(b, it)
                    if idx != len(items) - 1:
                        b.emit("POP", span=it.span)
                b.emit("POP_ENV", span=e.span)

            case ast.TupleExpr(items=items):
                for it in items:
                    self._compile_expr(b, it)
                b.emit("MAKE_TUPLE", len(items), span=e.span)

            case ast.ListExpr(items=items):
                for it in items:
                    self._compile_expr(b, it)
                b.emit("MAKE_LIST", len(items), span=e.span)

            case ast.MapExpr(entries=entries):
                for k, v in entries:
                    self._compile_expr(b, k)
                    self._compile_expr(b, v)
                b.emit("MAKE_MAP", len(entries), span=e.span)

            case ast.VariantExpr(tag=tag, payload=payload):
                self._compile_expr(b, payload)
                b.emit("MAKE_VARIANT", str(tag), span=e.span)

            case ast.Lambda(params=params, body=body):
                self._lambda_counter += 1
                code_name = f"<lambda:{self._lambda_counter}>"
                body_code = self.compile_expr(body, name=code_name)
                b.emit("MAKE_CLOSURE", (body_code, params), span=e.span)

            case ast.Call(func=fn, arg=arg):
                self._compile_expr(b, fn)
                self._compile_expr(b, arg)
                b.emit("CALL", span=e.span)

            case ast.Unary(op=op, expr=rhs):
                self._compile_expr(b, rhs)
                b.emit("UNARY", op, span=e.span)

            case ast.Binary(op=op, left=lhs, right=rhs):
                if op == "∧":
                    # left; if falsy -> False; else right -> bool
                    false_lbl = self._fresh("and_false")
                    end_lbl = self._fresh("and_end")
                    self._compile_expr(b, lhs)
                    b.jmp("JMP_IF_FALSE", false_lbl, span=e.span)
                    self._compile_expr(b, rhs)
                    b.emit("TO_BOOL", span=e.span)
                    b.jmp("JMP", end_lbl, span=e.span)
                    b.mark(false_lbl)
                    b.emit("CONST", False, span=e.span)
                    b.mark(end_lbl)
                    return

                if op == "∨":
                    # left; if truthy -> True; else right -> bool
                    true_lbl = self._fresh("or_true")
                    end_lbl = self._fresh("or_end")
                    self._compile_expr(b, lhs)
                    b.jmp("JMP_IF_TRUE", true_lbl, span=e.span)
                    self._compile_expr(b, rhs)
                    b.emit("TO_BOOL", span=e.span)
                    b.jmp("JMP", end_lbl, span=e.span)
                    b.mark(true_lbl)
                    b.emit("CONST", True, span=e.span)
                    b.mark(end_lbl)
                    return

                self._compile_expr(b, lhs)
                self._compile_expr(b, rhs)
                b.emit("BINARY", op, span=e.span)

            case ast.Dispatch(value=value_expr, arms=arms):
                end_lbl = self._fresh("dispatch_end")
                self._compile_expr(b, value_expr)  # scrutinee on stack
                for arm in arms:
                    next_lbl = self._fresh("dispatch_next")
                    b.emit("DUP", span=arm.span)
                    b.emit("MATCH", arm.pattern, span=arm.span)
                    b.jmp("JMP_IF_NONE", next_lbl, span=arm.span)
                    b.emit("PUSH_ENV_BIND", span=arm.span)  # consumes bindings
                    b.emit("POP", span=arm.span)  # drop scrutinee
                    self._compile_expr(b, arm.expr)
                    b.emit("POP_ENV", span=arm.span)
                    b.jmp("JMP", end_lbl, span=arm.span)
                    b.mark(next_lbl)
                # no match
                b.emit("POP", span=e.span)  # drop scrutinee
                b.emit("RAISE", "No dispatch arm matched", span=e.span)
                b.mark(end_lbl)

            case ast.Cycle(seed=seed_expr, arms=arms):
                loop_lbl = self._fresh("cycle_loop")
                end_lbl = self._fresh("cycle_end")
                self._compile_expr(b, seed_expr)  # state
                b.mark(loop_lbl)
                for arm in arms:
                    next_lbl = self._fresh("cycle_next")
                    b.emit("DUP", span=arm.span)
                    b.emit("MATCH", arm.pattern, span=arm.span)
                    b.jmp("JMP_IF_NONE", next_lbl, span=arm.span)
                    b.emit("PUSH_ENV_BIND", span=arm.span)
                    b.emit("POP", span=arm.span)  # drop state
                    self._compile_expr(b, arm.expr)
                    b.emit("POP_ENV", span=arm.span)
                    if arm.mode == "continue":
                        b.jmp("JMP", loop_lbl, span=arm.span)
                    else:
                        b.jmp("JMP", end_lbl, span=arm.span)
                    b.mark(next_lbl)
                b.emit("POP", span=e.span)  # drop state
                b.emit("RAISE", "No cycle arm matched", span=e.span)
                b.mark(end_lbl)

            case _:
                raise NotImplementedError(f"No compiler support for {type(e).__name__}")

    def compile_expr(self, expr: ast.Expr, *, name: str = "<expr>") -> Code:
        b = _Builder(name=name, instrs=[], labels={}, patches=[])
        self._compile_expr(b, expr)
        b.emit("HALT", span=expr.span)
        return b.finalize()

    def _fresh(self, prefix: str) -> str:
        self._lambda_counter += 1
        return f"{prefix}_{self._lambda_counter}"
