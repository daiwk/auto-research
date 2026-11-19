"""Close exactly the reviewed Nov19 scope; never promote metadata to full review."""

from __future__ import annotations
import hashlib
import json
import posixpath
import re
from PIL import Image
from english_learning_sources import deep_dive_units, question_units
from curate_nov19_latest_evidence import main as curate_main
from run_nov19_latest_components import (
    AUDIT,
    ROOT,
    BATCH,
    config,
    load,
    source_hashes,
    validate_raw,
)
from oct18_frozen_sources import verify_sources


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def reviewed(translations, units):
    if set(translations) != set(units):
        raise ValueError("English unit scope differs")
    for key, unit in units.items():
        row = translations[key]
        if (
            row.get("reviewed") is not True
            or row.get("source_sha256") != unit.source_sha256
            or set(row.get("fields", {})) != set(unit.fields)
            or any(
                not isinstance(v, str) or not v.strip() or re.search(r"[\u3400-\u9fff]", v)
                for v in row["fields"].values()
            )
        ):
            raise ValueError("unreviewed/stale English: " + key)


def learning_counts(expected):
    questions, english, proposals = {}, {}, []
    for name in ("foundation", "post", "agent", "root"):
        bundle = load(ROOT / f"docs/learning/questions/nov19-latest-{name}.json")["papers"]
        overlay = load(ROOT / f"docs/en/learning/translations/qa-nov19-latest-{name}.json")["units"]
        if set(questions) & set(bundle) or set(english) & set(overlay):
            raise ValueError("duplicate paper/question")
        questions.update({k: v["questions"] for k, v in bundle.items()})
        english.update(overlay)
        proposals.extend(load(AUDIT / f"deep-dive-proposals-{name}.json")["proposals"])
    if (
        set(questions) != expected
        or len(proposals) != len(expected)
        or {p["paper"] for p in proposals} != expected
    ):
        raise ValueError("incomplete authored learning scope")
    if any(
        {q["level"] for q in rows} != {"basics", "mechanism", "comparison", "implementation"}
        for rows in questions.values()
    ):
        raise ValueError("four question levels required")
    reviewed(english, question_units(questions))
    units = {}
    for p in proposals:
        theme, topic = p["target_card"].split("/", 1)
        record = load(ROOT / f"docs/learning/deep-dives/{theme}.json")["topics"][topic]
        members = next(
            t["papers"]
            for t in load(ROOT / f"docs/learning/topics/{theme}.json")["topics"]
            if t["id"] == topic
        )
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
            raise ValueError("deep dive not integrated: " + p["paper"])
        actual = deep_dive_units({p["target_card"]: record})
        keys = [
            f"dive/{p['target_card']}/comparison/{p['paper']}",
            f"dive/{p['target_card']}/analysis/{record['analysis'].index(p['analysis'])}",
            f"dive/{p['target_card']}/question/{p['question']['id']}",
            f"dive/{p['target_card']}/update/{update['date']}/{record['updates'].index(update)}",
        ]
        units.update({k: actual[k] for k in keys})
    reviewed(load(ROOT / "docs/en/learning/translations/dive-nov19-latest.json")["units"], units)
    return {
        "authored_bilingual_questions": sum(map(len, questions.values())),
        "same_topic_deep_dive_updates": len(proposals),
    }


def main():
    curate_main()
    frozen = load(AUDIT / "frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("executed source changed")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for device in ("cpu", "cuda"):
        validate_raw(load(AUDIT / f"raw-{device}.json"), frozen)
    from run_nov19_egojev_cpu import hashes as extra_hashes, validate_raw as validate_extra

    extra = load(AUDIT / "frozen-egojev-sources.json")
    if extra_hashes() != extra["source_sha256"]:
        raise ValueError("supplemental CPU source changed")
    verify_sources(ROOT, extra["commit"], extra["source_sha256"], extra["proof"])
    validate_extra(load(AUDIT / "raw-egojev-cpu.json"), extra)
    intake = load(AUDIT / "intake-scope.json")
    learning = learning_counts(set(intake["accepted_papers"]))
    manifest = load(ROOT / "docs/paper-figures-manifest.json")
    papers = []
    for identity in intake["accepted_papers"]:
        path = ROOT / "src/auto_research/paper_specs/catalog" / f"{identity.replace(':', '/')}.json"
        spec = load(path)
        component = identity in intake["component_papers"]
        if not component:
            reason = spec.get("deferral_reason") or spec["summary"]
            if "不复现（审查 DONE）" not in reason:
                reason += " 成本过高，不复现（审查 DONE）；不自动重试。"
            spec["deferral_reason"] = reason
            dump(path, spec)
        page = ROOT / "docs" / spec["detail_path"]
        digest = hashlib.sha256(page.read_bytes()).hexdigest()
        if f"<!-- source-sha256: {digest} -->" not in page.with_name("README-en.md").read_text():
            raise ValueError("stale English paper: " + identity)
        if (
            spec.get("review_done") is not True
            or spec.get("automatic_implementation_queue") is not False
            or spec.get("promotion_eligible") is not False
            or spec.get("evolve_integrated") is not False
        ):
            raise ValueError("incomplete/overstated review: " + identity)
        if component:
            supplemental = identity == "system-one:egojev"
            item = (
                {"evaluation_tier": "l1_mechanism", "cuda": False}
                if supplemental
                else config()["components"][spec["key"]]
            )
            execution_frozen = extra if supplemental else frozen
            for device in ("cpu", "cuda") if item["cuda"] else ("cpu",):
                evidence = load(page.parent / f"metrics/component-{device}-seeds42-44.json")
                if (
                    evidence["provenance"]["commit"] != execution_frozen["commit"]
                    or evidence["evaluation_tier"] != item["evaluation_tier"]
                ):
                    raise ValueError("wrong execution binding")
            if item["cuda"] and (
                spec.get("gpu_validation_passed") is not True
                or not (ROOT / spec["gpu_validation_artifact"]).exists()
            ):
                raise ValueError("GPU gate not met")
        elif spec.get("local_operator") or (page.parent / "metrics").exists():
            raise ValueError("review-only paper has pretend execution")
        asset = page.parent / "assets/paper-figure-01.png"
        provenance = load(asset.with_name("provenance.json"))
        if "figures" in provenance:
            matching = [p for p in provenance["figures"] if p.get("file") == asset.name]
            if len(matching) != 1:
                raise ValueError("ambiguous original figure")
            provenance = matching[0]
        image_hash = hashlib.sha256(asset.read_bytes()).hexdigest()
        if image_hash not in {
            provenance.get("asset_sha256"),
            provenance.get("image_sha256"),
            provenance.get("sha256"),
        }:
            raise ValueError("original figure hash differs: " + identity)
        width, height = Image.open(asset).size
        row = {
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
            "asset_sha256": image_hash,
        }
        manifest = [p for p in manifest if p["page"] != row["page"]] + [row]
        papers.append(
            spec
            | {
                "id": row["arxiv_id"],
                "status": "implemented" if component else "deferred",
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
        "new_first_releases": len(intake["new_papers"]),
        "announcement_overlap_backfill": 1,
        "historical_directory_backfill": 1,
        "low_cost_components": len(intake["component_papers"]),
        "cuda_components": sum(p["cuda"] for p in config()["components"].values()),
        "high_cost_review_only": len(intake["review_only_papers"]),
        "full_capability_reproductions": 0,
        **learning,
    }
    scope = intake | {
        "selected_scope_complete": True,
        "delivery_status": "fixed_scope_complete",
        "counts": counts,
        "papers": papers,
        "source_commit": frozen["commit"],
        "supplemental_cpu_source_commit": extra["commit"],
    }
    dump(AUDIT / "task-scope.json", scope)
    dump(ROOT / "docs/paper-figures-manifest.json", manifest)
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = load(ledger_path)
    ledger["batches"] = [r for r in ledger["batches"] if r.get("batch") != BATCH]
    ledger["batches"].append(
        {k: v for k, v in scope.items() if k != "papers"} | {"candidates": papers}
    )
    dump(ledger_path, ledger)
    cn = [
        "# 11月19日论文扫描与交付",
        "",
        "[English](../../en/research-audits/nov19-latest/README.md)",
        "",
        "本轮23项：21篇11月18日新首发、1篇11月17日首发/今日公告补录的Meta AVM、1篇11月2日Google SearchInject历史目录补录。18个低成本组件/接口、5篇高成本仅收录；7个CUDA组件在真实A100完成42/43/44三种子验证。92道逐题校对中英问答、23条同主题深读更新。",
        "",
        "## 范围与证据",
        "",
        "这是有限选题扫描，不是全来源/全机构穷尽审查。2781条重叠元数据与1082条当前公告不是新增论文数，也不是实现待办。本轮不改变全库审查水位。论文首发、公告、目录新增和仓库push分开记录。",
        "",
        "Google/Meta优先：MLE Agents核对Meta作者栏和真实A/B，同时保留延迟护栏退化；AVM完整8M视频训练高成本不复现；SearchInject只证明检索暴露控制，不证明攻击成功下降。CWM作者当前为Brown/AMI与NYU/AMI，不凭熟悉姓名标Meta；X-split原文未列机构，不猜Yandex。",
        "",
        "本地均为L0/L1诊断，不是模型能力、线上收益或Evolve晋级。高成本完整实验明确成本过高，不复现（审查 DONE），不自动重试。交叉复核发现的ECA/MRPD掩码指数溢出已在冻结前修复并加入极端值负控。",
        "",
        "最终跨主题复核补入Jeveration、EgoJev和JEPA Dots。EgoJev的显式概率CPU后处理用独立冻结组执行；已完成的17组件主体和7个A100结果保持原样，不覆盖或冒充再次测量。新增两篇的完整生成/机器人训练仅收录、不复现。",
        "",
        "[来源覆盖](source-coverage.json) · [优先来源核对](priority-primary-selection.json) · [完整交付账本](task-scope.json) · [成本与执行预算](preflight.json) · [真实CUDA产物](raw-cuda.json)",
        "",
        "## 完整清单",
        "",
        "| 领域 | 论文 | 首发 | 本地交付 |",
        "| --- | --- | --- | --- |",
    ]
    en = [
        "# November19 paper scan and delivery",
        "",
        "[简体中文](../../../research-audits/nov19-latest/README.md)",
        "",
        "23 items: 21 first releases from November18, Meta AVM first published November17 and announced today, and historical November2 Google SearchInject newly observed in the directory. 18 bounded components/interfaces and5 review-only high-cost papers;7 CUDA components actually ran on an A100 with seeds42/43/44. 92 individually reviewed bilingual questions and23 same-topic deep-dive updates.",
        "",
        "## Scope and evidence",
        "",
        "This is finite selection, not all-source or institution-wide exhaustion.2781overlapping metadata identities and1082current bulletin identities are neither a count of new papers nor an implementation backlog. The global review watermark is unchanged. Publication, announcement, directory observation and repository pushes remain separate events.",
        "",
        "Google/Meta were prioritized. Meta MLE Agents includes verified production A/B and the adverse latency guardrail. The complete8M-video AVM campaign is not reproduced. SearchInject measures exposure, not attack-success reduction. CWM has Brown/AMI and NYU/AMI bylines, not an inferred Meta affiliation; X-split leaves institution unspecified rather than guessing Yandex.",
        "",
        "All local evidence is L0/L1diagnostic, not model capability, online lift or Evolve promotion. High-cost full experiments are explicitly not reproduced, review DONE, without automatic retries. Independent review caught masked exponential overflow in ECA/MRPD; the fix and extreme-value negative controls precede the frozen run.",
        "",
        "A final cross-topic review added Jeveration, EgoJev and JEPA Dots. EgoJev's explicit-probability CPU postprocessing has its own frozen execution group. The completed17-component primary group and7 A100 measurements remain unchanged, not overwritten or presented as new runs. The added full generation/robotics training campaigns are review-only and not reproduced.",
        "",
        "[Coverage](../../../research-audits/nov19-latest/source-coverage.json) · [Priority source review](../../../research-audits/nov19-latest/priority-primary-selection.json) · [Delivery ledger](../../../research-audits/nov19-latest/task-scope.json) · [Cost preflight](../../../research-audits/nov19-latest/preflight.json) · [Actual CUDA run](../../../research-audits/nov19-latest/raw-cuda.json)",
        "",
        "## Complete list",
        "",
        "| Domain | Paper | First publication | Local delivery |",
        "| --- | --- | --- | --- |",
    ]
    for p in papers:
        relative = posixpath.relpath(p["detail_path"], "research-audits/nov19-latest")
        status = p.get("evaluation_tier") if p["component_implemented"] else "高成本仅收录，不复现"
        cn.append(f"| {p['domain']} | [{p['title']}]({relative}) | {p['published']} | {status} |")
        english_status = (
            p.get("evaluation_tier")
            if p["component_implemented"]
            else "Review only; full campaign not reproduced"
        )
        en.append(
            f"| {p['domain']} | [{p['title']}](../{relative.replace('README.md', 'README-en.md')}) | {p['published']} | {english_status} |"
        )
    chinese = "\n".join(cn) + "\n"
    (AUDIT / "README.md").write_text(chinese)
    target = ROOT / "docs/en/research-audits/nov19-latest/README.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "<!-- source-sha256: "
        + hashlib.sha256(chinese.encode()).hexdigest()
        + " -->\n"
        + "\n".join(en)
        + "\n"
    )
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
