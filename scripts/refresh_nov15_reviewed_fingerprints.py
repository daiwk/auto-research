"""Refresh reviewed Nov15 provenance after format-only Markdown corrections.

No prose is translated or generated here. Compared existing sources must still
match their prior hashes; only this fixed batch's reviewed source pages change.
"""
import hashlib
import json
import re

from english_learning_sources import deep_dive_units
from run_nov15_refresh_components import AUDIT, ROOT, load


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main():
    accepted = set(load(AUDIT / "intake-scope.json")["accepted_papers"])
    papers = {row["domain"] + ":" + row["key"]: row
              for row in load(ROOT / "docs/research-manifest.json")["papers"]}
    fingerprints = {identity: hashlib.sha256((ROOT / "docs" / row["detail_path"]).read_bytes()).hexdigest()
                    for identity, row in papers.items()}
    for identity in accepted:
        english = (ROOT / "docs" / papers[identity]["detail_path"]).with_name("README-en.md")
        content, count = re.subn(r"(?m)^<!-- source-sha256: [a-f0-9]{64} -->$",
                                 "<!-- source-sha256: " + fingerprints[identity] + " -->",
                                 english.read_text())
        if count != 1:
            raise ValueError("exactly one reviewed source fingerprint required: " + identity)
        english.write_text(content.rstrip() + "\n")
    for name in ("foundation", "post", "agent", "root"):
        path = AUDIT / f"deep-dive-proposals-{name}.json"
        payload = load(path)
        for proposal in payload["proposals"]:
            for identity, value in proposal["source_revisions"].items():
                if identity not in accepted and fingerprints[identity] != value:
                    raise ValueError("existing comparison source unexpectedly changed: " + identity)
                proposal["source_revisions"][identity] = fingerprints[identity]
        write(path, payload)
    units = {}
    for path in (ROOT / "docs/learning/deep-dives").glob("*.json"):
        bank = load(path)
        for topic, record in bank["topics"].items():
            for update in record["updates"]:
                if update["date"] == "2026-11-15" and set(update["papers"]) & accepted:
                    for identity in update["source_revisions"]:
                        update["source_revisions"][identity] = fingerprints[identity]
            units.update(deep_dive_units({path.stem + "/" + topic: record}))
        write(path, bank)
    path = ROOT / "docs/en/learning/translations/dive-nov15-refresh.json"
    english = load(path)
    for key, entry in english["units"].items():
        entry["source_sha256"] = units[key].source_sha256
    write(path, english)
    for name in ("foundation", "agent", "post", "root"):
        path = AUDIT / f"{name}-review.json"
        review = load(path)
        for record in review.get("accepted", review.get("papers", review.get("records", []))):
            identity = record.get("identity")
            if not identity and record.get("key"):
                identity = next((p for p in accepted if p.split(":", 1)[1] == record["key"]), None)
            if identity in accepted and "source_readme_sha256" in record:
                record["source_readme_sha256"] = fingerprints[identity]
        write(path, review)
    print("refreshed exact reviewed source fingerprints; no prose or claim-tier changes")


if __name__ == "__main__":
    main()
