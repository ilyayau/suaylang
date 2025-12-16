# Research hypothesis (SuayLang v0.1)

This document states the primary research hypothesis for SuayLang and breaks it into measurable, reviewer-facing claims.

## Primary hypothesis

**H1 (composability + local reasoning):**
Making *control flow expression-based and pattern-driven* (via `dispatch` and `cycle` as expressions) improves composability and local reasoning compared to statement-oriented control flow, without relying on implicit mutation or hidden state.

Interpretation constraints (what H1 does **not** claim):
- H1 does **not** claim SuayLang is universally “more readable” for all programmers.
- H1 does **not** claim performance superiority.
- H1 does **not** claim fewer bugs in general; it claims a reduction in *control-flow-related* reasoning burden under a specific rubric.

## Measurable sub-claims

### C1 — Readability (rubric-measured, not participant-study)
For a fixed set of small tasks (branching-heavy logic, iterative state evolution, and interpreter-like logic), SuayLang solutions will:
- use fewer distinct control constructs, and
- keep control flow locally visible within the expression boundaries.

Operationalization:
- **LOC** (non-empty, non-comment lines).
- **Control construct count**:
  - SuayLang: count occurrences of `▷` (`dispatch`), `⟲` (`cycle`), `↩`, `↯`.
  - Baseline (Python): count `if`/`elif`/`else`, `while`/`for`, `match`/`case`, `break`/`continue`.

Evidence:
- Method + table in docs/research/MICRO_EVAL.md.
- Reproducible metrics script: scripts/micro_eval.py.

### C2 — Predictability of evaluation (semantic transparency)
SuayLang programs in the v0.1 contract have predictable evaluation in the sense that:
- control-flow decisions are *explicitly represented* as `dispatch`/`cycle` nodes in the AST;
- the evaluation step boundaries are stable and inspectable via the interpreter trace (engineering artifact);
- there is a direct mapping from high-level control to VM jumps and state transitions.

Operationalization:
- For a supported subset, map each `dispatch`/`cycle` to a small, bounded bytecode schema.
- Document the schema and any unsupported constructs.

Evidence:
- docs/BYTECODE.md and docs/SEMANTIC_WALKTHROUGH.md (existing).
- Conformance and coverage statements in docs/research/CONFORMANCE.md (added).

### C3 — Ease of semantic mapping to VM / state machines
`cycle` can be interpreted as an explicit state machine:
- seed = initial state
- arms = transition relation
- `↩` = transition (continue)
- `↯` = accept/finish

Operationalization:
- Implement differential tests: same program executed by interpreter vs VM must be observationally equivalent on the supported subset.
- Include at least one generative component to search for divergences.

Evidence:
- Differential runner: scripts/conformance.py.
- Shared corpus: tests/corpus/conformance/*.suay.
- Generative differential test: tests/test_conformance_fuzz.py.

## Threats to validity (conservative)

### Internal validity
- **Rubric bias:** the “local reasoning steps” rubric may privilege expression-based styles.
  - Mitigation: define the rubric *before* looking at results; report the rubric and raw counts.
- **Task selection bias:** chosen tasks may overfit SuayLang strengths.
  - Mitigation: include at least one interpreter-like task and at least one mixed branch+loop task; explicitly list excluded tasks.

### Construct validity
- **LOC is not comprehension:** fewer lines does not guarantee improved understanding.
  - Mitigation: treat LOC as a descriptive metric only; emphasize the control-construct and reasoning-step metrics.
- **Construct-count proxy limitations:** counting keywords does not capture nesting or complexity.
  - Mitigation: count both constructs and nesting depth where feasible; report limitations.

### External validity
- **Population:** results do not generalize across programmer backgrounds.
  - Mitigation: frame evaluation as micro-evaluation for skeptical reviewers; not a user study.
- **Tooling confound:** Unicode syntax may affect readability due to font/editor support.
  - Mitigation: treat Unicode as a research variable (docs/research/UNICODE_VARIABLE.md).

### Implementation validity
- **Subset mismatch:** VM may not support all constructs supported by the interpreter.
  - Mitigation: publish a coverage statement for the conformance claim; treat unsupported as “not evaluated,” not “equivalent.”
- **Oracle fragility:** error message wording is intentionally unstable in v0.1.
  - Mitigation: define observational equivalence that is robust to message wording (category + span + stdout), with an optional strict mode.
