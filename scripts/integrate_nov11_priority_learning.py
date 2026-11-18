"""Integrate the reviewed November priority readings; never translate prose."""
from __future__ import annotations

import json
from pathlib import Path

from english_learning_sources import deep_dive_units

ROOT = Path(__file__).resolve().parents[1]


def main():
    proposals = json.loads((ROOT / "docs/research-audits/nov11-components/priority-deep-dive-proposals.json").read_text())["proposals"]
    path = ROOT / "docs/learning/deep-dives/agent-research.json"
    payload = json.loads(path.read_text())
    english = {}
    for proposal in proposals:
        card = proposal["target_card"]
        record = payload["topics"][card.split("/", 1)[1]]
        paper = proposal["paper"]
        if paper in record["reviewed_papers"]:
            raise ValueError("refusing to append an already integrated priority paper")
        record["reviewed_papers"].append(paper)
        record["updated"] = "2026-11-11"
        record["comparisons"].append({"paper": paper, **proposal["comparison"]})
        analysis_index = len(record["analysis"])
        record["analysis"].append(proposal["analysis"])
        record["questions"].append(proposal["question"])
        update = proposal["update"]
        update_index = len(record["updates"])
        record["updates"].append(update | {"source_revisions": {
            identity: proposal["source_revisions"][identity] for identity in update["papers"]}})
        units = deep_dive_units({card: record})
        fields = proposal["english"]
        localized = {
            f"dive/{card}/comparison/{paper}": fields["comparison"],
            f"dive/{card}/analysis/{analysis_index}": fields["analysis"],
            f"dive/{card}/question/{proposal['question']['id']}": fields["question"],
            f"dive/{card}/update/{update['date']}/{update_index}": {"summary": fields["update"]},
        }
        for key, values in localized.items():
            english[key] = {"source_sha256": units[key].source_sha256, "reviewed": True, "fields": values}
    output = ROOT / "docs/en/learning/translations/dive-nov11-priority.json"
    if output.exists():
        raise ValueError("reviewed English units must not be overwritten")
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    output.write_text(json.dumps({"schema_version": 1, "units": english}, ensure_ascii=False, indent=2) + "\n")
    print("integrated three reviewed priority readings and twelve English units")


if __name__ == "__main__":
    main()
