"""CoLiR v1: cached cross-policy likelihood selection, not a VLM trainer."""

import random

import torch

from ._nov18_contracts import receipt, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def _boolean(value, shape, device):
    if (not isinstance(value, torch.Tensor) or value.dtype != torch.bool
            or value.shape != shape or value.device != device):
        raise ValueError("same-device Boolean correctness/mask required")


def contrastive_scores(initial_under_initial, initial_under_final,
                       final_under_initial, final_under_final,
                       initial_correct, final_correct):
    """Eq.15 on two distinct response sets; generating and cross-policy scores.

    Log likelihoods are complete-response log probabilities supplied by the
    caller. They are NOT token means, correctness logits, or fresh responses.
    Ineligible rows get neutral zero plus a separate false eligibility bit.
    """
    tensor(initial_under_initial, "initial_under_initial", ndim=2)
    device = initial_under_initial.device
    tensor(initial_under_final, "initial_under_final", shape=initial_under_initial.shape, device=device)
    tensor(final_under_initial, "final_under_initial", ndim=2, device=device)
    tensor(final_under_final, "final_under_final", shape=final_under_initial.shape, device=device)
    if initial_under_initial.shape[0] != final_under_initial.shape[0]:
        raise ValueError("matching prompt rows required; response sets may have different sizes")
    _boolean(initial_correct, initial_under_initial.shape, device)
    _boolean(final_correct, final_under_initial.shape, device)
    initial_negative = ~initial_correct
    final_positive = final_correct
    eligible = initial_negative.any(-1) & final_positive.any(-1) & (~final_correct).any(-1)
    positive_gain = (final_under_final-final_under_initial).detach()
    negative_suppression = (initial_under_initial-initial_under_final).detach()
    p1 = torch.where(final_positive, positive_gain, 0.).sum(-1)/final_positive.sum(-1).clamp(min=1)
    p2 = torch.where(initial_negative, negative_suppression, 0.).sum(-1)/initial_negative.sum(-1).clamp(min=1)
    return torch.where(eligible, .5*(p1+p2), 0.), eligible


def select_task_memory(prompt_ids, scores, eligible, *, budget=80):
    """Per-task top B eligible prompts; stable input order resolves exact ties."""
    tensor(scores, "scores", ndim=1)
    _boolean(eligible, scores.shape, scores.device)
    if (not isinstance(prompt_ids, (tuple, list)) or len(prompt_ids) != len(scores)
            or any(not isinstance(x, str) or not x for x in prompt_ids)
            or len(set(prompt_ids)) != len(prompt_ids)):
        raise ValueError("unique nonempty prompt identities required")
    if type(budget) is not int or budget < 0:
        raise ValueError("nonnegative integer per-task memory budget required")
    indices = [i for i, bit in enumerate(eligible.tolist()) if bit]
    indices.sort(key=lambda i: (-scores[i].item(), i))
    return tuple(prompt_ids[i] for i in indices[:budget])


def sample_replay(prompt_ids, count, seed):
    """Uniform sampling without replacement for this bounded component batch.

    The paper specifies uniform prompt replay, not this batch's replacement or
    tie policy. The caller owns task scheduling and current-policy rollouts.
    """
    if (not isinstance(prompt_ids, (tuple, list)) or len(set(prompt_ids)) != len(prompt_ids)
            or any(not isinstance(x, str) or not x for x in prompt_ids)
            or type(count) is not int or not 0 <= count <= len(prompt_ids)
            or type(seed) is not int):
        raise ValueError("unique IDs, valid count and integer seed required")
    return tuple(random.Random(seed).sample(list(prompt_ids), count))


def gate_replay_kl(per_token_kl, replay_rows, response_mask):
    """Restrict supplied KL values to replay; leave trainer reduction explicit."""
    tensor(per_token_kl, "per_token_kl", ndim=2)
    _boolean(replay_rows, (per_token_kl.shape[0],), per_token_kl.device)
    _boolean(response_mask, per_token_kl.shape, per_token_kl.device)
    return torch.where(replay_rows[:, None] & response_mask, per_token_kl, 0.)


def sample_historical_tasks(task_memories, count, seed):
    """Uniform active task, then uniform retained prompt; replacement is explicit.

    Unlike flattening unequal per-task buffers, this preserves the paper's
    task-uniform allocation. Replacement is this component's batching policy;
    it is not specified by the paper and is not a reproduced trainer.
    """
    if (not isinstance(task_memories, dict) or type(count) is not int or count < 0
            or type(seed) is not int):
        raise ValueError("task mapping, nonnegative count and integer seed required")
    for task, prompts in task_memories.items():
        if (not isinstance(task, str) or not task or not isinstance(prompts, (tuple, list))
                or len(set(prompts)) != len(prompts)
                or any(not isinstance(x, str) or not x for x in prompts)):
            raise ValueError("task IDs and unique per-task prompt IDs required")
    tasks = sorted(task for task, prompts in task_memories.items() if prompts)
    if not tasks and count:
        raise ValueError("no eligible historical prompt to replay")
    rng = random.Random(seed)
    result = []
    for _ in range(count):
        task = rng.choice(tasks)
        result.append((task, rng.choice(task_memories[task])))
    return tuple(result)


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    a = -torch.rand(5, 4, generator=g, dtype=torch.float64).to(device)-4
    b = a-torch.tensor([.2, .4, .1, .8, .3], device=device)[:, None]
    c = -torch.rand(5, 3, generator=g, dtype=torch.float64).to(device)-5
    d = c+torch.tensor([.8, .1, .3, .2, .1], device=device)[:, None]
    initial_ok = torch.tensor([[0, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1],
                               [0, 0, 0, 0], [0, 1, 0, 1]], dtype=torch.bool, device=device)
    final_ok = torch.tensor([[1, 0, 0], [1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 0]],
                           dtype=torch.bool, device=device)
    scores, eligible = contrastive_scores(a, b, c, d, initial_ok, final_ok)
    memory = select_task_memory(["a", "b", "c", "d", "e"], scores, eligible, budget=80)
    kl = torch.rand(2, 3, generator=g, dtype=torch.float64).to(device).requires_grad_()
    replay = torch.tensor([True, False], device=device)
    mask = torch.tensor([[True, False, True], [True, True, True]], device=device)
    gated = gate_replay_kl(kl, replay, mask)
    gated.sum().backward()
    return receipt(seed, "l1_mechanism", {
        "exact_contrastive_score": torch.allclose(scores[:2], torch.tensor([.5, .25], device=device, dtype=scores.dtype)),
        "mixed_final_and_initial_negative_required": eligible.tolist() == [True, True, False, False, False],
        "selection_preserves_only_eligible_prompt_ids": memory == ("a", "b"),
        "no_silent_padding_of_memory": len(memory) == 2,
        "uniform_sampler_stays_in_memory": set(sample_replay(memory, 2, seed)) == set(memory),
        "new_task_and_masked_kl_gradient_zero": bool((kl.grad[1] == 0).all()) and kl.grad[0, 1].item() == 0,
        "replay_valid_kl_gradient_present": kl.grad[0, 0].item() == 1,
        "selection_has_no_autograd": not scores.requires_grad,
    }, {"selected_prompts": len(memory), "eligible_prompts": eligible.sum().item(),
        "highest_score": scores.max().item(), "replay_kl_sum": gated.sum().item()})
