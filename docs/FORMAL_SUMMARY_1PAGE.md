# SuayLang: Formal Summary (One Page)

## Syntax Subset
- let x = e
- x := e
- match e with {p -> e}
- while c do e
- state_machine {state, event -> next_state}
- error(code, span)

## Evaluation Judgement
- ⟨e, σ⟩ ⇓ v
- ⟨e, σ⟩ ⇓ error(code, span)

## Equivalence Definition
- Two runs are equivalent if:
  - Same value, or
  - Same (error_code, span category), or
  - Same stdout under normalization

## Observation Policy
- Only value, error (code+span), and stdout are observable.
- Message text and formatting are ignored.
- Non-deterministic output is not allowed.

## Error Model Invariants
- Error codes must be stable across versions.
- Spans must contain the true token location.
- Each error code is unique and contractually enforced.
- Diagnostics are deterministic for a given input and commit.
