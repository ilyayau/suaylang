# Non-Goals

- No concurrency or parallelism (single-threaded only)
- No JIT compilation or runtime code generation
- No static or gradual typing (dynamic only)
- No external FFI/interoperability
- No advanced optimizations (focus is on correctness, not speed)
- No full-featured IDE integration
- No user-facing internationalization/localization

## Rationale
These are out of scope to keep the artifact minimal, scorable, and focused on backend equivalence and diagnostics stability. Each would require additional contracts, metrics, or infrastructure not justified by the current research question.
