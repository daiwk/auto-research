---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 生成式召回与推理推荐

[搜广推](index.md) / 子主题导学 · 约 3 分钟 · 60 张论文卡

## 先想一个问题

把物品改写成token后，推荐究竟改变了哪一步？

## 记住这一点

生成式召回把候选选择改为在用户上下文下生成物品码：先建立可还原到目录的标识，再学习码序列分布，最后用约束解码得到可服务物品。TIGER串起量化与自回归检索，COBRA进一步级联稀疏码和稠密表示，PLUM把推荐数据继续预训练接到已有语言模型。偏好优化与推理token是在这条链路上改变训练或搜索。

## 一个例子

目录里只有代码(3,7)和(3,9)，模型却给(3,5)很高概率。即使生成文本看起来合理，这也不是有效商品；解码必须服从目录约束。若两个商品共享同一码，还要处理碰撞或保留后续区分路径。

## 什么时候要小心

token loss下降不等于Recall提高，增加beam也不能恢复被错误码本或前缀约束排除的物品。部分论文同时生成列表，归组看主要生成机制，列表价值可接着读重排主题；本地缩小训练不等同于复现生产规模。

## 先读这几篇

按TIGER的离散ID生成→COBRA的稀疏—稠密级联→PLUM的已有LLM继续预训练阅读；这三篇有实际本地核心链路，但TIGER和PLUM的本地结果并未验证最终召回提升。

1. [Recommender Systems with Generative Retrieval](../../../reproductions/2305.05065-tiger/README.md) · [原论文](https://arxiv.org/abs/2305.05065)
2. [Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations](../../../reproductions/2503.02453-cobra/README.md) · [原论文](https://arxiv.org/abs/2503.02453)
3. [PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations](../../../reproductions/2510.07784-plum/README.md) · [原论文](https://arxiv.org/abs/2510.07784)

## 自测一下

模型能生成格式正确的三层SID，为什么仍可能没有有效召回？

??? note "展开参考答案"

    格式正确只保证长度和词表合法；组合可能不在目录中，也可能对应多个物品或错误兴趣。还需检查目录可达性、碰撞消解，以及隔离测试集上的候选覆盖和排序质量。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 60 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models 搜广推与 LLM 应用 Kuaishou Technology 2026-10-22 推荐FRM的显式CoT会增加生成时延，也可能过度思考或被固定推理模板带偏。OneLatent先用探索、评价、归因三视角生成自适应教师监督，再学习三个潜在token接口，最后只生成三层语义ID，避免在线输出长推理文本。 成本过高，不复现（审查 DONE），不下载235B教师、不做56卡训练的缩小替身、不自动重试因此本项是资料与成本审查完成，没有本地模型、诊断proxy、benchmark指标、GPU回执或evolve映射。Appendix A.1原配置为7节点×每节点8GPU，即56GPU、全参数BF16、4096tokens、两有效epochs；监督涉及Qwen3-235B-A22B教师及工业数据。单张A100/A30或Mac不适合照搬完整矩阵，本轮不先下载/试跑来验证它昂贵。  大模型能力与推荐融合 潜在推理与生成式推荐 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-onelatent-08691361">OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-10-22</p>
<p><strong>方法要点：</strong>推荐FRM的显式CoT会增加生成时延，也可能过度思考或被固定推理模板带偏。OneLatent先用探索、评价、归因三视角生成自适应教师监督，再学习三个潜在token接口，最后只生成三层语义ID，避免在线输出长推理文本。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE），不下载235B教师、不做56卡训练的缩小替身、不自动重试因此本项是资料与成本审查完成，没有本地模型、诊断proxy、benchmark指标、GPU回执或evolve映射。Appendix A.1原配置为7节点×每节点8GPU，即56GPU、全参数BF16、4096tokens、两有效epochs；监督涉及Qwen3-235B-A22B教师及工业数据。单张A100/A30或Mac不适合照搬完整矩阵，本轮不先下载/试跑来验证它昂贵。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30675v1">原论文</a> · <a href="../../../../recommendation-components/2610.30675-onelatent/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs 搜广推与 LLM 应用 University of Electronic Science and Technology of China 2026-10-20 同一用户长历史中，有用证据随已生成SID前缀而变；热门前缀的交互负载还会压倒其他分支。SPAR由三部分组成：按前缀检索粗到细记忆的PATH、冻结残差码本后的RQ-PIB负载修复，以及SFT+DPO偏好对齐。本地只实现第二部分的修复子程序，不拿字典或K-means冒充整个推荐模型。 完整生产训练与A/B成本过高，不复现（审查 DONE）。已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；没有实现PATH Decoder、RQ训练或偏好训练。完整生产训练与A/B成本过高，不复现（审查 DONE）。输入必须提供冻结码中心、残差、分配、训练期权重和父前缀。算法实现Eq13–15/Algorithm1的分支修复，以独立构造验证最小可行移动、空分支目的地、重商品上界、总负载守恒、至多一次移动和“不修复则超载”的负对照。合成权重不是推荐指标，也不能说明未来曝光更公平。  生成式推荐 前缀负载平衡 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-spar-prefix-balance-335a990d">SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs</h2>
<p class="ar-learning-card__meta">University of Electronic Science and Technology of China · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>同一用户长历史中，有用证据随已生成SID前缀而变；热门前缀的交互负载还会压倒其他分支。SPAR由三部分组成：按前缀检索粗到细记忆的PATH、冻结残差码本后的RQ-PIB负载修复，以及SFT+DPO偏好对齐。本地只实现第二部分的修复子程序，不拿字典或K-means冒充整个推荐模型。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整生产训练与A/B成本过高，不复现（审查 DONE）。已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；已实现RQ-PIB的冻结码本修复阶段，仅L1机制诊断；没有实现PATH Decoder、RQ训练或偏好训练。完整生产训练与A/B成本过高，不复现（审查 DONE）。输入必须提供冻结码中心、残差、分配、训练期权重和父前缀。算法实现Eq13–15/Algorithm1的分支修复，以独立构造验证最小可行移动、空分支目的地、重商品上界、总负载守恒、至多一次移动和“不修复则超载”的负对照。合成权重不是推荐指标，也不能说明未来曝光更公平。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.27898v1">原论文</a> · <a href="../../../../recommendation-components/2610.27898-spar-prefix-balance/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-10-12 生成式推荐尚未生成目标商品时无法读取其侧信息，导致逐级生成与最终排序同时缺少商品属性。TacGR在每级语义码之前预测连续侧信息并做解码器内交叉，同时用辅助排序塔防止回归目标坍塌、单向掩码隔离预测噪声。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：24.2亿私有样本、646万用户、753万商品；8层512维GQA/SwiGLU-MoE解码器，64专家top-2、序列长度1024。数据不可用，原规模训练超出单卡A100/A30或Mac预算；没有实测本地耗时，不用昂贵试跑估算。  generative-recommendation target-side-feature multitask-ranking 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-unisgr-v2-08304e35">UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation</h2>
<p class="ar-learning-card__meta">Alibaba International Digital Commerce Group · 论文公开：2026-10-12</p>
<p><strong>方法要点：</strong>生成式推荐尚未生成目标商品时无法读取其侧信息，导致逐级生成与最终排序同时缺少商品属性。TacGR在每级语义码之前预测连续侧信息并做解码器内交叉，同时用辅助排序塔防止回归目标坍塌、单向掩码隔离预测噪声。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：24.2亿私有样本、646万用户、753万商品；8层512维GQA/SwiGLU-MoE解码器，64专家top-2、序列长度1024。数据不可用，原规模训练超出单卡A100/A30或Mac预算；没有实测本地耗时，不用昂贵试跑估算。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16132">原论文</a> · <a href="../../../../reproductions/2610.16132-unisgr-v2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat 搜广推与 LLM 应用 WeChat E-commerce Search team（正文未单列作者机构） 2026-10-12 WeGR 联合优化协同语义编码和生成检索偏好：CoCo-VAE 让连续表示学习查询—商品与商品—商品共现，刷新低使用率码字，并用残差保真和跨样本碰撞损失改善码本利用率。DHPO 从短 SID 前缀逐步扩展到完整 SID，同时扩展奖励匹配和策略梯度范围，以多正例 SFT 稳定稀疏奖励下的训练。 三种子只是有界机制诊断，稳定相对提升不适用。本地对照口径：基线为 SFT 和完整 SID GRPO+MSFT，实验组为动态 horizon DHPO+MSFT；共用同一 CoCo-VAE 和 SFT 初始化。三种子只是有界机制诊断，稳定相对提升不适用。  generative-recommendation semantic-id preference-optimization 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-wegr-8c03ebb0">WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat</h2>
<p class="ar-learning-card__meta">WeChat E-commerce Search team（正文未单列作者机构） · 论文公开：2026-10-12</p>
<p><strong>方法要点：</strong>WeGR 联合优化协同语义编码和生成检索偏好：CoCo-VAE 让连续表示学习查询—商品与商品—商品共现，刷新低使用率码字，并用残差保真和跨样本碰撞损失改善码本利用率。DHPO 从短 SID 前缀逐步扩展到完整 SID，同时扩展奖励匹配和策略梯度范围，以多正例 SFT 稳定稀疏奖励下的训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>三种子只是有界机制诊断，稳定相对提升不适用。本地对照口径：基线为 SFT 和完整 SID GRPO+MSFT，实验组为动态 horizon DHPO+MSFT；共用同一 CoCo-VAE 和 SFT 初始化。三种子只是有界机制诊断，稳定相对提升不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.16979">原论文</a> · <a href="../../../../reproductions/2610.16979-wegr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative End-to-end Ad Retrieval at Douyin 搜广推与 LLM 应用 ByteDance 2026-09-30 GEAR 用正交基参数化 BasisVQ/BasisRQ，使码本更新具有全局共享和稳定旋转；生成器输出层级 token，碰撞 item 再由上下文条件 reranker 精排。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  ad-retrieval generative-retrieval semantic-id 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-gear-42599d59">Generative End-to-end Ad Retrieval at Douyin</h2>
<p class="ar-learning-card__meta">ByteDance · 论文公开：2026-09-30</p>
<p><strong>方法要点：</strong>GEAR 用正交基参数化 BasisVQ/BasisRQ，使码本更新具有全局共享和稳定旋转；生成器输出层级 token，碰撞 item 再由上下文条件 reranker 精排。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。执行 BasisVQ、前缀残差量化接口与碰撞 rerank；不复刻流式 PS、分钟级索引和线上流量，不把本地随机张量作为广告效果。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.39327">原论文</a> · <a href="../../../../reproductions/2609.39327-gear/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GRP v0.1 Technical Report 搜广推与 LLM 应用 Snap Inc. 2026-09-29 GRP 不是一次性替换成熟推荐漏斗，而是逐步把统一生成模型作为召回源接入，再替换弱源、增加配额并逐步绕过排序器。模型用 encoder-decoder 生成多模态 Semantic ID；MHP 通过 stop-gradient 路径联合学习排序，之后冻结为 RL reward。mGRPO 在 GRPO 上增加以 logged target 为锚点的单边 margin，只在策略开始牺牲原目标召回时惩罚。 复现级别：L1 架构与目标机制。复现级别：L1 架构与目标机制。本地实现独立 SID block mask、生成/排序梯度隔离和 mGRPO 单边召回保护；不宣称复现 Snap 线上效果。未包含 Snap 私有数据、Qwen3-VL SID tokenizer、生产尺度训练、CUDA graph serving、反向目录和在线流量，因此标记 concept_demo / l1_mechanism，不进入 Evolve 的效果提升证据池。本地对照口径：基线为不触发 logged-target 单边保护的同一 GRPO surrogate，实验组启用保护项；  generative-recommendation ranking rl-alignment 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-grp-12c5e416">GRP v0.1 Technical Report</h2>
<p class="ar-learning-card__meta">Snap Inc. · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>GRP 不是一次性替换成熟推荐漏斗，而是逐步把统一生成模型作为召回源接入，再替换弱源、增加配额并逐步绕过排序器。模型用 encoder-decoder 生成多模态 Semantic ID；MHP 通过 stop-gradient 路径联合学习排序，之后冻结为 RL reward。mGRPO 在 GRPO 上增加以 logged target 为锚点的单边 margin，只在策略开始牺牲原目标召回时惩罚。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 架构与目标机制。复现级别：L1 架构与目标机制。本地实现独立 SID block mask、生成/排序梯度隔离和 mGRPO 单边召回保护；不宣称复现 Snap 线上效果。未包含 Snap 私有数据、Qwen3-VL SID tokenizer、生产尺度训练、CUDA graph serving、反向目录和在线流量，因此标记 concept_demo / l1_mechanism，不进入 Evolve 的效果提升证据池。本地对照口径：基线为不触发 logged-target 单边保护的同一 GRPO surrogate，实验组启用保护项；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.36688">原论文</a> · <a href="../../../../reproductions/2609.36688-grp/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="X-Rec Technical Report 搜广推与 LLM 应用 TikTok (ByteDance) 2026-09-24 传统 U2I 召回将用户兴趣压缩为一个或少量向量，生成式语义 ID 方法则要逐 token 解码。X-Rec 直接在归一化 item embedding 球面上生成多个召回触发向量：先预测 item 所在的粗粒度聚类（anchor），再以该 anchor 为条件把球面噪声沿测地线流向目标 item。生成的向量与全量 item embedding 做近邻检索，可覆盖多个兴趣区域而无需语义 ID 量化。论文的另一个重点是计算结构：历史行为先经过前 L-1 层 Transformer； 未执行：TikTok 私有多属性日志与 streaming benchmark、工业 item encoder、ANN/在线 KV 服务、真实线上 A/B。Fidelity：核心机制复现；证据等级：L2 公开数据集。公开 MovieLens 任务只检验算法链路，不代表 TikTok 流量或论文绝对结果。当前是低预算机制实验；在 MovieLens-1M 上，X-Rec 的三种子均值低于 U2I，不能宣称收益。实际执行：item 对比学习、球面 anchor 聚类与 CE、测地线 RFM 监督、末层历史 K/V 复用、时间/anchor 调制、切空间速度、球面 Euler 和多 trigger 全目录检索。  retrieval generative-recommendation flow-matching 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-xrec-d9eceda3">X-Rec Technical Report</h2>
<p class="ar-learning-card__meta">TikTok (ByteDance) · 论文公开：2026-09-24</p>
<p><strong>方法要点：</strong>传统 U2I 召回将用户兴趣压缩为一个或少量向量，生成式语义 ID 方法则要逐 token 解码。X-Rec 直接在归一化 item embedding 球面上生成多个召回触发向量：先预测 item 所在的粗粒度聚类（anchor），再以该 anchor 为条件把球面噪声沿测地线流向目标 item。生成的向量与全量 item embedding 做近邻检索，可覆盖多个兴趣区域而无需语义 ID 量化。论文的另一个重点是计算结构：历史行为先经过前 L-1 层 Transformer；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>未执行：TikTok 私有多属性日志与 streaming benchmark、工业 item encoder、ANN/在线 KV 服务、真实线上 A/B。Fidelity：核心机制复现；证据等级：L2 公开数据集。公开 MovieLens 任务只检验算法链路，不代表 TikTok 流量或论文绝对结果。当前是低预算机制实验；在 MovieLens-1M 上，X-Rec 的三种子均值低于 U2I，不能宣称收益。实际执行：item 对比学习、球面 anchor 聚类与 CE、测地线 RFM 监督、末层历史 K/V 复用、时间/anchor 调制、切空间速度、球面 Euler 和多 trigger 全目录检索。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.29180">原论文</a> · <a href="../../../../reproductions/2609.29180-xrec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation 搜广推与 LLM 应用 Beihang University 2026-09-20 传统召回与排序分开优化，召回侧较难利用排序反馈；多层残差量化又可能逐层积累误差。UNIQUE 将物品先映射到一个扁平 code：物品向量由用户反馈监督的双塔编码，最近邻分配经使用频率校正，并用 EMA 更新码本。用户静态特征、近期行为、中期行为及兴趣摘要构成前缀；候选 item/code 各自只关注这一前缀，而不读取其他候选。共享的编码结果同时训练 code 分布和多个排序目标，推理时先按 code 提名，再对对应物品排序。 复现级别：公开数据缩比机制实验（概念验证）。复现级别：公开数据缩比机制实验（概念验证）。执行了反馈感知单层扁平量化、EMA 与频率平衡、用户多粒度前缀、目标注意力分离、code 生成与曝光排序联合训练；缺少百度生产特征、多目标头和在线基础设施，不能称为完整论文复现。仅用公开 item ID、标签、点击/长播与播放时长；没有百度的文本、发布者、细粒度反馈和多场景目标头。本地对照口径：同一早融合排序器、同数据和训练预算下，去掉联合 code 生成是基线，三 seed test CTR-AUC 均值约 0.5282；完整缩比实验组约 0.5270，相对 -0.23%。本地没有观察到稳定提升。  retrieval ranking generative-recommendation 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-unique-d194acb1">UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation</h2>
<p class="ar-learning-card__meta">Beihang University · 论文公开：2026-09-20</p>
<p><strong>方法要点：</strong>传统召回与排序分开优化，召回侧较难利用排序反馈；多层残差量化又可能逐层积累误差。UNIQUE 将物品先映射到一个扁平 code：物品向量由用户反馈监督的双塔编码，最近邻分配经使用频率校正，并用 EMA 更新码本。用户静态特征、近期行为、中期行为及兴趣摘要构成前缀；候选 item/code 各自只关注这一前缀，而不读取其他候选。共享的编码结果同时训练 code 分布和多个排序目标，推理时先按 code 提名，再对对应物品排序。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据缩比机制实验（概念验证）。复现级别：公开数据缩比机制实验（概念验证）。执行了反馈感知单层扁平量化、EMA 与频率平衡、用户多粒度前缀、目标注意力分离、code 生成与曝光排序联合训练；缺少百度生产特征、多目标头和在线基础设施，不能称为完整论文复现。仅用公开 item ID、标签、点击/长播与播放时长；没有百度的文本、发布者、细粒度反馈和多场景目标头。本地对照口径：同一早融合排序器、同数据和训练预算下，去掉联合 code 生成是基线，三 seed test CTR-AUC 均值约 0.5282；完整缩比实验组约 0.5270，相对 -0.23%。本地没有观察到稳定提升。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.23718">原论文</a> · <a href="../../../../reproductions/2609.23718-unique/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations 搜广推与 LLM 应用 Tencent 2026-09-16 以意图标识×摘要标识组织广告语义层次，用生成、判别和排序联合目标训练，并在请求侧动态约束 beam 只产生合法标识。 复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。  sponsored-search generative-retrieval hierarchical-identifiers 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-angle-c3d4b151">One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-09-16</p>
<p><strong>方法要点：</strong>以意图标识×摘要标识组织广告语义层次，用生成、判别和排序联合目标训练，并在请求侧动态约束 beam 只产生合法标识。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：公开数据核心机制。复现级别：公开数据核心机制。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地在 MovieLens 100K 执行层次标识、联合打分和受约束检索；不使用腾讯私有广告日志或生产索引。本地 seeds 42/43/44 见 metrics/movielens-100k-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.18296">原论文</a> · <a href="../../../../reproductions/2609.18296-angle/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning 搜广推与 LLM 应用 Tencent 2026-09-01 TGR 把工业推荐的三个方向纳入同一框架：CCFormer 承担可扩展排序，BARGE/HiGR 用分层语义 ID 生成单物品或整页列表，TGR-Reason 把离线生成的 reason token 注入在线解码，避免请求时再做昂贵 rollout。 复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现分层语义 ID 路径、列表目标和 reason-token 注入的组合。未复刻私有 semantic-ID catalog、生产 CCFormer checkpoint 与在线生成服务；仅实现公开数据可审计核心机制。MovieLens 100K 三 seed 固定协议下 NDCG@10 从 0.05401 提升到 0.05953。完整产物见 metrics/public-seeds42-44.json。  generative-recommendation ranking-network reason-token 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-tgr-d333ba35">TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-09-01</p>
<p><strong>方法要点：</strong>TGR 把工业推荐的三个方向纳入同一框架：CCFormer 承担可扩展排序，BARGE/HiGR 用分层语义 ID 生成单物品或整页列表，TGR-Reason 把离线生成的 reason token 注入在线解码，避免请求时再做昂贵 rollout。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制 + 公开数据。复现级别：核心机制 + 公开数据。复现分层语义 ID 路径、列表目标和 reason-token 注入的组合。未复刻私有 semantic-ID catalog、生产 CCFormer checkpoint 与在线生成服务；仅实现公开数据可审计核心机制。MovieLens 100K 三 seed 固定协议下 NDCG@10 从 0.05401 提升到 0.05953。完整产物见 metrics/public-seeds42-44.json。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.00986">原论文</a> · <a href="../../../../reproductions/2609.00986-tgr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising 搜广推与 LLM 应用 Kuaishou Technology 2026-08-25 直播间内容、商品和反馈高速变化，静态 semantic ID、单一时间尺度历史和离策略偏好优化都会过时。TAGR 在三层适配：LSID 周期刷新语义/协同分配但保持 token 词表稳定；IAG 融合短、中、长期意图；IOPO 间歇执行 on-policy GRPO，并在两次 burst 之间继续 NTP 维护，防止在线 RL 覆盖行为分布。 Fidelity：核心机制复现。本地执行稳定词表的可刷新 LSID、多尺度 intent 与行为/价值双分支；生产在线训练与广告系统未复刻。未使用快手私有日志、在线 reward model、真实 GRPO burst、广告价值标签和实时 serving；本地只验证三个核心适配结构及其在非时变公开数据上的失败边界。本地对照口径：基线为一阶转移与热度融合；实验组加入两级 LSID、三尺度 intent 和有界行为/价值门控。MovieLens-1M 上 NDCG@10 从 0.1123 降至 0.0821（-26.86%），但 head share 从 0.7275 降至 0.1303。  generative-recommendation live-streaming-advertising semantic-id online-rl 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-tagr-4f20f91f">TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-08-25</p>
<p><strong>方法要点：</strong>直播间内容、商品和反馈高速变化，静态 semantic ID、单一时间尺度历史和离策略偏好优化都会过时。TAGR 在三层适配：LSID 周期刷新语义/协同分配但保持 token 词表稳定；IAG 融合短、中、长期意图；IOPO 间歇执行 on-policy GRPO，并在两次 burst 之间继续 NTP 维护，防止在线 RL 覆盖行为分布。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。本地执行稳定词表的可刷新 LSID、多尺度 intent 与行为/价值双分支；生产在线训练与广告系统未复刻。未使用快手私有日志、在线 reward model、真实 GRPO burst、广告价值标签和实时 serving；本地只验证三个核心适配结构及其在非时变公开数据上的失败边界。本地对照口径：基线为一阶转移与热度融合；实验组加入两级 LSID、三尺度 intent 和有界行为/价值门控。MovieLens-1M 上 NDCG@10 从 0.1123 降至 0.0821（-26.86%），但 head share 从 0.7275 降至 0.1303。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.24034">原论文</a> · <a href="../../../../reproductions/2608.24034-tagr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sona Technical Report 搜广推与 LLM 应用 Yandex 2026-08-11 Yandex Music 原链路有 15 个以上候选生成器与独立预排、精排。Sona 用 chronology event encoder 表示用户，以历史压缩控制长序列成本，自回归生成 Semantic ID，并用同一状态的 Ranking Module 对物品排序；高容量 teacher 只在训练期提供蒸馏监督。 Fidelity：核心机制复现。实际训练压缩历史编码器、三层自回归 Semantic ID 头与 item ranker；本地负迁移如实保留。未复刻私有音乐语义 tokenizer、完整 teacher、15+ 生产候选源和智能音箱 serving；本地仅验证核心训练与推理数据流。本地对照口径：基线为同预算共享 encoder 排序器，实验组为 history compression + SID decoder + item ranker；NDCG@10 相对变化 -92.05%。  generative-recommendation semantic-id ranking history-compression 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-sona-74c5ab5b">Sona Technical Report</h2>
<p class="ar-learning-card__meta">Yandex · 论文公开：2026-08-11</p>
<p><strong>方法要点：</strong>Yandex Music 原链路有 15 个以上候选生成器与独立预排、精排。Sona 用 chronology event encoder 表示用户，以历史压缩控制长序列成本，自回归生成 Semantic ID，并用同一状态的 Ranking Module 对物品排序；高容量 teacher 只在训练期提供蒸馏监督。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。实际训练压缩历史编码器、三层自回归 Semantic ID 头与 item ranker；本地负迁移如实保留。未复刻私有音乐语义 tokenizer、完整 teacher、15+ 生产候选源和智能音箱 serving；本地仅验证核心训练与推理数据流。本地对照口径：基线为同预算共享 encoder 排序器，实验组为 history compression + SID decoder + item ranker；NDCG@10 相对变化 -92.05%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.11015">原论文</a> · <a href="../../../../reproductions/2608.11015-sona/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-08-08 先生成可服务的 Semantic ID，再按需生成可跳过的解释 copy；在线侧融合 SID 与 copy 表示，同时保留解释一致性。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation semantic-id llm-recommendation push 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-pushdualgen-379bfcda">PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-08-08</p>
<p><strong>方法要点：</strong>先生成可服务的 Semantic ID，再按需生成可跳过的解释 copy；在线侧融合 SID 与 copy 表示，同时保留解释一致性。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.07989">原论文</a> · <a href="../../../../reproductions/2608.07989-pushdualgen/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation 搜广推与 LLM 应用 Yandex 2026-08-06 Yandex 原系统包含 15 个以上召回器和独立预排/排序。Gryphon-v2 复用生成式推荐的共享 history encoder：生成头预测 Semantic ID，item-level ranking head 对生成候选直接排序；离线高容量 teacher 同时监督当前模型 rollout 和 logged impressions，从而让排序器见到 serving 分布与真实曝光分布。 Fidelity：核心机制复现。实现共享历史编码器、生成头、训练期 teacher、双来源 rollout 蒸馏与 item-level ranker；本地负结果如实保留。未复刻 Yandex 私有音乐/多模态 SID、8,000 长历史、十分钟在线更新和 Triton serving；公开数据只验证核心训练数据流。本地对照口径：基线为同预算生成式召回，实验组加入双来源蒸馏与 ranker；相对基线 NDCG@10 -26.84%。  generative-recommendation retrieval ranking rollout-distillation 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-gryphon-v2-65508cc1">Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation</h2>
<p class="ar-learning-card__meta">Yandex · 论文公开：2026-08-06</p>
<p><strong>方法要点：</strong>Yandex 原系统包含 15 个以上召回器和独立预排/排序。Gryphon-v2 复用生成式推荐的共享 history encoder：生成头预测 Semantic ID，item-level ranking head 对生成候选直接排序；离线高容量 teacher 同时监督当前模型 rollout 和 logged impressions，从而让排序器见到 serving 分布与真实曝光分布。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制复现。实现共享历史编码器、生成头、训练期 teacher、双来源 rollout 蒸馏与 item-level ranker；本地负结果如实保留。未复刻 Yandex 私有音乐/多模态 SID、8,000 长历史、十分钟在线更新和 Triton serving；公开数据只验证核心训练数据流。本地对照口径：基线为同预算生成式召回，实验组加入双来源蒸馏与 ranker；相对基线 NDCG@10 -26.84%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06213">原论文</a> · <a href="../../../../reproductions/2608.06213-gryphon-v2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Hierarchical Residual Policy Optimization for Generative Recommendations 搜广推与 LLM 应用 City University of Hong Kong / Kuaishou 2026-08-01 主题：生成式推荐后训练。最终物品回报直接广播给所有 SID token 会造成稀疏且高方差的信用。HRPO 在用户簇内平滑 prefix utility，再分解 residual token credit 并累积 credit-to-go，最后用 RRPO 做保守更新。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上构造二进制层级 SID，实际计算 prefix smoothing、residual credit 与 credit-to-go。  generative-recommendation reinforcement-learning semantic-id credit-assignment 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-hrpo-d54751e8">Hierarchical Residual Policy Optimization for Generative Recommendations</h2>
<p class="ar-learning-card__meta">City University of Hong Kong / Kuaishou · 论文公开：2026-08-01</p>
<p><strong>方法要点：</strong>主题：生成式推荐后训练。最终物品回报直接广播给所有 SID token 会造成稀疏且高方差的信用。HRPO 在用户簇内平滑 prefix utility，再分解 residual token credit 并累积 credit-to-go，最后用 RRPO 做保守更新。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。MovieLens-1M 上构造二进制层级 SID，实际计算 prefix smoothing、residual credit 与 credit-to-go。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.00750">原论文</a> · <a href="../../../../reproductions/2608.00750-hrpo/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation 搜广推与 LLM 应用 Huazhong Agricultural University (Kuaishou internship) 2026-07-30 从用户反馈发现生成策略，以双空间关系蒸馏把策略压入轻量排序器，从而避免线上调用 LLM。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation policy-optimization distillation 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-feedback-policy-7fbe9a73">From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation</h2>
<p class="ar-learning-card__meta">Huazhong Agricultural University (Kuaishou internship) · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>从用户反馈发现生成策略，以双空间关系蒸馏把策略压入轻量排序器，从而避免线上调用 LLM。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27789">原论文</a> · <a href="../../../../reproductions/2607.27789-feedback-policy/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LLM-Based Generative Retrieval for Snapchat Content Recommendation 搜广推与 LLM 应用 Snap Inc. 2026-07-30 先从共参与图传播内容相关性，再用分层残差量化形成 semantic ID；训练时把 SID token 与真实内容表征对齐，并学习用户序列到下一 SID 的生成转移。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为普通 residual SID，实验组加入共参与传播、grounding 与 SID transition；  retrieval generative-recommendation semantic-id llm multimodal 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-snaplgr-28d916e6">LLM-Based Generative Retrieval for Snapchat Content Recommendation</h2>
<p class="ar-learning-card__meta">Snap Inc. · 论文公开：2026-07-30</p>
<p><strong>方法要点：</strong>先从共参与图传播内容相关性，再用分层残差量化形成 semantic ID；训练时把 SID token 与真实内容表征对齐，并学习用户序列到下一 SID 的生成转移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线为普通 residual SID，实验组加入共参与传播、grounding 与 SID transition；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28895">原论文</a> · <a href="../../../../reproductions/2607.28895-snaplgr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Reward Guided Decoding for Generative Recommendation 搜广推与 LLM 应用 Institute of Information Engineering, Chinese Academy of Sciences 2026-07-28 保持生成器概率作为先验，在解码时用独立 reward 进行指数倾斜；闭式策略在提升期望 reward 的同时用 KL 温度限制偏离，无需重新训练生成器。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按生成器似然解码，实验组用内容/新颖度 reward 做 KL 正则倾斜；seed 42 的 NDCG@10 为 0.02249，基线为 0.05401，负结果保留。  generative-recommendation decoding reward business-alignment 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-reward-guided-decoding-a3100a32">Reward Guided Decoding for Generative Recommendation</h2>
<p class="ar-learning-card__meta">Institute of Information Engineering, Chinese Academy of Sciences · 论文公开：2026-07-28</p>
<p><strong>方法要点：</strong>保持生成器概率作为先验，在解码时用独立 reward 进行指数倾斜；闭式策略在提升期望 reward 的同时用 KL 温度限制偏离，无需重新训练生成器。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；生产模型、私有日志与服务基础设施明确列为边界，不用普通基线冒充完整工业系统。本地使用公开 MovieLens 特征或由其构造的可审计代理任务，不能复现论文公司的私有用户日志、线上流量分配、生产模型规模和 serving 栈。因此本页只把本地结果解释为机制级验证；不将其外推为论文线上 lift，也不声称与原文绝对指标可直接比较。本地对照口径：基线按生成器似然解码，实验组用内容/新颖度 reward 做 KL 正则倾斜；seed 42 的 NDCG@10 为 0.02249，基线为 0.05401，负结果保留。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.25344">原论文</a> · <a href="../../../../reproductions/2607.25344-reward-guided-decoding/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OxygenREC-v2: Internalizing Discrimination into Generative Recommendation 搜广推与 LLM 应用 JD.COM 2026-07-27 工业生成式推荐通常先生成候选，再外挂判别器或 reward model 重排；重排只能改变顺序，不能补回生成阶段漏掉的商品。OxygenREC-v2 把 click/cart/order 行为作为 decoder instruction，从第一枚 SID token 起控制候选生成；后训练再使用仅训练期可见的未来交互，联合可验证轨迹优化、自蒸馏和高熵位置的 forward-KL。 Fidelity: 核心机制复现。实际训练行为 instruction、行为加权目标、未来交互 privileged view 与熵路由蒸馏；生产模型和私有漏斗数据未复刻。这是核心机制的小规模复现，不含京东私有多行为日志、三层生产 SID、3B-A1B MoE 和线上服务。负结果主要说明“流行度分位”不是购买意图的可靠替代，不否定论文的私有数据结论。本地对照口径：基线与实验组使用同一 MovieLens 切片、full-catalog 候选、训练步数和 seed；实验组只增加论文机制，相对 NDCG@10 为 -54.09%。  generative-recommendation privileged-distillation behavior-instruction 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-oxygenrec-v2-987866fe">OxygenREC-v2: Internalizing Discrimination into Generative Recommendation</h2>
<p class="ar-learning-card__meta">JD.COM · 论文公开：2026-07-27</p>
<p><strong>方法要点：</strong>工业生成式推荐通常先生成候选，再外挂判别器或 reward model 重排；重排只能改变顺序，不能补回生成阶段漏掉的商品。OxygenREC-v2 把 click/cart/order 行为作为 decoder instruction，从第一枚 SID token 起控制候选生成；后训练再使用仅训练期可见的未来交互，联合可验证轨迹优化、自蒸馏和高熵位置的 forward-KL。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际训练行为 instruction、行为加权目标、未来交互 privileged view 与熵路由蒸馏；生产模型和私有漏斗数据未复刻。这是核心机制的小规模复现，不含京东私有多行为日志、三层生产 SID、3B-A1B MoE 和线上服务。负结果主要说明“流行度分位”不是购买意图的可靠替代，不否定论文的私有数据结论。本地对照口径：基线与实验组使用同一 MovieLens 切片、full-catalog 候选、训练步数和 seed；实验组只增加论文机制，相对 NDCG@10 为 -54.09%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24255">原论文</a> · <a href="../../../../reproductions/2607.24255-oxygenrec-v2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence 搜广推与 LLM 应用 Kuaishou / IIE, CAS / UCAS 2026-07-27 传统工业 cascade 分别训练 recall 和 ranking：两边重复编码用户历史，生成轨迹在候选交接时丢失，训练目标也可能冲突。UniR² 把用户上下文、目标物品 SID 轨迹和 item ranking features 拼成一个 decoder-only 异构序列，让生成轨迹成为召回与排序之间的表示桥。DQ-PCA 为同一层提供两种 query：generation query 只能读取完整用户 prefix 和此前 SID； 本地使用两级 16-way SID，而非三层 8129 codebook，也未运行 beam search、3×640 服务模型和流水线并行。Fidelity: 核心机制复现。实际训练层级 SID、Dual-Query Prefix-Causal Attention、ranking-only LoRA 和生成/排序联合目标；缩小 codebook、模型和业务标签。MovieLens next-item 与 genre-affinity 代理快手 click/long-view/gift；  generative-recommendation unified-recall-ranking multi-objective-ranking lora 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-unir2-b2b6f557">Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence</h2>
<p class="ar-learning-card__meta">Kuaishou / IIE, CAS / UCAS · 论文公开：2026-07-27</p>
<p><strong>方法要点：</strong>传统工业 cascade 分别训练 recall 和 ranking：两边重复编码用户历史，生成轨迹在候选交接时丢失，训练目标也可能冲突。UniR² 把用户上下文、目标物品 SID 轨迹和 item ranking features 拼成一个 decoder-only 异构序列，让生成轨迹成为召回与排序之间的表示桥。DQ-PCA 为同一层提供两种 query：generation query 只能读取完整用户 prefix 和此前 SID；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>本地使用两级 16-way SID，而非三层 8129 codebook，也未运行 beam search、3×640 服务模型和流水线并行。Fidelity: 核心机制复现。实际训练层级 SID、Dual-Query Prefix-Causal Attention、ranking-only LoRA 和生成/排序联合目标；缩小 codebook、模型和业务标签。MovieLens next-item 与 genre-affinity 代理快手 click/long-view/gift；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24439">原论文</a> · <a href="../../../../reproductions/2607.24439-unir2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="EGR: Embedding-Native Generative Retrieval with a Shared LLM 搜广推与 LLM 应用 Snap Inc. 2026-07-25 同一编码骨干产生 item 索引向量和 user query 向量，并让 item representation learning 与 next-item prediction 全程联合训练。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 EGR 为 0.05025，相对变化 -6.95%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。  retrieval generative-retrieval shared-encoder 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-egr-a66d7f0c">EGR: Embedding-Native Generative Retrieval with a Shared LLM</h2>
<p class="ar-learning-card__meta">Snap Inc. · 论文公开：2026-07-25</p>
<p><strong>方法要点：</strong>同一编码骨干产生 item 索引向量和 user query 向量，并让 item representation learning 与 next-item prediction 全程联合训练。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 EGR 为 0.05025，相对变化 -6.95%。这是公开代理任务的负结果，生产线上 lift 的外推不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.23038">原论文</a> · <a href="../../../../reproductions/2607.23038-egr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation 搜广推与 LLM 应用 Tencent 2026-07-23 RQ-VAE 把一个 item 展成多个 Semantic-ID token 后，普通 Transformer 会丢失 item 边界；单量化路径还会让早期 beam 偏差逐层放大。BARGE 用 ICA 将同一 item 的 token 聚合后门控回写，用 HPR 对累计语义路径做逐层对比重排，并通过正交切分产生两条互补解码路径。 Fidelity: 核心机制复现。实际训练 OSQ 双语义路径、ICA、HPR、双 decoder 与 item-space OR-fusion；缩小公开数据与服务规模。MovieLens genre 替代腾讯 item embedding；全库 teacher-forced path scoring 替代生产 beam kernel，未使用私有曝光负例和线上 serving。OSQ、ICA、HPR、DPD 均真实训练，但本地百分比不对应论文线上 lift。本地对照口径：基线是同 width、层数、训练行、optimizer 和 140 steps 的 single-path RQ-VAE/TIGER；  generative-recommendation semantic-id reranking 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-barge-1cfb2666">Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-07-23</p>
<p><strong>方法要点：</strong>RQ-VAE 把一个 item 展成多个 Semantic-ID token 后，普通 Transformer 会丢失 item 边界；单量化路径还会让早期 beam 偏差逐层放大。BARGE 用 ICA 将同一 item 的 token 聚合后门控回写，用 HPR 对累计语义路径做逐层对比重排，并通过正交切分产生两条互补解码路径。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际训练 OSQ 双语义路径、ICA、HPR、双 decoder 与 item-space OR-fusion；缩小公开数据与服务规模。MovieLens genre 替代腾讯 item embedding；全库 teacher-forced path scoring 替代生产 beam kernel，未使用私有曝光负例和线上 serving。OSQ、ICA、HPR、DPD 均真实训练，但本地百分比不对应论文线上 lift。本地对照口径：基线是同 width、层数、训练行、optimizer 和 140 steps 的 single-path RQ-VAE/TIGER；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.21028">原论文</a> · <a href="../../../../reproductions/2607.21028-barge/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="TSGR: Taobao Search Generative Retrieval 搜广推与 LLM 应用 Taobao &amp; Tmall Group of Alibaba / Zhejiang University 2026-07-21 淘宝搜索的生成式召回不仅要找到相关商品，还要把商业价值直接带进生成路径。TSGR 先用 residual quantization 生成语义前缀，再为同一前缀下的商品并行分配全局价值码和 query-conditioned 价值码；最后用与生成 backbone 联合训练的 Value-aware Ranking Module（VRM）完成精细排序，避免把独立预排器硬接在生成器后面。 复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行并行价值 Semantic ID 和联合 VRM；私有淘宝日志与生产 serving 未复刻。本地在 MovieLens 100K 上真实构建两级 residual semantic prefix、全局/条件价值码，并用 23,027 个加权正例和 115,135 个负例拟合联合 VRM；融合权重只在 validation 上选择。  generative-retrieval semantic-id search pre-ranking 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-tsgr-1abc60bc">TSGR: Taobao Search Generative Retrieval</h2>
<p class="ar-learning-card__meta">Taobao &amp; Tmall Group of Alibaba / Zhejiang University · 论文公开：2026-07-21</p>
<p><strong>方法要点：</strong>淘宝搜索的生成式召回不仅要找到相关商品，还要把商业价值直接带进生成路径。TSGR 先用 residual quantization 生成语义前缀，再为同一前缀下的商品并行分配全局价值码和 query-conditioned 价值码；最后用与生成 backbone 联合训练的 Value-aware Ranking Module（VRM）完成精细排序，避免把独立预排器硬接在生成器后面。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。真实执行并行价值 Semantic ID 和联合 VRM；私有淘宝日志与生产 serving 未复刻。本地在 MovieLens 100K 上真实构建两级 residual semantic prefix、全局/条件价值码，并用 23,027 个加权正例和 115,135 个负例拟合联合 VRM；融合权重只在 validation 上选择。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18796">原论文</a> · <a href="../../../../reproductions/2607.18796-tsgr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RecGPT-V3 Technical Report 搜广推与 LLM 应用 Alibaba / Taobao 2026-07-17 RecGPT-V1 把用户意图引入推荐链路，V2 用多智能体扩展推理，但每次请求仍重复读取最长约 55K token 的完整历史；自然语言 tag 到商品又形成有损瓶颈，显式 CoT 的数千 token 也无法承受高 QPS。V3 同时改造三处：Memory Hub 将完整行为压成带行为模式、偏好摘要、原始行为索引和时间信息的可追溯 memory unit；新行为只更新相关 unit 或创建新 unit。 Fidelity: 核心机制复现。实际训练两级 Semantic ID、结构化 Memory Hub、显式教师到 latent token 的重建蒸馏和 ranking-feedback；基础模型、数据与线上系统缩小。本地真实训练了两级 RQ-VAE、SID/text item tower、显式教师、memory attention、latent 多段重建和 dense ranking-feedback KL；MovieLens genre 替代淘宝文本/图像/属性，520 items 替代工业商品池，公开 teacher+popularity reward 替代生产 CTR ranker。  generative-recommendation semantic-id user-memory latent-reasoning 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-recgpt-v3-d1c7b19e">RecGPT-V3 Technical Report</h2>
<p class="ar-learning-card__meta">Alibaba / Taobao · 论文公开：2026-07-17</p>
<p><strong>方法要点：</strong>RecGPT-V1 把用户意图引入推荐链路，V2 用多智能体扩展推理，但每次请求仍重复读取最长约 55K token 的完整历史；自然语言 tag 到商品又形成有损瓶颈，显式 CoT 的数千 token 也无法承受高 QPS。V3 同时改造三处：Memory Hub 将完整行为压成带行为模式、偏好摘要、原始行为索引和时间信息的可追溯 memory unit；新行为只更新相关 unit 或创建新 unit。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实际训练两级 Semantic ID、结构化 Memory Hub、显式教师到 latent token 的重建蒸馏和 ranking-feedback；基础模型、数据与线上系统缩小。本地真实训练了两级 RQ-VAE、SID/text item tower、显式教师、memory attention、latent 多段重建和 dense ranking-feedback KL；MovieLens genre 替代淘宝文本/图像/属性，520 items 替代工业商品池，公开 teacher+popularity reward 替代生产 CTR ranker。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.15591">原论文</a> · <a href="../../../../reproductions/2607.15591-recgpt-v3/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap 搜广推与 LLM 应用 Amap / Alibaba 2026-07-13 把下一 POI 编成 Semantic ID 序列，并用时空特征、课程式预训练/SFT 与 EAKTO 强化优化长周期用户反馈。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-recommendation next-poi semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-guess-where-you-go-0a00ce9c">Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap</h2>
<p class="ar-learning-card__meta">Amap / Alibaba · 论文公开：2026-07-13</p>
<p><strong>方法要点：</strong>把下一 POI 编成 Semantic ID 序列，并用时空特征、课程式预训练/SFT 与 EAKTO 强化优化长周期用户反馈。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.26073">原论文</a> · <a href="../../../../reproductions/2607.26073-guess-where-you-go/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale 搜广推与 LLM 应用 Kuaishou / Beihang University 2026-06-24 用解耦语义 ID 连接生成式推荐与兴趣条件视频生成，并以跨域 reward 协调候选选择和内容创建。 Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 RaG 为 0.04235，相对变化 -21.59%。仅验证 D-SID 接口，视频生成器未复刻；生产线上 lift 的外推不适用。  generative-recommendation semantic-id video-generation 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-rag-generation-6f1ef070">Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale</h2>
<p class="ar-learning-card__meta">Kuaishou / Beihang University · 论文公开：2026-06-24</p>
<p><strong>方法要点：</strong>用解耦语义 ID 连接生成式推荐与兴趣条件视频生成，并以跨域 reward 协调候选选择和内容创建。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，不能复现论文公司的私有日志、线上分桶、生产模型规模和 serving 栈。因此本页只解释为核心机制级验证，不宣称复现原文绝对指标或线上增益。本地对照口径：同一全目录协议下，基线 NDCG@10 为 0.05401，实验组 RaG 为 0.04235，相对变化 -21.59%。仅验证 D-SID 接口，视频生成器未复刻；生产线上 lift 的外推不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.25496">原论文</a> · <a href="../../../../reproductions/2606.25496-rag-generation/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark 搜广推与 LLM 应用 University of Science and Technology of China / Alibaba 2026-05-25 将 query 与 item 共同序列化做生成式搜索，Linear HSTU 以线性复杂度编码历史，HFG-Attention 再融合稀疏交叉特征。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；  generative-search search-ranking long-sequence 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-qgs-de75c3ea">From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark</h2>
<p class="ar-learning-card__meta">University of Science and Technology of China / Alibaba · 论文公开：2026-05-25</p>
<p><strong>方法要点：</strong>将 query 与 item 共同序列化做生成式搜索，Linear HSTU 以线性复杂度编码历史，HFG-Attention 再融合稀疏交叉特征。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；公司私有特征、生产基础模型与在线流量不可公开，论文 A/B 数字仅作原文引用。本地实现执行了独立的模型状态和打分路径；它不是把论文名映射到同一个加权公式。未复刻项见 adapter 的 omitted_core_components，本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.25514">原论文</a> · <a href="../../../../reproductions/2605.25514-qgs/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search 搜广推与 LLM 应用 Alibaba Group / Taobao &amp; Tmall 2026-05-18 新品只按即时成交优化会持续缺曝光。GrowthGR 用 counterfactual ItemLTV 估计点击带来的长期订单增量，再以 RQ-VAE SID 和 decoder-only generator 召回；MoPO 联合购买、点击、曝光、排序和高 uplift 标签，并用 clipped inverse propensity 强化稀有高价值物品。 Fidelity: 核心机制复现。ItemLTV、三层 Semantic ID、NTP、MoPO/GRPO clipped update 与有效 SID 约束均实际执行。未来正反馈频次代理 7 日订单，公开数据不支持还原真实搜索漏斗和多模态商品 foundation embedding。本地对照口径：基线是同一 transition policy 的 NTP retrieval；实验组 GrowthGR 加入 ItemLTV 与 8 轮 MoPO，相对基线 Hit@10 +0.00%、NDCG@10 +2.05%。  generative-recommendation reinforcement-learning new-items 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-growthgr-aa9df061">Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search</h2>
<p class="ar-learning-card__meta">Alibaba Group / Taobao &amp; Tmall · 论文公开：2026-05-18</p>
<p><strong>方法要点：</strong>新品只按即时成交优化会持续缺曝光。GrowthGR 用 counterfactual ItemLTV 估计点击带来的长期订单增量，再以 RQ-VAE SID 和 decoder-only generator 召回；MoPO 联合购买、点击、曝光、排序和高 uplift 标签，并用 clipped inverse propensity 强化稀有高价值物品。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。ItemLTV、三层 Semantic ID、NTP、MoPO/GRPO clipped update 与有效 SID 约束均实际执行。未来正反馈频次代理 7 日订单，公开数据不支持还原真实搜索漏斗和多模态商品 foundation embedding。本地对照口径：基线是同一 transition policy 的 NTP retrieval；实验组 GrowthGR 加入 ItemLTV 与 8 轮 MoPO，相对基线 Hit@10 +0.00%、NDCG@10 +2.05%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.17994">原论文</a> · <a href="../../../../reproductions/2605.17994-growthgr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL 搜广推与 LLM 应用 Alibaba Taobao &amp; Tmall Group 2026-05-14 论文让首级 SID 服从商品类目，再用残差码表达类目内差异；Expert-Guided RL 组合点击、购买、语义与约束信号优化生成检索。 Fidelity: 核心机制复现。实现类目约束 Semantic ID、残差量化、多信号奖励和 EG-GRPO 更新。没有复刻 64-GPU 渐进训练、Tmall 私有 query log 和生产 beam service；EG-GRPO 更新本身真实执行。本地对照口径：基线是协同 item-ID 检索；实验组执行 CQ-SID 与 240 次 group-relative policy update；NDCG@10 相对 +1.66%。  generative-retrieval semantic-id reinforcement-learning 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-cq-sid-a55bb5d1">Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL</h2>
<p class="ar-learning-card__meta">Alibaba Taobao &amp; Tmall Group · 论文公开：2026-05-14</p>
<p><strong>方法要点：</strong>论文让首级 SID 服从商品类目，再用残差码表达类目内差异；Expert-Guided RL 组合点击、购买、语义与约束信号优化生成检索。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。实现类目约束 Semantic ID、残差量化、多信号奖励和 EG-GRPO 更新。没有复刻 64-GPU 渐进训练、Tmall 私有 query log 和生产 beam service；EG-GRPO 更新本身真实执行。本地对照口径：基线是协同 item-ID 检索；实验组执行 CQ-SID 与 240 次 group-relative policy update；NDCG@10 相对 +1.66%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.14434">原论文</a> · <a href="../../../../reproductions/2605.14434-cq-sid/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unified Value Alignment for Generative Recommendation in Industrial Advertising 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-05-07 传统生成式推荐主要优化用户行为匹配，却没有直接表示广告主的出价、ROI、优化目标等商业价值；工业广告还要求生成路径合法、满足请求级库存约束。UniVA 将“用户偏好、商业价值、可投放性”放进同一套生成式模型：Commercial SID 在语义 token 后编码商业属性；Generation-as-Ranking 用生成头和价值头联合给路径打分；eCPM-aware RL 让策略直接偏向请求内相对高价值广告；个性化 trie 则保证 beam 只沿当前请求可投放的广告路径展开。论文的三项关键改动是： Commercial token 的机制诊断是正向的：以相同前两级语义前缀分组，组内 bid proxy 的平均标准差由 0.34956 降至 0.09773（-72.04%）。Fidelity: 完整核心链路。本地实际执行 Commercial SID、HSTU 用户编码、cross-attention → causal self-attention 解码、MoR、共享专家 + top-k Sparse MoE、generation/value 双头、监督学习与 PPO/value 交替训练，以及 value-guided 个性化 trie beam search。  generative-advertising commercial-sid ppo value-aware-serving 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-univa-ad679aba">Unified Value Alignment for Generative Recommendation in Industrial Advertising</h2>
<p class="ar-learning-card__meta">Tencent / WeChat Channels · 论文公开：2026-05-07</p>
<p><strong>方法要点：</strong>传统生成式推荐主要优化用户行为匹配，却没有直接表示广告主的出价、ROI、优化目标等商业价值；工业广告还要求生成路径合法、满足请求级库存约束。UniVA 将“用户偏好、商业价值、可投放性”放进同一套生成式模型：Commercial SID 在语义 token 后编码商业属性；Generation-as-Ranking 用生成头和价值头联合给路径打分；eCPM-aware RL 让策略直接偏向请求内相对高价值广告；个性化 trie 则保证 beam 只沿当前请求可投放的广告路径展开。论文的三项关键改动是：</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Commercial token 的机制诊断是正向的：以相同前两级语义前缀分组，组内 bid proxy 的平均标准差由 0.34956 降至 0.09773（-72.04%）。Fidelity: 完整核心链路。本地实际执行 Commercial SID、HSTU 用户编码、cross-attention → causal self-attention 解码、MoR、共享专家 + top-k Sparse MoE、generation/value 双头、监督学习与 PPO/value 交替训练，以及 value-guided 个性化 trie beam search。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.05803">原论文</a> · <a href="../../../../reproductions/2605.05803-univa/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation 搜广推与 LLM 应用 JD.com 2026-04-16 逐 item 生成忽略同一页面内的互补和顺序。GenRec 将下一页作为序列目标，用非对称 Token Merger 压缩输入，并以 GRPO-SR 的组内 reward 优化整页，同时保留 NLL 正则抑制策略漂移。 复现保真度：核心机制复现。复现保真度：核心机制复现。Page-wise NTP、非对称 Token Merger 与 GRPO-SR/NLL 约束实际执行。把连续三个正反馈组成一页，联合估计 page policy，并用序位 reward advantage 更新、NLL policy 约束。  generative-recommendation grpo page-wise 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-genrec-e5f875fa">GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation</h2>
<p class="ar-learning-card__meta">JD.com · 论文公开：2026-04-16</p>
<p><strong>方法要点：</strong>逐 item 生成忽略同一页面内的互补和顺序。GenRec 将下一页作为序列目标，用非对称 Token Merger 压缩输入，并以 GRPO-SR 的组内 reward 优化整页，同时保留 NLL 正则抑制策略漂移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。Page-wise NTP、非对称 Token Merger 与 GRPO-SR/NLL 约束实际执行。把连续三个正反馈组成一页，联合估计 page policy，并用序位 reward advantage 更新、NLL policy 约束。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.14878">原论文</a> · <a href="../../../../reproductions/2604.14878-genrec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute 搜广推与 LLM 应用 Authors did not disclose affiliation / large-scale e-commerce platform 2026-04-14 在 SID 前生成品类、卖家和品牌等属性链，用容量受限量化抑制热点 token 塌缩，并以任务上下文稳定多场景生成。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 unirec-coa 核心机制，相对 NDCG@10 -4.93%。  generative-recommendation semantic-id preference-alignment 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-unirec-coa-7ee11184">UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute</h2>
<p class="ar-learning-card__meta">Authors did not disclose affiliation / large-scale e-commerce platform · 论文公开：2026-04-14</p>
<p><strong>方法要点：</strong>在 SID 前生成品类、卖家和品牌等属性链，用容量受限量化抑制热点 token 塌缩，并以任务上下文稳定多场景生成。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 unirec-coa 核心机制，相对 NDCG@10 -4.93%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.12234">原论文</a> · <a href="../../../../reproductions/2604.12234-unirec-coa/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="MBGR: Multi-Business Generative Recommendation 搜广推与 LLM 应用 Meituan 2026-04-03 多业务日志交错时，普通 next-item 监督只覆盖实际下一条业务。MBGR 用 business-conditioned autoencoder 保留 SID 语义，以共享 MoE 生成业务特定表示；LDR 在每个时刻为每个业务寻找最近未来交互，无标签业务被 mask。 Fidelity: 核心机制复现。Business-aware SID、共享 experts、逐业务预测与 Label Dynamic Routing 均实际执行。genre 是公开业务域代理，不能替代 Meituan 多业务私有日志与线上生成器规模。本地对照口径：基线是共享 next-item 模型；实验组 MBGR 用 genre 作为 19 个业务域并执行 BID/MBP/LDR，相对基线 Hit@10 -4.17%、NDCG@10 -5.92%。  generative-recommendation multi-domain semantic-id 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-mbgr-3a21e1da">MBGR: Multi-Business Generative Recommendation</h2>
<p class="ar-learning-card__meta">Meituan · 论文公开：2026-04-03</p>
<p><strong>方法要点：</strong>多业务日志交错时，普通 next-item 监督只覆盖实际下一条业务。MBGR 用 business-conditioned autoencoder 保留 SID 语义，以共享 MoE 生成业务特定表示；LDR 在每个时刻为每个业务寻找最近未来交互，无标签业务被 mask。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。Business-aware SID、共享 experts、逐业务预测与 Label Dynamic Routing 均实际执行。genre 是公开业务域代理，不能替代 Meituan 多业务私有日志与线上生成器规模。本地对照口径：基线是共享 next-item 模型；实验组 MBGR 用 genre 作为 19 个业务域并执行 BID/MBP/LDR，相对基线 Hit@10 -4.17%、NDCG@10 -5.92%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.02684">原论文</a> · <a href="../../../../reproductions/2604.02684-mbgr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation 搜广推与 LLM 应用 Alibaba International Digital Commerce Group 2026-03-30 RCLRec 从行为历史里选择与转化相关的短子序列，并按逆时间顺序作为 decoder 前缀。联合生成目标提供逐样本的中间监督，质量感知损失抑制无信息课程，缓解转化标签稀疏。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04768，相对变化 -11.71%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation conversion-modeling curriculum-learning 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-rclrec-bd92f42c">RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation</h2>
<p class="ar-learning-card__meta">Alibaba International Digital Commerce Group · 论文公开：2026-03-30</p>
<p><strong>方法要点：</strong>RCLRec 从行为历史里选择与转化相关的短子序列，并按逆时间顺序作为 decoder 前缀。联合生成目标提供逐样本的中间监督，质量感知损失抑制无信息课程，缓解转化标签稀疏。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.04768，相对变化 -11.71%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.28124">原论文</a> · <a href="../../../../reproductions/2603.28124-rclrec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation 搜广推与 LLM 应用 Taobao &amp; Tmall Group / Alibaba 2026-03-20 Direct 路径负责低时延，Reasoning 路径补足复杂意图；IL-GRPO 用线上 CTR 奖励优化整组 query，并采用离线/在线混合服务。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 aigq 核心机制，相对 NDCG@10 +8.09%。  query-recommendation generative-recommendation reinforcement-learning 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-aigq-4359f5f2">AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation</h2>
<p class="ar-learning-card__meta">Taobao &amp; Tmall Group / Alibaba · 论文公开：2026-03-20</p>
<p><strong>方法要点：</strong>Direct 路径负责低时延，Reasoning 路径补足复杂意图；IL-GRPO 用线上 CTR 奖励优化整组 query，并采用离线/在线混合服务。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 aigq 核心机制，相对 NDCG@10 +8.09%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.19710">原论文</a> · <a href="../../../../reproductions/2603.19710-aigq/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify 搜广推与 LLM 应用 Spotify 2026-03-18 纯近期序列容易只召回习惯内容。GLIDE 用 Semantic ID 自回归生成候选，同时把近期行为和长期用户 embedding 作为两类 prompt，兼顾即时意图与探索。 复现保真度：核心机制复现。复现保真度：核心机制复现。Residual Semantic ID、code 生成和双时间尺度 prompt 均实际执行。公开 item feature 做三级 residual quantization，以 code transition 生成并融合短期历史/长期内容画像。  generative-retrieval semantic-id soft-prompt 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-glide-1ae86d8e">Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify</h2>
<p class="ar-learning-card__meta">Spotify · 论文公开：2026-03-18</p>
<p><strong>方法要点：</strong>纯近期序列容易只召回习惯内容。GLIDE 用 Semantic ID 自回归生成候选，同时把近期行为和长期用户 embedding 作为两类 prompt，兼顾即时意图与探索。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>复现保真度：核心机制复现。复现保真度：核心机制复现。Residual Semantic ID、code 生成和双时间尺度 prompt 均实际执行。公开 item feature 做三级 residual quantization，以 code transition 生成并融合短期历史/长期内容画像。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.17540">原论文</a> · <a href="../../../../reproductions/2603.17540-glide/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation 搜广推与 LLM 应用 Tencent 2026-03-03 用 fake item token 统一生成、点击价值估计和广告排序，并通过分布一致性约束让生成概率与 value head 保持同一偏好。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 oneranker 核心机制；相对 NDCG@10 -7.65%。  advertising generative-recommendation ranking multi-task 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-oneranker-399e9549">OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-03-03</p>
<p><strong>方法要点：</strong>用 fake item token 统一生成、点击价值估计和广告排序，并通过分布一致性约束让生成概率与 value head 保持同一偏好。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 oneranker 核心机制；相对 NDCG@10 -7.65%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.02999">原论文</a> · <a href="../../../../reproductions/2603.02999-oneranker/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation 搜广推与 LLM 应用 Alibaba International / Wuhan University 2026-02-27 Semantic ID 自回归生成的早期错误会向后传播。GRC 把 draft SID、首错位置/属性一致性反思、corrected SID 串成结构化模板；再对完整轨迹做 GRPO，并用反思 token 熵把固定纠错预算分配给最不确定的 beam。 Fidelity: 核心机制复现。结构化 SFT、完整轨迹 GRPO 与 entropy-guided reflection scheduling 均实际执行。MovieLens genre 代理 category/seller/brand 属性；未复刻工业 LLM 参数量。本地对照口径：基线是同一 SID 的 GR backbone；实验组 GRC 加入 1,320 条结构化轨迹、10 轮 GRPO 与 EGRS，相对基线 Hit@10 -12.50%、NDCG@10 -11.12%。  generative-recommendation reinforcement-learning self-correction 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-grc-7f75523b">Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation</h2>
<p class="ar-learning-card__meta">Alibaba International / Wuhan University · 论文公开：2026-02-27</p>
<p><strong>方法要点：</strong>Semantic ID 自回归生成的早期错误会向后传播。GRC 把 draft SID、首错位置/属性一致性反思、corrected SID 串成结构化模板；再对完整轨迹做 GRPO，并用反思 token 熵把固定纠错预算分配给最不确定的 beam。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。结构化 SFT、完整轨迹 GRPO 与 entropy-guided reflection scheduling 均实际执行。MovieLens genre 代理 category/seller/brand 属性；未复刻工业 LLM 参数量。本地对照口径：基线是同一 SID 的 GR backbone；实验组 GRC 加入 1,320 条结构化轨迹、10 轮 GRPO 与 EGRS，相对基线 Hit@10 -12.50%、NDCG@10 -11.12%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.23639">原论文</a> · <a href="../../../../reproductions/2602.23639-grc/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Generative Recommendation for Large-Scale Advertising 搜广推与 LLM 应用 Kuaishou 2026-02-26 广告生成式推荐同时受商业语义、实时更新和延迟约束。GR4AD 用多粒度 UA-SID 编码广告，LazyAR 放松层间自回归依赖，VSL 按商业价值加权监督，RSPO 直接优化列表排序，Dynamic Beam Serving 随负载调整 beam。 Fidelity: 核心机制复现。UA-SID、并行 LazyAR、VSL、list-wise RSPO 均训练；私有多模态广告、eCPM、在线持续学习和动态 beam 服务未复刻。本地对照口径：统一跨模型基线是 DIN，GR4AD NDCG@10 相对 DIN +69.67%；内部 DLRM 基线加入 UA-SID/LazyAR/VSL/RSPO 后 +49.88%。两项都伴随 head share 0.505 的偏置风险。60 steps、180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval advertising reinforcement-learning serving 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-gr4ad-4d146b97">Generative Recommendation for Large-Scale Advertising</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2026-02-26</p>
<p><strong>方法要点：</strong>广告生成式推荐同时受商业语义、实时更新和延迟约束。GR4AD 用多粒度 UA-SID 编码广告，LazyAR 放松层间自回归依赖，VSL 按商业价值加权监督，RSPO 直接优化列表排序，Dynamic Beam Serving 随负载调整 beam。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。UA-SID、并行 LazyAR、VSL、list-wise RSPO 均训练；私有多模态广告、eCPM、在线持续学习和动态 beam 服务未复刻。本地对照口径：统一跨模型基线是 DIN，GR4AD NDCG@10 相对 DIN +69.67%；内部 DLRM 基线加入 UA-SID/LazyAR/VSL/RSPO 后 +49.88%。两项都伴随 head share 0.505 的偏置风险。60 steps、180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22732">原论文</a> · <a href="../../../../reproductions/2602.22732-gr4ad/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress 搜广推与 LLM 应用 Alibaba / AliExpress 2026-02-26 普通生成推荐只做 next-item，难以即时响应 Query、Category、Longtail、Discover、Season、Holiday 等业务任务。SIGMA 先通过搜索语义、视觉、世界知识和协同行为四类 relevance pair，把 LLM 语义与在线 ID embedding 对齐；随后用“短 SID prefix + unique item ID”同时保留生成效率和商品精度；七任务 instruction SFT 统一训练； 七任务分桶样本只有约 18/任务，逐任务数字只作诊断，不作结论。Fidelity: 完整核心链路。本地实际执行 causal-LM LoRA 多视角 InfoNCE+KD、RQ-SID prefix 与 unique ID 混合 token、七类 instruction SFT、SID-prefix NTP、同-prefix hard-negative InfoNCE、prefix beam→子目录 item retrieval→APF。不是用最终分数规则模拟 SIGMA。使用真实 SmolLM LoRA 编码与反向，不是固定 embedding 直接代替 multi-view grounding；  generative-recommendation multi-task-sft hybrid-token semantic-grounding 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-sigma-3e17a33a">SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress</h2>
<p class="ar-learning-card__meta">Alibaba / AliExpress · 论文公开：2026-02-26</p>
<p><strong>方法要点：</strong>普通生成推荐只做 next-item，难以即时响应 Query、Category、Longtail、Discover、Season、Holiday 等业务任务。SIGMA 先通过搜索语义、视觉、世界知识和协同行为四类 relevance pair，把 LLM 语义与在线 ID embedding 对齐；随后用“短 SID prefix + unique item ID”同时保留生成效率和商品精度；七任务 instruction SFT 统一训练；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>七任务分桶样本只有约 18/任务，逐任务数字只作诊断，不作结论。Fidelity: 完整核心链路。本地实际执行 causal-LM LoRA 多视角 InfoNCE+KD、RQ-SID prefix 与 unique ID 混合 token、七类 instruction SFT、SID-prefix NTP、同-prefix hard-negative InfoNCE、prefix beam→子目录 item retrieval→APF。不是用最终分数规则模拟 SIGMA。使用真实 SmolLM LoRA 编码与反向，不是固定 embedding 直接代替 multi-view grounding；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22913">原论文</a> · <a href="../../../../reproductions/2602.22913-sigma/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators 搜广推与 LLM 应用 Google 2026-02-26 生成式推荐常需要将解码限制在新鲜内容、库存或地域等合法 item 子集中。STATIC 将前缀树离线压成 CSR 迁移矩阵，浅层可用 dense lookup；每步在 GPU/TPU 上抽取合法候选，消除 CPU 指针追踪和设备往返。 成本过高，不复现（审查 DONE）：完整实验需要 TPU v6e、1B 模型及生产环境；本次实现 Algorithms 1/2 的独立 PyTorch 算子：CSR 离线构建、固定最大分支宽度的向量化 speculative gather、浅层 dense lookup、log-space 掩码、beam 父状态重排和显式 EOS。使用变长 ID 时必须保留 EOS，调用方需收集已结束 beam；不提供完整语言模型。  生成式推荐 约束解码与服务效率 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-static-constraint-decoding-c02cbeaf">Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators</h2>
<p class="ar-learning-card__meta">Google · 论文公开：2026-02-26</p>
<p><strong>方法要点：</strong>生成式推荐常需要将解码限制在新鲜内容、库存或地域等合法 item 子集中。STATIC 将前缀树离线压成 CSR 迁移矩阵，浅层可用 dense lookup；每步在 GPU/TPU 上抽取合法候选，消除 CPU 指针追踪和设备往返。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）：完整实验需要 TPU v6e、1B 模型及生产环境；本次实现 Algorithms 1/2 的独立 PyTorch 算子：CSR 离线构建、固定最大分支宽度的向量化 speculative gather、浅层 dense lookup、log-space 掩码、beam 父状态重排和显式 EOS。使用变长 ID 时必须保留 EOS，调用方需收集已结束 beam；不提供完整语言模型。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.22647">原论文</a> · <a href="../../../../recommendation-components/2602.22647-static-constraint-decoding/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following 搜广推与 LLM 应用 NetEase Cloud Music 2026-02-14 Climber-Pilot 用时间感知多物品预测把长周期、多物品消费前瞻蒸馏进单步生成模型；条件引导稀疏注意力在 attention 内注入类目和业务约束，无需额外过滤或多步推理。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.09251，相对变化 +71.29%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-retrieval long-horizon instruction-following 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-climber-pilot-a97c0a4c">Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following</h2>
<p class="ar-learning-card__meta">NetEase Cloud Music · 论文公开：2026-02-14</p>
<p><strong>方法要点：</strong>Climber-Pilot 用时间感知多物品预测把长周期、多物品消费前瞻蒸馏进单步生成模型；条件引导稀疏注意力在 attention 内注入类目和业务约束，无需额外过滤或多步推理。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.09251，相对变化 +71.29%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13581">原论文</a> · <a href="../../../../reproductions/2602.13581-climber-pilot/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems 搜广推与 LLM 应用 Forth AI / Shopee / Singapore University of Technology and Design 2026-02-13 先让 LLM 从上下文生成潜在 query，再用真实排序模型的 item 偏好构建正负 query，通过 RG-SFT 与 DPO 对齐 top-rank 意图。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rgalign-rec 核心机制，相对 NDCG@10 -14.03%。  llm-recommendation query-reasoning preference-alignment 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-rgalign-rec-56b59d1c">RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems</h2>
<p class="ar-learning-card__meta">Forth AI / Shopee / Singapore University of Technology and Design · 论文公开：2026-02-13</p>
<p><strong>方法要点：</strong>先让 LLM 从上下文生成潜在 query，再用真实排序模型的 item 偏好构建正负 query，通过 RG-SFT 与 DPO 对齐 top-rank 意图。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rgalign-rec 核心机制，相对 NDCG@10 -14.03%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.12968">原论文</a> · <a href="../../../../reproductions/2602.12968-rgalign-rec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning 搜广推与 LLM 应用 Beihang University 2026-02-13 RoleGen 让 LLM Reasoner 判断物品在转化轨迹中的功能角色，并通过反事实路径估计其工具性作用；候选再进入 SID 生成骨干，通过推理—执行—反馈—反思闭环迭代，降低休眠用户兴趣坍缩。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05605，相对变化 +3.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation counterfactual-reasoning dormant-users 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-rolegen-9ce78677">Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning</h2>
<p class="ar-learning-card__meta">Beihang University · 论文公开：2026-02-13</p>
<p><strong>方法要点：</strong>RoleGen 让 LLM Reasoner 判断物品在转化轨迹中的功能角色，并通过反事实路径估计其工具性作用；候选再进入 SID 生成骨干，通过推理—执行—反馈—反思闭环迭代，降低休眠用户兴趣坍缩。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens-1M 的公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05605，相对变化 +3.78%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.13134">原论文</a> · <a href="../../../../reproductions/2602.13134-rolegen/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage 搜广推与 LLM 应用 Tencent / WeChat Channels 2026-02-11 生成式推荐通常只从行为日志学习 next-item likelihood，难以理解用户为何偏好某个内容；直接把 LLM 放到在线链路又无法满足工业延迟。S-GRec 将 LLM 仅作为离线语义 judge：两阶段 Personalized Semantic Judge（PSJ）先输出可解释的方面证据，再学习每个用户的方面权重；轻量生成器线上只生成 Semantic ID，不依赖 LLM。论文的第二个问题是语义目标可能与收入目标冲突。 这是最大的数据保真度差异。Fidelity: 完整核心链路。本地实际执行 causal LLM LoRA judge、方面打分 SFT+GRPO、用户条件权重 pairwise GRPO、SID 自回归生成器、5% 稀疏 semantic sampling，以及从相同 SFT checkpoint 初始化的 Reward-Sum、Adv-Sum、A2PO。模型规模与数据规模缩小，腾讯私有人工广告标注和 eCPM 模型由公开 Office 行为与 Qwen embedding 构造的监督替代。Qwen3-4B PSJ 缩小为 SmolLM2-135M；  generative-recommendation llm-as-judge grpo a2po 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-s-grec-c5ba1bc0">S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage</h2>
<p class="ar-learning-card__meta">Tencent / WeChat Channels · 论文公开：2026-02-11</p>
<p><strong>方法要点：</strong>生成式推荐通常只从行为日志学习 next-item likelihood，难以理解用户为何偏好某个内容；直接把 LLM 放到在线链路又无法满足工业延迟。S-GRec 将 LLM 仅作为离线语义 judge：两阶段 Personalized Semantic Judge（PSJ）先输出可解释的方面证据，再学习每个用户的方面权重；轻量生成器线上只生成 Semantic ID，不依赖 LLM。论文的第二个问题是语义目标可能与收入目标冲突。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>这是最大的数据保真度差异。Fidelity: 完整核心链路。本地实际执行 causal LLM LoRA judge、方面打分 SFT+GRPO、用户条件权重 pairwise GRPO、SID 自回归生成器、5% 稀疏 semantic sampling，以及从相同 SFT checkpoint 初始化的 Reward-Sum、Adv-Sum、A2PO。模型规模与数据规模缩小，腾讯私有人工广告标注和 eCPM 模型由公开 Office 行为与 Qwen embedding 构造的监督替代。Qwen3-4B PSJ 缩小为 SmolLM2-135M；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.10606">原论文</a> · <a href="../../../../reproductions/2602.10606-s-grec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation 搜广推与 LLM 应用 Tencent 2026-02-10 Thinking Tokens 形成连续潜在意图，扩散去噪逐步修正冲突兴趣，GRPO 再把连续生成与离散排序奖励端到端对齐。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 diffureason 核心机制，相对 NDCG@10 -6.50%。  generative-recommendation diffusion reinforcement-learning 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-diffureason-5f379d3c">DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation</h2>
<p class="ar-learning-card__meta">Tencent · 论文公开：2026-02-10</p>
<p><strong>方法要点：</strong>Thinking Tokens 形成连续潜在意图，扩散去噪逐步修正冲突兴趣，GRPO 再把连续生成与离散排序奖励端到端对齐。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 diffureason 核心机制，相对 NDCG@10 -6.50%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.09744">原论文</a> · <a href="../../../../reproductions/2602.09744-diffureason/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment 搜广推与 LLM 应用 Apple 2026-02-01 先从可搜索目录检索补全证据，再以 SFT 和 DPO 同时对齐相关性、安全、参与度、目录/上下文 groundedness 与多样性。 保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rag-qac 核心机制，相对 NDCG@10 -4.48%。  query-auto-completion retrieval-augmented-generation preference-alignment 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-rag-qac-5e006d24">Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment</h2>
<p class="ar-learning-card__meta">Apple · 论文公开：2026-02-01</p>
<p><strong>方法要点：</strong>先从可搜索目录检索补全证据，再以 SFT 和 DPO 同时对齐相关性、安全、参与度、目录/上下文 groundedness 与多样性。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文线上结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 固定全库候选、相同切分和 seed 上执行论文核心机制；私有特征、生产基础模型和在线流量不可公开，论文 A/B 数字只作原文引用。本地实现拥有独立模型状态和打分路径；负结果同样保留，且本地相对变化不得与原文 A/B 提升混写。本地对照口径：基线为共享 transition + content scorer；实验组在同一用户、物品、全库候选和 seed 上只加入 rag-qac 核心机制，相对 NDCG@10 -4.48%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.01023">原论文</a> · <a href="../../../../reproductions/2602.01023-rag-qac/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce 搜广推与 LLM 应用 Kuaishou 2026-01-29 快手电商的商品卡、短视频和直播分发原本由不同链路维护。OneMall 用统一商品 Semantic ID、Query-Former 压缩、多行为 cross-attention、Sparse MoE 生成器及 RL 对齐，把多个场景收进一个生成推荐家族。 Fidelity: 核心机制复现。执行场景 prompt、三层 Semantic ID 和跨行为融合；缩小数据与模型规模。MovieLens genre 仅代理场景；未复刻快手私有商品特征、Sparse MoE、生产 RL 和线上 serving。本地对照口径：基线是共享 transition/content ensemble；实验组只增加场景 prompt、三层 residual SID 和跨行为融合，MovieLens-100K NDCG@10 0.03540→0.03693，相对 +4.33%，Hit@10 相对 -4.35%。  generative-recommendation multi-scenario semantic-id 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-onemall-15aa9dcd">OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2026-01-29</p>
<p><strong>方法要点：</strong>快手电商的商品卡、短视频和直播分发原本由不同链路维护。OneMall 用统一商品 Semantic ID、Query-Former 压缩、多行为 cross-attention、Sparse MoE 生成器及 RL 对齐，把多个场景收进一个生成推荐家族。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。执行场景 prompt、三层 Semantic ID 和跨行为融合；缩小数据与模型规模。MovieLens genre 仅代理场景；未复刻快手私有商品特征、Sparse MoE、生产 RL 和线上 serving。本地对照口径：基线是共享 transition/content ensemble；实验组只增加场景 prompt、三层 residual SID 和跨行为融合，MovieLens-100K NDCG@10 0.03540→0.03693，相对 +4.33%，Hit@10 相对 -4.35%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21770">原论文</a> · <a href="../../../../reproductions/2601.21770-onemall/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation 搜广推与 LLM 应用 Kuaishou Technology 2026-01-26 在每一级 SID 生成前插入可解释 thinking token，并让它与真实 codebook 分布对比学习；协同共现图和负载均衡共同改善由粗到细的语义层级。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05463，相对变化 +1.15%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation latent-reasoning semantic-id 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-s2gr-c72e2aca">S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-01-26</p>
<p><strong>方法要点：</strong>在每一级 SID 生成前插入可解释 thinking token，并让它与真实 codebook 分布对比学习；协同共现图和负载均衡共同改善由粗到细的语义层级。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05463，相对变化 +1.15%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.18664">原论文</a> · <a href="../../../../reproductions/2601.18664-s2gr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations 搜广推与 LLM 应用 Kuaishou Technology 2026-01-08 轻量 path-level PRM 在每个 SID 层级评价中间路径，训练时提供稠密反馈、推理时提前剪除已发生语义漂移的 beam；因此增加 beam width 能形成可控的 test-time scaling。 不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05929，相对变化 +9.79%。本地代理目标与论文生产任务不同，不能外推线上 lift。  generative-recommendation process-reward test-time-scaling 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-promise-c348f413">PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations</h2>
<p class="ar-learning-card__meta">Kuaishou Technology · 论文公开：2026-01-08</p>
<p><strong>方法要点：</strong>轻量 path-level PRM 在每个 SID 层级评价中间路径，训练时提供稠密反馈、推理时提前剪除已发生语义漂移的 beam；因此增加 beam width 能形成可控的 test-time scaling。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。Fidelity: 核心机制复现。本地代码执行论文最有辨识度、可由公开数据验证的机制；私有数据、生产模型与服务栈明确列为边界。本地使用 MovieLens 100K 的固定公开子集及可审计代理目标，只验证中心计算机制；不复现原论文的私有日志、生产基础模型、线上分桶和 serving 栈。因此本页不宣称复现原文绝对指标或线上增益。本地对照口径：同一 MovieLens 全目录协议下，基线 NDCG@10 为 0.05401，实验组为 0.05929，相对变化 +9.79%。本地代理目标与论文生产任务不同，不能外推线上 lift。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.04674">原论文</a> · <a href="../../../../reproductions/2601.04674-promise/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="DualGR: Generative Retrieval with Long and Short-Term Interests Modeling 搜广推与 LLM 应用 USTC / Kuaishou Technology 2025-11-16 短期兴趣与长期兴趣使用双路由器，约束 Semantic ID 前缀有效性，并以曝光感知项抑制头部坍缩。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dualgr 核心机制；相对 NDCG@10 +6.73%。  retrieval generative-recommendation semantic-id long-short-interest 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-dualgr-b1420088">DualGR: Generative Retrieval with Long and Short-Term Interests Modeling</h2>
<p class="ar-learning-card__meta">USTC / Kuaishou Technology · 论文公开：2025-11-16</p>
<p><strong>方法要点：</strong>短期兴趣与长期兴趣使用双路由器，约束 Semantic ID 前缀有效性，并以曝光感知项抑制头部坍缩。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 dualgr 核心机制；相对 NDCG@10 +6.73%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2511.12518">原论文</a> · <a href="../../../../reproductions/2511.12518-dualgr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations 搜广推与 LLM 应用 Google DeepMind / YouTube 2025-10-09 传统 large embedding model（LEM）把绝大多数参数放在千万级 ID embedding 表，神经网络容量反而很小，难以获得 LLM 式 scaling。PLUM 从 Gemini-1.5 MoE 初始化，把视频量化成 Semantic ID（SID），先用用户行为与视频文本/ASR/频道元数据做 continued pre-training（CPT），再以 next-SID generation 做生成式召回。线上用 beam search 直接生成候选 SID，不再维护点积检索索引。 LLM 初始化组在有无 CPT 时 Recall@10 都为 0，未复现论文中 LLM initialization 的增益。Fidelity: 完整核心链路复现。本地实际执行多层 RQ Semantic ID、预训练 decoder-only LM 的 CPT、next-SID SFT 和 token-level constrained beam search；只缩小模型/数据规模并替换私有模态。本地对照口径：基线是随机初始化无 CPT（R1），实验组是随机初始化有 CPT（CR1）；Recall@10 都是 0.0050（0.00%），但 SFT final loss 从 3.5023 降至 2.5933；   搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-plum-515f2ca7">PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations</h2>
<p class="ar-learning-card__meta">Google DeepMind / YouTube · 论文公开：2025-10-09</p>
<p><strong>方法要点：</strong>传统 large embedding model（LEM）把绝大多数参数放在千万级 ID embedding 表，神经网络容量反而很小，难以获得 LLM 式 scaling。PLUM 从 Gemini-1.5 MoE 初始化，把视频量化成 Semantic ID（SID），先用用户行为与视频文本/ASR/频道元数据做 continued pre-training（CPT），再以 next-SID generation 做生成式召回。线上用 beam search 直接生成候选 SID，不再维护点积检索索引。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>LLM 初始化组在有无 CPT 时 Recall@10 都为 0，未复现论文中 LLM initialization 的增益。Fidelity: 完整核心链路复现。本地实际执行多层 RQ Semantic ID、预训练 decoder-only LM 的 CPT、next-SID SFT 和 token-level constrained beam search；只缩小模型/数据规模并替换私有模态。本地对照口径：基线是随机初始化无 CPT（R1），实验组是随机初始化有 CPT（CR1）；Recall@10 都是 0.0050（0.00%），但 SFT final loss 从 3.5023 降至 2.5933；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2510.07784">原论文</a> · <a href="../../../../reproductions/2510.07784-plum/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="IntSR: An Integrated Generative Framework for Search and Recommendation 搜广推与 LLM 应用 Alibaba / Amap 2025-09-25 用显式查询和隐式会话意图共同生成 POI/物品，统一搜索与推荐词表，并加入时间上下文刻画意图漂移。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 intsr 核心机制；相对 NDCG@10 +33.56%。  search recommendation generative-retrieval content-understanding 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-intsr-9d48eca1">IntSR: An Integrated Generative Framework for Search and Recommendation</h2>
<p class="ar-learning-card__meta">Alibaba / Amap · 论文公开：2025-09-25</p>
<p><strong>方法要点：</strong>用显式查询和隐式会话意图共同生成 POI/物品，统一搜索与推荐词表，并加入时间上下文刻画意图漂移。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为共享 transition + content scorer，实验组只加入 intsr 核心机制；相对 NDCG@10 +33.56%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2509.21179">原论文</a> · <a href="../../../../reproductions/2509.21179-intsr/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec-V2 Technical Report 搜广推与 LLM 应用 Kuaishou 2025-08-28 OneRec-V1 用 encoder-decoder 生成推荐 session，但长历史 encoder 重复计算，偏好对齐又依赖额外 reward model。V2 只把最新曝光作为监督目标；Context Processor 一次生成所有 decoder 层共享的 K/V，目标侧只解码 [BOS,s1,s2]→[s1,s2,s3]。Lazy block 依次执行 cross-attention、causal self-attention 和 FFN，并结合 GQA、K=V、跨层 KV sharing。 Fidelity: 完整核心链路复现。实际训练三层 residual-quantized Semantic ID、newest-impression SFT、layer-shared K/V Lazy Decoder、Duration-Aware Reward Shaping 和 GBPO；仅缩小模型/数据，省略私有异构特征与分布式 serving。本地对照口径：效率基线是 Encoder-Decoder，实验组 Lazy SFT 的延迟 -54.78%、validation loss -0.34%；对齐基线是 Lazy SFT，加入 GBPO 后反馈加权概率 +21.66%。  llm-recommendation generative-retrieval reinforcement-learning 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-onerec-v2-8a1036e5">OneRec-V2 Technical Report</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2025-08-28</p>
<p><strong>方法要点：</strong>OneRec-V1 用 encoder-decoder 生成推荐 session，但长历史 encoder 重复计算，偏好对齐又依赖额外 reward model。V2 只把最新曝光作为监督目标；Context Processor 一次生成所有 decoder 层共享的 K/V，目标侧只解码 [BOS,s1,s2]→[s1,s2,s3]。Lazy block 依次执行 cross-attention、causal self-attention 和 FFN，并结合 GQA、K=V、跨层 KV sharing。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。实际训练三层 residual-quantized Semantic ID、newest-impression SFT、layer-shared K/V Lazy Decoder、Duration-Aware Reward Shaping 和 GBPO；仅缩小模型/数据，省略私有异构特征与分布式 serving。本地对照口径：效率基线是 Encoder-Decoder，实验组 Lazy SFT 的延迟 -54.78%、validation loss -0.34%；对齐基线是 Lazy SFT，加入 GBPO 后反馈加权概率 +21.66%。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2508.20900">原论文</a> · <a href="../../../../reproductions/2508.20900-onerec-v2/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems 搜广推与 LLM 应用 Pinterest 2025-04-09 普通 next-item 只会延续用户最常见行为，且严格顺序不适合 feed session。PinRec 把期望 outcome 注入输出头，并在同一未来窗口一次生成多个 ANN-compatible item vectors。 Fidelity: 完整核心链路复现。真实执行因果 decoder、outcome embedding、归一化 ANN 输出、无序未来窗口 multi-token 对比学习；MovieLens 评分档位替代 Pinterest 多 surface action。本地对照口径：基线是 unconditioned next-token 模型；实验组是 outcome-conditioned 三 token window；Unordered Recall@10 -27.78%、NDCG@10 -34.82%。这是 outcome/multi-token 模块消融，不是相对 DIN。  generative-retrieval outcome-conditioning multi-token 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-pinrec-66bf0193">PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems</h2>
<p class="ar-learning-card__meta">Pinterest · 论文公开：2025-04-09</p>
<p><strong>方法要点：</strong>普通 next-item 只会延续用户最常见行为，且严格顺序不适合 feed session。PinRec 把期望 outcome 注入输出头，并在同一未来窗口一次生成多个 ANN-compatible item vectors。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。真实执行因果 decoder、outcome embedding、归一化 ANN 输出、无序未来窗口 multi-token 对比学习；MovieLens 评分档位替代 Pinterest 多 surface action。本地对照口径：基线是 unconditioned next-token 模型；实验组是 outcome-conditioned 三 token window；Unordered Recall@10 -27.78%、NDCG@10 -34.82%。这是 outcome/multi-token 模块消融，不是相对 DIN。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2504.10507">原论文</a> · <a href="../../../../reproductions/2504.10507-pinrec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations 搜广推与 LLM 应用 Baidu 2025-03-04 纯 Semantic ID 在量化阶段丢失细粒度信息。COBRA 先生成稀疏 code，再以 code 条件生成可端到端更新的 dense vector；推理先 beam 搜索 code，再用 dense 最近邻细排。 Fidelity: 完整核心链路复现。稀疏 S-ID、以 S-ID 为条件的稠密向量、联合训练和 coarse-to-fine BeamFusion 均执行；生产 ANN 服务未复刻。本地对照口径：统一跨模型基线是 DIN，COBRA NDCG@10 相对 DIN +25.75%；内部 sparse-only 基线加入 dense cascade 后 +45.83%。两项提升不能相互替代。180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  generative-retrieval semantic-id dense-retrieval 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-cobra-75daff60">Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations</h2>
<p class="ar-learning-card__meta">Baidu · 论文公开：2025-03-04</p>
<p><strong>方法要点：</strong>纯 Semantic ID 在量化阶段丢失细粒度信息。COBRA 先生成稀疏 code，再以 code 条件生成可端到端更新的 dense vector；推理先 beam 搜索 code，再用 dense 最近邻细排。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。稀疏 S-ID、以 S-ID 为条件的稠密向量、联合训练和 coarse-to-fine BeamFusion 均执行；生产 ANN 服务未复刻。本地对照口径：统一跨模型基线是 DIN，COBRA NDCG@10 相对 DIN +25.75%；内部 sparse-only 基线加入 dense cascade 后 +45.83%。两项提升不能相互替代。180 users/280 items、seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.02453">原论文</a> · <a href="../../../../reproductions/2503.02453-cobra/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment 搜广推与 LLM 应用 Kuaishou 2025-02-26 传统 retrieve→rank 多阶段系统目标割裂；已有生成式召回又多为 point-wise next-item generation，难以保证一个推荐 session 内的连贯性与多样性。OneRec 用三层 RQ Semantic ID 表示物品，以 MoE 模型一次生成 5 个目标物品的完整 session，并训练个性化 reward model 预测 watch/interaction 指标。 Fidelity: 完整核心链路复现。当前代码实际训练 RQ Semantic IDs、session-wise encoder-decoder、稀疏 MoE、个性化 reward model 和 self-hard DPO；仅缩小模型、session 长度和公开数据规模。本地对照口径：基线是 Session Generator SFT；实验组是 reward model+self-hard DPO 后的 OneRec；NDCG@10 从 0.01565 降至 0（-100%）。这是 preference alignment 阶段消融，不是 OneRec 相对 DIN 的结果。   搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-onerec-bec96f9e">OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment</h2>
<p class="ar-learning-card__meta">Kuaishou · 论文公开：2025-02-26</p>
<p><strong>方法要点：</strong>传统 retrieve→rank 多阶段系统目标割裂；已有生成式召回又多为 point-wise next-item generation，难以保证一个推荐 session 内的连贯性与多样性。OneRec 用三层 RQ Semantic ID 表示物品，以 MoE 模型一次生成 5 个目标物品的完整 session，并训练个性化 reward model 预测 watch/interaction 指标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。当前代码实际训练 RQ Semantic IDs、session-wise encoder-decoder、稀疏 MoE、个性化 reward model 和 self-hard DPO；仅缩小模型、session 长度和公开数据规模。本地对照口径：基线是 Session Generator SFT；实验组是 reward model+self-hard DPO 后的 OneRec；NDCG@10 从 0.01565 降至 0（-100%）。这是 preference alignment 阶段消融，不是 OneRec 相对 DIN 的结果。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.18965">原论文</a> · <a href="../../../../reproductions/2502.18965-onerec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation 搜广推与 LLM 应用 Meituan 2025-02-14 逐物品 next-item 训练把同一消费意图中的多个物品硬排成先后标签，也无法把“下一次访问会同时消费的一组物品”作为多正例。SessionRec 先由 Item-based Session Encoder（ISE）把一次访问中的物品聚合为 session token，再由 Session-based Sequence Encoder（SSE）建模跨 session 兴趣迁移，最终让一个 query 同时召回下一 session 的所有正例。 Fidelity: 核心机制复现。真实执行 session 内聚合、session 间 Transformer、多正例 next-session retrieval，以及 session 内曝光负例排序损失；私有特征与 ANN 服务未复刻。本地对照口径：基线是等预算的扁平 Item Transformer；实验组是 SessionRec Transformer；NDCG@20 从 0.004718 降至 0.003678（-22.05%）。这是 session 建模消融；DIN 未在 KuaiRand session 任务中参与比较。  session recommendation generative retrieval 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-sessionrec-2fd19641">SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation</h2>
<p class="ar-learning-card__meta">Meituan · 论文公开：2025-02-14</p>
<p><strong>方法要点：</strong>逐物品 next-item 训练把同一消费意图中的多个物品硬排成先后标签，也无法把“下一次访问会同时消费的一组物品”作为多正例。SessionRec 先由 Item-based Session Encoder（ISE）把一次访问中的物品聚合为 session token，再由 Session-based Sequence Encoder（SSE）建模跨 session 兴趣迁移，最终让一个 query 同时召回下一 session 的所有正例。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 核心机制复现。真实执行 session 内聚合、session 间 Transformer、多正例 next-session retrieval，以及 session 内曝光负例排序损失；私有特征与 ANN 服务未复刻。本地对照口径：基线是等预算的扁平 Item Transformer；实验组是 SessionRec Transformer；NDCG@20 从 0.004718 降至 0.003678（-22.05%）。这是 session 建模消融；DIN 未在 KuaiRand session 任务中参与比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.10157">原论文</a> · <a href="../../../../reproductions/2502.10157-sessionrec/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System 搜广推与 LLM 应用 Tencent / WeChat 2024-11-21 ID 召回难利用广告内容。LEADRE 以跨域行为、长期总结和实时行为构造 intent-aware prompt，将广告量化为 S-ID，并用广告语义/商业价值辅助任务和 DPO 对齐，线上把长期生成缓存与实时服务组合。 Fidelity: 完整核心链路复现。Semantic ID、长短期/商业意图、语义与价值辅助任务、SFT→DPO 和可缓存/实时双路径均执行；私有广告与生产服务未复刻。本地对照口径：统一跨模型基线是 DIN，LEADRE NDCG@10 相对 DIN +12.94%；内部基线是 S-ID 多任务 SFT，继续 DPO 后 -4.53%。主结论与对齐阶段消融分开报告。MovieLens-100K，180 users/280 items，seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；  llm-recommendation generative-retrieval advertising preference-alignment 搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-leadre-72cfaef2">LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System</h2>
<p class="ar-learning-card__meta">Tencent / WeChat · 论文公开：2024-11-21</p>
<p><strong>方法要点：</strong>ID 召回难利用广告内容。LEADRE 以跨域行为、长期总结和实时行为构造 intent-aware prompt，将广告量化为 S-ID，并用广告语义/商业价值辅助任务和 DPO 对齐，线上把长期生成缓存与实时服务组合。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity: 完整核心链路复现。Semantic ID、长短期/商业意图、语义与价值辅助任务、SFT→DPO 和可缓存/实时双路径均执行；私有广告与生产服务未复刻。本地对照口径：统一跨模型基线是 DIN，LEADRE NDCG@10 相对 DIN +12.94%；内部基线是 S-ID 多任务 SFT，继续 DPO 后 -4.53%。主结论与对齐阶段消融分开报告。MovieLens-100K，180 users/280 items，seeds 42–44。统一 DIN（100 steps）Hit/NDCG 为 0.0481/0.02167；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2411.13789">原论文</a> · <a href="../../../../reproductions/2411.13789-leadre/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="recommendation" data-theme="recommendation" data-topic="recommendation/generative-retrieval-reasoning" data-search="Recommender Systems with Generative Retrieval 搜广推与 LLM 应用 Google / Google DeepMind 2023-05-08 传统召回为每个物品维护独立 ID embedding，难以共享语义，也无法自然生成新物品。TIGER 先把内容向量量化成分层 Semantic ID，再让 encoder-decoder 像生成 token 一样生成下一个物品；同一语义前缀的冲突由额外 token 消解。 保真度：核心机制复现。保真度：核心机制复现。RQ-VAE、残差语义 ID、collision token 和自回归 Transformer 检索链路均实际训练；MovieLens genre 替代 Sentence-T5 商品文本，省略 hashed user token 与 cold-start epsilon mixing。本地对照口径：基线是词表容量和参数量匹配的随机分层 ID 生成器；实验组是 TIGER Semantic ID；NDCG@10 从 0.01043 降至 0.00635（-39.16%）。这是 ID 方案消融，不是相对 DIN 的比较。   搜广推 生成式召回与推理推荐">
<p class="ar-learning-card__domain"><a href="./">搜广推 / 生成式召回与推理推荐</a></p>
<h2 id="paper-recommendation-tiger-7436853d">Recommender Systems with Generative Retrieval</h2>
<p class="ar-learning-card__meta">Google / Google DeepMind · 论文公开：2023-05-08</p>
<p><strong>方法要点：</strong>传统召回为每个物品维护独立 ID embedding，难以共享语义，也无法自然生成新物品。TIGER 先把内容向量量化成分层 Semantic ID，再让 encoder-decoder 像生成 token 一样生成下一个物品；同一语义前缀的冲突由额外 token 消解。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>保真度：核心机制复现。保真度：核心机制复现。RQ-VAE、残差语义 ID、collision token 和自回归 Transformer 检索链路均实际训练；MovieLens genre 替代 Sentence-T5 商品文本，省略 hashed user token 与 cold-start epsilon mixing。本地对照口径：基线是词表容量和参数量匹配的随机分层 ID 生成器；实验组是 TIGER Semantic ID；NDCG@10 从 0.01043 降至 0.00635（-39.16%）。这是 ID 方案消融，不是相对 DIN 的比较。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.05065">原论文</a> · <a href="../../../../reproductions/2305.05065-tiger/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
