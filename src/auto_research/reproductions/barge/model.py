from __future__ import annotations

from dataclasses import dataclass
import random

import numpy as np

from auto_research.runtime import device_for
from ..industrial_batch import padded_histories, training_pairs
from ..llm_training import require_torch
from ..tiger.model import append_collision_tokens, residual_kmeans


@dataclass(frozen=True)
class BARGEConfig:
    dimensions: int = 48
    heads: int = 4
    layers: int = 2
    sequence_length: int = 16
    codebooks: int = 2
    codebook_size: int = 16
    osq_steps: int = 90
    training_steps: int = 140
    batch_size: int = 48
    learning_rate: float = 5e-4
    hpr_weight: float = 0.15
    hpr_score_weight: float = 0.35


def train_osq_ids(features: np.ndarray, config: BARGEConfig, seed: int):
    """Train the orthogonal split and two residual quantizers, then freeze IDs."""
    torch = require_torch()
    torch.manual_seed(seed)
    device = device_for(torch)
    values = torch.tensor(features, dtype=torch.float32, device=device)
    width = features.shape[1]
    if width % 2:
        values = torch.nn.functional.pad(values, (0, 1))
        width += 1
    vectors = torch.nn.Parameter(torch.randn(2, width, device=device))
    codebooks = torch.nn.ParameterList([
        torch.nn.Parameter(
            torch.randn(config.codebook_size, width // 2, device=device) * 0.05
        )
        for _ in range(2 * config.codebooks)
    ])
    optimizer = torch.optim.AdamW([vectors, *codebooks], lr=2e-3)
    losses = []

    def rotation():
        identity = torch.eye(width, device=device)
        result = identity
        for vector in vectors:
            normalized = vector / vector.norm().clamp_min(1e-8)
            result = (identity - 2 * normalized[:, None] * normalized[None, :]) @ result
        return result

    def quantize(part, channel):
        residual = part
        quantized = torch.zeros_like(part)
        codes = []
        commitment = part.new_zeros(())
        for level in range(config.codebooks):
            book = codebooks[channel * config.codebooks + level]
            index = torch.cdist(residual, book).argmin(-1)
            selected = book[index]
            commitment = commitment + torch.nn.functional.mse_loss(
                residual.detach(), selected
            ) + 0.25 * torch.nn.functional.mse_loss(residual, selected.detach())
            quantized = quantized + selected
            residual = residual - selected
            codes.append(index)
        straight_through = part + (quantized - part).detach()
        return straight_through, commitment, torch.stack(codes, 1)

    for _ in range(config.osq_steps):
        matrix = rotation()
        rotated = values @ matrix.T
        left, right = rotated.chunk(2, -1)
        left_q, left_loss, _ = quantize(left, 0)
        right_q, right_loss, _ = quantize(right, 1)
        reconstruction = torch.cat((left_q, right_q), -1) @ matrix
        loss = torch.nn.functional.mse_loss(reconstruction, values)
        loss = loss + 0.20 * (left_loss + right_loss)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_([vectors, *codebooks], 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))

    with torch.inference_mode():
        matrix = rotation()
        rotated = values @ matrix.T
        left, right = rotated.chunk(2, -1)
        # Stable hard assignment after training avoids straight-through jitter.
        left_codes = residual_kmeans(
            left.cpu().numpy(), config.codebooks, config.codebook_size, seed + 11
        )
        right_codes = residual_kmeans(
            right.cpu().numpy(), config.codebooks, config.codebook_size, seed + 29
        )
        left_ids, left_collisions = append_collision_tokens(left_codes)
        right_ids, right_collisions = append_collision_tokens(right_codes)
        orthogonality_error = float(
            (matrix.T @ matrix - torch.eye(width, device=device)).abs().max().cpu()
        )
    return (left_ids, right_ids), {
        "initial_loss": float(np.mean(losses[:10])),
        "final_loss": float(np.mean(losses[-10:])),
        "orthogonality_error": orthogonality_error,
        "channel_a_collision_cardinality": left_collisions,
        "channel_b_collision_cardinality": right_collisions,
    }


def build_barge(ids_a: np.ndarray, ids_b: np.ndarray, config: BARGEConfig):
    torch = require_torch()
    nn = torch.nn
    id_tensors = (
        torch.tensor(ids_a, dtype=torch.long),
        torch.tensor(ids_b, dtype=torch.long),
    )
    cardinalities = tuple(
        tuple(int(ids[:, level].max()) + 1 for level in range(ids.shape[1]))
        for ids in (ids_a, ids_b)
    )
    levels = ids_a.shape[1]

    class Channel(nn.Module):
        def __init__(self, sizes):
            super().__init__()
            self.embeddings = nn.ModuleList(
                nn.Embedding(size, config.dimensions) for size in sizes
            )
            self.heads = nn.ModuleList(
                nn.Linear(config.dimensions, size, bias=False) for size in sizes
            )
            self.context_projection = nn.ModuleList(
                nn.Linear(config.dimensions, config.dimensions, bias=False)
                for _ in sizes
            )
            self.path_projection = nn.ModuleList(
                nn.Linear(config.dimensions, config.dimensions, bias=False)
                for _ in sizes
            )
            self.log_temperature = nn.Parameter(torch.zeros(levels))
            layer = nn.TransformerDecoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.decoder = nn.TransformerDecoder(layer, config.layers)
            self.bos = nn.Parameter(torch.randn(config.dimensions) * 0.02)
            self.position = nn.Parameter(torch.randn(levels, config.dimensions) * 0.02)

        def path_embeddings(self, ids):
            values, cumulative = [], 0.0
            for level, embedding in enumerate(self.embeddings):
                cumulative = cumulative + embedding(ids[:, level])
                values.append(cumulative)
            return torch.stack(values, 1)

        def decode(self, memory, target_ids):
            path = self.path_embeddings(target_ids)
            decoder_input = torch.cat((
                self.bos[None, None].expand(len(target_ids), 1, -1),
                path[:, :-1],
            ), 1) + self.position[None]
            causal = nn.Transformer.generate_square_subsequent_mask(
                levels, device=memory.device
            )
            hidden = self.decoder(decoder_input, memory, tgt_mask=causal)
            logits = [head(hidden[:, level]) for level, head in enumerate(self.heads)]
            return logits, path, hidden[:, 0]

        def hpr_scores(self, context, paths):
            scores = []
            for level in range(levels):
                left = torch.nn.functional.normalize(
                    self.context_projection[level](context), dim=-1
                )
                right = torch.nn.functional.normalize(
                    self.path_projection[level](paths[:, level]), dim=-1
                )
                scores.append(left @ right.T * self.log_temperature[level].exp())
            return scores

    class BARGE(nn.Module):
        def __init__(self):
            super().__init__()
            self.register_buffer("ids_a", id_tensors[0])
            self.register_buffer("ids_b", id_tensors[1])
            self.channels = nn.ModuleList(Channel(sizes) for sizes in cardinalities)
            self.ica_query = nn.Parameter(torch.randn(config.dimensions) * 0.02)
            self.ica_projection = nn.Sequential(
                nn.Linear(config.dimensions, 2 * config.dimensions),
                nn.GELU(),
                nn.Linear(2 * config.dimensions, config.dimensions),
            )
            self.ica_gate = nn.Linear(2 * config.dimensions, config.dimensions)
            encoder_layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.encoder = nn.TransformerEncoder(encoder_layer, config.layers)
            self.last_gate_mean = 0.0

        def item_tokens(self, items):
            tokens = []
            for channel_index, channel in enumerate(self.channels):
                ids = (self.ids_a, self.ids_b)[channel_index][items]
                tokens.extend(
                    embedding(ids[..., level])
                    for level, embedding in enumerate(channel.embeddings)
                )
            return torch.stack(tokens, -2)

        def encode(self, histories):
            tokens = self.item_tokens(histories)
            weights = torch.einsum(
                "d,bnld->bnl", self.ica_query, tokens
            ) / config.dimensions ** 0.5
            context = torch.einsum("bnl,bnld->bnd", weights.softmax(-1), tokens)
            projected = self.ica_projection(context)
            gate = torch.sigmoid(
                self.ica_gate(
                    torch.cat((tokens, projected.unsqueeze(-2).expand_as(tokens)), -1)
                )
            )
            self.last_gate_mean = float(gate.detach().mean().cpu())
            enriched = tokens + gate * projected.unsqueeze(-2)
            return self.encoder(enriched.flatten(1, 2))

        def losses(self, histories, targets):
            memory = self.encode(histories)
            total = memory.new_zeros(())
            diagnostics = {}
            for index, channel in enumerate(self.channels):
                ids = (self.ids_a, self.ids_b)[index][targets]
                logits, paths, context = channel.decode(memory, ids)
                ntp = sum(
                    torch.nn.functional.cross_entropy(logit, ids[:, level])
                    for level, logit in enumerate(logits)
                ) / levels
                matrices = channel.hpr_scores(context, paths)
                labels = torch.arange(len(targets), device=targets.device)
                hpr = sum(
                    0.5 * (
                        torch.nn.functional.cross_entropy(matrix, labels)
                        + torch.nn.functional.cross_entropy(matrix.T, labels)
                    )
                    for matrix in matrices
                ) / levels
                total = total + ntp + config.hpr_weight * hpr
                diagnostics[f"channel_{index}_ntp"] = ntp
                diagnostics[f"channel_{index}_hpr"] = hpr
            return total, diagnostics

        def channel_scores(self, memory, channel_index, candidates):
            channel = self.channels[channel_index]
            ids = (self.ids_a, self.ids_b)[channel_index][candidates]
            expanded = memory.expand(len(candidates), -1, -1)
            logits, paths, context = channel.decode(expanded, ids)
            generation = sum(
                torch.log_softmax(logit, -1).gather(
                    -1, ids[:, level, None]
                ).squeeze(-1)
                for level, logit in enumerate(logits)
            )
            hpr = 0.0
            for level, matrix in enumerate(channel.hpr_scores(context[:1], paths)):
                hpr = hpr + matrix.squeeze(0)
            return generation + config.hpr_score_weight * hpr / levels

        def score_catalog(self, histories):
            memory = self.encode(histories)
            candidates = torch.arange(self.ids_a.shape[0], device=memory.device)
            scores = [
                self.channel_scores(memory, channel, candidates)
                for channel in range(2)
            ]
            # Paper OR-fusion: an item ranks highly if either orthogonal channel retrieves it.
            rank_scores = []
            for score in scores:
                rank = torch.empty_like(score)
                rank[score.argsort(descending=True)] = torch.arange(
                    len(score), dtype=score.dtype, device=score.device
                )
                rank_scores.append(-rank)
            return torch.maximum(rank_scores[0], rank_scores[1])

    return BARGE()


def train_barge(model, data, config: BARGEConfig, seed: int):
    torch = require_torch()
    torch.manual_seed(seed)
    random.seed(seed)
    device = device_for(torch)
    model = model.to(device)
    rows = training_pairs(data, config.sequence_length)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses, ntp, hpr = [], [], []
    model.train()
    for _ in range(config.training_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = padded_histories([row[0] for row in batch], config.sequence_length, device, torch)
        targets = torch.tensor([row[1] for row in batch], device=device)
        loss, diagnostic = model.losses(histories, targets)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
        ntp.append(float((diagnostic["channel_0_ntp"] + diagnostic["channel_1_ntp"]).detach().cpu() / 2))
        hpr.append(float((diagnostic["channel_0_hpr"] + diagnostic["channel_1_hpr"]).detach().cpu() / 2))
    return model, {
        "steps": config.training_steps,
        "initial_loss": float(np.mean(losses[:10])),
        "final_loss": float(np.mean(losses[-10:])),
        "final_ntp_loss": float(np.mean(ntp[-10:])),
        "final_hpr_loss": float(np.mean(hpr[-10:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "ica_gate_mean": model.last_gate_mean,
        "device": device.type,
    }


def score_catalog(model, history, config: BARGEConfig, torch):
    recent = tuple(history[-config.sequence_length:])
    padded = (recent[0],) * (config.sequence_length - len(recent)) + recent
    histories = torch.tensor(
        [padded], dtype=torch.long, device=next(model.parameters()).device
    )
    model.eval()
    with torch.inference_mode():
        return model.score_catalog(histories).cpu().numpy()
