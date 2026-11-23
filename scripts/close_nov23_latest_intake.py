"""Close the explicit nine-paper intake, never a full-window census."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
from pathlib import Path

from PIL import Image

from oct18_frozen_sources import verify_sources
from run_nov23_latest_components import AUDIT, BATCH, ROOT, config, load, source_hashes, validate_raw

GROUPS = ("foundation", "agent", "post", "root")
DATE = "2026-11-23"


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n")


def proposed():
    rows = []
    for group in GROUPS:
        data = load(AUDIT/f"paper-proposals-{group}.json")["papers"]
        rows += list(data.values()) if isinstance(data, dict) else data
    expected = set(load(AUDIT/"intake-scope.json")["accepted_papers"])
    if {r["domain"]+":"+r["key"] for r in rows} != expected or len(rows) != len(expected):
        raise ValueError("authored selection scope changed")
    return rows


def prepare():
    for row in proposed():
        path = ROOT/"src/auto_research/paper_specs/catalog"/row["domain"]/(row["key"]+".json")
        row.setdefault("announced_on", None)
        row.setdefault("discovered_on", DATE)
        row.setdefault("reviewed_on", DATE)
        if path.exists():
            previous = load(path)
            if previous != row:
                raise ValueError("refusing to overwrite installed spec/evidence: "+str(path))
        else:
            dump(path, row)
    print("Installed exactly nine authored specs; no completion claim.")


def coverage():
    cache = ROOT/".cache/nov23-latest"
    api, bulletin = load(cache/"metadata-pool.json"), load(cache/"announcement-pool.json")
    previous = load(ROOT/"docs/research-audits/nov21-latest/metadata-index.json")
    priority = load(cache/"priority-audit/priority-source-captures.json")
    dump(AUDIT/"priority-source-captures.json", priority)
    dump(AUDIT/"metadata-index.json", {
        "schema_version":1,"metadata_only":True,"captured_at":api["captured_at"],
        "requested_window":api["requested_window"],"overlap_start_utc":api["overlap_start_utc"],
        "categories":api["categories"],"all_sources_exhaustive":False,
        "coverage_complete_to_overlap_boundary":api["coverage_complete_to_overlap_boundary"],
        "metadata_inventory_is_implementation_backlog":False,"receipts":api["receipts"],
        "identities":[{k:r.get(k) for k in ("canonical_id","title","published","updated","repository_status")} for r in api["papers"]],
        "announcement_receipts":bulletin["receipts"],"announced_identities":bulletin["identities"]})
    old = {r["canonical_id"] for r in previous["identities"]}
    fresh = [r for r in api["papers"] if r["canonical_id"] not in old and r["published"][:10] >= "2026-11-20"]
    value = {"schema_version":1,"reviewed_on":DATE,"window":api["requested_window"],
        "metadata_identities":len(api["papers"]),"announcement_identities":len(bulletin["identities"]),
        "newly_captured_first_releases_since_previous_capture":len(fresh),
        "first_releases_in_requested_window":sum(r["published"][:10]>=api["requested_window"]["start"] for r in api["papers"]),
        "announcement_identity_delta_from_previous_batch":len(set(bulletin["identities"])-set(previous["announced_identities"])),
        "official_directory_pages":len(priority["pages"]),"parse_complete_pages":sum(r.get("parse_complete") is True for r in priority["pages"]),
        "repository_event_queries":len(priority["repository_events"]),"all_sources_exhaustive":False,"watermark_advanced":False,
        "review_watermark_unchanged":"2026-11-15","primary_priority_review":"priority-primary-selection.json",
        "limits":["Nov20 first releases were newly captured onNov23; they are not Nov23 publications.",
                  "Bulletins still dateNov20 and do not establish announcement dates for metadata-only selections.",
                  "This is a finite selection, not full-method review of1260 records or an implementation backlog.",
                  "Directory differences compare finite inventories againstNov15, not first publication dates or global deletion.",
                  "Two Meta landing pages lack a complete parsed publication inventory; this is not evidence of zero new Meta work.",
                  "Google/Meta bylines, original dates and full-text/official code are verified for selected papers; source-only leads with no full algorithm remain archived limitations, not invented implementations."]}
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
        raise ValueError("frozen source drift")
    verify_sources(ROOT,frozen["commit"],frozen["source_sha256"],frozen["proof"])
    for device in ("cpu","cuda"):
        validate_raw(load(AUDIT/f"raw-{device}.json"),frozen)
    scope=load(AUDIT/"intake-scope.json")
    components=set(scope["component_papers"])
    figures=load(ROOT/"docs/paper-figures-manifest.json")
    rows=[]
    questions={}
    for group in GROUPS:
        questions.update(load(AUDIT/f"{group}-authored-bundle.json")["papers"])
    if set(questions)!=set(scope["accepted_papers"]):
        raise ValueError("missing authored paper questions")
    for proposed_row in proposed():
        identity=proposed_row["domain"]+":"+proposed_row["key"]
        row=load(ROOT/"src/auto_research/paper_specs/catalog"/proposed_row["domain"]/(proposed_row["key"]+".json"))
        path=ROOT/"docs"/row["detail_path"]
        sha=hashlib.sha256(path.read_bytes()).hexdigest()
        if f"<!-- source-sha256: {sha} -->" not in path.with_name("README-en.md").read_text():
            raise ValueError("English source drift: "+identity)
        if row.get("evolve_integrated") is not False or row.get("full_experiment_status")!="not_reproduced_high_cost":
            raise ValueError("wrong cost/capability boundary")
        if len(questions[identity]["questions"])!=4:
            raise ValueError("four reviewed question levels required")
        asset=path.parent/"assets/paper-figure-01.png"
        provenance=load(asset.with_name("provenance.json"))
        if "figures" in provenance:
            provenance=next(x for x in provenance["figures"] if x["file"]==asset.name)
        image_sha=hashlib.sha256(asset.read_bytes()).hexdigest()
        if image_sha not in {provenance.get("asset_sha256"),provenance.get("image_sha256"),provenance.get("sha256")}:
            raise ValueError("figure source drift")
        w,h=Image.open(asset).size
        aid=re.search(r"\d{4}\.\d{4,5}",row["paper_url"]).group()
        figure={"page":path.relative_to(ROOT).as_posix(),"paper_url":row["paper_url"],"arxiv_id":aid,
            "figure":provenance.get("figure",provenance.get("figure_label","Original figure")),"original_caption":provenance.get("caption",""),
            "source_url":provenance.get("source_url",row["paper_url"]),"extraction":"original_source_reviewed",
            "asset":asset.relative_to(ROOT).as_posix(),"width":w,"height":h,"score":0,"error":"","asset_sha256":image_sha}
        figures=[x for x in figures if x["page"]!=figure["page"]]+[figure]
        component=identity in components
        rows.append(row|{"id":aid,"status":"implemented" if component else "deferred",
            "resolution":"bounded_component_accepted" if component else "not_reproduced_high_cost",
            "reason":row["summary"],"component_implemented":component,"full_capability_reproduced":False,
            "doc":row["detail_path"],"review_scope":"selected_primary_method_and_cost_review"})
    counts={"accepted_papers":len(rows),"low_cost_components":len(components),"cuda_components":1,"high_cost_review_only":2,
            "authored_bilingual_questions":len(rows)*4,"same_topic_deep_dive_updates":len(rows),"full_capability_reproductions":0,
            "first_published_nov20":sum(r["published"]=="2026-11-20" for r in rows),"historical_backfill":sum(r["published"]<"2026-11-20" for r in rows)}
    scope |= {"selected_scope_complete":True,"delivery_status":"fixed_scope_complete","counts":counts,"papers":rows,"source_commit":frozen["commit"]}
    dump(AUDIT/"task-scope.json",scope)
    dump(ROOT/"docs/paper-figures-manifest.json",figures)
    ledger=load(ROOT/"docs/paper-discovery-ledger.json")
    ledger["batches"]=[b for b in ledger["batches"] if b.get("batch")!=BATCH]+[{k:v for k,v in scope.items() if k!="papers"}|{"candidates":rows}]
    dump(ROOT/"docs/paper-discovery-ledger.json",ledger)
    cov=coverage()
    cn=["# 11月23日近期论文与Google目录补录","","[English](../../en/research-audits/nov23-latest/README.md)","",
        "本轮9篇：8篇11月20日首发、本次相较11月21日元数据新捕获；另有Google合作的SPOT-Bench，4月27日首发、核对11月5日v2的历史目录补录。不是11月23日新发9篇。","",
        "## 范围与证据","",f"官方重叠池{cov['metadata_identities']}条、旧公告{cov['announcement_identities']}个身份只作召回；本次核到160条11月20日首发，未核到11月21—23日首发，公告身份新增0。提交、修订、公告、发现和审查日期分开，不猜新选题公告日。有限选题不是全来源审查，水位保持11月15日。","",
        "Google DeepMind DISCO优先收录；SPOT按固定v2一作NUS、Yale Song署名Google，不因官方目录调换一作。官方目录54/56页面完成链接解析，两份Meta落地页缺少完整出版清单。14条Google目录增量是对Nov15有限目录的差，不是14篇新首发；SearchInject/LogAct等已有条目不因push重开。缺全文的硬件AI线索作为来源限制归档。","",
        "交付7个L1机制/计分组件，全部CPU三seed，AIMuon另有真实A100三seed；没有下载模型/数据或调用API。CTRL与CoEvoBench只收录，高成本完整实验不复现（审查DONE），不是待跑TODO。其余7篇的完整能力实验同样不复现；机制负控与合成分数不等于论文benchmark，不接Evolve晋级。","",
        "[任务范围](task-scope.json) · [覆盖](source-coverage.json) · [优先来源](priority-primary-selection.json) · [预算](preflight.json) · [CPU实跑](raw-cpu.json) · [A100实跑](raw-cuda.json)","",
        "## 完整清单","","| 领域 | 论文 | 首发 | 交付 |","| --- | --- | --- | --- |"]
    en=["# November23 paper intake and Google-directory backfill","","[简体中文](../../../research-audits/nov23-latest/README.md)","",
        "Nine papers: eight first appearedNovember20 and were newly captured relative toNovember21, plus SPOT-Bench, an April27 historical backfill from Google's directory, reviewingNovember5v2. These are not nine November23 publications.","",
        "## Scope and evidence","",f"The {cov['metadata_identities']} overlapping metadata records and{cov['announcement_identities']} old bulletin identities are recall pools. This capture found160 November20 first releases, none verified fromNovember21–23, and zero added bulletin identities. Submission, revision, announcement, discovery and review are separate; announcement dates are not guessed. This finite intake is not all-source review, and the watermark remainsNovember15.","",
        "Google DeepMind DISCO received priority. SPOT's fixed-v2 first author is at NUS and Yale Song at Google; directory ordering does not replace the byline. Link parsing completed for54/56 official pages; two Meta landing pages lack a complete publication inventory. Fourteen Google additions compare finite inventories againstNovember15, not first releases. Existing SearchInject/LogAct records are not reopened merely for pushes. Hardware-AI leads lacking full methods are archived source limitations.","",
        "Seven L1 mechanism/scoring components ran on CPU with three seeds, and AIMuon additionally on a real A100. No model/data downloads or APIs were used. CTRL and CoEvoBench are review-only: high-cost full experiments not reproduced, review DONE, not pending jobs. Full capability campaigns for the seven components are also not reproduced. Synthetic controls and scores are not paper benchmarks or Evolve promotion.","",
        "## Complete list","","| Domain | Paper | First publication | Delivery |","| --- | --- | --- | --- |"]
    for row in rows:
        rel=posixpath.relpath(row["detail_path"],"research-audits/nov23-latest")
        label="L1组件" if row["component_implemented"] else "高成本不复现"
        cn.append(f"| {row['domain']} | [{row['title']}]({rel}) | {row['published']} | {label} |")
        en.append(f"| {row['domain']} | [{row['title']}](../{rel.replace('README.md','README-en.md')}) | {row['published']} | {'L1 component' if row['component_implemented'] else 'High cost, not reproduced'} |")
    chinese="\n".join(cn)+"\n"
    (AUDIT/"README.md").write_text(chinese)
    target=ROOT/"docs/en/research-audits/nov23-latest/README.md"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text("<!-- source-sha256: "+hashlib.sha256(chinese.encode()).hexdigest()+" -->\n"+"\n".join(en)+"\n")
    print(json.dumps(counts))


if __name__=="__main__":
    main()
