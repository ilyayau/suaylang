from __future__ import annotations

import argparse
import contextlib
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from suaylang.compiler import Compiler
from suaylang.contract import error_code
from suaylang.errors import Diagnostic, SuayError
from suaylang.interpreter import Interpreter
from suaylang.lexer import Lexer
from suaylang.parser import Parser
from suaylang.runtime import SuayRuntimeError
from suaylang.vm import VM

Backend = Literal["interp", "vm"]
Phase = Literal["ok", "lex", "parse", "runtime"]


@dataclass(frozen=True)
class RunResult:
    phase: Phase
    stdout: str
    snapshot: dict[str, object] | None


def _normalize_stdout(s: str) -> str:
    return s.replace("\r\n", "\n")


def _capture(fn) -> tuple[str, object | None, BaseException | None]:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            val = fn()
        return _normalize_stdout(buf.getvalue()), val, None
    except BaseException as e:  # noqa: BLE001 - deliberate boundary
        return _normalize_stdout(buf.getvalue()), None, e


def _run_interpreter(source: str, *, filename: str) -> RunResult:
    def run() -> object:
        tokens = Lexer(source, filename=filename).tokenize()
        program = Parser(tokens, source, filename=filename).parse_program()
        return Interpreter(source=source, filename=filename, trace=False).eval_program(program)

    out, _val, err = _capture(run)
    if err is None:
        return RunResult(phase="ok", stdout=out, snapshot=None)
    return RunResult(phase=_phase_of(err), stdout=out, snapshot=_snapshot_of(err))


def _run_vm(source: str, *, filename: str) -> RunResult:
    def run() -> object:
        tokens = Lexer(source, filename=filename).tokenize()
        program = Parser(tokens, source, filename=filename).parse_program()
        code = Compiler().compile_program(program, name=filename)
        return VM(source=source, filename=filename, trace=False).run(code)

    out, _val, err = _capture(run)
    if err is None:
        return RunResult(phase="ok", stdout=out, snapshot=None)
    return RunResult(phase=_phase_of(err), stdout=out, snapshot=_snapshot_of(err))


def _phase_of(err: BaseException) -> Phase:
    if isinstance(err, Diagnostic):
        return "lex" if err.error_type == "lexical" else "parse"
    if isinstance(err, SuayRuntimeError):
        return "runtime"
    if isinstance(err, SuayError):
        # Treat other SuayError variants as runtime for contract purposes.
        return "runtime"
    return "runtime"


def _snapshot_of(err: BaseException) -> dict[str, object]:
    code = error_code(err)

    if isinstance(err, Diagnostic):
        return {
            "phase": "lex" if err.error_type == "lexical" else "parse",
            "code": code,
            "line": err.line,
            "column": err.column,
        }

    if isinstance(err, SuayRuntimeError):
        line = err.span.start.line if err.span is not None else None
        column = err.span.start.column if err.span is not None else None
        return {
            "phase": "runtime",
            "code": code,
            "line": line,
            "column": column,
        }

    if isinstance(err, SuayError):
        return {
            "phase": "runtime",
            "code": code,
            "line": None,
            "column": None,
        }

    return {
        "phase": "runtime",
        "code": None,
        "line": None,
        "column": None,
    }


def _load_expected_err(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: dict[str, object]) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _case_kind(path: Path) -> Literal["ok", "err"]:
    name = path.name
    if name.startswith("ok_"):
        return "ok"
    if name.startswith("err_"):
        return "err"
    raise ValueError(
        f"Contract case must be named ok_* or err_*: {path.as_posix()}"
    )


def _run_backend(backend: Backend, source: str, *, filename: str) -> RunResult:
    if backend == "interp":
        return _run_interpreter(source, filename=filename)
    return _run_vm(source, filename=filename)


def _validate_err_snapshot(case: Path, snap: dict[str, object] | None) -> str | None:
    if snap is None:
        return "expected error, got ok"

    if not snap.get("code"):
        return "error has no stable code (update suaylang.contract.error_code)"

    if snap.get("line") is None or snap.get("column") is None:
        return "error has no span (line/column)"

    # Basic shape check.
    if snap.get("phase") not in {"lex", "parse", "runtime"}:
        return f"unexpected phase: {snap.get('phase')!r}"

    return None


def _determinism_check(backend: Backend, source: str, *, filename: str) -> str | None:
    r1 = _run_backend(backend, source, filename=filename)
    r2 = _run_backend(backend, source, filename=filename)
    if (r1.phase, r1.stdout, r1.snapshot) != (r2.phase, r2.stdout, r2.snapshot):
        return "nondeterministic result on repeated run"
    return None


def run_contract(
    *,
    cases_dir: Path,
    backend_mode: Literal["both", "interp", "vm"],
    update: bool,
    check_determinism: bool,
) -> int:
    repo_root = Path(__file__).resolve().parents[2]
    cases = sorted(p for p in cases_dir.glob("*.suay") if p.is_file())

    if not cases:
        print(f"No contract cases found in {cases_dir.as_posix()}")
        return 2

    total = 0
    failed = 0

    for case in cases:
        total += 1
        src = case.read_text(encoding="utf-8")
        display_name = str(case.relative_to(repo_root))
        kind = _case_kind(case)

        backends: list[Backend]
        if backend_mode == "interp":
            backends = ["interp"]
        elif backend_mode == "vm":
            backends = ["vm"]
        else:
            backends = ["interp", "vm"]

        results: dict[Backend, RunResult] = {}
        problems: list[str] = []

        for b in backends:
            r = _run_backend(b, src, filename=display_name)
            results[b] = r

            if check_determinism:
                det = _determinism_check(b, src, filename=display_name)
                if det is not None:
                    problems.append(f"{b}: {det}")

            if kind == "ok" and r.phase != "ok":
                problems.append(f"{b}: expected ok, got {r.phase} {r.snapshot}")
            if kind == "err":
                err_problem = _validate_err_snapshot(case, r.snapshot)
                if err_problem is not None:
                    problems.append(f"{b}: {err_problem} ({r.phase} {r.snapshot})")

        # Cross-backend agreement (if applicable).
        if len(backends) == 2:
            a = results["interp"]
            b = results["vm"]
            if (a.phase, a.stdout, a.snapshot) != (b.phase, b.stdout, b.snapshot):
                problems.append(
                    "interp/vm differ: "
                    f"interp=({a.phase}, {a.stdout!r}, {a.snapshot}) "
                    f"vm=({b.phase}, {b.stdout!r}, {b.snapshot})"
                )

        out_path = case.with_suffix(".out.txt")
        err_path = case.with_suffix(".err.json")

        if kind == "ok":
            if update:
                # Only write if execution actually succeeded.
                base = results[backends[0]]
                out_path.write_text(base.stdout, encoding="utf-8")
            else:
                if not out_path.exists():
                    problems.append(f"missing expected output snapshot: {out_path.name}")
                else:
                    expected_out = _normalize_stdout(out_path.read_text(encoding="utf-8"))
                    got_out = results[backends[0]].stdout
                    if got_out != expected_out:
                        problems.append(
                            f"stdout mismatch\nexpected:\n{expected_out!r}\ngot:\n{got_out!r}"
                        )

        if kind == "err":
            expected = results[backends[0]].snapshot or {}
            if update:
                _write_json(err_path, expected)
            else:
                if not err_path.exists():
                    problems.append(f"missing expected error snapshot: {err_path.name}")
                else:
                    got = results[backends[0]].snapshot
                    exp = _load_expected_err(err_path)
                    if got != exp:
                        problems.append(f"error snapshot mismatch expected={exp} got={got}")

        if problems:
            failed += 1
            print(f"FAIL {case.name}")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"OK   {case.name}")

    print(f"\nContract summary: {total - failed}/{total} ok")
    return 0 if failed == 0 else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Run the SuayLang v1 core contract corpus")
    p.add_argument(
        "--cases-dir",
        type=Path,
        default=Path("tests") / "contract",
        help="Directory containing *.suay contract cases",
    )
    p.add_argument(
        "--backend",
        choices=["both", "interp", "vm"],
        default="both",
        help="Which backend(s) to test",
    )
    p.add_argument(
        "--update",
        action="store_true",
        help="(Re)generate *.out.txt / *.err.json snapshots from current behavior",
    )
    p.add_argument(
        "--no-determinism-check",
        action="store_true",
        help="Skip running each case twice to enforce determinism",
    )

    args = p.parse_args(argv)
    return run_contract(
        cases_dir=args.cases_dir,
        backend_mode=args.backend,
        update=args.update,
        check_determinism=not args.no_determinism_check,
    )
