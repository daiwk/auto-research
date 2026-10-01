#!/usr/bin/env python3
"""Generate reviewed docs and deterministic L1 receipts for the Oct-1 batch."""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research.latest_20261001 import (
    MetaSkillBank, ProposedAction, apply_context_file, meta_reasoning_dispatch,
    route_branch, update_branch_subsets,
)
from auto_research.foundation_latest_20261001 import (
    ce_guided_router, pumba_window, splash_memory, splash_select_layout,
    tadm_fusion, vjepa_policy_losses,
)
from auto_research.latest_20261001_catalog import LATEST_METHOD_PAPERS
from auto_research.post_training.latest_20261001 import (
    advisd_contrast, advisd_gate, flowmap_separated_loss, gats_schedule,
    interpolated_policy, maestro_disagreement,
)
from auto_research.recommendation_latest_20261001 import (
    cohortmix_prior, cohortmix_slate, cohortmix_update, recap_recursive_routes,
)

SEEDS = (42, 43, 44)

SUMMARY = {
    "meta-reasoning": "把对象级工作交给 worker，把控制本身拆成 Assess、Propose、Evaluate 和 Dispatch；控制器只携带紧凑状态，通过持久 artifact memory 复用既有工作，并在统一调用预算内决定继续、分叉或停止。",
    "context-lm": "把上下文视为模型可直接编辑的文件，使保留、删除和重组信息成为模型行为，而不是外部 harness 的固定策略；多 Agent 各自维护 context file，服务端从第一个不匹配 token 起重新 prefill。",
    "meta-skills": "从开发任务的 harness 执行反馈中提炼包含 when、provide、use 的 meta-skill，再冻结技能库；测试任务只检索相关 meta-skill 来构建新 harness，不用测试结果反向修改技能库。",
    "branch-mixture": "将 harness 搜索拆成多条分支，每条分支维护不同的开发子集和 proposal policy；全分支都解决的样本被移除，具有分支区分度的样本被保留，部署时由只看输入特征的 router 选择开发集冠军。",
    "advisd": "冻结 executor，只训练 advisor；反思先提出修正，再对同一已记录 executor 响应分别计算有建议与无建议的平均 log-likelihood，只有影响幅度超过 donor-advice 校准阈值的决定才进入自蒸馏。",
    "gats": "用教师训练尾部成功率作为固定参考，以学生滞后一拍的移动平均估计能力差距；OPD 权重随差距线性下降，学生达到教师参考后永久关闭教师分支，继续只做 GRPO。",
    "cohortmix-ts": "从历史 cohort 学习用户群和 item arm，用元数据给新用户构造固定强度的混合 Beta 先验；每轮用 Thompson sampling 选择未曝光 slate，并按用户反馈独立更新后验。",
    "recap-ctr": "不再只增加单个 CTR predictor 的交互容量，而是扩展相关 estimator；RECAP 在共享参数的递归 backbone 上形成多条 route，并结合独立模型蒸馏、训练轨迹 EMA 与推理 route 平均。",
    "maestro-opd": "MAESTRO 用教师 top-k 覆盖度和 Bhattacharyya 相似度构造逐 token Policy Disagreement Score，并对靠近响应起点的位置加权；教师只在高分歧位置介入，减少整段 teacher rollout 的固定开销。",
    "ipd": "在每个 token 状态把 student 与 teacher 分布按 $m_\\gamma=(1-\\gamma)\\pi_S+\\gamma\\pi_T$ 插值，从纯 on-policy 连续过渡到 off-policy teacher；论文再用验证感知的 speculative sampler 精确采样该目标策略。",
    "flowmap-opd": "把生成状态的 rollout 分布与 teacher/student 比较 kernel 解耦：rollout 只负责提供具有正确边缘分布的状态，优化 kernel 在这些冻结状态上比较 flow map、诱导速度或瞬时速度。",
    "vjepa-policy": "冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。",
    "ce-guided-moe": "在原生 MoE affinity 旁增加逐 expert token-error head，并用预测误差的 started-log 对路由 logit 做衰减；高预测错误的 expert 在 Top-K 前被降权，同时误差头由真实 next-token CE 监督。",
    "tadm": "将昂贵 anchor network 的潜表示跨多个反向扩散步缓存，只周期性刷新；小型 fusion module 根据当前状态门控修正陈旧 anchor，再交给轻量 denoiser。",
    "pumba": "训练时沿模型自己的 progressive-unmasking 轨迹连续展开多个 denoising step，把隐藏 carry 传给下一步，并在固定窗口内通过时间反向传播，使前一步学会产生对后续有用的 carry。",
    "splash": "统一描述 attention weight 与 KV cache 的所有权，引入权重分片、请求独占 KV 的 DOP；调度器把布局切换成本按剩余步数摊销，在 TP、DP、CP、DOP 间在线切换。",
}

FORMULA = {
    "meta-reasoning": "$s_t=Assess(x,s_{t-1},\\Delta M_t;M_t)$，$\\tilde a_t=Evaluate(x,s_t,b_t,\\mathcal A_t;M_t)$，随后 $a_t=Dispatch(\\cdot)$。本地实现对可行 action 按预期价值/调用成本选择，并把完整 artifact 留在持久 memory。",
    "context-lm": "$c_{t+1}=f_\\theta^{CLM}(c_t)$。本地实现 replace/append 文件变换、显式容量边界和从首个 prefix mismatch 起算的 suffix cache reuse。",
    "meta-skills": "$s=(when,provide,use)$，开发期循环为 $S_{j+1}=Revise(S_j,\\{(H_x^j,F(e_x^j))\\})$。本地技能库只接受开发反馈，测试选择不写回。",
    "branch-mixture": "$J_b^t(H)=|X_b^t|^{-1}\\sum_x\\mathbb E[r(f_M(H,x),x)]$。本地实现有区分度开发子集更新和不读取测试标签的线性 router。",
    "advisd": "$c_k=T_k^{-1}\\sum_t[\\log\\pi(y_{k,t}|C_k^+)-\\log\\pi(y_{k,t}|C_k^-)]$；阈值是 donor contrast 绝对值的经验分位数。",
    "gats": "$\\lambda_t=\\max(1-M_{S,t}/M_T,0)$，$L_{GATS}=L_{GRPO}+(1-d_t)\\lambda_tL_{OPD}$；$M_{S,t}\\ge M_T$ 后 $d_t$ 永久置一。",
    "cohortmix-ts": "$\\hat\\mu_{c,a}=(\\alpha_0+s_{c,a})/(\\alpha_0+\\beta_0+s_{c,a}+f_{c,a})$，新用户先验为群组 membership 加权的固定强度 Beta pseudo-count。",
    "recap-ctr": "$\\bar Z_M=M^{-1}\\sum_m Z_m$，共享 block 递归产生多 route logit 并做平均；本地同时保留训练轨迹 EMA。",
    "maestro-opd": "$PDS_t=1-C_tB_t$，其中 $C_t$ 是教师 top-k 在学生 top-k 中的概率覆盖，$B_t$ 是归一化 top-k 分布的 Bhattacharyya 系数。",
    "ipd": "$m_\\gamma(\\cdot|s)=(1-\\gamma)\\pi_S(\\cdot|s)+\\gamma\\pi_T(\\cdot|s)$；本地验证端点、归一化和总变差线性插值。",
    "flowmap-opd": "$L(\\theta)=\\mathbb E_{z\\sim\\rho^\\theta}[\\ell(\\theta,T;z)]$。本地从计算图中 detach rollout state，仅让 local KL kernel 更新 student。",
    "vjepa-policy": "$L_{predict}=|M|^{-1}\\sum_{i\\in M}\\|P(E(x),q)_i-sg(E(y)_i)\\|_1$，并联合 flow-matching action velocity loss。",
    "ce-guided-moe": "$\\tilde a_{t,i}=a_{t,i}-\\gamma\\log(1+\\hat e_{t,i}/\\tau)$，再对 $\\tilde a$ 做 softmax 与 Top-K。",
    "tadm": "$\\tilde h_{t|t'}=h_{t'}+g_\\phi(c_t,h_{t'})\\odot\\Delta_\\phi(c_t,h_{t'})$。本地实现门控 cache correction。",
    "pumba": "$L_W=W^{-1}\\sum_{j=1}^W CE(f_\\theta(x_{t_j},h_{j-1}),x_0)$，梯度在窗口内穿过 carry，窗口间截断。",
    "splash": "$M_{TP}=W_A/T+Bks$，$M_{DOP}=W_A/T+Bks/T$，$M_{DP}=M_{CP}=W_A+Bks/T$；调度目标额外摊销 switch cost。",
}

RESULTS = {
    "meta-reasoning": "ProgramBench 上 GPT-5.5 达 71.5%，Codex 为 58.0%；Opus 4.8 达 67.2%，Claude Code 为 65.5%。其他长程任务相对 direct control 平均提高 3.6–4.2 分。",
    "context-lm": "BrowseComp-Plus 准确率提高 11.4%、FLOPs 减少 21.5%；EdgeBench 分数提高 5%、FLOPs 减少 59%；在线 RL 使 Qwen3.5-9B 提高 47.6% 且 FLOPs 减少 12%。",
    "meta-skills": "相对 no-skill 基线提高 8.95 个百分点，相对直接复用固定 skill bank 提高 12.02 个百分点；详情页不把该结果外推到本地 fixture。",
    "branch-mixture": "相对 Meta-Harness，在奥数推理、Terminal-Bench 2.0、SWE-bench Lite 上分别相对提高 34.8%、11.6%、3.8%。",
    "advisd": "相对 advisor-GRPO，BFCL-v3 提高 4.2–6.4 个百分点，EnvScaler 提高 3.9–5.1 分。",
    "gats": "三组 Qwen2.5 teacher/student 配置均优于 matched-budget GRPO，平均成功率提高 4.37–11.87 个百分点。",
    "cohortmix-ts": "25 天随机部署中，受限完整窗口子组的 early-to-late correctness change 组间差为 6.23 个百分点，95% bootstrap 区间 [0.5,11.9]，p=0.043；全体注册用户参与指标无显著差异。",
    "recap-ctr": "原文在多个公开 CTR benchmark 上改善性能—参数 Pareto，但没有量化线上 A/B；因此本条只作为学术机制和 Evolve 算子。",
    "maestro-opd": "Qwen3 0.6B/1.7B 在八个数学 benchmark 的 macro average 最佳，并相对标准 OPD 缩短约 67.3% 响应长度。",
    "ipd": "原文在文本与多模态任务上比较 SFT、OPD、SFT→OPD 与不同插值系数；本地不复述论文规模提升为自己的结果。",
    "flowmap-opd": "原文在 ImageNet 和多 specialist teacher consolidation 上验证 few-step student；本地只验证 rollout/kernel 梯度隔离。",
    "vjepa-policy": "0.9B 总参数（0.6B 可训练）在 LIBERO、LIBERO-Plus、RoboCasa-GR1 与代表性 WAM/VLA 竞争；本地不运行机器人 checkpoint。",
    "ce-guided-moe": "Granite MoE 实验报告平均约 2.3 个百分点提升；本地只验证误差感知 affinity 衰减。",
    "tadm": "DiffusionGemma-26B 后训练版吞吐提高约 49%–79%；预训练版最多减少 38% Transformer 层计算，并比 ADLM 测得吞吐最高提高 73%。",
    "pumba": "LLaDA-8B 在保持质量时减少约 22%–26% function evaluations；本地只验证窗口内 BPTT。",
    "splash": "B200/GLM-5.3 上端到端吞吐为固定布局的 1.3–1.73 倍，切换中位开销低于所在 step 的 0.51%；A100/A30 不冒充论文硬件结果。",
}

BOUNDARY = {
    "meta-reasoning": "执行预算可行性、Evaluate/Dispatch 选择和持久 artifact/紧凑 state 分离；不调用前沿 worker，不复述 ProgramBench 为本地成绩。",
    "context-lm": "执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。",
    "meta-skills": "执行开发反馈 refine 与冻结后检索；fixture reward 不是 AI4AI benchmark。",
    "branch-mixture": "执行分支子集分化和输入路由；没有 LLM 生成 harness，也不运行 SWE-bench。",
    "advisd": "执行 paired contrast、donor calibration 和选择 gate；不调用 Gemini/Claude executor，未复现 BFCL-v3。",
    "gats": "执行滞后一拍移动平均、gap weight 和永久 withdrawal；未做 Qwen Agent RL。",
    "cohortmix-ts": "执行固定强度 mixture prior、Thompson slate 与 posterior update；未复刻历史矩阵分解和 25 天部署。",
    "recap-ctr": "执行共享递归、route 平均、trajectory EMA 和可运行 RankMixer Evolve block；未做 benchmark 训练或独立模型蒸馏。",
    "maestro-opd": "执行 top-k coverage/Bhattacharyya PDS；未生成 teacher rollouts。",
    "ipd": "执行精确 token mixture；高吞吐 speculative sampler 和模型训练未复现。",
    "flowmap-opd": "执行 rollout state detach 与 local kernel KL；未训练图像 flow-map generator。",
    "vjepa-policy": "执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。",
    "ce-guided-moe": "执行 error-aware routing 公式；未训练 Granite MoE。",
    "tadm": "执行 stale-anchor 门控修正；未加载 DiffusionGemma-26B。",
    "pumba": "执行连续 denoising carry 与窗口内 BPTT；未训练 LLaDA-8B。",
    "splash": "执行内存模型和 transition-aware layout planner；未实现 CUDA handoff，也不声称经过 B200/H200 性能验证。",
}

MODULE = {
    "meta-reasoning": "src/auto_research/agent_research/latest_20261001.py",
    "context-lm": "src/auto_research/agent_research/latest_20261001.py",
    "meta-skills": "src/auto_research/agent_research/latest_20261001.py",
    "branch-mixture": "src/auto_research/agent_research/latest_20261001.py",
    "advisd": "src/auto_research/post_training/latest_20261001.py",
    "gats": "src/auto_research/post_training/latest_20261001.py",
    "maestro-opd": "src/auto_research/post_training/latest_20261001.py",
    "ipd": "src/auto_research/post_training/latest_20261001.py",
    "flowmap-opd": "src/auto_research/post_training/latest_20261001.py",
    "vjepa-policy": "src/auto_research/foundation_latest_20261001.py",
    "ce-guided-moe": "src/auto_research/foundation_latest_20261001.py",
    "tadm": "src/auto_research/foundation_latest_20261001.py",
    "pumba": "src/auto_research/foundation_latest_20261001.py",
    "splash": "src/auto_research/foundation_latest_20261001.py",
    "cohortmix-ts": "src/auto_research/reproductions/cohortmix_ts/",
    "recap-ctr": "src/auto_research/reproductions/recap_ctr/",
}


def run(record, seed):
    import torch

    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    key = record["key"]
    if key == "meta-reasoning":
        _, audit = meta_reasoning_dispatch([ProposedAction("reuse", 8, 2, ("a",)), ProposedAction("fresh", 9, 5)], remaining_budget=8)
        return audit
    if key == "context-lm":
        value = apply_context_file("goal:old", [{"operation": "replace", "old": "old", "new": "new"}, {"operation": "append", "text": "\nfact"}], maximum_characters=32)
        return {"context_characters": len(value), "contains_old_goal": "old" in value}
    if key == "meta-skills":
        bank = MetaSkillBank(); bank.revise([{"skill": "verify", "reward": 1, "when": ["code"], "provide": ["tests"], "use": ["submit"]}])
        return {"selected_skills": len(bank.select(["code"], limit=2)), "bank_size": len(bank.skills)}
    if key == "branch-mixture":
        subsets = update_branch_subsets({"a": {"x": 1, "common": 1}, "b": {"y": 1, "common": 1}})
        selected, scores = route_branch({"math": 1}, {"a": {"math": 2}, "b": {"code": 3}})
        return {"retained_cases": sum(map(len, subsets.values())), "selected_branch_a": selected == "a", "score_margin": scores["a"] - scores["b"]}
    if key == "advisd":
        contrast = advisd_contrast(torch.randn(6, 5), torch.randn(6, 5))
        selected, threshold = advisd_gate(contrast, torch.randn(20) * .2, torch.tensor([0, 0, 1, 0, 0, 0]), quantile=.8)
        return {"selected_decisions": int(selected.sum()), "threshold": float(threshold), "mean_abs_contrast": float(contrast.abs().mean())}
    if key == "gats":
        weight, withdrawn, audit = gats_schedule([.7, .8, .9], [.2, .3 + seed / 1000], window=2)
        return {"opd_weight": weight, "withdrawn": withdrawn, **audit}
    if key == "cohortmix-ts":
        alpha, beta = cohortmix_prior([.75, .25], [[8, 2, 5], [1, 7, 2]], [[2, 8, 5], [9, 3, 8]], alpha0=1, beta0=1, strength=10)
        chosen, draws = cohortmix_slate(alpha, beta, size=2, seed=seed)
        ua, ub = cohortmix_update(alpha, beta, chosen, [1, 0])
        return {"prior_mean": float((alpha / (alpha + beta)).mean()), "maximum_draw": float(draws.max()), "posterior_mass": float((ua + ub).sum())}
    if key == "recap-ctr":
        block = torch.nn.Sequential(torch.nn.Linear(6, 6), torch.nn.Tanh())
        avg, audit = recap_recursive_routes(torch.randn(12, 6), block, routes=3, ema_decay=.9)
        return {
            "averaged_variance": float(avg.var().detach()),
            "route_diversity": float(audit["routes"].var(0).mean().detach()),
            "ema_norm": float(audit["trajectory_ema"].norm().detach()),
        }
    if key == "maestro-opd":
        teacher = torch.softmax(torch.randn(2, 5, 9), -1); student = torch.softmax(torch.randn(2, 5, 9), -1)
        token, prefix = maestro_disagreement(teacher, student, top_k=3)
        return {"token_pds_mean": float(token.mean()), "prefix_pds_mean": float(prefix.mean())}
    if key == "ipd":
        student = torch.softmax(torch.randn(4, 9), -1); teacher = torch.softmax(torch.randn(4, 9), -1)
        mixed = interpolated_policy(student, teacher, .35)
        return {"normalization_error": float((mixed.sum(-1) - 1).abs().max()), "teacher_weight": .35}
    if key == "flowmap-opd":
        student = torch.nn.Linear(5, 4); teacher = torch.nn.Linear(5, 4)
        loss, states = flowmap_separated_loss(torch.randn(8, 5, requires_grad=True), student, teacher)
        loss.backward()
        return {"kernel_kl": float(loss.detach()), "rollout_state_detached": not states.requires_grad, "student_gradient_norm": float(student.weight.grad.norm())}
    if key == "vjepa-policy":
        class Velocity(torch.nn.Module):
            def __init__(self): super().__init__(); self.proj = torch.nn.Linear(7, 4)
            def forward(self, action, latent): return self.proj(torch.cat((action, latent), -1))
        loss, audit = vjepa_policy_losses(torch.randn(2, 3), torch.randn(2, 3), Velocity(), torch.randn(2, 4), torch.randn(2, 4), torch.tensor([.2, .8]))
        return {"joint_loss": float(loss.detach()), **audit}
    if key == "ce-guided-moe":
        native = torch.randn(4, 6); error = torch.rand(4, 6) * 3
        prob, adjusted = ce_guided_router(native, error)
        return {"probability_error": float((prob.sum(-1) - 1).abs().max()), "mean_attenuation": float((native - adjusted).mean())}
    if key == "tadm":
        stale = torch.randn(4, 5); current = torch.randn(4, 5)
        fused, gate = tadm_fusion(stale, current, lambda c, h: c - h, lambda c, h: c - h)
        return {"fused_norm": float(fused.norm()), "mean_gate": float(gate.mean())}
    if key == "pumba":
        initial = torch.randn(2, 3, 7, requires_grad=True); target = torch.randint(0, 7, (2, 3))
        def step(logits, carry, _):
            carry = logits if carry is None else .5 * carry + logits
            return carry, carry
        loss, carry, losses = pumba_window(step, initial, target, window=3); loss.backward()
        return {"window_loss": float(loss.detach()), "steps": len(losses), "initial_gradient_norm": float(initial.grad.norm()), "boundary_carry_detached": not carry.requires_grad}
    if key == "splash":
        memory = {layout: splash_memory(layout, attention_weights=120, batch=8, kv_heads=2, sequence=16, tensor_parallel=4) for layout in ("tp", "dop", "dp", "cp")}
        layout, effective = splash_select_layout({"tp": 1.0, "dop": .8}, "tp", {("tp", "dop"): 4.0}, remaining_steps=50)
        return {"dop_memory": memory["dop"], "tp_memory": memory["tp"], "selected_dop": layout == "dop", "dop_effective_cost": effective["dop"]}
    raise KeyError(key)


def aggregate(rows):
    result = {}
    for key in rows[0]:
        values = [row[key] for row in rows]
        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            result[f"{key}_mean"] = statistics.fmean(values)
    return result


def render(record):
    upstream = f"是：[{record['code']}]({record['code']})" if record.get("code") else "否：截至 2026-10-01 未找到原作者公开仓库"
    local = MODULE[record["key"]]
    local_url = "tree" if local.endswith("/") else "blob"
    return f"""# {record['title']}

> **复现级别：L1 核心机制诊断。** {BOUNDARY[record['key']]}

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv {record['paper_url'].rsplit('/', 1)[-1]}]({record['paper_url']}) |
| 公司/机构 | {record['first_author_affiliation']}（按第一作者署名单位） |
| 首次公开日期 | {record['published']}（arXiv v1） |
| 原文开源代码 | {upstream} |
| Adapter | `{record['adapter']}` |
| 本地复现代码 | [`{local}`](https://github.com/daiwk/auto-research/{local_url}/main/{local}) |

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

> **原论文关键图**：展示论文核心架构、训练流程或系统协议。图片来自[原论文]({record['paper_url']})，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

{FORMULA[record['key']]}

### 论文离线与线上效果

{RESULTS[record['key']]}

## 本地复现

> **本地对照口径**：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。

三种子诊断见 [`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)。`diagnostic_only=true`，只证明核心状态转换、梯度或调度不变量可执行，不能进入正式能力排名。

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
            "schema_version": 2,
            "manifest_ref": f"{record['domain']}:{record['key']}",
            "method": record["key"],
            "dataset": "deterministic public mechanism mini-suite",
            "seeds": list(SEEDS),
            "diagnostic_only": True,
            "seed_results": rows,
            "aggregate_metrics": aggregate(rows),
            "evaluation_protocol": {
                "tier": "l1_mechanism", "formal_comparison": False,
                "diagnostic_only": True,
                "seeds": list(SEEDS),
                "claim_policy": "mechanism execution and invariants only",
            },
            "provenance": {
                "artifact_path": str(artifact.relative_to(ROOT)),
                "dataset_fingerprint": "oct01-public-mechanism-fixtures-v1",
                "original_code_commit": "working tree",
            },
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(readme.relative_to(ROOT))


if __name__ == "__main__":
    main()
