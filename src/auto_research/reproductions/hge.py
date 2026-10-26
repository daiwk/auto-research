"""HGE Eqs.2--11 on caller-provided embeddings, prices and regression values.

This is an L1 differentiable component, not a complete DIN/DCN recommender,
private-log training recipe, calibration comparison or production reproduction.
The residual is deliberately signed as in Eq.10; no undocumented output clamp.
"""
from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/hge-a100-20261026.json"


def _finite(value: Tensor, name: str) -> None:
    if not value.is_floating_point() or not bool(torch.isfinite(value).all()):
        raise ValueError(f"{name}: finite floating tensor required")


def proxy_value(conversion: Tensor, item_probability: Tensor, quantity: Tensor, prices: Tensor) -> Tensor:
    """Eq.5: item probabilities are conditional Bernoulli, NOT a softmax.

    Inputs are [B], [B,K], [B,K], [B,K]. There is no padding or inferred label
    mask: the caller supplies exactly the displayed top-K item set.
    """
    if (item_probability.ndim != 2 or min(item_probability.shape) < 1
            or item_probability.numel() > 262_144 or conversion.shape != item_probability.shape[:1]
            or quantity.shape != item_probability.shape or prices.shape != item_probability.shape):
        raise ValueError("bounded aligned [B] / [B,K] inputs required")
    for name, value in (("conversion", conversion), ("item_probability", item_probability),
                        ("quantity", quantity), ("prices", prices)):
        _finite(value, name)
        if value.device != conversion.device or value.dtype != conversion.dtype:
            raise ValueError("matching dtype/device required")
    if (bool(((conversion < 0) | (conversion > 1)).any())
            or bool(((item_probability < 0) | (item_probability > 1)).any())
            or bool((quantity < 0).any()) or bool((prices < 0).any())):
        raise ValueError("probabilities in [0,1], nonnegative quantities/prices required")
    result = conversion * (item_probability * quantity * prices).sum(-1)
    _finite(result, "PLL output")
    return result


def residual_fusion(pll: Tensor, residual: Tensor, regression: Tensor, alpha: Tensor) -> Tensor:
    """Eqs.10--11, explicit per-example gate; no ground-truth behavior routing."""
    if pll.ndim != 1 or pll.numel() < 1 or any(x.shape != pll.shape for x in (residual, regression, alpha)):
        raise ValueError("aligned nonempty [B] values required")
    for name, value in (("pll", pll), ("residual", residual), ("regression", regression), ("alpha", alpha)):
        _finite(value, name)
        if value.device != pll.device or value.dtype != pll.dtype:
            raise ValueError("matching dtype/device required")
    if bool(((alpha < 0) | (alpha > 1)).any()):
        raise ValueError("fusion weight in [0,1] required")
    result = alpha * (pll + residual) + (1 - alpha) * regression
    _finite(result, "fusion output")
    return result


class HierarchicalGTV(nn.Module):
    """HSAE + PLL heads + residual/context gate; universal tower is external.

    Eq.3 concatenates context AFTER item-only MHSA. Consequently H' and H1
    have item_dim + context_dim channels. Caller supplies positional embeddings;
    no implicit permutation invariance or generated price labels are claimed.
    Small explicit dimensions are a component configuration, not paper-scale
    Dice towers, DIN/DCN features, negative sampling or the Eq.12 loss recipe.
    """

    def __init__(self, item_dim: int, context_dim: int, heads: int, hidden: int):
        super().__init__()
        values = (item_dim, context_dim, heads, hidden)
        if (any(type(v) is not int or not 1 <= v <= 512 for v in values)
                or item_dim % heads or (item_dim + context_dim) * hidden > 131_072):
            raise ValueError("bounded positive integer dimensions and divisible heads required")
        self.item_dim, self.context_dim = item_dim, context_dim
        joint = item_dim + context_dim
        self.attention = nn.MultiheadAttention(item_dim, heads, dropout=0, batch_first=True)
        self.norm1 = nn.LayerNorm(joint)
        self.ffn = nn.Sequential(nn.Linear(joint, hidden), nn.GELU(), nn.Linear(hidden, joint))
        self.norm2 = nn.LayerNorm(joint)
        self.global_head = nn.Linear(joint + context_dim, 1)
        self.item_head = nn.Linear(joint + context_dim, 1)
        self.quantity_head = nn.Linear(joint + context_dim, 1)
        self.residual_head = nn.Linear(context_dim, 1)
        self.gate = nn.Linear(context_dim, 1)

    def forward(self, items: Tensor, positions: Tensor, context: Tensor,
                prices: Tensor, regression: Tensor) -> dict[str, Tensor]:
        if (items.ndim != 3 or min(items.shape) < 1 or items.shape[-1] != self.item_dim
                or items.shape[1] > 256 or items.numel() > 262_144 or positions.shape != items.shape
                or context.shape != (items.shape[0], self.context_dim)
                or prices.shape != items.shape[:2] or regression.shape != items.shape[:1]):
            raise ValueError("bounded aligned item/position/context/price/regression shapes required")
        parameter = next(self.parameters())
        for name, value in (("items", items), ("positions", positions), ("context", context),
                            ("prices", prices), ("regression", regression)):
            _finite(value, name)
            if value.device != parameter.device or value.dtype != parameter.dtype:
                raise ValueError("inputs must match module dtype/device")
        h0 = items + positions
        attention, _ = self.attention(h0, h0, h0, need_weights=False)
        expanded = context[:, None].expand(-1, items.shape[1], -1)
        h_prime = self.norm1(torch.cat((h0 + attention, expanded), dim=-1))
        h1 = self.norm2(h_prime + self.ffn(h_prime))
        item_input = torch.cat((h1, expanded), dim=-1)
        conversion = self.global_head(torch.cat((h1.mean(1), context), dim=-1)).squeeze(-1).sigmoid()
        item_probability = self.item_head(item_input).squeeze(-1).sigmoid()
        quantity = F.softplus(self.quantity_head(item_input).squeeze(-1))
        pll = proxy_value(conversion, item_probability, quantity, prices)
        residual = self.residual_head(context).squeeze(-1)
        alpha = self.gate(context).squeeze(-1).sigmoid()
        final = residual_fusion(pll, residual, regression, alpha)
        return {"value": final, "pll": pll, "residual": residual, "alpha": alpha,
                "conversion": conversion, "item_probability": item_probability, "quantity": quantity,
                "item_attention": attention, "contextual_items": h1}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or real available CUDA required; no fallback")
    with torch.random.fork_rng(devices=[torch.cuda.current_device()] if device == "cuda" else []):
        torch.manual_seed(seed)
        model = HierarchicalGTV(8, 4, 2, 16).to(device=device, dtype=torch.float64)
    gen = torch.Generator(device=device).manual_seed(seed)
    items = torch.randn(4, 5, 8, generator=gen, device=device, dtype=torch.float64, requires_grad=True)
    positions = torch.randn(items.shape, generator=gen, device=device, dtype=torch.float64)
    context = torch.randn(4, 4, generator=gen, device=device, dtype=torch.float64)
    prices = torch.rand(4, 5, generator=gen, device=device, dtype=torch.float64) * 10
    regression = torch.rand(4, generator=gen, device=device, dtype=torch.float64, requires_grad=True)
    output = model(items, positions, context, prices, regression)
    reference = torch.stack([output["conversion"][b] * sum(output["item_probability"][b, k]
        * output["quantity"][b, k] * prices[b, k] for k in range(5)) for b in range(4)])
    error = (reference - output["pll"]).abs().max().item()
    changed_context = model(items, positions, context + 1, prices, regression)
    context_attention_error = (output["item_attention"] - changed_context["item_attention"]).abs().max().item()
    changed_positions = model(items, positions * 0, context, prices, regression)
    position_gap = (changed_positions["value"] - output["value"]).abs().max().item()
    residual_gap = (residual_fusion(output["pll"], output["residual"] * 0, regression, output["alpha"])
                    - output["value"]).abs().max().item()
    unit_gap = (proxy_value(output["conversion"], output["item_probability"],
                           output["quantity"], torch.ones_like(prices)) - output["pll"]).abs().max().item()
    # A mechanism diagnostic, NOT fitting labels or selecting on a test set.
    loss = output["value"].square().mean()
    loss.backward()
    gradients = [p.grad for p in model.parameters()]
    grad_norm = sum(g.abs().sum().item() for g in gradients if g is not None)
    endpoint0 = residual_fusion(output["pll"], output["residual"], regression, torch.zeros_like(regression))
    endpoint1 = residual_fusion(output["pll"], output["residual"], regression, torch.ones_like(regression))
    joint_purchase = proxy_value(torch.ones(1, device=device, dtype=torch.float64),
        torch.tensor([[0.8, 0.9]], device=device, dtype=torch.float64),
        torch.ones(1, 2, device=device, dtype=torch.float64), torch.ones(1, 2, device=device, dtype=torch.float64))
    checks = {"eq5_independent_reference": error < 1e-12,
              "context_injected_after_item_attention": context_attention_error == 0,
              "position_negative_control": position_gap > 1e-8,
              "price_negative_control": unit_gap > 1e-8,
              "residual_negative_control": residual_gap > 1e-8,
              "fusion_endpoints": torch.equal(endpoint0, regression) and torch.equal(endpoint1, output["pll"] + output["residual"]),
              "conditional_item_not_softmax": abs(joint_purchase.item() - 1.7) < 1e-12,
              "finite_nonzero_backward": all(g is not None and bool(torch.isfinite(g).all()) for g in gradients)
                  and grad_norm > 0 and bool(torch.isfinite(items.grad).all())
                  and bool(torch.isfinite(regression.grad).all()) and bool((regression.grad.abs() > 0).all())}
    if not all(checks.values()):
        raise RuntimeError(f"HGE defining checks failed: {checks}")
    return {"seed": seed, "metrics": {"pll_reference_error": error, "context_attention_error": context_attention_error,
        "position_negative_control_gap": position_gap, "price_negative_control_gap": unit_gap,
        "residual_negative_control_gap": residual_gap, "parameter_gradient_l1": grad_norm,
        "examples": 4, "items_per_container": 5, "pretrained_model_calls": 0}, "checks": checks}
