"""Real gradients on a tiny neural fixture; not capability measurements."""
import torch
from torch import nn
from types import SimpleNamespace

from auto_research.agent_research.oct10_backend import LocalLanguageModel, race_actor_step
from auto_research.agent_research.race import TrainingTrajectory, Turn


def test_mass_samples_each_worker_with_independent_role_index(monkeypatch):
    from auto_research.agent_research.mass import Conversation
    import auto_research.post_training.oct10_checkpoint as checkpoint
    monkeypatch.setattr(checkpoint, "install_lora", lambda model: None)
    backend = LocalLanguageModel.__new__(LocalLanguageModel)
    backend.model, backend.device = NeuralFixture(), "cpu"
    observed = []
    def continuation(context, target):
        observed.append(target)
        return backend.model.bias[:1] - 1
    backend.continuation = continuation
    conversations = [Conversation(role, ({"role": "user", "content": "task"},
        {"role": "assistant", "content": text}))
        for role, text in (("orchestrator", "o"), ("worker", "w1"), ("worker", "w2"))]
    backend.train_conversations(conversations, conversations[:1], steps=3)
    assert observed[:3] == ["o", "w1", "w2"]


class Tokenizer:
    def encode(self, text, **kwargs):
        return [ord(c) for c in text]

    def apply_chat_template(self, messages, **kwargs):
        return "USER:" + messages[-1]["content"] + "ASSISTANT:"

    def decode(self, tokens, **kwargs):
        return "".join(chr(t) for t in tokens)

    def __call__(self, text, **kwargs):
        return {"offset_mapping": [(i, i + 1) for i in range(len(text))]}


class NeuralFixture(nn.Module):
    def __init__(self):
        super().__init__()
        self.bias = nn.Parameter(torch.zeros(128))

    def forward(self, ids, **kwargs):
        return SimpleNamespace(logits=self.bias.expand(*ids.shape, 128))


def test_actor_closure_has_real_gradient_and_excludes_forced_syntax():
    backend = LocalLanguageModel.__new__(LocalLanguageModel)
    backend.model, backend.tokenizer, backend.device = NeuralFixture(), Tokenizer(), "cpu"
    def turn(reasoning, action):
        target = "<think>" + reasoning + "</think>\nAction:" + action
        start = len("<think>")
        mask = tuple(start <= i < start + len(reasoning) or i == len(target) - 1
                     for i in range(len(target)))
        return Turn(reasoning, action, "tool result", tuple(map(ord, target)), mask, ("A", "B"), target)
    successful = TrainingTrajectory("tool task", (turn("r", "A"), turn("s", "B")), True)
    failure = TrainingTrajectory("tool task", (turn("r", "B"),), False)
    optimizer = torch.optim.AdamW(backend.model.parameters(), lr=.01)
    result = race_actor_step(backend, (successful, failure), (1., -1.), optimizer)
    assert result["closure_terms"] == 1
    assert result["original_policy_tokens"] == 6
    assert result["skipped_reasoning_tokens"] == 1
    assert backend.model.bias.grad[ord(">")] < 0
    assert backend.model.bias.abs().sum() > 0
