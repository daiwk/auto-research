#!/usr/bin/env python3
"""Generate complete, mechanism-specific documentation for the 2026-08 P0/P1 batch."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METRICS = json.loads((ROOT / "docs/experiments/p0-p1-closed-audit-20260808-seed42.json").read_text())

POST = [
    dict(id="2607.17247", key="distilled-rl", title="Distilled RL：把教师监督变成细粒度 RL 信号",
         paper_title="Distilled Reinforcement Learning for LLM Post-training", date="2026-07-19",
         org="Chen Wang 等（按一作归档）", code="[已开源：597358816/Distilled-RL](https://github.com/597358816/Distilled-RL)",
         background="传统 RL 只有序列级奖励，OPD 又会无条件模仿教师。Distilled RL 把教师/学生反向概率比作为 token 级奖励重权重，只在正优势样本上启用教师，并以序列几何均值消除长度尺度偏差。",
         formula=r"\rho_t=\pi_T(y_t|y_{<t})/\pi_{old}(y_t|y_{<t}),\quad \tilde\rho_t=\operatorname{clip}(\rho_t)/\exp(\frac1T\sum_s\log\operatorname{clip}(\rho_s)),\quad w_t=\mathbf1[A>0]\tilde\rho_t+\mathbf1[A\le0].",
         paper_result="三种学生模型的平均 Pass@1 均超过 RL、OPD 与 OPD+RL；例如 Qwen3-4B 为 58.96，RL 为 57.40。无生产 A/B。",
         local="实现反向比率裁剪、负样本 reset 与序列几何归一化；教师不是无条件 KL target。"),
    dict(id="2608.06296", key="u-opsd", title="U-OPSD：完全无外部监督的 on-policy 自蒸馏",
         paper_title="On-Policy Self-Distillation without Any Supervision", date="2026-08-06",
         org="Yijiang Li 等（按一作归档）", code="未发现/未发布官方代码（核查日期：2026-08-08）",
         background="U-OPSD 不使用答案、环境奖励或更大教师。模型多次采样后做多数投票，以最短一致解作为 privileged view，定点修复最长且高置信错误轨迹，是真正依赖内部一致性的自蒸馏。",
         formula=r"\hat y=\operatorname{mode}\{y^{(k)}\}_{k=1}^K,\quad c=K^{-1}\sum_k\mathbf1[y^{(k)}=\hat y],\quad \mathcal L=\mathbf1[c\ge\tau]\operatorname{KL}(\pi(\cdot|x,\hat y)\Vert\pi(\cdot|x)).",
         paper_result="Qwen3 非 thinking 4B/8B 相对 base 平均提升 8.5/10.7 个点，并平均超过 OPSD 3.2/2.3 个点。无生产 A/B。",
         local="实现多 rollout 自一致投票、置信门控与无 gold 伪教师；公开算术 mini-suite 上该无监督假设并不成立，因此如实记录退化结果。"),
    dict(id="2608.06347", key="rp-opsd", title="RP-OPSD：围绕推理枢纽做多语种能力迁移",
         paper_title="RP-OPSD: Reasoning-Pivot-Guided On-Policy Self-Distillation for Multilingual Reasoning Transfer", date="2026-08-06",
         org="Nanjing University / Xinye Wang", code="[已开源：NJUNLP/RP-OPSD](https://github.com/NJUNLP/RP-OPSD)",
         background="跨语言迁移中，表面措辞与真正改变推理状态的 pivot 不应同权。RP-OPSD 比较带英文参考解与去掉参考解的匹配教师视图，用分布位移定位 pivot，再在这些位置强化 privileged distillation 并保留 reference anchor。",
         formula=r"g_t=\operatorname{norm}(|\log\pi_T(\cdot|r)-\log\pi_T(\cdot|\varnothing)|),\quad q_t=(1-g_t)\pi_S+g_t\pi_T^r,\quad \mathcal L=\sum_t\operatorname{CE}(q_t,\pi_S).",
         paper_result="覆盖 17 种语言和多难度数学基准，整体超过强多语推理基线与 OPSD 变体；论文无生产 A/B。",
         local="实现 reference-conditioned / ablated 双视图、pivot gate 与 reference anchor。"),
    dict(id="2608.01837", key="pcsd", title="PCSD：用持续一致性过滤局部教师噪声",
         paper_title="PCSD: Persistent Consistency for Self-Distillation in Agentic Reinforcement Learning", date="2026-08-03",
         org="Chunji Lv 等（按一作归档）", code="未发现/未发布官方代码（核查日期：2026-08-08）",
         background="单 token teacher gap 容易受噪声影响，整步共享权重又会抹掉位置差异。PCSD 在自适应窗口内指数累积 teacher-favoring signal，并对下降趋势衰减，最后用连续 sigmoid gate 与 GRPO 联合训练。",
         formula=r"s_t=\log\pi_T(y_t)-\log\pi_S(y_t),\quad p_t=\beta p_{t-1}+(1-\beta)s_t,\quad g_t=\sigma(p_t\,m_t),\quad \mathcal L=\mathcal L_{GRPO}+\lambda\sum_tg_t\mathcal L_{OPSD,t}.",
         paper_result="ALFWorld 两个 backbone 分别超过 GRPO 15.6/13.3 点，超过 SDAR 6.2/5.5 点；无生产 A/B。",
         local="实现指数持续证据、趋势衰减与连续门控，候选位置作为 token 位置代理。"),
    dict(id="2608.03223", key="adrs", title="ADRS：回报相关的自蒸馏奖励塑形",
         paper_title="Agentic Reinforcement Learning with Self-Distilled Reward Shaping", date="2026-08-04",
         org="Ranxu Zhang 等（按一作归档）", code="[已开源：gitrxh/ADRS-arxiv](https://github.com/gitrxh/ADRS-arxiv)",
         background="privileged teacher 的高置信并不必然与真实任务回报一致。ADRS 在每个交互 step 内标准化教师分数，以教师置信与 realized return 的相关性形成 TVA gate，再把 gated token signal 写入原生 reward-to-advantage 路径，推理时无需技能。",
         formula=r"z_{i,t}=(s_{i,t}-\mu_t)/(\sigma_t+\epsilon),\quad g_t=[\operatorname{corr}(z_{\cdot,t},R)]_+,\quad A'_{i,t}=A_i+\lambda g_tz_{i,t}.",
         paper_result="三个交互基准、多个 RL backbone、低数据和未见任务上均持续提升；摘要未给统一单值，且无生产 A/B。",
         local="实现 step 内中心化、return association、TVA gate 与原生 REINFORCE advantage 注入。"),
    dict(id="2606.30406", key="mopd", title="MOPD：多领域教师的 on-policy 能力整合",
         paper_title="MOPD: Multi-Teacher On-Policy Distillation for Capability Integration in LLM Post-Training", date="2026-06-29",
         org="Xiaomi / Wenhan Ma", code="未发现/未发布官方代码（核查日期：2026-08-08）",
         background="多能力联合 RL 会产生域间耦合，参数合并和离策略微调又容易丢能力。MOPD 先独立训练各域 RL teacher，再只在 student 自己的 rollout 上组合教师密集信号，使各域可并行演进。",
         formula=r"q(y_t|x)=\sum_d\alpha_d(x)\pi_{T_d}(y_t|x,y_{<t}),\quad \mathcal L=\mathbb E_{y\sim\pi_S}\sum_t\operatorname{CE}(q_t,\pi_S^t).",
         paper_result="Qwen3-30B-A3B 上超过 Mix-RL、Cascade RL、Off-Policy FT 与参数合并，并已用于 MiMo-V2-Flash 后训练；论文未给生产 A/B。",
         local="实现四个奖励轴的 domain teacher、按样本域证据混合，并限制在 student rollout support。"),
    dict(id="2606.06712", key="opd-lm", title="OPDLM：从自回归模型高效迁移到扩散语言模型",
         paper_title="Data-Efficient Autoregressive-to-Diffusion Language Models via On-Policy Distillation", date="2026-06-04",
         org="Texas A&M University / Xingyu Su", code="未发现/未发布官方代码（核查日期：2026-08-08）",
         background="ARLM 改成双向注意力后既会遗忘原知识，也有随机 mask 训练与 confidence decoding 推理之间的偏移。OPDLM 让双向学生在自身推理轨迹上生成，冻结 AR 教师在同一轨迹给 target logits。",
         formula=r"y^{(k)}\sim\pi_{DLM}^{(k)},\quad \mathcal L_{OPD}=\mathbb E_{y^{(k)}}\sum_{t\in M_k}\operatorname{KL}(\pi_{AR}(\cdot|y_{<t})\Vert\pi_{DLM}(\cdot|y_{\setminus M_k})).",
         paper_result="达到强性能所需训练 token 比既有 DLM 转换方法少 15× 到 7,000×；无生产 A/B。",
         local="用相邻候选状态模拟双向去噪视图，保留冻结 AR teacher anchor；不冒充完整 diffusion decoder。"),
]

AGENT = [
    dict(id="2608.05987", key="agent-opsd", title="AgentOPSD：递归贝叶斯关键 turn 信用分配",
         paper_title="AgentOPSD: Recursive Self-Distillation for Agentic Reinforcement Learning", date="2026-08-06", org="Zi-Han Wang 等（按一作归档）",
         code="[仓库已公开：ZethWang/AgentOPSD；README 标注完整代码待发布](https://github.com/ZethWang/AgentOPSD)",
         background="轨迹奖励难定位少数关键决策。AgentOPSD 把 privileged replay 的 token teacher/student log-prob gap 聚合成 turn evidence，再在 log-odds 空间递归更新成功信念，以相邻信念修订量识别 pivotal turn。",
         formula=r"e_t=\sum_{j\in turn_t}(\log\pi_T(y_j)-\log\pi_S(y_j)),\quad \ell_t=\ell_{t-1}+e_t,\quad c_t=\sigma(\ell_t)-\sigma(\ell_{t-1}).",
         paper_result="Qwen2.5-7B 在 ALFWorld 达到 89.1% success，并超过 GRPO 与自蒸馏基线；无生产 A/B。",
         local="实现逐 turn evidence、递归 log-odds belief、pivotal revision 和 critic-free policy update。"),
    dict(id="2608.04788", key="ocsd", title="OCSD：消除 replay scaffold 混杂的观测校准蒸馏",
         paper_title="Agentic Reinforcement Learning with Observation-Calibrated Self-Distillation", date="2026-08-05", org="Yi Yang 等（按一作归档）",
         code="[已开源：yiy1x/OCSD](https://github.com/yiy1x/OCSD)",
         background="直接重放未来 observation 时，token 分数变化同时来自观测信息和重放脚手架。OCSD 构造结构完全匹配的 Full 与 Observation-Ablated 两个 replay，仅以二者残差调制高不确定 step 的 GRPO 更新。",
         formula=r"r_t=(\log\pi_{full}(y_t)-\log\pi_S(y_t))-(\log\pi_{abl}(y_t)-\log\pi_S(y_t)),\quad A'_{t}=A_{traj}(1+\lambda u_tr_t).",
         paper_result="在 ALFWorld、WebShop、Search-QA 和三个 Qwen3 规模上稳定超过强基线；摘要未给统一单值，无生产 A/B。",
         local="执行 full/observation-ablated matched replay、residual calibration 和 turn-level credit。"),
    dict(id="2608.03137", key="vermem", title="VerMem：带局部和全局验证器的统一记忆管理",
         paper_title="Verifiable Memory: Learning Unified Memory Management with Local and Global Verifiers for Large Language Model Agents", date="2026-08-04", org="Sun Yat-sen University / Xiaolong Sun",
         code="[已开源：Sun-SYSU-24/VerMem](https://github.com/Sun-SYSU-24/VerMem)",
         background="长期记忆、活动上下文与 episodic history 往往分开优化，轨迹奖励无法判断单次记忆操作是否正确。VerMem 用一个策略管理三类状态和七种原子操作，以 local verifier 审核状态转移、global verifier 审核证据一致性。",
         formula=r"R=R_{task}+\lambda_lV_{local}(m_t,a_t,m_{t+1})+\lambda_gV_{global}(M_T,\tau)-\lambda_cC(a_t),\quad \max_\pi\mathbb E_\pi[R].",
         paper_result="五个 benchmark、两个 backbone 上在绝大多数指标最好；受控 online-token budget 下给出最优效率—性能前沿。无生产 A/B。",
         local="显式维护 LTM、active context、episodes，执行 retrieve/add/restore，并分别计数 local/global verifier。"),
    dict(id="2608.01739", key="coevo-mem", title="CoEvo-Mem：检索路由与记忆库交替共进化",
         paper_title="CoEvo-Mem: Co-Evolving Retrieval Policy and Memory Bank for LLM Agents", date="2026-08-03", org="Bowen Ye 等（按一作归档）",
         code="未发现/未发布官方代码（核查日期：2026-08-08）",
         background="只优化 query routing 或只更新 memory bank 会忽略二者反馈环。CoEvo-Mem 让冻结 LLM 生成 route-specific rewrite 和 prior，轻量 residual router 在线修正；任务结果更新路由，轨迹反馈更新 memory value 与 graph relation，并交替冻结一侧控制非平稳性。",
         formula=r"q'=q_{LLM}+\Delta_\phi(q),\quad \phi\leftarrow\arg\max J(\phi;M\ \mathrm{fixed}),\quad M\leftarrow\operatorname{Update}(M;\tau,\phi\ \mathrm{fixed}).",
         paper_result="七个多样 benchmark 上达到 SOTA，验证 retrieval-memory co-evolution；无生产 A/B。",
         local="实现 route rewrite、残差路由与 router/memory bank 交替更新；检索键包含任务轴和工具签名，防止跨任务误复用。"),
]


def diagram(label: str) -> str:
    return f'''```mermaid
flowchart LR
 A["学生 / Agent rollout"] --> B["{label}"]
 B --> C["可审计的目标或状态更新"]
 C --> D["公共 mini-suite 评测"]
```'''


def research_page(item: dict, module: str) -> str:
    result = METRICS["post_training" if module == "post-training" else "agent"][item["key"]]
    if module == "post-training":
        before, after = result["baseline"]["accuracy"], result["final"]["accuracy"]
        delta = (after / before - 1) * 100
        local_result = f"Arithmetic candidate suite、120 steps、seed 42：accuracy {before:.4f} → **{after:.4f}（{delta:+.2f}%）**。诊断字段完整记录在固定指标文件中。"
        command = f'auto-research post-train --algorithm {item["key"]} --dataset arithmetic-smoke --maximum-examples 256 --steps 120 --seed 42'
        code_dir = "src/auto_research/post_training/"
        label = "训练目标与教师视图"
    else:
        metrics = result["metrics"]
        local_result = f'PlanBench mini-suite、120 episodes、seed 42：joint success **{metrics["joint_success"]:.4f}**，average cost {metrics["average_cost"]:.4f}；论文特有操作均有非零 telemetry。'
        command = f'auto-research agent-eval --method {item["key"]} --benchmark planbench-mini --episodes 120 --seed 42'
        code_dir = "src/auto_research/agent_research/"
        label = "论文特有规划 / 记忆算子"
    return f'''# {item["title"]}

> **Fidelity：核心机制复现**。本页把原论文结论、本地机制验证和未复刻部分分开陈述。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [{item["paper_title"]}（arXiv {item["id"]}）](https://arxiv.org/abs/{item["id"]}) |
| 公司 / 机构 | {item["org"]} |
| 首次公开日期 | {item["date"]}（arXiv v1） |
| 原作者代码 | {item["code"]} |
| 本地 adapter / 方法键 | `{item["key"]}` |
| 本地复现代码 | [`{code_dir}`](https://github.com/daiwk/auto-research/tree/main/{code_dir}) |

## 原始论文总结

### 背景与主要改动

{item["background"]}

{diagram(label)}

### 核心公式

$$
{item["formula"]}
$$

### 论文离线与线上效果

{item["paper_result"]}

## 本地复现

{item["local"]}

{local_result}

```bash
{command}
auto-research evolve --model {"post-training" if module == "post-training" else "agent"} --dataset {"arithmetic-smoke" if module == "post-training" else "planbench-mini"} --direction "组合 {item["key"]} 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`../../experiments/p0-p1-closed-audit-20260808-seed42.json`](../../experiments/p0-p1-closed-audit-20260808-seed42.json)。

## 复现边界

本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。
'''


def reproduction_page(item: dict) -> str:
    slug = f'{item["id"]}-{item["key"]}'
    data = json.loads((ROOT / "docs/reproductions" / slug / "metrics/public-seed42.json").read_text())
    base, method = data["baseline"], data["method"]
    if item["key"] == "open-language-model":
        local = f'WikiText-2、30 steps、seed 42：同预算 LLaMA-modern PPL {base["perplexity"]:.2f}，OLM composable {method["perplexity"]:.2f}；两者参数量均为 {method["parameters"]}。此实验验证组合 DSL 不改变执行语义，不把近零差异宣称为效果提升。'
        comparison = f'基线为同预算 LLaMA-modern，实验组为 `olm_composable`；相对 PPL {data["relative"]["perplexity_percent"]:+.6f}%。'
    else:
        local = f'MovieLens-100K、260 users / 420 items、seed 42：NDCG@10 {base["ndcg_at_10"]:.4f} → **{method["ndcg_at_10"]:.4f}（{data["relative"]["ndcg_at_10_percent"]:+.2f}%）**；线上数值仅引用原文。'
        comparison = f'基线为共享 transition + content scorer，实验组只加入 {item["key"]} 核心机制；相对 NDCG@10 {data["relative"]["ndcg_at_10_percent"]:+.2f}%。'
    return f'''# {item["title"]}

> **Fidelity：核心机制复现**。公开数据只验证论文机制，不模拟生产流量。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv {item["id"]}](https://arxiv.org/abs/{item["id"]}) |
| 公司/机构 | {item["org"]} |
| 首次公开日期 | {item["date"]}（arXiv v1） |
| 原文开源代码 | {item["code"]} |
| Adapter | `{item["key"]}` |
| 本地复现代码 | [`src/auto_research/reproductions/{item["code_package"]}/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/{item["code_package"]}/) |

## 原始论文总结

### 背景与主要改动

{item["background"]}

{diagram(item["diagram"])}

### 核心公式

$$
{item["formula"]}
$$

### 论文离线与线上效果

{item["paper_result"]}

## 本地复现

> **本地对照口径**：{comparison}

{item["local"]}

{local}

```bash
auto-research reproduce --paper {item["key"]} --dataset-dir data --seed 42
auto-research evolve --model {"micro-llm" if item["key"] == "open-language-model" else "rankmixer"} --dataset {"wikitext-2" if item["key"] == "open-language-model" else "movielens-100k"} --direction "探索 {item["key"]} 的已安装核心算子" --generations 2 --population 4
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

{item["boundary"]}
'''


REPRO = [
    dict(id="2608.02148", key="dme", code_package="dme", title="DME：兼顾大规模召回与细粒度语义的抖音多模态向量模型", paper_title="Douyin Multimodal Embedding Model Technical Report", date="2026-08-03", org="ByteDance / Douyin", code="否：未发现/未发布官方代码（核查日期：2026-08-08）",
         background="对比学习向量服务高效但监督过粗，显式 CoT 又无法在线服务。DME 先做大规模多模态对比预训练，再以 Evidence-Grounded Typed Latent Reasoning 整理检索证据，并用 Cross-Conditional Reconstruction 保留对侧细粒度语义；两个生成头只在训练期使用。",
         diagram="对比预训练 → typed latent evidence → 双向重建", formula=r"z_q=E_q(q),\ z_d=E_d(d),\quad \mathcal L=\mathcal L_{contrast}+\lambda_r\mathcal L_{typed\ latent}+\lambda_c[\mathcal L(d|z_q)+\mathcal L(q|z_d)].",
         paper_result="MMEB-v2 上 2B/9B 为 74.8/78.4；抖音内部离线相对 +2.92%，搜索线上 A/B Lifetime +0.1%，且已部署于生成、图搜和 AI 搜索。",
         local="执行 typed latent evidence、双向 ridge reconstruction training head 和零 serving generation head。", boundary="未复刻 2B/9B 多模态 backbone、抖音私有语料和十亿级向量索引。"),
    dict(id="2608.01949", key="steps", code_package="steps", title="STEPS：全量部署的自触发 Agentic Push 推荐", paper_title="A Self-Triggered Agentic Push Recommendation System", date="2026-08-03", org="ByteDance / Douyin", code="否：未发现/未发布官方代码（核查日期：2026-08-08）",
         background="固定频控无法实时调整，周期轮询又在成本与时机间冲突。STEPS 把“是否推送”和“何时再次唤醒”合成闭环：planning agent 用 gated ordinal regression 规划间隔，execution agent 用轨迹回报决定发送，轻量 filter agent 控制算力并拦截异常计划。",
         diagram="规划唤醒间隔 → 执行推送 → 过滤保护 → 再次自触发", formula=r"p(k|s)=\sigma(b_k-f_\theta(s))-\sigma(b_{k-1}-f_\theta(s)),\quad a_t=\arg\max_aQ_\phi(s_t,a),\quad \tilde a_t=a_t\mathbf1[g(s_t)>\tau].",
         paper_result="已全量部署于 10 亿+用户的抖音；线上 active days +0.2843%，push permission disablement -1.9089%，filter 降计算开销 79.42%。",
         local="执行 ordinal interval、trajectory utility、filter safeguard 和闭环自触发得分。", boundary="MovieLens 没有真实 push permission、触达成本和 wall-clock 唤醒器，只验证决策分解。"),
    dict(id="2608.01738", key="spear", code_package="spear", title="SPEAR：选择感知的个性化改写与社区搜索", paper_title="SPEAR: Selection-aware Personalized End-to-end Adaptive Rewriting and Retrieval for Community Search", date="2026-08-03", org="Dewu / Wenbin Wu", code="是：[mallocagi1-cell/spear](https://github.com/mallocagi1-cell/spear)",
         background="端到端改写—检索容易让通用词凭高 path score 胜出、偏离原 query。SPEAR 用双 embedding 和梯度隔离保护 recall 语义，以 rewrite confidence × item relevance 的乘法门消除捷径，再由动态 selector 产生 request-specific 权重、scale 和 bias。",
         diagram="原 query / 用户画像 → 双 embedding → 乘法门 → 动态 selector", formula=r"s(q',d)=s_{orig}(q,d)+\underbrace{c(q'|q,u)\cdot r(q',d)}_{\text{selection-aware gate}},\quad \hat s=\gamma(q,u)s+\beta(q,u).",
         paper_result="10 万工业 session 上 semantic similarity@10 +18.2、click recall@10 +99.5；线上 query-view CTR +0.259、平均阅读深度 +0.733，2025 年起全量部署于得物社区搜索。",
         local="执行 recall/rank 双 embedding、乘法 confidence×fidelity gate、dynamic scale 和原 query residual。", boundary="MovieLens item 内容代理商品/帖子，未复刻得物 query rewrite generator、私有 session 与线上排序链路。"),
    dict(id="2607.16669", key="open-language-model", code_package="open_language_model", title="OpenLanguageModel：面向教学与研究的可读可组合小模型预训练", paper_title="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research", date="2026-07-18", org="Indian Institute of Technology Madras", code="是：[openlanguagemodel/openlanguagemodel](https://github.com/openlanguagemodel/openlanguagemodel)",
         background="许多预训练框架把模型结构、训练循环和分布式运行强耦合，难以做透明消融。OLM 让组件保持普通 PyTorch module，用 Block、Residual、Repeat、Parallel 描述布线，同一模型可从 notebook 迁移到 CPU、单 GPU 和单机多 GPU。",
         diagram="普通 module → Block / Residual / Repeat / Parallel → AutoTrainer", formula=r"h_{l+1}=\operatorname{Block}_l(h_l),\quad \operatorname{Residual}(f)(x)=x+f(x),\quad \operatorname{Parallel}(f,g)(x)=f(x)+g(x).",
         paper_result="提供 9 个模型家族的 27 个 preset；348M 参数四卡 weak-scaling efficiency 90.6%，并与独立参考实现高度一致。无生产 A/B。",
         local="新增 `olm_composable` genome，暴露普通 module、四种组合 operator 和 cpu/mps/cuda portability，并纳入实时论文检索后的 evolve 候选。", boundary="未搬运上游整个包和 27 个 preset，也未复刻 348M 四卡实验；本地验证结构语义和统一 evaluator 接口。"),
]


def main() -> None:
    for item in POST:
        path = ROOT / "docs/post-training" / f'{item["id"]}-{item["key"]}' / "README.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(research_page(item, "post-training"), encoding="utf-8")
    for item in AGENT:
        path = ROOT / "docs/agent-research" / f'{item["id"]}-{item["key"]}' / "README.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(research_page(item, "agent-research"), encoding="utf-8")
    for item in REPRO:
        path = ROOT / "docs/reproductions" / f'{item["id"]}-{item["key"]}' / "README.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(reproduction_page(item), encoding="utf-8")


if __name__ == "__main__":
    main()
