#!/usr/bin/env python3
"""Idempotently add historical P0 batches H06/H07 to recommendation catalogs."""

from pathlib import Path

from auto_research.reproductions.historical_p0_h06_h07 import PAPERS


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "reproductions" / "catalog"
SUMMARY = {
    "unimvt": "联合学习去偏 CTR 与因果 uplift，并显式估计 treatment 和 counterfactual 响应。",
    "rq_gmm": "以残差高斯混合量化替代硬聚类，用概率语义 ID 增强多模态 CTR。",
    "capts": "以价值感知匹配和跨渠道自适应路由选择 I2I 召回 trigger。",
    "mlcc": "分层压缩并交叉低维特征，在受控计算量下扩大推荐网络容量。",
    "ug_sep": "拆分用户侧与通用计算，使大规模推荐模型复用只需计算一次的表示。",
    "smes": "用渐进式稀疏路由和去重执行，为不同任务动态分配专家容量。",
    "pit": "按用户动态组合 item token，使生成式推荐的语义 ID 同时表达个体偏好。",
    "zenith": "以 Prime Token Fusion 和 Boost 扩展直播排序模型的深度与宽度。",
    "easq": "用独立 LoRA 与多任务路径把稀疏问卷满意度接入持续在线学习。",
    "s2gr": "把语义引导逐步写入潜空间推理，增强生成式推荐的中间决策。",
    "sparsectr": "组合全局、转移和局部稀疏注意力，建模千级长期行为序列。",
    "hcub": "用层级上下文 uplift bandit 在目录个性化中学习增量收益。",
    "airbnb_ebr": "用旅程级检索和多阶段排序统一 Airbnb 的体验推荐链路。",
    "promise": "以过程奖励监督生成式推荐的中间推理，而非只依赖最终命中。",
    "harmonrank": "用关系感知注意力和一致性约束协调多阶段工业排序。",
}
TOPIC = {
    "unimvt": "因果推断与长期价值",
    "rq_gmm": "内容理解与语义表征",
    "capts": "召回、触发与多通道路由",
    "mlcc": "排序网络与长序列",
    "ug_sep": "排序网络与长序列",
    "smes": "多任务学习与多目标优化",
    "pit": "生成式召回与端到端推荐",
    "zenith": "排序网络与长序列",
    "easq": "多任务学习与多目标优化",
    "s2gr": "生成式召回与端到端推荐",
    "sparsectr": "排序网络与长序列",
    "hcub": "因果推断与长期价值",
    "airbnb_ebr": "召回、触发与多通道路由",
    "promise": "生成式召回与端到端推荐",
    "harmonrank": "重排、混排与多目标页面决策",
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


def main() -> None:
    companies: dict[str, list[str]] = {}
    months: dict[str, list[str]] = {}
    topics: dict[str, list[str]] = {}
    ordered = sorted(PAPERS.items(), key=lambda item: item[1]["published"], reverse=True)
    for internal, row in ordered:
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
