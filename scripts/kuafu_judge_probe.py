#!/usr/bin/env python3
"""Check whether a proposed KuaFu reward judge detects obvious source errors."""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    args = parser.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from auto_research.reproductions.kuafu.rl import (
        build_source_judge_prompt, parse_judge_response,
    )

    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint, local_files_only=True)
    if not tokenizer.chat_template:
        raise ValueError("judge probe needs an instruction checkpoint with chat template")
    model = AutoModelForCausalLM.from_pretrained(
        args.checkpoint, dtype=torch.bfloat16, local_files_only=True,
    ).to("cuda").eval()
    source = "A conference was held in Paris in 2021."
    for response in ("Paris.", "Berlin in 2024."):
        prompt = build_source_judge_prompt(source, "Where and when was it held?", response)
        chat = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False,
            add_generation_prompt=True,
        )
        encoded = tokenizer(chat, return_tensors="pt").to("cuda")
        with torch.no_grad():
            generated = model.generate(
                **encoded, do_sample=False, max_new_tokens=96,
                pad_token_id=tokenizer.eos_token_id,
            )
        raw = tokenizer.decode(
            generated[0, encoded.input_ids.shape[1]:], skip_special_tokens=True
        )
        print(response, repr(raw), parse_judge_response(raw))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
