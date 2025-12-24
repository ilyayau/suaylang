from __future__ import annotations

from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    example = repo / "examples" / "hello.suay"
    if not example.exists():
        print("demo: missing examples/hello.suay")
        return 2

    print("demo: running interpreter")
    from suaylang.cli import main as suay_main

    suay_main([str(example)])

    print("demo: running VM")
    from suaylang.vm_cli import main as vm_main

    vm_main([str(example)])

    print("demo: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
