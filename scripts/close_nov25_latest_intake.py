"""Close only the explicit nine-paper selection, not the full recall window."""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
from collections import Counter

from PIL import Image
from oct18_frozen_sources import verify_sources
from run_nov25_latest_components import AUDIT, BATCH, ROOT, config, load, source_hashes, validate_raw

GROUPS = ("foundation", "agent", "post", "root")
DATE = "2026-11-25"


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
    print("Installed nine authored specs; not a completion claim.")


def coverage():
    cache=ROOT/".cache/nov25-latest"
    api, bulletin=load(cache/"metadata-pool.json"),load(cache/"announcement-pool.json")
    previous=load(ROOT/"docs/research-audits/nov24-latest/metadata-index.json")
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
        "new_metadata_identities_relative_to_nov24_capture":len(fresh),
        "newly_captured_recent_first_releases_by_date":dict(sorted(recent.items())),
        "first_releases_in_requested_window":sum(api["requested_window"]["start"]<=r["published"][:10]<=api["requested_window"]["end"] for r in api["papers"]),
        "latest_original_publication_observed":max(r["published"] for r in api["papers"]),
        "announcement_dates_observed":sorted({r["announced_on"] for r in bulletin["receipts"]}),
        "announcement_identity_delta_from_previous_batch":len(set(bulletin["identities"])-set(previous["announced_identities"])),
        "official_directory_pages":len(priority["pages"]),"parse_complete_pages":sum(r.get("parse_complete") is True for r in priority["pages"]),
        "repository_event_queries":len(priority["repository_events"]),"all_sources_exhaustive":False,"watermark_advanced":False,
        "review_watermark_unchanged":"2026-11-15","primary_priority_review":"priority-primary-selection.json",
        "limits":["First submission, revision, announcement, discovery and review dates are distinct.",
        "Current bulletin is datedNov24 and does not establish announcement dates for selected metadata-only papers.",
        "Recent overlap startsNov23; this finite selection does not close the outstanding full window sinceNov15.",
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
        if len(questions[identity]["questions"])!=4 or row.get("evolve_integrated") is not False or row.get("full_experiment_status")!="not_reproduced_high_cost":
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
        "first_publications_by_date":dict(sorted(Counter(r["published"] for r in rows).items()))}
    scope|={"selected_scope_complete":True,"delivery_status":"fixed_scope_complete","counts":counts,"papers":rows,"source_commit":frozen["commit"]}
    dump(AUDIT/"task-scope.json",scope)
    dump(ROOT/"docs/paper-figures-manifest.json",figures)
    ledger=load(ROOT/"docs/paper-discovery-ledger.json")
    ledger["batches"]=[b for b in ledger["batches"] if b.get("batch")!=BATCH]+[{k:v for k,v in scope.items() if k!="papers"}|{"candidates":rows}]
    dump(ROOT/"docs/paper-discovery-ledger.json",ledger)
    cov=coverage()
    cn=["# 11月25日近期论文增量选题","","[English](../../en/research-audits/nov25-latest/README.md)","",
        "本轮9篇均为11月24日首发、11月25日选题交付，不是9篇今天新发：LazUnirec、LARF、UDVR、Thresholded LongCE、EPRO、Agent-Kernel、CAPE、CriticJEPA、RecurSciBench。前两篇有正文生产A/B；Google/Meta官方新增线索、旧论文和仓库release另作优先核验，不把开仓/push日期当新论文。","",
        f"官方重叠池{cov['metadata_identities']}条、11月24日公告{cov['announcement_identities']}个身份仅作召回。相对Nov24批次，新捕获近期首发分布为{cov['newly_captured_recent_first_releases_by_date']}，不是合格论文数量或实现积压。未观察到11月25日首发；不猜本轮选题公告日。有限增量不等于全窗口审查闭环，审查水位仍11月15日。","",
        "7个L1局部机制/协议组件完成CPU三seed；LazUnirec另有真实单A100三seed。CriticJEPA与RecurSciBench仅资料收录。所有高成本完整矩阵均不复现（审查DONE），无自动重试。没有checkpoint/数据下载、API调用、完整模型/Agent能力复现或Evolve晋级。CAPE小型诊断为求最优实际校准全20格，没有取得校准节省，负结果保留；不能套用论文速度收益。","",
        "[范围](task-scope.json) · [覆盖](source-coverage.json) · [优先来源](priority-primary-selection.json) · [预算](preflight.json) · [CPU](raw-cpu.json) · [GPU](raw-cuda.json)","",
        "## 完整清单","","| 领域 | 论文 | 首发 | 交付 |","| --- | --- | --- | --- |"]
    en=["# November25 incremental paper selection","","[简体中文](../../../research-audits/nov25-latest/README.md)","",
        "All nine selected papers first appearedNovember24 and are delivered in thisNovember25 intake, not nine releases today: LazUnirec, LARF, UDVR, Thresholded LongCE, EPRO, Agent-Kernel, CAPE, CriticJEPA and RecurSciBench. The first two have full-text production A/B evidence. Google/Meta source additions, historical identities and repository releases are audited separately; creation/push dates are not paper dates.","",
        f"The{cov['metadata_identities']} metadata records and{cov['announcement_identities']} November24 bulletin identities are recall pools. Newly captured recent first releases relative to theNovember24 batch are{cov['newly_captured_recent_first_releases_by_date']}, not counts of qualifying papers or a backlog. NoNovember25 first release was observed, and announcement dates for this selection are not guessed. This finite intake does not close the full review window; the watermark remainsNovember15.","",
        "Seven L1 operator/protocol components completed CPU three-seed diagnostics; LazUnirec also ran on one real A100. CriticJEPA and RecurSciBench are review-only. All costly full campaigns are not reproduced (review DONE), without retries. No checkpoint/data downloads, APIs, full model/agent capability reproduction or Evolve promotion. CAPE's tiny optimum diagnostic actually calibrated all20 cells and saved no calibration calls; that negative result is retained rather than borrowing the paper's speed gains.","",
        "## Complete list","","| Domain | Paper | Original publication | Delivery |","| --- | --- | --- | --- |"]
    for row in rows:
        rel=posixpath.relpath(row["detail_path"],"research-audits/nov25-latest")
        cn.append(f"| {row['domain']} | [{row['title']}]({rel}) | {row['published']} | {'L1组件' if row['component_implemented'] else '高成本不复现'} |")
        en.append(f"| {row['domain']} | [{row['title']}](../{rel.replace('README.md','README-en.md')}) | {row['published']} | {'L1 component' if row['component_implemented'] else 'High cost, not reproduced'} |")
    chinese="\n".join(cn)+"\n"
    (AUDIT/"README.md").write_text(chinese)
    target=ROOT/"docs/en/research-audits/nov25-latest/README.md"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text("<!-- source-sha256: "+hashlib.sha256(chinese.encode()).hexdigest()+" -->\n"+"\n".join(en)+"\n")
    print(json.dumps(counts))


if __name__=="__main__":
    main()
