from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[1]


def _sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256-" + h.hexdigest()


def _rel(path: Path) -> str:
    return path.resolve().relative_to(_REPO_ROOT.resolve()).as_posix()


def _git_commit() -> str:
    try:
        return os.popen("git rev-parse HEAD").read().strip()
    except Exception:
        return "unknown"


def main() -> int:
    manifest: dict[str, object] = {
        "commit": _git_commit(),
        "artifacts": {},
        "python_version": sys.version.replace("\n", " ").strip(),
        "os": os.popen("uname -a").read().strip(),
    }

    candidates: list[Path] = []

    # Always include these reviewer-facing anchors if present.
    candidates += [
        _REPO_ROOT / "README.md",
        _REPO_ROOT / "docs" / "REVIEWER_PORTAL.md",
        _REPO_ROOT / "docs" / "COMMITTEE_ONEPAGER.md",
        _REPO_ROOT / "docs" / "EVIDENCE_MAP.md",
        _REPO_ROOT / "docs" / "evidence_map.json",
        _REPO_ROOT / "results" / "README.md",
        _REPO_ROOT / "results" / "baseline.md",
        _REPO_ROOT / "results" / "baseline_raw.json",
    ]

    # Whole results tree (excluding giant raw inputs by default).
    results_dir = _REPO_ROOT / "results"
    if results_dir.exists():
        for p in sorted(results_dir.rglob("*")):
            if not p.is_file():
                continue
            rel = _rel(p)
            if rel in {"results/manifest.json", "results/hashes.txt"}:
                continue
            candidates.append(p)

    # Pre-rendered plots and diagrams for README rendering.
    for p in sorted((_REPO_ROOT / "docs" / "plots").glob("*.png")) if (_REPO_ROOT / "docs" / "plots").exists() else []:
        candidates.append(p)
    for p in sorted((_REPO_ROOT / "docs" / "diagrams").glob("*.svg")) if (_REPO_ROOT / "docs" / "diagrams").exists() else []:
        candidates.append(p)
    for p in sorted((_REPO_ROOT / "docs" / "diagrams" / "ascii").glob("*.txt")) if (_REPO_ROOT / "docs" / "diagrams" / "ascii").exists() else []:
        candidates.append(p)

    uniq: dict[str, Path] = {}
    for p in candidates:
        if p.exists() and p.is_file():
            uniq[str(p.resolve())] = p

    artifacts: dict[str, str] = {}
    for p in sorted(uniq.values(), key=_rel):
        artifacts[_rel(p)] = _sha256sum(p)
    manifest["artifacts"] = artifacts

    out_path = _REPO_ROOT / "results" / "manifest.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
