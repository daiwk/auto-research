---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 视觉世界建模：状态、生成与动作条件

[多模态](index.md) / 22 个问题 · 22 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">22 个问题 · 22 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:dt-jepa" data-paper-title="DT-JEPA: Learning to Predict Future Representations for Decision-Making" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="DT-JEPA: Learning to Predict Future Representations for Decision-Making 基础模型 Southeast University 2026-10-23 传统DT用单个return-to-go条件，无法区分回报相同但未来动力学不同的轨迹。本方法将条件改成由历史预测的未来latent分布：历史encoder生成Gaussian参数，EMA target encoder只在训练期编码真实未来；重参数采样的预测未来通过独立gamma/beta MLP调制DT hidden。离线目标为BC加Gaussian NLL；在线通过双target critic的较小值构建多步target，并优化Q1指导的actor目标。 成本过高，不复现（审查 DONE）。D4RL共19个locomotion/navigation数据配置、主表5种子、多个未见reward的在线适配及基线/消融；附录DT4层/4头/512hidden、batch256/context20。原文未给总GPU小时，不臆测。完整offline+online矩阵超单卡短时预算，不安装MuJoCo、不下载轨迹、不启动环境试跑。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  JEPA与世界模型 未来表征与离线决策 多模态 视觉世界建模：状态、生成与动作条件 为什么未来 latent 要由历史预测，而真实未来只交给训练期的目标编码器？ 决策时真实未来尚未发生，直接用它作条件会造成泄漏。历史编码器预测未来分布，并通过重参数采样得到决策条件；EMA 目标只提供训练对齐信号。相同回报可能对应不同动力学，未来表征尝试补足单一 return-to-go 无法区分的信息。 例如两条轨迹都得十分，但一条将撞到障碍、另一条可通行；预测未来状态比仅给“目标十分”更能区分后续选择。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-dt-jepa-898e3cdc" class="ar-learning-paper-anchor"></span>
<h2 id="qa-07079ed5e9b5243c">为什么未来 latent 要由历史预测，而真实未来只交给训练期的目标编码器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adt-jepa">DT-JEPA: Learning to Predict Future Representations for Decision-Making</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Southeast University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>决策时真实未来尚未发生，直接用它作条件会造成泄漏。历史编码器预测未来分布，并通过重参数采样得到决策条件；EMA 目标只提供训练对齐信号。相同回报可能对应不同动力学，未来表征尝试补足单一 return-to-go 无法区分的信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两条轨迹都得十分，但一条将撞到障碍、另一条可通行；预测未来状态比仅给“目标十分”更能区分后续选择。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32657v1">原论文</a> · <a href="../../../../foundation-models/2610.32657-dt-jepa/">实现解读</a> · <a href="#qa-07079ed5e9b5243c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:uniaction" data-paper-title="UniAction: Unified Action Conditioning for World Models" data-learning-pending="false" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="UniAction: Unified Action Conditioning for World Models 多模态大模型 Stanford University 2026-10-23 异质动作以不同粒度编码，token较多的动作在同一softmax中会仅因数量而占据更大attention mass。UniAction以共享semantic codebook编码元素身份，将(t,y,x)送入既有视频模型的native positional mechanism，再对action部分统一加一个基数bias，保持action内部相对logits不变，同时移除总mass对Na的线性依赖。 成本过高，不复现（审查 DONE）。诊断回调仅证明参数传递，不能当成真实视频backbone位置实现。Wan2.2-I2V-A14B high-noise expert LoRA，GoalForce/SolarWM/EgoDex/DROID各10K clips，共40K段81帧480×832；410反事实生成、多个motion/pose估计器、4个专家和100人评测。完整视频训练/生成显著超过单A100/A30短时资源，不下载14B权重或40K视频，不试跑成本。本轮已在CPU及真实NVIDIA A100上执行同一冻结版本、42/43/44三个种子：独立机制指标、脱敏GPU凭证。仅验收下述L1组件，不宣称完整模型能力。  世界模型与动作条件 统一动作表示 多模态 视觉世界建模：状态、生成与动作条件 为什么给 action logits 加 log(Nref/Na)，能抵消完全复制动作 Token 带来的注意力总权重变化？ 同一联合 softmax 中，复制相同 key/value 且位置编码相同，会增加重复项的指数和，使 action 总权重仅因数量变大。数量对应的对数偏置抵消这种重复，同时保留 action 内相对 logits；加入不同内容或不同位置的动作仍可合理改变输出。 例如把每个动作 token 连位置表示一起复制两份，未经校正动作会更占权重；校正后不应仅凭重复份数改变结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-uniaction-704ab058" class="ar-learning-paper-anchor"></span>
<h2 id="qa-32b91700ff0ec00d">为什么给 action logits 加 log(Nref/Na)，能抵消完全复制动作 Token 带来的注意力总权重变化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Auniaction">UniAction: Unified Action Conditioning for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一联合 softmax 中，复制相同 key/value 且位置编码相同，会增加重复项的指数和，使 action 总权重仅因数量变大。数量对应的对数偏置抵消这种重复，同时保留 action 内相对 logits；加入不同内容或不同位置的动作仍可合理改变输出。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把每个动作 token 连位置表示一起复制两份，未经校正动作会更占权重；校正后不应仅凭重复份数改变结果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.32977v1">原论文</a> · <a href="../../../../multimodal-models/2610.32977-uniaction/">实现解读</a> · <a href="#qa-32b91700ff0ec00d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:inside-jepa" data-paper-title="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Inside-JEPA: From Prediction to Relational Grounding in Latent World Models 基础模型 Australian Institute for Machine Learning, Adelaide University 2026-10-22 普通 JEPA 能预测潜在状态，但潜变量未必对应可解释关系。本文把每个有序实体对的关系通道直接拼入动态状态，并要求逆动态头根据前后关系通道恢复动作；预测损失的未来目标仍由 EMA 编码器提供，而逆动态的未来状态必须来自可反传的 online 编码器。仅预测、读全部状态、只读实体和打乱动作标签的对照用于区分信号来自哪里。原文 §3 该完整矩阵超出单 A100/A30/Mac 短时预算，成本过高，不复现（审查 DONE）；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。RelationalStateEncoder 接收 [B,4,512] 冻结特征、[B,4,4] 归一化框、实体类型和共享实体 mask，本地组件每次调用最多64对帧；真实 crop、ResNet18、检测跟踪均由外部提供，当前未运行它们。InsideJEPA 实现预测器、可选离散/连续动作条件、五臂损失与显式 EMA 更新。  世界模型 JEPA 关系表示与逆动态 多模态 视觉世界建模：状态、生成与动作条件 为什么逆动态头的未来状态要来自可反传的 online 编码器，而非 EMA target？ 逆动态目标要把“哪些关系能解释动作”的信号传回表示层，若未来关系全停梯度，该侧就失去相应学习压力。JEPA 预测目标仍可使用稳定 EMA，但逆动态路径有不同梯度职责；还需通过只读实体、打乱动作等对照确认关系通道真正提供作用信息。 例如模型需根据移动前后的“杯子在盒子左侧”关系恢复动作；未来关系分支可反传，才能学会保留这种变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-inside-jepa-840eadf0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-098a3adf3f209998">为什么逆动态头的未来状态要来自可反传的 online 编码器，而非 EMA target？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ainside-jepa">Inside-JEPA: From Prediction to Relational Grounding in Latent World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Australian Institute for Machine Learning, Adelaide University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>逆动态目标要把“哪些关系能解释动作”的信号传回表示层，若未来关系全停梯度，该侧就失去相应学习压力。JEPA 预测目标仍可使用稳定 EMA，但逆动态路径有不同梯度职责；还需通过只读实体、打乱动作等对照确认关系通道真正提供作用信息。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模型需根据移动前后的“杯子在盒子左侧”关系恢复动作；未来关系分支可反传，才能学会保留这种变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与五臂；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31194v1">原论文</a> · <a href="../../../../foundation-models/2610.31194-inside-jepa/">实现解读</a> · <a href="#qa-098a3adf3f209998">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:alps" data-paper-title="ALPS: Visual State Encoders for World Models" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ALPS: Visual State Encoders for World Models 基础模型 University of California, Santa Cruz 2026-10-21 世界模型以视觉 token 为状态进行预测和规划，但一个编码器通常只擅长物理状态、语言对齐或像素重建中的一部分。ALPS 尝试让同一组 patch token 同时承担三种接口：机器人状态探针能读出位置，文字指令能对应图像，而未来 token 能被解码成图像以便检查。第一阶段从零训练 ViT-B/16：同一组未做最终 LayerNorm 的 patch token接受图文对比、caption、自重建和密集跨裁剪对应四种监督。第二阶段将第一阶段 encoder 同时用作学生初始化和固定教师； 完整预训练和实验成本过高，不复现（审查 DONE），not_reproduced_high_cost 为终态，不下载大模型/训练数据、不试探性跑完整训练、不自动重试。诊断使用两组裁剪、patch、8 维 query 和 6 维随机 token。输入会检查 shape、有限值、正尺度、裁剪范围和标准差；不静默修正无效数据。模块导入不要求 torch，执行时才加载；不联网、不自动安装依赖、不执行上游脚本或下载 checkpoint。正式评测必须将训练统计与测试轨迹隔离，验证集选参，测试集只用于最终报告。  视觉表征与世界模型 联合嵌入与自监督学习 多模态 视觉世界建模：状态、生成与动作条件 第二阶段为什么只监督教师裁剪 B 中落在学生裁剪 A 内的 patch？ 学生只看得到 A，要求它逐点预测完全不在视野内的 B 区域会把不可见内容也当成确定监督。几何映射先找可对应位置，再预测固定教师的目标，外观增强则训练鲁棒表示；教师固定与学生初始化相同，不意味着训练中两者会一起更新。 例如学生只看到图片左半边，教师裁剪横跨左右；应只监督二者重叠部分，而不能要求学生精确读出右侧从未见到的小字。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-alps-4489dea8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8d4c87309e5eec26">第二阶段为什么只监督教师裁剪 B 中落在学生裁剪 A 内的 patch？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aalps">ALPS: Visual State Encoders for World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Cruz</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生只看得到 A，要求它逐点预测完全不在视野内的 B 区域会把不可见内容也当成确定监督。几何映射先找可对应位置，再预测固定教师的目标，外观增强则训练鲁棒表示；教师固定与学生初始化相同，不意味着训练中两者会一起更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生只看到图片左半边，教师裁剪横跨左右；应只监督二者重叠部分，而不能要求学生精确读出右侧从未见到的小字。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30120v1">原论文</a> · <a href="../../../../foundation-models/2610.30120-alps/">实现解读</a> · <a href="#qa-8d4c87309e5eec26">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:aw0" data-paper-title="Agentic World Action Models" data-learning-pending="false" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Agentic World Action Models 多模态大模型 UC Berkeley 2026-10-21 世界动作模型能预测未来视觉和控制轨迹，但通常缺少可组合的技能结构；代码型机器人 Agent 能重用程序，却未必把计划与物理动态预测统一起来。AW-0 在 Mixture-of-Transformers 中组合三个专家：代码专家产生参数化程序片段，视频专家预测未来场景，动作专家产生连续控制。程序既能约束预测，也可在可选执行模式中调用技能库。每个专家有独立投影、归一化与 FFN，通过每层联合注意力交换信息；专家内部双向、专家之间按代码→视频→动作分块因果。 原始训练与完整对照矩阵明显超出低成本预算，且真实硬件和未随 release 提供的语料无法由合成 fixture 替代，因此成本过高，不复现（审查 DONE）。本地未验证、未生成预测，也没有生产搜广推线上 A/B 证据。本页、原论文 Figure 2、完整作者/代码元数据、成本依据和终态 catalog 已收录。没有运行 adapter、低成本 proxy、benchmark 指标或 GPU 验证收据；也不把“找到开源代码”当作复现完成。promotion_eligible=false、evolve_integrated=false，不进入 Evolve 训练或自动选参。  视频理解与世界模型 具身技能与联合动作生成 多模态 视觉世界建模：状态、生成与动作条件 AW-0 为什么允许专家内部双向交互，却把专家之间限制为代码→视频→动作？ 内部双向交互有利于同一模态组织完整表示，跨专家分块因果则保持计划、场景预测与动作的条件方向。代码不应提前读取后续视频或动作来伪装规划，动作却可利用代码与预测场景；完全互读会改变信息可用性及推理时的执行顺序。 例如先生成“抓取杯子”的程序，视频专家据此预测场景，动作专家再产出控制；不能让程序先偷看真实未来动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-aw0-c41ecc38" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b0c5a8e2785d041b">AW-0 为什么允许专家内部双向交互，却把专家之间限制为代码→视频→动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Aaw0">Agentic World Action Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC Berkeley</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>内部双向交互有利于同一模态组织完整表示，跨专家分块因果则保持计划、场景预测与动作的条件方向。代码不应提前读取后续视频或动作来伪装规划，动作却可利用代码与预测场景；完全互读会改变信息可用性及推理时的执行顺序。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先生成“抓取杯子”的程序，视频专家据此预测场景，动作专家再产出控制；不能让程序先偷看真实未来动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30136v1">原论文</a> · <a href="../../../../multimodal-models/2610.30136-aw0/">实现解读</a> · <a href="#qa-b0c5a8e2785d041b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:locale-jepa" data-paper-title="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LocaLeJEPA: Maximum Entropy Representations under Geometric Priors 基础模型 University of Pennsylvania 2026-10-20 LeJEPA 将整体表示推向各向同性高斯；当表示本身具有局部流形、双曲或等变几何时，单一全局分布不一定合适。LocaLeJEPA 不改写为另一种高斯损失，而是将每个 batch 的多视图平均表示分簇，在各簇内分别匹配均匀球分布。各簇位置不被拉向共同原点，局部形状通过重中心后的残差约束。 完整实验标注成本过高，不复现（审查 DONE），不下载、不试跑、不进入自动训练队列。3 seed 不改变 L1 诊断资格，无正式 capability comparison、无 Evolve 晋级。已实现 uniform_ball_cf、ballreg_loss、torch_kmeans_labels、local_ballreg_loss 和 locale_jepa_loss。前向真实计算局部均匀球统计并反向传播至投影；仅分簇赋值 detached，预测均值和重中心残差没有 stop-gradient。采用作者官方 pure-torch k-means 路径，不额外引入聚类依赖。  JEPA与世界模型 局部均匀球分布匹配 多模态 视觉世界建模：状态、生成与动作条件 为什么 LocaLeJEPA 不把所有簇都直接拉向同一个高斯分布？ 不同局部簇可能对应具有自身几何的状态，把它们统一拉向原点会破坏簇间位置和局部结构。方法先固定分组，再对各簇重中心残差匹配均匀球体分布，保留整体布局；簇太小时还要明确回退，不能把目标偷换为普通全局高斯正则。 例如两团表示分别对应两种运动模式，各自分散但位置不同；约束局部形状无需把两团的中心都拉到同一点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-locale-jepa-ba12e8f4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-039c7085ea195e93">为什么 LocaLeJEPA 不把所有簇都直接拉向同一个高斯分布？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alocale-jepa">LocaLeJEPA: Maximum Entropy Representations under Geometric Priors</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同局部簇可能对应具有自身几何的状态，把它们统一拉向原点会破坏簇间位置和局部结构。方法先固定分组，再对各簇重中心残差匹配均匀球体分布，保留整体布局；簇太小时还要明确回退，不能把目标偷换为普通全局高斯正则。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两团表示分别对应两种运动模式，各自分散但位置不同；约束局部形状无需把两团的中心都拉到同一点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.28458v1">原论文</a> · <a href="../../../../foundation-models/2610.28458-locale-jepa/">实现解读</a> · <a href="#qa-039c7085ea195e93">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppmem" data-paper-title="Persistent Planar Memory for Video World Models" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Persistent Planar Memory for Video World Models 基础模型 Tsinghua University 2026-10-16 长视频生成若只保存少量历史帧，跨视角回访容易遗忘场景；持续保存全部像素点云又非常大。PPMem把场景记忆压成可光栅化的平面primitive，在视频生成过程中由同一骨干联合预测，再通过持久pool向后续chunk反馈深度。每个局部平面用中心深度、两个矩形尺度和四元数共7个参数表示，变换到世界坐标后合并。pool按遮挡投票删除错误旧面，按观察质量去重，并依据已给定的下一段相机轨迹提前淘汰即将被更好观测替换的面；它不是读取未来真实视频。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。没有本地世界模型、训练结果或Evolve能力算子。本轮只核原文方法、元数据、结果归属及成本，不下载模型或视频，不制造小张量“世界模型能力”分数。没有GPU回执要求，因为没有接受执行CUDA实现。  多模态基础模型 世界模型与持久三维记忆 多模态 视觉世界建模：状态、生成与动作条件 依据下一段相机轨迹淘汰平面，为什么不等于读取未来真实视频？ 相机轨迹可以是生成任务已给定的控制条件，它说明之后将朝哪里看，并不提供那里的真实图像。平面池据此管理将被更好观测替换的几何，后续视频仍需模型生成；只有把未知未来观测或真值几何提前送入记忆，才构成另一种信息泄漏。 例如用户预先指定镜头绕桌子一圈，系统可据轨迹安排记忆；它仍不知道桌子背面的真实纹理，不能当成已经看到。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-ppmem-5417d641" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1ffec7e05ce43b92">依据下一段相机轨迹淘汰平面，为什么不等于读取未来真实视频？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appmem">Persistent Planar Memory for Video World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>相机轨迹可以是生成任务已给定的控制条件，它说明之后将朝哪里看，并不提供那里的真实图像。平面池据此管理将被更好观测替换的几何，后续视频仍需模型生成；只有把未知未来观测或真值几何提前送入记忆，才构成另一种信息泄漏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户预先指定镜头绕桌子一圈，系统可据轨迹安排记忆；它仍不知道桌子背面的真实纹理，不能当成已经看到。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与流程；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23795">原论文</a> · <a href="../../../../foundation-models/2610.23795-ppmem/">实现解读</a> · <a href="#qa-1ffec7e05ce43b92">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ego-p2c" data-paper-title="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video 基础模型 Arizona State University 2026-10-15 第一视角视频空间推理既要提问、采集证据，也要保证感知回答可靠。固定外部视觉工具无法随推理策略一起改进；把规划与感知压到同一组参数中又可能引入梯度冲突。EgoP²C先在冻结VLM上分别训练规划/组合（PC）与感知（V）的LoRA教师，再复制选定FFN形成PC、V、通用直接回答（G）专家。学生自己生成交互片段，由相应冻结教师实时评价同一批学生tokens，而非模仿教师另行生成的答案。公共视频前缀始终走冻结基础路径；角色私有文字、选项和历史不混入公共KV。 完整实验成本过高，不复现（审查 DONE）。本地保留真实角色FFN复制、q/k/v/o低秩残差、因果attention、公共前缀冻结、严格参数冻结、完整词表打分及上述损失。使用12维单层小型decoder和人工token ids，没有视觉编码器或真实视频。预设PLAN和DIRECT骨架，仅各片段内部由学生当前分布实时采样；没有训练过的空间教师、自由工具调用或学习到的路由器。  多模态基础模型 空间推理与分段多教师蒸馏 多模态 视觉世界建模：状态、生成与动作条件 为什么分段蒸馏必须让各教师评价同一批学生 tokens？ 学生实际生成的交互决定了它访问的前缀，各角色教师在这些前缀上评分，才能分别指出规划、感知或直接回答的偏差。若改成模仿教师另写的一条答案，就丢失在策略监督；共享视频 KV 还不能混入角色私有历史，以免破坏信息隔离。 例如学生先提出一个视角问题，再给出空间判断；规划教师评前段、感知教师评相关片段，二者都评学生真正走过的文本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-ego-p2c-b2c2eae5" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c60c2b24dcf80f55">为什么分段蒸馏必须让各教师评价同一批学生 tokens？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aego-p2c">EgoP²C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Arizona State University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>学生实际生成的交互决定了它访问的前缀，各角色教师在这些前缀上评分，才能分别指出规划、感知或直接回答的偏差。若改成模仿教师另写的一条答案，就丢失在策略监督；共享视频 KV 还不能混入角色私有历史，以免破坏信息隔离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如学生先提出一个视角问题，再给出空间判断；规划教师评前段、感知教师评相关片段，二者都评学生真正走过的文本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与信息边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22681">原论文</a> · <a href="../../../../foundation-models/2610.22681-ego-p2c/">实现解读</a> · <a href="#qa-c60c2b24dcf80f55">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gen4p" data-paper-title="Gen4P: Video Generators are 4D Perceivers" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Gen4P: Video Generators are 4D Perceivers 基础模型 Nanyang Technological University 2026-10-15 视频生成预训练包含运动与几何先验。Gen4P不通过多次去噪恢复几何，而是在干净视频潜变量上运行一次DiT编码，用按需cross-attention查询输出3D轨迹、点云、深度和相机参数。连续时间查询适配不同视频长度，冻结depth-LoRA提供额外几何先验，独立4D-LoRA学习新任务。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地训练、能力指标或Evolve算子。无本地adapter、GPU验收、训练指标或可执行Evolve映射。上游repo存在不等同代码已开源；未来若作者真正发布实现，只有出现新的独立证据或用户明确需求时再审查。本轮只完成方法、代码发布状态与资源配置核验；没有下载视频、checkpoint、运行训练或制造小模型“4D能力”分数。  多模态基础模型 视频生成与四维感知 多模态 视觉世界建模：状态、生成与动作条件 使用视频生成器做四维感知时，为什么不必执行完整多步去噪？ Gen4P 利用预训练 DiT 内部的运动与几何表示，而不是要求它重新生成视频。干净视频潜变量经过一次规定条件的编码，查询再读出轨迹或深度；冻结几何适配与新任务 LoRA 承担不同职责。少一次生成过程并不意味着感知任务无需监督或解码器。 例如输入现有视频后查询某点三秒后的三维位置，读取一次场景表示即可训练预测头，不需要先生成另一段完整视频。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-gen4p-e9a640f8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-e6914c7043932711">使用视频生成器做四维感知时，为什么不必执行完整多步去噪？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agen4p">Gen4P: Video Generators are 4D Perceivers</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Gen4P 利用预训练 DiT 内部的运动与几何表示，而不是要求它重新生成视频。干净视频潜变量经过一次规定条件的编码，查询再读出轨迹或深度；冻结几何适配与新任务 LoRA 承担不同职责。少一次生成过程并不意味着感知任务无需监督或解码器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如输入现有视频后查询某点三秒后的三维位置，读取一次场景表示即可训练预测头，不需要先生成另一段完整视频。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22371">原论文</a> · <a href="../../../../foundation-models/2610.22371-gen4p/">实现解读</a> · <a href="#qa-e6914c7043932711">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:egojepa" data-paper-title="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos 基础模型 Mohamed bin Zayed University of Artificial Intelligence 2026-10-14 人类第一视角视频中的手运动不需要经规则映射为每种机器人的动作。EgoJEPA先用手部运动差分条件JEPA预测未来视觉表示，再联合建模视觉与潜动作，最后仅适配目标机器人的输入输出动作接口。 成本过高，不复现（审查 DONE）。仅研究资料；成本过高，不复现（审查 DONE）。无本地能力指标、训练结果或可执行 Evolve 算子。无本地adapter、指标文件或GPU回执，也不登记可执行Evolve算子。原论文结果仅作为阅读资料。范围见本轮实现与审查合同。本轮只完成方法、资源需求、公开代码状态及原图收录，没有运行完整实验、下载checkpoint或制造模拟能力分数。  JEPA与世界模型 具身多模态 多模态 视觉世界建模：状态、生成与动作条件 EgoJEPA 为什么先学习潜动作，而不把人的手部轨迹直接规则映射成机器人关节？ 人的手与机器人的执行器形态不同，硬映射容易把特定身体结构当成通用动作。方法先用运动差分条件学习与视觉变化相关的潜动作，再联合视觉建模，最后适配目标机器人的动作接口；可迁移的是作用关系，而不是假设两种关节坐标天然等价。 例如人的捏取动作和夹爪闭合角度不同，但都能导致杯子被拿起；先学这一状态变化，再适配夹爪的输入输出。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-egojepa-867ae28c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-245e1f402013e420">EgoJEPA 为什么先学习潜动作，而不把人的手部轨迹直接规则映射成机器人关节？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aegojepa">EgoJEPA: Beyond Retargeting for Dexterous Manipulation from Egocentric Videos</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>人的手与机器人的执行器形态不同，硬映射容易把特定身体结构当成通用动作。方法先用运动差分条件学习与视觉变化相关的潜动作，再联合视觉建模，最后适配目标机器人的动作接口；可迁移的是作用关系，而不是假设两种关节坐标天然等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如人的捏取动作和夹爪闭合角度不同，但都能导致杯子被拿起；先学这一状态变化，再适配夹爪的输入输出。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20904">原论文</a> · <a href="../../../../foundation-models/2610.20904-egojepa/">实现解读</a> · <a href="#qa-245e1f402013e420">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:esc" data-paper-title="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis 基础模型 FAIR at Meta / Mila - Québec AI Institute / Université de Montréal 2026-10-14 单幅图像经扩散模型生成新视角时，2D视觉质量或相机姿态对齐不保证3D几何一致。ESC 联合生成 RGB 与逆深度，用 Plücker ray maps 条件化 Qwen MM-DiT，并以双向深度重投影约束 PCC 识别“物体消失”与“凭空出现”。推理时按 PCC 在多次随机生成中选优。 完整实验成本过高，不复现（审查 DONE）。未实现、未训练、未 GPU 验证。历史补发现，不是10月18日至21日的新首发。完整实验成本过高，不复现（审查 DONE）。本页没有可运行 adapter、没有本地效果指标，不进入自动训练或 Evolve 晋级队列。未实现、未训练、未 GPU 验证。本轮只有资料与算法边界收录，不提供伪 adapter、占位效果 JSON 或假 CUDA 回执。已核验固定 v1 正文、方法、架构图及 Appendix E.1 成本。  多模态基础模型 几何一致新视角生成 多模态 视觉世界建模：状态、生成与动作条件 为什么新视角图像看起来清晰、相机姿态也正确，仍可能不满足 PCC？ 外观逼真不约束两视角是否描述同一个三维场景。PCC 用深度重投影及可见性检查双向几何差，区分物体消失与凭空出现；遮挡和无效像素必须处理，不能用普通 RGB 差代替。Best-of-N 选优比较的是几何一致性，而非直接选择最漂亮的图片。 例如转动镜头后桌上的杯子消失，新图依旧自然清晰；双向深度重投影却会暴露这处不一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-esc-e793a8c8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-fdc0872eefd4d85b">为什么新视角图像看起来清晰、相机姿态也正确，仍可能不满足 PCC？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aesc">ESC: Escaping 2D Diffusion Ambiguity with Geometric Constraints for Consistent Novel View Synthesis</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / Mila - Québec AI Institute / Université de Montréal</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>外观逼真不约束两视角是否描述同一个三维场景。PCC 用深度重投影及可见性检查双向几何差，区分物体消失与凭空出现；遮挡和无效像素必须处理，不能用普通 RGB 差代替。Best-of-N 选优比较的是几何一致性，而非直接选择最漂亮的图片。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如转动镜头后桌上的杯子消失，新图依旧自然清晰；双向深度重投影却会暴露这处不一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23732v1">原论文</a> · <a href="../../../../foundation-models/2610.23732-esc/">实现解读</a> · <a href="#qa-fdc0872eefd4d85b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:jepa-prediction-planning" data-paper-title="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models 基础模型 论文未列机构 2026-10-14 JEPA 在自己的潜空间预测下一观察，较小的一步 loss 不一定表示更好的长程行动。论文固定一个只在真实观察编码上拟合的物理状态解码器，分别解码真实下一表征与预测下一表征，把编码器本身的可读性和预测器新增的误差拆开。规划仍用相同 checkpoint、相同任务和配对种子单独执行，不能由预测指标推导成功率。 原文三个环境的世界模型重训、每环境多训练/解码/规划种子和完整 MPC：成本过高，不复现（审查 DONE）。CPU 接口实测保存真实解码器拟合与受控输入的诊断指标，不代表世界模型能力。本地对照口径：共享状态规范与归一化、同一冻结解码器；输入必须来自相同 transition。世界模型预测与外部规划分别评价，不自动接入 Evolve 选择。  世界模型评测 冻结物理状态解码器 预测与规划配对比较 多模态 视觉世界建模：状态、生成与动作条件 为什么要从预测状态误差中减去真实表征经同一解码器得到的误差？ 解码误差同时混合编码器可读性、解码器不足和预测器偏差。固定同一解码器，先测真实下一表征，再测预测下一表征，差值更接近预测环节新增的影响；它可能为负，不能截零。即便差值小，长程规划成功率仍需独立配对验证。 例如解码器本来就把位置估错两格，预测表征又错三格；不能把全部三格都归因预测器，应先扣除真实表征的基础误差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-jepa-prediction-planning-96c625cf" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c221d8dad06e5450">为什么要从预测状态误差中减去真实表征经同一解码器得到的误差？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ajepa-prediction-planning">One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>解码误差同时混合编码器可读性、解码器不足和预测器偏差。固定同一解码器，先测真实下一表征，再测预测下一表征，差值更接近预测环节新增的影响；它可能为负，不能截零。即便差值小，长程规划成功率仍需独立配对验证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如解码器本来就把位置估错两格，预测表征又错三格；不能把全部三格都归因预测器，应先扣除真实表征的基础误差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19375v1">原论文</a> · <a href="../../../../foundation-models/2610.19375-jepa-prediction-planning/">实现解读</a> · <a href="#qa-c221d8dad06e5450">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:oob-regularization" data-paper-title="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning 基础模型 European Molecular Biology Laboratory (EMBL) 2026-10-14 联合嵌入自监督学习一方面拉近同一图像的不同增强视图，另一方面用抗坍塌正则保持表示多样性。小 batch 对整个表示分布的估计可能很差；单纯增大 GPU batch 又受显存限制。OOB 把“统计范围”与“本次优化 batch”解耦：定期编码整个训练集，按全数据分布构建每个样本的固定目标，再存入 CPU。在线训练只读取当前样本对应的锚点，不在每一步重新估计全数据正则。Gaussian 变体沿随机单位方向投影，把每列样本排序后匹配标准正态分位数； 完整原研究为成本过高，不复现（审查 DONE）。先核验 MD5 c99cafc152244af753f735de768cd75f，再解析官方 pickle，拒绝任意未验证 pickle。本地实现两种真实锚点算法，并在有限的官方 CIFAR 图像上执行有对照的训练。它不是原论文多数据集、100 epochs 的完整研究；短预算的负结果照实保留，不进入 Evolve 自动晋级。完整原研究为成本过高，不复现（审查 DONE）。本地对照口径：基线为同投影 / 分位数口径的 in-batch Gaussian 及 SimCLR；  self-supervised-learning joint-embedding small-batch representation-learning 多模态 视觉世界建模：状态、生成与动作条件 OOB 为什么能让小 batch 使用接近全数据范围的抗坍塌监督？ 它把全数据统计与在线优化分开：定期编码训练集并建立每样本锚点，随后小 batch 读取对应固定目标。这样在线更新无需每步重新估计完整分布，但锚点会随模型变化而陈旧，需要刷新；这不同于直接在小 batch 上计算普通方差或协方差损失。 例如显存一次只能放八张图，仍可事先用全训练集生成排序分位数目标，再让这八张各自匹配自己的缓存锚点。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-oob-regularization-98328dd1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-39f15ae4c6df1bd0">OOB 为什么能让小 batch 使用接近全数据范围的抗坍塌监督？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aoob-regularization">Dataset-Level Regularization for Joint-Embedding Self-Supervised Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · European Molecular Biology Laboratory (EMBL)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把全数据统计与在线优化分开：定期编码训练集并建立每样本锚点，随后小 batch 读取对应固定目标。这样在线更新无需每步重新估计完整分布，但锚点会随模型变化而陈旧，需要刷新；这不同于直接在小 batch 上计算普通方差或协方差损失。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如显存一次只能放八张图，仍可事先用全训练集生成排序分位数目标，再让这八张各自匹配自己的缓存锚点。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20158">原论文</a> · <a href="../../../../reproductions/2610.20158-oob-regularization/">实现解读</a> · <a href="#qa-39f15ae4c6df1bd0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:time-jepa" data-paper-title="Time-JEPA: Grounding Video World Models with Physical Time Series" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Time-JEPA: Grounding Video World Models with Physical Time Series 基础模型 Harbin Institute of Technology 2026-10-14 视频自监督目标不必保留精确的速度、关节角等物理状态。Time-JEPA 用同步传感器或标注作辅助目标，但它们不是编码器输入：训练时同一个 online encoder 分别处理 masked 上下文和 unmasked 视频，评测移除物理态 head，仍只输入视频。 完整实验成本过高，不复现（审查 DONE）。CPU与真实单张A100的42/43/44三seed诊断已完成。实现不只封装 loss：包含时间戳 nearest 对齐、逐变量 valid tubelet 池化、训练独占统计、真正的上下文 self-attention encoder、masked latent predictor、unmasked 两层物理 head、冻结 target 和显式 EMA 更新。nearest 的距离阈值由调用方传入、平局取较早测量，是本地明确的对齐策略，不冒充所有原始数据集的具体解码流程。  JEPA与世界模型 物理时序监督 多模态 视觉世界建模：状态、生成与动作条件 物理时间序列只作训练标签，为何还能改善仅输入视频的编码器？ 辅助头把视频表示映射到速度或关节角，误差反向推动编码器保留这些物理信息，部署时可以删除该头。传感器不进入输入，因此评测仍是视频任务；无效帧要保持掩码，归一化统计也只能来自训练集，避免伪造零标签或测试泄漏。 例如训练时用同步速度监督视频表示，测试只给运动画面；若把速度数值直接拼进测试输入，就变成不同任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-time-jepa-c002ea0d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-045efa8d388d00cd">物理时间序列只作训练标签，为何还能改善仅输入视频的编码器？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atime-jepa">Time-JEPA: Grounding Video World Models with Physical Time Series</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Harbin Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>辅助头把视频表示映射到速度或关节角，误差反向推动编码器保留这些物理信息，部署时可以删除该头。传感器不进入输入，因此评测仍是视频任务；无效帧要保持掩码，归一化统计也只能来自训练集，避免伪造零标签或测试泄漏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练时用同步速度监督视频表示，测试只给运动画面；若把速度数值直接拼进测试输入，就变成不同任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与隔离要求；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23982">原论文</a> · <a href="../../../../foundation-models/2610.23982-time-jepa/">实现解读</a> · <a href="#qa-045efa8d388d00cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ev-jepa" data-paper-title="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference 基础模型 Meta Reality Labs Research 2026-10-09 固定容量的视频模型难以同时适配端侧预算和跨设备协作，独立训练不同宽度也不保证中间表示兼容。EV-JEPA共享嵌套宽度参数，每步联合训练窄、宽与窄转宽三条路径，以冻结视频教师约束共同表示空间，并增加可调token压缩。 成本过高，暂不复现；成本过高，暂不复现；待验收（仅研究资料）。本轮完成全文审查与延期登记，不下载模型或数据，不训练、不注册可执行Adapter、不接入evolve。下文论文数值不是本地实验结果。原文§4.1：128 GPU、300epochs，Kinetics-710/SSv2/HowTo100M视频，冻结V-JEPA2 ViT-G教师；每步同时训练窄、宽、混合三路径。压缩器另需100epochs×300iterations、全局batch4096。不是本地测速，原预算显著超出单卡A100/A30或Mac；不下载全视频或尝试多臂训练。  jepa video-representation elastic-inference 多模态 视觉世界建模：状态、生成与动作条件 为何训练窄模型和宽模型之外，还要专门训练“窄转宽”路径？ 两种宽度各自表现好，不保证窄模型中间状态可直接交给宽模型。混合路径显式训练切分层的升宽接口，并以共同冻结教师约束表示，使跨设备接力有训练依据；这与随意裁剪通道或在运行时硬接两个独立模型不同，也不能省掉接力通信成本。 例如手机先跑窄层再把状态交给服务器宽层；若从未训练这种交接，服务器接到的表示可能不在其熟悉的分布中。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-ev-jepa-12c252ce" class="ar-learning-paper-anchor"></span>
<h2 id="qa-339f1d60618048c6">为何训练窄模型和宽模型之外，还要专门训练“窄转宽”路径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aev-jepa">EV-JEPA: Elastic V-JEPA for Any Device and Cross-Device Inference</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta Reality Labs Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>两种宽度各自表现好，不保证窄模型中间状态可直接交给宽模型。混合路径显式训练切分层的升宽接口，并以共同冻结教师约束表示，使跨设备接力有训练依据；这与随意裁剪通道或在运行时硬接两个独立模型不同，也不能省掉接力通信成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如手机先跑窄层再把状态交给服务器宽层；若从未训练这种交接，服务器接到的表示可能不在其熟悉的分布中。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.14324">原论文</a> · <a href="../../../../reproductions/2610.14324-ev-jepa/">实现解读</a> · <a href="#qa-339f1d60618048c6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smolwam" data-paper-title="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices 基础模型 ML Collective 2026-10-09 Cosmos Policy 将机器人状态、两路相机、动作和未来状态编码为九个 latent frame，沿用视频生成接口：33 帧 VAE、T5-XXL、28-block 2B DiT、1764 tokens 和五步去噪。SmolWAM 并非只换一个轻量 action head，而是在保留预训练 trunk、token 原位置与 rectified-flow readout 的同时，逐项恢复接口改变造成的分布偏移。单帧 Wan VAE 配合 0.5M adapter，映射回原 clip latent 空间； 8 步仅是缩小训练机制诊断，不代表原68,830row/5000step效果。当前为 core_mechanism：真实 A100 已完成三 seed 缩放 teacher 蒸馏、两阶段布局课程与新 student LIBERO 闭环，不用 VQA/随机小网络替代。新 student 与 no-op 均无任务成功；原5000步蒸馏未重训，不能称 full_pipeline 或能力提升。本地对照口径：基线为同固定 LIBERO 初始状态实际执行的 no-op 策略，实验组为各 seed 新训练、validation-selected SmolWAM student；完整 teacher 保持率与相对提速不适用。  world-action-model robotics efficient-inference 多模态 视觉世界建模：状态、生成与动作条件 为什么缩小动作查询接口时，还要保留原 token 位置与 rectified-flow 方向？ 预训练 trunk 已适应特定位置语义和从数据到噪声的速度定义，换轻量接口若同时改掉这些约定，会产生额外分布偏移。SmolWAM 逐项恢复适配而非只缩小动作头；载入权重成功也不能证明错误的噪声方向或位置设置下仍等价运行。 例如教师学的是噪声减数据的速度，若学生默认反向定义却仍套用原读出公式，动作恢复就可能朝错误方向变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-smolwam-cc2de315" class="ar-learning-paper-anchor"></span>
<h2 id="qa-6d581a20417b2084">为什么缩小动作查询接口时，还要保留原 token 位置与 rectified-flow 方向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmolwam">SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · ML Collective</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预训练 trunk 已适应特定位置语义和从数据到噪声的速度定义，换轻量接口若同时改掉这些约定，会产生额外分布偏移。SmolWAM 逐项恢复适配而非只缩小动作头；载入权重成功也不能证明错误的噪声方向或位置设置下仍等价运行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如教师学的是噪声减数据的速度，若学生默认反向定义却仍套用原读出公式，动作恢复就可能朝错误方向变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.13740">原论文</a> · <a href="../../../../reproductions/2610.13740-smolwam/">实现解读</a> · <a href="#qa-6d581a20417b2084">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lewam" data-paper-title="LeWAM: End-to-End World and Action Modeling with JEPAs" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="LeWAM: End-to-End World and Action Modeling with JEPAs 基础模型 UC San Diego 2026-10-08 传统 JEPA 学习“给定动作会到什么状态”，之后另训逆动力学或在线搜索动作。两阶段会使控制监督无法塑造视觉表征，宽高斯动作搜索也较昂贵。LeWAM 在同一训练阶段更新视觉编码器、潜在动力学和随机策略：既预测动作导致的未来 latent，又通过 flow matching 学习如何行动。视觉编码器由从零训练的 ResNet-18、空间 softmax 和两层投影 MLP 组成。模拟版本约 16.9M 参数，latent/MoT 宽度 192，4 层、4 头。 当前为 core_mechanism：真实 A100 已完成三 seed 缩放联合训练→新候选三臂闭环，证据绑定实际源码与权重哈希。目标来自训练轨迹，仍是非 holdout 诊断；未观测到规划相对 reactive 的优势，不宣称完整论文效果复现。本地对照口径：本轮真实测量用各 seed 的新训练、validation-selected checkpoint；基线为同一候选的 reactive policy，实验组为 best-of-K 与梯度规划。原目标来自训练轨迹，稳定能力相对提升不适用。发布模型入口仍保留，但未将其成绩冒充新候选成绩。  world-action-model jepa latent-planning 多模态 视觉世界建模：状态、生成与动作条件 为什么 LeWAM 的噪声动作分支不能经中间层读取干净动作？ 干净动作作为未来动力学监督，在训练中可供状态查询使用，却不是部署时策略已知的信息。如果噪声动作通过共享注意力偷读它，就可能复制目标而不学从观察和目标生成动作。分支独立参数不够，必须同时约束跨层可见性以堵住间接泄漏。 例如训练给出真实“向左推”的动作供预测未来；生成动作的噪声分支不能先看见这个答案，再把恢复结果算成决策能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-lewam-7895d3a3" class="ar-learning-paper-anchor"></span>
<h2 id="qa-64e4dca51fbd2f0a">为什么 LeWAM 的噪声动作分支不能经中间层读取干净动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alewam">LeWAM: End-to-End World and Action Modeling with JEPAs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · UC San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>干净动作作为未来动力学监督，在训练中可供状态查询使用，却不是部署时策略已知的信息。如果噪声动作通过共享注意力偷读它，就可能复制目标而不学从观察和目标生成动作。分支独立参数不够，必须同时约束跨层可见性以堵住间接泄漏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如训练给出真实“向左推”的动作供预测未来；生成动作的噪声分支不能先看见这个答案，再把恢复结果算成决策能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12818">原论文</a> · <a href="../../../../reproductions/2610.12818-lewam/">实现解读</a> · <a href="#qa-64e4dca51fbd2f0a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:raw-video-midtraining" data-paper-title="Mid-Training Language Models on Raw Video" data-learning-pending="false" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Mid-Training Language Models on Raw Video 多模态大模型 Meta AI / Massachusetts Institute of Technology 2026-10-08 将有序帧的patch编码为连续视觉token并按空间顺序序列化；因果LM预测下一视觉token，目标侧stop-gradient。中期训练没有字幕或文本损失；随后与对照使用相同图文指令调优，隔离视频阶段贡献。原文§3–4 成本过高，不复现（审查 DONE）；Google/Meta优先补漏。成本过高，不复现（审查 DONE）；不以MSE演示冒充视频中期训练。原文§4.1.4使用128张H100训练27300步，batch256、16K上下文，之后还有指令调优。原始资源配置  视频理解与世界模型 无字幕视频中期训练 多模态 视觉世界建模：状态、生成与动作条件 目标侧 stop-gradient 为什么不意味着视觉 tokenizer 完全冻结？ 目标路径停止梯度是防止预测目标跟随预测一起塌缩或移动，输入侧视觉 tokenizer 仍可通过 LM 与预测头接收梯度。模型在无字幕中期训练中学习视觉序列关系，之后需匹配的指令调优对照；不能把没有文字损失误解为整个视觉前端不训练。 例如用前一帧 patch 预测下一 patch，下一目标不反传，但前一输入经过的视觉参数仍可被预测误差更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-raw-video-midtraining-db4472b0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-cca299426ddfa506">目标侧 stop-gradient 为什么不意味着视觉 tokenizer 完全冻结？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Araw-video-midtraining">Mid-Training Language Models on Raw Video</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI / Massachusetts Institute of Technology</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标路径停止梯度是防止预测目标跟随预测一起塌缩或移动，输入侧视觉 tokenizer 仍可通过 LM 与预测头接收梯度。模型在无字幕中期训练中学习视觉序列关系，之后需匹配的指令调优对照；不能把没有文字损失误解为整个视觉前端不训练。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用前一帧 patch 预测下一 patch，下一目标不反传，但前一输入经过的视觉参数仍可被预测误差更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与原文效果；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.11019">原论文</a> · <a href="../../../../multimodal-models/2610.11019-raw-video-midtraining/">实现解读</a> · <a href="#qa-cca299426ddfa506">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:woven" data-paper-title="WOVEN: Weaving Visual World Modeling into Multimodal LLMs" data-learning-pending="false" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="WOVEN: Weaving Visual World Modeling into Multimodal LLMs 多模态大模型 Northwestern University 2026-10-08 静态识别不等于理解状态变化。WOVEN以为共同对象，用视频生成模型rollout提供结果/中间状态，而非在prompt里预写结果。相同初始状态在不同动作下的rollout提供counterfactual候选；按scene、action、reasoning三个轴形成可控监督，用error-typed distractors区分错误机制。该paper的核心是真实视觉转移监督进入MLLM训练，不是训练图片class scorer。 相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。本地对照口径：同一冻结公共VLM零LoRA残差为基线，真实transition response SFT为实验组；相对原论文benchmark不适用，source_id分组小样本accuracy只用于L1诊断。  multimodal-foundation-model visual-transition-reasoning world-model-supervision 多模态 视觉世界建模：状态、生成与动作条件 为什么要按初始场景或 source 分组切分，而不能随机拆散视觉转移问答？ 同一初始图像可以衍生多个动作、问题与反事实选项，随机按题切分可能把几乎相同的视觉状态放进训练和测试。分组隔离减少这种捷径，再区分场景、动作与推理操作的迁移；高同源问答分数不能自动说明理解了未知场景的状态变化。 例如同一桌面分别问“向左推会怎样”和“什么动作导致杯子移动”，两题共享底图，应作为一组切分而非分居训练测试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-woven-63239e78" class="ar-learning-paper-anchor"></span>
<h2 id="qa-507c29cd3a03e147">为什么要按初始场景或 source 分组切分，而不能随机拆散视觉转移问答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Awoven">WOVEN: Weaving Visual World Modeling into Multimodal LLMs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Northwestern University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一初始图像可以衍生多个动作、问题与反事实选项，随机按题切分可能把几乎相同的视觉状态放进训练和测试。分组隔离减少这种捷径，再区分场景、动作与推理操作的迁移；高同源问答分数不能自动说明理解了未知场景的状态变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一桌面分别问“向左推会怎样”和“什么动作导致杯子移动”，两题共享底图，应作为一组切分而非分居训练测试。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12417">原论文</a> · <a href="../../../../reproductions/2610.12417-woven/">实现解读</a> · <a href="#qa-507c29cd3a03e147">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vjepa-policy" data-paper-title="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents 基础模型 Tsinghua University 2026-09-29 冻结 V-JEPA 2.1 视觉编码器，在预测视觉潜空间中联合训练 instruction-conditioned future-latent predictor 和 flow-matching action expert；动作生成读取 predictor 的未来信息上下文。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。执行 future-latent stop-gradient 与 action flow matching；未加载 V-JEPA 2.1 或机器人数据。本地对照口径：基线为论文机制关闭或默认状态，实验组为开启对应核心算子；本批只验证不变量和状态转换，跨模型相对变化不适用。  世界动作模型 预测视觉潜变量 机器人 多模态 视觉世界建模：状态、生成与动作条件 动作专家读取预测未来潜变量，与直接读取训练视频未来帧有何区别？ 预测未来由当前观察与指令生成，部署时也能获得；真实未来仅作为训练目标，用于塑造预测器。动作 flow expert 因而使用可计算的前瞻上下文，而非提前观察结果。冻结视觉编码器稳定表示，却不保证预测误差不会在控制过程中累积。 例如根据当前桌面预测抓取后的杯子位置，再产生动作；不能把实际抓取结束后的照片先传给策略再评价成功率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-vjepa-policy-d720eedd" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b1dc62a377da6fe6">动作专家读取预测未来潜变量，与直接读取训练视频未来帧有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avjepa-policy">V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tsinghua University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预测未来由当前观察与指令生成，部署时也能获得；真实未来仅作为训练目标，用于塑造预测器。动作 flow expert 因而使用可计算的前瞻上下文，而非提前观察结果。冻结视觉编码器稳定表示，却不保证预测误差不会在控制过程中累积。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如根据当前桌面预测抓取后的杯子位置，再产生动作；不能把实际抓取结束后的照片先传给策略再评价成功率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.37250">原论文</a> · <a href="../../../../foundation-models/2609.37250-vjepa-policy/">实现解读</a> · <a href="#qa-b1dc62a377da6fe6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:vbvr-pro" data-paper-title="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning" data-learning-pending="false" data-domain="foundation-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning 基础模型 Nanyang Technological University / VBVR Community 2026-08-26 通用 VLM judge 容易被流畅输出误导，难以逐实例核对时空状态。VBVR-Pro 为每种任务定义可执行 scorer，把中间状态、约束和最终状态都变成可验证奖励，并据此训练多模态生成模型。 Fidelity：核心机制的程序化验证。本地复刻 task-specific deterministic scorer 与标量 judge 对照，不训练视频生成大模型。该结果只验证 scorer 的确定性和可解释失败归因，不等同于论文七个外部 benchmark 或 14B/19B checkpoint 训练。本地对照口径：基线为带噪标量 VLM-judge analogue；实验组为三个确定性 task-specific verifier。300 个程序化任务 reward mean 0.5942 → 1.0000（+68.30%）。  multimodal-foundation-model native-visual-reasoning verifiable-reward benchmark 多模态 视觉世界建模：状态、生成与动作条件 可执行 scorer 为什么比通用 VLM judge 更适合某些时空约束任务？ 任务若能明确列出中间状态、约束和最终条件，就可逐实例检查，而不只凭答案是否流畅判断。这样的奖励把可验证条件接入训练，但只覆盖已定义的规则；scorer 自身正确、被评模型不读 gold 与生成任务真正执行，仍是不同的验证要求。 例如移动方块不能穿墙且最终到达目标格，可逐步检查轨迹；一段听起来合理却实际穿墙的解释不应获得成功奖励。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-foundation-models-vbvr-pro-eb931970" class="ar-learning-paper-anchor"></span>
<h2 id="qa-3c05a2d2ce10e7f4">可执行 scorer 为什么比通用 VLM judge 更适合某些时空约束任务？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Avbvr-pro">VBVR-Pro: A Scalable and Verifiable Suite for Native Visual Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University / VBVR Community</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务若能明确列出中间状态、约束和最终条件，就可逐实例检查，而不只凭答案是否流畅判断。这样的奖励把可验证条件接入训练，但只覆盖已定义的规则；scorer 自身正确、被评模型不读 gold 与生成任务真正执行，仍是不同的验证要求。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如移动方块不能穿墙且最终到达目标格，可逐步检查轨迹；一段听起来合理却实际穿墙的解释不应获得成功奖励。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.26105">原论文</a> · <a href="../../../../reproductions/2608.26105-vbvr-pro/">实现解读</a> · <a href="#qa-3c05a2d2ce10e7f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="multimodal-models:mice" data-paper-title="Editing Everything Everywhere All at Once" data-learning-pending="false" data-domain="multimodal-models" data-theme="multimodal-models" data-topic="multimodal-models/world-state-actions" data-search="Editing Everything Everywhere All at Once 多模态大模型 University of Modena and Reggio Emilia 2026-06-30 多区域同时编辑容易把一处指令的属性传到另一处。MICE 在联合注意力中隔离不同文字组，并用实例掩码的平滑空间偏置控制视觉交互，以兼顾局部绑定与周围区域融合。方法不训练新的编辑模型。 以单张 A100/A30 或 Mac 的资源限制评估，完整矩阵需要大权重、长时间生成和外部服务，标注成本过高，不复现（审查 DONE）。诊断使用 2 个生成掩码、6×8 raster 和随机 Q/K/V，真实执行 attention 与反向传播。实现 instance_aware_masks、instance_log_bias、mice_joint_bias、mice_joint_attention 和统一 diagnostic(seed, device)。模块导入不加载 PyTorch，实际调用时才需要。输入必须是已经在同一网格上的、非空、互不重叠的二值 mask；  视觉生成与编辑 多实例编辑与注意力隔离 多模态 视觉世界建模：状态、生成与动作条件 多实例编辑为什么同时需要文字组隔离与平滑空间偏置？ 文字组隔离减少一条编辑指令直接影响另一组语义，空间偏置则把该指令绑定到相应实例并允许边界附近融合。只有硬切区域可能产生接缝，只有全局文字约束又可能串色；偏置在注意力里控制可见性，并不等于训练了一个新的编辑模型。 例如要求左鞋变红、右鞋变蓝，文字组不应互相传播颜色，而平滑实例区域帮助各自颜色与周围图像自然衔接。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">多模态 / 视觉世界建模：状态、生成与动作条件</a></p>
<span id="paper-multimodal-models-mice-b52a199b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-17c3380975ca6c68">多实例编辑为什么同时需要文字组隔离与平滑空间偏置？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=multimodal-models%3Amice">Editing Everything Everywhere All at Once</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Modena and Reggio Emilia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文字组隔离减少一条编辑指令直接影响另一组语义，空间偏置则把该指令绑定到相应实例并允许边界附近融合。只有硬切区域可能产生接缝，只有全局文字约束又可能串色；偏置在注意力里控制可见性，并不等于训练了一个新的编辑模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如要求左鞋变红、右鞋变蓝，文字组不应互相传播颜色，而平滑实例区域帮助各自颜色与周围图像自然衔接。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2606.31278v1">原论文</a> · <a href="../../../../multimodal-models/2606.31278-mice/">实现解读</a> · <a href="#qa-17c3380975ca6c68">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

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

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
