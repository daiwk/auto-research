---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 生成一个物品，先后跨过码本、模型分布与合法目录三道关

[搜广推](../index.md) · 更新 2026-11-15 · 67 篇主题资料 / 12 篇重点对照

TIGER把物品变成层次码并学习下一码序列，COBRA在稀疏码后补回条件稠密向量，PLUM把已有LLM通过继续预训练接到行为/SID空间。STATIC不改表示而改变合法解码的执行方式，Reward Guided Decoding则在既有支持上倾斜业务偏好。先定位改变的是哪一关，再判断它能否找回漏掉的物品。 PinGER再把历史输入与SID监督拆开，并将前缀多样化选择、分层DPO和合法目录分别治理。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/recommendation/generative-retrieval-reasoning.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：物品表示：离散码、稀疏—稠密级联与LLM继续预训练 · 学习分布与推理搜索分别改变什么 · 合法目录约束与业务reward的区别 · 先验支持、beam预算和本地缩比证据

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [Recommender Systems with Generative Retrieval](../../../reproductions/2305.05065-tiger/README.md) · [原始来源](https://arxiv.org/abs/2305.05065)<br>章节：背景与主要改动、核心公式、本地复现 | RQ-VAE逐层量化内容残差，加碰撞消解token形成物品SID，encoder-decoder自回归预测下一物品码序列。 | 共享语义前缀便于参数共享，但码本碰撞和早期路径错误会影响可达性。本地按有效物品ID累加token log-prob评分，不能将其等同生产beam吞吐。 |
| [Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations](../../../reproductions/2503.02453-cobra/README.md) · [原始来源](https://arxiv.org/abs/2503.02453)<br>章节：背景与主要改动、核心公式、本地复现 | 先生成稀疏code，再以该code和历史为条件生成dense query，beam code分数与dense相似度级联召回。 | 为量化丢失的细节增加区分通道，也引入稠密索引、融合权重和两阶段预算；若目标code根本未进入beam，后段dense通常无从补回。 |
| [PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations](../../../reproductions/2510.07784-plum/README.md) · [原始来源](https://arxiv.org/abs/2510.07784)<br>章节：背景与主要改动、核心公式、本地结果 | 从已有MoE LLM初始化，以行为和视频元数据CPT对齐，再做next-SID召回；SID-v2同时约束重建、量化和共现。 | 容量从大型ID表转向可扩展主干，但依赖CPT配方和预训练资源。线上生成SID不用点积索引，不代表没有SID映射、目录维护与解码成本。 |
| [Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md) · [原始来源](https://arxiv.org/abs/2602.22647)<br>章节：背景与主要改动、核心公式、结果与边界 | 将合法token路径编成加速器内CSR迁移，先全词表log-softmax，再非法项置负无穷，并同步维护beam前缀和node状态。 | 改变约束执行的成本与合法性，不会创造模型未学到的偏好；不能在每个合法子集重新归一化后还声称保持同一条原模型路径分数。 |
| [Reward Guided Decoding for Generative Recommendation](../../../reproductions/2607.25344-reward-guided-decoding/README.md) · [原始来源](https://arxiv.org/abs/2607.25344)<br>章节：背景与主要改动、核心公式、复现边界 | 固定生成先验P0，用exp(R/β)倾斜得到Q，以KL温度限制偏离，不重新训练生成器。 | reward可重排既有支持，却不能令P0为零的路径凭空出现；代理reward和线上价值不同，本地MovieLens构造任务不等于生产收益。 |
| [PailitaoMMSearch2.0 Technical Report: Scaling Generative Retrieval to Unified End-to-End Multimodal Search](../../../recommendation-components/2610.36958-pailitao-mmsearch2/README.md) · [原始来源](https://arxiv.org/abs/2610.36958v1)<br>章节：背景与主要改动、核心公式 | 统一图文到SID集合，多意图/预算训练与Sample–Beam服务对齐。 | 完整多模型多阶段和私有生产实验高成本不复现；无本地占位模型。 |
| [PinGER: Token-Efficient Generative Retrieval with Semantic IDs](../../../recommendation-components/2610.33435-pinger/README.md) · [原始来源](https://arxiv.org/abs/2610.33435v1)<br>章节：背景与主要改动、核心公式、高成本完整实验 | 训练交错SID/dense并关闭跨商品SID读取，服务删除过去SID；按LCP深度逐beam惩罚，所有SID前缀DPO与NTP锚联合后训练。 | 不同于TIGER逐项历史SID输入，也不能把前缀多样性当STATIC合法性；多样性会牺牲离线recall，本地无完整tokenizer/服务。 |
| [ReuseGR: Offline–Online Decoupled Generative Retrieval via Adaptive Prefix Reuse](../../../recommendation-components/2611.04259-reusegr/README.md) · [原始来源](https://arxiv.org/abs/2611.04259v1)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 按query共享7B规划的SID前缀，0.5B读取当前用户历史补全；ReuseCut以逐级覆盖准则选择复用深度。 | 比缓存完整结果保留更多个性化空间，但深缓存会限制可达目标；准备好depth0与冷miss使用不同模型，低成本标签核不等于学习BudgetCut。 |
| [SPADE: Spatiotemporal Preference Alignment and Diversity Enhancement for Local Search](../../../recommendation-components/2611.04662-spade-local-search/README.md) · [原始来源](https://arxiv.org/abs/2611.04662v1)<br>章节：背景与主要改动、核心公式、结果、负控与边界 | 用业务价值重加权BPE合并，再以父beam名次的有界sigmoid奖励控制自由文本query生成的裁剪。 | 与固定SID子树的约束和LCP惩罚不同；名次奖励不测两候选语义距离，也不无条件保留最终top1。本地不含STAR/MARS-DPO或完整query模型。 |
| [ReSID: Rethinking Long-Tail Retrieval in Generative Recommendation through item Reachability](../../../recommendation-components/2611.16404-resid/README.md) · [原始来源](https://arxiv.org/abs/2611.16404v1)<br>章节：背景与主要改动、核心公式、结果、负控与边界、高成本完整实验 | 独立子空间parallel SID，加训练prior校准与prefix语义势能guided beam，再按Hamming mismatch和beam score恢复候选。 | TIGER逐层量化residual并要求有效SID检索；ReSID同时改变token结构与候选可达性，不能仅用tail bonus解释。局部冻结输入核不训练量化器或生成器。 |
| [TriGen: A Generative Paradigm for Trigger-Induced Recommendation](../../../recommendation-components/2611.16395-trigen/README.md) · [原始来源](https://arxiv.org/abs/2611.16395v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界 | 固定窗口tail注入trigger，pristine history上的trigger/default双路径经pooled router和独立level PFFN持续调制生成。 | TIGER定义内容量化和自回归ID检索；TriGen处理即时trigger与历史偏好的条件冲突。局部可微条件不含完整encoder/decoder，随机梯度不能当Recall。 |
| [KuaiRecV2: Benchmarking Large-Scale Continual Learning for Diversified and Multi-task Recommendation](../../../recommendation-components/2611.16795-kuairec-v2-protocol/README.md) · [原始来源](https://arxiv.org/abs/2611.16795v1)<br>章节：背景与主要改动、核心公式、数据协议与代码映射、结果、负控与边界 | 以逐用户/日validation、实例加权FullMonth和一次召回多行为评测定义持续学习协议；本地仅有限split/HR/NDCG接口。 | TIGER是生成检索模型，KuaiRecV2是可评不同模型的动态item-pool benchmark。官方链接API404，L0接口不代表已下载官方数据或完成能力排名。 |

</div>

## 取舍分析 {#analysis}

### 先看物品能否到达，再看排名是否正确

TIGER和PLUM先决定物品怎样映射到SID以及每步码的概率；COBRA再在已提名的稀疏区域内补细节。若码碰撞没有消解、前缀被错误排除或合法目录缺失，单纯扩大reward权重无法恢复目标。应把token预测、有效物品覆盖和最终排序分别测量，beam变宽也不能证明码本更好。

对照来源：[tiger](../../../reproductions/2305.05065-tiger/README.md) · [plum](../../../reproductions/2510.07784-plum/README.md) · [cobra](../../../reproductions/2503.02453-cobra/README.md) · [reward-guided-decoding](../../../reproductions/2607.25344-reward-guided-decoding/README.md)

### 合法性与偏好不是同一个分数

STATIC回答某前缀下哪些token能通向合法目录，Reward Guided Decoding回答在允许的分布中怎样偏向reward。前者的非法负无穷是可行域，后者的指数倾斜是软偏好；把库存违规只当有限惩罚，仍可能选出高reward的非法项。约束编译、原模型概率和业务价值应保留各自语义。

对照来源：[static-constraint-decoding](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md) · [reward-guided-decoding](../../../reproductions/2607.25344-reward-guided-decoding/README.md)

### 10月29日：新方法与来源变化

PailitaoMMSearch2.0将多意图图文请求直接解码为商品SID候选集合，以数据工具、CPT、混合预算SFT和意图均衡RL扩展服务。Sample–Beam使推理采样与候选束生成分别对应训练/展示需要；大模型或更长思考不保证所有意图更好。与其他生成式召回对比时应固定候选集合、预算和生产混排口径，而不是只比模型名字。完整方案本地不复现。

对照来源：[tiger](../../../reproductions/2305.05065-tiger/README.md) · [pailitao-mmsearch2](../../../recommendation-components/2610.36958-pailitao-mmsearch2/README.md)

### 历史输入、候选覆盖与合法路径分别付费

TIGER把历史商品表示成多级SID序列；PinGER保留SID逐级监督，却限制主干内的读取角色，让后续商品只读历史dense。这里dense仍可包含SID fusion，不能误写成没有离散信息。PinGER的LCP惩罚只改变同层beam如何分散名额，不负责排除不存在的SID；STATIC才显式编译合法迁移。更广前缀也非免费收益：原文λ=3时distinct@1上升而R@100下降。原文整栈线上增益不能被归到本地mask或DPO单核。

对照来源：[pinger](../../../recommendation-components/2610.33435-pinger/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md) · [static-constraint-decoding](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md)

### 共享哪部分计算、输出什么对象，与怎样拉开候选并非同一问题

TIGER用语义码把物品变成可生成路径，ReuseGR沿用SID分层却将query前缀规划跨用户共享，当前历史仍影响后缀。SPADE生成的是可执行自由文本query，OA-BPE先改变切词先验，再用父beam名次奖励调节搜索存活；它不执行PinGER的共同SID前缀惩罚。比较时先固定候选预算和输出对象，再分别记录历史输入成本、离线规划成本与在线解码成本，不能把前缀可达覆盖当作完整召回提升。

对照来源：[reusegr](../../../recommendation-components/2611.04259-reusegr/README.md) · [spade-local-search](../../../recommendation-components/2611.04662-spade-local-search/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md) · [pinger](../../../recommendation-components/2610.33435-pinger/README.md)

### 语义ID能表达物品，不等于物品能穿过窄beam

TIGER把内容编码为逐层residual SID；ReSID指出早期量化和解码剪枝可让长尾目标根本到不了最终排名。独立子空间抑制残差误差传播，log-prior校准与log-mean-exp势能在prefix阶段引导，partial matching再容忍局部错码。三者改变不同环节，不能把真实gold相似度喂给搜索来制造长尾提升；本地全枚举分数相等也不证明线上10.3ms或收入提升。

对照来源：[resid](../../../recommendation-components/2611.16404-resid/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

### 条件来自哪份历史，比给生成器多一个向量更重要

TIGER按历史条件生成Semantic ID，TriGen还处理最近点击引起的意图重定向。tail-injected encoder序列可以耦合trigger与历史，而双路径必须读pristine history来保留默认偏好；router先pool路径再输出每level权重，PFFN独立参数并不允许读取未来SID。完整生成训练、mask隔离与GPU算子证据分层记录，不能用六市场线上提升替随机层背书。

对照来源：[trigen](../../../recommendation-components/2611.16395-trigen/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

### 模型名称不统一评测时间轴，月均分也不能抹掉每日退化

TIGER原文静态数据下的生成检索与KuaiRecV2的动态候选池回答不同问题。持续学习协议每天保留每用户最后一条作validation，FullMonth按实例加权，并保留每日轨迹观察适应/遗忘；同请求多任务子集必须复用单次召回。评价器gold不得回流producer。当前L0接口不实现候选池、history、官方数据或模型，不能据有限HR与TIGER真实本地NDCG比较。

对照来源：[kuairec-v2-protocol](../../../recommendation-components/2611.16795-kuairec-v2-protocol/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### COBRA多了dense向量后，为什么仍不能保证找回TIGER式早期码路径里漏掉的物品？ {#cross-dense-cannot-recover-pruned-code}

??? note "展开答案与例子"

    **答案：** COBRA的dense query以稀疏code为条件，通常在beam已提名的区域内细排；目标code若未进入搜索，后段并不自动遍历全部遗漏区域。它补的是量化后同区域的细粒度区分，不能把级联后段当成无条件召回修复器。

    **教学例子：** 示意：第一层beam只保留跑鞋类，摄影类整支被剪掉；即使跑鞋类的dense排序完美，也不会突然召回相机。

    对照来源：[cobra](../../../reproductions/2503.02453-cobra/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

### STATIC的合法路径掩码和Reward Guided Decoding的高reward，冲突时应该怎样理解？ {#cross-legal-mask-and-reward-tilt}

??? note "展开答案与例子"

    **答案：** 合法掩码先定义哪些结果允许出现，reward只在可行结果间表达偏好。指数倾斜仍乘原先验，先验或掩码给零支持的结果不能因reward高而复活。若把约束改成有限扣分，就变成了另一个允许违规被补偿的优化问题。

    **教学例子：** 示意：库存为零的商品本来预测收益很高，仍应被合法目录排除；不能靠把它的收益减一点就假定永远不会被选中。

    对照来源：[static-constraint-decoding](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md) · [reward-guided-decoding](../../../reproductions/2607.25344-reward-guided-decoding/README.md)

### TIGER和PLUM都预测SID，为什么不能只比较同一个next-token loss就判断训练路线相同？ {#cross-same-sid-not-same-training}

??? note "展开答案与例子"

    **答案：** TIGER从内容量化与序列生成建立链路；PLUM还继承LLM并通过行为、文本/ASR等混合CPT对齐语言与协同空间，SID-v2本身也加入共现和渐进深度重建。相同目标接口不代表初始化、数据与表示训练相同，比较效果需固定评估目录和预算。

    **教学例子：** 示意：两模型都预测三层码，一个只学行为序列，另一个先看元数据与行为混合语料；最后一层交叉熵的名称相同，并没有抹去前面的训练差异。

    对照来源：[tiger](../../../reproductions/2305.05065-tiger/README.md) · [plum](../../../reproductions/2510.07784-plum/README.md)

### 为何不能把Pailitao的完整线上增益当作Sample–Beam一个模块的因果收益？ {#cross-oct29-method-boundary}

??? note "展开答案与例子"

    **答案：** 线上测的是完整部署配置，含训练数据、模型和最终呈现/混排。模块作用由匹配控制的离线消融提供不同证据，二者不可直接等同；本地仅资料收录，也没有可执行接口。

    **教学例子：** 教学例：换了训练数据、模型和候选混排后交易增加，不能仅因同时用了新beam配方就把全部提升归给beam。

    对照来源：[tiger](../../../reproductions/2305.05065-tiger/README.md) · [pailitao-mmsearch2](../../../recommendation-components/2610.36958-pailitao-mmsearch2/README.md)

### PinGER的前缀多样化能代替STATIC合法目录掩码，或保证TIGER式离线召回同时提高吗？ {#cross-pinger-prefix-spread-versus-static-legality}

??? note "展开答案与例子"

    **答案：** 不能。LCP惩罚在候选父前缀间分散名额，是软选择偏好；STATIC定义哪些路径通向合法物品，是可行域。分散到更多子树还可能牺牲单一held-out物品的recall，PinGER原表也显示这种取舍。输入删SID、更多多样性和合法输出不可混成一项。

    **教学例子：** 教学示意：三个语义类别都得到beam名额，仍可能含目录不存在的叶子；过滤非法叶子也不自动保证目标物品被保留下来。

    对照来源：[pinger](../../../recommendation-components/2610.33435-pinger/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md) · [static-constraint-decoding](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md)

### ReuseGR、PinGER和SPADE都谈prefix或多样性，能把三者的控制量合成一个分数吗？ {#cross-reuse-prior-rank-and-semantic-distance}

??? note "展开答案与例子"

    **答案：** 不能不加区分地合并。ReuseGR控制共享到哪一层及可达子树，PinGER用共同SID前缀惩罚重复子树，SPADE按父beam名次加奖励且输出自由query。它们作用于不同对象和阶段，应先对齐服务预算，再分别测可达性、去冗余和最终质量。

    **教学例子：** 教学例：缓存两层prefix节省计算，并不自动让候选更分散；给排名靠后的自由query加奖励，也没有计算它与已选query的语义距离。

    对照来源：[reusegr](../../../recommendation-components/2611.04259-reusegr/README.md) · [spade-local-search](../../../recommendation-components/2611.04662-spade-local-search/README.md) · [pinger](../../../recommendation-components/2610.33435-pinger/README.md)

### TIGER生成的精确SID概率低，就能在最终重排里用ReSID补回来吗？ {#cross-cross-nov15-resid-reachability}

??? note "展开答案与例子"

    **答案：** 只有候选或足够近的SID已经存活时重排才有机会；被beam早剪掉的分支需在解码阶段处理。ReSID还改变独立量化与partial matching，不能退化成只对最终列表加分。

    **教学例子：** 教学例：第一层只留下prefix0而目标在prefix1下，最终排序看不到该目标。

    对照来源：[resid](../../../recommendation-components/2611.16404-resid/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

### 把trigger拼到TIGER历史后，让两个TriGen条件分支都读这份序列可以吗？ {#cross-cross-nov15-trigen-pristine}

??? note "展开答案与例子"

    **答案：** 不符合固定v1定义。注入序列用于encoder；双路径另读pristine history，使default-query路径不随trigger改变。丢掉这份原始历史会破坏分离意图与长期偏好的结构。

    **教学例子：** 教学例：只改变trigger时default path应保持数值不变，而非也被重复trigger带走。

    对照来源：[trigen](../../../recommendation-components/2611.16395-trigen/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

### KuaiRecV2有限例子的HR=1，可以与TIGER的MovieLens NDCG比较吗？ {#cross-cross-nov15-kuairec-evidence-level}

??? note "展开答案与例子"

    **答案：** 不可以。前者是无模型、无官方数据的L0协议例子，后者是特定数据与实际训练的指标；任务、数据、候选池、时间轴和证据层级不同。应接入真实模型/官方数据并同协议同预算对照后再谈能力。

    **教学例子：** 教学例：两条手写request的rank discount算对，不等于在30天约4.84亿交互上检索。

    对照来源：[kuairec-v2-protocol](../../../recommendation-components/2611.16795-kuairec-v2-protocol/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-11-15** · 加入KuaiRecV2公共评测协议入口，明确daily validation、按实例加权与single-retrieval evaluate-all；未核实官方仓库可访问，不伪称benchmark已接入，完整大规模评测高成本不复现。

涉及：[kuairec-v2-protocol](../../../recommendation-components/2611.16795-kuairec-v2-protocol/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

**2026-11-15** · 加入有六市场线上A/B的TriGen，区分固定窗口尾注入、pristine双路径与位置专属PFFN，保留observed-prefix边界。局部前后向不是完整推荐训练；完整工业矩阵高成本不复现。

涉及：[trigen](../../../recommendation-components/2611.16395-trigen/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

**2026-11-15** · 补入有量化线上A/B的ReSID，区分parallel/residual ID、prefix可达性与最终排序；CPU核不冒充推荐训练或生产性能，完整工业实验成本过高不复现。

涉及：[resid](../../../recommendation-components/2611.16404-resid/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md)

**2026-11-04** · 补入ReuseGR与SPADE，区分query前缀复用、用户历史条件、业务分词先验和父beam名次奖励；对照TIGER/PinGER保留不同输出对象与候选预算边界，不把CPU算子或完整A/B混成同层证据。

涉及：[reusegr](../../../recommendation-components/2611.04259-reusegr/README.md) · [spade-local-search](../../../recommendation-components/2611.04662-spade-local-search/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md) · [pinger](../../../recommendation-components/2610.33435-pinger/README.md)

**2026-10-30** · 精读PinGER三mask规则、单层LCP惩罚和逐prefixDPO锚；与TIGER历史SID成本及STATIC合法迁移分轴对照，保留多样性/recall取舍和整栈线上证据边界。

涉及：[pinger](../../../recommendation-components/2610.33435-pinger/README.md) · [tiger](../../../reproductions/2305.05065-tiger/README.md) · [static-constraint-decoding](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md)

**2026-10-29** · PailitaoMMSearch2.0将多意图图文请求直接解码为商品SID候选集合，以数据工具、CPT、混合预算SFT和意图均衡RL扩展服务。Sample–Beam使推理采样与候选束生成分别对应训练/展示需要；大模型或更长思考不保证所有意图更好。与其他生成式召回对比时应固定候选集合、预算和生产混排口径，而不是只比模型名字。完整方案本地不复现。

涉及：[pailitao-mmsearch2](../../../recommendation-components/2610.36958-pailitao-mmsearch2/README.md)

**2026-10-27** · 首版：比较tiger、cobra、plum、static-constraint-decoding、reward-guided-decoding，围绕物品表示：离散码、稀疏—稠密级联与LLM继续预训练与学习分布与推理搜索分别改变什么建立分析和跨论文问答。

覆盖 60 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 67 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation](../../../reproductions/2603.19710-aigq/README.md)
- [One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations](../../../reproductions/2609.18296-angle/README.md)
- [Bridging the Structural Gap: Adapting Autoregressive Generation for Recommendation](../../../reproductions/2607.21028-barge/README.md)
- [Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following](../../../reproductions/2602.13581-climber-pilot/README.md)
- [Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations](../../../reproductions/2503.02453-cobra/README.md)
- [Efficient Generative Retrieval for E-commerce Search with Semantic Cluster IDs and Expert-Guided RL](../../../reproductions/2605.14434-cq-sid/README.md)
- [DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation](../../../reproductions/2602.09744-diffureason/README.md)
- [DualGR: Generative Retrieval with Long and Short-Term Interests Modeling](../../../reproductions/2511.12518-dualgr/README.md)
- [EGR: Embedding-Native Generative Retrieval with a Shared LLM](../../../reproductions/2607.23038-egr/README.md)
- [From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation](../../../reproductions/2607.27789-feedback-policy/README.md)
- [Generative End-to-end Ad Retrieval at Douyin](../../../reproductions/2609.39327-gear/README.md)
- [GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation](../../../reproductions/2604.14878-genrec/README.md)
- [Deploying Semantic ID-based Generative Retrieval for Large-Scale Podcast Discovery at Spotify](../../../reproductions/2603.17540-glide/README.md)
- [Generative Recommendation for Large-Scale Advertising](../../../reproductions/2602.22732-gr4ad/README.md)
- [Learning to Reflect and Correct: Towards Better Decoding Trajectories for Large-Scale Generative Recommendation](../../../reproductions/2602.23639-grc/README.md)
- [Towards Sustainable Growth: A Multi-Value-Aware Retrieval Framework for E-Commerce Search](../../../reproductions/2605.17994-growthgr/README.md)
- [GRP v0.1 Technical Report](../../../reproductions/2609.36688-grp/README.md)
- [Gryphon-v2: One Model in Place of a Cascade — Generate-and-Rank Recommender with Rollout Distillation](../../../reproductions/2608.06213-gryphon-v2/README.md)
- [Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap](../../../reproductions/2607.26073-guess-where-you-go/README.md)
- [Hierarchical Residual Policy Optimization for Generative Recommendations](../../../reproductions/2608.00750-hrpo/README.md)
- [IntSR: An Integrated Generative Framework for Search and Recommendation](../../../reproductions/2509.21179-intsr/README.md)
- [LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System](../../../reproductions/2411.13789-leadre/README.md)
- [MBGR: Multi-Business Generative Recommendation](../../../reproductions/2604.02684-mbgr/README.md)
- [OneLatent: Latent Reasoning for Efficient Foundation Recommendation Models](../../../recommendation-components/2610.30675-onelatent/README.md)
- [OneMall: One Model, More Scenarios -- End-to-End Generative Recommender Family at Kuaishou E-Commerce](../../../reproductions/2601.21770-onemall/README.md)
- [OneRanker: Unified Generation and Ranking with One Model in Industrial Advertising Recommendation](../../../reproductions/2603.02999-oneranker/README.md)
- [OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment](../../../reproductions/2502.18965-onerec/README.md)
- [OneRec-V2 Technical Report](../../../reproductions/2508.20900-onerec-v2/README.md)
- [OxygenREC-v2: Internalizing Discrimination into Generative Recommendation](../../../reproductions/2607.24255-oxygenrec-v2/README.md)
- [PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems](../../../reproductions/2504.10507-pinrec/README.md)
- [PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations](../../../reproductions/2510.07784-plum/README.md)
- [PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations](../../../reproductions/2601.04674-promise/README.md)
- [PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation](../../../reproductions/2608.07989-pushdualgen/README.md)
- [From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark](../../../reproductions/2605.25514-qgs/README.md)
- [Recommendation as Generation: Unifying Personalized Video Generation and Recommendation at Industrial Scale](../../../reproductions/2606.25496-rag-generation/README.md)
- [Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment](../../../reproductions/2602.01023-rag-qac/README.md)
- [RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation](../../../reproductions/2603.28124-rclrec/README.md)
- [RecGPT-V3 Technical Report](../../../reproductions/2607.15591-recgpt-v3/README.md)
- [Reward Guided Decoding for Generative Recommendation](../../../reproductions/2607.25344-reward-guided-decoding/README.md)
- [RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems](../../../reproductions/2602.12968-rgalign-rec/README.md)
- [Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning](../../../reproductions/2602.13134-rolegen/README.md)
- [S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage](../../../reproductions/2602.10606-s-grec/README.md)
- [S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation](../../../reproductions/2601.18664-s2gr/README.md)
- [SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation](../../../reproductions/2502.10157-sessionrec/README.md)
- [SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress](../../../reproductions/2602.22913-sigma/README.md)
- [LLM-Based Generative Retrieval for Snapchat Content Recommendation](../../../reproductions/2607.28895-snaplgr/README.md)
- [Sona Technical Report](../../../reproductions/2608.11015-sona/README.md)
- [SPAR: Stepwise Personalized Autoregressive Recommendation with Prefix-Balanced Semantic IDs](../../../recommendation-components/2610.27898-spar-prefix-balance/README.md)
- [Vectorizing the Trie: Efficient Constrained Decoding for LLM-based Generative Retrieval on Accelerators](../../../recommendation-components/2602.22647-static-constraint-decoding/README.md)
- [TAGR: Temporally Adaptive Generative Recommendation for Industrial Live-Streaming Advertising](../../../reproductions/2608.24034-tagr/README.md)
- [TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning](../../../reproductions/2609.00986-tgr/README.md)
- [Recommender Systems with Generative Retrieval](../../../reproductions/2305.05065-tiger/README.md)
- [TSGR: Taobao Search Generative Retrieval](../../../reproductions/2607.18796-tsgr/README.md)
- [UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation](../../../reproductions/2609.23718-unique/README.md)
- [Unifying Generative Recall and Multi-Objective Ranking in a Single Decoder-Only Sequence](../../../reproductions/2607.24439-unir2/README.md)
- [UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute](../../../reproductions/2604.12234-unirec-coa/README.md)
- [UniSGR-V2: Stepwise Target-Side Feature Anticipation and Crossing for Generative Recommendation](../../../reproductions/2610.16132-unisgr-v2/README.md)
- [Unified Value Alignment for Generative Recommendation in Industrial Advertising](../../../reproductions/2605.05803-univa/README.md)
- [WeGR: Unified Generative Retrieval for Industrial Search Systems in WeChat](../../../reproductions/2610.16979-wegr/README.md)
- [X-Rec Technical Report](../../../reproductions/2609.29180-xrec/README.md)
- [PailitaoMMSearch2.0 Technical Report: Scaling Generative Retrieval to Unified End-to-End Multimodal Search](../../../recommendation-components/2610.36958-pailitao-mmsearch2/README.md)
- [PinGER: Token-Efficient Generative Retrieval with Semantic IDs](../../../recommendation-components/2610.33435-pinger/README.md)
- [ReuseGR: Offline–Online Decoupled Generative Retrieval via Adaptive Prefix Reuse](../../../recommendation-components/2611.04259-reusegr/README.md)
- [SPADE: Spatiotemporal Preference Alignment and Diversity Enhancement for Local Search](../../../recommendation-components/2611.04662-spade-local-search/README.md)
- [ReSID: Rethinking Long-Tail Retrieval in Generative Recommendation through item Reachability](../../../recommendation-components/2611.16404-resid/README.md)
- [TriGen: A Generative Paradigm for Trigger-Induced Recommendation](../../../recommendation-components/2611.16395-trigen/README.md)
- [KuaiRecV2: Benchmarking Large-Scale Continual Learning for Diversified and Multi-task Recommendation](../../../recommendation-components/2611.16795-kuairec-v2-protocol/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/recommendation/generative-retrieval-reasoning.md) · [返回全部精读卡片](../index.md)
