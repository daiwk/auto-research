"""Integrate fixed authored, reviewed bilingual comparisons with exact source hashes."""
from __future__ import annotations

import hashlib
import json

from english_learning_sources import deep_dive_units
from run_nov15_refresh_components import AUDIT, ROOT

FILES = [f"deep-dive-proposals-{name}.json" for name in ("foundation", "agent", "post", "root")]


def load(path):
    return json.loads(path.read_text())


def write(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main():
    proposals = [row for name in FILES for row in load(AUDIT / name)["proposals"]]
    expected = set(load(AUDIT / "intake-scope.json")["accepted_papers"])
    if {row["paper"] for row in proposals} != expected or len(proposals) != len(expected):
        raise ValueError("exact fixed-paper authored learning scope incomplete or duplicated")
    manifest = load(ROOT / "docs/research-manifest.json")
    paths = {f"{p['domain']}:{p['key']}": ROOT / "docs" / p["detail_path"] for p in manifest["papers"]}
    themes = {path.stem: load(path) for path in (ROOT / "docs/learning/topics").glob("*.json")}
    banks = {path.stem: load(path) for path in (ROOT / "docs/learning/deep-dives").glob("*.json")}
    output = ROOT / "docs/en/learning/translations/dive-nov15-refresh.json"
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
        for identity, fingerprint in row["source_revisions"].items():
            if hashlib.sha256(paths[identity].read_bytes()).hexdigest() != fingerprint:
                raise ValueError("reviewed paper changed before integration: " + identity)
        if not set(row["update"]["papers"]) <= set(row["source_revisions"]):
            raise ValueError("all compared update sources require exact fingerprints")
        if not (set(row["source_revisions"]) - {paper}) <= set(members):
            raise ValueError("comparison source is outside its target topic: " + paper)
        members.append(paper)
        record["reviewed_papers"].append(paper)
        record["updated"] = "2026-11-15"
        record["comparisons"].append({"paper": paper, **row["comparison"]})
        analysis_index = len(record["analysis"])
        record["analysis"].append(row["analysis"])
        record["questions"].append(row["question"])
        update, update_index = row["update"], len(record["updates"])
        if update["date"] != "2026-11-15" or paper not in update["papers"]:
            raise ValueError("dated update must include its new paper")
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
                raise ValueError("reviewed English fields differ from the authored source")
            english[key] = {"source_sha256": units[key].source_sha256, "reviewed": True, "fields": values}
    for name, payload in themes.items():
        write(ROOT / f"docs/learning/topics/{name}.json", payload)
    for name, payload in banks.items():
        write(ROOT / f"docs/learning/deep-dives/{name}.json", payload)
    write(output, {"schema_version": 1, "units": english})
    print("integrated fixed authored topic additions and source-bound reviewed English deep-dive units")


if __name__ == "__main__":
    main()
