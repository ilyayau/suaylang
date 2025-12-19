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
import html
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape as _xml_escape


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


def _preprocess_markdown(md: str) -> str:
    """Normalize a few common inputs before parsing.

    - Decode HTML entities (e.g. &bull; -> •).
    - Treat leading "• " as a bullet list marker.
    """

    md = html.unescape(md)
    lines: list[str] = []
    for line in md.splitlines():
        stripped = line.lstrip(" ")
        indent = line[: len(line) - len(stripped)]
        if stripped.startswith("• "):
            lines.append(indent + "- " + stripped[2:])
        else:
            lines.append(line)
    return "\n".join(lines) + ("\n" if md.endswith("\n") else "")


def _render_inline(tokens) -> str:
    """Render markdown-it inline tokens to ReportLab Paragraph markup.

    This intentionally supports a small safe subset: bold, italic, inline code,
    and hard/soft breaks. Unmatched markers are treated as literal by markdown-it.
    """

    parts: list[str] = []

    for tok in tokens:
        t = tok.type
        if t == "text":
            parts.append(_xml_escape(tok.content))
        elif t == "softbreak":
            parts.append(" ")
        elif t == "hardbreak":
            parts.append("<br/>")
        elif t == "code_inline":
            parts.append(f'<font face="Courier">{_xml_escape(tok.content)}</font>')
        elif t == "em_open":
            parts.append("<i>")
        elif t == "em_close":
            parts.append("</i>")
        elif t == "strong_open":
            parts.append("<b>")
        elif t == "strong_close":
            parts.append("</b>")
        else:
            # Conservative fallback: keep content but do not emit unknown markup.
            if getattr(tok, "content", ""):
                parts.append(_xml_escape(tok.content))

    return "".join(parts)


def _md_to_flowables(md: str, *, styles: dict[str, object], style_code) -> list[object]:
    """Parse markdown and return a sequence of ReportLab flowables."""

    try:
        from markdown_it import MarkdownIt
    except Exception as e:
        raise SystemExit(
            "Missing dependency: markdown-it-py. Install dev deps (pip install -e '.[dev]') "
            "or install it directly (pip install markdown-it-py).\n"
            f"Import error: {e}"
        )

    md = _preprocess_markdown(md)
    parser = MarkdownIt("commonmark", {"html": False, "linkify": False, "typographer": False})
    tokens = parser.parse(md)

    Paragraph = styles["Paragraph"]
    Spacer = styles["Spacer"]
    Preformatted = styles["Preformatted"]

    story: list[object] = []

    # We intentionally render list bullets via Paragraph(bulletText=...) to ensure
    # no literal "bull"/"&bull;" ends up in the PDF text stream.
    # (Some PDF extractors/encodings can surface Symbol-font bullets as "bull".)
    @dataclass
    class _ListCtx:
        kind: str  # 'bullet' | 'ordered'
        next_num: int

    @dataclass
    class _ItemCtx:
        flowables: list[object]
        bullet_text: str
        bullet_used: bool
        depth: int

    list_ctx_stack: list[_ListCtx] = []
    item_stack: list[_ItemCtx] = []
    para_inline = None
    current_heading_level: int | None = None
    heading_inline = None

    def _cur_container() -> list[object]:
        return item_stack[-1].flowables if item_stack else story

    def _li_style_for_depth(depth: int):
        base = styles["li"]
        # Create a cheap per-depth derived style (avoid mutating shared style).
        name = f"SuayLI_depth_{depth}"
        try:
            return styles[name]
        except Exception:
            pass
        from reportlab.lib.styles import ParagraphStyle

        left = base.leftIndent + (depth - 1) * 14
        derived = ParagraphStyle(name, parent=base, leftIndent=left, bulletIndent=base.bulletIndent)
        styles[name] = derived
        return derived

    for tok in tokens:
        t = tok.type

        if t == "heading_open":
            current_heading_level = int(tok.tag[1:]) if tok.tag.startswith("h") else 2
            heading_inline = None
            continue
        if t == "heading_close":
            level = current_heading_level or 2
            style = styles["h1"] if level <= 1 else styles["h2"] if level == 2 else styles["h3"]
            inline_text = ""
            if heading_inline is not None:
                inline_text = _render_inline(heading_inline.children or [])
            _cur_container().append(Paragraph(inline_text, style))
            current_heading_level = None
            heading_inline = None
            continue

        if t == "bullet_list_open":
            list_ctx_stack.append(_ListCtx(kind="bullet", next_num=1))
            continue
        if t == "ordered_list_open":
            start_val: int = 1
            if tok.attrs:
                for k, v in tok.attrs:
                    if k == "start":
                        try:
                            start_val = int(v)
                        except Exception:
                            start_val = 1
            list_ctx_stack.append(_ListCtx(kind="ordered", next_num=start_val))
            continue

        if t in ("bullet_list_close", "ordered_list_close"):
            if list_ctx_stack:
                list_ctx_stack.pop()
            continue

        if t == "list_item_open":
            ctx = list_ctx_stack[-1] if list_ctx_stack else _ListCtx(kind="bullet", next_num=1)
            if ctx.kind == "ordered":
                bullet_text = f"{ctx.next_num}."
                ctx.next_num += 1
            else:
                bullet_text = "\u2022"  # •

            item_stack.append(
                _ItemCtx(
                    flowables=[],
                    bullet_text=bullet_text,
                    bullet_used=False,
                    depth=max(1, len(list_ctx_stack)),
                )
            )
            continue
        if t == "list_item_close":
            if not item_stack:
                continue
            finished = item_stack.pop()
            # Ensure at least one flowable so the bullet renders.
            if not finished.flowables:
                li_style = _li_style_for_depth(finished.depth)
                finished.flowables.append(
                    Paragraph("", li_style, bulletText=finished.bullet_text)
                )

            _cur_container().extend(finished.flowables)
            _cur_container().append(Spacer(1, 2))
            continue

        if t == "paragraph_open":
            para_inline = None
            continue
        if t == "paragraph_close":
            if para_inline is None:
                text = ""
            else:
                text = _render_inline(para_inline.children or [])
            if item_stack:
                item = item_stack[-1]
                li_style = _li_style_for_depth(item.depth)
                if not item.bullet_used:
                    item.flowables.append(
                        Paragraph(text, li_style, bulletText=item.bullet_text)
                    )
                    item.bullet_used = True
                else:
                    item.flowables.append(Paragraph(text, li_style))
            else:
                story.append(Paragraph(text, styles["p"]))
            para_inline = None
            continue

        if t == "inline":
            if current_heading_level is not None:
                heading_inline = tok
            else:
                para_inline = tok
            continue

        if t in ("fence", "code_block"):
            code_text = tok.content.rstrip("\n")
            _cur_container().append(Spacer(1, 4))
            _cur_container().append(Preformatted(code_text, style_code))
            _cur_container().append(Spacer(1, 6))
            continue

        if t == "hr":
            _cur_container().append(Spacer(1, 8))
            continue

    return story


def build_pdf(*, md_path: Path, out_path: Path) -> None:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            ListFlowable,
            ListItem,
            Preformatted,
        )
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
    style_li = ParagraphStyle(
        "SuayLI",
        parent=style_p,
        leftIndent=18,
        bulletIndent=6,
        spaceAfter=2,
    )
    style_code = ParagraphStyle(
        "SuayCode",
        parent=base,
        fontName="Courier",
        fontSize=9,
        leading=11,
        textColor=colors.black,
    )

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

    render_api = {
        "Paragraph": Paragraph,
        "Spacer": Spacer,
        "Preformatted": Preformatted,
        "h1": style_h1,
        "h2": style_h2,
        "h3": style_h3,
        "p": style_p,
        "li": style_li,
    }

    story = _md_to_flowables(md, styles=render_api, style_code=style_code)

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
