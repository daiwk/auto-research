"""Extracted unchanged from auto_research.agent_research.latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def multi_memory_grpo_objective(
    final_ratio,
    memory_ratio,
    rewards,
    *,
    clip: float = 0.2,
    memory_weight: float = 1.0,
    epsilon: float = 1e-6,
):
    """ReMem Eqs. (11), (14)-(16): propagate final reward to every memory."""
    import torch

    if final_ratio.ndim != 2 or memory_ratio.ndim != 3:
        raise ValueError("final ratios are [group,tokens], memory ratios [group,memories,tokens]")
    if final_ratio.shape[0] != memory_ratio.shape[0] or rewards.shape != final_ratio.shape[:1]:
        raise ValueError("all tensors must share the rollout group dimension")
    advantage = (rewards - rewards.mean()) / rewards.std(unbiased=False).clamp_min(epsilon)

    def surrogate(ratio, expanded_advantage):
        unclipped = ratio * expanded_advantage
        clipped = ratio.clamp(1 - clip, 1 + clip) * expanded_advantage
        return torch.minimum(unclipped, clipped).mean()

    answer = surrogate(final_ratio, advantage[:, None])
    memory = surrogate(memory_ratio, advantage[:, None, None])
    return answer + memory_weight * memory, {
        "answer_objective": float(answer.detach()),
        "memory_objective": float(memory.detach()),
        "memory_count": memory_ratio.shape[1],
    }
