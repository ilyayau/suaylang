# Related Work (high-signal, 1-page positioning)

This project treats SuayLang as an **instrument**: a small, explicit-control-flow language used to evaluate falsifiable claims about interpreter↔VM equivalence (H2) and (optionally) structural proxies for local reasoning complexity (H1).

## Expression-oriented control flow / pattern matching

- **Pattern matching compilation:** SuayLang’s `dispatch` is a minimal, expression-shaped match; its design is aligned with decision-tree views of pattern matching (but does not attempt to optimize or generalize the full space).

## Operational semantics (small-step / big-step)

- **Semantics framing:** The interpreter is treated as the baseline operational semantics for v0.1, and equivalence is evaluated observationally against that baseline (rather than asserting a separate, implementation-independent standard).

## Differential testing / compiler fuzzing

- **Differential testing:** H2 evidence is produced via a fixed corpus plus seeded differential fuzzing, following the basic idea that implementation disagreements are counterexamples.

## VM equivalence / testing language implementations

- **Two-backend validation:** The project’s core evaluation loop is interpreter vs VM observation comparison, similar in spirit to compiler-testing work where independent execution paths are compared for disagreements.

## Tooling / diagnostics

- **Diagnostics stability:** Tests include golden diagnostic snapshots to make user-visible errors stable enough to audit and to keep evaluation artifacts reproducible.

## References (5–7)

- G. D. Plotkin, “A Structural Approach to Operational Semantics,” 1981.
- G. Kahn, “Natural Semantics,” 1987.
- L. Maranget, “Compiling Pattern Matching to Good Decision Trees,” 2008.
- W. M. McKeeman, “Differential Testing for Software,” 1998.
- K. Claessen and J. Hughes, “QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs,” 2000.
- X. Yang et al., “Finding and Understanding Bugs in C Compilers,” 2011. (Csmith)
- R. Nystrom, “Crafting Interpreters,” 2021.

