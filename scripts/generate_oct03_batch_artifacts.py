#!/usr/bin/env python3
"""Generate documentation and deterministic L1 receipts for the Oct-3 batch."""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research.latest_20261003 import (  # noqa: E402
    MemFitStore, autocorrect_compaction, jev_spawn, pace_authorize,
    rule_evolve_select, update_belief_state,
)
from auto_research.foundation_latest_20261003 import (  # noqa: E402
    af_muon_vocab_direction, dense_caption_distillation, hawk_draft_target,
    ireko_nested_subnetwork, llm2jev_distribution, mwop_masks,
    rea_select_context,
)
from auto_research.latest_20261003_catalog import LATEST_METHOD_PAPERS  # noqa: E402
from auto_research.post_training.latest_20261003 import (  # noqa: E402
    carm_response_mask, drift_opd_loss, gradient_aligned_rejected_weights,
    group_mass_cap, lego_opd_teacher, sharpening_tax,
    sharpo_segment_advantages, token_level_video_credit,
)
from auto_research.recommendation_latest_20261003 import (  # noqa: E402
    agent_web_evidence, rptune_curate,
)

SEEDS = (42, 43, 44)

DETAILS = {
    "rptune": ("用查询-商品编码器、可学习调整项和下游 LLM 反馈共同决定商品保留与摆放顺序；高优商品靠近提示词末端，再对编排后的目录做选择后训练。", "$s_i=10e_q^Te_i+MLP([e_q;e_i])$，保留 top-k 后按分数升序排列。", "7 个真实商家上编排平均提高 14.0 EM 点，后训练再提高 10.3 点。", "只执行 rank/prune/position 核心编排，不调用 Gemini/Gemma、商家目录或论文训练。"),
    "agent-web-rec": ("先从平台获取候选语义，再按语义相关性和时间衰减检索目标用户私有记忆；仅在本地证据置信度不足时查询邻居 Agent 的紧凑偏好模式。", "$w=\beta w_{sem}+(1-\beta)e^{-\gamma\Delta t}$；$\kappa<\theta$ 时才协作。", "四个 InstructRec 域上均优于所比较基线。", "只执行有界检索与置信门控；不暴露私有记录，不运行 LLM Agent Web。"),
    "llm2jev": ("直接从括号数字选项的 next-token 概率形成有限类别分布；微调时使用 listwise 决策损失，并以 KL 锚定基础模型辅助输出。", "$p(o)\propto\exp\sum_t\log p([o]_t)$，$L=L_{list}+\lambda KL(p_{base}\|p_{aux})$。", "Qwen3.5-4B 无训练即可匹配同骨干社区 Jev 模型，微调收益主要集中在弱项。", "执行候选联合打分和 KL 锚定；未加载 4B checkpoint 或跑 JevBench。"),
    "omni-embed-mini": ("冻结文本骨干，把每个媒体样本的稠密级联描述经同一文本骨干得到 teacher target，再训练轻量投影器和分阶段 LoRA 对齐六种模态。", "$L_{distill}=1-\cos(z_{media},stopgrad(z_{caption}))$。", "0.9B 模型覆盖文本、语音、音频、图像、视频和富文档且保持文本检索能力。", "执行同几何空间的稠密描述蒸馏；未训练模态编码器或复现实测榜单。"),
    "mwop": ("在同一注意力头内分别剪 V2V/T2V/T2T 路径，并为视觉、文本执行选择不同 FFN 通道；注意力剪枝后重新估计 FFN 重要性。", "$I(w)\approx|w\partial L/\partial w|$，不同模态路径独立 top-k。", "论文在多种 MLLM 上报告较高压缩率下的精度保持与吞吐收益。", "执行独立路径/通道 mask；不声称 kernel 加速或模型级精度。"),
    "af-muon": ("矩阵继续用 Muon 谱范数方向，稀疏输入查表与稠密输出分类器共享的词表采用 support-aware 有限帽 LMO，一维参数用 RMS 更新。", "$d_i=1[g_i\\ne0]\\,g_i/\\|g_i\\|\\min(\\|g_i\\|,c)$。", "省去 AdamW 二阶状态，同时保持 tied-embedding 模型训练稳定性。", "执行词表 support/cap 方向；未完成论文规模预训练。"),
    "rea": ("把全局指令放入持久前缀，把多轮交互放入 episodic memory；检索时按角色决定保留原文、压缩表示或省略。", "$C=I_{persistent}\oplus TopK(E, relevance)$。", "Long-MT-Bench+ judge 6.32→7.36，平均延迟降低 2.91×。", "执行角色分离与 episodic top-k；不调用压缩 LLM。"),
    "hawk": ("从 target 多层隐藏状态学习混合，给浅层 drafter 提供压缩视觉表示，并用 drafter 自己提议后的 shifted trajectory 训练。", "$h_d=\sum_l softmax(a)_l h_l$，监督来自 shift 后 target 分布。", "论文报告 LVLM 投机解码接受率和无损速度提升。", "执行层混合与 shifted target 隔离；未实现专用解码 kernel。"),
    "irekogpt": ("保留 SliceGPT 投影矩阵而非直接丢弃，使同一 checkpoint 暴露嵌套宽度；再以多压缩率校准和 ridge 修正下游线性层。", "$W_k=P_{:k}^TWP_{:k}$，不同 k 共享同一嵌套基。", "Llama/Qwen 初步实验在高压缩率下优于朴素 PCA slimming。", "执行嵌套子网合同；未加载原模型或复现吞吐。"),
    "sharpening-tax": ("比较 base 与后训练策略在固定采样预算下的任务覆盖；再用 posterior-tempered group sampling 按估计难度调温，兼顾 pass@1 与覆盖率。", "$Tax_K=Coverage_K(base)-Coverage_K(post)$。", "14 对 checkpoint、3 个 Agent benchmark 中税普遍存在；PTGS 同时改善单次准确率和覆盖。", "执行固定预算覆盖差指标；不运行 Meta 模型或 Agent 环境。"),
    "carm": ("对每个 token 的 current/rollout log-ratio 先取绝对值再平均，避免正负漂移在序列级几何均值中抵消。", "$s=\exp(T^{-1}\sum_t|\log r_t|)$，$s\le\tau$ 才保留响应。", "AIME/BeyondAIME mean@16 最高 +3.13 点，四个代码榜 pass@1 +2.88 点。", "执行 detached response gate；未训练 Qwen3.5。"),
    "gmc-grpo": ("异步 rollout 的重要性比在 group 级统一缩放，使总质量受帽约束；在共同二阶矩保证下减少 trajectory-wise clipping 的持续偏差。", "$w_i=r_i\min(1,C/\sum_jr_j)$。", "大延迟设置下在 Qwen3 推理实验中优于稳定基线。", "执行 group mass capping；未搭建异步 RL 集群。"),
    "gaw-po": ("用拒绝 token 梯度与 preferred update direction 的对齐度调节负权重；越支持优选行为的 token 越少受罚。", "$w_t=1-[cos(g_t,g_+)]_+$。", "11 个数学、推理、代码和 QA benchmark 平均优于 DPO 0.97 点。", "执行梯度对齐权重；未进行 LoRA/DPO 训练。"),
    "sharpo": ("用同组成功轨迹作为自蒸馏 teacher context，在环境交互 segment 内计算 teacher-student log-prob gap，并有界缩放 GRPO advantage。", "$A_{seg}=A\cdot2\sigma(\overline{\log p_T-\log p_S})$。", "Qwen2.5-7B-Instruct 在 ALFWorld/WebShop 优于 GRPO、SDAR、RLSD、StepOPSD。", "执行 segment credit；未读取 gold plan，也未训练 7B Agent。"),
    "tvrl": ("冻结 VLM 的视频输入梯度定位对 reward 最敏感的生成 token，再把同组 advantage 稠密重分配到 token。", "$c_t=\|\partial R/\partial z_t\|/mean_t\|\partial R/\partial z_t\|$。", "论文在视频生成评测上报告比标量 GRPO 更好的提示遵循和时序质量。", "执行梯度 credit 归一化；未训练视频扩散模型。"),
    "lego-opd": ("把语言专家作为 token prior，把 grounding 专家只作为视觉 likelihood，以乘积专家形式组成 OPD teacher，避免连同 VLM 语言偏差一起蒸馏。", "$p_T(y|x,v)\propto p_L(y|x)p_G(y|x,v)^\alpha$。", "多模态 benchmark 上改善 grounding，同时较直接 VLM teacher 更好保留语言推理。", "执行 factorized teacher composition；未加载 LLM/VLM teacher。"),
    "drift-opd": ("把序列级 reverse-KL 拆成当前 chunk 的一步 reverse-KL 与刻画长期动作后果的 future potential；critic 从离线 demonstrations 学习。", "$L=KL(\pi_S\|\pi_T)-\lambda E[V_{future}]$。", "论文在连续 VLA 策略上报告无需在线 rollout 的长程任务改进。", "执行 objective 分解和 teacher stop-gradient；未运行机器人环境。"),
    "autocompact": ("judge 同时审查何时压缩、工作摘要写什么、压缩后下一步怎么做；纠错后的输出直接进入环境，随后以 SFT+结果 RL 联合学习。", "$(d,s,a)\leftarrow JudgeCorrect(d,s,a)$ 后再执行。", "SWE-bench Verified +9.2 点，SWE-PolyBench Verified +5.0 点。", "执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。"),
    "belief-state-pos": ("把当前世界事实与尚未解决的任务要求显式维护为 belief；若连续动作没有减少 unresolved requirements，则识别 Belief Trapping 并触发针对性恢复。", "$b_t=(facts_t, unresolved_t)$，$\Delta|unresolved|\ge0$ 标记停滞。", "四个执行/诊断 benchmark 上改善长程 Agent 成功率。", "执行 belief 更新与停滞检测；未调用外部工具环境。"),
    "pace-capability": ("在每次工具副作用发生前，根据认证请求编译出的 authority 与输入 provenance 同时检查 effect；入库时安全不代表执行时可信。", "$allow=effects(call)\subseteq authority\land trusted(provenance)$。", "论文给出认证执行合同和多类注入攻击评测。", "执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。"),
    "rule-evolve": ("维护 coding rule 候选池，由 mutator 生成变体，再只用隔离 validation evaluator 选择并回写更优规则。", "$r^*=argmax_{r\in pool\cup mutate(pool)}Score_{val}(r)$。", "跨两套 Coding Agent、四个模型和三个 benchmark 优于手工规则与 prompt 优化基线。", "执行候选变异后的 validation 选择；不调用 LLM mutator。"),
    "jev-spawn": ("先从自然语言任务构造有限 compositional action space，以 Jev 分布并行保留多个分支；反馈更新后验并保留备选以支持恢复。", "$p'(a)\propto p(a)e^{feedback(a)}$。", "八个任务、七个 Agent baseline 上评估速度、成本与成功率。", "执行有限动作 posterior 和 top-branch retention；不调用 Jev checkpoint。"),
    "memfit": ("原始 turn 追加写入不改写，只用 segment summary 建索引；读取融合 lexical、semantic 与 rerank 信号，避免昂贵 LLM 写入。", "$score=lexical+semantic$，write 为 append-only。", "论文报告相对 LLM memory 管线更低写入延迟和成本，并保持长期问答质量。", "执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。"),
}


def module_for(record):
    if record["domain"] == "recommendation":
        return "src/auto_research/recommendation_latest_20261003.py"
    if record["domain"] == "foundation-models":
        return "src/auto_research/foundation_latest_20261003.py"
    if record["domain"] == "post-training":
        return "src/auto_research/post_training/latest_20261003.py"
    return "src/auto_research/agent_research/latest_20261003.py"


def run(record, seed):
    torch.manual_seed(seed)
    key = record["key"]
    if key == "rptune":
        order, scores = rptune_curate(torch.randn(8), torch.randn(12, 8), torch.randn(12) * .1, prune_rate=.5); return {"retained": len(order), "best_last": int(order[-1]) == int(scores.argmax())}
    if key == "agent-web-rec":
        chosen, patterns, audit = agent_web_evidence(torch.rand(8), torch.arange(8.), semantic_weight=.7, memory_budget=3, confidence=.4, confidence_threshold=.7, collaborator_patterns=("a", "b")); return {"retrieved": len(chosen), "patterns": len(patterns), **audit}
    if key == "llm2jev":
        p = llm2jev_distribution(torch.randn(5, 2)); return {"probability_sum": float(p.sum()), "choices": len(p)}
    if key == "omni-embed-mini": return {"distillation_loss": float(dense_caption_distillation(torch.randn(4, 8), torch.randn(4, 8)))}
    if key == "mwop":
        masks = mwop_masks(torch.rand(4, 3), torch.rand(8), torch.rand(8), keep=3); return {"attention_kept": int(masks[0].sum()), "visual_kept": int(masks[1].sum()), "text_kept": int(masks[2].sum())}
    if key == "af-muon":
        d = af_muon_vocab_direction(torch.tensor([[3., 4.], [0., 0.], [6., 8.]]), cap=2); return {"active_rows": int((d.norm(dim=1)>0).sum()), "max_norm": float(d.norm(dim=1).max())}
    if key == "rea":
        ins, eps = rea_select_context(("policy",), ("old", "useful"), (.1, .9), episode_budget=1); return {"instructions": len(ins), "episodes": len(eps)}
    if key == "hawk":
        h, target = hawk_draft_target((torch.zeros(2,3), torch.ones(2,3)), torch.tensor([-2.,2.]), torch.randn(2,3)); return {"mixed_hidden_mean": float(h.mean()), "teacher_detached": not target.requires_grad}
    if key == "irekogpt":
        w, basis = ireko_nested_subnetwork(torch.eye(6), torch.eye(6), width=3); return {"width": w.shape[0], "basis_columns": basis.shape[1]}
    if key == "sharpening-tax": return {"tax_at_8": float(sharpening_tax(torch.tensor(.3), torch.tensor(.1), samples=8))}
    if key == "carm":
        mask, drift = carm_response_mask(torch.log(torch.tensor([[10.,.1],[1.01,.99]])), torch.zeros(2,2), threshold=1.1); return {"accepted": int(mask.sum()), "max_drift": float(drift.max())}
    if key == "gmc-grpo":
        w = group_mass_cap(torch.rand(3,4)*2, mass_cap=1); return {"max_group_mass": float(w.sum(-1).max())}
    if key == "gaw-po":
        w = gradient_aligned_rejected_weights(torch.randn(5,4), torch.randn(4)); return {"weight_mean": float(w.mean()), "tokens": len(w)}
    if key == "sharpo":
        a = sharpo_segment_advantages(torch.tensor(1.), torch.randn(6), torch.randn(6), ((0,3),(3,6))); return {"credit_mean": float(a.mean()), "segment_gap": float((a[:3].mean()-a[3:].mean()).abs())}
    if key == "tvrl":
        c = token_level_video_credit(torch.randn(2,5,4), group_advantage=1.5); return {"credit_mean": float(c.mean()), "tokens": c.numel()}
    if key == "lego-opd":
        p = lego_opd_teacher(torch.randn(2,7), torch.randn(2,7), grounding_strength=.7); return {"probability_sum": float(p.sum(-1).mean())}
    if key == "drift-opd": return {"loss": float(drift_opd_loss(torch.randn(3,7), torch.randn(3,7), torch.rand(3), potential_weight=.5))}
    if key == "autocompact":
        row, audit = autocorrect_compaction(False,"stale","repeat",lambda _: {"decision":True,"summary":"root","next_action":"patch"}); return {"fields_corrected": sum(audit.values()), "will_compact": row["decision"]}
    if key == "belief-state-pos":
        state, trapped = update_belief_state({"facts":{},"unresolved":("door",)}, {}, ("door",)); return {"unresolved": len(state["unresolved"]), "trapped": trapped}
    if key == "pace-capability":
        allowed, audit = pace_authorize({"tool":"shell","effects":("write",),"influenced_by":("request",)}, {"shell":("write",)}, {"trusted_sources":("request",)}); return {"allowed": allowed, "tainted": audit["tainted"]}
    if key == "rule-evolve":
        selected, audit = rule_evolve_select(("base",), ("better-rule",), len); return {"selected_length": len(selected), **audit}
    if key == "jev-spawn":
        actions, p = jev_spawn(torch.tensor([.6,.3,.1]), ("a","b","c"), (0.,2.,0.), branches=2); return {"branches": len(actions), "probability_sum": float(p.sum())}
    if key == "memfit":
        store=MemFitStore(); store.append("budget ten",segment="f"); store.append("launch Friday",segment="r"); rows=store.retrieve(("budget",),{1:.1},limit=1); return {"stored":len(store.turns),"retrieved":len(rows)}
    raise KeyError(key)


def aggregate(rows):
    result = {}
    for key in rows[0]:
        values = [row[key] for row in rows]
        if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
            result[f"{key}_mean"] = statistics.fmean(values)
    return result


def render(record):
    summary, formula, result, boundary = DETAILS[record["key"]]
    upstream = f"是：[{record['code']}]({record['code']})" if record.get("code") else "否：截至 2026-10-03 未找到原作者公开实现"
    module = module_for(record)
    if record["domain"] == "recommendation":
        source = f"src/auto_research/reproductions/{record['key'].replace('-', '_')}/"
    else:
        source = module
    return f"""# {record['title']}

> **复现级别：L1 核心机制诊断。** {boundary}

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv v1]({record['paper_url']}) |
| 公司/机构 | {record['first_author_affiliation']}（按第一作者署名单位） |
| 首次公开日期 | {record['published']}（arXiv v1） |
| 原文开源代码 | {upstream} |
| Adapter | `{record['adapter']}` |
| 本地复现代码 | [`{source}`](https://github.com/daiwk/auto-research/tree/main/{source}) |

## 原始论文总结

### 背景与主要改动

{summary}

```mermaid
flowchart LR
  I[输入与当前状态] --> M[{record['adapter']} 核心机制]
  M --> A[可审计中间量]
  A --> O[输出或状态更新]
```

<!-- paper-figure:start -->
### 原论文关键图

[![{record['title']} 原论文关键图](assets/paper-figure-01.png)]({record['paper_url'].replace('/abs/', '/pdf/')})

> **原论文关键图**：展示核心架构、训练流程或系统协议。图片来自[原论文]({record['paper_url']})，版权归原作者所有。
<!-- paper-figure:end -->

### 核心公式

{formula}

### 论文离线与线上效果

{result}

## 本地复现

> **本地对照口径**：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- `diagnostic_only=true`，不进入正式能力排名。

## 复现边界

{boundary}
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
            "evaluation_protocol": {"tier":"l1_mechanism","formal_comparison":False,"diagnostic_only":True,"seeds":list(SEEDS),"claim_policy":"mechanism execution and invariants only"},
            "provenance": {"artifact_path":str(artifact.relative_to(ROOT)),"dataset_fingerprint":"oct03-public-mechanism-fixtures-v1","original_code_commit":"working tree"},
        }, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(readme.relative_to(ROOT))


if __name__ == "__main__":
    main()
