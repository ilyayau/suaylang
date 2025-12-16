# Examples

All examples are runnable from a source checkout after installation.

## Quick run

```sh
suay doctor
suay run examples/hello.suay
```

## Example set (at least 5)

1) Hello / higher-order builtins:
- `examples/hello.suay`

2) Dispatch patterns:
- `examples/committee_02_dispatch.suay`

3) Cycle (state-machine iteration):
- `examples/committee_03_cycle.suay`

4) Modules / `link` (MVP):
- `examples/committee_05_modules.suay`
- supporting modules under `examples/modules/`

5) Errors / diagnostics:
- `examples/committee_04_error.suay`

## Run commands

```sh
suay run examples/committee_02_dispatch.suay
suay run examples/committee_03_cycle.suay
suay run examples/committee_05_modules.suay
suay run examples/committee_04_error.suay  # expected to fail with a user-facing error
```
