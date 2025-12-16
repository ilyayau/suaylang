from __future__ import annotations


def main() -> int:
    """Conformance runner (scaffold).

    TODO: Implement interpreter↔VM observational equivalence runner.

    Planned responsibilities:
    - load a shared corpus of .suay programs
    - execute each program via interpreter and via compiled VM
    - compare observations (stdout, termination kind, error category/span)
    - emit a minimal, reviewer-friendly summary

    This file is intentionally a stub in the initial research scaffolding.
    """

    raise NotImplementedError("TODO: implement conformance runner")


if __name__ == "__main__":
    raise SystemExit(main())
