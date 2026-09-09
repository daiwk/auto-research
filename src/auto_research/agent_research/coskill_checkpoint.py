"""Single-device shared-checkpoint CoSkill on the public ToolRoute simulator.

This is not an ALFWorld/WebShop score reproduction. It trains the final
transformer block, with all other checkpoint parameters frozen.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time

from .capability_benchmark import CapabilityEnvironment, build_capability_tasks
from .coskill_rollout import attempt, collect_group, role_advantages
from .sep7_mechanisms import HierarchicalSkills

MODEL = "Qwen/Qwen3-4B-Instruct-2507"
REVISION = "cdbee75f17c01a7cc42f958dc650907174af0554"


class SharedCheckpoint:
    def __init__(self, model_id=MODEL, revision=REVISION, device="cuda"):
        import torch
        from huggingface_hub import snapshot_download
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        checkpoint = snapshot_download(model_id, revision=revision, local_files_only=True)
        self.tokenizer = AutoTokenizer.from_pretrained(
            checkpoint, local_files_only=True,
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            checkpoint, local_files_only=True,
            torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
            attn_implementation="eager",
        ).to(device).eval()
        self.model.requires_grad_(False)
        self.block = self.model.model.layers[-1]
        # Keep the optimized weights in FP32: tiny RL updates can otherwise
        # round back to the identical BF16 values after every optimizer step.
        self.block.float()
        self.block.requires_grad_(True)
        self.initial = {name: value.detach().clone() for name, value in self.block.named_parameters()}
        self.tokens = {}
        self.old = {}
        self.reference = {}
        self.sampling = True

    def score(self, inputs, outputs):
        torch = self.torch
        ids = torch.cat([inputs, outputs], dim=-1)
        with torch.autocast(device_type=self.model.device.type,
                            dtype=torch.bfloat16, enabled=self.model.device.type == "cuda"):
            logits = self.model(ids, use_cache=False).logits[:, inputs.shape[-1] - 1:-1].float()
        return logits.log_softmax(-1).gather(-1, outputs.unsqueeze(-1)).squeeze(-1).squeeze(0)

    def similarity(self, left, right):
        torch = self.torch
        values = []
        for text in (left, right):
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.model.device)
            with torch.inference_mode(), torch.autocast(
                device_type=self.model.device.type, dtype=torch.bfloat16,
                enabled=self.model.device.type == "cuda",
            ):
                # The penultimate hidden state excludes the trainable final
                # block, so retrieval remains a frozen encoder throughout RL.
                states = self.model.model(
                    **inputs, use_cache=False, output_hidden_states=True,
                ).hidden_states[-2].float().mean(1)[0]
            values.append(torch.nn.functional.normalize(states, dim=0))
        return float((values[0] @ values[1]).cpu())

    def __call__(self, role, prompt):
        torch = self.torch
        rendered = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self.tokenizer(rendered, return_tensors="pt").input_ids.to(self.model.device)
        with torch.no_grad(), torch.autocast(
            device_type=self.model.device.type, dtype=torch.bfloat16,
            enabled=self.model.device.type == "cuda",
        ):
            result = self.model.generate(
                inputs, max_new_tokens=80 if role == "editing" else 24,
                do_sample=self.sampling, pad_token_id=self.tokenizer.eos_token_id,
                temperature=1.0, top_p=1.0, top_k=0,
                attention_mask=torch.ones_like(inputs),
            )
            outputs = result[:, inputs.shape[-1]:]
            text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            if not self.sampling:
                return text
            key = (prompt, text)
            self.tokens[key] = (inputs, outputs)
            self.old[key] = self.score(inputs, outputs).detach()
            # A frozen initial policy, not the just-updated behavior policy.
            current = {name: value.detach().clone() for name, value in self.block.named_parameters()}
            self.block.load_state_dict(self.initial)
            self.reference[key] = self.score(inputs, outputs).detach()
            self.block.load_state_dict(current)
        return text

    def update(self, decisions, optimizer, beta=0.01):
        torch = self.torch
        advantages = role_advantages(decisions)
        counts = {role: sum(row.role == role for row in decisions)
                  for role in ("reasoning", "editing")}
        optimizer.zero_grad()
        losses = {role: 0.0 for role in counts}
        role_norms = {}
        for role in counts:
            before = [None if p.grad is None else p.grad.detach().clone()
                      for p in self.block.parameters()]
            for row, advantage in zip(decisions, advantages):
                if row.role != role:
                    continue
                key = (row.prompt, row.completion)
                current = self.score(*self.tokens[key])
                ratio = (current - self.old[key]).exp()
                surrogate = torch.minimum(ratio * float(advantage),
                                          ratio.clamp(0.8, 1.2) * float(advantage))
                difference = self.reference[key] - current
                kl = difference.exp() - difference - 1
                loss = (-surrogate + beta * kl).mean() / counts[row.role]
                loss.backward()
                losses[row.role] += float(loss.detach())
            role_norms[role] = sum(float((p.grad if old is None else p.grad - old).float().square().sum())
                                   for p, old in zip(self.block.parameters(), before)
                                   if p.grad is not None) ** 0.5
            del before
        norm = torch.nn.utils.clip_grad_norm_(self.block.parameters(), 1.0)
        optimizer.step()
        self.tokens.clear()
        self.old.clear()
        self.reference.clear()
        return {"loss_by_role": losses, "gradient_norm": float(norm),
                "gradient_norm_by_role": role_norms,
                "nonzero_advantages": int((abs(advantages) > 1e-8).sum())}


def evaluate(policy, skills, seed, split, episodes, max_turns):
    policy.sampling = False
    rows = []
    for task in build_capability_tasks(episodes, seed, split):
        key = skills.retrieve(task.observation.request)
        environment = CapabilityEnvironment(task)
        result = attempt(task.observation, environment.call, policy,
                         skills.bundles.get(key, []), task.observation.task_id,
                         edit=False, max_turns=max_turns, similarity=skills.similarity)
        rows.append({"id": task.observation.task_id, "success": result.reward,
                     "calls": len(environment.calls), "trace": result.trace})
    return {"success_rate": sum(row["success"] for row in rows) / len(rows), "episodes": rows}


def run(seed=42, train_episodes=12, eval_episodes=12, max_turns=8, group_size=2,
        verification_attempts=2, learning_rate=1e-5, device="cuda", *,
        include_test=True, state_path=None):
    import torch

    torch.manual_seed(seed)
    started = time.monotonic()
    policy = SharedCheckpoint(device=device)
    optimizer = torch.optim.AdamW(policy.block.parameters(), lr=learning_rate)
    skills = HierarchicalSkills(similarity=policy.similarity)
    baseline = evaluate(policy, skills, seed, "validation", eval_episodes, max_turns)
    history = []
    tasks = build_capability_tasks(train_episodes, seed, "train")
    for task in tasks:
        policy.sampling = True
        decisions, verification = collect_group(
            task.observation, lambda: CapabilityEnvironment(task).call, policy, skills,
            group_size=group_size, verification_attempts=verification_attempts,
            max_turns=max_turns,
        )
        update = policy.update(decisions, optimizer)
        history.append({"task": task.observation.task_id, "update": update,
                        "verification": verification,
                        "decisions": [asdict(row) for row in decisions]})
        print(json.dumps({"seed": seed, "trained_task": task.observation.task_id,
                          "update": update}), flush=True)
    validation = evaluate(policy, skills, seed, "validation", eval_episodes, max_turns)
    # The test split is evaluated once, after all fixed-budget training.
    test = evaluate(policy, skills, seed, "test", eval_episodes, max_turns) if include_test else None
    if state_path is not None:
        state_path = Path(state_path)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save({"block": policy.block.state_dict(), "skills": skills.bundles}, state_path)
    parameter_delta = sum(float((value.detach().float() - policy.initial[name].float()).abs().sum())
                          for name, value in policy.block.named_parameters())
    return {
        "seed": seed, "model": MODEL, "revision": REVISION,
        "dataset": "toolroute-l2.1", "dataset_revision": hashlib.sha256(
            Path(__file__).with_name("capability_benchmark.py").read_bytes()).hexdigest(),
        "scope": "shared final-block training on ToolRoute, not original benchmark reproduction",
        "baseline_validation": baseline, "validation": validation, "test": test,
        "history": history, "parameter_l1_change": parameter_delta,
        "skill_bundles": skills.bundles, "skill_lineage": skills.lineage,
        "elapsed_seconds": time.monotonic() - started,
        "accelerator": torch.cuda.get_device_name() if device == "cuda" else "CPU",
        "peak_memory_bytes": torch.cuda.max_memory_allocated() if device == "cuda" else None,
        "config": {"train_episodes": train_episodes, "eval_episodes": eval_episodes,
                   "max_turns": max_turns, "group_size": group_size,
                   "verification_attempts": verification_attempts,
                   "learning_rate": learning_rate},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train-episodes", type=int, default=12)
    parser.add_argument("--eval-episodes", type=int, default=12)
    parser.add_argument("--max-turns", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.seed, args.train_episodes, args.eval_episodes, args.max_turns)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
