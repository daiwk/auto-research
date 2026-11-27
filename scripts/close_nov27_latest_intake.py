"""Close this seven-paper selection, never silently advance the review watermark."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import posixpath
import re

from PIL import Image

from oct18_frozen_sources import verify_sources
from run_nov27_latest_components import AUDIT, BATCH, ROOT, config, load, source_hashes, validate_raw

DATE = "2026-11-27"
GROUPS = ("foundation", "post", "agent", "root")


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def proposed():
    rows = []
    for group in GROUPS:
        value = load(AUDIT / f"paper-proposals-{group}.json")["papers"]
        rows.extend(value.values() if isinstance(value, dict) else value)
    expected = set(load(AUDIT / "intake-scope.json")["accepted_papers"])
    if len(rows) != len(expected) or {r["domain"] + ":" + r["key"] for r in rows} != expected:
        raise ValueError("authored scope differs from accepted selection")
    return rows


def prepare():
    for row in proposed():
        path = ROOT / f"src/auto_research/paper_specs/catalog/{row['domain']}/{row['key']}.json"
        row.setdefault("announced_on", None)
        row.setdefault("discovered_on", DATE)
        row.setdefault("reviewed_on", DATE)
        if path.exists() and load(path) != row:
            raise ValueError("refusing to overwrite installed spec")
        if not path.exists():
            dump(path, row)
    print("Installed seven reviewed specs; no execution-completion claim.")


def coverage():
    cache = ROOT / ".cache/nov27-latest"
    api, bulletin = load(cache / "metadata-pool.json"), load(cache / "announcement-pool.json")
    previous = load(ROOT / "docs/research-audits/nov26-latest/metadata-index.json")
    priority = load(AUDIT / "priority-source-captures.json")
    old = {r["canonical_id"] for r in previous["identities"]}
    fresh = [r for r in api["papers"] if r["canonical_id"] not in old]
    dump(AUDIT / "metadata-index.json", {"schema_version": 1, "metadata_only": True,
        "captured_at": api["captured_at"], "requested_window": api["requested_window"],
        "overlap_start_utc": api["overlap_start_utc"], "categories": api["categories"],
        "coverage_complete_to_overlap_boundary": api["coverage_complete_to_overlap_boundary"],
        "all_sources_exhaustive": False, "metadata_inventory_is_implementation_backlog": False,
        "receipts": api["receipts"], "identities": [{k: r.get(k) for k in ("canonical_id", "title", "published", "updated", "repository_status")} for r in api["papers"]],
        "announcement_receipts": bulletin["receipts"], "announced_identities": bulletin["identities"]})
    values = {"schema_version": 1, "reviewed_on": DATE, "window": api["requested_window"],
        "metadata_identities": len(api["papers"]), "announcement_identities": len(bulletin["identities"]),
        "new_metadata_identities_relative_to_nov26_capture": len(fresh),
        "newly_captured_recent_first_releases_by_date": dict(sorted(Counter(r["published"][:10] for r in fresh if r["published"][:10] >= "2026-11-24").items())),
        "first_releases_in_requested_window": sum(api["requested_window"]["start"] <= r["published"][:10] <= api["requested_window"]["end"] for r in api["papers"]),
        "latest_original_publication_observed": max(r["published"] for r in api["papers"]),
        "announcement_dates_observed": sorted({r.get("announced_on") for r in bulletin["receipts"] if r.get("announced_on")}),
        "announcement_identity_delta_from_previous_batch": len(set(bulletin["identities"]) - set(previous["announced_identities"])),
        "official_directory_pages": len(priority["pages"]), "parse_complete_pages": sum(r.get("parse_complete") is True for r in priority["pages"]),
        "repository_event_queries": len(priority["repository_events"]),
        "metadata_coverage_complete_to_overlap_boundary": api["coverage_complete_to_overlap_boundary"],
        "all_sources_exhaustive": False, "watermark_advanced": False, "review_watermark_unchanged": "2026-11-15",
        "limits": ["Finite selection from overlapping first releases/revisions, not today's newly published paper count.",
            "API capture reachesNov24 overlap boundary; this is transport/metadata coverage, not per-paper method/selection closure.",
            "NoNovember26 original first release observed; bulletin remainsNovember26. Missing selected announcement dates stay null.",
            "Unselected metadata identities are a recall pool, not an unfinished implementation queue.",
            "Google directory delta is zero versusNov26; inherited15 URL additions versusNov15 are not15 new papers.",
            "Two incomplete Meta pages and bounded source scans prevent exhaustive-source claims."]}
    dump(AUDIT / "source-coverage.json", values)
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true")
    args = parser.parse_args()
    if args.prepare:
        prepare()
        return
    frozen = load(AUDIT / "frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("executed source drift")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for device in ("cpu", "cuda"):
        validate_raw(load(AUDIT / f"raw-{device}.json"), frozen)
    scope = load(AUDIT / "intake-scope.json")
    questions = {k: v for group in GROUPS for k, v in load(AUDIT / f"{group}-authored-bundle.json")["papers"].items()}
    figures = load(ROOT / "docs/paper-figures-manifest.json")
    rows = []
    for proposal in proposed():
        identity = proposal["domain"] + ":" + proposal["key"]
        row = load(ROOT / f"src/auto_research/paper_specs/catalog/{proposal['domain']}/{proposal['key']}.json")
        page = ROOT / "docs" / row["detail_path"]
        digest = hashlib.sha256(page.read_bytes()).hexdigest()
        if f"<!-- source-sha256: {digest} -->" not in page.with_name("README-en.md").read_text():
            raise ValueError("stale English: " + identity)
        if len(questions[identity]["questions"]) != 4 or row.get("evolve_integrated") is not False:
            raise ValueError("question/evidence boundary differs")
        if row.get("full_experiment_status") not in {"not_reproduced_high_cost", "not_run_scope_limited"}:
            raise ValueError("unrecorded complete-experiment scope")
        if (row["full_experiment_status"] == "not_run_scope_limited") != (row["full_experiment_review_done"] is False):
            raise ValueError("scope limitation incorrectly closed as high-cost")
        for token in ("<!-- paper-figure:start -->", "### 原论文关键图", "assets/paper-figure-01.png", "图片来自[原论文]", "版权归原作者所有", "<!-- paper-figure:end -->"):
            if token not in page.read_text():
                raise ValueError("figure contract missing: " + identity + " " + token)
        asset = page.parent / "assets/paper-figure-01.png"
        provenance = load(asset.with_name("provenance.json"))
        if "figures" in provenance:
            provenance = next(r for r in provenance["figures"] if r["file"] == asset.name)
        image_sha = hashlib.sha256(asset.read_bytes()).hexdigest()
        if image_sha not in {provenance.get("asset_sha256"), provenance.get("image_sha256"), provenance.get("sha256")}:
            raise ValueError("figure fingerprint differs")
        width, height = Image.open(asset).size
        aid = re.search(r"\d{4}\.\d{4,5}", row["paper_url"]).group()
        figure = {"page": page.relative_to(ROOT).as_posix(), "paper_url": row["paper_url"], "arxiv_id": aid,
            "figure": provenance.get("figure", provenance.get("figure_label", "Original figure")),
            "original_caption": provenance.get("caption", ""), "source_url": provenance.get("source_url", row["paper_url"]),
            "extraction": "original_source_reviewed", "asset": asset.relative_to(ROOT).as_posix(), "width": width, "height": height,
            "score": 0, "error": "", "asset_sha256": image_sha}
        figures = [x for x in figures if x["page"] != figure["page"]] + [figure]
        rows.append(row | {"id": aid, "status": "implemented", "resolution": "bounded_component_accepted",
            "reason": row["summary"], "component_implemented": True, "full_capability_reproduced": False,
            "doc": row["detail_path"], "review_scope": "selected_primary_method_and_cost_review"})
    counts = {"accepted_papers": len(rows), "low_cost_components": len(rows), "l1_mechanism_components": len(rows),
        "l0_interfaces": 0, "high_cost_review_only": 0, "cuda_components": sum(r["cuda"] for r in config()["components"].values()),
        "authored_bilingual_questions": len(rows) * 4, "same_topic_deep_dive_updates": len(rows), "full_capability_reproductions": 0,
        "full_experiments_terminal_high_cost": sum(r["full_experiment_status"] == "not_reproduced_high_cost" for r in rows),
        "full_experiments_scope_limited": sum(r["full_experiment_status"] == "not_run_scope_limited" for r in rows),
        "first_publications_by_date": dict(sorted(Counter(r["published"] for r in rows).items()))}
    scope |= {"selected_scope_complete": True, "delivery_status": "fixed_scope_complete", "counts": counts,
              "papers": rows, "source_commit": frozen["commit"]}
    dump(AUDIT / "task-scope.json", scope)
    dump(ROOT / "docs/paper-figures-manifest.json", figures)
    ledger = load(ROOT / "docs/paper-discovery-ledger.json")
    ledger["batches"] = [b for b in ledger["batches"] if b.get("batch") != BATCH] + [{k: v for k, v in scope.items() if k != "papers"} | {"candidates": rows}]
    dump(ROOT / "docs/paper-discovery-ledger.json", ledger)
    cov = coverage()
    cn = ["# 11月27日重叠池与版本补录", "", "[English](../../en/research-audits/nov27-latest/README.md)", "",
        "本轮7项不是7篇今天新发：5篇11月24日首发、1篇11月25日首发；ELBO-TDS最早2025年发表，本次由11月25日v2带出。7个L1机制组件，不是完整模型/Agent能力复现，均未接入Evolve晋级。", "",
        f"实际捕获{cov['metadata_identities']}条元数据和{cov['announcement_identities']}个公告身份；最新首发仍11月25日，公告仍11月26日，未观察到11月26日新首发。新增捕获不等于新增发表，API重叠边界抓全也不等于逐篇审查闭环。水位保持11月15日。", "",
        "Google/Meta优先核验：相对上一批Google目录新增0；Meta新JEP-AV仓库仅ComingSoon，未有可核方法/论文身份；Habitats是source-only框架，Psyre/COrigami及DISCO的维护/释码不伪称新论文。来源异常保留。", "",
        "所有组件完成CPU三seed，ELBO-TDS另有真实A100三seed。DeCo是CPU低精度数学仿真，不是A100原生FP4核/加速测试。Compute-aware完整公开模拟可能可负担，未承接完整范围，不硬标高成本；其余昂贵完整实验终态不复现（审查DONE）。0模型/训练数据下载、0模型API。", "",
        "[固定范围](task-scope.json) · [来源覆盖](source-coverage.json) · [优先主源](priority-primary-selection.json) · [CPU](raw-cpu.json) · [GPU](raw-cuda.json)", "",
        "## 完整清单", "", "| 领域 | 论文 | 首发 | 交付 |", "| --- | --- | --- | --- |"]
    en = ["# November27 overlap and revision intake", "", "[简体中文](../../../research-audits/nov27-latest/README.md)", "",
        "These are not seven releases today: five first appearedNovember24 and oneNovember25. ELBO-TDS originally appeared in2025; its November25 v2 prompted this intake. Seven L1 mechanisms do not reproduce full model/agent capability or qualify for Evolve promotion.", "",
        f"The actual capture contains{cov['metadata_identities']} metadata identities and{cov['announcement_identities']} bulletin identities. Latest observed first publication remainsNovember25 and bulletinNovember26; noNovember26 first release was observed. Newly captured is not newly published, and complete metadata overlap transport is not per-paper review closure. The watermark remainsNovember15.", "",
        "Google/Meta priority checks found zero added Google directory URLs versus the previous batch. Meta's new JEP-AV repository says only ComingSoon, without verified method/paper identity. Habitats remains a source-only framework; Psyre/COrigami/DISCO maintenance or source releases are not new papers. Source exceptions remain explicit.", "",
        "All components completed CPU three-seed diagnostics; ELBO-TDS additionally ran on a real A100. DeCo is CPU low-precision arithmetic simulation, not an A100-native FP4 kernel/speed test. The compute-aware paper's public simulation may be affordable but was not undertaken; it is scope-limited, not falsely cost-deferred. Other costly full campaigns are terminally not reproduced(review DONE). No checkpoint/training-data downloads or model APIs.", "",
        "## Complete list", "", "| Domain | Paper | Original publication | Delivery |", "| --- | --- | --- | --- |"]
    for row in rows:
        rel = posixpath.relpath(row["detail_path"], "research-audits/nov27-latest")
        cn.append(f"| {row['domain']} | [{row['title']}]({rel}) | {row['published']} | L1机制组件 |")
        en.append(f"| {row['domain']} | [{row['title']}](../{rel.replace('README.md', 'README-en.md')}) | {row['published']} | L1 mechanism |")
    chinese = "\n".join(cn) + "\n"
    (AUDIT / "README.md").write_text(chinese)
    target = ROOT / "docs/en/research-audits/nov27-latest/README.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"<!-- source-sha256: {hashlib.sha256(chinese.encode()).hexdigest()} -->\n" + "\n".join(en) + "\n")
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
