"""P²-MOPD's module-granularity two-channel update (arXiv:2611.03953).

An L1 optimizer component, not a language model, rollout engine, domain-teacher
bank or implementation of the full MOPD surrogate. Inputs are public numerical
weights/gradients. No model-capability or Evolve-promotion claim is made.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor, nn

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/p2-mopd-a100-20261104.json"


class PriorModule:
    """One materialized projection W and frozen task directions, Eq. 4--5."""

    def __init__(self, base: Tensor, task_vectors: Tensor, coefficients: Tensor):
        if base.ndim < 1 or base.numel() == 0 or not base.is_floating_point():
            raise ValueError("nonempty floating base tensor required")
        if (task_vectors.ndim != base.ndim + 1 or task_vectors.shape[1:] != base.shape
                or task_vectors.shape[0] < 1 or coefficients.shape != (task_vectors.shape[0],)):
            raise ValueError("one coefficient and matching task tensor per expert required")
        for value in (base, task_vectors, coefficients):
            if value.device != base.device or value.dtype != base.dtype or not bool(torch.isfinite(value).all()):
                raise ValueError("finite tensors with identical floating dtype/device required")
        self.task_vectors = task_vectors.detach().clone()
        self.coefficients = nn.Parameter(coefficients.detach().clone())
        self.weight = nn.Parameter(base.detach().clone() + self._mixture(self.coefficients.detach()))

    def _mixture(self, coefficients: Tensor) -> Tensor:
        return (self.task_vectors * coefficients.reshape((-1,) + (1,) * self.weight_rank)).sum(0)

    @property
    def weight_rank(self) -> int:
        return self.task_vectors.ndim - 1

    def equivalent_base(self) -> Tensor:
        """Recover B for auditing only; optimization stores materialized W."""
        return self.weight.detach() - self._mixture(self.coefficients.detach())


class ParameterPriorOptimizer:
    """Algorithm 1 / Appendix B, module-level coefficients and zero decay.

    Both channels consume the same pre-update gradient. Coefficient gradients
    are computed BEFORE global weight clipping. The two channels have separate
    global clip budgets and Adam states. A non-finite batch changes no weights,
    coefficients or optimizer states; there is no partial-channel update.
    """

    def __init__(self, modules: list[PriorModule], *, other_parameters=(),
                 lr_weight: float = 1e-3, lr_coefficient: float = 1e-2,
                 weight_clip: float = 1., coefficient_clip: float = 1.):
        if not modules or any(not isinstance(module, PriorModule) for module in modules):
            raise ValueError("at least one prior module required")
        if any(not math.isfinite(value) or value <= 0 for value in
               (lr_weight, lr_coefficient, weight_clip, coefficient_clip)):
            raise ValueError("finite positive learning rates and clipping budgets required")
        self.modules = list(modules)
        self.weight_parameters = [module.weight for module in modules] + list(other_parameters)
        self.coefficient_parameters = [module.coefficients for module in modules]
        parameters = self.weight_parameters + self.coefficient_parameters
        if len({id(parameter) for parameter in parameters}) != len(parameters):
            raise ValueError("optimizer channels cannot alias or repeat parameters")
        if any(not isinstance(parameter, nn.Parameter) or not parameter.requires_grad for parameter in parameters):
            raise ValueError("trainable leaf parameters required")
        if any(parameter.device != parameters[0].device or parameter.dtype != parameters[0].dtype
               for parameter in parameters):
            raise ValueError("one shared parameter device and dtype required")
        self.weight_clip, self.coefficient_clip = weight_clip, coefficient_clip
        self.weight_optimizer = torch.optim.AdamW(self.weight_parameters, lr=lr_weight, weight_decay=0.)
        self.coefficient_optimizer = torch.optim.Adam(self.coefficient_parameters, lr=lr_coefficient)

    def zero_grad(self) -> None:
        self.weight_optimizer.zero_grad(set_to_none=True)
        self.coefficient_optimizer.zero_grad(set_to_none=True)

    @torch.no_grad()
    def step(self) -> bool:
        if any(module.weight.grad is None for module in self.modules):
            raise ValueError("backward must supply a gradient for every projection")
        gradients = [parameter.grad for parameter in self.weight_parameters if parameter.grad is not None]
        if any(not bool(torch.isfinite(gradient).all()) for gradient in gradients):
            return False
        coefficient_gradients = [
            (module.task_vectors * module.weight.grad.unsqueeze(0)).flatten(1).sum(-1)
            for module in self.modules
        ]
        if any(not bool(torch.isfinite(gradient).all()) for gradient in coefficient_gradients):
            return False
        # Check both norms before clipping or modifying either optimizer state.
        for channel in (gradients, coefficient_gradients):
            norms = torch.stack([gradient.norm() for gradient in channel])
            if not bool(torch.isfinite(norms.norm())):
                return False
        old_coefficients = [module.coefficients.detach().clone() for module in self.modules]
        for module, gradient in zip(self.modules, coefficient_gradients):
            module.coefficients.grad = gradient
        torch.nn.utils.clip_grad_norm_(self.weight_parameters, self.weight_clip, error_if_nonfinite=True)
        torch.nn.utils.clip_grad_norm_(self.coefficient_parameters, self.coefficient_clip, error_if_nonfinite=True)
        self.weight_optimizer.step()
        self.coefficient_optimizer.step()
        for module, previous in zip(self.modules, old_coefficients):
            module.weight.add_(module._mixture(module.coefficients - previous))
        return True


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Five-step explicit/materialized equivalence, not teacher recovery."""
    generator = torch.Generator(device="cpu").manual_seed(seed)
    base = torch.randn(3, 4, generator=generator, dtype=torch.float64).to(device)
    directions = torch.randn(2, 3, 4, generator=generator, dtype=torch.float64).to(device)
    coefficients = torch.full((2,), .5, dtype=torch.float64, device=device)
    module = PriorModule(base, directions, coefficients)
    optimizer = ParameterPriorOptimizer([module], lr_weight=.03, lr_coefficient=.04,
                                        weight_clip=.4, coefficient_clip=.2)
    explicit_base, explicit_alpha = nn.Parameter(base.clone()), nn.Parameter(coefficients.clone())
    reference_weight = torch.optim.AdamW([explicit_base], lr=.03, weight_decay=0.)
    reference_alpha = torch.optim.Adam([explicit_alpha], lr=.04)
    target = torch.randn(3, 4, generator=generator, dtype=torch.float64).to(device)
    initial = float((module.weight.detach() - target).square().mean())
    max_error = 0.
    for _ in range(5):
        optimizer.zero_grad(); reference_weight.zero_grad(); reference_alpha.zero_grad()
        (module.weight - target).square().mean().backward()
        explicit = explicit_base + (directions * explicit_alpha[:, None, None]).sum(0)
        (explicit - target).square().mean().backward()
        torch.nn.utils.clip_grad_norm_([explicit_base], .4)
        torch.nn.utils.clip_grad_norm_([explicit_alpha], .2)
        reference_weight.step(); reference_alpha.step()
        if not optimizer.step():
            raise ValueError("finite synthetic diagnostic was unexpectedly rejected")
        reference = explicit_base + (directions * explicit_alpha[:, None, None]).sum(0)
        max_error = max(max_error, float((module.weight - reference).detach().abs().max()))
    final = float((module.weight.detach() - target).square().mean())
    alpha_change = float((module.coefficients.detach() - coefficients).norm())
    base_change = (module.equivalent_base() - base).flatten()
    basis = directions.flatten(1).T
    outside_span = float((base_change - basis @ torch.linalg.pinv(basis) @ base_change).norm())
    before_weight, before_alpha = module.weight.detach().clone(), module.coefficients.detach().clone()
    module.weight.grad = torch.full_like(module.weight, float("nan"))
    skipped = optimizer.step() is False
    checks = {
        "five_step_explicit_adam_equivalence": max_error < 1e-10,
        "coefficient_channel_moves": alpha_change > 0,
        "student_channel_leaves_task_vector_span": outside_span > 1e-8,
        "task_vectors_frozen": not module.task_vectors.requires_grad and module.task_vectors.grad is None,
        "component_objective_decreases": final < initial,
        "nonfinite_batch_no_partial_update": skipped and torch.equal(before_weight, module.weight) and torch.equal(before_alpha, module.coefficients),
    }
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"initial_component_loss": initial, "final_component_loss": final,
                        "explicit_equivalence_max_error": max_error, "coefficient_change_norm": alpha_change,
                        "outside_task_vector_span_norm": outside_span,
                        "optimizer_steps": 5, "model_calls": 0}, "checks": checks}
