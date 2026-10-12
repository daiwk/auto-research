#!/usr/bin/env python3
"""Measure a public model's paired one-shot workflows, NOT the Jev model.

Generated programs execute only in Linux ProgramSandbox. ``pairs.jsonl`` has
exactly WorkflowOutcome fields and can be consumed by run_oct12_agents.py
--method jev-workflow. See measurement.json for cost units and annotation
applicability; token units are not billed dollars. No solved program or gold
packing is supplied to generation.
"""
from __future__ import annotations

import argparse
from collections.abc import Mapping
from dataclasses import asdict, dataclass
import hashlib
import json
import os
from pathlib import Path
import random
import time

from auto_research.agent_research.oct12_checkpoint import extract_source
from auto_research.agent_research.oct12_memory_tools import WorkflowOutcome, audit_workflows
from auto_research.agent_research.oct12_provenance import verify_local_checkpoint
from auto_research.agent_research.program_sandbox import CIRCLE_TASK, ProgramSandbox, packing_score


TASK_ID = "public-circle-packing-26"
SAMPLING = {"do_sample": True, "temperature": 0.8, "top_p": 0.95, "top_k": 0}


@dataclass(frozen=True)
class Generation:
    text: str
    token_ids: tuple[int, ...]
    prompt_tokens: int
    seed: int
    budget_exhausted: bool = False


def validate_design(seeds, budgets):
    if len(budgets) != 2 or len(set(budgets)) != 2 or any(
            not isinstance(value, int) or isinstance(value, bool) or value <= 0 for value in budgets):
        raise ValueError("exactly two distinct positive generation budgets required")
    if not seeds or len(set(seeds)) != len(seeds) or any(
            not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed < 2**32
            for seed in seeds):
        raise ValueError("unique integer seeds in [0, 2**32) required")


class TorchGenerationBackend:
    """Frozen, verified, local-only HF generation with exact emitted-ID counts."""
    def __init__(self, checkpoint: Path, checkpoint_id: str, revision: str, device="cpu"):
        # Configure deterministic CUDA matmul before model/device initialization.
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
        self.provenance = verify_local_checkpoint(checkpoint, checkpoint_id, revision)
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        if device not in {"cpu", "cuda"}:
            raise ValueError("device must be cpu or cuda")
        if device == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("requested CUDA is unavailable")
        torch.use_deterministic_algorithms(True)
        torch.set_num_threads(1)
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        torch.backends.cudnn.benchmark = False
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(
            checkpoint, local_files_only=True, trust_remote_code=False)
        self.model = AutoModelForCausalLM.from_pretrained(
            checkpoint, local_files_only=True, trust_remote_code=False, use_safetensors=True,
            torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
            attn_implementation="eager").to(device)
        self.model.eval()
        for parameter in self.model.parameters():
            parameter.requires_grad_(False)
        self.parameter_versions = self._versions()
        self.verified = True

    def _versions(self):
        return tuple((name, parameter._version) for name, parameter in self.model.named_parameters())

    def assert_frozen(self):
        if self.model.training or any(p.requires_grad for p in self.model.parameters()):
            raise RuntimeError("generation model must remain eval-mode and frozen")
        if self._versions() != self.parameter_versions:
            raise RuntimeError("model parameter version changed during measurement")

    def synchronize(self):
        if self.device == "cuda":
            import torch
            torch.cuda.synchronize()

    def generate(self, task_prompt: str, *, seed: int, max_new_tokens: int) -> Generation:
        import numpy as np
        import torch
        self.assert_frozen()
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if self.device == "cuda":
            torch.cuda.manual_seed_all(seed)
        messages = [{"role": "user", "content": task_prompt}]
        if self.tokenizer.chat_template:
            encoded = self.tokenizer.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
        else:
            encoded = self.tokenizer(task_prompt, return_tensors="pt")
        # Transformers versions may return either a Tensor or BatchEncoding.
        # Never replace a returned mask: its padding/special-token semantics matter.
        if isinstance(encoded, Mapping):
            ids = encoded.get("input_ids")
            attention_mask = encoded.get("attention_mask")
        else:
            ids, attention_mask = encoded, None
        if not torch.is_tensor(ids) or ids.ndim != 2 or ids.shape[0] != 1 or ids.shape[1] < 1:
            raise ValueError("tokenizer must return one nonempty input_ids tensor")
        if attention_mask is None:
            attention_mask = torch.ones_like(ids)
        elif not torch.is_tensor(attention_mask) or attention_mask.shape != ids.shape:
            raise ValueError("tokenizer attention_mask must match input_ids tensor")
        ids = ids.to(self.device)
        attention_mask = attention_mask.to(self.device)
        eos = self.model.generation_config.eos_token_id
        if eos is None:
            eos = self.tokenizer.eos_token_id
        eos_ids = set(eos if isinstance(eos, (list, tuple)) else [eos])
        pad = self.tokenizer.pad_token_id
        if pad is None:
            pad = next((token for token in eos_ids if token is not None), None)
        with torch.inference_mode():
            output = self.model.generate(
                ids, attention_mask=attention_mask, max_new_tokens=max_new_tokens,
                **SAMPLING, pad_token_id=pad, use_cache=True, return_dict_in_generate=False)
        emitted = tuple(int(token) for token in output[0, ids.shape[1]:].tolist())
        self.assert_frozen()
        return Generation(self.tokenizer.decode(emitted, skip_special_tokens=True), emitted,
                          int(ids.shape[1]), seed,
                          len(emitted) == max_new_tokens and (not emitted or emitted[-1] not in eos_ids))


def evaluate_generated_program(sandbox, source: str):
    """Only sandbox executes source; the host merely parses and checks geometry."""
    stdout, stderr, return_code = sandbox.execute(source)
    if stderr.startswith("bwrap:") or "Operation not permitted" in stderr:
        raise RuntimeError("sandbox setup failed: " + stderr)
    if return_code:
        return False, None, f"execution failed ({return_code}): {stderr}", return_code
    try:
        score = packing_score(json.loads(stdout))
    except (ValueError, TypeError, OverflowError) as error:
        return False, None, "invalid packing: " + str(error), return_code
    return True, score, "valid geometry; externally verified", return_code


def measure_pairs(backend, sandbox, *, seeds=(42, 43, 44), budgets=(64, 256),
                  clock=time.perf_counter):
    """Injection is for fixture diagnostics only; CLI supplies real components."""
    validate_design(seeds, budgets)
    outcomes, traces = [], []
    for run_index, seed in enumerate(seeds):
        # Explicitly alternate order; tiny sample counts do not remove all timing bias.
        ordered = budgets if run_index % 2 == 0 else tuple(reversed(budgets))
        for budget in ordered:
            configuration = f"budget-{budget}"
            backend.assert_frozen()
            backend.synchronize()
            start = clock()
            generation = backend.generate(CIRCLE_TASK, seed=seed, max_new_tokens=budget)
            backend.synchronize()
            decision_end = clock()
            if generation.seed != seed or len(generation.token_ids) > budget:
                raise ValueError("backend seed/token count differs from requested paired design")
            if generation.prompt_tokens <= 0 or any(
                    not isinstance(token, int) or isinstance(token, bool) or token < 0
                    for token in generation.token_ids):
                raise ValueError("actual nonnegative token IDs and prompt count required")
            program = extract_source(generation.text)
            success, score, feedback, return_code = evaluate_generated_program(sandbox, program)
            task_end = clock()
            backend.assert_frozen()
            outcome = WorkflowOutcome(TASK_ID, seed, configuration, success,
                                      decision_end - start, task_end - start,
                                      float(len(generation.token_ids)), False, False)
            outcomes.append(outcome)
            traces.append({
                "task_id": TASK_ID, "run_id": seed, "seed": seed,
                "configuration": configuration, "configured_budget": budget,
                "execution_order": list(ordered), "prompt_tokens": generation.prompt_tokens,
                "generated_tokens": len(generation.token_ids),
                "generated_token_ids": list(generation.token_ids),
                "generated_token_ids_sha256": hashlib.sha256(
                    json.dumps(generation.token_ids).encode()).hexdigest(),
                "budget_exhausted": generation.budget_exhausted,
                "model_output": generation.text, "sandbox_program": program,
                "sandbox_return_code": return_code, "external_geometry_score": score,
                "external_feedback": feedback,
            })
    audit = audit_workflows(outcomes)
    real = (type(backend) is TorchGenerationBackend and getattr(backend, "verified", False)
            and type(sandbox) is ProgramSandbox and clock is time.perf_counter)
    measurement = {
        "schema_version": 1, "status": "completed", "task_id": TASK_ID,
        "measurement_kind": "real_public_checkpoint_workflow_measurement" if real else
                            "injected_fixture_timing_schema_diagnostic",
        "real_model_execution": bool(real), "diagnostic_only": True,
        "capability_comparison": False, "evolve_promotion_eligible": False,
        "model_claim": "workflow measurement infrastructure, not Jev model reproduction",
        "checkpoint": getattr(backend, "provenance", None),
        "device": getattr(backend, "device", "injected_fixture"),
        "seeds": list(seeds), "budgets": list(budgets), "sampling": dict(SAMPLING),
        "rng_reset_per_configuration": ["python", "numpy", "torch", "torch_cuda_if_used"],
        "weight_audit": "requires_grad false, eval mode and unchanged parameter version counters",
        "cost_unit": "generated_token_units", "billing_currency": None,
        "token_count_rule": "exact emitted token IDs, including EOS; no prompt tokens or retokenization",
        "timing_unit": "perf_counter_seconds",
        "decision_time_scope": "seed reset, prompt tokenization, synchronized generation and decode",
        "task_time_scope": "decision plus source extraction, Linux sandbox and external geometry check",
        "timing_excludes": "checkpoint loading, disk artifact writes; no warmup generations performed",
        "configuration_order_policy": "alternate the two budgets by run index; actual order in traces",
        "success_definition": "26 finite nonnegative-radius circles, unit-square bounds, no overlaps; "
                              "valid geometry only, not best-known optimization score",
        "behavior_annotation_applicability": {
            "failed_recovery": "not_applicable: one-shot workflow has no recovery attempt",
            "premature_completion": "not_applicable: no agent completion-claim protocol",
        },
        "behavior_schema_note": "False booleans are not_applicable schema placeholders; aggregate zero "
                                "counts do not prove these agent failure modes were measured",
        "gold_boundary": "only public task specification enters generation; no gold or solved program",
        "public_task_specification": CIRCLE_TASK,
        "public_task_specification_sha256": hashlib.sha256(CIRCLE_TASK.encode()).hexdigest(),
        "runner_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "timing_source": "time.perf_counter" if clock is time.perf_counter else "injected_fixture_clock",
        "audit": audit, "traces": traces,
    }
    return outcomes, measurement


def write_results(output: Path, outcomes, measurement):
    if output.exists():
        raise FileExistsError("a fresh output directory is required")
    # Validate strict paired outcome records before publishing any files.
    audit_workflows(outcomes)
    raw = "".join(json.dumps(asdict(row), ensure_ascii=False) + "\n" for row in outcomes)
    metadata = dict(measurement)
    metadata["files"] = {"pairs.jsonl": hashlib.sha256(raw.encode()).hexdigest()}
    output.mkdir(parents=True)
    (output / "pairs.jsonl").write_text(raw, encoding="utf-8")
    (output / "measurement.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metadata


def comma_ints(value):
    try:
        return tuple(int(piece) for piece in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("comma-separated integers required") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--checkpoint-id", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", type=comma_ints, default=(42, 43, 44))
    parser.add_argument("--budgets", type=comma_ints, default=(64, 256))
    parser.add_argument("--output", type=Path, required=True, help="fresh output directory")
    args = parser.parse_args(argv)
    validate_design(args.seeds, args.budgets)
    if args.output.exists():
        raise FileExistsError("a fresh output directory is required")
    sandbox = ProgramSandbox()  # Fail closed before expensive checkpoint loading.
    backend = TorchGenerationBackend(args.checkpoint, args.checkpoint_id, args.revision, args.device)
    outcomes, measurement = measure_pairs(backend, sandbox, seeds=args.seeds, budgets=args.budgets)
    metadata = write_results(args.output, outcomes, measurement)
    print(json.dumps({"measurement_kind": metadata["measurement_kind"],
                      "cost_unit": metadata["cost_unit"], "files": metadata["files"],
                      "paired_executions": metadata["audit"]["paired_executions"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
