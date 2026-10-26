"""DetectorScope's auditable sparse head (2610.30006v1, Sec.4 and App.B.2).

Real frozen SAE activations and description-validation predictions are EXTERNAL
inputs. This module neither invents interpretable features nor runs an LLM,
SAE, Gemini annotator, text detector benchmark or the paper's full pipeline.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/detector-scope-a100-20261026.json"


def _finite_float(value: Tensor, name: str) -> None:
    if not value.is_floating_point() or not bool(torch.isfinite(value).all()):
        raise ValueError(f"{name}: finite floating tensor required")


def pool_sae_features(activations: Tensor, token_mask: Tensor) -> Tensor:
    """Frozen [B,layers,tokens,features] -> layer-major max-pool [B,L*F].

    Only real tokens are pooled; padding is zeroed before pooling, consistent
    with nonnegative SAE latents. Empty documents are rejected, not treated as
    a zero-feature prediction. No gradient enters an external SAE/backbone.
    """
    if (activations.ndim != 4 or min(activations.shape) < 1
            or activations.numel() > 1_048_576 or token_mask.dtype != torch.bool
            or token_mask.shape != (activations.shape[0], activations.shape[2])
            or token_mask.device != activations.device or not bool(token_mask.any(-1).all())):
        raise ValueError("bounded SAE activations[B,L,T,F] and nonempty bool token mask[B,T] required")
    _finite_float(activations, "SAE activations")
    valid = token_mask[:, None, :, None]
    if bool((activations.masked_select(valid.expand_as(activations)) < 0).any()):
        raise ValueError("SAE activations at valid tokens must be nonnegative")
    return torch.where(valid, activations.detach(), 0.).amax(2).flatten(1)


def _average_ranks(row: Tensor) -> Tensor:
    _, inverse, counts = torch.unique(row, sorted=True, return_inverse=True, return_counts=True)
    c = counts.to(row.dtype)
    return (c.cumsum(0) - (c - 1) / 2)[inverse]


def spearman_simulation_scores(true_quantiles: Tensor, predicted_quantiles: Tensor) -> Tensor:
    """Sec.4.2 Spearman rho across external validation examples per feature.

    Inputs [features,examples] are externally collected true/predicted quantile
    assignments. Average ranks handle ties. Constant rankings are undefined
    and rejected instead of silently fabricating a validated description.
    """
    if (true_quantiles.ndim != 2 or min(true_quantiles.shape) < 1
            or true_quantiles.shape[1] < 2 or true_quantiles.numel() > 262_144
            or predicted_quantiles.shape != true_quantiles.shape
            or predicted_quantiles.device != true_quantiles.device
            or predicted_quantiles.dtype != true_quantiles.dtype):
        raise ValueError("matching bounded quantile assignments[F,N>=2] required")
    for value in (true_quantiles, predicted_quantiles):
        _finite_float(value, "quantile assignments")
        if bool(((value < 0) | (value != value.floor())).any()):
            raise ValueError("quantile assignments must be nonnegative integer bins")
    result = []
    for real, predicted in zip(true_quantiles.detach(), predicted_quantiles.detach()):
        a, b = _average_ranks(real), _average_ranks(predicted)
        a, b = a - a.mean(), b - b.mean()
        norm = a.norm() * b.norm()
        if norm.item() == 0 or not bool(torch.isfinite(norm)):
            raise ValueError("constant or nonrepresentable rankings cannot validate a description")
        result.append((a @ b / norm).clamp(-1., 1.))
    return torch.stack(result)


def fit_training_rms(train_features: Tensor) -> Tensor:
    """Fit once on explicit training rows, without centering; dead scale=1.

    Stable RMS computation avoids overflow in x.square() for finite large
    activations. No validation/test input enters this function implicitly.
    """
    if train_features.ndim != 2 or min(train_features.shape) < 1 or train_features.numel() > 1_048_576:
        raise ValueError("bounded nonempty training features[N,F] required")
    _finite_float(train_features, "training features")
    if bool((train_features < 0).any()):
        raise ValueError("SAE features must be nonnegative")
    x = train_features.detach()
    maxima = x.amax(0)
    divisor = torch.where(maxima > 0, maxima, 1.)
    scale = divisor * (x / divisor).square().mean(0).sqrt()
    return torch.where(scale > 0, scale, 1.)


class AuditableSparseHead(nn.Module):
    """Global simulation mask, train-only RMS and proximal-SGD logistic head.

    Training operates in RMS-normalized coordinates. Prediction/attribution
    folds weights back to raw coordinates; zero-ablation attribution is an
    exact logit difference, NOT a probability difference or human explanation
    correctness guarantee. The bias is trained but never L1-thresholded.
    """
    def __init__(self, train_features: Tensor, simulation_scores: Tensor, *, tau: float = .85):
        super().__init__()
        scale = fit_training_rms(train_features)
        if (simulation_scores.shape != scale.shape or simulation_scores.device != scale.device
                or simulation_scores.dtype != scale.dtype or not math.isfinite(tau) or not -1 <= tau <= 1):
            raise ValueError("matching feature simulation scores and tau in[-1,1] required")
        _finite_float(simulation_scores, "simulation scores")
        if bool(((simulation_scores < -1) | (simulation_scores > 1)).any()):
            raise ValueError("Spearman simulation scores must be in[-1,1]")
        self.register_buffer("rms_scale", scale.clone())
        self.register_buffer("interp_mask", (simulation_scores.detach() >= tau).clone())
        self.weight = nn.Parameter(scale.new_zeros(scale.shape))
        self.bias = nn.Parameter(scale.new_zeros(()))
        self.register_buffer("weight_momentum", scale.new_zeros(scale.shape))
        self.register_buffer("bias_momentum", scale.new_zeros(()))

    def _features(self, features: Tensor) -> Tensor:
        if (features.ndim != 2 or features.shape[0] < 1 or features.shape[1:] != self.weight.shape
                or features.numel() > 1_048_576 or features.device != self.weight.device
                or features.dtype != self.weight.dtype):
            raise ValueError("matching nonempty bounded features[N,F] required")
        _finite_float(features, "features")
        if bool((features < 0).any()):
            raise ValueError("SAE features must be nonnegative")
        return features.detach()

    def forward(self, features: Tensor) -> Tensor:
        x = self._features(features) * self.interp_mask / self.rms_scale
        result = x @ self.weight + self.bias
        if not bool(torch.isfinite(result).all()):
            raise ValueError("nonrepresentable head logits; no silent clamping")
        return result

    def proximal_step(self, train_features: Tensor, labels: Tensor, *, lr: float = .03,
                      l1: float = .1, momentum: float = .9) -> dict[str, float]:
        """One real BCE SGD+momentum step followed by Eq.9 soft-threshold.

        Inputs must be designated training rows by the caller. No implicit
        fitting/tuning on prediction inputs, and no L1 subgradient double count.
        """
        if (not all(math.isfinite(v) for v in (lr, l1, momentum)) or lr <= 0 or l1 < 0
                or not 0 <= momentum < 1 or labels.shape != train_features.shape[:1]
                or labels.device != self.weight.device or labels.dtype != self.weight.dtype):
            raise ValueError("positive lr, nonnegative l1, momentum[0,1) and binary labels[N] required")
        _finite_float(labels, "labels")
        if bool(((labels != 0) & (labels != 1)).any()):
            raise ValueError("binary labels required")
        loss = F.binary_cross_entropy_with_logits(self(train_features), labels.detach())
        gw, gb = torch.autograd.grad(loss, (self.weight, self.bias))
        if not bool(torch.isfinite(gw).all()) or not bool(torch.isfinite(gb)):
            raise ValueError("nonfinite head gradient")
        with torch.no_grad():
            vw = momentum * self.weight_momentum + gw
            vb = momentum * self.bias_momentum + gb
            proposed = self.weight - lr * vw
            new_weight = proposed.sign() * (proposed.abs() - lr * l1).clamp_min(0)
            new_bias = self.bias - lr * vb
            if not bool(torch.isfinite(new_weight).all()) or not bool(torch.isfinite(new_bias)):
                raise ValueError("nonfinite proximal step; state not updated")
            self.weight_momentum.copy_(vw)
            self.bias_momentum.copy_(vb)
            self.weight.copy_(new_weight)
            self.bias.copy_(new_bias)
        return {"bce_before_step": loss.item(), "gradient_norm": gw.norm().item()}

    @torch.no_grad()
    def predict_with_attributions(self, features: Tensor) -> dict[str, Tensor]:
        x = self._features(features)
        raw_weight = self.weight * self.interp_mask / self.rms_scale
        contributions = x * raw_weight
        logits = contributions.sum(-1) + self.bias
        if not bool(torch.isfinite(logits).all()) or not bool(torch.isfinite(contributions).all()):
            raise ValueError("nonrepresentable raw-scale attribution")
        return {"logits": logits, "probabilities": logits.sigmoid(), "contributions": contributions,
                "raw_weight": raw_weight.clone(), "bias": self.bias.clone()}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or actual available cuda required; no fallback")
    with torch.random.fork_rng(devices=[torch.cuda.current_device()] if device == "cuda" else []):
        gen = torch.Generator(device=device).manual_seed(seed)
        acts = torch.rand(16, 2, 4, 3, generator=gen, device=device, dtype=torch.float64)
        mask = torch.tensor([[True, True, True, False]], device=device).expand(16, -1)
        acts[:, :, -1] = 9999.
        acts[:, :, :, 2] = 0.
        acts.requires_grad_()
        pooled = pool_sae_features(acts, mask)
        true = torch.tensor([[0, 0, 1, 2, 3, 3]], device=device, dtype=torch.float64).expand(6, -1)
        predictions = true.clone()
        predictions[1] = 3 - predictions[1]
        scores = spearman_simulation_scores(true, predictions).requires_grad_()
        train, labels = pooled[:12], torch.tensor([0., 1.] * 6, device=device, dtype=torch.float64)
        # Refit only explicit training rows; pooled[12:] are diagnostic held-out inputs.
        head = AuditableSparseHead(train, scores, tau=.85)
        initial_bce = F.binary_cross_entropy_with_logits(head(train), labels).item()
        step = head.proximal_step(train, labels, lr=.03, l1=.001)
        after_bce = F.binary_cross_entropy_with_logits(head(train), labels).item()
        sample = pooled[12:]
        output = head.predict_with_attributions(sample)
        fold_error = (head(sample) - output["logits"]).abs().max().item()
        cf = []
        for feature in range(sample.shape[1]):
            ablated = sample.clone()
            ablated[:, feature] = 0
            cf.append(output["logits"] - head.predict_with_attributions(ablated)["logits"])
        cf_error = (torch.stack(cf, -1) - output["contributions"]).abs().max().item()
        scale = head.rms_scale.clone()
        head.predict_with_attributions(sample * 1e6)
        # Deliberately leak held-out outliers into a second fit to ensure the
        # negative control changes the scale, while the actual head stays fixed.
        leaked = fit_training_rms(torch.cat([train, sample * 1e6]))
        train_rms = torch.where(train.square().mean(0) > 0, train.square().mean(0).sqrt(), 1.)
        pool_reference = acts.detach()[:, :, :3].amax(2).flatten(1)
        # A subgradient-only update cannot produce this proximal exact zero.
        tiny = AuditableSparseHead(train, scores, tau=.85)
        with torch.no_grad():
            tiny.weight.fill_(1e-8)
        tiny.proximal_step(train, labels, lr=.03, l1=100.)
        negative_pool_gap = (acts.detach().amax(2).flatten(1) - pooled).abs().max().item()
        scale_leak_gap = (leaked - scale).abs().max().item()
        checks = {
            "max_pool_masks_padding_and_concatenates_layers": torch.equal(pool_reference, pooled) and negative_pool_gap > 1,
            "spearman_ties_and_global_mask": bool(torch.allclose(scores.detach(), scores.new_tensor([1., -1., 1., 1., 1., 1.])))
                and not bool(head.interp_mask[1]),
            "training_only_rms_no_centering": torch.allclose(scale, train_rms) and torch.equal(scale, head.rms_scale)
                and scale_leak_gap > 1 and bool((head.rms_scale[[2, 5]] == 1).all()),
            "external_sae_and_validation_scores_frozen": acts.grad is None and scores.grad is None
                and not pooled.requires_grad and not head.rms_scale.requires_grad,
            "actual_sgd_momentum_proximal_update": step["gradient_norm"] > 0 and after_bce < initial_bce
                and bool((head.weight_momentum != 0).any()),
            "proximal_exact_zeros_bias_not_shrunk": bool((tiny.weight == 0).all())
                and tiny.bias.item() != 0.,
            "folded_raw_weights_match_normalized_logits": fold_error < 1e-12,
            "zero_ablation_is_exact_logit_contribution": cf_error < 1e-12
                and bool((output["contributions"][:, ~head.interp_mask] == 0).all()),
        }
        if not all(checks.values()):
            raise RuntimeError(f"DetectorScope mechanism failed: {checks}")
        return {"seed": seed, "metrics": {"fixture_bce_before": initial_bce, "fixture_bce_after": after_bce,
            "gradient_norm": step["gradient_norm"], "raw_fold_error": fold_error,
            "counterfactual_attribution_error": cf_error, "padding_negative_control_gap": negative_pool_gap,
            "rms_leakage_negative_control_gap": scale_leak_gap, "retained_features": int(head.interp_mask.sum()),
            "nonzero_head_weights": int((head.weight != 0).sum()), "training_documents": 12,
            "held_out_documents": 4, "optimizer_steps": 1, "pretrained_model_calls": 0}, "checks": checks}
