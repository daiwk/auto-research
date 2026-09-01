from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores, softmax


def split_streams(history, serving_events: int = 4) -> tuple[np.ndarray, np.ndarray]:
    events = np.asarray(history, dtype=np.int64)
    if len(events) <= serving_events:
        return events[:1], events
    return events[:-serving_events], events[-serving_events:]


def score_monolithic(data, history) -> np.ndarray:
    return base_scores(data, history)


def score_transx(data, history) -> np.ndarray:
    behavior, serving = split_streams(history)
    item_features = data.sequences.features
    behavior_features = item_features[behavior]
    serving_context = item_features[serving].mean(0)

    # Candidate queries cross-attend to a cached behavior stream. A local tail
    # and a global pooled token keep cost bounded while preserving long history.
    local = behavior_features[-min(8, len(behavior_features)) :]
    global_token = behavior_features.mean(0, keepdims=True)
    cache = np.concatenate((global_token, local), axis=0)
    attention = softmax(item_features @ cache.T / np.sqrt(cache.shape[1]), axis=1)
    crossed = np.sum((attention @ cache) * item_features, axis=1)
    serving_score = item_features @ serving_context
    transition = data.transition[serving].mean(0)
    return 0.48 * transition + 0.32 * crossed + 0.20 * serving_score


def transx_diagnostics(data, history) -> dict[str, float]:
    behavior, serving = split_streams(history)
    cache_tokens = 1 + min(8, len(behavior))
    monolithic_pairs = len(history) ** 2
    crossed_pairs = len(serving) * cache_tokens
    return {
        "behavior_events": int(len(behavior)),
        "serving_events": int(len(serving)),
        "cached_behavior_tokens": int(cache_tokens),
        "monolithic_attention_pairs": int(monolithic_pairs),
        "cross_stream_attention_pairs": int(crossed_pairs),
        "attention_pair_reduction": float(1 - crossed_pairs / max(monolithic_pairs, 1)),
    }
