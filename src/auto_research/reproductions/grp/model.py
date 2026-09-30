"""Public GRP mechanisms: independent item blocks, detached ranker and mGRPO."""

from __future__ import annotations


def block_causal_mask(items: int, codes_per_item: int, *, device=None):
    """Causal inside each SID block and fully masked across candidate items."""
    import torch

    if items < 1 or codes_per_item < 1:
        raise ValueError("items and codes_per_item must be positive")
    length = items * codes_per_item
    mask = torch.ones(length, length, dtype=torch.bool, device=device)
    for item in range(items):
        start = item * codes_per_item
        mask[start:start + codes_per_item, start:start + codes_per_item] = torch.triu(
            torch.ones(codes_per_item, codes_per_item, dtype=torch.bool, device=device), diagonal=1,
        )
    return mask


def m_grpo_loss(policy_log_prob, old_log_prob, reference_log_prob, rewards, logged_target_log_prob, *, clip: float = 0.2, margin: float = 0.0, protection_weight: float = 1.0):
    """GRP mGRPO: clipped group-relative surrogate plus one-sided recall guard."""
    import torch

    if not (policy_log_prob.shape == old_log_prob.shape == reference_log_prob.shape == rewards.shape):
        raise ValueError("sample-level tensors must match")
    advantage = (rewards - rewards.mean()) / rewards.std(unbiased=False).clamp_min(1e-6)
    ratio = (policy_log_prob - old_log_prob.detach()).exp()
    surrogate = torch.minimum(ratio * advantage, ratio.clamp(1 - clip, 1 + clip) * advantage)
    policy_loss = -surrogate.mean()
    # Activate only when a sampled high-reward candidate is gaining relative to
    # the logged target beyond the frozen-reference relation.
    drift = (policy_log_prob - logged_target_log_prob) - (reference_log_prob - logged_target_log_prob.detach())
    guard = torch.relu(drift - margin).mean()
    return policy_loss + protection_weight * guard, {"policy_loss": float(policy_loss.detach()), "recall_guard": float(guard.detach())}


class GRPHeads:
    """Small encoder/decoder/ranker reference preserving GRP gradient boundaries."""

    def __new__(cls, hidden_size: int, vocab_size: int, heads: int = 2):
        import torch
        import torch.nn as nn

        class _Model(nn.Module):
            def __init__(self):
                super().__init__()
                self.encoder = nn.TransformerEncoderLayer(hidden_size, heads, 2 * hidden_size, batch_first=True)
                self.decoder = nn.TransformerDecoderLayer(hidden_size, heads, 2 * hidden_size, batch_first=True)
                self.sid_head = nn.Linear(hidden_size, vocab_size)
                self.candidate = nn.Linear(hidden_size, hidden_size)
                self.ranker = nn.Sequential(nn.Linear(2 * hidden_size, hidden_size), nn.ReLU(), nn.Linear(hidden_size, 2))

            def forward(self, history, targets, candidates, *, items: int, codes_per_item: int):
                encoded = self.encoder(history)
                mask = block_causal_mask(items, codes_per_item, device=targets.device)
                decoded = self.decoder(targets, encoded, tgt_mask=mask)
                generation = self.sid_head(decoded)
                history_summary = encoded.detach().mean(1)
                candidate_hidden = self.candidate(candidates.detach())
                repeated = history_summary[:, None, :].expand_as(candidate_hidden)
                rank_scores = self.ranker(torch.cat((repeated, candidate_hidden), -1))
                return generation, rank_scores

        return _Model()
