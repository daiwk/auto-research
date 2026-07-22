from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class SlimPerConfig:
    item_count: int
    dimensions: int = 32
    maximum_length: int = 32
    layers: int = 3
    baseline_layers: int = 6
    knowledge_slots: int = 8
    query_slots: int = 4
    template_slots: int = 8


def build_models(config: SlimPerConfig, feature_matrix: np.ndarray, torch):
    nn = torch.nn; d = config.dimensions
    features = torch.tensor(feature_matrix, dtype=torch.float32)

    class Tokenizer(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(config.item_count + 1, d, padding_idx=config.item_count)
            self.content = nn.Linear(features.shape[1], d, bias=False)
            self.register_buffer("features", features)

        def forward(self, ids):
            safe = ids.clamp_max(config.item_count - 1)
            content = self.content(self.features[safe])
            mask = (ids < config.item_count).unsqueeze(-1)
            return (self.item(ids) + content) * mask

    class SequenceBaseline(nn.Module):
        """Matched discriminative full-sequence Transformer baseline."""
        def __init__(self):
            super().__init__(); self.tokens = Tokenizer()
            layer = nn.TransformerEncoderLayer(d, 4, 8 * d, batch_first=True, norm_first=True)
            self.encoder = nn.TransformerEncoder(layer, config.baseline_layers)
            self.output = nn.Linear(d, 1)

        def forward(self, history, candidate):
            values = torch.cat((self.tokens(history), self.tokens(candidate[:, None])), 1)
            padding = torch.cat((history == config.item_count, torch.zeros((len(history), 1), dtype=torch.bool, device=history.device)), 1)
            return self.output(self.encoder(values, src_key_padding_mask=padding)[:, -1]).squeeze(-1)

    class SlimPerLayer(nn.Module):
        def __init__(self):
            super().__init__()
            self.query_projection = nn.Parameter(torch.randn(config.query_slots, config.knowledge_slots) * 0.02)
            self.template_projection = nn.Parameter(torch.randn(config.template_slots, config.knowledge_slots) * 0.02)
            self.match_norm = nn.RMSNorm(config.query_slots * config.template_slots)
            self.knowledge_norm = nn.RMSNorm(config.knowledge_slots * d)
            width = config.query_slots * config.template_slots + config.knowledge_slots * d + d
            self.refine = nn.Sequential(nn.Linear(width, 2 * d), nn.SiLU(), nn.Linear(2 * d, config.knowledge_slots * d))
            self.task = nn.Sequential(nn.Linear(d, d), nn.SiLU(), nn.Linear(d, 1))

        def forward(self, knowledge, user_tokens, user_dense, padding):
            query = torch.einsum("qk,bkd->bqd", self.query_projection, knowledge)
            weights = torch.einsum("bqd,bnd->bqn", query, user_tokens) / query.shape[-1] ** 0.5
            weights = weights.masked_fill(padding[:, None], -1e4).softmax(-1)
            selected = torch.einsum("bqn,bnd->bqd", weights, user_tokens)
            template = torch.einsum("tk,bkd->btd", self.template_projection, knowledge)
            relevance = torch.einsum("bqd,btd->bqt", selected, template)
            merged = torch.cat((
                self.match_norm(relevance.flatten(1)),
                self.knowledge_norm(knowledge.flatten(1)),
                user_dense,
            ), -1)
            knowledge = knowledge + self.refine(merged).view_as(knowledge)
            return knowledge, self.task(knowledge.mean(1)).squeeze(-1), weights

    class SlimPer(nn.Module):
        def __init__(self):
            super().__init__(); self.tokens = Tokenizer()
            self.slot = nn.Parameter(torch.randn(config.knowledge_slots, d) * 0.02)
            self.initialize = nn.Linear(2 * d, config.knowledge_slots * d)
            self.layers = nn.ModuleList(SlimPerLayer() for _ in range(config.layers))
            self.last_attention = None

        def encode_request(self, history):
            # This is called once per request and shared by all candidates (ROO).
            user_tokens = self.tokens(history)
            mask = (history < config.item_count).float().unsqueeze(-1)
            dense = (user_tokens * mask).sum(1) / mask.sum(1).clamp_min(1)
            return user_tokens, dense, history == config.item_count

        def forward_encoded(self, encoded, candidate):
            user_tokens, user_dense, padding = encoded
            item = self.tokens(candidate[:, None]).squeeze(1)
            initial = self.initialize(torch.cat((user_dense, item), -1)).view(-1, config.knowledge_slots, d)
            knowledge = initial + self.slot[None]
            logits = 0.0
            for layer in self.layers:
                knowledge, task, attention = layer(knowledge, user_tokens, user_dense, padding)
                logits = logits + task
            self.last_attention = attention.detach()
            return logits

        def forward(self, history, candidate):
            return self.forward_encoded(self.encode_request(history), candidate)

    return SequenceBaseline(), SlimPer()


def training_rows(data, seed: int, maximum_length: int):
    rng = np.random.default_rng(seed); histories, candidates, labels = [], [], []
    pad = data.item_count
    for sequence in data.train:
        for end in range(2, len(sequence)):
            history = list(sequence[max(0, end - maximum_length):end])
            history = [pad] * (maximum_length - len(history)) + history
            positive = sequence[end]
            pool = [item for item in range(data.item_count) if item not in set(sequence[:end + 1])]
            negative = int(rng.choice(pool))
            histories.extend((history, history)); candidates.extend((positive, negative)); labels.extend((1.0, 0.0))
    return np.asarray(histories), np.asarray(candidates), np.asarray(labels, dtype=np.float32)


def train(model, data, config: SlimPerConfig, seed: int, torch, steps: int = 120):
    rows = training_rows(data, seed, config.maximum_length)
    from auto_research.runtime import device_for
    device = device_for(torch); model.to(device); torch.manual_seed(seed)
    tensors = [torch.tensor(value, device=device) for value in rows]
    optimizer = torch.optim.AdamW(model.parameters(), lr=8e-4); rng = np.random.default_rng(seed); losses = []
    for _ in range(steps):
        index = torch.tensor(rng.choice(len(rows[0]), min(256, len(rows[0])), replace=False), device=device)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(model(tensors[0][index], tensors[1][index]), tensors[2][index])
        optimizer.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step(); losses.append(float(loss.detach().cpu()))
    return {"steps": steps, "initial_loss": float(np.mean(losses[:5])), "final_loss": float(np.mean(losses[-5:])), "parameters": sum(p.numel() for p in model.parameters()), "device": device.type}


def score_catalog(model, history, config: SlimPerConfig, torch):
    device = next(model.parameters()).device; items = torch.arange(config.item_count, device=device)
    padded = [config.item_count] * max(0, config.maximum_length - len(history)) + list(history[-config.maximum_length:])
    history_tensor = torch.tensor([padded], device=device)
    with torch.inference_mode():
        if hasattr(model, "encode_request"):
            encoded = model.encode_request(history_tensor)
            encoded = tuple(value.expand(config.item_count, *value.shape[1:]) for value in encoded)
            return model.forward_encoded(encoded, items).cpu().numpy()
        return model(history_tensor.expand(config.item_count, -1), items).cpu().numpy()


def complexity(config: SlimPerConfig):
    n, l, k, q, d = config.maximum_length, config.layers, config.knowledge_slots, config.query_slots, config.dimensions
    return {
        "baseline_attention_score_elements": config.baseline_layers * (n + 1) ** 2,
        "slimper_attention_score_elements": l * q * n,
        "baseline_intermediate_elements": config.baseline_layers * (n + 1) * d,
        "slimper_intermediate_elements": l * k * d,
        "user_tokens_shared_across_candidates": True,
    }
