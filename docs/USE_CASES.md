# Use cases (v0.1)

SuayLang is intentionally small. Its credible impact comes from being a **clear notation for control flow**.

## Use case 1: State-machine workflows

When a problem is naturally a finite-state process (approval flows, protocol handshakes, ETL stages), SuayLang’s `cycle` + `dispatch` makes the state transitions explicit:

- the loop state is a value
- each step is a pattern match
- termination is explicit (`↩` continue / `↯` finish)

This reduces “hidden” loop control and makes workflow logic easy to review.

See demo:

- `demos/workflow_state_machine/`

## Use case 2: Safe, readable automation scripts

For small automation scripts where correctness and reviewability matter more than ecosystem breadth:

- explicit binding vs mutation (`←` vs `⇐`) makes state changes obvious
- expression-oriented style keeps control flow composable
- a strict error model with spans and no Python tracebacks improves UX in teaching/review settings

This is a narrow niche: **reviewable scripts** rather than general-purpose application development.
