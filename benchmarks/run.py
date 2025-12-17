from __future__ import annotations

# ruff: noqa: E402

import argparse
import contextlib
import io
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


def bench_file(path: Path, *, iters: int, warmup: int) -> tuple[float, float, int]:
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

    def vm_run() -> None:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            vm.run(code)

    for _ in range(warmup):
        interp_run()
        vm_run()

    t_interp = _timeit(interp_run, iters=iters)
    t_vm = _timeit(vm_run, iters=iters)
    return _median_ms(t_interp), _median_ms(t_vm), instr_count


def _iter_suay_files(root: Path) -> list[Path]:
    if root.is_file() and root.suffix == ".suay":
        return [root]
    if root.is_dir():
        return sorted(p for p in root.rglob("*.suay") if p.is_file())
    return []


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="benchmarks",
        description="Run SuayLang micro-benchmarks and print a Markdown table.",
    )
    ap.add_argument(
        "paths",
        nargs="*",
        default=["evaluation/tasks"],
        help=".suay files or directories (default: evaluation/tasks)",
    )
    ap.add_argument("--iters", type=int, default=200, help="Iterations per program")
    ap.add_argument("--warmup", type=int, default=5, help="Warm-up runs per backend")
    args = ap.parse_args()

    roots = [Path(p) for p in args.paths]
    targets: list[Path] = []
    for r in roots:
        targets.extend(_iter_suay_files(r))

    if not targets:
        print("benchmarks: no .suay files found")
        return 2

    rows: list[tuple[str, float, float, float, int]] = []
    for p in targets:
        ti, tv, ninstr = bench_file(p, iters=int(args.iters), warmup=int(args.warmup))
        ratio = (ti / tv) if tv > 0 else float("inf")
        rows.append((p.as_posix(), ti, tv, ratio, ninstr))

    print("| Program | Interpreter (ms) | VM (ms) | Relative (interp/vm) | VM instr |")
    print("|---|---:|---:|---:|---:|")
    for rel, ti, tv, ratio, ninstr in rows:
        print(f"| {rel} | {ti:.3f} | {tv:.3f} | {ratio:.2f} | {ninstr} |")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
