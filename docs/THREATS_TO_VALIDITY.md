# Threats to Validity

- **Generator bias:** The seeded program generator may not cover all edge cases or may overfit to shared bugs.
- **Shared-bug risk:** Interpreter and VM may share code or logic, masking divergences.
- **Benchmark representativeness:** Microbenchmarks may not reflect real-world usage or stress cases.
- **Normalization masking:** Output normalization may hide subtle differences.
- **Human-proxy limitations:** Static metrics may not fully capture user experience or real diagnostics quality.

## Mitigations
- Use multiple seeds and program shapes for generator.
- Differential testing with golden diagnostics and injected faults.
- Explicitly report coverage by construct and mutation catch rate.
- Document normalization policy and its limits.
- Label all human-proxy metrics as such and do not over-claim.
