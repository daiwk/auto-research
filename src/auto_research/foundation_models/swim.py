"""SWIM v1 stage-1 inverse-dynamics loss and detached metric-transfer components.

Training states/future states/actions are explicit offline labels. No such data
is exposed as planning input here: image encoder, JEPA/SIGReg training, physical
simulators and CEM are absent. This is not a world model or a capable policy.
"""
import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/swim-a100-20261030.json"


def _finite(x: Tensor, ndim: int) -> None:
    if (x.ndim != ndim or not 0 < x.numel() <= 1_048_576
            or x.dtype not in (torch.float32, torch.float64)
            or not bool(torch.isfinite(x).all())):
        raise ValueError("bounded finite float32/float64 tensor required")


class GatedInverseDynamics(nn.Module):
    """AppendixA two LN/GELU layers, sigmoid gates initialized at alpha=2.

    Inputs must already follow external state/action standardization, floor
    and clipping. No preprocessing statistics or split is estimated here.
    Current state remains UNGATED. Smaller hidden widths
    retain the objective but are not the author's 1024-wide trained predictor.
    """

    def __init__(self, state_width: int, action_width: int, hidden_width: int = 64):
        super().__init__()
        if any(isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= 1024
               for v in (state_width, action_width, hidden_width)):
            raise ValueError("bounded positive network widths required")
        self.state_width, self.action_width, self.hidden_width = state_width, action_width, hidden_width
        self.alpha = nn.Parameter(torch.full((state_width,), 2.))
        self.predictor = nn.Sequential(nn.Linear(2 * state_width, hidden_width),
            nn.LayerNorm(hidden_width), nn.GELU(), nn.Linear(hidden_width, hidden_width),
            nn.LayerNorm(hidden_width), nn.GELU(), nn.Linear(hidden_width, 2 * action_width))

    @property
    def gates(self) -> Tensor:
        return self.alpha.sigmoid()

    def forward(self, current: Tensor, later: Tensor) -> dict:
        _finite(current, 2)
        _finite(later, 2)
        if (current.shape != later.shape or current.shape[1] != self.state_width
                or len(current) * self.hidden_width > 1_048_576
                or current.device != later.device or current.dtype != later.dtype):
            raise ValueError("aligned standardized offline current/later states required")
        displacement = later.detach() - current.detach()
        _finite(displacement, 2)
        features = torch.cat((current.detach(), self.gates * displacement), -1)
        _finite(features, 2)
        mean, log_std = self.predictor(features).chunk(2, -1)
        _finite(mean, 2)
        _finite(log_std, 2)
        return {"mean": mean, "log_std": log_std.clamp(-5, 2), "features": features}

    def action_log_probability(self, current: Tensor, later: Tensor, actions: Tensor) -> Tensor:
        _finite(actions, 2)
        result = self(current, later)
        if (actions.shape != (len(current), self.action_width) or actions.dtype != current.dtype
                or actions.device != current.device):
            raise ValueError("aligned standardized recorded action chunk required")
        loss = (.5 * ((actions.detach() - result["mean"]) * (-result["log_std"]).exp()).square()
                + result["log_std"] + .5 * math.log(2 * math.pi)).sum(-1)
        _finite(loss, 1)
        return -loss

    def stage1_loss(self, current: Tensor, later: Tensor, actions: Tensor, *,
                    discrimination: str = "hinge", negatives: int = 1,
                    margin: float = 1., temperature: float = 1.,
                    discrimination_weight: float = 1., gate_penalty: float = .03) -> dict:
        """Eqs.4.1--4.5; mismatch later states are NEXT cyclic examples.

        Hinge uses exactly the next example; InfoNCE uses the next N, excludes
        self, and does not silently expand to every batch item. Original states
        and actions stay fixed for each row when evaluating alternatives.
        """
        if (len(current) < 2 or discrimination not in ("hinge", "infonce")
                or isinstance(negatives, bool) or not isinstance(negatives, int)
                or not 1 <= negatives < len(current) or discrimination == "hinge" and negatives != 1
                or len(current) * (negatives + 1) > 65_536
                or any(isinstance(v, bool) or not math.isfinite(v) or v <= 0 for v in (margin, temperature))
                or any(isinstance(v, bool) or not math.isfinite(v) or v < 0
                       for v in (discrimination_weight, gate_penalty))):
            raise ValueError("valid cyclic negatives, loss and finite objective weights required")
        positive = self.action_log_probability(current, later, actions)
        indices = (torch.arange(len(current), device=current.device)[:, None]
                   + torch.arange(1, negatives + 1, device=current.device)[None]) % len(current)
        negative_scores = torch.stack([self.action_log_probability(current, later[indices[:, k]], actions)
                                       for k in range(negatives)], -1)
        nll = -positive.mean()
        if discrimination == "hinge":
            disc = (margin - positive + negative_scores[:, 0]).clamp_min(0).mean()
        else:
            logits = torch.cat((positive[:, None], negative_scores), -1) / temperature
            disc = -logits.log_softmax(-1)[:, 0].mean()
        penalty = self.gates.sum()
        loss = nll + discrimination_weight * disc + gate_penalty * penalty
        _finite(loss, 0)
        return {"loss": loss,
                "nll": nll, "discrimination": disc, "gate_l1": penalty,
                "positive_logp": positive, "negative_logp": negative_scores,
                "negative_indices": indices}


def weighted_state_distances(states: Tensor, pairs: Tensor, gates: Tensor) -> Tensor:
    """Eq.4.6: sqrt(g)*standardized q, then squared distances, target detached.

    No second coordinate-wise normalization is applied: that would undo the
    weights. Stage-2 states are un-clipped once-standardized training data.
    """
    _finite(states, 2)
    _finite(gates, 1)
    if (gates.shape != states.shape[1:] or gates.device != states.device or gates.dtype != states.dtype
            or bool(((gates < 0) | (gates > 1)).any()) or pairs.ndim != 2 or pairs.shape[1] != 2
            or pairs.numel() < 2 or pairs.numel() > 65_536 or pairs.dtype != torch.long
            or pairs.device != states.device or bool(((pairs < 0) | (pairs >= len(states))).any())):
        raise ValueError("aligned continuous gates and valid training frame pairs required")
    with torch.no_grad():
        scaled = states * gates.sqrt()
        result = (scaled[pairs[:, 0]] - scaled[pairs[:, 1]]).square().sum(-1)
        _finite(result, 1)
        return result


def latent_state_correlation(latents: Tensor, pairs: Tensor, target_distances: Tensor) -> Tensor:
    """Eq.3.6/4.7 correlation subloss only, not prediction+SIGReg training."""
    _finite(latents, 2)
    _finite(target_distances, 1)
    if (pairs.ndim != 2 or pairs.shape != (len(target_distances), 2) or pairs.dtype != torch.long
            or pairs.device != latents.device or target_distances.device != latents.device
            or target_distances.dtype != latents.dtype
            or bool(((pairs < 0) | (pairs >= len(latents))).any())):
        raise ValueError("same valid frame pairs and detached state-distance targets required")
    distance = (latents[pairs[:, 0]] - latents[pairs[:, 1]]).square().sum(-1)
    _finite(distance, 1)
    x = distance - distance.mean()
    y = target_distances.detach() - target_distances.detach().mean()
    denominator = x.norm() * y.norm()
    if not bool(torch.isfinite(denominator)) or denominator <= 0:
        raise ValueError("Pearson correlation is undefined for constant distance vectors")
    loss = 1 - x @ y / denominator
    _finite(loss, 0)
    return loss


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or actual available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    args = {"device": device, "dtype": torch.float64, "generator": gen}
    with torch.random.fork_rng(devices=[torch.cuda.current_device()] if device == "cuda" else []):
        torch.manual_seed(seed)
        model = GatedInverseDynamics(5, 3, 12).to(device=device, dtype=torch.float64)
    current, later, actions = torch.randn(6, 5, **args), torch.randn(6, 5, **args), torch.randn(6, 3, **args)
    hinge = model.stage1_loss(current, later, actions)
    info = model.stage1_loss(current, later, actions, discrimination="infonce", negatives=3)
    prediction = model(current, later)
    independent_logp = torch.distributions.Normal(prediction["mean"], prediction["log_std"].exp()).log_prob(actions).sum(-1)
    nll_error = (hinge["nll"] + independent_logp.mean()).abs().item()
    hinge_ref = (1 - independent_logp + model.action_log_probability(current, later.roll(-1, 0), actions)).clamp_min(0).mean()
    hinge_error = (hinge["discrimination"] - hinge_ref).abs().item()
    info_ref = torch.cat((info["positive_logp"][:, None], info["negative_logp"]), -1)
    info_error = (info["discrimination"] - (-info_ref[:, 0] + info_ref.logsumexp(-1)).mean()).abs().item()
    before = model.alpha.detach().clone()
    behavior_gate_gradient = torch.autograd.grad(info["nll"] + info["discrimination"],
                                                model.alpha, retain_graph=True)[0].norm().item()
    info["loss"].backward()
    gate_gradient = model.alpha.grad.norm().item()
    predictor_gradient = sum(p.grad.norm().item() for p in model.predictor.parameters())
    torch.optim.SGD(model.parameters(), lr=.001).step()
    gate_delta = (model.alpha - before).norm().item()
    pairs = torch.tensor([[0, 1], [1, 3], [2, 5], [0, 4], [3, 5]], device=device)
    external_gates = model.gates.detach().clone().requires_grad_()
    target = weighted_state_distances(current, pairs, external_gates)
    direct = ((current[pairs[:, 0]] - current[pairs[:, 1]]).square() * external_gates.detach()).sum(-1)
    target_error = (target - direct).abs().max().item()
    latents = torch.randn(6, 4, **args).requires_grad_()
    correlation = latent_state_correlation(latents, pairs, target)
    correlation.backward()
    checks = {"gaussian_nll_independent_reference": nll_error < 1e-12,
        "cyclic_hinge_negative_reference": hinge_error < 1e-12,
        "infonce_selected_denominator_reference": info_error < 1e-12,
        "current_state_is_not_gated": torch.equal(prediction["features"][:, :5], current),
        "gates_and_inverse_model_really_train": gate_gradient > 0 and behavior_gate_gradient > 0
            and predictor_gradient > 0 and gate_delta > 0,
        "sqrt_gate_distance_reference": target_error < 1e-12,
        "stage_two_gate_target_is_detached": external_gates.grad is None and not target.requires_grad,
        "latent_geometry_receives_real_gradient": latents.grad.norm().item() > 0}
    if not all(checks.values()):
        raise RuntimeError(f"SWIM checks failed: {checks}")
    return {"seed": seed, "metrics": {"nll_reference_error": nll_error,
        "hinge_reference_error": hinge_error, "infonce_reference_error": info_error,
        "metric_reference_error": target_error, "gate_gradient_norm": gate_gradient,
        "behavior_only_gate_gradient_norm": behavior_gate_gradient,
        "predictor_gradient_norm": predictor_gradient, "gate_parameter_delta": gate_delta,
        "correlation_loss": correlation.item(), "environment_interactions": 0}, "checks": checks}
