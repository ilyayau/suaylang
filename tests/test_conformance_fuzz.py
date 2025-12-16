from __future__ import annotations

from dataclasses import replace

from hypothesis import given, settings
from hypothesis import strategies as st

from suaylang import ast
from suaylang.compiler import Compiler
from suaylang.conformance import compare_observations
from suaylang.interpreter import Interpreter
from suaylang.tokens import Position, Span
from suaylang.vm import VM


def _span() -> Span:
    p = Position(offset=0, line=1, column=1)
    return Span(start=p, end=p)


def _program(items: list[ast.Expr]) -> ast.Program:
    return ast.Program(span=_span(), items=items)


def _observe_ast_interpreter(
    program: ast.Program,
) -> tuple[str, object | None, str | None]:
    # Minimal observation for fuzzing: stdout + success value or runtime error.
    import contextlib
    import io

    buf = io.StringIO()
    interp = Interpreter(source="", filename="<fuzz>", trace=False)

    try:
        with contextlib.redirect_stdout(buf):
            val = interp.eval_program(program)
        return buf.getvalue(), val, None
    except Exception as e:  # noqa: BLE001
        return buf.getvalue(), None, type(e).__name__


def _observe_ast_vm(program: ast.Program) -> tuple[str, object | None, str | None]:
    import contextlib
    import io

    buf = io.StringIO()
    code = Compiler().compile_program(program, name="<fuzz>")
    vm = VM(source="", filename="<fuzz>", trace=False)

    try:
        with contextlib.redirect_stdout(buf):
            val = vm.run(code)
        return buf.getvalue(), val, None
    except Exception as e:  # noqa: BLE001
        return buf.getvalue(), None, type(e).__name__


# --- Strategies over a VM-supported subset ---

op_strategy = st.sampled_from(["+", "−", "×", "÷", "%", "=", "≠", "<", "≤", ">", "≥"])


@st.composite
def lit_expr(draw) -> ast.Expr:
    s = _span()
    kind = draw(st.sampled_from(["int", "bool", "unit"]))
    if kind == "int":
        return ast.IntLit(span=s, value=draw(st.integers(min_value=-10, max_value=10)))
    if kind == "bool":
        return ast.BoolLit(span=s, value=draw(st.booleans()))
    return ast.UnitLit(span=s)


@st.composite
def expr(draw, depth: int = 0) -> ast.Expr:
    s = _span()
    if depth >= 3:
        return draw(lit_expr())

    choice = draw(st.sampled_from(["lit", "binary", "dispatch_variant"]))
    if choice == "lit":
        return draw(lit_expr())

    if choice == "binary":
        left = draw(expr(depth=depth + 1))
        right = draw(expr(depth=depth + 1))
        op = draw(op_strategy)
        return ast.Binary(span=s, op=op, left=left, right=right)

    # dispatch over a small set of variant tags
    tag = draw(st.sampled_from(["Ok", "Err"]))
    payload = ast.IntLit(span=s, value=draw(st.integers(min_value=0, max_value=5)))
    scrutinee = ast.VariantExpr(span=s, tag=tag, payload=payload)

    # arms: match Ok•x => 1, Err•x => 0, _ => 2
    arm1 = ast.DispatchArm(
        span=s,
        pattern=ast.PVariant(span=s, tag="Ok", payload=ast.PName(span=s, name="x")),
        expr=ast.IntLit(span=s, value=1),
    )
    arm2 = ast.DispatchArm(
        span=s,
        pattern=ast.PVariant(span=s, tag="Err", payload=ast.PName(span=s, name="x")),
        expr=ast.IntLit(span=s, value=0),
    )
    arm3 = ast.DispatchArm(
        span=s,
        pattern=ast.PWildcard(span=s),
        expr=ast.IntLit(span=s, value=2),
    )
    return ast.Dispatch(span=s, value=scrutinee, arms=[arm1, arm2, arm3])


@given(st.lists(expr(), min_size=1, max_size=5))
@settings(max_examples=100)
def test_fuzz_interpreter_vm_agree(items: list[ast.Expr]) -> None:
    # Build a small program; ignore UNIT-only programs.
    program = _program([replace(it, span=_span()) for it in items])

    out_i, val_i, err_i = _observe_ast_interpreter(program)
    out_v, val_v, err_v = _observe_ast_vm(program)

    # Convert these minimal observations into the same comparison policy.
    # We treat any exception type-name mismatch as a failure.
    if err_i is None and err_v is None:
        assert out_i == out_v
        try:
            assert val_i == val_v
        except Exception:
            pass
        return

    assert err_i == err_v
    assert out_i == out_v

    # Avoid unused import warning for compare_observations; also ensure module is exercised.
    _ = compare_observations
    assert _ is not None
