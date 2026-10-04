#!/usr/bin/env python3
"""Generate docs and deterministic L1 receipts for the Meta reconciliation."""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research.official_meta_backfill_20261004 import (  # noqa: E402
    PAHFMemory,
    aira2_async_schedule,
    aira2_hidden_consistent_select,
    bounded_hyperagent_step,
    hyperagent_parent_probabilities,
    sira_filter_terms,
    sira_weighted_scores,
)
from auto_research.latest_20261004_catalog import LATEST_METHOD_PAPERS  # noqa: E402

SEEDS = (42, 43, 44)
SOURCE = "src/auto_research/agent_research/official_meta_backfill_20261004.py"

DETAILS = {
    "sira": {
        "summary": (
            "冻结 LLM 先生成相关证据可能使用、但原查询缺失的词汇，再用倒排索引中的文档频率"
            "过滤不存在或过于常见的词；原查询与验证后的扩展只执行一次加权 BM25。"
        ),
        "formula": (
            "$score(d)=BM25(q_{orig},d)+w\\,BM25(q_{exp},d)$；查询侧词项需满足 "
            "$0<DF(t)\\le\\tau|C|$。"
        ),
        "result": (
            "十个 BEIR 任务平均检索表现优于论文所比稠密、学习式稀疏及 Agent 检索基线；"
            "BrowseComp-Wikipedia 的 Recall@1/10/100 分别为 9.70%/15.27%/36.14%。"
        ),
        "boundary": (
            "本地执行 DF gate 与加权单次检索组合，不调用论文 LLM、不重建 2558 万文档索引，"
            "也不把公开离线结果写成线上 A/B。"
        ),
    },
    "aira2": {
        "summary": (
            "以无同步屏障的 steady-state worker pool 提高实验吞吐；训练、搜索、最终选择使用固定"
            "的 80/10/10 隐藏切分，搜索只看 search score，结束后才用未参与爬山的 validation 选冠军。"
        ),
        "formula": (
            "$p(i)\\propto(N-r_i+1)^{1/T}$；$D_{train}$、$D_{search}$、$D_{val}$ 一次划分后"
            "跨候选保持一致，test signal 不进入本地接口。"
        ),
        "result": (
            "论文 v2 在 MLE-bench-30 报告 24h/72h Percentile Rank 81.5%/83.1%，"
            "并在 AIRS-Bench 20 项任务中 6 项超过人工 SOTA。"
        ),
        "boundary": (
            "本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct "
            "operator 或论文长时训练，因此不是多 GPU 性能复现。"
        ),
    },
    "pahf": {
        "summary": (
            "Agent 在行动前从显式用户记忆检索偏好，未知或低置信时主动澄清；行动后无论当前"
            "记忆是否自信，都接收纠正并覆盖过期偏好，从而处理新用户、上下文差异和偏好漂移。"
        ),
        "formula": (
            "$a_t=\\pi_{act}(I_t,O_t,m_t,q_t,f_t^{pre})$；理论动态 regret 为 "
            "$O(K+\\gamma Tm^{-k})$。"
        ),
        "result": (
            "论文四阶段实验中 PAHF 在 embodied 的 Phase-2/4 为 70.5%/68.8%，shopping 为 "
            "41.3%/70.3%，均优于无记忆和单一反馈通道。"
        ),
        "boundary": (
            "本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 "
            "GPT、机器人环境或论文购物模拟器。"
        ),
    },
    "hyperagents": {
        "summary": (
            "把任务 Agent 与修改它的 meta Agent 放入同一可编辑程序，并在开放档案中积累变体；"
            "父代概率同时奖励当前性能与较少后代的探索价值，使改进机制本身也可继续被改进。"
        ),
        "formula": (
            "$s_i=\\sigma(\\lambda(\\alpha_i-\\alpha_{mid}))$，$h_i=1/(1+n_i)$，"
            "$p_i=s_ih_i/\\sum_j s_jh_j$。"
        ),
        "result": (
            "论文在代码、论文评审、机器人 reward design 和 IMO 评分上展示开放式档案改进，"
            "并报告跨代形成评测分析、成本规划和持久记忆等元认知结构。"
        ),
        "boundary": (
            "本地执行论文父代分布和有界结构化 archive step；禁止执行生成代码或 shell，"
            "因此只验证搜索控制机制，不声称复现自指代码修改能力。"
        ),
    },
}


def run(record: dict, seed: int) -> dict[str, float | int | bool]:
    key = record["key"]
    if key == "sira":
        frequencies = {"retrieval": 7 + seed % 3, "common": 90, "agentic": 3}
        accepted = sira_filter_terms(
            ("retrieval", "missing", "common", "agentic"), frequencies,
            corpus_size=100, max_fraction=.1,
        )
        scores = sira_weighted_scores((1.0, 2.0, .5), (.2, .1, 2.0), expansion_weight=.7)
        return {"accepted_terms": len(accepted), "top_document": scores.index(max(scores))}
    if key == "aira2":
        schedule = aira2_async_schedule((5 + seed % 3, 1, 2, 4), workers=2)
        selected, audit = aira2_hidden_consistent_select(
            {"overfit": .99, "robust": .80 + seed / 10000},
            {"overfit": .40, "robust": .90},
        )
        return {
            "makespan": max(row[3] for row in schedule),
            "selected_robust": selected == "robust",
            "test_labels_visible": bool(audit["test_labels_visible"]),
        }
    if key == "pahf":
        memory = PAHFMemory.empty()
        asked = bool(memory.pre_action("sleepy")["ask_clarification"])
        memory.integrate_pre_action_feedback("sleepy", "tea")
        drifted = memory.integrate_post_action_feedback("sleepy", "coffee")
        return {
            "clarification_requested": asked,
            "drift_detected": drifted,
            "final_preference_corrected": memory.pre_action("sleepy")["preference"] == "coffee",
        }
    if key == "hyperagents":
        probabilities = hyperagent_parent_probabilities((.9, .8), (20, seed % 2), top_m=2)
        archive = bounded_hyperagent_step(
            ({"strategy": "base", "score": .5},), parent_index=0,
            modifier=lambda _: {"strategy": "reflect", "reflection": True},
            evaluator=lambda child: .8 if child["reflection"] else .1,
        )
        return {
            "probability_sum": sum(probabilities),
            "archive_size": len(archive),
            "structured_only": "shell" not in archive[-1],
        }
    raise KeyError(key)


def aggregate(rows: list[dict]) -> dict[str, float]:
    result = {}
    for key in rows[0]:
        values = [row[key] for row in rows]
        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            result[f"{key}_mean"] = statistics.fmean(values)
    return result


def render(record: dict) -> str:
    detail = DETAILS[record["key"]]
    upstream = (
        f"是：[{record['code']}]({record['code']})" if record.get("code")
        else "否：截至 2026-10-04 未在论文、Meta 官方页或作者主页找到原作者公开实现"
    )
    return f"""# {record['title']}

> **复现级别：L1 核心机制诊断。** {detail['boundary']}

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv]({record['paper_url']}) |
| 公司/机构 | {record['first_author_affiliation']}（按第一作者署名单位） |
| 首次公开日期 | {record['published']}（arXiv v1） |
| 原文开源代码 | {upstream} |
| Adapter | `{record['adapter']}` |
| 本地复现代码 | [`{SOURCE}`](https://github.com/daiwk/auto-research/tree/main/{SOURCE}) |

## 原始论文总结

### 背景与主要改动

{detail['summary']}

```mermaid
flowchart LR
  I[受限输入与公开状态] --> M[{record['adapter']} 定义性机制]
  M --> A[可审计中间量]
  A --> O[有界输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![{record['title']} 原论文关键图](assets/paper-figure-01.png)]({record['paper_url'].replace('/abs/', '/pdf/')})

> **原论文关键图**：展示核心架构或实验协议。图片来自[原论文]({record['paper_url']})，版权归原作者所有。
<!-- paper-figure:end -->

### 核心公式

{detail['formula']}

### 论文离线与线上效果

{detail['result']}

> 这些论文均未报告可归因于该方法的生产线上 A/B；上述数字是论文公开离线评测，不与本地诊断混写。

## 本地复现

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- 基线为机制关闭或默认状态；`diagnostic_only=true`，不进入正式能力排名。

## 复现边界

{detail['boundary']}
"""


def main() -> None:
    for record in LATEST_METHOD_PAPERS:
        rows = [{"seed": seed, **run(record, seed)} for seed in SEEDS]
        readme = ROOT / "docs" / record["detail_path"]
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text(render(record), encoding="utf-8")
        artifact = readme.parent / "metrics" / "mechanism-seeds42-44.json"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 2,
            "manifest_ref": f"agent-research:{record['key']}",
            "method": record["key"],
            "dataset": "deterministic public mechanism mini-suite",
            "seeds": list(SEEDS),
            "diagnostic_only": True,
            "seed_results": rows,
            "aggregate_metrics": aggregate(rows),
            "evaluation_protocol": {
                "tier": "l1_mechanism", "formal_comparison": False,
                "diagnostic_only": True, "seeds": list(SEEDS),
                "claim_policy": "mechanism execution and invariants only",
            },
            "provenance": {
                "artifact_path": str(artifact.relative_to(ROOT)),
                "dataset_fingerprint": "meta-official-backfill-public-fixtures-v1",
                "original_code_commit": "working tree",
            },
        }
        artifact.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(readme.relative_to(ROOT))


if __name__ == "__main__":
    main()
