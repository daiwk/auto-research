"""Explicitly authored Nov23 Agent papers; no shared catalog/bank writes.

--fetch captures three small fixed arXiv PDFs/TeX sources. Default authors only
owned docs and proposals; no checkpoint, data download, API call or experiment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov23-latest/agent-primary"
AUDIT = ROOT / "docs/research-audits/nov23-latest"
DATE = "2026-11-23"
IDS = ("2611.27159", "2611.27070", "2611.27116")
HEADINGS = ["背景与主要改动", "核心公式", "数据协议与代码映射", "同主题比较与边界", "高成本完整实验"]
PAPERS = [
    dict(
        key="acting-to-learning", module="acting_to_learning", id="2611.27159", author="Yaoyuan Yan",
        title="From Acting to Learning: Experience Selection toward Continually Learning Agents",
        cn_title="From Acting to Learning：成功经验该选哪些，而不只是收集多少",
        org="Country Garden Services AI Lab / Omni AI", published="2026-11-20T05:45:48Z",
        topic="Agent 策略学习", card="agent-research/agent-policy-learning",
        peer="agent-research:ace-data", peer_path="agent-research/2608.27260-ace-data/README.md",
        code=None, code_cn="未找到/未核实论文专属公开源码：固定v1正文与TeX仅说明记录已版本化，未给出可核实仓库；不能将LESS或ALFWorld引用仓库当成本篇开源。",
        code_en="No paper-specific source repository was found or verified in fixed v1. The paper says records are versioned but supplies no verifiable repository link; LESS and ALFWorld dependencies are not this paper's release.",
        page=2, figure="Figure 1", crop=[100, 65, 515, 425],
        locations=["Problem and Selection Procedure: optimizer-aware score and Algorithm 1", "Experimental Design: student, shared executor and task groups", "Costs and Limitations", "Reproducibility appendix"],
        method="论文把成功交互后的经验选择单独隔离：历史池先固定，选择规则决定训练哪些action记录，所有学生使用同一训练预算与部署executor。它不是一个新通用梯度影响公式；打分沿用LESS式优化器感知梯度，贡献是Agent学习中的严格对照，尤其把排序规则和可选择的覆盖空间交叉。完整研究只有一次选择—训练阶段，没有验证多轮持续学习、遗忘或自主修改harness。",
        method_en="The paper isolates experience selection after successful interaction: historical pools are fixed, a selector chooses action records, and students share a training budget and deployment executor. The score follows LESS rather than introducing a new general influence formula. Its contribution is the controlled agent-learning comparison, especially crossing ranking criteria with coverage freedom. Only one selection-and-training stage is studied; multi-round continual learning, forgetting and autonomous harness editing are not evaluated.",
        mechanism="候选LoRA梯度在warmup第8/16/24/32个checkpoint上，与冻结Adam一、二阶矩构成ranking feature；省略bias correction，不能称作完整AdamW更新。每个公共support梯度先单独归一化，再按任务family取均值；候选feature归一化后与之做点积，先平均checkpoint，再在family间取最大。40条公开support action不含评测query答案。全局选择先按完整messages内容精确去重，保留首代表索引，选256种内容，再三次shuffle共768次展示；matched版本保持reference每个task/action位置与不同内容配额。最终学生从原始base重新开始，不能继承打分warmup权重。",
        mechanism_en="At warmup checkpoints8/16/24/32, candidate LoRA gradients combine with frozen first/second Adam moments into a ranking feature. Bias correction is omitted, so this is not a full AdamW update. Each public-support gradient is unit-normalized before its family mean; normalized candidate features are dotted with these means, averaged across checkpoints, then maximized across families. Forty public support actions contain no evaluation-query answers. Global selection exactly deduplicates complete message contents, keeps first representative indices, selects256 contents and replays three shuffled passes for768 presentations. Matched selection preserves every reference task/action position and distinct-content quota. Final students restart from the original base, not warmup weights.",
        formula=r"a_c(e)=\frac{\beta_1m_c+(1-\beta_1)g_c(e)}{\sqrt{\beta_2v_c+(1-\beta_2)g_c(e)^2+\epsilon}},\quad s(e)=\max_f\frac14\sum_{c\in\{8,16,24,32\}}u(a_c(e))^\top b_{c,f}.",
        result="作者比较2个固定ALFWorld经验池、9种selector、8个初始化×2个sampling seed，共288个4B学生；每个checkpoint在128个development task groups上用同一executor评价。全局gradient相对同等自由度的random提升8.25/5.96个百分点，相对high-NLL提升4.10/4.05点。另128个reserved task groups的等来源提升为7.03/5.03点。它们不是官方ALFWorld seen/unseen test；8×2不是16个独立初始化。固定展示次数不等于相同token或FLOPs；长度机制控制未通过，不能声称已排除长度解释。未报告生产线上A/B。",
        result_en="The author study uses two fixed ALFWorld pools, nine selectors and eight initializations by two sampling seeds, producing2884B students evaluated on128 development task groups with one executor. Global gradient selection exceeds equally unconstrained random by8.25/5.96points and high-NLL by4.10/4.05points. On128 reserved groups, equal-source gains are7.03/5.03points. These are not the official ALFWorld seen/unseen test sets, and eight-by-two is not16 independent initializations. Equal presentations do not equal tokens or FLOPs. The length-control feasibility check fails, leaving length effects unresolved. No production A/B is reported.",
        local="本地独立实现NumPy float64公式核：显式梯度/冻结moments转feature、逐support向量归一化、checkpoint平均后family最大值、按完整字符串精确去重、全局top/random和三轮调度、按reference逐位置匹配stratum并保持不同内容配额的选择。零范数方向原文未定义，明确拒绝而不补造0分；feature中间溢出也拒绝。测试用显式合成梯度与历史action字符串，不把梯度相似度换成词项相似度。没有自动抽LoRA梯度、warmup训练、ALFWorld、Qwen checkpoint、部署executor、学生SFT或能力比较；调用方必须保证support来自公开训练侧而非query答案。",
        local_en="The independent NumPy float64 slice implements explicit-gradient/frozen-moment features, individually normalized support gradients, checkpoint averaging before family maximization, exact full-string deduplication, global top/random selection with three replay passes, and reference-position/stratum distinct-content quotas. Undefined zero-norm directions and intermediate feature overflow are rejected, not assigned invented scores. Synthetic gradients and historical-action strings exercise the formulas; lexical similarity does not replace gradients. No LoRA extraction, warmup training, ALFWorld, Qwen checkpoint, deployment executor, student SFT or capability comparison runs. Callers must ensure support is public training-side information rather than query answers.",
        controls="负控核对checkpoint/family运算顺序、support均值不再归一化、重复行不增加random抽样概率、得分并列按首代表索引、每个shuffle pass访问全部选中内容、matched仍可选择reference以外的同stratum内容、跨stratum重复内容拒绝、NaN/负二阶矩/中间溢出拒绝。seed只改变合成输入与调度，不是独立训练。",
        controls_en="Controls check checkpoint/family order, no renormalization of the support mean, unchanged random sampling under duplicate rows, first-index score ties, complete shuffled passes, matched access to nonreference contents in the same stratum, rejection of cross-stratum duplicate contents, and rejection of NaNs, negative second moments and intermediate overflow. Seeds change synthetic inputs and schedules, not independently trained models.",
        cost="原文Qwen3-4B-Instruct-2507（revision cdbee75f17c01a7cc42f958dc650907174af0554），rank16 LoRA，每学生192 updates、768 presentations、2048序列；两池721/732条action记录、418/508种内容。作者主研究62.146累计GPU小时，补64学生17.419小时、97 checkpoint reserved评测24.240小时，合计至少103.805 GPU小时，历史采集另计。单A100/A30或Mac不能在本轮短时预算内完整重做该多臂矩阵，完整实验不复现，不下载权重/数据、不试训。CPU数组核预期秒级；这是估计，具体耗时以统一runner回执为准。",
        cost_en="The source uses Qwen3-4B-Instruct-2507 revision cdbee75f17c01a7cc42f958dc650907174af0554,rank16LoRA,192updates,768presentations and2048-token sequences per student. Pools contain721/732action records and418/508contents. Reported costs are62.146GPU-hours for the main study,17.419for64additional students and24.240for reserved evaluation of97checkpoints: at least103.805GPU-hours, excluding earlier collection. The full multi-arm matrix exceeds this batch's short one-A100/A30-or-Mac budget; no weights/data or trial training are launched. CPU array controls are estimated to take seconds; measured timing belongs to the shared runner receipt.",
        compare="ACE Lens把Accuracy、学习者相对Complexity和Diversity作为数据准入维度；本篇进一步问同样成功的action在当前学生/optimizer状态下，对公开任务family有多大梯度相关性，并把coverage自由度作为对照的一部分。两者都不能把“成功”自动等同于“最值得学”；较低NLL只表示容易预测，不是更高训练收益。ACE旧页的mini-suite也不是本篇ALFWorld训练对照，不能横向比较其满分与本文提升。",
        compare_en="ACE Lens organizes admission around Accuracy, learner-relative Complexity and Diversity. This paper instead ranks already successful actions by optimizer-aware gradient relevance to public task families and controls coverage freedom explicitly. Both distinguish success from learning value; low NLL means predictability, not necessarily greater training benefit. The older ACE mini-suite is not the paper's ALFWorld training comparison and cannot be ranked against its gains.",
        flow_cn="A[固定成功经验池] --> B[去重内容与真实历史]\n  B --> C[冻结moments上的显式梯度score]\n  C --> D[全局或task/action配额选择]\n  D --> E[从原base冷启动学生]\n  E --> F[同executor开发与reserved评测]",
        flow_en="A[Fixed successful experience pools] --> B[Exact contents and genuine histories]\n  B --> C[Gradient scores at frozen moments]\n  C --> D[Global or quota-matched selection]\n  D --> E[Cold-start student from base]\n  E --> F[Shared executor on disjoint panels]",
        questions=[
            ("success-vs-learning","basics","既然记录都成功，为什么还要选择？","成功只说明当时动作完成了任务；重复、容易预测的记录未必补上学生缺口。论文在固定经验池与训练预算下比较选择规则，而不把采集成功率当学生学习收益。","教学例：重复100次熟悉的拿杯子动作，可能不如补一条学生缺失的清洁动作；这只是示意，不是本文测量。","Why select among successful records?","Success describes the original interaction, not the student's marginal learning value. The study fixes pools and update budgets to compare selection rather than equating collection success with learning gain.","Teaching example: one missing cleaning action may teach more than100repetitions of a familiar pickup; this is illustrative, not a measured result."),
            ("checkpoint-before-family","mechanism","为什么不能每个checkpoint先挑最高family再平均？","原公式先对同一family跨checkpoint累积，再取family最大值；反过来会把不同时间各自最有利的family拼成不存在的一致相关性。","教学例：family A在两个checkpoint为1和-1，B为-1和1；正确分数是0，逐checkpoint取max却会得到1。","Why average checkpoints before maximizing families?","The score accumulates evidence for one family across checkpoints before selecting a family. Reversing the order can combine incompatible per-checkpoint winners.","Teaching example: familyA has scores1,-1 andB has-1,1; the specified score is0, while per-checkpoint maximization incorrectly gives1."),
            ("ace-selection-space","comparison","与ACE Lens相比，本篇额外控制了什么？","ACE组织数据可信度、复杂度和覆盖；本篇把排序规则与选择空间分开，global random和global high-NLL也可自由改变coverage，避免把自由度差异误算成gradient优势。","教学例：如果gradient可跨任务挑256条，random也应能跨任务挑256条；不能只给random固定旧任务配额。","What does this study control beyond ACE Lens?","It separates the ranking rule from its admissible selection space. Global random and high-NLL share the gradient selector's freedom to change coverage, avoiding a confound from unequal freedom.","Teaching example: if gradient selects256records globally, random must also have global freedom rather than being forced to preserve old task quotas."),
            ("cold-start-no-query","implementation","打分warmup权重能作为最终学生起点吗？","不能在复刻该协议时这样做。warmup只提供feature，最终学生从原base和新LoRA重新开始；公开support action不等于评测query答案，后者不能进入打分器。","教学例：先在4个warmup checkpoint算score，选择内容后丢弃warmup adapter，再按相同初始化训练各selector。","May final students start from feature-warmup weights?","Not under this protocol. Warmup provides features only; final students restart from the original base with fresh LoRA. Public support actions are not evaluation-query answers, which must remain outside scoring.","Teaching example: compute scores at four warmup checkpoints, discard that adapter, then train selector arms from paired original initializations."),
        ],
    ),
    dict(
        key="r2-tool-redundancy", module="r2_tool_redundancy", id="2611.27070", author="Yilin Zhao",
        title="$R^2$: Recognizing and Reducing Redundant Visual Tool Use",
        cn_title="R²：把视觉反馈依赖变成正确轨迹内的效率优势",
        org="Tsinghua University", published="2026-11-20T03:38:36Z", topic="Agent 策略学习",
        card="agent-research/agent-policy-learning", peer="agent-research:adastep",
        peer_path="agent-research/2610.03223-adastep/README.md", code=None,
        code_cn="固定v1正文与TeX未找到本篇方法专属的已核实公开源码链接；文中其他开源VLM/训练框架不等于本方法开源。",
        code_en="No verified paper-specific method source link was found in fixed-v1 text or TeX. Referenced open models and training frameworks are not a release of this method.",
        page=4, figure="Figure 2", crop=[35, 60, 575, 360],
        locations=["§3.1 CAT", "§3.2 Eq.1-10", "Appendix C.1 Tables9-10", "Appendix C.3 Table12", "Appendix E all-tool-avoidance caveat"],
        method="R²把三个问题分开：CAT描述题目是否可能从工具获益；VFD描述一次返回观察对后续同一段推理文本提供多少额外似然支持；RA-GRPO在答对的轨迹之间比较工具效率，而不是奖励所有少调用的轨迹。CAT标签来自训练侧tool/no-tool rollouts的多次正确性和实际调用，不是根据问题长度或关键词猜测；VFD也不是gold-answer概率或“这次工具有用”的因果证明。",
        method_en="R² separates sample-level tool utility(CAT), the additional likelihood support an observation supplies to the same subsequent reasoning window(VFD), and efficiency comparisons among correct trajectories(RA-GRPO). CAT uses training-side tool/no-tool rollouts and actual invocations, not question-length or keyword heuristics. VFD is neither a gold-answer score nor a causal proof that a call is necessary.",
        mechanism="VFD仅替换当前调用的视觉反馈，保留原图、其他历史与待评分推理tokens；实际反馈的平均log概率减去3个同尺寸不重叠随机crop的平均。前10%训练步按来源、只用reasoning windows估计30%分位阈值，之后冻结；直接答案window可在监督时用，但不参与初始化。每轨迹均匀抽一个eligible call，以M×冗余指示量估计全部eligible冗余数，完整记录但score缺失时指示量设1，空eligible集为0。Tool-Independent另加0.5×全部调用数。效率优势只在同题答对轨迹内居中、除固定调用预算4，再以0.2加到outcome优势；不能把失败少调用当高效率成功。",
        mechanism_en="VFD replaces only the current feedback while retaining the source image, other history and scored reasoning tokens. It subtracts mean log probability under three same-sized nonoverlapping random crops from that under actual feedback. During the first10%of training, source-specific30th-percentile thresholds use reasoning windows only, then freeze. Direct-answer windows may be scored later but cannot initialize thresholds. One uniformly sampled eligible call estimates the redundant count byMtimes its indicator; unavailable scores with complete records set the indicator to1, and empty eligible sets cost0. Tool-Independent adds0.5times all calls. Efficiency advantages are centered only among correct trajectories, divided by fixed call budget4, and added with weight0.2 to outcome advantages. Cheap failures receive no efficiency reward.",
        formula=r"d=\ell(u\mid h,v)-\frac1J\sum_j\ell(u\mid h,\tilde v^{(j)}),\quad C_i=M_i z_i+K\mathbf1[c(x)=\mathrm{Independent}]N_i,\quad A_i=A_i^{out}+\beta\mathbf1[r_i=1]\frac{\bar C^+-C_i}{B}.",
        result="作者在7个视觉benchmark上，RA-GRPO相对Vanilla GRPO平均调用从1.13降到0.99（12.39%），benchmark宏平均准确率67.98→68.13，类别宏平均提升3.35个百分点；每题最多4次工具调用。不是每个benchmark都涨：HR-4K、HR-8K、V⋆Bench相对Vanilla GRPO准确率下降。CoF-SFT附加实验最后完全不调用工具，作者停止对其做进一步工具分析；不能把少调用直接当会用工具。均为离线论文结果，未报告生产线上A/B。",
        result_en="Across seven visual benchmarks, the paper reports1.13to0.99mean calls versus Vanilla GRPO(12.39%fewer), benchmark macro accuracy67.98to68.13and a3.35-point category-macro gain, with at most four calls per question. Accuracy does not improve on every benchmark: HR-4K,HR-8KandV-starBench decline versus Vanilla GRPO. An additional CoF-SFT experiment learns to avoid tools entirely; the authors stop further tool analysis there. Fewer calls alone do not establish tool-use capability. Results are offline, with no production A/B.",
        local="CPU NumPy组件只执行同文本token log概率的VFD差、reasoning-only分来源冻结阈值、单eligible-call无偏冗余估计和类别base cost、sample-SD outcome advantage、仅正确轨迹效率项及clipped GRPO标量目标。分位数采用线性插值、目标按每轨迹有效token均值再组平均，是公开的数值约定；不宣称与未公开trainer逐位相等。调用方必须已保证同一推理window、有效crop与完整记录；数组不能证明这些语义。没有VLM、crop构造/评分、CAT rollout标注、图像数据、policy反传/更新或视觉Agent评测；数值差分只检验标量目标导数，不是训练。没有gold答案/计划接口，reward为外部trainer/evaluator给定的0/1标量。",
        local_en="The CPU NumPy slice computes same-text token-log-probability VFD, reasoning-only source-frozen thresholds, one-eligible-call redundancy estimation and category base costs, sample-SD outcome advantages, correct-only efficiency terms and a clipped GRPO scalar. Linear quantile interpolation and mean-valid-tokens-per-trajectory then group averaging are explicit local conventions, not bitwise equivalence to an unreleased trainer. Callers must supply aligned reasoning windows, valid crops and complete records; arrays cannot establish those semantics. No VLM, crop construction/scoring, CAT rollout labeling, images, policy backprop/update or visual-agent evaluation runs. Finite differences check a scalar derivative, not training. There is no gold-answer/plan interface;binary rewards are external trainer/evaluator inputs.",
        controls="负控包括actual与alternative相同时VFD为0、阈值不吸收答案window、来源缺warmup拒绝、d恰好等于阈值不判冗余、None与空eligible区分、抽一个调用而非逐个累加、失败轨迹效率项严格为0、correct集合内效率项和为0、全错/单个correct/相同cost时效率为0、负优势裁剪方向、padding无贡献与中间溢出拒绝。三seed的数值控制不支持工具效率或准确率提升结论。",
        controls_en="Controls cover zero VFD for identical feedback scores, exclusion of answer windows from calibration, rejection of missing-source warmup, strict threshold inequality, unavailable-score versus empty-eligible behavior, one-call sampling rather than full counting, zero efficiency terms for failures, zero-sum correct-set efficiency, all-wrong/single-correct/equal-cost cases, negative-advantage clipping, padding exclusion and intermediate-overflow rejection. Three seeds of numerical controls do not establish tool-efficiency or accuracy gains.",
        cost="原文Qwen3-VL-8B-Instruct、3254训练例、406步、每步8题×8轨迹、8192输出tokens、最大20480训练context；8张H100约13小时，即约104 H100 GPU小时，另含CAT数据构建、多次VFD评分及7个benchmark。对单A100/A30或Mac明显高成本，完整视觉RL与评测直接不复现，不下载权重/图像、不试跑；只运行秒级CPU显式数组核（预估，实测看runner）。",
        cost_en="The paper uses Qwen3-VL-8B-Instruct,3254examples,406steps,eight questions by eight trajectories per step,8192output tokens and up to20480training context tokens. Eight H100s for about13hours total about104H100GPU-hours, before CAT construction, repeated VFD scoring and seven-benchmark evaluation. This clearly exceeds oneA100/A30or a Mac. Full visual RL/evaluation is not reproduced, with no weight/image downloads or trial runs; only small CPU explicit-array controls execute, estimated in seconds pending runner timing.",
        compare="AdaStep看同锚状态下动作间回报方差相对动作内噪声，调节局部信用可靠性；R²看当前视觉反馈对同一后续推理的依赖，并把成本只在correct集合内相对化。它们都补充终局奖励，但方差解释率不是观察必要性，VFD也不衡量动作内随机回报噪声。不能把AdaStep的权重直接当VFD，或把R²效率项施加给失败轨迹。本地两者都是统计/数值组件，不能比较其Agent能力。",
        compare_en="AdaStep weights local credit by between-action return variance relative to within-action noise at a shared anchor state. R² estimates dependence on a current visual observation and relativizes costs only within the correct set. Both supplement outcome rewards, but explained variance is not observation necessity, and VFD does not estimate stochastic return noise. AdaStep weights cannot substitute for VFD, nor may R² efficiency reward failures. Both local slices are statistical/numerical components rather than comparable agent-capability evaluations.",
        flow_cn="A[训练侧CAT类别] --> D[类别base cost]\n  B[同推理文本的actual/替代log概率] --> C[VFD与冻结来源阈值]\n  C --> D\n  D --> E[仅correct集合相对效率]\n  E --> F[outcome加效率优势与clipped目标]",
        flow_en="A[Training-side CAT category] --> D[Category base cost]\n  B[Same reasoning under actual/alternative feedback] --> C[VFD and frozen source threshold]\n  C --> D\n  D --> E[Relative efficiency among correct outputs]\n  E --> F[Outcome plus efficiency in clipped objective]",
        questions=[
            ("less-calls-not-capability","basics","工具调用越少就越好，为什么不直接奖励少调用？","失败轨迹也可能一次工具都没用。R²先保留正确性监督，再只在同题正确轨迹中比较成本；少调用本身不证明能解决任务或会用工具。","教学例：一条答错但0调用、两条答对分别1/3调用；效率奖励只能比较后两条，不能给答错轨迹加分。","Why not directly reward fewer calls?","Wrong trajectories may use no tools. R² keeps correctness supervision and compares efficiency only among correct trajectories for the same question. Fewer calls alone prove neither task success nor tool skill.","Teaching example: one wrong zero-call output and correct one-/three-call outputs; only the two correct outputs receive relative efficiency credit."),
            ("same-reasoning-vfd","mechanism","VFD为什么固定同一段后续推理，不重新生成？","它比较当前观察对已经生成的同一文本提供的额外似然支持，避免把随机重生成的文字差异混进来；只替换当前反馈，其他历史仍保留。低VFD是冗余信号，不是因果必要性证明。","教学例：原crop和随机crop都让同一推理段log概率为-0.4，则VFD为0；不能把不同答案的概率相减冒充该指标。","Why score the same reasoning rather than regenerate it?","VFD measures additional likelihood support for already generated text, avoiding a confound from random regeneration. Only current feedback changes; other history stays. Low VFD signals potential redundancy, not proven causal necessity.","Teaching example: if actual and alternative crops both give the same window mean log probability-.4,VFD is0; probabilities of different answers are not this comparison."),
            ("adastep-vs-vfd","comparison","R²与AdaStep都是credit方法，能交换统计量吗？","不能。AdaStep从同状态动作组的回报方差估计局部信用可靠性；R²用当前视觉反馈的同文本似然差估计冗余成本，再只在correct集合内比较。它们条件信息与归一化对象不同。","教学例：重复crop可能VFD接近0，但动作后环境回报很稳定；稳定不等于观察不冗余。","Can R² and AdaStep exchange their statistics?","No. AdaStep uses action-group return variance at a shared state to estimate credit reliability. R² uses same-text feedback likelihood differences for costs, then compares correct outputs only. Their conditioning and normalization differ.","Teaching example: a repeated crop may have near-zeroVFD despite stable later returns; stability does not make the observation nonredundant."),
            ("missing-score-vs-ineligible","implementation","score缺失和没有eligible调用可以都记0吗？","不可以。附录C.3规定：记录完整但score不可用的抽中eligible调用记z=1；空eligible集合才冗余成本为0。失败/记录不完整调用先排除，不应伪装成缺失score的完整调用。","教学例：3个eligible里抽到一个None，估计冗余数为3；如果3次调用全部无有效crop，eligible为空，冗余项才为0。","Are missing scores and no eligible calls both zero cost?","No. C.3 assignsz=1to an otherwise eligible complete call with unavailable score. Only an empty eligible set has zero redundancy cost. Failed/incomplete calls are excluded before sampling.","Teaching example: samplingNonefrom three eligible calls estimates3redundant calls; if no call returns an eligible crop, the redundancy term is0."),
        ],
    ),
    dict(
        key="coevobench", module=None, id="2611.27116", author="Chuan Xiao",
        title="CoEvoBench: Can LLMs Drive Recursive Co-Evolution of Agentic Systems?",
        cn_title="CoEvoBench：让反馈决定改模型还是改Harness，而非按步骤完成科研仪式",
        org="Zhejiang University / Alibaba Group / Shanghai Jiao Tong University",
        published="2026-11-20T04:40:59Z", topic="执行框架与自改进",
        card="agent-research/harness-and-self-improvement", peer="agent-research:sage-evolve",
        peer_path="agent-research/2611.26132-sage-evolve/README.md",
        code="https://github.com/AlibabaResearch/CoEvoBench/tree/d39a924c8985806933c94777d8e969d6e756262c",
        code_cn="是：[原作者AlibabaResearch固定提交](https://github.com/AlibabaResearch/CoEvoBench/tree/d39a924c8985806933c94777d8e969d6e756262c)，MIT。上游README同时披露当前镜像/最终评分接口的验收和完整性缺口；开源不等于本地已跑通。",
        code_en="Yes: [fixed AlibabaResearch commit](https://github.com/AlibabaResearch/CoEvoBench/tree/d39a924c8985806933c94777d8e969d6e756262c),MIT. Its README also discloses acceptance/integrity gaps in current images and final-scoring interfaces; release is not local end-to-end validation.",
        page=2, figure="Figure 1", crop=[65, 65, 550, 462],
        locations=["§3.1-3.4 Eq.1-7", "§4 Table1", "§5 model-harness coupling", "Appendix11 resources", "Appendix19 audit", "fixed upstream README no-GPU smoke caveat"],
        method="CoEvoBench不是另一个固定自进化算法，而是测LLM researcher能否自主驱动模型权重和harness联合开发的benchmark。目标系统为(θ,H)：同一初始base与领域初始harness出发，researcher可检查执行、造训练数据/训模型、改工具和控制逻辑。开发后提交冻结的模型—harness对，在独立Test任务上执行。关键不是是否做过“诊断—训练—改代码”，而是先前反馈能否改变下一步干预和最终候选选择。",
        method_en="CoEvoBench is a benchmark of autonomous model-harness co-development, not another fixed evolution algorithm. A target system is(theta,H), starting from common base weights and a domain-specific initial harness. The LLM researcher may inspect executions, construct training data/update weights, and edit tools/control logic. A nominated frozen pair is evaluated on separate Test tasks. The question is whether feedback changes the next intervention and final choice, not whether a researcher merely completes diagnosis/training/code-editing stages.",
        mechanism="五个域覆盖SWE-bench Verified、TB-Lite、AppWorld、Telecom及BFCL多轮/记忆。Visible可看任务和轨迹，Selection只回聚合性能、不给题面/轨迹，Test仅operator最终评价。每run24小时、4张H20、100美元teacher allowance；θ和H相互耦合，不能把两者增益相加当独立贡献。正文对确认违规run退回base权重但保留最终harness，另报退回整个初始系统的更严格规则。75个9B run中22个确认违规（均访问禁用数据，6个还训练其上）；这说明须审计完整数据血缘，不能把benchmark声称隔离当成绝无泄漏证明。",
        mechanism_en="Five domains cover SWE-bench Verified,TB-Lite,AppWorld,Telecom,and BFCL multi-turn/memory. Visible exposes tasks/traces;Selection returns aggregate scores without task contents/traces;Test is operator-only. Each run gets24hours,fourH20s and a100-dollar teacher allowance. Weights and harness are coupled, so their gains are not additive independent contributions. The main rule resets confirmed-violation runs to base weights while retaining their final harness; a stricter alternative resets the whole system. Among759B runs,22confirmed violations all accessed prohibited data and six trained on it. Full data-lineage audits remain essential; intended isolation is not proof that leakage never occurred.",
        formula=r"S=(\theta,H),\quad a_t\sim R(\cdot\mid\mathcal T_t),\quad\mathcal T_{t+1}=\mathcal T_t\oplus(a_t,o_{t+1}),\quad J_b(R)=\widehat{\mathcal E}_b(S_b^\star)-\mathcal E_b(S_b^{(0)}).",
        result="原文9B目标的加权Test均分：base1.09、最强researcher31.23、instruction-tuned reference37.42；权重按各域reference-base gap的倒数归一，不是五域简单平均。28个无audit问题且改善的reviewed runs里25个最大单步增益来自最初候选；编码任务最强配置往往提交base+harness而非训练权重，交互任务才更常从训练获益。这不是已实现无上限递归自改进，更不是本文本地测量。未报告生产线上A/B。",
        result_en="For the9B target,weighted Test scores are1.09forBase,31.23for the strongest researcher,and37.42for the instruction-tuned reference. Weights normalize inverse reference-minus-base gaps rather than taking an ordinary five-domain mean. In25of28reviewed improving runs without audit issues,the first candidate supplies the largest single gain. Strong coding submissions often use base weights plus an improved harness;training pays off more often on interaction tasks. These are author results,not unbounded RSI or local measurements.No production A/B is reported.",
        local="本地只收录固定v1、代码提交、split/审计/成本契约与同主题比较；没有新建算法模块、可执行adapter、训练、researcher API调用或benchmark试跑。上游no-GPU toy researcher明确是生命周期fixture，不是自主科研Agent；把它执行成功不算本论文能力复现，也不应注册为Evolve算子。高成本决定本身已审查完成，不需要伪造种子指标或GPU回执。",
        local_en="Local delivery is review-only: fixed-v1/code metadata,split/audit/cost contracts and a same-topic comparison.No algorithm module,executable adapter,training,researcher API call or benchmark trial is created.The upstream no-GPU toy researcher is explicitly a lifecycle fixture,not an autonomous researcher.Running it cannot reproduce this paper's capability or justify an Evolve operator.A completed high-cost review requires no invented seed metrics or GPU receipt.",
        controls="审查保留两种audit评分规则，不把reset权重简化成删除所有违规影响的形式证明；论文记录的可见集过拟合和harness—模型错配是方法分析，不是本地负控实测。代码仓库状态与论文报告分开记录。无本地能力结果，不创建自动实现/重试队列。",
        controls_en="The review preserves both audit scoring rules and does not treat resetting weights as a formal proof that every consequence of prohibited access disappears.Visible-set overfitting and model-harness mismatch are author analyses,not locally measured controls.Repository acceptance status is distinct from paper-reported experiments.No local capability result or automatic implementation/retry queue is created.",
        cost="正文每个development run为4×H20×24小时上限（96 H20 GPU小时）加100美元teacher allowance，并非本地实测；全矩阵还含5个researcher×5个域×3次独立run×2个目标家族（Qwen3.5-9B-Base/MiniCPM5-2B-Base），并需容器/环境构建、训练、服务与隔离最终评价。即使2B能在单A100/A30放下，也不能据此把长rollout和多臂研究变成廉价等价实验。预算为单A100/A30或Mac，直接终态不复现；不下载checkpoint/大数据、不起Docker/GPU、不运行toy证明成本、不调用teacher或researcher。",
        cost_en="Each development run is budgeted up to4H20s for24hours(96H20GPU-hours),plus100dollars for a teacher;these are protocol limits,not local measurements.The full matrix spans five researchers,five domains,three runs and two target families(Qwen3.5-9B-Base/MiniCPM5-2B-Base),with container/environment building,training,serving and isolated final evaluation.A2B model fitting oneA100/A30does not make long rollouts and the multi-arm research campaign cheap or equivalent.With oneA100/A30or a Mac available,the full study is terminally not reproduced.No checkpoints/large data,Docker/GPU,toy cost probes,teacher or researcher calls are launched.",
        compare="Sage-Evolve固定anchor并改变active observation来发现新训练缺口，提出具体自改进策略；CoEvoBench固定benchmark开发/选择/Test契约，把选择改模型还是改harness交给被测researcher，并评价其提交结果。前者的“改观察”不是偷偷改最终评分器，后者的“两个可改旋钮”也不是交替更新就算成功。共同边界是不能用visible训练成绩选最终能力结论；本地Sage只有CPU控制核，CoEvo仅审查，二者没有可比较的Agent提升。",
        compare_en="Sage-Evolve is a specific strategy that keeps an anchor while changing active observations to expose training gaps.CoEvoBench instead fixes development/Selection/Test contracts,lets the evaluated researcher decide whether to edit weights or harness,and scores the nominated system.Changing observations is not changing final graders,and access to two levers does not make fixed alternation successful co-evolution.Both require evidence beyond visible training performance.The local Sage slice is a CPU control kernel and CoEvo is review-only;neither supplies comparable agent gains.",
        flow_cn="A[共同base与初始Harness] --> B[Researcher检查执行反馈]\n  B --> C{改模型 或改Harness}\n  C --> D[Visible诊断与Selection聚合评分]\n  D --> B\n  D --> E[冻结最终pair]\n  E --> F[独立Test与完整轨迹审计]",
        flow_en="A[Common base and initial harness] --> B[Researcher reads execution feedback]\n  B --> C{Edit weights or harness}\n  C --> D[Visible diagnostics and Selection scores]\n  D --> B\n  D --> E[Freeze nominated pair]\n  E --> F[Separate Test and full-trajectory audit]",
        questions=[
            ("benchmark-not-algorithm","basics","CoEvoBench本身是一套自动自进化算法吗？","不是。它提供共同起点、可修改模型/harness的动作空间、预算和隔离评价，测researcher如何根据反馈决定下一步；不同被测researcher可走不同开发路线。","教学例：一个researcher只修格式接口后提交base，另一个先改工具再训模型，都可在同一协议下评价，而不是强制轮流训练/改代码。","Is CoEvoBench itself an evolution algorithm?","No.It supplies common starting systems,model/harness action spaces,budgets and isolated evaluation to measure the researcher's feedback-driven decisions.Different researchers may follow different routes.","Teaching example: one researcher may submitBaseafter an interface fix;another may edit tools then train.Both are evaluated under one protocol,without mandatory alternation."),
            ("coupled-levers","mechanism","为什么不能把模型收益与Harness收益简单相加？","模型是在特定harness轨迹上学到行为的。换接口、history或工具后，原训练权重的收益可能反转；必须交叉评价同一权重/不同harness与同一harness/不同权重。","教学例：旧harness下训练比base多解5题，换harness后少解4题；重新收集新harness轨迹再训才恢复正收益。数字是论文case，不是本地实验。","Why not add weight and harness gains?","Weights learn behavior under a particular harness.Changing interfaces,history or tools may reverse a training gain.Cross-evaluation must hold one component fixed while varying the other.","Teaching example: a paper case goes fromfiveextra solved tasks tofourfewer after a harness change;retraining on refreshed trajectories restores a gain.These are author observations,not local results."),
            ("adaobs-vs-benchmark","comparison","与Sage-Evolve相比，CoEvoBench把什么交给researcher？","Sage给出固定anchor/自适应active observation的具体策略；CoEvo给出有保护的开发与最终评测协议，让researcher自己决定改权重还是改harness。前者是策略，后者是测决策的benchmark。","教学例：按长度细分失败是Sage式观察改变；在CoEvo里研究者还要判断该修parser、重训还是放弃训练路线。","What does CoEvoBench leave to the researcher compared with Sage-Evolve?","Sage specifies a fixed-anchor/adaptive-observation strategy.CoEvo supplies protected development/final-evaluation contracts and lets the researcher choose weight or harness interventions.It benchmarks research decisions rather than prescribing that strategy.","Teaching example: length-bucket diagnostics change a Sage-style observation;the CoEvo researcher must additionally decide whether to fix a parser,retrain,or abandon training."),
            ("toy-not-rsi","implementation","上游no-GPU toy跑通能算低成本RSI复现吗？","不能。上游明确toy是生命周期fixture，只检查workspace、broker与退出；没有自主researcher、模型更新或真实held-out任务得分。本轮完整实验高成本终态，只做审查，不把fixture晋级。","教学例：定时器到期能清理容器是运维验收；researcher从负结果改路线并在独立Test改善才是该benchmark要测的能力。","Does a no-GPU toy smoke run reproduce RSI cheaply?","No.The upstream toy is a lifecycle fixture for workspace,broker and shutdown,not an autonomous researcher,model update or held-out capability score.The full study is terminally cost-deferred here;fixtures are not promoted.","Teaching example:deadline cleanup validates operations;changing research direction after negative feedback and improving on separate Testtasks is the capability being evaluated."),
        ],
    ),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    for aid in IDS:
        for kind, suffix in (("pdf", "pdf"), ("src", "tar.gz")):
            path = CACHE / f"{aid}v1.{suffix}"
            if not path.exists():
                request = Request(f"https://arxiv.org/{kind}/{aid}v1", headers={"User-Agent": "auto-research/primary-review"})
                with urlopen(request, timeout=40) as response:
                    raw = response.read(15_000_001)
                if len(raw) > 15_000_000:
                    raise ValueError("small-paper capture budget exceeded")
                path.write_bytes(raw)
            print(path.name, path.stat().st_size, digest(path), flush=True)
    path = CACHE / "coevobench-readme-d39a924c.md"
    if not path.exists():
        request = Request("https://raw.githubusercontent.com/AlibabaResearch/CoEvoBench/d39a924c8985806933c94777d8e969d6e756262c/README.md",
                          headers={"User-Agent": "auto-research/primary-review"})
        with urlopen(request, timeout=30) as response:
            raw = response.read(500001)
        if len(raw) > 500000:
            raise ValueError("upstream README exceeds review budget")
        path.write_bytes(raw)
    print(path.name, path.stat().st_size, digest(path), flush=True)


def inspect():
    import fitz
    for aid in IDS:
        pdf = fitz.open(CACHE / f"{aid}v1.pdf")
        for number, page in enumerate(pdf):
            text = page.get_text()
            if number < 3 or "Figure 2:" in text or "Figure 1:" in text:
                print(aid, number + 1, page.rect, text[:160].replace("\n", " "))
                page.get_pixmap(matrix=fitz.Matrix(1.1, 1.1)).save(CACHE / f"{aid}-page{number + 1}.png")


def refresh_figures():
    """Regenerate owned figure assets after an explicit visual crop correction."""
    import fitz
    for paper in PAPERS:
        assets = ROOT / f"docs/agent-research/{paper['id']}-{paper['key']}/assets"
        provenance = assets / "provenance.json"
        record = json.loads(provenance.read_text())
        pdf = fitz.open(CACHE / f"{paper['id']}v1.pdf")
        image = assets / "paper-figure-01.png"
        pdf[paper["page"] - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(paper["crop"])).save(image)
        pdf.close()
        figure = record["figures"][0]
        figure.update(crop_points=paper["crop"], asset_sha256=digest(image), image_sha256=digest(image))
        write(provenance, record)


def author():
    import fitz
    from english_learning_sources import question_units

    bundle_path = AUDIT / "agent-authored-bundle.json"
    if bundle_path.exists():
        raise ValueError("append-once owned bundle already exists; review changes in place")
    papers, english, specs, proposals, reviews = {}, {}, [], [], []
    for paper in PAPERS:
        key, aid = paper["key"], paper["id"]
        identity = "agent-research:" + key
        directory = ROOT / f"docs/agent-research/{aid}-{key}"
        assets = directory / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        source = CACHE / f"{aid}v1.pdf"
        image = assets / "paper-figure-01.png"
        pdf = fitz.open(source)
        pdf[paper["page"] - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(paper["crop"])).save(image)
        pdf.close()
        source_hash, image_hash = digest(source), digest(image)
        write(assets / "provenance.json", {"schema_version": 1, "reviewed_on": DATE, "figures": [{
            "file": image.name, "paper_id": aid, "version": "v1", "figure": paper["figure"],
            "source_url": f"https://arxiv.org/pdf/{aid}v1#page={paper['page']}",
            "paper_url": f"https://arxiv.org/abs/{aid}v1", "source_kind": "fixed_version_pdf_crop_rendered_png",
            "source_sha256": source_hash, "asset_sha256": image_hash, "image_sha256": image_hash,
            "page": paper["page"], "crop_points": paper["crop"], "render_dpi": 144,
            "caption_included": True, "scientific_content_modified": False,
            "visual_review_done": True,
            "attribution": "Original author figure and caption; copyright belongs to the authors. Not local results.",
            "license": "See fixed original arXiv source; no new license granted."}]})
        component = paper["module"] is not None
        module = "auto_research.agent_research." + paper["module"] if component else None
        local = "src/auto_research/agent_research/" + paper["module"] + ".py" if component else None
        test = "tests/test_nov23_" + paper["module"] + ".py" if component else None
        command = f"PYTHONPATH=src python -c 'from {module} import diagnostic; print(diagnostic(42))'" if component else None
        peer_link = os.path.relpath(ROOT / "docs" / paper["peer_path"], directory)
        label_cn = "`component_only` / L1 CPU公式与调度诊断，`diagnostic_only=true`。不是Agent能力复现或Evolve集成。" if component else "`deferred_high_cost` / 资料收录，未实现、未运行；成本过高，不复现（审查 DONE）。"
        label_en = "`component_only` / L1 CPU formula/scheduling diagnostics, `diagnostic_only=true`. Not agent-capability reproduction or Evolve integration." if component else "`deferred_high_cost` / review-only, not implemented or run. Too costly; not reproduced (review DONE)."
        local_cn = f"`{local}`；测试 `{test}`" if component else "无：本篇仅审查，未创建复现代码目录或adapter"
        local_en = f"`{local}`; tests `{test}`" if component else "None: review-only; no reproduction-code directory or adapter was created"
        run_cn = f"""```bash
{command}
PYTHONPATH=src python -m pytest {test} -q
```

冻结源码后由统一runner记录[42/43/44三seed CPU机制结果](metrics/component-cpu-seeds42-44.json)。输入是显式合成控制，不加载能力benchmark、不据test选参数。三seed不是三次模型训练，不提升L1证据等级。""" if component else "本篇没有本地执行命令或能力指标。review-only成本终态不需要也不伪造metrics或GPU验证。"
        run_en = f"""```bash
{command}
PYTHONPATH=src python -m pytest {test} -q
```

After source freeze,the shared runner records [seed42/43/44 CPU mechanism results](metrics/component-cpu-seeds42-44.json). Inputs are explicit synthetic controls,with no capability benchmark or test-based tuning. Three seeds are not three trained models and do not upgrade L1 evidence.""" if component else "There is no local execution command or capability metric. The terminal review-only cost decision needs no invented metrics or GPU validation."
        cn = f'''# {paper["cn_title"]}

[English](README-en.md)

> {label_cn} 首发为2026-11-20，发现/审查为2026-11-23，不称11月23日新首发。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [{paper["title"]}](https://arxiv.org/abs/{aid}v1)，固定v1 |
| 公司/机构/学校 | 一作{paper["author"]}；{paper["org"]} |
| 首次公开日期 | {paper["published"].replace("T", " ").replace("Z", " UTC")}，arXiv v1；当前修订同日同时间，没有另一次修订 |
| 公告/发现日期 | 本轮公告池未含此身份，公告日未核实；2026-11-23从官方arXiv元数据发现并审查 |
| 原作者开源代码 | {paper["code_cn"]} |
| 本地 Adapter / 方法 | `adapter: null`；{("CPU组件key" if component else "资料key")} `{key}` |
| 本地复现代码目录 | {local_cn} |

## 原始论文总结

### 背景与主要改动

{paper["method"]}

{paper["mechanism"]}

```mermaid
flowchart LR
  {paper["flow_cn"]}
```

<!-- paper-figure:start -->
### 原论文关键图

[![原论文{paper["figure"]}](assets/paper-figure-01.png)](https://arxiv.org/pdf/{aid}v1#page={paper['page']})

图片来自[固定v1原论文](https://arxiv.org/pdf/{aid}v1#page={paper['page']})第{paper['page']}页{paper['figure']}与完整图注，版权归原作者。仅裁掉无关正文和留白，科学内容未修改；已目视核对。[源PDF/裁剪SHA256与坐标](assets/provenance.json)。原图不是本地实验。
<!-- paper-figure:end -->

### 核心公式

$$
{paper["formula"]}
$$

### 论文离线与线上效果

{paper["result"]}

## 本地复现与边界

### 数据协议与代码映射

{paper["local"]}

{run_cn}

### 同主题比较与边界

与已读旧代表[{paper["peer"]}]({peer_link})对照：{paper["compare"]}

{paper["controls"]}

### 高成本完整实验

{paper["cost"]} **成本过高，不复现（审查 DONE）。** 完整实验是终态成本决定，不进入自动重试/实现队列，不因便宜组件通过而升级为完整论文复现。

### 来源核对

固定v1 PDF SHA256：`{source_hash}`。核对位置：{'；'.join(paper['locations'])}。本页是有限增量选题，不推进全库11月15日审查水位，也不宣称Google/Meta或全部Agent文献已穷尽。
'''
        page = directory / "README.md"
        page.write_text(cn)
        cn_hash = digest(page)
        en = f'''# {paper["title"]}

<!-- source-sha256: {cn_hash} -->

[简体中文](README.md)

> {label_en} First released2026-11-20,discovered/reviewed2026-11-23;not a Nov23 first release.

## Paper information

| Field | Value |
| --- | --- |
| Paper | [Fixed arXiv v1](https://arxiv.org/abs/{aid}v1) |
| Company/institution | First author{paper["author"]};{paper["org"]} |
| Original publication | {paper["published"].replace("T", " ").replace("Z", " UTC")};current update has the same timestamp,no separate revision |
| Announcement/discovery | Identity absent from this batch's announcement pool;announcement date unverified.Discovered/reviewed through official arXiv metadata on2026-11-23 |
| Author source code | {paper["code_en"]} |
| Local adapter/key | `adapter: null`;{("CPU component" if component else "review-only")} key `{key}` |
| Local reproduction code | {local_en} |

## Original paper summary

### Background and changes

{paper["method_en"]}

{paper["mechanism_en"]}

### Architecture

```mermaid
flowchart LR
  {paper["flow_en"]}
```

### Key original figure

[![Original {paper["figure"]}](assets/paper-figure-01.png)](https://arxiv.org/pdf/{aid}v1#page={paper['page']})

{paper['figure']}with its complete caption comes from fixed-v1 PDF page{paper['page']};copyright belongs to the original authors.Only unrelated text/whitespace is cropped,with scientific content unchanged.Visually reviewed.[Source](https://arxiv.org/pdf/{aid}v1#page={paper['page']}) and [PDF/crop SHA256 provenance](assets/provenance.json).The image is not local evidence.

### Core equations

$$
{paper["formula"]}
$$

### Reported offline and online results

{paper["result_en"]}

## Local reproduction and limits

### Data protocol and code mapping

{paper["local_en"]}

{run_en}

### Same-topic comparison and limits

Reviewed against [{paper["peer"]}]({peer_link.replace("README.md", "README-en.md")}):{paper["compare_en"]}

{paper["controls_en"]}

### High-cost full experiments

{paper["cost_en"]} **Too costly;not reproduced(review DONE).** This is a terminal cost decision,not an automatic retry/implementation queue.Passing a cheap component does not reproduce the full paper.

### Source review

Fixed-v1 PDF SHA256:`{source_hash}`.Reviewed locations:{'; '.join(paper['locations'])}.This is a finite incremental selection.It does not move the global Nov15 review watermark or claim exhaustive Google/Meta/Agent coverage.
'''
        page.with_name("README-en.md").write_text(en)
        spec = {
            "key": key, "domain": "agent-research", "title": paper["title"],
            "first_author": paper["author"], "first_author_affiliation": paper["org"],
            "published_at": paper["published"], "published": "2026-11-20", "updated_at": paper["published"],
            "announced_on": None, "discovered_on": DATE, "reviewed_on": DATE,
            "paper_url": f"https://arxiv.org/abs/{aid}v1", "reviewed_version": "v1",
            "reviewed_arxiv_id": aid + "v1", "reviewed_version_url": f"https://arxiv.org/pdf/{aid}v1",
            "detail_path": f"agent-research/{aid}-{key}/README.md", "topic": [paper["topic"], key],
            "verified_priority_organizations": [], "code": paper["code"], "code_status": paper["code_cn"],
            "code_license": "MIT" if key == "coevobench" else None, "adapter": None,
            "priority": "P1", "intake_class": "metadata_new_first_release",
            "implementation_status": "component_only" if component else "deferred_high_cost",
            "local_operator": module + ".diagnostic" if component else None,
            "local_command": command, "evaluation_tier": "l1_mechanism" if component else None,
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "requires_gpu_validation": False, "gpu_validation_passed": False, "gpu_validation_artifact": None,
            "review_done": True, "full_experiment_review_done": True,
            "full_experiment_status": "not_reproduced_high_cost", "review_resolution": "not_reproduced_high_cost",
            "automatic_retry": False, "automatic_implementation_queue": False,
            "cost_assessment": {"source": f"https://arxiv.org/pdf/{aid}v1", "available_resource": "one A100 or A30, or local Mac",
                                "basis": paper["cost"], "cost_type": "published_configuration_not_local_measurement",
                                "decision": "成本过高，不复现（审查 DONE）；" + ("仅CPU L1公式组件。" if component else "仅资料收录。")},
            "summary": paper["method"], "fidelity_note": paper["local"], "method_source_sha256": source_hash,
        }
        specs.append(spec)
        bank = []
        for qid, level, question, answer, example, eq, ea, ee in paper["questions"]:
            row = {"id": qid, "level": level, "question": question, "answer": answer, "example": example,
                   "source_sections": HEADINGS, "added": DATE}
            bank.append(row)
            uid = f"qa/{identity}/{qid}"
            english[uid] = {"source_sha256": question_units({identity: [row]})[uid].source_sha256,
                            "reviewed": True, "fields": {"question": eq, "answer": ea, "example": ee}}
        papers[identity] = {"questions": bank}
        comparison = next(row for row in bank if row["level"] == "comparison")
        english_comparison = next(row for row in paper["questions"] if row[1] == "comparison")
        revisions = {identity: cn_hash, paper["peer"]: digest(ROOT / "docs" / paper["peer_path"])}
        proposals.append({
            "paper": identity, "target_card": paper["card"], "source_revisions": revisions,
            "comparison": {"position": paper["method"], "tradeoff": paper["compare"], "sections": HEADINGS},
            "analysis": {"title": paper["cn_title"], "body": paper["mechanism"] + paper["controls"], "papers": [identity, paper["peer"]]},
            "question": {"id": "cross-nov23-" + key, **{field: comparison[field] for field in ("question", "answer", "example")},
                         "papers": [identity, paper["peer"]]},
            "update": {"date": DATE, "papers": [identity, paper["peer"]], "source_revisions": revisions,
                       "summary": paper["local"] + " 完整实验高成本不复现，审查DONE。"},
            "english": {"comparison": {"position": paper["method_en"], "tradeoff": paper["compare_en"]},
                        "analysis": {"title": paper["title"], "body": paper["mechanism_en"] + " " + paper["controls_en"]},
                        "question": {"question": english_comparison[5], "answer": english_comparison[6], "example": english_comparison[7]},
                        "update": paper["local_en"] + " Full experiments are terminally not reproduced."}})
        reviews.append({
            "id": aid, "key": key, "identity": identity, "published_at": paper["published"], "updated_at": paper["published"],
            "announced_on": None, "discovered_on": DATE, "first_author": paper["author"],
            "first_author_affiliation": paper["org"], "source_url": f"https://arxiv.org/pdf/{aid}v1",
            "source_sha256": source_hash, "tex_source_sha256": digest(CACHE / f"{aid}v1.tar.gz"),
            "locations": paper["locations"], "code": paper["code"], "code_status": paper["code_en"],
            "implementation_status": spec["implementation_status"], "evaluation_tier": spec["evaluation_tier"],
            "scope": paper["local_en"], "cost_basis": paper["cost_en"], "full_experiment_status": "not_reproduced_high_cost",
            "requires_gpu_validation": False, "review_done": True, "source_revisions": revisions,
        })
    write(bundle_path, {"schema_version": 1, "date": DATE, "papers": papers, "english_question_units": english})
    write(AUDIT / "paper-proposals-agent.json", {"schema_version": 1, "reviewed_on": DATE, "integration_owner": "root", "papers": specs})
    write(AUDIT / "deep-dive-proposals-agent.json", {"schema_version": 1, "reviewed_on": DATE, "integration_owner": "root", "proposals": proposals})
    write(AUDIT / "agent-review.json", {"schema_version": 1, "reviewed_on": DATE,
                                       "scope": "Three Nov20 first releases discovered Nov23, no Nov21-23 first release or exhaustive claim",
                                       "implementation_preflight_completed": True,
                                       "available_resource": "one A100/A30 or Mac; only bounded CPU formulas execute",
                                       "reviews": reviews, "p2_dispositions": []})
    print("Authored 3 bilingual papers,12 bilingual questions and3 same-topic proposals; shared registries/banks unchanged.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--inspect", action="store_true")
    parser.add_argument("--refresh-figures", action="store_true")
    args = parser.parse_args()
    if args.fetch:
        fetch()
    elif args.inspect:
        inspect()
    elif args.refresh_figures:
        refresh_figures()
    else:
        author()


if __name__ == "__main__":
    main()
