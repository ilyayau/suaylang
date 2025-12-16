# Tutorial: hello → workflow demo (≤15 minutes)

This tutorial assumes Python 3.10+.

## 1) Install (2 minutes)

Linux/macOS:

```sh
git clone https://github.com/ilyayau/suaylang
cd suaylang
./scripts/install.sh
suay doctor
```

Windows (PowerShell):

```powershell
git clone https://github.com/ilyayau/suaylang
cd suaylang
./scripts/install.ps1
suay doctor
```

## 2) Hello world (30 seconds)

```sh
suay run examples/hello.suay
```

## 3) Learn the 3 signature constructs (5 minutes)

- Binding: `name ← expr` (ASCII: `<-`)
- Dispatch: `value ▷ ⟪ ... ⟫` (ASCII: `|> { ... }`)
- Cycle: `⟲ seed ▷ ⟪ ... ⟫` (ASCII: `~~ seed |> { ... }`)

If your keyboard can’t easily input Unicode, use the ASCII aliases documented in:

- `docs/syntax_mapping.md`

## 4) Run the workflow state-machine demo (5 minutes)

```sh
suay run demos/workflow_state_machine/main.suay
```

The demo is intentionally small but non-trivial: it models a workflow as explicit states and transitions.

## 5) Validate the implementation (2 minutes)

```sh
pytest -q
python tools/conformance/run.py
python -m tools.conformance.fuzz --seed 0 --n 1000
```

## 6) Run micro-benchmarks (optional)

```sh
make bench
```
