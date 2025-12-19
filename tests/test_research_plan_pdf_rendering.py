from __future__ import annotations

from pathlib import Path


def _extract_pdf_text(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "Missing dependency: pypdf. Install dev deps (pip install -e '.[dev]') "
            "or install it directly (pip install pypdf)."
        ) from e

    reader = PdfReader(str(pdf_path))
    parts: list[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def test_research_plan_pdf_builds_to_temp(tmp_path: Path) -> None:
    from tools.build_research_plan_pdf import build_pdf

    repo_root = Path(__file__).resolve().parents[1]
    md_path = repo_root / "docs" / "RESEARCH_PLAN.md"
    out_path = tmp_path / "RESEARCH_PLAN.pdf"

    build_pdf(md_path=md_path, out_path=out_path)
    assert out_path.exists()
    assert out_path.stat().st_size > 2_000


def test_research_plan_pdf_does_not_leak_raw_markdown(tmp_path: Path) -> None:
    from tools.build_research_plan_pdf import build_pdf

    repo_root = Path(__file__).resolve().parents[1]
    md_path = repo_root / "docs" / "RESEARCH_PLAN.md"
    out_path = tmp_path / "RESEARCH_PLAN.pdf"

    build_pdf(md_path=md_path, out_path=out_path)
    text = _extract_pdf_text(out_path)

    forbidden = ["bull", "&bull", "```", "**", "__"]
    for marker in forbidden:
        assert marker not in text

    # Ensure list bullets render as real bullets.
    bullet_markers = {"\u2022", "•", "\x7f"}
    assert any(
        (line.lstrip()[:1] in bullet_markers) for line in text.splitlines() if line.strip()
    )


def test_research_plan_pdf_contains_expected_content(tmp_path: Path) -> None:
    from tools.build_research_plan_pdf import build_pdf

    repo_root = Path(__file__).resolve().parents[1]
    md_path = repo_root / "docs" / "RESEARCH_PLAN.md"
    out_path = tmp_path / "RESEARCH_PLAN.pdf"

    build_pdf(md_path=md_path, out_path=out_path)
    text = _extract_pdf_text(out_path)

    # Headings / key phrases that should survive rendering.
    assert "Research Plan" in text
    assert "Research Questions" in text
    # Code fences should render without backticks.
    assert "committee" in text.lower() or "protocol" in text.lower()
