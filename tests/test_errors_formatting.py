from __future__ import annotations

from suaylang.errors import Diagnostic, _line_text


def test_line_text_basic_cases() -> None:
    src = "a\nbbb\nccc\n"
    assert _line_text(src, 1) == "a"
    assert _line_text(src, 2) == "bbb"
    assert _line_text(src, 3) == "ccc"


def test_line_text_out_of_range() -> None:
    src = "one\n"
    assert _line_text(src, 0) is None
    assert _line_text(src, -1) is None
    assert _line_text(src, 2) == ""

    src2 = "one"
    assert _line_text(src2, 2) is None


def test_diagnostic_str_renders_context_and_caret_from_source() -> None:
    src = "say · 1\n"
    d = Diagnostic(
        error_type="lexical",
        message="Unexpected character '@'",
        line=1,
        column=5,
        filename="<test>",
        source=src,
        context_line=None,
    )
    s = str(d)

    assert s.startswith("<test>:1:5: lexical error: Unexpected character '@'")
    assert "say · 1" in s
    assert "^" in s


def test_diagnostic_str_prefers_explicit_context_line() -> None:
    d = Diagnostic(
        error_type="syntax",
        message="Expected ')'",
        line=10,
        column=2,
        filename=None,
        source="ignored\n",
        context_line="X",
    )
    s = str(d)
    assert s.startswith("10:2: syntax error: Expected ')'")
    assert "\nX\n" in s
