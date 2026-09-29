#!/usr/bin/env python3
"""Bounded, explicitly diagnostic KuaFu public-MRQA training/evaluation.

The public SQuAD/MRQA archive is not Tencent's private behavior dataset. The
head/tail controls use the same source-token count as the compressed cache but
share its decoder, so they are input ablations rather than independently
trained, paper-comparable baselines. Dev gold is scored only after training.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def _digest(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--mrqa-train", type=Path, required=True)
    parser.add_argument("--mrqa-dev", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--train-limit", type=int, default=4)
    parser.add_argument("--dev-limit", type=int, default=4)
    parser.add_argument("--max-items", type=int, default=4)
    parser.add_argument("--max-item-tokens", type=int, default=24)
    parser.add_argument("--max-answer-tokens", type=int, default=16)
    parser.add_argument("--independent-control", action="store_true",
                        help="train a separate equal-cache-token raw-head Q&A control")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if min(args.train_limit, args.dev_limit, args.max_items,
           args.max_item_tokens, args.max_answer_tokens) < 1:
        parser.error("all sample and token budgets must be positive")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from auto_research.reproductions.llm_lora import inject_lora
    from auto_research.reproductions.kuafu.evaluation import (
        exact_match, greedy_answer, raw_context_qa_loss, same_token_budget, token_f1,
    )
    from auto_research.reproductions.kuafu.model import (
        KuafuSystem, TwoAxisProjector, cosine_residual_scale,
    )
    from auto_research.reproductions.kuafu.mrqa import (
        load_mrqa, validate_disjoint_qids,
    )

    if not torch.cuda.is_available():
        raise RuntimeError("the advertised checkpoint path requires NVIDIA CUDA")
    torch.manual_seed(args.seed)
    train = load_mrqa(args.mrqa_train, expected_split="train",
                      limit=args.train_limit, one_per_context=True)
    dev = load_mrqa(args.mrqa_dev, expected_split="dev",
                    limit=args.dev_limit, one_per_context=True)
    validate_disjoint_qids(train, dev)
    train.sort(key=lambda example: len(example.items))
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint, local_files_only=True)

    def load_model():
        model = AutoModelForCausalLM.from_pretrained(
            args.checkpoint, local_files_only=True, dtype=torch.bfloat16,
            attn_implementation="sdpa",
        ).to("cuda")
        inject_lora(model, rank=4, alpha=8)
        return model

    encoder, decoder = load_model(), load_model()
    if encoder.config.model_type != "qwen3" or decoder.config.model_type != "qwen3":
        raise ValueError("this audited MRQA path requires a Qwen3 causal checkpoint")
    projector = TwoAxisProjector(
        encoder.config.hidden_size, 128, 4, 2,
    ).to(device="cuda", dtype=torch.bfloat16)
    system = KuafuSystem(encoder, decoder, projector)

    def encode(text: str, limit: int) -> torch.Tensor:
        return tokenizer(text, add_special_tokens=False, truncation=True,
                         max_length=limit, return_tensors="pt").input_ids[0].to("cuda")

    def inputs(example):
        items = [encode(text, args.max_item_tokens)
                 for text in example.items[:args.max_items]]
        if not items or any(not item.numel() for item in items):
            raise ValueError("empty MRQA item after tokenization")
        question = encode(example.question + " Answer with a short phrase only.", 64)
        return items, question

    stage_losses: dict[str, list[float]] = {}
    for stage in ("reconstruction", "compressed_qa", "co_training"):
        system.set_stage(stage)
        optimizer = torch.optim.AdamW(
            [parameter for parameter in system.parameters() if parameter.requires_grad],
            lr=1e-5,
        )
        stage_losses[stage] = []
        for index, example in enumerate(train):
            items, question = inputs(example)
            if stage == "reconstruction":
                prompt = encode("Reconstruct the original text:", 24)
                target = torch.cat(items)
                projected = False
                residual = 0.0
            else:
                prompt = question
                target = torch.cat((
                    encode(example.answers[0], args.max_answer_tokens),
                    torch.tensor([tokenizer.eos_token_id], device="cuda"),
                ))
                projected = True
                residual = cosine_residual_scale(index, len(train))
            optimizer.zero_grad(set_to_none=True)
            loss = system.sequence_loss(
                items, prompt_ids=prompt, target_ids=target,
                projected=projected, residual_scale=residual,
            )
            if not torch.isfinite(loss):
                raise RuntimeError(f"non-finite {stage} loss")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                [parameter for parameter in system.parameters()
                 if parameter.requires_grad], 1.0,
            )
            optimizer.step()
            stage_losses[stage].append(float(loss.detach().cpu()))

    system.eval()
    scores = {arm: {"em": [], "f1": []}
              for arm in ("compressed", "raw_head_equal_tokens",
                          "raw_tail_equal_tokens", "raw_full")}
    skipped_short = 0
    with torch.no_grad():
        for example in dev:
            items, question = inputs(example)
            raw = torch.cat(items)
            try:
                head, tail = same_token_budget(
                    raw, item_count=len(items),
                    tokens_per_item=projector.output_tokens,
                )
            except ValueError:
                skipped_short += 1
                continue
            embeddings = decoder.get_input_embeddings()
            prefixes = {
                "compressed": system.context_embeddings(
                    items, question, residual_scale=0.0,
                ),
                "raw_head_equal_tokens": torch.cat((embeddings(head), embeddings(question))),
                "raw_tail_equal_tokens": torch.cat((embeddings(tail), embeddings(question))),
                "raw_full": torch.cat((embeddings(raw), embeddings(question))),
            }
            for arm, prefix in prefixes.items():
                answer_ids = greedy_answer(
                    decoder, prefix, eos_token_id=tokenizer.eos_token_id,
                    max_tokens=args.max_answer_tokens,
                )
                answer = tokenizer.decode(answer_ids, skip_special_tokens=True)
                scores[arm]["em"].append(exact_match(answer, example.answers))
                scores[arm]["f1"].append(token_f1(answer, example.answers))

    if not scores["compressed"]["em"]:
        raise RuntimeError("no evaluable MRQA dev examples")
    result = {
        "status": "passed", "diagnostic_only": True,
        "paper_result_reproduced": False,
        "dataset": "MRQA 2019 SQuAD train/dev", "seed": args.seed,
        "checkpoint": {
            "model_type": encoder.config.model_type,
            "source": "user-supplied local checkpoint",
            "revision": args.checkpoint.name
            if len(args.checkpoint.name) == 40
            and all(character in "0123456789abcdef" for character in args.checkpoint.name)
            else "unverified-local-revision",
        },
        "train_sha256": _digest(args.mrqa_train),
        "dev_sha256": _digest(args.mrqa_dev),
        "train_questions": len(train), "dev_questions": len(dev),
        "dev_skipped_short": skipped_short,
        "max_items": args.max_items,
        "cached_tokens_per_item": projector.output_tokens,
        "max_item_tokens": args.max_item_tokens,
        "stage_losses": stage_losses,
        "dev_metrics": {
            arm: {metric: sum(values) / len(values)
                  for metric, values in metrics.items()}
            for arm, metrics in scores.items()
        },
        "control_caveat": "Head/tail/full use the same decoder trained on compressed input; "
                          "these are input ablations, not separately trained baselines.",
    }
    if args.independent_control:
        torch.manual_seed(args.seed)
        control = load_model()
        control.train()
        control_optimizer = torch.optim.AdamW(
            (parameter for parameter in control.parameters() if parameter.requires_grad),
            lr=1e-5,
        )
        control_losses = []
        control_train = []
        for example in train:
            items, question = inputs(example)
            raw = torch.cat(items)
            try:
                head, _ = same_token_budget(
                    raw, item_count=len(items), tokens_per_item=projector.output_tokens,
                )
            except ValueError:
                continue
            answer = torch.cat((
                encode(example.answers[0], args.max_answer_tokens),
                torch.tensor([tokenizer.eos_token_id], device="cuda"),
            ))
            control_train.append((head, question, answer))
        if not control_train:
            raise RuntimeError("no train examples support the equal-cache-token raw control")
        # Match the two compressed QA stages by update count. The compressed
        # reconstruction stage remains extra work, so this is a diagnostic,
        # not a FLOP-matched paper baseline.
        for _epoch in range(2):
            for head, question, answer in control_train:
                control_optimizer.zero_grad(set_to_none=True)
                loss = raw_context_qa_loss(control, head, question, answer)
                if not torch.isfinite(loss):
                    raise RuntimeError("non-finite independent control loss")
                loss.backward()
                torch.nn.utils.clip_grad_norm_(
                    [parameter for parameter in control.parameters()
                     if parameter.requires_grad], 1.0,
                )
                control_optimizer.step()
                control_losses.append(float(loss.detach().cpu()))
        control.eval()
        independent_scores = {"em": [], "f1": []}
        with torch.no_grad():
            for example in dev:
                items, question = inputs(example)
                raw = torch.cat(items)
                try:
                    head, _ = same_token_budget(
                        raw, item_count=len(items), tokens_per_item=projector.output_tokens,
                    )
                except ValueError:
                    continue
                embeddings = control.get_input_embeddings()
                prefix = torch.cat((embeddings(head), embeddings(question)))
                answer_ids = greedy_answer(
                    control, prefix, eos_token_id=tokenizer.eos_token_id,
                    max_tokens=args.max_answer_tokens,
                )
                answer = tokenizer.decode(answer_ids, skip_special_tokens=True)
                independent_scores["em"].append(exact_match(answer, example.answers))
                independent_scores["f1"].append(token_f1(answer, example.answers))
        result["independent_control"] = {
            "input": "raw_head_equal_cache_tokens",
            "train_questions": len(control_train),
            "qa_updates": len(control_losses),
            "train_final_loss": control_losses[-1],
            "dev_metrics": {
                metric: sum(values) / len(values)
                for metric, values in independent_scores.items()
            },
            "budget_caveat": "Equal Q&A update count, not equal FLOPs: compressed arm "
                             "also trains a reconstruction stage and an encoder/projector.",
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
