from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from suaylang.conformance import compare_observations, observe_interpreter, observe_vm

from tools.conformance.fuzz_runner import run_fuzz


@dataclass(frozen=True)
class H2Summary:
    corpus_files: int
    corpus_divergences: int
    fuzz_seed: int
    fuzz_n: int
    fuzz_divergences: int
    bugs_fixed_k: int
    subset_constructs_x: int


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _iter_suay_files(root: Path) -> list[Path]:
    if root.is_file() and root.suffix == ".suay":
        return [root]
    if root.is_dir():
        return sorted(p for p in root.rglob("*.suay") if p.is_file())
    return []


def _count_subset_constructs(path: Path) -> int:
    """Count constructs listed as '- ...' under '## Subset constructs (expressions)'."""

    text = _read(path)
    in_section = False
    count = 0
    for line in text.splitlines():
        if line.strip() == "## Subset constructs (expressions)":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.lstrip().startswith("- "):
            count += 1
    return count


def _run_conformance(paths: list[Path]) -> tuple[int, int]:
    files: list[Path] = []
    for p in paths:
        files.extend(_iter_suay_files(p))

    failures = 0
    for file_path in files:
        src = _read(file_path)
        interp = observe_interpreter(src, filename=str(file_path))
        vm = observe_vm(src, filename=str(file_path))
        res = compare_observations(interp, vm)
        if res.ok:
            continue
        failures += 1
        print(f"FAIL {file_path}: {res.reason}")

    return len(files), failures


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="h2-eval",
        description="Run the fixed H2 evaluation (conformance + fuzz) and print a numeric summary.",
    )
    ap.add_argument(
        "--corpus",
        type=str,
        default="tests/corpus/conformance",
        help="Conformance corpus path (file or directory)",
    )
    ap.add_argument(
        "--tasks",
        type=str,
        default="evaluation/tasks",
        help="Fixed task set path (file or directory)",
    )
    ap.add_argument("--seed", type=int, default=0, help="Fuzz RNG seed")
    ap.add_argument("--n", type=int, default=1000, help="Fuzz program count")
    ap.add_argument(
        "--subset",
        type=str,
        default="docs/spec/supported_subset.md",
        help="Path to supported subset spec (for construct counting)",
    )
    ap.add_argument(
        "--bugs-fixed",
        type=int,
        default=0,
        help="K: number of bugs found & fixed while reaching divergences=0 (manual accounting)",
    )
    ap.add_argument("--json", action="store_true", help="Print JSON summary")
    args = ap.parse_args()

    subset_x = _count_subset_constructs(Path(args.subset))

    corpus_files, corpus_div = _run_conformance([Path(args.corpus), Path(args.tasks)])
    if corpus_files == 0:
        print("h2: no .suay files found in the provided corpora")
        return 2

    stats, _saved = run_fuzz(
        n=int(args.n),
        seed=int(args.seed),
        save_dir=Path("tools/conformance/fuzz_failures"),
        fail_fast=False,
        save_non_ok=False,
        save_non_ok_limit=0,
    )

    summary = H2Summary(
        corpus_files=corpus_files,
        corpus_divergences=corpus_div,
        fuzz_seed=stats.seed,
        fuzz_n=stats.n,
        fuzz_divergences=stats.divergences,
        bugs_fixed_k=int(args.bugs_fixed),
        subset_constructs_x=subset_x,
    )

    if args.json:
        print(json.dumps(summary.__dict__, indent=2, sort_keys=True))
    else:
        print(
            "H2: corpus M={M} fuzz N={N} divergences={D} bugs_fixed K={K} subset_constructs X={X}".format(
                M=summary.corpus_files,
                N=summary.fuzz_n,
                D=(summary.corpus_divergences + summary.fuzz_divergences),
                K=summary.bugs_fixed_k,
                X=summary.subset_constructs_x,
            )
        )
        print(
            "  conformance: files={M} divergences={D}".format(
                M=summary.corpus_files, D=summary.corpus_divergences
            )
        )
        print(
            "  fuzz: seed={seed} n={n} divergences={d}".format(
                seed=summary.fuzz_seed, n=summary.fuzz_n, d=summary.fuzz_divergences
            )
        )

    return 0 if (summary.corpus_divergences == 0 and summary.fuzz_divergences == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
