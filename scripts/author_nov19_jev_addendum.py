"""Authored JEV/JEPA addendum; preserve the five previously delivered papers."""

from hashlib import sha256
import json
from pathlib import Path
import fitz

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov19-latest/foundation"
AUDIT = ROOT / "docs/research-audits/nov19-latest"
DATE = "2026-11-19"

PAPERS = [
    dict(
        aid="2611.24738",
        key="jeveration",
        domain="system-one",
        title="Jeveration: System One Models Now Generate",
        cn_title="Jeveration：以共享随机状态协调一次前向图像决策",
        author="Yuhe Liu",
        org="National University of Singapore",
        topic=["类型化决策", "联合图像生成"],
        card="system-one/typed-readout",
        peer="foundation-models:llm2jev",
        module=None,
        page=4,
        crop=(54, 42, 559, 268),
        figure="Figure3: Architecture overview",
        overview_cn="把图像表示为128个离散code的联合Choice，所有位置共享随机状态，而不是把各位置的边缘分布独立采样。冻结Qwen3.5-4B配共享LoRA与任务head，先学masked图像分布，再以distribution matching和置信纠正训练单步决策；同一checkpoint还做图到图与dense prediction。",
        overview_en="Images become a joint Choice over128 discrete codes. A shared random state coordinates positions rather than independently sampling marginal codes. A frozen Qwen3.5-4B with shared LoRA/heads first learns masked image conditionals, then distribution matching and confidence correction teach single-pass decisions. One checkpoint also serves image-to-image and dense tasks.",
        formula=r"q_\theta(c\mid y)=\mathbb E_{\xi\sim p_0}\prod_{i=1}^{N}q_{\theta,i}(c_i\mid y,\xi),\qquad \mathcal L_{gen}=\mathcal L_{DM}+\lambda\mathcal L_{corr}.",
        details_cn="给定共享xi后可并行选择，但对xi求混合后各位置不再必须独立。仅添加随机噪声不够：原文指出直接监督可忽略该状态。纠正target在训练时重mask最低置信的一半位置，由冻结的第一阶段模型补全；推理仍是一次生成前向，不是把训练辅助步骤算成免费。",
        details_en="Choices factorize conditionally on shared xi, but mixing over xi permits dependence. Noise alone is insufficient: direct supervision can ignore it. Training correction re-masks the least-confident half and uses the frozen first-stage model to complete them; inference remains one generation pass.",
        results_cn="论文报告512px、GenEval0.74、单H200端到端77.8ms；122.2倍是相对表内较慢的Janus-Pro-7B，不能当成对所有方法的加速。不同分辨率/模型规模也需区分。未报告生产线上A/B；没有本地图像质量或延迟测量。",
        results_en="The paper reports512px, GenEval0.74 and77.8ms end-to-end on one H200. The122.2x ratio is relative to the listed Janus-Pro-7B, not every method; resolutions and sizes differ. No production A/B or local image-quality/latency measurement is claimed.",
        local_cn="仅资料收录，无模型、head、训练、生成或指标文件。不能用几个共享随机数加线性层假装得到论文的联合图像生成。",
        local_en="Review only: no model, head, training, image generation or metrics. Shared random numbers plus a linear fixture would not reproduce the learned joint generator.",
        compare_cn="LLM2Jev把候选标签读成有限决策分布；Jeveration还必须协调空间上众多输出，并学会使用共同随机状态。单选候选打分成功，不证明整图联合分布或图像质量。",
        compare_en="LLM2Jev reads a finite candidate decision distribution. Jeveration must also coordinate spatial outputs and learn to use shared randomness. Candidate scoring alone does not establish a coherent joint image distribution.",
        cost_cn="原文§4.1和补充§4：冻结4B骨干，约1B可训练参数；92k第一阶段+6.7k第二阶段，四张RTX PRO6000约4天，另有百万级图像和多任务评测。按已有论文测量已明显超单A100/A30/Mac短预算，不试训、不下载。",
        cost_en="Section4.1 and supplementary4 report a frozen4B backbone, about1B trainable parameters,92k+6.7k updates and around four days on four RTX PRO6000 GPUs, plus million-scale images and multitask evaluation. This reported cost exceeds one A100/A30 or Mac short-run budget; no probe/download is attempted.",
        diagram="flowchart LR\n Y[Prompt or source image] --> V[Frozen VLM plus shared LoRA]\n X[Shared random state] --> V\n V --> C[Parallel image code Choices]\n C --> D[Image decoder]\n V --> M[Dense task heads]\n T[Masked conditionals and correction training] --> V",
        qa=[
            (
                "why-shared-randomness",
                "basics",
                "为什么逐位置独立采样容易不协调？",
                "各位置可能选择不同有效图像的局部模式；共享随机状态让它们在同一实现条件下决定，再形成联合混合分布。",
                "教学例：左半边选择白天、右半边选择夜晚都是合理边缘，却不是同一场景。",
                "Why can independent position samples be incoherent?",
                "Positions can select parts of different valid images. Shared randomness coordinates one realization before mixing over realizations.",
                "Day on the left and night on the right can be valid marginals but an incoherent whole.",
            ),
            (
                "training-not-noise-only",
                "mechanism",
                "只把所有位置加同一随机输入是否足够？",
                "不够。模型可忽略随机状态；原文先学习masked分布，再做distribution matching与纠正监督来教会它使用状态。",
                "教学例：输出恒定图片也可完全忽略随机数，形式上有xi但没有多样性。",
                "Is adding shared randomness sufficient?",
                "No. The model may ignore it; masked-distribution learning and subsequent matching/correction teach its use.",
                "A constant image can ignore xi despite receiving random input.",
            ),
            (
                "choice-versus-image",
                "comparison",
                "与LLM2Jev有限候选Choice多了什么困难？",
                "整图有多个位置，既要符合提示又要跨位置协调；单个候选softmax没有学习空间联合分布的负担。",
                "教学例：选一张现成图片与生成128个相互一致的code不是同一任务。",
                "What is harder than an LLM2Jev candidate Choice?",
                "Multiple spatial decisions must jointly match a prompt. A single candidate softmax need not learn that spatial joint law.",
                "Choosing an existing image differs from generating128 mutually coherent codes.",
            ),
            (
                "not-head-fixture",
                "implementation",
                "为什么这次不实现一个随机head就算完成？",
                "核心是经过两阶段训练的联合图像分布和解码链路，廉价head fixture不能替代。完整实验成本已由原文四卡四天证明。",
                "教学例：随机输出128个token无法验证GenEval或77.8ms端到端结果。",
                "Why not count a random output head as reproduction?",
                "The learned two-stage joint distribution and decoder are defining components. A cheap head fixture cannot replace them.",
                "Random128-token outputs verify neither GenEval nor the77.8ms result.",
            ),
        ],
    ),
    dict(
        aid="2611.24616",
        key="egojev",
        domain="system-one",
        title="EgoJev: Finding Evidence in Egocentric Video by Reading VLM Decisions",
        cn_title="EgoJev：以决策分布几何融合与分位数分配视频帧",
        author="Chunggi Lee",
        org="Harvard University",
        topic=["类型化决策", "视频证据与帧预算"],
        card="system-one/typed-readout",
        peer="multimodal-models:system-one-rerank",
        module="egojev_components",
        page=4,
        crop=(54, 42, 559, 280),
        figure="Figure2: EgoJev coarse-to-fine readout and answer frames",
        overview_cn="同一冻结VLM把带数字标签的候选缩略图放在一个prompt中，读取完整标签的条件概率而不是生成时间文本。粗分布决定细看窗口，细分布先保留窗口粗概率总量，再与对应粗分布做几何平均。最后在时间的分段均匀分布上取中点分位数，分配有限回答帧。",
        overview_en="One frozen VLM compares labeled thumbnails in one prompt. Complete label probabilities replace written timestamps. Coarse mass selects refinement windows; local fine readouts retain their window mass and are geometrically fused with coarse probabilities. Midpoint quantiles of a piecewise-uniform time distribution allocate answer frames.",
        formula=r"P_s^\star\propto\sqrt{P^c_{j(s)}P_s^f},\qquad t_b=F^{-1}\left(\frac{b-1/2}{B}\right),\quad b=1,\ldots,B.",
        details_cn="细读窗口的局部分布归一后乘该窗口的粗概率总量；未细读窗口均摊其窗口质量。平方根不同于普通乘积，后者过度锐化。k=0直接保留单层粗分布。分位数需在bin内插值而不是一律取bin中心。标签如17]可能多token，完整读出需逐条件概率相乘并含终止]，本地不实现这部分。",
        details_en="Normalize each refined local distribution, then multiply by its coarse window mass; unrefined windows spread that mass evenly. A square root is not a plain product. For k0, keep the single-level coarse distribution. Inverse-CDF placement interpolates within bins. Full labels such as17] require all conditional token probabilities, including the closing bracket; that VLM readout is not implemented locally.",
        results_cn="原文QAEgo4D准确率从uniform51.2%到62.0%，每题26.7秒为A100 MIG切片上的50题平均。本文组件没有读视频、VLM或答案，不能报告上述准确率。未报告生产线上A/B。",
        results_en="The paper reports QAEgo4D accuracy51.2% uniform versus62.0% EgoJev and26.7s/question averaged over50 cases on an A100 MIG slice. Local postprocessing reads no videos, VLMs or answers and does not reproduce that accuracy. No production A/B is reported.",
        local_cn="CPU组件仅接受显式给定的候选概率，执行窗口质量/稳定top-k、细层质量缩放、几何融合和分段均匀逆CDF。输入不含gold证据或答案；未实现VLM标签打分、tokenizer、图像预填缓存、label permutation检查、视频解码或回答模型。诊断概率是合成算例，不是VLM能力证据；L1只指后处理机制。",
        local_en="The CPU component consumes explicit candidate probabilities and implements window masses/stable top-k, fine-mass scaling, geometric fusion and piecewise-uniform inverse CDF. There are no gold inputs, VLM/tokenizer calls, visual prefill cache, permutation-label check, video decoding or answering model. Synthetic diagnostic probabilities establish only L1 postprocessing, not VLM capability.",
        compare_cn="System One多模态重排把一个联合候选分布用于排序；EgoJev将分布用于时间预算分配。前者单token字母读出不能不加检查地替代后者多token数字标签概率，frame quantile也不是单纯top-k帧。",
        compare_en="System One reranking sorts a joint candidate distribution. EgoJev uses it to allocate time budget. Single-token letter readout cannot silently replace multi-token numeric labels, and quantile frames are not simply the top-k frames.",
        cost_cn="完整矩阵含500题QAEgo4D、996题MyEgo、500题EgoSchema、四个VLM与多基线/消融。按原文26.7秒/题估算仅500题约3.7小时（不是本机实测；其他任务耗时不同），再含长视频和模型资源。完整实验高成本不复现；本地只跑秒级CPU概率算子，无权重/视频下载。",
        cost_en="The full matrix has500QAEgo4D,996MyEgo and500EgoSchema questions, four VLMs and baseline/ablation runs. At the paper’s26.7s/question,500cases alone imply about3.7hours, an estimate rather than a local measurement and not a timing estimate for other tasks. Full experiments are not reproduced; only tiny CPU probability cases run without weights/videos.",
        diagram="flowchart LR\n C[Explicit coarse probabilities] --> W[Window mass and top k]\n F[Explicit refined probabilities] --> S[Preserve coarse window mass]\n W --> S\n S --> G[Geometric coarse fine fusion]\n G --> Q[Piecewise uniform inverse CDF]\n Q --> T[Answer frame times only]",
        qa=[
            (
                "distribution-not-score",
                "basics",
                "为什么候选分布而不只一个最优帧有用？",
                "分布同时表示多个可能证据位置，能让回答帧在确信处集中、不确定处展开；单个argmax会丢掉预算分配信息。",
                "教学例：两个窗口各占50%时，8帧应覆盖两边，而非全堆在一个并列最优点。",
                "Why retain a distribution rather than one best frame?",
                "It allocates frames across plausible evidence: concentrate when certain, spread when uncertain. Argmax loses that information.",
                "With two windows of50% mass, eight frames should cover both.",
            ),
            (
                "geometric-mass",
                "mechanism",
                "细读概率能直接与粗概率相乘吗？",
                "先归一每个细读窗口并乘其粗总质量，再做平方根几何融合和全局归一。普通乘积会比原式更尖锐，未细读窗口也不能丢掉。",
                "教学例：一个窗口仅有20%粗质量，即使内部最高概率为1，也不应先变成全视频100%。",
                "May fine probabilities be multiplied directly?",
                "Normalize locally, restore coarse window mass, then apply square-root fusion and global normalization. Plain multiplication sharpens differently and unrefined windows retain mass.",
                "A window with20% coarse mass must not become100% globally just because its local maximum is1.",
            ),
            (
                "ranking-versus-quantiles",
                "comparison",
                "与System One多模态重排的候选排序有何不同？",
                "这里用分布的逆CDF选择时间中点分位数，而不是按概率取top-k；分位数可能在同一高质量bin内取多个不同时间。",
                "教学例：后半段概率为1、总时长10秒、预算2时为6.25和8.75秒，不是两个7.5秒。",
                "How does this differ from System One reranking?",
                "It uses inverse-CDF midpoint quantiles, not probability top-k. Multiple distinct times may lie inside one high-mass segment.",
                "With all mass in the last half of10seconds and budget2, times are6.25 and8.75, not two7.5s.",
            ),
            (
                "probabilities-not-vlm-evidence",
                "implementation",
                "CPU后处理通过为什么不能宣称62%准确率？",
                "给定概率并未验证VLM是否找到正确证据；完整方法还需多token标签读出、真实视频与回答评测。合成输入不冒充模型分数。",
                "教学例：手工把证据窗口设为概率1，只能测试分位数公式，不能测试证据识别。",
                "Why does CPU parity not establish62% accuracy?",
                "Given probabilities do not establish that a VLM found evidence. Full evaluation needs multi-token labels, real videos and answers; synthetic inputs are not model scores.",
                "Manually assigning evidence mass1 tests placement arithmetic, not evidence recognition.",
            ),
        ],
    ),
    dict(
        aid="2611.24062",
        key="jepa-dots",
        domain="multimodal-models",
        title="JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control",
        cn_title="JEPA Dots：隔离语言任务表征与固定动作下的动力学预测",
        author="Xianhao Pan",
        org="Z Robotics",
        topic=["世界模型", "任务与动力学分离"],
        card="multimodal-models/world-state-actions",
        peer="foundation-models:lewam",
        module=None,
        page=2,
        crop=(54, 43, 559, 388),
        figure="Figure1: Dynamics/task separation and masked world-action modeling",
        overview_cn="共享视觉骨干之后拆动力学和任务两条latent路径，语言FiLM只进入任务路径。world query只读动力学历史和给定clean动作，policy读历史、goal和noisy动作；多层mask同时阻断间接泄漏。固定参数、观测和给定动作时，换指令不能改变world预测，但policy可以生成不同动作。",
        overview_en="A shared visual backbone feeds separate dynamics and task latents; language FiLM enters only the task path. World queries read dynamics history and supplied clean actions; the policy reads history, goals and noisy actions. Multi-layer masks also block indirect leakage. Fixed observations/actions/parameters yield instruction-invariant world predictions while policy actions may change.",
        formula=r"\widetilde F(\ell)=F+\gamma(e_\ell)\odot F+\beta(e_\ell),\quad\hat Z(H,A;\ell_1)=\hat Z(H,A;\ell_2),\qquad\mathcal L=\mathcal L_{act}+\mathcal L_{world}+0.04\mathcal L_{sub}.",
        details_cn="不变性约束的是forward信息通路，不是说共享骨干训练后两种latent统计独立。world预测分支只在训练监督中使用，部署是action flow生成8动作、执行前2个后重规划，不是用world model在线搜索动作。",
        details_en="The invariance is a forward-conditioning property, not statistical independence after joint backbone training. The world branch supplies training supervision; deployment generates eight actions by action flow and executes the first two before replanning, rather than searching actions through the world model.",
        results_cn="原文reference实验40个已训练LIBERO任务总体84.9%，对照task-ID适配76.0%。NanoVLA-S等外部发表成绩使用不同protocol，不可当严格同预算胜出。未报告生产线上A/B，本轮没有机器人成功率测量。",
        results_en="The reference experiment reports84.9% over40 trained LIBERO tasks versus76.0% for its task-ID adaptation baseline. Published NanoVLA-S comparisons use different protocols, not a controlled matched-budget win. No production A/B or local robot-success measurement is claimed.",
        local_cn="仅资料、公式、机构及成本收录，无operator、训练、LIBERO安装、机器人执行、metrics或GPU回执。不得用一个语言无关函数的恒等式fixture冒充完整双latent控制模型。",
        local_en="Review-only method, equations, affiliation and cost. There is no operator, training, LIBERO installation, robot run, metrics or GPU receipt. A trivially language-free function would not reproduce the dual-latent controller.",
        compare_cn="LeWAM联合world/action并用预测模型规划；JEPA Dots强调语言目标与动力学给定动作输入的隔离，部署world分支不参与动作搜索。相同masked-MoT背景不代表推理链相同。",
        compare_en="LeWAM jointly models worlds/actions and plans through prediction. JEPA Dots separates language goals from fixed-action dynamics and does not use its world branch for deployment action search. Shared masked-MoT ancestry does not imply identical inference.",
        cost_cn="39.1M参数含冻结句子encoder，训练60epochs约15k更新；40任务每模型4000闭环episode、每episode最多600步，三run消融每variant12000episode。小参数量不代表低完整实验成本；单A100/A30/Mac本轮不下载LIBERO、不试训或运行长闭环。",
        cost_en="The39.1M total includes a frozen sentence encoder. Training uses60epochs/about15k updates;40tasks require4000closed-loop episodes/model, up to600steps each, and three-run ablations use12000episodes/variant. Small parameter count does not make this campaign cheap. No LIBERO download, training probe or long control run is attempted.",
        diagram="flowchart LR\n O[Observations] --> B[Shared visual backbone]\n B --> D[Dynamics latent]\n B --> T[Task latent with language FiLM]\n L[Instruction] --> T\n D --> W[World branch with clean supplied actions]\n D --> P[Flow policy]\n T --> P\n P --> A[Execute first two of eight actions]\n W --> S[Training supervision only]",
        qa=[
            (
                "conditioning-separation",
                "basics",
                "为什么相同观测和动作下world预测不该因语言改变？",
                "语言描述的是任务目标，不应改变这些已固定动作的物理后果；因此语言只进入task/policy而非world动力学通路。",
                "教学例：同样向左移动夹爪，指令改成拿杯子不应让固定动作的预测位移突然向右。",
                "Why keep fixed-action world predictions invariant to language?",
                "Instructions specify goals, not different physics for identical observations/actions, so language enters task/policy paths rather than world dynamics.",
                "The same leftward command should not predict rightward motion merely because the goal becomes picking a cup.",
            ),
            (
                "mask-not-statistical-independence",
                "mechanism",
                "隔离goal token是否足以防止泄漏？",
                "还需限制中间token的多层信息通路；只在最后一层屏蔽直接goal边，不保证前层信息没进入world可见token。",
                "教学例：history token先读goal，再被world读到，会产生间接语言通道。",
                "Is directly hiding goal tokens sufficient?",
                "Intermediate multi-layer paths must also be restricted. A final-layer direct mask cannot undo earlier goal information in visible tokens.",
                "A history token that first reads goals can leak them when later read by the world branch.",
            ),
            (
                "lewam-deployment",
                "comparison",
                "与LeWAM的world-action联学相比，部署差异是什么？",
                "JEPA Dots world分支只供训练监督，部署执行flow policy；不能因此说它已复现LeWAM通过world模型优化动作的规划链。",
                "教学例：生成8步动作后执行2步再观测，是receding-horizon policy，不等于对world cost做梯度规划。",
                "How does deployment differ from LeWAM?",
                "The JEPA Dots world branch is training supervision, while deployment uses a flow policy, not LeWAM-style world-model action optimization.",
                "Executing two actions from an eight-step chunk is receding-horizon control, not gradient planning over a world cost.",
            ),
            (
                "small-model-expensive-eval",
                "implementation",
                "39.1M参数为何仍不跑完整实验？",
                "成本主要还来自多个训练run和40任务的数千闭环episode；参数少不能抵消环境模拟与评测矩阵。",
                "教学例：4000episode各最多600步，单模型上限即240万环境步，尚未算三run消融。",
                "Why defer a39.1M model’s full experiment?",
                "Multiple training runs and thousands of closed-loop episodes across40tasks remain costly despite small weights.",
                "4000episodes times up to600steps gives2.4million environment steps/model before three-run ablations.",
            ),
        ],
    ),
]


def dump(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def render(p, metadata, english=False):
    lang = "en" if english else "cn"
    aid, key = p["aid"], p["key"]
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
    title = p["title"] if english else p["cn_title"]
    text = (
        f"# {title}\n\n"
        + ("[简体中文](README.md)" if english else "[English](README-en.md)")
        + "\n\n"
    )
    status = (
        (
            "L1 CPU postprocessing only; no VLM capability evidence"
            if p["module"]
            else "Review only; no implementation"
        )
        if english
        else ("仅L1 CPU后处理；无VLM能力证据" if p["module"] else "仅资料收录；无实现")
    )
    text += (
        f"> **{status}**. "
        + (
            "Full experiments: **high cost, not reproduced (review DONE)**."
            if english
            else "完整实验：**成本过高，不复现（审查 DONE）**。"
        )
        + "\n\n"
    )
    text += (
        f"## {labels[0]}\n\n| "
        + ("Field | Value" if english else "字段 | 内容")
        + " |\n| --- | --- |\n"
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
    values = [
        f"[arXiv:{aid}v1](https://arxiv.org/abs/{aid}v1); [fixed PDF](https://arxiv.org/pdf/{aid}v1)",
        f"{p['author']}: {p['org']} (fixed-v1 PDF byline)",
        f"{metadata['published']} (arXiv v1); announcement2026-11-19",
        "No author method source or license verified in fixed v1; dependencies are not a method release."
        if english
        else "固定v1未找到可核验的原作者方法源码/许可证；依赖仓库不算本方法开源。",
        f"`{key}`; `adapter: null`; not Evolve-integrated"
        if english
        else f"`{key}`；`adapter: null`；未接入Evolve",
        (
            "`src/auto_research/system_one/egojev_components.py`"
            if p["module"]
            else ("None (not reproduced)" if english else "无（不复现）")
        ),
    ]
    text += "".join(f"| {k} | {v} |\n" for k, v in zip(fields, values, strict=True))
    text += f"\n## {labels[1]}\n\n### {labels[2]}\n\n" + p["overview_" + lang] + "\n\n"
    text += "~~~mermaid\n" + p["diagram"] + "\n~~~\n\n"
    text += f"<!-- paper-figure:start -->\n### {labels[3]}\n\n[![{key} original paper figure](assets/paper-figure-01.png)](https://arxiv.org/pdf/{aid}v1)\n\n"
    text += (
        "Original PDF crop, no semantic edits; author method, not local evidence. [Page, crop and SHA256](assets/provenance.json). Copyright retained by the original authors.\n"
        if english
        else f"固定v1原始PDF裁切，未修改科学内容；是作者方法，不是本地证据。[页码、裁切与SHA256](assets/provenance.json)。图片来自[原论文](https://arxiv.org/pdf/{aid}v1)，版权归原作者所有。\n"
    )
    text += "<!-- paper-figure:end -->\n\n"
    text += f"### {labels[4]}\n\n$$\n" + p["formula"] + "\n$$\n\n" + p["details_" + lang] + "\n\n"
    text += f"### {labels[5]}\n\n" + p["results_" + lang] + "\n\n"
    text += f"## {labels[6]}\n\n### {labels[7]}\n\n" + p["local_" + lang] + "\n\n"
    if p["module"]:
        text += "```bash\nPYTHONPATH=src python -c 'from auto_research.system_one.egojev_components import diagnostic; print(diagnostic(42))'\nPYTHONPATH=src python -m pytest tests/test_nov19_jev_addendum.py -q\n```\n\n"
        text += (
            "[Canonical CPU component evidence](metrics/component-cpu-seeds42-44.json); independent frozen-source execution, not a video benchmark.\n\n"
            if english
            else "[规范CPU组件证据](metrics/component-cpu-seeds42-44.json)；独立冻结源码执行，不是视频benchmark。\n\n"
        )
    text += f"### {labels[8]}\n\n" + p["compare_" + lang] + "\n\n"
    text += f"### {labels[9]}\n\n" + p["cost_" + lang] + "\n\n"
    text += (
        "**High cost, not reproduced (review DONE)**. No full experiment, large download, automatic retry or implementation queue; no capability promotion.\n"
        if english
        else "**成本过高，不复现（审查 DONE）**；不启动完整实验、不下载大资源、不自动重试、不进入自动实现队列，不作能力晋级。\n"
    )
    return text


def main():
    metadata = {
        p["canonical_id"]: p
        for p in json.loads((ROOT / ".cache/nov19-latest/metadata-pool.json").read_text())["papers"]
    }
    manifest = json.loads((ROOT / "docs/research-manifest.json").read_text())["papers"]
    details = {p["domain"] + ":" + p["key"]: p["detail_path"] for p in manifest}
    qpath = ROOT / "docs/learning/questions/nov19-latest-foundation.json"
    epath = ROOT / "docs/en/learning/translations/qa-nov19-latest-foundation.json"
    ppath = AUDIT / "deep-dive-proposals-foundation.json"
    rpath = AUDIT / "foundation-review.json"
    bank, english, proposals, review = [
        json.loads(p.read_text()) for p in (qpath, epath, ppath, rpath)
    ]
    identities = {p["domain"] + ":" + p["key"] for p in PAPERS}
    proposals["proposals"] = [p for p in proposals["proposals"] if p["paper"] not in identities]
    review["accepted"] = [p for p in review["accepted"] if p["identity"] not in identities]
    for p in PAPERS:
        aid, key, domain = p["aid"], p["key"], p["domain"]
        identity = domain + ":" + key
        relative = f"{domain}/{aid}-{key}/README.md"
        details[identity] = relative
        path = ROOT / "docs" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        cn = render(p, metadata[aid])
        path.write_text(cn)
        digest = sha256(cn.encode()).hexdigest()
        (path.parent / "README-en.md").write_text(
            "<!-- source-sha256: " + digest + " -->\n" + render(p, metadata[aid], True)
        )
        pdf = CACHE / (aid + "v1.pdf")
        doc = fitz.open(pdf)
        page = doc[p["page"] - 1]
        page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).save(CACHE / (aid + "-addendum-preview.png"))
        assets = path.parent / "assets"
        assets.mkdir(exist_ok=True)
        figure = assets / "paper-figure-01.png"
        page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(p["crop"])).save(figure)
        source_sha = sha256(pdf.read_bytes()).hexdigest()
        dump(
            assets / "provenance.json",
            {
                "source_url": f"https://arxiv.org/pdf/{aid}v1",
                "paper_url": f"https://arxiv.org/abs/{aid}v1",
                "reviewed_version": "v1",
                "retrieved_on": DATE,
                "page": p["page"],
                "crop_box_pdf_points": p["crop"],
                "caption": p["figure"],
                "source_pdf_sha256": source_sha,
                "asset_sha256": sha256(figure.read_bytes()).hexdigest(),
                "extraction": "Original PDF crop; no semantic edits",
                "copyright": "Copyright retained by original authors; research commentary, not local evidence.",
            },
        )
        cost = {
            "source": f"https://arxiv.org/html/{aid}v1",
            "available_resource": "one A100 or A30, or local Mac",
            "paper_configuration": p["cost_cn"],
            "model_scale": p["cost_en"],
            "estimated_cost_basis": "Paper configuration and reported timings, not local full-run measurements.",
            "decision": "成本过高，不复现（审查 DONE）；"
            + ("仅CPU概率后处理组件" if p["module"] else "仅资料收录，无实现"),
        }
        spec = {
            "domain": domain,
            "key": key,
            "title": p["title"],
            "paper_url": f"https://arxiv.org/abs/{aid}v1",
            "reviewed_version_url": f"https://arxiv.org/pdf/{aid}v1",
            "reviewed_version": "v1",
            "published": metadata[aid]["published"][:10],
            "published_at": metadata[aid]["published"],
            "announced_on": DATE,
            "detail_path": relative,
            "topic": p["topic"],
            "first_author": p["author"],
            "first_author_affiliation": p["org"],
            "verified_priority_organizations": [],
            "affiliation_evidence": "Fixed-v1 PDF first-author byline; no affiliation inferred from models/citations.",
            "code": None,
            "code_status": "固定v1未找到可核验原作者方法源码；依赖不算方法开源。",
            "code_license": "未找到可核验方法源码许可证",
            "upstream_revision": None,
            "method_source_sha256": source_sha,
            "adapter": None,
            "priority": "P1",
            "intake_class": "newly_announced",
            "implementation_status": "component_only" if p["module"] else "deferred_high_cost",
            "evaluation_tier": "l1_mechanism" if p["module"] else "review_only",
            "diagnostic_only": True,
            "promotion_eligible": False,
            "evolve_integrated": False,
            "local_operator": "auto_research.system_one.egojev_components.diagnostic"
            if p["module"]
            else None,
            "local_command": "PYTHONPATH=src python -c 'from auto_research.system_one.egojev_components import diagnostic; print(diagnostic(42))'"
            if p["module"]
            else None,
            "requires_gpu_validation": False,
            "gpu_validation_passed": False,
            "gpu_validation_artifact": None,
            "review_done": True,
            "review_resolution": "not_reproduced_high_cost",
            "full_experiment_status": "not_reproduced_high_cost",
            "full_experiment_review_done": True,
            "automatic_retry": False,
            "automatic_implementation_queue": False,
            "cost_assessment": cost,
            "summary": p["overview_cn"] + " " + p["local_cn"],
        }
        if not p["module"]:
            spec["deferral_reason"] = p["cost_cn"] + " 成本过高，不复现（审查 DONE）。"
        dump(ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json", spec)
        review["accepted"].append(
            {
                "arxiv_id": aid,
                "key": key,
                "domain": domain,
                "identity": identity,
                "title": p["title"],
                "priority": "P1",
                "first_author": p["author"],
                "first_author_affiliation": p["org"],
                "first_published_at": metadata[aid]["published"],
                "announced_on": DATE,
                "reviewed_version": "v1",
                "reviewed_source_url": spec["reviewed_version_url"],
                "source_sha256": source_sha,
                "sections_read": ["3", "4.1", "supplementary implementation/evaluation"],
                "implementation_status": spec["implementation_status"],
                "evaluation_tier": spec["evaluation_tier"],
                "scope": p["local_en"],
                "cost_basis": p["cost_en"],
                "component_budget": "CPU only, tiny supplied probability vectors, zero VLM/video/gold inputs"
                if p["module"]
                else "No implementation",
                "requires_gpu_validation": False,
                "gpu_validation_passed": False,
                "local_detail_path": relative,
                "code_url": None,
                "upstream_revision": None,
                "code_verification": "No method source verified in fixed v1; cited dependencies do not establish source release.",
                "review_done": True,
                "review_resolution": "not_reproduced_high_cost",
                "full_experiment_status": "not_reproduced_high_cost",
                "full_experiment_review_done": True,
                "automatic_retry": False,
                "automatic_implementation_queue": False,
            }
        )
        questions = []
        english_questions = {}
        for qid, level, q, a, e, eq, ea, ee in p["qa"]:
            questions.append(
                {
                    "id": qid,
                    "level": level,
                    "question": q,
                    "answer": a,
                    "example": e,
                    "source_sections": [
                        "背景与主要改动",
                        "核心公式",
                        "数据协议与代码映射",
                        "同主题比较与边界",
                        "高成本完整实验",
                    ],
                    "added": DATE,
                }
            )
            english_questions[qid] = {"question": eq, "answer": ea, "example": ee}
        bank["papers"][identity] = {"questions": questions}
        for uid, unit in question_units({identity: questions}).items():
            qid = uid.rsplit("/", 1)[1]
            english["units"][uid] = {
                "source_sha256": unit.source_sha256,
                "reviewed": True,
                "fields": english_questions[qid],
            }
        pair = [identity, p["peer"]]
        revisions = {x: sha256((ROOT / "docs" / details[x]).read_bytes()).hexdigest() for x in pair}
        q = questions[2]
        proposals["proposals"].append(
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
                    "body": p["compare_cn"] + " " + p["details_cn"],
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
                    "summary": p["compare_cn"] + " 高成本完整实验不复现，组件与能力证据分开。",
                },
                "english": {
                    "comparison": {"position": p["overview_en"], "tradeoff": p["compare_en"]},
                    "analysis": {
                        "title": p["title"],
                        "body": p["compare_en"] + " " + p["details_en"],
                    },
                    "question": english_questions[q["id"]],
                    "update": p["compare_en"]
                    + " Full experiments are not reproduced; components are separate from capability evidence.",
                },
            }
        )
    for path, data in [(qpath, bank), (epath, english), (ppath, proposals), (rpath, review)]:
        dump(path, data)
    print(
        "Appended3papers,1CPUcomponent,12reviewed bilingual questions; preserved5previous write-ups."
    )


if __name__ == "__main__":
    main()
