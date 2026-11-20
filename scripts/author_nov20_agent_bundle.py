"""Three independently authored Nov20 Agent/System One paper records.

Run once after source review; shared learning/topic/catalog integration belongs
to the batch owner. No abstract-to-prose or automatic translation is used.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov20-latest"
DATE = "2026-11-20"
HEADINGS = ["背景与主要改动", "核心公式", "数据协议与代码映射", "结果、负控与边界", "高成本完整实验"]

PAPERS = [
    dict(
        key="buggymle-cci", module="agent_research.buggymle_cci", domain="agent-research",
        id="2611.25088", title="BuggyMLE: Scaling Machine Learning Engineering Difficulty with Bug Injection",
        cn_title="BuggyMLE：用代码复杂度分层，而不是把指标恢复当完整修复",
        author="John Wu", org="Google Research / University of Illinois Urbana-Champaign",
        published="2026-11-18T19:26:15Z", tier="l0_interface", topic="执行框架与自改进",
        code=None, license=None, card="agent-research/harness-and-self-improvement",
        peer="agent-research:mle-star", peer_path="agent-research/2506.15692-mle-star/README.md",
        page=8, figure="Figure 3", crop=[55,75,540,397],
        locations=["§3.1 Eq.1-5", "Table4 feature definitions", "Appendix A.2 / Figure10 coefficient signs", "Appendix D training", "Appendix E episode limits"],
        method="BuggyMLE先审核可运行、指标稳定且对代码变化敏感的ML仓库，再让Injector注入不同规模的错误。Oracle通过逐个恢复变动找最小恢复集合，再把每个改动单独应用到干净仓库，筛出确有独立指标影响的错误。Solver必须在多文件仓库里真实修复；评价同时检查执行、指标恢复和逐错误语义修复，不能把补偿性调参当修好了全部bug。",
        method_en="BuggyMLE audits runnable ML repositories with stable, responsive metrics, then uses an Injector to create controlled mutations. An Oracle first finds a minimal reversion set and then applies each mutation separately to the clean repository to identify individually impactful bugs. Solvers repair multi-file repositories. Execution, metric recovery and per-bug semantic repair are checked separately; compensating through tuning is not equivalent to repairing every bug.",
        mechanism="CCI在八个参考benchmark上，先取十项结构特征的任务中位数，做log1p和特征z-score，再对repo、dependency、patch三组求均值，并把组分数按参考方差缩放。固定logistic系数的负加权和构成raw CCI，再用参考最小/最大值定标。新任务不能重新拟合或裁剪回[0,1]。Figure10的repo系数为+0.64，dependency为-0.34，patch为-0.99；repo项是给定其他项的条件调整，不支持“仓库越大必然越难”。",
        mechanism_en="CCI uses task-level median structural features on eight reference benchmarks, applies log1p and feature z-scores, averages within repository, dependency and patch groups, then rescales group scores by reference variance. The negative coefficient-weighted sum is raw CCI, followed by fixed reference min-max scaling. A new task must not refit or clip the scale. Figure10 gives coefficients +0.64, -0.34 and -0.99; the positive repository term is a conditional adjustment, not a claim that larger repositories are always harder.",
        formula=r"z_i=\frac{\log(1+f_i)-\mu_i}{\sigma_i},\quad u_G=\frac{|G|^{-1}\sum_{i\in G}z_i}{s_G},\quad C=-\sum_G\beta_Gu_G,\quad C_{scaled}=\frac{C-C_{min}}{C_{max}-C_{min}}.",
        result="固定v1以222个源仓库生成6600多个变体、近260K行注入代码。八benchmark平均solve rate与CCI的R²为0.951；逐模型/benchmark的LOBO MAE为0.115，benchmark均值MAE为0.048，两者分母不同。14个评测模型中最高完整修复率随难度从95%降至9%；Table3中9B课程模型的SWE-bench Lite从24.3%到33.0%。这是作者离线实验，不是本机结果；未报告生产线上A/B。",
        result_en="Fixed v1 generates over6,600 variants and nearly260K injected lines from222 source repositories. CCI relates to benchmark-average solve rate at R²=0.951; per-model/benchmark LOBO MAE is0.115 while benchmark-average MAE is0.048, with different aggregation units. Across14 evaluated models, the best full-repair rate drops from95% to9% with difficulty. Table3 shows the9B curriculum model improving SWE-bench Lite from24.3% to33.0%. These are author offline results, not local measurements. No production A/B is reported.",
        local="本地仅实现给定十项特征的benchmark中位数、固定校准投影和可选的稳定logistic读数。没有AST/依赖图抽取、Injector、Oracle、LLM solver、校准拟合或模型训练。完整μ/σ、组尺度、截距与参考边界未在原文公开成可直接加载文件，因此API强制调用方显式提供Calibration；诊断用合成校准，不能称为复算了作者八benchmark CCI。Patch特征属于构建/评测端，不能把隐藏修复补丁或其困难标签传给被测Agent。",
        local_en="The local slice implements medians of supplied ten-feature rows, fixed-calibration projection and an optional numerically stable logistic readout. It does not extract ASTs/dependency graphs, run an Injector/Oracle/solver, fit calibration or train models. Complete means, scales, intercept and reference bounds are not released as a loadable artifact, so Calibration is an explicit required input. Diagnostics use synthetic calibration and do not reproduce the author's eight-benchmark CCI. Patch features belong to curation/evaluation; hidden repair patches or their difficulty labels must not be exposed to the evaluated agent.",
        controls="负控保留正repo系数、组方差缩放和参考区间外结果；验证median不是mean，未给截距时不捏造预测成功率。拒绝NaN、零尺度和退化边界。Table4把total_lines_delta写成净变化，若值≤-1会使log1p无定义，接口明确拒绝，既不取绝对值，也不补造作者未说明的变换。",
        controls_en="Controls preserve the positive repository coefficient, group variance scaling and out-of-reference outputs, check median rather than mean, and return no predicted success without an intercept. NaNs, zero scales and degenerate bounds fail. Table4 calls total_lines_delta net line change; values≤-1 make log1p undefined and are rejected, not silently absolutized or replaced with an undocumented transform.",
        cost="完整研究涉及222仓库、6600+变体、多次完整ML执行、前沿模型Oracle/评审和Qwen3.5-9B的五阶段LoRA SFT/GRPO；评测episode最高8小时。此规模明显超过单A100/A30或Mac廉价验证预算，不下载数据/权重，不启动探跑；本地只运行毫秒级公式控制。",
        cost_en="The full study covers222 repositories,6,600+ variants, repeated ML pipelines, frontier-model Oracle/judges and a five-stage Qwen3.5-9B LoRA SFT/GRPO pipeline, with evaluation episodes allowed up to eight hours. This clearly exceeds a cheap single-A100/A30 or Mac run. No datasets/weights or trial runs are started; only tiny arithmetic controls execute.",
        compare="MLE-STAR用检索、真实消融与validation结果定位并改进模型代码；BuggyMLE用有Oracle归因的注入错误构建难度阶梯，CCI是评测/课程设计尺度。前者选改进方案，后者塑造训练与评测任务；不能把后者的结构分数当成前者的真实验证收益。",
        compare_en="MLE-STAR uses retrieval, actual ablations and validation results to improve model code. BuggyMLE builds difficulty tiers from oracle-attributed injected bugs; CCI is a curation/curriculum scale. Selecting an improved solution differs from shaping evaluation/training tasks, and a structural score is not a validation improvement.",
        flow_cn="R[干净仓库审核] --> I[多bug注入]\n  I --> O[最小恢复集合和单独归因]\n  O --> D[难度分层及训练]\n  D --> S[多文件Solver]\n  S --> E[执行与指标及语义修复分别检查]",
        flow_en="R[Audit clean repositories] --> I[Inject multiple bugs]\n  I --> O[Minimal reversions and isolated attribution]\n  O --> D[Difficulty tiers and training]\n  D --> S[Multi-file solver]\n  S --> E[Separate execution metric and repair checks]",
        questions=[
            ("patch-not-size","basics","CCI只看仓库有多大吗？","不是。十项特征分成repo、dependency和patch三组，论文中patch组对困难度的贡献最大，且repo系数是条件调整。","教学例：一百万行仓库的一行修复，可以比跨二十文件的修改容易。","Does CCI only measure repository size?","No. Ten features form repository, dependency and patch groups; patch complexity dominates, and the repository coefficient is conditional.","Teaching example: a one-line fix in a million-line repository may be easier than a change spanning twenty files."),
            ("frozen-scale","mechanism","给新任务计算CCI时，为什么不能用新任务重新定标？","特征和组尺度、系数、min-max边界都来自固定参考benchmark；在新任务上重拟合会改变尺度，让不同任务不可比较。","教学例：每批都把最难题压成1，会掩盖第二批整体更难。","Why must new tasks retain the reference scale?","Feature/group scales, coefficients and min-max bounds come from fixed reference benchmarks. Refitting on new tasks changes the scale and prevents comparisons.","Teaching example: mapping every batch's hardest task to1 hides an overall difficulty increase."),
            ("cci-vs-ablation","comparison","CCI和MLE-STAR的消融分数能互换吗？","不能。CCI预测结构困难度，MLE-STAR用执行和validation消融选择值得改的代码块；结构困难不等于模型效果差。","教学例：跨文件修复很难，并不说明该模型validation AUC低。","Can CCI replace MLE-STAR's ablation score?","No. CCI models structural difficulty; MLE-STAR uses execution and validation ablations to choose code changes. Structural difficulty is not model quality.","Teaching example: a difficult cross-file repair does not imply low validation AUC."),
            ("calibration-not-invented","implementation","本地接口为什么不直接输出作者的八benchmark成功率？","完整校准常数没有可加载发布文件；调用方必须给固定参数。合成校准只测试公式，缺截距时成功率返回null，不能补造。","教学例：传入μ=0、σ=1是单测，不是作者拟合参数。","Why does the interface not output the author's fitted success rates?","No loadable complete calibration is released. Callers supply fixed parameters; synthetic calibration tests arithmetic only, and success is null without an intercept.","Teaching example: μ=0 and σ=1 are test inputs, not the authors' fitted constants."),
        ],
    ),
    dict(
        key="looproute", module="system_one.looproute", domain="system-one", id="2611.25363",
        title="Stop Going in Circles:Loop-Triggered Routing for System 1 Decision Agents",
        cn_title="LoopRoute：在重复执行前拦截，让LLM只接管两步",
        author="Zeming Yu", org="Sichuan University", published="2026-11-19T02:01:59Z",
        tier="l1_mechanism", topic="按需决策", code=None, license=None,
        card="system-one/adaptive-decisions", peer="foundation-models:selective-reasoning",
        peer_path="system-one/2610.19644-selective-reasoning/README.md",
        page=4, figure="Figure 2", crop=[60,65,540,333],
        locations=["§3 Eq.2-5", "Appendix C public keys and counters", "Table2 / Table9", "§4.5 irreversible errors"],
        method="System One决策模型能快速选动作，但局部选择正确不保证长任务完成。LoopRoute默认把控制权交给冻结Jev；只有同一公开状态下的同一动作已经执行两次，才拦截第三次提案，让LLM按实际环境反馈接管最多两步，然后无额外恢复测试地交回Jev。后续再次卡住可再次接管。",
        method_en="Fast System One action selection does not guarantee long-task completion. LoopRoute normally gives control to frozen Jev. After the same action has executed twice under the same public state, it intercepts the next proposal and lets an LLM take at most two feedback-driven actions. Control then returns without a separate recovery test; later loops can trigger another takeover.",
        mechanism="状态key不含不断增长的history或step。ALFWorld用已确认事实和排序后的可行动作；MapReader用当前动作回应、房间描述和inventory；TextWorld用房间、inventory和候选ID到命令映射。ALFWorld只累计决策模型执行，新事实或接管结束会清空；另外两者累计两种policy的执行并保持到episode结束。被拦截提案既不占环境步，也不更新计数。",
        mechanism_en="Keys exclude growing history and step counters. ALFWorld uses confirmed facts and sorted admissible actions; MapReader uses the action response, room description and inventory; TextWorld uses room, inventory and the candidate-ID/command map. ALFWorld counts only decision-policy executions and clears on new information or takeover completion. The other adapters count both policies and retain counts throughout the episode. Intercepted proposals consume no environment step and update no count.",
        formula=r"r_t=\mathbf1[N_t(k_t,\hat a_t)\ge2],\qquad a_t=\begin{cases}\pi_\ell(x_t),&b_t>0\ \mathrm{or}\ r_t=1,\\\pi_f(x_t),&\mathrm{otherwise},\end{cases}\qquad B=2.",
        result="原文在ALFWorld134题、MapReader100题、Cooking100题及7个LLM上报告相对独立Jev的平均成功率增益21.0%、60.1%、30.1%；这里不是与全LLM策略相比。全LLM仍可能更准：GPT-6-Astra Cooking为100/100，路由为83/100。时间统计是累计API请求时间，不是端到端wall-clock；部分split参与早期探索，原文承认不是完全未触碰的开发外测试。未报告生产A/B。",
        result_en="On134 ALFWorld,100 MapReader and100 Cooking tasks across seven LLMs, the reported mean gains over standalone Jev are21.0%,60.1% and30.1%; these are not improvements over full LLM control. Full LLM control can remain more accurate: GPT-6-Astra solves100/100 Cooking tasks versus83/100 routed. Timing sums API request durations rather than end-to-end wall-clock. Some splits informed earlier exploration, so the paper does not claim untouched development-free tests. No production A/B is reported.",
        local="本地执行公开状态key、pending decision/实际执行分离、第三次提案拦截、准确两步接管及各benchmark计数规则。只接受显式公开字段，不接收gold、奖励或成功标签；new_information由可信外部ALFWorld适配器提供，本地不假装语义核实事实。没有Jev/LLM backend、benchmark环境或实际API请求；控制轨迹只证明路由规则，不证明任务成功率。",
        local_en="The local kernel executes public-state keys, separate pending decisions and actual executions, third-proposal interception, exact two-action takeovers and benchmark-specific counters. It takes declared public fields, not gold/reward/success labels. A trusted external ALFWorld adapter supplies new_information; semantic fact verification is not implemented. There is no Jev/LLM backend, benchmark environment or API request. Controlled traces validate routing rules, not task success.",
        controls="负控区分相同动作但不同状态、未执行提案和真实执行；拒绝未提交transition就再次route，防止重试被当执行。测试ALFWorld不计LLM动作、接管结束清空，以及MapReader/TextWorld计两种动作且不清空。终止立即结束接管；共享key拒绝history/step/gold附加字段。",
        controls_en="Controls distinguish the same action in different states, proposals and executions. Routing again before recording a transition fails, preventing retries from counting as execution. Tests cover ALFWorld excluding LLM actions and clearing at handoff, versus both-policy persistent counters elsewhere. Termination immediately ends takeover; public-key schemas reject added history/step/gold fields.",
        cost="完整矩阵包含334任务、7个前沿LLM、全控制/路由比较、六个额外决策模型与多组消融，需真实Jev/API和多环境长rollout。单卡不能等价替代这些服务及调用费用，因此完整实验高成本不跑；只执行秒级CPU路由核，不下载模型，不调用付费API。",
        cost_en="The full matrix spans334 tasks, seven frontier LLMs, full/routed comparisons, six additional decision models and ablations with real Jev/API services and long environment rollouts. One GPU cannot substitute those services or charges. Full experiments are not run; only seconds-scale CPU routing controls execute without models or paid APIs.",
        compare="Selective Reasoning依据共享读出、benefit gate和答案分布确定性，决定何时生成/读取/停止推理；LoopRoute依据真实环境状态-动作复现，决定是否把控制权短暂交给另一policy。前者的高certainty不代表环境已进展，后者的未重复也不保证动作正确。",
        compare_en="Selective Reasoning uses shared readout, a benefit gate and answer-distribution certainty to start, read and stop reasoning. LoopRoute uses recurrence of executed public state/action pairs to hand control briefly to another policy. High certainty is not environment progress, and absence of recurrence is not action correctness.",
        flow_cn="J[Jev公开状态提案] --> R{已执行同一对两次}\n  R -->|否| E[执行并更新计数]\n  R -->|是| I[丢弃提案不占步]\n  I --> L[LLM最多两步实际反馈]\n  L --> J",
        flow_en="J[Jev proposal from public state] --> R{Pair already executed twice}\n  R -->|No| E[Execute and update counters]\n  R -->|Yes| I[Discard proposal without a step]\n  I --> L[At most two feedback-driven LLM actions]\n  L --> J",
        questions=[
            ("pair-not-action","basics","为什么不能只统计动作重复？","同一动作在不同状态下可能必要。论文统计选定公开状态key和动作的组合，且key不含永远变化的step/history。","教学例：在两个房间各look一次不等于同地卡死。","Why not count repeated actions alone?","The same action may be needed in different states. Recurrence uses a public state/action pair, excluding ever-changing step/history.","Teaching example: looking once in each of two rooms is not a loop at one location."),
            ("third-proposal","mechanism","阈值为2时，第二次动作就被拦截吗？","不是。计数是已执行次数：前两次执行，第三次提案才拦截且不计环境步，随后LLM的第一步已经消耗两步接管预算之一。","教学例：look、look之后再提look，改为LLM的open，余下一步。","Does threshold2 intercept the second action?","No. It counts completed executions: two run, then the third proposal is intercepted without an environment step. The first LLM action consumes one of two takeover slots.","Teaching example: after look/look, another look is intercepted for LLM open, leaving one slot."),
            ("recurrence-vs-certainty","comparison","LoopRoute和Selective Reasoning都省推理，证据一样吗？","不一样。一个看环境中的重复执行，另一个看冻结读出与推理收益/确定性；重复不是低置信度，高置信度也不等于任务有进展。","教学例：模型非常确信地反复开一个锁住的门，仍应触发循环路由。","Does it use the same evidence as Selective Reasoning?","No. LoopRoute observes recurring executions; Selective Reasoning uses frozen readout and benefit/certainty. Recurrence is not uncertainty, and certainty is not progress.","Teaching example: confidently reopening a locked door can still trigger recurrence routing."),
            ("adapter-specific-counters","implementation","能给三个环境共用一套重置规则吗？","不能。ALFWorld只计决策模型动作，并在新事实或接管结束清空；MapReader/TextWorld计两种policy动作且保持整局。公共的是触发和有限接管结构。","教学例：LLM在同一MapReader状态执行open两次，会被后续计数看到；ALFWorld不累计它们。","Can all environments share one reset rule?","No. ALFWorld counts decision-model actions and clears on new information or handoff. MapReader/TextWorld count both policies throughout the episode. Only the trigger/bounded-handoff framework is shared.","Teaching example: two LLM open actions count in MapReader but not in ALFWorld."),
        ],
    ),
    dict(
        key="grepmem", module="agent_research.grepmem", domain="agent-research", id="2611.25123",
        title="Forget Freely, Grep Later: Lossless, Index-Free Memory for Long-Horizon LLM Agents",
        cn_title="GrepMem：压缩工作上下文，但保留可grep的原始历史",
        author="Ziyan Yang", org="University of Southern California", published="2026-11-18T20:02:57Z",
        tier="l1_mechanism", topic="记忆与技能", code="https://github.com/limenlp/GrepMem/tree/b7e3744c2f7489feac4060b379be6936960dc7bd", license="MIT",
        card="agent-research/memory-and-skills", peer="agent-research:memgpt",
        peer_path="agent-research/2310.08560-memgpt/README.md",
        page=3, figure="Figure 2", crop=[60,65,540,357],
        locations=["§3 Algorithm1", "§3.1-3.2", "Appendix A/B grep format", "Appendix D Table4 compute"],
        method="GrepMem把有限工作上下文和完整历史分开：压缩时只把活跃上下文换成系统提示、任务与摘要，原始消息、工具调用/输出和摘要仍追加到纯文本日志。第一次压缩之后才开放grep_history，让模型按需用大小写不敏感正则取回遗漏细节。不需要embedding、索引或知识抽取，但“lossless”只指原日志保留，不代表模型每次都能找对或答对。",
        method_en="GrepMem separates bounded working context from complete history. Compaction replaces active context with the system prompt, task and summary, while original messages, tool calls/results and summaries remain in an append-only text log. Only after first compaction can the policy use case-insensitive grep_history to recover omitted details. No embeddings, index or extraction are required. Lossless describes log retention, not guaranteed retrieval or answers.",
        mechanism="grep按原始记录头与行号返回最早匹配，默认10条、最多30条，offset跳过匹配行而非记录；前后context默认1行、最多3行。旧grep结果仍留在原日志，但搜索跳过它们以免递归重复。单次输出上限6K字符，围绕匹配裁到300字符并在完整match边界停止，返回继续offset；非法正则或超过10秒都返回错误。",
        mechanism_en="Search returns oldest matches under original record headers and line numbers:10 by default, at most30, with an offset over matching lines rather than records and up to three context lines. Prior grep outputs remain logged but are skipped by searches to avoid recursive duplication. Responses cap at6K characters, clip lines around matches to300 characters, stop at whole matches and return a continuation offset. Invalid regexes and searches exceeding ten seconds return errors.",
        formula=r"L_{t+1}=L_t\Vert(a_t,o_t,s_t),\qquad c_{after}=({system},{task},s_t),\qquad retrieve(q)=\operatorname{regex}_i(q,L_t\setminus\text{prior grep outputs}).",
        result="作者用Qwen3.5-9B在五种记忆策略下训练，GrepMem在ContextBench达到95-97%，有损基线最高21%；BCP-Multi比SUPO高8.8个百分点，比MemGPT高7.0点。ContextBench耗用token约为MemGPT的29%。这些是作者训练后测量，token统计包含全部prompt和生成调用，不是本地regex吞吐或磁盘节省。未报告生产A/B；原始日志仍随交互增长。",
        result_en="With Qwen3.5-9B trained under five memory strategies, the paper reports95-97% ContextBench accuracy versus at most21% for lossy baselines, and gains of8.8 points over SUPO and7.0 over MemGPT on BCP-Multi. ContextBench token use is about29% of MemGPT's. These are author post-training measurements over all prompt/generated calls, not local regex throughput or disk savings. No production A/B is reported; the raw log still grows with interaction.",
        local="本地实现append-only记录、显式摘要压缩、第一次压缩后的grep准入、正则/分页/上下文/原行号、跳过旧grep输出与字符上限。正则在隔离子进程内运行并用硬timeout终止，仅接收输入文本而不打开路径。摘要由调用方明确提供；没有LLM摘要器、GRPO、问题回答或真实历史接入。只对合成公开观察做控制测试，不读取本机Codex会话，也不把字符串检索当Agent能力。",
        local_en="The local substrate implements append-only records, explicit-summary compaction, post-compaction grep admission, regex/pagination/context/original line numbers, recursive-output exclusion and character limits. Regexes run in a separate worker with a hard timeout over supplied text, never paths. Summaries are explicit caller inputs. There is no LLM summarizer, GRPO, question answering or real-history integration. Tests use synthetic public observations and never read local Codex sessions; string retrieval is not agent capability.",
        controls="控制测试验证摘要可遗漏原始细节而日志仍保留、只计原始匹配而不递归grep输出、大小写无关、连续offset不漏页；长行与多匹配验证6K上限，灾难性回溯正则会终止worker，随后正常查询仍可用。论文的模型turn预算、自动token估计与forced-answer调用不在这个存储工具组件内，不捏造自动压缩策略或训练效果。",
        controls_en="Controls check omitted summary details remain in the log, grep outputs do not duplicate original matches, case-insensitive search and continuation offsets work, and long lines/many hits respect6K. Catastrophic regex backtracking terminates only the worker and a later normal query still works. Model-turn budgets, token estimation and forced-answer calls are outside this storage/tool slice; no automatic compression policy or training gain is fabricated.",
        cost="原文每次训练使用24张H100（8 trainer、16 rollout），另有共享3卡dense retriever，合计约6000 H100小时，4000个episode、9B模型。明显超出单卡预算，完整训练/评测不复现，不下载模型和14.9M文档；本地只运行秒级CPU日志/检索控制。",
        cost_en="Each paper run uses24 H100s (8 trainer,16 rollout) plus a shared three-GPU dense retriever; total training is about6,000 H100-hours over4,000 episodes and a9B model. Full training/evaluation is not reproduced on the single-GPU budget; no model or14.9M-document corpus is downloaded. Only seconds-scale CPU log/retrieval controls run.",
        compare="MemGPT以分层内存、page-out/page-in与模型工具调用管理归档；GrepMem不预先抽取归档结构，保留原始轨迹并做词法搜索。两者都可压缩工作上下文，但GrepMem没有减少原始日志占盘；模型是否会选对检索词仍需训练与真实任务评价，本地固定key的旧MemGPT诊断也不能作能力对照。",
        compare_en="MemGPT manages layered memory and archival paging through model tool calls. GrepMem avoids a pre-extracted archive and lexically searches raw trajectories. Both can compact active context, but GrepMem does not reduce raw-log storage. Selecting useful search terms still needs training and real task evaluation; the older local fixed-key MemGPT diagnostic is not a capability baseline.",
        flow_cn="M[消息与工具输出] --> C[有限工作上下文]\n  M --> L[完整追加日志]\n  C --> S[调用方摘要与重置]\n  S --> G[首次压缩后开放grep]\n  G --> L\n  L --> R[带行号分页结果]\n  R --> C",
        flow_en="M[Messages and tool outputs] --> C[Bounded working context]\n  M --> L[Complete append-only log]\n  C --> S[Caller summary and reset]\n  S --> G[Enable grep after first compaction]\n  G --> L\n  L --> R[Paginated results with line numbers]\n  R --> C",
        questions=[
            ("context-not-disk","basics","GrepMem会让原始会话日志越来越小吗？","不会。压缩的是工作上下文，消息、工具输出和摘要仍追加到完整日志；lossless是保留内容，不是节省原始日志磁盘。","教学例：摘要省略订单号后可以grep找回，但原始订单文本仍占空间。","Does GrepMem shrink the raw conversation log?","No. It compacts working context while retaining messages, tool results and summaries in a growing log. Lossless means retention, not raw-log disk reduction.","Teaching example: a summarized-away order ID can be recovered because the original text still occupies storage."),
            ("grep-after-compact","mechanism","为什么grep结果本身不再参与下次搜索？","它只是旧内容的复制，递归检索会膨胀重复命中。原输出仍被记录，但grep跳过该类记录；工具在第一次压缩后才开放。","教学例：第一次查到Alpha，第二次仍只计算原始Alpha，而非再加一份引用。","Why exclude earlier grep outputs from later searches?","They copy earlier content and would recursively inflate matches. They remain logged but are skipped, and grep is enabled only after first compaction.","Teaching example: after finding Alpha once, a second query counts the original Alpha, not its quoted copy."),
            ("raw-vs-layered","comparison","它和MemGPT的记忆结构有什么不同？","MemGPT分层管理与换入换出，GrepMem保留原始文本、按正则取回而不建语义索引；两者都不能仅凭存储单测宣称模型会正确回忆。","教学例：grep订单编号不要求先把订单提炼成一条结构化记忆。","How does its memory differ from MemGPT?","MemGPT manages layers and paging; GrepMem preserves raw text and retrieves through regex without a semantic index. Neither storage unit test proves model recall.","Teaching example: grepping an order ID needs no prior extraction into a structured memory entry."),
            ("bounded-regex","implementation","实现grep工具时只加max_matches够吗？","不够。还需要匹配行offset、最多3行context、6K字符上限、300字符行裁剪、非法正则错误和10秒终止；坏正则不能卡住整个Agent。","教学例：带行尾锚点的嵌套重复模式，在长a串后接不匹配字符时可能灾难回溯；搜索worker应超时，正常查询仍能继续。","Is max_matches enough to bound the tool?","No. It also needs match offsets, up to three context lines,6K output,300-character line clipping, regex errors and a ten-second stop. A bad pattern must not stall the whole agent.","Teaching example: a nested repetition with an end-of-line anchor may backtrack catastrophically on a long run of a characters followed by a nonmatching character. The worker should time out while normal queries remain usable."),
        ],
    ),
]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n")


def main():
    import fitz
    from english_learning_sources import question_units

    questions, overlays, reviews, proposals = {}, {}, [], []
    for p in PAPERS:
        key, aid, domain = p["key"], p["id"], p["domain"]
        identity = f"{domain}:{key}"
        folder = ROOT/f"docs/{domain}/{aid}-{key}"
        assets = folder/"assets";assets.mkdir(parents=True,exist_ok=True)
        source = ROOT/f".cache/nov20-latest/agent-primary/{aid}v1.pdf"
        source_sha = hashlib.sha256(source.read_bytes()).hexdigest()
        pdf = fitz.open(source)
        image = assets/"paper-figure-01.png"
        pdf[p["page"]-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(p["crop"])).save(image)
        image_sha = hashlib.sha256(image.read_bytes()).hexdigest()
        write(assets/"provenance.json", {"schema_version":1,"reviewed_on":DATE,"figures":[{
            "file":image.name,"paper_id":aid,"version":"v1","figure":p["figure"],
            "source_url":f"https://arxiv.org/pdf/{aid}v1#page={p['page']}",
            "paper_url":f"https://arxiv.org/abs/{aid}v1","source_kind":"fixed_version_pdf_crop_rendered_png",
            "source_sha256":source_sha,"asset_sha256":image_sha,"image_sha256":image_sha,
            "page":p["page"],"crop_points":p["crop"],"render_dpi":144,"caption_included":True,
            "scientific_content_modified":False,"visual_review_done":True,
            "attribution":"Copyright belongs to original authors. Original figure and caption, not local evidence.",
            "license":"See original arXiv source; no new license granted."}]})
        code_cn = f"[原作者仓库固定提交]({p['code']})；{p['license']}" if p["code"] else "固定v1及本轮核对来源未发现可核验的论文专用公开方法源码；不把引用依赖算开源。"
        code_en = f"[Fixed author repository commit]({p['code']}); {p['license']}" if p["code"] else "No paper-specific public method source verified in fixed v1 and reviewed sources; cited dependencies are not a release."
        command = f"PYTHONPATH=src python -c 'from auto_research.{p['module']} import diagnostic; print(diagnostic(42))'"
        peer_link = os.path.relpath(ROOT/"docs"/p["peer_path"],folder)
        local_code = f"src/auto_research/{p['module'].replace('.','/')}.py"
        stamp = p["published"].replace("T"," ").replace("Z"," UTC")
        cn = f'''# {p["cn_title"]}

[English](README-en.md)

> **component_only / {p["tier"]}；不是模型或Agent能力复现。** 完整实验成本过高，不复现（审查 DONE）；不作为Evolve晋级证据。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [{p["title"]}](https://arxiv.org/abs/{aid}v1)；[固定v1 PDF](https://arxiv.org/pdf/{aid}v1) |
| 一作机构 / 公司 / 学校 | {p["author"]}，{p["org"]} |
| 首次公开日期 | **{stamp}**；11月20日公告/审查不等于首发 |
| 原作者代码 | {code_cn} |
| 本地 Adapter / key | `{key}`；`adapter=null`，未接入Evolve |
| 本地复现代码 | `{local_code}` |

## 原始论文总结

### 背景与主要改动

{p["method"]}

{p["mechanism"]}

### 架构与流程

```mermaid
flowchart LR
  {p["flow_cn"]}
```

<!-- paper-figure:start -->
### 原论文关键图

![{key} {p["figure"]}](assets/paper-figure-01.png)

固定v1 PDF第{p["page"]}页{p["figure"]}及原图注；仅裁留白和无关正文，未改科学内容。图片来自[原论文](https://arxiv.org/pdf/{aid}v1#page={p['page']})，版权归原作者所有；不是本地结果。[资产来源](assets/provenance.json)。
<!-- paper-figure:end -->

### 核心公式

$$
{p["formula"]}
$$

### 论文离线与线上效果

{p["result"]}

## 本地复现

### 数据协议与代码映射

{p["local"]}

```bash
{command}
PYTHONPATH=src python -m pytest tests/test_nov20_agent_components.py -q
```

本轮统一冻结源码后由批次runner生成[三种子CPU诊断](metrics/component-cpu-seeds42-44.json)；合成控制值不是任务成功率。

### 结果、负控与边界

{p["controls"]}

同主题实读对照：[{p["peer"]}]({peer_link})。{p["compare"]}

### 高成本完整实验

{p["cost"]} **成本过高，不复现（审查 DONE）**。此终态不自动重试、不进入完整实现队列，不阻塞其他交付；低成本组件通过不证明完整论文效果。
'''
        (folder/"README.md").write_text(cn)
        cn_sha=hashlib.sha256(cn.encode()).hexdigest()
        en=f'''# {p["title"]}

<!-- source-sha256: {cn_sha} -->

[简体中文](README.md)

> **component_only / {p["tier"]}; not model or agent capability replication.** Full experiments are too costly and not reproduced (review DONE). No Evolve promotion evidence.

## Paper information

| Field | Value |
| --- | --- |
| Paper link | [{p["title"]}](https://arxiv.org/abs/{aid}v1); [fixed v1 PDF](https://arxiv.org/pdf/{aid}v1) |
| First-author institution / company / school | {p["author"]}, {p["org"]} |
| Original publication date | **{stamp}**; November20 announcement/review is not first publication |
| Original author code | {code_en} |
| Local Adapter / key | `{key}`; `adapter=null`, not integrated with Evolve |
| Local reproduction code | `{local_code}` |

## Original paper summary

### Background and main changes

{p["method_en"]}

{p["mechanism_en"]}

### Architecture and flow

```mermaid
flowchart LR
  {p["flow_en"]}
```

### Original paper figure

![{key} {p["figure"]}](assets/paper-figure-01.png)

Fixed v1 PDF page{p["page"]}, {p["figure"]} with original caption. Only whitespace and unrelated body text are cropped; scientific content is unchanged. Copyright belongs to the original authors. [Source](https://arxiv.org/pdf/{aid}v1#page={p['page']}) · [Provenance](assets/provenance.json). Not local evidence.

### Core equations

$$
{p["formula"]}
$$

### Reported offline and online results

{p["result_en"]}

## Local reproduction

### Data protocol and code mapping

{p["local_en"]}

```bash
{command}
PYTHONPATH=src python -m pytest tests/test_nov20_agent_components.py -q
```

After the shared source freeze, the batch runner writes [three-seed CPU diagnostics](metrics/component-cpu-seeds42-44.json). Synthetic control values are not task success rates.

### Results, negative controls and limits

{p["controls_en"]}

Reviewed same-topic comparison: [{p["peer"]}]({peer_link.replace('README.md','README-en.md')}). {p["compare_en"]}

### High-cost full experiments

{p["cost_en"]} **Too costly; not reproduced (review DONE).** This is terminal, not an automatic retry or full-implementation queue. Passing the cheap slice does not establish the paper's full results.
'''
        (folder/"README-en.md").write_text(en)
        spec={"key":key,"domain":domain,"title":p["title"],"first_author":p["author"],
              "first_author_affiliation":p["org"],"published_at":p["published"],"published":p["published"][:10],
              "announced_on":DATE,"paper_url":f"https://arxiv.org/abs/{aid}v1",
              "reviewed_version":"v1","reviewed_arxiv_id":aid+"v1","reviewed_version_url":f"https://arxiv.org/pdf/{aid}v1",
              "detail_path":f"{domain}/{aid}-{key}/README.md","topic":[p["topic"],key],
              "verified_priority_organizations":["Google"] if key=="buggymle-cci" else [],
              "code":p["code"],"code_status":code_cn,"code_license":p["license"],"adapter":None,
              "priority":"P0" if key=="buggymle-cci" else "P1","intake_class":"newly_announced",
              "implementation_status":"component_only","local_operator":f"auto_research.{p['module']}.diagnostic",
              "local_command":command,"evaluation_tier":p["tier"],"diagnostic_only":True,
              "promotion_eligible":False,"evolve_integrated":False,"requires_gpu_validation":False,
              "gpu_validation_passed":False,"gpu_validation_artifact":None,"review_done":True,
              "full_experiment_review_done":True,"full_experiment_status":"not_reproduced_high_cost",
              "review_resolution":"not_reproduced_high_cost","automatic_retry":False,"automatic_implementation_queue":False,
              "cost_assessment":{"source":f"https://arxiv.org/pdf/{aid}v1","available_resource":"one A100 or A30, or local Mac",
                                 "basis":p["cost"],"decision":"成本过高，不复现（审查 DONE）；仅低成本CPU组件。"},
              "summary":p["method"],"fidelity_note":p["local"],"method_source_sha256":source_sha}
        write(ROOT/f"src/auto_research/paper_specs/catalog/{domain}/{key}.json",spec)
        bank=[]
        for qid,level,q,a,e,eq,ea,ee in p["questions"]:
            row={"id":qid,"level":level,"question":q,"answer":a,"example":e,"source_sections":HEADINGS,"added":DATE}
            bank.append(row)
            unit=question_units({identity:[row]})[f"qa/{identity}/{qid}"]
            overlays[f"qa/{identity}/{qid}"]={"source_sha256":unit.source_sha256,"reviewed":True,
                                             "fields":{"question":eq,"answer":ea,"example":ee}}
        questions[identity]={"questions":bank}
        peer_sha=hashlib.sha256((ROOT/"docs"/p["peer_path"]).read_bytes()).hexdigest()
        q=next(q for q in bank if q["level"]=="comparison")
        qe=next(q for q in p["questions"] if q[1]=="comparison")
        proposals.append({"paper":identity,"target_card":p["card"],"source_revisions":{identity:cn_sha,p["peer"]:peer_sha},
                          "comparison":{"position":p["method"],"tradeoff":p["compare"],"sections":HEADINGS},
                          "analysis":{"title":p["cn_title"],"body":p["mechanism"]+p["controls"],"papers":[identity,p["peer"]]},
                          "question":{"id":"cross-nov20-"+key,"question":q["question"],"answer":q["answer"],"example":q["example"],"papers":[identity,p["peer"]]},
                          "update":{"date":DATE,"papers":[identity,p["peer"]],"summary":p["local"]+" 完整实验高成本不复现。"},
                          "english":{"comparison":{"position":p["method_en"],"tradeoff":p["compare_en"]},
                                     "analysis":{"title":p["title"],"body":p["mechanism_en"]+" "+p["controls_en"]},
                                     "question":{"question":qe[5],"answer":qe[6],"example":qe[7]},
                                     "update":p["local_en"]+" Full experiments not reproduced."}})
        reviews.append({"id":aid,"key":key,"identity":identity,"published_at":p["published"],"announced_on":DATE,
                        "first_author":p["author"],"first_author_affiliation":p["org"],"source_url":f"https://arxiv.org/pdf/{aid}v1",
                        "source_sha256":source_sha,"locations":p["locations"],"code":p["code"],"code_status":code_en,
                        "implementation_status":"component_only","evaluation_tier":p["tier"],"scope":p["local_en"],
                        "cost_basis":p["cost_en"],"full_experiment_status":"not_reproduced_high_cost",
                        "requires_gpu_validation":False,"review_done":True})
    write(ROOT/"docs/learning/questions/nov20-latest-agent.json",{"schema_version":1,"papers":questions})
    write(ROOT/"docs/en/learning/translations/qa-nov20-latest-agent.json",{"schema_version":1,"units":overlays})
    write(AUDIT/"deep-dive-proposals-agent.json",{"schema_version":1,"reviewed_on":DATE,"integration_owner":"root","proposals":proposals})
    write(AUDIT/"agent-review.json",{"schema_version":1,"reviewed_on":DATE,"scope":"Finite three-paper primary-method review: one Nov19 first release, two Nov18 first-release/Nov20-announcement overlap additions; no exhaustive claim.",
                                      "implementation_preflight_completed":True,"available_resource":"single A100 or A30 or Mac; only CPU control kernels here",
                                      "reviews":reviews,"p2_dispositions":[]})
    print("Authored three bilingual papers,12 bilingual questions and3 same-topic proposals; no shared bank integration.")


if __name__=="__main__":
    main()
