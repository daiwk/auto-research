"""Signal-free, prompt-protected KV eviction from arXiv:2609.03430."""

from __future__ import annotations


def random_retained_indices(
    sequence_length: int,
    retained_tokens: int,
    *,
    prompt_tokens: int,
    heads: int,
    seed: int = 42,
    device=None,
):
    """Return an independent equal-budget retained set for every KV head.

    The full prompt is immutable.  Generated positions receive iid uniform
    scores per head, exactly implementing the paper's defining policy.
    """
    import torch

    if not 0 <= prompt_tokens <= retained_tokens <= sequence_length:
        raise ValueError("require 0 <= prompt_tokens <= retained_tokens <= sequence_length")
    if heads < 1:
        raise ValueError("heads must be positive")
    device = device or torch.device("cpu")
    protected = torch.arange(prompt_tokens, device=device)
    generated = torch.arange(prompt_tokens, sequence_length, device=device)
    random_budget = retained_tokens - prompt_tokens
    generator = torch.Generator(device=device).manual_seed(seed)
    rows = []
    for _ in range(heads):
        if random_budget:
            scores = torch.rand(len(generated), generator=generator, device=device)
            sampled = generated[torch.topk(scores, random_budget, sorted=False).indices]
            rows.append(torch.sort(torch.cat((protected, sampled))).values)
        else:
            rows.append(protected)
    return torch.stack(rows)


def recent_retained_indices(
    sequence_length: int,
    retained_tokens: int,
    *,
    prompt_tokens: int,
    heads: int,
    device=None,
):
    """Equal-budget prompt + most-recent baseline."""
    import torch

    if not 0 <= prompt_tokens <= retained_tokens <= sequence_length:
        raise ValueError("invalid retention budget")
    device = device or torch.device("cpu")
    protected = torch.arange(prompt_tokens, device=device)
    recent = torch.arange(
        sequence_length - (retained_tokens - prompt_tokens), sequence_length, device=device
    )
    row = torch.unique(torch.cat((protected, recent)), sorted=True)
    return row.expand(heads, -1).clone()
