# 2026-10-19：定向组件补充与来源差异审计

本批选中 **9篇：7项低成本组件/协议、2篇高成本资料**。其中1篇是 Google 官方目录发现的历史补漏，另8篇来自10月16日公告中的重叠候选；**不是10月19日新发表9篇**。

七项组件已验收：**3项CUDA在单张A100上各执行3个种子，4项CPU也各执行3个种子**（42、43、44）。这只是算子/协议诊断，不是七篇完整实验复现。

审查水位维持 **2026-10-15**，本批不推进水位，`all_sources_exhaustive=false`。选中论文的组件实现、GPU验收和来源覆盖是不同状态；不能用其中一项替代另一项。逐来源收据、SHA256、目录差异处置与九篇固定范围见 [source-coverage.json](source-coverage.json)。

## 本批固定范围

| 优先级 | 论文 / arXiv v1日期 | 本地范围 | 主流程验收 |
| --- | --- | --- | --- |
| P0 | [SKILL.state](../../agent-research/2608.26263-skill-state/README.md)，2026-08-26 | CPU：显式状态、JSON merge patch、只保留最新观察的执行循环 | [CPU三种子产物](../../agent-research/2608.26263-skill-state/metrics/component-cpu-seeds42-44.json)已验收 |
| P1 | [AlphaDiana](../../agent-research/2610.20675-alpha-diana/README.md)，2026-10-14 | CPU：稳定sample、重试/失败计量、共享记忆会话政策 | [CPU三种子产物](../../agent-research/2610.20675-alpha-diana/metrics/component-cpu-seeds42-44.json)已验收 |
| P1 | [AgentPerturb](../../agent-research/2610.21624-agent-perturb/README.md)，2026-10-15 | CPU：单目标扰动、独立验证、配对覆盖率与未知评分边界 | [CPU三种子产物](../../agent-research/2610.21624-agent-perturb/metrics/component-cpu-seeds42-44.json)已验收 |
| P1 | [DIVERGE](../../post-training/2610.22324-diverge-ideation/README.md)，2026-10-15 | CPU：多样性/质量的集合奖励协议 | [CPU三种子产物](../../post-training/2610.22324-diverge-ideation/metrics/component-cpu-seeds42-44.json)已验收 |
| P1 | [FPOT](../../foundation-models/2610.21257-fpot/README.md)，2026-10-15 | CUDA：分数二次幂权重量化算子 | [A100三种子产物](../../foundation-models/2610.21257-fpot/metrics/component-cuda-seeds42-44.json) / [GPU收据](../../gpu-validations/fpot-a100-20261019.json)已验收 |
| P1 | [LAMP](../../foundation-models/2610.22182-lamp/README.md)，2026-10-15 | CUDA：冻结特征上的层间自适应预测混合 | [A100三种子产物](../../foundation-models/2610.22182-lamp/metrics/component-cuda-seeds42-44.json) / [GPU收据](../../gpu-validations/lamp-a100-20261019.json)已验收 |
| P1 | [KnowGPO](../../post-training/2610.22331-knowgpo/README.md)，2026-10-15 | CUDA：知识分组优势/目标算子 | [A100三种子产物](../../post-training/2610.22331-knowgpo/metrics/component-cuda-seeds42-44.json) / [GPU收据](../../gpu-validations/knowgpo-a100-20261019.json)已验收 |
| P1 | [AutoSFT](../../agent-research/2610.22194-auto-sft/README.md)，2026-10-15 | 仅方法与成本资料，无假Adapter | 完整实验成本过高，不复现（审查DONE） |
| P1 | [Gen4P](../../foundation-models/2610.22371-gen4p/README.md)，2026-10-15 | 仅方法与成本资料，无假Adapter | 完整实验成本过高，不复现（审查DONE） |

SKILL.state 的v1来自8月26日，本批核对的是后续版本的显式状态机制，不能把目录新增URL或版本更新改写成新论文首发。其余八篇的v1在10月14–15日，来自10月16日公告重叠。本页只固定本批范围，不声称剩余候选均已逐篇全文审结。

## 实际抓取时间与原始收据

抓取检查时间为 **2026-10-19 03:34:14—03:36:45（Asia/Shanghai）**；原始收据保留对应UTC值 `2026-10-18T19:34:14.229591+00:00` 至 `2026-10-18T19:36:45.590972+00:00`。抓取时间、公告日和论文v1日期分别记录，不混为首发时间。

来源文件为本轮实际生成的 `retrieval.json` 与 Google / Meta / DeepMind 三份差异JSON。提交的覆盖文件只保留49个页面的URL、原始抓取时间、内容SHA256和数量，不复制2.7MB的摘要集合。SHA256证明的是本次抓取内容指纹，不是可永久访问的网页镜像，也不证明网络来源已穷尽。

### 六类 arXiv 最新公告

| 分类 | 公告日 | new | cross-list | replacement | 解析 / 预期 |
| --- | --- | ---: | ---: | ---: | ---: |
| [cs.AI](https://arxiv.org/list/cs.AI/new?show=2000) | 2026-10-16 | 132 | 154 | 167 | 453 / 453 |
| [cs.CL](https://arxiv.org/list/cs.CL/new?show=2000) | 2026-10-16 | 105 | 72 | 90 | 267 / 267 |
| [cs.IR](https://arxiv.org/list/cs.IR/new?show=2000) | 2026-10-16 | 8 | 6 | 12 | 26 / 26 |
| [cs.LG](https://arxiv.org/list/cs.LG/new?show=2000) | 2026-10-16 | 166 | 140 | 161 | 467 / 467 |
| [cs.CV](https://arxiv.org/list/cs.CV/new?show=2000) | 2026-10-16 | 135 | 30 | 88 | 253 / 253 |
| [cs.RO](https://arxiv.org/list/cs.RO/new?show=2000) | 2026-10-16 | 89 | 13 | 47 | 149 / 149 |

以上六页均抓取成功、解析数量相符，最新仍是10月16日公告。分类之间有交叉，不能把1615条分类记录称作1615篇独立论文；replacement也不自动算新方法。页面解析完整仅说明收据未漏页内条目，不等于所有条目已全文审结。

### Google / Meta 优先来源

| 官方目录 | 本轮成功页 / 尝试页 | 本轮唯一URL | 10月15日基线 | URL差异 |
| --- | ---: | ---: | ---: | ---: |
| [Google Research](https://research.google/pubs/?category=2026&sort=-publication__year) | 28 / 28 | 417 | 412 | 5 |
| [Meta AI](https://ai.meta.com/results/?content_types%5B0%5D=publication&page=1) | 6 / 6 | 144 | 144 | 0 |
| [Google DeepMind](https://deepmind.google/research/publications/) | 9 / 9 | 265 | 265 | 0 |

比较基线分别是 `oct15-review-closure/` 中三个官方目录来源审计，不以“过去目录里有URL”推断论文已经实现。没有目录差异也不等于公司在所有网站、仓库或模型发布渠道都没有新内容。

## Google 五个URL差异逐项处置

| 目录差异 | 结论 | 原因 |
| --- | --- | --- |
| [SKILL.state](https://research.google/pubs/skillstate-scalable-long-horizon-agent-skills/) | 纳入本批P0历史补漏 | v1为2026-08-26；实现有独立价值、可低成本执行的显式状态组件 |
| [Differential Observability…-2](https://research.google/pubs/differential-observability-detecting-silent-state-divergence-in-ebpf-based-cloud-networks-2/) | 重复目录URL，不另算新论文 | 同标题[无后缀URL](https://research.google/pubs/differential-observability-detecting-silent-state-divergence-in-ebpf-based-cloud-networks/)已在基线审计；单独的`-2`地址不构成新方法证据 |
| [Regression Test Selection…-4](https://research.google/pubs/regression-test-selection-at-scale-4/) | 重复目录URL，不另算新论文 | 同标题[`-2`URL](https://research.google/pubs/regression-test-selection-at-scale-2/)已在基线审计；`-4`不是新的论文身份 |
| [The AI Divide…](https://research.google/pubs/the-ai-divide-bridging-the-implementation-gap-in-state-and-territorial-public-health-departments-2/) | 域外，不实现 | 公共卫生部门的AI落地/政策研究，不是本批研究库领域内的独立ML/Agent算法 |
| [Uniform Laws of Large Numbers…](https://research.google/pubs/uniform-laws-of-large-numbers-in-product-spaces/) | 域外，不实现 | 概率/统计学习理论，不属于本批模型、训练或Agent可执行组件范围 |

因此是 **5个新增目录URL → 1篇历史补漏 + 2个重复URL + 2篇域外研究**，不是5篇当日新算法论文。

## 验收状态与不可越过的边界

四项CPU与三项A100组件均已完成主流程验收；每项种子为42、43、44。首轮源码固定在 `8c963f810e45ce3886e43b1b5da39980e41c95c0`；AlphaDiana 的缺记录成本检查随后修复，两个 Agent 协议按 `39e912c1124c49b7d3a85957909fb143d8c9ba3c` 重新执行。未变化的 GPU 源码与实跑仍绑定首轮提交。各项实际metrics和GPU收据链接见上表；[冻结源码证明](frozen-sources.json)供离线浅克隆校验，不依赖旧分支一直可达。GPU结论仅覆盖本轮小规模算子执行，不包含完整checkpoint、真实任务能力或端到端加速结论。

九篇的**完整实验**统一按成本门槛标记 `not_reproduced_high_cost`，属于审查DONE而非阻塞水位的TODO；两篇资料没有算法Adapter。全部保持诊断边界，不把构造轨迹称为官方benchmark，不把算子检查称作完整能力复现，不据此晋升evolve。

## 标签与状态计数复核

本批新增的静态保真清单命中为两处输出类型检查、两处将 actor 已生成回答送入独立 grader，以及一处运行时版本计数。逐处确认它们不读取 gold：reference 只在评分侧，版本计数也不作为动作或能力执行证据。相应行为测试覆盖私有字段隔离、失败计量和无效 patch 不执行；静态清单本身不充当语义通过证书。

## 尚未声称覆盖的范围

- 本批不是六类公告全候选的全文审查闭环；只审结并固定上述九篇的组件/资料选择。
- 本轮未穷尽其他机构官网、作者仓库、模型/benchmark发布与未列来源；也没有把摘要不写A/B当作工业论文的拒绝条件。
- Google/Meta优先来源的目录检查不替代正文中的线上实验、部署和成本证据核验。
- 没有根据未提供的目录日期猜测首发日，也没有把高成本不复现写成算法实现完成。
- 审查水位继续为10月15日；下一次需要独立的覆盖闭环才能推进，不能仅因本批组件全部通过就修改日期。
