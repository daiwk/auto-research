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
BACKGROUND_HEADING = "### 背景与主要改动"
BROWSE_INTROS = {
    "institution": (
        "每篇论文独占一行；按主要公司、机构或学校分组，并保留首次公开年月和"
        "一至两句中文方法简介。"
    ),
    "topic": (
        "按论文解决的核心问题分组；每篇论文独占一行，简介直接概括主要机制，"
        "实验结果与复现边界请进入详情页查看。"
    ),
    "year": (
        "按首次公开年份浏览；同年论文按日期倒序排列，每篇独占一行并附主要方法简介。"
    ),
}


def read_method_summary(module: str, link: str) -> str:
    """Read the canonical Chinese method summary from a paper detail page."""

    page = DOCS / module / link
    text = page.read_text(encoding="utf-8")
    if BACKGROUND_HEADING not in text:
        raise ValueError(f"{page} missing {BACKGROUND_HEADING}")

    paragraph: list[str] = []
    for line in text.split(BACKGROUND_HEADING, 1)[1].splitlines():
        stripped = line.strip()
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith(("#", "```", "<!--")):
            if paragraph:
                break
            continue
        paragraph.append(stripped)

    summary = re.sub(r"\s+", " ", " ".join(paragraph)).strip()
    # Markdown source wraps Chinese prose across physical lines. Joining those
    # lines with a normal space must not leave artifacts such as “执行记录 成”.
    summary = re.sub(
        r"(?<=[\u3400-\u4dbf\u4e00-\u9fff]) "
        r"(?=[\u3400-\u4dbf\u4e00-\u9fff])",
        "",
        summary,
    )
    summary = re.sub(r"(?<=[，。；：、！？]) +", "", summary)
    summary = re.sub(r" +(?=[，。；：、！？])", "", summary)
    # Browse pages should stay scannable like the recommendation catalog:
    # retain the problem statement and the main mechanism, not the full section.
    sentences = re.findall(r"[^。]+(?:。|$)", summary)
    summary = "".join(sentences[:2]).strip()
    if not summary:
        raise ValueError(f"{page} has no method summary below {BACKGROUND_HEADING}")
    return summary


def read_rows(module: str) -> list[dict[str, str]]:
    rows = []
    for line in (DOCS / module / "catalog.md").read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if not match:
            continue
        row = {key: value.strip() for key, value in match.groupdict().items()}
        date = re.search(r"(\d{4})-\d{2}-\d{2}", row["info"])
        row["year"] = date.group(1) if date else "未标注"
        row["date"] = date.group(0) if date else "未标注"
        row["institution"] = (
            row["info"][: date.start()].rstrip("，, ") if date else row["info"]
        )
        row["summary"] = read_method_summary(module, row["link"])
        rows.append(row)
    return rows


def render(module: str, dimension: str, title: str) -> str:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_rows(module):
        groups[row[dimension]].append(row)
    lines = [
        f"# {title}",
        "",
        BROWSE_INTROS[dimension],
        "",
    ]
    for group in sorted(groups, reverse=dimension == "year"):
        lines.extend([f"## {group}", ""])
        if dimension in {"institution", "year"}:
            ordered = sorted(
                groups[group],
                key=lambda item: (item["date"], item["title"].lower()),
                reverse=True,
            )
        else:
            ordered = sorted(
                groups[group], key=lambda item: item["title"].lower()
            )
        for row in ordered:
            date_prefix = (
                f"{row['date'][:7]} · "
                if dimension in {"institution", "year"}
                else ""
            )
            lines.append(
                f"- {date_prefix}[{row['title']}](../{row['link']})"
                f"（`{row['key']}`）："
                f"{row['summary']}"
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
