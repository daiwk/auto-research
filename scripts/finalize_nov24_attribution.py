"""Normalize attribution only, preserving all frozen execution evidence.

The reviewed Chinese wording becomes the mandatory figure-attribution label.
English meaning and scientific content do not change. Update only this batch's
authored README fingerprints and derived English deep-dive unit fingerprints.
"""
import hashlib
import json
import re
from pathlib import Path

from english_learning_sources import deep_dive_units

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"docs/research-audits/nov24-latest"


def load(path):
    return json.loads(path.read_text())


def dump(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+"\n")


def refresh_revisions(value, hashes):
    if isinstance(value, dict):
        for key, item in value.items():
            if key=="source_revisions" and isinstance(item, dict):
                for identity in set(item)&set(hashes):
                    item[identity]=hashes[identity]
            else:
                refresh_revisions(item,hashes)
    elif isinstance(value,list):
        for item in value:
            refresh_revisions(item,hashes)


def main():
    hashes={}
    for identity in load(AUDIT/"intake-scope.json")["accepted_papers"]:
        spec=load(ROOT/"src/auto_research/paper_specs/catalog"/(identity.replace(":","/")+".json"))
        page=ROOT/"docs"/spec["detail_path"]
        text=page.read_text()
        text=text.replace("图来自[固定v1原始SVG]","图片来自[原论文]")
        text=text.replace("原图/算法来自[固定v1论文]","图片来自[原论文]")
        text=text.replace("版权归原作者。","版权归原作者所有。")
        if "图片来自[原论文]" not in text:
            marker="固定版本PDF原图与完整原图注"
            if marker not in text:
                raise ValueError("unreviewed attribution variant: "+identity)
            text=text.replace(marker,f"图片来自[原论文]({spec['reviewed_version_url']})；"+marker)
        if "版权归原作者所有" not in text:
            raise ValueError("missing copyright ownership: "+identity)
        page.write_text(text)
        digest=hashlib.sha256(page.read_bytes()).hexdigest()
        hashes[identity]=digest
        english=page.with_name("README-en.md")
        en=english.read_text()
        assert len(re.findall(r"<!-- source-sha256: [0-9a-f]{64} -->",en))==1
        english.write_text(re.sub(r"<!-- source-sha256: [0-9a-f]{64} -->",f"<!-- source-sha256: {digest} -->",en))
    for pattern in ("deep-dive-proposals-*.json","*-review.json"):
        for path in AUDIT.glob(pattern):
            data=load(path)
            refresh_revisions(data,hashes)
            dump(path,data)
    for path in (ROOT/"docs/learning/deep-dives").glob("*.json"):
        data=load(path)
        changed=False
        for record in data["topics"].values():
            for update in record["updates"]:
                if update["date"]=="2026-11-24" and set(update["papers"])&set(hashes):
                    refresh_revisions(update,hashes)
                    changed=True
        if changed:
            dump(path,data)
    units={}
    for path in (ROOT/"docs/learning/deep-dives").glob("*.json"):
        units.update(deep_dive_units({path.stem+"/"+key:row for key,row in load(path)["topics"].items()}))
    path=ROOT/"docs/en/learning/translations/dive-nov24-latest.json"
    data=load(path)
    for key,row in data["units"].items():
        row["source_sha256"]=units[key].source_sha256
    dump(path,data)
    print("Attribution labels and Nov24 fingerprints normalized; scientific prose and executed source unchanged.")


if __name__=="__main__":
    main()
