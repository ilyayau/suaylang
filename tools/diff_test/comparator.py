from __future__ import annotations

import hashlib
import re
from dataclasses import asdict

from .runner import Observation


_WS_RE = re.compile(r"\s+")


def _norm_out(s: str) -> str:
    return s.replace("\r\n", "\n")


def _norm_msg(s: str | None) -> str:
    if not s:
        return ""
    return _WS_RE.sub(" ", s.strip())


def equivalent(a: Observation, b: Observation) -> tuple[bool, str | None]:
    if a.termination != b.termination:
        return False, f"termination differs: interp={a.termination} vm={b.termination}"

    if _norm_out(a.stdout) != _norm_out(b.stdout):
        return False, "stdout differs"

    # stderr is allowed to differ; it is recorded for debugging.

    if a.termination == "ok":
        if a.value_repr != b.value_repr:
            # Best-effort structural equality.
            #
            # Closures and builtins are intentionally opaque values across backends
            # (interpreter and VM use different runtime representations).
            a_has_opaque = bool(a.value_repr) and (
                "Closure" in a.value_repr
                or "ClosureBC" in a.value_repr
                or "Builtin" in a.value_repr
                or "<builtin" in a.value_repr
            )
            b_has_opaque = bool(b.value_repr) and (
                "Closure" in b.value_repr
                or "ClosureBC" in b.value_repr
                or "Builtin" in b.value_repr
                or "<builtin" in b.value_repr
            )
            if a_has_opaque and b_has_opaque:
                return True, None

            return False, f"value differs: interp={a.value_repr} vm={b.value_repr}"
        return True, None

    # For errors/timeouts, compare coarse type and location.
    if (a.error_type or "") != (b.error_type or ""):
        return False, f"error type differs: interp={a.error_type} vm={b.error_type}"

    if (a.line, a.column) != (b.line, b.column):
        return (
            False,
            f"error location differs: interp={a.line}:{a.column} vm={b.line}:{b.column}",
        )

    return True, None


def divergence_fingerprint(
    *,
    source: str,
    interp: Observation,
    vm: Observation,
    category: str,
    size_bucket: str,
) -> str:
    payload = {
        "category": category,
        "size_bucket": size_bucket,
        "source_hash": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "interp": asdict(interp),
        "vm": asdict(vm),
    }
    raw = repr(payload).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]
