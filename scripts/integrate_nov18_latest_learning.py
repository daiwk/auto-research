"""Integrate47 authored bilingual topic comparisons with exact source revisions."""

from __future__ import annotations
import hashlib
import json
from english_learning_sources import deep_dive_units
from run_nov18_latest_components import ROOT, AUDIT, load


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    proposals = [
        r
        for name in ("foundation", "post", "agent", "root")
        for r in load(AUDIT / f"deep-dive-proposals-{name}.json")["proposals"]
    ]
    expected = set(load(AUDIT / "intake-scope.json")["accepted_papers"])
    if {r["paper"] for r in proposals} != expected or len(proposals) != len(expected):
        raise ValueError("exact authored47-paper scope missing or duplicated")
    paths = {
        p["domain"] + ":" + p["key"]: ROOT / "docs" / p["detail_path"]
        for p in load(ROOT / "docs/research-manifest.json")["papers"]
    }
    themes = {p.stem: load(p) for p in (ROOT / "docs/learning/topics").glob("*.json")}
    banks = {p.stem: load(p) for p in (ROOT / "docs/learning/deep-dives").glob("*.json")}
    output = ROOT / "docs/en/learning/translations/dive-nov18-latest.json"
    if output.exists():
        raise ValueError("already integrated; do not overwrite reviewed translations")
    english = {}
    for row in proposals:
        card, paper = row["target_card"], row["paper"]
        theme, topic = card.split("/", 1)
        record = banks[theme]["topics"][topic]
        members = next(t for t in themes[theme]["topics"] if t["id"] == topic)["papers"]
        if any(paper in t["papers"] for x in themes.values() for t in x["topics"]):
            raise ValueError("already assigned: " + paper)
        for identity, fingerprint in row["source_revisions"].items():
            if hashlib.sha256(paths[identity].read_bytes()).hexdigest() != fingerprint:
                raise ValueError("reviewed source changed: " + identity)
        if not (set(row["source_revisions"]) - {paper}) <= set(members):
            raise ValueError("comparison outside same topic: " + paper)
        for field in ("analysis", "question", "update"):
            if not set(row[field]["papers"]) <= set(row["source_revisions"]):
                raise ValueError("unfingerprinted comparison source")
        members.append(paper)
        record["reviewed_papers"].append(paper)
        record["updated"] = "2026-11-18"
        record["comparisons"].append({"paper": paper, **row["comparison"]})
        analysis_index = len(record["analysis"])
        record["analysis"].append(row["analysis"])
        record["questions"].append(row["question"])
        update_index = len(record["updates"])
        update = row["update"]
        if update["date"] != "2026-11-18" or paper not in update["papers"]:
            raise ValueError("wrong dated update scope")
        record["updates"].append(
            update | {"source_revisions": {k: row["source_revisions"][k] for k in update["papers"]}}
        )
        units = deep_dive_units({card: record})
        fields = row["english"]
        values = {
            f"dive/{card}/comparison/{paper}": fields["comparison"],
            f"dive/{card}/analysis/{analysis_index}": fields["analysis"],
            f"dive/{card}/question/{row['question']['id']}": fields["question"],
            f"dive/{card}/update/{update['date']}/{update_index}": {"summary": fields["update"]},
        }
        for key, texts in values.items():
            if set(texts) != set(units[key].fields):
                raise ValueError("English authored field mismatch: " + key)
            english[key] = {
                "source_sha256": units[key].source_sha256,
                "reviewed": True,
                "fields": texts,
            }
    for name, value in themes.items():
        dump(ROOT / f"docs/learning/topics/{name}.json", value)
    for name, value in banks.items():
        dump(ROOT / f"docs/learning/deep-dives/{name}.json", value)
    dump(output, {"schema_version": 1, "units": english})
    print(
        json.dumps(
            {"same_topic_updates": len(proposals), "reviewed_english_deep_dive_units": len(english)}
        )
    )


if __name__ == "__main__":
    main()
