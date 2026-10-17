"""Independent bounded-Huffman BF16 exponent codec, LCT Sections 4/B/C.

This is a small tensor reference: CPU codebook construction is precomputed from
a caller-supplied model, then Torch CUDA/CPU tensor packing and sequential stream
decoding execute the same bit format. No fused Triton, throughput or allocator
claims. Raw BF16 bits (including NaNs, infinities and signed zeros) are retained.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor

ESCAPE = 256


def _bounded_lengths(weights: list[float], limit: int) -> list[int]:
    """Binary Package-Merge, optimal prefix lengths for the given alphabet."""
    n = len(weights)
    if n == 1:
        return [0]
    if n > 2 ** limit:
        raise ValueError("alphabet cannot fit prefix cap")
    leaves = sorted((value, (i,)) for i, value in enumerate(weights))
    current = leaves
    for _ in range(1, limit):
        packages = [(current[i][0] + current[i + 1][0], current[i][1] + current[i + 1][1])
                    for i in range(0, len(current) - 1, 2)]
        current = sorted(leaves + packages)
    lengths = [0] * n
    for _, symbols in current[:2 * n - 2]:
        for symbol in symbols:
            lengths[symbol] += 1
    if any(not 1 <= length <= limit for length in lengths):
        raise RuntimeError("invalid package-merge result")
    return lengths


@dataclass(frozen=True)
class ExponentCodebook:
    codes: tuple[int, ...]  # 257 slots including escape, -1 means escaped
    lengths: tuple[int, ...]
    prefix_cap: int
    expected_bits: float


def build_codebook(probabilities: list[float] | tuple[float, ...], prefix_cap: int = 8) -> ExponentCodebook:
    """Test all probability-tail cutoffs; never fit to the encoded tensor at runtime."""
    if (len(probabilities) != 256 or not isinstance(prefix_cap, int) or not 1 <= prefix_cap <= 8 or
            any(not math.isfinite(p) or p <= 0 for p in probabilities)):
        raise ValueError("256 strictly positive finite model probabilities and prefix cap 1..8 required")
    total = sum(probabilities)
    if not math.isfinite(total) or total <= 0:
        raise ValueError("finite positive model total required")
    p = [x / total for x in probabilities]
    order = sorted(range(256), key=lambda i: (-p[i], i))
    best: tuple[float, list[int], list[int]] | None = None
    for cutoff in range(min(255, 2 ** prefix_cap - 1) + 1):
        symbols = order[:cutoff] + [ESCAPE]
        weights = [p[i] for i in order[:cutoff]] + [sum(p[i] for i in order[cutoff:])]
        lengths = _bounded_lengths(weights, prefix_cap)
        cost = sum(w * length for w, length in zip(weights, lengths, strict=True)) + weights[-1] * 8
        if best is None or cost < best[0]:
            best = cost, symbols, lengths
    if prefix_cap == 8:
        # All 256 symbols directly coded: bounded Huffman necessarily uses 8 bits.
        cost = 8.
        if best is None or cost < best[0]:
            best = cost, list(range(256)), [8] * 256
    assert best is not None
    cost, symbols, lengths = best
    codes = [-1] * 257
    output_lengths = [0] * 257
    code, previous = 0, 0
    for length, symbol in sorted(zip(lengths, symbols, strict=True)):
        code <<= length - previous
        codes[symbol], output_lengths[symbol] = code, length
        code += 1
        previous = length
    return ExponentCodebook(tuple(codes), tuple(output_lengths), prefix_cap, cost)


def gaussian_exponent_model() -> tuple[float, ...]:
    """Fixed centered, zero-inflated model; not calibrated on diagnostic/test input."""
    weights = [math.exp(-abs(i - 127) / 2.5) + 1e-12 for i in range(256)]
    weights[0] = .02
    return tuple(weights)


def _center_map(center: int, device: torch.device) -> Tensor:
    e = torch.arange(256, dtype=torch.int64, device=device)
    d = (e - 127 - center) % 256
    z = (-127 - center) % 256
    return torch.where(e == 0, 0, torch.where(d < z, d + 1, d))


@dataclass(frozen=True)
class CompressedBF16:
    side_bytes: Tensor
    prefix_bytes: Tensor
    prefix_counts: Tensor
    overflow_exponents: Tensor
    overflow_counts: Tensor
    shape: tuple[int, ...]
    streams: int
    budget_bits: int
    center: int
    codebook: ExponentCodebook

    @property
    def payload_storage_bytes(self) -> int:
        return sum(t.numel() * t.element_size() for t in (
            self.side_bytes, self.prefix_bytes, self.prefix_counts,
            self.overflow_exponents, self.overflow_counts))

    @property
    def standalone_codebook_bytes(self) -> int:
        # Explicit logical serialization: uint16 code + uint8 length per slot.
        return 257 * 3

    @property
    def serialized_header_bytes(self) -> int:
        # A declared int32 serialization: ndim, shape, streams, budget, center.
        # Python object overhead and shared lookup tables are separate costs.
        return 4 * (len(self.shape) + 4)


def compress_bf16(tensor: Tensor, codebook: ExponentCodebook, *, streams: int = 8,
                  budget_bits: int = 128, center: int = 0) -> CompressedBF16:
    if tensor.dtype != torch.bfloat16 or tensor.numel() == 0 or tensor.numel() > 65536:
        raise ValueError("bounded reference supports 1..65536 BF16 elements")
    if (not isinstance(streams, int) or not 1 <= streams <= 256 or
            not isinstance(budget_bits, int) or not 8 <= budget_bits <= 65536 or budget_bits % 8 or
            not isinstance(center, int) or not -128 <= center <= 127):
        raise ValueError("valid streams, byte-aligned bounded stream budget and exponent center required")
    device = tensor.device
    raw = tensor.contiguous().view(torch.int16).reshape(-1).to(torch.int64) & 65535
    exponent = (raw >> 7) & 255
    side = (((raw >> 8) & 128) | (raw & 127)).to(torch.uint8)
    mapping = _center_map(center, device)
    symbols = mapping[exponent]
    codes = torch.tensor(codebook.codes, dtype=torch.int64, device=device)
    lengths = torch.tensor(codebook.lengths, dtype=torch.int64, device=device)
    escaped = codes[symbols] < 0
    # The only-symbol escape code can have length zero (literal-only mode).
    word = torch.where(escaped, (codes[ESCAPE] << 8) | symbols, codes[symbols])
    length = torch.where(escaped, lengths[ESCAPE] + 8, lengths[symbols])
    count = raw.numel()
    steps = math.ceil(count / streams)
    pad = steps * streams - count
    def cyclic(x: Tensor, fill: int = 0) -> Tensor:
        return torch.cat((x, x.new_full((pad,), fill))).reshape(steps, streams).t()
    words, sizes, exponents = cyclic(word), cyclic(length), cyclic(exponent)
    logical = torch.arange(steps * streams, device=device).reshape(steps, streams).t() < count
    end = sizes.cumsum(-1)
    accepted = (end <= budget_bits) & logical
    prefix_counts = accepted.sum(-1).to(torch.int32)
    offsets = end - sizes
    bit = torch.arange(16, device=device)
    bits = ((words.unsqueeze(-1) >> (sizes.unsqueeze(-1) - 1 - bit).clamp_min(0)) & 1)
    write = accepted.unsqueeze(-1) & (bit < sizes.unsqueeze(-1))
    positions = offsets.unsqueeze(-1) + bit
    stream_ids = torch.arange(streams, device=device)[:, None, None].expand_as(positions)
    addresses = stream_ids * (budget_bits // 8) + positions // 8
    byte_values = bits << (positions % 8)
    packed = torch.zeros(streams * (budget_bits // 8), dtype=torch.int64, device=device)
    packed.scatter_add_(0, addresses[write], byte_values[write])
    tails = logical & ~accepted
    return CompressedBF16(side, packed.to(torch.uint8).reshape(streams, -1), prefix_counts,
                          exponents[tails].to(torch.uint8), tails.sum(-1).to(torch.int32),
                          tuple(tensor.shape), streams, budget_bits, center, codebook)


def decompress_bf16(packed: CompressedBF16) -> Tensor:
    device = packed.side_bytes.device
    count, streams = packed.side_bytes.numel(), packed.streams
    steps = math.ceil(count / streams)
    symbols = torch.full((256,), -1, dtype=torch.int64, device=device)
    prefix_lengths = torch.zeros(256, dtype=torch.int64, device=device)
    for symbol, (code, length) in enumerate(zip(packed.codebook.codes, packed.codebook.lengths, strict=True)):
        if code >= 0:
            start, stop = code << (8 - length), (code + 1) << (8 - length)
            symbols[start:stop], prefix_lengths[start:stop] = symbol, length
    reverse = torch.empty(256, dtype=torch.int64, device=device)
    reverse[_center_map(packed.center, device)] = torch.arange(256, device=device)
    offsets = torch.zeros(streams, dtype=torch.int64, device=device)
    tail_starts = packed.overflow_counts.to(torch.int64).cumsum(0) - packed.overflow_counts
    restored = torch.empty(streams, steps, dtype=torch.int64, device=device)
    lanes = torch.arange(streams, device=device)[:, None]
    bit = torch.arange(16, device=device)
    tails = packed.overflow_exponents.to(torch.int64)
    if not tails.numel():
        tails = torch.zeros(1, dtype=torch.int64, device=device)
    for step in range(steps):
        positions = offsets[:, None] + bit
        byte = (positions // 8).clamp_max(packed.prefix_bytes.shape[-1] - 1)
        values = (packed.prefix_bytes[lanes, byte].to(torch.int64) >> (positions % 8)) & 1
        values = values * (positions < packed.budget_bits)
        lookahead = (values * (1 << (15 - bit))).sum(-1)
        index = lookahead >> 8
        symbol, length = symbols[index], prefix_lengths[index]
        if bool((symbol < 0).any()):
            raise ValueError("invalid Huffman prefix")
        literal = (lookahead >> (8 - length)) & 255
        decoded_symbol = torch.where(symbol == ESCAPE, literal, symbol)
        decoded_exponent = reverse[decoded_symbol]
        is_prefix = step < packed.prefix_counts
        tail_index = (tail_starts + step - packed.prefix_counts).clamp(0, tails.numel() - 1)
        restored[:, step] = torch.where(is_prefix, decoded_exponent, tails[tail_index])
        offsets += torch.where(is_prefix, length + (symbol == ESCAPE).long() * 8, 0)
    exponent = restored.t().reshape(-1)[:count]
    side = packed.side_bytes.to(torch.int64)
    bits = ((side & 128) << 8) | (exponent << 7) | (side & 127)
    return bits.to(torch.int16).view(torch.bfloat16).reshape(packed.shape)


class _LCTLinear(torch.autograd.Function):
    @staticmethod
    def forward(ctx, inputs: Tensor, weight: Tensor, codebook: ExponentCodebook):
        if (inputs.ndim != 2 or weight.ndim != 2 or inputs.shape[-1] != weight.shape[-1] or
                inputs.device != weight.device):
            raise ValueError("compatible 2D BF16 inputs and weight on one device required")
        # Codec objects retain only packed buffers, not the original dense input.
        ctx.inputs = compress_bf16(inputs, codebook, streams=8, budget_bits=128)
        ctx.weight = compress_bf16(weight, codebook, streams=8, budget_bits=128)
        return inputs @ weight.t()

    @staticmethod
    def backward(ctx, gradient: Tensor):
        inputs, weight = decompress_bf16(ctx.inputs), decompress_bf16(ctx.weight)
        return gradient @ weight, gradient.t() @ inputs, None


def lct_linear(inputs: Tensor, weight: Tensor, codebook: ExponentCodebook) -> Tensor:
    """Small actual autograd interface; packing backward state, not identity STE."""
    return _LCTLinear.apply(inputs, weight, codebook)
