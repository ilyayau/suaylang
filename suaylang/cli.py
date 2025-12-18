from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from pathlib import Path
from dataclasses import is_dataclass

from .errors import SuayError
from .contract import lookup_ref, format_error
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .runtime import Env, UNIT


def cmd_doctor() -> int:
    """Sanity-check the installation and core execution path.

    This is intentionally small and deterministic: it should work on any machine
    with Python and a functioning install of the package.
    """

    print("SuayLang doctor")
    print(f"python: {sys.version.splitlines()[0]}")
    print(f"python_exe: {sys.executable}")
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


def cmd_run_expr(source: str, *, trace: bool = False) -> int:
    # Treat this as a normal program input; caller controls quoting.
    tokens = Lexer(source, filename="<expr>").tokenize()
    program = Parser(tokens, source, filename="<expr>").parse_program()
    Interpreter(source=source, filename="<expr>", trace=trace).eval_program(program)
    return 0


def cmd_new(project_name: str, *, directory: str | None = None) -> int:
    # Keep this intentionally minimal and non-magical.
    base = Path(directory) if directory else Path.cwd()
    project_dir = base / project_name
    if project_dir.exists():
        _print_err(f"Refusing to overwrite existing path: {project_dir}")
        return 1

    (project_dir / "src").mkdir(parents=True)
    (project_dir / "src" / "main.suay").write_text(
        "total ← fold · (⌁(a b) a + b) · 0 · [10 20]\n"
        'say · ("total=" ⊞ (text · total))\n',
        encoding="utf-8",
    )
    (project_dir / "README.md").write_text(
        "# SuayLang starter project\n\n## Run\n\n```sh\nsuay run src/main.suay\n```\n",
        encoding="utf-8",
    )
    (project_dir / ".gitignore").write_text(".venv/\n__pycache__/\n", encoding="utf-8")

    print(f"Created {project_dir}")
    print("Next:")
    print(f"  cd {project_dir}")
    print("  suay run src/main.suay")
    return 0


def _repl_to_text(v: object) -> str:
    # REPL output formatting is a convenience, not part of language semantics.
    if v is UNIT:
        return "ø"
    if isinstance(v, bool):
        return "⊤" if v else "⊥"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return v
    if isinstance(v, tuple):
        return "(" + " ".join(_repl_to_text(x) for x in v) + ")"
    if isinstance(v, list):
        return "[" + " ".join(_repl_to_text(x) for x in v) + "]"
    if isinstance(v, dict):
        inner = ", ".join(
            f"{_repl_to_text(k)} ↦ {_repl_to_text(val)}" for k, val in v.items()
        )
        return "⟦" + inner + "⟧"
    return str(v)


def cmd_repl(*, trace: bool = False) -> int:
    print("SuayLang REPL (experimental) — Ctrl-D to exit")
    interp = Interpreter(source="", filename="<repl>", trace=trace)
    env = Env(parent=interp._builtins_env)  # intentionally shared across entries

    while True:
        try:
            line = input("suay> ")
        except EOFError:
            print()
            return 0

        if not line.strip():
            continue

        src = line.rstrip("\n") + "\n"
        try:
            tokens = Lexer(src, filename="<repl>").tokenize()
            program = Parser(tokens, src, filename="<repl>").parse_program()
            result: object = UNIT
            for item in program.items:
                result = interp.eval_expr(item, env)
            if result is not UNIT:
                print(_repl_to_text(result))
        except SuayError as e:
            _print_err(str(e))
        except Exception as e:
            _print_err(f"internal error: {type(e).__name__}: {e}")


def cmd_fmt(_: list[str] | None = None) -> int:
    _print_err("suay fmt: not implemented yet (planned)")
    return 2


def cmd_test(*, args: list[str] | None = None) -> int:
    # Convenience wrapper; requires dev dependencies.
    cmd = [sys.executable, "-m", "pytest", "-q"]
    if args:
        cmd.extend(args)
    try:
        proc = subprocess.run(cmd)
        return int(proc.returncode)
    except FileNotFoundError:
        _print_err(
            'pytest is not available. Install dev dependencies: pip install -e ".[dev]"'
        )
        return 1
    except Exception as e:
        _print_err(f"internal error: {type(e).__name__}: {e}")
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="suay", description="SuayLang CLI")
    parser.add_argument(
        "--error-codes",
        action="store_true",
        help="Include stable error codes in diagnostics (contract-mode tooling)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Execute a .suay file (or -e expression)")
    p_run.add_argument("file", nargs="?", help="Path to .suay file")
    p_run.add_argument(
        "-e",
        "--expr",
        dest="expr",
        help="Execute source provided on the command line (one program)",
    )
    p_run.add_argument(
        "--trace", action="store_true", help="Print step-by-step evaluation trace"
    )

    p_check = sub.add_parser("check", help="Lex+parse only; no execution")
    p_check.add_argument("file", help="Path to .suay file")

    p_ast = sub.add_parser("ast", help="Print AST")
    p_ast.add_argument("file", help="Path to .suay file")

    sub.add_parser("doctor", help="Verify installation and run a tiny self-check")

    p_new = sub.add_parser("new", help="Create a starter SuayLang project")
    p_new.add_argument("name", help="Project folder name")
    p_new.add_argument(
        "--dir",
        dest="directory",
        default=None,
        help="Parent directory (default: current directory)",
    )

    p_repl = sub.add_parser("repl", help="Start an interactive REPL (experimental)")
    p_repl.add_argument(
        "--trace", action="store_true", help="Print step-by-step evaluation trace"
    )

    sub.add_parser("fmt", help="Format Suay source (planned; placeholder)")

    p_test = sub.add_parser(
        "test", help="Run the project test suite (requires dev deps)"
    )
    p_test.add_argument("pytest_args", nargs=argparse.REMAINDER)

    p_ref = sub.add_parser("ref", help="Print a reference link for a topic/operator/error")
    p_ref.add_argument("topic", nargs="?", default="", help="Topic, operator, or error code")

    p_explain = sub.add_parser(
        "explain", help="Explain a stable error code from the error catalog"
    )
    p_explain.add_argument("code", help="Error code like E-LEX or E-SYNTAX")

    args = parser.parse_args(argv)

    try:
        if args.cmd == "run":
            if getattr(args, "expr", None):
                if getattr(args, "file", None):
                    _print_err("suay run: provide either a file or -e/--expr, not both")
                    return 2
                return cmd_run_expr(str(args.expr), trace=bool(args.trace))
            if not getattr(args, "file", None):
                _print_err("suay run: missing file (or use -e/--expr)")
                return 2
            return cmd_run(str(args.file), trace=bool(args.trace))
        if args.cmd == "check":
            return cmd_check(args.file)
        if args.cmd == "ast":
            return cmd_ast(args.file)
        if args.cmd == "doctor":
            return cmd_doctor()
        if args.cmd == "new":
            return cmd_new(str(args.name), directory=getattr(args, "directory", None))
        if args.cmd == "repl":
            return cmd_repl(trace=bool(getattr(args, "trace", False)))
        if args.cmd == "fmt":
            return cmd_fmt(None)
        if args.cmd == "test":
            rest = list(getattr(args, "pytest_args", []) or [])
            if rest and rest[0] == "--":
                rest = rest[1:]
            return cmd_test(args=rest)
        if args.cmd == "ref":
            target = lookup_ref(str(getattr(args, "topic", "") or ""))
            print(target.format())
            return 0
        if args.cmd == "explain":
            code = str(getattr(args, "code"))
            catalog = lookup_ref(code).path
            if not catalog.exists():
                _print_err(f"Missing error catalog: {catalog}")
                return 2
            text = catalog.read_text(encoding="utf-8")
            needle = f"## {code.upper()}"
            lines = text.splitlines()
            start = None
            for i, line in enumerate(lines):
                if line.strip().startswith(needle):
                    start = i
                    break
            if start is None:
                _print_err(f"Unknown error code: {code}")
                return 2
            end = len(lines)
            for j in range(start + 1, len(lines)):
                if lines[j].startswith("## "):
                    end = j
                    break
            print("\n".join(lines[start:end]).rstrip())
            return 0
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
        _print_err(format_error(e, include_code=bool(getattr(args, "error_codes", False))))
        return 1
    except Exception as e:
        # Last-resort: keep the CLI user-facing (no raw Python tracebacks).
        _print_err(f"internal error: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
