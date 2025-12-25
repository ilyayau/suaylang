# Spec compliance tests

This document defines how to test conformance to the spec.

## Minimum compliance set

- Parser accepts programs defined by spec/grammar.ebnf and rejects those outside it.
- Interpreter and VM agree on observations for the shipped corpora.
- Diagnostics codes and span policies follow docs/ERROR_CODES.md and docs/DIAGNOSTICS_CONTRACT.md.

## How to run

- Fast: `make reproduce-fast`
- Full: `make reproduce-all`

## Artifacts

- Counterexamples: results/diff_report.md + results/diff_report.json
- Integrity: results/manifest.json + results/hashes.txt
