"""Residual-corrected subspace optimizers from arXiv:2610.19844v1.

``beta`` is the paper's *new-gradient* coefficient, not torch SGD momentum.
Matrices are transposed internally for a right projection when rows > columns.
Only the basis and low-rank momentum persist; the residual is never a state.
"""
from __future__ import annotations

import math
from collections.abc import Iterable
from typing import Any, Callable

import torch
from torch import Tensor
from torch.optim import Optimizer


def _work_dtype(tensor: Tensor) -> torch.dtype:
    return torch.float64 if tensor.dtype == torch.float64 else torch.float32


def matrix_sign(matrix: Tensor, *, method: str = "svd", steps: int = 5) -> Tensor:
    """Rectangular polar sign, with zero singular directions kept zero.

    SVD is the exact reference used by Algorithms 3/4. ``newton_schulz`` is
    the five-step quintic approximation used by practical Muon, not an exact
    polar factor; callers must not advertise its singular values as all one.
    """
    if matrix.ndim != 2 or not matrix.is_floating_point():
        raise ValueError("matrix_sign requires a real floating-point matrix")
    if method not in {"svd", "newton_schulz"}:
        raise ValueError("sign method must be svd or newton_schulz")
    if not isinstance(steps, int) or steps < 1:
        raise ValueError("Newton-Schulz steps must be positive")
    value = matrix.to(dtype=_work_dtype(matrix))
    if not bool(torch.isfinite(value).all()):
        raise ValueError("matrix sign received a non-finite value")
    largest = value.abs().max()
    if float(largest) == 0:
        return torch.zeros_like(value)
    # Sign is positively scale invariant. Normalize before computing a norm
    # so valid very small/large FP32 gradients do not underflow/overflow it.
    value = value / largest
    norm = torch.linalg.vector_norm(value)
    if method == "svd":
        left, singular, right = torch.linalg.svd(value, full_matrices=False)
        tolerance = torch.finfo(value.dtype).eps * max(value.shape) * singular.max()
        return (left * (singular > tolerance).to(value.dtype)) @ right
    transposed = value.shape[0] > value.shape[1]
    value = value.T if transposed else value
    value = value / norm.clamp_min(torch.finfo(value.dtype).tiny)
    for _ in range(steps):
        gram = value @ value.T
        value = 3.4445 * value + (-4.7750 * gram + 2.0315 * (gram @ gram)) @ value
    return value.T if transposed else value


def _basis(gradient: Tensor, rank: int, previous: Tensor | None, method: str) -> Tensor:
    rows = gradient.shape[0]
    if rank == rows:
        return torch.eye(rows, dtype=gradient.dtype, device=gradient.device)
    if float(torch.linalg.vector_norm(gradient)) == 0:
        if previous is not None:
            return previous.clone()
        return torch.eye(rows, dtype=gradient.dtype, device=gradient.device)[:, :rank].clone()
    if method == "warm_start" and previous is not None:
        projected = previous.T @ gradient
        row_norms = torch.linalg.vector_norm(projected, dim=1, keepdim=True)
        normalized = projected / row_norms.clamp_min(torch.finfo(gradient.dtype).tiny)
        candidate = gradient @ normalized.T
        # A completely orthogonal new gradient cannot be tracked by a zero
        # warm start. An exact SVD fallback is explicit, not a silent NaN.
        if float(torch.linalg.vector_norm(candidate)) > 0:
            return torch.linalg.qr(candidate, mode="reduced").Q[:, :rank]
    # A view would retain the full SVD-U storage and defeat the memory claim.
    return torch.linalg.svd(gradient, full_matrices=False).U[:, :rank].clone()


class _ResidualOptimizer(Optimizer):
    """Shared mechanics; public construction is through SMRC or PMRC."""

    algorithm: str

    def __init__(
        self,
        params: Iterable[Tensor] | Iterable[dict[str, Any]],
        *,
        lr: float,
        beta: float,
        gamma: float,
        rank: int,
        refresh_interval: int | None,
        projection: str,
        basis_method: str,
        weight_decay: float,
        adamw_betas: tuple[float, float],
        eps: float,
        variant: str,
        nesterov: bool,
        sign_method: str,
        ns_steps: int,
        residual_cap: float,
    ):
        defaults = dict(
            lr=lr, beta=beta, gamma=gamma, rank=rank,
            refresh_interval=refresh_interval, projection=projection,
            basis_method=basis_method, weight_decay=weight_decay,
            adamw_betas=adamw_betas, eps=eps, variant=variant,
            nesterov=nesterov, sign_method=sign_method, ns_steps=ns_steps,
            residual_cap=residual_cap, use_subspace=True,
        )
        super().__init__(params, defaults)
        for group in self.param_groups:
            self._validate_group(group)
            for param in group["params"]:
                if not param.is_floating_point():
                    raise ValueError("SMRC/PMRC support real floating-point parameters only")

    def _validate_group(self, group: dict[str, Any]) -> None:
        for name in ("lr", "gamma", "eps", "residual_cap"):
            if not math.isfinite(group[name]) or group[name] < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if group["gamma"] <= 0 or group["eps"] <= 0 or group["residual_cap"] <= 0:
            raise ValueError("gamma, eps and residual_cap must be positive")
        if self.algorithm == "smrc" and group["gamma"] > 1:
            raise ValueError("SMRC requires gamma in (0, 1]")
        if not 0 < group["beta"] < 1:
            raise ValueError("beta is the new-gradient coefficient and must be in (0, 1)")
        if not isinstance(group["rank"], int) or group["rank"] < 1:
            raise ValueError("rank must be a positive integer")
        interval = group["refresh_interval"]
        if interval is not None and (not isinstance(interval, int) or interval < 1):
            raise ValueError("refresh_interval must be None or a positive integer")
        if group["projection"] not in {"auto", "left", "right"}:
            raise ValueError("projection must be auto, left or right")
        if group["basis_method"] not in {"svd", "warm_start"}:
            raise ValueError("basis_method must be svd or warm_start")
        if group["variant"] not in {"theory", "practical"}:
            raise ValueError("variant must be theory or practical")
        if group["sign_method"] not in {"svd", "newton_schulz"}:
            raise ValueError("sign_method must be svd or newton_schulz")
        if not isinstance(group["ns_steps"], int) or group["ns_steps"] < 1:
            raise ValueError("ns_steps must be positive")
        if not math.isfinite(group["weight_decay"]) or group["weight_decay"] < 0:
            raise ValueError("weight_decay must be finite and nonnegative")
        if len(group["adamw_betas"]) != 2 or any(
            not 0 <= value < 1 for value in group["adamw_betas"]
        ):
            raise ValueError("adamw_betas must contain two coefficients in [0, 1)")

    def load_state_dict(self, state_dict: dict[str, Any]) -> None:
        super().load_state_dict(state_dict)
        # Optimizer.load_state_dict casts floating state to the parameter dtype;
        # restore from the ORIGINAL saved tensor, avoiding a lossy BF16 roundtrip.
        for group, saved_group in zip(self.param_groups, state_dict["param_groups"], strict=True):
            self._validate_group(group)
            for param, saved_id in zip(group["params"], saved_group["params"], strict=True):
                for name in ("basis", "momentum", "exp_avg", "exp_avg_sq"):
                    value = state_dict["state"].get(saved_id, {}).get(name)
                    if isinstance(value, Tensor):
                        self.state[param][name] = value.to(
                            device=param.device, dtype=_work_dtype(param)
                        )

    @torch.no_grad()
    def step(self, closure: Callable[[], Tensor] | None = None) -> Tensor | None:
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        # Validate every gradient before mutating any parameter or state.
        for group in self.param_groups:
            self._validate_group(group)
            for param in group["params"]:
                grad = param.grad
                if grad is None:
                    continue
                if grad.is_sparse:
                    raise ValueError("sparse gradients are not supported")
                if not bool(torch.isfinite(grad).all()):
                    raise ValueError("non-finite gradients are not supported")
        for group in self.param_groups:
            for param in group["params"]:
                if param.grad is None:
                    continue
                if param.ndim != 2 or not group["use_subspace"]:
                    self._adamw_step(param, group)
                else:
                    self._matrix_step(param, group)
        return loss

    def _adamw_step(self, param: Tensor, group: dict[str, Any]) -> None:
        """Explicit fallback for vectors, biases, embeddings and LM heads."""
        state = self.state[param]
        grad = param.grad.to(dtype=_work_dtype(param))
        if not state:
            state.update(step=0, exp_avg=torch.zeros_like(grad), exp_avg_sq=torch.zeros_like(grad))
        state["step"] += 1
        first, second = group["adamw_betas"]
        state["exp_avg"].mul_(first).add_(grad, alpha=1 - first)
        state["exp_avg_sq"].mul_(second).addcmul_(grad, grad, value=1 - second)
        unbiased = state["exp_avg"] / (1 - first ** state["step"])
        denominator = (state["exp_avg_sq"] / (1 - second ** state["step"])).sqrt()
        param.mul_(1 - group["lr"] * group["weight_decay"])
        param.add_((unbiased / (denominator + group["eps"])).to(param.dtype), alpha=-group["lr"])

    def _matrix_step(self, param: Tensor, group: dict[str, Any]) -> None:
        state = self.state[param]
        transpose = group["projection"] == "right" or (
            group["projection"] == "auto" and param.shape[0] > param.shape[1]
        )
        grad = param.grad.to(dtype=_work_dtype(param))
        oriented = grad.T if transpose else grad
        rank = min(group["rank"], *oriented.shape)
        if not state:
            state.update(step=0, stage_steps=0, stage=0, refresh_pending=True)
        if state["refresh_pending"]:
            previous = state.get("basis")
            state["basis"] = _basis(oriented, rank, previous, group["basis_method"])
            state["momentum"] = torch.zeros(
                (rank, oriented.shape[1]), device=param.device, dtype=oriented.dtype
            )
            state["refresh_pending"] = False
            state["stage"] += 1
        basis = state["basis"]
        projected = basis.T @ oriented
        residual = oriented - basis @ projected
        momentum = state["momentum"]
        momentum.mul_(1 - group["beta"]).add_(projected, alpha=group["beta"])
        if self.algorithm == "smrc":
            low_rank_direction = momentum
        else:
            direction = (1 - group["beta"]) * momentum + group["beta"] * projected \
                if group["nesterov"] else momentum
            low_rank_direction = matrix_sign(
                direction, method=group["sign_method"], steps=group["ns_steps"]
            )
        projected_update = basis @ low_rank_direction
        gamma = group["gamma"]
        scale = 1.0
        if self.algorithm == "pmrc" and group["variant"] == "practical":
            numerator = projected_update.square().sum()
            denominator = residual.square().sum().clamp_min(1e-30)
            gamma = min(gamma, float(group["residual_cap"] * (numerator / denominator).sqrt()))
            scale = 0.2 * math.sqrt(max(param.shape))
        update = projected_update + gamma * residual
        update = update.T if transpose else update
        param.mul_(1 - group["lr"] * group["weight_decay"])
        param.add_(update.to(param.dtype), alpha=-group["lr"] * scale)
        state["step"] += 1
        state["stage_steps"] += 1
        state["last_residual_coefficient"] = gamma
        interval = group["refresh_interval"]
        if interval is not None and state["stage_steps"] == interval:
            if self.algorithm == "smrc":
                # Algorithm 2 line 9: this is a *parameter* correction, not
                # momentum transport/reprojection. Do it before next backward.
                correction = basis @ momentum
                correction = correction.T if transpose else correction
                param.add_(correction.to(param.dtype), alpha=(
                    -group["lr"] * (1 - group["beta"]) / group["beta"]
                ))
            # Algorithm 4 deliberately has no parameter boundary correction.
            momentum.zero_()
            state["stage_steps"] = 0
            state["refresh_pending"] = True


class SMRC(_ResidualOptimizer):
    """Algorithms 1/2: subspace EMA momentum + orthogonal residual gradient.

    Stage transitions execute eagerly at the end of ``refresh_interval``-th
    step. Therefore the next forward/backward sees the corrected parameter.
    If a run stops exactly at a boundary, its final parameter is the next
    stage's initial iterate (including the correction), not the preceding
    stage's uncorrected terminal iterate. ``None`` means one fixed-basis stage.
    Non-matrices, and groups with ``use_subspace=False``, use explicit AdamW.
    """

    algorithm = "smrc"

    def __init__(
        self, params, lr: float = 0.01, *, beta: float = 0.1, gamma: float = 0.8,
        rank: int = 8, refresh_interval: int | None = 50,
        projection: str = "auto", weight_decay: float = 0.0,
        adamw_betas: tuple[float, float] = (0.9, 0.999), eps: float = 1e-8,
    ):
        super().__init__(
            params, lr=lr, beta=beta, gamma=gamma, rank=rank,
            refresh_interval=refresh_interval, projection=projection,
            basis_method="svd", weight_decay=weight_decay,
            adamw_betas=adamw_betas, eps=eps, variant="theory", nesterov=False,
            sign_method="svd", ns_steps=5, residual_cap=4.0,
        )


class PMRC(_ResidualOptimizer):
    """Algorithms 3/4 or the separately labelled Appendix E.2.1 variant.

    ``variant='theory'``: exact rectangular sign, SVD bases, no Nesterov or
    shape scaling/cap by default. ``variant='practical'``: cap, shape scaling,
    warm-start row-normalized QR, Nesterov and 5-step NS defaults. QR uses
    torch's stable reduced QR, not the authors' SCQR speed kernel; no matching
    projector-latency claim is made. Embeddings/heads must be opt-out groups.
    """

    algorithm = "pmrc"

    def __init__(
        self, params, lr: float = 0.01, *, beta: float = 0.05, gamma: float = 1.0,
        rank: int = 8, refresh_interval: int | None = 50,
        projection: str = "auto", variant: str = "theory",
        basis_method: str | None = None, nesterov: bool | None = None,
        sign_method: str | None = None, ns_steps: int = 5,
        residual_cap: float = 4.0, weight_decay: float = 0.0,
        adamw_betas: tuple[float, float] = (0.9, 0.999), eps: float = 1e-8,
    ):
        practical = variant == "practical"
        super().__init__(
            params, lr=lr, beta=beta, gamma=gamma, rank=rank,
            refresh_interval=refresh_interval, projection=projection,
            basis_method=basis_method or ("warm_start" if practical else "svd"),
            weight_decay=weight_decay, adamw_betas=adamw_betas, eps=eps,
            variant=variant, nesterov=practical if nesterov is None else nesterov,
            sign_method=sign_method or ("newton_schulz" if practical else "svd"),
            ns_steps=ns_steps, residual_cap=residual_cap,
        )
