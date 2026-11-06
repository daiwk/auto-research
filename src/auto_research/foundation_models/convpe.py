"""ConvPE v1 Eqs. (2)-(4): the default 1-D causal score bias, not a serving kernel."""

from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F


REQUIRES_GPU_VALIDATION = True


class ConvPEBias(nn.Module):
    """Ungrouped, unfactorized ConvPE with modulo sharing of bias heads.

    `compact_bias` avoids a dense score matrix. `forward` scatters the same
    values into a dense reference with keys starting at absolute position 0.
    The caller still applies its own causal/attention mask and softmax.
    """

    def __init__(
        self, model_dim: int, channels: int, window: int, attention_heads: int, bias_heads: int,
    ) -> None:
        super().__init__()
        dims = (model_dim, channels, window, attention_heads, bias_heads)
        if any(type(value) is not int or value <= 0 for value in dims):
            raise ValueError("dimensions must be positive integers")
        if attention_heads % bias_heads:
            raise ValueError("bias_heads must divide attention_heads")
        self.model_dim = model_dim
        self.window = window
        self.attention_heads = attention_heads
        self.bias_heads = bias_heads
        self.projection = nn.Linear(model_dim, channels, bias=False)
        self.convolution = nn.Conv1d(channels, bias_heads * window, window, bias=True)

    def compact_bias(self, hidden: Tensor, *, history: Tensor | None = None) -> Tensor:
        """Return [batch, queries, bias heads, relative lags].

        History is the preceding raw hidden states (at most window-1), in
        chronological order. At the sequence start, missing history is zero.
        """
        if (
            not isinstance(hidden, Tensor) or hidden.ndim != 3 or hidden.shape[-1] != self.model_dim
            or hidden.shape[0] == 0 or hidden.shape[1] == 0 or not hidden.is_floating_point()
        ):
            raise ValueError("hidden must be a nonempty floating [batch, queries, model_dim] tensor")
        if history is not None:
            if (
                not isinstance(history, Tensor) or history.ndim != 3
                or history.shape[0] != hidden.shape[0] or history.shape[-1] != self.model_dim
                or history.shape[1] >= self.window or history.device != hidden.device
                or history.dtype != hidden.dtype
            ):
                raise ValueError("history must match hidden and contain at most window-1 positions")
        query_count = hidden.shape[1]
        states = hidden if history is None else torch.cat((history, hidden), dim=1)
        projected = self.projection(states).transpose(1, 2)
        scores = self.convolution(F.pad(projected, (self.window - 1, 0)))
        return scores[:, :, -query_count:].transpose(1, 2).reshape(
            hidden.shape[0], query_count, self.bias_heads, self.window,
        )

    def forward(self, hidden: Tensor, *, query_start: int = 0, history: Tensor | None = None) -> Tensor:
        """Return [batch, attention heads, queries, keys], with key length start+queries."""
        if type(query_start) is not int or query_start < 0:
            raise ValueError("query_start must be a nonnegative integer")
        compact = self.compact_bias(hidden, history=history)
        history_count = 0 if history is None else history.shape[1]
        if history_count != min(query_start, self.window - 1):
            raise ValueError("need exactly min(query_start, window-1) history positions")
        batch, queries, _, _ = compact.shape
        keys = query_start + queries
        heads = torch.arange(self.attention_heads, device=hidden.device) % self.bias_heads
        query_positions = torch.arange(query_start, keys, device=hidden.device)
        key_positions = torch.arange(keys, device=hidden.device)
        lags = query_positions[:, None] - key_positions[None, :]
        valid = (lags >= 0) & (lags < self.window)
        by_head = compact.permute(0, 2, 1, 3).index_select(1, heads)
        indices = lags.clamp(0, self.window - 1).expand(batch, self.attention_heads, queries, keys)
        return torch.where(valid, by_head.gather(-1, indices), 0.0)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Check the formula, causal prefix invariance, and differentiation on tiny tensors."""
    if device not in ("cpu", "cuda"):
        raise ValueError("diagnostic device must be cpu or cuda")
    with torch.random.fork_rng(devices=[]):
        torch.random.default_generator.manual_seed(seed)
        layer = ConvPEBias(6, 3, 3, 4, 2).to(device=device, dtype=torch.float64)
        x = torch.randn(2, 7, 6, dtype=torch.float64).to(device).requires_grad_()
    dense = layer(x)
    projected = x.detach() @ layer.projection.weight.detach().T
    kernel = layer.convolution.weight.detach()
    intercept = layer.convolution.bias.detach()
    oracle = torch.zeros_like(dense)
    for head in range(layer.attention_heads):
        for pos in range(x.shape[1]):
            for lag in range(min(pos + 1, layer.window)):
                channel = (head % layer.bias_heads) * layer.window + lag
                value = intercept[channel].expand(x.shape[0]).clone()
                for tap in range(layer.window):
                    source = pos - layer.window + 1 + tap
                    if source >= 0:
                        value += (projected[:, source] * kernel[channel, :, tap]).sum(-1)
                oracle[:, head, pos, pos - lag] = value
    split = 4
    prefix = layer(x[:, :split])
    chunk = layer(x[:, split:], query_start=split, history=x[:, split-2:split])
    gradients = torch.autograd.grad(dense.square().mean(), (x, *layer.parameters()))
    oracle_error = (dense - oracle).abs().max().item()
    prefix_error = (dense[:, :, :split, :split] - prefix).abs().max().item()
    chunk_error = (dense[:, :, split:, :] - chunk).abs().max().item()
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "formula_max_abs_error": oracle_error,
            "causal_prefix_max_abs_error": prefix_error,
            "decode_chunk_max_abs_error": chunk_error,
            "hidden_gradient_l2": gradients[0].norm().item(),
        },
        "checks": {
            "eq_2_to_4": oracle_error <= 1e-10,
            "future_invariant_prefix": prefix_error <= 1e-10,
            "chunk_matches_prefill": chunk_error <= 1e-10,
            "modulo_head_sharing": torch.equal(dense[:, :2], dense[:, 2:]),
            "finite_nonzero_gradients": all(
                bool(grad.isfinite().all()) and grad.norm().item() > 0 for grad in gradients
            ),
            "requested_device_executed": dense.device.type == device,
        },
    }
