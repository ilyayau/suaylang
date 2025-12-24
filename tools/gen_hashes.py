from __future__ import annotations

import hashlib
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _rel(path: Path) -> str:
    return path.resolve().relative_to(_REPO_ROOT.resolve()).as_posix()


def main() -> int:
    candidates: list[Path] = []

    # Core evidence artifacts.
    candidates += [
        _REPO_ROOT / "README.md",
        _REPO_ROOT / "docs" / "COMMITTEE_ONEPAGER.md",
        _REPO_ROOT / "docs" / "REPRODUCIBILITY.md",
        _REPO_ROOT / "docs" / "OBSERVATION_POLICY.md",
        _REPO_ROOT / "docs" / "THREATS_TO_VALIDITY.md",
        _REPO_ROOT / "docs" / "LIMITATIONS.md",
        _REPO_ROOT / "docs" / "CLAIM_EVIDENCE_MATRIX.md",
        _REPO_ROOT / "results" / "README.md",
    ]

    # Results artifacts (if present).
    results_dir = _REPO_ROOT / "results"
    if results_dir.exists():
        for p in sorted(results_dir.glob("*.md")):
            candidates.append(p)
        for p in sorted(results_dir.glob("*.json")):
            candidates.append(p)
        for p in sorted((results_dir / "img").glob("*.png")) if (results_dir / "img").exists() else []:
            candidates.append(p)

    # Pre-rendered diagrams / plots.
    for p in sorted((_REPO_ROOT / "docs" / "diagrams").glob("*.svg")) if (_REPO_ROOT / "docs" / "diagrams").exists() else []:
        candidates.append(p)
    for p in sorted((_REPO_ROOT / "docs" / "plots").glob("*.png")) if (_REPO_ROOT / "docs" / "plots").exists() else []:
        candidates.append(p)

    # Deduplicate and keep existing only.
    uniq: dict[str, Path] = {}
    for p in candidates:
        if p.exists():
            uniq[str(p.resolve())] = p

    out_path = _REPO_ROOT / "results" / "hashes.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    for p in sorted(uniq.values(), key=lambda x: _rel(x)):
        lines.append(f"{_sha256(p)}  {_rel(p)}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
