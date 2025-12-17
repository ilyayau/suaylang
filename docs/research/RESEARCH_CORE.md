# Research Core (SuayLang v0.1)

## 1) Formal problem statement

When a language has multiple execution backends (e.g., interpreter and bytecode VM), the system can become non-reproducible if the backends disagree on observable behavior. This problem is common in research prototypes and educational interpreters that evolve into VMs: the VM is often treated as an “optimization,” while semantic drift is under-measured. The research objective is to make backend agreement a falsifiable claim with concrete evidence artifacts.

## 2) Research questions

- **RQ1 (Equivalence):** Can SuayLang’s interpreter and bytecode VM be maintained as **observationally equivalent** on a defined subset, and can this be validated automatically with counterexamples?
- **RQ2 (Design proxy):** Do expression-shaped explicit control-flow constructs (`dispatch`, `cycle`) reduce *structural proxy* complexity (tokens, depth, branching) versus a statement-based baseline on selected tasks?

## 3) Hypotheses

### H2 (required)

**H2:** *Interpreter and bytecode VM can be made observationally equivalent on a defined subset, and equivalence can be validated automatically.*

### H1 (optional; proxy-based)

**H1:** *Expression-based explicit control flow reduces local reasoning complexity compared to statement-based control flow on selected tasks.*

H1 is intentionally evaluated only via proxy metrics and is not claimed as a human-subject readability result.

## 4) Success metrics (quantitative)

### H2 metrics

- **Conformance corpora:** total corpus size $M$ (count of `.suay` files) and number of divergences $D$.
- **Differential fuzzing:** program count $N$ (per seed) and number of divergences $D$.

Success for the snapshot requires **$D=0$** for the stated corpora and seed/N settings.

### H1 metrics (proxies)

For each task, compute:

- token count
- approximate AST depth
- branch-point count

Report the table and interpret conservatively (no population claims).

## 5) Falsifiable claim (what would disprove it)

### H2 falsification

H2 is falsified for the evaluated snapshot if any interpreter↔VM divergence is observed under the project’s observation policy:

- different termination class (ok/lex/parse/runtime/internal)
- different stdout (normalized)
- different value (best-effort structural equality)
- different error class or coarse (line, column)

Any printed counterexample produced by the conformance runner constitutes a falsification instance.

### H1 falsification

H1 is falsified (for the selected tasks, under the stated counting rules) if SuayLang systematically increases branch points and/or AST depth relative to the Python baseline.

## 6) Why this matters academically

- **PL semantics:** operational agreement between two evaluators is made testable via observations rather than assumed.
- **PL tooling/testing:** the artifact includes deterministic seeds and raw logs, enabling external replication and audit.
- **VM validation:** emphasizes evidence-producing validation rather than performance claims.

## 7) Alternatives considered and rejected

- **Full formal proof of equivalence:** rejected for v0.1 due to scope/time; replaced with falsifiable observation-based validation.
- **Implementation-independent normative spec first:** rejected for v0.1; the interpreter is treated as the baseline semantics and the VM is validated against it.
- **Large language surface:** rejected; a small VM-supported subset makes counterexamples easier to localize and reduces confounds.

## 8) Threats to validity (at least 6)

- Observation policy may miss some differences (e.g., internal allocation/identity) if not surfaced in value equality.
- Fuzz generator is template-based and may under-sample certain syntactic forms.
- Conformance corpora can overfit to known examples; unseen programs may still diverge.
- Equivalence is only as strong as the subset definition and compiler coverage.
- Performance results are machine-dependent and not a primary correctness metric.
- Proxy metrics for H1 can be sensitive to coding style and do not measure comprehension.

## 9) Limitations

- Equivalence is limited to the VM-supported subset (modules via `link` are interpreter-only in v0.1).
- No human-subject study is included for H1.
- Diagnostic golden tests cover a limited but expanding set of error cases.

## 10) Negative results (explicit)

- **Unicode barrier:** Unicode-first syntax improves concision but can raise tooling/keyboard friction; this is not solved here.
- **VM not always faster:** micro-benchmarks can include programs where the VM is slower (e.g., very small scripts dominated by overhead).

## Pointers to evidence

- H2 results: [docs/research/H2_results.md](H2_results.md)
- Differential testing details: [docs/research/differential_testing.md](differential_testing.md)
- Coverage matrix: [docs/research/coverage_matrix.md](coverage_matrix.md)
- H1 proxy table: [docs/research/H1_metrics.md](H1_metrics.md)
- References: [docs/research/REFERENCES.bib](REFERENCES.bib)
