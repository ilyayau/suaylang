# H1 metrics (proxy evidence)

H1 statement (see [docs/research/RESEARCH_CORE.md](RESEARCH_CORE.md)):

> Expression-based explicit control flow reduces local reasoning complexity compared to statement-based control flow on selected tasks.

This repository does **not** claim a human-subject readability result. H1 is evaluated only via structural proxies.

## Task set

The fixed tasks live under:

- `evaluation/h1_tasks/suay/` (SuayLang)
- `evaluation/h1_tasks/python/` (Python baseline)

## Metrics definitions (explicit)

- **Token count**
  - SuayLang: count lexer tokens excluding NEWLINE and EOF.
  - Python: count `tokenize` tokens excluding layout/whitespace tokens.
- **Approx AST depth**
  - SuayLang: maximum structural depth over dataclass fields in the parsed AST.
  - Python: maximum structural depth over `ast` nodes.
- **Branch points**
  - SuayLang: count of `dispatch` arms + `cycle` arms (structural branching sites).
  - Python: count of `if/for/while/match/try/ifexp/boolop` nodes.

## How to reproduce

```sh
python tools/metrics/h1_metrics.py --out docs/research/H1_metrics_table.md
```

## Table

See: [docs/research/H1_metrics_table.md](H1_metrics_table.md)

## Conservative conclusion

On this small task suite, SuayLang’s branch points are often higher than Python’s, largely because `cycle` and `dispatch` make state transitions and case splits explicit and local. This does not refute H1 directly (proxies are not comprehension), but it is a negative signal for the simplistic “fewer branches” proxy.

## Limitations

- Proxy metrics do not measure comprehension, correctness, or maintenance cost.
- Python baselines reflect one possible style; alternative idioms (e.g., `match`) can change the proxy counts.
- AST depth is a structural artifact of the chosen AST representation.
