from dataclasses import fields

import pytest
import torch

from auto_research.agent_research.asteroid import (
    CausalHistoryStudent,
    ExpertExample,
    PublicEpisode,
    ThreeDoorTask,
    collect_iteration,
    deploy,
    diagnostic,
    imitation_loss,
    public_tokens,
)


def test_public_history_has_no_goal_or_expert_action():
    assert {field.name for field in fields(PublicEpisode)} == {
        "action", "reward", "observation", "terminal"
    }
    assert ThreeDoorTask(1).observation == ThreeDoorTask(2).observation == 0
    history = (PublicEpisode(0, 0),)
    records = [ExpertExample(history, ThreeDoorTask(z).expert_episode()) for z in (1, 2)]
    student = CausalHistoryStudent().eval()
    torch.testing.assert_close(student([r.history for r in records])[0], student([history])[0])
    tokens = public_tokens([r.history for r in records], 2, torch.device("cpu"))
    for token in tokens:
        torch.testing.assert_close(token[0], token[1])


def test_collector_samples_student_before_expert_episode(monkeypatch):
    calls = []

    class DoorZeroStudent(CausalHistoryStudent):
        def forward(self, histories):
            assert all(isinstance(x, tuple) for x in histories)
            calls.append("student")
            return torch.tensor([[0.0, -torch.inf, -torch.inf]] * len(histories))

    student = DoorZeroStudent()
    original = ThreeDoorTask.expert_episode

    def spy(task):
        calls.append("teacher")
        return original(task)

    monkeypatch.setattr(ThreeDoorTask, "expert_episode", spy)
    rows = collect_iteration(student, [1, 2], 2, torch.Generator().manual_seed(7))
    assert calls == ["student", "student", "teacher", "teacher"]
    assert [row.expert_episode.action for row in rows] == [1, 2]
    assert all(row.history == (PublicEpisode(0, 0), PublicEpisode(0, 0)) for row in rows)


def test_deployment_has_no_teacher_calls_and_starts_empty(monkeypatch):
    contexts = []

    class RecordingStudent(CausalHistoryStudent):
        def forward(self, histories):
            contexts.extend(histories)
            return torch.tensor([[0.0, -torch.inf, -torch.inf]] * len(histories))

    def forbidden_teacher(task):
        raise AssertionError("deployment must never request privileged expert labels")

    monkeypatch.setattr(ThreeDoorTask, "expert_episode", forbidden_teacher)
    episodes = deploy(RecordingStudent(), ThreeDoorTask(1), 4, torch.Generator().manual_seed(3))
    assert episodes == (PublicEpisode(0, 0),) * 4
    assert list(map(len, contexts)) == [0, 1, 2, 2]


def test_expert_query_nll_matches_independent_reference_and_gradients():
    student = CausalHistoryStudent()
    rows = [
        ExpertExample((PublicEpisode(0, 0),), PublicEpisode(1, 1)),
        ExpertExample((), PublicEpisode(2, 1)),
    ]
    logits = student([row.history for row in rows])
    reference = -(logits[0, 1] - logits[0].logsumexp(0) + logits[1, 2] - logits[1].logsumexp(0)) / 2
    loss = imitation_loss(student, rows)
    torch.testing.assert_close(loss, reference)
    loss.backward()
    assert student.head.weight.grad is not None
    assert student.head.weight.grad.abs().sum() > 0
    assert student.action_embedding.weight.grad.abs().sum() > 0


def test_causal_attention_cannot_read_future_unmasked_token():
    student = CausalHistoryStudent().eval()
    actions = torch.tensor([[3, 0, 1]])
    rewards = torch.tensor([[2, 0, 1]])
    padding = torch.zeros_like(actions, dtype=torch.bool)
    before = student.token_logits(actions, rewards, padding)[:, 0]
    actions[:, 1:] = 2
    rewards[:, 1:] = 0
    after = student.token_logits(actions, rewards, padding)[:, 0]
    torch.testing.assert_close(before, after)


def test_labels_are_supervised_not_given_to_student_inputs():
    student = CausalHistoryStudent()
    history = (PublicEpisode(0, 0),)
    logits = student([history])
    a = imitation_loss(student, [ExpertExample(history, PublicEpisode(1, 1))])
    b = imitation_loss(student, [ExpertExample(history, PublicEpisode(2, 1))])
    torch.testing.assert_close(a, -logits.log_softmax(-1)[0, 1])
    torch.testing.assert_close(b, -logits.log_softmax(-1)[0, 2])


def test_context_and_successful_teacher_validation():
    with pytest.raises(ValueError, match="successful"):
        ExpertExample((), PublicEpisode(0, 0))
    with pytest.raises(ValueError, match="context exceeds"):
        public_tokens([(PublicEpisode(0, 0),) * 3], 2, torch.device("cpu"))
    with pytest.raises(TypeError, match="public episodes"):
        public_tokens([({"goal": 0},)], 2, torch.device("cpu"))
    with pytest.raises(ValueError, match="outside"):
        PublicEpisode(3, 0)


def test_diagnostic_performs_bounded_training_and_preserves_rng():
    state = torch.random.get_rng_state().clone()
    output = diagnostic(42)
    assert all(output["checks"].values()), output
    assert output["metrics"]["optimizer_steps"] == 54
    assert output["metrics"]["expert_query_count"] == 72
    assert not any("accuracy" in key or "success_rate" in key for key in output["metrics"])
    assert torch.equal(state, torch.random.get_rng_state())
