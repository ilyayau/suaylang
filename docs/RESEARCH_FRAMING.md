# Research framing (committee-first)

## Short abstract (paper-style)

SuayLang is a research artifact for evaluating backend equivalence between two independent executions of a small language: a reference interpreter and a bytecode VM. The contribution is methodological: it makes the observation policy explicit, maps claims to concrete artifacts and reproduction commands, and emits integrity metadata (hashes) over generated evidence.

## Research question (1 sentence)

Can a reference interpreter and a bytecode VM be made observationally equivalent under a fixed observation policy, and evaluated via a deterministic, artifact-driven protocol?

## Hypothesis (formal, falsifiable)

For the shipped corpora and supported subset, interpreter and VM observations are equivalent under docs/OBSERVATION_POLICY.md.

Falsifiable criteria (any of these falsifies the hypothesis for a given case):

- Termination class differs (`ok|lex|parse|runtime|internal`).
- Stdout differs after newline normalization.
- Returned value differs for `ok` runs.
- Error kind differs; or (line, column) differs where span comparison is required by the protocol.

Where failures are recorded:

- Protocol definition: docs/EXPERIMENT_PROTOCOL.md
- Outputs: results/ (see results/README.md)

## Motivation (research gap)

Equivalence claims for language backends are often presented as narrative statements or ad-hoc tests, which makes committee review and independent reproduction difficult. The gap addressed here is reproducible *evaluation packaging*: a reviewer can run one command, inspect a small set of files, and verify or falsify the claim.

## Novelty (explicit vs prior work)

Compared to randomized testing, property-based testing, and mutation testing, SuayLang’s novelty is the committee-first packaging of equivalence evaluation:

- explicit observation policy,
- claim → evidence → artifact mapping,
- integrity metadata (hashes) and independent reproduction receipts.

See docs/RELATED_WORK.md.

## What fails if the hypothesis is wrong

If the hypothesis is wrong, at least one of the following will occur:

- CI/test gates fail.
- The pipeline produces a counterexample program showing a backend divergence.
- Results artifacts show inconsistent observations under the policy.

Operationally, the expectation is “fail loudly”: the discrepancy is a falsification signal.

## Contributions (C1, C2, C3)

- **C1 (Protocol):** Deterministic, artifact-driven equivalence protocol (`make reproduce-all`) and detailed protocol doc.
- **C2 (Contract):** Observation/diagnostics contract (stable codes, spans, and what is compared).
- **C3 (Packaging):** Evidence map + integrity metadata for committee review and independent reproduction.

## Explicit assumptions

- Primary supported evaluation environment: Linux + Python 3.12.x (CI pins 3.12).
- Programs do not rely on external nondeterministic inputs unless explicitly stated.
- Timing measurements vary across machines; functional observations must not.

## Validity discussion

- Internal validity: strengthened by two independent executions and deterministic reproduction; threatened by shared-design coupling.
- External validity: limited by the supported subset and corpora; strengthened by publishing corpora and saving counterexamples.

## Threat model (methodology-level)

Threats considered are methodological, not adversarial security:

- False positives: comparator too strict (e.g., span comparisons overly constrained).
- False negatives: comparator too permissive (meaningful differences ignored).
- Tooling drift: host/runtime changes alter observations.

See docs/THREATS_TO_VALIDITY.md.

## Limitations

See docs/LIMITATIONS.md.

## Negative results

This repository does not claim negative results in narrative form.

- If divergences are found, they should be recorded as minimized counterexamples and referenced via results/ artifacts.

## Future work (prioritized)

- P0: expand differential testing coverage; store minimized regressions; keep CI bounded.
- P1: maintain a spec–implementation diff log; add machine-readable spec extracts.
- P2: upgrade performance protocol (multi-run stats, platform variance, budgets).

## Ethics statement

See docs/ETHICS.md.

## Japanese research context (short)

In a MEXT-style evaluation setting, reproducibility, clarity of claims, and auditability of evidence are first-class. This artifact is organized around fast reviewer paths (30 seconds / 7 minutes / 15 minutes) and deterministic evidence files.

## Supervisor alignment note

This project is structured for supervisor-style review: the hypothesis is explicitly falsifiable, evidence is deterministic and file-based, and limitations/threats are separated from the main narrative.
