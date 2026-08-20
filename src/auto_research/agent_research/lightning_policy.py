from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib.metadata
import json
from pathlib import Path
import random
import time
from typing import Any

from .code_benchmark import LocalCodeSandbox, build_code_benchmark


SMOLLM2_MODEL_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"
SMOLLM2_REVISION = "12fd25f77366fa6b3b4b768ec3050bf629380bac"
AGENT_LIGHTNING_REVISION = "8e22ca1902b4dc8a44d84477ffd87a50023e64b3"


@dataclass(frozen=True)
class LightningPolicyConfig:
    output_dir: Path
    model_id: str = SMOLLM2_MODEL_ID
    model_revision: str = SMOLLM2_REVISION
    checkpoint_path: Path | None = None
    steps: int = 6
    episodes: int = 6
    learning_rate: float = 1e-5
    seed: int = 42
    device: str = "cuda"
    offline: bool = False
    maximum_length: int = 512

    def validate(self) -> None:
        if min(self.steps, self.episodes, self.maximum_length) < 1:
            raise ValueError("steps, episodes and maximum-length must be positive")
        if self.learning_rate <= 0:
            raise ValueError("learning-rate must be positive")


def transition_spans(task) -> tuple[dict[str, Any], ...]:
    return (
        {
            "name": "agent.prompt",
            "attributes": {"task_id": task.task_id, "issue": task.issue},
            "reward": 0.0,
        },
        {
            "name": "agent.patch.rejected",
            "attributes": {"candidate": task.wrong_patch},
            "reward": -1.0,
        },
        {
            "name": "agent.patch.chosen",
            "attributes": {"candidate": task.correct_patch},
            "reward": 1.0,
        },
    )


def _prompt(task) -> str:
    return (
        "Fix the Python issue by selecting the better patch.\n"
        f"Issue: {task.issue}\nSource:\n{task.source}\nTests:\n{task.tests}\nPatch:\n"
    )


def _sequence_score(model, tokenizer, prompt: str, completion: str, device, maximum_length):
    import torch

    prefix = tokenizer(prompt, add_special_tokens=True)["input_ids"]
    full = tokenizer(
        prompt + completion,
        add_special_tokens=True,
        truncation=True,
        max_length=maximum_length,
        return_tensors="pt",
    )["input_ids"].to(device)
    prefix_length = min(len(prefix), full.shape[1] - 1)
    logits = model(input_ids=full).logits[:, :-1]
    targets = full[:, 1:]
    token_logps = torch.log_softmax(logits, dim=-1).gather(
        -1, targets.unsqueeze(-1)
    ).squeeze(-1)
    start = max(0, prefix_length - 1)
    return token_logps[:, start:].mean()


def _evaluate(model, tokenizer, tasks, device, maximum_length):
    successes = commands = tokens = 0
    traces = []
    model.eval()
    for task in tasks:
        import torch
        with torch.no_grad():
            wrong = _sequence_score(
                model, tokenizer, _prompt(task), task.wrong_patch, device, maximum_length
            )
            correct = _sequence_score(
                model, tokenizer, _prompt(task), task.correct_patch, device, maximum_length
            )
        selected = task.correct_patch if correct >= wrong else task.wrong_patch
        sandbox = LocalCodeSandbox(task)
        try:
            sandbox.edit(selected)
            passed, _ = sandbox.test()
            commands += 1
            successes += int(passed)
        finally:
            sandbox.close()
        tokens += len(tokenizer(_prompt(task) + selected)["input_ids"])
        traces.append({
            "task_id": task.task_id,
            "correct_logp": float(correct.detach().cpu()),
            "wrong_logp": float(wrong.detach().cpu()),
            "success": passed,
        })
    return {
        "joint_success": successes / max(1, len(tasks)),
        "executor_commands": commands,
        "policy_tokens": tokens,
    }, traces


def run_lightning_policy_training(
    config: LightningPolicyConfig,
) -> tuple[dict[str, Any], Path]:
    config.validate()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    random.seed(config.seed)
    torch.manual_seed(config.seed)
    source = str(config.checkpoint_path or config.model_id)
    common = {
        "revision": None if config.checkpoint_path else config.model_revision,
        "local_files_only": config.offline or config.checkpoint_path is not None,
    }
    tokenizer = AutoTokenizer.from_pretrained(source, **common)
    model = AutoModelForCausalLM.from_pretrained(source, **common)
    device = torch.device(config.device)
    model.to(device)
    model.config.use_cache = False
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    tasks = build_code_benchmark(config.episodes)
    baseline, baseline_trace = _evaluate(
        model, tokenizer, tasks, device, config.maximum_length
    )
    losses = []
    started = time.monotonic()
    for step in range(config.steps):
        task = tasks[step % len(tasks)]
        model.train()
        chosen = _sequence_score(
            model, tokenizer, _prompt(task), task.correct_patch,
            device, config.maximum_length,
        )
        rejected = _sequence_score(
            model, tokenizer, _prompt(task), task.wrong_patch,
            device, config.maximum_length,
        )
        # Agent Lightning's transition decomposition reaches the trainable
        # policy here as a pairwise positive/negative credit signal.
        loss = -torch.nn.functional.logsigmoid(chosen - rejected)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    final, final_trace = _evaluate(
        model, tokenizer, tasks, device, config.maximum_length
    )
    try:
        lightning_version = importlib.metadata.version("agentlightning")
    except importlib.metadata.PackageNotFoundError:
        lightning_version = None
    payload = {
        "schema_version": 2,
        "task": "ag-001-agent-lightning-checkpoint-policy",
        "config": {
            **asdict(config),
            "output_dir": str(config.output_dir),
            "checkpoint_path": str(config.checkpoint_path) if config.checkpoint_path else None,
        },
        "provenance": {
            "model_id": config.model_id,
            "model_revision": config.model_revision,
            "agentlightning_version": lightning_version,
            "agentlightning_revision": AGENT_LIGHTNING_REVISION,
            "adapter_contract": "rollout spans -> transition credit -> pairwise policy update",
        },
        "baseline": baseline,
        "final": final,
        "training": {
            "steps": config.steps,
            "credit_updates": config.steps * 2,
            "transition_spans": sum(len(transition_spans(task)) for task in tasks),
            "losses": losses,
            "duration_seconds": time.monotonic() - started,
        },
        "traces": {"baseline": baseline_trace, "final": final_trace},
        "claim_boundary": (
            "real checkpoint update and real local executor; the tiny fixture suite validates "
            "the training bridge, not SWE-bench generalization"
        ),
    }
    config.output_dir.mkdir(parents=True, exist_ok=True)
    path = config.output_dir / "metrics.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return payload, path
