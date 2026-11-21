---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 经验进入长期系统前，要解决存取、价值与准入

[Agent](../index.md) · 更新 2026-11-21 · 66 篇主题资料 / 17 篇重点对照

MemGPT 管信息放在哪里，MemPrice 管有限窗口里保留何种精度，CMP 管效用如何识别；Voyager 把成功程序变技能，VaG 管技能进入库的风险，SkillRise 用后续任务检验整理价值。存得下、相关、合法和能帮助未来，是四个不同问题。 EMMA再把结构化记忆分配给controller、agent与skill，按失败scope限制单次编辑及下一次实际使用义务。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/agent-research/memory-and-skills.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：对象是原始事件、压缩表示、运行状态还是可执行技能 · 决定发生在写入、读取、淘汰还是持久准入 · 价值来自相似度、当前成功、随机曝光还是下游任务 · 原始细节和错误后代是否可以恢复或撤销

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [MemGPT](../../../agent-research/2310.08560-memgpt/README.md) · [原始来源](https://arxiv.org/abs/2310.08560)<br>章节：背景与主要改动、核心公式、复现边界 | 分层管理核心信息、当前上下文和外部归档，以模型函数调用和 heartbeat 控制换入换出。 | 外部容量不等于当前可见，检索仍可能漏证据；本地使用确定性 key 与代理成本，不是语义检索服务。 |
| [MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents](../../../agent-research/2610.24955-memprice/README.md) · [原始来源](https://arxiv.org/abs/2610.24955)<br>章节：背景与主要改动、核心公式、本地复现与边界 | 每项记忆选 raw/summary/abstraction/keywords/delete 中一版，以背包满足硬预算，队列价格反映长期占用。 | 联合分配依赖效用和token大小输入，窗口已删细节只能经归档刷新恢复；本地只执行DP与状态合同。 |
| [Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval](../../../agent-research/2610.02070-causal-memory-policy/README.md) · [原始来源](https://arxiv.org/abs/2610.02070)<br>章节：背景与主要改动、核心公式、复现边界 | 在固定候选池预留均衡随机曝光，估计设计下处理/对照净效应及标准误，不确定时保护记忆。 | 处理一条会改变其他槽位分布，效应不能当独立加性系数；本地合成结果不证明真实问答或长期删除策略。 |
| [Voyager](../../../agent-research/2305.16291-voyager/README.md) · [原始来源](https://arxiv.org/abs/2305.16291)<br>章节：背景与主要改动、核心公式、复现边界 | 自动课程产生任务，代码执行和反馈修订后，将验证成功程序作为可检索技能继续组合。 | 一次环境成功仍有适用前提；本地技能是结构化工具计划，没有 Mineflayer/GPT-4 或真实 Minecraft。 |
| [When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents](../../../agent-research/2608.05810-vag/README.md) · [原始来源](https://arxiv.org/abs/2608.05810)<br>章节：背景与主要改动、核心公式、复现边界 | 在持久写入前检查结构、行为无害与语义一致，再按边际收益选择可兼容 Hot 技能集合。 | 阻止污染早于事后删除，但验证仍受覆盖限制；本地只执行相关核心算子，候选发现不等于完整能力进化。 |
| [SkillRise](../../../agent-research/2607.26784-skillrise/README.md) · [原始来源](https://arxiv.org/abs/2607.26784)<br>章节：背景与主要改动、核心公式、复现边界 | 同一policy交替求解与整理文档，当前结果监督solve，下游折扣结果监督curate。 | 要求任务序列能暴露经验迁移价值；本地仅验证状态和phase信用，未做原文模型RL。 |
| [Remembering Is Not Enough: Refining Memories and Learning When to Use Them in Multi-Agent Systems](../../../agent-research/2610.36652-discernmem/README.md) · [原始来源](https://arxiv.org/abs/2610.36652v1)<br>章节：背景与主要改动、核心公式 | 配对效果、范围优先归因、双参照修复门槛及版本证据清空。 | scope/defect/replay分数外部提供，不用规则冒充LLM诊断与修复。 |
| [EMMA: Structured Episodic Memory for Multi-Agent Workflow Synthesis](../../../agent-research/2610.35966-emma/README.md) · [原始来源](https://arxiv.org/abs/2610.35966v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 按controller/agent/skill组织持久记忆，依据失败scope只改责任条目；临时execution slip不写长期经验，overflow先拆未完成步骤。 | 单编辑守卫不证明语义正确，安全判断仍外置；接受编辑后须下一次实际使用，不能以最终未重跑编辑冒充改进。完整多环境系统未复现。 |
| [ENGRAM: From Agent Experience to Weights through Verified Consolidation](../../../agent-research/2611.09472-engram-consolidation/README.md) · [原始来源](https://arxiv.org/abs/2611.09472)<br>章节：背景与主要改动、核心公式、诊断与边界 | 训练前以学生熟练度或成功教师示范准入；训练后按技能用配对探针决定候选无检索能否替代 Base+ETG。 | 验证通过才能归档合格记录，混合启用仍保留检索。局部探针不等于完整 rollout；本地只执行 CPU 双关口，不做训练。 |
| [Don&#x27;t Just Trust Your Memory: Evidence-Linked Memory Reduces Memory-Induced Degradation in LLM Agents](../../../agent-research/2611.14320-wikitrace/README.md) · [原始来源](https://arxiv.org/abs/2611.14320)<br>章节：背景与主要改动、核心公式、数据协议与代码映射 | 冻结训练轨迹、模型解释和洞见的三层证据链接；测试Agent先看全部洞见，再按需回查原始运行。 | 来源可回查不等于解释已验证或Agent会正确使用；本地只有只读语料、hash与导航，没有编译LLM或任务能力对照。 |
| [LiSA: Lifelong Safety Adaptation via Conservative Policy Induction](../../../agent-research/2605.14454-lisa/README.md) · [原始来源](https://arxiv.org/abs/2605.14454)<br>章节：核心公式、数据协议与代码映射、本地结果与负控 | 以Beta后验下界门控广义策略，并用按领域的混合标签局部提示保留边界；跨日平均链接重聚类和同原句运行时统计继承均显式执行。 | 置信度度量反馈条件下的可复用可靠性，不是因果收益或token效用；本地策略草稿与embedding来自外层，未运行LLM归纳和guardrail。 |
| [PolicyBank: Evolving Policy Understanding for LLM Agents](../../../agent-research/2604.15505-policybank/README.md) · [原始来源](https://arxiv.org/abs/2604.15505)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、复现边界 | 按工具能力存半结构化授权解释，header→ID选择→全文检索，再据外部开发反馈Add/Revise/Omit。 | MemGPT解决有限上下文的分层容量与换入换出，PolicyBank解决spec与requirement差异。容量足够不代表规则正确；本地PolicyBank只有L0合同，语义修复仍缺失。 |
| [CoReMem: Cost-Internalizing Memory for Successive Coding Tasks with Prospective Valuation](../../../agent-research/2611.17316-coremem/README.md) · [原始来源](https://arxiv.org/abs/2611.17316v1)<br>章节：背景与主要改动、核心公式 | 在继承repo的后续任务上，以同状态有／无记忆rollout估计价值，并将整体价值通过可追踪首次锚点使用门控到步骤。 | MemPrice分配上下文容量与记忆保真；CoReMem优化未来编码解决率和工作量。token占用、行为步骤和语义效用不是同一目标，局部算子不产生记忆内容。 |
| [Instant Weight-Space Consolidation for Long-Term Memory in LLMs](../../../agent-research/2611.20759-clam-memory/README.md) · [原始来源](https://arxiv.org/abs/2611.20759v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | CLAM把可积累的参数记忆与逐字检索缓冲分开：冻结LLM提供每层会话activation，hypernetwork在不做测试时梯度下降的情况下写出down_proj LoRA，查询时再配top5会话片段。没有提取调用不等于没有前置训练；能力来自离线context distillation。 | CoReMem通过未来同仓库任务的有／无记忆差估值并训练写入信用；CLAM通过全历史teacher蒸馏把history压进权重。前者是前瞻效用，后者是参数通道，两者都不能用静态摘要相似度冒充任务收益。完整实验成本过高，不复现（审查DONE）。 |
| [Forget Freely, Grep Later: Lossless, Index-Free Memory for Long-Horizon LLM Agents](../../../agent-research/2611.25123-grepmem/README.md) · [原始来源](https://arxiv.org/abs/2611.25123v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界、高成本完整实验 | GrepMem把有限工作上下文和完整历史分开：压缩时只把活跃上下文换成系统提示、任务与摘要，原始消息、工具调用/输出和摘要仍追加到纯文本日志。第一次压缩之后才开放grep_history，让模型按需用大小写不敏感正则取回遗漏细节。不需要embedding、索引或知识抽取，但“lossless”只指原日志保留，不代表模型每次都能找对或答对。 | MemGPT以分层内存、page-out/page-in与模型工具调用管理归档；GrepMem不预先抽取归档结构，保留原始轨迹并做词法搜索。两者都可压缩工作上下文，但GrepMem没有减少原始日志占盘；模型是否会选对检索词仍需训练与真实任务评价，本地固定key的旧MemGPT诊断也不能作能力对照。 |
| [MemFolder: Structure-Guided Memory Folding for Efficient Agent Memory Management](../../../agent-research/2611.26427-memfolder/README.md) · [原始来源](https://arxiv.org/abs/2611.26427v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验 | MemFolder把记录数和取回上下文长度分开处理。RecordFolder先用LLM统一实体，再以密度峰选首锚点、以相对已有锚点的novelty渐进选互补锚点；语义/实体亲和与时间链修正分组，最后由LLM按时间合并。ContextFolder沿用这些分组，按事实重要性和token比例编码，通过看不到源记录和预期答案的blind reader检查可恢复性。分组不是摘要生成，校验也不是无损保证。 | MemForest按事件构建最大生成树并渐进合并，检索时从anchor传播到时间邻域；MemFolder先以全局互补锚点确定目标组数，再用实体/语义gain和Hungarian非分支时间链修正组，并另加独立的ContextFolder编码层。二者都保留结构，但树形层次与一入一出的链不等价。现有本地MemForest用词项重叠近似语义，本地MemFolder只收显式embedding，因此不能凭两者单测数值宣称谁的模型记忆更好。 |
| [MemLife: Curating and Reasoning over Long-Term Egocentric Video Memories](../../../agent-research/2609.40195-memlife/README.md) · [原始来源](https://arxiv.org/abs/2609.40195v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、同主题比较与边界、高成本完整实验 | MemLife先把每段第一视角视频和语音写成有时间锚点、实体落地的第一人称文本，再由reader按问题进行语义搜索和时间区间读取。MemOpt只训练writer，reader保持冻结；FIRM将逐token的faithfulness、逐候选的informativeness和retrievability相乘。前者看源视频是否支持内容，后两者分别看回答所需事实是否被保留、已缓存reader动作能否找回该候选，不把完整reader成败混成一个写入奖励。 | MemFolder主要改变已有记忆如何分组、合并与编码，MemOpt则改变writer生成什么文本以及如何分配训练credit；前者的结构压缩和后者的写入奖励不互相替代。MemFolder的ContextFolder blind reader看不到源记录/预期答案；MemOpt训练评审可用源视频和训练问答，但这些信息不得流向被评测reader。二者本地都是L1数学组件，不能把分组数或优势方差当QA准确率比较。 |

</div>

## 取舍分析 {#analysis}

### 资源分配器需要效用，但不会自动产生因果证据

MemGPT 使信息可被移到归档，MemPrice 再在当前窗口联合分配多级表示；两者都需要决定什么值得留下。CMP 处理的是另一层：难题更常检索某条记忆，不能把相关失败都归咎于它，随机曝光才提供可识别的对照。将 CMP 的估计交给分配器也须保留曝光设计和不确定度，不能把固定槽位净效应直接当可随意相加的单项价值。

对照来源：[memgpt](../../../agent-research/2310.08560-memgpt/README.md) · [memprice](../../../agent-research/2610.24955-memprice/README.md) · [causal-memory-policy](../../../agent-research/2610.02070-causal-memory-policy/README.md)

### 当前成功、持久准入与未来受益是三个时点

Voyager 让成功程序进入技能积累链，VaG 更强调新经验会影响后代，需在写入前检查并考虑共同使用的兼容性。SkillRise 又把整理行为交给下游任务结果评价：当前成功主要说明求解，不足以说明留下的文档帮助未来。这不是谁更先进的直线序列，而是不同证据合同：执行通过、库准入和跨任务学习应分别记录。

对照来源：[voyager](../../../agent-research/2305.16291-voyager/README.md) · [vag](../../../agent-research/2608.05810-vag/README.md) · [skillrise](../../../agent-research/2607.26784-skillrise/README.md)

### 10月29日：新方法与来源变化

DiscernMem把失败先分为记忆使用范围不对和内容缺陷：对同任务、seed、配置做单记忆/无记忆配对重放，再检查修复是否同时守住父记忆与无记忆基线。它补充了简单追加反思的风险控制：团队结果差不能直接归罪某条记忆；新版本也不能继承旧版本已测效果。本地只做这些测量和版本合同，没有LLM修复或重放。

对照来源：[memgpt](../../../agent-research/2310.08560-memgpt/README.md) · [discernmem](../../../agent-research/2610.36652-discernmem/README.md)

### 先定位修改责任，再证明这次修改有用

DiscernMem用孤立注入与无记忆配对重放区分作用范围和内容缺陷，并以父记忆/无记忆双参照验收修复。EMMA更偏编辑组织：controller、agent specialization与skill有不同所有者，一次反思只能改承担责任的一项，执行失误只影响临时计划。一个解决归因与修复效果，一个约束该改哪层及如何exercise；结构合法不能替代配对收益，也不能把外部语义安全Boolean视为已实现的LLM审查。

对照来源：[emma](../../../agent-research/2610.35966-emma/README.md) · [discernmem](../../../agent-research/2610.36652-discernmem/README.md)

### 窗口里不放某条记忆，不等于权重可以取代它

MemPrice 按预算和效用在多种表示之间选择，决定此刻读什么；ENGRAM 在外部训练后做候选无检索与 Base+ETG 的同题配对，决定哪些已用于训练的记录可以退出检索。前者节省窗口成本但不证明权重已经掌握技能；后者检验局部行为，但不等于端到端能力或总存储下降。

对照来源：[memprice](../../../agent-research/2610.24955-memprice/README.md) · [engram-consolidation](../../../agent-research/2611.09472-engram-consolidation/README.md)

### 先找到相关记录，与检查一句经验的来源是两件事

MemFit保留原turn并用摘要索引和混合检索缩小候选；WikiTrace保留洞见到解释及原执行的链接，让模型可检查一条经验为何成立。排序正确不能修复错误解释，源完整也不保证模型会下钻。二者本地都是独立组件：前者未调用embedding/cross-encoder，后者未调用编译LLM或测试Actor，不能由接口测试推断长期问答收益。

对照来源：[wikitrace](../../../agent-research/2611.14320-wikitrace/README.md) · [memfit](../../../agent-research/2610.00872-memfit/README.md)

### 记忆值不值得放入，与证据够不够支撑，是两根轴

MemPrice在有限token下联合分配保真等级，以效用与长期压力定价；LiSA在语义检索后问广义规则是否有足够支持，弱规则可能不展示而局部矛盾提示仍保留。低token成本不保证可靠，可靠也不保证预算内最优。两者分别需要外部效用/压缩或策略/embedding，不能把合成输入下的精确求解说成任务能力提升。

对照来源：[lisa](../../../agent-research/2605.14454-lisa/README.md) · [memprice](../../../agent-research/2610.24955-memprice/README.md)

### 记忆记得更多，与记忆中的授权规则可信，是两种问题

MemGPT分层归档使长期信息可取回；PolicyBank则允许修正先前解释而不是反复遵守有缺口的规则。标题选择降低注入量，但相关ID选择仍需真实actor。外部PolicyAgent给出修正不应被库当成授权真理，本地只有typed变更和provenance；恶意反馈、真实权限审核与正式验证都在边界外。

对照来源：[policybank](../../../agent-research/2604.15505-policybank/README.md) · [memgpt](../../../agent-research/2310.08560-memgpt/README.md)

### 记忆的价格、价值和信用来自不同测量合同

MemPrice的精确背包把外部估计效用与token大小在容量内折衷，压力队列调节长期保留。CoReMem则必须从相同继承repo比较未来任务，固定成功优先reward，再用锚点定位使用。二者的外部语义模块都没有由本地算子补齐：少存token不等于少做动作，锚点出现不等于因果效果。

对照来源：[coremem](../../../agent-research/2611.17316-coremem/README.md) · [memprice](../../../agent-research/2610.24955-memprice/README.md)

### CLAM：会话流压缩到固定大小的参数记忆

Read用9层Perceiver cross-attention、每层8slots，slots只看当前会话。Carry先对slots做一次8头self-attention，再对每slot产生一个sigmoid门混合旧Q与新x，并LayerNorm。Decode用每层每rank一个query生成rank8 adapter，大小不随会话数增加；合成模型还含固定bias。顺序和门不能被普通均值池化替代。 CoReMem通过未来同仓库任务的有／无记忆差估值并训练写入信用；CLAM通过全历史teacher蒸馏把history压进权重。前者是前瞻效用，后者是参数通道，两者都不能用静态摘要相似度冒充任务收益。完整实验成本过高，不复现（审查DONE）。

对照来源：[clam-memory](../../../agent-research/2611.20759-clam-memory/README.md) · [coremem](../../../agent-research/2611.17316-coremem/README.md)

### GrepMem：压缩工作上下文，但保留可grep的原始历史

grep按原始记录头与行号返回最早匹配，默认10条、最多30条，offset跳过匹配行而非记录；前后context默认1行、最多3行。旧grep结果仍留在原日志，但搜索跳过它们以免递归重复。单次输出上限6K字符，围绕匹配裁到300字符并在完整match边界停止，返回继续offset；非法正则或超过10秒都返回错误。控制测试验证摘要可遗漏原始细节而日志仍保留、只计原始匹配而不递归grep输出、大小写无关、连续offset不漏页；长行与多匹配验证6K上限，灾难性回溯正则会终止worker，随后正常查询仍可用。论文的模型turn预算、自动token估计与forced-answer调用不在这个存储工具组件内，不捏造自动压缩策略或训练效果。

对照来源：[grepmem](../../../agent-research/2611.25123-grepmem/README.md) · [memgpt](../../../agent-research/2310.08560-memgpt/README.md)

### MemFolder：用互补锚点和非分支时间链减少检索单元

实体权重为log(N/df)，共有的实体权重可为0；weighted Jaccard与cosine按共享实体质量和两种信号方差自适应混合。方差先在整个W窗口的前后记录对上计算，再筛正gain和每后继最多d条候选边；gain相对的是后继与初始锚点的cosine。Hungarian最大化总gain，各节点最多一入一出，锚点不可有入边，所以没有分叉或时间环。有锚点的链留在该组，无锚点链按整链cosine总和选组，未匹配项保留原分组。负控包括全记录恰好分配一次、重复embedding仍保留K个非空组、N=1、所有实体共有时退化为cosine、在筛边前计算窗口方差、时间边向前且锚点无入边、每节点最多一入一出，以及一个greedy得0.9而Hungarian得1.6的显式矩阵单测。后者仅是组合优化单测，不是记忆准确率。上下文验证可能误判源事实，且原文回退可选择缺失required facts的较短候选，不能把ContextFolder宣传为无损存储。

对照来源：[memfolder](../../../agent-research/2611.26427-memfolder/README.md) · [memforest](../../../agent-research/2609.08273-memforest/README.md)

### MemLife / MemOpt：把忠实、信息保留和可检索性分解给记忆写入器

Eq.11先对每个候选的response token求均值，再对候选做宏平均，避免长记忆独占基线。方差是每个候选围绕同一group均值的token偏差平方再宏平均，不能改成候选内部方差，否则丢掉informativeness/retrievability的候选间信号。Eq.12归一化后先clip到±3，再按组中有效response token加权重心化，最后全局masked whitening；prompt和padding始终排除。KL属于Eq.16 loss项，不进入FIRM奖励或优势统计。训练reward可用训练问答，问题独立的writer与被评测reader不可读测试答案。长度不等候选构造宏均值0.5而token池均值0.25，检验group方差0.25而非候选内方差0；稀疏离群值检验clip后重心化。有效response奖励限定[0,1]；极大有限padding先归零，有限输入的ratio乘advantage或KL项溢出也明确拒绝，不能输出inf或把溢出方差伪装成零优势。负控还包括全平group、空候选/padding、无效概率、KL只影响独立loss、不改变奖励、严格未来片段和其他subject在检索前排除、恰好query_time的片段可用。所有输入是合成显式控制值，没有任何gold QA或视频内容输入reader；通过率不是长视频QA能力。

对照来源：[memlife](../../../agent-research/2609.40195-memlife/README.md) · [memfolder](../../../agent-research/2611.26427-memfolder/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### MemPrice 背包选中一条“高效用”记忆，为什么 CMP 仍会追问这个效用是怎样测出来的？ {#cross-allocation-versus-identification}

??? note "展开答案与例子"

    **答案：** 背包只在给定效用与大小下求联合分配，不证明上游估计可靠。如果记忆常在难题出现，观察到失败多可能只是选择偏差；CMP 用均衡随机曝光和对照估计设计下净作用，并保留标准误。这个净效应又受槽位替代影响，不能不加条件当成独立可加背包收益。

    **教学例子：** 教学例：故障排查记忆总在最难事故被检索，成功率低不说明它有害；先辨别没有它时会怎样，再讨论是否值得占窗口。

    对照来源：[memprice](../../../agent-research/2610.24955-memprice/README.md) · [causal-memory-policy](../../../agent-research/2610.02070-causal-memory-policy/README.md)

### Voyager 一次执行成功的程序，为什么不能不经检查就当成 VaG 里可与所有技能共同使用的长期经验？ {#cross-successful-skill-versus-admission}

??? note "展开答案与例子"

    **答案：** 一次成功支持该环境中的执行路径，未说明程序在其他前提仍无害，也未排除与已有技能冲突。VaG 在写入前分开检查结构、行为和语义，再以集合边际价值选择兼容组合。两种机制可以讨论不同生命周期，但不能把成功、无害和组合收益合并成一张通过票。

    **教学例子：** 教学例：技能在空目录中成功，若暗含删除旧文件的前提，搬到共享目录可能有害；单次成功没有验证这个新作用域。

    对照来源：[voyager](../../../agent-research/2305.16291-voyager/README.md) · [vag](../../../agent-research/2608.05810-vag/README.md)

### 为什么 SkillRise 的整理文档不能直接沿用 Voyager 式当前任务成功信号？ {#cross-current-outcome-versus-future-skill}

??? note "展开答案与例子"

    **答案：** 当前成功主要说明刚才的动作完成目标，文档价值却体现在后续相关任务能否借它行动。SkillRise 将solve与curate分phase，用下游折扣回报监督后者，并只作用于对应生成token。Voyager 的成功程序准入提供执行证据，不能替代这项跨任务信用；漂亮但无用的总结也不应因当前成功自动获奖。

    **教学例子：** 教学例：当前任务靠偶然试错成功，文档若只写具体答案，下一题无法复用；下游评价才会暴露它没有留下可迁移步骤。

    对照来源：[skillrise](../../../agent-research/2607.26784-skillrise/README.md) · [voyager](../../../agent-research/2305.16291-voyager/README.md)

### 为何修复后比父记忆好，还可能不能接收？ {#cross-oct29-method-boundary}

??? note "展开答案与例子"

    **答案：** 父记忆本来就可能有害；候选还必须不弱于无记忆基线，守住历史任务并不增加完全失败数。单一正增益不能替代双参照非退化检查。

    **教学例子：** 教学例：父记忆得0.2，候选0.4，无记忆0.8；候选比父版好，但仍不能据此称记忆有价值。

    对照来源：[memgpt](../../../agent-research/2310.08560-memgpt/README.md) · [discernmem](../../../agent-research/2610.36652-discernmem/README.md)

### EMMA一次只改一项记忆，是否就已经完成DiscernMem要求的因果归因与修复验收？ {#cross-emma-single-edit-versus-memory-effect}

??? note "展开答案与例子"

    **答案：** 没有。单编辑减少修改scope并明确责任，但还需实际使用和重跑；DiscernMem另用相同任务/seed的隔离记忆与无记忆结果，核对候选是否同时不弱于父版和无记忆。结构约束与效果证据不是相同的通过条件。

    **教学例子：** 教学示意：把一次检索拼写错误写成永久skill违反EMMA的scope规则；把skill文本改得合法也不能证明它比不使用记忆更有帮助。

    对照来源：[emma](../../../agent-research/2610.35966-emma/README.md) · [discernmem](../../../agent-research/2610.36652-discernmem/README.md)

### MemPrice 决定本轮不加载某条记录，能用这个信号直接批准 ENGRAM 释放记忆吗？ {#cross-engram-approval-versus-window-budget}

??? note "展开答案与例子"

    **答案：** 不能。MemPrice 解决给定预算下的表示分配。ENGRAM 的释放还要有本轮训练参与、留出探针和通过双门槛的无检索候选；已归档的记录不从物理存储删除。

    **教学例子：** 教学例：四个探针只有两题正确，即使比 Base+ETG 多答对一题，在严格下限为 50% 时仍须保留记忆。

    对照来源：[memprice](../../../agent-research/2610.24955-memprice/README.md) · [engram-consolidation](../../../agent-research/2611.09472-engram-consolidation/README.md)

### 最相关的经验已排第一，为什么WikiTrace仍需要原轨迹，MemFit的检索测试又能说明什么？ {#cross-source-link-versus-memory-ranking}

??? note "展开答案与例子"

    **答案：** 相关性只决定先看到谁，不证明经验正确或适用。WikiTrace的来源层可让模型检查被摘要遗漏的观察；MemFit本地融合hook只验证给定分数如何组合，并未测模型算出的语义分或下钻行为。应分别验来源保真、排序与实际使用。

    **教学例子：** 教学例：记忆说“任务结束”，原轨迹还有后续提交动作。排第一没有解决遗漏；正确链接也尚未证明模型会发现它。

    对照来源：[wikitrace](../../../agent-research/2611.14320-wikitrace/README.md) · [memfit](../../../agent-research/2610.00872-memfit/README.md)

### 一个只有一次支持的规则很短，MemPrice能放进预算，LiSA为什么仍可能不展示？ {#cross-cross-memory-confidence-versus-capacity}

??? note "展开答案与例子"

    **答案：** 容量选择和证据可靠性不是同一约束。MemPrice的候选成本/效用允许某表示入选，不证明规则正确；LiSA的Beta(2,1)5%分位数约0.22361，低于0.55。若它是已发现的局部边界提示，又不适用广义策略同一门控。

    **教学例子：** 教学例：10token规则被分配器保留，但只成功过一次；全局安全建议应暂缓，公开/私密两个情境的局部冲突提示可以另行呈现。

    对照来源：[lisa](../../../agent-research/2605.14454-lisa/README.md) · [memprice](../../../agent-research/2610.24955-memprice/README.md)

### 成功轨迹记忆能否替代PolicyBank的授权解释更新？ {#cross-cross-colm-policybank}

??? note "展开答案与例子"

    **答案：** 不一定。轨迹告诉agent过去怎么做，可能反复执行有缺口的spec。PolicyBank关注开发反馈中的授权逻辑差异；本地结构化存储仍不具备语义修复能力。

    **教学例子：** 教学例：十次成功改签案例也无法证明不改签时应否补偿，需要明确边界反馈。

    对照来源：[policybank](../../../agent-research/2604.15505-policybank/README.md) · [memgpt](../../../agent-research/2310.08560-memgpt/README.md)

### 降低记忆token占用是否必然提高CoReMem的前瞻价值？ {#cross-cross-nov15-coremem}

??? note "展开答案与例子"

    **答案：** 不必然。占用节省可能丢掉未来必要检查；CoReMem要在相同继承状态上测后续解决率和工作量。MemPrice的容量目标与这个reward不是可互换指标。

    **教学例子：** 教学例：删掉一条短测试命令只省数token，却可能让下一任务多探索十步。

    对照来源：[coremem](../../../agent-research/2611.17316-coremem/README.md) · [memprice](../../../agent-research/2610.24955-memprice/README.md)

### CLAM与CoReMem都写memory，有何关键区别？ {#cross-cross-nov18-latest-clam-memory}

??? note "展开答案与例子"

    **答案：** CLAM蒸馏全历史答案生成参数；CoReMem以未来任务有无记忆差值训练信用。前者不是后者的低成本替身。

    **教学例子：** 教学例：记住一个姓名不等于证明下一仓库任务节省步骤。

    对照来源：[clam-memory](../../../agent-research/2611.20759-clam-memory/README.md) · [coremem](../../../agent-research/2611.17316-coremem/README.md)

### 它和MemGPT的记忆结构有什么不同？ {#cross-cross-nov20-grepmem}

??? note "展开答案与例子"

    **答案：** MemGPT分层管理与换入换出，GrepMem保留原始文本、按正则取回而不建语义索引；两者都不能仅凭存储单测宣称模型会正确回忆。

    **教学例子：** 教学例：grep订单编号不要求先把订单提炼成一条结构化记忆。

    对照来源：[grepmem](../../../agent-research/2611.25123-grepmem/README.md) · [memgpt](../../../agent-research/2310.08560-memgpt/README.md)

### MemFolder的时间链和MemForest的事件树能互换吗？ {#cross-cross-nov21-memfolder}

??? note "展开答案与例子"

    **答案：** 不能。MemFolder匹配约束每节点最多一入一出，无锚点链整体分组；MemForest保留事件树层次并用anchor邻域传播。数据结构和检索假设不同。

    **教学例子：** 教学例：一个父事件分出两条子事件可在树中表达，不能直接塞进无分支匹配链。

    对照来源：[memfolder](../../../agent-research/2611.26427-memfolder/README.md) · [memforest](../../../agent-research/2609.08273-memforest/README.md)

### MemOpt和MemFolder都优化记忆，优化的对象一样吗？ {#cross-cross-nov21-memlife}

??? note "展开答案与例子"

    **答案：** 不一样。MemOpt分解训练奖励以改writer输出；MemFolder整理和压缩已有记录。不能把检索单元变少等同于writer更忠实或更会保留事实。

    **教学例子：** 教学例：把两条记忆合为一组是结构整理，降低幻觉token的训练credit是写入器优化。

    对照来源：[memlife](../../../agent-research/2609.40195-memlife/README.md) · [memfolder](../../../agent-research/2611.26427-memfolder/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-21** · 本地只接收显式概率/奖励数组与response mask，执行Eq.7的概率差、FIRM乘积、Eq.11-12宏统计、clip/组内token重心化/全局whitening和Eq.16已给ratio/advantage/KL的标量loss算术。独立NumPy float64实现，normalization epsilon=1e-6，whitening epsilon=1e-8、样本方差correction=1作为显式数值协议；不声称与外部trainer逐bit相同。空候选从G排除，空group输出0；全batch少于2个有效token则拒绝，不补造whitening。另有最多512条的显式unit-vector SearchMemory/FetchMemory：先按end≤query_time及区间完整包含过滤，再排序；返回按时间排列。单subject过滤是本地隔离合同，不是论文LVQA混合受试者基准，也不认证调用者身份。没有视频/embedding模型、VLM评审、writer/reader、训练数据构建、cached reader trace生成、RL训练或Evolve接入。 完整实验高成本不复现。

涉及：[memlife](../../../agent-research/2609.40195-memlife/README.md) · [memfolder](../../../agent-research/2611.26427-memfolder/README.md)

**2026-11-21** · 本地实现显式embedding和已ground实体集合上的RecordFolder分组核，包括归一化、DPC/novelty锚点、全窗口方差、IDF亲和、正gain候选、SciPy真正Hungarian和链级重新归组；仅接收按时间排序的输入，最多512条。用总体方差ddof=0、Python round、相同分数按输入顺序、重复embedding的锚点固定保留本组，是论文未完全指定时公开的确定性约定。没有LLM实体提取、实体别名合并、文本合并、ContextFolder、embedding模型或下游问答；调用方负责提供已ground标签和时间顺序，不用词项Jaccard冒充语义embedding。不接收文件路径，不读取Codex会话，也不自动删除或压缩用户文件。 完整实验高成本不复现。

涉及：[memfolder](../../../agent-research/2611.26427-memfolder/README.md) · [memforest](../../../agent-research/2609.08273-memforest/README.md)

**2026-11-20** · 本地实现append-only记录、显式摘要压缩、第一次压缩后的grep准入、正则/分页/上下文/原行号、跳过旧grep输出与字符上限。正则在隔离子进程内运行并用硬timeout终止，仅接收输入文本而不打开路径。摘要由调用方明确提供；没有LLM摘要器、GRPO、问题回答或真实历史接入。只对合成公开观察做控制测试，不读取本机Codex会话，也不把字符串检索当Agent能力。 完整实验高成本不复现。

涉及：[grepmem](../../../agent-research/2611.25123-grepmem/README.md) · [memgpt](../../../agent-research/2310.08560-memgpt/README.md)

**2026-11-18** · 本轮review-only，不提供可执行adapter、metrics或GPU验证，不下载权重／合成语料。只把v1的read/carry/decode、两阶段训练、rank与检索协议记录为可核对方法；把随机初始化hypernetwork跑一次不能算完成记忆巩固。 完整实验高成本不复现，不作能力证据。

涉及：[clam-memory](../../../agent-research/2611.20759-clam-memory/README.md) · [coremem](../../../agent-research/2611.17316-coremem/README.md)

**2026-11-15** · 在继承repo的后续任务上，以同状态有／无记忆rollout估计价值，并将整体价值通过可追踪首次锚点使用门控到步骤。 MemPrice分配上下文容量与记忆保真；CoReMem优化未来编码解决率和工作量。token占用、行为步骤和语义效用不是同一目标，局部算子不产生记忆内容。

涉及：[coremem](../../../agent-research/2611.17316-coremem/README.md) · [memprice](../../../agent-research/2610.24955-memprice/README.md)

**2026-11-13** · 补入policybank历史遗漏，按工具能力存半结构化授权解释，header→ID选择→全文检索，再据外部开发反馈Add/Revise/Omit。 MemGPT解决有限上下文的分层容量与换入换出，PolicyBank解决spec与requirement差异。容量足够不代表规则正确；本地PolicyBank只有L0合同，语义修复仍缺失。

涉及：[policybank](../../../agent-research/2604.15505-policybank/README.md) · [memgpt](../../../agent-research/2310.08560-memgpt/README.md)

**2026-11-11** · 补入证据量感知的广义策略门控和不门控局部冲突通道，区分记忆容量/效用与反馈可靠性；完整API评测高成本不复现。

涉及：[lisa](../../../agent-research/2605.14454-lisa/README.md)

**2026-11-11** · 加入WikiTrace，区分相关性排序与经验来源核查；训练语料冻结、解释不等于事实、源轨迹不可改写。CPU链接/只读诊断不代表编译或任务求解能力，完整多臂rollout不复现。

涉及：[wikitrace](../../../agent-research/2611.14320-wikitrace/README.md) · [memfit](../../../agent-research/2610.00872-memfit/README.md)

**2026-11-09** · 加入 ENGRAM：拆解训练准入、候选启用、可验证记忆释放三个决定；区分窗口省预算、减少可检索记录与存储缩减。完整训练不复现。

涉及：[engram-consolidation](../../../agent-research/2611.09472-engram-consolidation/README.md)

**2026-10-30** · 精读EMMA的三层所有权、scope单编辑、overflow与下一尝试exercise义务；与DiscernMem的配对归因和双基线修复验收区分，保留未实现语义服务边界。

涉及：[emma](../../../agent-research/2610.35966-emma/README.md) · [discernmem](../../../agent-research/2610.36652-discernmem/README.md)

**2026-10-29** · DiscernMem把失败先分为记忆使用范围不对和内容缺陷：对同任务、seed、配置做单记忆/无记忆配对重放，再检查修复是否同时守住父记忆与无记忆基线。它补充了简单追加反思的风险控制：团队结果差不能直接归罪某条记忆；新版本也不能继承旧版本已测效果。本地只做这些测量和版本合同，没有LLM修复或重放。

涉及：[discernmem](../../../agent-research/2610.36652-discernmem/README.md)

**2026-10-27** · 首版：比较分层存储、记忆价格、随机曝光效用、成功程序积累、预提交准入与下游技能信用。

覆盖 55 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 66 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Cache Engineering for Agents](../../../agent-research/2610.28577-cache-engineering/README.md)
- [Remembering Has a Price: Learning Memory Worth under Resource Constraints](../../../agent-research/2610.26453-tokenworth/README.md)
- [MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents](../../../agent-research/2610.24955-memprice/README.md)
- [MemoProAgent: Toward Memory-Driven Proactive Assistance](../../../agent-research/2610.22671-proper-agent/README.md)
- [MemScope: Evolving Agent Memory Architectures through Localized Code Repair](../../../agent-research/2610.21170-memscope/README.md)
- [Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing](../../../agent-research/2610.22196-hy-memory/README.md)
- [Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents](../../../agent-research/2610.20116-transparent-compact/README.md)
- [Recursive Formation and First-Class Reuse of Compositional Capabilities](../../../agent-research/2610.19414-formcraft/README.md)
- [Test-Time Memory Construction](../../../reproductions/2610.13348-t2mem/README.md)
- [NEAR: Neighborhood-Aware Residuals for Memory Retrieval](../../../reproductions/2610.13314-near/README.md)
- [Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence](../../../reproductions/2610.13277-beyond-final-embedding/README.md)
- [Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents](../../../agent-research/2610.12124-hippocam/README.md)
- [Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents](../../../agent-research/2610.02002-mem-plus-plus/README.md)
- [Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval](../../../agent-research/2610.02070-causal-memory-policy/README.md)
- [Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States](../../../agent-research/2610.01415-belief-state-pos/README.md)
- [AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents](../../../agent-research/2610.02163-autocompact/README.md)
- [MemFit: Efficient Long-Term Agentic Memory](../../../agent-research/2610.00872-memfit/README.md)
- [UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval](../../../agent-research/2609.36805-upliftmem/README.md)
- [ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents](../../../agent-research/2609.37311-remem/README.md)
- [Context Language Models](../../../agent-research/2609.37725-context-lm/README.md)
- [Mnemon: Raw Records, Fast Judgments, Slow Thoughts](../../../agent-research/2609.36059-mnemon/README.md)
- [Continuous Context Management](../../../agent-research/2609.35540-ccm/README.md)
- [Interactive Memory Learning for Long-Term Conversations](../../../agent-research/2609.17088-interactive-memory/README.md)
- [Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents](../../../agent-research/2609.17653-evoskill-gui/README.md)
- [When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents](../../../agent-research/2609.10750-skill-retention/README.md)
- [Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents](../../../agent-research/2609.11060-grounded-memory/README.md)
- [MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging](../../../agent-research/2609.08273-memforest/README.md)
- [CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution](../../../agent-research/2609.04865-coskill/README.md)
- [AtomRec: Evolving Atomic Memory for Agentic Recommendation](../../../agent-research/2609.04882-atomrec/README.md)
- [Imagine Before Acting: Prospective Skill Identification for LLM Agents](../../../reproductions/2609.01642-skilldreamer/README.md)
- [SPT: Skills as Pre-Training Data for Agentic Language Models](../../../agent-research/2608.26563-spt/README.md)
- [When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems](../../../agent-research/2608.26895-covemem/README.md)
- [SKILL.state: Scalable Long-Horizon Agent Skills](../../../agent-research/2608.26263-skill-state/README.md)
- [CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval](../../../agent-research/2608.25500-caskg/README.md)
- [SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents](../../../agent-research/2608.24747-skillforge/README.md)
- [HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation](../../../agent-research/2608.15703-hymem/README.md)
- [When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents](../../../agent-research/2608.05810-vag/README.md)
- [Learning Globally Reusable Skills for Coding Agents](../../../agent-research/2608.06153-gse/README.md)
- [MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off](../../../agent-research/2608.04843-memorycpt/README.md)
- [VerMem](../../../agent-research/2608.03137-vermem/README.md)
- [CoEvo-Mem](../../../agent-research/2608.01739-coevo-mem/README.md)
- [SkillRise](../../../agent-research/2607.26784-skillrise/README.md)
- [UniMem](../../../agent-research/2607.26017-unimem/README.md)
- [HiSkill](../../../agent-research/2607.25853-hiskill/README.md)
- [Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents](../../../agent-research/2607.13591-memcon/README.md)
- [Memento-Skills](../../../agent-research/2603.18743-memento-skills/README.md)
- [U-Mem](../../../agent-research/2602.22406-u-mem/README.md)
- [Learning Personalized Agents from Human Feedback](../../../agent-research/2602.16173-pahf/README.md)
- [MemSkill](../../../agent-research/2602.02474-memskill/README.md)
- [SAGE](../../../agent-research/2512.17102-sage/README.md)
- [LEGOMem](../../../agent-research/2510.04851-legomem/README.md)
- [MemTool](../../../agent-research/2507.21428-memtool/README.md)
- [MemGPT](../../../agent-research/2310.08560-memgpt/README.md)
- [Voyager](../../../agent-research/2305.16291-voyager/README.md)
- [Generative Agents](../../../agent-research/2304.03442-generative-agents/README.md)
- [Remembering Is Not Enough: Refining Memories and Learning When to Use Them in Multi-Agent Systems](../../../agent-research/2610.36652-discernmem/README.md)
- [EMMA: Structured Episodic Memory for Multi-Agent Workflow Synthesis](../../../agent-research/2610.35966-emma/README.md)
- [ENGRAM: From Agent Experience to Weights through Verified Consolidation](../../../agent-research/2611.09472-engram-consolidation/README.md)
- [LiSA: Lifelong Safety Adaptation via Conservative Policy Induction](../../../agent-research/2605.14454-lisa/README.md)
- [Don&#x27;t Just Trust Your Memory: Evidence-Linked Memory Reduces Memory-Induced Degradation in LLM Agents](../../../agent-research/2611.14320-wikitrace/README.md)
- [PolicyBank: Evolving Policy Understanding for LLM Agents](../../../agent-research/2604.15505-policybank/README.md)
- [CoReMem: Cost-Internalizing Memory for Successive Coding Tasks with Prospective Valuation](../../../agent-research/2611.17316-coremem/README.md)
- [Instant Weight-Space Consolidation for Long-Term Memory in LLMs](../../../agent-research/2611.20759-clam-memory/README.md)
- [Forget Freely, Grep Later: Lossless, Index-Free Memory for Long-Horizon LLM Agents](../../../agent-research/2611.25123-grepmem/README.md)
- [MemFolder: Structure-Guided Memory Folding for Efficient Agent Memory Management](../../../agent-research/2611.26427-memfolder/README.md)
- [MemLife: Curating and Reasoning over Long-Term Egocentric Video Memories](../../../agent-research/2609.40195-memlife/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/memory-and-skills.md) · [返回全部精读卡片](../index.md)
