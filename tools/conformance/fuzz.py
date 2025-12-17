from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

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
        "--subset",
        type=str,
        default="",
        help=(
            "Restrict generator to a comma-separated set of templates "
            "(arith,dispatch,cycle_sum,map_fold,fib,undef_name). Empty means all."
        ),
    )
    ap.add_argument(
        "--raw",
        action="store_true",
        help="Write per-program raw JSONL logs under data/raw/fuzz_runs/",
    )
    ap.add_argument(
        "--raw-path",
        type=str,
        default="",
        help="Optional explicit path for the raw JSONL log",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Print a machine-readable JSON summary",
    )
    args = ap.parse_args()

    subset_templates: set[str] | None = None
    if str(args.subset).strip():
        subset_templates = {s.strip() for s in str(args.subset).split(",") if s.strip()}

    raw_fp = None
    if bool(args.raw):
        raw_path = (
            Path(str(args.raw_path))
            if str(args.raw_path).strip()
            else Path("data/raw/fuzz_runs") / f"seed_{int(args.seed)}_n_{int(args.n)}.jsonl"
        )
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_fp = raw_path.open("w", encoding="utf-8")

    def _sha256_json(obj: Any) -> str:
        b = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(b).hexdigest()

    def on_case(i: int, seed: int, src: str, interp: Any, vm: Any, ok: bool, reason: str) -> None:
        if raw_fp is None:
            return
        rec = {
            "id": i,
            "seed": seed,
            "src_sha256": hashlib.sha256(src.encode("utf-8")).hexdigest(),
            "interp_sha256": _sha256_json(getattr(interp, "__dict__", interp)),
            "vm_sha256": _sha256_json(getattr(vm, "__dict__", vm)),
            "ok": bool(ok),
            "reason": str(reason),
            "interp_term": getattr(interp, "termination", None),
            "vm_term": getattr(vm, "termination", None),
        }
        raw_fp.write(json.dumps(rec, ensure_ascii=False) + "\n")

    stats, saved = run_fuzz(
        n=int(args.n),
        seed=int(args.seed),
        save_dir=Path(str(args.save_dir)),
        fail_fast=bool(args.fail_fast),
        save_non_ok=bool(args.save_non_ok),
        save_non_ok_limit=int(args.save_non_ok_limit),
        subset_templates=subset_templates,
        on_case=on_case,
    )

    if raw_fp is not None:
        raw_fp.close()

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
