# SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [arXiv 2610.13157](https://arxiv.org/abs/2610.13157) |
| 公司/机构 | Microsoft / Zhejiang University |
| 首次公开日期 | 2026-10-09（arXiv v1） |
| 原文开源代码 | 否：原文与关联原始来源未找到本方法已发布源码（2026-10-13核验）；不是宣称全网不存在 |
| Adapter | `soar` |
| 本地复现代码 | [`src/auto_research/reproductions/soar/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/soar/) |
| 实现/评测层级 | 核心算法实际模型路径；L0/L1机制诊断，不是原benchmark完整复现 |
| GPU门禁 | 必须真实A100/A30执行并提交绑定源码的脱敏回执；未取得者仍未验收 |

## 原始论文总结

### 背景与主要改动

只按答案奖训练的search agent可能答对却伪造证据依赖。SOAR独立记录atomic query的internal recall和external retrieval，再要求显式声明source。internal recall不接收旧reasoning或external evidence；来源一致性、正确性与格式reward训练真实策略。

### 架构与数据流

以下为本地重绘，不冒充原论文图片。

```mermaid
flowchart TD
  Q[policy产生atomic search query] --> I[隔离上下文内部recall]
  Q --> X[独立公开文本检索]
  I --> O[显式双stream观察]
  X --> O
  O --> A[policy声明source并回答]
  A --> V[正确性格式来源一致性reward]
  V --> U[trajectory GRPO及reference KL]
```

<!-- paper-figure:start -->
### 原论文关键图

[![SOAR: Source-Aware Reinforcement Learning with Precise Credit Assignment for Search Agents 原论文 Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2610.13157v1/method.svg)

中文图注（原论文 Figure 2）：上半部展示 Actor 同时访问搜索引擎与内部知识，形成多条 rollout，结合参考模型和来源一致性规则奖励计算组优势并更新策略；下半部展示不同轨迹如何选择与组合内部、外部证据，把奖励归因到信息选择行为。此图为作者原始训练框架，不是本地检索语料或训练结果。

精确来源：[固定 v1 的 Figure 2，HTML `S2.F2`](https://arxiv.org/html/2610.13157v1#S2.F2)；[原始 SVG](https://arxiv.org/html/2610.13157v1/method.svg)。本地原始字节副本与 SHA-256 记录在 [figure-source.json](figure-source.json)，版权归原作者；与上方本地 Mermaid 重绘分开。

> **原论文 Figure 2（关键图）**：上文说明所选原图或方法截图的范围；并非本地测量。图片来自[原论文](https://arxiv.org/html/2610.13157v1/method.svg)，版权归原作者所有；点击图片可查看固定版本来源。
<!-- paper-figure:end -->

### 核心公式

$$
i_{\rm int}\sim\pi_\theta(\cdot\mid P_{\rm elic},q_j),\quad
R=R_{\rm ans}+0.2R_{\rm fmt}+0.1R_{\rm mat}.
$$
$R_{\rm mat}=\mathbf1[\operatorname{Verify}(y,\mathcal E_{C_y})]$，仅检查声明stream，不能靠另一stream中碰巧有答案给奖。Appendix D规定归一化；本地明示总权重归一化，再按trajectory group计算GRPO优势。工具观察/internal recall token不接受策略loss。

### 论文离线与线上效果

原文Qwen2.5-3B/7B、E5-base-v2和2018 Wikipedia，在NQ/HotpotQA train学习、7个QA benchmark评测。主文报告3B平均EM0.414、7B0.448；3B fabrication从16.08%到4.05%。HTML部分表格转换缺失，以4.2/表4正文为出处，不补造全表。未报告生产线上A/B。

选取的原文稳定标量与出处保存于 [paper-results.json](paper-results.json)，全部标为paper-reported，不是本地测量。

## 本地复现

> **本地对照口径**：基线为相同source-aware工作流的without-source-reward消融；另有冻结初始策略；实验组仅支持本页L0/L1机制，稳定相对提升不适用。

### 数据与标签访问协议

公开checkpoint/data必须固定revision并通过既有 `checkpoint_source` / `validate_holdout` 的文件hash验证。本轮SOAR队列使用明确派生的**工具文档属性QA训练诊断**，不在不匹配的WikiText+GSM上宣称知识QA效果。Actor及冻结reference都用Qwen2.5-0.5B-Instruct revision `7ae557604adf67be50417f59c2c2f167def9a775`，SOAR无需装载7B teacher。参考答案只由独立训练奖励/离线scorer读取，agent消息只含问题与真实工具返回的文档，不接收当前题gold/plan。

独立KB来自[固定公开EcoAgent catalog](https://github.com/Elliotes/EcoAgent/blob/bc5db40a20b254c5249401d2220ea71b06c86a5c/data/processed/tools_clean_with_reliability.csv)，revision为 `bc5db40a20b254c5249401d2220ea71b06c86a5c`，原CSV SHA-256为 `1b388d317aeb1004c266eb65ff64a4864e7907412a2fbfb4667c492a871e8d8e`。`scripts/prepare_soar_catalog_qa.py`先封存全部5,172个tool的原始名称、UID、来源、URL、标签和说明（8,394个不超过900字符的连续片段），不使用reliability/quality分数、train_pairs或任何测试标签。之后才按tool UID固定hash分组，生成8条train和4条validation属性问题；两组tool不重叠，查询属性为catalog UID或文档URL。所有问题共享事先封存的完整KB，因此是共享知识库内的检索/来源流诊断，不是未知知识库泛化。

切分清单将source明确标成 `Elliotes/EcoAgent#derived-tool-document-attribute-training-QA-v1`；其中 `source_split=train` 仅表示本地生成的training-QA源池，不冒充EcoAgent官方train split。generator、独立KB、源QA和两分区的SHA-256均保存；不打开 `eval_real_test.jsonl`，不把LongMemEval等官方eval改成训练集。数据与配置已准备不等于GPU训练已完成。

必须有独立public corpus的revision/hash/rows/source URL；documents不得包含benchmark answer/gold字段。policy实际产生search，recall每次只收query，再接双stream观察。按真实trajectory reward做LoRA；without-source-reward另跑。没有corpus或组全零优势必须真实失败。

### 可执行入口与预算

入口为 `scripts/run_oct13_post_training.py --method soar`，adapter则从数据目录读取 `oct13_execution.json`。必须提供student镜像路径及public id/revision、派生train/validation路径、split manifest、dataset revision与独立KB来源。下面是待实跑配置示例，不表示GPU已完成：

```bash
PYTHONPATH=src python scripts/run_oct13_post_training.py \
  --method soar --config data/oct13_execution.json \
  --device cuda --seed 42 --train-examples 8 --group 4 --max-turns 3 --max-tokens 256 --steps 4 --verifier normalized-em --variant source-consistent --corpus-path "$CORPUS" --corpus-id Elliotes/EcoAgent --corpus-revision bc5db40a20b254c5249401d2220ea71b06c86a5c \
  --output runs/oct13/soar-42
```

对照仅将variant改为 `without-source-reward`，重新从同一checkpoint和seed初始化，保持同一数据、4 steps、4轨迹/组、3 turns和256 token响应上限。两臂各最多36,864个生成token（含内部recall与前后评估），这是配置上界，不是已测成本或FLOPs。真实模型必须产生search并读取公开说明；零检索、无有效来源匹配或零优势不得包装成来源选择能力验证。

真实生成、拒绝、难度校准、teacher profiling及监督token预算进入结果；失败写不可覆盖的 `failure.json`，成功写 `result.json` / `report.md`。不能仅以本地目录名伪造source metadata。

### 当前结果与验收状态

[mechanism-contracts.json](metrics/mechanism-contracts.json)保存已CPU执行的公式/行为合同标量，deterministic tensor/fixture协议，`diagnostic_only: true`、`formal_comparison: false`。不替代公开checkpoint训练、GPU回执、同预算能力比较或原benchmark。GPU指标由实际结果核验后另行摘录；本页不声明未执行实验已经完成。

### 2026-10-14 实际失败记录（旧6a源码）

[seed42两奖励臂负结果](metrics/public-a100-failed-seed42-6aabe57a.json)绑定真实A100 `6aabe57a` 与预先独立封存EcoAgent公开catalog KB/属性QA train split，不是官方RATED/SOAR benchmark。source-consistent/without-source-reward各4groups全部zero advantage、0更新，全部answer/format/source_match0，训练实际各1search。每臂policy生成1056tokens+隔离recall34tokens，elapsed34.11/34.01秒；失败不强制优势，不签GPU通过回执。

更大已缓存7B policy的train-only格式探针仅是待批准提案：原序4train×2episodes、最多3turn/cap256、wall300s、0LoRA/0评估；不静默换模型或追加预算，不以test挑方案。现有两臂失败保持，整方法实际非零策略更新与完整多seed计划仍未完成。

### 代码映射

algorithm.py：双stream、EM、真实文本index及reward；checkpoint.py：policy工具循环、隔离recall、trajectory优势/KL/LoRA。`scripts/prepare_soar_catalog_qa.py`：固定catalog白名单KB与tool-group切分；其隔离与哈希回归在 `tests/reproductions/test_soar_catalog_qa.py`。

共享 `post_training/oct13_common.py` 只承担资源装载、成本记录、response likelihood、真实optimizer step和输出；论文机制保留在本目录。行为测试为 `tests/reproductions/test_oct13_post_training.py`；State/GPPO/TAPO还保留既有专属测试。

### 边界与未完成项

小lexical index替代E5/Wikipedia基础设施，不替代source policy/reward。原文未释放EM normalization代码，本地明示词边界匹配；不把它冒充GPT-5.6-Sol fabrication指标。工具文档属性QA不是RATED官方tool-selection test，也不是SOAR七个知识QA benchmark；共享KB下的tool-group隔离不等于未知KB泛化。不能制造来源文本或用参考答案冒充evidence。

仍需适用A100/A30路径及对照实跑、新源码绑定脱敏receipt、全局目录同步与CI。三个seed不会自动升级机制诊断为正式能力证据。本条未注册未经验证的evolve映射。

