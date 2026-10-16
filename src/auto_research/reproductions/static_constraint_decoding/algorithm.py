"""Independent PyTorch implementation of STATIC Algorithms 1/2 (2602.22647).

Construction is CPU/offline. All decode-time sparse extraction, masking, beam
selection and state reordering stay on the input device. Scores are normalized
before constraints: masking must not renormalize the language-model probability.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import torch
from torch import Tensor


@dataclass(frozen=True)
class StaticTrie:
    row_ptr: Tensor
    columns: Tensor
    targets: Tensor
    terminal: Tensor
    dense_row: Tensor
    dense_targets: Tensor
    max_branches: tuple[int, ...]
    vocab_size: int
    depth: int
    dense_depth: int

    @classmethod
    def build(cls, sequences: Iterable[Iterable[int]], vocab_size: int, *,
              dense_depth: int = 0, eos_token: int | None = None) -> StaticTrie:
        if vocab_size < 1 or dense_depth not in (0, 1, 2):
            raise ValueError("positive vocabulary and dense_depth in 0..2 required")
        rows = [tuple(row) for row in sequences]
        if not rows or any(not row for row in rows):
            raise ValueError("constraints must contain nonempty sequences")
        if any(type(token) is not int or not 0 <= token < vocab_size for row in rows for token in row):
            raise ValueError("constraint tokens must be vocabulary integers")
        if eos_token is not None:
            if not 0 <= eos_token < vocab_size or any(eos_token in row for row in rows):
                raise ValueError("EOS must be reserved and absent from item identifiers")
            rows = [row + (eos_token,) for row in rows]
        elif len({len(row) for row in rows}) != 1:
            raise ValueError("variable-length identifiers require an explicit EOS token")
        # State zero is a dead sink; the empty prefix is state one.
        edges: list[dict[int, int]] = [{}, {}]
        depths = [0, 0]
        ends = [False, False]
        for row in sorted(set(rows)):
            state = 1
            for token in row:
                if token not in edges[state]:
                    edges[state][token] = len(edges)
                    edges.append({})
                    depths.append(depths[state] + 1)
                    ends.append(False)
                state = edges[state][token]
            ends[state] = True
        depth = max(depths)
        if dense_depth > depth:
            raise ValueError("dense_depth exceeds identifier depth")
        ptr, cols, targets = [0], [], []
        for row in edges:
            for token, state in sorted(row.items()):
                cols.append(token)
                targets.append(state)
            ptr.append(len(cols))
        # Pad once for speculative fixed-width gather beyond the last CSR row.
        maximum = max(map(len, edges))
        cols.extend([0] * maximum)
        targets.extend([0] * maximum)
        shallow = [i for i, d in enumerate(depths) if i and d < dense_depth]
        if len(shallow) * vocab_size > 2_000_000:
            raise ValueError("dense lookup exceeds the bounded construction budget; use dense_depth=0")
        dense = torch.zeros((len(shallow) + 1, vocab_size), dtype=torch.long)
        mapping = torch.zeros(len(edges), dtype=torch.long)
        for index, state in enumerate(shallow, 1):
            mapping[state] = index
            for token, target in edges[state].items():
                dense[index, token] = target
        branches = tuple(max((len(edges[i]) for i, d in enumerate(depths) if i and d == level), default=0)
                         for level in range(depth))
        return cls(torch.tensor(ptr), torch.tensor(cols), torch.tensor(targets),
                   torch.tensor(ends), mapping, dense, branches, vocab_size, depth, dense_depth)

    def to(self, device) -> StaticTrie:
        return StaticTrie(*(value.to(device) for value in
                            (self.row_ptr, self.columns, self.targets, self.terminal,
                             self.dense_row, self.dense_targets)),
                          self.max_branches, self.vocab_size, self.depth, self.dense_depth)

    def candidates(self, log_probs: Tensor, nodes: Tensor, step: int) -> tuple[Tensor, Tensor, Tensor]:
        """Return candidate scores/tokens/next states without dense CSR expansion."""
        if not 0 <= step < self.depth or nodes.dtype != torch.long:
            raise ValueError("invalid decoding step or node dtype")
        if log_probs.shape != (*nodes.shape, self.vocab_size):
            raise ValueError("log probabilities and node batch shapes differ")
        if log_probs.device != self.row_ptr.device or nodes.device != self.row_ptr.device:
            raise ValueError("trie, probabilities and node state must share a device")
        if step < self.dense_depth:
            next_nodes = self.dense_targets[self.dense_row[nodes]]
            tokens = torch.arange(self.vocab_size, device=nodes.device).expand_as(next_nodes)
            return log_probs.masked_fill(next_nodes == 0, -torch.inf), tokens, next_nodes
        width = self.max_branches[step]
        offsets = torch.arange(width, device=nodes.device)
        starts = self.row_ptr[nodes]
        lengths = self.row_ptr[nodes + 1] - starts
        indices = starts[..., None] + offsets
        tokens, next_nodes = self.columns[indices], self.targets[indices]
        valid = offsets < lengths[..., None]
        return (log_probs.gather(-1, tokens).masked_fill(~valid, -torch.inf), tokens,
                next_nodes.masked_fill(~valid, 0))


def beam_step(trie: StaticTrie, logits: Tensor, nodes: Tensor, scores: Tensor,
              prefixes: Tensor, *, step: int, beam_width: int) -> dict[str, Tensor]:
    if logits.ndim != 3 or scores.shape != nodes.shape or prefixes.shape[:2] != nodes.shape:
        raise ValueError("expected batch × beam logits, scores, nodes and prefixes")
    if prefixes.shape[2] != step or beam_width < 1:
        raise ValueError("prefix length must match step and beam width must be positive")
    log_probs = logits.log_softmax(-1)
    candidate_scores, tokens, targets = trie.candidates(log_probs, nodes, step)
    combined = candidate_scores + scores[..., None]
    batch, beams, choices = combined.shape
    count = min(beam_width, beams * choices)
    selected_scores, indices = combined.reshape(batch, -1).topk(count, dim=-1)
    parents = indices // choices
    selected_tokens = tokens.reshape(batch, -1).gather(1, indices)
    selected_nodes = targets.reshape(batch, -1).gather(1, indices)
    alive = torch.isfinite(selected_scores)
    selected_nodes = selected_nodes.masked_fill(~alive, 0)
    old = prefixes.gather(1, parents[..., None].expand(batch, count, step))
    return {"prefixes": torch.cat((old, selected_tokens[..., None]), -1),
            "nodes": selected_nodes, "scores": selected_scores, "alive": alive,
            "finished": alive & trie.terminal[selected_nodes], "parents": parents}
