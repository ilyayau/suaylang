# Coverage report (ci)

- commit: `4234c44ddc148f009e738402c684135de7e2e497`

## AST node kinds

Observed node kinds: 24

| node_kind | count |
|---|---:|
| Name | 3442 |
| PName | 2249 |
| IntLit | 2037 |
| Binary | 1397 |
| VariantExpr | 1215 |
| Binding | 1172 |
| DispatchArm | 1146 |
| TupleExpr | 930 |
| PVariant | 856 |
| DecLit | 589 |
| Dispatch | 573 |
| Program | 572 |
| CycleArm | 566 |
| PBool | 566 |
| Lambda | 555 |
| Call | 508 |
| MapExpr | 379 |
| BoolLit | 367 |
| UnitLit | 347 |
| ListExpr | 335 |
| PWildcard | 290 |
| PTuple | 284 |
| Cycle | 283 |
| Unary | 91 |

## Opcode kinds (static)

Observed opcode kinds: 20

| opcode | count |
|---|---:|
| POP | 3751 |
| LOAD | 3442 |
| CONST | 3340 |
| DUP | 1712 |
| JMP | 1712 |
| JMP_IF_NONE | 1712 |
| MATCH | 1712 |
| POP_ENV | 1712 |
| PUSH_ENV_BIND | 1712 |
| BINARY | 1397 |
| MAKE_VARIANT | 1215 |
| DEF | 1172 |
| HALT | 1127 |
| MAKE_TUPLE | 930 |
| RAISE | 856 |
| MAKE_CLOSURE | 555 |
| CALL | 508 |
| MAKE_MAP | 379 |
| MAKE_LIST | 335 |
| UNARY | 91 |

## Feature coverage (derived)

This table is derived from AST node counts (best-effort).

| feature | count |
|---|---:|
| binding | 0 |
| block | 0 |
| call | 508 |
| cycle | 283 |
| dispatch | 573 |
| lambda | 555 |
| list | 0 |
| map | 0 |
| mutation | 0 |
| tuple | 0 |
| variant | 0 |
