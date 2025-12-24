# Terminology consistency audit

Canonical terms used across docs:

- “interpreter” = reference evaluator
- “VM” = bytecode virtual machine
- “backend” = interpreter or VM
- “observation policy” = docs/OBSERVATION_POLICY.md
- “artifact pipeline” = `make reproduce-all`

Rules:

- Avoid mixing “SuayInterp” vs “Interpreter” in prose; prefer “interpreter”.
- Avoid “bytecode engine” when “VM” is intended.
- Avoid embedding numeric results in narrative docs; link to results/ artifacts.

Audit targets:

- README.md
- docs/TECHREPORT.md
- docs/COMMITTEE_ONEPAGER.md
- docs/RELATED_WORK.md
