# Core Research Claim (SuayLang v0.1)

## A) Hypothesis

Expression-based, explicit control flow (SuayLang `dispatch`/`cycle`) improves local semantic checkability and enables observational equivalence between a reference interpreter and a bytecode VM on a defined, VM-supported subset.

## B) What we will measure

- Differential testing (interpreter vs VM)
  - Observable outputs: termination class, stdout (normalized), returned value (best-effort structural equality), and coarse error location (line/column).
  - Evidence artifacts: [tools/conformance/run.py](tools/conformance/run.py), [tools/conformance/fuzz_runner.py](tools/conformance/fuzz_runner.py), and the comparison policy in [suaylang/conformance.py](suaylang/conformance.py).

- Semantic construct coverage
  - Covered constructs (subset-level): `dispatch`, `cycle`, binding/mutation, blocks, lambdas, calls, variants, lists/tuples, maps, arithmetic/comparison.
  - Scope statement: [docs/research/semantic_scope.md](docs/research/semantic_scope.md) and [docs/research/feature_matrix.md](docs/research/feature_matrix.md).

- Number of distinct error classes covered
  - Measured termination categories: `ok | lex | parse | runtime | internal` (5 classes), with counts recorded by the differential harness.

- Key properties (as exercised and checked via artifacts)
  - Determinism (fixed program + fixed seed yields stable observations)
  - No implicit state transitions (state changes are explicit via `←`/`⇐` and `cycle` transitions)
  - Predictable evaluation order (interpreter defines a single evaluation strategy; VM is checked against it)
  - Stable diagnostic structure (span-anchored errors with stable formatting, maintained via golden diagnostics)

## C) Experimental protocol

- Program generation (property-based / differential testing)
  - Generate many small, bounded programs from the VM-supported subset using [tools/conformance/fuzz_runner.py](tools/conformance/fuzz_runner.py).
  - Generation is reproducible via `--seed` and bounded via `--n`.

- Subset definition (in/out)
  - In-scope: constructs supported by the compiler/VM, per [docs/research/semantic_scope.md](docs/research/semantic_scope.md) and [docs/research/feature_matrix.md](docs/research/feature_matrix.md).
  - Out-of-scope: interpreter-only features (e.g., `link` modules), external I/O, and constructs not implemented by the compiler.

- Equivalence checking
  - Run each program on the interpreter and on the VM.
  - Compare: (1) termination class, (2) stdout, (3) value on success, (4) error type + coarse (line, column) location on failure.
  - On any mismatch, save the program and both observations as a reproducer.

- Reporting
  - Report: “N programs tested, 0 divergences, K divergences found (and fixed)”, with the seed, N, and saved repro paths.
  - Fixed-program coverage is reported by the conformance corpus runner: `python tools/conformance/run.py` (inputs under `tests/corpus/conformance/`).
