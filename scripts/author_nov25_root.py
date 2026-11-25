"""Append-once authored LazUnirec review and bilingual learning proposals."""
from hashlib import sha256
import json
from pathlib import Path

from english_learning_sources import question_units

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"docs/research-audits/nov25-latest"
PAGE=ROOT/"docs/recommendation-components/2611.32590-lazunirec/README.md"
SOURCE="https://arxiv.org/pdf/2611.32590v1"
IDENTITY="recommendation:lazunirec"
DATE="2026-11-25"
TEXT={
    "method":(
        "LazUnirec把历史、trigger、多兴趣检索query和同请求候选组织到同一Transformer，但不要求召回与排序完全共用全部参数。召回/排序各有Q/K/V低秩残差与private FFN expert，另由条件router选择top-2 shared experts。按scenario/task观察共享参数的归一化梯度历史，以EMA方向方差估计可靠性，停止梯度后重加权任务损失；排序还向召回做请求内候选分布蒸馏。",
        "LazUnirec organizes history, trigger, multi-interest retrieval queries and same-request candidates in one Transformer without forcing retrieval and ranking to share every parameter. Each task has private Q/K/V low-rank residuals and a private FFN expert, alongside top-two condition-routed shared experts. Scenario/task-specific histories of normalized shared-parameter gradients estimate directional reliability using EMA variance. Detached weights scale task losses, and ranking distills a request-local candidate distribution into retrieval."),
    "formula":(
        "Eq7对history/trigger只用共享投影，对两任务另加BτAτ残差；Eq10/11在选中的共享expert内重新softmax，再直接加private输出，而不是把private expert混入同一softmax。Eq12先将EMA二阶矩减一阶矩平方并截断到非负，e=min(emax,(variance+epsilon)^−1/2)；可靠性为r=Mean(e)/(1+Mean(e))，batch内omega=r/Mean(r)。§4.1.4在该归一后截到[0.8,1.2]，不再二次归一，因此最终权重均值未必为1。",
        "Equation7 uses only the shared projection for history/trigger and adds BτAτ residuals for the two tasks. Equations10–11 re-softmax within selected shared experts, then directly add the private output rather than including it in that softmax. Equation12 clamps EMA second-minus-squared-first moment variance at zero and sets e=min(emax,(variance+epsilon)^−1/2). Reliability is r=Mean(e)/(1+Mean(e)), with omega=r/Mean(r) within a batch. Section4.1.4 clips this normalized weight to[0.8,1.2] without a second normalization; its final mean need not be one."),
    "kd":(
        "Eq15是先用兴趣概率pi乘内积、再跨兴趣max，不是先max后平均；Eq16/17对同一请求候选做softmax，教师排序CTR logits detach，最小化KL(teacher||retrieval)。本地沿用论文温度0.5/0.01与EMA decay0.99；原文没有唯一规定初始化、方向归一范数、epsilon/emax，本地显式选零初始化无bias correction、L2与1e−8/100，只是有界数值参考。",
        "Equation15 multiplies each inner product by its interest probability before max over interests, not averaging after max. Equations16–17 softmax over aligned same-request candidates, detach ranking CTR teacher logits and minimize KL(teacher||retrieval). The reference uses paper temperatures0.5/0.01 and EMA decay0.99. Initialization, direction-normalization norm and epsilon/emax are not uniquely specified: zero initialization without bias correction, L2 and1e−8/100 are explicit bounded reference choices."),
    "reported":(
        "固定v1 §4.8/Table5披露：2026年10月在工业电商trigger-free/trigger-based场景，以10%流量进行一周生产A/B，同时替换原MIMA召回与LazFormer排序。前者IPV/Orders/Buyers/GMV相对提高5.25%/5.75%/4.57%/4.01%，后者为4.01%/4.64%/3.06%/3.06%。Table1 Scenario1 CTR GAUC从OneTrans-V2的0.6695到0.6722。以上为完整私有生产系统的作者结果，不是本地组件指标，也不能归因到单独某个loss。",
        "Fixedv1 Section4.8/Table5 reports a one-week,10%-traffic production A/B in October2026 over trigger-free/trigger-based e-commerce scenarios, replacing both MIMA retrieval and LazFormer ranking. Relative IPV/orders/buyers/GMV changes are5.25%/5.75%/4.57%/4.01% for the former and4.01%/4.64%/3.06%/3.06% for the latter. Table1 Scenario1 CTR GAUC changes from OneTrans-V2's0.6695 to0.6722. These are author results for a complete private production system, not local component metrics or causal attribution to one loss."),
    "comparison":(
        "OneTrans-V2用阶段隔离token共享因果用户上下文，精排向预排传递中心化logits/sigmoid信号；LazUnirec关注召回与排序的梯度冲突，用task-private LoRA/expert及方向可靠性区分更新，并向检索蒸馏请求内softmax分布。共享上下文不等于所有参数完全共用，独立任务参数也不自动保证梯度正交。旧OneTrans-V2公开MovieLens链路是concept demo，本批则只验局部算子，不能比较二者的代理能力分数。",
        "OneTrans-V2 shares causal user context through stage-isolated tokens and transfers centered-logit/sigmoid signals from fine ranking to pre-ranking. LazUnirec addresses retrieval/ranking gradient conflict with task-private LoRA/experts and directional reliability, distilling a request-local softmax distribution into retrieval. Shared context does not mean fully shared parameters, and private parameters do not guarantee orthogonal gradients. The existing MovieLens OneTrans-V2 path is a concept demo, while this batch checks only operators; their proxy capability scores are not comparable."),
    "local":(
        "执行Eq7低秩任务投影、Eq10/11 sparse shared/private输出组合、Eq12–14 EMA evidence/相对权重/停止梯度及Eq15–17请求内MaxSim/KL，并用真实autograd验证参数路径。输入router scores/expert outputs/已探测gradient与interest probabilities是显式张量，不虚构未给细节的条件router或概率头。未实现完整Transformer/RMSNorm/attention mask、embedding、场景数据管线、expert网络、MoE z-loss、训练调度与部署；因此不是完整模型、正式benchmark或Evolve算子。",
        "The component executes Equation7 task-private low-rank projection, Equations10–11 sparse shared/private output composition, Equations12–14 EMA evidence/relative weights/stop-gradient and Equations15–17 request-local MaxSim/KL, with real autograd path checks. Router scores, expert outputs, probed gradients and interest probabilities are explicit tensors; unspecified router/probability heads are not fabricated. The complete Transformer, RMSNorm, attention mask, embeddings, scenario pipeline, expert networks, MoE z-loss, training schedule and deployment are absent. This is not a complete model, formal benchmark or Evolve operator."),
    "controls":(
        "三seed均为小型合成张量与50步方向历史，不训练用户模型、不读取test或私有日志。检查history不读LoRA、task-private参数不串梯度、未选expert梯度为零、private输出直接相加、稳定方向较反复翻转方向可靠、权重和teacher断梯度、pi在max之前相乘以及请求间softmax不混合。方差小不证明方向正确；即使机制负控全过，也不证明CTR、GMV或生产吞吐提升。",
        "All three seeds use tiny synthetic tensors and50-step direction histories, without user-model training, test data or private logs. Controls cover history bypassing LoRA, task-private gradient isolation, zero unselected-expert gradients, direct private-output addition, stable-versus-alternating directional evidence, detached weights/teacher, pi multiplication before max and no cross-request softmax pooling. Low variance does not prove a correct direction; passing these controls does not establish CTR, GMV or production throughput gains."),
    "cost":(
        "§4.1使用私有25天日志训练、后一日测试，H100上训练5层/256宽/4heads/最长2048历史，每请求最多15 ranking tokens与8 retrieval queries，每层14 shared experts+每任务1 private expert，并做多基线、多场景与线上优化/一周A/B。原文未披露总样本量、GPU数量或总GPU小时，不凭dim256推算可负担。完整数据/模型/服务矩阵超本轮单A100/A30或Mac短时预算且私有输入不可得，成本过高，不复现（审查 DONE），不下载、不探跑、不自动重试。仅局部组件每seed预算30秒、0checkpoint/数据下载、0API。",
        "Section4.1 trains on25 private log days and tests on the following day, using H100s, five layers, width256, four heads, history up to2048, up to15 ranking tokens and eight retrieval queries per request, and14 shared plus one private expert per task. The campaign includes multiple baselines/scenarios, serving optimizations and week-long A/B. Total samples, GPU count and GPU-hours are undisclosed; width256 alone cannot establish affordability. The complete data/model/serving matrix exceeds this single-A100/A30-or-Mac short-run budget and private inputs are unavailable: high cost, not reproduced (review DONE), with no downloads, probes or retries. Only the local component has a30-second-per-seed cap, zero checkpoint/data downloads and zero APIs."),
}
QUESTIONS=[
    ("共享同一骨干为何还需要task-private参数？","召回与排序目标不同，共享参数可能收到冲突更新。低秩残差与private expert提供任务容量，shared专家仍传递共同知识；这不是梯度已正交的证明。","教学例：同一历史对点击召回有用、对转化排序却需不同交互；两个任务可读同一用户表示但使用不同低秩投影。","Why retain task-private parameters under a shared backbone?","Retrieval and ranking objectives can yield conflicting shared updates. Low-rank residuals and private experts add task capacity while shared experts transfer common knowledge; orthogonal gradients are not guaranteed.","Teaching example: the same history may support click retrieval while conversion ranking needs different interactions; both tasks can read one user context with distinct low-rank projections."),
    ("梯度可靠性等于梯度幅值或方向正确性吗？","都不是。对归一化方向计算历史EMA方差，小方差表示相对稳定。稳定错误方向也可有高evidence；权重还依赖同batch其他任务，不是概率置信度。","教学例：[1,0]与[100,0]有相同L2方向；[1,0]/[-1,0]反复翻转则有较大方向方差，即使每步梯度范数都为1。","Is gradient reliability its magnitude or correctness?","Neither. EMA variance of normalized directions measures relative stability. A consistently wrong direction can have high evidence, and batch-relative weights are not calibrated confidence probabilities.","Teaching example: [1,0] and[100,0] have the same L2 direction; alternating[1,0]/[-1,0] has directional variance even though every gradient norm is one."),
    ("LazUnirec蒸馏与OneTrans-V2的精排→预排信号相同吗？",TEXT["comparison"][0],"教学例：LazUnirec两候选分数同时加同一常量不改变请求内softmax教师；不能因此认为任意独立sigmoid蒸馏目标也有相同不变性。","Is its distillation the same as OneTrans-V2 fine-to-pre-ranking transfer?",TEXT["comparison"][1],"Teaching example: adding one constant to both teacher candidate scores leaves a request-local softmax unchanged; an arbitrary independent sigmoid-distillation objective need not share that invariance."),
    ("为什么权重和排序teacher必须detach，clip后要再归一吗？","Eq14权重和Eq16排序teacher均停止梯度，避免模型绕过任务监督去优化evidence或反向改teacher。§4.1.4先相对batch均值归一再clip到[0.8,1.2]，不额外二次归一。","教学例：裁剪后权重[0.8,1.2,1.2]均值为1.0667；再除均值会改变既定损失，且不再严格保留裁剪下界。","Why detach weights and the ranking teacher, and renormalize after clipping?","Equations14/16 detach weights and teacher to avoid optimizing evidence or backpropagating into the teacher through this objective. Section4.1.4 normalizes by batch reliability before clipping to[0.8,1.2], without a second normalization.","Teaching example: clipped weights[0.8,1.2,1.2] average1.0667; renormalizing changes the loss and no longer strictly retains the stated lower bound."),
]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+"\n")


def main():
    import fitz
    if PAGE.exists():
        raise ValueError("append-once authoring; do not overwrite reviewed source")
    assets=PAGE.parent/"assets"
    assets.mkdir(parents=True)
    pdf=ROOT/".cache/nov25-latest/root-primary/2611.32590v1.pdf"
    crop=[64,70,551,316]
    image=assets/"paper-figure-01.png"
    fitz.open(pdf)[2].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(crop)).save(image)
    dump(assets/"provenance.json",{"schema_version":1,"paper_url":SOURCE,"source_url":SOURCE+"#page=3",
        "pdf_page":3,"figure":"Figure2","caption":"The overall framework of LazUnirec.","source_sha256":digest(pdf),
        "crop_pdf_points":crop,"render_scale":2,"asset_sha256":digest(image),"visually_reviewed":True,
        "scientific_content_modified":False,"copyright":"Original authors"})
    for english in (False,True):
        idx=1 if english else 0
        headings=["Original paper","Background and method","Core formula","Reported offline and online results","Relationship to existing methods","Local implementation","Data protocol and code mapping","Results, controls and limits","High-cost full experiment"] if english else ["原始论文总结","背景与主要改动","核心公式","论文离线与线上效果","与已有方法的关系","本地复现","数据协议与代码映射","结果、负控与边界","高成本完整实验"]
        attribution=("Original Figure2 from fixedv1 page3, with complete caption; visually checked without scientific modification. Copyright belongs to the original authors. Not local evidence." if english else "图片来自[原论文]("+SOURCE+"#page=3)第3页Figure2，完整保留图注，版权归原作者所有；已视觉核对、未改科学内容，不是本地结果。")
        metadata=(f"""| Field | Value |
| --- | --- |
| Paper | [Fixed2611.32590v1]({SOURCE}) |
| Company / first-author institution | Xiaodong Li; Alibaba International Digital Commerce Group |
| Original publication | 2026-11-24T13:26:54Z; discovered/reviewed November25; announcement unverified |
| Author code | No paper-specific author repository supplied in fixedv1; no verified public implementation found in this intake |
| Local adapter / key | `lazunirec`; null adapter, independent component |
| Local code | `src/auto_research/reproductions/lazunirec_components.py` |""" if english else f"""| 字段 | 内容 |
| --- | --- |
| 论文链接 | [LazUnirec，固定2611.32590v1]({SOURCE}) |
| 公司 / 作者机构 | 一作Xiaodong Li；全体署名Alibaba International Digital Commerce Group |
| 首次公开日期 | **2026-11-24T13:26:54Z**；本轮发现/审查2026-11-25，公告日期未核定 |
| 原作者开源代码 | 固定v1未给本篇作者代码仓库；本轮未找到可核验的公开方法实现 |
| 本地 adapter / key | `lazunirec`；adapter为null，独立组件 |
| 本地复现代码 | `src/auto_research/reproductions/lazunirec_components.py` |""")
        content=rf"""# LazUnirec: Unifying Retrieval and Ranking in Multi-scenario Industrial Recommendation

{'[简体中文](README.md)' if english else '[English](README-en.md)'}

> {'L1 diagnostic component, not a complete model or capability reproduction. High-cost full experiments are not reproduced (review DONE); no Evolve promotion.' if english else 'L1机制组件，diagnostic only，不是完整模型或能力复现。高成本完整实验不复现（审查 DONE），不接Evolve晋级。'}

## {'Paper information' if english else '论文信息'}

{metadata}

## {headings[0]}

### {headings[1]}

{TEXT['method'][idx]}

<!-- paper-figure:start -->
### {'Key original figure' if english else '原论文关键图'}

[![LazUnirec original Figure2](assets/paper-figure-01.png)]({SOURCE}#page=3)

{attribution} [Provenance/SHA256](assets/provenance.json).
<!-- paper-figure:end -->

### {headings[2]}

{TEXT['formula'][idx]}

$$
\omega_i=\operatorname{{clip}}\left(\frac{{r_i}}{{\operatorname{{Mean}}_j r_j}},0.8,1.2\right),\quad
\mathcal L_{{ue}}=\sum_i\operatorname{{sg}}(\omega_i)\mathcal L_i.
$$

{TEXT['kd'][idx]}

### {headings[3]}

{TEXT['reported'][idx]}

### {headings[4]}

{TEXT['comparison'][idx]}

## {headings[5]}

### {headings[6]}

{TEXT['local'][idx]}

```bash
PYTHONPATH=src python -c 'from auto_research.reproductions.lazunirec_components import diagnostic; print(diagnostic(42))'
PYTHONPATH=src python -m pytest -q tests/test_nov25_lazunirec.py
```

### {headings[7]}

{TEXT['controls'][idx]}

{'Source-bound three-seed CPU and real A100/A30 receipts cover only these small kernels, not a model benchmark.' if english else '冻结源绑定的CPU三seed和真实A100/A30回执只覆盖小型算子，不是模型benchmark。'} [CPU](metrics/component-cpu-seeds42-44.json) · [CUDA](metrics/component-cuda-seeds42-44.json).

### {headings[8]}

{TEXT['cost'][idx]}
"""
        if english:
            content="<!-- source-sha256: "+digest(PAGE)+" -->\n\n"+content
        (PAGE.with_name("README-en.md") if english else PAGE).write_text(content)
    questions=[{"id":"nov25-"+level,"level":level,"question":q[0],"answer":q[1],"example":q[2],"added":DATE,
        "source_sections":["背景与主要改动","核心公式","与已有方法的关系","结果、负控与边界"]}
        for level,q in zip(("basics","mechanism","comparison","implementation"),QUESTIONS,strict=True)]
    units=question_units({IDENTITY:questions})
    english={f"qa/{IDENTITY}/{r['id']}":{"source_sha256":units[f"qa/{IDENTITY}/{r['id']}"].source_sha256,"reviewed":True,
        "fields":{"question":q[3],"answer":q[4],"example":q[5]}} for r,q in zip(questions,QUESTIONS,strict=True)}
    peer="recommendation:onetrans-v2"
    peer_spec=json.loads((ROOT/"src/auto_research/paper_specs/catalog/recommendation/onetrans-v2.json").read_text())
    q=QUESTIONS[2]
    proposal={"paper":IDENTITY,"target_card":"recommendation/history-ranking-backbones",
        "source_revisions":{IDENTITY:digest(PAGE),peer:digest(ROOT/"docs"/peer_spec["detail_path"])},
        "comparison":{"position":TEXT["local"][0],"tradeoff":TEXT["comparison"][0],"sections":["与已有方法的关系","结果、负控与边界"]},
        "analysis":{"title":q[0],"body":TEXT["comparison"][0],"papers":[IDENTITY,peer]},
        "question":{"id":"nov25-lazunirec","question":q[0],"answer":q[1],"example":q[2],"papers":[IDENTITY,peer]},
        "update":{"date":DATE,"papers":[IDENTITY,peer],"summary":TEXT["local"][0]},
        "english":{"comparison":{"position":TEXT["local"][1],"tradeoff":TEXT["comparison"][1]},
        "analysis":{"title":q[3],"body":TEXT["comparison"][1]},"question":{"question":q[3],"answer":q[4],"example":q[5]},"update":TEXT["local"][1]}}
    spec={"domain":"recommendation","key":"lazunirec","title":"LazUnirec: Unifying Retrieval and Ranking in Multi-scenario Industrial Recommendation",
        "paper_url":"https://arxiv.org/abs/2611.32590v1","reviewed_version_url":SOURCE,"reviewed_version":"v1",
        "detail_path":PAGE.relative_to(ROOT/"docs").as_posix(),"first_author":"Xiaodong Li",
        "first_author_affiliation":"Alibaba International Digital Commerce Group","browse_company":"Alibaba",
        "published":"2026-11-24","published_at":"2026-11-24T13:26:54Z","announced_on":None,"discovered_on":DATE,"reviewed_on":DATE,
        "code":None,"code_status":"固定v1未给本篇作者仓库；本轮未找到可核验的公开方法实现","code_license":None,"upstream_revision":None,
        "adapter":None,"topic":["多任务与联合建模","共享骨干与梯度可靠性"],"browse_topic":["生成、排序与冷启动","多任务学习与多目标优化"],
        "priority":"P0","verified_priority_organizations":[],"intake_class":"nov24_first_publication_discovered_nov25",
        "implementation_status":"component_only","evaluation_tier":"l1_mechanism","diagnostic_only":True,"promotion_eligible":False,"evolve_integrated":False,
        "requires_gpu_validation":True,"gpu_validation_passed":False,"gpu_validation_artifact":"docs/gpu-validations/lazunirec-a100-20261125-latest.json",
        "full_experiment_status":"not_reproduced_high_cost","full_experiment_review_done":True,"review_done":True,"review_resolution":"not_reproduced_high_cost",
        "automatic_retry":False,"automatic_implementation_queue":False,"summary":TEXT["method"][0]+" "+TEXT["local"][0],
        "local_operator":"auto_research.reproductions.lazunirec_components.diagnostic",
        "local_command":"PYTHONPATH=src python -c 'from auto_research.reproductions.lazunirec_components import diagnostic; print(diagnostic(42))'",
        "method_source_sha256":digest(pdf),"cost_assessment":{"source":SOURCE,"basis":TEXT["cost"][0],"decision":"成本过高，不复现（审查 DONE）","local_seconds_per_seed_cap":30},
        "online_ab":[{"product":"Alibaba international e-commerce trigger-free recommendation","metric":"GMV","lift_percent":4.01,
        "traffic":"10% production traffic, one week in October2026; replaces MIMA retrieval and LazFormer ranking together",
        "source_url":SOURCE,"source_location":"Section4.8/Table5; full private pipeline, not isolated local kernels"},
        {"product":"Alibaba international e-commerce trigger-based recommendation","metric":"GMV","lift_percent":3.06,
        "traffic":"10% production traffic, one week in October2026","source_url":SOURCE,"source_location":"Section4.8/Table5"}]}
    dump(AUDIT/"paper-proposals-root.json",{"schema_version":1,"papers":{IDENTITY:spec}})
    dump(AUDIT/"root-authored-bundle.json",{"schema_version":1,"papers":{IDENTITY:{"questions":questions}},"english_question_units":english})
    dump(AUDIT/"deep-dive-proposals-root.json",{"schema_version":1,"proposals":[proposal]})


if __name__=="__main__":
    main()
