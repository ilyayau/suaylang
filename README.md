# SuayLang (v0.1)

[![CI](https://github.com/ilyayau/suaylang/actions/workflows/ci.yml/badge.svg)](https://github.com/ilyayau/suaylang/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

SuayLang is a small, expression-oriented programming language designed around **explicit control flow**.
It is implemented in pure Python and includes two execution paths:

- an interpreter (reference behavior)
- a minimal stack-based bytecode compiler + VM (alternate execution)

This repository is intended for public review: language design, semantics, error model, and tooling are documented and tested.

Canonical contract docs:

- [docs/LANGUAGE_REFERENCE.md](docs/LANGUAGE_REFERENCE.md) (single source-of-truth)
- [docs/ASCII_SYNTAX.md](docs/ASCII_SYNTAX.md) (ASCII aliases; normative)
- [docs/ERROR_CODES.md](docs/ERROR_CODES.md) (stable error codes)

For a stability definition of “v0.1”, see [docs/LANGUAGE_CONTRACT_v0.1.md](docs/LANGUAGE_CONTRACT_v0.1.md).

## 60-second Quickstart

If you can copy-paste this, you can run SuayLang.

### Linux/macOS

```sh
git clone https://github.com/ilyayau/suaylang
cd suaylang
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .

suay doctor
suay run examples/hello.suay

# Contract-mode helpers:
suay ref ascii
suay explain E-SYNTAX
suay --error-codes run examples/hello.suay
```

### Windows (PowerShell)

```powershell
git clone https://github.com/ilyayau/suaylang
cd suaylang
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e .

suay doctor
suay run examples/hello.suay
```

## Research Orientation

This project is designed for open scientific review and international reproducibility, with clear semantics and rerunnable evaluation artifacts (tests, conformance, fuzzing, benchmarks).

## Evaluation snapshot (v0.1.0)

- Conformance corpus: 4 programs, divergences = 0 (`python tools/conformance/run.py`)
- Fixed task set: 6 programs, divergences = 0 (`python tools/conformance/run.py evaluation/tasks`)
- Differential fuzz: seed=0, N=1000, divergences = 0 (`python -m tools.conformance.fuzz --seed 0 --n 1000`)
- Micro-benchmarks: interpreter vs VM median timings + VM instruction counts (see [docs/research/results.md](docs/research/results.md))
- Golden diagnostics: stable snapshots (`tests/golden/cases/*.txt`, `tests/golden/diagnostics/*.txt`)

## How to reproduce results

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"

pytest -q
python tools/conformance/run.py
python tools/conformance/run.py evaluation/tasks
python -m tools.conformance.fuzz --seed 0 --n 1000
python benchmarks/run.py evaluation/tasks --iters 200
```

## Related Work (brief)

- Rust: both use pattern matching; SuayLang makes branching/looping expression-shaped (`dispatch`/`cycle`) and validates an interpreter against a bytecode VM.
- OCaml: both use variants + pattern matching; SuayLang adds an explicit state-machine loop (`cycle`) with continue/finish modes.
- Haskell: both encourage expression-oriented style; SuayLang models looping via `cycle` rather than recursion as the default.
- Erlang: both use tagged values for control flow; SuayLang is single-process and focuses on interpreter↔VM equivalence evidence.
- Scheme/Racket: both treat many constructs as expressions; SuayLang keeps a fixed, small operator surface to keep the semantics scorable and test-backed.
- WebAssembly (Wasm): both expose a bytecode execution model; SuayLang treats bytecode as an alternate backend validated against an interpreter.
- Lua: both aim for a small core; SuayLang’s main measurable output is backend equivalence + diagnostics stability rather than embeddability.
- Crafting Interpreters-style systems: both build interpreters/VMs; SuayLang makes the equivalence test harness and scope statement part of the artifact.

## References

- G. D. Plotkin, “A Structural Approach to Operational Semantics,” 1981.
- G. Kahn, “Natural Semantics,” 1987.
- L. Maranget, “Compiling Pattern Matching to Good Decision Trees,” 2008.
- K. Claessen and J. Hughes, “QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs,” 2000.
- W. M. McKeeman, “Differential Testing for Software,” 1998.
- X. Yang et al., “Finding and Understanding Bugs in C Compilers,” 2011.
- V. Le et al., “Compiler Validation via Equivalence Modulo Inputs,” 2014.
- A. V. Aho, M. S. Lam, R. Sethi, and J. D. Ullman, “Compilers: Principles, Techniques, and Tools,” 2nd ed., 2006.

## Quickstart (2 minutes)

### Linux/macOS

```sh
git clone https://github.com/ilyayau/suaylang
cd suaylang
./scripts/install.sh

suay doctor
suay run examples/hello.suay

suay new my-project
cd my-project
suay run src/main.suay
```

### Windows (PowerShell)

```powershell
git clone https://github.com/ilyayau/suaylang
cd suaylang
./scripts/install.ps1

suay doctor
suay run examples/hello.suay

suay new my-project
cd my-project
suay run src/main.suay
```

Reference sheet:
- [docs/REFERENCE_SHEET.md](docs/REFERENCE_SHEET.md)
- ASCII aliases (first-class): [docs/syntax_mapping.md](docs/syntax_mapping.md)

Demo + tutorial:
- [demos/README.md](demos/README.md)
- [docs/TUTORIAL.md](docs/TUTORIAL.md)
- [docs/USE_CASES.md](docs/USE_CASES.md)

## Start in 60 seconds

Linux/macOS:

```sh
git clone https://github.com/ilyayau/suaylang && cd suaylang && ./scripts/install.sh
suay run examples/hello.suay
```

Windows (PowerShell):

```powershell
git clone https://github.com/ilyayau/suaylang; cd suaylang; ./scripts/install.ps1
suay run examples/hello.suay
```

## Why this language exists

SuayLang is a constraint-driven experiment:

- Control flow should be **composable** (branching and looping are expressions).
- State changes should be **visible** (binding and mutation are distinct).
- Programs should map cleanly to **bytecode/state-machine** reasoning.

It is not trying to compete with mainstream languages or their ecosystems.

## Language overview

SuayLang is expression-first. Its signature constructs are:

- Binding: `name ← expr`
- Mutation: `name ⇐ expr` (updates an existing binding)
- Blocks: `⟪ ... ⟫` (newlines separate forms)
- Lambda: `⌁(pattern ...) expr` (closures, lexical scoping)
- Application: `f · x · y` (curried)
- Pattern match: `value ▷ ⟪ ▷ pat ⇒ expr ... ⟫` ("dispatch")
- Pattern-driven loop: `⟲ seed ▷ ⟪ ▷ pat ⇒ ↩ expr | ▷ pat ⇒ ↯ expr ... ⟫` ("cycle")
- Variants: `Tag•payload`
- Maps: `⟦ key ↦ value , ... ⟧`

Newlines are significant; top-level and block forms are separated by newline(s).

## Examples (representative, small)

### 1) Higher-order style (map + fold)

```suay
square ← ⌁(x) x × x
nums ← [1 2 3 4]

total ← fold · (⌁(a b) a + b) · 0 · (map · square · nums)
say · ("total=" ⊞ (text · total))
```

### 2) Dispatch: branch on data shape

```suay
classify ← ⌁(v)
    v ▷ ⟪
    ▷ Ok•x  ⇒ "ok:" ⊞ (text · x)
    ▷ Err•m ⇒ "err:" ⊞ m
    ▷ _     ⇒ "unknown"
    ⟫

say · (classify · (Ok•41))
```

### 3) Cycle: explicit state machine

```suay
sum_to ← ⌁(n)
    ⟲ (Step•(1 0)) ▷ ⟪
    ▷ Done•acc     ⇒ ↯ acc
    ▷ Step•(i acc) ⇒ ↩ (
            (i > n) ▷ ⟪
            ▷ ⊤ ⇒ Done•acc
            ▷ ⊥ ⇒ Step•(i + 1  acc + i)
            ⟫
        )
    ⟫

say · (text · (sum_to · 5))
```

## Demo (3 commands)

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

suay run examples/hello.suay
pytest -q
python scripts/smoke.py
```

### 4) Modules (MVP): explicit loading via `link`

```suay
m ← link · "./examples/modules/math"  
add ← m · "add"
say · (text · (add · 2 · 3))
```

## Execution model (what runs)

### Interpreter (reference)

- Deterministic evaluation order.
- Lexical scoping + closures.
- `dispatch` chooses the first matching arm; arm bindings exist only inside that arm.
- `cycle` repeats by matching the current state; each arm explicitly chooses `↩` (continue) or `↯` (finish).

### Bytecode VM (MVP)

The VM is a stack machine with an explicit environment chain. It is designed to mirror the interpreter’s semantics for the supported subset.

See [docs/BYTECODE.md](docs/BYTECODE.md) for the instruction model and mapping.

## Tooling and error model

The CLI reports user-facing errors with file/line/column spans and caret context. The project’s tests enforce that CLI failures do not emit Python tracebacks.

Example shape:

```text
examples/bad.suay:1:14: runtime error: Undefined name 'z'
...source line...
                         ^
stack:
- examples/bad.suay:4:1: call f
- examples/bad.suay:2:10: call g
```

## Run / reproduce

### Requirements

- Python 3.10+

### Reproducible build in ~60 seconds

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
make check
```

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for a 15-minute reviewer path.
See [docs/testing.md](docs/testing.md) for the testing pyramid.

### One-command installation

From a clean environment:

```sh
python -m pip install -e .
```

Verify the install:

```sh
suay doctor
```

Expected output includes a line `doctor:ok` followed by `OK`.

### CLI

From a source checkout:

```sh
./suay --help
./suay check examples/hello.suay
./suay run examples/hello.suay
```

After installation, you can also run:

```sh
suay --help
suay run examples/hello.suay
```

Expected output:

```text
total=30
```

The CLI is also available as:

```sh
python -m suaylang --help
```

### Bytecode demo

```sh
python examples/bytecode_demo.py
```

## Documentation index

## Research Artifacts

- Research folder: [docs/research/](docs/research/)
- Evaluation plan (methodology only): [docs/research/evaluation_plan.md](docs/research/evaluation_plan.md)
- Reviewer path (15 minutes): [docs/research/REVIEWER_PATH.md](docs/research/REVIEWER_PATH.md)

- Grammar (formal EBNF aligned to implementation): [docs/GRAMMAR.md](docs/GRAMMAR.md)
- Minimal standard library (builtins): [docs/STDLIB.md](docs/STDLIB.md)
- Bytecode + VM (MVP): [docs/BYTECODE.md](docs/BYTECODE.md)
- Semantics walkthrough (step-by-step evaluation): [docs/SEMANTIC_WALKTHROUGH.md](docs/SEMANTIC_WALKTHROUGH.md)
- Design rationale (opinionated, non-marketing): [docs/WHY_SUAYLANG.md](docs/WHY_SUAYLANG.md)
- v0.1 stability contract: [docs/LANGUAGE_CONTRACT_v0.1.md](docs/LANGUAGE_CONTRACT_v0.1.md)
- Accessibility redesign proposal (syntax-only, no new features): [docs/ACCESSIBILITY_REDESIGN.md](docs/ACCESSIBILITY_REDESIGN.md)
- Committee-mode checklist (15-minute evaluation script): [docs/COMMITTEE_MODE_CHECKLIST.md](docs/COMMITTEE_MODE_CHECKLIST.md)

## Canonical examples (committee pack)

These are short, self-contained examples intended for live evaluation:

- `examples/committee_01_basic.suay`
- `examples/committee_02_dispatch.suay`
- `examples/committee_03_cycle.suay`
- `examples/committee_04_error.suay`
- `examples/committee_05_modules.suay`

## 5-minute first program (from an empty directory)

```sh
mkdir my-suay && cd my-suay
python -m venv .venv
source .venv/bin/activate

# install SuayLang (from a checkout of this repository)
python -m pip install -e /path/to/suayLang
suay doctor

# write a first program
cat > hello.suay <<'SUAY'
square ← ⌁(x) x × x
say · ("square(7)=" ⊞ (text · (square · 7)))
SUAY

suay run hello.suay
```

Expected output:

```text
square(7)=49
```

## VS Code extension (local)

The local extension in [vscode-extension/suaylang](vscode-extension/suaylang) provides syntax highlighting and a minimal LSP experience.

## Tests

```sh
python -m unittest discover -s tests -v
```

## Development

Create a virtual environment and install in editable mode:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
suay doctor
```

Contribution guidelines and security policy:

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## Repository layout

- `suaylang/` — lexer/parser/interpreter/compiler/vm + runtime/errors
- `examples/` — example programs and Python demos
- `tests/` — unit and stress tests (`unittest`)
- `docs/` — grammar, semantics, bytecode, contracts
- `vscode-extension/` — editor support
