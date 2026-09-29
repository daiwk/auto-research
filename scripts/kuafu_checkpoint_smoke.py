#!/usr/bin/env python3
"""Bounded real-checkpoint CUDA smoke for KuaFu training stages.

This is a mechanism test, not a paper-result reproduction: it does not
estimate MRQA EM/F1. Do not use its losses as
evidence that KuaFu improves over an uncompressed baseline.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--mrqa-train", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--judge-checkpoint", type=Path)
    parser.add_argument("--rl-max-tokens", type=int, default=48)
    parser.add_argument("--rl-group-size", type=int, default=4)
    parser.add_argument("--rl-temperature", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from auto_research.reproductions.llm_lora import inject_lora
    from auto_research.reproductions.kuafu.model import KuafuSystem, TwoAxisProjector
    from auto_research.reproductions.kuafu.mrqa import load_mrqa
    from auto_research.reproductions.kuafu.rl import (
        build_source_judge_prompt, parse_judge_response, train_hallucination_step,
    )

    if not torch.cuda.is_available():
        raise RuntimeError("this validation path requires an NVIDIA GPU")
    torch.manual_seed(args.seed)
    example = load_mrqa(args.mrqa_train, expected_split="train", limit=1)[0]
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint, local_files_only=True)

    def load():
        model = AutoModelForCausalLM.from_pretrained(
            args.checkpoint, dtype=torch.bfloat16, local_files_only=True,
            attn_implementation="sdpa",
        ).to("cuda")
        inject_lora(model, rank=4, alpha=8)
        return model

    encoder, decoder = load(), load()
    width = encoder.config.hidden_size
    projector = TwoAxisProjector(width, 128, 4, 2).to(device="cuda", dtype=torch.bfloat16)
    system = KuafuSystem(encoder, decoder, projector)
    item = tokenizer(example.items[0], add_special_tokens=False,
                     truncation=True, max_length=24, return_tensors="pt").input_ids[0]
    question = tokenizer(example.question, add_special_tokens=False,
                         truncation=True, max_length=24, return_tensors="pt").input_ids[0]
    answer = tokenizer(example.answers[0], add_special_tokens=False,
                       truncation=True, max_length=12, return_tensors="pt").input_ids[0]
    if not item.numel() or not question.numel() or not answer.numel():
        raise RuntimeError("tokenizer produced an empty MRQA example")
    stages = (
        ("reconstruction", False, item),
        ("compressed_qa", True, answer),
        ("co_training", True, answer),
    )
    losses = {}
    for stage, projected, target in stages:
        system.set_stage(stage)
        optimizer = torch.optim.AdamW(
            [p for p in system.parameters() if p.requires_grad], lr=1e-5
        )
        optimizer.zero_grad(set_to_none=True)
        loss = system.sequence_loss(
            [item], prompt_ids=question, target_ids=target, projected=projected,
            residual_scale=1.0 if stage != "co_training" else 0.5,
        )
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite {stage} loss")
        loss.backward()
        if system.memory_embeddings.grad is None:
            raise RuntimeError(f"{stage} did not backpropagate to memory tokens")
        optimizer.step()
        losses[stage] = float(loss.detach().cpu())
    rl_result = None
    if args.judge_checkpoint:
        judge_tokenizer = AutoTokenizer.from_pretrained(
            args.judge_checkpoint, local_files_only=True
        )
        judge_model = AutoModelForCausalLM.from_pretrained(
            args.judge_checkpoint, dtype=torch.bfloat16, local_files_only=True,
            attn_implementation="sdpa",
        ).to("cuda").eval()
        for parameter in judge_model.parameters():
            parameter.requires_grad_(False)

        def judge(source: str, question_text: str, response: str):
            prompt = build_source_judge_prompt(source, question_text, response)
            chat = judge_tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}], tokenize=False,
                add_generation_prompt=True,
            )
            encoded = judge_tokenizer(chat, return_tensors="pt",
                                      truncation=True, max_length=1536).to("cuda")
            with torch.no_grad():
                generated = judge_model.generate(
                    **encoded, do_sample=False, max_new_tokens=96,
                    pad_token_id=judge_tokenizer.eos_token_id,
                )
            answer_text = judge_tokenizer.decode(
                generated[0, encoded.input_ids.shape[1]:], skip_special_tokens=True
            )
            return parse_judge_response(answer_text)

        system.set_stage("hallucination_rl")
        optimizer = torch.optim.AdamW(
            [p for p in system.decoder.parameters() if p.requires_grad], lr=1e-5
        )
        rl_question = tokenizer.apply_chat_template(
            [{"role": "user", "content": (
                example.question + " Answer with a short phrase only."
            )}], tokenize=True, add_generation_prompt=True,
            return_tensors="pt",
        )[0]
        trace = []
        rl_result = train_hallucination_step(
            system, item_ids=[item], prompt_ids=rl_question,
            source=" ".join(example.items), question=example.question,
            decode=lambda ids: tokenizer.decode(ids, skip_special_tokens=True),
            judge=judge, optimizer=optimizer,
            eos_token_id=tokenizer.eos_token_id,
            generator=torch.Generator().manual_seed(args.seed),
            group_size=args.rl_group_size, max_tokens=args.rl_max_tokens,
            temperature=args.rl_temperature, trace=trace,
        )
        rl_result["diagnostic_trace"] = trace
    rl_updated = rl_result is not None and rl_result.get("status") == "updated"
    result = {
        "status": "passed",
        "scope": "bounded-four-stage-cuda-smoke" if rl_updated else "three-supervised-stage-cuda-smoke",
        "diagnostic_only": True, "seed": args.seed,
        "accelerator": "NVIDIA A100", "memory_tokens": 4,
        "cached_tokens": 2, "cache_width": 128, "backbone_width": width,
        "losses": losses, "rl": rl_result,
        "paper_result_reproduced": False,
        "missing": (["MRQA EM/F1", "equal-budget baseline", "three-seed comparison"]
                    if rl_updated else ["hallucination-aware RL", "MRQA EM/F1",
                                       "equal-budget baseline", "three-seed comparison"]),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
