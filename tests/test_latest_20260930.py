from __future__ import annotations

import numpy as np
import pytest

from auto_research.agent_research.latest_20260930 import (
    HarnessProposer,
    Transition,
    adapt_harness,
    graphhca_credit,
    multi_memory_grpo_objective,
    time_evolving_memory,
    video_rsi_accept,
)
from auto_research.foundation_latest_20260930 import (
    ChineseJevHead,
    MultiScaleGLA,
    causal_hold_upsample,
    chinese_jev_objective,
    leapquant_compress,
    leapquant_window,
    masked_block_average,
    stepquant_bit_allocation,
    stepquant_dual_axis,
)
from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.post_training.latest_20260930 import (
    LSPDReplayBuffer,
    dr_opd_reverse_kl,
    dr_opd_token_weights,
    lspd_objective,
    roft_retrospection_loss,
    sipo_token_advantage,
    token_policy_gradient_loss,
)
from auto_research.reproductions.helix.experiment import reproduce as reproduce_helix
from auto_research.reproductions.helix.model import HELIXCore, mixup_channels


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


def test_stepquant_allocation_and_dual_axis_quantization():
    torch = pytest.importorskip("torch")
    allocation = stepquant_bit_allocation(
        [[1.0, .25], [.6, .2]], [-.01, -.4], (4, 8), average_bits=6,
    )
    assert allocation["used_bits"] <= allocation["budget_bits"]
    assert allocation["bits"][0] >= allocation["bits"][1]
    state = torch.tensor([[8.0, .5, .25], [.2, .1, .05]])
    restored, audit = stepquant_dual_axis(state, torch.tensor([4.0, 1.0]), bits=4)
    assert restored.shape == state.shape
    assert audit["row_scale"].shape == (2,)
    assert torch.isfinite(restored).all()


def test_leapquant_compensator_and_window_reduce_boundary_requantization():
    torch = pytest.importorskip("torch")
    state = torch.diag(torch.tensor([12.0, 2.0, .4, .1]))
    no_compensator, _ = leapquant_compress(state, bits=4, rank=0)
    compensated, audit = leapquant_compress(state, bits=4, rank=1)
    assert (compensated - state).square().mean() < (no_compensator - state).square().mean()
    decays = torch.full((3, 4), .95)
    keys = torch.eye(4)[:3]
    corrections = torch.flip(keys, dims=(1,))
    boundary, window = leapquant_window(state, decays, keys, corrections, bits=4, rank=1)
    assert boundary.shape == state.shape and len(window["intermediate_states"]) == 3


def test_chinese_jev_candidate_head_and_rlcd_objective():
    torch = pytest.importorskip("torch")
    head = ChineseJevHead(16)
    hidden = torch.randn(3, 4, 16, requires_grad=True)
    logits = head(hidden, torch.tensor([0, 1, 2]))
    targets = torch.eye(4)[:3]
    loss, audit = chinese_jev_objective(
        logits, targets, torch.tensor([0, 1, 2]),
        generator=torch.Generator().manual_seed(42),
    )
    loss.backward()
    assert logits.shape == (3, 4) and hidden.grad is not None
    assert audit["reward_std"] > 0


def test_dr_opd_jvp_credit_and_sipo_uniform_failure_signal():
    torch = pytest.importorskip("torch")
    discrepancy = torch.tensor([[.2, -.4], [.1, .5]])
    derivative = torch.tensor([[1.0, .5], [-.5, 2.0]])
    weights, audit = dr_opd_token_weights(discrepancy, derivative, strength=.5)
    assert weights.shape == discrepancy.shape and audit["credit_rms"] > 0
    student = torch.tensor([[-1.0, -2.0], [-1.5, -2.5]], requires_grad=True)
    loss = dr_opd_reverse_kl(student, student.detach() - discrepancy, weights, torch.ones_like(student))
    loss.backward()
    assert student.grad is not None
    advantage, sipo_audit = sipo_token_advantage(
        torch.zeros(2),
        torch.tensor([[-1.0, -1.1], [-.8, -1.2]]),
        torch.tensor([[-1.3, -1.0], [-1.1, -1.0]]),
        torch.ones(2, 2),
    )
    assert sipo_audit["uniform_failure_group"] is True
    assert advantage.abs().sum() > 0
    assert token_policy_gradient_loss(student, advantage, torch.ones_like(student)).isfinite()


def test_remem_propagates_final_advantage_without_gold_memory_update():
    torch = pytest.importorskip("torch")
    seen = []

    def update(memory, chunk):
        seen.append((memory, chunk))
        return memory + tuple(chunk)

    memory, trace = time_evolving_memory(list("abcdef"), chunk_size=2, memory_budget=3, update=update)
    assert memory == ("d", "e", "f") and len(trace) == 3
    objective, audit = multi_memory_grpo_objective(
        torch.tensor([[1.1, .9], [.9, 1.1]]),
        torch.tensor([[[1.1, .9], [1.0, 1.0]], [[.9, 1.1], [1.0, 1.0]]]),
        torch.tensor([1.0, 0.0]),
    )
    assert objective.isfinite() and audit["memory_count"] == 2


def test_video_rsi_gate_and_helix_one_way_cache():
    accepted, reason = video_rsi_accept(.6, 100, .61, 108, maximum_cost_growth=.1)
    assert accepted and reason.startswith("accuracy_gain")
    accepted, _ = video_rsi_accept(.6, 100, .595, 80, minimum_cost_reduction=.1, maximum_accuracy_loss=.01)
    assert accepted
    torch = pytest.importorskip("torch")
    tokens = torch.arange(32.0).reshape(1, 4, 8)
    assert mixup_channels(tokens).shape == tokens.shape
    model = HELIXCore(16)
    user = torch.randn(2, 5, 16)
    cache = model.encode_user(user)
    score, hidden = model(torch.randn(2, 4, 16), torch.randn(2, 3, 16), user_cache=cache)
    assert score.shape == (2,) and hidden.shape == (2, 4, 16)
    result = reproduce_helix(None, seed=42)
    assert result["metrics"]["user_cache_unchanged"] is True
