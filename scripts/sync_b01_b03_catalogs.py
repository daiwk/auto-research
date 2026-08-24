#!/usr/bin/env python3
"""Idempotently add B01--B03 papers to the three recommendation browse pages."""

from pathlib import Path

from auto_research.reproductions.historical_b01_b03_metadata import ENTRIES


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "reproductions" / "catalog"
SUMMARY = {
    "dynamic-codebook": "用曝光加权动态大码本替代多级小码本，并保留独立碰撞码以缩短 SID 解码。",
    "netflix-mediafm": "把冻结多模态 embedding 接入统一资产双塔，并用查询相似度增强搜索画布打分。",
    "ogr": "以统一语义-协同 ID 生成整张 slate，再用列表反馈做保守策略对齐。",
    "inthq": "让多个业务任务在长短双流的不同层级执行交互查询，而非仅共享底层编码。",
    "pushdualgen": "先生成可服务 SID，再按需生成可解释 copy，并在在线侧融合两种表示。",
    "recharness": "用 bandit 在有限预算下路由候选结构实验，并把验证反馈写回下一轮。",
    "gala": "通过三元组预训练、GRPO 行为对齐和 ID/多模态门控形成可部署表示。",
    "feedback-policy": "从真实反馈发现生成策略，再用双空间关系蒸馏到轻量线上排序器。",
    "real-estate-rerank": "结合对话需求、房源属性、文本描述与候选集合统计执行 LLM 重排。",
    "adaptive-ad-load": "从随机现场实验学习收入—转化曲线，再按请求动态选择广告数量。",
    "guess-where-you-go": "把时空历史编码为 SID，并以课程训练和长期反馈优化下一 POI 生成。",
    "genpage": "用一个模型直接生成整页，并以长期用户奖励和业务约束进行后训练。",
    "journeyformer": "统一编码长短 guest journey 与事件时间，在生产搜索中替代手工序列特征。",
    "l2rec": "用个性化双视图 LoRA-MoE 分别适配语义和行为，再自适应融合。",
    "qgs": "把 query-item 联合序列交给 Linear HSTU，并融合稀疏交叉特征做生成式搜索。",
    "tubifm": "以统一 user story 和任务提示让同一模型完成 item、carousel 与 search 排序。",
    "pearl-percentile": "通过多样本对比估计低方差行为 percentile，并扩展到多个直播目标。",
    "dadf": "冻结成熟 watch-time 模型，学习分布感知乘性残差且保持服务接口不变。",
}
TOPIC = {
    "dynamic-codebook": "生成式召回与端到端推荐", "netflix-mediafm": "内容理解与语义表征",
    "ogr": "重排、混排与多目标页面决策", "inthq": "排序网络与长序列",
    "pushdualgen": "生成式召回与端到端推荐", "recharness": "采样、蒸馏与强化学习",
    "gala": "内容理解与语义表征", "feedback-policy": "采样、蒸馏与强化学习",
    "real-estate-rerank": "重排、混排与多目标页面决策", "adaptive-ad-load": "因果推断与长期价值",
    "guess-where-you-go": "生成式召回与端到端推荐", "genpage": "重排、混排与多目标页面决策",
    "journeyformer": "排序网络与长序列", "l2rec": "LLM / Foundation model + Recommendation",
    "qgs": "生成式召回与端到端推荐", "tubifm": "LLM / Foundation model + Recommendation",
    "pearl-percentile": "因果推断与长期价值", "dadf": "因果推断与长期价值",
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
    text = text[:index] + "\n".join(missing) + "\n" + text[index:]
    path.write_text(text, encoding="utf-8")


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

