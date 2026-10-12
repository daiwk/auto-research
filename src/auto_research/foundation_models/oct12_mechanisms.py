"""Oct-12 foundation mechanisms, not paper-scale benchmark substitutes.

MSAR follows Eqs. 9-17 of arXiv:2610.13630. Orthros implements the
two-token-stream SWA/cross-attention algorithm of arXiv:2610.13735;
its prefill is linear for fixed window, not kernelized linear attention.
DualQuant follows Algorithm 1 of arXiv:2610.13767, with explicitly bounded
INT4 / MXINT4 reference arithmetic (no native low-bit CUDA kernel).
"""

from __future__ import annotations

import copy
import math
from dataclasses import dataclass
from typing import Callable

import torch
from torch import Tensor, nn
from torch.nn import functional as F


def rms(x: Tensor, eps: float = 1e-6) -> Tensor:
    return x * torch.rsqrt(x.float().square().mean(-1, keepdim=True) + eps).to(x.dtype)


class RMSNorm(nn.Module):
    def __init__(self, width: int):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(width))

    def forward(self, x: Tensor) -> Tensor:
        return rms(x) * self.weight


class SwiGLU(nn.Module):
    def __init__(self, width: int):
        super().__init__()
        self.gate = nn.Linear(width, 2 * width, bias=False)
        self.up = nn.Linear(width, 2 * width, bias=False)
        self.down = nn.Linear(2 * width, width, bias=False)

    def forward(self, x: Tensor) -> Tensor:
        return self.down(F.silu(self.gate(x)) * self.up(x))


class CausalAttention(nn.Module):
    def __init__(self, width: int, heads: int):
        super().__init__()
        if width % heads:
            raise ValueError("width must be divisible by heads")
        self.heads, self.head_dim = heads, width // heads
        self.q = nn.Linear(width, width, bias=False)
        self.k = nn.Linear(width, width, bias=False)
        self.v = nn.Linear(width, width, bias=False)
        self.o = nn.Linear(width, width, bias=False)

    def split(self, x: Tensor) -> Tensor:
        return x.reshape(x.shape[0], x.shape[1], self.heads, self.head_dim).transpose(1, 2)

    def merge(self, x: Tensor) -> Tensor:
        return x.transpose(1, 2).reshape(x.shape[0], x.shape[2], -1)

    def forward(self, x: Tensor) -> Tensor:
        y = F.scaled_dot_product_attention(self.split(self.q(x)), self.split(self.k(x)),
                                          self.split(self.v(x)), is_causal=True)
        return self.o(self.merge(y))


class TransformerBlock(nn.Module):
    def __init__(self, width: int, heads: int):
        super().__init__()
        self.attention_norm, self.ffn_norm = RMSNorm(width), RMSNorm(width)
        self.attention, self.ffn = CausalAttention(width, heads), SwiGLU(width)

    def forward(self, x: Tensor) -> Tensor:
        x = x + self.attention(self.attention_norm(x))
        return x + self.ffn(self.ffn_norm(x))


class TinyTransformerLM(nn.Module):
    def __init__(self, vocab: int = 256, width: int = 64, layers: int = 2,
                 heads: int = 4, max_length: int = 1024):
        super().__init__()
        self.embedding = nn.Embedding(vocab, width)
        self.position = nn.Embedding(max_length, width)
        self.blocks = nn.ModuleList(TransformerBlock(width, heads) for _ in range(layers))
        self.norm, self.head = RMSNorm(width), nn.Linear(width, vocab, bias=False)

    def embed(self, ids: Tensor, offset: int = 0) -> Tensor:
        positions = torch.arange(offset, offset + ids.shape[1], device=ids.device)
        return self.embedding(ids) + self.position(positions)[None]

    def forward(self, ids: Tensor) -> Tensor:
        x = self.embed(ids)
        for block in self.blocks:
            x = block(x)
        return self.head(self.norm(x))


class SourceExpansion(nn.Module):
    """One single-stream bank; generated views are never retained in state."""
    def __init__(self, width: int, kernels: tuple[int, ...] = (4, 8, 12)):
        super().__init__()
        self.convs = nn.ModuleList(nn.Conv1d(width, width, k, groups=width,
                                           bias=False) for k in kernels)
        for conv in self.convs:
            nn.init.zeros_(conv.weight)
            # PyTorch cross-correlation: the rightmost coefficient is delta=0.
            with torch.no_grad():
                conv.weight[:, 0, -1] = 1

    def forward(self, source: Tensor) -> Tensor:
        views = [source]
        for conv in self.convs:
            views.append(conv(F.pad(source.transpose(1, 2),
                                    (conv.kernel_size[0] - 1, 0))).transpose(1, 2))
        return torch.stack(views, dim=-2)  # [batch, token, stream, FULL width]


class DepthRead(nn.Module):
    """Per-stream full-dimensional depth softmax and sigmoid H_pre mixer."""
    def __init__(self, width: int, streams: int):
        super().__init__()
        self.query = nn.Parameter(torch.zeros(streams, width))
        self.mixer = nn.Linear(streams * width, streams)
        self.scale = nn.Parameter(torch.tensor(0.01))
        nn.init.zeros_(self.mixer.weight)
        nn.init.constant_(self.mixer.bias, math.log(1 / max(streams - 1, 1)))

    def forward(self, sources: list[Tensor], banks: list[SourceExpansion],
                *, return_weights: bool = False):
        if not sources or len(sources) != len(banks):
            raise ValueError("source / expansion banks must be nonempty and aligned")
        # Local temporary only; persistent state is the single-stream `sources`.
        expanded = torch.stack([bank(value) for bank, value in zip(banks, sources)], dim=2)
        scores = (rms(expanded) * self.query).sum(-1)
        depth_weights = scores.softmax(dim=2)
        retrieved = (depth_weights[..., None] * expanded).sum(2)
        mixed_weights = torch.sigmoid(self.scale * F.linear(
            rms(retrieved.flatten(-2)), self.mixer.weight) + self.mixer.bias)
        result = (mixed_weights[..., None] * retrieved).sum(-2)
        if return_weights:
            return result, depth_weights, mixed_weights
        return result


class MSARLM(TinyTransformerLM):
    """Real autoregressive attention/FFN branches with Block MSAR retrieval."""
    def __init__(self, *args, block_size: int = 2, kernels: tuple[int, ...] = (4, 8, 12),
                 **kwargs):
        super().__init__(*args, **kwargs)
        if block_size < 1:
            raise ValueError("block_size must be positive")
        width = self.embedding.embedding_dim
        self.block_size = block_size
        self.branch_count = 2 * len(self.blocks)
        banks = 1 + math.ceil(self.branch_count / block_size)
        self.expansions = nn.ModuleList(SourceExpansion(width, kernels) for _ in range(banks))
        self.reads = nn.ModuleList(DepthRead(width, len(kernels) + 1)
                                   for _ in range(self.branch_count))
        self.last_persistent_sources = 0

    def forward(self, ids: Tensor) -> Tensor:
        summaries, partial = [self.embed(ids)], None
        branches = []
        for block in self.blocks:
            branches.extend([(block.attention_norm, block.attention),
                             (block.ffn_norm, block.ffn)])
        for index, (norm, branch) in enumerate(branches):
            sources = summaries if partial is None else summaries + [partial]
            hidden = self.reads[index](sources, list(self.expansions[:len(sources)]))
            update = branch(norm(hidden))
            partial = update if partial is None else partial + update
            if (index + 1) % self.block_size == 0:
                summaries.append(partial)
                partial = None
        self.last_persistent_sources = len(summaries) + int(partial is not None)
        # The terminal output is merged without generating further streams.
        terminal = sum(summaries)
        if partial is not None:
            terminal = terminal + partial
        return self.head(self.norm(terminal))


@dataclass
class KVState:
    key: Tensor
    value: Tensor


def sliding_window_attention(q: Tensor, k: Tensor, v: Tensor, window: int) -> Tensor:
    """O(T * window) reference execution, no T-by-T base attention matrix."""
    if window < 1 or q.shape[-2] != k.shape[-2]:
        raise ValueError("positive window and aligned full-sequence Q/K required")
    length = q.shape[-2]
    window = min(window, length)
    key_windows = F.pad(k, (0, 0, window - 1, 0)).unfold(-2, window, 1).movedim(-1, -2)
    value_windows = F.pad(v, (0, 0, window - 1, 0)).unfold(-2, window, 1).movedim(-1, -2)
    scores = (q.unsqueeze(-2) * key_windows).sum(-1) / math.sqrt(q.shape[-1])
    valid = (torch.arange(length, device=q.device)[:, None] >=
             torch.arange(window - 1, -1, -1, device=q.device)[None])
    scores = scores.masked_fill(~valid, -torch.inf)
    return (scores.softmax(-1)[..., None] * value_windows).sum(-2)


class OrthrosAttention(CausalAttention):
    def __init__(self, width: int, heads: int, window: int):
        super().__init__(width, heads)
        if window < 1:
            raise ValueError("window must be positive")
        self.window = window
        self.base_alpha = nn.Parameter(torch.ones(width))
        self.base_beta = nn.Parameter(torch.zeros(width))
        self.output_alpha = nn.Parameter(torch.ones(width))
        self.output_beta = nn.Parameter(torch.zeros(width))

    def queries(self, base: Tensor, output: Tensor) -> tuple[Tensor, Tensor]:
        return (self.split(self.q(base) * self.base_alpha + self.base_beta),
                self.split(self.q(output) * self.output_alpha + self.output_beta))

    def forward_pair(self, base: Tensor, output: Tensor, output_start: int):
        q, cross_q = self.queries(base, output)
        key, value = self.split(self.k(base)), self.split(self.v(base))
        local = sliding_window_attention(q, key, value, self.window)
        positions = torch.arange(output_start, base.shape[1], device=base.device)
        mask = torch.arange(base.shape[1], device=base.device)[None] <= positions[:, None]
        cross = F.scaled_dot_product_attention(cross_q, key, value, attn_mask=mask)
        return self.o(self.merge(local)), self.o(self.merge(cross)), KVState(key, value)

    def decode_pair(self, base: Tensor, output: Tensor, state: KVState):
        q, cross_q = self.queries(base, output)
        key = torch.cat([state.key, self.split(self.k(base))], dim=-2)
        value = torch.cat([state.value, self.split(self.v(base))], dim=-2)
        local = F.scaled_dot_product_attention(q, key[..., -self.window:, :],
                                               value[..., -self.window:, :])
        cross = F.scaled_dot_product_attention(cross_q, key, value)
        return self.o(self.merge(local)), self.o(self.merge(cross)), KVState(key, value)


class OrthrosLM(TinyTransformerLM):
    def __init__(self, *args, window: int = 16, **kwargs):
        super().__init__(*args, **kwargs)
        for block in self.blocks:
            width = self.embedding.embedding_dim
            old = block.attention
            block.attention = OrthrosAttention(width, old.heads, window)
            block.attention.load_state_dict(old.state_dict(), strict=False)

    @classmethod
    def from_transformer(cls, model: TinyTransformerLM, window: int = 16):
        """Weight conversion, preserving Q/K/V/O, FFN, norms, embedding/head.

        Only the four stream-affine vectors are new, initialized as identities.
        Subsequent conversion training is ordinary next-token cross entropy.
        """
        first = model.blocks[0].attention
        converted = cls(model.embedding.num_embeddings, model.embedding.embedding_dim,
                        len(model.blocks), first.heads, model.position.num_embeddings,
                        window=window)
        missing, unexpected = converted.load_state_dict(copy.deepcopy(model.state_dict()), strict=False)
        expected = {f"blocks.{i}.attention.{name}" for i in range(len(model.blocks))
                    for name in ("base_alpha", "base_beta", "output_alpha", "output_beta")}
        if set(missing) != expected or unexpected:
            raise ValueError("unsupported transformer conversion layout")
        return converted.to(model.embedding.weight.device)

    def forward_with_state(self, ids: Tensor, output_start: int = 0):
        if not 0 <= output_start < ids.shape[1]:
            raise ValueError("output_start must identify at least one output token")
        base = self.embed(ids)
        output = base[:, output_start:].clone()
        states = []
        for block in self.blocks:
            local, cross, state = block.attention.forward_pair(
                block.attention_norm(base), block.attention_norm(output), output_start)
            base, output = base + local, output + cross
            base = base + block.ffn(block.ffn_norm(base))
            output = output + block.ffn(block.ffn_norm(output))
            states.append(state)
        return self.head(self.norm(output)), states

    def forward(self, ids: Tensor, output_start: int = 0) -> Tensor:
        return self.forward_with_state(ids, output_start)[0]

    def prefill(self, prompt: Tensor):
        return self.forward_with_state(prompt, prompt.shape[1] - 1)

    def decode(self, token: Tensor, states: list[KVState]):
        if token.shape[1] != 1 or len(states) != len(self.blocks):
            raise ValueError("decode requires one token and one cache per layer")
        offset = states[0].key.shape[-2]
        if any(state.key.shape[-2] != offset for state in states):
            raise ValueError("layer cache lengths disagree")
        base = self.embed(token, offset)
        output, new_states = base.clone(), []
        for block, state in zip(self.blocks, states):
            local, cross, updated = block.attention.decode_pair(
                block.attention_norm(base), block.attention_norm(output), state)
            base, output = base + local, output + cross
            base = base + block.ffn(block.ffn_norm(base))
            output = output + block.ffn(block.ffn_norm(output))
            new_states.append(updated)
        return self.head(self.norm(output)), new_states


def int4_grid(x: Tensor) -> Tensor:
    """Signed INT4 codebook [-8, 7], round-to-nearest reference quantizer."""
    return x.round().clamp(-8, 7)


def project_inverse_scale(x: Tensor, scale_format: str) -> Tensor:
    if scale_format == "bf16":
        return x.clamp(2.0 ** -126, 2.0 ** 126).to(torch.bfloat16).float()
    if scale_format == "e8m0":
        x = x.clamp(2.0 ** -126, 2.0 ** 126)
        low = x.log2().floor().exp2()
        high = (low * 2).clamp(max=2.0 ** 126)
        return torch.where(x - low <= high - x, low, high)
    raise ValueError("only bf16 INT4 and E8M0 MXINT4 scale reference formats are supported")


@dataclass
class DualScaleTile:
    codes: Tensor
    row_inverse: Tensor
    column_inverse: Tensor
    mse_history: list[float]

    def reconstruct(self) -> Tensor:
        return self.codes * self.row_inverse[:, None] * self.column_inverse[None]


def solve_dual_scale(weight: Tensor, iterations: int = 15, scale_format: str = "bf16",
                     quantizer: Callable[[Tensor], Tensor] = int4_grid) -> DualScaleTile:
    """Weight-only variable-splitting BCD, exact scalar outer-scale updates.

    The quantizer is a fixed-grid black box. Outer inverse scales are solved
    with grid assignments fixed, projected, synchronized to inner copies,
    and assignments recomputed between row and column updates.
    """
    if weight.ndim != 2 or iterations < 1 or not torch.isfinite(weight).all():
        raise ValueError("finite matrix and positive iterations are required")
    w = weight.detach().float()
    row_inverse = project_inverse_scale(w.abs().amax(1).clamp_min(1e-8) / 7, scale_format)
    column_inverse = torch.ones(w.shape[1], device=w.device)
    history = []

    def codes():
        return quantizer(w / row_inverse[:, None] / column_inverse[None])

    for _ in range(iterations):
        q = codes()  # inner copies held fixed
        r = q * column_inverse[None]
        denominator = r.square().sum(1)
        row_candidate = (w * r).sum(1) / denominator.clamp_min(1e-30)
        row_candidate = torch.where(denominator > 0, row_candidate, torch.ones_like(row_candidate))
        row_inverse = project_inverse_scale(row_candidate, scale_format)
        q = codes()  # synchronize row inner/outer copies before column solve
        s = q * row_inverse[:, None]
        denominator = s.square().sum(0)
        col_candidate = (w * s).sum(0) / denominator.clamp_min(1e-30)
        col_candidate = torch.where(denominator > 0, col_candidate, torch.ones_like(col_candidate))
        column_inverse = project_inverse_scale(col_candidate, scale_format)
        q = codes()  # synchronize column inner/outer copies
        history.append(float((w - q * row_inverse[:, None] * column_inverse[None]).square().mean()))
    return DualScaleTile(q, row_inverse, column_inverse, history)


def activation_int4(x: Tensor, scale_format: str = "bf16") -> Tensor:
    scale = project_inverse_scale(x.float().abs().amax(-1, keepdim=True).clamp_min(1e-8) / 7,
                                  scale_format)
    return int4_grid(x.float() / scale) * scale


class DualQuantLinear(nn.Module):
    """Tile/group W4A4 software simulation; stores codes as FP tensors.

    INT4 has BF16 external scales; MXINT4 enforces E8M0 scales. No packing,
    FP4 codebook, FP4 kernel, memory-saving or throughput claim is made.
    Column scales are derived from weights only. Activation rescaling and
    activation quantization are actually executed in forward.
    """
    def __init__(self, linear: nn.Linear, group_size: int = 32, tile_rows: int = 128,
                 iterations: int = 15, scale_format: str = "bf16", dual: bool = True):
        super().__init__()
        if group_size < 1 or tile_rows < 1:
            raise ValueError("tile sizes must be positive")
        self.in_features, self.out_features = linear.in_features, linear.out_features
        self.group_size, self.tile_rows, self.scale_format = group_size, tile_rows, scale_format
        self.register_buffer("reference_weight", linear.weight.detach().clone())
        self.register_buffer("bias", None if linear.bias is None else linear.bias.detach().clone())
        self.tiles = []
        for row in range(0, self.out_features, tile_rows):
            for col in range(0, self.in_features, group_size):
                w = linear.weight[row:row + tile_rows, col:col + group_size].detach().float()
                if dual:
                    tile = solve_dual_scale(w, iterations, scale_format)
                else:
                    ri = project_inverse_scale(w.abs().amax(1).clamp_min(1e-8) / 7, scale_format)
                    tile = DualScaleTile(int4_grid(w / ri[:, None]), ri,
                                         torch.ones(w.shape[1], device=w.device), [])
                index = len(self.tiles)
                for name, tensor in [("q", tile.codes), ("r", tile.row_inverse),
                                     ("c", tile.column_inverse)]:
                    self.register_buffer(f"{name}_{index}", tensor)
                self.tiles.append((row, col, tuple(w.shape), tile.mse_history))

    def forward(self, x: Tensor) -> Tensor:
        outputs = []
        for row in range(0, self.out_features, self.tile_rows):
            total = None
            for index, (tile_row, col, shape, _) in enumerate(self.tiles):
                if tile_row != row:
                    continue
                q, ri, ci = (getattr(self, f"{name}_{index}") for name in ("q", "r", "c"))
                scaled = x[..., col:col + shape[1]].float() * ci[None].reshape(
                    (1,) * (x.ndim - 1) + (shape[1],))
                part = F.linear(activation_int4(scaled, self.scale_format), q) * ri
                total = part if total is None else total + part
            outputs.append(total)
        result = torch.cat(outputs, dim=-1).to(x.dtype)
        return result if self.bias is None else result + self.bias

    def weight_mse(self) -> float:
        reconstructed = torch.empty_like(self.reference_weight, dtype=torch.float32)
        for index, (row, col, shape, _) in enumerate(self.tiles):
            q, ri, ci = (getattr(self, f"{name}_{index}") for name in ("q", "r", "c"))
            reconstructed[row:row + shape[0], col:col + shape[1]] = q * ri[:, None] * ci[None]
        return float((reconstructed - self.reference_weight.float()).square().mean())
