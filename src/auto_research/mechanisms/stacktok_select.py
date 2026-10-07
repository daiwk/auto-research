"""Extracted unchanged from auto_research.foundation_latest_20260916_followup; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def _softmax(values):
    values = np.asarray(values, dtype=np.float64)
    shifted = values - np.max(values, axis=-1, keepdims=True)
    exp = np.exp(shifted)
    return exp / (exp.sum(axis=-1, keepdims=True) + 1e-12)

def stacktok_select(tokens, query, budget: int):
    """StackTok reference-gated relevance/coverage interleaving."""
    tokens = np.asarray(tokens, dtype=np.float64)
    query = np.asarray(query, dtype=np.float64)
    budget = max(1, min(int(budget), len(tokens)))
    norms = np.linalg.norm(tokens, axis=1) + 1e-12
    similarity = (tokens @ tokens.T) / (norms[:, None] * norms[None, :])
    relevance = tokens @ query / (norms * (np.linalg.norm(query) + 1e-12))
    affinity = _softmax(relevance)
    entropy = float(-(affinity * np.log(affinity + 1e-12)).sum() / np.log(max(2, len(tokens))))
    coverage_order = [int(np.argmax(norms))]
    while len(coverage_order) < budget:
        remaining = [i for i in range(len(tokens)) if i not in coverage_order]
        coverage_order.append(max(remaining, key=lambda i: float(1.0 - similarity[i, coverage_order].max())))
    reference = []
    selected = []
    for step in range(budget):
        if selected:
            current_coverage = float(np.mean(np.max(similarity[:, selected], axis=1)))
        else:
            current_coverage = 0.0
        ref_prefix = coverage_order[: step + 1]
        target = float(np.mean(np.max(similarity[:, ref_prefix], axis=1))) * (0.5 + 0.5 * entropy)
        remaining = [i for i in range(len(tokens)) if i not in selected]
        if current_coverage + 1e-12 < target:
            choice = max(remaining, key=lambda i: float(1.0 - similarity[i, selected].max()) if selected else norms[i])
            reference.append(0.0)
        else:
            choice = max(remaining, key=lambda i: float(relevance[i]))
            reference.append(1.0)
        selected.append(int(choice))
    return np.asarray(selected), {
        "query_entropy": entropy,
        "relevance_steps": float(sum(reference)),
        "coverage_steps": float(len(reference) - sum(reference)),
        "retained_fraction": float(budget / len(tokens)),
    }

def persistent_recurrent_memory(hidden, state, wx, wh, gate_vector, steps: int = 2):
    """PRM observe -> recurrent update -> gated influence topology."""
    hidden = np.asarray(hidden, dtype=np.float64)
    state = np.asarray(state, dtype=np.float64)
    scores = hidden @ state / np.sqrt(hidden.shape[1])
    observation = _softmax(scores) @ hidden
    for _ in range(max(1, int(steps))):
        proposal = np.tanh(observation @ wx + state @ wh)
        update = 1.0 / (1.0 + np.exp(-proposal))
        state = update * proposal + (1.0 - update) * state
        state /= np.linalg.norm(state) + 1e-12
    gate = 1.0 / (1.0 + np.exp(-(hidden @ gate_vector)))
    influenced = hidden + gate[:, None] * state[None, :]
    return influenced, state, {"state_norm": float(np.linalg.norm(state)), "mean_gate": float(gate.mean())}

def register_chunk(registers, chunk_hidden, write_matrix):
    """Carry only continuous register state after clearing generated text."""
    registers = np.asarray(registers, dtype=np.float64)
    chunk = np.asarray(chunk_hidden, dtype=np.float64)
    write = np.asarray(write_matrix, dtype=np.float64)
    affinity = _softmax(registers @ chunk.T / np.sqrt(chunk.shape[1]))
    updated = np.tanh(registers + (affinity @ chunk) @ write)
    return updated, {
        "register_slots": float(len(registers)),
        "cleared_text_tokens": float(len(chunk)),
        "carry_norm": float(np.linalg.norm(updated)),
    }
