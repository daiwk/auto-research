"""Unbundling v1 §5/E.1: additive vision-only capacity, not a trained MLLM."""
from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/unbundling-vision-a100-20261115.json"


class SwiGLU(nn.Module):
    def __init__(self, width: int, hidden: int):
        super().__init__()
        self.gate = nn.Linear(width, hidden, bias=False)
        self.up = nn.Linear(width, hidden, bias=False)
        self.down = nn.Linear(hidden, width, bias=True)

    def forward(self, x: Tensor) -> Tensor:
        return self.down(F.silu(self.gate(x)) * self.up(x))


class InFusionBlock(nn.Module):
    """One joint causal-attention block; FFN-only or QKVO+FFN added capacity.

    Visual tokens can affect text through joint attention. The modality mask
    gates extra projections, not attention visibility. This tiny reference
    omits the paper's positional embedding, GQA and multilayer backbone.
    """

    def __init__(self, width: int, hidden: int, heads: int = 2, *, qkvo: bool = True):
        super().__init__()
        if min(width, hidden, heads) < 1 or width % heads:
            raise ValueError("positive dimensions and width divisible by heads required")
        self.heads, self.width = heads, width
        self.norm_attention, self.norm_ffn = nn.RMSNorm(width), nn.RMSNorm(width)
        self.shared = nn.ModuleDict({k: nn.Linear(width, width, bias=False) for k in "qkvo"})
        self.vision = nn.ModuleDict({k: nn.Linear(width, width, bias=False) for k in "qkvo"}) if qkvo else None
        self.ffn, self.vision_ffn = SwiGLU(width, hidden), SwiGLU(width, hidden)
        if self.vision is not None:
            for layer in self.vision.values():
                nn.init.zeros_(layer.weight)
        nn.init.zeros_(self.vision_ffn.down.weight)
        nn.init.zeros_(self.vision_ffn.down.bias)

    def forward(self, x: Tensor, vision_mask: Tensor, *, added_capacity: bool = True) -> Tensor:
        if (x.ndim != 3 or x.shape[-1] != self.width or min(x.shape[:2]) < 1
                or vision_mask.shape != x.shape[:2] or vision_mask.dtype != torch.bool
                or vision_mask.device != x.device or not torch.isfinite(x).all()):
            raise ValueError("finite [batch,tokens,width] and colocated boolean token mask required")
        mask = vision_mask.unsqueeze(-1).to(x.dtype)

        def project(key: str, value: Tensor) -> Tensor:
            base = self.shared[key](value)
            return (base + mask * self.vision[key](value)
                    if added_capacity and self.vision is not None else base)

        normalized = self.norm_attention(x)
        batch, tokens, width = x.shape
        q, k, v = (project(name, normalized).view(batch, tokens, self.heads, width // self.heads)
                   .transpose(1, 2) for name in "qkv")
        context = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        context = context.transpose(1, 2).reshape(batch, tokens, width)
        attended = x + project("o", context)
        # Both FFNs consume the SAME normalized input, not one another's output.
        normalized_ffn = self.norm_ffn(attended)
        output = attended + self.ffn(normalized_ffn)
        return output + mask * self.vision_ffn(normalized_ffn) if added_capacity else output


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device not in {"cpu", "cuda"} or (device == "cuda" and not torch.cuda.is_available()):
        raise ValueError("available CPU or real CUDA device required")
    torch.manual_seed(seed)
    block = InFusionBlock(16, 24).to(device)
    x = torch.randn(2, 6, 16, device=device)
    mask = torch.tensor([[True, True, False, False, False, False]], device=device).expand(2, -1)
    base = block(x, mask, added_capacity=False).detach()
    initial = block(x, mask).detach()
    target = base.clone()
    target[:, :2] += 0.3
    for parameter in list(block.shared.parameters()) + list(block.ffn.parameters()):
        parameter.requires_grad_(False)
    optimizer = torch.optim.AdamW([p for p in block.parameters() if p.requires_grad], lr=0.01)
    before = float(F.mse_loss(initial, target))
    for _ in range(16):
        optimizer.zero_grad()
        loss = F.mse_loss(block(x, mask), target)
        loss.backward()
        optimizer.step()
    after = float(F.mse_loss(block(x, mask), target).detach())
    text_mask = torch.zeros_like(mask)
    text_equal = torch.allclose(block(x, text_mask), block(x, text_mask, added_capacity=False))
    modified = x.clone()
    modified[:, 3:] += 10
    causal = torch.allclose(block(x, mask)[:, :3], block(modified, mask)[:, :3], atol=1e-5)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"training_mse_before": before, "training_mse_after": after,
                        "initial_max_difference": float((initial - base).abs().max())},
            "checks": {"zero_initialized_equivalence": bool(torch.equal(initial, base)),
                       "text_only_shared_path_unchanged": bool(text_equal),
                       "joint_attention_is_causal": bool(causal),
                       "added_capacity_optimized": after < before,
                       "vision_ffn_updated": bool(block.vision_ffn.down.weight.detach().abs().sum() > 0)}}
