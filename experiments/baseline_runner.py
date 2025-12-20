"""
baseline_runner.py: Runs the baseline suite for SuayLang and Python, collects metrics, and writes results.

- Discovers all .suay/.py pairs in baseline_suite/
- Runs each .py with Python, each .suay with the SuayLang interpreter and VM
- Measures runtime (median of N runs), compile time (if applicable), bytecode size (if applicable)
- Captures diagnostics (error output, if any)
- Collects environment metadata (Python version, OS, CPU, commit hash)
- Writes results to results/baseline_raw.json and results/baseline.md (table)

Usage: python experiments/baseline_runner.py
"""
import os
import sys
import time
import json
import platform
import subprocess
from statistics import median
from pathlib import Path

# Config
BASELINE_SUITE = Path(__file__).parent.parent / "baseline_suite"
RESULTS_DIR = Path(__file__).parent.parent / "results"
N_RUNS = 5
SUAY_INTERPRETER = "suay"  # Assumed in PATH
SUAY_VM = "suay-vm"        # Assumed in PATH

# Utility: get commit hash
def get_commit_hash():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=Path(__file__).parent.parent).decode().strip()
    except Exception:
        return None

def get_env_metadata():
    return {
        "python_version": platform.python_version(),
        "os": platform.platform(),
        "cpu": platform.processor(),
        "commit_hash": get_commit_hash(),
    }

def run_python(file):
    times = []
    for _ in range(N_RUNS):
        start = time.perf_counter()
        proc = subprocess.run([sys.executable, str(file)], capture_output=True, text=True)
        end = time.perf_counter()
        times.append(end - start)
    return {
        "median_runtime": median(times),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "exit_code": proc.returncode,
    }

def run_suay(file, mode):
    # mode: "interpreter" or "vm"
    exe = SUAY_INTERPRETER if mode == "interpreter" else SUAY_VM
    times = []
    for _ in range(N_RUNS):
        start = time.perf_counter()
        proc = subprocess.run([exe, str(file)], capture_output=True, text=True)
        end = time.perf_counter()
        times.append(end - start)
    return {
        "median_runtime": median(times),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "exit_code": proc.returncode,
    }

def main():
    results = {"env": get_env_metadata(), "benchmarks": []}
    for suay_file in sorted(BASELINE_SUITE.glob("*.suay")):
        base = suay_file.stem
        py_file = BASELINE_SUITE / f"{base}.py"
        entry = {"name": base}
        if py_file.exists():
            entry["python"] = run_python(py_file)
        else:
            entry["python"] = None
        entry["suay_interpreter"] = run_suay(suay_file, "interpreter")
        entry["suay_vm"] = run_suay(suay_file, "vm")
        results["benchmarks"].append(entry)
    # Write JSON
    RESULTS_DIR.mkdir(exist_ok=True)
    with open(RESULTS_DIR / "baseline_raw.json", "w") as f:
        json.dump(results, f, indent=2)
    # Write Markdown table
    with open(RESULTS_DIR / "baseline.md", "w") as f:
        f.write("| Name | Python (s) | SuayInterp (s) | SuayVM (s) |\n")
        f.write("|------|------------|---------------|-----------|\n")
        for b in results["benchmarks"]:
            py = b["python"]["median_runtime"] if b["python"] else "-"
            interp = b["suay_interpreter"]["median_runtime"]
            vm = b["suay_vm"]["median_runtime"]
            f.write(f"| {b['name']} | {py} | {interp} | {vm} |\n")
    print("Baseline results written to results/baseline_raw.json and results/baseline.md")

if __name__ == "__main__":
    main()
