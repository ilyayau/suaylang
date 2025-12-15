import unittest

from suaylang.interpreter import run_source
from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.compiler import Compiler
from suaylang.vm import VM


def run_vm_source(src: str) -> object:
    tokens = Lexer(src, filename="<test>").tokenize()
    program = Parser(tokens, src, filename="<test>").parse_program()
    code = Compiler().compile_program(program)
    return VM(source=src, filename="<test>").run(code)


class StdlibTests(unittest.TestCase):
    def test_count_text_list_map(self) -> None:
        self.assertEqual(run_source('count · "abcd"\n', filename="<test>"), 4)
        self.assertEqual(run_source("count · [1 2 3]\n", filename="<test>"), 3)
        self.assertEqual(
            run_source('count · ⟦"a" ↦ 1, "b" ↦ 2⟧\n', filename="<test>"), 2
        )

        self.assertEqual(run_vm_source('count · "abcd"\n'), 4)
        self.assertEqual(run_vm_source("count · [1 2 3]\n"), 3)
        self.assertEqual(run_vm_source('count · ⟦"a" ↦ 1, "b" ↦ 2⟧\n'), 2)

    def test_at_take_drop_abs(self) -> None:
        self.assertEqual(run_source("at · [10 20 30] · 1\n", filename="<test>"), 20)
        self.assertEqual(run_source('at · "hey" · 1\n', filename="<test>"), "e")
        self.assertEqual(run_source('take · "hello" · 2\n', filename="<test>"), "he")
        self.assertEqual(run_source('drop · "hello" · 2\n', filename="<test>"), "llo")
        self.assertEqual(run_source("abs · -7\n", filename="<test>"), 7)

        self.assertEqual(run_vm_source("at · [10 20 30] · 1\n"), 20)
        self.assertEqual(run_vm_source('at · "hey" · 1\n'), "e")
        self.assertEqual(run_vm_source('take · "hello" · 2\n'), "he")
        self.assertEqual(run_vm_source('drop · "hello" · 2\n'), "llo")
        self.assertEqual(run_vm_source("abs · -7\n"), 7)

    def test_keys_has_put(self) -> None:
        src = 'm ← ⟦"a" ↦ 1, "b" ↦ 2⟧\nhas · m · "a"\n'
        self.assertEqual(run_source(src, filename="<test>"), True)
        self.assertEqual(run_vm_source(src), True)

        src2 = 'm ← ⟦"a" ↦ 1⟧\nm2 ← put · m · "b" · 2\ncount · (keys · m2)\n'
        self.assertEqual(run_source(src2, filename="<test>"), 2)
        self.assertEqual(run_vm_source(src2), 2)
