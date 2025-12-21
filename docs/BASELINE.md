# Baseline Comparison

| System | Programs | Divergences | Coverage (AST/opcode) | Benchmarks | Command |
|--------|----------|-------------|----------------------|------------|---------|
| Interpreter only | 5001 | 0 | 24/20 | 6 | make research |
| Interpreter+VM   | 5001 | 0 | 24/20 | 6 | make research |

- Baseline: Interpreter only (no VM, no diagnostics contract)
- Full system: Interpreter+VM, diagnostics contract enforced
- Metrics: # programs, divergences, coverage, benchmarks
