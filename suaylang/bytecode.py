from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .tokens import Span


@dataclass(frozen=True)
class Instr:
    op: str
    arg: Any = None
    span: Span | None = None


@dataclass
class Code:
    """A minimal bytecode container.

    MVP choices:
    - Instructions carry their arg inline (no constant pool yet).
    - Instructions may carry an optional source span for user-friendly runtime errors.

    Extensible later via:
    - constant pool + index operands
    - separate debug table (pc -> span)
    - locals table
    """

    name: str
    instrs: list[Instr]

    def disassemble(self) -> str:
        lines: list[str] = []
        for pc, ins in enumerate(self.instrs):
            arg = "" if ins.arg is None else _fmt_arg(ins.arg)
            lines.append(f"{pc:04d}  {ins.op}{(' ' + arg) if arg else ''}")
        return "\n".join(lines)


def _fmt_arg(arg: Any) -> str:
    # Keep disassembly compact for closures and nested code objects.
    if isinstance(arg, Code):
        return f"<{arg.name}>"
    if isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], Code):
        code_obj, params = arg
        try:
            nparams = len(params)  # type: ignore[arg-type]
        except Exception:
            nparams = "?"
        return f"(<{code_obj.name}>, params={nparams})"
    return repr(arg)
