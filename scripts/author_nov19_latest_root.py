"""Author the five reviewed root paper notes and bilingual learning records.

The prose and Q&A below are manually reviewed source-specific content. This is
not an automatic abstract-to-question or machine-translation pipeline.
"""

from __future__ import annotations
import hashlib
import json
from pathlib import Path
import author_nov18_latest_root as figures
from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov19-latest"
CACHE = ROOT / ".cache/nov19-latest/root"
DATE = "2026-11-19"

PAPERS = [
    dict(
        id="2611.23910",
        key="mle-agents",
        domain="recommendation",
        author="Matthew Li",
        institution="Meta Platforms",
        priority_orgs=["Meta"],
        module="reproductions/mle_agents_components.py",
        gpu=False,
        tier="l0_interface",
        topic=["研究与服务闭环", "自动模型研发"],
        card="recommendation/research-serving-loop",
        compare="recommendation:evopilot",
        figure=1,
        image="mle_agent_2_0.png",
        title="MLE Agents: Autonomous ML Engineering in Large-scale Recommendation Systems",
        name="MLE Agents：工业精排的目标校准与方差探针准入",
        cn="Meta把提假设、改代码、训练和读指标组成有人监督的模型研发循环。2.0每轮名义上并行七个候选和一个方差探针，使用与线上影响校准过的加权NE，而不是只追逐点击AUPRC。失败块名单、结构化输出和只回传近期未采纳赢家控制上下文陈旧；最终模型仍由工程师审核并独立做线上实验。",
        en="Meta combines hypotheses, code changes, training and metric inspection in a human-on-the-loop development cycle. Version2.0 nominally evaluates seven candidates and a variance probe in parallel, using weighted NE calibrated against online outcomes instead of click AUPRC alone. A failure blocklist, structured outputs and recent uncarried winners limit stale context. Engineers still review the final model and conduct a separate online experiment.",
        formula=r"L=0.3NE_{click}+0.7NE_{downstream},\qquad accept=\mathbf1[L_{probe}-L_{candidate}\ge0.0005].",
        method_cn="§1.2给出0.3/0.7目标，§3.5明确与同轮variance probe比较，而不是任意旧基线。完成状态须有两条独立信号；一候选只改一项连贯机制。阈值来自历史噪声探针，不能把0.0005说成显著性检验或跨数据通用常数。接口返回离线搜索接纳和仍需人工审核，不发起训练或生产发布。",
        method_en="Section1.2 defines the0.3/0.7 objective; section3.5 compares a candidate to its same-iteration variance probe, not an arbitrary old baseline. Completion needs two independent signals and each candidate makes one coherent change. The0.0005 threshold is estimated from historical training noise, not a significance test or a universal constant. The interface reports offline search admission and required human review without launching jobs or production changes.",
        result_cn="1097个完成候选中325个被接受，另有155个探针；加权NE从0.6611到0.6388。超过一周的真实生产A/B使搜索会话量相对+0.23%±0.15（95%区间，Fieller方法），同时time-to-render护栏退化。1.0的15.6%与2.0的29.6%接受率伴随目标和预算变化，不是受控消融；不能把离线接纳率当成线上成功率。",
        result_en="Of1097 completed candidates,325 were accepted, with155 additional probes; weighted NE changed from0.6611 to0.6388. Production A/B over more than one week reports relative search-session lift+0.23%±0.15 (95% interval, Fieller method), alongside a time-to-render guardrail regression. The15.6% versus29.6% acceptance comparison also changes the objective and budget, so it is not a controlled ablation or an online-success rate.",
        limits_cn="本地只执行目标与完成/准入接口。没有运行Claude研究调用、候选代码生成、私有数据分布式训练或线上A/B，也没有新增可执行Evolve搜索策略。合成输入不代表Meta模型指标。",
        limits_en="Only the objective and completion/admission interface run locally. There are no Claude research calls, candidate generation, distributed private-data training, online A/B or executable new Evolve search strategy. Fixture inputs are not Meta model measurements.",
        cost_cn="§3.3记录候选训练评估中位耗时3.54小时，完整活动1252个完成任务并依赖亿级私有样本和生产流量。单卡不能承担原活动。",
        cost_en="Section3.3 reports median training/evaluation time3.54hours per candidate. The full campaign completed1252 jobs on hundreds of millions of private examples and production traffic; one GPU cannot reproduce it.",
        contrast_cn="EvoPilot先锁定控制/实验两臂的比较合同并拒绝不匹配证据；MLE Agents强调搜索目标与同轮噪声探针。二者都不让“训练结束”自动成为可发布结论，目标校准也不能取代EvoPilot的产物一致性检查。",
        contrast_en="EvoPilot fixes a matched control/treatment contract and rejects mismatched evidence; MLE Agents emphasizes objective calibration and same-iteration noise probes. Neither treats a completed job as a launchable conclusion, and calibrated objectives do not replace artifact consistency checks.",
    ),
    dict(
        id="2611.24283",
        key="xsplit-argus",
        domain="recommendation",
        author="Alexander Ploshkin",
        institution="固定v1未列一作机构（不由其他作者邮箱推断）",
        priority_orgs=[],
        module="reproductions/xsplit_argus_components.py",
        gpu=True,
        tier="l1_mechanism",
        topic=["排序网络与长序列", "历史压缩与在线复用"],
        card="recommendation/history-ranking-backbones",
        compare="recommendation:argus",
        figure=1,
        pdf=(4, [80, 300, 515, 555]),
        title="X-split Argus: Learning Reusable History Tokens for Efficient CTR Prediction",
        name="X-split ARGUS：可复用历史token与双头蒸馏",
        cn="将候选无关的旧历史压成因果编码器末K个状态，在线只编码最近M个事件；候选token再对两段记忆做cross-attention。离线缓存是服务时的执行安排，不是训练时detach压缩器。点击监督头与原始logit的L1蒸馏头共享历史表示，但上线只使用监督头。",
        en="A candidate-independent causal encoder retains the lastK states of older history. Serving encodes only the most recentM events, and candidate tokens cross-attend to both memories. Offline caching is a serving execution choice, not a reason to detach the compressor during training. A supervised click head and an L1 raw-logit distillation head share representations; only the supervised head serves predictions.",
        formula=r"Z(b)=[c_{b-K+1};\ldots;c_b],\quad V_t=[Z(b(t));u_{b(t)+1:t-1}],\quad L=BCE(z^{GT},y+\epsilon(1-y))+\lambda|z^{KD}-sg(z^T)|.",
        method_cn="Eq1–11：历史编码因果且候选无关；训练memory只选目标之前状态。默认b(t)=max(0,t−1−M)，服务缓存cutoff允许与最近事件重叠或留缺口。训练runtime共享全序列因果局部attention，服务只重算最近M条，左边界/有效感受野并不相同。KD是原始logit的L1，不是BCE或KL；仅负标签抬到epsilon，教师完全detach。小网络缩小层数/维度，保留真实attention、双头与梯度。",
        method_en="Eqs1–11 require causal, candidate-independent history states and strictly pretarget memory. The default boundary ismax(0,t−1−M); a serving snapshot may overlap recent events or leave a gap. Shared causal local-attention training and serving on only the lastM events have different left boundaries/receptive fields. KD is raw-logit L1, not BCE or KL. Only negatives are smoothed and teacher logits are detached. The small network reduces depth/dimension but executes real attention, separate heads and gradients.",
        result_cn="§5.1：7天用户哈希稳定分桶，每臂为该广告surface的6%；ACV相对+4.65%、clicks+2.96%，p<0.001，一月后反向A/B确认。相同流量需多15%的线上GPU，不能写成成本下降。原文PDF作者栏未给机构；同名ARGUS前作属Yandex不足以推定本篇机构。",
        result_en="Section5.1 reports seven-day stable user-hash A/B,6% of the advertising surface per arm: relative ACV+4.65% and clicks+2.96%,p<0.001, with a reverse test one month later. Serving the same traffic needs15% more online GPUs, not a cost reduction. The fixed PDF byline lists no institution; the Yandex affiliation of the earlier ARGUS paper does not establish this paper affiliation.",
        limits_cn="输入是显式小型事件/候选特征；未训练teacher或复现词表、每日缓存、RTB数据和生产服务。负控改目标/未来反馈保持预测不变；KD反传到compressor，但不能据此推断NE或ACV收益。",
        limits_en="Inputs are explicit small event/candidate features. Teacher training, vocabularies, daily caching, RTB data and serving are absent. Changing target/future feedback leaves predictions invariant and KD reaches the compressor; neither check establishes NE or ACV gains.",
        cost_cn="原配置一年/8192事件，compressor和runtime各6层、1024维，私有RTB数据及持续离线预计算；完整训练和生产A/B不适合单卡本轮预算。",
        cost_en="The paper uses one year/8192 events, six1024-wide layers in each history encoder, private RTB data and recurring precomputation. Full training and production A/B exceed this single-device batch budget.",
        contrast_cn="ARGUS前作按反馈→物品分解下一事件分布；X-split重点是候选无关历史缓存和候选特定点击logit蒸馏，目标排列与预测头不能照搬。二者的本地负结果/诊断也不能互相当作能力对照。",
        contrast_en="Earlier ARGUS factorizes the next event as feedback then item. X-split focuses on candidate-independent cached history and candidate-specific click-logit distillation, so token ordering and heads are not interchangeable. Their local negative results/diagnostics are not a matched capability comparison.",
    ),
    dict(
        id="2611.24006",
        key="mars-fapo",
        domain="recommendation",
        author="MARS Team（集体署名）",
        institution="Taobao",
        priority_orgs=[],
        module="reproductions/mars_fapo_components.py",
        gpu=True,
        tier="l1_mechanism",
        topic=["研究与服务闭环", "多阶段推荐编排"],
        card="recommendation/research-serving-loop",
        compare="recommendation:evopilot",
        figure=3,
        image="post_train.png",
        title="MARS Technical Report",
        name="MARS：近线推荐编排与ActionMask偏好优化",
        cn="MARS让近线0.6B策略为用户产生跨召回、粗排、精排和重排的七维配置，经校验后缓存，在线始终不等待LLM。SFT建立合法格式，FAPO把偏好比较集中到实际不同的动作值token，最后GRPO在沙箱回放和冻结奖励模型上继续优化。正文版权行为Taobao，贡献者按名字母排序，不虚构个人一作机构。",
        en="MARS uses a near-line0.6B policy to produce seven-dimensional user configurations spanning retrieval, preranking, ranking and reranking. Validated configurations are cached; online serving never waits for an LLM. SFT establishes valid formatting, FAPO compares differing action-value tokens, and GRPO continues with sandbox replay and a frozen reward model. The manuscript credits Taobao and lists contributors alphabetically rather than assigning an invented individual-first-author affiliation.",
        formula=r"g^A(y)=|A|^{-1}\sum_{t\in A}\log\pi(y_t),\quad \log o^A=g^A-\log(1-e^{g^A}),\quad L=-\overline{\log\pi(y^+)}-\beta w_{pref}\log\sigma(\log o^A_+-\log o^A_-).",
        method_cn="Eq11–13保留全chosen回答的生成anchor，只有偏好项乘clip(1+2(p+−p−)/p均值,0.2,3)。缺失任一历史V2P时权重为1。只有弱证据且达到相对gap才允许反转chosen/rejected；强证据不反转。动作mask由可信的字段值span/token对齐层提供，必须包含完整变化值而非共享JSON结构；不以脆弱字符串搜索冒充原tokenizer。历史配置V2P是观察统计，不是因果后验。",
        method_en="Eqs11–13 retain the full chosen-response generation anchor; only preference loss receivesclip(1+2(p+−p−)/scenario_mean,0.2,3). A missing V2P estimate gives weight1. Only weak-evidence pairs meeting the relative-gap rule may reverse; strong pairs retain their business-score ordering. Masks come from a trusted field-value span/token alignment layer and cover complete differing values, not shared JSON structure. No fragile substring matcher impersonates the tokenizer. Historical configuration V2P is observational, not causal.",
        result_cn="两周稳定用户随机分桶，各臂5%，五个淘宝营销场景；百亿补贴V2P+5.22%、GMV+7.34%，整体模式混合约20% Minimal并关联线上均值延迟−12ms。使用ITT包含fallback流量，不仅筛有效缓存请求。近线LLM成本没有计入这12ms；原文说明GMV序列相关与pCTR用户聚类尚需重分析，不能宣称因果拆分各阶段贡献。",
        result_en="Two-week stable user-randomized A/B uses5% per arm across five Taobao scenarios. Baiyibutie reports V2P+5.22%,GMV+7.34%; a roughly20% Minimal mode mix is associated with12ms lower mean serving latency. ITT includes fallback traffic rather than only valid cached actions. The12ms excludes near-line LLM compute. GMV serial correlation and pCTR user clustering remain reanalysis limitations, and stage-specific causal contributions are not isolated.",
        limits_cn="本地只实现posterior启发式权重、弱证据翻转规则与FAPO张量损失；没有0.6B生成、字段tokenizer、SFT/GRPO、Sandbox、奖励模型、iGraph缓存或实时推荐。结构token仍有生成梯度，rejected非动作token没有偏好梯度。",
        limits_en="Local code implements only historical weighting, weak-pair orientation and the FAPO tensor loss. There is no0.6B generation, field tokenizer, SFT/GRPO, sandbox, reward model, iGraph cache or live recommendation. Chosen structural tokens retain generation gradients; rejected nonaction tokens have no preference gradient.",
        cost_cn="§5.1每周约10万样本，32张H20，每个SFT/FAPO/GRPO阶段约4小时，并需要生产回放及千万DAU流量。完整实验成本远超单A100/A30。",
        cost_en="Section5.1 samples about100k examples weekly, uses32H20 GPUs for roughly four hours per SFT/FAPO/GRPO stage, and requires production replay and ten-million-DAU traffic. The full experiment far exceeds one A100/A30.",
        contrast_cn="EvoPilot校验模型开发实验的两臂证据，MARS生成和训练线上流水线配置。MARS的缓存/fallback是服务安全，不能替代开发比较合同；ActionMask loss也不能证明策略已经能生成合法或优质配置。",
        contrast_en="EvoPilot validates evidence for model-development comparisons; MARS trains serving-pipeline configurations. Cache/fallback safety does not replace an experiment contract, and an ActionMask loss does not establish valid or high-quality policy generation.",
    ),
    dict(
        id="2611.02643",
        key="searchinject",
        domain="agent-research",
        author="Kainan Zhou",
        institution="Google LLC",
        priority_orgs=["Google"],
        module="agent_research/searchinject_components.py",
        gpu=False,
        tier="l1_mechanism",
        topic=["Agent 评测与可靠性", "检索上下文准入"],
        card="agent-research/harness-and-self-improvement",
        compare="agent-research:silentguard",
        figure=1,
        pdf=(1, [45, 35, 300, 263]),
        title="SearchInject: Retrieval Exposure Control for Indirect Prompt Injection in Language-Model Search",
        name="SearchInject：检索风险与干净误隔离预算",
        cn="间接注入先要进入上下文才有机会影响LLM。SearchInject在原top100候选中，用相关性、abuse、instruction概率及两项相关性交互做logistic风险评分；超过冻结阈值才隔离，按原顺序从同一候选池补足top10。它控制暴露，而不是验证下游攻击成功。Google官方目录今天新增，但论文首发11月2日，按历史发现补录，不算今天新论文。",
        en="An indirect injection must enter context before influencing an LLM. SearchInject scores the original top100 candidates with relevance, abuse, instruction likelihood and two relevance interactions. It quarantines scores strictly above a frozen threshold and refills top10 in the original order from the same pool. It controls exposure, not downstream attack success. The Google directory entry is new to this capture, but the November2 paper is a historical backfill, not a new publication today.",
        formula=r"z=[r,a,i,ar,ir],\quad s=\sigma(b+\beta^Tz),\qquad \max_\tau Recall_{crafted}(\tau)\;s.t.\;\widehat{FQ}_{clean}(\tau)\le0.005,\quad quarantine\iff s>\tau.",
        method_cn="§III-C/D：joint模型为class-balanced logistic regression，不能把输出当校准概率。阈值只在calibration集选并冻结；文档重复出现在不同query时按placement计数。原稿未发布abuse/字符与词n-gram词表、IDF、scaler或拟合系数，因此本地明确接收外部特征/系数，只实现score、约束选阈与有序refill，不用关键词规则假装原检测器。",
        method_en="SectionsIII-C/D use class-balanced logistic regression, not calibrated probabilities. Choose and freeze the threshold on calibration only, counting repeated query-document placements separately. Fitted abuse models, word/character vocabularies, IDF, scalers and coefficients are unreleased. Local APIs explicitly accept external features/coefficients and implement scoring, constrained threshold selection and ordered refill; keyword rules do not stand in for the detector.",
        result_cn="300个SciFact查询、每query四种已见构造家族；BM25暴露率0.9408→0.1583，干净NDCG最大绝对变化0.0018。calibration误隔离0.498%但test达0.59%–0.65%，不是新样本0.5%保证。104case生成跟进零确认攻击且48判断未决，不能计算攻击成功率下降；1200个query×family结果不是1200个独立样本。",
        result_en="The study uses300 SciFact queries and four construction families seen during development. BM25 exposure changes0.9408→0.1583; the largest clean NDCG absolute change is0.0018. Calibration false quarantine is0.498% but test is0.59–0.65%, not a0.5% guarantee on new data. The104-case generation follow-up confirms no hijacks and leaves48 judgments unresolved, so it cannot estimate attack-success reduction;1200query-family outcomes are not1200 independent observations.",
        limits_cn="显式数值夹具只检查feature顺序、严格>阈值、干净经验约束与refill。无真实payload、SciFact检索、拟合分类器、生成模型或安全认证；更低阈值移除更多候选，也可能补入原rank10外的攻击页。",
        limits_en="Explicit numerical fixtures check feature order, strict thresholding, empirical clean cost and refill. There are no real payloads, SciFact retrieval, fitted classifiers, generators or security certification. A lower threshold can remove more candidates yet refill a surviving attack page from below rank10.",
        cost_cn="完整检测器缺失可复放的拟合参数、分区与数据hash，生成跟进还依赖两个4B级模型。材料缺口与生成成本下不尝试重建/扩展完整实验。",
        cost_en="A full replay lacks fitted parameters, split artifacts and data hashes; the generation follow-up additionally needs two roughly4B models. Missing artifacts and generation cost rule out a full reconstruction/expansion in this batch.",
        contrast_cn="SilentGuard核对工具返回值是否满足请求不变量；SearchInject在第三方文本进入上下文之前做风险准入。前者检查语义执行合同，后者检查检索暴露，HTTP200或低暴露率都不能证明最终回答安全。",
        contrast_en="SilentGuard checks tool responses against request invariants; SearchInject screens third-party text before context admission. Semantic execution contracts and retrieval exposure are distinct: neither HTTP200 nor lower exposure proves a safe final answer.",
    ),
    dict(
        id="2611.24849",
        key="execjudges",
        domain="agent-research",
        author="Eugene Agichtein",
        institution="Emory University",
        priority_orgs=[],
        module="agent_research/execjudges_components.py",
        gpu=False,
        tier="l0_interface",
        topic=["Agent 评测与可靠性", "可执行评审与共识"],
        card="agent-research/evaluation-and-reliability",
        compare="agent-research:fuse-evaluator",
        figure=1,
        pdf=(2, [48, 80, 558, 245]),
        title="Can Programs Replace LLM Judges? Executable Program Judges for Scalable and Efficient Relevance Labeling",
        name="ExecJudges：显式证据等级与向下取整共识",
        cn="对每个topic独立生成三个轻量Python评审程序，程序回答on-subject/some-answer/exact/dedicated四个证据问题，固定评分函数映射为等级，再对三个分数均值向下取整。LLM负责一次性的程序编写而不是逐文档调用，生成代码必须隔离执行。本地不执行来自网络或LLM的代码。",
        en="For each topic, three independently generated lightweight programs answer on-subject/some-answer/exact/dedicated evidence questions. A fixed function maps answers to grades, then floors the mean of the three grades. The LLM writes programs once rather than judging every document, and generated code must run in isolation. Local code never executes network- or LLM-generated code.",
        formula=r"g=\begin{cases}0&\neg on\\1&on\land\neg some\\3&on\land some\land exact\land dedicated\\2&otherwise\end{cases},\qquad label=\left\lfloor k^{-1}\sum_i g_i\right\rfloor.",
        method_cn="§3.2：0–3和0–2量表分别实现；没有证据不能由其他布尔项抬高等级。共识是floor不是round或多数票；k=3与取整规则在测试前固定。ExecJudges-L可看少量训练标签，评测必须分开这些样本，不能把gold测试qrels送给生成器。本地只接受显式布尔证据/分数，没有假装实现LLM writer、NLP toolkit或恶意代码沙箱。",
        method_en="Section3.2 uses separate0–3 and0–2 scales. Other booleans cannot override absent subject/answer evidence. Consensus floors rather than rounds or votes; k=3 and the rule were fixed before test evaluation. ExecJudges-L may use a small labeled training subset, but evaluation must separate it and never give test qrels to the writer. Local APIs accept explicit booleans/grades, not a pretend LLM writer, NLP toolkit or hostile-code sandbox.",
        result_cn="七个TREC集合；作者报告系统排名Kendall tau为0.87–0.94，写程序每topic约$0.17–$0.49，标注CPU小于1秒。不同集合/标签预算对应不同比较，不概括为全面优于LLM。上下文中出现训练标签并非本地回答准确率的证据；本文没有生产A/B。",
        result_en="Across seven TREC collections, the authors report system-ranking Kendall tau0.87–0.94, program-writing cost about$0.17–$0.49 per topic and CPU grading below one second. Results depend on collection and label budget, not universal superiority to LLM judges. Training labels are not evidence of local answer accuracy. No production A/B is reported.",
        limits_cn="只运行固定grade mapping和floor聚合的L0接口，未生成或执行评审程序、未下载TREC、未调用模型，不输出相关性准确率。布尔值必须严格bool，整数0/1不会静默当证据。",
        limits_en="Only the fixed grade mapping and floor aggregation run as L0 interfaces. No program generation/execution, TREC download or model call occurs, and no relevance accuracy is reported. Evidence must be strict booleans; integers0/1 are not silently accepted.",
        cost_cn="完整七集合生成/修复/多标签预算实验依赖付费前沿writer和大规模TREC池，预算及代码沙箱维护不在本轮范围；不运行完整campaign。",
        cost_en="The full seven-collection generation/repair/multiple-label-budget campaign needs a paid frontier writer and large TREC pools plus a secure execution sandbox; it is outside this batch budget.",
        contrast_cn="FUSE用隐藏真实动机和可验证模拟状态评估社会推理；ExecJudges将检索证据映射为显式等级。确定性聚合能提高可检查性，却不产生正确的证据判断，也不代替隐藏状态评测。",
        contrast_en="FUSE evaluates social reasoning against hidden motives and verifiable simulated state; ExecJudges maps retrieval evidence to explicit grades. Deterministic aggregation improves inspectability but supplies neither correct evidence judgments nor hidden-state evaluation.",
    ),
]

# (stable id, question, answer, example, English question/answer/example)
QA = {
    "mle-agents": [
        (
            "calibrated-objective",
            "为什么不用点击AUPRC一直搜索？",
            "它曾偏向易预测的直达查询，与线上下游参与不一致，因此用历史线上对齐后加权NE。",
            "教学例：click NE降.01、downstream升.01时，0.3/0.7目标变差.004。",
            "Why not search click AUPRC forever?",
            "It overemphasized easy navigational queries and did not track downstream engagement, motivating historically calibrated weighted NE.",
            "Teaching example: click NE−.01 and downstream NE+.01 worsen the0.3/0.7 objective by.004.",
        ),
        (
            "probe-reference",
            "候选应和什么比才能过噪声门槛？",
            "与同一轮variance probe比较；超过0.0005的目标下降才形成离线搜索接纳。",
            "教学例：候选.65胜旧基线.68，但同轮探针.64，仍应拒绝。",
            "What is the admission reference?",
            "Use the same-iteration variance probe and require at least0.0005 objective reduction for offline search admission.",
            "Teaching example: .65 beats an old.68 baseline but loses to this round’s.64 probe and must be rejected.",
        ),
        (
            "contract-not-launch",
            "MLE Agents和EvoPilot的准入能互代吗？",
            "不能。前者校准目标/训练噪声，后者核对两臂实验与产物；都还需要最终人工和线上确认。",
            "教学例：数据版本不同的两臂即使NE差够大，也不能用噪声门槛盖过协议失败。",
            "Can MLE admission replace EvoPilot?",
            "No. MLE calibrates objectives/noise; EvoPilot validates matched experiments and artifacts. Both still need human and online review.",
            "Teaching example: a large NE gap does not excuse different data versions across arms.",
        ),
        (
            "two-completion-signals",
            "为什么完成状态有一条成功还不能接纳？",
            "论文要求两条独立状态信号确认完成；崩溃、缺失评估或日志误报不能冒充真实结果。",
            "教学例：调度器成功而产物未写完时保留未完成，接口不得自动上线。",
            "Why are two completion signals required?",
            "A scheduler success alone can coexist with missing evaluation or partial artifacts; both independent signals must confirm completion.",
            "Teaching example: a completed job with unfinished artifacts stays inadmissible and never launches automatically.",
        ),
    ],
    "xsplit-argus": [
        (
            "cache-not-detach",
            "历史token缓存意味着训练时冻结compressor吗？",
            "不意味着。缓存是服务安排，GT和KD均经decoder反传到共同的历史编码器。",
            "教学例：KD头误差变化后compressor有梯度，但teacher不能有梯度。",
            "Does caching freeze the compressor during training?",
            "No. Caching is a serving choice; GT and KD gradients flow through the decoder into shared history encoders.",
            "Teaching example: a KD error produces compressor gradients but no teacher gradient.",
        ),
        (
            "causal-boundary",
            "近期历史与缓存cutoff为什么不能只用一个参数？",
            "缓存快照可以落后或与近期窗口重叠；训练默认相邻，但服务两者未必相邻，必须独立检查目标前边界。",
            "教学例：目标t=7、M=2时默认b=4；服务b=5会重叠一个历史事件而不是读取目标。",
            "Why distinguish recent budget and cache cutoff?",
            "A serving snapshot can lag or overlap recent events; default training adjacency does not make serving boundaries identical. Both must precede the target.",
            "Teaching example: one-based target7 andM=2 giveb=4; servingb=5 overlaps one historical event without reading the target.",
        ),
        (
            "argus-not-same-head",
            "为什么不能直接把ARGUS的物品头用到X-split？",
            "ARGUS分解反馈和next-item；X-split用候选特征预测点击，另用辅助头匹配teacher原始logit，任务和头不同。",
            "教学例：把L1 logit误差替成物品softmax CE会改变监督信号。",
            "Why not reuse the original ARGUS item head unchanged?",
            "ARGUS factorizes feedback/next-item; X-split predicts candidate clicks and uses a separate raw-logit KD head. The tasks and heads differ.",
            "Teaching example: item-softmax CE cannot replace raw-logit L1.",
        ),
        (
            "future-negative-control",
            "怎样检查反馈泄漏而不是只看shape？",
            "改目标及未来事件的反馈/特征，目标预测必须不变且未来梯度为零；仅检查输出维度不够。",
            "教学例：把t及其后特征加100仍预测不变；改t−1则允许变化。",
            "How do we test feedback leakage beyond shape?",
            "Perturb target/future events and require unchanged target predictions and zero future gradients. Shape checks alone are insufficient.",
            "Teaching example: adding100 fromt onward changes no target score, while changingt−1 may matter.",
        ),
    ],
    "mars-fapo": [
        (
            "nearline-not-free",
            "MARS为什么不增加同步LLM延迟，却不等于免费？",
            "LLM近线生成并缓存，在线只消费合法配置；近线推理、刷新和缓存仍耗资源。",
            "教学例：线上平均少12ms不代表0.6B解码快12ms。",
            "Why is near-line orchestration not free?",
            "Online serving consumes cached valid actions, but near-line generation, refresh and storage still cost resources.",
            "Teaching example: 12ms lower serving latency is not12ms faster0.6B decoding.",
        ),
        (
            "mask-and-anchor",
            "ActionMask只学习变化值，为何结构token仍有梯度？",
            "mask只限制偏好odds项；chosen全回答生成anchor保持不变，仍监督结构。",
            "教学例：rejected共享括号梯度为0，chosen括号仍受生成损失约束。",
            "Why do structural tokens retain gradients?",
            "ActionMask limits only the preference odds; the full chosen-response generation anchor still supervises structure.",
            "Teaching example: rejected shared braces have zero gradient; chosen braces retain generation gradients.",
        ),
        (
            "policy-versus-verifier",
            "MARS和EvoPilot都是Agent，有什么根本区别？",
            "MARS训练用户流水线动作；EvoPilot审核模型开发比较证据。配置格式合法不等于实验结论可信。",
            "教学例：合法Minimal动作不能代替控制/实验模型的数据版本核对。",
            "How do MARS and EvoPilot differ?",
            "MARS trains per-user pipeline actions; EvoPilot audits model-development comparisons. Valid action formatting does not make experimental claims reliable.",
            "Teaching example: a valid Minimal action cannot replace control/treatment data-version checks.",
        ),
        (
            "posterior-not-causal",
            "缺失历史V2P或强证据与V2P冲突时怎么做？",
            "缺失任一估计权重回1；强证据保留业务排序，仅弱证据满足gap才可翻转，且V2P非因果估计。",
            "教学例：chosen=.1,rejected=.2，强证据不翻转但权重可降低至.2。",
            "What happens with missing V2P or conflicting strong evidence?",
            "Missing either estimate gives weight1. Strong pairs retain business-score orientation; only weak pairs meeting the gap may reverse. V2P is not causal.",
            "Teaching example: chosen.1 versus rejected.2 does not reverse strong evidence, although its preference weight may fall to.2.",
        ),
    ],
    "searchinject": [
        (
            "exposure-not-hijack",
            "暴露率下降是否证明攻击成功率下降？",
            "不能。它记录恶意载体进入上下文，仍需定义并验证下游任务劫持；原跟进没有确认的undefended成功。",
            "教学例：移走83个载体而两臂均零确认攻击，不能计算有效防御率。",
            "Does lower exposure prove fewer successful attacks?",
            "No. Carrier admission differs from verified downstream hijacking; the follow-up confirms no undefended success from which to estimate a reduction.",
            "Teaching example: removing83carriers with zero confirmed hijacks in either arm does not yield a defense-success rate.",
        ),
        (
            "strict-refill",
            "s等于阈值时保留吗，移除后如何补足？",
            "相等保留；仅s>tau隔离，按原top100顺序补到10，不重新排序也不重新检索。",
            "教学例：.8阈值下.8保留、.9删除，原第11名可能补入。",
            "What happens at equality and after quarantine?",
            "Equality is retained; onlys>tau is quarantined. Refill to10in the original top100order without reranking or new retrieval.",
            "Teaching example: at.8, retain.8and remove.9; the original rank11may enter context.",
        ),
        (
            "different-gates",
            "SearchInject和SilentGuard的门槛是否相同？",
            "不是。前者筛选检索上下文，后者验证工具结果不变量；一种通过不证明另一种安全。",
            "教学例：低风险页面仍可能给出不满足过滤条件的API值。",
            "Are SearchInject and SilentGuard the same gate?",
            "No. One screens retrieved context and the other validates tool-result invariants. Passing one does not certify the other.",
            "Teaching example: low-risk text may still report an API value violating the requested filter.",
        ),
        (
            "calibration-transfer",
            "0.5%经验约束能直接当线上保证吗？",
            "不能。阈值冻结后分布变化可能超出；原文test误隔离0.59–0.65%，应保留而非抹掉。",
            "教学例：calibration1000项最多5项被隔离，test不因此也最多5项。",
            "Is the0.5% empirical constraint an online guarantee?",
            "No. A frozen threshold can exceed it under shift; the reported test rate0.59–0.65%must remain visible.",
            "Teaching example: at most5of1000calibration placements does not guarantee the same test count.",
        ),
    ],
    "execjudges": [
        (
            "writer-not-every-document",
            "ExecJudges把LLM调用放到哪一步？",
            "每topic写独立程序，然后CPU复用程序给所有文档；本地只有映射接口，没有writer。",
            "教学例：三程序可打分1000文档，不应伪称本地调用了3000次LLM。",
            "Where are LLM calls spent?",
            "They write independent programs per topic, which CPU grading reuses for all documents. The local implementation is only a mapping interface, not a writer.",
            "Teaching example: three programs can grade1000documents without claiming3000local LLM calls.",
        ),
        (
            "floor-not-vote",
            "三个等级3,2,3为何最终是2？",
            "先算均值8/3，再向下取整；不是多数票3，也不是四舍五入3。",
            "教学例：1,0,1均值2/3，最终0。",
            "Why do grades3,2,3produce2?",
            "Floor the mean8/3; do not take majority vote or nearest rounding.",
            "Teaching example:1,0,1has mean2/3and final label0.",
        ),
        (
            "evidence-versus-hidden-state",
            "与FUSE的验证有什么不同？",
            "ExecJudges映射文本证据，FUSE对隐藏动机模拟状态核验；聚合正确不保证证据判断正确。",
            "教学例：三个程序都误判exact，floor仍可能错；不能当成隐藏动机推断成功。",
            "How does this differ from FUSE verification?",
            "ExecJudges maps textual evidence; FUSE verifies reasoning against hidden simulated motives. Correct aggregation does not make evidence judgments correct.",
            "Teaching example: all three programs may misread exact evidence and still aggregate incorrectly.",
        ),
        (
            "qrels-and-code-isolation",
            "完整实现还必须保护哪些边界？",
            "测试qrels不进入writer，生成代码要在禁网/禁模型调用的资源沙箱运行；本地不提供这种沙箱。",
            "教学例：能返回四个bool的Python函数不等于可安全执行不可信代码。",
            "What boundaries remain for a full implementation?",
            "Keep test qrels from the writer and execute generated code under no-network/no-model resource isolation. The local interface is not that sandbox.",
            "Teaching example: a function returning four booleans does not make untrusted code safe to execute.",
        ),
    ],
}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def main():
    figures.CACHE = CACHE
    metadata = {
        p["canonical_id"]: p
        for p in json.loads((ROOT / ".cache/nov19-latest/metadata-pool.json").read_text())["papers"]
    }
    metadata["2611.02643"] = {"published": "2026-11-02T07:04:42Z"}
    existing = {
        p["domain"] + ":" + p["key"]: ROOT / "docs" / p["detail_path"]
        for p in json.loads((ROOT / "docs/research-manifest.json").read_text())["papers"]
    }
    questions, translations, proposals, reviews = {}, {}, [], []
    for p in PAPERS:
        identity = p["domain"] + ":" + p["key"]
        detail = (
            ("recommendation-components" if p["domain"] == "recommendation" else p["domain"])
            + "/"
            + p["id"]
            + "-"
            + p["key"]
            + "/README.md"
        )
        page = ROOT / "docs" / detail
        page.parent.mkdir(parents=True, exist_ok=True)
        figures.original_figure(p, page)
        date = metadata[p["id"]]["published"]
        code_cn = "固定v1及关联来源未找到可获取的本论文专用作者代码；依赖仓库不计为本篇开源。"
        code_en = "No accessible paper-specific author implementation found in fixed v1 and linked sources; dependency repositories do not count as this paper code."
        module = "src/auto_research/" + p["module"]
        command = f"PYTHONPATH=src python -c 'from auto_research.{p['module'][:-3].replace('/', '.')} import diagnostic; print(diagnostic(42, device=\"cpu\"))'"
        body = f"""# {p["name"]}

[English](README-en.md)

> {p["tier"]}：低成本组件/接口诊断，不是完整模型能力证据，不接入Evolve晋级。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [{p["title"]}](https://arxiv.org/abs/{p["id"]}v1)；[固定v1全文](https://arxiv.org/html/{p["id"]}v1) |
| 公司 / 作者机构 | 一作 {p["author"]}：{p["institution"]}；按固定v1及正文核验，不由同名作者/前作推断 |
| 首次公开日期 | {date.replace("T", " ").replace("Z", " UTC")}（arXiv v1；与公告/目录更新时间分开） |
| 原作者开源代码 | {code_cn} |
| 本地adapter / 稳定键 | `{p["key"]}`；adapter=null，仅独立组件 |
| 本地复现代码目录 | `{module}` |

## 原始论文总结

### 背景与主要改动

{p["cn"]}

<!-- paper-figure:start -->
### 原论文关键图

![原文 Figure {p["figure"]}](assets/paper-figure-01.png)

图片来自[原论文](https://arxiv.org/pdf/{p["id"]}v1)，版权归原作者所有。原始图/PDF裁剪，不是本地结果；[出处与SHA256](assets/provenance.json)。
<!-- paper-figure:end -->

### 核心公式

$$
{p["formula"]}
$$

{p["method_cn"]}

### 论文离线与线上效果

{p["result_cn"]}

## 本地复现与边界

### 数据协议与代码映射

{p["limits_cn"]}

```bash
{command}
```

### 结果、负控与边界

三种子42/43/44只检查数值、协议、失败负控和梯度，不是独立能力试验。[CPU诊断](metrics/component-cpu-seeds42-44.json)。{"CUDA张量路径另需实际A100/A30回执，不能用CPU代替。" if p["gpu"] else "CPU协议无需GPU，不制造CUDA执行记录。"}

### 高成本完整实验

{p["cost_cn"]} **成本过高，不复现（审查 DONE）**；不自动重试、不进入训练队列。低成本组件通过不改变此结论。

### 同主题对照

{p["contrast_cn"]}
"""
        page.write_text(body)
        fingerprint = hashlib.sha256(page.read_bytes()).hexdigest()
        en = f"""<!-- source-sha256: {fingerprint} -->
# {p["title"]}

[简体中文](README.md)

> {p["tier"]}: bounded component/interface diagnostic, not complete capability evidence or Evolve promotion.

## Paper information

| Field | Content |
| --- | --- |
| Paper | [arXiv fixed v1](https://arxiv.org/abs/{p["id"]}v1); [full text](https://arxiv.org/html/{p["id"]}v1) |
| Institution | First author {p["author"] if p["key"] != "mars-fapo" else "MARS Team (collective byline)"}: {p["institution"] if p["key"] != "xsplit-argus" else "not listed in fixed v1; not inferred from names or an earlier paper"} |
| First publication | {date.replace("T", " ").replace("Z", " UTC")}; separate from announcement/directory dates |
| Original source code | {code_en} |
| Local adapter / key | `{p["key"]}`; adapter=null, independent component only |
| Local implementation | `{module}` |

## Paper summary

### Motivation and changes

{p["en"]}

<!-- paper-figure:start -->
### Original figure

![Original Figure {p["figure"]}](assets/paper-figure-01.png)

From the [original paper](https://arxiv.org/pdf/{p["id"]}v1); copyright belongs to the original authors. Original asset/PDF crop, not local results. [Provenance](assets/provenance.json).
<!-- paper-figure:end -->

### Core formulas

$$
{p["formula"]}
$$

{p["method_en"]}

### Author results

{p["result_en"]}

## Local implementation and boundaries

### Data protocol and code mapping

{p["limits_en"]}

```bash
{command}
```

### Results, controls and limits

Seeds42/43/44 check arithmetic, protocols, negative controls and gradients, not independent capability trials. [CPU diagnostics](metrics/component-cpu-seeds42-44.json). {"CUDA needs actual A100/A30 execution evidence, never CPU substitution." if p["gpu"] else "CPU-only protocols need no GPU or fabricated CUDA record."}

### High-cost full experiments

{p["cost_en"]} **Not reproduced due to high cost; review DONE.** No automatic retry/training queue. Passing the small component does not change that disposition.

### Same-topic comparison

{p["contrast_en"]}
"""
        page.with_name("README-en.md").write_text(en)
        spec = dict(
            domain=p["domain"],
            key=p["key"],
            title=p["title"],
            paper_url=f"https://arxiv.org/abs/{p['id']}v1",
            reviewed_version_url=f"https://arxiv.org/html/{p['id']}v1",
            reviewed_version="v1",
            published=date[:10],
            published_at=date,
            detail_path=detail,
            topic=p["topic"],
            first_author=p["author"],
            first_author_affiliation=p["institution"],
            verified_priority_organizations=p["priority_orgs"],
            code=None,
            code_status=code_cn,
            method_source_sha256=hashlib.sha256(
                (CACHE / (p["id"] + "v1.html")).read_bytes()
            ).hexdigest(),
            adapter=None,
            priority="P0" if p["priority_orgs"] else "P1",
            intake_class="historical_directory_backfill"
            if p["key"] == "searchinject"
            else "new_paper",
            implementation_status="component_only",
            evaluation_tier=p["tier"],
            diagnostic_only=True,
            promotion_eligible=False,
            evolve_integrated=False,
            requires_gpu_validation=p["gpu"],
            full_experiment_status="not_reproduced_high_cost",
            full_experiment_review_done=True,
            review_resolution="not_reproduced_high_cost",
            review_done=True,
            automatic_retry=False,
            automatic_implementation_queue=False,
            cost_assessment={
                "source": f"https://arxiv.org/pdf/{p['id']}v1",
                "available_resource": "one A100/A30 or local Mac",
                "paper_configuration": p["cost_en"],
                "basis": p["cost_cn"],
                "decision": "成本过高，不复现（审查 DONE）",
            },
            summary=p["cn"] + " 本地边界：" + p["limits_cn"],
            local_operator="auto_research." + p["module"][:-3].replace("/", ".") + ".diagnostic",
            local_command=command,
        )
        if p["gpu"]:
            spec.update(
                gpu_validation_passed=False,
                gpu_validation_artifact=f"docs/gpu-validations/{p['key']}-a100-20261119-latest.json",
            )
        dump(ROOT / f"src/auto_research/paper_specs/catalog/{p['domain']}/{p['key']}.json", spec)
        rows = []
        for level, q in zip(
            ("basics", "mechanism", "comparison", "implementation"), QA[p["key"]], strict=True
        ):
            qid, cnq, cna, cnex, enq, ena, enex = q
            row = dict(
                id=qid,
                level=level,
                question=cnq,
                answer=cna,
                example=cnex,
                source_sections=[
                    "背景与主要改动",
                    "核心公式",
                    "数据协议与代码映射",
                    "高成本完整实验",
                    "同主题对照",
                ],
                added=DATE,
            )
            rows.append(row)
            translations[f"qa/{identity}/{qid}"] = {
                "reviewed": True,
                "fields": {"question": enq, "answer": ena, "example": enex},
            }
        questions[identity] = {"questions": rows}
        peer = p["compare"]
        revisions = {
            identity: fingerprint,
            peer: hashlib.sha256(existing[peer].read_bytes()).hexdigest(),
        }
        proposals.append(
            dict(
                paper=identity,
                target_card=p["card"],
                source_revisions=revisions,
                comparison={
                    "position": p["cn"],
                    "tradeoff": p["contrast_cn"],
                    "sections": ["背景与主要改动", "核心公式", "同主题对照"],
                },
                analysis={
                    "title": p["name"] + "：机制和证据边界",
                    "body": p["method_cn"] + " " + p["contrast_cn"],
                    "papers": [identity, peer],
                },
                question={
                    "id": "cross-nov19-" + p["key"],
                    "question": rows[2]["question"],
                    "answer": rows[2]["answer"],
                    "example": rows[2]["example"],
                    "papers": [identity, peer],
                },
                update={
                    "date": DATE,
                    "papers": [identity, peer],
                    "summary": p["limits_cn"] + " 完整高成本实验不复现，审查DONE。",
                },
                english={
                    "comparison": {"position": p["en"], "tradeoff": p["contrast_en"]},
                    "analysis": {
                        "title": p["key"] + ": mechanism and evidence boundaries",
                        "body": p["method_en"] + " " + p["contrast_en"],
                    },
                    "question": translations[f"qa/{identity}/{rows[2]['id']}"]["fields"],
                    "update": p["limits_en"]
                    + " Full high-cost experiments are not reproduced; review DONE.",
                },
            )
        )
        reviews.append(
            spec
            | {
                "id": p["id"],
                "source_locations": [
                    "fixed-v1 author byline",
                    "method and formulas",
                    "experiments and limitations",
                ],
                "selection_reason": p["result_cn"],
                "source_url": spec["reviewed_version_url"],
            }
        )
    units = question_units({k: v["questions"] for k, v in questions.items()})
    for key, value in translations.items():
        value["source_sha256"] = units[key].source_sha256
    dump(
        ROOT / "docs/learning/questions/nov19-latest-root.json",
        {"schema_version": 1, "papers": questions},
    )
    dump(
        ROOT / "docs/en/learning/translations/qa-nov19-latest-root.json",
        {"schema_version": 1, "units": translations},
    )
    dump(
        AUDIT / "deep-dive-proposals-root.json",
        {"schema_version": 1, "reviewed_on": DATE, "proposals": proposals},
    )
    dump(
        AUDIT / "root-review.json",
        {
            "schema_version": 1,
            "reviewed_on": DATE,
            "papers": reviews,
            "all_sources_exhaustive": False,
        },
    )
    print(json.dumps({"root_papers": len(reviews), "authored_bilingual_questions": len(units)}))


if __name__ == "__main__":
    main()
