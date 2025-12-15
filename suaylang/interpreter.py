from __future__ import annotations

from dataclasses import dataclass
import os

from . import ast
from .errors import SuayError
from .lexer import Lexer
from .parser import Parser
from .runtime import Builtin, Closure, Env, StackFrame, SuayRuntimeError, UNIT, Unit, Variant


def _is_truthy(v: object) -> bool:
    if v is UNIT:
        return False
    if isinstance(v, bool):
        return v
    return True


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
    if isinstance(v, Closure):
        return f"<⌁ {v.name or 'anon'}>"
    if isinstance(v, Builtin):
        return f"<builtin {v.name}>"
    return str(v)


def _merge_maps(a: dict[object, object], b: dict[object, object]) -> dict[object, object]:
    out = dict(a)
    out.update(b)
    return out


def _is_number(v: object) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


@dataclass
class ModuleSystem:
    cache: dict[str, Env]
    loading: list[str]


@dataclass
class Interpreter:
    source: str
    filename: str | None = None
    trace: bool = False
    modules: ModuleSystem | None = None

    def __post_init__(self) -> None:
        self._depth = 0
        self._builtins_env = Env(parent=None)
        self._install_builtins(self._builtins_env)
        if self.modules is None:
            self.modules = ModuleSystem(cache={}, loading=[])

    def eval_program(self, program: ast.Program) -> object:
        env = Env(parent=self._builtins_env)
        result: object = UNIT
        for item in program.items:
            result = self.eval_expr(item, env)
        return result

    # ---------- Modules ----------

    def _resolve_module_path(self, raw: str) -> str:
        # Path-based resolution. Relative paths are resolved relative to the importing file.
        p = raw
        if not os.path.splitext(p)[1]:
            p = p + ".suay"
        base = os.path.dirname(os.path.abspath(self.filename)) if self.filename else os.getcwd()
        return os.path.abspath(os.path.join(base, p))

    def _load_module_env(self, abs_path: str, *, call_span) -> Env:
        assert self.modules is not None
        if abs_path in self.modules.cache:
            return self.modules.cache[abs_path]

        if abs_path in self.modules.loading:
            chain = " -> ".join([*self.modules.loading, abs_path])
            raise SuayRuntimeError(
                f"Circular module load detected: {chain}",
                span=call_span,
                source=self.source,
                filename=self.filename,
            )

        self.modules.loading.append(abs_path)
        try:
            try:
                with open(abs_path, "r", encoding="utf-8") as f:
                    mod_source = f.read()
            except OSError as e:
                raise SuayRuntimeError(
                    f"Cannot load module {abs_path!r}: {e}",
                    span=call_span,
                    source=self.source,
                    filename=self.filename,
                )

            # Each module gets its own scope (child of builtins only).
            mod_tokens = Lexer(mod_source, filename=abs_path).tokenize()
            mod_program = Parser(mod_tokens, mod_source, filename=abs_path).parse_program()
            mod_interp = Interpreter(source=mod_source, filename=abs_path, trace=self.trace, modules=self.modules)
            mod_env = Env(parent=mod_interp._builtins_env)
            for item in mod_program.items:
                mod_interp.eval_expr(item, mod_env)

            self.modules.cache[abs_path] = mod_env
            return mod_env
        except SuayRuntimeError as e:
            # Add an import stack frame at the call site (if we have one).
            if call_span is not None:
                raise e.with_frame(StackFrame(label=f"load module {abs_path}", span=call_span))
            raise
        except SuayError:
            # Lex/syntax errors are already user-facing; let them bubble.
            raise
        finally:
            self.modules.loading.pop()

    def eval_expr(self, expr: ast.Expr, env: Env) -> object:
        if self.trace:
            self._trace_enter(expr)
        try:
            v = self._eval_expr(expr, env)
            if self.trace:
                self._trace_exit(expr, v)
            return v
        except SuayRuntimeError as e:
            if e.span is None or e.source is None or e.filename is None:
                raise e.with_location(span=expr.span, source=self.source, filename=self.filename)
            raise
        except RecursionError:
            raise SuayRuntimeError(
                "Maximum recursion depth exceeded",
                span=expr.span,
                source=self.source,
                filename=self.filename,
            )
        except Exception as e:  # defensive: wrap unexpected errors
            raise SuayRuntimeError(
                f"Internal interpreter error: {type(e).__name__}: {e}",
                span=expr.span,
                source=self.source,
                filename=self.filename,
            )

    def _eval_expr(self, expr: ast.Expr, env: Env) -> object:
        match expr:
            case ast.UnitLit():
                return UNIT
            case ast.BoolLit(value=value):
                return bool(value)
            case ast.IntLit(value=value):
                return int(value)
            case ast.DecLit(value=value):
                return float(value)
            case ast.TextLit(value=value):
                return str(value)
            case ast.Name(value=name):
                try:
                    return env.get(name)
                except KeyError:
                    raise SuayRuntimeError(
                        f"Undefined name {name!r}",
                        span=expr.span,
                        source=self.source,
                        filename=self.filename,
                    )

            case ast.Binding(name=name, value=value_expr):
                value = self.eval_expr(value_expr, env)
                if isinstance(value, Closure) and value.name is None:
                    value = Closure(params=value.params, body=value.body, env=value.env, name=name)
                try:
                    env.define(name, value)
                except KeyError:
                    raise SuayRuntimeError(
                        f"Name {name!r} is already bound in this scope",
                        span=expr.span,
                        source=self.source,
                        filename=self.filename,
                    )
                return value

            case ast.Mutation(name=name, value=value_expr):
                value = self.eval_expr(value_expr, env)
                try:
                    env.set_existing(name, value)
                except KeyError:
                    raise SuayRuntimeError(
                        f"Cannot mutate {name!r}: name is not bound in any enclosing scope",
                        span=expr.span,
                        source=self.source,
                        filename=self.filename,
                    )
                return value

            case ast.Block(items=items):
                child = Env(parent=env)
                result: object = UNIT
                for item in items:
                    result = self.eval_expr(item, child)
                return result

            case ast.TupleExpr(items=items):
                return tuple(self.eval_expr(it, env) for it in items)

            case ast.ListExpr(items=items):
                return [self.eval_expr(it, env) for it in items]

            case ast.MapExpr(entries=entries):
                out: dict[object, object] = {}
                for k_expr, v_expr in entries:
                    k = self.eval_expr(k_expr, env)
                    v = self.eval_expr(v_expr, env)
                    try:
                        out[k] = v
                    except TypeError as e:
                        raise SuayRuntimeError(
                            f"Invalid map key (unhashable): {e}",
                            span=k_expr.span,
                            source=self.source,
                            filename=self.filename,
                        )
                return out

            case ast.VariantExpr(tag=tag, payload=payload_expr):
                payload = self.eval_expr(payload_expr, env)
                return Variant(tag=tag, payload=payload)

            case ast.Lambda(params=params, body=body):
                return Closure(params=params, body=body, env=env, name=None)

            case ast.Call(func=fn_expr, arg=arg_expr):
                fn_val = self.eval_expr(fn_expr, env)
                arg_val = self.eval_expr(arg_expr, env)
                return self._apply(fn_val, arg_val, call_span=expr.span)

            case ast.Unary(op=op, expr=rhs_expr):
                rhs = self.eval_expr(rhs_expr, env)
                if op in ("¬",):
                    return not _is_truthy(rhs)
                if op in ("−", "-"):
                    if not _is_number(rhs):
                        raise SuayRuntimeError(
                            f"Unary minus expects a number, got {type(rhs).__name__}",
                            span=expr.span,
                            source=self.source,
                            filename=self.filename,
                        )
                    return -rhs
                raise SuayRuntimeError(
                    f"Unknown unary operator {op!r}",
                    span=expr.span,
                    source=self.source,
                    filename=self.filename,
                )

            case ast.Binary(op=op, left=left_expr, right=right_expr):
                # Short-circuit boolean operators.
                if op == "∧":
                    left = self.eval_expr(left_expr, env)
                    if not _is_truthy(left):
                        return False
                    right = self.eval_expr(right_expr, env)
                    return _is_truthy(right)
                if op == "∨":
                    left = self.eval_expr(left_expr, env)
                    if _is_truthy(left):
                        return True
                    right = self.eval_expr(right_expr, env)
                    return _is_truthy(right)

                left = self.eval_expr(left_expr, env)
                right = self.eval_expr(right_expr, env)
                return self._binary(op, left, right, expr.span)

            case ast.Dispatch(value=value_expr, arms=arms):
                scrut = self.eval_expr(value_expr, env)
                for arm in arms:
                    binds = self._match_pattern(arm.pattern, scrut)
                    if binds is None:
                        continue
                    arm_env = Env(parent=env)
                    for k, v in binds.items():
                        arm_env.define(k, v)
                    return self.eval_expr(arm.expr, arm_env)
                raise SuayRuntimeError(
                    "No dispatch arm matched",
                    span=expr.span,
                    source=self.source,
                    filename=self.filename,
                )

            case ast.Cycle(seed=seed_expr, arms=arms):
                state = self.eval_expr(seed_expr, env)
                while True:
                    matched = False
                    for arm in arms:
                        binds = self._match_pattern(arm.pattern, state)
                        if binds is None:
                            continue
                        matched = True
                        arm_env = Env(parent=env)
                        for k, v in binds.items():
                            arm_env.define(k, v)
                        val = self.eval_expr(arm.expr, arm_env)
                        if arm.mode == "continue":
                            state = val
                            break
                        if arm.mode == "finish":
                            return val
                        raise SuayRuntimeError(
                            f"Invalid cycle arm mode {arm.mode!r}",
                            span=arm.span,
                            source=self.source,
                            filename=self.filename,
                        )
                    if not matched:
                        raise SuayRuntimeError(
                            "No cycle arm matched",
                            span=expr.span,
                            source=self.source,
                            filename=self.filename,
                        )

            case _:
                raise SuayRuntimeError(
                    f"Unsupported AST node: {type(expr).__name__}",
                    span=expr.span,
                    source=self.source,
                    filename=self.filename,
                )

    def _binary(self, op: str, left: object, right: object, span) -> object:
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
                    return _merge_maps(left, right)
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

    def _apply(self, fn_val: object, arg_val: object, call_span) -> object:
        try:
            if isinstance(fn_val, Builtin):
                # Special-case `link`: it needs the call-site span to report module-load errors.
                if fn_val.name == "link":
                    new_bound = (*fn_val.bound, arg_val)
                    if len(new_bound) < fn_val.arity:
                        return Builtin(name=fn_val.name, arity=fn_val.arity, impl=fn_val.impl, bound=new_bound)
                    if len(new_bound) > fn_val.arity:
                        raise SuayRuntimeError(
                            "Builtin over-applied",
                            span=call_span,
                            source=self.source,
                            filename=self.filename,
                        )

                    path, name = new_bound
                    if not isinstance(path, str) or not isinstance(name, str):
                        raise SuayRuntimeError(
                            f"link expects (Text,Text); got ({type(path).__name__},{type(name).__name__})",
                            span=call_span,
                            source=self.source,
                            filename=self.filename,
                        )
                    if name.startswith("_"):
                        raise SuayRuntimeError(
                            f"Module member {name!r} is private",
                            span=call_span,
                            source=self.source,
                            filename=self.filename,
                        )

                    abs_path = self._resolve_module_path(path)
                    mod_env = self._load_module_env(abs_path, call_span=call_span)
                    try:
                        return mod_env.get_local(name)
                    except KeyError:
                        raise SuayRuntimeError(
                            f"Module {abs_path!r} has no exported name {name!r}",
                            span=call_span,
                            source=self.source,
                            filename=self.filename,
                        )

                try:
                    return fn_val.apply(arg_val)
                except SuayRuntimeError as e:
                    # Ensure builtins always surface with a call-site location.
                    raise e.with_location(span=call_span, source=self.source, filename=self.filename)

            if isinstance(fn_val, Closure):
                if not fn_val.params:
                    raise SuayRuntimeError(
                        "Cannot call a function with no remaining parameters",
                        span=call_span,
                        source=self.source,
                        filename=self.filename,
                    )
                first, rest = fn_val.params[0], fn_val.params[1:]
                binds = self._match_pattern(first, arg_val)
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
                    return Closure(params=rest, body=fn_val.body, env=call_env, name=fn_val.name)

                # all params satisfied
                try:
                    return self.eval_expr(fn_val.body, call_env)
                except SuayRuntimeError as e:
                    label = fn_val.name or "<lambda>"
                    if call_span is not None:
                        raise e.with_frame(StackFrame(label=f"call {label}", span=call_span))
                    raise e

            raise SuayRuntimeError(
                f"Value is not callable: {type(fn_val).__name__}",
                span=call_span,
                source=self.source,
                filename=self.filename,
            )

        except SuayRuntimeError:
            raise

    def _match_pattern(self, pat: ast.Pattern, value: object) -> dict[str, object] | None:
        def merge_into(dst: dict[str, object], src: dict[str, object]) -> bool:
            # Return False on conflict (duplicate binder).
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
                    binds = self._match_pattern(p, v)
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
                    binds = self._match_pattern(p, v)
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
                tail_binds = self._match_pattern(tail, rest)
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
                return self._match_pattern(payload_pat, value.payload)

            case _:
                raise SuayRuntimeError(
                    f"Unsupported pattern: {type(pat).__name__}",
                    span=pat.span,
                    source=self.source,
                    filename=self.filename,
                )

    def _install_builtins(self, env: Env) -> None:
        def say(x: object) -> Unit:
            print(_to_text(x))
            return UNIT

        def hear(prompt: object) -> str:
            # Read one line from stdin. Prompt is printed without an extra newline.
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


        # Note: Builtins are curried by arity.
        env.define("say", Builtin(name="say", arity=1, impl=say))
        env.define("hear", Builtin(name="hear", arity=1, impl=hear))
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
        env.define("link", Builtin(name="link", arity=2, impl=lambda _path, _name: UNIT))

    def _trace_enter(self, expr: ast.Expr) -> None:
        self._depth += 1
        pad = "  " * (self._depth - 1)
        print(f"{pad}→ {type(expr).__name__}")

    def _trace_exit(self, expr: ast.Expr, value: object) -> None:
        pad = "  " * (self._depth - 1)
        print(f"{pad}← {type(expr).__name__} = {_to_text(value)}")
        self._depth -= 1


def run_source(source: str, *, filename: str | None = None, trace: bool = False) -> object:
    """Convenience: lex + parse + interpret a SuayLang source string."""
    tokens = Lexer(source, filename=filename).tokenize()
    program = Parser(tokens, source, filename=filename).parse_program()
    return Interpreter(source=source, filename=filename, trace=trace).eval_program(program)
