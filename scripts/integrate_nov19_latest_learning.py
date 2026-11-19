"""Append reviewed same-topic Nov19 comparisons and exact bilingual overlays."""

from __future__ import annotations
import hashlib
import argparse
import json
from english_learning_sources import deep_dive_units
from run_nov19_latest_components import AUDIT, ROOT, load


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--append-new",
        action="store_true",
        help="Append late reviewed intake without overwriting prior authored updates",
    )
    args = parser.parse_args()
    proposals = [
        r
        for name in ("foundation", "post", "agent", "root")
        for r in load(AUDIT / f"deep-dive-proposals-{name}.json")["proposals"]
    ]
    expected = set(load(AUDIT / "intake-scope.json")["accepted_papers"])
    if {r["paper"] for r in proposals} != expected or len(proposals) != len(expected):
        raise ValueError("exact authored intake missing/duplicated")
    paths = {
        p["domain"] + ":" + p["key"]: ROOT / "docs" / p["detail_path"]
        for p in load(ROOT / "docs/research-manifest.json")["papers"]
    }
    themes = {p.stem: load(p) for p in (ROOT / "docs/learning/topics").glob("*.json")}
    banks = {p.stem: load(p) for p in (ROOT / "docs/learning/deep-dives").glob("*.json")}
    output = ROOT / "docs/en/learning/translations/dive-nov19-latest.json"
    if output.exists() and not args.append_new:
        raise ValueError("already integrated; preserve reviewed update history")
    english = load(output)["units"] if output.exists() else {}
    for row in proposals:
        card, paper = row["target_card"], row["paper"]
        theme, topic = card.split("/", 1)
        record = banks[theme]["topics"][topic]
        members = next(t for t in themes[theme]["topics"] if t["id"] == topic)["papers"]
        for identity, fingerprint in row["source_revisions"].items():
            if hashlib.sha256(paths[identity].read_bytes()).hexdigest() != fingerprint:
                raise ValueError("reviewed source changed: " + identity)
        if any(paper in t["papers"] for x in themes.values() for t in x["topics"]):
            if (
                not args.append_new
                or paper not in members
                or {"paper": paper, **row["comparison"]} not in record["comparisons"]
                or row["analysis"] not in record["analysis"]
                or row["question"] not in record["questions"]
                or row["update"]
                | {
                    "source_revisions": {
                        k: row["source_revisions"][k] for k in row["update"]["papers"]
                    }
                }
                not in record["updates"]
            ):
                raise ValueError("existing authored update differs: " + paper)
            continue
        if not (set(row["source_revisions"]) - {paper}) <= set(members):
            raise ValueError("comparison peer outside same topic: " + paper)
        for field in ("analysis", "question", "update"):
            if not set(row[field]["papers"]) <= set(row["source_revisions"]):
                raise ValueError("unfingerprinted source")
        members.append(paper)
        record["reviewed_papers"].append(paper)
        record["updated"] = "2026-11-19"
        record["comparisons"].append({"paper": paper, **row["comparison"]})
        analysis_index = len(record["analysis"])
        record["analysis"].append(row["analysis"])
        record["questions"].append(row["question"])
        update_index = len(record["updates"])
        update = row["update"]
        if update["date"] != "2026-11-19" or paper not in update["papers"]:
            raise ValueError("wrong update date/scope")
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
                raise ValueError("English fields differ: " + key)
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
        json.dumps({"same_topic_updates": len(proposals), "reviewed_english_units": len(english)})
    )


if __name__ == "__main__":
    main()
