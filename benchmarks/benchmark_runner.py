from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import platform
import statistics
import subprocess
import sys
import time
import tracemalloc
from dataclasses import dataclass
from pathlib import Path

from suaylang.bytecode import Code
from suaylang.compiler import Compiler
from suaylang.interpreter import Interpreter
from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.vm import VM

_REPO_ROOT = Path(__file__).resolve().parents[1]


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=_REPO_ROOT, text=True).strip()
    except Exception:
        return "unknown"


def _cpu_info() -> str:
    # Best-effort; stable enough for report metadata.
    try:
        if os.path.exists("/proc/cpuinfo"):
            txt = Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="ignore")
            for line in txt.splitlines():
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return platform.processor() or "unknown"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse(source: str, filename: str) -> object:
    tokens = Lexer(source, filename=filename).tokenize()
    return Parser(tokens, source, filename=filename).parse_program()


def _count_instrs(code: Code) -> int:
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


def _percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    if p <= 0:
        return sorted_vals[0]
    if p >= 1:
        return sorted_vals[-1]
    # Nearest-rank method.
    k = int((len(sorted_vals) * p) + 0.999999999) - 1
    k = max(0, min(k, len(sorted_vals) - 1))
    return sorted_vals[k]


def _p90_ms(times: list[float]) -> float:
    xs = sorted(times)
    return _percentile(xs, 0.90) * 1000.0


def _mem_peak_bytes(fn) -> int:
    # Best-effort: measures Python allocations via tracemalloc, not RSS.
    tracemalloc.start()
    try:
        fn()
        _cur, peak = tracemalloc.get_traced_memory()
        return int(peak)
    finally:
        tracemalloc.stop()


@dataclass(frozen=True)
class BenchRow:
    program: str
    parse_ms_median: float
    parse_ms_p90: float
    compile_ms_median: float
    compile_ms_p90: float
    interp_ms_median: float
    interp_ms_p90: float
    vm_ms_median: float
    vm_ms_p90: float
    vm_instr_static: int
    vm_steps_ok: int
    mem_peak_parse_bytes: int
    mem_peak_compile_bytes: int
    mem_peak_interp_bytes: int
    mem_peak_vm_bytes: int
    raw_parse_s: list[float]
    raw_compile_s: list[float]
    raw_interp_s: list[float]
    raw_vm_s: list[float]


def bench_file(path: Path, *, iters: int, warmup: int) -> BenchRow:
    src = _read(path)

    def parse_once() -> object:
        return _parse(src, filename=str(path))

    # Warm caches for fairer steady-state results.
    for _ in range(warmup):
        parse_once()

    parse_times = _timeit(parse_once, iters=iters)
    program = parse_once()

    compiler = Compiler()

    def compile_once() -> Code:
        return compiler.compile_program(program, name=str(path))

    for _ in range(warmup):
        compile_once()

    compile_times = _timeit(compile_once, iters=iters)
    code = compile_once()

    instr_static = _count_instrs(code)

    interp = Interpreter(source=src, filename=str(path), trace=False)

    def interp_run() -> object:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            return interp.eval_program(program)

    vm = VM(source=src, filename=str(path), trace=False)

    def vm_run_with_stats() -> tuple[object, int]:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            return vm.run_with_stats(code)

    def vm_run() -> object:
        v, _steps = vm_run_with_stats()
        return v

    for _ in range(warmup):
        interp_run()
        vm_run()

    # Deterministic step count for successful run.
    _val, steps_ok = vm_run_with_stats()

    interp_times = _timeit(interp_run, iters=iters)
    vm_times = _timeit(vm_run, iters=iters)

    # Memory peaks (best-effort; single representative run per phase).
    mem_parse = _mem_peak_bytes(parse_once)
    mem_compile = _mem_peak_bytes(compile_once)
    mem_interp = _mem_peak_bytes(interp_run)
    mem_vm = _mem_peak_bytes(vm_run)

    return BenchRow(
        program=path.as_posix(),
        parse_ms_median=_median_ms(parse_times),
        parse_ms_p90=_p90_ms(parse_times),
        compile_ms_median=_median_ms(compile_times),
        compile_ms_p90=_p90_ms(compile_times),
        interp_ms_median=_median_ms(interp_times),
        interp_ms_p90=_p90_ms(interp_times),
        vm_ms_median=_median_ms(vm_times),
        vm_ms_p90=_p90_ms(vm_times),
        vm_instr_static=int(instr_static),
        vm_steps_ok=int(steps_ok),
        mem_peak_parse_bytes=int(mem_parse),
        mem_peak_compile_bytes=int(mem_compile),
        mem_peak_interp_bytes=int(mem_interp),
        mem_peak_vm_bytes=int(mem_vm),
        raw_parse_s=list(parse_times),
        raw_compile_s=list(compile_times),
        raw_interp_s=list(interp_times),
        raw_vm_s=list(vm_times),
    )


def _iter_bench_programs(bench_dir: Path) -> list[Path]:
    programs = sorted(p for p in bench_dir.glob("*.suay") if p.is_file())
    # Exclude module sources used by benchmarks.
    programs = [p for p in programs if p.name not in {"mod.suay"}]
    return programs


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(prog="benchmark-runner", description="Run SuayLang benchmarks with parse/compile/exec timings.")
    ap.add_argument("--profile", choices=["smoke", "full"], default="full")
    ap.add_argument("--iters", type=int, default=20)
    ap.add_argument("--warmup", type=int, default=3)
    ap.add_argument("--bench-dir", type=str, default=str(_REPO_ROOT / "benchmarks" / "v1"))
    ap.add_argument("--out-dir", type=str, default=str(_REPO_ROOT / "results"))
    args = ap.parse_args()

    iters = int(args.iters)
    warmup = int(args.warmup)

    if args.profile == "full" and iters < 20:
        iters = 20

    if args.profile == "smoke":
        # Keep CI bounded.
        iters = min(iters, 5)
        warmup = min(warmup, 1)

    bench_dir = Path(str(args.bench_dir))
    programs = _iter_bench_programs(bench_dir)
    if len(programs) != 6:
        print(f"bench: expected 6 benchmark programs in {bench_dir.as_posix()}, found {len(programs)}")
        for p in programs:
            print(f"- {p.name}")
        return 2

    rows: list[BenchRow] = []
    for p in programs:
        rows.append(bench_file(p, iters=iters, warmup=warmup))

    out_dir = Path(str(args.out_dir))
    raw_path = out_dir / "bench_raw.json"
    md_path = out_dir / "benchmarks.md"

    payload = {
        "commit": _git_commit(),
        "metadata": {
            "python": sys.version.replace("\n", " "),
            "platform": platform.platform(),
            "cpu": _cpu_info(),
        },
        "profile": args.profile,
        "iters": iters,
        "warmup": warmup,
        "bench_dir": bench_dir.as_posix(),
        "rows": [row.__dict__ for row in rows],
    }

    _write_json(raw_path, payload)

    # Human-readable summary.
    md: list[str] = []
    md.append("# Benchmarks (SuayLang)")
    md.append("")
    md.append("Backed by raw JSON in `results/bench_raw.json`.")
    md.append("")
    md.append(f"- commit: `{payload['commit']}`")
    md.append(f"- profile: `{args.profile}`")
    md.append(f"- iters: {iters} (per phase; per program)")
    md.append(f"- warmup: {warmup}")
    md.append(f"- bench_dir: `{payload['bench_dir']}`")
    md.append(f"- python: {payload['metadata']['python']}")
    md.append(f"- platform: {payload['metadata']['platform']}")
    md.append(f"- cpu: {payload['metadata']['cpu']}")
    md.append("")

    md.append("## Summary table (ms)")
    md.append("")
    md.append("All timings are median / p90.")
    md.append("")
    md.append("| Program | Parse | Compile | Interp | VM | interp/vm (median) | VM instr | VM steps |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        ratio = (r.interp_ms_median / r.vm_ms_median) if r.vm_ms_median > 0 else float("inf")
        md.append(
            "| {p} | {pa:.3f}/{pa90:.3f} | {co:.3f}/{co90:.3f} | {ti:.3f}/{ti90:.3f} | {tv:.3f}/{tv90:.3f} | {ra:.2f} | {ni} | {st} |".format(
                p=Path(r.program).name,
                pa=r.parse_ms_median,
                pa90=r.parse_ms_p90,
                co=r.compile_ms_median,
                co90=r.compile_ms_p90,
                ti=r.interp_ms_median,
                ti90=r.interp_ms_p90,
                tv=r.vm_ms_median,
                tv90=r.vm_ms_p90,
                ra=ratio,
                ni=r.vm_instr_static,
                st=r.vm_steps_ok,
            )
        )

    md.append("")
    md.append("## Interpretation (10 bullets, no hand-waving)")
    md.append("")
    md.append("- VM wins are expected when the same bytecode runs many steps (e.g., `cycle` / recursion), amortizing compile overhead.")
    md.append("- Interpreter can be competitive on tiny programs where parse/compile dominate and runtime is short.")
    md.append("- `dispatch` heavy benchmarks stress pattern matching and branching; they show whether opcode dispatch beats AST walking.")
    md.append("- `cycle` state-machine workloads are designed to be branchy but allocation-light; they tend to favor the VM.")
    md.append("- `map+fold` exercises higher-order builtins plus closure calls; results depend heavily on how often the backend crosses Python function boundaries.")
    md.append("- Text/Map workloads include `put/keys/has/text`; these are Python-implemented builtins and may reduce VM advantage (both backends pay Python cost).")
    md.append("- Module access uses repeated `link` calls; module caching helps, so this mostly measures cached lookup + call-site error framing overhead.")
    md.append("- p90 values make tail latency visible; if p90 diverges from median, noise (GC, CPU scheduling) is a likely contributor.")
    md.append("- Memory numbers are `tracemalloc` peaks (Python allocations), not RSS; treat them as relative signals only.")
    md.append("- This is a microbenchmark suite: it does not model I/O, large modules, or long-running real applications; use it for trends, not absolutes.")

    _write_md(md_path, "\n".join(md))

    print(f"bench: wrote {raw_path} and {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
