from __future__ import annotations

from dataclasses import dataclass

from .errors import SuayError
from .tokens import Span


# -------- Values --------


@dataclass(frozen=True)
class Unit:
    pass


UNIT = Unit()


@dataclass(frozen=True)
class Variant:
    tag: str
    payload: object


@dataclass(frozen=True)
class Closure:
    params: list[object]  # ast.Pattern
    body: object  # ast.Expr
    env: "Env"
    name: str | None = None


@dataclass(frozen=True)
class Builtin:
    name: str
    arity: int
    impl: object  # callable
    bound: tuple[object, ...] = ()

    def apply(self, arg: object) -> "Builtin | object":
        new_bound = (*self.bound, arg)
        if len(new_bound) < self.arity:
            return Builtin(name=self.name, arity=self.arity, impl=self.impl, bound=new_bound)
        if len(new_bound) > self.arity:
            raise ValueError("Builtin over-applied")
        return self.impl(*new_bound)


# -------- Environment --------


@dataclass
class Env:
    parent: "Env | None" = None

    def __post_init__(self) -> None:
        self._values: dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        if name in self._values:
            raise KeyError(name)
        self._values[name] = value

    def set_existing(self, name: str, value: object) -> None:
        env = self._find_env_containing(name)
        if env is None:
            raise KeyError(name)
        env._values[name] = value

    def get(self, name: str) -> object:
        if name in self._values:
            return self._values[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise KeyError(name)

    def get_local(self, name: str) -> object:
        if name in self._values:
            return self._values[name]
        raise KeyError(name)

    def keys_local(self) -> list[str]:
        return list(self._values.keys())

    def _find_env_containing(self, name: str) -> "Env | None":
        if name in self._values:
            return self
        if self.parent is not None:
            return self.parent._find_env_containing(name)
        return None


# -------- Runtime Errors --------


@dataclass(frozen=True)
class StackFrame:
    label: str
    span: Span


class SuayRuntimeError(SuayError):
    def __init__(
        self,
        message: str,
        *,
        span: Span | None = None,
        frames: list[StackFrame] | None = None,
        source: str | None = None,
        filename: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.span = span
        self.frames = frames or []
        self.source = source
        self.filename = filename

    def with_frame(self, frame: StackFrame) -> "SuayRuntimeError":
        return SuayRuntimeError(
            self.message,
            span=self.span,
            frames=[frame, *self.frames],
            source=self.source,
            filename=self.filename,
        )

    def with_location(self, *, span: Span | None = None, source: str | None = None, filename: str | None = None) -> "SuayRuntimeError":
        """Fill in missing location information, without overwriting existing details."""
        return SuayRuntimeError(
            self.message,
            span=self.span or span,
            frames=self.frames,
            source=self.source or source,
            filename=self.filename or filename,
        )

    def __str__(self) -> str:
        parts: list[str] = []
        parts.append(self._format_primary())
        if self.frames:
            parts.append("stack:")
            for fr in self.frames:
                parts.append(self._format_frame(fr))
        return "\n".join(parts)

    def _format_primary(self) -> str:
        if self.span is None:
            return f"runtime error: {self.message}"
        pos = self.span.start
        loc = f"{pos.line}:{pos.column}"
        prefix = f"{self.filename}:{loc}" if self.filename else loc
        out = f"{prefix}: runtime error: {self.message}"
        line_text = self._line_text(pos.line)
        if line_text is not None:
            caret = " " * (max(pos.column, 1) - 1) + "^"
            out += f"\n{line_text}\n{caret}"
        return out

    def _format_frame(self, fr: StackFrame) -> str:
        pos = fr.span.start
        loc = f"{pos.line}:{pos.column}"
        prefix = f"{self.filename}:{loc}" if self.filename else loc
        return f"- {prefix}: {fr.label}"

    def _line_text(self, line: int) -> str | None:
        if self.source is None:
            return None
        if line <= 0:
            return None
        i = 1
        start = 0
        while i < line and start < len(self.source):
            nl = self.source.find("\n", start)
            if nl == -1:
                return None
            start = nl + 1
            i += 1
        end = self.source.find("\n", start)
        if end == -1:
            end = len(self.source)
        return self.source[start:end]
