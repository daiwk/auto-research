"""Orchestration-only fixtures; these tests are never capability/GPU evidence."""
from types import SimpleNamespace

import pytest
import torch

from auto_research.post_training.response_policy import GeneratedResponse
from auto_research.post_training.proximal_checkpoint import run_proximal_checkpoint


class FixturePolicy:
    seen = []
    def __init__(self, **kwargs):
        self.model = torch.nn.Linear(1, 1, bias=False)
        torch.nn.init.zeros_(self.model.weight)
        self.provenance = {"kind": "unit-test-fixture-not-capability-evidence"}
        self.optimizer = None
    def prepare_lora(self, **kwargs):
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=.01)
    def generate(self, messages, *, samples=1, **kwargs):
        self.seen.extend(messages)
        return [GeneratedResponse((1,) if i % 2 == 0 else (2,), "31" if i % 2 == 0 else "7", False)
                for i in range(samples)]
    def token_statistics(self, messages, tokens, **kwargs):
        self.seen.extend(messages)
        sign = 1. if tokens[0] == 1 else -1.
        current = self.model.weight.flatten() * sign - 1.
        return current, None
    def trainable_digest(self):
        return str(self.model.weight.detach().tolist())


@pytest.mark.parametrize("method", ["gppo-framework", "tapo-trajectory", "grpo-control"])
def test_proximal_runtime_updates_without_sending_reference_to_generator(method, monkeypatch, tmp_path):
    import auto_research.post_training.proximal_checkpoint as module
    FixturePolicy.seen = []
    monkeypatch.setattr(module, "ResponsePolicy", FixturePolicy)
    monkeypatch.setattr(module, "validate_holdout", lambda *args, **kwargs: {"verified": True})
    monkeypatch.setattr(module, "load_public_rows", lambda path: [{"question": "Public question", "answer": "SECRET_GOLD #### 31"}])
    result = run_proximal_checkpoint(method=method, student_path=tmp_path, student_id="fixture", student_revision="fixture",
                                     train_path=tmp_path, validation_path=tmp_path, split_manifest=tmp_path,
                                     dataset_revision="fixture", device="cpu", steps=2, inner_updates=2,
                                     max_tokens=16, validation_examples=1)
    assert result["parameters_changed"]
    assert len(result["training"]) == 2
    assert result["training"][0]["updates"][0]["gradient_l2_norm"] > 0
    assert result["training"][0]["advantages"][0] > 0
    assert "SECRET_GOLD" not in str(FixturePolicy.seen)
    assert result["diagnostic_only"]


def test_zero_advantage_runtime_fails_instead_of_claiming_training(monkeypatch, tmp_path):
    import auto_research.post_training.proximal_checkpoint as module
    class ZeroPolicy(FixturePolicy):
        def generate(self, messages, *, samples=1, **kwargs):
            return [GeneratedResponse((1,), "7", False) for _ in range(samples)]
    monkeypatch.setattr(module, "ResponsePolicy", ZeroPolicy)
    monkeypatch.setattr(module, "validate_holdout", lambda *args, **kwargs: {"verified": True})
    monkeypatch.setattr(module, "load_public_rows", lambda path: [{"question": "Question", "answer": "#### 31"}])
    with pytest.raises(module.ProximalExecutionFailure, match="nonzero-advantage") as failure:
        run_proximal_checkpoint(method="gppo-framework", student_path=tmp_path, student_id="fixture", student_revision="fixture",
                                train_path=tmp_path, validation_path=tmp_path, split_manifest=tmp_path,
                                dataset_revision="fixture", device="cpu", max_task_attempts=2,
                                max_tokens=16, validation_examples=1)
    assert failure.value.evidence["status"] == "failed"
    assert failure.value.evidence["zero_advantage_groups"] == 2


def test_response_policy_never_silently_truncates_history():
    from auto_research.post_training.response_policy import ResponsePolicy
    policy = ResponsePolicy.__new__(ResponsePolicy)
    policy.device, policy.context_limit = "cpu", 4
    class Tokenizer:
        def apply_chat_template(self, messages, **kwargs):
            return "original full history"
        def __call__(self, text, **kwargs):
            return SimpleNamespace(input_ids=torch.ones(1, 5, dtype=torch.long))
    policy.tokenizer = Tokenizer()
    with pytest.raises(ValueError, match="silently truncated"):
        policy.prompt_ids(({"role": "user", "content": "full history"},))
