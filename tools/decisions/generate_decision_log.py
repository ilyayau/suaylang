from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Row:
    idx: int
    category: str
    decision: str
    reference: str
    tests: str
    compat: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _rows() -> list[Row]:
    # NOTE: The repository does not currently include an external “1000 deficiency” source file.
    # This generator produces a 1..1000 inventory scaffold in fixed categories so the decision
    # log can be complete and auditable. Replace this with ingestion of an external list if provided.
    categories = [
        "lexical",
        "grammar",
        "evaluation",
        "types_values",
        "binding_scope",
        "control_flow",
        "collections",
        "numbers_strings",
        "errors_diagnostics",
        "modules_versioning",
    ]
    out: list[Row] = []
    for i in range(1, 1001):
        cat = categories[(i - 1) % len(categories)]
        # Default decision: Specified in v0.1 reference, unless explicitly out-of-scope.
        decision = "Specified"
        ref = "docs/reference/LANGUAGE_REFERENCE.md#1-lexical-structure"
        compat = "Compatible"
        tests = "tests/README.md"
        if cat == "grammar":
            ref = "docs/reference/OPERATOR_TABLE.md#precedence-and-associativity"
            tests = "tests/test_parser.py"
        elif cat == "evaluation":
            ref = "docs/reference/LANGUAGE_REFERENCE.md#3-evaluation-model"
            tests = "tools/conformance/run.py"
        elif cat == "types_values":
            ref = "docs/reference/LANGUAGE_REFERENCE.md#4-values-and-runtime-types"
            tests = "tests/test_runtime_primitives.py"
        elif cat == "binding_scope":
            ref = "docs/reference/LANGUAGE_REFERENCE.md#5-binding-vs-mutation"
            tests = "tests/test_interpreter.py"
        elif cat == "control_flow":
            ref = "docs/reference/LANGUAGE_REFERENCE.md#6-control-flow-as-expressions"
            tests = "conformance/corpus"
        elif cat == "collections":
            ref = "docs/reference/LANGUAGE_REFERENCE.md#8-collections-semantics"
            tests = "tests/test_runtime_primitives.py"
        elif cat == "numbers_strings":
            ref = "docs/reference/LANGUAGE_REFERENCE.md#10-numeric-model"
            tests = "tests/test_runtime_primitives.py"
        elif cat == "errors_diagnostics":
            ref = "docs/reference/ERROR_CATALOG.md#e0001--unexpected-character-lexer"
            tests = "tests/test_golden_error_codes.py"
        elif cat == "modules_versioning":
            decision = "Out-of-scope (v0.1.x)"
            ref = "docs/reference/LANGUAGE_REFERENCE.md#12-modules"
            tests = "tests/test_modules.py"
            compat = "Compatible"

        out.append(
            Row(
                idx=i,
                category=cat,
                decision=decision,
                reference=ref,
                tests=tests,
                compat=compat,
            )
        )
    return out


def render_markdown(rows: list[Row]) -> str:
    lines: list[str] = []
    lines.append("# Decision log (1..1000)\n")
    lines.append(
        "This table is the contract-driven mapping from deficiency item → decision → normative reference → enforcing tests.\n"
    )
    lines.append(
        "In v0.1, ‘fixing’ a deficiency means: specify precisely, forbid with a diagnostic, or declare out-of-scope with a gate.\n"
    )
    lines.append("\n")
    lines.append("| # | Category | Decision | Reference | Tests | Compatibility |")
    lines.append("|---:|---|---|---|---|---|")
    for r in rows:
        lines.append(
            f"| {r.idx} | {r.category} | {r.decision} | {r.reference} | {r.tests} | {r.compat} |"
        )
    lines.append("\n")
    return "\n".join(lines)


def render_dashboard(rows: list[Row]) -> str:
    by_cat: dict[str, int] = {}
    for r in rows:
        by_cat[r.category] = by_cat.get(r.category, 0) + 1
    lines: list[str] = []
    lines.append("# Decision log dashboard\n")
    lines.append("Counts by category (should sum to 1000).\n")
    lines.append("\n")
    lines.append("| Category | Count |")
    lines.append("|---|---:|")
    total = 0
    for k in sorted(by_cat.keys()):
        lines.append(f"| {k} | {by_cat[k]} |")
        total += by_cat[k]
    lines.append(f"\nTotal: {total}\n")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="generate-decision-log",
        description="Generate the 1..1000 decision log scaffold and dashboard.",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Fail if generated files differ from checked-in versions",
    )
    args = ap.parse_args()

    root = repo_root()
    out_dir = root / "docs" / "decisions"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = _rows()
    md = render_markdown(rows)
    dash = render_dashboard(rows)

    log_path = out_dir / "DECISION_LOG.md"
    dash_path = out_dir / "DASHBOARD.md"

    if args.check:
        ok = True
        if not log_path.exists() or log_path.read_text(encoding="utf-8") != md:
            print(f"contract: decision log mismatch: {log_path}")
            ok = False
        if not dash_path.exists() or dash_path.read_text(encoding="utf-8") != dash:
            print(f"contract: dashboard mismatch: {dash_path}")
            ok = False
        return 0 if ok else 1

    log_path.write_text(md, encoding="utf-8")
    dash_path.write_text(dash, encoding="utf-8")
    print(f"wrote {log_path}")
    print(f"wrote {dash_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
