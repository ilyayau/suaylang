from __future__ import annotations

import argparse
from pathlib import Path

from suaylang.conformance import compare_observations, observe_interpreter, observe_vm

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_ROOT = _REPO_ROOT / "tools" / "conformance" / "regressions"


def _iter_programs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(p for p in root.rglob("program.suay") if p.is_file())


def main() -> int:
    ap = argparse.ArgumentParser(prog="suay-regressions")
    ap.add_argument(
        "--root",
        type=str,
        default=str(_DEFAULT_ROOT),
        help="Regression corpus root (default: tools/conformance/regressions)",
    )
    args = ap.parse_args()

    root = Path(args.root)
    programs = _iter_programs(root)
    if not programs:
        print("regressions: OK (no cases)")
        return 0

    failures = 0
    for p in programs:
        src = p.read_text(encoding="utf-8")
        interp = observe_interpreter(src, filename=str(p))
        vm = observe_vm(src, filename=str(p))
        res = compare_observations(interp, vm)
        if res.ok:
            continue
        failures += 1
        print(f"FAIL {p}: {res.reason}")

    if failures:
        print(f"regressions: FAIL cases={len(programs)} fail={failures}")
        return 1

    print(f"regressions: OK cases={len(programs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
