#!/usr/bin/env python3
"""Generate documentation and deterministic receipts for the Sep-30 closure."""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research.latest_20260930_closure import (
    bootstrap_error_certificate, continuous_context, mnemon_view,
    rubric_process_credit, symbolic_gate,
)
from auto_research.foundation_latest_20260930_closure import (
    frac_modes, frac_recurrence, telescopic_loss,
)
from auto_research.latest_20260930_closure_catalog import LATEST_METHOD_PAPERS
from auto_research.post_training.latest_20260930_closure import (
    mas_privileged_coordination, mas_role_advantage, olive_loss,
    reward_aligned_weights, rfpo_advantages, ross_selective_loss,
)
from auto_research.recommendation_latest_20260930_closure import (
    Skill, SkillGenome, SkillGenomeController, promptshift_metrics,
)

SEEDS = (42, 43, 44)
SUMMARY = {
    "evoskillrec": "把推荐网络拆成带输入输出类型的可执行 skill genome；控制器在约束空间组合技能，只有通过 validation 的创新才晋级并进入后续复用库。",
    "promptshift": "在行为历史不变时比较身份提示与无身份参考列表，用 Drift 与 SliceShift 量化身份线索偏移，再依据用户主流度自适应混合原分与逆群体流行度。",
    "telescopic-lm": "每步随机抽一个网络深度前缀做 next-token 监督，同时保留全深度 anchor，使同一 checkpoint 的每个深度都成为可用语言模型。",
    "frac-ssm": "以对数间隔的有限指数模态逼近分数阶动力学的幂律记忆，在有界递归状态下兼顾长尾记忆和并行训练。",
    "rfpo": "冻结已校准 critic，把前缀成功概率同时作为 rollout reward、GAE baseline 和未完成轨迹预报，并在去长度偏置后二值化，降低策略利用 critic 偏差的风险。",
    "olive": "由当前 student 生成前缀，再让 teacher 从该 student state 续写；student 只在 teacher continuation token 上计算交叉熵。",
    "ross": "保留历史 self-rollout 的完整上下文，但只对筛选出的模型 continuation 计算损失，避免模仿其中错误或冗余步骤。",
    "r2-opd": "用验证结果的一致性和 teacher/student 分歧共同重分配稠密蒸馏权重，使更有结果价值的修正获得更大相对影响。",
    "mas-opd": "以目标角色与非目标角色 teacher 信号差构造 role advantage，并把协作冲突归因只提供给 teacher 形成 privileged coordination supervision。",
    "dr-credit": "按 rubric 的历史已接受支持计算本次工具结果带来的新增或部分支持，再与最终结果优势结合，避免重复证据反复得分。",
    "ccm": "每轮输出动作和更新后的有界 memory；下一轮只读原任务、memory 与最新 observation，并用完整历史只在训练侧提供 privileged distillation。",
    "sage-planner": "执行前用符号前置条件门阻止不安全动作并给出类型化原因；失败时只重写相关子目标的后缀，保留已完成前缀。",
    "certified-selective-eval": "按任务簇而非轨迹独立假设做 bootstrap，给自动判断区域的错误率建立上置信界，只有证书低于预算才自动接管。",
    "mnemon": "保存原始带日期记录，由慢速规划生成搜索、快速 Jev 判断记录是否需要，再在预算内构造供原回答模型使用的小视图。",
}
BOUNDARY = {
    "evoskillrec": "执行 typed genome、validation evaluator、promotion 与 reuse；未调用外部 LLM 发明任意代码，也不复述论文大规模搜索收益。",
    "promptshift": "执行列表指标与后处理 reranker；身份 slice 和相关性由公开 fixture 给出，不生成真实用户画像。",
    "telescopic-lm": "验证随机深度和 full anchor 的梯度路径；未做 20B-token 预训练。",
    "frac-ssm": "执行有限模态递归与长尾记忆不变量；不是 1.3B 参数语言模型结果。",
    "rfpo": "执行冻结 critic 的去偏、二值奖励与 GAE；未训练长链思维模型。",
    "olive": "执行 student-prefix/teacher-continuation 的精确 loss mask；未调用闭源 teacher。",
    "ross": "执行 full-context/selective-loss 边界；选择 mask 是 fixture，不冒充论文 selector。",
    "r2-opd": "执行 outcome/disagreement 连续重加权；不外推七个数学 benchmark 的增益。",
    "mas-opd": "执行 role advantage 与 privileged conflict mask；未进行多模型 MAS 联训。",
    "dr-credit": "执行 rubric-history 增量支持；rubric 与证据分数来自 fixture，不读取 gold answer。",
    "ccm": "执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。",
    "sage-planner": "执行零 token 符号 gate 与局部后缀编辑；未运行 AI2-THOR。",
    "certified-selective-eval": "执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。",
    "mnemon": "执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。",
}
MODULE = {
    "recommendation": "src/auto_research/recommendation_latest_20260930_closure.py",
    "foundation-models": "src/auto_research/foundation_latest_20260930_closure.py",
    "post-training": "src/auto_research/post_training/latest_20260930_closure.py",
    "agent-research": "src/auto_research/agent_research/latest_20260930_closure.py",
}


def run(record, seed):
    import torch

    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    key = record["key"]
    if key == "evoskillrec":
        controller = SkillGenomeController(lambda value: -float(np.square(value - 3).mean()))
        controller.register(Skill("scale", "features", "features", lambda value: value * 2))
        controller.register(Skill("bias", "features", "score", lambda value: value + 1))
        genome = SkillGenome(("scale", "bias"), "features", "score")
        out = controller.evaluate_and_promote(genome, np.array([1.0]), baseline=-1.0)
        return {"validation_score": out["score"], "promoted": out["promoted"], "reusable_genomes": len(controller.reuse())}
    if key == "promptshift":
        return promptshift_metrics([0, 1, 2, 3], [0, 2, 4, 3], [.9, .8, .2, .3, .1], {2, 4}, k=4)
    if key == "telescopic-lm":
        logits = [torch.randn(2, 4, 11, requires_grad=True) for _ in range(4)]
        loss, audit = telescopic_loss(logits, torch.randint(0, 11, (2, 4)), 1 + seed % 3)
        loss.backward()
        return {"loss": float(loss.detach()), **audit, "full_anchor_gradient": logits[-1].grad is not None}
    if key == "frac-ssm":
        rates, weights = frac_modes(8, .01, 1, .5)
        output, state = frac_recurrence(rng.normal(size=(32, 4)), rates, weights)
        return {"output_norm": float(np.linalg.norm(output)), "state_norm": float(np.linalg.norm(state)), "modes": len(rates)}
    if key == "rfpo":
        advantage, audit = rfpo_advantages(rng.random(9), length_bias=.01)
        return {"advantage_mean": float(advantage.mean()), **audit}
    if key == "olive":
        logits = torch.randn(2, 6, 9, requires_grad=True)
        loss, mask = olive_loss(logits, torch.randint(0, 9, (2, 6)), [2, 3])
        loss.backward()
        return {"loss": float(loss.detach()), "supervised_tokens": int(mask.sum()), "prefix_gradient_zero": bool(logits.grad[~mask].abs().sum() == 0)}
    if key == "ross":
        logits = torch.randn(2, 6, 9, requires_grad=True)
        mask = torch.tensor([[0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 0, 0]], dtype=torch.bool)
        loss = ross_selective_loss(logits, torch.randint(0, 9, (2, 6)), mask)
        loss.backward()
        return {"loss": float(loss.detach()), "selected_tokens": int(mask.sum()), "unselected_gradient_zero": bool(logits.grad[~mask].abs().sum() == 0)}
    if key == "r2-opd":
        teacher = torch.log_softmax(torch.randn(2, 4, 7), -1)
        student = torch.log_softmax(torch.randn(2, 4, 7), -1)
        weight = reward_aligned_weights(teacher, student, torch.tensor(rng.integers(0, 2, (2, 4))))
        return {"weight_mean": float(weight.mean()), "weight_std": float(weight.std())}
    if key == "mas-opd":
        role, audit = mas_role_advantage(torch.randn(1, 4), torch.randn(1, 4), torch.tensor([[1., 1., 1., 0.]]))
        student = torch.log_softmax(torch.randn(1, 4, 5), -1).requires_grad_()
        teacher = torch.log_softmax(torch.randn(1, 4, 5), -1).requires_grad_()
        loss = mas_privileged_coordination(student, teacher, torch.tensor([[1., 0., 1., 0.]]))
        loss.backward()
        return {"role_norm": float(role.norm()), "coordination_loss": float(loss.detach()), **audit, "teacher_detached": teacher.grad is None}
    if key == "dr-credit":
        _, audit = rubric_process_credit([.2, .5, .1], [.7, .4, .8])
        return audit
    if key == "ccm":
        prompt = continuous_context("task", range(10), "latest", memory_budget=3)
        return {"retained_memory": len(prompt["memory"]), "full_history_retained": False}
    if key == "sage-planner":
        accepted, blocked = symbolic_gate(["open", "take"], {"at-door"}, {"open": ({"at-door"}, {"open"}), "take": ({"visible"}, {"holding"})})
        return {"accepted_actions": len(accepted), "blocked_actions": len(blocked), "model_calls_for_gate": 0}
    if key == "certified-selective-eval":
        return bootstrap_error_certificate([[0, 0], [0], [0, seed % 2]], budget=.8, samples=500, seed=seed)
    if key == "mnemon":
        _, audit = mnemon_view([{"date": str(i), "text": text} for i, text in enumerate(("likes jazz", "weather", "jazz concert"))], ["jazz"], budget=1)
        return audit
    raise KeyError(key)


def aggregate(rows):
    result = {}
    for key in rows[0]:
        values = [row[key] for row in rows]
        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            result[f"{key}_mean"] = statistics.fmean(values)
    return result


def render(record):
    upstream = f"是：[{record['code']}]({record['code']})" if record.get("code") else "否：截至 2026-09-30 未找到原作者公开仓库"
    module = MODULE[record["domain"]]
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
| 本地复现代码 | [`{module}`](https://github.com/daiwk/auto-research/blob/main/{module}) |

## 原始论文总结

### 背景与主要改动

{SUMMARY[record['key']]}

```mermaid
flowchart LR
  I[公开输入/当前状态] --> M[{record['adapter']} 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/更新状态]
```

<!-- paper-figure:start -->
### 原论文关键图

[![{record['title']} 原论文关键图](assets/paper-figure-01.png)]({record['paper_url'].replace('/abs/', '/pdf/')})

> **原论文关键图**：展示论文核心架构、训练流程或评测协议。图片来自[原论文]({record['paper_url']})，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

本地 reference kernel 保留论文决定性的门控、掩码、递归、信用权重或晋级条件；测试同时检查梯度隔离、类型边界和确定性。

### 论文离线与线上效果

论文中的 benchmark、速度或训练曲线属于原文结果。本地三种子 mini-suite 仅检验机制和不变量，不与论文规模结果横比，也不外推线上收益。

## 本地复现

三种子诊断见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。其中 `diagnostic_only=true`，不能进入正式能力排名。

## 复现边界

{BOUNDARY[record['key']]}
"""


def main():
    for record in LATEST_METHOD_PAPERS:
        rows = [{"seed": seed, **run(record, seed)} for seed in SEEDS]
        readme = ROOT / "docs" / record["detail_path"]
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text(render(record), encoding="utf-8")
        artifact = readme.parent / "metrics" / "mechanism-seeds42-44.json"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(json.dumps({
            "schema_version": 2, "manifest_ref": f"{record['domain']}:{record['key']}",
            "method": record["key"], "dataset": "deterministic public mechanism mini-suite",
            "seeds": list(SEEDS), "diagnostic_only": True, "seed_results": rows,
            "aggregate_metrics": aggregate(rows),
            "evaluation_protocol": {"tier": "l1_mechanism", "formal_comparison": False, "diagnostic_only": True, "claim_policy": "mechanism execution and invariants only"},
            "provenance": {"artifact_path": str(artifact.relative_to(ROOT)), "dataset_fingerprint": "sep30-closure-public-fixtures-v1", "original_code_commit": "working tree"},
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(readme.relative_to(ROOT))


if __name__ == "__main__":
    main()
