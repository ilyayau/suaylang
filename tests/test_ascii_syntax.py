from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any

import pytest

from suaylang.conformance import observe_interpreter
from suaylang.lexer import Lexer
from suaylang.parser import Parser


def _parse(source: str) -> object:
    toks = Lexer(source, filename="<test>").tokenize()
    return Parser(toks, source, filename="<test>").parse_program()


def _shape(x: Any) -> Any:
    """Serialize an AST into a stable, span-free structure for comparisons."""
    if is_dataclass(x):
        cls = type(x).__name__
        out: list[Any] = [cls]
        for f in fields(x):
            if f.name == "span":
                continue
            out.append((f.name, _shape(getattr(x, f.name))))
        return tuple(out)
    if isinstance(x, list):
        return tuple(_shape(v) for v in x)
    if isinstance(x, tuple):
        return tuple(_shape(v) for v in x)
    if isinstance(x, dict):
        return tuple(sorted((_shape(k), _shape(v)) for k, v in x.items()))
    return x


UNICODE_OK = (
    "inc ← ⌁(x) x + 1\n"
    'm ← ⟦ "a" ↦ 1 , "b" ↦ 2 ⟧\n'
    "sum_to ← ⌁(n)\n"
    "  ⟲ (Step•(1 0)) ▷ ⟪\n"
    "  ▷ Done•acc     ⇒ ↯ acc\n"
    "  ▷ Step•(i acc) ⇒ ↩ (\n"
    "        (i > n) ▷ ⟪\n"
    "        ▷ ⊤ ⇒ Done•acc\n"
    "        ▷ ⊥ ⇒ Step•(i + 1  acc + i)\n"
    "        ⟫\n"
    "      )\n"
    "  ⟫\n"
    "v ← Ok•41\n"
    "v ▷ ⟪\n"
    "▷ Ok•n  ⇒ inc · n\n"
    "▷ _     ⇒ 0\n"
    "⟫\n"
    "sum_to · 5\n"
)

ASCII_OK = (
    "inc <- \\(x) x + 1\n"
    'm <- [[ "a" -> 1 , "b" -> 2 ]]\n'
    "sum_to <- \\(n)\n"
    "  ~~ (Step::(1 0)) |> {\n"
    "  |> Done::acc     => << acc\n"
    "  |> Step::(i acc) => >> (\n"
    "        (i > n) |> {\n"
    "        |> #t => Done::acc\n"
    "        |> #f => Step::(i + 1  acc + i)\n"
    "        }\n"
    "      )\n"
    "  }\n"
    "v <- Ok::41\n"
    "v |> {\n"
    "|> Ok::n  => inc . n\n"
    "|> _      => 0\n"
    "}\n"
    "sum_to . 5\n"
)


def test_ascii_and_unicode_parse_to_same_ast_shape() -> None:
    u = _parse(UNICODE_OK)
    a = _parse(ASCII_OK)
    assert _shape(u) == _shape(a)


def test_ascii_and_unicode_evaluate_identically_for_ok_programs() -> None:
    u = observe_interpreter(UNICODE_OK, filename="<unicode>")
    a = observe_interpreter(ASCII_OK, filename="<ascii>")

    assert u.termination == "ok"
    assert a.termination == "ok"
    assert u.stdout == a.stdout
    assert u.value == a.value


@pytest.mark.parametrize(
    "source, expected_line, expected_col",
    [
        ("x ← y\n", 1, 5),
        ("x <- y\n", 1, 6),
    ],
)
def test_error_spans_are_correct_in_each_syntax(
    source: str, expected_line: int, expected_col: int
) -> None:
    obs = observe_interpreter(source, filename="<err>")
    assert obs.termination == "runtime"
    assert obs.line == expected_line
    assert obs.column == expected_col


def test_ascii_slash_slash_line_comments_are_supported() -> None:
    src = "x <- 1 // comment\n" "x\n"
    obs = observe_interpreter(src, filename="<ascii-comment>")
    assert obs.termination == "ok"
    assert obs.value == 1
