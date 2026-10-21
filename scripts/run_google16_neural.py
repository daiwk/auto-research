#!/usr/bin/env python3
"""Four bounded component diagnostics; no model/data downloads or generation.

Synthetic math fixtures only test defining equations/gradients. Optional AMS
uses a real cached public checkpoint and caller-pinned prompt corpus, but its
scores are not validated safety classifications or capability measurements.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

import torch

from auto_research.foundation_models.google16_me_pois import (
    MobilityPrototypeLoss, transferred_visit_distribution,
)
from auto_research.foundation_models.google16_robust_gate import (
    cached_router_nll, gated_mass, primal_dual_step, sir_resample,
)
from auto_research.foundation_models.google16_data_quality_lsa import (
    closest_sft_value, outcome_supervision_loss, population_initialization,
    rollout, sft_loss,
)
from auto_research.foundation_models.google16_ams import (
    SCALE_CONVENTION, compare_fingerprints, extract_last_token_activations,
    select_concept_layer, tier_one,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ["scripts/run_google16_neural.py", *[
    f"src/auto_research/foundation_models/google16_{name}.py"
    for name in ("me_pois", "robust_gate", "data_quality_lsa", "ams")]]


def hash_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def me_pois_diagnostic(device: str) -> dict:
    model = MobilityPrototypeLoss(6, 8, 5, 4).to(device)
    visits = torch.randn(8, 8, device=device, requires_grad=True)
    poi_ids = torch.tensor([0, 1, 2, 3, 4, 5, 0, 1], device=device)
    anchors = torch.tensor([0, 1], device=device)
    sparse = torch.tensor([2, 3, 4, 5], device=device)
    hist = torch.tensor([[8., 0., 2., 0.], [0., 4., 0., 6.]], device=device)
    prior = transferred_visit_distribution(
        torch.tensor([[0., 1.], [1., 0.], [2., 0.], [3., 0.]], device=device),
        torch.tensor([[0., 0.], [3., 1.]], device=device), hist,
        torch.tensor([.5, 1., 3.], device=device))
    terms = model(visits, poi_ids, torch.randn(6, 5, device=device), anchors,
                  hist / hist.sum(-1, keepdim=True), sparse, prior)
    terms["loss"].backward()
    return {"fixture_only": True, "metrics": {
        **{key: float(value.detach()) for key, value in terms.items()},
        "prior_row_sum_error_max": float((prior.sum(-1) - 1).abs().max()),
        "prototype_gradient_norm": float(model.prototypes.grad.norm()),
        "visit_gradient_norm": float(visits.grad.norm()),
        "temporal_gradient_norm": float(model.temporal[0].weight.grad.norm()),
        "text_projection_gradient_norm": float(model.text_projection.weight.grad.norm()),
    }}


def robust_gate_diagnostic(device: str, steps: int, seed: int) -> dict:
    experts = torch.tensor([[.7, .15, .1, .05], [.05, .1, .15, .7]], device=device)
    domains = torch.tensor([[.6, .2, .15, .05], [.05, .15, .2, .6]], device=device)
    logits = torch.nn.Parameter(torch.zeros(4, 2, device=device))
    optimizer = torch.optim.AdamW([logits], lr=.01, weight_decay=0)
    adversary = torch.full((2,), .5, device=device)
    dual = torch.zeros((), device=device)
    initial = gated_mass(experts, logits).detach()
    trajectory = []
    for _ in range(steps):
        state = primal_dual_step(logits, experts, domains, adversary, dual, optimizer)
        adversary, dual = state["adversary"], state["dual"]
        trajectory.append({key: float(state[key]) for key in ("partition", "objective")})
    final = gated_mass(experts, logits).detach()
    generator = torch.Generator(device=device).manual_seed(seed)
    samples = sir_resample(experts, logits, 16, 32, generator)
    router = torch.randn(2, 3, 2, device=device, requires_grad=True)
    cached = torch.tensor([[[.7, .1], [.1, .6], [.4, .3]]], device=device).repeat(2, 1, 1).log()
    distillation = cached_router_nll(router, cached)
    distillation.backward()
    return {"fixture_only": True, "adversary_objective": "practical_domain_nll_not_theory_kl",
            "normalization_estimator": "exact_finite_support_no_MC_or_EMA", "trajectory": trajectory, "metrics": {
        "steps": steps, "initial_partition": float(initial.sum()), "final_partition": float(final.sum()),
        "global_partition_residual": float(abs(final.sum() - 1)),
        "adversary_sum_error": float(abs(adversary.sum() - 1)), "dual": float(dual),
        "gate_change_l1": float((final - initial).abs().sum()),
        "sir_samples": len(samples), "sir_distinct_outcomes": len(samples.unique()),
        "cached_router_nll": float(distillation.detach()), "router_gradient_norm": float(router.grad.norm()),
    }}


def lsa_diagnostic(device: str) -> dict:
    dim, batch, n = 4, 6, 8
    covariance = torch.diag(torch.tensor([1., 1., 2., 2.], device=device))
    x = torch.randn(batch, n, dim, device=device) @ torch.linalg.cholesky(covariance).T
    weights = torch.randn(batch, dim, device=device)
    y = (x @ weights[..., None]).squeeze(-1)
    value, query_key = population_initialization(covariance, n)
    value, query_key = value.requires_grad_(), query_key.requires_grad_()
    sft = sft_loss(x, y, weights, value, query_key, 2, .3)
    outcome = outcome_supervision_loss(x, y, weights, value, query_key, 3)
    (sft + outcome).backward()
    predicted = rollout(x, y, value.detach(), query_key.detach(), 3)
    solution = closest_sft_value(x, weights, covariance, .3)
    empirical = x.transpose(-2, -1) @ x / n
    phi = (empirical @ weights[..., None]).squeeze(-1).T
    # Normal equations, not fitting a benchmark or asserting a theory trend.
    residual = (solution @ phi + .3 * weights.T) @ phi.T
    return {"fixture_only": True, "metrics": {
        "sft_loss": float(sft.detach()), "os_regression_loss": float(outcome.detach()),
        "value_gradient_norm": float(value.grad.norm()), "query_key_gradient_norm": float(query_key.grad.norm()),
        "rollout_steps": predicted.shape[1], "closed_form_normal_equation_max_error": float(residual.abs().max()),
    }, "os_is_policy_gradient_rl": False, "inference_receives_target_weight": False}


def ams_checkpoint_diagnostic(checkpoint: Path, model_id: str, revision: str,
                              concepts_path: Path, device: str) -> dict:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    if not checkpoint.is_dir() or not re.fullmatch(r"[0-9a-f]{40}", revision) or not model_id:
        raise ValueError("cached checkpoint and exact public revision/model-id required")
    weight_paths = sorted(checkpoint.glob("*.safetensors"))
    if not weight_paths or sum(path.stat().st_size for path in weight_paths) > 2_200_000_000:
        raise ValueError("AMS cost gate requires cached safetensors total <=2.2GB")
    corpus = json.loads(concepts_path.read_text())
    if not corpus.get("source_url") or not re.fullmatch(r"[0-9a-f]{40}", corpus.get("revision", "")) or set(corpus["concepts"]) != {
        "harmful_content", "injection_resistance", "refusal_capability"
    }:
        raise ValueError("three named concepts plus pinned public corpus provenance required")
    for rows in corpus["concepts"].values():
        if not isinstance(rows, list) or not 2 <= len(rows) <= 16 or any(
            not isinstance(row, dict) or set(row) != {"positive", "negative"}
            or any(not isinstance(value, str) or not value for value in row.values()) for row in rows
        ):
            raise ValueError("each concept requires 2–16 nonempty positive/negative prompt pairs")
    tokenizer = AutoTokenizer.from_pretrained(str(checkpoint), local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        str(checkpoint), local_files_only=True, trust_remote_code=False,
        dtype=torch.float32, attn_implementation="eager").to(device).eval()
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    fingerprints, serialized = {}, {}
    for name, rows in corpus["concepts"].items():
        positive, layers = extract_last_token_activations(model, tokenizer, [r["positive"] for r in rows], device=device)
        negative, other = extract_last_token_activations(model, tokenizer, [r["negative"] for r in rows], device=device)
        if layers != other:
            raise ValueError("inconsistent hidden-state layer identities")
        fingerprint = select_concept_layer(positive, negative, layers)
        fingerprints[name] = fingerprint
        serialized[name] = {"layer": fingerprint.layer, "separation": fingerprint.separation,
                            "pairs": fingerprint.pairs, "direction": fingerprint.direction.cpu().tolist(),
                            "self_comparison": compare_fingerprints(fingerprint, fingerprint)}
    artifact = {"fixture_only": False, "checkpoint": {"id": model_id, "revision": revision,
                "weight_sha256": {p.name: hash_file(p) for p in weight_paths}},
                "corpus": {"source_url": corpus["source_url"], "revision": corpus["revision"],
                           "sha256": hash_file(concepts_path), "protocol": corpus.get("protocol", "custom_concepts")},
                "metrics": {"concepts": len(serialized),
                            "forward_passes": sum(2 * len(rows) for rows in corpus["concepts"].values()),
                            "minimum_separation": min(f.separation for f in fingerprints.values())},
                "fingerprints": serialized, "reference_band_not_safety_verdict": tier_one(fingerprints),
                "scale_convention": SCALE_CONVENTION, "safety_capability_validated": False,
                "independent_baseline_used": False, "generation_calls": 0}
    del model
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--model-id")
    parser.add_argument("--revision")
    parser.add_argument("--concepts", type=Path)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=16)
    parser.add_argument("--source-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA requested but unavailable; CPU fallback forbidden")
    if not 1 <= args.steps <= 64:
        raise SystemExit("bounded finite-support gate supports 1–64 steps")
    if any((args.checkpoint, args.model_id, args.revision, args.concepts)) and not all(
        (args.checkpoint, args.model_id, args.revision, args.concepts)
    ):
        raise SystemExit("checkpoint, model-id, revision and concepts must be specified together")
    if args.output.exists():
        raise SystemExit("immutable run output already exists")
    source_commit = args.source_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise SystemExit("full frozen source commit required")
    torch.manual_seed(args.seed)
    torch.set_num_threads(1)
    start = time.monotonic()
    result = {"schema_version": 2, "protocol": "google16-neural-components-l1-v1",
              "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
              "seed": args.seed, "code_commit": source_commit,
              "source_sha256": {name: hash_file(ROOT / name) for name in SOURCES},
              "device": args.device, "accelerator_model": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
              "created_at_utc": datetime.now(timezone.utc).isoformat(),
              "components": {}, "full_experiments_reproduced": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Preserve partial/failing evidence; completed is set only after all requested paths.
    def save():
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    try:
        for key, function in (("me-pois", lambda: me_pois_diagnostic(args.device)),
                              ("modular-robust-generative", lambda: robust_gate_diagnostic(args.device, args.steps, args.seed)),
                              ("data-quality-lsa", lambda: lsa_diagnostic(args.device))):
            result["components"][key] = function()
            save()
        if args.checkpoint:
            result["components"]["activation-model-scanner"] = ams_checkpoint_diagnostic(
                args.checkpoint, args.model_id, args.revision, args.concepts, args.device)
        else:
            result["ams_checkpoint_run"] = "not_requested_not_validated"
        result["completed"] = True
    except Exception as exc:
        result["completed"] = False
        result["failure"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    finally:
        result["elapsed_seconds"] = time.monotonic() - start
        save()


if __name__ == "__main__":
    main()
