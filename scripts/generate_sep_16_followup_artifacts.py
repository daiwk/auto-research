#!/usr/bin/env python3
"""Generate L1 docs and receipts for the Sep-16 follow-up batch."""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.foundation_latest_20260916_followup import (
    echo_candidates, echo_lossless_verify, persistent_recurrent_memory,
    register_chunk, reproducible_reduce, stacktok_select, videomm_select,
)
from auto_research.latest_20260916_followup_catalog import LATEST_METHOD_PAPERS
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner

SEEDS = (42, 43, 44)
SUMMARY = {
    "echo": "用早层高频探索与末层低频权威校验组成双循环；两侧 bonus logits 协同补树，并保留精确拒绝采样校正。",
    "videomm": "先在低分辨率 Macro Proxy 上定位相关区域，仅在宏观共识不足时激活高保真 Micro Tokens。",
    "tiao": "通过遮蔽源文档前后的 token 概率变化估计依赖性，同时重塑轨迹优势并聚焦重要 token 更新。",
    "repoatlas": "在固定预算下执行 select–project–refresh，把任务相关代码子图同步投影为视觉拓扑与精确文本索引。",
    "stacktok": "把 query relevance 作为目标、coverage 作为随预算变化的支撑约束，逐步在两种选取准则间切换。",
    "interactive-memory": "Planner 决定写入高价值记忆，Trigger 决定何时取回，两者通过跨会话延迟奖励共同演化。",
    "sd-dpo": "识别事实正确但风格不同的 rejected response，反转其偏好方向并按组比例加权以抵消风格梯度。",
    "open-1b-audit": "固定 kernel reduction、数据批次与集体通信顺序，并用逐步状态哈希支持异构硬件单步重放审计。",
    "persistent-recurrent-memory": "在 Transformer 上下半层之间插入 observe–GRU update–gated influence 的持久状态通路。",
    "register-tokens-dllm": "清除上一段文本后仅携带固定数量的连续 register hidden states，让扩散语言模型跨 chunk 推理。",
}
BOUNDARY = {
    "echo": "本地执行候选合并和 lossless 校正；CUDA receipt 只验证 tensor 路径，不复述论文吞吐。",
    "videomm": "本地执行 macro 选择和 micro 激活；不加载完整视频 MLLM，也不外推 LongVideoBench 效果。",
    "tiao": "本地执行 token dependency 与双尺度 credit；未训练 7B 模型。",
    "repoatlas": "本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。",
    "stacktok": "本地执行单 crop 的 reference-gated selector；未加载五个论文 VLM。",
    "interactive-memory": "本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。",
    "sd-dpo": "本地执行偏好反转和组平衡损失；事实分数由 fixture 提供，不冒充 judge LLM。",
    "open-1b-audit": "本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。",
    "persistent-recurrent-memory": "本地执行拓扑 reference kernel；未复现 TinyStories 完整训练曲线。",
    "register-tokens-dllm": "本地执行 bounded continuous carry；未加载 LLaDA/Dream checkpoint 或 diffu-GRPO。",
}


def aggregate(rows):
    numeric = set.intersection(*(set(row) for row in rows))
    output = {}
    for key in sorted(numeric):
        values = [row[key] for row in rows]
        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            output[f"{key}_mean"] = statistics.fmean(map(float, values))
            output[f"{key}_std"] = statistics.stdev(map(float, values))
    return output


def run_foundation(key, seed):
    rng = np.random.default_rng(seed)
    if key == "echo":
        early, final = rng.normal(size=16), rng.normal(size=16)
        _, audit = echo_candidates(early, final, (1, 3), 4)
        draft = np.stack([np.random.default_rng(seed + i).dirichlet(np.ones(16)) for i in range(4)])
        target = np.stack([np.random.default_rng(seed + 20 + i).dirichlet(np.ones(16)) for i in range(4)])
        _, _, verify = echo_lossless_verify(draft, target, rng.random(4))
        return {**audit, **verify}
    if key == "videomm":
        _, _, audit = videomm_select(rng.normal(size=(48, 12)), rng.normal(size=12), 4, 3)
        return audit
    if key == "stacktok":
        _, audit = stacktok_select(rng.normal(size=(40, 12)), rng.normal(size=12), 8)
        return audit
    if key == "persistent-recurrent-memory":
        _, _, audit = persistent_recurrent_memory(rng.normal(size=(16, 8)), rng.normal(size=8), rng.normal(size=(8, 8)), rng.normal(size=(8, 8)), rng.normal(size=8))
        return audit
    if key == "register-tokens-dllm":
        _, audit = register_chunk(rng.normal(size=(4, 8)), rng.normal(size=(16, 8)), rng.normal(size=(8, 8)))
        return audit
    _, audit = reproducible_reduce([rng.normal(size=32) for _ in range(4)])
    return {key: value for key, value in audit.items() if isinstance(value, (int, float, bool))}


def run_rows(record):
    rows = []
    for seed in SEEDS:
        if record["domain"] == "post-training":
            result, _ = PostTrainingRunner(PostTrainingConfig(algorithm=record["key"], allow_network=False, maximum_examples=128, steps=60, seed=seed, output_dir=ROOT / "runs/post-training")).run()
            row = {**result.final, **result.training["last_diagnostics"]}
        elif record["domain"] == "agent-research":
            result, _ = AgentResearchRunner(AgentResearchConfig(method=record["key"], episodes=120, seed=seed, output_dir=ROOT / "runs/agent-research")).run()
            row = {**result.metrics, **{key: value for key, value in result.diagnostics.items() if isinstance(value, (int, float)) and not isinstance(value, bool)}}
        else:
            row = run_foundation(record["key"], seed)
        rows.append({"seed": seed, **row})
    return rows


def render(record, metric_name):
    upstream = f"是：[{record['code']}]({record['code']})" if record.get("code") else "否：截至 2026-09-16 未找到原作者公开仓库"
    if record.get("code_extra"):
        upstream += f"；审计工具：[{record['code_extra']}]({record['code_extra']})"
    implementation = {
        "post-training": "src/auto_research/post_training/latest_20260916_followup.py",
        "agent-research": "src/auto_research/agent_research/latest_20260916_followup.py",
    }.get(record["domain"], "src/auto_research/foundation_latest_20260916_followup.py")
    gpu = "\n\nCUDA 路径的真实机器验证见本页论文信息所对应的 `docs/gpu-validations/` receipt；receipt 不包含主机名、SSH alias 或驱动/build 字符串。" if record.get("requires_gpu_validation") else ""
    return f"""# {record['title']}

> **复现级别：L1 核心机制诊断。** {BOUNDARY[record['key']]}

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

{SUMMARY[record['key']]}

```mermaid
flowchart LR
  I[公开输入与当前状态] --> M[{record['adapter']} 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

### 核心公式与实现对应

本地 reference kernel 保留决定性的排序、门控、偏好方向、信用权重或状态转换，并输出可审计统计。三种子 fixture 用来验证不变量和边界，不把随机 mini-suite 分数解释成论文能力。

### 论文效果

论文中的准确率、速度、训练损失或 benchmark 结论只作为原文结果；本地结果不与其直接横比，也不外推线上收益。

## 本地复现

三种子结果见 [`metrics/{metric_name}`](metrics/{metric_name})。统一 receipt 标记 `diagnostic_only=true`，不能进入正式能力排名。{gpu}

## 复现边界

{BOUNDARY[record['key']]}
"""


def main():
    for record in LATEST_METHOD_PAPERS:
        rows = run_rows(record)
        detail = ROOT / "docs" / record["detail_path"]
        detail.parent.mkdir(parents=True, exist_ok=True)
        metric_name = "mechanism-seeds42-44.json"
        detail.write_text(render(record, metric_name), encoding="utf-8")
        artifact = detail.parent / "metrics" / metric_name
        artifact.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 2, "method": record["key"], "dataset": "deterministic mechanism mini-suite", "seeds": list(SEEDS),
            "runs": rows, "aggregate_metrics": aggregate(rows), "manifest_ref": f"{record['domain']}:{record['key']}",
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": list(SEEDS), "formal_comparison": False, "diagnostic_only": True, "claim_policy": "mechanism execution only; not a paper-scale capability result"},
            "provenance": {"commit": "working tree before commit", "command": "PYTHONPATH=src python scripts/generate_sep_16_followup_artifacts.py", "artifact_path": artifact.relative_to(ROOT).as_posix(), "dataset_fingerprint": "deterministic-sep16-followup-mini-suite-v1"},
        }
        artifact.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

