# Release process

This repository aims to follow Semantic Versioning.

## Versioning policy (0.x)

While the project is `0.x`, we apply SemVer with these constraints:

- Patch releases (`0.1.x`) must preserve **source compatibility** with the v0.1 grammar and preserve behavior for valid programs, except for explicitly unspecified formatting details.
- Minor releases (`0.2`, `0.3`, …) may introduce breaking changes, but must include migration notes.

The authoritative stability definition for v0.1 is [docs/LANGUAGE_CONTRACT_v0.1.md](docs/LANGUAGE_CONTRACT_v0.1.md).

## Preconditions

- Working tree clean.
- CI is green on `main`.
- Version updated in `pyproject.toml`.
- Changelog updated in `CHANGELOG.md`.

## Build and verify locally

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"

make check
python -m build

# Packaging metadata sanity
python -m twine check dist/*

# Coverage gate (same threshold as CI)
pytest -q --cov=suaylang --cov-report=term-missing --cov-fail-under=85

# Typing baseline
python -m mypy
```

## Tag

Tag must match the version, prefixed with `v`:

```sh
git tag v0.1.0
git push origin v0.1.0
```

## GitHub Release

Create a GitHub Release for the tag (manual or via workflow).

Release notes source of truth:

- Use `CHANGELOG.md` for the changelog entry.
- For a curated GitHub release body, start from the matching document in `docs/releases/`.

Attach the following artifacts:

- `dist/*.whl`
- `dist/*.tar.gz`

## Post-release

- Verify install from wheel in a fresh venv.
- Update the README if commands or requirements changed.
