from __future__ import annotations

from dataclasses import dataclass

from .comparator import equivalent
from .runner import observe_interpreter, observe_vm


@dataclass(frozen=True)
class MinimizeResult:
    minimized_source: str
    removed_lines: int


def minimize_by_lines(
    *,
    source: str,
    filename: str,
    category: str,
    size_bucket: str,
    timeout_s: float,
) -> MinimizeResult:
    """A simple delta-debugging minimizer.

    Strategy: repeatedly try removing each line; keep the removal if it preserves
    the divergence.
    """

    lines = source.splitlines(True)

    def diverges(src: str) -> bool:
        i = observe_interpreter(src, filename=filename, timeout_s=timeout_s)
        v = observe_vm(src, filename=filename, timeout_s=timeout_s)
        ok, _reason = equivalent(i, v)
        return not ok

    if not diverges(source):
        return MinimizeResult(minimized_source=source, removed_lines=0)

    removed = 0
    changed = True
    while changed and len(lines) > 1:
        changed = False
        for idx in range(len(lines)):
            trial = lines[:idx] + lines[idx + 1 :]
            trial_src = "".join(trial)
            if trial_src.strip() == "":
                continue
            if diverges(trial_src):
                lines = trial
                removed += 1
                changed = True
                break

    return MinimizeResult(minimized_source="".join(lines), removed_lines=removed)
