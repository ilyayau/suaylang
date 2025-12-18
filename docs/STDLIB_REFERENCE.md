# Standard Library Reference (v0.1)

## Status

v0.1 ships an *intrinsic* minimal standard library as **builtins** (documented in [docs/STDLIB.md](STDLIB.md)).

A module-based stdlib (`std/core`, `std/collections`, ...) is part of the release plan, but is not shipped in v0.1.

## Builtins (contract)

All builtins are curried by arity.

### IO

- `say . x -> #u` prints `x` (stringified) plus newline.
- `hear . #u -> Text` reads a line from stdin.

### Text / sequences

- `text . x -> Text` converts a value to `Text`.
- `at . xs . i -> value` index `Text`/`List`/`Tuple`.
- `take . xs . n -> xs` prefix.
- `drop . xs . n -> xs` suffix.

### Collections

- `count . x -> Int` length of `Text`/`List`/`Tuple`/`Map`.
- `keys . map -> List` map keys.
- `has . map . key -> Bool` membership.
- `put . map . key . val -> Map` persistent insert/update.

### Higher-order

- `map . f . xs -> List`
- `fold . f . init . xs -> value`

### Math

- `abs . n -> Num`

## Host boundary

v0.1 builtins are implemented by the host runtime (Python) but their behavior is specified at the language level.

Future IO/FS/Path functionality will be introduced via an explicit `std/host` boundary with versioning and stable error codes.
