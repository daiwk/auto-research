"""PAIR exposed-preference objective and positional history, not its 0.6B encoder.

Independent Eq.1–6 component implementation; inputs are external embeddings.
No production data, reference policy, full encoder training or capability claim.
"""
from __future__ import annotations

import random
import torch
from torch import nn
from torch.nn import functional as F


def exposure_negatives(clicked, exposed, member_pool, *, seed=42, count=3):
    """Prioritize unclicked impressions; fill distinct slots outside exposure."""
    if not isinstance(count, int) or count < 1:
        raise ValueError('positive negative count required')
    hard = list(dict.fromkeys(x for x in exposed if x != clicked))
    rng = random.Random(seed)
    rng.shuffle(hard)
    result = hard[:count]
    excluded = set(exposed) | {clicked}
    easy = list(dict.fromkeys(x for x in member_pool if x not in excluded))
    rng.shuffle(easy)
    result += easy[:count-len(result)]
    if len(result) != count:
        raise ValueError('insufficient distinct non-positive negatives')
    return tuple(result)


class PositionalHistory(nn.Module):
    """Query-agnostic attention; slot zero is the most recent clicked profile."""
    def __init__(self, dim, window=10):
        super().__init__()
        if dim < 1 or window < 1:
            raise ValueError('positive dimensions/window required')
        self.position = nn.Parameter(torch.zeros(window, dim))
        self.attention = nn.Parameter(torch.empty(dim))
        nn.init.normal_(self.attention, std=.1)
        self.gamma = nn.Parameter(torch.tensor(1.))

    def forward(self, profile, history, mask):
        if (profile.ndim != 2 or history.ndim != 3 or history.shape[0] != profile.shape[0] or
                history.shape[2] != profile.shape[1] or history.shape[1] > len(self.position) or
                mask.shape != history.shape[:2] or mask.dtype != torch.bool or not mask.any(dim=1).all()):
            raise ValueError('aligned finite embeddings and nonempty boolean history masks required')
        if not torch.isfinite(profile).all() or not torch.isfinite(history).all():
            raise ValueError('nonfinite embeddings')
        scores = ((history+self.position[:history.shape[1]])*self.attention).sum(-1)
        weights = scores.masked_fill(~mask, -torch.inf).softmax(-1)
        intent = (weights.unsqueeze(-1)*history).sum(1)
        fused = F.normalize(F.normalize(profile, dim=-1)+self.gamma*F.normalize(intent, dim=-1), dim=-1)
        return fused, weights


def preference_loss(query, candidates, *, temperature=.02, dimensions=None):
    """Each row has one clicked candidate at slot0, followed by real negatives.

    Matryoshka is a SUM over requested prefix losses, not their mean. Caller
    owns data construction and temporal splitting, no target is read here.
    """
    if (query.ndim != 2 or candidates.ndim != 3 or candidates.shape[0] != query.shape[0] or
            candidates.shape[2] != query.shape[1] or candidates.shape[1] < 2 or
            not 0 < temperature < float('inf') or not torch.isfinite(query).all() or not torch.isfinite(candidates).all()):
        raise ValueError('finite query/positive+negative candidates and temperature required')
    dims = (query.shape[-1],) if dimensions is None else tuple(dimensions)
    if not dims or len(set(dims)) != len(dims) or any(type(d) is not int or not 1 <= d <= query.shape[-1] for d in dims):
        raise ValueError('distinct valid prefix dimensions required')
    losses = []
    for d in dims:
        score = torch.einsum('bd,bnd->bn', F.normalize(query[:, :d], dim=-1),
                             F.normalize(candidates[:, :, :d], dim=-1))/temperature
        losses.append((-score[:, 0]+torch.logsumexp(score, dim=-1)).mean())
    return torch.stack(losses).sum()


def diagnostic(seed=42, device='cpu'):
    torch.manual_seed(seed)
    dtype = torch.float64
    model = PositionalHistory(8, 4).to(device=device, dtype=dtype)
    profile = torch.randn(3, 8, device=device, dtype=dtype)
    history = torch.randn(3, 4, 8, device=device, dtype=dtype)
    mask = torch.tensor([[1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 1, 1]], dtype=torch.bool, device=device)
    candidates = torch.randn(3, 4, 8, device=device, dtype=dtype)
    optimizer = torch.optim.SGD(model.parameters(), lr=.01)
    initial = torch.cat([p.detach().flatten() for p in model.parameters()]).clone()
    max_reference_error = 0.
    for _ in range(3):
        optimizer.zero_grad()
        query, weights = model(profile, history, mask)
        loss = preference_loss(query, candidates, temperature=.2, dimensions=[4, 8])
        reference = torch.stack([F.cross_entropy(torch.stack([
            torch.stack([F.cosine_similarity(query[b, :d], c[:d], dim=0)/.2 for c in candidates[b]])
            for b in range(3)]), torch.zeros(3, dtype=torch.long, device=device)) for d in (4, 8)]).sum()
        max_reference_error = max(max_reference_error, float((loss-reference).abs().detach()))
        loss.backward()
        optimizer.step()
    final = torch.cat([p.detach().flatten() for p in model.parameters()])
    query, weights = model(profile, history, mask)
    changed_history = history.clone()
    changed_history[~mask] = 1e6
    masked_query, _ = model(profile, changed_history, mask)
    no_history = F.normalize(profile, dim=-1)
    hard = exposure_negatives('clicked', ['clicked', 'h1', 'h2'], ['easy', 'h1', 'clicked'])
    loss = preference_loss(query, candidates, temperature=.2, dimensions=[4, 8])
    return {'seed': seed, 'metrics': {'formula_reference_error': max_reference_error,
        'optimizer_updates': 3, 'parameter_update_l2': float((final-initial).norm()),
        'masked_history_error': float((query-masked_query).abs().max().detach()),
        'history_effect_l2': float((query-no_history).norm().detach()),
        'final_loss': float(loss.detach()), 'model_calls': 0},
        'checks': {'independent_loss_reference': max_reference_error < 1e-10,
            'three_real_updates': bool((final-initial).norm() > 0),
            'masked_history_isolated': bool(torch.equal(query, masked_query)),
            'hard_negatives_first': set(hard[:2]) == {'h1', 'h2'} and hard[2] == 'easy',
            'history_changes_representation': bool((query-no_history).norm() > 0),
            'finite_gradients': all(p.grad is not None and torch.isfinite(p.grad).all().item() for p in model.parameters()),
            'query_agnostic_normalized_attention': bool(torch.allclose(weights.sum(-1), torch.ones(3, device=device, dtype=dtype)))}}
