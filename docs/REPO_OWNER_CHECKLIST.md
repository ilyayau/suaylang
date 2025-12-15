# Repo Owner Checklist (GitHub settings)

This checklist captures GitHub-side metadata/polish that can’t be reliably set by automation in a coding session.

## About panel

- **Description**: “SuayLang — explicit control-flow language (interpreter + bytecode VM) in Python”
- **Website/Homepage**: link to the README or a project page if you have one
- **Topics** (suggested):
  - programming-language
  - language-design
  - interpreter
  - compiler
  - bytecode
  - virtual-machine
  - research
  - python

## Repository settings

- Enable GitHub Actions (CI).
- Enable Issues (for bug reports) and apply templates if desired.
- (Optional) Enable Discussions for reviewer questions.

## Release setup

- Create the first GitHub Release matching the version in `pyproject.toml` (e.g. `v0.1.0`).
- Attach `dist/*.whl` and `dist/*.tar.gz` artifacts from CI or a local `python -m build`.
