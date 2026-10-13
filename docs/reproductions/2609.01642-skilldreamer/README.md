# SkillDreamer：行动前想清楚需要什么能力

> 本轮阅读与实现的是 v2 实质修订；v1 首发在 2026-08-28，**不计作 2026-10 新 v1**。本地保留真实模型 PSG/HSR/CSI，但算术环境只是 live-interaction diagnostic，不冒充 SkillUsage/SkillNet-Gym 能力复现。

## 论文信息

| 项目 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2609.01642](https://arxiv.org/abs/2609.01642) |
| 公司/机构 | Sichuan University |
| 首次公开日期 | 2026-08-28（arXiv v1） |
| 原文开源代码 | 否：原文与官方页面未找到作者实现仓库（核查日期 2026-10-13） |
| Adapter | `skilldreamer` |
| 本地复现代码 | [`src/auto_research/reproductions/skilldreamer/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/skilldreamer/) |

原始 v1 时间为 2026-08-28 13:19:50 UTC；v2 为 2026-10-09 04:15:57 UTC。正文题名为 *Imagine Before Acting: Prospective Skill Identification for LLM Agents*；SkillDreamer 是方法名。

## 原始论文总结

### 背景与主要改动

任务描述主要说目标，技能文档主要写程序性知识。直接相似度容易优先找到背景相近、但不能解决当前能力缺口的技能；检索到了也未必会在执行时调用。SkillDreamer 在检索和调用两侧显式表达能力需求。

PSG 先由 LLM 从任务推断 1–5 个独立 capability 和语义 anchors，再为每个 capability 生成 procedure-like pseudo skill。pseudo skill 只是检索代理，并非验证过的可执行技能。HSR 融合原任务与各 pseudo 的 dense relevance，再以 anchors 的 BM25 做 candidate 内 min-max reranking。各 capability 的排名矩阵逐行轮询、去重，避免一种能力占满候选。

CSI 在下一动作前重新检查当前 subgoal、证据与未解决限制，说明所需 capability、匹配或不匹配与下一有界动作。MATCH/PARTIAL_MATCH 时先加载真实候选技能，再决定行动；每五个已执行动作插入运行时检查，失败或新证据也触发重评。能力检查不能从已选工具反向编造，也不能把“加载过”当作“做成功”。

### 架构流程

```mermaid
graph LR
 Q[只有用户任务] --> C[LLM推断capabilities与anchors]
 C --> P[LLM生成pseudo skills]
 Q --> H[HSR task与pseudo dense融合]
 P --> H
 C --> B[anchors BM25 rerank]
 H --> B
 B --> R[capability roundrobin候选]
 R --> S[CSI每动作能力重评]
 E[真实环境观察与失败] --> S
 S --> L[加载真实gallery技能]
 L --> A[再生成并执行工具动作]
 A --> E
```

上方为本地重绘示意，源码：[architecture.mmd](assets/architecture.mmd)；来源版本与边界见 [source-provenance.json](assets/source-provenance.json)。

<!-- paper-figure:start -->
### 原论文关键图

[![SkillDreamer：行动前想清楚需要什么能力 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/2609.01642v2#page=3)

图 2：PSG 先推断 required capability 与 semantic anchor，再生成仅用于检索的 pseudo skill；HSR 同时使用原任务与伪技能，召回真实 skill gallery 的候选；执行时 CSI 按当前子任务重评能力，并按需调用真实技能。右侧周期检查沿执行轨迹进行，不是读取 gold plan。来源：Liu 等，[v2 Figure 2](https://arxiv.org/html/2609.01642v2#S2.F2)，[原 PDF 第 3 页](https://arxiv.org/pdf/2609.01642v2#page=3)。

此图为固定 v2 原文 PDF 的 250 dpi 局部截图，图内文字未改写，已视觉核验；不是本地测量，也不将 v2 更新算作 10 月新 v1。论文标注 arXiv perpetual non-exclusive license，并非 CC BY；图示版权仍归原作者。PDF/图片 SHA256、页码与裁切范围见 [original-figures.json](assets/original-figures.json)。

> **原论文 Figure 2（关键图）**：上文说明所选原图或方法截图的范围；并非本地测量。图片来自[原论文](https://arxiv.org/pdf/2609.01642v2#page=3)，版权归原作者所有；点击图片可查看固定版本来源。
<!-- paper-figure:end -->

### 核心公式

对 task dense score $r_i^q$、pseudo $j$ 的 dense score $r_{ij}^p$：

$$
d_{ij}=2r_i^q+r_{ij}^p.
$$

各 pseudo 先选 $K_c=20$ 候选，再在该集合对三项 min-max 标准化：

$$
h_{ij}=2\bar r_i^q+\bar r_{ij}^p+\overline{BM25(anchor,s_i)}.
$$

逐排名行扫描各 capability 的 top-$K_r$，去重收集 $K$ 技能。CSI 的 periodic context 在 $n\bmod5=0$ 时注入；$n$ 是实际执行动作，不是模型思考次数。

### 论文离线与线上效果

| 原文指标 | Direct/Original | SkillDreamer |
| --- | --- | --- |
| Qwen-0.6B SkillUsage R@5 | 52.68% | 60.42% |
| Qwen-0.6B SkillRet R@5 | 59.14% | 66.93% |
| GPT-5.5 SkillUsage Pass / Load | 48.1 / 92.9 | 50.6 / 96.4 |
| DeepSeek-V4-Flash SkillUsage Pass / Load | 37.1 / 51.2 | 41.4 / 77.4 |
| Qwen3.6-27B 统一SkillUsage Pass | 31.3% | 37.6%，Load均59.5% |

来源：[原文 §3 与附录 D](https://arxiv.org/html/2609.01642v2#S3)。原 benchmark 有 6660/约3.4万技能、SkillUsage 84 个有效执行任务；原结果并非本地再测。pseudo 直接交给 agent 反而降低 Pass，是“想象的 procedure 不是已验证技能”的重要负结果。未报告生产线上 A/B。

## 本地复现

> **本地对照口径**：基线为同模型 no-skills 与原任务 dense direct retrieval，实验组为真实 PSG/HSR/CSI；缩放算术交互对原 benchmark 的相对能力结论不适用。

```bash
PYTHONPATH=src python scripts/run_skilldreamer.py \
  --config /path/to/skilldreamer.json --seed 42 --output runs/skilldreamer/seed42.json
```

配置含已验证本地 Instruct `model_dir`、MiniLM `encoder_dir`、带 provenance 的公开 `raw_data`、`device` 和提前固定 `max_queries`、`top_k`、`action_budget`、`max_new_tokens`。模型真实生成 capability/anchors 与 pseudo，HSR 实际编码/BM25/rerank；没有固定 candidate 代替 LLM generation，PSG 无效也不启发式补造。CSI 加载 `gallery.json` 的实际 procedure 后，必须再生成一条 action，才能使用该技能的内容。

### 数据协议、结果与边界

以公开 GSM8K-style question/answer JSONL 中的 question 为任务，参考答案在独立 external scorer 中按数字比较；模型和环境观察均不接收 gold answer、gold plan 或 gold skill。首N条在读取 relevance 之外预先固定，按固定 hash 分离 validation/test，当前超参数事先固定不看 test 改写。五条本地通用技能为算术验证、比例、库存、金额和时间处理，不含题目答案。

环境复用已审查的 `ArithmeticEnvironment`，真实运行有界 AST calculator，只接受数字和允许的算术运算，不执行模型生成 Python、不访问外部系统。记录 actual executed actions、skill loads、生成失败、提交答案和外部 Pass；PSG/schema 失败计零 reward，不删除失败任务。不因 Load 高就宣称策略更强。

本轮未运行原 SkillUsage/SkillRet/SkillNet-Gym，没有原规模技能库、原模型或编码器；本地为 `core_mechanism` 的 live-interaction diagnostic，固定 `diagnostic_only=true`、`promotion_eligible=false`。合同证据见 [implementation-contract.json](metrics/implementation-contract.json)，真实模型 GPU 三 seed 指标和 receipt 必须来自实际运行。本文不把单测 fixture 当作模型能力结果。

### 代码映射

`algorithm.py` 对应 PSG 双阶段、HSR公式/roundrobin、CSI周期检查与技能加载；`experiment.py` 加载真实 checkpoint、执行三方法并独立评分；`gallery.json` 是通用 procedure 集而非训练/测试 gold plan；`paper.yaml` 显式列出未运行的原 benchmark，Evolve operators 为空。

测试：`python -m pytest tests/reproductions/test_oct13_agents_jepa.py`，验证不能读取 gold、pseudo 不进入执行、gallery body 必须先加载后再行动、真实 calculator 输出回到下一次能力评估。
