#!/usr/bin/env python3
"""Run experiments and document historical B04--B06 reproductions."""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.reproductions.historical_b04_b06_metadata import ENTRIES
from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "reproductions"
CHECKED = "2026-08-24"

METHODS = {
    "prl-puts": ("双头 Q 网络分别估计 Repin 与 P2P utility，再通过 Pareto sweeping 离线筛选不劣策略；线上仅切换可治理的权重策略，不更换模型。", "a^*=\\arg\\max_a[\\alpha Q_{repin}(s,a)+(1-\\alpha)Q_{p2p}(s,a)]", "双目标 Q 网络", "Pareto 策略扫描", "用户分群策略"),
    "ektm": ("让 CTR 表示按 CVR 任务相似度向多个转化塔迁移，并以难例感知损失抑制负迁移，保持多任务部署成本可控。", "F_i=\\operatorname{mean}(f_{ctr},\\hat s_{i1}f^1_{cvr},\\ldots,\\hat s_{iT}f^T_{cvr})", "CTR/CVR 多任务", "相似度知识迁移", "难例增强预测"),
    "adasid": ("按碰撞负载、语义相容性和训练阶段动态放松 SID 重叠约束，避免把所有碰撞等价惩罚。", "\\lambda_{ij}(t)=g(o_{ij},\\operatorname{sim}_{ij},t),\\quad L=L_{rq}+\\sum_{ij}\\lambda_{ij}L_{overlap}", "多模态 Item", "自适应碰撞调节", "AdaSID 检索"),
    "unirec-coa": ("在 SID 前生成品类、卖家和品牌等属性链，用容量受限量化抑制热点 token 塌缩，并以任务上下文稳定多场景生成。", "p(a,s|u)=p(a|u)\\prod_l p(s_l|a,s_{<l},u)", "Chain-of-Attribute", "容量约束 SID", "RFT+DPO 解码"),
    "uniscale": ("ES³ 从曝光外全空间扩充数据，HHSFT 分层融合异构样本；数据规模和模型容量协同扩展，并配合低成本部署。", "h^{l+1}=h^l+\\sum_d g_d(h^l)\\,FFN_d(h^l)", "Entire-Space 数据", "HHSFT 分层融合", "搜索排序"),
    "gatesid": ("共享注意力融合语义与协同行为，再用冷启动感知 gate 调节对比对齐强度：新物品偏语义，热门物品保留协同信号。", "z_i=g_i z_i^{sem}+(1-g_i)z_i^{coll},\\quad g_i=\\sigma(Wx_i)", "语义/协同序列", "GFSA+GRCA", "冷启动排序"),
    "aigq": ("Direct 路径负责低时延，Reasoning 路径补足复杂意图；IL-GRPO 用线上 CTR 奖励优化整组 query，并采用离线/在线混合服务。", "J=\\mathbb E[R(Q)]-\\beta D_{KL}(\\pi_\\theta\\|\\pi_{ref})", "行为上下文压缩", "Direct+Reasoning", "IL-GRPO Query 列表"),
    "safro": ("满意度 reward 同时建模即时互动与长期留存，Dual-Relative PO 在组内和任务间归一化优势，关系门控融合多搜索目标。", "A_{i,t}=\\frac{r_{i,t}-\\mu_t}{\\sigma_t+\\epsilon}+\\frac{r_{i,t}-\\mu_i}{\\sigma_i+\\epsilon}", "满意度 Reward", "Dual-Relative PO", "任务关系融合"),
    "sort-ranking": ("系统重做特征 token 化、注意力和 FFN，并以面向工业硬件的结构压缩长序列，使单一 Transformer 替代传统 DLRM。", "H'=H+\\operatorname{MHA}(H),\\quad H''=H'+\\operatorname{FFN}(H')", "工业特征 Tokens", "优化 Attention/FFN", "多场景排序"),
    "quasid": ("用业务资格信号决定碰撞对的 margin，而不是统一排斥；反馈稀疏或冷启动 item 得到更强的可辨识 SID。", "L_{qual}=\\sum_{ij}q_{ij}[m_{ij}-d(z_i,z_j)]_+", "残差量化 SID", "资格感知碰撞", "召回/排序复用"),
    "gpl-prerank": ("LLM 从用户行为生成兴趣锚点，为未曝光召回候选产生伪标签；预排序器联合真实与伪监督，且线上不调用 LLM。", "L=L_{exposed}+\\lambda\\sum_{j\\in unexposed}CE(\\hat y_j^{LLM},p_j)", "兴趣锚点", "LLM 伪标签", "无额外时延预排序"),
    "ltv-video-ranking": ("PDQ 消除位置偏差，归因模块分配会话内长期价值，作者周期任务再引入跨日优质创作者价值。", "q_i=F_{Y|pos}^{-1}(F_{Y|pos_i}(y_i)),\\quad s=\\sum_k w_k v_k", "即时行为", "PDQ+价值归因", "长期多目标融合"),
    "rgalign-rec": ("先让 LLM 从上下文生成潜在 query，再用真实排序模型的 item 偏好构建正负 query，通过 RG-SFT 与 DPO 对齐 top-rank 意图。", "L_{DPO}=-\\log\\sigma(\\beta[\\log\\pi(q^w)-\\log\\pi(q^l)])", "上下文→潜在 Query", "Ranking Guide", "RG-SFT+DPO"),
    "linkedin-feed-sr": ("将 Feed 候选、交互历史和上下文统一成超长序列，采用 HSTU 式目标注意力、负样本自由评估及增量服务优化。", "h_t=\\operatorname{HSTU}(e_{1:t}),\\quad s_i=\\langle h_t,e_i\\rangle", "长 Feed 历史", "Sequential Recommender", "全候选排序"),
    "cadet": ("Decoder-only Transformer 先编码可缓存历史，候选打分后再注入 post-scoring context，避免训练与服务错位并统一广告 CTR 模型。", "h_i'=h_i+\\operatorname{Attn}(q(c),K(h_{\\le i}),V(h_{\\le i}))", "历史+候选序列", "CADET Block", "Context-conditioned CTR"),
    "diffureason": ("Thinking Tokens 形成连续潜在意图，扩散去噪逐步修正冲突兴趣，GRPO 再把连续生成与离散排序奖励端到端对齐。", "z_{t-1}=\\mu_\\theta(z_t,h)+\\sigma_t\\epsilon,\\quad J=\\mathbb E[A\\log\\pi_\\theta]", "Thinking Tokens", "Diffusion Refinement", "GRPO 排序"),
    "sarm": ("离线 MLLM 生成直播语义 anchor，轻量 SAE 将 anchor 注入端到端排序；非对称部署只在线更新排序器，避免 MLLM 时延。", "h_a=SAE(tokens(a)),\\quad s=Rank(h_{id},h_a,h_u)", "MLLM 语义 Anchor", "SAE 非对称部署", "直播排序"),
    "ml-dcn": ("把 DCNv2 的全维交叉替换为可调内部维度的低秩交叉，并以可学习 mask 选择交叉通道，在相同 FLOPs 下扩大容量。", "x_{l+1}=x_l+x_0\\odot[U_l(V_l(x_l\\odot m_l))]+b_l", "稀疏特征", "Masked Low-Rank Cross", "Ads CTR"),
    "rag-qac": ("先从可搜索目录检索补全证据，再以 SFT 和 DPO 同时对齐相关性、安全、参与度、目录/上下文 groundedness 与多样性。", "R=\\sum_k w_kR_k,\\quad L=L_{SFT}+\\lambda L_{DPO}", "Prefix+RAG", "SFT+DPO 多目标", "Query 补全"),
}


def fmt(value: float) -> str:
    return f"{value:+.2f}%"


def main() -> None:
    for key, row in ENTRIES.items():
        result = get_adapter(key).run(ROOT / "data", 42)
        directory = DOCS / f"{row.arxiv_id}-{key}"
        metrics = directory / "metrics"
        metrics.mkdir(parents=True, exist_ok=True)
        (metrics / "public-seed42.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary, formula, left, middle, right = METHODS[key]
        upstream = f"是：[{row.code_url.rsplit('/', 1)[-1]}]({row.code_url})" if row.code_url else f"否：原文未提供官方/作者代码（核查日期：{CHECKED}）"
        local = key.replace("-", "_")
        base, method = result["baseline"], result["method"]
        ndcg = result["relative"]["ndcg_at_10_percent"]
        page = f"""# {row.title}

> **保真度：核心机制复现**。原文线上结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv {row.arxiv_id}](https://arxiv.org/abs/{row.arxiv_id}) |
| 公司/机构 | {row.organization} |
| 首次公开日期 | {row.published}（arXiv v1） |
| 原文开源代码 | {upstream} |
| Adapter | `{key}` |
| 本地复现代码 | [`src/auto_research/reproductions/{local}/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/{local}/) |

## 原始论文总结

### 背景与主要改动

{summary}

```mermaid
flowchart LR
 A["{left}"] --> B["{middle}"] --> C["{right}"]
```

### 核心公式

$$
{formula}
$$

### 论文离线与线上效果

原文线上证据：**{row.metric} {fmt(row.lift)}**（{row.traffic}，{row.source_location}）。论文私有口径不能与下方 MovieLens 指标直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 `{key}` 核心机制，相对 NDCG@10 {fmt(ndcg)}。

MovieLens-100K、{result['dataset']['users']} users / {result['dataset']['items']} items、seed 42：NDCG@10 {base['ndcg_at_10']:.4f} → **{method['ndcg_at_10']:.4f}（{fmt(ndcg)}）**，Hit@10 {base['hit_at_10']:.4f} → {method['hit_at_10']:.4f}。验证集只选择混合权重，测试集未参与调参。

```bash
auto-research reproduce --paper {key} --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

{result['scope']} 本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。
"""
        (directory / "README.md").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
