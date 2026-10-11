#!/usr/bin/env python3
"""CPU-only replay of pinned public SWE-agent logs; never runs their commands.

Calibration selects lambda and a severe-flag-density policy without seeing
evaluation labels. This bounded replay is not a live SWE-bench capability run.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import time

import numpy as np

from auto_research.agent_research.ontrack import MonitorConfig, OnTrackMonitor, Reference
from auto_research.agent_research.ontrack_replay import auc, instance_id, paired_auc_interval, parse_trace, partition_instances

DATASET = "sailplane/swe-agent-trajs"
DATA_REVISION = "04eb93df490e7fbb7b6e8358da8145aba6f5a25c"
EMBEDDING = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
SEVERE = {"LOOP", "STALLED", "OFF_TRACK", "CAUSAL_INVERSION", "BLOCK"}


class CpuEmbeddings:
    def __init__(self, cache):
        import torch
        from transformers import AutoModel, AutoTokenizer
        self.torch = torch
        torch.set_num_threads(1)
        self.tokenizer = AutoTokenizer.from_pretrained(EMBEDDING, revision=EMBEDDING_REVISION, cache_dir=cache)
        self.model = AutoModel.from_pretrained(EMBEDDING, revision=EMBEDDING_REVISION, cache_dir=cache).to("cpu").eval()
        self.cache = {}

    def prime(self, texts):
        pending = list(dict.fromkeys(text[:4096] for text in texts if text[:4096] not in self.cache))
        for start in range(0, len(pending), 32):
            batch = pending[start:start + 32]
            inputs = self.tokenizer(batch, padding=True, truncation=True, max_length=256, return_tensors="pt")
            with self.torch.no_grad():
                hidden = self.model(**inputs).last_hidden_state
                mask = inputs["attention_mask"].unsqueeze(-1)
                means = (hidden * mask).sum(1) / mask.sum(1).clamp_min(1)
                vectors = self.torch.nn.functional.normalize(means, dim=1).numpy()
            self.cache.update(zip(batch, vectors))

    def __call__(self, texts):
        self.prime(texts)
        return np.array([self.cache[text[:4096]] for text in texts])


def replay(rows, references, embed, *, relaxation, steps):
    result = []
    for row in rows:
        monitor = OnTrackMonitor(embed, references=references, config=MonitorConfig(relaxation=relaxation))
        start = time.perf_counter()
        signals = [monitor.admit(e) for e in row["events"][:steps]]
        density = [sum(x["verdict"] in SEVERE for x in signals[max(0, i - 5):i + 1]) /
                   len(signals[max(0, i - 5):i + 1]) for i in range(len(signals))]
        pooled = np.mean(embed([e.action for e in row["events"][:steps]]), axis=0)
        pooled /= max(np.linalg.norm(pooled), 1e-12)
        cosine = max(float(pooled @ np.mean(embed([e.action for e in ref.events]), axis=0) /
                           max(np.linalg.norm(np.mean(embed([e.action for e in ref.events]), axis=0)), 1e-12)) for ref in references)
        result.append({"instance_id": row["instance_id"], "score": signals[-1]["score"],
                       "cosine": cosine, "maximum_severe_density": max(density),
                       "verdicts": [x["verdict"] for x in signals],
                       "escalations": sum(x["escalated"] for x in signals),
                       "finalization": monitor.finalize(),
                       "elapsed_seconds": time.perf_counter() - start})
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cache", type=Path, default=Path(".cache/ontrack-public"))
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--calibration-instances", type=int, default=64)
    p.add_argument("--reference-pool", type=int, default=32)
    p.add_argument("--references", type=int, default=3)
    p.add_argument("--evaluation-instances", type=int, default=64)
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("--reference-steps", type=int, default=24)
    p.add_argument("--seed", type=int, default=42)
    a = p.parse_args()
    if min(a.references, a.steps, a.reference_steps, a.evaluation_instances) < 1:
        p.error("positive replay budgets required")
    from huggingface_hub import hf_hub_download
    import pyarrow.parquet as pq
    path = hf_hub_download(DATASET, "data/train-00000-of-00001.parquet", repo_type="dataset",
                           revision=DATA_REVISION, cache_dir=a.cache / "dataset")
    data_hash = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if data_hash != "ed6c7d9a0f39fcfbb890eedd72bdf0ccfe295ac7a1f17b468f787515bdbe201e":
        raise ValueError("public dataset differs from pinned content")
    parsed, rejected = [], 0
    for raw in pq.read_table(path, columns=["trajectory", "filename", "resolved"]).to_pylist():
        try:
            events = parse_trace(raw)
            if len(events) < a.steps:
                continue
            parsed.append({"instance_id": instance_id(raw["filename"]), "events": events, "resolved": bool(raw["resolved"])})
        except (ValueError, TypeError, KeyError):
            rejected += 1
    partitions = partition_instances([r["instance_id"] for r in parsed], seed=a.seed,
                                     calibration=a.calibration_instances, reference_pool=a.reference_pool)
    by_id = {}
    for row in parsed:
        if row["instance_id"] in by_id:
            raise ValueError("multiple traces per instance require clustered scoring, not silently duplicated rows")
        by_id[row["instance_id"]] = row
    calibration = [by_id[i] for i in partitions["calibration"]]
    pool = [by_id[i] for i in partitions["reference_pool"]]
    reference_rows = [r for r in pool if r["resolved"]][:a.references]
    if len(reference_rows) < a.references:
        raise ValueError("too few mined successes in isolated reference pool")
    evaluation = [by_id[i] for i in partitions["evaluation"][:a.evaluation_instances]]
    references = [Reference(r["events"][:a.reference_steps], "mined") for r in reference_rows]
    embed = CpuEmbeddings(a.cache / "embedding")
    embed.prime([text for r in [*calibration, *evaluation, *reference_rows]
                 for e in r["events"][:max(a.steps, a.reference_steps)]
                 for text in (e.action, e.arguments, e.effect)])
    labels = [r["resolved"] for r in calibration]
    sweep = []
    for relaxation in (.01, .05, .1, .2, .3, .5, 1.):
        rows = replay(calibration, references, embed, relaxation=relaxation, steps=a.steps)
        value = auc(labels, [r["score"] for r in rows])
        if value is None:
            raise ValueError("calibration needs both outcome classes")
        sweep.append({"relaxation": relaxation, "auc": value, "rows": rows})
        print(json.dumps({"phase": "calibration", "relaxation": relaxation, "auc": value}), flush=True)
    chosen = max(sweep, key=lambda r: r["auc"])
    threshold_sweep = []
    for threshold in (.2, .4, .6, .7, .9, 1.):
        selected = [r["maximum_severe_density"] > threshold for r in chosen["rows"]]
        false = sum(s and label for s, label in zip(selected, labels)) / sum(labels)
        true = sum(s and not label for s, label in zip(selected, labels)) / sum(not x for x in labels)
        threshold_sweep.append({"threshold": threshold, "false_stop": false, "true_stop": true})
    policy = max((r for r in threshold_sweep if r["false_stop"] <= .1), key=lambda r: (r["true_stop"], r["threshold"]))
    # Evaluation is invoked only after both choices are frozen.
    result = replay(evaluation, references, embed, relaxation=chosen["relaxation"], steps=a.steps)
    labels = [r["resolved"] for r in evaluation]
    stopped = [r["maximum_severe_density"] > policy["threshold"] for r in result]
    metrics = {"evaluation_instances": len(result), "resolved": sum(labels),
               "ontrack_auc": auc(labels, [r["score"] for r in result]),
               "cosine_auc": auc(labels, [r["cosine"] for r in result]),
               "paired_auc_difference_ci95": paired_auc_interval(labels, [r["score"] for r in result],
                                                                  [r["cosine"] for r in result], seed=a.seed),
               "false_stop_count": sum(s and label for s, label in zip(stopped, labels)),
               "true_stop_count": sum(s and not label for s, label in zip(stopped, labels)),
               "maximum_score": max(r["score"] for r in result), "minimum_score": min(r["score"] for r in result)}
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    report = {"schema_version": 2, "manifest_ref": "agent-research:ontrack", "method": "ontrack",
              "dataset": DATASET, "seeds": [a.seed], "metrics": metrics,
              "evaluation_protocol": {"tier": "l2_public", "diagnostic_only": False, "formal_comparison": False,
                                      "seeds": [a.seed], "claim_policy": "bounded public-log replay, not live Agent capability or production safety"},
              "checkpoint": {"id": EMBEDDING, "revision": EMBEDDING_REVISION, "device": "cpu"},
              "dataset_provenance": {"id": DATASET, "revision": DATA_REVISION, "sha256": data_hash,
                                     "parsed": len(parsed), "malformed": rejected},
              "configuration": {"seed": a.seed, "steps": a.steps, "reference_steps": a.reference_steps,
                                "selected_relaxation": chosen["relaxation"], "abort_policy": policy,
                                "thresholds": asdict(MonitorConfig(relaxation=chosen["relaxation"]))},
              "calibration": [{k: v for k, v in r.items() if k != "rows"} for r in sweep],
              "policy_calibration": threshold_sweep,
              "partition_ids": {**partitions, "evaluation": [r["instance_id"] for r in evaluation]},
              "reference_ids": [r["instance_id"] for r in reference_rows],
              "rows": [{**r, "resolved": label, "counterfactual_stop": stop} for r, label, stop in zip(result, labels, stopped)],
              "provenance": {"original_code_commit": commit, "artifact_path": str(a.output),
                             "dataset_fingerprint": data_hash},
              "limitations": ["CPU-only; no trajectory commands executed; no live SWE-bench claimed",
                              "path-string extractor is not complete dependency tracing; no bitset runtime claim",
                              "first k events and truncated references; not original 2294-trace protocol",
                              "one instance-disjoint seed, no multi-seed stable capability improvement claim",
                              "abort is counterfactual flag density, not measured dollar savings",
                              "reference labels stay external to monitored event/embedding input"]}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    print(json.dumps(metrics), flush=True)


if __name__ == "__main__":
    main()
