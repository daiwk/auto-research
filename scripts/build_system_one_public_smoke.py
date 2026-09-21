#!/usr/bin/env python3
"""Build a tiny, traceable Choice/Noul/Score smoke suite from human labels."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


SOURCES = {
    "boolq": {
        "dataset": "google/boolq", "config": "default", "split": "validation",
        "license": "CC BY-SA 3.0",
    },
    "helpsteer2": {
        "dataset": "nvidia/HelpSteer2", "config": "default", "split": "validation",
        "license": "CC BY 4.0",
    },
    "pubmedqa": {
        "dataset": "qiaojin/PubMedQA", "config": "pqa_labeled", "split": "train",
        "license": "MIT",
    },
}


def _fetch(spec):
    query = urlencode({
        "dataset": spec["dataset"], "config": spec["config"],
        "split": spec["split"],
    })
    url = f"https://datasets-server.huggingface.co/first-rows?{query}"
    with urlopen(url, timeout=60) as response:
        payload = response.read()
    return url, payload, json.loads(payload)["rows"]


def _record(name, raw):
    if name == "boolq":
        return {
            "id": f"boolq-{raw['row_idx']}", "domain": "verification",
            "family": name,
            "input": {"state": {"passage": raw["row"]["passage"],
                                  "question": raw["row"]["question"]},
                      "questions": {"decision": {"type": "noul",
                          "instructions": "Does the passage answer the question with yes? Use only the passage."}}},
            "reference": {"target": bool(raw["row"]["answer"]),
                          "human_reviewed": True},
        }
    if name == "helpsteer2":
        return {
            "id": f"helpsteer2-{raw['row_idx']}", "domain": "rubric-rating",
            "family": name,
            "input": {"state": {"prompt": raw["row"]["prompt"],
                                  "response": raw["row"]["response"]},
                      "questions": {"decision": {"type": "score",
                          "instructions": "Rate how helpful this response is from 0 to 4.",
                          "criteria": {str(i): label for i, label in enumerate((
                              "not helpful", "mostly unhelpful", "partly helpful",
                              "helpful", "fully helpful"))}}}},
            "reference": {"target": int(raw["row"]["helpfulness"]),
                          "human_reviewed": True},
        }
    context = raw["row"]["context"]["contexts"]
    return {
        "id": f"pubmedqa-{raw['row_idx']}", "domain": "medical-verification",
        "family": name,
        "input": {"state": {"question": raw["row"]["question"],
                              "abstract_context": context},
                  "questions": {"decision": {"type": "choice",
                      "instructions": "Based only on the abstract, answer the research question.",
                      "criteria": {"yes": "yes", "no": "no", "maybe": "maybe"}}}},
        "reference": {"target": raw["row"]["final_decision"],
                      "human_reviewed": True},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    downloaded = {}
    raw_rows = {}
    for name, spec in SOURCES.items():
        url, payload, rows = _fetch(spec)
        downloaded[name] = {
            **spec, "url": url, "response_sha256": hashlib.sha256(payload).hexdigest(),
        }
        raw_rows[name] = rows
    order = (("boolq", 0), ("helpsteer2", 0), ("pubmedqa", 0),
             ("boolq", 1), ("helpsteer2", 1), ("pubmedqa", 1))
    records = [
        _record(name, raw_rows[name][index])
        for name, index in order
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records),
        encoding="utf-8",
    )
    manifest = args.output.with_suffix(".manifest.json")
    manifest.write_text(json.dumps({
        "schema_version": 1,
        "purpose": "GPU path smoke validation; not a formal benchmark result",
        "selection": "first two rows from each public split; no model-dependent selection",
        "family_split_key": "source dataset; rows from one source cannot cross validation/test",
        "types": ["choice", "noul", "score"],
        "records": len(records),
        "sources": downloaded,
        "dataset_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
