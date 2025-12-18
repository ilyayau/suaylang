from __future__ import annotations

from pathlib import Path

import pytest

from suaylang.conformance import compare_observations, observe_interpreter, observe_vm


_REPO_ROOT = Path(__file__).resolve().parents[2]
_CORPUS = _REPO_ROOT / "conformance" / "corpus"


def _iter_cases() -> list[Path]:
    if not _CORPUS.exists():
        return []
    return sorted(p for p in _CORPUS.rglob("*.suay") if p.is_file())


@pytest.mark.parametrize("case", _iter_cases(), ids=lambda p: str(p.relative_to(_REPO_ROOT)))
def test_conformance_interpreter_matches_vm(case: Path) -> None:
    src = case.read_text(encoding="utf-8")
    filename = str(case.relative_to(_REPO_ROOT))

    interp = observe_interpreter(src, filename=filename)
    vm = observe_vm(src, filename=filename)
    res = compare_observations(interp, vm)

    assert res.ok, f"{filename}: {res.reason}"
