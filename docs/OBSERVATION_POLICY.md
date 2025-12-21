# Observation Policy (SuayLang)

## Formal Definition

- **Observed:**  
  - Final value (program output)
  - Error kind, code, and span (if error occurs)
  - Standard output (stdout) as produced by the program

- **Ignored:**  
  - Output formatting (whitespace, line endings, pretty-printing)
  - Non-deterministic output (e.g., random seeds, timestamps, unless explicitly fixed)
  - Execution time, memory usage (unless specifically benchmarked)
  - Side effects outside stdout (e.g., file I/O, network)

## False Negatives (What Divergences Can Be Missed)

- Value or error is semantically identical but formatted differently (e.g., “42” vs “ 42\n”)
- Non-deterministic output not controlled by fixed seeds
- Errors that do not propagate to the observation point (e.g., silent internal failures)
- Unchecked side effects (e.g., file writes, network)
- Diagnostic messages that are not part of the observed error contract

## How to Falsify This Claim

A reviewer can falsify the “observational equivalence” claim by producing any of the following, which will be caught by the test harness:

1. **Value Mismatch:**  
   Interpreter and VM produce different final values for the same input.
2. **Error Kind/Code Mismatch:**  
   Interpreter and VM raise different error kinds or codes for the same input.
3. **Error Span Mismatch:**  
   Error occurs at different source locations (span) in interpreter vs VM.
4. **Stdout Mismatch:**  
   Interpreter and VM print different output to stdout (ignoring formatting).
5. **Silent Divergence:**  
   One backend terminates successfully, the other with an error.

**How the harness detects these:**  
- All outputs are normalized and compared after each run.
- Any mismatch in value, error, or stdout is reported as a divergence in results/diff_report.md and results/diff_report.json.
- The test suite includes negative/falsification cases to ensure the harness is not “blind” to real bugs.
