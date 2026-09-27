"""PACT must train on sampled tokens without reading the reference completion."""

from __future__ import annotations

import math

import pytest

from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.post_training.generation import CharacterTokenizer, build_policy
from auto_research.post_training.pact import build_critic, pact_step


def test_pact_requires_freely_generated_responses():
    with pytest.raises(ValueError, match="requires a free-generation dataset"):
        PostTrainingConfig(algorithm="pact", dataset="arithmetic-smoke")


def test_pact_updates_actor_before_critic_and_uses_post_actor_ratios():
    torch = pytest.importorskip("torch")
    torch.manual_seed(13)
    tokenizer = CharacterTokenizer(["question", " answer", "42"])
    policy = build_policy(len(tokenizer), 12)
    critic = build_critic(len(tokenizer), 12)
    actor_before = [row.detach().clone() for row in policy.parameters()]
    critic_before = [row.detach().clone() for row in critic.parameters()]
    actor_optimizer = torch.optim.AdamW(policy.parameters(), lr=0.01)
    critic_optimizer = torch.optim.AdamW(critic.parameters(), lr=0.01)

    actor_loss, diagnostics = pact_step(
        policy, critic, tokenizer, "question", [tuple(tokenizer.encode(" 42")), tuple(tokenizer.encode(" 11"))],
        [1.0, 0.0], actor_optimizer, critic_optimizer, "cpu",
    )
    assert math.isfinite(actor_loss)
    assert diagnostics["update_order"] == "actor-then-critic"
    assert diagnostics["critic_target"].startswith("post-actor current-token IS")
    assert diagnostics["critic_accepted_fraction"] == 1.0
    assert diagnostics["post_actor_ratio_mean"] != pytest.approx(1.0, abs=1e-8)
    assert any(not torch.equal(before, after) for before, after in zip(actor_before, policy.parameters()))
    assert any(not torch.equal(before, after) for before, after in zip(critic_before, critic.parameters()))


def test_pact_runner_writes_verifiable_small_model_result(tmp_path):
    pytest.importorskip("torch")
    result, run_dir = PostTrainingRunner(PostTrainingConfig(
        algorithm="pact", dataset="arithmetic-generate", steps=1,
        maximum_examples=8, group_size=2, seeds=(42,), output_dir=tmp_path,
        allow_network=False,
    )).run()
    assert result.training["runs"][0]["critic_parameters"] > 0
    assert result.training["runs"][0]["history"][0]["update_order"] == "actor-then-critic"
    if result.baseline["accuracy"] == 0:
        assert result.relative_accuracy is None
        assert "不适用（基线为 0）" in (run_dir / "report.md").read_text()
    assert (run_dir / "metrics.json").is_file()
