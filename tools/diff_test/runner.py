from __future__ import annotations

import contextlib
import io
import os
import platform
import re
import signal
import sys
import time
from dataclasses import dataclass
from typing import Literal

from suaylang.compiler import Compiler
from suaylang.errors import Diagnostic, SuayError
from suaylang.interpreter import Interpreter
from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.runtime import SuayRuntimeError
from suaylang.vm import VM

Termination = Literal["ok", "lex", "parse", "runtime", "internal", "timeout"]


@dataclass(frozen=True)
class Observation:
    termination: Termination
    stdout: str
    stderr: str
    value_repr: str | None = None
    error_type: str | None = None
    line: int | None = None
    column: int | None = None
    message: str | None = None
    elapsed_ms: float | None = None
    vm_steps: int | None = None


@contextlib.contextmanager
def _timeout(seconds: float):
    if seconds <= 0:
        yield
        return

    if os.name != "posix":
        # Best-effort on non-POSIX.
        yield
        return

    def handler(_signum, _frame):
        raise TimeoutError("timeout")

    old = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


_WS_RE = re.compile(r"\s+")


def _norm_text(s: str) -> str:
    return s.replace("\r\n", "\n")


def _norm_msg(s: str) -> str:
    return _WS_RE.sub(" ", s.strip())


def observe_interpreter(source: str, *, filename: str, timeout_s: float) -> Observation:
    out_buf = io.StringIO()
    err_buf = io.StringIO()
    t0 = time.perf_counter()

    def run() -> object:
        tokens = Lexer(source, filename=filename).tokenize()
        program = Parser(tokens, source, filename=filename).parse_program()
        return Interpreter(source=source, filename=filename, trace=False).eval_program(
            program
        )

    try:
        with (
            contextlib.redirect_stdout(out_buf),
            contextlib.redirect_stderr(err_buf),
            _timeout(timeout_s),
        ):
            val = run()
        t1 = time.perf_counter()
        return Observation(
            termination="ok",
            stdout=_norm_text(out_buf.getvalue()),
            stderr=_norm_text(err_buf.getvalue()),
            value_repr=repr(val),
            elapsed_ms=(t1 - t0) * 1000.0,
        )
    except TimeoutError:
        t1 = time.perf_counter()
        return Observation(
            termination="timeout",
            stdout=_norm_text(out_buf.getvalue()),
            stderr=_norm_text(err_buf.getvalue()),
            message="timeout",
            elapsed_ms=(t1 - t0) * 1000.0,
        )
    except BaseException as e:  # noqa: BLE001
        t1 = time.perf_counter()
        if isinstance(e, Diagnostic):
            term: Termination = "lex" if e.error_type == "lexical" else "parse"
            return Observation(
                termination=term,
                stdout=_norm_text(out_buf.getvalue()),
                stderr=_norm_text(err_buf.getvalue()),
                error_type=e.error_type,
                line=e.line,
                column=e.column,
                message=_norm_msg(e.message),
                elapsed_ms=(t1 - t0) * 1000.0,
            )
        if isinstance(e, SuayRuntimeError):
            line = e.span.start.line if e.span else None
            col = e.span.start.column if e.span else None
            return Observation(
                termination="runtime",
                stdout=_norm_text(out_buf.getvalue()),
                stderr=_norm_text(err_buf.getvalue()),
                error_type="runtime",
                line=line,
                column=col,
                message=_norm_msg(str(e)),
                elapsed_ms=(t1 - t0) * 1000.0,
            )
        if isinstance(e, SuayError):
            return Observation(
                termination="internal",
                stdout=_norm_text(out_buf.getvalue()),
                stderr=_norm_text(err_buf.getvalue()),
                error_type="suay",
                message=_norm_msg(str(e)),
                elapsed_ms=(t1 - t0) * 1000.0,
            )
        return Observation(
            termination="internal",
            stdout=_norm_text(out_buf.getvalue()),
            stderr=_norm_text(err_buf.getvalue()),
            error_type=type(e).__name__,
            message=_norm_msg(str(e)),
            elapsed_ms=(t1 - t0) * 1000.0,
        )


def observe_vm(source: str, *, filename: str, timeout_s: float) -> Observation:
    out_buf = io.StringIO()
    err_buf = io.StringIO()
    t0 = time.perf_counter()

    def run() -> object:
        tokens = Lexer(source, filename=filename).tokenize()
        program = Parser(tokens, source, filename=filename).parse_program()
        code = Compiler().compile_program(program, name=filename)
        vm = VM(source=source, filename=filename, trace=False)
        val, steps = vm.run_with_stats(code)
        return val, int(steps)

    try:
        with (
            contextlib.redirect_stdout(out_buf),
            contextlib.redirect_stderr(err_buf),
            _timeout(timeout_s),
        ):
            val, steps = run()
        t1 = time.perf_counter()
        return Observation(
            termination="ok",
            stdout=_norm_text(out_buf.getvalue()),
            stderr=_norm_text(err_buf.getvalue()),
            value_repr=repr(val),
            elapsed_ms=(t1 - t0) * 1000.0,
            vm_steps=int(steps),
        )
    except TimeoutError:
        t1 = time.perf_counter()
        return Observation(
            termination="timeout",
            stdout=_norm_text(out_buf.getvalue()),
            stderr=_norm_text(err_buf.getvalue()),
            message="timeout",
            elapsed_ms=(t1 - t0) * 1000.0,
        )
    except BaseException as e:  # noqa: BLE001
        t1 = time.perf_counter()
        if isinstance(e, Diagnostic):
            term: Termination = "lex" if e.error_type == "lexical" else "parse"
            return Observation(
                termination=term,
                stdout=_norm_text(out_buf.getvalue()),
                stderr=_norm_text(err_buf.getvalue()),
                error_type=e.error_type,
                line=e.line,
                column=e.column,
                message=_norm_msg(e.message),
                elapsed_ms=(t1 - t0) * 1000.0,
            )
        if isinstance(e, SuayRuntimeError):
            line = e.span.start.line if e.span else None
            col = e.span.start.column if e.span else None
            return Observation(
                termination="runtime",
                stdout=_norm_text(out_buf.getvalue()),
                stderr=_norm_text(err_buf.getvalue()),
                error_type="runtime",
                line=line,
                column=col,
                message=_norm_msg(str(e)),
                elapsed_ms=(t1 - t0) * 1000.0,
            )
        if isinstance(e, SuayError):
            return Observation(
                termination="internal",
                stdout=_norm_text(out_buf.getvalue()),
                stderr=_norm_text(err_buf.getvalue()),
                error_type="suay",
                message=_norm_msg(str(e)),
                elapsed_ms=(t1 - t0) * 1000.0,
            )
        return Observation(
            termination="internal",
            stdout=_norm_text(out_buf.getvalue()),
            stderr=_norm_text(err_buf.getvalue()),
            error_type=type(e).__name__,
            message=_norm_msg(str(e)),
            elapsed_ms=(t1 - t0) * 1000.0,
        )


def environment_metadata() -> dict[str, str]:
    return {
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
    }
