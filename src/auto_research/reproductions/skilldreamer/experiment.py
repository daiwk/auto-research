"""GSM8K arithmetic execution diagnostic with actual local LLM and skill loads."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import re

import numpy as np

from ..near.data import FrozenMiniLM, sha256_file
from ..near.experiment import verify_provenance
from .algorithm import Skill, execute_agent, hybrid_retrieval, prospective_skills


class LocalGenerator:
    def __init__(self, path: Path, device: str, seed: int, max_new_tokens: int = 256):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        torch.manual_seed(seed)
        self.torch, self.device, self.max_new_tokens = torch, device, max_new_tokens
        self.calls, self.generated_tokens = 0, 0
        self.tokenizer = AutoTokenizer.from_pretrained(str(path), local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(str(path), local_files_only=True,
            torch_dtype=torch.bfloat16 if device.startswith("cuda") else torch.float32).to(device)
        self.model.eval().requires_grad_(False)

    def __call__(self, prompt):
        messages = [{"role": "system", "content": "Follow the requested schema. No reference answer is available."},
                    {"role": "user", "content": prompt}]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        encoded = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=2048).to(self.device)
        with self.torch.no_grad():
            output = self.model.generate(**encoded, do_sample=True, temperature=0.7,
                top_p=0.9, max_new_tokens=self.max_new_tokens,
                pad_token_id=self.tokenizer.eos_token_id)
        self.calls += 1
        self.generated_tokens += output.shape[1] - encoded.input_ids.shape[1]
        return self.tokenizer.decode(output[0, encoded.input_ids.shape[1]:], skip_special_tokens=True)


def _numeric_equal(predicted, expected):
    try:
        return math.isclose(float(str(predicted).replace(",", "")), float(str(expected).replace(",", "")),
                            rel_tol=1e-6, abs_tol=1e-6)
    except (ValueError, TypeError):
        return False


def run_skilldreamer(config: dict, seed: int) -> dict:
    model_dir, encoder_dir = Path(config["model_dir"]), Path(config["encoder_dir"])
    model_info = json.loads((model_dir / "provenance.json").read_text())
    if not re.fullmatch(r"[0-9a-f]{40}", model_info.get("revision", "")):
        raise ValueError("fixed public checkpoint commit required")
    required = tuple(name for name in model_info["files"]
                     if name.endswith((".safetensors", ".json")))
    provenance = verify_provenance(model_dir, model_info["public_id"], model_info["revision"], required)
    encoder_info = verify_provenance(encoder_dir, "sentence-transformers/all-MiniLM-L6-v2",
        "1110a243fdf4706b3f48f1d95db1a4f5529b4d41", ("model.safetensors", "config.json", "tokenizer.json"))
    raw = Path(config["raw_data"])
    source = json.loads((raw.parent / "provenance.json").read_text())
    raw_hash = sha256_file(raw)
    if source.get("files", {}).get(raw.name) != raw_hash:
        raise ValueError("public task input hash differs from its verified provenance")
    rows = [json.loads(line) for line in raw.read_text().splitlines() if line.strip()][:config.get("max_queries", 24)]
    # Read reference answers only into the external scorer, not the agent records.
    goals, references = {}, {}
    for i, row in enumerate(rows):
        identifier = str(i)
        goals[identifier] = str(row["question"])
        references[identifier] = str(row["answer"]).rsplit("####", 1)[-1].strip()
    ordered = sorted(goals, key=lambda i: hashlib.sha256(("skilldreamer-v1:" + i).encode()).hexdigest())
    validation_n = max(1, len(ordered) // 3)
    validation_ids, test_ids = ordered[:validation_n], ordered[validation_n:]
    if not test_ids:
        raise ValueError("disjoint validation and test tasks required")
    device = config.get("device", "cpu")
    generate = LocalGenerator(model_dir, device, seed, config.get("max_new_tokens", 256))
    encoder = FrozenMiniLM(encoder_dir, device)
    encode = lambda texts: encoder.encode(texts)[0]
    gallery = [Skill(**row) for row in json.loads(Path(__file__).with_name("gallery.json").read_text())]
    variants, summaries = {}, {}
    for mode in ("no_skills", "direct", "skilldreamer"):
        outcomes = []
        for identifier in test_ids:
            generate.torch.manual_seed(seed + int(identifier))
            calls_before, tokens_before = generate.calls, generate.generated_tokens
            goal = goals[identifier]
            try:
                if mode == "no_skills":
                    candidates = []
                elif mode == "direct":
                    features = encode([goal, *[s.name + "\n" + s.description + "\n" + s.body for s in gallery]])
                    order = np.argsort(-(features[1:] @ features[0]), kind="stable")[:config.get("top_k", 3)]
                    candidates = [gallery[i] for i in order]
                else:
                    pseudo, anchors = prospective_skills(goal, generate)
                    candidates = hybrid_retrieval(goal, pseudo, anchors, gallery, encode,
                                                  top_k=config.get("top_k", 3))
                outcome = execute_agent(goal, generate, candidates, mode=mode,
                                        action_budget=config.get("action_budget", 8))
                outcome["correct"] = (_numeric_equal(outcome["submitted_answer"], references[identifier])
                    and outcome["generation_errors"] == 0 and outcome["tool_errors"] == 0)
            except ValueError as exc:
                outcome = {"correct": False, "loaded_skills": [], "executed_actions": 0,
                           "failure": str(exc), "model_calls": 0}
            outcome["model_calls_including_psg"] = generate.calls - calls_before
            outcome["generated_tokens_including_psg"] = generate.generated_tokens - tokens_before
            outcome["id"] = identifier
            outcomes.append(outcome)
        variants[mode] = outcomes
        summaries[mode] = {"pass_rate": float(np.mean([x["correct"] for x in outcomes])),
                           "load_rate": float(np.mean([bool(x["loaded_skills"]) for x in outcomes])),
                           "executed_actions": sum(x["executed_actions"] for x in outcomes),
                           "generation_failures": sum("failure" in x or x.get("generation_errors", 0) > 0 for x in outcomes),
                           "tool_failure_episodes": sum(x.get("tool_errors", 0) > 0 for x in outcomes),
                           "model_calls": sum(x["model_calls_including_psg"] for x in outcomes),
                           "generated_tokens": sum(x["generated_tokens_including_psg"] for x in outcomes)}
    return {"paper": "skilldreamer", "seed": seed, "device": device,
            "fidelity": "core_mechanism", "evaluation_tier": "l2_public_dataset",
            "diagnostic_only": True, "promotion_eligible": False,
            "variants": summaries, "episodes": variants,
            "protocol": {"dataset": source, "raw_sha256": raw_hash,
                         "validation_ids": validation_ids, "test_ids": test_ids,
                         "checkpoint": provenance, "encoder": encoder_info,
                         "selection": "fixed alpha=2, top_k and action budget specified before test; no test tuning",
                         "gold_visible_to_policy": False, "original_skill_benchmark": False,
                         "environment": "actual AST arithmetic calculator; no model-code execution"},
            "limitations": ["GSM8K and five local generic skills replace original executable skill benchmarks",
                            "this is a scaled live-interaction diagnostic, not SkillUsage/SkillNet-Gym capability proof",
                            "skill load rate alone is not task success; generation failures preserved as zero rewards"]}


def reproduce_skilldreamer(dataset_dir: Path, seed: int) -> dict:
    return run_skilldreamer(json.loads((dataset_dir / "skilldreamer.json").read_text()), seed)


def render(result: dict) -> str:
    return "# SkillDreamer 实际执行诊断\n\n非原 SkillUsage/SkillNet-Gym；不据此做能力晋级。\n\n" + f"结果：`{result['variants']}`\n"
