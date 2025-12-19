from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TASK_ROOT = _REPO_ROOT / "evaluation" / "human_proxy"


@dataclass(frozen=True)
class Metrics:
    loc_nonempty: int
    token_count: int
    max_nesting: int
    control_flow_markers: int
    operator_diversity: int


_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*|\d+\.\d+|\d+|\"(?:\\.|[^\"])*\"|\S")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _loc_nonempty(src: str) -> int:
    return sum(1 for ln in src.splitlines() if ln.strip())


def _token_count(src: str) -> int:
    return len(_TOKEN_RE.findall(src))


def _max_nesting(src: str) -> int:
    # Delimiter-based proxy: counts nesting of (), {}, [] and Suay map delimiters [[ ]].
    depth = 0
    maxd = 0
    i = 0
    while i < len(src):
        ch = src[i]
        two = src[i : i + 2]
        if two == "[[":
            depth += 1
            maxd = max(maxd, depth)
            i += 2
            continue
        if two == "]]":
            depth = max(0, depth - 1)
            i += 2
            continue
        if ch in "([{":
            depth += 1
            maxd = max(maxd, depth)
        elif ch in ")]}":
            depth = max(0, depth - 1)
        i += 1
    return maxd


def _metrics_suay(src: str) -> Metrics:
    ops = ["<-", "<~", "|>", "~~", "=>", ".", "::", "++", "+", "-", "*", "/", "&&", "||", "!=", "<=", ">=", "="]
    present = {op for op in ops if op in src}
    control = src.count("|>") + src.count("~~")
    return Metrics(
        loc_nonempty=_loc_nonempty(src),
        token_count=_token_count(src),
        max_nesting=_max_nesting(src),
        control_flow_markers=int(control),
        operator_diversity=len(present),
    )


def _metrics_python(src: str) -> Metrics:
    # Control-flow markers are keyword occurrences.
    keywords = ["if", "elif", "else", "for", "while", "match", "case", "try", "except"]
    control = 0
    for kw in keywords:
        control += len(re.findall(rf"\b{re.escape(kw)}\b", src))

    # Operator diversity is a small set of common syntax markers.
    ops = ["=", "+", "-", "*", "/", "==", "!=", "<=", ">=", ":", "def", "return", "lambda"]
    present = set()
    for op in ops:
        if op in src:
            present.add(op)

    return Metrics(
        loc_nonempty=_loc_nonempty(src),
        token_count=_token_count(src),
        max_nesting=_max_nesting(src),
        control_flow_markers=int(control),
        operator_diversity=len(present),
    )


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=_REPO_ROOT, text=True).strip()
    except Exception:
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(prog="human-proxy", description="Run proxy human-facing experiment (static metrics).")
    ap.add_argument("--out-dir", type=str, default=str(_REPO_ROOT / "results"))
    args = ap.parse_args()

    pairs: dict[str, dict[str, Path]] = {}
    for p in sorted(_TASK_ROOT.iterdir()):
        if not p.is_file():
            continue
        stem = p.stem
        task = stem
        if stem.endswith(".suay") or stem.endswith(".py"):
            # defensive; should not happen
            task = Path(stem).stem
        task = p.stem

    for p in sorted(_TASK_ROOT.glob("*.suay")):
        task = p.stem
        pairs.setdefault(task, {})["suay"] = p
    for p in sorted(_TASK_ROOT.glob("*.py")):
        task = p.stem
        pairs.setdefault(task, {})["python"] = p

    tasks = sorted(t for t, d in pairs.items() if "suay" in d and "python" in d)
    if not tasks:
        print("human-proxy: no task pairs found under evaluation/human_proxy")
        return 2

    out_dir = Path(str(args.out_dir))
    csv_path = out_dir / "human_study.csv"
    md_path = out_dir / "human_study.md"

    rows: list[dict[str, object]] = []
    for task in tasks:
        suay_src = _read(pairs[task]["suay"])
        py_src = _read(pairs[task]["python"])
        ms = _metrics_suay(suay_src)
        mp = _metrics_python(py_src)

        rows.append({"task": task, "language": "suay", **ms.__dict__})
        rows.append({"task": task, "language": "python", **mp.__dict__})

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "task",
                "language",
                "loc_nonempty",
                "token_count",
                "max_nesting",
                "control_flow_markers",
                "operator_diversity",
            ],
        )
        w.writeheader()
        for r in rows:
            w.writerow(r)

    md: list[str] = []
    md.append("# Human-facing experiment (proxy) — results")
    md.append("")
    md.append("This is a proxy protocol with computed static metrics (not a real participant study).")
    md.append("")
    md.append(f"- commit: `{_git_commit()}`")
    md.append(f"- python: `{sys.version.split()[0]}`")
    md.append("")
    md.append("## Task-by-task comparison")
    md.append("")
    md.append("| task | metric | suay | python |")
    md.append("|---|---|---:|---:|")

    # Summarize: per task, compare key metrics.
    for task in tasks:
        r_s = next(r for r in rows if r["task"] == task and r["language"] == "suay")
        r_p = next(r for r in rows if r["task"] == task and r["language"] == "python")
        for metric in ["loc_nonempty", "token_count", "control_flow_markers", "max_nesting"]:
            md.append(f"| {task} | {metric} | {r_s[metric]} | {r_p[metric]} |")

    md.append("")
    md.append("## Interpretation (5–10 lines)")
    md.append("")
    md.append("Across these micro-tasks, SuayLang often shifts branching/looping into expression forms (`dispatch`/`cycle`).")
    md.append("The proxy is considered supportive when SuayLang achieves comparable or lower token count and control-flow markers without increasing nesting depth.")
    md.append("This does not establish human comprehension; it provides a reproducible, reviewable signal and a concrete task set to recruit participants against later.")
    md.append("")
    md.append("Threats to validity: tokenization is approximate; Python idioms vary; static counts do not model reader time/correctness.")

    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")

    print(f"human-proxy: wrote {csv_path} and {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
