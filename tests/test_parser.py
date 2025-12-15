import unittest

from suaylang import ast
from suaylang.lexer import Lexer
from suaylang.parser import ParseError, Parser


def parse_program(src: str) -> ast.Program:
    tokens = Lexer(src).tokenize()
    return Parser(tokens, src).parse_program()


class ParserTests(unittest.TestCase):
    def test_parser_empty_input_yields_empty_program(self) -> None:
        program = parse_program("")
        self.assertEqual(program.items, [])

    def test_parser_requires_newline_between_top_level_forms(self) -> None:
        with self.assertRaises(ParseError):
            parse_program("x ← 1 y ← 2")

    def test_parser_grouping_parentheses_do_not_create_tuple(self) -> None:
        program = parse_program("x ← (1)\n")
        self.assertIsInstance(program.items[0], ast.Binding)
        self.assertIsInstance(program.items[0].value, ast.IntLit)

    def test_parser_singleton_tuple_requires_trailing_comma(self) -> None:
        program = parse_program("x ← (1,)\n")
        self.assertIsInstance(program.items[0], ast.Binding)
        self.assertIsInstance(program.items[0].value, ast.TupleExpr)
        self.assertEqual(len(program.items[0].value.items), 1)

    def test_parser_mutation_parses_as_mutation_node(self) -> None:
        program = parse_program("x ← 1\nx ⇐ 2\n")
        self.assertIsInstance(program.items[0], ast.Binding)
        self.assertIsInstance(program.items[1], ast.Mutation)

    def test_parser_dispatch_missing_fat_arrow_is_syntax_error(self) -> None:
        bad = "1 ▷ ⟪ ▷ _ 1 ⟫\n"
        with self.assertRaises(ParseError):
            parse_program(bad)
