from __future__ import annotations

# ruff: noqa: E402

import argparse
import contextlib
import csv
import io
import json
import statistics
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from suaylang.bytecode import Code
from suaylang.compiler import Compiler
from suaylang.interpreter import Interpreter
from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.vm import VM


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse(source: str, filename: str) -> object:
    tokens = Lexer(source, filename=filename).tokenize()
    return Parser(tokens, source, filename=filename).parse_program()


def _timeit(fn, *, iters: int) -> list[float]:
    times: list[float] = []
    for _ in range(iters):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return times


def _median_ms(times: list[float]) -> float:
    return statistics.median(times) * 1000.0


def _count_instrs(code: Code) -> int:
    """Count instructions across nested code objects produced by closures."""

    seen: set[int] = set()

    def walk(c: Code) -> int:
        cid = id(c)
        if cid in seen:
            return 0
        seen.add(cid)

        total = len(c.instrs)
        for ins in c.instrs:
            arg = ins.arg
            if isinstance(arg, Code):
                total += walk(arg)
            elif isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], Code):
                total += walk(arg[0])
        return total

    return walk(code)


def bench_file(path: Path, *, iters: int, warmup: int) -> tuple[float, float, int, int]:
    src = _read(path)
    program = _parse(src, filename=str(path))

    interp = Interpreter(source=src, filename=str(path), trace=False)

    def interp_run() -> None:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            interp.eval_program(program)

    compiler = Compiler()
    code = compiler.compile_program(program, name=str(path))
    instr_count = _count_instrs(code)
    vm = VM(source=src, filename=str(path), trace=False)

    def vm_run_with_stats() -> tuple[object, int]:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            return vm.run_with_stats(code)

    def vm_run() -> None:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            vm.run(code)

    for _ in range(warmup):
        interp_run()
        vm_run()

    # Executed instruction count is deterministic for a given program.
    _val, exec_steps = vm_run_with_stats()

    t_interp = _timeit(interp_run, iters=iters)
    t_vm = _timeit(vm_run, iters=iters)
    return _median_ms(t_interp), _median_ms(t_vm), instr_count, int(exec_steps)


def _iter_suay_files(root: Path) -> list[Path]:
    if root.is_file() and root.suffix == ".suay":
        return [root]
    if root.is_dir():
        return sorted(p for p in root.rglob("*.suay") if p.is_file())
    return []


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="benchmarks",
        description="Run SuayLang micro-benchmarks and optionally write JSON/CSV/Markdown results.",
    )
    ap.add_argument(
        "paths",
        nargs="*",
        default=["evaluation/tasks"],
        help=".suay files or directories (default: evaluation/tasks)",
    )
    ap.add_argument("--iters", type=int, default=200, help="Iterations per program")
    ap.add_argument("--warmup", type=int, default=5, help="Warm-up runs per backend")
    ap.add_argument(
        "--json-out",
        type=str,
        default="",
        help="Write machine-readable JSON results to this path",
    )
    ap.add_argument(
        "--csv-out",
        type=str,
        default="",
        help="Write machine-readable CSV results to this path",
    )
    ap.add_argument(
        "--md-out",
        type=str,
        default="",
        help="Write Markdown summary table to this path",
    )
    args = ap.parse_args()

    roots = [Path(p) for p in args.paths]
    targets: list[Path] = []
    for r in roots:
        targets.extend(_iter_suay_files(r))

    if not targets:
        print("benchmarks: no .suay files found")
        return 2

    rows: list[dict[str, object]] = []
    for p in targets:
        ti, tv, ninstr, steps = bench_file(
            p, iters=int(args.iters), warmup=int(args.warmup)
        )
        ratio = (ti / tv) if tv > 0 else float("inf")
        rows.append(
            {
                "program": p.as_posix(),
                "interp_ms_median": float(ti),
                "vm_ms_median": float(tv),
                "relative_interp_over_vm": float(ratio),
                "vm_instr_static": int(ninstr),
                "vm_instr_executed": int(steps),
                "iters": int(args.iters),
                "warmup": int(args.warmup),
            }
        )

    md_lines: list[str] = []
    md_lines.append(
        "| Program | Interpreter (ms, median) | VM (ms, median) | Relative (interp/vm) | VM instr (static) | VM instr (executed) |"
    )
    md_lines.append("|---|---:|---:|---:|---:|---:|")
    for r in rows:
        md_lines.append(
            "| {program} | {ti:.3f} | {tv:.3f} | {ratio:.2f} | {ninstr} | {steps} |".format(
                program=r["program"],
                ti=float(r["interp_ms_median"]),
                tv=float(r["vm_ms_median"]),
                ratio=float(r["relative_interp_over_vm"]),
                ninstr=int(r["vm_instr_static"]),
                steps=int(r["vm_instr_executed"]),
            )
        )

    # Default behavior: print a Markdown table to stdout.
    if not args.json_out and not args.csv_out and not args.md_out:
        print("\n".join(md_lines))
        return 0

    if args.md_out:
        out = Path(str(args.md_out))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    if args.json_out:
        out = Path(str(args.json_out))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"rows": rows}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.csv_out:
        out = Path(str(args.csv_out))
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(
                f,
                fieldnames=[
                    "program",
                    "interp_ms_median",
                    "vm_ms_median",
                    "relative_interp_over_vm",
                    "vm_instr_static",
                    "vm_instr_executed",
                    "iters",
                    "warmup",
                ],
            )
            w.writeheader()
            for r in rows:
                w.writerow(r)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
