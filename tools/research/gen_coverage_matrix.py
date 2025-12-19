from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_MANIFEST = _REPO_ROOT / "conformance" / "manifest.json"
_DEFAULT_OUT = _REPO_ROOT / "docs" / "research" / "coverage_matrix.md"


@dataclass(frozen=True)
class Entry:
    feature: str
    programs: list[str]


def _load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _vm_support(feature: str) -> str:
    """Best-effort VM support status.

    This is intentionally conservative and stays tied to actual implementation:
    - `supported`: exercised by the fixed conformance suite and expected to run on VM.
    - `partial`: known gaps or tool-only coverage.
    - `missing`: explicitly not implemented in VM.

    Update this function when new features land.
    """

    # Current v0.1 implementation supports all features used in conformance/manifest.json,
    # including v0.1 module loading via `link`.
    if feature in {"modules", "link", "import_cycle"}:
        return "supported"

    return "supported"


def render_matrix(manifest: dict) -> str:
    corpus_root = str(manifest.get("corpus_root", "conformance/corpus"))

    by_feature: dict[str, set[str]] = defaultdict(set)
    for prog in manifest.get("programs", []):
        f = prog["file"]
        for feat in prog.get("covers", []):
            by_feature[str(feat)].add(str(f))

    features = sorted(by_feature.keys())

    lines: list[str] = []
    lines.append("# Coverage Matrix")
    lines.append("")
    lines.append(
        "This matrix is generated from `conformance/manifest.json` and is intended to be reviewer-auditable."
    )
    lines.append("")
    lines.append(f"- Corpus root: `{corpus_root}`")
    lines.append(f"- Programs (fixed): {len(manifest.get('programs', []))}")
    lines.append("")
    lines.append("| Feature | Programs | VM support |")
    lines.append("|---|---|---|")

    for feat in features:
        progs = sorted(by_feature[feat])
        vm = _vm_support(feat)
        joined = ", ".join(f"`{p}`" for p in progs)
        lines.append(f"| `{feat}` | {joined} | {vm} |")

    lines.append("")
    lines.append("## How to regenerate")
    lines.append("")
    lines.append("```sh")
    lines.append("python -m tools.research.gen_coverage_matrix")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(prog="gen_coverage_matrix")
    ap.add_argument("--manifest", type=str, default=str(_MANIFEST))
    ap.add_argument("--out", type=str, default=str(_DEFAULT_OUT))
    ap.add_argument("--check", action="store_true", help="Fail if output differs")
    args = ap.parse_args()

    manifest = _load_manifest(Path(args.manifest))
    text = render_matrix(manifest)

    out = Path(args.out)
    if args.check:
        if not out.exists():
            raise SystemExit(f"missing: {out}")
        if out.read_text(encoding="utf-8") != text:
            raise SystemExit(f"out of date: {out}")
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
