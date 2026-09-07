#!/usr/bin/env python3
"""Idempotently add the 2026-09-07 industrial scan to browse catalogs."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs/reproductions/catalog"
ROWS = {
    "allecompanion": {
        "slug": "2609.05063-allecompanion",
        "title": "Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro",
        "company": "Allegro.com",
        "topic": "### 召回、触发与多通道路由",
        "summary": "用 ComCat 互补类别图、类别约束双塔和 Category Adapter 过滤共购噪声。",
    },
    "autolr": {
        "slug": "2609.04871-autolr",
        "title": "AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems",
        "company": "NetEase",
        "topic": "### 自主研究与反馈闭环",
        "summary": "以多专家评审、证据加权预算和确定性晋级门串联研究、实验与上线评审。",
    },
}


def insert(path: Path, heading: str, lines: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [line for line in lines if line not in text]
    if not missing:
        return
    marker = heading + "\n"
    if marker not in text:
        text = text.rstrip() + f"\n\n{heading}\n"
    index = text.index(marker) + len(marker)
    path.write_text(text[:index] + "\n".join(missing) + "\n" + text[index:], encoding="utf-8")


def main() -> None:
    for row in ROWS.values():
        line = f"- 2026-09 · [{row['title']}](../{row['slug']}/README.md)：{row['summary']}"
        insert(CATALOG / "by-company.md", f"## {row['company']}", [line])
        plain = f"- [{row['title']}](../{row['slug']}/README.md)：{row['summary']}"
        insert(CATALOG / "by-month.md", "## 2026-09", [plain])
        insert(CATALOG / "by-topic.md", row["topic"], [plain])


if __name__ == "__main__":
    main()
