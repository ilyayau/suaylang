# Research Contributions

1. **Novelty (language / semantics / execution model)**

   SuayLang uses an explicit, expression-level control model centered on `dispatch` (pattern-based branching over values, including variants) and `cycle` (an explicit state-machine loop with `continue`/`finish` arm modes).

   Artifact: the frozen scope statement and examples in [docs/research/semantic_scope.md](docs/research/semantic_scope.md) and [docs/REFERENCE_SHEET.md](docs/REFERENCE_SHEET.md).

2. **Validation approach (how it is evaluated)**

   The bytecode VM is validated against the reference interpreter by differential testing:
   - a deterministic conformance corpus runner, and
   - a seeded differential fuzz runner that compares termination, stdout, result values, and coarse error location.

   Artifacts: [tools/conformance/run.py](tools/conformance/run.py), [tools/conformance/fuzz_runner.py](tools/conformance/fuzz_runner.py), and the comparison policy in [suaylang/conformance.py](suaylang/conformance.py).

3. **Measured result (what is observed)**

   For the VM-supported subset exercised by the harness, the project reports:
   - $N=5000$ fuzz-generated programs at seed 0 with **0 divergences** (interpreter vs VM), and
   - a small micro-benchmark table reporting relative performance and instruction counts (interpreter vs VM only).

   Artifacts: [docs/research/differential_testing.md](docs/research/differential_testing.md) and [benchmarks/results.md](benchmarks/results.md).
