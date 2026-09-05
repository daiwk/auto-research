#!/usr/bin/env python3
"""Idempotently add the historical P0 H05 batch to recommendation catalogs."""

from pathlib import Path

from auto_research.reproductions.historical_p0_h05 import PAPERS


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "reproductions" / "catalog"
SUMMARY = {
    "marc": "从中间层抽取任务相关表征，显式解耦推荐适配与低维压缩。",
    "rankup": "随机置换多 embedding、全局 token 和任务解耦共同提升表征有效秩。",
    "sid_coord": "以层级 SID、目标感知 HID–SID 门控和兴趣对齐增强长尾泛化。",
    "rclrec": "把转化相关行为逆序组成短课程，为稀疏转化增加中间监督。",
    "tagllm": "用用户兴趣手册约束细粒度多模态标签，并把生成能力蒸馏到小模型。",
    "genfacet": "联合生成搜索分面和改写 query，再以检索满意度执行偏好对齐。",
    "cgr": "在自回归重排中直接执行约束感知奖励剪枝。",
    "hpgr": "以 session 层级预训练和偏好引导稀疏注意力建模长行为序列。",
    "climber_pilot": "将多步消费前瞻蒸馏到单步召回，并在注意力内注入业务指令。",
    "rolegen": "通过功能角色和反事实转化路径寻找能激活休眠用户的桥接物品。",
}
TOPIC = {
    "marc": "LLM / Foundation model + Recommendation",
    "rankup": "排序网络与长序列",
    "sid_coord": "冷启动与语义-行为对齐",
    "rclrec": "生成式召回与端到端推荐",
    "tagllm": "内容理解与语义表征",
    "genfacet": "搜索、召回与长期价值",
    "cgr": "重排、混排与多目标页面决策",
    "hpgr": "排序网络与长序列",
    "climber_pilot": "生成式召回与端到端推荐",
    "rolegen": "因果推断与长期价值",
}


def insert(path: Path, heading: str, lines: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [
        line for line in lines
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


def main() -> None:
    companies: dict[str, list[str]] = {}
    months: dict[str, list[str]] = {}
    topics: dict[str, list[str]] = {}
    for internal, row in PAPERS.items():
        slug = f"{row['arxiv_id']}-{row['key']}"
        summary = SUMMARY[internal]
        company_line = (
            f"- {row['published'][:7]} · [{row['title']}]"
            f"(../{slug}/README.md)：{summary}"
        )
        plain_line = f"- [{row['title']}](../{slug}/README.md)：{summary}"
        companies.setdefault(row["organization"], []).append(company_line)
        months.setdefault(row["published"][:7], []).append(plain_line)
        topics.setdefault(TOPIC[internal], []).append(plain_line)
    for heading, lines in companies.items():
        insert(CATALOG / "by-company.md", f"## {heading}", lines)
    for heading, lines in months.items():
        insert(CATALOG / "by-month.md", f"## {heading}", lines)
    for heading, lines in topics.items():
        insert(CATALOG / "by-topic.md", f"### {heading}", lines)


if __name__ == "__main__":
    main()
