"""Primary identity observations; repository pushes are not new publications."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov27-latest"
AUDIT = ROOT / "docs/research-audits/nov27-latest"


def main():
    current = json.loads((AUDIT / "priority-source-captures.json").read_text())
    previous = json.loads((ROOT / "docs/research-audits/nov26-latest/priority-source-captures.json").read_text())
    choices = {
        "facebookresearch/JEP-AV": (None, "source_only_placeholder", "CreatedNov26, README only Coming Soon plus license; no verified paper title/identity/date, method or runnable model. Archive source limitation, do not invent a JEPA reproduction."),
        "google-deepmind/psyre": ("2607.21797", "historical_source_framework", "Reactive-dataflow framework references2023 PL work and July2026 clock-calculus work. No new LLM/Agent algorithm identified from this README; do not execute installation instructions."),
        "google-deepmind/habitats": (None, "source_only_framework_no_verified_paper", "Reward-policy objective-evolution framework describes planner/mutator and cross-fitness but gives no verified paper identity or first-publication date. No fabricated catalog entry or API run."),
        "google-deepmind/origami-design": ("2606.26299", "historical_source_release", "README identifies June2026 COrigami, not a new November publication. Historical showcase tool-call histories were unrecorded; never claim replayability from stick figures alone. No campaign reopened."),
        "google-deepmind/disco": ("2611.27104", "already_cataloged_code_observation", "Names already-cataloged DISCO. A code push is not a new paper or evidence that our binary/unboosted L1 is a complete LLM-discovery agent."),
    }
    observations = []
    folder = CACHE / "priority-readmes"
    folder.mkdir(parents=True, exist_ok=True)
    for repo, (identity, decision, reason) in choices.items():
        result = subprocess.run(["gh", "api", f"repos/{repo}/readme", "-H", "Accept: application/vnd.github.raw+json"], capture_output=True, check=False)
        if result.returncode:
            observations.append({"repository": repo, "source_url": "https://github.com/" + repo,
                "decision": "source_exception_archived", "automatic_retry": False, "blocking": False})
            continue
        path = folder / (repo.replace("/", "--") + ".md")
        path.write_bytes(result.stdout)
        observations.append({"repository": repo, "source_url": "https://github.com/" + repo,
            "capture": path.relative_to(ROOT).as_posix(), "capture_sha256": sha256(result.stdout).hexdigest(),
            "paper_arxiv_identity": identity, "decision": decision, "reason": reason,
            "read_scope": "README identity/source-release observation, not full-paper method review"})
    result = subprocess.run(["gh", "api", "repos/google-research/google-research/commits?since=2026-11-26T00:00:00Z&per_page=30"], capture_output=True, check=False)
    monorepo = []
    if result.returncode == 0:
        (folder / "google-research-monorepo-commits.json").write_bytes(result.stdout)
        monorepo = [{"sha": r["sha"], "date": r["commit"]["author"]["date"], "message": r["commit"]["message"]} for r in json.loads(result.stdout)]
    added = sorted(set(current["google_directory_delta"]["added"]) - set(previous["google_directory_delta"]["added"]))
    payload = {"schema_version": 1, "reviewed_on": "2026-11-27", "captured_at": datetime.now(timezone.utc).isoformat(),
        "window": current["window"], "all_sources_exhaustive": False,
        "new_directory_urls_relative_to_nov26": added, "new_directory_url_count": len(added),
        "official_pages": len(current["pages"]), "parse_complete_pages": sum(r.get("parse_complete") is True for r in current["pages"]),
        "repository_query_count": len(current["repository_events"]), "repository_event_observations": sum(len(r.get("items", [])) for r in current["repository_events"]),
        "repository_primary_observations": observations, "monorepo_commits": monorepo,
        "monorepo_selection": "Observed commit adds orbit-guided ALOS PRISM/GEM-15 destriping. Earth-elevation processing, not an identified new in-scope LLM/Agent/JEPA or industrial recommendation algorithm; message-level topic screening only.",
        "known_blog": {"source": "https://research.google/blog/2026/11/", "latest_observed": "2026-11-25",
            "paper": "2609.17496", "decision": "New Fuse blog refers to already-cataloged paper, no duplicate intake"},
        "limits": ["No global absence/exhaustive Google/Meta claim.", "Fifteen directory URL additions are inherited versus Nov15, not today's new publications.",
            "Incomplete Meta landing pages remain source exceptions, not evidence of no new work.", "No previous high-cost campaign automatically reopened."]}
    (AUDIT / "priority-primary-selection.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"new_directory_urls": len(added), "primary_readme_checks": len(observations), "monorepo_commits": len(monorepo)}))


if __name__ == "__main__":
    main()
