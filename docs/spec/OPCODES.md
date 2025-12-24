# Opcode table (v0.1)

This table is derived from docs/BYTECODE.md and the VM implementation in suaylang/vm.py.

Notation:

- Stack shown as [..., a, b] where b is top.
- Effects are given as before → after.

| Opcode | Arg | Stack effect | Notes |
|---|---|---|---|
| CONST | value | [...] → [..., value] | push literal/host value |
| LOAD | name | [...] → [..., value] | lookup in env chain |
| DEF | name | [..., v] → [..., v] | defines in current env |
| SET | name | [..., v] → [..., v] | mutates existing binding |
| POP | – | [..., v] → [...] | discard |
| DUP | – | [..., v] → [..., v, v] | duplicate top |
| PUSH_ENV | – | [...] → [...] | env := Env(parent=env) |
| POP_ENV | – | [...] → [...] | env := env.parent (must exist) |
| PUSH_ENV_BIND | – | [..., dict] → [...] | pushes new env with bindings |
| MAKE_TUPLE | n | [..., v1..vn] → [..., (v1..vn)] | order preserved |
| MAKE_LIST | n | [..., v1..vn] → [..., [v1..vn]] | order preserved |
| MAKE_MAP | n | [..., k1, v1, ..., kn, vn] → [..., {k→v}] | keys must be hashable |
| MAKE_VARIANT | tag | [..., payload] → [..., Variant(tag,payload)] | tagged value |
| MAKE_CLOSURE | (code, params) | [...] → [..., closure] | captures current env |
| CALL | – | [..., fn, arg] → [..., result] | calls builtin or closure |
| JMP | pc | [...] → [...] | pc := target |
| JMP_IF_FALSE | pc | [..., v] → [...] | pop v; if falsy jump |
| JMP_IF_TRUE | pc | [..., v] → [...] | pop v; if truthy jump |
| TO_BOOL | – | [..., v] → [..., bool] | maps truthiness to bool |
| RAISE | message | [...] → (error) | raises runtime error at span |
