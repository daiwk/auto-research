"""Reviewed ELBO_TDS v2 historical-revision intake; append-once authoring."""
from hashlib import sha256
import json
from pathlib import Path

import fitz

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov27-latest"
DATE = "2026-11-27"
IDENTITY = "recommendation:elbo-tds"
DETAIL = "recommendation-components/2511.21032-elbo-tds/README.md"
PAPER = "https://arxiv.org/pdf/2511.21032v2"
TITLE = "ELBO_TDS: Temporal Distribution Shift Generalization for Industry-Scale Recommender Systems"


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main():
    page = ROOT / "docs" / DETAIL
    if page.exists():
        raise ValueError("append-once authoring: do not overwrite reviewed material")
    pdf = ROOT / ".cache/nov27-latest/root-primary/elbo-tds-v2.pdf"
    assets = page.parent / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    crop = [385, 83, 559, 202]
    with fitz.open(pdf) as document:
        document[2].get_pixmap(matrix=fitz.Matrix(4, 4), clip=fitz.Rect(crop)).save(assets / "paper-figure-01.png")
    dump(assets / "provenance.json", {"source_url": PAPER, "figure": "Figure 2(d)", "page": 3,
        "crop_pdf_points": crop, "caption": "Architecture of ELBO_TDS: latent-space projection, multi-task learning and reconstruction.",
        "source_sha256": sha256(pdf.read_bytes()).hexdigest(),
        "asset_sha256": sha256((assets / "paper-figure-01.png").read_bytes()).hexdigest(),
        "extraction": "Original PDF Figure2(d) crop, not a redraw or local result", "reviewed_on": DATE})
    method = [
        "ELBO-TDS假设短期变化围绕相对稳定的用户/商品因素发生。它不只对齐增广表示：固定单位方差的encoder后验经重参数采样，decoder保留个体特征，跨视图prior约束抑制暂态噪声；任务预测只用原始观测的确定性均值。统计特征做分桶邻域扰动，序列随机mask，类别embedding dropout，再用全局特征选择限制增广强度。",
        "ELBO-TDS assumes short-term fluctuations around relatively stable user/item factors. It does more than align augmented representations: unit-variance encoder posteriors are reparameterized, decoders retain individual features, and cross-view priors suppress transient noise. Task prediction uses deterministic means from original observations. Statistical buckets are perturbed locally, sequence inputs masked and categorical embeddings dropped, gated by global feature selection."]
    comparison = [
        "COTTI的CPC用常态/促销两视图的可微门控控制对比一致性，RW对历史距离重加权，ABA在服务logit上作促销校准。ELBO-TDS用多视图高斯prior与输入重建约束稳定因素，并把有标签任务留在原始观测上；没有ABA式上线概率修正。两者都依赖稳定语义假设，不能从对齐或重建直接推断因果可识别，也不能用不同生产A/B宣称彼此胜负。",
        "COTTI uses a differentiable CPC gate for regular/promotional-view consistency, history-distance RW weights and serving-time ABA calibration. ELBO-TDS instead constrains stable factors through a multi-view Gaussian prior and input reconstruction, leaving supervised prediction on original observations; it has no ABA-style serving probability correction. Both rely on stable-semantics assumptions. Alignment or reconstruction does not establish causal identifiability, and different production A/B experiments do not establish a head-to-head winner."]
    local = [
        "本地L1只实现Eq3–7/Algorithm1的小型双encoder/decoder与dot-product预测器、单位高斯重参数采样和slot级增广。输入为调用者给定的分桶ID或已嵌入浮点slot：不读取生产特征或学习真实稳定因素。slot选择、各slot独立mask、MSE的元素均值是显式本地配置；没有完整字段embedding/dropout分组、时序增量trainer、MMoE、私有排序链路或公开benchmark效果比较。",
        "The L1 component implements a small dual encoder/decoder with dot-product prediction, unit-Gaussian reparameterization and slot-level augmentation for Equations3–7/Algorithm1. Callers provide bucket IDs or embedded floating slots; no production features or true stable factors are read. Slot selection, independent slot masking and element-mean MSE are explicit local choices. Complete field embedding/dropout grouping, chronological incremental training, MMoE, private ranking and public benchmark comparisons are absent."]
    cost = [
        "Table1的完整Commercial-Main有280亿训练交互、9亿验证和9亿测试；KuaiRand也有530万训练交互，完整实验还比较多种baseline/任务/MLP与MMoE、J和增广/权重网格。AppendixB.5为单V100-16GB/A30-24GB，不能伪称多卡不可行；但Table9在7亿样本Commercial-Small上每batch约999–1611ms、完整多配置多seed及私有生产评测超出本轮短时预算。总GPU小时未报告，以上是配置基础的成本判断，不是本地测量。完整矩阵成本过高，不复现（审查 DONE）；不下载数据、不探跑或重试。小型组件实际成本另记运行产物。",
        "Table1 lists28B training,0.9B validation and0.9B test interactions for Commercial-Main; KuaiRand has5.3M training interactions. The full campaign also covers baselines, tasks, MLP/MMoE and augmentation/weight grids. AppendixB.5 uses a single V100-16GB/A30-24GB, so multi-GPU infeasibility must not be invented. Table9 reports roughly999–1611ms per batch on the0.7B-example Commercial-Small; the multi-configuration/multi-seed/private-production campaign exceeds this bounded intake. Total GPU-hours are not reported: this is configuration-based cost assessment, not local measurement. The complete matrix is high cost, not reproduced(review DONE), without downloads, probes or retries. Component execution cost is recorded separately."]
    cn = rf"""# ELBO-TDS：时间漂移中的变分重建与跨视图prior

[English](README-en.md)

> L1机制组件，不是完整工业复现；原始首发2025年，2026年11月25日v2带出本次补录，不是今天新发。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [ELBO-TDS](https://arxiv.org/abs/2511.21032)；[固定v2]({PAPER}) |
| 公司 / 作者机构 | 一作Yuxuan Zhu及Cong Fu：Shopee；合作机构NTU、Singapore Management University |
| 首次公开日期 | 2025-11-26 04:02:23 UTC（v1）；本轮核对v2为2026-11-25 03:39:34 UTC，11月26日replacement公告 |
| 原作者开源代码 | [ELBO4TDS](https://github.com/FuCongResearchSquad/ELBO4TDS)，本轮核验公开；固定HEAD `85358987d35e12ca6e454da2520f6c43e0c99dbb`；未核到许可证，按公式独立实现，未复制作者源码 |
| 本地adapter / 稳定键 | `elbo-tds`；adapter=null，组件函数不是全pipeline |
| 本地复现代码目录 | `src/auto_research/reproductions/elbo_tds_components.py` |

## 原始论文总结

### 背景与主要改动

{method[0]}

```mermaid
flowchart LR
  X[原始用户/商品特征] --> A[多视图增广]
  A --> E[encoder均值 + 单位高斯噪声]
  E --> R[decoder重建增广输入]
  E --> P[各视图向本样本均值收缩]
  X --> D[确定性encoder均值]
  D --> S[任务预测]
  R --> L[监督loss + alpha乘SSL]
  P --> L
  S --> L
```

<!-- paper-figure:start -->
### 原论文关键图

![原文Figure2(d)模型结构](assets/paper-figure-01.png)

图片来自[原论文]({PAPER})，版权归原作者所有；只裁出原Figure2(d)模型结构，不是本地结果。[出处与SHA256](assets/provenance.json)。
<!-- paper-figure:end -->

### 核心公式

$$
z_s^j=f_{{\phi_s}}(x_s^j)+\epsilon_s^j,\quad \epsilon_s^j\sim\mathcal N(0,I),\quad
\bar z_s=J^{{-1}}\sum_jz_s^j.
$$

$$
L=L_{{pred}}(f_{{\theta}}(\mu_u(x_u),\mu_i(x_i)),y)+\alpha\sum_{{s\in\{{u,i\}}}}
\left[\operatorname{{MSE}}(f_{{\theta_s}}(z_s^j),x_s^j)+\operatorname{{MSE}}(z_s^j,\bar z_s)\right].
$$

对应Eq3–7：prior均值按同一样本跨视图计算，不混用户；不stop-gradient。方差固定为I使熵项是常数。重建目标是各自增广输入，不偷偷替换为干净真值。预测头不加噪声、不使用增广视图；alpha=0只剩原始监督分支。

### 论文离线与线上效果

Table3在KuaiRand单任务MLP报告ERM→ELBO-TDS：AUC0.9053±0.0029→0.9112±0.0008、GAUC0.5086±0.0053→0.5191±0.0037。§4.3是两周真实流量切分A/B，对照为同一incremental-training系统，实验在粗排与精排加入ELBO-TDS；GMV/User相对+2.33%、独立人工相关性+0.2%。后者原文以百分号报告，不能擅写百分点。流量比例、分臂人数、p值和置信区间未披露。完整生产效果不能归给本地合成损失。

### 与已有方法的关系

{comparison[0]}

## 本地复现

### 数据协议与代码映射

{local[0]}

```bash
PYTHONPATH=src python -c 'from auto_research.reproductions.elbo_tds_components import diagnostic; print(diagnostic(42, device="cpu"))'
```

`augment_features`→§3.3边界；`ELBOTDSCore.objective`→Eq3–7；`predict`→原始均值的监督/推理路径。CUDA同入口，仅在真实设备证据通过后标记已验证。

### 结果、负控与边界

6对样本、3视图、3维latent、42/43/44种子只作L1数值与梯度诊断。独立两两距离恒等式核prior，alpha=0核SSL消失，改变SSL视图不能改变监督loss，全局选择概率0保持输入，检查bucket边界、所有encoder/decoder梯度有限且参数真更新。单测另核prior梯度跨视图和为0及完全mask。没有候选/超参数选择、test集读取、准确率提升或Evolve晋级；CPU/CUDA原始结果、源码证明和回执分别保留。

### 高成本完整实验

{cost[0]}
"""
    en = rf"""# ELBO-TDS: variational reconstruction and cross-view priors under temporal drift

[简体中文](README.md)

> L1 component, not a complete industrial reproduction. Originally published2025; this historical intake follows the November25,2026 v2, not a release today.

## Paper information

| Field | Value |
| --- | --- |
| Paper | [ELBO-TDS](https://arxiv.org/abs/2511.21032); [reviewed v2]({PAPER}) |
| Company / author institution | First author Yuxuan Zhu and Cong Fu:Shopee; collaborators NTU and Singapore Management University |
| Original publication | November26,2025 04:02:23UTC(v1); reviewed v2 November25,2026 03:39:34UTC, November26 replacement announcement |
| Author code | [ELBO4TDS](https://github.com/FuCongResearchSquad/ELBO4TDS), public repository confirmed; HEAD `85358987d35e12ca6e454da2520f6c43e0c99dbb`. No license verified; independent formula implementation, no copied upstream source |
| Local adapter / stable key | `elbo-tds`; adapter=null, not a full pipeline |
| Local code | `src/auto_research/reproductions/elbo_tds_components.py` |

## Original paper

### Motivation and changes

{method[1]}

### Original figure

![Original Figure2(d)](assets/paper-figure-01.png)

From the [original paper]({PAPER}), copyright belongs to the authors. Crop of Figure2(d), not a local result. [Provenance](assets/provenance.json).

### Core equations

Use Equations3–7 shown in the Chinese companion: $z_s^j=f_{{\phi_s}}(x_s^j)+\epsilon_s^j$, $\epsilon_s^j\sim\mathcal N(0,I)$, and $\bar z_s=J^{{-1}}\sum_jz_s^j$. The total objective is original-observation predictive loss plus alpha times reconstruction and cross-view-prior losses for both sides. The prior mean is across views of one sample, never users, and is not detached. Fixed unit variance makes entropy constant. Reconstruction targets each augmented input, not a hidden clean target. Prediction is deterministic and unaugmented; alpha zero leaves only supervision.

### Reported offline and online results

Table3, KuaiRand single-task MLP, ERM→ELBO-TDS:AUC0.9053±0.0029→0.9112±0.0008 and GAUC0.5086±0.0053→0.5191±0.0037. Section4.3 reports a two-week real traffic-split A/B against the same incremental-training system, adding ELBO-TDS at coarse/fine ranking: GMV/User+2.33% relative and independent human relevance+0.2%. The latter is reported with a percent sign, not established as percentage points. Traffic fraction, arm counts, p-values and confidence intervals are undisclosed. Production gains cannot be attributed to synthetic local losses.

### Relationship to existing methods

{comparison[1]}

## Local implementation

### Data and code mapping

{local[1]}

```bash
PYTHONPATH=src python -c 'from auto_research.reproductions.elbo_tds_components import diagnostic; print(diagnostic(42, device="cpu"))'
```

`augment_features` covers Section3.3 boundaries; `ELBOTDSCore.objective` covers Equations3–7; `predict` is the original-mean supervision/inference path. The CUDA entry is identical and may be admitted only after actual-device evidence.

### Controls and limits

Six pairs, three views, three latent dimensions and seeds42/43/44 provide L1 arithmetic/gradient diagnostics only. Controls independently compute the prior through pairwise-distance identity, remove SSL at alpha zero, preserve supervised loss when SSL views change, preserve inputs at zero global selection, enforce bucket bounds and verify finite gradients/real encoder/decoder updates. Tests additionally check zero cross-view gradient sum for the prior and complete masking. There is no candidate/hyperparameter selection, test access, accuracy improvement or Evolve promotion. CPU/CUDA raw results, source proof and receipts remain separate.

### Complete experiment cost

{cost[1]}
"""
    page.write_text(cn)
    page.with_name("README-en.md").write_text(f"<!-- source-sha256: {sha256(cn.encode()).hexdigest()} -->\n" + en)
    spec = {"domain": "recommendation", "key": "elbo-tds", "title": TITLE,
        "paper_url": "https://arxiv.org/abs/2511.21032v2", "reviewed_version_url": PAPER, "reviewed_version": "v2",
        "detail_path": DETAIL, "first_author": "Yuxuan Zhu", "first_author_affiliation": "Shopee",
        "browse_company": "Shopee", "published": "2025-11-26", "published_at": "2025-11-26T04:02:23Z",
        "updated_at": "2026-11-25T03:39:34Z", "announced_on": "2026-11-26", "discovered_on": DATE, "reviewed_on": DATE,
        "code": "https://github.com/FuCongResearchSquad/ELBO4TDS", "code_status": "公开作者仓库已核验，许可证未找到；按公式独立实现",
        "code_license": None, "upstream_revision": "85358987d35e12ca6e454da2520f6c43e0c99dbb", "adapter": None,
        "topic": ["训练目标与决策优化", "时间漂移与稳健增量训练"], "priority": "P1", "verified_priority_organizations": [],
        "intake_class": "historical_paper_recent_revision_intake", "implementation_status": "component_only",
        "evaluation_tier": "l1_mechanism", "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "requires_gpu_validation": True, "gpu_validation_passed": False,
        "gpu_validation_artifact": "docs/gpu-validations/elbo-tds-a100-20261127-latest.json",
        "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
        "review_done": True, "review_resolution": "not_reproduced_high_cost", "automatic_retry": False, "automatic_implementation_queue": False,
        "summary": method[0] + " " + local[0], "local_operator": "auto_research.reproductions.elbo_tds_components.diagnostic",
        "local_command": "PYTHONPATH=src python -c 'from auto_research.reproductions.elbo_tds_components import diagnostic; print(diagnostic(42))'",
        "method_source_sha256": sha256(pdf.read_bytes()).hexdigest(),
        "cost_assessment": {"source": PAPER, "basis": cost[0], "decision": "成本过高，不复现（审查 DONE）", "local_seconds_per_seed_cap": 30},
        "online_ab": [{"product": "Shopee coarse/fine ranking", "metric": "GMV/User", "lift_percent": 2.33,
            "traffic": "Two-week controlled production traffic split; same incremental baseline, fraction undisclosed",
            "source_url": PAPER, "source_location": "Section4.3 / AppendixB.2"}]}
    dump(AUDIT / "paper-proposals-root.json", {"papers": [spec]})
    qa = [
        ("basics", "ELBO-TDS要保留什么，又要消除什么？", "保留相对稳定且能预测个体行为的因素，减少短期促销等噪声；重建项避免仅对齐导致个体细节丢失。", "教学例：两人都喜欢手机，但一个看重新款、另一个看重低价；不能把二者表示压成相同。", "What should ELBO-TDS preserve and suppress?", "Preserve relatively stable predictive individual factors while suppressing transient noise. Reconstruction prevents alignment alone from discarding individual detail.", "Teaching example: both users like phones but one values novelty and the other low prices; their representations should not collapse together."),
        ("mechanism", "prior均值跨哪个维度计算，为什么熵项不训练？", "prior对同一样本的J个采样视图求均值而不是混整个batch；后验固定单位方差，熵为常数，梯度为0。", "教学例：两个用户各3个视图得到两个中心，不能把6个视图缩向同一个中心。", "Which axis defines the prior mean, and why is entropy not trained?", "Average J sampled views of the same example, not the batch. Fixed unit posterior variance makes entropy constant with zero gradient.", "Teaching example: two users with three views need two centers, not one center over all six views."),
        ("comparison", "ELBO-TDS和COTTI如何分别应对促销漂移？", comparison[0], "教学例：当所有视图只保留促销价时，重建不能凭空恢复常态偏好；COTTI的上调校准也不能纠正过预测。", "How do ELBO-TDS and COTTI address promotional drift differently?", comparison[1], "Teaching example: reconstruction cannot recover regular preferences if every view contains only promotional prices; COTTI's upward calibration also cannot correct overprediction."),
        ("implementation", "为什么不能把有标签预测也喂给增广采样表示？", "Eq6和Algorithm1在原始观测上用确定性encoder均值预测，保持训练/推理一致。SSL的采样与增广是独立分支，改变它们不应改变监督loss。", "教学例：固定用户/商品原始输入，只把SSL视图放大5倍；监督loss必须不变，重建和prior可以变。", "Why not predict labels from augmented sampled states?", "Equation6 and Algorithm1 predict using deterministic encoder means from original observations, matching inference. SSL sampling and augmentation are separate and must not alter supervised loss.", "Teaching example: keep original user/item inputs fixed and multiply SSL views by five; supervised loss must remain unchanged while reconstruction/prior may change.")]
    questions = [{"id": "nov27-" + q[0], "level": q[0], "question": q[1], "answer": q[2], "example": q[3], "added": DATE,
        "source_sections": ["背景与主要改动", "核心公式", "与已有方法的关系", "结果、负控与边界"]} for q in qa]
    units = question_units({IDENTITY: questions})
    translations = {}
    for key, unit in units.items():
        index = next(i for i, row in enumerate(questions) if key.endswith("/" + row["id"]))
        translations[key] = {"source_sha256": unit.source_sha256, "reviewed": True,
            "fields": dict(zip(("question", "answer", "example"), qa[index][4:]))}
    dump(AUDIT / "root-authored-bundle.json", {"schema_version": 1, "papers": {IDENTITY: {"questions": questions}}, "english_question_units": translations})
    peer = "recommendation:cotti"
    peer_path = ROOT / "docs/recommendation-components/2611.22597-cotti/README.md"
    question = {"id": "nov27-elbo-tds", "question": qa[2][1], "answer": comparison[0], "example": qa[2][3], "papers": [IDENTITY, peer]}
    proposal = {"paper": IDENTITY, "target_card": "recommendation/feedback-multitask-causality",
        "source_revisions": {IDENTITY: sha256(page.read_bytes()).hexdigest(), peer: sha256(peer_path.read_bytes()).hexdigest()},
        "comparison": {"position": local[0], "tradeoff": comparison[0], "sections": ["与已有方法的关系", "结果、负控与边界"]},
        "analysis": {"title": qa[2][1], "body": comparison[0], "papers": [IDENTITY, peer]}, "question": question,
        "update": {"date": DATE, "papers": [IDENTITY, peer], "summary": method[0] + " " + local[0]},
        "english": {"comparison": {"position": local[1], "tradeoff": comparison[1]},
            "analysis": {"title": qa[2][4], "body": comparison[1]},
            "question": dict(zip(("question", "answer", "example"), qa[2][4:])), "update": method[1] + " " + local[1]}}
    dump(AUDIT / "deep-dive-proposals-root.json", {"schema_version": 1, "proposals": [proposal]})
    dump(AUDIT / "root-primary-review.json", {"reviewed_on": DATE, "source": PAPER, "source_sha256": sha256(pdf.read_bytes()).hexdigest(),
        "read_scope": "full fixed-v2 text, derivations/Algorithm1, public and industrial configuration, production A/B", "code_revision": spec["upstream_revision"],
        "original_date_and_revision_distinct": True, "cost_assessment": spec["cost_assessment"],
        "industrial_rejections": [{"id": "2611.32855", "source": "https://arxiv.org/html/2611.32855v1", "decision": "not_selected_industrial_online_threshold", "reason": "SIDECAR §5 offline Amazon exact-topK/model-call experiments; no production traffic-split experiment in full methods/results. No named exception requested."}]})


if __name__ == "__main__":
    main()
