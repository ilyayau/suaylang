# Limitations

- No concurrency: Only single-threaded execution is supported. Rationale: Focus is on backend equivalence, not parallel semantics.
- No JIT: No just-in-time compilation. Rationale: Ensures deterministic, auditable execution.
- No type inference: Only explicit types or dynamic typing. Rationale: Type system research is out of scope.
- Performance is not a primary goal: Benchmarks are reported, but not optimized. Rationale: Correctness and equivalence take precedence.
- No user-facing language extensions: Only core language features are included. Rationale: Simplicity and auditability.
- No external I/O beyond stdout: To ensure reproducibility and deterministic results.
