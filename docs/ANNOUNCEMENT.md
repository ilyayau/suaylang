# SuayLang v0.1: Unicode-first explicit control flow (interpreter + VM)

SuayLang is a small, expression-oriented language built around **explicit control flow**:

- `dispatch` (`▷`) for pattern-based branching
- `cycle` (`⟲`) for pattern-driven state machines
- distinct binding vs mutation (`←` vs `⇐`)

This repo is set up as a reproducible research artifact:

- interpreter ↔ VM conformance corpus (`python tools/conformance/run.py`)
- differential fuzzing (`python -m tools.conformance.fuzz`)
- micro-benchmarks (`make bench`)
- Unicode syntax remains primary, but an ASCII alias layer is supported (see `docs/syntax_mapping.md`).

Quickstart:

```sh
./scripts/install.sh
suay run examples/hello.suay
suay run demos/workflow_state_machine/main.suay
```
