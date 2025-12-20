# Killer Example: State Machine with Pattern Transitions

This example demonstrates SuayLang’s unique ability to express state machines and pattern-based transitions as first-class expressions.

## Why this is awkward in Python/C
- In Python or C, state machines require explicit loops, switch/case or if/else ladders, and manual state tracking.
- Pattern matching is not first-class; transitions are scattered and error-prone.

## Why it’s natural in SuayLang
- State transitions are encoded as pattern arms in a single expression.
- Each arm can return (<<) or continue (>>) with a new state.
- The entire workflow is a value, not a control structure.

## Example: sum_to_n.suay
```suay
sum_to <- \(n)
    ~~ (Step::(1 0)) |> {
    |> Done::acc     => << acc
    |> Step::(i acc) => >> (
            (i > n) |> {
            |> #t => Done::acc
            |> #f => Step::(i + 1  acc + i)
            }
        )
    }

say . (text . (sum_to . 5))
```

## Expected output
```
sum=15
```

## How to run
```sh
suay run examples/killer/sum_to_n.suay
```
