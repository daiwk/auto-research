"""Verify finite delivery, bind figures/learning, and append one audit observation."""

from __future__ import annotations
import hashlib
import json
import posixpath
import re
from PIL import Image
from english_learning_sources import deep_dive_units, question_units
from curate_nov18_latest_evidence import main as curate_main
from run_nov18_latest_components import (
    ROOT,
    AUDIT,
    BATCH,
    config,
    load,
    source_hashes,
    validate_raw,
)
from oct18_frozen_sources import verify_sources


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def reviewed(payload, units):
    if set(payload) != set(units):
        raise ValueError("authored reviewed English scope differs")
    for key, unit in units.items():
        row = payload[key]
        if (
            row.get("reviewed") is not True
            or row.get("source_sha256") != unit.source_sha256
            or set(row.get("fields", {})) != set(unit.fields)
            or any(
                not isinstance(t, str) or not t.strip() or re.search(r"[\u3400-\u9fff]", t)
                for t in row["fields"].values()
            )
        ):
            raise ValueError("unreviewed/stale English learning unit: " + key)


def learning_counts():
    questions = {}
    english = {}
    proposals = []
    for name in ("foundation", "post", "agent", "root"):
        bundle = load(ROOT / f"docs/learning/questions/nov18-latest-{name}.json")["papers"]
        overlay = load(ROOT / f"docs/en/learning/translations/qa-nov18-latest-{name}.json")["units"]
        if set(questions) & set(bundle) or set(english) & set(overlay):
            raise ValueError("duplicate learning paper/unit")
        questions.update({key: value["questions"] for key, value in bundle.items()})
        english.update(overlay)
        proposals.extend(load(AUDIT / f"deep-dive-proposals-{name}.json")["proposals"])
    expected = set(load(AUDIT / "intake-scope.json")["accepted_papers"])
    if (
        set(questions) != expected
        or len(proposals) != len(expected)
        or {p["paper"] for p in proposals} != expected
    ):
        raise ValueError("missing authored learning scope")
    if any(
        {q["level"] for q in rows} != {"basics", "mechanism", "comparison", "implementation"}
        for rows in questions.values()
    ):
        raise ValueError("all four learning levels required")
    reviewed(english, question_units(questions))
    dive_units = {}
    for p in proposals:
        theme, topic = p["target_card"].split("/", 1)
        membership = load(ROOT / f"docs/learning/topics/{theme}.json")
        members = next(t["papers"] for t in membership["topics"] if t["id"] == topic)
        record = load(ROOT / f"docs/learning/deep-dives/{theme}.json")["topics"][topic]
        update = p["update"] | {
            "source_revisions": {k: p["source_revisions"][k] for k in p["update"]["papers"]}
        }
        if (
            p["paper"] not in members
            or p["paper"] not in record["reviewed_papers"]
            or {"paper": p["paper"], **p["comparison"]} not in record["comparisons"]
            or p["analysis"] not in record["analysis"]
            or p["question"] not in record["questions"]
            or update not in record["updates"]
        ):
            raise ValueError("authored deep dive not actually integrated: " + p["paper"])
        keys = [
            f"dive/{p['target_card']}/comparison/{p['paper']}",
            f"dive/{p['target_card']}/analysis/{record['analysis'].index(p['analysis'])}",
            f"dive/{p['target_card']}/question/{p['question']['id']}",
            f"dive/{p['target_card']}/update/{update['date']}/{record['updates'].index(update)}",
        ]
        actual = deep_dive_units({p["target_card"]: record})
        dive_units.update({k: actual[k] for k in keys})
    reviewed(
        load(ROOT / "docs/en/learning/translations/dive-nov18-latest.json")["units"], dive_units
    )
    return {
        "authored_bilingual_questions": sum(map(len, questions.values())),
        "same_topic_deep_dive_updates": len(proposals),
    }


def main():
    frozen = load(AUDIT / "frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("execution source changed after actual run")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for device in ("cpu", "cuda"):
        validate_raw(load(AUDIT / f"raw-{device}.json"), frozen)
    intake = load(AUDIT / "intake-scope.json")
    learning = learning_counts()
    figures = load(ROOT / "docs/paper-figures-manifest.json")
    papers = []
    for identity in intake["accepted_papers"]:
        domain, key = identity.split(":", 1)
        spec = load(ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json")
        page = ROOT / "docs" / spec["detail_path"]
        en = page.with_name("README-en.md")
        fingerprint = hashlib.sha256(page.read_bytes()).hexdigest()
        if not en.exists() or f"<!-- source-sha256: {fingerprint} -->" not in en.read_text():
            raise ValueError("stale English paper: " + identity)
        if (
            spec.get("review_done") is not True
            or spec.get("automatic_implementation_queue") is not False
            or spec.get("evolve_integrated") is not False
            or spec.get("promotion_eligible") is not False
        ):
            raise ValueError("incomplete or overstated review: " + identity)
        component = identity in intake["component_papers"]
        if component:
            item = config()["components"][key]
            for device in ("cpu", "cuda") if item["cuda"] else ("cpu",):
                result = load(page.parent / f"metrics/component-{device}-seeds42-44.json")
                if (
                    result["provenance"]["commit"] != frozen["commit"]
                    or result["evaluation_tier"] != item["evaluation_tier"]
                ):
                    raise ValueError("wrong frozen component evidence: " + identity)
            if item["cuda"] and (
                spec.get("gpu_validation_passed") is not True
                or not (ROOT / spec["gpu_validation_artifact"]).is_file()
            ):
                raise ValueError("actual GPU acceptance missing: " + identity)
        elif spec.get("local_operator") or (page.parent / "metrics").exists():
            raise ValueError("review-only paper has pretend execution: " + identity)
        asset = page.parent / "assets/paper-figure-01.png"
        provenance = load(asset.with_name("provenance.json"))
        if "figures" in provenance:
            matches = [r for r in provenance["figures"] if r.get("file") == asset.name]
            if len(matches) != 1:
                raise ValueError("ambiguous original figure")
            provenance = matches[0]
        digest = hashlib.sha256(asset.read_bytes()).hexdigest()
        if digest not in {
            provenance.get("asset_sha256"),
            provenance.get("image_sha256"),
            provenance.get("sha256"),
        }:
            raise ValueError("figure source hash mismatch: " + identity)
        width, height = Image.open(asset).size
        figure = {
            "page": page.relative_to(ROOT).as_posix(),
            "paper_url": spec["paper_url"],
            "arxiv_id": re.search(r"\d{4}\.\d{4,5}", spec["paper_url"]).group(),
            "figure": str(
                provenance.get("figure", provenance.get("figure_label", "Original figure"))
            ),
            "original_caption": provenance.get("caption", ""),
            "source_url": provenance.get("source_url", provenance.get("url", spec["paper_url"])),
            "extraction": "original_source_reviewed",
            "asset": asset.relative_to(ROOT).as_posix(),
            "width": width,
            "height": height,
            "score": 0,
            "error": "",
            "asset_sha256": digest,
        }
        figures = [r for r in figures if r["page"] != figure["page"]] + [figure]
        papers.append(
            spec
            | {
                "id": figure["arxiv_id"],
                "status": "implemented" if component else "reviewed",
                "resolution": "bounded_component_accepted"
                if component
                else "not_reproduced_high_cost",
                "reason": spec["summary"],
                "component_implemented": component,
                "full_capability_reproduced": False,
                "doc": spec["detail_path"],
                "review_scope": "selected_primary_method_and_cost_review",
            }
        )
    counts = {
        "accepted_papers": len(papers),
        "new_papers": len(intake["new_papers"]),
        "historical_new_code": len(intake["historical_new_code"]),
        "low_cost_components": len(config()["components"]),
        "cuda_components": sum(r["cuda"] for r in config()["components"].values()),
        "high_cost_review_only": len(intake["review_only_papers"]),
        **learning,
        "full_capability_reproductions": 0,
    }
    scope = intake | {
        "selected_scope_complete": True,
        "delivery_status": "fixed_scope_complete",
        "counts": counts,
        "papers": papers,
        "source_commit": frozen["commit"],
        "superseded_run": "superseded-run.json",
    }
    dump(AUDIT / "task-scope.json", scope)
    dump(ROOT / "docs/paper-figures-manifest.json", figures)
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = load(ledger_path)
    ledger["batches"] = [r for r in ledger["batches"] if r.get("batch") != BATCH]
    ledger["batches"].append(
        {k: v for k, v in scope.items() if k != "papers"} | {"candidates": papers}
    )
    dump(ledger_path, ledger)
    cn = [
        "# 11月16–18日论文更新与交付",
        "",
        "[English](../../en/research-audits/nov18-latest/README.md)",
        "",
        f"本批{len(papers)}项：46篇区间内新论文，1篇旧论文新开源补录；35个低成本组件，12篇高成本仅收录。22个CUDA组件已在真实A100执行三种子验证。189道中英学习题、47条同主题深读更新。",
        "",
        "## 范围与证据",
        "",
        "这是有限选题扫描和交付，不是所有来源/所有论文的全文穷尽审查。3369条含11月13日起重叠、旧稿修订及跨类去重的元数据不是3369篇新论文，也不是待实现积压。本次不改全库审查水位。",
        "",
        "优先核对Google/Meta官方目录、公开仓库事件及固定原文作者栏。Meta VisHead-Spec已实现低成本算子；Google efficient_evals是11月16日新开源、3月2日首发旧论文，单独计补漏。KVUse等生产离线回放未被误当线上A/B。",
        "",
        "所有本地指标都是L0/L1诊断，不是模型能力、生产提升或Evolve晋级证据。高成本完整实验明确不复现，审查DONE，不自动重试。WM-Quant旧错误网格诊断被作废保留，修复后以新源码重新执行。",
        "",
        "来源与范围：[来源覆盖](source-coverage.json)、[Google/Meta原文选择](priority-primary-selection.json)、[完整交付账本](task-scope.json)、[成本预检](preflight.json)、[实际GPU结果](raw-cuda.json)。",
        "",
        "## 交付清单",
        "",
        "| 领域 | 论文 | 首发日期 | 本地交付 |",
        "| --- | --- | --- | --- |",
    ]
    en = [
        "# November16–18 paper refresh and delivery",
        "",
        "[简体中文](../../../research-audits/nov18-latest/README.md)",
        "",
        "47 items:46 papers first published in the window and1 historical paper with a new official code release;35 bounded components and12 review-only high-cost papers.22 CUDA components were executed on a real A100 with three seeds.189 bilingual questions and47 same-topic deep-dive updates.",
        "",
        "## Scope and evidence",
        "",
        "This is finite selection and delivery, not full-text exhaustion across every source/paper. The3369 metadata identities include November13 overlap, older revisions and cross-lists; they are neither3369 new papers nor an implementation backlog. The global review watermark is unchanged.",
        "",
        "Google/Meta official directories, public repository events and fixed-paper bylines were prioritized. Meta VisHead-Spec has bounded operators. Google efficient_evals was released on November16 for a March2 paper and is counted as historical new-code backfill. Offline production-derived replay, including KVUse, is not mislabeled production A/B.",
        "",
        "Local L0/L1 diagnostics establish neither model capability, production lift nor Evolve promotion. High-cost full experiments are explicitly not reproduced, review DONE, with no automatic retry. An incorrect WM-Quant grid diagnostic remains preserved as invalidated; corrected source was frozen and executed again.",
        "",
        "Sources: [coverage](../../../research-audits/nov18-latest/source-coverage.json), [Google/Meta primary selection](../../../research-audits/nov18-latest/priority-primary-selection.json), [delivery ledger](../../../research-audits/nov18-latest/task-scope.json), [cost preflight](../../../research-audits/nov18-latest/preflight.json), [actual CUDA run](../../../research-audits/nov18-latest/raw-cuda.json).",
        "",
        "## Delivery list",
        "",
        "| Domain | Paper | First publication | Local delivery |",
        "| --- | --- | --- | --- |",
    ]
    for p in papers:
        relative = posixpath.relpath(p["detail_path"], "research-audits/nov18-latest")
        status = p.get("evaluation_tier") if p["component_implemented"] else "高成本仅收录，不复现"
        cn.append(f"| {p['domain']} | [{p['title']}]({relative}) | {p['published']} | {status} |")
        en.append(
            f"| {p['domain']} | [{p['title']}](../{relative.replace('README.md', 'README-en.md')}) | {p['published']} | {p.get('evaluation_tier') if p['component_implemented'] else 'Review only; full campaign not reproduced'} |"
        )
    cn = "\n".join(cn) + "\n"
    (AUDIT / "README.md").write_text(cn)
    target = ROOT / "docs/en/research-audits/nov18-latest/README.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "<!-- source-sha256: "
        + hashlib.sha256(cn.encode()).hexdigest()
        + " -->\n"
        + "\n".join(en)
        + "\n"
    )
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
