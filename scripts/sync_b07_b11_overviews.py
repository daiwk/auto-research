#!/usr/bin/env python3
"""Add the completed B07 foundation batch to the reproduction overview."""

from pathlib import Path

from auto_research.historical_b07_b11 import PAPERS


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs/reproductions/README.md"
START = "<!-- historical-b07:start -->"
END = "<!-- historical-b07:end -->"


def _replace_block(text: str, start: str, end: str, block: str, anchor: str) -> str:
    if start in text:
        before, rest = text.split(start, 1)
        _, after = rest.split(end, 1)
        return before + block + after.lstrip("\n")
    return text.replace(anchor, block + anchor)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    text = text.replace("253 个 adapter", "262 个 adapter")
    text = text.replace("## 全部复现（253/253）", "## 全部复现（262/262）")
    rows = []
    for paper in PAPERS:
        if paper.batch != "B07":
            continue
        slug = f"{paper.arxiv_id}-{paper.key}"
        rows.append(f"- `{paper.key}` · [{paper.title}]({slug}/README.md)：{paper.summary}")
    block = (
        f"{START}\n## 2026 历史扫描 B07（9 个基础模型 / 基础设施 adapter）\n\n"
        + "\n".join(rows)
        + f"\n\n{END}\n\n"
    )
    text = _replace_block(text, START, END, block, "## 全部复现（262/262）")
    PATH.write_text(text, encoding="utf-8")

    for domain, title, batches in (
        ("post-training", "2026 历史扫描 B08～B09", {"B08", "B09"}),
        ("agent-research", "2026 历史扫描 B10～B11", {"B10", "B11"}),
    ):
        path = ROOT / f"docs/{domain}/README.md"
        page = path.read_text(encoding="utf-8")
        start = f"<!-- historical-{domain}:start -->"
        end = f"<!-- historical-{domain}:end -->"
        bullets = []
        for paper in PAPERS:
            if paper.batch in batches:
                slug = f"{paper.arxiv_id}-{paper.key}"
                bullets.append(f"- [{paper.title}]({slug}/README.md)：{paper.summary}")
        section = f"{start}\n## {title}\n\n" + "\n".join(bullets) + f"\n\n{end}\n\n"
        page = _replace_block(page, start, end, section, "## 研究闭环")
        path.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
