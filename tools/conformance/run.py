from __future__ import annotations

import argparse
from pathlib import Path

from suaylang.conformance import compare_observations, observe_interpreter, observe_vm


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _iter_suay_files(root: Path) -> list[Path]:
    if root.is_file() and root.suffix == ".suay":
        return [root]
    if root.is_dir():
        return sorted(p for p in root.rglob("*.suay") if p.is_file())
    return []


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="conformance", description="SuayLang conformance runner"
    )
    ap.add_argument(
        "paths",
        nargs="*",
        default=["tests/corpus/conformance"],
        help="One or more .suay files or directories (default: tests/corpus/conformance)",
    )
    args = ap.parse_args()

    roots = [Path(p) for p in args.paths]
    files: list[Path] = []
    for r in roots:
        files.extend(_iter_suay_files(r))

    if not files:
        print("conformance: no .suay files found")
        return 2

    failures = 0
    for p in files:
        src = _read(p)
        interp = observe_interpreter(src, filename=str(p))
        vm = observe_vm(src, filename=str(p))
        res = compare_observations(interp, vm)
        if res.ok:
            continue
        failures += 1
        print(f"FAIL {p}: {res.reason}")
        print("--- interpreter ---")
        print(
            f"termination={interp.termination} stdout={interp.stdout!r} value={interp.value!r} err={interp.error_type} {interp.line}:{interp.column}"
        )
        print("--- vm ---")
        print(
            f"termination={vm.termination} stdout={vm.stdout!r} value={vm.value!r} err={vm.error_type} {vm.line}:{vm.column}"
        )

    if failures:
        print(f"conformance: {failures} failure(s) out of {len(files)}")
        return 1

    print(f"conformance: ok ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
