"""Reference kernels for the 2026-09-14--15 foundation/multimodal batch.

These kernels preserve each paper's defining state transition.  They are small
enough for deterministic contract tests and are explicitly not paper-scale
training or serving reproductions.
"""

from __future__ import annotations

import hashlib

import numpy as np


def _softmax(values):
    values = np.asarray(values, dtype=np.float64)
    shifted = values - np.max(values, axis=-1, keepdims=True)
    exp = np.exp(shifted)
    return exp / (exp.sum(axis=-1, keepdims=True) + 1e-12)


def echo_candidates(early_logits, final_logits, retrieved_tokens=(), top_k: int = 4):
    """ECHO asymmetric bonus-logit candidate union for the next draft tree."""
    early = np.asarray(early_logits, dtype=np.float64)
    final = np.asarray(final_logits, dtype=np.float64)
    if early.shape != final.shape or early.ndim != 1:
        raise ValueError("early_logits and final_logits must be equal 1-D arrays")
    k = max(1, min(int(top_k), len(early)))
    early_bonus = early + np.maximum(final - early, 0.0)
    final_bonus = final + np.maximum(early - final, 0.0)
    ranked = list(np.argsort(early_bonus)[-k:][::-1])
    ranked += list(np.argsort(final_bonus)[-k:][::-1])
    ranked += [int(token) for token in retrieved_tokens if 0 <= int(token) < len(early)]
    candidates = tuple(dict.fromkeys(ranked))
    return candidates, {
        "early_bonus_mass": float(np.maximum(final - early, 0.0).sum()),
        "final_bonus_mass": float(np.maximum(early - final, 0.0).sum()),
        "candidate_count": float(len(candidates)),
    }


def echo_lossless_verify(draft_probabilities, target_probabilities, uniforms):
    """Exact speculative accept/reject correction for an ECHO draft path."""
    draft = np.asarray(draft_probabilities, dtype=np.float64)
    target = np.asarray(target_probabilities, dtype=np.float64)
    uniforms = np.asarray(uniforms, dtype=np.float64)
    if draft.shape != target.shape or draft.ndim != 2:
        raise ValueError("draft and target probabilities must be equal 2-D arrays")
    if len(uniforms) < len(draft):
        raise ValueError("one uniform variate is required per draft position")
    accepted = 0
    correction = None
    for index, (q, p) in enumerate(zip(draft, target)):
        token = int(np.argmax(q))
        ratio = min(1.0, float(p[token] / max(q[token], 1e-12)))
        if uniforms[index] <= ratio:
            accepted += 1
            continue
        correction = np.maximum(p - q, 0.0)
        correction /= correction.sum() + 1e-12
        break
    return accepted, correction, {
        "accepted_tokens": float(accepted),
        "state_reuse_fraction": float(accepted / max(1, len(draft))),
        "lossless_correction_used": float(correction is not None),
    }


def videomm_select(tokens, query, group_size: int = 4, keep_groups: int = 2, consensus_margin: float = 0.08):
    """VideoMM macro proxy selection followed by adaptive micro activation."""
    tokens = np.asarray(tokens, dtype=np.float64)
    query = np.asarray(query, dtype=np.float64)
    if tokens.ndim != 2 or tokens.shape[1] != len(query):
        raise ValueError("tokens must be [N,D] and query must be [D]")
    groups = np.array_split(np.arange(len(tokens)), max(1, int(np.ceil(len(tokens) / group_size))))
    macro = np.stack([tokens[group].mean(axis=0) for group in groups])
    scores = macro @ query / ((np.linalg.norm(macro, axis=1) * np.linalg.norm(query)) + 1e-12)
    order = np.argsort(scores)[::-1]
    chosen = order[: max(1, min(int(keep_groups), len(groups)))]
    margin = float(scores[order[0]] - scores[order[1]]) if len(order) > 1 else 1.0
    # Ambiguous macro consensus recruits one extra high-fidelity region.
    if margin < consensus_margin and len(chosen) < len(groups):
        chosen = order[: len(chosen) + 1]
    indices = np.concatenate([groups[index] for index in chosen])
    return tokens[indices], indices, {
        "macro_groups": float(len(groups)),
        "activated_micro_tokens": float(len(indices)),
        "retained_fraction": float(len(indices) / max(1, len(tokens))),
        "consensus_margin": margin,
    }


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


def reproducible_reduce(shards):
    """OPEN-1B fixed-order float64 reduction with a canonical state hash."""
    arrays = [np.asarray(shard, dtype=np.float64) for shard in shards]
    if not arrays or any(array.shape != arrays[0].shape for array in arrays):
        raise ValueError("non-empty equal-shaped shards required")
    total = np.zeros_like(arrays[0])
    for array in arrays:  # order is part of the contract
        total = np.add(total, array, dtype=np.float64)
    reduced = total * np.float64(1.0 / len(arrays))
    digest = hashlib.sha256(reduced.astype("<f8", copy=False).tobytes()).hexdigest()
    return reduced, {"shards": float(len(arrays)), "state_hash": digest, "bitwise_replay": True}


def echo_cuda_kernel(early_logits, final_logits, top_k: int = 8):
    """CUDA-compatible ECHO bonus-logit union using torch tensors."""
    import torch

    if early_logits.device.type != "cuda" or final_logits.device.type != "cuda":
        raise ValueError("echo_cuda_kernel requires CUDA tensors")
    k = max(1, min(int(top_k), early_logits.numel()))
    early_bonus = early_logits + torch.relu(final_logits - early_logits)
    final_bonus = final_logits + torch.relu(early_logits - final_logits)
    candidates = torch.unique(torch.cat((torch.topk(early_bonus, k).indices, torch.topk(final_bonus, k).indices)))
    return candidates, early_bonus, final_bonus


def videomm_cuda_kernel(tokens, query, group_size: int = 8, keep_groups: int = 4):
    """CUDA-compatible macro-proxy selection and micro-token gather."""
    import torch

    if tokens.device.type != "cuda" or query.device.type != "cuda":
        raise ValueError("videomm_cuda_kernel requires CUDA tensors")
    usable = tokens.shape[0] - tokens.shape[0] % group_size
    macro = tokens[:usable].reshape(-1, group_size, tokens.shape[1]).mean(dim=1)
    scores = torch.nn.functional.cosine_similarity(macro, query.unsqueeze(0), dim=1)
    chosen = torch.topk(scores, min(int(keep_groups), len(macro))).indices
    offsets = torch.arange(group_size, device=tokens.device)
    indices = (chosen[:, None] * group_size + offsets[None, :]).reshape(-1)
    return tokens.index_select(0, indices), indices, scores
