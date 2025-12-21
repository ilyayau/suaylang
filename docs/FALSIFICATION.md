# Falsification Scenarios

If any of these occur, our main claim is false.

## 1. Normalization hides semantic differences
- If output normalization causes the diff test to miss a real semantic divergence.
- **Mitigation:** All normalization rules are documented and reviewed; raw outputs are archived.
- **Detection:** Compare raw and normalized outputs for a sample of programs.

## 2. Shared-bug risk between interpreter and VM
- If a bug in shared code causes both backends to fail identically, masking a divergence.
- **Mitigation:** Injected bug tests and mutation harness; code review for shared logic.
- **Detection:** Run mutation/injection suite and check for uncaught faults.

## 3. Generator blind spots
- If the program generator fails to cover a class of programs, missing divergences or contract failures.
- **Mitigation:** Use multiple seeds, program shapes, and manual stress cases.
- **Detection:** Review coverage by construct and add targeted stress tests.
