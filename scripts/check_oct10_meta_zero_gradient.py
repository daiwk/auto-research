"""Finite-gradient edge check; numerical diagnostic, not model capability."""
import argparse
import json

import torch

from auto_research.post_training.oct10_objectives import virtual_adamw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    args = parser.parse_args()
    torch.manual_seed(42)
    model = torch.nn.Linear(2, 2).to(args.device)
    weight = torch.nn.Parameter(torch.tensor(1., device=args.device))
    optimizer = torch.optim.AdamW(model.parameters())
    loss = model(torch.ones(1, 2, device=args.device)).sum() * weight * 0
    virtual = virtual_adamw(model, optimizer, loss)
    outer = sum(parameter.square().sum() for parameter in virtual.values())
    gradient, = torch.autograd.grad(outer, weight)
    assert torch.isfinite(gradient) and gradient == 0
    print(json.dumps({"seed": 42, "zero_gradient_hypergradient": float(gradient),
                      "finite": bool(torch.isfinite(gradient)), "diagnostic_only": True}))


if __name__ == "__main__":
    main()
