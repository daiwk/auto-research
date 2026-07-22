from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from auto_research.runtime import device_for
from ..llm_training import require_torch
from ..tiger.model import TIGERConfig, train_semantic_ids


@dataclass(frozen=True)
class RecGPTV3Config:
    dimensions: int = 48
    heads: int = 4
    maximum_history: int = 40
    recent_events: int = 8
    memory_slots: int = 6
    latent_tokens: int = 4
    codebook_size: int = 16
    rqvae_steps: int = 80
    training_steps: int = 180
    batch_size: int = 48
    learning_rate: float = 5e-4


def semantic_ids(features: np.ndarray, config: RecGPTV3Config, seed: int):
    tiger = TIGERConfig(
        codebooks=2,
        codebook_size=config.codebook_size,
        rqvae_steps=config.rqvae_steps,
        training_steps=1,
    )
    ids, diagnostics = train_semantic_ids(features, tiger, seed)
    return ids[:, :2], diagnostics


def _encoder(nn, config):
    layer = nn.TransformerEncoderLayer(
        config.dimensions, config.heads, 4 * config.dimensions,
        dropout=0.0, batch_first=True, norm_first=True,
    )
    return nn.TransformerEncoder(layer, 2)


def build_models(features: np.ndarray, ids: np.ndarray, config: RecGPTV3Config):
    torch = require_torch()
    nn = torch.nn
    feature_tensor = torch.tensor(features, dtype=torch.float32)
    id_tensor = torch.tensor(ids, dtype=torch.long)

    class ItemTower(nn.Module):
        def __init__(self):
            super().__init__()
            self.register_buffer("features", feature_tensor)
            self.register_buffer("semantic_ids", id_tensor)
            self.text = nn.Sequential(nn.Linear(features.shape[1], 64), nn.GELU(), nn.Linear(64, config.dimensions))
            self.sid = nn.ModuleList([nn.Embedding(config.codebook_size, config.dimensions) for _ in range(2)])

        def forward(self, items=None):
            index = torch.arange(len(self.features), device=self.features.device) if items is None else items
            values = self.text(self.features[index])
            codes = self.semantic_ids[index]
            return values + 0.5 * (self.sid[0](codes[..., 0]) + self.sid[1](codes[..., 1]))

    class StatelessV2(nn.Module):
        def __init__(self):
            super().__init__()
            self.items = ItemTower()
            self.position = nn.Embedding(config.maximum_history, config.dimensions)
            self.encoder = _encoder(nn, config)
            self.norm = nn.LayerNorm(config.dimensions)

        def encode(self, histories):
            positions = torch.arange(histories.shape[1], device=histories.device)
            hidden = self.encoder(self.items(histories) + self.position(positions))
            return self.norm(hidden[:, -1])

        def forward(self, histories):
            return self.encode(histories) @ self.items().T

    class RecGPTV3(nn.Module):
        def __init__(self):
            super().__init__()
            self.items = ItemTower()
            self.position = nn.Embedding(config.maximum_history, config.dimensions)
            self.explicit_teacher = _encoder(nn, config)
            self.memory_queries = nn.Parameter(torch.randn(config.memory_slots, config.dimensions) * 0.02)
            self.latent_queries = nn.Parameter(torch.randn(config.latent_tokens, config.dimensions) * 0.02)
            self.memory_attention = nn.MultiheadAttention(config.dimensions, config.heads, batch_first=True)
            self.latent_attention = nn.MultiheadAttention(config.dimensions, config.heads, batch_first=True)
            self.student = _encoder(nn, config)
            self.reconstruct = nn.Linear(config.dimensions, config.dimensions)
            self.norm = nn.LayerNorm(config.dimensions)

        def explicit(self, histories):
            positions = torch.arange(histories.shape[1], device=histories.device)
            states = self.explicit_teacher(self.items(histories) + self.position(positions))
            chunks = torch.chunk(states, config.latent_tokens, dim=1)
            segments = torch.stack([chunk.mean(1) for chunk in chunks], dim=1)
            return states[:, -1], segments

        def encode(self, histories, return_aux=False):
            old = histories[:, :-config.recent_events]
            recent = histories[:, -config.recent_events:]
            old_values = self.items(old)
            queries = self.memory_queries.unsqueeze(0).expand(histories.shape[0], -1, -1)
            memory, memory_weights = self.memory_attention(queries, old_values, old_values, need_weights=True)
            context = torch.cat((memory, self.items(recent)), dim=1)
            latent_queries = self.latent_queries.unsqueeze(0).expand(histories.shape[0], -1, -1)
            latent, _ = self.latent_attention(latent_queries, context, context, need_weights=False)
            latent = self.student(latent)
            representation = self.norm(latent.mean(1) + context.mean(1))
            if return_aux:
                teacher, segments = self.explicit(histories)
                return representation, latent, teacher, segments, memory_weights
            return representation

        def forward(self, histories, return_aux=False):
            encoded = self.encode(histories, return_aux=return_aux)
            if not return_aux:
                return encoded @ self.items().T
            representation, latent, teacher, segments, weights = encoded
            return representation @ self.items().T, teacher @ self.items().T, latent, segments, weights

    return StatelessV2(), RecGPTV3()


def training_rows(data, maximum_history: int):
    rows = []
    for sequence in data.train:
        for index in range(2, len(sequence)):
            history = tuple(sequence[max(0, index - maximum_history):index])
            padded = (history[0],) * (maximum_history - len(history)) + history
            rows.append((padded, sequence[index]))
    return rows


def train(model, data, config: RecGPTV3Config, seed: int, method: bool):
    torch = require_torch()
    torch.manual_seed(seed); np.random.seed(seed); random.seed(seed)
    device = device_for(torch); model = model.to(device)
    rows = training_rows(data, config.maximum_history); rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []; reconstruction = []; ranking_feedback = []
    popularity = torch.tensor(np.log1p(data.popularity), dtype=torch.float32, device=device)
    popularity = (popularity - popularity.mean()) / popularity.std().clamp_min(1e-6)
    model.train()
    teacher_warmup = []
    if method:
        # Paper stage 1: establish a stable explicit-CoT teacher before the
        # explicit-to-implicit alignment curriculum starts.
        for _ in range(config.training_steps // 2):
            batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
            histories = torch.tensor([row[0] for row in batch], dtype=torch.long, device=device)
            targets = torch.tensor([row[1] for row in batch], dtype=torch.long, device=device)
            _, teacher_logits, _, _, _ = model(histories, return_aux=True)
            loss = torch.nn.functional.cross_entropy(teacher_logits, targets)
            optimizer.zero_grad(set_to_none=True); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
            teacher_warmup.append(float(loss.detach().cpu()))
        for parameter in model.explicit_teacher.parameters():
            parameter.requires_grad_(False)
        optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=config.learning_rate)
    for _ in range(config.training_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = torch.tensor([row[0] for row in batch], dtype=torch.long, device=device)
        targets = torch.tensor([row[1] for row in batch], dtype=torch.long, device=device)
        if method:
            logits, teacher_logits, latent, segments, _ = model(histories, return_aux=True)
            prediction = torch.nn.functional.cross_entropy(logits, targets)
            reconstruct = torch.nn.functional.mse_loss(model.reconstruct(latent), segments.detach())
            # Public stand-in for RLRF: distil a dense downstream ranking signal,
            # combining the explicit teacher with the logged popularity prior.
            reward = torch.softmax(teacher_logits.detach() + 0.02 * popularity, dim=-1)
            feedback = torch.nn.functional.kl_div(torch.log_softmax(logits, -1), reward, reduction="batchmean")
            loss = prediction + 0.30 * reconstruct + 0.12 * feedback
            reconstruction.append(float(reconstruct.detach().cpu()))
            ranking_feedback.append(float(feedback.detach().cpu()))
        else:
            loss = torch.nn.functional.cross_entropy(model(histories), targets)
        optimizer.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {
        "initial_loss": float(np.mean(losses[:20])), "final_loss": float(np.mean(losses[-20:])),
        "reconstruction_loss": float(np.mean(reconstruction[-20:])) if reconstruction else None,
        "ranking_feedback_loss": float(np.mean(ranking_feedback[-20:])) if ranking_feedback else None,
        "teacher_warmup_initial_loss": float(np.mean(teacher_warmup[:20])) if teacher_warmup else None,
        "teacher_warmup_final_loss": float(np.mean(teacher_warmup[-20:])) if teacher_warmup else None,
        "device": device.type,
    }


def score_catalog(model, history, config: RecGPTV3Config, torch):
    recent = tuple(history[-config.maximum_history:])
    padded = (recent[0],) * (config.maximum_history - len(recent)) + recent
    tensor = torch.tensor([padded], dtype=torch.long, device=next(model.parameters()).device)
    model.eval()
    with torch.inference_mode():
        return model(tensor).squeeze(0).cpu().numpy()


def diagnostics(model, data, config: RecGPTV3Config, torch):
    histories = []
    for history in data.train[: min(64, len(data.train))]:
        recent = tuple(history[-config.maximum_history:])
        histories.append((recent[0],) * (config.maximum_history - len(recent)) + recent)
    values = torch.tensor(histories, dtype=torch.long, device=next(model.parameters()).device)
    model.eval()
    with torch.inference_mode():
        _, _, latent, segments, weights = model(values, return_aux=True)
        cosine = torch.nn.functional.cosine_similarity(model.reconstruct(latent), segments, dim=-1).mean()
        representative = weights.argmax(-1)
        traceable = (representative >= 0).float().mean()
    full = config.maximum_history
    memory_input = config.memory_slots + config.recent_events
    return {
        "latent_reconstruction_cosine": float(cosine.cpu()),
        "memory_traceable_fraction": float(traceable.cpu()),
        "memory_input_tokens": memory_input,
        "full_history_tokens": full,
        "memory_token_reduction_percent": 100 * (1 - memory_input / full),
        "explicit_reasoning_slots": config.maximum_history,
        "latent_reasoning_slots": config.latent_tokens,
        "reasoning_slot_reduction_percent": 100 * (1 - config.latent_tokens / config.maximum_history),
    }
