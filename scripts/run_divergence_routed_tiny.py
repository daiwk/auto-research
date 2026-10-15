#!/usr/bin/env python3
"""Real byte-LM DrOPD diagnostic without checkpoint downloads or transformers.

A tiny teacher receives bounded next-token training on public text, is frozen,
and supervises an independently initialized student on its own sampled tokens.
This is L1 algorithm execution, not pretrained-model or benchmark evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time


def run(args):
    import torch
    from torch import nn
    from torch.nn import functional as F
    from auto_research.post_training.divergence_routed_opd import prepare_routing, routed_ppo_loss

    if args.output.exists():
        raise FileExistsError("choose a fresh output; preserve existing evidence")
    if not 1 <= args.steps <= 20 or not 1 <= args.teacher_steps <= 64 or not 1 <= args.max_tokens <= 32:
        raise ValueError("diagnostic budget capped at 20 online steps, 64 teacher steps and 32 tokens")
    if not args.corpus_id or not args.corpus_revision:
        raise ValueError("fixed public corpus identity and revision required")
    seeds = tuple(int(seed) for seed in args.seeds.split(","))
    if not seeds or len(seeds) != len(set(seeds)) or len(seeds) > 3:
        raise ValueError("one to three independent seeds required")
    payload = args.corpus_path.read_bytes()
    if len(payload) < 2048 or len(payload) > 2_000_000:
        raise ValueError("use a bounded 2 KB..2 MB public-domain text corpus")
    tokens = torch.tensor(list(payload), dtype=torch.long, device=args.device)
    boundary = int(.9 * len(tokens))
    train, validation = tokens[:boundary], tokens[boundary:]
    # The slices do not share tokens. Prefixes for online generation come only
    # from train; held-out bytes are used solely for the final NLL diagnostic.
    class ByteLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(256, 32)
            self.recurrent = nn.GRU(32, 48, batch_first=True)
            self.head = nn.Linear(48, 256)

        def forward(self, ids):
            hidden, _ = self.recurrent(self.embedding(ids))
            return self.head(hidden)

    def batch(source, width=32, count=4):
        starts = torch.randint(len(source) - width - 1, (count,), device=source.device)
        return torch.stack([source[s:s + width + 1] for s in starts])

    def heldout_nll(model):
        # Fixed validation windows, independent of train sampling and seeds.
        ids = validation[:129].unsqueeze(0)
        with torch.no_grad():
            return float(F.cross_entropy(model(ids[:, :-1]).reshape(-1, 256), ids[:, 1:].reshape(-1)))

    started, outcomes = time.monotonic(), []
    for seed in seeds:
        torch.manual_seed(seed)
        teacher = ByteLM().to(args.device)
        teacher_optimizer = torch.optim.AdamW(teacher.parameters(), lr=.01)
        for _ in range(args.teacher_steps):
            ids = batch(train)
            loss = F.cross_entropy(teacher(ids[:, :-1]).reshape(-1, 256), ids[:, 1:].reshape(-1))
            teacher_optimizer.zero_grad()
            loss.backward()
            teacher_optimizer.step()
        teacher.eval().requires_grad_(False)
        frozen = [p.detach().clone() for p in teacher.parameters()]
        # Separate initialization, not a cloned identical teacher/student.
        torch.manual_seed(seed + 10000)
        student = ByteLM().to(args.device).eval()
        optimizer = torch.optim.AdamW(student.parameters(), lr=.001)
        before = [p.detach().clone() for p in student.parameters()]
        baseline = heldout_nll(student)
        history = []
        generated_tokens = 0
        for step in range(args.steps):
            prefix = batch(train, width=16, count=2)[:, :16]
            ids = prefix
            with torch.no_grad():
                for _ in range(args.max_tokens):
                    probabilities = student(ids)[:, -1].softmax(-1)
                    ids = torch.cat((ids, torch.multinomial(probabilities, 1)), -1)
                mask = torch.zeros_like(ids[:, 1:], dtype=torch.bool)
                mask[:, prefix.shape[1] - 1:] = True
                old = student(ids)[:, :-1]
                target = teacher(ids)[:, :-1]
                routing = prepare_routing(old, target, mask, top_k=16, fraction=.2)
            generated_tokens += int(mask.sum())
            optimizer.zero_grad()
            loss, diagnostics = routed_ppo_loss(student(ids)[:, :-1], routing)
            loss.backward()
            norm = torch.nn.utils.clip_grad_norm_(student.parameters(), 1., error_if_nonfinite=True)
            if not float(norm) > 0:
                raise RuntimeError("zero DrOPD gradient")
            optimizer.step()
            history.append({"step": step, "loss": float(loss.detach()),
                            "gradient_norm": float(norm), **diagnostics})
        delta = sum(float((p.detach() - q).square().sum())
                    for p, q in zip(student.parameters(), before, strict=True)) ** .5
        teacher_delta = sum(float((p.detach() - q).square().sum())
                            for p, q in zip(teacher.parameters(), frozen, strict=True)) ** .5
        if not delta > 0 or teacher_delta != 0:
            raise RuntimeError("actual student update and unchanged frozen teacher required")
        outcomes.append({"seed": seed, "parameter_delta_l2": delta,
                         "teacher_parameter_delta_l2": teacher_delta,
                         "teacher_warmup_steps": args.teacher_steps, "generated_tokens": generated_tokens,
                         "baseline_validation_nll": baseline, "final_validation_nll": heldout_nll(student),
                         "history": history})
    result = {
        "method": "divergence-routed-opd", "paper": "2610.19572v1",
        "evaluation_tier": "L1", "diagnostic_only": True, "promotion_eligible": False,
        "scope": "tiny byte autoregressive LM: actual online sampling, frozen teacher and PPO parameter updates",
        "not_claimed": ["pretrained LLM capability", "paper mathematical benchmark improvements", "HF checkpoint path validation"],
        "full_reproduction": "not_reproduced_high_cost", "seeds": list(seeds), "results": outcomes,
        "public_resources": {"corpus_id": args.corpus_id, "corpus_revision": args.corpus_revision,
                             "corpus_sha256": hashlib.sha256(payload).hexdigest(),
                             "byte_ranges": {"train": [0, boundary], "validation": [boundary, len(tokens)]},
                             "checkpoint": "none; independent seeded initialization; teacher bounded next-token warmup"},
        "budget": {"steps_per_seed": args.steps, "teacher_steps_per_seed": args.teacher_steps,
                   "rollouts_per_step": 2, "max_new_tokens": args.max_tokens},
        "accelerator": torch.cuda.get_device_name() if args.device.startswith("cuda") else args.device,
        "elapsed_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"method": result["method"], "seeds": list(seeds),
                      "parameter_delta_l2": [r["parameter_delta_l2"] for r in outcomes],
                      "elapsed_seconds": result["elapsed_seconds"]}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-path", type=Path, required=True)
    parser.add_argument("--corpus-id", required=True)
    parser.add_argument("--corpus-revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--steps", type=int, default=2)
    parser.add_argument("--teacher-steps", type=int, default=16)
    parser.add_argument("--max-tokens", type=int, default=16)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
