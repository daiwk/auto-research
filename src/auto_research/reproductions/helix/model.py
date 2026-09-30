"""Candidate-independent cache and mix-token interaction from HELIX."""

from __future__ import annotations


def mixup_channels(tokens):
    """HELIX Eq. (10): every output token receives one slice from every input."""
    if tokens.ndim != 3:
        raise ValueError("tokens must be [batch, mix tokens, hidden]")
    batch, count, hidden = tokens.shape
    if hidden % count:
        raise ValueError("hidden dimension must be divisible by mix-token count")
    width = hidden // count
    return tokens.reshape(batch, count, count, width).transpose(1, 2).reshape(batch, count, hidden)


class HELIXCore:
    """Compact executable HELIX block with one-way user-to-candidate flow."""

    def __new__(cls, hidden_size: int, mix_tokens: int = 4, heads: int = 4):
        import torch
        import torch.nn as nn

        if hidden_size % mix_tokens or hidden_size % heads:
            raise ValueError("hidden size must divide mix tokens and attention heads")

        class _Model(nn.Module):
            def __init__(self):
                super().__init__()
                self.mix_tokens = mix_tokens
                self.user_encoder = nn.TransformerEncoderLayer(hidden_size, heads, 2 * hidden_size, batch_first=True)
                self.candidate_retrieval = nn.MultiheadAttention(hidden_size, heads, batch_first=True)
                self.user_retrieval = nn.MultiheadAttention(hidden_size, heads, batch_first=True)
                self.norm_candidate = nn.LayerNorm(hidden_size)
                self.norm_user = nn.LayerNorm(hidden_size)
                self.gate = nn.Linear(hidden_size, hidden_size)
                self.up = nn.ModuleList(nn.Linear(hidden_size, 2 * hidden_size) for _ in range(mix_tokens))
                self.down = nn.ModuleList(nn.Linear(hidden_size, hidden_size) for _ in range(mix_tokens))
                self.output = nn.Linear(hidden_size, 1)

            def encode_user(self, user_sequence):
                """Reusable U-only cache; no candidate tensor enters this method."""
                return self.user_encoder(user_sequence)

            def _mptf(self, tokens):
                mixed = mixup_channels(tokens)
                return torch.stack([
                    down(torch.nn.functional.silu(parts[..., :hidden_size]) * parts[..., hidden_size:])
                    for parts, down in zip(
                        (up(mixed[:, index]) for index, up in enumerate(self.up)), self.down
                    )
                ], dim=1)

            def forward(self, mix, candidate_sequence, *, user_cache):
                candidate_update, _ = self.candidate_retrieval(
                    self.norm_candidate(mix), candidate_sequence, candidate_sequence
                )
                mix = mix + torch.sigmoid(self.gate(candidate_update)) * candidate_update
                mix = mix + self._mptf(mix)
                user_update, _ = self.user_retrieval(self.norm_user(mix), user_cache, user_cache)
                mix = mix + torch.sigmoid(self.gate(user_update)) * user_update
                mix = mix + self._mptf(mix)
                return self.output(mix.mean(dim=1)).squeeze(-1), mix

        return _Model()
