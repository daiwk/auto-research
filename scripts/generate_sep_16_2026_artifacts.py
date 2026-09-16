#!/usr/bin/env python3
"""Generate documentation and L1 receipts for the Sep-16 P0/P1 batch."""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.foundation_latest_20260916 import agentkv_scores, loopspec_schedule, r4t_targets
from auto_research.latest_20260916_catalog import LATEST_METHOD_PAPERS
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.reproductions.registry import get_adapter


SEEDS = (42, 43, 44)
DESCRIPTIONS = {
    "gamma-opd": ("以折扣时间信用逼近序列级 reverse-KL，再用有界奖励优势补入可验证结果。", "本地执行折扣回传和 RBM；未训练论文规模语言模型。"),
    "tlm-dre": ("按 turn 分配多尺度权重，并对正负 token 密度比采用非对称更新。", "本地执行 turn 权重与非对称 token 更新；未运行真实多轮 Agent 环境。"),
    "stride-opd": ("teacher 累积置信度越界时早停，并从最弱正确 turn 的缓存前缀重新开始。", "本地执行早停和前缀重启；未复现大模型 rollout 吞吐。"),
    "df-opd": ("由教师在自身策略空间生成问题，减少对外部后训练语料的依赖。", "本地执行自生成问题的策略特征诊断；未生成自然语言训练集。"),
    "opd-aha": ("用真实视觉与空视觉教师分布之差重建视觉偏好目标，抑制错误语言前缀的惯性。", "本地执行目标重建公式；未加载多模态 checkpoint。"),
    "growmtp": ("在 RL rollout 内按被接受的草稿深度训练 MTP head，并与主干梯度解耦。", "本地执行 depth-coupled acceptance loss；未报告 GPU 加速。"),
    "fuse-evaluator": ("用隐藏动机可验证的多 Agent 模拟评测用户转述、 framing bias 与社会推理。", "本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。"),
    "harness-bandit": ("联合 learnability、transferability 与探索 bonus 分配多 harness 训练预算。", "本地执行在线 harness 调度；没有进行大模型 RL。"),
    "sciencebuddy": ("内层递归演化交互 harness，外层用成功轨迹更新科学 Agent 策略。", "本地执行双层状态更新；没有连接真实实验室环境。"),
    "r4t": ("先以集合级复合奖励产生对齐目标，再把目标编译到单次扩散式 fan-out 检索器。", "本地执行 alignment/diversity 集合目标；没有训练 53.9M 参数扩散检索器。"),
    "loopspec": ("利用循环深度的中间预测做自推测，并以流水线残差提案隐藏验证等待。", "本地执行深度调度 reference kernel；未宣称论文 GPU 吞吐。"),
    "agentkv": ("按 Agent 阶段保留代表性 query buffer，以跨阶段查询相关性决定 KV 淘汰。", "本地执行 phase-aware scoring；未修改 SGLang 或运行 CUDA kernel。"),
}


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def aggregate(rows):
    common = set.intersection(*(set(row) for row in rows))
    output = {}
    for key in sorted(common):
        values = [row[key] for row in rows]
        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            output[f"{key}_mean"] = statistics.fmean(map(float, values))
            output[f"{key}_std"] = statistics.stdev(map(float, values))
    return output


def run_rows(record):
    rows = []
    for seed in SEEDS:
        if record["domain"] == "post-training":
            result, _ = PostTrainingRunner(PostTrainingConfig(
                algorithm=record["key"], allow_network=False, maximum_examples=128,
                steps=60, seed=seed, output_dir=ROOT / "runs/post-training",
            )).run()
            rows.append({"seed": seed, **result.final, **result.training["last_diagnostics"]})
        elif record["domain"] == "agent-research":
            result, _ = AgentResearchRunner(AgentResearchConfig(
                method=record["key"], episodes=120, seed=seed,
                output_dir=ROOT / "runs/agent-research",
            )).run()
            rows.append({"seed": seed, **result.metrics, **{
                key: value for key, value in result.diagnostics.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            }})
        else:
            rng = np.random.default_rng(seed)
            if record["key"] == "r4t":
                _, audit = r4t_targets(rng.normal(size=12), rng.normal(size=(30, 12)))
            elif record["key"] == "loopspec":
                first, second, audit = loopspec_schedule(np.linspace(.92, .45, 8))
                audit.update(first_depth=float(first), residual_depth=float(second))
            else:
                scores, audit = agentkv_scores(
                    rng.normal(size=(48, 12)),
                    {"plan": rng.normal(size=(4, 12)), "tool": rng.normal(size=(6, 12))},
                )
                audit.update(retained_top_quartile_mean=float(np.sort(scores)[-12:].mean()))
            rows.append({"seed": seed, **audit})
    return rows


def render(record, metrics_name):
    summary, boundary = DESCRIPTIONS[record["key"]]
    code = record["code"]
    upstream = f"是：[{code}]({code})" if code else "否：截至 2026-09-16 未找到原作者公开仓库"
    implementation = {
        "post-training": "src/auto_research/post_training/latest_20260916.py",
        "agent-research": "src/auto_research/agent_research/latest_20260916.py",
        "foundation-models": "src/auto_research/foundation_latest_20260916.py",
    }[record["domain"]]
    return f"""# {record['title']}

> **复现级别：L1 核心机制诊断。** {boundary}

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [{record['title']}]({record['paper_url']}) |
| 公司/机构 | {record['first_author_affiliation']}（按第一作者署名单位） |
| 首次公开日期 | {record['published']}（arXiv v1） |
| 原文开源代码 | {upstream} |
| Adapter / 方法 | `{record['adapter']}` |
| 本地复现代码 | [`{implementation}`](https://github.com/daiwk/auto-research/blob/main/{implementation}) |

## 原始论文总结

### 背景与主要改动

{summary}

本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。

```mermaid
flowchart LR
  I[公开输入与状态] --> M[{record['adapter']} 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或策略更新]
```

### 核心公式

实现保留论文的决定性状态转换，并输出权重、门控、深度、阶段或缓存统计；固定预算和三种子只用于检查机制不变量，不等同于论文规模训练。

### 论文离线与线上效果

论文报告的能力、速度或成本结论只作为原文事实记录；本地指标不与其直接横比，也不外推线上收益。

## 本地复现

三种子结果见 [`metrics/{metrics_name}`](metrics/{metrics_name})。统一 receipt 标记 `diagnostic_only=true`，不会被公开看板当成完整能力提升。

### 复现边界

{boundary}
"""


def render_industrial(key, runs):
    adapter = get_adapter(key)
    row = adapter.paper
    upstream = "否：截至 2026-09-16 未找到原作者公开仓库"
    result = runs[0]
    baseline = result["baseline"]["ndcg_at_10"]
    proposed = result["method"]["ndcg_at_10"]
    lift = (proposed / baseline - 1.0) * 100 if baseline else 0.0
    focus = {
        "gese": "集合级多样性/忠实度探索后，再以当前上下文选择个性化标题；生产系统报告 CTR +2.57%、停留时长 +0.87%。",
        "lazformer": "先做可迁移生成式预训练，再用 ranking residual adapter、近密远疏 token 与 hybrid sparse attention 适配排序；两周 A/B 报告 IPV +5.21%、GMV +9.85%。",
    }[key]
    return f"""# {row.title}

> **复现级别：公开数据核心机制。** 私有日志、生产 checkpoint 与 serving 栈均未复刻。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1]({row.url}) |
| 公司/机构 | {row.organization}（第一作者署名单位） |
| 首次公开日期 | {row.published}（arXiv v1） |
| 原文开源代码 | {upstream} |
| Adapter | `{key}` |
| 本地复现代码 | [`src/auto_research/reproductions/{key}/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/{key}/) |

## 原始论文总结

### 背景与主要改动

{focus}

```mermaid
flowchart LR
  H[公开历史序列] --> M[{key} 核心机制]
  M --> R[统一候选打分]
  R --> E[同切分离线评测]
```

### 核心公式

本地实现把论文的核心机制约束为确定性候选打分：GESE 显式组合 relevance、集合多样性、faithfulness 与上下文 selector；LazFormer 分离可迁移预训练映射和 ranking residual adapter，并只在 validation 选择融合系数。

### 论文离线与线上效果

论文线上结论来自正文生产 A/B；本地只报告同一公开候选集和切分上的离线指标，不把二者混为同一种提升。

## 本地复现

### 线上与本地结果

线上数字来自论文正文 A/B，不与本地 MovieLens 结果混写。本地 seeds 42/43/44 见 [`metrics/movielens-100k-seeds42-44.json`](metrics/movielens-100k-seeds42-44.json)。首个 seed 的统一 NDCG@10 基线为 {baseline:.5f}，实验组为 {proposed:.5f}，相对变化 {lift:+.2f}%。

> **本地对照口径**：同一公开候选集、同一切分下，基线 NDCG@10={baseline:.5f}，实验组 NDCG@10={proposed:.5f}，相对变化 {lift:+.2f}%。

## 复现边界

本地只验证公开数据上的核心状态转换；未复刻私有训练数据、大模型生成器、生产流量反馈或在线服务。当前不映射 evolve，避免 registry-only 标签。
"""


def main():
    for record in LATEST_METHOD_PAPERS:
        rows = run_rows(record)
        detail = ROOT / "docs" / record["detail_path"]
        detail.parent.mkdir(parents=True, exist_ok=True)
        metric_name = "mechanism-seeds42-44.json"
        detail.write_text(render(record, metric_name), encoding="utf-8")
        artifact = detail.parent / "metrics" / metric_name
        write_json(artifact, {
            "schema_version": 2, "method": record["key"],
            "dataset": "deterministic mechanism mini-suite", "seeds": list(SEEDS),
            "runs": rows, "aggregate_metrics": aggregate(rows),
            "manifest_ref": f"{record['domain']}:{record['key']}",
            "evaluation_protocol": {
                "tier": "l1_mechanism", "seeds": list(SEEDS),
                "formal_comparison": False, "diagnostic_only": True,
                "claim_policy": "mechanism execution only; not a paper-scale capability result",
            },
            "provenance": {
                "commit": "working tree before commit",
                "command": "PYTHONPATH=src python scripts/generate_sep_16_2026_artifacts.py",
                "artifact_path": artifact.relative_to(ROOT).as_posix(),
                "dataset_fingerprint": "deterministic-sep16-mechanism-mini-suite-v1",
            },
        })

    for key in ("gese", "lazformer"):
        adapter = get_adapter(key)
        runs = [adapter.run(ROOT / "data", seed) for seed in SEEDS]
        detail = ROOT / f"docs/reproductions/{adapter.paper.arxiv_id}-{key}"
        detail.mkdir(parents=True, exist_ok=True)
        detail.joinpath("README.md").write_text(render_industrial(key, runs), encoding="utf-8")
        artifact = detail / "metrics/movielens-100k-seeds42-44.json"
        write_json(artifact, {
            "schema_version":2,"method":key,"dataset":"MovieLens 100K","seeds":list(SEEDS),
            "runs":runs,"manifest_ref":f"reproduction:{key}",
            "evaluation_protocol": {
                "tier": "l2_public_dataset", "seeds": list(SEEDS),
                "formal_comparison": False, "diagnostic_only": False,
                "claim_policy": "public-data core mechanism; online numbers are paper-only",
            },
            "provenance": {
                "commit": "working tree before commit",
                "command": "PYTHONPATH=src python scripts/generate_sep_16_2026_artifacts.py",
                "artifact_path": artifact.relative_to(ROOT).as_posix(),
                "dataset_fingerprint": "movielens-100k-public-subset-v1",
            },
        })


if __name__ == "__main__":
    main()
