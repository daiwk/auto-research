"""Bounded Qwen3-4B DCE/SRCL diagnostic on official public GSM8K files.

This does not reproduce the paper's OpenThoughts/AIME/HMMT benchmark. Train
and validation are disjoint official train rows; test is official GSM8K test
and is read only after training. The executable path requires CUDA.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import random

from auto_research.datasets import GSM8K_REVISION, gsm8k
from auto_research.post_training.recursive_opsd import (
    _prompt_ids, numeric_answer, student_prompt, train_round,
)
from auto_research.post_training.local_lora import attach_lora


QWEN_ID = "Qwen/Qwen3-4B-Instruct-2507"
QWEN_REVISION = "cdbee75f17c01a7cc42f958dc650907174af0554"


def _evaluate(model, tokenizer, rows, *, max_new_tokens):
    import torch

    model.eval()
    correct = 0
    total_tokens = 0
    with torch.no_grad():
        for row in rows:
            prompt = _prompt_ids(tokenizer, student_prompt(row["question"]))
            output = model.generate(
                input_ids=torch.tensor([prompt], device=next(model.parameters()).device),
                attention_mask=torch.ones((1, len(prompt)), device=next(model.parameters()).device),
                max_new_tokens=max_new_tokens, do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )[0, len(prompt):].tolist()
            answer = numeric_answer(tokenizer.decode(output, skip_special_tokens=True))
            gold = numeric_answer(row["answer"])
            correct += int(answer is not None and answer == gold)
            total_tokens += len(output)
    return {
        "accuracy": correct / len(rows),
        "correct": correct,
        "examples": len(rows),
        "mean_generated_tokens": total_tokens / len(rows),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=2)
    parser.add_argument("--train-examples", type=int, default=8)
    parser.add_argument("--validation-examples", type=int, default=4)
    parser.add_argument("--test-examples", type=int, default=4)
    parser.add_argument("--max-new-tokens", type=int, default=96)
    parser.add_argument("--teacher-mode", choices=("dynamic", "frozen"), default="dynamic")
    parser.add_argument("--lambda-guidance", type=float, default=1.0)
    parser.add_argument("--lambda-srcl", type=float, default=0.1)
    args = parser.parse_args()
    if min(args.steps, args.train_examples, args.validation_examples, args.test_examples) < 1:
        parser.error("all sample counts and steps must be positive")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not torch.cuda.is_available():
        raise RuntimeError("Qwen3-4B DCE/SRCL validation requires a real CUDA device")
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    rows = gsm8k(args.data_dir, allow_network=False)
    needed = args.train_examples + args.validation_examples
    if len(rows["train"]) < needed or len(rows["test"]) < args.test_examples:
        raise ValueError("official GSM8K files contain too few examples")
    train = rows["train"][:args.train_examples]
    validation = rows["train"][args.train_examples:needed]
    test = rows["test"][:args.test_examples]
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.checkpoint, local_files_only=True, dtype=torch.bfloat16,
        attn_implementation="sdpa",
    ).to("cuda")
    model = attach_lora(model, target_modules=("q_proj", "v_proj"), rank=8, alpha=16)
    optimizer = torch.optim.AdamW(
        (parameter for parameter in model.parameters() if parameter.requires_grad), lr=5e-6,
    )
    initial_adapters = {
        name: parameter.detach().clone()
        for name, parameter in model.named_parameters() if parameter.requires_grad
    }
    baseline_validation = _evaluate(model, tokenizer, validation, max_new_tokens=args.max_new_tokens)
    history = []
    for step in range(args.steps):
        row = train[step % len(train)]
        result = train_round(
            model, tokenizer, optimizer, problem=row["question"],
            gold_solution=row["answer"], max_new_tokens=args.max_new_tokens,
            lambda_guidance=args.lambda_guidance, lambda_srcl=args.lambda_srcl,
            teacher_mode=args.teacher_mode,
        )
        history.append({"step": step + 1, **asdict(result)})
    final_validation = _evaluate(model, tokenizer, validation, max_new_tokens=args.max_new_tokens)
    adapter_parameter_delta_l2 = sum(
        (parameter.detach() - initial_adapters[name]).float().square().sum().item()
        for name, parameter in model.named_parameters() if name in initial_adapters
    ) ** 0.5
    # Test is not used for checkpoint or parameter selection.
    final_test = _evaluate(model, tokenizer, test, max_new_tokens=args.max_new_tokens)
    payload = {
        "schema_version": 1,
        "diagnostic_only": True,
        "paper_result_reproduced": False,
        "method": "DCE+SRCL" if args.lambda_srcl else "DCE",
        "teacher_mode": args.teacher_mode,
        "public_model": {"id": QWEN_ID, "revision": QWEN_REVISION},
        "public_dataset": {"id": "openai/grade-school-math", "revision": GSM8K_REVISION},
        "protocol": {
            "seed": args.seed, "steps": args.steps,
            "train_examples": len(train), "validation_examples": len(validation),
            "test_examples": len(test), "max_new_tokens": args.max_new_tokens,
            "lora_rank": 8, "lora_target_modules": ["q_proj", "v_proj"],
            "paper_train_distribution": False, "paper_benchmark": False,
            "test_used_for_selection": False,
        },
        "baseline_validation": baseline_validation,
        "history": history,
        "adapter_parameter_delta_l2": adapter_parameter_delta_l2,
        "final_validation": final_validation,
        "final_test": final_test,
        "accelerator_model": torch.cuda.get_device_name(0),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
