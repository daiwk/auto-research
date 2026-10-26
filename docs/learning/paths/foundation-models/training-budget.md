---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 训练预算：数据配比、目标与优化器

[基础模型](index.md) / 28 个问题 · 28 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<p class="ar-learning-status" data-learning-status role="status">28 个问题 · 28 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lazyflash" data-paper-title="LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning 基础模型 Microsoft 2026-10-22 与稀疏前向attention不同，LazyFlash保留训练和部署前向完全dense。它按query block的dO Frobenius范数衡量梯度贡献，用gradient-mass budget约束预计丢弃量，并importance采样反向block。必须在tiled FlashAttention反向内部跳过内存访问/计算，才能兑现论文速度；用PyTorch dense backward后置零或toy mask不构成该方法的低成本完整实现。 成本过高，不复现（审查 DONE）。原文8张H200、65,536长度、2500steps，多个Qwen3模型和语音50K小时训练数据；所有计时在H200。自定义FlashAttention反向kernel及跨长度/模型/精度验证本身也超过本轮单卡低成本范围。不安装/编译kernel或加载权重来“试试”。无本地operator、metrics或GPUreceipt；无capability/evolve声明。原方法的定义性产物是可执行的tiled backward kernel，本轮不以通用softmax/mask代理充数。已读方法、实验及附录后终结完整复现成本审查。  推理与系统效率 长上下文训练 基础模型 训练预算：数据配比、目标与优化器 LazyFlash前向仍是dense，为什么训练加速来自反向，而不是减少可见上下文？ 它保持前向完整注意力，用输出梯度的块范数分配反向保留概率，再对采样块按概率倒数重加权，估计dense梯度。要真正节省时间，必须在tiled反向内核里跳过相应访存与计算。先完整反传再把梯度置零，不具备同样成本；单次随机梯度也不会逐元素等于dense。 教学例子：某query块的梯度贡献很小，可降低其反向执行概率；前向仍看过全部证据。只有没有实际执行被跳过块的反向工作，才可能获得相应速度收益。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-lazyflash-43455fcb" class="ar-learning-paper-anchor"></span>
<h2 id="qa-73f4f2504e86cd44">LazyFlash前向仍是dense，为什么训练加速来自反向，而不是减少可见上下文？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alazyflash">LazyFlash: Forward-Dense, Backward-Sparse Attention for Accelerated Long-Context Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Microsoft</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它保持前向完整注意力，用输出梯度的块范数分配反向保留概率，再对采样块按概率倒数重加权，估计dense梯度。要真正节省时间，必须在tiled反向内核里跳过相应访存与计算。先完整反传再把梯度置零，不具备同样成本；单次随机梯度也不会逐元素等于dense。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某query块的梯度贡献很小，可降低其反向执行概率；前向仍看过全部证据。只有没有实际执行被跳过块的反向工作，才可能获得相应速度收益。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.31911v1">原论文</a> · <a href="../../../../foundation-models/2610.31911-lazyflash/">实现解读</a> · <a href="#qa-73f4f2504e86cd44">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:rkl-policy-distillation" data-paper-title="Reverse-KL Policy Distillation: Statistical Guarantees and Limits" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Reverse-KL Policy Distillation: Statistical Guarantees and Limits 基础模型 University of Virginia 2026-10-22 反向 KL 的风险取决于候选策略自己的访问分布。仅在过往 rollout 状态上重新拟合 token KL，会把“候选自己很少到达的状态”算得过重。本文的在线 full-feedback Algorithm 1 同时截断累计 KL 和前缀重要性比，通过有界候选/rollout 比较更新策略空间中的指数权重。 状态为 not_run_scope_limited_protocol，不是“成本过高”或“已实证验证”。bounded_prefix_comparisons 实现 Eq.2/Eq.6；exponential_weights 固定 1/256；learn_online 实现 Algorithm 1。teacher 接口只能按 (h,state) 查询完整动作分布，每 episode 恰好查询次，不接收全局风险、最优候选或 gold trajectory。evaluate_exact_moments 是独立评估入口，用有限状态前向概率递推精确计算、和该 fixture 的最小可用；只能在训练返回之后运行。  策略蒸馏理论 有限策略空间在线学习 基础模型 训练预算：数据配比、目标与优化器 反向KL蒸馏为何不能只在旧rollout状态上重拟合token KL？ 目标风险按候选策略自己的访问分布计算，旧策略频繁到达的状态可能被候选很少访问。该算法用截断的前缀重要性比与累计KL增量，构造有界候选比较，再更新整条策略的权重。前缀比不包含当前动作，同一个比值要乘在比较差的两项上；这与普通旧数据KL回归不同。 教学例子：旧策略常走一条失败支路，新候选几乎不会进入；不修正访问分布，就可能把这条支路上的token误差算得过重，掩盖候选真正会遇到的状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-rkl-policy-distillation-fa9bc42e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c10cf8835375ff57">反向KL蒸馏为何不能只在旧rollout状态上重拟合token KL？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Arkl-policy-distillation">Reverse-KL Policy Distillation: Statistical Guarantees and Limits</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Virginia</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标风险按候选策略自己的访问分布计算，旧策略频繁到达的状态可能被候选很少访问。该算法用截断的前缀重要性比与累计KL增量，构造有界候选比较，再更新整条策略的权重。前缀比不包含当前动作，同一个比值要乘在比较差的两项上；这与普通旧数据KL回归不同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旧策略常走一条失败支路，新候选几乎不会进入；不修正访问分布，就可能把这条支路上的token误差算得过重，掩盖候选真正会遇到的状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30844v1">原论文</a> · <a href="../../../../foundation-models/2610.30844-rkl-policy-distillation/">实现解读</a> · <a href="#qa-c10cf8835375ff57">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:t-muon" data-paper-title="T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training 基础模型 University of California, Santa Barbara 2026-10-18 普通 Muon 逐矩阵求 polar。本文先把结构相关矩阵放进三阶张量，再在第三轴变换域分别求 polar；这不是把张量任意展平后运行普通 Muon。分组方式与变换方式是两个独立选择：论文比较相邻层、QKV、单矩阵的 head、QKV 的 head-stack。 与单张 A100/A30 或本地 Mac 的低成本验证目标不匹配，完整训练成本过高，不复现（审查 DONE）。CPU与真实单张A100均完成42/43/44三seed的FP64数值、梯度和参数更新诊断。CPU与真实单张A100均完成42/43/44三seed的FP64数值、梯度和参数更新诊断。A100的polar参考误差均值约1.31e-14、参数更新参考误差约1.34e-16；只证明小矩阵实现一致，不证明论文PPL改善、预训练稳定性或内核加速。见实际指标和GPU回执，执行源码绑定冻结提交324217ed26fe2e297e25879ad092281eb0960b87。  预训练与数据 优化器与张量几何 基础模型 训练预算：数据配比、目标与优化器 T-MUON为何先把相关矩阵组成三阶张量，而不是直接展平后做普通Muon？ 它在第三轴的变换域中分别求polar，再逆变换回各矩阵，使结构相关矩阵能够在该轴上耦合。矩阵如何分组与选择什么变换是独立设计，任意展平会丢掉这层定义。还原后的形状缩放依据原矩阵，零秩切片不能因任意零空间基产生虚假更新。 教学例子：把相邻层或Q/K/V作为第三轴的几片，先在该轴混合再分别正交化，与把所有数拼成一张长矩阵正交化，约束和结果都不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-t-muon-99464230" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1d73398509874a34">T-MUON为何先把相关矩阵组成三阶张量，而不是直接展平后做普通Muon？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3At-muon">T-MUON: Tensorizing Muon via t-SVD for Large Language Model Pre-training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它在第三轴的变换域中分别求polar，再逆变换回各矩阵，使结构相关矩阵能够在该轴上耦合。矩阵如何分组与选择什么变换是独立设计，任意展平会丢掉这层定义。还原后的形状缩放依据原矩阵，零秩切片不能因任意零空间基产生虚假更新。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把相邻层或Q/K/V作为第三轴的几片，先在该轴混合再分别正交化，与把所有数拼成一张长矩阵正交化，约束和结果都不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.24938">原论文</a> · <a href="../../../../foundation-models/2610.24938-t-muon/">实现解读</a> · <a href="#qa-1d73398509874a34">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bmuon" data-paper-title="BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility 基础模型 Inria 2026-10-16 Muon的spectral-norm更新不一定产生容易按隐藏通道剪枝的权重。BMuon不在前向额外加gate，也不只是对训练好的Muon模型剪枝；它让所有MLP块的隐藏通道共享同一分配预算，并在每个通道的输入行/输出列两侧共同改变更新几何。原文Figure 1展示结构化剪枝结果；核心方法最直接的来源为Algorithm1和Eq7/8。该结果图不是本地测量。 完整实验成本过高，不复现（审查 DONE）。BudgetMuon接受多个真实配对MLP，执行梯度、Nesterov动量、全局预算MM及双边参数更新。当前采用小矩阵精确SVD polar，不是原文生产实现的5步Newton–Schulz；不宣称运行速度相同。支持FP32/FP64；FP16/BF16明确拒绝，不默许低精度数值问题。缺失一侧梯度也拒绝，避免破坏通道耦合。  预训练与数据 优化器与结构化可压缩性 基础模型 训练预算：数据配比、目标与优化器 BMuon的通道预算为什么要跨全部MLP共享，还同时作用于输入行和输出列？ 一个隐藏通道由输入矩阵的一行和输出矩阵的一列共同定义；只改变一侧不完整。BMuon让所有MLP通道竞争同一总分配预算，并在两侧的Muon更新几何中使用该分配，使不同层之间也能重新分配可压缩性。它是在训练更新中塑造结构，不是额外前向gate或事后各层独立剪枝。 教学例子：总共只留100份通道预算时，两层不必各拿50；更有贡献的一层可拿更多，但每个通道的入边和出边都应按同一分配一起处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-bmuon-2e7cc5f8" class="ar-learning-paper-anchor"></span>
<h2 id="qa-90c13d183e56fedd">BMuon的通道预算为什么要跨全部MLP共享，还同时作用于输入行和输出列？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abmuon">BMuon: Budgeting Muon&#x27;s Spectral Geometry for Structured Compressibility</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Inria</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个隐藏通道由输入矩阵的一行和输出矩阵的一列共同定义；只改变一侧不完整。BMuon让所有MLP通道竞争同一总分配预算，并在两侧的Muon更新几何中使用该分配，使不同层之间也能重新分配可压缩性。它是在训练更新中塑造结构，不是额外前向gate或事后各层独立剪枝。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>总共只留100份通道预算时，两层不必各拿50；更有贡献的一层可拿更多，但每个通道的入边和出边都应按同一分配一起处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23571">原论文</a> · <a href="../../../../foundation-models/2610.23571-bmuon/">实现解读</a> · <a href="#qa-90c13d183e56fedd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:bit-sparse" data-paper-title="BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks 基础模型 University of Cambridge 2026-10-15 ReLU 家族已有大量精确零；BitSparse 保存 bitmask、正值和 tile prefix，在反向时无损重建，避免靠有损量化或额外前向换空间。§3 定义格式，公式 1–2 与 Appendix C 定义 ReLU/ReLU² 线性层反向。 按原文 RTX3090 约 7.4–7.7秒/步×3350 步推算单臂约 7小时，成本过高，不复现（审查 DONE）；CUDA诊断记录与真实GPU回执保存设备、种子及执行源码身份。无模型或数据下载。三个 seed 的合成输入 revision 为 synthetic-formula-and-bit-patterns@oct17-foundation-components-v1。BF16 33×37 激活检验含 padding 的 tile 格式；另以双精度 9×13 输入、7×13 权重做独立 dense 前向/反向参考。tile 8 是有意缩小的格式验收，不是原文默认 tile64 的性能测试。  训练与系统效率 无损激活压缩 基础模型 训练预算：数据配比、目标与优化器 BitSparse为什么可以无损减少激活存储，却不需要额外重跑一次前向？ ReLU家族激活已有精确零，方法只保存非零值、每位置一bit的mask与分块前缀，反向时重建原激活。它利用结构性零而非降低非零值精度，也不靠重新计算补回丢掉的信息。能否节省空间取决于零比例和元数据成本，不能只看到用了bitmask就忽略仍需保存的正值。 教学例子：8个激活中6个为零，可保存8位mask加2个原精度数值；反向按mask把两个数放回原位，不必再次执行生成这些激活的网络。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-bit-sparse-b3242cb0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8d6a729d709d628c">BitSparse为什么可以无损减少激活存储，却不需要额外重跑一次前向？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Abit-sparse">BitSparse: Compact Activation Storage for ReLU Feed-Forward Networks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>ReLU家族激活已有精确零，方法只保存非零值、每位置一bit的mask与分块前缀，反向时重建原激活。它利用结构性零而非降低非零值精度，也不靠重新计算补回丢掉的信息。能否节省空间取决于零比例和元数据成本，不能只看到用了bitmask就忽略仍需保存的正值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>8个激活中6个为零，可保存8位mask加2个原精度数值；反向按mask把两个数放回原位，不必再次执行生成这些激活的网络。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22256">原论文</a> · <a href="../../../../foundation-models/2610.22256-bit-sparse/">实现解读</a> · <a href="#qa-8d6a729d709d628c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hardware-diversity" data-paper-title="Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs 基础模型 Meta 2026-10-15 CUDA 程序能够转换为 HIP，不代表跨硬件性能相同。本文以推荐训练为案例，联合修改模型/并行与内存策略，用分析模型选择 GEMM 配置，并用 Agent 辅助编译、调试和内核移植；它是系统研究报告，而非单一新推荐模型。 成本过高且硬件不匹配，不复现（审查 DONE）。研究资料；成本过高且硬件不匹配，不复现（审查 DONE）。不下载生产模型、不尝试集群训练，不注册可执行 adapter，不接入 Evolve；下文结果均来自论文，不是本地 GPU 测量。状态为成本过高，不复现（审查 DONE），不是待自动重试 TODO，也不是算法已实现。资料收录不阻塞其他组件或审查水位；若以后明确要求实现某个公开算子，应重新界定该算子、硬件和验证合同，不冒充完整生产系统复现。本轮仅完成元数据、正文与成本审查。原配置依赖 MI350X/B200 集群和私有工作负载，现有一张 A100 或 A30 无法等价复现；不启动下载、性能探跑或完整训练。  训练系统 硬件模型协同设计 推荐训练系统 基础模型 训练预算：数据配比、目标与优化器 CUDA代码转成HIP后能运行，为什么还不能认为跨硬件性能已经迁移？ 接口兼容只解决能否执行；计算单元、内存层次、tile形状与并行策略会改变实际瓶颈。该研究联合模型、内存、并行与内核选型，并用分析模型估计计算、访存和尾部空转。硬件常数与最佳配置依设备而变，不能把一张卡的选型结果直接搬到另一张卡当作已测加速。 教学例子：同一个GEMM tile在一类设备上充分占满计算单元，换设备后却可能受共享内存或尾部工作量限制；成功编译并不会自动修复这种布局不匹配。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-hardware-diversity-2c171dec" class="ar-learning-paper-anchor"></span>
<h2 id="qa-1a1c64a8f0514de8">CUDA代码转成HIP后能运行，为什么还不能认为跨硬件性能已经迁移？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahardware-diversity">Architecting for Hardware Diversity: Meta&#x27;s End-to-End Co-Design for High-Performance AI Training on AMD GPUs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>接口兼容只解决能否执行；计算单元、内存层次、tile形状与并行策略会改变实际瓶颈。该研究联合模型、内存、并行与内核选型，并用分析模型估计计算、访存和尾部空转。硬件常数与最佳配置依设备而变，不能把一张卡的选型结果直接搬到另一张卡当作已测加速。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一个GEMM tile在一类设备上充分占满计算单元，换设备后却可能受共享内存或尾部工作量限制；成功编译并不会自动修复这种布局不匹配。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22230">原论文</a> · <a href="../../../../foundation-models/2610.22230-hardware-diversity/">实现解读</a> · <a href="#qa-1a1c64a8f0514de8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:lct" data-paper-title="LCT: Losslessly Compressed Tensors with GPU friendly execution for Training" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="LCT: Losslessly Compressed Tensors with GPU friendly execution for Training 基础模型 University of Cambridge 2026-10-15 浮点指数往往比 sign/mantissa 更可压缩，但训练需要反复编码。LCT 将两部分分开，以固定模型预计算短码，运行时中心变换适应量级，循环 stream 在固定预算之外保留原始指数尾。主源 §4、Appendix B/C；不是用通用 zlib 压缩替代算法。 完整链路成本过高，不复现（审查 DONE），不启动探跑；CUDA诊断记录与真实GPU回执保存设备、种子与源码身份。不下载模型或语料。revision synthetic-formula-and-bit-patterns@oct17-foundation-components-v1，seeds42/43/44。使用公开定义的合成 BF16 位模式：512个元素中的前256个覆盖所有指数，另改变 sign/fraction；固定码表模型不是根据测试输入拟合。16 streams×32-bit预算故意产生 overflow；另以充足预算及其他中心检查还原。  训练与系统效率 无损浮点编码 基础模型 训练预算：数据配比、目标与优化器 LCT压缩指数时，罕见符号或stream超预算为什么也不能丢掉？ 目标是逐bit可还原，因此罕见指数使用escape加原始符号，流预算耗尽后的剩余项进入原始指数尾。sign与fraction部分单独保留，固定码表避免反复学习编码。它是在可压缩部分和回退路径之间组织存储，而不是通过舍弃低概率值变成有损量化。 教学例子：常见指数用短码，遇到罕见指数先写escape再写原8位；即使压缩流满了，余下指数仍原样保存，不能为了达到目标大小就把它们改成零。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-lct-f385814a" class="ar-learning-paper-anchor"></span>
<h2 id="qa-74b7ca86cd3c25c0">LCT压缩指数时，罕见符号或stream超预算为什么也不能丢掉？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Alct">LCT: Losslessly Compressed Tensors with GPU friendly execution for Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是逐bit可还原，因此罕见指数使用escape加原始符号，流预算耗尽后的剩余项进入原始指数尾。sign与fraction部分单独保留，固定码表避免反复学习编码。它是在可压缩部分和回退路径之间组织存储，而不是通过舍弃低概率值变成有损量化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>常见指数用短码，遇到罕见指数先写escape再写原8位；即使压缩流满了，余下指数仍原样保存，不能为了达到目标大小就把它们改成零。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22179">原论文</a> · <a href="../../../../foundation-models/2610.22179-lct/">实现解读</a> · <a href="#qa-74b7ca86cd3c25c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muon-paired-budget" data-paper-title="When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark 基础模型 论文未列一作机构 2026-10-15 优化器每步效果更好不等于同时间更好，也不意味着更容易调参。论文在单A100上对齐初始化、数据顺序和开发候选数，分别比较数据、训练时间、冻结调参池三种预算。它不是新的Muon优化公式，主要贡献是谨慎分离比较口径。测试数据在选参和轨迹分析冻结后只评一次。 按可用单卡预算，完整实验成本过高，不复现（审查 DONE）。三种子是协议随机性诊断，不是模型稳定提升。不训练Muon/AdamW、不下载FineWeb/CIFAR。固定合成轨迹revision synthetic-agent-cards-and-validation-trajectories@oct17-supplement-protocols-v1，seeds42/43/44；每seed构造可手算的分段线性validation曲线、较慢但等数据更优的替代策略、三个合成配对replication IDs，以及23个固定候选AUC。三种子是协议随机性诊断，不是模型稳定提升。  优化与训练效率 公平预算评测协议 基础模型 训练预算：数据配比、目标与优化器 Muon同样步数下更低loss，为什么仍不足以宣布同算力或同调参成本更优？ 每步耗时、数据吞吐和调参开销可能不同。配对基准固定初始化、数据顺序与候选池，分别按已处理数据、实际训练时间和冻结调参预算比较；参数只在开发阶段选择，测试冻结后读取。相同步数只是一个横轴，不能代替另外两种成本口径。 教学例子：A每步进步更大但耗时翻倍，100步更好不代表十分钟内更好；若又为时间指标单独重挑A的最佳配置，就混入了额外调参优势。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-muon-paired-budget-6bbbedd2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-01050f98565ed331">Muon同样步数下更低loss，为什么仍不足以宣布同算力或同调参成本更优？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuon-paired-budget">When Does Muon Actually Win? A Paired Data-, Time-, and Tuning-Budget Benchmark</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 论文未列一作机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每步耗时、数据吞吐和调参开销可能不同。配对基准固定初始化、数据顺序与候选池，分别按已处理数据、实际训练时间和冻结调参预算比较；参数只在开发阶段选择，测试冻结后读取。相同步数只是一个横轴，不能代替另外两种成本口径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>A每步进步更大但耗时翻倍，100步更好不代表十分钟内更好；若又为时间指标单独重挑A的最佳配置，就混入了额外调参优势。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21555">原论文</a> · <a href="../../../../foundation-models/2610.21555-muon-paired-budget/">实现解读</a> · <a href="#qa-01050f98565ed331">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:smrc-pmrc" data-paper-title="Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon 基础模型 Nanjing University / Alibaba Token Hub 2026-10-14 低秩优化器只存投影后的动量，能减少持久状态；但梯度主奇异方向可能被噪声占据，直接丢掉子空间外分量会遗漏有效下降方向。本文让低秩动量负责投影内更新，原始梯度的正交残差负责其余方向，不额外保存一个全尺寸残差状态。SMRC 使用 EMA 动量，PMRC 对低维动量取矩阵符号；二者不能简单替换成同一个“投影 SGD”。 完整实验：成本过高，不复现（审查 DONE）。L1 组件诊断。Fidelity: 核心机制复现；L1 组件诊断。这里交付可直接更新真实参数的 PyTorch 优化器和有界验证入口，不代表完整 LLM 预训练、SFT 或论文大规模效果已复现。完整实验：成本过高，不复现（审查 DONE）。本地对照口径：基线为全空间 EMA-SGD、精确矩阵符号 Muon 和 AdamW，实验组为 SMRC、理论 PMRC、实用 PMRC；参数初始化、梯度噪声/输入与更新次数一致；固定小预算，仅作机制诊断，跨算法下游效果相对提升不适用。  llm-training optimizer training-efficiency 基础模型 训练预算：数据配比、目标与优化器 SMRC/PMRC只存低秩动量，怎样补上子空间外的有效梯度？ 投影内部分由低维动量更新，当前原始梯度的正交残差提供其余方向，不额外持久保存全尺寸残差状态。SMRC对低维动量作EMA，PMRC还改变矩阵方向处理；换基时二者规则也不同。节省动量存储不意味着可以把残差删掉，或把两种方法都简化成同一个投影SGD。 教学例子：主要子空间抓住两个高能方向，但较小的第三方向仍有下降信息；用当前梯度残差补这部分，同时无需为它再保留一整张长期动量矩阵。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-smrc-pmrc-96d2a34c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-00d2545fa87f1553">SMRC/PMRC只存低秩动量，怎样补上子空间外的有效梯度？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Asmrc-pmrc">Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanjing University / Alibaba Token Hub</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>投影内部分由低维动量更新，当前原始梯度的正交残差提供其余方向，不额外持久保存全尺寸残差状态。SMRC对低维动量作EMA，PMRC还改变矩阵方向处理；换基时二者规则也不同。节省动量存储不意味着可以把残差删掉，或把两种方法都简化成同一个投影SGD。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>主要子空间抓住两个高能方向，但较小的第三方向仍有下降信息；用当前梯度残差补这部分，同时无需为它再保留一整张长期动量矩阵。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19844">原论文</a> · <a href="../../../../reproductions/2610.19844-smrc-pmrc/">实现解读</a> · <a href="#qa-00d2545fa87f1553">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:adamw4bit" data-paper-title="Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization 基础模型 University of California, Berkeley / Nubank 2026-10-08 AdamW 的量化误差会进入后续矩递推。ZIP-SR 在预条件器空间随机舍入第二矩；ZE-EDEN 排除零码点并校准块尺度。两者使用 NF4 第一矩，训练末尾 10% 对 LM head 第一矩随机舍入。原文 真实训练使用公开数据，但本批产物按 L1 有界机制诊断登记；WikiText-2 官方 train/valid/test；字节 tokenizer，训练前 100 万字节，验证和测试仅评估固定 16 个 64-token 片段。相同初始化、批次、200 步、学习率和模型结构；所有方案统一使用独立 LM head。仅以验证集选方案，选定后才打开 test。  训练优化与稳定性 低精度训练 基础模型 训练预算：数据配比、目标与优化器 4-bit AdamW为什么要在预条件器空间控制第二矩舍入，而不只让第二矩数值接近？ 第二矩经过偏差校正、开平方和取倒数后才影响更新，原数值上相近的误差在这个非线性映射后可能不等价。ZIP-SR据预条件器值决定随机舍入概率，ZE-EDEN则处理码点与尺度；状态误差还会进入后续递推。当前工作矩先用于参数更新，再量化存储，顺序也属于机制。 教学例子：两个很小的第二矩数值只有一点差别，取倒数平方根后却可能明显改变步长；应保护实际乘到梯度上的尺度，而不只比较压缩前后的均方误差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-adamw4bit-715c8ec7" class="ar-learning-paper-anchor"></span>
<h2 id="qa-c8a13b370455cc00">4-bit AdamW为什么要在预条件器空间控制第二矩舍入，而不只让第二矩数值接近？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aadamw4bit">Rounding in Preconditioner Space: Redesigning 4-bit AdamW Optimizer-State Quantization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Berkeley / Nubank</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第二矩经过偏差校正、开平方和取倒数后才影响更新，原数值上相近的误差在这个非线性映射后可能不等价。ZIP-SR据预条件器值决定随机舍入概率，ZE-EDEN则处理码点与尺度；状态误差还会进入后续递推。当前工作矩先用于参数更新，再量化存储，顺序也属于机制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个很小的第二矩数值只有一点差别，取倒数平方根后却可能明显改变步长；应保护实际乘到梯度上的尺度，而不只比较压缩前后的均方误差。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12444">原论文</a> · <a href="../../../../foundation-models/2610.12444-adamw4bit/">实现解读</a> · <a href="#qa-c8a13b370455cc00">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:af-muon" data-paper-title="AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models 基础模型 原文首页未列第一作者机构 2026-10-01 矩阵继续用 Muon 谱范数方向，稀疏输入查表与稠密输出分类器共享的词表采用 support-aware 有限帽 LMO，一维参数用 RMS 更新。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行词表 support/cap 方向；未完成论文规模预训练。执行词表 support/cap 方向；未完成论文规模预训练。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  优化器 Muon 显存效率 基础模型 训练预算：数据配比、目标与优化器 AF-Muon为何不能把tied embedding当普通隐藏矩阵统一做Muon更新？ 共享词表同时承担稀疏输入查表与稠密输出分类，两种梯度结构并不相同。AF-Muon对隐藏矩阵保留Muon式谱方向，对共享词表使用support-aware有限帽方向，对一维参数另用RMS更新。不能仅按输入中出现的词判断支持集，因为输出分类路径也可能给许多词表行提供梯度。 教学例子：一个词没在输入中出现，却作为输出候选受到分类损失影响；若只更新输入命中的行，就会漏掉共享输出头的有效梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-af-muon-b7027d08" class="ar-learning-paper-anchor"></span>
<h2 id="qa-bc1646d03073e9ba">AF-Muon为何不能把tied embedding当普通隐藏矩阵统一做Muon更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aaf-muon">AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共享词表同时承担稀疏输入查表与稠密输出分类，两种梯度结构并不相同。AF-Muon对隐藏矩阵保留Muon式谱方向，对共享词表使用support-aware有限帽方向，对一维参数另用RMS更新。不能仅按输入中出现的词判断支持集，因为输出分类路径也可能给许多词表行提供梯度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个词没在输入中出现，却作为输出候选受到分类损失影响；若只更新输入命中的行，就会漏掉共享输出头的有效梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01395">原论文</a> · <a href="../../../../foundation-models/2610.01395-af-muon/">实现解读</a> · <a href="#qa-bc1646d03073e9ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:taco-optimizer" data-paper-title="TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning 基础模型 University of Central Florida 2026-10-01 每个二维权重列只保留绝对值最大的梯度分量及符号，形成 column-wise one-sparse steepest direction；低精度列状态替代逐参数 dense optimizer state。 未复现 13B/32B 全参微调或论文精度。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。执行一稀疏方向与低精度列 momentum，并在 A100 上验证 CUDA 更新；未复现 13B/32B 全参微调或论文精度。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  优化器 显存效率 全参微调 基础模型 训练预算：数据配比、目标与优化器 TACO每列只保留一个梯度位置，为什么不是普通的逐元素sign更新？ 它先在每个二维权重列中找绝对值最大的分量，只保留该位置的符号，其余位置更新为零。这样得到列级one-sparse方向，并配合低精度列状态减少优化器存储。逐元素sign则会更新所有非零梯度位置，既不是同一方向，也不具有相同稀疏结构。 教学例子：一列梯度为0.2、负0.9、0.4时，该列只在第二行给负方向；普通sign会同时给出正、负、正三个更新。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-taco-optimizer-aae79ac1" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f73d70ba75b1e7db">TACO每列只保留一个梯度位置，为什么不是普通的逐元素sign更新？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ataco-optimizer">TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Central Florida</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它先在每个二维权重列中找绝对值最大的分量，只保留该位置的符号，其余位置更新为零。这样得到列级one-sparse方向，并配合低精度列状态减少优化器存储。逐元素sign则会更新所有非零梯度位置，既不是同一方向，也不具有相同稀疏结构。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一列梯度为0.2、负0.9、0.4时，该列只在第二行给负方向；普通sign会同时给出正、负、正三个更新。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02199">原论文</a> · <a href="../../../../foundation-models/2610.02199-taco-optimizer/">实现解读</a> · <a href="#qa-f73d70ba75b1e7db">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:tess" data-paper-title="TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic) 基础模型 Nanyang Technological University 2026-10-01 先分别训练仅看训练集的模型和加入验证集指导的模型，以两者逐样本损失差构造价值伪标签；再用 pointwise value matching 训练数据 selector。避免直接选择目标的病态优化，并让小规模教师产生的选样规则迁移到更大的未见数据池。 L1 顺序训练与选样目标诊断：真实训练两份小模型和 selector；L1 顺序训练与选样目标诊断：真实训练两份小模型和 selector；没有声称复现大模型数据选择收益。本地二维合成分类特征代替论文语言模型和指令样本特征；只验证顺序训练、伪标签和 selector 学习。完整 LLM 数据池评分、重训练及质量收益尚未验证，不作为正式 Evolve 数据选择算子。PYTHONPATH=src python scripts/run_oct04_seven_papers.py 生成互不重用的 64 个训练、32 个验证、48 个池样本；两分类器各训练 60 步、selector 120 步，三 seed。  预训练与数据 元网络数据选择 基础模型 训练预算：数据配比、目标与优化器 TESS为什么先用两模型损失差作伪标签，再训练selector，而不直接优化选择结果？ 一份模型只看训练数据，另一份得到验证目标指导；同初始化下的逐样本损失差提供价值信号，再用pointwise匹配训练可迁移selector。两阶段设计把价值估计与选择器学习分开，避免某些直接选择目标的病态优化。验证信息用于开发指导，不能把最终test偷偷当作这份指导数据。 教学例子：同一个样本在普通模型与验证指导模型上的损失变化不同，可用来学习哪些样本更贴近目标；上线选择新数据时则由selector预测，而非逐样本读取未来测试成绩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-tess-5d7b0b3c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-b2d1ae7150fa0a51">TESS为什么先用两模型损失差作伪标签，再训练selector，而不直接优化选择结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Atess">TESS: Scalable, Transferable Meta-network for Data Selection Requires a Different Loss (and Why the Obvious Choice is Problematic)</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Nanyang Technological University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一份模型只看训练数据，另一份得到验证目标指导；同初始化下的逐样本损失差提供价值信号，再用pointwise匹配训练可迁移selector。两阶段设计把价值估计与选择器学习分开，避免某些直接选择目标的病态优化。验证信息用于开发指导，不能把最终test偷偷当作这份指导数据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一个样本在普通模型与验证指导模型上的损失变化不同，可用来学习哪些样本更贴近目标；上线选择新数据时则由selector预测，而非逐样本读取未来测试成绩。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.02092">原论文</a> · <a href="../../../../foundation-models/2610.02092-tess/">实现解读</a> · <a href="#qa-b2d1ae7150fa0a51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:open-1b-audit" data-paper-title="OPEN-1B: A Fully Auditable Training Run" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="OPEN-1B: A Fully Auditable Training Run 基础模型 Gensyn 2026-09-15 固定 kernel reduction、数据批次与集体通信顺序，并用逐步状态哈希支持异构硬件单步重放审计。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。本地验证固定顺序 reduction 与 canonical hash；不是 400B-token 预训练重放。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不能进入正式能力排名。  可复现训练 训练审计 基础模型 训练预算：数据配比、目标与优化器 只固定随机种子，为何还不足以审计一次预训练能否逐步重放？ 数据批次、kernel归约与集体通信顺序也会影响浮点计算轨迹。OPEN-1B把这些执行条件与逐步状态哈希一起记录，用单步重放定位差异，而不只比较最终loss。状态哈希能发现不一致，但不能自动解释差异来源，也不等于换硬件后天然逐bit相同。 教学例子：同样梯度项换一种求和顺序就可能产生小数值差；若只保存seed，难以知道差异从哪一步开始，逐步哈希与执行顺序记录可帮助缩小范围。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-open-1b-audit-631edf79" class="ar-learning-paper-anchor"></span>
<h2 id="qa-eeaeefec1cc1f4e2">只固定随机种子，为何还不足以审计一次预训练能否逐步重放？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopen-1b-audit">OPEN-1B: A Fully Auditable Training Run</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Gensyn</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>数据批次、kernel归约与集体通信顺序也会影响浮点计算轨迹。OPEN-1B把这些执行条件与逐步状态哈希一起记录，用单步重放定位差异，而不只比较最终loss。状态哈希能发现不一致，但不能自动解释差异来源，也不等于换硬件后天然逐bit相同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同样梯度项换一种求和顺序就可能产生小数值差；若只保存seed，难以知道差异从哪一步开始，逐步哈希与执行顺序记录可帮助缩小范围。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与实现对应；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17380">原论文</a> · <a href="../../../../foundation-models/2609.17380-open-1b-audit/">实现解读</a> · <a href="#qa-eeaeefec1cc1f4e2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:musec" data-paper-title="Musec: MomentUm SpEctral Clipping for Stable Muon-type Training" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Musec: MomentUm SpEctral Clipping for Stable Muon-type Training 基础模型 National University of Singapore 2026-09-10 对 Muon momentum 的奇异值做平滑谱裁剪，避免硬截断不连续，同时限制不稳定大方向。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。本地执行完整 SVD soft clipping reference；未复刻大模型训练吞吐。三种子指标见 metrics/mechanism-seeds42-44.json。所有候选使用相同公开 fixture、预算和 seed；本页结果只证明核心状态转换实际执行。  优化器 谱裁剪 基础模型 训练预算：数据配比、目标与优化器 Musec的谱裁剪与把所有梯度统一缩小，有什么区别？ 谱裁剪作用于动量矩阵的奇异值，重点限制不稳定的大方向，并用平滑处理避免硬阈值附近的不连续。统一缩放则同时压小所有方向，无法表达这种选择性。它控制的是更新几何；稳定性与最终优化质量仍需分开验证，不能由范数受控直接推出任务效果更好。 教学例子：一个矩阵方向特别大、其他方向正常；谱处理可以主要约束异常方向，而整体乘0.1会连正常方向也一起缩得很小。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-musec-4d47b01b" class="ar-learning-paper-anchor"></span>
<h2 id="qa-42029f8a35e58893">Musec的谱裁剪与把所有梯度统一缩小，有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amusec">Musec: MomentUm SpEctral Clipping for Stable Muon-type Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · National University of Singapore</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>谱裁剪作用于动量矩阵的奇异值，重点限制不稳定的大方向，并用平滑处理避免硬阈值附近的不连续。统一缩放则同时压小所有方向，无法表达这种选择性。它控制的是更新几何；稳定性与最终优化质量仍需分开验证，不能由范数受控直接推出任务效果更好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个矩阵方向特别大、其他方向正常；谱处理可以主要约束异常方向，而整体乘0.1会连正常方向也一起缩得很小。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式或操作；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.11655">原论文</a> · <a href="../../../../foundation-models/2609.11655-musec/">实现解读</a> · <a href="#qa-42029f8a35e58893">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:hilp" data-paper-title="Hierarchical Latent Prediction for Language Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Hierarchical Latent Prediction for Language Models 基础模型 University of Texas at Austin 2026-08-06 主题：分层 latent 预训练。NextLat 的逐步 latent rollout 会累积误差。HiLP 增加更粗粒度的抽象 latent 目标，让局部状态同时受长时间尺度结构约束。 复现级别：核心机制复现。复现级别：核心机制复现。论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。合成多尺度序列上比较 next-latent 与加入块级 abstract latent 的预测误差；结构也接入 micro-LLM evolve。  pretraining latent-prediction multi-token-prediction speculative-decoding 基础模型 训练预算：数据配比、目标与优化器 HiLP为什么在逐步latent预测之外，再加一个更粗时间尺度的目标？ 连续一步预测可能把小误差逐步传下去，局部相似并不保证远处结构仍正确。HiLP用粗粒度抽象latent目标约束更长尺度，同时保留next-token与局部latent训练，使表示兼顾近期细节和远程结构。层级目标提供额外约束，不等于消除了rollout误差或无需检验长程效果。 教学例子：每一步都稍微偏离路线，走很多步后会离终点很远；除了预测下一步，还预测下一个阶段的抽象状态，可以对局部轨迹施加更远的约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-hilp-e751afd4" class="ar-learning-paper-anchor"></span>
<h2 id="qa-988153cb726324b4">HiLP为什么在逐步latent预测之外，再加一个更粗时间尺度的目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ahilp">Hierarchical Latent Prediction for Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Texas at Austin</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>连续一步预测可能把小误差逐步传下去，局部相似并不保证远处结构仍正确。HiLP用粗粒度抽象latent目标约束更长尺度，同时保留next-token与局部latent训练，使表示兼顾近期细节和远程结构。层级目标提供额外约束，不等于消除了rollout误差或无需检验长程效果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>每一步都稍微偏离路线，走很多步后会离终点很远；除了预测下一步，还预测下一个阶段的抽象状态，可以对局部轨迹施加更远的约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.05806">原论文</a> · <a href="../../../../reproductions/2608.05806-hilp/">实现解读</a> · <a href="#qa-988153cb726324b4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-orchestra" data-paper-title="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data 基础模型 Fudan University / Shanghai Jiao Tong University / SII-GAIR 2026-07-27 固定 corpus-level 清洗会过度处理本来干净的文本，也会对不同噪声使用同一操作。DataOrchestra 为每个 1024-token chunk 生成计划：先选 Drop、Untouch 或 Clean；Clean 时再按 NP（Noise Pruning）→ SR（Surface Rectification）→ PA（Pedagogical Augmentation）选择阶段，并为 rewrite 生成该 chunk 专属 instruction。 Fidelity: 核心机制复现。实际训练 per-example orchestrator、执行多操作路由并以同预算重新预训练；程序化教师和小模型替代论文大规模 LLM 工具链。本地 8-feature MLP 与程序化规则替代 Qwen3-235B teacher/verifier、Qwen3-1.7B orchestrator、0.6B NP 和 4B SR/PA；四种确定性编辑替代自然语言 chunk-specific rewrite，WikiText-2 替代 20B/30B token 多语料。因此这是 orchestration 决策与下游预训练链路的核心机制复现，不是论文数据质量规模结论的复刻。  llm-pretraining data-curation data-cleaning learned-orchestration 基础模型 训练预算：数据配比、目标与优化器 DataOrchestra为何先允许Drop和Untouch，而不是给每个chunk都依次清洗三遍？ 不同样本需要不同处理，干净文本反复改写既浪费算力又可能损伤内容。orchestrator先决定丢弃、原样保留或清洗，只有Clean才组合噪声剪除、表面修正与教学增强，并生成样本专属指令；训练计划还经过真实执行与核验。目标是质量与成本的取舍，不是最大化被清洗比例。 教学例子：一段干净教科书可Untouch，网页噪声段先剪除导航，严重缺内容的段落可Drop；给三者统一套改写指令，可能花钱把原本正确的文本改坏。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-data-orchestra-f57d3169" class="ar-learning-paper-anchor"></span>
<h2 id="qa-221959926fa7c86d">DataOrchestra为何先允许Drop和Untouch，而不是给每个chunk都依次清洗三遍？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-orchestra">DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University / Shanghai Jiao Tong University / SII-GAIR</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同样本需要不同处理，干净文本反复改写既浪费算力又可能损伤内容。orchestrator先决定丢弃、原样保留或清洗，只有Clean才组合噪声剪除、表面修正与教学增强，并生成样本专属指令；训练计划还经过真实执行与核验。目标是质量与成本的取舍，不是最大化被清洗比例。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一段干净教科书可Untouch，网页噪声段先剪除导航，严重缺内容的段落可Drop；给三者统一套改写指令，可能花钱把原本正确的文本改坏。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.24717">原论文</a> · <a href="../../../../reproductions/2607.24717-data-orchestra/">实现解读</a> · <a href="#qa-221959926fa7c86d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gaugequant" data-paper-title="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries 基础模型 University of Cambridge 2026-07-22 LLM 内部通道存在保持函数不变的 gauge 对称性，但不同等价基的量化误差差异很大。GaugeQuant 在训练中在线学习量化友好正交基，以 LogSumExp 压制 activation outliers，不需要额外 calibration corpus。 未训练 LLaMA-2 7B，也没有 int4 kernel；Fidelity: 核心机制复现。真实学习正交 gauge、优化 outlier，并走 W4A4 STE 路径。未训练 LLaMA-2 7B，也没有 int4 kernel；STE fake quant 用于验证在线 gauge 学习机制，不代表实际吞吐。本地对照口径：基线是浮点 llama_modern；实验组训练 Householder 正交 gauge 并执行 W4A4 STE，LM loss 5.7471→5.7313，相对 -0.27%，PPL 313.27→308.38（-1.56%）。  llm-training quantization w4a4 基础模型 训练预算：数据配比、目标与优化器 GaugeQuant为什么能先换内部坐标基，再降低量化误差，而不必先改变原始浮点函数？ 某些内部通道变换具有函数等价的对称性：一侧乘正交基，另一侧作逆变换，浮点组合保持一致。量化却依赖坐标轴上的数值分布，因此等价基可能有不同outlier和舍入误差。方法在线学习更友好的基，利用的是函数等价与量化不等价之间的空间，不能随意在不满足对称条件的位置旋转。 教学例子：原来能量集中在一个特别大的通道，经合法旋转可分散到多个通道；逆变换保持浮点输出，而低比特码本可能更容易表示分散后的数值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-gaugequant-8dce1822" class="ar-learning-paper-anchor"></span>
<h2 id="qa-be6020bebde4aa23">GaugeQuant为什么能先换内部坐标基，再降低量化误差，而不必先改变原始浮点函数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agaugequant">GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>某些内部通道变换具有函数等价的对称性：一侧乘正交基，另一侧作逆变换，浮点组合保持一致。量化却依赖坐标轴上的数值分布，因此等价基可能有不同outlier和舍入误差。方法在线学习更友好的基，利用的是函数等价与量化不等价之间的空间，不能随意在不满足对称条件的位置旋转。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原来能量集中在一个特别大的通道，经合法旋转可分散到多个通道；逆变换保持浮点输出，而低比特码本可能更容易表示分散后的数值。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.20757">原论文</a> · <a href="../../../../reproductions/2607.20757-gaugequant/">实现解读</a> · <a href="#qa-be6020bebde4aa23">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:ppl-factory" data-paper-title="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning 基础模型 McGill University 2026-07-20 固定的“选最难/最容易”规则会随任务和数据预算失效。PPL-Factory 先用冻结基础模型计算任务相关 NLL：语言建模按 packed block，推理 SFT 只看 reasoning/answer response；再按预算切换策略，高预算偏 easy，较低预算选 middle，极低预算从 middle pool 随机抽样以保覆盖。 未运行 Qwen2.5-7B、GSM8K/MATH response-only NLL 和答案准确率。Fidelity: 核心机制复现。真实训练冻结 scorer、逐块计算 NLL，并从同一 checkpoint 对 random/easy/middle 子集做同预算微调。只复现 CLM packed-block 分支；未运行 Qwen2.5-7B、GSM8K/MATH response-only NLL 和答案准确率。负结果保留，不外推为对原论文的否定。本地对照口径：基线是 20% 随机 block；  llm-training data-selection efficient-finetuning 基础模型 训练预算：数据配比、目标与优化器 PPL-Factory为什么不总选最难样本，还要随任务和数据预算改变选择区间？ 样本难度与有用性并非固定单调关系；高预算、低预算和极小预算下，学习信号与覆盖的取舍不同。它先用冻结基础模型按任务口径打分，再分别偏向easy、middle或从middle池随机抽样。推理SFT只看response损失，不能让prompt长度主导所谓难度。 教学例子：预算只能留几十条时，机械挑最难可能全是模型尚无学习信号的样本；从中等池随机抽取可保留部分覆盖。预算足够大后，最佳策略又可能改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-ppl-factory-5bbf227d" class="ar-learning-paper-anchor"></span>
<h2 id="qa-0f2dc94cbdd47750">PPL-Factory为什么不总选最难样本，还要随任务和数据预算改变选择区间？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Appl-factory">PPL-Factory: Task-Aware and Budget-Aware Data Selection from Language Modeling to Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · McGill University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>样本难度与有用性并非固定单调关系；高预算、低预算和极小预算下，学习信号与覆盖的取舍不同。它先用冻结基础模型按任务口径打分，再分别偏向easy、middle或从middle池随机抽样。推理SFT只看response损失，不能让prompt长度主导所谓难度。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预算只能留几十条时，机械挑最难可能全是模型尚无学习信号的样本；从中等池随机抽取可保留部分覆盖。预算足够大后，最佳策略又可能改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18199">原论文</a> · <a href="../../../../reproductions/2607.18199-ppl-factory/">实现解读</a> · <a href="#qa-0f2dc94cbdd47750">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:open-language-model" data-paper-title="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research 基础模型 Indian Institute of Technology Madras 2026-07-18 许多预训练框架把模型结构、训练循环和分布式运行强耦合，难以做透明消融。OLM 让组件保持普通 PyTorch module，用 Block、Residual、Repeat、Parallel 描述布线，同一模型可从 notebook 迁移到 CPU、单 GPU 和单机多 GPU。 Fidelity：核心机制复现。公开数据只验证论文机制，不模拟生产流量。未搬运上游整个包和 27 个 preset，也未复刻 348M 四卡实验；本地验证结构语义和统一 evaluator 接口。本地对照口径：基线为同预算 LLaMA-modern，实验组为 olm_composable；相对 PPL -0.000001%。  pretraining-infrastructure composable-architecture small-language-model evolve 基础模型 训练预算：数据配比、目标与优化器 OpenLanguageModel的可组合Block/Residual/Repeat，怎样帮助判断消融到底改了什么？ 它把普通PyTorch组件与布线结构分开，让重复、残差和并行关系可直接组合，降低模型、训练循环与分布式执行的耦合。这样同一结构更容易跨notebook和不同设备运行，也更容易保持消融的其他条件一致。可读可组合是工程属性，本身不是模型能力提升的实验结论。 教学例子：比较串联两个块与两支并行相加时，可只改布线表达，沿用数据和训练循环；若同时换了整个分布式框架，就更难把结果归因于结构变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-open-language-model-02ba0f0c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-ae8ca0c028b6ef9a">OpenLanguageModel的可组合Block/Residual/Repeat，怎样帮助判断消融到底改了什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aopen-language-model">OpenLanguageModel: Readable and Composable Small-Language-Model Pretraining for Education and Research</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Indian Institute of Technology Madras</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把普通PyTorch组件与布线结构分开，让重复、残差和并行关系可直接组合，降低模型、训练循环与分布式执行的耦合。这样同一结构更容易跨notebook和不同设备运行，也更容易保持消融的其他条件一致。可读可组合是工程属性，本身不是模型能力提升的实验结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>比较串联两个块与两支并行相加时，可只改布线表达，沿用数据和训练循环；若同时换了整个分布式框架，就更难把结果归因于结构变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.16669">原论文</a> · <a href="../../../../reproductions/2607.16669-open-language-model/">实现解读</a> · <a href="#qa-ae8ca0c028b6ef9a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:gemini-for-google" data-paper-title="Customizing an LLM for Enterprise Software Engineering" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Customizing an LLM for Enterprise Software Engineering 基础模型 Google 2026-05-15 从企业开发历史中提取高价值代码与交互信号，经过去重、质量过滤和污染控制形成中训练数据；用通用数据回放抑制灾难性遗忘，再做面向内部工具的后训练和部署评测。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。只执行中训练 replay 目标与不变量；没有 Google 私有万亿 token 数据、Gemini 权重或内部开发环境，不把原文 A/B 当作本地成绩。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  企业 LLM 数据治理 中训练与后训练 基础模型 训练预算：数据配比、目标与优化器 企业代码适配为什么还混入通用数据回放，而不是只训练内部高价值样本？ 企业样本使模型熟悉内部代码、工具和交互方式，但单独优化这部分可能遗忘通用能力。通用回放给训练提供另一组约束；去重、质量和污染控制则保护数据及评测口径。混合比例表达适配与保留的权衡，不能由内部任务提升直接推出通用能力也保持不变。 教学例子：模型学会内部构建命令后仍要完成一般代码推理；若训练全被内部模式占满，通用任务可能退化，所以应同时验证企业收益与通用回放的保留效果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-gemini-for-google-0c2d88a0" class="ar-learning-paper-anchor"></span>
<h2 id="qa-88875c261b2a4f2b">企业代码适配为什么还混入通用数据回放，而不是只训练内部高价值样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Agemini-for-google">Customizing an LLM for Enterprise Software Engineering</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>企业样本使模型熟悉内部代码、工具和交互方式，但单独优化这部分可能遗忘通用能力。通用回放给训练提供另一组约束；去重、质量和污染控制则保护数据及评测口径。混合比例表达适配与保留的权衡，不能由内部任务提升直接推出通用能力也保持不变。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型学会内部构建命令后仍要完成一般代码推理；若训练全被内部模式占满，通用任务可能退化，所以应同时验证企业收益与通用回放的保留效果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2605.16517">原论文</a> · <a href="../../../../foundation-models/2605.16517-gemini-for-google/">实现解读</a> · <a href="#qa-88875c261b2a4f2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-quality-lsa" data-paper-title="Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models 基础模型 University of Southern California / Google Research 2026-03-01 以 in-context 线性回归的权重预测分析预训练与后训练数据协方差。SFT 使用教师中间状态，OS 仅监督最终预测；原文明确 OS 是 outcome-supervised regression，不是包含采样、优势估计和 policy gradient 的完整 RL。§3、§4 给出线性注意力结构及闭式解。 GPT2 多网格、多重复长训练成本过高，不复现（审查 DONE） runner 使用 d=4、6个生成 prompt 的数学诊断，fixture_only: true，没有 benchmark train/test 能力结论。population_initialization、context_embedding、lsa_forward、rollout、sft_loss、outcome_supervision_loss 与 closest_sft_value 可组合执行。自主 rollout 没有真实权重参数，只读取公开任务上下文；训练目标只进入明确命名的训练 loss。  预训练与数据 SFT与outcome supervision理论 基础模型 训练预算：数据配比、目标与优化器 这篇数据质量理论里的OS，为什么不能直接称为完整的强化学习后训练？ OS在此指outcome-supervised regression：只监督最终预测，并与使用教师中间状态的SFT对比。线性attention模型与协方差假设让作者能分析闭式关系，但没有完整策略采样、优势估计和policy gradient链路。该理论可帮助理解信息与目标差别，不能被扩成真实LLM RL已得到同样结论。 教学例子：学生只在最后一步的回归权重上计算平方误差，与每一步都对齐教师状态不同；即便前者叫结果监督，也并没有因此出现奖励驱动的策略梯度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-data-quality-lsa-d7c7a545" class="ar-learning-paper-anchor"></span>
<h2 id="qa-7a5caefc122995f3">这篇数据质量理论里的OS，为什么不能直接称为完整的强化学习后训练？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-quality-lsa">Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>OS在此指outcome-supervised regression：只监督最终预测，并与使用教师中间状态的SFT对比。线性attention模型与协方差假设让作者能分析闭式关系，但没有完整策略采样、优势估计和policy gradient链路。该理论可帮助理解信息与目标差别，不能被扩成真实LLM RL已得到同样结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>学生只在最后一步的回归权重上计算平方误差，与每一步都对齐教师状态不同；即便前者叫结果监督，也并没有因此出现奖励驱动的策略梯度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2603.01293">原论文</a> · <a href="../../../../foundation-models/2603.01293-data-quality-lsa/">实现解读</a> · <a href="#qa-7a5caefc122995f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:modular-robust-generative" data-paper-title="A Theoretical Framework for Modular Learning of Robust Generative Models" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="A Theoretical Framework for Modular Learning of Robust Generative Models 基础模型 Google Research 2026-02-19 以冻结生成专家为基础，优化面对最差数据域的输入相关 gate。核心不是专家均值：逐输入 softmax 不保证整个生成分布积分为一，必须额外约束全局质量。另将非因果教师采样轨迹蒸馏到只读前缀的因果 router。§5.2、§6、§7.3 给出实施过程。 原尺度多专家、多对照、多数据/seed完整 campaign 成本过高，不复现（审查 DONE） runner 为两专家×四结果的生成式数学诊断，显式 fixture_only: true。gated_mass 明确返回未归一化质量；primal_dual_step 执行三方更新；sir_resample 进行实际重要性重采样；cached_router_nll 对冻结缓存训练 router。独立测试覆盖全局约束反例、EG/dual 公式、采样复现、混合概率及梯度隔离。该 API 不自动验证调用方网络的因果性，调用者必须只用前缀产生 router logits。  网络架构 鲁棒模块化生成 基础模型 训练预算：数据配比、目标与优化器 生成专家的gate在每个输入上都softmax，为何组合分布仍可能没有归一化？ 若gate随被评价的完整样本变化，它不能像固定混合系数那样移出全局求和；逐输入权重和为1并不保证混合密度对全部样本求和为1。方法因此额外约束总质量，并区分最差域的KL与NLL口径。忽略全局约束，或事后悄悄归一化，都改变了原优化问题。 教学例子：只有A、B两个样本，gate在A处偏向最擅长A的专家，在B处又偏向最擅长B的专家；两处都取到高密度后，总和可能大于1，尽管每处gate都和为1。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-modular-robust-generative-72932b77" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8f5d8c105b8e3a12">生成专家的gate在每个输入上都softmax，为何组合分布仍可能没有归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amodular-robust-generative">A Theoretical Framework for Modular Learning of Robust Generative Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若gate随被评价的完整样本变化，它不能像固定混合系数那样移出全局求和；逐输入权重和为1并不保证混合密度对全部样本求和为1。方法因此额外约束总质量，并区分最差域的KL与NLL口径。忽略全局约束，或事后悄悄归一化，都改变了原优化问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只有A、B两个样本，gate在A处偏向最擅长A的专家，在B处又偏向最擅长B的专家；两处都取到高密度后，总和可能大于1，尽管每处gate都和为1。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.17554">原论文</a> · <a href="../../../../foundation-models/2602.17554-modular-robust-generative/">实现解读</a> · <a href="#qa-8f5d8c105b8e3a12">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:eco-optimizer" data-paper-title="ECO: Quantized Training without Full-Precision Master Weights" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="ECO: Quantized Training without Full-Precision Master Weights 基础模型 Google Research / ISTA 2026-01-29 低精度训练通常仍保留高精度 master weights 累积微小更新。ECO 直接在量化权重上更新，将本次重量化误差注入已有动量，避免再保存主权重或持久误差缓冲；Adam 必须使用逐元素有效步长，不能把 SGDM 的标量系数照搬过去。图按原文 Algorithm 1–3 重绘。原文算法及 Figure 1。 成本过高，不复现（审查 DONE）。完整实验成本过高，不复现（审查 DONE），依据论文配置判断，未运行成本探针。历史高优先补漏资料；成本过高，不复现（审查 DONE）。没有本地能力结果或可执行 Evolve 算子。§4.2 按参数量训练个 C4 token，最低 30M 配置也为 3B token；另有 Gemma-3 1B、2.1B MoE 预训练及 DeepSeek-MoE-16B 微调。完整实验成本过高，不复现（审查 DONE），依据论文配置判断，未运行成本探针。  预训练与数据 优化器与训练稳定性 基础模型 训练预算：数据配比、目标与优化器 ECO去掉高精度master weights后，微小更新被量化吃掉的问题怎样处理？ 它直接更新量化权重，并把本次重量化误差反馈到已有动量，避免额外保存主权重或独立误差缓冲。补偿系数与优化器步长相关；Adam的有效步长逐元素变化，不能照搬SGDM标量系数。无额外缓冲规则还有推导近似，不能说每一步都与高精度轨迹精确等价。 教学例子：一次更新小于量化网格，权重暂时没变；误差信息进入动量，影响后续更新，而不是凭空丢掉或另外保存一整份高精度权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-eco-optimizer-dd39c986" class="ar-learning-paper-anchor"></span>
<h2 id="qa-60e5874d502e6a0b">ECO去掉高精度master weights后，微小更新被量化吃掉的问题怎样处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Aeco-optimizer">ECO: Quantized Training without Full-Precision Master Weights</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / ISTA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它直接更新量化权重，并把本次重量化误差反馈到已有动量，避免额外保存主权重或独立误差缓冲。补偿系数与优化器步长相关；Adam的有效步长逐元素变化，不能照搬SGDM标量系数。无额外缓冲规则还有推导近似，不能说每一步都与高精度轨迹精确等价。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一次更新小于量化网格，权重暂时没变；误差信息进入动量，影响后续更新，而不是凭空丢掉或另外保存一整份高精度权重。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.22101v1">原论文</a> · <a href="../../../../foundation-models/2601.22101-eco-optimizer/">实现解读</a> · <a href="#qa-60e5874d502e6a0b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:me-pois" data-paper-title="Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement 基础模型 University of Southern California 2026-01-29 原方法用访问序列编码器连接短期轨迹与长期地点原型，并把高频地点的时段分布跨空间尺度传给稀疏地点；文本语义作为另一条对齐监督。冻结预训练表征后，再训练地图属性探针。主要机制与公式见原文 §3.2–3.6。 阻碍是付费/私有移动数据、SafeGraph 与 Maps 标签及完整多 embedding 组合，因此完整实验不复现，不进入自动重试队列。当前仅为 L0/L1 公式与梯度诊断，无 validation/test 能力结论。实现 transferred_visit_distribution、prototype_contrastive_loss、distribution_kl_sum 和 MobilityPrototypeLoss。接口要求调用方提供真实访问编码及文本特征；没有用随机向量冒充轨迹编码器。  预训练与数据 地理位置表征 基础模型 训练预算：数据配比、目标与优化器 ME-POIs怎样给访问稀少的地点补充时段信息，为什么不能把所有尺度锚点一锅归一化？ 它借助高频地点的时段分布，在每个空间尺度内部先按距离对锚点归一化，再在尺度间平均，避免某个尺度只因锚点多就主导结果。轨迹编码连接短期访问与长期地点原型，文本另作语义对齐。行为时段、地点语义与冻结后的属性探针各有角色，不能混作一个标签。 教学例子：小尺度有2个近邻锚点，大尺度有20个；先各自归一化再平均，可让尺度贡献按设计组合，而不是让大尺度仅凭数量多就压过近邻信息。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-me-pois-4510ed6c" class="ar-learning-paper-anchor"></span>
<h2 id="qa-f585319aed43d6d3">ME-POIs怎样给访问稀少的地点补充时段信息，为什么不能把所有尺度锚点一锅归一化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Ame-pois">Mobility-Embedded POIs: Learning What A Place Is and How It Is Used from Human Movement</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它借助高频地点的时段分布，在每个空间尺度内部先按距离对锚点归一化，再在尺度间平均，避免某个尺度只因锚点多就主导结果。轨迹编码连接短期访问与长期地点原型，文本另作语义对齐。行为时段、地点语义与冻结后的属性探针各有角色，不能混作一个标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>小尺度有2个近邻锚点，大尺度有20个；先各自归一化再平均，可让尺度贡献按设计组合，而不是让大尺度仅凭数量多就压过近邻信息。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.21149">原论文</a> · <a href="../../../../foundation-models/2601.21149-me-pois/">实现解读</a> · <a href="#qa-f585319aed43d6d3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:muon" data-paper-title="Muon is Scalable for LLM Training" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Muon is Scalable for LLM Training 基础模型 Moonshot AI / UCLA 2025-02-24 AdamW 把矩阵参数当作独立标量更新，Muon 则把隐藏层梯度视为矩阵，通过 momentum 与 Newton–Schulz 近似极分解得到正交化更新方向。论文为大规模训练补上 weight decay 和按参数形状缩放；非隐藏矩阵参数继续使用 AdamW。 Fidelity: 核心机制复现。隐藏层二维矩阵使用 Muon，embedding、norm、bias 与输出参数保留 AdamW。未复刻分布式 optimizer state、通信优化、3B/16B MoE 和 5.7T-token compute frontier；本地结论只说明算法路径正确运行，不支持 2× 效率在小模型复现。本地对照口径：基线和实验组结构、参数量、数据与 30-step 预算完全相同，只把 AdamW 换为 Muon；WikiText-2 LM loss 5.7471→5.8016，相对 +0.95%（更差），PPL 相对 +5.61%。  llm-training optimizer training-efficiency 基础模型 训练预算：数据配比、目标与优化器 Muon为什么把梯度当矩阵处理，而不是像AdamW那样逐坐标调步长？ 它对带动量的隐藏矩阵梯度做近似极分解，调整更新的谱几何，再配合权重衰减与形状缩放。处理对象是矩阵整体的方向关系，不只是每个标量自己的二阶矩。论文大规模方案对非隐藏矩阵参数仍使用AdamW，因此不能把整个训练器简单写成所有张量都调用同一个正交化函数。 教学例子：两列梯度几乎共线，逐坐标缩放与矩阵极分解会给出不同更新方向；词表或一维参数是否适合该规则，也需要按论文参数分工处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-muon-e884dc79" class="ar-learning-paper-anchor"></span>
<h2 id="qa-93b41ee941026af3">Muon为什么把梯度当矩阵处理，而不是像AdamW那样逐坐标调步长？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Amuon">Muon is Scalable for LLM Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Moonshot AI / UCLA</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它对带动量的隐藏矩阵梯度做近似极分解，调整更新的谱几何，再配合权重衰减与形状缩放。处理对象是矩阵整体的方向关系，不只是每个标量自己的二阶矩。论文大规模方案对非隐藏矩阵参数仍使用AdamW，因此不能把整个训练器简单写成所有张量都调用同一个正交化函数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两列梯度几乎共线，逐坐标缩放与矩阵极分解会给出不同更新方向；词表或一维参数是否适合该规则，也需要按论文参数分工处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2502.16982">原论文</a> · <a href="../../../../reproductions/2502.16982-muon/">实现解读</a> · <a href="#qa-93b41ee941026af3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:data-mixing-laws" data-paper-title="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance 基础模型 University of Cambridge / Shanghai AI Laboratory 2024-03-25 先训练多组小预算 domain mixture，拟合各评测域的混合缩放律，再搜索未训练过的最优配比。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际用公开文本域的十组 pilot mixture 拟合逐域指数 mixing law，并在未训练配比网格上选择最优配比；小型 unigram proxy 不等同于 RedPajama 多模型 scaling curve。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为均匀数据混合，实验组为 data-mixing-laws；相对 validation loss -3.48%。  pretraining-data scaling-law data-mixture 基础模型 训练预算：数据配比、目标与优化器 Data Mixing Laws怎样搜索没真正训练过的数据配比，依据又有什么限制？ 先用多组小预算混合训练观察各评测域损失，再拟合配比、规模与性能关系，最后在拟合模型上搜索目标加权最优配比。省掉的是穷举每个大预算配方的成本，预测可靠性仍取决于试验覆盖和拟合假设；验证选择不能使用最终测试结果反复调配。 教学例子：已经测过代码占比20%、50%、80%的小模型，可预测中间配比的表现，再选择少量候选验证；不能把曲线预测值直接当成该大模型配方的实测成绩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-data-mixing-laws-e8c71fa2" class="ar-learning-paper-anchor"></span>
<h2 id="qa-8a72a4e046d49e6c">Data Mixing Laws怎样搜索没真正训练过的数据配比，依据又有什么限制？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adata-mixing-laws">Data Mixing Laws: Optimizing Data Mixtures by Predicting Language Modeling Performance</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Cambridge / Shanghai AI Laboratory</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>先用多组小预算混合训练观察各评测域损失，再拟合配比、规模与性能关系，最后在拟合模型上搜索目标加权最优配比。省掉的是穷举每个大预算配方的成本，预测可靠性仍取决于试验覆盖和拟合假设；验证选择不能使用最终测试结果反复调配。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>已经测过代码占比20%、50%、80%的小模型，可预测中间配比的表现，再选择少量候选验证；不能把曲线预测值直接当成该大模型配方的实测成绩。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2403.16952">原论文</a> · <a href="../../../../reproductions/2403.16952-data-mixing-laws/">实现解读</a> · <a href="#qa-8a72a4e046d49e6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="foundation-models:doremi" data-paper-title="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining" data-learning-pending="false" data-domain="foundation-models" data-theme="foundation-models" data-topic="foundation-models/training-budget" data-search="DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining 基础模型 Stanford University / Google Research 2023-05-17 用小型 proxy model 的 excess loss 做 group DRO，动态提升欠拟合域权重，再按所得配比训练目标模型。 保真度：核心机制复现。保真度：核心机制复现。原文结论、本地公开数据实验和未复刻部分分开陈述。实际在两个公开文本域上训练 reference unigram proxy，执行 group-DRO excess-loss 指数权重更新，再以所学配比评估；未复刻 The Pile、280M proxy 与 8B target。本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。本地对照口径：基线为均匀数据混合，实验组为 doremi；相对 validation loss -0.15%。  pretraining-data data-mixture group-dro 基础模型 训练预算：数据配比、目标与优化器 DoReMi为什么提高excess loss较大的域，而不是直接追最高原始loss的域？ 原始loss同时反映任务固有难度和当前欠拟合；减去参考模型的域损失后，excess loss更关注相对参考仍未学好的部分。小proxy通过group DRO学习域配比，再把配比交给目标模型训练。得到的是特定数据和参考下的资源分配，不能把高熵域天然难预测误当成它总该拿最多预算。 教学例子：A域原始loss为5、参考为4.9，B域为3、参考为2；前者虽绝对更难，B相对参考的缺口却更大，权重更新会区分这两种情况。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">基础模型 / 训练预算：数据配比、目标与优化器</a></p>
<span id="paper-foundation-models-doremi-7bfdfa8e" class="ar-learning-paper-anchor"></span>
<h2 id="qa-82c48593bd66c5dc">DoReMi为什么提高excess loss较大的域，而不是直接追最高原始loss的域？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=foundation-models%3Adoremi">DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University / Google Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始loss同时反映任务固有难度和当前欠拟合；减去参考模型的域损失后，excess loss更关注相对参考仍未学好的部分。小proxy通过group DRO学习域配比，再把配比交给目标模型训练。得到的是特定数据和参考下的资源分配，不能把高熵域天然难预测误当成它总该拿最多预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>A域原始loss为5、参考为4.9，B域为3、参考为2；前者虽绝对更难，B相对参考的缺口却更大，权重更新会区分这两种情况。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2305.10429">原论文</a> · <a href="../../../../reproductions/2305.10429-doremi/">实现解读</a> · <a href="#qa-82c48593bd66c5dc">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

有限训练预算应该先改数据、更新方向，还是模型规模？

## 记住这一点

DoReMi 用小代理模型相对参考模型的域级 excess loss 做 Group DRO，学习数据混合比例，再把配比用于目标模型训练。Muon 对隐藏矩阵的动量作近似正交化，并配合衰减和形状缩放；其余参数不能随意照搬同一种更新。两者分别改变“训练看什么”和“梯度怎样走”，应分轴检验。

## 一个例子

代码、网页、百科各占三分之一只是一个起点。DoReMi 的权重取决于相对参考模型的学习困难，不能简单把最高原始 loss 的域全加满。更换 Muon 后还要比较等 token、等时间或等 FLOPs 的曲线，不能只取相同步数的某一个点宣布节省预算。

## 什么时候要小心

小代理得到的配比不保证任意规模都最优，优化器收益也依赖学习率与预算。低精度状态、压缩激活和数据筛选可能影响不同资源。文档中的机制诊断、短预算负结果及高成本未复现都应保留原边界。

## 先读这几篇

先读 DoReMi，明确域权重为什么由 excess loss 而非原始 loss 决定；再读 Muon 的矩阵更新，理解优化方向与非矩阵参数边界。之后看数据选择、低精度状态和训练系统。

1. [DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining](../../../reproductions/2305.10429-doremi/README.md) · [原论文](https://arxiv.org/abs/2305.10429)
2. [Muon is Scalable for LLM Training](../../../reproductions/2502.16982-muon/README.md) · [原论文](https://arxiv.org/abs/2502.16982)

## 自测一下

优化器 A 每步 loss 降得快、但一步耗时是 B 的两倍，能直接说 A 更省算力吗？

??? note "展开参考答案"

    不能。先确定目标是达到同质量所需时间、FLOPs 还是 token 数，再比较对应成本曲线；训练数据和调参预算也要匹配。单步下降和端到端效率不是同一指标。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
