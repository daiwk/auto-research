"""Controlled auxiliary-label CUDA diagnostics, NOT an official benchmark.

The vision checkpoint, causal KV decoder, recurrent policy and losses are real.
Only teacher annotations and the all-failed reward scenario are explicit test
fixtures. No gold answers are read; no capability result is produced.
"""
import argparse
import json
from pathlib import Path

import torch
from PIL import Image
from transformers import AutoModelForImageTextToText, AutoProcessor

from auto_research.multimodal.vimod import DART, TRACE
from auto_research.multimodal.vimod_checkpoint import SmolVLMJointKV


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--image", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="cuda")
    args = p.parse_args()
    torch.manual_seed(args.seed)
    processor = AutoProcessor.from_pretrained(args.checkpoint, local_files_only=True)
    model = AutoModelForImageTextToText.from_pretrained(
        args.checkpoint, local_files_only=True, dtype=torch.bfloat16,
        attn_implementation="eager").to(args.device)
    dimensions = model.config.text_config.hidden_size
    head_dim = dimensions // model.config.text_config.num_attention_heads
    dart = DART(dimensions, head_dim, affinity_dim=32, upper=8).to(args.device)
    trace = TRACE(dimensions, dimensions, layers=3, state_dim=64, key_dim=32).to(args.device)
    backend = SmolVLMJointKV(model, processor, dart, trace)
    image = Image.open(args.image).convert("RGB")
    question = "Describe the map briefly."
    with torch.no_grad():
        bank = backend.prefill(image, question)
    # First-group evidence is a declared gradient fixture, not an annotation
    # attributed to a real teacher or the public dataset.
    first = torch.where(bank.memory.membership == 0)[0].tolist()
    second = torch.where(bank.memory.membership == 1)[0].tolist()
    text = "This is a controlled runtime diagnostic response with several tokens."
    response_tokens = len(processor.tokenizer(text, add_special_tokens=False)["input_ids"])
    evidence = [first if i % 2 == 0 else second for i in range((response_tokens + 3) // 4)]
    metrics = {}
    for stage in ("set", "joint", "rl"):
        before = torch.cat([parameter.detach().flatten() for parameter in trace.parameters()]).clone()
        optimizer = torch.optim.AdamW(trace.parameters(), lr=1e-4)
        optimizer.zero_grad()
        if stage == "rl":
            groups = len(bank.memory.counts)

            def teacher(*, image, question, prefix):
                del image, question, prefix
                return {"labels": [1] + [0] * (groups - 1), "valid": [1] * groups}

            loss, statistics = backend.trace_rl_loss(image, question, lambda _: False, teacher,
                                                     group=2, maximum_tokens=5, routing_interval=4)
            metrics.update({f"rl_{key}": value for key, value in statistics.items()})
        else:
            loss = backend.trace_supervised_loss(image, question, text, evidence,
                                                stage=stage, routing_interval=4)
        loss.backward()
        gradient = sum(float(parameter.grad.detach().square().sum())
                       for parameter in trace.parameters() if parameter.grad is not None) ** .5
        optimizer.step()
        after = torch.cat([parameter.detach().flatten() for parameter in trace.parameters()])
        delta = float((after - before).norm())
        if not gradient > 0 or not delta > 0 or not torch.isfinite(loss):
            raise RuntimeError(f"{stage} did not execute a finite nonzero training update")
        metrics.update({f"{stage}_loss": float(loss.detach()), f"{stage}_gradient_norm": gradient,
                        f"{stage}_parameter_delta": delta})
        print(json.dumps({"stage": stage, "gradient_norm": gradient, "parameter_delta": delta}), flush=True)
    report = {"seed": args.seed, "diagnostic_only": True, "evaluation_tier": "L1",
              "annotation_source": "controlled synthetic auxiliary labels, not real teacher",
              "reward_source": "explicit all-failed verifier fixture, no gold access",
              "metrics": metrics}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
