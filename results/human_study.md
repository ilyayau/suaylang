# Human-facing experiment (proxy) — results

This is a proxy protocol with computed static metrics (not a real participant study).

- commit: `ae3e32ee0f9e63f41798de93a2c9de71832d12cb`
- python: `3.13.11`

## Task-by-task comparison

| task | metric | suay | python |
|---|---|---:|---:|
| classify_variant | loc_nonempty | 8 | 9 |
| classify_variant | token_count | 66 | 76 |
| classify_variant | control_flow_markers | 4 | 2 |
| classify_variant | max_nesting | 2 | 3 |
| map_fold | loc_nonempty | 8 | 7 |
| map_fold | token_count | 69 | 61 |
| map_fold | control_flow_markers | 3 | 1 |
| map_fold | max_nesting | 3 | 3 |
| sum_to | loc_nonempty | 10 | 9 |
| sum_to | token_count | 99 | 51 |
| sum_to | control_flow_markers | 7 | 1 |
| sum_to | max_nesting | 4 | 2 |

## Interpretation (5–10 lines)

Across these micro-tasks, SuayLang often shifts branching/looping into expression forms (`dispatch`/`cycle`).
The proxy is considered supportive when SuayLang achieves comparable or lower token count and control-flow markers without increasing nesting depth.
This does not establish human comprehension; it provides a reproducible, reviewable signal and a concrete task set to recruit participants against later.

Threats to validity: tokenization is approximate; Python idioms vary; static counts do not model reader time/correctness.
