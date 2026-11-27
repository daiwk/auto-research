"""Append the seven reviewed paper-specific bilingual learning bundles once."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from english_learning_sources import deep_dive_units, question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov27-latest"
DATE = "2026-11-27"
GROUPS = ("foundation", "post", "agent", "root")


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
    for group in GROUPS:
        bundle = load(AUDIT / f"{group}-authored-bundle.json")
        papers, english = bundle["papers"], bundle["english_question_units"]
        if found & set(papers):
            raise ValueError("duplicate authored ownership")
        found.update(papers)
        units = question_units({key: value["questions"] for key, value in papers.items()})
        if set(english) != set(units):
            raise ValueError("English QA scope differs: " + group)
        for key, unit in units.items():
            row = english[key]
            if row.get("reviewed") is not True or set(row["fields"]) != set(unit.fields) or row.get("source_sha256") != unit.source_sha256:
                raise ValueError("unreviewed or stale QA: " + key)
        outputs[ROOT / f"docs/learning/questions/nov27-latest-{group}.json"] = {"schema_version": 1, "papers": papers}
        outputs[ROOT / f"docs/en/learning/translations/qa-nov27-latest-{group}.json"] = {"schema_version": 1, "units": english}
    if found != expected:
        raise ValueError("authored question scope differs")
    proposals = [r for group in GROUPS for r in load(AUDIT / f"deep-dive-proposals-{group}.json")["proposals"]]
    if len(proposals) != len(expected) or {r["paper"] for r in proposals} != expected:
        raise ValueError("deep-dive scope differs")
    themes = {p.stem: load(p) for p in (ROOT / "docs/learning/topics").glob("*.json")}
    banks = {p.stem: load(p) for p in (ROOT / "docs/learning/deep-dives").glob("*.json")}
    target = ROOT / "docs/en/learning/translations/dive-nov27-latest.json"
    if target.exists():
        raise ValueError("append-once integration already exists")
    translations = {}
    for row in proposals:
        paper, card = row["paper"], row["target_card"]
        theme, topic = card.split("/", 1)
        record = banks[theme]["topics"][topic]
        members = next(x for x in themes[theme]["topics"] if x["id"] == topic)["papers"]
        if any(paper in x["papers"] for t in themes.values() for x in t["topics"]):
            raise ValueError("paper already assigned: " + paper)
        if not set(row["source_revisions"]) - {paper} <= set(members):
            raise ValueError("comparison peer outside chosen topic: " + paper)
        for identity, digest in row["source_revisions"].items():
            if hashlib.sha256(paths[identity].read_bytes()).hexdigest() != digest:
                raise ValueError("reviewed README changed: " + identity)
        for field in ("analysis", "question", "update"):
            if not set(row[field]["papers"]) <= set(row["source_revisions"]):
                raise ValueError("unfingerprinted comparison: " + paper)
        if row["update"]["date"] != DATE or paper not in row["update"]["papers"]:
            raise ValueError("wrong update date/scope")
        members.append(paper)
        record["reviewed_papers"].append(paper)
        record["updated"] = DATE
        record["comparisons"].append({"paper": paper, **row["comparison"]})
        ai, ui = len(record["analysis"]), len(record["updates"])
        record["analysis"].append(row["analysis"])
        record["questions"].append(row["question"])
        record["updates"].append(row["update"] | {"source_revisions": {k: row["source_revisions"][k] for k in row["update"]["papers"]}})
        units = deep_dive_units({card: record})
        english = row["english"]
        fields = {f"dive/{card}/comparison/{paper}": english["comparison"],
                  f"dive/{card}/analysis/{ai}": english["analysis"],
                  f"dive/{card}/question/{row['question']['id']}": english["question"],
                  f"dive/{card}/update/{DATE}/{ui}": {"summary": english["update"]}}
        for key, text in fields.items():
            if set(text) != set(units[key].fields):
                raise ValueError("English deep fields differ: " + key)
            translations[key] = {"source_sha256": units[key].source_sha256, "reviewed": True, "fields": text}
    for name, value in themes.items():
        outputs[ROOT / f"docs/learning/topics/{name}.json"] = value
    for name, value in banks.items():
        outputs[ROOT / f"docs/learning/deep-dives/{name}.json"] = value
    outputs[target] = {"schema_version": 1, "units": translations}
    for path in outputs:
        if path.exists() and "deep-dives" not in path.parts and "topics" not in path.parts:
            raise ValueError("refusing to overwrite authored content: " + str(path))
    for path, value in outputs.items():
        dump(path, value)
    print(json.dumps({"bilingual_questions": len(expected) * 4, "same_topic_updates": len(proposals), "english_deep_units": len(translations)}))


if __name__ == "__main__":
    main()
