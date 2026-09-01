from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes, softmax


def build_semantic_native(data, seed: int = 42, width: int = 12) -> dict:
    codes = hierarchical_codes(data.sequences.features, levels=3, width=width, seed=seed)
    codebooks = []
    for level in range(codes.shape[1]):
        values = np.zeros((width, data.sequences.features.shape[1]), dtype=np.float64)
        for code in range(width):
            members = data.sequences.features[codes[:, level] == code]
            if len(members):
                values[code] = members.mean(axis=0)
        codebooks.append(values)
    # Depth-truncated bigrams preserve coarse and middle semantic identity.
    bigrams = codes[:, 0] * width + codes[:, 1]
    return {"codes": codes, "codebooks": codebooks, "bigrams": bigrams, "width": width}


def _semantic_tokens(data, state: dict, items: np.ndarray) -> np.ndarray:
    codes = state["codes"][items]
    return 0.65 * state["codebooks"][0][codes[:, 0]] + 0.35 * state["codebooks"][1][codes[:, 1]]


def _attend(tokens: np.ndarray, queries: np.ndarray) -> np.ndarray:
    scale = np.sqrt(max(tokens.shape[1], 1))
    weights = softmax(queries @ tokens.T / scale, axis=-1)
    return weights @ tokens


def score_vanilla_short(data, state: dict, history) -> np.ndarray:
    sequence = np.asarray(history[-12:], dtype=np.int64)
    tokens = data.sequences.features[sequence].astype(np.float64)
    query = tokens[-1:]
    user = _attend(tokens, query).mean(axis=0)
    return data.sequences.features @ user + 0.08 * data.popularity


def score_semantic_long(data, state: dict, history, folding: int = 4) -> tuple[np.ndarray, dict]:
    sequence = np.asarray(history[-48:], dtype=np.int64)
    semantic = _semantic_tokens(data, state, sequence)
    folded = []
    for start in range(0, len(semantic), folding):
        window = semantic[start : start + folding]
        # Parameter-free temporal folding trades resolution for a richer token.
        folded.append(0.65 * window.mean(axis=0) + 0.35 * window[-1])
    folded_tokens = np.asarray(folded)
    global_queries = np.stack(
        (semantic.mean(axis=0), semantic[-min(8, len(semantic)) :].mean(axis=0))
    )
    tokens = np.concatenate((global_queries, folded_tokens), axis=0)
    global_state = _attend(tokens, global_queries).mean(axis=0)
    pooled = tokens.mean(axis=0)
    user = 0.6 * global_state + 0.4 * pooled
    semantic_items = _semantic_tokens(data, state, np.arange(data.item_count))
    score = semantic_items @ user + 0.12 * data.transition[sequence[-1]] + 0.05 * data.popularity
    return score, {
        "input_events": len(sequence),
        "folding_factor": folding,
        "folded_tokens": len(folded_tokens),
        "global_queries": len(global_queries),
        "attention_tokens": len(tokens),
        "attention_pair_reduction": 1.0 - (len(tokens) ** 2 / max(len(sequence) ** 2, 1)),
    }
