"""Authored Nov21 DFRL/e-RWSC write-ups and reviewed bilingual learning bundles.

This script touches only these two new papers and this author's audit bundles.
It does not execute research models, synthesize a paper's method from an abstract,
or update shared manifests, question banks, or topic history.
"""

from hashlib import sha256
import json
from pathlib import Path

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-21"
AUDIT = ROOT / "docs/research-audits/nov21-latest"
CACHE = ROOT / ".cache/nov21-latest/post-primary"

PAPERS = {
    "dfrl": {
        "domain": "post-training", "id": "2611.25597", "module": "post_training.dfrl",
        "title": "Decision-Focused Reinforcement Learning for LLM Post-Training",
        "author": "Haotian Zhai", "affiliation": "The University of Texas at Austin",
        "stamp": "2026-11-19T06:44:35Z", "topic": "policy-optimization", "peer": "post-training:rloo",
        "figure": (5, "Figure 1", [66, 60, 530, 373]),
        "caption": "DFRL pipeline with RLOO as an example: context, parameter predictions, downstream optimization, observed-parameter decision regret, and policy update. The shared hindsight optimum cancels in RLOO advantages.",
        "sections": ["PDF p1 byline", "Section3 Eq.4-13", "AppendixB.3", "AppendixB.5"],
        "method": "预测误差小不保证由预测触发的决策成本低。DFRL把LLM生成的参数预测交给下游优化器，以真实观测参数评估该决策，再把负决策regret用于后训练；不对优化器求导。它是目标/反馈框架，不是另一个替代RLOO的策略优化器。对同一实例独立生成K≥2条预测时，RLOO的实例内leave-one-out baseline抵消共同的hindsight最优成本，因此更新不必额外求真实参数下的最优解。\n\n昂贵精确反馈有两种处理：heuristic warm-start先用便宜可行决策的成本，按validation确定的边界切换精确成本；它有偏。reward correction则为整批M×K预测只抛一个Bernoulli(p)：选中时求全部精确成本并作逆概率校正，没选中时只用便宜估计。便宜估计可以有偏，校正对该批随机开关求期望恢复精确梯度，但增大方差，不保证更快收敛。",
        "method_en": "Lower prediction error need not imply lower induced decision cost. DFRL passes an LLM's parameter prediction to a downstream optimizer, evaluates the decision under observed parameters, and post-trains with negative decision regret without differentiating through the optimizer. It specifies an objective and feedback pipeline, not an optimizer replacing RLOO. With K at least two independent predictions per instance, the within-instance leave-one-out baseline cancels the common hindsight optimum, so the update need not solve the problem under the observed parameters.\n\nTwo schemes reduce expensive feedback. Heuristic warm-starting first uses costs of cheap feasible decisions and switches to exact costs at a validation-selected boundary; its early gradient is biased. Reward correction draws one Bernoulli(p) for the entire M-by-K batch: selected batches solve every exact decision and apply inverse-probability correction, while unselected batches use cheap estimates alone. Cheap estimates may be biased; expectation over the batch switch recovers the exact gradient but introduces variance, not a guaranteed speedup.",
        "formula": r"A_{mk}=-C_{mk}+\frac{1}{K-1}\sum_{j\ne k}C_{mj},\qquad \widehat A_{mk}=\widetilde A_{mk}+\frac{I}{p}(A_{mk}-\widetilde A_{mk}),\qquad I\sim\operatorname{Bernoulli}(p).",
        "extra": "这里单个I共享给整批，不是对每token或候选独立选择后仍声称复刻Eq.12。I=0时不要求也不调用精确求解器；优势不可再做组内标准差归一化，否则不再是所分析的无偏估计。成本越低优势越高，不能把成本当正奖励。p过小可能使单批校正极大。",
        "extra_en": "One I is shared by the whole batch, not sampled independently per token or candidate while claiming Equation12. I=0 neither requires nor invokes the exact solver. Do not additionally standardize advantages by group standard deviation: that changes the analyzed estimator. Lower cost yields higher advantage; cost is not a positive reward. Very small p can cause large single-batch corrections.",
        "result": "原文在H&M库存规划中报告带reasoning的最佳配置相对SFT减少31.4% regret、相对最强常规预测基线减少12.4%。这两项是离线决策regret，不是预测准确率或生产A/B；未报告线上A/B。便宜反馈的方差/偏差与精确求解时间决定净收益，本地小问题解析梯度检查不验证4B模型的业务改善。",
        "result_en": "On H&M inventory planning, the paper's best reasoning configuration reduces decision regret by31.4% relative to SFT and12.4% relative to the strongest conventional forecasting baseline. These are offline decision-regret results, not predictive accuracy or production A/B; no online A/B is reported. Exact-solve time and the bias/variance of cheap feedback determine net efficiency. Local tiny-problem gradient checks do not verify4B-model business improvements.",
        "scope": "纯stdlib、CPU-only的实际成本RLOO优势、单批共享Bernoulli逆概率校正与lazy整批精确成本回调、显式warm-start边界、小规模枚举knapsack。诊断对三个可采样参数预测的真实可行决策计算观测成本，穷举两个独立categorical样本的score-gradient期望并与解析梯度比较；偏置cheap成本仅为明确的负控输入，不冒充训练好的估计器。没有LLM、token生成、参数JSON解析器、H&M处理、Adam训练或能力评测；非Evolve算子。",
        "scope_en": "Pure-standard-library, CPU-only realized-cost RLOO advantages, one-batch Bernoulli inverse-probability correction with a lazy whole-batch exact-cost callback, an explicit warm-start boundary, and tiny exact knapsack enumeration. Diagnostics compute observed costs of real feasible decisions for three sampleable parameter predictions, enumerate the score-gradient expectation of two independent categorical samples, and compare it with the analytic gradient. Biased cheap costs are explicit negative-control inputs, not a trained estimator. No LLM, token generation, parameter-JSON parser, H&M pipeline, Adam training, capability evaluation or Evolve operator is supplied.",
        "cost": "AppendixB.5使用Qwen3.5-4B、4013个SFT实例，四个non-thinking RL条件各64更新×16实例×8响应=8192条训练响应，并有学习率选择、reasoning教师/额外SFT与评测；另有三合成问题、多种子与一小时预算实验。完整矩阵远超本轮30秒/seed的CPU定义核预算。8192是论文配置计算，不是本机实测；不下载模型、H&M或调用教师。",
        "cost_en": "AppendixB.5 uses Qwen3.5-4B and4,013 SFT instances; each of four non-thinking RL conditions has64 updates times16 instances times8 responses, or8,192 training responses, plus learning-rate selection, a reasoning teacher, extra SFT and evaluation. Separate synthetic-problem, multi-seed and one-hour-budget studies add cost. This matrix exceeds this batch's30-second-per-seed CPU component budget.8,192 is configuration arithmetic, not a local measurement; no model, H&M data or teacher API is downloaded or called.",
        "compare": "已有RLOO实现把整条response作为action，用其他response的奖励均值作baseline，并可加KL shaping。DFRL在这里指定奖励来自下游真实决策成本；其文中RLOO分析抵消共同hindsight常数，reward correction用整批开关减少昂贵反馈调用。RLOO没有自动定义什么是业务regret；DFRL也没有使任意归一化、clipping或候选相关baseline都保持无偏。两者是目标/反馈与估计器两个维度，而非互斥算法。",
        "compare_en": "Existing RLOO treats a complete response as an action, baselines its reward against the other responses, and may add KL shaping. DFRL specifies downstream realized decision cost as feedback; its RLOO analysis cancels the common hindsight constant, and batch-switch reward correction reduces expensive feedback calls. RLOO does not define business regret automatically, and DFRL does not make arbitrary normalization, clipping or candidate-dependent baselines unbiased. They concern an objective/feedback pipeline and an estimator, not mutually exclusive algorithms.",
        "mermaid": 'flowchart LR\n  A["独立参数预测"] --> B["预测参数下求解决策"]\n  B --> C["观测参数下实际成本"]\n  C --> D["实例内RLOO优势"]\n  E["整批Bernoulli：便宜/精确反馈"] --> D\n  D --> F["score-gradient；不穿过优化器"]',
        "questions": [
            ("为什么预测更准不一定决策更好？", "优化器只在可行决策间选择；预测误差若跨过改变最优决策的边界，会有大regret，别处较大的误差却可能不改决策。DFRL直接奖励诱导决策的真实成本，而非每维预测误差。", "教学例：容量只能选一件商品时，两件商品利润接近，微小的排序翻转可选错商品；把两件利润都等量平移虽增大MSE，却可能不改选择。", "Why can a more accurate prediction induce a worse decision?", "An optimizer chooses among feasible decisions. Error crossing a decision boundary can cause large regret, while larger error elsewhere may leave the decision unchanged. DFRL rewards realized induced decision cost rather than coordinate-wise prediction error.", "Teaching example: with capacity for one item and nearly tied profits, a small ranking reversal changes the chosen item. Shifting both predicted profits equally increases MSE but may leave the choice unchanged."),
            ("reward correction为什么只抛一次硬币？", "Eq.12对整批M×K共享I；I=1时计算该批全部精确优势，并以1/p校正便宜优势，否则整批跳过精确求解。实例内baseline仍分别计算，不能把不同实例混在一起。", "教学例：M=2、K=2、p=1/4时，一次更新要么做4次精确求解，要么0次，期望1次；这不是每条独立抽一次的原文实现。", "Why does reward correction use one coin flip?", "Equation12 shares I across the whole M-by-K batch. I=1 obtains every exact advantage and corrects cheap advantages by1/p; otherwise all exact solves are skipped. Baselines remain within each instance, not across instances.", "Teaching example: with M=2,K=2,p=1/4, an update makes either four exact solves or zero, averaging one. Independent per-response coins are not the specified implementation."),
            ("DFRL是替代RLOO的另一种优化器吗？", "不是。DFRL指定决策regret目标和反馈，RLOO可作为其无偏score-gradient估计器。相同实例的hindsight最优成本在baseline中抵消，但任意优势标准化或KL shaping都会改变原文分析的目标/更新。", "教学例：成本2和5给优势3和负3；同时减去共同hindsight成本1，优势仍是3和负3，不需要多求一次真实参数下的最优解。", "Is DFRL another optimizer replacing RLOO?", "No. DFRL specifies a decision-regret objective and feedback, while RLOO can estimate its score gradient. The shared hindsight optimum cancels from the baseline; arbitrary advantage standardization or KL shaping changes the analyzed objective or update.", "Teaching example: costs2 and5 yield advantages3 and minus3. Subtracting the same hindsight cost1 leaves them unchanged, avoiding another solve under observed parameters."),
            ("没有选中精确反馈时还能先算exact成本吗？", "不能把先求全批exact再屏蔽当作节省求解。本地I=0分支不调用lazy exact回调；I=1只调用一次整批supplier。p必须大于0且不大于1，p很小时方差和溢出风险需显式处理。", "教学例：便宜优势为0、精确优势为4、p=1/4时，选中返回16，未选中返回0，期望4；每批返回16不是稳定收益或收敛保证。", "Can exact costs be computed before deciding to skip them?", "Solving every exact problem and masking afterward does not save solves. The local I=0 branch never calls the lazy callback; I=1 calls the whole-batch supplier once. Require0<p<=1 and handle variance and overflow at small p explicitly.", "Teaching example: with cheap advantage0, exact advantage4 and p=1/4, selected batches return16 and unselected batches0, averaging4. A batch value16 is neither stable gain nor a convergence guarantee."),
        ],
    },
    "e-rwsc": {
        "domain": "foundation-models", "id": "2611.26413", "module": "foundation_models.e_rwsc",
        "title": "Sequential Anytime Valid Tests for Efficient Inference-Time Alignment",
        "author": "Vishesh Kumar Singh", "affiliation": "Indian Institute of Technology Kanpur",
        "stamp": "2026-11-19T17:00:42Z", "topic": "evaluation-and-evidence", "peer": "foundation-models:llm-stochasticity",
        "figure": (13, "Algorithm 2", [106, 420, 530, 735]),
        "caption": "Algorithm2 e-RWSC: predictable bets precede the next sample, each observed answer has its own e-process, first appearances initialize without a bet, and exhausted budgets return an uncertified RWSC fallback.",
        "sections": ["PDF p1 byline", "Section2 Eq.1-2", "Section3 Eq.6-10", "AppendixA Algorithm2", "AppendixD Table5-6"],
        "method": "固定N的Best-of-N对容易题也花满预算；只追踪当前领先答案的SPRT会反复换假设，不能直接沿用Wald错误保证。e-RWSC按答案分别保留e-process，以过去响应的reward-weighted self-consistency质量和首现后的匹配次数构造可预测Kelly下注。新答案第一次出现只登记为单位资本，不把这个由定义强制成功的样本计作证据。所有旧答案的下注先于下一条响应/奖励计算，领先者改变也不重置资本。\n\n答案按首现rank分配可求和权重1/[j(j+1)]；加权资本跨过1/alpha时才发证，选该答案簇内奖励最高的响应。Nmax用尽而无证书时退回RWSC，必须保留uncertified。证明假定固定政策的iid抽样，证书仅说明该答案在政策分布的概率超过阈值，不说明真实正确。奖励影响下注速度而不改变被认证对象；坏reward仍可能使选择/回退表现差。",
        "method_en": "Fixed-N Best-of-N spends the full budget even on easy queries. A leader-tracking SPRT repeatedly changes its hypotheses and cannot inherit Wald's error guarantee. e-RWSC maintains an e-process per answer and makes predictable Kelly bets using past reward-weighted self-consistency masses and post-appearance agreement counts. The first appearance only initializes unit capital; it is not evidence from a success forced by the definition. Every old answer's stake is computed before the next response or reward, and leader changes do not reset capital.\n\nAnswers receive summable first-appearance-rank weights1/[j(j+1)]. A certificate is issued only when weighted capital reaches1/alpha, returning the highest-reward response in that answer cluster. Exhausting Nmax without a certificate falls back to explicitly uncertified RWSC. The guarantee assumes iid draws from a fixed policy and certifies probability above a threshold, not factual correctness. Rewards affect betting speed rather than the certified event; bad rewards may still harm selection or fallback quality.",
        "formula": r"E_n^{(a)}=\prod_{i=\sigma_a+1}^{n}\left[1+\lambda_i^{(a)}\left(\mathbf 1\{A_i=a\}-p^\dagger\right)\right],\quad E_{\sigma_a}^{(a)}=1,\qquad \pi_j=\frac{1}{j(j+1)},\quad \pi_{J(a)}E_n^{(a)}\ge\frac{1}{\alpha}.",
        "extra": "Eq.10先用过去前缀计算theta估计，再把Kelly stake裁到[0,c/p]，c<1保证一次不匹配不把资本清零。实现采用log资本和稳定softmax；零奖励方差按均匀响应权重处理，这是明确的数值约定。仅支持0.5≤p<1的多数认证，精确tie按首现顺序；这些约定不改变为正确性背书的禁令。",
        "extra_en": "Equation10 estimates theta from the past prefix and clips the Kelly stake to[0,c/p], with c<1 preventing one disagreement from wiping out capital. This implementation uses log capital and stable softmax. Zero reward variance uses uniform response weights, an explicit numerical convention. Only majority thresholds0.5<=p<1 are supported; exact ties use first appearance. None of these conventions makes the certificate evidence of factual correctness.",
        "result": "AppendixD Table6的MATH500、Qwen2.5-3B-Instruct与ArmoRM-8B、Nmax512配置报告e-RWSC整体accuracy78.0%、已认证子集94.5%、平均196.1候选；固定预算BoN为69.8%、512候选。已认证子集与整体分母不同，不能把94.5%当全部题的准确率；这些论文结果不是本地测量。未报告生产线上A/B。",
        "result_en": "For MATH500 with Qwen2.5-3B-Instruct, ArmoRM-8B and Nmax512, AppendixD Table6 reports e-RWSC overall accuracy78.0%, certified-subset accuracy94.5% and196.1 mean candidates; fixed-budget BoN uses512 candidates and scores69.8%. The certified subset and full set have different denominators;94.5% is not overall accuracy. These are paper results, not local measurements. No production online A/B is reported.",
        "scope": "纯stdlib、CPU-only的RWSC聚合、前缀可预测下注、逐答案log资本与首现权重、首次出现跳过、认证终止和显式未认证预算回退。诊断使用明确的合成答案/奖励流，检查因果顺序、领先变化不重置、错误答案也可能被认证、softmax极值和均匀tie。没有LLM、reward model、答案解析或公开benchmark运行；不把合成流叫模型输出，不接Evolve晋级。",
        "scope_en": "Pure-standard-library, CPU-only RWSC aggregation, prefix-predictable betting, per-answer log capital and first-appearance weights, skipped first appearances, certified stopping and explicit uncertified budget fallback. Diagnostics use declared synthetic answer/reward streams to check causality, no reset on leader changes, certification of a wrong but concentrated answer, extreme-score softmax and uniform ties. No LLM, reward model, answer extractor, public benchmark run or Evolve promotion is provided; synthetic streams are not model outputs.",
        "cost": "AppendixD在作者RTX6000Ada测量中，每题固定512候选约3657.7GPU秒、e-RWSC平均约1400.8GPU秒，另有多模型、多reward model、多基准矩阵。这是作者硬件的测量，不是本机A100/A30时间预测；完整生成/打分实验直接不复现。本轮只执行廉价CPU停止核，不下载3B/8B或更大模型。",
        "cost_en": "AppendixD measures about3,657.7 GPU seconds per query for512 fixed candidates and about1,400.8 for e-RWSC on the authors' RTX6000Ada, plus a multi-model, multi-reward-model, multi-benchmark matrix. These are measurements on their hardware, not A100/A30 time estimates. Full generation and scoring are not reproduced. Only the cheap CPU stopping kernel runs; no3B/8B or larger models are downloaded.",
        "compare": "LLM Stochasticity区分边缘分布拟合与时序依赖；e-RWSC的保证需要固定政策的iid响应，不能由平衡答案直方图或“请随机回答”提示推导。前者的统计诊断可暴露某些依赖，却不能证明后者的全部假设。e-RWSC也不估计答案是否符合现实：即使输入真独立，政策总偏向错误答案时仍可快速发多数证书。",
        "compare_en": "LLM Stochasticity distinguishes marginal distribution fit from temporal dependence. e-RWSC requires iid responses from a fixed policy; a balanced answer histogram or a prompt asking for randomness does not establish that assumption. Statistical diagnostics can expose some dependence but do not prove every certification assumption. e-RWSC also does not establish factual truth: even genuinely independent draws from a policy concentrated on a wrong answer can certify that majority quickly.",
        "mermaid": 'flowchart LR\n  A["只看过去前缀计算下注"] --> B["获得下一响应与reward"]\n  B --> C["结算所有旧答案e-process"]\n  C --> D["新答案首现：E=1，不下注"]\n  D --> E{"rank加权资本过界？"}\n  E -->|是| F["多数证书；非正确性保证"]\n  E -->|否且预算尽| G["uncertified RWSC回退"]\n  E -->|继续| A',
        "questions": [
            ("e-RWSC证书是在证明答案正确吗？", "不是。它在固定政策iid抽样假设下控制误认证非多数答案的概率，认证的是政策分布中的占优概率，而不读取或判断真实答案。", "教学例：假设政策几乎总把2+2回答成5，5也可能很快获得多数证书；这不让5变成正确答案。", "Does an e-RWSC certificate prove the answer is correct?", "No. Under iid sampling from a fixed policy, it controls false certification of a non-majority answer. It certifies dominance in the policy distribution, without reading or judging the gold answer.", "Teaching example: if a policy almost always answers5 to2+2,5 can quickly obtain a majority certificate without becoming correct."),
            ("为什么新答案第一次出现不能立即增长资本？", "首现时这个样本等于该答案是由定义强制的，不是此前可预测下注的随机成功；因此只登记E=1和Z=0，从下一条响应才开始结算。", "教学例：第一个答案出现后资本仍为1，rank1权重为1/2；不能把第一次出现当作一次押中而直接加大证据。", "Why must first appearance not immediately grow capital?", "The answer matching its first observation is forced by the definition, not a success of a previously predictable bet. Initialize E=1 and Z=0, then settle bets starting at the next response.", "Teaching example: after the first answer appears, its capital remains1 with rank-one weight1/2. Counting its appearance as a successful wager invents evidence."),
            ("答案直方图均匀，是否就满足iid保证？", "不满足。LLM Stochasticity说明边缘分布平衡仍可有确定性时序依赖；e-RWSC的固定政策独立抽样假设不能靠均匀图或随机提示替代。", "教学例：0、1、2、3无限循环时各值频率相等，但下一值可由上一值确定；这不是四分类iid采样。", "Does a uniform answer histogram establish iid sampling?", "No. LLM Stochasticity shows that balanced marginal frequencies can coexist with deterministic temporal dependence. A histogram or randomness prompt cannot replace e-RWSC's fixed-policy independent-sampling assumption.", "Teaching example: an endless0,1,2,3 cycle has equal frequencies, yet each next value is determined by its predecessor; it is not iid categorical sampling."),
            ("达到Nmax但没跨界，可以标为已认证吗？", "不能。返回的是reward-weighted self-consistency回退，certified必须为false。还要检查当前下注只看旧前缀，新响应的答案和极端reward都不能倒灌到刚才的stake。", "教学例：两个进程共享同一过去前缀，下一奖励分别是正一百万和负一百万；它们结算本步前的下注必须相同，预算用尽也不会补发证书。", "Can an Nmax-exhausted answer be labeled certified?", "No. It is a reward-weighted self-consistency fallback with certified=false. Also check that each stake uses only the old prefix: the incoming answer or an extreme reward cannot influence the stake just being settled.", "Teaching example: two processes share a prefix but their next rewards are plus and minus one million. Their pre-settlement stakes must match; exhausting the budget does not create a certificate."),
        ],
    },
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False)+"\n")


def main():
    import fitz

    bundle, english_units, proposals, reviews = {}, {}, [], []
    for key, c in PAPERS.items():
        identity = c["domain"]+":"+key
        source = f"https://arxiv.org/html/{c['id']}v1"
        pdf = CACHE / f"{c['id']}.pdf"
        local = f"src/auto_research/{c['module'].replace('.', '/')}.py"
        detail = f"{c['domain']}/{c['id']}-{key}/README.md"
        directory = ROOT / "docs" / c["domain"] / f"{c['id']}-{key}"
        assets = directory / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        document = fitz.open(pdf)
        page, figure, crop = c["figure"]
        target = assets / "paper-figure-01.png"
        document[page-1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(crop)).save(target)
        figure_url = f"https://arxiv.org/pdf/{c['id']}v1#page={page}"
        write(assets / "provenance.json", {"schema_version": 1, "paper_url": source,
            "source_url": figure_url, "source_sha256": digest(pdf), "pdf_page": page,
            "figure": figure, "caption": c["caption"], "crop_pdf_points": crop,
            "render_scale": 2, "asset_sha256": digest(target), "image_sha256": digest(target),
            "visually_reviewed": True, "scientific_content_modified": False,
            "copyright": "Copyright remains with original authors; original screenshot with attribution."})
        command = f"PYTHONPATH=src python -c 'from auto_research.{c['module']} import diagnostic; print(diagnostic(42))'"
        code_cn = "截至2026-11-21，固定v1作者入口与全文未找到已核实的本篇方法源码仓库；引用项目不等于本篇开源。"
        code_en = "As of2026-11-21, no verified paper-specific author code repository was found in the fixed-v1 author entry or full text; cited projects do not establish release of this method."
        cn = f'''# {c['title']}

[English](README-en.md)

> **L1核心机制组件，diagnostic only；不是LLM能力或完整论文复现。** 纯CPU，无CUDA宣传路径；不作为Evolve晋级证据。完整实验成本过高，不复现（审查 DONE）。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [arXiv:{c['id']}v1](https://arxiv.org/abs/{c['id']}v1)；[固定v1原文]({source}) |
| 公司 / 作者机构 | 一作 **{c['author']}**；**{c['affiliation']}** |
| 首次公开日期 | **{c['stamp']}**；本轮2026-11-21为重叠池新选题，不是11月20/21新首发 |
| 原作者开源代码 | {code_cn} |
| 本地 adapter / key | `{key}`；`adapter: null`，独立CPU组件 |
| 本地复现代码 | `{local}` |

## 原始论文总结

### 背景与主要改动

{c['method']}

<!-- paper-figure:start -->
### 原论文关键图

[![原论文 {figure}](assets/paper-figure-01.png)]({figure_url})

图片来自[原论文]({figure_url})第{page}页{figure}完整截图，版权归原作者所有；已视觉核对，无科学内容改动。[原图裁剪与SHA256](assets/provenance.json)。图示属于作者方法，不是本地运行结果。
<!-- paper-figure:end -->

```mermaid
{c['mermaid']}
```

### 核心公式

$$
{c['formula']}
$$

{c['extra']}

### 论文离线与线上效果

{c['result']}

### 与已有方法的关系

{c['compare']}

## 本地复现

### 数据协议与代码映射

{c['scope']}

```bash
{command}
PYTHONPATH=src python -m pytest -q tests/test_nov21_{'e_rwsc' if key == 'e-rwsc' else 'dfrl'}.py
```

### 结果、负控与边界

统一三种子CPU产物为[`metrics/component-cpu-seeds42-44.json`](metrics/component-cpu-seeds42-44.json)。这里只检查定义核与负控；没有下载数据或权重，没有训练模型或宣称benchmark收益。单元测试不能替代真实模型能力评测。公开的CPU路径显式拒绝`device="cuda"`，因此不伪造GPU验收；若未来新增CUDA宣传路径，必须另做真实A100/A30验证。

### 高成本完整实验

{c['cost']}

**成本过高，不复现（审查 DONE）**。不尝试长时探针、不扩大训练、不加入自动重试队列。可用预算是一张A100或A30，或本地Mac；本轮仅运行每seed最多30秒的CPU组件，不假设多卡或两台同时可用。
'''
        (directory / "README.md").write_text(cn)
        cn_hash = digest(directory / "README.md")
        en = f'''# {c['title']}

<!-- source-sha256: {cn_hash} -->

[简体中文](README.md)

> **L1 mechanism component, diagnostic only; not LLM capability or a full paper reproduction.** CPU only, with no advertised CUDA path or Evolve-promotion evidence. High-cost full experiments are not reproduced (review DONE).

## Paper information

| Field | Value |
| --- | --- |
| Paper | [arXiv:{c['id']}v1](https://arxiv.org/abs/{c['id']}v1); [fixed-v1 text]({source}) |
| First author / institution | **{c['author']}**, **{c['affiliation']}** |
| Original publication | **{c['stamp']}**; selected from the overlap pool on2026-11-21, not a Nov20/21 first release |
| Original author code | {code_en} |
| Local adapter / key | `{key}`; `adapter: null`, independent CPU component |
| Local code | `{local}` |

## Original paper

### Background and method

{c['method_en']}

### Key original figure

[![Original {figure}](assets/paper-figure-01.png)]({figure_url})

Original {figure}, complete screenshot from fixed-v1 PDF page{page}; copyright belongs to the authors. Visually checked, without scientific-content changes. [Original source]({figure_url}); [crop and SHA256 provenance](assets/provenance.json). This depicts the authors' method, not local results.

### Core formula

$$
{c['formula']}
$$

{c['extra_en']}

### Reported results

{c['result_en']}

### Relationship to existing methods

{c['compare_en']}

## Local implementation

### Data protocol and code mapping

{c['scope_en']}

```bash
{command}
PYTHONPATH=src python -m pytest -q tests/test_nov21_{'e_rwsc' if key == 'e-rwsc' else 'dfrl'}.py
```

### Results, controls and limits

The unified three-seed CPU artifact is[`metrics/component-cpu-seeds42-44.json`](metrics/component-cpu-seeds42-44.json). It checks mechanism definitions and controls, with no data/checkpoint download, model training or benchmark-gain claim. Unit tests are not capability evaluation. The public CPU path rejects`device="cuda"`; no GPU validation is fabricated. Any future advertised CUDA path requires separate real A100/A30 validation.

### High-cost full experiment

{c['cost_en']}

**High cost: not reproduced (review DONE).** No lengthy probe, expanded training or automatic retry queue. Available resources are one A100 or A30, or a local Mac. This batch runs only CPU components capped at30 seconds per seed, without assuming multiple GPUs or simultaneous access to both hosts.
'''
        (directory / "README-en.md").write_text(en)
        spec = {"domain": c["domain"], "key": key, "title": c["title"],
            "paper_url": f"https://arxiv.org/abs/{c['id']}v1", "reviewed_version_url": source,
            "reviewed_version": "v1", "detail_path": detail, "first_author": c["author"],
            "first_author_affiliation": c["affiliation"], "published": c["stamp"][:10], "published_at": c["stamp"],
            "code": None, "code_status": code_cn, "code_license": None, "upstream_revision": None,
            "adapter": None, "topic": [c["topic"], "CPU机制组件"], "priority": "P1",
            "intake_class": "overlap_new_selection", "implementation_status": "component_only",
            "evaluation_tier": "l1_mechanism", "diagnostic_only": True, "promotion_eligible": False,
            "evolve_integrated": False, "requires_gpu_validation": False, "gpu_validation_passed": False,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
            "review_done": True, "review_resolution": "not_reproduced_high_cost",
            "automatic_retry": False, "automatic_implementation_queue": False,
            "cost_assessment": {"source": source, "source_sections": c["sections"], "basis": c["cost"],
                "available_resource": "One A100 or A30, or local Mac; this implementation is CPU-only",
                "decision": "High-cost full experiments not reproduced; review DONE, no automatic retry.",
                "local_budget": {"checkpoint_download_bytes": 0, "dataset_download_bytes": 0,
                    "paid_api_calls": 0, "local_component_seconds_per_seed_cap": 30}},
            "summary": c["method"].split("\n")[0]+" "+c["scope"],
            "local_operator": f"auto_research.{c['module']}.diagnostic", "local_command": command,
            "method_source_sha256": digest(pdf)}
        write(ROOT / f"src/auto_research/paper_specs/catalog/{c['domain']}/{key}.json", spec)
        rows = []
        for level, q in zip(("basics", "mechanism", "comparison", "implementation"), c["questions"], strict=True):
            rows.append({"id": "nov21-"+level, "level": level, "question": q[0], "answer": q[1], "example": q[2],
                "source_sections": ["背景与主要改动", "核心公式", "与已有方法的关系", "结果、负控与边界"], "added": DATE})
        bundle[identity] = {"questions": rows}
        units = question_units({identity: rows})
        for row, q in zip(rows, c["questions"], strict=True):
            uid = f"qa/{identity}/{row['id']}"
            english_units[uid] = {"source_sha256": units[uid].source_sha256, "reviewed": True,
                "fields": {"question": q[3], "answer": q[4], "example": q[5]}}
        peer_domain, peer_key = c["peer"].split(":")
        peer = json.loads((ROOT / f"src/auto_research/paper_specs/catalog/{peer_domain}/{peer_key}.json").read_text())
        peer_hash = digest(ROOT / "docs" / peer["detail_path"])
        q = c["questions"][2]
        proposals.append({"paper": identity, "target_card": c["domain"]+"/"+c["topic"],
            "source_revisions": {identity: cn_hash, c["peer"]: peer_hash},
            "comparison": {"position": c["scope"], "tradeoff": c["compare"],
                "sections": ["背景与主要改动", "与已有方法的关系", "结果、负控与边界"]},
            "analysis": {"title": q[0], "body": c["compare"]+" "+c["questions"][3][1], "papers": [identity, c["peer"]]},
            "question": {"id": "nov21-"+key, "question": q[0], "answer": q[1], "example": q[2], "papers": [identity, c["peer"]]},
            "update": {"date": DATE, "papers": [identity, c["peer"]], "summary": c["scope"]+" 完整实验成本过高不复现；组件不构成能力晋级。"},
            "english": {"comparison": {"position": c["scope_en"], "tradeoff": c["compare_en"]},
                "analysis": {"title": q[3], "body": c["compare_en"]+" "+c["questions"][3][4]},
                "question": {"question": q[3], "answer": q[4], "example": q[5]},
                "update": c["scope_en"]+" High-cost full experiments are not reproduced; components do not establish capability promotion."}})
        reviews.append({"id": c["id"], "key": key, "domain": c["domain"], "title": c["title"],
            "first_author": c["author"], "affiliation": c["affiliation"], "published_at": c["stamp"],
            "announced_on": "2026-11-20", "selected_on": DATE, "intake_class": "overlap_new_selection",
            "reviewed_version": "v1", "source_url": source, "pdf_sha256": digest(pdf),
            "html_sha256": digest(CACHE / f"{c['id']}.html"), "sections": c["sections"],
            "gpu": False, "tier": "l1_mechanism", "scope": c["scope"], "cost": c["cost"],
            "code": None, "upstream_revision": None, "review_done": True,
            "repository_status_before_batch": "not_in_manifest_or_ledger_by_arxiv_id",
            "full_experiment_status": "not_reproduced_high_cost", "automatic_retry": False,
            "automatic_implementation_queue": False, "local_module": local,
            "english_source_sha256": cn_hash})
    write(AUDIT / "post-authored-bundle.json", {"schema_version": 1, "date": DATE, "papers": bundle,
        "english_question_units": english_units, "integration_owner": "root"})
    write(AUDIT / "deep-dive-proposals-post.json", {"schema_version": 1, "reviewed_on": DATE,
        "integration_owner": "root", "proposals": proposals})
    write(AUDIT / "post-review.json", {"schema_version": 1, "reviewed_on": DATE, "owner": "nov21_post_review",
        "coverage": "Two selected Nov19 overlap methods; no Nov20/21 first-release or exhaustive-coverage claim.",
        "google_meta_authorship": "Neither fixed-v1 first author is Google/Meta; cited models do not establish affiliation.",
        "accepted": reviews, "not_selected_this_batch": [
            {"id": "2611.26510", "title": "AutoMaster", "decision": "not_selected_this_finite_intake",
             "reason": "Useful autonomous Skill-FT system, but a serving/control interface would omit the defining teacher/rollout/SFT loop; selected two independent executable objective/stopping cores instead.", "automatic_retry": False},
            {"id": "2611.25391", "title": "HOPD", "decision": "not_selected_this_finite_intake",
             "reason": "Domain-specific continual SAR MLLM and historical-teacher loop; avoid a generic-KL placeholder or another expensive source-by-source training matrix this batch.", "automatic_retry": False}]})
    print("Authored2 bilingual paper pairs,8 reviewed QA,2 same-topic proposals; shared banks untouched.")


if __name__ == "__main__":
    main()
