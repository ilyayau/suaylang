# Micro-benchmarks (SuayLang v0.1)

This document defines a conservative micro-benchmark methodology for SuayLang.
It intentionally avoids hype and cross-language performance claims.

## Goal

Measure relative performance between:
- the reference interpreter, and
- the bytecode compiler + VM,

on small, explainable programs that stress the language’s distinctive features.

## Non-goals

- No cross-language speed comparisons.
- No claims about “fastest” or “production-ready performance.”
- No attempt to model real-world workloads.

## Benchmark categories

Benchmarks are grouped under:
- benchmarks/dispatch/ — dispatch-heavy programs
- benchmarks/cycle/ — cycle-heavy state machines
- benchmarks/calls/ — function-call-heavy programs
- benchmarks/mixed/ — mixed control-flow and calls

## Measurement procedure

Runner:
- scripts/bench_micro.py

Principles:
- parse once for execution timings
- redirect stdout/stderr during timing to avoid I/O dominance
- warm up before measuring
- report median/min/max across many iterations

## Reporting

Report per benchmark:
- interpreter timing (ms)
- VM timing (ms)
- ratio (interp / vm)

Example table (placeholder):

| Benchmark | Interp median (ms) | VM median (ms) | Ratio (interp/vm) | Notes |
|---|---:|---:|---:|---|
| dispatch/dispatch_chain.suay | (run script) | (run script) | (computed) | |

## Limitations

- Results are environment-specific (CPU, Python version, OS).
- Micro-benchmarks can be gamed; this suite is intentionally small and interpretable.
- VM coverage limitations apply (benchmarks must stay within the VM-supported subset).
