"""Append-once, reviewed industrial component docs and bilingual teaching."""
from hashlib import sha256
import json
from pathlib import Path

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov26-latest"
DATE = "2026-11-26"

PAPERS = {
    "onequery": {
        "id": "2611.33653", "title": "OneQuery: Unified Sequence-to-Structure Generation for Multilingual E-commerce Query Understanding",
        "published_at": "2026-11-25T02:19:27Z", "author": "Mingyu Zhang", "affiliation": "Xiamen University; co-first author Jiejie Qin, Alibaba Group; Harbin Institute of Technology collaborator",
        "company": "Alibaba", "pdf": "onequery.pdf", "figure": "Figure2", "crop": [50, 85, 563, 397], "cuda": False,
        "topic": ["大模型能力与推荐融合", "查询理解与结构化生成"], "card": "retrieval-matching", "peer": "larf",
        "method": ["OneQuery把语言识别、纠错、英语翻译和查询标注作为同一次schema引导JSON生成，而不是四个独立模型逐级传错。Stage1混合四类单任务SFT；Stage2从部分标注中保留真值、用Stage1补齐缺字段，清洗后混合3.6M伪标注与310K人工样本；Stage3用任务特定reward做GRPO。生产端14B离线缓存头部查询，蒸馏0.3B学生实时处理尾部。", "OneQuery produces language, spelling, English translation and semantic tags in one schema-guided JSON generation rather than propagating errors through four independent models. Stage1 mixes single-task SFT. Stage2 retains observed labels and fills missing fields using Stage1, then combines3.6M cleaned pseudo-labels with310K human records. Stage3 uses task-specific rewards with GRPO. Production caches head-query outputs from14B offline and serves tail queries using a distilled0.3B student."],
        "formula": ["Eq7的默认非均匀权重来自§5.4 reward-v4：(0.35,0.25,0.25,0.15)。比较前做NFKC、小写与空白规整。语言和翻译严格exact match；QT比较完整(type,text)集合，不是F1。需要纠错时，正确串得1，否则只给0.3倍归一化Levenshtein相似度；无需纠错时，只有保留原串得1。Eq5为组内均值/标准差优势，Eq6同时处理正负优势的clipped ratio。", "Equation7 uses the nonuniform reward-v4 weights from Section5.4:(0.35,0.25,0.25,0.15). Comparisons follow NFKC, lowercasing and whitespace normalization. Language and translation require exact matches; QT requires equality of the whole(type,text) set, not F1. When correction is needed, an exact correction earns1 and other outputs earn0.3 times normalized Levenshtein similarity. When no correction is needed, only preserving the input earns1. Equations5/6 define within-group normalized advantages and signed clipped-ratio arithmetic."],
        "reported": ["Table1的14B pipeline→Stage3：语言Acc0.9514→0.9665，Translation ROUGE-2 78.20→80.50，纠错F1 0.8568→0.8717，QT F1 0.8128→0.8366。§5.6在AliExpress多国真实A/B，对照是现有线上QU系统；L2P+0.5%、SBS人工相关性+0.8pt。未披露流量比例、样本数、持续时长或置信区间；不能把SBS百分点写成相对百分比。线上收益属于完整缓存/学生/下游链路，不是reward算子的本地效果。", "Table1 compares14B pipeline with Stage3: language accuracy0.9514→0.9665, translation ROUGE-2 78.20→80.50, spelling F1 0.8568→0.8717 and QT F1 0.8128→0.8366. Section5.6 reports real multi-country AliExpress A/B against the existing production QU system: L2P+0.5% and human SBS relevance+0.8points. Traffic fraction, sample count, duration and confidence intervals are undisclosed; SBS points are not a relative percentage. These are full cached/student/downstream-system results, not local reward measurements."],
        "local": ["本地只执行Eq5–13的reward、优势和clipping算术。QT输入为显式tuple列表，不发明私有标注串的parser；无效schema直接拒绝，不猜造格式reward。空串对空串编辑相似度取1、sigma采用总体标准差、delta=1e-8是显式边界约定。没有语言模型、schema约束解码、部分标注补齐、SFT、GRPO参数训练、蒸馏或服务；gold只作为reward计算输入，不存在读取gold的Agent。", "The local component executes only Equations5–13 reward, advantage and clipping arithmetic. QT is an explicit tuple list, not a fabricated parser for a private tag syntax. Invalid schemas are rejected rather than receiving an invented format reward. Empty-versus-empty edit similarity1, population standard deviation and delta1e-8 are declared boundary conventions. There is no language model, constrained decoder, label completion, SFT, GRPO parameter training, distillation or serving. References enter only the reward evaluator; no agent can read gold."],
        "controls": ["CPU三seed仅生成小组随机reward，验证NFKC/顺序不变、缺一个QT实体即0、无需纠错的改写为0、partial reward不超过0.3、常数组优势为0和正负ratio截断。显式权重按原值加权，不自动二次归一。所有结果为L1机制诊断，既不衡量查询理解准确率，也不支持Evolve晋级。", "CPU three-seed cases use small generated reward groups and check NFKC/set-order invariance, zero QT credit when one entity is missing, rejection of unnecessary corrections, partial spelling credit at most0.3, zero constant-group advantages and both signs of ratio clipping. Supplied weights are not silently renormalized. This is an L1 diagnostic, not query-understanding accuracy or Evolve evidence."],
        "comparison": ["LARF把单文档相关性建成五维ordinal标签，并使用PNR、规则反馈和terminal digit margin；OneQuery监督的是同一query的四个异构结构字段。OneQuery的QT reward是完整集合exact match，不能换成LARF的分级距离或文档间有序pair。LARF训练期生成head/服务分类head也不等于OneQuery的头部缓存/尾部蒸馏。两篇作者线上指标不可直接比较。", "LARF models five ordinal relevance attributes of one document with PNR, rule feedback and terminal-digit margins. OneQuery instead supervises four heterogeneous structured fields of one query. Its QT reward requires whole-set exact matching, not LARF's graded distance or inter-document ordering. LARF's training generation/serving classification split also differs from OneQuery's head cache/tail distillation. Their production metrics are not directly comparable."],
        "cost": ["§5.1以ME-LLM5.2-14B（另有4B/8B）做完整三阶段，16×A100-80GB，3.6M伪标注+310K人工样本、31K RL query、每query8次采样；另含私有评测19,087条和线上蒸馏/缓存/A/B。总GPU小时未披露，不能从0.3B服务学生反推训练便宜。成本过高，不复现（审查 DONE）；不下载模型或训练数据、不探跑、不重试。", "Section5.1 uses ME-LLM5.2-14B and4B/8B variants in the complete three-stage pipeline on16 A100-80GB GPUs, with3.6M pseudo-labels,310K human records,31K RL queries and eight samples per query, plus19,087 private evaluation queries and production distillation/cache/A/B. Total GPU-hours are undisclosed; a0.3B serving student does not make the training campaign cheap. High cost, not reproduced(review DONE), with no model/data downloads, probes or retries."],
    },
    "camar": {
        "id": "2611.33628", "title": "Multi-Modal Causal Disentanglement for Multi-Domain Sequential Audio Recommendation",
        "published_at": "2026-11-25T01:57:30Z", "author": "Yu Ren", "affiliation": "Hangzhou Dianzi University / NetEase Cloud Music; co-first author Pengcheng Li, NetEase Cloud Music",
        "company": "NetEase", "pdf": "camar.pdf", "figure": "Figure1", "crop": [44, 38, 568, 306], "cuda": True,
        "topic": ["生成、排序与冷启动", "多任务学习与多目标优化"], "card": "history-ranking-backbones", "peer": "lazunirec",
        "method": ["CAMAR先用共享跨域RQ-VAE语义ID、独立域序列encoder形成偏好，再用有向域对的两层ReLU PCN对缺失域补全。每域线性拆出invariant/specific两部分；平方内积约束二者，GRL分类器去除invariant的域信息，仅invariant参与active-domain self-attention，最后按域gate融合共享向量与本域specific。该结构约束不是仅靠一个正则项声称发现真实因果因素。", "CAMAR first combines shared cross-domain RQ-VAE semantic IDs with independent domain sequence encoders, then uses directed-pair two-layer ReLU PCNs to impute missing domains. Linear maps split invariant and specific factors. Squared inner products separate them, a GRL classifier discourages domain identity in invariant factors, only invariant factors enter active-domain self-attention, and domain gates fuse the shared vector with the domain's own specific factor. This architectural constraint is not proof of identifying real causal factors."],
        "formula": ["Eq5的PCN输入stop-gradient；Eq7的target也stop-gradient，表示匹配只更新PCN。Eq10是未归一化内积的平方，不是cosine。Eq11/12的GRL只反转classifier输入的梯度，不能把recall梯度也反向。Eq13对active域双向attention并只平均active输出，inactive imputed因子绕过attention，不污染shared；specific始终留在本域。Eq14逐元素gate后L2归一，Eq15每域用户均值后跨域求和。", "Equation5 stops gradients at the PCN input and Equation7 also stops the target, so representation matching updates only PCNs. Equation10 squares the unnormalized inner product, not cosine similarity. Equations11/12 reverse gradients at the classifier input, not recall gradients. Equation13 attends bidirectionally among active domains and averages only active outputs; inactive imputed factors bypass attention and cannot contaminate the shared factor. Specific factors remain local. Equation14 applies elementwise gates then L2 normalization; Equation15 sums per-domain user-mean losses."],
        "reported": ["§V-E/TableV：2026年5月在网易云音乐进行两周生产A/B，对照是原线上各域召回；实验组新增CAMAR通道，但共享相同精排/重排模块。Song会话平均播放时长+1.0%，Playlist喜欢率+3.0%，Podcast会话平均播放时长+1.6%；论文称统计显著但没有给p值/CI/流量比例。私有TableII/Public TableIII的离线收益属于完整模型；不能归给本地GRL或合成loss。", "SectionV-E/TableV reports a two-week NetEase Cloud Music production A/B in May2026. Treatment adds CAMAR as a recall channel over existing per-domain recall while holding ranking/reranking shared. Song session listening duration increases1.0%, Playlist like rate3.0%, and Podcast listening duration1.6%. The paper states significance without p-values, confidence intervals or traffic fractions. Offline TablesII/III describe full models, not gains attributable to this local GRL or synthetic loss."],
        "local": ["只实现给定per-domain state/candidate张量上的Eq5–7、9–15：真实两层PCN、双线性factor、单层active-only MHA、域gate/classifier、GRL、正交和sampled-softmax。没有多模态encoder、RQ-VAE/语义码本、item/history backbone、Eq8 task-level冷启动Lcf、完整LTN或三阶段训练器；因此不宣称完整CAMAR。bias-free factor、MHA细节/MLP隐藏宽度等原文未唯一给出，显式采用本地参考配置。", "The component executes Equations5–7 and9–15 on supplied domain states/candidates: real two-layer PCNs, linear factor maps, one active-only MHA layer, domain gates/classifier, GRL, orthogonality and sampled softmax. Multi-modal encoders, RQ-VAE/semantic codebooks, item/history backbones, Equation8 task-level cold-start loss, complete LTN and the three-stage trainer are absent; this is not full CAMAR. Bias-free factor maps, MHA details and MLP hidden widths are declared local choices where the paper does not uniquely specify them."],
        "controls": ["三seed使用4用户×3域×8维合成state和每域5候选，做真实autograd/Adam更新。负控检查inactive补全与表示target/source均无encoder梯度、GRL只反转输入不反转classifier参数、改某域specific不影响其他域、把inactive invariant放大1000不改shared、输出L2范数为1。零active用户、无overlap表示监督和不合法形状直接拒绝。局部公式通过不证明Hit/NDCG、泛化、生产收益或因果独立性。", "Three seeds use4 users,3 domains,width8 and five candidates per domain with real autograd/Adam updates. Controls verify detached imputation/source/target paths, GRL reversal only at inputs rather than classifier parameters, domain-specific noninterference, unchanged shared vectors after multiplying inactive perturbations by1000, and unit-norm outputs. Zero-active users, overlap-free representation supervision and invalid shapes are rejected. These checks establish neither Hit/NDCG, generalization, production lift nor causal independence."],
        "comparison": ["LazUnirec对召回/排序任务用private LoRA/expert及梯度方向可靠性调权；CAMAR对song/playlist/podcast域显式拆invariant/specific，并只让invariant跨域。前者主要控制共享参数更新冲突，后者同时限制表示流动和域可辨识性。梯度稳定不等于域不变，内积正交也不等于统计独立；两者的私有数据与本地合成诊断都不能支持直接胜负比较。", "LazUnirec uses private LoRA/experts and directional-reliability weights across retrieval/ranking tasks. CAMAR splits invariant/specific factors across song/playlist/podcast and permits only invariant cross-domain interaction. The former controls shared-update conflict; the latter constrains representation flow and domain distinguishability. Stable gradients do not establish domain invariance, and orthogonal inner products do not establish statistical independence. Neither private data nor local synthetic diagnostics support a direct quality ranking."],
        "cost": ["§V-A/TableI约539M私有交互和16M Amazon交互；需多模态特征/RQ-VAE预处理、独立序列骨干、9基线/消融、多域全库评测与两周线上A/B。原文列A100 GPUs、4095负例和验证权重搜索，未给GPU数量/总小时。完整矩阵明显超单A100/A30或Mac短时预算：成本过高，不复现（审查 DONE）。只验小算子，不下载数据/权重或启动完整试跑。", "SectionV-A/TableI covers about539M private and16M Amazon interactions, multi-modal/RQ-VAE preprocessing, sequence backbones, nine baselines/ablations, multi-domain full-catalog evaluation and two-week production A/B. The paper lists A100 GPUs,4095 negatives and validation weight search without GPU count or total hours. The complete matrix exceeds this single-A100/A30-or-Mac short-run budget: high cost, not reproduced(review DONE). Only small components run; no data/checkpoint downloads or full probes."],
    },
}

QA = {
    "onequery": [
        ("把四项任务放进一个JSON，改变了什么？", "模型可从原查询联合生成四字段，避免独立流水线只看到上游错误结果；但联合格式本身不保证语义一致，仍需训练与清洗。", "教学例：错译商品词会误导流水线QT；联合模型同时看原始拼写和其他字段，有机会纠正，但本地reward并不具备这种生成能力。", "What changes when four tasks share one JSON output?", "The model generates four fields jointly from the original query instead of inheriting only erroneous upstream outputs. A shared format does not guarantee consistency; training and cleaning remain necessary.", "Teaching example: a mistranslated product term can mislead pipeline QT. A joint model can consider original spelling and the other fields, but the local reward component cannot generate such a correction."),
        ("为什么纠错reward不是统一exact match或统一编辑相似度？", "需要改时保留最高1分给正确串，其余最多0.3分；不需要改时任何改写都0分。这能区分部分修正与过度修正。", "教学例：red shose的近似修正可得低额分；本来正确的red shoes改成red shoe仍是0，不能因为编辑距离很小而奖励。", "Why not use exact match or edit similarity for every spelling case?", "When correction is needed, exact output earns1 and all partial outputs at most0.3. When none is needed, every rewrite earns zero. This separates partial repair from overcorrection.", "Teaching example: a partial repair of red shose can receive small credit. Rewriting the already-correct red shoes to red shoe earns zero despite a small edit distance."),
        ("OneQuery的QT reward能换成LARF的ordinal距离吗？", PAPERS["onequery"]["comparison"][0], "教学例：参考含brand和product，少一个字段时QT reward=0；不能按匹配了一半给0.5，或按等级距离衰减。", "Can QT reward be replaced by LARF's ordinal distance?", PAPERS["onequery"]["comparison"][1], "Teaching example: if the reference contains brand and product, missing either gives zero QT reward, not0.5 for matching half or an ordinal-distance score."),
        ("常数组reward的优势和无效schema如何处理？", "常数组的分子为0，加正delta后优势仍全0。本地无效schema拒绝而不是猜造原文没给的格式奖励；gold仅在scorer侧。", "教学例：8个候选reward均0.7时，不能因seed变化强行给某个候选正优势；缺QT字段的输出也不能当成QT空集合自动通过。", "How are constant groups and malformed schemas handled?", "Constant-group centered rewards are zero and remain zero with positive delta. The local interface rejects malformed schemas rather than inventing a format reward; gold stays inside the scorer.", "Teaching example: eight rewards all equal0.7 must not yield seed-dependent positive advantages. Missing QT must not silently become an empty set that passes."),
    ],
    "camar": [
        ("CAMAR为何同时保留invariant和specific？", "共享偏好可跨song/playlist/podcast迁移，但音色、节奏或叙事习惯等域残差不应被强迫共享。CAMAR只允许invariant跨域，specific留在本域。", "教学例：通勤偏好可关联歌曲与播客，歌曲音色偏好却不应直接支配播客召回。", "Why retain invariant and specific factors together?", "Shared preferences can transfer across song, playlist and podcast, while domain residuals such as timbre, rhythm or narration should not be forced into one shared factor. Only invariant factors cross domains.", "Teaching example: a commuting preference may connect songs and podcasts, but song-timbre preference should not directly control podcast recall."),
        ("缺失域补全为何不能进入shared平均？", "原文将inactive的imputed invariant绕过attention，shared只聚合active域，避免把由已知域推测的结果又当独立证据反馈回来。", "教学例：只有song行为时，补出的podcast不是新观测；把两者平均会重复计算同一来源的信息。", "Why exclude imputed inactive domains from the shared average?", "Inactive imputed invariant factors bypass attention, and shared pooling uses only active domains, preventing predictions from being fed back as independent evidence.", "Teaching example: with only song history, an imputed podcast factor is not a new observation. Averaging both would count information from one source twice."),
        ("CAMAR与LazUnirec都在解决同一种共享问题吗？", PAPERS["camar"]["comparison"][0], "教学例：某域invariant每步梯度很稳定，仍可能编码domain ID；高可靠权重不能代替GRL域分类对抗。", "Do CAMAR and LazUnirec solve the same sharing problem?", PAPERS["camar"]["comparison"][1], "Teaching example: a domain factor can have stable gradients while encoding domain identity. Reliability weights cannot replace adversarial domain classification."),
        ("GRL应反转哪些梯度，表示匹配更新谁？", "GRL仅反转classifier输入梯度，classifier参数仍正常下降；Eq5/7使PCN源和target都detach，表示匹配只更新PCN。不能反转整个recall分支。", "教学例：前向GRL(x)=x，系数0.6时输入梯度乘−0.6；线性classifier权重梯度不乘−0.6。", "Which gradients does GRL reverse, and what does representation matching update?", "GRL reverses only gradients entering the classifier input; classifier parameters still descend normally. Detached PCN source and target in Equations5/7 restrict representation matching to PCN updates. Recall gradients must not be reversed.", "Teaching example: GRL(x)=x in the forward pass. With coefficient0.6, input gradients multiply by−0.6 while linear classifier weight gradients do not."),
    ],
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n")


def main():
    import fitz
    specs, bank, overlays, proposals = {}, {}, {}, []
    for key, row in PAPERS.items():
        identity = "recommendation:"+key
        source = "https://arxiv.org/pdf/"+row["id"]+"v1"
        page = ROOT/f"docs/recommendation-components/{row['id']}-{key}/README.md"
        if page.exists():
            raise ValueError("append-once source already exists: "+key)
        assets = page.parent/"assets"; assets.mkdir(parents=True)
        pdf = ROOT/".cache/nov26-latest/root-primary"/row["pdf"]
        image = assets/"paper-figure-01.png"
        fitz.open(pdf)[3].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(row["crop"])).save(image)
        dump(assets/"provenance.json", {"schema_version": 1, "paper_url": source, "source_url": source+"#page=4", "pdf_page": 4,
             "figure": row["figure"], "caption": "Three-Stage Training Framework of OneQuery." if key=="onequery" else "The overall workflow of CAMAR, with multi-modal preference encoding and causal preference disentanglement.",
             "source_sha256": digest(pdf), "crop_pdf_points": row["crop"], "asset_sha256": digest(image), "visually_reviewed": True,
             "render_scale": 2, "scientific_content_modified": False, "copyright": "Original authors"})
        for en in (False, True):
            i = int(en)
            heads = ("Original paper summary", "Background and method", "Core formula", "Reported offline and online results", "Relationship to existing methods", "Local implementation", "Data protocol and code mapping", "Results, controls and limits", "High-cost full experiment") if en else ("原始论文总结", "背景与主要改动", "核心公式", "论文离线与线上效果", "与已有方法的关系", "本地复现", "数据协议与代码映射", "结果、负控与边界", "高成本完整实验")
            info = f"""| {'Field' if en else '字段'} | {'Value' if en else '内容'} |
| --- | --- |
| {'Paper' if en else '论文链接'} | [Fixed {row['id']}v1]({source}) |
| {'Company / first-author institution' if en else '公司 / 一作机构'} | {row['author']}; {row['affiliation']} |
| {'Original publication' if en else '首次公开日期'} | {row['published_at']}; {'discovered/reviewed' if en else '发现/审查'} {DATE}; {'verified announcement' if en else '已核公告日'} 2026-11-26 |
| {'Author code' if en else '原作者开源代码'} | {'No dedicated author repository given in fixedv1; no verified public method implementation found in this bounded intake' if en else '固定v1未给专属作者仓库；本轮未找到已核验公开方法代码，未找到/尚未发布，不把引用仓库当本文实现'} |
| {'Local adapter / key' if en else '本地adapter / key'} | `{key}`; `adapter: null`, {'standalone component' if en else '独立组件'} |
| {'Local code' if en else '本地复现代码'} | `src/auto_research/reproductions/{key}_components.py` |"""
            local_links = "[CPU](metrics/component-cpu-seeds42-44.json)"+(" · [CUDA](metrics/component-cuda-seeds42-44.json)" if row["cuda"] else "")
            content = f"""# {row['title']}

{'[简体中文](README.md)' if en else '[English](README-en.md)'}

> {'L1 mechanism diagnostic, not complete capability reproduction; full high-cost campaigns not reproduced(review DONE), no Evolve promotion.' if en else 'L1机制诊断，不是完整能力复现；高成本完整实验不复现（审查 DONE），不接Evolve晋级。'}

## {'Paper information' if en else '论文信息'}

{info}

## {heads[0]}

### {heads[1]}

{row['method'][i]}

<!-- paper-figure:start -->
### {'Key original figure' if en else '原论文关键图'}

[![{key} {row['figure']}](assets/paper-figure-01.png)]({source}#page=4)

{('Image from [the original paper]('+source+'#page=4), fixedv1 page4, with complete caption. Copyright belongs to the original authors. Visually checked, not local evidence.') if en else ('图片来自[原论文]('+source+'#page=4)固定v1第4页，完整保留图注，版权归原作者所有；已目视核对，不是本地结果。')} [Provenance/SHA256](assets/provenance.json).
<!-- paper-figure:end -->

```mermaid
flowchart LR
    A[{'Input and explicit fields' if key=='onequery' else 'Per-domain observed states'}] --> B[{'Exact/edit/set rewards' if key=='onequery' else 'Stopped PCN completion'}]
    B --> C[{'Weighted reward and group advantages' if key=='onequery' else 'Invariant and specific factors'}]
    C --> D[{'Signed ratio clipping' if key=='onequery' else 'Active-only shared attention and local gates'}]
```

### {heads[2]}

{row['formula'][i]}

### {heads[3]}

{row['reported'][i]}

### {heads[4]}

{row['comparison'][i]}

## {heads[5]}

### {heads[6]}

{row['local'][i]}

```bash
PYTHONPATH=src python -c 'from auto_research.reproductions.{key}_components import diagnostic; print(diagnostic(42))'
PYTHONPATH=src python -m pytest tests/test_nov26_industrial_components.py -q
```

### {heads[7]}

{row['controls'][i]}

{'Frozen-source three-seed artifacts, diagnostic only; the CUDA component additionally requires real A100/A30 evidence.' if en else '冻结源绑定三seed产物仅为诊断；CUDA组件另需真实A100/A30证据。'} {local_links}.

### {heads[8]}

{row['cost'][i]}
"""
            if en:
                content = "<!-- source-sha256: "+digest(page)+" -->\n\n"+content
            (page.with_name("README-en.md") if en else page).write_text(content)
        questions = [{"id": "nov26-"+level, "level": level, "question": item[0], "answer": item[1], "example": item[2], "added": DATE,
                      "source_sections": ["背景与主要改动", "核心公式", "与已有方法的关系", "结果、负控与边界"]}
                     for level, item in zip(("basics", "mechanism", "comparison", "implementation"), QA[key], strict=True)]
        units = question_units({identity: questions})
        for question, item in zip(questions, QA[key], strict=True):
            unit = f"qa/{identity}/{question['id']}"
            overlays[unit] = {"source_sha256": units[unit].source_sha256, "reviewed": True, "fields": dict(zip(("question", "answer", "example"), item[3:], strict=True))}
        bank[identity] = {"questions": questions}
        peer = "recommendation:"+row["peer"]
        peer_spec = json.loads((ROOT/f"src/auto_research/paper_specs/catalog/recommendation/{row['peer']}.json").read_text())
        comparison_q = QA[key][2]
        proposals.append({"paper": identity, "target_card": "recommendation/"+row["card"],
            "source_revisions": {identity: digest(page), peer: digest(ROOT/"docs"/peer_spec["detail_path"])},
            "comparison": {"position": row["local"][0], "tradeoff": row["comparison"][0], "sections": ["与已有方法的关系", "结果、负控与边界"]},
            "analysis": {"title": comparison_q[0], "body": row["comparison"][0], "papers": [identity, peer]},
            "question": {"id": "nov26-"+key, "question": comparison_q[0], "answer": comparison_q[1], "example": comparison_q[2], "papers": [identity, peer]},
            "update": {"date": DATE, "papers": [identity, peer], "summary": row["local"][0]},
            "english": {"comparison": {"position": row["local"][1], "tradeoff": row["comparison"][1]}, "analysis": {"title": comparison_q[3], "body": row["comparison"][1]},
                        "question": {"question": comparison_q[3], "answer": comparison_q[4], "example": comparison_q[5]}, "update": row["local"][1]}})
        online = ([{"product": "AliExpress multi-country search", "metric": "L2P", "lift_percent": .5,
                    "traffic": "Real A/B against existing production QU; duration/traffic fraction undisclosed; SBS relevance separately+0.8points", "source_url": source, "source_location": "Section5.6"}]
                  if key=="onequery" else [{"product": "NetEase Cloud Music "+name, "metric": metric, "lift_percent": lift,
                    "traffic": "Two-week May2026 A/B; extra CAMAR recall channel with same ranking/reranking; fraction undisclosed", "source_url": source, "source_location": "SectionV-E/TableV"}
                    for name, metric, lift in (("Song", "Play Duration", 1.), ("Playlist", "Like Rate", 3.), ("Podcast", "Play Duration", 1.6))])
        specs[identity] = {"domain": "recommendation", "key": key, "title": row["title"], "paper_url": "https://arxiv.org/abs/"+row["id"]+"v1",
            "reviewed_version_url": source, "reviewed_version": "v1", "detail_path": page.relative_to(ROOT/"docs").as_posix(), "first_author": row["author"],
            "first_author_affiliation": row["affiliation"], "browse_company": row["company"], "published": "2026-11-25", "published_at": row["published_at"],
            "announced_on": "2026-11-26", "discovered_on": DATE, "reviewed_on": DATE, "code": None, "code_status": "固定v1未给专属作者仓库；本轮未找到已核实公开方法实现", "code_license": None, "upstream_revision": None,
            "adapter": None, "topic": row["topic"], "browse_topic": row["topic"], "priority": "P0", "verified_priority_organizations": [], "intake_class": "nov25_first_publication_discovered_nov26",
            "implementation_status": "component_only", "evaluation_tier": "l1_mechanism", "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "requires_gpu_validation": row["cuda"], "gpu_validation_passed": False, "gpu_validation_artifact": "docs/gpu-validations/camar-a100-20261126-latest.json" if row["cuda"] else None,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True, "review_done": True, "review_resolution": "not_reproduced_high_cost", "automatic_retry": False, "automatic_implementation_queue": False,
            "summary": row["method"][0]+" "+row["local"][0], "local_operator": "auto_research.reproductions."+key+"_components.diagnostic",
            "local_command": "PYTHONPATH=src python -c 'from auto_research.reproductions."+key+"_components import diagnostic; print(diagnostic(42))'", "method_source_sha256": digest(pdf),
            "cost_assessment": {"source": source, "basis": row["cost"][0], "decision": "成本过高，不复现（审查 DONE）", "local_seconds_per_seed_cap": 30}, "online_ab": online}
    dump(AUDIT/"paper-proposals-root.json", {"schema_version": 1, "papers": specs})
    dump(AUDIT/"root-authored-bundle.json", {"schema_version": 1, "papers": bank, "english_question_units": overlays})
    dump(AUDIT/"deep-dive-proposals-root.json", {"schema_version": 1, "proposals": proposals})


if __name__ == "__main__":
    main()
