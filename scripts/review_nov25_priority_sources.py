"""Finite Google/Meta official-source audit; repository events are not papers."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"docs/research-audits/nov25-latest"
CACHE=ROOT/".cache/nov25-latest"


def load(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    captures=load(CACHE/"priority-audit/priority-source-captures.json")
    previous_path=ROOT/"docs/research-audits/nov24-latest/priority-primary-selection.json"
    previous=load(previous_path)
    prior={r["source_url"]:r for r in previous["google_added_directory_urls"]}
    decisions=[]
    for row in captures["added_details"]:
        new=row["url"] not in prior
        result={"source_url":row["url"],"capture_sha256":row.get("sha256"),
            "parse_complete":row.get("parse_complete",False),"reviewed_on":"2026-11-25",
            "automatic_retry":False,"is_new_directory_url_relative_to_nov24":new}
        if new:
            if "social-workers" not in row["url"]:
                raise ValueError("new official directory lead lacks authored review")
            result|={"decision":"extended_abstract_reviewed_full_materials_unverified_archived",
                "original_first_publication_date_verified":False,
                "paper_title":"I Want to Be Pushed, I Want to Grow: Enabling Social Workers to Design Evaluations of LLM Augmentation in Their Work",
                "published_primary_url":"https://ojs.aaai.org/index.php/AIES/article/download/43241/50801",
                "published_pdf_sha256":digest(CACHE/"social-workers.pdf"),"published_primary_pages_read":2,
                "first_author_affiliation":"Carnegie Mellon University","verified_priority_organizations":["Google Research"],
                "affiliation_evidence":"Published PDF: Anna Kawakami/CMU; coauthor Renee Shelby/Google Research. Google directory discovery does not replace the byline.",
                "reason":"Read the complete two-page AIES2026 extended abstract: eight workshops with19 workers,16 worker-authored evaluation cases and an LLM-judge rubric. The work does describe a benchmark; do not dismiss it as non-algorithmic from the abstract. The short publication does not release the executable rubric/cases or enough validation detail. Its linked extended Google Drive version was inaccessible via the web tool, so full-method/public-material availability remains unverified. Archive this precise source limitation, do not invent a scorer or claim full-method rejection.",
                "linked_extended_version":"https://drive.google.com/file/d/14afU70spaglF9Wbi-v3phVjqBs-4Hfi-/view?usp=sharing",
                "full_method_review_complete":False,"resolution":"source_limitation_archived_not_implementation_backlog"}
        else:
            result|={"decision":"carried_forward_finite_directory_triage",
                "previous_review":"nov24-latest/priority-primary-selection.json",
                "previous_decision":prior[row["url"]]["decision"],
                "reason":"Same finiteNov15-baseline directory difference previously triaged. Carry forward its disposition without nesting complete historical records or claiming a new paper/full-method review."}
        decisions.append(result)
    known={
        "facebookresearch/agentbox":("partial_infrastructure_release_existing_paper","Read official README: Meta FAIR container orchestrator originally built for AIRA2 and subsequently refactored, not release of the complete research/evolution pipeline. Linked arXiv2603.26499 is existing AIRA2, originalMarch27,2026, not aNovember25 first release. Do not relabel its null complete-paper-code field or reopen the high-cost campaign for a new repository creation."),
        "facebookresearch/GenIA":("existing_terminal_high_cost_not_reopened","Official README links historical2610.12388; existing ledger already records verified Meta collaboration, author code/license and terminal not-reproduced-high-cost. November memory/appearance optimization notes alone do not establish an affordable complete bounded campaign. No weights/render-stack probe or automatic reopening."),
        "facebookresearch/OpenApps":("historical_identity_only_not_new_publication","Official README links2511.20766, a2025 historical benchmark identity, with CPU Python app infrastructure. November2026 push is not its first publication. This recent-paper intake does not claim a full-method review, new implementation or rejection of the historical benchmark."),
        "facebookresearch/PrivacyGuard":("source_only_library_observation","Read official README: privacy-analysis library/attacks and LLM analysis utilities; no new standalone paper identity verified from this README in the finite intake. Do not invent a new paper date or run privacy attacks."),
        "google-deepmind/robotics-antigravity-plugin":("source_only_plugin_observation","Read official README: robotics agent/controller plugin, simulation and real-arm examples. No new standalone paper identity verified in the README; not a new algorithm inferred from repository activity. No robot operation, package installation or provider call."),
        "facebookresearch/autoform-bot":("existing_catalog_identity","Existing AutoformBot/AutoformBench; no changed defining method verified by the push."),
        "facebookresearch/atlas-lean":("existing_catalog_identity","Existing ATLAS/AutoformBot linked identity; a library push alone is not a new method."),
        "facebookresearch/logact":("existing_catalog_identity","Existing LogAct; preserve terminal decisions rather than reopen from a push."),
        "google-research/mseb":("carried_forward_source_only_library","PreviousNov24 README triage retained; no newly verified standalone paper from this library event."),
        "google-deepmind/reaf-sim":("carried_forward_source_only_library","PreviousNov24 simulation-library source observation retained; not a new paper date.")}
    files={"facebookresearch/GenIA":"GenIA-readme.json","facebookresearch/OpenApps":"OpenApps-readme.json",
        "facebookresearch/PrivacyGuard":"PrivacyGuard-readme.json","google-deepmind/robotics-antigravity-plugin":"robotics-antigravity-plugin-readme.json"}
    observations=[]
    for query in captures["repository_events"]:
        for item in query.get("items",[]):
            name=item["full_name"]
            decision,reason=known.get(name,("event_observed_not_full_method_reviewed","Bounded repository recall only. No standalone release/date/novel-method conclusion made for this general tooling/library event."))
            observations.append({"repository":name,"event":query["event"],"source_url":item["html_url"],
                "observed_created_at":item.get("created_at"),"observed_pushed_at":item.get("pushed_at"),
                "decision":decision,"reason":reason,"readme_capture_sha256":digest(CACHE/files[name]) if name in files else None})
    value={"schema_version":1,"reviewed_on":"2026-11-25","all_sources_exhaustive":False,"watermark_advanced":False,
        "directory_baseline":"Nov15 finite inventory, not first-publication dates",
        "raw_directory_receipt_sha256":digest(CACHE/"priority-audit/priority-source-captures.json"),
        "previous_priority_review_sha256":digest(previous_path),"directory_comparison_complete":captures["google_directory_delta"]["comparison_complete"],
        "google_added_directory_urls":decisions,"new_directory_urls_relative_to_previous_batch":sum(r["is_new_directory_url_relative_to_nov24"] for r in decisions),
        "repository_observations":observations,"unique_repository_identities":len({r["repository"] for r in observations}),
        "selected_priority_papers":[],"priority_selection_note":"No new Google/Meta paper selected in this finite source pass; not a claim that no such paper exists globally.",
        "industrial_priority":[{"identity":"recommendation:lazunirec","source_url":"https://arxiv.org/pdf/2611.32590v1",
            "evidence":"Fixedv1 Alibaba International byline, Section4.8/Table5:10% production traffic for one week inOctober2026; GMV+4.01% trigger-free,+3.06% trigger-based. Complete retriever+ranker replacement, not isolated local-loss effect."},
            {"identity":"recommendation:larf","source_url":"https://arxiv.org/pdf/2611.32125v1",
            "evidence":"Fixedv1 Tencent Yuanbao byline, Section5.6/Table5: deployed1.7B student vs production baseline; high-satisfaction+1.77%, low-satisfaction−3.22%. Allocation/duration/sample size undisclosed, not invented."}],
        "unselected_industrial_leads":[{"id":"2611.32855","source_url":"https://arxiv.org/pdf/2611.32855v1",
            "reason":"Fixedv1 first-author Etsy; SIDECAR theoretical/certified semantic-ID decoding study, with production-scale transfer discussed separately. No qualifying quantified real production A/B verified. Do not substitute offline certificates for the industrial intake gate or relabel as Google from an author's name."}],
        "source_exceptions":[{k:r.get(k) for k in ("url","http_status","sha256","capture","parse_complete","error_type")} for r in captures["pages"] if r.get("parse_complete") is not True],
        "notes":["Two incomplete Meta landing inventories do not prove absence of new Meta work.",
            "The newly created AgentBox appears in both created and pushed observations; it is one repository, not two papers.",
            "Existing high-cost GenIA stays terminal; no archive is silently reintroduced as a reproduction TODO.",
            "New directory items, first submissions, revisions, bulletin dates and source-code releases remain separate.",
            "This finite selection does not close all metadata/source review since theNov15 watermark."]}
    (AUDIT/"priority-primary-selection.json").write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"new_directory_urls":value["new_directory_urls_relative_to_previous_batch"],"repository_events":len(observations),"unique_repositories":value["unique_repository_identities"],"industrial_selected":2}))


if __name__=="__main__":
    main()
