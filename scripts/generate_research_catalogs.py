#!/usr/bin/env python3
"""Generate post-training and Agent browse catalogs from their canonical tables."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ROW = re.compile(
    r"^\| (?P<topic>[^|]+) \| \[(?P<title>[^\]]+)\]\((?P<link>[^)]+)\) "
    r"\| (?P<info>[^|]+) \| (?P<code>[^|]+) \| `(?P<key>[^`]+)` \|$"
)


def read_rows(module: str) -> list[dict[str, str]]:
    rows = []
    for line in (DOCS / module / "catalog.md").read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if not match:
            continue
        row = {key: value.strip() for key, value in match.groupdict().items()}
        date = re.search(r"(\d{4})-\d{2}-\d{2}", row["info"])
        row["year"] = date.group(1) if date else "未标注"
        row["institution"] = (
            row["info"][: date.start()].rstrip("，, ") if date else row["info"]
        )
        rows.append(row)
    return rows


def render(module: str, dimension: str, title: str) -> str:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_rows(module):
        groups[row[dimension]].append(row)
    lines = [
        f"# {title}",
        "",
        "本页由统一方法索引生成；新增论文先登记到"
        "[方法索引](../catalog.md)，再运行 "
        "`python scripts/generate_research_catalogs.py` 更新三套分类。",
        "",
    ]
    for group in sorted(groups, reverse=dimension == "year"):
        lines.extend([f"## {group}", ""])
        for row in sorted(groups[group], key=lambda item: item["title"].lower()):
            lines.append(
                f"- [{row['title']}](../{row['link']})（`{row['key']}`）："
                f"{row['topic']}；详情页包含核心机制、公式、原文结果和本地复现边界。"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    for module, label in (
        ("post-training", "LLM 后训练"),
        ("agent-research", "Agent 研究"),
    ):
        target = DOCS / module / "catalog"
        target.mkdir(exist_ok=True)
        for dimension, title in (
            ("institution", f"{label}：按公司 / 机构 / 学校"),
            ("topic", f"{label}：按主题"),
            ("year", f"{label}：按年份"),
        ):
            (target / f"by-{dimension}.md").write_text(
                render(module, dimension, title), encoding="utf-8"
            )


if __name__ == "__main__":
    main()
