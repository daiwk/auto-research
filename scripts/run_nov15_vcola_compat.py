"""Source-bound tiny random-Qwen3.5 V-CoLA compatibility checks, not 9B inference.

Runs real vision and hybrid language layers without pretrained weights, datasets
or network calls. Requires the official compact-GVA delta kernel API to execute
the new compatibility path; older dependencies are not silently treated as that
API. All three seeds share a hard 180-second, at-most-one A100/A30 budget.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import inspect
import json
import math
from pathlib import Path
import signal
import subprocess
import time

from oct18_frozen_sources import capture_sources, verify_sources

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov15-refresh/vcola-compat"
BATCH = "2026-11-15-vcola-compact-gva-compat"
SEEDS = [42, 43, 44]
MAXIMUM_SECONDS = 180
EXECUTION_FILES = [
    "scripts/run_nov15_vcola_compat.py",
    "scripts/oct18_frozen_sources.py",
    "src/auto_research/multimodal/vcola.py",
    "src/auto_research/multimodal/vcola_checkpoint.py",
    "tests/multimodal/test_vcola.py",
]


def source_hashes():
    return {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in EXECUTION_FILES}


def write_new(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def _fixture_module():
    path = ROOT / "tests/multimodal/test_vcola.py"
    spec = importlib.util.spec_from_file_location("vcola_compat_source_fixture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if Path(module.__file__).resolve() != path:
        raise ValueError("wrong source-bound tiny-model fixture")
    return module


def _validate_row(row):
    if (row.get("seed") not in SEEDS or row.get("diagnostic_only") is not True
            or row.get("evaluation_tier") != "l1_mechanism"):
        raise ValueError("wrong compatibility diagnostic identity")
    if not row.get("checks") or any(value is not True for value in row["checks"].values()):
        raise AssertionError("compatibility check failed: " + str(row["checks"]))
    if not row.get("metrics") or any(isinstance(value, bool)
            or not isinstance(value, (int, float)) or not math.isfinite(value)
            for value in row["metrics"].values()):
        raise ValueError("finite native diagnostic metrics required")


def diagnostic(seed, device, fixture):
    import torch
    from transformers.models.qwen3_5 import modeling_qwen3_5 as official

    from auto_research.multimodal import vcola, vcola_checkpoint

    for module, path in [(vcola, "src/auto_research/multimodal/vcola.py"),
                         (vcola_checkpoint, "src/auto_research/multimodal/vcola_checkpoint.py")]:
        if Path(module.__file__).resolve() != ROOT / path:
            raise ValueError("compatibility run imported an unrelated checkout")
    # Reuse the exact regression fixture's configuration, then reinitialize
    # the actual official model after setting this seed (the fixture defaults
    # to seed42 internally). No from_pretrained/model cache is consulted.
    template = fixture.tiny_model()
    config, model_class = template.config, type(template)
    del template
    torch.manual_seed(seed)
    model = model_class(config).to(device).eval().requires_grad_(False)
    backend = vcola_checkpoint.Qwen35VCoLA(model)

    # Explicit [B,S,H,D] contract. S==H_v is deliberate, and H_k==2 tests
    # consecutive head replication rather than accidental cyclic tiling.
    q, k = [torch.randn(1, 4, 2, 8, device=device) * .1 for _ in range(2)]
    value = torch.randn(1, 4, 4, 6, device=device) * .1
    decay, beta = -torch.rand(1, 4, 4, device=device), torch.rand(1, 4, 4, device=device)
    expanded_q, expanded_k = vcola_checkpoint._replay_query_key_heads(q, k, value)
    with torch.no_grad():
        compact_output, compact_state = official.torch_chunk_gated_delta_rule(
            q, k, value, g=decay, beta=beta, chunk_size=4, initial_state=None,
            output_final_state=True, use_qk_l2norm_in_kernel=True)
        repeated_output, repeated_state = official.torch_chunk_gated_delta_rule(
            q.repeat_interleave(2, dim=2), k.repeat_interleave(2, dim=2), value,
            g=decay, beta=beta, chunk_size=4, initial_state=None,
            output_final_state=True, use_qk_l2norm_in_kernel=True)
        scores = vcola.delta_state_scores(expanded_q, expanded_k, value, decay, beta)

    ids = torch.tensor([[7, 58, *([60] * 49), 59, 8, 9]], device=device)
    batch = {"input_ids": ids, "attention_mask": torch.ones_like(ids),
             "mm_token_type_ids": (ids == 60).long(),
             "pixel_values": torch.randn(196, 1536, device=device),
             "image_grid_thw": torch.tensor([[1, 14, 14]], device=device)}
    with torch.no_grad():
        expected = model(**batch, use_cache=False, logits_to_keep=1).logits[:, -1].float()
        prefix = backend.prepare(batch)
        baseline, details = backend.forward(prefix, collect_scores=True)
        compressed, compressed_details = backend.forward(prefix, remain_rate=.5, exit_layer=3)

    first = backend.text.layers[0].linear_attn
    before = dict(vars(first))
    original_forward = first.forward
    raw = inspect.unwrap(original_forward.__func__)
    original_kernel = raw.__globals__.get("torch_chunk_gated_delta_rule")
    invalid = vcola_checkpoint.VisualPrefix(
        torch.ones(1, 5, 32, device=device),
        torch.arange(5, device=device)[None, None].expand(3, 1, -1),
        torch.tensor([True, False, True, False, False], device=device), 5)
    rejected = False
    try:
        backend.forward(invalid, remain_rate=.5)
    except ValueError as error:
        if "contiguous" not in str(error):
            raise
        rejected = True

    native_device = next(model.parameters()).device.type
    checks = {
        "actual_model_on_requested_device": native_device == device,
        "compact_gva_matches_explicit_repeat_output": bool(torch.allclose(
            compact_output, repeated_output, atol=2e-5, rtol=1e-4)),
        "compact_gva_matches_explicit_repeat_state": bool(torch.allclose(
            compact_state, repeated_state, atol=2e-5, rtol=1e-4)),
        "consecutive_group_head_order": bool(torch.equal(expanded_q, q.repeat_interleave(2, dim=2))
                                              and torch.equal(expanded_k, k.repeat_interleave(2, dim=2))),
        "replay_matches_actual_compact_kernel": bool(torch.allclose(
            scores.recurrent_output, compact_output.float(), atol=2e-5, rtol=1e-4)),
        "actual_vision_encoder_token_count": int(prefix.visual_mask.sum()) == 49,
        "original_multimodal_baseline_logits_parity": bool(torch.allclose(
            baseline, expected, atol=1e-5, rtol=1e-4)),
        "state_capture_equivalent_to_actual_prefill": details["recurrence_relative_error"] < 1e-5,
        "physical_visual_merge_and_exit": [row["visual_tokens"] for row in compressed_details["layers"]]
            == [49, 24, 24, 0],
        "physical_sequence_lengths": [row["sequence_tokens"] for row in compressed_details["layers"]]
            == [54, 29, 29, 5],
        "original_text_positions_preserved": compressed_details["original_text_positions_preserved"] is True,
        "compressed_logits_finite": bool(torch.isfinite(compressed).all()),
        "noncontiguous_visual_failure_preserved": rejected,
        "failure_restores_exact_instance_fields": vars(first).keys() == before.keys()
            and all(vars(first)[name] is value for name, value in before.items()),
        "failure_restores_forward_and_module_kernel": first.forward == original_forward
            and raw.__globals__.get("torch_chunk_gated_delta_rule") is original_kernel,
    }
    metrics = {
        "compact_vs_repeated_output_max_error": float((compact_output - repeated_output).abs().max()),
        "compact_vs_repeated_state_max_error": float((compact_state - repeated_state).abs().max()),
        "replay_output_max_error": float((scores.recurrent_output - compact_output.float()).abs().max()),
        "baseline_logits_max_error": float((baseline - expected).abs().max()),
        "capture_recurrence_relative_error": float(details["recurrence_relative_error"]),
        "original_visual_tokens": 49, "merged_visual_tokens": 24, "final_sequence_tokens": 5,
        "random_model_parameters": sum(parameter.numel() for parameter in model.parameters()),
    }
    row = {"seed": seed, "execution_device": native_device, "diagnostic_only": True,
           "evaluation_tier": "l1_mechanism", "checks": checks, "metrics": metrics}
    _validate_row(row)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--source-commit")
    parser.add_argument("--frozen-proof", type=Path, default=AUDIT / "frozen-sources.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    hashes = source_hashes()
    if args.freeze:
        commit = args.source_commit or subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        proof = capture_sources(ROOT, commit, EXECUTION_FILES)
        verify_sources(ROOT, commit, hashes, proof)
        write_new(args.frozen_proof, {"schema_version": 1, "commit": commit,
                                     "source_sha256": hashes, "proof": proof})
        print(json.dumps({"frozen_commit": commit, "execution_files": len(hashes)}))
        return
    if args.source_commit is None or args.output is None:
        parser.error("--source-commit and --output required for actual execution")
    if args.output.exists():
        raise ValueError("refusing to overwrite compatibility evidence")
    frozen = json.loads(args.frozen_proof.read_text())
    if frozen["commit"] != args.source_commit or frozen["source_sha256"] != hashes:
        raise ValueError("compatibility execution sources differ from frozen commit")
    verify_sources(ROOT, args.source_commit, hashes, frozen["proof"])

    import torch
    import transformers
    torch.set_num_threads(2)
    torch.set_default_dtype(torch.float32)
    torch.set_float32_matmul_precision("highest")
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    accelerator = "CPU"
    if args.device == "cuda":
        if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
            raise ValueError("exactly one visible real NVIDIA CUDA device required")
        accelerator = torch.cuda.get_device_name(0)
        if not accelerator.startswith(("NVIDIA A100", "NVIDIA A30")):
            raise ValueError("this short-budget validation requires an A100 or A30")
        torch.cuda.synchronize()

    def time_limit(signum, frame):
        raise TimeoutError("180-second V-CoLA compatibility budget exceeded; no automatic retry")

    started = time.monotonic()
    previous_handler = signal.signal(signal.SIGALRM, time_limit)
    signal.setitimer(signal.ITIMER_REAL, MAXIMUM_SECONDS)
    try:
        fixture = _fixture_module()
        rows = [diagnostic(seed, args.device, fixture) for seed in SEEDS]
        if args.device == "cuda":
            torch.cuda.synchronize()
        elapsed = time.monotonic() - started
        if elapsed > MAXIMUM_SECONDS:
            raise TimeoutError("180-second V-CoLA compatibility budget exceeded")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
    verify_sources(ROOT, args.source_commit, hashes, frozen["proof"])
    output = {"schema_version": 2, "batch": BATCH, "device": args.device,
              "accelerator": accelerator, "transformers_version": transformers.__version__,
              "seeds": SEEDS, "code_commit": args.source_commit, "source_sha256": hashes,
              "execution_source_proof": frozen["proof"], "per_seed": rows,
              "elapsed_seconds": elapsed, "maximum_run_seconds": MAXIMUM_SECONDS,
              "model_scope": "random tiny Qwen3.5 from regression-test configuration; not a pretrained 9B checkpoint",
              "model_configuration": {"text_hidden_size": 32, "text_layers": 4,
                                      "vision_hidden_size": 16, "vision_layers": 1,
                                      "vocabulary_size": 64, "one_image_visual_tokens": 49},
              "input_scope": "seeded random pixel patches and synthetic Q/K/V, no gold task answers",
              "precision": "float32; TF32 disabled for numerical reference parity",
              "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
              "formal_comparison": False, "promotion_eligible": False, "evolve_integrated": False,
              "pretrained_model_calls": 0, "model_and_dataset_downloads": 0, "api_calls": 0,
              "full_experiments_executed": False, "automatic_retry": False}
    write_new(args.output, output)
    print(json.dumps({"seeds": SEEDS, "device": args.device, "accelerator": accelerator,
                      "transformers_version": transformers.__version__, "elapsed_seconds": elapsed}))


if __name__ == "__main__":
    main()
