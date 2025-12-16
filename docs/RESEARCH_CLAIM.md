# Core Research Claim (SuayLang v0.1)

## 1) Hypothesis

SuayLang’s expression-based, explicit control flow (`dispatch` and `cycle`) enables **reproducible, artifact-backed observational equivalence testing** between a reference interpreter and a bytecode VM for a documented, VM-supported subset.

## 2) What is measured

- **Differential testing (interpreter vs VM)**
  - Evidence artifact: the shared observation/comparison policy in [suaylang/conformance.py](suaylang/conformance.py) and the seeded runner in [tools/conformance/fuzz_runner.py](tools/conformance/fuzz_runner.py).
  - Outputs compared: termination class, stdout, result values (best-effort), and coarse error location for diagnostics/runtime errors.

- **Semantic construct coverage (within the VM-supported subset)**
  - Covered by corpus and fuzz templates: `dispatch`, `cycle`, binding (`←`), calls (`·`), variants, lists/tuples, arithmetic/comparison.
  - Scope statement: [docs/research/semantic_scope.md](docs/research/semantic_scope.md).
  - Corpus runner: [tools/conformance/run.py](tools/conformance/run.py) with inputs under [tests/corpus/conformance](tests/corpus/conformance).

- **Error-class coverage**
  - Measured termination categories: `ok | lex | parse | runtime | internal`.
  - Differential testing records counts per category (see [docs/research/differential_testing.md](docs/research/differential_testing.md)).

- **Key properties (as exercised and observed in artifacts)**
  - **Determinism**: the reference implementation provides deterministic execution for a fixed program and fixed input; the differential harness uses deterministic seeds and compares observable outputs.
  - **Absence of implicit state (at the language level)**: state changes are explicit via binding (`←`) and mutation (`⇐`), and loops are explicit via `cycle` state transitions.
  - **Predictable evaluation order (in the reference implementation)**: the interpreter defines a single evaluation strategy; the VM is validated against that strategy via observation-based equivalence checks.

## 3) Experimental protocol

- **Program generation (property-based / fuzzing)**
  - The runner [tools/conformance/fuzz_runner.py](tools/conformance/fuzz_runner.py) generates randomized programs from a bounded subset designed to terminate.
  - Generation is reproducible via `--seed` and bounded via `--n`.

- **Execution on both backends**
  - For each generated program:
    1. Run on the reference interpreter.
    2. Compile with the bytecode compiler and run on the VM.
  - Both runs capture stdout and classify termination (success, diagnostic, runtime error, internal error).

- **Equivalence checking**
  - Observations are compared by [suaylang/conformance.py](suaylang/conformance.py):
    - termination class must match,
    - stdout must match (normalized for line endings),
    - on success, result values are compared with best-effort structural equality,
    - on errors, coarse error type and (line, column) are compared.
  - On any mismatch, the harness saves a reproducer program and both observations.

- **Subset covered and exclusions**
  - The evaluation is explicitly limited to the **VM-supported subset** (AST nodes supported by the compiler/VM), per [docs/research/semantic_scope.md](docs/research/semantic_scope.md).
  - Excluded (because they are not required for the current equivalence claim, are interpreter-only, or introduce external nondeterminism):
    - module loading via `link` (interpreter-only in current v0.1 scope),
    - file IO and interactive input,
    - constructs not implemented by the bytecode compiler,
    - unbounded recursion and unbounded loops.

This protocol is designed to support a narrow, defensible claim: **interpreter and VM agree observationally on the tested VM-supported subset**, not on the full language.
