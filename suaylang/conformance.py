from __future__ import annotations

import contextlib
import io
from dataclasses import dataclass
from typing import Literal

from .errors import Diagnostic, SuayError
from .compiler import Compiler
from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser
from .runtime import SuayRuntimeError
from .vm import VM

Termination = Literal["ok", "lex", "parse", "runtime", "internal"]


@dataclass(frozen=True)
class Observation:
    termination: Termination
    stdout: str
    value: object | None = None
    error_type: str | None = None
    line: int | None = None
    column: int | None = None


def _capture(fn) -> tuple[str, object | None, BaseException | None]:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            val = fn()
        return buf.getvalue(), val, None
    except BaseException as e:  # noqa: BLE001 - deliberate boundary
        return buf.getvalue(), None, e


def observe_interpreter(source: str, *, filename: str = "<conformance>") -> Observation:
    def run() -> object:
        tokens = Lexer(source, filename=filename).tokenize()
        program = Parser(tokens, source, filename=filename).parse_program()
        return Interpreter(source=source, filename=filename, trace=False).eval_program(
            program
        )

    out, val, err = _capture(run)
    if err is None:
        return Observation(termination="ok", stdout=out, value=val)

    if isinstance(err, Diagnostic):
        # LexError/ParseError are Diagnostics.
        term: Termination = "lex" if err.error_type == "lexical" else "parse"
        return Observation(
            termination=term,
            stdout=out,
            error_type=err.error_type,
            line=err.line,
            column=err.column,
        )

    if isinstance(err, SuayRuntimeError):
        line = err.span.start.line if err.span else None
        col = err.span.start.column if err.span else None
        return Observation(
            termination="runtime",
            stdout=out,
            error_type="runtime",
            line=line,
            column=col,
        )

    if isinstance(err, SuayError):
        return Observation(termination="internal", stdout=out, error_type="suay")

    return Observation(
        termination="internal", stdout=out, error_type=type(err).__name__
    )


def observe_vm(source: str, *, filename: str = "<conformance>") -> Observation:
    def run() -> object:
        tokens = Lexer(source, filename=filename).tokenize()
        program = Parser(tokens, source, filename=filename).parse_program()
        code = Compiler().compile_program(program, name=filename)
        return VM(source=source, filename=filename, trace=False).run(code)

    out, val, err = _capture(run)
    if err is None:
        return Observation(termination="ok", stdout=out, value=val)

    if isinstance(err, Diagnostic):
        term: Termination = "lex" if err.error_type == "lexical" else "parse"
        return Observation(
            termination=term,
            stdout=out,
            error_type=err.error_type,
            line=err.line,
            column=err.column,
        )

    if isinstance(err, SuayRuntimeError):
        line = err.span.start.line if err.span else None
        col = err.span.start.column if err.span else None
        return Observation(
            termination="runtime",
            stdout=out,
            error_type="runtime",
            line=line,
            column=col,
        )

    if isinstance(err, SuayError):
        return Observation(termination="internal", stdout=out, error_type="suay")

    return Observation(
        termination="internal", stdout=out, error_type=type(err).__name__
    )


@dataclass(frozen=True)
class ConformanceResult:
    ok: bool
    reason: str | None
    interp: Observation
    vm: Observation


def compare_observations(interp: Observation, vm: Observation) -> ConformanceResult:
    if interp.termination != vm.termination:
        return ConformanceResult(
            ok=False,
            reason=f"termination differs: interp={interp.termination} vm={vm.termination}",
            interp=interp,
            vm=vm,
        )

    if interp.stdout.replace("\r\n", "\n") != vm.stdout.replace("\r\n", "\n"):
        return ConformanceResult(
            ok=False,
            reason="stdout differs",
            interp=interp,
            vm=vm,
        )

    if interp.termination == "ok":
        # Best-effort structural equality. If values are not comparable, we accept.
        try:
            if interp.value != vm.value:
                return ConformanceResult(
                    ok=False,
                    reason=f"result differs: interp={interp.value!r} vm={vm.value!r}",
                    interp=interp,
                    vm=vm,
                )
        except Exception:
            pass
        return ConformanceResult(ok=True, reason=None, interp=interp, vm=vm)

    # For errors, compare coarse type and location.
    if interp.error_type != vm.error_type:
        return ConformanceResult(
            ok=False,
            reason=f"error type differs: interp={interp.error_type} vm={vm.error_type}",
            interp=interp,
            vm=vm,
        )

    if (interp.line, interp.column) != (vm.line, vm.column):
        return ConformanceResult(
            ok=False,
            reason=f"error location differs: interp={interp.line}:{interp.column} vm={vm.line}:{vm.column}",
            interp=interp,
            vm=vm,
        )

    return ConformanceResult(ok=True, reason=None, interp=interp, vm=vm)
