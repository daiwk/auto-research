"""DT-JEPA v1 Eqs.7--16 as trainable bounded mechanism components.

Architectures and a valid history-only DT hidden representation are explicit
caller inputs. No D4RL data, simulator, policy capability or evolve integration
is implied. Future trajectory labels are used only by the training loss.
"""
import copy
import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/dt-jepa-a100-20261026.json"


def _finite(x: Tensor, ndim: int | None = None) -> None:
    if ((ndim is not None and x.ndim != ndim) or x.numel() < 1 or x.numel() > 1_048_576
            or not x.is_floating_point() or not bool(torch.isfinite(x).all())):
        raise ValueError("bounded finite nonempty floating tensor required")


def gaussian_future_nll(mean: Tensor, log_std: Tensor, target: Tensor) -> Tensor:
    """Eq.7 diagonal Gaussian: SUM latent dimensions, MEAN batch, target sg."""
    for x in (mean, log_std, target):
        _finite(x, 2)
    if any(x.shape != mean.shape or x.dtype != mean.dtype or x.device != mean.device for x in (log_std, target)):
        raise ValueError("aligned Gaussian parameters/target required")
    loss = (.5 * ((target.detach() - mean) * (-log_std).exp()).square()
            + log_std + .5 * math.log(2 * math.pi)).sum(-1).mean()
    if not bool(torch.isfinite(loss)):
        raise ValueError("nonfinite Gaussian NLL; no altered variance floor/clipping")
    return loss


def masked_sequence_sum_mean(values: Tensor, valid: Tensor) -> Tensor:
    """Paper equations sum time (and feature axes), then mean batch."""
    _finite(values)
    if (values.ndim < 2 or valid.shape != values.shape[:2] or valid.dtype != torch.bool
            or valid.device != values.device or not bool(valid.any(-1).all())):
        raise ValueError("nonempty aligned sequence mask required")
    mask = valid.reshape(valid.shape + (1,) * (values.ndim - 2))
    loss = torch.where(mask, values, 0).flatten(1).sum(-1).mean()
    if not bool(torch.isfinite(loss)):
        raise ValueError("nonfinite sequence objective")
    return loss


class PredictiveFuture(nn.Module):
    """Caller-defined f_theta, q_eta, MLP_gamma/beta and action head.

    predictor(history_features) must return (mean, log_standard_deviation).
    forward accepts observable history, external history-only DT h and noise;
    it does not accept future states, task rewards or labeled actions.
    """

    def __init__(self, encoder: nn.Module, predictor: nn.Module, gamma: nn.Module,
                 beta: nn.Module, action_head: nn.Module):
        super().__init__()
        if any(True for _ in encoder.buffers()):
            raise ValueError("paper does not specify encoder buffer EMA; supply a buffer-free encoder")
        self.encoder = encoder
        self.target_encoder = copy.deepcopy(encoder).requires_grad_(False).eval()
        self.predictor, self.gamma, self.beta, self.action_head = predictor, gamma, beta, action_head

    def train(self, mode: bool = True):
        super().train(mode)
        self.target_encoder.eval()
        return self

    def forward(self, history: Tensor, dt_hidden: Tensor, noise: Tensor) -> dict:
        _finite(history)
        _finite(dt_hidden, 3)
        mean, log_std = self.predictor(self.encoder(history))
        for x in (mean, log_std, noise):
            _finite(x, 2)
            if x.device != dt_hidden.device or x.dtype != dt_hidden.dtype:
                raise ValueError("predictor/DT/noise dtype and device must agree")
        if mean.shape != log_std.shape or mean.shape != noise.shape or mean.shape[0] != dt_hidden.shape[0]:
            raise ValueError("aligned predicted Gaussian and explicit noise required")
        future = mean + log_std.exp() * noise
        _finite(future, 2)
        gamma, beta = self.gamma(future), self.beta(future)
        if gamma.shape != dt_hidden.shape[:1] + dt_hidden.shape[-1:] or beta.shape != gamma.shape:
            raise ValueError("gamma/beta must match DT hidden width")
        modulated = (1 + gamma[:, None]) * F.layer_norm(dt_hidden, (dt_hidden.shape[-1],)) + beta[:, None]
        actions = self.action_head(modulated)
        _finite(actions, 3)
        return {"mean": mean, "log_std": log_std, "future": future,
                "modulated": modulated, "actions": actions}

    def pretraining_loss(self, history: Tensor, future_segment: Tensor, dt_hidden: Tensor,
                         actions: Tensor, noise: Tensor, valid: Tensor, *, jepa_weight: float) -> dict:
        if isinstance(jepa_weight, bool) or not math.isfinite(jepa_weight) or jepa_weight < 0:
            raise ValueError("finite nonnegative JEPA weight required")
        result = self(history, dt_hidden, noise)
        _finite(future_segment)
        with torch.no_grad():
            target = self.target_encoder(future_segment)
        prediction_loss = gaussian_future_nll(result["mean"], result["log_std"], target)
        _finite(actions, 3)
        if actions.shape != result["actions"].shape or actions.device != dt_hidden.device or actions.dtype != dt_hidden.dtype:
            raise ValueError("matching training action labels required")
        bc_loss = masked_sequence_sum_mean((result["actions"] - actions.detach()).square(), valid)
        total = bc_loss + jepa_weight * prediction_loss
        _finite(total)
        return {**result, "jepa_loss": prediction_loss, "bc_loss": bc_loss, "loss": total}

    @torch.no_grad()
    def update_target(self, *, rho: float = .99) -> None:
        if isinstance(rho, bool) or not math.isfinite(rho) or not 0 <= rho <= 1:
            raise ValueError("EMA rho in [0,1] required")
        if any(True for _ in self.encoder.buffers()) or any(True for _ in self.target_encoder.buffers()):
            raise ValueError("paper does not specify encoder buffer EMA; supply a buffer-free encoder")
        target = dict(self.target_encoder.named_parameters())
        source = dict(self.encoder.named_parameters())
        if target.keys() != source.keys():
            raise ValueError("target and source encoder parameters must align")
        for name in target:
            if (target[name].shape != source[name].shape or target[name].dtype != source[name].dtype
                    or target[name].device != source[name].device):
                raise ValueError("target and source parameter schemas must match")
            _finite(target[name])
            _finite(source[name])
        for name in target:
            target[name].mul_(rho).add_(source[name], alpha=1-rho)


def multistep_td_targets(rewards: Tensor, target_q1: Tensor, target_q2: Tensor, *, discount: float) -> Tensor:
    """Eq.13 for m=0..T-1, bootstrap at T with min(targetQ1,targetQ2).

    Input is a contiguous fixed trajectory segment, not an arbitrary packed or
    terminal-containing batch. Terminal handling is not defined by this paper.
    """
    _finite(rewards, 2)
    _finite(target_q1, 1)
    _finite(target_q2, 1)
    if (target_q1.shape != rewards.shape[:1] or target_q2.shape != target_q1.shape
            or any(q.device != rewards.device or q.dtype != rewards.dtype for q in (target_q1, target_q2))
            or isinstance(discount, bool) or not math.isfinite(discount) or not 0 <= discount <= 1):
        raise ValueError("aligned target critics and discount in [0,1] required")
    with torch.no_grad():
        carry = torch.minimum(target_q1, target_q2)
        result = []
        for i in reversed(range(rewards.shape[1])):
            carry = rewards[:, i] + discount * carry
            result.append(carry)
        targets = torch.stack(result[::-1], -1)
    _finite(targets, 2)
    return targets


def critic_loss(predicted_q: Tensor, td_targets: Tensor, valid: Tensor) -> Tensor:
    if predicted_q.shape != td_targets.shape:
        raise ValueError("aligned critic values/targets required")
    _finite(predicted_q, 2)
    _finite(td_targets, 2)
    return masked_sequence_sum_mean((predicted_q - td_targets.detach()).square(), valid)


def adaptation_objective(bc_loss: Tensor, jepa_loss: Tensor, policy_q: Tensor, valid: Tensor,
                         *, jepa_weight: float, q_weight: float) -> dict:
    """Eqs.15--16; caller evaluates Q1 on current generated actions.

    The caller freezes critic parameters during actor optimization while keeping
    dQ/da. Do not detach policy_q: its gradient is the defining actor signal.
    """
    for x in (bc_loss, jepa_loss):
        _finite(x, 0)
    for weight in (jepa_weight, q_weight):
        if isinstance(weight, bool) or not math.isfinite(weight) or weight < 0:
            raise ValueError("finite nonnegative adaptation weights required")
    _finite(policy_q, 2)
    value_loss = -masked_sequence_sum_mean(policy_q, valid)
    total = bc_loss + jepa_weight * jepa_loss + q_weight * value_loss
    _finite(total, 0)
    return {"loss": total, "q_loss": value_loss}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or actual available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    class Gaussian(nn.Module):
        def __init__(self):
            super().__init__()
            self.mean, self.logstd = nn.Linear(4, 4), nn.Linear(4, 4)
        def forward(self, h):
            return self.mean(h), self.logstd(h)
    with torch.random.fork_rng(devices=[torch.cuda.current_device()] if device == "cuda" else []):
        torch.manual_seed(seed)
        model = PredictiveFuture(nn.Linear(6, 4), Gaussian(), nn.Linear(4, 8), nn.Linear(4, 8), nn.Linear(8, 2)).to(device=device, dtype=torch.float64)
    history = torch.randn(3, 6, generator=gen, device=device, dtype=torch.float64)
    future = torch.randn(3, 6, generator=gen, device=device, dtype=torch.float64, requires_grad=True)
    hidden = torch.randn(3, 4, 8, generator=gen, device=device, dtype=torch.float64)
    actions = torch.randn(3, 4, 2, generator=gen, device=device, dtype=torch.float64)
    noise = torch.randn(3, 4, generator=gen, device=device, dtype=torch.float64)
    valid = torch.tensor([[True, True, True, True], [True, True, False, False], [True, True, True, False]], device=device)
    result = model.pretraining_loss(history, future, hidden, actions, noise, valid, jepa_weight=.1)
    target = model.target_encoder(future).detach()
    ref_nll = -torch.distributions.Normal(result["mean"], result["log_std"].exp()).log_prob(target).sum(-1).mean()
    nll_error = (result["jepa_loss"] - ref_nll).abs().item()
    ref_modulated = (1 + model.gamma(result["future"])[:, None]) * F.layer_norm(hidden, (8,)) + model.beta(result["future"])[:, None]
    mod_error = (result["modulated"] - ref_modulated).abs().max().item()
    bc_grads = torch.autograd.grad(result["bc_loss"], tuple(model.predictor.parameters()), retain_graph=True)
    bc_predictor_grad = sum(g.norm().item() for g in bc_grads)
    result["loss"].backward()
    detached = future.grad is None and all(p.grad is None for p in model.target_encoder.parameters())
    grad_norm = sum(p.grad.norm().item() for p in model.predictor.parameters())
    before = {n: p.detach().clone() for n, p in model.target_encoder.named_parameters()}
    with torch.no_grad():
        for p in model.encoder.parameters():
            p.add_(.05)
    model.update_target(rho=.8)
    ema_error = max((p - (.8 * before[n] + .2 * dict(model.encoder.named_parameters())[n])).abs().max().item()
                    for n, p in model.target_encoder.named_parameters())
    rewards = torch.randn(3, 3, generator=gen, device=device, dtype=torch.float64)
    q1 = torch.tensor([1., 4., 2.], device=device, dtype=torch.float64, requires_grad=True)
    q2 = torch.tensor([2., 3., 1.], device=device, dtype=torch.float64, requires_grad=True)
    td = multistep_td_targets(rewards, q1, q2, discount=.9)
    td_ref = torch.stack([sum(.9 ** (k-m) * rewards[:, k] for k in range(m, 3))
                         + .9 ** (3-m) * torch.minimum(q1, q2) for m in range(3)], -1)
    td_error = (td - td_ref).abs().max().item()
    policy_q = torch.randn(3, 3, generator=gen, device=device, dtype=torch.float64, requires_grad=True)
    adapted = adaptation_objective(result["bc_loss"].detach(), result["jepa_loss"].detach(), policy_q,
        valid[:, :3], jepa_weight=.1, q_weight=.3)
    adapted["loss"].backward()
    bc_reference = sum((result["actions"][b, valid[b]] - actions[b, valid[b]]).square().sum() for b in range(3)) / 3
    checks = {"gaussian_nll_independent_reference": nll_error < 1e-12,
              "ema_future_target_stop_gradient": detached,
              "reparameterized_predictor_receives_gradient": grad_norm > 0 and math.isfinite(grad_norm)
                  and bc_predictor_grad > 0 and math.isfinite(bc_predictor_grad),
              "adaln_formula_reference": mod_error < 1e-12,
              "bc_sums_time_then_means_batch": torch.allclose(result["bc_loss"], bc_reference, atol=1e-12, rtol=0),
              "ema_parameter_update_reference": ema_error < 1e-12,
              "multistep_twin_min_target_reference": td_error < 1e-12 and not td.requires_grad,
              "actor_q_gradient_not_detached": torch.equal(policy_q.grad != 0, valid[:, :3]),
              "inference_has_no_future_or_labels": "future_segment" not in PredictiveFuture.forward.__annotations__ and "actions" not in PredictiveFuture.forward.__annotations__}
    if not all(checks.values()):
        raise RuntimeError(f"DT-JEPA mechanism check failed: {checks}")
    return {"seed": seed, "metrics": {"pretraining_loss": result["loss"].item(),
        "jepa_nll": result["jepa_loss"].item(), "behavior_cloning_loss": result["bc_loss"].item(),
        "nll_reference_error": nll_error, "adaln_reference_error": mod_error, "ema_reference_error": ema_error,
        "td_reference_error": td_error, "predictor_gradient_norm": grad_norm,
        "bc_predictor_gradient_norm": bc_predictor_grad,
        "environment_interactions": 0}, "checks": checks}
