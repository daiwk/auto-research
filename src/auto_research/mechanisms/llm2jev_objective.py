"""Extracted unchanged from auto_research.foundation_latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def llm2jev_objective(decision_logits, target, auxiliary_logits, base_logits, *, kl_weight: float):
    """Listwise decision loss with the paper's base-model KL anchor."""
    import torch.nn.functional as F

    listwise = F.cross_entropy(decision_logits[None], target.reshape(1))
    base = F.softmax(base_logits.detach(), dim=-1)
    anchor = F.kl_div(F.log_softmax(auxiliary_logits, dim=-1), base, reduction="batchmean")
    return listwise + kl_weight * anchor
