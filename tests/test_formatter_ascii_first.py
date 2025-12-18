from __future__ import annotations

from suaylang.formatter import FormatOptions, format_source


def test_fmt_rewrites_unicode_tokens_to_ascii_but_not_strings_or_comments() -> None:
    src = (
        'x ← "keep ← inside string"\n'
        "y ← 1  ⍝ comment has ← and ⟪ ⟫ and ·\n"
        "f ← ⌁(u) u\n"
        "z ← f · ø\n"
        "m ← ⟦ \"a\" ↦ 1, \"b\" ↦ 2 ⟧\n"
        "v ← Ok•41\n"
        "w ← (⊤ ∧ ⊥) ∨ ⊥\n"
    )

    out = format_source(src, filename="<test>", options=FormatOptions(unicode=False))

    assert 'x <- "keep ← inside string"\n' in out
    assert "// comment has ← and ⟪ ⟫ and ·" in out  # comment marker canonicalized; body preserved

    # Spot-check canonical replacements.
    assert "f <- \\(" in out
    assert "z <- f . #u" in out
    assert "[[ \"a\" -> 1, \"b\" -> 2 ]]" in out
    assert "Ok::41" in out
    assert "(#t && #f) || #f" in out


def test_fmt_rewrites_ascii_tokens_to_unicode() -> None:
    src = (
        "x <- 1\n"
        "y <~ 2\n"
        "v <- Ok::41\n"
        "v |> {\n"
        "|> Ok::n => n\n"
        "|> _     => 0\n"
        "}\n"
    )
    out = format_source(src, filename="<test>", options=FormatOptions(unicode=True))

    assert "x ← 1" in out
    assert "y ⇐ 2" in out
    assert "Ok•41" in out
    assert "▷" in out
    assert "⟪" in out and "⟫" in out
