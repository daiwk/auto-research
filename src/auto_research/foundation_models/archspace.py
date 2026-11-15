"""ArchSpace v1 Eq.2--5 arithmetic, not architecture search or a fitted new law."""
from __future__ import annotations

import math
from dataclasses import dataclass

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class CoupledLaw:
    floor: float
    alpha_m: float
    gamma_m: float
    alpha_d: float
    gamma_d: float
    gamma_md: float
    eta_coeff: float
    eta_m: float
    eta_d: float
    batch_coeff: float
    batch_m: float
    batch_d: float
    height_coeff: float
    height_m: float
    height_d: float
    rho: float

    @staticmethod
    def _positive(*values: float) -> None:
        if any(not math.isfinite(x) or x <= 0 for x in values):
            raise ValueError("finite positive FLOPs/token, tokens, LR and batch required")

    def recipe(self, model_flops_per_token: float, tokens: float) -> tuple[float, float]:
        self._positive(model_flops_per_token, tokens)
        m, d = model_flops_per_token, tokens
        return (self.eta_coeff * m ** self.eta_m * d ** self.eta_d,
                self.batch_coeff * m ** self.batch_m * d ** self.batch_d)

    def base_loss(self, model_flops_per_token: float, tokens: float) -> float:
        self._positive(model_flops_per_token, tokens)
        m, d = model_flops_per_token, tokens
        return self.floor + (self.alpha_m * m ** -self.gamma_m
                             + self.alpha_d * d ** -self.gamma_d) ** self.gamma_md

    def loss(self, model_flops_per_token: float, tokens: float, lr: float, batch: float) -> float:
        self._positive(model_flops_per_token, tokens, lr, batch)
        eta_star, batch_star = self.recipe(model_flops_per_token, tokens)
        e, b = math.log(lr / eta_star), math.log(batch / batch_star)
        height = self.height_coeff * model_flops_per_token ** self.height_m * tokens ** self.height_d
        penalty = 2 * height * (math.cosh(e - 0.5 * b) - 1 + self.rho * (math.cosh(b) - 1))
        return self.base_loss(model_flops_per_token, tokens) + penalty

    def budget_optimum(self, training_flops: float) -> tuple[float, float]:
        """C=M*D, where M is FLOPs/token, NOT parameter count N."""
        self._positive(training_flops)
        m = (self.gamma_m * self.alpha_m / (self.gamma_d * self.alpha_d)
             * training_flops ** self.gamma_d) ** (1 / (self.gamma_m + self.gamma_d))
        return m, training_flops / m


QWEN35 = CoupledLaw(1.722, 6.77e4, .520, 1.90e4, .453, .505,
                    421, -.408, -.152, 36.8, -.047, .485, 17.9, -.075, -.242, 1.16)
OLMO3 = CoupledLaw(1.488, 3.96e5, .576, 5.99e4, .475, .402,
                   269, -.389, -.154, 47.3, -.036, .457, 14.0, -.097, -.203, 1.15)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    del seed
    if device != "cpu":
        raise ValueError("ArchSpace arithmetic is CPU-only; it advertises no CUDA path")
    m, d = QWEN35.budget_optimum(1e20)
    eta, batch = QWEN35.recipe(m, d)
    optimum = QWEN35.loss(m, d, eta, batch)
    shifted = QWEN35.loss(m, d, eta * 2, batch * 4)
    unshifted = QWEN35.loss(m, d, eta, batch * 4)
    return {"diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"model_flops_per_token": m, "training_tokens": d,
                        "predicted_base_loss": optimum, "coupled_batch_penalty": shifted - optimum},
            "checks": {"budget_conserved": math.isclose(m * d, 1e20),
                       "penalty_zero_at_recipe": math.isclose(optimum, QWEN35.base_loss(m, d)),
                       "conditional_lr_sqrt_batch": optimum < shifted < unshifted,
                       "budget_optimum_beats_neighbors": all(
                           QWEN35.base_loss(m * factor, d / factor) > optimum for factor in (.8, 1.2))}}
