from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from . import ast
from .bytecode import Code, Instr
from .runtime import Builtin, Closure, Env, StackFrame, SuayRuntimeError, UNIT, Unit, Variant


def _is_truthy(v: object) -> bool:
    if v is UNIT:
        return False
    if isinstance(v, bool):
        return v
    return True


def _is_number(v: object) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _to_text(v: object) -> str:
    if v is UNIT:
        return "ø"
    if isinstance(v, bool):
        return "⊤" if v else "⊥"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return v
    if isinstance(v, tuple):
        return "(" + " ".join(_to_text(x) for x in v) + ")"
    if isinstance(v, list):
        return "[" + " ".join(_to_text(x) for x in v) + "]"
    if isinstance(v, dict):
        inner = ", ".join(f"{_to_text(k)} ↦ {_to_text(val)}" for k, val in v.items())
        return "⟦" + inner + "⟧"
    if isinstance(v, Variant):
        return f"{v.tag}•{_to_text(v.payload)}"
    if isinstance(v, ClosureBC):
        return f"<⌁ {v.name or 'anon'}>"
    if isinstance(v, Builtin):
        return f"<builtin {v.name}>"
    if isinstance(v, Closure):
        return f"<⌁ {v.name or 'anon'}>"
    return str(v)


@dataclass(frozen=True)
class ClosureBC:
    params: list[ast.Pattern]
    code: Code
    env: Env
    name: str | None = None


class VM:
    def __init__(self, *, source: str, filename: str | None = None, trace: bool = False) -> None:
        self.source = source
        self.filename = filename
        self.trace = trace
        self._depth = 0

    def run(self, code: Code) -> object:
        env = Env(parent=None)
        self._install_builtins(env)
        return self.run_in_env(code, env)

    def run_in_env(self, code: Code, env: Env) -> object:
        stack: list[object] = []
        pc = 0

        while pc < len(code.instrs):
            ins = code.instrs[pc]
            if self.trace:
                self._trace_step(code, pc, ins, stack)

            try:
                op = ins.op
                if op == "CONST":
                    stack.append(ins.arg)
                elif op == "LOAD":
                    try:
                        stack.append(env.get(str(ins.arg)))
                    except KeyError:
                        raise SuayRuntimeError(
                            f"Undefined name {ins.arg!r}",
                            span=ins.span,
                            source=self.source,
                            filename=self.filename,
                        )
                elif op == "DEF":
                    val = stack.pop()
                    try:
                        env.define(str(ins.arg), val)
                    except KeyError:
                        raise SuayRuntimeError(
                            f"Name {ins.arg!r} is already bound in this scope",
                            span=ins.span,
                            source=self.source,
                            filename=self.filename,
                        )
                    stack.append(val)
                elif op == "SET":
                    val = stack.pop()
                    try:
                        env.set_existing(str(ins.arg), val)
                    except KeyError:
                        raise SuayRuntimeError(
                            f"Cannot mutate {ins.arg!r}: name is not bound in any enclosing scope",
                            span=ins.span,
                            source=self.source,
                            filename=self.filename,
                        )
                    stack.append(val)
                elif op == "POP":
                    stack.pop()
                elif op == "DUP":
                    stack.append(stack[-1])
                elif op == "PUSH_ENV":
                    env = Env(parent=env)
                elif op == "POP_ENV":
                    assert env.parent is not None
                    env = env.parent
                elif op == "PUSH_ENV_BIND":
                    binds = stack.pop()
                    if not isinstance(binds, dict):
                        raise SuayRuntimeError(
                            "Internal VM error: PUSH_ENV_BIND expects dict",
                            span=ins.span,
                            source=self.source,
                            filename=self.filename,
                        )
                    child = Env(parent=env)
                    for k, v in binds.items():
                        child.define(str(k), v)
                    env = child
                elif op == "MAKE_TUPLE":
                    n = int(ins.arg)
                    items = [stack.pop() for _ in range(n)][::-1]
                    stack.append(tuple(items))
                elif op == "MAKE_LIST":
                    n = int(ins.arg)
                    items = [stack.pop() for _ in range(n)][::-1]
                    stack.append(items)
                elif op == "MAKE_MAP":
                    n = int(ins.arg)
                    out: dict[object, object] = {}
                    for _ in range(n):
                        v = stack.pop()
                        k = stack.pop()
                        try:
                            out[k] = v
                        except TypeError as e:
                            raise SuayRuntimeError(
                                f"Invalid map key (unhashable): {e}",
                                span=ins.span,
                                source=self.source,
                                filename=self.filename,
                            )
                    stack.append(out)
                elif op == "MAKE_VARIANT":
                    payload = stack.pop()
                    stack.append(Variant(tag=str(ins.arg), payload=payload))
                elif op == "MAKE_CLOSURE":
                    code_obj, params = ins.arg
                    stack.append(ClosureBC(params=list(params), code=code_obj, env=env, name=None))
                elif op == "CALL":
                    arg = stack.pop()
                    fn = stack.pop()
                    stack.append(self._apply(fn, arg, call_span=ins.span))
                elif op == "UNARY":
                    rhs = stack.pop()
                    opx = str(ins.arg)
                    if opx == "¬":
                        stack.append(not _is_truthy(rhs))
                    elif opx in ("−", "-"):
                        if not _is_number(rhs):
                            raise SuayRuntimeError(
                                f"Unary minus expects a number, got {type(rhs).__name__}",
                                span=ins.span,
                                source=self.source,
                                filename=self.filename,
                            )
                        stack.append(-rhs)  # type: ignore[operator]
                    else:
                        raise SuayRuntimeError(
                            f"Unknown unary operator {opx!r}",
                            span=ins.span,
                            source=self.source,
                            filename=self.filename,
                        )
                elif op == "BINARY":
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(self._binary(str(ins.arg), left, right, span=ins.span))
                elif op == "TO_BOOL":
                    stack.append(_is_truthy(stack.pop()))
                elif op == "JMP":
                    pc = int(ins.arg)
                    continue
                elif op == "JMP_IF_FALSE":
                    v = stack.pop()
                    if not _is_truthy(v):
                        pc = int(ins.arg)
                        continue
                elif op == "JMP_IF_TRUE":
                    v = stack.pop()
                    if _is_truthy(v):
                        pc = int(ins.arg)
                        continue
                elif op == "MATCH":
                    v = stack.pop()
                    binds = self._match_pattern(ins.arg, v, span=ins.span)
                    stack.append(binds)
                elif op == "JMP_IF_NONE":
                    top = stack.pop()
                    if top is None:
                        pc = int(ins.arg)
                        continue
                    stack.append(top)
                elif op == "RAISE":
                    raise SuayRuntimeError(
                        str(ins.arg),
                        span=ins.span,
                        source=self.source,
                        filename=self.filename,
                    )
                elif op == "HALT":
                    return stack[-1] if stack else UNIT
                else:
                    raise SuayRuntimeError(
                        f"Unknown opcode {op}",
                        span=ins.span,
                        source=self.source,
                        filename=self.filename,
                    )

            except SuayRuntimeError:
                raise
            except RecursionError:
                raise SuayRuntimeError(
                    "Maximum recursion depth exceeded",
                    span=ins.span,
                    source=self.source,
                    filename=self.filename,
                )
            except Exception as e:
                raise SuayRuntimeError(
                    f"Internal VM error: {type(e).__name__}: {e}",
                    span=ins.span,
                    source=self.source,
                    filename=self.filename,
                )

            pc += 1

        return stack[-1] if stack else UNIT

    # -------- Builtins --------

    def _install_builtins(self, env: Env) -> None:
        def say(x: object) -> Unit:
            print(_to_text(x))
            return UNIT

        def hear(prompt: object) -> str:
            try:
                p = _to_text(prompt)
                return input(p)
            except EOFError:
                return ""

        def text(x: object) -> str:
            return _to_text(x)

        def abs1(x: object) -> int | float:
            if not _is_number(x):
                raise SuayRuntimeError(
                    f"abs expects a number, got {type(x).__name__}",
                    source=self.source,
                    filename=self.filename,
                )
            return -x if x < 0 else x  # type: ignore[operator]

        def count1(x: object) -> int:
            if isinstance(x, (str, list, tuple, dict)):
                return len(x)
            raise SuayRuntimeError(
                f"count expects Text, List, Tuple, or Map; got {type(x).__name__}",
                source=self.source,
                filename=self.filename,
            )

        def at2(xs: object, i: object) -> object:
            if not isinstance(i, int) or isinstance(i, bool):
                raise SuayRuntimeError(
                    f"at expects an Int index; got {type(i).__name__}",
                    source=self.source,
                    filename=self.filename,
                )

            if isinstance(xs, str):
                n = len(xs)
                j = i if i >= 0 else n + i
                if j < 0 or j >= n:
                    raise SuayRuntimeError(
                        f"Index {i} out of range for Text of length {n}",
                        source=self.source,
                        filename=self.filename,
                    )
                return xs[j]

            if isinstance(xs, (list, tuple)):
                n = len(xs)
                j = i if i >= 0 else n + i
                if j < 0 or j >= n:
                    raise SuayRuntimeError(
                        f"Index {i} out of range for sequence of length {n}",
                        source=self.source,
                        filename=self.filename,
                    )
                return xs[j]

            raise SuayRuntimeError(
                f"at expects Text, List, or Tuple; got {type(xs).__name__}",
                source=self.source,
                filename=self.filename,
            )

        def take2(xs: object, n: object) -> object:
            if not isinstance(n, int) or isinstance(n, bool):
                raise SuayRuntimeError(
                    f"take expects an Int count; got {type(n).__name__}",
                    source=self.source,
                    filename=self.filename,
                )
            if n < 0:
                raise SuayRuntimeError(
                    "take expects a non-negative count",
                    source=self.source,
                    filename=self.filename,
                )
            if isinstance(xs, str):
                return xs[:n]
            if isinstance(xs, list):
                return xs[:n]
            raise SuayRuntimeError(
                f"take expects Text or List; got {type(xs).__name__}",
                source=self.source,
                filename=self.filename,
            )

        def drop2(xs: object, n: object) -> object:
            if not isinstance(n, int) or isinstance(n, bool):
                raise SuayRuntimeError(
                    f"drop expects an Int count; got {type(n).__name__}",
                    source=self.source,
                    filename=self.filename,
                )
            if n < 0:
                raise SuayRuntimeError(
                    "drop expects a non-negative count",
                    source=self.source,
                    filename=self.filename,
                )
            if isinstance(xs, str):
                return xs[n:]
            if isinstance(xs, list):
                return xs[n:]
            raise SuayRuntimeError(
                f"drop expects Text or List; got {type(xs).__name__}",
                source=self.source,
                filename=self.filename,
            )

        def keys1(m: object) -> list[object]:
            if not isinstance(m, dict):
                raise SuayRuntimeError(
                    f"keys expects a Map, got {type(m).__name__}",
                    source=self.source,
                    filename=self.filename,
                )
            return list(m.keys())

        def has2(m: object, k: object) -> bool:
            if not isinstance(m, dict):
                raise SuayRuntimeError(
                    f"has expects a Map, got {type(m).__name__}",
                    source=self.source,
                    filename=self.filename,
                )
            try:
                return k in m
            except TypeError:
                raise SuayRuntimeError(
                    "has expects a hashable key",
                    source=self.source,
                    filename=self.filename,
                )

        def put3(m: object, k: object, v: object) -> dict[object, object]:
            if not isinstance(m, dict):
                raise SuayRuntimeError(
                    f"put expects a Map, got {type(m).__name__}",
                    source=self.source,
                    filename=self.filename,
                )
            out = dict(m)
            try:
                out[k] = v
            except TypeError:
                raise SuayRuntimeError(
                    "put expects a hashable key",
                    source=self.source,
                    filename=self.filename,
                )
            return out

        def map1(fn: object, xs: object) -> list[object]:
            if not isinstance(xs, list):
                raise SuayRuntimeError(
                    f"map expects a list, got {type(xs).__name__}",
                    source=self.source,
                    filename=self.filename,
                )
            out: list[object] = []
            for x in xs:
                out.append(self._apply(fn, x, call_span=None))
            return out

        def fold1(fn: object, init: object, xs: object) -> object:
            if not isinstance(xs, list):
                raise SuayRuntimeError(
                    f"fold expects a list, got {type(xs).__name__}",
                    source=self.source,
                    filename=self.filename,
                )
            acc = init
            for x in xs:
                acc = self._apply(self._apply(fn, acc, call_span=None), x, call_span=None)
            return acc

        env.define("hear", Builtin(name="hear", arity=1, impl=hear))
        env.define("say", Builtin(name="say", arity=1, impl=say))
        env.define("text", Builtin(name="text", arity=1, impl=text))
        env.define("abs", Builtin(name="abs", arity=1, impl=abs1))
        env.define("count", Builtin(name="count", arity=1, impl=count1))
        env.define("at", Builtin(name="at", arity=2, impl=at2))
        env.define("take", Builtin(name="take", arity=2, impl=take2))
        env.define("drop", Builtin(name="drop", arity=2, impl=drop2))
        env.define("keys", Builtin(name="keys", arity=1, impl=keys1))
        env.define("has", Builtin(name="has", arity=2, impl=has2))
        env.define("put", Builtin(name="put", arity=3, impl=put3))
        env.define("map", Builtin(name="map", arity=2, impl=map1))
        env.define("fold", Builtin(name="fold", arity=3, impl=fold1))

    # -------- Call / operators --------

    def _apply(self, fn_val: object, arg_val: object, *, call_span) -> object:
        if isinstance(fn_val, Builtin):
            try:
                return fn_val.apply(arg_val)
            except SuayRuntimeError as e:
                raise e.with_location(span=call_span, source=self.source, filename=self.filename)

        if isinstance(fn_val, ClosureBC):
            if not fn_val.params:
                raise SuayRuntimeError(
                    "Cannot call a function with no remaining parameters",
                    span=call_span,
                    source=self.source,
                    filename=self.filename,
                )
            first, rest = fn_val.params[0], fn_val.params[1:]
            binds = self._match_pattern(first, arg_val, span=call_span)
            if binds is None:
                raise SuayRuntimeError(
                    "Function argument did not match parameter pattern",
                    span=call_span,
                    source=self.source,
                    filename=self.filename,
                )
            call_env = Env(parent=fn_val.env)
            for k, v in binds.items():
                call_env.define(k, v)

            if rest:
                return ClosureBC(params=rest, code=fn_val.code, env=call_env, name=fn_val.name)

            try:
                return self.run_in_env(fn_val.code, call_env)
            except SuayRuntimeError as e:
                label = fn_val.name or "<lambda>"
                if call_span is not None:
                    raise e.with_frame(StackFrame(label=f"call {label}", span=call_span))
                raise

        # allow calling existing interpreter Closure objects too
        if isinstance(fn_val, Closure):
            raise SuayRuntimeError(
                "VM cannot call interpreter closures (compile the program end-to-end)",
                span=call_span,
                source=self.source,
                filename=self.filename,
            )

        raise SuayRuntimeError(
            f"Value is not callable: {type(fn_val).__name__}",
            span=call_span,
            source=self.source,
            filename=self.filename,
        )

    def _binary(self, op: str, left: object, right: object, *, span) -> object:
        try:
            if op in ("+",):
                if not _is_number(left) or not _is_number(right):
                    raise SuayRuntimeError(
                        f"+ expects numbers, got {type(left).__name__} and {type(right).__name__}",
                        span=span,
                        source=self.source,
                        filename=self.filename,
                    )
                return left + right  # type: ignore[operator]

            if op in ("−", "-"):
                if not _is_number(left) or not _is_number(right):
                    raise SuayRuntimeError(
                        f"− expects numbers, got {type(left).__name__} and {type(right).__name__}",
                        span=span,
                        source=self.source,
                        filename=self.filename,
                    )
                return left - right  # type: ignore[operator]

            if op in ("×", "*"):
                if not _is_number(left) or not _is_number(right):
                    raise SuayRuntimeError(
                        f"× expects numbers, got {type(left).__name__} and {type(right).__name__}",
                        span=span,
                        source=self.source,
                        filename=self.filename,
                    )
                return left * right  # type: ignore[operator]

            if op in ("÷", "/"):
                if not _is_number(left) or not _is_number(right):
                    raise SuayRuntimeError(
                        f"÷ expects numbers, got {type(left).__name__} and {type(right).__name__}",
                        span=span,
                        source=self.source,
                        filename=self.filename,
                    )
                return left / right  # type: ignore[operator]

            if op == "%":
                if not _is_number(left) or not _is_number(right):
                    raise SuayRuntimeError(
                        f"% expects numbers, got {type(left).__name__} and {type(right).__name__}",
                        span=span,
                        source=self.source,
                        filename=self.filename,
                    )
                return left % right  # type: ignore[operator]

            if op == "⊞":
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                if isinstance(left, list) and isinstance(right, list):
                    return [*left, *right]
                if isinstance(left, dict) and isinstance(right, dict):
                    out = dict(left)
                    out.update(right)
                    return out
                raise SuayRuntimeError(
                    f"⊞ expects (Text,Text), (List,List), or (Map,Map); got {type(left).__name__} and {type(right).__name__}",
                    span=span,
                    source=self.source,
                    filename=self.filename,
                )

            if op == "=":
                return left == right
            if op == "≠":
                return left != right

            if op == "<":
                if _is_number(left) and _is_number(right):
                    return left < right  # type: ignore[operator]
                if isinstance(left, str) and isinstance(right, str):
                    return left < right
                raise SuayRuntimeError(
                    f"< expects (Num,Num) or (Text,Text); got {type(left).__name__} and {type(right).__name__}",
                    span=span,
                    source=self.source,
                    filename=self.filename,
                )

            if op == "≤":
                if _is_number(left) and _is_number(right):
                    return left <= right  # type: ignore[operator]
                if isinstance(left, str) and isinstance(right, str):
                    return left <= right
                raise SuayRuntimeError(
                    f"≤ expects (Num,Num) or (Text,Text); got {type(left).__name__} and {type(right).__name__}",
                    span=span,
                    source=self.source,
                    filename=self.filename,
                )

            if op == ">":
                if _is_number(left) and _is_number(right):
                    return left > right  # type: ignore[operator]
                if isinstance(left, str) and isinstance(right, str):
                    return left > right
                raise SuayRuntimeError(
                    f"> expects (Num,Num) or (Text,Text); got {type(left).__name__} and {type(right).__name__}",
                    span=span,
                    source=self.source,
                    filename=self.filename,
                )

            if op == "≥":
                if _is_number(left) and _is_number(right):
                    return left >= right  # type: ignore[operator]
                if isinstance(left, str) and isinstance(right, str):
                    return left >= right
                raise SuayRuntimeError(
                    f"≥ expects (Num,Num) or (Text,Text); got {type(left).__name__} and {type(right).__name__}",
                    span=span,
                    source=self.source,
                    filename=self.filename,
                )

        except (TypeError, ZeroDivisionError) as e:
            raise SuayRuntimeError(
                f"Runtime error for operator {op!r}: {e}",
                span=span,
                source=self.source,
                filename=self.filename,
            )

        raise SuayRuntimeError(
            f"Unknown operator {op!r}",
            span=span,
            source=self.source,
            filename=self.filename,
        )

    # -------- Patterns --------

    def _match_pattern(self, pat: ast.Pattern, value: object, *, span) -> dict[str, object] | None:
        def merge_into(dst: dict[str, object], src: dict[str, object]) -> bool:
            for k, v in src.items():
                if k in dst:
                    return False
                dst[k] = v
            return True

        match pat:
            case ast.PWildcard():
                return {}
            case ast.PName(name=name):
                return {name: value}
            case ast.PUnit():
                return {} if value is UNIT else None
            case ast.PBool(value=b):
                return {} if isinstance(value, bool) and value == b else None
            case ast.PInt(value=i):
                return {} if isinstance(value, int) and value == i else None
            case ast.PDec(value=f):
                return {} if isinstance(value, float) and value == f else None
            case ast.PText(value=s):
                return {} if isinstance(value, str) and value == s else None

            case ast.PTuple(items=items):
                if not isinstance(value, tuple):
                    return None
                if len(value) != len(items):
                    return None
                out: dict[str, object] = {}
                for p, v in zip(items, value, strict=True):
                    binds = self._match_pattern(p, v, span=span)
                    if binds is None:
                        return None
                    if not merge_into(out, binds):
                        raise SuayRuntimeError(
                            "Duplicate name binder in pattern",
                            span=pat.span,
                            source=self.source,
                            filename=self.filename,
                        )
                return out

            case ast.PList(items=items, tail=tail):
                if not isinstance(value, list):
                    return None
                if tail is None and len(value) != len(items):
                    return None
                if tail is not None and len(value) < len(items):
                    return None
                out: dict[str, object] = {}
                for p, v in zip(items, value[: len(items)], strict=True):
                    binds = self._match_pattern(p, v, span=span)
                    if binds is None:
                        return None
                    if not merge_into(out, binds):
                        raise SuayRuntimeError(
                            "Duplicate name binder in pattern",
                            span=pat.span,
                            source=self.source,
                            filename=self.filename,
                        )
                if tail is None:
                    return out
                rest = value[len(items) :]
                tail_binds = self._match_pattern(tail, rest, span=span)
                if tail_binds is None:
                    return None
                if not merge_into(out, tail_binds):
                    raise SuayRuntimeError(
                        "Duplicate name binder in pattern",
                        span=pat.span,
                        source=self.source,
                        filename=self.filename,
                    )
                return out

            case ast.PVariant(tag=tag, payload=payload_pat):
                if not isinstance(value, Variant):
                    return None
                if value.tag != tag:
                    return None
                return self._match_pattern(payload_pat, value.payload, span=span)

            case _:
                raise SuayRuntimeError(
                    f"Unsupported pattern: {type(pat).__name__}",
                    span=pat.span,
                    source=self.source,
                    filename=self.filename,
                )

    def _trace_step(self, code: Code, pc: int, ins: Instr, stack: list[object]) -> None:
        pad = "  " * self._depth
        top = "" if not stack else _to_text(stack[-1])
        print(f"{pad}{code.name}:{pc:04d} {ins.op} {'' if ins.arg is None else ins.arg} | top={top}")
