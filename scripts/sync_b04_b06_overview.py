#!/usr/bin/env python3
"""Idempotently register historical batches B04--B06 in the reproduction overview."""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.reproductions.historical_b04_b06 import SPECS
from auto_research.reproductions.historical_b04_b06_metadata import ENTRIES


ROOT = Path(__file__).resolve().parents[1]
OVERVIEW = ROOT / "docs" / "reproductions" / "README.md"
SUMMARY = {
    "prl-puts": "双头 Q 网络与 Pareto utility 扫描",
    "ektm": "任务相似度驱动的多任务知识迁移",
    "adasid": "碰撞负载与语义相容性驱动的动态 SID",
    "unirec-coa": "属性链生成与业务偏好对齐",
    "uniscale": "Entire-Space 数据与模型协同扩展",
    "gatesid": "冷启动感知的语义/协同门控",
    "aigq": "混合 query 生成与 IL-GRPO",
    "safro": "满意度感知的双重相对策略优化",
    "sort-ranking": "工业 Ranking Transformer 系统优化",
    "quasid": "资格感知的 SID 碰撞约束",
    "gpl-prerank": "LLM 伪标签增强在线预排序",
    "ltv-video-ranking": "位置去偏与长期价值建模",
    "rgalign-rec": "排序器指导的潜在 query 对齐",
    "linkedin-feed-sr": "工业长序列 Feed 排序",
    "cadet": "候选后上下文条件化广告 CTR",
    "diffureason": "扩散式潜在推理与 GRPO",
    "sarm": "MLLM 语义 anchor 增强直播排序",
    "ml-dcn": "Masked Low-Rank DCN 特征交叉",
    "rag-qac": "RAG 与多目标对齐的查询补全",
}
BATCH = {
    key: "B04" if index < 6 else "B05" if index < 12 else "B06"
    for index, key in enumerate(ENTRIES)
}


def signed(value: float) -> str:
    return f"{value:+.2f}%"


def main() -> None:
    text = OVERVIEW.read_text(encoding="utf-8")
    # Six Google/Meta full-text recoveries landed after the overview's old
    # 228 count; B04--B06 then add another nineteen adapters.
    text = text.replace("228 个 adapter", "253 个 adapter")
    text = text.replace("247 个 adapter", "253 个 adapter")
    text = text.replace("全部复现（228/228）", "全部复现（253/253）")
    text = text.replace("全部复现（247/247）", "全部复现（253/253）")

    if "## 2026 历史扫描 B04～B06" not in text:
        groups: list[str] = []
        for batch in ("B04", "B05", "B06"):
            lines = [f"### {batch}", ""]
            for key, row in ENTRIES.items():
                if BATCH[key] != batch:
                    continue
                slug = f"{row.arxiv_id}-{key}"
                lines.append(f"- `{key}` · [{SPECS[key].title}]({slug}/README.md)：{SUMMARY[key]}。")
            groups.append("\n".join(lines))
        section = (
            "## 2026 历史扫描 B04～B06（19 个 adapter）\n\n"
            "19 篇均逐篇核验正文中的生产 A/B 位置，并在 MovieLens-100K 的相同切分、"
            "候选集与 seed 42 下运行独立核心机制；线上数字与本地结果严格分栏。\n\n"
            + "\n\n".join(groups)
            + "\n\n"
        )
        text = text.replace("## 全部复现（253/253）", section + "## 全部复现（253/253）")

    if "`prl-puts` ·" not in text.split("## 全部复现（253/253）", 1)[1]:
        rows: list[str] = []
        for key, row in ENTRIES.items():
            slug = f"{row.arxiv_id}-{key}"
            metric_path = ROOT / "docs" / "reproductions" / slug / "metrics" / "public-seed42.json"
            metrics = json.loads(metric_path.read_text(encoding="utf-8"))
            local = metrics["relative"]["ndcg_at_10_percent"]
            online = f"{row.metric} {signed(row.lift)}"
            rows.append(
                f"| 核心机制 | `{key}` · [{SPECS[key].title}]({slug}/README.md) | "
                f"{online} | {SUMMARY[key]}；NDCG@10 {signed(local)} |"
            )
        header = "|---|---|---|---|\n"
        index = text.index(header, text.index("## 全部复现（253/253）")) + len(header)
        text = text[:index] + "\n".join(rows) + "\n" + text[index:]

    OVERVIEW.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
