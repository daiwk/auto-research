"""Generate this batch's authored foundation QA/proposals only.

No old author script is called; no shared learning bank, README or frozen
evidence is modified. English prose is authored below, not machine-derived.
"""

from hashlib import sha256
import json
from pathlib import Path

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov25-latest"
DATE = "2026-11-25"
SECTIONS = ["背景与主要改动", "核心公式", "同主题比较与边界", "数据协议与代码映射", "高成本完整实验"]

CONTENT = {
    "udvr": {
        "peer": "foundation-models:proland", "peer_path": "foundation-models/2611.00236-proland/README.md",
        "card": "foundation-models/training-budget",
        "position": "UDVR固定U列/V行的长度，把尺度移入不参与优化的D；attention双侧吸收，FFN仅吸收U侧。它通过不同分支正则与形状规则设置更新尺度，不是训练一个独立幅值参数。",
        "tradeoff": "ProLand协调LoRA乘积空间谱方向，并独立恢复B的Stiefel约束；UDVR不要求正交，只固定长度。长度相等不保证方向独立，QR与单独Muon不是替代实现；两个L1诊断都不支持跨模型训练效果比较。",
        "detail": "原文FFN的D更新不含V侧尺度，故GELU路径不函数守恒；attention才有精确UDV守恒。D必须是buffer，真实任务梯度与分支正则先更新U/V，之后再重平衡，不能把投影放在梯度前充数。",
        "en_position": "UDVR pins U-column/V-row lengths and moves scale into a non-optimized D buffer, absorbing both sides for attention but only U for FFNs. Branch-specific regularizers and a shape rule set update scale; D is not an independently trained magnitude.",
        "en_tradeoff": "ProLand coordinates product-space LoRA spectral directions and separately restores B toward the Stiefel manifold. UDVR imposes lengths, not orthogonality. Equal lengths do not imply independent directions; QR and separate Muon updates are not substitutes. Neither local L1 diagnostic supports cross-model training comparisons.",
        "en_detail": "The FFN D update excludes removed V scale, so its GELU path is not function-preserving. Exact UDV invariance applies to attention. D remains a buffer; task and branch-regularizer gradients update U/V before rebalancing.",
        "qa": [
            ("buffer-not-learned-gain", "basics", "D不参与优化，为什么仍能改变？", "每步U/V更新后，重平衡把被移除的方向尺度乘进D。它随更新轨迹变化，但没有独立梯度或学习率。", "教学例：U某列的范数翻倍，归一回原长度时attention对应D元素吸收这个2；D不需要出现在Adam参数表。", "Why can D change without being optimized?", "Rebalancing transfers removed U/V scales into D after each factor update. D follows the trajectory without an independent gradient or learning rate.", "Illustration: doubling a U-column norm transfers a factor2 into its attention D entry when repinned, without adding D to Adam."),
            ("two-branch-scale-transfer", "mechanism", "为什么不能把attention的D=SDR直接用于原文FFN？", "FFN有激活，原文只将U尺度移入D，V仍投影但其尺度被丢弃；同时用系数2的FFN正则补足传入D的收缩。双侧守恒只属于attention分支。", "教学例：保持UD不变却将V除以2，GELU(xUD)V输出减半；把它断言为原函数不变会误判。", "Why not use attention's D=SDR update in the paper's FFN?", "The activation leads the paper to transfer only U scale into D while projecting V and discarding its scale. The FFN regularizer has factor2 to restore shrinkage reaching D. Two-sided product invariance is an attention property.", "Illustration: holding UD fixed and dividing V by2 halves GELU(xUD)V, so a function-invariance assertion would be wrong."),
            ("length-not-stiefel", "comparison", "UDVR和ProLand都约束因子，约束相同吗？", "不相同。UDVR逐列/行固定长度而允许方向相关；ProLand围绕B的正交性与乘积空间谱更新。二者的几何和优化顺序不能互换。", "教学例：两列完全一样但范数都为目标值可满足UDVR，却不满足B转置B=I。", "Do UDVR and ProLand impose the same factor constraint?", "No. UDVR fixes individual lengths while allowing correlated directions. ProLand combines B orthogonality with product-space spectral updates. Their geometry and update ordering are not interchangeable.", "Illustration: identical columns with the target norm can satisfy UDVR but not B-transpose-B=I."),
            ("post-step-real-buffer", "implementation", "怎样验收重平衡不是只在初始化执行？", "用真实损失反传并更新U/V，逐步调用重平衡后核对方向范数；另查D不在参数表、attention乘积守恒及零方向拒绝。只测初始化shape不够。", "教学例：跑4次Adam，每次更新后检查所有方向长度；对零列应报错，而不是加未声明epsilon伪造方向。", "How do we check rebalancing beyond initialization?", "Backpropagate a real loss, update U/V, rebalance each step and check direction norms. Also verify D is not a parameter, attention-product invariance and rejection of zero directions. Initial shapes alone are insufficient.", "Illustration: check every direction after four Adam updates; a zero column must fail instead of receiving an undeclared epsilon direction.")
        ],
    },
    "thresholded-longce": {
        "peer": "foundation-models:merlin", "peer_path": "foundation-models/2610.37645-merlin/README.md",
        "card": "foundation-models/context-and-state",
        "position": "TLCE不改状态容量，而比较同一目标的full/short log-prob；仅当优势超过1nat且短窗已积累128token时给capped ratio权重，再按总权重归一化。它强调已被模型利用的远上下文信息。",
        "tradeoff": "MERLIN用routing key的一二阶矩改变多状态读取，TLCE改变训练监督分配。更强读取结构不等于已经学会召回；反之损失加权也不能恢复固定状态中未保存的信息。两者需要相同模型/数据预算的独立组合实验，现有小核不支持组合收益。",
        "detail": "短窗最大512，边界必须重置状态/attention，额外前向无梯度，权重也stop-gradient。全程联合重复实验包含另一个内容干预，本地未实现句子重复，不能将TLCE接口当成全文recall比较。",
        "en_position": "TLCE keeps state capacity unchanged and compares full/short log-probabilities for the same target. A capped ratio applies only above1nat of benefit and after128short-context tokens, with total-weight normalization. It emphasizes distant information the model already uses.",
        "en_tradeoff": "MERLIN changes multi-state readout using routing-key first/second moments; TLCE changes supervision allocation. Flexible readout does not establish learned recall, while weighting cannot recover information absent from state. Joint benefits require matched model/data budgets and are not established by existing small components.",
        "en_detail": "Short windows contain at most512tokens, reset state/attention, and run without gradients; weights are also detached. Full-training combined experiments include sentence repetition, absent locally. The loss interface is not a reproduction of the paper's recall comparison.",
        "qa": [
            ("benefit-not-importance-oracle", "basics", "TLCE会自动找到所有应该依赖远处信息的token吗？", "不会。权重取决于当前模型的full概率是否已经显著高于short；尚未利用的远处线索不会因为理论上有用就被加权。", "教学例：远处有答案但full与short概率同为0.1，差为0，权重仍为1。", "Does TLCE find every token that should use distant context?", "No. Weighting depends on the current model already assigning substantially higher probability with full context. A theoretically useful but unused cue receives no extra weight.", "Illustration: if both probabilities are0.1 despite a distant answer, the difference is0 and the weight remains1."),
            ("strict-and-offset-boundaries", "mechanism", "Δ=1和窗内位置127时，TLCE会加权吗？", "都不会。必须Δ严格大于1且offset至少128；符合条件后exp(Δ)最多为5，并对valid目标的总权重归一化。", "教学例：Δ分别为1/2/2，offset为128/127/128时权重为1/1/5；不是1/e²/e²。", "Do delta=1 or window offset127 receive extra weight?", "No. Delta must be strictly above1 and offset at least128. Eligible exponentiated differences are capped at5 and normalized over valid targets' total weight.", "Illustration: deltas1/2/2 at offsets128/127/128 receive1/1/5, not1/e-squared/e-squared."),
            ("supervision-versus-readout", "comparison", "TLCE能替代MERLIN的多状态路由吗？", "不能。TLCE重分配训练损失而不改变记忆结构；MERLIN改变分段状态的读取权重。未存的信息和未学会使用的信息是不同瓶颈。", "教学例：若两个历史压进同一状态后已无法区分，给后续token更大loss不能保证还原；保留多个状态则改变了可读取信息。", "Can TLCE replace MERLIN's multi-state routing?", "No. TLCE reallocates loss without changing memory structure; MERLIN changes segment-state readout. Missing information and unlearned use of available information are different bottlenecks.", "Illustration: weighting a later token cannot guarantee recovery after two histories become indistinguishable in one state; preserving multiple states changes what can be read."),
            ("reset-and-detach", "implementation", "为什么只传入两组任意log-prob不足以验证短窗协议？", "权重公式不能证明short来自真正重置的因果窗口。需要实际分窗前向、检查边界重置且无梯度，并核对full梯度只为负归一化权重。", "教学例：650-token输入在512处重新调用模型，short第512位置应等同独立短序列首位，而不继承前512的GRU状态。", "Why are two arbitrary log-probability arrays insufficient to verify the short-window protocol?", "The weighting formula cannot prove that short scores came from reset causal windows. Run actual chunked no-grad forwards, check reset boundaries and confirm the full gradient is only the negative normalized weight.", "Illustration: for650tokens, call the model again at512; its short score there must match an independent first position without the preceding GRU state.")
        ],
    },
    "criticjepa": {
        "peer": "foundation-models:jepa-prediction-planning", "peer_path": "foundation-models/2610.19375-jepa-prediction-planning/README.md",
        "card": "multimodal-models/world-state-actions",
        "position": "CriticJEPA每层用真实训练轨迹的hindsight目标学习conditional flow提案，冻结层级rollout作选择；可短有锚精修，但最终按不含anchor的cost重选。排序能力与可利用的梯度方向分开验证。",
        "tradeoff": "预测—规划评测区分表示可读性、预测误差与实际成功；CriticJEPA在同一冻结模型上进一步区分候选来源、排序与优化。两者都不能用latent loss取代环境执行。CriticJEPA额外要求真实flow和多层时间合同，固定候选fixture只能是诊断，不能替代能力实现。",
        "detail": "最终critic cost保留H-JEPA的目标空间、评分时间窗与action-consistency项；上层选择计划的首个预测状态作为子目标。论文FLOPs计入反传而非墙时。本地按18模型/多域训练规划矩阵高成本终态收录，无operator、无环境执行或自动重试。",
        "en_position": "CriticJEPA learns per-level conditional flow proposals from hindsight goals in real training trajectories and selects using a frozen hierarchical rollout. Optional short anchored polish precedes final selection without the anchor. Ranking quality and useful gradient directions are tested separately.",
        "en_tradeoff": "Prediction-planning evaluation separates representation readability, prediction error and execution success. CriticJEPA further distinguishes candidate sources, rankings and optimization under one frozen model. Neither substitutes latent loss for execution. CriticJEPA additionally needs trained flows and temporal hierarchy contracts; fixed candidates are diagnostic, not capability implementations.",
        "en_detail": "The final critic retains H-JEPA's target space, scoring windows and action-consistency term. The first predicted upper state becomes the subgoal. Paper FLOPs include backpropagation, not wall time. The18-model multi-domain matrix is terminally cost-deferred locally, with no operator, environment execution or automatic retry.",
        "qa": [
            ("ranking-is-not-gradient-quality", "basics", "能正确比较两个计划，就表示世界模型梯度能持续改进动作吗？", "不表示。排序仅需候选间相对评分有信息；优化需要沿局部梯度移动也改善真实执行。持续搜索还可能利用预测误差。", "教学例：模型把安全绕行排在撞墙前，仍可能在绕行附近沿错误梯度把动作推向墙；该例说明逻辑差异，不是论文实测轨迹。", "Does ranking two plans imply gradients can keep improving actions?", "No. Ranking needs informative relative scores; optimization needs local gradient moves to improve real execution. Prolonged search may exploit prediction error.", "Illustration: a model may rank a safe detour above a collision yet have gradients near that detour pointing toward a wall. This is a teaching example, not a measured trajectory."),
            ("anchor-not-final-score", "mechanism", "anchor惩罚为什么不留在最终选择cost里？", "anchor限制每个候选偏离自身提案的距离，用于局部精修；最终需要比较实际rollout目标cost，而不是奖励离初始候选更近。", "教学例：A的rollout cost为1但移动0.5，B为2但未移动；最终应选A，不能因为A离提案远就让anchor翻转排名。", "Why remove the anchor from the final selection score?", "The anchor limits local departure from each proposal during polish. Final selection compares rollout objective costs rather than rewarding proximity to a starting proposal.", "Illustration: if A has rollout cost1 after moving0.5 and unchanged B has cost2, final selection chooses A without letting an anchor reverse the ranking."),
            ("prediction-planning-and-candidate-source", "comparison", "CriticJEPA比预测—规划评测多区分了什么？", "前者在同一冻结模型里改变候选来源与搜索方式，区分能否排序、梯度是否有效和环境成功；后者用冻结解码协议拆表示与预测误差，并单独要求真实规划结果。", "教学例：一步误差相同的模型可对flow提案有用、对长搜索生成的离分布候选无用；因此不能仅按一步loss选规划器。", "What distinction does CriticJEPA add to prediction-planning evaluation?", "It changes candidate sources and search under a frozen model to separate ranking, useful gradients and execution. The evaluation protocol instead decomposes representation/prediction errors with a frozen decoder and separately requires real planning outcomes.", "Illustration: an unchanged one-step-error model may rank flow proposals usefully but not out-of-distribution prolonged-search outputs; one-step loss alone cannot select the planner."),
            ("no-fixture-for-proposer", "implementation", "用预先写好的好动作候选能算低成本CriticJEPA复现吗？", "不能。conditional flow的训练、生成及跨层目标/时间窗决定候选分布，是核心机制。固定候选可诊断critic接口，但不能声称复现提案能力；完整矩阵已按成本终态不复现。", "教学例：手填一条到目标的动作再让critic选中，只证明列表里有答案；本地因此不写这种可执行operator，也不报告控制成功率。", "Do hand-written good actions count as a low-cost CriticJEPA reproduction?", "No. Trained conditional flows, generation and cross-level target/time contracts define the candidate distribution. Fixed candidates can diagnose an interface, not proposal capability; full experiments are terminally cost-deferred.", "Illustration: inserting a goal-reaching action by hand only proves the list contains an answer. No such executable operator or control-success metric is provided locally.")
        ],
    },
}


def main():
    specs = json.loads((AUDIT / "paper-proposals-foundation.json").read_text())["papers"]
    papers, english, proposals, accepted = {}, {}, [], []
    for spec in specs:
        content, identity = CONTENT[spec["key"]], "foundation-models:" + spec["key"]
        questions, translations = [], {}
        for qid, level, q, a, example, eq, ea, ee in content["qa"]:
            questions.append({"id": qid, "level": level, "question": q, "answer": a, "example": example,
                              "source_sections": SECTIONS, "added": DATE})
            translations[qid] = {"question": eq, "answer": ea, "example": ee}
        papers[identity] = {"questions": questions}
        units = question_units({identity: questions})
        for question in questions:
            uid = f"qa/{identity}/{question['id']}"
            english[uid] = {"source_sha256": units[uid].source_sha256, "reviewed": True,
                            "fields": translations[question["id"]]}
        pair = [identity, content["peer"]]
        revisions = {identity: sha256((ROOT / "docs" / spec["detail_path"]).read_bytes()).hexdigest(),
                     content["peer"]: sha256((ROOT / "docs" / content["peer_path"]).read_bytes()).hexdigest()}
        question = questions[2]
        proposals.append({"paper": identity, "target_card": content["card"], "source_revisions": revisions,
                          "comparison": {"position": content["position"], "tradeoff": content["tradeoff"], "sections": SECTIONS[:3]},
                          "analysis": {"title": spec["title"], "body": content["tradeoff"] + " " + content["detail"], "papers": pair},
                          "question": {"id": "nov25-" + spec["key"], "question": question["question"], "answer": question["answer"], "example": question["example"], "papers": pair},
                          "update": {"date": DATE, "papers": pair, "summary": content["tradeoff"] + " 完整实验按成本终态收录，不以L1诊断或资料收录晋级Evolve。"},
                          "english": {"comparison": {"position": content["en_position"], "tradeoff": content["en_tradeoff"]},
                                      "analysis": {"title": spec["title"], "body": content["en_tradeoff"] + " " + content["en_detail"]},
                                      "question": translations[question["id"]], "update": content["en_tradeoff"] + " Full experiments are terminally cost-deferred; no L1 diagnostic or review-only entry is Evolve evidence."}})
        accepted.append({"arxiv_id": spec["paper_url"].split("/")[-1].split("v")[0], "identity": identity,
                         "key": spec["key"], "domain": spec["domain"], "title": spec["title"], "first_author": spec["first_author"],
                         "first_author_affiliation": spec["first_author_affiliation"], "first_published_at": spec["published_at"],
                         "announced_on": spec["announced_on"], "intake_class": spec["intake_class"], "reviewed_version": "v1",
                         "reviewed_source_url": spec["reviewed_version_url"], "source_sha256": spec["method_source_sha256"],
                         "sections_read": spec["cost_assessment"]["sections"], "scope": spec["summary"],
                         "source_revisions": revisions,
                         "cost_basis": spec["cost_assessment"], "implementation_status": spec["implementation_status"],
                         "evaluation_tier": spec["evaluation_tier"], "local_detail_path": spec["detail_path"],
                         "requires_gpu_validation": False, "gpu_validation_passed": False, "code_url": spec["code"],
                         "upstream_revision": spec["upstream_revision"], "full_experiment_status": "not_reproduced_high_cost",
                         "full_experiment_review_done": True, "review_done": True, "automatic_retry": False,
                         "automatic_implementation_queue": False})
    outputs = {
        "foundation-authored-bundle.json": {"schema_version": 1, "date": DATE, "papers": papers, "english_question_units": english},
        "deep-dive-proposals-foundation.json": {"schema_version": 1, "reviewed_on": DATE, "integration_owner": "root", "proposals": proposals},
        "foundation-review.json": {"schema_version": 1, "reviewed_on": DATE, "accepted": accepted,
                                   "preflight_before_implementation": True, "available_resource": "one A100 or A30, or local Mac",
                                   "watermark_change_claimed": False, "large_downloads_authorized_or_needed": False,
                                   "scope": "Finite Nov24 first-release selection; two CPU-only L1 components and one terminal high-cost review-only paper. Not exhaustive coverage."},
    }
    for name, record in outputs.items():
        (AUDIT / name).write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
