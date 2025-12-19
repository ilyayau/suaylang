from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from dataclasses import asdict
from pathlib import Path

from .comparator import divergence_fingerprint, equivalent
from .coverage import ast_node_counts, opcode_counts
from .minimizer import minimize_by_lines
from .program_generator import generate_invalid_program, generate_valid_program
from .runner import environment_metadata, observe_interpreter, observe_vm

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _git_commit() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=_REPO_ROOT, text=True
        ).strip()
        return out
    except Exception:
        return "unknown"


def _merge_counts(dst: dict[str, int], src: dict[str, int]) -> None:
    for k, v in src.items():
        dst[k] = dst.get(k, 0) + int(v)


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _profile_defaults(profile: str) -> tuple[list[int], int, int]:
    if profile == "ci":
        # Requested CI gate: seeds 0..9, N=500/seed (mix valid+invalid).
        return list(range(0, 10)), 400, 100
    if profile == "full":
        # Requested local full run: seeds 0..99, N=2000/seed (mix valid+invalid).
        return list(range(0, 100)), 1600, 400
    raise ValueError(f"Unknown profile: {profile}")


def _split_across_buckets(n: int, buckets: list[str]) -> dict[str, int]:
    if n < 0:
        raise ValueError("n must be >= 0")
    if not buckets:
        raise ValueError("buckets must be non-empty")
    base = n // len(buckets)
    rem = n % len(buckets)
    out: dict[str, int] = {}
    for i, b in enumerate(buckets):
        out[b] = base + (1 if i < rem else 0)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(prog="diff-test", description="Differential testing harness (interpreter vs VM).")
    ap.add_argument("--profile", choices=["ci", "full"], default="ci")
    ap.add_argument("--timeout-s", type=float, default=0.5)
    ap.add_argument("--out-dir", type=str, default=str(_REPO_ROOT / "results"))
    ap.add_argument("--save-generated", action="store_true", help="Save a small sample of generated programs under tools/diff_test/corpus/generated/.")
    args = ap.parse_args()

    seeds, n_valid, n_invalid = _profile_defaults(str(args.profile))
    buckets = ["small", "medium", "large"]

    out_dir = Path(str(args.out_dir))
    regress_dir = _REPO_ROOT / "tools" / "diff_test" / "corpus" / "regressions"
    gen_dir = _REPO_ROOT / "tools" / "diff_test" / "corpus" / "generated"

    start = time.perf_counter()

    total = 0
    divergences: list[dict[str, object]] = []
    divergence_ids: set[str] = set()

    term_counts: dict[str, int] = {}
    invalid_category_counts: dict[str, int] = {}
    size_counts: dict[str, int] = {b: 0 for b in buckets}

    per_seed: dict[str, dict[str, object]] = {}

    ast_counts_total: dict[str, int] = {}
    opcode_counts_total: dict[str, int] = {}

    # VM executed-step counts are available for successful VM runs.
    total_vm_steps_ok = 0

    def _seed_key(seed: int | str | None) -> str:
        if seed is None:
            return "<none>"
        return str(seed)

    def record_termination(o: object, *, seed: int | str | None) -> None:
        t = getattr(o, "termination")
        term_counts[str(t)] = term_counts.get(str(t), 0) + 1

        sk = _seed_key(seed)
        entry = per_seed.get(sk)
        if entry is None:
            entry = {
                "seed": sk,
                "total_programs": 0,
                "divergences": 0,
                "termination_counts": {},
            }
            per_seed[sk] = entry

        entry["total_programs"] = int(entry["total_programs"]) + 1
        tc = dict(entry["termination_counts"])  # type: ignore[assignment]
        tc[str(t)] = int(tc.get(str(t), 0)) + 1
        entry["termination_counts"] = tc

    # Run fixed corpus (including minimized regressions) first if present.
    fixed_dir = _REPO_ROOT / "tools" / "diff_test" / "corpus" / "fixed"
    fixed_files = sorted(p for p in fixed_dir.rglob("*.suay") if p.is_file())
    regression_files = sorted(p for p in regress_dir.rglob("*.suay") if p.is_file())

    def run_case(
        source: str, *, name: str, category: str, size_bucket: str, seed: int | str | None
    ) -> None:
        nonlocal total, total_vm_steps_ok
        total += 1
        size_counts[size_bucket] = size_counts.get(size_bucket, 0) + 1

        i = observe_interpreter(source, filename=name, timeout_s=float(args.timeout_s))
        v = observe_vm(source, filename=name, timeout_s=float(args.timeout_s))

        record_termination(i, seed=seed)

        ok, reason = equivalent(i, v)
        if ok:
            if v.termination == "ok" and v.vm_steps is not None:
                total_vm_steps_ok += int(v.vm_steps)
            # Coverage is best-effort: only if parsing/compiling succeeds.
            try:
                _merge_counts(ast_counts_total, ast_node_counts(source, filename=name))
            except Exception:
                pass
            try:
                _merge_counts(opcode_counts_total, opcode_counts(source, filename=name))
            except Exception:
                pass
            return

        # Divergence.
        fp = divergence_fingerprint(
            source=source,
            interp=i,
            vm=v,
            category=category,
            size_bucket=size_bucket,
        )
        if fp not in divergence_ids:
            divergence_ids.add(fp)

        sk = _seed_key(seed)
        if sk in per_seed:
            per_seed[sk]["divergences"] = int(per_seed[sk]["divergences"]) + 1

        # Minimize and save regression.
        minimized = minimize_by_lines(
            source=source,
            filename=name,
            category=category,
            size_bucket=size_bucket,
            timeout_s=float(args.timeout_s),
        )

        regress_dir.mkdir(parents=True, exist_ok=True)
        repro_path = regress_dir / f"{fp}.suay"
        repro_path.write_text(minimized.minimized_source, encoding="utf-8")

        meta_path = regress_dir / f"{fp}.json"
        _write_json(
            meta_path,
            {
                "id": fp,
                "reason": reason,
                "category": category,
                "size_bucket": size_bucket,
                "removed_lines": minimized.removed_lines,
                "interp": asdict(i),
                "vm": asdict(v),
                "repro": repro_path.as_posix(),
            },
        )

        divergences.append(
            {
                "id": fp,
                "reason": reason,
                "category": category,
                "size_bucket": size_bucket,
                "repro": repro_path.as_posix(),
                "meta": meta_path.as_posix(),
            }
        )

    # Fixed cases (treated as valid).
    for p in fixed_files:
        src = p.read_text(encoding="utf-8")
        run_case(src, name=p.as_posix(), category="fixed", size_bucket="small", seed="fixed")

    for p in regression_files:
        src = p.read_text(encoding="utf-8")
        run_case(src, name=p.as_posix(), category="regression", size_bucket="small", seed="regression")

    # Generated cases.
    # Ensure exact per-seed totals across buckets (no rounding loss).
    valid_by_bucket = _split_across_buckets(int(n_valid), buckets)
    invalid_by_bucket = _split_across_buckets(int(n_invalid), buckets)

    save_budget = 3 if args.save_generated else 0

    for seed in seeds:
        for bucket in buckets:
            for idx in range(int(valid_by_bucket[bucket])):
                src = generate_valid_program(seed=int(seed), index=int(idx), size_bucket=bucket)
                name = f"<gen valid seed={seed} idx={idx} bucket={bucket}>"
                run_case(src, name=name, category="valid", size_bucket=bucket, seed=int(seed))
                if save_budget > 0 and idx < save_budget:
                    gen_dir.mkdir(parents=True, exist_ok=True)
                    (gen_dir / f"seed{seed}_{bucket}_valid_{idx}.suay").write_text(src, encoding="utf-8")

            for idx in range(int(invalid_by_bucket[bucket])):
                cat, src = generate_invalid_program(seed=int(seed), index=int(idx), size_bucket=bucket)
                invalid_category_counts[cat] = invalid_category_counts.get(cat, 0) + 1
                name = f"<gen invalid seed={seed} idx={idx} bucket={bucket} cat={cat}>"
                run_case(src, name=name, category=f"invalid/{cat}", size_bucket=bucket, seed=int(seed))
                if save_budget > 0 and idx < save_budget:
                    gen_dir.mkdir(parents=True, exist_ok=True)
                    (gen_dir / f"seed{seed}_{bucket}_invalid_{cat}_{idx}.suay").write_text(src, encoding="utf-8")

    elapsed_s = time.perf_counter() - start

    report = {
        "profile": args.profile,
        "commit": _git_commit(),
        "metadata": environment_metadata(),
        "seeds": seeds,
        "n_valid_per_seed": n_valid,
        "n_invalid_per_seed": n_invalid,
        "n_total_per_seed": int(n_valid) + int(n_invalid),
        "size_buckets": buckets,
        "total_programs": total,
        "total_vm_steps_ok": int(total_vm_steps_ok),
        "divergences": len(divergences),
        "unique_divergences": len(divergence_ids),
        "fixed_divergences": 0,
        "termination_counts": term_counts,
        "invalid_category_counts": invalid_category_counts,
        "size_bucket_counts": size_counts,
        "per_seed": dict(sorted(per_seed.items(), key=lambda kv: kv[0])),
        "runtime_seconds": elapsed_s,
        "divergence_index": divergences,
    }

    coverage = {
        "commit": _git_commit(),
        "profile": args.profile,
        "ast_node_counts": dict(sorted(ast_counts_total.items())),
        "opcode_counts": dict(sorted(opcode_counts_total.items())),
        "termination_counts": term_counts,
    }

    feature_counts = {
        "dispatch": int(ast_counts_total.get("Dispatch", 0)),
        "cycle": int(ast_counts_total.get("Cycle", 0)),
        "lambda": int(ast_counts_total.get("Lambda", 0)),
        "call": int(ast_counts_total.get("Call", 0)),
        "variant": int(ast_counts_total.get("Variant", 0)),
        "map": int(ast_counts_total.get("Map", 0)),
        "list": int(ast_counts_total.get("ListLit", 0)),
        "tuple": int(ast_counts_total.get("TupleLit", 0)),
        "binding": int(ast_counts_total.get("Bind", 0)),
        "mutation": int(ast_counts_total.get("Set", 0)),
        "block": int(ast_counts_total.get("Block", 0)),
    }
    coverage["feature_counts"] = feature_counts

    diff_json = out_dir / "diff_report.json"
    diff_md = out_dir / "diff_report.md"
    cov_json = out_dir / "coverage.json"
    cov_md = out_dir / "coverage.md"

    _write_json(diff_json, report)
    _write_json(cov_json, coverage)

    # Markdown summaries.
    md = []
    md.append(f"# Differential test report ({args.profile})")
    md.append("")
    md.append(f"- commit: `{report['commit']}`")
    md.append(f"- total programs: {report['total_programs']}")
    md.append(f"- seeds: {len(seeds)}")
    md.append(f"- VM executed steps (ok runs): {report['total_vm_steps_ok']}")
    md.append(f"- divergences: {report['divergences']} (unique: {report['unique_divergences']})")
    md.append(f"- runtime: {report['runtime_seconds']:.2f}s")
    md.append("")

    md.append("## Per-seed breakdown")
    md.append("")
    md.append("| seed | total | divergences |")
    md.append("|---:|---:|---:|")
    for sk, stats in sorted(per_seed.items(), key=lambda kv: kv[0]):
        md.append(
            f"| {sk} | {int(stats.get('total_programs', 0))} | {int(stats.get('divergences', 0))} |"
        )
    md.append("")
    md.append("## Termination breakdown")
    md.append("")
    md.append("| termination | count |")
    md.append("|---|---:|")
    for k, v in sorted(term_counts.items()):
        md.append(f"| {k} | {v} |")

    md.append("")
    md.append("## Divergences (if any)")
    md.append("")
    if divergences:
        md.append("| id | category | bucket | reason | repro |")
        md.append("|---|---|---|---|---|")
        for d in divergences[:50]:
            md.append(
                f"| {d['id']} | {d['category']} | {d['size_bucket']} | {d['reason']} | {d['repro']} |"
            )
        if len(divergences) > 50:
            md.append("")
            md.append(f"(showing first 50 of {len(divergences)})")
    else:
        md.append("No divergences recorded.")

    _write_md(diff_md, "\n".join(md))

    cm = []
    cm.append(f"# Coverage report ({args.profile})")
    cm.append("")
    cm.append(f"- commit: `{coverage['commit']}`")
    cm.append("")

    cm.append("## AST node kinds")
    cm.append("")
    cm.append(f"Observed node kinds: {len(ast_counts_total)}")
    cm.append("")
    cm.append("| node_kind | count |")
    cm.append("|---|---:|")
    for k, v in sorted(ast_counts_total.items(), key=lambda kv: (-kv[1], kv[0]))[:60]:
        cm.append(f"| {k} | {v} |")
    if len(ast_counts_total) > 60:
        cm.append("")
        cm.append(f"(showing top 60 of {len(ast_counts_total)})")

    cm.append("")
    cm.append("## Opcode kinds (static)")
    cm.append("")
    cm.append(f"Observed opcode kinds: {len(opcode_counts_total)}")
    cm.append("")
    cm.append("| opcode | count |")
    cm.append("|---|---:|")
    for k, v in sorted(opcode_counts_total.items(), key=lambda kv: (-kv[1], kv[0])):
        cm.append(f"| {k} | {v} |")

    cm.append("")
    cm.append("## Feature coverage (derived)")
    cm.append("")
    cm.append("This table is derived from AST node counts (best-effort).")
    cm.append("")
    cm.append("| feature | count |")
    cm.append("|---|---:|")
    for k, v in sorted(feature_counts.items()):
        cm.append(f"| {k} | {v} |")

    _write_md(cov_md, "\n".join(cm))

    print(f"diff-test: wrote {diff_json} and {diff_md}")
    print(f"diff-test: wrote {cov_json} and {cov_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
