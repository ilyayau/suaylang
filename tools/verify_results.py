from __future__ import annotations

import hashlib
import json
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256-" + h.hexdigest()


def main() -> int:
    manifest_path = _REPO_ROOT / "results" / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit("verify-results: missing results/manifest.json (run `make manifest`)")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        raise SystemExit("verify-results: manifest.artifacts missing or not an object")

    errors: list[str] = []
    checked = 0

    for rel, expected in sorted(artifacts.items()):
        if not isinstance(rel, str) or not isinstance(expected, str):
            errors.append(f"invalid entry: {rel!r} -> {expected!r}")
            continue
        p = (_REPO_ROOT / rel).resolve()
        try:
            p.relative_to(_REPO_ROOT.resolve())
        except Exception:
            errors.append(f"path escapes repo root: {rel}")
            continue
        if not p.exists():
            errors.append(f"missing: {rel}")
            continue
        if not p.is_file():
            errors.append(f"not a file: {rel}")
            continue

        actual = _sha256(p)
        if actual != expected:
            errors.append(f"hash mismatch: {rel} expected {expected} got {actual}")
        checked += 1

    if errors:
        msg = "\n".join(errors[:50])
        raise SystemExit(f"verify-results: FAILED ({len(errors)} errors)\n{msg}")

    print(f"verify-results: OK ({checked} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
