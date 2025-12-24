# VM invariants (v0.1)

This is a documentation-only list of invariants implied by the current VM implementation (suaylang/vm.py).

## Execution invariants

- Program counter pc is an integer index into code.instrs.
- The VM stops when pc reaches len(code.instrs) (or when HALT-equivalent logic returns in the implementation).
- Stack underflow is a bug; the compiler must emit code that respects stack discipline.

## Environment invariants

- env is always a valid environment object.
- POP_ENV requires env.parent to exist (the VM asserts this).
- PUSH_ENV_BIND expects a dict of bindings; otherwise the VM raises an internal runtime error.

## Determinism invariants

- For a fixed input program and fixed commit, evaluation is deterministic except where host-level nondeterminism is introduced (not part of v0.1 surface contract).
- Diagnostic codes are stable by contract (docs/ERROR_CODES.md).
