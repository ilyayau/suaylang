from __future__ import annotations

import argparse
import json
from pathlib import Path

from .fuzz_runner import run_fuzz


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="suay-fuzz", description="SuayLang differential fuzz runner"
    )
    ap.add_argument(
        "--n", type=int, default=5000, help="Number of programs to generate"
    )
    ap.add_argument("--seed", type=int, default=0, help="RNG seed (deterministic)")
    ap.add_argument(
        "--save-dir",
        type=str,
        default="tools/conformance/fuzz_failures",
        help="Directory for saved repro cases",
    )
    ap.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first divergence",
    )
    ap.add_argument(
        "--save-non-ok",
        action="store_true",
        help="Also save a limited number of lex/parse/runtime/internal cases (for diagnostics regression)",
    )
    ap.add_argument(
        "--save-non-ok-limit",
        type=int,
        default=3,
        help="Max saved non-ok cases per kind",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Print a machine-readable JSON summary",
    )
    args = ap.parse_args()

    stats, saved = run_fuzz(
        n=int(args.n),
        seed=int(args.seed),
        save_dir=Path(str(args.save_dir)),
        fail_fast=bool(args.fail_fast),
        save_non_ok=bool(args.save_non_ok),
        save_non_ok_limit=int(args.save_non_ok_limit),
    )

    if args.json:
        print(
            json.dumps(
                {"stats": stats.__dict__, "saved": [str(p) for p in saved]}, indent=2
            )
        )
    else:
        print(
            "fuzz: seed={seed} n={n} divergences={div} ok={ok} "
            "runtime={rt} lex={lex} parse={parse} internal={internal}".format(
                seed=stats.seed,
                n=stats.n,
                div=stats.divergences,
                ok=stats.ok,
                rt=stats.runtime_errors,
                lex=stats.lex_errors,
                parse=stats.parse_errors,
                internal=stats.internal_errors,
            )
        )
        if saved:
            print(f"saved repro cases: {len(saved)}")

    return 1 if stats.divergences else 0


if __name__ == "__main__":
    raise SystemExit(main())
