from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Case:
    path: str
    expected_stdout: str | None
    expect_success: bool
    must_contain: list[str]


def _run_case(case: Case) -> None:
    cmd = [sys.executable, "-m", "suaylang", "run", case.path]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[1],
    )

    out = (proc.stdout or "").replace("\r\n", "\n")
    err = (proc.stderr or "").replace("\r\n", "\n")
    combined = out + err

    if case.expect_success and proc.returncode != 0:
        raise AssertionError(
            f"Expected success but got exit={proc.returncode}\n"
            f"cmd={cmd}\n--- stdout ---\n{out}\n--- stderr ---\n{err}"
        )
    if (not case.expect_success) and proc.returncode == 0:
        raise AssertionError(
            f"Expected failure but got exit=0\ncmd={cmd}\n--- stdout ---\n{out}"
        )

    if case.expected_stdout is not None and out != case.expected_stdout:
        raise AssertionError(
            f"Unexpected stdout\ncmd={cmd}\n--- expected ---\n{case.expected_stdout}"
            f"\n--- actual ---\n{out}\n--- stderr ---\n{err}"
        )

    for needle in case.must_contain:
        if needle not in combined:
            raise AssertionError(
                f"Expected output to contain {needle!r}\ncmd={cmd}\n--- combined ---\n{combined}"
            )

    if "Traceback" in combined:
        raise AssertionError(
            f"Python traceback leaked to user output\ncmd={cmd}\n--- combined ---\n{combined}"
        )


def main() -> int:
    cases = [
        Case(
            path="examples/hello.suay",
            expected_stdout="total=30\n",
            expect_success=True,
            must_contain=[],
        ),
        Case(
            path="examples/committee_01_basic.suay",
            expected_stdout="square(7)=49\n",
            expect_success=True,
            must_contain=[],
        ),
        Case(
            path="examples/committee_02_dispatch.suay",
            expected_stdout="ok:41\nerr:bad\n",
            expect_success=True,
            must_contain=[],
        ),
        Case(
            path="examples/committee_03_cycle.suay",
            expected_stdout="sum_to(5)=15\n",
            expect_success=True,
            must_contain=[],
        ),
        Case(
            path="examples/committee_04_error.suay",
            expected_stdout=None,
            expect_success=False,
            must_contain=["runtime error"],
        ),
    ]

    for c in cases:
        _run_case(c)

    print("smoke:ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
