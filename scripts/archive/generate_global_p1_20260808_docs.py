#!/usr/bin/env python3
"""Generate full detail pages for the 15 P1 implementations."""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[1]
RUN = json.loads((ROOT / "docs/experiments/global-p1-20260808-seed42.json").read_text())
FIGURE_START = "<!-- paper-figure:start -->"
FIGURE_END = "<!-- paper-figure:end -->"

REPRO = {
    "twin-v2": ("离线层次聚类将百万级生命周期行为压缩成带规模信息的虚拟物品；在线 GSU 检索相关簇，ESU 以 cluster-aware target attention 精排。", r"a_c=q^\top k_c-\tfrac12\log |c|,\quad h=\sum_{c\in\operatorname{TopK}(a)}\sum_{i\in c}\alpha_i v_i.", "Kuaishou 三场景 Watch Time +0.672%/+0.800%/+0.728%，已服务约 4 亿 DAU 主流量。"),
    "sim": ("以候选 item 为 query，GSU 从终身行为中快速搜索相关子序列，ESU 再计算候选与子序列的精确注意力。", r"S=\operatorname{TopK}_{i\in H}s_{GSU}(q,i),\quad h_q=\sum_{i\in S}\operatorname{softmax}(q^\top k_i)v_i.", "Alibaba 展示广告主流量：CTR +7.1%，RPM +4.4%，最长历史 54,000。"),
    "crsd": ("先以 CPT、SFT 和多维偏好优化构建领域 reasoning LLM，再让同一轻量学生的普通输入与 reasoning-augmented 输入做对比式自蒸馏，线上无需推理链。", r"\mathcal L=\mathcal L_{label}+\lambda D_{KL}(p_s(\cdot|x,r)\Vert p_s(\cdot|x))+\gamma\mathcal L_{con}.", "Meituan 搜索广告 30% 流量：AdCTR +0.91%、AdCVR +1.06%、GTV +0.40%，bad case -30.5 个百分点。"),
    "clip": ("用独立图像/文本 encoder 将配对样本映射到同一单位球面，通过双向 batch contrastive objective 学习可迁移零样本表示。", r"\mathcal L=\tfrac12\operatorname{CE}(I T^\top/\tau,y)+\tfrac12\operatorname{CE}(T I^\top/\tau,y).", "4 亿图文对预训练；ImageNet zero-shot 达到原始监督 ResNet-50 水平，并评测 30 多个数据集。"),
    "llava": ("冻结视觉 encoder，用可训练 projector 把视觉特征映射到 LLM token 空间，再在 GPT-4 生成的多模态指令数据上做端到端 instruction tuning。", r"H_v=W_pE_v(I),\quad\mathcal L=-\sum_t\log p_\theta(y_t|H_v,x,y_{<t}).", "合成多模态指令集达到 GPT-4 的 85.1% 相对分；LLaVA+GPT-4 在 ScienceQA 为 92.53%。"),
    "speculative-decoding": ("小 draft model 并行提出多个 token，target model 一次验证整个块；拒绝时从校正后的残差分布采样，从而严格保持 target 分布。", r"a(x)=\min(1,p(x)/q(x)),\quad p'(x)\propto[p(x)-q(x)]_+.", "T5-XXL 报告 2–3× 加速且输出分布完全一致。"),
    "awq": ("利用 calibration activation 找到显著输入通道，通过等价通道缩放保护约 1% 关键权重，再执行硬件友好的统一低比特 weight-only 量化。", r"XW=(X S^{-1})(S W),\quad S_j=(\mathbb E|X_j|)^\alpha,\quad \alpha^*=\arg\min\|XW-XS^{-1}Q(SW)\|^2.", "AWQ 在语言、代码、数学与多模态模型上优于既有 PTQ；TinyChat 在桌面和移动 GPU 上超过 FP16 3×。"),
    "medusa": ("在冻结或联合微调的 backbone 上增加多个 future-token heads，以 tree attention 同时验证候选分支，减少串行解码步数。", r"\mathcal L=\sum_{k=1}^K\lambda_k\operatorname{CE}(p_k(x_{t+k}|h_t),x_{t+k}).", "Medusa-1 超过 2.2×，Medusa-2 为 2.3–3.6×，并保持生成质量。"),
}

POST = {
    "minirl": ("2512.01374", "Stabilizing Reinforcement Learning with LLMs", "2025-12-01", "Chujie Zheng（按一作归档）", "否：未发现/未发布原作者官方代码仓库", "分解训推差异与 policy staleness，on-policy 使用 importance correction，off-policy 结合 clipping 与 MoE Routing Replay。", r"\rho_t=\pi_\theta/\pi_{rollout},\quad \mathcal L=-\mathbb E[\operatorname{clip}(\rho_t)A_t\log\pi_\theta],\quad z_t=z_t^{rollout}.", "30B MoE、数十万 GPU 小时实验显示稳定后不同 cold start 最终表现接近。"),
    "missing-old-logits": ("2605.12070", "Missing Old Logits in Asynchronous Agentic RL", "2026-05-12", "Zhong Guan（按一作归档）", "否：未发现/未发布原作者官方代码仓库", "指出异步 RL 丢失历史训练侧 logits 后，训推校正与策略陈旧校正发生语义混叠；给出快照、old-logit model、中断同步和 PPO-EWMA 修复。", r"\rho=\underbrace{\pi_{train}^{old}/\pi_{infer}^{old}}_{train/infer}\underbrace{\pi_\theta/\pi_{train}^{old}}_{staleness}.", "论文报告 revised PPO-EWMA 同时提升训练速度和优化效果；无生产 A/B。"),
    "stare": ("2606.19236", "STARE: Surprisal-Guided Token-Level Advantage Reweighting", "2026-06-17", "Haipeng Luo（按一作归档）", "是：[原作者仓库](https://github.com/hp-luo/STARE)", "按 batch surprisal 分位数识别 entropy-critical token，重加权其 advantage，并以目标 entropy 闭环 gate 调节方向。", r"\Delta H_t\approx A(\tau)\,g_\theta(x_t),\quad \tilde A_t=w(s_t,H-H^*)A(\tau).", "1.5B–32B、短/长 CoT 与多轮工具任务均维持 entropy；AIME24/25 平均 accuracy 超过 DAPO 4%–8%。"),
}

AGENT = {
    "agent-r1": ("2511.14460", "Agent-R1", "2025-11-18", "Mingyue Cheng（按一作归档）", "是：[原作者仓库](https://github.com/AgentR1/Agent-R1)", "把每次 agent/environment 交互作为独立 transition，以可插拔上下文管理、环境接口与优化器支持 token 或 step 级信用。", r"\tau=(s_t,a_t,o_{t+1})_{t=1}^T,\quad A_t=\delta_t+\gamma\lambda A_{t+1}.", "技术报告展示统一框架对多轮 agentic RL 工作流的支持；无生产 A/B。"),
    "camel": ("2303.17760", "CAMEL", "2023-03-31", "Guohao Li（按一作归档）", "是：[原作者仓库](https://github.com/camel-ai/camel)", "用 inception prompting 固定 user/assistant 的角色、目标和边界，通过轮流消息完成任务并生成可研究的多 Agent 社会轨迹。", r"m_t^A\sim\pi_A(\cdot|r_A,g,h_t),\quad m_t^B\sim\pi_B(\cdot|r_B,g,h_t,m_t^A).", "NeurIPS 2023 系统研究多 Agent instruction-following cooperation；无生产 A/B。"),
    "toolbench": ("2305.16504", "ToolBench / ToolLLM", "2023-05-25", "Qiantong Xu（按一作归档）", "否：未发现/未发布该论文原作者官方代码仓库", "分析开源 LLM 工具失败后，组合程序化使用样例、system prompt、in-context demonstration retriever 与生成格式约束。", r"a^*=\arg\max_a p_\theta(a|x,D_{tool},p_{sys}),\quad R=\mathbf1[\operatorname{execute}(a)=y].", "最高 90% tool success；8 个 ToolBench 任务中 4 个可与 GPT-4 竞争。"),
    "gaia": ("2311.12983", "GAIA", "2023-11-21", "Grégoire Mialon（按一作归档）", "是：[官方 benchmark](https://huggingface.co/gaia-benchmark)", "以 466 个真实问题联合考查推理、多模态、网页浏览与工具使用，采用精确短答案和三级难度。", r"\operatorname{score}=N^{-1}\sum_i\mathbf1[\operatorname{normalize}(\hat y_i)=\operatorname{normalize}(y_i)].", "人类 92%，带插件 GPT-4 15%；300 个答案保留用于 leaderboard。"),
}


def diagram(label):
    return f'''```mermaid
flowchart LR
 A["公开输入"] --> B["{label} 核心机制"]
 B --> C["同预算训练 / 执行"]
 C --> D["公开评测与诊断"]
```'''


def repro_page(key):
    adapter = get_adapter(key); result = json.loads((ROOT / "docs/reproductions" / f"{adapter.paper.arxiv_id}-{key}" / "metrics/public-seed42.json").read_text())
    summary, formula, original = REPRO[key]
    code = f"是：[原作者仓库]({adapter.paper.code_url})" if adapter.paper.code_url else "否：未发现/未发布原作者官方代码仓库（核查日期：2026-08-08）"
    metric = "ndcg_at_10" if "ndcg_at_10" in result["baseline"] else next(k for k in result["baseline"] if k != "name")
    base, method = result["baseline"][metric], result["method"][metric]
    delta = 100 * (method - base) / max(abs(base), 1e-12)
    paper_label = adapter.paper.publication_label or f"arXiv {adapter.paper.arxiv_id}"
    return f'''# {adapter.paper.title}

> **保真度：{adapter.fidelity.label}**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [{paper_label}]({adapter.paper.url}) |
| 公司/机构 | {adapter.paper.organization} |
| 首次公开日期 | {adapter.paper.published}（arXiv v1） |
| 原文开源代码 | {code} |
| Adapter | `{key}` |
| 本地复现代码 | [`src/auto_research/reproductions/{key.replace('-', '_')}/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/{key.replace('-', '_')}/) |

## 原始论文总结

### 背景与主要改动

{summary}

{diagram(key)}

### 核心公式

$$
{formula}
$$

### 论文离线与线上效果

{original}

## 本地复现

> **本地对照口径**：基线为 `{result['baseline']['name']}`，实验组为 `{result['method']['name']}`，只改变论文核心机制；`{metric}` {base:.4f} → **{method:.4f}，相对基线 {delta:+.2f}%**。

```bash
auto-research reproduce --paper {key} --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

{result['scope']} 本地相对变化不得与原文指标混写。
'''


def method_page(key, item, module):
    pid, title, date, org, code, summary, formula, original = item
    row = RUN["post_training" if module == "post-training" else "agent"][key]
    if module == "post-training":
        local = f"Arithmetic candidate suite、120 steps、seed 42：accuracy {row['baseline']['accuracy']:.4f} → **{row['final']['accuracy']:.4f}（{100*row['relative_accuracy']:+.2f}%）**。"
        command = f"auto-research post-train --algorithm {key} --dataset arithmetic-smoke --maximum-examples 256 --steps 120 --seed 42"
        code_dir = "src/auto_research/post_training/"
    else:
        m = row["metrics"]
        local = f"{row['benchmark']}、120 episodes、seed 42：joint success **{m['joint_success']:.4f}**，average cost **{m['average_cost']:.4f}**。"
        command = f"auto-research agent-study --method {key} --benchmark {row['benchmark']} --episodes 120 --seed 42"
        code_dir = "src/auto_research/agent_research/"
    return f'''# {title}

> **保真度：核心机制复现**。本页不把确定性 mini-suite 冒充原论文完整 benchmark。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [{title}（arXiv {pid}）](https://arxiv.org/abs/{pid}) |
| 公司 / 机构 | {org} |
| 首次公开日期 | {date}（arXiv v1） |
| 原作者代码 | {code} |
| 本地 adapter / 方法键 | `{key}` |
| 本地复现代码 | [`{code_dir}`](https://github.com/daiwk/auto-research/tree/main/{code_dir}) |

## 原始论文总结

### 背景与主要改动

{summary}

{diagram(key)}

### 核心公式

$$
{formula}
$$

### 论文离线与线上效果

{original} 论文未报告生产线上 A/B，本页不补造线上数字。

## 本地复现

{local}

```bash
{command}
auto-research evolve --model {"post-training" if module == "post-training" else "agent"} --dataset {"arithmetic-smoke" if module == "post-training" else row['benchmark']} --direction "组合 {key} 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`../../experiments/global-p1-20260808-seed42.json`](../../experiments/global-p1-20260808-seed42.json)。

## 复现边界

本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。
'''


def write_page(target: Path, content: str) -> None:
    """Keep a previously synchronized original-paper figure on regeneration."""

    if target.exists():
        previous = target.read_text(encoding="utf-8")
        if FIGURE_START in previous and FIGURE_END in previous:
            figure = previous.split(FIGURE_START, 1)[1].split(FIGURE_END, 1)[0]
            block = f"{FIGURE_START}{figure}{FIGURE_END}\n\n"
            content = content.replace("### 核心公式\n", block + "### 核心公式\n", 1)
    target.write_text(content, encoding="utf-8")


def main():
    for key in REPRO:
        adapter = get_adapter(key); target = ROOT / "docs/reproductions" / f"{adapter.paper.arxiv_id}-{key}" / "README.md"
        target.parent.mkdir(parents=True, exist_ok=True); write_page(target, repro_page(key))
    for module, rows in (("post-training", POST), ("agent-research", AGENT)):
        for key, item in rows.items():
            target = ROOT / "docs" / module / f"{item[0]}-{key}" / "README.md"
            target.parent.mkdir(parents=True, exist_ok=True); write_page(target, method_page(key, item, module))


if __name__ == "__main__":
    main()
