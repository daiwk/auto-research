"""Extracted unchanged from auto_research.foundation_latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def taco_direction(gradient):
    """Exact column-wise one-sparse steepest direction used by TACO."""
    import torch

    if gradient.ndim != 2:
        raise ValueError("TACO applies its one-sparse rule to matrices")
    rows = gradient.abs().argmax(dim=0, keepdim=True)
    signs = gradient.gather(0, rows).sign()
    return torch.zeros_like(gradient).scatter_(0, rows, signs)

class TACO:
    """Minimal first-order TACO optimizer with low-precision column momentum."""

    def __init__(self, parameters, *, lr: float = 1e-3, beta: float = 0.9):
        import torch

        if lr <= 0 or not 0 <= beta < 1:
            raise ValueError("invalid TACO hyperparameters")
        self.parameters = list(parameters)
        self.lr = lr
        self.beta = beta
        self.state: dict[int, torch.Tensor] = {}

    def step(self):
        import torch

        with torch.no_grad():
            for parameter in self.parameters:
                if parameter.grad is None:
                    continue
                if parameter.ndim != 2:
                    parameter.add_(parameter.grad, alpha=-self.lr)
                    continue
                direction = taco_direction(parameter.grad)
                rows = parameter.grad.abs().argmax(dim=0)
                components = parameter.grad.gather(0, rows[None]).squeeze(0)
                momentum = self.state.get(id(parameter), torch.zeros_like(components, dtype=torch.float16))
                momentum.mul_(self.beta).add_(components.to(momentum.dtype), alpha=1 - self.beta)
                self.state[id(parameter)] = momentum
                update = direction * momentum.to(parameter.dtype).abs()[None]
                parameter.add_(update, alpha=-self.lr)

    @property
    def state_elements(self):
        return sum(value.numel() for value in self.state.values())
