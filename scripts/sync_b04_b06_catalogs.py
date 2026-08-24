#!/usr/bin/env python3
"""Idempotently add B04--B06 papers to recommendation browse pages."""

from pathlib import Path

from auto_research.reproductions.historical_b04_b06_metadata import ENTRIES


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "reproductions" / "catalog"
SUMMARY = {
    "prl-puts": "以双头 Q 网络和 Pareto 扫描选择可治理的个性化多目标 utility 策略。",
    "ektm": "按任务相似度把 CTR 知识迁移到多个 CVR 塔，并抑制难例负迁移。",
    "adasid": "依据碰撞负载、语义相容性和训练阶段动态调节 SID 重叠约束。",
    "unirec-coa": "先生成属性链再生成容量受限 SID，并以 RFT/DPO 对齐业务目标。",
    "uniscale": "以 Entire-Space 数据和分层异构融合协同扩展搜索排序模型。",
    "gatesid": "用冷启动感知门控动态融合语义 SID 与协同行为信号。",
    "aigq": "组合 Direct/Reasoning query 生成、IL-GRPO 与混合在线服务。",
    "safro": "用满意度奖励和双重相对优势优化短视频搜索多任务融合。",
    "sort-ranking": "系统优化 token 化、注意力和 FFN，统一替代工业 DLRM 排序。",
    "quasid": "按业务资格信号设定碰撞 margin，提升冷启动 SID 可辨识度。",
    "gpl-prerank": "LLM 为未曝光候选生成伪标签，线上预排序器不增加 LLM 时延。",
    "ltv-video-ranking": "组合位置去偏、会话归因与作者周期任务建模长期价值。",
    "rgalign-rec": "用真实排序模型偏好指导潜在 query 的 SFT 与 DPO 对齐。",
    "linkedin-feed-sr": "用工业长序列推荐器重写 LinkedIn Feed 排序与服务链路。",
    "cadet": "以候选后上下文条件化的 Decoder-only Transformer 统一广告 CTR。",
    "diffureason": "将 Thinking Tokens、扩散去噪和 GRPO 组成端到端序列推荐。",
    "sarm": "离线 MLLM 生成语义 anchor，轻量非对称模块注入直播排序。",
    "ml-dcn": "用可学习 mask 与低秩交叉扩大 DCN 容量并保持线上成本中性。",
    "rag-qac": "以 RAG、SFT 和 DPO 同时优化补全相关性、安全与 groundedness。",
}
TOPIC = {
    "prl-puts": "重排、混排与多目标页面决策", "ektm": "排序网络与长序列",
    "adasid": "生成式召回与端到端推荐", "unirec-coa": "生成式召回与端到端推荐",
    "uniscale": "排序网络与长序列", "gatesid": "生成式召回与端到端推荐",
    "aigq": "生成式召回与端到端推荐", "safro": "采样、蒸馏与强化学习",
    "sort-ranking": "排序网络与长序列", "quasid": "生成式召回与端到端推荐",
    "gpl-prerank": "LLM / Foundation model + Recommendation", "ltv-video-ranking": "因果推断与长期价值",
    "rgalign-rec": "LLM / Foundation model + Recommendation", "linkedin-feed-sr": "排序网络与长序列",
    "cadet": "广告与商业决策", "diffureason": "生成式召回与端到端推荐",
    "sarm": "内容理解与语义表征", "ml-dcn": "广告与商业决策",
    "rag-qac": "LLM / Foundation model + Recommendation",
}


def insert(path: Path, heading: str, lines: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [line for line in lines if line.split("](../", 1)[1].split("/", 1)[0] not in text]
    if not missing:
        return
    marker = heading + "\n"
    if marker not in text:
        text = text.rstrip() + f"\n\n{heading}\n"
    index = text.index(marker) + len(marker)
    path.write_text(text[:index] + "\n".join(missing) + "\n" + text[index:], encoding="utf-8")


def main() -> None:
    companies: dict[str, list[str]] = {}
    months: dict[str, list[str]] = {}
    topics: dict[str, list[str]] = {}
    for key, row in ENTRIES.items():
        slug = f"{row.arxiv_id}-{key}"
        company_line = f"- {row.published[:7]} · [{row.title}](../{slug}/README.md)：{SUMMARY[key]}"
        plain_line = f"- [{row.title}](../{slug}/README.md)：{SUMMARY[key]}"
        companies.setdefault(row.organization, []).append(company_line)
        months.setdefault(row.published[:7], []).append(plain_line)
        topics.setdefault(TOPIC[key], []).append(plain_line)
    for heading, lines in companies.items():
        insert(CATALOG / "by-company.md", f"## {heading}", lines)
    for heading, lines in months.items():
        insert(CATALOG / "by-month.md", f"## {heading}", lines)
    for heading, lines in topics.items():
        insert(CATALOG / "by-topic.md", f"### {heading}", lines)


if __name__ == "__main__":
    main()
