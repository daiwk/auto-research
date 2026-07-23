from __future__ import annotations

import math

from ..industrial_ranking import require_backend
from ..july_2026_common import item_feature_tensor


def build_tmallgs(data, config):
    torch, nn = require_backend()

    class FieldAdaptiveBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.q = nn.Parameter(torch.empty(3, config.dimensions, config.dimensions))
            self.k = nn.Parameter(torch.empty(3, config.dimensions, config.dimensions))
            self.v = nn.Parameter(torch.empty(3, config.dimensions, config.dimensions))
            nn.init.xavier_uniform_(self.q)
            nn.init.xavier_uniform_(self.k)
            nn.init.xavier_uniform_(self.v)
            self.noise_gate = nn.Sequential(nn.Linear(config.dimensions, 1), nn.Sigmoid())
            self.ffn = nn.Sequential(
                nn.LayerNorm(config.dimensions),
                nn.Linear(config.dimensions, 3 * config.dimensions),
                nn.SiLU(),
                nn.Linear(3 * config.dimensions, config.dimensions),
            )
            self.norm = nn.LayerNorm(config.dimensions)

        def forward(self, tokens, fields):
            q = torch.einsum("bld,ldh->blh", tokens, self.q[fields])
            k = torch.einsum("bld,ldh->blh", tokens, self.k[fields])
            v = torch.einsum("bld,ldh->blh", tokens, self.v[fields])
            scores = q @ k.transpose(1, 2) / math.sqrt(config.dimensions)
            attention = torch.softmax(scores, dim=-1)
            update = attention @ v
            gate = self.noise_gate(tokens)
            values = self.norm(tokens + gate * update)
            return values + self.ffn(values), gate

    class TMallGS(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.position = nn.Embedding(config.sequence_length + 1, config.dimensions)
            self.anchor = nn.Parameter(torch.zeros(config.dimensions))
            self.content = nn.Parameter(
                item_feature_tensor(data, config.dimensions, torch), requires_grad=False
            )
            self.saliency = nn.Sequential(
                nn.Linear(config.dimensions, config.dimensions), nn.Sigmoid()
            )
            self.blocks = nn.ModuleList([FieldAdaptiveBlock() for _ in range(config.layers)])
            self.film = nn.Linear(2 * config.dimensions, 2 * config.dimensions)
            self.main = nn.LayerNorm(config.dimensions)
            self.bias_context = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.bias_item = nn.Linear(config.dimensions, config.dimensions, bias=False)

        def forward(self, histories, **_):
            batch, length = histories.shape
            history = self.item(histories) + self.content[histories]
            history = history * (1.0 + self.saliency(history))
            anchor = self.anchor[None, None].expand(batch, 1, -1)
            tokens = torch.cat([anchor, history], dim=1)
            tokens = tokens + self.position(torch.arange(length + 1, device=histories.device))
            split = 1 + length // 2
            fields = torch.cat([
                torch.zeros(1, dtype=torch.long, device=histories.device),
                torch.ones(split - 1, dtype=torch.long, device=histories.device),
                torch.full((length - split + 1,), 2, dtype=torch.long, device=histories.device),
            ])
            auxiliary, gates = [], []
            for block in self.blocks:
                tokens, gate = block(tokens, fields)
                gates.append(gate.mean())
                auxiliary.append(self.main(tokens[:, 0]) @ self.item.weight.T)
            context = self.main(tokens[:, 0])
            explicit = self.content[histories[:, -1]]
            scale, shift = self.film(torch.cat([context, explicit], dim=-1)).chunk(2, dim=-1)
            catalog = self.item.weight + self.content
            modulated = context * (1.0 + torch.tanh(scale)) + shift
            main_logits = modulated @ catalog.T
            bias = self.bias_context(context) @ self.bias_item(self.content).T
            return {
                "logits": main_logits + 0.1 * bias,
                "auxiliary_logits": auxiliary,
                "mean_noise_gate": torch.stack(gates).mean(),
            }

    return TMallGS()


def progressive_loss(model, extras, logits, targets, histories, users, step, torch):
    main = torch.nn.functional.cross_entropy(logits, targets)
    auxiliary = [
        torch.nn.functional.cross_entropy(values, targets)
        for values in extras["auxiliary_logits"]
    ]
    if auxiliary:
        errors = torch.stack([value.detach() for value in auxiliary])
        weights = torch.softmax(errors, dim=0)
        progressive = sum(weight * value for weight, value in zip(weights, auxiliary))
    else:
        progressive = main.new_zeros(())
    loss = main + 0.25 * progressive
    return loss, {"main": main, "error_aware_progressive": progressive}
