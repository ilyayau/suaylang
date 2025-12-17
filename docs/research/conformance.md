# Conformance: interpreter ↔ VM equivalence (v0.1)

## What is being checked

SuayLang has two execution paths:

- **Interpreter** (reference semantics)
- **Bytecode VM** (alternate execution)

To reduce semantic drift risk, this repo provides:

1) A **conformance corpus runner** (fixed, human-readable programs)
2) A **differential fuzz runner** (many small generated programs)

Both compare these observable outcomes:

- termination class: `ok` / `lex` / `parse` / `runtime` / `internal`
- stdout (normalized for newlines)
- value equality (best-effort structural equality)
- for errors: error type + coarse (line, column) location

## Conformance corpus runner

Command:

```sh
python tools/conformance/run.py
```

Default corpus location:

- `tests/corpus/conformance/`

Success output:

- `conformance: OK files=N divergences=0 pass=N fail=0`

This runner is intended to be stable and used in CI.

## Differential fuzz runner

Command:

```sh
python -m tools.conformance.fuzz --seed 0 --n 5000
```

This generates `N` bounded programs, runs them on interpreter and VM, and reports divergences.

### Recorded result (reproducible)

- seed: `0`
- N: `5000`
- divergences: `0`

If divergences occur, repro cases are written under:

- `tools/conformance/fuzz_failures/`

## Scope

The conformance and fuzz layers target the subset supported by the VM compiler.
See:

- `docs/research/semantic_scope.md`
- `docs/research/feature_matrix.md`
