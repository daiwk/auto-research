"""Actual SmolVLM DART training and TRACE Joint-KV inference smoke.

Requires public training records, never silently trains on a benchmark test.
TRACE weights must be supplied for a capability comparison; randomly initialized
TRACE inference is expressly a routing/runtime diagnostic.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shlex
import subprocess

import torch
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor

from auto_research.multimodal.vimod import DART, TRACE
from auto_research.multimodal.vimod_checkpoint import SmolVLMJointKV


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--checkpoint-id", required=True)
    p.add_argument("--checkpoint-revision", required=True)
    p.add_argument("--train-jsonl", type=Path, required=True)
    p.add_argument("--dataset-id", required=True)
    p.add_argument("--dataset-revision", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--steps", type=int, default=3)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="cpu")
    p.add_argument("--trace-weights", type=Path)
    p.add_argument("--dart-weights", type=Path)
    p.add_argument("--phase", choices=("dart", "trace-set", "trace-joint", "trace-rl"), default="dart")
    p.add_argument("--online-teacher-command")
    p.add_argument("--group", type=int, default=16)
    args = p.parse_args()
    if args.steps < 1:
        p.error("positive steps required")
    rows = [json.loads(line) for line in args.train_jsonl.read_text().splitlines() if line.strip()]
    if not rows or any(row.get("split") != "train" or not row.get("verified")
                       or not row.get("response") for row in rows):
        p.error("verified public training records required: image, question, response, split=train")
    for row in rows:
        image_path = Path(row["image"])
        row["image"] = str(image_path if image_path.is_absolute() else args.train_jsonl.parent / image_path)
    torch.manual_seed(args.seed)
    processor = AutoProcessor.from_pretrained(args.checkpoint, local_files_only=True)
    dtype = torch.bfloat16 if args.device == "cuda" else torch.float32
    model = AutoModelForImageTextToText.from_pretrained(
        args.checkpoint, local_files_only=True, dtype=dtype,
        attn_implementation="eager").to(args.device)
    text_config = model.config.text_config
    dimensions = text_config.hidden_size
    head_dim = dimensions // text_config.num_attention_heads
    dart = DART(dimensions, head_dim, affinity_dim=32, upper=8).to(args.device)
    trace = TRACE(dimensions, dimensions, layers=3, state_dim=64, key_dim=32).to(args.device)
    if args.trace_weights:
        trace.load_state_dict(torch.load(args.trace_weights, map_location=args.device, weights_only=True))
    if args.dart_weights:
        dart.load_state_dict(torch.load(args.dart_weights, map_location=args.device, weights_only=True))
    if args.phase != "dart" and not args.dart_weights:
        p.error("TRACE training requires trained DART weights")
    if args.phase == "trace-joint" and not args.trace_weights:
        p.error("joint stage requires set-stage TRACE weights")
    if args.phase == "trace-rl" and (not args.trace_weights or not args.online_teacher_command):
        p.error("RL requires joint-stage weights and a real causal online teacher command")
    if args.phase in ("trace-set", "trace-joint") and any(not row.get("evidence_by_segment") for row in rows):
        p.error("TRACE SFT requires explicit upstream evidence_by_segment Fine-index annotations")
    backend = SmolVLMJointKV(model, processor, dart, trace, group_size=4)
    trained_module = dart if args.phase == "dart" else trace
    optimizer = torch.optim.AdamW(trained_module.parameters(), lr=1e-5 if args.phase == "dart" else 1e-4,
                                 weight_decay=0.)
    before = torch.cat([parameter.detach().flatten() for parameter in trained_module.parameters()]).clone()
    history = []
    for step in range(args.steps):
        row = rows[step % len(rows)]
        image = Image.open(row["image"]).convert("RGB")
        dart.train()
        optimizer.zero_grad()
        if args.phase == "dart":
            loss = backend.distill_response(image, row["question"], row["response"], maximum_tokens=4)
        elif args.phase in ("trace-set", "trace-joint"):
            loss = backend.trace_supervised_loss(image, row["question"], row["response"],
                                                row["evidence_by_segment"],
                                                stage="set" if args.phase == "trace-set" else "joint",
                                                routing_interval=4)
        else:
            def teacher(*, image, question, prefix):
                request = {"image": row["image"], "question": question, "prefix": prefix,
                           "evidence_group_contract": "return labels and valid arrays aligned with DART groups"}
                output = subprocess.run(shlex.split(args.online_teacher_command), input=json.dumps(request),
                                        text=True, capture_output=True, check=True, timeout=180)
                return json.loads(output.stdout)

            # External task verifier sees output/reference; neither reaches
            # TRACE hidden observations or the causal online teacher request.
            def verifier(text):
                import re
                matches = re.findall(r"\b([A-Z])\b", text)
                return bool(matches and matches[-1] == row["response"].strip())

            loss, _ = backend.trace_rl_loss(image, row["question"], verifier, teacher,
                                            group=args.group, maximum_tokens=20, routing_interval=4)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(trained_module.parameters(), 1.)
        optimizer.step()
        history.append(float(loss.detach()))
        print(json.dumps({"step": step, "loss": history[-1]}), flush=True)
    after = torch.cat([parameter.detach().flatten() for parameter in trained_module.parameters()])
    dart.eval()
    trace.eval()
    # Training example decode verifies runtime wiring only. It is not a test score.
    row = rows[0]
    generation = backend.generate(Image.open(row["image"]).convert("RGB"), row["question"],
                                  maximum_tokens=20, routing_interval=4)
    report = {"seed": args.seed, "training_steps": args.steps,
              "dataset": {"id": args.dataset_id, "revision": args.dataset_revision},
              "checkpoint": {"id": args.checkpoint_id, "revision": args.checkpoint_revision},
              "diagnostic_only": True, "evaluation_tier": "L1",
              "fidelity": "core_mechanism", "phase": args.phase, "training_loss_history": history,
              "parameter_delta": float((after - before).norm()),
              "trace_trained": args.phase != "dart" or args.trace_weights is not None,
              "joint_kv_generation": generation,
              "limitations": ["SmolVLM rather than Qwen3-VL",
                               ("4-token verified response DART training budget" if args.phase == "dart"
                                else "20-token on-policy rollout budget" if args.phase == "trace-rl"
                                else "explicit annotated response TRACE supervised training"),
                               ("TRACE has not been trained in this run" if args.phase == "dart" and not args.trace_weights
                                else "TRACE weights trained or explicitly supplied; no capability qualification"),
                               "no held-out capability score or efficiency claim"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(dart.state_dict(), args.output.with_suffix(".dart.pt"))
    torch.save(trace.state_dict(), args.output.with_suffix(".trace.pt"))
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
