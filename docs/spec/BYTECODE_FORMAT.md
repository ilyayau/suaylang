# Bytecode format (v0.1)

Normative references:

- docs/BYTECODE.md (instruction set description)
- suaylang/bytecode.py and suaylang/vm.py (implementation)

## Model

- Stack-based execution.
- Current lexical environment with parent chain.
- Code is a sequence of instructions; program counter (pc) steps through instrs.

## Instruction representation

Each instruction is conceptually:

- op: string opcode name
- arg: optional argument
- span: optional source span for diagnostics

## Control flow

- Conditional and unconditional jumps update pc.
- Short-circuit semantics compile into jump patterns.
