"""Owned Nov24 Agent primary captures, authored bilingual papers and proposals.

No shared catalog/registry/ledger/learning-bank writes. No models, datasets,
teacher calls, live judges or actual Agent rollouts are launched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov24-latest/agent-primary"
AUDIT = ROOT / "docs/research-audits/nov24-latest"
DATE = "2026-11-24"
HEADINGS = ["背景与主要改动", "核心公式", "数据协议与代码映射", "同主题比较与边界", "完整实验与成本决定"]
PAPERS = [
    dict(key="ooas", module="ooas", id="2611.30405", author="Hao Luan",
         title="Optimistic Online Learning for Coding Agents with Aggregate Feedback",
         org="National University of Singapore, School of Computing / Institute of Data Science",
         published="2026-11-23T10:05:39Z", topic="Agent 策略学习", card="agent-research/agent-policy-learning",
         peer="agent-research:acting-to-learning", peer_path="agent-research/2611.27159-acting-to-learning/README.md",
         code=None, page=5, figure="Algorithm 1", crop=[65, 65, 550, 278]),
    dict(key="transport-safe-audit", module="transport_safe_audit", id="2611.30742", author="Yulliwas Ameur",
         title="Transport-Safe Evaluation of LLM Agents: Trajectory-Dependent Judge Error and Anytime-Valid Auditing",
         org="Efrei Research Lab, Université Paris-Panthéon-Assas / CEDRIC, Conservatoire National des Arts et Métiers",
         published="2026-11-23T14:19:52Z", topic="评测与可靠性", card="agent-research/harness-and-self-improvement",
         peer="agent-research:coevobench", peer_path="agent-research/2611.27116-coevobench/README.md",
         code=None, page=6, figure="Figure 1", crop=[60, 485, 550, 760]),
    dict(key="morse", module=None, id="2611.30011", author="Ce Zhang",
         title="MORSE: Optimizing Streaming Memory Design via Open-World Auto-Research",
         org="Carnegie Mellon University / Northwestern University / University of Illinois Urbana-Champaign / University of Pittsburgh",
         published="2026-11-23T04:11:45Z", topic="执行框架与自改进", card="agent-research/harness-and-self-improvement",
         peer="agent-research:harness2", peer_path="agent-research/2610.14224-harness2/README.md",
         code=None, page=3, figure="Figure 2", crop=[55, 65, 560, 345]),
]
CONTENT = {
"ooas": dict(
    cn_title="OOAS：只看到任务总回报，也能用逐轮hint学习策略",
    code_cn="固定v1全文未找到本方法专属已核实源码；文内GitHub链接是API文档，引用TACT也不等同本篇开源。",
    code_en="No verified method-specific source release was found in fixed v1. GitHub API documentation and the referenced TACT method are not a release of this paper.",
    method="OOAS把activation steering候选选择建模为逐turn多臂bandit。每轮先见所有候选的reward hint，选一个策略；任务结束只见已选序列的加和reward，不见逐轮贡献。它不是猜哪条编辑会通过隐藏测试，而是在聚合反馈粒度下修正累计hint误差。论文理论要求reward向量、hint和任务划分预先固定、独立于学习者随机数；真实编码Agent的状态依赖轨迹不自动满足该假设。",
    method_en="OOAS models activation-steering selection as a turn-level bandit. Each turn reveals reward hints for all candidate policies; only the selected sequence's aggregate reward arrives at task completion. The method corrects cumulative hint errors without observing individual rewards. Its theory assumes reward vectors, hints and the task partition are fixed independently of learner randomization. Stateful coding-agent trajectories do not automatically satisfy that assumption.",
    mechanism="分布不是softmax：FTRL同时使用Tsallis项和log barrier。turn t把已完成任务score、当前任务此前hint和本轮hint乘已过turn数相加，再求内点最优分布。每任务只抽一次K个Exp(1)噪声，所有turn共享，以argmin ξ/p选臂。整任务都选同一臂k的概率ρ由各turn概率比的最大值计算，不能用边缘概率相乘；只有该事件发生时才以Z/ρ修正此臂，发生切臂则残差修正全0，但所有臂仍加hint之和。Alg2用可观察potential gap的有符号累积触发严格大于阈值的doubling，重启score与gap，不把负gap裁为0。",
    mechanism_en="The distribution is not softmax: FTRL combines Tsallis and log-barrier terms. It uses completed-task scores, previous hints in the current task and the current hint weighted by elapsed turns. A task draws one Exp(1) noise vector shared across all turns and selects argmin noise/probability. The probability rho that arm k wins every turn uses maxima of probability ratios, not products of marginals. Only that event receives residual Z/rho; switched tasks have zero residual correction while every arm still receives accumulated hints. Algorithm2 doubles its threshold when a signed cumulative observable potential gap strictly exceeds it, resetting score and gap rather than clipping negative gaps.",
    formula=r"\psi(p)=2\alpha(\sqrt K-\sum_k\sqrt{p_k})+\beta\sum_k\log\frac1{Kp_k},\quad \rho_{b,k}=\left(\sum_\ell\max_{t\in I_b}\frac{p_{t,\ell}}{p_{t,k}}\right)^{-1},\quad \widehat D_{b,k}=\frac{\mathbf1[A_t=k\ \forall t\in I_b]}{\rho_{b,k}}Z_b.",
    result="作者在Qwen3.5-27B+mini-swe-agent的SWE-V（500题）和TB2（89题）报告adaptive Cap resolve rate65.0%/34.8%，static Cap为62.0%/32.6%；Gate为63.0%/32.6%，static Gate57.0%/30.3%。真实Agent只测Alg2，不把Alg1 oracle误差预算模拟当可观测调参。理论leading regret依赖hint误差，但10^8 turn模拟中的log样式曲线不是任意Agent环境的统一保证。未报告生产线上A/B。",
    result_en="With Qwen3.5-27B and mini-swe-agent, the paper reports adaptive Cap resolve rates of65.0%/34.8% on500 SWE-V and89 TB2 tasks versus62.0%/32.6% for static Cap. Adaptive Gate reaches63.0%/32.6% versus57.0%/30.3%. Only Algorithm2 is evaluated with real agents; Algorithm1's oracle prediction-error budget in simulations is not observable tuning. Hint-dependent theoretical regret and log-like simulated curves are not universal guarantees for arbitrary agent environments. No production A/B is reported.",
    local="独立标准库CPU核实际解FTRL的KKT方程：Gk+α/√pk+β/pk为共同乘子，通过平移score与二分求解，而非softmax替身；实现共享Exp采样、ρ、聚合残差、potential和Alg2重启。begin→choose→finish只接受当前hint和最终aggregate，不接受turn reward向量或gold答案/计划。噪声注入只供数学控制。没有LLM、activation probe、TACT干预、代码执行器、真实任务分数或Evolve映射。数值求根是有公差的float64近似，不声称无限精度理论实现。",
    local_en="The independent standard-library CPU kernel solves FTRL's KKT equations: Gk+alpha/sqrt(pk)+beta/pk share a multiplier, found by score translation and bisection rather than a softmax substitute. It implements shared exponential sampling, rho, aggregate residuals, the potential and Algorithm2 restarts. The begin/choose/finish API receives current hints and one terminal aggregate, not turn reward vectors or gold answers/plans. Injected noise is for mathematical controls only. No LLM, activation probe, TACT intervention, code executor, real-task score or Evolve mapping runs. The float64 root solver has numerical tolerance, not infinite precision.",
    controls="负控覆盖KKT残差、分布平移不变、共享noise的整任务事件概率不等于独立概率乘积、切臂时无残差归因、每turn的hint倍率、任务长度上限、重复begin/finish拒绝、aggregate越界不丢pending状态、保留负potential gap及重启后score归零。使用分析事件分区核对importance权重，不用少量Monte Carlo冒充无偏证明。",
    controls_en="Controls check KKT residuals, translation invariance, shared-noise event probabilities versus independent products, zero residual attribution after switching, elapsed-turn hint weighting, task bounds, lifecycle errors, preserved pending state after invalid aggregates, signed negative gaps and restart resets. Analytic event partitions check importance weighting; a small Monte Carlo run is not advertised as proof of unbiasedness.",
    compare="From Acting to Learning在固定历史池里选SFT action记录，选择后冷启动学生；OOAS在任务执行中选steering臂，并在任务结束后修正hint。前者的梯度相关性不是后者的reward预测，后者的共享noise也不是经验重放的shuffle。两者都必须分开选择信息与最终评测；本地均没有真实Agent能力比较。",
    compare_en="From Acting to Learning selects SFT action records from fixed history pools and cold-starts students. OOAS selects steering arms during execution and corrects hints after each task. Gradient relevance is not a reward hint, and shared task noise is not replay shuffling. Both require separation of selection information from final evaluation; neither local slice compares agent capability.",
    cost="完整Agent矩阵需27B模型、589个真实编码/终端任务、Cap/Gate多臂与baseline，最长256/128turn；完整模拟用10^7–10^8turn、50seeds、最多512臂。单A100/A30或Mac的短时预算不承担此长rollout/多臂研究，完整实验直接终态不复现，不下载checkpoint/benchmark、不调用API或探跑。仅小K/L CPU核，预估秒级，实测以统一runner为准。",
    cost_en="The full campaign uses a27B model,589 real coding/terminal tasks, Cap/Gate multi-arm comparisons and baselines, with up to256/128 turns. Simulations span10^7-10^8 turns,50 seeds and up to512 arms. This long-rollout/multi-arm campaign exceeds the short one-A100/A30-or-Mac budget and is terminally not reproduced. No checkpoints, benchmarks, APIs or trial runs are launched. Only bounded small-K/L CPU controls run, estimated in seconds pending shared-runner timing.",
    flow_cn="A[本轮reward hints] --> B[Tsallis与barrier FTRL]\n  B --> C[任务共享Exp噪声选臂]\n  C --> D[仅任务结束aggregate]\n  D --> E[hint残差重要性校正]\n  E --> F[有符号gap与doubling]\n  F --> B",
    flow_en="A[Current reward hints] --> B[Tsallis plus barrier FTRL]\n  B --> C[Task-shared exponential noise]\n  C --> D[Terminal aggregate only]\n  D --> E[Importance-correct hint residual]\n  E --> F[Signed gap and doubling]\n  F --> B",
    questions=[
        ("aggregate-not-turn","basics","任务完成才有反馈，为什么不能逐轮做普通bandit更新？","因为只观察一项任务总reward，无法知道每轮被选臂各贡献多少；把总reward复制到每轮会改变估计器。OOAS先用hint，再用整任务事件校正。","教学例：两轮分别选A/B后总reward为1，不能据此断定A和B各得1，也不能任意各分0.5。","Why not apply ordinary per-turn bandit updates?","Only one task aggregate is observed; copying it to every turn invents individual rewards. OOAS uses hints and task-level event corrections instead.","Teaching example: choosing A then B and observing total1 does not establish reward1 for both or justify assigning.5 to each."),
        ("shared-event-probability","mechanism","整任务都选同一臂的概率能把各轮pk相乘吗？","不能。每任务共享一组Exp噪声，动作相关；ρ使用跨turn概率比的最大值。独立相乘对应另一种采样，会使importance权重失真。","教学例：两臂概率从(0.3,0.7)变成(0.8,0.2)，共享噪声下A全胜概率0.3，不是0.24。","May all-turn selection probabilities be multiplied?","No. Shared exponential noise correlates choices within a task. Rho uses maxima of cross-turn probability ratios; multiplying marginals assumes different randomization and misweights corrections.","Teaching example: probabilities(.3,.7) then(.8,.2) give all-A probability.3 under shared noise, not.24."),
        ("offline-vs-online","comparison","与From Acting to Learning都做选择，选择的对象和时点相同吗？","不同。旧文选历史action用于后续SFT；OOAS在当前执行turn选steering策略，结束后用aggregate更新。不能用离线gradient score直接替代hint并宣称有同样regret保证。","教学例：挑256条清洁经验是训练数据选择；本轮选Cap=1.5还是2.0是在线干预选择。","Do the two selectors choose the same object at the same time?","No. The earlier paper selects historical actions for SFT; OOAS chooses steering policies online and updates after aggregate feedback. Offline gradient scores do not automatically satisfy its hint/regret assumptions.","Teaching example: choosing256 cleaning records selects training data; choosing Cap1.5 versus2.0 selects a current intervention."),
        ("signed-gap-restart","implementation","potential gap为负应裁成0再累计吗？","不应。Alg2累计有符号gap，只有总值严格超过H才doubling并清零score和gap；改成非负累计改变重启时点和算法。","教学例：已有gap为-2，新gap为3时累计是1，不是3；H=1时等于阈值仍不重启。","Should negative potential gaps be clipped to zero?","No. Algorithm2 accumulates signed gaps and restarts only when the sum strictly exceeds H. Clipping changes restart times and the algorithm.","Teaching example: gap-2 followed by3 sums to1, not3; with H=1, equality still does not restart."),
    ]),
"transport-safe-audit": dict(
    cn_title="Transport-safe audit：校准过的LLM裁判也未必能跨Agent搬用",
    code_cn="固定v1官方TeX与正文未给出可核实的本篇专属公开源码仓库，未找到/未核实；引用统计方法或AgentRewardBench不是本篇代码发布。",
    code_en="No verifiable paper-specific source repository is supplied in fixed-v1 text/TeX. Referenced statistical methods and AgentRewardBench are not a code release for this paper.",
    method="不同Agent产生不同轨迹；即使裁判在给定(X,Y)时看不到Agent身份，其sensitivity/specificity的平均值也会随成功/失败轨迹分布改变。论文连接scalar transport偏差、支持与识别、随机人工audit、anytime monitoring和rank sets；这些统计工具本身不是新发明。主要证据是semi-synthetic，公共Agent数据的既有分析未在本文独立重跑，不据此声称轨迹长度有因果作用。",
    method_en="Agents induce different trajectory distributions. Even a judge blind to agent identity given(X,Y) may have different averaged sensitivity/specificity under those distributions. The paper connects scalar-transport bias, support/identification, randomized human auditing, anytime monitoring and rank sets; these statistical tools are not individually new. Evidence is mainly semi-synthetic. Prior public-agent analyses are not independently rerun, and no causal effect of trajectory length is established.",
    mechanism="已知随机audit概率φ有正下界时，AIPW用out-of-fold预测m加R/φ(Y−m)修正；未audit样本只用m，估计值不强裁[0,1]。bounded allocation令φ=min(1,max(φmin,λ√m(1−m)))满足可达预算。在线e-process要求预测函数和audit规则由过去选定、新V到达后求值，当前label不能反过来改它们；目标必须固定且逐任务独立稳定。支持缺失时给outer set而不补造点估计，rank只用严格区间分离而非中点硬排。",
    mechanism_en="With known randomized audit propensities bounded away from zero, AIPW adds R/phi(Y-m) to out-of-fold imputations; unaudited rows use m only, and estimates are not clipped to[0,1]. Bounded allocation uses min(1,max(floor,lambda*sqrt(m(1-m)))) under an attainable budget. Online e-processes require past-chosen prediction/audit functions evaluated at new V, without using the current label. The target must be frozen and stable across independently drawn tasks. Missing support produces outer sets rather than invented point estimates, and ranks use strict interval separation rather than midpoint ordering.",
    formula=r"\widehat\theta=\frac1n\sum_i\left[\widehat m_{-k(i)}(V_i)+\frac{R_i}{\varphi_i}(Y_i-\widehat m_{-k(i)}(V_i))\right],\quad E_t(\theta)=\frac1{2|\Lambda|}\sum_{\lambda\in\Lambda}\left[\prod_{i\le t}(1+\lambda W_i(\theta))+\prod_{i\le t}(1-\lambda W_i(\theta))\right].",
    result="四Agent semi-synthetic主实验中，scalar oracle calibration最大偏差0.245、mean pointwise coverage0.016、完整排名恢复0/250；uniform/design-aware audit AIPW最大偏差<0.003，coverage0.939/0.950。200条稳定模拟stream逐episode反复查看，Wald共同coverage0.535、confidence sequence0.995，后者更宽。它们是模拟覆盖频率，不是新Agent能力或生产线上A/B；真人label被视为参考，不代表无噪声真理。未报告生产线上A/B。",
    result_en="In the four-agent semi-synthetic study, oracle-calibrated scalar correction has maximum bias.245, mean pointwise coverage.016 and exact ranking recovery0/250. Uniform/design-aware audit AIPW has maximum bias below.003 and coverage.939/.950. Across200 stable simulated streams inspected after each episode, joint coverage is.535 for repeated Wald intervals and.995 for the confidence sequence, which is wider. These are simulation frequencies, not new agent capability or production A/B. Human labels are a reference, not proven error-free truth. No production A/B is reported.",
    local="本地是evaluator侧标准库算术：scalar transport偏差、带显式fold声明的AIPW、finite-strata bounded allocation、支持缺失outer set、严格区间rank sets和log-space hedged e-process。plan先提交m与φ再随机决定audit；observe只收已audit的0/1，未audit必须None，并逐episode更新。拒绝换target、未冻结/非独立任务声明和λ不严格小于φmin。仅对预先固定有限θ网格反演，accepted_grid不是连续CS端点，真值不在网格时没有网格覆盖说法。没有nuisance拟合、真人采集、LLM裁判、三judge潜变量模型、cluster bootstrap或live leaderboard；时序/fold声明是外部统计契约，不是恶意调用方不可绕过的安全证明。",
    local_en="The evaluator-side standard-library slice implements scalar bias, AIPW with declared fold provenance, finite-stratum bounded allocation, support outer sets, strict interval rank sets and a log-space hedged e-process. Plan commits m/phi before drawing an audit; observe accepts binary labels only for audited rows and requires None otherwise. Every episode updates. Changed targets, nonfrozen/nonindependent task declarations and lambda not strictly below the positivity floor are rejected. Inversion is only on a predeclared finite theta grid: accepted_grid is not continuous CS endpoints or coverage for off-grid truth. No nuisance fitting, human collection, LLM judge, three-judge latent model, cluster bootstrap or live leaderboard runs. Timing/fold declarations are external statistical contracts, not adversarial information-flow security proofs.",
    controls="精确枚举小型Bernoulli audit设计，验证错误imputation仍design-unbiased；检查AIPW可超1而不裁剪、同fold训练拒绝、预算/positivity/零方差stratum、log-space与直接乘积相同、长stream不溢出、未audit真值拒绝、未知target拒绝、重叠/恰接区间不硬定序。三seed只是数学控制，不是coverage达到0.95的经验估计。",
    controls_en="Exact enumeration of a small Bernoulli audit design checks unbiasedness despite wrong imputation. Controls cover unclipped estimates above1, own-fold rejection, allocation/positivity/zero-variance strata, agreement with direct products, log-space long-stream stability, rejection of unaudited labels and changed targets, and unresolved overlapping/touching intervals. Three seeds are mathematical controls, not an empirical estimate of95% coverage.",
    compare="CoEvoBench保护Selection/Test内容并审计训练血缘，回答候选是否越界及能否泛化；本篇问即使访问隔离正确，LLM judge误差是否能跨轨迹分布transport。二者不能替代：无数据泄漏不等于judge已校准，AIPW也不能消除被评Agent读了gold造成的污染。CoEvo完整系统本地未跑，本篇也没有live judge结果可横比。",
    compare_en="CoEvoBench protects Selection/Test material and audits training lineage, addressing prohibited access and generalization. This paper asks whether judge errors transport across trajectory distributions even when access isolation is correct. Neither substitutes for the other: no leakage does not ensure calibration, and AIPW cannot undo gold contamination of an evaluated agent. There are no local live-judge results to compare with CoEvoBench.",
    cost="论文是CPU统计研究，不能伪称必须GPU。完整allocation研究最多500次重复×500000 episodes（约2.5亿episode级记录），另有250次四Agent、48cell、200×3000step anytime与1000次rank实验；部分target样本量/可执行脚本未给，完整重做总成本无法仅凭元数据廉价核定。按成本门禁不为证明费用启动整套试跑，完整campaign本轮终态不复现；保留秒级小数组/精确设计枚举。无live LLM judge、人类标注费或GPU小时实测，也不补造这些费用。",
    cost_en="This is CPU statistical research, not a study that necessarily requires GPUs. The full allocation campaign reaches500 replications by500000 episodes(about250 million episode records), plus250 four-agent replications,48-cell stress tests,200 by3000-step monitoring streams and1000 rank experiments. Some target sizes/executable scripts are not supplied, so full reproduction cost cannot be cheaply established from metadata. The cost gate closes the full campaign without a costly probe; only bounded small-array/exact-design controls execute. No live-judge, human-labeling or GPU cost is measured or invented.",
    flow_cn="A[轨迹covariates与judge输出] --> B[支持与识别检查]\n  B --> C[已知概率随机audit]\n  C --> D[跨fold AIPW]\n  C --> E[先提交预测再见label]\n  E --> F[log-space e-process]\n  D --> G[outer intervals与rank sets]\n  F --> G",
    flow_en="A[Trajectory covariates and judge verdicts] --> B[Support and identification]\n  B --> C[Known randomized audit probabilities]\n  C --> D[Cross-fit AIPW]\n  C --> E[Commit prediction before label]\n  E --> F[Log-space e-process]\n  D --> G[Outer intervals and rank sets]\n  F --> G",
    questions=[
        ("blind-not-transport","basics","judge不看Agent名字，校准就能通用吗？","不一定。它可在给定轨迹X与成功Y时blind，但不同Agent的成功/失败轨迹X分布不同，导致平均sensitivity/specificity改变；scalar纠正于是有transport偏差。","教学例：judge对短轨迹很准、对长失败常误判；更常生成长轨迹的Agent即使匿名也不能直接用旧平均错误率。","Does hiding agent names make calibration universal?","No. Conditional blindness given trajectoryX and successY does not fix the distribution of X within successes/failures. Different distributions change averaged error rates and bias scalar transport.","Teaching example: a judge accurate on short traces but unreliable on long failures still treats an anonymous long-trace agent differently."),
        ("audit-correction-not-clipping","mechanism","AIPW估计超过1应强行裁到1吗？","不能把裁剪当该design-unbiased估计器。R/φ校正可使有限样本超出[0,1]，但其随机audit期望正确；裁剪会改变期望。报告不确定性与界，不伪造合理外观。","教学例：m=0、φ=0.1、抽中且Y=1时单条校正为10；未抽中为0，期望仍是1。","Should AIPW estimates above1 be clipped?","Not while claiming this design-unbiased estimator. Inverse-propensity correction may leave[0,1] in finite samples; clipping changes its expectation. Report uncertainty rather than cosmetically forcing a probability.","Teaching example: m=0,phi=.1 and auditedY=1 give contribution10; unaudited contribution0 still gives expectation1."),
        ("calibration-vs-contamination","comparison","与CoEvo的数据隔离审计，哪一个能替代哪一个？","都不能。CoEvo限制任务/答案访问和训练血缘；本篇校正裁判测量误差。没有泄漏仍可judge偏差；校正judge也不能让读过gold的Agent重新成为合格评测对象。","教学例：一个没见测试答案的Agent被错误裁判低估，需要audit；一个见过测试答案的Agent即使judge完全准确也已污染。","Can measurement audits replace CoEvo-style data isolation?","No. Data isolation concerns access/lineage; this method concerns judge measurement error. A clean agent can still be misgraded, while perfect grading cannot validate a gold-contaminated agent.","Teaching example: an unseen-test agent may need judge auditing; a test-answer-exposed agent remains contaminated even under a perfect judge."),
        ("predictable-fixed-target","implementation","看到当前label后再调audit概率，或者更新Agent后继续同一e-process，可以吗？","不可以。预测/audit规则须依赖过去，当前label不能回流；稳定target要求冻结Agent与独立任务。更新模型、混Agent或固定小样本无放回抽取不自动满足。网格反演也不能冒充连续CS。","教学例：先定φ=0.2再随机audit合法；看到失败才把本条φ改成1会破坏已声明设计概率。","May the current label change its propensity, or an updated agent continue the same process?","No. Prediction/audit rules must be past-measurable, and a stable target requires a frozen agent with independently drawn tasks. Updated/mixed agents or small fixed-benchmark sampling are not automatically covered. Grid inversion is not continuous CS inversion.","Teaching example: committing phi=.2 before random auditing is valid; changing that episode's phi to1 after seeing failure invalidates the declared design."),
    ]),
"morse": dict(
    cn_title="MORSE：用反复出现的记忆失败驱动在线研究与工具扩展",
    code_cn="固定v1与[作者项目页](https://zhangce01.github.io/morse/)未找到可核实的公开方法代码仓库；项目展示页不是源码发布，不把Editor读过的第三方工具当本方法开源。",
    code_en="No verifiable public method repository was found in fixed v1 or the [author project page](https://zhangce01.github.io/morse/). A project showcase and third-party tools read by the editor are not a method source release.",
    method="流式视频记忆必须在不知道未来query时单遍决定保留哪些帧。MORSE让冻结VLM外的Editor从训练trace归因反复失败，主动搜索论文、model cards与code，再改write/read harness；缺感知能力可请求新模型，但需host核查license、训练来源和成本后部署。核心是研究—实现—验证的自主Editor与可扩展服务，不是固定候选列表或门控公式本身。",
    method_en="Streaming memory must retain evidence in one pass before future queries are known. MORSE's editor diagnoses recurring failures in training traces, researches papers/model cards/code and edits write/read harnesses around a frozen VLM. Missing perception capabilities can be requested but require host review of licensing, training provenance and cost before deployment. The defining mechanism is the research/implementation/validation editor plus expandable services, not a fixed candidate list or gate formula alone.",
    mechanism="20轮accuracy后5轮efficiency。accuracy要求平均correct-option probability至少增加0.004；efficiency要求延迟≤父代0.9，允许每轮概率/正确数损失0.003/2，同时相对stage-entry累计损失≤0.008/4。都须延迟≤1s、write load≤1、完整validation问题数不变。accuracy可从qualified archive选，efficiency不取archive；合并后必须重新验证。64张persistent帧之外另有16秒近期窗口，text/vector无全局存储上限，不能宣传总memory恒定。Editor只看训练逐题trace及validation聚合；benchmark/答案链接经broker禁止。",
    mechanism_en="Twenty accuracy rounds precede five efficiency rounds. Accuracy requires at least.004 mean correct-option-probability gain. Efficiency requires latency at most.9 of the parent, per-update losses at most.003 probability/two correct answers, and stage-entry cumulative losses at most.008/four answers. Both enforce latency at most1 second, write load at most1 and unchanged validation question counts. Accuracy may select qualified archive entries; efficiency excludes the archive. Merges are revalidated. The64-frame persistent cap is separate from a16-second recent window, and text/vectors have no global cap; total memory is not constant. The editor sees training traces and aggregate validation feedback; the broker blocks benchmark/answer sources.",
    formula=r"M_t=W_H(M_{t-1},x_t;\mathcal T),\quad\hat y=F(q,R_H(M_t,q;\mathcal T)),\quad g_{eff}:\ell(H')\le\rho\ell(H),\ \Delta\bar P\ge-\epsilon,\ \Delta c\ge-\kappa.",
    result="Qwen3-VL8B上作者报告OVO-Bench75.1%、StreamingBench78.9%、StreamBench71.6%，同backbone较次优harness高3.1/2.7/6.3点；OVO平均答复0.30s。训练/validation为780题370streams与388题182streams，测试视频隔离。evolution latency用固定线性服务成本模型，test latency才在单H100实测，两者不能混写成本地计时。未报告生产线上A/B；没有本地Agent测量。",
    result_en="For Qwen3-VL8B, the paper reports75.1% OVO-Bench,78.9% StreamingBench and71.6% StreamBench, beating the next evaluated same-backbone harness by3.1/2.7/6.3 points, with.30-second mean OVO answer latency. Training/validation comprise780 questions on370 streams and388 on182 streams, with test-video separation. Evolution uses fixed linear service-cost estimates; test latency is measured on oneH100. Neither is local timing. No production A/B or local agent measurement is reported.",
    local="仅资料收录与成本审查：固定v1、来源/元数据、访问边界、成本和同主题比较。没有本地算法模块、Editor、研究broker、视频服务、harness代码演化、benchmark、GPU试跑或Evolve operator。不能实现几个gate后称已复现MORSE，也不需要给review-only制造三seed指标或GPU receipt。",
    local_en="Review-only delivery records fixed-v1 sources/metadata, access boundaries, costs and a same-topic comparison. No local algorithm module, editor, research broker, video service, harness evolution, benchmark, GPU trial or Evolve operator is created. Gate arithmetic alone would not reproduce MORSE; review-only disposition requires no invented three-seed metrics or GPU receipt.",
    controls="审查保留估计latency与实测latency、frame cap与无限text/vector、已装服务与实际采用服务、rejected diff复用与重新验证的区别。作者用gold计算validation指标只发生在host/evaluator侧，不允许把gold给Solver/Editor。本地没有通过率或性能负控实测。",
    controls_en="The review distinguishes estimated from measured latency, frame caps from uncapped text/vectors, installed from adopted services, and reused rejected diffs from revalidated candidates. Gold-dependent validation metrics belong to host/evaluator boundaries, not the solver/editor. No local success-rate or performance controls are measured.",
    compare="Harness²固定工具表面，用Propose–Probe–Compose执行对照改当前任务harness，再跨任务保存经验；MORSE在流式记忆设计中把在线文献研究和host批准的感知工具获取纳入搜索，保留当前head迭代。二者不能简化为同一“反思循环”：MORSE的validation概率/成本gate与持续服务扩展有专门契约，Harness²匿名selector也不是其scorer。本地Harness²机制替身与本篇review-only没有可比较Agent分数。",
    compare_en="Harness² improves current-task harnesses through Propose/Probe/Compose execution contrasts and saves cross-task lessons within a fixed tool surface. MORSE adds online literature research and host-approved perception acquisition to streaming-memory design while iterating a persistent head. Their feedback, candidate selection and tool-admission contracts differ. Harness²'s anonymous selector is not MORSE's validation probability/cost scorer. The local Harness² diagnostic and this review-only entry have no comparable agent scores.",
    cost="每个backbone25轮、每轮最多6初始candidate另有merge；三套独立backbone为Qwen2.5-VL7B、Qwen3-VL8B、Qwen3.8-27B，Editor Claude Opus5.5，多种CLIP/OCR/VideoMAE/encoder等服务、780train/388validation与三test视频bench；最多20000service calls/episode、131072context/call。单H100是test计时硬件，不是完整演化耗时预算。相对单A100/A30或Mac的短时任务明显高成本，完整系统终态不复现，不下载模型/视频、不部署服务、不付费调用或试跑。",
    cost_en="Each backbone uses25 rounds with up to six initial candidates per round plus merges. Three separate backbones are Qwen2.5-VL7B,Qwen3-VL8B andQwen3.8-27B, with Claude Opus5.5 editing, multiple CLIP/OCR/VideoMAE/encoder services,780 training/388 validation questions and three test video benchmarks. Host limits allow20000 service calls per episode and131072 context tokens per call. The singleH100 is test-timing hardware, not a complete evolution budget. This clearly exceeds the short one-A100/A30-or-Mac scope; the full system is terminally not reproduced without model/video downloads, services, paid calls or probes.",
    flow_cn="A[训练trace反复失败] --> B[搜索论文模型和代码]\n  B --> C[Editor改记忆write/read]\n  B --> D[host审核感知工具]\n  D --> C\n  C --> E[私有validation聚合gate]\n  E --> F[accuracy后efficiency]\n  F --> A",
    flow_en="A[Recurring training-trace failures] --> B[Research papers models and code]\n  B --> C[Editor revises memory write/read]\n  B --> D[Host reviews perception tools]\n  D --> C\n  C --> E[Private aggregate validation gates]\n  E --> F[Accuracy then efficiency]\n  F --> A",
    questions=[
        ("research-beyond-recall","basics","MORSE比已有闭环harness自改进多了什么？","Editor不仅靠已有知识想修复，还从反复失败出发在线查论文/模型/code，并能请求host批准的新感知能力；核心不是多写一个反思提示。","教学例：短暂手物交互反复漏记，Editor查到动作分类模型后请求服务，再改记忆的写入和读取方式。","What goes beyond a closed-world harness loop?","The editor researches recurring failures externally and can request host-approved perception capabilities, rather than relying only on prior knowledge and a fixed tool set.","Teaching example: recurring missed hand-object interactions motivate research on an action classifier, a service request and corresponding memory changes."),
        ("stage-entry-loss-budget","mechanism","每轮损失都很小，efficiency阶段还需累计损失约束吗？","需要。只限制相对父代的损失会逐轮积累退化；原文另相对efficiency入口harness限制总概率和正确数损失。","教学例：每轮掉0.003连续5轮会掉0.015；总容忍只有0.008，后续不能因单轮合格就继续放行。","Why bound total loss as well as each update?","Small parent-relative losses can accumulate. The efficiency gate also bounds probability/count losses relative to the stage-entry harness.","Teaching example: five losses of.003 total.015, exceeding the.008 cumulative tolerance even though each update meets its local bound."),
        ("harness2-open-tools","comparison","与Harness²都改harness，能共用一个选择器解释吗？","不能。Harness²匿名选择已执行最终产物，跨任务重启初始harness；MORSE持续head并按私有validation质量/延迟筛选，还扩展host批准感知服务。对象和反馈不同。","教学例：匿名挑两个报告不是按正确选项概率筛视频记忆程序；装了VideoMAE也不等于已被最终harness采用。","Can MORSE and Harness² share one selector interpretation?","No. Harness² anonymously selects executed final artifacts and restarts each task; MORSE iterates a head using private validation quality/latency and approved perception services. Their selection objects and feedback differ.","Teaching example: choosing anonymous reports differs from scoring a video-memory program's option probabilities; installing VideoMAE does not imply adoption."),
        ("frame-cap-not-total-memory","implementation","64帧上限是否保证总memory恒定？","不是。另有16秒近期窗口，text和embeddings没有host全局上限。复述成本时应分别记录pixels、文本、向量和服务调用，不能只报frame cap。","教学例：历史帧保持64张，但每分钟新增一条caption仍会让文本随视频时长增长。","Does the64-frame cap make total memory constant?","No. A separate16-second window exists, while text/embeddings have no host-wide cap. Pixels, text, vectors and service calls need separate accounting.","Teaching example: retaining64 historical frames while adding a caption each minute still makes text storage grow with video duration."),
    ]),
}
for _paper in PAPERS:
    _paper.update(CONTENT[_paper["key"]])


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n")


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    for paper in PAPERS:
        for kind, suffix in (("pdf", "pdf"), ("src", "tar.gz")):
            path = CACHE / f"{paper['id']}v1.{suffix}"
            if not path.exists():
                request = Request(f"https://arxiv.org/{kind}/{paper['id']}v1", headers={"User-Agent": "auto-research/primary-review"})
                with urlopen(request, timeout=40) as response:
                    raw = response.read(15_000_001)
                if len(raw) > 15_000_000:
                    raise ValueError("small-paper capture budget exceeded")
                path.write_bytes(raw)
            print(path.name, path.stat().st_size, digest(path), flush=True)


def inspect():
    import fitz
    for paper in PAPERS:
        pdf = fitz.open(CACHE / f"{paper['id']}v1.pdf")
        for number, page in enumerate(pdf):
            text = page.get_text()
            if (number < 2 or "Algorithm 1" in text or "Figure 2:" in text
                    or (paper["key"] == "transport-safe-audit" and "Four-agent benchmark" in text)):
                print(paper["id"], number+1, text[:120].replace("\n", " "))
                page.get_pixmap(matrix=fitz.Matrix(1.1, 1.1)).save(CACHE / f"{paper['id']}-page{number+1}.png")


def author():
    import fitz
    from english_learning_sources import question_units

    bundle_path = AUDIT / "agent-authored-bundle.json"
    if bundle_path.exists():
        raise ValueError("append-once owned bundle exists; preserve reviewed records")
    papers, english, specs, dives, reviews = {}, {}, {}, [], []
    for paper in PAPERS:
        key, aid = paper["key"], paper["id"]
        identity = "agent-research:"+key
        directory = ROOT / f"docs/agent-research/{aid}-{key}"
        assets = directory / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        source = CACHE / f"{aid}v1.pdf"
        source_hash = digest(source)
        pdf = fitz.open(source)
        image = assets / "paper-figure-01.png"
        pdf[paper["page"]-1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(paper["crop"])).save(image)
        pdf.close()
        image_hash = digest(image)
        write(assets / "provenance.json", {"schema_version": 1, "reviewed_on": DATE, "figures": [{
            "file": image.name, "figure": paper["figure"], "paper_id": aid, "version": "v1",
            "paper_url": f"https://arxiv.org/abs/{aid}v1", "source_url": f"https://arxiv.org/pdf/{aid}v1#page={paper['page']}",
            "source_sha256": source_hash, "asset_sha256": image_hash, "image_sha256": image_hash,
            "source_kind": "fixed_version_pdf_crop_rendered_png", "page": paper["page"],
            "crop_points": paper["crop"], "render_dpi": 144, "caption_included": True,
            "scientific_content_modified": False, "visual_review_done": True,
            "attribution": "Original authors' figure/algorithm and caption. Not local results; no new license granted."}]})
        component = paper["module"] is not None
        module = "auto_research.agent_research."+paper["module"] if component else None
        local = "src/auto_research/agent_research/"+paper["module"]+".py" if component else None
        command = f"PYTHONPATH=src python -c 'from {module} import diagnostic; print(diagnostic(42))'" if component else None
        peer_link = os.path.relpath(ROOT / "docs" / paper["peer_path"], directory)
        label = "`component_only` / L1 CPU数学机制诊断，`diagnostic_only=true`；不是Agent能力复现。" if component else "`deferred_high_cost` / 仅资料收录，未实现、未运行。"
        label_en = "`component_only` / L1 CPU mathematical diagnostics, `diagnostic_only=true`; not agent-capability reproduction." if component else "`deferred_high_cost` / review-only, not implemented or run."
        local_path = f"`{local}`；`tests/test_nov24_agent_components.py`" if component else "无：review-only，未创建本地算法或复现代码目录"
        local_path_en = f"`{local}`; `tests/test_nov24_agent_components.py`" if component else "None: review-only; no local algorithm/reproduction-code directory"
        run_cn = f"""```bash
{command}
PYTHONPATH=src python -m pytest tests/test_nov24_agent_components.py -q
```

源码冻结后的[42/43/44三seed机制指标](metrics/component-cpu-seeds42-44.json)由统一runner生成。合成数学控制无能力benchmark、无test调参；三seed不是三次模型训练，也不提升证据层级。""" if component else "无本地实验命令、metrics或GPU回执；review-only终态不需要伪造执行证据。"
        run_en = f"""```bash
{command}
PYTHONPATH=src python -m pytest tests/test_nov24_agent_components.py -q
```

The shared runner records [seed42/43/44 mechanism metrics](metrics/component-cpu-seeds42-44.json) after source freeze. Synthetic mathematical controls load no capability benchmark and use no test-based tuning. Three seeds are not three model trainings and do not upgrade evidence.""" if component else "No local experiment command, metrics or GPU receipt exists. Review-only closure needs no invented execution evidence."
        cn = f'''# {paper['cn_title']}

[English](README-en.md)

> {label} 2026-11-23首发、2026-11-24发现/审查，不称11月24日新首发；不接入Evolve晋级。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [{paper['title']}](https://arxiv.org/abs/{aid}v1)，本轮固定v1 |
| 公司/机构/学校 | 一作{paper['author']}；{paper['org']} |
| 首次公开日期 | {paper['published'].replace('T', ' ').replace('Z', ' UTC')}，arXiv v1；updated与首发相同，无另一次修订 |
| 公告/发现日期 | 本轮公告池无此身份，公告日未核实；发现/审查日2026-11-24 |
| 原作者开源代码 | {paper['code_cn']} |
| 本地 Adapter / 方法 | `adapter: null`；key `{key}` |
| 本地复现代码目录 | {local_path} |

## 原始论文总结

### 背景与主要改动

{paper['method']}

{paper['mechanism']}

```mermaid
flowchart LR
  {paper['flow_cn']}
```

<!-- paper-figure:start -->
### 原论文关键图

[![原论文{paper['figure']}](assets/paper-figure-01.png)](https://arxiv.org/pdf/{aid}v1#page={paper['page']})

原图/算法来自[固定v1论文](https://arxiv.org/pdf/{aid}v1#page={paper['page']})第{paper['page']}页{paper['figure']}，完整保留图注/算法标题与内容，版权归原作者。仅裁无关正文/留白，科学内容未修改，已目视核对。[来源SHA256、裁剪坐标](assets/provenance.json)。它不是本地实验。
<!-- paper-figure:end -->

### 核心公式

$$
{paper['formula']}
$$

### 论文离线与线上效果

{paper['result']}

## 本地复现与边界

### 数据协议与代码映射

{paper['local']}

{run_cn}

### 同主题比较与边界

已读旧代表[{paper['peer']}]({peer_link})：{paper['compare']}

{paper['controls']}

### 完整实验与成本决定

{paper['cost']} **成本过高，不复现（审查 DONE）**；完整campaign不进入自动重试/实现队列。CPU组件通过不是完整论文数值复现。

### 来源核对

PDF SHA256：`{source_hash}`；固定v1 TeX SHA256：`{digest(CACHE / f'{aid}v1.tar.gz')}`。有限增量选题不推进全库11月15日审查水位，不宣称已穷尽Google/Meta或整个Agent领域。
'''
        page = directory / "README.md"
        page.write_text(cn)
        cn_hash = digest(page)
        en = f'''# {paper['title']}

<!-- source-sha256: {cn_hash} -->

[简体中文](README.md)

> {label_en} First released2026-11-23; discovered/reviewed2026-11-24, not a Nov24 first release. Not eligible for Evolve promotion.

## Paper information

| Field | Value |
| --- | --- |
| Paper | [Fixed arXiv v1](https://arxiv.org/abs/{aid}v1) |
| Institution | First author{paper['author']}; {paper['org']} |
| Original publication | {paper['published'].replace('T', ' ').replace('Z', ' UTC')}; update has the same timestamp, no separate revision |
| Announcement/discovery | Identity absent from this batch's announcement pool; announcement date unverified. Discovered/reviewed2026-11-24 |
| Author source code | {paper['code_en']} |
| Local adapter/key | `adapter: null`; `{key}` |
| Local reproduction code | {local_path_en} |

## Original paper summary

### Background and changes

{paper['method_en']}

{paper['mechanism_en']}

### Architecture

```mermaid
flowchart LR
  {paper['flow_en']}
```

### Key original figure

[![Original {paper['figure']}](assets/paper-figure-01.png)](https://arxiv.org/pdf/{aid}v1#page={paper['page']})

Original {paper['figure']} and its full caption/algorithm title from fixed-v1 PDF page{paper['page']}. Copyright belongs to the authors. Only unrelated text/whitespace is cropped; scientific content is unchanged and visually reviewed. [Source](https://arxiv.org/pdf/{aid}v1#page={paper['page']}) and [SHA256/crop provenance](assets/provenance.json). Not local evidence.

### Core equations

$$
{paper['formula']}
$$

### Reported offline and online results

{paper['result_en']}

## Local reproduction and limits

### Data protocol and code mapping

{paper['local_en']}

{run_en}

### Same-topic comparison and limits

Reviewed older representative [{paper['peer']}]({peer_link.replace('README.md', 'README-en.md')}): {paper['compare_en']}

{paper['controls_en']}

### Full experiments and cost decision

{paper['cost_en']} **Too costly; not reproduced (review DONE).** The full campaign enters no automatic retry/implementation queue. Passing CPU controls does not reproduce the complete paper.

### Source review

PDF SHA256: `{source_hash}`; fixed-v1 TeX SHA256: `{digest(CACHE / f'{aid}v1.tar.gz')}`. This finite incremental selection does not move the global Nov15 review watermark or claim exhaustive Google/Meta/Agent coverage.
'''
        page.with_name("README-en.md").write_text(en)
        spec = {
            "domain": "agent-research", "key": key, "title": paper["title"],
            "paper_url": f"https://arxiv.org/abs/{aid}v1", "reviewed_version_url": f"https://arxiv.org/pdf/{aid}v1",
            "reviewed_version": "v1", "reviewed_arxiv_id": aid+"v1",
            "detail_path": f"agent-research/{aid}-{key}/README.md", "first_author": paper["author"],
            "first_author_affiliation": ("Carnegie Mellon University" if key == "morse" else
                                         "National University of Singapore, School of Computing" if key == "ooas" else paper["org"]),
            "organizations": paper["org"].split(" / "), "published": "2026-11-23", "published_at": paper["published"],
            "updated_at": paper["published"], "discovered_on": DATE, "reviewed_on": DATE, "announced_on": None,
            "code": None, "code_status": paper["code_cn"], "code_license": None,
            "adapter": None, "topic": [paper["topic"], "CPU机制组件" if component else "系统成本审查"],
            "priority": "P1", "intake_class": "nov23_first_publication_discovered_nov24",
            "implementation_status": "component_only" if component else "deferred_high_cost", "component_implemented": component,
            "local_operator": module+".diagnostic" if component else None, "local_command": command,
            "evaluation_tier": "l1_mechanism" if component else None, "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False, "requires_gpu_validation": False,
            "gpu_validation_passed": False, "gpu_validation_artifact": None, "review_done": True,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
            "review_resolution": "not_reproduced_high_cost", "automatic_retry": False, "automatic_implementation_queue": False,
            "cost_assessment": {"source": f"https://arxiv.org/pdf/{aid}v1", "basis": paper["cost"],
                                "available_resource": "one A100 or A30, or local Mac", "cost_type": "published_configuration_and_readonly_estimate_not_local_measurement",
                                "decision": "成本过高，不复现（审查 DONE）；仅有界CPU组件或资料收录。",
                                "local_budget": {"checkpoint_download_bytes": 0, "dataset_download_bytes": 0, "paid_api_calls": 0,
                                                 "local_component_seconds_per_seed_cap": 30 if component else 0}},
            "summary": paper["method"], "fidelity_note": paper["local"], "method_source_sha256": source_hash,
        }
        if key == "morse":
            spec["deferral_reason"] = "成本过高，不复现（审查 DONE）；完整多backbone视频服务与Editor演化矩阵超出单卡短时预算，仅资料收录，无自动重试。"
        specs[identity] = spec
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
        dives.append({"paper": identity, "target_card": paper["card"], "source_revisions": revisions,
                      "comparison": {"position": paper["method"], "tradeoff": paper["compare"], "sections": HEADINGS},
                      "analysis": {"title": paper["cn_title"], "body": paper["mechanism"]+paper["controls"], "papers": [identity, paper["peer"]]},
                      "question": {"id": "cross-nov24-"+key, **{field: comparison[field] for field in ("question", "answer", "example")}, "papers": [identity, paper["peer"]]},
                      "update": {"date": DATE, "papers": [identity, paper["peer"]], "source_revisions": revisions,
                                 "summary": paper["local"]+" 完整campaign终态不复现，审查DONE。"},
                      "english": {"comparison": {"position": paper["method_en"], "tradeoff": paper["compare_en"]},
                                  "analysis": {"title": paper["title"], "body": paper["mechanism_en"]+" "+paper["controls_en"]},
                                  "question": {"question": english_comparison[5], "answer": english_comparison[6], "example": english_comparison[7]},
                                  "update": paper["local_en"]+" The full campaign is terminally not reproduced."}})
        reviews.append({"identity": identity, "id": aid, "published_at": paper["published"], "updated_at": paper["published"],
                        "discovered_on": DATE, "announced_on": None, "source_url": f"https://arxiv.org/pdf/{aid}v1",
                        "source_sha256": source_hash, "source_revisions": revisions, "scope": paper["local_en"],
                        "cost_basis": paper["cost_en"], "implementation_status": spec["implementation_status"], "review_done": True})
    write(AUDIT / "paper-proposals-agent.json", {"schema_version": 1, "reviewed_on": DATE, "papers": specs})
    write(bundle_path, {"schema_version": 1, "date": DATE, "papers": papers, "english_question_units": english})
    write(AUDIT / "deep-dive-proposals-agent.json", {"schema_version": 1, "reviewed_on": DATE, "integration_owner": "root", "proposals": dives})
    write(AUDIT / "agent-review.json", {"schema_version": 1, "reviewed_on": DATE,
                                       "scope": "Three Nov23 first releases found Nov24; finite selection, no watermark movement",
                                       "implementation_preflight_completed": True, "reviews": reviews})
    print("Authored3 bilingual papers,12 reviewed bilingual QA units and3 deep-dive proposals; no shared files written.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    if args.fetch:
        fetch()
    elif args.inspect:
        inspect()
    else:
        author()


if __name__ == "__main__":
    main()
