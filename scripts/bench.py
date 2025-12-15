from __future__ import annotations

import argparse
import contextlib
import io
import statistics
import time
from pathlib import Path

from suaylang.compiler import Compiler
from suaylang.interpreter import Interpreter
from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.vm import VM


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


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


def _report(label: str, times: list[float]) -> None:
    ms = [t * 1000.0 for t in times]
    print(
        f"{label}: median={statistics.median(ms):.3f}ms  min={min(ms):.3f}ms  max={max(ms):.3f}ms"
    )


def bench_file(path: str, *, iters: int) -> None:
    src = _read(path)

    # Parse once for execution benchmarks.
    program = _parse(src, filename=path)

    def parse_only() -> None:
        _parse(src, filename=path)

    interp = Interpreter(source=src, filename=path, trace=False)

    def interp_run() -> None:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            interp.eval_program(program)

    compiler = Compiler()

    def compile_only() -> None:
        compiler.compile_program(program, name=path)

    code = compiler.compile_program(program, name=path)
    vm = VM(source=src, filename=path, trace=False)

    def vm_run() -> None:
        with (
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            vm.run(code)

    # Warm-up (small, fixed).
    for _ in range(5):
        parse_only()
        interp_run()
        vm_run()

    print(f"== {path} ==")
    _report("parse", _timeit(parse_only, iters=iters))
    _report("interp", _timeit(interp_run, iters=iters))
    _report("compile", _timeit(compile_only, iters=iters))
    _report("vm", _timeit(vm_run, iters=iters))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=200)
    ap.add_argument(
        "paths",
        nargs="*",
        default=["examples/hello.suay", "examples/committee_03_cycle.suay"],
    )
    args = ap.parse_args()

    for p in args.paths:
        bench_file(p, iters=args.iters)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
