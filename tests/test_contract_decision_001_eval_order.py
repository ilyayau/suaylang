from __future__ import annotations

from suaylang.conformance import observe_interpreter, observe_vm


def _assert_ok_and_stdout(source: str, expected_stdout: str) -> None:
    interp = observe_interpreter(source, filename="<decision-001>")
    vm = observe_vm(source, filename="<decision-001>")

    assert interp.termination == "ok"
    assert vm.termination == "ok"

    # normalize for windows line endings
    assert interp.stdout.replace("\r\n", "\n") == expected_stdout
    assert vm.stdout.replace("\r\n", "\n") == expected_stdout


def test_decision_001_binary_evaluates_left_to_right() -> None:
    # Uses side effects: `say` prints and returns unit, but `=` still evaluates both sides.
    src = 'ok ← (say · "L") = (say · "R")\n'
    _assert_ok_and_stdout(src, "L\nR\n")


def test_decision_001_call_evaluates_func_then_arg() -> None:
    # Make the function position produce output when called, then ensure the outer arg
    # is evaluated only after the function position has been fully evaluated.
    src = (
        "mk ← ⌁(_) (⌁(y) y)\n"
        "f ← ⌁(_) ⟪\n"
        '  say · "F"\n'
        "  mk · ø\n"
        "⟫\n"
        "x ← ⌁(_) ⟪\n"
        '  say · "X"\n'
        "  1\n"
        "⟫\n"
        "tmp ← (f · ø) · (x · ø)\n"
    )
    _assert_ok_and_stdout(src, "F\nX\n")
