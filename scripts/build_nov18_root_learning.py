"""Materialize the explicitly authored/reviewed Nov18 root Q&A pairs.

No translation service or template-generated answers. Fingerprints are derived
from the exact Chinese records so later source edits invalidate translations.
"""
from __future__ import annotations

import json
from pathlib import Path

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
PAIRS = {
    "foundation-models:hvmap": [
        ("native-space-first", "basics",
         "HVMap为什么不能直接拿一个查询向量搜索所有库？",
         "不同编码器产生的维度和语义坐标系不兼容。HVMap在hub编码一次后映射查询，每库独立召回，再把候选映射到另一空间重排；并非把向量补零就能跨库可比。",
         "教学例：同样的二维坐标在两个旋转空间代表不同语义，直接点积会改变最近邻。",
         "Why not search every database with one unchanged query vector?",
         "Different encoders have incompatible dimensions and semantic coordinates. HVMap maps a hub-encoded query, retrieves independently and maps candidates for reranking. Zero padding does not align meaning.",
         "Teaching example: identical coordinates in rotated spaces represent different meanings; direct dot products change nearest neighbors."),
        ("absolute-fuzzy-anchor", "mechanism",
         "fuzzy contrastive loss为什么不能替换为mapped-to-mapped RKD？",
         "原式比较目标间距离与映射结果到原始目标的距离；对角项锚定每个配对的绝对对齐。整体旋转或取负保留mapped之间距离，RKD可能为零，但与原始目标不对齐时fuzzy loss非零。",
         "教学例：目标是单位正交基，映射结果整体取负；RKD为0，原式sum loss为12。",
         "Why is mapped-to-mapped RKD not the fuzzy contrastive objective?",
         "The objective compares target-target distances with mapped-to-original-target distances. Diagonal terms anchor paired absolute alignment. A global rotation or sign flip preserves mapped pairwise distances but not alignment to original targets.",
         "Teaching example: negating a three-vector orthonormal basis gives RKD zero but fuzzy sum loss 12."),
        ("mapping-versus-shared-representation", "comparison",
         "HVMap与ECG-RAG都涉及表示转换，目标相同吗？",
         "不同。HVMap对齐异构库、保留各库native分数并联合重排；ECG-RAG复用同一文档表示服务检索与生成压缩。前者不产生答案，后者仍需decoder和联合训练；局部算子都不能代表完整RAG能力。",
         "教学例：HVMap返回跨库候选排序，不会因此获得ECG压缩context并生成答案的路径。",
         "Do HVMap and ECG-RAG solve the same representation problem?",
         "No. HVMap aligns heterogeneous databases while retaining native scores for a union rerank. ECG-RAG reuses one document representation for retrieval and compressed generation context. HVMap does not answer questions; ECG still needs its decoder and joint training.",
         "Teaching example: a cross-database HVMap ranking does not supply ECG's compressed-context answer-generation path."),
        ("native-weight-not-hub", "implementation",
         "SCORE2里0.7权重和最终K配额应怎样处理？",
         "0.7作用于候选所属库的native空间，不总是hub；另0.3为映射空间。每库先取K个，最后联合取K，不强制各库平分。多spoke经hub最多两次映射，原生向量不能被原地覆盖。",
         "教学例：库A候选分数.9/.8，库B为.2/.1，K=2时两项都应来自A。",
         "How do SCORE2's 0.7 weight and final K quota work?",
         "The 0.7 weight belongs to the candidate database's native space, not always the hub; 0.3 weights its mapped space. Retrieve K per database, then select global K without equal quotas. Spokes use at most two hub maps and retain native embeddings.",
         "Teaching example: scores .9/.8 from A and .2/.1 from B produce two A winners for K=2."),
    ],
    "foundation-models:mixed-signals-weights": [
        ("wsp-not-gradient-descent", "basics",
         "Mixed Signals中的权重空间编程，为什么不能直接用SGD实现？",
         "其研究问题是LLM能否通过推理读取或写入权重，规则排除梯度下降与迭代拟合。SGD能优化网络但回答不同问题；本地只实现外部补丁接口，未伪装一个LLM编辑器。",
         "教学例：把loss.backward和optimizer.step藏在edit函数中，仍是梯度训练，不是WSP。",
         "Why not implement weight-space programming using SGD?",
         "The study asks whether LLM reasoning can read or write weights under rules excluding gradient descent and iterative fitting. SGD answers a different question. Local code provides an external patch interface, not a pretend LLM editor.",
         "Teaching example: hiding backward and optimizer.step inside edit is still gradient training, not WSP."),
        ("atomic-and-budgeted", "mechanism",
         "补丁原子性和practice预算为何都需要负控？",
         "无效参数不能在校验后半途留下已改权重，所以先验证全补丁再提交并预留回滚。practice每次实际尝试在执行前计数，失败仍消耗预算；否则异常可以变成免费搜索。",
         "教学例：weight合法、bias含NaN时两者都不能写入；一次callback异常也消耗一次。",
         "Why test both atomic patches and practice budgets?",
         "Validate the entire patch before mutation and preserve rollback, so a later invalid parameter cannot leave partial edits. Count each practice attempt before calling it, including failures, or exceptions become free search.",
         "Teaching example: a valid weight plus a NaN bias changes neither parameter; one callback exception still consumes one call."),
        ("read-signals-versus-edit-weights", "comparison",
         "Mixed Signals接口与AMS激活扫描能互相替代吗？",
         "不能。AMS从固定模型激活方向检查安全训练变化，不编辑参数，也不是安全认证；WSP研究推理修改权重并在未见被试验证。两者诊断通过都不能推出医疗效果或真实修复能力。",
         "教学例：AMS自比较方向相同不证明模型未被修改；线性harness补丁改变forward也不证明EEG修复。",
         "Can the Mixed Signals interface substitute for AMS activation scanning?",
         "No. AMS inspects fixed-model activation directions for safety-training changes; it neither edits weights nor certifies safety. WSP studies reasoning-based edits evaluated on unseen subjects. Passing diagnostics establishes neither medical efficacy nor real repair capability.",
         "Teaching example: AMS self-comparison does not prove an unmodified model; a changed linear-harness forward does not prove EEG repair."),
        ("recovery-and-test-isolation", "implementation",
         "recovery超过1是不是bug，测试标签能给编辑器吗？",
         "恢复比例按(repaired-faulty)/(healthy-faulty)计算，可能大于1或小于0，不应截断；零分母报错。test标签只能留在评价器，不能以practice反馈泄漏；本地callback不是恶意代码沙箱。",
         "教学例：healthy=.8、faulty=.4、repaired=.9，recovery=1.25，是超过健康参考，不是125%准确率。",
         "Is recovery above one a bug, and may editors see test labels?",
         "Recovery is (repaired-faulty)/(healthy-faulty); values above one or below zero remain unclipped, and a zero denominator is rejected. Test labels stay evaluator-only, not practice feedback. The local callback is not an adversarial-code sandbox.",
         "Teaching example: healthy=.8, faulty=.4, repaired=.9 yields recovery=1.25, not 125% accuracy."),
    ],
}


def main():
    papers, translations = {}, {}
    for identity, entries in PAIRS.items():
        rows = []
        for key, level, q, answer, example, eq, ea, ee in entries:
            row = {"id": key, "level": level, "question": q, "answer": answer, "example": example,
                   "source_sections": ["核心公式", "数据协议与代码映射", "结果、负控与边界"], "added": "2026-11-18"}
            rows.append(row)
            unit_id = f"qa/{identity}/{key}"
            unit = question_units({identity: [row]})[unit_id]
            translations[unit_id] = {"source_sha256": unit.source_sha256, "reviewed": True,
                                     "fields": {"question": eq, "answer": ea, "example": ee}}
        papers[identity] = {"questions": rows}
    for path, payload in (("docs/learning/questions/nov18-root.json", {"schema_version": 1, "papers": papers}),
                          ("docs/en/learning/translations/qa-nov18-root.json", {"schema_version": 1, "units": translations})):
        (ROOT / path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
