"""Reference kernels for the 2026-09-11 foundation-model paper batch."""

from __future__ import annotations

from dataclasses import dataclass
import math
import re

import numpy as np


@dataclass(frozen=True)
class QuantizedBlock:
    codes: np.ndarray
    minimum: np.ndarray
    scale: np.ndarray
    bits: int


def windowed_key_quantize(keys: np.ndarray, *, bits: int = 2, window: int = 8) -> list[QuantizedBlock]:
    """OmniKVQuant short-window asymmetric quantization for temporal keys."""
    keys = np.asarray(keys, dtype=np.float64)
    if keys.ndim != 2 or bits < 1 or window < 1:
        raise ValueError("keys must be [tokens, dimensions], with positive bits/window")
    levels = 2**bits - 1
    blocks = []
    for start in range(0, len(keys), window):
        values = keys[start : start + window]
        minimum = values.min(0)
        maximum = values.max(0)
        scale = np.maximum((maximum - minimum) / levels, 1e-12)
        codes = np.clip(np.rint((values - minimum) / scale), 0, levels).astype(np.uint8)
        blocks.append(QuantizedBlock(codes, minimum, scale, bits))
    return blocks


def dequantize_blocks(blocks: list[QuantizedBlock]) -> np.ndarray:
    return np.concatenate([
        block.minimum + block.scale * block.codes.astype(np.float64)
        for block in blocks
    ])


def modality_value_rotate(values: np.ndarray, modalities: np.ndarray) -> tuple[np.ndarray, dict[int, np.ndarray]]:
    """Center and independently rotate each modality's value geometry."""
    values = np.asarray(values, dtype=np.float64)
    modalities = np.asarray(modalities)
    if len(values) != len(modalities):
        raise ValueError("values and modalities must have matching token counts")
    rotated = np.empty_like(values)
    rotations = {}
    for modality in np.unique(modalities):
        mask = modalities == modality
        group = values[mask]
        _, _, vh = np.linalg.svd(group - group.mean(0), full_matrices=False)
        rotation = vh.T
        if rotation.shape != (values.shape[1], values.shape[1]):
            rotation = np.eye(values.shape[1])
        rotated[mask] = group @ rotation
        rotations[int(modality)] = rotation
    return rotated, rotations


def sensenova_patch_targets(patches: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Spatial patch-reconstruction targets without a tokenizer or VAE."""
    patches = np.asarray(patches, dtype=np.float64)
    mask = np.asarray(mask, dtype=bool)
    if patches.ndim != 3 or mask.shape != patches.shape[:2]:
        raise ValueError("patches must be [batch, tokens, dim] and mask [batch, tokens]")
    reconstructed = patches.copy()
    for row in range(len(patches)):
        visible = patches[row, ~mask[row]]
        fill = visible.mean(0) if len(visible) else np.zeros(patches.shape[-1])
        reconstructed[row, mask[row]] = fill
    return reconstructed


def multi_expert_opd(teacher_deltas: np.ndarray, gate_logits: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """SenseNova-U1.5 mixture-of-experts OPD direction."""
    deltas = np.asarray(teacher_deltas, dtype=np.float64)
    logits = np.asarray(gate_logits, dtype=np.float64)
    weights = np.exp(logits - logits.max(-1, keepdims=True))
    weights /= weights.sum(-1, keepdims=True)
    return np.sum(deltas * weights[..., None], axis=-2), weights


def frames_on_demand(
    caption_embedding: np.ndarray,
    query_embedding: np.ndarray,
    frame_embeddings: np.ndarray,
    *,
    maximum_frames: int,
    threshold: float = 0.35,
) -> tuple[np.ndarray, dict[str, float]]:
    """Caption-first visual-need routing with a bounded frame budget."""
    caption = np.asarray(caption_embedding, dtype=np.float64)
    query = np.asarray(query_embedding, dtype=np.float64)
    frames = np.asarray(frame_embeddings, dtype=np.float64)
    cosine = float(caption @ query / (np.linalg.norm(caption) * np.linalg.norm(query) + 1e-12))
    need_visual = cosine < threshold
    if not need_visual or maximum_frames <= 0:
        chosen = np.asarray([], dtype=np.int64)
    else:
        scores = frames @ query / (np.linalg.norm(frames, axis=1) * np.linalg.norm(query) + 1e-12)
        chosen = np.argsort(-scores)[: min(maximum_frames, len(frames))]
    return chosen, {"caption_query_similarity": cosine, "visual_need": float(need_visual), "selected_frames": float(len(chosen))}


def repetition_regularization(repetition_factor: float, *, sparse_model: bool) -> dict[str, float]:
    """Repeat-aware masking/dropout schedule from the dense-vs-MoE study."""
    if repetition_factor < 1:
        raise ValueError("repetition_factor must be >= 1")
    pressure = math.log2(repetition_factor) / 6.0
    dropout = min(0.45, 0.05 + (0.18 if sparse_model else 0.10) * pressure)
    masking = min(0.50, 0.08 + (0.22 if sparse_model else 0.12) * pressure)
    return {"dropout": dropout, "token_masking": masking, "repeat_pressure": pressure}


def soft_musec_update(momentum: np.ndarray, *, clip: float = 1.0, softness: float = 0.2) -> tuple[np.ndarray, dict[str, float]]:
    """Smooth spectral clipping for a Muon-style matrix update."""
    matrix = np.asarray(momentum, dtype=np.float64)
    u, singular, vh = np.linalg.svd(matrix, full_matrices=False)
    clipped = clip * np.tanh(singular / max(clip * softness, 1e-12))
    update = (u * clipped) @ vh
    return update, {
        "spectral_norm_before": float(singular.max(initial=0.0)),
        "spectral_norm_after": float(clipped.max(initial=0.0)),
        "clipped_singular_values": float(np.count_nonzero(singular > clip)),
    }


def similarity_contracting_windows(turns: list[str], embeddings: np.ndarray, *, minimum_similarity: float = 0.25) -> list[list[str]]:
    """SWRouter segmentation: extend a window only while similarity contracts."""
    embeddings = np.asarray(embeddings, dtype=np.float64)
    if len(turns) != len(embeddings):
        raise ValueError("turns and embeddings must have equal length")
    windows: list[list[str]] = []
    for turn, vector in zip(turns, embeddings):
        if not windows:
            windows.append([turn])
            continue
        previous_index = sum(len(window) for window in windows) - 1
        previous = embeddings[previous_index]
        similarity = float(previous @ vector / (np.linalg.norm(previous) * np.linalg.norm(vector) + 1e-12))
        if similarity >= minimum_similarity:
            windows[-1].append(turn)
        else:
            windows.append([turn])
    return windows


def route_model(query: str, windows: list[list[str]], model_profiles: dict[str, set[str]]) -> tuple[str, dict[str, float]]:
    tokens = set(re.findall(r"[a-z0-9]+", (query + " " + " ".join(windows[-1])).lower()))
    scores = {
        name: len(tokens & profile) / max(1, len(tokens | profile))
        for name, profile in model_profiles.items()
    }
    return max(scores, key=scores.get), scores
