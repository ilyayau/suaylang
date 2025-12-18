# SuayLang — Minimal Standard Library

SuayLang ships with a tiny set of always-available builtins (curried by arity). These are designed to feel natural with the `.` call operator and the language’s expression-first style.

## IO

- `say . x -> #u`
  - Prints `x` (via `text`) with a newline.
- `hear . prompt -> Text`
  - Prints `prompt` (no extra newline) and reads one line from stdin.
  - Returns `""` on EOF.

## Text

- `text . x -> Text`
  - Converts any value to text.
- `at . xs . i -> value`
  - Index into `Text`, `List`, or `Tuple`.
  - Negative indices are allowed.
  - For `Text`, returns a 1-character `Text`.
- `take . xs . n -> xs`
  - Prefix of `Text` or `List`.
- `drop . xs . n -> xs`
  - Suffix of `Text` or `List`.

## Collections

- `count . x -> Int`
  - Length of `Text`, `List`, `Tuple`, or `Map`.
- `keys . map -> List`
  - Returns map keys in insertion order.
- `has . map . key -> Bool`
  - True if `key` is present in `map`.
- `put . map . key . val -> Map`
  - Returns a new map with `key` set to `val`.

## Higher-order

- `map . f . xs -> List`
  - Applies `f` to each element of `xs`.
- `fold . f . init . xs -> value`
  - Left fold.

## Math

- `abs . n -> Num`
  - Absolute value of a number.

## Notes

- Module loading is provided by a separate builtin: `link . path . name -> value`.
- Most functions raise a user-facing `runtime error` on type mismatches.
