"""Close only the explicit eleven-paper selection, not the full recall window."""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
from collections import Counter

from PIL import Image
from oct18_frozen_sources import verify_sources
from run_nov26_latest_components import AUDIT, BATCH, ROOT, config, load, source_hashes, validate_raw

GROUPS = ("foundation", "agent", "post", "root")
DATE = "2026-11-26"


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n")


def proposed():
    rows=[]
    for group in GROUPS:
        value=load(AUDIT/f"paper-proposals-{group}.json")["papers"]
        rows.extend(value.values() if isinstance(value, dict) else value)
    expected=set(load(AUDIT/"intake-scope.json")["accepted_papers"])
    if {r["domain"]+":"+r["key"] for r in rows} != expected or len(rows) != len(expected):
        raise ValueError("authored scope differs from accepted finite selection")
    return rows


def prepare():
    for row in proposed():
        path=ROOT/f"src/auto_research/paper_specs/catalog/{row['domain']}/{row['key']}.json"
        row.setdefault("announced_on",None)
        row.setdefault("discovered_on",DATE)
        row.setdefault("reviewed_on",DATE)
        if path.exists() and load(path) != row:
            raise ValueError("refusing to overwrite installed spec: "+str(path))
        if not path.exists():
            dump(path,row)
    print("Installed eleven authored specs; not a completion claim.")


def coverage():
    cache=ROOT/".cache/nov26-latest"
    api, bulletin=load(cache/"metadata-pool.json"),load(cache/"announcement-pool.json")
    previous=load(ROOT/"docs/research-audits/nov25-latest/metadata-index.json")
    priority=load(cache/"priority-audit/priority-source-captures.json")
    dump(AUDIT/"priority-source-captures.json",priority)
    dump(AUDIT/"metadata-index.json",{
        "schema_version":1,"metadata_only":True,"captured_at":api["captured_at"],
        "requested_window":api["requested_window"],"overlap_start_utc":api["overlap_start_utc"],
        "categories":api["categories"],"all_sources_exhaustive":False,
        "coverage_complete_to_overlap_boundary":api["coverage_complete_to_overlap_boundary"],
        "metadata_inventory_is_implementation_backlog":False,"receipts":api["receipts"],
        "identities":[{k:r.get(k) for k in ("canonical_id","title","published","updated","repository_status")} for r in api["papers"]],
        "announcement_receipts":bulletin["receipts"],"announced_identities":bulletin["identities"]})
    old={r["canonical_id"] for r in previous["identities"]}
    fresh=[r for r in api["papers"] if r["canonical_id"] not in old]
    recent=Counter(r["published"][:10] for r in fresh if r["published"][:10]>=api["overlap_start_utc"][:10])
    value={"schema_version":1,"reviewed_on":DATE,"window":api["requested_window"],
        "metadata_identities":len(api["papers"]),"announcement_identities":len(bulletin["identities"]),
        "new_metadata_identities_relative_to_nov25_capture":len(fresh),
        "newly_captured_recent_first_releases_by_date":dict(sorted(recent.items())),
        "first_releases_in_requested_window":sum(api["requested_window"]["start"]<=r["published"][:10]<=api["requested_window"]["end"] for r in api["papers"]),
        "latest_original_publication_observed":max(r["published"] for r in api["papers"]),
        "announcement_dates_observed":sorted({r["announced_on"] for r in bulletin["receipts"]}),
        "announcement_identity_delta_from_previous_batch":len(set(bulletin["identities"])-set(previous["announced_identities"])),
        "official_directory_pages":len(priority["pages"]),"parse_complete_pages":sum(r.get("parse_complete") is True for r in priority["pages"]),
        "repository_event_queries":len(priority["repository_events"]),"all_sources_exhaustive":False,"watermark_advanced":False,
        "metadata_coverage_complete_to_overlap_boundary":api["coverage_complete_to_overlap_boundary"],
        "metadata_transport_exceptions":[r for r in api["receipts"] if r.get("transport_complete") is not True],
        "review_watermark_unchanged":"2026-11-15","primary_priority_review":"priority-primary-selection.json",
        "limits":["First submission, revision, announcement, discovery and review dates are distinct.",
        "Current bulletin is datedNov26 and includes all eleven selected identities; announcement dates are verified independently of original v1 publication dates.",
        "Recent overlap startsNov24; HTTP429 interrupted recall before the overlap boundary; this finite selection does not close the outstanding full window sinceNov15.",
        "Recall pools and repository events are not newly qualified papers or an implementation backlog.",
        "Google directory differences use the finiteNov15 baseline, not a daily publication count.",
        "Two incomplete Meta landing pages do not demonstrate absence of new Meta work."]}
    dump(AUDIT/"source-coverage.json",value)
    return value


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare",action="store_true")
    args=parser.parse_args()
    if args.prepare:
        prepare()
        return
    frozen=load(AUDIT/"frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("executed source drift")
    verify_sources(ROOT,frozen["commit"],frozen["source_sha256"],frozen["proof"])
    for device in ("cpu","cuda"):
        validate_raw(load(AUDIT/f"raw-{device}.json"),frozen)
    scope=load(AUDIT/"intake-scope.json")
    components=set(scope["component_papers"])
    figures=load(ROOT/"docs/paper-figures-manifest.json")
    questions={}
    for group in GROUPS:
        questions.update(load(AUDIT/f"{group}-authored-bundle.json")["papers"])
    if set(questions)!=set(scope["accepted_papers"]):
        raise ValueError("missing authored questions")
    rows=[]
    for proposal in proposed():
        identity=proposal["domain"]+":"+proposal["key"]
        row=load(ROOT/f"src/auto_research/paper_specs/catalog/{proposal['domain']}/{proposal['key']}.json")
        page=ROOT/"docs"/row["detail_path"]
        sha=hashlib.sha256(page.read_bytes()).hexdigest()
        if f"<!-- source-sha256: {sha} -->" not in page.with_name("README-en.md").read_text():
            raise ValueError("stale English: "+identity)
        if len(questions[identity]["questions"])!=4 or row.get("evolve_integrated") is not False or row.get("full_experiment_status") not in {"not_reproduced_high_cost", "not_run_scope_limited"}:
            raise ValueError("missing question/cost boundary: "+identity)
        for token in ("<!-- paper-figure:start -->", "### 原论文关键图", "assets/paper-figure-01.png",
                      "图片来自[原论文]", "版权归原作者所有", "<!-- paper-figure:end -->"):
            if token not in page.read_text():
                raise ValueError("missing figure contract: "+identity+" "+token)
        asset=page.parent/"assets/paper-figure-01.png"
        provenance=load(asset.with_name("provenance.json"))
        if "figures" in provenance:
            provenance=next(x for x in provenance["figures"] if x["file"]==asset.name)
        image_sha=hashlib.sha256(asset.read_bytes()).hexdigest()
        if image_sha not in {provenance.get("asset_sha256"),provenance.get("image_sha256"),provenance.get("sha256")}:
            raise ValueError("figure source drift")
        w,h=Image.open(asset).size
        aid=re.search(r"\d{4}\.\d{4,5}",row["paper_url"]).group()
        figure={"page":page.relative_to(ROOT).as_posix(),"paper_url":row["paper_url"],"arxiv_id":aid,
            "figure":provenance.get("figure",provenance.get("figure_label","Original figure")),"original_caption":provenance.get("caption",""),
            "source_url":provenance.get("source_url",row["paper_url"]),"extraction":"original_source_reviewed",
            "asset":asset.relative_to(ROOT).as_posix(),"width":w,"height":h,"score":0,"error":"","asset_sha256":image_sha}
        figures=[x for x in figures if x["page"]!=figure["page"]]+[figure]
        component=identity in components
        if not component and "不复现（审查 DONE）" not in row.get("deferral_reason", ""):
            raise ValueError("review-only paper lacks terminal cost reason: "+identity)
        rows.append(row|{"id":aid,"status":"implemented" if component else "deferred",
            "resolution":"bounded_component_accepted" if component else "not_reproduced_high_cost",
            "reason":row["summary"],"component_implemented":component,"full_capability_reproduced":False,
            "doc":row["detail_path"],"review_scope":"selected_primary_method_and_cost_review"})
    counts={"accepted_papers":len(rows),"low_cost_components":len(components),"cuda_components":sum(x["cuda"] for x in config()["components"].values()),
        "high_cost_review_only":len(rows)-len(components),"authored_bilingual_questions":len(rows)*4,
        "same_topic_deep_dive_updates":len(rows),"full_capability_reproductions":0,
        "l1_mechanism_components":sum(x["evaluation_tier"]=="l1_mechanism" for x in config()["components"].values()),
        "l0_interfaces":sum(x["evaluation_tier"]=="l0_interface" for x in config()["components"].values()),
        "first_publications_by_date":dict(sorted(Counter(r["published"] for r in rows).items()))}
    scope|={"selected_scope_complete":True,"delivery_status":"fixed_scope_complete","counts":counts,"papers":rows,"source_commit":frozen["commit"]}
    dump(AUDIT/"task-scope.json",scope)
    dump(ROOT/"docs/paper-figures-manifest.json",figures)
    ledger=load(ROOT/"docs/paper-discovery-ledger.json")
    ledger["batches"]=[b for b in ledger["batches"] if b.get("batch")!=BATCH]+[{k:v for k,v in scope.items() if k!="papers"}|{"candidates":rows}]
    dump(ROOT/"docs/paper-discovery-ledger.json",ledger)
    cov=coverage()
    cn=["# 11月26日近期论文增量选题","","[English](../../en/research-audits/nov26-latest/README.md)","",
        "本轮11篇均为11月25日首发，不是11篇今天新发。低成本交付为RAP、DuoMI、BRIAR、FEAST、HoMe、OneQuery、CAMAR七个L1机制组件及DualPM一个L0回调接口；JEPA EU、CARE-OPD、Agentic LongLive三篇高成本仅收录。OneQuery/CAMAR均核对正文生产A/B，作者线上结果与本地小组件分开。","",
        f"本轮官方重叠池{cov['metadata_identities']}条、当前公告{cov['announcement_identities']}个身份仅作召回；相对上一批新捕获近期首发分布为{cov['newly_captured_recent_first_releases_by_date']}，不是合格论文数量或实现积压。日期口径见覆盖记录，不推定选题公告日。有限选题不等于全窗口审查闭环，水位仍11月15日。","",
        "八个组件/接口完成CPU三seed，CAMAR另有真实单A100三seed。RAP核心CPU实验本身可负担，本轮未执行其完整公开评测矩阵，标not_run_scope_limited而非伪造高成本；其余已评估为高成本的完整训练/API矩阵终态不复现（审查DONE），无自动重试。没有checkpoint/训练数据下载、API调用、完整能力复现或Evolve晋级。","",
        "Google/Meta优先目录与仓库核验见优先来源记录：新Google博客对应已有FUSE，旧论文释码/普通维护不当新论文；SCALE4D官方技术报告单列原文成本审查与首次公开日期限制，不把submit号当正式arXiv身份。","",
        "[范围](task-scope.json) · [覆盖](source-coverage.json) · [优先来源](priority-primary-selection.json) · [预算](preflight.json) · [CPU](raw-cpu.json) · [GPU](raw-cuda.json)","",
        "## 完整清单","","| 领域 | 论文 | 首发 | 交付 |","| --- | --- | --- | --- |"]
    en=["# November26 incremental paper selection","","[简体中文](../../../research-audits/nov26-latest/README.md)","",
        "All eleven selected papers first appeared November25, not eleven releases today. Delivery comprises seven L1 components(RAP, DuoMI, BRIAR, FEAST, HoMe, OneQuery, CAMAR), one L0 callback interface(DualPM), and three high-cost review-only entries(JEPA EU, CARE-OPD, Agentic LongLive). OneQuery/CAMAR full-text production A/B results are distinguished from local component evidence.","",
        f"The {cov['metadata_identities']} metadata identities and {cov['announcement_identities']} current bulletin identities are recall pools. Newly captured recent first-release dates relative to the previous batch are {cov['newly_captured_recent_first_releases_by_date']}, not qualified-paper counts or an implementation backlog. Coverage records distinguish dates; selected announcement dates are not guessed. This finite selection does not close the full window; the watermark remains November15.","",
        "Eight components/interfaces completed CPU three-seed diagnostics, and CAMAR additionally ran on one real A100. RAP's core CPU experiments are affordable but its complete public evaluation matrix was outside this intake; it is not_run_scope_limited, not falsely cost-deferred. Other full campaigns assessed as expensive are terminally not reproduced(review DONE), without retries. No checkpoints/training data downloads, APIs, full capability reproduction or Evolve promotion.","",
        "Google/Meta priority records distinguish the new Google blog for already-cataloged FUSE from new papers, and historical code releases from maintenance. The official SCALE4D report has a separate primary cost review and first-publication-date limitation; an arXiv submission placeholder is not a public arXiv identity.","",
        "## Complete list","","| Domain | Paper | Original publication | Delivery |","| --- | --- | --- | --- |"]
    for row in rows:
        rel=posixpath.relpath(row["detail_path"],"research-audits/nov26-latest")
        cn.append(f"| {row['domain']} | [{row['title']}]({rel}) | {row['published']} | {(('L0接口' if row['evaluation_tier']=='l0_interface' else 'L1组件') if row['component_implemented'] else '高成本不复现')} |")
        en.append(f"| {row['domain']} | [{row['title']}](../{rel.replace('README.md','README-en.md')}) | {row['published']} | {(('L0 interface' if row['evaluation_tier']=='l0_interface' else 'L1 component') if row['component_implemented'] else 'High cost, not reproduced')} |")
    chinese="\n".join(cn)+"\n"
    (AUDIT/"README.md").write_text(chinese)
    target=ROOT/"docs/en/research-audits/nov26-latest/README.md"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text("<!-- source-sha256: "+hashlib.sha256(chinese.encode()).hexdigest()+" -->\n"+"\n".join(en)+"\n")
    print(json.dumps(counts))


if __name__=="__main__":
    main()
