"""Execute real checkpoint Agent mechanisms; short runs are runtime diagnostics."""

import argparse
import json
from pathlib import Path

from auto_research.agent_research.hippocam import Hippocam
from auto_research.agent_research.mass import Task, run_mass
from auto_research.agent_research.oct10_backend import (
    EvoAllocBackend,
    HippocamBackend,
    LocalLanguageModel,
    MASSBackend,
    bounded_calculator_rollouts,
    race_actor_step,
    race_sft,
)
from auto_research.agent_research.race import TrainingTrajectory, Turn


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=("mass", "race", "hippocam", "evoalloc"), required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument(
        "--race-bounded",
        action="store_true",
        help="Run public executable calculator L1 environment, not official benchmark",
    )
    parser.add_argument("--race-episodes", type=int, default=64)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.dataset.read_text().splitlines() if line.strip()]
    if not rows or any(not isinstance(row.get("question"), str) for row in rows):
        raise ValueError("training JSONL requires question strings")
    settings = {"device": args.device, "seed": args.seed, "max_tokens": args.max_tokens}
    if args.method == "mass":
        backend = MASSBackend(args.checkpoint, **settings)
        tasks = tuple(
            Task(
                str(i),
                row["question"],
                "Solve independently; verifier checks derivation; integrate.",
            )
            for i, row in enumerate(rows[:1])
        )
        backend, audits = run_mass(
            backend, tasks, cycles=2, search_iterations=1, candidates=3, selected=2
        )
        result = {"cycles": 2, "audits": audits, "training": backend.training_audits}
    elif args.method == "race":
        backend = LocalLanguageModel(args.checkpoint, **settings)
        if args.race_bounded:
            import torch
            from auto_research.post_training.oct10_checkpoint import install_lora

            trajectories, advantages, rewards = bounded_calculator_rollouts(
                backend, episodes=args.race_episodes
            )
            initial_successes = [t for t in trajectories if t.successful]
            if not initial_successes:
                raise RuntimeError(
                    "No successful native rollout for SFT; no oracle fallback allowed"
                )
            result = race_sft(backend, initial_successes[0])
            # Sample again from the SFT-updated policy before its RL update.
            trajectories, advantages, rewards = bounded_calculator_rollouts(
                backend, episodes=args.race_episodes
            )
            parameters = [p for p in backend.model.parameters() if p.requires_grad]
            if not parameters:
                install_lora(backend.model)
                parameters = [p for p in backend.model.parameters() if p.requires_grad]
            optimizer = torch.optim.AdamW(parameters, lr=3e-5)
            result["actor_step"] = race_actor_step(backend, trajectories, advantages, optimizer)
            result["on_policy_successes"] = sum(rewards)
            result["on_policy_episodes"] = len(rewards)
            result["on_policy_rl_evaluated"] = True
            result["environment"] = (
                "auto-research bounded-calculator-v1 (L1, not official ScienceWorld)"
            )
        else:
            result = run_race_trace(backend, rows[0])
    elif args.method == "hippocam":
        backend = HippocamBackend(args.checkpoint, **settings)
        result = run_hippocam(backend, rows)
    else:
        result = run_evoalloc(args, settings)
    result.update(
        {
            "method": args.method,
            "seed": args.seed,
            "diagnostic_only": True,
            "evaluation_tier": "L1",
            "checkpoint": str(args.checkpoint),
            "device": args.device,
        }
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(
        json.dumps({k: v for k, v in result.items() if k not in {"audits", "history", "training"}})
    )


def run_race_trace(backend, row):
    # The caller supplies real recorded environment traces, not lines of a
    # QA explanation relabelled as fictitious actions/observations.
    if row.get("split") != "train" or row.get("successful") is not True:
        raise ValueError("RACE SFT requires explicitly successful training trace")
    if not row.get("environment") or not row.get("source_revision"):
        raise ValueError("trace requires public environment and source revision provenance")
    turns = tuple(Turn(t["reasoning"], t["action"], t["observation"]) for t in row["turns"])
    trajectory = TrainingTrajectory(row["question"], turns, True)
    result = race_sft(backend, trajectory)
    result["training_only_reference_actions"] = True
    result["on_policy_rl_evaluated"] = False
    result["environment"] = row["environment"]
    return result


def run_hippocam(backend, rows):
    memory = Hippocam(
        backend.tokenizer.encode,
        backend.summarize,
        capacity=2048,
        rounds=1,
        minimum_tail=128,
        min_saving=16,
    )
    for i, row in enumerate(rows[:3]):
        memory.append("user", row["question"], round_id=str(i), complete=False)
        memory.janus(**backend.janus(memory))
        messages = [{"role": m.role, "content": m.content} for m in memory.context]
        overhead = max(0, backend.prompt_ids(messages).numel() - memory.tokens(memory.context))
        memory.pressure_control(overhead_tokens=overhead)
        response = backend.generate(
            [{"role": m.role, "content": m.content} for m in memory.context]
        )
        memory.append("assistant", response, round_id=str(i), complete=False)
        memory.after_response()
        memory.complete_round(str(i))
    references = list(memory.archive)
    result = {
        "archive_nodes": len(references),
        "active_messages": len(memory.context),
        "recall_children": len(memory.recall(references[0])) if references else 0,
        "context_tokens": memory.tokens(memory.context),
        "janus_schedule": "real shared-checkpoint operation/purpose/exit-condition generation",
    }
    # Separately labelled deterministic controller probe exercises the real
    # Precip/Palim backend even when this small model never chooses CLOSE.
    probe = Hippocam(
        backend.tokenizer.encode,
        backend.summarize,
        capacity=2048,
        rounds=1,
        minimum_tail=8,
        min_saving=1,
    )
    probe.janus(
        open_intents=(("Read an observed record", "record read"),),
        guidance="I will read the record.",
    )
    probe.append("user", rows[0]["question"])
    probe.janus(close=1, guidance="The record has been read.")
    probe.append("assistant", "Continue with new work.")
    probe.after_response()
    probe.append("user", (rows[0]["question"] + "\n") * 80)
    probe.append(
        "assistant",
        "Keep this unfinished tool exchange intact.",
        round_id="protected-probe",
        complete=False,
    )
    before = probe.tokens(probe.context)
    probe.pressure_control()
    result["controlled_precip_probe_archive_nodes"] = len(probe.archive)
    result["controlled_palim_tokens_before"] = before
    result["controlled_palim_tokens_after"] = probe.tokens(probe.context)
    result["controlled_probe_is_capability_evidence"] = False
    return result


def run_evoalloc(args, settings):
    from auto_research.agent_research.evoalloc import evolve_allocation
    from auto_research.agent_research.program_sandbox import CIRCLE_INITIAL

    backend = EvoAllocBackend(args.checkpoint, **settings)
    initial = backend.sandbox.evaluate_packing(CIRCLE_INITIAL).score
    result = evolve_allocation(
        initial_archive={"initial": initial},
        initial_strategy="Evaluate potentially improved valid packings; discard obvious invalid code.",
        propose=backend.propose,
        decide=backend.decide,
        full_evaluate=backend.full_evaluate,
        update_experiences=backend.update_experiences,
        reflect_strategy=backend.reflect_strategy,
        budget=4,
        experience_interval=1,
        strategy_interval=2,
        exploration=0.3,
        seed=args.seed,
    )
    result["history"] = [
        {
            "candidate": entry["candidate"].identifier,
            "actions": entry["allocation"].actions,
            "score": entry["observed_score"],
            "reason": entry["evaluation_reason"],
        }
        for entry in result["history"]
    ]
    from dataclasses import asdict

    result["experiences"] = [asdict(e) for e in result["experiences"]]
    result["controlled_reflection_probe"] = backend.reflect_strategy(result["strategy"], (), ())
    result["controlled_reflection_is_promoted_strategy"] = False
    return result


if __name__ == "__main__":
    main()
