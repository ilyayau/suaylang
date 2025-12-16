from __future__ import annotations

from pathlib import Path

from suaylang.conformance import compare_observations, observe_interpreter, observe_vm


def test_conformance_corpus() -> None:
    root = Path(__file__).resolve().parent / "corpus" / "conformance"
    files = sorted(root.glob("*.suay"))
    assert files, "expected at least one conformance corpus file"

    for p in files:
        src = p.read_text(encoding="utf-8")
        interp = observe_interpreter(src, filename=str(p))
        vm = observe_vm(src, filename=str(p))
        res = compare_observations(interp, vm)
        assert res.ok, f"{p} failed: {res.reason}"
