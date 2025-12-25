# Stack and recursion limits

## Interpreter

- Recursion depth is bounded by the host Python recursion limit.
- Exceeding the bound is a runtime error (code per docs/ERROR_CODES.md).

## VM

- VM has an explicit value stack.
- Stack growth is bounded by available memory; stack overflow is treated as a runtime error.

## Stress tests

- Deep recursion tests should exist under tests/ and be runnable in reproduce-all.
