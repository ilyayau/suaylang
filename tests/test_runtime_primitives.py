from __future__ import annotations

import pytest

from suaylang.runtime import Builtin, Env, StackFrame, SuayRuntimeError
from suaylang.tokens import Position, Span


def test_builtin_currying_and_overapply() -> None:
    add2 = Builtin(name="add", arity=2, impl=lambda x, y: x + y)

    add1 = add2.apply(1)
    assert isinstance(add1, Builtin)
    assert add1.apply(2) == 3

    over = Builtin(name="add", arity=2, impl=lambda x, y: x + y, bound=(1, 2))
    with pytest.raises(ValueError):
        over.apply(3)


def test_env_define_get_set_existing() -> None:
    parent = Env()
    parent.define("x", 1)

    child = Env(parent=parent)
    assert child.get("x") == 1

    child.define("y", 2)
    assert child.get_local("y") == 2

    child.set_existing("x", 99)
    assert parent.get("x") == 99

    with pytest.raises(KeyError):
        child.define("y", 3)

    with pytest.raises(KeyError):
        child.get("missing")


def test_runtime_error_formats_location_and_stack() -> None:
    src = "boom\n"
    sp = Span(
        Position(offset=0, line=1, column=1), Position(offset=1, line=1, column=2)
    )

    e = SuayRuntimeError("nope", span=sp, source=src, filename="<test>")
    s = str(e)
    assert "<test>:1:1: runtime error: nope" in s
    assert "boom" in s

    e2 = e.with_frame(StackFrame(label="call f", span=sp))
    s2 = str(e2)
    assert "stack:" in s2
    assert "call f" in s2
