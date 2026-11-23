"""Record bounded official-directory/repository triage, not inferred papers."""

import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"docs/research-audits/nov23-latest"
CACHE=ROOT/".cache/nov23-latest"


def main():
    captures=json.loads((CACHE/"priority-audit/priority-source-captures.json").read_text())
    decisions=[]
    for row in captures["added_details"]:
        url=row["url"]
        if "dont-pause" in url:
            decision="selected_historical_directory_backfill"
            reason="Fixed arXiv2604.24317v2 byline is first-author NUS, Yale Song Google. OriginalApr27, revisionNov5, discoveredNov23; Algorithm1/Eq2 scorer accepted, no full streaming controller/benchmark."
        elif "searchinject" in url:
            decision="already_cataloged"
            reason="SearchInject was cataloged inNov19; finite directory difference againstNov15 does not reopen a completed selection."
        elif "beyond-the-structural-filter" in url or "from-prompt-to-probe" in url:
            decision="source_limitation_archived"
            reason="Read the official page including its extended method description. LLM-assisted proprietary SoC verification is potentially relevant, but the page supplies no independently accessible full technical paper/code/data link or verified original publication date. Do not invent an LLM/RTL implementation from a workflow paragraph; not a completed full-method review or a claim that no novel algorithm exists."
        else:
            decision="outside_this_finite_paper_intake"
            reason="Official page describes hardware/formal-verification/design-for-test, generic software safety, polyomino mathematics or time-series Bayesian inference, not a newly specified LLM/recommendation/post-training/agent/world-model method or public benchmark selected in this intake. This is source-page scope triage, not full-text method review."
        decisions.append({"source_url":url,"capture_sha256":row.get("sha256"),"parse_complete":row.get("parse_complete",False),
                          "reviewed_on":"2026-11-23","decision":decision,"reason":reason,"automatic_retry":False})
    repositories=[]
    for query in captures["repository_events"]:
        for item in query.get("items",[]):
            name=item["full_name"]
            reason="Repository activity is a recall signal, not a paper publication date; general tooling/domain libraries are not automatically catalog papers."
            decision="repository_event_only_not_a_new_paper"
            if name=="facebookresearch/parq":
                reason="Official README links arXiv2503.15748; official abstract verifies original2025-03-19T23:38:49Z with no later revision. A Nov22 repository push is not a2026/Nov23 first release. Historical method is not reviewed/implemented in this bounded fresh intake; do not claim it already reproduced."
                decision="outside_window_historical_identity_only"
            elif name=="facebookresearch/logact" or name=="facebookresearch/autoform-bot":
                reason="Existing LogAct/AutoformBench catalog identity; repository push alone does not establish a changed defining method or authorize reopening a terminal experiment."
                decision="existing_catalog_no_new_method_verified"
            elif name=="facebookresearch/lean_kernel_verify":
                reason="Read official README: compiler/Lean tool, case-input-specific proofs not general safety; public end-to-end frontends still require internal Buck2 monorepo. No standalone paper identity verified here, no claimed A100/Blackwell parity or integration. Archive source-only tooling lead; not a completed reproduction."
                decision="source_only_tooling_lead_archived"
            elif name=="google-deepmind/extract_frag_trees":
                reason="Official README describes a Java exporter of SIRIUS chemistry fragmentation trees, not a new LLM/world-model algorithm. No chemistry runtime download or reproduction."
                decision="outside_research_domain"
            repositories.append({"repository":name,"event":query["event"],"source_url":item["html_url"],
                "observed_pushed_at":item.get("pushed_at"),"observed_created_at":item.get("created_at"),"decision":decision,"reason":reason})
    data={"schema_version":1,"reviewed_on":"2026-11-23","all_sources_exhaustive":False,"watermark_advanced":False,
        "directory_baseline":"Nov15 finite Google inventory, not previous-publication time",
        "directory_comparison_complete":captures["google_directory_delta"]["comparison_complete"],
        "google_added_directory_urls":decisions,"repository_observations":repositories,
        "selected_priority_papers":[{"identity":"foundation-models:disco","priority":"P0","evidence":"Fixedv1 allsix authors Google DeepMind; originalNov20T04:25:13Z. Binary/unboosted statistical component only. Claimed upstream repository is unavailable; no fabricated code SHA."},
                                    {"identity":"foundation-models:spot-bench","priority":"P0","evidence":"Google directory and fixedv2 Google coauthor; first-author affiliation remains NUS. Apr27 historical backfill, not a Nov23 new publication."}],
        "source_exceptions":[{k:r.get(k) for k in ("url","http_status","sha256","capture","parse_complete","error_type")} for r in captures["pages"] if r.get("parse_complete") is not True],
        "notes":["Two incomplete Meta landing-page inventories cannot prove zero new Meta work.",
                 "The DeepMind selected publication directory is not an exhaustive chronological feed.",
                 "Google official source entries without an accessible full paper remain archived limitations, not invented implementations or blanket non-algorithm rejections.",
                 "No new qualifying industrial production-A/B method was verified in this finite intake; the earlier Meta whole-page ranking offline-only decision is not silently waived."]}
    data["raw_directory_receipt_sha256"]=hashlib.sha256((CACHE/"priority-audit/priority-source-captures.json").read_bytes()).hexdigest()
    (AUDIT/"priority-primary-selection.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"directory_decisions":len(decisions),"repository_observations":len(repositories),"selected_priority_papers":2}))


if __name__=="__main__":
    main()
