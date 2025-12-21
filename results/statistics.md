# Aggregated Statistics

## Baseline Timings (Python, Interpreter, VM)
| Program        | Python (s) | Interpreter (s) | VM (s) |
|---------------|------------|-----------------|--------|
| fib           | 0.0222     | 0.1567          | 0.1406 |
| map_fold      | 0.0261     | 0.1433          | 0.1348 |
| oob_error     | 0.0186     | 0.1428          | 0.1268 |
| sum_to_n      | 0.0244     | 0.1544          | 0.1440 |
| variant_match | 0.0224     | 0.1510          | 0.1454 |

## Aggregates
- Mean (Python): 0.0227 s
- Median (Python): 0.0222 s
- Std (Python): 0.0027 s
- Min/Max (Python): 0.0186 / 0.0261 s
- Mean (Interpreter): 0.1492 s
- Median (Interpreter): 0.1510 s
- Std (Interpreter): 0.0060 s
- Min/Max (Interpreter): 0.1428 / 0.1567 s
- Mean (VM): 0.1383 s
- Median (VM): 0.1406 s
- Std (VM): 0.0072 s
- Min/Max (VM): 0.1268 / 0.1454 s

## 95% CI (bootstrap, n=5)
- Python: [0.0186, 0.0261]
- Interpreter: [0.1428, 0.1567]
- VM: [0.1268, 0.1454]

## Source
- Raw samples: [results/baseline_raw.json](baseline_raw.json)
- Summary: [results/baseline_summary.md](baseline_summary.md)
