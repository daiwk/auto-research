---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 记忆与技能：让经验可取回、可失效

[Agent](index.md) / 55 个问题 · 55 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">55 个问题 · 55 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cache-engineering" data-paper-title="Cache Engineering for Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Cache Engineering for Agents Agent Tsinghua University 2026-10-20 删改早期对话文本会使后续KV失效，重prefill又产生费用。作者保留逻辑文本，直接drop旧工具响应的KV，必要时repos重设保留键的位置；缓存状态取决于操作发生的历史，不能只根据最终token前缀判断是否可复用。AKV基于扩展radix结构管理位置版本、驱逐与恢复，并探索RSI生成缓存策略。§3–4 成本过高，不复现（审查 DONE）。本轮未实现、未运行、未下载模型。本轮未实现、未运行、未下载模型。不提供本地执行命令，不生成GPU收据或虚构指标；上游安装方式请看作者仓库。不能用少量RoPE张量运算冒充已接入AKV系统、真实推理或RSI。  Agent运行时 KV缓存管理与推理效率 Agent 记忆与技能：让经验可取回、可失效 为什么同样的最终文本前缀，也不一定对应可复用的同一份 KV？ KV 取决于计算时可见的历史与位置，drop 发生早晚不同可能已影响后续状态。repos 还要对 RoPE Key 作位置变换，不能只改索引或连 Value 一起旋转；缓存索引因此需要记录位置版本与操作历史，单看逻辑字符串相同不足以证明等价。 例如旧工具响应在生成前被驱逐与生成后才被驱逐，后续 token 曾看到的内容不同，即使最后保留文本一样也不能混用缓存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-cache-engineering-55c07860" class="ar-learning-paper-anchor"></span>
<h2 id="qa-32449a79dfd682e3">为什么同样的最终文本前缀，也不一定对应可复用的同一份 KV？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acache-engineering">Cache Engineering for Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>KV 取决于计算时可见的历史与位置，drop 发生早晚不同可能已影响后续状态。repos 还要对 RoPE Key 作位置变换，不能只改索引或连 Value 一起旋转；缓存索引因此需要记录位置版本与操作历史，单看逻辑字符串相同不足以证明等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧工具响应在生成前被驱逐与生成后才被驱逐，后续 token 曾看到的内容不同，即使最后保留文本一样也不能混用缓存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28577">原论文</a> · <a href="../../../../agent-research/2610.28577-cache-engineering/">实现解读</a> · <a href="#qa-32449a79dfd682e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tokenworth" data-paper-title="Remembering Has a Price: Learning Memory Worth under Resource Constraints" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Remembering Has a Price: Learning Memory Worth under Resource Constraints Agent Nanjing University 2026-10-19 生成长度、交互次数和记忆容量同时受限时，相关记忆也可能浪费稀缺预算。TokenWorth 用四维可解释基础特征学习稳定规律，再用 Recursive Feature Machine（RFM）校正查询相关的非线性残差。快更新拟合残差价值，慢更新调整特征几何；同一个价值模型既用于检索，也用于有界记忆库的写入和淘汰。§4 与附录 B 原论文 Figure 2 展示完整价值学习和记忆生命周期框架；本页重绘与原图分开，原图由统一资源流程归档。 完整实验成本过高，不复现（审查 DONE）；默认使用论文 DB 调度（基础/KRR/AGOP 每 50/50/200 个反馈更新），诊断 runner 为缩短覆盖周期显式用 10/8/24，不能混作官方实验参数。component_only / L1 CPU 数学与时序诊断。学习的是选中记忆关联的执行结果，不是反事实因果贡献，也不是 Agent 能力验证。CPU 组件实际实现 512 维 token/字符 3–5 gram 哈希、Newton、Laplacian KRR、解析梯度与对角 AGOP、FIFO、检索及入库门。哈希函数 SHA256 和 Unicode 分词是明确的本地确定性选择，不声称与未指定细节位级相同。  记忆与长期交互 在线价值学习与有界记忆 Agent 记忆与技能：让经验可取回、可失效 为什么同一个 memory-worth 模型同时控制检索与淘汰，而不只按相似度排序？ 相似记忆也可能冗长、过时或不可靠，预算有限时应比较实际任务价值。稳定基础特征给出可解释方向，RFM 进一步学习查询相关残差，同一价值标尺再用于读取和保留；反馈只应更新真正被选中使用的记忆，不能给未访问条目编造成败标签。 例如两条记忆同样谈某接口，旧文档更相似却已过期，新文档较短且可靠；价值选择可以保留后者而非机械追相似度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-tokenworth-16bf712f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-339227d3e489e486">为什么同一个 memory-worth 模型同时控制检索与淘汰，而不只按相似度排序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atokenworth">Remembering Has a Price: Learning Memory Worth under Resource Constraints</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似记忆也可能冗长、过时或不可靠，预算有限时应比较实际任务价值。稳定基础特征给出可解释方向，RFM 进一步学习查询相关残差，同一价值标尺再用于读取和保留；反馈只应更新真正被选中使用的记忆，不能给未访问条目编造成败标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条记忆同样谈某接口，旧文档更相似却已过期，新文档较短且可靠；价值选择可以保留后者而非机械追相似度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26453">原论文</a> · <a href="../../../../agent-research/2610.26453-tokenworth/">实现解读</a> · <a href="#qa-339227d3e489e486">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memprice" data-paper-title="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents Agent Hong Kong University of Science and Technology 2026-10-18 长交互里，过去某个细节会不会有用通常事先未知。单纯按相关性保留记忆会忽略各条信息对同一上下文容量的竞争。MemPrice 给每项记忆提供 raw、summary、abstraction、keywords、delete 五级表示，联合分配有限 token；再用随占用累积的虚拟队列提高保留细节的价格。当前窗口中已经删掉的细节不能凭空恢复，只有刷新时从外部原始归档按固定流程重新提取。§3 与附录 G 原论文 Figure 2 展示记忆分配框架，Algorithm 1 明确刷新不重置队列和全局轮数。 完整实验成本过高，不复现（审查 DONE），不发起 API、模型下载或长轨迹试跑。component_only / L1 CPU 机制诊断。只验证分配和状态更新，不代表长记忆问答或 Agent 能力。CPU 组件真实运行稀疏整数动态规划、效用单调修复、降保真约束、压力更新和刷新跨界状态。token 大小与压缩内容由可信调用方给出，不能把字符数当真实 token。刷新只开放下一轮从归档重新形成的候选，不实现论文的 LLM 压缩/效用模型或 BM25 归档恢复。相同等级的文本是否确实由现有内容压缩而来，也需要上游保证；本地等级检查不能证明语义来源。  记忆与长期交互 多保真分配与资源定价 Agent 记忆与技能：让经验可取回、可失效 为什么记忆刷新不应该顺便把虚拟队列和全局轮数清零？ 队列承载累计资源压力，轮数决定动态价格的尺度，刷新只是从外部归档重新提取表示。若一起清零，系统会忘记过去长期超额占用，突然把细节重新定价得过便宜；硬容量仍须每轮满足，平均占用目标也不能替代这个即时约束。 例如连续多轮上下文接近满额后，刷新摘要不应让价格突然归零，否则系统又会保留一大批昂贵原文并重复拥塞。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memprice-d97f4c90" class="ar-learning-paper-anchor"></span>
<h2 id="qa-29f54f6e9186beb3">为什么记忆刷新不应该顺便把虚拟队列和全局轮数清零？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemprice">MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>队列承载累计资源压力，轮数决定动态价格的尺度，刷新只是从外部归档重新提取表示。若一起清零，系统会忘记过去长期超额占用，突然把细节重新定价得过便宜；硬容量仍须每轮满足，平均占用目标也不能替代这个即时约束。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如连续多轮上下文接近满额后，刷新摘要不应让价格突然归零，否则系统又会保留一大批昂贵原文并重复拥塞。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24955">原论文</a> · <a href="../../../../agent-research/2610.24955-memprice/">实现解读</a> · <a href="#qa-29f54f6e9186beb3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hy-memory" data-paper-title="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing Agent Tencent Hunyuan 2026-10-15 先在学生自己写出的记忆状态上做 OPD，学习不同框架的写入协议；再冻结 reader 和 judge，单独优化 writer。逐块探针补足稀疏奖励，跨块事实归因定位贡献，存储增长惩罚防止“全部记住”。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。模型和框架入口不代表本库完成了30B记忆训练。无可执行 adapter、训练分数或 Evolve 晋级；不把其他记忆算子当成本论文复现。范围见本批验收合同。只做资料收录。§7配置为30B-A3B、128 H20，每批64 windows×8 rollouts；不下载模型、不启动多框架 RL 或服务扫评。成本过高，不复现（审查 DONE）。  长期记忆 Agentic RL On-policy distillation Agent 记忆与技能：让经验可取回、可失效 冻结 reader 和 judge 后再优化 writer，为什么有助于归因记忆写入的收益？ 读取器和评分器同时变化会混淆“写得更好”与“读得更强”。固定它们后，逐块探针与事实归因更能定位 writer 的贡献，再用存储增长惩罚防止全部保留；同一块每条 rollout 只投一票，不能把更多调用误当成更多独立证据。 例如两版 writer 都交给同一 reader 回答后续问题，差异才更能反映保留了哪些事实，而非一版恰好搭配更强回答模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-hy-memory-1a0f6bb8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4e2c519e59efd8df">冻结 reader 和 judge 后再优化 writer，为什么有助于归因记忆写入的收益？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahy-memory">Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Hunyuan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>读取器和评分器同时变化会混淆“写得更好”与“读得更强”。固定它们后，逐块探针与事实归因更能定位 writer 的贡献，再用存储增长惩罚防止全部保留；同一块每条 rollout 只投一票，不能把更多调用误当成更多独立证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两版 writer 都交给同一 reader 回答后续问题，差异才更能反映保留了哪些事实，而非一版恰好搭配更强回答模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22196">原论文</a> · <a href="../../../../agent-research/2610.22196-hy-memory/">实现解读</a> · <a href="#qa-4e2c519e59efd8df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memscope" data-paper-title="MemScope: Evolving Agent Memory Architectures through Localized Code Repair" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemScope: Evolving Agent Memory Architectures through Localized Code Repair Agent Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences 2026-10-15 只给“分数下降”或压缩总结，很难知道长链 Agent 该改记忆写入、检索还是下游使用。MemScope 让 Patch Agent 联合检查原始执行轨迹、运行时记忆和当前 provider 代码，定位后做有界原位修改，保留 provider identity 与现有记忆兼容性；证据不足时可以明确 no-patch，而不是每轮都强行修改。原文 §3、附录 A–B 完整实验包含大量 API／工具执行，对现有单卡或 Mac 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现局部代码替换事务和失败回滚，没有语言模型 Patch Agent，也不执行任意代码。每 seed 随机化 provider 中阈值字符串及记忆记录，实际执行成功局部替换、故意失败的兼容性 probe 和签名改变；校验失败 code 回滚、既有 memory 保留及 probe 副作用不持久化。测量的是事务合同，不是阈值调参有效性；CPU 产物保留逐 seed 来源和负对照。  长期记忆 证据驱动的局部架构修复 Agent 记忆与技能：让经验可取回、可失效 为什么 memory provider 的签名没变，也不能直接认定补丁兼容旧记忆？ 签名只约束调用形状，内部可能改变字段含义、读取方式或写入语义。MemScope 结合原始轨迹、运行时记忆与代码定位问题，用有界事务修改并运行针对真实格式的 probe；失败需保留原代码和记忆，证据不足时也应允许不打补丁。 例如读取函数参数仍叫 memory，但补丁把时间字段从秒改成天，旧记录就可能被误解；仅通过语法检查看不出这种退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memscope-50996985" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5218d2bd32d78c40">为什么 memory provider 的签名没变，也不能直接认定补丁兼容旧记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemscope">MemScope: Evolving Agent Memory Architectures through Localized Code Repair</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>签名只约束调用形状，内部可能改变字段含义、读取方式或写入语义。MemScope 结合原始轨迹、运行时记忆与代码定位问题，用有界事务修改并运行针对真实格式的 probe；失败需保留原代码和记忆，证据不足时也应允许不打补丁。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如读取函数参数仍叫 memory，但补丁把时间字段从秒改成天，旧记录就可能被误解；仅通过语法检查看不出这种退化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21170">原论文</a> · <a href="../../../../agent-research/2610.21170-memscope/">实现解读</a> · <a href="#qa-5218d2bd32d78c40">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:proper-agent" data-paper-title="MemoProAgent: Toward Memory-Driven Proactive Assistance" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoProAgent: Toward Memory-Driven Proactive Assistance Agent Michigan State University 2026-10-15 主动助理没有用户提问：它必须从长期记忆找出干预的依据，并在正确时机只提醒一次。相关记忆不一定意味着应该打断用户。ProPerAgent 用情节—语义图组织记忆，根据当前物体做实体匹配、单跳关联及 Personalized PageRank，再由独立 LLM gate 保留值得干预的证据；生成器结合当前画面与已说过的话，决定发言或静默。训练阶段只优化生成器产生的 token，工具注入的证据 token 不参与策略梯度。方法 §5、附录 I 完整实验成本过高，不复现（审查 DONE）；本地结果为三 seed 的合成机制诊断，不是正式多 seed 能力比较。component_only / L1 CPU 机制诊断。不是已接入 ProPerMem 的视频 Agent，也不是完整 GRPO 复现。本地真实执行事实来源检查、未来时间过滤、归一化实体 embedding、图边/PPR、gate 引用接纳、因果发言序列和联合评分。embedding、事实抽取、语义 gate 与 actor 必须由调用方提供；CPU fixture 的 one-hot 向量和确定性回调只检查接口，不代表任何视觉或语言能力。  记忆与长期交互 主动干预与内容时机联合评测 Agent 记忆与技能：让经验可取回、可失效 相关记忆已经检索出来，为什么主动助理还需要独立的干预 gate？ 相关性只说明话题相近，不说明现在值得打断用户。gate 判断证据是否构成合适干预，生成器再结合当前画面与已说过的话选择发言或静默；时机和次数都是目标的一部分，迟到或重复提醒不能因为内容正确就算完美成功。 例如记得用户对坚果过敏，但只有看到相关食品且尚未提醒时才有介入理由；反复播放同一句警告会造成错误触发。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-proper-agent-67e59e1f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-045d69d686b724af">相关记忆已经检索出来，为什么主动助理还需要独立的干预 gate？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aproper-agent">MemoProAgent: Toward Memory-Driven Proactive Assistance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Michigan State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相关性只说明话题相近，不说明现在值得打断用户。gate 判断证据是否构成合适干预，生成器再结合当前画面与已说过的话选择发言或静默；时机和次数都是目标的一部分，迟到或重复提醒不能因为内容正确就算完美成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如记得用户对坚果过敏，但只有看到相关食品且尚未提醒时才有介入理由；反复播放同一句警告会造成错误触发。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22671v2">原论文</a> · <a href="../../../../agent-research/2610.22671-proper-agent/">实现解读</a> · <a href="#qa-045d69d686b724af">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:formcraft" data-paper-title="Recursive Formation and First-Class Reuse of Compositional Capabilities" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Recursive Formation and First-Class Reuse of Compositional Capabilities Agent not listed in paper 2026-10-14 一次合成出的能力不应只留下推导历史，而应成为可独立调用、继续组合、持久保存的一等操作。FormCraft 区分三个阶段：类型与接口相容的形成、独立验证后的持久准入、通过相同公开接口直接复用。已形成的复合操作可作为普通候选，后续搜索不用重走其历史形成链，运行时内部计算并未消失。 其 LLM 长轨迹扩展没有公开低成本可核配置，成本过高，不复现（审查 DONE），不以静态 registry label 声称接入 Evolve。本页是从论文独立实现的 CPU 序列域机制与本地固定任务实验，不复制未声明许可的上游源码。不声称复现原论文全部领域、原始目标或 LLM 能力，不进入 Evolve 晋级。本地 local-fixed-sequence-D01-D12-v1 与论文同名 D 编号仅表示深度 1–12，不是作者原始目标文件。原语为整数序列追加 0/1，种子冻结目标后缀。每目标有四个训练样例；Composer 根据样例枚举真实算子链，不能读取目标后缀或 holdout。  可验证能力组合 持久技能与递归复用 Agent 记忆与技能：让经验可取回、可失效 为什么“形成一个复合能力”与“允许它进入持久技能库”要分成两步？ 接口相容只说明操作可以组合，不说明组合满足目标行为。独立验证器确认后才准入，持久身份再绑定父操作、类型和组合方式，加载时检查引用与无环性；之后可直接调用，但内部真实计算并未消失，不能把少搜一次说成零成本执行。 例如把排序再去重组合成新操作，能连起来并不保证处理空输入正确；验证后才保存，之后才能作为一个候选直接复用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-formcraft-179a4f71" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3b8c5d9187005269">为什么“形成一个复合能力”与“允许它进入持久技能库”要分成两步？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aformcraft">Recursive Formation and First-Class Reuse of Compositional Capabilities</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · not listed in paper</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>接口相容只说明操作可以组合，不说明组合满足目标行为。独立验证器确认后才准入，持久身份再绑定父操作、类型和组合方式，加载时检查引用与无环性；之后可直接调用，但内部真实计算并未消失，不能把少搜一次说成零成本执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把排序再去重组合成新操作，能连起来并不保证处理空输入正确；验证后才保存，之后才能作为一个候选直接复用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19414">原论文</a> · <a href="../../../../agent-research/2610.19414-formcraft/">实现解读</a> · <a href="#qa-3b8c5d9187005269">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:transparent-compact" data-paper-title="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents Agent Hokkaido University 2026-10-14 长会话压缩通常依赖模型重写摘要，可能丢失只在对话出现的承诺或悄悄改变其措辞。本方法保留用户与助手原话，将思考和工具输出移出活跃上下文，留下明确删减标记，并提供到完整原始会话的恢复路径。压缩不调用模型；论文的 context_lookup 则由模型子代理搜索历史，二者不能混成“零模型完整恢复能力”。 原论文 27B/长上下文（至少 128k）、多臂×多次推理及盲评完整实验超出本轮预算，成本过高，不复现（审查 DONE）。本地实现的是纯 CPU 确定性压缩组件和原始负载恢复索引，不是 Pi 插件逐字节复刻，不是模型记忆能力复现；未调用 LLM，不报告回答准确率，不进入 Evolve 晋级。支持标准消息 JSON 数组及 Pi JSONL。Pi 按 id/parentId 只读取选定叶节点的祖先分支，拒绝缺父、循环和重复 ID，不将兄弟分支混入上下文；不执行会话中的命令。正文保留 Unicode 和换行，未知/非文本块移入可恢复负载。  Agent记忆与上下文 透明压缩与恢复 Agent 记忆与技能：让经验可取回、可失效 为什么保留原话和删减标记，比重新生成一段流畅摘要更透明？ 原话保留承诺的措辞，删减标记明确告诉模型哪些负载已移出，并提供完整会话的恢复路径。这样压缩不会把推测悄悄改成确定事实；但恢复索引存在不等于模型已经找到证据，历史搜索仍可能需要子代理调用，不能统称零模型成本。 例如用户说“暂时不要部署”，生成摘要若漏掉“暂时”会改变意思；保留原句并标出工具日志被移走更容易审计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-transparent-compact-55d09739" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4625d241bccf4365">为什么保留原话和删减标记，比重新生成一段流畅摘要更透明？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atransparent-compact">Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hokkaido University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原话保留承诺的措辞，删减标记明确告诉模型哪些负载已移出，并提供完整会话的恢复路径。这样压缩不会把推测悄悄改成确定事实；但恢复索引存在不等于模型已经找到证据，历史搜索仍可能需要子代理调用，不能统称零模型成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户说“暂时不要部署”，生成摘要若漏掉“暂时”会改变意思；保留原句并标出工具日志被移走更容易审计。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20116">原论文</a> · <a href="../../../../agent-research/2610.20116-transparent-compact/">实现解读</a> · <a href="#qa-4625d241bccf4365">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:beyond-final-embedding" data-paper-title="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence Agent Southeast University 2026-10-09 最终 pooled embedding 会丢掉局部事实线索，但冻结 embedding encoder 的最后层 token states 已经含有上下文证据。论文保留内容 token（排除 query prefix、special tokens 和 padding），离线给每条 token 绑定原 memory ID。在整个候选 bank 中做全局稀疏 token top-k，再按 ID 聚合回 memory 排名；不是对每条 memory 独立 MaxSim 后排序。 实际 GPU 诊断结果与负结果如下，不能以合同 fixture 代替真实测量。本地对照口径：基线为同冻结 MiniLM 的原生 pooled cosine，实验组为真实 sparse-token fusion 及 source训练的 queryadapter；原文规模相对效果不适用。  memory-retrieval token-level-evidence query-adaptation Agent 记忆与技能：让经验可取回、可失效 全局 token top-k 再按 memory ID 聚合，为什么不同于逐条记忆做 MaxSim？ 全局检索让所有记忆 token 竞争稀疏返回预算，逐条 MaxSim 则对每份记录独立寻找匹配，计算与候选分布都不同。未返回位置还需统一 floor，避免把缺失匹配当成真实零证据；pooled 分支保留整体语义，也让没返回局部 token 的记忆仍可入选。 例如某记录只有一个罕见日期与问题强匹配，全局 token 检索可先找日期再回到记录，不必先让整段 pooled 向量胜出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-beyond-final-embedding-06288f14" class="ar-learning-paper-anchor"></span>
<h2 id="qa-84ba9ade85040011">全局 token top-k 再按 memory ID 聚合，为什么不同于逐条记忆做 MaxSim？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abeyond-final-embedding">Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局检索让所有记忆 token 竞争稀疏返回预算，逐条 MaxSim 则对每份记录独立寻找匹配，计算与候选分布都不同。未返回位置还需统一 floor，避免把缺失匹配当成真实零证据；pooled 分支保留整体语义，也让没返回局部 token 的记忆仍可入选。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某记录只有一个罕见日期与问题强匹配，全局 token 检索可先找日期再回到记录，不必先让整段 pooled 向量胜出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13277">原论文</a> · <a href="../../../../reproductions/2610.13277-beyond-final-embedding/">实现解读</a> · <a href="#qa-84ba9ade85040011">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:near" data-paper-title="NEAR: Neighborhood-Aware Residuals for Memory Retrieval" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="NEAR: Neighborhood-Aware Residuals for Memory Retrieval Agent Southeast University 2026-10-09 记忆记录往往共享人名、话题和事件。共享内容会让无关证据的整体 embedding 高于真正包含事实的记录。NEAR 将这些近邻从干扰源变成 reference：离线为每条 memory 找近邻均值方向，去掉沿该方向的投影；查询不先检索候选，而从预计算小表得到对应 reference。每层在归一化残差上重新计算邻域，保留原始向量与多层 scoring view。 该旧诊断原样保留。本地对照口径：基线为同冻结 MiniLM 的原生 masked-mean pooled cosine，实验组为 NEAR 邻域残差融合；已执行三 seed，但同一数据切分与相同排名不构成独立数据重复，稳定相对提升结论不适用。  memory-retrieval neighborhood-residual single-index-retrieval Agent 记忆与技能：让经验可取回、可失效 减去近邻均值方向为什么可能帮助找到包含独有事实的记忆？ 近邻常共享人名与主题，这些共同分量会让无关记录也很相似。投影去除共享方向后，残差凸显区别性信息；查询用预计算参考表，而非先偷看相关标签确定方向。残差也可能去掉有用共有线索，所以仍保留原始视图并在开发集决定融合方式。 例如两条都提到张三出差，只有一条写周五回程；弱化共同的“张三出差”方向，可让回程事实更容易影响排序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-near-5f289457" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8d0178f13d458596">减去近邻均值方向为什么可能帮助找到包含独有事实的记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Anear">NEAR: Neighborhood-Aware Residuals for Memory Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>近邻常共享人名与主题，这些共同分量会让无关记录也很相似。投影去除共享方向后，残差凸显区别性信息；查询用预计算参考表，而非先偷看相关标签确定方向。残差也可能去掉有用共有线索，所以仍保留原始视图并在开发集决定融合方式。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条都提到张三出差，只有一条写周五回程；弱化共同的“张三出差”方向，可让回程事实更容易影响排序。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13314">原论文</a> · <a href="../../../../reproductions/2610.13314-near/">实现解读</a> · <a href="#qa-8d0178f13d458596">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:t2mem" data-paper-title="Test-Time Memory Construction" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Test-Time Memory Construction Agent Northeastern University 2026-10-09 离线只提取事件级轻量 metadata 并保留原会话链接。推理时依据查询、已有 memory 与最新 observation 构造 memory cache，再自主选择 SearchMeta、ReadRaw 或 Answer；memory 与信息需求交错演化。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为原文 Naive RAG/structured offline memory；本地未做稳定多seed对照；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  long-term-memory test-time-construction adaptive-retrieval Agent 记忆与技能：让经验可取回、可失效 ReadRaw 为什么只允许读取已经观察到的 metadata ID？ 轻量元数据先给出可追溯的事件入口，后续读取原文需要绑定这些实际返回过的身份，避免模型编造链接或跳到未授权记录。记忆随当前问题逐步构建，搜索、精读与回答交错；元数据索引不是一份预先完整理解的记忆，更不能携带最终答案。 例如先搜索到会议事件 M7，再按 M7 读取原对话；模型随口生成 M999 不能直接被当成真实历史证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-t2mem-26ea91d6" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b0c127555f8d8377">ReadRaw 为什么只允许读取已经观察到的 metadata ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3At2mem">Test-Time Memory Construction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轻量元数据先给出可追溯的事件入口，后续读取原文需要绑定这些实际返回过的身份，避免模型编造链接或跳到未授权记录。记忆随当前问题逐步构建，搜索、精读与回答交错；元数据索引不是一份预先完整理解的记忆，更不能携带最终答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先搜索到会议事件 M7，再按 M7 读取原对话；模型随口生成 M999 不能直接被当成真实历史证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13348">原论文</a> · <a href="../../../../reproductions/2610.13348-t2mem/">实现解读</a> · <a href="#qa-b0c127555f8d8377">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hippocam" data-paper-title="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents Agent Institute of Information Engineering, Chinese Academy of Sciences 2026-10-08 Janus 在推理前维护嵌套目的，Precip 在主响应后、工具结果前归纳闭合意图。Palim 递归整理早期前缀为叙事和知识，原消息保留为树形子节点；recall 每次返回一层，Agent 自行决定深入。原文 ALFWorld 成功率 97.8%、ScienceWorld 进展 81.9%、StreamBench 平均准确率 81.7%，未报告线上 A/B。 独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。实现意图位置更新、after-response hook、完整工具交换保护、普通/紧急前缀折叠、最小节省/重试、失败保留源文和一层 recall；辅助 checkpoint 真正生成摘要。自主 Janus 未产生闭合时报告 0 次归档；独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。  长期记忆 意图组织 经验学习 Agent 记忆与技能：让经验可取回、可失效 层次化 recall 为什么一次只返回一层，而不立即展开全部原始历史？ 上层叙事先提供目的与结构，Agent 据当前需要决定是否深入，避免每次召回都重新灌满上下文。原消息保留在子节点，使摘要不是不可逆删除；同时必须给下一轮开销预留容量，若保护的完整交换仍放不下，应明确失败而非静默截断。 例如上层记忆说“上周修复登录问题”，只有需要核对报错时才再展开日志子节点，不必把所有调试输出一并送回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-hippocam-33da2b45" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f958509ffcb6e00a">层次化 recall 为什么一次只返回一层，而不立即展开全部原始历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahippocam">Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>上层叙事先提供目的与结构，Agent 据当前需要决定是否深入，避免每次召回都重新灌满上下文。原消息保留在子节点，使摘要不是不可逆删除；同时必须给下一轮开销预留容量，若保护的完整交换仍放不下，应明确失败而非静默截断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如上层记忆说“上周修复登录问题”，只有需要核对报错时才再展开日志子节点，不必把所有调试输出一并送回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12124">原论文</a> · <a href="../../../../agent-research/2610.12124-hippocam/">实现解读</a> · <a href="#qa-f958509ffcb6e00a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autocompact" data-paper-title="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents Agent 原文首页未列第一作者机构 2026-10-01 judge 同时审查何时压缩、工作摘要写什么、压缩后下一步怎么做；纠错后的输出直接进入环境，随后以 SFT+结果 RL 联合学习。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Coding Agent 上下文压缩 RL Agent 记忆与技能：让经验可取回、可失效 为什么 judge 要把压缩时机、摘要内容和下一步动作放在一起纠错？ 三者相互影响：过早压缩会丢证据，摘要遗漏会诱发错误动作，正确摘要也可能被后续行为浪费。联合纠错后直接把结果放回环境，训练才能看到这套决策的实际后果；仅评价摘要是否流畅，无法判断它对长程编码任务是否足够。 例如马上要修改某接口时，摘要若漏掉参数限制，即使文字清楚也会导致下一步改错；judge 应同时修正记忆和动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-autocompact-45b25080" class="ar-learning-paper-anchor"></span>
<h2 id="qa-93322668d5d24082">为什么 judge 要把压缩时机、摘要内容和下一步动作放在一起纠错？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautocompact">AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>三者相互影响：过早压缩会丢证据，摘要遗漏会诱发错误动作，正确摘要也可能被后续行为浪费。联合纠错后直接把结果放回环境，训练才能看到这套决策的实际后果；仅评价摘要是否流畅，无法判断它对长程编码任务是否足够。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如马上要修改某接口时，摘要若漏掉参数限制，即使文字清楚也会导致下一步改错；judge 应同时修正记忆和动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02163">原论文</a> · <a href="../../../../agent-research/2610.02163-autocompact/">实现解读</a> · <a href="#qa-93322668d5d24082">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:belief-state-pos" data-paper-title="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States Agent 原文首页未列第一作者机构 2026-10-01 把当前世界事实与尚未解决的任务要求显式维护为 belief；若连续动作没有减少 unresolved requirements，则识别 Belief Trapping 并触发针对性恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 belief 更新与停滞检测；未调用外部工具环境。执行 belief 更新与停滞检测；未调用外部工具环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长程 Agent belief state 恢复 Agent 记忆与技能：让经验可取回、可失效 显式 unresolved requirements 为什么比只保存一段历史摘要更容易检测停滞？ 历史摘要描述做过什么，未解决要求则提供任务进度的可比较目标。连续动作若未减少这些要求，就可识别在相似状态间打转，并触发针对缺口的恢复；这不是把动作数当进展，事实与未完成要求也须随真实观察更新，不能凭模型自信划掉。 例如 Agent 重复搜索五次却始终没确认日期，未解决列表仍有“核实日期”，系统就能发现忙碌并未带来目标推进。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-belief-state-pos-6f953573" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cd2d64d0824632e7">显式 unresolved requirements 为什么比只保存一段历史摘要更容易检测停滞？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abelief-state-pos">Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>历史摘要描述做过什么，未解决要求则提供任务进度的可比较目标。连续动作若未减少这些要求，就可识别在相似状态间打转，并触发针对缺口的恢复；这不是把动作数当进展，事实与未完成要求也须随真实观察更新，不能凭模型自信划掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 Agent 重复搜索五次却始终没确认日期，未解决列表仍有“核实日期”，系统就能发现忙碌并未带来目标推进。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01415">原论文</a> · <a href="../../../../agent-research/2610.01415-belief-state-pos/">实现解读</a> · <a href="#qa-cd2d64d0824632e7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:causal-memory-policy" data-paper-title="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval Agent Illinois Institute of Technology 2026-10-01 被检索到的记忆与任务难度天然相关，直接按任务成败删除记忆存在选择偏差。CMP 在固定候选池中预留均衡随机曝光槽位，使每条记忆都有可估计的处理/对照样本，再用带标准误的效用判断保护不确定的记忆。 尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；L1 因果测量协议：实现均衡随机曝光、Hájek 估计及不确定性感知单 query 决策。不把它夸大为已验证的长期记忆清理策略。尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；合成效用恢复不是 Agent 答题准确率，不进入能力排行榜或 Evolve 晋级证据。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：12 条记忆、600 次检索、每次 2 槽，三 seed 合成外部结果。每条记忆曝光恰好 100 次；产物保留正负效用、标准误及 forget 判断。  因果检索干预 记忆管理 Agent 记忆与技能：让经验可取回、可失效 为什么不能因某条记忆经常出现在失败任务中，就直接把它删除？ 困难任务本来更可能检索特定记忆，关联成败含选择偏差。均衡随机曝光为处理和对照提供可比样本，再用标准误保护不确定条目；固定槽位下替换一条也改变其他记忆分布，因此估计的是该设计的净效应，不是孤立记忆的普适加性价值。 例如故障手册总在最难事故中被调用，成功率低可能因为事故难；随机控制曝光后才能判断它是否真的有害。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-causal-memory-policy-919f3b4b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-34b255d1bf60271a">为什么不能因某条记忆经常出现在失败任务中，就直接把它删除？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acausal-memory-policy">Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Illinois Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>困难任务本来更可能检索特定记忆，关联成败含选择偏差。均衡随机曝光为处理和对照提供可比样本，再用标准误保护不确定条目；固定槽位下替换一条也改变其他记忆分布，因此估计的是该设计的净效应，不是孤立记忆的普适加性价值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如故障手册总在最难事故中被调用，成功率低可能因为事故难；随机控制曝光后才能判断它是否真的有害。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02070">原论文</a> · <a href="../../../../agent-research/2610.02070-causal-memory-policy/">实现解读</a> · <a href="#qa-34b255d1bf60271a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mem-plus-plus" data-paper-title="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents Agent The University of Texas at Austin 2026-10-01 写入时完整保留文档、日期和作者，不调用生成模型做不可逆摘要；读取时先按问题时间过滤，再融合 lexical 与 semantic ranking。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 记忆 时间检索 组织知识 Agent 记忆与技能：让经验可取回、可失效 为什么读取时先按问题时间过滤，比事后提醒模型“别用未来信息”更可靠？ 未来文档一旦进入上下文，模型即使被提醒也可能利用其中线索。先做时间资格过滤，让 lexical 与 semantic 排名只作用在当时可见资料上，直接控制信息边界；原文、日期与作者完整保留还支持事后追溯，但不等于检索总能找到正确记录。 例如回答三月时的组织决策，四月公布的调整不能进入候选，即使它与问题高度相似，也不能用于解释当时已知事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-mem-plus-plus-c101fe19" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b68bb4b0178000af">为什么读取时先按问题时间过滤，比事后提醒模型“别用未来信息”更可靠？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amem-plus-plus">Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未来文档一旦进入上下文，模型即使被提醒也可能利用其中线索。先做时间资格过滤，让 lexical 与 semantic 排名只作用在当时可见资料上，直接控制信息边界；原文、日期与作者完整保留还支持事后追溯，但不等于检索总能找到正确记录。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如回答三月时的组织决策，四月公布的调整不能进入候选，即使它与问题高度相似，也不能用于解释当时已知事实。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02002">原论文</a> · <a href="../../../../agent-research/2610.02002-mem-plus-plus/">实现解读</a> · <a href="#qa-b68bb4b0178000af">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memfit" data-paper-title="MemFit: Efficient Long-Term Agentic Memory" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemFit: Efficient Long-Term Agentic Memory Agent 原文首页未列第一作者机构 2026-09-30 原始 turn 追加写入不改写，只用 segment summary 建索引；读取融合 lexical、semantic 与 rerank 信号，避免昂贵 LLM 写入。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 记忆 无损写入 混合检索 Agent 记忆与技能：让经验可取回、可失效 append-only 原始 turn 与可检索 segment summary 为什么要分开保存？ 摘要适合建立紧凑索引，却可能遗漏细节；原始记录不改写，使后续精读仍有可追溯依据。写入不反复调用昂贵模型重构全部历史，读取再融合词法、语义和重排信号；索引命中只是入口，不能把摘要缺失的内容当成从未出现过。 例如摘要只标“讨论支付接口”，搜索后仍能读原始 turn 找到确切超时值；若只保留摘要，该数值就可能不可恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memfit-d14853dc" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b9ff61056b142ab1">append-only 原始 turn 与可检索 segment summary 为什么要分开保存？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemfit">MemFit: Efficient Long-Term Agentic Memory</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>摘要适合建立紧凑索引，却可能遗漏细节；原始记录不改写，使后续精读仍有可追溯依据。写入不反复调用昂贵模型重构全部历史，读取再融合词法、语义和重排信号；索引命中只是入口，不能把摘要缺失的内容当成从未出现过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如摘要只标“讨论支付接口”，搜索后仍能读原始 turn 找到确切超时值；若只保留摘要，该数值就可能不可恢复。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00872">原论文</a> · <a href="../../../../agent-research/2610.00872-memfit/">实现解读</a> · <a href="#qa-b9ff61056b142ab1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:context-lm" data-paper-title="Context Language Models" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Context Language Models Agent University of Washington / Meta Superintelligence Labs 2026-09-29 把上下文视为模型可直接编辑的文件，使保留、删除和重组信息成为模型行为，而不是外部 harness 的固定策略；多 Agent 各自维护 context file，服务端从第一个不匹配 token 起重新 prefill。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  上下文管理 Agent RL 多 Agent Agent 记忆与技能：让经验可取回、可失效 让模型直接编辑 context file，为什么也会改变 KV 复用成本？ 上下文文件的前缀决定已计算缓存是否仍匹配；改动早期 token 后，后缀通常需要重新 prefill。模型因而不仅决定记住什么，还在用文件变换控制后续运行成本；删除更短未必总便宜，若破坏了大量缓存，重算代价也要算入。 例如在文件尾追加新观察可保留已有前缀缓存，若重写开头摘要，则即便总字数更少，也可能需要重算后面的整段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-context-lm-ca518f91" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7eb6f092d33d44b2">让模型直接编辑 context file，为什么也会改变 KV 复用成本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acontext-lm">Context Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington / Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>上下文文件的前缀决定已计算缓存是否仍匹配；改动早期 token 后，后缀通常需要重新 prefill。模型因而不仅决定记住什么，还在用文件变换控制后续运行成本；删除更短未必总便宜，若破坏了大量缓存，重算代价也要算入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如在文件尾追加新观察可保留已有前缀缓存，若重写开头摘要，则即便总字数更少，也可能需要重算后面的整段。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37725">原论文</a> · <a href="../../../../agent-research/2609.37725-context-lm/">实现解读</a> · <a href="#qa-7eb6f092d33d44b2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:remem" data-paper-title="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents Agent The Hong Kong Polytechnic University 2026-09-29 推荐 Agent 一方面要从异构商品页稳定提取信息，另一方面不能把完整用户历史无限塞进上下文。ReMem 用 OCR 驱动的多模态 item perception 生成紧凑语义表示，再以固定预算、随时间更新的 dynamic memory 保存偏好；Multi-Memory GRPO 让多个记忆视图共享策略更新。 复现级别：L1 记忆机制。复现级别：L1 记忆机制。实现固定预算的 time-evolving memory 和 multi-memory GRPO 目标；未接入真实购物网页与 OCR 模型。这里不是完整网页 Agent：未运行 OCR、浏览器、作者数据或真实 episode；固定小样本只用于验证信息流，不能宣传为推荐能力提升。  长期记忆 推荐 Agent 多模态感知 Agent 记忆与技能：让经验可取回、可失效 为什么推荐 Agent 要同时改 item perception 和有界记忆，而不能只把用户历史压短？ 页面信息若提取错误，后续偏好记忆再精巧也只是在保存错误语义。OCR 驱动的感知先形成紧凑 item 表示，动态记忆再在预算内更新用户偏好；多记忆视图共享策略训练，用不同证据视角评价行为，但不应把测试偏好答案注入记忆来制造提升。 例如商品价格藏在图片小字里，单压缩浏览历史无法纠正读错价格；先提取可靠属性，再保留与用户预算有关的信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-remem-598e18f2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-40acc119d72f0bd6">为什么推荐 Agent 要同时改 item perception 和有界记忆，而不能只把用户历史压短？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aremem">ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>页面信息若提取错误，后续偏好记忆再精巧也只是在保存错误语义。OCR 驱动的感知先形成紧凑 item 表示，动态记忆再在预算内更新用户偏好；多记忆视图共享策略训练，用不同证据视角评价行为，但不应把测试偏好答案注入记忆来制造提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如商品价格藏在图片小字里，单压缩浏览历史无法纠正读错价格；先提取可靠属性，再保留与用户预算有关的信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37311">原论文</a> · <a href="../../../../agent-research/2609.37311-remem/">实现解读</a> · <a href="#qa-40acc119d72f0bd6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:upliftmem" data-paper-title="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval Agent Beihang University 2026-09-29 相关记忆不一定提升执行。UpliftMem 以同一冻结 executor 在“使用完整 memory set”和“不使用 memory”时的结果差作为 supervision，并在集合级建模互补、冗余和冲突。候选集合太多无法全跑时，用相关 Gaussian 后验下的 EVSI 把额外 rollout 分配给最可能改变局部检索决策的集合。 复现级别：L1 uplift 与 probe 机制。复现级别：L1 uplift 与 probe 机制。实现同 executor 的 paired uplift 和相关 Gaussian EVSI 选择。本地 set_level_uplift 强制 paired treatment/control；gaussian_evsi 在固定 posterior 上选 probe；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现完整 set constructor、共享 scorer、ALFWorld/WebShop/BigCodeBench 执行器，因此只作为机制与评测基础设施。  Agent 记忆 集合 uplift 主动探测 Agent 记忆与技能：让经验可取回、可失效 为什么 memory set 的效用不能直接等于各条记忆相关性之和？ 条目之间可能互补、重复或冲突，集合整体对执行的影响不是单项分数简单相加。方法用同一冻结 executor 的有记忆与无记忆结果差作监督，额外 rollout 再按能否改变局部选择分配；相关性只是候选线索，不等于实际任务增益。 例如一条给接口名、一条给参数约束，合用才可执行；两份重复接口简介即使都相似，也未必比这组互补证据更有用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-upliftmem-e7065d9f" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9be80c53f396be47">为什么 memory set 的效用不能直接等于各条记忆相关性之和？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aupliftmem">UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>条目之间可能互补、重复或冲突，集合整体对执行的影响不是单项分数简单相加。方法用同一冻结 executor 的有记忆与无记忆结果差作监督，额外 rollout 再按能否改变局部选择分配；相关性只是候选线索，不等于实际任务增益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条给接口名、一条给参数约束，合用才可执行；两份重复接口简介即使都相似，也未必比这组互补证据更有用。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36805">原论文</a> · <a href="../../../../agent-research/2609.36805-upliftmem/">实现解读</a> · <a href="#qa-9be80c53f396be47">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ccm" data-paper-title="Continuous Context Management" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Continuous Context Management Agent University of Miami 2026-09-28 每轮输出动作和更新后的有界 memory；下一轮只读原任务、memory 与最新 observation，并用完整历史只在训练侧提供 privileged distillation。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  上下文管理 Agent RL Agent 记忆与技能：让经验可取回、可失效 训练教师能看完整历史时，为什么学生下一轮仍只能读有界 memory？ 特权历史用于给训练信号，学生部署接口仍受原任务、记忆和最新观察限制，这样才能学会把必要状态写入有限空间。若评测时把完整历史也补给学生，便绕过了连续管理的难题；记忆更新与动作一起输出，意味着保存选择必须服务下一步行为。 例如教师知道早先提过的端口号，学生应把它写入小记忆供后续使用；测试时不能直接把整段旧对话重新塞回来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-ccm-d42ba3fe" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2ae6086f325e6ed3">训练教师能看完整历史时，为什么学生下一轮仍只能读有界 memory？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Accm">Continuous Context Management</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Miami</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>特权历史用于给训练信号，学生部署接口仍受原任务、记忆和最新观察限制，这样才能学会把必要状态写入有限空间。若评测时把完整历史也补给学生，便绕过了连续管理的难题；记忆更新与动作一起输出，意味着保存选择必须服务下一步行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师知道早先提过的端口号，学生应把它写入小记忆供后续使用；测试时不能直接把整段旧对话重新塞回来。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35540">原论文</a> · <a href="../../../../agent-research/2609.35540-ccm/">实现解读</a> · <a href="#qa-2ae6086f325e6ed3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mnemon" data-paper-title="Mnemon: Raw Records, Fast Judgments, Slow Thoughts" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mnemon: Raw Records, Fast Judgments, Slow Thoughts Agent 原文未列机构 2026-09-28 保存原始带日期记录，由慢速规划生成搜索、快速 Jev 判断记录是否需要，再在预算内构造供原回答模型使用的小视图。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  长期记忆 Jev System 1/2 Agent 记忆与技能：让经验可取回、可失效 为什么慢速搜索规划与快速记录判断要拆开，而不是每条记录都长推理？ 搜索规划决定下一步去哪里找证据，逐条资格判断则更适合受限快速决策；分开能把推理预算集中在检索方向，而非重复解释每份候选。原始带日期记录仍保留，最终回答只读预算内小视图；快速判断本身不保证证据完备或时间边界正确。 例如先决定查某次发布会议，再快速筛选几十条记录是否相关，最后把少量原文交给回答器，而不对每条写长篇分析。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-mnemon-dd3564ee" class="ar-learning-paper-anchor"></span>
<h2 id="qa-42c0610048928da3">为什么慢速搜索规划与快速记录判断要拆开，而不是每条记录都长推理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amnemon">Mnemon: Raw Records, Fast Judgments, Slow Thoughts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>搜索规划决定下一步去哪里找证据，逐条资格判断则更适合受限快速决策；分开能把推理预算集中在检索方向，而非重复解释每份候选。原始带日期记录仍保留，最终回答只读预算内小视图；快速判断本身不保证证据完备或时间边界正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先决定查某次发布会议，再快速筛选几十条记录是否相关，最后把少量原文交给回答器，而不对每条写长篇分析。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36059">原论文</a> · <a href="../../../../agent-research/2609.36059-mnemon/">实现解读</a> · <a href="#qa-42c0610048928da3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoskill-gui" data-paper-title="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents Agent Zhejiang University 2026-09-15 把 GUI 技能拆成可编辑组件，执行失败后由信息隔离 critic 反思，并只修改责任组件，验证后的技能可跨任务复用。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。  GUI Agent 技能进化 Agent 记忆与技能：让经验可取回、可失效 失败后只修改责任技能组件，为什么比重新生成整份 GUI 技能更可审计？ 局部修改把失败证据与具体部件关联，保留已验证的其他行为，便于确认改动是否解决原缺陷而非引入大范围漂移。critic 还需信息隔离，不能凭隐藏答案给出神奇补丁；修改后的技能必须再验证，才有理由在其他任务中复用。 例如登录技能只在弹窗关闭步骤失败，应先修正该组件的定位条件，而不把输入用户名、提交等已经可靠的部分一起重写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-evoskill-gui-aeb4c952" class="ar-learning-paper-anchor"></span>
<h2 id="qa-2dd3ecf51946e14e">失败后只修改责任技能组件，为什么比重新生成整份 GUI 技能更可审计？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoskill-gui">Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部修改把失败证据与具体部件关联，保留已验证的其他行为，便于确认改动是否解决原缺陷而非引入大范围漂移。critic 还需信息隔离，不能凭隐藏答案给出神奇补丁；修改后的技能必须再验证，才有理由在其他任务中复用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如登录技能只在弹窗关闭步骤失败，应先修正该组件的定位条件，而不把输入用户名、提交等已经可靠的部分一起重写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17653">原论文</a> · <a href="../../../../agent-research/2609.17653-evoskill-gui/">实现解读</a> · <a href="#qa-2dd3ecf51946e14e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:interactive-memory" data-paper-title="Interactive Memory Learning for Long-Term Conversations" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Interactive Memory Learning for Long-Term Conversations Agent Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory 2026-09-15 Planner 决定写入高价值记忆，Trigger 决定何时取回，两者通过跨会话延迟奖励共同演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  长期记忆 多 Agent 强化学习 Agent 记忆与技能：让经验可取回、可失效 写入 Planner 与读取 Trigger 为什么需要跨会话延迟奖励共同学习？ 有些信息写下时看不出用途，直到后续会话才知道是否值得保存；读取时机又决定这些信息能否真正影响任务。共同延迟奖励连接写入选择和以后取用，避免只奖励当前摘要质量；评估仍须按时间先后，不能用未来问题提前挑选应写内容。 例如今天记下用户换了工作地点，下一周规划通勤才体现价值；若只看当天聊天流畅度，可能永远学不到这条记忆该保存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-interactive-memory-e350b33d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e0579dd9a1ccc407">写入 Planner 与读取 Trigger 为什么需要跨会话延迟奖励共同学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ainteractive-memory">Interactive Memory Learning for Long-Term Conversations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有些信息写下时看不出用途，直到后续会话才知道是否值得保存；读取时机又决定这些信息能否真正影响任务。共同延迟奖励连接写入选择和以后取用，避免只奖励当前摘要质量；评估仍须按时间先后，不能用未来问题提前挑选应写内容。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如今天记下用户换了工作地点，下一周规划通勤才体现价值；若只看当天聊天流畅度，可能永远学不到这条记忆该保存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17088">原论文</a> · <a href="../../../../agent-research/2609.17088-interactive-memory/">实现解读</a> · <a href="#qa-e0579dd9a1ccc407">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:grounded-memory" data-paper-title="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents Agent Microsoft 2026-09-09 给异步记忆 curator 最小权限只读工具，在写入前验证、限定作用域并刷新候选记忆。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent 记忆 环境探测 Agent 记忆与技能：让经验可取回、可失效 记忆 curator 为什么应在写入前用最小权限只读工具探测环境？ 对话里的说法可能过时或只适用于局部环境，先探测能把候选记忆绑定到当前可见事实和作用域。只读最小权限减少整理过程改变被验证对象的机会；验证完成也只是该条件下成立，不能把一次探测提升成永久、跨环境通用的知识。 例如记忆候选说“服务端口是八千”，curator 可只读配置确认并标注环境，不能为让它成立而顺手修改服务配置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-grounded-memory-32bdf0be" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b73212381aeefde5">记忆 curator 为什么应在写入前用最小权限只读工具探测环境？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agrounded-memory">Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对话里的说法可能过时或只适用于局部环境，先探测能把候选记忆绑定到当前可见事实和作用域。只读最小权限减少整理过程改变被验证对象的机会；验证完成也只是该条件下成立，不能把一次探测提升成永久、跨环境通用的知识。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如记忆候选说“服务端口是八千”，curator 可只读配置确认并标注环境，不能为让它成立而顺手修改服务配置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11060">原论文</a> · <a href="../../../../agent-research/2609.11060-grounded-memory/">实现解读</a> · <a href="#qa-b73212381aeefde5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skill-retention" data-paper-title="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents Agent Manulife 2026-09-09 混合真实样本 replay 与 embedding anchor/LwF 类正则，防止合成技能数据微调破坏真实和 OOD 路由能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能检索 灾难性遗忘 Agent 记忆与技能：让经验可取回、可失效 为什么用更多合成技能数据微调，反而可能降低真实任务的技能检索能力？ 合成样本的表述和分布可能与真实请求不同，微调会把 embedding 与路由边界拉向合成模式。真实样本 replay 保留原任务约束，anchor 或旧模型蒸馏限制表示漂移；这些正则保护的是迁移与保留，不代表合成数据越多越好或所有遗忘都会消失。 例如合成任务总把工具名写全，真实用户却用简称；只学合成表达会漏掉真实请求，回放真实简称可保护原有路由。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-skill-retention-6ccb63cf" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b9b020e8d70e745d">为什么用更多合成技能数据微调，反而可能降低真实任务的技能检索能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askill-retention">When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Manulife</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>合成样本的表述和分布可能与真实请求不同，微调会把 embedding 与路由边界拉向合成模式。真实样本 replay 保留原任务约束，anchor 或旧模型蒸馏限制表示漂移；这些正则保护的是迁移与保留，不代表合成数据越多越好或所有遗忘都会消失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如合成任务总把工具名写全，真实用户却用简称；只学合成表达会漏掉真实请求，回放真实简称可保护原有路由。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10750">原论文</a> · <a href="../../../../agent-research/2609.10750-skill-retention/">实现解读</a> · <a href="#qa-b9b020e8d70e745d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memforest" data-paper-title="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging Agent Shanghai Jiao Tong University 2026-09-08 MemForest 不把全部历史压进一条摘要，而是先按事件切分成多棵树，再在容量压力下渐进合并节点。查询从语义 anchor 出发向邻域传播，保留时间结构和跨事件关联。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现事件分区、渐进合并与 anchor 邻域检索；语义相似度用词项重叠近似。三种子结果见 metrics/mini-suite-seeds42-44.json。本地 EventTree 是紧凑 CPU 数据结构，使用 token Jaccard 选择树并真实执行压缩；未运行作者 embedding、LLM 摘要器或长程 benchmark。  事件树记忆压缩 Agent 记忆与技能：让经验可取回、可失效 为什么容量紧张时渐进合并事件树，比持续重写一份总摘要更利于定位证据？ 事件分区保留局部时间与因果结构，容量压力下只合并必要节点，避免每次压缩都搅乱全部历史。查询从语义锚点向邻域传播，还能利用跨事件关联；层次摘要仍可能遗漏细节，因此树结构是控制损失与检索路径，不是无损压缩保证。 例如付款失败和之后退款分属两次事件，树间关联可连接它们；一份反复重写的总摘要可能混淆先后次序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memforest-6306606d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f36339169a34d4f1">为什么容量紧张时渐进合并事件树，比持续重写一份总摘要更利于定位证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemforest">MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>事件分区保留局部时间与因果结构，容量压力下只合并必要节点，避免每次压缩都搅乱全部历史。查询从语义锚点向邻域传播，还能利用跨事件关联；层次摘要仍可能遗漏细节，因此树结构是控制损失与检索路径，不是无损压缩保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如付款失败和之后退款分属两次事件，树间关联可连接它们；一份反复重写的总摘要可能混淆先后次序。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08273">原论文</a> · <a href="../../../../agent-research/2609.08273-memforest/">实现解读</a> · <a href="#qa-f36339169a34d4f1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:atomrec" data-paper-title="AtomRec: Evolving Atomic Memory for Agentic Recommendation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AtomRec: Evolving Atomic Memory for Agentic Recommendation Agent Xi&#x27;an Jiaotong-Liverpool University 2026-09-04 粗粒度用户摘要会在重写时覆盖旧偏好，单一协同边又难以解释推荐。AtomRec 将用户和物品历史拆成可独立演化的原子字段，建立语义协同链接，并以多跳路径取回“为什么推荐”的证据。 复现级别：真实 checkpoint 原子记忆实验。复现级别：真实 checkpoint 原子记忆实验。冻结 Qwen 生成字段、语义链接、历史更新与候选排序，以模型隐状态作本地 encoder；不是原论文线上系统或完整基准复现。未获得原作者代码、提示词和完整实验配置；Qwen 隐状态不是论文的 SentenceT5，Amazon Beauty 也不代表 Xiaohongshu 线上分布。本地不声称复刻原系统或线上实验。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Agentic recommendation memory Agent 记忆与技能：让经验可取回、可失效 把用户画像拆成原子字段，为什么有助于避免新偏好覆盖旧偏好？ 更新只针对命中的事实字段，不必重写整份用户摘要，降低无关信息被顺带删除或改意的风险。语义协同边和多跳路径又把推荐依据连接起来，使可追溯证据与偏好值分开；原子化仍需要处理冲突和时间范围，不能默认旧事实永远有效。 例如用户新增“晚餐不吃辣”，只更新晚餐口味字段，保留通勤预算和早餐偏好，而非让一次摘要重写把它们全部抹掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-atomrec-2a7b7ab5" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8309c3740cf37d71">把用户画像拆成原子字段，为什么有助于避免新偏好覆盖旧偏好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aatomrec">AtomRec: Evolving Atomic Memory for Agentic Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xi&#x27;an Jiaotong-Liverpool University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>更新只针对命中的事实字段，不必重写整份用户摘要，降低无关信息被顺带删除或改意的风险。语义协同边和多跳路径又把推荐依据连接起来，使可追溯证据与偏好值分开；原子化仍需要处理冲突和时间范围，不能默认旧事实永远有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户新增“晚餐不吃辣”，只更新晚餐口味字段，保留通勤预算和早餐偏好，而非让一次摘要重写把它们全部抹掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04882">原论文</a> · <a href="../../../../agent-research/2609.04882-atomrec/">实现解读</a> · <a href="#qa-8309c3740cf37d71">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coskill" data-paper-title="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution Agent Institute of Automation, Chinese Academy of Sciences 2026-09-04 以往技能库要么与策略优化分离，要么把元技能写成固定工作流。CoSkill 让 Reasoning Agent 使用任务技能及其子步骤技能，让可学习 Meta-Skill Agent 根据执行回报改写技能；二者共享 backbone 并端到端联合训练。 复现级别：公开 checkpoint 训练实验。复现级别：公开 checkpoint 训练实验。Qwen3-4B 的同一末层参数同时接收推理和技能编辑梯度，动作由真实模型生成并交给 ToolRoute 环境执行；不是原论文 ALFWorld/WebShop、VERL 或 7B 训练复现。本地使用 Qwen3-4B 最后一层和自建 ToolRoute，不含论文的离线技能初始化、SentenceT5 子技能检索、ALFWorld/WebShop 或原仓库训练规模，因此不得与论文分数横向比较。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Hierarchical skill coevolution Agent 记忆与技能：让经验可取回、可失效 共享团队回报为何能让推理策略和 Meta-Skill 策略一起适配？ 技能内容决定推理可用的程序，推理选择又决定哪些技能得到执行反馈。联合目标把两侧对任务结果的影响连起来，交替更新减少只改库而策略不用、或只改策略却受旧技能限制的问题；共同回报仍不自动解决单次修改的信用归因。 例如原技能步骤过长导致执行失败，Meta-Skill 可压缩步骤，推理 Agent 再学何时调用改版，而不是只把新文档塞进库。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-coskill-9fe84c48" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4f7ee74d56713c41">共享团队回报为何能让推理策略和 Meta-Skill 策略一起适配？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoskill">CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>技能内容决定推理可用的程序，推理选择又决定哪些技能得到执行反馈。联合目标把两侧对任务结果的影响连起来，交替更新减少只改库而策略不用、或只改策略却受旧技能限制的问题；共同回报仍不自动解决单次修改的信用归因。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原技能步骤过长导致执行失败，Meta-Skill 可压缩步骤，推理 Agent 再学何时调用改版，而不是只把新文档塞进库。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04865">原论文</a> · <a href="../../../../agent-research/2609.04865-coskill/">实现解读</a> · <a href="#qa-4f7ee74d56713c41">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skilldreamer" data-paper-title="Imagine Before Acting: Prospective Skill Identification for LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Imagine Before Acting: Prospective Skill Identification for LLM Agents Agent Sichuan University 2026-08-28 任务描述主要说目标，技能文档主要写程序性知识。直接相似度容易优先找到背景相近、但不能解决当前能力缺口的技能；检索到了也未必会在执行时调用。SkillDreamer 在检索和调用两侧显式表达能力需求。PSG 先由 LLM 从任务推断 1–5 个独立 capability 和语义 anchors，再为每个 capability 生成 procedure-like pseudo skill。pseudo skill 只是检索代理，并非验证过的可执行技能。 seed42期间有教师短诊断并存，43/44以两个worker并行；本轮阅读与实现的是 v2 实质修订；v1 首发在 2026-08-28，不计作 2026-10 新 v1。本地保留真实模型 PSG/HSR/CSI，但算术环境只是 live-interaction diagnostic，不冒充 SkillUsage/SkillNet-Gym 能力复现。本地对照口径：基线为同模型 no-skills 与原任务 dense direct retrieval，实验组为真实 PSG/HSR/CSI；缩放算术交互对原 benchmark 的相对能力结论不适用。  skill-retrieval prospective-reasoning capability-aware-invocation Agent 记忆与技能：让经验可取回、可失效 生成 pseudo skill 后，为什么还需要 CSI 在执行前重新判断能力匹配？ 伪技能把任务目标转成程序性检索代理，帮助找到相关文档，但它本身未经过验证，也不保证检索结果适合当前子目标。CSI 再核对证据、限制与下一有界动作，连接“找得到技能”与“实际用对技能”；不能把想象出的步骤当成已可执行能力。 例如伪技能帮助检索到网页下载流程，执行前仍需检查当前网页是否需要登录，不能因文档标题相近就直接套用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-skilldreamer-d1e698b9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-874ddf7bcc58f94f">生成 pseudo skill 后，为什么还需要 CSI 在执行前重新判断能力匹配？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askilldreamer">Imagine Before Acting: Prospective Skill Identification for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sichuan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>伪技能把任务目标转成程序性检索代理，帮助找到相关文档，但它本身未经过验证，也不保证检索结果适合当前子目标。CSI 再核对证据、限制与下一有界动作，连接“找得到技能”与“实际用对技能”；不能把想象出的步骤当成已可执行能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如伪技能帮助检索到网页下载流程，执行前仍需检查当前网页是否需要登录，不能因文档标题相近就直接套用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01642">原论文</a> · <a href="../../../../reproductions/2609.01642-skilldreamer/">实现解读</a> · <a href="#qa-874ddf7bcc58f94f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:covemem" data-paper-title="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems Agent Shenzhen Technology University 2026-08-27 文本记忆要反复调用 LLM 重写，且丢掉全目录协同几何。CoVeMem 用冻结 LightGCN 状态构造 bank，由当前候选集检索相关历史，投影成 soft token，并通过语义对齐和 masked listwise 联训让 LLM 真正读取记忆。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现候选集检索、向量记忆 bank 和 soft-token read 诊断。未训练 LightGCN/LoRA checkpoint；本地验证候选条件向量读取和零文本重写控制流。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5197。  可训练协同记忆 Agent 记忆与技能：让经验可取回、可失效 为什么需要语义对齐和 masked listwise 目标，不能只把 LightGCN 向量塞成 soft tokens？ 投影维度匹配不保证 LLM 会利用协同几何，语义对齐提供接口约束，候选内排序目标再迫使预测读取相关记忆。候选集驱动的检索也让同一用户面对不同选项时取回不同历史；冻结 bank 不意味着连接器无需训练，更不保证文本解释天然忠实。 例如同一用户对电影候选和图书候选需要不同历史子集，soft token 还得通过排序监督学会影响对应候选的分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-covemem-d06a5714" class="ar-learning-paper-anchor"></span>
<h2 id="qa-d1a6536e3ba1db6b">为什么需要语义对齐和 masked listwise 目标，不能只把 LightGCN 向量塞成 soft tokens？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acovemem">When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shenzhen Technology University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>投影维度匹配不保证 LLM 会利用协同几何，语义对齐提供接口约束，候选内排序目标再迫使预测读取相关记忆。候选集驱动的检索也让同一用户面对不同选项时取回不同历史；冻结 bank 不意味着连接器无需训练，更不保证文本解释天然忠实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一用户对电影候选和图书候选需要不同历史子集，soft token 还得通过排序监督学会影响对应候选的分数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26895">原论文</a> · <a href="../../../../agent-research/2608.26895-covemem/">实现解读</a> · <a href="#qa-d1a6536e3ba1db6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spt" data-paper-title="SPT: Skills as Pre-Training Data for Agentic Language Models" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SPT: Skills as Pre-Training Data for Agentic Language Models Agent Beijing University of Posts and Telecommunications 2026-08-27 Agent 轨迹昂贵且只描述一次执行；skill package 则显式编码可复用工作流。SPT 在 post-training 前对 SkillCorpus 做 causal LM mid-training，并把被引用文件插到主说明的首次引用附近。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现 skill package、Reference Insert 和跨任务技能先验。未训练真实 LLM checkpoint；本地验证多文件引用装配和技能先验对无 oracle 工具路由的影响。ToolRoute-L2.1 三 seed：joint success 0.8056，plan F1 0.8340，平均成本 4.9439。  Agent 技能预训练 Agent 记忆与技能：让经验可取回、可失效 把被引用文件插在首次引用附近，为什么比只预训练技能主说明更完整？ 技能往往把参数约束或示例放在配套文件，主说明的引用只是入口。就近展开让因果语言模型在需要的位置看到真实依赖，而非学习悬空引用；与通用语料混合又控制技能训练的分布偏移，不能把读过技能文本等同于执行能力已被验证。 例如说明写“按 schema.json 填参”，若训练只含这句话却没有 schema，模型无法学到字段限制；就近插入可补齐依赖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-spt-bfd17eb8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-40ec6a0c367caa76">把被引用文件插在首次引用附近，为什么比只预训练技能主说明更完整？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspt">SPT: Skills as Pre-Training Data for Agentic Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>技能往往把参数约束或示例放在配套文件，主说明的引用只是入口。就近展开让因果语言模型在需要的位置看到真实依赖，而非学习悬空引用；与通用语料混合又控制技能训练的分布偏移，不能把读过技能文本等同于执行能力已被验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如说明写“按 schema.json 填参”，若训练只含这句话却没有 schema，模型无法学到字段限制；就近插入可补齐依赖。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26563">原论文</a> · <a href="../../../../agent-research/2608.26563-spt/">实现解读</a> · <a href="#qa-40ec6a0c367caa76">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:caskg" data-paper-title="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval Agent Jilin University / Ant Group 2026-08-26 先从语义、词法、I/O 和结构证据建高召回有向图，再以 remove、substitute、reorder 三类文本反事实探针校准边，Bayesian smoothing 后只发布可靠关系。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。CaSKG 从训练 split 学习可复用 skill 路由，在隔离 test 上结合图式记忆与候选验证调用工具。ToolRoute-L2.1 三 seed 的 joint success 为 0.8000，plan step F1 为 0.8327，平均成本 5.0116。  反事实因果技能图 Agent 记忆与技能：让经验可取回、可失效 为什么技能图中的语义或 I/O 相似边，还要用 remove、substitute、reorder 探针校准？ 相似性适合高召回，却不证明某技能真正依赖另一技能或应按该顺序执行。文本反事实改变局部结构，观察关系是否仍成立，再经平滑筛出更可靠边；这提供的是探针条件下的关系证据，不能自动宣称已经完成真实环境的因果效应验证。 例如两个技能都提文件上传，删除认证步骤后才暴露前置依赖；仅凭共同词汇把它们连成可互换关系可能出错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-caskg-e0c69536" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7ef6f17d03610eb0">为什么技能图中的语义或 I/O 相似边，还要用 remove、substitute、reorder 探针校准？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acaskg">CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Jilin University / Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似性适合高召回，却不证明某技能真正依赖另一技能或应按该顺序执行。文本反事实改变局部结构，观察关系是否仍成立，再经平滑筛出更可靠边；这提供的是探针条件下的关系证据，不能自动宣称已经完成真实环境的因果效应验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个技能都提文件上传，删除认证步骤后才暴露前置依赖；仅凭共同词汇把它们连成可互换关系可能出错。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25500">原论文</a> · <a href="../../../../agent-research/2608.25500-caskg/">实现解读</a> · <a href="#qa-7ef6f17d03610eb0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skill-state" data-paper-title="SKILL.state: Scalable Long-Horizon Agent Skills" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SKILL.state: Scalable Long-Horizon Agent Skills Agent Google 2026-08-26 普通Agent把旧观察、动作和推理反复塞回下一轮。SKILL.state把可持续的信息投影到当前执行状态，每步只传技能说明、状态和最新观察；不是在完整对话外再加一个状态块。模型生成结构化patch和动作，运行时验证后提交，瞬时推理不保留。定义性流程见§3与算法1。 成本过高，不复现（审查 DONE）；actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；运行时实际执行递归合并、null删除、schema拒绝、原状态保留及有界重试。传入actor的是只含三种公共信息的不可变字符串视图，不包含gold、grader、旧回答或旧观察。actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；不是语言模型。  Agent运行时 显式执行状态与上下文控制 Agent 记忆与技能：让经验可取回、可失效 SKILL.state 为什么不是“完整对话再加一个状态块”？ 下一步只接收技能说明、当前状态和最新观察，旧对话不再反复携带，因此可持续信息必须显式写入状态。递归 patch 保留未修改字段并允许删除，运行时验证后才提交；若仍传全部历史，就绕过了状态充分性和容量受限的核心要求。 例如前轮确认的文件路径要写入状态字段，下一轮才能使用；若偷偷保留整段聊天来找路径，就无法检验状态是否足够。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-skill-state-4eba9d90" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cfd225f5bb30fb38">SKILL.state 为什么不是“完整对话再加一个状态块”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askill-state">SKILL.state: Scalable Long-Horizon Agent Skills</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>下一步只接收技能说明、当前状态和最新观察，旧对话不再反复携带，因此可持续信息必须显式写入状态。递归 patch 保留未修改字段并允许删除，运行时验证后才提交；若仍传全部历史，就绕过了状态充分性和容量受限的核心要求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前轮确认的文件路径要写入状态字段，下一轮才能使用；若偷偷保留整段聊天来找路径，就无法检验状态是否足够。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26263">原论文</a> · <a href="../../../../agent-research/2608.26263-skill-state/">实现解读</a> · <a href="#qa-cfd225f5bb30fb38">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skillforge" data-paper-title="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents Agent AMAP, Alibaba Group 2026-08-25 SkillRL 类方法从轨迹提取技能后只追加，错误和过时技能会永久污染库。SkillForge 让 policy 输出环境动作时显式选择技能，把调用决策纳入 RL；成功、失败和对比轨迹经多路径 induction 生成候选，环境证据再决定激活、修订或去重。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。技能被显式调用，并根据环境证据更新 posterior 与修订状态。本地用结构化 plan 作为技能内容，执行调用、验证、posterior 与修订控制流；未运行 LLM teacher induction、ALFWorld/WebShop/AppWorld 或 RL 训练。PlanBench-mini 120 episodes：创建 12 个技能、复用 108 次，joint success 1.0000，平均成本 0.6200。  可验证技能锻造 Agent 记忆与技能：让经验可取回、可失效 为什么技能候选要经历激活、修订或去重，而不从成功轨迹提取后直接永久追加？ 单次成功可能依赖偶然环境，旧技能还会过时或互相冲突。多路径归纳先产生候选，调用策略和环境反馈再决定是否使用及怎样修订，把技能选择纳入学习；追加只增加库容量，却不能保证候选适用或避免错误被反复检索强化。 例如成功下载经验写死了旧按钮名称，新界面失败后应修订或停用该技能，而不是把第二份相近文档继续叠到库里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-skillforge-0aa71f73" class="ar-learning-paper-anchor"></span>
<h2 id="qa-a921645b2a022efd">为什么技能候选要经历激活、修订或去重，而不从成功轨迹提取后直接永久追加？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askillforge">SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AMAP, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单次成功可能依赖偶然环境，旧技能还会过时或互相冲突。多路径归纳先产生候选，调用策略和环境反馈再决定是否使用及怎样修订，把技能选择纳入学习；追加只增加库容量，却不能保证候选适用或避免错误被反复检索强化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如成功下载经验写死了旧按钮名称，新界面失败后应修订或停用该技能，而不是把第二份相近文档继续叠到库里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24747">原论文</a> · <a href="../../../../agent-research/2608.24747-skillforge/">实现解读</a> · <a href="#qa-a921645b2a022efd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hymem" data-paper-title="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation Agent Institute of Automation, Chinese Academy of Sciences 2026-08-16 把 planning、execution 和 isolated reasoning 分层，结构化摘要在 context refresh 间保存任务进展。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  记忆 长时序 Agent Agent 记忆与技能：让经验可取回、可失效 规划、执行和 isolated reasoning 分层，为什么能减少上下文污染？ 不同层需要的信息粒度不同：规划关注目标进度，执行关注当前操作，临时推理无需永久传播。刷新间由结构化摘要保留必要状态，可避免大量局部猜测挤占长期任务信息；隔离并不等于证据自动正确，摘要仍须保留关键约束与来源。 例如一次调试尝试产生很多假设，只把验证后的接口变化和剩余问题传回规划层，不让所有临时猜想变成长期事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-hymem-ebf0c9bb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-79c1cf512c450ba6">规划、执行和 isolated reasoning 分层，为什么能减少上下文污染？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahymem">HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同层需要的信息粒度不同：规划关注目标进度，执行关注当前操作，临时推理无需永久传播。刷新间由结构化摘要保留必要状态，可避免大量局部猜测挤占长期任务信息；隔离并不等于证据自动正确，摘要仍须保留关键约束与来源。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次调试尝试产生很多假设，只把验证后的接口变化和剩余问题传回规划层，不让所有临时猜想变成长期事实。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.15703">原论文</a> · <a href="../../../../agent-research/2608.15703-hymem/">实现解读</a> · <a href="#qa-79c1cf512c450ba6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gse" data-paper-title="Learning Globally Reusable Skills for Coding Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Globally Reusable Skills for Coding Agents Agent Tianjin University 2026-08-06 主题：全局技能进化。GSE 用 Skill Relation Graph 显式维护技能关系，以聚类合并局部经验，并通过 replay verification 防止过拟合与行为回退。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的全局技能进化算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  全局技能进化 Agent 记忆与技能：让经验可取回、可失效 为什么把相似局部技能聚类合并后，还要做 replay verification？ 相似描述可能隐藏不同前置条件，合并会删掉对某些任务关键的分支。重放原有案例可检验全局复用是否以牺牲旧行为为代价，技能关系图再显式管理冲突；聚类紧凑度或新任务成功不能单独证明合并安全，也不等于跨分布泛化。 例如两个文件解析技能分别处理带表头与无表头输入，合并后应重放两类案例，避免统一流程只留下其中一种假设。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-gse-c467dca4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-08e42839803cd827">为什么把相似局部技能聚类合并后，还要做 replay verification？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agse">Learning Globally Reusable Skills for Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似描述可能隐藏不同前置条件，合并会删掉对某些任务关键的分支。重放原有案例可检验全局复用是否以牺牲旧行为为代价，技能关系图再显式管理冲突；聚类紧凑度或新任务成功不能单独证明合并安全，也不等于跨分布泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个文件解析技能分别处理带表头与无表头输入，合并后应重放两类案例，避免统一流程只留下其中一种假设。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06153">原论文</a> · <a href="../../../../agent-research/2608.06153-gse/">实现解读</a> · <a href="#qa-08e42839803cd827">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:vag" data-paper-title="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents Agent 论文未列机构 2026-08-06 主题：技能进化安全。技能一旦进入上下文会污染后代，事后删除无法彻底回滚。VaG 在写入前依次做结构、行为无害性、语义一致性验证，再以边际收益选择可共同使用的 Hot 技能集合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的技能进化安全算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  技能进化安全 Agent 记忆与技能：让经验可取回、可失效 为什么技能写入前的验证，不能完全由写入后发现有害再删除替代？ 技能一旦影响新轨迹和后代技能，污染可能已传播，删除原条目不能撤销所有衍生结果。预提交依次检查结构、行为无害性和语义一致性，再选择能共同使用的集合，把准入与运行后回滚分开；单个技能看似有效也不保证组合没有冲突。 例如错误重试规则已被另一技能吸收，删除最早文档也不会自动修复后者；写入前验证能减少这种继承污染。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-vag-dfb74800" class="ar-learning-paper-anchor"></span>
<h2 id="qa-203b6b4073c19e5f">为什么技能写入前的验证，不能完全由写入后发现有害再删除替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avag">When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>技能一旦影响新轨迹和后代技能，污染可能已传播，删除原条目不能撤销所有衍生结果。预提交依次检查结构、行为无害性和语义一致性，再选择能共同使用的集合，把准入与运行后回滚分开；单个技能看似有效也不保证组合没有冲突。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如错误重试规则已被另一技能吸收，删除最早文档也不会自动修复后者；写入前验证能减少这种继承污染。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05810">原论文</a> · <a href="../../../../agent-research/2608.05810-vag/">实现解读</a> · <a href="#qa-203b6b4073c19e5f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memorycpt" data-paper-title="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off Agent Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS 2026-08-05 主题：端到端 Agent 记忆。QAD 将离线记忆构建链蒸馏为紧凑模型；QAR 用 RRF 检索和 LoRA summarizer 生成查询相关上下文，并以成本感知 GRPO 优化 Quality per Cost。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的端到端 Agent 记忆算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  端到端 Agent 记忆 Agent 记忆与技能：让经验可取回、可失效 以 Quality per Cost 为目标，为什么不能只追求更短的查询摘要？ 成本减少若损害回答质量，比例目标未必改善；同时构建、检索和总结各自都有推理费用。离线链蒸馏降低构建开销，RRF 与查询相关总结控制读取成本，再用成本感知奖励评价整体；应在相同质量口径下比较，而非把 token 少直接当成功。 例如把五百字证据压到二十字虽便宜，却漏掉关键例外导致答错；保留八十字正确依据可能有更高质量成本比。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memorycpt-45f8aee7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e2c6e5282ef27147">以 Quality per Cost 为目标，为什么不能只追求更短的查询摘要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemorycpt">MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成本减少若损害回答质量，比例目标未必改善；同时构建、检索和总结各自都有推理费用。离线链蒸馏降低构建开销，RRF 与查询相关总结控制读取成本，再用成本感知奖励评价整体；应在相同质量口径下比较，而非把 token 少直接当成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把五百字证据压到二十字虽便宜，却漏掉关键例外导致答错；保留八十字正确依据可能有更高质量成本比。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04843">原论文</a> · <a href="../../../../agent-research/2608.04843-memorycpt/">实现解读</a> · <a href="#qa-e2c6e5282ef27147">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:vermem" data-paper-title="VerMem" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="VerMem Agent Sun Yat-sen University 2026-08-04 长期记忆、活动上下文与 episodic history 往往分开优化，轨迹奖励无法判断单次记忆操作是否正确。VerMem 用一个策略管理三类状态和七种原子操作，以 local verifier 审核状态转移、global verifier 审核证据一致性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。显式维护 LTM、active context、episodes，执行 retrieve/add/restore，并分别计数 local/global verifier。  可验证统一记忆 Agent 记忆与技能：让经验可取回、可失效 local verifier 与 global verifier 为什么要分别检查记忆操作？ 局部验证器检查一次状态转移是否符合操作合同，无法独自判断长期证据是否前后一致；全局验证器补充整条轨迹与最终记忆的关系。二者与任务奖励共同训练状态管理，避免合法小步骤累积成错误事实；验证器通过率仍不是模型任务准确率。 例如删除字段这一操作格式合法，但删除了后续答案唯一依据，局部检查可能通过，全局证据一致性却应提出问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-vermem-8bc3a085" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b3def5f3a30eb45a">local verifier 与 global verifier 为什么要分别检查记忆操作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avermem">VerMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部验证器检查一次状态转移是否符合操作合同，无法独自判断长期证据是否前后一致；全局验证器补充整条轨迹与最终记忆的关系。二者与任务奖励共同训练状态管理，避免合法小步骤累积成错误事实；验证器通过率仍不是模型任务准确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删除字段这一操作格式合法，但删除了后续答案唯一依据，局部检查可能通过，全局证据一致性却应提出问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03137">原论文</a> · <a href="../../../../agent-research/2608.03137-vermem/">实现解读</a> · <a href="#qa-b3def5f3a30eb45a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coevo-mem" data-paper-title="CoEvo-Mem" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoEvo-Mem Agent 论文未列机构 2026-08-03 只优化 query routing 或只更新 memory bank 会忽略二者反馈环。CoEvo-Mem 让冻结 LLM 生成 route-specific rewrite 和 prior，轻量 residual router 在线修正；任务结果更新路由，轨迹反馈更新 memory value 与 graph relation，并交替冻结一侧控制非平稳性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 route rewrite、残差路由与 router/memory bank 交替更新；检索键包含任务轴和工具签名，防止跨任务误复用。  检索—记忆共进化 Agent 记忆与技能：让经验可取回、可失效 路由器与记忆库为什么交替冻结，而不是每轮同时任意更新？ 路由改变会影响看到哪些记忆，记忆变化又会改变路由反馈，二者一起漂移难以判断改动来源。冻结一侧再更新另一侧控制非平稳性，轻量残差也保留基础 LLM 的路由先验；这并不保证收敛或提升，只让反馈关系更可学习和审计。 例如先固定记忆库比较两种检索路线，再固定路线调整低价值记忆；若两者同时大改，失败时很难定位是哪一侧造成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-coevo-mem-e947b4e5" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f09a664c62c12948">路由器与记忆库为什么交替冻结，而不是每轮同时任意更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoevo-mem">CoEvo-Mem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>路由改变会影响看到哪些记忆，记忆变化又会改变路由反馈，二者一起漂移难以判断改动来源。冻结一侧再更新另一侧控制非平稳性，轻量残差也保留基础 LLM 的路由先验；这并不保证收敛或提升，只让反馈关系更可学习和审计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先固定记忆库比较两种检索路线，再固定路线调整低价值记忆；若两者同时大改，失败时很难定位是哪一侧造成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01739">原论文</a> · <a href="../../../../agent-research/2608.01739-coevo-mem/">实现解读</a> · <a href="#qa-f09a664c62c12948">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skillrise" data-paper-title="SkillRise" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillRise Agent Zhejiang University 2026-07-29 标准 Agent RL 把任务视为独立 episode，外部 skill bank 又把抽取、检索和执行缠在一起。SkillRise 把相关但不同的任务排成由易到难的序列，让同一 policy 交替求解当前任务与整理一个直接传给下一任务的 skill document；求解阶段由当前结果监督，整理阶段由折扣后的下游任务结果监督。 本地验证状态演化与 credit 分离，不训练 Qwen3，也不运行 ALFWorld/WebShop/ScienceWorld；因此不能把 mini-suite 的 100% success 与论文 Pass@k 横向比较。PlanBench mini 按 task axis 组织相关任务；每个 episode 交替执行 solve 和 curate，成功轨迹更新 skill document，并单独记录跨任务复用与下游 credit。  跨任务技能进化 Agent 记忆与技能：让经验可取回、可失效 为什么整理技能文档的奖励来自后续任务，而不是当前任务成功？ 当前成功主要评价求解过程，不能说明留下的技能是否帮助别人或未来自己。把相关任务串成序列，整理阶段用折扣下游回报监督，促使文档保留可迁移经验；两个 phase 的 advantage 必须施加到各自生成 token，不能把信用无差别广播。 例如这题靠偶然猜中答案，但文档记录了可复用的测试步骤；只有之后任务因此更容易完成，才能体现整理的价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-skillrise-fa529938" class="ar-learning-paper-anchor"></span>
<h2 id="qa-9386b52986589e13">为什么整理技能文档的奖励来自后续任务，而不是当前任务成功？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askillrise">SkillRise</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前成功主要评价求解过程，不能说明留下的技能是否帮助别人或未来自己。把相关任务串成序列，整理阶段用折扣下游回报监督，促使文档保留可迁移经验；两个 phase 的 advantage 必须施加到各自生成 token，不能把信用无差别广播。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如这题靠偶然猜中答案，但文档记录了可复用的测试步骤；只有之后任务因此更容易完成，才能体现整理的价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26784">原论文</a> · <a href="../../../../agent-research/2607.26784-skillrise/">实现解读</a> · <a href="#qa-9386b52986589e13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hiskill" data-paper-title="HiSkill" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HiSkill Agent Beijing University of Posts and Telecommunications 2026-07-28 用高层 skill、可执行 AtomicOp 和多类有向边组织经验，推理时只检索任务相关子图来落地动作。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。图节点来自受控轨迹，不由在线 LLM 抽取；主要验证层次和关系是否改善复用。PlanBench mini-suite 构建高层 skill/AtomicOp 节点及 decomposition、transition、recovery 边，记录子图复用。  Hierarchical skill memory Agent 记忆与技能：让经验可取回、可失效 技能图为什么要区分分解边、时间边和恢复边？ 这些边表达不同执行语义：分解说明高层目标由哪些 AtomicOp 落地，时间边约束先后，恢复边提供失败后的可用路径。混成一种相似度关系会丢失可执行条件；检索相关子图后还需根据当前状态 grounding，不能把找到技能名就算完成动作。 例如“上传文件”先分解为选文件与提交，失败后沿恢复边刷新登录；把恢复步骤当固定前置流程会引入无谓操作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-hiskill-6a9652b8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-01a662c9411b2245">技能图为什么要区分分解边、时间边和恢复边？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahiskill">HiSkill</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这些边表达不同执行语义：分解说明高层目标由哪些 AtomicOp 落地，时间边约束先后，恢复边提供失败后的可用路径。混成一种相似度关系会丢失可执行条件；检索相关子图后还需根据当前状态 grounding，不能把找到技能名就算完成动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“上传文件”先分解为选文件与提交，失败后沿恢复边刷新登录；把恢复步骤当固定前置流程会引入无谓操作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25853">原论文</a> · <a href="../../../../agent-research/2607.25853-hiskill/">实现解读</a> · <a href="#qa-01a662c9411b2245">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:unimem" data-paper-title="UniMem" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UniMem Agent CASIA 2026-07-28 新颖任务先进入 episodic buffer；反复出现且可靠的执行模式再被自路由控制器固化到可扩展 parametric memory。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。参数记忆是结构化模式表，不是扩展 LLM 权重块；验证稳定性/可塑性路由逻辑。EvoMem mini-suite 实现 episodic route、复现频次阈值、parametric route 和 consolidation 统计。  Continual agent memory Agent 记忆与技能：让经验可取回、可失效 为什么新任务先放 episodic buffer，反复可靠出现后才固化到参数记忆？ 一次事件可能是噪声或特例，先留情节记录保留上下文，重复且可靠的模式再适合形成稳定参数化知识。自路由决定两种记忆如何使用，减少把偶然经验过早写进长期行为的风险；出现次数也需配合可靠性，不能把重复错误当成可固化规律。 例如首次遇到临时服务故障先记为事件，多次确认同一配置约束后再沉淀为通用处理模式，而不立即修改所有任务策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-unimem-c304c78e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3cf08ee16e225a73">为什么新任务先放 episodic buffer，反复可靠出现后才固化到参数记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aunimem">UniMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · CASIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一次事件可能是噪声或特例，先留情节记录保留上下文，重复且可靠的模式再适合形成稳定参数化知识。自路由决定两种记忆如何使用，减少把偶然经验过早写进长期行为的风险；出现次数也需配合可靠性，不能把重复错误当成可固化规律。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如首次遇到临时服务故障先记为事件，多次确认同一配置约束后再沉淀为通用处理模式，而不立即修改所有任务策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26017">原论文</a> · <a href="../../../../agent-research/2607.26017-unimem/">实现解读</a> · <a href="#qa-3cf08ee16e225a73">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memcon" data-paper-title="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents Agent 未明确标注（正文 HTML 未显示一作机构映射） 2026-07-15 MemCon 将记忆使用拆成一个独立的在线控制问题：根据任务进展、重复动作、记忆规模和已有成功计划，选择检索深度、计划注入、替换查询或记忆维护。控制器用轻量表格 UCB 探索，并从任务结束时的二元反馈及效率奖励学习，不为了选择记忆操作额外调用 LLM。 原六 benchmark、多框架和多 LLM 的端到端比较会产生大量长轨迹推理，成本过高，暂不复现；L1 机制诊断。本轮完成：CPU 核心控制器与真实记忆操作；L1 机制诊断。没有调用 LLM，没有读取任务标准答案或标准计划，不是原论文六个 benchmark 的能力复现，也不作为 evolve 晋级证据。已实现：附录 C 状态/动作、正文 UCB、warm-start、终末奖励、逆序信用、真实 backend 操作、持久化/恢复。本轮核心算法只使用 Python 标准库，CPU 上运行，不下载权重或数据，不增加付费调用。  主动记忆 在线上下文 bandit 记忆维护与计划复用 Agent 记忆与技能：让经验可取回、可失效 为什么记忆控制器的 UCB 必须按当前离散状态计数，而非只用全局动作频率？ 某操作在早期探索有用，不代表任务后期或记忆拥塞时也有用。状态局部的访问数与价值让控制器分别学习这些条件下的取舍，未访问动作先探索，再从终局与效率反馈更新；不额外调用 LLM 只指控制选择，实际检索和执行仍可能有成本。 例如“深检索”在刚开始有价值，临近结束却可能拖延；两个状态应各自累计尝试，不能用一份全局成功率混在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memcon-717a2e37" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8957db0ab44f22e6">为什么记忆控制器的 UCB 必须按当前离散状态计数，而非只用全局动作频率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemcon">Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 未明确标注（正文 HTML 未显示一作机构映射）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>某操作在早期探索有用，不代表任务后期或记忆拥塞时也有用。状态局部的访问数与价值让控制器分别学习这些条件下的取舍，未访问动作先探索，再从终局与效率反馈更新；不额外调用 LLM 只指控制选择，实际检索和执行仍可能有成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“深检索”在刚开始有价值，临近结束却可能拖延；两个状态应各自累计尝试，不能用一份全局成功率混在一起。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13591">原论文</a> · <a href="../../../../agent-research/2607.13591-memcon/">实现解读</a> · <a href="#qa-8957db0ab44f22e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memento-skills" data-paper-title="Memento-Skills" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memento-Skills Agent Memento Team 2026-03-19 从执行日志反思出结构化技能说明，按任务检索并写回版本化技能，而不是原样堆叠轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 0.0500，average cost 0.2800；方法特有操作有非零 telemetry。  技能设计 Agent 记忆与技能：让经验可取回、可失效 版本化技能为什么比把执行日志原样追加到上下文更可复用？ 日志记录一次具体经历，结构化技能抽出适用条件与步骤，检索时更容易匹配新任务。版本合并还记录后续修正，避免同一技能出现互相矛盾的旧说明；抽象需要保留失败条件与来源，不能因为语言更简洁就假定已成为可靠通用程序。 例如一次部署日志含临时目录和重试输出，技能版保留检查依赖与回滚条件，之后升级版本修正过期参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memento-skills-c4d49bbe" class="ar-learning-paper-anchor"></span>
<h2 id="qa-884b9152b4a7f491">版本化技能为什么比把执行日志原样追加到上下文更可复用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemento-skills">Memento-Skills</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Memento Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>日志记录一次具体经历，结构化技能抽出适用条件与步骤，检索时更容易匹配新任务。版本合并还记录后续修正，避免同一技能出现互相矛盾的旧说明；抽象需要保留失败条件与来源，不能因为语言更简洁就假定已成为可靠通用程序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次部署日志含临时目录和重试输出，技能版保留检查依赖与回滚条件，之后升级版本修正过期参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.18743">原论文</a> · <a href="../../../../agent-research/2603.18743-memento-skills/">实现解读</a> · <a href="#qa-884b9152b4a7f491">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:u-mem" data-paper-title="U-Mem" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="U-Mem Agent National University of Singapore 2026-02-25 传统 Agent 记忆通常被动写入和检索，缺少“当前知识不够时主动去哪里找”的决策。U-Mem 将获取过程建模为成本递增的级联：先尝试 self/teacher，再做工具研究，最后请求 expert；检索结合语义相似度与 Thompson sampling，并在写回前验证和整理记忆。 保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；当前 mini-suite 不包含论文使用的真实 LLM、HotpotQA 或 AIME 推理。mini-suite 的知识源、专家和验证器都是确定性的，不包含真实搜索 API、模型幻觉或 token 成本。因此这里验证的是主动获取状态机与成本记账，不是 HotpotQA/AIME 分数复刻。evomem-mini 覆盖 episode 内/跨 episode × knowledge/execution 四象限。  主动记忆 Agent 记忆与技能：让经验可取回、可失效 为什么获取知识按 self/teacher、工具研究、expert 逐级升级，而非一开始总找最强专家？ 不同级别的获取成本不同，先尝试便宜且可能足够的路径，把高成本援助留给仍不确定的问题。Thompson sampling 让历史效用与不确定性共同影响检索，写回前再验证；级联不是保证低价来源总正确，而是收益与成本的顺序决策。 例如常见配置问题先查已有记忆，找不到再读文档，仍有歧义才请专家；无需每次都支付最高级帮助成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-u-mem-1e639ec3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-4c22d63ec43b7864">为什么获取知识按 self/teacher、工具研究、expert 逐级升级，而非一开始总找最强专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Au-mem">U-Mem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同级别的获取成本不同，先尝试便宜且可能足够的路径，把高成本援助留给仍不确定的问题。Thompson sampling 让历史效用与不确定性共同影响检索，写回前再验证；级联不是保证低价来源总正确，而是收益与成本的顺序决策。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如常见配置问题先查已有记忆，找不到再读文档，仍有歧义才请专家；无需每次都支付最高级帮助成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与算法；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22406">原论文</a> · <a href="../../../../agent-research/2602.22406-u-mem/">实现解读</a> · <a href="#qa-4c22d63ec43b7864">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pahf" data-paper-title="Learning Personalized Agents from Human Feedback" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Personalized Agents from Human Feedback Agent Meta Superintelligence Labs / Princeton University（工作完成于 Meta） 2026-02-18 Agent 在行动前从显式用户记忆检索偏好，未知或低置信时主动澄清；行动后无论当前记忆是否自信，都接收纠正并覆盖过期偏好，从而处理新用户、上下文差异和偏好漂移。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。三种子诊断：metrics/mechanism-seeds42-44.json  个性化 Agent 显式记忆 双通道反馈 Agent 记忆与技能：让经验可取回、可失效 为什么行动后即使原记忆很自信，也必须允许用户纠正偏好？ 自信只反映当前记忆状态，不保证偏好没随场景或时间变化。行动前检索和澄清处理未知，行动后纠正覆盖过期内容，两个阶段解决不同问题；若只在低置信时接受反馈，曾经学错或已漂移的高置信偏好反而会被永久固化。 例如用户过去常选早班机，如今因作息改变拒绝；系统应更新偏好，而不能因为旧记录自信就继续反复订早班。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-pahf-5582b2a9" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ed0c2c2164e5bf6a">为什么行动后即使原记忆很自信，也必须允许用户纠正偏好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apahf">Learning Personalized Agents from Human Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / Princeton University（工作完成于 Meta）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自信只反映当前记忆状态，不保证偏好没随场景或时间变化。行动前检索和澄清处理未知，行动后纠正覆盖过期内容，两个阶段解决不同问题；若只在低置信时接受反馈，曾经学错或已漂移的高置信偏好反而会被永久固化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户过去常选早班机，如今因作息改变拒绝；系统应更新偏好，而不能因为旧记录自信就继续反复订早班。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16173">原论文</a> · <a href="../../../../agent-research/2602.16173-pahf/">实现解读</a> · <a href="#qa-ed0c2c2164e5bf6a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memskill" data-paper-title="MemSkill" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemSkill Agent Nanyang Technological University 2026-02-02 controller 从历史 episode 选择记忆，designer 将重复成功模式编译为技能，并随新反馈升级技能版本。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  记忆技能 Agent 记忆与技能：让经验可取回、可失效 controller 选择记忆与 designer 编译技能为什么不是同一件事？ 选择解决当前任务需要读哪段经验，编译则把重复成功模式转换为以后可调用的程序知识。二者时间尺度与对象不同，新反馈还要驱动版本升级；检索到一次成功 episode 不足以证明其细节可直接固化，仍需区分通用步骤与偶然环境条件。 例如先为当前报错找历史修复记录，多次确认同类模式后才形成技能；那次日志里的临时账号不应被一起编译成固定参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memskill-ffe2092a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c0f675d6e105b894">controller 选择记忆与 designer 编译技能为什么不是同一件事？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemskill">MemSkill</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>选择解决当前任务需要读哪段经验，编译则把重复成功模式转换为以后可调用的程序知识。二者时间尺度与对象不同，新反馈还要驱动版本升级；检索到一次成功 episode 不足以证明其细节可直接固化，仍需区分通用步骤与偶然环境条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先为当前报错找历史修复记录，多次确认同类模式后才形成技能；那次日志里的临时账号不应被一起编译成固定参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.02474">原论文</a> · <a href="../../../../agent-research/2602.02474-memskill/">实现解读</a> · <a href="#qa-c0f675d6e105b894">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sage" data-paper-title="SAGE" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SAGE Agent University of Wisconsin–Madison 2025-12-18 从成功轨迹抽象技能，失败时修订或淘汰，并以任务回报学习技能检索与复用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3000；方法特有操作有非零 telemetry。  技能库强化学习 Agent 记忆与技能：让经验可取回、可失效 为什么成功轨迹抽出的技能仍需要在失败时修订或淘汰？ 成功只说明技能在当时条件可用，新任务可能不满足同样前提。执行回报既训练检索选择，也反馈技能内容是否失效，修订与淘汰阻止错误长期累积；若库只增不减，相关但过时的技能可能持续被检索并强化错误行为。 例如旧网站的下载技能曾经成功，页面改版后按钮路径失效，应修订或停用，而不是因历史成功继续把它排第一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-sage-ae754679" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b5c319a86b79af83">为什么成功轨迹抽出的技能仍需要在失败时修订或淘汰？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asage">SAGE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成功只说明技能在当时条件可用，新任务可能不满足同样前提。执行回报既训练检索选择，也反馈技能内容是否失效，修订与淘汰阻止错误长期累积；若库只增不减，相关但过时的技能可能持续被检索并强化错误行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧网站的下载技能曾经成功，页面改版后按钮路径失效，应修订或停用，而不是因历史成功继续把它排第一。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.17102">原论文</a> · <a href="../../../../agent-research/2512.17102-sage/">实现解读</a> · <a href="#qa-b5c319a86b79af83">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:legomem" data-paper-title="LEGOMem" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="LEGOMem Agent Microsoft Research 2025-10-06 整段成功轨迹难以迁移到新任务，单一全局记忆又混合了任务分解和工具执行。LEGOMem 把经验拆成像积木一样的 procedural units：orchestrator memory 保存任务分解与委派，agent memory 保存具体动作模板，运行时按新任务重新组合。 保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；当前 PlanBench mini 不替代论文的 OfficeBench 多 Agent 环境。当前没有真实 Office 应用、LLM 多 Agent 委派或错误恢复。实现证明过程单元能提取、验证和跨 episode 复用，但不构成 OfficeBench 原始结果的复刻。planbench-mini 使用可验证结构化计划。实现从成功计划提取 action/domain 单元，分别复用高层分解和细粒度动作，并记录 reused_plans。  过程记忆 Agent 记忆与技能：让经验可取回、可失效 为什么编排记忆与执行记忆分开，更容易重新组合到新任务？ 任务分解与委派描述高层依赖，具体动作模板描述如何落地工具调用，把它们混成整段轨迹会绑死人员和环境。分层后可复用分解结构并替换执行单元；只有经过验证的单元准入，拼接后仍要检查接口与前置条件，不能任意积木化。 例如“收集、核对、汇总”流程不变，但某次从数据库读取、另一次从文件读取；编排可复用，底层执行模板可替换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-legomem-3e37af3a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-21c86cef36853d28">为什么编排记忆与执行记忆分开，更容易重新组合到新任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alegomem">LEGOMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务分解与委派描述高层依赖，具体动作模板描述如何落地工具调用，把它们混成整段轨迹会绑死人员和环境。分层后可复用分解结构并替换执行单元；只有经过验证的单元准入，拼接后仍要检查接口与前置条件，不能任意积木化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“收集、核对、汇总”流程不变，但某次从数据库读取、另一次从文件读取；编排可复用，底层执行模板可替换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与算法；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04851">原论文</a> · <a href="../../../../agent-research/2510.04851-legomem/">实现解读</a> · <a href="#qa-21c86cef36853d28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memtool" data-paper-title="MemTool" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemTool Agent PricewaterhouseCoopers Commercial Technology and Innovation Office 2025-07-29 大量 MCP 工具描述会迅速占满上下文，静态截断又可能删掉当前工作流需要的工具。MemTool 比较 autonomous、workflow 和 hybrid 管理方式；hybrid 策略保护当前工作流的必需工具，其余工具依据近期性和历史成功率动态淘汰。 保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；ScaleMCP mini 只验证多轮工具集合管理，不包含 5,000 个真实 MCP server。工具是本地确定性描述，没有真实 MCP 网络延迟、权限失败或模型工具选择误差。结果支持受限上下文的淘汰逻辑与指标链路，不能直接对比论文的 5,000-server 实验。scalemcp-mini 生成连续工具需求，在固定 memory size 下更新保护集合、淘汰非必要工具，并统计 task success、上下文成本和 tool_evictions。  工具记忆 Agent 记忆与技能：让经验可取回、可失效 为什么当前工作流必需工具必须优先于近期性或历史成功率被保护？ 启发式保留分数反映过去使用情况，却可能低估接下来尚未调用的必需工具。先保护工作流依赖，再在其余工具中淘汰低分项，才能避免执行中途失去关键接口；如果必需集合本身超过容量，也不能靠静默截断假装工作流仍完整。 例如归档任务最后才需上传工具，它近期没用过但仍是必需步骤；不能只因低近期性把它从当前上下文删掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memtool-13c64e5c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-356e892465a4deff">为什么当前工作流必需工具必须优先于近期性或历史成功率被保护？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemtool">MemTool</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PricewaterhouseCoopers Commercial Technology and Innovation Office</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>启发式保留分数反映过去使用情况，却可能低估接下来尚未调用的必需工具。先保护工作流依赖，再在其余工具中淘汰低分项，才能避免执行中途失去关键接口；如果必需集合本身超过容量，也不能靠静默截断假装工作流仍完整。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如归档任务最后才需上传工具，它近期没用过但仍是必需步骤；不能只因低近期性把它从当前上下文删掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与算法；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.21428">原论文</a> · <a href="../../../../agent-research/2507.21428-memtool/">实现解读</a> · <a href="#qa-356e892465a4deff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memgpt" data-paper-title="MemGPT" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemGPT Agent University of California, Berkeley 2023-10-12 有限 context window 使长文档和多轮会话不断遗忘。MemGPT 借鉴操作系统虚拟内存，把常驻核心信息、当前工作上下文和外部归档分层管理；模型通过函数调用移动数据，并以 interrupt/heartbeat 控制继续推理和与用户交互。 本页实现 core、working、archival 三层状态，工作上下文超预算时触发 interrupt、page-out，并在后续任务中 page-in。实现分层状态、换入换出和 interrupt 计数；归档检索使用确定性 key，不调用 embedding 服务或 LLM function calling。成本是统一代理成本，不是 token 或线上延迟。EvoMem mini 120 episodes、seed 42、memory size 24；working tier 使用一半容量，压力触发 page-out，重复任务从 archival tier page-in。  虚拟上下文 Agent 记忆与技能：让经验可取回、可失效 外部归档很大，为什么仍需要模型主动管理 page-in/page-out？ 归档容量不等于模型当前能读取的上下文，相关内容必须被调入工作窗口才能影响回答。分页操作连接长期保存与当前任务，heartbeat 或中断控制继续取证和与用户交互；它提供虚拟内存式接口，不是让模型一次直接看见无限历史。 例如旧对话中的地址保存在归档，回答寄件问题前仍需检索并调入；仅说“归档里有”不会自动让当前推理知道地址。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memgpt-81032c11" class="ar-learning-paper-anchor"></span>
<h2 id="qa-aaf7b125e9d02507">外部归档很大，为什么仍需要模型主动管理 page-in/page-out？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemgpt">MemGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>归档容量不等于模型当前能读取的上下文，相关内容必须被调入工作窗口才能影响回答。分页操作连接长期保存与当前任务，heartbeat 或中断控制继续取证和与用户交互；它提供虚拟内存式接口，不是让模型一次直接看见无限历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧对话中的地址保存在归档，回答寄件问题前仍需检索并调入；仅说“归档里有”不会自动让当前推理知道地址。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.08560">原论文</a> · <a href="../../../../agent-research/2310.08560-memgpt/">实现解读</a> · <a href="#qa-aaf7b125e9d02507">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:voyager" data-paper-title="Voyager" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Voyager Agent NVIDIA 2023-05-25 开放世界 Agent 需要持续选择有新颖性的任务、把成功行为积累为技能，并根据环境报错修复程序。Voyager 用 GPT-4 自动生成 curriculum，以代码作为动作空间；成功程序按描述索引进 skill library，新任务检索并组合已有技能。 本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。本页实现自动课程入口、执行反馈/自验证，以及可增长、可复用的 executable skill library；不声称在本地复刻 Minecraft 世界。保留 curriculum/skill/verification 三组件和跨 episode 复用；本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。  终身学习 Agent 记忆与技能：让经验可取回、可失效 为什么只有通过环境验证的程序才进入技能库？ 代码看起来合理不保证能在当前世界执行，环境反馈能暴露缺材料、接口错误或不满足目标。成功后再按描述索引，后续任务才有可复用的行为基础；自动课程负责持续选新目标，技能库负责保留已证实动作，两者不能由单纯程序生成替代。 例如程序写出合成铁镐的步骤，但背包没有铁锭时不能算技能成功；实际完成后才适合作为之后探索的可调用工具。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-voyager-f3989bf0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-aa9ceda6b2719950">为什么只有通过环境验证的程序才进入技能库？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avoyager">Voyager</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>代码看起来合理不保证能在当前世界执行，环境反馈能暴露缺材料、接口错误或不满足目标。成功后再按描述索引，后续任务才有可复用的行为基础；自动课程负责持续选新目标，技能库负责保留已证实动作，两者不能由单纯程序生成替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如程序写出合成铁镐的步骤，但背包没有铁锭时不能算技能成功；实际完成后才适合作为之后探索的可调用工具。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16291">原论文</a> · <a href="../../../../agent-research/2305.16291-voyager/">实现解读</a> · <a href="#qa-aa9ceda6b2719950">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:generative-agents" data-paper-title="Generative Agents" data-learning-pending="false" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Generative Agents Agent Stanford University 2023-04-07 只把完整历史塞给 LLM 无法支撑长期一致行为。论文把每次观察写入 memory stream，按 recency、importance、relevance 检索；累计重要事件达到阈值后生成更高层 reflection，再结合记忆与当前状态制定日程和行动计划。 本页实现 memory stream 的相关性/近期性/重要性检索、累计重要性触发反思，以及用检索记忆生成计划。复现记忆打分、反思触发和计划依赖；没有运行 25 个 LLM persona、Smallville 地图或人类可信度评测，因此这里只比较执行成功率、上下文代理成本和内部状态。EvoMem mini 120 episodes、seed 42、memory size 24，采用三项打分取 top-3，并按累计重要性合成 reflection。  记忆与反思 Agent 记忆与技能：让经验可取回、可失效 高 importance 的旧事件为什么不该自动取代与当前问题更相关的记忆？ 重要性衡量对长期行为的意义，相关性衡量当前查询匹配，近期性又处理时间衰减，三者承担不同角色。反思把多件重要经历抽象成高层认识，但行动仍需结合当前状态；只按某一项检索会偏向永远重复大事件或只看最新闲聊。 例如搬家很重要，但问今天约饭地点时，昨晚确认的餐厅更直接相关；综合排序才能兼顾长期背景和当前细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-generative-agents-beb05f66" class="ar-learning-paper-anchor"></span>
<h2 id="qa-5c25df77a18e7bbd">高 importance 的旧事件为什么不该自动取代与当前问题更相关的记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agenerative-agents">Generative Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重要性衡量对长期行为的意义，相关性衡量当前查询匹配，近期性又处理时间衰减，三者承担不同角色。反思把多件重要经历抽象成高层认识，但行动仍需结合当前状态；只按某一项检索会偏向永远重复大事件或只看最新闲聊。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如搬家很重要，但问今天约饭地点时，昨晚确认的餐厅更直接相关；综合排序才能兼顾长期背景和当前细节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.03442">原论文</a> · <a href="../../../../agent-research/2304.03442-generative-agents/">实现解读</a> · <a href="#qa-5c25df77a18e7bbd">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

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

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
