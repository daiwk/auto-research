from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class UniR2Config:
    dimensions: int = 40
    heads: int = 4
    maximum_history: int = 24
    codebook_size: int = 16
    sid_levels: int = 2
    lora_rank: int = 4
    steps: int = 130
    batch_size: int = 48
    learning_rate: float = 8e-4


def dual_query_masks(prefix: int, sid: int, ranking: int, torch, device=None):
    """Return paper Eq. 8 prefix-causal and ranking mutual-visibility masks."""
    generation = torch.zeros((sid, prefix + sid), dtype=torch.bool, device=device)
    for index in range(sid):
        generation[index, : prefix + index + 1] = True
    # Ranking reads compact user memory, the full generated SID trajectory and
    # all synchronously available ranking feature tokens.
    rank = torch.ones(
        (ranking, 1 + sid + ranking), dtype=torch.bool, device=device
    )
    return generation, rank


def build_model(data, semantic_ids, config: UniR2Config, *, unified: bool):
    import torch
    from torch import nn

    ids = torch.tensor(semantic_ids, dtype=torch.long)
    features = torch.tensor(data.features, dtype=torch.float32)

    class LowRank(nn.Module):
        def __init__(self):
            super().__init__()
            self.a = nn.Linear(config.dimensions, config.lora_rank, bias=False)
            self.b = nn.Linear(config.lora_rank, config.dimensions, bias=False)
            nn.init.zeros_(self.b.weight)

        def forward(self, values):
            return self.b(self.a(values))

    class DQAttention(nn.Module):
        def __init__(self):
            super().__init__()
            self.q = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.k = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.v = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.output = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.rank_q = LowRank()
            self.rank_k = LowRank()
            self.rank_v = LowRank()
            self.rank_output = LowRank()

        def attend(self, query, key, value, mask, *, project=True):
            batch, q_length, _ = query.shape
            k_length = key.shape[1]
            head_dim = config.dimensions // config.heads
            q = query.view(batch, q_length, config.heads, head_dim).transpose(1, 2)
            k = key.view(batch, k_length, config.heads, head_dim).transpose(1, 2)
            v = value.view(batch, k_length, config.heads, head_dim).transpose(1, 2)
            scores = q @ k.transpose(-1, -2) / math.sqrt(head_dim)
            scores = scores.masked_fill(~mask[None, None], -1e4)
            mixed = torch.softmax(scores, -1) @ v
            mixed = mixed.transpose(1, 2).reshape(
                batch, q_length, config.dimensions
            )
            return self.output(mixed) if project else mixed

        def generation(self, prefix, sid):
            values = torch.cat((prefix, sid), 1)
            mask, _ = dual_query_masks(
                prefix.shape[1], sid.shape[1], 1, torch, values.device
            )
            return self.attend(self.q(sid), self.k(values), self.v(values), mask)

        def ranking(self, compact_user, sid, rank_tokens):
            values = torch.cat((compact_user, sid, rank_tokens), 1)
            _, mask = dual_query_masks(
                1, sid.shape[1], rank_tokens.shape[1], torch, values.device
            )
            # sg(WX) + BA X: ranking losses update only the LoRA path.
            query = self.q(rank_tokens).detach() + self.rank_q(rank_tokens)
            key = self.k(values).detach() + self.rank_k(values)
            value = self.v(values).detach() + self.rank_v(values)
            mixed = self.attend(query, key, value, mask, project=False)
            return self.output(mixed).detach() + self.rank_output(mixed)

    class UniR2(nn.Module):
        def __init__(self):
            super().__init__()
            self.unified = unified
            self.register_buffer("semantic_ids", ids)
            self.register_buffer("features", features)
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.feature = nn.Linear(features.shape[1], config.dimensions, bias=False)
            self.sid = nn.ModuleList(
                [
                    nn.Embedding(config.codebook_size, config.dimensions)
                    for _ in range(config.sid_levels)
                ]
            )
            self.bos = nn.Parameter(torch.randn(1, 1, config.dimensions) * 0.02)
            self.position = nn.Embedding(config.maximum_history, config.dimensions)
            self.user_encoder = nn.GRU(
                config.dimensions, config.dimensions, batch_first=True
            )
            self.dq = DQAttention()
            self.generation_heads = nn.ModuleList(
                [
                    nn.Linear(config.dimensions, config.codebook_size)
                    for _ in range(config.sid_levels)
                ]
            )
            self.rank_tokens = nn.Parameter(
                torch.randn(2, config.dimensions) * 0.02
            )
            self.ranking_head = nn.Linear(2 * config.dimensions, 2)
            if not unified:
                self.separate_ranker = nn.Sequential(
                    nn.Linear(3 * config.dimensions, 2 * config.dimensions),
                    nn.GELU(),
                    nn.Linear(2 * config.dimensions, 2),
                )

        def item_values(self, items):
            return self.item(items) + self.feature(self.features[items])

        def user_states(self, histories):
            positions = torch.arange(histories.shape[1], device=histories.device)
            values = self.item_values(histories) + self.position(positions)
            states, _ = self.user_encoder(values)
            return states

        def forward(self, histories, candidates):
            states = self.user_states(histories)
            codes = self.semantic_ids[candidates]
            sid_inputs = [self.bos.expand(len(histories), -1, -1)]
            for level in range(config.sid_levels - 1):
                sid_inputs.append(self.sid[level](codes[:, level])[:, None])
            sid_inputs = torch.cat(sid_inputs, 1)
            if self.unified:
                generated = self.dq.generation(states, sid_inputs)
                gen_logits = [
                    head(generated[:, level])
                    for level, head in enumerate(self.generation_heads)
                ]
                trajectory = torch.stack(
                    [
                        self.sid[level](codes[:, level])
                        for level in range(config.sid_levels)
                    ],
                    1,
                )
                item = self.item_values(candidates)[:, None]
                rank_tokens = item + self.rank_tokens[None]
                ranked = self.dq.ranking(
                    states[:, -1:, :], trajectory, rank_tokens
                )
                rank_logits = self.ranking_head(ranked.reshape(len(histories), -1))
            else:
                # Conventional cascade: recall and ranking do not interact.
                compact = states[:, -1]
                gen_logits = [
                    head(compact) for head in self.generation_heads
                ]
                item = self.item_values(candidates)
                rank_logits = self.separate_ranker(
                    torch.cat((compact, item, compact * item), -1)
                )
            return gen_logits, rank_logits

    return UniR2()
