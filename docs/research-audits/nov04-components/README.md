# 11月4日近期论文：Google/Meta优先与低成本组件

实际可见的最新arXiv公告为 **2026-11-03**。本页是固定8篇的交付，不宣称全网或公告池全文穷尽；新首发、近期补漏、官方URL变化和版本更新分别记账。

## 固定范围

| 优先级 | 论文 | 本地交付 | 未执行的完整实验 |
| --- | --- | --- | --- |
| P0 · Google | [XLA from the Trenches](../../foundation-models/2611.00624-xla-trenches/README.md) | 仅审查，公开工具与内部TPU系统分开登记 | 多代TPU、约20万私有生产图与内部agent工具，不用A100替代TPU |
| P0 · Meta合作 | [Strategist](../../agent-research/2611.03618-strategist/README.md) | CPU：blueprint/AST、检索分数核、测量卡与配对选择 | 不运行完整executor/meta-agent搜索与多benchmark矩阵 |
| P0 · 工业A/B | [WeSearch](../../recommendation-components/2611.00530-wesearch/README.md) | CPU：簇候选并集、OPQ/ADC距离、固定参数新快照 | 不运行私有十亿文档检索器、训练/特征FFN或生产A/B |
| P1 | [ProLand](../../foundation-models/2611.00236-proland/README.md) | CUDA：thin-factor动量、低秩polar与Landing | 不微调完整LLM/多模型多秩矩阵 |
| P1 | [GAVAGAI](../../foundation-models/2611.00319-gavagai/README.md) | CUDA：带Nothing的容量OT、停梯度对齐与先验 | 原文4×A100、约11小时训练，不跑完整视觉语言训练 |
| P1 | [SpecOPD](../../post-training/2611.02846-specopd/README.md) | CUDA：树mask、前驱readout、TV前缀损失 | 不加载drafter/teacher、采rollout或声明推理提速 |
| P1 | [RLiD](../../post-training/2611.02455-rlid/README.md) | CUDA：合法菜单策略、校准、PPO与信用方差审计 | 不运行扩散LLM/环境任务RL |
| P1 · 补漏 | [AgentHeal](../../agent-research/2610.39234-agentheal/README.md) | CPU：外部证据、来源版本/合规/弃答判定 | 不运行真实浏览器actor或语义judge |

8篇完整实验均明确**成本过高，不复现（审查 DONE）**，不进入自动重试。7个组件仅为L1诊断，1篇仅资料收录；没有完整能力复现或执行型Evolve接入。Strategist一作机构仍为Princeton，Meta合作不改写为一作Meta。AgentHeal于10月29日首发，是相对前轮快照的补漏；其余7篇在前轮10月30日快照之后首发。

## 实际执行与复核

[成本预审](preflight.json) · [冻结源码证明](frozen-sources.json) · [CPU原始结果](raw-cpu.json) · [CUDA原始结果](raw-cuda.json) · [逐篇范围与成本](task-scope.json)

CPU执行7组件×3seed，真实A100执行4个CUDA组件×3seed；使用42/43/44、小矩阵与状态合同，不下载模型/能力数据、不调LLM/API。每篇独立`metrics/component-{cpu,cuda}-seeds42-44.json`保存实际数值，四篇各有独立[GPU回执](../../gpu-validation.md)。运行器内部时间不含研究、传输和启动，不是完整实验耗时。

交叉审查发现WeSearch重构可把分别有界的小输入展开成超大输出，已在索引前限制组合规模并增加拒绝测试，随后以修复后源码重新冻结和执行CPU/A100；旧诊断保留，不挪用旧源码回执。GAVAGAI固定8步OT的行和残差被如实保留，不靠事后重归一化假装完全收敛。

## 来源与去重

[来源回执与身份列表](source-coverage.json)包含8类new、8类recent和45页有界机构目录。new共3015个分类条目、2168个去重身份，recent共4796个身份；这些是召回规模，不是新合格论文数或已读全文数。**统一审查水位仍为2026-10-15**。

Google目录439条、Meta六页144条、DeepMind九页266个去重详情URL。DeepMind标题写267，解析集合为266，差异保留，不宣称穷尽。[优先机构复核](priority-review.json)逐项解释新增5个URL：FabScore是旧题名的新可读来源，但首次公开日期仍未确认；What Limits Us和EmbeddingGemma2已有记录；Entitlement Is Not Authorization属于订阅权限一致性，Chiplet Fault Grading属于制造测试，不因Google优先而越过主题边界。

[原始详情回执](primary-receipts.json)保留成功/失败区别；[10条未完成审查线索](unreviewed-leads.json)明确不算本批实现或审查DONE，不把“没读完”写成“高成本不复现”。后续从已知线索继续，不重包装为另一批当天新论文。

## 学习资料与双语

8篇各新增基础、机制、对比、实现四层问答，共32题；同步7个既有专题的对照、分析、自测和绑定README指纹的更新。论文页、问答、深读和本页均在同一PR交付校对后的英文版。

[最近问答](../../learning/recent.md) · [全部问答](../../learning/all.md) · [专题精读](../../learning/deep-dives/index.md)
