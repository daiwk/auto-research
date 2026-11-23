"""Reviewed AIMuon/SPOT write-ups and append-once learning proposals."""

from hashlib import sha256
import json
from pathlib import Path

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov23-latest"
CACHE = ROOT / ".cache/nov23-latest/root-primary"
DATE = "2026-11-23"

PAPERS = {
    "aimuon": {
        "id": "2611.27077", "version": "v1", "title": "Accelerating Muon with Spectral Residual Correction",
        "stamp": "2026-11-20T03:43:01Z", "author": "Zhixin Ren", "affiliation": "Tsinghua University",
        "module": "aimuon", "topic": "training-budget", "peer": "foundation-models:af-muon", "cuda": True,
        "figure": (6, "Algorithm 1", [105, 45, 510, 295]),
        "caption": "AIMuon: EMA momentum, independently transformed gradient residual, nuclear-norm weighting and Muon-matched update magnitude.",
        "code": None, "revision": None, "license": None,
        "code_cn": "固定v1和本轮作者入口未找到可核验的本篇原作者源码；文中Muon博客不是AIMuon代码发布。",
        "code_en": "No verified paper-specific author code was found in fixed v1 or the reviewed author entry; the cited Muon blog is not an AIMuon release.",
        "method_cn": "AIMuon不改普通EMA动量，而改参数子问题：先更新M，再算E=G−M，分别对M与E做谱变换，以各自核范数估计决定相对权重。把残差混进动量后只做一次变换通常不等价，因为矩阵符号映射非线性。实用Algorithm1用两次五步BF16 Newton–Schulz近似，并用内积绝对值估计核范数，不做额外SVD；最后把合成步的Frobenius范数匹配到同M的Muon，权重衰减解耦。理论收敛结论针对未归一化、精确矩阵符号版本，不自动覆盖这个BF16实用算法。",
        "method_en": "AIMuon retains ordinary EMA momentum but changes the parameter subproblem. It updates M, forms E=G−M, transforms M and E independently, and weights their directions by estimated nuclear norms. Mixing the residual before one transform is generally inequivalent because the matrix-sign map is nonlinear. Practical Algorithm1 uses two five-step BF16 Newton–Schulz approximations and absolute inner products instead of another SVD. It matches the combined Frobenius magnitude to Muon with the same M and applies decoupled weight decay. The stationarity theorem concerns the unnormalized exact matrix-sign iteration, not automatically this practical BF16 algorithm.",
        "formula": r"M=\beta M_{old}+(1-\beta)G,\quad E=G-M,\quad \widehat\nu_A=|\langle A,NS_5(A)\rangle|,\quad \widetilde O=\widehat\nu_M\left[NS_5(M)+c\frac{\widehat\nu_E}{\widehat\nu_M+\epsilon}NS_5(E)\right].",
        "extra_cn": "Eq21进一步设O=0.2√max(m,n)·||NS5(M)||F·Õ/(||Õ||F+ε)，再做Θ′=(1−ηλwd)Θ−ηO。C.2的Eq20/21稳定项为1e−12，不是AdamW的1e−8。AppendixC规定输入转BF16、行数大于列数时转置，按max(Frobenius范数,1e−7)归一化，五次使用系数(3.4445,−4.7750,2.0315)。本地不加入bias correction或Nesterov，不宣称一维参数、embedding、分布式优化器已实现。",
        "extra_en": "Equation21 sets O=0.2√max(m,n)·||NS5(M)||F·Õ/(||Õ||F+ε), followed by Θ′=(1−ηλwd)Θ−ηO. C.2 specifies epsilon1e−12 in Eq20/21, not AdamW's1e−8. AppendixC casts to BF16, transposes tall inputs, normalizes by max(Frobenius norm,1e−7), and applies coefficients (3.4445,−4.7750,2.0315) five times. The component adds neither bias correction nor Nesterov and does not implement vector parameters, embedding treatment or a distributed optimizer.",
        "result_cn": "Table1的GPT-2-small三seed最终validation loss为Muon3.1980±0.0005、AIMuon3.1945±0.0005；Table2达到Muon最终loss的步数减少8.98%/10.05%/6.49%（三个模型）。这不是wall-clock等比例加速：作者报告GPT-2-medium同token预算训练4.50h对4.26h，Qwen3-0.6B14.96h对14.36h，均不含验证。未报告生产线上A/B，以上不是本地结果。",
        "result_en": "Table1 reports GPT-2-small three-seed final validation loss of3.1980±0.0005 for Muon and3.1945±0.0005 for AIMuon. Table2 reports8.98%/10.05%/6.49% fewer steps to Muon's final loss across three models. These are not equal wall-clock speedups: matched-token GPT-2-medium runs take4.50h versus4.26h, and Qwen3-0.6B14.96h versus14.36h, excluding validation. No production online A/B is reported; these are not local measurements.",
        "scope_cn": "仅矩阵参数的函数式Algorithm1、NS5和20步合成二次矩阵损失autograd诊断。检查相同动量的步长匹配、c=0退回Muon、独立变换不等于预混合、零矩阵、转置和BF16溢出拒绝；没有语言模型预训练、FineWeb读取、超参数搜索或Evolve算子。CPU与真实A100三seed的指标是数值/机制诊断，不是模型能力比较。",
        "scope_en": "Only the functional matrix-parameter Algorithm1, NS5, and a20-step synthetic quadratic-matrix autograd diagnostic are implemented. Controls cover same-momentum magnitude matching, c=0 recovery of Muon, separate-versus-premixed transforms, zeros, transposition and BF16 overflow rejection. There is no LM pretraining, FineWeb reader, hyperparameter search or Evolve operator. CPU and real-A100 three-seed evidence is numerical/mechanism diagnosis, not a model capability comparison.",
        "cost_cn": "Section4.1使用8×H100，从零训练GPT-2-small/medium和Qwen3-0.6B，约2.48B/6.9B/12B tokens，另有各优化器独立调参和多seed/消融。Section4.3训练用时是作者8卡测量，不能当作单A100估计。完整矩阵直接成本过高不复现；本地只用8×12合成矩阵，每seed预算30秒，无模型/数据下载和API。",
        "cost_en": "Section4.1 trains GPT-2-small/medium and Qwen3-0.6B from scratch on8 H100s and about2.48B/6.9B/12B tokens, with independent optimizer tuning, seeds and ablations. Section4.3 timings are the authors' eight-device measurements, not single-A100 estimates. The full matrix is high-cost and not reproduced. Only8-by-12 synthetic matrices run locally under a30-second-per-seed component budget, with no model/data downloads or APIs.",
        "compare_cn": "AF-Muon处理tied embedding上稀疏输入与稠密输出的冲突，以support/cap词表方向和一维RMS去掉AdamW；AIMuon改变的是矩阵参数的谱残差方向，不解决共享词表support问题，也不能自动替代AF-Muon全参数分工。相同步长只排除纯尺度效应，不保证新方向一定更优。",
        "compare_en": "AF-Muon addresses sparse-input/dense-output conflicts in tied embeddings through vocabulary support/cap directions and vector RMS updates without AdamW. AIMuon instead changes matrix spectral residual directions; it does not solve vocabulary support or replace AF-Muon's parameter partition. Matching magnitude removes a pure-scale explanation but does not guarantee a better direction.",
        "questions": [
            ("AIMuon改的是动量还是参数步？", "保留普通EMA，改参数子问题得到独立残差谱方向。不是Nesterov动量，也不是把当前梯度直接加到Muon结果。", "教学例：β=0.9、旧M=0时，新M=0.1G，E=0.9G；必须先更新M再算E。", "Does AIMuon change momentum or the parameter step?", "It retains ordinary EMA and derives an independent spectral residual direction from the parameter subproblem, rather than Nesterov momentum or a raw-gradient add-on.", "Teaching example: with β=.9 and old M=0, new M=.1G and E=.9G; update M before forming E."),
            ("为何分别变换残差，再做步长匹配？", "矩阵符号变换非线性，分别变换后加权一般不等于先混合再变换。RMS匹配去掉共同尺度，却保留核范数比带来的方向变化。", "教学例：两个不同奇异向量方向的矩阵相加后，其polar方向不等于两个polar方向的和；归一到同范数也不会使它们相同。", "Why transform the residual separately before magnitude matching?", "Matrix-sign is nonlinear, so weighted separately transformed signals generally differ from a transformed mixture. RMS matching removes common scale, not relative nuclear-norm-induced directional changes.", "Teaching example: matrices with different singular-vector directions generally have a polar sum different from the polar of their sum, even after equal-norm rescaling."),
            ("AIMuon能替代AF-Muon的tied embedding处理吗？", "不能直接推断。AF-Muon管词表support/cap及向量更新；AIMuon只定义矩阵谱残差。组合需要明确参数分工和真实验证。", "教学例：一个训练step中只出现两个词，词表输入梯度稀疏；矩阵残差修正不会自动给未出现词定义support约束。", "Does AIMuon replace AF-Muon's tied-embedding treatment?", "Not by itself. AF-Muon handles vocabulary support/caps and vector updates; AIMuon defines matrix spectral residuals. Combining them needs an explicit parameter partition and real verification.", "Teaching example: if a step contains two vocabulary entries, a spectral residual does not automatically define support constraints for unseen entries."),
            ("步数减少是否等于训练时间减少？", "不是。每step多一次NS5有成本；论文同token预算的AIMuon训练时间反而更长。微型损失下降更不能证明LLM预训练收益。", "教学例：少10%步骤但每步贵20%，总时间是0.9×1.2=1.08倍；这是教学算例，不是论文实测。", "Do fewer steps imply less training time?", "No. The extra NS5 costs work per step; matched-token AIMuon runs take longer in the paper. A decreasing tiny quadratic loss also does not establish LM pretraining gains.", "Teaching example:10% fewer steps at20% greater per-step cost means1.08 times the time; this is illustrative arithmetic, not a paper measurement."),
        ],
    },
    "spot-bench": {
        "id": "2604.24317", "version": "v2", "title": "Don't Pause! Every prediction matters in a streaming video",
        "stamp": "2026-04-27T11:07:03Z", "author": "Dibyadip Chatterjee", "affiliation": "National University of Singapore",
        "module": "spot_bench", "topic": "evaluation-and-evidence", "peer": "foundation-models:e-rwsc", "cuda": False,
        "figure": (6, "Figure 3", [104, 75, 510, 178]),
        "caption": "Streaming evaluation protocol: matched slots, false positives, false negatives and the asymmetric early/late timeliness kernel.",
        "code": "https://github.com/dibschat/SPOT-Bench", "revision": "12ab7f6c215d22c651bbbfde33c09ea5b6a4f101", "license": "MIT",
        "code_cn": "是：[原作者SPOT-Bench](https://github.com/dibschat/SPOT-Bench)，固定12ab7f6c215d22c651bbbfde33c09ea5b6a4f101，MIT；本地独立实现并核对evals/metrics.py，不下载视频或执行上游模型。",
        "code_en": "Yes: [author repository](https://github.com/dibschat/SPOT-Bench), pinned12ab7f6c215d22c651bbbfde33c09ea5b6a4f101, MIT. The local independent scorer was checked against evals/metrics.py without downloading videos or executing upstream models.",
        "method_cn": "SPOT-Bench针对持续视频流：每个输出都会影响分数，不只在暂停询问时读一个答案。人工可接受时间窗是gold slot，窗内timeliness为1，窗外采用早侧较宽、晚侧较窄的Gaussian尾。语义正确且时间有效的响应按时间顺序被开放slot吸收，每slot最多K次并只保留最好timeliness；过量或不匹配输出为FP，空slot为FN。T-F1以加权TP衡量及时性、覆盖和过度回应。Ctrl-SPOT则是另一个完整流式控制器，组合持久query状态、长短期KV、检索与dead-time总结；本地只做评测器，不冒充控制器。",
        "method_en": "SPOT-Bench evaluates continuous video output: every response affects the score rather than only answers at paused queries. Human-acceptable windows define gold slots. Timeliness is1 inside and has wider early and narrower late Gaussian tails outside. Temporally valid, semantically correct responses arrive chronologically; each open slot absorbs up to K and keeps its best timeliness. Excess or unmatched outputs are false positives and empty slots false negatives. Weighted T-F1 combines timing, coverage and over-response. Ctrl-SPOT is a separate full streaming controller combining persistent query state, long/short KV, retrieval and dead-time summaries; the local work is a scorer, not that controller.",
        "formula": r"P=\frac{xTP}{TP+FP},\quad R=\frac{xTP}{TP+FN},\quad T\!F1=\frac{2PR}{P+R},\qquad xTP=\sum_{j:C_j>0}\max_{i\,matched\,j}\mathcal T(t_i;s_j,e_j).",
        "extra_cn": "固定v2 Algorithm1及固定作者源码均没有匹配后break：同一预测可以吸收进多个合格开放slot，TP按非空slot数而非全部预测数计。本地忠实该明确算法，不悄悄改成正文另一处的closest-single-slot口述。K默认5，threshold显式提供；阈值0仍要求T>0。semantics[slot][prediction]由调用者提供，是离线评测输入，不给被评估policy。没有GPT judge、语义模型或视频输入。",
        "extra_en": "Fixed-v2 Algorithm1 and pinned author code do not break after a match: one prediction may fill multiple eligible open slots. TP counts occupied slots, not all absorbed responses. The component follows that explicit algorithm instead of silently substituting the prose's closest-single-slot description. K defaults to5; a threshold is explicit and zero still requires T>0. Caller-supplied semantics[slot][prediction] is offline evaluator input, never exposed to an evaluated policy. No GPT judge, semantic model or video input is implemented.",
        "result_cn": "固定v2 Table5在940视频/5093 slots的任务库上报告，Qwen2.5-VL单帧baseline macro T-F1@5为3.9%，Ctrl-SPOT+Qwen2.5-VL为10.2%，+InternVL3.5为11.7%；这些是完整流式模型的论文结果，不是本地计分器产生的能力分数。Table7单H100的latency0.51s也是作者特定设置。未报告生产线上A/B。",
        "result_en": "Fixed-v2 Table5 reports macro T-F1@5 of3.9% for single-frame Qwen2.5-VL,10.2% for Ctrl-SPOT with that backbone, and11.7% with InternVL3.5 on a940-video/5,093-slot suite. These are full streaming-model paper results, not capability scores from the local scorer. Table7's0.51s single-H100 latency is also the authors' setting. No production online A/B is reported.",
        "scope_cn": "纯CPU、stdlib的非对称timeliness、按原时间索引语义矩阵、开放slot逐时吸收与K关闭、加权P/R/F1。合成trace负控包括错误语义、空输出、7次重复超过K=5、多slot重叠和早晚惩罚；完美合成trace得1只是定义检查，不是任何Agent能力。无Ctrl-SPOT的持久query/CPU-GPU KV/检索/总结，无视频、LLM或付费judge调用，不接Evolve晋级。",
        "scope_en": "Pure-CPU standard-library asymmetric timeliness, semantic matrices indexed by original predictions, chronological open-slot absorption and K-closing, and weighted precision/recall/F1. Synthetic controls cover wrong semantics, no outputs, seven repeats exceeding K=5, overlapping slots and asymmetric penalties. A perfect synthetic trace scoring1 checks a definition, not agent capability. Persistent queries, CPU/GPU KV, retrieval and summaries of Ctrl-SPOT are absent, as are video, LLM and paid-judge calls or Evolve promotion.",
        "cost_cn": "完整基准940视频、5093 slots，多个3B–9B模型逐秒流式推理，另含7B/8B控制器和语义judge评测。即使单H100单点可运行，完整视频×模型×任务矩阵与服务集成不符合日常单A100/A30低成本预算，直接不复现；不是先下载视频再证明贵。仅计分组件每seed预算30秒、0模型/数据下载、0API。",
        "cost_en": "The full suite has940 videos and5,093 slots with per-second streaming over multiple3B–9B models,7B/8B controllers and semantic judging. Even if one H100 runs a single configuration, the complete video/model/task matrix and serving integration exceed the routine single-A100/A30 component budget. They are not reproduced, without downloading videos merely to demonstrate cost. Only the scorer has a30-second-per-seed budget and zero model/data downloads or APIs.",
        "compare_cn": "e-RWSC依据固定政策iid答案流，检验的是多数占优而非答案真实正确；SPOT的slot则用评测gold时间和显式语义匹配计及时性，不提供在线显著性证书。两者都可在输入完美时给出漂亮数值，但一个是采样分布假设下的停止证据，一个是给定trace的离线计分，不能混作模型能力。",
        "compare_en": "e-RWSC assumes iid responses from a fixed policy and certifies majority dominance rather than truth. SPOT slots use gold evaluation times and explicit semantic matches to score timeliness, without an online significance certificate. Both can produce attractive values on ideal inputs, but one is stopping evidence under sampling assumptions and the other offline scoring of supplied traces; neither may be conflated with model capability.",
        "questions": [
            ("为何暂停后答对不等于流式表现好？", "暂停协议不测空闲时间乱答、重复回应或延迟。SPOT让全程每次输出影响及时性与FP/FN。", "教学例：事件发生时说对一次，但每秒又重复十次；暂停准确率仍可满分，T-F1会惩罚K预算外重复。", "Why does correctness after pausing not establish streaming quality?", "Pause protocols omit dead-time spam, repeated replies and delay. SPOT accounts for every response through timing and FP/FN.", "Teaching example: one correct event reply followed by ten repeats can keep paused accuracy perfect while reducing T-F1 beyond the occupancy budget."),
            ("K=5代表选全流最好的五个答案吗？", "不是。每slot依时间先后吸收前5个有效语义匹配，再关闭并只保留其中最好时间分；之后不能用未来答案追补。", "教学例：K=1时略早的首个正确响应已关闭slot，后来完美定时响应会成为FP；K=2则能改善该slot的最佳分。", "Does K=5 choose the best five answers over the entire stream?", "No. Each slot chronologically absorbs its first five valid semantic matches, closes, and retains their best timing credit. Later answers cannot replace them.", "Teaching example: at K=1 an early correct response closes a slot and a later perfectly timed response is an FP; K=2 can improve the slot's best credit."),
            ("T-F1=1是否像e-RWSC证书一样有统计保证？", "不是。T-F1只是给定trace/标注/语义匹配的离线分数。e-RWSC也只在固定政策iid假设下证明多数占优，不证明真实正确。", "教学例：手工给一个正确时刻和True语义标签就可得1；这没有执行任何视觉模型，也不是Agent能力。", "Does T-F1=1 carry an e-RWSC-like statistical guarantee?", "No. T-F1 is offline scoring of supplied traces, annotations and semantic matches. e-RWSC itself certifies only majority dominance under fixed-policy iid assumptions, not truth.", "Teaching example: a hand-authored timestamp and True semantic label can score1 without running a vision model or demonstrating agent capability."),
            ("同一响应能否匹配多个slot，评测gold能给policy吗？", "本地按固定v2 Algorithm1及作者代码允许多个开放slot吸收同一响应，不用口述closest规则替换。gold与semantic矩阵只给离线scorer，不能回传被评估policy。", "教学例：两个重叠slot都语义匹配时，该响应可令TP slots为2；这也说明slot数不能误当响应数。", "Can one response fill multiple slots, and may the policy see evaluation gold?", "The local scorer follows fixed-v2 Algorithm1 and author code, allowing multiple open slots rather than substituting prose's closest-slot rule. Gold and semantic matrices remain evaluator-only, not policy feedback.", "Teaching example: two overlapping semantically matching slots may yield two TP slots from one response, showing why slot counts differ from response counts."),
        ],
    },
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+"\n")


def main():
    import fitz

    bundle, english, proposals, specs = {}, {}, [], {}
    for key, c in PAPERS.items():
        identity = "foundation-models:"+key
        page = ROOT/"docs/foundation-models"/(c["id"]+"-"+key)/"README.md"
        assets = page.parent/"assets"
        assets.mkdir(parents=True, exist_ok=True)
        pdf = CACHE/(c["id"]+c["version"]+".pdf")
        number, label, crop = c["figure"]
        image = assets/"paper-figure-01.png"
        fitz.open(pdf)[number-1].get_pixmap(matrix=fitz.Matrix(2,2), clip=fitz.Rect(crop)).save(image)
        source = f"https://arxiv.org/html/{c['id']}{c['version']}"
        figure_url = f"https://arxiv.org/pdf/{c['id']}{c['version']}#page={number}"
        dump(assets/"provenance.json", {"schema_version":1,"paper_url":source,"source_url":figure_url,
            "source_sha256":digest(pdf),"pdf_page":number,"figure":label,"caption":c["caption"],
            "crop_pdf_points":crop,"render_scale":2,"asset_sha256":digest(image),"visually_reviewed":True,
            "scientific_content_modified":False,"copyright":"Original authors; attributed original screenshot."})
        command = f"PYTHONPATH=src python -c 'from auto_research.foundation_models.{c['module']} import diagnostic; print(diagnostic(42))'"
        gpu_cn = "CUDA路径必须有真实A100/A30回执；本轮只验证小矩阵，不下载模型。" if c["cuda"] else "CPU-only，显式拒绝CUDA；没有宣称GPU模型能力。"
        gpu_en = "The CUDA path requires a real A100/A30 receipt; this batch validates tiny matrices without model downloads." if c["cuda"] else "CPU only, explicitly rejecting CUDA; no GPU model capability is claimed."
        release = "11月20日首发，本轮11月23日新捕获选题" if key=="aimuon" else "4月27日首发；本轮Google目录历史补录，核对11月5日v2，不把发现日当首发"
        cn = f"""# {c['title']}

[English](README-en.md)

> **L1机制/计分组件，diagnostic only，不是完整论文能力复现。** 高成本完整实验不复现（审查 DONE），不接Evolve晋级。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [arXiv:{c['id']}{c['version']}]({source}) |
| 公司 / 作者机构 | 一作 **{c['author']}**，**{c['affiliation']}**；{'合作者Yale Song署名Google Inc.，不把一作归为Google' if key=='spot-bench' else '按固定v1首页署名'} |
| 首次公开日期 | **{c['stamp']}**；{release} |
| 原作者开源代码 | {c['code_cn']} |
| 本地 adapter / key | `{key}`；adapter为null，独立组件 |
| 本地复现代码 | `src/auto_research/foundation_models/{c['module']}.py` |

## 原始论文总结

### 背景与主要改动

{c['method_cn']}

<!-- paper-figure:start -->
### 原论文关键图

[![原论文 {label}](assets/paper-figure-01.png)]({figure_url})

固定{c['version']}第{number}页{label}完整截图和图注，版权归原作者；已视觉核对，未改科学内容。[来源]({figure_url}) · [裁剪/指纹](assets/provenance.json)。这是论文方法图，不是本地结果。
<!-- paper-figure:end -->

```mermaid
flowchart LR
  A["显式输入"] --> B["{'EMA与独立谱残差' if c['cuda'] else '时间与语义匹配'}"]
  B --> C["{'同Muon步长归一' if c['cuda'] else 'K占用和加权TP'}"]
  C --> D["{'矩阵参数步' if c['cuda'] else '离线T-F1'}"]
```

### 核心公式

$$
{c['formula']}
$$

{c['extra_cn']}

### 论文离线与线上效果

{c['result_cn']}

### 与已有方法的关系

{c['compare_cn']}

## 本地复现

### 数据协议与代码映射

{c['scope_cn']}

```bash
{command}
PYTHONPATH=src python -m pytest -q tests/test_nov23_{c['module']}.py
```

### 结果、负控与边界

三seed CPU产物见[机制诊断](metrics/component-cpu-seeds42-44.json)。{gpu_cn} 不读取用户会话或私有数据；合成数值不是模型能力，不能因三个seed就进入正式排名。

### 高成本完整实验

{c['cost_cn']}

**成本过高，不复现（审查 DONE）**；保留有价值方法和边界，不自动重试，不阻塞审查水位。
"""
        page.write_text(cn)
        en = f"""# {c['title']}

<!-- source-sha256: {digest(page)} -->

[简体中文](README.md)

> **L1 mechanism/scoring component, diagnostic only, not a full capability reproduction.** High-cost full experiments are not reproduced (review DONE), with no Evolve promotion.

## Paper information

| Field | Value |
| --- | --- |
| Paper | [Fixed {c['version']}]({source}) |
| First author / affiliation | {c['author']}; {c['affiliation']}. {'Yale Song is affiliated with Google Inc.; the first author is not relabeled Google.' if key=='spot-bench' else 'Verified fixed-v1 byline.'} |
| Original publication | {c['stamp']}; {'newly captured November20 first release, reviewed November23' if key=='aimuon' else 'historical April27 backfill from Google’s directory, reviewing November5 v2; discovery is not publication'} |
| Original source code | {c['code_en']} |
| Local adapter / key | `{key}`; null adapter, independent component |
| Local code | `src/auto_research/foundation_models/{c['module']}.py` |

## Original paper

### Background and method

{c['method_en']}

### Key original figure

[![Original {label}](assets/paper-figure-01.png)]({figure_url})

Complete {label} and caption from fixed-{c['version']} page{number}, visually checked without scientific modification. Copyright belongs to the authors. [Source]({figure_url}) · [crop and fingerprint](assets/provenance.json). This is a paper figure, not local evidence.

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
PYTHONPATH=src python -m pytest -q tests/test_nov23_{c['module']}.py
```

### Results, controls and limits

The three-seed CPU artifact is [mechanism diagnostics](metrics/component-cpu-seeds42-44.json). {gpu_en} No user conversations or private data are read. Synthetic values are not model capability, and three seeds do not qualify them for formal ranking.

### High-cost full experiment

{c['cost_en']}

**High cost: not reproduced (review DONE).** Keep the method and its limits without automatic retries or a blocked review watermark.
"""
        page.with_name("README-en.md").write_text(en)
        rows=[]
        for level,q in zip(("basics","mechanism","comparison","implementation"),c["questions"],strict=True):
            rows.append({"id":"nov23-"+level,"level":level,"question":q[0],"answer":q[1],"example":q[2],"added":DATE,
                         "source_sections":["背景与主要改动","核心公式","与已有方法的关系","结果、负控与边界"]})
        bundle[identity]={"questions":rows}
        units=question_units({identity:rows})
        for row,q in zip(rows,c["questions"],strict=True):
            uid=f"qa/{identity}/{row['id']}"
            english[uid]={"source_sha256":units[uid].source_sha256,"reviewed":True,"fields":{"question":q[3],"answer":q[4],"example":q[5]}}
        peer=json.loads((ROOT/"src/auto_research/paper_specs/catalog"/(c["peer"].replace(":","/")+".json")).read_text())
        q=c["questions"][2]
        proposals.append({"paper":identity,"target_card":"foundation-models/"+c["topic"],
            "source_revisions":{identity:digest(page),c["peer"]:digest(ROOT/"docs"/peer["detail_path"])},
            "comparison":{"position":c["scope_cn"],"tradeoff":c["compare_cn"],"sections":["背景与主要改动","与已有方法的关系","结果、负控与边界"]},
            "analysis":{"title":q[0],"body":c["compare_cn"],"papers":[identity,c["peer"]]},
            "question":{"id":"nov23-"+key,"question":q[0],"answer":q[1],"example":q[2],"papers":[identity,c["peer"]]},
            "update":{"date":DATE,"papers":[identity,c["peer"]],"summary":c["scope_cn"]},
            "english":{"comparison":{"position":c["scope_en"],"tradeoff":c["compare_en"]},
                       "analysis":{"title":q[3],"body":c["compare_en"]},"question":{"question":q[3],"answer":q[4],"example":q[5]},"update":c["scope_en"]}})
        specs[identity]={"domain":"foundation-models","key":key,"title":c["title"],"paper_url":f"https://arxiv.org/abs/{c['id']}{c['version']}",
            "reviewed_version_url":source,"reviewed_version":c["version"],"detail_path":page.relative_to(ROOT/"docs").as_posix(),
            "first_author":c["author"],"first_author_affiliation":c["affiliation"],"published":c["stamp"][:10],"published_at":c["stamp"],
            "code":c["code"],"code_status":c["code_cn"],"code_license":c["license"],"upstream_revision":c["revision"],
            "adapter":None,"topic":["预训练与数据" if c["cuda"] else "多模态基础模型","谱残差优化" if c["cuda"] else "流式视频评测"],
            "priority":"P1" if c["cuda"] else "P0","verified_priority_organizations":[] if c["cuda"] else ["Google"],
            "intake_class":"new_metadata_since_previous_capture" if c["cuda"] else "historical_official_directory_backfill",
            "implementation_status":"component_only","evaluation_tier":"l1_mechanism","diagnostic_only":True,"promotion_eligible":False,"evolve_integrated":False,
            "requires_gpu_validation":c["cuda"],"gpu_validation_passed":False,
            "gpu_validation_artifact":"docs/gpu-validations/aimuon-a100-20261123-latest.json" if c["cuda"] else None,
            "full_experiment_status":"not_reproduced_high_cost","full_experiment_review_done":True,"review_done":True,
            "review_resolution":"not_reproduced_high_cost","automatic_retry":False,"automatic_implementation_queue":False,
            "cost_assessment":{"source":source,"basis":c["cost_cn"],"available_resource":"one A100 or A30, or Mac","decision":"High-cost full campaign not reproduced; review DONE","local_seconds_per_seed_cap":30},
            "summary":c["method_cn"]+" "+c["scope_cn"],"local_operator":f"auto_research.foundation_models.{c['module']}.diagnostic","local_command":command,
            "method_source_sha256":digest(pdf)}
    dump(AUDIT/"root-authored-bundle.json",{"schema_version":1,"papers":bundle,"english_question_units":english})
    dump(AUDIT/"deep-dive-proposals-root.json",{"schema_version":1,"proposals":proposals})
    dump(AUDIT/"paper-proposals-root.json",{"schema_version":1,"papers":specs})
    print("Authored2 paper pairs,8 bilingual questions,2 topic updates; no shared banks changed.")


if __name__=="__main__":
    main()
