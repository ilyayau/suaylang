import unittest

from suaylang.lexer import LexError, Lexer
from suaylang.tokens import TokenType


class LexerTests(unittest.TestCase):
    def test_lexer_empty_input_produces_eof_only(self) -> None:
        tokens = Lexer("").tokenize()
        self.assertEqual([t.type for t in tokens], [TokenType.EOF])

    def test_lexer_ignores_comment_but_emits_newline_token(self) -> None:
        src = "x ← 1 ⍝ comment\n2\n"
        tokens = Lexer(src).tokenize()
        types = [t.type for t in tokens]
        self.assertIn(TokenType.NEWLINE, types)
        self.assertEqual(types[-1], TokenType.EOF)

    def test_lexer_string_escapes_are_decoded(self) -> None:
        tokens = Lexer('"a\\n\\t\\"\\\\"').tokenize()
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, 'a\n\t"\\')

    def test_lexer_unit_literal_is_not_identifier(self) -> None:
        tokens = Lexer("ø").tokenize()
        self.assertEqual(tokens[0].type, TokenType.UNIT)

    def test_lexer_unknown_character_raises_lex_error(self) -> None:
        with self.assertRaises(LexError):
            Lexer("@").tokenize()
