# Coverage matrix (construct-level)

This matrix links the supported subset to evidence artifacts: fixed corpora, fuzzing, VM support, interpreter support, and golden diagnostics.

| Construct | In corpus? | In fuzz? | In VM? | In interpreter? | Golden diagnostics? |
|---|:--:|:--:|:--:|:--:|:--:|
| Literals | ✓ | ✓ | ✓ | ✓ | ✓ |
| Names | ✓ | ✓ | ✓ | ✓ | ✓ |
| Binding/Mutation | ✓ | ✓ | ✓ | ✓ | ✓ |
| Blocks | ✓ | — | ✓ | ✓ | ✓ |
| Tuples | ✓ | ✓ | ✓ | ✓ | ✓ |
| Lists | ✓ | ✓ | ✓ | ✓ | ✓ |
| Maps | ✓ | — | ✓ | ✓ | ✓ |
| Variants | ✓ | ✓ | ✓ | ✓ | ✓ |
| Lambda/Closures | ✓ | — | ✓ | ✓ | ✓ |
| Call/Application | ✓ | ✓ | ✓ | ✓ | ✓ |
| Unary ops | — | — | ✓ | ✓ | ✓ |
| Binary ops | ✓ | ✓ | ✓ | ✓ | ✓ |
| Dispatch | ✓ | ✓ | — | ✓ | ✓ |
| Cycle | ✓ | ✓ | — | ✓ | ✓ |
| Modules (link) | — | — | — | ✓ | ✓ |

Golden diagnostic case count: 3
