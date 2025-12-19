from __future__ import annotations

from dataclasses import is_dataclass

from suaylang.formatter import FormatOptions, format_source
from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.conformance import observe_interpreter, observe_vm


def _strip_spans(node: object) -> object:
    """Convert an AST into a structural form that ignores source spans."""
    if is_dataclass(node):
        cls = type(node)
        out: dict[str, object] = {"__type__": cls.__name__}
        for name in getattr(node, "__dataclass_fields__").keys():
            if name == "span":
                continue
            out[name] = _strip_spans(getattr(node, name))
        return out
    if isinstance(node, list):
        return [_strip_spans(x) for x in node]
    if isinstance(node, tuple):
        return tuple(_strip_spans(x) for x in node)
    if isinstance(node, dict):
        return {k: _strip_spans(v) for k, v in node.items()}
    return node


def _parse(src: str) -> object:
    toks = Lexer(src, filename="<test>").tokenize()
    return Parser(toks, src, filename="<test>").parse_program()


def test_ascii_and_unicode_parse_to_same_ast_structure() -> None:
    # Dispatch arms must be separated by newlines; otherwise the expression
    # parser will consume the next arm marker as an infix dispatch.
    unicode_src = (
        "x ← 1\n"
        "y ← 2\n"
        "add ← ⌁(a b) a + b\n"
        "v ← Ok•(x y)\n"
        "v ▷ ⟪\n"
        "▷ Ok•(a b) ⇒ add · a · b\n"
        "▷ _ ⇒ 0\n"
        "⟫\n"
    )

    # Formatter converts token spellings, but preserves whitespace/comments.
    ascii_src = format_source(unicode_src, options=FormatOptions(unicode=False))

    a1 = _strip_spans(_parse(unicode_src))
    a2 = _strip_spans(_parse(ascii_src))
    assert a1 == a2


def test_ascii_and_unicode_semantics_match_interpreter_and_vm() -> None:
    unicode_src = (
        "total ← fold · (⌁(a b) a + b) · 0 · [10 20]\n"
        'say · ("total=" ⊞ (text · total))\n'
        "total\n"
    )
    ascii_src = format_source(unicode_src, options=FormatOptions(unicode=False))

    i_u = observe_interpreter(unicode_src, filename="<u>")
    i_a = observe_interpreter(ascii_src, filename="<a>")
    assert i_u.termination == "ok"
    assert i_a.termination == "ok"
    assert i_u.stdout.replace("\r\n", "\n") == i_a.stdout.replace("\r\n", "\n")
    assert i_u.value == i_a.value

    v_u = observe_vm(unicode_src, filename="<u>")
    v_a = observe_vm(ascii_src, filename="<a>")
    assert v_u.termination == "ok"
    assert v_a.termination == "ok"
    assert v_u.stdout.replace("\r\n", "\n") == v_a.stdout.replace("\r\n", "\n")
    assert v_u.value == v_a.value
