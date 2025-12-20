# Baseline Results

This file contains the results of running the baseline suite for SuayLang (interpreter and VM) and Python. The suite consists of small, deterministic programs for direct, measurable comparison.

- **How to reproduce:**
	- Run: `python experiments/baseline_runner.py`
	- Results are written to `results/baseline_raw.json` (full data) and `results/baseline.md` (table)

- **Metrics:**
	- Median runtime (seconds, N=5)
	- Diagnostics (stdout/stderr, exit code)
	- Environment metadata (Python version, OS, CPU, commit hash)

- **Programs:**
	- sum_to_n
	- fib
	- map_fold
	- oob_error
	- variant_match (SuayLang only)

---

## Results Table

See the table below for the latest measured results. For full details, see `baseline_raw.json`.

| Name         | Python (s) | SuayInterp (s) | SuayVM (s) |
|--------------|------------|---------------|-----------|
| sum_to_n     | ...        | ...           | ...       |
| fib          | ...        | ...           | ...       |
| map_fold     | ...        | ...           | ...       |
| oob_error    | ...        | ...           | ...       |
| variant_match| -          | ...           | ...       |

---

- **Note:** Replace `...` with actual numbers after running the runner.
- **Diagnostics and full output:** See `baseline_raw.json`.
- Implement baseline runner or table generator.
- Update this file with real numbers from results/ or scripts.
- Link from README and results/README.md.
