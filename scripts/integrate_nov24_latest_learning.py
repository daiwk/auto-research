"""Append reviewed overlap and historical-priority learning bundles once."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from english_learning_sources import deep_dive_units, question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov24-latest"
DATE = "2026-11-24"
GROUPS = ("foundation", "agent", "post", "root")


def load(path):
    return json.loads(path.read_text())


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    expected = set(load(AUDIT / "intake-scope.json")["accepted_papers"])
    paths = {p["domain"] + ":" + p["key"]: ROOT / "docs" / p["detail_path"]
             for p in load(ROOT / "docs/research-manifest.json")["papers"]}
    outputs, found = {}, set()
    for name in GROUPS:
        bundle = load(AUDIT / f"{name}-authored-bundle.json")
        papers, english = bundle["papers"], bundle["english_question_units"]
        if found & set(papers):
            raise ValueError("duplicate authored paper ownership")
        found.update(papers)
        units = question_units({key: value["questions"] for key, value in papers.items()})
        if set(english) != set(units):
            raise ValueError("authored English question scope differs: " + name)
        for key, unit in units.items():
            row = english[key]
            if (row.get("reviewed") is not True or set(row["fields"]) != set(unit.fields)
                    or row.get("source_sha256") != unit.source_sha256):
                raise ValueError("unreviewed/stale authored question: " + key)
        outputs[ROOT / f"docs/learning/questions/nov24-latest-{name}.json"] = {"schema_version": 1, "papers": papers}
        outputs[ROOT / f"docs/en/learning/translations/qa-nov24-latest-{name}.json"] = {"schema_version": 1, "units": english}
    if found != expected:
        raise ValueError("fixed question scope missing or expanded")
    proposals = [row for name in GROUPS
                 for row in load(AUDIT / f"deep-dive-proposals-{name}.json")["proposals"]]
    if len(proposals) != len(expected) or {row["paper"] for row in proposals} != expected:
        raise ValueError("authored proposal scope missing/duplicated")
    themes = {p.stem: load(p) for p in (ROOT / "docs/learning/topics").glob("*.json")}
    banks = {p.stem: load(p) for p in (ROOT / "docs/learning/deep-dives").glob("*.json")}
    english = {}
    target = ROOT / "docs/en/learning/translations/dive-nov24-latest.json"
    if target.exists():
        raise ValueError("append-once integration already exists; preserve history")
    for row in proposals:
        paper, card = row["paper"], row["target_card"]
        theme, topic = card.split("/", 1)
        record = banks[theme]["topics"][topic]
        members = next(x for x in themes[theme]["topics"] if x["id"] == topic)["papers"]
        if any(paper in x["papers"] for value in themes.values() for x in value["topics"]):
            raise ValueError("paper already assigned to a topic: " + paper)
        if not set(row["source_revisions"]) - {paper} <= set(members):
            raise ValueError("comparison outside selected topic: " + paper)
        for identity, digest in row["source_revisions"].items():
            if hashlib.sha256(paths[identity].read_bytes()).hexdigest() != digest:
                raise ValueError("reviewed README changed: " + identity)
        for field in ("analysis", "question", "update"):
            if not set(row[field]["papers"]) <= set(row["source_revisions"]):
                raise ValueError("unfingerprinted comparison source")
        if row["update"]["date"] != DATE or paper not in row["update"]["papers"]:
            raise ValueError("wrong update date/scope")
        members.append(paper)
        record["reviewed_papers"].append(paper)
        record["updated"] = DATE
        record["comparisons"].append({"paper": paper, **row["comparison"]})
        ai, ui = len(record["analysis"]), len(record["updates"])
        record["analysis"].append(row["analysis"])
        record["questions"].append(row["question"])
        record["updates"].append(row["update"] | {"source_revisions": {
            key: row["source_revisions"][key] for key in row["update"]["papers"]}})
        units = deep_dive_units({card: record})
        fields = row["english"]
        translated = {
            f"dive/{card}/comparison/{paper}": fields["comparison"],
            f"dive/{card}/analysis/{ai}": fields["analysis"],
            f"dive/{card}/question/{row['question']['id']}": fields["question"],
            f"dive/{card}/update/{DATE}/{ui}": {"summary": fields["update"]},
        }
        for key, texts in translated.items():
            if set(texts) != set(units[key].fields):
                raise ValueError("English topic fields differ: " + key)
            english[key] = {"source_sha256": units[key].source_sha256, "reviewed": True, "fields": texts}
    for name, value in themes.items():
        outputs[ROOT / f"docs/learning/topics/{name}.json"] = value
    for name, value in banks.items():
        outputs[ROOT / f"docs/learning/deep-dives/{name}.json"] = value
    outputs[target] = {"schema_version": 1, "units": english}
    for path in outputs:
        if path.exists() and "deep-dives" not in path.parts and "topics" not in path.parts:
            raise ValueError("refusing to overwrite authored content: " + str(path))
    for path, value in outputs.items():
        dump(path, value)
    print(json.dumps({"same_topic_updates": len(proposals), "reviewed_english_deep_units": len(english)}))


if __name__ == "__main__":
    main()
