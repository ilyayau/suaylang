from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt


def _parse_results_table(md: str) -> list[dict[str, float | str]]:
    # Extract the first markdown table under "## Results".
    # Expected columns:
    # | Program | Interpreter (ms) | VM (ms) | Relative (interp/vm) | VM instr | Notes |
    lines = [ln.rstrip("\n") for ln in md.splitlines()]

    # Find header row.
    header_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("| Program |") and "Relative" in ln:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("Could not find microbench results table header in input markdown")

    # Find rows after separator (next line is |---|...|)
    i = header_idx + 2
    rows: list[dict[str, float | str]] = []

    def parse_cell(cell: str) -> str:
        return cell.strip()

    while i < len(lines):
        ln = lines[i].strip()
        if not ln.startswith("|"):
            break
        parts = [parse_cell(p) for p in ln.strip("|").split("|")]
        if len(parts) < 6:
            break
        program = parts[0]
        try:
            interp_ms = float(parts[1])
            vm_ms = float(parts[2])
            rel = float(parts[3])
            vm_instr = float(parts[4])
        except ValueError:
            i += 1
            continue
        rows.append(
            {
                "program": program,
                "interp_ms": interp_ms,
                "vm_ms": vm_ms,
                "relative": rel,
                "vm_instr": vm_instr,
            }
        )
        i += 1

    if not rows:
        raise ValueError("Parsed 0 rows from results table")
    return rows


def plot_relative(rows: list[dict[str, float | str]], out_path: Path) -> None:
    programs = [str(r["program"]) for r in rows]
    rel = [float(r["relative"]) for r in rows]

    out_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7.2, 3.2))
    xs = range(len(programs))
    plt.bar(xs, rel)
    plt.axhline(1.0, linewidth=1.0)
    plt.xticks(xs, programs, rotation=20, ha="right")
    plt.ylabel("Relative runtime (interp / vm)")
    plt.title("Microbench: Interpreter vs VM (relative)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in-md", required=True, help="Path to benchmarks/results.md")
    ap.add_argument("--out", required=True, help="Output image path (png)")
    args = ap.parse_args()

    in_path = Path(args.in_md)
    out_path = Path(args.out)

    md = in_path.read_text(encoding="utf-8")

    # Sanity: ensure this is the expected file
    if not re.search(r"#\s+Micro-benchmarks", md):
        raise ValueError("Input markdown does not look like benchmarks/results.md")

    rows = _parse_results_table(md)
    plot_relative(rows, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
