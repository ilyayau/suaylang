# Module system (status + contract direction)

## Status in v0.1

v0.1 does **not** have a syntax-level module system (`import`/`export`).

The only supported module-loading mechanism is the MVP builtin `link` (interpreter feature):

- `m <- link . "./path/to/mod"`
- `m . "name"` returns the top-level binding `name` from that module

Rules:
- Names beginning with `_` are private and rejected when accessed.
- Circular module loads are rejected.
- Module loads are cached within a single run.

Known limitation:
- The bytecode VM does not implement `link`/modules in v0.1, so module loading is outside the interpreter↔VM conformance subset.

## Error codes

See [docs/ERROR_CODES.md](ERROR_CODES.md).

- `E-IMPORT` for module load failures (file not found / unreadable).
- `E-IMPORT-CYCLE` for circular module load detection.

## Direction (planned)

The release plan targets a v1 module system with:
- imports by module path (e.g. `src/a/b.suay` => `a::b`)
- explicit exports
- specified resolution algorithm
- import cycle diagnostics and VM parity

This section is informational; the contract for the v1 module system will be written once implemented.
