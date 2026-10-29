---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 工具与协作执行：把计划变成可检查的动作

[Agent](index.md) / 197 个问题 · 49 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

[阅读本主题精读卡片：多篇论文对比、分析与问答](../../deep-dives/agent-research/tools-and-collaboration.md)

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
<p class="ar-learning-status" data-learning-status role="status">197 个问题 · 49 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rpl" data-paper-title="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning Agent KAIST AI / Meta Superintelligence Labs 2026-10-17 固定检索pipeline把召回数量、融合和返回上下文绑在一起。RPL让策略生成短程序组合稀疏/稠密召回、RRF、去重和重排，只将显式打印的证据交回模型。为解决稀疏奖励难探索的问题，保留策略已有query，对最后一次检索程序做受语法约束的结构变异；执行核验通过后生成续写轨迹，再穿插蒸馏与RL。§3及附录B 成本过高，不复现（审查 DONE）；RetrievalProgram最多4个不同query，宽度取论文阶梯，最多20篇显式输出；execute只解释数据类并调用注入的SDK，不解析或执行Python源码。多路检索实际执行RRF，单路、列表内部或跨路遇到相同ID不同内容时统一拒绝，只有内容完全一致的重复才去重；重排不得注入召回外文档。RRF常数60是明确的本地惯例；输出是文档数上限，不是假装实现了论文2048-token观测限制。  检索与工具 可编程检索与结构变异 Agent 工具与协作执行：把计划变成可检查的动作 可编程检索为什么只把显式打印的文档交回模型？ 召回、融合、去重和重排可在程序内处理较大候选池，但模型上下文只接收最终明确输出。这样把检索计算与观察预算解耦；若把所有中间召回暗中拼回上下文，就绕过了程序选择和预算，不能声称相同检索策略。 例如稠密召回五十篇、重排后打印三篇，模型只应看到三篇，而不是同时读取隐藏的其余四十七篇。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-rpl-95ce1341" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-96cfb6b806b00ac8">可编程检索为什么只把显式打印的文档交回模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arpl">Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI / Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>召回、融合、去重和重排可在程序内处理较大候选池，但模型上下文只接收最终明确输出。这样把检索计算与观察预算解耦；若把所有中间召回暗中拼回上下文，就绕过了程序选择和预算，不能声称相同检索策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如稠密召回五十篇、重排后打印三篇，模型只应看到三篇，而不是同时读取隐藏的其余四十七篇。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24854">原论文</a> · <a href="../../../../agent-research/2610.24854-rpl/">实现解读</a> · <a href="#qa-96cfb6b806b00ac8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rpl" data-paper-title="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning Agent KAIST AI / Meta Superintelligence Labs 2026-10-17 固定检索pipeline把召回数量、融合和返回上下文绑在一起。RPL让策略生成短程序组合稀疏/稠密召回、RRF、去重和重排，只将显式打印的证据交回模型。为解决稀疏奖励难探索的问题，保留策略已有query，对最后一次检索程序做受语法约束的结构变异；执行核验通过后生成续写轨迹，再穿插蒸馏与RL。§3及附录B 成本过高，不复现（审查 DONE）；RetrievalProgram最多4个不同query，宽度取论文阶梯，最多20篇显式输出；execute只解释数据类并调用注入的SDK，不解析或执行Python源码。多路检索实际执行RRF，单路、列表内部或跨路遇到相同ID不同内容时统一拒绝，只有内容完全一致的重复才去重；重排不得注入召回外文档。RRF常数60是明确的本地惯例；输出是文档数上限，不是假装实现了论文2048-token观测限制。  检索与工具 可编程检索与结构变异 Agent 工具与协作执行：把计划变成可检查的动作 为什么答案错误时仍可能保留检索程序监督，却屏蔽答案 span？ 程序可通过语法与执行核验，说明检索组合本身值得学习，最终答案错误不必把全部结构监督一并丢掉。反之，保留错误答案会教坏生成行为；程序或续写 actor 也不能看到 verifier 的 gold，环境观察不应被当成策略自己生成的训练 token。 例如程序正确融合两路召回并去重，回答器却抄错日期，可保留检索步骤训练而遮掉错误日期的答案监督。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-387614f0d3ed6061">为什么答案错误时仍可能保留检索程序监督，却屏蔽答案 span？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arpl">Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI / Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>程序可通过语法与执行核验，说明检索组合本身值得学习，最终答案错误不必把全部结构监督一并丢掉。反之，保留错误答案会教坏生成行为；程序或续写 actor 也不能看到 verifier 的 gold，环境观察不应被当成策略自己生成的训练 token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如程序正确融合两路召回并去重，回答器却抄错日期，可保留检索步骤训练而遮掉错误日期的答案监督。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24854">原论文</a> · <a href="../../../../agent-research/2610.24854-rpl/">实现解读</a> · <a href="#qa-387614f0d3ed6061">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rpl" data-paper-title="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning Agent KAIST AI / Meta Superintelligence Labs 2026-10-17 固定检索pipeline把召回数量、融合和返回上下文绑在一起。RPL让策略生成短程序组合稀疏/稠密召回、RRF、去重和重排，只将显式打印的证据交回模型。为解决稀疏奖励难探索的问题，保留策略已有query，对最后一次检索程序做受语法约束的结构变异；执行核验通过后生成续写轨迹，再穿插蒸馏与RL。§3及附录B 成本过高，不复现（审查 DONE）；RetrievalProgram最多4个不同query，宽度取论文阶梯，最多20篇显式输出；execute只解释数据类并调用注入的SDK，不解析或执行Python源码。多路检索实际执行RRF，单路、列表内部或跨路遇到相同ID不同内容时统一拒绝，只有内容完全一致的重复才去重；重排不得注入召回外文档。RRF常数60是明确的本地惯例；输出是文档数上限，不是假装实现了论文2048-token观测限制。  检索与工具 可编程检索与结构变异 Agent 工具与协作执行：把计划变成可检查的动作 结构变异保留原 query 与重新让模型生成全新查询有什么区别？ 保留策略已有 query，把探索集中在召回模态、宽度、融合和重排结构，便于区分程序组织的作用；全新 query 同时改变语义与控制流。局部变异可能探索受限，但不能用 gold 直接编出正确文档作为所谓变异结果。 例如原查询不变，把召回从三扩到五可检验宽度是否补证据；若同时换成答案关键词，就混入另一种改进。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-82a8516fcb0b64ae">结构变异保留原 query 与重新让模型生成全新查询有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arpl">Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI / Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>保留策略已有 query，把探索集中在召回模态、宽度、融合和重排结构，便于区分程序组织的作用；全新 query 同时改变语义与控制流。局部变异可能探索受限，但不能用 gold 直接编出正确文档作为所谓变异结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原查询不变，把召回从三扩到五可检验宽度是否补证据；若同时换成答案关键词，就混入另一种改进。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24854">原论文</a> · <a href="../../../../agent-research/2610.24854-rpl/">实现解读</a> · <a href="#qa-82a8516fcb0b64ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rpl" data-paper-title="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning Agent KAIST AI / Meta Superintelligence Labs 2026-10-17 固定检索pipeline把召回数量、融合和返回上下文绑在一起。RPL让策略生成短程序组合稀疏/稠密召回、RRF、去重和重排，只将显式打印的证据交回模型。为解决稀疏奖励难探索的问题，保留策略已有query，对最后一次检索程序做受语法约束的结构变异；执行核验通过后生成续写轨迹，再穿插蒸馏与RL。§3及附录B 成本过高，不复现（审查 DONE）；RetrievalProgram最多4个不同query，宽度取论文阶梯，最多20篇显式输出；execute只解释数据类并调用注入的SDK，不解析或执行Python源码。多路检索实际执行RRF，单路、列表内部或跨路遇到相同ID不同内容时统一拒绝，只有内容完全一致的重复才去重；重排不得注入召回外文档。RRF常数60是明确的本地惯例；输出是文档数上限，不是假装实现了论文2048-token观测限制。  检索与工具 可编程检索与结构变异 Agent 工具与协作执行：把计划变成可检查的动作 Meta公开RPL完整代码后，本地typed-program组件就自动变成完整复现了吗？ 不会。官方源码发布只改变来源可核验性；本地仍未运行神经检索器、跨轮Python状态、策略生成、GRPO或蒸馏训练。还要遵循主项目CC-BY-NC与vendored部分各自许可，不因仓库可见就自动复制或升级能力证据。 教学例：拿到完整工厂图纸，不等于已有的小型管道模拟器已经生产出同样产品；必须另验真实执行链路和成本。 2026-10-29">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-908c2d6b9d2abe39">Meta公开RPL完整代码后，本地typed-program组件就自动变成完整复现了吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arpl">Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-29 · KAIST AI / Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不会。官方源码发布只改变来源可核验性；本地仍未运行神经检索器、跨轮Python状态、策略生成、GRPO或蒸馏训练。还要遵循主项目CC-BY-NC与vendored部分各自许可，不因仓库可见就自动复制或升级能力证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：拿到完整工厂图纸，不等于已有的小型管道模拟器已经生产出同样产品；必须另验真实执行链路和成本。</p>
<p class="ar-learning-sources">依据：论文信息、背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24854">原论文</a> · <a href="../../../../agent-research/2610.24854-rpl/">实现解读</a> · <a href="#qa-908c2d6b9d2abe39">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rpl" data-paper-title="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning Agent KAIST AI / Meta Superintelligence Labs 2026-10-17 固定检索pipeline把召回数量、融合和返回上下文绑在一起。RPL让策略生成短程序组合稀疏/稠密召回、RRF、去重和重排，只将显式打印的证据交回模型。为解决稀疏奖励难探索的问题，保留策略已有query，对最后一次检索程序做受语法约束的结构变异；执行核验通过后生成续写轨迹，再穿插蒸馏与RL。§3及附录B 成本过高，不复现（审查 DONE）；RetrievalProgram最多4个不同query，宽度取论文阶梯，最多20篇显式输出；execute只解释数据类并调用注入的SDK，不解析或执行Python源码。多路检索实际执行RRF，单路、列表内部或跨路遇到相同ID不同内容时统一拒绝，只有内容完全一致的重复才去重；重排不得注入召回外文档。RRF常数60是明确的本地惯例；输出是文档数上限，不是假装实现了论文2048-token观测限制。  检索与工具 可编程检索与结构变异 Agent 工具与协作执行：把计划变成可检查的动作 本地 RPL 的受限程序怎样控制召回规模、融合和最终输出？ 程序最多使用四个不同 query，召回与重排宽度取规定阶梯，多路召回要实际融合，并限制显式打印的文档数量。同 ID 异内容统一拒绝，重排不能注入召回外文档。本地只解释数据类和注入 SDK，文档数预算也不等于原文 token 限制或任意 Python 执行能力。 教学例：召回二十条再打印三条是合法的计算与观察分离；若重排偷偷补入一条未召回文档，就破坏了证据来源合同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a5e7b293a86bb7f2">本地 RPL 的受限程序怎样控制召回规模、融合和最终输出？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arpl">Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · KAIST AI / Meta Superintelligence Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>程序最多使用四个不同 query，召回与重排宽度取规定阶梯，多路召回要实际融合，并限制显式打印的文档数量。同 ID 异内容统一拒绝，重排不能注入召回外文档。本地只解释数据类和注入 SDK，文档数预算也不等于原文 token 限制或任意 Python 执行能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：召回二十条再打印三条是合法的计算与观察分离；若重排偷偷补入一条未召回文档，就破坏了证据来源合同。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本与复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24854">原论文</a> · <a href="../../../../agent-research/2610.24854-rpl/">实现解读</a> · <a href="#qa-a5e7b293a86bb7f2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:world-of-swecraft" data-paper-title="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds Agent Massachusetts Institute of Technology 2026-10-16 传统代码Agent评测通常分配一个预定义issue，难以衡量多个维护者如何自主找任务、分工和跨仓库改进。Software World由真实依赖库构成，让Agent用持久记忆、issue、PR和发布进行长期协作，以不可见的下游包检查群体产出是否真正有用。SW-Env用Harbor会话和Forgejo模拟软件维护环境，通信权限、仓库所有权与会话预算可独立控制；SW-Eval在隐藏依赖包上安装冻结版本，测正确性与指令计数，避免只优化自己看到的微基准。多会话持久状态不是无限增长的单条对话。 仅研究资料，成本过高，不复现（审查 DONE）。仅研究资料，成本过高，不复现（审查 DONE）。没有本地软件世界、Agent实验或能力指标。完整复现需要多仓库构建、隔离部署、代码执行沙箱、真实模型会话及大量隐藏下游评测；原论文规模已明显超过单卡A100/A30与Mac低成本预算。成本过高，不复现（审查 DONE）。不克隆和执行未知项目脚本、不伪造本地Agent成绩、不保留自动运行队列，也不宣称Evolve已接入。  多Agent协作 软件生态与自进化评测 Agent 工具与协作执行：把计划变成可检查的动作 World of SWEcraft 为什么把软件任务扩展成多个维护者共同演进的包生态？ 单个 Agent 修一个已给定 issue，不能完整反映跨项目依赖与多人维护的长期影响。World of SWEcraft 让维护者持续改变各自软件包，改动会影响下游使用者，因而需要兼顾本地进展和协作交付。群体活动多不代表生态更好，应由实际下游功能与资源结果检验。 教学例：一个包升级函数签名后，自己的测试通过，下游两个包却无法导入；这类跨维护者后果正是单 issue 测试不易覆盖的。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-world-of-swecraft-5a1942f1" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-10201c0f398592ac">World of SWEcraft 为什么把软件任务扩展成多个维护者共同演进的包生态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aworld-of-swecraft">World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>单个 Agent 修一个已给定 issue，不能完整反映跨项目依赖与多人维护的长期影响。World of SWEcraft 让维护者持续改变各自软件包，改动会影响下游使用者，因而需要兼顾本地进展和协作交付。群体活动多不代表生态更好，应由实际下游功能与资源结果检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一个包升级函数签名后，自己的测试通过，下游两个包却无法导入；这类跨维护者后果正是单 issue 测试不易覆盖的。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24061v1">原论文</a> · <a href="../../../../agent-research/2610.24061-world-of-swecraft/">实现解读</a> · <a href="#qa-10201c0f398592ac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:world-of-swecraft" data-paper-title="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds Agent Massachusetts Institute of Technology 2026-10-16 传统代码Agent评测通常分配一个预定义issue，难以衡量多个维护者如何自主找任务、分工和跨仓库改进。Software World由真实依赖库构成，让Agent用持久记忆、issue、PR和发布进行长期协作，以不可见的下游包检查群体产出是否真正有用。SW-Env用Harbor会话和Forgejo模拟软件维护环境，通信权限、仓库所有权与会话预算可独立控制；SW-Eval在隐藏依赖包上安装冻结版本，测正确性与指令计数，避免只优化自己看到的微基准。多会话持久状态不是无限增长的单条对话。 仅研究资料，成本过高，不复现（审查 DONE）。仅研究资料，成本过高，不复现（审查 DONE）。没有本地软件世界、Agent实验或能力指标。完整复现需要多仓库构建、隔离部署、代码执行沙箱、真实模型会话及大量隐藏下游评测；原论文规模已明显超过单卡A100/A30与Mac低成本预算。成本过高，不复现（审查 DONE）。不克隆和执行未知项目脚本、不伪造本地Agent成绩、不保留自动运行队列，也不宣称Evolve已接入。  多Agent协作 软件生态与自进化评测 Agent 工具与协作执行：把计划变成可检查的动作 为什么用隐藏下游包验证群体改进，而不只运行 Agent 自己维护的微基准？ 群体可能优化已见基准的特例，却破坏真实依赖者。冻结版本在不可见下游安装与检查，能检验公共产物的兼容性和收益；失败任务必须按既定 strict 或 carry 规则处理，不能删掉后再平均，指令计数收益也不能冒充墙钟加速。 例如库把某函数针对自测输入特化，微基准很快却令下游解析器失败；隐藏依赖检查会暴露这种局部优化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ac28edabd2d0ac9a">为什么用隐藏下游包验证群体改进，而不只运行 Agent 自己维护的微基准？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aworld-of-swecraft">World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>群体可能优化已见基准的特例，却破坏真实依赖者。冻结版本在不可见下游安装与检查，能检验公共产物的兼容性和收益；失败任务必须按既定 strict 或 carry 规则处理，不能删掉后再平均，指令计数收益也不能冒充墙钟加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如库把某函数针对自测输入特化，微基准很快却令下游解析器失败；隐藏依赖检查会暴露这种局部优化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24061v1">原论文</a> · <a href="../../../../agent-research/2610.24061-world-of-swecraft/">实现解读</a> · <a href="#qa-ac28edabd2d0ac9a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:world-of-swecraft" data-paper-title="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds Agent Massachusetts Institute of Technology 2026-10-16 传统代码Agent评测通常分配一个预定义issue，难以衡量多个维护者如何自主找任务、分工和跨仓库改进。Software World由真实依赖库构成，让Agent用持久记忆、issue、PR和发布进行长期协作，以不可见的下游包检查群体产出是否真正有用。SW-Env用Harbor会话和Forgejo模拟软件维护环境，通信权限、仓库所有权与会话预算可独立控制；SW-Eval在隐藏依赖包上安装冻结版本，测正确性与指令计数，避免只优化自己看到的微基准。多会话持久状态不是无限增长的单条对话。 仅研究资料，成本过高，不复现（审查 DONE）。仅研究资料，成本过高，不复现（审查 DONE）。没有本地软件世界、Agent实验或能力指标。完整复现需要多仓库构建、隔离部署、代码执行沙箱、真实模型会话及大量隐藏下游评测；原论文规模已明显超过单卡A100/A30与Mac低成本预算。成本过高，不复现（审查 DONE）。不克隆和执行未知项目脚本、不伪造本地Agent成绩、不保留自动运行队列，也不宣称Evolve已接入。  多Agent协作 软件生态与自进化评测 Agent 工具与协作执行：把计划变成可检查的动作 持久多会话协作与单条无限长群聊有什么区别？ Agent 通过仓库、issue、PR、发布及持久记忆交接工作，会话权限与预算可控，信息不必都堆进同一对话。共享工件可跨会话保留，但也有协调、所有权和版本成本，不能把更多 Agent 或更大模型自动等同更高群体产出。 例如一名维护者发布新版后另一依赖库更新适配，协作通过版本工件发生，不要求所有历史聊天每轮同时可见。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ebc669cc7428ed58">持久多会话协作与单条无限长群聊有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aworld-of-swecraft">World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Agent 通过仓库、issue、PR、发布及持久记忆交接工作，会话权限与预算可控，信息不必都堆进同一对话。共享工件可跨会话保留，但也有协调、所有权和版本成本，不能把更多 Agent 或更大模型自动等同更高群体产出。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一名维护者发布新版后另一依赖库更新适配，协作通过版本工件发生，不要求所有历史聊天每轮同时可见。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24061v1">原论文</a> · <a href="../../../../agent-research/2610.24061-world-of-swecraft/">实现解读</a> · <a href="#qa-ebc669cc7428ed58">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:world-of-swecraft" data-paper-title="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds Agent Massachusetts Institute of Technology 2026-10-16 传统代码Agent评测通常分配一个预定义issue，难以衡量多个维护者如何自主找任务、分工和跨仓库改进。Software World由真实依赖库构成，让Agent用持久记忆、issue、PR和发布进行长期协作，以不可见的下游包检查群体产出是否真正有用。SW-Env用Harbor会话和Forgejo模拟软件维护环境，通信权限、仓库所有权与会话预算可独立控制；SW-Eval在隐藏依赖包上安装冻结版本，测正确性与指令计数，避免只优化自己看到的微基准。多会话持久状态不是无限增长的单条对话。 仅研究资料，成本过高，不复现（审查 DONE）。仅研究资料，成本过高，不复现（审查 DONE）。没有本地软件世界、Agent实验或能力指标。完整复现需要多仓库构建、隔离部署、代码执行沙箱、真实模型会话及大量隐藏下游评测；原论文规模已明显超过单卡A100/A30与Mac低成本预算。成本过高，不复现（审查 DONE）。不克隆和执行未知项目脚本、不伪造本地Agent成绩、不保留自动运行队列，也不宣称Evolve已接入。  多Agent协作 软件生态与自进化评测 Agent 工具与协作执行：把计划变成可检查的动作 strict 与 carry 在正确性失败轮的速度聚合如何不同？ strict 将失败包的任务速度比记为一，carry 沿用最近一次通过时的速度比；两者都保留全部任务分母，再取几何平均。指令计数收益不是墙钟加速，本地没有运行协作环境，仅公式实现也不能称复现 55K 会话研究。 例如某轮优化导致测试失败，不能删掉该包只平均成功项；carry 可以保留其前次有效表现，而非采用失败轮更快数值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3324ecfdacb047a6">strict 与 carry 在正确性失败轮的速度聚合如何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aworld-of-swecraft">World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>strict 将失败包的任务速度比记为一，carry 沿用最近一次通过时的速度比；两者都保留全部任务分母，再取几何平均。指令计数收益不是墙钟加速，本地没有运行协作环境，仅公式实现也不能称复现 55K 会话研究。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某轮优化导致测试失败，不能删掉该包只平均成功项；carry 可以保留其前次有效表现，而非采用失败轮更快数值。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与成本判断；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24061v1">原论文</a> · <a href="../../../../agent-research/2610.24061-world-of-swecraft/">实现解读</a> · <a href="#qa-3324ecfdacb047a6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:diviner" data-paper-title="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure Agent Meta 2026-10-15 生产事故的症状可能跨推荐、排序、数据、配置和算力服务传播。LLM 能调用工具并不代表它能可靠诊断：超时不等于无异常，历史相似事故不证明本次根因，事后总结也不能作为事故发生时的证据。原文 §4–5用 Encode／Execute／Evaluate／Adapt 四阶段闭环组织领域知识、Lead–worker 调查、事后审查和 owner 批准的知识更新。运行中只调整本次调查计划，不能自行发布新的共享工作流或执行缓解操作。 成本过高，不复现（审查 DONE），亦不伪造公开事故替代结论。这些是合同诊断，不是 RCA 成功率。component_only / L1 CPU 协议组件。实现证据接纳、假设状态与人工批准合同，不运行生产 RCA Agent，不进入 Evolve 晋级。每 seed 产生 24 个有来源的人工事件，随机化工具状态、可获得时间和数值。独立参考条件重算可接纳数；负对照把任何非空工具响应都当证据，从而保留错误接纳计数。另测未批准发布被拒和 owner 批准后版本前进。接口不接真实事故，也不生成根因答案。  工具使用与可靠性 生产事故诊断与证据治理 Agent 工具与协作执行：把计划变成可检查的动作 为什么事故诊断必须记录证据的可获得时间，而不只记录事件时间？ 事故发生时可能还拿不到后来汇总的日志或事后结论，使用它们会造成前视。Diviner 证据合同要求同事故、目标、窗口且 available time 不晚于 as-of，区分调查时可见材料与最终解释；结构合规仍不证明内容蕴含或真实根因。 例如十点发生的错误在十一点才生成汇总报告，十点半调查不能读取该报告，即使报告描述的事件时间是十点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-diviner-0cc63af7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ca9a7eaa53802c0f">为什么事故诊断必须记录证据的可获得时间，而不只记录事件时间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adiviner">Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>事故发生时可能还拿不到后来汇总的日志或事后结论，使用它们会造成前视。Diviner 证据合同要求同事故、目标、窗口且 available time 不晚于 as-of，区分调查时可见材料与最终解释；结构合规仍不证明内容蕴含或真实根因。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十点发生的错误在十一点才生成汇总报告，十点半调查不能读取该报告，即使报告描述的事件时间是十点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21281">原论文</a> · <a href="../../../../agent-research/2610.21281-diviner/">实现解读</a> · <a href="#qa-ca9a7eaa53802c0f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:diviner" data-paper-title="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure Agent Meta 2026-10-15 生产事故的症状可能跨推荐、排序、数据、配置和算力服务传播。LLM 能调用工具并不代表它能可靠诊断：超时不等于无异常，历史相似事故不证明本次根因，事后总结也不能作为事故发生时的证据。原文 §4–5用 Encode／Execute／Evaluate／Adapt 四阶段闭环组织领域知识、Lead–worker 调查、事后审查和 owner 批准的知识更新。运行中只调整本次调查计划，不能自行发布新的共享工作流或执行缓解操作。 成本过高，不复现（审查 DONE），亦不伪造公开事故替代结论。这些是合同诊断，不是 RCA 成功率。component_only / L1 CPU 协议组件。实现证据接纳、假设状态与人工批准合同，不运行生产 RCA Agent，不进入 Evolve 晋级。每 seed 产生 24 个有来源的人工事件，随机化工具状态、可获得时间和数值。独立参考条件重算可接纳数；负对照把任何非空工具响应都当证据，从而保留错误接纳计数。另测未批准发布被拒和 owner 批准后版本前进。接口不接真实事故，也不生成根因答案。  工具使用与可靠性 生产事故诊断与证据治理 Agent 工具与协作执行：把计划变成可检查的动作 工具超时为什么既不能支持、也不能反驳根因假设？ 超时说明未取得有效观察，不代表被测服务正常或异常。证据还需匹配事故、目标、时间窗口及当时可获得性，历史相似案例也只是线索；调查计划可在本轮调整，持久工作流发布和缓解执行则是不同权限，不能由一次自动诊断直接越过。 例如查询排序服务日志超时，不能据此写“没有排序异常”；应标记未知并换取证方式，也不能用事故后总结倒灌当前证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a9cacdbf91e3b740">工具超时为什么既不能支持、也不能反驳根因假设？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adiviner">Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>超时说明未取得有效观察，不代表被测服务正常或异常。证据还需匹配事故、目标、时间窗口及当时可获得性，历史相似案例也只是线索；调查计划可在本轮调整，持久工作流发布和缓解执行则是不同权限，不能由一次自动诊断直接越过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如查询排序服务日志超时，不能据此写“没有排序异常”；应标记未知并换取证方式，也不能用事故后总结倒灌当前证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21281">原论文</a> · <a href="../../../../agent-research/2610.21281-diviner/">实现解读</a> · <a href="#qa-a9cacdbf91e3b740">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:diviner" data-paper-title="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure Agent Meta 2026-10-15 生产事故的症状可能跨推荐、排序、数据、配置和算力服务传播。LLM 能调用工具并不代表它能可靠诊断：超时不等于无异常，历史相似事故不证明本次根因，事后总结也不能作为事故发生时的证据。原文 §4–5用 Encode／Execute／Evaluate／Adapt 四阶段闭环组织领域知识、Lead–worker 调查、事后审查和 owner 批准的知识更新。运行中只调整本次调查计划，不能自行发布新的共享工作流或执行缓解操作。 成本过高，不复现（审查 DONE），亦不伪造公开事故替代结论。这些是合同诊断，不是 RCA 成功率。component_only / L1 CPU 协议组件。实现证据接纳、假设状态与人工批准合同，不运行生产 RCA Agent，不进入 Evolve 晋级。每 seed 产生 24 个有来源的人工事件，随机化工具状态、可获得时间和数值。独立参考条件重算可接纳数；负对照把任何非空工具响应都当证据，从而保留错误接纳计数。另测未批准发布被拒和 owner 批准后版本前进。接口不接真实事故，也不生成根因答案。  工具使用与可靠性 生产事故诊断与证据治理 Agent 工具与协作执行：把计划变成可检查的动作 运行中调查适应与发布持久知识为什么采用不同治理边界？ 当前调查可根据新证据调整计划，影响范围限本次；共享工作流和知识会影响未来事故，需下一版本、重放验证和 artifact owner 批准。论文不授权自主缓解生产系统，也不能把观测性 MTTR 差异解释为随机因果效果。 例如本次临时增加配置查询可以直接用于调查，改写全团队通用排障流程则要经独立验证和 owner 发布。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1ac48fe99644b2db">运行中调查适应与发布持久知识为什么采用不同治理边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adiviner">Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>当前调查可根据新证据调整计划，影响范围限本次；共享工作流和知识会影响未来事故，需下一版本、重放验证和 artifact owner 批准。论文不授权自主缓解生产系统，也不能把观测性 MTTR 差异解释为随机因果效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如本次临时增加配置查询可以直接用于调查，改写全团队通用排障流程则要经独立验证和 owner 发布。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21281">原论文</a> · <a href="../../../../agent-research/2610.21281-diviner/">实现解读</a> · <a href="#qa-1ac48fe99644b2db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:diviner" data-paper-title="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure Agent Meta 2026-10-15 生产事故的症状可能跨推荐、排序、数据、配置和算力服务传播。LLM 能调用工具并不代表它能可靠诊断：超时不等于无异常，历史相似事故不证明本次根因，事后总结也不能作为事故发生时的证据。原文 §4–5用 Encode／Execute／Evaluate／Adapt 四阶段闭环组织领域知识、Lead–worker 调查、事后审查和 owner 批准的知识更新。运行中只调整本次调查计划，不能自行发布新的共享工作流或执行缓解操作。 成本过高，不复现（审查 DONE），亦不伪造公开事故替代结论。这些是合同诊断，不是 RCA 成功率。component_only / L1 CPU 协议组件。实现证据接纳、假设状态与人工批准合同，不运行生产 RCA Agent，不进入 Evolve 晋级。每 seed 产生 24 个有来源的人工事件，随机化工具状态、可获得时间和数值。独立参考条件重算可接纳数；负对照把任何非空工具响应都当证据，从而保留错误接纳计数。另测未批准发布被拒和 owner 批准后版本前进。接口不接真实事故，也不生成根因答案。  工具使用与可靠性 生产事故诊断与证据治理 Agent 工具与协作执行：把计划变成可检查的动作 事故证据进入 EvidenceLedger 前，需要绑定哪些身份和时间边界？ 记录需要对应当前事故、目标、调查时间窗口，并区分事件何时发生与证据何时可获得；可获得时间不得晚于本次 as-of。缺少这些约束，其他服务日志或事后总结都可能被误当成当时证据。本地只校验这些来源合同和治理 gate，不据此生成或证明真实根因。 教学例：凌晨的异常日志直到早上才汇总，不能用于声称凌晨调查已经掌握它；另一事故的同名报错也不能直接混入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f0e7a7715b53924c">事故证据进入 EvidenceLedger 前，需要绑定哪些身份和时间边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adiviner">Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>记录需要对应当前事故、目标、调查时间窗口，并区分事件何时发生与证据何时可获得；可获得时间不得晚于本次 as-of。缺少这些约束，其他服务日志或事后总结都可能被误当成当时证据。本地只校验这些来源合同和治理 gate，不据此生成或证明真实根因。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：凌晨的异常日志直到早上才汇总，不能用于声称凌晨调查已经掌握它；另一事故的同名报错也不能直接混入。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21281">原论文</a> · <a href="../../../../agent-research/2610.21281-diviner/">实现解读</a> · <a href="#qa-f0e7a7715b53924c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gemini-minecraft" data-paper-title="A team of Gemini 4 Argon agents beats Minecraft" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="A team of Gemini 4 Argon agents beats Minecraft Agent Google DeepMind 2026-10-15 四个执行 Agent 通过编写 JavaScript 程序操纵 Mineflayer 角色；Observer 汇总世界状态，聊天和笔记传递进度。研究重点是长期协作、程序化工具与持久状态，而不是新训练目标。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地执行 Agent、游戏成功率或 GPU 验证，不接入 Evolve。无本地 capability 指标、训练结果或 Evolve 算子；不创建虚构成功回执。范围见本批验收合同。只完成资料、原图和成本审查，不调用商业模型或运行游戏。原文长时交互超过本轮单卡/本地预算，完整实验标注成本过高，不复现（审查 DONE）。  多 Agent 协作 长期规划与工具使用 Agent 工具与协作执行：把计划变成可检查的动作 Minecraft 长程通关为什么适合研究团队协作，而不只是单次指令跟随？ 通关涉及探索、资源收集、制作与战斗，多个目标在时间和资源上相互依赖，执行还会不断遇到新状态。该工作研究多 Agent 分工、观察与共享信息如何支撑长期推进。一次完整通关可展示系统能做什么，但不能由单次记录推导成功概率或单独模块的因果收益。 教学例：一名角色采矿、另一名收集食物，进展必须协调；若采矿者实际未拿到材料，共享笔记写“已完成”也不能完成制作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-gemini-minecraft-c1e2611e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e601316159b12b01">Minecraft 长程通关为什么适合研究团队协作，而不只是单次指令跟随？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agemini-minecraft">A team of Gemini 4 Argon agents beats Minecraft</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>通关涉及探索、资源收集、制作与战斗，多个目标在时间和资源上相互依赖，执行还会不断遇到新状态。该工作研究多 Agent 分工、观察与共享信息如何支撑长期推进。一次完整通关可展示系统能做什么，但不能由单次记录推导成功概率或单独模块的因果收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一名角色采矿、另一名收集食物，进展必须协调；若采矿者实际未拿到材料，共享笔记写“已完成”也不能完成制作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22319">原论文</a> · <a href="../../../../agent-research/2610.22319-gemini-minecraft/">实现解读</a> · <a href="#qa-e601316159b12b01">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gemini-minecraft" data-paper-title="A team of Gemini 4 Argon agents beats Minecraft" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="A team of Gemini 4 Argon agents beats Minecraft Agent Google DeepMind 2026-10-15 四个执行 Agent 通过编写 JavaScript 程序操纵 Mineflayer 角色；Observer 汇总世界状态，聊天和笔记传递进度。研究重点是长期协作、程序化工具与持久状态，而不是新训练目标。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地执行 Agent、游戏成功率或 GPU 验证，不接入 Evolve。无本地 capability 指标、训练结果或 Evolve 算子；不创建虚构成功回执。范围见本批验收合同。只完成资料、原图和成本审查，不调用商业模型或运行游戏。原文长时交互超过本轮单卡/本地预算，完整实验标注成本过高，不复现（审查 DONE）。  多 Agent 协作 长期规划与工具使用 Agent 工具与协作执行：把计划变成可检查的动作 Observer 与共享笔记为什么不能替代每个执行 Agent 的真实环境反馈？ 汇总状态适合协调分工，但可能延迟或遗漏局部变化；执行程序仍需以世界实际返回判断成败。程序化动作、持久记录和多会话协作共同支持长程任务，不能仅因聊天中说已完成就推进依赖步骤，也不能把协作案例描述当作本地运行结果。 例如一名角色记下“桥已修好”，另一名过桥前仍可能看到桥被破坏；应依据当前观察修正计划，而非盲信旧笔记。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bec7e1165a81dee5">Observer 与共享笔记为什么不能替代每个执行 Agent 的真实环境反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agemini-minecraft">A team of Gemini 4 Argon agents beats Minecraft</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>汇总状态适合协调分工，但可能延迟或遗漏局部变化；执行程序仍需以世界实际返回判断成败。程序化动作、持久记录和多会话协作共同支持长程任务，不能仅因聊天中说已完成就推进依赖步骤，也不能把协作案例描述当作本地运行结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一名角色记下“桥已修好”，另一名过桥前仍可能看到桥被破坏；应依据当前观察修正计划，而非盲信旧笔记。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22319">原论文</a> · <a href="../../../../agent-research/2610.22319-gemini-minecraft/">实现解读</a> · <a href="#qa-bec7e1165a81dee5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gemini-minecraft" data-paper-title="A team of Gemini 4 Argon agents beats Minecraft" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="A team of Gemini 4 Argon agents beats Minecraft Agent Google DeepMind 2026-10-15 四个执行 Agent 通过编写 JavaScript 程序操纵 Mineflayer 角色；Observer 汇总世界状态，聊天和笔记传递进度。研究重点是长期协作、程序化工具与持久状态，而不是新训练目标。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地执行 Agent、游戏成功率或 GPU 验证，不接入 Evolve。无本地 capability 指标、训练结果或 Evolve 算子；不创建虚构成功回执。范围见本批验收合同。只完成资料、原图和成本审查，不调用商业模型或运行游戏。原文长时交互超过本轮单卡/本地预算，完整实验标注成本过高，不复现（审查 DONE）。  多 Agent 协作 长期规划与工具使用 Agent 工具与协作执行：把计划变成可检查的动作 四 Agent 协作与一个 Agent 单独长跑，成本和证据怎样比较？ 并行角色可分工探索与程序执行，也增加通信、重复工作和协调成本。原文是一个 Easy 随机世界的长时成功案例，没有多种子对照可支持可靠性或成本优势，不能把通关本身改写为四 Agent 普遍优于单 Agent。 例如四人同时采资源可能更快，也可能都去采同一种物品；一次成功未提供足够信息区分协作收益和额外计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a451cee9a3ff262f">四 Agent 协作与一个 Agent 单独长跑，成本和证据怎样比较？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agemini-minecraft">A team of Gemini 4 Argon agents beats Minecraft</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>并行角色可分工探索与程序执行，也增加通信、重复工作和协调成本。原文是一个 Easy 随机世界的长时成功案例，没有多种子对照可支持可靠性或成本优势，不能把通关本身改写为四 Agent 普遍优于单 Agent。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如四人同时采资源可能更快，也可能都去采同一种物品；一次成功未提供足够信息区分协作收益和额外计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22319">原论文</a> · <a href="../../../../agent-research/2610.22319-gemini-minecraft/">实现解读</a> · <a href="#qa-a451cee9a3ff262f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gemini-minecraft" data-paper-title="A team of Gemini 4 Argon agents beats Minecraft" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="A team of Gemini 4 Argon agents beats Minecraft Agent Google DeepMind 2026-10-15 四个执行 Agent 通过编写 JavaScript 程序操纵 Mineflayer 角色；Observer 汇总世界状态，聊天和笔记传递进度。研究重点是长期协作、程序化工具与持久状态，而不是新训练目标。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地执行 Agent、游戏成功率或 GPU 验证，不接入 Evolve。无本地 capability 指标、训练结果或 Evolve 算子；不创建虚构成功回执。范围见本批验收合同。只完成资料、原图和成本审查，不调用商业模型或运行游戏。原文长时交互超过本轮单卡/本地预算，完整实验标注成本过高，不复现（审查 DONE）。  多 Agent 协作 长期规划与工具使用 Agent 工具与协作执行：把计划变成可检查的动作 二十七小时通关记录能否写成 100% 成功率或本地可执行能力？ 不能。一次案例没有独立重复的成功率分母，约二万四千调用属于作者运行成本；本地仅收录资料和成本，没有商业模型调用、游戏执行、GPU 回执或 Evolve 算子。公式化交互记号也不是完成真实 Minecraft 系统。 例如一场游戏一次通关只能报告“一次成功案例”，不能列成十次均成功，也不能把原视频当本地运行 receipt。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e5f10c30d9efc8b8">二十七小时通关记录能否写成 100% 成功率或本地可执行能力？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agemini-minecraft">A team of Gemini 4 Argon agents beats Minecraft</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google DeepMind</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。一次案例没有独立重复的成功率分母，约二万四千调用属于作者运行成本；本地仅收录资料和成本，没有商业模型调用、游戏执行、GPU 回执或 Evolve 算子。公式化交互记号也不是完成真实 Minecraft 系统。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一场游戏一次通关只能报告“一次成功案例”，不能列成十次均成功，也不能把原视频当本地运行 receipt。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22319">原论文</a> · <a href="../../../../agent-research/2610.22319-gemini-minecraft/">实现解读</a> · <a href="#qa-e5f10c30d9efc8b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-agent-harness" data-paper-title="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs Agent University of Illinois Urbana-Champaign 2026-10-15 Agent 不需要每一步都让昂贵 LLM 生成长文本，但离线多选题高准确率也不保证闭环不出错。JevAgentHarness 在 agent 自己访问的 shadow trajectories 上，分别校准工具、参数等决策的委派阈值，低置信交回 LLM，并报告成功／费用／关键路径延迟。AgentDecision-4B 另用到达过的错误后状态训练，避免只模仿成功轨迹。原文 §2–4、附录 A/D 对单 A100/A30 或 Mac 的本轮预算，完整训练、真实工具任务和多臂评测成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现按决策类别拟合阈值、低置信回退及声明成本会计；没有 Jev／LLM 调用、AgentDecision-4B 训练或统一 Evolve 接入。每 seed 的低／高置信值随机化，40 行 shadow 数值 fixture 拟合不同阈值，在 12 个独立公共请求上实际调用概率 callback 或强模型 callback。负对照把阈值压低到 0.5，保留错误委派；NaN 输出触发回退；  工具使用与可靠性 System One/JEV置信委派与回退 Agent 工具与协作执行：把计划变成可检查的动作 Jev Agent Harness 为什么不把 Agent 的每次小判断都交给同样昂贵的推理？ 工具流程包含大量范围有限的判断，有些适合廉价决策器，有些需要继续推理。该研究关注如何在明确的决策接口中委派并保留回退，让节省调用与错误代价共同决定使用范围。便宜判断器并不自动适合开放任务，必须在它实际遇到的状态上检查可靠性。 教学例：是否保留一条候选记录可尝试廉价判断；涉及缺失证据的开放解释则可能仍需主模型，不能因两者都能输出是非就混用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-jev-agent-harness-91c2ebf3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6c94f465af04e5cf">Jev Agent Harness 为什么不把 Agent 的每次小判断都交给同样昂贵的推理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-agent-harness">JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具流程包含大量范围有限的判断，有些适合廉价决策器，有些需要继续推理。该研究关注如何在明确的决策接口中委派并保留回退，让节省调用与错误代价共同决定使用范围。便宜判断器并不自动适合开放任务，必须在它实际遇到的状态上检查可靠性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：是否保留一条候选记录可尝试廉价判断；涉及缺失证据的开放解释则可能仍需主模型，不能因两者都能输出是非就混用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21412">原论文</a> · <a href="../../../../agent-research/2610.21412-jev-agent-harness/">实现解读</a> · <a href="#qa-6c94f465af04e5cf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-agent-harness" data-paper-title="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs Agent University of Illinois Urbana-Champaign 2026-10-15 Agent 不需要每一步都让昂贵 LLM 生成长文本，但离线多选题高准确率也不保证闭环不出错。JevAgentHarness 在 agent 自己访问的 shadow trajectories 上，分别校准工具、参数等决策的委派阈值，低置信交回 LLM，并报告成功／费用／关键路径延迟。AgentDecision-4B 另用到达过的错误后状态训练，避免只模仿成功轨迹。原文 §2–4、附录 A/D 对单 A100/A30 或 Mac 的本轮预算，完整训练、真实工具任务和多臂评测成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现按决策类别拟合阈值、低置信回退及声明成本会计；没有 Jev／LLM 调用、AgentDecision-4B 训练或统一 Evolve 接入。每 seed 的低／高置信值随机化，40 行 shadow 数值 fixture 拟合不同阈值，在 12 个独立公共请求上实际调用概率 callback 或强模型 callback。负对照把阈值压低到 0.5，保留错误委派；NaN 输出触发回退；  工具使用与可靠性 System One/JEV置信委派与回退 Agent 工具与协作执行：把计划变成可检查的动作 为什么委派阈值要在 Agent 自己访问的 shadow trajectories 上按决策类型校准？ 真实闭环会到达错误后状态，离线干净多选题不覆盖这些输入；工具选择与参数选择的风险和收益也不同。配对比较决策模型与强模型，按任务价值和成本找可靠阈值，不确定或未见类别回退，才能把准确率、费用和延迟放进同一控制问题。 例如小模型选对工具却常把参数填错，两类决策应有不同委派条件；不能用一条整体准确率给全部调用统一放行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e9b8fa18e0639f8f">为什么委派阈值要在 Agent 自己访问的 shadow trajectories 上按决策类型校准？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-agent-harness">JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实闭环会到达错误后状态，离线干净多选题不覆盖这些输入；工具选择与参数选择的风险和收益也不同。配对比较决策模型与强模型，按任务价值和成本找可靠阈值，不确定或未见类别回退，才能把准确率、费用和延迟放进同一控制问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如小模型选对工具却常把参数填错，两类决策应有不同委派条件；不能用一条整体准确率给全部调用统一放行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21412">原论文</a> · <a href="../../../../agent-research/2610.21412-jev-agent-harness/">实现解读</a> · <a href="#qa-e9b8fa18e0639f8f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-agent-harness" data-paper-title="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs Agent University of Illinois Urbana-Champaign 2026-10-15 Agent 不需要每一步都让昂贵 LLM 生成长文本，但离线多选题高准确率也不保证闭环不出错。JevAgentHarness 在 agent 自己访问的 shadow trajectories 上，分别校准工具、参数等决策的委派阈值，低置信交回 LLM，并报告成功／费用／关键路径延迟。AgentDecision-4B 另用到达过的错误后状态训练，避免只模仿成功轨迹。原文 §2–4、附录 A/D 对单 A100/A30 或 Mac 的本轮预算，完整训练、真实工具任务和多臂评测成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现按决策类别拟合阈值、低置信回退及声明成本会计；没有 Jev／LLM 调用、AgentDecision-4B 训练或统一 Evolve 接入。每 seed 的低／高置信值随机化，40 行 shadow 数值 fixture 拟合不同阈值，在 12 个独立公共请求上实际调用概率 callback 或强模型 callback。负对照把阈值压低到 0.5，保留错误委派；NaN 输出触发回退；  工具使用与可靠性 System One/JEV置信委派与回退 Agent 工具与协作执行：把计划变成可检查的动作 按成本与任务价值选择阈值，与固定 0.7 自信门有什么区别？ 效用阈值比较 decision 与 strong 的配对正确性差和节省调用成本，寻找高置信区间都非负的 suffix。固定常量忽略类别、代价和过度自信；阈值拟合也非万能，原文保留校准失败及追加训练无收益的负结果。 例如某类错误代价很高，微小节费不足以接受准确率下降；另一类可恢复决策则可能容忍更低委派门槛。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d5e0239b2d9b5b36">按成本与任务价值选择阈值，与固定 0.7 自信门有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-agent-harness">JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>效用阈值比较 decision 与 strong 的配对正确性差和节省调用成本，寻找高置信区间都非负的 suffix。固定常量忽略类别、代价和过度自信；阈值拟合也非万能，原文保留校准失败及追加训练无收益的负结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某类错误代价很高，微小节费不足以接受准确率下降；另一类可恢复决策则可能容忍更低委派门槛。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21412">原论文</a> · <a href="../../../../agent-research/2610.21412-jev-agent-harness/">实现解读</a> · <a href="#qa-d5e0239b2d9b5b36">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-agent-harness" data-paper-title="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs Agent University of Illinois Urbana-Champaign 2026-10-15 Agent 不需要每一步都让昂贵 LLM 生成长文本，但离线多选题高准确率也不保证闭环不出错。JevAgentHarness 在 agent 自己访问的 shadow trajectories 上，分别校准工具、参数等决策的委派阈值，低置信交回 LLM，并报告成功／费用／关键路径延迟。AgentDecision-4B 另用到达过的错误后状态训练，避免只模仿成功轨迹。原文 §2–4、附录 A/D 对单 A100/A30 或 Mac 的本轮预算，完整训练、真实工具任务和多臂评测成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现按决策类别拟合阈值、低置信回退及声明成本会计；没有 Jev／LLM 调用、AgentDecision-4B 训练或统一 Evolve 接入。每 seed 的低／高置信值随机化，40 行 shadow 数值 fixture 拟合不同阈值，在 12 个独立公共请求上实际调用概率 callback 或强模型 callback。负对照把阈值压低到 0.5，保留错误委派；NaN 输出触发回退；  工具使用与可靠性 System One/JEV置信委派与回退 Agent 工具与协作执行：把计划变成可检查的动作 未知类别或样本不足时应该强行套用最近阈值吗？ 不应。默认每 bin 至少二十行，同置信不拆分，尾部不足合并；整类不足、无合格 suffix 或未知类别全部回退强模型。fit 只接校准验证数据，runtime 不含 gold 或强模型答案；本地人工 callback 只验证委派合同。 例如只见过三条参数决策不能拟合可靠类别阈值，直接回退比借另一个工具类别的门槛冒充校准更符合合同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-92de0166e9d9fec7">未知类别或样本不足时应该强行套用最近阈值吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-agent-harness">JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不应。默认每 bin 至少二十行，同置信不拆分，尾部不足合并；整类不足、无合格 suffix 或未知类别全部回退强模型。fit 只接校准验证数据，runtime 不含 gold 或强模型答案；本地人工 callback 只验证委派合同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只见过三条参数决策不能拟合可靠类别阈值，直接回退比借另一个工具类别的门槛冒充校准更符合合同。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21412">原论文</a> · <a href="../../../../agent-research/2610.21412-jev-agent-harness/">实现解读</a> · <a href="#qa-92de0166e9d9fec7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:leash" data-paper-title="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents Agent Simular 2026-10-15 小模型先执行、必要时交给强模型可降低成本，但“何时接管”和“强模型接管后是否走偏”是两个问题。LEASH 利用弱模型表示与历史成功/失败参考的距离，不额外训练一个监控网络；初始和运行时 gate 决定 handoff，之后定期用弱模型的未执行 Shadow 动作表示监督强模型，并在需要时要求其重新审视策略。 完整多模型多配置实验成本高且需要 GUI/远程接口，成本过高，不复现（审查 DONE）。Shadow 高分回调在两次改变强动作后停止，未执行探针动作。component_only / L1 CPU 机制诊断。输入是明确生成的合成向量，不是模型 hidden states；统计校准和 Shadow callback 不等于完成 OSWorld 或真实 GUI Agent。每 seed 使用 30 个合成 reference task、90 action 向量及 12 个隔离 evaluation task；  专家模型编排 公共评测与协议 Agent 工具与协作执行：把计划变成可检查的动作 LEASH 为什么研究让弱模型工作、在风险较高时再交给强模型？ 一直调用强模型成本较高，始终依赖弱模型又可能在关键状态失败。LEASH 研究由弱模型先执行，并用风险信号决定何时接管，试图在任务结果与调用资源之间折中。接管并非免费，风险分数也不是天然校准的概率，效果需要按实际完整任务核算。 教学例：小模型能处理常规文件搜索，面对罕见的恢复状态时交给强模型；是否划算，要看接管次数以及最终是否真正交付。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-leash-edca97db" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d41c3c5dadc1bc88">LEASH 为什么研究让弱模型工作、在风险较高时再交给强模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aleash">LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Simular</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一直调用强模型成本较高，始终依赖弱模型又可能在关键状态失败。LEASH 研究由弱模型先执行，并用风险信号决定何时接管，试图在任务结果与调用资源之间折中。接管并非免费，风险分数也不是天然校准的概率，效果需要按实际完整任务核算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：小模型能处理常规文件搜索，面对罕见的恢复状态时交给强模型；是否划算，要看接管次数以及最终是否真正交付。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22280">原论文</a> · <a href="../../../../agent-research/2610.22280-leash/">实现解读</a> · <a href="#qa-d41c3c5dadc1bc88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:leash" data-paper-title="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents Agent Simular 2026-10-15 小模型先执行、必要时交给强模型可降低成本，但“何时接管”和“强模型接管后是否走偏”是两个问题。LEASH 利用弱模型表示与历史成功/失败参考的距离，不额外训练一个监控网络；初始和运行时 gate 决定 handoff，之后定期用弱模型的未执行 Shadow 动作表示监督强模型，并在需要时要求其重新审视策略。 完整多模型多配置实验成本高且需要 GUI/远程接口，成本过高，不复现（审查 DONE）。Shadow 高分回调在两次改变强动作后停止，未执行探针动作。component_only / L1 CPU 机制诊断。输入是明确生成的合成向量，不是模型 hidden states；统计校准和 Shadow callback 不等于完成 OSWorld 或真实 GUI Agent。每 seed 使用 30 个合成 reference task、90 action 向量及 12 个隔离 evaluation task；  专家模型编排 公共评测与协议 Agent 工具与协作执行：把计划变成可检查的动作 强模型接管后，为什么还要用未执行的 Shadow 动作继续监督？ 升级解决弱模型可能失败的问题，却不保证强模型之后不偏离。弱模型的影子表示提供低成本参照，定期判断是否需要强模型重新审视策略，但不实际执行影子动作；距离分数只是与失败参考更近的指标，不是已校准失败概率或测试固定接管配额。 例如强模型接管后准备点击删除，弱模型影子建议先检查权限，系统可触发复核，却不能把两套动作都同时执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-cc752aad38fc797e">强模型接管后，为什么还要用未执行的 Shadow 动作继续监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aleash">LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Simular</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>升级解决弱模型可能失败的问题，却不保证强模型之后不偏离。弱模型的影子表示提供低成本参照，定期判断是否需要强模型重新审视策略，但不实际执行影子动作；距离分数只是与失败参考更近的指标，不是已校准失败概率或测试固定接管配额。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如强模型接管后准备点击删除，弱模型影子建议先检查权限，系统可触发复核，却不能把两套动作都同时执行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22280">原论文</a> · <a href="../../../../agent-research/2610.22280-leash/">实现解读</a> · <a href="#qa-cc752aad38fc797e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:leash" data-paper-title="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents Agent Simular 2026-10-15 小模型先执行、必要时交给强模型可降低成本，但“何时接管”和“强模型接管后是否走偏”是两个问题。LEASH 利用弱模型表示与历史成功/失败参考的距离，不额外训练一个监控网络；初始和运行时 gate 决定 handoff，之后定期用弱模型的未执行 Shadow 动作表示监督强模型，并在需要时要求其重新审视策略。 完整多模型多配置实验成本高且需要 GUI/远程接口，成本过高，不复现（审查 DONE）。Shadow 高分回调在两次改变强动作后停止，未执行探针动作。component_only / L1 CPU 机制诊断。输入是明确生成的合成向量，不是模型 hidden states；统计校准和 Shadow callback 不等于完成 OSWorld 或真实 GUI Agent。每 seed 使用 30 个合成 reference task、90 action 向量及 12 个隔离 evaluation task；  专家模型编排 公共评测与协议 Agent 工具与协作执行：把计划变成可检查的动作 参考距离分数与校准后的失败概率为什么不能等同？ 分数比较弱表示到 Pass/Fail 均值的 Mahalanobis 距离，高分只说明相对更近失败类。分布漂移、协方差和表示结构会影响阈值，目标路由比例也不是 test 硬配额；应按 reference 校准，不能将数值直接解释为百分之几会失败。 例如分数二不代表失败概率二成，换一个表示尺度或任务分布后同分值也可能对应不同风险。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e0d0812a090585e4">参考距离分数与校准后的失败概率为什么不能等同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aleash">LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Simular</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分数比较弱表示到 Pass/Fail 均值的 Mahalanobis 距离，高分只说明相对更近失败类。分布漂移、协方差和表示结构会影响阈值，目标路由比例也不是 test 硬配额；应按 reference 校准，不能将数值直接解释为百分之几会失败。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如分数二不代表失败概率二成，换一个表示尺度或任务分布后同分值也可能对应不同风险。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22280">原论文</a> · <a href="../../../../agent-research/2610.22280-leash/">实现解读</a> · <a href="#qa-e0d0812a090585e4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:leash" data-paper-title="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents Agent Simular 2026-10-15 小模型先执行、必要时交给强模型可降低成本，但“何时接管”和“强模型接管后是否走偏”是两个问题。LEASH 利用弱模型表示与历史成功/失败参考的距离，不额外训练一个监控网络；初始和运行时 gate 决定 handoff，之后定期用弱模型的未执行 Shadow 动作表示监督强模型，并在需要时要求其重新审视策略。 完整多模型多配置实验成本高且需要 GUI/远程接口，成本过高，不复现（审查 DONE）。Shadow 高分回调在两次改变强动作后停止，未执行探针动作。component_only / L1 CPU 机制诊断。输入是明确生成的合成向量，不是模型 hidden states；统计校准和 Shadow callback 不等于完成 OSWorld 或真实 GUI Agent。每 seed 使用 30 个合成 reference task、90 action 向量及 12 个隔离 evaluation task；  专家模型编排 公共评测与协议 Agent 工具与协作执行：把计划变成可检查的动作 运行 gate 为什么用每任务最大分，Shadow 又在哪些步触发？ 运行风险校准以 reference 每任务最大 action 分为单位，所有同任务观察留同一 OOF 折；按 step 分位数会改变整体升级率。handoff 后从第一个 strong step 起每三步探测，即一、四、七，最多六次干预、两次改变强动作后停止。 例如在第三区间才开始探测会错过第一步风险；把同一任务不同步拆进训练和验证也会泄露任务特征。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-18c5ccd7b7190180">运行 gate 为什么用每任务最大分，Shadow 又在哪些步触发？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aleash">LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Simular</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>运行风险校准以 reference 每任务最大 action 分为单位，所有同任务观察留同一 OOF 折；按 step 分位数会改变整体升级率。handoff 后从第一个 strong step 起每三步探测，即一、四、七，最多六次干预、两次改变强动作后停止。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如在第三区间才开始探测会错过第一步风险；把同一任务不同步拆进训练和验证也会泄露任务特征。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射、成本与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22280">原论文</a> · <a href="../../../../agent-research/2610.22280-leash/">实现解读</a> · <a href="#qa-18c5ccd7b7190180">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:structural-signal-retriever" data-paper-title="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems Agent State University of Campinas 2026-10-15 多 Agent 注册表扩大后，把全部 Agent Card 塞给 LLM 会增加输入和选择成本。SSR §III 不训练额外模型，而是从明确的能力字段提取可解释词法信号，以倒排表预先缩小候选池。这里 structural 指来源于 name、description、skills、tags、examples、tools 的字段，不是句法图或隐向量。核心词法机制是已有IDF检索的特定集成，不应包装为新语义模型。 完整实验成本过高，不复现（审查 DONE）。本地CPU诊断记录保存可审计逐seed数据。无数据下载、LLM调用或GPU需求。固定 revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1；seeds42/43/44各生成64张合成能力card及12个查询，检索器只接收能力文本，接口没有gold answer或目标card参数。  工具使用与路由 Agent发现与词法检索 Agent 工具与协作执行：把计划变成可检查的动作 SSR 为什么要先解决大目录里“该找哪个 Agent”的发现问题？ 多个 Agent 各有能力描述，若每次全部送入模型会增加选择成本。SSR 用公开描述中的离散词信号构造倒排检索，先形成候选池再交给后续决策。它提供可解释的字面匹配，不能理解没有共同信号的改写，因此无命中时应承认空池，而非伪称语义召回。 教学例：任务含“发票”，能力描述也出现该信号时可建立候选；目录只写另一种无重叠术语时，SSR 可能确实找不到。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-structural-signal-retriever-c1b3c953" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-164006635fc0f00e">SSR 为什么要先解决大目录里“该找哪个 Agent”的发现问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Astructural-signal-retriever">SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · State University of Campinas</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个 Agent 各有能力描述，若每次全部送入模型会增加选择成本。SSR 用公开描述中的离散词信号构造倒排检索，先形成候选池再交给后续决策。它提供可解释的字面匹配，不能理解没有共同信号的改写，因此无命中时应承认空池，而非伪称语义召回。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：任务含“发票”，能力描述也出现该信号时可建立候选；目录只写另一种无重叠术语时，SSR 可能确实找不到。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21113">原论文</a> · <a href="../../../../agent-research/2610.21113-structural-signal-retriever/">实现解读</a> · <a href="#qa-164006635fc0f00e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:structural-signal-retriever" data-paper-title="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems Agent State University of Campinas 2026-10-15 多 Agent 注册表扩大后，把全部 Agent Card 塞给 LLM 会增加输入和选择成本。SSR §III 不训练额外模型，而是从明确的能力字段提取可解释词法信号，以倒排表预先缩小候选池。这里 structural 指来源于 name、description、skills、tags、examples、tools 的字段，不是句法图或隐向量。核心词法机制是已有IDF检索的特定集成，不应包装为新语义模型。 完整实验成本过高，不复现（审查 DONE）。本地CPU诊断记录保存可审计逐seed数据。无数据下载、LLM调用或GPU需求。固定 revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1；seeds42/43/44各生成64张合成能力card及12个查询，检索器只接收能力文本，接口没有gold answer或目标card参数。  工具使用与路由 Agent发现与词法检索 Agent 工具与协作执行：把计划变成可检查的动作 SSR 为什么在无词法命中时返回空池，而不声称找到了语义相近 Agent？ 它的 structural 信号来自明确字段中的词与相邻词组，IDF 得分不包含未匹配语义。倒排索引只省去零分候选的枚举，保持同一词法正分排序；无命中就应暴露信息不足，不能把任意回退结果包装成这套机制提供的语义理解。 例如注册卡只写“invoice”，查询用一个没有共享词的表达可能返回空池；系统应知道是词法覆盖不足，而非假装已理解同义关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2848f9d257695af3">SSR 为什么在无词法命中时返回空池，而不声称找到了语义相近 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Astructural-signal-retriever">SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · State University of Campinas</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它的 structural 信号来自明确字段中的词与相邻词组，IDF 得分不包含未匹配语义。倒排索引只省去零分候选的枚举，保持同一词法正分排序；无命中就应暴露信息不足，不能把任意回退结果包装成这套机制提供的语义理解。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如注册卡只写“invoice”，查询用一个没有共享词的表达可能返回空池；系统应知道是词法覆盖不足，而非假装已理解同义关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21113">原论文</a> · <a href="../../../../agent-research/2610.21113-structural-signal-retriever/">实现解读</a> · <a href="#qa-2848f9d257695af3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:structural-signal-retriever" data-paper-title="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems Agent State University of Campinas 2026-10-15 多 Agent 注册表扩大后，把全部 Agent Card 塞给 LLM 会增加输入和选择成本。SSR §III 不训练额外模型，而是从明确的能力字段提取可解释词法信号，以倒排表预先缩小候选池。这里 structural 指来源于 name、description、skills、tags、examples、tools 的字段，不是句法图或隐向量。核心词法机制是已有IDF检索的特定集成，不应包装为新语义模型。 完整实验成本过高，不复现（审查 DONE）。本地CPU诊断记录保存可审计逐seed数据。无数据下载、LLM调用或GPU需求。固定 revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1；seeds42/43/44各生成64张合成能力card及12个查询，检索器只接收能力文本，接口没有gold answer或目标card参数。  工具使用与路由 Agent发现与词法检索 Agent 工具与协作执行：把计划变成可检查的动作 倒排 SSR 与穷举同一 IDF 分数为什么可以保持正分排序一致？ 所有 IDF 为正，倒排并集恰好收集与查询至少共享一信号的 card，零分项被排除；候选仍按相同分数、匹配数和 ID 打平排序。因此加速来自省去零交集打分，不是换了语义目标；无命中应返回空池。 例如一千张 card 只有十张共享查询词，只对这十张打分仍与全量扫描的正分结果相同，不需要伪造后备选项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-192b9bf0a837b4c8">倒排 SSR 与穷举同一 IDF 分数为什么可以保持正分排序一致？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Astructural-signal-retriever">SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · State University of Campinas</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>所有 IDF 为正，倒排并集恰好收集与查询至少共享一信号的 card，零分项被排除；候选仍按相同分数、匹配数和 ID 打平排序。因此加速来自省去零交集打分，不是换了语义目标；无命中应返回空池。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一千张 card 只有十张共享查询词，只对这十张打分仍与全量扫描的正分结果相同，不需要伪造后备选项。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21113">原论文</a> · <a href="../../../../agent-research/2610.21113-structural-signal-retriever/">实现解读</a> · <a href="#qa-192b9bf0a837b4c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:structural-signal-retriever" data-paper-title="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems Agent State University of Campinas 2026-10-15 多 Agent 注册表扩大后，把全部 Agent Card 塞给 LLM 会增加输入和选择成本。SSR §III 不训练额外模型，而是从明确的能力字段提取可解释词法信号，以倒排表预先缩小候选池。这里 structural 指来源于 name、description、skills、tags、examples、tools 的字段，不是句法图或隐向量。核心词法机制是已有IDF检索的特定集成，不应包装为新语义模型。 完整实验成本过高，不复现（审查 DONE）。本地CPU诊断记录保存可审计逐seed数据。无数据下载、LLM调用或GPU需求。固定 revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1；seeds42/43/44各生成64张合成能力card及12个查询，检索器只接收能力文本，接口没有gold answer或目标card参数。  工具使用与路由 Agent发现与词法检索 Agent 工具与协作执行：把计划变成可检查的动作 重复词、64 信号上限与 empty_pool 有哪些实现要求？ 信号二元去重，词频只影响超限时 unigram 截断，不能重复加权；再按固定规则补 bigram。无命中返回空池，不调用 provider 造答案；API 失败与非法索引保留为失败，当前本地无真实 LLM，不能把接口 fixture 当编排成功率。 例如 card 把“search”重复十次不会获得十倍分，查询完全无词法命中时也不能静默切成全目录语义检索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b24b4dfd98b871d6">重复词、64 信号上限与 empty_pool 有哪些实现要求？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Astructural-signal-retriever">SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · State University of Campinas</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>信号二元去重，词频只影响超限时 unigram 截断，不能重复加权；再按固定规则补 bigram。无命中返回空池，不调用 provider 造答案；API 失败与非法索引保留为失败，当前本地无真实 LLM，不能把接口 fixture 当编排成功率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 card 把“search”重复十次不会获得十倍分，查询完全无词法命中时也不能静默切成全目录语义检索。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21113">原论文</a> · <a href="../../../../agent-research/2610.21113-structural-signal-retriever/">实现解读</a> · <a href="#qa-b24b4dfd98b871d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tracer" data-paper-title="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents Agent Microsoft 2026-10-15 把完整工具目录塞进 prompt 会占用大量上下文，纯工具描述相似度又忽略历史执行路径。TRACER 用 turn 内完整调用前缀索引执行 trie，候选是该前缀在训练中实际出现过的下一工具；边上记录频率和发生该转移时的完整 conversation context 均值。训练两个五维线性 head，逐状态决定经验频率/上下文先验的权重和温度；未知前缀或低置信时回到全目录向量检索。原图出处：原文 Figure 6：完整 TRACER 架构。 以单 A100/A30/Mac 的预算，成本过高，不复现（审查 DONE）；本地仅 component_only / CPU 算子诊断。本地仅 component_only / CPU 算子诊断。真正优化的是可学习混合与温度；使用合成三维表示而非原始语义 encoder，也没有 LLM 选择或执行工具。高 fixture recall 不是 Agent 能力，promotion_eligible: false。每 seed 使用 40 train trajectories / 20 held-out trajectories，每条三步，120 个训练步和 60 个测试步。  tool-retrieval Agent 工具与协作执行：把计划变成可检查的动作 大型工具目录为什么会让 Agent 花很多上下文，却仍选不到正确的下一步？ 把所有工具说明常驻上下文会带来输入成本，静态 Top-K 又可能遗漏当前流程接下来需要的接口。TRACER 关注从已发生的调用经验与当前上下文中预测可用工具子集，让工具发现适应执行进程。预测只是候选支持，不能替代参数验证或真实调用成功。 教学例：完成身份查询后更可能需要读取账户记录，而不是再看整套上千工具目录；若用户转而取消任务，当前上下文也应改变推荐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-tracer-f2f8d03e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e1efe2d57b68e50f">大型工具目录为什么会让 Agent 花很多上下文，却仍选不到正确的下一步？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atracer">TRACER: Trajectory-Aware Tool Retrieval for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>把所有工具说明常驻上下文会带来输入成本，静态 Top-K 又可能遗漏当前流程接下来需要的接口。TRACER 关注从已发生的调用经验与当前上下文中预测可用工具子集，让工具发现适应执行进程。预测只是候选支持，不能替代参数验证或真实调用成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：完成身份查询后更可能需要读取账户记录，而不是再看整套上千工具目录；若用户转而取消任务，当前上下文也应改变推荐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21267">原论文</a> · <a href="../../../../agent-research/2610.21267-tracer/">实现解读</a> · <a href="#qa-e1efe2d57b68e50f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tracer" data-paper-title="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents Agent Microsoft 2026-10-15 把完整工具目录塞进 prompt 会占用大量上下文，纯工具描述相似度又忽略历史执行路径。TRACER 用 turn 内完整调用前缀索引执行 trie，候选是该前缀在训练中实际出现过的下一工具；边上记录频率和发生该转移时的完整 conversation context 均值。训练两个五维线性 head，逐状态决定经验频率/上下文先验的权重和温度；未知前缀或低置信时回到全目录向量检索。原图出处：原文 Figure 6：完整 TRACER 架构。 以单 A100/A30/Mac 的预算，成本过高，不复现（审查 DONE）；本地仅 component_only / CPU 算子诊断。本地仅 component_only / CPU 算子诊断。真正优化的是可学习混合与温度；使用合成三维表示而非原始语义 encoder，也没有 LLM 选择或执行工具。高 fixture recall 不是 Agent 能力，promotion_eligible: false。每 seed 使用 40 train trajectories / 20 held-out trajectories，每条三步，120 个训练步和 60 个测试步。  tool-retrieval Agent 工具与协作执行：把计划变成可检查的动作 为什么工具 trie 用 turn 内完整调用前缀，而不是只看上一把工具？ 同一个上一工具可能出现在不同工作流，完整前缀保留路径身份，下一工具候选才对应真实训练转移。上下文相似度补充当前意图，学习的权重与温度决定如何融合；未知前缀要回退目录检索，不能强行把未见路径套到最相似的旧分支。 例如“搜索→下载”与“认证→下载”后续可能分别需要解析与权限检查，只看最后一个下载工具会混淆两种路线。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a03d84108db990af">为什么工具 trie 用 turn 内完整调用前缀，而不是只看上一把工具？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atracer">TRACER: Trajectory-Aware Tool Retrieval for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一个上一工具可能出现在不同工作流，完整前缀保留路径身份，下一工具候选才对应真实训练转移。上下文相似度补充当前意图，学习的权重与温度决定如何融合；未知前缀要回退目录检索，不能强行把未见路径套到最相似的旧分支。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“搜索→下载”与“认证→下载”后续可能分别需要解析与权限检查，只看最后一个下载工具会混淆两种路线。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21267">原论文</a> · <a href="../../../../agent-research/2610.21267-tracer/">实现解读</a> · <a href="#qa-a03d84108db990af">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tracer" data-paper-title="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents Agent Microsoft 2026-10-15 把完整工具目录塞进 prompt 会占用大量上下文，纯工具描述相似度又忽略历史执行路径。TRACER 用 turn 内完整调用前缀索引执行 trie，候选是该前缀在训练中实际出现过的下一工具；边上记录频率和发生该转移时的完整 conversation context 均值。训练两个五维线性 head，逐状态决定经验频率/上下文先验的权重和温度；未知前缀或低置信时回到全目录向量检索。原图出处：原文 Figure 6：完整 TRACER 架构。 以单 A100/A30/Mac 的预算，成本过高，不复现（审查 DONE）；本地仅 component_only / CPU 算子诊断。本地仅 component_only / CPU 算子诊断。真正优化的是可学习混合与温度；使用合成三维表示而非原始语义 encoder，也没有 LLM 选择或执行工具。高 fixture recall 不是 Agent 能力，promotion_eligible: false。每 seed 使用 40 train trajectories / 20 held-out trajectories，每条三步，120 个训练步和 60 个测试步。  tool-retrieval Agent 工具与协作执行：把计划变成可检查的动作 经验频率与上下文先验为什么要用可学习权重而非固定相加？ 高频工具不一定适合当前语境，语义相近转移也可能样本稀少。两个线性 head 按五维状态特征决定混合权重和温度，温度影响置信 gate 而不改变排序；学习仍依赖校准和训练覆盖，不是从频率直接得到成功概率。 例如某前缀常接工具甲，但当前上下文更像过去接乙的状态，模型可减弱经验频率权重来避免机械复制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ee6c2772d37a26ac">经验频率与上下文先验为什么要用可学习权重而非固定相加？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atracer">TRACER: Trajectory-Aware Tool Retrieval for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高频工具不一定适合当前语境，语义相近转移也可能样本稀少。两个线性 head 按五维状态特征决定混合权重和温度，温度影响置信 gate 而不改变排序；学习仍依赖校准和训练覆盖，不是从频率直接得到成功概率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某前缀常接工具甲，但当前上下文更像过去接乙的状态，模型可减弱经验频率权重来避免机械复制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21267">原论文</a> · <a href="../../../../agent-research/2610.21267-tracer/">实现解读</a> · <a href="#qa-ee6c2772d37a26ac">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tracer" data-paper-title="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TRACER: Trajectory-Aware Tool Retrieval for LLM Agents Agent Microsoft 2026-10-15 把完整工具目录塞进 prompt 会占用大量上下文，纯工具描述相似度又忽略历史执行路径。TRACER 用 turn 内完整调用前缀索引执行 trie，候选是该前缀在训练中实际出现过的下一工具；边上记录频率和发生该转移时的完整 conversation context 均值。训练两个五维线性 head，逐状态决定经验频率/上下文先验的权重和温度；未知前缀或低置信时回到全目录向量检索。原图出处：原文 Figure 6：完整 TRACER 架构。 以单 A100/A30/Mac 的预算，成本过高，不复现（审查 DONE）；本地仅 component_only / CPU 算子诊断。本地仅 component_only / CPU 算子诊断。真正优化的是可学习混合与温度；使用合成三维表示而非原始语义 encoder，也没有 LLM 选择或执行工具。高 fixture recall 不是 Agent 能力，promotion_eligible: false。每 seed 使用 40 train trajectories / 20 held-out trajectories，每条三步，120 个训练步和 60 个测试步。  tool-retrieval Agent 工具与协作执行：把计划变成可检查的动作 crossfit 为什么必须排除目标 trajectory 整折，而不只遮当前标签？ 同一轨迹其他步骤会影响 trie 和边上下文均值，只遮标签仍可泄露该轨迹结构。每步信号需由不含整折的索引产生，standardizer 也只拟合训练折；本地合成向量 head 真训练不等于真实工具任务的选择能力。 例如目标工具未直接进 loss 输入，但若其转移已在全索引里计数，仍会让训练样本看见自己的答案路径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f6d187227006150a">crossfit 为什么必须排除目标 trajectory 整折，而不只遮当前标签？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atracer">TRACER: Trajectory-Aware Tool Retrieval for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一轨迹其他步骤会影响 trie 和边上下文均值，只遮标签仍可泄露该轨迹结构。每步信号需由不含整折的索引产生，standardizer 也只拟合训练折；本地合成向量 head 真训练不等于真实工具任务的选择能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如目标工具未直接进 loss 输入，但若其转移已在全索引里计数，仍会让训练样本看见自己的答案路径。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21267">原论文</a> · <a href="../../../../agent-research/2610.21267-tracer/">实现解读</a> · <a href="#qa-f6d187227006150a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aria" data-paper-title="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems Agent Florida State University 2026-10-14 多 Agent 的早期错误会沿消息和工具结果传播。ARIA 不只在结束后解释失败，而是把执行验证过的修复转成训练数据，让模型在部分轨迹上决定何时干预、在哪里切断及如何续写。原文 §2、附录 B的训练链包括结构 SFT、repair DPO、diagnosis transfer、repair GRPO 和 gate GRPO。本地没有以人工 heuristic 冒充这些学习阶段，只抽出可独立检验的补丁合同。 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现 cut-and-continuation 数据合同，不训练 inspection gate 或修复策略。随机事件序列实际执行合法 cut 与新 tool request 替换；负对照注入未知 cut、保留前缀 ID 冲突和伪造工具观察。另以随机成对执行 verdict 检查“只看 patched pass”会产生的错误样本接纳。verdict 是调用方 scorer 的人工 fixture，不是 Agent 推出的答案；模块不把 gold 传给模型。详见 CPU 产物。  多Agent协作 运行时诊断与续写修复 Agent 工具与协作执行：把计划变成可检查的动作 为什么在早期部分轨迹上修复，而不只在结束后写失败总结？ 早期错误会沿多 Agent 消息传播，运行中切断并续写有机会阻止后续放大。ARIA 学习何时干预、在哪里切断及如何续写，但补丁仍须实际执行验证；结构上替换了后缀不代表诊断正确或环境状态已精确回滚。 例如第三区域消息把单位写错，后续多名 Agent 都沿用；在传播前修复比任务结束后说明单位错误更可能改变结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-aria-04eaa6e6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-61400377d7f00fa0">为什么在早期部分轨迹上修复，而不只在结束后写失败总结？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaria">ARIA: Runtime Inspection and Amendment for Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Florida State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>早期错误会沿多 Agent 消息传播，运行中切断并续写有机会阻止后续放大。ARIA 学习何时干预、在哪里切断及如何续写，但补丁仍须实际执行验证；结构上替换了后缀不代表诊断正确或环境状态已精确回滚。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第三区域消息把单位写错，后续多名 Agent 都沿用；在传播前修复比任务结束后说明单位错误更可能改变结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20780">原论文</a> · <a href="../../../../agent-research/2610.20780-aria/">实现解读</a> · <a href="#qa-61400377d7f00fa0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aria" data-paper-title="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems Agent Florida State University 2026-10-14 多 Agent 的早期错误会沿消息和工具结果传播。ARIA 不只在结束后解释失败，而是把执行验证过的修复转成训练数据，让模型在部分轨迹上决定何时干预、在哪里切断及如何续写。原文 §2、附录 B的训练链包括结构 SFT、repair DPO、diagnosis transfer、repair GRPO 和 gate GRPO。本地没有以人工 heuristic 冒充这些学习阶段，只抽出可独立检验的补丁合同。 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现 cut-and-continuation 数据合同，不训练 inspection gate 或修复策略。随机事件序列实际执行合法 cut 与新 tool request 替换；负对照注入未知 cut、保留前缀 ID 冲突和伪造工具观察。另以随机成对执行 verdict 检查“只看 patched pass”会产生的错误样本接纳。verdict 是调用方 scorer 的人工 fixture，不是 Agent 推出的答案；模块不把 gold 传给模型。详见 CPU 产物。  多Agent协作 运行时诊断与续写修复 Agent 工具与协作执行：把计划变成可检查的动作 修复轨迹为什么只能提出待执行 tool call，不能直接写入一个成功 tool result？ 工具结果必须来自真实执行，否则补丁只是伪造证据。切断点保留已观察前缀，模型续写可提出新行动，再与 fresh control 比较是否真的恢复；结构合法只证明补丁格式可接纳，不能单独证明归因正确或错误已被修好。 例如模型提出重新运行测试是合法修复候选，但不能在续写里直接捏造“全部通过”；必须执行测试并读取实际结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-72d8e93a8b1ee2a9">修复轨迹为什么只能提出待执行 tool call，不能直接写入一个成功 tool result？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaria">ARIA: Runtime Inspection and Amendment for Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Florida State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具结果必须来自真实执行，否则补丁只是伪造证据。切断点保留已观察前缀，模型续写可提出新行动，再与 fresh control 比较是否真的恢复；结构合法只证明补丁格式可接纳，不能单独证明归因正确或错误已被修好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型提出重新运行测试是合法修复候选，但不能在续写里直接捏造“全部通过”；必须执行测试并读取实际结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20780">原论文</a> · <a href="../../../../agent-research/2610.20780-aria/">实现解读</a> · <a href="#qa-72d8e93a8b1ee2a9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aria" data-paper-title="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems Agent Florida State University 2026-10-14 多 Agent 的早期错误会沿消息和工具结果传播。ARIA 不只在结束后解释失败，而是把执行验证过的修复转成训练数据，让模型在部分轨迹上决定何时干预、在哪里切断及如何续写。原文 §2、附录 B的训练链包括结构 SFT、repair DPO、diagnosis transfer、repair GRPO 和 gate GRPO。本地没有以人工 heuristic 冒充这些学习阶段，只抽出可独立检验的补丁合同。 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现 cut-and-continuation 数据合同，不训练 inspection gate 或修复策略。随机事件序列实际执行合法 cut 与新 tool request 替换；负对照注入未知 cut、保留前缀 ID 冲突和伪造工具观察。另以随机成对执行 verdict 检查“只看 patched pass”会产生的错误样本接纳。verdict 是调用方 scorer 的人工 fixture，不是 Agent 推出的答案；模块不把 gold 传给模型。详见 CPU 产物。  多Agent协作 运行时诊断与续写修复 Agent 工具与协作执行：把计划变成可检查的动作 patched pass 与 fresh control fail 为什么要同时作为 verified 条件？ patched 成功可能只是重跑随机性或环境改变，fresh control 也成功时无法说明修复带来必要改进。配对条件减少把普通重试误当修复的情况，但仍不是完整框架精确因果重放；原文用重建 continuation context，有明确证据边界。 例如修补后测试通过，但不修补重新跑也通过，这对样本不应被当成已验证修复训练对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0d5c547a0a9d2f33">patched pass 与 fresh control fail 为什么要同时作为 verified 条件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaria">ARIA: Runtime Inspection and Amendment for Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Florida State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>patched 成功可能只是重跑随机性或环境改变，fresh control 也成功时无法说明修复带来必要改进。配对条件减少把普通重试误当修复的情况，但仍不是完整框架精确因果重放；原文用重建 continuation context，有明确证据边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如修补后测试通过，但不修补重新跑也通过，这对样本不应被当成已验证修复训练对。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20780">原论文</a> · <a href="../../../../agent-research/2610.20780-aria/">实现解读</a> · <a href="#qa-0d5c547a0a9d2f33">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aria" data-paper-title="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ARIA: Runtime Inspection and Amendment for Multi-Agent Systems Agent Florida State University 2026-10-14 多 Agent 的早期错误会沿消息和工具结果传播。ARIA 不只在结束后解释失败，而是把执行验证过的修复转成训练数据，让模型在部分轨迹上决定何时干预、在哪里切断及如何续写。原文 §2、附录 B的训练链包括结构 SFT、repair DPO、diagnosis transfer、repair GRPO 和 gate GRPO。本地没有以人工 heuristic 冒充这些学习阶段，只抽出可独立检验的补丁合同。 成本过高，不复现（审查 DONE）。component_only / L1 CPU。实现 cut-and-continuation 数据合同，不训练 inspection gate 或修复策略。随机事件序列实际执行合法 cut 与新 tool request 替换；负对照注入未知 cut、保留前缀 ID 冲突和伪造工具观察。另以随机成对执行 verdict 检查“只看 patched pass”会产生的错误样本接纳。verdict 是调用方 scorer 的人工 fixture，不是 Agent 推出的答案；模块不把 gold 传给模型。详见 CPU 产物。  多Agent协作 运行时诊断与续写修复 Agent 工具与协作执行：把计划变成可检查的动作 cut 事件、补丁类型和长度有哪些硬合同？ 切断保留被引用的已观察事件，非空 cut 必须早于定位坏事件；补丁最多八事件、一万二千规范 JSON 字符，ID 不冲突且不能只换 ID 重贴旧后缀。只允许 assistant 消息或待执行 tool call，不能伪造工具结果；本地未训练五阶段模型。 例如模型可提出重新查询订单，但不能直接插入“工具返回已付款”的假 observation，让修复看起来凭空成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7108f55dcf61f947">cut 事件、补丁类型和长度有哪些硬合同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaria">ARIA: Runtime Inspection and Amendment for Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Florida State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>切断保留被引用的已观察事件，非空 cut 必须早于定位坏事件；补丁最多八事件、一万二千规范 JSON 字符，ID 不冲突且不能只换 ID 重贴旧后缀。只允许 assistant 消息或待执行 tool call，不能伪造工具结果；本地未训练五阶段模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型可提出重新查询订单，但不能直接插入“工具返回已付款”的假 observation，让修复看起来凭空成功。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、成本与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20780">原论文</a> · <a href="../../../../agent-research/2610.20780-aria/">实现解读</a> · <a href="#qa-7108f55dcf61f947">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-workflow" data-paper-title="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows Agent Nanjing University 2026-10-09 这是一篇评测研究，不是新的 self-improvement 算法。比较决策延迟/费用与端到端成功交付；failed recovery、premature completion 和失败开销计入资源每成功，而非只报告单步省时。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为同task/run的原配置与替换decision配置；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evaluation delivered-outcome latency-cost-recovery Agent 工具与协作执行：把计划变成可检查的动作 评估廉价决策替代时，为什么要把“完成一次交付”而非一次调用当作单位？ Agent 是由多步决策、工具和重试组成的工作流，局部省资源可能增加后续失败与重跑。Jev Workflow 关注完整交付所需的总资源，使采用廉价判断的收益与它造成的额外尝试放在同一口径。不同成功集合应分别报告，不能只摘一项局部延迟说明系统更高效。 教学例：每次判断省半秒，却多失败三次才完成任务，用户真正支付的是所有尝试；需要按最后交付累计计算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-jev-workflow-32efeb08" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e21801a615beb116">评估廉价决策替代时，为什么要把“完成一次交付”而非一次调用当作单位？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-workflow">When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Agent 是由多步决策、工具和重试组成的工作流，局部省资源可能增加后续失败与重跑。Jev Workflow 关注完整交付所需的总资源，使采用廉价判断的收益与它造成的额外尝试放在同一口径。不同成功集合应分别报告，不能只摘一项局部延迟说明系统更高效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：每次判断省半秒，却多失败三次才完成任务，用户真正支付的是所有尝试；需要按最后交付累计计算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13092">原论文</a> · <a href="../../../../reproductions/2610.13092-jev-workflow/">实现解读</a> · <a href="#qa-e21801a615beb116">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-workflow" data-paper-title="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows Agent Nanjing University 2026-10-09 这是一篇评测研究，不是新的 self-improvement 算法。比较决策延迟/费用与端到端成功交付；failed recovery、premature completion 和失败开销计入资源每成功，而非只报告单步省时。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为同task/run的原配置与替换decision配置；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evaluation delivered-outcome latency-cost-recovery Agent 工具与协作执行：把计划变成可检查的动作 单步决策更快，为什么每次成功交付的总资源反而可能更高？ 错误决策会引入重试、恢复失败或过早完成，省下的单次延迟可能被失败轨迹抵消。资源每成功把所有尝试的费用和时间计入，再除成功数；只看双方都成功的配对可比较顺利路径，但不能替代全尝试交付口径或隐藏失败成本。 例如快速方案每次便宜一半却经常失败，十次才完成两次；完整统计可能比稍慢但十次成功八次的方案更贵。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f67a6f111ad8004f">单步决策更快，为什么每次成功交付的总资源反而可能更高？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-workflow">When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>错误决策会引入重试、恢复失败或过早完成，省下的单次延迟可能被失败轨迹抵消。资源每成功把所有尝试的费用和时间计入，再除成功数；只看双方都成功的配对可比较顺利路径，但不能替代全尝试交付口径或隐藏失败成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如快速方案每次便宜一半却经常失败，十次才完成两次；完整统计可能比稍慢但十次成功八次的方案更贵。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13092">原论文</a> · <a href="../../../../reproductions/2610.13092-jev-workflow/">实现解读</a> · <a href="#qa-f67a6f111ad8004f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-workflow" data-paper-title="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows Agent Nanjing University 2026-10-09 这是一篇评测研究，不是新的 self-improvement 算法。比较决策延迟/费用与端到端成功交付；failed recovery、premature completion 和失败开销计入资源每成功，而非只报告单步省时。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为同task/run的原配置与替换decision配置；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evaluation delivered-outcome latency-cost-recovery Agent 工具与协作执行：把计划变成可检查的动作 matched-success 与 all-attempt delivery 分别回答什么问题？ matched-success 只比较两配置在相同 task/run 都成功的资源差，适合看成功路径是否更便宜；all-attempt 把失败成本和全部成功数纳入，评价真实交付。前者有选择条件，不能替代后者或隐藏某配置大量失败带来的损失。 例如只挑双方都完成的三题可发现决策变快，却看不见另外七题有多少因新路由失败；两种口径要并列解释。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-be33fb879417f3dd">matched-success 与 all-attempt delivery 分别回答什么问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-workflow">When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>matched-success 只比较两配置在相同 task/run 都成功的资源差，适合看成功路径是否更便宜；all-attempt 把失败成本和全部成功数纳入，评价真实交付。前者有选择条件，不能替代后者或隐藏某配置大量失败带来的损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只挑双方都完成的三题可发现决策变快，却看不见另外七题有多少因新路由失败；两种口径要并列解释。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13092">原论文</a> · <a href="../../../../reproductions/2610.13092-jev-workflow/">实现解读</a> · <a href="#qa-be33fb879417f3dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:jev-workflow" data-paper-title="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows Agent Nanjing University 2026-10-09 这是一篇评测研究，不是新的 self-improvement 算法。比较决策延迟/费用与端到端成功交付；failed recovery、premature completion 和失败开销计入资源每成功，而非只报告单步省时。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为同task/run的原配置与替换decision配置；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  agent-evaluation delivered-outcome latency-cost-recovery Agent 工具与协作执行：把计划变成可检查的动作 零成功、缺少配对或无效资源值时为什么不能继续算漂亮比值？ 零成功的成本每成功无定义，缺 task/run 配对破坏比较，负数或非有限资源不是有效执行记录。基础设施应显式拒绝或保留相应状态，不能删掉失败来恢复分母；当前只消费实际 paired trace，不加载或伪造 Jev 权重/API。 例如一配置全失败时不能把分母加一个小 ε 后宣称有限效率，也不能从作者表格复制一行冒充本地执行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c39238132ac53294">零成功、缺少配对或无效资源值时为什么不能继续算漂亮比值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ajev-workflow">When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>零成功的成本每成功无定义，缺 task/run 配对破坏比较，负数或非有限资源不是有效执行记录。基础设施应显式拒绝或保留相应状态，不能删掉失败来恢复分母；当前只消费实际 paired trace，不加载或伪造 Jev 权重/API。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一配置全失败时不能把分母加一个小 ε 后宣称有限效率，也不能从作者表格复制一行冒充本地执行。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、结果、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13092">原论文</a> · <a href="../../../../reproductions/2610.13092-jev-workflow/">实现解读</a> · <a href="#qa-c39238132ac53294">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rated" data-paper-title="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics Agent Texas Tech University 2026-10-09 独立 query/tool encoder 做 CLS 归一化与 contrastive InfoNCE 训练。部署时 encoder 冻结，先语义 top-K，再融合 metadata prior 与逐工具 discounted LinUCB；只从实际选中工具的执行成功、错误或超时更新对应 arm。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为冻结语义dual encoder；线上反馈重排实验组；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  tool-retrieval execution-reliability contextual-bandit Agent 工具与协作执行：把计划变成可检查的动作 工具语义相关为什么还需要执行可靠性重排？ 描述最匹配的工具可能持续失败、超时或已不可用，语义相似度无法独自反映当前运行状态。RATED 先召回相关 Top-K，再结合静态 metadata 与逐工具在线反馈，兼顾任务相关和可靠性；不能为了避失败而选择语义不满足任务的工具。 例如两个 API 都能查天气，其中一个最近频繁超时，系统可在相关候选内偏向另一个，而不是改选无关但稳定的计算器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-rated-710146a7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8d43794df2d72755">工具语义相关为什么还需要执行可靠性重排？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arated">RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Texas Tech University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>描述最匹配的工具可能持续失败、超时或已不可用，语义相似度无法独自反映当前运行状态。RATED 先召回相关 Top-K，再结合静态 metadata 与逐工具在线反馈，兼顾任务相关和可靠性；不能为了避失败而选择语义不满足任务的工具。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个 API 都能查天气，其中一个最近频繁超时，系统可在相关候选内偏向另一个，而不是改选无关但稳定的计算器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13889">原论文</a> · <a href="../../../../reproductions/2610.13889-rated/">实现解读</a> · <a href="#qa-8d43794df2d72755">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rated" data-paper-title="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics Agent Texas Tech University 2026-10-09 独立 query/tool encoder 做 CLS 归一化与 contrastive InfoNCE 训练。部署时 encoder 冻结，先语义 top-K，再融合 metadata prior 与逐工具 discounted LinUCB；只从实际选中工具的执行成功、错误或超时更新对应 arm。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为冻结语义dual encoder；线上反馈重排实验组；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  tool-retrieval execution-reliability contextual-bandit Agent 工具与协作执行：把计划变成可检查的动作 为什么执行反馈只更新实际选中工具的 LinUCB arm？ 只有被执行工具产生可观察的成功、错误或超时，未选择工具的反事实结果并不知道。逐工具更新避免把一次失败归罪整个候选集，折扣又让旧可靠性随时间衰减；语义 top-K 提供相关候选，可靠性探索项并不意味着模型已证明未调用工具更好。 例如工具甲本次超时，应更新甲的记录；同题没调用的乙不能直接记成功，只能保持不确定并等待以后探索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f3a60a5875bf4cde">为什么执行反馈只更新实际选中工具的 LinUCB arm？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arated">RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Texas Tech University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只有被执行工具产生可观察的成功、错误或超时，未选择工具的反事实结果并不知道。逐工具更新避免把一次失败归罪整个候选集，折扣又让旧可靠性随时间衰减；语义 top-K 提供相关候选，可靠性探索项并不意味着模型已证明未调用工具更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具甲本次超时，应更新甲的记录；同题没调用的乙不能直接记成功，只能保持不确定并等待以后探索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13889">原论文</a> · <a href="../../../../reproductions/2610.13889-rated/">实现解读</a> · <a href="#qa-f3a60a5875bf4cde">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rated" data-paper-title="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics Agent Texas Tech University 2026-10-09 独立 query/tool encoder 做 CLS 归一化与 contrastive InfoNCE 训练。部署时 encoder 冻结，先语义 top-K，再融合 metadata prior 与逐工具 discounted LinUCB；只从实际选中工具的执行成功、错误或超时更新对应 arm。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为冻结语义dual encoder；线上反馈重排实验组；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  tool-retrieval execution-reliability contextual-bandit Agent 工具与协作执行：把计划变成可检查的动作 冻结双 encoder 与在线 discounted LinUCB 分别适应什么？ encoder 提供离线学到的查询工具语义空间，部署冻结以保持基础检索；LinUCB 根据实际调用反馈更新每个 arm，并通过折扣适应可靠性变化。两者更新范围不同，不能把 bandit 重排说成在线重新训练整个语言编码器。 例如服务恢复后，后续成功反馈可逐渐提高该 arm 价值，但文本 encoder 的参数仍保持不变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-34d38c6c74c040d3">冻结双 encoder 与在线 discounted LinUCB 分别适应什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arated">RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Texas Tech University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>encoder 提供离线学到的查询工具语义空间，部署冻结以保持基础检索；LinUCB 根据实际调用反馈更新每个 arm，并通过折扣适应可靠性变化。两者更新范围不同，不能把 bandit 重排说成在线重新训练整个语言编码器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如服务恢复后，后续成功反馈可逐渐提高该 arm 价值，但文本 encoder 的参数仍保持不变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13889">原论文</a> · <a href="../../../../reproductions/2610.13889-rated/">实现解读</a> · <a href="#qa-34d38c6c74c040d3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:rated" data-paper-title="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics Agent Texas Tech University 2026-10-09 独立 query/tool encoder 做 CLS 归一化与 contrastive InfoNCE 训练。部署时 encoder 冻结，先语义 top-K，再融合 metadata prior 与逐工具 discounted LinUCB；只从实际选中工具的执行成功、错误或超时更新对应 arm。事实来源：原文全文。 当前是 core_mechanism / L1 机制诊断接口；未声称完成原论文能力复测，未接入 Evolve 晋级。本地对照口径：基线为冻结语义dual encoder；线上反馈重排实验组；实验组由当前真实实现执行；稳定相对提升不适用，尚无正式能力对照。  tool-retrieval execution-reliability contextual-bandit Agent 工具与协作执行：把计划变成可检查的动作 discounted LinUCB 的 γ 怎样影响选中工具的历史统计？ 选中 arm 的对角 A 与 b 先按 γ 衰减，再累加当前特征平方和执行反馈，使较旧证据的相对影响降低。A 同时影响探索不确定度，不能只把折扣理解为改一个成功率。本地语义编码器确有短训练，但授权工具绑定返回失败，不能将 bandit 更新本身当成工具能力成功。 教学例：某工具曾长期可靠但最近持续超时，折扣让新失败逐渐改变统计；如果只永久累计旧成功，变化会被长期历史淹没。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f0e3acf45069aec6">discounted LinUCB 的 γ 怎样影响选中工具的历史统计？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arated">RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Texas Tech University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>选中 arm 的对角 A 与 b 先按 γ 衰减，再累加当前特征平方和执行反馈，使较旧证据的相对影响降低。A 同时影响探索不确定度，不能只把折扣理解为改一个成功率。本地语义编码器确有短训练，但授权工具绑定返回失败，不能将 bandit 更新本身当成工具能力成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：某工具曾长期可靠但最近持续超时，折扣让新失败逐渐改变统计；如果只永久累计旧成功，变化会被长期历史淹没。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、结果、验证与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13889">原论文</a> · <a href="../../../../reproductions/2610.13889-rated/">实现解读</a> · <a href="#qa-f0e3acf45069aec6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mingbird" data-paper-title="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks Agent University of Science and Technology Beijing 2026-10-01 通过 domain 路由和扁平 schema 降低小模型工具调用负担；当模型宣称完成时重新注入原任务与计划并检查产物，发现重复调用或无输出循环时提醒修正，同时为常见 JSON 格式错误提供有限救援。改进的是推理运行框架，不需要把它解释为新的基础模型结构。 L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；使用显式脚本策略，不冒充真实小模型任务成功率。未实现整个 Windows GUI/语音产品、未跑 LRAB/τ²、未接入真实本地 LLM。注册工具仍继承调用方权限，此模块不是隔离沙箱，不应直接注册任意 shell。外部验收不能读取策略未获授权的私密信息并反馈给策略。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 在临时目录中真实写入文件：第一次 finish 因文件不存在被拒绝，随后执行写入，最后重新检查通过。  本地 Agent 运行框架 工具使用 Agent 工具与协作执行：把计划变成可检查的动作 MingBird 为什么专门关注小模型完成多工具长任务的困难？ 小模型的上下文、工具理解与错误恢复能力都有限，把全部接口和长历史一并输入容易增加负担。MingBird 将工具组织、执行循环和完成检查纳入系统设计，帮助策略在受限资源下推进任务。流程组件存在并不表示小模型已能可靠完成任意长程工作，仍需真实产物核验。 教学例：任务横跨文件和数据库，小模型先面对相关工具域，再逐步执行并检查交付文件，而不是一次读完整目录后宣布完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-mingbird-bbd1f960" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ce08018ff6229f8e">MingBird 为什么专门关注小模型完成多工具长任务的困难？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amingbird">Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology Beijing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>小模型的上下文、工具理解与错误恢复能力都有限，把全部接口和长历史一并输入容易增加负担。MingBird 将工具组织、执行循环和完成检查纳入系统设计，帮助策略在受限资源下推进任务。流程组件存在并不表示小模型已能可靠完成任意长程工作，仍需真实产物核验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：任务横跨文件和数据库，小模型先面对相关工具域，再逐步执行并检查交付文件，而不是一次读完整目录后宣布完成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02001">原论文</a> · <a href="../../../../agent-research/2610.02001-mingbird/">实现解读</a> · <a href="#qa-ce08018ff6229f8e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mingbird" data-paper-title="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks Agent University of Science and Technology Beijing 2026-10-01 通过 domain 路由和扁平 schema 降低小模型工具调用负担；当模型宣称完成时重新注入原任务与计划并检查产物，发现重复调用或无输出循环时提醒修正，同时为常见 JSON 格式错误提供有限救援。改进的是推理运行框架，不需要把它解释为新的基础模型结构。 L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；使用显式脚本策略，不冒充真实小模型任务成功率。未实现整个 Windows GUI/语音产品、未跑 LRAB/τ²、未接入真实本地 LLM。注册工具仍继承调用方权限，此模块不是隔离沙箱，不应直接注册任意 shell。外部验收不能读取策略未获授权的私密信息并反馈给策略。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 在临时目录中真实写入文件：第一次 finish 因文件不存在被拒绝，随后执行写入，最后重新检查通过。  本地 Agent 运行框架 工具使用 Agent 工具与协作执行：把计划变成可检查的动作 模型宣称完成后，为什么还要重新注入原任务与计划并检查产物？ 长轨迹中模型可能遗忘目标或把动作执行当成最终交付，重新对照原始要求能发现缺文件、缺验证和提前结束。循环检测与有限格式救援解决运行故障，不是直接提升基础模型知识；字节预算也必须按实际 UTF-8 计算，不能用字符数替代。 例如模型成功创建文件后说完成，但原任务还要求生成测试报告；回看原任务才能发现产物清单尚未满足。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d9bfd00f5a7bc2d8">模型宣称完成后，为什么还要重新注入原任务与计划并检查产物？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amingbird">Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology Beijing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长轨迹中模型可能遗忘目标或把动作执行当成最终交付，重新对照原始要求能发现缺文件、缺验证和提前结束。循环检测与有限格式救援解决运行故障，不是直接提升基础模型知识；字节预算也必须按实际 UTF-8 计算，不能用字符数替代。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型成功创建文件后说完成，但原任务还要求生成测试报告；回看原任务才能发现产物清单尚未满足。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02001">原论文</a> · <a href="../../../../agent-research/2610.02001-mingbird/">实现解读</a> · <a href="#qa-d9bfd00f5a7bc2d8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mingbird" data-paper-title="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks Agent University of Science and Technology Beijing 2026-10-01 通过 domain 路由和扁平 schema 降低小模型工具调用负担；当模型宣称完成时重新注入原任务与计划并检查产物，发现重复调用或无输出循环时提醒修正，同时为常见 JSON 格式错误提供有限救援。改进的是推理运行框架，不需要把它解释为新的基础模型结构。 L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；使用显式脚本策略，不冒充真实小模型任务成功率。未实现整个 Windows GUI/语音产品、未跑 LRAB/τ²、未接入真实本地 LLM。注册工具仍继承调用方权限，此模块不是隔离沙箱，不应直接注册任意 shell。外部验收不能读取策略未获授权的私密信息并反馈给策略。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 在临时目录中真实写入文件：第一次 finish 因文件不存在被拒绝，随后执行写入，最后重新检查通过。  本地 Agent 运行框架 工具使用 Agent 工具与协作执行：把计划变成可检查的动作 domain 路由与扁平 schema 相比把全部工具原样放入上下文，有何取舍？ 路由先缩小工具域，参数过多时保留 required 降低小模型格式负担，减少无关接口干扰；但 optional 参数有时影响任务语义，不能随意删必需约束。该方法改变 harness 输入与恢复，未创造新的基础模型结构。 例如一个工具十个参数中两项必填，可先展示简化接口；若用户明确要求某可选过滤条件，仍须正确处理其需求。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5fd8604251771df1">domain 路由与扁平 schema 相比把全部工具原样放入上下文，有何取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amingbird">Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology Beijing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>路由先缩小工具域，参数过多时保留 required 降低小模型格式负担，减少无关接口干扰；但 optional 参数有时影响任务语义，不能随意删必需约束。该方法改变 harness 输入与恢复，未创造新的基础模型结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个工具十个参数中两项必填，可先展示简化接口；若用户明确要求某可选过滤条件，仍须正确处理其需求。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02001">原论文</a> · <a href="../../../../agent-research/2610.02001-mingbird/">实现解读</a> · <a href="#qa-5fd8604251771df1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mingbird" data-paper-title="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks Agent University of Science and Technology Beijing 2026-10-01 通过 domain 路由和扁平 schema 降低小模型工具调用负担；当模型宣称完成时重新注入原任务与计划并检查产物，发现重复调用或无输出循环时提醒修正，同时为常见 JSON 格式错误提供有限救援。改进的是推理运行框架，不需要把它解释为新的基础模型结构。 L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；L1 可移植运行框架诊断：实际执行工具、检查产物和阻止假完成；使用显式脚本策略，不冒充真实小模型任务成功率。未实现整个 Windows GUI/语音产品、未跑 LRAB/τ²、未接入真实本地 LLM。注册工具仍继承调用方权限，此模块不是隔离沙箱，不应直接注册任意 shell。外部验收不能读取策略未获授权的私密信息并反馈给策略。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 在临时目录中真实写入文件：第一次 finish 因文件不存在被拒绝，随后执行写入，最后重新检查通过。  本地 Agent 运行框架 工具使用 Agent 工具与协作执行：把计划变成可检查的动作 重复调用签名与 prefill 预算分别怎么精确计算？ 签名由工具名和规范 JSON 参数组成，参数顺序不同仍视为同调用，第六次重复在执行前拦截；连续十五次无输出也触发纠偏。prefill 按 UTF-8 字节而非字符计，JSON 救援只解析注册工具、不 eval；本地非完整 GUI 产品或沙箱。 例如两个 JSON 仅键顺序相反不应绕过重复检测；一个汉字通常占多个 UTF-8 字节，按字符数会低估输入预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-797790e34afbed84">重复调用签名与 prefill 预算分别怎么精确计算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amingbird">Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology Beijing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>签名由工具名和规范 JSON 参数组成，参数顺序不同仍视为同调用，第六次重复在执行前拦截；连续十五次无输出也触发纠偏。prefill 按 UTF-8 字节而非字符计，JSON 救援只解析注册工具、不 eval；本地非完整 GUI 产品或沙箱。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个 JSON 仅键顺序相反不应绕过重复检测；一个汉字通常占多个 UTF-8 字节，按字符数会低估输入预算。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02001">原论文</a> · <a href="../../../../agent-research/2610.02001-mingbird/">实现解读</a> · <a href="#qa-797790e34afbed84">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cera-moa" data-paper-title="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents Agent IIIS, Tsinghua University 2026-09-16 用中层隐藏状态估计 Agent 对样本的熟悉度，以累计阈值自适应选专家，并把训练样本定向分配给相应专家。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。  多 Agent 路由与协同进化 Agent 工具与协作执行：把计划变成可检查的动作 CERA-MoA 为什么希望不同专家分担自己更熟悉的样本？ 多专家系统若对所有问题都调用同样数量的相同模型，可能浪费资源，也难形成分工。CERA-MoA 根据样本与专家的熟悉程度组织选择，并让训练分配支持这种差异。熟悉度是用于路由的信号，不等于答案已经正确，最终仍需核验任务结果和总计算开销。 教学例：一个专家更熟悉代码，另一个更熟悉数学，可对不同样本分配不同参与集合；不能仅看角色名称就认定分工有效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-cera-moa-0d23f31e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a2b4d20645f640f0">CERA-MoA 为什么希望不同专家分担自己更熟悉的样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acera-moa">CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · IIIS, Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多专家系统若对所有问题都调用同样数量的相同模型，可能浪费资源，也难形成分工。CERA-MoA 根据样本与专家的熟悉程度组织选择，并让训练分配支持这种差异。熟悉度是用于路由的信号，不等于答案已经正确，最终仍需核验任务结果和总计算开销。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一个专家更熟悉代码，另一个更熟悉数学，可对不同样本分配不同参与集合；不能仅看角色名称就认定分工有效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18779">原论文</a> · <a href="../../../../agent-research/2609.18779-cera-moa/">实现解读</a> · <a href="#qa-a2b4d20645f640f0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cera-moa" data-paper-title="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents Agent IIIS, Tsinghua University 2026-09-16 用中层隐藏状态估计 Agent 对样本的熟悉度，以累计阈值自适应选专家，并把训练样本定向分配给相应专家。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。  多 Agent 路由与协同进化 Agent 工具与协作执行：把计划变成可检查的动作 根据样本熟悉度自适应选专家，为什么还要把训练样本定向分配回专家？ 路由不只在推理时挑人，训练分配会改变各专家之后擅长什么，两侧存在反馈。中层表示估计熟悉度，累计阈值控制本题需要多少专家，再定向训练强化分工；若只改路由却让所有专家始终同样训练，专长结构可能难以持续形成。 例如代码题多分给更熟悉程序的专家，语言题给另一专家；边界不明确的题可激活更多成员，而不是永远固定同一队伍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7a271c323eae1f5d">根据样本熟悉度自适应选专家，为什么还要把训练样本定向分配回专家？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acera-moa">CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · IIIS, Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>路由不只在推理时挑人，训练分配会改变各专家之后擅长什么，两侧存在反馈。中层表示估计熟悉度，累计阈值控制本题需要多少专家，再定向训练强化分工；若只改路由却让所有专家始终同样训练，专长结构可能难以持续形成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如代码题多分给更熟悉程序的专家，语言题给另一专家；边界不明确的题可激活更多成员，而不是永远固定同一队伍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18779">原论文</a> · <a href="../../../../agent-research/2609.18779-cera-moa/">实现解读</a> · <a href="#qa-7a271c323eae1f5d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cera-moa" data-paper-title="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents Agent IIIS, Tsinghua University 2026-09-16 用中层隐藏状态估计 Agent 对样本的熟悉度，以累计阈值自适应选专家，并把训练样本定向分配给相应专家。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。  多 Agent 路由与协同进化 Agent 工具与协作执行：把计划变成可检查的动作 累计阈值自适应选专家与固定 Top-2 有何不同？ 固定 Top-2 每题使用相同数量专家，累计阈值根据分布集中程度调整集合，容易样本可少调用，不确定样本可多覆盖。变化的专家数也改变成本，因此质量比较需计入总计算，不能只看平均路由数就声称更高效。 例如一个专家明显占优时可单独使用，多个专家分数接近时可能需更多协作，而非所有题一律两个。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f4b34cd474558571">累计阈值自适应选专家与固定 Top-2 有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acera-moa">CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · IIIS, Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定 Top-2 每题使用相同数量专家，累计阈值根据分布集中程度调整集合，容易样本可少调用，不确定样本可多覆盖。变化的专家数也改变成本，因此质量比较需计入总计算，不能只看平均路由数就声称更高效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个专家明显占优时可单独使用，多个专家分数接近时可能需更多协作，而非所有题一律两个。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18779">原论文</a> · <a href="../../../../agent-research/2609.18779-cera-moa/">实现解读</a> · <a href="#qa-f4b34cd474558571">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cera-moa" data-paper-title="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents Agent IIIS, Tsinghua University 2026-09-16 用中层隐藏状态估计 Agent 对样本的熟悉度，以累计阈值自适应选专家，并把训练样本定向分配给相应专家。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。本地执行熟悉度路由与定向更新；未训练论文规模专家策略。  多 Agent 路由与协同进化 Agent 工具与协作执行：把计划变成可检查的动作 定向训练分配与仅在推理时路由的更新边界是什么？ CERA-MoA 还将训练样本定向分给对应专家，使路由和专家能力共同演化；只执行选择掩码没有训练这些策略。本地只验证熟悉度路由与定向更新 reference，未训练论文规模专家，三 seed 状态统计不能当真实专家能力进化。 例如记录样本被分给专家甲，不代表甲已经完成梯度训练；必须看到相应参数更新与独立任务验证才能声称学习发生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-64e00323a4a519f4">定向训练分配与仅在推理时路由的更新边界是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acera-moa">CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · IIIS, Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>CERA-MoA 还将训练样本定向分给对应专家，使路由和专家能力共同演化；只执行选择掩码没有训练这些策略。本地只验证熟悉度路由与定向更新 reference，未训练论文规模专家，三 seed 状态统计不能当真实专家能力进化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如记录样本被分给专家甲，不代表甲已经完成梯度训练；必须看到相应参数更新与独立任务验证才能声称学习发生。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18779">原论文</a> · <a href="../../../../agent-research/2609.18779-cera-moa/">实现解读</a> · <a href="#qa-64e00323a4a519f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:repoatlas" data-paper-title="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views Agent Beihang University 2026-09-15 在固定预算下执行 select–project–refresh，把任务相关代码子图同步投影为视觉拓扑与精确文本索引。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  编程 Agent 多模态仓库视图 Agent 工具与协作执行：把计划变成可检查的动作 面对陌生大仓库时，RepoAtlas 希望 Agent 先建立怎样的地图？ 只逐文件阅读容易迷失全局，只有仓库概览又难定位具体符号和依赖。RepoAtlas 研究把结构拓扑与精确文本入口结合，让 Agent 知道模块如何联系，也能回到实际代码检查。地图服务导航，不能替代源代码证据；代码变化后旧结构也可能误导后续修改。 教学例：修登录问题时先看认证模块与 API 的联系，再跳到具体校验函数；只读模块名无法判断真正的条件分支。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-repoatlas-e75f59d2" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8c0ccc4c019a0e9e">面对陌生大仓库时，RepoAtlas 希望 Agent 先建立怎样的地图？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arepoatlas">RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只逐文件阅读容易迷失全局，只有仓库概览又难定位具体符号和依赖。RepoAtlas 研究把结构拓扑与精确文本入口结合，让 Agent 知道模块如何联系，也能回到实际代码检查。地图服务导航，不能替代源代码证据；代码变化后旧结构也可能误导后续修改。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：修登录问题时先看认证模块与 API 的联系，再跳到具体校验函数；只读模块名无法判断真正的条件分支。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16936">原论文</a> · <a href="../../../../agent-research/2609.16936-repoatlas/">实现解读</a> · <a href="#qa-8c0ccc4c019a0e9e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:repoatlas" data-paper-title="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views Agent Beihang University 2026-09-15 在固定预算下执行 select–project–refresh，把任务相关代码子图同步投影为视觉拓扑与精确文本索引。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  编程 Agent 多模态仓库视图 Agent 工具与协作执行：把计划变成可检查的动作 视觉拓扑与精确文本索引为什么要同步 refresh？ 拓扑展示模块依赖，文本索引负责定位可编辑的真实符号，两者一旦不同步，Agent 可能沿正确图找到过期文件。select–project–refresh 在预算内选择任务相关子图并维护双视图，提供的是共同来源的导航接口，不是用一张漂亮架构图替代源码证据。 例如函数被移动到新模块，图中调用边和文本路径都应更新；只刷新其中一侧会让后续检索指向已经不存在的位置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-5335c0c305107d48">视觉拓扑与精确文本索引为什么要同步 refresh？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arepoatlas">RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>拓扑展示模块依赖，文本索引负责定位可编辑的真实符号，两者一旦不同步，Agent 可能沿正确图找到过期文件。select–project–refresh 在预算内选择任务相关子图并维护双视图，提供的是共同来源的导航接口，不是用一张漂亮架构图替代源码证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如函数被移动到新模块，图中调用边和文本路径都应更新；只刷新其中一侧会让后续检索指向已经不存在的位置。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16936">原论文</a> · <a href="../../../../agent-research/2609.16936-repoatlas/">实现解读</a> · <a href="#qa-5335c0c305107d48">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:repoatlas" data-paper-title="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views Agent Beihang University 2026-09-15 在固定预算下执行 select–project–refresh，把任务相关代码子图同步投影为视觉拓扑与精确文本索引。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  编程 Agent 多模态仓库视图 Agent 工具与协作执行：把计划变成可检查的动作 任务相关代码子图与全仓库摘要有什么取舍？ 子图在预算内保留当前任务最相关关系，减少无关信息，却可能漏掉远处依赖；全仓库摘要覆盖广但粒度粗。选择应随实现和反馈刷新，不能一次截图后永远复用，也不能把视觉图存在直接当作代码理解提升。 例如修改认证函数需带入调用方与配置，若最初只看单文件，后续测试反馈可要求扩展子图。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-054bffbc80cbfc11">任务相关代码子图与全仓库摘要有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arepoatlas">RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>子图在预算内保留当前任务最相关关系，减少无关信息，却可能漏掉远处依赖；全仓库摘要覆盖广但粒度粗。选择应随实现和反馈刷新，不能一次截图后永远复用，也不能把视觉图存在直接当作代码理解提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如修改认证函数需带入调用方与配置，若最初只看单文件，后续测试反馈可要求扩展子图。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16936">原论文</a> · <a href="../../../../agent-research/2609.16936-repoatlas/">实现解读</a> · <a href="#qa-054bffbc80cbfc11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:repoatlas" data-paper-title="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views Agent Beihang University 2026-09-15 在固定预算下执行 select–project–refresh，把任务相关代码子图同步投影为视觉拓扑与精确文本索引。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。本地只使用公开 observation 构造有界文本视图；未宣称接入真实 SWE-bench 浏览器环境。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  编程 Agent 多模态仓库视图 Agent 工具与协作执行：把计划变成可检查的动作 本地有界文本视图是否已实现真实 SWE-bench 多模态仓库环境？ 没有。本地只用公开 observation 构造预算内文本视图及选择刷新状态，不声称真实浏览器或 SWE-bench 接入。索引、边与预算可验证，但视觉拓扑生成、模型消费和真实代码修改结果需要独立执行证据，不能由 fixture 直接补齐。 例如输出十个节点和源位置只说明视图数据存在，没有模型看图并修复 issue，就不能报告仓库任务能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4e19879cd431db5b">本地有界文本视图是否已实现真实 SWE-bench 多模态仓库环境？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Arepoatlas">RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Beihang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地只用公开 observation 构造预算内文本视图及选择刷新状态，不声称真实浏览器或 SWE-bench 接入。索引、边与预算可验证，但视觉拓扑生成、模型消费和真实代码修改结果需要独立执行证据，不能由 fixture 直接补齐。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如输出十个节点和源位置只说明视图数据存在，没有模型看图并修复 issue，就不能报告仓库任务能力。</p>
<p class="ar-learning-sources">依据：核心公式与实现对应、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.16936">原论文</a> · <a href="../../../../agent-research/2609.16936-repoatlas/">实现解读</a> · <a href="#qa-4e19879cd431db5b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hcrg" data-paper-title="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration Agent Google Cloud 2026-09-11 HCRG 用 AST 提取 INHERITS/CALLS/IMPORTS，缓存全局架构骨架，按父依赖先后迁移，三跳取回结构上下文。原文对照是 800 字符/150 overlap/top-5 向量 RAG。§3–4 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0，仅 Python AST 支持的 graph 子系统。不是 Java tree-sitter 管线或真实 LLM 跨语言迁移复现。完整实验：成本过高，不复现（审查 DONE）。8 项 Python 自建源码机制测试通过：跨模块继承、三跳边界、签名骨架、父依赖顺序、显式循环组、缓存与部分静态指标，以及未导入跨模块同名、参数/局部变量shadow、歧义和外部依赖保留。诊断记录  代码 Agent 图检索 代码迁移 Agent 工具与协作执行：把计划变成可检查的动作 为什么代码迁移要先识别父依赖，再迁移调用者？ 父类、导入或被调用接口影响后续代码假设，先处理可解析父依赖可提供更稳定上下文。HCRG 从 AST 构建关系与架构骨架，最多三跳取结构证据；静态图不能覆盖动态调用，不能将未解析符号猜成全仓库同名对象。 例如子类依赖父类构造函数签名，先确定父类迁移接口，再写子类更容易避免重复或不一致定义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-hcrg-d21831b9" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0f0b7b0eab559fdf">为什么代码迁移要先识别父依赖，再迁移调用者？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahcrg">Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>父类、导入或被调用接口影响后续代码假设，先处理可解析父依赖可提供更稳定上下文。HCRG 从 AST 构建关系与架构骨架，最多三跳取结构证据；静态图不能覆盖动态调用，不能将未解析符号猜成全仓库同名对象。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如子类依赖父类构造函数签名，先确定父类迁移接口，再写子类更容易避免重复或不一致定义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12464">原论文</a> · <a href="../../../../agent-research/2609.12464-hcrg/">实现解读</a> · <a href="#qa-0f0b7b0eab559fdf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hcrg" data-paper-title="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration Agent Google Cloud 2026-09-11 HCRG 用 AST 提取 INHERITS/CALLS/IMPORTS，缓存全局架构骨架，按父依赖先后迁移，三跳取回结构上下文。原文对照是 800 字符/150 overlap/top-5 向量 RAG。§3–4 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0，仅 Python AST 支持的 graph 子系统。不是 Java tree-sitter 管线或真实 LLM 跨语言迁移复现。完整实验：成本过高，不复现（审查 DONE）。8 项 Python 自建源码机制测试通过：跨模块继承、三跳边界、签名骨架、父依赖顺序、显式循环组、缓存与部分静态指标，以及未导入跨模块同名、参数/局部变量shadow、歧义和外部依赖保留。诊断记录  代码 Agent 图检索 代码迁移 Agent 工具与协作执行：把计划变成可检查的动作 依赖图出现环时，为什么不能假称仍有逐节点的父优先拓扑顺序？ 有向环中的节点互相依赖，不存在满足所有边的线性先后。应识别强连通分组，把组间依赖排序与组内迁移问题分开；AST 结构上下文能够揭示这种限制，却不会自动给出论文未定义的破环算法，不能用任意顺序冒充精确依赖处理。 例如 A 调 B、B 又导入 A，应作为循环组一起分析；先迁移 A 再说所有父依赖已完成，会与图的实际关系矛盾。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-62471e72ac894fa6">依赖图出现环时，为什么不能假称仍有逐节点的父优先拓扑顺序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahcrg">Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>有向环中的节点互相依赖，不存在满足所有边的线性先后。应识别强连通分组，把组间依赖排序与组内迁移问题分开；AST 结构上下文能够揭示这种限制，却不会自动给出论文未定义的破环算法，不能用任意顺序冒充精确依赖处理。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 A 调 B、B 又导入 A，应作为循环组一起分析；先迁移 A 再说所有父依赖已完成，会与图的实际关系矛盾。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12464">原论文</a> · <a href="../../../../agent-research/2609.12464-hcrg/">实现解读</a> · <a href="#qa-62471e72ac894fa6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hcrg" data-paper-title="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration Agent Google Cloud 2026-09-11 HCRG 用 AST 提取 INHERITS/CALLS/IMPORTS，缓存全局架构骨架，按父依赖先后迁移，三跳取回结构上下文。原文对照是 800 字符/150 overlap/top-5 向量 RAG。§3–4 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0，仅 Python AST 支持的 graph 子系统。不是 Java tree-sitter 管线或真实 LLM 跨语言迁移复现。完整实验：成本过高，不复现（审查 DONE）。8 项 Python 自建源码机制测试通过：跨模块继承、三跳边界、签名骨架、父依赖顺序、显式循环组、缓存与部分静态指标，以及未导入跨模块同名、参数/局部变量shadow、歧义和外部依赖保留。诊断记录  代码 Agent 图检索 代码迁移 Agent 工具与协作执行：把计划变成可检查的动作 三跳结构上下文与 800 字符向量 chunk 检索有什么差别？ 向量 chunk 依文字相似返回局部片段，结构检索沿继承、调用、导入关系获取依赖证据，可能找出措辞不同却执行相关的代码。两者各有遗漏边界，论文单仓库部分指标还下降，不能将结构路线概括为所有迁移质量全面更好。 例如工具函数名和当前问题词汇不相似，但被待迁移函数直接调用，结构边可帮助把它纳入上下文。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-61a331bb82962207">三跳结构上下文与 800 字符向量 chunk 检索有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahcrg">Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>向量 chunk 依文字相似返回局部片段，结构检索沿继承、调用、导入关系获取依赖证据，可能找出措辞不同却执行相关的代码。两者各有遗漏边界，论文单仓库部分指标还下降，不能将结构路线概括为所有迁移质量全面更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具函数名和当前问题词汇不相似，但被待迁移函数直接调用，结构边可帮助把它纳入上下文。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12464">原论文</a> · <a href="../../../../agent-research/2609.12464-hcrg/">实现解读</a> · <a href="#qa-61a331bb82962207">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hcrg" data-paper-title="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration Agent Google Cloud 2026-09-11 HCRG 用 AST 提取 INHERITS/CALLS/IMPORTS，缓存全局架构骨架，按父依赖先后迁移，三跳取回结构上下文。原文对照是 800 字符/150 overlap/top-5 向量 RAG。§3–4 完整实验：成本过高，不复现（审查 DONE）。诊断记录 component_only / L0，仅 Python AST 支持的 graph 子系统。不是 Java tree-sitter 管线或真实 LLM 跨语言迁移复现。完整实验：成本过高，不复现（审查 DONE）。8 项 Python 自建源码机制测试通过：跨模块继承、三跳边界、签名骨架、父依赖顺序、显式循环组、缓存与部分静态指标，以及未导入跨模块同名、参数/局部变量shadow、歧义和外部依赖保留。诊断记录  代码 Agent 图检索 代码迁移 Agent 工具与协作执行：把计划变成可检查的动作 静态建图遇到局部变量 shadow 或未解析符号时，应怎样避免造出错误依赖？ 同名不代表同一个定义，局部绑定会遮蔽全局名字，无法解析的调用也不能直接连到仓库里任意同名节点。实现应保留作用域边界和未解析信息，再在可确定的结构上取上下文。本地只支持受限 Python AST，不覆盖所有动态调用或原文其他语言的迁移环境。 教学例：函数内部把全局工具名赋成局部对象，后续调用应按局部绑定解释；不能因仓库有同名函数就连成全局调用边。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-febd84dd63974652">静态建图遇到局部变量 shadow 或未解析符号时，应怎样避免造出错误依赖？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahcrg">Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同名不代表同一个定义，局部绑定会遮蔽全局名字，无法解析的调用也不能直接连到仓库里任意同名节点。实现应保留作用域边界和未解析信息，再在可确定的结构上取上下文。本地只支持受限 Python AST，不覆盖所有动态调用或原文其他语言的迁移环境。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：函数内部把全局工具名赋成局部对象，后续调用应按局部绑定解释；不能因仓库有同名函数就连成全局调用边。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.12464">原论文</a> · <a href="../../../../agent-research/2609.12464-hcrg/">实现解读</a> · <a href="#qa-febd84dd63974652">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:feedback-scaffold" data-paper-title="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks Agent Fudan University 2026-09-08 论文指出统一反馈不适合整个探索过程：早期能力不足时使用 action guidance 降低搜索难度，后期则改为 observation enrichment，让 Agent 自己选择动作，避免长期依赖示范。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现早期公开动作引导、后期观察增强的阶段切换；不读取 gold plan。三种子结果见 metrics/mini-suite-seeds42-44.json。第一步只可采用公开 observation 中明确给出的 workflow；后续仅加入状态摘要，隐藏 AgentTask.plan 从不进入策略。当前未训练 LLM，也没有真实环境 rollout。  环境反馈脚手架 Agent 工具与协作执行：把计划变成可检查的动作 训练较弱的长程 Agent 时，为什么“完全放手探索”和“始终告诉答案”都有困难？ 完全放手可能让策略很少得到可学习的成功经验，始终给正确动作又可能让它只学会依赖外部帮助。Feedback Scaffold 研究在训练中逐步调整支持方式，让早期更容易起步，后期仍需自己决策。评价目标应是撤去相应支架后的能力，不能把受指导完成当成自主解决。 教学例：新手起初需要示范下一步，熟悉后只给检查结果让其判断；若测试时继续替它选动作，就测不到独立处理能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-feedback-scaffold-b914bba8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-86b6f2fda9fa582b">训练较弱的长程 Agent 时，为什么“完全放手探索”和“始终告诉答案”都有困难？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afeedback-scaffold">Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完全放手可能让策略很少得到可学习的成功经验，始终给正确动作又可能让它只学会依赖外部帮助。Feedback Scaffold 研究在训练中逐步调整支持方式，让早期更容易起步，后期仍需自己决策。评价目标应是撤去相应支架后的能力，不能把受指导完成当成自主解决。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：新手起初需要示范下一步，熟悉后只给检查结果让其判断；若测试时继续替它选动作，就测不到独立处理能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08404">原论文</a> · <a href="../../../../agent-research/2609.08404-feedback-scaffold/">实现解读</a> · <a href="#qa-86b6f2fda9fa582b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:feedback-scaffold" data-paper-title="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks Agent Fudan University 2026-09-08 论文指出统一反馈不适合整个探索过程：早期能力不足时使用 action guidance 降低搜索难度，后期则改为 observation enrichment，让 Agent 自己选择动作，避免长期依赖示范。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现早期公开动作引导、后期观察增强的阶段切换；不读取 gold plan。三种子结果见 metrics/mini-suite-seeds42-44.json。第一步只可采用公开 observation 中明确给出的 workflow；后续仅加入状态摘要，隐藏 AgentTask.plan 从不进入策略。当前未训练 LLM，也没有真实环境 rollout。  环境反馈脚手架 Agent 工具与协作执行：把计划变成可检查的动作 为什么早期用 action guidance，后期要转向 observation enrichment？ 能力不足时直接引导动作能降低探索难度，帮助获得可学习轨迹；长期持续示范却可能让策略依赖外部答案。后期改为丰富观察，把取证支持留下、动作选择交还 Agent，逐步降低脚手架依赖；两阶段反馈角色不同，不能用统一强提示覆盖所有训练过程。 例如初学开柜时先提示“找钥匙”，熟练后只补充锁的状态，让 Agent 自己决定下一步，而非永远告诉它完整动作序列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-32e4e27887fc3581">为什么早期用 action guidance，后期要转向 observation enrichment？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afeedback-scaffold">Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>能力不足时直接引导动作能降低探索难度，帮助获得可学习轨迹；长期持续示范却可能让策略依赖外部答案。后期改为丰富观察，把取证支持留下、动作选择交还 Agent，逐步降低脚手架依赖；两阶段反馈角色不同，不能用统一强提示覆盖所有训练过程。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如初学开柜时先提示“找钥匙”，熟练后只补充锁的状态，让 Agent 自己决定下一步，而非永远告诉它完整动作序列。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08404">原论文</a> · <a href="../../../../agent-research/2609.08404-feedback-scaffold/">实现解读</a> · <a href="#qa-32e4e27887fc3581">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:feedback-scaffold" data-paper-title="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks Agent Fudan University 2026-09-08 论文指出统一反馈不适合整个探索过程：早期能力不足时使用 action guidance 降低搜索难度，后期则改为 observation enrichment，让 Agent 自己选择动作，避免长期依赖示范。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现早期公开动作引导、后期观察增强的阶段切换；不读取 gold plan。三种子结果见 metrics/mini-suite-seeds42-44.json。第一步只可采用公开 observation 中明确给出的 workflow；后续仅加入状态摘要，隐藏 AgentTask.plan 从不进入策略。当前未训练 LLM，也没有真实环境 rollout。  环境反馈脚手架 Agent 工具与协作执行：把计划变成可检查的动作 带脚手架完成任务与撤去脚手架后的自主完成，为什么需要分开评价？ 脚手架可能直接减少动作选择难度或补充额外证据，成功既反映策略也反映外部支持。撤去后才可观察训练是否留下可迁移的决策能力。比较时要说明哪些帮助仍然可见，不能把不同信息条件的分数混用；本地阶段调度诊断尤其不能替代真实训练迁移实验。 教学例：训练时提示“先读配置”，测试若仍给同一正确提示，只能说明会跟随；自主测试则需要模型自己发现应查配置。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c298fb923271d9a8">带脚手架完成任务与撤去脚手架后的自主完成，为什么需要分开评价？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afeedback-scaffold">Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>脚手架可能直接减少动作选择难度或补充额外证据，成功既反映策略也反映外部支持。撤去后才可观察训练是否留下可迁移的决策能力。比较时要说明哪些帮助仍然可见，不能把不同信息条件的分数混用；本地阶段调度诊断尤其不能替代真实训练迁移实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：训练时提示“先读配置”，测试若仍给同一正确提示，只能说明会跟随；自主测试则需要模型自己发现应查配置。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08404">原论文</a> · <a href="../../../../agent-research/2609.08404-feedback-scaffold/">实现解读</a> · <a href="#qa-c298fb923271d9a8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:feedback-scaffold" data-paper-title="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks Agent Fudan University 2026-09-08 论文指出统一反馈不适合整个探索过程：早期能力不足时使用 action guidance 降低搜索难度，后期则改为 observation enrichment，让 Agent 自己选择动作，避免长期依赖示范。 复现级别：公开观察解析诊断。复现级别：公开观察解析诊断。实现早期公开动作引导、后期观察增强的阶段切换；不读取 gold plan。三种子结果见 metrics/mini-suite-seeds42-44.json。第一步只可采用公开 observation 中明确给出的 workflow；后续仅加入状态摘要，隐藏 AgentTask.plan 从不进入策略。当前未训练 LLM，也没有真实环境 rollout。  环境反馈脚手架 Agent 工具与协作执行：把计划变成可检查的动作 本地第一步 workflow 可以从隐藏 AgentTask.plan 读取吗？ 不能。只能使用公开 observation 明确给出的 workflow，后续仅加入状态摘要，隐藏计划不进入策略。当前未训练 LLM 或执行真实环境 rollout，受控支架路径只能验证信息隔离与阶段调度，不能把 oracle 指导造成满分写成学会长程任务。 例如评测文件含标准三步计划，不能伪装成环境提示送给模型；否则不是观察增强而是直接泄露答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e00f463b6f22a769">本地第一步 workflow 可以从隐藏 AgentTask.plan 读取吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afeedback-scaffold">Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。只能使用公开 observation 明确给出的 workflow，后续仅加入状态摘要，隐藏计划不进入策略。当前未训练 LLM 或执行真实环境 rollout，受控支架路径只能验证信息隔离与阶段调度，不能把 oracle 指导造成满分写成学会长程任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如评测文件含标准三步计划，不能伪装成环境提示送给模型；否则不是观察增强而是直接泄露答案。</p>
<p class="ar-learning-sources">依据：本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.08404">原论文</a> · <a href="../../../../agent-research/2609.08404-feedback-scaffold/">实现解读</a> · <a href="#qa-e00f463b6f22a769">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:swe-prime" data-paper-title="SWE-Prime: Fewer Trajectories, Better Performance" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-Prime: Fewer Trajectories, Better Performance Agent Sun Yat-sen University 2026-08-27 成功轨迹仍可能冗余、危险或不可学习。SWE-Prime 先按过程、结果和代表性选轨迹，再按贡献、可学习性和风险选语义段；上下文完整保留，但只对选中段计算 SFT loss。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现轨迹筛选、语义段筛选和 loss mask。未训练代码 LLM，也未运行官方 SWE-Bench；本地只比较相同 observation/tool 接口下的筛选策略。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5497。  软件轨迹筛选 Agent 工具与协作执行：把计划变成可检查的动作 成功轨迹为什么仍可能不适合作为全部 SFT 目标？ 成功可能包含冗余试错、危险命令或对当前模型不可学习的步骤，照单全收会训练这些行为。SWE-Prime 先选过程、结果和代表性，再选贡献、可学习性与风险较合适的语义段；成功是必要证据之一，不是所有 token 都值得模仿的保证。 例如最后修好 bug 的轨迹曾误删文件再恢复，成功结果并不意味着误删步骤也应被当成正面示范。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-swe-prime-e014601a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cabb17e601059f07">成功轨迹为什么仍可能不适合作为全部 SFT 目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aswe-prime">SWE-Prime: Fewer Trajectories, Better Performance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>成功可能包含冗余试错、危险命令或对当前模型不可学习的步骤，照单全收会训练这些行为。SWE-Prime 先选过程、结果和代表性，再选贡献、可学习性与风险较合适的语义段；成功是必要证据之一，不是所有 token 都值得模仿的保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最后修好 bug 的轨迹曾误删文件再恢复，成功结果并不意味着误删步骤也应被当成正面示范。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27449">原论文</a> · <a href="../../../../agent-research/2608.27449-swe-prime/">实现解读</a> · <a href="#qa-cabb17e601059f07">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:swe-prime" data-paper-title="SWE-Prime: Fewer Trajectories, Better Performance" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-Prime: Fewer Trajectories, Better Performance Agent Sun Yat-sen University 2026-08-27 成功轨迹仍可能冗余、危险或不可学习。SWE-Prime 先按过程、结果和代表性选轨迹，再按贡献、可学习性和风险选语义段；上下文完整保留，但只对选中段计算 SFT loss。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现轨迹筛选、语义段筛选和 loss mask。未训练代码 LLM，也未运行官方 SWE-Bench；本地只比较相同 observation/tool 接口下的筛选策略。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5497。  软件轨迹筛选 Agent 工具与协作执行：把计划变成可检查的动作 为什么上下文完整保留，却只对选中语义段计算 SFT loss？ 未选段仍可能是理解后续行为所需的因果背景，删除会造成不完整前缀；但其生成行为可能冗余、危险或不值得模仿。mask 把“提供上下文”与“作为学习目标”分开，让模型读到真实过程而只学习有贡献且可学的部分，成功轨迹也不必全量监督。 例如前面一次错误命令解释了后续修复原因，可保留给模型看，却不奖励重新生成那条危险命令。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-09148f0475ab00b9">为什么上下文完整保留，却只对选中语义段计算 SFT loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aswe-prime">SWE-Prime: Fewer Trajectories, Better Performance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>未选段仍可能是理解后续行为所需的因果背景，删除会造成不完整前缀；但其生成行为可能冗余、危险或不值得模仿。mask 把“提供上下文”与“作为学习目标”分开，让模型读到真实过程而只学习有贡献且可学的部分，成功轨迹也不必全量监督。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前面一次错误命令解释了后续修复原因，可保留给模型看，却不奖励重新生成那条危险命令。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27449">原论文</a> · <a href="../../../../agent-research/2608.27449-swe-prime/">实现解读</a> · <a href="#qa-09148f0475ab00b9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:swe-prime" data-paper-title="SWE-Prime: Fewer Trajectories, Better Performance" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-Prime: Fewer Trajectories, Better Performance Agent Sun Yat-sen University 2026-08-27 成功轨迹仍可能冗余、危险或不可学习。SWE-Prime 先按过程、结果和代表性选轨迹，再按贡献、可学习性和风险选语义段；上下文完整保留，但只对选中段计算 SFT loss。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现轨迹筛选、语义段筛选和 loss mask。未训练代码 LLM，也未运行官方 SWE-Bench；本地只比较相同 observation/tool 接口下的筛选策略。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5497。  软件轨迹筛选 Agent 工具与协作执行：把计划变成可检查的动作 整条轨迹筛选与轨迹内部语义段筛选，各解决哪一层数据质量问题？ 轨迹级筛选关注结果、过程和代表性，先决定哪些完整经历值得保留；段级筛选再检查其中行为的贡献、可学习性和风险。优质轨迹仍可能含局部冗余，优秀片段也可能出自缺乏有效全局结果的记录。分层处理区分样本选择与监督目标，不是简单只留成功答案。 教学例：一次修复总体通过测试，但中途有无关依赖安装；可保留完整执行作为上下文，同时不把那段行为设为模仿目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fe246fc75fa9c390">整条轨迹筛选与轨迹内部语义段筛选，各解决哪一层数据质量问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aswe-prime">SWE-Prime: Fewer Trajectories, Better Performance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>轨迹级筛选关注结果、过程和代表性，先决定哪些完整经历值得保留；段级筛选再检查其中行为的贡献、可学习性和风险。优质轨迹仍可能含局部冗余，优秀片段也可能出自缺乏有效全局结果的记录。分层处理区分样本选择与监督目标，不是简单只留成功答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一次修复总体通过测试，但中途有无关依赖安装；可保留完整执行作为上下文，同时不把那段行为设为模仿目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27449">原论文</a> · <a href="../../../../agent-research/2608.27449-swe-prime/">实现解读</a> · <a href="#qa-fe246fc75fa9c390">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:swe-prime" data-paper-title="SWE-Prime: Fewer Trajectories, Better Performance" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-Prime: Fewer Trajectories, Better Performance Agent Sun Yat-sen University 2026-08-27 成功轨迹仍可能冗余、危险或不可学习。SWE-Prime 先按过程、结果和代表性选轨迹，再按贡献、可学习性和风险选语义段；上下文完整保留，但只对选中段计算 SFT loss。 复现级别：核心机制 + L2.1 无 oracle 评测。复现级别：核心机制 + L2.1 无 oracle 评测。实现轨迹筛选、语义段筛选和 loss mask。未训练代码 LLM，也未运行官方 SWE-Bench；本地只比较相同 observation/tool 接口下的筛选策略。ToolRoute-L2.1 三 seed：joint success 0.7708，plan F1 0.8004，平均成本 4.5497。  软件轨迹筛选 Agent 工具与协作执行：把计划变成可检查的动作 本地筛选策略结果能否说明代码 LLM 已训练或 SWE-bench 已运行？ 不能。本地在相同 observation/tool 接口比较筛选策略，未训练代码模型或运行官方 SWE-bench。实现应检查 loss mask 只覆盖目标段、上下文仍完整，以及 train/validation/test 隔离；小型工具路由指标不能改名为代码修复提升。 例如筛掉高风险片段后工具路线更稳定，最多支持本地协议观察，不能据此声称复刻原文只用一成代码轨迹的结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-7dac67bcfc67dd77">本地筛选策略结果能否说明代码 LLM 已训练或 SWE-bench 已运行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aswe-prime">SWE-Prime: Fewer Trajectories, Better Performance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Sun Yat-sen University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地在相同 observation/tool 接口比较筛选策略，未训练代码模型或运行官方 SWE-bench。实现应检查 loss mask 只覆盖目标段、上下文仍完整，以及 train/validation/test 隔离；小型工具路由指标不能改名为代码修复提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如筛掉高风险片段后工具路线更稳定，最多支持本地协议观察，不能据此声称复刻原文只用一成代码轨迹的结果。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27449">原论文</a> · <a href="../../../../agent-research/2608.27449-swe-prime/">实现解读</a> · <a href="#qa-7dac67bcfc67dd77">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:adavdr" data-paper-title="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research Agent Accio Team, Alibaba Group 2026-08-26 先以目标模型能力过滤不必要工具调用，只在中间证据不可靠时回退反思；SFT 后用 redundancy-aware reward 做 RL，兼顾视频理解、外部检索和调用成本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。AdaVDR 在无 oracle 的状态化工具环境中执行候选验证、失败反思与回退。ToolRoute-L2.1 三 seed 的 joint success 为 0.8167，plan step F1 为 0.8366，平均成本 5.0577；  视频研究自适应工具与反思 Agent 工具与协作执行：把计划变成可检查的动作 为什么工具必要性要相对目标模型能力判断？ 模型自身已能回答的部分不必重复外部调用，确实缺信息时才用工具。必要性因模型能力和当前证据而变，不是全局禁止某工具；中间证据不可靠再反思回退，避免只按调用数量最少优化而漏掉必需验证。 例如清晰画面可直接读出颜色，细小文字则可能需要放大或检索；换一个视觉能力较弱模型，必要性边界会改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-adavdr-576e1cf8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ac1cf4aa14f91dfb">为什么工具必要性要相对目标模型能力判断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aadavdr">AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Accio Team, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型自身已能回答的部分不必重复外部调用，确实缺信息时才用工具。必要性因模型能力和当前证据而变，不是全局禁止某工具；中间证据不可靠再反思回退，避免只按调用数量最少优化而漏掉必需验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如清晰画面可直接读出颜色，细小文字则可能需要放大或检索；换一个视觉能力较弱模型，必要性边界会改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25559">原论文</a> · <a href="../../../../agent-research/2608.25559-adavdr/">实现解读</a> · <a href="#qa-ac1cf4aa14f91dfb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:adavdr" data-paper-title="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research Agent Accio Team, Alibaba Group 2026-08-26 先以目标模型能力过滤不必要工具调用，只在中间证据不可靠时回退反思；SFT 后用 redundancy-aware reward 做 RL，兼顾视频理解、外部检索和调用成本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。AdaVDR 在无 oracle 的状态化工具环境中执行候选验证、失败反思与回退。ToolRoute-L2.1 三 seed 的 joint success 为 0.8167，plan step F1 为 0.8366，平均成本 5.0577；  视频研究自适应工具与反思 Agent 工具与协作执行：把计划变成可检查的动作 为什么工具必要性判断与证据不可靠时的回退反思要分开？ 前者决定是否需要外部取证，后者在已取得信息后判断是否值得重新检查，两者面对不同失败点。按能力过滤无必要调用可节省成本，冗余惩罚再约束训练；若为了少调用而无视不可靠证据，也会牺牲视频研究结果，不能把调用数最低直接当最优。 例如模型能直接判断视频有人跑步就不搜索网页，但人物身份线索矛盾时应回退核查，不能机械坚持首次结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-88d371dfdcbc173d">为什么工具必要性判断与证据不可靠时的回退反思要分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aadavdr">AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Accio Team, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者决定是否需要外部取证，后者在已取得信息后判断是否值得重新检查，两者面对不同失败点。按能力过滤无必要调用可节省成本，冗余惩罚再约束训练；若为了少调用而无视不可靠证据，也会牺牲视频研究结果，不能把调用数最低直接当最优。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型能直接判断视频有人跑步就不搜索网页，但人物身份线索矛盾时应回退核查，不能机械坚持首次结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25559">原论文</a> · <a href="../../../../agent-research/2608.25559-adavdr/">实现解读</a> · <a href="#qa-88d371dfdcbc173d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:adavdr" data-paper-title="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research Agent Accio Team, Alibaba Group 2026-08-26 先以目标模型能力过滤不必要工具调用，只在中间证据不可靠时回退反思；SFT 后用 redundancy-aware reward 做 RL，兼顾视频理解、外部检索和调用成本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。AdaVDR 在无 oracle 的状态化工具环境中执行候选验证、失败反思与回退。ToolRoute-L2.1 三 seed 的 joint success 为 0.8167，plan step F1 为 0.8366，平均成本 5.0577；  视频研究自适应工具与反思 Agent 工具与协作执行：把计划变成可检查的动作 redundancy-aware reward 与一律惩罚所有调用有什么差别？ 冗余惩罚针对不必要或重复调用，保留有助回答的工具价值；一律惩罚可能让策略为省成本拒绝取证。需要连同答案奖励和可靠性反思检查，调用更少不保证更好，失败恢复或 verifier 也会带来必要额外成本。 例如第二次相同搜索没有新信息可算冗余，但核对冲突来源的额外搜索可能正是保证答案可靠的关键。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e89b590dd2f51e78">redundancy-aware reward 与一律惩罚所有调用有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aadavdr">AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Accio Team, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>冗余惩罚针对不必要或重复调用，保留有助回答的工具价值；一律惩罚可能让策略为省成本拒绝取证。需要连同答案奖励和可靠性反思检查，调用更少不保证更好，失败恢复或 verifier 也会带来必要额外成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如第二次相同搜索没有新信息可算冗余，但核对冲突来源的额外搜索可能正是保证答案可靠的关键。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25559">原论文</a> · <a href="../../../../agent-research/2608.25559-adavdr/">实现解读</a> · <a href="#qa-e89b590dd2f51e78">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:adavdr" data-paper-title="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research Agent Accio Team, Alibaba Group 2026-08-26 先以目标模型能力过滤不必要工具调用，只在中间证据不可靠时回退反思；SFT 后用 redundancy-aware reward 做 RL，兼顾视频理解、外部检索和调用成本。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。AdaVDR 在无 oracle 的状态化工具环境中执行候选验证、失败反思与回退。ToolRoute-L2.1 三 seed 的 joint success 为 0.8167，plan step F1 为 0.8366，平均成本 5.0577；  视频研究自适应工具与反思 Agent 工具与协作执行：把计划变成可检查的动作 本地 ToolRoute 的较高成功率应怎样与成本和视频边界一起报告？ 必须同时保留额外 verifier 成本，并说明本地是无 oracle 状态化工具环境、未运行原文视频数据与完整 VDR 系统。PlanBench 满分只作机制诊断，不能将回退计数或不同协议成功率写成视频研究能力提升。 例如本地候选验证多花一步换来任务成功，可如实报告这次取舍，不能只摘成功率而宣称同时减少视频工具调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-bebf5ef6d4303580">本地 ToolRoute 的较高成功率应怎样与成本和视频边界一起报告？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aadavdr">AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Accio Team, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>必须同时保留额外 verifier 成本，并说明本地是无 oracle 状态化工具环境、未运行原文视频数据与完整 VDR 系统。PlanBench 满分只作机制诊断，不能将回退计数或不同协议成功率写成视频研究能力提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如本地候选验证多花一步换来任务成功，可如实报告这次取舍，不能只摘成功率而宣称同时减少视频工具调用。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25559">原论文</a> · <a href="../../../../agent-research/2608.25559-adavdr/">实现解读</a> · <a href="#qa-bebf5ef6d4303580">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:progrouter" data-paper-title="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs Agent Aston University 2026-08-26 用多视角 scorer 衡量子任务完成度、进展趋势和状态质量，再由双路径 predictor 估计候选模型的边际进展，以 meta-gate 在质量、时间和长期成本预算间逐步决策。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。ProgRouter 把验证后的工具选择压缩为可复用程序路由，validation/test 冻结路由后再执行。ToolRoute-L2.1 三 seed的 joint success 为 0.7778，plan step F1 为 0.8037，平均成本 4.6324。  在线进展成本路由 Agent 工具与协作执行：把计划变成可检查的动作 ProgRouter 为什么关注同一任务执行过程中不断变化的模型需求？ 复杂任务不同阶段需要的推理强度不同，固定一直用强模型成本高，一直用弱模型又可能卡住。ProgRouter 研究按当前进展选择下一次调用哪个模型，使路由服务于继续推进任务。模型的静态平均准确率不足以说明此刻能带来多少帮助，实际收益还受时间和调用预算限制。 教学例：常规文件定位可交给便宜模型，定位后遇到复杂推断再换模型；不能因为某模型总体排名高就让每一步都调用它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-progrouter-c8bea01c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0b2e86e619f312c8">ProgRouter 为什么关注同一任务执行过程中不断变化的模型需求？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprogrouter">ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Aston University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>复杂任务不同阶段需要的推理强度不同，固定一直用强模型成本高，一直用弱模型又可能卡住。ProgRouter 研究按当前进展选择下一次调用哪个模型，使路由服务于继续推进任务。模型的静态平均准确率不足以说明此刻能带来多少帮助，实际收益还受时间和调用预算限制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：常规文件定位可交给便宜模型，定位后遇到复杂推断再换模型；不能因为某模型总体排名高就让每一步都调用它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25992">原论文</a> · <a href="../../../../agent-research/2608.25992-progrouter/">实现解读</a> · <a href="#qa-0b2e86e619f312c8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:progrouter" data-paper-title="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs Agent Aston University 2026-08-26 用多视角 scorer 衡量子任务完成度、进展趋势和状态质量，再由双路径 predictor 估计候选模型的边际进展，以 meta-gate 在质量、时间和长期成本预算间逐步决策。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。ProgRouter 把验证后的工具选择压缩为可复用程序路由，validation/test 冻结路由后再执行。ToolRoute-L2.1 三 seed的 joint success 为 0.7778，plan step F1 为 0.8037，平均成本 4.6324。  在线进展成本路由 Agent 工具与协作执行：把计划变成可检查的动作 为什么模型路由要预测边际进展，而不只比较各模型的平均准确率？ 不同子任务状态下，强模型可能只比弱模型多推进一点，也可能解决关键阻塞。边际进展结合当前完成度、趋势和质量，才能评价下一次调用的价值，再与时间和长期预算权衡；平均准确率忽略阶段差异，预测分数也仍须由后续执行检验。 例如格式修复时小模型已足够，困难证明阶段强模型才可能带来显著推进；固定每一步都用平均最强者会浪费预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1a4bcdd40231ca7a">为什么模型路由要预测边际进展，而不只比较各模型的平均准确率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprogrouter">ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Aston University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同子任务状态下，强模型可能只比弱模型多推进一点，也可能解决关键阻塞。边际进展结合当前完成度、趋势和质量，才能评价下一次调用的价值，再与时间和长期预算权衡；平均准确率忽略阶段差异，预测分数也仍须由后续执行检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如格式修复时小模型已足够，困难证明阶段强模型才可能带来显著推进；固定每一步都用平均最强者会浪费预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25992">原论文</a> · <a href="../../../../agent-research/2608.25992-progrouter/">实现解读</a> · <a href="#qa-1a4bcdd40231ca7a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:progrouter" data-paper-title="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs Agent Aston University 2026-08-26 用多视角 scorer 衡量子任务完成度、进展趋势和状态质量，再由双路径 predictor 估计候选模型的边际进展，以 meta-gate 在质量、时间和长期成本预算间逐步决策。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。ProgRouter 把验证后的工具选择压缩为可复用程序路由，validation/test 冻结路由后再执行。ToolRoute-L2.1 三 seed的 joint success 为 0.7778，plan step F1 为 0.8037，平均成本 4.6324。  在线进展成本路由 Agent 工具与协作执行：把计划变成可检查的动作 质量、时间与长期成本 meta-gate 相比始终调用最便宜模型有什么取舍？ 最便宜单次调用可能因反复失败增加总成本，meta-gate 以预计进展、调用代价和预算压力共同选择。它也可能为高质量候选支付额外费用，不能只报告调用单价下降；应同时看交付质量、时间和完整预算。 例如便宜模型三轮无进展，换较贵模型一次解决可能总体更省；若贵模型也无进展，则预测应被实际反馈否定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-22fc3889a20630c0">质量、时间与长期成本 meta-gate 相比始终调用最便宜模型有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprogrouter">ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Aston University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最便宜单次调用可能因反复失败增加总成本，meta-gate 以预计进展、调用代价和预算压力共同选择。它也可能为高质量候选支付额外费用，不能只报告调用单价下降；应同时看交付质量、时间和完整预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如便宜模型三轮无进展，换较贵模型一次解决可能总体更省；若贵模型也无进展，则预测应被实际反馈否定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25992">原论文</a> · <a href="../../../../agent-research/2608.25992-progrouter/">实现解读</a> · <a href="#qa-22fc3889a20630c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:progrouter" data-paper-title="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs Agent Aston University 2026-08-26 用多视角 scorer 衡量子任务完成度、进展趋势和状态质量，再由双路径 predictor 估计候选模型的边际进展，以 meta-gate 在质量、时间和长期成本预算间逐步决策。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。ProgRouter 把验证后的工具选择压缩为可复用程序路由，validation/test 冻结路由后再执行。ToolRoute-L2.1 三 seed的 joint success 为 0.7778，plan step F1 为 0.8037，平均成本 4.6324。  在线进展成本路由 Agent 工具与协作执行：把计划变成可检查的动作 本地冻结程序路由与论文多模型进展 predictor 的实现范围相同吗？ 不同。本地将验证后的工具选择压成路由，validation/test 冻结后实际执行，mini-suite 检查 progress/meta-gate 与降级；没有复刻论文模型、服务资源或完整 benchmark。代理成本与程序选择结果不能当作真实能耗焦耳或 citation precision。 例如本地一条路由少读两个候选，不等于真实 HumanEval 工作流节省相同能耗，需要模型和硬件计量才能验证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a1d2177e87e77e3d">本地冻结程序路由与论文多模型进展 predictor 的实现范围相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprogrouter">ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Aston University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同。本地将验证后的工具选择压成路由，validation/test 冻结后实际执行，mini-suite 检查 progress/meta-gate 与降级；没有复刻论文模型、服务资源或完整 benchmark。代理成本与程序选择结果不能当作真实能耗焦耳或 citation precision。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如本地一条路由少读两个候选，不等于真实 HumanEval 工作流节省相同能耗，需要模型和硬件计量才能验证。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25992">原论文</a> · <a href="../../../../agent-research/2608.25992-progrouter/">实现解读</a> · <a href="#qa-a1d2177e87e77e3d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:topas" data-paper-title="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving Agent University of Science and Technology of China 2026-08-26 在共享 KV-cache 预算下，同时估算工作流最长剩余路径与下游 prefix reuse 收益，并纳入 prefix 移动、抢占和 aging，避免只优化局部命中率或单请求进度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TOPAS 在状态化工具环境里先做安全排序与候选压缩，再根据调用反馈恢复。ToolRoute-L2.1 三 seed 的 joint success 为 0.7556，plan step F1 为 0.7887，平均成本 4.5571。  工作流 Prefix-State 调度 Agent 工具与协作执行：把计划变成可检查的动作 TOPAS 为什么关注整个工作流最长剩余路径，而不只看单请求进度？ 一个请求可能阻塞多个下游任务，局部优先会让工作流尾部等待。关键路径估计把依赖和剩余工作纳入调度，再权衡 prefix 复用、移动和抢占成本；目标是整体完成时间，缓存命中率只是其中一个中间量。 例如一个短请求完成后能解锁五个后续节点，即使另一个长请求已跑很多，也可能应先处理这个依赖瓶颈。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-topas-ae42000c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-75c29be356dd9dec">TOPAS 为什么关注整个工作流最长剩余路径，而不只看单请求进度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atopas">TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个请求可能阻塞多个下游任务，局部优先会让工作流尾部等待。关键路径估计把依赖和剩余工作纳入调度，再权衡 prefix 复用、移动和抢占成本；目标是整体完成时间，缓存命中率只是其中一个中间量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个短请求完成后能解锁五个后续节点，即使另一个长请求已跑很多，也可能应先处理这个依赖瓶颈。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25523">原论文</a> · <a href="../../../../agent-research/2608.25523-topas/">实现解读</a> · <a href="#qa-75c29be356dd9dec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:topas" data-paper-title="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving Agent University of Science and Technology of China 2026-08-26 在共享 KV-cache 预算下，同时估算工作流最长剩余路径与下游 prefix reuse 收益，并纳入 prefix 移动、抢占和 aging，避免只优化局部命中率或单请求进度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TOPAS 在状态化工具环境里先做安全排序与候选压缩，再根据调用反馈恢复。ToolRoute-L2.1 三 seed 的 joint success 为 0.7556，plan step F1 为 0.7887，平均成本 4.5571。  工作流 Prefix-State 调度 Agent 工具与协作执行：把计划变成可检查的动作 为什么共享缓存调度不能只追求最高 prefix hit rate？ 缓存命中提高局部复用，却可能让关键路径上的工作流等待，或产生昂贵搬运和抢占。TOPAS 同时估计最长剩余路径、下游复用收益及移动成本，并用 aging 避免长期饥饿；命中率是一项中间指标，不能单独代表多 Agent 任务的总完成时间。 例如反复服务一批高命中小请求，却堵住即将完成的主流程；牺牲一点命中率优先关键路径，可能更早交付整个任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-844b8a90e779e693">为什么共享缓存调度不能只追求最高 prefix hit rate？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atopas">TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>缓存命中提高局部复用，却可能让关键路径上的工作流等待，或产生昂贵搬运和抢占。TOPAS 同时估计最长剩余路径、下游复用收益及移动成本，并用 aging 避免长期饥饿；命中率是一项中间指标，不能单独代表多 Agent 任务的总完成时间。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如反复服务一批高命中小请求，却堵住即将完成的主流程；牺牲一点命中率优先关键路径，可能更早交付整个任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25523">原论文</a> · <a href="../../../../agent-research/2608.25523-topas/">实现解读</a> · <a href="#qa-844b8a90e779e693">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:topas" data-paper-title="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving Agent University of Science and Technology of China 2026-08-26 在共享 KV-cache 预算下，同时估算工作流最长剩余路径与下游 prefix reuse 收益，并纳入 prefix 移动、抢占和 aging，避免只优化局部命中率或单请求进度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TOPAS 在状态化工具环境里先做安全排序与候选压缩，再根据调用反馈恢复。ToolRoute-L2.1 三 seed 的 joint success 为 0.7556，plan step F1 为 0.7887，平均成本 4.5571。  工作流 Prefix-State 调度 Agent 工具与协作执行：把计划变成可检查的动作 关键路径优先与 aging 分别处理整体延迟的哪一种风险？ 关键路径优先关注哪些请求会阻塞工作流完成，aging 则随等待增长提升长期未获资源请求的优先级，防止调度持续偏向其他路线。二者解决依赖瓶颈和公平等待的不同问题，需要与缓存复用及移动成本共同权衡；任何单项优先级都不保证所有任务同时最快。 教学例：短链请求因一直没有缓存命中而反复被跳过，aging 可逐渐提升其机会；另一长链上的阻塞节点仍有关键路径价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b3ba7f4b88395eaa">关键路径优先与 aging 分别处理整体延迟的哪一种风险？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atopas">TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>关键路径优先关注哪些请求会阻塞工作流完成，aging 则随等待增长提升长期未获资源请求的优先级，防止调度持续偏向其他路线。二者解决依赖瓶颈和公平等待的不同问题，需要与缓存复用及移动成本共同权衡；任何单项优先级都不保证所有任务同时最快。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：短链请求因一直没有缓存命中而反复被跳过，aging 可逐渐提升其机会；另一长链上的阻塞节点仍有关键路径价值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25523">原论文</a> · <a href="../../../../agent-research/2608.25523-topas/">实现解读</a> · <a href="#qa-b3ba7f4b88395eaa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:topas" data-paper-title="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving Agent University of Science and Technology of China 2026-08-26 在共享 KV-cache 预算下，同时估算工作流最长剩余路径与下游 prefix reuse 收益，并纳入 prefix 移动、抢占和 aging，避免只优化局部命中率或单请求进度。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TOPAS 在状态化工具环境里先做安全排序与候选压缩，再根据调用反馈恢复。ToolRoute-L2.1 三 seed 的 joint success 为 0.7556，plan step F1 为 0.7887，平均成本 4.5571。  工作流 Prefix-State 调度 Agent 工具与协作执行：把计划变成可检查的动作 本地模拟 prefix hit 与 ToolRoute 结果能证明真实 LLM serving 加速吗？ 不能。受控 mini-suite 只模拟 prefix、关键路径与 aging，状态化工具结果也不含真实 KV serving kernel。原文 mean/p99 JCT 是作者系统实验，需实际请求、内存、移动与墙钟测量；不能用代理 cost 或命中次数直接换算。 例如 cache hit 计数增加三次不等于节省三次相同 prefill 时间，真实收益还取决于前缀长度和调度开销。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-53eb77d8871172b0">本地模拟 prefix hit 与 ToolRoute 结果能证明真实 LLM serving 加速吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atopas">TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Science and Technology of China</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。受控 mini-suite 只模拟 prefix、关键路径与 aging，状态化工具结果也不含真实 KV serving kernel。原文 mean/p99 JCT 是作者系统实验，需实际请求、内存、移动与墙钟测量；不能用代理 cost 或命中次数直接换算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 cache hit 计数增加三次不等于节省三次相同 prefill 时间，真实收益还取决于前缀长度和调度开销。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.25523">原论文</a> · <a href="../../../../agent-research/2608.25523-topas/">实现解读</a> · <a href="#qa-53eb77d8871172b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:traceml" data-paper-title="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development Agent Carnegie Mellon University 2026-08-26 统一记录每个代码版本、得分、动作意图、编辑规模和效果，比较 4465 条人类轨迹与 Agent 轨迹；把人类会交替阶段、回开旧方案的规律蒸馏成 planning prior。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TraceML 策略从训练 split 的失败轨迹写入反思先验，validation/test 只读取先验并通过真实工具反馈推进，不读取隐藏 route 或答案。  ML 开发轨迹规划 Agent 工具与协作执行：把计划变成可检查的动作 TraceML 为什么研究人类开发 ML 方案的全过程，而不只收集最后一个高分模型？ 最终代码和分数看不到开发者如何探索、放弃、回到旧方案或分配实验预算。TraceML 记录决策与版本变化，试图把这些过程变成可研究的规划经验。观察到人类行为规律不等于证明它是最优策略，模型利用这些数据后的能力也需在独立任务验证。 教学例：最终方案用了较小模型，但开发中曾试过大模型并发现瓶颈；只保存最终文件会丢掉为什么转向的关键信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-traceml-cea4f922" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9262e749f8e77b96">TraceML 为什么研究人类开发 ML 方案的全过程，而不只收集最后一个高分模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atraceml">TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终代码和分数看不到开发者如何探索、放弃、回到旧方案或分配实验预算。TraceML 记录决策与版本变化，试图把这些过程变成可研究的规划经验。观察到人类行为规律不等于证明它是最优策略，模型利用这些数据后的能力也需在独立任务验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：最终方案用了较小模型，但开发中曾试过大模型并发现瓶颈；只保存最终文件会丢掉为什么转向的关键信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26086">原论文</a> · <a href="../../../../agent-research/2608.26086-traceml/">实现解读</a> · <a href="#qa-9262e749f8e77b96">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:traceml" data-paper-title="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development Agent Carnegie Mellon University 2026-08-26 统一记录每个代码版本、得分、动作意图、编辑规模和效果，比较 4465 条人类轨迹与 Agent 轨迹；把人类会交替阶段、回开旧方案的规律蒸馏成 planning prior。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TraceML 策略从训练 split 的失败轨迹写入反思先验，validation/test 只读取先验并通过真实工具反馈推进，不读取隐藏 route 或答案。  ML 开发轨迹规划 Agent 工具与协作执行：把计划变成可检查的动作 记录版本、动作意图和编辑规模，为什么比只保存分数曲线更能学习规划规律？ 分数只表示结果，无法区分模型在试新架构、调参还是回退旧方案。把每次修改与意图及效果对应起来，才能观察阶段切换和重开旧路线的策略，再形成规划先验；人类轨迹中的相关规律仍需在 Agent 环境检验，不能直接解释成最优策略。 例如两次分数下降，一次是探索新特征、一次是意外删配置，只有版本和动作记录才能判断该继续尝试还是立即回滚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8d61cb02f607c749">记录版本、动作意图和编辑规模，为什么比只保存分数曲线更能学习规划规律？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atraceml">TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分数只表示结果，无法区分模型在试新架构、调参还是回退旧方案。把每次修改与意图及效果对应起来，才能观察阶段切换和重开旧路线的策略，再形成规划先验；人类轨迹中的相关规律仍需在 Agent 环境检验，不能直接解释成最优策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两次分数下降，一次是探索新特征、一次是意外删配置，只有版本和动作记录才能判断该继续尝试还是立即回滚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26086">原论文</a> · <a href="../../../../agent-research/2608.26086-traceml/">实现解读</a> · <a href="#qa-8d61cb02f607c749">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:traceml" data-paper-title="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development Agent Carnegie Mellon University 2026-08-26 统一记录每个代码版本、得分、动作意图、编辑规模和效果，比较 4465 条人类轨迹与 Agent 轨迹；把人类会交替阶段、回开旧方案的规律蒸馏成 planning prior。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TraceML 策略从训练 split 的失败轨迹写入反思先验，validation/test 只读取先验并通过真实工具反馈推进，不读取隐藏 route 或答案。  ML 开发轨迹规划 Agent 工具与协作执行：把计划变成可检查的动作 人类阶段交替和重新打开旧方案，与单调推进计划有什么不同？ 人类开发可在分析、实现和评测间往返，也会基于新证据重访旧假设；单调计划容易把已放弃方向永久排除。先验可鼓励适时回开，但不能机械要求每题都循环相同次数，行为差距缩小也不等于最终分数一定提升。 例如新验证发现问题来自数据，之前放弃的简单模型可能重新有价值，而不是只继续加复杂度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-07360ef008b25b07">人类阶段交替和重新打开旧方案，与单调推进计划有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atraceml">TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>人类开发可在分析、实现和评测间往返，也会基于新证据重访旧假设；单调计划容易把已放弃方向永久排除。先验可鼓励适时回开，但不能机械要求每题都循环相同次数，行为差距缩小也不等于最终分数一定提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新验证发现问题来自数据，之前放弃的简单模型可能重新有价值，而不是只继续加复杂度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26086">原论文</a> · <a href="../../../../agent-research/2608.26086-traceml/">实现解读</a> · <a href="#qa-07360ef008b25b07">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:traceml" data-paper-title="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development Agent Carnegie Mellon University 2026-08-26 统一记录每个代码版本、得分、动作意图、编辑规模和效果，比较 4465 条人类轨迹与 Agent 轨迹；把人类会交替阶段、回开旧方案的规律蒸馏成 planning prior。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。真实执行论文特有的控制流/目标；未把确定性任务成功率当作论文 benchmark 复现。本地 mini-suite 用公开、确定性的候选/计划任务隔离机制差异；论文 checkpoint、私有训练数据、外部服务和完整 benchmark 均未声称已复刻。TraceML 策略从训练 split 的失败轨迹写入反思先验，validation/test 只读取先验并通过真实工具反馈推进，不读取隐藏 route 或答案。  ML 开发轨迹规划 Agent 工具与协作执行：把计划变成可检查的动作 本地失败反思先验在 validation/test 能继续读隐藏 route 吗？ 不能。先验从训练 split 形成，验证测试只读固定先验并根据真实工具反馈行动，不读隐藏答案或路线。PlanBench 的四阶段与重开计数是机制 smoke，ToolRoute 也非 Kaggle 原文全实验，不能把两套指标混成同一 ML 开发能力。 例如 test 失败后可依据公开错误调整动作，但不能打开 reference plan 来“重开正确方案”，否则先验已变成答案通道。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e992817dbacafea4">本地失败反思先验在 validation/test 能继续读隐藏 route 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atraceml">TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。先验从训练 split 形成，验证测试只读固定先验并根据真实工具反馈行动，不读隐藏答案或路线。PlanBench 的四阶段与重开计数是机制 smoke，ToolRoute 也非 Kaggle 原文全实验，不能把两套指标混成同一 ML 开发能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 test 失败后可依据公开错误调整动作，但不能打开 reference plan 来“重开正确方案”，否则先验已变成答案通道。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26086">原论文</a> · <a href="../../../../agent-research/2608.26086-traceml/">实现解读</a> · <a href="#qa-e992817dbacafea4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:smith" data-paper-title="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification Agent Appier AI Research / National Taiwan University 2026-08-25 现有工具创建通常在推理时让冻结模型写代码，创建者与使用者没有联合信号。SMITH 在同一 policy 中混合 build task（从样例写 schema/backend）和 use task（在 held-out 问题调用池中工具），分别给 schema 合法性、代码执行和最终答案奖励，并用更难问题鼓励可复用抽象。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。同一 Agent 交替 build/use，并独立执行 schema、代码和 outcome 三类 verifier。本地工具为结构化 plan，并真实分开 build/use 状态和三轴 verifier；未运行 Qwen3-4B、可执行 Python sandbox、Reasoning-Gym、TabMWP 或 GQA。PlanBench-mini 120 episodes：生成 12 个工具、复用 108 次，执行 360 个分轴 verifier，joint success 1.0000、平均成本 0.4550。  多维验证工具自进化 Agent 工具与协作执行：把计划变成可检查的动作 SMITH 为什么让 Agent 不只使用现成工具，还学习创建可再用的工具？ 固定工具集未必覆盖新任务需要的处理方式，反复临时写代码又会重复劳动。SMITH 把工具构建与后续使用作为相互关联的任务，使生成的接口和实现接受真实使用检验。能产出代码不代表工具有用，格式、执行结果和下游答案各自都可能失败。 教学例：多次遇到相同数据清洗需求，可以创建专用处理工具；它是否值得保留，要看后来能否正确调用并完成实际清洗。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-smith-3e4d7833" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-aaa53cee12cd56e6">SMITH 为什么让 Agent 不只使用现成工具，还学习创建可再用的工具？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asmith">SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Appier AI Research / National Taiwan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定工具集未必覆盖新任务需要的处理方式，反复临时写代码又会重复劳动。SMITH 把工具构建与后续使用作为相互关联的任务，使生成的接口和实现接受真实使用检验。能产出代码不代表工具有用，格式、执行结果和下游答案各自都可能失败。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：多次遇到相同数据清洗需求，可以创建专用处理工具；它是否值得保留，要看后来能否正确调用并完成实际清洗。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24571">原论文</a> · <a href="../../../../agent-research/2608.24571-smith/">实现解读</a> · <a href="#qa-aaa53cee12cd56e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:smith" data-paper-title="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification Agent Appier AI Research / National Taiwan University 2026-08-25 现有工具创建通常在推理时让冻结模型写代码，创建者与使用者没有联合信号。SMITH 在同一 policy 中混合 build task（从样例写 schema/backend）和 use task（在 held-out 问题调用池中工具），分别给 schema 合法性、代码执行和最终答案奖励，并用更难问题鼓励可复用抽象。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。同一 Agent 交替 build/use，并独立执行 schema、代码和 outcome 三类 verifier。本地工具为结构化 plan，并真实分开 build/use 状态和三轴 verifier；未运行 Qwen3-4B、可执行 Python sandbox、Reasoning-Gym、TabMWP 或 GQA。PlanBench-mini 120 episodes：生成 12 个工具、复用 108 次，执行 360 个分轴 verifier，joint success 1.0000、平均成本 0.4550。  多维验证工具自进化 Agent 工具与协作执行：把计划变成可检查的动作 为什么创建工具与使用工具要在同一策略中联合训练？ 只奖励生成可运行代码，可能得到难调用或不解决新题的工具；只训练使用者又无法改进工具设计。build 与 held-out use 混合任务把 schema、执行和最终结果信号连起来，鼓励可复用抽象；样例通过不是独立问题解决，使用评测仍需隔离。 例如工具能算训练样例却把常量写死，代码执行奖励可能通过，但 held-out 调用会失败，从而暴露它没有真正可复用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-26ea08414f79720d">为什么创建工具与使用工具要在同一策略中联合训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asmith">SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Appier AI Research / National Taiwan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只奖励生成可运行代码，可能得到难调用或不解决新题的工具；只训练使用者又无法改进工具设计。build 与 held-out use 混合任务把 schema、执行和最终结果信号连起来，鼓励可复用抽象；样例通过不是独立问题解决，使用评测仍需隔离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具能算训练样例却把常量写死，代码执行奖励可能通过，但 held-out 调用会失败，从而暴露它没有真正可复用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24571">原论文</a> · <a href="../../../../agent-research/2608.24571-smith/">实现解读</a> · <a href="#qa-26ea08414f79720d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:smith" data-paper-title="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification Agent Appier AI Research / National Taiwan University 2026-08-25 现有工具创建通常在推理时让冻结模型写代码，创建者与使用者没有联合信号。SMITH 在同一 policy 中混合 build task（从样例写 schema/backend）和 use task（在 held-out 问题调用池中工具），分别给 schema 合法性、代码执行和最终答案奖励，并用更难问题鼓励可复用抽象。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。同一 Agent 交替 build/use，并独立执行 schema、代码和 outcome 三类 verifier。本地工具为结构化 plan，并真实分开 build/use 状态和三轴 verifier；未运行 Qwen3-4B、可执行 Python sandbox、Reasoning-Gym、TabMWP 或 GQA。PlanBench-mini 120 episodes：生成 12 个工具、复用 108 次，执行 360 个分轴 verifier，joint success 1.0000、平均成本 0.4550。  多维验证工具自进化 Agent 工具与协作执行：把计划变成可检查的动作 schema、代码执行、最终答案三轴奖励为什么不能互相替代？ schema 合法只保证接口可解析，代码运行只保证执行不崩溃，最终结果才检验任务是否解决。三者各自有失败方式，单一成功标志会隐藏问题；更难问题用于促使工具形成抽象，不能靠扩大样例硬编码冒充泛化。 例如函数签名正确且能返回数字，但计算公式错了，前两轴可过、答案轴仍应失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b59b77f1e41a46c9">schema、代码执行、最终答案三轴奖励为什么不能互相替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asmith">SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Appier AI Research / National Taiwan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>schema 合法只保证接口可解析，代码运行只保证执行不崩溃，最终结果才检验任务是否解决。三者各自有失败方式，单一成功标志会隐藏问题；更难问题用于促使工具形成抽象，不能靠扩大样例硬编码冒充泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如函数签名正确且能返回数字，但计算公式错了，前两轴可过、答案轴仍应失败。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24571">原论文</a> · <a href="../../../../agent-research/2608.24571-smith/">实现解读</a> · <a href="#qa-b59b77f1e41a46c9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:smith" data-paper-title="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification Agent Appier AI Research / National Taiwan University 2026-08-25 现有工具创建通常在推理时让冻结模型写代码，创建者与使用者没有联合信号。SMITH 在同一 policy 中混合 build task（从样例写 schema/backend）和 use task（在 held-out 问题调用池中工具），分别给 schema 合法性、代码执行和最终答案奖励，并用更难问题鼓励可复用抽象。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。同一 Agent 交替 build/use，并独立执行 schema、代码和 outcome 三类 verifier。本地工具为结构化 plan，并真实分开 build/use 状态和三轴 verifier；未运行 Qwen3-4B、可执行 Python sandbox、Reasoning-Gym、TabMWP 或 GQA。PlanBench-mini 120 episodes：生成 12 个工具、复用 108 次，执行 360 个分轴 verifier，joint success 1.0000、平均成本 0.4550。  多维验证工具自进化 Agent 工具与协作执行：把计划变成可检查的动作 本地结构化 plan 工具是否等于可执行 Python sandbox？ 不等于。本地分开 build/use 状态并实际运行三轴 verifier，但工具内容是受控计划，没有 Qwen3-4B、Python 沙箱或 Reasoning-Gym 等环境。生成与复用次数只能验证流程，不应将原文代码工具训练效果归给该小型替代表示。 例如计划节点“加法”可由规则解释器执行，不代表系统能安全编译并运行任意模型生成 Python backend。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-83a7dab631c78030">本地结构化 plan 工具是否等于可执行 Python sandbox？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asmith">SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Appier AI Research / National Taiwan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等于。本地分开 build/use 状态并实际运行三轴 verifier，但工具内容是受控计划，没有 Qwen3-4B、Python 沙箱或 Reasoning-Gym 等环境。生成与复用次数只能验证流程，不应将原文代码工具训练效果归给该小型替代表示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如计划节点“加法”可由规则解释器执行，不代表系统能安全编译并运行任意模型生成 Python backend。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24571">原论文</a> · <a href="../../../../agent-research/2608.24571-smith/">实现解读</a> · <a href="#qa-83a7dab631c78030">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pmcoder" data-paper-title="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution Agent Vanderbilt University 2026-08-07 用层级 phase planner 条件化 episodic retrieval，再用记忆轨迹统计检测 stuck 并重规划，以真实执行 verdict 验证。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  代码 Agent 记忆与规划 Agent 工具与协作执行：把计划变成可检查的动作 软件 issue 要经过定位、修改和测试时，PMCoder 希望记住哪些可继续利用的经验？ 长修复任务会产生定位线索、失败尝试和测试结论，若每轮从原 issue 重新出发，容易重复查找或重犯错误。PMCoder 用过程阶段组织计划与经验读取，让当前步骤利用恰当的历史。记忆只是执行支持，仍需当前代码和测试确认，不能把记住旧解法等同于修复新问题。 教学例：定位阶段发现问题在解析器，测试阶段确认某边界输入失败；下一轮应利用这些结论，而不是再次全仓库搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-pmcoder-088b3672" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-69e13b18b74254a0">软件 issue 要经过定位、修改和测试时，PMCoder 希望记住哪些可继续利用的经验？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apmcoder">Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Vanderbilt University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长修复任务会产生定位线索、失败尝试和测试结论，若每轮从原 issue 重新出发，容易重复查找或重犯错误。PMCoder 用过程阶段组织计划与经验读取，让当前步骤利用恰当的历史。记忆只是执行支持，仍需当前代码和测试确认，不能把记住旧解法等同于修复新问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：定位阶段发现问题在解析器，测试阶段确认某边界输入失败；下一轮应利用这些结论，而不是再次全仓库搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06811">原论文</a> · <a href="../../../../agent-research/2608.06811-pmcoder/">实现解读</a> · <a href="#qa-69e13b18b74254a0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pmcoder" data-paper-title="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution Agent Vanderbilt University 2026-08-07 用层级 phase planner 条件化 episodic retrieval，再用记忆轨迹统计检测 stuck 并重规划，以真实执行 verdict 验证。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  代码 Agent 记忆与规划 Agent 工具与协作执行：把计划变成可检查的动作 为什么 episodic retrieval 要由当前 phase 条件化，而非每步都对原 issue 做相同检索？ 定位、修改和验证阶段需要不同证据，固定检索容易重复返回主题相似但不适合当前动作的轨迹。层级规划用 phase 约束经验选择，再根据历史行为检测卡住并重规划；最终仍由真实执行 verdict 判断，不应把“计划切换了”当成问题已经解决。 例如定位阶段需要找相关文件，验证阶段需要已知回归测试；只按 issue 文本反复检索，可能一直返回定位经验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d5a49a3fee65a642">为什么 episodic retrieval 要由当前 phase 条件化，而非每步都对原 issue 做相同检索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apmcoder">Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Vanderbilt University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>定位、修改和验证阶段需要不同证据，固定检索容易重复返回主题相似但不适合当前动作的轨迹。层级规划用 phase 约束经验选择，再根据历史行为检测卡住并重规划；最终仍由真实执行 verdict 判断，不应把“计划切换了”当成问题已经解决。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如定位阶段需要找相关文件，验证阶段需要已知回归测试；只按 issue 文本反复检索，可能一直返回定位经验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06811">原论文</a> · <a href="../../../../agent-research/2608.06811-pmcoder/">实现解读</a> · <a href="#qa-d5a49a3fee65a642">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pmcoder" data-paper-title="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution Agent Vanderbilt University 2026-08-07 用层级 phase planner 条件化 episodic retrieval，再用记忆轨迹统计检测 stuck 并重规划，以真实执行 verdict 验证。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  代码 Agent 记忆与规划 Agent 工具与协作执行：把计划变成可检查的动作 记忆轨迹统计的 stuck 检测与每次失败立刻重写全部计划有何取舍？ 统计可识别重复无进展模式，再有针对性重规划；一次失败可能提供新证据，不一定说明整个方向错误。全部重写容易重复已做工作，完全不改又可能持续卡住；实际 verdict 用于验证恢复，不是自评宣称“已修好”。 例如两次相同补丁都触发同一测试错误可提示换方案，首次出现新报错则可能只是正常推进，需要区别判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b8b4cfdcf0674ba0">记忆轨迹统计的 stuck 检测与每次失败立刻重写全部计划有何取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apmcoder">Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Vanderbilt University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>统计可识别重复无进展模式，再有针对性重规划；一次失败可能提供新证据，不一定说明整个方向错误。全部重写容易重复已做工作，完全不改又可能持续卡住；实际 verdict 用于验证恢复，不是自评宣称“已修好”。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两次相同补丁都触发同一测试错误可提示换方案，首次出现新报错则可能只是正常推进，需要区别判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06811">原论文</a> · <a href="../../../../agent-research/2608.06811-pmcoder/">实现解读</a> · <a href="#qa-b8b4cfdcf0674ba0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pmcoder" data-paper-title="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution Agent Vanderbilt University 2026-08-07 用层级 phase planner 条件化 episodic retrieval，再用记忆轨迹统计检测 stuck 并重规划，以真实执行 verdict 验证。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  代码 Agent 记忆与规划 Agent 工具与协作执行：把计划变成可检查的动作 本地 phase/retrieval 满分能否与 SWE-bench 多解决二十五题横比？ 不能。本地确定性 PlanBench 只验证分阶段检索、停滞和重规划路径，不访问真实仓库容器或论文模型。成本字段与原工具 token 无直接等价关系，应报告 trace 和分支证据，而不把饱和成功率当 issue resolution 能力。 例如规则按阶段选对模板并通过三步计划，不说明系统可在未知代码库定位、修改并运行真实失败测试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6d42348ca21f71f7">本地 phase/retrieval 满分能否与 SWE-bench 多解决二十五题横比？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apmcoder">Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Vanderbilt University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地确定性 PlanBench 只验证分阶段检索、停滞和重规划路径，不访问真实仓库容器或论文模型。成本字段与原工具 token 无直接等价关系，应报告 trace 和分支证据，而不把饱和成功率当 issue resolution 能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如规则按阶段选对模板并通过三步计划，不说明系统可在未知代码库定位、修改并运行真实失败测试。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06811">原论文</a> · <a href="../../../../agent-research/2608.06811-pmcoder/">实现解读</a> · <a href="#qa-6d42348ca21f71f7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:codegrep" data-paper-title="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents Agent NetEase Guangzhou AI Lab 2026-08-06 主题：代码检索 Agent。以 GRPO 训练 14B 检索 Agent 并行发出 grep/glob/read，多轮缩小候选文件，再交给冻结 coding agent；优化的是下游修复收益而非孤立检索分数。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的代码检索 Agent 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  代码检索 Agent Agent 工具与协作执行：把计划变成可检查的动作 CodeGrep 为什么把大仓库中的证据获取看作需要学习的多步工作？ 修复 issue 前往往不知道相关文件、符号和调用关系，单次检索可能只找到文字相近片段。CodeGrep 让 Agent 逐步搜索、读代码并根据新线索继续查找，使证据获取服务后续修复。找到文件并非终点，读到的信息是否真的帮助解决问题仍需下游执行检验。 教学例：报错提到配置，第一次 grep 找到入口，读代码后发现真正默认值在另一个模块，需要继续追踪而非就地猜补丁。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-codegrep-29277303" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-237d4d1814ad8cbe">CodeGrep 为什么把大仓库中的证据获取看作需要学习的多步工作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acodegrep">CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Guangzhou AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>修复 issue 前往往不知道相关文件、符号和调用关系，单次检索可能只找到文字相近片段。CodeGrep 让 Agent 逐步搜索、读代码并根据新线索继续查找，使证据获取服务后续修复。找到文件并非终点，读到的信息是否真的帮助解决问题仍需下游执行检验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：报错提到配置，第一次 grep 找到入口，读代码后发现真正默认值在另一个模块，需要继续追踪而非就地猜补丁。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05886">原论文</a> · <a href="../../../../agent-research/2608.05886-codegrep/">实现解读</a> · <a href="#qa-237d4d1814ad8cbe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:codegrep" data-paper-title="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents Agent NetEase Guangzhou AI Lab 2026-08-06 主题：代码检索 Agent。以 GRPO 训练 14B 检索 Agent 并行发出 grep/glob/read，多轮缩小候选文件，再交给冻结 coding agent；优化的是下游修复收益而非孤立检索分数。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的代码检索 Agent 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  代码检索 Agent Agent 工具与协作执行：把计划变成可检查的动作 为什么代码检索 Agent 的奖励来自下游修复收益，而不只看找对文件？ 正确文件可能仍缺少调用链和约束，检索也可能耗费过多 token 与轮次。把结果交给冻结 coding agent，观察实际修复并计入成本，能评价证据是否可用；冻结执行器减少两侧同时变化的混淆，但单次下游失败也不自动证明某条证据无价值。 例如找到报错函数却没读其调用约束，修复器仍会改错；检索相关文件和测试上下文才可能真正提高可修复性。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-be1af93d2bb20565">为什么代码检索 Agent 的奖励来自下游修复收益，而不只看找对文件？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acodegrep">CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Guangzhou AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>正确文件可能仍缺少调用链和约束，检索也可能耗费过多 token 与轮次。把结果交给冻结 coding agent，观察实际修复并计入成本，能评价证据是否可用；冻结执行器减少两侧同时变化的混淆，但单次下游失败也不自动证明某条证据无价值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如找到报错函数却没读其调用约束，修复器仍会改错；检索相关文件和测试上下文才可能真正提高可修复性。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05886">原论文</a> · <a href="../../../../agent-research/2608.05886-codegrep/">实现解读</a> · <a href="#qa-be1af93d2bb20565">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:codegrep" data-paper-title="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents Agent NetEase Guangzhou AI Lab 2026-08-06 主题：代码检索 Agent。以 GRPO 训练 14B 检索 Agent 并行发出 grep/glob/read，多轮缩小候选文件，再交给冻结 coding agent；优化的是下游修复收益而非孤立检索分数。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的代码检索 Agent 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  代码检索 Agent Agent 工具与协作执行：把计划变成可检查的动作 多轮 grep/glob/read 与一次向量 Top-K 有何信息获取差别？ grep 和 glob 可根据代码符号与路径逐步缩小范围，read 后再更新查询，属于交互式程序证据获取；一次向量检索在初次相似度上固定候选。多轮适应也消耗调用与上下文，不能只比较最终文件命中而忽略探索成本。 例如先 glob 找测试目录，再 grep 报错符号，读调用者后继续搜索依赖，后一步条件来自前一步实际代码。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ed35b36b766cbf45">多轮 grep/glob/read 与一次向量 Top-K 有何信息获取差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acodegrep">CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Guangzhou AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>grep 和 glob 可根据代码符号与路径逐步缩小范围，read 后再更新查询，属于交互式程序证据获取；一次向量检索在初次相似度上固定候选。多轮适应也消耗调用与上下文，不能只比较最终文件命中而忽略探索成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先 glob 找测试目录，再 grep 报错符号，读调用者后继续搜索依赖，后一步条件来自前一步实际代码。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05886">原论文</a> · <a href="../../../../agent-research/2608.05886-codegrep/">实现解读</a> · <a href="#qa-ed35b36b766cbf45">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:codegrep" data-paper-title="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents Agent NetEase Guangzhou AI Lab 2026-08-06 主题：代码检索 Agent。以 GRPO 训练 14B 检索 Agent 并行发出 grep/glob/read，多轮缩小候选文件，再交给冻结 coding agent；优化的是下游修复收益而非孤立检索分数。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的代码检索 Agent 算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  代码检索 Agent Agent 工具与协作执行：把计划变成可检查的动作 本地检索算子与真实 14B GRPO 训练之间必须区分哪些证据？ 本地仅在公共 mini-suite 验证受限选择和状态机制，未训练 14B 检索 Agent、运行真实 SWE-bench 或完整下游修复器。token 与轮数惩罚需要实际计量，候选注册或模拟搜索不能当作 RL 已执行及端到端加速。 例如一个 fixture 少选两次 read 只说明代理调用减少，没有模型生成和真实文件内容就不能报告修复成功提高一点二百分点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-28aaa8a73f03f573">本地检索算子与真实 14B GRPO 训练之间必须区分哪些证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acodegrep">CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · NetEase Guangzhou AI Lab</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地仅在公共 mini-suite 验证受限选择和状态机制，未训练 14B 检索 Agent、运行真实 SWE-bench 或完整下游修复器。token 与轮数惩罚需要实际计量，候选注册或模拟搜索不能当作 RL 已执行及端到端加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个 fixture 少选两次 read 只说明代理调用减少，没有模型生成和真实文件内容就不能报告修复成功提高一点二百分点。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05886">原论文</a> · <a href="../../../../agent-research/2608.05886-codegrep/">实现解读</a> · <a href="#qa-28aaa8a73f03f573">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:manta" data-paper-title="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems Agent Cornell University 2026-07-30 根据任务先验初始化通信拓扑，运行中监控协作 trace，并有界调整角色、边、顺序、可见性和验证路径。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  多 Agent 自进化 Agent 工具与协作执行：把计划变成可检查的动作 多 Agent 团队为什么可能因沟通安排不当而浪费协作机会？ 角色再多，若消息传给不需要的人、关键结果未到达依赖者或交流顺序错误，工作仍会停滞。MANTA 研究让通信结构随执行反馈适应任务，而不把团队配置视为固定名单。改变拓扑也会增加协调成本，效果需看信息可见性、任务结果和资源开销。 教学例：验证者发现约束错误，却只回复无关角色，执行者继续沿旧计划行动；需要调整的是信息流，而不一定是再加一个 Agent。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-manta-a024f561" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6c9e155972b09a66">多 Agent 团队为什么可能因沟通安排不当而浪费协作机会？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amanta">MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>角色再多，若消息传给不需要的人、关键结果未到达依赖者或交流顺序错误，工作仍会停滞。MANTA 研究让通信结构随执行反馈适应任务，而不把团队配置视为固定名单。改变拓扑也会增加协调成本，效果需看信息可见性、任务结果和资源开销。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：验证者发现约束错误，却只回复无关角色，执行者继续沿旧计划行动；需要调整的是信息流，而不一定是再加一个 Agent。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28527">原论文</a> · <a href="../../../../agent-research/2607.28527-manta/">实现解读</a> · <a href="#qa-6c9e155972b09a66">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:manta" data-paper-title="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems Agent Cornell University 2026-07-30 根据任务先验初始化通信拓扑，运行中监控协作 trace，并有界调整角色、边、顺序、可见性和验证路径。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  多 Agent 自进化 Agent 工具与协作执行：把计划变成可检查的动作 为什么通信拓扑调整要同时约束边、顺序与可见性，而非只增加更多 Agent？ 协作失败可能来自信息没传到、角色重复或验证路径缺失，人数增加不一定解决。运行轨迹驱动有界拓扑修改，把角色关系与信息流作为优化对象；预算投影限制额外通信和执行成本，改图的收益也须由实际任务反馈确认，不能仅以边数增加判断改进。 例如审查者一直看不到最新代码，应改消息可见性而非再加三名审查者；否则只是重复评估同一份旧材料。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-12a63e7249c622c4">为什么通信拓扑调整要同时约束边、顺序与可见性，而非只增加更多 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amanta">MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>协作失败可能来自信息没传到、角色重复或验证路径缺失，人数增加不一定解决。运行轨迹驱动有界拓扑修改，把角色关系与信息流作为优化对象；预算投影限制额外通信和执行成本，改图的收益也须由实际任务反馈确认，不能仅以边数增加判断改进。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如审查者一直看不到最新代码，应改消息可见性而非再加三名审查者；否则只是重复评估同一份旧材料。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28527">原论文</a> · <a href="../../../../agent-research/2607.28527-manta/">实现解读</a> · <a href="#qa-12a63e7249c622c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:manta" data-paper-title="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems Agent Cornell University 2026-07-30 根据任务先验初始化通信拓扑，运行中监控协作 trace，并有界调整角色、边、顺序、可见性和验证路径。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  多 Agent 自进化 Agent 工具与协作执行：把计划变成可检查的动作 在线拓扑适应与开始前一次性选团队有什么取舍？ 初始团队只依据任务先验，在线适应可响应实际瓶颈、失败或冗余通信，但也可能引入不稳定和额外开销。调整应投影到预算和权限范围，不能为了提高分数无限增 Agent 或开放所有私有历史。 例如发现两个角色重复查同一来源，可合并或改边；若因此让评测参考流入执行角色，就超出了合法适应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0ca487177d340d40">在线拓扑适应与开始前一次性选团队有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amanta">MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>初始团队只依据任务先验，在线适应可响应实际瓶颈、失败或冗余通信，但也可能引入不稳定和额外开销。调整应投影到预算和权限范围，不能为了提高分数无限增 Agent 或开放所有私有历史。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如发现两个角色重复查同一来源，可合并或改边；若因此让评测参考流入执行角色，就超出了合法适应。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28527">原论文</a> · <a href="../../../../agent-research/2607.28527-manta/">实现解读</a> · <a href="#qa-0ca487177d340d40">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:manta" data-paper-title="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems Agent Cornell University 2026-07-30 根据任务先验初始化通信拓扑，运行中监控协作 trace，并有界调整角色、边、顺序、可见性和验证路径。 复现级别：核心 Agent 机制 mini-suite。复现级别：核心 Agent 机制 mini-suite。本地实现独立规划、记忆、credit assignment 或拓扑路径，并在确定性任务上记录过程计数；不是原论文完整外部环境。确定性 mini-suite 不访问真实浏览器、AppWorld、SWE-bench 或外部工具服务；它验证机制分支、过程状态和报告契约可执行。完整环境结果需按原文资源另行复现。运行目录是 runs/agent-research/，仓库只保存指标。另见 ../../experiments/。  多 Agent 自进化 Agent 工具与协作执行：把计划变成可检查的动作 Π_budget 在拓扑更新中的作用与本地 evidence 边界是什么？ 投影将提议的角色、边和顺序调整限制在允许资源内，不是先执行超预算结构再只统计部分成本。本地确定性 suite 验证这些状态和调度分支，没有真实多 Agent 模型与环境，拓扑变化计数不代表论文五 benchmark 泛化。 例如候选提出十个角色而预算只容四个，必须先得到可执行受限图；不能十个都跑完再把六个从成本表删掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-6fda2c22ac9a171c">Π_budget 在拓扑更新中的作用与本地 evidence 边界是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amanta">MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cornell University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>投影将提议的角色、边和顺序调整限制在允许资源内，不是先执行超预算结构再只统计部分成本。本地确定性 suite 验证这些状态和调度分支，没有真实多 Agent 模型与环境，拓扑变化计数不代表论文五 benchmark 泛化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如候选提出十个角色而预算只容四个，必须先得到可执行受限图；不能十个都跑完再把六个从成本表删掉。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28527">原论文</a> · <a href="../../../../agent-research/2607.28527-manta/">实现解读</a> · <a href="#qa-6fda2c22ac9a171c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cam-df" data-paper-title="CAM-DF" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAM-DF Agent Peking University 2026-07-29 工具 router 只能给出相关性排序，不能回答“应该开放前几个工具”。CAM-DF 在任何工具执行前虚拟遍历排序前缀，以任务充分性减异构工具成本作为 payoff；停止当前前缀与最佳后续前缀的 payoff gap 决定标签，gap 绝对值决定错误的 regret 权重。 本地是确定性工具 mini-suite，不是 τ-bench Retail live execution；充分性来自 benchmark 可审计 required-tools，而不是另训的 scorer。ScaleMCP mini 为每个任务构造冻结排序和异构成本，枚举所有前缀的下游 payoff，执行 regret-weighted 停止并只挂载所选工具。  成本感知工具停止 Agent 工具与协作执行：把计划变成可检查的动作 工具排序之后为什么还需要决定开放前几个？ 相关性顺序没有回答候选集合何时已足够，开放过多工具增加成本和干扰，过少会缺必要接口。CAM-DF 在工具执行前虚拟比较前缀充分性与异构成本，选择停止点；这是暴露范围控制，不是实际工具调用后的动态 stop。 例如排名前两项只含查询工具、第三项才有修改接口，任务需要修改时不能仅因前两项相关分高就停止开放。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-cam-df-2b7f3d23" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-20b5ca35f6a5f4ae">工具排序之后为什么还需要决定开放前几个？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acam-df">CAM-DF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相关性顺序没有回答候选集合何时已足够，开放过多工具增加成本和干扰，过少会缺必要接口。CAM-DF 在工具执行前虚拟比较前缀充分性与异构成本，选择停止点；这是暴露范围控制，不是实际工具调用后的动态 stop。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如排名前两项只含查询工具、第三项才有修改接口，任务需要修改时不能仅因前两项相关分高就停止开放。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27083">原论文</a> · <a href="../../../../agent-research/2607.27083-cam-df/">实现解读</a> · <a href="#qa-20b5ca35f6a5f4ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cam-df" data-paper-title="CAM-DF" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAM-DF Agent Peking University 2026-07-29 工具 router 只能给出相关性排序，不能回答“应该开放前几个工具”。CAM-DF 在任何工具执行前虚拟遍历排序前缀，以任务充分性减异构工具成本作为 payoff；停止当前前缀与最佳后续前缀的 payoff gap 决定标签，gap 绝对值决定错误的 regret 权重。 本地是确定性工具 mini-suite，不是 τ-bench Retail live execution；充分性来自 benchmark 可审计 required-tools，而不是另训的 scorer。ScaleMCP mini 为每个任务构造冻结排序和异构成本，枚举所有前缀的下游 payoff，执行 regret-weighted 停止并只挂载所选工具。  成本感知工具停止 Agent 工具与协作执行：把计划变成可检查的动作 停止标签为什么由当前前缀与最佳后续前缀的 payoff gap 决定？ 相关性排名不回答开放多少工具才足够，停止过早可能缺能力，继续过久又付出额外成本。虚拟前缀的充分性减成本形成 payoff，差值决定停或续，绝对差衡量选错的遗憾；这些评估发生在执行前，不能把虚拟收益写成真实工具成功率。 例如前两把工具已能完成任务，第三把虽相关却很贵，继续前缀收益更低；停止标签应考虑这部分成本而非只看排名。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0570cdc0a7c4faa1">停止标签为什么由当前前缀与最佳后续前缀的 payoff gap 决定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acam-df">CAM-DF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相关性排名不回答开放多少工具才足够，停止过早可能缺能力，继续过久又付出额外成本。虚拟前缀的充分性减成本形成 payoff，差值决定停或续，绝对差衡量选错的遗憾；这些评估发生在执行前，不能把虚拟收益写成真实工具成功率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如前两把工具已能完成任务，第三把虽相关却很贵，继续前缀收益更低；停止标签应考虑这部分成本而非只看排名。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27083">原论文</a> · <a href="../../../../agent-research/2607.27083-cam-df/">实现解读</a> · <a href="#qa-0570cdc0a7c4faa1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cam-df" data-paper-title="CAM-DF" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAM-DF Agent Peking University 2026-07-29 工具 router 只能给出相关性排序，不能回答“应该开放前几个工具”。CAM-DF 在任何工具执行前虚拟遍历排序前缀，以任务充分性减异构工具成本作为 payoff；停止当前前缀与最佳后续前缀的 payoff gap 决定标签，gap 绝对值决定错误的 regret 权重。 本地是确定性工具 mini-suite，不是 τ-bench Retail live execution；充分性来自 benchmark 可审计 required-tools，而不是另训的 scorer。ScaleMCP mini 为每个任务构造冻结排序和异构成本，枚举所有前缀的下游 payoff，执行 regret-weighted 停止并只挂载所选工具。  成本感知工具停止 Agent 工具与协作执行：把计划变成可检查的动作 regret 权重与普通 stop/continue 二分类标签有什么不同？ 两种错误代价可能差很大，gap 符号给停止标签，绝对值衡量错选损失。只做等权分类把几乎打平与漏掉关键工具同等看待；最佳后续前缀提供比较基准，也依赖充分性估计正确，不能视作部署时隐藏真值。 例如多开放一个廉价工具只有微小损失，过早停下漏掉退款接口损失很大，regret 权重应让后者更受重视。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-580c3367b255c392">regret 权重与普通 stop/continue 二分类标签有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acam-df">CAM-DF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两种错误代价可能差很大，gap 符号给停止标签，绝对值衡量错选损失。只做等权分类把几乎打平与漏掉关键工具同等看待；最佳后续前缀提供比较基准，也依赖充分性估计正确，不能视作部署时隐藏真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如多开放一个廉价工具只有微小损失，过早停下漏掉退款接口损失很大，regret 权重应让后者更受重视。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27083">原论文</a> · <a href="../../../../agent-research/2607.27083-cam-df/">实现解读</a> · <a href="#qa-580c3367b255c392">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:cam-df" data-paper-title="CAM-DF" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAM-DF Agent Peking University 2026-07-29 工具 router 只能给出相关性排序，不能回答“应该开放前几个工具”。CAM-DF 在任何工具执行前虚拟遍历排序前缀，以任务充分性减异构工具成本作为 payoff；停止当前前缀与最佳后续前缀的 payoff gap 决定标签，gap 绝对值决定错误的 regret 权重。 本地是确定性工具 mini-suite，不是 τ-bench Retail live execution；充分性来自 benchmark 可审计 required-tools，而不是另训的 scorer。ScaleMCP mini 为每个任务构造冻结排序和异构成本，枚举所有前缀的下游 payoff，执行 regret-weighted 停止并只挂载所选工具。  成本感知工具停止 Agent 工具与协作执行：把计划变成可检查的动作 本地 required-tools 充分性可以作为一般部署 scorer 吗？ 不能。当前充分性来自可审计 mini-suite 的 required-tools，用于诊断前缀选择，不是另训的语义 scorer。隐藏必需工具不能传给实际策略宣称自主选择，工具暴露下降也不是 τ-bench live execution 的真实 token 或成功率收益。 例如评分器知道第三项必需可用于离线算 payoff，但部署 router 若直接读取该列表，就绕过了论文要学习的充分性判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c90b30ce9f21e6a3">本地 required-tools 充分性可以作为一般部署 scorer 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acam-df">CAM-DF</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。当前充分性来自可审计 mini-suite 的 required-tools，用于诊断前缀选择，不是另训的语义 scorer。隐藏必需工具不能传给实际策略宣称自主选择，工具暴露下降也不是 τ-bench live execution 的真实 token 或成功率收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如评分器知道第三项必需可用于离线算 payoff，但部署 router 若直接读取该列表，就绕过了论文要学习的充分性判断。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27083">原论文</a> · <a href="../../../../agent-research/2607.27083-cam-df/">实现解读</a> · <a href="#qa-c90b30ce9f21e6a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autoformbot" data-paper-title="Formalizing Mathematics at Scale" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Formalizing Mathematics at Scale Agent FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris 2026-05-28 先构建教材声明的依赖DAG，工作者在独立worktree写Lean，经并发审查和合并队列进入主库；失败轨迹生成技能，监督者在合并后核查目标并反馈重规划。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；开源框架不等于本地已运行。每书约一周；39目标的小书消融仍使用600M至1200M tokens，持续数小时。成本过高，不复现（审查 DONE），不调用付费模型、不启动Lean多Agent任务。保留源码和协议，无本地分数、GPU回执或evolve可执行映射，不重新排入自动队列。  多Agent协作 形式化验证与依赖调度 Agent 工具与协作执行：把计划变成可检查的动作 把整本教材的数学声明形式化，为什么不等于逐条独立翻译成 Lean？ 后续定理依赖先前定义和引理，翻译时还要维护共享仓库、编译状态和原意一致性。AutoFormBot 研究多个工作者如何在这种依赖网络中持续推进，并让局部产物能合并成全局目标。编译通过只说明形式系统接受，仍需检查是否忠实表达教材命题。 教学例：一个工作者改了基础定义，其他人的证明可能全部失效；即使各自分支曾编译通过，也必须合并后重新核对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-autoformbot-6fe44000" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-edd356cace2c3e7c">把整本教材的数学声明形式化，为什么不等于逐条独立翻译成 Lean？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautoformbot">Formalizing Mathematics at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后续定理依赖先前定义和引理，翻译时还要维护共享仓库、编译状态和原意一致性。AutoFormBot 研究多个工作者如何在这种依赖网络中持续推进，并让局部产物能合并成全局目标。编译通过只说明形式系统接受，仍需检查是否忠实表达教材命题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一个工作者改了基础定义，其他人的证明可能全部失效；即使各自分支曾编译通过，也必须合并后重新核对。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29955">原论文</a> · <a href="../../../../agent-research/2605.29955-autoformbot/">实现解读</a> · <a href="#qa-edd356cace2c3e7c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autoformbot" data-paper-title="Formalizing Mathematics at Scale" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Formalizing Mathematics at Scale Agent FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris 2026-05-28 先构建教材声明的依赖DAG，工作者在独立worktree写Lean，经并发审查和合并队列进入主库；失败轨迹生成技能，监督者在合并后核查目标并反馈重规划。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；开源框架不等于本地已运行。每书约一周；39目标的小书消融仍使用600M至1200M tokens，持续数小时。成本过高，不复现（审查 DONE），不调用付费模型、不启动Lean多Agent任务。保留源码和协议，无本地分数、GPU回执或evolve可执行映射，不重新排入自动队列。  多Agent协作 形式化验证与依赖调度 Agent 工具与协作执行：把计划变成可检查的动作 为什么数学形式化工作者要独立 worktree，并经合并队列后再核对全局目标？ 独立工作区减少并发文件冲突，依赖 DAG 指定可先形式化哪些声明，合并审查维护共享库一致性。局部 Lean 通过不保证所有教材目标都已覆盖，监督者还要对照全局进度重规划；失败经验可沉淀技能，但不能因分支存在就认定证明已合入。 例如两个工作者各证明一个引理，分别通过后仍需检查名称冲突及主定理依赖；不能把两个孤立文件当成完整教材已形式化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f57c0f41ebcd567f">为什么数学形式化工作者要独立 worktree，并经合并队列后再核对全局目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautoformbot">Formalizing Mathematics at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>独立工作区减少并发文件冲突，依赖 DAG 指定可先形式化哪些声明，合并审查维护共享库一致性。局部 Lean 通过不保证所有教材目标都已覆盖，监督者还要对照全局进度重规划；失败经验可沉淀技能，但不能因分支存在就认定证明已合入。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个工作者各证明一个引理，分别通过后仍需检查名称冲突及主定理依赖；不能把两个孤立文件当成完整教材已形式化。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29955">原论文</a> · <a href="../../../../agent-research/2605.29955-autoformbot/">实现解读</a> · <a href="#qa-f57c0f41ebcd567f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autoformbot" data-paper-title="Formalizing Mathematics at Scale" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Formalizing Mathematics at Scale Agent FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris 2026-05-28 先构建教材声明的依赖DAG，工作者在独立worktree写Lean，经并发审查和合并队列进入主库；失败轨迹生成技能，监督者在合并后核查目标并反馈重规划。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；开源框架不等于本地已运行。每书约一周；39目标的小书消融仍使用600M至1200M tokens，持续数小时。成本过高，不复现（审查 DONE），不调用付费模型、不启动Lean多Agent任务。保留源码和协议，无本地分数、GPU回执或evolve可执行映射，不重新排入自动队列。  多Agent协作 形式化验证与依赖调度 Agent 工具与协作执行：把计划变成可检查的动作 机械编译与独立忠实性审查为什么不能只留前者？ Lean 核检查的是形式命题证明，非法新 axiom、sorry、削弱命题或隐藏依赖可绕过原任务。编译必要但不充分，还需核对自然语言声明、依赖和独立评审；不能用调度任务全部完成替代数学忠实性。 例如把“所有自然数”改成“零”后很容易证明，代码可编译却不再形式化原定理，审查必须发现这种削弱。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0e097cb6f2ea1e55">机械编译与独立忠实性审查为什么不能只留前者？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautoformbot">Formalizing Mathematics at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Lean 核检查的是形式命题证明，非法新 axiom、sorry、削弱命题或隐藏依赖可绕过原任务。编译必要但不充分，还需核对自然语言声明、依赖和独立评审；不能用调度任务全部完成替代数学忠实性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把“所有自然数”改成“零”后很容易证明，代码可编译却不再形式化原定理，审查必须发现这种削弱。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29955">原论文</a> · <a href="../../../../agent-research/2605.29955-autoformbot/">实现解读</a> · <a href="#qa-0e097cb6f2ea1e55">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autoformbot" data-paper-title="Formalizing Mathematics at Scale" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Formalizing Mathematics at Scale Agent FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris 2026-05-28 先构建教材声明的依赖DAG，工作者在独立worktree写Lean，经并发审查和合并队列进入主库；失败轨迹生成技能，监督者在合并后核查目标并反馈重规划。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；开源框架不等于本地已运行。每书约一周；39目标的小书消融仍使用600M至1200M tokens，持续数小时。成本过高，不复现（审查 DONE），不调用付费模型、不启动Lean多Agent任务。保留源码和协议，无本地分数、GPU回执或evolve可执行映射，不重新排入自动队列。  多Agent协作 形式化验证与依赖调度 Agent 工具与协作执行：把计划变成可检查的动作 本地是否运行了教材级 Lean 多 Agent 或只保留协议？ 本地仅收录原文方法、依赖和成本，未启动 Lean 任务、付费调用、训练或 GPU 验证。原文每书多天及巨量 token 不能用简单 DAG 状态机替代后宣传完整复现，四万多声明也是作者结果且各书并非全部完成。 例如一个任务队列显示四十目标已调度，不意味着四十个 Lean 证明已经编译和忠实性审查通过。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3bee4ada3ee0e2fa">本地是否运行了教材级 Lean 多 Agent 或只保留协议？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautoformbot">Formalizing Mathematics at Scale</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地仅收录原文方法、依赖和成本，未启动 Lean 任务、付费调用、训练或 GPU 验证。原文每书多天及巨量 token 不能用简单 DAG 状态机替代后宣传完整复现，四万多声明也是作者结果且各书并非全部完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个任务队列显示四十目标已调度，不意味着四十个 Lean 证明已经编译和忠实性审查通过。</p>
<p class="ar-learning-sources">依据：本地复现与成本决策；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.29955">原论文</a> · <a href="../../../../agent-research/2605.29955-autoformbot/">实现解读</a> · <a href="#qa-3bee4ada3ee0e2fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:prompts" data-paper-title="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving Agent University of Maryland / Google 2026-05-18 Coordinator、Analyzer 和 Proposal Agent 联合读取 profiler 与知识库，诊断瓶颈并输出可解释的 sharding 候选。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  训练服务优化 多 Agent 性能诊断 Agent 工具与协作执行：把计划变成可检查的动作 PROMPTS 为什么把大模型的并行切分配置当成需要反复观测的优化任务？ 模型训练的瓶颈可能来自计算、内存或通信，并随硬件和配置改变。PROMPTS 让 Agent 利用实际 profiler 证据提出并行切分方案，再观察效果，而非只套用常见配置。配置建议不等于已经加速，必须在目标训练系统测量时间、资源和可行性。 教学例：增加切分本想减内存，却让跨设备通信变慢；只有真实 profile 才能辨别当前受内存还是通信限制。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-prompts-61564db7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-6c5e1155db8327b8">PROMPTS 为什么把大模型的并行切分配置当成需要反复观测的优化任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprompts">PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型训练的瓶颈可能来自计算、内存或通信，并随硬件和配置改变。PROMPTS 让 Agent 利用实际 profiler 证据提出并行切分方案，再观察效果，而非只套用常见配置。配置建议不等于已经加速，必须在目标训练系统测量时间、资源和可行性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：增加切分本想减内存，却让跨设备通信变慢；只有真实 profile 才能辨别当前受内存还是通信限制。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/prompts-performance-optimization-via-multi-agent-planning-for-llm-training-and-serving/">原论文</a> · <a href="../../../../agent-research/mlsys2026-prompts/">实现解读</a> · <a href="#qa-6c5e1155db8327b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:prompts" data-paper-title="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving Agent University of Maryland / Google 2026-05-18 Coordinator、Analyzer 和 Proposal Agent 联合读取 profiler 与知识库，诊断瓶颈并输出可解释的 sharding 候选。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  训练服务优化 多 Agent 性能诊断 Agent 工具与协作执行：把计划变成可检查的动作 为什么 sharding 提案必须结合 profiler，而不能只检索一套常见最佳配置？ 最优并行方式取决于计算、通信和内存的实际瓶颈，知识库只提供候选经验。Analyzer 读测量定位约束，Proposal Agent 再提出可解释分片方案，Coordinator 组织验证；生成配置或公式自检不等于运行了训练系统，也不能把预计加速冒充实测。 例如模型卡说某配置快，但当前设备是通信受限；profiler 若显示 all-reduce 占主导，就需要针对通信重新比较方案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a638de4eb75357c6">为什么 sharding 提案必须结合 profiler，而不能只检索一套常见最佳配置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprompts">PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最优并行方式取决于计算、通信和内存的实际瓶颈，知识库只提供候选经验。Analyzer 读测量定位约束，Proposal Agent 再提出可解释分片方案，Coordinator 组织验证；生成配置或公式自检不等于运行了训练系统，也不能把预计加速冒充实测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型卡说某配置快，但当前设备是通信受限；profiler 若显示 all-reduce 占主导，就需要针对通信重新比较方案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/prompts-performance-optimization-via-multi-agent-planning-for-llm-training-and-serving/">原论文</a> · <a href="../../../../agent-research/mlsys2026-prompts/">实现解读</a> · <a href="#qa-a638de4eb75357c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:prompts" data-paper-title="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving Agent University of Maryland / Google 2026-05-18 Coordinator、Analyzer 和 Proposal Agent 联合读取 profiler 与知识库，诊断瓶颈并输出可解释的 sharding 候选。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  训练服务优化 多 Agent 性能诊断 Agent 工具与协作执行：把计划变成可检查的动作 Coordinator、Analyzer、Proposal 分工与直接搜索配置表有什么区别？ 分工把任务协调、瓶颈解释和具体候选提议拆开，可根据证据缩小搜索并说明原因；配置表搜索主要枚举预设空间。多 Agent 本身也有成本，真正收益需看候选在真实训练或 serving 上的结果，不是解释长度或模型投票数。 例如 Analyzer 指出通信占主导，Proposal 才据此调整 sharding，而不是给每个维度随机试一遍再编理由。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5bb83b305c81a947">Coordinator、Analyzer、Proposal 分工与直接搜索配置表有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprompts">PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分工把任务协调、瓶颈解释和具体候选提议拆开，可根据证据缩小搜索并说明原因；配置表搜索主要枚举预设空间。多 Agent 本身也有成本，真正收益需看候选在真实训练或 serving 上的结果，不是解释长度或模型投票数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 Analyzer 指出通信占主导，Proposal 才据此调整 sharding，而不是给每个维度随机试一遍再编理由。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/prompts-performance-optimization-via-multi-agent-planning-for-llm-training-and-serving/">原论文</a> · <a href="../../../../agent-research/mlsys2026-prompts/">实现解读</a> · <a href="#qa-5bb83b305c81a947">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:prompts" data-paper-title="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving Agent University of Maryland / Google 2026-05-18 Coordinator、Analyzer 和 Proposal Agent 联合读取 profiler 与知识库，诊断瓶颈并输出可解释的 sharding 候选。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。本地执行 profiler 证据排序和受限配置提案；未接入 Google TPU profiler/GSPMD。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  训练服务优化 多 Agent 性能诊断 Agent 工具与协作执行：把计划变成可检查的动作 本地 profiler 排序与受限配置提案包含 TPU/GSPMD 实测吗？ 没有。本地只验证证据排序和提案边界 reference，未接入 Google TPU profiler 或 GSPMD，也没有真实生产工作负载性能矩阵。原文 top-3 命中与最高性能提升属于作者测量，不能把本地候选顺序直接写成同样吞吐收益。 例如预设 profile 指标可让选择器建议减少通信，但若未编译运行配置，就没有实际训练速度可报告。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a73f467c2768d482">本地 profiler 排序与受限配置提案包含 TPU/GSPMD 实测吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprompts">PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland / Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地只验证证据排序和提案边界 reference，未接入 Google TPU profiler 或 GSPMD，也没有真实生产工作负载性能矩阵。原文 top-3 命中与最高性能提升属于作者测量，不能把本地候选顺序直接写成同样吞吐收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预设 profile 指标可让选择器建议减少通信，但若未编译运行配置，就没有实际训练速度可报告。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://research.google/pubs/prompts-performance-optimization-via-multi-agent-planning-for-llm-training-and-serving/">原论文</a> · <a href="../../../../agent-research/mlsys2026-prompts/">实现解读</a> · <a href="#qa-a73f467c2768d482">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:paperorchestra" data-paper-title="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing Agent Google Cloud AI Research 2026-04-06 PaperOrchestra 用 Outline、Plotting、Literature Review、Section Writing、Content Refinement 五个 Agent，把零散想法和实验日志转成含文献与图表的 LaTeX 稿件。大纲之后图示与文献检索并行，引用经过实体和时间截止核验，最终根据多维评价接受或回退修订；系统不负责替作者发明或执行新实验。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。无可执行 adapter、生成能力指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。原文附录 B 在 10 篇计时子集报告每文约 60–70 次 LLM 调用、39.6 分钟裁尾均值；完整 200 篇、多基线、多 judge 和人工评测成本远不止单次运行。写作需 Gemini3.1Pro，检索为 Gemini3Flash＋联网搜索，另有图像生成和多轮审稿。以上为作者报告和配置判断，不是本地测量，也不假设外部 API 免费或无限。  多Agent协作 研究与论文写作 Agent 工具与协作执行：把计划变成可检查的动作 PaperOrchestra 为什么需要把已有实验材料组织成论证，而不只生成流畅论文段落？ 研究写作要把问题、方法、证据与引用连接起来，流畅文本可能掩盖缺失实验或不受支持的结论。PaperOrchestra 研究多角色如何围绕已有想法和日志协作写作、核查与修订。写作自动化不补足未做的科学验证，引用存在也不表示它支持当前主张。 教学例：日志只有两个数据集，就应围绕这两项解释证据；把语言改得更肯定，不能创造第三个实验或泛化结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-paperorchestra-986964dd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-99583ab8b60fcb1e">PaperOrchestra 为什么需要把已有实验材料组织成论证，而不只生成流畅论文段落？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apaperorchestra">PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究写作要把问题、方法、证据与引用连接起来，流畅文本可能掩盖缺失实验或不受支持的结论。PaperOrchestra 研究多角色如何围绕已有想法和日志协作写作、核查与修订。写作自动化不补足未做的科学验证，引用存在也不表示它支持当前主张。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：日志只有两个数据集，就应围绕这两项解释证据；把语言改得更肯定，不能创造第三个实验或泛化结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05018v1">原论文</a> · <a href="../../../../agent-research/2604.05018-paperorchestra/">实现解读</a> · <a href="#qa-99583ab8b60fcb1e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:paperorchestra" data-paper-title="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing Agent Google Cloud AI Research 2026-04-06 PaperOrchestra 用 Outline、Plotting、Literature Review、Section Writing、Content Refinement 五个 Agent，把零散想法和实验日志转成含文献与图表的 LaTeX 稿件。大纲之后图示与文献检索并行，引用经过实体和时间截止核验，最终根据多维评价接受或回退修订；系统不负责替作者发明或执行新实验。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。无可执行 adapter、生成能力指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。原文附录 B 在 10 篇计时子集报告每文约 60–70 次 LLM 调用、39.6 分钟裁尾均值；完整 200 篇、多基线、多 judge 和人工评测成本远不止单次运行。写作需 Gemini3.1Pro，检索为 Gemini3Flash＋联网搜索，另有图像生成和多轮审稿。以上为作者报告和配置判断，不是本地测量，也不假设外部 API 免费或无限。  多Agent协作 研究与论文写作 Agent 工具与协作执行：把计划变成可检查的动作 为什么引用核验与修订接纳不能替代真实实验和论文论证？ 引用实体、摘要和截止时间检查只保证来源身份及时间资格，修订分数只约束既有内容的改写方向。五类写作 Agent 应基于真实想法与日志组织稿件，不负责凭空创造结果；机械 BibTeX 校验或判定器也不能被包装为完整文献综合与研究能力。 例如图表 Agent 可根据已有实验日志画曲线，却不能为让稿件完整而填一组想象指标；引用真实也不会使虚构结果变真。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8dc7aca4108c4bbc">为什么引用核验与修订接纳不能替代真实实验和论文论证？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apaperorchestra">PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>引用实体、摘要和截止时间检查只保证来源身份及时间资格，修订分数只约束既有内容的改写方向。五类写作 Agent 应基于真实想法与日志组织稿件，不负责凭空创造结果；机械 BibTeX 校验或判定器也不能被包装为完整文献综合与研究能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如图表 Agent 可根据已有实验日志画曲线，却不能为让稿件完整而填一组想象指标；引用真实也不会使虚构结果变真。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05018v1">原论文</a> · <a href="../../../../agent-research/2604.05018-paperorchestra/">实现解读</a> · <a href="#qa-8dc7aca4108c4bbc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:paperorchestra" data-paper-title="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing Agent Google Cloud AI Research 2026-04-06 PaperOrchestra 用 Outline、Plotting、Literature Review、Section Writing、Content Refinement 五个 Agent，把零散想法和实验日志转成含文献与图表的 LaTeX 稿件。大纲之后图示与文献检索并行，引用经过实体和时间截止核验，最终根据多维评价接受或回退修订；系统不负责替作者发明或执行新实验。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。无可执行 adapter、生成能力指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。原文附录 B 在 10 篇计时子集报告每文约 60–70 次 LLM 调用、39.6 分钟裁尾均值；完整 200 篇、多基线、多 judge 和人工评测成本远不止单次运行。写作需 Gemini3.1Pro，检索为 Gemini3Flash＋联网搜索，另有图像生成和多轮审稿。以上为作者报告和配置判断，不是本地测量，也不假设外部 API 免费或无限。  多Agent协作 研究与论文写作 Agent 工具与协作执行：把计划变成可检查的动作 自动评价与人工偏好为什么不能当同一种写作质量结论？ 自动 judge 可能偏好形式与流畅度，人工尤其在文献综述上有不同判断，原文也报告两者相关性较弱。修订总分提高仍需核查事实和子维度，不能把单一 judge 提分当真实论文质量或研究正确性已验证。 例如生成更多相关术语可能让自动分数升高，但引用错配或夸大实验仍会降低专家对文献综述的评价。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-299e40fd9b62b309">自动评价与人工偏好为什么不能当同一种写作质量结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apaperorchestra">PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自动 judge 可能偏好形式与流畅度，人工尤其在文献综述上有不同判断，原文也报告两者相关性较弱。修订总分提高仍需核查事实和子维度，不能把单一 judge 提分当真实论文质量或研究正确性已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如生成更多相关术语可能让自动分数升高，但引用错配或夸大实验仍会降低专家对文献综述的评价。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05018v1">原论文</a> · <a href="../../../../agent-research/2604.05018-paperorchestra/">实现解读</a> · <a href="#qa-299e40fd9b62b309">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:paperorchestra" data-paper-title="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing Agent Google Cloud AI Research 2026-04-06 PaperOrchestra 用 Outline、Plotting、Literature Review、Section Writing、Content Refinement 五个 Agent，把零散想法和实验日志转成含文献与图表的 LaTeX 稿件。大纲之后图示与文献检索并行，引用经过实体和时间截止核验，最终根据多维评价接受或回退修订；系统不负责替作者发明或执行新实验。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。无可执行 adapter、生成能力指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。原文附录 B 在 10 篇计时子集报告每文约 60–70 次 LLM 调用、39.6 分钟裁尾均值；完整 200 篇、多基线、多 judge 和人工评测成本远不止单次运行。写作需 Gemini3.1Pro，检索为 Gemini3Flash＋联网搜索，另有图像生成和多轮审稿。以上为作者报告和配置判断，不是本地测量，也不假设外部 API 免费或无限。  多Agent协作 研究与论文写作 Agent 工具与协作执行：把计划变成可检查的动作 引用核验和修订回退有哪些具体条件，本地完成到哪一步？ 引用须匹配实际实体、有摘要、严格早于截止并按 paper ID 去重；修订分数下降，或平分但子轴净退步时回退，最多三轮。本地仅资料与成本审查，无五 Agent、写作模型或 metrics，不能用 BibTeX 检查器冒充完整文献综合能力。 例如同一论文两个网址应按实体去重，截止日之后的成果不能用来生成截止前研究材料；格式合法也不说明引用支持句子。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ac6886826864233b">引用核验和修订回退有哪些具体条件，本地完成到哪一步？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apaperorchestra">PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>引用须匹配实际实体、有摘要、严格早于截止并按 paper ID 去重；修订分数下降，或平分但子轴净退步时回退，最多三轮。本地仅资料与成本审查，无五 Agent、写作模型或 metrics，不能用 BibTeX 检查器冒充完整文献综合能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一论文两个网址应按实体去重，截止日之后的成果不能用来生成截止前研究材料；格式合法也不说明引用支持句子。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05018v1">原论文</a> · <a href="../../../../agent-research/2604.05018-paperorchestra/">实现解读</a> · <a href="#qa-ac6886826864233b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aira2" data-paper-title="AIRA2: Overcoming Bottlenecks in AI Research Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AIRA2: Overcoming Bottlenecks in AI Research Agents Agent FAIR at Meta / University College London 2026-03-27 以无同步屏障的 steady-state worker pool 提高实验吞吐；训练、搜索、最终选择使用固定的 80/10/10 隐藏切分，搜索只看 search score，结束后才用未参与爬山的 validation 选冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。三种子诊断：metrics/mechanism-seeds42-44.json  AI 研究 Agent 异步进化 隐藏一致评测 Agent 工具与协作执行：把计划变成可检查的动作 AIR-A2 为什么把自动 ML 研究看成实验资源调度问题，而不只是多提几个点子？ 研究 Agent 可不断产生候选，但训练实验耗时不同，设备和评测预算有限，提案质量与执行吞吐会共同影响搜索进展。AIR-A2 关注让实验管线持续工作并管理候选反馈。忙碌程度不等于研究收益，最终仍要在隔离评测中核验选中方案。 教学例：一个实验跑两小时，另一个只跑十分钟；若整代都等最长任务，空闲设备就无法及时试新的候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-aira2-3f4a88e8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-4269c39e84e5ecd2">AIR-A2 为什么把自动 ML 研究看成实验资源调度问题，而不只是多提几个点子？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaira2">AIRA2: Overcoming Bottlenecks in AI Research Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / University College London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究 Agent 可不断产生候选，但训练实验耗时不同，设备和评测预算有限，提案质量与执行吞吐会共同影响搜索进展。AIR-A2 关注让实验管线持续工作并管理候选反馈。忙碌程度不等于研究收益，最终仍要在隔离评测中核验选中方案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一个实验跑两小时，另一个只跑十分钟；若整代都等最长任务，空闲设备就无法及时试新的候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26499">原论文</a> · <a href="../../../../agent-research/2603.26499-aira2/">实现解读</a> · <a href="#qa-4269c39e84e5ecd2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aira2" data-paper-title="AIRA2: Overcoming Bottlenecks in AI Research Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AIRA2: Overcoming Bottlenecks in AI Research Agents Agent FAIR at Meta / University College London 2026-03-27 以无同步屏障的 steady-state worker pool 提高实验吞吐；训练、搜索、最终选择使用固定的 80/10/10 隐藏切分，搜索只看 search score，结束后才用未参与爬山的 validation 选冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。三种子诊断：metrics/mechanism-seeds42-44.json  AI 研究 Agent 异步进化 隐藏一致评测 Agent 工具与协作执行：把计划变成可检查的动作 为什么 steady-state worker pool 比每代等待全部实验结束更能利用计算资源？ 不同实验耗时不一，同步屏障会让快任务完成后闲等最慢者；持续池让空闲 worker 立即接下一候选。吞吐提升不应改变评测隔离：搜索仅用固定 search 分数，结束后再由未参与爬山的 validation 选冠军，不能边跑边偷看最终选择集。 例如三个实验十分钟完成、一个要一小时，同步代会浪费前三个槽位；持续池可继续试验，但仍共享预先冻结的数据切分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6b1a28c04e252ad2">为什么 steady-state worker pool 比每代等待全部实验结束更能利用计算资源？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaira2">AIRA2: Overcoming Bottlenecks in AI Research Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / University College London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同实验耗时不一，同步屏障会让快任务完成后闲等最慢者；持续池让空闲 worker 立即接下一候选。吞吐提升不应改变评测隔离：搜索仅用固定 search 分数，结束后再由未参与爬山的 validation 选冠军，不能边跑边偷看最终选择集。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三个实验十分钟完成、一个要一小时，同步代会浪费前三个槽位；持续池可继续试验，但仍共享预先冻结的数据切分。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26499">原论文</a> · <a href="../../../../agent-research/2603.26499-aira2/">实现解读</a> · <a href="#qa-6b1a28c04e252ad2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aira2" data-paper-title="AIRA2: Overcoming Bottlenecks in AI Research Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AIRA2: Overcoming Bottlenecks in AI Research Agents Agent FAIR at Meta / University College London 2026-03-27 以无同步屏障的 steady-state worker pool 提高实验吞吐；训练、搜索、最终选择使用固定的 80/10/10 隐藏切分，搜索只看 search score，结束后才用未参与爬山的 validation 选冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。三种子诊断：metrics/mechanism-seeds42-44.json  AI 研究 Agent 异步进化 隐藏一致评测 Agent 工具与协作执行：把计划变成可检查的动作 search split 与最终 validation 分开的目的是什么？ 搜索会反复利用分数选择候选，容易对 search 集爬山；最终 validation 未参与这段过程，结束时才选冠军，可减少选择过拟合。两者都不是训练数据，也不意味着 validation 可无限反复用来修改搜索策略，隐藏 test 更不能进入接口。 例如一百个候选都按 search 排名探索，最后只用保留的 validation 选最终模型，而不是每次都看 validation 再继续改候选。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-58f57008467d2ded">search split 与最终 validation 分开的目的是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaira2">AIRA2: Overcoming Bottlenecks in AI Research Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / University College London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>搜索会反复利用分数选择候选，容易对 search 集爬山；最终 validation 未参与这段过程，结束时才选冠军，可减少选择过拟合。两者都不是训练数据，也不意味着 validation 可无限反复用来修改搜索策略，隐藏 test 更不能进入接口。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一百个候选都按 search 排名探索，最后只用保留的 validation 选最终模型，而不是每次都看 validation 再继续改候选。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26499">原论文</a> · <a href="../../../../agent-research/2603.26499-aira2/">实现解读</a> · <a href="#qa-58f57008467d2ded">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:aira2" data-paper-title="AIRA2: Overcoming Bottlenecks in AI Research Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AIRA2: Overcoming Bottlenecks in AI Research Agents Agent FAIR at Meta / University College London 2026-03-27 以无同步屏障的 steady-state worker pool 提高实验吞吐；训练、搜索、最终选择使用固定的 80/10/10 隐藏切分，搜索只看 search score，结束后才用未参与爬山的 validation 选冠军。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。本地只执行异步调度与 HCE 信号隔离；未复刻 8×H200、Apptainer、Gemini ReAct operator 或论文长时训练，因此不是多 GPU 性能复现。三种子诊断：metrics/mechanism-seeds42-44.json  AI 研究 Agent 异步进化 隐藏一致评测 Agent 工具与协作执行：把计划变成可检查的动作 80/10/10 能否每个候选重新随机切分？ 不能。一次固定切分需跨候选一致，否则分数差混入数据难度差，无法公平比较；本地只验证异步调度与信号隔离，未复刻多 H200、Apptainer 或长时研究 Agent。rank-based 选择概率也只是搜索规则，不是候选真实性能证明。 例如甲刚好拿到简单 search 样本、乙拿到难样本，即使两者模型相同也可能排名不同，固定 split 才能控制这项混杂。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c3a6743a353f8dfc">80/10/10 能否每个候选重新随机切分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aaira2">AIRA2: Overcoming Bottlenecks in AI Research Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / University College London</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。一次固定切分需跨候选一致，否则分数差混入数据难度差，无法公平比较；本地只验证异步调度与信号隔离，未复刻多 H200、Apptainer 或长时研究 Agent。rank-based 选择概率也只是搜索规则，不是候选真实性能证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如甲刚好拿到简单 search 样本、乙拿到难样本，即使两者模型相同也可能排名不同，固定 split 才能控制这项混杂。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.26499">原论文</a> · <a href="../../../../agent-research/2603.26499-aira2/">实现解读</a> · <a href="#qa-c3a6743a353f8dfc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dynamic-brt" data-paper-title="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair Agent Google 2026-01-27 论文让修复和 BRT 留在同一条轨迹；TDD、TLD、Freeform 改变生成顺序。BRT 必须在原 bug 上失败、生成修复上通过。选择器按非测试修复归组，避免不同测试拆散同一修复的票数；ranked 在多数修复组内优先保留测试。原文 §3 完整实验：成本过高，不复现（审查 DONE）。component_only / L1 机制诊断。component_only / L1 机制诊断。实现测试验证及选择器，没有实现或宣称 Passerine 生成 Agent 的能力。完整实验：成本过高，不复现（审查 DONE）。11 项单元测试已通过。自建 increment 算术实例真实启动独立 Python 子进程，观察 assertion_failed → passed；恒真测试、异常而非断言失败、未通过回归的修复均不接纳。ranked 与 dual 的不同选项已通过多数分组实例验证。诊断指标  代码 Agent 程序修复 测试与验证 Agent 工具与协作执行：把计划变成可检查的动作 自动修 bug 时，为什么先得到能复现问题的测试很有价值？ 文字 issue 往往不够精确，复现测试把失败条件变成可执行观察，帮助区分补丁是否改变目标行为。Dynamic BRT 研究在候选修复过程中生成和选择这类测试。它们提供局部证据，覆盖不足或为错误补丁量身定制的测试仍可能误导，不能代替完整正确性验证。 教学例：报告说空列表会崩溃，复现测试固定这个输入并检查异常；补丁通过该测试后，其他输入仍需要独立检查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-dynamic-brt-f3fe2d3c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-21b0ad9ec1ec3a10">自动修 bug 时，为什么先得到能复现问题的测试很有价值？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adynamic-brt">Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文字 issue 往往不够精确，复现测试把失败条件变成可执行观察，帮助区分补丁是否改变目标行为。Dynamic BRT 研究在候选修复过程中生成和选择这类测试。它们提供局部证据，覆盖不足或为错误补丁量身定制的测试仍可能误导，不能代替完整正确性验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：报告说空列表会崩溃，复现测试固定这个输入并检查异常；补丁通过该测试后，其他输入仍需要独立检查。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.19066">原论文</a> · <a href="../../../../agent-research/2601.19066-dynamic-brt/">实现解读</a> · <a href="#qa-21b0ad9ec1ec3a10">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dynamic-brt" data-paper-title="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair Agent Google 2026-01-27 论文让修复和 BRT 留在同一条轨迹；TDD、TLD、Freeform 改变生成顺序。BRT 必须在原 bug 上失败、生成修复上通过。选择器按非测试修复归组，避免不同测试拆散同一修复的票数；ranked 在多数修复组内优先保留测试。原文 §3 完整实验：成本过高，不复现（审查 DONE）。component_only / L1 机制诊断。component_only / L1 机制诊断。实现测试验证及选择器，没有实现或宣称 Passerine 生成 Agent 的能力。完整实验：成本过高，不复现（审查 DONE）。11 项单元测试已通过。自建 increment 算术实例真实启动独立 Python 子进程，观察 assertion_failed → passed；恒真测试、异常而非断言失败、未通过回归的修复均不接纳。ranked 与 dual 的不同选项已通过多数分组实例验证。诊断指标  代码 Agent 程序修复 测试与验证 Agent 工具与协作执行：把计划变成可检查的动作 测试在原 bug 上失败、在生成修复上通过，为什么还不能证明修复正确？ 自生成测试可能只覆盖修复碰巧满足的局部行为，二者相互吻合不等于原题完整语义。这个条件只定义候选 BRT；更强的可信判断还需隔离参考修复等验证。按非测试 patch 分组投票，也避免同一修复因配了不同测试而被拆散票数。 例如修复把返回值写成常量，自测也只检查这一个输入，两项条件都可能通过，但其他输入仍错，不能宣称真正修好。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bc8c2cd9cd8b383e">测试在原 bug 上失败、在生成修复上通过，为什么还不能证明修复正确？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adynamic-brt">Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自生成测试可能只覆盖修复碰巧满足的局部行为，二者相互吻合不等于原题完整语义。这个条件只定义候选 BRT；更强的可信判断还需隔离参考修复等验证。按非测试 patch 分组投票，也避免同一修复因配了不同测试而被拆散票数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如修复把返回值写成常量，自测也只检查这一个输入，两项条件都可能通过，但其他输入仍错，不能宣称真正修好。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.19066">原论文</a> · <a href="../../../../agent-research/2601.19066-dynamic-brt/">实现解读</a> · <a href="#qa-bc8c2cd9cd8b383e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dynamic-brt" data-paper-title="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair Agent Google 2026-01-27 论文让修复和 BRT 留在同一条轨迹；TDD、TLD、Freeform 改变生成顺序。BRT 必须在原 bug 上失败、生成修复上通过。选择器按非测试修复归组，避免不同测试拆散同一修复的票数；ranked 在多数修复组内优先保留测试。原文 §3 完整实验：成本过高，不复现（审查 DONE）。component_only / L1 机制诊断。component_only / L1 机制诊断。实现测试验证及选择器，没有实现或宣称 Passerine 生成 Agent 的能力。完整实验：成本过高，不复现（审查 DONE）。11 项单元测试已通过。自建 increment 算术实例真实启动独立 Python 子进程，观察 assertion_failed → passed；恒真测试、异常而非断言失败、未通过回归的修复均不接纳。ranked 与 dual 的不同选项已通过多数分组实例验证。诊断指标  代码 Agent 程序修复 测试与验证 Agent 工具与协作执行：把计划变成可检查的动作 为什么选择器按非测试 patch 归组，而不把每份测试各算一个候选？ 同一修复可搭配多个不同测试，若逐对计票会拆散或放大同一代码方案的支持。按非测试部分归组再在多数修复组内选测试，更接近比较实际修复；标识符归一化仍是启发式，不是语义等价证明。 例如十条轨迹生成同样代码但不同断言，应该识别为一个修复组，而不是十种独立修复策略。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-b670f7557ce5a306">为什么选择器按非测试 patch 归组，而不把每份测试各算一个候选？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adynamic-brt">Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一修复可搭配多个不同测试，若逐对计票会拆散或放大同一代码方案的支持。按非测试部分归组再在多数修复组内选测试，更接近比较实际修复；标识符归一化仍是启发式，不是语义等价证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十条轨迹生成同样代码但不同断言，应该识别为一个修复组，而不是十种独立修复策略。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.19066">原论文</a> · <a href="../../../../agent-research/2601.19066-dynamic-brt/">实现解读</a> · <a href="#qa-b670f7557ce5a306">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:dynamic-brt" data-paper-title="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair Agent Google 2026-01-27 论文让修复和 BRT 留在同一条轨迹；TDD、TLD、Freeform 改变生成顺序。BRT 必须在原 bug 上失败、生成修复上通过。选择器按非测试修复归组，避免不同测试拆散同一修复的票数；ranked 在多数修复组内优先保留测试。原文 §3 完整实验：成本过高，不复现（审查 DONE）。component_only / L1 机制诊断。component_only / L1 机制诊断。实现测试验证及选择器，没有实现或宣称 Passerine 生成 Agent 的能力。完整实验：成本过高，不复现（审查 DONE）。11 项单元测试已通过。自建 increment 算术实例真实启动独立 Python 子进程，观察 assertion_failed → passed；恒真测试、异常而非断言失败、未通过回归的修复均不接纳。ranked 与 dual 的不同选项已通过多数分组实例验证。诊断指标  代码 Agent 程序修复 测试与验证 Agent 工具与协作执行：把计划变成可检查的动作 执行失败能否把任意异常都视为成功复现 bug？ 不能。本地要求非空断言在原程序触发 assertion_failed，再在修复上通过且回归合格；语法错误或其他异常不算 BRT。执行仅支持有限 AST 白名单和独立限时进程，不是任意恶意代码沙箱，也未运行真实 LLM reviewers 或私有 Google bug。 例如原测试因 import 不存在而崩溃，不证明它复现业务 bug；不能与修复后正常运行简单配成“失败到通过”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d498db4f0ce1da26">执行失败能否把任意异常都视为成功复现 bug？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adynamic-brt">Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地要求非空断言在原程序触发 assertion_failed，再在修复上通过且回归合格；语法错误或其他异常不算 BRT。执行仅支持有限 AST 白名单和独立限时进程，不是任意恶意代码沙箱，也未运行真实 LLM reviewers 或私有 Google bug。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如原测试因 import 不存在而崩溃，不证明它复现业务 bug；不能与修复后正常运行简单配成“失败到通过”。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.19066">原论文</a> · <a href="../../../../agent-research/2601.19066-dynamic-brt/">实现解读</a> · <a href="#qa-d498db4f0ce1da26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:watch-and-learn" data-paper-title="Watch and Learn: Learning to Use Computers from Online Videos" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Watch and Learn: Learning to Use Computers from Online Videos Agent The Ohio State University 2025-10-06 W&amp;L 把“视频里发生了什么操作”建模为逆动力学：输入前后两张屏幕图像，预测导致状态变化的动作。训练好的 IDM 再标注网络教程视频，结合任务检索形成轨迹，分别用于 CUA 的上下文示范和监督训练，而非直接让通用大模型猜动作或用规则恢复轨迹。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。本页没有可执行 adapter、组件指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。固定 v1 §3.1/附录 D.3 使用超过 630k 状态转移，IDM 训练为 8×A100 80GB、15 epochs；另有 53,125 个视频轨迹、7B CUA SFT、联网检索/API 和真实 OSWorld 桌面评测。该配置明显超过单张 A100/A30 或本地 Mac 的短时预算；这是作者配置形成的成本判断，不是本地计时。  工具与环境交互 计算机使用与视频示范 Agent 工具与协作执行：把计划变成可检查的动作 Watch and Learn 为什么尝试利用网上教程视频，而不只依赖昂贵的操作轨迹标注？ 教程视频含有真实软件操作过程，但通常没有机器可直接学习的点击坐标、按键和动作序列。该工作研究把可见演示转成计算机使用训练材料，扩大数据来源。画面本身不是动作真值，遮挡、录制剪辑和输入文本缺失都会影响转化质量与后续执行。 教学例：教程显示文件从一个窗口移到另一个，训练前仍要辨别发生了拖动还是复制命令，不能只凭截图差异编一个点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-watch-and-learn-e9cf239b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-78e1133fbfd419f4">Watch and Learn 为什么尝试利用网上教程视频，而不只依赖昂贵的操作轨迹标注？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awatch-and-learn">Watch and Learn: Learning to Use Computers from Online Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>教程视频含有真实软件操作过程，但通常没有机器可直接学习的点击坐标、按键和动作序列。该工作研究把可见演示转成计算机使用训练材料，扩大数据来源。画面本身不是动作真值，遮挡、录制剪辑和输入文本缺失都会影响转化质量与后续执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：教程显示文件从一个窗口移到另一个，训练前仍要辨别发生了拖动还是复制命令，不能只凭截图差异编一个点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04673v1">原论文</a> · <a href="../../../../agent-research/2510.04673-watch-and-learn/">实现解读</a> · <a href="#qa-78e1133fbfd419f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:watch-and-learn" data-paper-title="Watch and Learn: Learning to Use Computers from Online Videos" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Watch and Learn: Learning to Use Computers from Online Videos Agent The Ohio State University 2025-10-06 W&amp;L 把“视频里发生了什么操作”建模为逆动力学：输入前后两张屏幕图像，预测导致状态变化的动作。训练好的 IDM 再标注网络教程视频，结合任务检索形成轨迹，分别用于 CUA 的上下文示范和监督训练，而非直接让通用大模型猜动作或用规则恢复轨迹。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。本页没有可执行 adapter、组件指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。固定 v1 §3.1/附录 D.3 使用超过 630k 状态转移，IDM 训练为 8×A100 80GB、15 epochs；另有 53,125 个视频轨迹、7B CUA SFT、联网检索/API 和真实 OSWorld 桌面评测。该配置明显超过单张 A100/A30 或本地 Mac 的短时预算；这是作者配置形成的成本判断，不是本地计时。  工具与环境交互 计算机使用与视频示范 Agent 工具与协作执行：把计划变成可检查的动作 为什么看教程视频需要学习逆动力学，而不是把前后截图差异直接当成鼠标动作？ 视觉变化可能来自滚动、键盘输入或程序响应，仅像素差无法唯一确定操作。逆动力学模型在前后屏幕上预测动作类型、坐标与文本，再把推断串成轨迹供检索和训练；这些标签仍是模型估计，不能把规则恢复或随意猜动作冒充已训练的 IDM。 例如页面向下移动可能由滚轮也可能由按键触发，动作模型需结合画面与监督区分，而非看到内容下移就硬填一次点击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6d5dc634ef7c4b6c">为什么看教程视频需要学习逆动力学，而不是把前后截图差异直接当成鼠标动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awatch-and-learn">Watch and Learn: Learning to Use Computers from Online Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>视觉变化可能来自滚动、键盘输入或程序响应，仅像素差无法唯一确定操作。逆动力学模型在前后屏幕上预测动作类型、坐标与文本，再把推断串成轨迹供检索和训练；这些标签仍是模型估计，不能把规则恢复或随意猜动作冒充已训练的 IDM。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如页面向下移动可能由滚轮也可能由按键触发，动作模型需结合画面与监督区分，而非看到内容下移就硬填一次点击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04673v1">原论文</a> · <a href="../../../../agent-research/2510.04673-watch-and-learn/">实现解读</a> · <a href="#qa-6d5dc634ef7c4b6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:watch-and-learn" data-paper-title="Watch and Learn: Learning to Use Computers from Online Videos" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Watch and Learn: Learning to Use Computers from Online Videos Agent The Ohio State University 2025-10-06 W&amp;L 把“视频里发生了什么操作”建模为逆动力学：输入前后两张屏幕图像，预测导致状态变化的动作。训练好的 IDM 再标注网络教程视频，结合任务检索形成轨迹，分别用于 CUA 的上下文示范和监督训练，而非直接让通用大模型猜动作或用规则恢复轨迹。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。本页没有可执行 adapter、组件指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。固定 v1 §3.1/附录 D.3 使用超过 630k 状态转移，IDM 训练为 8×A100 80GB、15 epochs；另有 53,125 个视频轨迹、7B CUA SFT、联网检索/API 和真实 OSWorld 桌面评测。该配置明显超过单张 A100/A30 或本地 Mac 的短时预算；这是作者配置形成的成本判断，不是本地计时。  工具与环境交互 计算机使用与视频示范 Agent 工具与协作执行：把计划变成可检查的动作 视频示范检索与用标注轨迹监督训练分别改变什么？ 检索在当前上下文提供相关演示，不改执行模型参数；SFT 将轨迹模式写入参数。两者都依赖 IDM 标注质量，不能把视频数量直接当正确动作样本数，也不能仅凭相同标题宣称已经完成真实桌面学习。 例如同一教程可被放进 prompt 作为范例，也可用于离线训练，但部署成本与错误传播路径不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-26c0fe3cc14e615b">视频示范检索与用标注轨迹监督训练分别改变什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awatch-and-learn">Watch and Learn: Learning to Use Computers from Online Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>检索在当前上下文提供相关演示，不改执行模型参数；SFT 将轨迹模式写入参数。两者都依赖 IDM 标注质量，不能把视频数量直接当正确动作样本数，也不能仅凭相同标题宣称已经完成真实桌面学习。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一教程可被放进 prompt 作为范例，也可用于离线训练，但部署成本与错误传播路径不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04673v1">原论文</a> · <a href="../../../../agent-research/2510.04673-watch-and-learn/">实现解读</a> · <a href="#qa-26c0fe3cc14e615b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:watch-and-learn" data-paper-title="Watch and Learn: Learning to Use Computers from Online Videos" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Watch and Learn: Learning to Use Computers from Online Videos Agent The Ohio State University 2025-10-06 W&amp;L 把“视频里发生了什么操作”建模为逆动力学：输入前后两张屏幕图像，预测导致状态变化的动作。训练好的 IDM 再标注网络教程视频，结合任务检索形成轨迹，分别用于 CUA 的上下文示范和监督训练，而非直接让通用大模型猜动作或用规则恢复轨迹。 历史目录补漏：成本过高，不复现（审查 DONE）。历史目录补漏：成本过高，不复现（审查 DONE）。本页没有可执行 adapter、组件指标或 GPU 通过声明，不进入自动实现/重试队列。成本过高，不复现（审查 DONE）。固定 v1 §3.1/附录 D.3 使用超过 630k 状态转移，IDM 训练为 8×A100 80GB、15 epochs；另有 53,125 个视频轨迹、7B CUA SFT、联网检索/API 和真实 OSWorld 桌面评测。该配置明显超过单张 A100/A30 或本地 Mac 的短时预算；这是作者配置形成的成本判断，不是本地计时。  工具与环境交互 计算机使用与视频示范 Agent 工具与协作执行：把计划变成可检查的动作 动作、坐标和输入文本为何不能用一个简单规则头代替？ 原文用动作分类、离散到 0–1000 的坐标分类及 GPT-2 small 文本自回归头，配合 SigLIP-2 和四层 Transformer。三项损失未披露额外权重就不能补造；本地只有资料与成本审查，无 IDM、语料下载或桌面评测。 例如能从鼠标位置差猜点击的规则，不会自动学会从两张截图恢复输入文本，更不能替代联合训练的 IDM。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-30274243761e3d5f">动作、坐标和输入文本为何不能用一个简单规则头代替？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awatch-and-learn">Watch and Learn: Learning to Use Computers from Online Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Ohio State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原文用动作分类、离散到 0–1000 的坐标分类及 GPT-2 small 文本自回归头，配合 SigLIP-2 和四层 Transformer。三项损失未披露额外权重就不能补造；本地只有资料与成本审查，无 IDM、语料下载或桌面评测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如能从鼠标位置差猜点击的规则，不会自动学会从两张截图恢复输入文本，更不能替代联合训练的 IDM。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.04673v1">原论文</a> · <a href="../../../../agent-research/2510.04673-watch-and-learn/">实现解读</a> · <a href="#qa-30274243761e3d5f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolgrad" data-paper-title="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients Agent Google 2025-08-06 先从目标答案反推工具轨迹，再使用 textual gradient 定位并修订失败调用，降低人工轨迹标注成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  工具学习 数据生成 Agent 工具与协作执行：把计划变成可检查的动作 ToolGrad 为什么关注生成高质量工具调用训练轨迹的成本？ 多步工具任务需要正确接口、参数和结果衔接，人工示范昂贵，模型直接生成又可能积累调用错误。ToolGrad 研究在数据构建侧利用目标反馈修订轨迹，为后续学习提供可执行样本。训练构造时可见的目标不能偷渡给评测 Agent，否则不再是在未知答案下使用工具。 教学例：构造数据时可检查查询是否通向预定结果并修订参数；测试时 Agent 应自己获得证据，不能先读标准答案再挑查询。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-toolgrad-568745ef" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a8c8872eb7a3514e">ToolGrad 为什么关注生成高质量工具调用训练轨迹的成本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolgrad">ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多步工具任务需要正确接口、参数和结果衔接，人工示范昂贵，模型直接生成又可能积累调用错误。ToolGrad 研究在数据构建侧利用目标反馈修订轨迹，为后续学习提供可执行样本。训练构造时可见的目标不能偷渡给评测 Agent，否则不再是在未知答案下使用工具。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：构造数据时可检查查询是否通向预定结果并修订参数；测试时 Agent 应自己获得证据，不能先读标准答案再挑查询。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.04086">原论文</a> · <a href="../../../../agent-research/2508.04086-toolgrad/">实现解读</a> · <a href="#qa-a8c8872eb7a3514e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolgrad" data-paper-title="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients Agent Google 2025-08-06 先从目标答案反推工具轨迹，再使用 textual gradient 定位并修订失败调用，降低人工轨迹标注成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  工具学习 数据生成 Agent 工具与协作执行：把计划变成可检查的动作 从目标答案反推轨迹为什么只适合数据生成侧，而不能作为评测 Agent 的输入？ 反推利用已知答案构造候选工具链，textual gradient 再定位失败调用并修订，目的是减少训练轨迹标注。评测若把目标答案传给行动者，就已经泄漏任务目标值，不能衡量独立取证；训练数据的构造信息与部署时可见信息必须明确分开。 例如训练侧已知某城市人口，可反查需要哪些 API；测试时 Agent 应只接到人口问题，不能同时拿到参考数字再安排搜索。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-48defda29bfde8a3">从目标答案反推轨迹为什么只适合数据生成侧，而不能作为评测 Agent 的输入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolgrad">ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>反推利用已知答案构造候选工具链，textual gradient 再定位失败调用并修订，目的是减少训练轨迹标注。评测若把目标答案传给行动者，就已经泄漏任务目标值，不能衡量独立取证；训练数据的构造信息与部署时可见信息必须明确分开。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练侧已知某城市人口，可反查需要哪些 API；测试时 Agent 应只接到人口问题，不能同时拿到参考数字再安排搜索。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.04086">原论文</a> · <a href="../../../../agent-research/2508.04086-toolgrad/">实现解读</a> · <a href="#qa-48defda29bfde8a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolgrad" data-paper-title="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients Agent Google 2025-08-06 先从目标答案反推工具轨迹，再使用 textual gradient 定位并修订失败调用，降低人工轨迹标注成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  工具学习 数据生成 Agent 工具与协作执行：把计划变成可检查的动作 textual gradient 与数值梯度在修订失败调用时有何区别？ textual gradient 是用语言指出参数、工具或顺序问题，再生成文本修改，不是对离散调用直接做可微反传。它依赖反馈质量与真实执行验证，不能因名称有 gradient 就声称完成端到端参数优化，也不能用修订文字代替重跑。 例如反馈说“日期格式错误”后把参数改成标准格式，这是文本编辑；是否修好还要实际调用并检查返回。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-637567167fcf5e81">textual gradient 与数值梯度在修订失败调用时有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolgrad">ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>textual gradient 是用语言指出参数、工具或顺序问题，再生成文本修改，不是对离散调用直接做可微反传。它依赖反馈质量与真实执行验证，不能因名称有 gradient 就声称完成端到端参数优化，也不能用修订文字代替重跑。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如反馈说“日期格式错误”后把参数改成标准格式，这是文本编辑；是否修好还要实际调用并检查返回。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.04086">原论文</a> · <a href="../../../../agent-research/2508.04086-toolgrad/">实现解读</a> · <a href="#qa-637567167fcf5e81">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolgrad" data-paper-title="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients Agent Google 2025-08-06 先从目标答案反推工具轨迹，再使用 textual gradient 定位并修订失败调用，降低人工轨迹标注成本。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。本地执行 answer-first 路线与去重 textual edit；未训练 12B 模型或运行 BFCL。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  工具学习 数据生成 Agent 工具与协作执行：把计划变成可检查的动作 本地 answer-first 与去重 edit 的证据能覆盖 ToolGrad-12B 和 BFCL 吗？ 不能。本地只执行反推路线和去重文本修订 reference，未训练 12B 模型或运行 BFCL。必须保留答案仅训练侧可见、执行结果真实且失败不回填的边界；状态转换通过不等于生成数据质量和下游工具能力已提升。 例如同一错误参数被改两次后去重，可验证编辑规则，却没有证明模型能为未知 API 自动生成正确训练轨迹。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b381ff66f4e2605b">本地 answer-first 与去重 edit 的证据能覆盖 ToolGrad-12B 和 BFCL 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolgrad">ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地只执行反推路线和去重文本修订 reference，未训练 12B 模型或运行 BFCL。必须保留答案仅训练侧可见、执行结果真实且失败不回填的边界；状态转换通过不等于生成数据质量和下游工具能力已提升。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一错误参数被改两次后去重，可验证编辑规则，却没有证明模型能为未知 API 自动生成正确训练轨迹。</p>
<p class="ar-learning-sources">依据：核心公式或操作、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.04086">原论文</a> · <a href="../../../../agent-research/2508.04086-toolgrad/">实现解读</a> · <a href="#qa-b381ff66f4e2605b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolrl" data-paper-title="ToolRL" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolRL Agent University of Illinois Urbana-Champaign 2025-04-16 联合优化工具选择、参数生成和执行结果；动态 reward scaling 让不同工具难度进入同一 RL batch。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.1250；方法特有操作有非零 telemetry。  工具强化学习 Agent 工具与协作执行：把计划变成可检查的动作 ToolRL 为什么不能只检查最后一句答案对不对，就认为工具策略已经学好？ 最终结果把选工具、填参数、执行和利用返回值混在一起，难判断失败来自哪一步。ToolRL 研究用更细的工具反馈训练策略，使行为本身也接受约束。多项奖励仍需合理校准，不能用格式正确或执行成功掩盖答案错误，也不能把本地奖励计算当成大模型 RL 完成。 教学例：选对天气工具却传错城市，返回值格式仍正常；只给最终答案一个分数，很难定位应改的是参数还是工具选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-toolrl-7e3d5cc8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7dbdad52ce7f9b4a">ToolRL 为什么不能只检查最后一句答案对不对，就认为工具策略已经学好？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolrl">ToolRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终结果把选工具、填参数、执行和利用返回值混在一起，难判断失败来自哪一步。ToolRL 研究用更细的工具反馈训练策略，使行为本身也接受约束。多项奖励仍需合理校准，不能用格式正确或执行成功掩盖答案错误，也不能把本地奖励计算当成大模型 RL 完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：选对天气工具却传错城市，返回值格式仍正常；只给最终答案一个分数，很难定位应改的是参数还是工具选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.13958">原论文</a> · <a href="../../../../agent-research/2504.13958-toolrl/">实现解读</a> · <a href="#qa-7dbdad52ce7f9b4a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolrl" data-paper-title="ToolRL" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolRL Agent University of Illinois Urbana-Champaign 2025-04-16 联合优化工具选择、参数生成和执行结果；动态 reward scaling 让不同工具难度进入同一 RL batch。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.1250；方法特有操作有非零 telemetry。  工具强化学习 Agent 工具与协作执行：把计划变成可检查的动作 不同工具奖励难度不同时，为什么要做工具条件下的动态 scaling？ 容易工具的高原始奖励可能主导同一批更新，困难工具虽有进步却被淹没。按工具分布中心化和缩放，让相对表现更可比较，同时保留选择、参数、执行与答案多种信号；归一化不自动修正错误奖励定义，也不意味着所有工具实际难度相同。 例如计算器多数能成功，数据库复杂查询常失败；分别按各自奖励分布评价进步，避免训练只偏向更容易拿分的计算器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-39b3cc929256b458">不同工具奖励难度不同时，为什么要做工具条件下的动态 scaling？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolrl">ToolRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>容易工具的高原始奖励可能主导同一批更新，困难工具虽有进步却被淹没。按工具分布中心化和缩放，让相对表现更可比较，同时保留选择、参数、执行与答案多种信号；归一化不自动修正错误奖励定义，也不意味着所有工具实际难度相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如计算器多数能成功，数据库复杂查询常失败；分别按各自奖励分布评价进步，避免训练只偏向更容易拿分的计算器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.13958">原论文</a> · <a href="../../../../agent-research/2504.13958-toolrl/">实现解读</a> · <a href="#qa-39b3cc929256b458">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolrl" data-paper-title="ToolRL" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolRL Agent University of Illinois Urbana-Champaign 2025-04-16 联合优化工具选择、参数生成和执行结果；动态 reward scaling 让不同工具难度进入同一 RL batch。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.1250；方法特有操作有非零 telemetry。  工具强化学习 Agent 工具与协作执行：把计划变成可检查的动作 工具选择奖励与执行、答案奖励，为什么不能互相替代？ 选择奖励检查接口是否匹配任务，执行奖励检查调用能否实际运行，答案奖励评价是否完成最终目标。正确选择可能因参数错误而执行失败，成功执行也可能返回与问题无关的信息。分开监督能暴露这些不同错误，不能把任一环节高分直接当作端到端能力。 教学例：数据库工具选对且查询成功，但时间范围写错，得到另一月份的结果；前两项通过并不意味着最终答案应获奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-119474e77ea679ab">工具选择奖励与执行、答案奖励，为什么不能互相替代？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolrl">ToolRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>选择奖励检查接口是否匹配任务，执行奖励检查调用能否实际运行，答案奖励评价是否完成最终目标。正确选择可能因参数错误而执行失败，成功执行也可能返回与问题无关的信息。分开监督能暴露这些不同错误，不能把任一环节高分直接当作端到端能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：数据库工具选对且查询成功，但时间范围写错，得到另一月份的结果；前两项通过并不意味着最终答案应获奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.13958">原论文</a> · <a href="../../../../agent-research/2504.13958-toolrl/">实现解读</a> · <a href="#qa-119474e77ea679ab">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolrl" data-paper-title="ToolRL" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolRL Agent University of Illinois Urbana-Champaign 2025-04-16 联合优化工具选择、参数生成和执行结果；动态 reward scaling 让不同工具难度进入同一 RL batch。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.1250；方法特有操作有非零 telemetry。  工具强化学习 Agent 工具与协作执行：把计划变成可检查的动作 本地奖励和状态更新是否证明真实多工具 RL 训练完成？ 没有。本地只验证论文特有目标、转移与预算，没有原文大模型、多卡 RL 或完整真实工具 benchmark。奖励计算正确可检验公式，但还需策略实际采样、外部执行和参数更新，不能以方法注册或 mini-suite 满分补齐这些证据。 例如给定四轴分数算出 advantage 只是目标函数测试，若没有训练模型，就不能声称它已学会参数生成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ecda3bd045c50ef5">本地奖励和状态更新是否证明真实多工具 RL 训练完成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolrl">ToolRL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地只验证论文特有目标、转移与预算，没有原文大模型、多卡 RL 或完整真实工具 benchmark。奖励计算正确可检验公式，但还需策略实际采样、外部执行和参数更新，不能以方法注册或 mini-suite 满分补齐这些证据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给定四轴分数算出 advantage 只是目标函数测试，若没有训练模型，就不能声称它已学会参数生成。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.13958">原论文</a> · <a href="../../../../agent-research/2504.13958-toolrl/">实现解读</a> · <a href="#qa-ecda3bd045c50ef5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:retool" data-paper-title="ReTool" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ReTool Agent ByteDance Seed 2025-04-15 策略在自然语言 reasoning 与工具执行之间交替，并由可执行反馈学习调用、纠错和停止。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.0500；方法特有操作有非零 telemetry。  推理中工具调用 Agent 工具与协作执行：把计划变成可检查的动作 为什么 ReTool 要同时学习调用、纠错和停止？ 工具可以提高计算或取证能力，也会失败并消耗成本，策略需判断何时调用、如何利用报错修正及何时已有足够答案。仅学会输出工具语法不等于会控制整个推理链，停止过早和重复调用都可能损害任务结果。 例如数学题中先用代码核算，报错后修参数，得到一致结果后停止，而不是一直调用计算器或未经检查直接结束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-retool-db452677" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-da7a79464de2183e">为什么 ReTool 要同时学习调用、纠错和停止？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aretool">ReTool</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具可以提高计算或取证能力，也会失败并消耗成本，策略需判断何时调用、如何利用报错修正及何时已有足够答案。仅学会输出工具语法不等于会控制整个推理链，停止过早和重复调用都可能损害任务结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数学题中先用代码核算，报错后修参数，得到一致结果后停止，而不是一直调用计算器或未经检查直接结束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.11536">原论文</a> · <a href="../../../../agent-research/2504.11536-retool/">实现解读</a> · <a href="#qa-da7a79464de2183e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:retool" data-paper-title="ReTool" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ReTool Agent ByteDance Seed 2025-04-15 策略在自然语言 reasoning 与工具执行之间交替，并由可执行反馈学习调用、纠错和停止。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.0500；方法特有操作有非零 telemetry。  推理中工具调用 Agent 工具与协作执行：把计划变成可检查的动作 工具调用带成本惩罚时，为什么不能简单训练成“尽量不调用工具”？ 策略目标同时包含答案收益，少调用只有在不显著损害结果时才有价值。交替推理与真实执行反馈让模型学习哪些步骤值得外包、失败后如何纠正以及何时停止；若只优化调用数，模型可能用流畅猜测替代必要计算，反而失去工具使用能力。 例如心算两位数可以省调用，但复杂统计应执行代码；一次可靠计算的收益可能远大于为省调用而给出错误答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f341f5ec4e371354">工具调用带成本惩罚时，为什么不能简单训练成“尽量不调用工具”？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aretool">ReTool</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略目标同时包含答案收益，少调用只有在不显著损害结果时才有价值。交替推理与真实执行反馈让模型学习哪些步骤值得外包、失败后如何纠正以及何时停止；若只优化调用数，模型可能用流畅猜测替代必要计算，反而失去工具使用能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如心算两位数可以省调用，但复杂统计应执行代码；一次可靠计算的收益可能远大于为省调用而给出错误答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.11536">原论文</a> · <a href="../../../../agent-research/2504.11536-retool/">实现解读</a> · <a href="#qa-f341f5ec4e371354">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:retool" data-paper-title="ReTool" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ReTool Agent ByteDance Seed 2025-04-15 策略在自然语言 reasoning 与工具执行之间交替，并由可执行反馈学习调用、纠错和停止。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.0500；方法特有操作有非零 telemetry。  推理中工具调用 Agent 工具与协作执行：把计划变成可检查的动作 结果奖励减调用成本与固定每题调用一次有什么取舍？ 固定调用不看题目难度和当前证据，简单题浪费、复杂题不足；成本化回报允许按收益选择次数。惩罚过大也可能压掉必要工具，所以应同时报告答案正确性和完整调用成本，不能用减少次数单独证明方法更好。 例如一道心算题零调用可行，多阶段数值题可能需要两次验证，统一一次并非对两者都合适。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-68920b8b5af8933d">结果奖励减调用成本与固定每题调用一次有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aretool">ReTool</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定调用不看题目难度和当前证据，简单题浪费、复杂题不足；成本化回报允许按收益选择次数。惩罚过大也可能压掉必要工具，所以应同时报告答案正确性和完整调用成本，不能用减少次数单独证明方法更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一道心算题零调用可行，多阶段数值题可能需要两次验证，统一一次并非对两者都合适。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.11536">原论文</a> · <a href="../../../../agent-research/2504.11536-retool/">实现解读</a> · <a href="#qa-68920b8b5af8933d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:retool" data-paper-title="ReTool" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ReTool Agent ByteDance Seed 2025-04-15 策略在自然语言 reasoning 与工具执行之间交替，并由可执行反馈学习调用、纠错和停止。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。PlanBench mini-suite、120 episodes、seed 42：joint success 1.0000，average cost 1.0500；方法特有操作有非零 telemetry。  推理中工具调用 Agent 工具与协作执行：把计划变成可检查的动作 工具 observation 能否由模型自行续写来凑完整 reasoning/action 轨迹？ 不能。执行反馈必须来自实际工具或环境，模型只能生成自己的推理与动作；伪造结果会失去学习调用和纠错的真实依据。本地仅验证受控状态和预算，不含论文模型训练及真实数学 benchmark，代理满分不是原文效果复刻。 例如模型生成“Python 输出 42”但没有运行代码，不能计为工具成功，更不能给该动作真实执行奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-888b668a9e5c1718">工具 observation 能否由模型自行续写来凑完整 reasoning/action 轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aretool">ReTool</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ByteDance Seed</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。执行反馈必须来自实际工具或环境，模型只能生成自己的推理与动作；伪造结果会失去学习调用和纠错的真实依据。本地仅验证受控状态和预算，不含论文模型训练及真实数学 benchmark，代理满分不是原文效果复刻。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型生成“Python 输出 42”但没有运行代码，不能计为工具成功，更不能给该动作真实执行奖励。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.11536">原论文</a> · <a href="../../../../agent-research/2504.11536-retool/">实现解读</a> · <a href="#qa-888b668a9e5c1718">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:openhands" data-paper-title="OpenHands" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="OpenHands Agent All-Hands-AI 2024-07-23 OpenHands 提供开放的软件 Agent 平台，把终端、编辑器、浏览器等动作统一到 event stream，并以 sandbox 隔离执行，覆盖修 bug、写代码和仓库维护。 浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。用编辑器、终端和可观测事件流驱动通用软件开发 Agent。已实现编辑器/终端事件和真实代码 sandbox；浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。本地将 file-editor 与 terminal 动作写入 event stream；terminal 在独立临时目录执行固定回归测试，最终报告动作、编辑 hash、命令输出和 success。  通用软件 Agent Agent 工具与协作执行：把计划变成可检查的动作 OpenHands 为什么把软件 Agent 做成能编辑、执行和浏览的工作平台？ 真实软件任务不止生成代码，还需要查看文件、运行命令、检查页面和接续长过程。OpenHands 提供把这些操作与反馈连接起来的基础设施，让控制策略有一致的工作环境。平台支持接口与具体 Agent 能否完成任务是两层证据，接通工具也不等于所有控制策略可靠。 教学例：修改前端后需启动服务并看页面，再根据报错回到代码；只有代码生成接口无法覆盖这条完整工作链。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-openhands-e21fcd2c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-718d5bd7d13021cc">OpenHands 为什么把软件 Agent 做成能编辑、执行和浏览的工作平台？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aopenhands">OpenHands</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · All-Hands-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实软件任务不止生成代码，还需要查看文件、运行命令、检查页面和接续长过程。OpenHands 提供把这些操作与反馈连接起来的基础设施，让控制策略有一致的工作环境。平台支持接口与具体 Agent 能否完成任务是两层证据，接通工具也不等于所有控制策略可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：修改前端后需启动服务并看页面，再根据报错回到代码；只有代码生成接口无法覆盖这条完整工作链。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16741">原论文</a> · <a href="../../../../agent-research/2407.16741-openhands/">实现解读</a> · <a href="#qa-718d5bd7d13021cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:openhands" data-paper-title="OpenHands" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="OpenHands Agent All-Hands-AI 2024-07-23 OpenHands 提供开放的软件 Agent 平台，把终端、编辑器、浏览器等动作统一到 event stream，并以 sandbox 隔离执行，覆盖修 bug、写代码和仓库维护。 浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。用编辑器、终端和可观测事件流驱动通用软件开发 Agent。已实现编辑器/终端事件和真实代码 sandbox；浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。本地将 file-editor 与 terminal 动作写入 event stream；terminal 在独立临时目录执行固定回归测试，最终报告动作、编辑 hash、命令输出和 success。  通用软件 Agent Agent 工具与协作执行：把计划变成可检查的动作 统一 event stream 为什么有助于把终端、编辑器和浏览器串成可检查的软件工作流？ 每个动作与 sandbox 返回都进入同一时序记录，后续策略可依据真实反馈继续，审阅者也能追踪修改和验证的来源。统一事件不意味着各种工具语义相同，更不等于代码已安全或正确；执行隔离、权限和实际测试仍承担各自职责。 例如编辑事件修改文件，终端事件跑测试，浏览器事件核对页面；统一记录能判断测试究竟发生在修改前还是修改后。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7201d318abb3e27c">统一 event stream 为什么有助于把终端、编辑器和浏览器串成可检查的软件工作流？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aopenhands">OpenHands</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · All-Hands-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个动作与 sandbox 返回都进入同一时序记录，后续策略可依据真实反馈继续，审阅者也能追踪修改和验证的来源。统一事件不意味着各种工具语义相同，更不等于代码已安全或正确；执行隔离、权限和实际测试仍承担各自职责。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如编辑事件修改文件，终端事件跑测试，浏览器事件核对页面；统一记录能判断测试究竟发生在修改前还是修改后。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16741">原论文</a> · <a href="../../../../agent-research/2407.16741-openhands/">实现解读</a> · <a href="#qa-7201d318abb3e27c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:openhands" data-paper-title="OpenHands" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="OpenHands Agent All-Hands-AI 2024-07-23 OpenHands 提供开放的软件 Agent 平台，把终端、编辑器、浏览器等动作统一到 event stream，并以 sandbox 隔离执行，覆盖修 bug、写代码和仓库维护。 浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。用编辑器、终端和可观测事件流驱动通用软件开发 Agent。已实现编辑器/终端事件和真实代码 sandbox；浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。本地将 file-editor 与 terminal 动作写入 event stream；terminal 在独立临时目录执行固定回归测试，最终报告动作、编辑 hash、命令输出和 success。  通用软件 Agent Agent 工具与协作执行：把计划变成可检查的动作 平台 runtime 与具体 Agent controller 为什么不能当同一贡献？ 平台提供动作、观察与隔离接口，controller 决定如何规划和使用这些接口，不同策略可共用平台。运行一段 editor/terminal 链路只验证执行能力，不能自动代表完整 OpenHands 模型推理或官方 SWE-bench resolved rate。 例如同一 sandbox 可以由规则脚本或语言模型控制，二者共享工具却不具有相同 issue 理解与修复能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9579dd55c1112b36">平台 runtime 与具体 Agent controller 为什么不能当同一贡献？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aopenhands">OpenHands</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · All-Hands-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>平台提供动作、观察与隔离接口，controller 决定如何规划和使用这些接口，不同策略可共用平台。运行一段 editor/terminal 链路只验证执行能力，不能自动代表完整 OpenHands 模型推理或官方 SWE-bench resolved rate。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一 sandbox 可以由规则脚本或语言模型控制，二者共享工具却不具有相同 issue 理解与修复能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16741">原论文</a> · <a href="../../../../agent-research/2407.16741-openhands/">实现解读</a> · <a href="#qa-9579dd55c1112b36">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:openhands" data-paper-title="OpenHands" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="OpenHands Agent All-Hands-AI 2024-07-23 OpenHands 提供开放的软件 Agent 平台，把终端、编辑器、浏览器等动作统一到 event stream，并以 sandbox 隔离执行，覆盖修 bug、写代码和仓库维护。 浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。用编辑器、终端和可观测事件流驱动通用软件开发 Agent。已实现编辑器/终端事件和真实代码 sandbox；浏览器动作目前只保留接口语义，尚未连接网页交互环境，也未运行完整 OpenHands controller 与官方 SWE-bench 容器。本地将 file-editor 与 terminal 动作写入 event stream；terminal 在独立临时目录执行固定回归测试，最终报告动作、编辑 hash、命令输出和 success。  通用软件 Agent Agent 工具与协作执行：把计划变成可检查的动作 本地浏览器接口语义是否表示网页交互已经接通？ 没有。本地真实写入 editor 事件并在独立临时目录跑固定回归，浏览器仅保留接口语义，未连接网页环境或完整 controller。应依据实际事件和结果声称验证范围，不能把一个 browser action 类型存在写成真实导航测试通过。 例如日志允许记录 browser_open，不等于已打开页面、获取 DOM 并点击控件；这些交互还需要真实浏览器证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-56484f867d35a859">本地浏览器接口语义是否表示网页交互已经接通？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aopenhands">OpenHands</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · All-Hands-AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地真实写入 editor 事件并在独立临时目录跑固定回归，浏览器仅保留接口语义，未连接网页环境或完整 controller。应依据实际事件和结果声称验证范围，不能把一个 browser action 类型存在写成真实导航测试通过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如日志允许记录 browser_open，不等于已打开页面、获取 DOM 并点击控件；这些交互还需要真实浏览器证据。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2407.16741">原论文</a> · <a href="../../../../agent-research/2407.16741-openhands/">实现解读</a> · <a href="#qa-56484f867d35a859">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:swe-agent" data-paper-title="SWE-agent" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-agent Agent Princeton University 2024-05-06 通用 shell 对 LLM 而言动作空间过宽、输出冗长。SWE-agent 用专门 ACI 约束仓库搜索、文件查看、精确编辑和测试，让模型能围绕 issue 定位故障并验证 patch。 为软件工程 Agent 设计面向仓库浏览、编辑和测试的 Agent-Computer Interface。这是可执行的 SWE-style micro benchmark，不是官方 SWE-bench Lite 数据与 Docker 镜像。名称 swebench-local 明确保留该区别，不能将本地 success 当作论文 resolved rate。本地 ACI 只暴露读文件、写 solution.py 和固定 unittest 命令；每题初始仓库必须先真实失败，Agent 定位、编辑并以退出码验证。  软件工程 ACI Agent 工具与协作执行：把计划变成可检查的动作 修复 GitHub issue 的 Agent 为什么需要一个便于反复查看和修改仓库的接口？ 模型要在未知仓库里定位问题、读取必要上下文、做小改动并验证，原始终端输出可能过长或难以稳定操作。SWE-agent 研究面向这类流程的交互界面，使行动和反馈更适合模型。界面降低操作负担，不替代任务理解与测试，也不能凭命令执行成功认定 issue 已解决。 教学例：查看命中文件后定位相关行再修改，比一次打印整仓库更容易保持上下文；但修改后仍必须检查目标测试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-swe-agent-79904a33" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-260212a2f996528e">修复 GitHub issue 的 Agent 为什么需要一个便于反复查看和修改仓库的接口？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aswe-agent">SWE-agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模型要在未知仓库里定位问题、读取必要上下文、做小改动并验证，原始终端输出可能过长或难以稳定操作。SWE-agent 研究面向这类流程的交互界面，使行动和反馈更适合模型。界面降低操作负担，不替代任务理解与测试，也不能凭命令执行成功认定 issue 已解决。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：查看命中文件后定位相关行再修改，比一次打印整仓库更容易保持上下文；但修改后仍必须检查目标测试。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.15793">原论文</a> · <a href="../../../../agent-research/2405.15793-swe-agent/">实现解读</a> · <a href="#qa-260212a2f996528e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:swe-agent" data-paper-title="SWE-agent" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-agent Agent Princeton University 2024-05-06 通用 shell 对 LLM 而言动作空间过宽、输出冗长。SWE-agent 用专门 ACI 约束仓库搜索、文件查看、精确编辑和测试，让模型能围绕 issue 定位故障并验证 patch。 为软件工程 Agent 设计面向仓库浏览、编辑和测试的 Agent-Computer Interface。这是可执行的 SWE-style micro benchmark，不是官方 SWE-bench Lite 数据与 Docker 镜像。名称 swebench-local 明确保留该区别，不能将本地 success 当作论文 resolved rate。本地 ACI 只暴露读文件、写 solution.py 和固定 unittest 命令；每题初始仓库必须先真实失败，Agent 定位、编辑并以退出码验证。  软件工程 ACI Agent 工具与协作执行：把计划变成可检查的动作 专门 ACI 为什么可能比给模型无限制 shell 更有效？ 动作空间过宽和冗长输出会增加选择与定位负担，专门界面把搜索、查看、精确编辑和测试变成更易理解的操作反馈。改进的是 Agent 与仓库的交互合同，不是给模型偷偷提供正确 patch；界面约束也不能替代真正执行测试与检查任务完成。 例如只展示目标函数附近行并提供精确替换，比把整个文件打印进提示更易定位，但仍要运行回归测试确认修改有效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dafefde79785114c">专门 ACI 为什么可能比给模型无限制 shell 更有效？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aswe-agent">SWE-agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>动作空间过宽和冗长输出会增加选择与定位负担，专门界面把搜索、查看、精确编辑和测试变成更易理解的操作反馈。改进的是 Agent 与仓库的交互合同，不是给模型偷偷提供正确 patch；界面约束也不能替代真正执行测试与检查任务完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只展示目标函数附近行并提供精确替换，比把整个文件打印进提示更易定位，但仍要运行回归测试确认修改有效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.15793">原论文</a> · <a href="../../../../agent-research/2405.15793-swe-agent/">实现解读</a> · <a href="#qa-dafefde79785114c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:swe-agent" data-paper-title="SWE-agent" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-agent Agent Princeton University 2024-05-06 通用 shell 对 LLM 而言动作空间过宽、输出冗长。SWE-agent 用专门 ACI 约束仓库搜索、文件查看、精确编辑和测试，让模型能围绕 issue 定位故障并验证 patch。 为软件工程 Agent 设计面向仓库浏览、编辑和测试的 Agent-Computer Interface。这是可执行的 SWE-style micro benchmark，不是官方 SWE-bench Lite 数据与 Docker 镜像。名称 swebench-local 明确保留该区别，不能将本地 success 当作论文 resolved rate。本地 ACI 只暴露读文件、写 solution.py 和固定 unittest 命令；每题初始仓库必须先真实失败，Agent 定位、编辑并以退出码验证。  软件工程 ACI Agent 工具与协作执行：把计划变成可检查的动作 ACI 与原样暴露 shell 的比较为什么要固定底层模型和任务？ 否则收益可能来自模型更强或任务更简单，而非接口本身。ACI 改变观察与动作边界，评估需控制其他条件并看真实 patch 与测试结果；不能用一次顺利编辑证明所有代码修复能力，或将命令格式正确当 issue 已解决。 例如同一模型面对同一 bug 分别用窄编辑器和原始 shell，才较能观察接口对定位及修改的影响。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-99e902304d6ed5e3">ACI 与原样暴露 shell 的比较为什么要固定底层模型和任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aswe-agent">SWE-agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>否则收益可能来自模型更强或任务更简单，而非接口本身。ACI 改变观察与动作边界，评估需控制其他条件并看真实 patch 与测试结果；不能用一次顺利编辑证明所有代码修复能力，或将命令格式正确当 issue 已解决。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一模型面对同一 bug 分别用窄编辑器和原始 shell，才较能观察接口对定位及修改的影响。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.15793">原论文</a> · <a href="../../../../agent-research/2405.15793-swe-agent/">实现解读</a> · <a href="#qa-99e902304d6ed5e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:swe-agent" data-paper-title="SWE-agent" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SWE-agent Agent Princeton University 2024-05-06 通用 shell 对 LLM 而言动作空间过宽、输出冗长。SWE-agent 用专门 ACI 约束仓库搜索、文件查看、精确编辑和测试，让模型能围绕 issue 定位故障并验证 patch。 为软件工程 Agent 设计面向仓库浏览、编辑和测试的 Agent-Computer Interface。这是可执行的 SWE-style micro benchmark，不是官方 SWE-bench Lite 数据与 Docker 镜像。名称 swebench-local 明确保留该区别，不能将本地 success 当作论文 resolved rate。本地 ACI 只暴露读文件、写 solution.py 和固定 unittest 命令；每题初始仓库必须先真实失败，Agent 定位、编辑并以退出码验证。  软件工程 ACI Agent 工具与协作执行：把计划变成可检查的动作 本地 swebench-local 的初始失败与固定 unittest 各证明什么？ 初始真实失败表明任务确有待修问题，编辑后退出码验证这组回归是否通过；本地只暴露读文件、写 solution.py 与固定测试。它是可执行 micro benchmark，非官方 SWE-bench Lite 容器，测试通过也仅支持当前用例覆盖。 例如把一个算术函数修到固定测试通过，可证明编辑执行链路有效，但不能改称解决真实 GitHub issue 的官方 resolved rate。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-52983128b5e50c57">本地 swebench-local 的初始失败与固定 unittest 各证明什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aswe-agent">SWE-agent</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Princeton University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>初始真实失败表明任务确有待修问题，编辑后退出码验证这组回归是否通过；本地只暴露读文件、写 solution.py 与固定测试。它是可执行 micro benchmark，非官方 SWE-bench Lite 容器，测试通过也仅支持当前用例覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把一个算术函数修到固定测试通过，可证明编辑执行链路有效，但不能改称解决真实 GitHub issue 的官方 resolved rate。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2405.15793">原论文</a> · <a href="../../../../agent-research/2405.15793-swe-agent/">实现解读</a> · <a href="#qa-52983128b5e50c57">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autogen" data-paper-title="AutoGen" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AutoGen Agent Microsoft Research 2023-08-16 复杂应用常需要多个模型、工具和人类协作，手写控制流难复用。AutoGen 提供 ConversableAgent 与 conversation programming：每个角色声明能力、回复策略和终止条件，通过群聊或嵌套会话组合成工作流。 AutoGen 把 Agent 抽象为可对话、可配置的角色，用消息路由和终止条件编排 planner、executor、critic、人类或工具。实现 planner/executor/critic 的消息协议、角色交接与显式终止；未嵌入完整 AutoGen 运行时、容器代码执行或真实 LLM 群聊，1.0 是确定性控制流测试而非论文应用得分。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.0000，记录 120 份 plan、360 条跨角色消息和 120 次 critic round。  多 Agent Agent 工具与协作执行：把计划变成可检查的动作 AutoGen 为什么把多 Agent 应用组织成可编程对话？ 复杂任务可能需要模型、代码执行器和人协作，固定一轮问答难以表达反馈后的继续工作。AutoGen 用可配置角色和消息交互组织这些参与者，使工具结果或回复触发后续步骤。角色名称不等于协作能力，还要定义谁回复、何时转交和何时停止，并核验实际产物。 教学例：助手提出代码，执行器返回报错，助手据此修改；这个交互应由明确协议控制，而不是让两个人设无限闲聊。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-autogen-60994f2d" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-520344c861492850">AutoGen 为什么把多 Agent 应用组织成可编程对话？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautogen">AutoGen</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>复杂任务可能需要模型、代码执行器和人协作，固定一轮问答难以表达反馈后的继续工作。AutoGen 用可配置角色和消息交互组织这些参与者，使工具结果或回复触发后续步骤。角色名称不等于协作能力，还要定义谁回复、何时转交和何时停止，并核验实际产物。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：助手提出代码，执行器返回报错，助手据此修改；这个交互应由明确协议控制，而不是让两个人设无限闲聊。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.08155">原论文</a> · <a href="../../../../agent-research/2308.08155-autogen/">实现解读</a> · <a href="#qa-520344c861492850">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autogen" data-paper-title="AutoGen" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AutoGen Agent Microsoft Research 2023-08-16 复杂应用常需要多个模型、工具和人类协作，手写控制流难复用。AutoGen 提供 ConversableAgent 与 conversation programming：每个角色声明能力、回复策略和终止条件，通过群聊或嵌套会话组合成工作流。 AutoGen 把 Agent 抽象为可对话、可配置的角色，用消息路由和终止条件编排 planner、executor、critic、人类或工具。实现 planner/executor/critic 的消息协议、角色交接与显式终止；未嵌入完整 AutoGen 运行时、容器代码执行或真实 LLM 群聊，1.0 是确定性控制流测试而非论文应用得分。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.0000，记录 120 份 plan、360 条跨角色消息和 120 次 critic round。  多 Agent Agent 工具与协作执行：把计划变成可检查的动作 对话编程为什么需要显式终止条件，而不能让多个角色一直互相回复？ 消息本身可以不断触发新回复，若没有角色职责、工具边界和停止规则，协作容易重复或形成循环。conversation programming 把这些规则变成可组合控制流，适合群聊与嵌套会话；角色数量增加并不保证分工正确，最终仍需可验证产物判断完成。 例如写作者与审查者每轮都说“再优化一下”会无限往返；约定验证通过或预算耗尽时结束，才能形成可控工作流。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-47f466dc66f53411">对话编程为什么需要显式终止条件，而不能让多个角色一直互相回复？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautogen">AutoGen</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>消息本身可以不断触发新回复，若没有角色职责、工具边界和停止规则，协作容易重复或形成循环。conversation programming 把这些规则变成可组合控制流，适合群聊与嵌套会话；角色数量增加并不保证分工正确，最终仍需可验证产物判断完成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如写作者与审查者每轮都说“再优化一下”会无限往返；约定验证通过或预算耗尽时结束，才能形成可控工作流。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.08155">原论文</a> · <a href="../../../../agent-research/2308.08155-autogen/">实现解读</a> · <a href="#qa-47f466dc66f53411">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autogen" data-paper-title="AutoGen" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AutoGen Agent Microsoft Research 2023-08-16 复杂应用常需要多个模型、工具和人类协作，手写控制流难复用。AutoGen 提供 ConversableAgent 与 conversation programming：每个角色声明能力、回复策略和终止条件，通过群聊或嵌套会话组合成工作流。 AutoGen 把 Agent 抽象为可对话、可配置的角色，用消息路由和终止条件编排 planner、executor、critic、人类或工具。实现 planner/executor/critic 的消息协议、角色交接与显式终止；未嵌入完整 AutoGen 运行时、容器代码执行或真实 LLM 群聊，1.0 是确定性控制流测试而非论文应用得分。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.0000，记录 120 份 plan、360 条跨角色消息和 120 次 critic round。  多 Agent Agent 工具与协作执行：把计划变成可检查的动作 消息驱动编排与一个固定线性脚本有什么差别？ 线性脚本预设唯一顺序，消息策略可按内容或状态选择接收者、嵌套会话和结束，使工具与人类协作更灵活。灵活也可能带来无效对话和循环，不能以消息数更多或角色更多证明任务质量提升，成本需全计。 例如审核失败可以触发一次嵌套修复对话，成功则直接结束，而不是无论结果都走完相同五轮聊天。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8669aba9d7a12d1d">消息驱动编排与一个固定线性脚本有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautogen">AutoGen</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>线性脚本预设唯一顺序，消息策略可按内容或状态选择接收者、嵌套会话和结束，使工具与人类协作更灵活。灵活也可能带来无效对话和循环，不能以消息数更多或角色更多证明任务质量提升，成本需全计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如审核失败可以触发一次嵌套修复对话，成功则直接结束，而不是无论结果都走完相同五轮聊天。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.08155">原论文</a> · <a href="../../../../agent-research/2308.08155-autogen/">实现解读</a> · <a href="#qa-8669aba9d7a12d1d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autogen" data-paper-title="AutoGen" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="AutoGen Agent Microsoft Research 2023-08-16 复杂应用常需要多个模型、工具和人类协作，手写控制流难复用。AutoGen 提供 ConversableAgent 与 conversation programming：每个角色声明能力、回复策略和终止条件，通过群聊或嵌套会话组合成工作流。 AutoGen 把 Agent 抽象为可对话、可配置的角色，用消息路由和终止条件编排 planner、executor、critic、人类或工具。实现 planner/executor/critic 的消息协议、角色交接与显式终止；未嵌入完整 AutoGen 运行时、容器代码执行或真实 LLM 群聊，1.0 是确定性控制流测试而非论文应用得分。PlanBench mini 固定 120 episodes：joint success 1.0000、平均成本 3.0000，记录 120 份 plan、360 条跨角色消息和 120 次 critic round。  多 Agent Agent 工具与协作执行：把计划变成可检查的动作 本地 planner/executor/critic 协议是否运行完整 AutoGen runtime？ 没有。本地实现角色交接、消息记录与显式终止的确定性控制流，未嵌入完整 runtime、真实 LLM 群聊或容器代码执行。plan 与 critic round 数量可检查流程，但其满分不能作为原文多应用能力或开发效率指标。 例如三角色按规则各发一条消息可以通过协议测试，没有模型理解与真实工具执行时不能称完成开放软件任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9d058576a8a28231">本地 planner/executor/critic 协议是否运行完整 AutoGen runtime？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautogen">AutoGen</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地实现角色交接、消息记录与显式终止的确定性控制流，未嵌入完整 runtime、真实 LLM 群聊或容器代码执行。plan 与 critic round 数量可检查流程，但其满分不能作为原文多应用能力或开发效率指标。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三角色按规则各发一条消息可以通过协议测试，没有模型理解与真实工具执行时不能称完成开放软件任务。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.08155">原论文</a> · <a href="../../../../agent-research/2308.08155-autogen/">实现解读</a> · <a href="#qa-9d058576a8a28231">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:metagpt" data-paper-title="MetaGPT" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MetaGPT Agent DeepWisdom 2023-08-01 简单串联多个聊天 Agent 容易让幻觉级联。MetaGPT 把人类软件团队的 SOP 编码成角色化消息流程，每个角色生产结构化中间物，由下游角色消费和验证。 用标准作业流程（SOP）把软件需求依次交给产品、架构、工程和测试角色。保留 SOP、角色交付物、真实编辑与测试；本地不是完整 MetaGPT LLM 对话，也不是官方 SWE-bench Lite，fixture 仅验证执行链路和可审计 trace。每个 episode 创建真实临时 Python 仓库；四个角色留下结构化 artifact，工程角色修改文件，QA 角色通过固定 python -m unittest -q 执行回归测试。  多 Agent 软件工程 Agent 工具与协作执行：把计划变成可检查的动作 MetaGPT 为什么借用软件团队的角色和交付物来组织多 Agent 工作？ 软件开发包含需求、设计、实现和测试，相互依赖的信息若只靠自由聊天传递容易失真。MetaGPT 把流程职责和中间交付物显式化，让下一角色有可检查输入。分工有助于组织工作，但文档齐全不等于代码正确，最终仍需执行与验证。 教学例：架构师给出接口定义，工程师据此实现，测试者检查约定；若接口只散在聊天里，不同角色可能各自理解成不同参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-metagpt-ffaa73e8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-843bb845fe7721da">MetaGPT 为什么借用软件团队的角色和交付物来组织多 Agent 工作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ametagpt">MetaGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepWisdom</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>软件开发包含需求、设计、实现和测试，相互依赖的信息若只靠自由聊天传递容易失真。MetaGPT 把流程职责和中间交付物显式化，让下一角色有可检查输入。分工有助于组织工作，但文档齐全不等于代码正确，最终仍需执行与验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：架构师给出接口定义，工程师据此实现，测试者检查约定；若接口只散在聊天里，不同角色可能各自理解成不同参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.00352">原论文</a> · <a href="../../../../agent-research/2308.00352-metagpt/">实现解读</a> · <a href="#qa-843bb845fe7721da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:metagpt" data-paper-title="MetaGPT" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MetaGPT Agent DeepWisdom 2023-08-01 简单串联多个聊天 Agent 容易让幻觉级联。MetaGPT 把人类软件团队的 SOP 编码成角色化消息流程，每个角色生产结构化中间物，由下游角色消费和验证。 用标准作业流程（SOP）把软件需求依次交给产品、架构、工程和测试角色。保留 SOP、角色交付物、真实编辑与测试；本地不是完整 MetaGPT LLM 对话，也不是官方 SWE-bench Lite，fixture 仅验证执行链路和可审计 trace。每个 episode 创建真实临时 Python 仓库；四个角色留下结构化 artifact，工程角色修改文件，QA 角色通过固定 python -m unittest -q 执行回归测试。  多 Agent 软件工程 Agent 工具与协作执行：把计划变成可检查的动作 结构化中间物为什么比角色间自由聊天更能抑制软件工作流的幻觉级联？ 下游依赖清晰的需求、设计和测试合同，能检查上游是否提供必要字段与约束，而不只接收自然语言承诺。SOP 规定角色顺序和消费关系，使错误更易定位；结构化不等于内容正确，仍需要下游验证与真实执行，不能把格式齐全当成可用软件。 例如架构师输出明确接口，工程师才能核对实现签名；若只收到“系统设计好了”，后续各角色可能各自想象不同约定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-03055a1e793d577f">结构化中间物为什么比角色间自由聊天更能抑制软件工作流的幻觉级联？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ametagpt">MetaGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepWisdom</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>下游依赖清晰的需求、设计和测试合同，能检查上游是否提供必要字段与约束，而不只接收自然语言承诺。SOP 规定角色顺序和消费关系，使错误更易定位；结构化不等于内容正确，仍需要下游验证与真实执行，不能把格式齐全当成可用软件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如架构师输出明确接口，工程师才能核对实现签名；若只收到“系统设计好了”，后续各角色可能各自想象不同约定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.00352">原论文</a> · <a href="../../../../agent-research/2308.00352-metagpt/">实现解读</a> · <a href="#qa-03055a1e793d577f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:metagpt" data-paper-title="MetaGPT" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MetaGPT Agent DeepWisdom 2023-08-01 简单串联多个聊天 Agent 容易让幻觉级联。MetaGPT 把人类软件团队的 SOP 编码成角色化消息流程，每个角色生产结构化中间物，由下游角色消费和验证。 用标准作业流程（SOP）把软件需求依次交给产品、架构、工程和测试角色。保留 SOP、角色交付物、真实编辑与测试；本地不是完整 MetaGPT LLM 对话，也不是官方 SWE-bench Lite，fixture 仅验证执行链路和可审计 trace。每个 episode 创建真实临时 Python 仓库；四个角色留下结构化 artifact，工程角色修改文件，QA 角色通过固定 python -m unittest -q 执行回归测试。  多 Agent 软件工程 Agent 工具与协作执行：把计划变成可检查的动作 角色按 PM、Architect、Engineer、QA 分工与简单多次自我复述有什么不同？ 分工给每阶段不同输入输出责任，需求、设计、实现与验证是不同工件，而非同一答案换措辞重复。收益来自合同和反馈闭环，角色标签本身不会自动产生独立审查；若所有阶段共享错误假设，仍会一起失效。 例如 QA 应执行测试检查代码，而不是只把工程师的“看起来正确”再说一次，才能形成实际验证环节。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f75b36d8fc81d025">角色按 PM、Architect、Engineer、QA 分工与简单多次自我复述有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ametagpt">MetaGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepWisdom</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>分工给每阶段不同输入输出责任，需求、设计、实现与验证是不同工件，而非同一答案换措辞重复。收益来自合同和反馈闭环，角色标签本身不会自动产生独立审查；若所有阶段共享错误假设，仍会一起失效。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 QA 应执行测试检查代码，而不是只把工程师的“看起来正确”再说一次，才能形成实际验证环节。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.00352">原论文</a> · <a href="../../../../agent-research/2308.00352-metagpt/">实现解读</a> · <a href="#qa-f75b36d8fc81d025">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:metagpt" data-paper-title="MetaGPT" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MetaGPT Agent DeepWisdom 2023-08-01 简单串联多个聊天 Agent 容易让幻觉级联。MetaGPT 把人类软件团队的 SOP 编码成角色化消息流程，每个角色生产结构化中间物，由下游角色消费和验证。 用标准作业流程（SOP）把软件需求依次交给产品、架构、工程和测试角色。保留 SOP、角色交付物、真实编辑与测试；本地不是完整 MetaGPT LLM 对话，也不是官方 SWE-bench Lite，fixture 仅验证执行链路和可审计 trace。每个 episode 创建真实临时 Python 仓库；四个角色留下结构化 artifact，工程角色修改文件，QA 角色通过固定 python -m unittest -q 执行回归测试。  多 Agent 软件工程 Agent 工具与协作执行：把计划变成可检查的动作 本地真实临时仓库测试与完整 MetaGPT LLM 团队有哪些差距？ 本地四角色留下结构化 artifact，工程阶段确实编辑 Python 文件，QA 运行固定 unittest；但没有完整 LLM 多 Agent 对话或官方 SWE-bench。它支持可审计执行链路，不支持把 fixture 成功率等同 HumanEval、MBPP 或真实团队软件交付。 例如测试输出与编辑 hash 可验证这次文件确实被修改和执行，不能由此假设角色会为未知需求自主设计正确架构。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ad3ab6d711ba69e5">本地真实临时仓库测试与完整 MetaGPT LLM 团队有哪些差距？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ametagpt">MetaGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · DeepWisdom</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地四角色留下结构化 artifact，工程阶段确实编辑 Python 文件，QA 运行固定 unittest；但没有完整 LLM 多 Agent 对话或官方 SWE-bench。它支持可审计执行链路，不支持把 fixture 成功率等同 HumanEval、MBPP 或真实团队软件交付。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如测试输出与编辑 hash 可验证这次文件确实被修改和执行，不能由此假设角色会为未知需求自主设计正确架构。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2308.00352">原论文</a> · <a href="../../../../agent-research/2308.00352-metagpt/">实现解读</a> · <a href="#qa-ad3ab6d711ba69e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolbench" data-paper-title="ToolBench" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolBench Agent Tsinghua University 2023-05-25 分析开源 LLM 工具失败后，组合程序化使用样例、system prompt、in-context demonstration retriever 与生成格式约束。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.8400。  工具指令与评测 Agent 工具与协作执行：把计划变成可检查的动作 ToolBench 为什么研究让语言模型学习多种工具，而不是为每个任务单独手写调用程序？ 真实工具目录包含不同接口和参数，模型需要理解任务、找到相关示例并产出可执行调用。ToolBench 研究数据、示例使用与调用约束如何支持这种通用工具使用。学会输出格式只是一个环节，接口行为、执行返回和最终答案都要验证，不能把合成样例通过当成真实 API 能力。 教学例：同样是查资料，天气和地图接口要求不同字段；模型应根据工具说明组织参数，而不是把一个固定模板套到全部服务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-toolbench-89c52f4b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-2a0f6c07e30bff56">ToolBench 为什么研究让语言模型学习多种工具，而不是为每个任务单独手写调用程序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolbench">ToolBench</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真实工具目录包含不同接口和参数，模型需要理解任务、找到相关示例并产出可执行调用。ToolBench 研究数据、示例使用与调用约束如何支持这种通用工具使用。学会输出格式只是一个环节，接口行为、执行返回和最终答案都要验证，不能把合成样例通过当成真实 API 能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：同样是查资料，天气和地图接口要求不同字段；模型应根据工具说明组织参数，而不是把一个固定模板套到全部服务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16504">原论文</a> · <a href="../../../../agent-research/2305.16504-toolbench/">实现解读</a> · <a href="#qa-2a0f6c07e30bff56">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolbench" data-paper-title="ToolBench" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolBench Agent Tsinghua University 2023-05-25 分析开源 LLM 工具失败后，组合程序化使用样例、system prompt、in-context demonstration retriever 与生成格式约束。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.8400。  工具指令与评测 Agent 工具与协作执行：把计划变成可检查的动作 为什么检索调用示例之外，还需要格式约束和真实执行检查？ 示例帮助模型理解何时以及怎样用工具，却不保证新调用满足 schema 或参数语义。格式约束控制可解析性，执行结果再检查调用是否实现目标；三者分别补充经验、合同与环境反馈，不能用一个看起来像 JSON 的字符串替代真实工具能力。 例如模型检索到天气 API 示例后生成字段齐全的调用，城市参数却写错；JSON 合法仍不代表查到了用户所需城市的天气。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-effa1825464a63ea">为什么检索调用示例之外，还需要格式约束和真实执行检查？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolbench">ToolBench</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>示例帮助模型理解何时以及怎样用工具，却不保证新调用满足 schema 或参数语义。格式约束控制可解析性，执行结果再检查调用是否实现目标；三者分别补充经验、合同与环境反馈，不能用一个看起来像 JSON 的字符串替代真实工具能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型检索到天气 API 示例后生成字段齐全的调用，城市参数却写错；JSON 合法仍不代表查到了用户所需城市的天气。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16504">原论文</a> · <a href="../../../../agent-research/2305.16504-toolbench/">实现解读</a> · <a href="#qa-effa1825464a63ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolbench" data-paper-title="ToolBench" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolBench Agent Tsinghua University 2023-05-25 分析开源 LLM 工具失败后，组合程序化使用样例、system prompt、in-context demonstration retriever 与生成格式约束。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.8400。  工具指令与评测 Agent 工具与协作执行：把计划变成可检查的动作 in-context demonstration retriever 与固定放同一组示例有什么差别？ 检索按当前任务选择相关使用示范，固定示例可能覆盖有限且占用无关上下文。检索也可能选错或让模型照搬旧参数，因此只能复用方法，不能把示范答案当当前输出；比较应固定模型和任务而计入示例读取成本。 例如查询数据库时取 SQL 工具示例比天气样例更有用，但示例中的表名不能未经核对直接用于新库。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1f0d05b126401e20">in-context demonstration retriever 与固定放同一组示例有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolbench">ToolBench</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>检索按当前任务选择相关使用示范，固定示例可能覆盖有限且占用无关上下文。检索也可能选错或让模型照搬旧参数，因此只能复用方法，不能把示范答案当当前输出；比较应固定模型和任务而计入示例读取成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如查询数据库时取 SQL 工具示例比天气样例更有用，但示例中的表名不能未经核对直接用于新库。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16504">原论文</a> · <a href="../../../../agent-research/2305.16504-toolbench/">实现解读</a> · <a href="#qa-1f0d05b126401e20">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolbench" data-paper-title="ToolBench" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ToolBench Agent Tsinghua University 2023-05-25 分析开源 LLM 工具失败后，组合程序化使用样例、system prompt、in-context demonstration retriever 与生成格式约束。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 0.8400。  工具指令与评测 Agent 工具与协作执行：把计划变成可检查的动作 本地 planbench-mini 的工具成功能否等同论文八任务或真实 API 成功率？ 不能。本条本地只验证示例、约束或状态协议的特定机制，没有原文大模型、真实完整工具矩阵或训练。工具返回与最终评分需来自独立执行，受控任务满分不等于公开 benchmark，更不能因同名 ToolBench 混入另一数据集协议。 例如预设计划经过解析器成功执行，证明当前接口可用，不说明模型已能面对未知服务文档自动产生正确调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9b063717d0acaa6b">本地 planbench-mini 的工具成功能否等同论文八任务或真实 API 成功率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolbench">ToolBench</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本条本地只验证示例、约束或状态协议的特定机制，没有原文大模型、真实完整工具矩阵或训练。工具返回与最终评分需来自独立执行，受控任务满分不等于公开 benchmark，更不能因同名 ToolBench 混入另一数据集协议。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预设计划经过解析器成功执行，证明当前接口可用，不说明模型已能面对未知服务文档自动产生正确调用。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.16504">原论文</a> · <a href="../../../../agent-research/2305.16504-toolbench/">实现解读</a> · <a href="#qa-9b063717d0acaa6b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:critic" data-paper-title="CRITIC" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CRITIC Agent Microsoft 2023-05-19 仅让 LLM 反思自己的文本可能重复同一错误。CRITIC 调用搜索、代码解释器等外部工具，把可观测反馈带回修订循环，使 critique 有环境证据。 让 Agent 用外部工具验证初稿，再依据真实反馈自我修正。外部反馈和迭代改码是真实执行的；反馈源仅为受控代码测试，没有搜索引擎、toxicity classifier 或通用 LLM critic。Agent 先写入一个有缺陷 patch，真实运行 unittest 获取 traceback，再根据反馈写入正确 patch 并复测；报告记录每轮编辑、命令、退出码和输出。  工具反馈 Agent 工具与协作执行：把计划变成可检查的动作 CRITIC 为什么关心模型已经写完答案后，仍能发现并修正错误？ 初稿可能在事实、推理或代码上出错，模型对自身输出的信心又不一定可靠。CRITIC 研究让模型主动借助外部工具获取检查信号，再据此批评和修订。它把可观察证据引入改稿过程，但检查工具覆盖有限，迭代也可能引入新错，需要分别评估检查与最终结果。 教学例：模型写出一段计算代码后，运行发现边界输入异常，再修改逻辑；仅重读自己“应该正确”的解释不提供同等观察。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-critic-11dab3d3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bafd7c35b893a5b8">CRITIC 为什么关心模型已经写完答案后，仍能发现并修正错误？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acritic">CRITIC</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>初稿可能在事实、推理或代码上出错，模型对自身输出的信心又不一定可靠。CRITIC 研究让模型主动借助外部工具获取检查信号，再据此批评和修订。它把可观察证据引入改稿过程，但检查工具覆盖有限，迭代也可能引入新错，需要分别评估检查与最终结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：模型写出一段计算代码后，运行发现边界输入异常，再修改逻辑；仅重读自己“应该正确”的解释不提供同等观察。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.11738">原论文</a> · <a href="../../../../agent-research/2305.11738-critic/">实现解读</a> · <a href="#qa-bafd7c35b893a5b8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:critic" data-paper-title="CRITIC" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CRITIC Agent Microsoft 2023-05-19 仅让 LLM 反思自己的文本可能重复同一错误。CRITIC 调用搜索、代码解释器等外部工具，把可观测反馈带回修订循环，使 critique 有环境证据。 让 Agent 用外部工具验证初稿，再依据真实反馈自我修正。外部反馈和迭代改码是真实执行的；反馈源仅为受控代码测试，没有搜索引擎、toxicity classifier 或通用 LLM critic。Agent 先写入一个有缺陷 patch，真实运行 unittest 获取 traceback，再根据反馈写入正确 patch 并复测；报告记录每轮编辑、命令、退出码和输出。  工具反馈 Agent 工具与协作执行：把计划变成可检查的动作 为什么外部工具反馈比模型只重读自己的答案更可能发现重复性错误？ 同一模型的自我批评可能沿用原先错误假设，工具提供独立可观察约束，例如搜索事实或代码执行结果。修订围绕这些证据改变答案，形成闭环；工具也可能失败或无结果，不能把没有反馈当成已验证正确，更不能伪造成功检查。 例如答案算错乘积，模型重读仍觉得合理，实际运行计算器会给出不同数值，修订才能针对明确矛盾而非泛泛反思。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1766e55c41f638fd">为什么外部工具反馈比模型只重读自己的答案更可能发现重复性错误？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acritic">CRITIC</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一模型的自我批评可能沿用原先错误假设，工具提供独立可观察约束，例如搜索事实或代码执行结果。修订围绕这些证据改变答案，形成闭环；工具也可能失败或无结果，不能把没有反馈当成已验证正确，更不能伪造成功检查。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如答案算错乘积，模型重读仍觉得合理，实际运行计算器会给出不同数值，修订才能针对明确矛盾而非泛泛反思。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.11738">原论文</a> · <a href="../../../../agent-research/2305.11738-critic/">实现解读</a> · <a href="#qa-1766e55c41f638fd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:critic" data-paper-title="CRITIC" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CRITIC Agent Microsoft 2023-05-19 仅让 LLM 反思自己的文本可能重复同一错误。CRITIC 调用搜索、代码解释器等外部工具，把可观测反馈带回修订循环，使 critique 有环境证据。 让 Agent 用外部工具验证初稿，再依据真实反馈自我修正。外部反馈和迭代改码是真实执行的；反馈源仅为受控代码测试，没有搜索引擎、toxicity classifier 或通用 LLM critic。Agent 先写入一个有缺陷 patch，真实运行 unittest 获取 traceback，再根据反馈写入正确 patch 并复测；报告记录每轮编辑、命令、退出码和输出。  工具反馈 Agent 工具与协作执行：把计划变成可检查的动作 代码执行反馈与网页检索反馈，对 critique 提供的证据有什么不同？ 执行可直接暴露某个输入下的输出或异常，约束的是该次运行行为；网页检索提供外部文本，需要再检查来源与结论是否相符。两者都扩展了模型自评，但可信边界不同：测试未覆盖的代码仍可能有错，检索命中也不等于网页内容必然支持当前答案。 教学例：除零异常能直接指出一次运行失败；搜到同主题网页则还要读具体段落，不能仅靠搜索标题判定原回答正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4d28a5a81f959747">代码执行反馈与网页检索反馈，对 critique 提供的证据有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acritic">CRITIC</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>执行可直接暴露某个输入下的输出或异常，约束的是该次运行行为；网页检索提供外部文本，需要再检查来源与结论是否相符。两者都扩展了模型自评，但可信边界不同：测试未覆盖的代码仍可能有错，检索命中也不等于网页内容必然支持当前答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：除零异常能直接指出一次运行失败；搜到同主题网页则还要读具体段落，不能仅靠搜索标题判定原回答正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.11738">原论文</a> · <a href="../../../../agent-research/2305.11738-critic/">实现解读</a> · <a href="#qa-4d28a5a81f959747">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:critic" data-paper-title="CRITIC" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CRITIC Agent Microsoft 2023-05-19 仅让 LLM 反思自己的文本可能重复同一错误。CRITIC 调用搜索、代码解释器等外部工具，把可观测反馈带回修订循环，使 critique 有环境证据。 让 Agent 用外部工具验证初稿，再依据真实反馈自我修正。外部反馈和迭代改码是真实执行的；反馈源仅为受控代码测试，没有搜索引擎、toxicity classifier 或通用 LLM critic。Agent 先写入一个有缺陷 patch，真实运行 unittest 获取 traceback，再根据反馈写入正确 patch 并复测；报告记录每轮编辑、命令、退出码和输出。  工具反馈 Agent 工具与协作执行：把计划变成可检查的动作 本地真实 traceback 循环具体覆盖了哪种反馈？ 本地先写缺陷 patch、真实运行 unittest，再依据反馈编辑并复测，记录每轮命令和退出码。覆盖的是受控代码反馈与迭代，未接搜索引擎、toxicity classifier 或通用 LLM critic；不能把真实测试执行扩大为全部论文任务已验证。 例如两轮 patch 由测试失败转通过，能证明这一代码实例被修正；它不提供论文开放域问答准确率或无害性结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-72d92522b177ffce">本地真实 traceback 循环具体覆盖了哪种反馈？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acritic">CRITIC</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地先写缺陷 patch、真实运行 unittest，再依据反馈编辑并复测，记录每轮命令和退出码。覆盖的是受控代码反馈与迭代，未接搜索引擎、toxicity classifier 或通用 LLM critic；不能把真实测试执行扩大为全部论文任务已验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两轮 patch 由测试失败转通过，能证明这一代码实例被修正；它不提供论文开放域问答准确率或无害性结果。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.11738">原论文</a> · <a href="../../../../agent-research/2305.11738-critic/">实现解读</a> · <a href="#qa-72d92522b177ffce">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:camel" data-paper-title="CAMEL" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAMEL Agent King Abdullah University of Science and Technology 2023-03-31 用 inception prompting 固定 user/assistant 的角色、目标和边界，通过轮流消息完成任务并生成可研究的多 Agent 社会轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.3500。  多 Agent 协作 Agent 工具与协作执行：把计划变成可检查的动作 CAMEL 为什么用角色合作研究任务完成，而不只研究单模型的一次回答？ 一些任务需要持续提出要求、执行和反馈，两个角色的交互可形成比单次输出更长的协作过程。CAMEL 用明确任务和角色约束研究这种合作及其生成数据。对话长度或角色分工本身不证明解决质量，角色也可能误解目标、重复交流或偏离任务，因此仍需检查结果。 教学例：一个角色提出数据分析需求，另一个逐步实现并接受反馈；若二者都只复述需求，多轮交流并没有真正完成分析。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-camel-640cbec7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-707d4c87b3c8e6c6">CAMEL 为什么用角色合作研究任务完成，而不只研究单模型的一次回答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acamel">CAMEL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · King Abdullah University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一些任务需要持续提出要求、执行和反馈，两个角色的交互可形成比单次输出更长的协作过程。CAMEL 用明确任务和角色约束研究这种合作及其生成数据。对话长度或角色分工本身不证明解决质量，角色也可能误解目标、重复交流或偏离任务，因此仍需检查结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：一个角色提出数据分析需求，另一个逐步实现并接受反馈；若二者都只复述需求，多轮交流并没有真正完成分析。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17760">原论文</a> · <a href="../../../../agent-research/2303.17760-camel/">实现解读</a> · <a href="#qa-707d4c87b3c8e6c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:camel" data-paper-title="CAMEL" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAMEL Agent King Abdullah University of Science and Technology 2023-03-31 用 inception prompting 固定 user/assistant 的角色、目标和边界，通过轮流消息完成任务并生成可研究的多 Agent 社会轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.3500。  多 Agent 协作 Agent 工具与协作执行：把计划变成可检查的动作 inception prompting 固定角色、目标和边界，为什么不仅是给两个模型起名字？ 角色提示影响双方职责、可提出的请求及如何配合，轮流消息在这些约束下推进共同任务。若只换名称却没有能力与边界差异，可能得到两段重复回答而非协作；社会轨迹的存在也不是目标已达成的证据，需要另行检查任务产物。 例如一方提出实现需求、另一方负责写方案，并约定不能更改总目标；若两者都只夸赞对方，聊天很长也没有工作推进。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-03d873922f3e2ffc">inception prompting 固定角色、目标和边界，为什么不仅是给两个模型起名字？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acamel">CAMEL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · King Abdullah University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>角色提示影响双方职责、可提出的请求及如何配合，轮流消息在这些约束下推进共同任务。若只换名称却没有能力与边界差异，可能得到两段重复回答而非协作；社会轨迹的存在也不是目标已达成的证据，需要另行检查任务产物。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一方提出实现需求、另一方负责写方案，并约定不能更改总目标；若两者都只夸赞对方，聊天很长也没有工作推进。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17760">原论文</a> · <a href="../../../../agent-research/2303.17760-camel/">实现解读</a> · <a href="#qa-03d873922f3e2ffc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:camel" data-paper-title="CAMEL" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAMEL Agent King Abdullah University of Science and Technology 2023-03-31 用 inception prompting 固定 user/assistant 的角色、目标和边界，通过轮流消息完成任务并生成可研究的多 Agent 社会轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.3500。  多 Agent 协作 Agent 工具与协作执行：把计划变成可检查的动作 轮流双角色合作与单模型一次输出完整解法有什么取舍？ 对话可以逐步澄清和分担推理，也增加轮数、通信和错误传播机会。多个角色若共享同样偏差，不能靠互相赞同形成独立验证；评价应看真实任务和总成本，而非社会化消息看起来是否自然。 例如执行角色提出缺少输入，需求角色可补澄清；若两者都误读目标，轮流聊天只会扩展同一个错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-8dda7e7980ef7bf0">轮流双角色合作与单模型一次输出完整解法有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acamel">CAMEL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · King Abdullah University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>对话可以逐步澄清和分担推理，也增加轮数、通信和错误传播机会。多个角色若共享同样偏差，不能靠互相赞同形成独立验证；评价应看真实任务和总成本，而非社会化消息看起来是否自然。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如执行角色提出缺少输入，需求角色可补澄清；若两者都误读目标，轮流聊天只会扩展同一个错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17760">原论文</a> · <a href="../../../../agent-research/2303.17760-camel/">实现解读</a> · <a href="#qa-8dda7e7980ef7bf0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:camel" data-paper-title="CAMEL" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="CAMEL Agent King Abdullah University of Science and Technology 2023-03-31 用 inception prompting 固定 user/assistant 的角色、目标和边界，通过轮流消息完成任务并生成可研究的多 Agent 社会轨迹。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。planbench-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.3500。  多 Agent 协作 Agent 工具与协作执行：把计划变成可检查的动作 本地合作状态机与原文多 Agent instruction-following 研究的范围相同吗？ 不同。本地只验证角色化消息、状态更新和预算协议，没有完整大模型社会轨迹或原文 benchmark。固定程序输出角色台词可测试交接，但不能当真实自主合作行为，更不能据受控满分宣称多个 Agent 可靠完成开放任务。 例如脚本交替发两条模板消息说明轮流规则运行；它没有验证模型会在未知任务里保持角色和目标边界。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1991aa1d4d0cf319">本地合作状态机与原文多 Agent instruction-following 研究的范围相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acamel">CAMEL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · King Abdullah University of Science and Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同。本地只验证角色化消息、状态更新和预算协议，没有完整大模型社会轨迹或原文 benchmark。固定程序输出角色台词可测试交接，但不能当真实自主合作行为，更不能据受控满分宣称多个 Agent 可靠完成开放任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如脚本交替发两条模板消息说明轮流规则运行；它没有验证模型会在未知任务里保持角色和目标边界。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17760">原论文</a> · <a href="../../../../agent-research/2303.17760-camel/">实现解读</a> · <a href="#qa-1991aa1d4d0cf319">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hugginggpt" data-paper-title="HuggingGPT" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="HuggingGPT Agent Zhejiang University 2023-03-30 单个 LLM 难以覆盖视觉、语音和其他专业任务，而模型社区已有大量专家。HuggingGPT 让 ChatGPT 充当控制器：先把请求拆成带依赖的子任务，再按 Hugging Face 模型描述匹配专家，按拓扑顺序执行，最后把多模型输出组织为用户答案。 本页实现 task planning、按能力描述选择模型、依赖图执行和最终汇总四阶段。复现控制流、能力匹配和依赖执行；没有下载数百个 Hugging Face 模型，也未调用 ChatGPT。mini-suite 的 1.0 表示编排一致，不代表论文跨模态能力。PlanBench mini 120 episodes、seed 42；工具描述充当本地模型 capability registry，每个子任务保留 dependency edge 后执行。  专家模型编排 Agent 工具与协作执行：把计划变成可检查的动作 HuggingGPT 为什么把专家模型描述当可匹配的能力目录？ 控制器不必自己掌握所有视觉和语音能力，而是将子任务需求与模型卡描述匹配，再调用相应专家。描述提供选择线索而非能力保证，版本、输入输出类型和可用性仍须核查，不能因模型名相似就假设能互换。 例如“从图像识别对象”可匹配检测模型，“把语音转文本”匹配 ASR；两个任务需要不同媒体输入和输出合同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-hugginggpt-c07a7bb7" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-898d4e2f2bf49825">HuggingGPT 为什么把专家模型描述当可匹配的能力目录？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahugginggpt">HuggingGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>控制器不必自己掌握所有视觉和语音能力，而是将子任务需求与模型卡描述匹配，再调用相应专家。描述提供选择线索而非能力保证，版本、输入输出类型和可用性仍须核查，不能因模型名相似就假设能互换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如“从图像识别对象”可匹配检测模型，“把语音转文本”匹配 ASR；两个任务需要不同媒体输入和输出合同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17580">原论文</a> · <a href="../../../../agent-research/2303.17580-hugginggpt/">实现解读</a> · <a href="#qa-898d4e2f2bf49825">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hugginggpt" data-paper-title="HuggingGPT" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="HuggingGPT Agent Zhejiang University 2023-03-30 单个 LLM 难以覆盖视觉、语音和其他专业任务，而模型社区已有大量专家。HuggingGPT 让 ChatGPT 充当控制器：先把请求拆成带依赖的子任务，再按 Hugging Face 模型描述匹配专家，按拓扑顺序执行，最后把多模型输出组织为用户答案。 本页实现 task planning、按能力描述选择模型、依赖图执行和最终汇总四阶段。复现控制流、能力匹配和依赖执行；没有下载数百个 Hugging Face 模型，也未调用 ChatGPT。mini-suite 的 1.0 表示编排一致，不代表论文跨模态能力。PlanBench mini 120 episodes、seed 42；工具描述充当本地模型 capability registry，每个子任务保留 dependency edge 后执行。  专家模型编排 Agent 工具与协作执行：把计划变成可检查的动作 为什么多模态专家执行要遵守子任务依赖，而不是把所有模型同时调用？ 后续专家的输入可能是前面检测、识别或转写的输出，没有这些结果就无法正确调用。控制器先建依赖图，再按模型描述选择能力并拓扑执行，最后汇总；模型名称相似不证明接口兼容，独立任务才适合并行，依赖链不能被忽略。 例如先语音转写再翻译，需要把真实转写送入翻译器；两者同时启动并让翻译器猜转写内容，会破坏证据链。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a9a80e3694f3511f">为什么多模态专家执行要遵守子任务依赖，而不是把所有模型同时调用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahugginggpt">HuggingGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>后续专家的输入可能是前面检测、识别或转写的输出，没有这些结果就无法正确调用。控制器先建依赖图，再按模型描述选择能力并拓扑执行，最后汇总；模型名称相似不证明接口兼容，独立任务才适合并行，依赖链不能被忽略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先语音转写再翻译，需要把真实转写送入翻译器；两者同时启动并让翻译器猜转写内容，会破坏证据链。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17580">原论文</a> · <a href="../../../../agent-research/2303.17580-hugginggpt/">实现解读</a> · <a href="#qa-a9a80e3694f3511f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hugginggpt" data-paper-title="HuggingGPT" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="HuggingGPT Agent Zhejiang University 2023-03-30 单个 LLM 难以覆盖视觉、语音和其他专业任务，而模型社区已有大量专家。HuggingGPT 让 ChatGPT 充当控制器：先把请求拆成带依赖的子任务，再按 Hugging Face 模型描述匹配专家，按拓扑顺序执行，最后把多模型输出组织为用户答案。 本页实现 task planning、按能力描述选择模型、依赖图执行和最终汇总四阶段。复现控制流、能力匹配和依赖执行；没有下载数百个 Hugging Face 模型，也未调用 ChatGPT。mini-suite 的 1.0 表示编排一致，不代表论文跨模态能力。PlanBench mini 120 episodes、seed 42；工具描述充当本地模型 capability registry，每个子任务保留 dependency edge 后执行。  专家模型编排 Agent 工具与协作执行：把计划变成可检查的动作 语言控制器与专用多模态模型，分别承担理解编排还是具体计算？ 控制器解析用户需求、选择专家并组织子任务，专用模型实际处理视觉、语音等输入，结果再由控制器整合。编排正确不代表专家预测正确，专家单项成功也不保证最终综合回答符合任务。应分别核查选择、输入输出衔接和结果解释，不能把专家能力都归到语言控制器本身。 教学例：控制器决定先识图再生成语音，图像模型负责检测内容，语音模型负责合成；控制器并未因此自己获得同样的视觉参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-070cfaf4dcda6378">语言控制器与专用多模态模型，分别承担理解编排还是具体计算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahugginggpt">HuggingGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>控制器解析用户需求、选择专家并组织子任务，专用模型实际处理视觉、语音等输入，结果再由控制器整合。编排正确不代表专家预测正确，专家单项成功也不保证最终综合回答符合任务。应分别核查选择、输入输出衔接和结果解释，不能把专家能力都归到语言控制器本身。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：控制器决定先识图再生成语音，图像模型负责检测内容，语音模型负责合成；控制器并未因此自己获得同样的视觉参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17580">原论文</a> · <a href="../../../../agent-research/2303.17580-hugginggpt/">实现解读</a> · <a href="#qa-070cfaf4dcda6378">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:hugginggpt" data-paper-title="HuggingGPT" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="HuggingGPT Agent Zhejiang University 2023-03-30 单个 LLM 难以覆盖视觉、语音和其他专业任务，而模型社区已有大量专家。HuggingGPT 让 ChatGPT 充当控制器：先把请求拆成带依赖的子任务，再按 Hugging Face 模型描述匹配专家，按拓扑顺序执行，最后把多模型输出组织为用户答案。 本页实现 task planning、按能力描述选择模型、依赖图执行和最终汇总四阶段。复现控制流、能力匹配和依赖执行；没有下载数百个 Hugging Face 模型，也未调用 ChatGPT。mini-suite 的 1.0 表示编排一致，不代表论文跨模态能力。PlanBench mini 120 episodes、seed 42；工具描述充当本地模型 capability registry，每个子任务保留 dependency edge 后执行。  专家模型编排 Agent 工具与协作执行：把计划变成可检查的动作 本地 capability registry 和 dependency edge 是否已下载运行专家模型？ 没有。本地用工具描述代替模型能力目录，验证匹配与拓扑执行，没有数百个 Hugging Face checkpoint 或 ChatGPT 调用。边计数与编排一致性只能证明控制流，不能当跨模态内容质量或真实系统费用。 例如接口把检测节点输出交给回答节点，若内容由规则生成，就尚未证明真实视觉专家识别正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-974376ffc686eefe">本地 capability registry 和 dependency edge 是否已下载运行专家模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ahugginggpt">HuggingGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Zhejiang University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地用工具描述代替模型能力目录，验证匹配与拓扑执行，没有数百个 Hugging Face checkpoint 或 ChatGPT 调用。边计数与编排一致性只能证明控制流，不能当跨模态内容质量或真实系统费用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如接口把检测节点输出交给回答节点，若内容由规则生成，就尚未证明真实视觉专家识别正确。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.17580">原论文</a> · <a href="../../../../agent-research/2303.17580-hugginggpt/">实现解读</a> · <a href="#qa-974376ffc686eefe">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:art" data-paper-title="ART" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ART Agent University of Washington 2023-03-16 既有 tool-use prompting 常需为每个任务手写示例和调用顺序。ART 根据新任务自动检索相近的推理/工具示例，让冻结 LLM 生成程序；运行器遇到工具标记就暂停生成，执行工具并注入结果后继续。人可以用少量修订扩展任务库。 本页复现任务库检索、程序式多步推理、工具调用处暂停/恢复和成功示例写回，不把 mini-suite 写成完整 BIG-Bench/MMLU。保留自动示例检索、程序生成控制流、工具暂停和库更新；本地任务库很小，不调用冻结大模型，也未复刻 BIG-Bench/MMLU 原始分数。PlanBench mini 120 episodes、seed 42；按工具签名组织任务库，并逐工具暂停/恢复。  自动工具推理 Agent 工具与协作执行：把计划变成可检查的动作 ART 为什么希望新任务能复用已有的推理与工具示范？ 为每个任务手写完整 CoT 和工具流程成本高，已有任务示范可能包含可迁移的解题结构。ART 检索相关示例并生成带工具使用的过程，让外部计算参与解决新问题。示例复用仍需当前输入和工具返回校验，不是把旧答案照搬，也不保证任务换域后依旧适用。 教学例：见过用计算器比较成本的示范，遇到新的费用问题可复用分解方式；数字和工具返回必须针对本题重新获取。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-art-62b00229" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d8434f90df5880a2">ART 为什么希望新任务能复用已有的推理与工具示范？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aart">ART</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>为每个任务手写完整 CoT 和工具流程成本高，已有任务示范可能包含可迁移的解题结构。ART 检索相关示例并生成带工具使用的过程，让外部计算参与解决新问题。示例复用仍需当前输入和工具返回校验，不是把旧答案照搬，也不保证任务换域后依旧适用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：见过用计算器比较成本的示范，遇到新的费用问题可复用分解方式；数字和工具返回必须针对本题重新获取。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.09014">原论文</a> · <a href="../../../../agent-research/2303.09014-art/">实现解读</a> · <a href="#qa-d8434f90df5880a2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:art" data-paper-title="ART" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ART Agent University of Washington 2023-03-16 既有 tool-use prompting 常需为每个任务手写示例和调用顺序。ART 根据新任务自动检索相近的推理/工具示例，让冻结 LLM 生成程序；运行器遇到工具标记就暂停生成，执行工具并注入结果后继续。人可以用少量修订扩展任务库。 本页复现任务库检索、程序式多步推理、工具调用处暂停/恢复和成功示例写回，不把 mini-suite 写成完整 BIG-Bench/MMLU。保留自动示例检索、程序生成控制流、工具暂停和库更新；本地任务库很小，不调用冻结大模型，也未复刻 BIG-Bench/MMLU 原始分数。PlanBench mini 120 episodes、seed 42；按工具签名组织任务库，并逐工具暂停/恢复。  自动工具推理 Agent 工具与协作执行：把计划变成可检查的动作 为什么遇到工具标记时暂停生成、执行后再续写，比一次性写完含结果的程序更可靠？ 暂停让后续文本条件化于真实工具返回，避免模型预先想象执行结果。自动检索推理与工具示例减少手工提示负担，但运行器仍要识别标记并注入观察；冻结模型只是参数不更新，工具反馈仍会改变当前上下文和后续生成。 例如生成到数据库查询标记便执行，得到三条记录再汇总；不能先写出“查到十条”再补一段未执行查询装饰。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-16afeb1e858f4dd5">为什么遇到工具标记时暂停生成、执行后再续写，比一次性写完含结果的程序更可靠？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aart">ART</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>暂停让后续文本条件化于真实工具返回，避免模型预先想象执行结果。自动检索推理与工具示例减少手工提示负担，但运行器仍要识别标记并注入观察；冻结模型只是参数不更新，工具反馈仍会改变当前上下文和后续生成。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如生成到数据库查询标记便执行，得到三条记录再汇总；不能先写出“查到十条”再补一段未执行查询装饰。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.09014">原论文</a> · <a href="../../../../agent-research/2303.09014-art/">实现解读</a> · <a href="#qa-16afeb1e858f4dd5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:art" data-paper-title="ART" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ART Agent University of Washington 2023-03-16 既有 tool-use prompting 常需为每个任务手写示例和调用顺序。ART 根据新任务自动检索相近的推理/工具示例，让冻结 LLM 生成程序；运行器遇到工具标记就暂停生成，执行工具并注入结果后继续。人可以用少量修订扩展任务库。 本页复现任务库检索、程序式多步推理、工具调用处暂停/恢复和成功示例写回，不把 mini-suite 写成完整 BIG-Bench/MMLU。保留自动示例检索、程序生成控制流、工具暂停和库更新；本地任务库很小，不调用冻结大模型，也未复刻 BIG-Bench/MMLU 原始分数。PlanBench mini 120 episodes、seed 42；按工具签名组织任务库，并逐工具暂停/恢复。  自动工具推理 Agent 工具与协作执行：把计划变成可检查的动作 自动检索示例与为每个新任务手写 CoT 有何取舍？ 检索复用任务库中的推理工具模式，减少逐任务人工编写，但相似示例未必满足当前约束。少量人工修订可扩展库，仍要验证新程序，不能把旧示例完整照搬视为新任务已解决或不需任何人类维护。 例如旧示例展示先搜索再计算的结构可复用，新题的查询和参数仍由当前问题决定，而非复制旧题答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-64e08257bb08b925">自动检索示例与为每个新任务手写 CoT 有何取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aart">ART</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>检索复用任务库中的推理工具模式，减少逐任务人工编写，但相似示例未必满足当前约束。少量人工修订可扩展库，仍要验证新程序，不能把旧示例完整照搬视为新任务已解决或不需任何人类维护。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧示例展示先搜索再计算的结构可复用，新题的查询和参数仍由当前问题决定，而非复制旧题答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.09014">原论文</a> · <a href="../../../../agent-research/2303.09014-art/">实现解读</a> · <a href="#qa-64e08257bb08b925">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:art" data-paper-title="ART" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="ART Agent University of Washington 2023-03-16 既有 tool-use prompting 常需为每个任务手写示例和调用顺序。ART 根据新任务自动检索相近的推理/工具示例，让冻结 LLM 生成程序；运行器遇到工具标记就暂停生成，执行工具并注入结果后继续。人可以用少量修订扩展任务库。 本页复现任务库检索、程序式多步推理、工具调用处暂停/恢复和成功示例写回，不把 mini-suite 写成完整 BIG-Bench/MMLU。保留自动示例检索、程序生成控制流、工具暂停和库更新；本地任务库很小，不调用冻结大模型，也未复刻 BIG-Bench/MMLU 原始分数。PlanBench mini 120 episodes、seed 42；按工具签名组织任务库，并逐工具暂停/恢复。  自动工具推理 Agent 工具与协作执行：把计划变成可检查的动作 本地工具签名任务库与冻结 LLM 程序生成的差距是什么？ 本地只验证小库检索、逐工具暂停恢复和更新控制流，没有调用冻结大模型或运行 BIG-Bench、MMLU。暂停次数可以证明执行分支发生，但程序语义是否由模型正确生成尚需真实模型证据，代理成本也不等于原文 token。 例如三次工具暂停由结构化模板驱动，可检验 runner；不能据此声称模型已能为任意自然语言题自动编程。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-9e15636c7c6d5f1c">本地工具签名任务库与冻结 LLM 程序生成的差距是什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aart">ART</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Washington</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地只验证小库检索、逐工具暂停恢复和更新控制流，没有调用冻结大模型或运行 BIG-Bench、MMLU。暂停次数可以证明执行分支发生，但程序语义是否由模型正确生成尚需真实模型证据，代理成本也不等于原文 token。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三次工具暂停由结构化模板驱动，可检验 runner；不能据此声称模型已能为任意自然语言题自动编程。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2303.09014">原论文</a> · <a href="../../../../agent-research/2303.09014-art/">实现解读</a> · <a href="#qa-9e15636c7c6d5f1c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolformer" data-paper-title="Toolformer" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Toolformer Agent Meta AI Research 2023-02-09 手工标注工具调用昂贵，纯 prompting 又难以让较小模型稳定决定何时调用。Toolformer 先用少量 demonstration 采样 API call，再比较插入真实返回值、隐藏返回值和完全不调用时的后续 token loss，只保留确实有用的调用并继续语言模型训练。 本页实现候选 API call 生成、no-call/masked-call loss 对照和自监督过滤，只保留能降低预测 loss 的工具调用。实现自监督候选过滤的核心判据，但 loss 来自确定性 tool utility，不是 GPT-J token loss；未进行 6.7B continued training，也未复刻论文五类真实 API。ScaleMCP mini 对 required 和 distractor tools 都生成候选，只有相对 no-call 降低 loss 的调用被接受。  工具学习 Agent 工具与协作执行：把计划变成可检查的动作 Toolformer 为什么希望模型从文本训练中学会何时借助外部工具？ 语言模型可生成流畅文本，却不总擅长计算、查新事实或可靠检索。Toolformer 研究把有帮助的 API 调用融入训练语料，让模型学习调用的时机、参数及返回值利用。数据筛选只提供学习信号，工具存在也不保证每次调用有用，更不能把本地筛选流程当作模型已训练。 教学例：写到具体乘法时调用计算器，再接着完成句子；是否插入调用应取决于它能否帮助后续预测，而不是逢数字必调。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-toolformer-dc9c6efa" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-941bf8191f60f91a">Toolformer 为什么希望模型从文本训练中学会何时借助外部工具？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolformer">Toolformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言模型可生成流畅文本，却不总擅长计算、查新事实或可靠检索。Toolformer 研究把有帮助的 API 调用融入训练语料，让模型学习调用的时机、参数及返回值利用。数据筛选只提供学习信号，工具存在也不保证每次调用有用，更不能把本地筛选流程当作模型已训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：写到具体乘法时调用计算器，再接着完成句子；是否插入调用应取决于它能否帮助后续预测，而不是逢数字必调。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2302.04761">原论文</a> · <a href="../../../../agent-research/2302.04761-toolformer/">实现解读</a> · <a href="#qa-941bf8191f60f91a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolformer" data-paper-title="Toolformer" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Toolformer Agent Meta AI Research 2023-02-09 手工标注工具调用昂贵，纯 prompting 又难以让较小模型稳定决定何时调用。Toolformer 先用少量 demonstration 采样 API call，再比较插入真实返回值、隐藏返回值和完全不调用时的后续 token loss，只保留确实有用的调用并继续语言模型训练。 本页实现候选 API call 生成、no-call/masked-call loss 对照和自监督过滤，只保留能降低预测 loss 的工具调用。实现自监督候选过滤的核心判据，但 loss 来自确定性 tool utility，不是 GPT-J token loss；未进行 6.7B continued training，也未复刻论文五类真实 API。ScaleMCP mini 对 required 和 distractor tools 都生成候选，只有相对 no-call 降低 loss 的调用被接受。  工具学习 Agent 工具与协作执行：把计划变成可检查的动作 为什么筛选 API 调用要比较有返回、隐藏返回与不调用时的后续 loss？ 只看调用字符串可能把有用提示格式误认为真实工具价值。对照不同返回条件，检查实际结果是否降低后续预测损失，再保留超过门槛的调用训练模型，才能更接近学习调用效用；这个自监督代理也不等于所有任务正确率或真实业务收益。 例如计算器调用形式本身不告诉乘积，只有注入正确返回才改善后续预测，筛选才有理由保留这次计算调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bf11c35f247b81e0">为什么筛选 API 调用要比较有返回、隐藏返回与不调用时的后续 loss？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolformer">Toolformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只看调用字符串可能把有用提示格式误认为真实工具价值。对照不同返回条件，检查实际结果是否降低后续预测损失，再保留超过门槛的调用训练模型，才能更接近学习调用效用；这个自监督代理也不等于所有任务正确率或真实业务收益。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如计算器调用形式本身不告诉乘积，只有注入正确返回才改善后续预测，筛选才有理由保留这次计算调用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2302.04761">原论文</a> · <a href="../../../../agent-research/2302.04761-toolformer/">实现解读</a> · <a href="#qa-bf11c35f247b81e0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolformer" data-paper-title="Toolformer" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Toolformer Agent Meta AI Research 2023-02-09 手工标注工具调用昂贵，纯 prompting 又难以让较小模型稳定决定何时调用。Toolformer 先用少量 demonstration 采样 API call，再比较插入真实返回值、隐藏返回值和完全不调用时的后续 token loss，只保留确实有用的调用并继续语言模型训练。 本页实现候选 API call 生成、no-call/masked-call loss 对照和自监督过滤，只保留能降低预测 loss 的工具调用。实现自监督候选过滤的核心判据，但 loss 来自确定性 tool utility，不是 GPT-J token loss；未进行 6.7B continued training，也未复刻论文五类真实 API。ScaleMCP mini 对 required 和 distractor tools 都生成候选，只有相对 no-call 降低 loss 的调用被接受。  工具学习 Agent 工具与协作执行：把计划变成可检查的动作 Toolformer 的调用数据构建与人工逐条标注工具轨迹，监督来源有何区别？ 人工轨迹直接示范动作序列，Toolformer 则从少量示范出发采样候选调用，用返回值对后续文本预测的帮助筛选样本，再用于语言模型训练。它减少逐条人工标注需求，但仍依赖已有工具和筛选信号，不能据此声称无需任何示范或已经验证任意开放任务。 教学例：人工不必为每句话标出计算器调用，而是由候选生成与 loss 检查挑选部分调用；错误候选仍可能需要过滤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-50aa9ed63c22b586">Toolformer 的调用数据构建与人工逐条标注工具轨迹，监督来源有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolformer">Toolformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>人工轨迹直接示范动作序列，Toolformer 则从少量示范出发采样候选调用，用返回值对后续文本预测的帮助筛选样本，再用于语言模型训练。它减少逐条人工标注需求，但仍依赖已有工具和筛选信号，不能据此声称无需任何示范或已经验证任意开放任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：人工不必为每句话标出计算器调用，而是由候选生成与 loss 检查挑选部分调用；错误候选仍可能需要过滤。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2302.04761">原论文</a> · <a href="../../../../agent-research/2302.04761-toolformer/">实现解读</a> · <a href="#qa-50aa9ed63c22b586">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:toolformer" data-paper-title="Toolformer" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="Toolformer Agent Meta AI Research 2023-02-09 手工标注工具调用昂贵，纯 prompting 又难以让较小模型稳定决定何时调用。Toolformer 先用少量 demonstration 采样 API call，再比较插入真实返回值、隐藏返回值和完全不调用时的后续 token loss，只保留确实有用的调用并继续语言模型训练。 本页实现候选 API call 生成、no-call/masked-call loss 对照和自监督过滤，只保留能降低预测 loss 的工具调用。实现自监督候选过滤的核心判据，但 loss 来自确定性 tool utility，不是 GPT-J token loss；未进行 6.7B continued training，也未复刻论文五类真实 API。ScaleMCP mini 对 required 和 distractor tools 都生成候选，只有相对 no-call 降低 loss 的调用被接受。  工具学习 Agent 工具与协作执行：把计划变成可检查的动作 本地 utility loss 过滤为何不能当作 GPT-J continued training 完成？ 本地的 loss 来自确定性 tool utility，保留候选判据但没有 GPT-J token likelihood、6.7B 参数训练或五类真实 API。候选和接纳数量证明过滤运行，不证明模型学会何时调用；必须明确诊断代理，不能与原文零样本能力横比。 例如预设工具有用就降低一个规则 loss，验证的是筛选逻辑，不是语言模型在真实语料上自动发现工具价值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8a4db4174ad5d40b">本地 utility loss 过滤为何不能当作 GPT-J continued training 完成？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atoolformer">Toolformer</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地的 loss 来自确定性 tool utility，保留候选判据但没有 GPT-J token likelihood、6.7B 参数训练或五类真实 API。候选和接纳数量证明过滤运行，不证明模型学会何时调用；必须明确诊断代理，不能与原文零样本能力横比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如预设工具有用就降低一个规则 loss，验证的是筛选逻辑，不是语言模型在真实语料上自动发现工具价值。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2302.04761">原论文</a> · <a href="../../../../agent-research/2302.04761-toolformer/">实现解读</a> · <a href="#qa-8a4db4174ad5d40b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pal" data-paper-title="PAL" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PAL Agent Carnegie Mellon University 2022-11-18 LLM 擅长把问题分解成步骤，却会在算术和符号执行阶段出错。PAL 让 LLM 输出带变量和控制流的程序，最终计算完全交给 Python 等确定性 runtime；模型只承担自然语言理解和程序合成。 本页复现“语言模型生成程序、符号 runtime 执行、返回解释器答案”的系统边界，不把结构化 task program 写成 Codex 生成代码。保留神经程序生成与符号执行的职责分离；本地使用受控中间表示而非任意 Python，不调用 Codex，也未复刻原论文 GSM8K。ScaleMCP mini 120 episodes、seed 42；每题实际构建 CALL/RETURN 程序并由本地解释器执行。  程序推理 Agent 工具与协作执行：把计划变成可检查的动作 PAL 为什么让语言模型写程序，再把具体计算交给解释器？ 自然语言问题往往既需要理解关系，又需要精确执行运算。PAL 让模型把理解转成可运行程序，由解释器完成计算，减少语言模型逐步手算的负担。关键前提是程序确实表达题意，解释器只执行代码，不会发现遗漏条件或错误建模。 教学例：模型把人数和单价写成变量交给程序求总价；若忘了儿童半价，计算器算得再准确也只是执行了错误公式。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-pal-f0f14e4c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7e1c7b8a77c3e843">PAL 为什么让语言模型写程序，再把具体计算交给解释器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apal">PAL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>自然语言问题往往既需要理解关系，又需要精确执行运算。PAL 让模型把理解转成可运行程序，由解释器完成计算，减少语言模型逐步手算的负担。关键前提是程序确实表达题意，解释器只执行代码，不会发现遗漏条件或错误建模。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：模型把人数和单价写成变量交给程序求总价；若忘了儿童半价，计算器算得再准确也只是执行了错误公式。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.10435">原论文</a> · <a href="../../../../agent-research/2211.10435-pal/">实现解读</a> · <a href="#qa-7e1c7b8a77c3e843">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pal" data-paper-title="PAL" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PAL Agent Carnegie Mellon University 2022-11-18 LLM 擅长把问题分解成步骤，却会在算术和符号执行阶段出错。PAL 让 LLM 输出带变量和控制流的程序，最终计算完全交给 Python 等确定性 runtime；模型只承担自然语言理解和程序合成。 本页复现“语言模型生成程序、符号 runtime 执行、返回解释器答案”的系统边界，不把结构化 task program 写成 Codex 生成代码。保留神经程序生成与符号执行的职责分离；本地使用受控中间表示而非任意 Python，不调用 Codex，也未复刻原论文 GSM8K。ScaleMCP mini 120 episodes、seed 42；每题实际构建 CALL/RETURN 程序并由本地解释器执行。  程序推理 Agent 工具与协作执行：把计划变成可检查的动作 把算术交给 Python 后，模型为什么仍可能给出错误答案？ 确定性 runtime 保证执行给定程序，不保证程序正确表达题意。模型还要理解变量、关系和控制流，若把折扣顺序或单位写错，Python 会精确执行错误逻辑；PAL 分离程序合成与计算执行，降低算术出错但并不消除建模错误。 例如题意先打折再加运费，程序却给总额一起打折，计算器执行无误，最终价格仍与用户要求不符。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c9d3e89879637bdf">把算术交给 Python 后，模型为什么仍可能给出错误答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apal">PAL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>确定性 runtime 保证执行给定程序，不保证程序正确表达题意。模型还要理解变量、关系和控制流，若把折扣顺序或单位写错，Python 会精确执行错误逻辑；PAL 分离程序合成与计算执行，降低算术出错但并不消除建模错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如题意先打折再加运费，程序却给总额一起打折，计算器执行无误，最终价格仍与用户要求不符。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.10435">原论文</a> · <a href="../../../../agent-research/2211.10435-pal/">实现解读</a> · <a href="#qa-c9d3e89879637bdf">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pal" data-paper-title="PAL" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PAL Agent Carnegie Mellon University 2022-11-18 LLM 擅长把问题分解成步骤，却会在算术和符号执行阶段出错。PAL 让 LLM 输出带变量和控制流的程序，最终计算完全交给 Python 等确定性 runtime；模型只承担自然语言理解和程序合成。 本页复现“语言模型生成程序、符号 runtime 执行、返回解释器答案”的系统边界，不把结构化 task program 写成 Codex 生成代码。保留神经程序生成与符号执行的职责分离；本地使用受控中间表示而非任意 Python，不调用 Codex，也未复刻原论文 GSM8K。ScaleMCP mini 120 episodes、seed 42；每题实际构建 CALL/RETURN 程序并由本地解释器执行。  程序推理 Agent 工具与协作执行：把计划变成可检查的动作 PAL 与只用 CoT 手算相比，错误来源怎样变化？ CoT 同时承担理解、步骤和数值执行，PAL 把精确计算转给程序，减少手算误差但增加代码生成和接口风险。能运行的程序提供可检查中间量，仍应验证输入与公式；两条路线效果需按任务和预算测量，不能从确定性直接推导准确率。 例如长乘法交给解释器可避免算错数字，但把税率误读为金额仍属于模型理解错误，两种错误不能混在一起。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-94f7d51c0584d5a3">PAL 与只用 CoT 手算相比，错误来源怎样变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apal">PAL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>CoT 同时承担理解、步骤和数值执行，PAL 把精确计算转给程序，减少手算误差但增加代码生成和接口风险。能运行的程序提供可检查中间量，仍应验证输入与公式；两条路线效果需按任务和预算测量，不能从确定性直接推导准确率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长乘法交给解释器可避免算错数字，但把税率误读为金额仍属于模型理解错误，两种错误不能混在一起。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.10435">原论文</a> · <a href="../../../../agent-research/2211.10435-pal/">实现解读</a> · <a href="#qa-94f7d51c0584d5a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pal" data-paper-title="PAL" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="PAL Agent Carnegie Mellon University 2022-11-18 LLM 擅长把问题分解成步骤，却会在算术和符号执行阶段出错。PAL 让 LLM 输出带变量和控制流的程序，最终计算完全交给 Python 等确定性 runtime；模型只承担自然语言理解和程序合成。 本页复现“语言模型生成程序、符号 runtime 执行、返回解释器答案”的系统边界，不把结构化 task program 写成 Codex 生成代码。保留神经程序生成与符号执行的职责分离；本地使用受控中间表示而非任意 Python，不调用 Codex，也未复刻原论文 GSM8K。ScaleMCP mini 120 episodes、seed 42；每题实际构建 CALL/RETURN 程序并由本地解释器执行。  程序推理 Agent 工具与协作执行：把计划变成可检查的动作 本地 CALL/RETURN 中间表示等同任意 Python 程序执行吗？ 不等同。本地使用受控中间表示和解释器，验证程序构造及执行职责分离，不调用 Codex，也未运行原文 GSM8K。限制动作空间有助检查合同，但不能把受控可执行计划的满分改成开放 Python 合成能力或通用安全沙箱。 例如解释器只支持预定义 CALL 节点，不会验证任意循环、文件访问和外部依赖，范围与真实 Python runtime 不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8bc0289c64e50fec">本地 CALL/RETURN 中间表示等同任意 Python 程序执行吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apal">PAL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Carnegie Mellon University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不等同。本地使用受控中间表示和解释器，验证程序构造及执行职责分离，不调用 Codex，也未运行原文 GSM8K。限制动作空间有助检查合同，但不能把受控可执行计划的满分改成开放 Python 合成能力或通用安全沙箱。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如解释器只支持预定义 CALL 节点，不会验证任意循环、文件访问和外部依赖，范围与真实 Python runtime 不同。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2211.10435">原论文</a> · <a href="../../../../agent-research/2211.10435-pal/">实现解读</a> · <a href="#qa-8bc0289c64e50fec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mrkl" data-paper-title="MRKL" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MRKL Agent AI21 Labs 2022-05-01 单个 LLM 容易在精确计算、时效知识和可验证推理上失败。MRKL 把 LLM 放入系统架构，由 router 根据输入选择语言模型、知识库、计算器等专家；离散模块保证确定性能力，语言模型负责理解和自然语言接口。 本页实现显式 router、神经/离散专家注册表和结果汇总；不是让一个通用 prompt 直接返回正确工具链。保留 router 和可区分的专家执行计数；本地专家是确定性 mini-suite 工具，不调用 Jurassic-X、真实搜索服务或私有知识库，成本是统一代理成本而非线上延迟。ScaleMCP mini 120 episodes、seed 42；每个工具动作都先经 router，计算器、日历、地图、天气、数据库和表格进入离散专家。  神经符号路由 Agent 工具与协作执行：把计划变成可检查的动作 MRKL 为什么把语言模型与不同的外部专家模块组合起来？ 开放问题既可能需要语言理解，也可能需要精确计算、数据库查询或其他专用能力。MRKL 让语言模型组织任务并路由到适合的模块，再整合结果。模块化把能力来源分开，也增加路由和接口衔接的错误点，不能从某个模块可靠推出整个系统可靠。 教学例：问账户余额变化，可让数据库取数、计算模块求差，再用语言解释；若路由查询了错误账户，正确计算也无济于事。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-mrkl-816ab670" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-c7fbb257a95880c3">MRKL 为什么把语言模型与不同的外部专家模块组合起来？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amrkl">MRKL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AI21 Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>开放问题既可能需要语言理解，也可能需要精确计算、数据库查询或其他专用能力。MRKL 让语言模型组织任务并路由到适合的模块，再整合结果。模块化把能力来源分开，也增加路由和接口衔接的错误点，不能从某个模块可靠推出整个系统可靠。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：问账户余额变化，可让数据库取数、计算模块求差，再用语言解释；若路由查询了错误账户，正确计算也无济于事。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.00445">原论文</a> · <a href="../../../../agent-research/2205.00445-mrkl/">实现解读</a> · <a href="#qa-c7fbb257a95880c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mrkl" data-paper-title="MRKL" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MRKL Agent AI21 Labs 2022-05-01 单个 LLM 容易在精确计算、时效知识和可验证推理上失败。MRKL 把 LLM 放入系统架构，由 router 根据输入选择语言模型、知识库、计算器等专家；离散模块保证确定性能力，语言模型负责理解和自然语言接口。 本页实现显式 router、神经/离散专家注册表和结果汇总；不是让一个通用 prompt 直接返回正确工具链。保留 router 和可区分的专家执行计数；本地专家是确定性 mini-suite 工具，不调用 Jurassic-X、真实搜索服务或私有知识库，成本是统一代理成本而非线上延迟。ScaleMCP mini 120 episodes、seed 42；每个工具动作都先经 router，计算器、日历、地图、天气、数据库和表格进入离散专家。  神经符号路由 Agent 工具与协作执行：把计划变成可检查的动作 路由到确定性模块，为什么不能据此保证整个系统答案确定正确？ 计算器或数据库只在各自合同内可靠，路由器仍可能选错模块或传错输入，语言层也可能误解和错误组织结果。MRKL 的价值在于把精确能力从语言生成中拆出，明确各模块边界；局部确定性与端到端任务正确性是两层不同保证。 例如用户问含税价格，路由器虽调用计算器，却传入错误税率；结果可重复且精确，仍不是正确业务答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3b8ae0b3087063fb">路由到确定性模块，为什么不能据此保证整个系统答案确定正确？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amrkl">MRKL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AI21 Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>计算器或数据库只在各自合同内可靠，路由器仍可能选错模块或传错输入，语言层也可能误解和错误组织结果。MRKL 的价值在于把精确能力从语言生成中拆出，明确各模块边界；局部确定性与端到端任务正确性是两层不同保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户问含税价格，路由器虽调用计算器，却传入错误税率；结果可重复且精确，仍不是正确业务答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.00445">原论文</a> · <a href="../../../../agent-research/2205.00445-mrkl/">实现解读</a> · <a href="#qa-3b8ae0b3087063fb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mrkl" data-paper-title="MRKL" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MRKL Agent AI21 Labs 2022-05-01 单个 LLM 容易在精确计算、时效知识和可验证推理上失败。MRKL 把 LLM 放入系统架构，由 router 根据输入选择语言模型、知识库、计算器等专家；离散模块保证确定性能力，语言模型负责理解和自然语言接口。 本页实现显式 router、神经/离散专家注册表和结果汇总；不是让一个通用 prompt 直接返回正确工具链。保留 router 和可区分的专家执行计数；本地专家是确定性 mini-suite 工具，不调用 Jurassic-X、真实搜索服务或私有知识库，成本是统一代理成本而非线上延迟。ScaleMCP mini 120 episodes、seed 42；每个工具动作都先经 router，计算器、日历、地图、天气、数据库和表格进入离散专家。  神经符号路由 Agent 工具与协作执行：把计划变成可检查的动作 模块化专家与单一 LLM 包办所有步骤有什么取舍？ 专家可让确定性运算或时效知识更可控，单模型接口较简单却容易凭内部记忆回答。模块化增加路由、数据转换和错误处理成本，也受专家覆盖限制，不能因存在计算器就声称整个系统具备可证明正确性。 例如精确日期差交给日历模块合适，但“为何延期”仍需语言理解和证据，不能让一个离散函数包办所有语义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1ffb366fa4415fbc">模块化专家与单一 LLM 包办所有步骤有什么取舍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amrkl">MRKL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AI21 Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>专家可让确定性运算或时效知识更可控，单模型接口较简单却容易凭内部记忆回答。模块化增加路由、数据转换和错误处理成本，也受专家覆盖限制，不能因存在计算器就声称整个系统具备可证明正确性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如精确日期差交给日历模块合适，但“为何延期”仍需语言理解和证据，不能让一个离散函数包办所有语义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.00445">原论文</a> · <a href="../../../../agent-research/2205.00445-mrkl/">实现解读</a> · <a href="#qa-1ffb366fa4415fbc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:mrkl" data-paper-title="MRKL" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="MRKL Agent AI21 Labs 2022-05-01 单个 LLM 容易在精确计算、时效知识和可验证推理上失败。MRKL 把 LLM 放入系统架构，由 router 根据输入选择语言模型、知识库、计算器等专家；离散模块保证确定性能力，语言模型负责理解和自然语言接口。 本页实现显式 router、神经/离散专家注册表和结果汇总；不是让一个通用 prompt 直接返回正确工具链。保留 router 和可区分的专家执行计数；本地专家是确定性 mini-suite 工具，不调用 Jurassic-X、真实搜索服务或私有知识库，成本是统一代理成本而非线上延迟。ScaleMCP mini 120 episodes、seed 42；每个工具动作都先经 router，计算器、日历、地图、天气、数据库和表格进入离散专家。  神经符号路由 Agent 工具与协作执行：把计划变成可检查的动作 本地专家调用统计是否包含 Jurassic-X 或真实知识库？ 没有。本地使用确定性 mini-suite 的计算器、日历等专家，验证 router 与可区分执行计数，不调用 Jurassic-X、搜索服务或私有库。成本是代理量，不能当线上延迟；符号调用次数也不能证明开放问答或时效知识质量。 例如数据库模块返回 fixture 记录可测试调度，但没有真实库权限、查询失败和更新，就不能验证生产数据访问能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-559b994dc46c150a">本地专家调用统计是否包含 Jurassic-X 或真实知识库？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Amrkl">MRKL</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · AI21 Labs</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地使用确定性 mini-suite 的计算器、日历等专家，验证 router 与可区分执行计数，不调用 Jurassic-X、搜索服务或私有库。成本是代理量，不能当线上延迟；符号调用次数也不能证明开放问答或时效知识质量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如数据库模块返回 fixture 记录可测试调度，但没有真实库权限、查询失败和更新，就不能验证生产数据访问能力。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2205.00445">原论文</a> · <a href="../../../../agent-research/2205.00445-mrkl/">实现解读</a> · <a href="#qa-559b994dc46c150a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:saycan" data-paper-title="SayCan" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SayCan Agent Robotics at Google 2022-04-04 LLM 知道“应该做什么”，却不知道当前机器人“能不能做”。SayCan 为每个预训练技能同时计算语言相关性和 value-function affordance，选择乘积最高的技能并执行，再把动作追加到上下文继续规划。 本页复现逐步技能枚举及“语言分数 × affordance”决策，不把确定性工具 mini-suite 冒充真实移动机械臂。保留双分数逐步规划与不可行技能过滤；affordance 是确定性本地可执行性，不含视觉、机器人控制策略或真实 value-function 训练。PlanBench mini 120 episodes、seed 42；每一步同时打分必要技能和干扰技能。  具身规划 Agent 工具与协作执行：把计划变成可检查的动作 机器人为什么不能把语言模型生成的合理计划直接当成可执行动作？ 语言模型擅长判断语义上该做什么，却未必知道机器人当前位置、技能范围和物理条件。SayCan 研究把语言任务理解与实际技能可行性联系起来，选择既相关又有机会执行的下一步。可行性估计仍可能失准，模拟计划和真实完成要分别报告。 教学例：用户要饮料，语言上“拿杯子”合理；如果杯子不在可达范围，机器人需要先选择自己当前能完成的操作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-saycan-7674e520" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a29c0976bcc5a61c">机器人为什么不能把语言模型生成的合理计划直接当成可执行动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asaycan">SayCan</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Robotics at Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言模型擅长判断语义上该做什么，却未必知道机器人当前位置、技能范围和物理条件。SayCan 研究把语言任务理解与实际技能可行性联系起来，选择既相关又有机会执行的下一步。可行性估计仍可能失准，模拟计划和真实完成要分别报告。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：用户要饮料，语言上“拿杯子”合理；如果杯子不在可达范围，机器人需要先选择自己当前能完成的操作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2204.01691">原论文</a> · <a href="../../../../agent-research/2204.01691-saycan/">实现解读</a> · <a href="#qa-a29c0976bcc5a61c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:saycan" data-paper-title="SayCan" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SayCan Agent Robotics at Google 2022-04-04 LLM 知道“应该做什么”，却不知道当前机器人“能不能做”。SayCan 为每个预训练技能同时计算语言相关性和 value-function affordance，选择乘积最高的技能并执行，再把动作追加到上下文继续规划。 本页复现逐步技能枚举及“语言分数 × affordance”决策，不把确定性工具 mini-suite 冒充真实移动机械臂。保留双分数逐步规划与不可行技能过滤；affordance 是确定性本地可执行性，不含视觉、机器人控制策略或真实 value-function 训练。PlanBench mini 120 episodes、seed 42；每一步同时打分必要技能和干扰技能。  具身规划 Agent 工具与协作执行：把计划变成可检查的动作 语言相关性与 affordance 相乘，为什么能过滤“合理但做不到”的动作？ 语言模型衡量技能与指令、历史是否匹配，价值函数衡量当前环境下执行成功的可能，两者乘积要求语义合适且物理可行。单靠语言可能建议拿取够不到的物体，单靠可行性又可能执行无关动作；评分仍依赖技能库与价值估计的覆盖。 例如指令要拿杯子，但杯子在锁柜里，直接抓取语言上相关却可行性低；先开柜可能更适合作为下一技能。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-ff44151b17aba420">语言相关性与 affordance 相乘，为什么能过滤“合理但做不到”的动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asaycan">SayCan</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Robotics at Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语言模型衡量技能与指令、历史是否匹配，价值函数衡量当前环境下执行成功的可能，两者乘积要求语义合适且物理可行。单靠语言可能建议拿取够不到的物体，单靠可行性又可能执行无关动作；评分仍依赖技能库与价值估计的覆盖。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如指令要拿杯子，但杯子在锁柜里，直接抓取语言上相关却可行性低；先开柜可能更适合作为下一技能。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2204.01691">原论文</a> · <a href="../../../../agent-research/2204.01691-saycan/">实现解读</a> · <a href="#qa-ff44151b17aba420">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:saycan" data-paper-title="SayCan" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SayCan Agent Robotics at Google 2022-04-04 LLM 知道“应该做什么”，却不知道当前机器人“能不能做”。SayCan 为每个预训练技能同时计算语言相关性和 value-function affordance，选择乘积最高的技能并执行，再把动作追加到上下文继续规划。 本页复现逐步技能枚举及“语言分数 × affordance”决策，不把确定性工具 mini-suite 冒充真实移动机械臂。保留双分数逐步规划与不可行技能过滤；affordance 是确定性本地可执行性，不含视觉、机器人控制策略或真实 value-function 训练。PlanBench mini 120 episodes、seed 42；每一步同时打分必要技能和干扰技能。  具身规划 Agent 工具与协作执行：把计划变成可检查的动作 plan success 与 execution success 为什么不能当同一机器人指标？ 计划语义合理仍可能因感知、抓取或控制失败而执行不成，执行指标包含物理落实风险。SayCan 分别报告二者，不能拿较高规划率描述成实际机器人完成率；本地确定性可执行门更没有覆盖这些真实控制失误。 例如步骤“拿杯子再放桌上”规划正确，夹爪滑落导致未完成，不能因为计划合格就计一次执行成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-878039f33300c8bc">plan success 与 execution success 为什么不能当同一机器人指标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asaycan">SayCan</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Robotics at Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>计划语义合理仍可能因感知、抓取或控制失败而执行不成，执行指标包含物理落实风险。SayCan 分别报告二者，不能拿较高规划率描述成实际机器人完成率；本地确定性可执行门更没有覆盖这些真实控制失误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如步骤“拿杯子再放桌上”规划正确，夹爪滑落导致未完成，不能因为计划合格就计一次执行成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2204.01691">原论文</a> · <a href="../../../../agent-research/2204.01691-saycan/">实现解读</a> · <a href="#qa-878039f33300c8bc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:saycan" data-paper-title="SayCan" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="SayCan Agent Robotics at Google 2022-04-04 LLM 知道“应该做什么”，却不知道当前机器人“能不能做”。SayCan 为每个预训练技能同时计算语言相关性和 value-function affordance，选择乘积最高的技能并执行，再把动作追加到上下文继续规划。 本页复现逐步技能枚举及“语言分数 × affordance”决策，不把确定性工具 mini-suite 冒充真实移动机械臂。保留双分数逐步规划与不可行技能过滤；affordance 是确定性本地可执行性，不含视觉、机器人控制策略或真实 value-function 训练。PlanBench mini 120 episodes、seed 42；每一步同时打分必要技能和干扰技能。  具身规划 Agent 工具与协作执行：把计划变成可检查的动作 本地 affordance checks 验证了真实 value-function 训练吗？ 没有。本地用确定性可执行性过滤必要和干扰技能，保留双分数逐步选择，没有视觉、机器人策略或真实价值网络训练。检查数量和过滤数量证明路径运行，不是预测成功概率校准，不能直接对标实体机器人任务结果。 例如规则知道手被占用就拒绝抓取，可验证门控；它没有从图像估计物体可达性或抓取成功率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-449b830f70953589">本地 affordance checks 验证了真实 value-function 训练吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asaycan">SayCan</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Robotics at Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有。本地用确定性可执行性过滤必要和干扰技能，保留双分数逐步选择，没有视觉、机器人策略或真实价值网络训练。检查数量和过滤数量证明路径运行，不是预测成功概率校准，不能直接对标实体机器人任务结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如规则知道手被占用就拒绝抓取，可验证门控；它没有从图像估计物体可达性或抓取成功率。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2204.01691">原论文</a> · <a href="../../../../agent-research/2204.01691-saycan/">实现解读</a> · <a href="#qa-449b830f70953589">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:webgpt" data-paper-title="WebGPT" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="WebGPT Agent OpenAI 2021-12-17 长文本问答容易幻觉，且很难核查依据。WebGPT 让模型在文本浏览器里搜索、点击和滚动，回答必须收集引用；训练先做行为克隆，再用人类偏好 reward model 从多条浏览/回答轨迹中做拒绝采样。 本页复现文本浏览轨迹、证据引用和 reward-model 拒绝采样；本地确定性工具环境不是实时互联网浏览。保留 browser-action、citation constraint 和 trajectory rejection sampling；不访问实时网页、不训练 GPT-3/reward model，也不复刻 ELI5 人评。ScaleMCP mini 120 episodes、seed 42；每题生成两条工具轨迹，按证据覆盖选择。  浏览问答 Agent 工具与协作执行：把计划变成可检查的动作 WebGPT 为什么把浏览和来源支持纳入长篇问答，而不只让模型凭记忆作答？ 开放问题常需要新信息或多个来源，纯参数回答可能缺少可核查依据。WebGPT 让模型通过浏览收集证据，再形成带引用的回答，并利用人类反馈评价质量。浏览获得的文本仍需正确理解，链接数量不能代替来源对具体结论的支持，也不保证覆盖所有重要事实。 教学例：比较两项政策需要分别找到原始说明，再解释差异；只在段末附一个相关网站，不能证明其中每个数字都有依据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<span id="paper-agent-research-webgpt-13267288" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-cc127a045c60084f">WebGPT 为什么把浏览和来源支持纳入长篇问答，而不只让模型凭记忆作答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awebgpt">WebGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>开放问题常需要新信息或多个来源，纯参数回答可能缺少可核查依据。WebGPT 让模型通过浏览收集证据，再形成带引用的回答，并利用人类反馈评价质量。浏览获得的文本仍需正确理解，链接数量不能代替来源对具体结论的支持，也不保证覆盖所有重要事实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学例：比较两项政策需要分别找到原始说明，再解释差异；只在段末附一个相关网站，不能证明其中每个数字都有依据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2112.09332">原论文</a> · <a href="../../../../agent-research/2112.09332-webgpt/">实现解读</a> · <a href="#qa-cc127a045c60084f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:webgpt" data-paper-title="WebGPT" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="WebGPT Agent OpenAI 2021-12-17 长文本问答容易幻觉，且很难核查依据。WebGPT 让模型在文本浏览器里搜索、点击和滚动，回答必须收集引用；训练先做行为克隆，再用人类偏好 reward model 从多条浏览/回答轨迹中做拒绝采样。 本页复现文本浏览轨迹、证据引用和 reward-model 拒绝采样；本地确定性工具环境不是实时互联网浏览。保留 browser-action、citation constraint 和 trajectory rejection sampling；不访问实时网页、不训练 GPT-3/reward model，也不复刻 ELI5 人评。ScaleMCP mini 120 episodes、seed 42；每题生成两条工具轨迹，按证据覆盖选择。  浏览问答 Agent 工具与协作执行：把计划变成可检查的动作 带引用的浏览轨迹为什么还要经过人类偏好排序，而不只要求附上网址？ 网址存在不保证证据支持结论或回答满足问题，浏览过程与最终组织都需要质量判断。行为克隆先学习操作，再由偏好奖励选择较好轨迹；引用提供可核查入口，却不能让断章取义或未访问来源自动变可靠，仍需对应具体主张。 例如两段回答都贴了同一新闻链接，一段准确区分事件时间，另一段夸大结论；仅检查链接数量无法选出更好的答案。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-cb490f6e472d9e28">带引用的浏览轨迹为什么还要经过人类偏好排序，而不只要求附上网址？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awebgpt">WebGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>网址存在不保证证据支持结论或回答满足问题，浏览过程与最终组织都需要质量判断。行为克隆先学习操作，再由偏好奖励选择较好轨迹；引用提供可核查入口，却不能让断章取义或未访问来源自动变可靠，仍需对应具体主张。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两段回答都贴了同一新闻链接，一段准确区分事件时间，另一段夸大结论；仅检查链接数量无法选出更好的答案。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2112.09332">原论文</a> · <a href="../../../../agent-research/2112.09332-webgpt/">实现解读</a> · <a href="#qa-cb490f6e472d9e28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:webgpt" data-paper-title="WebGPT" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="WebGPT Agent OpenAI 2021-12-17 长文本问答容易幻觉，且很难核查依据。WebGPT 让模型在文本浏览器里搜索、点击和滚动，回答必须收集引用；训练先做行为克隆，再用人类偏好 reward model 从多条浏览/回答轨迹中做拒绝采样。 本页复现文本浏览轨迹、证据引用和 reward-model 拒绝采样；本地确定性工具环境不是实时互联网浏览。保留 browser-action、citation constraint 和 trajectory rejection sampling；不访问实时网页、不训练 GPT-3/reward model，也不复刻 ELI5 人评。ScaleMCP mini 120 episodes、seed 42；每题生成两条工具轨迹，按证据覆盖选择。  浏览问答 Agent 工具与协作执行：把计划变成可检查的动作 行为克隆与人类偏好 rejection sampling 分别起什么作用？ 行为克隆学习示范中的搜索、浏览和回答方式，偏好模型再对多条候选轨迹排序并选择。后者不自动生成新事实，也有 judge 偏差和多次采样成本；best-of-64 不能与单次输出忽略计算后直接比效率。 例如六十四条回答里选最好的一条提高偏好分，也确实支付了多轨迹浏览和生成成本，不能算成一次调用能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-849870cabbf2c4b0">行为克隆与人类偏好 rejection sampling 分别起什么作用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awebgpt">WebGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>行为克隆学习示范中的搜索、浏览和回答方式，偏好模型再对多条候选轨迹排序并选择。后者不自动生成新事实，也有 judge 偏差和多次采样成本；best-of-64 不能与单次输出忽略计算后直接比效率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如六十四条回答里选最好的一条提高偏好分，也确实支付了多轨迹浏览和生成成本，不能算成一次调用能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2112.09332">原论文</a> · <a href="../../../../agent-research/2112.09332-webgpt/">实现解读</a> · <a href="#qa-849870cabbf2c4b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:webgpt" data-paper-title="WebGPT" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/tools-and-collaboration" data-search="WebGPT Agent OpenAI 2021-12-17 长文本问答容易幻觉，且很难核查依据。WebGPT 让模型在文本浏览器里搜索、点击和滚动，回答必须收集引用；训练先做行为克隆，再用人类偏好 reward model 从多条浏览/回答轨迹中做拒绝采样。 本页复现文本浏览轨迹、证据引用和 reward-model 拒绝采样；本地确定性工具环境不是实时互联网浏览。保留 browser-action、citation constraint 和 trajectory rejection sampling；不访问实时网页、不训练 GPT-3/reward model，也不复刻 ELI5 人评。ScaleMCP mini 120 episodes、seed 42；每题生成两条工具轨迹，按证据覆盖选择。  浏览问答 Agent 工具与协作执行：把计划变成可检查的动作 本地两条轨迹按证据覆盖选择能等同实时网页与 reward model 吗？ 不能。本地保留浏览动作、引用约束和候选选择控制流，不访问实时网页、不训练 GPT-3 或人类偏好模型。证据覆盖是受控选择信号，不能改名成人评胜率、TruthfulQA 或真实网页事实核验成绩。 例如两条预设工具轨迹中选覆盖多的一条，可验证拒绝采样接口；没有真实页面和偏好模型就未复刻原完整系统。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 工具与协作执行：把计划变成可检查的动作</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f15afaaf211da371">本地两条轨迹按证据覆盖选择能等同实时网页与 reward model 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Awebgpt">WebGPT</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · OpenAI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。本地保留浏览动作、引用约束和候选选择控制流，不访问实时网页、不训练 GPT-3 或人类偏好模型。证据覆盖是受控选择信号，不能改名成人评胜率、TruthfulQA 或真实网页事实核验成绩。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条预设工具轨迹中选覆盖多的一条，可验证拒绝采样接口；没有真实页面和偏好模型就未复刻原完整系统。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2112.09332">原论文</a> · <a href="../../../../agent-research/2112.09332-webgpt/">实现解读</a> · <a href="#qa-f15afaaf211da371">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

模型已经有计划，怎样选择工具、解释返回值，并让多个角色共享可靠的执行状态？

## 记住这一点

工具调用需要完整契约：何时调用、参数是什么、返回值如何改变下一步、失败如何记录。Toolformer 用后续预测损失过滤有用的 API 调用；CRITIC 用外部工具反馈修订回答。协作系统在此基础上再分工、交接状态与核对产物。角色数量只是组织方式，真正起作用的是信息和责任怎样流动，以及工具是否实际执行。

## 一个例子

以修复一个仓库问题为例：检索角色定位代码，执行角色修改文件并运行测试，复核角色读取真实 diff 与测试输出。若执行超时，记录为超时，不把“已发出命令”写成成功。若测试报错来自环境，先区分环境故障与修复失败；让三个角色分别说“看起来正确”，并没有替代可执行检查。

## 什么时候要小心

工具返回是待验证的输入，可能过期、被注入或不完整。需要限制权限、保留失败与未知结果，避免重复执行有副作用的动作。当前库中的接口、候选调用过滤和小环境循环有各自复现边界；它们不自动构成完整浏览器、生产服务或软件工程 benchmark 能力。

## 先读这几篇

先读 Toolformer，理解调用何时有用；再读 CRITIC，观察工具证据怎样进入修订；最后读 SWE-agent，把单次调用扩展为有状态的仓库操作与测试循环。

1. [Toolformer](../../../agent-research/2302.04761-toolformer/README.md) · [原论文](https://arxiv.org/abs/2302.04761)
2. [CRITIC](../../../agent-research/2305.11738-critic/README.md) · [原论文](https://arxiv.org/abs/2305.11738)
3. [SWE-agent](../../../agent-research/2405.15793-swe-agent/README.md) · [原论文](https://arxiv.org/abs/2405.15793)

## 自测一下

一个角色生成补丁，另一个角色赞同，第三个角色宣告通过；没有任何测试执行记录，能算验证完成吗？

??? note "展开参考答案"

    不能。多角色共识仍可能共享同一个错误。应说明验收条件，实际执行相关检查并读取结果；未执行或中断的检查单独保留。若工具不允许执行，就把结论限制为静态审查，不能把角色对话计为测试通过。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
