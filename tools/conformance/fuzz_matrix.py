from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .fuzz_runner import run_fuzz

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_SEEDS = _REPO_ROOT / "tools" / "conformance" / "fuzz_seeds.json"


def main() -> int:
    ap = argparse.ArgumentParser(prog="suay-fuzz-matrix")
    ap.add_argument("--n", type=int, default=5000, help="Programs per seed")
    ap.add_argument(
        "--seeds",
        type=str,
        default=str(_DEFAULT_SEEDS),
        help="JSON file containing seed lists",
    )
    ap.add_argument(
        "--profile",
        choices=["ci", "nightly"],
        default="ci",
        help="Which seed list to use from the seeds JSON",
    )
    ap.add_argument(
        "--save-dir",
        type=str,
        default="tools/conformance/fuzz_failures",
        help="Directory for saved repro cases",
    )
    ap.add_argument("--fail-fast", action="store_true")
    ap.add_argument("--json-out", type=str, default="", help="Write JSON summary")
    args = ap.parse_args()

    seeds_doc = json.loads(Path(args.seeds).read_text(encoding="utf-8"))
    seeds = [int(x) for x in seeds_doc[str(args.profile)]]

    all_stats = []
    all_saved: list[str] = []
    any_div = False

    for seed in seeds:
        stats, saved = run_fuzz(
            n=int(args.n),
            seed=int(seed),
            save_dir=Path(str(args.save_dir)),
            fail_fast=bool(args.fail_fast),
            save_non_ok=False,
            save_non_ok_limit=0,
        )
        all_stats.append(asdict(stats))
        all_saved.extend(str(p) for p in saved)
        if stats.divergences:
            any_div = True
            if args.fail_fast:
                break

    summary = {
        "profile": str(args.profile),
        "n_per_seed": int(args.n),
        "seeds": seeds,
        "stats": all_stats,
        "saved": all_saved,
    }

    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        total = sum(s["n"] for s in all_stats)
        div = sum(s["divergences"] for s in all_stats)
        ok = sum(s["ok"] for s in all_stats)
        rt = sum(s["runtime_errors"] for s in all_stats)
        lex = sum(s["lex_errors"] for s in all_stats)
        parse = sum(s["parse_errors"] for s in all_stats)
        internal = sum(s["internal_errors"] for s in all_stats)
        print(
            f"fuzz-matrix: profile={args.profile} seeds={len(seeds)} total_n={total} "
            f"divergences={div} ok={ok} runtime={rt} lex={lex} parse={parse} internal={internal}"
        )
        if all_saved:
            print(f"saved repro cases: {len(all_saved)}")

    return 1 if any_div else 0


if __name__ == "__main__":
    raise SystemExit(main())
