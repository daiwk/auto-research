---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 按需决策：选择性推理、迁移与持续反馈

[结构化决策](index.md) / 子主题导学 · 约 3 分钟 · 4 张论文卡

## 先想一个问题

哪些请求值得追加推理，哪些反馈应该影响下一次选择？

## 记住这一点

Selective Reasoning 把是否启动推理、何时读取答案、何时接受并停止分成三个控制动作，以共享 reader 读取空前缀和推理中途的候选分布。Jev-DLC 在冻结 scorer 之上保留有界的动作记忆与修正方向，把 accept/revoke 反馈作用于之后的请求。迁移评测还要检验换语言和标签预算后是否仍成立。

## 一个例子

用户把上次的工具 A 改成 B，可作为后续相似请求的反馈，却不能在收到修正后回头把上次报成成功。另一个难题若需要推理，可中途读取候选分布并按预先确定的停止规则结束；“预算耗尽”应另记，不能冒充有把握的早停。

## 什么时候要小心

低熵只表示模型集中，并不等于答案正确，门控与阈值必须在评测前冻结。反馈序列要保持时间顺序；迁移和持续适配不能用未来标签。当前本地包含原测量统计复算或随机输入上的接口诊断，高成本完整模型链路未复现。

## 先读这几篇

先读 Selective Reasoning 的启动/读取/停止分工，理解单个请求内的预算；再读 Jev-DLC 的有界反馈状态与时间协议，理解请求之间的适配。然后看公共能力与跨语言迁移的边界。

1. [Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop](../../../system-one/2610.19644-selective-reasoning/README.md) · [原论文](https://arxiv.org/abs/2610.19644)
2. [Jev-DLC: Decision-Level Continual Learning from Typed Feedback](../../../system-one/2610.31521-jev-dlc/README.md) · [原论文](https://arxiv.org/abs/2610.31521v1)

## 自测一下

某题得到正确答案反馈后立刻更新并重答，能算持续学习带来的线上成功吗？

??? note "展开参考答案"

    不能。它已观察当前目标，不再是该题独立预测。应先记录本次原始选择和反馈，再只用更新后的状态评价之后尚未揭晓的请求，并与无反馈或固定策略作同序列比较。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 4 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Jev-DLC: Decision-Level Continual Learning from Typed Feedback 基础模型 The Hong Kong University of Science and Technology (Guangzhou) 2026-10-22 类型化决策能给出明确 accept 或 revoke(旧选择→新选择)。Jev-DLC 不把完整历史重新塞进模型，而是在冻结 scorer 上维护两个紧凑通道：保守通道记住重复动作的语义计数与局部方向；响应通道只存当前修正方向。反馈只能影响之后的请求，不能先看当前正确答案再报成功。 成本过高，不复现（审查 DONE）；三种子指标仅验证独立PA-I最小化参考、双通道/几何混合、反馈时序、硬掩码、revision和reset；外部给定随机logits/表示，不加载JEV、不生成任务答案。没有把1.0契约通过率标为模型准确率，也不根据合成反馈宣称能力提升。纯CPU路径无需CUDA回执。  System One / JEV 类型反馈与持续适配 结构化决策 按需决策：选择性推理、迁移与持续反馈">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<h2 id="paper-foundation-models-jev-dlc-8eed7f0b">Jev-DLC: Decision-Level Continual Learning from Typed Feedback</h2>
<p class="ar-learning-card__meta">The Hong Kong University of Science and Technology (Guangzhou) · 论文公开：2026-10-22</p>
<p><strong>方法要点：</strong>类型化决策能给出明确 accept 或 revoke(旧选择→新选择)。Jev-DLC 不把完整历史重新塞进模型，而是在冻结 scorer 上维护两个紧凑通道：保守通道记住重复动作的语义计数与局部方向；响应通道只存当前修正方向。反馈只能影响之后的请求，不能先看当前正确答案再报成功。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）；三种子指标仅验证独立PA-I最小化参考、双通道/几何混合、反馈时序、硬掩码、revision和reset；外部给定随机logits/表示，不加载JEV、不生成任务答案。没有把1.0契约通过率标为模型准确率，也不根据合成反馈宣称能力提升。纯CPU路径无需CUDA回执。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31521v1">原论文</a> · <a href="../../../../system-one/2610.31521-jev-dlc/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop 基础模型 University of Electronic Science and Technology of China 2026-10-14 Typed decision model 从明确候选中返回选择，适合 JEV / System One 式判断，但直接读出不一定足以完成多步推理。始终生成很长的推理又浪费算力。本论文在冻结 Qwen3.5-4B 上拟合共享 candidate-answer reader，让空推理前缀和中间推理前缀都能返回候选分布。控制器将三个问题分开：benefit gate 决定是否启动推理；从自然生成状态出发的 trigger 决定何时发起显式答案读取；归一化熵阈值决定是否接受当前候选并取消后续生成。 完整在线多策略实验为成本过高，不复现（审查 DONE）。本地完成的是固定原作者测量的 CPU 统计复核与不读取 gold 的控制器接口，不是 Qwen3.5-4B 在线能力复现。公开包不含原始 token trace / feature cache，不能据复算通过声称核实了 exact-prefix 关系。完整在线多策略实验为成本过高，不复现（审查 DONE）。本地对照口径：重算原作者公开 records.csv，以同题 / 同组配对、dataset / ProofWriter subtype 分层的 bootstrap 复核均值、差值、比值及pointwise区间。  System One / JEV 自适应推理与提前退出 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<h2 id="paper-foundation-models-selective-reasoning-8fcddd3e">Selective Reasoning for Typed Decision Models: When to Start, Read, and Stop</h2>
<p class="ar-learning-card__meta">University of Electronic Science and Technology of China · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>Typed decision model 从明确候选中返回选择，适合 JEV / System One 式判断，但直接读出不一定足以完成多步推理。始终生成很长的推理又浪费算力。本论文在冻结 Qwen3.5-4B 上拟合共享 candidate-answer reader，让空推理前缀和中间推理前缀都能返回候选分布。控制器将三个问题分开：benefit gate 决定是否启动推理；从自然生成状态出发的 trigger 决定何时发起显式答案读取；归一化熵阈值决定是否接受当前候选并取消后续生成。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整在线多策略实验为成本过高，不复现（审查 DONE）。本地完成的是固定原作者测量的 CPU 统计复核与不读取 gold 的控制器接口，不是 Qwen3.5-4B 在线能力复现。公开包不含原始 token trace / feature cache，不能据复算通过声称核实了 exact-prefix 关系。完整在线多策略实验为成本过高，不复现（审查 DONE）。本地对照口径：重算原作者公开 records.csv，以同题 / 同组配对、dataset / ProofWriter subtype 分层的 bootstrap 复核均值、差值、比值及pointwise区间。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19644">原论文</a> · <a href="../../../../system-one/2610.19644-selective-reasoning/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages 基础模型 Universitas Budi Luhur 2026-10-09 “输出概率校准良好”不等于“能可靠排序自己的错误”。本文在 NusaX 的 12 种语言和 NusaTranslation 的 7 种平行语言上，分别研究准确率、校准、错误排序、翻译和所需人工标签量。英语/印尼语和区域语言共享句子 ID，因此跨语言比较需要以句子为聚类单位，而不是把语言版本当独立样本。方法是先让低成本决策模型回答所有样本，再把低置信度的一部分交给本地分类器或 LLM。原作者以验证集宏 F1 选择最小路由比例，再冻结该比例评测测试集；不是在测试结果中挑最优点。本文不提出新的模型架构。 本地提供公开预测复算、15 等宽右闭区间 ECE、Brier、NLL、作者稳定排序 AURC、额外的置信度 tie-grouped AURC，以及按验证集宏 F1 选比例的级联。两个 AURC 的 tie 规则不同，因此名称分开。固定预测标签可能与公开四舍五入概率的 argmax 不一致；保留标签计算准确率，另报概率 argmax 准确率与不一致数量，校准/风险覆盖按作者概率 argmax 口径。  System One / JEV 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<h2 id="paper-foundation-models-jev-regional-transfer-a226a6c0">Does System One Transfer? Calibrated Typed-Decision Models, Label Budgets, and Translation for Indonesian Regional Languages</h2>
<p class="ar-learning-card__meta">Universitas Budi Luhur · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>“输出概率校准良好”不等于“能可靠排序自己的错误”。本文在 NusaX 的 12 种语言和 NusaTranslation 的 7 种平行语言上，分别研究准确率、校准、错误排序、翻译和所需人工标签量。英语/印尼语和区域语言共享句子 ID，因此跨语言比较需要以句子为聚类单位，而不是把语言版本当独立样本。方法是先让低成本决策模型回答所有样本，再把低置信度的一部分交给本地分类器或 LLM。原作者以验证集宏 F1 选择最小路由比例，再冻结该比例评测测试集；不是在测试结果中挑最优点。本文不提出新的模型架构。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地提供公开预测复算、15 等宽右闭区间 ECE、Brier、NLL、作者稳定排序 AURC、额外的置信度 tie-grouped AURC，以及按验证集宏 F1 选比例的级联。两个 AURC 的 tie 规则不同，因此名称分开。固定预测标签可能与公开四舍五入概率的 argmax 不一致；保留标签计算准确率，另报概率 argmax 准确率与不一致数量，校准/风险覆盖按作者概率 argmax 口径。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14112">原论文</a> · <a href="../../../../system-one/2610.14112-regional-transfer/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="system-one" data-topic="system-one/adaptive-decisions" data-search="Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks 基础模型 Dalian Maritime University 2026-10-08 论文用有限候选选择评估 Jev 的知识、推理和多语言能力。每题只提交问题与候选，运行一次；数学任务表现弱于知识任务。原文中的供应商分数与作者实测并非统一提示协议，本地实现因此分别记录，不混成可比排名。本文是评测研究，不提供新架构或训练目标。 规范化的 13 种 schema、候选排列、标签隔离、文件哈希和引用 / 实测分离已有行为测试。2026-10-10 在 A100 上使用固定 NanoJev checkpoint 对 ARC-Challenge 官方全部 1,172 道 test 题执行一次，327 题正确，准确率 27.90%，Wilson 95% 区间 25.41%–30.54%；没有用测试题训练、选参或重试。数据与 checkpoint revision 见脱敏 GPU 证据。该结果仅对应开放 NanoJev，不是论文闭源 Jev 的 97.6%。  System One / JEV 公共评测与能力边界 结构化决策 按需决策：选择性推理、迁移与持续反馈">
<p class="ar-learning-card__domain"><a href="./">结构化决策 / 按需决策：选择性推理、迁移与持续反馈</a></p>
<h2 id="paper-foundation-models-jev-capability-899cdbd2">Specialized Decision Models vs. General-Purpose LLMs: Benchmarking Jev Across Knowledge, Reasoning, and Multilingual Tasks</h2>
<p class="ar-learning-card__meta">Dalian Maritime University · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>论文用有限候选选择评估 Jev 的知识、推理和多语言能力。每题只提交问题与候选，运行一次；数学任务表现弱于知识任务。原文中的供应商分数与作者实测并非统一提示协议，本地实现因此分别记录，不混成可比排名。本文是评测研究，不提供新架构或训练目标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>规范化的 13 种 schema、候选排列、标签隔离、文件哈希和引用 / 实测分离已有行为测试。2026-10-10 在 A100 上使用固定 NanoJev checkpoint 对 ARC-Challenge 官方全部 1,172 道 test 题执行一次，327 题正确，准确率 27.90%，Wilson 95% 区间 25.41%–30.54%；没有用测试题训练、选参或重试。数据与 checkpoint revision 见脱敏 GPU 证据。该结果仅对应开放 NanoJev，不是论文闭源 Jev 的 97.6%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11978">原论文</a> · <a href="../../../../system-one/2610.11978-jev-capability/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
