from __future__ import annotations

from auto_research.runtime import device_for

import random
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import initialize, require_backend, summarize_training, training_examples


@dataclass(frozen=True)
class TIGERConfig:
    dimensions: int = 48
    heads: int = 4
    layers: int = 2
    sequence_length: int = 16
    codebooks: int = 3
    codebook_size: int = 16
    rqvae_steps: int = 240
    training_steps: int = 240
    batch_size: int = 48
    learning_rate: float = 4e-4
    candidate_chunk: int = 1024


def train_semantic_ids(features: np.ndarray, config: TIGERConfig, seed: int):
    torch, nn = require_backend()
    torch.manual_seed(seed)
    np.random.seed(seed)
    device = device_for(torch)
    values = torch.tensor(features, dtype=torch.float32, device=device)

    class RQVAE(nn.Module):
        def __init__(self):
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Linear(features.shape[1], 64), nn.ReLU(), nn.Linear(64, 32)
            )
            self.decoder = nn.Sequential(
                nn.Linear(32, 64), nn.ReLU(), nn.Linear(64, features.shape[1])
            )
            self.codebooks = nn.ParameterList([
                nn.Parameter(torch.randn(config.codebook_size, 32) * 0.05)
                for _ in range(config.codebooks)
            ])

        def quantize(self, latent):
            residual = latent
            quantized = torch.zeros_like(latent)
            rq_loss = latent.new_zeros(())
            codes = []
            for codebook in self.codebooks:
                distances = torch.cdist(residual, codebook)
                code = distances.argmin(dim=-1)
                selected = codebook[code]
                rq_loss += torch.nn.functional.mse_loss(
                    residual.detach(), selected
                ) + 0.25 * torch.nn.functional.mse_loss(
                    residual, selected.detach()
                )
                quantized = quantized + selected
                residual = residual - selected
                codes.append(code)
            straight_through = latent + (quantized - latent).detach()
            return straight_through, rq_loss, torch.stack(codes, dim=1)

    model = RQVAE().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    losses = []
    for _ in range(config.rqvae_steps):
        latent = model.encoder(values)
        quantized, rq_loss, _ = model.quantize(latent)
        reconstruction = torch.nn.functional.mse_loss(model.decoder(quantized), values)
        loss = reconstruction + rq_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    with torch.inference_mode():
        latent = model.encoder(values).cpu().numpy()
    codes = residual_kmeans(
        latent, config.codebooks, config.codebook_size, seed + 97
    )
    semantic_ids, collision_size = append_collision_tokens(codes)
    return semantic_ids, {
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
        "unique_prefixes": len({tuple(row) for row in codes}),
        "collision_token_cardinality": collision_size,
    }


def residual_kmeans(latent, levels: int, size: int, seed: int, iterations: int = 30):
    rng = np.random.default_rng(seed)
    residual = latent.copy()
    codes = []
    for _ in range(levels):
        centers = residual[rng.choice(len(residual), size=size, replace=False)].copy()
        for _ in range(iterations):
            distances = ((residual[:, None] - centers[None]) ** 2).sum(-1)
            labels = distances.argmin(axis=1)
            for index in range(size):
                members = residual[labels == index]
                if len(members):
                    centers[index] = members.mean(axis=0)
        labels = ((residual[:, None] - centers[None]) ** 2).sum(-1).argmin(axis=1)
        codes.append(labels)
        residual -= centers[labels]
    return np.stack(codes, axis=1).astype(np.int64)


def append_collision_tokens(codes: np.ndarray):
    counters: dict[tuple[int, ...], int] = {}
    collision = []
    for row in codes:
        key = tuple(int(value) for value in row)
        collision.append(counters.get(key, 0))
        counters[key] = counters.get(key, 0) + 1
    collision_size = max(collision, default=0) + 1
    return np.column_stack((codes, collision)).astype(np.int64), collision_size


def random_ids(
    item_count: int, config: TIGERConfig, seed: int, collision_size: int
):
    rng = np.random.default_rng(seed)
    capacity = config.codebook_size**config.codebooks
    values = rng.choice(capacity, size=item_count, replace=False)
    codes = []
    for value in values:
        row = []
        for _ in range(config.codebooks):
            row.append(int(value % config.codebook_size))
            value //= config.codebook_size
        codes.append(row)
    collision = rng.integers(0, collision_size, size=item_count)
    return np.column_stack((np.asarray(codes, dtype=np.int64), collision))


def build_model(semantic_ids: np.ndarray, config: TIGERConfig):
    torch, nn = require_backend()
    collision_size = int(semantic_ids[:, -1].max()) + 1
    vocab_size = config.codebooks * config.codebook_size + collision_size
    bos_token = vocab_size
    offsets = np.asarray(
        [level * config.codebook_size for level in range(config.codebooks)]
        + [config.codebooks * config.codebook_size],
        dtype=np.int64,
    )
    tokens = torch.tensor(semantic_ids + offsets, dtype=torch.long)

    class TIGER(nn.Module):
        def __init__(self):
            super().__init__()
            self.register_buffer("semantic_tokens", tokens)
            self.token = nn.Embedding(vocab_size + 1, config.dimensions)
            self.encoder_position = nn.Embedding(
                config.sequence_length * semantic_ids.shape[1], config.dimensions
            )
            self.decoder_position = nn.Embedding(semantic_ids.shape[1], config.dimensions)
            nn.init.normal_(self.token.weight, std=0.02)
            nn.init.normal_(self.encoder_position.weight, std=0.02)
            nn.init.normal_(self.decoder_position.weight, std=0.02)
            encoder_layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            decoder_layer = nn.TransformerDecoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.encoder = nn.TransformerEncoder(encoder_layer, config.layers)
            self.decoder = nn.TransformerDecoder(decoder_layer, config.layers)

        def encode(self, histories):
            source = self.semantic_tokens[histories].flatten(1, 2)
            positions = torch.arange(source.shape[1], device=source.device)
            return self.encoder(self.token(source) + self.encoder_position(positions))

        def decode(self, memory, target_items):
            target = self.semantic_tokens[target_items]
            bos = torch.full(
                (*target.shape[:-1], 1), bos_token, device=target.device
            )
            decoder_input = torch.cat((bos, target[..., :-1]), dim=-1)
            positions = torch.arange(target.shape[-1], device=target.device)
            embedded = self.token(decoder_input) + self.decoder_position(positions)
            causal = nn.Transformer.generate_square_subsequent_mask(
                target.shape[-1], device=target.device
            )
            hidden = self.decoder(embedded, memory, tgt_mask=causal)
            return hidden @ self.token.weight[:vocab_size].T, target

        def forward(self, histories, target_items):
            return self.decode(self.encode(histories), target_items)

    return TIGER()


def train_model(semantic_ids, data, config: TIGERConfig, seed: int):
    model, device, torch = initialize(build_model(semantic_ids, config), seed)
    rows = training_examples(data.train, config.sequence_length)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    model.train()
    for _ in range(config.training_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = torch.tensor([row[0] for row in batch], device=device)
        targets = torch.tensor([row[1] for row in batch], device=device)
        logits, target_tokens = model(histories, targets)
        loss = torch.nn.functional.cross_entropy(
            logits.reshape(-1, logits.shape[-1]), target_tokens.reshape(-1)
        )
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)


def score_all(model, history, item_count: int, config: TIGERConfig):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    recent = history[-config.sequence_length :]
    padded = (recent[0],) * (config.sequence_length - len(recent)) + recent
    histories = torch.tensor([padded], device=device)
    model.eval()
    scores = []
    with torch.inference_mode():
        memory = model.encode(histories)
        for start in range(0, item_count, config.candidate_chunk):
            candidates = torch.arange(
                start, min(start + config.candidate_chunk, item_count), device=device
            )
            expanded = memory.expand(len(candidates), -1, -1)
            logits, target_tokens = model.decode(expanded, candidates)
            log_probabilities = torch.log_softmax(logits, dim=-1)
            score = log_probabilities.gather(
                -1, target_tokens.unsqueeze(-1)
            ).squeeze(-1).sum(-1)
            scores.append(score.cpu().numpy())
    return np.concatenate(scores)
