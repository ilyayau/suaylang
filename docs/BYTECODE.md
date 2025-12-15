# SuayLang Bytecode (MVP)

This is a minimal compilation target for SuayLang: a small **stack-based** bytecode and a Python VM.

## Why stack-based?

- SuayLang is expression-oriented; stack VMs map naturally from expression trees.
- Small instruction set, easy to extend.
- Simple to implement and debug (bytecode disassembly is readable).

## Core model

- Execution uses a value stack.
- There is a current lexical environment (`Env`) with a parent chain.
- Blocks create a child environment.
- Lambdas compile into separate `Code` objects and become closures capturing their defining environment.

## Instruction set

Each instruction is `(op, arg?, span?)`.

### Stack / control

- `CONST value` → push a Python value (int/float/str/bool/UNIT/etc.)
- `POP` → pop and discard top
- `DUP` → duplicate top
- `HALT` → stop, return top of stack (or UNIT)

- `JMP target_pc` → unconditional jump
- `JMP_IF_FALSE target_pc` → pop value; if falsy jump
- `JMP_IF_TRUE target_pc` → pop value; if truthy jump
- `TO_BOOL` → pop value; push truthiness as `⊤/⊥` (Python bool)

Truthiness: `ø` is falsey; `⊥` is falsey; everything else is truthy.

### Names / scope

- `LOAD name` → push `env.get(name)`
- `DEF name` → pop value, define in current env, then push value back
- `SET name` → pop value, mutate existing binding in an enclosing env, then push value back

- `PUSH_ENV` → `env = Env(parent=env)`
- `POP_ENV` → `env = env.parent`

### Data

- `MAKE_TUPLE n` → pop `n` values → push tuple
- `MAKE_LIST n` → pop `n` values → push list
- `MAKE_MAP n` → pop `2n` values (k,v pairs) → push dict
- `MAKE_VARIANT tag` → pop payload → push `Variant(tag, payload)`

### Functions

- `MAKE_CLOSURE (code, params)` → push closure capturing current env
- `CALL` → pop arg then func → push result

### Pattern matching (for dispatch/cycle)

- `MATCH pattern` → pop value → push `dict` of bindings or `None`
- `JMP_IF_NONE target_pc` → pop top; if `None` jump, else re-push it
- `PUSH_ENV_BIND` → pop bindings dict → push new env with those bindings

### Errors

- `RAISE message` → raise a `SuayRuntimeError` at this instruction’s span

## AST → bytecode mapping (high level)

- Literals → `CONST`
- `Name` → `LOAD`
- `Binding`/`Mutation` → compile RHS then `DEF`/`SET`
- `Block` → `PUSH_ENV`, compile items (POP between), `POP_ENV`
- Collections → compile elements then `MAKE_*`
- `Unary` → compile rhs then `UNARY`
- `Binary` → compile operands then `BINARY`, except:
  - `∧` and `∨` compile into jumps for correct short-circuit semantics
- `Call` → compile func, compile arg, `CALL`
- `Lambda` → compile body to a new `Code`, then `MAKE_CLOSURE`
- `Dispatch`/`Cycle` → compiled into loops using `MATCH`, `JMP_*`, and env binding ops

## Status

The VM is intentionally minimal but already runs the `examples/hello.suay` style programs (lambdas, calls, list/map/fold, dispatch/cycle, blocks, bindings).
