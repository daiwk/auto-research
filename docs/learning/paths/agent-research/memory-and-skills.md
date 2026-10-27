---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 记忆与技能：让经验可取回、可失效

[Agent](index.md) / 220 个问题 · 55 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<div class="ar-learning-levels" role="group" aria-label="学习层次">
<span>学习层次</span>
<button type="button" data-learning-level="" aria-pressed="true">全部</button>
<button type="button" data-learning-level="basics" aria-pressed="false">基础理解</button>
<button type="button" data-learning-level="mechanism" aria-pressed="false">核心机制</button>
<button type="button" data-learning-level="comparison" aria-pressed="false">方法对比</button>
<button type="button" data-learning-level="implementation" aria-pressed="false">实现细节</button>
</div>
<p class="ar-learning-status" data-learning-status role="status">220 个问题 · 55 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cache-engineering" data-paper-title="Cache Engineering for Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Cache Engineering for Agents Agent Tsinghua University 2026-10-20 删改早期对话文本会使后续KV失效，重prefill又产生费用。作者保留逻辑文本，直接drop旧工具响应的KV，必要时repos重设保留键的位置；缓存状态取决于操作发生的历史，不能只根据最终token前缀判断是否可复用。AKV基于扩展radix结构管理位置版本、驱逐与恢复，并探索RSI生成缓存策略。§3–4 成本过高，不复现（审查 DONE）。本轮未实现、未运行、未下载模型。本轮未实现、未运行、未下载模型。不提供本地执行命令，不生成GPU收据或虚构指标；上游安装方式请看作者仓库。不能用少量RoPE张量运算冒充已接入AKV系统、真实推理或RSI。  Agent运行时 KV缓存管理与推理效率 Agent 记忆与技能：让经验可取回、可失效 逻辑对话完整保留时，drop KV 究竟删除了什么？ 它删除部分活跃注意力缓存，使后续 token 不再直接读取这些历史 KV，但逻辑文本仍保留用于记录或恢复。drop 不会自动改写保留项的位置或下一个追加位置，因此与文本摘要、删消息后重新 prefill 是不同状态操作。 例如旧工具响应仍能在对话记录中找到，但其 KV 已不在活跃集合，当前生成不能直接注意到那些缓存项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-cache-engineering-55c07860" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0c6d6f970c0c9373">逻辑对话完整保留时，drop KV 究竟删除了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acache-engineering">Cache Engineering for Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它删除部分活跃注意力缓存，使后续 token 不再直接读取这些历史 KV，但逻辑文本仍保留用于记录或恢复。drop 不会自动改写保留项的位置或下一个追加位置，因此与文本摘要、删消息后重新 prefill 是不同状态操作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧工具响应仍能在对话记录中找到，但其 KV 已不在活跃集合，当前生成不能直接注意到那些缓存项。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28577">原论文</a> · <a href="../../../../agent-research/2610.28577-cache-engineering/">实现解读</a> · <a href="#qa-0c6d6f970c0c9373">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cache-engineering" data-paper-title="Cache Engineering for Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Cache Engineering for Agents Agent Tsinghua University 2026-10-20 删改早期对话文本会使后续KV失效，重prefill又产生费用。作者保留逻辑文本，直接drop旧工具响应的KV，必要时repos重设保留键的位置；缓存状态取决于操作发生的历史，不能只根据最终token前缀判断是否可复用。AKV基于扩展radix结构管理位置版本、驱逐与恢复，并探索RSI生成缓存策略。§3–4 成本过高，不复现（审查 DONE）。本轮未实现、未运行、未下载模型。本轮未实现、未运行、未下载模型。不提供本地执行命令，不生成GPU收据或虚构指标；上游安装方式请看作者仓库。不能用少量RoPE张量运算冒充已接入AKV系统、真实推理或RSI。  Agent运行时 KV缓存管理与推理效率 Agent 记忆与技能：让经验可取回、可失效 为什么同样的最终文本前缀，也不一定对应可复用的同一份 KV？ KV 取决于计算时可见的历史与位置，drop 发生早晚不同可能已影响后续状态。repos 还要对 RoPE Key 作位置变换，不能只改索引或连 Value 一起旋转；缓存索引因此需要记录位置版本与操作历史，单看逻辑字符串相同不足以证明等价。 例如旧工具响应在生成前被驱逐与生成后才被驱逐，后续 token 曾看到的内容不同，即使最后保留文本一样也不能混用缓存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cache-engineering" data-paper-title="Cache Engineering for Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Cache Engineering for Agents Agent Tsinghua University 2026-10-20 删改早期对话文本会使后续KV失效，重prefill又产生费用。作者保留逻辑文本，直接drop旧工具响应的KV，必要时repos重设保留键的位置；缓存状态取决于操作发生的历史，不能只根据最终token前缀判断是否可复用。AKV基于扩展radix结构管理位置版本、驱逐与恢复，并探索RSI生成缓存策略。§3–4 成本过高，不复现（审查 DONE）。本轮未实现、未运行、未下载模型。本轮未实现、未运行、未下载模型。不提供本地执行命令，不生成GPU收据或虚构指标；上游安装方式请看作者仓库。不能用少量RoPE张量运算冒充已接入AKV系统、真实推理或RSI。  Agent运行时 KV缓存管理与推理效率 Agent 记忆与技能：让经验可取回、可失效 直接管理 KV 与把文本压缩成摘要，在恢复和缓存复用上有何不同？ 摘要改变逻辑输入并可能使后续 KV 失效，需重新预填充；直接管理保留逻辑记录，却改变活跃状态及位置版本。相同最终文本和 token 集合可能因操作时机形成不同 KV，复用身份必须包含历史，不能仅按最终前缀判断。 例如先删工具 KV 再生成一句话，与先生成该句再删旧 KV，后一句的隐藏状态可能不同，即使最终保留文本一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a73d4740f29bdb97">直接管理 KV 与把文本压缩成摘要，在恢复和缓存复用上有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acache-engineering">Cache Engineering for Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>摘要改变逻辑输入并可能使后续 KV 失效，需重新预填充；直接管理保留逻辑记录，却改变活跃状态及位置版本。相同最终文本和 token 集合可能因操作时机形成不同 KV，复用身份必须包含历史，不能仅按最终前缀判断。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先删工具 KV 再生成一句话，与先生成该句再删旧 KV，后一句的隐藏状态可能不同，即使最终保留文本一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28577">原论文</a> · <a href="../../../../agent-research/2610.28577-cache-engineering/">实现解读</a> · <a href="#qa-a73d4740f29bdb97">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cache-engineering" data-paper-title="Cache Engineering for Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Cache Engineering for Agents Agent Tsinghua University 2026-10-20 删改早期对话文本会使后续KV失效，重prefill又产生费用。作者保留逻辑文本，直接drop旧工具响应的KV，必要时repos重设保留键的位置；缓存状态取决于操作发生的历史，不能只根据最终token前缀判断是否可复用。AKV基于扩展radix结构管理位置版本、驱逐与恢复，并探索RSI生成缓存策略。§3–4 成本过高，不复现（审查 DONE）。本轮未实现、未运行、未下载模型。本轮未实现、未运行、未下载模型。不提供本地执行命令，不生成GPU收据或虚构指标；上游安装方式请看作者仓库。不能用少量RoPE张量运算冒充已接入AKV系统、真实推理或RSI。  Agent运行时 KV缓存管理与推理效率 Agent 记忆与技能：让经验可取回、可失效 repos 为何只旋转 key，而不是把 value 也乘同一 RoPE 变换？ 位置从 p 移到 q 时，已旋转 key 用 R(q)R(p)^-1 调整位置，value 保持不变；drop 本身也不重编号。缓存系统还需操作历史与版本管理，本地未实现 AKV 或真实 serving，少量旋转张量计算不能冒充完整缓存工程。 例如把保留 key 的位置从十移到五，需要撤旧旋转再施新旋转；同样旋转 value 会改变其内容读取语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-20470428e0e80972">repos 为何只旋转 key，而不是把 value 也乘同一 RoPE 变换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acache-engineering">Cache Engineering for Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>位置从 p 移到 q 时，已旋转 key 用 R(q)R(p)^-1 调整位置，value 保持不变；drop 本身也不重编号。缓存系统还需操作历史与版本管理，本地未实现 AKV 或真实 serving，少量旋转张量计算不能冒充完整缓存工程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把保留 key 的位置从十移到五，需要撤旧旋转再施新旋转；同样旋转 value 会改变其内容读取语义。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本与复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28577">原论文</a> · <a href="../../../../agent-research/2610.28577-cache-engineering/">实现解读</a> · <a href="#qa-20470428e0e80972">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tokenworth" data-paper-title="Remembering Has a Price: Learning Memory Worth under Resource Constraints" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Remembering Has a Price: Learning Memory Worth under Resource Constraints Agent Nanjing University 2026-10-19 生成长度、交互次数和记忆容量同时受限时，相关记忆也可能浪费稀缺预算。TokenWorth 用四维可解释基础特征学习稳定规律，再用 Recursive Feature Machine（RFM）校正查询相关的非线性残差。快更新拟合残差价值，慢更新调整特征几何；同一个价值模型既用于检索，也用于有界记忆库的写入和淘汰。§4 与附录 B 原论文 Figure 2 展示完整价值学习和记忆生命周期框架；本页重绘与原图分开，原图由统一资源流程归档。 完整实验成本过高，不复现（审查 DONE）；默认使用论文 DB 调度（基础/KRR/AGOP 每 50/50/200 个反馈更新），诊断 runner 为缩短覆盖周期显式用 10/8/24，不能混作官方实验参数。component_only / L1 CPU 数学与时序诊断。学习的是选中记忆关联的执行结果，不是反事实因果贡献，也不是 Agent 能力验证。CPU 组件实际实现 512 维 token/字符 3–5 gram 哈希、Newton、Laplacian KRR、解析梯度与对角 AGOP、FIFO、检索及入库门。哈希函数 SHA256 和 Unicode 分词是明确的本地确定性选择，不声称与未指定细节位级相同。  记忆与长期交互 在线价值学习与有界记忆 Agent 记忆与技能：让经验可取回、可失效 TokenWorth 为什么把记忆相关性与实际效用分开建模？ 相似内容未必帮助完成当前任务，还会占用有限生成、交互与记忆预算。基础分结合相似度、效用、可靠性和近期性，再以非线性残差修正查询关系；效用来自已完成任务反馈，不能把高文本相似度直接当成成功贡献。 例如旧记忆与当前题词汇高度相似，却使用过期工具接口；低相似但说明新接口限制的记忆可能更值得保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-tokenworth-16bf712f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f2c0104195a8c16b">TokenWorth 为什么把记忆相关性与实际效用分开建模？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atokenworth">Remembering Has a Price: Learning Memory Worth under Resource Constraints</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似内容未必帮助完成当前任务，还会占用有限生成、交互与记忆预算。基础分结合相似度、效用、可靠性和近期性，再以非线性残差修正查询关系；效用来自已完成任务反馈，不能把高文本相似度直接当成成功贡献。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧记忆与当前题词汇高度相似，却使用过期工具接口；低相似但说明新接口限制的记忆可能更值得保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26453">原论文</a> · <a href="../../../../agent-research/2610.26453-tokenworth/">实现解读</a> · <a href="#qa-f2c0104195a8c16b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tokenworth" data-paper-title="Remembering Has a Price: Learning Memory Worth under Resource Constraints" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Remembering Has a Price: Learning Memory Worth under Resource Constraints Agent Nanjing University 2026-10-19 生成长度、交互次数和记忆容量同时受限时，相关记忆也可能浪费稀缺预算。TokenWorth 用四维可解释基础特征学习稳定规律，再用 Recursive Feature Machine（RFM）校正查询相关的非线性残差。快更新拟合残差价值，慢更新调整特征几何；同一个价值模型既用于检索，也用于有界记忆库的写入和淘汰。§4 与附录 B 原论文 Figure 2 展示完整价值学习和记忆生命周期框架；本页重绘与原图分开，原图由统一资源流程归档。 完整实验成本过高，不复现（审查 DONE）；默认使用论文 DB 调度（基础/KRR/AGOP 每 50/50/200 个反馈更新），诊断 runner 为缩短覆盖周期显式用 10/8/24，不能混作官方实验参数。component_only / L1 CPU 数学与时序诊断。学习的是选中记忆关联的执行结果，不是反事实因果贡献，也不是 Agent 能力验证。CPU 组件实际实现 512 维 token/字符 3–5 gram 哈希、Newton、Laplacian KRR、解析梯度与对角 AGOP、FIFO、检索及入库门。哈希函数 SHA256 和 Unicode 分词是明确的本地确定性选择，不声称与未指定细节位级相同。  记忆与长期交互 在线价值学习与有界记忆 Agent 记忆与技能：让经验可取回、可失效 为什么同一个 memory-worth 模型同时控制检索与淘汰，而不只按相似度排序？ 相似记忆也可能冗长、过时或不可靠，预算有限时应比较实际任务价值。稳定基础特征给出可解释方向，RFM 进一步学习查询相关残差，同一价值标尺再用于读取和保留；反馈只应更新真正被选中使用的记忆，不能给未访问条目编造成败标签。 例如两条记忆同样谈某接口，旧文档更相似却已过期，新文档较短且可靠；价值选择可以保留后者而非机械追相似度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tokenworth" data-paper-title="Remembering Has a Price: Learning Memory Worth under Resource Constraints" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Remembering Has a Price: Learning Memory Worth under Resource Constraints Agent Nanjing University 2026-10-19 生成长度、交互次数和记忆容量同时受限时，相关记忆也可能浪费稀缺预算。TokenWorth 用四维可解释基础特征学习稳定规律，再用 Recursive Feature Machine（RFM）校正查询相关的非线性残差。快更新拟合残差价值，慢更新调整特征几何；同一个价值模型既用于检索，也用于有界记忆库的写入和淘汰。§4 与附录 B 原论文 Figure 2 展示完整价值学习和记忆生命周期框架；本页重绘与原图分开，原图由统一资源流程归档。 完整实验成本过高，不复现（审查 DONE）；默认使用论文 DB 调度（基础/KRR/AGOP 每 50/50/200 个反馈更新），诊断 runner 为缩短覆盖周期显式用 10/8/24，不能混作官方实验参数。component_only / L1 CPU 数学与时序诊断。学习的是选中记忆关联的执行结果，不是反事实因果贡献，也不是 Agent 能力验证。CPU 组件实际实现 512 维 token/字符 3–5 gram 哈希、Newton、Laplacian KRR、解析梯度与对角 AGOP、FIFO、检索及入库门。哈希函数 SHA256 和 Unicode 分词是明确的本地确定性选择，不声称与未指定细节位级相同。  记忆与长期交互 在线价值学习与有界记忆 Agent 记忆与技能：让经验可取回、可失效 快残差拟合与慢特征几何更新为什么分开？ 快更新及时拟合新反馈的价值偏差，慢更新用梯度统计调整核距离的特征几何，减少每次反馈都大幅改变表示的震荡。两种时间尺度承担不同适应任务；残差模型并非可以看所有候选结果，只有实际使用的记忆对有真实标签。 例如一次失败可先降低相关记忆的残差价值，累计多次反馈后再调整哪些特征差异应被核函数放大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a8e4f6ea933a6baa">快残差拟合与慢特征几何更新为什么分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atokenworth">Remembering Has a Price: Learning Memory Worth under Resource Constraints</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>快更新及时拟合新反馈的价值偏差，慢更新用梯度统计调整核距离的特征几何，减少每次反馈都大幅改变表示的震荡。两种时间尺度承担不同适应任务；残差模型并非可以看所有候选结果，只有实际使用的记忆对有真实标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次失败可先降低相关记忆的残差价值，累计多次反馈后再调整哪些特征差异应被核函数放大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26453">原论文</a> · <a href="../../../../agent-research/2610.26453-tokenworth/">实现解读</a> · <a href="#qa-a8e4f6ea933a6baa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tokenworth" data-paper-title="Remembering Has a Price: Learning Memory Worth under Resource Constraints" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Remembering Has a Price: Learning Memory Worth under Resource Constraints Agent Nanjing University 2026-10-19 生成长度、交互次数和记忆容量同时受限时，相关记忆也可能浪费稀缺预算。TokenWorth 用四维可解释基础特征学习稳定规律，再用 Recursive Feature Machine（RFM）校正查询相关的非线性残差。快更新拟合残差价值，慢更新调整特征几何；同一个价值模型既用于检索，也用于有界记忆库的写入和淘汰。§4 与附录 B 原论文 Figure 2 展示完整价值学习和记忆生命周期框架；本页重绘与原图分开，原图由统一资源流程归档。 完整实验成本过高，不复现（审查 DONE）；默认使用论文 DB 调度（基础/KRR/AGOP 每 50/50/200 个反馈更新），诊断 runner 为缩短覆盖周期显式用 10/8/24，不能混作官方实验参数。component_only / L1 CPU 数学与时序诊断。学习的是选中记忆关联的执行结果，不是反事实因果贡献，也不是 Agent 能力验证。CPU 组件实际实现 512 维 token/字符 3–5 gram 哈希、Newton、Laplacian KRR、解析梯度与对角 AGOP、FIFO、检索及入库门。哈希函数 SHA256 和 Unicode 分词是明确的本地确定性选择，不声称与未指定细节位级相同。  记忆与长期交互 在线价值学习与有界记忆 Agent 记忆与技能：让经验可取回、可失效 新候选通过入库门后，为什么仍可能立刻被淘汰？ 入库门检查新颖性或相对最佳旧记忆的探针价值，随后扩展库按整体价值淘汰最低项，新候选也参与竞争。探针来自当前及历史真实查询，不是未来测试题；只更新实际选中对，不能为未用候选捏造反事实成功标签。 例如候选足够新颖先进入满库，但在统一价值排序中最低，仍应自己退出，不能强制挤掉更有价值的旧记忆。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0647c429cb8f101e">新候选通过入库门后，为什么仍可能立刻被淘汰？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atokenworth">Remembering Has a Price: Learning Memory Worth under Resource Constraints</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>入库门检查新颖性或相对最佳旧记忆的探针价值，随后扩展库按整体价值淘汰最低项，新候选也参与竞争。探针来自当前及历史真实查询，不是未来测试题；只更新实际选中对，不能为未用候选捏造反事实成功标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如候选足够新颖先进入满库，但在统一价值排序中最低，仍应自己退出，不能强制挤掉更有价值的旧记忆。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.26453">原论文</a> · <a href="../../../../agent-research/2610.26453-tokenworth/">实现解读</a> · <a href="#qa-0647c429cb8f101e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memprice" data-paper-title="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents Agent Hong Kong University of Science and Technology 2026-10-18 长交互里，过去某个细节会不会有用通常事先未知。单纯按相关性保留记忆会忽略各条信息对同一上下文容量的竞争。MemPrice 给每项记忆提供 raw、summary、abstraction、keywords、delete 五级表示，联合分配有限 token；再用随占用累积的虚拟队列提高保留细节的价格。当前窗口中已经删掉的细节不能凭空恢复，只有刷新时从外部原始归档按固定流程重新提取。§3 与附录 G 原论文 Figure 2 展示记忆分配框架，Algorithm 1 明确刷新不重置队列和全局轮数。 完整实验成本过高，不复现（审查 DONE），不发起 API、模型下载或长轨迹试跑。component_only / L1 CPU 机制诊断。只验证分配和状态更新，不代表长记忆问答或 Agent 能力。CPU 组件真实运行稀疏整数动态规划、效用单调修复、降保真约束、压力更新和刷新跨界状态。token 大小与压缩内容由可信调用方给出，不能把字符数当真实 token。刷新只开放下一轮从归档重新形成的候选，不实现论文的 LLM 压缩/效用模型或 BM25 归档恢复。相同等级的文本是否确实由现有内容压缩而来，也需要上游保证；本地等级检查不能证明语义来源。  记忆与长期交互 多保真分配与资源定价 Agent 记忆与技能：让经验可取回、可失效 MemPrice 的五级表示为什么是联合分配问题？ 每项记忆可选择原文、摘要、抽象、关键词或删除，不同表示占用和效用不同，并共同竞争硬 token 容量。逐条独立选最有用版本可能超预算，因此需要在每项只能选一版的条件下联合优化；已删细节在当前窗口也不能凭空恢复。 例如一条记忆保留原文会挤掉另外两条摘要，最优决策要比较整组信息，而非各条都独立选择最高保真。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memprice-d97f4c90" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-64958fe98e9312aa">MemPrice 的五级表示为什么是联合分配问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemprice">MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每项记忆可选择原文、摘要、抽象、关键词或删除，不同表示占用和效用不同，并共同竞争硬 token 容量。逐条独立选最有用版本可能超预算，因此需要在每项只能选一版的条件下联合优化；已删细节在当前窗口也不能凭空恢复。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条记忆保留原文会挤掉另外两条摘要，最优决策要比较整组信息，而非各条都独立选择最高保真。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24955">原论文</a> · <a href="../../../../agent-research/2610.24955-memprice/">实现解读</a> · <a href="#qa-64958fe98e9312aa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memprice" data-paper-title="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents Agent Hong Kong University of Science and Technology 2026-10-18 长交互里，过去某个细节会不会有用通常事先未知。单纯按相关性保留记忆会忽略各条信息对同一上下文容量的竞争。MemPrice 给每项记忆提供 raw、summary、abstraction、keywords、delete 五级表示，联合分配有限 token；再用随占用累积的虚拟队列提高保留细节的价格。当前窗口中已经删掉的细节不能凭空恢复，只有刷新时从外部原始归档按固定流程重新提取。§3 与附录 G 原论文 Figure 2 展示记忆分配框架，Algorithm 1 明确刷新不重置队列和全局轮数。 完整实验成本过高，不复现（审查 DONE），不发起 API、模型下载或长轨迹试跑。component_only / L1 CPU 机制诊断。只验证分配和状态更新，不代表长记忆问答或 Agent 能力。CPU 组件真实运行稀疏整数动态规划、效用单调修复、降保真约束、压力更新和刷新跨界状态。token 大小与压缩内容由可信调用方给出，不能把字符数当真实 token。刷新只开放下一轮从归档重新形成的候选，不实现论文的 LLM 压缩/效用模型或 BM25 归档恢复。相同等级的文本是否确实由现有内容压缩而来，也需要上游保证；本地等级检查不能证明语义来源。  记忆与长期交互 多保真分配与资源定价 Agent 记忆与技能：让经验可取回、可失效 为什么记忆刷新不应该顺便把虚拟队列和全局轮数清零？ 队列承载累计资源压力，轮数决定动态价格的尺度，刷新只是从外部归档重新提取表示。若一起清零，系统会忘记过去长期超额占用，突然把细节重新定价得过便宜；硬容量仍须每轮满足，平均占用目标也不能替代这个即时约束。 例如连续多轮上下文接近满额后，刷新摘要不应让价格突然归零，否则系统又会保留一大批昂贵原文并重复拥塞。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memprice" data-paper-title="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents Agent Hong Kong University of Science and Technology 2026-10-18 长交互里，过去某个细节会不会有用通常事先未知。单纯按相关性保留记忆会忽略各条信息对同一上下文容量的竞争。MemPrice 给每项记忆提供 raw、summary、abstraction、keywords、delete 五级表示，联合分配有限 token；再用随占用累积的虚拟队列提高保留细节的价格。当前窗口中已经删掉的细节不能凭空恢复，只有刷新时从外部原始归档按固定流程重新提取。§3 与附录 G 原论文 Figure 2 展示记忆分配框架，Algorithm 1 明确刷新不重置队列和全局轮数。 完整实验成本过高，不复现（审查 DONE），不发起 API、模型下载或长轨迹试跑。component_only / L1 CPU 机制诊断。只验证分配和状态更新，不代表长记忆问答或 Agent 能力。CPU 组件真实运行稀疏整数动态规划、效用单调修复、降保真约束、压力更新和刷新跨界状态。token 大小与压缩内容由可信调用方给出，不能把字符数当真实 token。刷新只开放下一轮从归档重新形成的候选，不实现论文的 LLM 压缩/效用模型或 BM25 归档恢复。相同等级的文本是否确实由现有内容压缩而来，也需要上游保证；本地等级检查不能证明语义来源。  记忆与长期交互 多保真分配与资源定价 Agent 记忆与技能：让经验可取回、可失效 动态价格与固定相关性 Top-K 相比，如何反映长期容量压力？ Top-K 只按当前排名，动态价格由持续占用的虚拟队列形成，历史高占用会提高保留细节的代价。硬容量控制单轮上限，平均占用目标控制长期压力，二者不能混为同一阈值；该机制也不保证所有状态路径全局最优。 例如连续多轮都把窗口塞满，价格会逐渐上升，推动降保真；即使当前某条仍相关，也可能不值得保留长原文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-cfac8a0fe4b552e0">动态价格与固定相关性 Top-K 相比，如何反映长期容量压力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemprice">MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Top-K 只按当前排名，动态价格由持续占用的虚拟队列形成，历史高占用会提高保留细节的代价。硬容量控制单轮上限，平均占用目标控制长期压力，二者不能混为同一阈值；该机制也不保证所有状态路径全局最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如连续多轮都把窗口塞满，价格会逐渐上升，推动降保真；即使当前某条仍相关，也可能不值得保留长原文。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24955">原论文</a> · <a href="../../../../agent-research/2610.24955-memprice/">实现解读</a> · <a href="#qa-cfac8a0fe4b552e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memprice" data-paper-title="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents Agent Hong Kong University of Science and Technology 2026-10-18 长交互里，过去某个细节会不会有用通常事先未知。单纯按相关性保留记忆会忽略各条信息对同一上下文容量的竞争。MemPrice 给每项记忆提供 raw、summary、abstraction、keywords、delete 五级表示，联合分配有限 token；再用随占用累积的虚拟队列提高保留细节的价格。当前窗口中已经删掉的细节不能凭空恢复，只有刷新时从外部原始归档按固定流程重新提取。§3 与附录 G 原论文 Figure 2 展示记忆分配框架，Algorithm 1 明确刷新不重置队列和全局轮数。 完整实验成本过高，不复现（审查 DONE），不发起 API、模型下载或长轨迹试跑。component_only / L1 CPU 机制诊断。只验证分配和状态更新，不代表长记忆问答或 Agent 能力。CPU 组件真实运行稀疏整数动态规划、效用单调修复、降保真约束、压力更新和刷新跨界状态。token 大小与压缩内容由可信调用方给出，不能把字符数当真实 token。刷新只开放下一轮从归档重新形成的候选，不实现论文的 LLM 压缩/效用模型或 BM25 归档恢复。相同等级的文本是否确实由现有内容压缩而来，也需要上游保证；本地等级检查不能证明语义来源。  记忆与长期交互 多保真分配与资源定价 Agent 记忆与技能：让经验可取回、可失效 刷新归档后能否把队列和全局轮数一起重置？ 不能。刷新只允许从外部原始归档重新形成候选，队列压力和全局 t 要跨刷新保留。大小由 tokenizer 测得，分配用精确多重选择背包而非贪心；α=0.8 是平均占用目标，不允许单轮超过硬预算 B。 例如第十轮刷新后若把 t 设回一、Q 清零，就人为清除累积价格，改变算法对长期容量竞争的记忆。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7c7546f168cfded3">刷新归档后能否把队列和全局轮数一起重置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemprice">MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。刷新只允许从外部原始归档重新形成候选，队列压力和全局 t 要跨刷新保留。大小由 tokenizer 测得，分配用精确多重选择背包而非贪心；α=0.8 是平均占用目标，不允许单轮超过硬预算 B。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第十轮刷新后若把 t 设回一、Q 清零，就人为清除累积价格，改变算法对长期容量竞争的记忆。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24955">原论文</a> · <a href="../../../../agent-research/2610.24955-memprice/">实现解读</a> · <a href="#qa-7c7546f168cfded3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hy-memory" data-paper-title="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing Agent Tencent Hunyuan 2026-10-15 先在学生自己写出的记忆状态上做 OPD，学习不同框架的写入协议；再冻结 reader 和 judge，单独优化 writer。逐块探针补足稀疏奖励，跨块事实归因定位贡献，存储增长惩罚防止“全部记住”。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。模型和框架入口不代表本库完成了30B记忆训练。无可执行 adapter、训练分数或 Evolve 晋级；不把其他记忆算子当成本论文复现。范围见本批验收合同。只做资料收录。§7配置为30B-A3B、128 H20，每批64 windows×8 rollouts；不下载模型、不启动多框架 RL 或服务扫评。成本过高，不复现（审查 DONE）。  长期记忆 Agentic RL On-policy distillation Agent 记忆与技能：让经验可取回、可失效 为什么先学习写入协议，再冻结 reader 与 judge 优化 writer？ 写入格式首先要能被不同记忆框架正确解释，之后固定读取与评价组件才能把结果变化主要归于写入策略。若同时替换 reader、judge 和 writer，分数变化来源混杂；协议学习也要在学生实际写出的状态上进行，不能只看理想教师记忆。 例如 writer 把日期写进新字段，但 reader 不读取该字段，结果下降可能是接口问题；先对齐协议再固定 reader 才便于归因。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-hy-memory-1a0f6bb8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4283a29efc1ef0b5">为什么先学习写入协议，再冻结 reader 与 judge 优化 writer？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahy-memory">Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Hunyuan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>写入格式首先要能被不同记忆框架正确解释，之后固定读取与评价组件才能把结果变化主要归于写入策略。若同时替换 reader、judge 和 writer，分数变化来源混杂；协议学习也要在学生实际写出的状态上进行，不能只看理想教师记忆。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 writer 把日期写进新字段，但 reader 不读取该字段，结果下降可能是接口问题；先对齐协议再固定 reader 才便于归因。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22196">原论文</a> · <a href="../../../../agent-research/2610.22196-hy-memory/">实现解读</a> · <a href="#qa-4283a29efc1ef0b5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hy-memory" data-paper-title="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing Agent Tencent Hunyuan 2026-10-15 先在学生自己写出的记忆状态上做 OPD，学习不同框架的写入协议；再冻结 reader 和 judge，单独优化 writer。逐块探针补足稀疏奖励，跨块事实归因定位贡献，存储增长惩罚防止“全部记住”。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。模型和框架入口不代表本库完成了30B记忆训练。无可执行 adapter、训练分数或 Evolve 晋级；不把其他记忆算子当成本论文复现。范围见本批验收合同。只做资料收录。§7配置为30B-A3B、128 H20，每批64 windows×8 rollouts；不下载模型、不启动多框架 RL 或服务扫评。成本过高，不复现（审查 DONE）。  长期记忆 Agentic RL On-policy distillation Agent 记忆与技能：让经验可取回、可失效 冻结 reader 和 judge 后再优化 writer，为什么有助于归因记忆写入的收益？ 读取器和评分器同时变化会混淆“写得更好”与“读得更强”。固定它们后，逐块探针与事实归因更能定位 writer 的贡献，再用存储增长惩罚防止全部保留；同一块每条 rollout 只投一票，不能把更多调用误当成更多独立证据。 例如两版 writer 都交给同一 reader 回答后续问题，差异才更能反映保留了哪些事实，而非一版恰好搭配更强回答模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hy-memory" data-paper-title="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing Agent Tencent Hunyuan 2026-10-15 先在学生自己写出的记忆状态上做 OPD，学习不同框架的写入协议；再冻结 reader 和 judge，单独优化 writer。逐块探针补足稀疏奖励，跨块事实归因定位贡献，存储增长惩罚防止“全部记住”。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。模型和框架入口不代表本库完成了30B记忆训练。无可执行 adapter、训练分数或 Evolve 晋级；不把其他记忆算子当成本论文复现。范围见本批验收合同。只做资料收录。§7配置为30B-A3B、128 H20，每批64 windows×8 rollouts；不下载模型、不启动多框架 RL 或服务扫评。成本过高，不复现（审查 DONE）。  长期记忆 Agentic RL On-policy distillation Agent 记忆与技能：让经验可取回、可失效 逐块探针与最终 outcome 奖励为什么需要同时存在？ 最终答案反馈稀疏，逐块探针提供较近的写入质量信号，跨块归因再估计事实贡献；增长惩罚限制一味保存全部内容。局部探针高分不保证跨会话回答正确，最终 outcome 也不能独自解释哪一块写入有用。 例如早期块写对了日期，后续块又覆盖成错误日期，局部探针与最终归因需要共同发现这次破坏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6f446465268432d1">逐块探针与最终 outcome 奖励为什么需要同时存在？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahy-memory">Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Hunyuan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终答案反馈稀疏，逐块探针提供较近的写入质量信号，跨块归因再估计事实贡献；增长惩罚限制一味保存全部内容。局部探针高分不保证跨会话回答正确，最终 outcome 也不能独自解释哪一块写入有用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如早期块写对了日期，后续块又覆盖成错误日期，局部探针与最终归因需要共同发现这次破坏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22196">原论文</a> · <a href="../../../../agent-research/2610.22196-hy-memory/">实现解读</a> · <a href="#qa-6f446465268432d1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hy-memory" data-paper-title="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing Agent Tencent Hunyuan 2026-10-15 先在学生自己写出的记忆状态上做 OPD，学习不同框架的写入协议；再冻结 reader 和 judge，单独优化 writer。逐块探针补足稀疏奖励，跨块事实归因定位贡献，存储增长惩罚防止“全部记住”。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。模型和框架入口不代表本库完成了30B记忆训练。无可执行 adapter、训练分数或 Evolve 晋级；不把其他记忆算子当成本论文复现。范围见本批验收合同。只做资料收录。§7配置为30B-A3B、128 H20，每批64 windows×8 rollouts；不下载模型、不启动多框架 RL 或服务扫评。成本过高，不复现（审查 DONE）。  长期记忆 Agentic RL On-policy distillation Agent 记忆与技能：让经验可取回、可失效 同一 chunk 的多次模型调用能否当多张奖励票？ 不能。每条 rollout 对同一 chunk 只投一票，再在 chunk 组内标准化优势；按调用次数重复计权会让调用更频繁的轨迹获得额外影响。gold 仅供 judge，不能进入 writer、reader 或检索查询；本地未运行大规模写入 RL。 例如一条 rollout 为核对同一块调用五次，另一条只调用一次，两者仍各贡献一票，不能把前者放大五倍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-791e7424953c1d9b">同一 chunk 的多次模型调用能否当多张奖励票？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahy-memory">Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent Hunyuan</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。每条 rollout 对同一 chunk 只投一票，再在 chunk 组内标准化优势；按调用次数重复计权会让调用更频繁的轨迹获得额外影响。gold 仅供 judge，不能进入 writer、reader 或检索查询；本地未运行大规模写入 RL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条 rollout 为核对同一块调用五次，另一条只调用一次，两者仍各贡献一票，不能把前者放大五倍。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22196">原论文</a> · <a href="../../../../agent-research/2610.22196-hy-memory/">实现解读</a> · <a href="#qa-791e7424953c1d9b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memscope" data-paper-title="MemScope: Evolving Agent Memory Architectures through Localized Code Repair" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemScope: Evolving Agent Memory Architectures through Localized Code Repair Agent Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences 2026-10-15 只给“分数下降”或压缩总结，很难知道长链 Agent 该改记忆写入、检索还是下游使用。MemScope 让 Patch Agent 联合检查原始执行轨迹、运行时记忆和当前 provider 代码，定位后做有界原位修改，保留 provider identity 与现有记忆兼容性；证据不足时可以明确 no-patch，而不是每轮都强行修改。原文 §3、附录 A–B 完整实验包含大量 API／工具执行，对现有单卡或 Mac 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现局部代码替换事务和失败回滚，没有语言模型 Patch Agent，也不执行任意代码。每 seed 随机化 provider 中阈值字符串及记忆记录，实际执行成功局部替换、故意失败的兼容性 probe 和签名改变；校验失败 code 回滚、既有 memory 保留及 probe 副作用不持久化。测量的是事务合同，不是阈值调参有效性；CPU 产物保留逐 seed 来源和负对照。  长期记忆 证据驱动的局部架构修复 Agent 记忆与技能：让经验可取回、可失效 MemScope 为什么联合看原始轨迹、运行时记忆和 provider 代码？ 同一任务失败可能来自写入、检索或使用环节，仅看总分无法定位。原始轨迹说明实际行为，运行时记忆说明保存内容，代码说明处理规则，三者结合才有机会做有界修复；证据不足可返回 no-patch，不要求每轮强行改代码。 例如事实已写入却没被检索，与根本没写入需要改不同位置；只看“回答错了”无法区分这两种故障。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memscope-50996985" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7cf2a5900fc62d97">MemScope 为什么联合看原始轨迹、运行时记忆和 provider 代码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemscope">MemScope: Evolving Agent Memory Architectures through Localized Code Repair</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一任务失败可能来自写入、检索或使用环节，仅看总分无法定位。原始轨迹说明实际行为，运行时记忆说明保存内容，代码说明处理规则，三者结合才有机会做有界修复；证据不足可返回 no-patch，不要求每轮强行改代码。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如事实已写入却没被检索，与根本没写入需要改不同位置；只看“回答错了”无法区分这两种故障。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21170">原论文</a> · <a href="../../../../agent-research/2610.21170-memscope/">实现解读</a> · <a href="#qa-7cf2a5900fc62d97">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memscope" data-paper-title="MemScope: Evolving Agent Memory Architectures through Localized Code Repair" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemScope: Evolving Agent Memory Architectures through Localized Code Repair Agent Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences 2026-10-15 只给“分数下降”或压缩总结，很难知道长链 Agent 该改记忆写入、检索还是下游使用。MemScope 让 Patch Agent 联合检查原始执行轨迹、运行时记忆和当前 provider 代码，定位后做有界原位修改，保留 provider identity 与现有记忆兼容性；证据不足时可以明确 no-patch，而不是每轮都强行修改。原文 §3、附录 A–B 完整实验包含大量 API／工具执行，对现有单卡或 Mac 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现局部代码替换事务和失败回滚，没有语言模型 Patch Agent，也不执行任意代码。每 seed 随机化 provider 中阈值字符串及记忆记录，实际执行成功局部替换、故意失败的兼容性 probe 和签名改变；校验失败 code 回滚、既有 memory 保留及 probe 副作用不持久化。测量的是事务合同，不是阈值调参有效性；CPU 产物保留逐 seed 来源和负对照。  长期记忆 证据驱动的局部架构修复 Agent 记忆与技能：让经验可取回、可失效 为什么 memory provider 的签名没变，也不能直接认定补丁兼容旧记忆？ 签名只约束调用形状，内部可能改变字段含义、读取方式或写入语义。MemScope 结合原始轨迹、运行时记忆与代码定位问题，用有界事务修改并运行针对真实格式的 probe；失败需保留原代码和记忆，证据不足时也应允许不打补丁。 例如读取函数参数仍叫 memory，但补丁把时间字段从秒改成天，旧记录就可能被误解；仅通过语法检查看不出这种退化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memscope" data-paper-title="MemScope: Evolving Agent Memory Architectures through Localized Code Repair" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemScope: Evolving Agent Memory Architectures through Localized Code Repair Agent Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences 2026-10-15 只给“分数下降”或压缩总结，很难知道长链 Agent 该改记忆写入、检索还是下游使用。MemScope 让 Patch Agent 联合检查原始执行轨迹、运行时记忆和当前 provider 代码，定位后做有界原位修改，保留 provider identity 与现有记忆兼容性；证据不足时可以明确 no-patch，而不是每轮都强行修改。原文 §3、附录 A–B 完整实验包含大量 API／工具执行，对现有单卡或 Mac 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现局部代码替换事务和失败回滚，没有语言模型 Patch Agent，也不执行任意代码。每 seed 随机化 provider 中阈值字符串及记忆记录，实际执行成功局部替换、故意失败的兼容性 probe 和签名改变；校验失败 code 回滚、既有 memory 保留及 probe 副作用不持久化。测量的是事务合同，不是阈值调参有效性；CPU 产物保留逐 seed 来源和负对照。  长期记忆 证据驱动的局部架构修复 Agent 记忆与技能：让经验可取回、可失效 原位局部补丁与重新生成整个记忆 provider 有何取舍？ 局部修改保留 provider identity 和既有记忆兼容性，减少整套重写带来的格式漂移；但保留接口不保证语义不变，仍需实际 probe。整体重写更自由，却可能让旧记忆无法解释，两者不能只按代码行数比较有效性。 例如只修检索阈值可继续使用已有记录；重写成另一种 schema 若没有迁移，旧记录可能被静默忽略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-eb6033fa16a8e137">原位局部补丁与重新生成整个记忆 provider 有何取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemscope">MemScope: Evolving Agent Memory Architectures through Localized Code Repair</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部修改保留 provider identity 和既有记忆兼容性，减少整套重写带来的格式漂移；但保留接口不保证语义不变，仍需实际 probe。整体重写更自由，却可能让旧记忆无法解释，两者不能只按代码行数比较有效性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只修检索阈值可继续使用已有记录；重写成另一种 schema 若没有迁移，旧记录可能被静默忽略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21170">原论文</a> · <a href="../../../../agent-research/2610.21170-memscope/">实现解读</a> · <a href="#qa-eb6033fa16a8e137">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memscope" data-paper-title="MemScope: Evolving Agent Memory Architectures through Localized Code Repair" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemScope: Evolving Agent Memory Architectures through Localized Code Repair Agent Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences 2026-10-15 只给“分数下降”或压缩总结，很难知道长链 Agent 该改记忆写入、检索还是下游使用。MemScope 让 Patch Agent 联合检查原始执行轨迹、运行时记忆和当前 provider 代码，定位后做有界原位修改，保留 provider identity 与现有记忆兼容性；证据不足时可以明确 no-patch，而不是每轮都强行修改。原文 §3、附录 A–B 完整实验包含大量 API／工具执行，对现有单卡或 Mac 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现局部代码替换事务和失败回滚，没有语言模型 Patch Agent，也不执行任意代码。每 seed 随机化 provider 中阈值字符串及记忆记录，实际执行成功局部替换、故意失败的兼容性 probe 和签名改变；校验失败 code 回滚、既有 memory 保留及 probe 副作用不持久化。测量的是事务合同，不是阈值调参有效性；CPU 产物保留逐 seed 来源和负对照。  长期记忆 证据驱动的局部架构修复 Agent 记忆与技能：让经验可取回、可失效 AST 签名检查通过后，为何 probe 仍必须深拷贝记忆并能回滚？ 函数参数相同只证明接口形状一致，补丁可能破坏记录语义或产生副作用。probe 在深拷贝上执行，失败时保留旧代码与原记忆；replaceOnce 也须唯一命中。本地事务检查不是恶意代码 OS 沙箱，更不代表 Patch Agent 已智能进化 provider。 例如补丁保持 search(query) 签名却清空库，若直接在真实记忆上试 probe，失败后代码回滚也无法找回被删数据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c63246984a392d8f">AST 签名检查通过后，为何 probe 仍必须深拷贝记忆并能回滚？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemscope">MemScope: Evolving Agent Memory Architectures through Localized Code Repair</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>函数参数相同只证明接口形状一致，补丁可能破坏记录语义或产生副作用。probe 在深拷贝上执行，失败时保留旧代码与原记忆；replaceOnce 也须唯一命中。本地事务检查不是恶意代码 OS 沙箱，更不代表 Patch Agent 已智能进化 provider。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如补丁保持 search(query) 签名却清空库，若直接在真实记忆上试 probe，失败后代码回滚也无法找回被删数据。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21170">原论文</a> · <a href="../../../../agent-research/2610.21170-memscope/">实现解读</a> · <a href="#qa-c63246984a392d8f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:proper-agent" data-paper-title="MemoProAgent: Toward Memory-Driven Proactive Assistance" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoProAgent: Toward Memory-Driven Proactive Assistance Agent Michigan State University 2026-10-15 主动助理没有用户提问：它必须从长期记忆找出干预的依据，并在正确时机只提醒一次。相关记忆不一定意味着应该打断用户。ProPerAgent 用情节—语义图组织记忆，根据当前物体做实体匹配、单跳关联及 Personalized PageRank，再由独立 LLM gate 保留值得干预的证据；生成器结合当前画面与已说过的话，决定发言或静默。训练阶段只优化生成器产生的 token，工具注入的证据 token 不参与策略梯度。方法 §5、附录 I 完整实验成本过高，不复现（审查 DONE）；本地结果为三 seed 的合成机制诊断，不是正式多 seed 能力比较。component_only / L1 CPU 机制诊断。不是已接入 ProPerMem 的视频 Agent，也不是完整 GRPO 复现。本地真实执行事实来源检查、未来时间过滤、归一化实体 embedding、图边/PPR、gate 引用接纳、因果发言序列和联合评分。embedding、事实抽取、语义 gate 与 actor 必须由调用方提供；CPU fixture 的 one-hot 向量和确定性回调只检查接口，不代表任何视觉或语言能力。  记忆与长期交互 主动干预与内容时机联合评测 Agent 记忆与技能：让经验可取回、可失效 主动助理为什么既要会检索，又要决定保持静默？ 没有用户显式提问时，相关记忆只是潜在干预依据，当前情境未必需要打断。MemoProAgent 先从情节语义图检索，再由独立 gate 筛值得干预的证据，生成器结合画面与已说内容选择发言或静默；检索命中不等于干预成功。 例如看到药盒并想起用户习惯，不意味着每次经过药盒都提醒；只有符合当前触发条件且尚未提醒时才有意义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-proper-agent-67e59e1f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c6fb8b73132c6f21">主动助理为什么既要会检索，又要决定保持静默？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aproper-agent">MemoProAgent: Toward Memory-Driven Proactive Assistance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Michigan State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有用户显式提问时，相关记忆只是潜在干预依据，当前情境未必需要打断。MemoProAgent 先从情节语义图检索，再由独立 gate 筛值得干预的证据，生成器结合画面与已说内容选择发言或静默；检索命中不等于干预成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如看到药盒并想起用户习惯，不意味着每次经过药盒都提醒；只有符合当前触发条件且尚未提醒时才有意义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22671v2">原论文</a> · <a href="../../../../agent-research/2610.22671-proper-agent/">实现解读</a> · <a href="#qa-c6fb8b73132c6f21">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:proper-agent" data-paper-title="MemoProAgent: Toward Memory-Driven Proactive Assistance" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoProAgent: Toward Memory-Driven Proactive Assistance Agent Michigan State University 2026-10-15 主动助理没有用户提问：它必须从长期记忆找出干预的依据，并在正确时机只提醒一次。相关记忆不一定意味着应该打断用户。ProPerAgent 用情节—语义图组织记忆，根据当前物体做实体匹配、单跳关联及 Personalized PageRank，再由独立 LLM gate 保留值得干预的证据；生成器结合当前画面与已说过的话，决定发言或静默。训练阶段只优化生成器产生的 token，工具注入的证据 token 不参与策略梯度。方法 §5、附录 I 完整实验成本过高，不复现（审查 DONE）；本地结果为三 seed 的合成机制诊断，不是正式多 seed 能力比较。component_only / L1 CPU 机制诊断。不是已接入 ProPerMem 的视频 Agent，也不是完整 GRPO 复现。本地真实执行事实来源检查、未来时间过滤、归一化实体 embedding、图边/PPR、gate 引用接纳、因果发言序列和联合评分。embedding、事实抽取、语义 gate 与 actor 必须由调用方提供；CPU fixture 的 one-hot 向量和确定性回调只检查接口，不代表任何视觉或语言能力。  记忆与长期交互 主动干预与内容时机联合评测 Agent 记忆与技能：让经验可取回、可失效 相关记忆已经检索出来，为什么主动助理还需要独立的干预 gate？ 相关性只说明话题相近，不说明现在值得打断用户。gate 判断证据是否构成合适干预，生成器再结合当前画面与已说过的话选择发言或静默；时机和次数都是目标的一部分，迟到或重复提醒不能因为内容正确就算完美成功。 例如记得用户对坚果过敏，但只有看到相关食品且尚未提醒时才有介入理由；反复播放同一句警告会造成错误触发。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:proper-agent" data-paper-title="MemoProAgent: Toward Memory-Driven Proactive Assistance" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoProAgent: Toward Memory-Driven Proactive Assistance Agent Michigan State University 2026-10-15 主动助理没有用户提问：它必须从长期记忆找出干预的依据，并在正确时机只提醒一次。相关记忆不一定意味着应该打断用户。ProPerAgent 用情节—语义图组织记忆，根据当前物体做实体匹配、单跳关联及 Personalized PageRank，再由独立 LLM gate 保留值得干预的证据；生成器结合当前画面与已说过的话，决定发言或静默。训练阶段只优化生成器产生的 token，工具注入的证据 token 不参与策略梯度。方法 §5、附录 I 完整实验成本过高，不复现（审查 DONE）；本地结果为三 seed 的合成机制诊断，不是正式多 seed 能力比较。component_only / L1 CPU 机制诊断。不是已接入 ProPerMem 的视频 Agent，也不是完整 GRPO 复现。本地真实执行事实来源检查、未来时间过滤、归一化实体 embedding、图边/PPR、gate 引用接纳、因果发言序列和联合评分。embedding、事实抽取、语义 gate 与 actor 必须由调用方提供；CPU fixture 的 one-hot 向量和确定性回调只检查接口，不代表任何视觉或语言能力。  记忆与长期交互 主动干预与内容时机联合评测 Agent 记忆与技能：让经验可取回、可失效 Perfect 与“曾经说对一次”的 Hit 为什么衡量不同能力？ Perfect 要求内容正确、处于触发窗口且只说一次，Hit 不能排除提前、迟到或重复打断。静默负片段的任何发言还属于假触发；因此只提高召回可能损害用户体验，不能用内容命中替代完整时机与次数评价。 例如先提前提醒、稍后窗口内又提醒一次，可能命中内容，却因重复和时机问题不能算一次完美干预。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e48b4ca5f13b843f">Perfect 与“曾经说对一次”的 Hit 为什么衡量不同能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aproper-agent">MemoProAgent: Toward Memory-Driven Proactive Assistance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Michigan State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Perfect 要求内容正确、处于触发窗口且只说一次，Hit 不能排除提前、迟到或重复打断。静默负片段的任何发言还属于假触发；因此只提高召回可能损害用户体验，不能用内容命中替代完整时机与次数评价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先提前提醒、稍后窗口内又提醒一次，可能命中内容，却因重复和时机问题不能算一次完美干预。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22671v2">原论文</a> · <a href="../../../../agent-research/2610.22671-proper-agent/">实现解读</a> · <a href="#qa-e48b4ca5f13b843f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:proper-agent" data-paper-title="MemoProAgent: Toward Memory-Driven Proactive Assistance" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoProAgent: Toward Memory-Driven Proactive Assistance Agent Michigan State University 2026-10-15 主动助理没有用户提问：它必须从长期记忆找出干预的依据，并在正确时机只提醒一次。相关记忆不一定意味着应该打断用户。ProPerAgent 用情节—语义图组织记忆，根据当前物体做实体匹配、单跳关联及 Personalized PageRank，再由独立 LLM gate 保留值得干预的证据；生成器结合当前画面与已说过的话，决定发言或静默。训练阶段只优化生成器产生的 token，工具注入的证据 token 不参与策略梯度。方法 §5、附录 I 完整实验成本过高，不复现（审查 DONE）；本地结果为三 seed 的合成机制诊断，不是正式多 seed 能力比较。component_only / L1 CPU 机制诊断。不是已接入 ProPerMem 的视频 Agent，也不是完整 GRPO 复现。本地真实执行事实来源检查、未来时间过滤、归一化实体 embedding、图边/PPR、gate 引用接纳、因果发言序列和联合评分。embedding、事实抽取、语义 gate 与 actor 必须由调用方提供；CPU fixture 的 one-hot 向量和确定性回调只检查接口，不代表任何视觉或语言能力。  记忆与长期交互 主动干预与内容时机联合评测 Agent 记忆与技能：让经验可取回、可失效 PPR 检索和语义 gate 能否用同一个 open-loop 标志代替？ 不能。PPR 是基于实体关联的实际重启随机游走，gate 判断这些证据是否值得干预，二者功能不同。训练只优化生成器 token，工具注入证据不参与策略梯度；本地 fixture 不等于授权长期视频数据上的官方评测，不能用标志直接给出应说答案。 例如图上找到“杯子—饮水习惯”关系后，gate 仍应判断用户是否刚喝过水；检索关系本身不提供发言许可。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d55e6f3085127031">PPR 检索和语义 gate 能否用同一个 open-loop 标志代替？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aproper-agent">MemoProAgent: Toward Memory-Driven Proactive Assistance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Michigan State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。PPR 是基于实体关联的实际重启随机游走，gate 判断这些证据是否值得干预，二者功能不同。训练只优化生成器 token，工具注入证据不参与策略梯度；本地 fixture 不等于授权长期视频数据上的官方评测，不能用标志直接给出应说答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如图上找到“杯子—饮水习惯”关系后，gate 仍应判断用户是否刚喝过水；检索关系本身不提供发言许可。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22671v2">原论文</a> · <a href="../../../../agent-research/2610.22671-proper-agent/">实现解读</a> · <a href="#qa-d55e6f3085127031">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:formcraft" data-paper-title="Recursive Formation and First-Class Reuse of Compositional Capabilities" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Recursive Formation and First-Class Reuse of Compositional Capabilities Agent not listed in paper 2026-10-14 一次合成出的能力不应只留下推导历史，而应成为可独立调用、继续组合、持久保存的一等操作。FormCraft 区分三个阶段：类型与接口相容的形成、独立验证后的持久准入、通过相同公开接口直接复用。已形成的复合操作可作为普通候选，后续搜索不用重走其历史形成链，运行时内部计算并未消失。 其 LLM 长轨迹扩展没有公开低成本可核配置，成本过高，不复现（审查 DONE），不以静态 registry label 声称接入 Evolve。本页是从论文独立实现的 CPU 序列域机制与本地固定任务实验，不复制未声明许可的上游源码。不声称复现原论文全部领域、原始目标或 LLM 能力，不进入 Evolve 晋级。本地 local-fixed-sequence-D01-D12-v1 与论文同名 D 编号仅表示深度 1–12，不是作者原始目标文件。原语为整数序列追加 0/1，种子冻结目标后缀。每目标有四个训练样例；Composer 根据样例枚举真实算子链，不能读取目标后缀或 holdout。  可验证能力组合 持久技能与递归复用 Agent 记忆与技能：让经验可取回、可失效 一等复合能力与只保存一段形成历史有什么区别？ 一等能力有独立类型、公开调用 ID 和执行语义，可直接作为后续组合的候选；历史记录只说明过去如何拼出它，使用时可能仍需重做搜索。直接复用减少形成工作，但内部递归计算仍真实执行，不是把已知答案缓存成常量。 例如“追加 01”可成为普通算子，下一题直接组合这个 ID；它仍对当前输入实际追加两项，不返回上一题结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-formcraft-179a4f71" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f08554ccb6cff842">一等复合能力与只保存一段形成历史有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aformcraft">Recursive Formation and First-Class Reuse of Compositional Capabilities</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · not listed in paper</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一等能力有独立类型、公开调用 ID 和执行语义，可直接作为后续组合的候选；历史记录只说明过去如何拼出它，使用时可能仍需重做搜索。直接复用减少形成工作，但内部递归计算仍真实执行，不是把已知答案缓存成常量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“追加 01”可成为普通算子，下一题直接组合这个 ID；它仍对当前输入实际追加两项，不返回上一题结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19414">原论文</a> · <a href="../../../../agent-research/2610.19414-formcraft/">实现解读</a> · <a href="#qa-f08554ccb6cff842">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:formcraft" data-paper-title="Recursive Formation and First-Class Reuse of Compositional Capabilities" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Recursive Formation and First-Class Reuse of Compositional Capabilities Agent not listed in paper 2026-10-14 一次合成出的能力不应只留下推导历史，而应成为可独立调用、继续组合、持久保存的一等操作。FormCraft 区分三个阶段：类型与接口相容的形成、独立验证后的持久准入、通过相同公开接口直接复用。已形成的复合操作可作为普通候选，后续搜索不用重走其历史形成链，运行时内部计算并未消失。 其 LLM 长轨迹扩展没有公开低成本可核配置，成本过高，不复现（审查 DONE），不以静态 registry label 声称接入 Evolve。本页是从论文独立实现的 CPU 序列域机制与本地固定任务实验，不复制未声明许可的上游源码。不声称复现原论文全部领域、原始目标或 LLM 能力，不进入 Evolve 晋级。本地 local-fixed-sequence-D01-D12-v1 与论文同名 D 编号仅表示深度 1–12，不是作者原始目标文件。原语为整数序列追加 0/1，种子冻结目标后缀。每目标有四个训练样例；Composer 根据样例枚举真实算子链，不能读取目标后缀或 holdout。  可验证能力组合 持久技能与递归复用 Agent 记忆与技能：让经验可取回、可失效 为什么“形成一个复合能力”与“允许它进入持久技能库”要分成两步？ 接口相容只说明操作可以组合，不说明组合满足目标行为。独立验证器确认后才准入，持久身份再绑定父操作、类型和组合方式，加载时检查引用与无环性；之后可直接调用，但内部真实计算并未消失，不能把少搜一次说成零成本执行。 例如把排序再去重组合成新操作，能连起来并不保证处理空输入正确；验证后才保存，之后才能作为一个候选直接复用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:formcraft" data-paper-title="Recursive Formation and First-Class Reuse of Compositional Capabilities" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Recursive Formation and First-Class Reuse of Compositional Capabilities Agent not listed in paper 2026-10-14 一次合成出的能力不应只留下推导历史，而应成为可独立调用、继续组合、持久保存的一等操作。FormCraft 区分三个阶段：类型与接口相容的形成、独立验证后的持久准入、通过相同公开接口直接复用。已形成的复合操作可作为普通候选，后续搜索不用重走其历史形成链，运行时内部计算并未消失。 其 LLM 长轨迹扩展没有公开低成本可核配置，成本过高，不复现（审查 DONE），不以静态 registry label 声称接入 Evolve。本页是从论文独立实现的 CPU 序列域机制与本地固定任务实验，不复制未声明许可的上游源码。不声称复现原论文全部领域、原始目标或 LLM 能力，不进入 Evolve 晋级。本地 local-fixed-sequence-D01-D12-v1 与论文同名 D 编号仅表示深度 1–12，不是作者原始目标文件。原语为整数序列追加 0/1，种子冻结目标后缀。每目标有四个训练样例；Composer 根据样例枚举真实算子链，不能读取目标后缀或 holdout。  可验证能力组合 持久技能与递归复用 Agent 记忆与技能：让经验可取回、可失效 形成合法组合与持久准入为什么分成两步？ 类型相容和 DAG 合法只保证可调用，不保证实现目标功能；独立验证输入检查语义，通过后才准入持久库。若把训练样例匹配直接当准入，候选可能只记住少数例子；验证参考也必须留在 verifier，不能被 Composer 用来搜索。 例如两个算子接口匹配可形成链，但输出顺序仍可能错；要在独立输入上验证后才能供以后任务直接复用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c17b37b142fb2068">形成合法组合与持久准入为什么分成两步？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aformcraft">Recursive Formation and First-Class Reuse of Compositional Capabilities</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · not listed in paper</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>类型相容和 DAG 合法只保证可调用，不保证实现目标功能；独立验证输入检查语义，通过后才准入持久库。若把训练样例匹配直接当准入，候选可能只记住少数例子；验证参考也必须留在 verifier，不能被 Composer 用来搜索。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个算子接口匹配可形成链，但输出顺序仍可能错；要在独立输入上验证后才能供以后任务直接复用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19414">原论文</a> · <a href="../../../../agent-research/2610.19414-formcraft/">实现解读</a> · <a href="#qa-c17b37b142fb2068">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:formcraft" data-paper-title="Recursive Formation and First-Class Reuse of Compositional Capabilities" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Recursive Formation and First-Class Reuse of Compositional Capabilities Agent not listed in paper 2026-10-14 一次合成出的能力不应只留下推导历史，而应成为可独立调用、继续组合、持久保存的一等操作。FormCraft 区分三个阶段：类型与接口相容的形成、独立验证后的持久准入、通过相同公开接口直接复用。已形成的复合操作可作为普通候选，后续搜索不用重走其历史形成链，运行时内部计算并未消失。 其 LLM 长轨迹扩展没有公开低成本可核配置，成本过高，不复现（审查 DONE），不以静态 registry label 声称接入 Evolve。本页是从论文独立实现的 CPU 序列域机制与本地固定任务实验，不复制未声明许可的上游源码。不声称复现原论文全部领域、原始目标或 LLM 能力，不进入 Evolve 晋级。本地 local-fixed-sequence-D01-D12-v1 与论文同名 D 编号仅表示深度 1–12，不是作者原始目标文件。原语为整数序列追加 0/1，种子冻结目标后缀。每目标有四个训练样例；Composer 根据样例枚举真实算子链，不能读取目标后缀或 holdout。  可验证能力组合 持久技能与递归复用 Agent 记忆与技能：让经验可取回、可失效 冷加载时为什么重新检查规范 hash、父引用与无环性？ 持久能力身份由类型、操作和父 ID 的规范 JSON 哈希决定，文件可能损坏或被篡改；父引用完整及无环才能保证递归执行合法。真正持久复用需销毁旧对象再冷加载同一快照比较，本地序列域结果不能推广为通用 Lean 或 LLM 能力。 例如文件把父 ID 改为自己，即使名称没变也会产生循环；仅保存内存对象引用无法验证磁盘恢复合同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-22e0a1a33b08c7e5">冷加载时为什么重新检查规范 hash、父引用与无环性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aformcraft">Recursive Formation and First-Class Reuse of Compositional Capabilities</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · not listed in paper</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>持久能力身份由类型、操作和父 ID 的规范 JSON 哈希决定，文件可能损坏或被篡改；父引用完整及无环才能保证递归执行合法。真正持久复用需销毁旧对象再冷加载同一快照比较，本地序列域结果不能推广为通用 Lean 或 LLM 能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如文件把父 ID 改为自己，即使名称没变也会产生循环；仅保存内存对象引用无法验证磁盘恢复合同。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19414">原论文</a> · <a href="../../../../agent-research/2610.19414-formcraft/">实现解读</a> · <a href="#qa-22e0a1a33b08c7e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:transparent-compact" data-paper-title="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents Agent Hokkaido University 2026-10-14 长会话压缩通常依赖模型重写摘要，可能丢失只在对话出现的承诺或悄悄改变其措辞。本方法保留用户与助手原话，将思考和工具输出移出活跃上下文，留下明确删减标记，并提供到完整原始会话的恢复路径。压缩不调用模型；论文的 context_lookup 则由模型子代理搜索历史，二者不能混成“零模型完整恢复能力”。 原论文 27B/长上下文（至少 128k）、多臂×多次推理及盲评完整实验超出本轮预算，成本过高，不复现（审查 DONE）。本地实现的是纯 CPU 确定性压缩组件和原始负载恢复索引，不是 Pi 插件逐字节复刻，不是模型记忆能力复现；未调用 LLM，不报告回答准确率，不进入 Evolve 晋级。支持标准消息 JSON 数组及 Pi JSONL。Pi 按 id/parentId 只读取选定叶节点的祖先分支，拒绝缺父、循环和重复 ID，不将兄弟分支混入上下文；不执行会话中的命令。正文保留 Unicode 和换行，未知/非文本块移入可恢复负载。  Agent记忆与上下文 透明压缩与恢复 Agent 记忆与技能：让经验可取回、可失效 透明压缩为什么保留原话而把思考与工具负载移出？ 用户和助手原话包含事实及承诺，生成摘要可能改写含义；移出较大思考和工具负载并留删减标记，可让活跃视图更短且知道哪些内容缺失。完整原始负载另存并可恢复，但这不等于模型已自动找到并正确使用所有历史。 例如用户说“只在周五发布”应原样保留，长测试日志可移出并标记；模型需要时再按恢复路径核对日志。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-transparent-compact-55d09739" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-eba8a2358514944d">透明压缩为什么保留原话而把思考与工具负载移出？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atransparent-compact">Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hokkaido University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户和助手原话包含事实及承诺，生成摘要可能改写含义；移出较大思考和工具负载并留删减标记，可让活跃视图更短且知道哪些内容缺失。完整原始负载另存并可恢复，但这不等于模型已自动找到并正确使用所有历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户说“只在周五发布”应原样保留，长测试日志可移出并标记；模型需要时再按恢复路径核对日志。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20116">原论文</a> · <a href="../../../../agent-research/2610.20116-transparent-compact/">实现解读</a> · <a href="#qa-eba8a2358514944d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:transparent-compact" data-paper-title="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents Agent Hokkaido University 2026-10-14 长会话压缩通常依赖模型重写摘要，可能丢失只在对话出现的承诺或悄悄改变其措辞。本方法保留用户与助手原话，将思考和工具输出移出活跃上下文，留下明确删减标记，并提供到完整原始会话的恢复路径。压缩不调用模型；论文的 context_lookup 则由模型子代理搜索历史，二者不能混成“零模型完整恢复能力”。 原论文 27B/长上下文（至少 128k）、多臂×多次推理及盲评完整实验超出本轮预算，成本过高，不复现（审查 DONE）。本地实现的是纯 CPU 确定性压缩组件和原始负载恢复索引，不是 Pi 插件逐字节复刻，不是模型记忆能力复现；未调用 LLM，不报告回答准确率，不进入 Evolve 晋级。支持标准消息 JSON 数组及 Pi JSONL。Pi 按 id/parentId 只读取选定叶节点的祖先分支，拒绝缺父、循环和重复 ID，不将兄弟分支混入上下文；不执行会话中的命令。正文保留 Unicode 和换行，未知/非文本块移入可恢复负载。  Agent记忆与上下文 透明压缩与恢复 Agent 记忆与技能：让经验可取回、可失效 为什么保留原话和删减标记，比重新生成一段流畅摘要更透明？ 原话保留承诺的措辞，删减标记明确告诉模型哪些负载已移出，并提供完整会话的恢复路径。这样压缩不会把推测悄悄改成确定事实；但恢复索引存在不等于模型已经找到证据，历史搜索仍可能需要子代理调用，不能统称零模型成本。 例如用户说“暂时不要部署”，生成摘要若漏掉“暂时”会改变意思；保留原句并标出工具日志被移走更容易审计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:transparent-compact" data-paper-title="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents Agent Hokkaido University 2026-10-14 长会话压缩通常依赖模型重写摘要，可能丢失只在对话出现的承诺或悄悄改变其措辞。本方法保留用户与助手原话，将思考和工具输出移出活跃上下文，留下明确删减标记，并提供到完整原始会话的恢复路径。压缩不调用模型；论文的 context_lookup 则由模型子代理搜索历史，二者不能混成“零模型完整恢复能力”。 原论文 27B/长上下文（至少 128k）、多臂×多次推理及盲评完整实验超出本轮预算，成本过高，不复现（审查 DONE）。本地实现的是纯 CPU 确定性压缩组件和原始负载恢复索引，不是 Pi 插件逐字节复刻，不是模型记忆能力复现；未调用 LLM，不报告回答准确率，不进入 Evolve 晋级。支持标准消息 JSON 数组及 Pi JSONL。Pi 按 id/parentId 只读取选定叶节点的祖先分支，拒绝缺父、循环和重复 ID，不将兄弟分支混入上下文；不执行会话中的命令。正文保留 Unicode 和换行，未知/非文本块移入可恢复负载。  Agent记忆与上下文 透明压缩与恢复 Agent 记忆与技能：让经验可取回、可失效 确定性压缩与模型子代理 context_lookup 的成本为什么不能合并说成零调用？ 压缩规则本身无需模型，历史搜索与语义定位则由模型子代理完成，是另一条能力与成本链。本地实现精确按 ID 恢复和 hash 校验，没有实现论文模型检索；因此字符数下降只说明视图变化，不能当记忆回答能力或总存储同比下降。 例如已知日志 ID 后读回内容可零模型完成，但不知道要找哪条承诺时，语义搜索仍可能需要额外推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8116fd9b483b9d71">确定性压缩与模型子代理 context_lookup 的成本为什么不能合并说成零调用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atransparent-compact">Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hokkaido University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>压缩规则本身无需模型，历史搜索与语义定位则由模型子代理完成，是另一条能力与成本链。本地实现精确按 ID 恢复和 hash 校验，没有实现论文模型检索；因此字符数下降只说明视图变化，不能当记忆回答能力或总存储同比下降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如已知日志 ID 后读回内容可零模型完成，但不知道要找哪条承诺时，语义搜索仍可能需要额外推理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20116">原论文</a> · <a href="../../../../agent-research/2610.20116-transparent-compact/">实现解读</a> · <a href="#qa-8116fd9b483b9d71">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:transparent-compact" data-paper-title="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents Agent Hokkaido University 2026-10-14 长会话压缩通常依赖模型重写摘要，可能丢失只在对话出现的承诺或悄悄改变其措辞。本方法保留用户与助手原话，将思考和工具输出移出活跃上下文，留下明确删减标记，并提供到完整原始会话的恢复路径。压缩不调用模型；论文的 context_lookup 则由模型子代理搜索历史，二者不能混成“零模型完整恢复能力”。 原论文 27B/长上下文（至少 128k）、多臂×多次推理及盲评完整实验超出本轮预算，成本过高，不复现（审查 DONE）。本地实现的是纯 CPU 确定性压缩组件和原始负载恢复索引，不是 Pi 插件逐字节复刻，不是模型记忆能力复现；未调用 LLM，不报告回答准确率，不进入 Evolve 晋级。支持标准消息 JSON 数组及 Pi JSONL。Pi 按 id/parentId 只读取选定叶节点的祖先分支，拒绝缺父、循环和重复 ID，不将兄弟分支混入上下文；不执行会话中的命令。正文保留 Unicode 和换行，未知/非文本块移入可恢复负载。  Agent记忆与上下文 透明压缩与恢复 Agent 记忆与技能：让经验可取回、可失效 Pi 分支与工具 metadata 在压缩中为何不能随正文一起删掉？ 只应读取选定叶节点的祖先分支，防兄弟轨迹混入；工具配对 ID、名称、错误与退出状态支撑调用语义，即使正文被移出也要保留。启用正文字符 cap 会删除最旧完整块并留恢复标记，此时不能继续宣称全部原话仍在活跃上下文。 例如一次工具返回 isError=false 也应保留，不能把 false 当空值删除；否则再次压缩可能丢失这次调用实际成功的状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f938ecc9e7878519">Pi 分支与工具 metadata 在压缩中为何不能随正文一起删掉？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atransparent-compact">Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hokkaido University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只应读取选定叶节点的祖先分支，防兄弟轨迹混入；工具配对 ID、名称、错误与退出状态支撑调用语义，即使正文被移出也要保留。启用正文字符 cap 会删除最旧完整块并留恢复标记，此时不能继续宣称全部原话仍在活跃上下文。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次工具返回 isError=false 也应保留，不能把 false 当空值删除；否则再次压缩可能丢失这次调用实际成功的状态。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20116">原论文</a> · <a href="../../../../agent-research/2610.20116-transparent-compact/">实现解读</a> · <a href="#qa-f938ecc9e7878519">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:beyond-final-embedding" data-paper-title="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence Agent Southeast University 2026-10-09 最终 pooled embedding 会丢掉局部事实线索，但冻结 embedding encoder 的最后层 token states 已经含有上下文证据。论文保留内容 token（排除 query prefix、special tokens 和 padding），离线给每条 token 绑定原 memory ID。在整个候选 bank 中做全局稀疏 token top-k，再按 ID 聚合回 memory 排名；不是对每条 memory 独立 MaxSim 后排序。 实际 GPU 诊断结果与负结果如下，不能以合同 fixture 代替真实测量。本地对照口径：基线为同冻结 MiniLM 的原生 pooled cosine，实验组为真实 sparse-token fusion 及 source训练的 queryadapter；原文规模相对效果不适用。  memory-retrieval token-level-evidence query-adaptation Agent 记忆与技能：让经验可取回、可失效 为什么只保留 pooled embedding 可能漏掉记忆中的局部事实？ 整段池化把多个内容压到一个向量，某个日期或对象差异可能被共同话题稀释；最后层内容 token 保留更细的上下文证据，可用稀疏匹配补充。token 证据不是独立词典含义，也不保证所有匹配都事实正确，仍需与全局分支结合。 例如两段都谈旅行，只有一句写了改签日期；整段向量很相近，局部日期 token 更可能区分相关记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-beyond-final-embedding-06288f14" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9b251eeae4e985d6">为什么只保留 pooled embedding 可能漏掉记忆中的局部事实？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abeyond-final-embedding">Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整段池化把多个内容压到一个向量，某个日期或对象差异可能被共同话题稀释；最后层内容 token 保留更细的上下文证据，可用稀疏匹配补充。token 证据不是独立词典含义，也不保证所有匹配都事实正确，仍需与全局分支结合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两段都谈旅行，只有一句写了改签日期；整段向量很相近，局部日期 token 更可能区分相关记录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13277">原论文</a> · <a href="../../../../reproductions/2610.13277-beyond-final-embedding/">实现解读</a> · <a href="#qa-9b251eeae4e985d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:beyond-final-embedding" data-paper-title="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence Agent Southeast University 2026-10-09 最终 pooled embedding 会丢掉局部事实线索，但冻结 embedding encoder 的最后层 token states 已经含有上下文证据。论文保留内容 token（排除 query prefix、special tokens 和 padding），离线给每条 token 绑定原 memory ID。在整个候选 bank 中做全局稀疏 token top-k，再按 ID 聚合回 memory 排名；不是对每条 memory 独立 MaxSim 后排序。 实际 GPU 诊断结果与负结果如下，不能以合同 fixture 代替真实测量。本地对照口径：基线为同冻结 MiniLM 的原生 pooled cosine，实验组为真实 sparse-token fusion 及 source训练的 queryadapter；原文规模相对效果不适用。  memory-retrieval token-level-evidence query-adaptation Agent 记忆与技能：让经验可取回、可失效 全局 token top-k 再按 memory ID 聚合，为什么不同于逐条记忆做 MaxSim？ 全局检索让所有记忆 token 竞争稀疏返回预算，逐条 MaxSim 则对每份记录独立寻找匹配，计算与候选分布都不同。未返回位置还需统一 floor，避免把缺失匹配当成真实零证据；pooled 分支保留整体语义，也让没返回局部 token 的记忆仍可入选。 例如某记录只有一个罕见日期与问题强匹配，全局 token 检索可先找日期再回到记录，不必先让整段 pooled 向量胜出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:beyond-final-embedding" data-paper-title="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence Agent Southeast University 2026-10-09 最终 pooled embedding 会丢掉局部事实线索，但冻结 embedding encoder 的最后层 token states 已经含有上下文证据。论文保留内容 token（排除 query prefix、special tokens 和 padding），离线给每条 token 绑定原 memory ID。在整个候选 bank 中做全局稀疏 token top-k，再按 ID 聚合回 memory 排名；不是对每条 memory 独立 MaxSim 后排序。 实际 GPU 诊断结果与负结果如下，不能以合同 fixture 代替真实测量。本地对照口径：基线为同冻结 MiniLM 的原生 pooled cosine，实验组为真实 sparse-token fusion 及 source训练的 queryadapter；原文规模相对效果不适用。  memory-retrieval token-level-evidence query-adaptation Agent 记忆与技能：让经验可取回、可失效 全局 token Top-K 与逐 memory 完整 MaxSim 为什么不是同一检索？ 全局搜索先在整个 bank 取少量 token 邻居，再按原 memory ID 聚合，未返回匹配使用 query 相关 floor；完整 MaxSim 对每条 memory 都找最佳 token。稀疏搜索更节省匹配量，也可能漏证据，因此 pooled 分支仍可把没有返回 token 的记忆带回。 例如一条记忆的所有 token 都未进全局 Top-K，它仍有 floor 分数并可凭 pooled 相似度入选，不是直接被删掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0cd43e87a4cab556">全局 token Top-K 与逐 memory 完整 MaxSim 为什么不是同一检索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abeyond-final-embedding">Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局搜索先在整个 bank 取少量 token 邻居，再按原 memory ID 聚合，未返回匹配使用 query 相关 floor；完整 MaxSim 对每条 memory 都找最佳 token。稀疏搜索更节省匹配量，也可能漏证据，因此 pooled 分支仍可把没有返回 token 的记忆带回。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条记忆的所有 token 都未进全局 Top-K，它仍有 floor 分数并可凭 pooled 相似度入选，不是直接被删掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13277">原论文</a> · <a href="../../../../reproductions/2610.13277-beyond-final-embedding/">实现解读</a> · <a href="#qa-0cd43e87a4cab556">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:beyond-final-embedding" data-paper-title="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence Agent Southeast University 2026-10-09 最终 pooled embedding 会丢掉局部事实线索，但冻结 embedding encoder 的最后层 token states 已经含有上下文证据。论文保留内容 token（排除 query prefix、special tokens 和 padding），离线给每条 token 绑定原 memory ID。在整个候选 bank 中做全局稀疏 token top-k，再按 ID 聚合回 memory 排名；不是对每条 memory 独立 MaxSim 后排序。 实际 GPU 诊断结果与负结果如下，不能以合同 fixture 代替真实测量。本地对照口径：基线为同冻结 MiniLM 的原生 pooled cosine，实验组为真实 sparse-token fusion 及 source训练的 queryadapter；原文规模相对效果不适用。  memory-retrieval token-level-evidence query-adaptation Agent 记忆与技能：让经验可取回、可失效 query adapter 为什么不通过离散邻居选择反传？ 训练使用 all-memory MaxSim 的多正例交叉熵作为连续 surrogate，推理才做稀疏 token 搜索；离散 ANN 邻居选择不能凭空提供正确梯度。低秩残差只改 query 内容 token，保持范数，encoder、memory bank 与 pooled query 冻结，超参只看 validation。 例如改变 query 后 Top-K 索引跳变不能当普通可微函数求导；训练先用可微全量匹配学习，再在推理用稀疏索引。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e579e1a374e3da19">query adapter 为什么不通过离散邻居选择反传？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abeyond-final-embedding">Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>训练使用 all-memory MaxSim 的多正例交叉熵作为连续 surrogate，推理才做稀疏 token 搜索；离散 ANN 邻居选择不能凭空提供正确梯度。低秩残差只改 query 内容 token，保持范数，encoder、memory bank 与 pooled query 冻结，超参只看 validation。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如改变 query 后 Top-K 索引跳变不能当普通可微函数求导；训练先用可微全量匹配学习，再在推理用稀疏索引。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、数据协议、结果与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13277">原论文</a> · <a href="../../../../reproductions/2610.13277-beyond-final-embedding/">实现解读</a> · <a href="#qa-e579e1a374e3da19">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:near" data-paper-title="NEAR: Neighborhood-Aware Residuals for Memory Retrieval" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="NEAR: Neighborhood-Aware Residuals for Memory Retrieval Agent Southeast University 2026-10-09 记忆记录往往共享人名、话题和事件。共享内容会让无关证据的整体 embedding 高于真正包含事实的记录。NEAR 将这些近邻从干扰源变成 reference：离线为每条 memory 找近邻均值方向，去掉沿该方向的投影；查询不先检索候选，而从预计算小表得到对应 reference。每层在归一化残差上重新计算邻域，保留原始向量与多层 scoring view。 该旧诊断原样保留。本地对照口径：基线为同冻结 MiniLM 的原生 masked-mean pooled cosine，实验组为 NEAR 邻域残差融合；已执行三 seed，但同一数据切分与相同排名不构成独立数据重复，稳定相对提升结论不适用。  memory-retrieval neighborhood-residual single-index-retrieval Agent 记忆与技能：让经验可取回、可失效 NEAR 为什么把相似记忆当 reference，而不只把它们当竞争候选？ 多个记录共享人物与主题时，共同方向可能掩盖真正区分事实的细节。NEAR 用邻域均值方向构造参考，去除沿该方向的投影，建立残差检索视图；它仍保留原始表示融合，避免把共享但有用的信息全部丢掉。 例如多条会议记忆都提同一项目，残差可突出其中唯一包含改期日期的记录，而不让项目名重复主导排名。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-near-5f289457" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6332ddad35451607">NEAR 为什么把相似记忆当 reference，而不只把它们当竞争候选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Anear">NEAR: Neighborhood-Aware Residuals for Memory Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个记录共享人物与主题时，共同方向可能掩盖真正区分事实的细节。NEAR 用邻域均值方向构造参考，去除沿该方向的投影，建立残差检索视图；它仍保留原始表示融合，避免把共享但有用的信息全部丢掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如多条会议记忆都提同一项目，残差可突出其中唯一包含改期日期的记录，而不让项目名重复主导排名。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13314">原论文</a> · <a href="../../../../reproductions/2610.13314-near/">实现解读</a> · <a href="#qa-6332ddad35451607">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:near" data-paper-title="NEAR: Neighborhood-Aware Residuals for Memory Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="NEAR: Neighborhood-Aware Residuals for Memory Retrieval Agent Southeast University 2026-10-09 记忆记录往往共享人名、话题和事件。共享内容会让无关证据的整体 embedding 高于真正包含事实的记录。NEAR 将这些近邻从干扰源变成 reference：离线为每条 memory 找近邻均值方向，去掉沿该方向的投影；查询不先检索候选，而从预计算小表得到对应 reference。每层在归一化残差上重新计算邻域，保留原始向量与多层 scoring view。 该旧诊断原样保留。本地对照口径：基线为同冻结 MiniLM 的原生 masked-mean pooled cosine，实验组为 NEAR 邻域残差融合；已执行三 seed，但同一数据切分与相同排名不构成独立数据重复，稳定相对提升结论不适用。  memory-retrieval neighborhood-residual single-index-retrieval Agent 记忆与技能：让经验可取回、可失效 减去近邻均值方向为什么可能帮助找到包含独有事实的记忆？ 近邻常共享人名与主题，这些共同分量会让无关记录也很相似。投影去除共享方向后，残差凸显区别性信息；查询用预计算参考表，而非先偷看相关标签确定方向。残差也可能去掉有用共有线索，所以仍保留原始视图并在开发集决定融合方式。 例如两条都提到张三出差，只有一条写周五回程；弱化共同的“张三出差”方向，可让回程事实更容易影响排序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:near" data-paper-title="NEAR: Neighborhood-Aware Residuals for Memory Retrieval" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="NEAR: Neighborhood-Aware Residuals for Memory Retrieval Agent Southeast University 2026-10-09 记忆记录往往共享人名、话题和事件。共享内容会让无关证据的整体 embedding 高于真正包含事实的记录。NEAR 将这些近邻从干扰源变成 reference：离线为每条 memory 找近邻均值方向，去掉沿该方向的投影；查询不先检索候选，而从预计算小表得到对应 reference。每层在归一化残差上重新计算邻域，保留原始向量与多层 scoring view。 该旧诊断原样保留。本地对照口径：基线为同冻结 MiniLM 的原生 masked-mean pooled cosine，实验组为 NEAR 邻域残差融合；已执行三 seed，但同一数据切分与相同排名不构成独立数据重复，稳定相对提升结论不适用。  memory-retrieval neighborhood-residual single-index-retrieval Agent 记忆与技能：让经验可取回、可失效 去共享方向与训练 query-only adapter 在信息来源上有何不同？ NEAR 的 memory reference、尺度与小表只由 memory states 构建，不读 query 标签；query 根据 anchor 表取得参考方向。监督式 query adapter 则利用训练相关性更新查询变换。二者适用的信息合同不同，不能将无标签 reference 说成学到了答案相关方向。 例如不知道任何查询答案时仍能建立记忆邻域；但若按哪条是正确证据挑 reference，就已引入监督泄露。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-25b6ffcabe1f2f25">去共享方向与训练 query-only adapter 在信息来源上有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Anear">NEAR: Neighborhood-Aware Residuals for Memory Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>NEAR 的 memory reference、尺度与小表只由 memory states 构建，不读 query 标签；query 根据 anchor 表取得参考方向。监督式 query adapter 则利用训练相关性更新查询变换。二者适用的信息合同不同，不能将无标签 reference 说成学到了答案相关方向。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如不知道任何查询答案时仍能建立记忆邻域；但若按哪条是正确证据挑 reference，就已引入监督泄露。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13314">原论文</a> · <a href="../../../../reproductions/2610.13314-near/">实现解读</a> · <a href="#qa-25b6ffcabe1f2f25">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:near" data-paper-title="NEAR: Neighborhood-Aware Residuals for Memory Retrieval" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="NEAR: Neighborhood-Aware Residuals for Memory Retrieval Agent Southeast University 2026-10-09 记忆记录往往共享人名、话题和事件。共享内容会让无关证据的整体 embedding 高于真正包含事实的记录。NEAR 将这些近邻从干扰源变成 reference：离线为每条 memory 找近邻均值方向，去掉沿该方向的投影；查询不先检索候选，而从预计算小表得到对应 reference。每层在归一化残差上重新计算邻域，保留原始向量与多层 scoring view。 该旧诊断原样保留。本地对照口径：基线为同冻结 MiniLM 的原生 masked-mean pooled cosine，实验组为 NEAR 邻域残差融合；已执行三 seed，但同一数据切分与相同排名不构成独立数据重复，稳定相对提升结论不适用。  memory-retrieval neighborhood-residual single-index-retrieval Agent 记忆与技能：让经验可取回、可失效 融合多层视图后为什么不能再整体 L2 归一化拼接向量？ 各层分数按 memory–memory population variance 缩放并加权，拼接系数专门保证一次内积等于原融合公式。整体单位化会引入样本相关分母并改变排序；方差包含自相似项，邻域也在每层归一化残差上重算，不能沿用初层邻居。 例如两条记忆拼接范数不同，整体单位化会额外惩罚范数较大者，已不再是预设各层分数的线性和。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3bcdaa3f17a002c4">融合多层视图后为什么不能再整体 L2 归一化拼接向量？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Anear">NEAR: Neighborhood-Aware Residuals for Memory Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>各层分数按 memory–memory population variance 缩放并加权，拼接系数专门保证一次内积等于原融合公式。整体单位化会引入样本相关分母并改变排序；方差包含自相似项，邻域也在每层归一化残差上重算，不能沿用初层邻居。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条记忆拼接范数不同，整体单位化会额外惩罚范数较大者，已不再是预设各层分数的线性和。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13314">原论文</a> · <a href="../../../../reproductions/2610.13314-near/">实现解读</a> · <a href="#qa-3bcdaa3f17a002c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:t2mem" data-paper-title="Test-Time Memory Construction" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Test-Time Memory Construction Agent Northeastern University 2026-10-09 离线只提取事件级轻量 metadata 并保留原会话链接。推理时依据查询、已有 memory 与最新 observation 构造 memory cache，再自主选择 SearchMeta、ReadRaw 或 Answer；memory 与信息需求交错演化。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为原文 Naive RAG/structured offline memory；本地未做稳定多seed对照；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  long-term-memory test-time-construction adaptive-retrieval Agent 记忆与技能：让经验可取回、可失效 为什么离线只存轻量 metadata，而把详细 memory 构造放到查询时？ 完整会话中的有用信息依问题而异，离线摘要可能过早丢失细节。轻量事件 metadata 保留定位线索和原文链接，推理时通过 SearchMeta、ReadRaw 与 Answer 逐步形成查询相关 cache；这样仍需为多步访问付成本，不是完全不做记忆处理。 例如问一次旧旅行日期时先找到事件索引，再读相关原会话，不必在离线阶段为所有未来问题写一份万能摘要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-t2mem-26ea91d6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-94d7075589ae1f65">为什么离线只存轻量 metadata，而把详细 memory 构造放到查询时？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3At2mem">Test-Time Memory Construction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整会话中的有用信息依问题而异，离线摘要可能过早丢失细节。轻量事件 metadata 保留定位线索和原文链接，推理时通过 SearchMeta、ReadRaw 与 Answer 逐步形成查询相关 cache；这样仍需为多步访问付成本，不是完全不做记忆处理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如问一次旧旅行日期时先找到事件索引，再读相关原会话，不必在离线阶段为所有未来问题写一份万能摘要。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13348">原论文</a> · <a href="../../../../reproductions/2610.13348-t2mem/">实现解读</a> · <a href="#qa-94d7075589ae1f65">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:t2mem" data-paper-title="Test-Time Memory Construction" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Test-Time Memory Construction Agent Northeastern University 2026-10-09 离线只提取事件级轻量 metadata 并保留原会话链接。推理时依据查询、已有 memory 与最新 observation 构造 memory cache，再自主选择 SearchMeta、ReadRaw 或 Answer；memory 与信息需求交错演化。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为原文 Naive RAG/structured offline memory；本地未做稳定多seed对照；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  long-term-memory test-time-construction adaptive-retrieval Agent 记忆与技能：让经验可取回、可失效 ReadRaw 为什么只允许读取已经观察到的 metadata ID？ 轻量元数据先给出可追溯的事件入口，后续读取原文需要绑定这些实际返回过的身份，避免模型编造链接或跳到未授权记录。记忆随当前问题逐步构建，搜索、精读与回答交错；元数据索引不是一份预先完整理解的记忆，更不能携带最终答案。 例如先搜索到会议事件 M7，再按 M7 读取原对话；模型随口生成 M999 不能直接被当成真实历史证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:t2mem" data-paper-title="Test-Time Memory Construction" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Test-Time Memory Construction Agent Northeastern University 2026-10-09 离线只提取事件级轻量 metadata 并保留原会话链接。推理时依据查询、已有 memory 与最新 observation 构造 memory cache，再自主选择 SearchMeta、ReadRaw 或 Answer；memory 与信息需求交错演化。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为原文 Naive RAG/structured offline memory；本地未做稳定多seed对照；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  long-term-memory test-time-construction adaptive-retrieval Agent 记忆与技能：让经验可取回、可失效 测试时构造 memory 与一次检索后固定上下文有什么区别？ 一次检索预先决定证据集合，后续发现缺口时未必能补充；测试时构造将 memory 与信息需求交错更新，可继续搜索和读原文。它增加自主工具选择，也可能浪费步数；模型是否有效利用自由度要看真实答案而不只看动作执行。 例如读到会议提及“改期”后，可以再找后续事件确认新日期，而非坚持第一次检索出的旧日期。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-27318e8b4bfc56e5">测试时构造 memory 与一次检索后固定上下文有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3At2mem">Test-Time Memory Construction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一次检索预先决定证据集合，后续发现缺口时未必能补充；测试时构造将 memory 与信息需求交错更新，可继续搜索和读原文。它增加自主工具选择，也可能浪费步数；模型是否有效利用自由度要看真实答案而不只看动作执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如读到会议提及“改期”后，可以再找后续事件确认新日期，而非坚持第一次检索出的旧日期。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13348">原论文</a> · <a href="../../../../reproductions/2610.13348-t2mem/">实现解读</a> · <a href="#qa-27318e8b4bfc56e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:t2mem" data-paper-title="Test-Time Memory Construction" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Test-Time Memory Construction Agent Northeastern University 2026-10-09 离线只提取事件级轻量 metadata 并保留原会话链接。推理时依据查询、已有 memory 与最新 observation 构造 memory cache，再自主选择 SearchMeta、ReadRaw 或 Answer；memory 与信息需求交错演化。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为原文 Naive RAG/structured offline memory；本地未做稳定多seed对照；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  long-term-memory test-time-construction adaptive-retrieval Agent 记忆与技能：让经验可取回、可失效 ReadRaw 为什么必须拒绝尚未见过的 metadata ID？ metadata 是可公开发现的访问入口，限制原文读取到已观察 ID 可维护可追踪的证据获取过程，避免模型猜测或越过索引直接读取隐藏内容。检索排除 seen entries，gold 仅外部评分；本地真实 checkpoint 两题 F1 为零，运行通畅不能写成记忆答题成功。 例如模型猜出某个内部会话 ID 却未检索见到，读取应失败；先 SearchMeta 得到 ID 后才能合法 ReadRaw。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e80d57b9c393e851">ReadRaw 为什么必须拒绝尚未见过的 metadata ID？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3At2mem">Test-Time Memory Construction</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northeastern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>metadata 是可公开发现的访问入口，限制原文读取到已观察 ID 可维护可追踪的证据获取过程，避免模型猜测或越过索引直接读取隐藏内容。检索排除 seen entries，gold 仅外部评分；本地真实 checkpoint 两题 F1 为零，运行通畅不能写成记忆答题成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型猜出某个内部会话 ID 却未检索见到，读取应失败；先 SearchMeta 得到 ID 后才能合法 ReadRaw。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、结果、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13348">原论文</a> · <a href="../../../../reproductions/2610.13348-t2mem/">实现解读</a> · <a href="#qa-e80d57b9c393e851">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hippocam" data-paper-title="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents Agent Institute of Information Engineering, Chinese Academy of Sciences 2026-10-08 Janus 在推理前维护嵌套目的，Precip 在主响应后、工具结果前归纳闭合意图。Palim 递归整理早期前缀为叙事和知识，原消息保留为树形子节点；recall 每次返回一层，Agent 自行决定深入。原文 ALFWorld 成功率 97.8%、ScienceWorld 进展 81.9%、StreamBench 平均准确率 81.7%，未报告线上 A/B。 独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。实现意图位置更新、after-response hook、完整工具交换保护、普通/紧急前缀折叠、最小节省/重试、失败保留源文和一层 recall；辅助 checkpoint 真正生成摘要。自主 Janus 未产生闭合时报告 0 次归档；独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。  长期记忆 意图组织 经验学习 Agent 记忆与技能：让经验可取回、可失效 嵌套意图与普通按时间滚动摘要有什么不同？ 嵌套意图组织当前目的及子目的，意图闭合后才归纳对应经验；普通滚动摘要主要按时间长度压缩，未必知道某项工作是否完成。Hippocam 还保留原消息树与一层一层 recall，使抽象后仍可回溯来源，而非只剩不可恢复摘要。 例如“排查失败”意图下有“检查依赖”子意图，后者完成可归纳，但外层仍未闭合，不应把整个任务当完成归档。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-hippocam-33da2b45" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0dd2936011497890">嵌套意图与普通按时间滚动摘要有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahippocam">Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>嵌套意图组织当前目的及子目的，意图闭合后才归纳对应经验；普通滚动摘要主要按时间长度压缩，未必知道某项工作是否完成。Hippocam 还保留原消息树与一层一层 recall，使抽象后仍可回溯来源，而非只剩不可恢复摘要。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“排查失败”意图下有“检查依赖”子意图，后者完成可归纳，但外层仍未闭合，不应把整个任务当完成归档。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12124">原论文</a> · <a href="../../../../agent-research/2610.12124-hippocam/">实现解读</a> · <a href="#qa-0dd2936011497890">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hippocam" data-paper-title="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents Agent Institute of Information Engineering, Chinese Academy of Sciences 2026-10-08 Janus 在推理前维护嵌套目的，Precip 在主响应后、工具结果前归纳闭合意图。Palim 递归整理早期前缀为叙事和知识，原消息保留为树形子节点；recall 每次返回一层，Agent 自行决定深入。原文 ALFWorld 成功率 97.8%、ScienceWorld 进展 81.9%、StreamBench 平均准确率 81.7%，未报告线上 A/B。 独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。实现意图位置更新、after-response hook、完整工具交换保护、普通/紧急前缀折叠、最小节省/重试、失败保留源文和一层 recall；辅助 checkpoint 真正生成摘要。自主 Janus 未产生闭合时报告 0 次归档；独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。  长期记忆 意图组织 经验学习 Agent 记忆与技能：让经验可取回、可失效 层次化 recall 为什么一次只返回一层，而不立即展开全部原始历史？ 上层叙事先提供目的与结构，Agent 据当前需要决定是否深入，避免每次召回都重新灌满上下文。原消息保留在子节点，使摘要不是不可逆删除；同时必须给下一轮开销预留容量，若保护的完整交换仍放不下，应明确失败而非静默截断。 例如上层记忆说“上周修复登录问题”，只有需要核对报错时才再展开日志子节点，不必把所有调试输出一并送回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hippocam" data-paper-title="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents Agent Institute of Information Engineering, Chinese Academy of Sciences 2026-10-08 Janus 在推理前维护嵌套目的，Precip 在主响应后、工具结果前归纳闭合意图。Palim 递归整理早期前缀为叙事和知识，原消息保留为树形子节点；recall 每次返回一层，Agent 自行决定深入。原文 ALFWorld 成功率 97.8%、ScienceWorld 进展 81.9%、StreamBench 平均准确率 81.7%，未报告线上 A/B。 独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。实现意图位置更新、after-response hook、完整工具交换保护、普通/紧急前缀折叠、最小节省/重试、失败保留源文和一层 recall；辅助 checkpoint 真正生成摘要。自主 Janus 未产生闭合时报告 0 次归档；独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。  长期记忆 意图组织 经验学习 Agent 记忆与技能：让经验可取回、可失效 Precip 在响应后、工具结果前触发，为什么位置有意义？ 这个位置让系统依据已完成的主响应处理闭合意图，同时避免把尚未到达的工具观察当作已经知道的结果。工具交换还要保持完整，压缩不能把未闭合调用拆断；触发时机是状态合同，不是任意插入一个摘要调用都等价。 例如助手刚发出工具调用，结果尚未返回时不应总结“工具验证成功”；必须等待实际观察进入后续交换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8a074b4ab31f5006">Precip 在响应后、工具结果前触发，为什么位置有意义？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahippocam">Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这个位置让系统依据已完成的主响应处理闭合意图，同时避免把尚未到达的工具观察当作已经知道的结果。工具交换还要保持完整，压缩不能把未闭合调用拆断；触发时机是状态合同，不是任意插入一个摘要调用都等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如助手刚发出工具调用，结果尚未返回时不应总结“工具验证成功”；必须等待实际观察进入后续交换。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12124">原论文</a> · <a href="../../../../agent-research/2610.12124-hippocam/">实现解读</a> · <a href="#qa-8a074b4ab31f5006">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hippocam" data-paper-title="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents Agent Institute of Information Engineering, Chinese Academy of Sciences 2026-10-08 Janus 在推理前维护嵌套目的，Precip 在主响应后、工具结果前归纳闭合意图。Palim 递归整理早期前缀为叙事和知识，原消息保留为树形子节点；recall 每次返回一层，Agent 自行决定深入。原文 ALFWorld 成功率 97.8%、ScienceWorld 进展 81.9%、StreamBench 平均准确率 81.7%，未报告线上 A/B。 独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。独立核心机制 API 与真实 checkpoint 接口。短运行是 L1 诊断，非论文 benchmark 复测；尚未接入统一 Evolve 晋级。实现意图位置更新、after-response hook、完整工具交换保护、普通/紧急前缀折叠、最小节省/重试、失败保留源文和一层 recall；辅助 checkpoint 真正生成摘要。自主 Janus 未产生闭合时报告 0 次归档；独立受控 Precip/Palim 诊断不能作为自主记忆能力提升。  长期记忆 意图组织 经验学习 Agent 记忆与技能：让经验可取回、可失效 受控压力探针归档三次能否说自主系统学会了意图闭合？ 不能。真实自主三题没有触发闭合，归档数为零；另一个受控探针只验证压力下摘要和保护机制。预算还包括请求开销与预计下一轮，保护 K 个完整交换和动态 token 窗口后仍超容量应在主推理前失败，不应静默截断关键交换。 例如测试预设闭合信号可走通 Palim，不代表模型在未知任务中会自己生成同样信号；两种记录要分别报告。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d3449f814ee2415f">受控压力探针归档三次能否说自主系统学会了意图闭合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahippocam">Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Information Engineering, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。真实自主三题没有触发闭合，归档数为零；另一个受控探针只验证压力下摘要和保护机制。预算还包括请求开销与预计下一轮，保护 K 个完整交换和动态 token 窗口后仍超容量应在主推理前失败，不应静默截断关键交换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如测试预设闭合信号可走通 Palim，不代表模型在未知任务中会自己生成同样信号；两种记录要分别报告。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12124">原论文</a> · <a href="../../../../agent-research/2610.12124-hippocam/">实现解读</a> · <a href="#qa-d3449f814ee2415f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autocompact" data-paper-title="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents Agent 原文首页未列第一作者机构 2026-10-01 judge 同时审查何时压缩、工作摘要写什么、压缩后下一步怎么做；纠错后的输出直接进入环境，随后以 SFT+结果 RL 联合学习。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Coding Agent 上下文压缩 RL Agent 记忆与技能：让经验可取回、可失效 为什么压缩决策、工作摘要和下一动作要联合纠错？ 何时压缩决定丢弃风险，摘要决定留下哪些状态，下一动作检验这些状态能否支持继续工作。分开看可能得到单项合理却组合不一致的输出，AutoCompact 让 judge 同时检查三者，再把纠正结果送进环境，训练的是压缩后的实际行动链。 例如摘要保留了待修测试，但下一动作仍重复安装依赖，联合检查可发现这套压缩和继续计划不一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-autocompact-45b25080" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-caf61923d5bef656">为什么压缩决策、工作摘要和下一动作要联合纠错？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautocompact">AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>何时压缩决定丢弃风险，摘要决定留下哪些状态，下一动作检验这些状态能否支持继续工作。分开看可能得到单项合理却组合不一致的输出，AutoCompact 让 judge 同时检查三者，再把纠正结果送进环境，训练的是压缩后的实际行动链。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如摘要保留了待修测试，但下一动作仍重复安装依赖，联合检查可发现这套压缩和继续计划不一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02163">原论文</a> · <a href="../../../../agent-research/2610.02163-autocompact/">实现解读</a> · <a href="#qa-caf61923d5bef656">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autocompact" data-paper-title="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents Agent 原文首页未列第一作者机构 2026-10-01 judge 同时审查何时压缩、工作摘要写什么、压缩后下一步怎么做；纠错后的输出直接进入环境，随后以 SFT+结果 RL 联合学习。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Coding Agent 上下文压缩 RL Agent 记忆与技能：让经验可取回、可失效 为什么 judge 要把压缩时机、摘要内容和下一步动作放在一起纠错？ 三者相互影响：过早压缩会丢证据，摘要遗漏会诱发错误动作，正确摘要也可能被后续行为浪费。联合纠错后直接把结果放回环境，训练才能看到这套决策的实际后果；仅评价摘要是否流畅，无法判断它对长程编码任务是否足够。 例如马上要修改某接口时，摘要若漏掉参数限制，即使文字清楚也会导致下一步改错；judge 应同时修正记忆和动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autocompact" data-paper-title="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents Agent 原文首页未列第一作者机构 2026-10-01 judge 同时审查何时压缩、工作摘要写什么、压缩后下一步怎么做；纠错后的输出直接进入环境，随后以 SFT+结果 RL 联合学习。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Coding Agent 上下文压缩 RL Agent 记忆与技能：让经验可取回、可失效 学习压缩时机与固定到长度阈值就压缩有什么取舍？ 固定阈值只响应容量，不能判断当前是否处于容易丢失关键承诺或未完成操作的节点；学习决策可结合任务状态，但需要可靠监督且可能判断失误。不能只看上下文缩短比例评价，应同时看后续真实编码任务结果与成本。 例如工具结果刚返回、尚未写入结论时压缩风险较高，等状态明确后再压缩可能更容易保留必要信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a097c49f032f7e2a">学习压缩时机与固定到长度阈值就压缩有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautocompact">AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定阈值只响应容量，不能判断当前是否处于容易丢失关键承诺或未完成操作的节点；学习决策可结合任务状态，但需要可靠监督且可能判断失误。不能只看上下文缩短比例评价，应同时看后续真实编码任务结果与成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具结果刚返回、尚未写入结论时压缩风险较高，等状态明确后再压缩可能更容易保留必要信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02163">原论文</a> · <a href="../../../../agent-research/2610.02163-autocompact/">实现解读</a> · <a href="#qa-a097c49f032f7e2a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autocompact" data-paper-title="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents Agent 原文首页未列第一作者机构 2026-10-01 judge 同时审查何时压缩、工作摘要写什么、压缩后下一步怎么做；纠错后的输出直接进入环境，随后以 SFT+结果 RL 联合学习。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。执行三字段原位纠错合同；未训练 Coding Agent 或运行 SWE 容器。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Coding Agent 上下文压缩 RL Agent 记忆与技能：让经验可取回、可失效 judge 修正三元组后，环境应该执行原动作还是修正动作？ 应执行纠正后的决策、摘要和动作组合，否则训练记录与实际后果不一致。SFT 加结果 RL 需要基于真实执行反馈，本地只验证三字段原位纠错合同，没有训练 Coding Agent 或运行 SWE 容器，不能将字段测试说成代码修复效果。 例如 judge 将“立即提交”改为“先跑失败测试”，若环境仍提交旧动作，后续奖励就不能归到修正后的策略上。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dd8fc5de66dd4f65">judge 修正三元组后，环境应该执行原动作还是修正动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautocompact">AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应执行纠正后的决策、摘要和动作组合，否则训练记录与实际后果不一致。SFT 加结果 RL 需要基于真实执行反馈，本地只验证三字段原位纠错合同，没有训练 Coding Agent 或运行 SWE 容器，不能将字段测试说成代码修复效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 judge 将“立即提交”改为“先跑失败测试”，若环境仍提交旧动作，后续奖励就不能归到修正后的策略上。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02163">原论文</a> · <a href="../../../../agent-research/2610.02163-autocompact/">实现解读</a> · <a href="#qa-dd8fc5de66dd4f65">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:belief-state-pos" data-paper-title="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States Agent 原文首页未列第一作者机构 2026-10-01 把当前世界事实与尚未解决的任务要求显式维护为 belief；若连续动作没有减少 unresolved requirements，则识别 Belief Trapping 并触发针对性恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 belief 更新与停滞检测；未调用外部工具环境。执行 belief 更新与停滞检测；未调用外部工具环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长程 Agent belief state 恢复 Agent 记忆与技能：让经验可取回、可失效 显式 belief 为什么同时保存 facts 和 unresolved requirements？ facts 描述当前相信的世界状态，unresolved 描述尚未满足的任务要求，二者分别回答“知道什么”和“还缺什么”。只保存历史文字可能让 Agent 重复行为却以为有进展；显式要求集可辅助检测停滞，但其更新仍需证据支持，不能凭自信删掉要求。 例如已知用户地址属于事实，尚未确认库存属于未决项；多次重读地址并没有减少库存这个缺口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-belief-state-pos-6f953573" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-185b1b94efca0b3a">显式 belief 为什么同时保存 facts 和 unresolved requirements？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abelief-state-pos">Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>facts 描述当前相信的世界状态，unresolved 描述尚未满足的任务要求，二者分别回答“知道什么”和“还缺什么”。只保存历史文字可能让 Agent 重复行为却以为有进展；显式要求集可辅助检测停滞，但其更新仍需证据支持，不能凭自信删掉要求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如已知用户地址属于事实，尚未确认库存属于未决项；多次重读地址并没有减少库存这个缺口。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01415">原论文</a> · <a href="../../../../agent-research/2610.01415-belief-state-pos/">实现解读</a> · <a href="#qa-185b1b94efca0b3a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:belief-state-pos" data-paper-title="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States Agent 原文首页未列第一作者机构 2026-10-01 把当前世界事实与尚未解决的任务要求显式维护为 belief；若连续动作没有减少 unresolved requirements，则识别 Belief Trapping 并触发针对性恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 belief 更新与停滞检测；未调用外部工具环境。执行 belief 更新与停滞检测；未调用外部工具环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长程 Agent belief state 恢复 Agent 记忆与技能：让经验可取回、可失效 显式 unresolved requirements 为什么比只保存一段历史摘要更容易检测停滞？ 历史摘要描述做过什么，未解决要求则提供任务进度的可比较目标。连续动作若未减少这些要求，就可识别在相似状态间打转，并触发针对缺口的恢复；这不是把动作数当进展，事实与未完成要求也须随真实观察更新，不能凭模型自信划掉。 例如 Agent 重复搜索五次却始终没确认日期，未解决列表仍有“核实日期”，系统就能发现忙碌并未带来目标推进。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:belief-state-pos" data-paper-title="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States Agent 原文首页未列第一作者机构 2026-10-01 把当前世界事实与尚未解决的任务要求显式维护为 belief；若连续动作没有减少 unresolved requirements，则识别 Belief Trapping 并触发针对性恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 belief 更新与停滞检测；未调用外部工具环境。执行 belief 更新与停滞检测；未调用外部工具环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长程 Agent belief state 恢复 Agent 记忆与技能：让经验可取回、可失效 Belief Trapping 与单纯动作重复检测有什么不同？ 动作重复看表面行为相同，belief 停滞看任务未决要求是否减少。不同动作可能一直围绕同一无效假设打转，而同一查询在状态变化后也可能有用；因此进展诊断不应只按动作字符串判定，仍需正确维护要求与事实。 例如换三个搜索词都未确认付款状态，动作不同但任务仍停滞；稍后重新查询状态可能因交易完成而真正有进展。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-381bd7fc8171700f">Belief Trapping 与单纯动作重复检测有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abelief-state-pos">Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>动作重复看表面行为相同，belief 停滞看任务未决要求是否减少。不同动作可能一直围绕同一无效假设打转，而同一查询在状态变化后也可能有用；因此进展诊断不应只按动作字符串判定，仍需正确维护要求与事实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如换三个搜索词都未确认付款状态，动作不同但任务仍停滞；稍后重新查询状态可能因交易完成而真正有进展。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01415">原论文</a> · <a href="../../../../agent-research/2610.01415-belief-state-pos/">实现解读</a> · <a href="#qa-381bd7fc8171700f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:belief-state-pos" data-paper-title="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States Agent 原文首页未列第一作者机构 2026-10-01 把当前世界事实与尚未解决的任务要求显式维护为 belief；若连续动作没有减少 unresolved requirements，则识别 Belief Trapping 并触发针对性恢复。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 belief 更新与停滞检测；未调用外部工具环境。执行 belief 更新与停滞检测；未调用外部工具环境。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  长程 Agent belief state 恢复 Agent 记忆与技能：让经验可取回、可失效 Δ|unresolved|≥0 的信号能直接证明任务无解吗？ 不能。它只标记该窗口未减少未决项，可能是必要准备、证据缺失或更新器错误，应触发针对性恢复而非宣布无解。本地仅执行 belief 更新与停滞检测，没有外部工具环境或 learned 状态抽取，规则触发不能当成长程任务成功率。 例如准备身份验证暂未减少要求，但为下一步查询创造条件；把一次停滞信号直接当失败会过早终止合法路线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-de1c8d589bc7bfa8">Δ|unresolved|≥0 的信号能直接证明任务无解吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Abelief-state-pos">Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。它只标记该窗口未减少未决项，可能是必要准备、证据缺失或更新器错误，应触发针对性恢复而非宣布无解。本地仅执行 belief 更新与停滞检测，没有外部工具环境或 learned 状态抽取，规则触发不能当成长程任务成功率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如准备身份验证暂未减少要求，但为下一步查询创造条件；把一次停滞信号直接当失败会过早终止合法路线。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01415">原论文</a> · <a href="../../../../agent-research/2610.01415-belief-state-pos/">实现解读</a> · <a href="#qa-de1c8d589bc7bfa8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:causal-memory-policy" data-paper-title="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval Agent Illinois Institute of Technology 2026-10-01 被检索到的记忆与任务难度天然相关，直接按任务成败删除记忆存在选择偏差。CMP 在固定候选池中预留均衡随机曝光槽位，使每条记忆都有可估计的处理/对照样本，再用带标准误的效用判断保护不确定的记忆。 尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；L1 因果测量协议：实现均衡随机曝光、Hájek 估计及不确定性感知单 query 决策。不把它夸大为已验证的长期记忆清理策略。尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；合成效用恢复不是 Agent 答题准确率，不进入能力排行榜或 Evolve 晋级证据。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：12 条记忆、600 次检索、每次 2 槽，三 seed 合成外部结果。每条记忆曝光恰好 100 次；产物保留正负效用、标准误及 forget 判断。  因果检索干预 记忆管理 Agent 记忆与技能：让经验可取回、可失效 为什么仅观察某记忆被检索后任务失败，不能认定该记忆有害？ 困难任务可能更常触发该记忆，失败与检索同时出现不一定由记忆造成。CMP 在固定候选池随机化均衡曝光，获得处理与对照结果，再带标准误判断净效用；它解决特定设计下的识别问题，不是从任意生产日志自动提取因果。 例如复杂题更常检索长指南且更常失败，直接删指南会把任务难度的影响错算给记忆。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-causal-memory-policy-919f3b4b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b097fb0b5356bc68">为什么仅观察某记忆被检索后任务失败，不能认定该记忆有害？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acausal-memory-policy">Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Illinois Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>困难任务可能更常触发该记忆，失败与检索同时出现不一定由记忆造成。CMP 在固定候选池随机化均衡曝光，获得处理与对照结果，再带标准误判断净效用；它解决特定设计下的识别问题，不是从任意生产日志自动提取因果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如复杂题更常检索长指南且更常失败，直接删指南会把任务难度的影响错算给记忆。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02070">原论文</a> · <a href="../../../../agent-research/2610.02070-causal-memory-policy/">实现解读</a> · <a href="#qa-b097fb0b5356bc68">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:causal-memory-policy" data-paper-title="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval Agent Illinois Institute of Technology 2026-10-01 被检索到的记忆与任务难度天然相关，直接按任务成败删除记忆存在选择偏差。CMP 在固定候选池中预留均衡随机曝光槽位，使每条记忆都有可估计的处理/对照样本，再用带标准误的效用判断保护不确定的记忆。 尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；L1 因果测量协议：实现均衡随机曝光、Hájek 估计及不确定性感知单 query 决策。不把它夸大为已验证的长期记忆清理策略。尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；合成效用恢复不是 Agent 答题准确率，不进入能力排行榜或 Evolve 晋级证据。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：12 条记忆、600 次检索、每次 2 槽，三 seed 合成外部结果。每条记忆曝光恰好 100 次；产物保留正负效用、标准误及 forget 判断。  因果检索干预 记忆管理 Agent 记忆与技能：让经验可取回、可失效 为什么不能因某条记忆经常出现在失败任务中，就直接把它删除？ 困难任务本来更可能检索特定记忆，关联成败含选择偏差。均衡随机曝光为处理和对照提供可比样本，再用标准误保护不确定条目；固定槽位下替换一条也改变其他记忆分布，因此估计的是该设计的净效应，不是孤立记忆的普适加性价值。 例如故障手册总在最难事故中被调用，成功率低可能因为事故难；随机控制曝光后才能判断它是否真的有害。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:causal-memory-policy" data-paper-title="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval Agent Illinois Institute of Technology 2026-10-01 被检索到的记忆与任务难度天然相关，直接按任务成败删除记忆存在选择偏差。CMP 在固定候选池中预留均衡随机曝光槽位，使每条记忆都有可估计的处理/对照样本，再用带标准误的效用判断保护不确定的记忆。 尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；L1 因果测量协议：实现均衡随机曝光、Hájek 估计及不确定性感知单 query 决策。不把它夸大为已验证的长期记忆清理策略。尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；合成效用恢复不是 Agent 答题准确率，不进入能力排行榜或 Evolve 晋级证据。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：12 条记忆、600 次检索、每次 2 槽，三 seed 合成外部结果。每条记忆曝光恰好 100 次；产物保留正负效用、标准误及 forget 判断。  因果检索干预 记忆管理 Agent 记忆与技能：让经验可取回、可失效 保护不确定记忆与按估计均值为负就删除有什么差别？ 均值负但方差大、样本少时，真实效用可能仍为正，贸然删除有代价。CMP 的决策结合标准误与非对称删除代价，支持不足拒绝估计，无限不确定性返回 noop；它不是把每次负反馈都转成永久遗忘。 例如处理组两次恰好失败不足以证明有害，宽不确定性应促使继续保留或收集证据，而不是立即删除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-732a00c0f611285c">保护不确定记忆与按估计均值为负就删除有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acausal-memory-policy">Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Illinois Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>均值负但方差大、样本少时，真实效用可能仍为正，贸然删除有代价。CMP 的决策结合标准误与非对称删除代价，支持不足拒绝估计，无限不确定性返回 noop；它不是把每次负反馈都转成永久遗忘。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如处理组两次恰好失败不足以证明有害，宽不确定性应促使继续保留或收集证据，而不是立即删除。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02070">原论文</a> · <a href="../../../../agent-research/2610.02070-causal-memory-policy/">实现解读</a> · <a href="#qa-732a00c0f611285c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:causal-memory-policy" data-paper-title="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval Agent Illinois Institute of Technology 2026-10-01 被检索到的记忆与任务难度天然相关，直接按任务成败删除记忆存在选择偏差。CMP 在固定候选池中预留均衡随机曝光槽位，使每条记忆都有可估计的处理/对照样本，再用带标准误的效用判断保护不确定的记忆。 尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；L1 因果测量协议：实现均衡随机曝光、Hájek 估计及不确定性感知单 query 决策。不把它夸大为已验证的长期记忆清理策略。尚未运行真实 LLM 检索任务或跨 query 记忆删除实验；合成效用恢复不是 Agent 答题准确率，不进入能力排行榜或 Evolve 晋级证据。PYTHONPATH=src python scripts/run_oct04_seven_papers.py：12 条记忆、600 次检索、每次 2 槽，三 seed 合成外部结果。每条记忆曝光恰好 100 次；产物保留正负效用、标准误及 forget 判断。  因果检索干预 记忆管理 Agent 记忆与技能：让经验可取回、可失效 固定 k 曝光槽为什么使效应不能直接视作独立加性系数？ 多曝光一条记忆意味着固定槽内其他记忆的分布也变化，处理效应包含该随机设计下的替换净影响。设计每行 k 条、各列次数近似均衡，估计还需每臂至少两个观测；本地合成效用恢复不是跨 query 长期策略或真实答题准确率。 例如总共两个槽，加入甲会挤走其他候选，观察收益是“甲替代某些内容”的净效应，而非凭空新增甲的孤立贡献。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7827f7cfea1dba11">固定 k 曝光槽为什么使效应不能直接视作独立加性系数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acausal-memory-policy">Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Illinois Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多曝光一条记忆意味着固定槽内其他记忆的分布也变化，处理效应包含该随机设计下的替换净影响。设计每行 k 条、各列次数近似均衡，估计还需每臂至少两个观测；本地合成效用恢复不是跨 query 长期策略或真实答题准确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如总共两个槽，加入甲会挤走其他候选，观察收益是“甲替代某些内容”的净效应，而非凭空新增甲的孤立贡献。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02070">原论文</a> · <a href="../../../../agent-research/2610.02070-causal-memory-policy/">实现解读</a> · <a href="#qa-7827f7cfea1dba11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mem-plus-plus" data-paper-title="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents Agent The University of Texas at Austin 2026-10-01 写入时完整保留文档、日期和作者，不调用生成模型做不可逆摘要；读取时先按问题时间过滤，再融合 lexical 与 semantic ranking。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 记忆 时间检索 组织知识 Agent 记忆与技能：让经验可取回、可失效 Mem++ 的非破坏写入为什么同时保留日期和作者？ 原文内容提供事实，日期支持 as-of 查询与版本判断，作者保留来源责任和语境。写入不调用模型不可逆重写，因此后续问题可重新解释原记录；存原文仍不保证检索正确，也需要管理更多存储与读取成本。 例如同一政策被两人在不同日期更新，保留日期和作者才有机会区分旧建议与后来正式通知，而非把两者压成一句混合结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-mem-plus-plus-c101fe19" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-107269a5af712c2f">Mem++ 的非破坏写入为什么同时保留日期和作者？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amem-plus-plus">Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文内容提供事实，日期支持 as-of 查询与版本判断，作者保留来源责任和语境。写入不调用模型不可逆重写，因此后续问题可重新解释原记录；存原文仍不保证检索正确，也需要管理更多存储与读取成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一政策被两人在不同日期更新，保留日期和作者才有机会区分旧建议与后来正式通知，而非把两者压成一句混合结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02002">原论文</a> · <a href="../../../../agent-research/2610.02002-mem-plus-plus/">实现解读</a> · <a href="#qa-107269a5af712c2f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mem-plus-plus" data-paper-title="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents Agent The University of Texas at Austin 2026-10-01 写入时完整保留文档、日期和作者，不调用生成模型做不可逆摘要；读取时先按问题时间过滤，再融合 lexical 与 semantic ranking。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 记忆 时间检索 组织知识 Agent 记忆与技能：让经验可取回、可失效 为什么读取时先按问题时间过滤，比事后提醒模型“别用未来信息”更可靠？ 未来文档一旦进入上下文，模型即使被提醒也可能利用其中线索。先做时间资格过滤，让 lexical 与 semantic 排名只作用在当时可见资料上，直接控制信息边界；原文、日期与作者完整保留还支持事后追溯，但不等于检索总能找到正确记录。 例如回答三月时的组织决策，四月公布的调整不能进入候选，即使它与问题高度相似，也不能用于解释当时已知事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mem-plus-plus" data-paper-title="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents Agent The University of Texas at Austin 2026-10-01 写入时完整保留文档、日期和作者，不调用生成模型做不可逆摘要；读取时先按问题时间过滤，再融合 lexical 与 semantic ranking。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 记忆 时间检索 组织知识 Agent 记忆与技能：让经验可取回、可失效 先按时间过滤再做混合排序，与只把时间加入相似度特征有何不同？ 硬过滤把查询时点之后的记录直接排除，防止未来信息参与答案；软特征即使惩罚未来记录，也可能因相关分太高而选中。词法与语义融合在合法候选内进行，不能以更高检索分为理由突破时间可见性。 例如问六月一日当时政策，六月十日的新通知应先排除，而不是给它减一点分后仍可能排第一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-54c975b84b7d4d1c">先按时间过滤再做混合排序，与只把时间加入相似度特征有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amem-plus-plus">Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>硬过滤把查询时点之后的记录直接排除，防止未来信息参与答案；软特征即使惩罚未来记录，也可能因相关分太高而选中。词法与语义融合在合法候选内进行，不能以更高检索分为理由突破时间可见性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如问六月一日当时政策，六月十日的新通知应先排除，而不是给它减一点分后仍可能排第一。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02002">原论文</a> · <a href="../../../../agent-research/2610.02002-mem-plus-plus/">实现解读</a> · <a href="#qa-54c975b84b7d4d1c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mem-plus-plus" data-paper-title="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents Agent The University of Texas at Austin 2026-10-01 写入时完整保留文档、日期和作者，不调用生成模型做不可逆摘要；读取时先按问题时间过滤，再融合 lexical 与 semantic ranking。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。执行全量写入、as-of 过滤与混合检索；不运行 OrgMemBench 或外部 embedding 服务。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 记忆 时间检索 组织知识 Agent 记忆与技能：让经验可取回、可失效 本地全量写入与混合检索验证是否运行了 OrgMemBench 或外部 embedding 服务？ 没有。本地只执行原文保留、as-of 过滤和词法语义排名组合 reference，三 seed 输出验证机制不变量。原文组织记忆效果属于作者 benchmark，不能将本地预设向量或固定记录结果写成真实长期组织助理收益。 例如输入未来记录后确认它被过滤，可验证时间规则；没有真实组织问答与编码器时，不能计算可比的 OrgMemBench 能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5d808cecfe06482e">本地全量写入与混合检索验证是否运行了 OrgMemBench 或外部 embedding 服务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amem-plus-plus">Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地只执行原文保留、as-of 过滤和词法语义排名组合 reference，三 seed 输出验证机制不变量。原文组织记忆效果属于作者 benchmark，不能将本地预设向量或固定记录结果写成真实长期组织助理收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如输入未来记录后确认它被过滤，可验证时间规则；没有真实组织问答与编码器时，不能计算可比的 OrgMemBench 能力。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02002">原论文</a> · <a href="../../../../agent-research/2610.02002-mem-plus-plus/">实现解读</a> · <a href="#qa-5d808cecfe06482e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memfit" data-paper-title="MemFit: Efficient Long-Term Agentic Memory" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemFit: Efficient Long-Term Agentic Memory Agent 原文首页未列第一作者机构 2026-09-30 原始 turn 追加写入不改写，只用 segment summary 建索引；读取融合 lexical、semantic 与 rerank 信号，避免昂贵 LLM 写入。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 记忆 无损写入 混合检索 Agent 记忆与技能：让经验可取回、可失效 append-only 原始 turn 与 segment summary 各承担什么功能？ 原始 turn 作为不被重写的事实来源，segment summary 提供较紧凑的索引，读取时再结合词法、语义及重排信号找证据。索引摘要不是唯一真相，错漏可回到原文核查；无损追加也不意味着所有原文每轮都进入模型上下文。 例如摘要只写“讨论预算”，具体金额仍在原 turn；检索命中该段后应能回查金额，而不是从摘要猜数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memfit-d14853dc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4b853f8ead5db496">append-only 原始 turn 与 segment summary 各承担什么功能？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemfit">MemFit: Efficient Long-Term Agentic Memory</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始 turn 作为不被重写的事实来源，segment summary 提供较紧凑的索引，读取时再结合词法、语义及重排信号找证据。索引摘要不是唯一真相，错漏可回到原文核查；无损追加也不意味着所有原文每轮都进入模型上下文。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如摘要只写“讨论预算”，具体金额仍在原 turn；检索命中该段后应能回查金额，而不是从摘要猜数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00872">原论文</a> · <a href="../../../../agent-research/2610.00872-memfit/">实现解读</a> · <a href="#qa-4b853f8ead5db496">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memfit" data-paper-title="MemFit: Efficient Long-Term Agentic Memory" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemFit: Efficient Long-Term Agentic Memory Agent 原文首页未列第一作者机构 2026-09-30 原始 turn 追加写入不改写，只用 segment summary 建索引；读取融合 lexical、semantic 与 rerank 信号，避免昂贵 LLM 写入。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 记忆 无损写入 混合检索 Agent 记忆与技能：让经验可取回、可失效 append-only 原始 turn 与可检索 segment summary 为什么要分开保存？ 摘要适合建立紧凑索引，却可能遗漏细节；原始记录不改写，使后续精读仍有可追溯依据。写入不反复调用昂贵模型重构全部历史，读取再融合词法、语义和重排信号；索引命中只是入口，不能把摘要缺失的内容当成从未出现过。 例如摘要只标“讨论支付接口”，搜索后仍能读原始 turn 找到确切超时值；若只保留摘要，该数值就可能不可恢复。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memfit" data-paper-title="MemFit: Efficient Long-Term Agentic Memory" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemFit: Efficient Long-Term Agentic Memory Agent 原文首页未列第一作者机构 2026-09-30 原始 turn 追加写入不改写，只用 segment summary 建索引；读取融合 lexical、semantic 与 rerank 信号，避免昂贵 LLM 写入。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 记忆 无损写入 混合检索 Agent 记忆与技能：让经验可取回、可失效 便宜写入与每轮用 LLM 重写长期记忆有什么取舍？ append-only 避免反复生成摘要的成本和不可逆改写，代价是原文规模持续增加，读取与索引承担更多筛选工作。LLM 写入可提前抽象，但可能遗失细节；应把写入成本、存储和最终读取质量一起比较，而非只看某一步调用少。 例如保存一千轮原文很便宜，但后续必须从中快速找到一次更改地址；便宜写入不等于查询成本自动很低。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e107e4a047780dea">便宜写入与每轮用 LLM 重写长期记忆有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemfit">MemFit: Efficient Long-Term Agentic Memory</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>append-only 避免反复生成摘要的成本和不可逆改写，代价是原文规模持续增加，读取与索引承担更多筛选工作。LLM 写入可提前抽象，但可能遗失细节；应把写入成本、存储和最终读取质量一起比较，而非只看某一步调用少。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保存一千轮原文很便宜，但后续必须从中快速找到一次更改地址；便宜写入不等于查询成本自动很低。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00872">原论文</a> · <a href="../../../../agent-research/2610.00872-memfit/">实现解读</a> · <a href="#qa-e107e4a047780dea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memfit" data-paper-title="MemFit: Efficient Long-Term Agentic Memory" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemFit: Efficient Long-Term Agentic Memory Agent 原文首页未列第一作者机构 2026-09-30 原始 turn 追加写入不改写，只用 segment summary 建索引；读取融合 lexical、semantic 与 rerank 信号，避免昂贵 LLM 写入。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。执行无损追加和混合检索 hook；不调用 embedding/cross-encoder。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 记忆 无损写入 混合检索 Agent 记忆与技能：让经验可取回、可失效 本地 hybrid retrieval hook 能否表示已运行 embedding 与 cross-encoder？ 不能。hook 只是接入词法、语义和重排信号的接口，本地没有调用实际 embedding 或 cross-encoder。可检查追加不改写和排名组合，但语义分数若由 fixture 提供，不能据此声称真实长期对话检索质量或论文延迟已经复现。 例如给三条记录预设语义分后排序正确，验证的是组合函数；尚未测试模型能否从自然语言算出可靠的这些分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-499b4408c327aeaf">本地 hybrid retrieval hook 能否表示已运行 embedding 与 cross-encoder？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemfit">MemFit: Efficient Long-Term Agentic Memory</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。hook 只是接入词法、语义和重排信号的接口，本地没有调用实际 embedding 或 cross-encoder。可检查追加不改写和排名组合，但语义分数若由 fixture 提供，不能据此声称真实长期对话检索质量或论文延迟已经复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给三条记录预设语义分后排序正确，验证的是组合函数；尚未测试模型能否从自然语言算出可靠的这些分数。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00872">原论文</a> · <a href="../../../../agent-research/2610.00872-memfit/">实现解读</a> · <a href="#qa-499b4408c327aeaf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:context-lm" data-paper-title="Context Language Models" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Context Language Models Agent University of Washington / Meta Superintelligence Labs 2026-09-29 把上下文视为模型可直接编辑的文件，使保留、删除和重组信息成为模型行为，而不是外部 harness 的固定策略；多 Agent 各自维护 context file，服务端从第一个不匹配 token 起重新 prefill。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  上下文管理 Agent RL 多 Agent Agent 记忆与技能：让经验可取回、可失效 context file 为什么是模型行为的一部分，而不是固定外部摘要？ 模型可以直接决定保留、删除、重组上下文文件，后续行动读取它编辑后的状态。传统固定 harness 由外部规则决定何时压缩和保留什么，行为责任不同；让模型编辑也带来丢失关键约束的风险，仍要有容量与执行合同。 例如模型发现旧日志无用可主动删该段并保留结论，而不是等外部长度阈值统一摘要整段历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-context-lm-ca518f91" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1b83f4d20e64d534">context file 为什么是模型行为的一部分，而不是固定外部摘要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acontext-lm">Context Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington / Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型可以直接决定保留、删除、重组上下文文件，后续行动读取它编辑后的状态。传统固定 harness 由外部规则决定何时压缩和保留什么，行为责任不同；让模型编辑也带来丢失关键约束的风险，仍要有容量与执行合同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型发现旧日志无用可主动删该段并保留结论，而不是等外部长度阈值统一摘要整段历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37725">原论文</a> · <a href="../../../../agent-research/2609.37725-context-lm/">实现解读</a> · <a href="#qa-1b83f4d20e64d534">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:context-lm" data-paper-title="Context Language Models" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Context Language Models Agent University of Washington / Meta Superintelligence Labs 2026-09-29 把上下文视为模型可直接编辑的文件，使保留、删除和重组信息成为模型行为，而不是外部 harness 的固定策略；多 Agent 各自维护 context file，服务端从第一个不匹配 token 起重新 prefill。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  上下文管理 Agent RL 多 Agent Agent 记忆与技能：让经验可取回、可失效 让模型直接编辑 context file，为什么也会改变 KV 复用成本？ 上下文文件的前缀决定已计算缓存是否仍匹配；改动早期 token 后，后缀通常需要重新 prefill。模型因而不仅决定记住什么，还在用文件变换控制后续运行成本；删除更短未必总便宜，若破坏了大量缓存，重算代价也要算入。 例如在文件尾追加新观察可保留已有前缀缓存，若重写开头摘要，则即便总字数更少，也可能需要重算后面的整段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:context-lm" data-paper-title="Context Language Models" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Context Language Models Agent University of Washington / Meta Superintelligence Labs 2026-09-29 把上下文视为模型可直接编辑的文件，使保留、删除和重组信息成为模型行为，而不是外部 harness 的固定策略；多 Agent 各自维护 context file，服务端从第一个不匹配 token 起重新 prefill。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  上下文管理 Agent RL 多 Agent Agent 记忆与技能：让经验可取回、可失效 context 编辑与直接丢弃 KV cache 在逻辑记录上有何不同？ 文件编辑改变模型下一次看到的逻辑 token 序列，后续 cache 需要按前缀匹配重算；直接丢 KV 可保留逻辑记录却改变活跃缓存状态。二者操作对象不同，不能因为都降低活跃上下文就假设同样缓存身份或恢复语义。 例如删掉文件开头一段文字后，后续 token 前缀已变化，不能照搬原先整段 KV；只 drop KV 则可能仍保留原文本记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-84c99bee2b5a6493">context 编辑与直接丢弃 KV cache 在逻辑记录上有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acontext-lm">Context Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington / Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文件编辑改变模型下一次看到的逻辑 token 序列，后续 cache 需要按前缀匹配重算；直接丢 KV 可保留逻辑记录却改变活跃缓存状态。二者操作对象不同，不能因为都降低活跃上下文就假设同样缓存身份或恢复语义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如删掉文件开头一段文字后，后续 token 前缀已变化，不能照搬原先整段 KV；只 drop KV 则可能仍保留原文本记录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37725">原论文</a> · <a href="../../../../agent-research/2609.37725-context-lm/">实现解读</a> · <a href="#qa-84c99bee2b5a6493">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:context-lm" data-paper-title="Context Language Models" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Context Language Models Agent University of Washington / Meta Superintelligence Labs 2026-09-29 把上下文视为模型可直接编辑的文件，使保留、删除和重组信息成为模型行为，而不是外部 harness 的固定策略；多 Agent 各自维护 context file，服务端从第一个不匹配 token 起重新 prefill。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。执行 context-file 编辑和 suffix cache 边界；未训练 Qwen3.5-9B，也未运行 24 小时 Agent swarm。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  上下文管理 Agent RL 多 Agent Agent 记忆与技能：让经验可取回、可失效 为什么 suffix cache reuse 必须从首个 token mismatch 起重算？ 因果隐藏状态依赖先前 token，首个变化之后即使文本片段再次相同，其 KV 也可能不同。实现据最长共同前缀保留有效缓存，显式检查文件容量；本地仅做编辑和边界诊断，没有训练 CLM 或运行长时间多 Agent swarm。 例如第一百个 token 改了一个词，第一百零一个之后的状态都可能受影响，不能只重算被替换的那个位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-02bd02e85b8213dc">为什么 suffix cache reuse 必须从首个 token mismatch 起重算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acontext-lm">Context Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington / Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>因果隐藏状态依赖先前 token，首个变化之后即使文本片段再次相同，其 KV 也可能不同。实现据最长共同前缀保留有效缓存，显式检查文件容量；本地仅做编辑和边界诊断，没有训练 CLM 或运行长时间多 Agent swarm。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第一百个 token 改了一个词，第一百零一个之后的状态都可能受影响，不能只重算被替换的那个位置。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37725">原论文</a> · <a href="../../../../agent-research/2609.37725-context-lm/">实现解读</a> · <a href="#qa-02bd02e85b8213dc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:remem" data-paper-title="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents Agent The Hong Kong Polytechnic University 2026-09-29 推荐 Agent 一方面要从异构商品页稳定提取信息，另一方面不能把完整用户历史无限塞进上下文。ReMem 用 OCR 驱动的多模态 item perception 生成紧凑语义表示，再以固定预算、随时间更新的 dynamic memory 保存偏好；Multi-Memory GRPO 让多个记忆视图共享策略更新。 复现级别：L1 记忆机制。复现级别：L1 记忆机制。实现固定预算的 time-evolving memory 和 multi-memory GRPO 目标；未接入真实购物网页与 OCR 模型。这里不是完整网页 Agent：未运行 OCR、浏览器、作者数据或真实 episode；固定小样本只用于验证信息流，不能宣传为推荐能力提升。  长期记忆 推荐 Agent 多模态感知 Agent 记忆与技能：让经验可取回、可失效 ReMem 为什么把商品感知和用户记忆视为两个问题？ 异构商品页需要从文本和图像中稳定提取 item 信息，长期用户历史则需要在固定预算内保留随时间变化的偏好。前者关注当前物品证据，后者关注偏好演化，不能把 OCR 提取准确率当成推荐效果，也不能只压缩历史而假定商品输入已可靠。 例如用户最近改偏好为轻便鞋，系统既要读出网页商品重量，也要更新旧的“偏好厚底”记忆，两个环节缺一不可。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-remem-598e18f2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8426a6e9fbacaf9f">ReMem 为什么把商品感知和用户记忆视为两个问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aremem">ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>异构商品页需要从文本和图像中稳定提取 item 信息，长期用户历史则需要在固定预算内保留随时间变化的偏好。前者关注当前物品证据，后者关注偏好演化，不能把 OCR 提取准确率当成推荐效果，也不能只压缩历史而假定商品输入已可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户最近改偏好为轻便鞋，系统既要读出网页商品重量，也要更新旧的“偏好厚底”记忆，两个环节缺一不可。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37311">原论文</a> · <a href="../../../../agent-research/2609.37311-remem/">实现解读</a> · <a href="#qa-8426a6e9fbacaf9f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:remem" data-paper-title="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents Agent The Hong Kong Polytechnic University 2026-09-29 推荐 Agent 一方面要从异构商品页稳定提取信息，另一方面不能把完整用户历史无限塞进上下文。ReMem 用 OCR 驱动的多模态 item perception 生成紧凑语义表示，再以固定预算、随时间更新的 dynamic memory 保存偏好；Multi-Memory GRPO 让多个记忆视图共享策略更新。 复现级别：L1 记忆机制。复现级别：L1 记忆机制。实现固定预算的 time-evolving memory 和 multi-memory GRPO 目标；未接入真实购物网页与 OCR 模型。这里不是完整网页 Agent：未运行 OCR、浏览器、作者数据或真实 episode；固定小样本只用于验证信息流，不能宣传为推荐能力提升。  长期记忆 推荐 Agent 多模态感知 Agent 记忆与技能：让经验可取回、可失效 为什么推荐 Agent 要同时改 item perception 和有界记忆，而不能只把用户历史压短？ 页面信息若提取错误，后续偏好记忆再精巧也只是在保存错误语义。OCR 驱动的感知先形成紧凑 item 表示，动态记忆再在预算内更新用户偏好；多记忆视图共享策略训练，用不同证据视角评价行为，但不应把测试偏好答案注入记忆来制造提升。 例如商品价格藏在图片小字里，单压缩浏览历史无法纠正读错价格；先提取可靠属性，再保留与用户预算有关的信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:remem" data-paper-title="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents Agent The Hong Kong Polytechnic University 2026-09-29 推荐 Agent 一方面要从异构商品页稳定提取信息，另一方面不能把完整用户历史无限塞进上下文。ReMem 用 OCR 驱动的多模态 item perception 生成紧凑语义表示，再以固定预算、随时间更新的 dynamic memory 保存偏好；Multi-Memory GRPO 让多个记忆视图共享策略更新。 复现级别：L1 记忆机制。复现级别：L1 记忆机制。实现固定预算的 time-evolving memory 和 multi-memory GRPO 目标；未接入真实购物网页与 OCR 模型。这里不是完整网页 Agent：未运行 OCR、浏览器、作者数据或真实 episode；固定小样本只用于验证信息流，不能宣传为推荐能力提升。  长期记忆 推荐 Agent 多模态感知 Agent 记忆与技能：让经验可取回、可失效 动态固定预算记忆与完整历史上下文有什么取舍？ 完整历史保留多但成本随交互增长，动态记忆依据相关性和近期性更新，在预算内突出当前偏好，也可能丢失低频但重要限制。保留最近观测不能替代长期事实审计，是否提高推荐质量仍需真实用户 episode 而非记忆长度检查。 例如最近买了跑鞋不应自动抹去长期过敏材质限制；压缩后还需确认这些约束是否被可靠保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e31f4ffd2401e801">动态固定预算记忆与完整历史上下文有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aremem">ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整历史保留多但成本随交互增长，动态记忆依据相关性和近期性更新，在预算内突出当前偏好，也可能丢失低频但重要限制。保留最近观测不能替代长期事实审计，是否提高推荐质量仍需真实用户 episode 而非记忆长度检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最近买了跑鞋不应自动抹去长期过敏材质限制；压缩后还需确认这些约束是否被可靠保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37311">原论文</a> · <a href="../../../../agent-research/2609.37311-remem/">实现解读</a> · <a href="#qa-e31f4ffd2401e801">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:remem" data-paper-title="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents Agent The Hong Kong Polytechnic University 2026-09-29 推荐 Agent 一方面要从异构商品页稳定提取信息，另一方面不能把完整用户历史无限塞进上下文。ReMem 用 OCR 驱动的多模态 item perception 生成紧凑语义表示，再以固定预算、随时间更新的 dynamic memory 保存偏好；Multi-Memory GRPO 让多个记忆视图共享策略更新。 复现级别：L1 记忆机制。复现级别：L1 记忆机制。实现固定预算的 time-evolving memory 和 multi-memory GRPO 目标；未接入真实购物网页与 OCR 模型。这里不是完整网页 Agent：未运行 OCR、浏览器、作者数据或真实 episode；固定小样本只用于验证信息流，不能宣传为推荐能力提升。  长期记忆 推荐 Agent 多模态感知 Agent 记忆与技能：让经验可取回、可失效 Multi-Memory GRPO 为什么不能把所有记忆视图混成一个优势组？ 同一 query 的不同 memory view 应分别做组内奖励标准化，再共享 clipped policy 更新；混为一组会把视图难度差当动作优势。本地只验证预算、时间更新与目标公式，未运行 OCR、浏览器或真实推荐 episode，不宣称推荐能力提升。 例如稀疏记忆视图奖励整体较低，若与丰富视图直接混组，可能把难度差错误归给同一策略的具体回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4a97e3877c77acd7">Multi-Memory GRPO 为什么不能把所有记忆视图混成一个优势组？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aremem">ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong Polytechnic University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一 query 的不同 memory view 应分别做组内奖励标准化，再共享 clipped policy 更新；混为一组会把视图难度差当动作优势。本地只验证预算、时间更新与目标公式，未运行 OCR、浏览器或真实推荐 episode，不宣称推荐能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如稀疏记忆视图奖励整体较低，若与丰富视图直接混组，可能把难度差错误归给同一策略的具体回答。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37311">原论文</a> · <a href="../../../../agent-research/2609.37311-remem/">实现解读</a> · <a href="#qa-4a97e3877c77acd7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:upliftmem" data-paper-title="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval Agent Beihang University 2026-09-29 相关记忆不一定提升执行。UpliftMem 以同一冻结 executor 在“使用完整 memory set”和“不使用 memory”时的结果差作为 supervision，并在集合级建模互补、冗余和冲突。候选集合太多无法全跑时，用相关 Gaussian 后验下的 EVSI 把额外 rollout 分配给最可能改变局部检索决策的集合。 复现级别：L1 uplift 与 probe 机制。复现级别：L1 uplift 与 probe 机制。实现同 executor 的 paired uplift 和相关 Gaussian EVSI 选择。本地 set_level_uplift 强制 paired treatment/control；gaussian_evsi 在固定 posterior 上选 probe；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现完整 set constructor、共享 scorer、ALFWorld/WebShop/BigCodeBench 执行器，因此只作为机制与评测基础设施。  Agent 记忆 集合 uplift 主动探测 Agent 记忆与技能：让经验可取回、可失效 为什么 UpliftMem 直接估计整个 memory set 的收益？ 记忆之间可能互补、重复或冲突，单条相关性之和不能表达这些集合效应。它用同一冻结 executor 在完整集合与无记忆条件下的配对结果差作监督，目标是执行增益而非文本相似；收益也依赖该 executor 与任务分布，不能视为记忆固有常数。 例如甲说明工具参数、乙说明异常处理，两条一起才帮助完成任务；分别看每条可能都没有明显收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-upliftmem-e7065d9f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8147d2ef26cbd835">为什么 UpliftMem 直接估计整个 memory set 的收益？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aupliftmem">UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>记忆之间可能互补、重复或冲突，单条相关性之和不能表达这些集合效应。它用同一冻结 executor 在完整集合与无记忆条件下的配对结果差作监督，目标是执行增益而非文本相似；收益也依赖该 executor 与任务分布，不能视为记忆固有常数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如甲说明工具参数、乙说明异常处理，两条一起才帮助完成任务；分别看每条可能都没有明显收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36805">原论文</a> · <a href="../../../../agent-research/2609.36805-upliftmem/">实现解读</a> · <a href="#qa-8147d2ef26cbd835">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:upliftmem" data-paper-title="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval Agent Beihang University 2026-09-29 相关记忆不一定提升执行。UpliftMem 以同一冻结 executor 在“使用完整 memory set”和“不使用 memory”时的结果差作为 supervision，并在集合级建模互补、冗余和冲突。候选集合太多无法全跑时，用相关 Gaussian 后验下的 EVSI 把额外 rollout 分配给最可能改变局部检索决策的集合。 复现级别：L1 uplift 与 probe 机制。复现级别：L1 uplift 与 probe 机制。实现同 executor 的 paired uplift 和相关 Gaussian EVSI 选择。本地 set_level_uplift 强制 paired treatment/control；gaussian_evsi 在固定 posterior 上选 probe；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现完整 set constructor、共享 scorer、ALFWorld/WebShop/BigCodeBench 执行器，因此只作为机制与评测基础设施。  Agent 记忆 集合 uplift 主动探测 Agent 记忆与技能：让经验可取回、可失效 为什么 memory set 的效用不能直接等于各条记忆相关性之和？ 条目之间可能互补、重复或冲突，集合整体对执行的影响不是单项分数简单相加。方法用同一冻结 executor 的有记忆与无记忆结果差作监督，额外 rollout 再按能否改变局部选择分配；相关性只是候选线索，不等于实际任务增益。 例如一条给接口名、一条给参数约束，合用才可执行；两份重复接口简介即使都相似，也未必比这组互补证据更有用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:upliftmem" data-paper-title="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval Agent Beihang University 2026-09-29 相关记忆不一定提升执行。UpliftMem 以同一冻结 executor 在“使用完整 memory set”和“不使用 memory”时的结果差作为 supervision，并在集合级建模互补、冗余和冲突。候选集合太多无法全跑时，用相关 Gaussian 后验下的 EVSI 把额外 rollout 分配给最可能改变局部检索决策的集合。 复现级别：L1 uplift 与 probe 机制。复现级别：L1 uplift 与 probe 机制。实现同 executor 的 paired uplift 和相关 Gaussian EVSI 选择。本地 set_level_uplift 强制 paired treatment/control；gaussian_evsi 在固定 posterior 上选 probe；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现完整 set constructor、共享 scorer、ALFWorld/WebShop/BigCodeBench 执行器，因此只作为机制与评测基础设施。  Agent 记忆 集合 uplift 主动探测 Agent 记忆与技能：让经验可取回、可失效 EVSI 分配额外 rollout 与平均给每个候选相同次数有什么不同？ 平均分配不考虑不确定性会否影响最终选择，EVSI 关注一次新观测预期能否改变局部检索决策。相关 Gaussian 后验还表达候选之间依赖；这是一种预算分配规则，不意味着预测均值最高的集合已经实际执行成功。 例如两个集合差距很大时继续探测可能价值低，两个接近且不确定的候选更值得花一轮执行来区分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-247598bcebcf4e66">EVSI 分配额外 rollout 与平均给每个候选相同次数有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aupliftmem">UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平均分配不考虑不确定性会否影响最终选择，EVSI 关注一次新观测预期能否改变局部检索决策。相关 Gaussian 后验还表达候选之间依赖；这是一种预算分配规则，不意味着预测均值最高的集合已经实际执行成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个集合差距很大时继续探测可能价值低，两个接近且不确定的候选更值得花一轮执行来区分。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36805">原论文</a> · <a href="../../../../agent-research/2609.36805-upliftmem/">实现解读</a> · <a href="#qa-247598bcebcf4e66">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:upliftmem" data-paper-title="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval Agent Beihang University 2026-09-29 相关记忆不一定提升执行。UpliftMem 以同一冻结 executor 在“使用完整 memory set”和“不使用 memory”时的结果差作为 supervision，并在集合级建模互补、冗余和冲突。候选集合太多无法全跑时，用相关 Gaussian 后验下的 EVSI 把额外 rollout 分配给最可能改变局部检索决策的集合。 复现级别：L1 uplift 与 probe 机制。复现级别：L1 uplift 与 probe 机制。实现同 executor 的 paired uplift 和相关 Gaussian EVSI 选择。本地 set_level_uplift 强制 paired treatment/control；gaussian_evsi 在固定 posterior 上选 probe；三种子机制结果见 metrics/mechanism-seeds42-44.json。未实现完整 set constructor、共享 scorer、ALFWorld/WebShop/BigCodeBench 执行器，因此只作为机制与评测基础设施。  Agent 记忆 集合 uplift 主动探测 Agent 记忆与技能：让经验可取回、可失效 set_level_uplift 为什么必须要求 paired treatment/control？ 同一任务、冻结 executor 与匹配条件下比较有记忆和无记忆，才能减少任务或模型变化带来的混杂。本地只实现配对差与固定 posterior 的 EVSI，没有完整集合构造、共享 scorer 或真实环境 executor，因此组件计算不能当 Agent 成功率提升。 例如甲集合在难题上、无记忆在简单题上跑出的分数差没有可比性；必须让两种条件面对同一个任务实例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fb77451d166994c2">set_level_uplift 为什么必须要求 paired treatment/control？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aupliftmem">UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一任务、冻结 executor 与匹配条件下比较有记忆和无记忆，才能减少任务或模型变化带来的混杂。本地只实现配对差与固定 posterior 的 EVSI，没有完整集合构造、共享 scorer 或真实环境 executor，因此组件计算不能当 Agent 成功率提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如甲集合在难题上、无记忆在简单题上跑出的分数差没有可比性；必须让两种条件面对同一个任务实例。</p>
<p class="ar-learning-sources">依据：本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36805">原论文</a> · <a href="../../../../agent-research/2609.36805-upliftmem/">实现解读</a> · <a href="#qa-fb77451d166994c2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ccm" data-paper-title="Continuous Context Management" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Continuous Context Management Agent University of Miami 2026-09-28 每轮输出动作和更新后的有界 memory；下一轮只读原任务、memory 与最新 observation，并用完整历史只在训练侧提供 privileged distillation。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  上下文管理 Agent RL Agent 记忆与技能：让经验可取回、可失效 CCM 下一轮为什么只读任务、memory 和最新 observation？ 它要求每轮用有界 memory 承接过去的必要状态，避免完整历史不断增长。动作与新 memory 一起输出，形成持续状态更新；若实际仍把完整历史拼回下一轮，就绕过记忆压缩任务，也无法检验 memory 是否足够支持后续决策。 例如第一轮读到订单号后写入 memory，第二轮只看该 memory 与新工具结果，不能再从隐藏完整对话抄回遗漏编号。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-ccm-d42ba3fe" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6254981077290624">CCM 下一轮为什么只读任务、memory 和最新 observation？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Accm">Continuous Context Management</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Miami</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它要求每轮用有界 memory 承接过去的必要状态，避免完整历史不断增长。动作与新 memory 一起输出，形成持续状态更新；若实际仍把完整历史拼回下一轮，就绕过记忆压缩任务，也无法检验 memory 是否足够支持后续决策。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第一轮读到订单号后写入 memory，第二轮只看该 memory 与新工具结果，不能再从隐藏完整对话抄回遗漏编号。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35540">原论文</a> · <a href="../../../../agent-research/2609.35540-ccm/">实现解读</a> · <a href="#qa-6254981077290624">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ccm" data-paper-title="Continuous Context Management" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Continuous Context Management Agent University of Miami 2026-09-28 每轮输出动作和更新后的有界 memory；下一轮只读原任务、memory 与最新 observation，并用完整历史只在训练侧提供 privileged distillation。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  上下文管理 Agent RL Agent 记忆与技能：让经验可取回、可失效 训练教师能看完整历史时，为什么学生下一轮仍只能读有界 memory？ 特权历史用于给训练信号，学生部署接口仍受原任务、记忆和最新观察限制，这样才能学会把必要状态写入有限空间。若评测时把完整历史也补给学生，便绕过了连续管理的难题；记忆更新与动作一起输出，意味着保存选择必须服务下一步行为。 例如教师知道早先提过的端口号，学生应把它写入小记忆供后续使用；测试时不能直接把整段旧对话重新塞回来。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ccm" data-paper-title="Continuous Context Management" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Continuous Context Management Agent University of Miami 2026-09-28 每轮输出动作和更新后的有界 memory；下一轮只读原任务、memory 与最新 observation，并用完整历史只在训练侧提供 privileged distillation。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  上下文管理 Agent RL Agent 记忆与技能：让经验可取回、可失效 privileged full-history teacher 与部署学生的可见信息为什么不同？ 教师可在训练侧用完整历史提供更可靠监督，学生则必须仅凭受限上下文学习行动和记忆更新。若把教师历史直接传给学生，会消除所需信息瓶颈；训练监督更强也不表示部署时获得同样信息，效果应在真实受限路径评估。 例如教师知道前十轮的全部细节，可指导学生保留关键事实，但测试学生仍只能读取自己维护的短 memory。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-70af81e05a5b670f">privileged full-history teacher 与部署学生的可见信息为什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Accm">Continuous Context Management</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Miami</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教师可在训练侧用完整历史提供更可靠监督，学生则必须仅凭受限上下文学习行动和记忆更新。若把教师历史直接传给学生，会消除所需信息瓶颈；训练监督更强也不表示部署时获得同样信息，效果应在真实受限路径评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师知道前十轮的全部细节，可指导学生保留关键事实，但测试学生仍只能读取自己维护的短 memory。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35540">原论文</a> · <a href="../../../../agent-research/2609.35540-ccm/">实现解读</a> · <a href="#qa-70af81e05a5b670f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ccm" data-paper-title="Continuous Context Management" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Continuous Context Management Agent University of Miami 2026-09-28 每轮输出动作和更新后的有界 memory；下一轮只读原任务、memory 与最新 observation，并用完整历史只在训练侧提供 privileged distillation。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。执行逐轮有界上下文契约；未运行 TerminalBench 或 WebShop checkpoint。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  上下文管理 Agent RL Agent 记忆与技能：让经验可取回、可失效 如何检查 CCM 没有借未记录历史绕过有界上下文？ 检查每轮 policy 请求只含原任务、当前 memory 和最新观察，旧工具结果只有被写入 memory 才可见，并对 memory 施明确容量限制。本地只验这些状态合同，未运行 TerminalBench 或 WebShop checkpoint，不能把字段隔离测试当任务能力。 例如把前一轮完整 transcript 藏在一个额外 metadata 字段也会破坏合同，即使主 prompt 看起来已经缩短。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7faceb47315133fb">如何检查 CCM 没有借未记录历史绕过有界上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Accm">Continuous Context Management</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Miami</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>检查每轮 policy 请求只含原任务、当前 memory 和最新观察，旧工具结果只有被写入 memory 才可见，并对 memory 施明确容量限制。本地只验这些状态合同，未运行 TerminalBench 或 WebShop checkpoint，不能把字段隔离测试当任务能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把前一轮完整 transcript 藏在一个额外 metadata 字段也会破坏合同，即使主 prompt 看起来已经缩短。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.35540">原论文</a> · <a href="../../../../agent-research/2609.35540-ccm/">实现解读</a> · <a href="#qa-7faceb47315133fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mnemon" data-paper-title="Mnemon: Raw Records, Fast Judgments, Slow Thoughts" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mnemon: Raw Records, Fast Judgments, Slow Thoughts Agent 原文未列机构 2026-09-28 保存原始带日期记录，由慢速规划生成搜索、快速 Jev 判断记录是否需要，再在预算内构造供原回答模型使用的小视图。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  长期记忆 Jev System 1/2 Agent 记忆与技能：让经验可取回、可失效 Mnemon 为什么保留带日期原记录，却只给回答模型一个小视图？ 原记录保留可核查细节与时间来源，小视图在当前预算内提供必要证据，避免完整历史反复占上下文。慢规划生成搜索，快速 Jev 判断记录是否需要，两者服务于证据筛选；小视图遗漏时仍需回查，不能视为无损概括全部历史。 例如问最近一次改期，可从多年原记录中挑出相关几条带日期事件，而不把全部聊天重新发给回答模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-mnemon-dd3564ee" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f832a1b58f4143d5">Mnemon 为什么保留带日期原记录，却只给回答模型一个小视图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amnemon">Mnemon: Raw Records, Fast Judgments, Slow Thoughts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原记录保留可核查细节与时间来源，小视图在当前预算内提供必要证据，避免完整历史反复占上下文。慢规划生成搜索，快速 Jev 判断记录是否需要，两者服务于证据筛选；小视图遗漏时仍需回查，不能视为无损概括全部历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如问最近一次改期，可从多年原记录中挑出相关几条带日期事件，而不把全部聊天重新发给回答模型。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36059">原论文</a> · <a href="../../../../agent-research/2609.36059-mnemon/">实现解读</a> · <a href="#qa-f832a1b58f4143d5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mnemon" data-paper-title="Mnemon: Raw Records, Fast Judgments, Slow Thoughts" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mnemon: Raw Records, Fast Judgments, Slow Thoughts Agent 原文未列机构 2026-09-28 保存原始带日期记录，由慢速规划生成搜索、快速 Jev 判断记录是否需要，再在预算内构造供原回答模型使用的小视图。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  长期记忆 Jev System 1/2 Agent 记忆与技能：让经验可取回、可失效 为什么慢速搜索规划与快速记录判断要拆开，而不是每条记录都长推理？ 搜索规划决定下一步去哪里找证据，逐条资格判断则更适合受限快速决策；分开能把推理预算集中在检索方向，而非重复解释每份候选。原始带日期记录仍保留，最终回答只读预算内小视图；快速判断本身不保证证据完备或时间边界正确。 例如先决定查某次发布会议，再快速筛选几十条记录是否相关，最后把少量原文交给回答器，而不对每条写长篇分析。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mnemon" data-paper-title="Mnemon: Raw Records, Fast Judgments, Slow Thoughts" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mnemon: Raw Records, Fast Judgments, Slow Thoughts Agent 原文未列机构 2026-09-28 保存原始带日期记录，由慢速规划生成搜索、快速 Jev 判断记录是否需要，再在预算内构造供原回答模型使用的小视图。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  长期记忆 Jev System 1/2 Agent 记忆与技能：让经验可取回、可失效 慢规划与快速记录判断相比，用一个模型一步做完检索有什么取舍？ 分工让较昂贵推理决定搜索方向、较便宜判断筛候选，试图降低大量记录逐条处理成本。一阶段可更简单，却可能在搜索策略或细筛上花不均衡预算；实际优势取决于判断器可靠性与总调用成本，不能由快慢命名直接得出。 例如先规划“找三月会议改期”，再快速淘汰无关生日记录；若快判误删真正改期记录，慢规划也无法弥补。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1831a12ab0dad173">慢规划与快速记录判断相比，用一个模型一步做完检索有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amnemon">Mnemon: Raw Records, Fast Judgments, Slow Thoughts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分工让较昂贵推理决定搜索方向、较便宜判断筛候选，试图降低大量记录逐条处理成本。一阶段可更简单，却可能在搜索策略或细筛上花不均衡预算；实际优势取决于判断器可靠性与总调用成本，不能由快慢命名直接得出。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先规划“找三月会议改期”，再快速淘汰无关生日记录；若快判误删真正改期记录，慢规划也无法弥补。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36059">原论文</a> · <a href="../../../../agent-research/2609.36059-mnemon/">实现解读</a> · <a href="#qa-1831a12ab0dad173">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mnemon" data-paper-title="Mnemon: Raw Records, Fast Judgments, Slow Thoughts" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Mnemon: Raw Records, Fast Judgments, Slow Thoughts Agent 原文未列机构 2026-09-28 保存原始带日期记录，由慢速规划生成搜索、快速 Jev 判断记录是否需要，再在预算内构造供原回答模型使用的小视图。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。执行 raw-record 检索和有界 view；未加载 Jev checkpoint 或复述 LoCoMo 分数。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  长期记忆 Jev System 1/2 Agent 记忆与技能：让经验可取回、可失效 本地 bounded view 验证是否覆盖 Jev 语义判断与原回答模型？ 没有。本地只执行 raw-record 检索与预算内视图构造，未加载 Jev checkpoint，也不复述 LoCoMo 分数。记录顺序、日期与预算可以独立核对，但需要真实模型才可评价哪些记录语义上必要，以及原回答器是否能用其正确回答。 例如测试把三条指定记录装进容量内，说明视图接口正常；它没证明判断器能从自然语言自行选中那三条。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-421fc3dc6770c6a3">本地 bounded view 验证是否覆盖 Jev 语义判断与原回答模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amnemon">Mnemon: Raw Records, Fast Judgments, Slow Thoughts</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地只执行 raw-record 检索与预算内视图构造，未加载 Jev checkpoint，也不复述 LoCoMo 分数。记录顺序、日期与预算可以独立核对，但需要真实模型才可评价哪些记录语义上必要，以及原回答器是否能用其正确回答。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如测试把三条指定记录装进容量内，说明视图接口正常；它没证明判断器能从自然语言自行选中那三条。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36059">原论文</a> · <a href="../../../../agent-research/2609.36059-mnemon/">实现解读</a> · <a href="#qa-421fc3dc6770c6a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoskill-gui" data-paper-title="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents Agent Zhejiang University 2026-09-15 把 GUI 技能拆成可编辑组件，执行失败后由信息隔离 critic 反思，并只修改责任组件，验证后的技能可跨任务复用。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。  GUI Agent 技能进化 Agent 记忆与技能：让经验可取回、可失效 GUI 技能为什么拆成可编辑组件，而不是一段不可分脚本？ 组件化让失败能定位到感知、条件、动作或验证等责任环节，修订时只改相关部分，降低无关步骤回归风险。完整技能仍需在实际 GUI 状态下验证，组件接口合法不表示屏幕定位或操作语义可靠，也不能把所有失败都归给最后一步动作。 例如登录失败来自按钮位置变化时，可改定位组件，不必把凭据处理和后续导航全部重写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-evoskill-gui-aeb4c952" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-37640d1b810cdf3f">GUI 技能为什么拆成可编辑组件，而不是一段不可分脚本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoskill-gui">Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>组件化让失败能定位到感知、条件、动作或验证等责任环节，修订时只改相关部分，降低无关步骤回归风险。完整技能仍需在实际 GUI 状态下验证，组件接口合法不表示屏幕定位或操作语义可靠，也不能把所有失败都归给最后一步动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如登录失败来自按钮位置变化时，可改定位组件，不必把凭据处理和后续导航全部重写。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17653">原论文</a> · <a href="../../../../agent-research/2609.17653-evoskill-gui/">实现解读</a> · <a href="#qa-37640d1b810cdf3f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoskill-gui" data-paper-title="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents Agent Zhejiang University 2026-09-15 把 GUI 技能拆成可编辑组件，执行失败后由信息隔离 critic 反思，并只修改责任组件，验证后的技能可跨任务复用。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。  GUI Agent 技能进化 Agent 记忆与技能：让经验可取回、可失效 失败后只修改责任技能组件，为什么比重新生成整份 GUI 技能更可审计？ 局部修改把失败证据与具体部件关联，保留已验证的其他行为，便于确认改动是否解决原缺陷而非引入大范围漂移。critic 还需信息隔离，不能凭隐藏答案给出神奇补丁；修改后的技能必须再验证，才有理由在其他任务中复用。 例如登录技能只在弹窗关闭步骤失败，应先修正该组件的定位条件，而不把输入用户名、提交等已经可靠的部分一起重写。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoskill-gui" data-paper-title="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents Agent Zhejiang University 2026-09-15 把 GUI 技能拆成可编辑组件，执行失败后由信息隔离 critic 反思，并只修改责任组件，验证后的技能可跨任务复用。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。  GUI Agent 技能进化 Agent 记忆与技能：让经验可取回、可失效 隔离 critic 的局部修订与执行 Agent 随手自改有什么差别？ critic 依据允许的执行证据独立分析责任，限制补丁范围，再通过验证后复用；随手自改可能把执行时的错误假设继续带入修复。隔离并非保证判断正确，而是控制信息与责任边界，需要保留失败证据及验证结果。 例如执行器误以为页面加载完成，critic 应能从观察发现等待条件不足，而不是直接沿用“按钮不存在”的错误结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a807ac97630fd951">隔离 critic 的局部修订与执行 Agent 随手自改有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoskill-gui">Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>critic 依据允许的执行证据独立分析责任，限制补丁范围，再通过验证后复用；随手自改可能把执行时的错误假设继续带入修复。隔离并非保证判断正确，而是控制信息与责任边界，需要保留失败证据及验证结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如执行器误以为页面加载完成，critic 应能从观察发现等待条件不足，而不是直接沿用“按钮不存在”的错误结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17653">原论文</a> · <a href="../../../../agent-research/2609.17653-evoskill-gui/">实现解读</a> · <a href="#qa-a807ac97630fd951">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:evoskill-gui" data-paper-title="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents Agent Zhejiang University 2026-09-15 把 GUI 技能拆成可编辑组件，执行失败后由信息隔离 critic 反思，并只修改责任组件，验证后的技能可跨任务复用。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。本地只从公开 observation 读证据并演示受限技能修订；未运行 MobileWorld/AndroidWorld/OSWorld。  GUI Agent 技能进化 Agent 记忆与技能：让经验可取回、可失效 本地公开 observation 修订演示能验证真实 GUI 跨任务复用吗？ 不能。当前只从公开观察读取证据、执行受限技能修改 reference，未运行 MobileWorld、AndroidWorld 或 OSWorld。可验证不读 gold、补丁范围与状态转换，但真实屏幕理解、点击执行及验证后的跨任务成功率仍未建立。 例如字符串里按钮名变了后成功替换定位规则，只能证明补丁合同，不说明系统能在实际截图中找到新按钮。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8dc3dffbfabb507d">本地公开 observation 修订演示能验证真实 GUI 跨任务复用吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aevoskill-gui">Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前只从公开观察读取证据、执行受限技能修改 reference，未运行 MobileWorld、AndroidWorld 或 OSWorld。可验证不读 gold、补丁范围与状态转换，但真实屏幕理解、点击执行及验证后的跨任务成功率仍未建立。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如字符串里按钮名变了后成功替换定位规则，只能证明补丁合同，不说明系统能在实际截图中找到新按钮。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17653">原论文</a> · <a href="../../../../agent-research/2609.17653-evoskill-gui/">实现解读</a> · <a href="#qa-8dc3dffbfabb507d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:interactive-memory" data-paper-title="Interactive Memory Learning for Long-Term Conversations" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Interactive Memory Learning for Long-Term Conversations Agent Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory 2026-09-15 Planner 决定写入高价值记忆，Trigger 决定何时取回，两者通过跨会话延迟奖励共同演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  长期记忆 多 Agent 强化学习 Agent 记忆与技能：让经验可取回、可失效 Planner 写入与 Trigger 取回为何需要共同学习？ 写入决定未来有哪些信息可用，触发决定何时把它带入当前对话，两者对最终回答共同负责。仅优化写入可能存了很多却从不取回，仅优化触发又可能找不到没保存的事实；跨会话延迟奖励将早期选择与后续用途联系起来。 例如用户第一天提到食物过敏，Planner 要保存，第三天点餐时 Trigger 要适时取回，任一环节失效都会影响回答。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-interactive-memory-e350b33d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-705ddd2a1311bf6e">Planner 写入与 Trigger 取回为何需要共同学习？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ainteractive-memory">Interactive Memory Learning for Long-Term Conversations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>写入决定未来有哪些信息可用，触发决定何时把它带入当前对话，两者对最终回答共同负责。仅优化写入可能存了很多却从不取回，仅优化触发又可能找不到没保存的事实；跨会话延迟奖励将早期选择与后续用途联系起来。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户第一天提到食物过敏，Planner 要保存，第三天点餐时 Trigger 要适时取回，任一环节失效都会影响回答。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17088">原论文</a> · <a href="../../../../agent-research/2609.17088-interactive-memory/">实现解读</a> · <a href="#qa-705ddd2a1311bf6e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:interactive-memory" data-paper-title="Interactive Memory Learning for Long-Term Conversations" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Interactive Memory Learning for Long-Term Conversations Agent Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory 2026-09-15 Planner 决定写入高价值记忆，Trigger 决定何时取回，两者通过跨会话延迟奖励共同演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  长期记忆 多 Agent 强化学习 Agent 记忆与技能：让经验可取回、可失效 写入 Planner 与读取 Trigger 为什么需要跨会话延迟奖励共同学习？ 有些信息写下时看不出用途，直到后续会话才知道是否值得保存；读取时机又决定这些信息能否真正影响任务。共同延迟奖励连接写入选择和以后取用，避免只奖励当前摘要质量；评估仍须按时间先后，不能用未来问题提前挑选应写内容。 例如今天记下用户换了工作地点，下一周规划通勤才体现价值；若只看当天聊天流畅度，可能永远学不到这条记忆该保存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:interactive-memory" data-paper-title="Interactive Memory Learning for Long-Term Conversations" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Interactive Memory Learning for Long-Term Conversations Agent Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory 2026-09-15 Planner 决定写入高价值记忆，Trigger 决定何时取回，两者通过跨会话延迟奖励共同演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  长期记忆 多 Agent 强化学习 Agent 记忆与技能：让经验可取回、可失效 跨会话延迟奖励与每轮按检索相似度奖励有什么区别？ 相似度是即时代理，未必代表之后实际有用；延迟奖励观察后续对话结果，试图学习长期写入和触发价值。它也带来信用分配难题，不能把未来问题提前给写入器降低难度，否则不再是面向未知未来的记忆学习。 例如一条低频过敏信息当时与话题不太相似，却在后续点餐很关键；即时相似度可能低估它的长期价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-90095b41840d15b6">跨会话延迟奖励与每轮按检索相似度奖励有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ainteractive-memory">Interactive Memory Learning for Long-Term Conversations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似度是即时代理，未必代表之后实际有用；延迟奖励观察后续对话结果，试图学习长期写入和触发价值。它也带来信用分配难题，不能把未来问题提前给写入器降低难度，否则不再是面向未知未来的记忆学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条低频过敏信息当时与话题不太相似，却在后续点餐很关键；即时相似度可能低估它的长期价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17088">原论文</a> · <a href="../../../../agent-research/2609.17088-interactive-memory/">实现解读</a> · <a href="#qa-90095b41840d15b6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:interactive-memory" data-paper-title="Interactive Memory Learning for Long-Term Conversations" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Interactive Memory Learning for Long-Term Conversations Agent Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory 2026-09-15 Planner 决定写入高价值记忆，Trigger 决定何时取回，两者通过跨会话延迟奖励共同演化。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。本地执行 observation-safe Planner/Trigger 延迟奖励状态机；未训练论文规模对话 Agent。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  长期记忆 多 Agent 强化学习 Agent 记忆与技能：让经验可取回、可失效 observation-safe 状态机为何要区分写入时与未来评测时的信息？ 写入器只能看到当时已出现的观察，未来问题、答案和评分只可在相应执行后用于外部奖励。Planner/Trigger 延迟状态机本地验证的是这个隔离与反馈路径，未训练论文规模对话 Agent，不能用 fixture 的预设奖励声称记忆已学会长期偏好。 例如将第三天问题藏进第一天写入输入可让系统轻易挑中所需事实，但这种前视泄露使学习效果无法成立。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-210029a079c17858">observation-safe 状态机为何要区分写入时与未来评测时的信息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ainteractive-memory">Interactive Memory Learning for Long-Term Conversations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>写入器只能看到当时已出现的观察，未来问题、答案和评分只可在相应执行后用于外部奖励。Planner/Trigger 延迟状态机本地验证的是这个隔离与反馈路径，未训练论文规模对话 Agent，不能用 fixture 的预设奖励声称记忆已学会长期偏好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如将第三天问题藏进第一天写入输入可让系统轻易挑中所需事实，但这种前视泄露使学习效果无法成立。</p>
<p class="ar-learning-sources">依据：核心公式与实现对应、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17088">原论文</a> · <a href="../../../../agent-research/2609.17088-interactive-memory/">实现解读</a> · <a href="#qa-210029a079c17858">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:grounded-memory" data-paper-title="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents Agent Microsoft 2026-09-09 给异步记忆 curator 最小权限只读工具，在写入前验证、限定作用域并刷新候选记忆。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent 记忆 环境探测 Agent 记忆与技能：让经验可取回、可失效 为什么记忆 curator 写入前也要探测当前环境？ 执行轨迹里的说法可能过时、不完整或只是一次偶然状态，直接写入会把错误长期固化。curator 用最小权限只读工具验证、限定作用域并刷新候选，使记忆带有环境证据；只读并不保证结论永久有效，仍需时间与适用范围。 例如曾经失败的 API 可能只是临时权限问题，写成“这个工具不可用”前应只读检查当前配置和作用域。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-grounded-memory-32bdf0be" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-987d0970e9c03a33">为什么记忆 curator 写入前也要探测当前环境？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agrounded-memory">Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>执行轨迹里的说法可能过时、不完整或只是一次偶然状态，直接写入会把错误长期固化。curator 用最小权限只读工具验证、限定作用域并刷新候选，使记忆带有环境证据；只读并不保证结论永久有效，仍需时间与适用范围。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如曾经失败的 API 可能只是临时权限问题，写成“这个工具不可用”前应只读检查当前配置和作用域。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11060">原论文</a> · <a href="../../../../agent-research/2609.11060-grounded-memory/">实现解读</a> · <a href="#qa-987d0970e9c03a33">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:grounded-memory" data-paper-title="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents Agent Microsoft 2026-09-09 给异步记忆 curator 最小权限只读工具，在写入前验证、限定作用域并刷新候选记忆。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent 记忆 环境探测 Agent 记忆与技能：让经验可取回、可失效 记忆 curator 为什么应在写入前用最小权限只读工具探测环境？ 对话里的说法可能过时或只适用于局部环境，先探测能把候选记忆绑定到当前可见事实和作用域。只读最小权限减少整理过程改变被验证对象的机会；验证完成也只是该条件下成立，不能把一次探测提升成永久、跨环境通用的知识。 例如记忆候选说“服务端口是八千”，curator 可只读配置确认并标注环境，不能为让它成立而顺手修改服务配置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:grounded-memory" data-paper-title="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents Agent Microsoft 2026-09-09 给异步记忆 curator 最小权限只读工具，在写入前验证、限定作用域并刷新候选记忆。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent 记忆 环境探测 Agent 记忆与技能：让经验可取回、可失效 环境探测式准入与直接让 LLM 总结经验有什么区别？ 直接总结依赖已有轨迹文字，可能将推测压成事实；探测增加独立核查，能拒绝冲突并限制泛化范围。它额外消耗查询与维护成本，也只能核查工具能观察的条件，不能因有验证步骤就声称所有企业状态都可靠。 例如一次仓库路径不存在不应总结为所有项目都无该目录，探测可以把结论限定为当前仓库与版本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e27661bed1b5020f">环境探测式准入与直接让 LLM 总结经验有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agrounded-memory">Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>直接总结依赖已有轨迹文字，可能将推测压成事实；探测增加独立核查，能拒绝冲突并限制泛化范围。它额外消耗查询与维护成本，也只能核查工具能观察的条件，不能因有验证步骤就声称所有企业状态都可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次仓库路径不存在不应总结为所有项目都无该目录，探测可以把结论限定为当前仓库与版本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11060">原论文</a> · <a href="../../../../agent-research/2609.11060-grounded-memory/">实现解读</a> · <a href="#qa-e27661bed1b5020f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:grounded-memory" data-paper-title="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents Agent Microsoft 2026-09-09 给异步记忆 curator 最小权限只读工具，在写入前验证、限定作用域并刷新候选记忆。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。本地执行重复探测、冲突拒绝和记忆准入；未连接 GitHub Copilot SDK。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  Agent 记忆 环境探测 Agent 记忆与技能：让经验可取回、可失效 最小权限只读工具为什么不能被 curator 扩大成修复动作？ curator 的职责是核验候选记忆，写外部系统会改变它试图观察的状态并引入副作用。本地只验证重复探测、冲突拒绝与准入，未连接 Copilot SDK；调用合同通过不能说明真实企业 Agent 成本与成功率已复现。 例如发现配置值不同应更新记忆证据，而不是顺手把线上配置改回旧值再声称旧记忆被验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-84beb1f3d4030a3e">最小权限只读工具为什么不能被 curator 扩大成修复动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agrounded-memory">Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>curator 的职责是核验候选记忆，写外部系统会改变它试图观察的状态并引入副作用。本地只验证重复探测、冲突拒绝与准入，未连接 Copilot SDK；调用合同通过不能说明真实企业 Agent 成本与成功率已复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如发现配置值不同应更新记忆证据，而不是顺手把线上配置改回旧值再声称旧记忆被验证。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11060">原论文</a> · <a href="../../../../agent-research/2609.11060-grounded-memory/">实现解读</a> · <a href="#qa-84beb1f3d4030a3e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skill-retention" data-paper-title="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents Agent Manulife 2026-09-09 混合真实样本 replay 与 embedding anchor/LwF 类正则，防止合成技能数据微调破坏真实和 OOD 路由能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能检索 灾难性遗忘 Agent 记忆与技能：让经验可取回、可失效 合成技能数据为什么可能让技能检索器遗忘真实路由？ 合成分布可能在措辞、任务结构和难度上偏离真实使用，微调若只优化它，会改变原来有用的表示或排序边界。训练损失下降因此不代表真实和 OOD 检索保留；研究把真实 replay 与旧表示约束结合，关注新旧能力的共同表现。 例如合成任务总用标准函数名，真实用户却用口语描述，检索器可能学会新模板却忘了口语到技能的对应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-skill-retention-6ccb63cf" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c8463c103cf3df10">合成技能数据为什么可能让技能检索器遗忘真实路由？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askill-retention">When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Manulife</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>合成分布可能在措辞、任务结构和难度上偏离真实使用，微调若只优化它，会改变原来有用的表示或排序边界。训练损失下降因此不代表真实和 OOD 检索保留；研究把真实 replay 与旧表示约束结合，关注新旧能力的共同表现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如合成任务总用标准函数名，真实用户却用口语描述，检索器可能学会新模板却忘了口语到技能的对应。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10750">原论文</a> · <a href="../../../../agent-research/2609.10750-skill-retention/">实现解读</a> · <a href="#qa-c8463c103cf3df10">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skill-retention" data-paper-title="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents Agent Manulife 2026-09-09 混合真实样本 replay 与 embedding anchor/LwF 类正则，防止合成技能数据微调破坏真实和 OOD 路由能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能检索 灾难性遗忘 Agent 记忆与技能：让经验可取回、可失效 为什么用更多合成技能数据微调，反而可能降低真实任务的技能检索能力？ 合成样本的表述和分布可能与真实请求不同，微调会把 embedding 与路由边界拉向合成模式。真实样本 replay 保留原任务约束，anchor 或旧模型蒸馏限制表示漂移；这些正则保护的是迁移与保留，不代表合成数据越多越好或所有遗忘都会消失。 例如合成任务总把工具名写全，真实用户却用简称；只学合成表达会漏掉真实请求，回放真实简称可保护原有路由。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skill-retention" data-paper-title="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents Agent Manulife 2026-09-09 混合真实样本 replay 与 embedding anchor/LwF 类正则，防止合成技能数据微调破坏真实和 OOD 路由能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能检索 灾难性遗忘 Agent 记忆与技能：让经验可取回、可失效 真实样本 replay 与 embedding anchor/LwF 正则分别约束什么？ replay 让优化继续看到旧任务数据，anchor 或 LwF 类正则限制表示或旧输出漂移。前者补数据覆盖，后者约束参数变化造成的行为偏离，不能简单视为重复措施；权重过强也可能妨碍学习新合成技能，需要独立验证取舍。 例如保留旧口语查询用于 replay，同时要求其 embedding 不大幅移动，可分别从样本和表示两侧保护旧检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-80ec601077b5e3e4">真实样本 replay 与 embedding anchor/LwF 正则分别约束什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askill-retention">When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Manulife</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>replay 让优化继续看到旧任务数据，anchor 或 LwF 类正则限制表示或旧输出漂移。前者补数据覆盖，后者约束参数变化造成的行为偏离，不能简单视为重复措施；权重过强也可能妨碍学习新合成技能，需要独立验证取舍。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如保留旧口语查询用于 replay，同时要求其 embedding 不大幅移动，可分别从样本和表示两侧保护旧检索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10750">原论文</a> · <a href="../../../../agent-research/2609.10750-skill-retention/">实现解读</a> · <a href="#qa-80ec601077b5e3e4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skill-retention" data-paper-title="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents Agent Manulife 2026-09-09 混合真实样本 replay 与 embedding anchor/LwF 类正则，防止合成技能数据微调破坏真实和 OOD 路由能力。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。本地执行真实路线 anchor、冲突惩罚和 replay；未训练 34,396 技能的 0.6B 模型。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  技能检索 灾难性遗忘 Agent 记忆与技能：让经验可取回、可失效 本地 anchor、冲突惩罚与 replay 的通过是否包含 0.6B retriever 训练？ 不包含。本地仅执行真实路线锚点和相关约束 reference，未训练三万多技能的 0.6B 模型。可检查 replay 确实参与、锚点损失方向与冲突处理，但合成 fixture 的状态变化不能改写为真实或 OOD 检索保留率。 例如一个向量被拉回旧锚点说明正则梯度有效，不说明模型在未见用户问法上仍能找到正确技能。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a1783c4ed93b7227">本地 anchor、冲突惩罚与 replay 的通过是否包含 0.6B retriever 训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askill-retention">When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Manulife</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不包含。本地仅执行真实路线锚点和相关约束 reference，未训练三万多技能的 0.6B 模型。可检查 replay 确实参与、锚点损失方向与冲突处理，但合成 fixture 的状态变化不能改写为真实或 OOD 检索保留率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个向量被拉回旧锚点说明正则梯度有效，不说明模型在未见用户问法上仍能找到正确技能。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.10750">原论文</a> · <a href="../../../../agent-research/2609.10750-skill-retention/">实现解读</a> · <a href="#qa-a1783c4ed93b7227">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memforest" data-paper-title="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging Agent Shanghai Jiao Tong University 2026-09-08 MemForest 不把全部历史压进一条摘要，而是先按事件切分成多棵树，再在容量压力下渐进合并节点。查询从语义 anchor 出发向邻域传播，保留时间结构和跨事件关联。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现事件分区、渐进合并与 anchor 邻域检索；语义相似度用词项重叠近似。三种子结果见 metrics/mini-suite-seeds42-44.json。本地 EventTree 是紧凑 CPU 数据结构，使用 token Jaccard 选择树并真实执行压缩；未运行作者 embedding、LLM 摘要器或长程 benchmark。  事件树记忆压缩 Agent 记忆与技能：让经验可取回、可失效 为什么按事件形成多棵树，而不把全部历史压成一条摘要？ 不同事件有各自时间与语义结构，多树可让局部容量压力在事件内渐进合并，保留跨事件关联而避免一次全局摘要抹平来源。它仍需选择合并层级和摘要，树形组织不是无损语义保证，过度合并可能丢失低频细节。 例如旅行计划和项目会议各成一棵树，查询改期时可以先进入相关事件，而不在一条混合总摘要中寻找。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memforest-6306606d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7faeaf7a8b79a728">为什么按事件形成多棵树，而不把全部历史压成一条摘要？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemforest">MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同事件有各自时间与语义结构，多树可让局部容量压力在事件内渐进合并，保留跨事件关联而避免一次全局摘要抹平来源。它仍需选择合并层级和摘要，树形组织不是无损语义保证，过度合并可能丢失低频细节。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旅行计划和项目会议各成一棵树，查询改期时可以先进入相关事件，而不在一条混合总摘要中寻找。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08273">原论文</a> · <a href="../../../../agent-research/2609.08273-memforest/">实现解读</a> · <a href="#qa-7faeaf7a8b79a728">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memforest" data-paper-title="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging Agent Shanghai Jiao Tong University 2026-09-08 MemForest 不把全部历史压进一条摘要，而是先按事件切分成多棵树，再在容量压力下渐进合并节点。查询从语义 anchor 出发向邻域传播，保留时间结构和跨事件关联。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现事件分区、渐进合并与 anchor 邻域检索；语义相似度用词项重叠近似。三种子结果见 metrics/mini-suite-seeds42-44.json。本地 EventTree 是紧凑 CPU 数据结构，使用 token Jaccard 选择树并真实执行压缩；未运行作者 embedding、LLM 摘要器或长程 benchmark。  事件树记忆压缩 Agent 记忆与技能：让经验可取回、可失效 为什么容量紧张时渐进合并事件树，比持续重写一份总摘要更利于定位证据？ 事件分区保留局部时间与因果结构，容量压力下只合并必要节点，避免每次压缩都搅乱全部历史。查询从语义锚点向邻域传播，还能利用跨事件关联；层次摘要仍可能遗漏细节，因此树结构是控制损失与检索路径，不是无损压缩保证。 例如付款失败和之后退款分属两次事件，树间关联可连接它们；一份反复重写的总摘要可能混淆先后次序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memforest" data-paper-title="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging Agent Shanghai Jiao Tong University 2026-09-08 MemForest 不把全部历史压进一条摘要，而是先按事件切分成多棵树，再在容量压力下渐进合并节点。查询从语义 anchor 出发向邻域传播，保留时间结构和跨事件关联。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现事件分区、渐进合并与 anchor 邻域检索；语义相似度用词项重叠近似。三种子结果见 metrics/mini-suite-seeds42-44.json。本地 EventTree 是紧凑 CPU 数据结构，使用 token Jaccard 选择树并真实执行压缩；未运行作者 embedding、LLM 摘要器或长程 benchmark。  事件树记忆压缩 Agent 记忆与技能：让经验可取回、可失效 语义 anchor 邻域传播与只检索单个最相似节点有什么不同？ 单节点匹配可能只找到表面相关片段，邻域传播还可沿时间与跨事件链接补充支撑上下文。它提供结构性扩展，也可能带入噪声，因此传播范围和容量需要控制，不能把邻接节点都假定为正确证据。 例如命中“改期”节点后再读相邻确认节点，可知道新日期是否最终生效；只看最相似一句可能仍停留在提议。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-202f62121d392bce">语义 anchor 邻域传播与只检索单个最相似节点有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemforest">MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单节点匹配可能只找到表面相关片段，邻域传播还可沿时间与跨事件链接补充支撑上下文。它提供结构性扩展，也可能带入噪声，因此传播范围和容量需要控制，不能把邻接节点都假定为正确证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如命中“改期”节点后再读相邻确认节点，可知道新日期是否最终生效；只看最相似一句可能仍停留在提议。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08273">原论文</a> · <a href="../../../../agent-research/2609.08273-memforest/">实现解读</a> · <a href="#qa-202f62121d392bce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memforest" data-paper-title="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging Agent Shanghai Jiao Tong University 2026-09-08 MemForest 不把全部历史压进一条摘要，而是先按事件切分成多棵树，再在容量压力下渐进合并节点。查询从语义 anchor 出发向邻域传播，保留时间结构和跨事件关联。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现事件分区、渐进合并与 anchor 邻域检索；语义相似度用词项重叠近似。三种子结果见 metrics/mini-suite-seeds42-44.json。本地 EventTree 是紧凑 CPU 数据结构，使用 token Jaccard 选择树并真实执行压缩；未运行作者 embedding、LLM 摘要器或长程 benchmark。  事件树记忆压缩 Agent 记忆与技能：让经验可取回、可失效 本地 token Jaccard EventTree 与论文 embedding/LLM 摘要器的边界是什么？ 本地使用紧凑 CPU 数据结构、词项 Jaccard 选树并实际执行压缩，验证树分区与合并路径；没有运行作者 embedding、LLM 摘要器或长程 benchmark。结构正确和记录减少不能当成真实语义检索或记忆回答能力。 例如两个节点共享“会议”一词可被 Jaccard 选中，但是否为同一事件仍需要更丰富语义，当前接口不自动证明。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ff77fee8acfdac1a">本地 token Jaccard EventTree 与论文 embedding/LLM 摘要器的边界是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemforest">MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shanghai Jiao Tong University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地使用紧凑 CPU 数据结构、词项 Jaccard 选树并实际执行压缩，验证树分区与合并路径；没有运行作者 embedding、LLM 摘要器或长程 benchmark。结构正确和记录减少不能当成真实语义检索或记忆回答能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个节点共享“会议”一词可被 Jaccard 选中，但是否为同一事件仍需要更丰富语义，当前接口不自动证明。</p>
<p class="ar-learning-sources">依据：本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08273">原论文</a> · <a href="../../../../agent-research/2609.08273-memforest/">实现解读</a> · <a href="#qa-ff77fee8acfdac1a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:atomrec" data-paper-title="AtomRec: Evolving Atomic Memory for Agentic Recommendation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AtomRec: Evolving Atomic Memory for Agentic Recommendation Agent Xi&#x27;an Jiaotong-Liverpool University 2026-09-04 粗粒度用户摘要会在重写时覆盖旧偏好，单一协同边又难以解释推荐。AtomRec 将用户和物品历史拆成可独立演化的原子字段，建立语义协同链接，并以多跳路径取回“为什么推荐”的证据。 复现级别：真实 checkpoint 原子记忆实验。复现级别：真实 checkpoint 原子记忆实验。冻结 Qwen 生成字段、语义链接、历史更新与候选排序，以模型隐状态作本地 encoder；不是原论文线上系统或完整基准复现。未获得原作者代码、提示词和完整实验配置；Qwen 隐状态不是论文的 SentenceT5，Amazon Beauty 也不代表 Xiaohongshu 线上分布。本地不声称复刻原系统或线上实验。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Agentic recommendation memory Agent 记忆与技能：让经验可取回、可失效 原子字段记忆为什么比整份用户画像重写更易控制更新范围？ 用户和物品历史拆成可独立演化的字段后，新证据只修改命中的原子，避免一次摘要重写覆盖无关旧偏好。语义协同链接还支持多跳取回解释证据；字段细不自动保证真实，需要保留时间、来源和合法链接范围。 例如用户新近偏好轻便鞋，只更新鞋类重量字段，不应顺手覆盖长期的预算或过敏材质限制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-atomrec-2a7b7ab5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-351629bdd8e2893b">原子字段记忆为什么比整份用户画像重写更易控制更新范围？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aatomrec">AtomRec: Evolving Atomic Memory for Agentic Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xi&#x27;an Jiaotong-Liverpool University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户和物品历史拆成可独立演化的字段后，新证据只修改命中的原子，避免一次摘要重写覆盖无关旧偏好。语义协同链接还支持多跳取回解释证据；字段细不自动保证真实，需要保留时间、来源和合法链接范围。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户新近偏好轻便鞋，只更新鞋类重量字段，不应顺手覆盖长期的预算或过敏材质限制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04882">原论文</a> · <a href="../../../../agent-research/2609.04882-atomrec/">实现解读</a> · <a href="#qa-351629bdd8e2893b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:atomrec" data-paper-title="AtomRec: Evolving Atomic Memory for Agentic Recommendation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AtomRec: Evolving Atomic Memory for Agentic Recommendation Agent Xi&#x27;an Jiaotong-Liverpool University 2026-09-04 粗粒度用户摘要会在重写时覆盖旧偏好，单一协同边又难以解释推荐。AtomRec 将用户和物品历史拆成可独立演化的原子字段，建立语义协同链接，并以多跳路径取回“为什么推荐”的证据。 复现级别：真实 checkpoint 原子记忆实验。复现级别：真实 checkpoint 原子记忆实验。冻结 Qwen 生成字段、语义链接、历史更新与候选排序，以模型隐状态作本地 encoder；不是原论文线上系统或完整基准复现。未获得原作者代码、提示词和完整实验配置；Qwen 隐状态不是论文的 SentenceT5，Amazon Beauty 也不代表 Xiaohongshu 线上分布。本地不声称复刻原系统或线上实验。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Agentic recommendation memory Agent 记忆与技能：让经验可取回、可失效 把用户画像拆成原子字段，为什么有助于避免新偏好覆盖旧偏好？ 更新只针对命中的事实字段，不必重写整份用户摘要，降低无关信息被顺带删除或改意的风险。语义协同边和多跳路径又把推荐依据连接起来，使可追溯证据与偏好值分开；原子化仍需要处理冲突和时间范围，不能默认旧事实永远有效。 例如用户新增“晚餐不吃辣”，只更新晚餐口味字段，保留通勤预算和早餐偏好，而非让一次摘要重写把它们全部抹掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:atomrec" data-paper-title="AtomRec: Evolving Atomic Memory for Agentic Recommendation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AtomRec: Evolving Atomic Memory for Agentic Recommendation Agent Xi&#x27;an Jiaotong-Liverpool University 2026-09-04 粗粒度用户摘要会在重写时覆盖旧偏好，单一协同边又难以解释推荐。AtomRec 将用户和物品历史拆成可独立演化的原子字段，建立语义协同链接，并以多跳路径取回“为什么推荐”的证据。 复现级别：真实 checkpoint 原子记忆实验。复现级别：真实 checkpoint 原子记忆实验。冻结 Qwen 生成字段、语义链接、历史更新与候选排序，以模型隐状态作本地 encoder；不是原论文线上系统或完整基准复现。未获得原作者代码、提示词和完整实验配置；Qwen 隐状态不是论文的 SentenceT5，Amazon Beauty 也不代表 Xiaohongshu 线上分布。本地不声称复刻原系统或线上实验。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Agentic recommendation memory Agent 记忆与技能：让经验可取回、可失效 多跳证据路径与单一用户—物品协同边有什么不同？ 单边表达总体关联，多跳可展示偏好、历史物品属性与候选之间的支持链，帮助解释推荐原因。路径也可能包含不可靠语义边，不能把能连通当作因果偏好证明；下游排序仍要在闭合候选集和隔离目标条件下评价。 例如用户喜欢旧鞋的轻量特征，经属性链接到新鞋，比只说两物品共同购买更可追踪，但链接必须来自真实历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7726f178d983b0c6">多跳证据路径与单一用户—物品协同边有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aatomrec">AtomRec: Evolving Atomic Memory for Agentic Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xi&#x27;an Jiaotong-Liverpool University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单边表达总体关联，多跳可展示偏好、历史物品属性与候选之间的支持链，帮助解释推荐原因。路径也可能包含不可靠语义边，不能把能连通当作因果偏好证明；下游排序仍要在闭合候选集和隔离目标条件下评价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户喜欢旧鞋的轻量特征，经属性链接到新鞋，比只说两物品共同购买更可追踪，但链接必须来自真实历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04882">原论文</a> · <a href="../../../../agent-research/2609.04882-atomrec/">实现解读</a> · <a href="#qa-7726f178d983b0c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:atomrec" data-paper-title="AtomRec: Evolving Atomic Memory for Agentic Recommendation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="AtomRec: Evolving Atomic Memory for Agentic Recommendation Agent Xi&#x27;an Jiaotong-Liverpool University 2026-09-04 粗粒度用户摘要会在重写时覆盖旧偏好，单一协同边又难以解释推荐。AtomRec 将用户和物品历史拆成可独立演化的原子字段，建立语义协同链接，并以多跳路径取回“为什么推荐”的证据。 复现级别：真实 checkpoint 原子记忆实验。复现级别：真实 checkpoint 原子记忆实验。冻结 Qwen 生成字段、语义链接、历史更新与候选排序，以模型隐状态作本地 encoder；不是原论文线上系统或完整基准复现。未获得原作者代码、提示词和完整实验配置；Qwen 隐状态不是论文的 SentenceT5，Amazon Beauty 也不代表 Xiaohongshu 线上分布。本地不声称复刻原系统或线上实验。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Agentic recommendation memory Agent 记忆与技能：让经验可取回、可失效 本地 pre-target 重建与非法链接记零分别防什么问题？ 每个留出时点只用目标之前历史建立记忆，防未来行为泄露；生成链接只能引用给定历史 ID，非法或畸形输出直接失败，不回填标准答案。本地小样本 test 为负结果，说明链路执行不等于推荐收益，更不代表原作者线上系统。 例如推荐目标商品已出现在未来历史中就会让任务变简单；按时点重建必须删去它，而不能仅在 prompt 隐藏字段名。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-781bdb947b2bb38f">本地 pre-target 重建与非法链接记零分别防什么问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aatomrec">AtomRec: Evolving Atomic Memory for Agentic Recommendation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Xi&#x27;an Jiaotong-Liverpool University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个留出时点只用目标之前历史建立记忆，防未来行为泄露；生成链接只能引用给定历史 ID，非法或畸形输出直接失败，不回填标准答案。本地小样本 test 为负结果，说明链路执行不等于推荐收益，更不代表原作者线上系统。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如推荐目标商品已出现在未来历史中就会让任务变简单；按时点重建必须删去它，而不能仅在 prompt 隐藏字段名。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04882">原论文</a> · <a href="../../../../agent-research/2609.04882-atomrec/">实现解读</a> · <a href="#qa-781bdb947b2bb38f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coskill" data-paper-title="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution Agent Institute of Automation, Chinese Academy of Sciences 2026-09-04 以往技能库要么与策略优化分离，要么把元技能写成固定工作流。CoSkill 让 Reasoning Agent 使用任务技能及其子步骤技能，让可学习 Meta-Skill Agent 根据执行回报改写技能；二者共享 backbone 并端到端联合训练。 复现级别：公开 checkpoint 训练实验。复现级别：公开 checkpoint 训练实验。Qwen3-4B 的同一末层参数同时接收推理和技能编辑梯度，动作由真实模型生成并交给 ToolRoute 环境执行；不是原论文 ALFWorld/WebShop、VERL 或 7B 训练复现。本地使用 Qwen3-4B 最后一层和自建 ToolRoute，不含论文的离线技能初始化、SentenceT5 子技能检索、ALFWorld/WebShop 或原仓库训练规模，因此不得与论文分数横向比较。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Hierarchical skill coevolution Agent 记忆与技能：让经验可取回、可失效 CoSkill 的 Meta-Skill Agent 为什么是可学习策略，而非固定脚本？ 它依据执行回报修改技能内容，Reasoning Agent 则学习如何选择与使用任务和子步骤技能，两角色共享 backbone 并交替更新。技能库与行动策略因而共同适配，而不只是把规则提示存入库；仍需验证修改是否真的改善执行。 例如推理角色发现旧技能少了恢复步骤，元技能角色提出修改，随后重置环境验证，而不是直接把每次反思都永久收录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-coskill-9fe84c48" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bc25b0a6a77ac396">CoSkill 的 Meta-Skill Agent 为什么是可学习策略，而非固定脚本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoskill">CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它依据执行回报修改技能内容，Reasoning Agent 则学习如何选择与使用任务和子步骤技能，两角色共享 backbone 并交替更新。技能库与行动策略因而共同适配，而不只是把规则提示存入库；仍需验证修改是否真的改善执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如推理角色发现旧技能少了恢复步骤，元技能角色提出修改，随后重置环境验证，而不是直接把每次反思都永久收录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04865">原论文</a> · <a href="../../../../agent-research/2609.04865-coskill/">实现解读</a> · <a href="#qa-bc25b0a6a77ac396">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coskill" data-paper-title="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution Agent Institute of Automation, Chinese Academy of Sciences 2026-09-04 以往技能库要么与策略优化分离，要么把元技能写成固定工作流。CoSkill 让 Reasoning Agent 使用任务技能及其子步骤技能，让可学习 Meta-Skill Agent 根据执行回报改写技能；二者共享 backbone 并端到端联合训练。 复现级别：公开 checkpoint 训练实验。复现级别：公开 checkpoint 训练实验。Qwen3-4B 的同一末层参数同时接收推理和技能编辑梯度，动作由真实模型生成并交给 ToolRoute 环境执行；不是原论文 ALFWorld/WebShop、VERL 或 7B 训练复现。本地使用 Qwen3-4B 最后一层和自建 ToolRoute，不含论文的离线技能初始化、SentenceT5 子技能检索、ALFWorld/WebShop 或原仓库训练规模，因此不得与论文分数横向比较。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Hierarchical skill coevolution Agent 记忆与技能：让经验可取回、可失效 共享团队回报为何能让推理策略和 Meta-Skill 策略一起适配？ 技能内容决定推理可用的程序，推理选择又决定哪些技能得到执行反馈。联合目标把两侧对任务结果的影响连起来，交替更新减少只改库而策略不用、或只改策略却受旧技能限制的问题；共同回报仍不自动解决单次修改的信用归因。 例如原技能步骤过长导致执行失败，Meta-Skill 可压缩步骤，推理 Agent 再学何时调用改版，而不是只把新文档塞进库。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coskill" data-paper-title="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution Agent Institute of Automation, Chinese Academy of Sciences 2026-09-04 以往技能库要么与策略优化分离，要么把元技能写成固定工作流。CoSkill 让 Reasoning Agent 使用任务技能及其子步骤技能，让可学习 Meta-Skill Agent 根据执行回报改写技能；二者共享 backbone 并端到端联合训练。 复现级别：公开 checkpoint 训练实验。复现级别：公开 checkpoint 训练实验。Qwen3-4B 的同一末层参数同时接收推理和技能编辑梯度，动作由真实模型生成并交给 ToolRoute 环境执行；不是原论文 ALFWorld/WebShop、VERL 或 7B 训练复现。本地使用 Qwen3-4B 最后一层和自建 ToolRoute，不含论文的离线技能初始化、SentenceT5 子技能检索、ALFWorld/WebShop 或原仓库训练规模，因此不得与论文分数横向比较。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Hierarchical skill coevolution Agent 记忆与技能：让经验可取回、可失效 联合训练与固定技能库下只训练检索有什么不同？ 固定库方法只改变选哪个技能，联合训练还允许技能内容演化，解决内容本身不适合任务的问题。它也增加非平稳性和归因难度，因此需要角色信用、隔离编辑和无收益拒绝，不能因库增长就声称团队策略更强。 例如检索再准确也无法补救一份步骤顺序错误的技能；元技能可改顺序，但改后必须防止其他任务回归。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-343636ce44e2ae97">联合训练与固定技能库下只训练检索有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoskill">CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定库方法只改变选哪个技能，联合训练还允许技能内容演化，解决内容本身不适合任务的问题。它也增加非平稳性和归因难度，因此需要角色信用、隔离编辑和无收益拒绝，不能因库增长就声称团队策略更强。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如检索再准确也无法补救一份步骤顺序错误的技能；元技能可改顺序，但改后必须防止其他任务回归。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04865">原论文</a> · <a href="../../../../agent-research/2609.04865-coskill/">实现解读</a> · <a href="#qa-343636ce44e2ae97">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coskill" data-paper-title="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution Agent Institute of Automation, Chinese Academy of Sciences 2026-09-04 以往技能库要么与策略优化分离，要么把元技能写成固定工作流。CoSkill 让 Reasoning Agent 使用任务技能及其子步骤技能，让可学习 Meta-Skill Agent 根据执行回报改写技能；二者共享 backbone 并端到端联合训练。 复现级别：公开 checkpoint 训练实验。复现级别：公开 checkpoint 训练实验。Qwen3-4B 的同一末层参数同时接收推理和技能编辑梯度，动作由真实模型生成并交给 ToolRoute 环境执行；不是原论文 ALFWorld/WebShop、VERL 或 7B 训练复现。本地使用 Qwen3-4B 最后一层和自建 ToolRoute，不含论文的离线技能初始化、SentenceT5 子技能检索、ALFWorld/WebShop 或原仓库训练规模，因此不得与论文分数横向比较。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；  Hierarchical skill coevolution Agent 记忆与技能：让经验可取回、可失效 本地三 seed 实际更新后未晋级，应该怎样解释？ 真实路径出现双角色非零梯度和参数变化，但重置验证未取得正增益，因此技能候选未晋级并保留基线冠军。旧版读取评测标签的分数已作废，legacy 解析也不是能力；本地 Qwen ToolRoute 不能与论文 ALFWorld/WebShop 分数横比。 例如参数变化很大而 validation 不升，只能证明训练执行及拒绝路径有效，不能把“完成更新”写成“CoSkill 改善成功率”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f303b868421584ec">本地三 seed 实际更新后未晋级，应该怎样解释？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoskill">CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实路径出现双角色非零梯度和参数变化，但重置验证未取得正增益，因此技能候选未晋级并保留基线冠军。旧版读取评测标签的分数已作废，legacy 解析也不是能力；本地 Qwen ToolRoute 不能与论文 ALFWorld/WebShop 分数横比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如参数变化很大而 validation 不升，只能证明训练执行及拒绝路径有效，不能把“完成更新”写成“CoSkill 改善成功率”。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04865">原论文</a> · <a href="../../../../agent-research/2609.04865-coskill/">实现解读</a> · <a href="#qa-f303b868421584ec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skilldreamer" data-paper-title="Imagine Before Acting: Prospective Skill Identification for LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Imagine Before Acting: Prospective Skill Identification for LLM Agents Agent Sichuan University 2026-08-28 任务描述主要说目标，技能文档主要写程序性知识。直接相似度容易优先找到背景相近、但不能解决当前能力缺口的技能；检索到了也未必会在执行时调用。SkillDreamer 在检索和调用两侧显式表达能力需求。PSG 先由 LLM 从任务推断 1–5 个独立 capability 和语义 anchors，再为每个 capability 生成 procedure-like pseudo skill。pseudo skill 只是检索代理，并非验证过的可执行技能。 seed42期间有教师短诊断并存，43/44以两个worker并行；本轮阅读与实现的是 v2 实质修订；v1 首发在 2026-08-28，不计作 2026-10 新 v1。本地保留真实模型 PSG/HSR/CSI，但算术环境只是 live-interaction diagnostic，不冒充 SkillUsage/SkillNet-Gym 能力复现。本地对照口径：基线为同模型 no-skills 与原任务 dense direct retrieval，实验组为真实 PSG/HSR/CSI；缩放算术交互对原 benchmark 的相对能力结论不适用。  skill-retrieval prospective-reasoning capability-aware-invocation Agent 记忆与技能：让经验可取回、可失效 pseudo skill 为什么是检索代理，不能直接当成已验证程序？ 模型按任务想象所需能力和 procedure-like 描述，用来弥合目标文字与技能文档的表达差异。它没有经历实际执行验证，可能缺步骤或违背环境条件；真正行动前仍要加载真实技能并检查匹配，不能因为描述看起来完整就直接信任。 例如 pseudo 写“批量导出并校验文件”，可帮助找导出技能，但真实工具参数、权限和校验流程仍需从实际文档获得。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-skilldreamer-d1e698b9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-1051cd50b705bb42">pseudo skill 为什么是检索代理，不能直接当成已验证程序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askilldreamer">Imagine Before Acting: Prospective Skill Identification for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sichuan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型按任务想象所需能力和 procedure-like 描述，用来弥合目标文字与技能文档的表达差异。它没有经历实际执行验证，可能缺步骤或违背环境条件；真正行动前仍要加载真实技能并检查匹配，不能因为描述看起来完整就直接信任。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 pseudo 写“批量导出并校验文件”，可帮助找导出技能，但真实工具参数、权限和校验流程仍需从实际文档获得。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01642">原论文</a> · <a href="../../../../reproductions/2609.01642-skilldreamer/">实现解读</a> · <a href="#qa-1051cd50b705bb42">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skilldreamer" data-paper-title="Imagine Before Acting: Prospective Skill Identification for LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Imagine Before Acting: Prospective Skill Identification for LLM Agents Agent Sichuan University 2026-08-28 任务描述主要说目标，技能文档主要写程序性知识。直接相似度容易优先找到背景相近、但不能解决当前能力缺口的技能；检索到了也未必会在执行时调用。SkillDreamer 在检索和调用两侧显式表达能力需求。PSG 先由 LLM 从任务推断 1–5 个独立 capability 和语义 anchors，再为每个 capability 生成 procedure-like pseudo skill。pseudo skill 只是检索代理，并非验证过的可执行技能。 seed42期间有教师短诊断并存，43/44以两个worker并行；本轮阅读与实现的是 v2 实质修订；v1 首发在 2026-08-28，不计作 2026-10 新 v1。本地保留真实模型 PSG/HSR/CSI，但算术环境只是 live-interaction diagnostic，不冒充 SkillUsage/SkillNet-Gym 能力复现。本地对照口径：基线为同模型 no-skills 与原任务 dense direct retrieval，实验组为真实 PSG/HSR/CSI；缩放算术交互对原 benchmark 的相对能力结论不适用。  skill-retrieval prospective-reasoning capability-aware-invocation Agent 记忆与技能：让经验可取回、可失效 生成 pseudo skill 后，为什么还需要 CSI 在执行前重新判断能力匹配？ 伪技能把任务目标转成程序性检索代理，帮助找到相关文档，但它本身未经过验证，也不保证检索结果适合当前子目标。CSI 再核对证据、限制与下一有界动作，连接“找得到技能”与“实际用对技能”；不能把想象出的步骤当成已可执行能力。 例如伪技能帮助检索到网页下载流程，执行前仍需检查当前网页是否需要登录，不能因文档标题相近就直接套用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skilldreamer" data-paper-title="Imagine Before Acting: Prospective Skill Identification for LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Imagine Before Acting: Prospective Skill Identification for LLM Agents Agent Sichuan University 2026-08-28 任务描述主要说目标，技能文档主要写程序性知识。直接相似度容易优先找到背景相近、但不能解决当前能力缺口的技能；检索到了也未必会在执行时调用。SkillDreamer 在检索和调用两侧显式表达能力需求。PSG 先由 LLM 从任务推断 1–5 个独立 capability 和语义 anchors，再为每个 capability 生成 procedure-like pseudo skill。pseudo skill 只是检索代理，并非验证过的可执行技能。 seed42期间有教师短诊断并存，43/44以两个worker并行；本轮阅读与实现的是 v2 实质修订；v1 首发在 2026-08-28，不计作 2026-10 新 v1。本地保留真实模型 PSG/HSR/CSI，但算术环境只是 live-interaction diagnostic，不冒充 SkillUsage/SkillNet-Gym 能力复现。本地对照口径：基线为同模型 no-skills 与原任务 dense direct retrieval，实验组为真实 PSG/HSR/CSI；缩放算术交互对原 benchmark 的相对能力结论不适用。  skill-retrieval prospective-reasoning capability-aware-invocation Agent 记忆与技能：让经验可取回、可失效 HSR 的能力轮询与只取所有候选全局最高分有什么取舍？ 全局最高分可能被一个容易匹配的能力占满，遗漏任务其他必需能力。HSR 为各 capability 排序后逐行轮询、去重，兼顾需求覆盖；候选内 min-max 归一化也使分数依赖各自候选集合，不能当跨任务校准成功概率。 例如任务同时需清洗、绘图和导出，轮询可让三种能力各有代表，而不是五个名额都被清洗技能占据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f40d500470486920">HSR 的能力轮询与只取所有候选全局最高分有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askilldreamer">Imagine Before Acting: Prospective Skill Identification for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sichuan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>全局最高分可能被一个容易匹配的能力占满，遗漏任务其他必需能力。HSR 为各 capability 排序后逐行轮询、去重，兼顾需求覆盖；候选内 min-max 归一化也使分数依赖各自候选集合，不能当跨任务校准成功概率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如任务同时需清洗、绘图和导出，轮询可让三种能力各有代表，而不是五个名额都被清洗技能占据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01642">原论文</a> · <a href="../../../../reproductions/2609.01642-skilldreamer/">实现解读</a> · <a href="#qa-f40d500470486920">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skilldreamer" data-paper-title="Imagine Before Acting: Prospective Skill Identification for LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Imagine Before Acting: Prospective Skill Identification for LLM Agents Agent Sichuan University 2026-08-28 任务描述主要说目标，技能文档主要写程序性知识。直接相似度容易优先找到背景相近、但不能解决当前能力缺口的技能；检索到了也未必会在执行时调用。SkillDreamer 在检索和调用两侧显式表达能力需求。PSG 先由 LLM 从任务推断 1–5 个独立 capability 和语义 anchors，再为每个 capability 生成 procedure-like pseudo skill。pseudo skill 只是检索代理，并非验证过的可执行技能。 seed42期间有教师短诊断并存，43/44以两个worker并行；本轮阅读与实现的是 v2 实质修订；v1 首发在 2026-08-28，不计作 2026-10 新 v1。本地保留真实模型 PSG/HSR/CSI，但算术环境只是 live-interaction diagnostic，不冒充 SkillUsage/SkillNet-Gym 能力复现。本地对照口径：基线为同模型 no-skills 与原任务 dense direct retrieval，实验组为真实 PSG/HSR/CSI；缩放算术交互对原 benchmark 的相对能力结论不适用。  skill-retrieval prospective-reasoning capability-aware-invocation Agent 记忆与技能：让经验可取回、可失效 CSI 周期检查的每五步是模型思考轮数还是实际执行动作数？ 是实际执行动作计数；下一动作前还需核对当前 subgoal、证据与限制，MATCH 或 PARTIAL_MATCH 时先加载真实 procedure 再行动。加载不是成功调用，pseudo 无效也不启发式补造；本地应分别报告加载、工具执行与最终通过。 例如模型连续反思三次但未执行工具，不应把它计成三步来提前触发周期检查；否则改变 runtime 节奏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9583328c6cf5170b">CSI 周期检查的每五步是模型思考轮数还是实际执行动作数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askilldreamer">Imagine Before Acting: Prospective Skill Identification for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sichuan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>是实际执行动作计数；下一动作前还需核对当前 subgoal、证据与限制，MATCH 或 PARTIAL_MATCH 时先加载真实 procedure 再行动。加载不是成功调用，pseudo 无效也不启发式补造；本地应分别报告加载、工具执行与最终通过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型连续反思三次但未执行工具，不应把它计成三步来提前触发周期检查；否则改变 runtime 节奏。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、数据协议、结果与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.01642">原论文</a> · <a href="../../../../reproductions/2609.01642-skilldreamer/">实现解读</a> · <a href="#qa-9583328c6cf5170b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:covemem" data-paper-title="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems Agent Shenzhen Technology University 2026-08-27 文本记忆要反复调用 LLM 重写，且丢掉全目录协同几何。CoVeMem 用冻结 LightGCN 状态构造 bank，由当前候选集检索相关历史，投影成 soft token，并通过语义对齐和 masked listwise 联训让 LLM 真正读取记忆。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现候选集检索、向量记忆 bank 和 soft-token read 诊断。未训练 LightGCN/LoRA checkpoint；本地验证候选条件向量读取和零文本重写控制流。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5197。  可训练协同记忆 Agent 记忆与技能：让经验可取回、可失效 CoVeMem 的协同向量记忆为什么由当前候选集决定读取什么历史？ 当前候选集的平均协同表示提供局部需求，系统在用户历史中检索相关项，再投影成 LLM 可读取的 soft token。这样记忆聚焦本次排序，而不是固定把全部历史文本写成画像；候选集变化可能改变读取结果，不能把记忆视为静态用户常量。 例如候选都是户外装备时优先取回相关购买历史，候选换成护肤品后同一用户可读取另一部分历史。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-covemem-d06a5714" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-44e841fd1f10ce70">CoVeMem 的协同向量记忆为什么由当前候选集决定读取什么历史？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acovemem">When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shenzhen Technology University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前候选集的平均协同表示提供局部需求，系统在用户历史中检索相关项，再投影成 LLM 可读取的 soft token。这样记忆聚焦本次排序，而不是固定把全部历史文本写成画像；候选集变化可能改变读取结果，不能把记忆视为静态用户常量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如候选都是户外装备时优先取回相关购买历史，候选换成护肤品后同一用户可读取另一部分历史。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26895">原论文</a> · <a href="../../../../agent-research/2608.26895-covemem/">实现解读</a> · <a href="#qa-44e841fd1f10ce70">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:covemem" data-paper-title="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems Agent Shenzhen Technology University 2026-08-27 文本记忆要反复调用 LLM 重写，且丢掉全目录协同几何。CoVeMem 用冻结 LightGCN 状态构造 bank，由当前候选集检索相关历史，投影成 soft token，并通过语义对齐和 masked listwise 联训让 LLM 真正读取记忆。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现候选集检索、向量记忆 bank 和 soft-token read 诊断。未训练 LightGCN/LoRA checkpoint；本地验证候选条件向量读取和零文本重写控制流。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5197。  可训练协同记忆 Agent 记忆与技能：让经验可取回、可失效 为什么需要语义对齐和 masked listwise 目标，不能只把 LightGCN 向量塞成 soft tokens？ 投影维度匹配不保证 LLM 会利用协同几何，语义对齐提供接口约束，候选内排序目标再迫使预测读取相关记忆。候选集驱动的检索也让同一用户面对不同选项时取回不同历史；冻结 bank 不意味着连接器无需训练，更不保证文本解释天然忠实。 例如同一用户对电影候选和图书候选需要不同历史子集，soft token 还得通过排序监督学会影响对应候选的分数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:covemem" data-paper-title="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems Agent Shenzhen Technology University 2026-08-27 文本记忆要反复调用 LLM 重写，且丢掉全目录协同几何。CoVeMem 用冻结 LightGCN 状态构造 bank，由当前候选集检索相关历史，投影成 soft token，并通过语义对齐和 masked listwise 联训让 LLM 真正读取记忆。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现候选集检索、向量记忆 bank 和 soft-token read 诊断。未训练 LightGCN/LoRA checkpoint；本地验证候选条件向量读取和零文本重写控制流。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5197。  可训练协同记忆 Agent 记忆与技能：让经验可取回、可失效 soft token 协同记忆与反复重写文本画像有什么不同？ soft token 保留冻结 LightGCN bank 的协同几何，通过投影和对齐让语言模型使用；文本画像更可读，却依赖生成重写且可能丢失目录结构。向量接口也需要真实训练与解释边界，零新增文本维护调用不等于整体推理零成本。 例如一次候选排序可直接读取协同向量，不必再请 LLM 重写“用户喜好”，但投影、检索和语言前向仍消耗计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-78cbec70ede61b68">soft token 协同记忆与反复重写文本画像有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acovemem">When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shenzhen Technology University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>soft token 保留冻结 LightGCN bank 的协同几何，通过投影和对齐让语言模型使用；文本画像更可读，却依赖生成重写且可能丢失目录结构。向量接口也需要真实训练与解释边界，零新增文本维护调用不等于整体推理零成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次候选排序可直接读取协同向量，不必再请 LLM 重写“用户喜好”，但投影、检索和语言前向仍消耗计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26895">原论文</a> · <a href="../../../../agent-research/2608.26895-covemem/">实现解读</a> · <a href="#qa-78cbec70ede61b68">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:covemem" data-paper-title="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems Agent Shenzhen Technology University 2026-08-27 文本记忆要反复调用 LLM 重写，且丢掉全目录协同几何。CoVeMem 用冻结 LightGCN 状态构造 bank，由当前候选集检索相关历史，投影成 soft token，并通过语义对齐和 masked listwise 联训让 LLM 真正读取记忆。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现候选集检索、向量记忆 bank 和 soft-token read 诊断。未训练 LightGCN/LoRA checkpoint；本地验证候选条件向量读取和零文本重写控制流。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5197。  可训练协同记忆 Agent 记忆与技能：让经验可取回、可失效 masked listwise 联训为什么不能只用向量相似度代替？ 相似度选历史只是检索步骤，语义对齐与 masked listwise 目标用于让 LLM 真正利用记忆完成候选排序；省略它们会变成另一条纯向量路线。本地未训练 LightGCN 或 LoRA checkpoint，只验证候选条件读取和无文本重写控制流。 例如检索到三条相关历史后，语言模型若从未学过 soft token 含义，不能仅因张量已拼接就认定它会用来正确排序。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-276bc00150e629ff">masked listwise 联训为什么不能只用向量相似度代替？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acovemem">When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Shenzhen Technology University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似度选历史只是检索步骤，语义对齐与 masked listwise 目标用于让 LLM 真正利用记忆完成候选排序；省略它们会变成另一条纯向量路线。本地未训练 LightGCN 或 LoRA checkpoint，只验证候选条件读取和无文本重写控制流。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如检索到三条相关历史后，语言模型若从未学过 soft token 含义，不能仅因张量已拼接就认定它会用来正确排序。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26895">原论文</a> · <a href="../../../../agent-research/2608.26895-covemem/">实现解读</a> · <a href="#qa-276bc00150e629ff">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spt" data-paper-title="SPT: Skills as Pre-Training Data for Agentic Language Models" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SPT: Skills as Pre-Training Data for Agentic Language Models Agent Beijing University of Posts and Telecommunications 2026-08-27 Agent 轨迹昂贵且只描述一次执行；skill package 则显式编码可复用工作流。SPT 在 post-training 前对 SkillCorpus 做 causal LM mid-training，并把被引用文件插到主说明的首次引用附近。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现 skill package、Reference Insert 和跨任务技能先验。未训练真实 LLM checkpoint；本地验证多文件引用装配和技能先验对无 oracle 工具路由的影响。ToolRoute-L2.1 三 seed：joint success 0.8056，plan F1 0.8340，平均成本 4.9439。  Agent 技能预训练 Agent 记忆与技能：让经验可取回、可失效 为什么多文件 skill package 可作为 causal LM 中期训练数据？ skill 包含可复用程序性知识和引用材料，可在 post-training 前训练语言模型预测其文本，形成工作流先验。它不是只记录一次执行的轨迹，也不等于训练时真的运行了工具；学习文档模式仍需后续 SFT 或 RL 将其转成行动。 例如技能说明引用配置示例与辅助脚本，模型读到的是可复用方法，而不是某次任务的偶然完整工具日志。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-spt-bfd17eb8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c27cd9a103e2836c">为什么多文件 skill package 可作为 causal LM 中期训练数据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspt">SPT: Skills as Pre-Training Data for Agentic Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>skill 包含可复用程序性知识和引用材料，可在 post-training 前训练语言模型预测其文本，形成工作流先验。它不是只记录一次执行的轨迹，也不等于训练时真的运行了工具；学习文档模式仍需后续 SFT 或 RL 将其转成行动。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如技能说明引用配置示例与辅助脚本，模型读到的是可复用方法，而不是某次任务的偶然完整工具日志。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26563">原论文</a> · <a href="../../../../agent-research/2608.26563-spt/">实现解读</a> · <a href="#qa-c27cd9a103e2836c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spt" data-paper-title="SPT: Skills as Pre-Training Data for Agentic Language Models" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SPT: Skills as Pre-Training Data for Agentic Language Models Agent Beijing University of Posts and Telecommunications 2026-08-27 Agent 轨迹昂贵且只描述一次执行；skill package 则显式编码可复用工作流。SPT 在 post-training 前对 SkillCorpus 做 causal LM mid-training，并把被引用文件插到主说明的首次引用附近。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现 skill package、Reference Insert 和跨任务技能先验。未训练真实 LLM checkpoint；本地验证多文件引用装配和技能先验对无 oracle 工具路由的影响。ToolRoute-L2.1 三 seed：joint success 0.8056，plan F1 0.8340，平均成本 4.9439。  Agent 技能预训练 Agent 记忆与技能：让经验可取回、可失效 把被引用文件插在首次引用附近，为什么比只预训练技能主说明更完整？ 技能往往把参数约束或示例放在配套文件，主说明的引用只是入口。就近展开让因果语言模型在需要的位置看到真实依赖，而非学习悬空引用；与通用语料混合又控制技能训练的分布偏移，不能把读过技能文本等同于执行能力已被验证。 例如说明写“按 schema.json 填参”，若训练只含这句话却没有 schema，模型无法学到字段限制；就近插入可补齐依赖。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spt" data-paper-title="SPT: Skills as Pre-Training Data for Agentic Language Models" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SPT: Skills as Pre-Training Data for Agentic Language Models Agent Beijing University of Posts and Telecommunications 2026-08-27 Agent 轨迹昂贵且只描述一次执行；skill package 则显式编码可复用工作流。SPT 在 post-training 前对 SkillCorpus 做 causal LM mid-training，并把被引用文件插到主说明的首次引用附近。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现 skill package、Reference Insert 和跨任务技能先验。未训练真实 LLM checkpoint；本地验证多文件引用装配和技能先验对无 oracle 工具路由的影响。ToolRoute-L2.1 三 seed：joint success 0.8056，plan F1 0.8340，平均成本 4.9439。  Agent 技能预训练 Agent 记忆与技能：让经验可取回、可失效 skill mid-training 与只在部署时检索 skill 文档有什么区别？ 前者将程序性模式写入参数，部署未必逐次检索同一文档；后者在当前上下文显式提供技能，可更新但占 token。两者可能互补，训练过技能文本也不证明能正确调用工具，需要真实策略与环境验证，不能以文档装配成功替代。 例如模型可能记住先验证再提交的顺序，但特定 API 的新参数仍需运行时文档，参数知识不保证版本永远正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a101e15d0ef1c12a">skill mid-training 与只在部署时检索 skill 文档有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspt">SPT: Skills as Pre-Training Data for Agentic Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者将程序性模式写入参数，部署未必逐次检索同一文档；后者在当前上下文显式提供技能，可更新但占 token。两者可能互补，训练过技能文本也不证明能正确调用工具，需要真实策略与环境验证，不能以文档装配成功替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型可能记住先验证再提交的顺序，但特定 API 的新参数仍需运行时文档，参数知识不保证版本永远正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26563">原论文</a> · <a href="../../../../agent-research/2608.26563-spt/">实现解读</a> · <a href="#qa-a101e15d0ef1c12a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spt" data-paper-title="SPT: Skills as Pre-Training Data for Agentic Language Models" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SPT: Skills as Pre-Training Data for Agentic Language Models Agent Beijing University of Posts and Telecommunications 2026-08-27 Agent 轨迹昂贵且只描述一次执行；skill package 则显式编码可复用工作流。SPT 在 post-training 前对 SkillCorpus 做 causal LM mid-training，并把被引用文件插到主说明的首次引用附近。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现 skill package、Reference Insert 和跨任务技能先验。未训练真实 LLM checkpoint；本地验证多文件引用装配和技能先验对无 oracle 工具路由的影响。ToolRoute-L2.1 三 seed：joint success 0.8056，plan F1 0.8340，平均成本 4.9439。  Agent 技能预训练 Agent 记忆与技能：让经验可取回、可失效 引用文件为什么插在主说明首次引用附近，而不统一附在末尾？ 邻近插入保留主说明与具体材料的局部关联，帮助 causal LM 在需要的位置读取后续内容；同时按 α 混合 skill 与通用语料控制训练分布。本地仅验证多文件引用装配与无 oracle 路由影响，未训练真实 LLM checkpoint。 例如正文首次说“见配置样例”时立即插入样例，比文档末尾散放多个文件更容易保持引用对象和步骤的对应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ca6f583af366bb98">引用文件为什么插在主说明首次引用附近，而不统一附在末尾？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspt">SPT: Skills as Pre-Training Data for Agentic Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>邻近插入保留主说明与具体材料的局部关联，帮助 causal LM 在需要的位置读取后续内容；同时按 α 混合 skill 与通用语料控制训练分布。本地仅验证多文件引用装配与无 oracle 路由影响，未训练真实 LLM checkpoint。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如正文首次说“见配置样例”时立即插入样例，比文档末尾散放多个文件更容易保持引用对象和步骤的对应。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26563">原论文</a> · <a href="../../../../agent-research/2608.26563-spt/">实现解读</a> · <a href="#qa-ca6f583af366bb98">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:caskg" data-paper-title="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval Agent Jilin University / Ant Group 2026-08-26 先从语义、词法、I/O 和结构证据建高召回有向图，再以 remove、substitute、reorder 三类文本反事实探针校准边，Bayesian smoothing 后只发布可靠关系。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。CaSKG 从训练 split 学习可复用 skill 路由，在隔离 test 上结合图式记忆与候选验证调用工具。ToolRoute-L2.1 三 seed 的 joint success 为 0.8000，plan step F1 为 0.8327，平均成本 5.0116。  反事实因果技能图 Agent 记忆与技能：让经验可取回、可失效 为什么先建高召回技能图，再做反事实校准？ 语义、词法、I/O 和结构证据可以提出可能依赖，但相似或接口相连不一定真有用。CaSKG 先保留候选关系，再通过删除、替换、重排探针观察影响并平滑边可靠性，避免把初始图中的所有连接都直接发布为可靠技能关系。 例如两技能经常共现不代表先后必要，重排或移除探针可帮助检验当前任务中这条依赖是否值得保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-caskg-e0c69536" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f00340222eb367d2">为什么先建高召回技能图，再做反事实校准？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acaskg">CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Jilin University / Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义、词法、I/O 和结构证据可以提出可能依赖，但相似或接口相连不一定真有用。CaSKG 先保留候选关系，再通过删除、替换、重排探针观察影响并平滑边可靠性，避免把初始图中的所有连接都直接发布为可靠技能关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两技能经常共现不代表先后必要，重排或移除探针可帮助检验当前任务中这条依赖是否值得保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25500">原论文</a> · <a href="../../../../agent-research/2608.25500-caskg/">实现解读</a> · <a href="#qa-f00340222eb367d2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:caskg" data-paper-title="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval Agent Jilin University / Ant Group 2026-08-26 先从语义、词法、I/O 和结构证据建高召回有向图，再以 remove、substitute、reorder 三类文本反事实探针校准边，Bayesian smoothing 后只发布可靠关系。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。CaSKG 从训练 split 学习可复用 skill 路由，在隔离 test 上结合图式记忆与候选验证调用工具。ToolRoute-L2.1 三 seed 的 joint success 为 0.8000，plan step F1 为 0.8327，平均成本 5.0116。  反事实因果技能图 Agent 记忆与技能：让经验可取回、可失效 为什么技能图中的语义或 I/O 相似边，还要用 remove、substitute、reorder 探针校准？ 相似性适合高召回，却不证明某技能真正依赖另一技能或应按该顺序执行。文本反事实改变局部结构，观察关系是否仍成立，再经平滑筛出更可靠边；这提供的是探针条件下的关系证据，不能自动宣称已经完成真实环境的因果效应验证。 例如两个技能都提文件上传，删除认证步骤后才暴露前置依赖；仅凭共同词汇把它们连成可互换关系可能出错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:caskg" data-paper-title="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval Agent Jilin University / Ant Group 2026-08-26 先从语义、词法、I/O 和结构证据建高召回有向图，再以 remove、substitute、reorder 三类文本反事实探针校准边，Bayesian smoothing 后只发布可靠关系。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。CaSKG 从训练 split 学习可复用 skill 路由，在隔离 test 上结合图式记忆与候选验证调用工具。ToolRoute-L2.1 三 seed 的 joint success 为 0.8000，plan step F1 为 0.8327，平均成本 5.0116。  反事实因果技能图 Agent 记忆与技能：让经验可取回、可失效 文本反事实探针与真实环境因果干预的证据强度有什么不同？ 文本探针修改技能描述或顺序，提供关系校准信号，但可能只反映模型对措辞的判断；真实环境执行还需验证操作后果与任务状态。不能因名称含 causal 就把文本边可靠性解释为不受混杂的实际因果效应，机制与能力评价要分开。 例如模型认为删除某段会失败，但实际环境可能有另一工具完成同样功能；文本预测仍需真实执行检验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d742c44657a118f8">文本反事实探针与真实环境因果干预的证据强度有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acaskg">CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Jilin University / Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文本探针修改技能描述或顺序，提供关系校准信号，但可能只反映模型对措辞的判断；真实环境执行还需验证操作后果与任务状态。不能因名称含 causal 就把文本边可靠性解释为不受混杂的实际因果效应，机制与能力评价要分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型认为删除某段会失败，但实际环境可能有另一工具完成同样功能；文本预测仍需真实执行检验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25500">原论文</a> · <a href="../../../../agent-research/2608.25500-caskg/">实现解读</a> · <a href="#qa-d742c44657a118f8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:caskg" data-paper-title="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval Agent Jilin University / Ant Group 2026-08-26 先从语义、词法、I/O 和结构证据建高召回有向图，再以 remove、substitute、reorder 三类文本反事实探针校准边，Bayesian smoothing 后只发布可靠关系。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。CaSKG 从训练 split 学习可复用 skill 路由，在隔离 test 上结合图式记忆与候选验证调用工具。ToolRoute-L2.1 三 seed 的 joint success 为 0.8000，plan step F1 为 0.8327，平均成本 5.0116。  反事实因果技能图 Agent 记忆与技能：让经验可取回、可失效 Bayesian smoothing 中 s、n 与先验分别起什么作用？ 后验边分数为 (α0+s)/(α0+β0+n)，成功证据增加支持，探针数量控制置信收缩，先验避免少样本极端值；只有超过阈值的边发布。不能把一次探针成功直接记成概率一，本地 ToolRoute 隔离结果也不等于原论文完整环境复刻。 例如一条边只测一次成功，带先验后不应与测试百次都成功的边完全等同；二者可靠性证据量不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8d9c99d17e5d0f4b">Bayesian smoothing 中 s、n 与先验分别起什么作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acaskg">CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Jilin University / Ant Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后验边分数为 (α0+s)/(α0+β0+n)，成功证据增加支持，探针数量控制置信收缩，先验避免少样本极端值；只有超过阈值的边发布。不能把一次探针成功直接记成概率一，本地 ToolRoute 隔离结果也不等于原论文完整环境复刻。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条边只测一次成功，带先验后不应与测试百次都成功的边完全等同；二者可靠性证据量不同。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25500">原论文</a> · <a href="../../../../agent-research/2608.25500-caskg/">实现解读</a> · <a href="#qa-8d9c99d17e5d0f4b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skill-state" data-paper-title="SKILL.state: Scalable Long-Horizon Agent Skills" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SKILL.state: Scalable Long-Horizon Agent Skills Agent Google 2026-08-26 普通Agent把旧观察、动作和推理反复塞回下一轮。SKILL.state把可持续的信息投影到当前执行状态，每步只传技能说明、状态和最新观察；不是在完整对话外再加一个状态块。模型生成结构化patch和动作，运行时验证后提交，瞬时推理不保留。定义性流程见§3与算法1。 成本过高，不复现（审查 DONE）；actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；运行时实际执行递归合并、null删除、schema拒绝、原状态保留及有界重试。传入actor的是只含三种公共信息的不可变字符串视图，不包含gold、grader、旧回答或旧观察。actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；不是语言模型。  Agent运行时 显式执行状态与上下文控制 Agent 记忆与技能：让经验可取回、可失效 SKILL.state 为什么不把完整历史和显式状态同时送给模型？ 目标是以足够的结构化状态承接过去信息，下一轮只读技能说明、状态和最新观察；若仍附完整历史，就绕过状态覆盖要求并恢复上下文增长。该设计依赖 schema 能表达必要信息，历史本身是审计对象或 schema 不充分时可能不适合。 例如已完成步骤和待办写入状态后，下一轮不再重放十轮思考；遗漏订单号会真实影响后续，不能再从隐藏历史补回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-skill-state-4eba9d90" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-dda177944e00eb4a">SKILL.state 为什么不把完整历史和显式状态同时送给模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askill-state">SKILL.state: Scalable Long-Horizon Agent Skills</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是以足够的结构化状态承接过去信息，下一轮只读技能说明、状态和最新观察；若仍附完整历史，就绕过状态覆盖要求并恢复上下文增长。该设计依赖 schema 能表达必要信息，历史本身是审计对象或 schema 不充分时可能不适合。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如已完成步骤和待办写入状态后，下一轮不再重放十轮思考；遗漏订单号会真实影响后续，不能再从隐藏历史补回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26263">原论文</a> · <a href="../../../../agent-research/2608.26263-skill-state/">实现解读</a> · <a href="#qa-dda177944e00eb4a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skill-state" data-paper-title="SKILL.state: Scalable Long-Horizon Agent Skills" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SKILL.state: Scalable Long-Horizon Agent Skills Agent Google 2026-08-26 普通Agent把旧观察、动作和推理反复塞回下一轮。SKILL.state把可持续的信息投影到当前执行状态，每步只传技能说明、状态和最新观察；不是在完整对话外再加一个状态块。模型生成结构化patch和动作，运行时验证后提交，瞬时推理不保留。定义性流程见§3与算法1。 成本过高，不复现（审查 DONE）；actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；运行时实际执行递归合并、null删除、schema拒绝、原状态保留及有界重试。传入actor的是只含三种公共信息的不可变字符串视图，不包含gold、grader、旧回答或旧观察。actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；不是语言模型。  Agent运行时 显式执行状态与上下文控制 Agent 记忆与技能：让经验可取回、可失效 SKILL.state 为什么不是“完整对话再加一个状态块”？ 下一步只接收技能说明、当前状态和最新观察，旧对话不再反复携带，因此可持续信息必须显式写入状态。递归 patch 保留未修改字段并允许删除，运行时验证后才提交；若仍传全部历史，就绕过了状态充分性和容量受限的核心要求。 例如前轮确认的文件路径要写入状态字段，下一轮才能使用；若偷偷保留整段聊天来找路径，就无法检验状态是否足够。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skill-state" data-paper-title="SKILL.state: Scalable Long-Horizon Agent Skills" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SKILL.state: Scalable Long-Horizon Agent Skills Agent Google 2026-08-26 普通Agent把旧观察、动作和推理反复塞回下一轮。SKILL.state把可持续的信息投影到当前执行状态，每步只传技能说明、状态和最新观察；不是在完整对话外再加一个状态块。模型生成结构化patch和动作，运行时验证后提交，瞬时推理不保留。定义性流程见§3与算法1。 成本过高，不复现（审查 DONE）；actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；运行时实际执行递归合并、null删除、schema拒绝、原状态保留及有界重试。传入actor的是只含三种公共信息的不可变字符串视图，不包含gold、grader、旧回答或旧观察。actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；不是语言模型。  Agent运行时 显式执行状态与上下文控制 Agent 记忆与技能：让经验可取回、可失效 固定 schema 状态与通用滚动摘要在更新合同上有何差别？ 结构状态以递归 patch 保留未改字段，并用 null 明确删除，类型与字段可由运行时验证；自然语言摘要更自由但难以精确约束覆盖和删除。结构合法也不保证内容忠实，不能由 schema 验证通过推导语言模型状态更新正确。 例如 patch 只改 progress 时旧 order_id 应保留；自然语言重写若忘记编号，不一定有同样明确的字段级拒绝机制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-274f24591f4571fd">固定 schema 状态与通用滚动摘要在更新合同上有何差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askill-state">SKILL.state: Scalable Long-Horizon Agent Skills</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>结构状态以递归 patch 保留未改字段，并用 null 明确删除，类型与字段可由运行时验证；自然语言摘要更自由但难以精确约束覆盖和删除。结构合法也不保证内容忠实，不能由 schema 验证通过推导语言模型状态更新正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 patch 只改 progress 时旧 order_id 应保留；自然语言重写若忘记编号，不一定有同样明确的字段级拒绝机制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26263">原论文</a> · <a href="../../../../agent-research/2608.26263-skill-state/">实现解读</a> · <a href="#qa-274f24591f4571fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skill-state" data-paper-title="SKILL.state: Scalable Long-Horizon Agent Skills" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SKILL.state: Scalable Long-Horizon Agent Skills Agent Google 2026-08-26 普通Agent把旧观察、动作和推理反复塞回下一轮。SKILL.state把可持续的信息投影到当前执行状态，每步只传技能说明、状态和最新观察；不是在完整对话外再加一个状态块。模型生成结构化patch和动作，运行时验证后提交，瞬时推理不保留。定义性流程见§3与算法1。 成本过高，不复现（审查 DONE）；actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；运行时实际执行递归合并、null删除、schema拒绝、原状态保留及有界重试。传入actor的是只含三种公共信息的不可变字符串视图，不包含gold、grader、旧回答或旧观察。actor与执行器由调用方注入，本地诊断只做公开计数事件和惰性动作回调；不是语言模型。  Agent运行时 显式执行状态与上下文控制 Agent 记忆与技能：让经验可取回、可失效 有效状态提交后动作执行失败，运行时是否已撤销状态和外部副作用？ 没有。原算法先提交有效状态再执行动作，本地执行器抛错不盲目重试，也不宣称撤销外部副作用；调用方须把失败作为最新观察处理。格式重试上限与字符 cap 是本地保护，计数事件诊断不表示真实 LLM 能正确产生 patch。 例如状态已记“尝试支付”后网络超时，不能自动重发付款；应先核查实际结果，避免一次逻辑动作产生两次支付。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f3d7aef13f674cc1">有效状态提交后动作执行失败，运行时是否已撤销状态和外部副作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askill-state">SKILL.state: Scalable Long-Horizon Agent Skills</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。原算法先提交有效状态再执行动作，本地执行器抛错不盲目重试，也不宣称撤销外部副作用；调用方须把失败作为最新观察处理。格式重试上限与字符 cap 是本地保护，计数事件诊断不表示真实 LLM 能正确产生 patch。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如状态已记“尝试支付”后网络超时，不能自动重发付款；应先核查实际结果，避免一次逻辑动作产生两次支付。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本与复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26263">原论文</a> · <a href="../../../../agent-research/2608.26263-skill-state/">实现解读</a> · <a href="#qa-f3d7aef13f674cc1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skillforge" data-paper-title="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents Agent AMAP, Alibaba Group 2026-08-25 SkillRL 类方法从轨迹提取技能后只追加，错误和过时技能会永久污染库。SkillForge 让 policy 输出环境动作时显式选择技能，把调用决策纳入 RL；成功、失败和对比轨迹经多路径 induction 生成候选，环境证据再决定激活、修订或去重。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。技能被显式调用，并根据环境证据更新 posterior 与修订状态。本地用结构化 plan 作为技能内容，执行调用、验证、posterior 与修订控制流；未运行 LLM teacher induction、ALFWorld/WebShop/AppWorld 或 RL 训练。PlanBench-mini 120 episodes：创建 12 个技能、复用 108 次，joint success 1.0000，平均成本 0.6200。  可验证技能锻造 Agent 记忆与技能：让经验可取回、可失效 为什么技能库不能从轨迹提取后永远只追加？ 成功经验可能只适用于旧环境，失败总结也可能错误，永久追加会让过时内容继续被调用。SkillForge 让环境证据决定激活、修订或去重，并把技能选择和环境动作一起作为策略输出；库变大并非进步，技能使用和内容都需持续检验。 例如旧版工具要求某参数，新版已废弃，该技能若只追加不修订，会在后续任务重复制造相同调用错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-skillforge-0aa71f73" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-06b43e737dc5b20f">为什么技能库不能从轨迹提取后永远只追加？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askillforge">SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AMAP, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成功经验可能只适用于旧环境，失败总结也可能错误，永久追加会让过时内容继续被调用。SkillForge 让环境证据决定激活、修订或去重，并把技能选择和环境动作一起作为策略输出；库变大并非进步，技能使用和内容都需持续检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧版工具要求某参数，新版已废弃，该技能若只追加不修订，会在后续任务重复制造相同调用错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24747">原论文</a> · <a href="../../../../agent-research/2608.24747-skillforge/">实现解读</a> · <a href="#qa-06b43e737dc5b20f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skillforge" data-paper-title="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents Agent AMAP, Alibaba Group 2026-08-25 SkillRL 类方法从轨迹提取技能后只追加，错误和过时技能会永久污染库。SkillForge 让 policy 输出环境动作时显式选择技能，把调用决策纳入 RL；成功、失败和对比轨迹经多路径 induction 生成候选，环境证据再决定激活、修订或去重。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。技能被显式调用，并根据环境证据更新 posterior 与修订状态。本地用结构化 plan 作为技能内容，执行调用、验证、posterior 与修订控制流；未运行 LLM teacher induction、ALFWorld/WebShop/AppWorld 或 RL 训练。PlanBench-mini 120 episodes：创建 12 个技能、复用 108 次，joint success 1.0000，平均成本 0.6200。  可验证技能锻造 Agent 记忆与技能：让经验可取回、可失效 为什么技能候选要经历激活、修订或去重，而不从成功轨迹提取后直接永久追加？ 单次成功可能依赖偶然环境，旧技能还会过时或互相冲突。多路径归纳先产生候选，调用策略和环境反馈再决定是否使用及怎样修订，把技能选择纳入学习；追加只增加库容量，却不能保证候选适用或避免错误被反复检索强化。 例如成功下载经验写死了旧按钮名称，新界面失败后应修订或停用该技能，而不是把第二份相近文档继续叠到库里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skillforge" data-paper-title="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents Agent AMAP, Alibaba Group 2026-08-25 SkillRL 类方法从轨迹提取技能后只追加，错误和过时技能会永久污染库。SkillForge 让 policy 输出环境动作时显式选择技能，把调用决策纳入 RL；成功、失败和对比轨迹经多路径 induction 生成候选，环境证据再决定激活、修订或去重。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。技能被显式调用，并根据环境证据更新 posterior 与修订状态。本地用结构化 plan 作为技能内容，执行调用、验证、posterior 与修订控制流；未运行 LLM teacher induction、ALFWorld/WebShop/AppWorld 或 RL 训练。PlanBench-mini 120 episodes：创建 12 个技能、复用 108 次，joint success 1.0000，平均成本 0.6200。  可验证技能锻造 Agent 记忆与技能：让经验可取回、可失效 从成功、失败与对比轨迹多路径 induction，与只总结成功有何不同？ 成功轨迹提供可用步骤，失败暴露边界，对比轨迹帮助识别关键差异，候选因此不局限于复述一次成功。归纳仍只是提案，环境验证后才决定是否激活；不能把失败叙述中的猜测直接写成可靠规则，或用同一 case 成功证明通用。 例如成功与失败都用了相同查询，只有成功额外校验结果，可将“校验”提出为候选必要步骤，再验证而非直接宣告因果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f88f7b4c307b67d5">从成功、失败与对比轨迹多路径 induction，与只总结成功有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askillforge">SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AMAP, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成功轨迹提供可用步骤，失败暴露边界，对比轨迹帮助识别关键差异，候选因此不局限于复述一次成功。归纳仍只是提案，环境验证后才决定是否激活；不能把失败叙述中的猜测直接写成可靠规则，或用同一 case 成功证明通用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如成功与失败都用了相同查询，只有成功额外校验结果，可将“校验”提出为候选必要步骤，再验证而非直接宣告因果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24747">原论文</a> · <a href="../../../../agent-research/2608.24747-skillforge/">实现解读</a> · <a href="#qa-f88f7b4c307b67d5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skillforge" data-paper-title="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents Agent AMAP, Alibaba Group 2026-08-25 SkillRL 类方法从轨迹提取技能后只追加，错误和过时技能会永久污染库。SkillForge 让 policy 输出环境动作时显式选择技能，把调用决策纳入 RL；成功、失败和对比轨迹经多路径 induction 生成候选，环境证据再决定激活、修订或去重。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。技能被显式调用，并根据环境证据更新 posterior 与修订状态。本地用结构化 plan 作为技能内容，执行调用、验证、posterior 与修订控制流；未运行 LLM teacher induction、ALFWorld/WebShop/AppWorld 或 RL 训练。PlanBench-mini 120 episodes：创建 12 个技能、复用 108 次，joint success 1.0000，平均成本 0.6200。  可验证技能锻造 Agent 记忆与技能：让经验可取回、可失效 a_t=(环境动作,技能选择) 对本地验证提出什么要求？ 要记录策略在行动时实际选择了哪个技能及执行后果，不能只在日志中事后贴技能名。本地以结构化 plan 验证调用、posterior 与修订控制流，没有 LLM teacher induction 或 RL 训练，技能复用计数不能当成学得策略或论文环境成绩。 例如动作已执行完再挑一份相似技能做解释，不算策略真正使用技能；选择应在行动生成时影响执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-06647be6cbb7bceb">a_t=(环境动作,技能选择) 对本地验证提出什么要求？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askillforge">SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AMAP, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>要记录策略在行动时实际选择了哪个技能及执行后果，不能只在日志中事后贴技能名。本地以结构化 plan 验证调用、posterior 与修订控制流，没有 LLM teacher induction 或 RL 训练，技能复用计数不能当成学得策略或论文环境成绩。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如动作已执行完再挑一份相似技能做解释，不算策略真正使用技能；选择应在行动生成时影响执行。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24747">原论文</a> · <a href="../../../../agent-research/2608.24747-skillforge/">实现解读</a> · <a href="#qa-06647be6cbb7bceb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hymem" data-paper-title="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation Agent Institute of Automation, Chinese Academy of Sciences 2026-08-16 把 planning、execution 和 isolated reasoning 分层，结构化摘要在 context refresh 间保存任务进展。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  记忆 长时序 Agent Agent 记忆与技能：让经验可取回、可失效 planning、execution 与 isolated reasoning 为什么分别维护上下文？ 规划关注全局目标，执行处理具体工具状态，隔离推理承接局部分析，分层可避免每轮把所有细节互相污染。结构化进展摘要在 refresh 时保留必要联系；隔离不是删除证据，层间仍需公开结果接口，否则规划可能失去实际执行状态。 例如执行层产生长测试日志，只将失败类型和文件位置回传规划层，局部分析另开上下文而不反复复制全部日志。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-hymem-ebf0c9bb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6f117905da9d1b3c">planning、execution 与 isolated reasoning 为什么分别维护上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahymem">HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>规划关注全局目标，执行处理具体工具状态，隔离推理承接局部分析，分层可避免每轮把所有细节互相污染。结构化进展摘要在 refresh 时保留必要联系；隔离不是删除证据，层间仍需公开结果接口，否则规划可能失去实际执行状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如执行层产生长测试日志，只将失败类型和文件位置回传规划层，局部分析另开上下文而不反复复制全部日志。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.15703">原论文</a> · <a href="../../../../agent-research/2608.15703-hymem/">实现解读</a> · <a href="#qa-6f117905da9d1b3c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hymem" data-paper-title="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation Agent Institute of Automation, Chinese Academy of Sciences 2026-08-16 把 planning、execution 和 isolated reasoning 分层，结构化摘要在 context refresh 间保存任务进展。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  记忆 长时序 Agent Agent 记忆与技能：让经验可取回、可失效 规划、执行和 isolated reasoning 分层，为什么能减少上下文污染？ 不同层需要的信息粒度不同：规划关注目标进度，执行关注当前操作，临时推理无需永久传播。刷新间由结构化摘要保留必要状态，可避免大量局部猜测挤占长期任务信息；隔离并不等于证据自动正确，摘要仍须保留关键约束与来源。 例如一次调试尝试产生很多假设，只把验证后的接口变化和剩余问题传回规划层，不让所有临时猜想变成长期事实。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hymem" data-paper-title="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation Agent Institute of Automation, Chinese Academy of Sciences 2026-08-16 把 planning、execution 和 isolated reasoning 分层，结构化摘要在 context refresh 间保存任务进展。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  记忆 长时序 Agent Agent 记忆与技能：让经验可取回、可失效 分层隔离与单一长历史相比，主要改变什么信息流？ 单一历史让所有角色持续读取同一增长序列，分层方式限制各层可见范围并用摘要交接。它可能降低重复输入，也依赖摘要足够保留事实，不能仅按短上下文推断更高成功率；需要把摘要遗漏和层间失配作为实际风险评估。 例如规划层只见“测试失败”却没见失败文件，就可能派错下一步；层级结构本身无法补上过于粗糙的摘要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6af66bb3ebb4bbd4">分层隔离与单一长历史相比，主要改变什么信息流？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahymem">HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单一历史让所有角色持续读取同一增长序列，分层方式限制各层可见范围并用摘要交接。它可能降低重复输入，也依赖摘要足够保留事实，不能仅按短上下文推断更高成功率；需要把摘要遗漏和层间失配作为实际风险评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如规划层只见“测试失败”却没见失败文件，就可能派错下一步；层级结构本身无法补上过于粗糙的摘要。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.15703">原论文</a> · <a href="../../../../agent-research/2608.15703-hymem/">实现解读</a> · <a href="#qa-6af66bb3ebb4bbd4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hymem" data-paper-title="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation Agent Institute of Automation, Chinese Academy of Sciences 2026-08-16 把 planning、execution 和 isolated reasoning 分层，结构化摘要在 context refresh 间保存任务进展。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  记忆 长时序 Agent Agent 记忆与技能：让经验可取回、可失效 本地确定性 PlanBench 结果能否表明已跑 GAIA 或 BrowseComp-plus？ 不能。本地只验证分层上下文、刷新摘要和机制计数，没有浏览器、外部工具服务或论文大模型。mini-suite 的成本单位和饱和正确率属于受控协议，不能移植为真实长程 token 费用，也不能与原文 Pass@1 横比。 例如受控流程中一次摘要只记一个事件，不说明真实网页证据摘要也能用相同成本保留关键内容。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e300338bfd858cc0">本地确定性 PlanBench 结果能否表明已跑 GAIA 或 BrowseComp-plus？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahymem">HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Automation, Chinese Academy of Sciences</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地只验证分层上下文、刷新摘要和机制计数，没有浏览器、外部工具服务或论文大模型。mini-suite 的成本单位和饱和正确率属于受控协议，不能移植为真实长程 token 费用，也不能与原文 Pass@1 横比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如受控流程中一次摘要只记一个事件，不说明真实网页证据摘要也能用相同成本保留关键内容。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.15703">原论文</a> · <a href="../../../../agent-research/2608.15703-hymem/">实现解读</a> · <a href="#qa-e300338bfd858cc0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gse" data-paper-title="Learning Globally Reusable Skills for Coding Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Globally Reusable Skills for Coding Agents Agent Tianjin University 2026-08-06 主题：全局技能进化。GSE 用 Skill Relation Graph 显式维护技能关系，以聚类合并局部经验，并通过 replay verification 防止过拟合与行为回退。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的全局技能进化算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  全局技能进化 Agent 记忆与技能：让经验可取回、可失效 GSE 的全局可复用技能为什么需要 Skill Relation Graph？ 局部经验之间可能重叠、互补或冲突，关系图提供聚类与合并依据，让技能能跨任务复用而不是保留大量近重复片段。图关系仍需证据，语义相似不自动表示合并安全，尤其不同环境前提可能被抽象过程抹掉。 例如两任务都执行测试，但一个要求先生成配置，另一个已有配置，合并技能时应保留这个前提差异。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-gse-c467dca4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a0059fed14785844">GSE 的全局可复用技能为什么需要 Skill Relation Graph？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agse">Learning Globally Reusable Skills for Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>局部经验之间可能重叠、互补或冲突，关系图提供聚类与合并依据，让技能能跨任务复用而不是保留大量近重复片段。图关系仍需证据，语义相似不自动表示合并安全，尤其不同环境前提可能被抽象过程抹掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两任务都执行测试，但一个要求先生成配置，另一个已有配置，合并技能时应保留这个前提差异。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06153">原论文</a> · <a href="../../../../agent-research/2608.06153-gse/">实现解读</a> · <a href="#qa-a0059fed14785844">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gse" data-paper-title="Learning Globally Reusable Skills for Coding Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Globally Reusable Skills for Coding Agents Agent Tianjin University 2026-08-06 主题：全局技能进化。GSE 用 Skill Relation Graph 显式维护技能关系，以聚类合并局部经验，并通过 replay verification 防止过拟合与行为回退。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的全局技能进化算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  全局技能进化 Agent 记忆与技能：让经验可取回、可失效 为什么把相似局部技能聚类合并后，还要做 replay verification？ 相似描述可能隐藏不同前置条件，合并会删掉对某些任务关键的分支。重放原有案例可检验全局复用是否以牺牲旧行为为代价，技能关系图再显式管理冲突；聚类紧凑度或新任务成功不能单独证明合并安全，也不等于跨分布泛化。 例如两个文件解析技能分别处理带表头与无表头输入，合并后应重放两类案例，避免统一流程只留下其中一种假设。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gse" data-paper-title="Learning Globally Reusable Skills for Coding Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Globally Reusable Skills for Coding Agents Agent Tianjin University 2026-08-06 主题：全局技能进化。GSE 用 Skill Relation Graph 显式维护技能关系，以聚类合并局部经验，并通过 replay verification 防止过拟合与行为回退。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的全局技能进化算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  全局技能进化 Agent 记忆与技能：让经验可取回、可失效 聚类合并后 replay verification 与只看新任务成功有何区别？ 新任务成功只说明候选适合当前情境，replay 重新检查已有行为，帮助发现抽象后回归。它约束全局复用的代价，仍受回放任务覆盖限制；不能因为少量旧 case 都通过就声称所有任务都不退化。 例如合并后的技能简化了安装步骤，在新仓库通过，却可能删掉旧仓库必要环境变量；旧轨迹回放可以暴露该问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a4e90ad057a46e13">聚类合并后 replay verification 与只看新任务成功有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agse">Learning Globally Reusable Skills for Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>新任务成功只说明候选适合当前情境，replay 重新检查已有行为，帮助发现抽象后回归。它约束全局复用的代价，仍受回放任务覆盖限制；不能因为少量旧 case 都通过就声称所有任务都不退化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如合并后的技能简化了安装步骤，在新仓库通过，却可能删掉旧仓库必要环境变量；旧轨迹回放可以暴露该问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06153">原论文</a> · <a href="../../../../agent-research/2608.06153-gse/">实现解读</a> · <a href="#qa-a4e90ad057a46e13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gse" data-paper-title="Learning Globally Reusable Skills for Coding Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Globally Reusable Skills for Coding Agents Agent Tianjin University 2026-08-06 主题：全局技能进化。GSE 用 Skill Relation Graph 显式维护技能关系，以聚类合并局部经验，并通过 replay verification 防止过拟合与行为回退。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的全局技能进化算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  全局技能进化 Agent 记忆与技能：让经验可取回、可失效 本地关系图与回归惩罚验证能否复刻工业 Agent F1？ 不能。本地公共 mini-suite 执行图、选择与回归相关算子，未运行原文大模型、私有工业环境或昂贵 judge。原文工业 F1 属于作者完整系统证据，不能把本地图规模减少或 fixture 分数解释为相同业务质量提升。 例如聚类后十条技能变成五条，可验证合并发生；没有工业测试生成任务就不能由此推算 precision 或 recall。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a3a2c16881999ef1">本地关系图与回归惩罚验证能否复刻工业 Agent F1？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agse">Learning Globally Reusable Skills for Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tianjin University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地公共 mini-suite 执行图、选择与回归相关算子，未运行原文大模型、私有工业环境或昂贵 judge。原文工业 F1 属于作者完整系统证据，不能把本地图规模减少或 fixture 分数解释为相同业务质量提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如聚类后十条技能变成五条，可验证合并发生；没有工业测试生成任务就不能由此推算 precision 或 recall。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06153">原论文</a> · <a href="../../../../agent-research/2608.06153-gse/">实现解读</a> · <a href="#qa-a3a2c16881999ef1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:vag" data-paper-title="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents Agent 论文未列机构 2026-08-06 主题：技能进化安全。技能一旦进入上下文会污染后代，事后删除无法彻底回滚。VaG 在写入前依次做结构、行为无害性、语义一致性验证，再以边际收益选择可共同使用的 Hot 技能集合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的技能进化安全算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  技能进化安全 Agent 记忆与技能：让经验可取回、可失效 技能污染为什么可能在删除原技能后继续存在？ 有害技能进入上下文后可能影响后续生成的技能与决策，污染已传播到后代，删除最初记录不等于回滚全部衍生影响。VaG 因而在写入前验证，试图阻止污染进入持久循环；它仍依赖验证覆盖，不能保证检测所有语义风险。 例如一份错误提交规则被总结进三份后续技能，只删原文件时，三个派生版本仍会继续传播同样错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-vag-dfb74800" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b7cc4ccf17a5ebda">技能污染为什么可能在删除原技能后继续存在？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avag">When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有害技能进入上下文后可能影响后续生成的技能与决策，污染已传播到后代，删除最初记录不等于回滚全部衍生影响。VaG 因而在写入前验证，试图阻止污染进入持久循环；它仍依赖验证覆盖，不能保证检测所有语义风险。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一份错误提交规则被总结进三份后续技能，只删原文件时，三个派生版本仍会继续传播同样错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05810">原论文</a> · <a href="../../../../agent-research/2608.05810-vag/">实现解读</a> · <a href="#qa-b7cc4ccf17a5ebda">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:vag" data-paper-title="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents Agent 论文未列机构 2026-08-06 主题：技能进化安全。技能一旦进入上下文会污染后代，事后删除无法彻底回滚。VaG 在写入前依次做结构、行为无害性、语义一致性验证，再以边际收益选择可共同使用的 Hot 技能集合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的技能进化安全算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  技能进化安全 Agent 记忆与技能：让经验可取回、可失效 为什么技能写入前的验证，不能完全由写入后发现有害再删除替代？ 技能一旦影响新轨迹和后代技能，污染可能已传播，删除原条目不能撤销所有衍生结果。预提交依次检查结构、行为无害性和语义一致性，再选择能共同使用的集合，把准入与运行后回滚分开；单个技能看似有效也不保证组合没有冲突。 例如错误重试规则已被另一技能吸收，删除最早文档也不会自动修复后者；写入前验证能减少这种继承污染。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:vag" data-paper-title="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents Agent 论文未列机构 2026-08-06 主题：技能进化安全。技能一旦进入上下文会污染后代，事后删除无法彻底回滚。VaG 在写入前依次做结构、行为无害性、语义一致性验证，再以边际收益选择可共同使用的 Hot 技能集合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的技能进化安全算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  技能进化安全 Agent 记忆与技能：让经验可取回、可失效 pre-commit gate 与任务失败后清理技能有什么取舍？ 前置 gate 在结构、行为无害性和语义一致性阶段阻止不合格候选进入库，后置清理则已允许它影响执行和后代。前置验证增加准入成本，也可能误拒有用技能；机制重点是控制传播时点，不能把 gate 通过视为绝对安全证明。 例如新技能建议跳过验证，写入前可被无害性检查拒绝；等它造成失败后删除，已经影响的动作无法因此撤销。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-28954ff9e44b5448">pre-commit gate 与任务失败后清理技能有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avag">When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前置 gate 在结构、行为无害性和语义一致性阶段阻止不合格候选进入库，后置清理则已允许它影响执行和后代。前置验证增加准入成本，也可能误拒有用技能；机制重点是控制传播时点，不能把 gate 通过视为绝对安全证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新技能建议跳过验证，写入前可被无害性检查拒绝；等它造成失败后删除，已经影响的动作无法因此撤销。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05810">原论文</a> · <a href="../../../../agent-research/2608.05810-vag/">实现解读</a> · <a href="#qa-28954ff9e44b5448">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:vag" data-paper-title="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents Agent 论文未列机构 2026-08-06 主题：技能进化安全。技能一旦进入上下文会污染后代，事后删除无法彻底回滚。VaG 在写入前依次做结构、行为无害性、语义一致性验证，再以边际收益选择可共同使用的 Hot 技能集合。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的技能进化安全算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  技能进化安全 Agent 记忆与技能：让经验可取回、可失效 Hot 技能集合为什么不能把所有单独高分技能直接并列使用？ 技能间可能冲突或重复，集合收益取决于共同上下文，VaG 按边际收益选择可兼容组合，而非独立分数相加。本地只验证门控与选择算子，不运行昂贵 judge 或原环境；候选发现的注册也不自动证明真实可晋级控制器已集成。 例如两份技能各自有效，一份要求先缓存、一份要求每步清缓存，同时加载可能互相矛盾，需要集合级兼容判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-341ae6021330275f">Hot 技能集合为什么不能把所有单独高分技能直接并列使用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avag">When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>技能间可能冲突或重复，集合收益取决于共同上下文，VaG 按边际收益选择可兼容组合，而非独立分数相加。本地只验证门控与选择算子，不运行昂贵 judge 或原环境；候选发现的注册也不自动证明真实可晋级控制器已集成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两份技能各自有效，一份要求先缓存、一份要求每步清缓存，同时加载可能互相矛盾，需要集合级兼容判断。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05810">原论文</a> · <a href="../../../../agent-research/2608.05810-vag/">实现解读</a> · <a href="#qa-341ae6021330275f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memorycpt" data-paper-title="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off Agent Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS 2026-08-05 主题：端到端 Agent 记忆。QAD 将离线记忆构建链蒸馏为紧凑模型；QAR 用 RRF 检索和 LoRA summarizer 生成查询相关上下文，并以成本感知 GRPO 优化 Quality per Cost。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的端到端 Agent 记忆算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  端到端 Agent 记忆 Agent 记忆与技能：让经验可取回、可失效 QAD 与 QAR 为什么分别处理构建和查询阶段？ QAD 把离线记忆构建链蒸馏到紧凑模型，降低反复写入成本；QAR 在查询时融合检索并生成问题相关上下文，提高有限读取的用途。两者针对不同成本来源，省掉其中一段并不能声称完整端到端记忆配方已执行。 例如历史进入系统时由小模型整理，用户提问时再用检索与摘要挑相关内容，而不是每次从头运行完整大模型构建链。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memorycpt-45f8aee7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8ddb0c3f29f9f1b1">QAD 与 QAR 为什么分别处理构建和查询阶段？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemorycpt">MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>QAD 把离线记忆构建链蒸馏到紧凑模型，降低反复写入成本；QAR 在查询时融合检索并生成问题相关上下文，提高有限读取的用途。两者针对不同成本来源，省掉其中一段并不能声称完整端到端记忆配方已执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如历史进入系统时由小模型整理，用户提问时再用检索与摘要挑相关内容，而不是每次从头运行完整大模型构建链。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04843">原论文</a> · <a href="../../../../agent-research/2608.04843-memorycpt/">实现解读</a> · <a href="#qa-8ddb0c3f29f9f1b1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memorycpt" data-paper-title="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off Agent Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS 2026-08-05 主题：端到端 Agent 记忆。QAD 将离线记忆构建链蒸馏为紧凑模型；QAR 用 RRF 检索和 LoRA summarizer 生成查询相关上下文，并以成本感知 GRPO 优化 Quality per Cost。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的端到端 Agent 记忆算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  端到端 Agent 记忆 Agent 记忆与技能：让经验可取回、可失效 以 Quality per Cost 为目标，为什么不能只追求更短的查询摘要？ 成本减少若损害回答质量，比例目标未必改善；同时构建、检索和总结各自都有推理费用。离线链蒸馏降低构建开销，RRF 与查询相关总结控制读取成本，再用成本感知奖励评价整体；应在相同质量口径下比较，而非把 token 少直接当成功。 例如把五百字证据压到二十字虽便宜，却漏掉关键例外导致答错；保留八十字正确依据可能有更高质量成本比。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memorycpt" data-paper-title="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off Agent Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS 2026-08-05 主题：端到端 Agent 记忆。QAD 将离线记忆构建链蒸馏为紧凑模型；QAR 用 RRF 检索和 LoRA summarizer 生成查询相关上下文，并以成本感知 GRPO 优化 Quality per Cost。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的端到端 Agent 记忆算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  端到端 Agent 记忆 Agent 记忆与技能：让经验可取回、可失效 Quality per Cost 与只最大化答案质量有什么取舍？ 只追质量可能无限增加检索和推理，QPC 将质量与推理成本一起考虑，偏好在合理代价下有效回答。比值也可能偏向极便宜但质量不足的方案，因此应同时报告原始质量和成本，不能只摘一个更高比值掩盖任务成功下降。 例如方案甲质量九成成本十，乙八成成本二，比值可偏向乙；用户是否接受八成质量仍需明确，而非由比值自动决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c04a3362054db9b8">Quality per Cost 与只最大化答案质量有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemorycpt">MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只追质量可能无限增加检索和推理，QPC 将质量与推理成本一起考虑，偏好在合理代价下有效回答。比值也可能偏向极便宜但质量不足的方案，因此应同时报告原始质量和成本，不能只摘一个更高比值掩盖任务成功下降。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如方案甲质量九成成本十，乙八成成本二，比值可偏向乙；用户是否接受八成质量仍需明确，而非由比值自动决定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04843">原论文</a> · <a href="../../../../agent-research/2608.04843-memorycpt/">实现解读</a> · <a href="#qa-c04a3362054db9b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memorycpt" data-paper-title="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off Agent Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS 2026-08-05 主题：端到端 Agent 记忆。QAD 将离线记忆构建链蒸馏为紧凑模型；QAR 用 RRF 检索和 LoRA summarizer 生成查询相关上下文，并以成本感知 GRPO 优化 Quality per Cost。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的端到端 Agent 记忆算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  端到端 Agent 记忆 Agent 记忆与技能：让经验可取回、可失效 RRF 检索与 LoRA summarizer 可以用一次文本拼接冒充吗？ 不可以。RRF 需要实际融合多个排名，summarizer 要生成查询相关上下文，成本感知 GRPO 还需真实奖励与更新。本地仅保留相应核心选择或状态诊断，未训练论文大模型与完整 benchmark，不能把接口字段存在称为蒸馏和 RL 已完成。 例如把两份检索列表直接串起来既没有倒数排名融合，也没有学习摘要；结果能输入模型不表示执行了 QAR。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-acc6e61b27c2664b">RRF 检索与 LoRA summarizer 可以用一次文本拼接冒充吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemorycpt">MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不可以。RRF 需要实际融合多个排名，summarizer 要生成查询相关上下文，成本感知 GRPO 还需真实奖励与更新。本地仅保留相应核心选择或状态诊断，未训练论文大模型与完整 benchmark，不能把接口字段存在称为蒸馏和 RL 已完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把两份检索列表直接串起来既没有倒数排名融合，也没有学习摘要；结果能输入模型不表示执行了 QAR。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.04843">原论文</a> · <a href="../../../../agent-research/2608.04843-memorycpt/">实现解读</a> · <a href="#qa-acc6e61b27c2664b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:vermem" data-paper-title="VerMem" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="VerMem Agent Sun Yat-sen University 2026-08-04 长期记忆、活动上下文与 episodic history 往往分开优化，轨迹奖励无法判断单次记忆操作是否正确。VerMem 用一个策略管理三类状态和七种原子操作，以 local verifier 审核状态转移、global verifier 审核证据一致性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。显式维护 LTM、active context、episodes，执行 retrieve/add/restore，并分别计数 local/global verifier。  可验证统一记忆 Agent 记忆与技能：让经验可取回、可失效 长期记忆、活动上下文和 episodic history 为什么要统一管理？ 三类状态决定信息保存位置和当前可见性，分开优化可能造成写入、恢复和读取之间不一致。VerMem 由同一策略选择原子操作，局部验证状态转移、全局验证最终证据一致性；统一策略并不意味着三类状态相同或可以任意互换。 例如事实已归档到长期记忆，当前回答前需 retrieve 或 restore 进入活动上下文；仅在历史里存在并不保证模型能读到。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-vermem-8bc3a085" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-de819e9cc69de79c">长期记忆、活动上下文和 episodic history 为什么要统一管理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avermem">VerMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>三类状态决定信息保存位置和当前可见性，分开优化可能造成写入、恢复和读取之间不一致。VerMem 由同一策略选择原子操作，局部验证状态转移、全局验证最终证据一致性；统一策略并不意味着三类状态相同或可以任意互换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如事实已归档到长期记忆，当前回答前需 retrieve 或 restore 进入活动上下文；仅在历史里存在并不保证模型能读到。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03137">原论文</a> · <a href="../../../../agent-research/2608.03137-vermem/">实现解读</a> · <a href="#qa-de819e9cc69de79c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:vermem" data-paper-title="VerMem" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="VerMem Agent Sun Yat-sen University 2026-08-04 长期记忆、活动上下文与 episodic history 往往分开优化，轨迹奖励无法判断单次记忆操作是否正确。VerMem 用一个策略管理三类状态和七种原子操作，以 local verifier 审核状态转移、global verifier 审核证据一致性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。显式维护 LTM、active context、episodes，执行 retrieve/add/restore，并分别计数 local/global verifier。  可验证统一记忆 Agent 记忆与技能：让经验可取回、可失效 local verifier 与 global verifier 为什么要分别检查记忆操作？ 局部验证器检查一次状态转移是否符合操作合同，无法独自判断长期证据是否前后一致；全局验证器补充整条轨迹与最终记忆的关系。二者与任务奖励共同训练状态管理，避免合法小步骤累积成错误事实；验证器通过率仍不是模型任务准确率。 例如删除字段这一操作格式合法，但删除了后续答案唯一依据，局部检查可能通过，全局证据一致性却应提出问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:vermem" data-paper-title="VerMem" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="VerMem Agent Sun Yat-sen University 2026-08-04 长期记忆、活动上下文与 episodic history 往往分开优化，轨迹奖励无法判断单次记忆操作是否正确。VerMem 用一个策略管理三类状态和七种原子操作，以 local verifier 审核状态转移、global verifier 审核证据一致性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。显式维护 LTM、active context、episodes，执行 retrieve/add/restore，并分别计数 local/global verifier。  可验证统一记忆 Agent 记忆与技能：让经验可取回、可失效 local verifier 与 global verifier 分别能发现什么？ local 检查某次操作前后状态是否合规则，global 检查完整轨迹和最终记忆证据是否一致。局部每步合法仍可能遗漏关键证据，最终结果好也不能证明每次记忆操作正确；二者与任务奖励、操作成本共同提供不同监督。 例如一次删除在格式上合法，却删掉最终回答唯一来源；局部检查可通过，全局证据一致性仍应发现问题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c058bd626ac200eb">local verifier 与 global verifier 分别能发现什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avermem">VerMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>local 检查某次操作前后状态是否合规则，global 检查完整轨迹和最终记忆证据是否一致。局部每步合法仍可能遗漏关键证据，最终结果好也不能证明每次记忆操作正确；二者与任务奖励、操作成本共同提供不同监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一次删除在格式上合法，却删掉最终回答唯一来源；局部检查可通过，全局证据一致性仍应发现问题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03137">原论文</a> · <a href="../../../../agent-research/2608.03137-vermem/">实现解读</a> · <a href="#qa-c058bd626ac200eb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:vermem" data-paper-title="VerMem" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="VerMem Agent Sun Yat-sen University 2026-08-04 长期记忆、活动上下文与 episodic history 往往分开优化，轨迹奖励无法判断单次记忆操作是否正确。VerMem 用一个策略管理三类状态和七种原子操作，以 local verifier 审核状态转移、global verifier 审核证据一致性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。显式维护 LTM、active context、episodes，执行 retrieve/add/restore，并分别计数 local/global verifier。  可验证统一记忆 Agent 记忆与技能：让经验可取回、可失效 本地原子操作有非零 telemetry 是否等于七种操作与完整 RL 都已复现？ 不等于。README 明确本地维护三种状态并执行 retrieve、add、restore 等核心路径，计数证明这些分支运行；未运行原文多卡 RL 或完整环境。宣传范围应以实际操作与预算合同为准，不能用方法名或非零计数替代完整训练。 例如 restore 计数大于零说明状态恢复被调用，不说明一个学得策略会在真实长程任务中正确选择恢复时机。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-0c718fe823cf49a9">本地原子操作有非零 telemetry 是否等于七种操作与完整 RL 都已复现？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avermem">VerMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等于。README 明确本地维护三种状态并执行 retrieve、add、restore 等核心路径，计数证明这些分支运行；未运行原文多卡 RL 或完整环境。宣传范围应以实际操作与预算合同为准，不能用方法名或非零计数替代完整训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 restore 计数大于零说明状态恢复被调用，不说明一个学得策略会在真实长程任务中正确选择恢复时机。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.03137">原论文</a> · <a href="../../../../agent-research/2608.03137-vermem/">实现解读</a> · <a href="#qa-0c718fe823cf49a9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coevo-mem" data-paper-title="CoEvo-Mem" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoEvo-Mem Agent 论文未列机构 2026-08-03 只优化 query routing 或只更新 memory bank 会忽略二者反馈环。CoEvo-Mem 让冻结 LLM 生成 route-specific rewrite 和 prior，轻量 residual router 在线修正；任务结果更新路由，轨迹反馈更新 memory value 与 graph relation，并交替冻结一侧控制非平稳性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 route rewrite、残差路由与 router/memory bank 交替更新；检索键包含任务轴和工具签名，防止跨任务误复用。  检索—记忆共进化 Agent 记忆与技能：让经验可取回、可失效 为什么路由策略与记忆库更新会互相影响？ 路由决定哪些记忆被使用，使用结果形成反馈更新路由与记忆价值；记忆内容和图关系变化又改变后续路由的收益。只优化一侧可能固化另一侧的缺陷，CoEvo-Mem 交替改进，但反馈只覆盖实际轨迹，不能为未执行路线捏造结果。 例如某路由总选过期记录，先更新记忆库可改变其收益；新库上线后路由也需要重新学习哪些路径有效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-coevo-mem-e947b4e5" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d970af4f29aa476e">为什么路由策略与记忆库更新会互相影响？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoevo-mem">CoEvo-Mem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>路由决定哪些记忆被使用，使用结果形成反馈更新路由与记忆价值；记忆内容和图关系变化又改变后续路由的收益。只优化一侧可能固化另一侧的缺陷，CoEvo-Mem 交替改进，但反馈只覆盖实际轨迹，不能为未执行路线捏造结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某路由总选过期记录，先更新记忆库可改变其收益；新库上线后路由也需要重新学习哪些路径有效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01739">原论文</a> · <a href="../../../../agent-research/2608.01739-coevo-mem/">实现解读</a> · <a href="#qa-d970af4f29aa476e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coevo-mem" data-paper-title="CoEvo-Mem" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoEvo-Mem Agent 论文未列机构 2026-08-03 只优化 query routing 或只更新 memory bank 会忽略二者反馈环。CoEvo-Mem 让冻结 LLM 生成 route-specific rewrite 和 prior，轻量 residual router 在线修正；任务结果更新路由，轨迹反馈更新 memory value 与 graph relation，并交替冻结一侧控制非平稳性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 route rewrite、残差路由与 router/memory bank 交替更新；检索键包含任务轴和工具签名，防止跨任务误复用。  检索—记忆共进化 Agent 记忆与技能：让经验可取回、可失效 路由器与记忆库为什么交替冻结，而不是每轮同时任意更新？ 路由改变会影响看到哪些记忆，记忆变化又会改变路由反馈，二者一起漂移难以判断改动来源。冻结一侧再更新另一侧控制非平稳性，轻量残差也保留基础 LLM 的路由先验；这并不保证收敛或提升，只让反馈关系更可学习和审计。 例如先固定记忆库比较两种检索路线，再固定路线调整低价值记忆；若两者同时大改，失败时很难定位是哪一侧造成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coevo-mem" data-paper-title="CoEvo-Mem" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoEvo-Mem Agent 论文未列机构 2026-08-03 只优化 query routing 或只更新 memory bank 会忽略二者反馈环。CoEvo-Mem 让冻结 LLM 生成 route-specific rewrite 和 prior，轻量 residual router 在线修正；任务结果更新路由，轨迹反馈更新 memory value 与 graph relation，并交替冻结一侧控制非平稳性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 route rewrite、残差路由与 router/memory bank 交替更新；检索键包含任务轴和工具签名，防止跨任务误复用。  检索—记忆共进化 Agent 记忆与技能：让经验可取回、可失效 交替冻结一侧与路由、记忆同时不断变化相比有什么作用？ 更新路由时固定记忆，更新记忆时固定路由，提供较稳定的条件，降低两侧同时变化带来的非平稳归因困难。它不消除所有噪声，也不是保证收敛到全局最优；冻结 LLM 的 prior 与可训练残差 router 还需分别标明更新范围。 例如验证路由新参数时保持同一库，可减少“成绩变化究竟来自新路由还是新记录”的混淆。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3b67e8e3d352fecb">交替冻结一侧与路由、记忆同时不断变化相比有什么作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoevo-mem">CoEvo-Mem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>更新路由时固定记忆，更新记忆时固定路由，提供较稳定的条件，降低两侧同时变化带来的非平稳归因困难。它不消除所有噪声，也不是保证收敛到全局最优；冻结 LLM 的 prior 与可训练残差 router 还需分别标明更新范围。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如验证路由新参数时保持同一库，可减少“成绩变化究竟来自新路由还是新记录”的混淆。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01739">原论文</a> · <a href="../../../../agent-research/2608.01739-coevo-mem/">实现解读</a> · <a href="#qa-3b67e8e3d352fecb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coevo-mem" data-paper-title="CoEvo-Mem" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="CoEvo-Mem Agent 论文未列机构 2026-08-03 只优化 query routing 或只更新 memory bank 会忽略二者反馈环。CoEvo-Mem 让冻结 LLM 生成 route-specific rewrite 和 prior，轻量 residual router 在线修正；任务结果更新路由，轨迹反馈更新 memory value 与 graph relation，并交替冻结一侧控制非平稳性。 Fidelity：核心机制复现。本页把原论文结论、本地机制验证和未复刻部分分开陈述。本地使用确定性公共 mini-suite 验证核心状态更新和公平预算，不等同于原论文大模型、多卡 RL、私有环境或完整 benchmark；本地相对变化不得与原文提升混写。实现 route rewrite、残差路由与 router/memory bank 交替更新；检索键包含任务轴和工具签名，防止跨任务误复用。  检索—记忆共进化 Agent 记忆与技能：让经验可取回、可失效 检索键为什么包含任务轴和工具签名，不能只按 query 文本复用？ 相似查询在不同任务或工具版本下可能要求不同路线，键包含任务轴与签名可避免跨契约错误复用。当前本地验证 rewrite、残差和交替更新控制流，公共 mini-suite 不等于论文多 benchmark，也不能从注册到 evolve 就推断所有完整学习过程已执行。 例如两个服务都有“查询订单”，返回 schema 不同，不能因为文字相同就复用带旧字段的记忆路由。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-11233bf81c6e4297">检索键为什么包含任务轴和工具签名，不能只按 query 文本复用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoevo-mem">CoEvo-Mem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似查询在不同任务或工具版本下可能要求不同路线，键包含任务轴与签名可避免跨契约错误复用。当前本地验证 rewrite、残差和交替更新控制流，公共 mini-suite 不等于论文多 benchmark，也不能从注册到 evolve 就推断所有完整学习过程已执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个服务都有“查询订单”，返回 schema 不同，不能因为文字相同就复用带旧字段的记忆路由。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.01739">原论文</a> · <a href="../../../../agent-research/2608.01739-coevo-mem/">实现解读</a> · <a href="#qa-11233bf81c6e4297">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skillrise" data-paper-title="SkillRise" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillRise Agent Zhejiang University 2026-07-29 标准 Agent RL 把任务视为独立 episode，外部 skill bank 又把抽取、检索和执行缠在一起。SkillRise 把相关但不同的任务排成由易到难的序列，让同一 policy 交替求解当前任务与整理一个直接传给下一任务的 skill document；求解阶段由当前结果监督，整理阶段由折扣后的下游任务结果监督。 本地验证状态演化与 credit 分离，不训练 Qwen3，也不运行 ALFWorld/WebShop/ScienceWorld；因此不能把 mini-suite 的 100% success 与论文 Pass@k 横向比较。PlanBench mini 按 task axis 组织相关任务；每个 episode 交替执行 solve 和 curate，成功轨迹更新 skill document，并单独记录跨任务复用与下游 credit。  跨任务技能进化 Agent 记忆与技能：让经验可取回、可失效 同一 policy 为什么交替求解当前任务和整理 skill document？ 求解产生执行经验，整理把可迁移内容直接传给下一任务，让跨任务学习成为策略行为。相关任务由易到难组织，文档需要帮助后续而不是只解释当前成功；这不同于把每个 episode 完全独立训练，也不意味着所有经验都应保留。 例如先完成简单文件查找后，整理路径定位和验证方法，再在更复杂修改任务复用，而不是原样搬运上一题答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-skillrise-fa529938" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d86d7ab30cfa12bb">同一 policy 为什么交替求解当前任务和整理 skill document？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askillrise">SkillRise</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>求解产生执行经验，整理把可迁移内容直接传给下一任务，让跨任务学习成为策略行为。相关任务由易到难组织，文档需要帮助后续而不是只解释当前成功；这不同于把每个 episode 完全独立训练，也不意味着所有经验都应保留。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先完成简单文件查找后，整理路径定位和验证方法，再在更复杂修改任务复用，而不是原样搬运上一题答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26784">原论文</a> · <a href="../../../../agent-research/2607.26784-skillrise/">实现解读</a> · <a href="#qa-d86d7ab30cfa12bb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skillrise" data-paper-title="SkillRise" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillRise Agent Zhejiang University 2026-07-29 标准 Agent RL 把任务视为独立 episode，外部 skill bank 又把抽取、检索和执行缠在一起。SkillRise 把相关但不同的任务排成由易到难的序列，让同一 policy 交替求解当前任务与整理一个直接传给下一任务的 skill document；求解阶段由当前结果监督，整理阶段由折扣后的下游任务结果监督。 本地验证状态演化与 credit 分离，不训练 Qwen3，也不运行 ALFWorld/WebShop/ScienceWorld；因此不能把 mini-suite 的 100% success 与论文 Pass@k 横向比较。PlanBench mini 按 task axis 组织相关任务；每个 episode 交替执行 solve 和 curate，成功轨迹更新 skill document，并单独记录跨任务复用与下游 credit。  跨任务技能进化 Agent 记忆与技能：让经验可取回、可失效 为什么整理技能文档的奖励来自后续任务，而不是当前任务成功？ 当前成功主要评价求解过程，不能说明留下的技能是否帮助别人或未来自己。把相关任务串成序列，整理阶段用折扣下游回报监督，促使文档保留可迁移经验；两个 phase 的 advantage 必须施加到各自生成 token，不能把信用无差别广播。 例如这题靠偶然猜中答案，但文档记录了可复用的测试步骤；只有之后任务因此更容易完成，才能体现整理的价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skillrise" data-paper-title="SkillRise" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillRise Agent Zhejiang University 2026-07-29 标准 Agent RL 把任务视为独立 episode，外部 skill bank 又把抽取、检索和执行缠在一起。SkillRise 把相关但不同的任务排成由易到难的序列，让同一 policy 交替求解当前任务与整理一个直接传给下一任务的 skill document；求解阶段由当前结果监督，整理阶段由折扣后的下游任务结果监督。 本地验证状态演化与 credit 分离，不训练 Qwen3，也不运行 ALFWorld/WebShop/ScienceWorld；因此不能把 mini-suite 的 100% success 与论文 Pass@k 横向比较。PlanBench mini 按 task axis 组织相关任务；每个 episode 交替执行 solve 和 curate，成功轨迹更新 skill document，并单独记录跨任务复用与下游 credit。  跨任务技能进化 Agent 记忆与技能：让经验可取回、可失效 solve reward 与 curate reward 为什么不能共用当前任务结果？ solve 由当前结果监督，curate 的价值在下游任务中体现，应使用折扣后的后续回报。若整理也只看当前成功，会奖励对未来无用的漂亮总结；两阶段共享 policy，但优势只施加到各自生成 token，避免信用错配。 例如当前题已完成，写一份含当前答案的文档未必能帮下一题；后续任务表现才提供整理质量的反馈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e88f05c7ec0f5b77">solve reward 与 curate reward 为什么不能共用当前任务结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askillrise">SkillRise</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>solve 由当前结果监督，curate 的价值在下游任务中体现，应使用折扣后的后续回报。若整理也只看当前成功，会奖励对未来无用的漂亮总结；两阶段共享 policy，但优势只施加到各自生成 token，避免信用错配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如当前题已完成，写一份含当前答案的文档未必能帮下一题；后续任务表现才提供整理质量的反馈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26784">原论文</a> · <a href="../../../../agent-research/2607.26784-skillrise/">实现解读</a> · <a href="#qa-e88f05c7ec0f5b77">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:skillrise" data-paper-title="SkillRise" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SkillRise Agent Zhejiang University 2026-07-29 标准 Agent RL 把任务视为独立 episode，外部 skill bank 又把抽取、检索和执行缠在一起。SkillRise 把相关但不同的任务排成由易到难的序列，让同一 policy 交替求解当前任务与整理一个直接传给下一任务的 skill document；求解阶段由当前结果监督，整理阶段由折扣后的下游任务结果监督。 本地验证状态演化与 credit 分离，不训练 Qwen3，也不运行 ALFWorld/WebShop/ScienceWorld；因此不能把 mini-suite 的 100% success 与论文 Pass@k 横向比较。PlanBench mini 按 task axis 组织相关任务；每个 episode 交替执行 solve 和 curate，成功轨迹更新 skill document，并单独记录跨任务复用与下游 credit。  跨任务技能进化 Agent 记忆与技能：让经验可取回、可失效 本地文档更新和 downstream credit 计数是否表示 Qwen3 已接受 RL 训练？ 没有。本地在受控 PlanBench 检查状态演化、技能传递与 phase 信用分离，没有训练 Qwen3 或运行原文三环境。文档更新次数说明操作发生，不是策略参数学习证据，mini-suite 满分不能与论文 Pass@k 横比。 例如一百二十次文档写入可以由确定性规则完成；若没有真实梯度更新，就不能称为完成论文共享策略训练。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6488d5dae7432edc">本地文档更新和 downstream credit 计数是否表示 Qwen3 已接受 RL 训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Askillrise">SkillRise</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地在受控 PlanBench 检查状态演化、技能传递与 phase 信用分离，没有训练 Qwen3 或运行原文三环境。文档更新次数说明操作发生，不是策略参数学习证据，mini-suite 满分不能与论文 Pass@k 横比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一百二十次文档写入可以由确定性规则完成；若没有真实梯度更新，就不能称为完成论文共享策略训练。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26784">原论文</a> · <a href="../../../../agent-research/2607.26784-skillrise/">实现解读</a> · <a href="#qa-6488d5dae7432edc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hiskill" data-paper-title="HiSkill" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HiSkill Agent Beijing University of Posts and Telecommunications 2026-07-28 用高层 skill、可执行 AtomicOp 和多类有向边组织经验，推理时只检索任务相关子图来落地动作。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。图节点来自受控轨迹，不由在线 LLM 抽取；主要验证层次和关系是否改善复用。PlanBench mini-suite 构建高层 skill/AtomicOp 节点及 decomposition、transition、recovery 边，记录子图复用。  Hierarchical skill memory Agent 记忆与技能：让经验可取回、可失效 高层 skill 与 AtomicOp 为什么需要不同类型节点？ 高层技能表达目标和可复用子程序，AtomicOp 对应可落地动作，两者通过分解关系衔接。若把所有节点都当同一种文本片段，难区分抽象计划与可立即执行操作；落地仍需当前状态和工具合同，不能直接执行高层名称。 例如“整理订单”是高层技能，查询订单、验证状态、写出结果是原子操作，需要分解后才能形成合法工具调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-hiskill-6a9652b8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6f93afb88c05bebc">高层 skill 与 AtomicOp 为什么需要不同类型节点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahiskill">HiSkill</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高层技能表达目标和可复用子程序，AtomicOp 对应可落地动作，两者通过分解关系衔接。若把所有节点都当同一种文本片段，难区分抽象计划与可立即执行操作；落地仍需当前状态和工具合同，不能直接执行高层名称。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“整理订单”是高层技能，查询订单、验证状态、写出结果是原子操作，需要分解后才能形成合法工具调用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25853">原论文</a> · <a href="../../../../agent-research/2607.25853-hiskill/">实现解读</a> · <a href="#qa-6f93afb88c05bebc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hiskill" data-paper-title="HiSkill" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HiSkill Agent Beijing University of Posts and Telecommunications 2026-07-28 用高层 skill、可执行 AtomicOp 和多类有向边组织经验，推理时只检索任务相关子图来落地动作。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。图节点来自受控轨迹，不由在线 LLM 抽取；主要验证层次和关系是否改善复用。PlanBench mini-suite 构建高层 skill/AtomicOp 节点及 decomposition、transition、recovery 边，记录子图复用。  Hierarchical skill memory Agent 记忆与技能：让经验可取回、可失效 技能图为什么要区分分解边、时间边和恢复边？ 这些边表达不同执行语义：分解说明高层目标由哪些 AtomicOp 落地，时间边约束先后，恢复边提供失败后的可用路径。混成一种相似度关系会丢失可执行条件；检索相关子图后还需根据当前状态 grounding，不能把找到技能名就算完成动作。 例如“上传文件”先分解为选文件与提交，失败后沿恢复边刷新登录；把恢复步骤当固定前置流程会引入无谓操作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hiskill" data-paper-title="HiSkill" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HiSkill Agent Beijing University of Posts and Telecommunications 2026-07-28 用高层 skill、可执行 AtomicOp 和多类有向边组织经验，推理时只检索任务相关子图来落地动作。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。图节点来自受控轨迹，不由在线 LLM 抽取；主要验证层次和关系是否改善复用。PlanBench mini-suite 构建高层 skill/AtomicOp 节点及 decomposition、transition、recovery 边，记录子图复用。  Hierarchical skill memory Agent 记忆与技能：让经验可取回、可失效 decomposition、temporal 与 recovery 边为什么不能合并成普通相关边？ 分解边说明组成，时间边说明先后，恢复边说明失败后的替代或补救，语义不同会改变执行策略。普通相似关系无法表达何时能调用和出错后怎么办；仅图连通也不能证明动作可执行，需要按边类型解释当前子图。 例如“先验证再删除”的时间边不能误读为任意顺序，“删除失败后查权限”的恢复边也不应在正常流程总执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-3a39ef5716fcd49d">decomposition、temporal 与 recovery 边为什么不能合并成普通相关边？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahiskill">HiSkill</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分解边说明组成，时间边说明先后，恢复边说明失败后的替代或补救，语义不同会改变执行策略。普通相似关系无法表达何时能调用和出错后怎么办；仅图连通也不能证明动作可执行，需要按边类型解释当前子图。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“先验证再删除”的时间边不能误读为任意顺序，“删除失败后查权限”的恢复边也不应在正常流程总执行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25853">原论文</a> · <a href="../../../../agent-research/2607.25853-hiskill/">实现解读</a> · <a href="#qa-3a39ef5716fcd49d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hiskill" data-paper-title="HiSkill" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="HiSkill Agent Beijing University of Posts and Telecommunications 2026-07-28 用高层 skill、可执行 AtomicOp 和多类有向边组织经验，推理时只检索任务相关子图来落地动作。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。图节点来自受控轨迹，不由在线 LLM 抽取；主要验证层次和关系是否改善复用。PlanBench mini-suite 构建高层 skill/AtomicOp 节点及 decomposition、transition、recovery 边，记录子图复用。  Hierarchical skill memory Agent 记忆与技能：让经验可取回、可失效 本地受控轨迹建图可以证明在线 LLM 已学会抽取技能关系吗？ 不能。本地图节点和关系来自受控轨迹，验证层次、子图检索与复用，没有在线 LLM 经验抽取。AtomicOp reuse 数量可说明操作实际复用，但不代表开放环境语义关系被正确发现，也不能直接外推推理 token 节省。 例如预先指定恢复边后系统能走该边，只证明图执行器；尚未测试模型能从未知失败日志自行发现这条恢复关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f9bf03107aa70202">本地受控轨迹建图可以证明在线 LLM 已学会抽取技能关系吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahiskill">HiSkill</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beijing University of Posts and Telecommunications</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地图节点和关系来自受控轨迹，验证层次、子图检索与复用，没有在线 LLM 经验抽取。AtomicOp reuse 数量可说明操作实际复用，但不代表开放环境语义关系被正确发现，也不能直接外推推理 token 节省。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预先指定恢复边后系统能走该边，只证明图执行器；尚未测试模型能从未知失败日志自行发现这条恢复关系。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25853">原论文</a> · <a href="../../../../agent-research/2607.25853-hiskill/">实现解读</a> · <a href="#qa-f9bf03107aa70202">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:unimem" data-paper-title="UniMem" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UniMem Agent CASIA 2026-07-28 新颖任务先进入 episodic buffer；反复出现且可靠的执行模式再被自路由控制器固化到可扩展 parametric memory。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。参数记忆是结构化模式表，不是扩展 LLM 权重块；验证稳定性/可塑性路由逻辑。EvoMem mini-suite 实现 episodic route、复现频次阈值、parametric route 和 consolidation 统计。  Continual agent memory Agent 记忆与技能：让经验可取回、可失效 新任务先进入 episodic buffer，重复模式再固化有什么作用？ 情景记忆快速保存新经验，反复出现且可靠的模式再进入参数记忆，试图平衡可塑性与稳定性。过早固化可能把偶然或错误经历变成长期偏置，始终只存情景又可能反复检索；自路由决定何时利用哪类记忆。 例如第一次遇到某工具报错先存情景，多次确认同一恢复步骤有效后再考虑固化，而不是一次失败就改写长期规则。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-unimem-c304c78e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ceb2875337a2818b">新任务先进入 episodic buffer，重复模式再固化有什么作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aunimem">UniMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · CASIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>情景记忆快速保存新经验，反复出现且可靠的模式再进入参数记忆，试图平衡可塑性与稳定性。过早固化可能把偶然或错误经历变成长期偏置，始终只存情景又可能反复检索；自路由决定何时利用哪类记忆。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第一次遇到某工具报错先存情景，多次确认同一恢复步骤有效后再考虑固化，而不是一次失败就改写长期规则。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26017">原论文</a> · <a href="../../../../agent-research/2607.26017-unimem/">实现解读</a> · <a href="#qa-ceb2875337a2818b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:unimem" data-paper-title="UniMem" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UniMem Agent CASIA 2026-07-28 新颖任务先进入 episodic buffer；反复出现且可靠的执行模式再被自路由控制器固化到可扩展 parametric memory。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。参数记忆是结构化模式表，不是扩展 LLM 权重块；验证稳定性/可塑性路由逻辑。EvoMem mini-suite 实现 episodic route、复现频次阈值、parametric route 和 consolidation 统计。  Continual agent memory Agent 记忆与技能：让经验可取回、可失效 为什么新任务先放 episodic buffer，反复可靠出现后才固化到参数记忆？ 一次事件可能是噪声或特例，先留情节记录保留上下文，重复且可靠的模式再适合形成稳定参数化知识。自路由决定两种记忆如何使用，减少把偶然经验过早写进长期行为的风险；出现次数也需配合可靠性，不能把重复错误当成可固化规律。 例如首次遇到临时服务故障先记为事件，多次确认同一配置约束后再沉淀为通用处理模式，而不立即修改所有任务策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:unimem" data-paper-title="UniMem" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UniMem Agent CASIA 2026-07-28 新颖任务先进入 episodic buffer；反复出现且可靠的执行模式再被自路由控制器固化到可扩展 parametric memory。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。参数记忆是结构化模式表，不是扩展 LLM 权重块；验证稳定性/可塑性路由逻辑。EvoMem mini-suite 实现 episodic route、复现频次阈值、parametric route 和 consolidation 统计。  Continual agent memory Agent 记忆与技能：让经验可取回、可失效 情景检索与参数记忆在更新和调用上有何取舍？ 情景条目易追加、核查和删除，但读取占上下文与检索成本；参数记忆将重复模式内化，调用更直接，却更难精确撤销单条事实。研究强调互补路线，不能把固化等同于简单复制到另一张表，也不能忽略错误积累风险。 例如临时会议日期适合可追溯情景记录，稳定的工具使用模式才可能适合固化，二者更新频率不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1d5877beb700c4b8">情景检索与参数记忆在更新和调用上有何取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aunimem">UniMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · CASIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>情景条目易追加、核查和删除，但读取占上下文与检索成本；参数记忆将重复模式内化，调用更直接，却更难精确撤销单条事实。研究强调互补路线，不能把固化等同于简单复制到另一张表，也不能忽略错误积累风险。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如临时会议日期适合可追溯情景记录，稳定的工具使用模式才可能适合固化，二者更新频率不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26017">原论文</a> · <a href="../../../../agent-research/2607.26017-unimem/">实现解读</a> · <a href="#qa-1d5877beb700c4b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:unimem" data-paper-title="UniMem" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="UniMem Agent CASIA 2026-07-28 新颖任务先进入 episodic buffer；反复出现且可靠的执行模式再被自路由控制器固化到可扩展 parametric memory。 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性 mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。参数记忆是结构化模式表，不是扩展 LLM 权重块；验证稳定性/可塑性路由逻辑。EvoMem mini-suite 实现 episodic route、复现频次阈值、parametric route 和 consolidation 统计。  Continual agent memory Agent 记忆与技能：让经验可取回、可失效 本地 parametric route 是否实际扩展了 LLM 权重块？ 没有。本地参数记忆是结构化模式表，用于验证频次阈值、情景到固化的路由逻辑和统计，不是训练或扩展语言模型参数。不能用 consolidation 计数证明权重内化，也不能把确定性 suite 的成功率当成流式大模型能力。 例如模式出现三次后表里新增一条规则，只说明状态迁移；若 LLM 权重未更新，就不应写成参数学习已发生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b04dee9b415912bf">本地 parametric route 是否实际扩展了 LLM 权重块？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aunimem">UniMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · CASIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地参数记忆是结构化模式表，用于验证频次阈值、情景到固化的路由逻辑和统计，不是训练或扩展语言模型参数。不能用 consolidation 计数证明权重内化，也不能把确定性 suite 的成功率当成流式大模型能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模式出现三次后表里新增一条规则，只说明状态迁移；若 LLM 权重未更新，就不应写成参数学习已发生。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26017">原论文</a> · <a href="../../../../agent-research/2607.26017-unimem/">实现解读</a> · <a href="#qa-b04dee9b415912bf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memcon" data-paper-title="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents Agent 未明确标注（正文 HTML 未显示一作机构映射） 2026-07-15 MemCon 将记忆使用拆成一个独立的在线控制问题：根据任务进展、重复动作、记忆规模和已有成功计划，选择检索深度、计划注入、替换查询或记忆维护。控制器用轻量表格 UCB 探索，并从任务结束时的二元反馈及效率奖励学习，不为了选择记忆操作额外调用 LLM。 原六 benchmark、多框架和多 LLM 的端到端比较会产生大量长轨迹推理，成本过高，暂不复现；L1 机制诊断。本轮完成：CPU 核心控制器与真实记忆操作；L1 机制诊断。没有调用 LLM，没有读取任务标准答案或标准计划，不是原论文六个 benchmark 的能力复现，也不作为 evolve 晋级证据。已实现：附录 C 状态/动作、正文 UCB、warm-start、终末奖励、逆序信用、真实 backend 操作、持久化/恢复。本轮核心算法只使用 Python 标准库，CPU 上运行，不下载权重或数据，不增加付费调用。  主动记忆 在线上下文 bandit 记忆维护与计划复用 Agent 记忆与技能：让经验可取回、可失效 为什么 MemCon 把“是否用记忆”也当成控制动作？ 记忆检索、注入计划、改查询和维护都有成本，某些简单任务直接行动更便宜。MemCon 根据进展、重复、记忆规模等离散状态选择操作，任务结束后用成功与效率反馈学习，因此记忆不是每轮必须开启的固定外挂。 例如任务已明确下一工具且状态简单时，可选不检索；反复失败、已有相关成功计划时，再选择注入或更深检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memcon-717a2e37" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7c3c0d162719c7ac">为什么 MemCon 把“是否用记忆”也当成控制动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemcon">Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 未明确标注（正文 HTML 未显示一作机构映射）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>记忆检索、注入计划、改查询和维护都有成本，某些简单任务直接行动更便宜。MemCon 根据进展、重复、记忆规模等离散状态选择操作，任务结束后用成功与效率反馈学习，因此记忆不是每轮必须开启的固定外挂。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如任务已明确下一工具且状态简单时，可选不检索；反复失败、已有相关成功计划时，再选择注入或更深检索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13591">原论文</a> · <a href="../../../../agent-research/2607.13591-memcon/">实现解读</a> · <a href="#qa-7c3c0d162719c7ac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memcon" data-paper-title="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents Agent 未明确标注（正文 HTML 未显示一作机构映射） 2026-07-15 MemCon 将记忆使用拆成一个独立的在线控制问题：根据任务进展、重复动作、记忆规模和已有成功计划，选择检索深度、计划注入、替换查询或记忆维护。控制器用轻量表格 UCB 探索，并从任务结束时的二元反馈及效率奖励学习，不为了选择记忆操作额外调用 LLM。 原六 benchmark、多框架和多 LLM 的端到端比较会产生大量长轨迹推理，成本过高，暂不复现；L1 机制诊断。本轮完成：CPU 核心控制器与真实记忆操作；L1 机制诊断。没有调用 LLM，没有读取任务标准答案或标准计划，不是原论文六个 benchmark 的能力复现，也不作为 evolve 晋级证据。已实现：附录 C 状态/动作、正文 UCB、warm-start、终末奖励、逆序信用、真实 backend 操作、持久化/恢复。本轮核心算法只使用 Python 标准库，CPU 上运行，不下载权重或数据，不增加付费调用。  主动记忆 在线上下文 bandit 记忆维护与计划复用 Agent 记忆与技能：让经验可取回、可失效 为什么记忆控制器的 UCB 必须按当前离散状态计数，而非只用全局动作频率？ 某操作在早期探索有用，不代表任务后期或记忆拥塞时也有用。状态局部的访问数与价值让控制器分别学习这些条件下的取舍，未访问动作先探索，再从终局与效率反馈更新；不额外调用 LLM 只指控制选择，实际检索和执行仍可能有成本。 例如“深检索”在刚开始有价值，临近结束却可能拖延；两个状态应各自累计尝试，不能用一份全局成功率混在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memcon" data-paper-title="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents Agent 未明确标注（正文 HTML 未显示一作机构映射） 2026-07-15 MemCon 将记忆使用拆成一个独立的在线控制问题：根据任务进展、重复动作、记忆规模和已有成功计划，选择检索深度、计划注入、替换查询或记忆维护。控制器用轻量表格 UCB 探索，并从任务结束时的二元反馈及效率奖励学习，不为了选择记忆操作额外调用 LLM。 原六 benchmark、多框架和多 LLM 的端到端比较会产生大量长轨迹推理，成本过高，暂不复现；L1 机制诊断。本轮完成：CPU 核心控制器与真实记忆操作；L1 机制诊断。没有调用 LLM，没有读取任务标准答案或标准计划，不是原论文六个 benchmark 的能力复现，也不作为 evolve 晋级证据。已实现：附录 C 状态/动作、正文 UCB、warm-start、终末奖励、逆序信用、真实 backend 操作、持久化/恢复。本轮核心算法只使用 Python 标准库，CPU 上运行，不下载权重或数据，不增加付费调用。  主动记忆 在线上下文 bandit 记忆维护与计划复用 Agent 记忆与技能：让经验可取回、可失效 表格 UCB 控制与每轮让 LLM 决定记忆策略有什么取舍？ 表格控制不为调度额外调用语言模型，状态和动作较可解释，但依赖离散特征覆盖，难以表达任意语义情境。LLM 控制更灵活却消耗调用；这里 UCB 是状态局部探索，环境与记忆持续变化时也无无条件收敛保证。 例如重复动作标志可立即切换更深检索，但两种语义完全不同、离散状态相同的任务可能被表格视为同一情况。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d2c33c0e1bbf4b0c">表格 UCB 控制与每轮让 LLM 决定记忆策略有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemcon">Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 未明确标注（正文 HTML 未显示一作机构映射）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>表格控制不为调度额外调用语言模型，状态和动作较可解释，但依赖离散特征覆盖，难以表达任意语义情境。LLM 控制更灵活却消耗调用；这里 UCB 是状态局部探索，环境与记忆持续变化时也无无条件收敛保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如重复动作标志可立即切换更深检索，但两种语义完全不同、离散状态相同的任务可能被表格视为同一情况。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13591">原论文</a> · <a href="../../../../agent-research/2607.13591-memcon/">实现解读</a> · <a href="#qa-d2c33c0e1bbf4b0c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memcon" data-paper-title="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents Agent 未明确标注（正文 HTML 未显示一作机构映射） 2026-07-15 MemCon 将记忆使用拆成一个独立的在线控制问题：根据任务进展、重复动作、记忆规模和已有成功计划，选择检索深度、计划注入、替换查询或记忆维护。控制器用轻量表格 UCB 探索，并从任务结束时的二元反馈及效率奖励学习，不为了选择记忆操作额外调用 LLM。 原六 benchmark、多框架和多 LLM 的端到端比较会产生大量长轨迹推理，成本过高，暂不复现；L1 机制诊断。本轮完成：CPU 核心控制器与真实记忆操作；L1 机制诊断。没有调用 LLM，没有读取任务标准答案或标准计划，不是原论文六个 benchmark 的能力复现，也不作为 evolve 晋级证据。已实现：附录 C 状态/动作、正文 UCB、warm-start、终末奖励、逆序信用、真实 backend 操作、持久化/恢复。本轮核心算法只使用 Python 标准库，CPU 上运行，不下载权重或数据，不增加付费调用。  主动记忆 在线上下文 bandit 记忆维护与计划复用 Agent 记忆与技能：让经验可取回、可失效 MemCon 的 Q 更新能按 sample-mean UCB 或 TD bootstrap 实现吗？ 不能。本地按 v3 正文用状态局部计数，终末成功和效率奖励按剩余距离折扣，逆序逐次更新同一状态动作；不使用未来 Q bootstrap。未访问动作优先，用初始 Q 打平，本地与可变上游 main 的计数规则差异已明确记录。 例如一个动作在同 episode 出现两次，要按逆序分别接收折扣终末信用，不能只把总奖励加一次后除访问数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-67d5abfc2cadf284">MemCon 的 Q 更新能按 sample-mean UCB 或 TD bootstrap 实现吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemcon">Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 未明确标注（正文 HTML 未显示一作机构映射）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地按 v3 正文用状态局部计数，终末成功和效率奖励按剩余距离折扣，逆序逐次更新同一状态动作；不使用未来 Q bootstrap。未访问动作优先，用初始 Q 打平，本地与可变上游 main 的计数规则差异已明确记录。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个动作在同 episode 出现两次，要按逆序分别接收折扣终末信用，不能只把总奖励加一次后除访问数。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.13591">原论文</a> · <a href="../../../../agent-research/2607.13591-memcon/">实现解读</a> · <a href="#qa-67d5abfc2cadf284">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memento-skills" data-paper-title="Memento-Skills" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memento-Skills Agent Memento Team 2026-03-19 从执行日志反思出结构化技能说明，按任务检索并写回版本化技能，而不是原样堆叠轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 0.0500，average cost 0.2800；方法特有操作有非零 telemetry。  技能设计 Agent 记忆与技能：让经验可取回、可失效 从日志生成结构化技能为什么不等于保存整条轨迹？ 技能提炼可复用的前提、步骤与经验，轨迹包含一次具体执行的偶然细节；按任务检索并版本化合并，可以让后续任务读取方法而非重放旧输入。抽象也可能丢失必要条件，因此结构清晰不自动证明跨任务有效。 例如旧日志里的文件名和时间可去掉，但“先检查 schema 再转换”应保留成通用步骤，不能照搬上次输出当技能。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memento-skills-c4d49bbe" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e28f108866db2db6">从日志生成结构化技能为什么不等于保存整条轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemento-skills">Memento-Skills</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Memento Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>技能提炼可复用的前提、步骤与经验，轨迹包含一次具体执行的偶然细节；按任务检索并版本化合并，可以让后续任务读取方法而非重放旧输入。抽象也可能丢失必要条件，因此结构清晰不自动证明跨任务有效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧日志里的文件名和时间可去掉，但“先检查 schema 再转换”应保留成通用步骤，不能照搬上次输出当技能。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.18743">原论文</a> · <a href="../../../../agent-research/2603.18743-memento-skills/">实现解读</a> · <a href="#qa-e28f108866db2db6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memento-skills" data-paper-title="Memento-Skills" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memento-Skills Agent Memento Team 2026-03-19 从执行日志反思出结构化技能说明，按任务检索并写回版本化技能，而不是原样堆叠轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 0.0500，average cost 0.2800；方法特有操作有非零 telemetry。  技能设计 Agent 记忆与技能：让经验可取回、可失效 版本化技能为什么比把执行日志原样追加到上下文更可复用？ 日志记录一次具体经历，结构化技能抽出适用条件与步骤，检索时更容易匹配新任务。版本合并还记录后续修正，避免同一技能出现互相矛盾的旧说明；抽象需要保留失败条件与来源，不能因为语言更简洁就假定已成为可靠通用程序。 例如一次部署日志含临时目录和重试输出，技能版保留检查依赖与回滚条件，之后升级版本修正过期参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memento-skills" data-paper-title="Memento-Skills" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memento-Skills Agent Memento Team 2026-03-19 从执行日志反思出结构化技能说明，按任务检索并写回版本化技能，而不是原样堆叠轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 0.0500，average cost 0.2800；方法特有操作有非零 telemetry。  技能设计 Agent 记忆与技能：让经验可取回、可失效 版本化 Merge 与每次追加新技能有什么不同？ Merge 将新反馈整合进相关既有技能，记录变化而非无限堆近重复条目；追加更简单却可能保留互相矛盾版本。合并需要判断适用条件与回归，不能因同主题就覆盖所有差异，也不能把一次新成功当全局升级依据。 例如同一导出技能新增分页限制，应更新相关版本；若新情况只适用特定服务，要保留条件而非改成所有服务都分页。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b9e7b86356628ade">版本化 Merge 与每次追加新技能有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemento-skills">Memento-Skills</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Memento Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Merge 将新反馈整合进相关既有技能，记录变化而非无限堆近重复条目；追加更简单却可能保留互相矛盾版本。合并需要判断适用条件与回归，不能因同主题就覆盖所有差异，也不能把一次新成功当全局升级依据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一导出技能新增分页限制，应更新相关版本；若新情况只适用特定服务，要保留条件而非改成所有服务都分页。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.18743">原论文</a> · <a href="../../../../agent-research/2603.18743-memento-skills/">实现解读</a> · <a href="#qa-b9e7b86356628ade">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memento-skills" data-paper-title="Memento-Skills" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Memento-Skills Agent Memento Team 2026-03-19 从执行日志反思出结构化技能说明，按任务检索并写回版本化技能，而不是原样堆叠轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 0.0500，average cost 0.2800；方法特有操作有非零 telemetry。  技能设计 Agent 记忆与技能：让经验可取回、可失效 本地低 joint success 与非零技能 telemetry 可以说明什么？ 说明当前机制运行并且存在明显未成功任务，不能只挑创建或复用计数宣传改进。本地只验证状态更新和公平预算，没有原论文大模型、真实网页或完整 benchmark；负结果应与过程证据一起保留，而不是改称完整方法成功。 例如日志显示技能被检索十次但任务仍失败，计数证明调用发生，不证明技能内容正确或对执行有帮助。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-84e7bd0f8016135d">本地低 joint success 与非零技能 telemetry 可以说明什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemento-skills">Memento-Skills</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Memento Team</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>说明当前机制运行并且存在明显未成功任务，不能只挑创建或复用计数宣传改进。本地只验证状态更新和公平预算，没有原论文大模型、真实网页或完整 benchmark；负结果应与过程证据一起保留，而不是改称完整方法成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如日志显示技能被检索十次但任务仍失败，计数证明调用发生，不证明技能内容正确或对执行有帮助。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.18743">原论文</a> · <a href="../../../../agent-research/2603.18743-memento-skills/">实现解读</a> · <a href="#qa-84e7bd0f8016135d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:u-mem" data-paper-title="U-Mem" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="U-Mem Agent National University of Singapore 2026-02-25 传统 Agent 记忆通常被动写入和检索，缺少“当前知识不够时主动去哪里找”的决策。U-Mem 将获取过程建模为成本递增的级联：先尝试 self/teacher，再做工具研究，最后请求 expert；检索结合语义相似度与 Thompson sampling，并在写回前验证和整理记忆。 保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；当前 mini-suite 不包含论文使用的真实 LLM、HotpotQA 或 AIME 推理。mini-suite 的知识源、专家和验证器都是确定性的，不包含真实搜索 API、模型幻觉或 token 成本。因此这里验证的是主动获取状态机与成本记账，不是 HotpotQA/AIME 分数复刻。evomem-mini 覆盖 episode 内/跨 episode × knowledge/execution 四象限。  主动记忆 Agent 记忆与技能：让经验可取回、可失效 U-Mem 为什么把知识获取组织成成本递增级联？ 当前知识不足时先尝试自身或教师，再做工具研究，最后请求专家，避免一开始就付最高成本。每层应根据额外收益与代价决定升级，获取后还需验证整理才写回；级联不是永远保证低成本足够，也不意味着专家输出无需检查。 例如先查已存公式，仍无法确认边界条件才检索资料，再在确有必要时请求专家，而不是每道简单题都升级。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-u-mem-1e639ec3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-38a7caab07361558">U-Mem 为什么把知识获取组织成成本递增级联？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Au-mem">U-Mem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前知识不足时先尝试自身或教师，再做工具研究，最后请求专家，避免一开始就付最高成本。每层应根据额外收益与代价决定升级，获取后还需验证整理才写回；级联不是永远保证低成本足够，也不意味着专家输出无需检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先查已存公式，仍无法确认边界条件才检索资料，再在确有必要时请求专家，而不是每道简单题都升级。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与算法；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22406">原论文</a> · <a href="../../../../agent-research/2602.22406-u-mem/">实现解读</a> · <a href="#qa-38a7caab07361558">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:u-mem" data-paper-title="U-Mem" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="U-Mem Agent National University of Singapore 2026-02-25 传统 Agent 记忆通常被动写入和检索，缺少“当前知识不够时主动去哪里找”的决策。U-Mem 将获取过程建模为成本递增的级联：先尝试 self/teacher，再做工具研究，最后请求 expert；检索结合语义相似度与 Thompson sampling，并在写回前验证和整理记忆。 保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；当前 mini-suite 不包含论文使用的真实 LLM、HotpotQA 或 AIME 推理。mini-suite 的知识源、专家和验证器都是确定性的，不包含真实搜索 API、模型幻觉或 token 成本。因此这里验证的是主动获取状态机与成本记账，不是 HotpotQA/AIME 分数复刻。evomem-mini 覆盖 episode 内/跨 episode × knowledge/execution 四象限。  主动记忆 Agent 记忆与技能：让经验可取回、可失效 为什么获取知识按 self/teacher、工具研究、expert 逐级升级，而非一开始总找最强专家？ 不同级别的获取成本不同，先尝试便宜且可能足够的路径，把高成本援助留给仍不确定的问题。Thompson sampling 让历史效用与不确定性共同影响检索，写回前再验证；级联不是保证低价来源总正确，而是收益与成本的顺序决策。 例如常见配置问题先查已有记忆，找不到再读文档，仍有歧义才请专家；无需每次都支付最高级帮助成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:u-mem" data-paper-title="U-Mem" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="U-Mem Agent National University of Singapore 2026-02-25 传统 Agent 记忆通常被动写入和检索，缺少“当前知识不够时主动去哪里找”的决策。U-Mem 将获取过程建模为成本递增的级联：先尝试 self/teacher，再做工具研究，最后请求 expert；检索结合语义相似度与 Thompson sampling，并在写回前验证和整理记忆。 保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；当前 mini-suite 不包含论文使用的真实 LLM、HotpotQA 或 AIME 推理。mini-suite 的知识源、专家和验证器都是确定性的，不包含真实搜索 API、模型幻觉或 token 成本。因此这里验证的是主动获取状态机与成本记账，不是 HotpotQA/AIME 分数复刻。evomem-mini 覆盖 episode 内/跨 episode × knowledge/execution 四象限。  主动记忆 Agent 记忆与技能：让经验可取回、可失效 语义相似度加 Thompson sampling 与只按相似度取记忆有何不同？ 相似度偏向内容相关，Beta 后验采样给不确定但可能有用的记忆探索机会，成功失败反馈再更新。探索不是随机加入无关知识，而是在相关性与效用不确定性之间权衡；后验也依赖真实反馈，不能用模型自信代替验证。 例如两条同样相关记录，一条验证很多次、另一条较新，采样可偶尔检验新记录，而非永远只使用旧的最高分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ecb60d81ada577f1">语义相似度加 Thompson sampling 与只按相似度取记忆有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Au-mem">U-Mem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相似度偏向内容相关，Beta 后验采样给不确定但可能有用的记忆探索机会，成功失败反馈再更新。探索不是随机加入无关知识，而是在相关性与效用不确定性之间权衡；后验也依赖真实反馈，不能用模型自信代替验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条同样相关记录，一条验证很多次、另一条较新，采样可偶尔检验新记录，而非永远只使用旧的最高分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与算法；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22406">原论文</a> · <a href="../../../../agent-research/2602.22406-u-mem/">实现解读</a> · <a href="#qa-ecb60d81ada577f1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:u-mem" data-paper-title="U-Mem" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="U-Mem Agent National University of Singapore 2026-02-25 传统 Agent 记忆通常被动写入和检索，缺少“当前知识不够时主动去哪里找”的决策。U-Mem 将获取过程建模为成本递增的级联：先尝试 self/teacher，再做工具研究，最后请求 expert；检索结合语义相似度与 Thompson sampling，并在写回前验证和整理记忆。 保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；保真度：本地实现成本感知的分级获取、语义检索、Thompson sampling 和记忆验证；当前 mini-suite 不包含论文使用的真实 LLM、HotpotQA 或 AIME 推理。mini-suite 的知识源、专家和验证器都是确定性的，不包含真实搜索 API、模型幻觉或 token 成本。因此这里验证的是主动获取状态机与成本记账，不是 HotpotQA/AIME 分数复刻。evomem-mini 覆盖 episode 内/跨 episode × knowledge/execution 四象限。  主动记忆 Agent 记忆与技能：让经验可取回、可失效 本地专家和知识源是确定性的，会限制什么结论？ 它们不包含真实搜索失败、幻觉、付费模型或 token 成本，因此只验证升级、验证、写入状态机与代理成本记账。若低置信后总能从预设源得到正确知识，不能据此声称 HotpotQA 或 AIME 能力，以及现实成本收益已经复现。 例如 fixture 专家永远返回预设事实，只能测试“升级分支可用”，不能证明真实专家请求会成功或花费相同成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-14d3f0283f16c6fd">本地专家和知识源是确定性的，会限制什么结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Au-mem">U-Mem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它们不包含真实搜索失败、幻觉、付费模型或 token 成本，因此只验证升级、验证、写入状态机与代理成本记账。若低置信后总能从预设源得到正确知识，不能据此声称 HotpotQA 或 AIME 能力，以及现实成本收益已经复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 fixture 专家永远返回预设事实，只能测试“升级分支可用”，不能证明真实专家请求会成功或花费相同成本。</p>
<p class="ar-learning-sources">依据：核心公式与算法、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22406">原论文</a> · <a href="../../../../agent-research/2602.22406-u-mem/">实现解读</a> · <a href="#qa-14d3f0283f16c6fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pahf" data-paper-title="Learning Personalized Agents from Human Feedback" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Personalized Agents from Human Feedback Agent Meta Superintelligence Labs / Princeton University（工作完成于 Meta） 2026-02-18 Agent 在行动前从显式用户记忆检索偏好，未知或低置信时主动澄清；行动后无论当前记忆是否自信，都接收纠正并覆盖过期偏好，从而处理新用户、上下文差异和偏好漂移。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。三种子诊断：metrics/mechanism-seeds42-44.json  个性化 Agent 显式记忆 双通道反馈 Agent 记忆与技能：让经验可取回、可失效 行动前澄清与行动后纠正为什么是两种互补反馈？ 行动前在未知或低置信时询问，可减少对新偏好的猜测；行动后反馈让系统修正已执行行为和过期记忆，处理漂移。即使原记忆很自信也应接收纠正，因为用户偏好可能随情境和时间改变，置信不能成为拒绝更新的理由。 例如以前用户爱辣，今天点餐改为清淡，行动前可澄清；若已点错，明确纠正仍应覆盖当前情境的旧偏好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-pahf-5582b2a9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cc0d33bd49105a98">行动前澄清与行动后纠正为什么是两种互补反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apahf">Learning Personalized Agents from Human Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / Princeton University（工作完成于 Meta）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行动前在未知或低置信时询问，可减少对新偏好的猜测；行动后反馈让系统修正已执行行为和过期记忆，处理漂移。即使原记忆很自信也应接收纠正，因为用户偏好可能随情境和时间改变，置信不能成为拒绝更新的理由。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如以前用户爱辣，今天点餐改为清淡，行动前可澄清；若已点错，明确纠正仍应覆盖当前情境的旧偏好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16173">原论文</a> · <a href="../../../../agent-research/2602.16173-pahf/">实现解读</a> · <a href="#qa-cc0d33bd49105a98">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pahf" data-paper-title="Learning Personalized Agents from Human Feedback" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Personalized Agents from Human Feedback Agent Meta Superintelligence Labs / Princeton University（工作完成于 Meta） 2026-02-18 Agent 在行动前从显式用户记忆检索偏好，未知或低置信时主动澄清；行动后无论当前记忆是否自信，都接收纠正并覆盖过期偏好，从而处理新用户、上下文差异和偏好漂移。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。三种子诊断：metrics/mechanism-seeds42-44.json  个性化 Agent 显式记忆 双通道反馈 Agent 记忆与技能：让经验可取回、可失效 为什么行动后即使原记忆很自信，也必须允许用户纠正偏好？ 自信只反映当前记忆状态，不保证偏好没随场景或时间变化。行动前检索和澄清处理未知，行动后纠正覆盖过期内容，两个阶段解决不同问题；若只在低置信时接受反馈，曾经学错或已漂移的高置信偏好反而会被永久固化。 例如用户过去常选早班机，如今因作息改变拒绝；系统应更新偏好，而不能因为旧记录自信就继续反复订早班。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pahf" data-paper-title="Learning Personalized Agents from Human Feedback" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Personalized Agents from Human Feedback Agent Meta Superintelligence Labs / Princeton University（工作完成于 Meta） 2026-02-18 Agent 在行动前从显式用户记忆检索偏好，未知或低置信时主动澄清；行动后无论当前记忆是否自信，都接收纠正并覆盖过期偏好，从而处理新用户、上下文差异和偏好漂移。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。三种子诊断：metrics/mechanism-seeds42-44.json  个性化 Agent 显式记忆 双通道反馈 Agent 记忆与技能：让经验可取回、可失效 显式偏好记忆与把用户 persona 当隐藏真值输入有什么区别？ 显式记忆来自已发生的用户反馈，带有可观察依据；隐藏 persona 或 gold action 只供评测，提前提供会消除个性化学习难点。PAHF 关注从交互获得偏好与变化，不是每轮直接读取评测设定后选择标准动作。 例如用户说过“工作日不喝咖啡”可以记忆，测试文件暗藏的同一句不能未经交互就喂给策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-48e5888ea773945f">显式偏好记忆与把用户 persona 当隐藏真值输入有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apahf">Learning Personalized Agents from Human Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / Princeton University（工作完成于 Meta）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>显式记忆来自已发生的用户反馈，带有可观察依据；隐藏 persona 或 gold action 只供评测，提前提供会消除个性化学习难点。PAHF 关注从交互获得偏好与变化，不是每轮直接读取评测设定后选择标准动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户说过“工作日不喝咖啡”可以记忆，测试文件暗藏的同一句不能未经交互就喂给策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16173">原论文</a> · <a href="../../../../agent-research/2602.16173-pahf/">实现解读</a> · <a href="#qa-48e5888ea773945f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pahf" data-paper-title="Learning Personalized Agents from Human Feedback" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Learning Personalized Agents from Human Feedback Agent Meta Superintelligence Labs / Princeton University（工作完成于 Meta） 2026-02-18 Agent 在行动前从显式用户记忆检索偏好，未知或低置信时主动澄清；行动后无论当前记忆是否自信，都接收纠正并覆盖过期偏好，从而处理新用户、上下文差异和偏好漂移。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。本地执行显式记忆、澄清门和漂移覆盖，不读取隐藏 persona/gold action，不调用 GPT、机器人环境或论文购物模拟器。三种子诊断：metrics/mechanism-seeds42-44.json  个性化 Agent 显式记忆 双通道反馈 Agent 记忆与技能：让经验可取回、可失效 漂移覆盖为何不能只在低置信时允许写入？ 高置信反映过去证据，不保证当前偏好仍成立，行动后明确纠正应能覆盖过期值并保留情境。当前本地验证记忆、澄清门与漂移更新，不调用机器人、购物模拟器或 GPT；组件通过不表示所有真实用户个性化质量已验证。 例如旧偏好被确认十次，用户今天说医生建议停用，系统仍应按新反馈更新，而不能因高置信拒绝。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b7a9fbb39023c495">漂移覆盖为何不能只在低置信时允许写入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apahf">Learning Personalized Agents from Human Feedback</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Superintelligence Labs / Princeton University（工作完成于 Meta）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高置信反映过去证据，不保证当前偏好仍成立，行动后明确纠正应能覆盖过期值并保留情境。当前本地验证记忆、澄清门与漂移更新，不调用机器人、购物模拟器或 GPT；组件通过不表示所有真实用户个性化质量已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧偏好被确认十次，用户今天说医生建议停用，系统仍应按新反馈更新，而不能因高置信拒绝。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16173">原论文</a> · <a href="../../../../agent-research/2602.16173-pahf/">实现解读</a> · <a href="#qa-b7a9fbb39023c495">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memskill" data-paper-title="MemSkill" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemSkill Agent Nanyang Technological University 2026-02-02 controller 从历史 episode 选择记忆，designer 将重复成功模式编译为技能，并随新反馈升级技能版本。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  记忆技能 Agent 记忆与技能：让经验可取回、可失效 controller 与 designer 在情景记忆到技能的过程中各做什么？ controller 为当前任务从历史 episode 选择相关经验，designer 将重复成功模式编译成可复用技能，再根据新反馈升级版本。前者解决用哪些证据，后者解决如何形成方法；只检索旧日志而不编译，或只写技能却不关联任务，都缺少一部分链路。 例如多个成功导入任务都有“先验证列名”，controller 找到这些经验，designer 才把共同行为整理成可调用技能。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memskill-ffe2092a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-82b492a82fb86598">controller 与 designer 在情景记忆到技能的过程中各做什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemskill">MemSkill</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>controller 为当前任务从历史 episode 选择相关经验，designer 将重复成功模式编译成可复用技能，再根据新反馈升级版本。前者解决用哪些证据，后者解决如何形成方法；只检索旧日志而不编译，或只写技能却不关联任务，都缺少一部分链路。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如多个成功导入任务都有“先验证列名”，controller 找到这些经验，designer 才把共同行为整理成可调用技能。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.02474">原论文</a> · <a href="../../../../agent-research/2602.02474-memskill/">实现解读</a> · <a href="#qa-82b492a82fb86598">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memskill" data-paper-title="MemSkill" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemSkill Agent Nanyang Technological University 2026-02-02 controller 从历史 episode 选择记忆，designer 将重复成功模式编译为技能，并随新反馈升级技能版本。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  记忆技能 Agent 记忆与技能：让经验可取回、可失效 controller 选择记忆与 designer 编译技能为什么不是同一件事？ 选择解决当前任务需要读哪段经验，编译则把重复成功模式转换为以后可调用的程序知识。二者时间尺度与对象不同，新反馈还要驱动版本升级；检索到一次成功 episode 不足以证明其细节可直接固化，仍需区分通用步骤与偶然环境条件。 例如先为当前报错找历史修复记录，多次确认同类模式后才形成技能；那次日志里的临时账号不应被一起编译成固定参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memskill" data-paper-title="MemSkill" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemSkill Agent Nanyang Technological University 2026-02-02 controller 从历史 episode 选择记忆，designer 将重复成功模式编译为技能，并随新反馈升级技能版本。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  记忆技能 Agent 记忆与技能：让经验可取回、可失效 重复成功模式与一次成功轨迹在固化可信度上有何区别？ 单次成功可能依赖偶然环境或隐藏帮助，重复模式提供跨实例支持，更适合提炼技能。重复也不保证因果必要，仍要检查前提、失败反馈与版本变化；不能把出现频次直接当成通用正确性或省去验证。 例如三次都先清缓存后成功，可能只是这三题都恰好需要清缓存，技能应注明适用条件而非强制所有任务清缓存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-07fecf19d9da77a6">重复成功模式与一次成功轨迹在固化可信度上有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemskill">MemSkill</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单次成功可能依赖偶然环境或隐藏帮助，重复模式提供跨实例支持，更适合提炼技能。重复也不保证因果必要，仍要检查前提、失败反馈与版本变化；不能把出现频次直接当成通用正确性或省去验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三次都先清缓存后成功，可能只是这三题都恰好需要清缓存，技能应注明适用条件而非强制所有任务清缓存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.02474">原论文</a> · <a href="../../../../agent-research/2602.02474-memskill/">实现解读</a> · <a href="#qa-07fecf19d9da77a6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memskill" data-paper-title="MemSkill" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemSkill Agent Nanyang Technological University 2026-02-02 controller 从历史 episode 选择记忆，designer 将重复成功模式编译为技能，并随新反馈升级技能版本。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3200；方法特有操作有非零 telemetry。  记忆技能 Agent 记忆与技能：让经验可取回、可失效 本地技能版本更新与完整 designer 学习的证据边界是什么？ 本地只验证选择、编译式状态转换、版本与预算合同，没有复刻原论文 LLM、RL 或完整真实环境。版本号增加证明更新路径被调用，不说明模型已从自然语言日志学会提炼可靠技能，也不能将受控满分与原文跨任务能力相等同。 例如规则把重复步骤转成结构化模板可测试 pipeline，但没有 learned designer 时，不应声称自动发现开放任务程序知识。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-69a2bd22598ec1e6">本地技能版本更新与完整 designer 学习的证据边界是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemskill">MemSkill</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地只验证选择、编译式状态转换、版本与预算合同，没有复刻原论文 LLM、RL 或完整真实环境。版本号增加证明更新路径被调用，不说明模型已从自然语言日志学会提炼可靠技能，也不能将受控满分与原文跨任务能力相等同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如规则把重复步骤转成结构化模板可测试 pipeline，但没有 learned designer 时，不应声称自动发现开放任务程序知识。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.02474">原论文</a> · <a href="../../../../agent-research/2602.02474-memskill/">实现解读</a> · <a href="#qa-69a2bd22598ec1e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sage" data-paper-title="SAGE" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SAGE Agent University of Wisconsin–Madison 2025-12-18 从成功轨迹抽象技能，失败时修订或淘汰，并以任务回报学习技能检索与复用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3000；方法特有操作有非零 telemetry。  技能库强化学习 Agent 记忆与技能：让经验可取回、可失效 SAGE 技能失败后为什么既可以修订也可以淘汰？ 失败可能表明步骤需局部修复，也可能说明技能过时或不适合当前分布。只追加成功摘要会保留错误，全部淘汰又浪费可修复知识；SAGE 根据任务回报更新技能及其检索复用策略，目的在于持续管理而非无限增长库。 例如参数名称变更可修订，某服务永久下线则可能应淘汰对应技能，不必用同一种处理所有失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-sage-ae754679" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-52bc9ca93fa82930">SAGE 技能失败后为什么既可以修订也可以淘汰？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asage">SAGE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>失败可能表明步骤需局部修复，也可能说明技能过时或不适合当前分布。只追加成功摘要会保留错误，全部淘汰又浪费可修复知识；SAGE 根据任务回报更新技能及其检索复用策略，目的在于持续管理而非无限增长库。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如参数名称变更可修订，某服务永久下线则可能应淘汰对应技能，不必用同一种处理所有失败。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.17102">原论文</a> · <a href="../../../../agent-research/2512.17102-sage/">实现解读</a> · <a href="#qa-52bc9ca93fa82930">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sage" data-paper-title="SAGE" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SAGE Agent University of Wisconsin–Madison 2025-12-18 从成功轨迹抽象技能，失败时修订或淘汰，并以任务回报学习技能检索与复用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3000；方法特有操作有非零 telemetry。  技能库强化学习 Agent 记忆与技能：让经验可取回、可失效 为什么成功轨迹抽出的技能仍需要在失败时修订或淘汰？ 成功只说明技能在当时条件可用，新任务可能不满足同样前提。执行回报既训练检索选择，也反馈技能内容是否失效，修订与淘汰阻止错误长期累积；若库只增不减，相关但过时的技能可能持续被检索并强化错误行为。 例如旧网站的下载技能曾经成功，页面改版后按钮路径失效，应修订或停用，而不是因历史成功继续把它排第一。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sage" data-paper-title="SAGE" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SAGE Agent University of Wisconsin–Madison 2025-12-18 从成功轨迹抽象技能，失败时修订或淘汰，并以任务回报学习技能检索与复用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3000；方法特有操作有非零 telemetry。  技能库强化学习 Agent 记忆与技能：让经验可取回、可失效 学习技能检索 qφ 与固定语义最近邻有什么不同？ 语义最近邻按描述相似选项，学习检索可用执行回报调整哪些技能真正有助任务。回报仍受环境和任务难度影响，不能把被调用后成功直接视为独立因果贡献；检索策略更新需与技能库状态和可见信息一起核查。 例如两技能描述都像“整理文件”，实际验证更可靠的路线可得到较高学习分，而不只看共享关键词多少。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ffb4ccd96e5b0cbb">学习技能检索 qφ 与固定语义最近邻有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asage">SAGE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语义最近邻按描述相似选项，学习检索可用执行回报调整哪些技能真正有助任务。回报仍受环境和任务难度影响，不能把被调用后成功直接视为独立因果贡献；检索策略更新需与技能库状态和可见信息一起核查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两技能描述都像“整理文件”，实际验证更可靠的路线可得到较高学习分，而不只看共享关键词多少。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.17102">原论文</a> · <a href="../../../../agent-research/2512.17102-sage/">实现解读</a> · <a href="#qa-ffb4ccd96e5b0cbb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sage" data-paper-title="SAGE" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="SAGE Agent University of Wisconsin–Madison 2025-12-18 从成功轨迹抽象技能，失败时修订或淘汰，并以任务回报学习技能检索与复用。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 0.3000；方法特有操作有非零 telemetry。  技能库强化学习 Agent 记忆与技能：让经验可取回、可失效 本地 SAGE 与 sage-planner 能因同名共享实现结论吗？ 不能。这里 SAGE 管理 RL 驱动技能库，另一条 sage-planner 关注符号 action gate 与后缀编辑，算法对象不同。本地本条只验证技能状态更新和预算，没有原论文大模型训练或完整 benchmark，名称相似不能补齐缺失实现证据。 例如技能库一次修订并未执行任何符号前置条件门，不能借另一 SAGE 的 gate 测试宣称本方法全部验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-22f204cc4f69319a">本地 SAGE 与 sage-planner 能因同名共享实现结论吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asage">SAGE</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Wisconsin–Madison</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。这里 SAGE 管理 RL 驱动技能库，另一条 sage-planner 关注符号 action gate 与后缀编辑，算法对象不同。本地本条只验证技能状态更新和预算，没有原论文大模型训练或完整 benchmark，名称相似不能补齐缺失实现证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如技能库一次修订并未执行任何符号前置条件门，不能借另一 SAGE 的 gate 测试宣称本方法全部验证。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2512.17102">原论文</a> · <a href="../../../../agent-research/2512.17102-sage/">实现解读</a> · <a href="#qa-22f204cc4f69319a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:legomem" data-paper-title="LEGOMem" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="LEGOMem Agent Microsoft Research 2025-10-06 整段成功轨迹难以迁移到新任务，单一全局记忆又混合了任务分解和工具执行。LEGOMem 把经验拆成像积木一样的 procedural units：orchestrator memory 保存任务分解与委派，agent memory 保存具体动作模板，运行时按新任务重新组合。 保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；当前 PlanBench mini 不替代论文的 OfficeBench 多 Agent 环境。当前没有真实 Office 应用、LLM 多 Agent 委派或错误恢复。实现证明过程单元能提取、验证和跨 episode 复用，但不构成 OfficeBench 原始结果的复刻。planbench-mini 使用可验证结构化计划。实现从成功计划提取 action/domain 单元，分别复用高层分解和细粒度动作，并记录 reused_plans。  过程记忆 Agent 记忆与技能：让经验可取回、可失效 orchestrator memory 与 agent memory 为什么分别存过程单元？ 编排器需要任务分解和委派经验，执行 Agent 需要具体动作模板，两者抽象层次不同。拆分后可在新任务组合高层流程与低层动作，而不搬整段旧轨迹；只有通过任务验证的单元才进入长期记忆，避免把未证实步骤长期复用。 例如“收集数据后交给分析者”属于编排经验，某表格工具如何读范围属于执行经验，可各自复用而不绑定同一旧任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-legomem-3e37af3a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c4c27071fd8d1be5">orchestrator memory 与 agent memory 为什么分别存过程单元？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alegomem">LEGOMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>编排器需要任务分解和委派经验，执行 Agent 需要具体动作模板，两者抽象层次不同。拆分后可在新任务组合高层流程与低层动作，而不搬整段旧轨迹；只有通过任务验证的单元才进入长期记忆，避免把未证实步骤长期复用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“收集数据后交给分析者”属于编排经验，某表格工具如何读范围属于执行经验，可各自复用而不绑定同一旧任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与算法；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04851">原论文</a> · <a href="../../../../agent-research/2510.04851-legomem/">实现解读</a> · <a href="#qa-c4c27071fd8d1be5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:legomem" data-paper-title="LEGOMem" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="LEGOMem Agent Microsoft Research 2025-10-06 整段成功轨迹难以迁移到新任务，单一全局记忆又混合了任务分解和工具执行。LEGOMem 把经验拆成像积木一样的 procedural units：orchestrator memory 保存任务分解与委派，agent memory 保存具体动作模板，运行时按新任务重新组合。 保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；当前 PlanBench mini 不替代论文的 OfficeBench 多 Agent 环境。当前没有真实 Office 应用、LLM 多 Agent 委派或错误恢复。实现证明过程单元能提取、验证和跨 episode 复用，但不构成 OfficeBench 原始结果的复刻。planbench-mini 使用可验证结构化计划。实现从成功计划提取 action/domain 单元，分别复用高层分解和细粒度动作，并记录 reused_plans。  过程记忆 Agent 记忆与技能：让经验可取回、可失效 为什么编排记忆与执行记忆分开，更容易重新组合到新任务？ 任务分解与委派描述高层依赖，具体动作模板描述如何落地工具调用，把它们混成整段轨迹会绑死人员和环境。分层后可复用分解结构并替换执行单元；只有经过验证的单元准入，拼接后仍要检查接口与前置条件，不能任意积木化。 例如“收集、核对、汇总”流程不变，但某次从数据库读取、另一次从文件读取；编排可复用，底层执行模板可替换。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:legomem" data-paper-title="LEGOMem" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="LEGOMem Agent Microsoft Research 2025-10-06 整段成功轨迹难以迁移到新任务，单一全局记忆又混合了任务分解和工具执行。LEGOMem 把经验拆成像积木一样的 procedural units：orchestrator memory 保存任务分解与委派，agent memory 保存具体动作模板，运行时按新任务重新组合。 保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；当前 PlanBench mini 不替代论文的 OfficeBench 多 Agent 环境。当前没有真实 Office 应用、LLM 多 Agent 委派或错误恢复。实现证明过程单元能提取、验证和跨 episode 复用，但不构成 OfficeBench 原始结果的复刻。planbench-mini 使用可验证结构化计划。实现从成功计划提取 action/domain 单元，分别复用高层分解和细粒度动作，并记录 reused_plans。  过程记忆 Agent 记忆与技能：让经验可取回、可失效 过程积木重组与整条轨迹检索有什么泛化取舍？ 整轨迹保留一次执行完整上下文，却可能被具体任务绑死；过程单元可按新需求重新拼接，也容易丢掉跨单元前提。可组合性需要合法依赖和验证，不能因单元单独成功就假定任意组合都正确。 例如读取表格单元和邮件发送单元各自可用，组合时仍须确认收件人和数据权限，不能盲目串联。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-2732f77db1bafc8e">过程积木重组与整条轨迹检索有什么泛化取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alegomem">LEGOMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整轨迹保留一次执行完整上下文，却可能被具体任务绑死；过程单元可按新需求重新拼接，也容易丢掉跨单元前提。可组合性需要合法依赖和验证，不能因单元单独成功就假定任意组合都正确。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如读取表格单元和邮件发送单元各自可用，组合时仍须确认收件人和数据权限，不能盲目串联。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与算法；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04851">原论文</a> · <a href="../../../../agent-research/2510.04851-legomem/">实现解读</a> · <a href="#qa-2732f77db1bafc8e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:legomem" data-paper-title="LEGOMem" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="LEGOMem Agent Microsoft Research 2025-10-06 整段成功轨迹难以迁移到新任务，单一全局记忆又混合了任务分解和工具执行。LEGOMem 把经验拆成像积木一样的 procedural units：orchestrator memory 保存任务分解与委派，agent memory 保存具体动作模板，运行时按新任务重新组合。 保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；保真度：本地实现编排器与执行层过程单元、成功轨迹提取和跨 episode 复用；当前 PlanBench mini 不替代论文的 OfficeBench 多 Agent 环境。当前没有真实 Office 应用、LLM 多 Agent 委派或错误恢复。实现证明过程单元能提取、验证和跨 episode 复用，但不构成 OfficeBench 原始结果的复刻。planbench-mini 使用可验证结构化计划。实现从成功计划提取 action/domain 单元，分别复用高层分解和细粒度动作，并记录 reused_plans。  过程记忆 Agent 记忆与技能：让经验可取回、可失效 本地 reused_plans 是否验证了真实多 Agent Office 委派？ 没有。本地从可验证结构化计划提取 action/domain 单元，分别复用高层和细粒度动作，没有真实 Office 应用、LLM 委派或完整错误恢复。复用计数只证明过程单元被调用，不是 OfficeBench 的执行成功或真实工具成本。 例如规则把同一子计划用了一百次，不代表模型能在实际文档和邮件应用间正确分派并完成任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8e26df792894a3d7">本地 reused_plans 是否验证了真实多 Agent Office 委派？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alegomem">LEGOMem</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地从可验证结构化计划提取 action/domain 单元，分别复用高层和细粒度动作，没有真实 Office 应用、LLM 委派或完整错误恢复。复用计数只证明过程单元被调用，不是 OfficeBench 的执行成功或真实工具成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如规则把同一子计划用了一百次，不代表模型能在实际文档和邮件应用间正确分派并完成任务。</p>
<p class="ar-learning-sources">依据：核心公式与算法、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04851">原论文</a> · <a href="../../../../agent-research/2510.04851-legomem/">实现解读</a> · <a href="#qa-8e26df792894a3d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memtool" data-paper-title="MemTool" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemTool Agent PricewaterhouseCoopers Commercial Technology and Innovation Office 2025-07-29 大量 MCP 工具描述会迅速占满上下文，静态截断又可能删掉当前工作流需要的工具。MemTool 比较 autonomous、workflow 和 hybrid 管理方式；hybrid 策略保护当前工作流的必需工具，其余工具依据近期性和历史成功率动态淘汰。 保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；ScaleMCP mini 只验证多轮工具集合管理，不包含 5,000 个真实 MCP server。工具是本地确定性描述，没有真实 MCP 网络延迟、权限失败或模型工具选择误差。结果支持受限上下文的淘汰逻辑与指标链路，不能直接对比论文的 5,000-server 实验。scalemcp-mini 生成连续工具需求，在固定 memory size 下更新保护集合、淘汰非必要工具，并统计 task success、上下文成本和 tool_evictions。  工具记忆 Agent 记忆与技能：让经验可取回、可失效 工具描述为什么也需要有界动态记忆？ 大量 MCP schema 与说明会占上下文，全部常驻影响成本，静态截断又可能删掉正在使用的工具。MemTool 将当前工作流必需项设为保护集，再管理其他描述，重点是保留可执行所需接口；移除率高本身不是成功目标。 例如当前流程要先查订单再退款，即使退款工具最近没调用，也不能在中途因近期性低被淘汰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memtool-13c64e5c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-30295a2477bae0ec">工具描述为什么也需要有界动态记忆？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemtool">MemTool</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PricewaterhouseCoopers Commercial Technology and Innovation Office</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>大量 MCP schema 与说明会占上下文，全部常驻影响成本，静态截断又可能删掉正在使用的工具。MemTool 将当前工作流必需项设为保护集，再管理其他描述，重点是保留可执行所需接口；移除率高本身不是成功目标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如当前流程要先查订单再退款，即使退款工具最近没调用，也不能在中途因近期性低被淘汰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与算法；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.21428">原论文</a> · <a href="../../../../agent-research/2507.21428-memtool/">实现解读</a> · <a href="#qa-30295a2477bae0ec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memtool" data-paper-title="MemTool" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemTool Agent PricewaterhouseCoopers Commercial Technology and Innovation Office 2025-07-29 大量 MCP 工具描述会迅速占满上下文，静态截断又可能删掉当前工作流需要的工具。MemTool 比较 autonomous、workflow 和 hybrid 管理方式；hybrid 策略保护当前工作流的必需工具，其余工具依据近期性和历史成功率动态淘汰。 保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；ScaleMCP mini 只验证多轮工具集合管理，不包含 5,000 个真实 MCP server。工具是本地确定性描述，没有真实 MCP 网络延迟、权限失败或模型工具选择误差。结果支持受限上下文的淘汰逻辑与指标链路，不能直接对比论文的 5,000-server 实验。scalemcp-mini 生成连续工具需求，在固定 memory size 下更新保护集合、淘汰非必要工具，并统计 task success、上下文成本和 tool_evictions。  工具记忆 Agent 记忆与技能：让经验可取回、可失效 为什么当前工作流必需工具必须优先于近期性或历史成功率被保护？ 启发式保留分数反映过去使用情况，却可能低估接下来尚未调用的必需工具。先保护工作流依赖，再在其余工具中淘汰低分项，才能避免执行中途失去关键接口；如果必需集合本身超过容量，也不能靠静默截断假装工作流仍完整。 例如归档任务最后才需上传工具，它近期没用过但仍是必需步骤；不能只因低近期性把它从当前上下文删掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memtool" data-paper-title="MemTool" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemTool Agent PricewaterhouseCoopers Commercial Technology and Innovation Office 2025-07-29 大量 MCP 工具描述会迅速占满上下文，静态截断又可能删掉当前工作流需要的工具。MemTool 比较 autonomous、workflow 和 hybrid 管理方式；hybrid 策略保护当前工作流的必需工具，其余工具依据近期性和历史成功率动态淘汰。 保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；ScaleMCP mini 只验证多轮工具集合管理，不包含 5,000 个真实 MCP server。工具是本地确定性描述，没有真实 MCP 网络延迟、权限失败或模型工具选择误差。结果支持受限上下文的淘汰逻辑与指标链路，不能直接对比论文的 5,000-server 实验。scalemcp-mini 生成连续工具需求，在固定 memory size 下更新保护集合、淘汰非必要工具，并统计 task success、上下文成本和 tool_evictions。  工具记忆 Agent 记忆与技能：让经验可取回、可失效 hybrid 与纯 recency 淘汰的关键区别是什么？ hybrid 先保护工作流必需工具，只有剩余集合才按近期性和历史成功率排名淘汰；纯 recency 可能误删即将用到但尚未调用的步骤。保护集也需正确识别，不能用隐藏 required_tools 真值直接给策略降低难度。 例如新流程最后一步才需要发票工具，它近期性为零但属于必需项，混合策略应先保护而非依排名删除。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-13511d15aa68dae4">hybrid 与纯 recency 淘汰的关键区别是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemtool">MemTool</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PricewaterhouseCoopers Commercial Technology and Innovation Office</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>hybrid 先保护工作流必需工具，只有剩余集合才按近期性和历史成功率排名淘汰；纯 recency 可能误删即将用到但尚未调用的步骤。保护集也需正确识别，不能用隐藏 required_tools 真值直接给策略降低难度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新流程最后一步才需要发票工具，它近期性为零但属于必需项，混合策略应先保护而非依排名删除。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与算法；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.21428">原论文</a> · <a href="../../../../agent-research/2507.21428-memtool/">实现解读</a> · <a href="#qa-13511d15aa68dae4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memtool" data-paper-title="MemTool" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemTool Agent PricewaterhouseCoopers Commercial Technology and Innovation Office 2025-07-29 大量 MCP 工具描述会迅速占满上下文，静态截断又可能删掉当前工作流需要的工具。MemTool 比较 autonomous、workflow 和 hybrid 管理方式；hybrid 策略保护当前工作流的必需工具，其余工具依据近期性和历史成功率动态淘汰。 保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；保真度：本地实现 hybrid 工具记忆、工作流保护和动态淘汰；ScaleMCP mini 只验证多轮工具集合管理，不包含 5,000 个真实 MCP server。工具是本地确定性描述，没有真实 MCP 网络延迟、权限失败或模型工具选择误差。结果支持受限上下文的淘汰逻辑与指标链路，不能直接对比论文的 5,000-server 实验。scalemcp-mini 生成连续工具需求，在固定 memory size 下更新保护集合、淘汰非必要工具，并统计 task success、上下文成本和 tool_evictions。  工具记忆 Agent 记忆与技能：让经验可取回、可失效 容量已满时可以为了满足上限强制淘汰 required 工具吗？ 不应。公式只在非保护集合中找最低分，必需集合优先于启发式；若容量无法容纳应显式处理不可行合同，不能静默破坏流程。当前本地工具为确定性描述，无真实网络、权限失败或模型误选，不能对标五千服务器实验。 例如所有槽都被当前必需工具占用，新描述到达时不能偷偷删一个必需接口，再把后续调用失败归因模型。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c38703d1cf219e1f">容量已满时可以为了满足上限强制淘汰 required 工具吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemtool">MemTool</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · PricewaterhouseCoopers Commercial Technology and Innovation Office</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不应。公式只在非保护集合中找最低分，必需集合优先于启发式；若容量无法容纳应显式处理不可行合同，不能静默破坏流程。当前本地工具为确定性描述，无真实网络、权限失败或模型误选，不能对标五千服务器实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如所有槽都被当前必需工具占用，新描述到达时不能偷偷删一个必需接口，再把后续调用失败归因模型。</p>
<p class="ar-learning-sources">依据：核心公式与算法、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2507.21428">原论文</a> · <a href="../../../../agent-research/2507.21428-memtool/">实现解读</a> · <a href="#qa-c38703d1cf219e1f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memgpt" data-paper-title="MemGPT" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemGPT Agent University of California, Berkeley 2023-10-12 有限 context window 使长文档和多轮会话不断遗忘。MemGPT 借鉴操作系统虚拟内存，把常驻核心信息、当前工作上下文和外部归档分层管理；模型通过函数调用移动数据，并以 interrupt/heartbeat 控制继续推理和与用户交互。 本页实现 core、working、archival 三层状态，工作上下文超预算时触发 interrupt、page-out，并在后续任务中 page-in。实现分层状态、换入换出和 interrupt 计数；归档检索使用确定性 key，不调用 embedding 服务或 LLM function calling。成本是统一代理成本，不是 token 或线上延迟。EvoMem mini 120 episodes、seed 42、memory size 24；working tier 使用一半容量，压力触发 page-out，重复任务从 archival tier page-in。  虚拟上下文 Agent 记忆与技能：让经验可取回、可失效 归档容量很大为什么不意味着模型每轮都能直接读到全部内容？ 外部归档只是可存储状态，当前上下文仍受窗口限制，模型需通过函数调用换入所需片段。核心信息、工作区和归档分层使长期保存可行，但检索与调度可能失败，不能把无限存储误写成无限同时可见上下文。 例如一年前的用户偏好在归档中，当前回答前仍需检索并 page-in；仅文件存在不会自动影响下一 token。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-memgpt-81032c11" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-21988cc15fb83697">归档容量很大为什么不意味着模型每轮都能直接读到全部内容？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemgpt">MemGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>外部归档只是可存储状态，当前上下文仍受窗口限制，模型需通过函数调用换入所需片段。核心信息、工作区和归档分层使长期保存可行，但检索与调度可能失败，不能把无限存储误写成无限同时可见上下文。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一年前的用户偏好在归档中，当前回答前仍需检索并 page-in；仅文件存在不会自动影响下一 token。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.08560">原论文</a> · <a href="../../../../agent-research/2310.08560-memgpt/">实现解读</a> · <a href="#qa-21988cc15fb83697">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memgpt" data-paper-title="MemGPT" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemGPT Agent University of California, Berkeley 2023-10-12 有限 context window 使长文档和多轮会话不断遗忘。MemGPT 借鉴操作系统虚拟内存，把常驻核心信息、当前工作上下文和外部归档分层管理；模型通过函数调用移动数据，并以 interrupt/heartbeat 控制继续推理和与用户交互。 本页实现 core、working、archival 三层状态，工作上下文超预算时触发 interrupt、page-out，并在后续任务中 page-in。实现分层状态、换入换出和 interrupt 计数；归档检索使用确定性 key，不调用 embedding 服务或 LLM function calling。成本是统一代理成本，不是 token 或线上延迟。EvoMem mini 120 episodes、seed 42、memory size 24；working tier 使用一半容量，压力触发 page-out，重复任务从 archival tier page-in。  虚拟上下文 Agent 记忆与技能：让经验可取回、可失效 外部归档很大，为什么仍需要模型主动管理 page-in/page-out？ 归档容量不等于模型当前能读取的上下文，相关内容必须被调入工作窗口才能影响回答。分页操作连接长期保存与当前任务，heartbeat 或中断控制继续取证和与用户交互；它提供虚拟内存式接口，不是让模型一次直接看见无限历史。 例如旧对话中的地址保存在归档，回答寄件问题前仍需检索并调入；仅说“归档里有”不会自动让当前推理知道地址。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memgpt" data-paper-title="MemGPT" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemGPT Agent University of California, Berkeley 2023-10-12 有限 context window 使长文档和多轮会话不断遗忘。MemGPT 借鉴操作系统虚拟内存，把常驻核心信息、当前工作上下文和外部归档分层管理；模型通过函数调用移动数据，并以 interrupt/heartbeat 控制继续推理和与用户交互。 本页实现 core、working、archival 三层状态，工作上下文超预算时触发 interrupt、page-out，并在后续任务中 page-in。实现分层状态、换入换出和 interrupt 计数；归档检索使用确定性 key，不调用 embedding 服务或 LLM function calling。成本是统一代理成本，不是 token 或线上延迟。EvoMem mini 120 episodes、seed 42、memory size 24；working tier 使用一半容量，压力触发 page-out，重复任务从 archival tier page-in。  虚拟上下文 Agent 记忆与技能：让经验可取回、可失效 heartbeat 与正常向用户返回相比，控制流程有什么不同？ heartbeat 或 interrupt 让系统内部继续处理记忆与工具，而不把每次内部操作都当最终用户回答。它提供调度接口，不保证何时调用正确；无条件循环也可能浪费预算，需要与当前工作和可见结果相匹配。 例如刚把旧内容换出后可继续内部检索相关片段，再对用户作答，而不是先返回半截“正在移动记忆”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ae4e9dea4029ce9d">heartbeat 与正常向用户返回相比，控制流程有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemgpt">MemGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>heartbeat 或 interrupt 让系统内部继续处理记忆与工具，而不把每次内部操作都当最终用户回答。它提供调度接口，不保证何时调用正确；无条件循环也可能浪费预算，需要与当前工作和可见结果相匹配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如刚把旧内容换出后可继续内部检索相关片段，再对用户作答，而不是先返回半截“正在移动记忆”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.08560">原论文</a> · <a href="../../../../agent-research/2310.08560-memgpt/">实现解读</a> · <a href="#qa-ae4e9dea4029ce9d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:memgpt" data-paper-title="MemGPT" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="MemGPT Agent University of California, Berkeley 2023-10-12 有限 context window 使长文档和多轮会话不断遗忘。MemGPT 借鉴操作系统虚拟内存，把常驻核心信息、当前工作上下文和外部归档分层管理；模型通过函数调用移动数据，并以 interrupt/heartbeat 控制继续推理和与用户交互。 本页实现 core、working、archival 三层状态，工作上下文超预算时触发 interrupt、page-out，并在后续任务中 page-in。实现分层状态、换入换出和 interrupt 计数；归档检索使用确定性 key，不调用 embedding 服务或 LLM function calling。成本是统一代理成本，不是 token 或线上延迟。EvoMem mini 120 episodes、seed 42、memory size 24；working tier 使用一半容量，压力触发 page-out，重复任务从 archival tier page-in。  虚拟上下文 Agent 记忆与技能：让经验可取回、可失效 本地按确定性 key page-in 能代表语义归档检索能力吗？ 不能。本地实现分层状态、换入换出和中断计数，归档按确定性 key 查找，未调用 embedding 或 LLM function calling。代理成本也不是 token 或延迟；只证明 paging 路径执行，不说明真实模型能从长文档中自主找到正确证据。 例如已知键“订单123”直接取回记录，与用户模糊问“上次那笔订单”时自行理解并检索不是同一难度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-656d6a06d31b8c18">本地按确定性 key page-in 能代表语义归档检索能力吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amemgpt">MemGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地实现分层状态、换入换出和中断计数，归档按确定性 key 查找，未调用 embedding 或 LLM function calling。代理成本也不是 token 或延迟；只证明 paging 路径执行，不说明真实模型能从长文档中自主找到正确证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如已知键“订单123”直接取回记录，与用户模糊问“上次那笔订单”时自行理解并检索不是同一难度。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2310.08560">原论文</a> · <a href="../../../../agent-research/2310.08560-memgpt/">实现解读</a> · <a href="#qa-656d6a06d31b8c18">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:voyager" data-paper-title="Voyager" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Voyager Agent NVIDIA 2023-05-25 开放世界 Agent 需要持续选择有新颖性的任务、把成功行为积累为技能，并根据环境报错修复程序。Voyager 用 GPT-4 自动生成 curriculum，以代码作为动作空间；成功程序按描述索引进 skill library，新任务检索并组合已有技能。 本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。本页实现自动课程入口、执行反馈/自验证，以及可增长、可复用的 executable skill library；不声称在本地复刻 Minecraft 世界。保留 curriculum/skill/verification 三组件和跨 episode 复用；本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。  终身学习 Agent 记忆与技能：让经验可取回、可失效 Voyager 为什么把代码作为动作而不是只输出自然语言计划？ 代码可调用环境 API 执行较长行为，并从实际报错与观察中迭代修复，成功程序还能进入技能库供后续任务组合。自然语言计划只有意图，仍需另一个执行映射；代码可执行也不等于逻辑正确，必须在环境中验证。 例如“收集木头”可编成移动、寻找、采集循环，运行后检查库存；只说“去砍树”并未完成这些实际动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-voyager-f3989bf0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-fc830cd6a7e32dd0">Voyager 为什么把代码作为动作而不是只输出自然语言计划？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avoyager">Voyager</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>代码可调用环境 API 执行较长行为，并从实际报错与观察中迭代修复，成功程序还能进入技能库供后续任务组合。自然语言计划只有意图，仍需另一个执行映射；代码可执行也不等于逻辑正确，必须在环境中验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“收集木头”可编成移动、寻找、采集循环，运行后检查库存；只说“去砍树”并未完成这些实际动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16291">原论文</a> · <a href="../../../../agent-research/2305.16291-voyager/">实现解读</a> · <a href="#qa-fc830cd6a7e32dd0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:voyager" data-paper-title="Voyager" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Voyager Agent NVIDIA 2023-05-25 开放世界 Agent 需要持续选择有新颖性的任务、把成功行为积累为技能，并根据环境报错修复程序。Voyager 用 GPT-4 自动生成 curriculum，以代码作为动作空间；成功程序按描述索引进 skill library，新任务检索并组合已有技能。 本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。本页实现自动课程入口、执行反馈/自验证，以及可增长、可复用的 executable skill library；不声称在本地复刻 Minecraft 世界。保留 curriculum/skill/verification 三组件和跨 episode 复用；本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。  终身学习 Agent 记忆与技能：让经验可取回、可失效 为什么只有通过环境验证的程序才进入技能库？ 代码看起来合理不保证能在当前世界执行，环境反馈能暴露缺材料、接口错误或不满足目标。成功后再按描述索引，后续任务才有可复用的行为基础；自动课程负责持续选新目标，技能库负责保留已证实动作，两者不能由单纯程序生成替代。 例如程序写出合成铁镐的步骤，但背包没有铁锭时不能算技能成功；实际完成后才适合作为之后探索的可调用工具。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:voyager" data-paper-title="Voyager" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Voyager Agent NVIDIA 2023-05-25 开放世界 Agent 需要持续选择有新颖性的任务、把成功行为积累为技能，并根据环境报错修复程序。Voyager 用 GPT-4 自动生成 curriculum，以代码作为动作空间；成功程序按描述索引进 skill library，新任务检索并组合已有技能。 本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。本页实现自动课程入口、执行反馈/自验证，以及可增长、可复用的 executable skill library；不声称在本地复刻 Minecraft 世界。保留 curriculum/skill/verification 三组件和跨 episode 复用；本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。  终身学习 Agent 记忆与技能：让经验可取回、可失效 自动 curriculum 与固定任务清单对技能积累有什么不同？ curriculum 根据当前状态与已有技能挑有新颖性的目标，调整探索方向；固定清单便于控制却不随能力变化。自主选任务也可能追逐易得新颖性，需结合真实验证与进展，不应把任务数或探索距离单独当通用能力。 例如已有石工具后再选挖矿目标比反复采木更有探索价值，但是否真的完成仍要看环境库存和里程碑。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e1d7d24beac16b9f">自动 curriculum 与固定任务清单对技能积累有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avoyager">Voyager</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>curriculum 根据当前状态与已有技能挑有新颖性的目标，调整探索方向；固定清单便于控制却不随能力变化。自主选任务也可能追逐易得新颖性，需结合真实验证与进展，不应把任务数或探索距离单独当通用能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如已有石工具后再选挖矿目标比反复采木更有探索价值，但是否真的完成仍要看环境库存和里程碑。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16291">原论文</a> · <a href="../../../../agent-research/2305.16291-voyager/">实现解读</a> · <a href="#qa-e1d7d24beac16b9f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:voyager" data-paper-title="Voyager" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Voyager Agent NVIDIA 2023-05-25 开放世界 Agent 需要持续选择有新颖性的任务、把成功行为积累为技能，并根据环境报错修复程序。Voyager 用 GPT-4 自动生成 curriculum，以代码作为动作空间；成功程序按描述索引进 skill library，新任务检索并组合已有技能。 本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。本页实现自动课程入口、执行反馈/自验证，以及可增长、可复用的 executable skill library；不声称在本地复刻 Minecraft 世界。保留 curriculum/skill/verification 三组件和跨 episode 复用；本地技能是结构化工具计划，不是 Mineflayer JavaScript，未运行 Minecraft、GPT-4 与 embedding retrieval。  终身学习 Agent 记忆与技能：让经验可取回、可失效 本地结构化计划技能能否当成 Mineflayer JavaScript 程序库？ 不能。本地保留 curriculum、技能与 verification 三组件及跨 episode 复用，但技能是结构化工具计划，未运行 Minecraft、GPT-4 或 embedding 检索。受控重试计数不代表真实程序调试，不能移用原文物品数和探索距离增幅。 例如计划模板复用成功不说明系统能处理 Mineflayer 的异步移动报错，更不说明已经在新世界获得相同科技树收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cf860a830a3dce6b">本地结构化计划技能能否当成 Mineflayer JavaScript 程序库？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Avoyager">Voyager</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NVIDIA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地保留 curriculum、技能与 verification 三组件及跨 episode 复用，但技能是结构化工具计划，未运行 Minecraft、GPT-4 或 embedding 检索。受控重试计数不代表真实程序调试，不能移用原文物品数和探索距离增幅。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如计划模板复用成功不说明系统能处理 Mineflayer 的异步移动报错，更不说明已经在新世界获得相同科技树收益。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16291">原论文</a> · <a href="../../../../agent-research/2305.16291-voyager/">实现解读</a> · <a href="#qa-cf860a830a3dce6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:generative-agents" data-paper-title="Generative Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Generative Agents Agent Stanford University 2023-04-07 只把完整历史塞给 LLM 无法支撑长期一致行为。论文把每次观察写入 memory stream，按 recency、importance、relevance 检索；累计重要事件达到阈值后生成更高层 reflection，再结合记忆与当前状态制定日程和行动计划。 本页实现 memory stream 的相关性/近期性/重要性检索、累计重要性触发反思，以及用检索记忆生成计划。复现记忆打分、反思触发和计划依赖；没有运行 25 个 LLM persona、Smallville 地图或人类可信度评测，因此这里只比较执行成功率、上下文代理成本和内部状态。EvoMem mini 120 episodes、seed 42、memory size 24，采用三项打分取 top-3，并按累计重要性合成 reflection。  记忆与反思 Agent 记忆与技能：让经验可取回、可失效 reflection 与直接记下一次观察有什么区别？ 观察是具体事件，reflection 从多条重要记忆形成较高层推断，再参与后续检索与计划。它提供跨事件概括，但推断可能错误，不能把模型反思当事实来源；原观察仍应可追踪，计划也需与当前状态一致。 例如几次观察到同一人帮忙后生成“他乐于合作”的反思，这是概括而非新发生的客观事件，需要保留支持记录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<span id="paper-agent-research-generative-agents-beb05f66" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f33684b6de1a3530">reflection 与直接记下一次观察有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agenerative-agents">Generative Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>观察是具体事件，reflection 从多条重要记忆形成较高层推断，再参与后续检索与计划。它提供跨事件概括，但推断可能错误，不能把模型反思当事实来源；原观察仍应可追踪，计划也需与当前状态一致。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如几次观察到同一人帮忙后生成“他乐于合作”的反思，这是概括而非新发生的客观事件，需要保留支持记录。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.03442">原论文</a> · <a href="../../../../agent-research/2304.03442-generative-agents/">实现解读</a> · <a href="#qa-f33684b6de1a3530">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:generative-agents" data-paper-title="Generative Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Generative Agents Agent Stanford University 2023-04-07 只把完整历史塞给 LLM 无法支撑长期一致行为。论文把每次观察写入 memory stream，按 recency、importance、relevance 检索；累计重要事件达到阈值后生成更高层 reflection，再结合记忆与当前状态制定日程和行动计划。 本页实现 memory stream 的相关性/近期性/重要性检索、累计重要性触发反思，以及用检索记忆生成计划。复现记忆打分、反思触发和计划依赖；没有运行 25 个 LLM persona、Smallville 地图或人类可信度评测，因此这里只比较执行成功率、上下文代理成本和内部状态。EvoMem mini 120 episodes、seed 42、memory size 24，采用三项打分取 top-3，并按累计重要性合成 reflection。  记忆与反思 Agent 记忆与技能：让经验可取回、可失效 高 importance 的旧事件为什么不该自动取代与当前问题更相关的记忆？ 重要性衡量对长期行为的意义，相关性衡量当前查询匹配，近期性又处理时间衰减，三者承担不同角色。反思把多件重要经历抽象成高层认识，但行动仍需结合当前状态；只按某一项检索会偏向永远重复大事件或只看最新闲聊。 例如搬家很重要，但问今天约饭地点时，昨晚确认的餐厅更直接相关；综合排序才能兼顾长期背景和当前细节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">核心机制</p>
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
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:generative-agents" data-paper-title="Generative Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Generative Agents Agent Stanford University 2023-04-07 只把完整历史塞给 LLM 无法支撑长期一致行为。论文把每次观察写入 memory stream，按 recency、importance、relevance 检索；累计重要事件达到阈值后生成更高层 reflection，再结合记忆与当前状态制定日程和行动计划。 本页实现 memory stream 的相关性/近期性/重要性检索、累计重要性触发反思，以及用检索记忆生成计划。复现记忆打分、反思触发和计划依赖；没有运行 25 个 LLM persona、Smallville 地图或人类可信度评测，因此这里只比较执行成功率、上下文代理成本和内部状态。EvoMem mini 120 episodes、seed 42、memory size 24，采用三项打分取 top-3，并按累计重要性合成 reflection。  记忆与反思 Agent 记忆与技能：让经验可取回、可失效 recency、importance、relevance 三项为何不能只留其中一项？ 近期性偏向新信息，重要性保留对长期行为影响大的事件，相关性根据当前问题筛选。只按近期性会遗忘旧承诺，只按重要性可能总提无关大事，只按相关性又可能忽视时间变化；三者组合也仍需权重与任务验证。 例如旧日答应参加聚会很重要，今天的地点变化很新，当前计划需同时检索两者，而非只取最新闲聊。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-86aad2b622fd5b5f">recency、importance、relevance 三项为何不能只留其中一项？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agenerative-agents">Generative Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>近期性偏向新信息，重要性保留对长期行为影响大的事件，相关性根据当前问题筛选。只按近期性会遗忘旧承诺，只按重要性可能总提无关大事，只按相关性又可能忽视时间变化；三者组合也仍需权重与任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧日答应参加聚会很重要，今天的地点变化很新，当前计划需同时检索两者，而非只取最新闲聊。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.03442">原论文</a> · <a href="../../../../agent-research/2304.03442-generative-agents/">实现解读</a> · <a href="#qa-86aad2b622fd5b5f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:generative-agents" data-paper-title="Generative Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/memory-and-skills" data-search="Generative Agents Agent Stanford University 2023-04-07 只把完整历史塞给 LLM 无法支撑长期一致行为。论文把每次观察写入 memory stream，按 recency、importance、relevance 检索；累计重要事件达到阈值后生成更高层 reflection，再结合记忆与当前状态制定日程和行动计划。 本页实现 memory stream 的相关性/近期性/重要性检索、累计重要性触发反思，以及用检索记忆生成计划。复现记忆打分、反思触发和计划依赖；没有运行 25 个 LLM persona、Smallville 地图或人类可信度评测，因此这里只比较执行成功率、上下文代理成本和内部状态。EvoMem mini 120 episodes、seed 42、memory size 24，采用三项打分取 top-3，并按累计重要性合成 reflection。  记忆与反思 Agent 记忆与技能：让经验可取回、可失效 本地反思触发计数是否包含二十五个 LLM persona 的社会行为评测？ 没有。本地用受控 EvoMem 三项打分和累计重要性阈值验证检索、反思与计划依赖，没有 Smallville 地图、真实 persona 或人类可信度评审。反思数量和代理成本只能说明机制运行，不能当成关系形成或协同行为可信度。 例如累计分达到阈值生成一条规则反思，不代表多个模型会真实传播邀请或自主协调聚会。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 记忆与技能：让经验可取回、可失效</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-77326fa7f7760be0">本地反思触发计数是否包含二十五个 LLM persona 的社会行为评测？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agenerative-agents">Generative Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地用受控 EvoMem 三项打分和累计重要性阈值验证检索、反思与计划依赖，没有 Smallville 地图、真实 persona 或人类可信度评审。反思数量和代理成本只能说明机制运行，不能当成关系形成或协同行为可信度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如累计分达到阈值生成一条规则反思，不代表多个模型会真实传播邀请或自主协调聚会。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2304.03442">原论文</a> · <a href="../../../../agent-research/2304.03442-generative-agents/">实现解读</a> · <a href="#qa-77326fa7f7760be0">问题链接</a></p>
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
