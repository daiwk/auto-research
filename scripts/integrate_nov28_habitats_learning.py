"""Append the independently reviewed Habitats bilingual learning bundle once."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from english_learning_sources import deep_dive_units, question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov28-latest"
DATE = "2026-11-28"


def load(path):
    return json.loads(path.read_text())


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    bundle = load(AUDIT / "agent-authored-bundle.json")
    papers, english = bundle["papers"], bundle["english_question_units"]
    if set(papers) != {"agent-research:habitats"}:
        raise ValueError("authored scope differs")
    units = question_units({k: v["questions"] for k, v in papers.items()})
    if len(units) != 4 or set(english) != set(units):
        raise ValueError("four reviewed question levels required")
    for key, unit in units.items():
        row = english[key]
        if row.get("reviewed") is not True or set(row["fields"]) != set(unit.fields) or row.get("source_sha256") != unit.source_sha256:
            raise ValueError("unreviewed or stale QA: " + key)
    proposals = load(AUDIT / "deep-dive-proposals-agent.json")["proposals"]
    if len(proposals) != 1 or proposals[0]["paper"] != "agent-research:habitats":
        raise ValueError("deep-dive scope differs")
    row = proposals[0]
    card = row["target_card"]
    theme, topic = card.split("/", 1)
    topic_path = ROOT / f"docs/learning/topics/{theme}.json"
    bank_path = ROOT / f"docs/learning/deep-dives/{theme}.json"
    topics, bank = load(topic_path), load(bank_path)
    record = bank["topics"][topic]
    members = next(x for x in topics["topics"] if x["id"] == topic)["papers"]
    paper = row["paper"]
    if paper in members or not set(row["source_revisions"]) - {paper} <= set(members):
        raise ValueError("duplicate paper or comparison outside topic")
    paths = {p["domain"] + ":" + p["key"]: ROOT / "docs" / p["detail_path"] for p in load(ROOT / "docs/research-manifest.json")["papers"]}
    for identity, digest in row["source_revisions"].items():
        if hashlib.sha256(paths[identity].read_bytes()).hexdigest() != digest:
            raise ValueError("reviewed README changed: " + identity)
    for field in ("analysis", "question", "update"):
        if not set(row[field]["papers"]) <= set(row["source_revisions"]):
            raise ValueError("unfingerprinted comparison")
    if row["update"]["date"] != DATE or paper not in row["update"]["papers"]:
        raise ValueError("wrong update scope")
    members.append(paper)
    record["reviewed_papers"].append(paper)
    record["updated"] = DATE
    record["comparisons"].append({"paper": paper, **row["comparison"]})
    ai, ui = len(record["analysis"]), len(record["updates"])
    record["analysis"].append(row["analysis"])
    record["questions"].append(row["question"])
    record["updates"].append(row["update"] | {"source_revisions": {k: row["source_revisions"][k] for k in row["update"]["papers"]}})
    units = deep_dive_units({card: record})
    en = row["english"]
    fields = {f"dive/{card}/comparison/{paper}": en["comparison"],
              f"dive/{card}/analysis/{ai}": en["analysis"],
              f"dive/{card}/question/{row['question']['id']}": en["question"],
              f"dive/{card}/update/{DATE}/{ui}": {"summary": en["update"]}}
    translations = {}
    for key, value in fields.items():
        if set(value) != set(units[key].fields):
            raise ValueError("English deep fields differ")
        translations[key] = {"source_sha256": units[key].source_sha256, "reviewed": True, "fields": value}
    outputs = {
        ROOT / "docs/learning/questions/nov28-latest-agent.json": {"schema_version": 1, "papers": papers},
        ROOT / "docs/en/learning/translations/qa-nov28-latest-agent.json": {"schema_version": 1, "units": english},
        ROOT / "docs/en/learning/translations/dive-nov28-latest.json": {"schema_version": 1, "units": translations},
    }
    if any(path.exists() for path in outputs):
        raise ValueError("append-once output already exists")
    for path, value in {**outputs, topic_path: topics, bank_path: bank}.items():
        dump(path, value)
    print(json.dumps({"bilingual_questions": 4, "same_topic_updates": 1, "english_deep_units": 4}))


if __name__ == "__main__":
    main()
