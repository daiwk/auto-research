"""Authored Weight Coding review, bilingual questions and topic proposal.

Append-once authoring input; do not rerun after integration or source review.
"""
from hashlib import sha256
import json
from pathlib import Path

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov24-latest"
PAGE = ROOT / "docs/recommendation-components/2611.29613-weight-coding/README.md"
SOURCE = "https://arxiv.org/html/2611.29613v1"
IDENTITY = "recommendation:weight-coding"
DATE = "2026-11-24"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n")


METHOD_CN = "Weight Coding把已训练权重本身变成可执行编辑对象，固定架构、特征和服务逻辑。LLM Agent先扫描单模块编辑，按独立filter日期排除方向翻转，再直接改值、搜索或重新搜索组合后的参数。编辑原语包括缩放、重置、移除分支、压缩、快照插值、概念方向平移；编辑支持大小不等于独立自由度。原论文的GPU缓存引擎只重算被影响模块及下游，搜索阶段不反传目标模型。"
METHOD_EN = "Weight Coding edits trained parameters while fixing architecture, features and serving logic. An LLM agent scans module edits, filters sign reversals on separate dates, then edits values, searches, or re-searches composed parameters. Primitives include rescaling, resets, branch removal, compression, checkpoint interpolation and concept-direction steering. Changed support is not the number of independent controls. The paper's GPU cache recomputes affected modules and downstream paths without target-model backpropagation."
SCOPE_CN = "本地CPU参考只实现Table1的缩放、显式reference重置、投影置零、插值、方向平移，以及§3.4反向配对Gaussian ES、centered rank、Adam上升和validation选步。没有compression、LLM假设生成、缓存生产引擎、TorchScript编辑、真实检索模型或线上A/B。原文未公布Adam细节和ties规则，本地显式采用(.9,.999)、epsilon=1e-8和平均并列rank；不能声称恢复私有实现。每seed20步×16对，synthetic quadratic仅查机制；不接Evolve晋级。"
SCOPE_EN = "The CPU reference implements Table1 rescaling, explicit-reference resets, zeroing a selected projection, interpolation and steering, plus Section3.4 antithetic Gaussian ES, centered ranks, ascent Adam and validation-selected steps. Compression, LLM hypothesis generation, the cached production engine, TorchScript edits, real retrieval models and online A/B are absent. Adam details and tie rules were not published; the local reference explicitly uses (.9,.999), epsilon1e-8 and average tied ranks, without claiming private-code parity. Each seed uses20 steps and16 pairs on a synthetic quadratic, with no Evolve promotion."
COMPARE_CN = "EvoPilot强调比较证据的完整性：共同base、数据、评测器、有效输出深度和唯一treatment都要匹配，再由人工审核接纳。Weight Coding则规定了可搜索对象：固定架构/服务上的权重数值和少量row scales。验证协议与搜索算子互补、不能互相替代；本地ES不等于已经完成自主研究或部署。原论文直接叠加编辑会退化、重新搜索可恢复，这不意味着任意两个本地算子组合必然有收益。"
COMPARE_EN = "EvoPilot emphasizes comparison integrity: shared base, data, evaluator, effective output depth and the sole treatment must match before human acceptance. Weight Coding specifies what to search: weights and a small set of row scales under fixed architecture/serving. Verification protocols and search operators are complementary, not substitutes. Local ES is not completed autonomous research or deployment. The paper observes degradation from direct edit stacking and recovery through re-search, without guaranteeing gains from arbitrary local combinations."
COST_CN = "全文§3.3约2000编辑配置、190000搜索候选；§4.1为私有Pinterest多日期日志、147M双塔，另含106M生成检索、1.37B ranker、50M+Pin索引。§4.7每组约1000万真实用户、约一周A/B，离线GPU成本比作者finetune低不等于本地低成本可复现。完整Agent/模型/生产实验成本过高，不复现（审查 DONE）；不下载模型/日志，不请求线上权限，不自动重试。"
COST_EN = "Section3.3 evaluates approximately2,000 edit configurations and190,000 search candidates. Section4.1 uses private Pinterest date-partitioned logs and a147M two-tower model, with a106M generative retriever,1.37B ranker and50M-plus-Pin index elsewhere. Section4.7 runs roughly10-million-user, week-long A/B groups. Lower GPU cost than the authors' fine-tuning does not make the complete campaign affordable locally. The full agent/model/production experiments are not reproduced (review DONE), with no model/log downloads, production access request or automatic retry."
QUESTIONS = [
    ("为什么改64个LayerNorm gain不等于搜索64个自由度？", "把64个gain全重置为1可能改64个数值，但没有可调参数；搜索每个gain才可能有64个自由度。支持集合大小和优化维度必须分开。", "教学例：一次reset改变64个值、自由度0；只调一个共享缩放系数可以影响百万权重、自由度仍为1。", "Why are64 changed LayerNorm gains not necessarily64 search degrees of freedom?", "Resetting64 gains to one changes64 values but introduces no tunable control. Searching every gain may introduce64 controls; support size and optimization dimension differ.", "Teaching example: a reset changes64 entries with zero controls, while one shared multiplier may affect a million weights with just one control."),
    ("ES为何用配对噪声，平分时又怎么办？", "同一噪声正负两个方向评估后，以centered rank差加权估计更新。相同分数必须采用平均并列rank，否则常数评估器也会凭枚举顺序产生伪更新。", "教学例：32个候选得分全为1时，平均rank后全为0；参数应保持不变，而不是宣称搜索有进步。", "Why use antithetic noise, and how are ties handled?", "The same perturbation is evaluated in both directions; differences of centered ranks weight the update estimate. Equal scores use average tied ranks so enumeration cannot create a spurious update under a constant evaluator.", "Teaching example: if all32 scores are one, every centered rank is zero and parameters stay unchanged rather than showing fabricated progress."),
    ("它与Evopilot的自进化有什么不同？", COMPARE_CN, "教学例：修改模型结构和训练pipeline属于代码级搜索；只调现有层的row log-scales属于固定架构的权重编辑，两者都不能用test挑最佳轮次。", "How does it differ from Evopilot's evolution?", COMPARE_EN, "Teaching example: changing an architecture/training pipeline is code search; adjusting existing row log-scales is fixed-architecture weight editing. Neither may choose iterations using test data."),
    ("本地搜索分数提升能否证明Pinterest线上收益？", "不能。合成目标检查ES、参数不变性和选步接口。生产收益来自论文真实A/B，不来自本地。search接口只接objective与validation，不接test callback；调用者必须保证数据确实隔离。", "教学例：validation始终偏好初始权重时，返回step0；即使搜索目标改善也不能据此选一个validation更差的模型。", "Does a local search improvement establish Pinterest's online lift?", "No. Synthetic objectives test ES, invariants and selection interfaces. Production lift belongs to the paper's A/B, not local execution. The search accepts objective and validation, not a test callback; callers remain responsible for data isolation.", "Teaching example: when validation always favors the initial weights, selection returns step0 even if the search objective improves."),
]


def main():
    import fitz
    if PAGE.exists():
        raise ValueError("append-once authoring: paper already exists")
    assets = PAGE.parent / "assets"
    assets.mkdir(parents=True)
    pdf = ROOT / ".cache/nov24-latest/arxiv/2611.29613v1.pdf"
    crop = [51, 246, 563, 474]
    image = assets / "paper-figure-01.png"
    fitz.open(pdf)[0].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(crop)).save(image)
    dump(assets/"provenance.json", {"schema_version":1,"source_url":"https://arxiv.org/pdf/2611.29613v1#page=1",
        "paper_url":SOURCE,"source_sha256":digest(pdf),"pdf_page":1,"figure":"Figure1",
        "caption":"Weight coding by LLM agents: editing workflow and successive retrieval-model iterations.",
        "crop_pdf_points":crop,"render_scale":2,"asset_sha256":digest(image),
        "visually_reviewed":True,"scientific_content_modified":False,"copyright":"Original authors"})
    cn = rf"""# Weight Coding：直接编辑工业推荐模型权重

[English](README-en.md)

> **L1机制组件，diagnostic only，不是完整Agent或推荐能力复现。** 完整实验成本过高，不复现（审查 DONE）；不接Evolve晋级。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [Weight Coding, arXiv2611.29613v1]({SOURCE}) |
| 公司 / 作者机构 | 一作Junpeng Hou与全体作者均署名Pinterest, Inc. |
| 首次公开日期 | **2026-11-22T17:11:38Z**；本轮发现/审查2026-11-24，公告日期未核定 |
| 原作者开源代码 | 固定v1与arXiv/作者入口未找到论文专属原作者开源仓库；不把第三方ES或模型库算作本文发布 |
| 本地 adapter / key | `weight-coding`；adapter为null，独立组件 |
| 本地复现代码 | `src/auto_research/reproductions/weight_coding.py` |

## 原始论文总结

### 背景与主要改动

{METHOD_CN}

<!-- paper-figure:start -->
### 原论文关键图

[![原论文Figure1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2611.29613v1#page=1)

图片来自[原论文](https://arxiv.org/pdf/2611.29613v1#page=1)第1页Figure1，版权归原作者所有；完整原图和图注裁剪，已视觉核对、未修改科学内容。[来源指纹](assets/provenance.json)。不是本地实验结果。
<!-- paper-figure:end -->

### 核心公式

$$
w'=(1-\lambda)w+\lambda\bar w,\quad b'=b+\alpha\frac{{\mu_F-\mu_{{\neg F}}}}{{\|\mu_F-\mu_{{\neg F}}\|}},\quad W'_{{ij}}=e^{{s_i}}W_{{ij}}.
$$

每步16对反向Gaussian扰动；值搜索按初始tensor RMS缩放、sigma=0.05；row log-scale搜索sigma=0.1。32个目标分转换centered ranks，再Adam上升。dev positives两半分别用于搜索/validation，每10步选最佳；filter日期只能排除方向翻转，held-out日期不引导迭代。本地额外评估初始/最终步，数值细节是显式参考选择，不假称作者未发布源码。

### 论文离线与线上效果

固定v1 §4.7/Table4是生产流量A/B：每组约1000万用户、约一周，save-oriented三组的该检索来源人均saves提高8.4%–10.7%，每曝光提高4.3%–5.3%。不是站点总收益：正文明确其他retrievers会被蚕食，不能将source-attributed收益直接解释为site-wide。离线双塔held-out recall@10最高+15.0个百分点（相对+24%），也不是本地合成分数。

### 与已有方法的关系

{COMPARE_CN}

## 本地复现

### 数据协议与代码映射

{SCOPE_CN}

```bash
PYTHONPATH=src python -c 'from auto_research.reproductions.weight_coding import diagnostic; print(diagnostic(42))'
PYTHONPATH=src python -m pytest -q tests/test_nov24_weight_coding.py
```

### 结果、负控与边界

[CPU三seed机制产物](metrics/component-cpu-seeds42-44.json)绑定冻结源。检查原参数不突变、identity编辑、概念方向单位范数、平分无更新和validation可保留step0。合成objective/validation共用同一函数的收敛检查不是数据泛化实验；另用冲突validation检验拒绝改善search却恶化validation的候选。无gold、无真实用户数据、无能力排名。CPU-only拒绝CUDA；没有GPU宣传路径。

### 高成本完整实验

{COST_CN}
"""
    PAGE.write_text(cn)
    en = rf"""# Weight Coding: direct edits to industrial recommender weights

<!-- source-sha256: {digest(PAGE)} -->

[简体中文](README.md)

> **L1 mechanism component, diagnostic only, not a complete agent or recommender.** High-cost full experiments are not reproduced (review DONE); no Evolve promotion.

## Paper information

| Field | Value |
| --- | --- |
| Paper | [Weight Coding, fixed2611.29613v1]({SOURCE}) |
| Company / institution | First author Junpeng Hou and all coauthors: Pinterest, Inc. |
| Original publication | 2026-11-22T17:11:38Z; discovered/reviewed November24; announcement date unverified |
| Author code | No verified paper-specific author repository found in fixedv1, arXiv or the reviewed author entry; third-party ES/model libraries are not this paper's release |
| Local adapter / key | `weight-coding`; null adapter, independent component |
| Local code | `src/auto_research/reproductions/weight_coding.py` |

## Original paper

### Background and method

{METHOD_EN}

### Key original figure

[![Original Figure1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2611.29613v1#page=1)

Original Figure1 and caption from fixedv1 page1, visually verified without scientific modification. Copyright belongs to the original authors. [Provenance](assets/provenance.json). Not local experimental output.

### Core formula

$$
w'=(1-\lambda)w+\lambda\bar w,\quad b'=b+\alpha\frac{{\mu_F-\mu_{{\neg F}}}}{{\|\mu_F-\mu_{{\neg F}}\|}},\quad W'_{{ij}}=e^{{s_i}}W_{{ij}}.
$$

Each step uses16 antithetic Gaussian pairs. Value search uses initial tensor RMS and sigma0.05; row log-scale search uses sigma0.1. The32 objective scores become centered ranks followed by ascent Adam. Disjoint dev-positive halves serve search and validation, checked every10 steps. Filter dates only reject sign reversals; held-out dates never guide iteration. The local reference also checks the initial/final step and states unspecified numerical choices rather than claiming unpublished-code parity.

### Reported offline and online results

Fixedv1 Section4.7/Table4 reports real production A/B, approximately10million users per group for about a week. Three save-oriented groups increase source-attributed saves per user by8.4%–10.7% and saves per impression by4.3%–5.3%. These are not site-wide lifts: the text explicitly notes cannibalization of other retrievers. Offline held-out two-tower recall@10 improves by up to15.0 percentage points (+24% relative), not a local synthetic result.

### Relationship to existing methods

{COMPARE_EN}

## Local implementation

### Data protocol and code mapping

{SCOPE_EN}

```bash
PYTHONPATH=src python -c 'from auto_research.reproductions.weight_coding import diagnostic; print(diagnostic(42))'
PYTHONPATH=src python -m pytest -q tests/test_nov24_weight_coding.py
```

### Results, controls and limits

[CPU three-seed mechanism artifact](metrics/component-cpu-seeds42-44.json) is bound to frozen source. Controls check immutable inputs, identity edits, a unit concept direction, no update on tied scores, and validation retaining step0. Reusing one synthetic function for objective/validation tests convergence, not data generalization; a separate conflicting validation checks rejection of search-only gains. There are no gold answers, real user data or capability rankings. This CPU-only path rejects CUDA and advertises no GPU path.

### High-cost full experiment

{COST_EN}
"""
    PAGE.with_name("README-en.md").write_text(en)
    questions = [{"id":"nov24-"+level,"level":level,"question":q[0],"answer":q[1],"example":q[2],
        "added":DATE,"source_sections":["背景与主要改动","核心公式","与已有方法的关系","结果、负控与边界"]}
        for level,q in zip(("basics","mechanism","comparison","implementation"),QUESTIONS,strict=True)]
    units=question_units({IDENTITY:questions})
    english={f"qa/{IDENTITY}/{r['id']}":{"source_sha256":units[f"qa/{IDENTITY}/{r['id']}"].source_sha256,"reviewed":True,
        "fields":{"question":q[3],"answer":q[4],"example":q[5]}} for r,q in zip(questions,QUESTIONS,strict=True)}
    peer="recommendation:evopilot"
    peer_spec=json.loads((ROOT/"src/auto_research/paper_specs/catalog/recommendation/evopilot.json").read_text())
    peer_doc=ROOT/"docs"/peer_spec["detail_path"]
    q=QUESTIONS[2]
    proposal={"paper":IDENTITY,"target_card":"recommendation/research-serving-loop",
        "source_revisions":{IDENTITY:digest(PAGE),peer:digest(peer_doc)},
        "comparison":{"position":SCOPE_CN,"tradeoff":COMPARE_CN,"sections":["与已有方法的关系","结果、负控与边界"]},
        "analysis":{"title":q[0],"body":COMPARE_CN,"papers":[IDENTITY,peer]},
        "question":{"id":"nov24-weight-coding","question":q[0],"answer":q[1],"example":q[2],"papers":[IDENTITY,peer]},
        "update":{"date":DATE,"papers":[IDENTITY,peer],"summary":SCOPE_CN},
        "english":{"comparison":{"position":SCOPE_EN,"tradeoff":COMPARE_EN},"analysis":{"title":q[3],"body":COMPARE_EN},
        "question":{"question":q[3],"answer":q[4],"example":q[5]},"update":SCOPE_EN}}
    spec={"domain":"recommendation","key":"weight-coding","title":"Weight Coding: Evolving Web-Scale Recommenders through Direct Weight Edits with LLM Agents",
        "paper_url":"https://arxiv.org/abs/2611.29613v1","reviewed_version_url":SOURCE,"reviewed_version":"v1",
        "detail_path":PAGE.relative_to(ROOT/"docs").as_posix(),"published":"2026-11-22","published_at":"2026-11-22T17:11:38Z",
        "announced_on":None,"discovered_on":DATE,"reviewed_on":DATE,"first_author":"Junpeng Hou","first_author_affiliation":"Pinterest",
        "browse_company":"Pinterest","topic":["研究与服务闭环","直接权重编辑"],"browse_topic":["大模型能力与推荐融合","研究Agent与自动实验"],
        "code":None,"code_status":"固定v1及本轮官方入口未找到论文专属原作者源码仓库","code_license":None,"upstream_revision":None,
        "adapter":None,"priority":"P0","verified_priority_organizations":[],"intake_class":"recent_overlap_first_collection",
        "implementation_status":"component_only","evaluation_tier":"l1_mechanism","diagnostic_only":True,"promotion_eligible":False,"evolve_integrated":False,
        "requires_gpu_validation":False,"gpu_validation_passed":False,"gpu_validation_artifact":None,
        "full_experiment_status":"not_reproduced_high_cost","full_experiment_review_done":True,"review_done":True,
        "review_resolution":"not_reproduced_high_cost","automatic_retry":False,"automatic_implementation_queue":False,
        "summary":METHOD_CN+" "+SCOPE_CN,"local_operator":"auto_research.reproductions.weight_coding.diagnostic",
        "local_command":"PYTHONPATH=src python -c 'from auto_research.reproductions.weight_coding import diagnostic; print(diagnostic(42))'",
        "method_source_sha256":digest(pdf),"cost_assessment":{"source":SOURCE,"basis":COST_CN,"decision":"成本过高，不复现（审查 DONE）","local_seconds_per_seed_cap":30},
        "online_ab":[{"product":"Pinterest Image Search edited retrieval source","metric":"saves per user","lift_percent":10.7,
        "traffic":"about10M real users per group, about one week; source-attributed, not site-wide",
        "source_url":SOURCE,"source_location":"Section4.7/Table4; save-oriented arms+8.4% to+10.7%; other retrievers can be cannibalized"}]}
    dump(AUDIT/"paper-proposals-root.json",{"schema_version":1,"papers":{IDENTITY:spec}})
    dump(AUDIT/"root-authored-bundle.json",{"schema_version":1,"papers":{IDENTITY:{"questions":questions}},"english_question_units":english})
    dump(AUDIT/"deep-dive-proposals-root.json",{"schema_version":1,"proposals":[proposal]})


if __name__ == "__main__":
    main()
