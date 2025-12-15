from __future__ import annotations

import argparse
import platform
import sys
from dataclasses import is_dataclass

from .errors import SuayError
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


def cmd_doctor() -> int:
    """Sanity-check the installation and core execution path.

    This is intentionally small and deterministic: it should work on any machine
    with Python and a functioning install of the package.
    """

    print("SuayLang doctor")
    print(f"python: {sys.version.splitlines()[0]}")
    print(f"platform: {platform.platform()}")

    # Import sanity
    try:
        from . import __version__  # type: ignore
    except Exception:
        __version__ = "(unknown)"  # type: ignore
    print(f"suaylang: {__version__}")

    # End-to-end: lex -> parse -> interpret a tiny program.
    src = 'say · ("doctor:ok")\n'
    try:
        tokens = Lexer(src, filename="<doctor>").tokenize()
        program = Parser(tokens, src, filename="<doctor>").parse_program()
        Interpreter(source=src, filename="<doctor>", trace=False).eval_program(program)
    except SuayError as e:
        _print_err(str(e))
        return 1
    except Exception as e:
        _print_err(f"internal error: {type(e).__name__}: {e}")
        return 1

    print("OK")
    return 0


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _print_err(msg: str) -> None:
    print(msg, file=sys.stderr)


def _format_ast(node: object, *, indent: str = "", is_last: bool = True) -> str:
    branch = "└─ " if is_last else "├─ "
    next_indent = indent + ("   " if is_last else "│  ")

    # Special-case pair tuples used for map entries.
    if isinstance(node, tuple) and len(node) == 2:
        parts: list[str] = [f"{indent}{branch}Entry"]
        parts.append(_format_ast(node[0], indent=next_indent, is_last=False))
        parts.append(_format_ast(node[1], indent=next_indent, is_last=True))
        return "\n".join(parts)

    if not is_dataclass(node):
        return f"{indent}{branch}{node!r}"

    cls = type(node).__name__
    parts: list[str] = [f"{indent}{branch}{cls}"]

    # dataclass fields
    items = list(getattr(node, "__dataclass_fields__").keys())
    # Hide huge source spans by default; keep the info but don’t spam.
    if "span" in items:
        items.remove("span")
        items.append("span")

    for idx, name in enumerate(items):
        val = getattr(node, name)
        last_field = idx == len(items) - 1

        if name == "span":
            s = val
            parts.append(
                f"{next_indent}{'└─ ' if last_field else '├─ '}span {s.start.line}:{s.start.column}..{s.end.line}:{s.end.column}"
            )
            continue

        if isinstance(val, list):
            parts.append(
                f"{next_indent}{'└─ ' if last_field else '├─ '}{name} [{len(val)}]"
            )
            for j, child in enumerate(val):
                parts.append(
                    _format_ast(
                        child,
                        indent=next_indent + ("   " if last_field else "│  "),
                        is_last=(j == len(val) - 1),
                    )
                )
            continue

        if isinstance(val, tuple) and len(val) == 2:
            parts.append(f"{next_indent}{'└─ ' if last_field else '├─ '}{name}")
            parts.append(
                _format_ast(
                    val,
                    indent=next_indent + ("   " if last_field else "│  "),
                    is_last=True,
                )
            )
            continue

        if is_dataclass(val):
            parts.append(f"{next_indent}{'└─ ' if last_field else '├─ '}{name}")
            parts.append(
                _format_ast(
                    val,
                    indent=next_indent + ("   " if last_field else "│  "),
                    is_last=True,
                )
            )
            continue

        parts.append(f"{next_indent}{'└─ ' if last_field else '├─ '}{name} = {val!r}")

    return "\n".join(parts)


def cmd_check(path: str) -> int:
    src = _read_text(path)
    tokens = Lexer(src, filename=path).tokenize()
    Parser(tokens, src, filename=path).parse_program()
    print("OK")
    return 0


def cmd_ast(path: str) -> int:
    src = _read_text(path)
    tokens = Lexer(src, filename=path).tokenize()
    program = Parser(tokens, src, filename=path).parse_program()
    print(_format_ast(program))
    return 0


def cmd_run(path: str, *, trace: bool = False) -> int:
    src = _read_text(path)
    tokens = Lexer(src, filename=path).tokenize()
    program = Parser(tokens, src, filename=path).parse_program()
    Interpreter(source=src, filename=path, trace=trace).eval_program(program)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="suay", description="SuayLang CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Execute a .suay file")
    p_run.add_argument("file", help="Path to .suay file")
    p_run.add_argument(
        "--trace", action="store_true", help="Print step-by-step evaluation trace"
    )

    p_check = sub.add_parser("check", help="Lex+parse only; no execution")
    p_check.add_argument("file", help="Path to .suay file")

    p_ast = sub.add_parser("ast", help="Print AST")
    p_ast.add_argument("file", help="Path to .suay file")

    sub.add_parser("doctor", help="Verify installation and run a tiny self-check")

    args = parser.parse_args(argv)

    try:
        if args.cmd == "run":
            return cmd_run(args.file, trace=bool(args.trace))
        if args.cmd == "check":
            return cmd_check(args.file)
        if args.cmd == "ast":
            return cmd_ast(args.file)
        if args.cmd == "doctor":
            return cmd_doctor()
        _print_err("Unknown command")
        return 2

    except (
        FileNotFoundError,
        PermissionError,
        IsADirectoryError,
        UnicodeDecodeError,
        OSError,
    ) as e:
        _print_err(f"{getattr(args, 'file', '<input>')}: {e}")
        return 1
    except SuayError as e:
        _print_err(str(e))
        return 1
    except Exception as e:
        # Last-resort: keep the CLI user-facing (no raw Python tracebacks).
        _print_err(f"internal error: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
