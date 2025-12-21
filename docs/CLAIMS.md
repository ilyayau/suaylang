# Claim → Evidence Mapping

| Claim ID | Claim Statement | Metric Definition | Command to Reproduce | Output Artifact | Link |
|----------|-----------------|------------------|----------------------|-----------------|------|
| C1 | Interpreter and VM executions are observationally equivalent | # divergences in diff test | make diff-test | results/diff_report.md | [diff_report.md](../results/diff_report.md) |
| C2 | Diagnostics contract is enforced | # golden diagnostics matches | make golden | results/golden_diagnostics.md | [golden_diagnostics.md](../results/golden_diagnostics.md) |
| C3 | Coverage by construct is complete | # AST/opcode kinds covered | make research | results/coverage.md | [coverage.md](../results/coverage.md) |
| C4 | Baseline and ablation are evidenced | Baseline/ablation metrics | make research | results/baseline.md, results/ablation.md | [baseline.md](../results/baseline.md), [ablation.md](../results/ablation.md) |
| C5 | All results are reproducible | All outputs match on rerun | make reproduce | results/*, paper/suaylang-tech-report.pdf | [results/](../results/README.md) |
