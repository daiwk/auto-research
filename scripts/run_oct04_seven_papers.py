"""Reproducible CPU mechanism experiments, not paper benchmark replications.

Run with PYTHONPATH=src python scripts/run_oct04_seven_papers.py.
Optional --tabpfn-checkpoint runs the real frozen official regressor separately.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
from pathlib import Path
import tempfile

import numpy as np
import torch

from auto_research.agent_research.causal_memory_policy import (
    balanced_exposure,
    estimate_utility,
    query_decision,
)
from auto_research.agent_research.mingbird import flat_prefill, run_task
from auto_research.agent_research.t2spo import TrajectoryMemory, FrozenDistanceEstimator
from auto_research.latest_20261004_followup_catalog import LATEST_METHOD_PAPERS
from auto_research.post_training.oct04_objectives import (
    clipped_policy_loss,
    rlcpr_rewards,
    rlcpr_sampling_probabilities,
    t2spo_credit,
    weakest_link_loss,
)
from auto_research.post_training.tess import fit_tess
from auto_research.system_one.contracts import DecisionAnswer, SystemOneResponse
from auto_research.system_one.lookahead import choose_with_lookahead

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_REVISION = "4972a65a1b30806315c6f92499959ffbfc69a673"
CHECKPOINT_SHA256 = "2ab5a07d5c41dfe6db9aa7ae106fc6de898326c2765be66505a07e2868c10736"


class ForkableRooms:
    """Public diagnostic simulator with no reward exposed to the provider."""

    def __init__(self):
        self.room = "hall"

    def fork(self):
        return copy.deepcopy(self)

    def admissible_commands(self):
        return (
            ("enter kitchen", "enter bedroom")
            if self.room == "hall"
            else (("wash cup", "leave") if self.room == "enter kitchen" else ("sleep", "leave"))
        )

    def step(self, command):
        self.room = command
        return command


class DiagnosticProvider:
    """Explicit lexical fixture; never reported as trained Jev capability."""

    def decide(self, request):
        options = request.questions["action"].criteria
        key = next(k for k, v in options.items() if "wash cup" in v["then newly possible"])
        return SystemOneResponse(
            model="lexical-diagnostic",
            answers={
                "action": DecisionAnswer(
                    type="choice",
                    value=key,
                    probabilities={k: float(k == key) for k in options},
                    confidence=1.0,
                )
            },
        )


def experiments(seed):
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    output = {}
    # Actual optimization of the exact-vocabulary constraint objective.
    logits = torch.nn.Parameter(torch.randn(1, 3) * 0.1)
    teacher = torch.tensor([[0.7, 0.29, 0.01]]).log()
    optimizer = torch.optim.Adam([logits], lr=0.05)
    before = float(logits.softmax(-1)[0, 2].detach())
    for _ in range(80):
        optimizer.zero_grad()
        action = torch.multinomial(logits.detach().softmax(-1), 1).flatten()
        loss = weakest_link_loss(
            logits, action, teacher, torch.ones_like(logits), budget=2.0, penalty=4.0
        )
        loss.backward()
        optimizer.step()
    output["weakest-link"] = {
        "unsafe_probability_before": before,
        "unsafe_probability_after": float(logits.softmax(-1)[0, 2].detach()),
    }
    d = torch.tensor([4.0, 3.0, 2.0, 1.0])
    credit = t2spo_credit(
        d,
        torch.tensor([3.0, 4.0, 1.0, 0.5]),
        mask=torch.ones(4, dtype=torch.bool),
        success_terminal=torch.tensor([False, False, False, True]),
        failure_terminal=torch.zeros(4, dtype=torch.bool),
        truncated=torch.zeros(4, dtype=torch.bool),
    )
    lp = torch.zeros(4, requires_grad=True)
    clipped_policy_loss(lp, lp.detach(), credit, torch.ones(4, dtype=torch.bool)).backward()
    output["t2spo"] = {
        "progress_credit": float(credit[0]),
        "regression_credit": float(credit[1]),
        "terminal_credit": float(credit[-1]),
        "gradient_norm": float(lp.grad.norm()),
    }
    post = torch.tensor([[0.1, 0.9], [0.50, 0.51]])
    shaped, active = rlcpr_rewards(post, torch.tensor([[1.0, 2.0], [100.0, 200.0]]))
    probs = rlcpr_sampling_probabilities(torch.tensor([0.0, 1.0, 2.0, 3.0]))
    output["rlcpr"] = {
        "active_groups": int(active.sum()),
        "long_rollout_penalty": float((shaped - post)[1, 1]),
        "low_entropy_probability": float(probs[0]),
        "high_entropy_probability": float(probs[-1]),
    }
    exposure = balanced_exposure(12, 600, 2, seed=seed)
    # Effects are simulator ground truth visible only to outcome generation.
    effects = np.array([1.0, -1.0] + [0.0] * 10)
    outcomes = exposure @ effects + rng.normal(0, 0.1, 600)
    utility, error = estimate_utility(exposure, outcomes)
    output["causal-memory-policy"] = {
        "positive_utility": float(utility[0]),
        "negative_utility": float(utility[1]),
        "positive_se": float(error[0]),
        "negative_se": float(error[1]),
        "exposure_min": int(exposure.sum(0).min()),
        "exposure_max": int(exposure.sum(0).max()),
        "negative_forgotten": query_decision(utility[1], error[1]) == "forget",
    }
    # Disjoint feature draws; validation steers W; test is not consumed anywhere.
    x, v, pool = torch.randn(64, 2), torch.randn(32, 2), torch.randn(48, 2)
    y, vy = (x[:, 0] > 0).long(), (v[:, 0] + 0.8 * v[:, 1] > 0).long()
    result = fit_tess(
        torch.nn.Linear(2, 2),
        torch.nn.Sequential(torch.nn.Linear(2, 16), torch.nn.Tanh(), torch.nn.Linear(16, 1)),
        train_batch=(x, y),
        validation_batch=(v, vy),
        train_features=x,
        pool_features=pool,
        steps=60,
        selector_steps=120,
        learning_rate=0.02,
        per_example_loss=lambda model, batch: torch.nn.functional.cross_entropy(
            model(batch[0]), batch[1], reduction="none"
        ),
    )
    output["tess"] = {
        "pvm_initial": result["pvm_losses"][0],
        "pvm_final": result["pvm_losses"][-1],
        "pool_score_std": float(result["scores"].std()),
        "scored_pool_examples": len(pool),
    }
    env = ForkableRooms()
    command, options = choose_with_lookahead(
        env, DiagnosticProvider(), task="wash cup", observation="hall"
    )
    output["jev-lookahead"] = {
        "simulated_branches": len(options),
        "real_state_unchanged": env.room == "hall",
        "selected_command": command,
        "provider": "lexical-diagnostic",
    }
    with tempfile.TemporaryDirectory() as directory:
        artifact = Path(directory) / "report.txt"
        sequence = iter(
            [
                "finish",
                json.dumps({"tool": "write", "arguments": {"text": "checked report"}}),
                "finish",
            ]
        )

        def write(text):
            artifact.write_text(text)
            return "artifact written"

        result = run_task(
            lambda _: next(sequence),
            {"write": write},
            {"artifact exists": artifact.is_file},
            task="write report",
            max_turns=3,
        )
        prefill = flat_prefill(
            {"write": {"domains": ["files"], "parameters": {"text": "str"}, "required": ["text"]}},
            domain="files",
            budget_bytes=128,
        )
        output["mingbird"] = {
            "false_finish_rejected": not result["trace"][0]["complete"],
            "artifact_written": artifact.is_file(),
            "turns": len(result["trace"]),
            "prefill_bytes": len(prefill.encode()),
            "policy": "scripted-diagnostic",
        }
    return output


def run_tabpfn(checkpoint):
    checksum = hashlib.sha256(Path(checkpoint).read_bytes()).hexdigest()
    if checksum != CHECKPOINT_SHA256:
        raise ValueError("checkpoint does not match the pinned official revision")
    results = []
    for seed in (42, 43, 44):
        rng = np.random.default_rng(seed)
        memory = TrajectoryMemory()
        for round_id in range(5):
            step = np.arange(1, 7)
            features = np.column_stack(
                [6 - step, step, np.full(6, round_id), rng.normal(0, 0.1, 6)]
            )
            memory.add_completed(features, successful=True)
        estimator = FrozenDistanceEstimator(checkpoint, dimensions=3, seed=seed)
        estimator.fit_snapshot(memory)
        query = np.column_stack([6 - np.arange(1, 7), np.arange(1, 7), np.full(6, 5), np.zeros(6)])
        before = estimator.predict(query)
        memory.add_completed(query * 2, successful=True)
        after = estimator.predict(query)
        results.append(
            dict(
                seed=seed,
                mae=float(np.abs(before - np.arange(6, 0, -1)).mean()),
                prediction_min=float(before.min()),
                prediction_max=float(before.max()),
                frozen_snapshot_unchanged=bool(np.array_equal(before, after)),
            )
        )
    path = ROOT / "docs/post-training/2610.00388-t2spo/metrics/tabpfn-cpu.json"
    payload = dict(
        schema_version=2,
        method="t2spo",
        manifest_ref="post-training:t2spo",
        dataset="synthetic pre-action numeric states; not ALFWorld",
        seeds=[42, 43, 44],
        seed_results=results,
        diagnostic_only=True,
        evaluation_protocol=dict(
            tier="l1_mechanism",
            formal_comparison=False,
            diagnostic_only=True,
            seeds=[42, 43, 44],
            claim_policy="frozen TabPFN on synthetic states; not task capability",
        ),
        provenance=dict(
            checkpoint="Prior-Labs/TabPFN-v2-reg",
            checkpoint_revision=CHECKPOINT_REVISION,
            checkpoint_sha256=checksum,
            tabpfn_version=importlib.metadata.version("tabpfn"),
            dataset_fingerprint="t2spo-synthetic-step-round-distance-v1",
            script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            device="cpu",
            artifact_path=str(path.relative_to(ROOT)),
            command="TABPFN_DISABLE_TELEMETRY=1 PYTHONPATH=src python scripts/run_oct04_seven_papers.py --tabpfn-checkpoint <official-checkpoint>",
        ),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(results), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tabpfn-checkpoint")
    args = parser.parse_args()
    torch.set_num_threads(1)
    if args.tabpfn_checkpoint:
        run_tabpfn(args.tabpfn_checkpoint)
        return
    runs = {seed: experiments(seed) for seed in (42, 43, 44)}
    for paper in LATEST_METHOD_PAPERS:
        key = paper["key"]
        rows = [dict(seed=seed, **runs[seed][key]) for seed in runs]
        aggregates = {
            name + "_mean": float(np.mean([r[name] for r in rows]))
            for name, value in rows[0].items()
            if name != "seed" and type(value) in (float, int)
        }
        path = (
            ROOT / "docs" / Path(paper["detail_path"]).parent / "metrics/mechanism-seeds42-44.json"
        )
        payload = dict(
            schema_version=2,
            method=key,
            manifest_ref=f"{paper['domain']}:{key}",
            dataset="synthetic mechanism diagnostics v1; not paper benchmark",
            seeds=list(runs),
            diagnostic_only=True,
            seed_results=rows,
            aggregate_metrics=aggregates,
            evaluation_protocol=dict(
                tier="l1_mechanism",
                seeds=list(runs),
                formal_comparison=False,
                diagnostic_only=True,
                claim_policy="core equations and executable controls only",
            ),
            provenance=dict(
                artifact_path=str(path.relative_to(ROOT)),
                dataset_fingerprint="oct04-seven-synthetic-mechanisms-v1",
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                device="cpu",
                command="PYTHONPATH=src python scripts/run_oct04_seven_papers.py",
            ),
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        print(key, json.dumps(aggregates), flush=True)


if __name__ == "__main__":
    main()
