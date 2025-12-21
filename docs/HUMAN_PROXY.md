# Human-Proxy Metrics for Diagnostics and Readability

This artifact does not claim real user studies or UX superiority. Instead, we report static, machine-computable proxies for human-facing qualities:

- **Token count:** Number of tokens in error messages and programs.
- **Nesting depth:** Maximum AST nesting in programs.
- **Branch count:** Number of pattern branches per match/case.
- **Error-span distance:** Distance between error location and true token.
- **Error code stability:** Rate of error code changes across versions/commits.

## Why machine-only metrics miss UX
- Machine metrics cannot capture user comprehension, frustration, or learning curve.
- Error span precision and code stability are only proxies for real diagnostics quality.
- All results are labeled as proxies and should not be over-claimed as real UX evidence.

See [results/human_proxy.md](../results/human_proxy.md) for metrics and [docs/THREATS_TO_VALIDITY.md](THREATS_TO_VALIDITY.md) for limitations.
