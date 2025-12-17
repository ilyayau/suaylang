# Research Core (SuayLang v0.1)

## 1) Research problem

Small language implementations often ship an interpreter and later add a compiler+VM for speed or deployment. The research risk is semantic drift: the two backends may disagree in subtle, user-visible ways. SuayLang is used here as a controlled experimental platform to study (i) explicit control-flow constructs that are expression-shaped (`dispatch`, `cycle`) and (ii) an evidence-producing validation method for interpreter↔VM equivalence on a deliberately limited subset.

## 2) Primary hypothesis H2 (mandatory)

**H2:** *Interpreter and bytecode VM can be made observationally equivalent on a defined subset, and this equivalence can be validated automatically.*

### Success criteria (measurable)

H2 is supported for a specific release snapshot if all are true:

- **Conformance (fixed corpus):** Running the conformance runner over the fixed corpora reports **divergences = 0**.
- **Differential fuzzing:** Running the seeded fuzz runner for a fixed $N$ reports **divergences = 0**.
- **Subset is explicit:** The subset is enumerated (construct list) and results are stated as *“on this subset”*.

### Failure / falsification criteria

H2 is falsified for the evaluated snapshot if any occur:

- Any program in the fixed corpus produces different observable outcomes between interpreter and VM (termination class, stdout, value, or error class/location).
- Seeded fuzzing at the stated $N$ produces one or more divergences.
- The observed equivalence relies on undefined behavior or on features explicitly marked out-of-scope for the VM subset.

### Controlled scope for H2

H2 is only claimed on the **VM-supported subset** described in:

- [docs/spec/supported_subset.md](spec/supported_subset.md)

Rationale for limiting scope:

- The goal is not “a complete language spec”; it is to make equivalence falsifiable and automatically checkable.
- Interpreter-only features (e.g., module loading) are excluded so equivalence evidence is not diluted by unimplemented VM features.

## 3) Secondary hypothesis H1 (optional; measured with proxies)

**H1:** *Expression-based explicit control flow reduces local reasoning complexity compared to statement-based control flow on selected tasks.*

Because “reasoning complexity” is not directly observable in this repository, H1 is evaluated only through **simple structural proxies** on a fixed task set:

- token count
- approximate AST depth
- branch-point count

### Success criteria (measurable)

H1 is supported (weakly) for the selected tasks if, on a majority of tasks, SuayLang programs have:

- **no more branch points** than the Python baseline, and
- **no greater AST depth** than the Python baseline,

under the explicit counting rules in [docs/research/H1_metrics.md](research/H1_metrics.md).

### Failure / falsification criteria

H1 is falsified for the selected tasks if, under the stated rules, SuayLang consistently has **more branch points** and/or **greater AST depth** than Python, or if results are highly sensitive to superficial formatting and cannot be reproduced with the provided scripts.

### Controlled scope for H1

H1 is restricted to a small, fixed set of tasks intended to exercise `dispatch`/`cycle`. No claims are made about programmer populations, maintainability in production systems, or general readability.

## 4) Where the evidence lives

- H2 results: [docs/research/H2_results.md](research/H2_results.md)
- H1 metrics (proxy evidence): [docs/research/H1_metrics.md](research/H1_metrics.md)
- Scope control (explicit out-of-scope): [docs/SCOPE.md](SCOPE.md)
