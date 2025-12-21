# If Forced to Cut: Minimal Core Boundary

If required to reduce scope, the following would be cut first:

1. Human-proxy metrics (docs/HUMAN_PROXY.md, results/human_proxy.md)
   - Rationale: Not essential for backend equivalence or diagnostics contract claims.
2. Ablation study (results/ablation.md)
   - Rationale: Valuable for insight, but not core to equivalence claim.
3. Mutation/injection validation (results/mutation_catches.md, results/injection_report.md)
   - Rationale: Strengthens artifact, but not strictly required for main claim.
4. Extended stress tests (tests/stress/)
   - Rationale: Core stress cases would remain, but extended variants could be dropped.
5. Paper PDF (paper/TR-2025-01.pdf)
   - Rationale: Markdown source would suffice for artifact evaluation.

**Minimal core research artifact:**
- Differential test, coverage by construct, golden diagnostics, baseline, and manifest.
