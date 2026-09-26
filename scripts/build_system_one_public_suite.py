#!/usr/bin/env python3
"""Build the versioned System One public calibration/test/OOD benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


SOURCES = {
    "boolq": ("google/boolq", "default", "validation", "CC BY-SA 3.0"),
    "helpsteer2": ("nvidia/HelpSteer2", "default", "validation", "CC BY 4.0"),
    "pubmedqa": ("qiaojin/PubMedQA", "pqa_labeled", "train", "MIT"),
    "arc-challenge": ("allenai/ai2_arc", "ARC-Challenge", "validation", "CC BY-SA 4.0"),
    "truthfulqa": ("truthfulqa/truthful_qa", "multiple_choice", "validation", "Apache-2.0"),
}


def fetch(name: str, offset: int, length: int):
    dataset, config, split, license_name = SOURCES[name]
    url = "https://datasets-server.huggingface.co/rows?" + urlencode({
        "dataset": dataset, "config": config, "split": split,
        "offset": offset, "length": length,
    })
    with urlopen(url, timeout=90) as response:
        payload = response.read()
    decoded = json.loads(payload)
    if decoded.get("truncated_cells") or len(decoded.get("rows", ())) != length:
        raise ValueError(f"{name}: dataset response is truncated or incomplete")
    return decoded["rows"], {
        "dataset": dataset, "config": config, "split": split,
        "license": license_name, "url": url,
        "response_sha256": hashlib.sha256(payload).hexdigest(),
    }


def record(name: str, raw: dict, split: str) -> dict:
    row, index = raw["row"], raw["row_idx"]
    base = {"id": f"{name}-{index}", "source": name, "family": name,
            "source_row": index, "split": split}
    if name == "boolq":
        return {**base, "domain": "verification", "input": {
            "state": {"passage": row["passage"], "question": row["question"]},
            "questions": {"decision": {"type": "noul", "instructions":
                "Does the passage answer the question with yes? Use only the passage."}}},
            "reference": {"target": bool(row["answer"]), "human_reviewed": True}}
    if name == "helpsteer2":
        return {**base, "domain": "rubric-rating", "input": {
            "state": {"prompt": row["prompt"], "response": row["response"]},
            "questions": {"decision": {"type": "score", "instructions":
                "Rate how helpful this response is from 0 to 4.", "criteria": {
                    str(i): text for i, text in enumerate(("not helpful", "mostly unhelpful",
                        "partly helpful", "helpful", "fully helpful"))}}}},
            "reference": {"target": int(row["helpfulness"]), "human_reviewed": True}}
    if name == "pubmedqa":
        return {**base, "domain": "medical-verification", "input": {
            "state": {"question": row["question"],
                      "abstract_context": row["context"]["contexts"]},
            "questions": {"decision": {"type": "choice", "instructions":
                "Based only on the abstract, answer the research question.",
                "criteria": {"yes": "yes", "no": "no", "maybe": "maybe"}}}},
            "reference": {"target": row["final_decision"], "human_reviewed": True}}
    if name == "arc-challenge":
        labels, texts = row["choices"]["label"], row["choices"]["text"]
        return {**base, "domain": "science-reasoning", "input": {
            "state": {"question": row["question"]}, "questions": {"decision": {
                "type": "choice", "instructions": "Choose the best answer.",
                "criteria": dict(zip(labels, texts))}}},
            "reference": {"target": row["answerKey"], "human_reviewed": True}}
    choices, labels = row["mc1_targets"]["choices"], row["mc1_targets"]["labels"]
    keys = [chr(65 + i) for i in range(len(choices))]
    return {**base, "domain": "truthfulness", "input": {
        "state": {"question": row["question"]}, "questions": {"decision": {
            "type": "choice", "instructions": "Choose the truthful answer.",
            "criteria": dict(zip(keys, choices))}}},
        "reference": {"target": keys[labels.index(1)], "human_reviewed": True}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records, sources = [], {}
    for name in ("boolq", "helpsteer2", "pubmedqa"):
        rows, info = fetch(name, 0, 40)
        sources[name] = info
        records.extend(record(name, row, "calibration" if i < 20 else "test")
                       for i, row in enumerate(rows))
    for name in ("arc-challenge", "truthfulqa"):
        rows, info = fetch(name, 0, 40)
        sources[name] = info
        records.extend(record(name, row, "ood") for row in rows)
    if len(records) != 200 or len({row["id"] for row in records}) != 200:
        raise ValueError("formal suite requires exactly 200 unique examples")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n"
                                   for row in records), encoding="utf-8")
    counts = {split: sum(row["split"] == split for row in records)
              for split in ("calibration", "test", "ood")}
    manifest = {
        "schema_version": 2, "benchmark": "system-one-public-v1",
        "purpose": "formal public checkpoint comparison and Evolve selection",
        "selection": "fixed first rows; no model-dependent filtering",
        "split_policy": "calibration selects genome; test/OOD remain isolated until champion",
        "records": len(records), "counts": counts, "sources": sources,
        "dataset_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
    }
    args.output.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
