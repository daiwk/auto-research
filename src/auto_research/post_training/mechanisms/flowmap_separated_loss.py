"""Extracted unchanged from auto_research.post_training.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def flowmap_separated_loss(sampled_states, student_kernel, teacher_kernel):
    """FlowMap-OPD: rollout states are detached from the comparison kernel."""
    import torch
    import torch.nn.functional as F

    states = sampled_states.detach()
    student_logp = torch.log_softmax(student_kernel(states), dim=-1)
    with torch.no_grad():
        teacher_prob = torch.softmax(teacher_kernel(states), dim=-1)
    return F.kl_div(student_logp, teacher_prob, reduction="batchmean"), states
