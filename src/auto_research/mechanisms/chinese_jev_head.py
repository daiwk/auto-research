"""Extracted unchanged from auto_research.foundation_latest_20260930; stable mechanism boundary."""
from __future__ import annotations



class ChineseJevHead:
    """Compact executable candidate-marker head preserving Chinese-Jev Eq. (5)."""

    def __new__(cls, hidden_size: int, decision_types: int = 3):
        import torch.nn as nn

        class _Head(nn.Module):
            def __init__(self):
                super().__init__()
                self.type_embedding = nn.Embedding(decision_types, hidden_size)
                self.decision = nn.TransformerEncoderLayer(hidden_size, 4, 2 * hidden_size, batch_first=True)
                self.scorer = nn.Sequential(nn.Linear(hidden_size, hidden_size), nn.GELU(), nn.Linear(hidden_size, 1))

            def forward(self, candidate_hidden, decision_type):
                hidden = candidate_hidden + self.type_embedding(decision_type)[:, None, :]
                return self.scorer(self.decision(hidden)).squeeze(-1)

        return _Head()
