# Research hypothesis (SuayLang)

This document states the primary research hypothesis for SuayLang and breaks it into measurable sub-claims for skeptical review.

## Primary hypothesis

**H1 (composability and local reasoning):**
Representing branching and iteration as *expression-based, pattern-driven* control flow (`dispatch` and `cycle`) improves composability and local reasoning compared to statement-oriented control flow, by making control-flow decisions and state evolution explicit at the expression level.

Non-claims (explicit):
- This is not a claim of universal readability across all populations.
- This is not a performance claim.
- This is not a claim that Unicode syntax is inherently superior; Unicode is treated as a controlled design variable.

## Measurable sub-claims

### C1 — Readability (descriptive proxy via rubric)
For a fixed set of small tasks, SuayLang solutions will tend to:
- use fewer distinct control constructs, and
- keep control logic locally visible within the boundaries of a `dispatch`/`cycle` expression.

Measurements (planned):
- LOC (non-empty, non-comment lines)
- Control-construct counts (SuayLang vs baseline)
- A conservative “local reasoning steps” rubric

### C2 — Predictability of evaluation
In v0.1 programs, control-flow transitions are predictable in the sense that:
- control flow is represented explicitly in the AST (`Dispatch`, `Cycle`), and
- evaluation steps can be mapped to a small set of VM control operations on the supported subset.

Measurements (planned):
- Documented mapping from AST nodes to bytecode schemas (where applicable)
- Differential testing to detect divergences

### C3 — Ease of semantic mapping to VM / state machines
`cycle` corresponds directly to a state machine:
- seed = initial state
- arms = transition relation
- `↩` = transition
- `↯` = termination

Measurements (planned):
- Interpreter↔VM observational equivalence on a documented subset
- A bounded generative component to search for counterexamples

## Threats to validity

### Internal validity
- **Rubric bias**: the rubric may privilege expression-oriented code.
  - Mitigation: publish the rubric and raw counts; keep criteria simple and pre-declared.
- **Task selection bias**: tasks may overfit SuayLang’s design.
  - Mitigation: use a fixed task set spanning branching-heavy, state-evolution, and interpreter-like logic; document exclusions.

### Construct validity
- **LOC is not comprehension**: fewer lines do not imply better understanding.
  - Mitigation: treat LOC as descriptive only; emphasize control and reasoning metrics.
- **Keyword counting is a proxy**: it does not capture nesting or semantic complexity.
  - Mitigation: report limitations; optionally include nesting depth as a secondary descriptive metric.

### External validity
- Results may not generalize beyond the chosen baseline language and reviewer population.
  - Mitigation: frame outcomes as micro-evaluation evidence, not broad claims.

### Implementation validity
- **Subset mismatch**: the VM may not support all interpreter features.
  - Mitigation: conformance claims are restricted to a documented subset.
- **Error-message instability**: message wording is not stable in v0.1.
  - Mitigation: compare termination kind, stdout, and spans; treat message text as optional/relaxed.
