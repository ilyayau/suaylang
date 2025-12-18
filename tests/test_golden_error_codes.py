from __future__ import annotations

from pathlib import Path

import pytest

from suaylang.contract import format_error
from suaylang.errors import SuayError
from suaylang.interpreter import Interpreter
from suaylang.lexer import Lexer
from suaylang.parser import Parser


_CASES = Path(__file__).parent / "golden" / "diagnostics"
_REPO_ROOT = Path(__file__).resolve().parents[1]


def _run_program_text(source: str, *, filename: str) -> str:
    try:
        toks = Lexer(source, filename=filename).tokenize()
        program = Parser(toks, source, filename=filename).parse_program()
        Interpreter(source=source, filename=filename, trace=False).eval_program(program)
        return "<ok>\n"
    except SuayError as e:
        return format_error(e, include_code=True).rstrip() + "\n"


@pytest.mark.parametrize(
    "case",
    sorted(p for p in _CASES.glob("*.suay") if p.is_file()),
    ids=lambda p: p.name,
)
def test_golden_error_codes(case: Path) -> None:
    expected_path = case.with_suffix(".txt")
    assert expected_path.exists(), f"Missing snapshot: {expected_path}"

    src = case.read_text(encoding="utf-8")
    display_name = str(case.relative_to(_REPO_ROOT))
    got = _run_program_text(src, filename=display_name)
    expected = expected_path.read_text(encoding="utf-8")
    assert got == expected
