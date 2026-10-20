"""Real cached-model SpecGuard micro-suite; no paid API and no automatic downloads."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

from auto_research.agent_research.specguard import (
    LeanKernel, PROTOCOL, UPSTREAM_COMMIT, fingerprint, messages, public_tasks, run_task,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = ("src/auto_research/agent_research/specguard.py", "scripts/run_specguard_component.py")


class CachedModel:
    def __init__(self, checkpoint, revision, device, *, max_new_tokens, max_tokens,
                 max_calls, wall_seconds):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        self.device = device
        self.started = time.monotonic()
        self.wall_seconds = wall_seconds
        self.max_new_tokens, self.max_tokens, self.max_calls = max_new_tokens, max_tokens, max_calls
        self.calls, self.tokens, self.records = 0, 0, []
        if device == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA requested but unavailable")
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint, revision=revision,
            local_files_only=True, trust_remote_code=False)
        self.model = AutoModelForCausalLM.from_pretrained(checkpoint, revision=revision,
            local_files_only=True, trust_remote_code=False,
            torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32).to(device).eval()
        self.accelerator = torch.cuda.get_device_name() if device == "cuda" else "cpu"

    def generate(self, request, *, seed):
        left = self.wall_seconds-(time.monotonic()-self.started)
        if self.calls >= self.max_calls or self.tokens >= self.max_tokens or left <= 0:
            raise RuntimeError("global model budget exhausted; no automatic retries")
        self.torch.manual_seed(seed+self.calls)
        prompt = self.tokenizer.apply_chat_template(messages(request), tokenize=False,
                                                    add_generation_prompt=True)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        if inputs.input_ids.shape[1] > 8192:
            raise RuntimeError("bounded context exceeded")
        limit = min(self.max_new_tokens, self.max_tokens-self.tokens)
        self.calls += 1
        started = time.monotonic()
        with self.torch.inference_mode():
            output = self.model.generate(**inputs, max_new_tokens=limit, max_time=max(.1, left),
                do_sample=True, temperature=.2, top_p=.95,
                pad_token_id=self.tokenizer.eos_token_id)
        generated = output[0, inputs.input_ids.shape[1]:]
        count = int(generated.numel())
        self.tokens += count
        response = self.tokenizer.decode(generated, skip_special_tokens=True)
        self.records.append({"role": request.role, "attempt": request.attempt,
            "seed": seed, "input_tokens": int(inputs.input_ids.shape[1]),
            "generated_tokens": count, "seconds": time.monotonic()-started,
            "actual_model_device": str(next(self.model.parameters()).device),
            "request_sha256": fingerprint(asdict(request)),
            "response_sha256": hashlib.sha256(response.encode()).hexdigest()})
        return response


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True, help="existing local checkpoint/cache only")
    parser.add_argument("--model-id", required=True, help="public checkpoint identity")
    parser.add_argument("--revision", required=True, help="exact public model commit, not main")
    parser.add_argument("--source-commit", help="frozen 40-hex source commit for a no-git remote copy; "
                        "the local curator independently verifies its committed source blobs")
    parser.add_argument("--lean-bin", required=True)
    parser.add_argument("--device", choices=("cuda", "cpu"), default="cuda")
    parser.add_argument("--seeds", default="42")
    parser.add_argument("--max-attempts", type=int, default=2)
    parser.add_argument("--max-new-tokens", type=int, default=1024)
    parser.add_argument("--max-total-new-tokens", type=int, default=8000)
    parser.add_argument("--max-calls", type=int, default=18)
    parser.add_argument("--wall-seconds", type=int, default=600)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    seeds = [int(value) for value in args.seeds.split(",")]
    if (not seeds or len(set(seeds)) != len(seeds) or len(seeds) > 3 or
            len(args.revision) != 40 or any(c not in "0123456789abcdef" for c in args.revision) or
            not 1 <= args.max_attempts <= 2 or not 64 <= args.max_new_tokens <= 1536 or
            not 1 <= args.max_calls <= 54 or not 1 <= args.max_total_new_tokens <= 24000 or
            not 1 <= args.wall_seconds <= 900):
        raise ValueError("exact revision and strictly bounded micro-suite budgets required")
    if args.output.exists():
        raise FileExistsError("immutable run output already exists")
    commit = args.source_commit
    if commit is None:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                                text=True, check=True).stdout.strip()
    if re.fullmatch(r"[a-f0-9]{40}", commit) is None:
        raise ValueError("source commit must be an exact 40-hex commit")
    kernel = LeanKernel(args.lean_bin)
    model = CachedModel(args.checkpoint, args.revision, args.device,
        max_new_tokens=args.max_new_tokens, max_tokens=args.max_total_new_tokens,
        max_calls=args.max_calls, wall_seconds=args.wall_seconds)
    tasks, rows = public_tasks(), []
    sources = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCE_PATHS}
    raw = {"schema_version": 2, "method": "specguard", "protocol_id": PROTOCOL,
        "upstream_commit": UPSTREAM_COMMIT, "code_commit": commit, "source_sha256": sources,
        "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
        "promotion_eligible": False, "evolve_integrated": False,
        "full_experiment_status": "not_reproduced_high_cost",
        "dataset": {"id": "self-authored-increment-micro-suite", "public_benchmark": False,
                    "revision": fingerprint([asdict(t) for t in tasks])},
        "tasks": [asdict(t) for t in tasks], "seeds": seeds, "device": args.device,
        "accelerator": model.accelerator,
        "model": {"id": args.model_id, "revision": args.revision, "local_files_only": True},
        "lean": {"version": kernel.version, "binary_sha256": kernel.binary_sha256},
        "budget": {"max_attempts_per_role": args.max_attempts,
            "max_new_tokens_per_call": args.max_new_tokens,
            "max_total_new_tokens": args.max_total_new_tokens,
            "max_calls": args.max_calls, "wall_seconds": args.wall_seconds},
        "per_seed": rows, "model_records": model.records,
        "semantic_faithfulness": "manual_audit_required_not_proved_by_Lean"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Persist after every task, including failures; raw is not a curated passing receipt.
    def save():
        raw["actual_model_calls"], raw["actual_generated_tokens"] = model.calls, model.tokens
        args.output.write_text(json.dumps(raw, ensure_ascii=False, indent=2, allow_nan=False)+"\n",
                               encoding="utf-8")
    for seed in seeds:
        for task in tasks:
            result = run_task(task, lambda req: model.generate(req, seed=seed), kernel,
                              max_attempts=args.max_attempts)
            rows.append({"seed": seed, **result})
            save()
            print(json.dumps({"seed": seed, "task": task.task_id,
                              "verdict": result["verdict"], "evidence": result["evidence"]}), flush=True)
    raw["metrics"] = {"task_runs": len(rows), "certified_conflicts": sum(
        r["verdict"] == "conflict" for r in rows), "formal_agreements": sum(
        r["verdict"] == "no-conflict" for r in rows), "inconclusive": sum(
        r["verdict"] == "inconclusive" for r in rows)}
    save()


if __name__ == "__main__":
    main()
