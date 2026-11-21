"""Close only the fixed affordable overlap intake, without advancing a watermark."""

from __future__ import annotations

import hashlib
import json
import posixpath
import re

from PIL import Image

from english_learning_sources import deep_dive_units, question_units
from oct18_frozen_sources import verify_sources
from run_nov21_latest_components import AUDIT, BATCH, ROOT, config, load, source_hashes, validate_raw


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
        if {row["level"] for row in rows} != {"basics", "mechanism", "comparison", "implementation"}:
            raise ValueError("four authored levels required")
    units, english = question_units(questions), {}
    for path in (ROOT / "docs/en/learning/translations").glob("qa-nov21-latest-*.json"):
        for key, value in load(path)["units"].items():
            if key in english:
                raise ValueError("duplicate English question unit")
            english[key] = value
    if set(english) != set(units) or len(units) != len(expected) * 4:
        raise ValueError("four exact authored bilingual questions per selected paper required")
    reviewed(english, units)
    proposals = [row for name in ("foundation", "agent", "post")
                 for row in load(AUDIT / f"deep-dive-proposals-{name}.json")["proposals"]]
    banks = {p.stem: load(p) for p in (ROOT / "docs/learning/deep-dives").glob("*.json")}
    selected = {}
    for row in proposals:
        theme, topic = row["target_card"].split("/", 1)
        record = banks[theme]["topics"][topic]
        selected[row["target_card"]] = record
        # A new paper may also be a comparison peer in another new update.
        # Require this exact authored update once, not once as any reference.
        expected_update = row["update"] | {"source_revisions": {
            key: row["source_revisions"][key] for key in row["update"]["papers"]}}
        matches = [x for x in record["updates"] if x == expected_update]
        if row["paper"] not in record["reviewed_papers"] or len(matches) != 1:
            raise ValueError("missing/duplicate dated deep-dive update")
    dive = load(ROOT / "docs/en/learning/translations/dive-nov21-latest.json")["units"]
    all_units = deep_dive_units(selected)
    if len(dive) != len(expected) * 4 or not set(dive) <= set(all_units):
        raise ValueError("four exact reviewed deep-dive units per selected paper required")
    reviewed(dive, {key: all_units[key] for key in dive})
    return {"authored_bilingual_questions": len(units), "same_topic_deep_dive_updates": len(proposals)}


def prepare_coverage():
    cache = ROOT / ".cache/nov21-latest"
    api = load(cache / "metadata-pool.json")
    bulletin = load(cache / "announcement-pool.json")
    previous = load(ROOT / "docs/research-audits/nov20-latest/metadata-index.json")
    priority = load(AUDIT / "priority-source-captures.json")
    initial_priority = load(AUDIT / "priority-source-captures-initial.json")
    previous_announcements = set(previous["announced_identities"])
    since_start = [row for row in api["papers"] if row["published"][:10] >= api["requested_window"]["start"]]
    dump(AUDIT / "metadata-index.json", {
        "schema_version": 1, "metadata_only": True, "captured_at": api["captured_at"],
        "requested_window": api["requested_window"], "overlap_start_utc": api["overlap_start_utc"],
        "categories": api["categories"], "all_sources_exhaustive": False,
        "coverage_complete_to_overlap_boundary": api["coverage_complete_to_overlap_boundary"],
        "metadata_inventory_is_implementation_backlog": False, "receipts": api["receipts"],
        "identities": [{key: row.get(key) for key in ("canonical_id", "title", "published", "updated", "repository_status")}
                       for row in api["papers"]],
        "announcement_receipts": bulletin["receipts"], "announced_identities": bulletin["identities"],
    })
    counts = {"metadata_identities": len(api["papers"]), "announcement_identities": len(bulletin["identities"]),
              "first_releases_since_requested_start": len(since_start),
              "announcement_identity_delta_from_previous_batch": len(set(bulletin["identities"]) - previous_announcements)}
    dump(AUDIT / "source-coverage.json", {
        "schema_version": 1, "reviewed_on": "2026-11-21", "window": api["requested_window"], **counts,
        "metadata_only_inventory": "metadata-index.json", "fixed_intake": "intake-scope.json",
        "primary_priority_review": "priority-primary-selection.json", "all_sources_exhaustive": False,
        "watermark_advanced": False,
        "priority_directory_transport_exceptions": sum(row.get("status") == "source_exception_archived" for row in priority["pages"]),
        "priority_directory_parse_complete": sum(row.get("parse_complete") is True for row in priority["pages"]),
        "google_directory_comparison_complete": priority["google_directory_delta"]["comparison_complete"],
        "repository_event_queries": len(priority["repository_events"]),
        "capture_repair": {"initial_receipt": "priority-source-captures-initial.json",
                           "initial_receipt_sha256": hashlib.sha256((AUDIT / "priority-source-captures-initial.json").read_bytes()).hexdigest(),
                           "initial_nonempty_parsed_pages": sum(bool(row.get("links")) for row in initial_priority["pages"]),
                           "repair": "Decode transport gzip, retain original raw hashes and bytes, and reparse cached responses without a network retry. Incomplete Google directories do not imply baseline papers were removed."},
        "coverage_limits": [
            "The current official bulletins are still datedNov20. No Nov20/21 first release was verified in this captured nine-category pool, not a claim that no new paper exists anywhere.",
            "Six selected papers come from the previous announcement overlap: five first appearedNov19 and MV-JEPA first appearedNov18. Meta MemLife is a Sep30 historical backfill surfaced by official repository events. None is newly published today.",
            "Recall counts and unseen metadata are not an implementation backlog or a full-method review claim.",
            "Google/Meta are prioritized, but membership, familiar author names, upcoming catalog years and repository pushes are not proof of fixed-version affiliation or publication date.",
            "Meta whole-page policy improvement explicitly reports offline estimates, not quantified productionA/B; it is not admitted by silently weakening the recommendation selection gate.",
            "Unavailable or incomplete official directories remain archived source exceptions, not evidence that no Google/Meta work exists.",
        ],
    })
    return counts


def main():
    from curate_nov21_latest_evidence import main as curate
    curate()
    coverage = prepare_coverage()
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
        if (spec.get("promotion_eligible") is not False or spec.get("evolve_integrated") is not False
                or spec.get("full_experiment_status") != "not_reproduced_high_cost"):
            raise ValueError("diagnostic/full-campaign boundaries changed")
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
                "original_caption": provenance.get("caption", ""), "source_url": provenance.get("source_url", spec["paper_url"]),
                "extraction": "original_source_reviewed", "asset": image.relative_to(ROOT).as_posix(),
                "width": width, "height": height, "score": 0, "error": "", "asset_sha256": image_hash}
        figures = [x for x in figures if x["page"] != frow["page"]] + [frow]
        rows.append(spec | {"id": aid, "status": "implemented", "resolution": "bounded_component_accepted",
                            "reason": spec["summary"], "component_implemented": True, "full_capability_reproduced": False,
                            "doc": spec["detail_path"], "review_scope": "selected_primary_method_and_cost_review",
                            "intake_class": "historical_official_repository_backfill" if spec["published"] < "2026-11-18" else "overlap_new_selection"})
    items = config()["components"]
    counts.update(accepted_papers=len(rows), low_cost_components=len(items), cuda_components=sum(x["cuda"] for x in items.values()),
                  high_cost_review_only=0, full_capability_reproductions=0, new_first_releases=0,
                  overlap_new_selections=sum(x["published"] >= "2026-11-18" for x in rows),
                  first_published_nov19=sum(x["published"] == "2026-11-19" for x in rows),
                  first_published_nov18=sum(x["published"] == "2026-11-18" for x in rows),
                  historical_backfill=sum(x["published"] < "2026-11-18" for x in rows))
    scope = intake | {"selected_scope_complete": True, "delivery_status": "fixed_scope_complete",
                      "counts": counts, "papers": rows, "source_commit": frozen["commit"]}
    dump(AUDIT / "task-scope.json", scope)
    dump(ROOT / "docs/paper-figures-manifest.json", figures)
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = load(ledger_path)
    ledger["batches"] = [x for x in ledger["batches"] if x.get("batch") != BATCH]
    ledger["batches"].append({key: value for key, value in scope.items() if key != "papers"} | {"candidates": rows})
    dump(ledger_path, ledger)
    cn = ["# 11月21日增量扫描与重叠窗口选题", "", "[English](../../en/research-audits/nov21-latest/README.md)", "",
          "本轮7篇：旧公告池新选题6篇（5篇11月19日首发、MV-JEPA为11月18日首发），另补录官方仓库事件带出的Meta MemLife（9月30日首发）；都不是今天新发表。官方公告仍停在11月20日，本轮捕获元数据中没有核到11月20—21日首发。", "",
          "## 范围与证据", "",
          f"{coverage['metadata_identities']}条重叠元数据、{coverage['announcement_identities']}条公告只是召回池；公告身份相较上批新增{coverage['announcement_identity_delta_from_previous_batch']}条，不是待实现积压。有限选题不代表全来源穷尽，全库审查水位保持11月15日。", "",
          "Google/Meta优先核对。Meta whole-page ranking正文明确其工业收益是离线referee估计、A100时间是批摊销而非线上延迟，没有核到量化生产A/B，因此不在此悄悄放宽搜广推门槛。Google Duplex新博客不是独立公开算法论文；不可用页面保留为来源例外。", "",
          "官方目录的56次抓取中54次为来源例外；另2份DeepMind响应原本为gzip，已保留原字节和初始回执后离线重解析。Google目录不能完整比较，未观察到的旧链接不记成已移除。官方仓库事件只是线索，不能把push日当论文首发。", "",
          "交付7个低成本L1组件；CPU三种子执行全部7项，真实A100验证MV-JEPA一项。完整训练/生成/生产系统实验均为成本过高不复现（审查DONE），不自动重试。本地不是完整模型或Agent能力复现，也不作为Evolve晋级证据。ForeSpark已有高成本终态，本轮不因仓库push自动重开。", "",
          "[覆盖](source-coverage.json) · [优先核对](priority-primary-selection.json) · [任务账本](task-scope.json) · [运行预算](preflight.json) · [真实A100产物](raw-cuda.json)", "",
          "## 完整清单", "", "| 领域 | 论文 | 首发 | 本地交付 |", "| --- | --- | --- | --- |"]
    en = ["# November21 scan and overlapping selections", "", "[简体中文](../../../research-audits/nov21-latest/README.md)", "",
          "Seven selections: six from the previous bulletin pool (five first appeared on November19, and MV-JEPA on November18), plus Meta MemLife, a September30 historical backfill surfaced by official repository events. None was published today. Current bulletins remain dated November20; this metadata capture verified no November20–21 first release.", "",
          "## Scope and evidence", "",
          f"The {coverage['metadata_identities']} overlapping metadata records and {coverage['announcement_identities']} bulletin identities are recall pools. The bulletin identity delta is {coverage['announcement_identity_delta_from_previous_batch']}; none is an implementation-backlog count. This finite intake is not all-source exhaustion, and the review watermark stays at November15.", "",
          "Google/Meta received priority. Meta's whole-page ranking paper explicitly reports offline referee estimates; A100 timing is batch-amortized, not online latency. No quantified production A/B was verified, so the recommendation gate is not silently waived. Google's new Duplex blog does not independently specify a new public paper algorithm. Unavailable directories remain source exceptions.", "",
          "Of56 official-directory captures,54 are source exceptions. Two DeepMind responses were gzip-compressed; their original bytes and initial receipts were retained before offline reparsing. The Google directory comparison is incomplete, so unobserved baseline links are not labeled removed. Repository pushes are recall signals, never publication dates.", "",
          "Seven low-cost L1 components ran on CPU with three seeds; MV-JEPA additionally ran on a real A100. Full training, generation campaigns and production-system experiments are high-cost, not reproduced, review DONE, with no automatic retry. Component evidence is not complete model/agent capability or Evolve promotion. ForeSpark's existing terminal high-cost review was not reopened merely because its repository was pushed.", "",
          "## Complete list", "", "| Domain | Paper | First publication | Local delivery |", "| --- | --- | --- | --- |"]
    for row in rows:
        rel = posixpath.relpath(row["detail_path"], "research-audits/nov21-latest")
        cn.append(f"| {row['domain']} | [{row['title']}]({rel}) | {row['published']} | {row['evaluation_tier']} |")
        en.append(f"| {row['domain']} | [{row['title']}](../{rel.replace('README.md', 'README-en.md')}) | {row['published']} | {row['evaluation_tier']} |")
    chinese = "\n".join(cn) + "\n"
    (AUDIT / "README.md").write_text(chinese)
    target = ROOT / "docs/en/research-audits/nov21-latest/README.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("<!-- source-sha256: " + hashlib.sha256(chinese.encode()).hexdigest() + " -->\n" + "\n".join(en) + "\n")
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
