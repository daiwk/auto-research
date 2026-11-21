"""Reviewed, explicitly authored Nov21 Agent overlap additions; never a translator.

Only owned paper/spec/bundle files are written. Shared catalogs and learning
banks remain the batch owner's responsibility. Fetch mode downloads only the
two small public source papers, not models, data or user conversation records.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov21-latest/agent-primary"
AUDIT = ROOT / "docs/research-audits/nov21-latest"
DATE = "2026-11-21"
HEADINGS = ["背景与主要改动", "核心公式", "数据协议与代码映射", "同主题比较与边界", "高成本完整实验"]

PAPERS = [
    dict(
        key="sage-evolve", module="sage_evolve", id="2611.26132",
        title="Sage-Evolve-Preview: Adaptive Observation for Post-Training Self-Improvement",
        cn_title="Sage-Evolve / AdaObs：保持目标不变，平台期先改变观察方式",
        author="Yinhao Tang", org="University of Science and Technology of China / Shanghai AI Laboratory",
        published="2026-11-19T13:52:46Z", topic="执行框架与自改进",
        code=None, code_cn="固定v1及本轮核对来源未发现论文专用方法代码；引用的benchmark仓库不是本方法开源。",
        code_en="No paper-specific method source was found in fixed v1 or reviewed sources; cited benchmark repositories are not a method release.",
        card="agent-research/harness-and-self-improvement", peer="agent-research:harness2",
        peer_path="agent-research/2610.14224-harness2/README.md", page=4, crop=[65,65,530,350],
        locations=["§3.1 Eq.1-2", "§3.2 Eq.3", "Appendix B.1 Eq.4 and defaults", "Appendix B.2 Algorithm1", "Appendix B.5 Table5 and compute"],
        method="AdaObs区分固定anchor目标和引导当前研究的active observation。每轮仍在固定anchor上验收；训练进展停滞时，先细分已有输出的错误诊断，再增加同任务的困难层，最后累计加入同能力方向的相关任务。它改变的是发现训练缺口的观察，不是为了提高分数而改评分器、换掉原目标或把测试答案放进训练。",
        method_en="AdaObs separates the fixed anchor objective from the active observation guiding research. Every checkpoint is still checked on the anchor. At a plateau, it first refines diagnostics on existing outputs, then adds a harder tier of the same task, and finally adds a related task in the same capability direction. It changes how training gaps are observed, not the scoring rules, the original objective or test-answer access.",
        mechanism="同一观测阶段内，边际收益按每新增1万条保留样本的分数变化计算，用α=0.3做EMA；最近3次平滑值全部严格小于0.1才判平台。更换观测必须清空该历史。候选增量须让active或anchor至少一个严格改善，且anchor下降不超过0.5分。L2用独立参考模型，在通过率[0.2,0.6]内选最难层，保留旧层；L3保留旧任务。负例记忆排除的是当前gap下的具体配置，不是失败过一次就封禁整个L1。原文的训练每次从M0加base与累计增量重训，本地没有把它改成继续微调前一轮checkpoint。",
        mechanism_en="Within one observation phase, marginal return is score change per10,000 retained examples. An EMA with alpha0.3 triggers a plateau only when all three trailing smoothed values are strictly below0.1; changing observations resets that history. A candidate must strictly improve active or anchor score while losing at most0.5 anchor points. L2 selects the hardest tier with held-out reference pass rate in[0.2,0.6], retaining older tiers; L3 retains older tasks. Failure memory excludes a concrete configuration for the current gap, not an entire lever. The paper retrains from M0 on base data plus retained increments; no warm-start replacement is claimed locally.",
        formula=r"\mathrm{MR}_t=\frac{S_t^{act}-S_{t-1}^{act}}{\Delta d_t/10000},\qquad \widehat{\mathrm{MR}}_t=\alpha\mathrm{MR}_t+(1-\alpha)\widehat{\mathrm{MR}}_{t-1}.\qquad \operatorname{Plateau}(t)\iff\max_{t-w<i\le t}\widehat{\mathrm{MR}}_i<\epsilon.",
        result="Table1的8个anchor分别独立优化，AdaObs平均73.66、FixedObs66.44，不是一个统一模型在8项上的同时提升。原文的误差条主要是多次解码评测噪声，不是独立训练种子的方差。PostTrainBench另报告两种Agent backend上的迁移。都是作者离线结果，未报告生产线上A/B；本地组件不复算这些分数。",
        result_en="Table1 optimizes eight anchors independently: AdaObs averages73.66 versus66.44 for FixedObs, not one shared model improved simultaneously on all eight. Reported error bars mainly reflect repeated decoding evaluations, not variance across independent training seeds. A separate PostTrainBench study tests transfer across two agent backends. These are author offline results; no production A/B is reported, and local components do not reproduce these scores.",
        local="本地只执行显式分数的增量验收、边际收益算术、EMA/平台判定、不可变观测结构、按L1→L2→L3选首个可行的显式提案、累计层/任务检查、具体gap配置负例过滤和参考通过率选层。首个MR初始化EMA，等分提案按输入顺序，是明确的本地确定性约定。MR函数要求正的显式保留样本数，拒绝0分母；原文未完全展开拒绝增量的Δd口径，因此不擅自把尝试样本当保留样本，调用方也可直接向monitor提供已定义的MR。没有LLM Analyze/Plan/Produce、数据生成、污染检查器、SFT、集群调度或Harness编辑器；可行性和语义诊断由调用方负责。",
        local_en="The local slice executes acceptance gates on explicit scores, marginal-return arithmetic, EMA/plateau detection, immutable observation records, first-feasible supplied proposals in L1/L2/L3 order, cumulative tier/task validation, gap-specific failed-configuration filtering and reference-rate tier selection. The first MR initializes the EMA and input order resolves tied proposals: explicit deterministic local conventions. MR requires a positive supplied retained-example count and rejects a zero denominator. Because the paper does not fully define rejected-increment data accounting, attempted examples are not silently called retained; callers may supply a defined MR directly. No LLM analysis/planning/production, data generation, contamination checker, SFT, scheduler or harness editor executes. Proposal feasibility and semantic diagnosis remain external.",
        controls="负控包括恰好等于epsilon不能触发平台、跨phase误用分数被拒绝、切换phase清零、一次具体L1失败后同层其他方案仍可选、不同gap不共用封禁、L2/L3不得丢弃旧成员或一次改多个轴、anchor回退0.5分包含边界而0.501分拒绝。CPU控制只证明规则，不证明自动科研会找到更好的训练数据；不接入Evolve晋级。",
        controls_en="Controls keep equality with epsilon outside the plateau, reject cross-phase score use, reset history on a phase change, preserve other L1 options after one concrete failure and isolate failures by gap. L2/L3 may not discard prior members or change several axes. Exactly0.5 anchor regression is allowed, while0.501 is rejected. CPU controls establish rules, not successful autonomous data discovery or Evolve promotion.",
        cost="原文Qwen3.5-35B-A3B full-parameter SFT，256K样本/pack，64张H200，约12小时/iteration、最多8个并行run；另含64K生成和最高1M会话评测。相对单A100/A30或Mac明显高成本，完整训练与评测直接不复现，不下载权重、不探跑。只允许秒级CPU控制核。",
        cost_en="The paper uses full-parameter SFT of Qwen3.5-35B-A3B,256K-token samples/packs,64H200s and roughly12hours per iteration, with up to eight concurrent runs. Evaluations allow64K generation and up to1M-token sessions. This clearly exceeds oneA100/A30 or a Mac, so full training/evaluation is not reproduced, without weight downloads or trial runs. Only the small CPU control kernel executes.",
        compare="Harness²固定模型权重，用参考执行、候选执行对照和组合改任务Harness，并保存跨任务经验；AdaObs的完整研究会更新模型权重，固定anchor而改变active observation，平台检测针对数据边际收益。两者都用记忆避免重复，但“哪种执行框架更好”和“当前观察能否揭示新训练缺口”不是同一个选择问题；本地Harness²也是机制替身诊断，不能拿两者本地控制通过率比较Agent能力。",
        compare_en="Harness² holds model weights fixed and improves task harnesses through reference/candidate execution contrasts and composition, preserving cross-task lessons. Full AdaObs updates model weights while holding the anchor fixed and adapting observations; plateaus concern marginal data returns. Both use memory to avoid repetition, but choosing a harness differs from exposing a new training gap. The local Harness² slice is also a mechanism diagnostic, so their control pass rates cannot compare agent capability.",
        flow_cn="A[固定anchor与当前active] --> B[显式评分和保留门控]\n  B --> C[同phase边际收益EMA]\n  C --> D{平台}\n  D -->|是| E[L1诊断 L2难度 L3相关任务]\n  E --> F[具体失败配置过滤与累计观测]\n  F --> C",
        flow_en="A[Fixed anchor and active view] --> B[Explicit scores and retention gate]\n  B --> C[Within-phase marginal-return EMA]\n  C --> D{Plateau}\n  D -->|Yes| E[L1 diagnostics L2 difficulty L3 related task]\n  E --> F[Concrete failure filtering and cumulative view]\n  F --> C",
        questions=[
            ("anchor-vs-active","basics","active observation变了，目标是不是也变了？","不是。anchor是始终保留的验收目标；active只改变当前看哪些细分错误、难度或相关任务，帮助发现下一批训练增量。","教学例：原目标是长文问答，可新增8-needle诊断，但不能删除原题只报更容易题的分数。","Does changing the active observation change the objective?","No. The anchor remains the acceptance objective; the active view exposes diagnostic groups, tiers or related tasks to guide the next training increment.","Teaching example: add an eight-needle diagnostic to long-document QA without replacing the original evaluation with easier questions."),
            ("phase-reset","mechanism","为什么切换观测后必须重置边际收益历史？","不同观测的分数不是同一标尺。把较难任务较低的分数直接减掉旧任务分数，会把换测量工具当模型退化。","教学例：旧active为80、新active为40，不表示训练损失了40分；应重新建立同phase比较。","Why reset marginal-return history after changing observations?","Scores under different observations are not comparable. Subtracting an old easier-task score from a harder-task score confuses measurement change with model regression.","Teaching example: moving from an80-point old view to a40-point new view is not a measured40-point training loss; start within-phase comparisons again."),
            ("observation-vs-harness","comparison","AdaObs和Harness²都自进化，改的是同一层吗？","不是。Harness²改固定模型外的执行方式；AdaObs固定anchor、改变发现训练缺口的观测，并在完整研究中重训模型。两种本地诊断都不能冒充Agent能力收益。","教学例：把失败按上下文长度分桶是改观测，增加工具重试规则是改Harness。","Do AdaObs and Harness² evolve the same layer?","No. Harness² edits execution around a fixed model. AdaObs keeps the anchor fixed, changes how training gaps are observed and retrains models in the full study. Neither local diagnostic demonstrates capability gains.","Teaching example: grouping failures by context length changes observation; adding a tool retry rule changes the harness."),
            ("concrete-failure","implementation","一个L1诊断方案失败，能直接跳到L2吗？","不能据此封禁所有L1。负例记忆记录当前gap下的具体refinement配置，仍应先检查其他可行L1；没有可行L1才升级。","教学例：按格式分桶没找到新缺口，不代表按长度分桶也无效；换gap后也不能沿用旧封禁。","Does one failed L1 diagnostic rule out L1 entirely?","No. Negative memory records a concrete refinement for a current gap. Other feasible L1 options remain eligible; escalation follows only when no L1 option remains.","Teaching example: uninformative format groups do not invalidate length groups, and a failure for one gap should not blacklist another gap."),
        ],
    ),
    dict(
        key="memfolder", module="memfolder", id="2611.26427",
        title="MemFolder: Structure-Guided Memory Folding for Efficient Agent Memory Management",
        cn_title="MemFolder：用互补锚点和非分支时间链减少检索单元",
        author="Xuyang Liu", org="Sichuan University", published="2026-11-19T17:05:55Z", topic="记忆与技能",
        code="https://github.com/xuyang-liu16/MemFolder/tree/4226577050b468f60ec273f2199b61e20a19efbd",
        code_cn="是：[原作者固定仓库提交](https://github.com/xuyang-liu16/MemFolder/tree/4226577050b468f60ec273f2199b61e20a19efbd)；仓库API未识别明确许可证，不擅自标注MIT。",
        code_en="Yes: [fixed author repository commit](https://github.com/xuyang-liu16/MemFolder/tree/4226577050b468f60ec273f2199b61e20a19efbd). The repository API reports no recognized license; MIT is not invented.",
        card="agent-research/memory-and-skills", peer="agent-research:memforest", peer_path="agent-research/2609.08273-memforest/README.md",
        page=5, crop=[104,80,509,376], locations=["§3.3 Eq.1 and affinity", "§3.4 blind verification and fallback", "Table1 retention denominator", "Appendix A.1 defaults", "Figure2"],
        method="MemFolder把记录数和取回上下文长度分开处理。RecordFolder先用LLM统一实体，再以密度峰选首锚点、以相对已有锚点的novelty渐进选互补锚点；语义/实体亲和与时间链修正分组，最后由LLM按时间合并。ContextFolder沿用这些分组，按事实重要性和token比例编码，通过看不到源记录和预期答案的blind reader检查可恢复性。分组不是摘要生成，校验也不是无损保证。",
        method_en="MemFolder treats record count and retrieved-context length separately. RecordFolder grounds entities with an LLM, selects a density-peak first anchor and progressively chooses complementary anchors through novelty relative to those already selected. Semantic/entity affinity and temporal chains refine groups before chronological LLM consolidation. ContextFolder reuses groups, encodes facts under importance and token-ratio constraints, and tests recoverability with a blind reader that cannot see source records or expected answers. Grouping is not summary generation, and verification is not a losslessness guarantee.",
        mechanism="实体权重为log(N/df)，共有的实体权重可为0；weighted Jaccard与cosine按共享实体质量和两种信号方差自适应混合。方差先在整个W窗口的前后记录对上计算，再筛正gain和每后继最多d条候选边；gain相对的是后继与初始锚点的cosine。Hungarian最大化总gain，各节点最多一入一出，锚点不可有入边，所以没有分叉或时间环。有锚点的链留在该组，无锚点链按整链cosine总和选组，未匹配项保留原分组。",
        mechanism_en="Entity weights are log(N/df), so an entity common to every record can have zero weight. Shared entity mass and both signal variances adaptively mix weighted Jaccard with cosine. Variances are computed over every earlier/later pair in the W-window before positive-gain filtering and the d-edge-per-successor cap. Gain is measured against the successor's initial-anchor cosine. Hungarian matching maximizes total gain with at most one incoming and outgoing edge, and no incoming anchor edge. Thus links form forward nonbranching chains: anchored chains stay together, anchor-free chains choose the maximum summed cosine group, and unmatched records retain their initial group.",
        formula=r"w(e)=\log\frac{N}{\operatorname{df}(e)},\quad e_{ij}=\frac{\mu(E_i\cap E_j)}{\mu(E_i\cup E_j)},\quad \alpha_{ij}=\frac{\mu_{ij}\sigma_c^2}{\mu_{ij}\sigma_c^2+\sigma_e^2},\quad g(p,s)=\alpha_{ps}e_{ps}+(1-\alpha_{ps})c_{ps}-c_{s,a_0(s)}.",
        result="Table1在Mem0上减少50%记录后，三个文本benchmark平均60.5，相对未压缩61.1保留99.0%；99.0%是质量保留比，不是答题准确率99%。MemForest同口径保留97.1%，相差1.9个百分点的保留率。原文还有MemOS和M3-Bench web/robot；这些离线作者结果不是本地测试分数，未报告生产线上A/B。",
        result_en="In Table1,50% fewer records on Mem0 yield a three-text-benchmark average of60.5 versus61.1 uncompressed, or99.0% quality retention. That99.0% is not answer accuracy. MemForest retains97.1% under the same ratio, a1.9-percentage-point retention difference. Further author evaluations cover MemOS and M3-Bench web/robot. These are offline paper results, not local measurements; no production A/B is reported.",
        local="本地实现显式embedding和已ground实体集合上的RecordFolder分组核，包括归一化、DPC/novelty锚点、全窗口方差、IDF亲和、正gain候选、SciPy真正Hungarian和链级重新归组；仅接收按时间排序的输入，最多512条。用总体方差ddof=0、Python round、相同分数按输入顺序、重复embedding的锚点固定保留本组，是论文未完全指定时公开的确定性约定。没有LLM实体提取、实体别名合并、文本合并、ContextFolder、embedding模型或下游问答；调用方负责提供已ground标签和时间顺序，不用词项Jaccard冒充语义embedding。不接收文件路径，不读取Codex会话，也不自动删除或压缩用户文件。",
        local_en="The local RecordFolder grouping kernel consumes explicit embeddings and grounded entity sets: normalization, DPC/novelty anchors, full-window variances, IDF affinity, positive-gain candidates, actual SciPy Hungarian matching and chain reassignment. Inputs must be chronological and contain at most512 records. Population variance with ddof0,Python rounding,input-order ties and anchors pinned to their own groups under duplicate embeddings are explicit deterministic conventions where the paper leaves details open. There is no LLM entity extraction, alias merging,text consolidation,ContextFolder,embedding model or downstream QA. Callers supply grounded labels and chronological order; lexical Jaccard is not substituted for semantic embeddings. No paths or Codex conversations are read, and no user files are automatically removed or compressed.",
        controls="负控包括全记录恰好分配一次、重复embedding仍保留K个非空组、N=1、所有实体共有时退化为cosine、在筛边前计算窗口方差、时间边向前且锚点无入边、每节点最多一入一出，以及一个greedy得0.9而Hungarian得1.6的显式矩阵单测。后者仅是组合优化单测，不是记忆准确率。上下文验证可能误判源事实，且原文回退可选择缺失required facts的较短候选，不能把ContextFolder宣传为无损存储。",
        controls_en="Controls assign every record once,preserve K nonempty groups under duplicate embeddings,handle N1,reduce to cosine for universally common entities,and estimate window variance before filtering. Links must point forward,avoid incoming anchor edges and be nonbranching. A supplied-matrix unit test distinguishes greedy gain0.9 from Hungarian gain1.6; it is not memory accuracy. Verification can misjudge source facts, and the paper's fallback may choose a shorter candidate missing required facts, so ContextFolder must not be described as lossless storage.",
        cost="完整研究在两张A100-80GB上运行，涉及GPT-4o-mini实体抽取/合并/评审、GPT-4o多模态评测、OpenAI embedding、多个记忆框架和5个文本/多模态评测设置、每项3轮。真实重建与API矩阵明显超出本轮单A100/A30或Mac的小型组件预算，直接不复现、不下载数据或权重、不发起收费调用；只运行小矩阵CPU分组。",
        cost_en="The full study runs on twoA100-80GBs with GPT-4o-mini extraction/merging/judging,GPT-4o multimodal evaluation,OpenAI embeddings,multiple memory frameworks and five text/multimodal evaluation settings repeated three times. Rebuilding the stores and API matrix exceeds this batch's single-A100/A30 or Mac component budget. Full experiments are not reproduced: no data/weight downloads or paid calls are launched. Only small CPU grouping matrices execute.",
        compare="MemForest按事件构建最大生成树并渐进合并，检索时从anchor传播到时间邻域；MemFolder先以全局互补锚点确定目标组数，再用实体/语义gain和Hungarian非分支时间链修正组，并另加独立的ContextFolder编码层。二者都保留结构，但树形层次与一入一出的链不等价。现有本地MemForest用词项重叠近似语义，本地MemFolder只收显式embedding，因此不能凭两者单测数值宣称谁的模型记忆更好。",
        compare_en="MemForest builds event-level maximum-spanning trees and progressively merges nodes, retrieving temporal neighbors through anchor-guided propagation. MemFolder first fixes target groups using global complementary anchors,then refines them through entity/semantic gains and Hungarian nonbranching chains,and adds a separate ContextFolder encoding layer. Both preserve structure,but a hierarchy is not a one-in/one-out chain. Local MemForest approximates semantics through lexical overlap while local MemFolder takes supplied embeddings; their unit-test numbers cannot establish a memory-quality winner.",
        flow_cn="A[显式embedding和ground实体] --> B[DPC与novelty选K锚点]\n  B --> C[初始最近锚点组]\n  C --> D[实体IDF和全窗口方差亲和]\n  D --> E[正gain候选与Hungarian]\n  E --> F[非分支时间链归组]\n  F -.未实现.-> G[LLM合并与ContextFolder]",
        flow_en="A[Supplied embeddings and grounded entities] --> B[DPC and novelty choose K anchors]\n  B --> C[Initial nearest-anchor groups]\n  C --> D[IDF and full-window-variance affinity]\n  D --> E[Positive-gain candidates and Hungarian]\n  E --> F[Nonbranching temporal-chain groups]\n  F -.Not implemented.-> G[LLM merge and ContextFolder]",
        questions=[
            ("two-compression-axes","basics","记录减少一半，上下文token就一定减少一半吗？","不一定。合并后每条可能变长；RecordFolder减少检索单元数，ContextFolder才另外压缩每组文本，二者成本轴不同。","教学例：两条各20token合成一条40token，记录少50%，文本并未缩短。","Does halving records necessarily halve context tokens?","No. A merged record can be longer. RecordFolder reduces retrieval units; ContextFolder separately compresses each group's text.","Teaching example: merging two20-token records into one40-token record halves count but saves no text tokens."),
            ("rare-entity-affinity","mechanism","为什么所有记录都有的实体反而不应提高亲和？","IDF权重log(N/df)在df=N时为0，它不区分事件；没有共享实体质量时alpha=0，亲和退回cosine。","教学例：每条都出现“用户”不能把所有经历连成一个事件，稀有项目名才可能区分相关记录。","Why should an entity in every record add no affinity?","Its IDF log(N/df) is zero when df=N because it does not distinguish events. With no shared entity mass,alpha is zero and affinity returns to cosine.","Teaching example: the word user in every record should not link all experiences; a rare project name may identify related ones."),
            ("chain-versus-tree","comparison","MemFolder的时间链和MemForest的事件树能互换吗？","不能。MemFolder匹配约束每节点最多一入一出，无锚点链整体分组；MemForest保留事件树层次并用anchor邻域传播。数据结构和检索假设不同。","教学例：一个父事件分出两条子事件可在树中表达，不能直接塞进无分支匹配链。","Can MemFolder's temporal chains replace MemForest's event trees?","No. MemFolder permits at most one incoming/outgoing edge and reassigns anchor-free chains together. MemForest preserves event-tree hierarchy and retrieves through anchor neighborhoods.","Teaching example: a parent event with two child events fits a tree but not a nonbranching matched chain."),
            ("matching-not-greedy","implementation","为什么不能把Hungarian换成逐条挑最大gain？","局部最大会占掉其他节点唯一可用的后继。最大总gain必须同时满足一入一出；本地用真正Hungarian，未用贪心捷径。","教学例：0→2为0.9、0→3为0.8、1→2为0.8；贪心拿0.9，总体匹配却能拿1.6。","Why not greedily take the largest link gain?","A local maximum can consume another predecessor's only useful successor. Maximum total gain must respect incoming/outgoing constraints; the local code uses actual Hungarian matching.","Teaching example: gains0→2=.9,0→3=.8,1→2=.8 give greedy.9 versus a globally compatible total1.6."),
        ],
    ),
]

PAPERS.append(dict(
    key="memlife", module="memlife", id="2609.40195",
    title="MemLife: Curating and Reasoning over Long-Term Egocentric Video Memories",
    cn_title="MemLife / MemOpt：把忠实、信息保留和可检索性分解给记忆写入器",
    author="Guangzhi Xiong", org="Meta Reality Labs / University of Virginia（Work done at Meta）",
    published="2026-09-30T17:11:33Z", announced_on=None, topic="记忆与技能", priority="P0",
    verified_priority_organizations=["Meta"], intake_class="historical_repository_backfill",
    source_path=".cache/nov21-latest/root-primary/2609.40195v1.pdf",
    intake_cn="这是9月30日首发、11月21日官方仓库事件发现的历史补漏，不算本日新论文。",
    intake_en="This is a historical addition first released September30 and discovered through a November21 official repository event, not a new paper today.",
    code="https://github.com/facebookresearch/MemLife/tree/4d987734f65832eb950fb8e7c346d7e69cc2ce16",
    code_license="CC-BY-NC-4.0",
    code_cn="是：[Meta官方固定提交](https://github.com/facebookresearch/MemLife/tree/4d987734f65832eb950fb8e7c346d7e69cc2ce16)，代码/数据为CC-BY-NC-4.0；本地按论文公式独立实现，未复制该仓库代码。",
    code_en="Yes: [fixed official Meta commit](https://github.com/facebookresearch/MemLife/tree/4d987734f65832eb950fb8e7c346d7e69cc2ce16),CC-BY-NC-4.0 code/data. Local arithmetic is independently derived from paper equations, not copied from that repository.",
    card="agent-research/memory-and-skills", peer="agent-research:memfolder", peer_path="agent-research/2611.26427-memfolder/README.md",
    page=4, crop=[65,60,548,292],
    locations=["§3.1 Eq.1-3 causal cutoff", "§3.3 Eq.7-12 FIRM and macro statistics", "Appendix B.3 trace replay", "Appendix B.4 Eq.15-16 clipping and whitening", "fixed official memlife/memopt/advantage.py"],
    method="MemLife先把每段第一视角视频和语音写成有时间锚点、实体落地的第一人称文本，再由reader按问题进行语义搜索和时间区间读取。MemOpt只训练writer，reader保持冻结；FIRM将逐token的faithfulness、逐候选的informativeness和retrievability相乘。前者看源视频是否支持内容，后两者分别看回答所需事实是否被保留、已缓存reader动作能否找回该候选，不把完整reader成败混成一个写入奖励。",
    method_en="MemLife writes video frames and speech into time-anchored,entity-grounded first-person episodes,then lets a reader search semantically and fetch intervals. MemOpt trains only the writer while freezing the reader. FIRM multiplies token-level faithfulness with candidate-level informativeness and retrievability: source grounding,retention of answer-relevant facts,and recovery through cached reader actions are assessed separately instead of conflating writer quality with an entire reader trajectory's success.",
    mechanism="Eq.11先对每个候选的response token求均值，再对候选做宏平均，避免长记忆独占基线。方差是每个候选围绕同一group均值的token偏差平方再宏平均，不能改成候选内部方差，否则丢掉informativeness/retrievability的候选间信号。Eq.12归一化后先clip到±3，再按组中有效response token加权重心化，最后全局masked whitening；prompt和padding始终排除。KL属于Eq.16 loss项，不进入FIRM奖励或优势统计。训练reward可用训练问答，问题独立的writer与被评测reader不可读测试答案。",
    mechanism_en="Eq.11 averages response tokens within each candidate before macro-averaging candidates,preventing long memories from dominating the baseline. Variance macro-averages token deviations around the same group mean,not each candidate's own mean; the latter would discard between-candidate informativeness/retrievability signal. Eq.12 normalization is clipped to plus/minus3,then response-token-recentered within each group,and finally globally mask-whitened. Prompt/padding positions stay excluded. KL is an Eq.16 loss term,not part of FIRM or advantage statistics. Training QA may construct training rewards,but the question-independent writer and evaluated reader cannot read test answers.",
    formula=r"x_{i,t}=R_{faith,i,t}R_{inf,i}R_{ret,i},\qquad\mu_g=\frac1G\sum_i\frac1{L_i}\sum_t x_{i,t},\qquad\sigma_g^2=\frac1G\sum_i\frac1{L_i}\sum_t(x_{i,t}-\mu_g)^2,\qquad\widetilde A_{i,t}=\frac{x_{i,t}-\mu_g}{\sigma_g+\epsilon_n}.",
    result="Table1中SuperMemory-VQA：训练前MemLife准确率56.50、EgoRAG49.28，相差7.22个百分点；MemOpt将MemLife提高到60.35，再增3.85个百分点。训练使用S1–S6，validation为S7–S8，test为S9–S10；按validation的准确率加检索recall选checkpoint，其他benchmark仅作test。Oracle Context直接提供标注证据，不是正常reader的可用输入。论文没有生产线上A/B，以上不属于本地测量。",
    result_en="Table1 reports SuperMemory-VQA accuracy56.50 for untrained MemLife versus49.28 for EgoRAG,a7.22-percentage-point difference. MemOpt raises MemLife to60.35,another3.85points. Training uses subjectsS1-S6,validationS7-S8 and testS9-S10; checkpoint selection maximizes validation accuracy plus retrieval recall,with other benchmarks test-only. Oracle Context supplies annotated evidence directly and is not normal reader input. No production A/B is reported; none of these scores is measured locally.",
    local="本地只接收显式概率/奖励数组与response mask，执行Eq.7的概率差、FIRM乘积、Eq.11-12宏统计、clip/组内token重心化/全局whitening和Eq.16已给ratio/advantage/KL的标量loss算术。独立NumPy float64实现，normalization epsilon=1e-6，whitening epsilon=1e-8、样本方差correction=1作为显式数值协议；不声称与外部trainer逐bit相同。空候选从G排除，空group输出0；全batch少于2个有效token则拒绝，不补造whitening。另有最多512条的显式unit-vector SearchMemory/FetchMemory：先按end≤query_time及区间完整包含过滤，再排序；返回按时间排列。单subject过滤是本地隔离合同，不是论文LVQA混合受试者基准，也不认证调用者身份。没有视频/embedding模型、VLM评审、writer/reader、训练数据构建、cached reader trace生成、RL训练或Evolve接入。",
    local_en="The local slice takes explicit probability/reward arrays and response masks for the Eq.7 margin,FIRM product,Eq.11-12 macro statistics,clipping/group-token recentering/global whitening,and Eq.16 scalar loss from supplied ratios,advantages and KL. An independently derived NumPy float64 protocol uses normalization epsilon1e-6,whitening epsilon1e-8 and sample-variance correction1; bitwise trainer equivalence is not claimed. Empty candidates are excluded fromG,empty groups output zero,and fewer than two valid batch tokens are rejected. Bounded unit-vector SearchMemory/FetchMemory first filter full interval containment and end<=query_time,then rank and return chronologically. Single-subject filtering is a local isolation contract,not the paper's mixed-subject LVQA benchmark or caller authentication. No video/embedding model,VLM judge,writer/reader,training-data construction,cached-reader trace collection,RL trainer or Evolve integration is implemented.",
    controls="长度不等候选构造宏均值0.5而token池均值0.25，检验group方差0.25而非候选内方差0；稀疏离群值检验clip后重心化。有效response奖励限定[0,1]；极大有限padding先归零，有限输入的ratio乘advantage或KL项溢出也明确拒绝，不能输出inf或把溢出方差伪装成零优势。负控还包括全平group、空候选/padding、无效概率、KL只影响独立loss、不改变奖励、严格未来片段和其他subject在检索前排除、恰好query_time的片段可用。所有输入是合成显式控制值，没有任何gold QA或视频内容输入reader；通过率不是长视频QA能力。",
    controls_en="Unequal-length candidates distinguish a macro mean.5 from pooled-token mean.25,and group variance.25 from zero within-candidate variance. Sparse outliers check post-clip recentering. Valid response rewards are restricted to[0,1];extreme finite padding is erased before arithmetic,and overflow from finite ratios times advantages or KL terms is rejected rather than returning infinity or disguising an overflowed variance as zero advantage. Further controls cover flat groups,empty candidates/padding,invalid probabilities,KL affecting only the separate loss,and future/other-subject entries excluded before ranking while exact-cutoff entries remain available. Inputs are explicit synthetic controls,no gold QA or video is passed to a reader,and pass rates are not video-QA capability.",
    cost="固定论文以9B writer/reader和27B迁移组合处理长时视频，writer训练3个epoch并每轮重建记忆和reader trace；官方固定仓库完整训练要求一个8卡训练节点及一个8卡评估节点。单A100/A30或Mac不能廉价等价复现实验矩阵，完整训练和benchmark直接不复现；不下载权重或视频、不启动试跑，只做小数组CPU控制。",
    cost_en="The fixed paper evaluates9B writer/reader and27B transfer combinations over long video histories,trains for three epochs,and rebuilds memories and reader traces. The pinned official repository's full setup requires one eight-GPU training node and one eight-GPU evaluation node. This is not an affordable equivalent on oneA100/A30 or a Mac. Full training/benchmarks are not reproduced; no weights/videos or trial runs are launched,only small CPU array controls.",
    compare="MemFolder主要改变已有记忆如何分组、合并与编码，MemOpt则改变writer生成什么文本以及如何分配训练credit；前者的结构压缩和后者的写入奖励不互相替代。MemFolder的ContextFolder blind reader看不到源记录/预期答案；MemOpt训练评审可用源视频和训练问答，但这些信息不得流向被评测reader。二者本地都是L1数学组件，不能把分组数或优势方差当QA准确率比较。",
    compare_en="MemFolder mainly changes how existing memories are grouped,merged and encoded;MemOpt changes what a writer generates and how training credit is assigned. Structural compression and writer rewards do not substitute for one another. ContextFolder's blind reader cannot see source records/expected answers;MemOpt training judges may use source video and training QA,but those inputs must not reach the evaluated reader. Both local slices areL1 mathematics,so group counts or advantage variances cannot compare QA accuracy.",
    flow_cn="A[显式faith token与inf ret候选分数] --> B[FIRM乘积]\n  B --> C[长度公平宏均值与group偏差]\n  C --> D[clip 组内token重心化 全局whiten]\n  D --> E[显式ratio与KL的loss算术]\n  M[显式时间记忆与unit vector] --> F[subject与因果区间先过滤]\n  F --> G[语义排序与时间顺序返回]",
    flow_en="A[Supplied faith tokens and inf ret scalars] --> B[FIRM product]\n  B --> C[Length-fair macro mean and group deviation]\n  C --> D[Clip group-token recenter global whiten]\n  D --> E[Loss arithmetic from ratios and KL]\n  M[Explicit timed entries and unit vectors] --> F[Subject and causal interval filter first]\n  F --> G[Similarity rank and chronological return]",
    questions=[
        ("three-reward-dimensions","basics","记忆忠实于视频，就一定能回答未来问题吗？","不一定。它还可能漏掉关键事实或在大检索库中找不到。FIRM分别衡量faithfulness、informativeness、retrievability，三者相乘而非只看最终答案。","教学例：准确写“我进了房间”很忠实，但若没写钥匙放在哪，就无法回答钥匙位置。","Is a faithful memory necessarily useful for future questions?","No. It may omit a key fact or remain undiscoverable in a large store. FIRM separately scores faithfulness,informativeness and retrievability and multiplies them.","Teaching example: I entered the room can be faithful while omitting where the keys were placed."),
        ("macro-deviation","mechanism","为什么方差不能改成每条候选围绕自身均值的方差？","informativeness和retrievability在一条候选中是常数，它们的差异主要在候选之间；围绕自身均值会把这个信号删掉。Eq.11围绕同一group均值再做长度公平宏平均。","教学例：一条全1、一条全0的候选，各自内部方差都为0，但group显然有不同质量，正确方差为0.25。","Why not use within-candidate variance?","Informativeness and retrievability are constant within a candidate,so their signal lies between candidates. Eq.11 retains it by measuring deviations around the shared group mean before macro averaging.","Teaching example: all-one and all-zero candidates each have zero internal variance,but the correct group variance is.25."),
        ("writer-vs-folding","comparison","MemOpt和MemFolder都优化记忆，优化的对象一样吗？","不一样。MemOpt分解训练奖励以改writer输出；MemFolder整理和压缩已有记录。不能把检索单元变少等同于writer更忠实或更会保留事实。","教学例：把两条记忆合为一组是结构整理，降低幻觉token的训练credit是写入器优化。","Do MemOpt and MemFolder optimize the same object?","No. MemOpt decomposes training rewards to improve writer outputs;MemFolder organizes and compresses existing records. Fewer retrieval units do not prove greater faithfulness or fact retention.","Teaching example: grouping two records changes structure;lowering credit for a hallucinated token optimizes the writer."),
        ("causal-before-rank","implementation","能先在全部记忆里top-k，再过滤未来和其他subject吗？","不能。未来或不属于当前隔离scope的高分项会挤掉合法结果。应先用end≤query_time和显式subject/区间限定候选，再做相似度排序；这只是本地隔离接口，不是身份认证。","教学例：明天的片段相似度1、昨天为0.8，k=1时先top-k再过滤会错误返回空，而正确结果是昨天的片段。","May search rank all memories before filtering scope and time?","No. Future or out-of-scope high scores can displace eligible results. Filter end<=query_time and explicit subject/interval first,then rank. This local isolation interface is not identity authentication.","Teaching example: with tomorrow scoring1 and yesterday.8,ranking top1 before filtering wrongly returns nothing rather than yesterday."),
    ],
))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    for aid in ("2611.26132", "2611.26427"):
        for kind, suffix in (("abs", "abs.html"), ("html", "html"), ("pdf", "pdf")):
            path = CACHE / f"{aid}.{suffix}"
            if not path.exists():
                request = Request(f"https://arxiv.org/{kind}/{aid}v1", headers={"User-Agent": "auto-research/primary-review"})
                with urlopen(request, timeout=30) as response:
                    raw = response.read(15_000_001)
                if len(raw) > 15_000_000:
                    raise ValueError("source capture exceeds small-paper budget")
                path.write_bytes(raw)
            print(path.name, path.stat().st_size, digest(path), flush=True)


def author(*, append_memlife=False, refresh_memlife=False):
    import fitz
    from english_learning_sources import question_units

    bundle, english, proposals, reviews = {}, {}, [], []
    bundle_path = AUDIT / "agent-authored-bundle.json"
    if append_memlife or refresh_memlife:
        previous = json.loads(bundle_path.read_text())
        bundle, english = previous["papers"], previous["english_question_units"]
        proposals = json.loads((AUDIT / "deep-dive-proposals-agent.json").read_text())["proposals"]
        reviews = json.loads((AUDIT / "agent-review.json").read_text())["reviews"]
        if append_memlife and "agent-research:memlife" in bundle:
            raise ValueError("MemLife already appended; preserve reviewed content")
        if refresh_memlife:
            if "agent-research:memlife" not in bundle:
                raise ValueError("refresh requires the existing owned MemLife addition")
            del bundle["agent-research:memlife"]
            english = {k: v for k, v in english.items() if not k.startswith("qa/agent-research:memlife/")}
            proposals = [p for p in proposals if p["paper"] != "agent-research:memlife"]
            reviews = [r for r in reviews if r["identity"] != "agent-research:memlife"]
    elif bundle_path.exists():
        raise ValueError("append-once authored bundle already exists; review edits in place")
    for paper in (p for p in PAPERS if not (append_memlife or refresh_memlife) or p["key"] == "memlife"):
        key, aid = paper["key"], paper["id"]
        identity = "agent-research:" + key
        directory = ROOT / f"docs/agent-research/{aid}-{key}"
        assets = directory / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        source = ROOT / paper["source_path"] if paper.get("source_path") else CACHE / f"{aid}.pdf"
        source_hash = digest(source)
        image = assets / "paper-figure-01.png"
        pdf = fitz.open(source)
        pdf[paper["page"] - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(paper["crop"])).save(image)
        pdf.close()
        image_hash = digest(image)
        write(assets / "provenance.json", {"schema_version": 1, "reviewed_on": DATE, "figures": [{
            "file": image.name, "paper_id": aid, "version": "v1", "figure": "Figure 2",
            "source_url": f"https://arxiv.org/pdf/{aid}v1#page={paper['page']}",
            "paper_url": f"https://arxiv.org/abs/{aid}v1", "source_kind": "fixed_version_pdf_crop_rendered_png",
            "source_sha256": source_hash, "asset_sha256": image_hash, "image_sha256": image_hash,
            "page": paper["page"], "crop_points": paper["crop"], "render_dpi": 144,
            "caption_included": True, "scientific_content_modified": False, "visual_review_done": True,
            "attribution": "Copyright belongs to the original authors; original method figure, not local results.",
            "license": "See original arXiv source; no new license granted."}]})
        module = "auto_research.agent_research." + paper["module"]
        local = "src/auto_research/agent_research/" + paper["module"] + ".py"
        test = "tests/test_nov21_" + paper["module"] + ".py"
        command = f"PYTHONPATH=src python -c 'from {module} import diagnostic; print(diagnostic(42))'"
        peer_link = os.path.relpath(ROOT / "docs" / paper["peer_path"], directory)
        cn = f'''# {paper["cn_title"]}

> `component_only` / L1 CPU机制组件，`diagnostic_only=true`。{paper.get("intake_cn", "这是11月19日首发、11月20日公告的重叠池补漏，不算11月21日新论文。")}高成本完整实验不复现（审查 DONE），不是能力复现或已接入Evolve。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [{paper["title"]}](https://arxiv.org/abs/{aid}v1)，本轮固定v1 |
| 公司/机构/学校 | 一作{paper["author"]}；{paper["org"]} |
| 首次公开日期 | {paper["published"].replace("T", " ").replace("Z", " UTC")}，arXiv v1；{("公告日期" + paper.get("announced_on", "2026-11-20")) if paper.get("announced_on", "2026-11-20") else "本轮未单独核验公告日；2026-11-21发现官方仓库事件"} |
| 原作者开源代码 | {paper["code_cn"]} |
| 本地 Adapter / 方法 | 无完整adapter（`adapter: null`）；组件key `{key}` |
| 本地复现代码 | `{local}`；测试 `{test}` |

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

[![原论文Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/{aid}v1#page={paper['page']})

图片来自[原论文](https://arxiv.org/pdf/{aid}v1#page={paper['page']})固定v1第{paper['page']}页Figure 2及原始图注，版权归原作者所有；仅裁去无关正文/留白，科学内容未修改。[来源与裁剪SHA256](assets/provenance.json)。这是作者方法图，不是本地实验。
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

```bash
{command}
PYTHONPATH=src python -m pytest {test} -q
```

本轮只用显式合成控制输入，不加载公开能力benchmark，不存在据test选超参的流程。批次冻结源码后的统一runner生成[42/43/44三种子CPU诊断](metrics/component-cpu-seeds42-44.json)，三种子不改变L1层级，也不是三个独立模型训练。

### 同主题比较与边界

与[{paper["peer"]}]({peer_link})对照：{paper["compare"]}

{paper["controls"]}

### 高成本完整实验

{paper["cost"]} **成本过高，不复现（审查 DONE）。** 完整实验是已终态的成本决定，不进入自动重试或实现队列；便宜组件通过不等于完整论文已被复现。
'''
        page = directory / "README.md"
        page.write_text(cn)
        cn_hash = digest(page)
        en = f'''# {paper["title"]}

<!-- source-sha256: {cn_hash} -->

[简体中文](README.md)

> `component_only` / L1 CPU mechanism diagnostic, not capability reproduction or executable Evolve integration. {paper.get("intake_en", "This is an overlap addition first released November19 and announced November20, not a new November21 paper.")} High-cost full experiments are not reproduced (review DONE).

## Paper information

| Field | Value |
| --- | --- |
| Paper | [Fixed v1](https://arxiv.org/abs/{aid}v1) |
| First author and affiliation | {paper["author"]}; {paper["org"]} |
| Original publication | {paper["published"].replace("T", " ").replace("Z", " UTC")}; {("announcement " + paper.get("announced_on", "2026-11-20")) if paper.get("announced_on", "2026-11-20") else "announcement date not separately verified; official repository event observed2026-11-21"} |
| Original source code | {paper["code_en"]} |
| Local adapter / key | No full adapter (`adapter: null`); component `{key}` |
| Local code | `{local}`; tests `{test}` |

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

[![Original Figure 2](assets/paper-figure-01.png)](https://arxiv.org/pdf/{aid}v1#page={paper['page']})

Figure2 and original caption from fixed-v1 PDF page{paper['page']}; copyright belongs to the original authors. Only unrelated text/whitespace is cropped; scientific content is unchanged. [Source](https://arxiv.org/pdf/{aid}v1#page={paper['page']}) and [crop/SHA256 provenance](assets/provenance.json). This illustrates the author's method, not local evidence.

### Core equations

$$
{paper["formula"]}
$$

### Reported offline and online results

{paper["result_en"]}

## Local reproduction and limits

### Data protocol and code mapping

{paper["local_en"]}

```bash
{command}
PYTHONPATH=src python -m pytest {test} -q
```

Only explicit synthetic control inputs are used. No capability benchmark is loaded and no hyperparameters are selected on test data. After the batch source freeze, the shared runner writes [three-seed CPU diagnostics](metrics/component-cpu-seeds42-44.json). Three seeds do not promote L1 evidence or constitute independent model training.

### Same-topic comparison and limits

Reviewed against [{paper["peer"]}]({peer_link.replace("README.md", "README-en.md")}): {paper["compare_en"]}

{paper["controls_en"]}

### High-cost full experiments

{paper["cost_en"]} **Too costly; not reproduced (review DONE).** This is a terminal decision, not an automatic retry or implementation queue. Passing the cheap slice does not reproduce the full paper.
'''
        page.with_name("README-en.md").write_text(en)
        spec = {"key": key, "domain": "agent-research", "title": paper["title"],
                "first_author": paper["author"], "first_author_affiliation": paper["org"],
                "published_at": paper["published"], "published": paper["published"][:10],
                "announced_on": paper.get("announced_on", "2026-11-20"), "paper_url": f"https://arxiv.org/abs/{aid}v1",
                "reviewed_version": "v1", "reviewed_arxiv_id": aid + "v1", "reviewed_version_url": f"https://arxiv.org/pdf/{aid}v1",
                "detail_path": f"agent-research/{aid}-{key}/README.md", "topic": [paper["topic"], key],
                "verified_priority_organizations": paper.get("verified_priority_organizations", []), "code": paper["code"], "code_status": paper["code_cn"],
                "code_license": paper.get("code_license"), "adapter": None, "priority": paper.get("priority", "P1"), "intake_class": paper.get("intake_class", "overlap_backfill"),
                "implementation_status": "component_only", "local_operator": module + ".diagnostic",
                "local_command": command, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
                "promotion_eligible": False, "evolve_integrated": False, "requires_gpu_validation": False,
                "gpu_validation_passed": False, "gpu_validation_artifact": None,
                "review_done": True, "full_experiment_review_done": True,
                "full_experiment_status": "not_reproduced_high_cost", "review_resolution": "not_reproduced_high_cost",
                "automatic_retry": False, "automatic_implementation_queue": False,
                "cost_assessment": {"source": f"https://arxiv.org/pdf/{aid}v1", "available_resource": "one A100 or A30, or local Mac",
                                    "basis": paper["cost"], "decision": "成本过高，不复现（审查 DONE）；仅低成本CPU组件。"},
                "summary": paper["method"], "fidelity_note": paper["local"], "method_source_sha256": source_hash}
        write(ROOT / f"src/auto_research/paper_specs/catalog/agent-research/{key}.json", spec)
        bank = []
        for qid, level, question, answer, example, eq, ea, ee in paper["questions"]:
            row = {"id": qid, "level": level, "question": question, "answer": answer, "example": example,
                   "source_sections": HEADINGS, "added": DATE}
            bank.append(row)
            uid = f"qa/{identity}/{qid}"
            english[uid] = {"source_sha256": question_units({identity: [row]})[uid].source_sha256,
                            "reviewed": True, "fields": {"question": eq, "answer": ea, "example": ee}}
        bundle[identity] = {"questions": bank}
        comparison = next(row for row in bank if row["level"] == "comparison")
        english_comparison = next(row for row in paper["questions"] if row[1] == "comparison")
        proposals.append({"paper": identity, "target_card": paper["card"],
                          "source_revisions": {identity: cn_hash, paper["peer"]: digest(ROOT / "docs" / paper["peer_path"])},
                          "comparison": {"position": paper["method"], "tradeoff": paper["compare"], "sections": HEADINGS},
                          "analysis": {"title": paper["cn_title"], "body": paper["mechanism"] + paper["controls"], "papers": [identity, paper["peer"]]},
                          "question": {"id": "cross-nov21-" + key, **{field: comparison[field] for field in ("question", "answer", "example")}, "papers": [identity, paper["peer"]]},
                          "update": {"date": DATE, "papers": [identity, paper["peer"]], "summary": paper["local"] + " 完整实验高成本不复现。"},
                          "english": {"comparison": {"position": paper["method_en"], "tradeoff": paper["compare_en"]},
                                      "analysis": {"title": paper["title"], "body": paper["mechanism_en"] + " " + paper["controls_en"]},
                                      "question": {"question": english_comparison[5], "answer": english_comparison[6], "example": english_comparison[7]},
                                      "update": paper["local_en"] + " Full experiments are not reproduced."}})
        review = {"id": aid, "key": key, "identity": identity, "published_at": paper["published"],
                        "announced_on": paper.get("announced_on", "2026-11-20"), "first_author": paper["author"], "first_author_affiliation": paper["org"],
                        "source_url": f"https://arxiv.org/pdf/{aid}v1", "source_sha256": source_hash,
                        "locations": paper["locations"], "code": paper["code"], "code_status": paper["code_en"],
                        "implementation_status": "component_only", "evaluation_tier": "l1_mechanism",
                        "scope": paper["local_en"], "cost_basis": paper["cost_en"],
                  "full_experiment_status": "not_reproduced_high_cost", "requires_gpu_validation": False, "review_done": True}
        if key == "memlife":
            upstream = ROOT / ".cache/nov21-latest/root-primary/memlife-advantage-4d987734.py"
            review["upstream_arithmetic_reference"] = {
                "commit": "4d987734f65832eb950fb8e7c346d7e69cc2ce16",
                "path": "memlife/memopt/advantage.py", "source_sha256": digest(upstream),
                "implementation_copied": False,
                "note": "Read to resolve empty-candidate and post-clip token-recentering details; local implementation independently derived from equations."}
            review["numeric_review_fixes_before_freeze"] = [
                "Out-of-range finite FIRM rewards are rejected before variance arithmetic; finite padding is erased before deviations.",
                "Finite ratio/advantage or KL overflow fails closed at objective intermediates/final loss, with unit regressions and actual diagnostic checks."]
        reviews.append(review)
    write(AUDIT / "agent-authored-bundle.json", {"schema_version": 1, "date": DATE, "papers": bundle, "english_question_units": english})
    write(AUDIT / "deep-dive-proposals-agent.json", {"schema_version": 1, "reviewed_on": DATE, "integration_owner": "root", "proposals": proposals})
    write(AUDIT / "agent-review.json", {"schema_version": 1, "reviewed_on": DATE, "scope": "Two Nov19-first-release overlap additions and one Sep30 Meta historical repository addition; no new-Nov21 or exhaustive claim.",
                                       "implementation_preflight_completed": True, "available_resource": "one A100 or A30 or Mac; CPU-only bounded kernels here", "reviews": reviews, "p2_dispositions": []})
    print(f"Authored scope: {len(bundle)} bilingual papers,{len(english)} reviewed bilingual questions and{len(proposals)} same-topic proposals; no shared bank integration.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--append-memlife", action="store_true", help="Append newly approved Meta historical addition without rewriting the first two papers")
    parser.add_argument("--refresh-memlife", action="store_true", help="Re-author only the unmerged owned MemLife files after explicit source review")
    args = parser.parse_args()
    if args.fetch:
        fetch()
    else:
        author(append_memlife=args.append_memlife, refresh_memlife=args.refresh_memlife)


if __name__ == "__main__":
    main()
