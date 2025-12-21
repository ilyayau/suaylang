from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str | None = None
    stderr: str | None = None


def _run(argv: list[str]) -> CommandResult:
    proc = subprocess.run(argv, check=False)
    return CommandResult(argv=argv, returncode=proc.returncode)


def _run_capture(argv: list[str]) -> CommandResult:
    proc = subprocess.run(
        argv,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return CommandResult(
        argv=argv,
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def _git_commit() -> str | None:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except FileNotFoundError:
        return None

    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def _git_is_dirty() -> bool | None:
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except FileNotFoundError:
        return None
    if proc.returncode != 0:
        return None
    return bool(proc.stdout.strip())


def _cpu_model_linux() -> str | None:
    cpuinfo = Path("/proc/cpuinfo")
    if not cpuinfo.exists():
        return None
    try:
        for line in cpuinfo.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.lower().startswith("model name"):
                _, value = line.split(":", 1)
                return value.strip() or None
    except OSError:
        return None
    return None


def _environment_metadata() -> dict[str, Any]:
    cpu_model = _cpu_model_linux() or platform.processor() or None
    return {
        "git": {
            "commit": _git_commit(),
            "dirty": _git_is_dirty(),
        },
        "python": {
            "executable": sys.executable,
            "version": sys.version,
            "implementation": platform.python_implementation(),
        },
        "platform": {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "hardware": {
            "cpu": cpu_model,
        },
        "repro": {
            "source_date_epoch": os.environ.get("SOURCE_DATE_EPOCH"),
        },
    }


def _write_environment_reports(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = _environment_metadata()

    (out_dir / "environment.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    md_lines: list[str] = [
        "# Environment metadata",
        "",
        "Backed by raw JSON in `results/environment.json`.",
        "",
        f"- commit: `{meta['git']['commit']}`",
        f"- dirty: `{meta['git']['dirty']}`",
        f"- python: `{meta['python']['implementation']} {platform.python_version()}`",
        f"- platform: `{meta['platform']['platform']}`",
        f"- cpu: `{meta['hardware']['cpu']}`",
        "",
        "If `SOURCE_DATE_EPOCH` is set, it is recorded for reproducible builds.",
        "",
    ]
    (out_dir / "environment.md").write_text("\n".join(md_lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Regenerate research artifacts deterministically (program generation is seeded) "
            "and record environment metadata under results/."
        )
    )
    parser.add_argument("--out-dir", default="results")
    parser.add_argument("--diff-profile", default="ci")
    parser.add_argument("--bench-profile", default="smoke")
    parser.add_argument(
        "--golden",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Run golden diagnostics tests and write results/golden_diagnostics.*",
    )
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir)
    _write_environment_reports(out_dir)

    results: list[CommandResult] = []

    results.append(
        _run(
            [
                sys.executable,
                "-m",
                "tools.diff_test.main",
                "--profile",
                args.diff_profile,
                "--out-dir",
                str(out_dir),
            ]
        )
    )
    results.append(
        _run(
            [
                sys.executable,
                str(Path("benchmarks") / "benchmark_runner.py"),
                "--profile",
                args.bench_profile,
                "--out-dir",
                str(out_dir),
            ]
        )
    )

    if args.golden:
        golden = _run_capture(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "tests/test_golden_diagnostics.py",
                "tests/test_golden_error_codes.py",
            ]
        )
        results.append(golden)

        golden_payload = {
            "argv": golden.argv,
            "returncode": golden.returncode,
            "stdout": golden.stdout,
            "stderr": golden.stderr,
        }
        (out_dir / "golden_diagnostics.json").write_text(
            json.dumps(golden_payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        md = [
            "# Golden diagnostics report",
            "",
            "Backed by raw JSON in `results/golden_diagnostics.json`.",
            "",
            f"- returncode: `{golden.returncode}`",
            "- argv:",
            "  - `" + " `\n  - `".join(golden.argv) + "`",
            "",
        ]
        if golden.stdout:
            md.extend(["## stdout", "", "```", golden.stdout.rstrip(), "```", ""])
        if golden.stderr:
            md.extend(["## stderr", "", "```", golden.stderr.rstrip(), "```", ""])
        (out_dir / "golden_diagnostics.md").write_text("\n".join(md), encoding="utf-8")

    failing = [r for r in results if r.returncode != 0]
    if failing:
        for r in failing:
            print(f"FAILED: {r.returncode}: {' '.join(r.argv)}", file=sys.stderr)
        return failing[0].returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
