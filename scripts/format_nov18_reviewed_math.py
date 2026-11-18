"""Refresh reviewed Nov18 provenance after format-only Markdown corrections.

No prose is translated or generated here. Compared existing sources must still
match their prior hashes; only this fixed batch's reviewed source pages change.
"""
import argparse
import hashlib
import json
import re
import subprocess

from english_learning_sources import deep_dive_units
from run_nov18_components import AUDIT, ROOT, load


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--restore-from", help="optional full commit for a whitespace-equivalent preformat source")
    args = parser.parse_args()
    if args.restore_from and not re.fullmatch(r"[a-f0-9]{40}", args.restore_from):
        raise ValueError("full source commit required")
    accepted = set(load(AUDIT / "intake-scope.json")["accepted_papers"])
    papers = {row["domain"] + ":" + row["key"]: row
              for row in load(ROOT / "docs/research-manifest.json")["papers"]}
    changed = []
    for identity in accepted:
        page = ROOT / "docs" / papers[identity]["detail_path"]
        for path in (page, page.with_name("README-en.md")):
            old = path.read_text()
            if args.restore_from:
                baseline = subprocess.check_output(
                    ["git", "show", args.restore_from + ":" + path.relative_to(ROOT).as_posix()],
                    cwd=ROOT, text=True)
                def semantic(text):
                    return re.sub(r"\s+", "", re.sub(r"(?m)^<!-- source-sha256: [a-f0-9]{64} -->$", "", text))
                if semantic(old) != semantic(baseline):
                    raise ValueError("source changed beyond formatting: " + str(path))
                old = baseline
            lines = []
            for line in old.splitlines():
                if "$$" in line and line.strip() != "$$":
                    lines.extend(part.rstrip() for part in line.replace("$$", "\n$$\n").strip("\n").splitlines())
                else:
                    lines.append(line)
            new = "\n".join(lines) + "\n"
            if re.sub(r"\s+", "", old) != re.sub(r"\s+", "", new):
                raise ValueError("not a whitespace-only math correction")
            if new != path.read_text():
                path.write_text(new)
                changed.append(str(path.relative_to(ROOT)))
    print("format-only pages:", len(changed))
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
    for name in ("data", "eval", "agent", "root"):
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
                if update["date"] == "2026-11-18" and set(update["papers"]) & accepted:
                    for identity in update["source_revisions"]:
                        update["source_revisions"][identity] = fingerprints[identity]
            units.update(deep_dive_units({path.stem + "/" + topic: record}))
        write(path, bank)
    path = ROOT / "docs/en/learning/translations/dive-nov18-components.json"
    english = load(path)
    for key, entry in english["units"].items():
        entry["source_sha256"] = units[key].source_sha256
    write(path, english)
    for name in ("data", "agent", "eval", "root"):
        path = AUDIT / f"source-review-{name}.json"
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
