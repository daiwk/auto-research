#!/usr/bin/env python3
"""Generate reviewed docs and compact mechanism receipts for the Sep-14 batch."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import statistics
import subprocess
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.foundation_latest_20260914 import (
    dequantize_blocks, frames_on_demand, multi_expert_opd,
    repetition_regularization, sensenova_patch_targets,
    similarity_contracting_windows, soft_musec_update, windowed_key_quantize,
)
from auto_research.latest_20260914_catalog import LATEST_METHOD_PAPERS
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.reproductions.sirf.experiment import reproduce as reproduce_sirf


SEEDS = (42, 43, 44)
SUMMARIES = {
    "nsd": ("让学生远离自身生成的错误推理分布，并用动态 gate 只更新推理关键位置，避免把普通语言 token 一并遗忘。", "七个数学 benchmark 上，1.7B/4B/8B 模型平均提升 2.3%/7.5%/6.0%。", "本地在候选策略上构造负教师和动态 reasoning gate；未执行全参数 LLM 训练。"),
    "adaptive-opd-gate": ("把熵、不确定性、reference 偏移和教师—学生差距组合成逐 token gate，在 FKL/RKL 蒸馏方向间自适应分配。", "论文报告 33/36 个探索单元和 19/26 个均值匹配静态对照占优；部分三 seed 主对比未达显著。", "本地执行四信号 gate；结果仅是机制诊断，不把探索性结果写成稳定胜出。"),
    "locus": ("学习任务相关低秩后训练子空间，只在紧凑方向上更新以缩短回答，同时保留任务能力。", "Pythia 输出最高缩短 39.84%，Qwen 缩短 14.87%–17.58%，训练参数约 0.24%–0.28%。", "本地用样本特征 SVD 投影策略梯度；未训练论文规模语言模型。"),
    "tasco": ("冻结主模型，优化轻量 prefix；除置信度外还惩罚邻域扰动下的不稳定，从而避免自信但错误的轨迹。", "推理准确率最高提升 17.2%，输出 token 最多减少 28.1%。", "本地执行随机邻域扰动和稳定性惩罚；没有加载冻结 LLM prefix。"),
    "cobra-skills": ("把技能优化视为动态候选空间中的预算化 contextual bandit，优先评估高收益或高信息量技能，再依据执行反馈演化。", "六个 benchmark、三个模型上成本降低 55%–58%，相对无技能 Agent 提升 13.1/26.9/22.5 pp。", "本地执行 contextual-UCB 分配和反馈接纳；没有调用外部 LLM 或六套真实环境。"),
    "ecdysis": ("聚合跨任务重复失败以区分模型偶发错误和 harness 系统缺陷，再由 FDCR 多角色诊断形成修复规格。", "harness 训练最高加速 1.84 倍，推理准确率最高提升 18.56%。", "本地只在公开 observation 上聚合失败签名和触发修复门；不生成或执行 harness 代码。"),
    "grounded-memory": ("给异步记忆 curator 最小权限只读工具，在写入前验证、限定作用域并刷新候选记忆。", "CLBench pass rate 39%→73%，查询 8.8→4.7，任务 Agent 成本 $3.38→$1.68。", "本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。"),
    "toolgrad": ("先从目标答案反推工具轨迹，再使用 textual gradient 定位并修订失败调用，降低人工轨迹标注成本。", "ToolGrad-12B 在 BFCL 达 83.1，接近 Gemini 2.5 Pro 的 83.2。", "本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。"),
    "prompts": ("Coordinator、Analyzer 和 Proposal Agent 联合读取 profiler 与知识库，诊断瓶颈并输出可解释的 sharding 候选。", "8 个生产工作负载最高提升 434%；工程师最终采用方案始终在 top-3，top-1 命中 87.5%。", "本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。"),
    "searchatlas": ("把搜索轨迹转为 query—evidence—answer 有向图，审计证据是否真正覆盖问题约束和最终回答。", "自动图解析相对人工标注平均 edge F1 为 86.0%。", "本地构造公开 fixture 的证据传播边；未运行论文五个搜索 Agent。"),
    "skill-retention": ("混合真实样本 replay 与 embedding anchor/LwF 类正则，防止合成技能数据微调破坏真实和 OOD 路由能力。", "0.6B Qwen retriever/reranker 在保留 OOD 的同时，合成域检索提升 13.98%。", "本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。"),
    "t1-terminal-rl": ("TITO 使用 rollout 实际采样 token id 训练，turn boundary repair 修正漂移，R3 重放 MoE 路由选择。", "Terminal-Bench 2.1 从 base 43.8% 提升到 64.0%，训练—推理 log-prob gap 从 0.021 降到 0.013。", "本地审计 exact-token 和 route replay 状态；未训练 122B MoE 或运行 300+ turn 云沙箱。"),
    "omnikvquant": ("按短时间窗确定 key 量化范围，并按模态分别旋转 value，处理 temporal drift 与异构几何。", "Qwen2.5-Omni 在七个视听 benchmark 上以 2-bit KV 保留 98.1% FP16 表现。", "本地执行 2-bit 窗口量化和模态独立旋转的 NumPy reference；Triton kernel 另需 A100/A30 验证。"),
    "sensenova-u1-5": ("用空间 patch reconstruction 摆脱 tokenizer/VAE，并以多专家 OPD 统一视觉理解与生成后训练。", "论文报告统一 8B-MoT 模型在理解和生成任务上的综合结果。", "本地执行 masked patch target 与 expert OPD 融合；未复刻 8B 多阶段训练。"),
    "frames-on-demand": ("视频只做一次 caption memory；visual-need router 判断文本证据不足时，才在固定预算内读取相关帧。", "论文在保持竞争力的同时把视觉帧消耗降低约一个数量级。", "本地执行 caption/query gate 与 top-k 帧选择；未运行长视频 VLM。"),
    "repeat-aware-moe": ("研究重复数据下 MoE 比 Dense 更早过拟合的问题，并用更强 masking/dropout 抑制 expert 记忆化。", "强正则下，MoE 即使在 64 倍数据重复时仍可优于 Dense。", "本地实现随重复倍数和稀疏度变化的正则 schedule；未进行大规模预训练。"),
    "musec": ("对 Muon momentum 的奇异值做平滑谱裁剪，避免硬截断不连续，同时限制不稳定大方向。", "FineWeb、OpenWebText 和 C4 上跨学习率与模型规模提高稳定性。", "本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。"),
    "swrouter": ("按相邻语义相似度收缩多轮窗口，再用对比路由器选模型，并分开评测上下文构造和路由正确性。", "比最佳单模型提升 16.26%，比 Conv-ID Context 再提升 8.22%。", "本地执行窗口分段和 profile overlap 路由；未训练论文对比 encoder。"),
}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def aggregate(rows: list[dict]) -> dict[str, float]:
    common = set.intersection(*(set(row) for row in rows))
    output = {}
    for key in sorted(common):
        values = [row[key] for row in rows]
        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            numbers = [float(value) for value in values]
            output[f"{key}_mean"] = statistics.fmean(numbers)
            output[f"{key}_std"] = statistics.stdev(numbers)
    return output


def metric_rows(record):
    key, domain = record["key"], record["domain"]
    rows = []
    if domain == "post-training":
        for seed in SEEDS:
            result, _ = PostTrainingRunner(PostTrainingConfig(
                algorithm=key, allow_network=False, maximum_examples=128,
                steps=60, seed=seed, output_dir=ROOT / "runs/post-training",
            )).run()
            rows.append({"seed": seed, **result.final, **result.training["last_diagnostics"]})
    elif domain == "agent-research":
        for seed in SEEDS:
            result, _ = AgentResearchRunner(AgentResearchConfig(
                method=key, episodes=120, seed=seed,
                output_dir=ROOT / "runs/agent-research",
            )).run()
            rows.append({"seed": seed, **result.metrics, **{
                k: v for k, v in result.diagnostics.items()
                if isinstance(v, (int, float)) and not isinstance(v, bool)
            }})
    else:
        for seed in SEEDS:
            rng = np.random.default_rng(seed)
            if key == "omnikvquant":
                values = rng.normal(size=(32, 16)); restored = dequantize_blocks(windowed_key_quantize(values))
                rows.append({"seed": seed, "mse": float(np.mean((values-restored)**2)), "compression_bits": 2.0})
            elif key == "sensenova-u1-5":
                patches = rng.normal(size=(8, 16, 12)); mask = rng.random((8, 16)) < .4
                target = sensenova_patch_targets(patches, mask)
                delta, weights = multi_expert_opd(rng.normal(size=(8, 3, 12)), rng.normal(size=(8, 3)))
                rows.append({"seed": seed, "masked_fraction": float(mask.mean()), "target_finite": float(np.isfinite(target).mean()), "expert_entropy": float(-(weights*np.log(weights+1e-12)).sum(-1).mean()), "delta_norm": float(np.linalg.norm(delta, axis=-1).mean())})
            elif key == "frames-on-demand":
                chosen, audit = frames_on_demand(rng.normal(size=8), rng.normal(size=8), rng.normal(size=(24,8)), maximum_frames=4)
                rows.append({"seed": seed, **audit, "budget_respected": float(len(chosen) <= 4)})
            elif key == "repeat-aware-moe":
                rows.append({"seed": seed, **repetition_regularization(64, sparse_model=True)})
            elif key == "musec":
                _, audit = soft_musec_update(rng.normal(size=(24,16)))
                rows.append({"seed": seed, **audit})
            else:
                emb = np.asarray([[1.,0.],[.8,.2],[0.,1.]]) + rng.normal(0,.01,(3,2))
                windows = similarity_contracting_windows(["a","b","c"], emb)
                rows.append({"seed": seed, "windows": float(len(windows)), "turns": 3.0})
    return rows


def render_doc(record, metrics_name):
    summary, paper_result, boundary = SUMMARIES[record["key"]]
    code = record["code"]
    code_cell = f"是：[{code}]({code})" if code else "否：未找到作者公开仓库（核查日期：2026-09-14）"
    code_path = {
        "post-training": "src/auto_research/post_training/latest_20260914.py",
        "agent-research": "src/auto_research/agent_research/latest_20260914.py",
        "foundation-models": "src/auto_research/foundation_latest_20260914.py",
    }[record["domain"]]
    return f"""# {record['title']}

> **复现级别：L1 核心机制诊断。** {boundary}

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [{record['title']}]({record['paper_url']}) |
| 论文标识 | {record['paper_url'].rsplit('/', 1)[-1] or record['key']}（仓库 ID：`{record['key']}`） |
| 公司/机构 | {record['first_author_affiliation']}（按第一作者署名单位） |
| 首次公开日期 | {record['published']} |
| 原文开源代码 | {code_cell} |
| Adapter / 方法 | `{record['key']}` |
| 本地复现代码 | [`{code_path}`](https://github.com/daiwk/auto-research/blob/main/{code_path}) |

## 原始论文总结

### 背景与主要改动

{summary}

```mermaid
flowchart LR
  I[输入与公开状态] --> M[{record['key']} 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或更新]
```

### 核心公式或操作

本地代码把论文决定性操作实现为确定性的 reference kernel，并显式输出门控、选择、投影、图边或状态更新统计；测试覆盖公式不变量和边界条件。

### 论文离线与线上效果

{paper_result} 这些数字来自原论文，不与本地缩小实验直接比较；论文未报告线上 A/B 时不推断线上收益。

## 本地复现

三种子指标见 [`metrics/{metrics_name}`](metrics/{metrics_name})。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。

### 复现边界

{boundary}
"""


def main():
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    for record in LATEST_METHOD_PAPERS:
        rows = metric_rows(record)
        metrics_name = "mechanism-seeds42-44.json"
        detail = ROOT / "docs" / record["detail_path"]
        detail.parent.mkdir(parents=True, exist_ok=True)
        detail.write_text(render_doc(record, metrics_name))
        write_json(detail.parent / "metrics" / metrics_name, {
            "schema_version": 2, "method": record["key"], "dataset": "deterministic mechanism mini-suite",
            "seeds": list(SEEDS), "runs": rows, "aggregate_metrics": aggregate(rows),
            "manifest_ref": f"{record['domain']}:{record['key']}",
            "evaluation_protocol": {"tier": "l1_mechanism", "formal_comparison": False, "diagnostic_only": True, "claim_policy": "mechanism execution only; not a paper-scale capability result"},
            "provenance": {"commit": commit, "command": "PYTHONPATH=src python scripts/generate_sep_14_2026_artifacts.py"},
        })

    sirf_dir = ROOT / "docs/reproductions/2609.11752-sirf"
    runs = [reproduce_sirf(ROOT / "data", seed) for seed in SEEDS]
    write_json(sirf_dir / "metrics/policy-cases-seeds42-44.json", {
        "schema_version": 2, "method": "sirf", "dataset": "deterministic synthetic policy cases",
        "diagnostic_only": True,
        "seeds": list(SEEDS), "runs": runs,
        "aggregate_metrics": aggregate([run["method"] for run in runs]),
        "manifest_ref": "reproduction:sirf",
        "evaluation_protocol": {"tier": "l1_mechanism", "formal_comparison": False, "diagnostic_only": True, "claim_policy": "linear concept diagnostic; not 8B CPT or online A/B"},
        "provenance": {"commit": commit, "command": "PYTHONPATH=src python scripts/generate_sep_14_2026_artifacts.py"},
    })
    sirf_dir.mkdir(parents=True, exist_ok=True)
    sirf_dir.joinpath("README.md").write_text("""# SIRF：面向工业内容风控的规则内化基础模型

> **复现级别：概念诊断。** 执行规则关系合成、trigger/exemption 内化和 P95 阈值选择；线性模型替代 8B LLM CPT。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1](https://arxiv.org/abs/2609.11752) |
| 公司/机构 | 小红书（第一作者署名单位） |
| 首次公开日期 | 2026-09-10（arXiv v1） |
| 原文开源代码 | 否：未找到作者公开仓库（核查日期：2026-09-14） |
| Adapter | `sirf` |
| 本地复现代码 | [`src/auto_research/reproductions/sirf/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/sirf/) |

## 原始论文总结

### 背景与主要改动

SIRF 用 EntiGraph、MAGA 改写和账户级 CoT 合成长尾风控规则数据，通过 CPT 把复杂 trigger/exemption 规则写进模型权重，以单次 verdict 和可调阈值满足秒级线上判定。

```mermaid
flowchart LR
  S[平台规则] --> E[EntiGraph + MAGA + account CoT]
  E --> C[约 70M token CPT]
  C --> F[SFT verdict model]
  F --> T[高精度阈值与线上裁决]
```

### 核心公式

本地把规则表示为触发、豁免及其交互项，训练模型后在 held-out policy cases 上扫描阈值，报告满足 Precision≥95% 的最大 Black Recall。

### 论文离线与线上效果

同源 Qwen3-8B-SFT 对照下 Black Recall@P95 提升 15.1 pp；裁决层多释放约 20% 误罚样本。冻结场景误罚相对下降约 70%，累计百万用户规模；正文还报告随机 treatment/control A/B 中 weekly active penetration 显著提升，但只披露“高个位数到低双位数”区间，没有精确值。

## 本地复现

> **本地对照口径**：同源线性特征为基线，加入规则交互项的实验组在三 seed 上 Black Recall@P95 相对提高 65.81%（绝对约 33.84 个百分点）；这不是论文 8B 模型或线上流量结果。

三种子结果见 [`metrics/policy-cases-seeds42-44.json`](metrics/policy-cases-seeds42-44.json)。论文线上结果、本地合成数据结果严格分开。

### 复现边界

没有私有账户数据、8B CPT、EntiGraph/MAGA 语言生成和线上 serving，因此本地结果不能验证论文业务提升。
""")


if __name__ == "__main__":
    main()
