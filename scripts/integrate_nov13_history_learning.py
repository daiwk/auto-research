"""Integrate six authored, source-bound bilingual historical learning updates."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from english_learning_sources import deep_dive_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov13-history-repair"
KEYS = {"scientist-two", "ds-star", "era-flat-puct", "envharness", "mle-star", "alphaevolve"}
FILES = ["deep-dive-proposals.json", "ds-star-deep-dive-proposals.json",
         "envharness-deep-dive-proposals.json", "era-deep-dive-proposals.json",
         "deep-dive-proposals-priority.json"]


def load(path):
    return json.loads(path.read_text())


def write(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main():
    proposals = [row for name in FILES for row in load(AUDIT / name)["proposals"]]
    expected = {"agent-research:" + key for key in KEYS}
    if {row["paper"] for row in proposals} != expected or len(proposals) != len(expected):
        raise ValueError("exact six-paper authored learning scope incomplete or duplicated")
    manifest = load(ROOT / "docs/research-manifest.json")
    paths = {f"{p['domain']}:{p['key']}": ROOT / "docs" / p["detail_path"] for p in manifest["papers"]}
    themes = {path.stem: load(path) for path in (ROOT / "docs/learning/topics").glob("*.json")}
    banks = {path.stem: load(path) for path in (ROOT / "docs/learning/deep-dives").glob("*.json")}
    output = ROOT / "docs/en/learning/translations/dive-nov13-history.json"
    if output.exists():
        raise ValueError("already integrated; do not overwrite reviewed translations")
    english = {}
    for row in proposals:
        card, paper = row["target_card"], row["paper"]
        theme, topic = card.split("/", 1)
        record = banks[theme]["topics"][topic]
        members = next(item for item in themes[theme]["topics"] if item["id"] == topic)["papers"]
        if any(paper in item["papers"] for value in themes.values() for item in value["topics"]):
            raise ValueError("already assigned paper: " + paper)
        if not set(row["update"]["papers"]) <= set(row["source_revisions"]):
            raise ValueError("all compared update papers need source fingerprints")
        for identity, fingerprint in row["source_revisions"].items():
            if hashlib.sha256(paths[identity].read_bytes()).hexdigest() != fingerprint:
                raise ValueError("reviewed paper changed before integration: " + identity)
        members.append(paper)
        record["reviewed_papers"].append(paper)
        record["updated"] = "2026-11-13"
        record["comparisons"].append({"paper": paper, **row["comparison"]})
        analysis_index = len(record["analysis"])
        record["analysis"].append(row["analysis"])
        record["questions"].append(row["question"])
        update, update_index = row["update"], len(record["updates"])
        if update["date"] != "2026-11-13" or paper not in update["papers"]:
            raise ValueError("actual dated update must include its new paper")
        record["updates"].append(update | {"source_revisions": {
            identity: row["source_revisions"][identity] for identity in update["papers"]}})
        units = deep_dive_units({card: record})
        fields = row["english"]
        localized = {
            f"dive/{card}/comparison/{paper}": fields["comparison"],
            f"dive/{card}/analysis/{analysis_index}": fields["analysis"],
            f"dive/{card}/question/{row['question']['id']}": fields["question"],
            f"dive/{card}/update/{update['date']}/{update_index}": {"summary": fields["update"]},
        }
        for key, values in localized.items():
            if set(values) != set(units[key].fields):
                raise ValueError("English fields do not match authored source")
            english[key] = {"source_sha256": units[key].source_sha256, "reviewed": True, "fields": values}
    for name, payload in themes.items():
        write(ROOT / f"docs/learning/topics/{name}.json", payload)
    for name, payload in banks.items():
        write(ROOT / f"docs/learning/deep-dives/{name}.json", payload)
    write(output, {"schema_version": 1, "units": english})
    print("integrated six authored topic updates and 24 reviewed English deep-dive units")


if __name__ == "__main__":
    main()
