"""Author this run's reviewed post-training pages and teaching sources only.

No shared catalog, ledger, controller, or deep-dive bank is mutated here.
"""

from __future__ import annotations

from hashlib import sha256
import importlib
import json
from pathlib import Path

from english_learning_sources import question_units
from nov19_post_content import CONTENT

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov19-latest/post"
AUDIT = ROOT / "docs/research-audits/nov19-latest"
DATE = "2026-11-19"


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n")


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    import fitz

    metadata = {r["canonical_id"]: r for r in json.loads((ROOT / ".cache/nov19-latest/metadata-pool.json").read_text())["papers"]}
    questions, translations, proposals, reviews = {}, {}, [], []
    for key, c in CONTENT.items():
        identity = "post-training:"+key
        meta = metadata[c["id"]]
        title, stamp = meta["title"], meta["published"]
        path = f"post-training/{c['id']}-{key}/README.md"
        directory = ROOT / "docs" / Path(path).parent
        assets = directory / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        source_url = f"https://arxiv.org/html/{c['id']}v1"
        pdf = CACHE / (c["id"]+"v1.pdf")
        page, figure, bbox = c["figure"]
        document = fitz.open(pdf)
        image = assets / "paper-figure-01.png"
        document[page-1].get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(bbox), alpha=False).save(image)
        figure_url = f"https://arxiv.org/pdf/{c['id']}v1#page={page}"
        write(assets / "provenance.json", {
            "schema_version": 1, "reviewed_on": DATE, "figures": [{
                "file": image.name, "paper_id": c["id"], "version": "v1", "figure": figure,
                "page_number": page, "source_url": figure_url, "source_kind": "fixed_v1_pdf_rendered_crop",
                "pdf_sha256": digest(pdf), "image_sha256": digest(image), "crop_pdf_points": bbox,
                "render_scale": 3, "dpi": 216, "caption_included": True,
                "visual_review_done": True, "scientific_content_modified": False,
                "attribution": "Copyright belongs to the original authors. Original figure and caption reproduced for attributed research commentary, not a local result.",
                "license": "Original fixed-version arXiv paper; author copyright retained; no code relicensing.",
            }],
        })
        component = c["module"] is not None
        local = "src/auto_research/post_training/"+c["module"]+".py" if component else None
        tier = "l1_mechanism" if component else "review_only"
        code_cn = (f"论文提供[作者仓库地址]({c['code']})，但本轮官方GitHub API返回404；未验证可获取本篇源码、许可或固定commit，不称开源已验收。" if c.get("code") else "固定v1及所核作者入口未找到可验证的本篇方法源码发布；所用模型、训练库不算本篇开源。")
        code_en = (f"The paper supplies an [author repository URL]({c['code']}), but the official GitHub API returned404 in this review. No accessible method source, licence or fixed commit was verified; a validated open-source release is not claimed." if c.get("code") else "No verifiable method-source release found in fixed v1 or the bounded author entry points checked. Referenced models and trainers are not this paper's source release.")
        run = f"PYTHONPATH=src python -c 'from auto_research.post_training.{c['module']} import diagnostic; print(diagnostic(42))'" if component else None
        metrics_link = f"../../research-audits/nov19-latest/independent-cpu-runs/{key}.json"
        if component:
            module = importlib.import_module("auto_research.post_training."+c["module"])
            rows = [module.diagnostic(s, device="cpu") for s in [42, 43, 44]]
            if any(not all(r["checks"].values()) for r in rows):
                raise ValueError("failed CPU diagnostic "+key)
            write(directory / metrics_link, {
                "schema_version": 2, "key": key, "device": "cpu", "seeds": [42, 43, 44],
                "diagnostic_only": True, "evaluation_tier": tier, "per_seed": rows,
                "source_sha256": {local: digest(ROOT / local)}, "source_commit": None,
                "provenance_note": "Independent working-tree CPU execution; content hashes identify the code. This is not the later frozen-source batch receipt.",
                "formal_comparison": False, "capability_comparison": False,
                "promotion_eligible": False, "evolve_integrated": False,
            })
        cn_local = (f"已独立执行CPU seeds42/43/44：[指标]({metrics_link})。本地指标只检验公式、边界与负控，不是能力或排序效果。" if component else "本轮只完成方法、原图、成本与边界收录；无模型实现、能力指标或GPU待验收任务。")
        en_local = (f"Independent CPU seeds42/43/44 were executed: [metrics]({metrics_link}). These test formulas, boundaries and negative controls, not capability or ranking performance." if component else "This intake records the method, original figure, costs and limits only. There is no model implementation, capability metric or pending GPU-acceptance task.")
        cn_gpu = "\n\nCUDA路径须由本轮真实A100/A30冻结源码回执验收；统一回执未完成前不称GPU已通过。" if c["gpu"] else "\n\n此项仅CPU标量/序列算法，无CUDA广告路径，不需要以GPU测试冒充模型实验。" if component else ""
        en_gpu = "\n\nThe CUDA path requires this batch's actual frozen-source A100/A30 receipt; GPU acceptance is not claimed before that receipt exists." if c["gpu"] else "\n\nThis is a CPU scalar/sequence algorithm without an advertised CUDA path; GPU testing would not turn it into a model experiment." if component else ""
        cn = f"""# {title}

[English](README-en.md)

> **{'L1独立机制组件，diagnostic only' if component else '仅研究资料，无本地实现'}。** 完整实验成本过高，不复现（审查 DONE）；不自动重试、不进入Evolve晋级。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [arXiv {c['id']}v1](https://arxiv.org/abs/{c['id']}v1)；[固定v1原文]({source_url}) |
| 公司 / 作者机构 | 一作 **{c['author']}**：**{c['affiliation']}**；由固定v1作者栏核对，不把引用模型当机构 |
| 首次公开日期 | **{stamp}**（UTC，原始提交）；11月19日公告与本次审查不是首发日期 |
| 原作者开源代码 | {code_cn} |
| 本地 adapter / key | `{key}`；`adapter: null` |
| 本地复现代码 | {'`'+local+'`' if component else '无算法实现；仅本文与catalog资料，不创建占位模型'} |

## 原始论文总结

### 背景与主要改动

{c['method']}

<!-- paper-figure:start -->
### 原论文关键图

[![原论文 Figure {figure}](assets/paper-figure-01.png)]({figure_url})

图片来自[原论文]({figure_url})第{page}页，版权归原作者所有；保留完整图与原图注，未重绘或修改科学内容。裁剪与SHA见[provenance](assets/provenance.json)。图中的结果属于作者，不是本地实验。
<!-- paper-figure:end -->

```mermaid
flowchart LR
    A["合法输入或原文配置"] --> B["{key} 特有机制"]
    B --> C["{'有限公式与负控' if component else '成本审查与终态收录'}"]
    C --> D["不声称完整模型能力"]
```

### 核心公式

固定v1位置：{'；'.join(c['sections'])}。

$$
{c['formula']}
$$

### 论文离线与线上效果

{c['result']}

### 与已有方法的关系

{c['compare']}

## 本地复现

### 数据协议与代码映射

{c['scope']}

{('```bash'+chr(10)+run+chr(10)+'PYTHONPATH=src python -m pytest -q tests/post_training/test_nov19_post_components.py'+chr(10)+'```') if component else '无运行命令。方法收录不代表可执行adapter或Evolve operator。'}

### 结果、负控与边界

{cn_local}{cn_gpu}

{c['questions'][3][1]}

### 高成本完整实验

{c['cost']}

**成本过高，不复现（审查 DONE）**。上述规模与时间依据来自原文，不是本地测速；不下载checkpoint/数据，不探跑完整实验，不加入自动重试队列。可用预算为单张A100或A30、或Mac，不假设多卡或两台同时使用。
"""
        (directory / "README.md").write_text(cn)
        en = f"""# {title}

<!-- source-sha256: {digest(directory / 'README.md')} -->

[简体中文](README.md)

> **{'Independent L1 mechanism component, diagnostic only' if component else 'Research reference only; no local implementation'}.** The high-cost full experiment is not reproduced (review DONE), with no automatic retry or Evolve promotion.

## Paper information

| Field | Content |
| --- | --- |
| Paper link | [arXiv {c['id']}v1](https://arxiv.org/abs/{c['id']}v1); [fixed v1]({source_url}) |
| Company / author institution | First author **{c['author']}**: **{c['affiliation']}**, verified from the fixed-v1 byline rather than cited model names |
| Original publication date | **{stamp}** (UTC original submission); the November19 announcement/review is not the publication date |
| Original source code | {code_en} |
| Local adapter / key | `{key}`; `adapter: null` |
| Local reproduction code | {'`'+local+'`' if component else 'No algorithm implementation; only this write-up and catalog record, without a placeholder model'} |

## Original paper summary

### Background and main changes

{c['method_en']}

### Key original figure

[![Original Figure {figure}](assets/paper-figure-01.png)]({figure_url})

Original figure and full caption from [fixed-v1 PDF page{page}]({figure_url}); copyright belongs to the original authors. No scientific content was redrawn or changed. Crop and hashes: [provenance](assets/provenance.json). Author results are not local experiments.

### Core formula

Source locations: {'; '.join(c['sections'])}.

$$
{c['formula']}
$$

### Paper results and online evidence

{c['result_en']}

### Relation to existing methods

{c['compare_en']}

## Local reproduction

### Data protocol and code mapping

{c['scope_en']}

{('```bash'+chr(10)+run+chr(10)+'PYTHONPATH=src python -m pytest -q tests/post_training/test_nov19_post_components.py'+chr(10)+'```') if component else 'No execution command. Cataloging is not an executable adapter or Evolve operator.'}

### Results, negative controls and limits

{en_local}{en_gpu}

{c['questions'][3][4]}

### High-cost full experiment

{c['cost_en']}

**High cost: not reproduced (review DONE).** Resource and timing statements come from the paper, not local measurements. No checkpoint/data download, full-experiment probe or automatic retry is performed. The budget is one A100 or A30, or a Mac; multiple GPUs or simultaneous hosts are not assumed.
"""
        (directory / "README-en.md").write_text(en)
        spec = {
            "domain": "post-training", "key": key, "title": title,
            "paper_url": f"https://arxiv.org/abs/{c['id']}v1", "reviewed_version_url": source_url,
            "reviewed_version": "v1", "detail_path": path, "first_author": c["author"],
            "first_author_affiliation": c["affiliation"], "published": stamp[:10], "published_at": stamp,
            "code": c.get("code"), "code_status": code_cn, "code_license": None, "upstream_revision": None,
            "adapter": None, "topic": [c["topic"], "后训练算法组件" if component else "后训练方法资料"],
            "priority": "P1", "intake_class": "new_submission_announced_after_previous_scan",
            "implementation_status": "component_only" if component else "deferred_high_cost",
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "requires_gpu_validation": c["gpu"], "gpu_validation_passed": False,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
            "review_done": True, "review_resolution": "not_reproduced_high_cost",
            "automatic_retry": False, "automatic_implementation_queue": False,
            "cost_assessment": {"source": source_url, "source_sections": c["sections"], "basis": c["cost"],
                "available_resource": "Single NVIDIA A100/A30 or local Mac",
                "decision": "Full experiment not reproduced due to high cost; review DONE. No checkpoint/data download or paid API.",
                "local_budget": {"checkpoint_download_bytes": 0, "dataset_download_bytes": 0, "paid_api_calls": 0,
                    "local_component_seconds_per_seed_cap": 30 if component else 0,
                    "gpu_component_seconds_per_seed_cap": 30 if c["gpu"] else 0}},
            "summary": c["method"].split("\n")[0]+" "+c["scope"], "evaluation_tier": tier,
        }
        if c["gpu"]:
            spec["gpu_validation_artifact"] = f"docs/gpu-validations/{key}-a100-20261119-latest.json"
        if component:
            spec.update(local_operator=f"auto_research.post_training.{c['module']}.diagnostic", local_command=run)
        else:
            spec["deferral_reason"] = c["cost"]+" 成本过高，不复现（审查 DONE）。"
        write(ROOT / f"src/auto_research/paper_specs/catalog/post-training/{key}.json", spec)
        qrows, enrows = [], {}
        for level, q in zip(["basics", "mechanism", "comparison", "implementation"], c["questions"], strict=True):
            qid = "nov19-"+level
            qrows.append({"id": qid, "level": level, "question": q[0], "answer": q[1], "example": q[2],
                "source_sections": ["背景与主要改动", "核心公式", "与已有方法的关系", "结果、负控与边界"], "added": DATE})
            enrows[f"qa/{identity}/{qid}"] = {"question": q[3], "answer": q[4], "example": q[5]}
        questions[identity] = {"questions": qrows}
        units = question_units({identity: qrows})
        for uid, fields in enrows.items():
            translations[uid] = {"source_sha256": units[uid].source_sha256, "reviewed": True, "fields": fields}
        peer_identity = "post-training:"+c["peer"]
        peer = json.loads((ROOT / f"src/auto_research/paper_specs/catalog/post-training/{c['peer']}.json").read_text())
        source_revisions = {identity: digest(directory / "README.md"), peer_identity: digest(ROOT / "docs" / peer["detail_path"])}
        q = c["questions"][2]
        proposals.append({
            "paper": identity, "target_card": "post-training/"+c["topic"], "source_revisions": source_revisions,
            "comparison": {"position": c["scope"], "tradeoff": c["compare"], "sections": ["背景与主要改动", "与已有方法的关系", "结果、负控与边界"]},
            "analysis": {"title": q[0], "body": c["compare"]+" "+c["questions"][3][1], "papers": [identity, peer_identity]},
            "question": {"id": "nov19-"+key, "question": q[0], "answer": q[1], "example": q[2], "papers": [identity, peer_identity]},
            "update": {"date": DATE, "papers": [identity, peer_identity], "summary": c["scope"]+" 完整实验高成本不复现；组件或资料不构成能力晋级。"},
            "english": {
                "comparison": {"position": c["scope_en"], "tradeoff": c["compare_en"]},
                "analysis": {"title": q[3], "body": c["compare_en"]+" "+c["questions"][3][4]},
                "question": {"question": q[3], "answer": q[4], "example": q[5]},
                "update": c["scope_en"]+" The high-cost full experiment is not reproduced; components or references do not establish capability promotion.",
            },
        })
        reviews.append({"id": c["id"], "key": key, "title": title, "author": c["author"], "affiliation": c["affiliation"],
            "published_at": stamp, "announced_on": DATE, "reviewed_version": "v1", "source_url": source_url,
            "source_sha256": digest(CACHE / (c["id"]+"v1.html")), "pdf_sha256": digest(pdf),
            "sections": c["sections"], "gpu": c["gpu"], "tier": tier,
            "scope": c["scope"], "cost": c["cost"], "code": c.get("code"),
            "repository_status_before_batch": meta["repository_status"],
            "implementation_status": spec["implementation_status"], "review_done": True,
            "full_experiment_status": "not_reproduced_high_cost", "automatic_retry": False,
            "automatic_implementation_queue": False, "local_module": local, "english_source_sha256": digest(directory / "README.md")})
    write(ROOT / "docs/learning/questions/nov19-latest-post.json", {"schema_version": 1, "papers": questions})
    write(ROOT / "docs/en/learning/translations/qa-nov19-latest-post.json", {"schema_version": 1, "units": translations})
    write(AUDIT / "deep-dive-proposals-post.json", {"schema_version": 1, "reviewed_on": DATE, "integration_owner": "root", "proposals": proposals})
    write(AUDIT / "post-review.json", {"schema_version": 1, "reviewed_on": DATE, "owner": "nov19_post",
        "window": {"start": "2026-11-18", "end": DATE, "whole_end_day_claimed": False},
        "coverage": "Finite source-bound primary-method and cost selection from official metadata; not all-source exhaustion.",
        "google_meta_authorship": "None of these five fixed-v1 bylines has a Google/Meta first-author affiliation. ECA's PDF superscripts give UCAS/Tencent; model citations do not establish authorship.",
        "accepted": reviews})
    print("Authored five bilingual papers, four CPU diagnostics,20 reviewed bilingual questions and five deep-dive proposals.")


if __name__ == "__main__":
    main()
