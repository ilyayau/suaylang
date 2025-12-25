# Opcodes (spec)

This table documents the *bytecode VM instruction set* as part of the language artifact.
It is intentionally explicit about stack effects and determinism notes.

Source implementation references:
- docs/BYTECODE.md (overview)
- suaylang/vm.py (execution)
- suaylang/compiler.py (codegen)

## Opcode table

| Opcode | Operands | Stack effect | Memory/Env effect | Determinism notes |
|---|---|---|---|---|
| CONST | value | `[] -> [value]` | none | deterministic |
| POP | – | `[x] -> []` | none | deterministic |
| DUP | – | `[x] -> [x,x]` | none | deterministic |
| HALT | – | `[x] -> (return x)` | none | deterministic |
| JMP | target_pc | `[] -> []` | control-flow only | deterministic |
| JMP_IF_FALSE | target_pc | `[x] -> []` | control-flow based on truthiness | deterministic if truthiness is deterministic |
| JMP_IF_TRUE | target_pc | `[x] -> []` | control-flow based on truthiness | deterministic if truthiness is deterministic |
| TO_BOOL | – | `[x] -> [bool(x)]` | none | deterministic |
| LOAD | name | `[] -> [value]` | reads env | deterministic given env |
| DEF | name | `[v] -> [v]` | defines binding in current env | deterministic |
| SET | name | `[v] -> [v]` | mutates existing binding | deterministic if binding exists; else error |
| PUSH_ENV | – | `[] -> []` | env := child(env) | deterministic |
| POP_ENV | – | `[] -> []` | env := parent(env) | deterministic if parent exists |
| MAKE_TUPLE | n | `[v1..vn] -> [(v1..vn)]` | allocates | deterministic |
| MAKE_LIST | n | `[v1..vn] -> [[v1..vn]]` | allocates | deterministic |
| MAKE_MAP | n | `[k1,v1..kn,vn] -> [map]` | allocates; requires hashable keys | deterministic except raises on unhashable |
| MAKE_VARIANT | tag | `[payload] -> [Variant(tag,payload)]` | allocates | deterministic |
| MAKE_CLOSURE | (code, params) | `[] -> [closure]` | captures env | deterministic given env |
| CALL | – | `[fn,arg] -> [result]` | invokes closure | deterministic if callee is deterministic |
| MATCH | pattern | `[value] -> [bindings_or_None]` | pattern matching only | deterministic |
| JMP_IF_NONE | target_pc | `[x] -> []` (and jumps if `x=None`) | control-flow | deterministic |
| PUSH_ENV_BIND | – | `[bindings] -> []` | env := child(env) with bindings | deterministic |
| RAISE | message | `[] -> (error)` | raises runtime error at span | deterministic |

## Determinism contract

- Any nondeterminism must be declared in spec/determinism.md.
- The shipped artifact pipeline assumes determinism for reproducible hashes.
