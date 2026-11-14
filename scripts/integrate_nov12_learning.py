"""Integrate authored bilingual comparisons, without translating or inferring prose."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from english_learning_sources import deep_dive_units
from run_nov12_components import AUDIT, COMPONENTS, ROOT


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main():
    proposals = [row for name in ("agent", "foundation", "post-training")
                 for row in load(AUDIT / f"{name}-deep-dive-proposals.json")["proposals"]]
    expected = {f"{domain}:{key}" for key, (domain, _) in COMPONENTS.items()}
    if {row["paper"] for row in proposals} != expected or len(proposals) != len(expected):
        raise ValueError("the fixed eight-paper learning scope is incomplete or duplicated")
    manifest = load(ROOT / "docs/research-manifest.json")
    paths = {f"{p['domain']}:{p['key']}": ROOT / "docs" / p["detail_path"] for p in manifest["papers"]}
    themes = {path.stem: load(path) for path in (ROOT / "docs/learning/topics").glob("*.json")}
    banks = {path.stem: load(path) for path in (ROOT / "docs/learning/deep-dives").glob("*.json")}
    output = ROOT / "docs/en/learning/translations/dive-nov12-components.json"
    if output.exists():
        raise ValueError("already integrated; do not overwrite reviewed English units")
    english = {}
    for row in proposals:
        card, paper = row["target_card"], row["paper"]
        theme, topic = card.split("/", 1)
        record = banks[theme]["topics"][topic]
        members = next(item for item in themes[theme]["topics"] if item["id"] == topic)["papers"]
        if paper in record["reviewed_papers"] or any(
                paper in item["papers"] for t in themes.values() for item in t["topics"]):
            raise ValueError(f"already assigned or reviewed paper: {paper}")
        for identity, fingerprint in row["source_revisions"].items():
            if hashlib.sha256(paths[identity].read_bytes()).hexdigest() != fingerprint:
                raise ValueError(f"reviewed paper changed before integration: {identity}")
        members.append(paper)
        record["reviewed_papers"].append(paper)
        record["updated"] = "2026-11-12"
        record["comparisons"].append({"paper": paper, **row["comparison"]})
        analysis_index = len(record["analysis"])
        record["analysis"].append(row["analysis"])
        record["questions"].append(row["question"])
        update, update_index = row["update"], len(record["updates"])
        if update["date"] != "2026-11-12" or paper not in update["papers"]:
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
                raise ValueError("reviewed English fields do not match the authored source")
            english[key] = {"source_sha256": units[key].source_sha256,
                            "reviewed": True, "fields": values}
    for name, payload in themes.items():
        write(ROOT / f"docs/learning/topics/{name}.json", payload)
    for name, payload in banks.items():
        write(ROOT / f"docs/learning/deep-dives/{name}.json", payload)
    write(output, {"schema_version": 1, "units": english})
    print("integrated eight authored topic updates and 32 reviewed English deep-dive units")


if __name__ == "__main__":
    main()
