"""LIDAS b=4 middle growth with actual AdamW-state inheritance (2512.08819).

This is a layer/optimizer transformation, not a pretrained model or evidence of
reasoning improvement. Figure 2 resolves the inclusive-index typo in §3.1.
"""
from __future__ import annotations

from copy import deepcopy

import torch
from torch import nn

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/lidas-a100-20261113.json"


def growth_indices(depth: int) -> tuple[tuple[int, ...], int]:
    """Return four source layers and insertion boundary (zero-based, exclusive).

    For L=8, copy [2,3,4,5] after layer 5. The resulting order is
    0,1,2,3,4,5,2',3',4',5',6,7. For odd block counts LIDAS=MIDAS.
    """
    if isinstance(depth, bool) or not isinstance(depth, int) or depth < 4 or depth % 4:
        raise ValueError("depth must be a positive multiple of the paper's block size four")
    start = depth // 2 - 2
    return tuple(range(start, start + 4)), start + 4


def prop1_schedule(total_steps: int, stages: int) -> tuple[int, ...]:
    """PROP-1: stage durations proportional to 1,...,S; conserve integer budget.

    Largest-remainder rounding is an explicit local convention; the continuous
    formula is from Appendix A. Caller must keep the global LR step unchanged.
    """
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 1 for x in [total_steps, stages]):
        raise ValueError("positive integer steps and stages required")
    if total_steps < stages:
        raise ValueError("each stage requires a training step")
    denominator = stages * (stages + 1) // 2
    floors = [total_steps * i // denominator for i in range(1, stages + 1)]
    order = sorted(range(stages), key=lambda j: (-(total_steps * (j + 1) % denominator), j))
    for i in order[:total_steps - sum(floors)]:
        floors[i] += 1
    if min(floors) < 1:
        raise ValueError("budget too small for nonempty PROP-1 stages")
    return tuple(floors)


def grow_layers(layers: nn.ModuleList, optimizer: torch.optim.AdamW) -> nn.ModuleList:
    """Deep-copy the centered four layers and their AdamW moments, without aliases.

    Existing parameters, groups and state survive. Copied parameters join their
    source group, so a scheduler need not restart. Embeddings/head outside this
    ModuleList are untouched. Caller replaces its layer list with the return value.
    """
    if not isinstance(layers, nn.ModuleList) or not isinstance(optimizer, torch.optim.AdamW):
        raise TypeError("ModuleList and AdamW required")
    sources, boundary = growth_indices(len(layers))
    existing = [p for layer in layers for p in layer.parameters()]
    if len({id(p) for p in existing}) != len(existing):
        raise ValueError("tied parameters across layers need an explicit model-specific policy")
    groups = {id(p): g for g in optimizer.param_groups for p in g["params"]}
    if any(id(p) not in groups for p in existing):
        raise ValueError("every layer parameter must belong to the optimizer")
    copies = [deepcopy(layers[i]) for i in sources]
    pairs = [(old, new) for i, copy in zip(sources, copies, strict=True)
             for old, new in zip(layers[i].parameters(), copy.parameters(), strict=True)]
    inherited = [(old, new, deepcopy(optimizer.state.get(old, {}))) for old, new in pairs]
    for old, new, state in inherited:
        groups[id(old)]["params"].append(new)
        if state:
            optimizer.state[new] = state
    return nn.ModuleList([*layers[:boundary], *copies, *layers[boundary:]])


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    target = torch.device(device)
    if target.type not in {"cpu", "cuda"}:
        raise ValueError("CPU/CUDA required")
    with torch.random.fork_rng(devices=[] if target.type == "cpu" else [target.index or torch.cuda.current_device()]):
        torch.manual_seed(seed)
        layers = nn.ModuleList([nn.Linear(3, 3, bias=False, device=target) for _ in range(8)])
        optimizer = torch.optim.AdamW(layers.parameters(), lr=.01)
        x = torch.arange(9, device=target, dtype=torch.float32).reshape(3, 3) / 9
        nn.Sequential(*layers)(x).square().sum().backward()
        optimizer.step(); optimizer.zero_grad(set_to_none=True)
        grown = grow_layers(layers, optimizer)
        old, new = next(layers[2].parameters()), next(grown[6].parameters())
        inherited_equal = torch.equal(optimizer.state[old]["exp_avg"], optimizer.state[new]["exp_avg"])
        independent = old.data_ptr() != new.data_ptr() and optimizer.state[old]["exp_avg"].data_ptr() != optimizer.state[new]["exp_avg"].data_ptr()
        loss = nn.Sequential(*grown)(x).square().sum()
        loss.backward()
        grad = new.grad.detach().clone()
        before = new.detach().clone()
        optimizer.step()
        checks = {"depth_increased_by_four": len(grown) == 12,
                  "inherited_adam_moments": inherited_equal,
                  "no_parameter_or_moment_alias": independent,
                  "copied_layer_receives_gradient": bool(torch.isfinite(grad).all()) and bool(grad.abs().sum() > 0),
                  "copied_layer_updates": not torch.equal(before, new),
                  "device_is_requested": new.device.type == target.type,
                  "prop1_conserves_steps": sum(prop1_schedule(170000, 8)) == 170000}
        return {"seed": seed, "device": str(target), "metrics": {"grown_depth": len(grown), "loss": float(loss.detach()), "copied_gradient_norm": float(grad.norm())}, "checks": checks,
                "diagnostic_only": True, "evaluation_tier": "l1_mechanism"}
