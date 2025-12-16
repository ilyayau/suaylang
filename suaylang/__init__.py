"""SuayLang language implementation (lexer, parser, interpreter, VM)."""

from importlib import metadata

try:
    __version__ = metadata.version("suaylang")
except metadata.PackageNotFoundError:  # pragma: no cover
    # Source checkout fallback.
    __version__ = "0.1.0"

from .tokens import Token, TokenType, Position, Span
from .errors import SuayError, Diagnostic
from .lexer import Lexer, LexError
from .parser import Parser, ParseError
from .interpreter import Interpreter, run_source
from .compiler import Compiler
from .vm import VM
from .runtime import SuayRuntimeError
from . import ast

__all__ = [
    "Token",
    "TokenType",
    "Position",
    "Span",
    "SuayError",
    "Diagnostic",
    "Lexer",
    "LexError",
    "Parser",
    "ParseError",
    "Interpreter",
    "run_source",
    "Compiler",
    "VM",
    "SuayRuntimeError",
    "ast",
]
