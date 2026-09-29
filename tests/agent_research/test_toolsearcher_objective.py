import pytest
import torch

from auto_research.agent_research.toolsearcher_credit import TraceCredit
from auto_research.agent_research.toolsearcher_objective import (
    IGNORED, SELECTION, grouped_policy_loss,
)


def test_retrieved_tokens_have_no_gradient_and_search_and_selection_do():
    logprobs = torch.tensor([[-1.0, -1.0, -1.0, -1.0]], requires_grad=True)
    old = logprobs.detach().clone()
    events = torch.tensor([[IGNORED, 0, IGNORED, SELECTION]])
    credit = TraceCredit((1.0,), 0.5, (frozenset({"target"}),))
    loss = grouped_policy_loss(logprobs, old, events, (credit,))
    loss.backward()
    assert logprobs.grad[0, 0] == 0
    assert logprobs.grad[0, 2] == 0
    assert logprobs.grad[0, 1] < 0
    assert logprobs.grad[0, 3] < 0


def test_clipping_saturates_positive_advantage():
    current = torch.tensor([[-0.1]], requires_grad=True)
    old = torch.tensor([[-2.0]])
    credit = TraceCredit((1.0,), 0.0, (frozenset({"target"}),))
    loss = grouped_policy_loss(current, old, torch.tensor([[0]]), (credit,))
    loss.backward()
    assert current.grad.item() == pytest.approx(0.0)


def test_invalid_event_and_missing_reference_are_rejected():
    current = torch.tensor([[-1.0]])
    credit = TraceCredit((1.0,), 0.0, (frozenset({"target"}),))
    with pytest.raises(ValueError, match="unknown search event"):
        grouped_policy_loss(current, current, torch.tensor([[1]]), (credit,))
    with pytest.raises(ValueError, match="reference policy"):
        grouped_policy_loss(current, current, torch.tensor([[0]]), (credit,), kl_weight=0.1)
