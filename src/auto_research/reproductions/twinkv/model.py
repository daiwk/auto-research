"""TwinKV repair pass from arXiv:2608.27128.

The implementation evaluates Equation 4 only against the retained set.  This
is mathematically identical to materializing the full similarity matrix for a
repair pass, while reducing the temporary matrix from O(n²) to O(nK).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RepairDiagnostics:
    orphans: int
    donors: int
    swaps: int
    retained: int
    orphan_best_similarity_mean: float | None


def streaming_retained_indices(
    sequence_length: int,
    retained_tokens: int,
    *,
    sink_tokens: int = 4,
):
    """StreamingLLM-style sink + recent retained set."""
    import torch

    if not 0 < retained_tokens <= sequence_length:
        raise ValueError("retained_tokens must be in (0, sequence_length]")
    sink = min(sink_tokens, retained_tokens)
    recent = retained_tokens - sink
    leading = torch.arange(sink, dtype=torch.long)
    trailing = torch.arange(sequence_length - recent, sequence_length, dtype=torch.long)
    return torch.unique(torch.cat((leading, trailing)), sorted=True)


def repair_retained_indices(
    keys,
    retained,
    *,
    threshold: float = 0.85,
    local_window: int = 32,
    sink_tokens: int = 4,
    recent_tokens: int = 64,
):
    """Repair one head's retained set without changing its token budget."""
    import torch

    if keys.ndim != 2:
        raise ValueError("keys must have shape [sequence, head_dimension]")
    sequence_length = len(keys)
    retained = torch.unique(retained.to(device=keys.device, dtype=torch.long), sorted=True)
    if len(retained) == 0 or int(retained.min()) < 0 or int(retained.max()) >= sequence_length:
        raise ValueError("retained indices are empty or out of range")
    normalized = torch.nn.functional.normalize(keys.float(), dim=-1, eps=1e-12)
    similarity = normalized @ normalized[retained].T
    positions = torch.arange(sequence_length, device=keys.device)
    allowed = (positions[:, None] - retained[None, :]).abs() > local_window
    similarity = similarity.masked_fill(~allowed, -1.0)
    best = similarity.max(dim=1).values
    is_retained = torch.zeros(sequence_length, dtype=torch.bool, device=keys.device)
    is_retained[retained] = True
    protected = torch.zeros_like(is_retained)
    protected[: min(sink_tokens, sequence_length)] = True
    protected[max(0, sequence_length - recent_tokens):] = True
    orphan_indices = torch.where(~is_retained & (best < threshold))[0]
    donor_indices = torch.where(is_retained & ~protected & (best >= threshold))[0]
    orphan_order = orphan_indices[torch.argsort(best[orphan_indices])]
    donor_order = donor_indices[torch.argsort(best[donor_indices], descending=True)]
    swaps = min(len(orphan_order), len(donor_order))
    repaired_mask = is_retained.clone()
    if swaps:
        repaired_mask[donor_order[:swaps]] = False
        repaired_mask[orphan_order[:swaps]] = True
    repaired = torch.where(repaired_mask)[0]
    if len(repaired) != len(retained):
        raise AssertionError("TwinKV changed the wrapped policy budget")
    orphan_mean = (
        float(best[orphan_indices].mean().cpu()) if len(orphan_indices) else None
    )
    return repaired, RepairDiagnostics(
        orphans=len(orphan_indices),
        donors=len(donor_indices),
        swaps=swaps,
        retained=len(repaired),
        orphan_best_similarity_mean=orphan_mean,
    )
