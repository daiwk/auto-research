"""Close the finite Nov20 intake only after evidence and bilingual learning pass."""

from __future__ import annotations

import hashlib
import json
import posixpath
import re
from pathlib import Path

from PIL import Image

from english_learning_sources import deep_dive_units, question_units
from oct18_frozen_sources import verify_sources
from run_nov20_latest_components import AUDIT, BATCH, ROOT, config, load, source_hashes, validate_raw


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def reviewed(translations, units):
    for key, unit in units.items():
        row = translations.get(key, {})
        if (row.get("reviewed") is not True or row.get("source_sha256") != unit.source_sha256
                or set(row.get("fields", {})) != set(unit.fields)):
            raise ValueError("stale/incomplete reviewed English unit: " + key)


def learning_counts(expected):
    questions = {}
    for path in (ROOT / "docs/learning/questions").glob("*.json"):
        for identity, value in load(path)["papers"].items():
            if identity in expected:
                if identity in questions:
                    raise ValueError("duplicate question bank identity")
                questions[identity] = value["questions"]
    if set(questions) != expected:
        raise ValueError("new paper question scope missing")
    for rows in questions.values():
        if {r["level"] for r in rows} != {"basics", "mechanism", "comparison", "implementation"}:
            raise ValueError("four authored levels required")
    units = question_units(questions)
    english = {}
    for path in (ROOT / "docs/en/learning/translations").glob("qa-nov20-latest-*.json"):
        for key, value in load(path)["units"].items():
            if key in english:
                raise ValueError("duplicate English question unit")
            english[key] = value
    if set(english) != set(units) or len(units) != 44:
        raise ValueError("expected44exact authored bilingual questions")
    reviewed(english, units)
    proposals = [x for name in ("foundation", "post", "agent", "root")
                 for x in load(AUDIT / f"deep-dive-proposals-{name}.json")["proposals"]]
    banks = {p.stem: load(p) for p in (ROOT / "docs/learning/deep-dives").glob("*.json")}
    selected = {}
    for row in proposals:
        theme, topic = row["target_card"].split("/", 1)
        record = banks[theme]["topics"][topic]
        selected[row["target_card"]] = record
        if row["paper"] not in record["reviewed_papers"]:
            raise ValueError("unreviewed deep-dive identity")
        matches = [x for x in record["updates"] if x["date"] == "2026-11-20" and row["paper"] in x["papers"]]
        if len(matches) != 1:
            raise ValueError("missing/duplicate dated deep-dive update")
    dive = load(ROOT / "docs/en/learning/translations/dive-nov20-latest.json")["units"]
    all_units = deep_dive_units(selected)
    if len(dive) != 44 or not set(dive) <= set(all_units):
        raise ValueError("expected44exact reviewed deep-dive units")
    reviewed(dive, {k: all_units[k] for k in dive})
    return {"authored_bilingual_questions": len(units), "same_topic_deep_dive_updates": len(proposals)}


def prepare_coverage():
    cache = ROOT / ".cache/nov20-latest"
    first = load(cache / "metadata-pool.json")
    api = load(cache / "retry/metadata-pool.json")
    bulletin = load(cache / "retry/announcement-pool.json")
    dump(AUDIT / "metadata-index.json", {
        "schema_version": 1, "metadata_only": True, "captured_at": api["captured_at"],
        "requested_window": api["requested_window"], "overlap_start_utc": api["overlap_start_utc"],
        "categories": api["categories"],
        "coverage_complete_to_overlap_boundary": api["coverage_complete_to_overlap_boundary"],
        "all_sources_exhaustive": False, "metadata_inventory_is_implementation_backlog": False,
        "initial_failed_api_receipts": first["receipts"], "receipts": api["receipts"],
        "identities": [{k: row.get(k) for k in ("canonical_id", "title", "published", "updated", "repository_status")}
                       for row in api["papers"]],
        "announcement_receipts": bulletin["receipts"], "announced_identities": bulletin["identities"],
    })
    dump(AUDIT / "source-coverage.json", {
        "schema_version": 1, "reviewed_on": "2026-11-20", "window": api["requested_window"],
        "metadata_identities": len(api["papers"]), "announcement_identities": len(bulletin["identities"]),
        "metadata_only_inventory": "metadata-index.json", "priority_source_captures": "priority-source-captures.json",
        "fixed_intake": "intake-scope.json", "all_sources_exhaustive": False, "watermark_advanced": False,
        "coverage_limits": [
            "Nine configured arXiv categories plus finite official directories/repository events, not every source or affiliation.",
            "571 initially new metadata identities first published since Nov19 are a selection pool, not an implementation backlog.",
            "The initial API failed. A missing capture directory also discarded subsequent bulletin writes; both failures are preserved. After the mkdir fix, the independent retry succeeded.",
            "Metadata recall and current bulletins do not establish full-text review. Only selected primary methods and explicit exclusions were reviewed.",
            "Unavailable Meta official pages are archived nonblocking exceptions, not evidence of no Meta work.",
            "BuggyMLE, GrepMem and VisAlloc are Nov18 first releases/Nov20 announcements. Canon first appeared Nov12; its current first-author affiliation is Allen-Zhu Research, with research execution at FAIR/Meta.",
        ],
    })
    current = load(AUDIT / "priority-source-captures.json")
    previous = load(ROOT / "docs/research-audits/nov19-latest/priority-source-captures.json")
    delta = set(current["google_directory_delta"]["added"]) - set(previous["google_directory_delta"]["added"])
    exclusions = []
    for row in current["added_details"]:
        if row["url"].removeprefix("https://research.google") not in delta:
            continue
        slug = row["url"].split("/pubs/", 1)[-1].strip("/")
        related = slug.startswith(("from-prompt-to-probe", "i-want-to-be-pushed"))
        exclusions.append({
            "source_url": row["url"], "source_sha256": row.get("sha256"),
            "review_scope": "official_title_and_abstract_only",
            "decision": "not_selected_this_finite_intake",
            "reason": ("LLM application/evaluation case study; the captured official page does not supply a separately specified executable core or accessible full-method artifact for this batch. This is not a claim of no value or full-text rejection."
                       if related else "Official abstract concerns hardware verification/DFT, general safe coding, or Bayesian time-series inference, outside the current LLM/recommendation/Agent method intake."),
            "automatic_retry": False, "automatic_implementation_queue": False,
        })
    dump(AUDIT / "priority-primary-selection.json", {
        "schema_version": 1, "reviewed_on": "2026-11-20", "all_sources_exhaustive": False,
        "priority_admissions": {
            "agent-research:buggymle-cci": "Fixedv1 first author Google Research/UIUC; CCI calibration interface only, no bug-injection campaign or 9B training.",
            "recommendation:fleet-feature-optimization": "Fixedv1 Meta first author and production A/B; preserve unnamed metric and missing traffic/CI details; deterministic component only.",
            "foundation-models:canon-layers-scale": "Historical Meta research-execution provenance and official facebookresearch code; current byline Allen-Zhu Research, not relabeled as current Meta affiliation.",
        },
        "important_attribution_limits": [
            "LSER online A/B did not enable LLM auxiliary features; offline9.6pp HR@10 is not relative lift or online LLM attribution.",
            "Antom overall37.88% loss reduction differs from phase-II same-budget chargeback28.28% and common-date26.09%; no CI is invented.",
            "GrepMem retains a growing original log and is not Codex disk compaction or a reader for this user's conversation.",
        ], "official_directory_delta_reviews": exclusions,
    })


def main():
    from curate_nov20_latest_evidence import main as curate
    curate()
    prepare_coverage()
    frozen = load(AUDIT / "frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("executed source drift")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for device in ("cpu", "cuda"):
        validate_raw(load(AUDIT / f"raw-{device}.json"), frozen)
    intake = load(AUDIT / "intake-scope.json")
    counts = learning_counts(set(intake["accepted_papers"]))
    figures = load(ROOT / "docs/paper-figures-manifest.json")
    rows = []
    for identity in intake["accepted_papers"]:
        spec = load(ROOT / "src/auto_research/paper_specs/catalog" / (identity.replace(":", "/") + ".json"))
        page = ROOT / "docs" / spec["detail_path"]
        digest = hashlib.sha256(page.read_bytes()).hexdigest()
        if f"<!-- source-sha256: {digest} -->" not in page.with_name("README-en.md").read_text():
            raise ValueError("stale reviewed English: " + identity)
        component = identity in intake["component_papers"]
        if spec.get("promotion_eligible") is not False or spec.get("evolve_integrated") is not False:
            raise ValueError("diagnostic/review-only promotion prohibited")
        if not component and (spec.get("local_operator") or (page.parent / "metrics").exists()):
            raise ValueError("review-only pretend implementation")
        image = page.parent / "assets/paper-figure-01.png"
        provenance = load(image.with_name("provenance.json"))
        if "figures" in provenance:
            provenance = next(x for x in provenance["figures"] if x["file"] == image.name)
        image_hash = hashlib.sha256(image.read_bytes()).hexdigest()
        if image_hash not in {provenance.get("asset_sha256"), provenance.get("image_sha256"), provenance.get("sha256")}:
            raise ValueError("figure hash mismatch")
        width, height = Image.open(image).size
        aid = re.search(r"\d{4}\.\d{4,5}", spec["paper_url"]).group()
        frow = {"page": page.relative_to(ROOT).as_posix(), "paper_url": spec["paper_url"], "arxiv_id": aid,
                "figure": str(provenance.get("figure", provenance.get("figure_label", "Original figure"))),
                "original_caption": provenance.get("caption", ""),
                "source_url": provenance.get("source_url", spec["paper_url"]), "extraction": "original_source_reviewed",
                "asset": image.relative_to(ROOT).as_posix(), "width": width, "height": height,
                "score": 0, "error": "", "asset_sha256": image_hash}
        figures = [x for x in figures if x["page"] != frow["page"]] + [frow]
        rows.append(spec | {"id": aid, "status": "implemented" if component else "deferred",
                            "resolution": "bounded_component_accepted" if component else "not_reproduced_high_cost",
                            "reason": spec["summary"], "component_implemented": component,
                            "full_capability_reproduced": False, "doc": spec["detail_path"],
                            "review_scope": "selected_primary_method_and_cost_review"})
    counts.update(accepted_papers=len(rows), low_cost_components=9, cuda_components=4,
                  high_cost_review_only=2, full_capability_reproductions=0,
                  new_first_releases=sum(x["published"] >= "2026-11-19" for x in rows),
                  announcement_overlap_backfill=sum(x["published"] == "2026-11-18" for x in rows),
                  historical_backfill=sum(x["published"] < "2026-11-18" for x in rows))
    scope = intake | {"selected_scope_complete": True, "delivery_status": "fixed_scope_complete",
                      "counts": counts, "papers": rows, "source_commit": frozen["commit"]}
    dump(AUDIT / "task-scope.json", scope)
    dump(ROOT / "docs/paper-figures-manifest.json", figures)
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = load(ledger_path)
    ledger["batches"] = [x for x in ledger["batches"] if x.get("batch") != BATCH]
    ledger["batches"].append({k: v for k, v in scope.items() if k != "papers"} | {"candidates": rows})
    dump(ledger_path, ledger)
    cn = ["# 11月20日论文扫描与交付", "", "[English](../../en/research-audits/nov20-latest/README.md)", "",
          "本轮11项：7篇11月19日首发、3篇11月18日首发/今日公告补录、1篇11月12日Canon历史补录。9个低成本组件/接口、2篇高成本仅收录；4个CUDA组件在真实A100完成42/43/44三种子验证。44道逐题校对中英问答和11条同主题深读更新。", "",
          "## 范围与证据", "",
          "1884条重叠元数据、1081条公告是召回池，不是新增论文或待办数量。仅对固定选题和显式排除做相应层级的原文核对，不宣称全来源穷尽；全库审查水位保持11月15日不变。首发、公告、目录观察和仓库push分开记录。", "",
          "Google BuggyMLE与Meta舰队特征优化优先核验；Canon当前一作机构为Allen-Zhu Research，FAIR/Meta是实验执行来源，不改写成当前Meta署名。LSER线上A/B未启用LLM辅助特征，不能把整体线上收益归给LLM。", "",
          "全部运行是L0/L1诊断，不是模型能力、线上收益或Evolve晋级。高成本完整实验明确不复现、审查DONE，不自动重试。VisAlloc半精度与HiSA无符号位置问题均在最终冻结前修复，早期未执行快照与旧独立CPU事实保留。GrepMem只是新组件的显式日志查询，不读取本机Codex记录，也不提供磁盘压缩。", "",
          "[覆盖](source-coverage.json) · [优先来源](priority-primary-selection.json) · [任务账本](task-scope.json) · [执行预算](preflight.json) · [真实A100产物](raw-cuda.json)", "",
          "## 完整清单", "", "| 领域 | 论文 | 首发 | 本地交付 |", "| --- | --- | --- | --- |"]
    en = ["# November20 paper scan and delivery", "", "[简体中文](../../../research-audits/nov20-latest/README.md)", "",
          "11 items:7 first releases from November19,3 November18 papers announced today, and1 historical November12 Canon paper. Nine bounded components/interfaces and2 review-only high-cost papers. Four CUDA components actually ran on an A100 with seeds42/43/44;44 individually reviewed bilingual questions and11 same-topic updates are included.", "",
          "## Scope and evidence", "",
          "The1884 overlapping metadata identities and1081 bulletin identities are recall pools, not counts of new papers or pending implementations. Primary review is limited to the fixed intake and explicit exclusions. This is not all-source exhaustion, and the global review watermark remains November15. Publication, announcement, directory observation and repository pushes remain distinct.", "",
          "Google BuggyMLE and Meta fleet feature optimization receive priority. Canon's current first-author affiliation is Allen-Zhu Research; FAIR/Meta describes experiment provenance, not a rewritten current byline. LSER's online A/B did not enable auxiliary LLM features, so whole-stack online gains cannot be attributed to them.", "",
          "All local runs are L0/L1 diagnostics, not model capability, online lift or Evolve promotion. High-cost full campaigns are not reproduced, review DONE, without automatic retry. VisAlloc half-precision and HiSA unsigned-position defects were fixed before the final freeze; the earlier unexecuted snapshot and prior independent CPU facts remain preserved. GrepMem operates on explicit component logs, not this user's Codex history, and is not disk compression.", "",
          "## Complete list", "", "| Domain | Paper | First publication | Local delivery |", "| --- | --- | --- | --- |"]
    for row in rows:
        rel = posixpath.relpath(row["detail_path"], "research-audits/nov20-latest")
        status = row["evaluation_tier"] if row["component_implemented"] else "高成本仅收录，不复现"
        cn.append(f"| {row['domain']} | [{row['title']}]({rel}) | {row['published']} | {status} |")
        status_en = row["evaluation_tier"] if row["component_implemented"] else "Review only; not reproduced"
        en.append(f"| {row['domain']} | [{row['title']}](../{rel.replace('README.md', 'README-en.md')}) | {row['published']} | {status_en} |")
    chinese = "\n".join(cn) + "\n"
    (AUDIT / "README.md").write_text(chinese)
    target = ROOT / "docs/en/research-audits/nov20-latest/README.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("<!-- source-sha256: " + hashlib.sha256(chinese.encode()).hexdigest() + " -->\n" + "\n".join(en) + "\n")
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
