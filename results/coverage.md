# Coverage report (ci)

- commit: `e67d94e22cc3565de8cc2e928c4c08eb2eeaff36`

## AST node kinds

Observed node kinds: 24

| node_kind | count |
|---|---:|
| Name | 3487 |
| PName | 2213 |
| IntLit | 2057 |
| Binary | 1402 |
| VariantExpr | 1236 |
| Binding | 1195 |
| DispatchArm | 1178 |
| TupleExpr | 957 |
| PVariant | 885 |
| CycleArm | 592 |
| PBool | 592 |
| Dispatch | 589 |
| Program | 588 |
| DecLit | 577 |
| Call | 519 |
| Lambda | 516 |
| MapExpr | 358 |
| BoolLit | 352 |
| ListExpr | 351 |
| UnitLit | 342 |
| PTuple | 297 |
| Cycle | 296 |
| PWildcard | 293 |
| Unary | 93 |

## Opcode kinds (static)

Observed opcode kinds: 20

| opcode | count |
|---|---:|
| POP | 3875 |
| LOAD | 3487 |
| CONST | 3328 |
| DUP | 1770 |
| JMP | 1770 |
| JMP_IF_NONE | 1770 |
| MATCH | 1770 |
| POP_ENV | 1770 |
| PUSH_ENV_BIND | 1770 |
| BINARY | 1402 |
| MAKE_VARIANT | 1236 |
| DEF | 1195 |
| HALT | 1104 |
| MAKE_TUPLE | 957 |
| RAISE | 885 |
| CALL | 519 |
| MAKE_CLOSURE | 516 |
| MAKE_MAP | 358 |
| MAKE_LIST | 351 |
| UNARY | 93 |

## Feature coverage (derived)

This table is derived from AST node counts (best-effort).

| feature | count |
|---|---:|
| binding | 0 |
| block | 0 |
| call | 519 |
| cycle | 296 |
| dispatch | 589 |
| lambda | 516 |
| list | 0 |
| map | 0 |
| mutation | 0 |
| tuple | 0 |
| variant | 0 |
