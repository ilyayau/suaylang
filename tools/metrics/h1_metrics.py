from __future__ import annotations

import argparse
import ast as pyast
import io
import tokenize
from dataclasses import dataclass
from pathlib import Path

from suaylang.lexer import Lexer
from suaylang.parser import Parser


@dataclass(frozen=True)
class Metrics:
    tokens: int
    ast_depth: int
    branch_points: int


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _max_depth_obj(obj: object) -> int:
    """Approximate AST depth for SuayLang nodes.

    This is a structural depth over dataclass fields, not a semantic proof artifact.
    """

    from suaylang.ast import Node  # local import to avoid cycles

    seen: set[int] = set()

    def walk(x: object) -> int:
        if x is None:
            return 0
        xid = id(x)
        if xid in seen:
            return 0
        if isinstance(x, Node):
            seen.add(xid)
            child_depths: list[int] = []
            for v in vars(x).values():
                child_depths.append(walk(v))
            return 1 + (max(child_depths) if child_depths else 0)
        if isinstance(x, list):
            return max((walk(i) for i in x), default=0)
        if isinstance(x, tuple):
            return max((walk(i) for i in x), default=0)
        return 0

    return walk(obj)


def _suay_metrics(path: Path) -> Metrics:
    src = _read(path)
    toks = Lexer(src, filename=str(path)).tokenize()
    token_count = sum(1 for t in toks if t.type not in {t.type.EOF, t.type.NEWLINE})
    program = Parser(toks, src, filename=str(path)).parse_program()
    depth = _max_depth_obj(program)

    # Branch points: count pattern-arms in Dispatch/Cycle.
    from suaylang import ast as suayast

    def branch_walk(node: object) -> int:
        if node is None:
            return 0
        if isinstance(node, suayast.Dispatch):
            return len(node.arms) + branch_walk(node.value) + sum(
                branch_walk(a.pattern) + branch_walk(a.expr) for a in node.arms
            )
        if isinstance(node, suayast.Cycle):
            return len(node.arms) + branch_walk(node.seed) + sum(
                branch_walk(a.pattern) + branch_walk(a.expr) for a in node.arms
            )
        if isinstance(node, suayast.Node):
            return sum(branch_walk(v) for v in vars(node).values())
        if isinstance(node, list):
            return sum(branch_walk(v) for v in node)
        if isinstance(node, tuple):
            return sum(branch_walk(v) for v in node)
        return 0

    branches = branch_walk(program)
    return Metrics(tokens=token_count, ast_depth=depth, branch_points=branches)


def _python_metrics(path: Path) -> Metrics:
    src = _read(path)
    token_count = 0
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type in {tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER}:
            continue
        token_count += 1

    tree = pyast.parse(src, filename=str(path))

    def py_depth(n: pyast.AST) -> int:
        child_depths = [py_depth(c) for c in pyast.iter_child_nodes(n)]
        return 1 + (max(child_depths) if child_depths else 0)

    depth = py_depth(tree)

    branch_types = (
        pyast.If,
        pyast.For,
        pyast.While,
        pyast.Match,
        pyast.Try,
        pyast.IfExp,
        pyast.BoolOp,
    )
    branches = sum(1 for _n in pyast.walk(tree) if isinstance(_n, branch_types))
    return Metrics(tokens=token_count, ast_depth=depth, branch_points=branches)


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="h1-metrics",
        description="Compute simple structural metrics for H1 tasks (SuayLang vs Python).",
    )
    ap.add_argument(
        "--root",
        type=str,
        default="evaluation/h1_tasks",
        help="Root directory containing suay/ and python/ subfolders",
    )
    ap.add_argument(
        "--out",
        type=str,
        default="",
        help="Optional path to write a Markdown table (prints to stdout otherwise)",
    )
    args = ap.parse_args()

    root = Path(args.root)
    suay_dir = root / "suay"
    py_dir = root / "python"
    suay_files = sorted(p for p in suay_dir.glob("*.suay") if p.is_file())

    rows: list[tuple[str, Metrics, Metrics]] = []
    for suay_path in suay_files:
        py_path = py_dir / (suay_path.stem + ".py")
        if not py_path.exists():
            raise SystemExit(f"Missing Python baseline for {suay_path.name}: expected {py_path}")
        rows.append((suay_path.stem, _suay_metrics(suay_path), _python_metrics(py_path)))

    lines: list[str] = []
    lines.append("| Task | Suay tokens | Py tokens | Suay depth | Py depth | Suay branch pts | Py branch pts |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for name, sm, pm in rows:
        lines.append(
            f"| {name} | {sm.tokens} | {pm.tokens} | {sm.ast_depth} | {pm.ast_depth} | {sm.branch_points} | {pm.branch_points} |"
        )

    out_text = "\n".join(lines) + "\n"
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_text, encoding="utf-8")
    else:
        print(out_text, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
