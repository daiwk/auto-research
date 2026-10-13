"""ReplaySSM equations 5/6 and acceptance protocol, in independent PyTorch code.

This reference is not a fused serving kernel. Precision casts use native FP16
or FP32 storage; FP4/FP8 correctness is exercised by the separately pinned
author Triton emulation, which itself stores dequantized values in FP32.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor


@dataclass(frozen=True)
class Record:
    alpha: Tensor
    value: Tensor
    key: Tensor
    beta: Tensor | None = None


def replay(checkpoint: Tensor, records: list[Record]) -> Tensor:
    """Equation 5, materialized only for refresh/reference checks."""
    state = checkpoint.float()
    for item in records:
        state = item.alpha[..., None, None] * state + item.value[..., :, None] * item.key[..., None, :]
    return state


def output_only(checkpoint: Tensor, records: list[Record], queries: Tensor,
                committed: int = 0) -> Tensor:
    """Equation 6 without any per-token dv-by-dk intermediate state.

    Queries are [draft, ..., dk]; records include committed history then drafts.
    The implementation intentionally exposes scalar key/query contractions.
    """
    if committed < 0 or committed + len(queries) != len(records):
        raise ValueError("queries must cover exactly the draft suffix")
    outputs = []
    for position, query in enumerate(queries):
        prefix = records[:committed + position + 1]
        decay = torch.ones_like(prefix[0].alpha)
        update = torch.zeros_like(prefix[0].value, dtype=torch.float32)
        for item in reversed(prefix):
            update = update + (decay * (item.key.float() * query.float()).sum(-1))[..., None] * item.value.float()
            decay = decay * item.alpha.float()
        anchor = torch.einsum("...vk,...k->...v", checkpoint.float(), query.float())
        outputs.append(decay[..., None] * anchor + update)
    return torch.stack(outputs)


def gdn_corrections(checkpoint: Tensor, raw: list[Record]) -> list[Record]:
    """Appendix B.3: solve all GDN residual updates with one triangular solve.

    S_j = alpha_j S_(j-1) + beta_j (v_j - alpha_j S_(j-1) k_j) k_j^T.
    Raw values are retained so refresh never reuses low-precision residuals.
    """
    if not raw or any(item.beta is None for item in raw):
        raise ValueError("GDN raw records require beta")
    alpha = torch.stack([item.alpha.float() for item in raw])
    beta = torch.stack([item.beta.float() for item in raw])
    keys = torch.stack([item.key.float() for item in raw])
    values = torch.stack([item.value.float() for item in raw])
    cumulative = alpha.cumprod(0)
    matrix = torch.eye(len(raw), device=checkpoint.device).expand(*alpha.shape[1:], len(raw), len(raw)).clone()
    rhs = []
    for j in range(len(raw)):
        projected = torch.einsum("...vk,...k->...v", checkpoint.float(), keys[j])
        rhs.append(beta[j][..., None] * (values[j] - cumulative[j][..., None] * projected))
        for i in range(j):
            decay = alpha[i + 1:j + 1].prod(0)
            matrix[..., j, i] = beta[j] * decay * (keys[i] * keys[j]).sum(-1)
    right = torch.stack(rhs).movedim(0, -2)
    residual = torch.linalg.solve_triangular(matrix, right, upper=False).movedim(-2, 0)
    return [Record(raw[j].alpha, residual[j], raw[j].key) for j in range(len(raw))]


class ReplayBuffer:
    """Algorithms 2/3: stage drafts, flush only committed input, accept a prefix.

    Pointer rollback discards rejected records; no speculative state snapshot is
    retained. The CPU reference uses a bounded list, not a native circular CUDA
    allocation; this representation difference is explicit in reports.
    """
    def __init__(self, checkpoint: Tensor, window: int = 16,
                 recurrence_dtype: torch.dtype = torch.float32,
                 read_dtype: torch.dtype = torch.float32, *, gdn: bool = False):
        if window < 1 or checkpoint.ndim < 2:
            raise ValueError("positive window and matrix checkpoint required")
        self.window, self.gdn = window, gdn
        self.recurrence_dtype, self.read_dtype = recurrence_dtype, read_dtype
        self.high = checkpoint.to(recurrence_dtype).clone()
        self.low = checkpoint.to(read_dtype).clone()
        self.committed: list[Record] = []
        self.pending: list[Record] | None = None
        self.refreshes = 0

    def _records(self, checkpoint: Tensor, raw: list[Record]) -> list[Record]:
        return gdn_corrections(checkpoint, raw) if self.gdn else raw

    def current_state(self) -> Tensor:
        return replay(self.high, self._records(self.high, self.committed))

    def verify(self, drafts: list[Record], queries: Tensor) -> Tensor:
        if self.pending is not None:
            raise RuntimeError("accept/reject the pending verification first")
        if not drafts or len(drafts) > self.window or len(queries) != len(drafts):
            raise ValueError("draft/query count must be 1..window")
        flush = len(self.committed) + len(drafts) > self.window
        anchor = self.high if flush else self.low
        raw = self.committed + drafts
        outputs = output_only(anchor, self._records(anchor, raw), queries, len(self.committed))
        if flush:
            # Recompute raw GDN residuals from HP, never from the read copy.
            refreshed = replay(self.high, self._records(self.high, self.committed))
            self.high = refreshed.to(self.recurrence_dtype)
            self.low = refreshed.to(self.read_dtype)
            self.committed = []
            self.refreshes += 1
        self.pending = drafts
        return outputs

    def accept(self, length: int) -> None:
        if self.pending is None or not 0 <= length <= len(self.pending):
            raise ValueError("acceptance requires a valid pending prefix")
        self.committed.extend(self.pending[:length])
        self.pending = None
        if len(self.committed) > self.window:
            raise RuntimeError("committed replay window overflow")


def mechanism_suite(seed: int = 42, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    checkpoint = torch.randn(2, 8, 8, device=device) * 0.1
    runner = ReplayBuffer(checkpoint, window=4)
    conventional = checkpoint.clone()
    errors, accepted = [], 0
    for cycle in range(8):
        drafts = [Record(torch.full((2,), 0.95, device=device),
                         torch.randn(2, 8, device=device) * 0.1,
                         torch.randn(2, 8, device=device) * 0.1) for _ in range(3)]
        queries = torch.randn(3, 2, 8, device=device)
        actual = runner.verify(drafts, queries)
        expected = []
        state = conventional.clone()
        for item, query in zip(drafts, queries, strict=True):
            state = replay(state, [item])
            expected.append(torch.einsum("...vk,...k->...v", state, query))
        errors.append(float((actual - torch.stack(expected)).abs().max()))
        count = cycle % 4  # exercise zero acceptance and full acceptance
        runner.accept(count)
        conventional = replay(conventional, drafts[:count])
        accepted += count
        torch.testing.assert_close(runner.current_state(), conventional, atol=2e-6, rtol=2e-6)
    return {"seed": seed, "diagnostic_only": True, "promotion_eligible": False,
            "fidelity": "core_mechanism", "evaluation_tier": "l1_mechanism",
            "max_output_error": max(errors), "accepted_tokens": accepted,
            "checkpoint_refreshes": runner.refreshes,
            "native_bandwidth_speedup_claim": False,
            "limitations": ["bounded-list reference, not fused serving/ring-buffer implementation",
                            "random recurrent inputs, no language-model quality benchmark"]}
