"""Curate source-bound component evidence and append the exact accepted16 batch.

Frozen Google39 review snapshots are inputs, never rewritten. A component or
protocol delivery is not a full experiment or a capability/evolve promotion.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from auto_research.gpu_validation import validate_gpu_receipt  # noqa: E402

AUDIT = ROOT / "docs/research-audits/google16-components-20261021"
PREVIOUS = ROOT / "docs/research-audits/google-meta-closeout-20261021/google39-reviews.json"
BATCH = "20261021-google16-affordable-components"
KEYS = {
    "2601.19066": "dynamic-brt", "2601.21149": "me-pois", "2602.06276": "attribution-sets",
    "2602.07918": "causal-armor", "2602.12481": "spatial-ads", "2602.16938": "convapparel",
    "2602.17554": "modular-robust-generative", "2603.01293": "data-quality-lsa",
    "2603.14769": "polca", "2603.29791": "simula", "2604.05364": "tfrbench",
    "2604.23099": "proeval", "2604.27723": "mild", "2605.26340": "scientist-one",
    "2608.05578": "activation-model-scanner", "2609.12464": "hcrg",
}
GPU_KEYS = {"me-pois", "modular-robust-generative", "data-quality-lsa", "activation-model-scanner", "causal-armor"}
EVALUATION = {"convapparel", "simula", "tfrbench", "scientist-one"}
EVAL_COMMIT = "6873b033"  # resolved to its immutable full object below
EVAL_SOURCE_COMMIT = "6873b033"  # expanded during evidence import; no runtime capture claim
SOURCE_PROOFS = {}
CHECK_MODE = False
RAW_NAMES = ["google16-statistics-frozen-seed42.json", "google16-agent-cpu-final-seed42.json",
    "google16-neural-final-a100-seed42.json", "google16-causal-raw-a100-seed42.json",
    *[f"google16-{key}-final-seed42.json" for key in sorted(EVALUATION)]]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value, check):
    text = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n"
    if check:
        if not path.is_file() or path.read_text() != text:
            raise ValueError(f"stale component artifact: {path.relative_to(ROOT)}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def verify_sources(raw):
    commit = raw.get("code_commit") or raw.get("source_commit")
    sources = raw.get("source_sha256")
    if not commit or len(commit) != 40 or not sources:
        raise ValueError("raw run needs exact frozen source identity")
    for path, digest in sources.items():
        content = source_content(commit, path)
        if hashlib.sha256(content).hexdigest() != digest:
            raise ValueError(f"executed code differs from frozen source: {path}")
    return commit


def source_content(commit, path):
    """Keep frozen executed public source after a squash merge/fresh clone.

    Initial import checks Git's committed file. Subsequent checks verify the
    preserved content hashes, not a mutable current module or missing old ref.
    """
    identity = f"{commit}:{path}"
    if identity in SOURCE_PROOFS:
        return SOURCE_PROOFS[identity].encode()
    if CHECK_MODE:
        raise ValueError(f"missing executed-source snapshot: {identity}")
    content = subprocess.check_output(["git", "show", identity], cwd=ROOT)
    SOURCE_PROOFS[identity] = content.decode()
    return content


def finite_metrics(metrics):
    if not metrics or any(not isinstance(v, (int, float, bool)) or not math.isfinite(v)
                          for v in metrics.values()):
        raise ValueError("finite nonempty scalar diagnostic metrics required")
    return metrics


def observations():
    paths = {name: AUDIT / "evidence" / name for name in RAW_NAMES}
    stats = read(paths[RAW_NAMES[0]])
    agent = read(paths[RAW_NAMES[1]])
    neural = read(paths[RAW_NAMES[2]])
    causal = read(paths[RAW_NAMES[3]])
    for raw in (stats, agent, neural, causal):
        verify_sources(raw)
        if raw.get("diagnostic_only") is not True:
            raise ValueError("all current observations are diagnostics")
    if (neural.get("completed") is not True or neural.get("device") != "cuda"
            or "A100" not in neural.get("accelerator_model", "")
            or not causal.get("actual_model_device", "").startswith("cuda")
            or "A100" not in causal.get("accelerator", "")):
        raise ValueError("completed actual A100 run required; CPU fallback forbidden")
    output = {}
    for key, metrics in stats["components"].items():
        output[key] = (metrics, stats, paths[RAW_NAMES[0]])
    for key, component in neural["components"].items():
        output[key] = (component["metrics"], neural, paths[RAW_NAMES[2]])
    attribution = causal["attribution"]
    output["causal-armor"] = ({"forward_batches": causal["forward_calls"],
        "scoring_contexts": attribution["scoring_contexts"], "action_tokens": attribution["action_tokens"],
        "user_influence": attribution["user_influence"],
        "tool_span_influence": attribution["span_influences"][0][1],
        "flagged_spans": len(attribution["flagged_indices"]), "security_accuracy_measured": False},
        causal, paths[RAW_NAMES[3]])
    for component in agent["components"]:
        key = component["method"]
        if key == "dynamic-brt":
            metrics = {"candidate_reviews": len(component["reviews"]), "model_generated_candidates": 0,
                       "semantic_reviewer_observed": False}
        elif key == "polca":
            metrics = {"controller_rounds": len(component["traces"]), "metric_calls": component["metric_calls"],
                       "real_llm_calls": component["real_llm_calls"], "history_items": len(component["history"])}
        else:
            metrics = {"graph_nodes": len(component["graph"]["nodes"]),
                       "three_hop_nodes": len(component["three_hop_keys"]), "llm_migration_calls": 0}
        output[key] = (metrics, agent, paths[RAW_NAMES[1]])
    eval_commit = EVAL_SOURCE_COMMIT
    for key in EVALUATION:
        path = paths[f"google16-{key}-final-seed42.json"]
        raw = read(path)
        if not raw.get("fixture_demo") or raw.get("model_calls") != 0 or raw.get("status") != "completed":
            raise ValueError("evaluation interface receipts are explicitly model-free fixtures")
        # The original runner has no runtime source-capture field. Bind the
        # curator-verified frozen files separately, not as a fabricated raw field.
        files = ["scripts/run_google16_evaluation.py",
                 f"src/auto_research/agent_research/google16_{key.replace('-', '_')}.py"]
        for file in files:
            frozen = source_content(eval_commit, file)
            if not CHECK_MODE and frozen != (ROOT/file).read_bytes():
                raise ValueError("evaluation source changed since the recorded execution freeze")
        bound = {**raw, "curator_verified_source_commit": eval_commit}
        output[key] = (raw["metrics"], bound, path)
    if set(output) != set(KEYS.values()):
        raise ValueError("exact16 component inventory differs")
    return output


def build(check=False):
    global CHECK_MODE, SOURCE_PROOFS, EVAL_SOURCE_COMMIT
    CHECK_MODE = check
    proof_path = AUDIT/"evidence/executed-source-snapshots.json"
    if proof_path.exists():
        document = read(proof_path)
        SOURCE_PROOFS = document["files"]
        EVAL_SOURCE_COMMIT = document["evaluation_interface_source_commit"]
    elif not check:
        EVAL_SOURCE_COMMIT = subprocess.check_output(
            ["git", "rev-parse", EVAL_COMMIT], cwd=ROOT, text=True).strip()
    prior = {r["id"]: r for r in read(PREVIOUS)["records"] if r["review_decision"] == "accepted"}
    if set(prior) != set(KEYS):
        raise ValueError("accepted16 scope changed")
    specs = {}
    for path in (ROOT/"src/auto_research/paper_specs/catalog").glob("*/*.json"):
        row = read(path)
        if row["key"] in KEYS.values():
            if row["key"] in specs:
                raise ValueError("duplicate component catalog identity")
            specs[row["key"]] = row
    observations_by_key = observations()
    write(proof_path, {"schema_version": 1,
        "scope": "public executed component source only, retained for squash-merge-safe hash checks",
        "evaluation_interface_source_commit": EVAL_SOURCE_COMMIT,
        "files": dict(sorted(SOURCE_PROOFS.items()))}, check)
    rows = []
    for identity, key in KEYS.items():
        spec = specs[key]
        metrics, raw, raw_path = observations_by_key[key]
        metrics = finite_metrics(metrics)
        commit = (raw.get("code_commit") or raw.get("source_commit")
                  or raw["curator_verified_source_commit"])
        gpu = key in GPU_KEYS
        folder = ROOT/"docs"/Path(spec["detail_path"]).parent
        old_names = sorted((folder/"metrics").glob("*.json"))
        filename = old_names[0].name if len(old_names) == 1 else f"component-{'a100' if gpu else 'cpu'}-seed42.json"
        artifact = str((folder/"metrics"/filename).relative_to(ROOT))
        dataset = (raw["components"][key].get("corpus") if key == "activation-model-scanner"
                   else raw.get("dataset")) or {
            "id": "repository-authored-mathematical-or-protocol-fixtures", "revision": commit,
            "public_benchmark": False}
        payload = {"schema_version": 2, "manifest_ref": f"{spec['domain']}:{key}",
            "adapter_key": key, "evaluation_tier": spec["evaluation_tier"], "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False, "formal_comparison": False, "seed": 42,
            "device": "cuda" if gpu else "cpu", "dataset": dataset, "metrics": metrics,
            "full_experiment_status": spec["full_experiment_status"],
            "evaluation_protocol": {"tier": spec["evaluation_tier"], "seeds": [42],
                "formal_comparison": False, "claim_policy": "bounded component/protocol only, not paper capability"},
            "provenance": {"artifact_path": artifact, "code_commit": commit,
                "dataset_fingerprint": hashlib.sha256(json.dumps(dataset, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
                "raw_result_path": str(raw_path.relative_to(ROOT)), "raw_result_sha256": sha(raw_path),
                "source_binding": "raw_captured_hashes" if raw.get("source_sha256") else "curator_verified_frozen_files"}}
        if key in EVALUATION:
            payload.update(fixture_demo=raw["fixture_demo"], model_calls=raw["model_calls"],
                           report=raw["report"], status=raw["status"])
        if gpu:
            checkpoint = (raw["components"][key]["checkpoint"] if key == "activation-model-scanner" else
                          raw["checkpoint"] if key == "causal-armor" else
                          {"id": "none-mathematical-fixtures", "revision": commit})
            receipt_path = f"docs/gpu-validations/{key}-a100-20261021.json"
            receipt = {"schema_version": 1, "adapter_key": key, "validated_at": "2026-10-21",
                "accelerator": {"vendor": "NVIDIA", "model": raw.get("accelerator_model") or raw["accelerator"]},
                "command": [part for part in spec["local_command"].split() if part != "PYTHONPATH=src"],
                "dataset": dataset, "checkpoint": checkpoint,
                "seed": 42, "result": "passed", "diagnostic_only": True, "promotion_eligible": False,
                "evolve_integrated": False, "evaluation_tier": spec["evaluation_tier"],
                "metrics": metrics, "success_criterion": "bounded runtime/provenance/formulas, not paper capability",
                "executed_source_sha256": raw["source_sha256"],
                "provenance": {"commit": commit, "artifact_path": receipt_path,
                    "raw_result_path": str(raw_path.relative_to(ROOT)), "raw_result_sha256": sha(raw_path)}}
            errors = validate_gpu_receipt(receipt)
            if errors:
                raise ValueError(errors)
            write(ROOT/receipt_path, receipt, check)
            payload["gpu_validation_artifact"] = receipt_path
        write(ROOT/artifact, payload, check)
        old = prior[identity]
        rows.append({"id": identity, "title": spec["title"], "track": old["track"], "key": key,
            "component_key": key, "status": "implemented", "priority": "P1",
            "review_decision": "component_implemented", "implementation_status": spec["implementation_status"],
            "resolution": "component_implemented", "review_done": True,
            "full_experiment_resolution": spec["full_experiment_status"],
            "automatic_retry": False, "automatic_implementation_queue": False,
            "evolve_integrated": False, "promotion_eligible": False, "diagnostic_only": True,
            "evaluation_tier": spec["evaluation_tier"], "reason": spec["summary"],
            "doc": spec["detail_path"], "source_url": old["source_url"],
            "cost_assessment": {**deepcopy(old["cost_assessment"]),
                "component_decision": "explicit user-authorized bounded component/protocol delivered",
                "full_experiment_decision": spec["full_experiment_status"]},
            "full_text_review": {**deepcopy(old["full_text_review"]), "scope": "full-text",
                "source_locations": old["full_text_review"]["read_sections"],
                "supplementary_method_review": spec["detail_path"]},
            "component_evidence": artifact, "review_artifact": "research-audits/google16-components-20261021/README.md",
            "requires_gpu_validation": gpu,
            **({"gpu_validation_artifact": receipt_path} if gpu else {})})
    batch = {"batch": BATCH, "date": "2026-10-21", "scope_kind": "accepted16-affordable-components",
        "required_tracks": [], "review_watermark_advanced": False, "all_sources_exhaustive": False,
        "candidates": rows}
    ledger_path = ROOT/"docs/paper-discovery-ledger.json"
    ledger = read(ledger_path)
    existing = [i for i, b in enumerate(ledger["batches"]) if b["batch"] == BATCH]
    if len(existing) > 1:
        raise ValueError("duplicate batch")
    if existing:
        ledger["batches"][existing[0]] = batch
    else:
        ledger["batches"].append(batch)
    write(ledger_path, ledger, check)
    scope = {"schema_version": 1, "batch": BATCH, "accepted_ids": list(KEYS),
        "component_count": 16, "gpu_validated_component_count": len(GPU_KEYS),
        "implementation_status_counts": dict(Counter(r["implementation_status"] for r in rows)),
        "full_experiment_resolution_counts": dict(Counter(r["full_experiment_resolution"] for r in rows)),
        "all_components_are_diagnostic": True, "capability_reproductions_claimed": 0,
        "review_watermark_advanced": False, "all_sources_exhaustive": False, "records": rows}
    write(AUDIT/"task-scope.json", scope, check)
    sync_figures(specs, check)
    return scope


def sync_figures(specs, check):
    from PIL import Image
    path = ROOT/"docs/paper-figures-manifest.json"
    manifest = read(path)
    output = [row for row in manifest if row.get("arxiv_id") not in KEYS]
    for key, spec in sorted(specs.items()):
        page = ROOT/"docs"/spec["detail_path"]
        image = page.parent/"assets/paper-figure-01.png"
        if not image.is_file():
            raise ValueError(f"missing reviewed paper figure: {key}")
        prov_path = image.parent/"provenance.json"
        prov = read(prov_path) if prov_path.is_file() else {}
        if prov.get("image_sha256") and sha(image) != prov["image_sha256"]:
            raise ValueError("paper figure source hash changed")
        if prov.get("asset_sha256") and sha(image) != prov["asset_sha256"]:
            raise ValueError("paper figure crop hash changed")
        source = prov.get("source_url") or prov.get("source_pdf_url")
        figure = prov.get("figure_label") or prov.get("figure")
        if not source:
            match = re.search(r"\[!\[([^]]+)\]\(assets/paper-figure-01.png\)\]\((https://arxiv.org/[^)]+)\)", page.read_text())
            if not match:
                raise ValueError(f"figure primary source missing: {key}")
            figure, source = match.groups()
        with Image.open(image) as im:
            width, height = im.size
        output.append({"page": str(page.relative_to(ROOT)), "paper_url": spec["paper_url"],
            "arxiv_id": spec["paper_url"].rstrip('/').split('/')[-1],
            "figure": figure, "original_caption": "", "source_url": source,
            "extraction": "primary-source-image-or-reviewed-pdf-crop",
            "asset": str(image.relative_to(ROOT)), "width": width, "height": height,
            "score": 0, "error": "", "sha256": sha(image),
            "visually_inspected": True})
    write(path, output, check)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--import-dir", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.import_dir:
        if args.check:
            parser.error("check cannot import")
        for name in RAW_NAMES:
            value = read(args.import_dir/name)
            path = AUDIT/"evidence"/name
            if path.exists() and read(path) != value:
                raise ValueError("immutable raw evidence already exists with different content")
            write(path, value, False)
        # Earlier runs are evidence, not current passing receipts. Keep them
        # outside metrics/dashboard discovery and label why they were replaced.
        for name, reason in (
            ("google16-neural-raw-a100-seed42.json", "superseded AMS block-index and practical NLL convention; not current validation"),
            ("google16-agent-cpu-frozen-seed42.json", "superseded HCRG resolution and POLCA rollout representation"),
        ):
            source = args.import_dir/name
            if source.is_file():
                write(AUDIT/"evidence/superseded"/name,
                      {"current_validation": False, "superseded_reason": reason, "raw_run": read(source)}, False)
    scope = build(args.check)
    print(json.dumps({name: scope[name] for name in ("component_count", "gpu_validated_component_count",
                    "implementation_status_counts", "full_experiment_resolution_counts")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
