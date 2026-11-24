"""Bounded Google/Meta recall audit with explicit carried-forward decisions."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"docs/research-audits/nov24-latest"
CACHE=ROOT/".cache/nov24-latest"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    captures=json.loads((CACHE/"priority-audit/priority-source-captures.json").read_text())
    prior_path=ROOT/"docs/research-audits/nov23-latest/priority-primary-selection.json"
    prior=json.loads(prior_path.read_text())
    prior_decisions={x["source_url"]:x for x in prior["google_added_directory_urls"]}
    directories=[]
    for row in captures["added_details"]:
        previous=prior_decisions.get(row["url"])
        directories.append({"source_url":row["url"],"capture_sha256":row.get("sha256"),
            "parse_complete":row.get("parse_complete",False),"reviewed_on":"2026-11-24",
            "decision":"carried_forward_finite_source_triage" if previous else "source_only_not_selected",
            "previous_decision":previous,"previous_review":"nov23-latest/priority-primary-selection.json" if previous else None,
            "reason":"This URL is the same finiteNov15-baseline directory difference already triaged inNov23, not a newly published paper. Carry forward the recorded disposition; this is not a new full-method review." if previous else "No verified standalone method selected from this source-only lead in the finite intake; no invented reproduction.",
            "automatic_retry":False})
    repositories=[]
    known={"facebookresearch/autoform-bot":"Existing AutoformBench/AutoformBot catalog; no changed defining method verified from this push.",
        "facebookresearch/atlas-lean":"Read current README: v2 library is live; companion paper2605.29955 and AutoformBot are existing identities. A library push is not a newly published algorithm.",
        "facebookresearch/logact":"Existing LogAct catalog; no defining-method change verified from the push.",
        "facebookresearch/lean_kernel_verify":"Carry forward source-only compiler/Lean limitation fromNov23; no standalone paper identity newly established.",
        "facebookresearch/project_superdex":"Read official README: physics/robotics/studio/lab simulation platform. No standalone LLM/Agent/world-model paper identity verified in that README; source-only tooling observation, not rejection of a verified novel algorithm.",
        "google-research/ple":"Read official README: paper2610.30537 is already cataloged as physical-engineering-exam. Push time is not a new paper date.",
        "google-research/mseb":"Read README: Massive Sound Embedding Benchmark framework. This intake did not verify a new linked standalone paper/method or run its sound benchmark.",
        "google-deepmind/reaf-sim":"Read README: simulation library and MuJoCo playground integration. No new standalone in-scope paper verified from the README; not a completed method review."}
    raw_files={"facebookresearch/project_superdex":"project-superdex-readme.json","facebookresearch/atlas-lean":"atlas-lean-readme.json",
        "google-research/ple":"ple-readme.json","google-research/mseb":"mseb-readme.json","google-deepmind/reaf-sim":"reaf-sim-readme.json"}
    for query in captures["repository_events"]:
        for item in query.get("items",[]):
            name=item["full_name"]
            repositories.append({"repository":name,"event":query["event"],"source_url":item["html_url"],
                "observed_pushed_at":item.get("pushed_at"),"observed_created_at":item.get("created_at"),
                "decision":"bounded_readme_or_existing_identity_triage" if name in known else "event_observed_not_full_method_reviewed",
                "reason":known.get(name,"Repository push is a recall signal. No full-method or paper-release conclusion made for this general library/tooling event in the finite intake."),
                "readme_capture_sha256":digest(CACHE/raw_files[name]) if name in raw_files else None})
    blog=CACHE/"google-dca-blog.html"
    data={"schema_version":1,"reviewed_on":"2026-11-24","all_sources_exhaustive":False,"watermark_advanced":False,
        "raw_directory_receipt_sha256":digest(CACHE/"priority-audit/priority-source-captures.json"),
        "previous_priority_review_sha256":digest(prior_path),"directory_baseline":"Nov15 finite Google directory, not publication dates",
        "directory_comparison_complete":captures["google_directory_delta"]["comparison_complete"],
        "google_added_directory_urls":directories,"new_directory_urls_relative_to_previous_batch":len(set(x["source_url"] for x in directories)-set(prior_decisions)),
        "repository_observations":repositories,"selected_priority_papers":[
            {"identity":"foundation-models:deep-cross-attention","priority":"P0","source_url":"https://research.google/blog/supercharging-transformer-residual-connections/",
             "capture_sha256":digest(blog),"evidence":"Nov23 blog links ICML2025 DCA; fixed2502.06785v2 first authorMike Heddes/UCI, multiple Google Research coauthors. Feb10,2025 first release, July23v2. Historical backfill, not aNov23 new paper."},
            {"identity":"post-training:vopd","priority":"P0","evidence":"Fixed2611.30325v1 byline: first authorJuntong Shi/Stanford, Minkai Xu/Google DeepMind. Nov23 original. Author repository currently only promises forthcoming code; not a published runnable trainer."}],
        "industrial_priority":[{"identity":"recommendation:weight-coding","source_url":"https://arxiv.org/html/2611.29613v1",
            "evidence":"Fixedv1 Pinterest byline, Section4.7/Table4 real online A/B ~10M users/group ~one week; source-attributed saves/user+8.4–10.7%, not site-wide. Only CPU edit/search core implemented, private full campaign not reproduced."}],
        "source_exceptions":[{k:r.get(k) for k in ("url","http_status","sha256","capture","parse_complete","error_type")} for r in captures["pages"] if r.get("parse_complete") is not True],
        "notes":["Two incomplete Meta landing inventories do not prove zero new Meta papers.",
            "Existing GSLM2, Unbundling Vision and AutoformBot identities were checked in the current catalog; do not count resurfaced search results as new releases.",
            "MoR4Rec2611.29462 is an unselected academic sequential-recommendation lead; no qualifying production A/B established in this intake. Not implemented by treating offline improvements as industrial evidence.",
            "All unselected recent metadata remain recall observations, not a hidden mandatory implementation backlog or a completed full-window review."]}
    (AUDIT/"priority-primary-selection.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"priority_papers":2,"industrial_papers":1,"new_directory_urls_relative_to_nov23":data["new_directory_urls_relative_to_previous_batch"],"repository_observations":len(repositories)}))


if __name__=="__main__":
    main()
