#!/usr/bin/env python3
"""Idempotently add the 2026-09-05 recommendation scan to browse catalogs."""

from pathlib import Path

from auto_research.reproductions.recent_20260905 import PAPERS


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "reproductions" / "catalog"
SUMMARY = {
    "rest": "用双门控时序编码抑制行为噪声，并将重型用户编码与轻量候选交叉解耦，实现请求内共享计算。",
    "tgr": "统一分层语义 ID 生成、列表排序和离线 reason token 注入，在一套框架中覆盖生成与推理。",
    "camie": "用共同互动商品对训练对称多模态向量，使内容表征同时保留用户旅程中的行为相似性。",
    "setmir": "把多兴趣召回改写为集合预测，以 presence gate 和 query-level NMS 动态减少重复 ANN 请求。",
}
COMPANY = {
    "rest": "ByteDance / Douyin / TikTok",
    "tgr": "Tencent",
    "camie": "Snap Inc.",
    "setmir": "Snap Inc.",
}
TOPIC = {
    "rest": "排序网络与长序列",
    "tgr": "生成式召回与端到端推荐",
    "camie": "内容理解与语义表征",
    "setmir": "召回、触发与多通道路由",
}


def insert(path: Path, heading: str, lines: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [
        line
        for line in lines
        if line.split("](../", 1)[1].split("/", 1)[0] not in text
    ]
    if not missing:
        return
    marker = heading + "\n"
    if marker not in text:
        text = text.rstrip() + f"\n\n{heading}\n"
    index = text.index(marker) + len(marker)
    path.write_text(
        text[:index] + "\n".join(missing) + "\n" + text[index:],
        encoding="utf-8",
    )


def sort_month_sections(path: Path) -> None:
    """Keep month sections newest-first when a scan opens a new month."""
    text = path.read_text(encoding="utf-8")
    first_heading = text.index("\n## ")
    intro = text[:first_heading].rstrip()
    blocks = ["## " + block for block in text[first_heading + 4 :].split("\n## ")]
    blocks.sort(key=lambda block: block.splitlines()[0], reverse=True)
    path.write_text(intro + "\n\n" + "\n\n".join(block.rstrip() for block in blocks) + "\n", encoding="utf-8")


def main() -> None:
    companies: dict[str, list[str]] = {}
    months: dict[str, list[str]] = {}
    topics: dict[str, list[str]] = {}
    ordered = sorted(PAPERS.values(), key=lambda row: row["published"], reverse=True)
    for row in ordered:
        key = row["key"]
        slug = f"{row['arxiv_id']}-{key}"
        summary = SUMMARY[key]
        company_line = (
            f"- {row['published'][:7]} · [{row['title']}]"
            f"(../{slug}/README.md)：{summary}"
        )
        plain_line = f"- [{row['title']}](../{slug}/README.md)：{summary}"
        companies.setdefault(COMPANY[key], []).append(company_line)
        months.setdefault(row["published"][:7], []).append(plain_line)
        topics.setdefault(TOPIC[key], []).append(plain_line)
    for heading, lines in companies.items():
        insert(CATALOG / "by-company.md", f"## {heading}", lines)
    for heading, lines in months.items():
        insert(CATALOG / "by-month.md", f"## {heading}", lines)
    sort_month_sections(CATALOG / "by-month.md")
    for heading, lines in topics.items():
        insert(CATALOG / "by-topic.md", f"### {heading}", lines)


if __name__ == "__main__":
    main()
