from __future__ import annotations

import numpy as np
import pytest

from auto_research.agent_research.latest_20260930 import (
    HarnessProposer,
    Transition,
    adapt_harness,
    graphhca_credit,
)
from auto_research.foundation_latest_20260930 import MultiScaleGLA, causal_hold_upsample, masked_block_average
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.post_training.latest_20260930 import LSPDReplayBuffer, lspd_objective, roft_retrospection_loss


def test_roft_masks_context_and_lspd_detaches_teacher():
    torch = pytest.importorskip("torch")
    logits = torch.randn(1, 5, 7, requires_grad=True)
    loss = roft_retrospection_loss(
        logits, torch.tensor([[0, 1, 2, 3, 4]]), torch.tensor([[0, 0, 0, 1, 1]])
    )
    loss.backward()
    assert logits.grad[0, :3].abs().sum().item() == 0
    student = torch.tensor([[-1.0, -2.0]], requires_grad=True)
    teacher = torch.tensor([[-2.0, -4.0]], requires_grad=True)
    objective, diagnostics = lspd_objective(
        student, teacher, torch.tensor([[2.0, 2.0]]), torch.ones(1, 2), entropy_coeff=.1
    )
    assert objective.item() == pytest.approx(2.3)
    objective.backward()
    assert teacher.grad is None and diagnostics["tail_fraction"] == 0


def test_lspd_replay_and_post_training_dispatch(tmp_path):
    replay = LSPDReplayBuffer(capacity=2)
    for value in range(3):
        replay.append([float(value)], [0.0])
    assert len(replay) == 2
    assert len(replay.sample(2, np.random.default_rng(42))) == 2
    for method in ("roft", "lspd"):
        result, _ = PostTrainingRunner(PostTrainingConfig(
            algorithm=method, allow_network=False, maximum_examples=32,
            steps=2, seed=42, output_dir=tmp_path,
        )).run()
        assert result.training["steps"] == 2
        assert result.training["last_diagnostics"]["diagnostic_only"] == 1.0


def test_msgla_pooling_causal_hold_and_cuda_capable_backward():
    torch = pytest.importorskip("torch")
    hidden = torch.arange(1, 1 + 5 * 4, dtype=torch.float32).reshape(1, 5, 4)
    pooled, mask = masked_block_average(hidden, 2)
    assert pooled.shape == (1, 3, 4) and mask.tolist() == [[1.0, 1.0, 1.0]]
    branch = torch.tensor([[[1.0], [2.0], [3.0]]])
    assert causal_hold_upsample(branch, 2, 5).squeeze().tolist() == [0.0, 1.0, 1.0, 2.0, 2.0]
    layer = MultiScaleGLA(4, scales=(1, 2))
    x = torch.randn(2, 7, 4, requires_grad=True)
    output, audit = layer(x)
    output.square().mean().backward()
    assert output.shape == x.shape
    assert audit["routing_weights"].shape == (2, 7, 2)
    assert x.grad is not None


def test_graphhca_fixed_point_and_same_state_credit():
    rollouts = [
        ([Transition("s0", "short", "goal")], True),
        ([Transition("s0", "detour", "s1"), Transition("s1", "finish", "goal")], True),
        ([Transition("s0", "bad", "fail")], False),
    ]
    result = graphhca_credit(rollouts, discount=.9)
    assert result["values"]["goal"] == 1
    assert result["values"]["fail"] == 0
    assert result["values"]["s0"] > 0
    assert result["step_advantages"][0] > result["step_advantages"][2]


def test_harness_learning_uses_execution_reports_and_revises_repeatedly():
    proposer = HarnessProposer()
    for _ in range(8):
        proposer.train_step([.1, .2, .9, .3], learning_rate=.2)
    assert proposer.propose({"failure": "timeout"}) == "interpreter"

    def execute(harness):
        return {"score": len(harness) / 4, "failure": "missing_evidence" if "retrieve" not in harness else ""}

    harness, trace = adapt_harness(proposer, ("retry",), execute, rounds=3)
    assert len(trace) == 3
    assert all(set(row) == {"round", "revision", "report"} for row in trace)
    assert "interpreter" in harness
