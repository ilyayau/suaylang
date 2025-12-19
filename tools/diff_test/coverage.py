from __future__ import annotations

from dataclasses import is_dataclass

from suaylang.bytecode import Code
from suaylang.compiler import Compiler
from suaylang.lexer import Lexer
from suaylang.parser import Parser


def ast_node_counts(source: str, *, filename: str) -> dict[str, int]:
    tokens = Lexer(source, filename=filename).tokenize()
    program = Parser(tokens, source, filename=filename).parse_program()

    counts: dict[str, int] = {}

    def walk(node: object) -> None:
        if is_dataclass(node):
            t = type(node).__name__
            counts[t] = counts.get(t, 0) + 1
            for name in getattr(node, "__dataclass_fields__").keys():
                if name == "span":
                    continue
                walk(getattr(node, name))
            return
        if isinstance(node, list):
            for x in node:
                walk(x)
            return
        if isinstance(node, tuple):
            for x in node:
                walk(x)
            return
        if isinstance(node, dict):
            for v in node.values():
                walk(v)
            return

    walk(program)
    return counts


def opcode_counts(source: str, *, filename: str) -> dict[str, int]:
    tokens = Lexer(source, filename=filename).tokenize()
    program = Parser(tokens, source, filename=filename).parse_program()
    code = Compiler().compile_program(program, name=filename)

    seen: set[int] = set()
    counts: dict[str, int] = {}

    def walk(c: Code) -> None:
        cid = id(c)
        if cid in seen:
            return
        seen.add(cid)
        for ins in c.instrs:
            counts[ins.op] = counts.get(ins.op, 0) + 1
            arg = ins.arg
            if isinstance(arg, Code):
                walk(arg)
            elif isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], Code):
                walk(arg[0])

    walk(code)
    return counts
