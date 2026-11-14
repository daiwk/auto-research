"""Materialize two authored historical benchmark protocols and reviewed QA."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov13-colm-remaining"
CACHE = ROOT / ".cache/nov13-colm-remaining/benchmarks"
PAPERS = {
    "avmeme-exam": {
        "id": "2601.17645", "title": "AVMeme Exam: A Multimodal Multilingual Multicultural Benchmark for LLMs' Contextual and Cultural Knowledge and Thinking",
        "published_at": "2026-01-25T01:40:15Z", "first_author": "Xilin Jiang", "first_author_affiliation": "Columbia University",
        "code": "https://avmemeexam.github.io/public/", "code_status": "官方项目、受访问条件约束的数据与加载说明公开；完整模型评测框架源码未确认发布。",
        "operator": "auto_research.multimodal.avmeme_exam.evaluate", "module": "avmeme_exam",
        "figure": "avmeme-figure3.png", "figure_url": "https://arxiv.org/html/2601.17645v1/figure/data_pipeline.png",
        "priority_organizations": ["Google", "Meta"],
        "cost": "19个多模态模型、人工标注及多后端推理完整矩阵；官方媒体受访问条件约束，未下载或调用模型。原文未披露可直接套用的单卡总时长，不编造卡时。",
        "fidelity": "实现选项重排、私有答案映射、主集文本捷径过滤、视频捷径屏蔽及三轴分组计分。严格字母解析为明示本地约定；不处理媒体、不生成捷径标签或模型回答，不猜测七题型宏平均。",
        "summary": "AVMeme Exam用多语言、多文化短音视频多选题评估声音的情境、幽默和应用知识，并过滤文本捷径、屏蔽答案泄漏视频。本地只实现独立可核的协议与计分，不将夹具准确率冒充模型能力。",
    },
    "mmeb-v3": {
        "id": "2604.23321", "title": "MMEB-V3: Measuring the Performance Gaps of Omni-Modality Embedding Models",
        "published_at": "2026-04-25T14:15:05Z", "first_author": "Haohang Huang", "first_author_affiliation": "Eastern Institute of Technology, Ningbo",
        "code": "https://github.com/TIGER-AI-Lab/VLM2Vec/tree/olm2vec", "code_status": "作者公开olm2vec分支；固定提交643150de53fea9133e9d646872228feace906498核对metrics.py，未运行完整190任务矩阵。",
        "operator": "auto_research.multimodal.mmeb_v3.score_task", "module": "mmeb_v3",
        "figure": "mmeb-v3-figure1.png", "figure_url": "https://arxiv.org/html/2604.23321v1/introduction.png",
        "priority_organizations": ["Google"],
        "cost": "190任务、多种2B–8B模型、多模态数据物化和部分百万级候选池；OmniSET还依赖视频/音频生成。只核CPU排序算术，不下载模型、媒体或调用生成API。",
        "fidelity": "精确区分Hit@1/NDCG@5与任务等权聚合，显式选择线性/指数gain；OmniSET要求12方向同一混合池、保留query干扰项、语义与模态同时正确且不计入排行榜。输入排序外置，无编码器或官方数据物化。",
        "summary": "MMEB-V3把统一嵌入评测扩展至190任务，并以OmniSET分离语义匹配和输出模态遵循。本地实现计分与混合候选池诊断合同，不提供真实编码器或完整benchmark成绩。",
    },
}

QA = {
    "avmeme-exam": [
        ("main-split-removes-text-shortcuts", "basics", "为什么AVMeme Exam不能只在meme-full上比较模型？", "完整集中有题目可能不听声音也能猜对。作者用三个纯文本模型识别text_cheat，再形成846条主集；完整集1032条与主集回答不同问题，必须注明分母，不能混报。", "教学例：题目文本已写出流行语出处，纯文本猜对不代表识别了音轨。", "Why is comparing only on meme-full insufficient?", "Some full-set questions can be answered without hearing the clip. Three text-only models identify text_cheat examples, producing the 846-example main split from 1,032 full examples. The splits answer different questions and require explicit denominators.", "Teaching example: a question names a catchphrase's origin; text-only guessing does not establish audio understanding."),
        ("shuffle-private-key-and-mask-video", "mechanism", "重排选项与visual_cheat屏蔽分别防什么？", "重排减弱固定位置偏好，同时必须更新评测端正确字母；visual_cheat屏蔽直接揭露答案的视频。二者不生成正确答案，也不等同消除所有数据污染。", "教学例：正确选项从B移到A后仍按B评分会制造错误；视频字幕写出答案时音视频模式也应移除视频。", "What do option shuffling and visual_cheat masking prevent?", "Shuffling reduces fixed-position bias and requires updating the private correct letter. visual_cheat masking removes videos that directly reveal the solution. Neither creates answers nor eliminates all contamination.", "Teaching example: scoring the old B after the solution moved to A is wrong; a video subtitle revealing the answer requires video removal even in audiovisual mode."),
        ("cultural-mcq-versus-embedding-retrieval", "comparison", "AVMeme Exam和MMEB-V3都涉及多模态，能直接比较总分吗？", "不能。前者是文化情境多选正确率，后者是嵌入检索Hit@1/NDCG与任务聚合。不同输出、候选空间、分母和模型接口不能混为同一个多模态能力分数。", "教学例：音频梗选对一个文化用法，与在全模态候选池找对音频文档不是同一任务。", "Can AVMeme Exam and MMEB-V3 aggregate scores be compared directly?", "No. The former scores culturally situated multiple-choice answers; the latter evaluates embedding retrieval with Hit@1/NDCG and task aggregation. Outputs, candidate spaces, denominators and model interfaces differ.", "Teaching example: choosing a meme's cultural use is not retrieving the correct audio document from an omni-modal pool."),
        ("typed-request-is-not-sandbox", "implementation", "ActorRequest不含答案，是否就能保证没有泄漏？", "不能。它只限制正常回调的数据字段，调用方仍可能通过文件权限、闭包或问题文本泄漏答案。需独立进程/权限审计；本地固定A夹具只验证协议，不报告模型能力。", "教学例：把ScoringKey留在被测进程可读的全局变量中，字段再干净也不隔离。", "Does an answer-free ActorRequest guarantee no leakage?", "No. It limits normal callback fields, but filesystem permissions, closures or question text can still leak answers. Independent process and permission audits are necessary. The fixed-A fixture tests protocol only, not capability.", "Teaching example: a ScoringKey in a globally readable variable defeats isolation despite clean request fields."),
    ],
    "mmeb-v3": [
        ("six-categories-not-one-metric", "basics", "MMEB-V3为什么不能所有任务都套Hit@1？", "音频、图像、视频、Agent使用Hit@1；文本和视觉文档用NDCG@5以保留排序及分级相关性。类别内按任务等权，不是把全部查询混成一个分母。", "教学例：一项一万查询的任务不能自动获得一项一百查询任务的百倍权重。", "Why not use Hit@1 for every MMEB-V3 task?", "Audio, image, video and agent tasks use Hit@1; text and visual documents use NDCG@5 to retain ranking and graded relevance. Category aggregation weights tasks equally rather than pooling all queries.", "Teaching example: a task with 10,000 queries does not automatically receive 100 times the weight of one with 100 queries."),
        ("omniset-shared-pool-self-distractor", "mechanism", "OmniSET为什么保留查询本身，还不能先筛目标模态？", "目标是同时验证语义和所请求的输出模态。查询本身是同语义错误模态干扰项，12方向共享混合池；预筛目标模态会隐藏模型忽略模态指令的失败。", "教学例：图像查音频时把同一图像排第一，语义正确但模态错，应记0。", "Why retain the query itself and avoid target-modality prefiltering in OmniSET?", "The diagnostic tests both semantics and requested output modality. The query is a same-semantic, wrong-modality distractor, and twelve directions share one mixed pool. Prefiltering would hide modality-instruction failures.", "Teaching example: placing the original image first for image-to-audio retrieval has correct semantics but wrong modality and must score zero."),
        ("mmeb-versus-mveb-budget-and-purpose", "comparison", "MMEB-V3与MVEB都做嵌入评测，侧重点有什么区别？", "MMEB-V3覆盖六类并以OmniSET诊断模态遵循；MVEB深入视频分类、聚类和八方向检索，并约束帧/音频预算。任务、候选和输入预算不同，不能把一方总分或局部核当另一方结果。", "教学例：固定64帧上限的视频实验与混合TIVA候选池诊断控制的变量不同。", "How do MMEB-V3 and MVEB differ despite both evaluating embeddings?", "MMEB-V3 covers six categories and diagnoses modality adherence with OmniSET. MVEB focuses on video classification, clustering and eight retrieval directions with frame/audio budgets. Tasks, pools and budgets differ; neither aggregate nor local kernel substitutes for the other.", "Teaching example: a capped-64-frame video experiment controls different variables from a mixed TIVA-pool diagnostic."),
        ("explicit-gain-and-exact-task-coverage", "implementation", "本地为何要求显式gain和完整任务清单？", "固定上游同时输出线性及指数NDCG，擅选会悄悄改变分数；任务缺失也会抬高或降低平均值。API强制gain和预期任务精确匹配，仍不证明外部排序来自真实模型。", "教学例：删掉一个困难任务后报告其余均值，不能叫完整类别成绩；fixture排序即使得1也不是模型实测。", "Why require explicit NDCG gain and exact task coverage?", "The fixed upstream emits linear and exponential NDCG, so silently choosing one changes scores. Missing tasks also alter averages. The API enforces the gain and exact expected tasks, but cannot prove external rankings came from a real model.", "Teaching example: omitting a difficult task invalidates a complete-category claim; a perfect fixture ranking is not model evidence."),
    ],
}


def write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main():
    bank, translations = {}, {}
    for key, record in PAPERS.items():
        detail = f"multimodal-models/{record['id']}-{key}/README.md"
        page = ROOT / "docs" / detail
        asset = page.parent / "assets/paper-figure-01.png"
        asset.parent.mkdir(exist_ok=True)
        shutil.copyfile(CACHE / record["figure"], asset)
        english = page.with_name("README-en.md")
        fingerprint = hashlib.sha256(page.read_bytes()).hexdigest()
        text = english.read_text()
        if "<!-- source-sha256:" not in text:
            english.write_text(f"<!-- source-sha256: {fingerprint} -->\n" + text)
        spec = {field: record[field] for field in ("title", "first_author", "first_author_affiliation", "published_at", "code", "code_status", "summary")}
        spec.update(domain="multimodal-models", key=key, paper_url=f"https://arxiv.org/abs/{record['id']}", reviewed_version="v1", reviewed_arxiv_id=record["id"] + "v1", reviewed_version_url=f"https://arxiv.org/html/{record['id']}v1", detail_path=detail, topic=["跨模态评测与检索", "文化理解" if key == "avmeme-exam" else "全模态嵌入与模态遵循"], published=record["published_at"][:10], adapter=None, priority="P1", implementation_status="evaluation_protocol_interface", local_operator=record["operator"], local_command=f"PYTHONPATH=src python -c 'from auto_research.multimodal.{record['module']} import diagnostic; print(diagnostic(42))'", evaluation_tier="l0_interface", diagnostic_only=True, promotion_eligible=False, evolve_integrated=False, requires_gpu_validation=False, full_experiment_status="not_reproduced_high_cost", full_experiment_review_done=True, review_done=True, automatic_retry=False, automatic_implementation_queue=False, fidelity_note=record["fidelity"], cost_assessment={"source": f"https://arxiv.org/html/{record['id']}v1", "available_resource": "单张A100/A30或Mac", "basis": record["cost"]})
        write(ROOT / f"src/auto_research/paper_specs/catalog/multimodal-models/{key}.json", spec)
        identity = "multimodal-models:" + key
        questions = []
        for row in QA[key]:
            qid, level, question, answer, example, eq, ea, ee = row
            questions.append({"id": qid, "level": level, "question": question, "answer": answer, "example": example, "source_sections": ["背景与主要改动", "核心公式", "数据协议与代码映射", "复现边界与完整实验"], "added": "2026-11-13"})
            translations[f"qa/{identity}/{qid}"] = {"reviewed": True, "fields": {"question": eq, "answer": ea, "example": ee}}
        bank[identity] = questions
    units = question_units(bank)
    for key, value in translations.items():
        value["source_sha256"] = units[key].source_sha256
    write(ROOT / "docs/learning/questions/nov13-colm-benchmarks.json", {"schema_version": 1, "papers": {key: {"questions": rows} for key, rows in bank.items()}})
    write(ROOT / "docs/en/learning/translations/qa-nov13-colm-benchmarks.json", {"schema_version": 1, "units": translations})
    write(AUDIT / "benchmarks-review.json", {"schema_version": 1, "reviewed_on": "2026-11-13", "scope": "Two fixed-v1 benchmark papers; sourceful review and L0 protocol only", "papers": [{"id": value["id"], "key": key, "domain": "multimodal-models", "decision": "implement_l0_protocol_full_campaign_not_reproduced_high_cost", "verified_priority_organizations": value["priority_organizations"], "method_sections": ["benchmark construction", "evaluation protocol", "results and limitations"], "source_url": f"https://arxiv.org/html/{value['id']}v1", "source_sha256": hashlib.sha256((ROOT / '.cache/nov13-colm-remaining/evaluation' / (value['id'] + 'v1.html')).read_bytes()).hexdigest(), "figure_sha256": hashlib.sha256((CACHE / value["figure"]).read_bytes()).hexdigest(), "cost_basis": value["cost"]} for key, value in PAPERS.items()]})


if __name__ == "__main__":
    main()
