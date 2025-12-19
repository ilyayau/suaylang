#!/usr/bin/env python3
"""Build docs/RESEARCH_PLAN.pdf from docs/RESEARCH_PLAN.md.

Design goals:
- No LaTeX dependency.
- Deterministic, simple layout suitable for committee review.
- Markdown is the single source of truth.

Requires: reportlab
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


def _git_last_commit_and_epoch(paths: list[Path]) -> tuple[str, int] | None:
    """Return (commit_hash, commit_epoch) for the most recent commit touching any path.

    We intentionally base metadata on *source* inputs (e.g. the markdown), not HEAD.
    This prevents an infinite loop where embedding the commit hash causes the PDF
    to differ, which changes the commit hash, etc.
    """

    try:
        cmd = ["git", "log", "-1", "--format=%H%n%ct", "--"] + [str(p) for p in paths]
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode("utf-8")
        lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
        if len(lines) < 2:
            return None
        return (lines[0], int(lines[1]))
    except Exception:
        return None


def _utc_date_from_epoch(epoch: int) -> str:
    return _dt.datetime.fromtimestamp(epoch, tz=_dt.timezone.utc).strftime("%Y-%m-%d")


@dataclass(frozen=True)
class BuildMeta:
    commit: str
    date_utc: str


_CODE_FENCE_RE = re.compile(r"^```")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_BULLET_RE = re.compile(r"^\s*[-*]\s+(.*)$")


def _parse_markdown(md: str) -> list[tuple[str, str]]:
    """Return a list of (kind, text) blocks.

    kind ∈ {h1,h2,h3,p,li,codeblank,code}
    """

    blocks: list[tuple[str, str]] = []
    in_code = False

    for raw_line in md.splitlines():
        line = raw_line.rstrip("\n")

        if _CODE_FENCE_RE.match(line.strip()):
            in_code = not in_code
            continue

        if in_code:
            if line.strip() == "":
                blocks.append(("codeblank", ""))
            else:
                blocks.append(("code", line))
            continue

        if line.strip() == "":
            blocks.append(("p", ""))
            continue

        m = _HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            if level == 1:
                blocks.append(("h1", text))
            elif level == 2:
                blocks.append(("h2", text))
            else:
                blocks.append(("h3", text))
            continue

        m = _BULLET_RE.match(line)
        if m:
            blocks.append(("li", m.group(1).strip()))
            continue

        blocks.append(("p", line.strip()))

    return blocks


def build_pdf(*, md_path: Path, out_path: Path) -> None:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Preformatted
        from reportlab.lib import colors
        from reportlab.pdfgen.canvas import Canvas
    except Exception as e:
        raise SystemExit(
            "Missing dependency: reportlab. Install dev deps (pip install -e '.[dev]') "
            "or install it directly (pip install reportlab).\n"
            f"Import error: {e}"
        )

    source_meta = _git_last_commit_and_epoch([md_path])
    if source_meta is None:
        source_commit = "unknown"
        source_epoch = 946684800  # 2000-01-01 UTC (ReportLab's own invariant default)
    else:
        source_commit, source_epoch = source_meta

    # Make the build reproducible across machines/runs by pinning PDF metadata
    # timestamps (CreationDate/ModDate) via ReportLab's SOURCE_DATE_EPOCH hook.
    os.environ.setdefault("SOURCE_DATE_EPOCH", str(source_epoch))

    md = md_path.read_text(encoding="utf-8")
    meta = BuildMeta(commit=source_commit, date_utc=_utc_date_from_epoch(source_epoch))

    styles = getSampleStyleSheet()
    base = styles["Normal"]

    style_h1 = ParagraphStyle(
        "SuayH1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=19,
        spaceAfter=10,
    )
    style_h2 = ParagraphStyle(
        "SuayH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=14,
        spaceBefore=10,
        spaceAfter=6,
    )
    style_h3 = ParagraphStyle(
        "SuayH3",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        spaceBefore=8,
        spaceAfter=4,
    )
    style_p = ParagraphStyle(
        "SuayP",
        parent=base,
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        spaceAfter=4,
    )
    style_code = ParagraphStyle(
        "SuayCode",
        parent=base,
        fontName="Courier",
        fontSize=9,
        leading=11,
        textColor=colors.black,
    )

    # Minimal inline formatting: turn `code` into <font face="Courier">code</font>
    def fmt_inline(text: str) -> str:
        def repl(m: re.Match[str]) -> str:
            inner = m.group(1)
            inner = inner.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            return f'<font face="Courier">{inner}</font>'

        # Escape first, then unescape code spans via repl.
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return re.sub(r"`([^`]+)`", repl, escaped)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        leftMargin=0.9 * inch,
        rightMargin=0.9 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.75 * inch,
        title="SuayLang Research Plan",
    )

    class InvariantCanvas(Canvas):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault("invariant", 1)
            # Avoid zlib/version noise; file is small anyway.
            kwargs.setdefault("pageCompression", 0)
            super().__init__(*args, **kwargs)

    story: list[object] = []

    blocks = _parse_markdown(md)

    pending_list: list[ListItem] = []
    pending_code_lines: list[str] = []

    def flush_list() -> None:
        nonlocal pending_list
        if not pending_list:
            return
        story.append(
            ListFlowable(
                pending_list,
                bulletType="bullet",
                start="bullet",
                leftIndent=14,
                bulletFontName="Helvetica",
                bulletFontSize=9,
            )
        )
        story.append(Spacer(1, 4))
        pending_list = []

    def flush_code() -> None:
        nonlocal pending_code_lines
        if not pending_code_lines:
            return
        story.append(Spacer(1, 4))
        story.append(Preformatted("\n".join(pending_code_lines), style_code))
        story.append(Spacer(1, 6))
        pending_code_lines = []

    for kind, text in blocks:
        if kind != "li":
            flush_list()
        if kind not in ("code", "codeblank"):
            flush_code()

        if kind == "h1":
            story.append(Paragraph(fmt_inline(text), style_h1))
        elif kind == "h2":
            story.append(Paragraph(fmt_inline(text), style_h2))
        elif kind == "h3":
            story.append(Paragraph(fmt_inline(text), style_h3))
        elif kind == "li":
            pending_list.append(ListItem(Paragraph(fmt_inline(text), style_p)))
        elif kind == "code":
            pending_code_lines.append(text)
        elif kind == "codeblank":
            pending_code_lines.append("")
        else:  # paragraph
            if text.strip() == "":
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph(fmt_inline(text), style_p))

    flush_list()
    flush_code()

    def on_page(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        footer = f"SuayLang Research Plan — commit {meta.commit[:12]} — {meta.date_utc} (UTC)"
        canvas.drawString(doc.leftMargin, 0.5 * inch, footer)
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page, canvasmaker=InvariantCanvas)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build docs/RESEARCH_PLAN.pdf from docs/RESEARCH_PLAN.md")
    parser.add_argument(
        "--in",
        dest="in_path",
        default="docs/RESEARCH_PLAN.md",
        help="Input markdown path (default: docs/RESEARCH_PLAN.md)",
    )
    parser.add_argument(
        "--out",
        dest="out_path",
        default="docs/RESEARCH_PLAN.pdf",
        help="Output PDF path (default: docs/RESEARCH_PLAN.pdf)",
    )
    args = parser.parse_args(argv)

    md_path = Path(str(args.in_path))
    out_path = Path(str(args.out_path))

    if not md_path.exists():
        raise SystemExit(f"Missing input markdown: {md_path}")

    build_pdf(md_path=md_path, out_path=out_path)

    if not out_path.exists() or out_path.stat().st_size < 1024:
        raise SystemExit(f"PDF build failed or produced an empty file: {out_path}")

    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
