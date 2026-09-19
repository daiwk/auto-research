#!/usr/bin/env python3
"""Generate documentation and L1/L2 artifacts for the Sep-19 batch."""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.foundation_latest_20260919 import aspire_schedule, dqwen35_hybrid, fit_recall_head, on_demand_attention
from auto_research.latest_20260919_catalog import ANGLE_PAPER, LATEST_METHOD_PAPERS
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.reproductions.latest_20260919 import make_adapter

SEEDS = (42, 43, 44)
SUMMARY = {
    "angle":"以意图标识×摘要标识组织广告语义层次，用生成、判别和排序联合目标训练，并在请求侧动态约束 beam 只产生合法标识。",
    "retire-opd":"给不同技能配置解耦教师；学生同时执行 RL 与 on-policy distillation，当成功率接近教师且分布差距不再收缩时自动退休教师。",
    "oda":"默认只读局部 KV，由轻量 recall head 在全局注意力发生前预测其收益；仅高收益 token 触发全局读取，完整 KV 仍保留。",
    "evoskill-gui":"把 GUI 技能拆成可编辑组件，执行失败后由信息隔离 critic 反思，并只修改责任组件，验证后的技能可跨任务复用。",
    "compo":"不求偏好目标梯度，只比较正负参数扰动的结果得到一比特方向，再以逐坐标阈值抑制噪声。",
    "trajectory-learnability":"用成功轨迹训练参考模型，以参考与当前策略逐 token 对数似然变化衡量可学性，并据此重加权离线 OPD 轨迹。",
    "dependency-refinement":"把多轮轨迹表示为轮级依赖 DAG，依次执行叶节点裁剪、严格合并和宽松合并，减少冗余消息同时保留最终答案依赖。",
    "harness-design-study":"固定底层执行循环，分别控制 planning、action space 与 context management，隔离 coding-agent harness 中真正影响效果和成本的因素。",
    "cera-moa":"用中层隐藏状态估计 Agent 对样本的熟悉度，以累计阈值自适应选专家，并把训练样本定向分配给相应专家。",
    "dqwen35":"把 Qwen3.5 的注意力/RNN 混合骨干改成双向状态传播，再以掩码去噪目标训练为 diffusion language model。",
    "aspire":"每个请求依据在线接受率与当前 batch 成本独立选择 draft 长度，并周期性用全注意力 refresh layer 校正自推测状态。",
}
BOUNDARY = {
    "angle":"本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。",
    "retire-opd":"本地执行退休判据与学生更新；未训练论文规模 Agent 教师。",
    "oda":"本地执行 recall gate 和条件全局注意力；真实 A100 receipt 只证明 CUDA 路径，不外推 vLLM 吞吐。",
    "evoskill-gui":"本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。",
    "compo":"本地执行一比特比较 oracle 与阈值化更新；mini-suite 不是大模型对齐结果。",
    "trajectory-learnability":"本地执行逐 token 可学性聚合和轨迹加权；未复刻论文 GPU 训练预算。",
    "dependency-refinement":"本地执行依赖裁剪与合并；DAG 来自可审计 fixture，不冒充 LLM 标注器。",
    "harness-design-study":"本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。",
    "cera-moa":"本地执行熟悉度路由与定向更新；未训练论文规模专家策略。",
    "dqwen35":"本地执行双向混合状态 CUDA kernel；未加载 9B checkpoint 或复现预训练损失曲线。",
    "aspire":"本地执行 batch-aware scheduler 与 refresh gate；未改造 vLLM serving engine。",
}


def aggregate(rows):
    common = set.intersection(*(set(row) for row in rows)); output = {}
    for key in sorted(common):
        values = [row[key] for row in rows]
        if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
            output[f"{key}_mean"] = statistics.fmean(map(float, values)); output[f"{key}_std"] = statistics.stdev(map(float, values))
    return output


def foundation_row(key, seed):
    rng = np.random.default_rng(seed)
    if key == "oda":
        local = rng.normal(size=(12, 8)); gain = rng.normal(size=12); head = fit_recall_head(local, gain)
        _, audit = on_demand_attention(rng.normal(size=8), rng.normal(size=(16,8)), rng.normal(size=(16,8)), rng.normal(size=(64,8)), rng.normal(size=(64,8)), head)
        return audit
    if key == "dqwen35":
        _, audit = dqwen35_hybrid(rng.normal(size=(24,8)), rng.normal(size=(8,8))/8, rng.normal(size=(8,8))/8)
        return audit
    _, _, audit = aspire_schedule(rng.uniform(.3,.95,16), .1, 1.0, rng.integers(1,9,16))
    return audit


def rows(record):
    output = []
    for seed in SEEDS:
        if record["domain"] == "post-training":
            result, _ = PostTrainingRunner(PostTrainingConfig(algorithm=record["key"], allow_network=False, maximum_examples=64, steps=20, seed=seed, output_dir=ROOT/"runs/post-training")).run()
            row = {**result.final, **result.training["last_diagnostics"]}
        elif record["domain"] == "agent-research":
            result, _ = AgentResearchRunner(AgentResearchConfig(method=record["key"], episodes=36, seed=seed, output_dir=ROOT/"runs/agent-research")).run()
            row = {**result.metrics, **{k:v for k,v in result.diagnostics.items() if isinstance(v,(int,float)) and not isinstance(v,bool)}}
        elif record["domain"] == "recommendation":
            result = make_adapter().run(ROOT/"data", seed)
            row = {**{k:v for k,v in result["method"].items() if isinstance(v,(int,float)) and not isinstance(v,bool)}, **{k:v for k,v in result["stages"].items() if isinstance(v,(int,float)) and not isinstance(v,bool)}}
        else:
            row = foundation_row(record["key"], seed)
        output.append({"seed":seed, **row})
    return output


def render(record, metric_name):
    upstream = f"是：[{record['code']}]({record['code']})" if record.get("code") else "否：截至 2026-09-19 未找到原作者公开实现仓库"
    checkpoint = f"\n| 原文公开 checkpoint | [{record['checkpoint']}]({record['checkpoint']}) |" if record.get("checkpoint") else ""
    implementation = {"recommendation":"src/auto_research/reproductions/latest_20260919.py","post-training":"src/auto_research/post_training/latest_20260919.py","agent-research":"src/auto_research/agent_research/latest_20260919.py"}.get(record["domain"], "src/auto_research/foundation_latest_20260919.py")
    tier = "L2 公开数据集核心机制" if record["domain"] == "recommendation" else "L1 核心机制诊断"
    gpu = "\n\nCUDA 路径已在真实 NVIDIA A100 上运行；脱敏 receipt 见 `docs/gpu-validations/`。" if record.get("requires_gpu_validation") else ""
    if record["domain"] == "recommendation":
        return f"""# {record['title']}

> **复现级别：公开数据核心机制。** {BOUNDARY[record['key']]}

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1]({record['paper_url']}) |
| 公司/机构 | Tencent（第一作者署名单位） |
| 首次公开日期 | 2026-09-16（arXiv v1） |
| 原文开源代码 | 否：截至 2026-09-19 未找到原作者公开仓库 |
| Adapter | `angle` |
| 本地复现代码 | [`src/auto_research/reproductions/angle/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/angle/) |

## 原始论文总结

### 背景与主要改动

{SUMMARY['angle']}

```mermaid
flowchart LR
  H[公开历史序列] --> I[意图×摘要层次标识]
  I --> J[生成+判别+排序联合打分]
  J --> B[动态约束 beam]
  B --> E[同切分离线评测]
```

### 核心公式

本地以 `s = s_gen + 0.15 s_dis` 保留生成相关性与层次标识判别信号，再由请求相关合法标识集合约束 beam；融合系数只在 validation 上选择。

### 论文离线与线上效果

论文在 Weixin Top Stories 线上 A/B 报告消费 +1.81%、GMV +2.16%、点击 +1.50%、转化 +1.44%、曝光 +2.49%。这些是原文生产结果，不等于本地 MovieLens 指标。

## 本地复现

本地 seeds 42/43/44 见 [`metrics/{metric_name}`](metrics/{metric_name})。

> **本地对照口径**：同一 MovieLens 100K 候选集和时间切分下，基线与实验组使用相同评测；本地相对变化记录在指标文件中，不以论文线上 % 替代。

## 复现边界

{BOUNDARY['angle']}
"""
    return f"""# {record['title']}

> **复现级别：{tier}。** {BOUNDARY[record['key']]}

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [{record['title']}]({record['paper_url']}) |
| 公司/机构 | {record['first_author_affiliation']}（按第一作者署名单位） |
| 首次公开日期 | {record['published']}（arXiv v1） |
| 原文开源代码 | {upstream} |{checkpoint}
| Adapter / 方法 | `{record['adapter']}` |
| 本地复现代码 | [`{implementation}`](https://github.com/daiwk/auto-research/blob/main/{implementation}) |

## 原始论文总结

### 背景与主要改动

{SUMMARY[record['key']]}

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[{record['adapter']} 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/状态更新]
```

### 核心公式

本地 reference kernel 保留论文决定性的门控、权重、状态转换或调度规则，并把中间量写入指标产物；具体公式与变量对应见实现函数及测试中的不变量断言。

### 论文离线与线上效果

论文报告的线上、benchmark、训练效率或推理速度只作为原文结果。本地三种子 artifact 只验证核心机制、形状和状态不变量，不与论文数字直接横比。指标见 [`metrics/{metric_name}`](metrics/{metric_name})。{gpu}

## 复现边界

{BOUNDARY[record['key']]}
"""


def main():
    for record in (ANGLE_PAPER,) + LATEST_METHOD_PAPERS:
        result_rows = rows(record)
        detail = ROOT/"docs"/record["detail_path"]; detail.parent.mkdir(parents=True, exist_ok=True)
        name = "movielens-100k-seeds42-44.json" if record["domain"] == "recommendation" else "mechanism-seeds42-44.json"
        detail.write_text(render(record, name), encoding="utf-8")
        artifact = detail.parent/"metrics"/name; artifact.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema_version":2,"method":record["key"],"dataset":"MovieLens 100K" if record["domain"]=="recommendation" else "deterministic mechanism mini-suite","seeds":list(SEEDS),"runs":result_rows,"aggregate_metrics":aggregate(result_rows),"manifest_ref":f"{record['domain']}:{record['key']}","evaluation_protocol":{"tier":"l2_public_dataset" if record["domain"]=="recommendation" else "l1_mechanism","seeds":list(SEEDS),"formal_comparison":record["domain"]=="recommendation","diagnostic_only":record["domain"]!="recommendation","claim_policy":"paper-scale claims excluded"},"provenance":{"commit":"working tree before commit","command":"PYTHONPATH=src python scripts/generate_sep_19_2026_artifacts.py","artifact_path":artifact.relative_to(ROOT).as_posix(),"dataset_fingerprint":"sep19-public-fixture-v1"}}
        artifact.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


if __name__ == "__main__": main()
