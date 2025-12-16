# Hypothesis → evidence map

This is a conservative mapping from claims to planned evidence. It is intended to prevent overclaiming.

| Claim | Evidence (planned) | Limitations |
|---|---|---|
| H1: Expression-based, pattern-driven control improves composability/local reasoning | Micro-evaluation tasks comparing SuayLang vs Python; LOC + construct counts + rubric notes | No human-subject study; proxies may not reflect comprehension |
| C1: Readability improvements (proxy) | Measured construct counts on fixed tasks; annotated rubric steps | Unicode confounds; reviewer familiarity varies |
| C2: Predictability of evaluation | Documented AST forms; mapping to bytecode schemas where applicable; differential tests | Mapping only for supported VM subset |
| C3: Ease of mapping `cycle` to a state machine | Conformance tests on cycle-heavy corpus; generative differential tests on subset | Restricted subset; may miss rare divergences |
| Interpreter↔VM equivalence on supported subset | Differential runner comparing stdout, termination, error spans | Does not guarantee identical error text or stack trace |
| VM justification (engineering) via relative performance | Micro-benchmarks comparing interpreter vs VM on relevant categories | Timing results are environment-specific; no cross-language claims |
| Unicode is a deliberate trade-off | Unicode trade-off analysis and mitigation list | Not a validated usability study |
