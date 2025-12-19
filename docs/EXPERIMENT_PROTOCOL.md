# Experiment protocol (differential testing + coverage)

This document is runnable: the protocol is implemented in `tools/diff_test/` and produces machine-readable reports under `results/`.

## 1) Differential testing: what is compared

### Inputs

A test case is a single SuayLang source file (string). Cases are generated deterministically from a `(seed, index, size_bucket)` triple.
We generate **both**:

- **valid programs** (intended to execute successfully most of the time), and
- **intentionally-invalid programs** (intended to trigger lex/parse/runtime errors to exercise diagnostics and error paths).

### Execution backends

For each program we run:

1. the reference interpreter (`suaylang.interpreter.Interpreter`)
2. the bytecode compiler + VM (`suaylang.compiler.Compiler` + `suaylang.vm.VM`)

Both runs are isolated and time-bounded.

### Captured observation

Each backend produces a structured observation:

- termination: `ok|lex|parse|runtime|internal`
- stdout and stderr (normalized `\r\n -> \n`)
- for `ok`: returned value (repr)
- for error: error kind + best-effort span location (line/column) + message (normalized)

Implementation: `tools/diff_test/runner.py`.

### Equivalence rule

Equivalence is decided by `tools/diff_test/comparator.py`:

- Termination class must match.
- Stdout must match after newline normalization.
- If `ok`: values must compare equal (fallback to repr structural comparison when needed).
- If error: error kind must match and (line, column) must match.

Notes:
- We intentionally keep error-message matching *loose*: messages may evolve while spans and kinds remain stable.
- The protocol still records messages for debugging and minimization.

## 2) Multi-seed plan (scaling)

### Full run (external validity target)

- Seeds: `0..99` (100 seeds).
- Per-seed programs:
  - `N_valid >= 1000`
  - `N_invalid >= 200`
- Size buckets: `small`, `medium`, `large`.

The harness stratifies cases so each seed covers each size bucket.

### CI run (gating subset)

CI runs a smaller but structurally similar subset:

- Seeds: `0..9`
- `N_valid` and `N_invalid` reduced (configurable) to keep runtime bounded.

## 3) Minimization (shrinking failing programs)

When a divergence occurs:

1. The failing program is saved under `tools/diff_test/corpus/regressions/`.
2. The minimizer attempts line-based delta debugging:
   - repeatedly delete lines and keep deletions that preserve the divergence.
3. The minimized counterexample is saved and becomes a regression input in future runs.

Implementation: `tools/diff_test/minimizer.py`.

## 4) Coverage: what it means and how it’s measured

Coverage is reported as three complementary measures:

### 4.1 AST node-kind coverage

- We parse each **parsable** program and count occurrences of each AST dataclass type.
- Coverage is the set of observed node kinds + counts.

### 4.2 Opcode-kind coverage (static)

- For each **compilable** program we compile to bytecode and count which opcode kinds appear.
- Coverage is the set of observed opcode kinds + counts.

### 4.3 Semantic-branch proxy coverage

We report behavioral diversity as counts across termination categories and error categories:

- `ok|lex|parse|runtime|internal` frequencies
- top error signatures (kind + coarse message prefix)

This is a proxy for semantic-branch coverage; it is explicitly not statement/branch coverage.

Implementation: `tools/diff_test/coverage.py`.

## 5) “Why this is enough” (justification)

- **Determinism**: seeds make failures reproducible and reviewable.
- **Scale**: 100 seeds × multiple size buckets exercises a large slice of the state space.
- **Diversity**: generation includes:
  - long programs (large bucket),
  - nested blocks/dispatch/cycle,
  - higher-order calls,
  - map/list/tuple/variant shapes,
  - and adversarial error-path cases (bad tokens, unclosed blocks, bad arity).
- **Actionability**: divergences are minimized and stored as regressions.

Run it with:

- `make diff-test` (full)
- `make diff-test-ci` (CI subset)
