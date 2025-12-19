from __future__ import annotations

from suaylang.lexer import Lexer
from suaylang.parser import Parser


def parse_ok(source: str) -> None:
    tokens = Lexer(source, filename="<test>").tokenize()
    Parser(tokens, source, filename="<test>").parse_program()


def test_parse_allows_negative_call_argument() -> None:
    parse_ok("abs · -7\n")


def test_parse_long_call_chain_is_stable() -> None:
    src = "f ← ⌁(x) x\n" + "f" + " · 1" * 200 + "\n"
    parse_ok(src)


def test_parse_dispatch_requires_fat_arrow() -> None:
    tokens = Lexer("x ▷ ⟪ ▷ _ 1 ⟫\n", filename="<test>").tokenize()
    try:
        Parser(tokens, "x ▷ ⟪ ▷ _ 1 ⟫\n", filename="<test>").parse_program()
    except Exception as e:
        assert "Expected =>" in str(e)
    else:
        raise AssertionError("Expected parse to fail")


def test_parse_cycle_requires_arm_markers() -> None:
    tokens = Lexer("⟲ 0 ▷ ⟪ _ ⇒ ↯ 0 ⟫\n", filename="<test>").tokenize()
    try:
        Parser(tokens, "⟲ 0 ▷ ⟪ _ ⇒ ↯ 0 ⟫\n", filename="<test>").parse_program()
    except Exception as e:
        assert "Expected |>" in str(e)
    else:
        raise AssertionError("Expected parse to fail")


def test_parse_map_literal() -> None:
    parse_ok('m ← ⟦"a" ↦ 1, "b" ↦ 2⟧\nkeys · m\n')


def test_parse_variant_payload_tuple() -> None:
    parse_ok("v ← Tag•(1 2 3)\nv\n")
