"""Executable PN-Mix H3/L1 cache, following arXiv:2610.19605v1, Eqs. 2/6/7.

This is a correctness-oriented PyTorch reference, not the paper's fused Triton
kernel: attention really consumes unpacked quantized keys/values, but creates a
dense dequantized temporary. No production memory/throughput claim follows.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor


def _states(x: Tensor, name: str) -> None:
    if x.ndim != 4 or any(size <= 0 for size in x.shape):
        raise ValueError(f"{name} must have non-empty [batch, heads, tokens, channels] shape")
    if not x.is_floating_point() or not torch.isfinite(x).all():
        raise ValueError(f"{name} must contain finite floating-point states")


def _pair_view(x: Tensor, layout: str) -> Tensor:
    if x.shape[-1] % 2:
        raise ValueError("RoPE head dimension must be even")
    if layout == "adjacent":
        return x.reshape(*x.shape[:-1], -1, 2)
    if layout == "split":
        return torch.stack(x.chunk(2, dim=-1), dim=-1)
    raise ValueError("pair_layout must be adjacent or split (Hugging Face Llama)")


def pair_norm_scores(query: Tensor, key: Tensor, *, pair_layout: str = "adjacent") -> Tensor:
    """Eq. 6: prefill-only mean norms, with contiguous grouped-query head averaging."""
    _states(query, "query")
    _states(key, "key")
    if query.device != key.device or query.shape[0] != key.shape[0]:
        raise ValueError("query/key batch and device must agree")
    if query.shape[2:] != key.shape[2:] or query.shape[1] % key.shape[1]:
        raise ValueError(
            "prefill lengths/dimensions must agree and query heads must divide KV heads"
        )
    qnorm = _pair_view(query.float(), pair_layout).norm(dim=-1).mean(dim=-2)
    knorm = _pair_view(key.float(), pair_layout).norm(dim=-1).mean(dim=-2)
    grouped = qnorm.reshape(key.shape[0], key.shape[1], -1, key.shape[-1] // 2).mean(2)
    return grouped * knorm


def select_salient_pairs(scores: Tensor, high_ratio: float) -> Tensor:
    """Select floor(r*d/2) whole pairs; stable tie breaking is deterministic."""
    if scores.ndim != 3 or not torch.isfinite(scores).all() or (scores < 0).any():
        raise ValueError("scores must be finite nonnegative [batch, KV heads, pairs]")
    if not math.isfinite(high_ratio) or not 0 <= high_ratio <= 1:
        raise ValueError("high_ratio must be in [0, 1]")
    count = math.floor(scores.shape[-1] * high_ratio)
    indices = torch.argsort(scores, dim=-1, descending=True, stable=True)[..., :count]
    return torch.zeros_like(scores, dtype=torch.bool).scatter_(-1, indices, True)


def pack_codes(codes: Tensor, bits: int, *, dim: int = -1) -> Tensor:
    """Pack 1/2/4-bit unsigned codes into bytes along one explicit dimension."""
    if bits not in (1, 2, 4):
        raise ValueError("packing supports 1, 2 or 4 bits")
    if codes.dtype != torch.uint8 or (codes > (1 << bits) - 1).any():
        raise ValueError("codes must be uint8 and within the requested bit width")
    x = codes.movedim(dim, -1)
    per_byte = 8 // bits
    padding = (-x.shape[-1]) % per_byte
    if padding:
        x = torch.nn.functional.pad(x, (0, padding))
    x = x.reshape(*x.shape[:-1], x.shape[-1] // per_byte, per_byte).long()
    shifts = torch.arange(per_byte, device=x.device) * bits
    packed = (x << shifts).sum(-1).to(torch.uint8)
    return packed.movedim(-1, dim)


def unpack_codes(packed: Tensor, bits: int, length: int, *, dim: int = -1) -> Tensor:
    if bits not in (1, 2, 4) or packed.dtype != torch.uint8 or length < 0:
        raise ValueError("invalid packed representation")
    x = packed.movedim(dim, -1)
    per_byte = 8 // bits
    if x.shape[-1] != math.ceil(length / per_byte):
        raise ValueError("packed length does not match code length")
    shifts = torch.arange(per_byte, device=x.device) * bits
    codes = ((x.long().unsqueeze(-1) >> shifts) & ((1 << bits) - 1)).to(torch.uint8)
    return codes.flatten(-2)[..., :length].movedim(-1, dim)


def _channel_mask(pair_mask: Tensor, layout: str) -> Tensor:
    if layout == "adjacent":
        return pair_mask.repeat_interleave(2, dim=-1)
    if layout == "split":
        return torch.cat((pair_mask, pair_mask), dim=-1)
    raise ValueError("unknown pair layout")


def asymmetric_quantize(
    x: Tensor, bits: Tensor | int, *, dim: int
) -> tuple[Tensor, Tensor, Tensor]:
    """Eq. 2 and the Eq. 7 midpoint correction for every one-bit group.

    Metadata follows input dtype. FP16 inputs reproduce the paper's FP16
    metadata; float32 CPU tests retain float32 and report its actual storage.
    Constant groups are represented exactly without division by zero.
    """
    if not x.is_floating_point() or not torch.isfinite(x).all():
        raise ValueError("quantization input must be finite floating point")
    bit_tensor = torch.as_tensor(bits, device=x.device)
    if not torch.all((bit_tensor >= 1) & (bit_tensor <= 8) & (bit_tensor == bit_tensor.long())):
        raise ValueError("bits must be integers between 1 and 8")
    minimum = x.float().amin(dim=dim, keepdim=True)
    maximum = x.float().amax(dim=dim, keepdim=True)
    levels = (2**bit_tensor - 1).float()
    scale = (maximum - minimum) / levels
    offset = minimum
    one_bit = bit_tensor == 1
    scale = torch.where(one_bit, (maximum - minimum) / 2, scale).to(x.dtype)
    offset = torch.where(one_bit, (3 * minimum + maximum) / 4, offset).to(x.dtype)
    if not torch.isfinite(scale).all() or not torch.isfinite(offset).all():
        raise ValueError("quantization metadata exceeds input precision")
    denominator = torch.where(scale == 0, torch.ones_like(scale), scale).float()
    codes = ((x.float() - offset.float()) / denominator).round().clamp_min(0)
    codes = torch.minimum(codes, levels).to(torch.uint8)
    return codes, scale, offset


@dataclass(frozen=True)
class PNMixConfig:
    high_ratio: float = 0.5
    group_size: int = 128
    residual_size: int = 128
    sink_tokens: int = 32
    value_bits: int = 2
    value_group_size: int = 128
    pair_layout: str = "adjacent"

    def __post_init__(self) -> None:
        if not math.isfinite(self.high_ratio) or not 0 <= self.high_ratio <= 1:
            raise ValueError("high_ratio must be in [0, 1]")
        if self.group_size <= 0 or self.residual_size <= 0:
            raise ValueError("group and residual sizes must be positive")
        if self.residual_size % self.group_size:
            raise ValueError("residual_size must be divisible by group_size")
        if self.sink_tokens < 0 or self.value_group_size <= 0:
            raise ValueError("invalid sink/value group size")
        if self.value_bits not in (2, 4, 16):
            raise ValueError("value_bits must be 2, 4, or unquantized 16")
        if self.pair_layout not in ("adjacent", "split"):
            raise ValueError("pair_layout must be adjacent or split")


@dataclass(frozen=True)
class PackedKeyPage:
    low: Tensor
    high: Tensor
    scale: Tensor
    offset: Tensor
    tokens: int


@dataclass(frozen=True)
class PackedValueGroup:
    codes: Tensor
    scale: Tensor
    offset: Tensor
    channels: int


@dataclass(frozen=True)
class PackedPage:
    key: PackedKeyPage
    value: tuple[PackedValueGroup, ...] | Tensor


def quantize_key_page(key: Tensor, pair_mask: Tensor, *, pair_layout: str) -> PackedKeyPage:
    mask = _channel_mask(pair_mask, pair_layout)
    if mask.shape != (*key.shape[:2], key.shape[-1]):
        raise ValueError("pair mask is not compatible with key page")
    bits = torch.where(mask, 3, 1).unsqueeze(-2)
    codes, scale, offset = asymmetric_quantize(key, bits, dim=-2)
    selected = mask.sum(-1)
    if not torch.all(selected == selected.flatten()[0]):
        raise ValueError("all heads must use the same high-precision pair count")
    count = int(selected.flatten()[0])
    indices = torch.argsort(mask.to(torch.int8), dim=-1, descending=True, stable=True)[..., :count]
    upper = (codes >> 1).gather(-1, indices.unsqueeze(-2).expand(-1, -1, key.shape[-2], -1))
    return PackedKeyPage(
        pack_codes(codes & 1, 1, dim=-2),
        pack_codes(upper, 2, dim=-2),
        scale,
        offset,
        key.shape[-2],
    )


def dequantize_key_page(page: PackedKeyPage, pair_mask: Tensor, *, pair_layout: str) -> Tensor:
    mask = _channel_mask(pair_mask, pair_layout)
    codes = unpack_codes(page.low, 1, page.tokens, dim=-2)
    count = page.high.shape[-1]
    indices = torch.argsort(mask.to(torch.int8), dim=-1, descending=True, stable=True)[..., :count]
    upper = unpack_codes(page.high, 2, page.tokens, dim=-2)
    expanded = indices.unsqueeze(-2).expand(-1, -1, page.tokens, -1)
    high_codes = codes.gather(-1, expanded) | (upper << 1)
    codes.scatter_(-1, expanded, high_codes)
    return codes.to(page.scale.dtype) * page.scale + page.offset


def _quantize_value(value: Tensor, config: PNMixConfig) -> tuple[PackedValueGroup, ...] | Tensor:
    if config.value_bits == 16:
        return value.detach().clone()
    groups = []
    for block in value.split(config.value_group_size, dim=-1):
        codes, scale, offset = asymmetric_quantize(block, config.value_bits, dim=-1)
        groups.append(
            PackedValueGroup(pack_codes(codes, config.value_bits), scale, offset, block.shape[-1])
        )
    return tuple(groups)


def _dequantize_value(value: tuple[PackedValueGroup, ...] | Tensor, bits: int) -> Tensor:
    if isinstance(value, Tensor):
        return value
    return torch.cat(
        [
            unpack_codes(group.codes, bits, group.channels).to(group.scale.dtype) * group.scale
            + group.offset
            for group in value
        ],
        dim=-1,
    )


def reference_attention(
    query: Tensor, key: Tensor, value: Tensor, *, query_positions: Tensor | None = None
) -> tuple[Tensor, Tensor]:
    """Causal GQA with global positions; useful for dense and quantized-cache controls."""
    _states(query, "query")
    _states(key, "key")
    _states(value, "value")
    if (
        key.shape != value.shape
        or query.shape[0] != key.shape[0]
        or query.shape[-1] != key.shape[-1]
    ):
        raise ValueError("incompatible attention states")
    if query.device != key.device or value.device != key.device or query.shape[1] % key.shape[1]:
        raise ValueError("incompatible attention devices or grouped heads")
    if query_positions is None:
        if query.shape[-2] > key.shape[-2]:
            raise ValueError("query cannot be longer than the cache")
        query_positions = torch.arange(
            key.shape[-2] - query.shape[-2], key.shape[-2], device=query.device
        )
    if query_positions.ndim == 1:
        query_positions = query_positions.unsqueeze(0).expand(query.shape[0], -1)
    if (
        query_positions.shape != (query.shape[0], query.shape[-2])
        or query_positions.device != query.device
        or query_positions.is_floating_point()
        or (query_positions < 0).any()
        or (query_positions >= key.shape[-2]).any()
    ):
        raise ValueError("query_positions must index existing cache tokens")
    repeats = query.shape[1] // key.shape[1]
    keys = key.repeat_interleave(repeats, dim=1).float()
    values = value.repeat_interleave(repeats, dim=1).float()
    logits = query.float() @ keys.transpose(-1, -2) / math.sqrt(query.shape[-1])
    allowed = (
        torch.arange(key.shape[-2], device=query.device)[None, None, :]
        <= query_positions[:, :, None]
    )
    probabilities = logits.masked_fill(~allowed[:, None], -torch.inf).softmax(-1)
    return (probabilities @ values).to(query.dtype), probabilities


class PNMixCache:
    """Single-layer append-only cache with a once-per-prefill, packed pair mask.

    Tensors use [B,H,T,D]. Caller supplies *post-RoPE* Q/K and chooses the
    actual model pair layout. Existing pages never retain the original K/V.
    Sink/residual precision is exactly the input precision (FP16 in GPU runs).
    """

    def __init__(self, pair_mask: Tensor, config: PNMixConfig, prototype: Tensor) -> None:
        self.config = config
        self._pair_count = pair_mask.shape[-1]
        self._packed_mask = pack_codes(pair_mask.to(torch.uint8), 1)
        empty = prototype[..., :0, :].detach().clone()
        self._sink_key, self._sink_value = empty.clone(), empty.clone()
        self._residual_key, self._residual_value = empty.clone(), empty.clone()
        self._pages: list[PackedPage] = []
        self.saliency_computations = 1
        self.total_tokens = 0

    @classmethod
    def from_prefill(
        cls, query: Tensor, key: Tensor, value: Tensor, config: PNMixConfig | None = None
    ) -> PNMixCache:
        config = config or PNMixConfig()
        _states(value, "value")
        if key.shape != value.shape or key.dtype != value.dtype or key.device != value.device:
            raise ValueError("key/value shapes, dtypes, devices must agree")
        scores = pair_norm_scores(query, key, pair_layout=config.pair_layout)
        cache = cls(select_salient_pairs(scores, config.high_ratio), config, key)
        cache.append(key, value)
        return cache

    @property
    def high_pair_mask(self) -> Tensor:
        return unpack_codes(self._packed_mask, 1, self._pair_count).bool()

    @property
    def pages(self) -> tuple[PackedPage, ...]:
        return tuple(self._pages)

    @property
    def residual_tokens(self) -> int:
        return self._residual_key.shape[-2]

    def append(self, key: Tensor, value: Tensor) -> None:
        _states(key, "key")
        _states(value, "value")
        target = self._sink_key
        if (
            key.shape != value.shape
            or key.shape[:2] != target.shape[:2]
            or key.shape[-1] != target.shape[-1]
            or key.dtype != target.dtype
            or value.dtype != target.dtype
            or key.device != target.device
            or value.device != target.device
        ):
            raise ValueError(
                "appended states must match cache batch, heads, dimension, dtype, device"
            )
        with torch.no_grad():
            needed = min(self.config.sink_tokens - self._sink_key.shape[-2], key.shape[-2])
            if needed:
                self._sink_key = torch.cat((self._sink_key, key[..., :needed, :].detach()), dim=-2)
                self._sink_value = torch.cat(
                    (self._sink_value, value[..., :needed, :].detach()), dim=-2
                )
            self._residual_key = torch.cat(
                (self._residual_key, key[..., needed:, :].detach()), dim=-2
            )
            self._residual_value = torch.cat(
                (self._residual_value, value[..., needed:, :].detach()), dim=-2
            )
            while self._residual_key.shape[-2] >= self.config.residual_size:
                for start in range(0, self.config.residual_size, self.config.group_size):
                    stop = start + self.config.group_size
                    kpage = quantize_key_page(
                        self._residual_key[..., start:stop, :],
                        self.high_pair_mask,
                        pair_layout=self.config.pair_layout,
                    )
                    vpage = _quantize_value(self._residual_value[..., start:stop, :], self.config)
                    self._pages.append(PackedPage(kpage, vpage))
                self._residual_key = self._residual_key[..., self.config.residual_size :, :].clone()
                self._residual_value = self._residual_value[
                    ..., self.config.residual_size :, :
                ].clone()
            self.total_tokens += key.shape[-2]

    def materialize(self) -> tuple[Tensor, Tensor]:
        mask = self.high_pair_mask
        keys = [self._sink_key]
        values = [self._sink_value]
        for page in self._pages:
            keys.append(dequantize_key_page(page.key, mask, pair_layout=self.config.pair_layout))
            values.append(_dequantize_value(page.value, self.config.value_bits))
        keys.append(self._residual_key)
        values.append(self._residual_value)
        return torch.cat(keys, dim=-2), torch.cat(values, dim=-2)

    def attention(
        self, query: Tensor, *, query_positions: Tensor | None = None
    ) -> tuple[Tensor, Tensor]:
        key, value = self.materialize()
        return reference_attention(query, key, value, query_positions=query_positions)

    def storage(self) -> dict[str, int | float]:
        def nbytes(tensor: Tensor) -> int:
            return tensor.numel() * tensor.element_size()

        key_bytes = sum(nbytes(x) for x in (self._packed_mask, self._sink_key, self._residual_key))
        value_bytes = sum(nbytes(x) for x in (self._sink_value, self._residual_value))
        quantized = 0
        for page in self._pages:
            key_bytes += sum(
                nbytes(x) for x in (page.key.low, page.key.high, page.key.scale, page.key.offset)
            )
            quantized += page.key.tokens
            if isinstance(page.value, Tensor):
                value_bytes += nbytes(page.value)
            else:
                value_bytes += sum(
                    nbytes(x)
                    for group in page.value
                    for x in (group.codes, group.scale, group.offset)
                )
        elements = (
            self.total_tokens
            * self._sink_key.shape[0]
            * self._sink_key.shape[1]
            * self._sink_key.shape[-1]
        )
        return {
            "key_bytes": key_bytes,
            "value_bytes": value_bytes,
            "persistent_cache_bytes": key_bytes + value_bytes,
            "quantized_tokens": quantized,
            "sink_tokens": self._sink_key.shape[-2],
            "residual_tokens": self.residual_tokens,
            "key_bits_per_element_including_sink_residual": 8 * key_bytes / elements,
            "temporary_dequantized_cache_included": False,
        }
