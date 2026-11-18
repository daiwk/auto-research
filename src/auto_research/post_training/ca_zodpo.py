"""CA-ZODPO v1 Eq.3–5; activation subspace and low-rank ZO update."""

import torch
from ._nov18_contracts import receipt, scalar, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def contrastive_basis(chosen, rejected, *, rank, generator, power_iterations=2):
    tensor(chosen, "chosen", ndim=2)
    tensor(rejected, "rejected", shape=chosen.shape, device=chosen.device)
    if (
        type(rank) is not int
        or not 1 <= rank <= min(chosen.shape)
        or type(power_iterations) is not int
        or power_iterations < 0
    ):
        raise ValueError("valid rank and nonnegative power iterations required")
    with torch.no_grad():
        delta = chosen.detach() - rejected.detach()
        h = torch.cat([delta.mean(-1, keepdim=True), delta], -1)
        if int(torch.linalg.matrix_rank(h)) < rank:
            raise ValueError("requested rank unsupported by contrastive activations")
        omega = torch.randn(h.shape[1], rank, generator=generator, dtype=h.dtype).to(h.device)
        q = torch.linalg.qr(h @ omega, mode="reduced").Q
        for _ in range(power_iterations):
            q = torch.linalg.qr(h @ (h.T @ q), mode="reduced").Q
    return q


def direction(coefficients, basis):
    tensor(coefficients, "coefficients", ndim=2)
    tensor(basis, "basis", ndim=2, device=coefficients.device)
    if coefficients.shape[1] != basis.shape[1] or not torch.allclose(
        basis.T @ basis,
        torch.eye(basis.shape[1], device=basis.device, dtype=basis.dtype),
        atol=1e-6,
    ):
        raise ValueError("rank-matched orthonormal basis required")
    return coefficients @ basis.T / (basis.shape[1] ** 0.5)


def central_difference(loss_at, weight, perturbation, *, epsilon):
    tensor(weight, "weight", ndim=2)
    tensor(perturbation, "perturbation", shape=weight.shape, device=weight.device)
    eps = scalar(epsilon, "epsilon", lower=0, strict_lower=True)
    with torch.no_grad():
        plus = loss_at(weight + eps * perturbation)
        minus = loss_at(weight - eps * perturbation)
    tensor(plus, "plus")
    tensor(minus, "minus")
    if plus.numel() != 1 or minus.numel() != 1:
        raise ValueError("scalar loss callback required")
    return (plus - minus) / (2 * eps)


def momentum_update(
    weight,
    basis,
    coefficients,
    slope,
    *,
    learning_rate,
    momentum,
    previous=None,
    previous_basis=None,
):
    eta = scalar(learning_rate, "learning_rate", lower=0)
    mu = scalar(momentum, "momentum", lower=0, upper=1)
    direction(coefficients, basis)
    tensor(weight, "weight", shape=(coefficients.shape[0], basis.shape[0]), device=basis.device)
    tensor(slope, "slope")
    if slope.numel() != 1:
        raise ValueError("scalar finite-difference slope required")
    if previous is None:
        if previous_basis is not None:
            raise ValueError("incomplete previous state")
        transported = torch.zeros_like(coefficients)
    else:
        tensor(previous, "previous", ndim=2, device=basis.device)
        tensor(previous_basis, "previous_basis", ndim=2, device=basis.device)
        if (
            previous.shape[0] != coefficients.shape[0]
            or previous.shape[1] != previous_basis.shape[1]
            or previous_basis.shape[0] != basis.shape[0]
        ):
            raise ValueError("incompatible old basis/momentum")
        transported = previous @ (previous_basis.T @ basis)
    state = mu * transported + (1 - mu) * slope.detach() * coefficients.detach()
    return weight.detach() - eta * direction(state, basis.detach()), state.detach()


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    c = torch.randn(5, 8, generator=g, dtype=torch.float64).to(device)
    r = torch.randn(5, 8, generator=g, dtype=torch.float64).to(device)
    a = contrastive_basis(c, r, rank=2, generator=g)
    coeff = torch.randn(3, 2, generator=g, dtype=torch.float64).to(device)
    w = torch.randn(3, 5, generator=g, dtype=torch.float64).to(device)
    perturb = direction(coeff, a)
    slope = central_difference(lambda x: x.square().sum() / 2, w, perturb, epsilon=1e-4)
    exact = (w * perturb).sum()
    new, state = momentum_update(w, a, coeff, slope, learning_rate=0.01, momentum=0.5)
    flipped = a @ torch.tensor([[0.0, -1.0], [1.0, 0.0]], device=device, dtype=a.dtype)
    _, transport = momentum_update(
        w,
        flipped,
        torch.zeros_like(coeff),
        torch.tensor(0.0, device=device),
        learning_rate=0,
        momentum=1,
        previous=state,
        previous_basis=a,
    )
    return receipt(
        seed,
        "l1_mechanism",
        {
            "orthonormal_contrastive_basis": bool(
                torch.allclose(a.T @ a, torch.eye(2, device=device, dtype=a.dtype), atol=1e-10)
            ),
            "two_point_slope_matches_oracle": bool(torch.allclose(slope, exact, atol=1e-8)),
            "basis_transport_preserves_reconstructed_momentum": bool(
                torch.allclose(direction(state, a), direction(transport, flipped), atol=1e-10)
            ),
            "low_rank_update_executes": bool((new - w).abs().sum() > 0),
        },
        {
            "finite_difference_slope": slope.item(),
            "slope_error": float((slope - exact).abs()),
            "momentum_elements": state.numel(),
            "full_weight_elements": w.numel(),
        },
    )
