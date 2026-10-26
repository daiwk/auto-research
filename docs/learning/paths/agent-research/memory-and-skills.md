---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 记忆与技能：让经验可取回、可失效

[Agent](index.md) / 子主题导学 · 约 3 分钟 · 55 张论文卡

## 先想一个问题

上下文放不下时，应该保存什么，何时取回，旧经验又如何避免误导新任务？

## 记住这一点

记忆是带写入、检索、更新和淘汰策略的状态系统。MemGPT 通过不同存储层移动信息，让有限窗口按需访问外部归档；Voyager 把成功程序积累成可检索技能。事实、临时推断与可执行技能有不同的复用条件：一条事实可能过期，一个程序也可能只适用于特定工具版本。先问未来要做哪个决策，再决定保留何种证据。

## 一个例子

例如跨会话维护一个数据分析项目：常驻区保存用户明确的单位约定，工作区保留当前问题与中间统计，归档区保存完整查询和来源。下周数据表升级时，先核对字段版本，再复用旧查询技能；若用户改了单位，旧约定应被标记失效。把所有历史压成一句“用户喜欢简洁”，不能恢复计算口径。

## 什么时候要小心

压缩后可读不代表关键信息无损，检索命中也不代表适用于当前状态。验证应同时看任务效果、存储/调用预算、错误记忆传播和跨用户隔离。这里的本地分页、技能检索或状态夹具不证明真实长期记忆能力，也不意味着已运行 Minecraft 等原环境。

## 先读这几篇

先读 MemGPT，理解上下文与外部归档的移动；再读 Voyager，把事实记忆与可执行技能分开；最后读 Generative Agents，观察检索、反思与计划如何串联，但不把模拟社会行为当生产证据。

1. [MemGPT](../../../agent-research/2310.08560-memgpt/README.md) · [原论文](https://arxiv.org/abs/2310.08560)
2. [Voyager](../../../agent-research/2305.16291-voyager/README.md) · [原论文](https://arxiv.org/abs/2305.16291)
3. [Generative Agents](../../../agent-research/2304.03442-generative-agents/README.md) · [原论文](https://arxiv.org/abs/2304.03442)

## 自测一下

旧技能曾通过测试，但工具接口刚升级；检索分数最高，能直接执行吗？

??? note "展开参考答案"

    应先检查接口版本、输入假设和权限，再做低成本验证。相似度只解决“像不像”，不保证“现在能不能用”。技能要能记录适用条件、执行反馈与失效原因；无法确认时应回到当前证据，而非把历史成功当作永久保证。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 55 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Cache Engineering for Agents Agent Tsinghua University 2026-10-20 删改早期对话文本会使后续KV失效，重prefill又产生费用。作者保留逻辑文本，直接drop旧工具响应的KV，必要时repos重设保留键的位置；缓存状态取决于操作发生的历史，不能只根据最终token前缀判断是否可复用。AKV基于扩展radix结构管理位置版本、驱逐与恢复，并探索RSI生成缓存策略。§3–4 成本过高，不复现（审查 DONE）。本轮未实现、未运行、未下载模型。本轮未实现、未运行、未下载模型。不提供本地执行命令，不生成GPU收据或虚构指标；上游安装方式请看作者仓库。不能用少量RoPE张量运算冒充已接入AKV系统、真实推理或RSI。  Agent运行时 KV缓存管理与推理效率 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-cache-engineering-55c07860">Cache Engineering for Agents</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>删改早期对话文本会使后续KV失效，重prefill又产生费用。作者保留逻辑文本，直接drop旧工具响应的KV，必要时repos重设保留键的位置；缓存状态取决于操作发生的历史，不能只根据最终token前缀判断是否可复用。AKV基于扩展radix结构管理位置版本、驱逐与恢复，并探索RSI生成缓存策略。§3–4</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。本轮未实现、未运行、未下载模型。本轮未实现、未运行、未下载模型。不提供本地执行命令，不生成GPU收据或虚构指标；上游安装方式请看作者仓库。不能用少量RoPE张量运算冒充已接入AKV系统、真实推理或RSI。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28577">原论文</a> · <a href="../../../../agent-research/2610.28577-cache-engineering/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Remembering Has a Price: Learning Memory Worth under Resource Constraints Agent Nanjing University 2026-10-19 生成长度、交互次数和记忆容量同时受限时，相关记忆也可能浪费稀缺预算。TokenWorth 用四维可解释基础特征学习稳定规律，再用 Recursive Feature Machine（RFM）校正查询相关的非线性残差。快更新拟合残差价值，慢更新调整特征几何；同一个价值模型既用于检索，也用于有界记忆库的写入和淘汰。§4 与附录 B 原论文 Figure 2 展示完整价值学习和记忆生命周期框架；本页重绘与原图分开，原图由统一资源流程归档。 完整实验成本过高，不复现（审查 DONE）；默认使用论文 DB 调度（基础/KRR/AGOP 每 50/50/200 个反馈更新），诊断 runner 为缩短覆盖周期显式用 10/8/24，不能混作官方实验参数。component_only / L1 CPU 数学与时序诊断。学习的是选中记忆关联的执行结果，不是反事实因果贡献，也不是 Agent 能力验证。CPU 组件实际实现 512 维 token/字符 3–5 gram 哈希、Newton、Laplacian KRR、解析梯度与对角 AGOP、FIFO、检索及入库门。哈希函数 SHA256 和 Unicode 分词是明确的本地确定性选择，不声称与未指定细节位级相同。  记忆与长期交互 在线价值学习与有界记忆 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-tokenworth-16bf712f">Remembering Has a Price: Learning Memory Worth under Resource Constraints</h2>
<p class="ar-learning-card__meta">Nanjing University · 论文公开：2026-10-19</p>
<p><strong>方法要点：</strong>生成长度、交互次数和记忆容量同时受限时，相关记忆也可能浪费稀缺预算。TokenWorth 用四维可解释基础特征学习稳定规律，再用 Recursive Feature Machine（RFM）校正查询相关的非线性残差。快更新拟合残差价值，慢更新调整特征几何；同一个价值模型既用于检索，也用于有界记忆库的写入和淘汰。§4 与附录 B 原论文 Figure 2 展示完整价值学习和记忆生命周期框架；本页重绘与原图分开，原图由统一资源流程归档。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；默认使用论文 DB 调度（基础/KRR/AGOP 每 50/50/200 个反馈更新），诊断 runner 为缩短覆盖周期显式用 10/8/24，不能混作官方实验参数。component_only / L1 CPU 数学与时序诊断。学习的是选中记忆关联的执行结果，不是反事实因果贡献，也不是 Agent 能力验证。CPU 组件实际实现 512 维 token/字符 3–5 gram 哈希、Newton、Laplacian KRR、解析梯度与对角 AGOP、FIFO、检索及入库门。哈希函数 SHA256 和 Unicode 分词是明确的本地确定性选择，不声称与未指定细节位级相同。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26453">原论文</a> · <a href="../../../../agent-research/2610.26453-tokenworth/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents Agent Hong Kong University of Science and Technology 2026-10-18 长交互里，过去某个细节会不会有用通常事先未知。单纯按相关性保留记忆会忽略各条信息对同一上下文容量的竞争。MemPrice 给每项记忆提供 raw、summary、abstraction、keywords、delete 五级表示，联合分配有限 token；再用随占用累积的虚拟队列提高保留细节的价格。当前窗口中已经删掉的细节不能凭空恢复，只有刷新时从外部原始归档按固定流程重新提取。§3 与附录 G 原论文 Figure 2 展示记忆分配框架，Algorithm 1 明确刷新不重置队列和全局轮数。 完整实验成本过高，不复现（审查 DONE），不发起 API、模型下载或长轨迹试跑。component_only / L1 CPU 机制诊断。只验证分配和状态更新，不代表长记忆问答或 Agent 能力。CPU 组件真实运行稀疏整数动态规划、效用单调修复、降保真约束、压力更新和刷新跨界状态。token 大小与压缩内容由可信调用方给出，不能把字符数当真实 token。刷新只开放下一轮从归档重新形成的候选，不实现论文的 LLM 压缩/效用模型或 BM25 归档恢复。相同等级的文本是否确实由现有内容压缩而来，也需要上游保证；本地等级检查不能证明语义来源。  记忆与长期交互 多保真分配与资源定价 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-memprice-d97f4c90">MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents</h2>
<p class="ar-learning-card__meta">Hong Kong University of Science and Technology · 论文公开：2026-10-18</p>
<p><strong>方法要点：</strong>长交互里，过去某个细节会不会有用通常事先未知。单纯按相关性保留记忆会忽略各条信息对同一上下文容量的竞争。MemPrice 给每项记忆提供 raw、summary、abstraction、keywords、delete 五级表示，联合分配有限 token；再用随占用累积的虚拟队列提高保留细节的价格。当前窗口中已经删掉的细节不能凭空恢复，只有刷新时从外部原始归档按固定流程重新提取。§3 与附录 G 原论文 Figure 2 展示记忆分配框架，Algorithm 1 明确刷新不重置队列和全局轮数。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE），不发起 API、模型下载或长轨迹试跑。component_only / L1 CPU 机制诊断。只验证分配和状态更新，不代表长记忆问答或 Agent 能力。CPU 组件真实运行稀疏整数动态规划、效用单调修复、降保真约束、压力更新和刷新跨界状态。token 大小与压缩内容由可信调用方给出，不能把字符数当真实 token。刷新只开放下一轮从归档重新形成的候选，不实现论文的 LLM 压缩/效用模型或 BM25 归档恢复。相同等级的文本是否确实由现有内容压缩而来，也需要上游保证；本地等级检查不能证明语义来源。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24955">原论文</a> · <a href="../../../../agent-research/2610.24955-memprice/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing Agent Tencent Hunyuan 2026-10-15 先在学生自己写出的记忆状态上做 OPD，学习不同框架的写入协议；再冻结 reader 和 judge，单独优化 writer。逐块探针补足稀疏奖励，跨块事实归因定位贡献，存储增长惩罚防止“全部记住”。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。模型和框架入口不代表本库完成了30B记忆训练。无可执行 adapter、训练分数或 Evolve 晋级；不把其他记忆算子当成本论文复现。范围见本批验收合同。只做资料收录。§7配置为30B-A3B、128 H20，每批64 windows×8 rollouts；不下载模型、不启动多框架 RL 或服务扫评。成本过高，不复现（审查 DONE）。  长期记忆 Agentic RL On-policy distillation Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-hy-memory-1a0f6bb8">Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing</h2>
<p class="ar-learning-card__meta">Tencent Hunyuan · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>先在学生自己写出的记忆状态上做 OPD，学习不同框架的写入协议；再冻结 reader 和 judge，单独优化 writer。逐块探针补足稀疏奖励，跨块事实归因定位贡献，存储增长惩罚防止“全部记住”。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。模型和框架入口不代表本库完成了30B记忆训练。无可执行 adapter、训练分数或 Evolve 晋级；不把其他记忆算子当成本论文复现。范围见本批验收合同。只做资料收录。§7配置为30B-A3B、128 H20，每批64 windows×8 rollouts；不下载模型、不启动多框架 RL 或服务扫评。成本过高，不复现（审查 DONE）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22196">原论文</a> · <a href="../../../../agent-research/2610.22196-hy-memory/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemScope: Evolving Agent Memory Architectures through Localized Code Repair Agent Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences 2026-10-15 只给“分数下降”或压缩总结，很难知道长链 Agent 该改记忆写入、检索还是下游使用。MemScope 让 Patch Agent 联合检查原始执行轨迹、运行时记忆和当前 provider 代码，定位后做有界原位修改，保留 provider identity 与现有记忆兼容性；证据不足时可以明确 no-patch，而不是每轮都强行修改。原文 §3、附录 A–B 完整实验包含大量 API／工具执行，对现有单卡或 Mac 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现局部代码替换事务和失败回滚，没有语言模型 Patch Agent，也不执行任意代码。每 seed 随机化 provider 中阈值字符串及记忆记录，实际执行成功局部替换、故意失败的兼容性 probe 和签名改变；校验失败 code 回滚、既有 memory 保留及 probe 副作用不持久化。测量的是事务合同，不是阈值调参有效性；CPU 产物保留逐 seed 来源和负对照。  长期记忆 证据驱动的局部架构修复 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-memscope-50996985">MemScope: Evolving Agent Memory Architectures through Localized Code Repair</h2>
<p class="ar-learning-card__meta">Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>只给“分数下降”或压缩总结，很难知道长链 Agent 该改记忆写入、检索还是下游使用。MemScope 让 Patch Agent 联合检查原始执行轨迹、运行时记忆和当前 provider 代码，定位后做有界原位修改，保留 provider identity 与现有记忆兼容性；证据不足时可以明确 no-patch，而不是每轮都强行修改。原文 §3、附录 A–B</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验包含大量 API／工具执行，对现有单卡或 Mac 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现局部代码替换事务和失败回滚，没有语言模型 Patch Agent，也不执行任意代码。每 seed 随机化 provider 中阈值字符串及记忆记录，实际执行成功局部替换、故意失败的兼容性 probe 和签名改变；校验失败 code 回滚、既有 memory 保留及 probe 副作用不持久化。测量的是事务合同，不是阈值调参有效性；CPU 产物保留逐 seed 来源和负对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21170">原论文</a> · <a href="../../../../agent-research/2610.21170-memscope/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoProAgent: Toward Memory-Driven Proactive Assistance Agent Michigan State University 2026-10-15 主动助理没有用户提问：它必须从长期记忆找出干预的依据，并在正确时机只提醒一次。相关记忆不一定意味着应该打断用户。ProPerAgent 用情节—语义图组织记忆，根据当前物体做实体匹配、单跳关联及 Personalized PageRank，再由独立 LLM gate 保留值得干预的证据；生成器结合当前画面与已说过的话，决定发言或静默。训练阶段只优化生成器产生的 token，工具注入的证据 token 不参与策略梯度。方法 §5、附录 I 完整实验成本过高，不复现（审查 DONE）；本地结果为三 seed 的合成机制诊断，不是正式多 seed 能力比较。component_only / L1 CPU 机制诊断。不是已接入 ProPerMem 的视频 Agent，也不是完整 GRPO 复现。本地真实执行事实来源检查、未来时间过滤、归一化实体 embedding、图边/PPR、gate 引用接纳、因果发言序列和联合评分。embedding、事实抽取、语义 gate 与 actor 必须由调用方提供；CPU fixture 的 one-hot 向量和确定性回调只检查接口，不代表任何视觉或语言能力。  记忆与长期交互 主动干预与内容时机联合评测 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-proper-agent-67e59e1f">MemoProAgent: Toward Memory-Driven Proactive Assistance</h2>
<p class="ar-learning-card__meta">Michigan State University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>主动助理没有用户提问：它必须从长期记忆找出干预的依据，并在正确时机只提醒一次。相关记忆不一定意味着应该打断用户。ProPerAgent 用情节—语义图组织记忆，根据当前物体做实体匹配、单跳关联及 Personalized PageRank，再由独立 LLM gate 保留值得干预的证据；生成器结合当前画面与已说过的话，决定发言或静默。训练阶段只优化生成器产生的 token，工具注入的证据 token 不参与策略梯度。方法 §5、附录 I</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）；本地结果为三 seed 的合成机制诊断，不是正式多 seed 能力比较。component_only / L1 CPU 机制诊断。不是已接入 ProPerMem 的视频 Agent，也不是完整 GRPO 复现。本地真实执行事实来源检查、未来时间过滤、归一化实体 embedding、图边/PPR、gate 引用接纳、因果发言序列和联合评分。embedding、事实抽取、语义 gate 与 actor 必须由调用方提供；CPU fixture 的 one-hot 向量和确定性回调只检查接口，不代表任何视觉或语言能力。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22671v2">原论文</a> · <a href="../../../../agent-research/2610.22671-proper-agent/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Recursive Formation and First-Class Reuse of Compositional Capabilities Agent not listed in paper 2026-10-14 一次合成出的能力不应只留下推导历史，而应成为可独立调用、继续组合、持久保存的一等操作。FormCraft 区分三个阶段：类型与接口相容的形成、独立验证后的持久准入、通过相同公开接口直接复用。已形成的复合操作可作为普通候选，后续搜索不用重走其历史形成链，运行时内部计算并未消失。 其 LLM 长轨迹扩展没有公开低成本可核配置，成本过高，不复现（审查 DONE），不以静态 registry label 声称接入 Evolve。本页是从论文独立实现的 CPU 序列域机制与本地固定任务实验，不复制未声明许可的上游源码。不声称复现原论文全部领域、原始目标或 LLM 能力，不进入 Evolve 晋级。本地 local-fixed-sequence-D01-D12-v1 与论文同名 D 编号仅表示深度 1–12，不是作者原始目标文件。原语为整数序列追加 0/1，种子冻结目标后缀。每目标有四个训练样例；Composer 根据样例枚举真实算子链，不能读取目标后缀或 holdout。  可验证能力组合 持久技能与递归复用 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-formcraft-179a4f71">Recursive Formation and First-Class Reuse of Compositional Capabilities</h2>
<p class="ar-learning-card__meta">not listed in paper · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>一次合成出的能力不应只留下推导历史，而应成为可独立调用、继续组合、持久保存的一等操作。FormCraft 区分三个阶段：类型与接口相容的形成、独立验证后的持久准入、通过相同公开接口直接复用。已形成的复合操作可作为普通候选，后续搜索不用重走其历史形成链，运行时内部计算并未消失。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>其 LLM 长轨迹扩展没有公开低成本可核配置，成本过高，不复现（审查 DONE），不以静态 registry label 声称接入 Evolve。本页是从论文独立实现的 CPU 序列域机制与本地固定任务实验，不复制未声明许可的上游源码。不声称复现原论文全部领域、原始目标或 LLM 能力，不进入 Evolve 晋级。本地 local-fixed-sequence-D01-D12-v1 与论文同名 D 编号仅表示深度 1–12，不是作者原始目标文件。原语为整数序列追加 0/1，种子冻结目标后缀。每目标有四个训练样例；Composer 根据样例枚举真实算子链，不能读取目标后缀或 holdout。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19414">原论文</a> · <a href="../../../../agent-research/2610.19414-formcraft/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents Agent Hokkaido University 2026-10-14 长会话压缩通常依赖模型重写摘要，可能丢失只在对话出现的承诺或悄悄改变其措辞。本方法保留用户与助手原话，将思考和工具输出移出活跃上下文，留下明确删减标记，并提供到完整原始会话的恢复路径。压缩不调用模型；论文的 context_lookup 则由模型子代理搜索历史，二者不能混成“零模型完整恢复能力”。 原论文 27B/长上下文（至少 128k）、多臂×多次推理及盲评完整实验超出本轮预算，成本过高，不复现（审查 DONE）。本地实现的是纯 CPU 确定性压缩组件和原始负载恢复索引，不是 Pi 插件逐字节复刻，不是模型记忆能力复现；未调用 LLM，不报告回答准确率，不进入 Evolve 晋级。支持标准消息 JSON 数组及 Pi JSONL。Pi 按 id/parentId 只读取选定叶节点的祖先分支，拒绝缺父、循环和重复 ID，不将兄弟分支混入上下文；不执行会话中的命令。正文保留 Unicode 和换行，未知/非文本块移入可恢复负载。  Agent记忆与上下文 透明压缩与恢复 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-transparent-compact-55d09739">Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents</h2>
<p class="ar-learning-card__meta">Hokkaido University · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>长会话压缩通常依赖模型重写摘要，可能丢失只在对话出现的承诺或悄悄改变其措辞。本方法保留用户与助手原话，将思考和工具输出移出活跃上下文，留下明确删减标记，并提供到完整原始会话的恢复路径。压缩不调用模型；论文的 context_lookup 则由模型子代理搜索历史，二者不能混成“零模型完整恢复能力”。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原论文 27B/长上下文（至少 128k）、多臂×多次推理及盲评完整实验超出本轮预算，成本过高，不复现（审查 DONE）。本地实现的是纯 CPU 确定性压缩组件和原始负载恢复索引，不是 Pi 插件逐字节复刻，不是模型记忆能力复现；未调用 LLM，不报告回答准确率，不进入 Evolve 晋级。支持标准消息 JSON 数组及 Pi JSONL。Pi 按 id/parentId 只读取选定叶节点的祖先分支，拒绝缺父、循环和重复 ID，不将兄弟分支混入上下文；不执行会话中的命令。正文保留 Unicode 和换行，未知/非文本块移入可恢复负载。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20116">原论文</a> · <a href="../../../../agent-research/2610.20116-transparent-compact/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence Agent Southeast University 2026-10-09 最终 pooled embedding 会丢掉局部事实线索，但冻结 embedding encoder 的最后层 token states 已经含有上下文证据。论文保留内容 token（排除 query prefix、special tokens 和 padding），离线给每条 token 绑定原 memory ID。在整个候选 bank 中做全局稀疏 token top-k，再按 ID 聚合回 memory 排名；不是对每条 memory 独立 MaxSim 后排序。 实际 GPU 诊断结果与负结果如下，不能以合同 fixture 代替真实测量。本地对照口径：基线为同冻结 MiniLM 的原生 pooled cosine，实验组为真实 sparse-token fusion 及 source训练的 queryadapter；原文规模相对效果不适用。  memory-retrieval token-level-evidence query-adaptation Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-beyond-final-embedding-06288f14">Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence</h2>
<p class="ar-learning-card__meta">Southeast University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>最终 pooled embedding 会丢掉局部事实线索，但冻结 embedding encoder 的最后层 token states 已经含有上下文证据。论文保留内容 token（排除 query prefix、special tokens 和 padding），离线给每条 token 绑定原 memory ID。在整个候选 bank 中做全局稀疏 token top-k，再按 ID 聚合回 memory 排名；不是对每条 memory 独立 MaxSim 后排序。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>实际 GPU 诊断结果与负结果如下，不能以合同 fixture 代替真实测量。本地对照口径：基线为同冻结 MiniLM 的原生 pooled cosine，实验组为真实 sparse-token fusion 及 source训练的 queryadapter；原文规模相对效果不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13277">原论文</a> · <a href="../../../../reproductions/2610.13277-beyond-final-embedding/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="NEAR: Neighborhood-Aware Residuals for Memory Retrieval Agent Southeast University 2026-10-09 记忆记录往往共享人名、话题和事件。共享内容会让无关证据的整体 embedding 高于真正包含事实的记录。NEAR 将这些近邻从干扰源变成 reference：离线为每条 memory 找近邻均值方向，去掉沿该方向的投影；查询不先检索候选，而从预计算小表得到对应 reference。每层在归一化残差上重新计算邻域，保留原始向量与多层 scoring view。 该旧诊断原样保留。本地对照口径：基线为同冻结 MiniLM 的原生 masked-mean pooled cosine，实验组为 NEAR 邻域残差融合；已执行三 seed，但同一数据切分与相同排名不构成独立数据重复，稳定相对提升结论不适用。  memory-retrieval neighborhood-residual single-index-retrieval Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-near-5f289457">NEAR: Neighborhood-Aware Residuals for Memory Retrieval</h2>
<p class="ar-learning-card__meta">Southeast University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>记忆记录往往共享人名、话题和事件。共享内容会让无关证据的整体 embedding 高于真正包含事实的记录。NEAR 将这些近邻从干扰源变成 reference：离线为每条 memory 找近邻均值方向，去掉沿该方向的投影；查询不先检索候选，而从预计算小表得到对应 reference。每层在归一化残差上重新计算邻域，保留原始向量与多层 scoring view。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>该旧诊断原样保留。本地对照口径：基线为同冻结 MiniLM 的原生 masked-mean pooled cosine，实验组为 NEAR 邻域残差融合；已执行三 seed，但同一数据切分与相同排名不构成独立数据重复，稳定相对提升结论不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13314">原论文</a> · <a href="../../../../reproductions/2610.13314-near/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Test-Time Memory Construction Agent Northeastern University 2026-10-09 离线只提取事件级轻量 metadata 并保留原会话链接。推理时依据查询、已有 memory 与最新 observation 构造 memory cache，再自主选择 SearchMeta、ReadRaw 或 Answer；memory 与信息需求交错演化。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为原文 Naive RAG/structured offline memory；本地未做稳定多seed对照；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  long-term-memory test-time-construction adaptive-retrieval Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-t2mem-26ea91d6">Test-Time Memory Construction</h2>
<p class="ar-learning-card__meta">Northeastern University · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>离线只提取事件级轻量 metadata 并保留原会话链接。推理时依据查询、已有 memory 与最新 observation 构造 memory cache，再自主选择 SearchMeta、ReadRaw 或 Answer；memory 与信息需求交错演化。事实来源：原文全文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为原文 Naive RAG/structured offline memory；本地未做稳定多seed对照；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13348">原论文</a> · <a href="../../../../reproductions/2610.13348-t2mem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents Agent Institute of Information Engineering, Chinese Academy of Sciences 2026-10-08 Janus 在推理前维护嵌套目的，Precip 在主响应后、工具结果前归纳闭合意图。Palim 递归整理早期前缀为叙事和知识，原消息保留为树形子节点；recall 每次返回一层，Agent 自行决定深入。原文 ALFWorld 成功率 97.8%、ScienceWorld 进展 81.9%、StreamBench 平均准确率 81.7%，未报告线上 A/B。 独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。实现意图位置更新、after-response hook、完整工具交换保护、普通/紧急前缀折叠、最小节省/重试、失败保留源文和一层 recall；辅助 checkpoint 真正生成摘要。自主 Janus 未产生闭合时报告 0 次归档；独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。  长期记忆 意图组织 经验学习 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-hippocam-33da2b45">Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents</h2>
<p class="ar-learning-card__meta">Institute of Information Engineering, Chinese Academy of Sciences · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>Janus 在推理前维护嵌套目的，Precip 在主响应后、工具结果前归纳闭合意图。Palim 递归整理早期前缀为叙事和知识，原消息保留为树形子节点；recall 每次返回一层，Agent 自行决定深入。原文 ALFWorld 成功率 97.8%、ScienceWorld 进展 81.9%、StreamBench 平均准确率 81.7%，未报告线上 A/B。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。实现意图位置更新、after-response hook、完整工具交换保护、普通/紧急前缀折叠、最小节省/重试、失败保留源文和一层 recall；辅助 checkpoint 真正生成摘要。自主 Janus 未产生闭合时报告 0 次归档；独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12124">原论文</a> · <a href="../../../../agent-research/2610.12124-hippocam/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents Agent 原文首页未列第一作者机构 2026-10-01 judge 同时审查何时压缩、工作摘要写什么、压缩后下一步怎么做；纠错后的输出直接进入环境，随后以 SFT+结果 RL 联合学习。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Coding Agent 上下文压缩 RL Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-autocompact-45b25080">AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>judge 同时审查何时压缩、工作摘要写什么、压缩后下一步怎么做；纠错后的输出直接进入环境，随后以 SFT+结果 RL 联合学习。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02163">原论文</a> · <a href="../../../../agent-research/2610.02163-autocompact/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States Agent 原文首页未列第一作者机构 2026-10-01 把当前世界事实与尚未解决的任务要求显式维护为 belief；若连续动作没有减少 unresolved requirements，则识别 Belief Trapping 并触发针对性恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 belief 更新与停滞检测；未调用外部工具环境。执行 belief 更新与停滞检测；未调用外部工具环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长程 Agent belief state 恢复 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-belief-state-pos-6f953573">Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>把当前世界事实与尚未解决的任务要求显式维护为 belief；若连续动作没有减少 unresolved requirements，则识别 Belief Trapping 并触发针对性恢复。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 belief 更新与停滞检测；未调用外部工具环境。执行 belief 更新与停滞检测；未调用外部工具环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01415">原论文</a> · <a href="../../../../agent-research/2610.01415-belief-state-pos/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval Agent Illinois Institute of Technology 2026-10-01 被检索到的记忆与任务难度天然相关，直接按任务成败删除记忆存在选择偏差。CMP 在固定候选池中预留均衡随机曝光槽位，使每条记忆都有可估计的处理/对照样本，再用带标准误的效用判断保护不确定的记忆。 尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；L1 因果测量协议：实现均衡随机曝光、Hájek 估计及不确定性感知单 query 决策。不把它夸大为已验证的长期记忆清理策略。尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；合成效用恢复不是 Agent 答题准确率，不进入能力排行榜或 Evolve 晋级证据。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：12 条记忆、600 次检索、每次 2 槽，三 seed 合成外部结果。每条记忆曝光恰好 100 次；产物保留正负效用、标准误及 forget 判断。  因果检索干预 记忆管理 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-causal-memory-policy-919f3b4b">Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval</h2>
<p class="ar-learning-card__meta">Illinois Institute of Technology · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>被检索到的记忆与任务难度天然相关，直接按任务成败删除记忆存在选择偏差。CMP 在固定候选池中预留均衡随机曝光槽位，使每条记忆都有可估计的处理/对照样本，再用带标准误的效用判断保护不确定的记忆。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；L1 因果测量协议：实现均衡随机曝光、Hájek 估计及不确定性感知单 query 决策。不把它夸大为已验证的长期记忆清理策略。尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；合成效用恢复不是 Agent 答题准确率，不进入能力排行榜或 Evolve 晋级证据。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：12 条记忆、600 次检索、每次 2 槽，三 seed 合成外部结果。每条记忆曝光恰好 100 次；产物保留正负效用、标准误及 forget 判断。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02070">原论文</a> · <a href="../../../../agent-research/2610.02070-causal-memory-policy/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents Agent The University of Texas at Austin 2026-10-01 写入时完整保留文档、日期和作者，不调用生成模型做不可逆摘要；读取时先按问题时间过滤，再融合 lexical 与 semantic ranking。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 记忆 时间检索 组织知识 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-mem-plus-plus-c101fe19">Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents</h2>
<p class="ar-learning-card__meta">The University of Texas at Austin · 论文公开：2026-10-01</p>
<p><strong>方法要点：</strong>写入时完整保留文档、日期和作者，不调用生成模型做不可逆摘要；读取时先按问题时间过滤，再融合 lexical 与 semantic ranking。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02002">原论文</a> · <a href="../../../../agent-research/2610.02002-mem-plus-plus/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemFit: Efficient Long-Term Agentic Memory Agent 原文首页未列第一作者机构 2026-09-30 原始 turn 追加写入不改写，只用 segment summary 建索引；读取融合 lexical、semantic 与 rerank 信号，避免昂贵 LLM 写入。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 记忆 无损写入 混合检索 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-memfit-d14853dc">MemFit: Efficient Long-Term Agentic Memory</h2>
<p class="ar-learning-card__meta">原文首页未列第一作者机构 · 论文公开：2026-09-30</p>
<p><strong>方法要点：</strong>原始 turn 追加写入不改写，只用 segment summary 建索引；读取融合 lexical、semantic 与 rerank 信号，避免昂贵 LLM 写入。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00872">原论文</a> · <a href="../../../../agent-research/2610.00872-memfit/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Context Language Models Agent University of Washington / Meta Superintelligence Labs 2026-09-29 把上下文视为模型可直接编辑的文件，使保留、删除和重组信息成为模型行为，而不是外部 harness 的固定策略；多 Agent 各自维护 context file，服务端从第一个不匹配 token 起重新 prefill。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  上下文管理 Agent RL 多 Agent Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-context-lm-ca518f91">Context Language Models</h2>
<p class="ar-learning-card__meta">University of Washington / Meta Superintelligence Labs · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>把上下文视为模型可直接编辑的文件，使保留、删除和重组信息成为模型行为，而不是外部 harness 的固定策略；多 Agent 各自维护 context file，服务端从第一个不匹配 token 起重新 prefill。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37725">原论文</a> · <a href="../../../../agent-research/2609.37725-context-lm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents Agent The Hong Kong Polytechnic University 2026-09-29 推荐 Agent 一方面要从异构商品页稳定提取信息，另一方面不能把完整用户历史无限塞进上下文。ReMem 用 OCR 驱动的多模态 item perception 生成紧凑语义表示，再以固定预算、随时间更新的 dynamic memory 保存偏好；Multi-Memory GRPO 让多个记忆视图共享策略更新。 复现级别：L1 记忆机制。复现级别：L1 记忆机制。实现固定预算的 time-evolving memory 和 multi-memory GRPO 目标；未接入真实购物网页与 OCR 模型。这里不是完整网页 Agent：未运行 OCR、浏览器、作者数据或真实 episode；固定小样本只用于验证信息流，不能宣传为推荐能力提升。  长期记忆 推荐 Agent 多模态感知 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-remem-598e18f2">ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents</h2>
<p class="ar-learning-card__meta">The Hong Kong Polytechnic University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>推荐 Agent 一方面要从异构商品页稳定提取信息，另一方面不能把完整用户历史无限塞进上下文。ReMem 用 OCR 驱动的多模态 item perception 生成紧凑语义表示，再以固定预算、随时间更新的 dynamic memory 保存偏好；Multi-Memory GRPO 让多个记忆视图共享策略更新。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 记忆机制。复现级别：L1 记忆机制。实现固定预算的 time-evolving memory 和 multi-memory GRPO 目标；未接入真实购物网页与 OCR 模型。这里不是完整网页 Agent：未运行 OCR、浏览器、作者数据或真实 episode；固定小样本只用于验证信息流，不能宣传为推荐能力提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37311">原论文</a> · <a href="../../../../agent-research/2609.37311-remem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval Agent Beihang University 2026-09-29 相关记忆不一定提升执行。UpliftMem 以同一冻结 executor 在“使用完整 memory set”和“不使用 memory”时的结果差作为 supervision，并在集合级建模互补、冗余和冲突。候选集合太多无法全跑时，用相关 Gaussian 后验下的 EVSI 把额外 rollout 分配给最可能改变局部检索决策的集合。 复现级别：L1 uplift 与 probe 机制。复现级别：L1 uplift 与 probe 机制。实现同 executor 的 paired uplift 和相关 Gaussian EVSI 选择。本地 set_level_uplift 强制 paired treatment/control；gaussian_evsi 在固定 posterior 上选 probe；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现完整 set constructor、共享 scorer、ALFWorld/WebShop/BigCodeBench 执行器，因此只作为机制与评测基础设施。  Agent 记忆 集合 uplift 主动探测 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-upliftmem-e7065d9f">UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval</h2>
<p class="ar-learning-card__meta">Beihang University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>相关记忆不一定提升执行。UpliftMem 以同一冻结 executor 在“使用完整 memory set”和“不使用 memory”时的结果差作为 supervision，并在集合级建模互补、冗余和冲突。候选集合太多无法全跑时，用相关 Gaussian 后验下的 EVSI 把额外 rollout 分配给最可能改变局部检索决策的集合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：L1 uplift 与 probe 机制。复现级别：L1 uplift 与 probe 机制。实现同 executor 的 paired uplift 和相关 Gaussian EVSI 选择。本地 set_level_uplift 强制 paired treatment/control；gaussian_evsi 在固定 posterior 上选 probe；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现完整 set constructor、共享 scorer、ALFWorld/WebShop/BigCodeBench 执行器，因此只作为机制与评测基础设施。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36805">原论文</a> · <a href="../../../../agent-research/2609.36805-upliftmem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Continuous Context Management Agent University of Miami 2026-09-28 每轮输出动作和更新后的有界 memory；下一轮只读原任务、memory 与最新 observation，并用完整历史只在训练侧提供 privileged distillation。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  上下文管理 Agent RL Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-ccm-d42ba3fe">Continuous Context Management</h2>
<p class="ar-learning-card__meta">University of Miami · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>每轮输出动作和更新后的有界 memory；下一轮只读原任务、memory 与最新 observation，并用完整历史只在训练侧提供 privileged distillation。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35540">原论文</a> · <a href="../../../../agent-research/2609.35540-ccm/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mnemon: Raw Records, Fast Judgments, Slow Thoughts Agent 原文未列机构 2026-09-28 保存原始带日期记录，由慢速规划生成搜索、快速 Jev 判断记录是否需要，再在预算内构造供原回答模型使用的小视图。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  长期记忆 Jev System 1/2 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-mnemon-dd3564ee">Mnemon: Raw Records, Fast Judgments, Slow Thoughts</h2>
<p class="ar-learning-card__meta">原文未列机构 · 论文公开：2026-09-28</p>
<p><strong>方法要点：</strong>保存原始带日期记录，由慢速规划生成搜索、快速 Jev 判断记录是否需要，再在预算内构造供原回答模型使用的小视图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36059">原论文</a> · <a href="../../../../agent-research/2609.36059-mnemon/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents Agent Zhejiang University 2026-09-15 把 GUI 技能拆成可编辑组件，执行失败后由信息隔离 critic 反思，并只修改责任组件，验证后的技能可跨任务复用。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。  GUI Agent 技能进化 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-evoskill-gui-aeb4c952">Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>把 GUI 技能拆成可编辑组件，执行失败后由信息隔离 critic 反思，并只修改责任组件，验证后的技能可跨任务复用。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17653">原论文</a> · <a href="../../../../agent-research/2609.17653-evoskill-gui/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Interactive Memory Learning for Long-Term Conversations Agent Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory 2026-09-15 Planner 决定写入高价值记忆，Trigger 决定何时取回，两者通过跨会话延迟奖励共同演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  长期记忆 多 Agent 强化学习 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-interactive-memory-e350b33d">Interactive Memory Learning for Long-Term Conversations</h2>
<p class="ar-learning-card__meta">Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory · 论文公开：2026-09-15</p>
<p><strong>方法要点：</strong>Planner 决定写入高价值记忆，Trigger 决定何时取回，两者通过跨会话延迟奖励共同演化。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17088">原论文</a> · <a href="../../../../agent-research/2609.17088-interactive-memory/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents Agent Microsoft 2026-09-09 给异步记忆 curator 最小权限只读工具，在写入前验证、限定作用域并刷新候选记忆。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent 记忆 环境探测 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-grounded-memory-32bdf0be">Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents</h2>
<p class="ar-learning-card__meta">Microsoft · 论文公开：2026-09-09</p>
<p><strong>方法要点：</strong>给异步记忆 curator 最小权限只读工具，在写入前验证、限定作用域并刷新候选记忆。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11060">原论文</a> · <a href="../../../../agent-research/2609.11060-grounded-memory/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents Agent Manulife 2026-09-09 混合真实样本 replay 与 embedding anchor/LwF 类正则，防止合成技能数据微调破坏真实和 OOD 路由能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能检索 灾难性遗忘 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-skill-retention-6ccb63cf">When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents</h2>
<p class="ar-learning-card__meta">Manulife · 论文公开：2026-09-09</p>
<p><strong>方法要点：</strong>混合真实样本 replay 与 embedding anchor/LwF 类正则，防止合成技能数据微调破坏真实和 OOD 路由能力。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10750">原论文</a> · <a href="../../../../agent-research/2609.10750-skill-retention/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging Agent Shanghai Jiao Tong University 2026-09-08 MemForest 不把全部历史压进一条摘要，而是先按事件切分成多棵树，再在容量压力下渐进合并节点。查询从语义 anchor 出发向邻域传播，保留时间结构和跨事件关联。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现事件分区、渐进合并与 anchor 邻域检索；语义相似度用词项重叠近似。三种子结果见 metrics/mini-suite-seeds42-44.json。本地 EventTree 是紧凑 CPU 数据结构，使用 token Jaccard 选择树并真实执行压缩；未运行作者 embedding、LLM 摘要器或长程 benchmark。  事件树记忆压缩 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-memforest-6306606d">MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging</h2>
<p class="ar-learning-card__meta">Shanghai Jiao Tong University · 论文公开：2026-09-08</p>
<p><strong>方法要点：</strong>MemForest 不把全部历史压进一条摘要，而是先按事件切分成多棵树，再在容量压力下渐进合并节点。查询从语义 anchor 出发向邻域传播，保留时间结构和跨事件关联。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现事件分区、渐进合并与 anchor 邻域检索；语义相似度用词项重叠近似。三种子结果见 metrics/mini-suite-seeds42-44.json。本地 EventTree 是紧凑 CPU 数据结构，使用 token Jaccard 选择树并真实执行压缩；未运行作者 embedding、LLM 摘要器或长程 benchmark。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08273">原论文</a> · <a href="../../../../agent-research/2609.08273-memforest/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AtomRec: Evolving Atomic Memory for Agentic Recommendation Agent Xi&#x27;an Jiaotong-Liverpool University 2026-09-04 粗粒度用户摘要会在重写时覆盖旧偏好，单一协同边又难以解释推荐。AtomRec 将用户和物品历史拆成可独立演化的原子字段，建立语义协同链接，并以多跳路径取回“为什么推荐”的证据。 复现级别：真实 checkpoint 原子记忆实验。复现级别：真实 checkpoint 原子记忆实验。冻结 Qwen 生成字段、语义链接、历史更新与候选排序，以模型隐状态作本地 encoder；不是原论文线上系统或完整基准复现。未获得原作者代码、提示词和完整实验配置；Qwen 隐状态不是论文的 SentenceT5，Amazon Beauty 也不代表 Xiaohongshu 线上分布。本地不声称复刻原系统或线上实验。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Agentic recommendation memory Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-atomrec-2a7b7ab5">AtomRec: Evolving Atomic Memory for Agentic Recommendation</h2>
<p class="ar-learning-card__meta">Xi&#x27;an Jiaotong-Liverpool University · 论文公开：2026-09-04</p>
<p><strong>方法要点：</strong>粗粒度用户摘要会在重写时覆盖旧偏好，单一协同边又难以解释推荐。AtomRec 将用户和物品历史拆成可独立演化的原子字段，建立语义协同链接，并以多跳路径取回“为什么推荐”的证据。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：真实 checkpoint 原子记忆实验。复现级别：真实 checkpoint 原子记忆实验。冻结 Qwen 生成字段、语义链接、历史更新与候选排序，以模型隐状态作本地 encoder；不是原论文线上系统或完整基准复现。未获得原作者代码、提示词和完整实验配置；Qwen 隐状态不是论文的 SentenceT5，Amazon Beauty 也不代表 Xiaohongshu 线上分布。本地不声称复刻原系统或线上实验。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04882">原论文</a> · <a href="../../../../agent-research/2609.04882-atomrec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution Agent Institute of Automation, Chinese Academy of Sciences 2026-09-04 以往技能库要么与策略优化分离，要么把元技能写成固定工作流。CoSkill 让 Reasoning Agent 使用任务技能及其子步骤技能，让可学习 Meta-Skill Agent 根据执行回报改写技能；二者共享 backbone 并端到端联合训练。 复现级别：公开 checkpoint 训练实验。复现级别：公开 checkpoint 训练实验。Qwen3-4B 的同一末层参数同时接收推理和技能编辑梯度，动作由真实模型生成并交给 ToolRoute 环境执行；不是原论文 ALFWorld/WebShop、VERL 或 7B 训练复现。本地使用 Qwen3-4B 最后一层和自建 ToolRoute，不含论文的离线技能初始化、SentenceT5 子技能检索、ALFWorld/WebShop 或原仓库训练规模，因此不得与论文分数横向比较。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Hierarchical skill coevolution Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-coskill-9fe84c48">CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution</h2>
<p class="ar-learning-card__meta">Institute of Automation, Chinese Academy of Sciences · 论文公开：2026-09-04</p>
<p><strong>方法要点：</strong>以往技能库要么与策略优化分离，要么把元技能写成固定工作流。CoSkill 让 Reasoning Agent 使用任务技能及其子步骤技能，让可学习 Meta-Skill Agent 根据执行回报改写技能；二者共享 backbone 并端到端联合训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开 checkpoint 训练实验。复现级别：公开 checkpoint 训练实验。Qwen3-4B 的同一末层参数同时接收推理和技能编辑梯度，动作由真实模型生成并交给 ToolRoute 环境执行；不是原论文 ALFWorld/WebShop、VERL 或 7B 训练复现。本地使用 Qwen3-4B 最后一层和自建 ToolRoute，不含论文的离线技能初始化、SentenceT5 子技能检索、ALFWorld/WebShop 或原仓库训练规模，因此不得与论文分数横向比较。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04865">原论文</a> · <a href="../../../../agent-research/2609.04865-coskill/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Imagine Before Acting: Prospective Skill Identification for LLM Agents Agent Sichuan University 2026-08-28 任务描述主要说目标，技能文档主要写程序性知识。直接相似度容易优先找到背景相近、但不能解决当前能力缺口的技能；检索到了也未必会在执行时调用。SkillDreamer 在检索和调用两侧显式表达能力需求。PSG 先由 LLM 从任务推断 1–5 个独立 capability 和语义 anchors，再为每个 capability 生成 procedure-like pseudo skill。pseudo skill 只是检索代理，并非验证过的可执行技能。 seed42期间有教师短诊断并存，43/44以两个worker并行；本轮阅读与实现的是 v2 实质修订；v1 首发在 2026-08-28，不计作 2026-10 新 v1。本地保留真实模型 PSG/HSR/CSI，但算术环境只是 live-interaction diagnostic，不冒充 SkillUsage/SkillNet-Gym 能力复现。本地对照口径：基线为同模型 no-skills 与原任务 dense direct retrieval，实验组为真实 PSG/HSR/CSI；缩放算术交互对原 benchmark 的相对能力结论不适用。  skill-retrieval prospective-reasoning capability-aware-invocation Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-skilldreamer-d1e698b9">Imagine Before Acting: Prospective Skill Identification for LLM Agents</h2>
<p class="ar-learning-card__meta">Sichuan University · 论文公开：2026-08-28</p>
<p><strong>方法要点：</strong>任务描述主要说目标，技能文档主要写程序性知识。直接相似度容易优先找到背景相近、但不能解决当前能力缺口的技能；检索到了也未必会在执行时调用。SkillDreamer 在检索和调用两侧显式表达能力需求。PSG 先由 LLM 从任务推断 1–5 个独立 capability 和语义 anchors，再为每个 capability 生成 procedure-like pseudo skill。pseudo skill 只是检索代理，并非验证过的可执行技能。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>seed42期间有教师短诊断并存，43/44以两个worker并行；本轮阅读与实现的是 v2 实质修订；v1 首发在 2026-08-28，不计作 2026-10 新 v1。本地保留真实模型 PSG/HSR/CSI，但算术环境只是 live-interaction diagnostic，不冒充 SkillUsage/SkillNet-Gym 能力复现。本地对照口径：基线为同模型 no-skills 与原任务 dense direct retrieval，实验组为真实 PSG/HSR/CSI；缩放算术交互对原 benchmark 的相对能力结论不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01642">原论文</a> · <a href="../../../../reproductions/2609.01642-skilldreamer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems Agent Shenzhen Technology University 2026-08-27 文本记忆要反复调用 LLM 重写，且丢掉全目录协同几何。CoVeMem 用冻结 LightGCN 状态构造 bank，由当前候选集检索相关历史，投影成 soft token，并通过语义对齐和 masked listwise 联训让 LLM 真正读取记忆。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现候选集检索、向量记忆 bank 和 soft-token read 诊断。未训练 LightGCN/LoRA checkpoint；本地验证候选条件向量读取和零文本重写控制流。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5197。  可训练协同记忆 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-covemem-d06a5714">When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems</h2>
<p class="ar-learning-card__meta">Shenzhen Technology University · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>文本记忆要反复调用 LLM 重写，且丢掉全目录协同几何。CoVeMem 用冻结 LightGCN 状态构造 bank，由当前候选集检索相关历史，投影成 soft token，并通过语义对齐和 masked listwise 联训让 LLM 真正读取记忆。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现候选集检索、向量记忆 bank 和 soft-token read 诊断。未训练 LightGCN/LoRA checkpoint；本地验证候选条件向量读取和零文本重写控制流。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5197。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26895">原论文</a> · <a href="../../../../agent-research/2608.26895-covemem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SPT: Skills as Pre-Training Data for Agentic Language Models Agent Beijing University of Posts and Telecommunications 2026-08-27 Agent 轨迹昂贵且只描述一次执行；skill package 则显式编码可复用工作流。SPT 在 post-training 前对 SkillCorpus 做 causal LM mid-training，并把被引用文件插到主说明的首次引用附近。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现 skill package、Reference Insert 和跨任务技能先验。未训练真实 LLM checkpoint；本地验证多文件引用装配和技能先验对无 oracle 工具路由的影响。ToolRoute-L2.1 三 seed：joint success 0.8056，plan F1 0.8340，平均成本 4.9439。  Agent 技能预训练 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-spt-bfd17eb8">SPT: Skills as Pre-Training Data for Agentic Language Models</h2>
<p class="ar-learning-card__meta">Beijing University of Posts and Telecommunications · 论文公开：2026-08-27</p>
<p><strong>方法要点：</strong>Agent 轨迹昂贵且只描述一次执行；skill package 则显式编码可复用工作流。SPT 在 post-training 前对 SkillCorpus 做 causal LM mid-training，并把被引用文件插到主说明的首次引用附近。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现 skill package、Reference Insert 和跨任务技能先验。未训练真实 LLM checkpoint；本地验证多文件引用装配和技能先验对无 oracle 工具路由的影响。ToolRoute-L2.1 三 seed：joint success 0.8056，plan F1 0.8340，平均成本 4.9439。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26563">原论文</a> · <a href="../../../../agent-research/2608.26563-spt/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval Agent Jilin University / Ant Group 2026-08-26 先从语义、词法、I/O 和结构证据建高召回有向图，再以 remove、substitute、reorder 三类文本反事实探针校准边，Bayesian smoothing 后只发布可靠关系。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。CaSKG 从训练 split 学习可复用 skill 路由，在隔离 test 上结合图式记忆与候选验证调用工具。ToolRoute-L2.1 三 seed 的 joint success 为 0.8000，plan step F1 为 0.8327，平均成本 5.0116。  反事实因果技能图 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-caskg-e0c69536">CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval</h2>
<p class="ar-learning-card__meta">Jilin University / Ant Group · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>先从语义、词法、I/O 和结构证据建高召回有向图，再以 remove、substitute、reorder 三类文本反事实探针校准边，Bayesian smoothing 后只发布可靠关系。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。CaSKG 从训练 split 学习可复用 skill 路由，在隔离 test 上结合图式记忆与候选验证调用工具。ToolRoute-L2.1 三 seed 的 joint success 为 0.8000，plan step F1 为 0.8327，平均成本 5.0116。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25500">原论文</a> · <a href="../../../../agent-research/2608.25500-caskg/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SKILL.state: Scalable Long-Horizon Agent Skills Agent Google 2026-08-26 普通Agent把旧观察、动作和推理反复塞回下一轮。SKILL.state把可持续的信息投影到当前执行状态，每步只传技能说明、状态和最新观察；不是在完整对话外再加一个状态块。模型生成结构化patch和动作，运行时验证后提交，瞬时推理不保留。定义性流程见§3与算法1。 成本过高，不复现（审查 DONE）；actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；运行时实际执行递归合并、null删除、schema拒绝、原状态保留及有界重试。传入actor的是只含三种公共信息的不可变字符串视图，不包含gold、grader、旧回答或旧观察。actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；不是语言模型。  Agent运行时 显式执行状态与上下文控制 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-skill-state-4eba9d90">SKILL.state: Scalable Long-Horizon Agent Skills</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>普通Agent把旧观察、动作和推理反复塞回下一轮。SKILL.state把可持续的信息投影到当前执行状态，每步只传技能说明、状态和最新观察；不是在完整对话外再加一个状态块。模型生成结构化patch和动作，运行时验证后提交，瞬时推理不保留。定义性流程见§3与算法1。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）；actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；运行时实际执行递归合并、null删除、schema拒绝、原状态保留及有界重试。传入actor的是只含三种公共信息的不可变字符串视图，不包含gold、grader、旧回答或旧观察。actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；不是语言模型。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26263">原论文</a> · <a href="../../../../agent-research/2608.26263-skill-state/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents Agent AMAP, Alibaba Group 2026-08-25 SkillRL 类方法从轨迹提取技能后只追加，错误和过时技能会永久污染库。SkillForge 让 policy 输出环境动作时显式选择技能，把调用决策纳入 RL；成功、失败和对比轨迹经多路径 induction 生成候选，环境证据再决定激活、修订或去重。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。技能被显式调用，并根据环境证据更新 posterior 与修订状态。本地用结构化 plan 作为技能内容，执行调用、验证、posterior 与修订控制流；未运行 LLM teacher induction、ALFWorld/WebShop/AppWorld 或 RL 训练。PlanBench-mini 120 episodes：创建 12 个技能、复用 108 次，joint success 1.0000，平均成本 0.6200。  可验证技能锻造 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-skillforge-0aa71f73">SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents</h2>
<p class="ar-learning-card__meta">AMAP, Alibaba Group · 论文公开：2026-08-25</p>
<p><strong>方法要点：</strong>SkillRL 类方法从轨迹提取技能后只追加，错误和过时技能会永久污染库。SkillForge 让 policy 输出环境动作时显式选择技能，把调用决策纳入 RL；成功、失败和对比轨迹经多路径 induction 生成候选，环境证据再决定激活、修订或去重。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。技能被显式调用，并根据环境证据更新 posterior 与修订状态。本地用结构化 plan 作为技能内容，执行调用、验证、posterior 与修订控制流；未运行 LLM teacher induction、ALFWorld/WebShop/AppWorld 或 RL 训练。PlanBench-mini 120 episodes：创建 12 个技能、复用 108 次，joint success 1.0000，平均成本 0.6200。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24747">原论文</a> · <a href="../../../../agent-research/2608.24747-skillforge/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation Agent Institute of Automation, Chinese Academy of Sciences 2026-08-16 把 planning、execution 和 isolated reasoning 分层，结构化摘要在 context refresh 间保存任务进展。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  记忆 长时序 Agent Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-hymem-ebf0c9bb">HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation</h2>
<p class="ar-learning-card__meta">Institute of Automation, Chinese Academy of Sciences · 论文公开：2026-08-16</p>
<p><strong>方法要点：</strong>把 planning、execution 和 isolated reasoning 分层，结构化摘要在 context refresh 间保存任务进展。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.15703">原论文</a> · <a href="../../../../agent-research/2608.15703-hymem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Globally Reusable Skills for Coding Agents Agent Tianjin University 2026-08-06 主题：全局技能进化。GSE 用 Skill Relation Graph 显式维护技能关系，以聚类合并局部经验，并通过 replay verification 防止过拟合与行为回退。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的全局技能进化算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  全局技能进化 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-gse-c467dca4">Learning Globally Reusable Skills for Coding Agents</h2>
<p class="ar-learning-card__meta">Tianjin University · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>主题：全局技能进化。GSE 用 Skill Relation Graph 显式维护技能关系，以聚类合并局部经验，并通过 replay verification 防止过拟合与行为回退。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的全局技能进化算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06153">原论文</a> · <a href="../../../../agent-research/2608.06153-gse/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents Agent 论文未列机构 2026-08-06 主题：技能进化安全。技能一旦进入上下文会污染后代，事后删除无法彻底回滚。VaG 在写入前依次做结构、行为无害性、语义一致性验证，再以边际收益选择可共同使用的 Hot 技能集合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的技能进化安全算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  技能进化安全 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-vag-dfb74800">When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents</h2>
<p class="ar-learning-card__meta">论文未列机构 · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>主题：技能进化安全。技能一旦进入上下文会污染后代，事后删除无法彻底回滚。VaG 在写入前依次做结构、行为无害性、语义一致性验证，再以边际收益选择可共同使用的 Hot 技能集合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的技能进化安全算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05810">原论文</a> · <a href="../../../../agent-research/2608.05810-vag/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off Agent Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS 2026-08-05 主题：端到端 Agent 记忆。QAD 将离线记忆构建链蒸馏为紧凑模型；QAR 用 RRF 检索和 LoRA summarizer 生成查询相关上下文，并以成本感知 GRPO 优化 Quality per Cost。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的端到端 Agent 记忆算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  端到端 Agent 记忆 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-memorycpt-45f8aee7">MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off</h2>
<p class="ar-learning-card__meta">Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS · 论文公开：2026-08-05</p>
<p><strong>方法要点：</strong>主题：端到端 Agent 记忆。QAD 将离线记忆构建链蒸馏为紧凑模型；QAR 用 RRF 检索和 LoRA summarizer 生成查询相关上下文，并以成本感知 GRPO 优化 Quality per Cost。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的端到端 Agent 记忆算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04843">原论文</a> · <a href="../../../../agent-research/2608.04843-memorycpt/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="VerMem Agent Sun Yat-sen University 2026-08-04 长期记忆、活动上下文与 episodic history 往往分开优化，轨迹奖励无法判断单次记忆操作是否正确。VerMem 用一个策略管理三类状态和七种原子操作，以 local verifier 审核状态转移、global verifier 审核证据一致性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。显式维护 LTM、active context、episodes，执行 retrieve/add/restore，并分别计数 local/global verifier。  可验证统一记忆 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-vermem-8bc3a085">VerMem</h2>
<p class="ar-learning-card__meta">Sun Yat-sen University · 论文公开：2026-08-04</p>
<p><strong>方法要点：</strong>长期记忆、活动上下文与 episodic history 往往分开优化，轨迹奖励无法判断单次记忆操作是否正确。VerMem 用一个策略管理三类状态和七种原子操作，以 local verifier 审核状态转移、global verifier 审核证据一致性。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。显式维护 LTM、active context、episodes，执行 retrieve/add/restore，并分别计数 local/global verifier。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03137">原论文</a> · <a href="../../../../agent-research/2608.03137-vermem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoEvo-Mem Agent 论文未列机构 2026-08-03 只优化 query routing 或只更新 memory bank 会忽略二者反馈环。CoEvo-Mem 让冻结 LLM 生成 route-specific rewrite 和 prior，轻量 residual router 在线修正；任务结果更新路由，轨迹反馈更新 memory value 与 graph relation，并交替冻结一侧控制非平稳性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 route rewrite、残差路由与 router/memory bank 交替更新；检索键包含任务轴和工具签名，防止跨任务误复用。  检索—记忆共进化 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-coevo-mem-e947b4e5">CoEvo-Mem</h2>
<p class="ar-learning-card__meta">论文未列机构 · 论文公开：2026-08-03</p>
<p><strong>方法要点：</strong>只优化 query routing 或只更新 memory bank 会忽略二者反馈环。CoEvo-Mem 让冻结 LLM 生成 route-specific rewrite 和 prior，轻量 residual router 在线修正；任务结果更新路由，轨迹反馈更新 memory value 与 graph relation，并交替冻结一侧控制非平稳性。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 route rewrite、残差路由与 router/memory bank 交替更新；检索键包含任务轴和工具签名，防止跨任务误复用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01739">原论文</a> · <a href="../../../../agent-research/2608.01739-coevo-mem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillRise Agent Zhejiang University 2026-07-29 标准 Agent RL 把任务视为独立 episode，外部 skill bank 又把抽取、检索和执行缠在一起。SkillRise 把相关但不同的任务排成由易到难的序列，让同一 policy 交替求解当前任务与整理一个直接传给下一任务的 skill document；求解阶段由当前结果监督，整理阶段由折扣后的下游任务结果监督。 本地验证状态演化与 credit 分离，不训练 Qwen3，也不运行 ALFWorld/WebShop/ScienceWorld；因此不能把 mini-suite 的 100% success 与论文 Pass@k 横向比较。PlanBench mini 按 task axis 组织相关任务；每个 episode 交替执行 solve 和 curate，成功轨迹更新 skill document，并单独记录跨任务复用与下游 credit。  跨任务技能进化 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-skillrise-fa529938">SkillRise</h2>
<p class="ar-learning-card__meta">Zhejiang University · 论文公开：2026-07-29</p>
<p><strong>方法要点：</strong>标准 Agent RL 把任务视为独立 episode，外部 skill bank 又把抽取、检索和执行缠在一起。SkillRise 把相关但不同的任务排成由易到难的序列，让同一 policy 交替求解当前任务与整理一个直接传给下一任务的 skill document；求解阶段由当前结果监督，整理阶段由折扣后的下游任务结果监督。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地验证状态演化与 credit 分离，不训练 Qwen3，也不运行 ALFWorld/WebShop/ScienceWorld；因此不能把 mini-suite 的 100% success 与论文 Pass@k 横向比较。PlanBench mini 按 task axis 组织相关任务；每个 episode 交替执行 solve 和 curate，成功轨迹更新 skill document，并单独记录跨任务复用与下游 credit。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26784">原论文</a> · <a href="../../../../agent-research/2607.26784-skillrise/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HiSkill Agent Beijing University of Posts and Telecommunications 2026-07-28 用高层 skill、可执行 AtomicOp 和多类有向边组织经验，推理时只检索任务相关子图来落地动作。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。图节点来自受控轨迹，不由在线 LLM 抽取；主要验证层次和关系是否改善复用。PlanBench mini-suite 构建高层 skill/AtomicOp 节点及 decomposition、transition、recovery 边，记录子图复用。  Hierarchical skill memory Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-hiskill-6a9652b8">HiSkill</h2>
<p class="ar-learning-card__meta">Beijing University of Posts and Telecommunications · 论文公开：2026-07-28</p>
<p><strong>方法要点：</strong>用高层 skill、可执行 AtomicOp 和多类有向边组织经验，推理时只检索任务相关子图来落地动作。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。图节点来自受控轨迹，不由在线 LLM 抽取；主要验证层次和关系是否改善复用。PlanBench mini-suite 构建高层 skill/AtomicOp 节点及 decomposition、transition、recovery 边，记录子图复用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25853">原论文</a> · <a href="../../../../agent-research/2607.25853-hiskill/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UniMem Agent CASIA 2026-07-28 新颖任务先进入 episodic buffer；反复出现且可靠的执行模式再被自路由控制器固化到可扩展 parametric memory。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。参数记忆是结构化模式表，不是扩展 LLM 权重块；验证稳定性/可塑性路由逻辑。EvoMem mini-suite 实现 episodic route、复现频次阈值、parametric route 和 consolidation 统计。  Continual agent memory Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-unimem-c304c78e">UniMem</h2>
<p class="ar-learning-card__meta">CASIA · 论文公开：2026-07-28</p>
<p><strong>方法要点：</strong>新颖任务先进入 episodic buffer；反复出现且可靠的执行模式再被自路由控制器固化到可扩展 parametric memory。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。参数记忆是结构化模式表，不是扩展 LLM 权重块；验证稳定性/可塑性路由逻辑。EvoMem mini-suite 实现 episodic route、复现频次阈值、parametric route 和 consolidation 统计。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26017">原论文</a> · <a href="../../../../agent-research/2607.26017-unimem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents Agent 未明确标注（正文 HTML 未显示一作机构映射） 2026-07-15 MemCon 将记忆使用拆成一个独立的在线控制问题：根据任务进展、重复动作、记忆规模和已有成功计划，选择检索深度、计划注入、替换查询或记忆维护。控制器用轻量表格 UCB 探索，并从任务结束时的二元反馈及效率奖励学习，不为了选择记忆操作额外调用 LLM。 原六 benchmark、多框架和多 LLM 的端到端比较会产生大量长轨迹推理，成本过高，暂不复现；L1 机制诊断。本轮完成：CPU 核心控制器与真实记忆操作；L1 机制诊断。没有调用 LLM，没有读取任务标准答案或标准计划，不是原论文六个 benchmark 的能力复现，也不作为 evolve 晋级证据。已实现：附录 C 状态/动作、正文 UCB、warm-start、终末奖励、逆序信用、真实 backend 操作、持久化/恢复。本轮核心算法只使用 Python 标准库，CPU 上运行，不下载权重或数据，不增加付费调用。  主动记忆 在线上下文 bandit 记忆维护与计划复用 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-memcon-717a2e37">Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents</h2>
<p class="ar-learning-card__meta">未明确标注（正文 HTML 未显示一作机构映射） · 论文公开：2026-07-15</p>
<p><strong>方法要点：</strong>MemCon 将记忆使用拆成一个独立的在线控制问题：根据任务进展、重复动作、记忆规模和已有成功计划，选择检索深度、计划注入、替换查询或记忆维护。控制器用轻量表格 UCB 探索，并从任务结束时的二元反馈及效率奖励学习，不为了选择记忆操作额外调用 LLM。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原六 benchmark、多框架和多 LLM 的端到端比较会产生大量长轨迹推理，成本过高，暂不复现；L1 机制诊断。本轮完成：CPU 核心控制器与真实记忆操作；L1 机制诊断。没有调用 LLM，没有读取任务标准答案或标准计划，不是原论文六个 benchmark 的能力复现，也不作为 evolve 晋级证据。已实现：附录 C 状态/动作、正文 UCB、warm-start、终末奖励、逆序信用、真实 backend 操作、持久化/恢复。本轮核心算法只使用 Python 标准库，CPU 上运行，不下载权重或数据，不增加付费调用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13591">原论文</a> · <a href="../../../../agent-research/2607.13591-memcon/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memento-Skills Agent Memento Team 2026-03-19 从执行日志反思出结构化技能说明，按任务检索并写回版本化技能，而不是原样堆叠轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 0.0500，average cost 0.2800；方法特有操作有非零 telemetry。  技能设计 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-memento-skills-c4d49bbe">Memento-Skills</h2>
<p class="ar-learning-card__meta">Memento Team · 论文公开：2026-03-19</p>
<p><strong>方法要点：</strong>从执行日志反思出结构化技能说明，按任务检索并写回版本化技能，而不是原样堆叠轨迹。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 0.0500，average cost 0.2800；方法特有操作有非零 telemetry。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.18743">原论文</a> · <a href="../../../../agent-research/2603.18743-memento-skills/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="U-Mem Agent National University of Singapore 2026-02-25 传统 Agent 记忆通常被动写入和检索，缺少“当前知识不够时主动去哪里找”的决策。U-Mem 将获取过程建模为成本递增的级联：先尝试 self/teacher，再做工具研究，最后请求 expert；检索结合语义相似度与 Thompson sampling，并在写回前验证和整理记忆。 保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；当前 mini-suite 不包含论文使用的真实 LLM、HotpotQA 或 AIME 推理。mini-suite 的知识源、专家和验证器都是确定性的，不包含真实搜索 API、模型幻觉或 token 成本。因此这里验证的是主动获取状态机与成本记账，不是 HotpotQA/AIME 分数复刻。evomem-mini 覆盖 episode 内/跨 episode × knowledge/execution 四象限。  主动记忆 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-u-mem-1e639ec3">U-Mem</h2>
<p class="ar-learning-card__meta">National University of Singapore · 论文公开：2026-02-25</p>
<p><strong>方法要点：</strong>传统 Agent 记忆通常被动写入和检索，缺少“当前知识不够时主动去哪里找”的决策。U-Mem 将获取过程建模为成本递增的级联：先尝试 self/teacher，再做工具研究，最后请求 expert；检索结合语义相似度与 Thompson sampling，并在写回前验证和整理记忆。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；当前 mini-suite 不包含论文使用的真实 LLM、HotpotQA 或 AIME 推理。mini-suite 的知识源、专家和验证器都是确定性的，不包含真实搜索 API、模型幻觉或 token 成本。因此这里验证的是主动获取状态机与成本记账，不是 HotpotQA/AIME 分数复刻。evomem-mini 覆盖 episode 内/跨 episode × knowledge/execution 四象限。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22406">原论文</a> · <a href="../../../../agent-research/2602.22406-u-mem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Personalized Agents from Human Feedback Agent Meta Superintelligence Labs / Princeton University（工作完成于 Meta） 2026-02-18 Agent 在行动前从显式用户记忆检索偏好，未知或低置信时主动澄清；行动后无论当前记忆是否自信，都接收纠正并覆盖过期偏好，从而处理新用户、上下文差异和偏好漂移。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。三种子诊断：metrics/mechanism-seeds42-44.json  个性化 Agent 显式记忆 双通道反馈 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-pahf-5582b2a9">Learning Personalized Agents from Human Feedback</h2>
<p class="ar-learning-card__meta">Meta Superintelligence Labs / Princeton University（工作完成于 Meta） · 论文公开：2026-02-18</p>
<p><strong>方法要点：</strong>Agent 在行动前从显式用户记忆检索偏好，未知或低置信时主动澄清；行动后无论当前记忆是否自信，都接收纠正并覆盖过期偏好，从而处理新用户、上下文差异和偏好漂移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。三种子诊断：metrics/mechanism-seeds42-44.json</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16173">原论文</a> · <a href="../../../../agent-research/2602.16173-pahf/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemSkill Agent Nanyang Technological University 2026-02-02 controller 从历史 episode 选择记忆，designer 将重复成功模式编译为技能，并随新反馈升级技能版本。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  记忆技能 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-memskill-ffe2092a">MemSkill</h2>
<p class="ar-learning-card__meta">Nanyang Technological University · 论文公开：2026-02-02</p>
<p><strong>方法要点：</strong>controller 从历史 episode 选择记忆，designer 将重复成功模式编译为技能，并随新反馈升级技能版本。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.02474">原论文</a> · <a href="../../../../agent-research/2602.02474-memskill/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SAGE Agent University of Wisconsin–Madison 2025-12-18 从成功轨迹抽象技能，失败时修订或淘汰，并以任务回报学习技能检索与复用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3000；方法特有操作有非零 telemetry。  技能库强化学习 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-sage-ae754679">SAGE</h2>
<p class="ar-learning-card__meta">University of Wisconsin–Madison · 论文公开：2025-12-18</p>
<p><strong>方法要点：</strong>从成功轨迹抽象技能，失败时修订或淘汰，并以任务回报学习技能检索与复用。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3000；方法特有操作有非零 telemetry。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.17102">原论文</a> · <a href="../../../../agent-research/2512.17102-sage/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="LEGOMem Agent Microsoft Research 2025-10-06 整段成功轨迹难以迁移到新任务，单一全局记忆又混合了任务分解和工具执行。LEGOMem 把经验拆成像积木一样的 procedural units：orchestrator memory 保存任务分解与委派，agent memory 保存具体动作模板，运行时按新任务重新组合。 保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；当前 PlanBench mini 不替代论文的 OfficeBench 多 Agent 环境。当前没有真实 Office 应用、LLM 多 Agent 委派或错误恢复。实现证明过程单元能提取、验证和跨 episode 复用，但不构成 OfficeBench 原始结果的复刻。planbench-mini 使用可验证结构化计划。实现从成功计划提取 action/domain 单元，分别复用高层分解和细粒度动作，并记录 reused_plans。  过程记忆 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-legomem-3e37af3a">LEGOMem</h2>
<p class="ar-learning-card__meta">Microsoft Research · 论文公开：2025-10-06</p>
<p><strong>方法要点：</strong>整段成功轨迹难以迁移到新任务，单一全局记忆又混合了任务分解和工具执行。LEGOMem 把经验拆成像积木一样的 procedural units：orchestrator memory 保存任务分解与委派，agent memory 保存具体动作模板，运行时按新任务重新组合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；当前 PlanBench mini 不替代论文的 OfficeBench 多 Agent 环境。当前没有真实 Office 应用、LLM 多 Agent 委派或错误恢复。实现证明过程单元能提取、验证和跨 episode 复用，但不构成 OfficeBench 原始结果的复刻。planbench-mini 使用可验证结构化计划。实现从成功计划提取 action/domain 单元，分别复用高层分解和细粒度动作，并记录 reused_plans。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04851">原论文</a> · <a href="../../../../agent-research/2510.04851-legomem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemTool Agent PricewaterhouseCoopers Commercial Technology and Innovation Office 2025-07-29 大量 MCP 工具描述会迅速占满上下文，静态截断又可能删掉当前工作流需要的工具。MemTool 比较 autonomous、workflow 和 hybrid 管理方式；hybrid 策略保护当前工作流的必需工具，其余工具依据近期性和历史成功率动态淘汰。 保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；ScaleMCP mini 只验证多轮工具集合管理，不包含 5,000 个真实 MCP server。工具是本地确定性描述，没有真实 MCP 网络延迟、权限失败或模型工具选择误差。结果支持受限上下文的淘汰逻辑与指标链路，不能直接对比论文的 5,000-server 实验。scalemcp-mini 生成连续工具需求，在固定 memory size 下更新保护集合、淘汰非必要工具，并统计 task success、上下文成本和 tool_evictions。  工具记忆 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-memtool-13c64e5c">MemTool</h2>
<p class="ar-learning-card__meta">PricewaterhouseCoopers Commercial Technology and Innovation Office · 论文公开：2025-07-29</p>
<p><strong>方法要点：</strong>大量 MCP 工具描述会迅速占满上下文，静态截断又可能删掉当前工作流需要的工具。MemTool 比较 autonomous、workflow 和 hybrid 管理方式；hybrid 策略保护当前工作流的必需工具，其余工具依据近期性和历史成功率动态淘汰。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；ScaleMCP mini 只验证多轮工具集合管理，不包含 5,000 个真实 MCP server。工具是本地确定性描述，没有真实 MCP 网络延迟、权限失败或模型工具选择误差。结果支持受限上下文的淘汰逻辑与指标链路，不能直接对比论文的 5,000-server 实验。scalemcp-mini 生成连续工具需求，在固定 memory size 下更新保护集合、淘汰非必要工具，并统计 task success、上下文成本和 tool_evictions。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.21428">原论文</a> · <a href="../../../../agent-research/2507.21428-memtool/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemGPT Agent University of California, Berkeley 2023-10-12 有限 context window 使长文档和多轮会话不断遗忘。MemGPT 借鉴操作系统虚拟内存，把常驻核心信息、当前工作上下文和外部归档分层管理；模型通过函数调用移动数据，并以 interrupt/heartbeat 控制继续推理和与用户交互。 本页实现 core、working、archival 三层状态，工作上下文超预算时触发 interrupt、page-out，并在后续任务中 page-in。实现分层状态、换入换出和 interrupt 计数；归档检索使用确定性 key，不调用 embedding 服务或 LLM function calling。成本是统一代理成本，不是 token 或线上延迟。EvoMem mini 120 episodes、seed 42、memory size 24；working tier 使用一半容量，压力触发 page-out，重复任务从 archival tier page-in。  虚拟上下文 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-memgpt-81032c11">MemGPT</h2>
<p class="ar-learning-card__meta">University of California, Berkeley · 论文公开：2023-10-12</p>
<p><strong>方法要点：</strong>有限 context window 使长文档和多轮会话不断遗忘。MemGPT 借鉴操作系统虚拟内存，把常驻核心信息、当前工作上下文和外部归档分层管理；模型通过函数调用移动数据，并以 interrupt/heartbeat 控制继续推理和与用户交互。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页实现 core、working、archival 三层状态，工作上下文超预算时触发 interrupt、page-out，并在后续任务中 page-in。实现分层状态、换入换出和 interrupt 计数；归档检索使用确定性 key，不调用 embedding 服务或 LLM function calling。成本是统一代理成本，不是 token 或线上延迟。EvoMem mini 120 episodes、seed 42、memory size 24；working tier 使用一半容量，压力触发 page-out，重复任务从 archival tier page-in。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.08560">原论文</a> · <a href="../../../../agent-research/2310.08560-memgpt/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Voyager Agent NVIDIA 2023-05-25 开放世界 Agent 需要持续选择有新颖性的任务、把成功行为积累为技能，并根据环境报错修复程序。Voyager 用 GPT-4 自动生成 curriculum，以代码作为动作空间；成功程序按描述索引进 skill library，新任务检索并组合已有技能。 本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。本页实现自动课程入口、执行反馈/自验证，以及可增长、可复用的 executable skill library；不声称在本地复刻 Minecraft 世界。保留 curriculum/skill/verification 三组件和跨 episode 复用；本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。  终身学习 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-voyager-f3989bf0">Voyager</h2>
<p class="ar-learning-card__meta">NVIDIA · 论文公开：2023-05-25</p>
<p><strong>方法要点：</strong>开放世界 Agent 需要持续选择有新颖性的任务、把成功行为积累为技能，并根据环境报错修复程序。Voyager 用 GPT-4 自动生成 curriculum，以代码作为动作空间；成功程序按描述索引进 skill library，新任务检索并组合已有技能。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。本页实现自动课程入口、执行反馈/自验证，以及可增长、可复用的 executable skill library；不声称在本地复刻 Minecraft 世界。保留 curriculum/skill/verification 三组件和跨 episode 复用；本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16291">原论文</a> · <a href="../../../../agent-research/2305.16291-voyager/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Generative Agents Agent Stanford University 2023-04-07 只把完整历史塞给 LLM 无法支撑长期一致行为。论文把每次观察写入 memory stream，按 recency、importance、relevance 检索；累计重要事件达到阈值后生成更高层 reflection，再结合记忆与当前状态制定日程和行动计划。 本页实现 memory stream 的相关性/近期性/重要性检索、累计重要性触发反思，以及用检索记忆生成计划。复现记忆打分、反思触发和计划依赖；没有运行 25 个 LLM persona、Smallville 地图或人类可信度评测，因此这里只比较执行成功率、上下文代理成本和内部状态。EvoMem mini 120 episodes、seed 42、memory size 24，采用三项打分取 top-3，并按累计重要性合成 reflection。  记忆与反思 Agent 记忆与技能：让经验可取回、可失效">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<h2 id="paper-agent-research-generative-agents-beb05f66">Generative Agents</h2>
<p class="ar-learning-card__meta">Stanford University · 论文公开：2023-04-07</p>
<p><strong>方法要点：</strong>只把完整历史塞给 LLM 无法支撑长期一致行为。论文把每次观察写入 memory stream，按 recency、importance、relevance 检索；累计重要事件达到阈值后生成更高层 reflection，再结合记忆与当前状态制定日程和行动计划。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本页实现 memory stream 的相关性/近期性/重要性检索、累计重要性触发反思，以及用检索记忆生成计划。复现记忆打分、反思触发和计划依赖；没有运行 25 个 LLM persona、Smallville 地图或人类可信度评测，因此这里只比较执行成功率、上下文代理成本和内部状态。EvoMem mini 120 episodes、seed 42、memory size 24，采用三项打分取 top-3，并按累计重要性合成 reflection。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.03442">原论文</a> · <a href="../../../../agent-research/2304.03442-generative-agents/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
