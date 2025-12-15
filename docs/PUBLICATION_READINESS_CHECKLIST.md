# SuayLang Publication Readiness Checklist (Public Release + Academic Review)

This is a strict checklist for preparing SuayLang for:

- GitHub public release
- academic review
- MEXT-level submission

It is intentionally conservative: if an item is unchecked, assume it is a risk.

## A) Repository and legal hygiene

- [ ] A clear open-source license file exists (e.g., `LICENSE`) and matches the intended release terms.
- [ ] Copyright ownership is clear (no copied code; dependencies are documented).
- [ ] `README.md` describes scope, constraints, and how to reproduce results.
- [ ] `SECURITY.md` exists or the README explicitly states how to report security issues.
- [ ] `CODE_OF_CONDUCT.md` exists (recommended for public projects).
- [ ] Contact point is present (email or issue tracker policy).

## B) Reproducibility and environment

- [ ] Supported Python versions are stated and verified.
- [ ] Clean checkout run works: `python -m unittest discover -s tests -v` passes.
- [ ] No network access is required for tests.
- [ ] Instructions work on a fresh machine (no hidden local state).
- [ ] Examples run as documented.
- [ ] Any non-UTF-8 assumptions are avoided or stated.

## C) Code quality and maintainability

- [ ] Public entrypoints are stable and documented (CLI usage, interpreter/VM behavior).
- [ ] Error handling policy is consistent (no raw host-language tracebacks to users).
- [ ] Code structure is clear (lexer/parser/interpreter/compiler/vm separated by responsibility).
- [ ] Dead code and large commented-out blocks are removed.
- [ ] There is a consistent formatting approach (even if no formatter is enforced).

## D) Semantics and stability guarantees

- [ ] The v0.1 contract exists and matches implementation: `docs/LANGUAGE_CONTRACT_v0.1.md`.
- [ ] The formal grammar matches implementation behavior: `docs/GRAMMAR.md`.
- [ ] The minimal stdlib is documented and tested: `docs/STDLIB.md` and `tests/test_stdlib.py`.
- [ ] Interpreter and VM semantic differences (if any) are documented.
- [ ] Backwards-compatibility rules for patch releases are stated.

## E) Documentation completeness (reviewer-grade)

- [ ] Design rationale exists and is candid: `docs/WHY_SUAYLANG.md`.
- [ ] Step-by-step semantics walkthrough exists: `docs/SEMANTIC_WALKTHROUGH.md`.
- [ ] Bytecode documentation exists: `docs/BYTECODE.md`.
- [ ] Accessibility notes are clearly labeled as proposal vs. implemented behavior: `docs/ACCESSIBILITY_REDESIGN.md`.
- [ ] README links to all core docs.

## F) Tooling and UX

- [ ] CLI help text is accurate and minimal.
- [ ] Diagnostics include file/line/column spans and caret context.
- [ ] Stress tests enforce “no tracebacks” invariant.
- [ ] VS Code extension instructions are correct and do not assume unpublished marketplace installs.

## G) Academic evaluation readiness

- [ ] The paper text exists and is consistent with the repo: `docs/PAPER_SuayLang_Design_and_Implementation.md`.
- [ ] Claims are bounded and verifiable (no performance claims without data).
- [ ] Limitations are explicit (missing features, scope, VM status).
- [ ] The evaluation story is reproducible (tests + examples + documented semantics).
- [ ] Version is pinned (v0.1) and the contract is referenced in the paper and README.

## H) Versioning and release process

- [ ] A version tag strategy exists (e.g., `v0.1.0`, `v0.1.1`, …).
- [ ] Patch releases (`0.1.x`) are guaranteed source-compatible per the contract.
- [ ] Breaking changes require a minor bump (`0.2.0+`) and a migration note.
- [ ] A changelog strategy exists (`CHANGELOG.md` recommended).

## I) Final smoke checks

- [ ] Run: `./suay run examples/hello.suay` → prints `total=30`.
- [ ] Run: `python examples/bytecode_demo.py` → prints `total=30` and no errors.
- [ ] Run: `python -m unittest discover -s tests -v` → all green.
- [ ] Verify grep for accidental tracebacks in CLI output paths (stress tests should cover this).
