# Undefined behavior (UB)

This list is explicit: when UB occurs, the implementation may raise an error or behave inconsistently.

## Current UB list

- Using host-dependent floating-point edge cases as a semantic claim (NaN payloads, signaling NaNs).
- Relying on map iteration order as a semantic observable.

## Non-UB (defined to error)

- Unhashable map key: defined to raise a runtime error (code per docs/ERROR_CODES.md).
- Name mutation of unbound variable: defined to raise a runtime error.
