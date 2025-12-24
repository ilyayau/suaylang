# Notation

This table fixes terminology and notation used across docs.

| Notation | Meaning |
|---|---|
| $P$ | a SuayLang program (source text) |
| $I(P)$ | observation produced by the interpreter |
| $V(P)$ | observation produced by the VM |
| $\mathcal{O}$ | observation policy (docs/OBSERVATION_POLICY.md) |
| $I(P) \equiv_{\mathcal{O}} V(P)$ | observational equivalence under policy |

Observations are tuples of (termination class, stdout, value-or-error).
