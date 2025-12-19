from __future__ import annotations

import argparse
import os
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
from .formatter import FormatOptions, format_file
from . import __version__


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
    p = Path(path)
    if p.is_dir():
        candidates = [p / "src" / "main.suay", p / "main.suay"]
        entry = next((c for c in candidates if c.exists() and c.is_file()), None)
        if entry is None:
            _print_err(
                "suay run: directory has no entrypoint; expected src/main.suay (or main.suay)"
            )
            return 2
        p = entry
        path = str(p)

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


def cmd_new(
    project_name: str,
    *,
    directory: str | None = None,
    syntax: str = "ascii",
    template: str = "starter",
) -> int:
    # Keep this intentionally minimal and non-magical.
    base = Path(directory) if directory else Path.cwd()
    project_dir = base / project_name
    if project_dir.exists():
        _print_err(f"Refusing to overwrite existing path: {project_dir}")
        return 1

    (project_dir / "src").mkdir(parents=True)
    if syntax not in ("ascii", "unicode"):
        _print_err("suay new: --syntax must be 'ascii' or 'unicode'")
        return 2

    if template not in ("starter", "2d"):
        _print_err("suay new: --template must be 'starter' or '2d'")
        return 2

    if template == "starter":
        if syntax == "unicode":
            main_src = (
                "total ← fold · (⌁(a b) a + b) · 0 · [10 20]\n"
                'say · ("total=" ⊞ (text · total))\n'
            )
        else:
            # ASCII-first starter project.
            main_src = (
                "total <- fold . (\\(a b) a + b) . 0 . [10 20]\n"
                'say . ("total=" ++ (text . total))\n'
            )
    else:
        # Small interactive demo: move a point on a 2D plane.
        if syntax == "unicode":
            main_src = (
                "play ← ⌁(start)\n"
                "  ~~ start |> {\n"
                "  |> Quit::_ => << ø\n"
                "  |> Pos::(x y) => >> {\n"
                '      say · ("pos=(" ⊞ (text · x) ⊞ "," ⊞ (text · y) ⊞ ")")\n'
                '      say · "move: w/a/s/d (or q to quit)"\n'
                "      cmd ← hear · ø\n"
                "      (cmd = \"q\") |> {\n"
                "      |> ⊤ => Quit::ø\n"
                "      |> ⊥ => (cmd = \"w\") |> {\n"
                "          |> ⊤ => Pos::(x  y - 1)\n"
                "          |> ⊥ => (cmd = \"s\") |> {\n"
                "              |> ⊤ => Pos::(x  y + 1)\n"
                "              |> ⊥ => (cmd = \"a\") |> {\n"
                "                  |> ⊤ => Pos::(x - 1  y)\n"
                "                  |> ⊥ => (cmd = \"d\") |> {\n"
                "                      |> ⊤ => Pos::(x + 1  y)\n"
                "                      |> ⊥ => Pos::(x y)\n"
                "                      }\n"
                "                  }\n"
                "              }\n"
                "          }\n"
                "      }\n"
                "    }\n"
                "  }\n"
                "\n"
                "play · (Pos::(0 0))\n"
            )
        else:
            main_src = (
                "play <- \\(start)\n"
                "  ~~ start |> {\n"
                "  |> Quit::_ => << #u\n"
                "  |> Pos::(x y) => >> {\n"
                '      say . ("pos=(" ++ (text . x) ++ "," ++ (text . y) ++ ")")\n'
                '      say . "move: w/a/s/d (or q to quit)"\n'
                "      cmd <- hear . #u\n"
                "      (cmd = \"q\") |> {\n"
                "      |> #t => Quit::#u\n"
                "      |> #f => (cmd = \"w\") |> {\n"
                "          |> #t => Pos::(x  y - 1)\n"
                "          |> #f => (cmd = \"s\") |> {\n"
                "              |> #t => Pos::(x  y + 1)\n"
                "              |> #f => (cmd = \"a\") |> {\n"
                "                  |> #t => Pos::(x - 1  y)\n"
                "                  |> #f => (cmd = \"d\") |> {\n"
                "                      |> #t => Pos::(x + 1  y)\n"
                "                      |> #f => Pos::(x y)\n"
                "                      }\n"
                "                  }\n"
                "              }\n"
                "          }\n"
                "      }\n"
                "    }\n"
                "  }\n"
                "\n"
                "play . (Pos::(0 0))\n"
            )

    (project_dir / "src" / "main.suay").write_text(main_src, encoding="utf-8")
    (project_dir / "README.md").write_text(
        "# SuayLang project\n\n## Run\n\n```sh\nsuay run .\n```\n",
        encoding="utf-8",
    )
    (project_dir / ".gitignore").write_text(".venv/\n__pycache__/\n", encoding="utf-8")

    print(f"Created {project_dir}")
    print("Next:")
    print(f"  cd {project_dir}")
    print("  suay run .")
    return 0


def _repl_to_text(v: object, *, syntax: str) -> str:
    # REPL output formatting is a convenience, not part of language semantics.
    if v is UNIT:
        return "#u" if syntax == "ascii" else "ø"
    if isinstance(v, bool):
        if syntax == "ascii":
            return "#t" if v else "#f"
        return "⊤" if v else "⊥"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return v
    if isinstance(v, tuple):
        return "(" + " ".join(_repl_to_text(x, syntax=syntax) for x in v) + ")"
    if isinstance(v, list):
        return "[" + " ".join(_repl_to_text(x, syntax=syntax) for x in v) + "]"
    if isinstance(v, dict):
        arrow = "->" if syntax == "ascii" else "↦"
        left = "[[" if syntax == "ascii" else "⟦"
        right = "]]" if syntax == "ascii" else "⟧"
        inner = ", ".join(
            f"{_repl_to_text(k, syntax=syntax)} {arrow} {_repl_to_text(val, syntax=syntax)}"
            for k, val in v.items()
        )
        return left + inner + right
    return str(v)


def cmd_repl(*, trace: bool = False, syntax: str = "ascii") -> int:
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
                print(_repl_to_text(result, syntax=syntax))
        except SuayError as e:
            _print_err(str(e))
        except Exception as e:
            _print_err(f"internal error: {type(e).__name__}: {e}")


def cmd_fmt(paths: list[str], *, unicode: bool = False, check: bool = False) -> int:
    if not paths:
        _print_err("suay fmt: missing files")
        return 2

    opts = FormatOptions(unicode=unicode)
    needs_changes: list[str] = []

    for path in paths:
        p = Path(path)
        src = p.read_text(encoding="utf-8")
        formatted = format_file(p, options=opts)
        if formatted != src:
            needs_changes.append(path)
            if not check:
                p.write_text(formatted, encoding="utf-8")

    if check:
        if needs_changes:
            for p in needs_changes:
                _print_err(f"needs formatting: {p}")
            return 1
        return 0

    # In-place mode
    return 0


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
        "--version",
        action="version",
        version=f"suay {__version__}",
        help="Print version and exit",
    )
    parser.add_argument(
        "--error-codes",
        action="store_true",
        help="Include stable error codes in diagnostics (contract-mode tooling)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser(
        "run",
        help="Execute a .suay file (or a project directory) (or -e expression)",
    )
    p_run.add_argument("file", nargs="?", help="Path to .suay file or project directory")
    p_run.add_argument(
        "-e",
        "--expr",
        dest="expr",
        help="Execute source provided on the command line (one program)",
    )
    p_run.add_argument(
        "--trace", action="store_true", help="Print step-by-step evaluation trace"
    )
    p_run.add_argument(
        "--syntax",
        choices=["ascii", "unicode"],
        default=None,
        help="Preferred output syntax (REPL/value printing). Parsing accepts both.",
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
    p_new.add_argument(
        "--template",
        choices=["starter", "2d"],
        default="starter",
        help="Project template (default: starter)",
    )
    p_new.add_argument(
        "--syntax",
        choices=["ascii", "unicode"],
        default="ascii",
        help="Syntax style for generated templates (default: ascii)",
    )

    p_repl = sub.add_parser("repl", help="Start an interactive REPL (experimental)")
    p_repl.add_argument(
        "--trace", action="store_true", help="Print step-by-step evaluation trace"
    )
    p_repl.add_argument(
        "--syntax",
        choices=["ascii", "unicode"],
        default=None,
        help="Preferred output syntax (value printing). Parsing accepts both.",
    )

    p_fmt = sub.add_parser(
        "fmt",
        help="Rewrite Suay source into canonical ASCII (default) or Unicode",
    )
    p_fmt.add_argument("files", nargs="+", help="One or more .suay files")
    p_fmt.add_argument(
        "--syntax",
        choices=["ascii", "unicode"],
        default="ascii",
        help="Output syntax style (default: ascii)",
    )
    p_fmt.add_argument(
        "--unicode",
        action="store_true",
        help="Compatibility flag (equivalent to --syntax unicode)",
    )
    p_fmt.add_argument("--check", action="store_true", help="Check formatting without modifying files")

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

    output_syntax = str(getattr(args, "syntax", None) or os.environ.get("SUAY_OUTPUT_SYNTAX", "ascii"))
    if output_syntax not in ("ascii", "unicode"):
        output_syntax = "ascii"

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
            return cmd_new(
                str(args.name),
                directory=getattr(args, "directory", None),
                syntax=str(getattr(args, "syntax", "ascii")),
                template=str(getattr(args, "template", "starter")),
            )
        if args.cmd == "repl":
            return cmd_repl(trace=bool(getattr(args, "trace", False)), syntax=output_syntax)
        if args.cmd == "fmt":
            syntax = str(getattr(args, "syntax", "ascii"))
            if bool(getattr(args, "unicode", False)):
                syntax = "unicode"
            return cmd_fmt(
                list(getattr(args, "files", []) or []),
                unicode=(syntax == "unicode"),
                check=bool(getattr(args, "check", False)),
            )
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
