"""Normalize this unmerged batch's attribution/terminal fields and fingerprints.

No method prose, translated meaning, historical update or executed source is
changed. Re-review is required if a future edit changes more than these labels.
"""

import hashlib
import json
import re
from pathlib import Path

from english_learning_sources import deep_dive_units

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"docs/research-audits/nov23-latest"


def load(path):
    return json.loads(path.read_text())


def dump(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+"\n")


def main():
    identities=set(load(AUDIT/"intake-scope.json")["accepted_papers"])
    hashes={}
    for identity in identities:
        path=ROOT/"src/auto_research/paper_specs/catalog"/(identity.replace(":","/")+".json")
        spec=load(path)
        if spec["implementation_status"]=="deferred_high_cost":
            spec["deferral_reason"]="成本过高，不复现（审查 DONE）。 "+spec["cost_assessment"]["basis"]
            dump(path,spec)
        page=ROOT/"docs"/spec["detail_path"]
        cn=page.read_text()
        cn=cn.replace("来自[固定v1原图]", "图片来自[原论文]").replace("图片来自[固定v1原论文]", "图片来自[原论文]")
        cn=cn.replace("版权归原作者。", "版权归原作者所有。")
        page.write_text(cn)
        digest=hashlib.sha256(page.read_bytes()).hexdigest()
        hashes[identity]=digest
        english=page.with_name("README-en.md")
        text=english.read_text()
        assert len(re.findall(r"<!-- source-sha256: [0-9a-f]{64} -->",text))==1
        english.write_text(re.sub(r"<!-- source-sha256: [0-9a-f]{64} -->",f"<!-- source-sha256: {digest} -->",text))
    for group in ("foundation","agent","post","root"):
        path=AUDIT/f"paper-proposals-{group}.json"
        data=load(path)
        records=list(data["papers"].values()) if isinstance(data["papers"],dict) else data["papers"]
        for row in records:
            if row["implementation_status"]=="deferred_high_cost":
                row["deferral_reason"]="成本过高，不复现（审查 DONE）。 "+row["cost_assessment"]["basis"]
        dump(path,data)
        path=AUDIT/f"deep-dive-proposals-{group}.json"
        data=load(path)
        for row in data["proposals"]:
            for identity in set(row["source_revisions"])&identities:
                row["source_revisions"][identity]=hashes[identity]
        dump(path,data)
    for path in (ROOT/"docs/learning/deep-dives").glob("*.json"):
        data=load(path)
        changed=False
        for record in data["topics"].values():
            for update in record["updates"]:
                if update["date"]=="2026-11-23" and set(update["papers"])&identities:
                    for identity in set(update["source_revisions"])&identities:
                        update["source_revisions"][identity]=hashes[identity]
                        changed=True
        if changed:
            dump(path,data)
    units={}
    for path in (ROOT/"docs/learning/deep-dives").glob("*.json"):
        units.update(deep_dive_units({path.stem+"/"+key:row for key,row in load(path)["topics"].items()}))
    path=ROOT/"docs/en/learning/translations/dive-nov23-latest.json"
    data=load(path)
    for key,row in data["units"].items():
        row["source_sha256"]=units[key].source_sha256
    dump(path,data)
    print("Normalized only Nov23 attribution labels/terminal reasons; source and result evidence unchanged.")


if __name__=="__main__":
    main()
