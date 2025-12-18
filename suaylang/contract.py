from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .errors import Diagnostic, SuayError
from .runtime import SuayRuntimeError


@dataclass(frozen=True)
class RefTarget:
    path: Path
    anchor: str

    def format(self) -> str:
        return f"{self.path.as_posix()}#{self.anchor}" if self.anchor else self.path.as_posix()


def repo_root() -> Path:
    # suaylang/contract.py -> suaylang -> repo root
    return Path(__file__).resolve().parents[1]


def docs_root() -> Path:
    return repo_root() / "docs"


def reference_root() -> Path:
    # Legacy location kept for older drafts.
    return docs_root() / "reference"


def lookup_ref(topic: str) -> RefTarget:
    t = topic.strip()
    # Error codes
    tu = t.upper()
    if tu.startswith("E-") or tu.startswith("W-"):
        return RefTarget(docs_root() / "ERROR_CODES.md", tu)

    # Operators / keywords
    ops = {
        "dispatch": "6-control-flow-as-expressions",
        "cycle": "6-control-flow-as-expressions",
        "subset": "13-interpretervm-equivalence-requirements",
        "equivalence": "13-interpretervm-equivalence-requirements",
        "operators": "preference-and-associativity",
        "+": "precedence-and-associativity",
        "-": "precedence-and-associativity",
        "*": "precedence-and-associativity",
        "/": "precedence-and-associativity",
        "%": "precedence-and-associativity",
        "ascii": "operator-and-token-mapping",
    }
    if t in ops:
        if t == "operators" or t in {"+", "-", "*", "/", "%"}:
            return RefTarget(reference_root() / "OPERATOR_TABLE.md", ops[t])
        if t == "ascii":
            return RefTarget(docs_root() / "ASCII_SYNTAX.md", "")
        return RefTarget(docs_root() / "LANGUAGE_REFERENCE.md", "")

    # Default to the main reference.
    return RefTarget(docs_root() / "LANGUAGE_REFERENCE.md", "")


def error_code(e: BaseException) -> str | None:
    """Best-effort mapping from current error instances to stable contract codes.

    Contract codes are part of the language contract and are asserted by golden tests.
    We keep this as a mapping layer to avoid silently changing core semantics.
    """

    if isinstance(e, Diagnostic):
        msg = e.message
        if e.error_type == "lexical":
            if msg.startswith("Unknown string escape"):
                return "E-ESC"
            return "E-LEX"
        if e.error_type == "syntax":
            return "E-SYNTAX"
        return None

    if isinstance(e, SuayRuntimeError):
        msg = e.message
        if "division by zero" in msg:
            return "E-DIV0"
        if msg == "Maximum recursion depth exceeded":
            return "E-STACK"
        if msg.startswith("Circular module load detected"):
            return "E-IMPORT-CYCLE"
        if msg.startswith("Cannot load module"):
            return "E-IMPORT"
        if " expects " in msg or msg.startswith("Unary minus expects"):
            return "E-TYPE"
        if msg.startswith("Runtime error for operator") and "division by zero" in msg:
            return "E-DIV0"
        if msg.startswith("Runtime error for operator"):
            return "E-RUNTIME"
        if msg.startswith("Undefined name"):
            return "E-NAME"
        if msg.startswith("Name ") and "already bound" in msg:
            return "E-NAME"
        if msg.startswith("Cannot mutate"):
            return "E-NAME"
        if msg == "No dispatch arm matched":
            return "E-NOMATCH"
        if msg == "No cycle arm matched":
            return "E-NOMATCH"
        return None

    return None


def _format_context_line(ctx: str | None, *, column: int) -> str:
    if ctx is None:
        return ""
    caret = " " * (max(column, 1) - 1) + "^"
    return f"\n{ctx}\n{caret}"


def format_contract_error(e: SuayError, *, include_code: bool) -> str:
    """Stable, contract-mode error formatting.

    We intentionally do not delegate to __str__ here, so golden snapshots can remain
    stable even if default user-facing formatting evolves.
    """

    code = error_code(e) if include_code else None

    if isinstance(e, Diagnostic):
        kind = {
            "lexical": "lex",
            "syntax": "syntax",
        }.get(e.error_type, e.error_type)
        loc = f"{e.line}:{e.column}"
        prefix = f"{e.filename}:{loc}" if e.filename else loc
        head = f"{prefix}: {kind} error: {e.message}"
        if code is not None:
            head = f"{code} {head}"
        return head + _format_context_line(e.context_line, column=e.column)

    if isinstance(e, SuayRuntimeError):
        if e.span is None:
            head = f"runtime error: {e.message}"
            return f"{code} {head}" if code is not None else head

        pos = e.span.start
        loc = f"{pos.line}:{pos.column}"
        prefix = f"{e.filename}:{loc}" if e.filename else loc
        head = f"{prefix}: runtime error: {e.message}"
        if code is not None:
            head = f"{code} {head}"
        ctx = None
        if e.source is not None:
            # Mimic runtime's own context extraction.
            lines = e.source.splitlines()
            if 1 <= pos.line <= len(lines):
                ctx = lines[pos.line - 1]
        out = head + _format_context_line(ctx, column=pos.column)
        if e.frames:
            out += "\nstack:"
            for fr in e.frames:
                fr_pos = fr.span.start
                fr_loc = f"{fr_pos.line}:{fr_pos.column}"
                fr_prefix = f"{e.filename}:{fr_loc}" if e.filename else fr_loc
                out += f"\n- {fr_prefix}: {fr.label}"
        return out

    # Fallback to default formatting.
    s = str(e)
    if code is None:
        return s
    lines = s.splitlines()
    if not lines:
        return f"{code}:"
    lines[0] = f"{code} {lines[0]}"
    return "\n".join(lines)


def format_error(e: SuayError, *, include_code: bool) -> str:
    if not include_code:
        return str(e)
    return format_contract_error(e, include_code=True)
