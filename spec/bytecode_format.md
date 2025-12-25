# Bytecode format

This document specifies the serialized/logical structure of bytecode used by the VM.

## Logical structure

A bytecode program is a `Code` object containing:

- a list of instructions `(op, arg?, span?)`
- nested `Code` objects for closures

## Serialization

This artifact does not currently commit a stable on-disk serialization format.
The stable contract is the opcode semantics and the compiler-to-VM interface.

If a stable binary format is added later, it must be versioned and declared in spec/backward_compat.md.
