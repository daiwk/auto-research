"""Small dependency-free LoRA adapter for bounded CUDA diagnostics."""

from __future__ import annotations

from contextlib import contextmanager
import math


def attach_lora(model, *, target_modules=("q_proj", "v_proj"), rank: int = 8, alpha: float = 16.0):
    import torch

    if rank < 1 or alpha <= 0:
        raise ValueError("rank and alpha must be positive")
    for parameter in model.parameters():
        parameter.requires_grad_(False)

    class LowRankLinear(torch.nn.Module):
        def __init__(self, base):
            super().__init__()
            self.base = base
            self.a = torch.nn.Parameter(torch.empty(rank, base.in_features, device=base.weight.device, dtype=torch.float32))
            self.b = torch.nn.Parameter(torch.zeros(base.out_features, rank, device=base.weight.device, dtype=torch.float32))
            torch.nn.init.kaiming_uniform_(self.a, a=math.sqrt(5))
            self.scale = alpha / rank
            self.enabled = True

        def forward(self, inputs):
            output = self.base(inputs)
            if not self.enabled:
                return output
            update = torch.nn.functional.linear(
                torch.nn.functional.linear(inputs.float(), self.a), self.b,
            ) * self.scale
            return output + update.to(dtype=output.dtype)

    replaced = 0
    for module in model.modules():
        for name, child in list(module.named_children()):
            if name in target_modules and isinstance(child, torch.nn.Linear):
                setattr(module, name, LowRankLinear(child))
                replaced += 1
    if not replaced:
        raise ValueError(f"no linear modules matched {target_modules}")
    return model


@contextmanager
def disabled_adapters(model):
    adapters = [module for module in model.modules() if hasattr(module, "enabled") and hasattr(module, "scale")]
    previous = [module.enabled for module in adapters]
    try:
        for module in adapters:
            module.enabled = False
        yield
    finally:
        for module, enabled in zip(adapters, previous, strict=True):
            module.enabled = enabled
