# Coverage report (ci)

- commit: `ae3e32ee0f9e63f41798de93a2c9de71832d12cb`

## AST node kinds

Observed node kinds: 24

| node_kind | count |
|---|---:|
| Name | 3372 |
| PName | 2141 |
| IntLit | 1954 |
| Binary | 1347 |
| Binding | 1162 |
| VariantExpr | 1158 |
| DispatchArm | 1130 |
| TupleExpr | 888 |
| PVariant | 832 |
| DecLit | 570 |
| Dispatch | 565 |
| Program | 564 |
| CycleArm | 534 |
| PBool | 534 |
| Call | 525 |
| Lambda | 521 |
| BoolLit | 371 |
| UnitLit | 371 |
| MapExpr | 366 |
| ListExpr | 357 |
| PWildcard | 298 |
| PTuple | 268 |
| Cycle | 267 |
| Unary | 92 |

## Opcode kinds (static)

Observed opcode kinds: 20

| opcode | count |
|---|---:|
| POP | 3684 |
| LOAD | 3372 |
| CONST | 3266 |
| DUP | 1664 |
| JMP | 1664 |
| JMP_IF_NONE | 1664 |
| MATCH | 1664 |
| POP_ENV | 1664 |
| PUSH_ENV_BIND | 1664 |
| BINARY | 1347 |
| DEF | 1162 |
| MAKE_VARIANT | 1158 |
| HALT | 1085 |
| MAKE_TUPLE | 888 |
| RAISE | 832 |
| CALL | 525 |
| MAKE_CLOSURE | 521 |
| MAKE_MAP | 366 |
| MAKE_LIST | 357 |
| UNARY | 92 |

## Feature coverage (derived)

This table is derived from AST node counts (best-effort).

| feature | count |
|---|---:|
| binding | 0 |
| block | 0 |
| call | 525 |
| cycle | 267 |
| dispatch | 565 |
| lambda | 521 |
| list | 0 |
| map | 0 |
| mutation | 0 |
| tuple | 0 |
| variant | 0 |
