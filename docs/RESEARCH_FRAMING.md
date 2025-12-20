# Research Framing

## Research Question
- Main RQ: Can SuayLang maintain observational equivalence and stable diagnostics between interpreter and VM under a strict observation policy?
- Secondary RQ: How do diagnostics stability and backend equivalence compare to existing small languages?

## Hypothesis
- Interpreter and VM are observationally equivalent (termination, value, stdout) on a seeded program set.
- Diagnostics (error kind, code, span) are contractually enforced and stable.
- Success: 0 divergences, deterministic diagnostics, coverage of all node kinds.
- Failure: Any divergence or unstable diagnostics.

## Contributions
- Deterministic differential testing harness.
- Golden diagnostics contract and enforcement.
- Coverage reporting on language constructs.
- Baseline and ablation comparison pipeline.
- CI artifact reproducibility.
- Paper-shaped artifact with real results.

## Limitations / Non-goals
- No full-featured IDE integration.
- No external language interop.
- No performance optimization claims.
- No non-deterministic features.

## Threats to Validity
- Generator bias in seeded programs.
- Coverage gaps in node/opcode kinds.
- Seed dependence for differential tests.
- Oracle limits for diagnostics.
- Performance noise in benchmarks.

## Related Work Positioning
- Similar to Rust: strong diagnostics, but not contractually enforced.
- Similar to OCaml: pattern matching, but no backend equivalence contract.
- Similar to Python: small language, but no diagnostics stability.
- Similar to Lua: embeddable, but no formal semantics.
- Differs by explicit observation policy.
- Differs by artifact reproducibility.
- Differs by diagnostics contract.
- Differs by coverage reporting.
- Differs by CI artifact visibility.
- Differs by paper-shaped results.
- Existing approaches insufficient for scorable backend equivalence.
- Existing approaches insufficient for diagnostics stability.

---

## Why this matters academically

SuayLang operationalizes claims about semantics and tooling as executable, falsifiable contracts. This enables reproducible, reviewer-auditable evidence for backend equivalence and diagnostics stability, advancing the state of PL testing and artifact review.
