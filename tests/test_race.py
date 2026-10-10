import pytest
import torch

from auto_research.agent_research.race import TrainingTrajectory, Turn, cover_aware_loss, logic_cover


def test_logic_checks_all_future_actions_and_accepted_compressed_context():
    trajectory = TrainingTrajectory("task", tuple(Turn(f"r{i}", f"a{i}", f"o{i}") for i in range(4)), True)
    seen = []
    def likelihoods(candidate):
        removed = tuple(i for i, t in enumerate(candidate.turns) if not t.reasoning)
        seen.append(removed)
        # r1 is required for a3, although a1 itself has unchanged likelihood.
        return (-1., -1., -1., -1.01 if 1 in removed else -1.)
    compressed, skipped, audit = logic_cover(trajectory, likelihoods)
    assert skipped == (2, 3)
    assert seen == [(), (1,), (2,), (2, 3)]
    assert compressed.turns[0].reasoning and compressed.turns[1].reasoning
    assert not audit[0]["accepted"]
    with pytest.raises(ValueError):
        TrainingTrajectory("test", trajectory.turns, True, "test")


def test_masking_keeps_original_denominator_and_closure_scale():
    current = torch.zeros(2, 3, requires_grad=True)
    mask = torch.ones(2, 3, dtype=torch.bool)
    skipped = torch.tensor([[False, True, False], [False, False, False]])
    closure = torch.tensor([-2.], requires_grad=True)
    loss = cover_aware_loss(current, current.detach(), torch.ones(2), mask, skipped, closure, 4)
    assert float(loss.detach()) == pytest.approx(-5/6 + .01)
    loss.backward()
    assert current.grad[0, 1] == 0
    assert current.grad[1, 1] == pytest.approx(-1/6)
    assert float(closure.grad) == pytest.approx(-.02/4)
