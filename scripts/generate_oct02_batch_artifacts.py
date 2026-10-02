#!/usr/bin/env python3
"""Generate reviewed docs and deterministic L1 receipts for the Oct-2 batch."""

from __future__ import annotations

import json
from pathlib import Path
import statistics
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.agent_research.latest_20261002 import (  # noqa: E402
    CurriculumArm,
    NonDestructiveMemory,
    active_saddler_choice,
    defa_decisive_error,
    flowright_hierarchical_credit,
    safe_self_improvement_select,
    veriharness_select,
)
from auto_research.foundation_latest_20261002 import (  # noqa: E402
    TACO,
    gfg_mixed_objective,
    veto_compress,
)
from auto_research.latest_20261002_catalog import LATEST_METHOD_PAPERS  # noqa: E402
from auto_research.post_training.latest_20261002 import (  # noqa: E402
    dependency_shaped_rewards,
    fault_terminal_redistribution,
    range_grpo_advantages,
    where_opd_loss,
)
from auto_research.recommendation_latest_20261002 import (  # noqa: E402
    basis_vq,
    effective_training_time,
    gear_collision_rerank,
    gris_hierarchical_ids,
    repair_preference_state,
)

SEEDS = (42, 43, 44)

DETAILS = {
    "gemini-for-google": {
        "summary": "从企业开发历史中提取高价值代码与交互信号，经过去重、质量过滤和污染控制形成中训练数据；用通用数据回放抑制灾难性遗忘，再做面向内部工具的后训练和部署评测。",
        "formula": "$L=(1-\\lambda)L_{enterprise}+\\lambda L_{replay}$；本地算子显式暴露企业适配与通用能力保留之间的混合比例。",
        "result": "29,000 名开发者盲 A/B 中，平均每轮交互次数下降 23%，代码存活率提高 16.8%。",
        "boundary": "只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。",
        "module": "src/auto_research/foundation_latest_20261002.py",
    },
    "gear": {
        "summary": "GEAR 用正交基参数化 BasisVQ/BasisRQ，使码本更新具有全局共享和稳定旋转；生成器输出层级 token，碰撞 item 再由上下文条件 reranker 精排。",
        "formula": "$q(z)=B c_{argmin_j\\|zB-c_j\\|}$；碰撞组内按 $s_i=h_u^Te_i$ 排序。",
        "result": "抖音广告 7 天线上 A/B、每组 5% 流量：ADSS +0.563%、ADVV +0.658%；冷启动激活率 +1.46%。",
        "boundary": "执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。",
        "module": "src/auto_research/recommendation_latest_20261002.py",
    },
    "dars": {
        "summary": "把任务进度表示为带先决条件的 predicate 图；验证、失效和修复事件更新图状态，最近破损依赖按图距离衰减已完成工作的 credit，独立分支不受牵连。",
        "formula": "$r_t=\\Phi(s_{t+1})-\\Phi(s_t)$，依赖破损后的 predicate 权重为 $\\gamma^{d}$。",
        "result": "同预算下 ALFWorld 相对 GiGPO 最高提升 10 点，并在 WebShop、Search-R1、AIME 与工具无关推理上验证。",
        "boundary": "执行依赖衰减、失效/修复与 potential 差分；未训练 1.5B–8B 模型，官方仓库当前仅发布接口说明、代码仍在准备。",
        "module": "src/auto_research/post_training/latest_20261002.py",
    },
    "active-saddler": {
        "summary": "把反复出现的失败模式动态实例化为非平稳 bandit arm；课程控制器在发现新场景和重访已知弱点之间选择，并随 harness 修复结果更新优先级。",
        "formula": "$a_t=argmax_a[\\hat v_a+c\\sqrt{\\log(t)/(n_a+1)}]$，并周期性 Draw 未见场景。",
        "result": "相同 harness optimizer 与 rollout 预算下，GAIA2 Pass@1 +4.4 点，Terminal-Bench 2.0 +7.5 点。",
        "boundary": "执行动态 failure arm 与探索/利用调度；不调用 AutoSaddler 或真实 GAIA2/Terminal-Bench 环境。",
        "module": "src/auto_research/agent_research/latest_20261002.py",
    },
    "safe-self-improvement": {
        "summary": "把检测、当前可执行实现选择和下一轮编辑源分开；所有候选必须对当前条件重新验证，若无候选通过则回滚 founder，而不是继续运行已失败 incumbent。",
        "formula": "$p_{run}=argmax_{p\\in V_{current}} score(p)$；若 $V_{current}=\\varnothing$，执行 founder rollback。",
        "result": "历史分数在 48 条框架历史中的 22 条保留不安全程序；完整验证与 validated rollback 在核心轨迹研究中最终全正确，并保留超过 43% 部署节省。",
        "boundary": "执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。",
        "module": "src/auto_research/agent_research/latest_20261002.py",
    },
    "range-grpo": {
        "summary": "用 conformal reward interval 代替单点 judge 分数；组内只对可确定排序的区间产生方向信号，区间重叠时不制造虚假偏好。",
        "formula": "$A_i=G^{-1}\\sum_j relation([l_i,u_i],[l_j,u_j])$；区间塌缩为点时恢复 DR-GRPO。",
        "result": "论文在所评估半监督方法中取得最高的分布内与分布外平均表现，同时使用更少训练资源。",
        "boundary": "执行成对区间关系与 point-limit；不拟合 conformal judge，也不做大模型 GRPO。",
        "module": "src/auto_research/post_training/latest_20261002.py",
    },
    "veriharness": {
        "summary": "同一基础模型得到 workspace、证据工具和可复用验证技能；disagreement resolver 查证冲突 claim，consensus challenger 主动质疑共同 claim 和遗漏要求。",
        "formula": "$score(y)=supported(y)-contradicted(consensus)-\\epsilon|claims(y)|$。",
        "result": "五个长程 workspace benchmark 上，相对单 rollout 平均提高 6.2（Gemini 3.5 Flash）和 6.4 点（Claude Opus 4.8），并发布约 26k rollouts。",
        "boundary": "执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。",
        "module": "src/auto_research/agent_research/latest_20261002.py",
    },
    "effective-training-time": {
        "summary": "把端到端 wall time 分为真正消费新数据的训练时间与初始化、编译、checkpoint、发布和恢复等生命周期损耗，再按 owner 定位和优化。",
        "formula": "$ETT=training\\_on\\_new\\_data / wall\\_time$。",
        "result": "代表模型 ETT 平均提高 15.5%，最大 workload 达 85%；部署后全 fleet 从约 80% 提升到 90% 以上。",
        "boundary": "执行 ETT 分解与 owner loss 归因；这是用户批准的生产基础设施例外，不声称推荐模型效果或线上 A/B 收益。",
        "module": "src/auto_research/recommendation_latest_20261002.py",
    },
    "taco-optimizer": {
        "summary": "每个二维权重列只保留绝对值最大的梯度分量及符号，形成 column-wise one-sparse steepest direction；低精度列状态替代逐参数 dense optimizer state。",
        "formula": "$D_{ij}=sign(G_{ij})$ 当 $i=argmax_k|G_{kj}|$，否则为 0。",
        "result": "OPT-13B 上 optimizer state 27.7GB→0.16GB（174×），峰值显存 80.6GB→27.5GB（2.9×）。",
        "boundary": "执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。",
        "module": "src/auto_research/foundation_latest_20261002.py",
    },
    "veto": {
        "summary": "先在帧内合并语义近邻 token，再对压缩后的 frame representation 做跨帧去冗余；空间先行显著降低全局时间匹配成本。",
        "formula": "$X'=C_{time}(C_{space}(X))$；本地用确定性最远点代表验证双轴顺序与预算。",
        "result": "LLaVA-OneVision-7B 推理最高快 45%；10% token 预算下准确率 55.7%。",
        "boundary": "执行 GPU 上空间先行、时间后继的双轴压缩；未加载 7B VLM、真实视频 benchmark 或复述论文吞吐为本地结果。",
        "module": "src/auto_research/foundation_latest_20261002.py",
    },
    "mem-plus-plus": {
        "summary": "写入时完整保留文档、日期和作者，不调用生成模型做不可逆摘要；读取时先按问题时间过滤，再融合 lexical 与 semantic ranking。",
        "formula": "$score(d,q)=BM25(d,q)+sim(e_d,e_q)$，且仅检索 $time(d)\\le time(q)$。",
        "result": "OrgMemBench 相对最强 memory baseline 提升 8.0–13.1 点；gpt-4.1-mini 比 RAG 高 2.6 点。",
        "boundary": "执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。",
        "module": "src/auto_research/agent_research/latest_20261002.py",
    },
    "defa": {
        "summary": "融合 protocol relation 和语义依赖构造 event dependency graph，再从违规事件逆向追踪 source 与下游影响，形成 failure propagation graph 并定位 decisive error。",
        "formula": "$e^*=argmax_{e\\in Ancestor(V)} error(e)$，同时保留 responsible agent 与传播子图。",
        "result": "在 Who and When 系列达到最佳 responsible-agent 与 exact-step 准确率；用于 Trace2Skill 后下游准确率再提高 6–15 点。",
        "boundary": "执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。",
        "module": "src/auto_research/agent_research/latest_20261002.py",
    },
    "my-fault": {
        "summary": "自诊断器提出错误类别与位置，只有经证据验证的 claim 才进入在线 error pricing；学得的相对成本把终局 credit 守恒地重分配到步骤。",
        "formula": "$\\sum_t r'_t=R$，$r'_t=R(1/T+\\bar p-p_t)$。",
        "result": "ALFWorld signal coverage 95%，相比 GRPO 41%、GiGPO 72%；在 ALFWorld 与 WebShop 上取得强改进。",
        "boundary": "执行 verified diagnosis、error cost 与守恒重分配；未共同训练策略/诊断模型。",
        "module": "src/auto_research/post_training/latest_20261002.py",
    },
    "flowright": {
        "summary": "利用 workflow 拓扑把稀疏结果拆为层级、结构感知的 role credit，使单角色自进化、上下游协同或多 Agent co-evolution 可共用一个 harness。",
        "formula": "$r_i=R\\,w_i/\\sum_jw_j$，$w_i=valid_i(1+children_i)$。",
        "result": "跨文档、幻灯片、图表、代码、数学和金融任务最高 +7.41%；多角色共同进化整体 +5.03%，单角色 +2.83%。",
        "boundary": "执行结构 credit 守恒分配；不生成 workflow、不训练 Qwen3.5，也不运行 DataWright。",
        "module": "src/auto_research/agent_research/latest_20261002.py",
    },
    "where-opd": {
        "summary": "程序化合成场景自动给出对象身份和空间坐标；teacher 接收文本化空间特权信息，student 只看图像与问题，在自己的 on-policy token 上蒸馏 teacher。",
        "formula": "$L=\\sum_t m_t KL(\\pi_T(\\cdot|x,g),\\pi_S(\\cdot|x))/\\sum_tm_t$。",
        "result": "只用合成场景后训练，在六个真实视觉 benchmark 上平均提高 3.23 点。",
        "boundary": "执行带 spatial mask 的 on-policy teacher KL；未生成场景、未加载 MLLM，也不把随机 logits 当作视觉效果。",
        "module": "src/auto_research/post_training/latest_20261002.py",
    },
    "gris": {
        "summary": "把 Semantic ID 构造重写为层级图划分：节点承载内容语义，边承载协同信号；图为空时退化为内容量化。",
        "formula": "$SID(i)=RecursivePartition(G,X)_i$；每层显式组合平滑后的语义与图邻接。",
        "result": "多个真实数据集上相对 CF-aware SOTA 的 Hit@10 最高提高 52%。",
        "boundary": "执行 graph-informed 层级二分 ID；用户批准为学术/Evolve 例外，无线上 A/B，不进入工业证据结论。",
        "module": "src/auto_research/recommendation_latest_20261002.py",
    },
    "repair-state": {
        "summary": "冻结 encoder 与原 task head，从已有 forward cache 中比较各 timestep 表征和当前 preference state，选择长程、近期或局部 burst 的纠正证据并做 residual repair。",
        "formula": "$z'=z+\\sum_{t\\in TopK}softmax(q^T(h_t-z))(h_t-z)$。",
        "result": "12 个推荐 host 全部改善；Mamba4Rec/MovieLens MRR +3.96 点，head-only 仅 +0.19；个性化生成最高 +25.23%。",
        "boundary": "执行 frozen-cache evidence selection 与 residual correction；用户批准为学术/Evolve 例外，无线上 A/B。",
        "module": "src/auto_research/recommendation_latest_20261002.py",
    },
}


def run(record, seed):
    import torch

    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    key = record["key"]
    if key == "gemini-for-google":
        current, replay = torch.tensor(1.2), torch.tensor(.8)
        return {"mixed_loss": float(gfg_mixed_objective(current, replay, replay_fraction=.2))}
    if key == "gear":
        basis, _ = torch.linalg.qr(torch.randn(5, 5))
        quantized, ids = basis_vq(torch.randn(12, 5), basis, torch.randn(8, 5))
        order, scores = gear_collision_rerank(torch.randn(5), quantized[:4], [(0,), (0,), (1,), (1,)])
        return {"used_codes": int(ids.unique().numel()), "reranked_items": len(order), "score_std": float(scores.std())}
    if key == "dars":
        rewards, state = dependency_shaped_rewards([
            {"verify": ["a"]}, {"verify": ["b"]}, {"invalidate": ["a"]}, {"repair": ["a"]},
        ], {"b": ("a",)})
        return {"reward_total": sum(rewards), "verified": len(state["verified"]), "broken": len(state["broken"])}
    if key == "active-saddler":
        action, target, audit = active_saddler_choice([CurriculumArm("tool", .7, 2), CurriculumArm("plan", .5, 1)], ("new",), iteration=seed % 7 + 2)
        return {"pulled_known_arm": action == "pull", "target_length": len(target), "audit_items": len(audit)}
    if key == "safe-self-improvement":
        selected, audit = safe_self_improvement_select([{"name": "unsafe", "score": 9}], lambda _: {"safe": False, "correct": True}, founder={"name": "founder"})
        return {"rollback": audit["rollback"], "selected_founder": selected["name"] == "founder"}
    if key == "range-grpo":
        advantages = range_grpo_advantages(torch.tensor([0., 1., 2.]), torch.tensor([.2, 1.2, 2.2]))
        return {"advantage_span": float(advantages.max() - advantages.min()), "advantage_sum": float(advantages.sum())}
    if key == "veriharness":
        selected, audit = veriharness_select([{"id": "a", "claims": ["x"]}, {"id": "b", "claims": ["x", "y"]}], lambda claim: claim == "x")
        return {"selected_a": selected == "a", **audit}
    if key == "effective-training-time":
        ett, losses = effective_training_time({"training": 80, "compile": 8, "checkpoint": 7, "recovery": 5})
        return {"ett": ett, "loss_fraction": sum(losses.values())}
    if key == "taco-optimizer":
        layer = torch.nn.Linear(16, 8, bias=False); layer(torch.randn(4, 16)).square().mean().backward()
        optimizer = TACO(layer.parameters(), lr=.01); before = layer.weight.detach().clone(); optimizer.step()
        return {"parameter_delta": float((layer.weight - before).norm()), "state_elements": optimizer.state_elements, "dense_elements": layer.weight.numel()}
    if key == "veto":
        compressed, audit = veto_compress(torch.randn(8, 16, 12), spatial_keep=4, temporal_keep=3)
        return {"output_tokens": int(compressed.shape[0] * compressed.shape[1]), **audit}
    if key == "mem-plus-plus":
        memory = NonDestructiveMemory(); memory.write(text="old budget", date="2026-01", author="a"); memory.write(text="new budget", date="2026-09", author="b")
        rows = memory.retrieve(["budget"], {"old budget": .1, "new budget": .2}, as_of="2026-06")
        return {"stored_documents": len(memory.documents), "retrieved_documents": len(rows), "future_document_hidden": rows[0]["text"] == "old budget"}
    if key == "defa":
        decisive, audit = defa_decisive_error([{"id": "a", "step": 0, "error_score": .9}, {"id": "b", "step": 1, "error_score": .2}, {"id": "c", "step": 2, "violates": True, "error_score": 0}], {"c": ("b",), "b": ("a",)})
        return {"selected_first_step": decisive["id"] == "a", "propagation_nodes": len(audit["propagation_nodes"])}
    if key == "my-fault":
        rows, audit = fault_terminal_redistribution([1.0], [[{"step": 1, "category": "tool", "verified": True}]], {"tool": 2.0})
        return {"credit_total": float(rows[0].sum()), **audit}
    if key == "flowright":
        credit = flowright_hierarchical_credit({"lead": {}, "worker": {"parents": ["lead"]}}, 1.0, {"lead": 1, "worker": 1})
        return {"credit_total": sum(credit.values()), "lead_credit": credit["lead"]}
    if key == "where-opd":
        loss = where_opd_loss(torch.randn(2, 4, 7), torch.randn(2, 4, 7), torch.tensor([[1, 1, 0, 0], [1, 0, 1, 0]]))
        return {"spatial_kl": float(loss)}
    if key == "gris":
        features = torch.randn(10, 4); adjacency = torch.eye(10); adjacency[:-1, 1:] += torch.eye(9)
        ids = gris_hierarchical_ids(features, adjacency, levels=3)
        return {"unique_ids": int(ids.unique(dim=0).shape[0]), "levels": ids.shape[1]}
    if key == "repair-state":
        repaired, audit = repair_preference_state(torch.randn(6), torch.randn(12, 6), torch.randn(6), top_k=3)
        return {"state_norm": float(repaired.norm()), "selected_timesteps": len(audit["selected_timesteps"])}
    raise KeyError(key)


def aggregate(rows):
    result = {}
    for key in rows[0]:
        values = [row[key] for row in rows]
        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            result[f"{key}_mean"] = statistics.fmean(values)
    return result


def render(record):
    detail = DETAILS[record["key"]]
    if record.get("upstream_note"):
        upstream = record["upstream_note"].replace(
            "https://github.com/JianhuiWei7/DARS",
            "[官方占位仓库](https://github.com/JianhuiWei7/DARS)",
        )
    elif record.get("code"):
        upstream = f"是：[{record['code']}]({record['code']})"
    else:
        upstream = "否：截至 2026-10-02 未找到原作者公开实现"
    gpu = ""
    if record.get("requires_gpu_validation"):
        gpu = f"\n- GPU 验证：[`{record['gpu_validation_artifact']}`](https://github.com/daiwk/auto-research/blob/main/{record['gpu_validation_artifact']})"
    exception = f"\n> **收录例外**：{record['selection_exception']}\n" if record.get("selection_exception") else ""
    module = detail["module"]
    return f"""# {record['title']}

> **复现级别：L1 核心机制诊断。** {detail['boundary']}
{exception}
## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv {record['paper_url'].rsplit('/', 1)[-1]}]({record['paper_url']}) |
| 公司/机构 | {record['first_author_affiliation']}（按第一作者署名单位） |
| 首次公开日期 | {record['published']}（arXiv v1） |
| 原文开源代码 | {upstream} |
| Adapter | `{record['adapter']}` |
| 本地复现代码 | [`{module}`](https://github.com/daiwk/auto-research/blob/main/{module}) |

## 原始论文总结

### 背景与主要改动

{detail['summary']}

```mermaid
flowchart LR
  I[输入/当前状态] --> M[{record['adapter']} 核心机制]
  M --> A[可审计中间量]
  A --> O[输出/更新状态]
```

<!-- paper-figure:start -->
### 原论文关键图

[![{record['title']} 原论文关键图](assets/paper-figure-01.png)]({record['paper_url'].replace('/abs/', '/pdf/')})

> **原论文关键图**：展示论文核心架构、训练流程或系统协议。图片来自[原论文]({record['paper_url']})，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

{detail['formula']}

### 论文离线与线上效果

{detail['result']}

## 本地复现

> **本地对照口径**：基线为机制关闭或默认状态，实验组为开启对应核心算子。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。

- 三种子诊断：[`metrics/mechanism-seeds42-44.json`](metrics/mechanism-seeds42-44.json)
- `diagnostic_only=true`，不进入正式能力排名。{gpu}

## 复现边界

{detail['boundary']}
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
                "diagnostic_only": True, "seeds": list(SEEDS),
                "claim_policy": "mechanism execution and invariants only",
            },
            "provenance": {
                "artifact_path": str(artifact.relative_to(ROOT)),
                "dataset_fingerprint": "oct02-public-mechanism-fixtures-v1",
                "original_code_commit": "working tree",
            },
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(readme.relative_to(ROOT))


if __name__ == "__main__":
    main()
