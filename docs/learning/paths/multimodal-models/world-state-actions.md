---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 视觉世界建模：状态、生成与动作条件

[多模态](index.md) / 子主题导学 · 约 3 分钟 · 22 张论文卡

## 先想一个问题

模型是在识别画面，还是能判断动作将怎样改变状态？

## 记住这一点

把观察、动作和后续状态放在一起，才能学习可用于预测或控制的表示。LeWAM 联合学习未来潜状态预测与动作 flow matching，让视觉表征和策略相互塑造；规划时再用潜动力学评价动作候选。WOVEN 则把视频生成的视觉转移组织成场景、动作、推理类型受控的监督，训练模型理解结果、原因与反事实。

## 一个例子

同一桌面，把杯子向左推和向右推应产生不同结果；只认出“桌上有杯子”不足以控制机器人。表征预测可避免逐像素重建，但仍要检验动作条件是否有效、rollout 多步后是否漂移，以及选出的动作能否在闭环环境到达目标。

## 什么时候要小心

生成视频逼真、一步预测误差小或训练集问答分数高，都不自动证明规划有效。源场景与轨迹要分组隔离，反事实不能泄漏未来结果。本地 LeWAM 尚是非 holdout 闭环诊断，WOVEN 是小规模公开训练源实验；都不能替代原文完整泛化或机器人结论。

## 先读这几篇

先读 LeWAM 的潜状态/动作联合目标，理解预测怎样进入控制；再读 WOVEN 的视觉转移与受控监督，区分表征学习、生成数据、问答推理和闭环规划。之后按视觉几何、视频记忆或具身动作细分。

1. [LeWAM: End-to-End World and Action Modeling with JEPAs](../../../reproductions/2610.12818-lewam/README.md) · [原论文](https://arxiv.org/abs/2610.12818)
2. [WOVEN: Weaving Visual World Modeling into Multimodal LLMs](../../../reproductions/2610.12417-woven/README.md) · [原论文](https://arxiv.org/abs/2610.12417)

## 自测一下

世界模型的一步 latent MSE 更低，是否必然能带来更高的长程控制成功率？

??? note "展开参考答案"

    不必然。误差可能集中在与动作选择无关的方向，多步 rollout 还会累积偏差，策略搜索也可能利用模型漏洞。需要相同环境、目标和预算下的闭环控制对照，且不能用训练目标轨迹冒充 holdout。

## 这个子主题的论文卡片

导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">
<div class="ar-learning-controls">
<label for="learning-search">搜索卡片
<input id="learning-search" type="search" data-learning-search placeholder="搜索论文、机制、机构或本地边界"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">共 22 张卡片</p>
<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="DT-JEPA: Learning to Predict Future Representations for Decision-Making 基础模型 Southeast University 2026-10-23 传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。 成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  JEPA与世界模型 未来表征与离线决策 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-dt-jepa-898e3cdc">DT-JEPA: Learning to Predict Future Representations for Decision-Making</h2>
<p class="ar-learning-card__meta">Southeast University · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32657v1">原论文</a> · <a href="../../../../foundation-models/2610.32657-dt-jepa/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="UniAction: Unified Action Conditioning for World Models 多模态大模型 Stanford University 2026-10-23 异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。 成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  世界模型与动作条件 统一动作表示 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-multimodal-models-uniaction-704ab058">UniAction: Unified Action Conditioning for World Models</h2>
<p class="ar-learning-card__meta">Stanford University · 论文公开：2026-10-23</p>
<p><strong>方法要点：</strong>异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32977v1">原论文</a> · <a href="../../../../multimodal-models/2610.32977-uniaction/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models 基础模型 Australian Institute for Machine Learning, Adelaide University 2026-10-22 普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3 该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。  世界模型 JEPA 关系表示与逆动态 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-inside-jepa-840eadf0">Inside-JEPA: From Prediction to Relational Grounding in Latent World Models</h2>
<p class="ar-learning-card__meta">Australian Institute for Machine Learning, Adelaide University · 论文公开：2026-10-22</p>
<p><strong>方法要点：</strong>普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31194v1">原论文</a> · <a href="../../../../foundation-models/2610.31194-inside-jepa/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ALPS: Visual State Encoders for World Models 基础模型 University of California, Santa Cruz 2026-10-21 世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师； 完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。  视觉表征与世界模型 联合嵌入与自监督学习 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-alps-4489dea8">ALPS: Visual State Encoders for World Models</h2>
<p class="ar-learning-card__meta">University of California, Santa Cruz · 论文公开：2026-10-21</p>
<p><strong>方法要点：</strong>世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30120v1">原论文</a> · <a href="../../../../foundation-models/2610.30120-alps/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Agentic World Action Models 多模态大模型 UC Berkeley 2026-10-21 世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。 原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。  视频理解与世界模型 具身技能与联合动作生成 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-multimodal-models-aw0-c41ecc38">Agentic World Action Models</h2>
<p class="ar-learning-card__meta">UC Berkeley · 论文公开：2026-10-21</p>
<p><strong>方法要点：</strong>世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30136v1">原论文</a> · <a href="../../../../multimodal-models/2610.30136-aw0/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors 基础模型 University of Pennsylvania 2026-10-20 LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。  JEPA与世界模型 局部均匀球分布匹配 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-locale-jepa-ba12e8f4">LocaLeJEPA: Maximum Entropy Representations under Geometric Priors</h2>
<p class="ar-learning-card__meta">University of Pennsylvania · 论文公开：2026-10-20</p>
<p><strong>方法要点：</strong>LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28458v1">原论文</a> · <a href="../../../../foundation-models/2610.28458-locale-jepa/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Persistent Planar Memory for Video World Models 基础模型 Tsinghua University 2026-10-16 长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。  多模态基础模型 世界模型与持久三维记忆 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-ppmem-5417d641">Persistent Planar Memory for Video World Models</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-10-16</p>
<p><strong>方法要点：</strong>长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23795">原论文</a> · <a href="../../../../foundation-models/2610.23795-ppmem/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video 基础模型 Arizona State University 2026-10-15 第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。 完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。  多模态基础模型 空间推理与分段多教师蒸馏 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-ego-p2c-b2c2eae5">EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video</h2>
<p class="ar-learning-card__meta">Arizona State University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22681">原论文</a> · <a href="../../../../foundation-models/2610.22681-ego-p2c/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Gen4P: Video Generators are 4D Perceivers 基础模型 Nanyang Technological University 2026-10-15 视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。  多模态基础模型 视频生成与四维感知 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-gen4p-e9a640f8">Gen4P: Video Generators are 4D Perceivers</h2>
<p class="ar-learning-card__meta">Nanyang Technological University · 论文公开：2026-10-15</p>
<p><strong>方法要点：</strong>视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22371">原论文</a> · <a href="../../../../foundation-models/2610.22371-gen4p/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos 基础模型 Mohamed bin Zayed University of Artificial Intelligence 2026-10-14 人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  JEPA与世界模型 具身多模态 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-egojepa-867ae28c">EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos</h2>
<p class="ar-learning-card__meta">Mohamed bin Zayed University of Artificial Intelligence · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20904">原论文</a> · <a href="../../../../foundation-models/2610.20904-egojepa/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis 基础模型 FAIR at Meta / Mila - Québec AI Institute / Université de Montréal 2026-10-14 单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。 完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。  多模态基础模型 几何一致新视角生成 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-esc-e793a8c8">ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis</h2>
<p class="ar-learning-card__meta">FAIR at Meta / Mila - Québec AI Institute / Université de Montréal · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23732v1">原论文</a> · <a href="../../../../foundation-models/2610.23732-esc/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models 基础模型 论文未列机构 2026-10-14 JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。 原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。  世界模型评测 冻结物理状态解码器 预测与规划配对比较 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-jepa-prediction-planning-96c625cf">One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models</h2>
<p class="ar-learning-card__meta">论文未列机构 · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19375v1">原论文</a> · <a href="../../../../foundation-models/2610.19375-jepa-prediction-planning/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning 基础模型 European Molecular Biology Laboratory (EMBL) 2026-10-14 联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数； 完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；  self-supervised-learning joint-embedding small-batch representation-learning 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-oob-regularization-98328dd1">Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning</h2>
<p class="ar-learning-card__meta">European Molecular Biology Laboratory (EMBL) · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20158">原论文</a> · <a href="../../../../reproductions/2610.20158-oob-regularization/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Time-JEPA: Grounding Video World Models with Physical Time Series 基础模型 Harbin Institute of Technology 2026-10-14 视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。 完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。  JEPA与世界模型 物理时序监督 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-time-jepa-c002ea0d">Time-JEPA: Grounding Video World Models with Physical Time Series</h2>
<p class="ar-learning-card__meta">Harbin Institute of Technology · 论文公开：2026-10-14</p>
<p><strong>方法要点：</strong>视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23982">原论文</a> · <a href="../../../../foundation-models/2610.23982-time-jepa/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference 基础模型 Meta Reality Labs Research 2026-10-09 固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。  jepa video-representation elastic-inference 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-ev-jepa-12c252ce">EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference</h2>
<p class="ar-learning-card__meta">Meta Reality Labs Research · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14324">原论文</a> · <a href="../../../../reproductions/2610.14324-ev-jepa/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices 基础模型 ML Collective 2026-10-09 Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间； 8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。  world-action-model robotics efficient-inference 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-smolwam-cc2de315">SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices</h2>
<p class="ar-learning-card__meta">ML Collective · 论文公开：2026-10-09</p>
<p><strong>方法要点：</strong>Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间；</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13740">原论文</a> · <a href="../../../../reproductions/2610.13740-smolwam/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LeWAM: End-to-End World and Action Modeling with JEPAs 基础模型 UC San Diego 2026-10-08 传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。 当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。  world-action-model jepa latent-planning 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-lewam-7895d3a3">LeWAM: End-to-End World and Action Modeling with JEPAs</h2>
<p class="ar-learning-card__meta">UC San Diego · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12818">原论文</a> · <a href="../../../../reproductions/2610.12818-lewam/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Mid-Training Language Models on Raw Video 多模态大模型 Meta AI / Massachusetts Institute of Technology 2026-10-08 将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置  视频理解与世界模型 无字幕视频中期训练 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-multimodal-models-raw-video-midtraining-db4472b0">Mid-Training Language Models on Raw Video</h2>
<p class="ar-learning-card__meta">Meta AI / Massachusetts Institute of Technology · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11019">原论文</a> · <a href="../../../../multimodal-models/2610.11019-raw-video-midtraining/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WOVEN: Weaving Visual World Modeling into Multimodal LLMs 多模态大模型 Northwestern University 2026-10-08 静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。 相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。  multimodal-foundation-model visual-transition-reasoning world-model-supervision 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-multimodal-models-woven-63239e78">WOVEN: Weaving Visual World Modeling into Multimodal LLMs</h2>
<p class="ar-learning-card__meta">Northwestern University · 论文公开：2026-10-08</p>
<p><strong>方法要点：</strong>静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12417">原论文</a> · <a href="../../../../reproductions/2610.12417-woven/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents 基础模型 Tsinghua University 2026-09-29 冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  世界动作模型 预测视觉潜变量 机器人 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-vjepa-policy-d720eedd">V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents</h2>
<p class="ar-learning-card__meta">Tsinghua University · 论文公开：2026-09-29</p>
<p><strong>方法要点：</strong>冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 机制诊断</summary>
<p>复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37250">原论文</a> · <a href="../../../../foundation-models/2609.37250-vjepa-policy/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning 基础模型 Nanyang Technological University / VBVR Community 2026-08-26 通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。 Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。  multimodal-foundation-model native-visual-reasoning verifiable-reward benchmark 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-foundation-models-vbvr-pro-eb931970">VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning</h2>
<p class="ar-learning-card__meta">Nanyang Technological University / VBVR Community · 论文公开：2026-08-26</p>
<p><strong>方法要点：</strong>通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界</summary>
<p>Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26105">原论文</a> · <a href="../../../../reproductions/2608.26105-vbvr-pro/">实现解读</a></p>
</article>
<article class="ar-learning-card" data-learning-card data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Editing Everything Everywhere All at Once 多模态大模型 University of Modena and Reggio Emilia 2026-06-30 多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。 以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；  视觉生成与编辑 多实例编辑与注意力隔离 多模态 视觉世界建模：状态、生成与动作条件">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<h2 id="paper-multimodal-models-mice-b52a199b">Editing Everything Everywhere All at Once</h2>
<p class="ar-learning-card__meta">University of Modena and Reggio Emilia · 论文公开：2026-06-30</p>
<p><strong>方法要点：</strong>多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。</p>
<details class="ar-learning-boundary"><summary>本地范围与边界 · 成本过高，未复现</summary>
<p>以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；</p></details>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31278v1">原论文</a> · <a href="../../../../multimodal-models/2606.31278-mice/">实现解读</a></p>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


[跨主题搜索全部卡片](../../all.md)
