from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from suaylang.compiler import Compiler
from suaylang.interpreter import run_source
from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.vm import VM


def run_vm(source: str) -> object:
    tokens = Lexer(source, filename="<test>").tokenize()
    program = Parser(tokens, source, filename="<test>").parse_program()
    code = Compiler().compile_program(program, name="<test>")
    return VM(source=source, filename="<test>").run(code)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("1 + 2\n", 3),
        ("10 − 3\n", 7),
        ("2 × 4 + 1\n", 9),
        ("(2 + 4) × 3\n", 18),
        ("¬⊥\n", True),
        ("⊤ ∧ ⊥\n", False),
        ("⊤ ∨ ⊥\n", True),
    ],
)
def test_interpreter_and_vm_match_on_core_expressions(
    source: str, expected: object
) -> None:
    assert run_source(source, filename="<test>") == expected
    assert run_vm(source) == expected


def test_interpreter_and_vm_match_on_call_chains() -> None:
    source = "square ← ⌁(x) x × x\n(square · 7) + (square · 2)\n"
    assert run_source(source, filename="<test>") == run_vm(source)


def test_interpreter_and_vm_match_on_lists_and_concat() -> None:
    source = "a ← [1 2]\nb ← [3]\na ⊞ b\n"
    assert run_source(source, filename="<test>") == [1, 2, 3]
    assert run_vm(source) == [1, 2, 3]


def test_interpreter_and_vm_match_on_maps_put_has_keys() -> None:
    source = (
        'm ← ⟦"a" ↦ 1⟧\nm2 ← put · m · "b" · 2\n(has · m2 · "a") ∧ (has · m2 · "b")\n'
    )
    assert run_source(source, filename="<test>") is True
    assert run_vm(source) is True


@given(
    a=st.integers(min_value=-10_000, max_value=10_000),
    b=st.integers(min_value=-10_000, max_value=10_000),
)
def test_property_add_equivalence(a: int, b: int) -> None:
    source = f"a ← {a}\nb ← {b}\na + b\n"
    assert run_source(source, filename="<test>") == run_vm(source)


@given(
    a=st.integers(min_value=-1_000, max_value=1_000),
    b=st.integers(min_value=-1_000, max_value=1_000),
)
def test_property_mul_equivalence(a: int, b: int) -> None:
    source = f"a ← {a}\nb ← {b}\na × b\n"
    assert run_source(source, filename="<test>") == run_vm(source)


@given(n=st.integers(min_value=-1_000_000, max_value=1_000_000))
def test_property_abs_matches_python(n: int) -> None:
    source = f"abs · {n}\n"
    assert run_source(source, filename="<test>") == abs(n)
    assert run_vm(source) == abs(n)
