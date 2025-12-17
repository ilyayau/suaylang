from dataclasses import dataclass


@dataclass(frozen=True)
class Ok:
    x: int


@dataclass(frozen=True)
class Err:
    x: int


def classify(v: object) -> int:
    if isinstance(v, Ok):
        return v.x + 1
    if isinstance(v, Err):
        return v.x + 2
    return 0


_ = classify(Err(41))
