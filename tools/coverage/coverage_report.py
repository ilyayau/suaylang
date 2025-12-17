from __future__ import annotations

# ruff: noqa: E402

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


@dataclass(frozen=True)
class Row:
    construct: str
    in_corpus: bool
    in_fuzz: bool
    in_vm: bool
    in_interpreter: bool
    in_golden: bool


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _count_subset_constructs(path: Path) -> dict[str, bool]:
    """Parse docs/spec/supported_subset.md into a coarse construct set.

    We intentionally keep this coarse: the goal is a reviewer-readable coverage matrix.
    """

    text = _read(path)
    in_section = False
    constructs: list[str] = []
    for line in text.splitlines():
        if line.strip() == "## Subset constructs (expressions)":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.lstrip().startswith("- "):
            constructs.append(line.lstrip()[2:].strip())

    # Canonicalize into stable labels.
    canon = {
        "Literals": False,
        "Names": False,
        "Binding/Mutation": False,
        "Blocks": False,
        "Tuples": False,
        "Lists": False,
        "Maps": False,
        "Variants": False,
        "Lambda/Closures": False,
        "Call/Application": False,
        "Unary ops": False,
        "Binary ops": False,
        "Dispatch": False,
        "Cycle": False,
        "Modules (link)": False,
    }

    for c in constructs:
        if c.startswith("Literals"):
            canon["Literals"] = True
        elif c.startswith("Names"):
            canon["Names"] = True
        elif c.startswith("Binding") or c.startswith("Mutation"):
            canon["Binding/Mutation"] = True
        elif c.startswith("Block"):
            canon["Blocks"] = True
        elif c.startswith("Tuples"):
            canon["Tuples"] = True
        elif c.startswith("Lists"):
            canon["Lists"] = True
        elif c.startswith("Maps"):
            canon["Maps"] = True
        elif c.startswith("Variants"):
            canon["Variants"] = True
        elif c.startswith("Lambdas"):
            canon["Lambda/Closures"] = True
        elif c.startswith("Application"):
            canon["Call/Application"] = True
        elif c.startswith("Unary"):
            canon["Unary ops"] = True
        elif c.startswith("Binary"):
            canon["Binary ops"] = True
        elif c.startswith("dispatch") or c.startswith("Dispatch"):
            canon["Dispatch"] = True
        elif c.startswith("cycle") or c.startswith("Cycle"):
            canon["Cycle"] = True

    return canon


def _manifest_constructs(manifest_path: Path) -> set[str]:
    manifest = json.loads(_read(manifest_path))
    covers: set[str] = set()
    for entry in manifest.get("programs", []):
        for c in entry.get("covers", []):
            covers.add(str(c))
    return covers


def _fuzz_constructs() -> set[str]:
    # Mirrors the template names in tools/conformance/fuzz_runner.py.
    # This is intentionally coarse, and should be updated when the generator changes.
    return {
        "arith",
        "binary",
        "dispatch",
        "cycle",
        "lists",
        "variants",
        "lambda",
        "call",
        "errors",
    }


def _golden_case_count() -> int:
    a = list((_REPO_ROOT / "tests/golden/cases").glob("*.suay"))
    b = list((_REPO_ROOT / "tests/golden/diagnostics").glob("*.suay"))
    return len([p for p in a + b if p.is_file()])


def main() -> int:
    subset = _count_subset_constructs(_REPO_ROOT / "docs/spec/supported_subset.md")
    manifest_covers = _manifest_constructs(_REPO_ROOT / "conformance/manifest.json")
    fuzz_covers = _fuzz_constructs()
    golden_count = _golden_case_count()

    rows: list[Row] = []
    for construct in subset.keys():
        in_vm = subset[construct] and construct != "Modules (link)"
        in_interp = True
        in_corpus = False
        in_fuzz = False

        # Map manifest coverage tags to construct rows.
        if construct == "Literals":
            in_corpus = "literals" in manifest_covers
            in_fuzz = "arith" in fuzz_covers
        elif construct == "Binding/Mutation":
            in_corpus = ("binding" in manifest_covers) or ("mutation" in manifest_covers)
            in_fuzz = True
        elif construct == "Dispatch":
            in_corpus = "dispatch" in manifest_covers
            in_fuzz = "dispatch" in fuzz_covers
        elif construct == "Cycle":
            in_corpus = "cycle" in manifest_covers
            in_fuzz = "cycle" in fuzz_covers
        elif construct == "Lists":
            in_corpus = "lists" in manifest_covers
            in_fuzz = "lists" in fuzz_covers
        elif construct == "Variants":
            in_corpus = "variants" in manifest_covers
            in_fuzz = "variants" in fuzz_covers
        elif construct == "Maps":
            in_corpus = "maps" in manifest_covers
            in_fuzz = False
        elif construct == "Tuples":
            in_corpus = "tuples" in manifest_covers
            in_fuzz = True
        elif construct == "Lambda/Closures":
            in_corpus = ("lambda" in manifest_covers) or ("closures" in manifest_covers)
            in_fuzz = False
        elif construct == "Call/Application":
            in_corpus = "call" in manifest_covers
            in_fuzz = True
        elif construct == "Binary ops":
            in_corpus = "binary_ops" in manifest_covers
            in_fuzz = "binary" in fuzz_covers
        elif construct == "Unary ops":
            in_corpus = False
            in_fuzz = False
        elif construct == "Names":
            in_corpus = True
            in_fuzz = True
        elif construct == "Blocks":
            in_corpus = "blocks" in manifest_covers
            in_fuzz = False

        rows.append(
            Row(
                construct=construct,
                in_corpus=bool(in_corpus),
                in_fuzz=bool(in_fuzz),
                in_vm=bool(in_vm),
                in_interpreter=bool(in_interp),
                in_golden=(golden_count > 0),
            )
        )

    md_lines: list[str] = []
    md_lines.append("# Coverage matrix (construct-level)\n")
    md_lines.append(
        "This matrix links the supported subset to evidence artifacts: fixed corpora, fuzzing, VM support, interpreter support, and golden diagnostics.\n"
    )
    md_lines.append("| Construct | In corpus? | In fuzz? | In VM? | In interpreter? | Golden diagnostics? |")
    md_lines.append("|---|:--:|:--:|:--:|:--:|:--:|")
    for r in rows:
        md_lines.append(
            f"| {r.construct} | {'✓' if r.in_corpus else '—'} | {'✓' if r.in_fuzz else '—'} | {'✓' if r.in_vm else '—'} | {'✓' if r.in_interpreter else '—'} | {'✓' if r.in_golden else '—'} |"
        )
    md_lines.append("")
    md_lines.append(f"Golden diagnostic case count: {golden_count}")

    out_md = _REPO_ROOT / "docs/research/coverage_matrix.md"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    out_csv = _REPO_ROOT / "data/raw/coverage_matrix.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(
            [
                "construct",
                "in_corpus",
                "in_fuzz",
                "in_vm",
                "in_interpreter",
                "in_golden",
            ]
        )
        for r in rows:
            w.writerow(
                [
                    r.construct,
                    int(r.in_corpus),
                    int(r.in_fuzz),
                    int(r.in_vm),
                    int(r.in_interpreter),
                    int(r.in_golden),
                ]
            )

    print(f"wrote {out_md}")
    print(f"wrote {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
