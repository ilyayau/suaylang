# Committee Mode Checklist: What a Reviewer Will Try in the First 15 Minutes

This checklist is written as a script for a skeptical, hands-on evaluation.
Each item states the action and the expected result.

## 1) Install and verify

- [ ] Action: `python -m pip install -e .`
  - Expected: installs without errors; `suay` command becomes available.

- [ ] Action: `suay doctor`
  - Expected: prints Python version/platform, prints `doctor:ok`, ends with `OK`, exit code 0.

## 2) First program from scratch

- [ ] Action: create `hello.suay` with:
  - Expected: file can be run immediately.

```suay
square ← ⌁(x) x × x
say · ("square(7)=" ⊞ (text · (square · 7)))
```

- [ ] Action: `suay run hello.suay`
  - Expected: prints `square(7)=49`.

## 3) Confirm language primitives quickly

- [ ] Action: open the README and skim the “Language overview” and “Examples” sections.
  - Expected: constructs are named and shown (`←`, `⇐`, `dispatch`, `cycle`, `·`, variants).

- [ ] Action: read the semantics walkthrough.
  - Expected: step-by-step execution description without implementation jargon.

Reference: `docs/SEMANTIC_WALKTHROUGH.md`.

## 4) Run canonical examples

- [ ] Action: `suay run examples/committee_01_basic.suay`
  - Expected: prints `square(7)=49`.

- [ ] Action: `suay run examples/committee_02_dispatch.suay`
  - Expected: prints two lines: `ok:41` and `err:bad`.

- [ ] Action: `suay run examples/committee_03_cycle.suay`
  - Expected: prints `sum_to(5)=15`.

- [ ] Action: `suay run examples/committee_05_modules.suay`
  - Expected: prints `add(2,3)=5`.

## 5) Error experience (no tracebacks)

- [ ] Action: `suay run examples/committee_04_error.suay`
  - Expected: a calm runtime error with file/line/column and a caret span; **no Python traceback**.

- [ ] Action: intentionally introduce a syntax error (e.g. delete an `⇒` in a dispatch arm).
  - Expected: a syntax error with an accurate span and a helpful “Expected … got …” message; no traceback.

## 6) Reproducibility

- [ ] Action: `python -m unittest discover -s tests -v`
  - Expected: all tests pass on a clean checkout; stress tests assert no tracebacks.

## 7) Documentation sanity (what reviewers look for)

- [ ] Action: open `docs/LANGUAGE_CONTRACT_v0.1.md`.
  - Expected: explicit list of what v0.1 includes/excludes; stable vs unstable parts; compatibility rules.

- [ ] Action: open `docs/GRAMMAR.md`.
  - Expected: grammar matches implementation; precedence and newline rules are clear.

- [ ] Action: open `docs/BYTECODE.md`.
  - Expected: VM model is described in concrete terms; instruction set explains how control flow maps.
