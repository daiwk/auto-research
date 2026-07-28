from __future__ import annotations


def zeropower_via_newton_schulz(gradient, torch, steps: int = 5):
    """Approximate the polar factor used by Muon with quintic Newton-Schulz."""
    if gradient.ndim != 2:
        raise ValueError("Muon orthogonalization expects a matrix gradient")
    values = gradient.float()
    transposed = values.shape[0] > values.shape[1]
    if transposed:
        values = values.T
    values = values / (values.norm() + 1e-7)
    for _ in range(steps):
        gram = values @ values.T
        values = (
            3.4445 * values
            - 4.7750 * gram @ values
            + 2.0315 * gram @ gram @ values
        )
    return (values.T if transposed else values).to(gradient.dtype)


class Muon:
    """Muon for hidden matrices plus AdamW for embeddings/vectors.

    The split follows the Moonlight recipe: Muon updates internal 2-D matrices,
    while AdamW retains token embeddings, output heads, norms and biases.
    """

    def __init__(
        self,
        named_parameters,
        *,
        learning_rate: float,
        torch,
        momentum: float = 0.95,
        weight_decay: float = 0.1,
    ):
        self.torch = torch
        self.momentum = momentum
        muon, adamw = [], []
        for name, parameter in named_parameters:
            if (
                parameter.requires_grad
                and parameter.ndim == 2
                and "token" not in name
                and "output" not in name
            ):
                muon.append(parameter)
            elif parameter.requires_grad:
                adamw.append(parameter)
        self.muon_parameters = muon
        self.state = {}
        self.muon_group = {
            "params": muon,
            "lr": learning_rate,
            "weight_decay": weight_decay,
        }
        self.adamw = torch.optim.AdamW(
            adamw, lr=learning_rate, weight_decay=weight_decay
        )
        self.param_groups = [self.muon_group, *self.adamw.param_groups]
        self.last_orthogonality_error = 0.0

    def zero_grad(self, set_to_none: bool = True):
        for parameter in self.muon_parameters:
            if parameter.grad is not None:
                if set_to_none:
                    parameter.grad = None
                else:
                    parameter.grad.zero_()
        self.adamw.zero_grad(set_to_none=set_to_none)

    def add_param_group(self, group):
        self.adamw.add_param_group(group)
        self.param_groups = [self.muon_group, *self.adamw.param_groups]

    def step(self):
        torch = self.torch
        errors = []
        with torch.no_grad():
            for parameter in self.muon_parameters:
                if parameter.grad is None:
                    continue
                state = self.state.setdefault(
                    parameter, {"momentum_buffer": torch.zeros_like(parameter)}
                )
                buffer = state["momentum_buffer"]
                buffer.mul_(self.momentum).add_(
                    parameter.grad, alpha=1 - self.momentum
                )
                update = zeropower_via_newton_schulz(buffer, torch)
                scale = max(1.0, parameter.shape[0] / parameter.shape[1]) ** 0.5
                if self.muon_group["weight_decay"]:
                    parameter.mul_(
                        1
                        - self.muon_group["lr"]
                        * self.muon_group["weight_decay"]
                    )
                parameter.add_(
                    update,
                    alpha=-self.muon_group["lr"] * scale,
                )
                gram = (
                    update @ update.T
                    if update.shape[0] <= update.shape[1]
                    else update.T @ update
                )
                eye = torch.eye(
                    gram.shape[0], device=gram.device, dtype=gram.dtype
                )
                errors.append(float((gram - eye).abs().mean().cpu()))
        self.adamw.step()
        self.last_orthogonality_error = (
            sum(errors) / len(errors) if errors else 0.0
        )
