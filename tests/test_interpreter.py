import io
import unittest
from contextlib import redirect_stdout

from suaylang.interpreter import run_source
from suaylang.runtime import SuayRuntimeError, UNIT


def run_capture(src: str):
    buf = io.StringIO()
    with redirect_stdout(buf):
        result = run_source(src)
    return result, buf.getvalue()


class InterpreterTests(unittest.TestCase):
    def test_interpreter_empty_program_returns_unit(self) -> None:
        result = run_source("")
        self.assertIs(result, UNIT)

    def test_interpreter_say_prints_evaluated_expression(self) -> None:
        _, out = run_capture("say · (1 + 2)\n")
        self.assertEqual(out.strip(), "3")

    def test_interpreter_list_concat_works(self) -> None:
        _, out = run_capture("say · ([1 2] ⊞ [3])\n")
        self.assertEqual(out.strip(), "[1 2 3]")

    def test_interpreter_undefined_name_raises_runtime_error(self) -> None:
        with self.assertRaises(SuayRuntimeError) as ctx:
            run_source("say · x\n")
        self.assertIn("Undefined name", str(ctx.exception))

    def test_interpreter_divide_by_zero_raises_runtime_error(self) -> None:
        with self.assertRaises(SuayRuntimeError):
            run_source("say · (1 ÷ 0)\n")

    def test_interpreter_short_circuit_and_prevents_error(self) -> None:
        _, out = run_capture("say · (⊥ ∧ (1 ÷ 0))\n")
        self.assertEqual(out.strip(), "⊥")

    def test_interpreter_short_circuit_or_prevents_error(self) -> None:
        _, out = run_capture("say · (⊤ ∨ (1 ÷ 0))\n")
        self.assertEqual(out.strip(), "⊤")

    def test_interpreter_lambda_application_computes_value(self) -> None:
        src = "inc ← ⌁(x) x + 1\nsay · (inc · 2)\n"
        _, out = run_capture(src)
        self.assertEqual(out.strip(), "3")

    def test_interpreter_lambda_parameter_shadows_outer_name(self) -> None:
        src = "x ← 10\nf ← ⌁(x) x + 1\nsay · (f · 2)\nsay · x\n"
        _, out = run_capture(src)
        self.assertEqual(out.splitlines(), ["3", "10"])

    def test_interpreter_mutation_updates_enclosing_scope(self) -> None:
        src = "x ← 1\nset ← ⌁(_) ⟪ x ⇐ 2\n x ⟫\nsay · (set · ø)\nsay · x\n"
        _, out = run_capture(src)
        self.assertEqual(out.splitlines(), ["2", "2"])

    def test_interpreter_unhashable_map_key_raises_runtime_error(self) -> None:
        with self.assertRaises(SuayRuntimeError) as ctx:
            run_source("x ← ⟦ [1] ↦ 2 ⟧\n")
        self.assertIn("unhashable", str(ctx.exception))

    def test_interpreter_strict_comparison_rejects_mixed_types(self) -> None:
        with self.assertRaises(SuayRuntimeError) as ctx:
            run_source('say · (1 < "a")\n')
        self.assertIn("expects (Num,Num) or (Text,Text)", str(ctx.exception))

    def test_interpreter_dispatch_selects_matching_arm(self) -> None:
        src = 'say · (1 ▷ ⟪\n ▷ 1 ⇒ "one"\n ▷ _ ⇒ "other"\n⟫)\n'
        _, out = run_capture(src)
        self.assertEqual(out.strip(), "one")

    def test_interpreter_cycle_can_finish(self) -> None:
        src = "say · (⟲ 3 ▷ ⟪\n ▷ 0 ⇒ ↯ 0\n ▷ n ⇒ ↩ (n - 1)\n⟫)\n"
        _, out = run_capture(src)
        self.assertEqual(out.strip(), "0")


