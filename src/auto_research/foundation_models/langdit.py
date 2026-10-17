"""A small LangFlow-style LangDiT denoiser and exact local gradient contracts.

Independently implements equations 1–15 and unweighted inference mean (17) of
arXiv:2610.22330v1.  It is a mechanism component, not an implementation of the
learned LangFlow scheduler, the full sampler, Plaid adaptation, or OWT training.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F


def _finite(*values: Tensor) -> None:
    if any(not bool(torch.isfinite(value).all()) for value in values):
        raise ValueError("all numerical inputs must be finite")


def noise_coefficients(gamma: Tensor) -> tuple[Tensor, Tensor]:
    if not gamma.is_floating_point():
        raise ValueError("gamma must be floating point")
    _finite(gamma)
    return torch.sigmoid(-gamma).sqrt(), torch.sigmoid(gamma).sqrt()


def normalized_codebook(raw: Tensor, scale: float = .1) -> Tensor:
    if raw.ndim != 2 or not raw.is_floating_point() or not math.isfinite(scale) or scale <= 0:
        raise ValueError("finite positive scale and a floating [vocabulary,width] table required")
    _finite(raw)
    norms = raw.norm(dim=-1, keepdim=True)
    if bool((norms == 0).any()):
        raise ValueError("zero codebook rows cannot be normalized")
    return raw / norms * (scale * math.sqrt(raw.shape[-1]))


def corrupt_tokens(codebook: Tensor, tokens: Tensor, gamma: Tensor, noise: Tensor) -> Tensor:
    if (tokens.ndim != 2 or tokens.dtype != torch.long or gamma.shape != (tokens.shape[0],)
            or noise.shape != (*tokens.shape, codebook.shape[-1])
            or bool((tokens < 0).any()) or bool((tokens >= codebook.shape[0]).any())):
        raise ValueError("incompatible token, batch gamma, noise or vocabulary shapes")
    _finite(codebook, noise)
    alpha, sigma = noise_coefficients(gamma)
    return alpha[:, None, None] * codebook[tokens] + sigma[:, None, None] * noise


def likelihood_shortcut(z: Tensor, gamma: Tensor, codebook: Tensor, calibration: Tensor,
                        *, detach_codebook: bool = True, warmup: float = 1.) -> Tensor:
    """Equation 11: detach only the explicit right-hand codebook factor.

    ``z`` must NOT be detached: it can carry the codebook's separate input
    gradient.  Calibration is a multiplicative [batch] gate, not logits.
    """
    if (z.ndim != 3 or codebook.ndim != 2 or z.shape[-1] != codebook.shape[-1]
            or gamma.shape != (z.shape[0],) or calibration.shape != gamma.shape
            or not math.isfinite(warmup) or not 0 <= warmup <= 1):
        raise ValueError("invalid shortcut shapes or warmup outside [0,1]")
    _finite(z, codebook, calibration)
    alpha, sigma = noise_coefficients(gamma)
    coefficient = alpha / sigma.square()
    if not bool(torch.isfinite(coefficient).all()):
        raise ValueError("noise level makes the exact likelihood coefficient nonfinite")
    right = codebook.detach() if detach_codebook else codebook
    return (warmup * coefficient * calibration)[:, None, None] * (z @ right.t())


def posterior_mean(probabilities: Tensor, codebook: Tensor) -> Tensor:
    if probabilities.ndim != 3 or probabilities.shape[-1] != codebook.shape[0]:
        raise ValueError("probability vocabulary and codebook must agree")
    _finite(probabilities, codebook)
    if (bool((probabilities < 0).any())
            or not torch.allclose(probabilities.sum(-1), torch.ones_like(probabilities[..., 0]), atol=1e-5)):
        raise ValueError("probabilities must be nonnegative and sum to one")
    return probabilities @ codebook


def training_self_condition(probabilities: Tensor, codebook: Tensor) -> tuple[Tensor, Tensor]:
    """Equations 13–15; both confidence and the complete estimate are detached."""
    if codebook.shape[0] < 2:
        raise ValueError("entropy confidence needs at least two vocabulary entries")
    mean = posterior_mean(probabilities, codebook)
    entropy = -torch.special.xlogy(probabilities, probabilities).sum(-1, keepdim=True)
    confidence = (1 - entropy / math.log(codebook.shape[0])).clamp(0, 1)
    return (confidence * mean).detach(), confidence.detach()


class _RMSNorm(nn.Module):
    def __init__(self, width: int) -> None:
        super().__init__()
        self.gain = nn.Parameter(torch.ones(width))

    def forward(self, x: Tensor) -> Tensor:
        # Paper reduction is fp32, while learned gain/projection dtype is retained.
        norm = torch.rsqrt(x.float().square().mean(-1, keepdim=True) + 1e-6).to(x.dtype)
        return x * norm * self.gain


def _rotary(x: Tensor) -> Tensor:
    length, width = x.shape[-2], x.shape[-1]
    frequency = 10000. ** (-torch.arange(0, width, 2, device=x.device, dtype=x.dtype) / width)
    phase = torch.arange(length, device=x.device, dtype=x.dtype)[:, None] * frequency
    even, odd = x[..., 0::2], x[..., 1::2]
    return torch.stack((even * phase.cos() - odd * phase.sin(),
                        even * phase.sin() + odd * phase.cos()), dim=-1).flatten(-2)


class _NoiseBlock(nn.Module):
    def __init__(self, width: int, heads: int, condition_width: int) -> None:
        super().__init__()
        self.heads, self.head_width = heads, width // heads
        self.attention_norm, self.mlp_norm = _RMSNorm(width), _RMSNorm(width)
        self.query_norm, self.key_norm = _RMSNorm(self.head_width), _RMSNorm(self.head_width)
        self.qkv = nn.Linear(width, 3 * width)
        self.output = nn.Linear(width, width)
        self.mlp = nn.Sequential(nn.Linear(width, 4 * width), nn.GELU(), nn.Linear(4 * width, width))
        self.modulation = nn.Linear(condition_width, 6 * width)
        nn.init.zeros_(self.modulation.weight)
        nn.init.zeros_(self.modulation.bias)

    def forward(self, hidden: Tensor, condition: Tensor) -> Tensor:
        shift_a, scale_a, gate_a, shift_m, scale_m, gate_m = self.modulation(condition).chunk(6, -1)
        normalized = self.attention_norm(hidden) * (1 + scale_a[:, None]) + shift_a[:, None]
        batch, length, width = hidden.shape
        qkv = self.qkv(normalized).reshape(batch, length, 3, self.heads, self.head_width)
        q, k, v = (value.transpose(1, 2) for value in qkv.unbind(2))
        q, k = _rotary(self.query_norm(q)), _rotary(self.key_norm(k))
        weights = (q @ k.transpose(-2, -1) / math.sqrt(self.head_width)).softmax(-1)
        attention = (weights @ v).transpose(1, 2).reshape(batch, length, width)
        hidden = hidden + gate_a[:, None] * self.output(attention)
        normalized = self.mlp_norm(hidden) * (1 + scale_m[:, None]) + shift_m[:, None]
        return hidden + gate_m[:, None] * self.mlp(normalized)


class LangDiTDenoiser(nn.Module):
    """Dimension-scaled LangDiT with real bidirectional noise-conditioned attention."""

    def __init__(self, vocabulary: int = 19, width: int = 16, heads: int = 2,
                 depth: int = 2, condition_width: int = 32) -> None:
        super().__init__()
        if (min(vocabulary, width, heads, depth, condition_width) < 1 or vocabulary < 2
                or width % heads or (width // heads) % 2 or condition_width % 2):
            raise ValueError("positive dimensions and even head/condition widths required")
        self.width, self.condition_width = width, condition_width
        self.raw_codebook = nn.Parameter(torch.randn(vocabulary, width))
        self.input_projection = nn.Linear(2 * width, width, bias=False)
        nn.init.zeros_(self.input_projection.weight)
        self.noise_mlp = nn.Sequential(nn.Linear(condition_width, condition_width), nn.SiLU(),
                                       nn.Linear(condition_width, condition_width), nn.SiLU())
        self.blocks = nn.ModuleList(_NoiseBlock(width, heads, condition_width) for _ in range(depth))
        self.head_norm = _RMSNorm(width)
        self.head_modulation = nn.Linear(condition_width, 2 * width)
        nn.init.zeros_(self.head_modulation.weight)
        nn.init.zeros_(self.head_modulation.bias)
        self.vocabulary_head = nn.Linear(width, vocabulary, bias=False)
        self.calibration_mlp = nn.Sequential(nn.Linear(condition_width, 32), nn.SiLU(), nn.Linear(32, 1))
        nn.init.zeros_(self.calibration_mlp[-1].weight)
        nn.init.zeros_(self.calibration_mlp[-1].bias)

    def codebook(self) -> Tensor:
        return normalized_codebook(self.raw_codebook)

    def noise_embedding(self, gamma: Tensor) -> Tensor:
        _finite(gamma)
        half = self.condition_width // 2
        frequency = torch.exp(-math.log(10000.) * torch.arange(
            half, device=gamma.device, dtype=gamma.dtype) / max(half - 1, 1))
        phase = gamma[:, None] * frequency
        return self.noise_mlp(torch.cat((phase.cos(), phase.sin()), -1))

    def forward(self, z: Tensor, gamma: Tensor, self_condition: Tensor | None = None,
                *, warmup: float = 1., detach_shortcut: bool = True,
                calibrate: bool = True) -> Tensor:
        if z.ndim != 3 or z.shape[-1] != self.width or gamma.shape != (z.shape[0],):
            raise ValueError("expected [batch,length,width] and [batch] gamma")
        _finite(z, gamma)
        auxiliary = torch.zeros_like(z) if self_condition is None else self_condition
        if auxiliary.shape != z.shape:
            raise ValueError("self-conditioning must match noisy state")
        _finite(auxiliary)
        condition = self.noise_embedding(gamma)
        hidden = z + self.input_projection(torch.cat((z, auxiliary), -1))
        for block in self.blocks:
            hidden = block(hidden, condition)
        shift, scale = self.head_modulation(condition).chunk(2, -1)
        contextual = self.vocabulary_head(self.head_norm(hidden) * (1 + scale[:, None]) + shift[:, None])
        calibration = self.calibration_mlp(condition).squeeze(-1).clamp(-math.log(2), math.log(2)).exp()
        if not calibrate:
            calibration = torch.ones_like(calibration)
        return contextual + likelihood_shortcut(z, gamma, self.codebook(), calibration,
                                                detach_codebook=detach_shortcut, warmup=warmup)

    def training_logits(self, tokens: Tensor, gamma: Tensor, noise: Tensor,
                        bootstrap_examples: Tensor, *, step: int = 5000) -> tuple[Tensor, Tensor]:
        """Explicit mask selects examples for the paper's 25%-probability procedure.

        The caller supplies Bernoulli(0.25) draws; there is no hidden random state.
        This method does not implement or train LangFlow's learned scheduler.
        """
        if (bootstrap_examples.shape != (tokens.shape[0],) or bootstrap_examples.dtype != torch.bool
                or not isinstance(step, int) or step < 0):
            raise ValueError("boolean per-example bootstrap mask and nonnegative integer step required")
        z = corrupt_tokens(self.codebook(), tokens, gamma, noise)
        auxiliary = torch.zeros_like(z)
        if bool(bootstrap_examples.any()):
            with torch.no_grad():
                boot = self(z, gamma, warmup=min(step / 5000, 1.)).softmax(-1)
                weighted, _ = training_self_condition(boot, self.codebook())
                auxiliary = torch.where(bootstrap_examples[:, None, None], weighted, auxiliary)
        logits = self(z, gamma, auxiliary, warmup=min(step / 5000, 1.))
        return logits, auxiliary

    def inference_mean(self, z: Tensor, gamma: Tensor, self_condition: Tensor | None = None) -> Tensor:
        """Equation 17: unweighted posterior mean, with no bootstrap extra forward."""
        return posterior_mean(self(z, gamma, self_condition).softmax(-1), self.codebook())

    def token_loss(self, logits: Tensor, tokens: Tensor) -> Tensor:
        return F.cross_entropy(logits.flatten(0, 1), tokens.flatten())
