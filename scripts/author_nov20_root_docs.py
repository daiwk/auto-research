"""One-shot bilingual industrial-paper write-ups for root-owned components.

No algorithms, shared banks, registry or generated catalogs are modified here.
"""

from hashlib import sha256
import json
from pathlib import Path

import fitz

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov20-latest/root"
AUDIT = ROOT / "docs/research-audits/nov20-latest"
DATE = "2026-11-20"

PAPERS = [
    {
        "aid":"2611.26531", "key":"fleet-feature-optimization",
        "title":"Cost-Aware Agentic Feature Optimization System for Fleet-Scale Ranking Models",
        "author":"Chang Yang", "org":"Meta, Inc.", "published_at":"2026-11-19T18:12:04Z",
        "priority":"P0", "module":"fleet_feature_components", "tier":"l1_mechanism", "cuda":False,
        "topic":["研究与服务闭环","特征工程与成本约束"],
        "card":"recommendation/research-serving-loop", "peer":"recommendation:mle-agents",
        "sections":["2–5", "Algorithm1", "Table1"],
        "figure":[2,[52,80,560,255],"Figure 1: fleet-aware feature creation, blending and constrained search"],
        "formula":r"\theta^\star=\arg\min_\theta\operatorname{NE}(\theta),\quad R_k(\theta)\le\rho_kR_k(\theta_0),\qquad \Delta_b=C_b(O_b\cup S)-C_b(O_b\cup I).",
        "diagram":"flowchart LR\n F[External feature importance vectors] --> P[Pareto layers]\n P --> B[Ordered sources and explicit integer quotas]\n B --> T[Set cost oracle trimming and same category refill]\n T --> E[External training and resource measurements]\n E --> W[Lowest feasible improved validation NE]\n L[LLM proposals external] --> B",
        "cn":{
            "overview":"Meta把特征创建、FI估计、跨任务Pareto分层、多来源混合和有约束搜索连成fleet级流程。LLM提出假设，确定性工具验证；每个模型同时面对自身serving限制和跨模型共享的上游pipeline预算。另一个模型已经使用某特征时，新增使用不一定新增pipeline成本。",
            "detail":"FI向量按所有任务的逐维支配关系分层，不先把任务loss相加。多个来源固定顺序取未选特征，论文写round(pi_m N)，却没有规定舍入与末层同分切分；本地将整数quota及层内顺序显式交给调用方。成本使用完整特征集合oracle，不把共享成本猜成各特征价格求和；跨预算的最贵删除顺序也由外部提供。QPS约束必须先变换成1/QPS这种上界口径。",
            "results":"原文七个高影响生产模型在各自预算内平均NE相对降低0.31%；六模型trimming平均降低pipeline成本2.3%，主任务loss变化不超过约+0.03%的测量噪声。线上报告一个未命名主指标+0.20%，未披露本批A/B的流量比例、时长或CI，不能改称CTR/营收。实验只调特征量，混合pi虽已实现但未评测。",
            "local":"仅实现Pareto层、显式quota混合、集合依赖pipeline差值、删除/同类别补回原语和已完成validation trial准入。FI、成本oracle、删除顺序、训练与资源测量都为外部输入。不运行LLM feature proposer、FI估计、异步研究搜索或生产发布；这是CPU机制合同，不是完整Agent优化系统。",
            "compare":"MLE Agents用同轮方差探针对候选研发做目标准入；Fleet侧重特征共享成本与serving可行性。低NE不能覆盖资源超限，低成本也不能绕过NE必须优于基线的准入。两者诊断接口都不能自行证明模型研发或线上收益。",
            "cost":"原文每次真实训练评估需数小时到数天，一次研究约10–25个trial、通常并行4–8个，并依赖私有feature outcomes、fleet预算服务和生产模型。完整活动不适合本轮一张A100/A30或Mac预算。仅CPU显式输入组件，预期三seed不足30秒，零模型/数据下载、零API。",
        },
        "en":{
            "overview":"Meta combines feature creation, FI estimation, cross-task Pareto layers, multi-source blending and constrained search across a model fleet. LLMs propose hypotheses while deterministic tools validate them. Serving caps are model-specific, but upstream pipeline budgets are shared; another model's existing use can make an addition free for that budget.",
            "detail":"Pareto dominance compares FI dimensions without summing task losses. Ordered sources contribute unselected features. The paper uses round(pi_m N) but does not specify rounding or last-front ties, so integer quotas and tie order are caller inputs. Shared set costs require a real oracle, not additive prices. Cross-budget removal order is external. Convert QPS to an upper-bound quantity such as1/QPS first.",
            "results":"Seven production models average0.31% lower NE within their budgets. Trimming six models saves2.3% pipeline cost on average with main loss no worse than about+0.03% measurement noise. A production A/B reports+0.20% on an unnamed primary metric, without traffic fraction, duration or CI; it is not renamed CTR or revenue. Evaluated search tunes feature volumes, not mixture pi.",
            "local":"CPU primitives implement Pareto layers, explicit-quota blending, set-dependent pipeline deltas, remove/refill trimming and admission of completed validation trials. FI, cost oracle, removal order and measured trials are external. No LLM feature proposer, FI estimator, asynchronous research controller or production launch runs. This is not a complete agentic optimizer.",
            "compare":"MLE Agents calibrates candidate admission against a same-round variance probe. Fleet emphasizes shared feature cost and serving feasibility. Better NE cannot override a resource violation, and cheaper candidates still must improve NE. Neither diagnostic interface establishes model-engineering capability or production gains.",
            "cost":"Real trial evaluation takes hours to days; a session contains about10–25 trials with4–8 concurrent jobs, private feature outcomes, fleet budget services and production rankers. The complete campaign exceeds one A100/A30 or Mac budget. Explicit-input CPU primitives should take under30seconds across three seeds, with no model/data downloads or API calls.",
        },
        "qa":[
            ["shared-pipeline-cost","basics","为什么一个特征可以对模型有代价、对某pipeline预算却零增量？","模型仍付embedding/投影等serving代价；但预算内其他模型已消费该特征时，上游生成/存储工作已经发生，不能再算一份同样的pipeline增量。","教学例：A已用f，B新增f时，共享集合并集不变，但B自身推理FLOPs仍可能增加。","How can a feature add serving cost but no pipeline cost?","The model still pays embedding/projection work, but upstream generation/storage may already be paid by another model under that shared budget.","If A already uses f, adding f to B leaves the shared union unchanged while B's inference FLOPs may rise."],
            ["pareto-before-blend","mechanism","为什么先按任务FI作Pareto层，而不是直接求加权和？","不同任务的loss尺度/单位会让求和依赖人为权重；Pareto保留任何任务上有不可被同时支配贡献的特征，再由来源混合控制选择。","教学例：A=(4,1)、B=(1,4)、C=(0,0)，A/B同在首层，C被支配。","Why Pareto layers instead of a weighted task-FI sum?","Task losses differ in scale and units. Pareto layers retain features that cannot be dominated on all tasks before source blending chooses among them.","For A(4,1), B(1,4), C(0,0), A/B share the first front and C is dominated."],
            ["not-ne-alone","comparison","与MLE Agents的方差探针准入相比，本篇多了什么限制？","本篇显式处理每模型资源上界和fleet共享pipeline预算；离线NE更好也不能接受超预算trial。它没有替代MLE Agents的同轮噪声参照。","教学例：NE0.1但inverse-QPS超cap的候选必须让位于NE0.6且可行的候选。","What differs from MLE Agents' variance-probe admission?","Fleet adds model resource caps and shared pipeline budgets. Better validation NE does not admit an infeasible candidate, and these caps do not replace same-round noise calibration.","A candidate with NE0.1 but excessive inverse-QPS is rejected in favor of a feasible NE0.6 candidate."],
            ["explicit-quota-order","implementation","为什么本地不擅自决定round和多预算最贵顺序？","固定原文没有完整定义这些离散约定。调用方必须给整数quota、层内顺序和真实成本排序；缺少可补特征或预算仍违规时显式失败，而非静默填充。","教学例：两个source都把a排首位时，第二source应跳过a；耗尽quota不能悄悄从别的source补满。","Why are rounding and cost order explicit inputs?","The fixed paper leaves those discrete conventions incomplete. Callers supply quotas, within-front order and real cost priorities; exhaustion or infeasibility is reported rather than silently padded.","If two sources rank a first, the second skips a; source exhaustion is not silently refilled from elsewhere."],
        ],
    },
    {
        "aid":"2611.25659", "key":"dna", "title":"DNA: Unlocking Depth Scaling in CTR Models",
        "author":"Caiyuan Li", "org":"Alibaba Group", "published_at":"2026-11-19T07:40:54Z",
        "priority":"P1", "module":"dna_components", "tier":"l1_mechanism", "cuda":True,
        "topic":["排序网络与长序列","请求条件历史更新"],
        "card":"recommendation/history-ranking-backbones", "peer":"recommendation:longer",
        "sections":["3.1–3.6", "4", "5"],
        "figure":[4,[316,78,560,465],"Figure 3: request-shared sequence updates and per-candidate reads"],
        "formula":r"F_{l+1}=A_l^F(F_l,S_l),\quad U_{l+1}=A_l^U(U_l,S_l),\quad S_{l+1}=B_l(S_l,U_{l+1})\ (l<D-1),\qquad \hat y=\sigma(\mathrm{MLP}(\mathrm{Mean}[F_D;U_D])).",
        "diagram":"flowchart LR\n S[Incoming history Sl] --> K[Group specific K V shared per request]\n K --> U[Request read produces Ul plus1]\n K --> F[Candidate read produces Fl plus1]\n U --> B[Composite projection update of every history token]\n S --> B\n B --> N[Next layer history]\n F --> P[Candidate head with final shared request]\n U --> P",
        "cn":{
            "overview":"DNA把请求U与历史S组成候选无关的双流：每层请求和候选F分别读取同一组历史K/V，随后历史token再反向读取刚更新的U。这样下一层看到的是受当前请求塑形的历史，而不是每层重投影同一S0。请求与历史状态可在同一请求的所有候选间共享。",
            "detail":"共有D次请求read、D次候选read，却只有D-1次历史update，最后一层不再更新无人读取的S。read中各行为组使用不同K/V投影，各非序列token使用独立SwiGLU；update对全部请求token的拼接做composite K/V投影，行为组共享各自FFN，padding置零。QKNorm及head缩放保留。",
            "results":"原文在匹配forward FLOPs档位下，DNA相对CrossAttn的AUC绝对差为0.08–0.26个百分点。Taobao搜索DNA-4对线上CrossAttn-2报告CTR相对+0.8%、GMV+0.5%；原文该段没有披露实验时长、流量份额或CI，不补写。5,000候选成本示例中DNA-4约4.70T FLOPs/request，DNA-T-4约78.41T；这些依赖请求内共享，不代表跨请求可直接复用。",
            "local":"实际执行小型可微attention、组特异投影、token特异SwiGLU、composite请求投影及D-1次update；比较同缓存逐候选/批量结果，检查padding不影响分数、请求确实改变S、history/request梯度与backward有限性。score返回logits而不是点击概率，Eq13的sigmoid用BCEWithLogits稳定合并；本地QKNorm为逐head L2归一化乘可学习缩放。维度和层数缩小，输入是显式生成token，不含HHFT tokenizer、私有CTR训练、512维生产模型、线上服务或吞吐测量。fixture BCE只表示数值链路，不表示CTR能力。",
            "compare":"LONGER先用少量query读取长历史，后续主要在压缩token上计算；DNA不靠删掉历史token，而让每个历史token从少量请求token吸收上下文，下一层继续读更新后的完整S。两者都关注候选共享，但共享的对象和更新时机不同；本地诊断不提供二者推荐指标胜负。",
            "cost":"原文DNA-4约1.267B dense参数（不含embedding表），宽512、八heads，约千级历史token，私有Taobao日志训练并做多depth/FLOPs对照。完整规模训练与A/B不复现；仅预期三seed不足30秒的小张量CPU/CUDA机制运行，零模型/数据下载、零API。",
        },
        "en":{
            "overview":"DNA couples request U and history S as candidate-independent streams. Each layer lets request U and candidate F separately read the same history K/V, then history tokens read the newly updated U. The next layer sees request-shaped history instead of another projection of fixed S0. Request/history states are shared across candidates within that request.",
            "detail":"Depth D contains D request reads, D candidate reads and D-1 history updates; the final layer does not update an unused S. Reads use group-specific K/V projections and token-specific SwiGLUs. Updates apply composite K/V projections to concatenated request tokens, group-specific FFNs and padding zeroing. QKNorm and head scaling are retained.",
            "results":"At matched forward-compute tiers, reported AUC gains over CrossAttn are0.08–0.26percentage points. Taobao DNA-4 versus production CrossAttn-2 reports relative CTR+0.8% and GMV+0.5%; duration, traffic share and CI are not supplied in that section. At5,000 candidates, DNA-4 costs4.70T FLOPs/request versus78.41T for DNA-T-4. Sharing is within a request, not unconditional reuse across new requests.",
            "local":"Executes small differentiable attention, group-specific projections, token-specific SwiGLUs, composite request projections and D-1 updates. Controls compare batched/individual candidates, padding invariance, request-dependent history and finite gradients. score returns logits, not click probabilities; BCEWithLogits stably incorporates Eq13's sigmoid. Local QKNorm is per-head L2 normalization times learned scales. Width/depth are reduced. Explicit generated tokens replace HHFT inputs; private CTR training, the512-wide production model and serving benchmarks are absent. Fixture BCE is not CTR capability.",
            "compare":"LONGER compresses long-history interaction into a smaller query/token path. DNA retains history tokens and updates each from a few request tokens before the next read. Both exploit candidate sharing, but share different states at different points. Local mechanism checks do not rank their recommendation quality.",
            "cost":"Paper DNA-4 has roughly1.267B dense parameters excluding embedding tables, width512, eight heads, thousand-token histories, private Taobao training and multiple depth/compute comparisons. Full training/A/B is not reproduced. Tiny CPU/CUDA three-seed mechanisms should take under30seconds without model/data downloads or APIs.",
        },
        "qa":[
            ["evolving-history","basics","为什么多叠几层cross-attention不等于DNA？","固定历史基线每层只重投影S0；DNA让历史接收刚更新请求的信息，下一层读的是新的S。","教学例：同一历史面对两个不同搜索query，可以产生不同S1；固定S0投影没有这种依赖。","Why is deeper cross-attention not already DNA?","A fixed-history stack reprojects S0 at every layer. DNA lets history absorb the newly updated request, so later layers read a changed S.","The same history under two search queries may produce different S1; projecting fixed S0 cannot do this."],
            ["d-minus-one","mechanism","DNA-D为什么只有D-1次历史update？","每层的两次read先读传入S，再更新供下一层用。末层之后没有read，因此多做一次update不会进入预测链路。","教学例：D=3时读S0、S1、S2，只需两次update；不是三次。","Why does DNA-D have only D-1 history updates?","Both reads consume incoming S, and each update prepares the next layer. No read follows the final layer, so another update would not affect prediction.","D3 reads S0, S1 and S2 and requires only two updates."],
            ["longer-distinction","comparison","与LONGER减少后续长序列计算的方式有何不同？","LONGER把信息压到较小query/token路径；DNA保留历史token，让它们从少量请求token更新，并把更新开销在请求内候选间共享。","教学例：两者都可共享K/V，但这不意味着都在每层删除历史token。","How does it differ from LONGER?","LONGER concentrates history interaction into a smaller query/token path. DNA retains history tokens, updates them from a few request tokens and amortizes that work over candidates.","Both can share K/V, but neither shared-K/V fact implies the same token-deletion schedule."],
            ["no-cross-request-cache","implementation","同请求分批候选结果一致，能推出跨请求缓存也安全吗？","不能。新的请求U会改变历史状态，旧S/KV可能失效。本地只检验同一已准备request cache的批量与逐候选等价。","教学例：user历史不变但搜索词变了，必须重建请求条件状态，而不是直接拿上次S2。","Does within-request batching parity justify cross-request reuse?","No. A new U can change history states and invalidate prior S/KV. The local control covers only batch versus individual candidates using the same prepared request cache.","Even with unchanged user history, a new search query requires new request-conditioned states."],
        ],
    },
    {
        "aid":"2611.26096", "key":"lser-serving",
        "title":"From Sessions to Serving: Integrating LLM-Based Embeddings into Retrieval for Production Content Recommendation",
        "author":"Zhixiong Hu", "org":"Autodesk", "published_at":"2026-11-19T13:31:04Z",
        "priority":"P1", "module":"lser_protocol_components", "tier":"l0_interface", "cuda":False,
        "topic":["大模型能力与推荐融合","近线用户表示与召回"],
        "card":"recommendation/retrieval-matching", "peer":"recommendation:youtube-dnn",
        "sections":["2.1–2.2", "3", "4.1–4.2", "5"],
        "figure":[7,[52,80,560,275],"Figure 2: asynchronous nearline vectors and synchronous retrieval path"],
        "formula":r"S_u=\{e:t_{\rm start}\le t_e<t_0,\ \operatorname{session}(e)=s_u\},\quad H_u=\{e:t_{\rm hist}\le t_e<t_{\rm start}\},\quad e_u=f_{\rm user}(e_u^{sess},e_u^{hist},e_u^{LLM},x_u).",
        "diagram":"flowchart LR\n E[Externally eligible logged events] --> P[Strict pre cutoff session and history windows]\n P --> X[Sequence and optional LLM encoders external]\n X --> C[Asynchronously completed vector records]\n C --> A[Available at request time only]\n A --> B[External compatible baseline or LLM fusion]\n B --> R[ANN retrieval external]",
        "cn":{
            "overview":"LSER在双塔召回的用户侧融合会话、较长期历史、请求特征与可选LLM语义向量。较重encoder异步nearline计算，在线请求只读取已完成向量并融合/ANN检索。LLM路径并不替代BERT4Rec式encoder，而提供同一时间窗口的补充语义视角。",
            "detail":"session使用已记录的session ID，历史窗口止于session起点；所有事件严格早于label/request cutoff。通道资格、ID映射、回看长度和session规则是外部合同，未公开的receipt schema不能猜造。原文没有给出通用TTL；本地按(as_of,written_at)防异步乱序回退是接口防护，不冒称论文算法。",
            "results":"§4.2真实50/50随机线上对照是规则引擎vsBERT4Rec式学习召回+nearline，**当时未启用LLM向量**。报告产品/行业carousel CTR+10.3%、customer-story CTR+36.1%等相对lift，不能归因LLM。LLM贡献只由§4.1离线开关隔离：popular-products HR@10绝对+9.6个百分点、MRR+0.021；其他一些surface基本持平。线上时长/CI未提供，文中仅报p<0.05。",
            "local":"只实现显式事件的point-in-time切分与已完成缓存向量选择。调用方必须先将events/records隔离为同一user并完成资格过滤与catalog映射；本接口没有user_id权限隔离，不是完整生产防泄漏系统。缺必需向量时显式要求外部cold-start；LLM缺失或关闭时需外部兼容baseline fusion，不能自动改变治疗模型的输入维度。按最大as_of选择和丢弃不完整LLM pair是本地handoff保护约定，不是论文规定的TTL或具体fallback算法。没有BGE/Qwen encoder、16层decoder、InfoNCE训练、私有label receipt、真实embedding store、ANN或模型冷启动。绝不生成假向量，encoder_calls始终为0；这是L0接口而非召回能力。",
            "compare":"YouTube DNN把聚合观看历史与上下文经非线性用户塔变成召回向量，训练为下一次观看分类；LSER显式区分session/history序列encoder，并可加入LLM辅助语义向量与nearline刷新。两者都能以用户向量查询离线item索引，差异是表征和更新合同，不是把ANN改为LLM逐token生成。原文线上对照是规则引擎，不是YouTube DNN；本地接口不提供两者质量胜负。",
            "cost":"完整方案含冻结0.6B文本embedding模型、基于Qwen3式checkpoint适配的16层四head事件decoder、私有多内容label receipts、双塔训练、SageMaker近线服务与生产A/B。完整链路不在短时单A100/A30或Mac预算内且私有合同缺失；仅CPU协议三seed预期不足30秒，不下载模型/数据或调用API。",
        },
        "en":{
            "overview":"LSER fuses session, longer-term history, request features and optional LLM semantic vectors in a retrieval user tower. Expensive encoders refresh nearline asynchronously; request-time work reads available vectors, fuses them and performs ANN retrieval. LLM vectors complement rather than replace the BERT4Rec-style sequence encoder.",
            "detail":"Session windows use logged session IDs; history ends at session start, and every event is strictly before the label/request cutoff. Eligibility, ID mapping, lookback and sessionization are external contracts, not invented receipt schemas. The paper prescribes no universal TTL. Choosing by(as_of,written_at) against out-of-order completion is a local interface safeguard.",
            "results":"The50/50 production A/B in Section4.2 compares rules with BERT4Rec-style learned retrieval plus nearline serving, with LLM vectors disabled. Relative CTR lifts of10.3% for product/industry carousels and36.1% for customer stories are not LLM effects. LLM evidence is an offline toggle: popular-product HR@10+9.6percentage points and MRR+0.021, with some other surfaces flat. Online duration/CI are not given; p<0.05 is reported.",
            "local":"Only point-in-time slicing and completed-vector selection. Callers must isolate events/records to one user and apply eligibility/catalog mapping first: there is no user_id authorization boundary or complete production leakage defense. Missing required vectors need external cold start; missing/disabled LLM pairs require compatible baseline fusion, not automatic changes to treatment input dimensions. Greatest-as_of selection and dropping incomplete LLM pairs are local handoff safeguards, not prescribed TTL/fallback algorithms. There is no BGE/Qwen encoder,16-layer decoder, InfoNCE training, private receipts, real store, ANN or learned cold start. No vectors are fabricated; encoder_calls is always0. This is L0, not retrieval capability.",
            "compare":"YouTube DNN transforms aggregated watch history/context through a nonlinear user tower and trains next-watch classification. LSER separately encodes session/history and may add LLM semantic auxiliaries with nearline refresh. Both query an offline item index using user vectors; the difference is representation and freshness, not replacing ANN with token-by-token LLM generation. The paper's online control is rules, not YouTube DNN; local interfaces do not rank their quality.",
            "cost":"The full path includes a frozen0.6B text embedding model, an adapted Qwen3-style16-layer/four-head event decoder, private multicontent label receipts, two-tower training, SageMaker serving and production experiments. Private contracts and the campaign exceed this short single-device budget. CPU protocol cases should take under30seconds/three seeds without model/data downloads or APIs.",
        },
        "qa":[
            ["online-llm-disabled","basics","论文线上CTR+10.3%证明LLM向量有效吗？","不证明。线上实验的LLM辅助特征关闭；它验证从规则引擎迁移到学习召回与nearline路径。LLM增量只在离线对照中隔离。","教学例：BERT4Rec+nearline赢规则不能自动推导出再打开LLM会在生产继续增益。","Does the10.3% online CTR lift validate LLM vectors?","No. LLM features were disabled in that experiment. It validates rules-to-learned retrieval and nearline serving; LLM incrementality is isolated offline only.","BERT4Rec plus nearline beating rules does not prove that enabling LLM vectors adds a production lift."],
            ["strict-point-in-time","mechanism","label时间的同一条点击能否进自己的session输入？","不能。事件时间必须严格小于cutoff；session与history在session起点处分开，不使用当前label或未来行为。","教学例：cutoff=10时，timestamp=10的正例和11的事件都排除，不能用小于等于。","May a labeled click enter its own session input?","No. Event time must be strictly below the cutoff. Session and history split at session start and exclude the current label and future behavior.","With cutoff10, events at10 and11 are both excluded; a less-than-or-equal check leaks the label."],
            ["notellm-versus-user","comparison","与YouTube DNN候选生成相比，LSER新增什么而不是LLM直接生成推荐？","YouTube DNN聚合历史/上下文后用用户塔召回；LSER区分短长序列编码，增加可选LLM辅助特征与异步时效合同。两者仍可用用户向量查离线item索引，不是让LLM逐token生成item ID。","教学例：关闭LSER的LLM向量后仍是学习双塔召回，在线A/B也正是这个未启用LLM的版本。","What does LSER add beyond YouTube DNN rather than generating recommendations with an LLM?","YouTube DNN aggregates history/context into a user tower. LSER separates short/long sequence encoders and adds optional LLM features plus asynchronous freshness. Both can query an offline item index; the LLM does not generate item IDs token by token.","With LLM vectors disabled, LSER remains learned two-tower retrieval; this is the version used in its online A/B."],
            ["no-sync-or-fake-vector","implementation","nearline刷新尚未完成时，本地接口会同步调用LLM或补零向量吗？","都不会。只选择请求时已写入且输入cutoff不超时的记录；必需session/history缺失会显式要求外部cold-start，LLM不完整则交兼容baseline fusion。","教学例：request=10而written_at=12的向量不可读，即使as_of=9；这不表示论文规定了某固定TTL。","Does a pending refresh call an LLM or invent zero vectors?","Neither. Select only records written by request time with admissible input cutoffs. Missing session/history explicitly requires external cold start; incomplete LLM pairs require compatible baseline fusion.","At request10 a vector written_at12 is unavailable even with as_of9; this does not impose a paper-prescribed TTL."],
        ],
    },
]


def write(path,payload):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n")


def detail(p):
    return f"recommendation-components/{p['aid']}-{p['key']}/README.md"


def document(p,english=False):
    b=p["en" if english else "cn"]
    src=f"https://arxiv.org/pdf/{p['aid']}v1"
    tier=p["tier"]
    labels=["Paper information","Original paper summary","Background and principal changes","Original paper figure","Core equations","Paper offline and online results","Local reproduction","Data protocol and code mapping","Same-topic comparison and boundaries","High-cost full experiment"] if english else ["论文信息","原始论文总结","背景与主要改动","原论文关键图","核心公式","论文离线与线上效果","本地复现","数据协议与代码映射","同主题比较与边界","高成本完整实验"]
    fields=["Paper link","Company / institution / school","Original publication date","Original source code","Local adapter / key","Local reproduction code directory"] if english else ["论文链接","公司 / 机构 / 学校","首次公开日期","原作者开源代码","本地 adapter / key","本地复现代码目录"]
    values=[f"[arXiv:{p['aid']}v1](https://arxiv.org/abs/{p['aid']}v1); [fixed PDF]({src})",f"{p['author']}: {p['org']} (fixed-v1 PDF byline)",f"{p['published_at']} (arXiv v1); announced2026-11-20","No verified author method code found in fixedv1/associated sources; arXiv feedback GitHub is not author code." if english else "固定v1及关联来源未找到可核验的原作者本方法代码；arXiv报告问题的GitHub链接不算开源。",f"`{p['key']}`; `adapter: null`; not Evolve-integrated",f"`src/auto_research/reproductions/{p['module']}.py`"]
    text=f"# {p['title']}\n\n"+("[简体中文](README.md)" if english else "[English](README-en.md)")+f"\n\n> **{tier}**: "+("diagnostic component/interface only, not a complete capability reproduction. Full experiment: **high cost, not reproduced (review DONE)**." if english else "仅低成本机制/接口诊断，不是完整能力复现。完整实验：**成本过高，不复现（审查 DONE）**。")+f"\n\n## {labels[0]}\n\n| Field | Value |\n| --- | --- |\n"
    text+="".join(f"| {x} | {y} |\n" for x,y in zip(fields,values,strict=True))
    text+=f"\n## {labels[1]}\n\n### {labels[2]}\n\n{b['overview']}\n\n[Fixed-v1 primary source]({src})\n\n~~~mermaid\n{p['diagram']}\n~~~\n\n<!-- paper-figure:start -->\n### {labels[3]}\n\n[![{p['figure'][2]}](assets/paper-figure-01.png)]({src}#page={p['figure'][0]})\n\n"+("Original PDF crop, no semantic editing; author evidence, not a local result. [Provenance](assets/provenance.json); copyright remains with the authors.\n" if english else "原始PDF裁切，没有语义编辑；是原作者证据，不是本地结果。[页码、裁切与SHA256](assets/provenance.json)，版权归原作者。\n")+f"<!-- paper-figure:end -->\n\n### {labels[4]}\n\n$$\n{p['formula']}\n$$\n\n{b['detail']}\n\n### {labels[5]}\n\n{b['results']}\n\n## {labels[6]}\n\n### {labels[7]}\n\n{b['local']}\n\n"
    text+=f"```bash\nPYTHONPATH=src python -c 'from auto_research.reproductions.{p['module']} import diagnostic; print(diagnostic(42, device=\"cpu\"))'\nPYTHONPATH=src python -m pytest tests/test_nov20_root_components.py -q\n```\n\n"+("Seeds42/43/44 check deterministic contracts/generated tensors, not independent capability comparisons. CUDA paths require separate real-GPU receipts; CPU results do not substitute.\n\n" if english else "seeds42/43/44只检查合同/生成张量，不是独立能力比较。CUDA路径需要单独真实GPU回执，CPU结果不能替代。\n\n")
    text+=f"### {labels[8]}\n\n{b['compare']}\n\n### {labels[9]}\n\n{b['cost']}\n\n"+("Configuration-based cost judgment, not measured full-run duration. **High cost, not reproduced (review DONE)**; no automatic retry/implementation queue or capability/Evolve promotion.\n" if english else "这是配置依据的成本判断，不是完整实验实测耗时。**成本过高，不复现（审查 DONE）**；不自动重试/入实现队列，不声明能力提升或Evolve晋级。\n")
    return text


def main():
    if (AUDIT/"root-review.json").exists():
        raise RuntimeError("one-shot root bundle already authored; do not overwrite curated results")
    paths={x["domain"]+":"+x["key"]:x["detail_path"] for x in json.loads((ROOT/"docs/research-manifest.json").read_text())["papers"]}
    paths.update({"recommendation:"+p["key"]:detail(p) for p in PAPERS})
    bank,overlays,proposals,accepted={},{},[],[]
    for p in PAPERS:
        identity="recommendation:"+p["key"]
        pdf=CACHE/(p["aid"]+"v1.pdf")
        digest=sha256(pdf.read_bytes()).hexdigest()
        target=ROOT/"docs"/detail(p)
        assets=target.parent/"assets";assets.mkdir(parents=True,exist_ok=True)
        page,box,caption=p["figure"]
        d=fitz.open(pdf)
        asset=assets/"paper-figure-01.png"
        d[page-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(box),alpha=False).save(asset)
        write(assets/"provenance.json",{"source_url":f"https://arxiv.org/pdf/{p['aid']}v1","paper_url":f"https://arxiv.org/abs/{p['aid']}v1","reviewed_version":"v1","retrieved_on":DATE,"page":page,"crop_box_pdf_points":box,"caption":caption,"extraction":"Original PDF crop, no semantic editing","source_pdf_sha256":digest,"asset_sha256":sha256(asset.read_bytes()).hexdigest(),"copyright":"Copyright retained by the original authors; research commentary, not a local result."})
        cn=document(p);target.write_text(cn)
        (target.parent/"README-en.md").write_text("<!-- source-sha256: "+sha256(cn.encode()).hexdigest()+" -->\n"+document(p,True))
        cost={"source":f"https://arxiv.org/pdf/{p['aid']}v1; "+", ".join(p["sections"]),"available_resource":"one A100 or A30, or local Mac","paper_configuration":p["cn"]["cost"],"model_scale":p["en"]["cost"],"estimated_cost_basis":"Fixed source and measured paper configuration; no local complete-campaign timing or costly probe.","decision":"成本过高，不复现（审查 DONE）；仅低成本组件/接口"}
        spec={"domain":"recommendation","key":p["key"],"title":p["title"],"paper_url":f"https://arxiv.org/abs/{p['aid']}v1","reviewed_version_url":f"https://arxiv.org/pdf/{p['aid']}v1","reviewed_version":"v1","published":p["published_at"][:10],"published_at":p["published_at"],"announced_on":DATE,"detail_path":detail(p),"topic":p["topic"],"first_author":p["author"],"first_author_affiliation":p["org"],"affiliation_evidence":"Fixedv1 PDF byline and primary HTML checked.","verified_priority_organizations":["Meta"] if p["key"]=="fleet-feature-optimization" else [],"code":None,"code_status":"固定v1和关联来源未找到本篇原作者方法代码；arXiv反馈/依赖链接不计为开源。","code_license":"未找到可核验的原作者方法代码许可证","upstream_revision":None,"method_source_sha256":digest,"adapter":None,"priority":p["priority"],"intake_class":"new_first_release","implementation_status":"component_only","evaluation_tier":p["tier"],"diagnostic_only":True,"promotion_eligible":False,"evolve_integrated":False,"local_operator":f"auto_research.reproductions.{p['module']}.diagnostic","local_command":f"PYTHONPATH=src python -c 'from auto_research.reproductions.{p['module']} import diagnostic; print(diagnostic(42))'","requires_gpu_validation":p["cuda"],"gpu_validation_passed":False,"gpu_validation_artifact":"docs/gpu-validations/dna-a100-20261120-latest.json" if p["cuda"] else None,"full_experiment_status":"not_reproduced_high_cost","full_experiment_review_done":True,"review_done":True,"review_resolution":"not_reproduced_high_cost","automatic_retry":False,"automatic_implementation_queue":False,"cost_assessment":cost,"summary":p["cn"]["overview"]+" "+p["cn"]["local"]}
        if p["key"]=="fleet-feature-optimization":
            spec["online_ab_review"]={"source":spec["reviewed_version_url"],"section":"5 Results/Online","production":True,"primary_metric_relative_lift":0.002,"metric_name":"not disclosed","traffic_fraction":None,"duration":None,"confidence_interval":None,"limits":"Volume-only search evaluated; mixture tuning not evaluated; no attribution beyond reported fleet campaign."}
        elif p["key"]=="dna":
            spec["online_ab_review"]={"source":spec["reviewed_version_url"],"section":"5 Online Deployment","production":True,"control":"CrossAttn-2","treatment":"DNA-4","ctr_relative_lift":0.008,"gmv_relative_lift":0.005,"traffic_fraction":None,"duration":None,"confidence_interval":None,"limits":"No local CTR training or production experiment; within-request sharing does not imply cross-request state reuse."}
        else:
            spec["online_ab_review"]={"source":spec["reviewed_version_url"],"section":"4.2","production":True,"traffic_split":[0.5,0.5],"control":"prior rule-based content engine","treatment":"BERT4Rec-style learned retrieval and nearline serving; LLM vectors disabled","llm_features_enabled":False,"validates_llm_incrementality":False,"product_industry_ctr_relative_lift":0.103,"customer_story_ctr_relative_lift":0.361,"reported_significance":"p<0.05","duration":None,"confidence_interval":None,"offline_llm_hr10_absolute_pp":9.6,"limits":"Online result cannot be attributed to optional LLM features; dedicated production LLM toggle is future work."}
        write(ROOT/f"src/auto_research/paper_specs/catalog/recommendation/{p['key']}.json",spec)
        accepted.append({"arxiv_id":p["aid"],"key":p["key"],"domain":"recommendation","identity":identity,"title":p["title"],"first_author":p["author"],"first_author_affiliation":p["org"],"first_published_at":p["published_at"],"announced_on":DATE,"priority":p["priority"],"intake_class":"new_first_release","reviewed_version":"v1","reviewed_source_url":spec["reviewed_version_url"],"source_sha256":digest,"sections_read":p["sections"],"implementation_status":"component_only","evaluation_tier":p["tier"],"scope":p["en"]["local"],"cost_basis":p["en"]["cost"],"component_budget":"Expected less than30seconds/three seeds; no model/data downloads or API calls.","requires_gpu_validation":p["cuda"],"gpu_validation_passed":False,"local_detail_path":detail(p),"code_url":None,"upstream_revision":None,"full_experiment_status":"not_reproduced_high_cost","full_experiment_review_done":True,"review_done":True,"review_resolution":"not_reproduced_high_cost","automatic_retry":False,"automatic_implementation_queue":False})
        questions=[];english={}
        for qid,level,q,a,e,eq,ea,ee in p["qa"]:
            questions.append({"id":qid,"level":level,"question":q,"answer":a,"example":e,"source_sections":["背景与主要改动","核心公式","数据协议与代码映射","同主题比较与边界","高成本完整实验"],"added":DATE})
            english[qid]={"question":eq,"answer":ea,"example":ee}
        bank[identity]={"questions":questions}
        units=question_units({identity:questions})
        for q in questions:
            uid=f"qa/{identity}/{q['id']}"
            overlays[uid]={"source_sha256":units[uid].source_sha256,"reviewed":True,"fields":english[q["id"]]}
        pair=[identity,p["peer"]]
        revisions={pid:sha256((ROOT/"docs"/paths[pid]).read_bytes()).hexdigest() for pid in pair}
        compare=questions[2]
        proposals.append({"paper":identity,"target_card":p["card"],"source_revisions":revisions,"comparison":{"position":p["cn"]["overview"],"tradeoff":p["cn"]["compare"],"sections":["背景与主要改动","核心公式","同主题比较与边界"]},"analysis":{"title":p["title"],"body":p["cn"]["compare"]+" "+p["cn"]["detail"],"papers":pair},"question":{"id":"nov20-"+p["key"],"question":compare["question"],"answer":compare["answer"],"example":compare["example"],"papers":pair},"update":{"date":DATE,"papers":pair,"summary":p["cn"]["compare"]+" 原文线上证据与本地合同分开记录。"},"english":{"comparison":{"position":p["en"]["overview"],"tradeoff":p["en"]["compare"]},"analysis":{"title":p["title"],"body":p["en"]["compare"]+" "+p["en"]["detail"]},"question":english[compare["id"]],"update":p["en"]["compare"]+" Paper production evidence and local contracts remain separate."}})
    write(AUDIT/"root-authored-bundle.json",{"schema_version":1,"date":DATE,"papers":bank,"english_question_units":overlays})
    write(AUDIT/"deep-dive-proposals-root.json",{"schema_version":1,"reviewed_on":DATE,"integration_owner":"root","proposals":proposals})
    write(AUDIT/"root-review.json",{"schema_version":1,"reviewed_on":DATE,"requested_window":["2026-11-19",DATE],"scope":"Finite selected industrial first-source review, not all-source exhaustion.","preflight_before_implementation":True,"available_resource":"one A100 or A30, or local Mac","large_downloads_authorized_or_needed":False,"watermark_change_claimed":False,"accepted":accepted,"selection_notes":["Fleet current Meta byline and production A/B verified; unnamed primary metric is not relabeled CTR/revenue.","DNA original online control is CrossAttn-2; no invented duration/traffic fraction/CI.","LSER production A/B has LLM features disabled; only offline ablation isolates LLM incrementality.","Original method repositories not found; arXiv HTML feedback links are not author source releases."]})
    print("Authored3industrial papers,12reviewed bilingual questions and3deep-dive proposals; algorithms/shared banks untouched.")


if __name__=="__main__":
    main()
