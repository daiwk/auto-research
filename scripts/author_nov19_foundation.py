"""Authored bilingual fixed-v1 foundation intake; no global generated files."""

from hashlib import sha256
import json
from pathlib import Path

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov19-latest/foundation"
AUDIT = ROOT / "docs/research-audits/nov19-latest"
DATE = "2026-11-19"

DIAGRAMS = {
    "kernel-ridge-attention": "flowchart LR\n X[Projected causal Q K V] --> F[Shared learned Fourier features]\n C[Content clock] --> P[OU coefficient decay and covariance recovery]\n F --> R[Covariance guided residual write]\n P --> R\n R --> O[Inclusive query read]",
    "narrow-spec": "flowchart LR\n T[Target features] --> N[Narrow residual stream]\n N --> A[Output adapter]\n A --> H[Frozen target LM head]\n N --> F[Folded narrow head]\n F --> L[Same real arithmetic logits]\n H --> L",
    "loopcache-interface": "flowchart LR\n G[Global step] --> C[Cyclic KV loop]\n D[Current draft logits] --> M[New old margin threshold]\n M --> P[Replace and prune descendants]\n C --> S[Approximate spec branch external]\n S --> E[Exact full KV branch external]\n E --> T[Verified token commit external]",
    "counterfactual-wm": "flowchart LR\n O[Observed factual outcome] --> R[Observed residual]\n F[Factual action prediction] --> R\n A[Alternative action prediction] --> C[Residual reuse]\n R --> C\n C --> L[Same event alternative estimate]",
    "autoregressive-view-model": "flowchart LR\n I[Prefill views] --> R[Bounded context retrieval]\n H[Generated history] --> R\n C[Camera path] --> R\n R --> V[14B video flow model]\n V --> T[Causal rollout tuning and distillation]\n T --> N[New view clip]\n N --> H",
}


PAPERS = [
    dict(
        aid="2611.23896",
        key="kernel-ridge-attention",
        domain="foundation-models",
        title="Kernel Ridge Attention: Nonlinear Memory with Selective Forgetting",
        cn_title="KRA：在遗忘时恢复不确定性，用协方差决定写入方向",
        author="Haowei Chen",
        org="Independent Researcher",
        priority="P1",
        topic=["注意力与长上下文", "递归状态与核回归"],
        card="foundation-models/context-and-state",
        peer="foundation-models:mamba",
        module="kernel_ridge_attention",
        cuda=True,
        tier="l1_mechanism",
        sections=["2.1–2.4", "3", "4.1–4.4", "Appendix C/E"],
        code=None,
        revision=None,
        code_cn="固定v1未找到作者KRA源码；引用的FLA是依赖，不能算本方法已开源。",
        code_en="No author KRA implementation was found in fixed v1. Cited FLA is a dependency, not this method release.",
        overview_cn="KRA把历史关联写入固定大小的回归矩阵，同时保留后验协方差。共享可学习Fourier特征形成非线性核；内容相关OU时钟既衰减旧系数，也把协方差恢复到先验，使已经遗忘的方向重新可写。读取发生在当前值写入之后。",
        overview_en="KRA stores associations in fixed-size regression coefficients and posterior covariance. Shared learned Fourier features supply a nonlinear kernel. A content-dependent OU clock decays coefficients while restoring uncertainty toward the prior, reopening forgotten directions for writing. Reads include the current write.",
        formula=r"\bar\Theta_t=\delta_t\Theta_{t-1},\quad\bar P_t=\delta_t^2P_{t-1}+(1-\delta_t^2)\lambda^{-1}I,\quad G_t=\frac{\bar P_ta_t}{1+a_t^\top\bar P_ta_t},\quad\Theta_t=\bar\Theta_t+G_t(v_t-\bar\Theta_t^\top a_t)^\top,\quad P_t=\bar P_t-\frac{(\bar P_ta_t)(\bar P_ta_t)^\top}{1+a_t^\top\bar P_ta_t},\quad o_t=\Theta_t^\top b_t.",
        detail_cn="a、b由同一组cos/sin频率映射，范数为1。P不是可省略的标量门；它会旋转并缩放写入方向。独立dual参考求解内容Gram与OU时间Gram的乘积核，按每个因果prefix核对输出。",
        detail_en="Keys and queries share unit-norm sine/cosine features. P rotates and rescales a write; it is not a scalar gate. An independent dual reference solves each causal prefix with the product of content and OU-time Gram matrices.",
        results_cn="原文100M-token同预算实验中，KRA验证PPL为88.00，Transformer++为97.21；但自然稀有重复top-1为25.41%，低于Transformer++的32.00%。不能概括成所有记忆指标均优。仅一个训练seed，未报告生产线上A/B。",
        results_en="At the paper’s matched100M-token budget, validation perplexity is88.00 versus97.21 for Transformer++. Rare-repeat top1 is25.41%, below Transformer++32.00%; memory is not uniformly better. Training uses one seed. No production A/B is reported.",
        local_cn="实现共享Fourier特征、OU预测、协方差引导RLS、inclusive读取及状态续接；不含width4因果卷积前端、完整decoder、手写并行adjoint或融合内核。dual solve只作独立小规模参考，不能当高效推理路径。",
        local_en="Implements shared Fourier features, OU prediction, covariance-guided RLS, inclusive reads and streaming continuation. It excludes the width4 convolution frontend, decoder, parallel adjoints and fused kernels. The expensive dual solve is only a small independent reference.",
        compare_cn="Mamba用输入相关步长和读写向量控制SSM状态；KRA额外维护后验协方差来处理相关key方向的干扰。两者都是有界状态，但KRA每头还承担D平方协方差存储，不能仅按线性序列复杂度认为成本相同。",
        compare_en="Mamba controls an SSM with input-dependent steps and read/write vectors. KRA additionally maintains covariance to handle correlated-key interference, costing D-squared state per head. Bounded context-independent state does not make their costs identical.",
        cost_cn="原文约30.92M参数，100,007,936训练token、3,052更新，八张RTX5090、多个模型/消融；本轮单A100/A30不重做完整预训练矩阵。",
        cost_en="The paper trains30.92M parameters on100,007,936tokens for3,052updates using eight RTX5090 GPUs, plus baseline/ablation runs. The full pretraining matrix is outside this single-device short-run budget.",
        qa=[
            (
                "why-covariance",
                "basics",
                "为什么遗忘旧信息时还要补回协方差？",
                "协方差表示哪些特征方向仍可被新观测约束。只缩小P会让所有方向越来越难写；OU恢复项让遗忘同时恢复可塑性。",
                "教学例：delta=0.5且P=0.1I时，先验为I，预测P为0.775I，不是0.025I。",
                "Why restore covariance when forgetting?",
                "Covariance records which directions remain uncertain. Decaying P alone progressively suppresses writes; the OU prior term restores plasticity.",
                "With delta0.5, P0.1I and priorI, predicted P is0.775I, not0.025I.",
            ),
            (
                "write-geometry",
                "mechanism",
                "KRA为何不能用一个学习率乘key替代增益？",
                "增益由P乘key再归一化，非各向同性P会改变方向，不只是改变长度。",
                "教学例：key=(1,1)，P=diag(0.4,0.2)时写入方向比例为2:1，而非1:1。",
                "Why is a scalar write rate insufficient?",
                "P times the key can rotate the gain, not merely scale it. A scalar rate cannot reproduce anisotropic covariance geometry.",
                "For key(1,1) and P=diag(0.4,0.2), the write direction is2:1 rather than1:1.",
            ),
            (
                "mamba-state",
                "comparison",
                "与Mamba相比，多保留了什么状态？",
                "除回归系数外还有每头D乘D协方差；它描述已约束方向。Mamba的selective scan并不维护同一后验几何。",
                "教学例：D翻倍时，协方差元素从D平方变成4D平方，即使上下文长度不变。",
                "What extra state distinguishes it from Mamba?",
                "KRA stores a per-head D-by-D covariance in addition to regression coefficients. Mamba selective scans do not maintain that posterior geometry.",
                "Doubling D quadruples covariance elements even with fixed context length.",
            ),
            (
                "dual-validation",
                "implementation",
                "本地dual一致能证明论文吞吐吗？",
                "不能。它核对给定feature/clock序列的数学输出；完整网络、并行scan、精度和八卡训练未运行。",
                "教学例：逐prefix矩阵求逆虽可作正确性参考，却比递推更慢。",
                "Does dual parity prove paper throughput?",
                "No. It checks outputs for a fixed feature/clock path. The full network, parallel scan, precision strategy and eight-GPU training are absent.",
                "Repeated prefix solves are a correctness reference, not a fast serving algorithm.",
            ),
        ],
    ),
    dict(
        aid="2611.23835",
        key="narrow-spec",
        domain="foundation-models",
        title="NarrowSpec: Draft Hidden Width Need Not Match the Target in Speculative Decoding",
        cn_title="NarrowSpec：缩窄整个草稿残差流，而不只是词表投影",
        author="Alagappan Valliappan",
        org="NVIDIA",
        priority="P1",
        topic=["推理与系统效率", "推测解码与权重折叠"],
        card="foundation-models/generation-paths",
        peer="foundation-models:loopspec",
        module="narrow_spec",
        cuda=True,
        tier="l1_mechanism",
        sections=["2.1–2.4", "3", "Appendix B/C/D"],
        code=None,
        revision=None,
        code_cn="未找到可核验的独立NarrowSpec方法源码修订。正文使用[SpecForge](https://github.com/sgl-project/SpecForge)训练并列出released drafters；通用训练框架不等于本方法源码已发布。",
        code_en="No independently verified NarrowSpec source revision was found. The paper uses[SpecForge](https://github.com/sgl-project/SpecForge) and lists released drafters; a general training framework is not proof that this method implementation is released.",
        overview_cn="把DFlash/EAGLE-3的整个残差宽度设为目标的二分之一或四分之一，并从头训练窄草稿；边界adapter连接目标hidden和共享词表。DFlash输出adapter可与目标head相乘，EAGLE-3输入adapter可折进embedding。head数量和head维度保持不变，因此KV cache不因残差流变窄而自动缩小。",
        overview_en="DFlash/EAGLE-3 residual width is halved or quartered and the narrow drafter is trained from scratch. Boundary adapters connect target features and token space. DFlash folds its output adapter into the target head; EAGLE-3 can fold its input adapter into embeddings. Head geometry stays fixed, so KV cache size does not automatically shrink.",
        formula=r"W_{\rm fold}=W_{\rm lm}W_{\rm out},\quad W_{\rm lm}(W_{\rm out}h_d)=W_{\rm fold}h_d,\qquad E_{\rm fold}=E_tW_{\rm in}^{\top}.",
        detail_cn="两侧线性映射之间没有额外非线性或norm才能直接折叠。浮点结合顺序变化会改变舍入，不能要求bitwise一致；Q(WlmWout)一般不等于Q(Wlm)Wout，预先量化的head不能据此保证等价。",
        detail_en="A fold requires consecutive linear maps without intervening normalization/nonlinearity. Floating-point association changes rounding, so equality is not bitwise. Quantizing a product generally differs from multiplying a quantized head; a pre-quantized head is not covered by this identity.",
        results_cn="原文batch1/temperature0下端到端解码加速：B200为1.06–1.12倍，GB10为1.13–1.44倍。结果依赖训练后的接受长度和verify代价，不是矩阵维度比例本身；未报告生产线上A/B。",
        results_en="At batch1 and temperature0, reported end-to-end speedups are1.06–1.12x on B200 and1.13–1.44x on GB10. These depend on trained acceptance and verification cost, not width ratio alone. No production A/B is reported.",
        local_cn="仅实现两种边界折叠及输入/输出、hidden梯度一致性；不构造或训练DFlash/EAGLE-3，不运行目标模型、token接受/拒绝或SGLang。量化不交换负控使用说明性均匀量化，不冒充论文NVFP4内核。",
        local_en="Only the two boundary folds and output/input/hidden-gradient parity are implemented. There is no trained drafter, target model, token verifier or SGLang integration. A simple uniform-quantization negative control is illustrative, not the paper NVFP4 kernel.",
        compare_cn="LoopSpec改变looped模型的推测/验证流水线；NarrowSpec改变草稿网络的残差宽度，并保持目标verify不变。一个降低等待，一个减少草稿计算，不能用折叠等价证明任一方法的接受率。",
        compare_en="LoopSpec changes the draft/verify pipeline of a looped model. NarrowSpec narrows drafter residuals while leaving target verification unchanged. Pipeline waiting and drafter work are different axes; fold parity says nothing about acceptance quality.",
        cost_cn="Qwen3-8B与GPT-OSS-20B目标、DFlash/EAGLE-3三种宽度，四张B200训练；DFlash6epochs、EAGLE-3为3epochs，并做32K上下文和B200/GB10/H100服务矩阵。完整训练/服务实验超单A100/A30短预算。",
        cost_en="Two8B/20B targets, two drafter families and three widths train on four B200 GPUs: six DFlash epochs or three EAGLE-3 epochs. The32K-context B200/GB10/H100 serving matrix is not reproduced on one A100/A30.",
        qa=[
            (
                "residual-not-head",
                "basics",
                "只缩词表head是否等于NarrowSpec？",
                "不是。该方法缩整个残差流，包括读写残差的attention/MLP投影；词表head折叠只是边界处理。",
                "教学例：只把head低秩化仍保留原宽度的每层MLP，没执行本文主要干预。",
                "Is shrinking only the vocabulary head NarrowSpec?",
                "No. It narrows the whole residual stream and projections that read/write it. Head folding is only boundary handling.",
                "A low-rank head with unchanged decoder MLPs does not perform the principal intervention.",
            ),
            (
                "linear-fold-condition",
                "mechanism",
                "什么时候可以把输出adapter折进LM head？",
                "当两者是连续线性映射时，按Wlm乘Wout合并；若中间有norm或非线性则不能这样折。",
                "教学例：Wlm ReLU(Wout h)不等于(WlmWout)h。",
                "When may the output adapter be folded?",
                "When two consecutive maps are linear, combine Wlm times Wout. Intervening normalization or nonlinearity invalidates that fold.",
                "Wlm ReLU(Wout h) is not generally (WlmWout)h.",
            ),
            (
                "pipeline-versus-width",
                "comparison",
                "与LoopSpec降低推理开销的方向有什么不同？",
                "LoopSpec安排循环深度间的推测与验证；NarrowSpec减少草稿每次前向的残差宽度，不改变目标verify。",
                "教学例：较窄草稿仍可能因为接受长度变短而抵消每轮节省。",
                "How does this differ from LoopSpec?",
                "LoopSpec schedules speculation and verification across recurrent depths. NarrowSpec reduces drafter residual width without changing target verification.",
                "Fewer drafter operations can be offset by shorter acceptance length.",
            ),
            (
                "cache-and-quantization",
                "implementation",
                "本地折叠成功能否推出KV减半、量化等价和解码提速？",
                "都不能。原head几何固定；量化与矩阵乘法不交换；端到端速度还需训练后接受率和硬件验证。",
                "教学例：8维残差改4维，但KV heads与head_dim都不变时，KV张量元素数不变。",
                "Does fold parity imply smaller KV, quantization parity or speedup?",
                "No. Head geometry is fixed, quantization does not commute with multiplication, and speed depends on trained acceptance and hardware.",
                "Halving residual width leaves KV elements unchanged when head count and head dimension stay fixed.",
            ),
        ],
    ),
    dict(
        aid="2611.24301",
        key="loopcache-interface",
        domain="foundation-models",
        title="LoopCache: Accelerating Long-Context Self-Speculative Decoding for Looped Transformers",
        cn_title="LoopCache：循环KV调度与有条件草稿更新接口",
        author="Zizhuo Fu",
        org="Peking University",
        priority="P1",
        topic=["推理与系统效率", "循环模型与KV调度"],
        card="foundation-models/compression-and-cache",
        peer="foundation-models:spool",
        module="loopcache_interface",
        cuda=False,
        tier="l0_interface",
        sections=["4.1–4.3", "5.1–5.3"],
        code="https://github.com/zZzZ9zZ9/LoopCache",
        revision="0ebecb21cc1bfb4a26696496694e25ba9e819e68",
        code_cn="是：[作者仓库](https://github.com/zZzZ9zZ9/LoopCache)，MIT；只读核验HEAD `0ebecb21cc1bfb4a26696496694e25ba9e819e68`，未复制执行上游服务程序。",
        code_en="Yes:[author repository](https://github.com/zZzZ9zZ9/LoopCache), MIT, inspected HEAD`0ebecb21cc1bfb4a26696496694e25ba9e819e68`. Upstream serving code was not copied or executed.",
        overview_cn="固定深度的draft可能沿过时轨迹继续推进。LoopCache用新候选相对旧候选的logit差控制替换，并清除依赖旧token的所有后代。推测路径轮转读取同一loop cache，独立KV分支再以正确loop缓存重算；浅层差异较大时才单独读取对应loop的cache。",
        overview_en="A fixed-depth draft can remain on a stale trajectory. LoopCache replaces it only when the new-versus-old logit margin is large enough and prunes dependent descendants. Speculation shares a cyclic cache while a separate exact KV branch recomputes with correct loop caches. Selected shallow layers may decouple when loop mismatch is large.",
        formula=r"c(g)=1+((g-1)\bmod R),\quad \mathrm{update}\iff s\ne x\ \land\ z_r(s)-z_r(x)\ge\tau;\quad KV_\ell^{spec}(d,c)=\begin{cases}KV_{\ell,d}&\ell\in\mathcal S, |d-c|\ge\delta\\KV_{\ell,c}&\text{otherwise}.\end{cases}",
        detail_cn="阈值相等也触发替换；无需未来loop预测来决定当前更新。未来回到旧token的harmful-switch定义只用于分析，不能变成运行时oracle。近似spec cache不能直接提交token，必须等待独立exact分支。",
        detail_en="Equality at the margin threshold triggers replacement. Future-loop harmful-switch labels are analysis only, never runtime oracles. Approximate speculative-cache computation cannot commit a token; the exact branch is mandatory.",
        results_cn="原文在六类looped模型、4K–128K上下文上报告相对WFD/LoopSpec平均10.25倍/14.56倍速度；完整实验用八张A100和长上下文并行。这里不重测速度或接受率；未报告生产线上A/B。",
        results_en="Across six looped models and4K–128K contexts, reported average speedups are10.25x/14.56x over WFD/LoopSpec. The full campaign uses eight A100 GPUs and long-context parallelism. Local code reports neither speed nor acceptance. No production A/B is reported.",
        local_cn="仅实现Eq2–4的阈值更新、循环loop编号、浅层cache选择及最近完整验证周期接口，标记L0。没有模型、实际KV内存、exact verifier、随机采样拒绝或token提交；tokens_committed固定为0是接口边界，不是模型指标。",
        local_en="L0 implements margin updates, cyclic loop IDs, shallow-cache selection and the next full verification-cycle interface. It includes no model, real KV buffers, exact verifier, rejection sampler or token commit. A zero committed-token counter describes scope, not model performance.",
        compare_cn="Spool重建固定记录层输入下的递归状态；LoopCache安排loop-specific KV读取并以exact分支纠正近似推测。前者的摘要精确性与后者的目标解码精确性证明对象不同。",
        compare_en="Spool reconstructs recurrent state for fixed recorded layer inputs. LoopCache schedules loop-specific KV reads and corrects approximate speculation through an exact branch. Their exactness claims concern different objects.",
        cost_cn="六个0.84B–3.5B模型，最长128K上下文；原文全部实验使用八张A100，长上下文用context parallelism，并额外训练DFlash。完整服务/训练矩阵超本轮单卡资源。",
        cost_en="Six0.84B–3.5B models, contexts up to128K, eight A100 GPUs, context parallelism and an additionally trained DFlash baseline exceed this single-device short-run budget.",
        qa=[
            (
                "why-shared-loop",
                "basics",
                "循环cache调度解决什么瓶颈？",
                "将单步读取的长前缀cache从多个loop集中为一个；这减少读取来源，不代表推测计算已变为精确。",
                "教学例：R=4时全局步骤依次读取1、2、3、4、1，但spec token当前深度可能是3。",
                "What does cyclic-cache scheduling reduce?",
                "It concentrates long-prefix reads onto one loop cache per step. This does not make mismatched speculative computation exact.",
                "For R4, cache IDs cycle1,2,3,4,1 while a speculative token may be at depth3.",
            ),
            (
                "margin-and-pruning",
                "mechanism",
                "替换草稿为什么必须清理后代？",
                "后代以旧token为条件，旧token换掉后其hidden/cache依赖失效。门槛使用当前新旧logit差，不读取未来是否翻回。",
                "教学例：旧draft=A，后代为B/C；A改D后不能把原B/C接在D后直接验证。",
                "Why prune descendants after replacing a draft?",
                "Their hidden/cache states depended on the old token. The decision uses the current margin, not future reversal labels.",
                "Replacing ancestor A with D invalidates descendants B/C computed under A.",
            ),
            (
                "spool-exactness",
                "comparison",
                "与Spool的精确状态重建是同一个承诺吗？",
                "不是。Spool对固定记录输入重放状态变换；LoopCache的lossless token提交还依赖完整正确loop KV分支。",
                "教学例：调度编号正确不意味着已运行目标模型验证。",
                "Is this the same exactness as Spool?",
                "No. Spool replays transitions for fixed recorded inputs. Lossless token commitment in LoopCache also needs the correct full KV branch.",
                "A correct schedule ID does not imply that target verification ran.",
            ),
            (
                "interface-not-decoder",
                "implementation",
                "接口测试全过为何仍只标L0？",
                "本地没有token verifier和真实KV执行，不能验证最终分布或lossless输出；只检验决定何时更新、读取哪份cache的合同。",
                "教学例：tokens_committed=0明确表明没有输出能力评测。",
                "Why is a passing implementation still L0?",
                "No real KV execution or token verifier is implemented, so output distributions and losslessness are untested. Only update/read policy contracts are checked.",
                "The committed-token count is zero because no decoder ran.",
            ),
        ],
    ),
    dict(
        aid="2611.24778",
        key="counterfactual-wm",
        domain="foundation-models",
        title='Counterfactual World Models: JEPAs That Reason About "What If"',
        cn_title="Counterfactual WM：复用已发生事件的残差，而非预测平均未来",
        author="Randall Balestriero",
        org="Brown University / AMI Labs",
        priority="P1",
        topic=["世界模型与JEPA", "反事实预测与可识别性"],
        card="multimodal-models/world-state-actions",
        peer="foundation-models:dt-jepa",
        module="counterfactual_wm",
        cuda=True,
        tier="l1_mechanism",
        sections=["2.1–2.3", "3.1–3.4", "4.2–4.4", "Appendix B/D"],
        code=None,
        revision=None,
        code_cn="固定PDF列出[作者方法仓库](https://github.com/galilai-group/counterfactual-WM)，本轮只读请求返回404，未能核验可获取源码/修订/许可证；不写成已成功获取开源实现。",
        code_en="The fixed PDF links[the method repository](https://github.com/galilai-group/counterfactual-WM), but this review received404. Accessible code, revision and license could not be verified; the link is not presented as successfully retrieved source.",
        overview_cn="普通world model给动作的平均结果，不能仅凭更准的事实分布识别同一扰动下的个体反事实。本文将实际观测结果作为事件信息，加上同一事实预测器对两个动作的预测差；加性扰动时精确，平滑短时动力学下有交互误差界，但碰撞、乘法故障和弯曲坐标可破坏近似。",
        overview_en="A factual world model estimates average outcomes, not the same-event coupling between actions. This method combines an observed outcome with the factual predictor’s action contrast. It is exact under additive disturbances, with interaction bounds for smooth short transitions; contacts, gain faults and curved coordinates can break it.",
        formula=r"\hat z(a')=z_{obs}+\mu(H,a')-\mu(H,a),\qquad T_R-Y(a')=\mathbb E[\Delta]-\Delta,\quad\Delta=Y(a')-Y(a).",
        detail_cn="观测是已经执行动作a之后的结果，替代动作真值不作为算法输入。先在embedding运输后decode，与先decode每项再做残差运输一般不同；选择坐标需要额外readout假设。误差等于个体动作效应与平均动作效应之差，不是“world model零误差就保证反事实零误差”。",
        detail_en="The observed input follows the factual action; the true alternative outcome is never an algorithm input. Transport-then-decode differs from decoding each term before transport. Coordinate guarantees need readout assumptions. Error is individual-minus-average action effect, not simply factual-model prediction error.",
        results_cn="原文四个像素模拟环境中反事实R平方从38%–46%升到86%–96%；第五个水下环境用16倍事实数据，达到90%–94%。这些依赖冻结编码器、训练预测器和模拟器分支回放，不是本地算子结果；未报告生产线上A/B。",
        results_en="In four pixel-based simulators, reported counterfactual R-squared rises from38–46% to86–96%. A fifth underwater task uses16times more factual data and reaches90–94%. These require frozen encoders, fitted predictors and simulator replay, not this local operator. No production A/B is reported.",
        local_cn="执行Eq6残差复用和Eq7 readout坐标运输，严格拒绝隐式broadcast；加性系统验证等式，乘法gain fault与非线性readout保留预期失效。未训练JEPA、加载encoder、采集模拟轨迹或执行规划；诊断中的分析函数不冒充训练好的world model。",
        local_en="Implements equation6 residual reuse and equation7 readout-space transport, rejecting implicit broadcasting. Tests establish additive exactness and preserve expected failures under gain faults/nonlinear readouts. No JEPA training, encoder, simulator collection or planning runs. Analytic diagnostics are not trained world models.",
        compare_cn="DT-JEPA在历史下预测未来latent分布并用于决策，真实未来只在训练目标出现；CWM在一个事实结果已经可见后推断同一事件的替代动作结果。不能让CWM提前使用尚未观测的未来，亦不能把DT-JEPA的均值直接称个体反事实。",
        compare_en="DT-JEPA predicts future latent distributions from history for decision making; true futures appear only in training. CWM answers alternative actions after a factual outcome is observed. It cannot access an unobserved future, and a DT-JEPA mean is not automatically an individual counterfactual.",
        cost_cn="完整评测含多个冻结视觉encoder、五个像素模拟环境、1024宽两层predictor、每fit20,000更新/batch256/三种子及历史/readout/规划矩阵。没有总GPU小时披露；根据训练和模拟组合判断超单卡短时预算，不试跑扩大。",
        cost_en="Full evaluation combines several frozen visual encoders, five pixel simulators, width1024 two-block predictors,20,000updates per fit at batch256/three seeds, and history/readout/planning sweeps. Total GPU hours are not stated; configuration-based cost exceeds this short-run budget, without a costly probe.",
        qa=[
            (
                "average-versus-event",
                "basics",
                "为什么平均未来预测准确还不等于反事实准确？",
                "事实分布只给不同动作的边缘结果，没说明两种结果属于同一扰动事件的哪一对。个体反事实需要这份配对结构。",
                "教学例：U与1-U都均匀分布，但观测U=0.2时两种耦合的替代结果分别是0.2和0.8。",
                "Why is an accurate average future not an individual counterfactual?",
                "Factual laws give marginals per action, not their same-disturbance pairing. Individual counterfactuals need that coupling.",
                "U and1-U are both uniform, but observing U0.2 implies alternatives0.2 or0.8 under different couplings.",
            ),
            (
                "residual-reuse",
                "mechanism",
                "残差复用到底复用了什么？",
                "复用事实观测与事实预测之差，再加到替代动作预测上；无需恢复真实扰动变量。只在动作与扰动的交互足够小等条件下可靠。",
                "教学例：原预测向东1米，实测1.3米；替代预测向北1米时保留这次事件的0.3米漂移。",
                "What is reused by residual reuse?",
                "The observed-minus-factual-prediction residual is added to the alternative prediction. The true disturbance need not be recovered; reliability still needs suitable interaction assumptions.",
                "A0.3-meter event-specific drift is retained when changing the predicted command.",
            ),
            (
                "dt-jepa-information",
                "comparison",
                "与DT-JEPA查询时的信息有什么不同？",
                "DT-JEPA用行动前历史预测未来；CWM需已执行事实动作的结果。允许的信息集和问题不同，不能比较为同一预测任务。",
                "教学例：第一次执行动作前不能拿尚不存在的observed_outcome喂CWM。",
                "How does its information set differ from DT-JEPA?",
                "DT-JEPA predicts before acting from history. CWM needs the observed factual outcome. They answer different queries with different information.",
                "Before the first action, its not-yet-observed outcome cannot be passed to CWM.",
            ),
            (
                "failure-control",
                "implementation",
                "为什么测试里应保留乘法故障的非零误差？",
                "该故障使扰动与动作相乘，个体动作效应随事件变化，违反共享加性残差条件。清掉误差会掩盖论文已说明的边界。",
                "教学例：实际执行只有命令的50%时，原动作残差不能无条件照搬到两倍命令上。",
                "Why preserve nonzero gain-fault error?",
                "A disturbance multiplying the command makes action effects event-specific and breaks shared additive residuals. Hiding error would erase a stated limitation.",
                "If only50% of a command is delivered, its residual cannot simply be reused for twice the command.",
            ),
        ],
    ),
    dict(
        aid="2611.23417",
        key="autoregressive-view-model",
        domain="multimodal-models",
        title="Autoregressive View Model",
        cn_title="AVM：把场景作为带检索上下文的视图流生成",
        author="Jensen (Jinghao) Zhou",
        org="Meta / University of Oxford",
        priority="P0",
        topic=["世界模型", "自回归视频与场景持久性"],
        card="multimodal-models/world-state-actions",
        peer="foundation-models:counterfactual-wm",
        module=None,
        cuda=False,
        tier="review_only",
        sections=["3.1–3.4", "4", "5.1–5.4", "Appendix B/E"],
        code=None,
        revision=None,
        code_cn="原文[项目页](https://autoregressive-view-model.github.io)本轮请求404；固定v1未找到已发布的AVM方法源码/许可证。Wan2.1及评价工具是依赖，不算AVM开源。",
        code_en="The[project page](https://autoregressive-view-model.github.io) returned404 in this review. No released AVM method source/license was verified in fixed v1. Wan2.1 and evaluation tools are dependencies, not AVM source.",
        overview_cn="AVM不拟合显式3D表示，而在给定相机路径下生成短视图片段。预填图像/视频与历史生成片段统一成为context；检索保持活动上下文有界。先把双向视频DiT微调为N-in-1-out的flow matching，再以自身rollout做因果tuning和蒸馏，让生成内容可回到历史中支持后续重访。",
        overview_en="AVM streams short view clips along a camera path without fitting explicit3D geometry. Prefill observations and generated history share one context interface, with retrieval bounding active context. An N-in-1-out flow-matching model is followed by causal tuning/distillation on its own rollouts so earlier outputs can support revisits.",
        formula=r"\mathcal L_{FM}=\mathbb E\|v_\theta(x_t,t,C)-v_{target}\|^2,\qquad C_g=\operatorname{Retrieve}(C_{prefill}\cup C_{history},\operatorname{camera}_g).",
        detail_cn="上式用统一记号概括原文flow目标与context检索，不补造新的算法。检索对象既有真实输入也有模型生成的历史；没有显式3D不等于没有几何条件。相机、时间和context角色仍影响生成。",
        detail_en="The notation summarizes the paper flow objective and context retrieval, not a new algorithm. Retrieved history includes both observations and model-generated views. No explicit3D representation does not mean no geometric conditioning: cameras, time and context roles still matter.",
        results_cn="原文分别评测camera/text/object控制、视觉质量、动态性和图像/视频/历史context下的场景持久性；这些是不同任务维度，不能仅用一张相似图片声称全部完成。论文未报告生产随机流量线上A/B，本轮没有复跑其表格。",
        results_en="Evaluation separates camera/text/object control, visual quality, dynamics and persistence under image/video/history context. A single similar image cannot establish all dimensions. No randomized production A/B is reported; none of its benchmark tables is reproduced locally.",
        local_cn="仅原文方法、机构、成本与边界收录；没有operator、模型加载、训练、合成数据、metrics或GPU回执。不会用通用图像相似度/检索fixture代替14B视频模型的场景持久性。",
        local_en="Review-only method, affiliation, cost and boundary intake. No operator, checkpoint, training, synthetic-data pipeline, metrics or GPU receipt is supplied. Generic similarity/retrieval fixtures do not substitute for a14B video model’s persistence.",
        compare_cn="CWM在一个事实事件之后改变动作并复用同一扰动残差；AVM沿相机轨迹继续生成并检索历史视图。二者都使用world model语汇，但AVM的场景重访一致性不证明同一扰动反事实可识别。",
        compare_en="CWM changes an action after an observed event and reuses its disturbance residual. AVM continues camera-conditioned generation with retrieved history. Scene-revisit consistency does not establish identifiable same-disturbance counterfactuals.",
        cost_cn="固定v1使用14B视频diffusion transformer，约8M场景/视频，含双向flow训练、因果tuning、自rollout蒸馏和多维视频评测。本机单A100/A30或Mac无法在本轮短时低成本预算忠实重做，不下载权重/视频，不运行大模型探针。",
        cost_en="Fixed v1 uses a14B video diffusion transformer and approximately8M scenes/clips, with bidirectional flow training, causal tuning, on-policy distillation and multidimensional video evaluation. A faithful campaign is beyond one A100/A30 or Mac short-run budget; no weights, videos or model probes are downloaded/run.",
        qa=[
            (
                "view-stream",
                "basics",
                "没有显式3D表示，AVM怎样保留可用场景信息？",
                "用预填和历史视图作context，并按当前相机查询检索活动子集；它是生成条件，不是拟合NeRF或高斯场景。",
                "教学例：重访一间屋子时可检索此前生成的门和桌面视角，而不是重建一份完整mesh。",
                "How is scene information retained without explicit3D?",
                "Prefill and history views provide context, with an active subset retrieved for the camera query. This conditions generation rather than fitting a NeRF or Gaussian scene.",
                "A room revisit can retrieve earlier door/table views without a complete mesh.",
            ),
            (
                "own-rollouts",
                "mechanism",
                "为什么双向训练后还做自身rollout的因果tuning？",
                "流式后续生成会接触自己产生的历史；只在真实context训练不覆盖这类误差累积。因果tuning和蒸馏处理流式路径与少步采样。",
                "教学例：早期生成的桌腿略偏，后续片段需在这一历史上保持或修正，而非总拿真实桌腿作context。",
                "Why causal tuning on self-rollouts after bidirectional training?",
                "Streaming sees generated history and accumulated errors absent from purely factual context. Causal tuning/distillation addresses that path and few-step sampling.",
                "Later clips may condition on a slightly misplaced generated table leg, not always a real one.",
            ),
            (
                "counterfactual-not-revisit",
                "comparison",
                "场景重访一致是否等于CWM的反事实能力？",
                "不等于。重访是在相机轨迹和生成历史下维持场景；个体反事实还需同一扰动下不同动作结果的耦合假设。",
                "教学例：门框位置保持不变，不能说明同一阵风下船改航向会到哪里。",
                "Does revisit consistency imply CWM counterfactual ability?",
                "No. Revisit persistence concerns camera paths and generated history. Individual counterfactuals require a same-disturbance coupling across actions.",
                "A stable door frame says nothing about a boat’s alternative heading in the same wind.",
            ),
            (
                "no-cheap-shadow",
                "implementation",
                "为什么本轮不加一个检索小样例就算复现？",
                "检索只是AVM一部分，不能替代14B视频生成、flow训练及自rollout路径。成本门槛要求透明不复现，而不是把便宜影子程序叫完整实现。",
                "教学例：取出相近相机的旧帧不等于生成未见区域或动态物体。",
                "Why not count a tiny retrieval example as reproduction?",
                "Retrieval cannot replace14B video generation, flow training and self-rollout tuning. The cost gate requires explicit non-reproduction rather than a cheap shadow.",
                "Retrieving a nearby camera frame does not generate unseen regions or dynamic objects.",
            ),
        ],
    ),
]


def write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def document(p, meta, english=False):
    title = p["title"] if english else p["cn_title"]
    aid, key, module = p["aid"], p["key"], p["module"]
    code_path = (
        f"src/auto_research/foundation_models/{module}.py"
        if module
        else ("None (not reproduced)" if english else "无（不复现）")
    )
    warning = (
        (
            f"{p['tier']} component; not a complete model"
            if module
            else "Review only; no implementation"
        )
        if english
        else (f"{p['tier']}组件；不是完整模型" if module else "仅资料收录；无实现")
    )
    link = "[简体中文](README.md)" if english else "[English](README-en.md)"
    source = f"https://arxiv.org/pdf/{aid}v1"
    labels = (
        [
            "Paper information",
            "Original paper summary",
            "Background and main changes",
            "Original paper figure",
            "Core equations",
            "Paper offline and online results",
            "Local reproduction",
            "Data protocol and code mapping",
            "Same-topic comparison and boundaries",
            "High-cost full experiment",
        ]
        if english
        else [
            "论文信息",
            "原始论文总结",
            "背景与主要改动",
            "原论文关键图",
            "核心公式",
            "论文离线与线上效果",
            "本地复现",
            "数据协议与代码映射",
            "同主题比较与边界",
            "高成本完整实验",
        ]
    )
    fields = (
        [
            "Paper link",
            "Company / institution / school",
            "Original publication date",
            "Original source code",
            "Local adapter / key",
            "Local reproduction code directory",
        ]
        if english
        else [
            "论文链接",
            "公司 / 机构 / 学校",
            "首次公开日期",
            "原作者开源代码",
            "本地 adapter / key",
            "本地复现代码目录",
        ]
    )
    lang = "en" if english else "cn"
    metadata = [
        f"[arXiv:{aid}v1](https://arxiv.org/abs/{aid}v1); [fixed PDF]({source})",
        f"{p['author']}: {p['org']} (verified fixed-v1 PDF byline)",
        f"{meta['published']} (arXiv v1); announcement2026-11-19",
        p["code_" + lang],
        f"`{key}`; `adapter: null`; not Evolve-integrated",
        f"`{code_path}`",
    ]
    if not english:
        metadata[1] = f"一作 {p['author']}：{p['org']}（已核对固定v1 PDF署名）"
        metadata[2] = (
            f"{meta['published']}（arXiv v1）；公告2026-11-19，不把PDF内日期或公告当首发日期"
        )
        metadata[4] = f"`{key}`；`adapter: null`；未接入Evolve"
    text = (
        f"# {title}\n\n{link}\n\n> **{warning}**. "
        + (
            "Full experiments: **high cost, not reproduced (review DONE)**."
            if english
            else "完整实验：**成本过高，不复现（审查 DONE）**。"
        )
        + "\n\n"
    )
    text += (
        f"## {labels[0]}\n\n| Field | Value |\n| --- | --- |\n"
        if english
        else f"## {labels[0]}\n\n| 字段 | 内容 |\n| --- | --- |\n"
    )
    text += "".join(
        f"| {label} | {value} |\n" for label, value in zip(fields, metadata, strict=True)
    )
    text += (
        f"\n## {labels[1]}\n\n### {labels[2]}\n\n"
        + p["overview_" + lang]
        + f" [Fixed-v1 source]({source}).\n\n"
    )
    text += "~~~mermaid\n" + DIAGRAMS[key] + "\n~~~\n\n"
    text += f"<!-- paper-figure:start -->\n### {labels[3]}\n\n[![{key} original paper figure](assets/paper-figure-01.png)]({source})\n\n"
    text += (
        "Original PDF crop; author method/result, not local evidence. [Page, crop and SHA256](assets/provenance.json). Copyright remains with the original authors.\n"
        if english
        else f"固定v1原始PDF裁切，是作者方法/结果，不是本地指标。[页码、裁切与SHA256](assets/provenance.json)。图片来自[原论文]({source})，版权归原作者所有。\n"
    )
    text += "<!-- paper-figure:end -->\n\n"
    text += f"### {labels[4]}\n\n$$\n{p['formula']}\n$$\n\n" + p["detail_" + lang] + "\n\n"
    text += f"### {labels[5]}\n\n" + p["results_" + lang] + "\n\n"
    text += f"## {labels[6]}\n\n### {labels[7]}\n\n" + p["local_" + lang] + "\n\n"
    if module:
        text += f"""```bash
PYTHONPATH=src python -c 'from auto_research.foundation_models.{module} import diagnostic; print(diagnostic(42))'
PYTHONPATH=src python -m pytest tests/test_nov19_latest_foundation.py -q
```

"""
        text += (
            "Local generated tensors/contract cases are diagnostics only, not public capability benchmarks. Seeds42/43/44 do not elevate the evidence tier.\n\n"
            if english
            else "本地生成小张量/接口案例仅为诊断，不是公开能力benchmark；seeds42/43/44不自动提升证据等级。\n\n"
        )
        if p["cuda"]:
            text += (
                (
                    "CUDA acceptance is recorded separately in the[sanitized GPU receipt]"
                    if english
                    else "CUDA验收以[真实GPU回执]"
                )
                + f"(../../gpu-validations/{key}-a100-20261119-latest.json)"
                + (
                    "; CPU success cannot substitute for it.\n\n"
                    if english
                    else "为准；CPU通过不能替代。\n\n"
                )
            )
    text += f"### {labels[8]}\n\n" + p["compare_" + lang] + "\n\n"
    text += f"### {labels[9]}\n\n" + p["cost_" + lang] + "\n\n"
    text += (
        "This is a configuration-based cost estimate, not a measured full-run duration. **High cost, not reproduced (review DONE)**; no large downloads, full experiments, automatic retries or implementation queue. No capability improvement or Evolve promotion is claimed.\n"
        if english
        else "以上是配置依据的成本估计，不是完整实验实测耗时。**成本过高，不复现（审查 DONE）**；不下载大资源、不启动完整实验、不自动重试、不加入自动实现队列，不声明能力提升或Evolve晋级。\n"
    )
    return text


def main():
    pool = json.loads((ROOT / ".cache/nov19-latest/metadata-pool.json").read_text())
    meta = {p["canonical_id"]: p for p in pool["papers"]}
    known = json.loads((ROOT / "docs/research-manifest.json").read_text())["papers"]
    peers = {p["domain"] + ":" + p["key"]: p["detail_path"] for p in known}
    for p in PAPERS:
        peers[p["domain"] + ":" + p["key"]] = f"{p['domain']}/{p['aid']}-{p['key']}/README.md"
    bank, translations, accepted, proposals = {}, {}, [], []
    for p in PAPERS:
        aid, key, domain = p["aid"], p["key"], p["domain"]
        identity = domain + ":" + key
        detail = f"{domain}/{aid}-{key}/README.md"
        directory = ROOT / "docs" / detail
        directory.parent.mkdir(parents=True, exist_ok=True)
        cn = document(p, meta[aid])
        directory.write_text(cn)
        source_fingerprint = sha256(cn.encode()).hexdigest()
        (directory.parent / "README-en.md").write_text(
            "<!-- source-sha256: " + source_fingerprint + " -->\n" + document(p, meta[aid], True)
        )
        paper_source = CACHE / (aid + "v1.pdf")
        cost = {
            "source": f"https://arxiv.org/pdf/{aid}v1; " + ", ".join(p["sections"]),
            "available_resource": "one A100 or A30, or local Mac",
            "paper_configuration": p["cost_cn"],
            "model_scale": p["cost_en"],
            "estimated_cost_basis": "Configuration-based; no full-experiment time measured and no costly probe.",
            "decision": "成本过高，不复现（审查 DONE）；"
            + ("仅本地低成本组件验收" if p["module"] else "仅资料收录，无实现"),
        }
        spec = {
            "domain": domain,
            "key": key,
            "title": p["title"],
            "paper_url": f"https://arxiv.org/abs/{aid}v1",
            "reviewed_version_url": f"https://arxiv.org/pdf/{aid}v1",
            "reviewed_version": "v1",
            "published": meta[aid]["published"][:10],
            "published_at": meta[aid]["published"],
            "announced_on": DATE,
            "detail_path": detail,
            "topic": p["topic"],
            "first_author": p["author"],
            "first_author_affiliation": p["org"],
            "affiliation_evidence": "Fixed v1 PDF first-author affiliation; HTML byline cross-checked against PDF.",
            "verified_priority_organizations": ["Meta"]
            if key == "autoregressive-view-model"
            else [],
            "code": p["code"],
            "code_status": p["code_cn"],
            "code_license": "MIT" if p["code"] else "未找到可核验的原作者方法源码许可证",
            "upstream_revision": p["revision"],
            "method_source_sha256": sha256(paper_source.read_bytes()).hexdigest(),
            "adapter": None,
            "priority": p["priority"],
            "intake_class": "newly_announced",
            "implementation_status": "component_only" if p["module"] else "deferred_high_cost",
            "evaluation_tier": p["tier"],
            "diagnostic_only": True,
            "promotion_eligible": False,
            "evolve_integrated": False,
            "local_operator": "auto_research.foundation_models." + p["module"] + ".diagnostic"
            if p["module"]
            else None,
            "local_command": f"PYTHONPATH=src python -c 'from auto_research.foundation_models.{p['module']} import diagnostic; print(diagnostic(42))'"
            if p["module"]
            else None,
            "requires_gpu_validation": p["cuda"],
            "gpu_validation_passed": False,
            "gpu_validation_artifact": f"docs/gpu-validations/{key}-a100-20261119-latest.json"
            if p["cuda"]
            else None,
            "full_experiment_status": "not_reproduced_high_cost",
            "full_experiment_review_done": True,
            "review_done": True,
            "review_resolution": "not_reproduced_high_cost",
            "automatic_retry": False,
            "automatic_implementation_queue": False,
            "cost_assessment": cost,
            "summary": p["overview_cn"] + " " + p["local_cn"],
        }
        if not p["module"]:
            spec["deferral_reason"] = p["cost_cn"] + " 成本过高，不复现（审查 DONE）。"
        write(ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json", spec)
        accepted.append(
            {
                "arxiv_id": aid,
                "key": key,
                "domain": domain,
                "identity": identity,
                "title": p["title"],
                "first_author": p["author"],
                "first_author_affiliation": p["org"],
                "priority": p["priority"],
                "first_published_at": meta[aid]["published"],
                "announced_on": DATE,
                "reviewed_version": "v1",
                "reviewed_source_url": spec["reviewed_version_url"],
                "source_sha256": spec["method_source_sha256"],
                "sections_read": p["sections"],
                "implementation_status": spec["implementation_status"],
                "evaluation_tier": p["tier"],
                "scope": p["local_en"],
                "cost_basis": p["cost_en"],
                "component_budget": "Generated tiny tensors or CPU scheduling interface; zero model/data downloads; expected seconds, not measured full campaign.",
                "requires_gpu_validation": p["cuda"],
                "gpu_validation_passed": False,
                "local_detail_path": detail,
                "code_url": p["code"],
                "code_verification": p["code_en"],
                "upstream_revision": p["revision"],
                "review_done": True,
                "review_resolution": "not_reproduced_high_cost",
                "full_experiment_status": "not_reproduced_high_cost",
                "full_experiment_review_done": True,
                "automatic_retry": False,
                "automatic_implementation_queue": False,
            }
        )
        questions, english = [], {}
        source_sections = [
            "背景与主要改动",
            "核心公式",
            "同主题比较与边界",
            "数据协议与代码映射",
            "高成本完整实验",
        ]
        for qid, level, q, a, example, eq, ea, ee in p["qa"]:
            questions.append(
                {
                    "id": qid,
                    "level": level,
                    "question": q,
                    "answer": a,
                    "example": example,
                    "source_sections": source_sections,
                    "added": DATE,
                }
            )
            english[qid] = {"question": eq, "answer": ea, "example": ee}
        bank[identity] = {"questions": questions}
        units = question_units({identity: questions})
        for q in questions:
            uid = f"qa/{identity}/{q['id']}"
            translations[uid] = {
                "source_sha256": units[uid].source_sha256,
                "reviewed": True,
                "fields": english[q["id"]],
            }
        pair = [identity, p["peer"]]
        revisions = {
            pid: sha256((ROOT / "docs" / peers[pid]).read_bytes()).hexdigest()
            for pid in pair
            if (ROOT / "docs" / peers[pid]).exists()
        }
        q = questions[2]
        proposals.append(
            {
                "paper": identity,
                "target_card": p["card"],
                "source_revisions": revisions,
                "comparison": {
                    "position": p["overview_cn"],
                    "tradeoff": p["compare_cn"],
                    "sections": ["背景与主要改动", "核心公式", "同主题比较与边界"],
                },
                "analysis": {
                    "title": p["cn_title"],
                    "body": p["compare_cn"] + " " + p["detail_cn"],
                    "papers": pair,
                },
                "question": {
                    "id": "nov19-" + key,
                    "question": q["question"],
                    "answer": q["answer"],
                    "example": q["example"],
                    "papers": pair,
                },
                "update": {
                    "date": DATE,
                    "papers": pair,
                    "summary": p["compare_cn"] + " 本地组件合同和高成本不复现分别记录。",
                },
                "english": {
                    "comparison": {"position": p["overview_en"], "tradeoff": p["compare_en"]},
                    "analysis": {
                        "title": p["title"],
                        "body": p["compare_en"] + " " + p["detail_en"],
                    },
                    "question": english[q["id"]],
                    "update": p["compare_en"]
                    + " Local contracts and high-cost non-reproduction remain separate.",
                },
            }
        )
    write(
        ROOT / "docs/learning/questions/nov19-latest-foundation.json",
        {"schema_version": 1, "papers": bank},
    )
    write(
        ROOT / "docs/en/learning/translations/qa-nov19-latest-foundation.json",
        {"schema_version": 1, "units": translations},
    )
    write(
        AUDIT / "deep-dive-proposals-foundation.json",
        {
            "schema_version": 1,
            "reviewed_on": DATE,
            "integration_owner": "root",
            "proposals": proposals,
        },
    )
    write(
        AUDIT / "foundation-review.json",
        {
            "schema_version": 1,
            "reviewed_on": DATE,
            "requested_window": ["2026-11-18", DATE],
            "scope": "Finite high-value foundation/multimodal/JEPA selection from shared metadata and Nov19 official announcements; not full-text review of the entire metadata pool.",
            "preflight_before_implementation": True,
            "available_resource": "one A100 or A30, or local Mac",
            "large_downloads_authorized_or_needed": False,
            "watermark_change_claimed": False,
            "accepted": accepted,
            "selection_notes": [
                "AVM was first submitted2026-11-17T19:20:06Z and newly announced Nov19; original publication and announcement remain separate.",
                "CWM first-author PDF byline is Brown University / AMI Labs, not Meta. Familiar author history is not affiliation proof.",
                "CWM and AVM official links returned404; methods were checked against fixed PDFs, not treated as available source implementations.",
                "On-policy Morphing is owned by the post-training reviewer; recommendation candidates are owned by root.",
            ],
        },
    )
    print(
        "Authored5papers,4components,20reviewed bilingual questions; no global catalogs/ledger touched."
    )


if __name__ == "__main__":
    main()
