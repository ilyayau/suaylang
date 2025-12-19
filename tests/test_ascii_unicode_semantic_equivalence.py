from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from suaylang.contract import error_code
from suaylang.errors import Diagnostic, SuayError
from suaylang.interpreter import Interpreter
from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.runtime import SuayRuntimeError


@dataclass(frozen=True)
class Obs:
    termination: str  # ok | lex | parse | runtime
    stdout: str
    code: str | None
    line: int | None
    column: int | None


def _norm_stdout(s: str) -> str:
    return s.replace("\r\n", "\n")


def _observe_interpreter(source: str, *, filename: str) -> Obs:
    import contextlib
    import io

    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            toks = Lexer(source, filename=filename).tokenize()
            program = Parser(toks, source, filename=filename).parse_program()
            Interpreter(source=source, filename=filename, trace=False).eval_program(program)
        return Obs("ok", _norm_stdout(out.getvalue()), None, None, None)
    except SuayError as e:
        if isinstance(e, Diagnostic):
            term = "lex" if e.error_type == "lexical" else "parse"
            return Obs(term, _norm_stdout(out.getvalue()), error_code(e), e.line, e.column)
        if isinstance(e, SuayRuntimeError):
            line = e.span.start.line if e.span else None
            col = e.span.start.column if e.span else None
            return Obs("runtime", _norm_stdout(out.getvalue()), error_code(e), line, col)
        return Obs("runtime", _norm_stdout(out.getvalue()), error_code(e), None, None)


_CASES_DIR = Path(__file__).parent / "ascii_unicode_pairs"


def _case_pairs() -> list[tuple[Path, Path]]:
    ascii_cases = sorted(_CASES_DIR.glob("*_ascii.suay"))
    pairs: list[tuple[Path, Path]] = []
    for a in ascii_cases:
        u = Path(str(a).replace("_ascii.suay", "_unicode.suay"))
        assert u.exists(), f"Missing unicode pair for {a.name}: {u.name}"
        pairs.append((a, u))
    return pairs


@pytest.mark.parametrize("ascii_path,unicode_path", _case_pairs(), ids=lambda p: p.name)
def test_ascii_and_unicode_semantically_equivalent(ascii_path: Path, unicode_path: Path) -> None:
    ascii_src = ascii_path.read_text(encoding="utf-8")
    unicode_src = unicode_path.read_text(encoding="utf-8")

    a = _observe_interpreter(ascii_src, filename=str(ascii_path))
    u = _observe_interpreter(unicode_src, filename=str(unicode_path))

    assert a.termination == u.termination
    assert a.stdout == u.stdout

    # For failures we require stable code + location equivalence.
    if a.termination != "ok":
        assert a.code is not None
        assert a.code == u.code
        assert (a.line, a.column) == (u.line, u.column)
