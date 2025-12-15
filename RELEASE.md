# Release process

This repository aims to follow Semantic Versioning.

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
```

## Tag

Tag must match the version, prefixed with `v`:

```sh
git tag v0.1.0
git push origin v0.1.0
```

## GitHub Release

Create a GitHub Release for the tag (manual or via workflow), and attach:

- `dist/*.whl`
- `dist/*.tar.gz`

## Post-release

- Verify install from wheel in a fresh venv.
- Update the README if commands or requirements changed.
