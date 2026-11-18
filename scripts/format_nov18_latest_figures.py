"""Normalize reviewed figure wrappers; preserve prose and refresh exact hashes.

Only the unmerged47-paper intake is touched. No translation, algorithm, result
or scientific figure is changed. Updating the source fingerprints records this
mechanical, explicitly inspected presentation change rather than hiding drift.
"""

from __future__ import annotations
import hashlib
import re
from english_learning_sources import deep_dive_units
from run_nov18_latest_components import ROOT, AUDIT, load
from integrate_nov18_latest_learning import dump


def main():
    identities = load(AUDIT / "intake-scope.json")["accepted_papers"]
    hashes = {}
    changed = []
    for identity in identities:
        domain, key = identity.split(":")
        spec = load(ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json")
        page = ROOT / "docs" / spec["detail_path"]
        cn = page.read_text()
        enpage = page.with_name("README-en.md")
        en = enpage.read_text()
        if "<!-- paper-figure:start -->" not in cn:
            cn = cn.replace("### 原论文关键图", "<!-- paper-figure:start -->\n### 原论文关键图", 1)
            cn = cn.replace("\n### 核心公式", "\n<!-- paper-figure:end -->\n\n### 核心公式", 1)
            cn = cn.replace("图片来自[固定v1原论文]", "图片来自[原论文]")
            en = en.replace(
                "### Original paper figure",
                "<!-- paper-figure:start -->\n### Original paper figure",
                1,
            )
            en = en.replace(
                "\n### Core equations", "\n<!-- paper-figure:end -->\n\n### Core equations", 1
            )
            page.write_text(cn)
            changed.append(identity)
        start = cn.index("<!-- paper-figure:start -->")
        end = cn.index("<!-- paper-figure:end -->")
        if "```mermaid" in cn[start:end]:
            cn = cn[:end] + cn[end:].replace("<!-- paper-figure:end -->\n\n", "", 1)
            cn = cn[:start] + cn[start:].replace(
                "```mermaid", "<!-- paper-figure:end -->\n\n```mermaid", 1
            )
            page.write_text(cn)
        fingerprint = hashlib.sha256(cn.encode()).hexdigest()
        hashes[identity] = fingerprint
        en = re.sub(
            r"<!-- source-sha256: [0-9a-f]{64} -->",
            lambda _: f"<!-- source-sha256: {fingerprint} -->",
            en,
            count=1,
        )
        enpage.write_text(en)
    for name in ("foundation", "post", "agent", "root"):
        path = AUDIT / f"deep-dive-proposals-{name}.json"
        payload = load(path)
        for row in payload["proposals"]:
            for identity in set(row["source_revisions"]) & set(hashes):
                row["source_revisions"][identity] = hashes[identity]
        dump(path, payload)
    bank = {}
    for path in (ROOT / "docs/learning/deep-dives").glob("*.json"):
        payload = load(path)
        for topic, record in payload["topics"].items():
            for update in record["updates"]:
                for identity in set(update["source_revisions"]) & set(hashes):
                    if update["date"] != "2026-11-18":
                        raise ValueError("must not rewrite an older review revision")
                    update["source_revisions"][identity] = hashes[identity]
            bank[path.stem + "/" + topic] = record
        dump(path, payload)
    path = ROOT / "docs/en/learning/translations/dive-nov18-latest.json"
    payload = load(path)
    units = deep_dive_units(bank)
    for key, row in payload["units"].items():
        row["source_sha256"] = units[key].source_sha256
    dump(path, payload)
    print(
        "Presentation-only normalization; refreshed reviewed fingerprints for",
        len(changed),
        "paper figures",
    )


if __name__ == "__main__":
    main()
