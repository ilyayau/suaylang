from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "suaylang", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )


def test_cli_reports_lex_error_without_traceback(tmp_path: Path) -> None:
    p = tmp_path / "bad.suay"
    p.write_text("@\n", encoding="utf-8")

    proc = run_cli(["run", str(p)])
    assert proc.returncode != 0
    combined = (proc.stdout or "") + (proc.stderr or "")
    assert "Traceback" not in combined
    assert "lex" in combined.lower() or "syntax" in combined.lower()


def test_cli_reports_parse_error_without_traceback(tmp_path: Path) -> None:
    p = tmp_path / "bad.suay"
    p.write_text("x ← (1 2\n", encoding="utf-8")

    proc = run_cli(["run", str(p)])
    assert proc.returncode != 0
    combined = (proc.stdout or "") + (proc.stderr or "")
    assert "Traceback" not in combined
    assert "syntax" in combined.lower()


def test_cli_reports_runtime_error_without_traceback(tmp_path: Path) -> None:
    p = tmp_path / "bad.suay"
    p.write_text("say · (text · not_defined)\n", encoding="utf-8")

    proc = run_cli(["run", str(p)])
    assert proc.returncode != 0
    combined = (proc.stdout or "") + (proc.stderr or "")
    assert "Traceback" not in combined
    assert "runtime error" in combined.lower()


def test_cli_check_succeeds_on_valid_program() -> None:
    proc = run_cli(["check", "examples/hello.suay"])
    assert proc.returncode == 0


def test_doctor_succeeds() -> None:
    proc = run_cli(["doctor"])
    assert proc.returncode == 0
    combined = (proc.stdout or "") + (proc.stderr or "")
    assert "doctor:ok" in combined


@pytest.mark.parametrize(
    "path",
    [
        "examples/committee_01_basic.suay",
        "examples/committee_02_dispatch.suay",
        "examples/committee_03_cycle.suay",
    ],
)
def test_examples_run_cleanly(path: str) -> None:
    proc = run_cli(["run", path])
    assert proc.returncode == 0
    combined = (proc.stdout or "") + (proc.stderr or "")
    assert "Traceback" not in combined
