#!/usr/bin/env python3
"""Run and document the historical B01--B03 reproductions."""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.reproductions.historical_b01_b03_metadata import ENTRIES
from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "reproductions"
CHECKED = "2026-08-24"

METHODS = {
    "dynamic-codebook": ("把多级小语义码本压缩为动态更新的单级大码本，再保留独立碰撞码；既减少自回归步数，也用曝光加权更新抵抗码本漂移。", "r_i=e_i-c_{s_i},\\quad c_k\\leftarrow(1-\\eta)c_k+\\eta\\frac{\\sum_i w_i e_i\\mathbf1[s_i=k]}{\\sum_i w_i\\mathbf1[s_i=k]}", "多级 SID", "动态大码本", "碰撞码与短解码"),
    "netflix-mediafm": ("把冻结的 CLIP/MediaFM 多模态表示作为共享在线特征接入资产双塔，并以查询相似度增强搜索画布；离线 IPS 与 winner proxy 先筛选 checkpoint。", "s(a|u,q)=\\alpha\\langle u,a\\rangle+(1-\\alpha)\\langle q,a\\rangle", "冻结多模态表示", "统一资产双塔", "查询感知排序"),
    "ogr": ("TUSID 融合语义码与协同码，GL2P 直接规划整张 slate，SPA 再用保守策略优化对齐列表级反馈。", "J_{SPA}=\\mathbb E[R(Y)]-\\beta D_{KL}(\\pi_\\theta\\|\\pi_{SFT})", "统一 SID", "列表偏好规划", "保守策略对齐"),
    "inthq": ("双流分别保留行为与上下文表示，when/where/how/via 四个任务查询在多个层级交互检索，使任务信号进入编码器而非只留在任务头。", "h_t=\\sum_{m=1}^{M}\\operatorname{softmax}(q_tK_m^\\top)V_m", "长短双流", "任务交互查询", "分层多任务输出"),
    "pushdualgen": ("先生成可服务的 Semantic ID，再按需生成可跳过的解释 copy；在线侧融合 SID 与 copy 表示，同时保留解释一致性。", "p(s,c|h)=p(s|h)\\,p(c|s,h)^{\\mathbf1[g(h,s)=1]}", "SID 压缩", "SID→可选 Copy", "表示融合"),
    "recharness": ("将结构改造定义为有限 arm，用 bandit 根据历史收益和不确定性分配试验预算，再把胜者反馈写回下一轮候选。", "a_t=\\arg\\max_a[\\hat\\mu_a+\\sqrt{2\\log t/n_a}]", "候选结构 Arms", "Bandit 路由实验", "反馈更新"),
    "gala": ("先在 query-image-text 三元组上预训练多模态表示，再以行为奖励做 GRPO 对齐，最后用自适应门控融合多模态与 ID 表示。", "z=g\\odot z_{mm}+(1-g)\\odot z_{id},\\quad g=\\sigma(W[z_{mm};z_{id}])", "三元组预训练", "GRPO 行为对齐", "ID/多模态门控"),
    "feedback-policy": ("从用户反馈发现生成策略，以双空间关系蒸馏把策略压入轻量排序器，从而避免线上调用 LLM。", "\\mathcal L=\\mathcal L_{rank}+\\lambda\\|S_T-S_S\\|_F^2", "反馈归因", "策略发现", "关系蒸馏上线"),
    "real-estate-rerank": ("把对话需求、结构化房源属性、文本描述和候选集合统计交给 LLM 重排，用候选间比较补足向量召回的局部相关性。", "s_i=f_\\theta(q,p_u,x_i,\\operatorname{Agg}(X))", "对话与用户画像", "候选集合 LLM 重排", "房源顺序"),
    "adaptive-ad-load": ("在收入与转化约束下动态决定每次搜索展示多少广告，利用随机现场实验估计供给曲线，再由轻量策略选择 ad load。", "k^*(x)=\\arg\\max_k\\{R_k(x)+\\lambda C_k(x)\\}", "随机现场实验", "收益/转化估计", "自适应广告数"),
    "guess-where-you-go": ("把下一 POI 编成 Semantic ID 序列，并用时空特征、课程式预训练/SFT 与 EAKTO 强化优化长周期用户反馈。", "J=J_{SFT}+\\lambda\\mathbb E[A(s,a)\\log\\pi_\\theta(a|s)]", "时空历史与 SID", "CPT/SFT", "EAKTO 下一 POI"),
    "genpage": ("用一个生成模型直接输出整页而非逐阶段召回排序，并在 WBC/SFT 后以生产长期奖励进行 RL 后训练，同时处理业务规则和冷启动。", "\\pi^*=\\arg\\max_\\pi\\mathbb E_{Y\\sim\\pi(\\cdot|h)}[R_{page}(Y)]", "首页提示", "整页自回归生成", "WBC/RL 与规则"),
    "journeyformer": ("统一编码 Airbnb 长期和短期 guest journey，以事件类型、时间和 listing 表示构建序列，并通过缓存和稀疏计算满足线上时延。", "h_u=\\operatorname{Transformer}([e_i+e_{type}+e_{time}]_{i=1}^{L})", "长短旅程事件", "Journey Transformer", "Listing 排序"),
    "l2rec": ("共享 LLM 中插入按用户路由的双视图 LoRA-MoE，分别适配语义视图和行为视图，再由自适应跨视图门控融合。", "\\Delta W_v(u)=\\sum_{e\\in TopK(g_v(u))}g_{v,e}(u)B_{v,e}A_{v,e}", "语义/行为双视图", "个性化 LoRA-MoE", "跨视图融合"),
    "qgs": ("将 query 与 item 共同序列化做生成式搜索，Linear HSTU 以线性复杂度编码历史，HFG-Attention 再融合稀疏交叉特征。", "p(y|q,h)=\\prod_t p(y_t|q,h,y_{<t})", "Query+历史", "Linear HSTU", "生成式打分"),
    "tubifm": ("以统一 user story 序列描述跨页面旅程，同一个生成式 foundation model 通过任务提示完成 item、carousel 与 search 三种排序。", "s(i|h,\\tau)=\\log p_\\theta([ITEM=i]|\\operatorname{serialize}(h,\\tau))", "跨表面 User Story", "统一生成模型", "三任务排序"),
    "pearl-percentile": ("用多次对比而不是单个偏置标签估计行为 percentile，并按价值加权、bootstrap 和长期共训练扩展到多个排序目标。", "\\hat p_i=\\frac1N\\sum_{j=1}^{N}\\mathbf1[y_i>y_j],\\quad Var(\\hat p)=p(1-p)/N", "多样本对比", "无偏 Percentile", "多目标排序"),
    "dadf": ("冻结成熟的第一阶段 watch-time 模型，按条件分布学习乘性残差校正，并保持线上标量接口不变。", "\\hat y=\\hat y_0\\,b_\\phi(x,\\hat y_0),\\quad b^*=y/\\max(\\hat y_0,\\epsilon)", "冻结基模型", "分布感知残差", "乘性校正"),
}


def fmt(value: float) -> str:
    return f"{value:+.2f}%"


def main() -> None:
    for key, row in ENTRIES.items():
        result = get_adapter(key).run(ROOT / "data", 42)
        directory = DOCS / f"{row.arxiv_id}-{key}"
        metrics = directory / "metrics"
        metrics.mkdir(parents=True, exist_ok=True)
        (metrics / "public-seed42.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        summary, formula, left, middle, right = METHODS[key]
        code = row.code_url
        upstream = (
            f"是：[{code.rsplit('/', 1)[-1]}]({code})"
            if code else f"否：原文未提供官方/作者代码（核查日期：{CHECKED}）"
        )
        local = key.replace("-", "_")
        base, method = result["baseline"], result["method"]
        ndcg = result["relative"]["ndcg_at_10_percent"]
        online = row.metric + " " + fmt(row.lift)
        page = f"""# {row.title}

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

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

原文的主要线上证据为 **{online}**（{row.traffic}）。论文离线表与线上指标使用私有或论文指定口径，不能与下面的 MovieLens 数字直接比较。

## 本地复现

> **本地对照口径**：基线为共享 transition + content scorer；实验组在相同用户、物品、全库候选和 seed 上只加入 `{key}` 核心机制，相对 NDCG@10 {fmt(ndcg)}。

MovieLens-100K、{result['dataset']['users']} users / {result['dataset']['items']} items、seed 42：NDCG@10 {base['ndcg_at_10']:.4f} → **{method['ndcg_at_10']:.4f}（{fmt(ndcg)}）**，Hit@10 {base['hit_at_10']:.4f} → {method['hit_at_10']:.4f}。验证集只用于选择机制混合权重，测试集没有参与调参。

```bash
auto-research reproduce --paper {key} --dataset-dir data --seed 42
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

{result['scope']} 本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 `omitted_core_components`，本地相对变化不得与原文 A/B 提升混写。
"""
        (directory / "README.md").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()

