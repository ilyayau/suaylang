from __future__ import annotations

import string

from hypothesis import given, settings
from hypothesis import strategies as st

from suaylang.errors import SuayError
from suaylang.lexer import Lexer
from suaylang.parser import Parser


@settings(max_examples=200, deadline=200)
@given(
    st.text(
        alphabet=st.sampled_from(
            list(
                string.ascii_letters
                + string.digits
                + " _\n\t\r()[]{}.,\"'<>!=+-*/%&|\\#"
                + "⟪⟫⟦⟧←⇐↦⇒▷⟲↩↯•⋯⌁ø⊤⊥¬⊞×÷−≤≥≠∧∨·⍝"
            )
        ),
        min_size=0,
        max_size=200,
    )
)
def test_parser_fuzz_does_not_crash(source: str) -> None:
    """Grammar-fuzz layer: lexer+parser should never crash the process.

    It may succeed or raise a user-facing SuayError (lex/parse).
    """
    try:
        toks = Lexer(source, filename="<fuzz>").tokenize()
        Parser(toks, source, filename="<fuzz>").parse_program()
    except SuayError:
        return
