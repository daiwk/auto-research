"""DuoJEPA v1 §5.2--5.3: target-space CLS loss and one skipless image layer."""
from __future__ import annotations

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/duojepa-a100-20261115.json"


def target_space_loss(own_a: Tensor, own_b: Tensor, translated_a: Tensor,
                      translated_b: Tensor, temperature: float = .1) -> Tensor:
    """Inputs [batch, global views, width]; BOTH target centroid gradients flow."""
    if (own_a.ndim != 3 or min(own_a.shape) < 2
            or any(x.shape != own_a.shape or not torch.isfinite(x).all()
                   for x in (own_a, own_b, translated_a, translated_b))
            or not 0 < temperature < float("inf")):
        raise ValueError("finite matched [batch>=2,views>=2,width>=2] and positive temperature required")

    def normalized(x: Tensor) -> Tensor:
        return F.normalize(F.layer_norm(x, (x.shape[-1],)), dim=-1)

    def within_space(target: Tensor, translated_source: Tensor) -> Tensor:
        centroid = F.normalize(normalized(target).sum(1), dim=-1)
        anchors = normalized(translated_source).flatten(0, 1)
        logits = anchors @ centroid.T / temperature
        labels = torch.arange(len(target), device=target.device).repeat_interleave(target.shape[1])
        return F.cross_entropy(logits, labels)

    return within_space(own_a, translated_b) + within_space(own_b, translated_a)


class SkiplessTranslator(nn.Module):
    """Single-head image Eq.7, no residual additions, App.A initialization.

    Matrices act on row vectors (x @ W), so the QK product is Wq @ Wk.T.
    No backbone, LeJEPA projector, distributed negatives or patch loss is hidden
    behind this bounded reference. Text's post-norm variant is not implemented.
    """

    def __init__(self, width: int, *, alpha: float = 2, beta: float = .6, c: float = 3):
        super().__init__()
        if width < 2 or any(not math.isfinite(x) or x <= 0 for x in (alpha, beta, c)):
            raise ValueError("width>=2 and finite positive initialization constants required")
        self.width = width
        self.norm1, self.norm2 = nn.LayerNorm(width), nn.LayerNorm(width)
        self.q, self.k, self.v, self.out = (nn.Parameter(torch.empty(width, width)) for _ in range(4))
        self.gamma1, self.gamma2 = nn.Parameter(torch.ones(width)), nn.Parameter(torch.ones(width))
        self.mlp = nn.Sequential(nn.Linear(width, 4 * width), nn.GELU(), nn.Linear(4 * width, width))
        with torch.no_grad():
            product = alpha * torch.randn(width, width) / math.sqrt(width) + beta * torch.eye(width)
            u, singular, vh = torch.linalg.svd(product)
            self.q.copy_(u * singular.sqrt())
            self.k.copy_(vh.T * singular.sqrt())
            nn.init.orthogonal_(self.v, gain=c)
            nn.init.orthogonal_(self.out, gain=c)
            for layer in (self.mlp[0], self.mlp[2]):
                nn.init.orthogonal_(layer.weight)
                nn.init.zeros_(layer.bias)
        self.register_buffer("initial_qk_product", product)

    def forward(self, tokens: Tensor) -> Tensor:
        if tokens.ndim != 3 or tokens.shape[-1] != self.width or not torch.isfinite(tokens).all():
            raise ValueError("finite [batch,tokens,width] required")
        x = self.norm1(tokens)
        q, k, v = x @ self.q, x @ self.k, x @ self.v
        attention = (q @ k.transpose(-1, -2) / math.sqrt(self.width)).softmax(-1)
        y = self.gamma1 * ((attention @ v) @ self.out)
        return self.gamma2 * self.mlp(self.norm2(y))


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device not in {"cpu", "cuda"} or (device == "cuda" and not torch.cuda.is_available()):
        raise ValueError("available CPU or real CUDA device required")
    torch.manual_seed(seed)
    translator = SkiplessTranslator(12).to(device)
    inputs = torch.randn(6, 2, 3, 12, device=device)
    own_a = inputs[:, :, 0].detach().clone().requires_grad_(True)
    own_b = torch.randn_like(own_a, requires_grad=True)
    translated_a = translator(inputs.flatten(0, 1))[:, 0].view(6, 2, 12)
    translated_b = torch.randn_like(translated_a, requires_grad=True)
    loss = target_space_loss(own_a, own_b, translated_a, translated_b)
    loss.backward()
    with torch.no_grad():
        init_error = (translator.q @ translator.k.T - translator.initial_qk_product).abs().max()
        # Zero output weights: any residual shortcut would still return input.
        translator.mlp[2].weight.zero_()
        translator.mlp[2].bias.zero_()
        zero_output = translator(inputs.flatten(0, 1))
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"target_space_infonce": float(loss.detach()),
                        "qk_initialization_max_error": float(init_error),
                        "target_gradient_norm": float(own_a.grad.norm() + own_b.grad.norm())},
            "checks": {"qk_product_matches_initialized_target": bool(init_error < 1e-4),
                       "both_target_centroids_receive_gradients": all(x.grad is not None and bool(x.grad.norm() > 0)
                                                                     for x in (own_a, own_b)),
                       "translator_receives_gradients": translator.q.grad is not None,
                       "no_hidden_residual_shortcut": bool(torch.equal(zero_output, torch.zeros_like(zero_output)))}}
