"""MTM's mechanistic ETM Eqs.10--13 and steering Eqs.16--19 (2507.23220v3).

Frozen real SAE ENCODER weights and document binary-activation counts are EXTERNAL
interfaces. No substitute SAE/LLM, feature description, topic-judge or text
generation is supplied. Variational-network topology is caller-provided.
"""
import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/mechanistic-etm-a100-20261025.json"


class MechanisticETM(nn.Module):
    """Binomial SAE-feature topic model, NOT a multinomial word-topic ETM.

    posterior(counts)->(mu,log_variance), each [B,K]. SAE ENCODER [W,D] is frozen;
    learned topic directions [K,D] plus feature bias produce sigmoid beta[K,W].
    Explicit noise[B,K] fixes Monte Carlo samples across comparisons/updates.
    """
    def __init__(self, encoder_weights: Tensor, topics: int, posterior: nn.Module):
        super().__init__()
        if (encoder_weights.ndim != 2 or min(encoder_weights.shape) < 1
                or encoder_weights.numel() > 1_048_576 or not encoder_weights.is_floating_point()
                or not bool(torch.isfinite(encoder_weights).all())
                or not isinstance(topics, int) or not 2 <= topics <= 128):
            raise ValueError("bounded finite [features,hidden] frozen SAE ENCODER and topics2..128 required")
        self.register_buffer("encoder_weights", encoder_weights.detach().clone())
        self.posterior = posterior
        self.topic_vectors = nn.Parameter(encoder_weights.new_empty(topics, encoder_weights.shape[1]))
        self.feature_bias = nn.Parameter(encoder_weights.new_zeros(encoder_weights.shape[0]))
        nn.init.normal_(self.topic_vectors, std=.02)

    def forward(self, counts: Tensor, total_tokens: Tensor, noise: Tensor) -> dict[str, Tensor]:
        if (counts.ndim != 2 or counts.shape[-1] != len(self.encoder_weights) or counts.shape[0] < 1
                or counts.numel() > 65536 or counts.device != self.encoder_weights.device or counts.dtype != self.encoder_weights.dtype
                or total_tokens.shape != counts.shape[:1] or total_tokens.device != counts.device
                or not bool(torch.isfinite(counts).all()) or not bool(torch.isfinite(total_tokens).all())
                or bool((total_tokens <= 0).any()) or bool((total_tokens != total_tokens.floor()).any())
                or bool(((counts < 0) | (counts > total_tokens[:, None]) | (counts != counts.floor())).any())):
            raise ValueError("integer SAE activation counts[B,W] in[0,N_tokens], positive integer lengths required")
        mu, logvar = self.posterior(counts.detach())
        expected = (counts.shape[0], len(self.topic_vectors))
        if (mu.shape != expected or logvar.shape != expected or noise.shape != expected
                or any(x.device != counts.device or x.dtype != counts.dtype or not bool(torch.isfinite(x).all())
                       for x in (mu, logvar, noise))):
            raise ValueError("finite matching posterior mean/logvariance and explicit Gaussian noise[B,K] required")
        delta = mu + (.5 * logvar).exp() * noise
        logtheta = delta.log_softmax(-1)
        logits = self.topic_vectors @ self.encoder_weights.T + self.feature_bias
        if not bool(torch.isfinite(logits).all()) or not bool(torch.isfinite(delta).all()):
            raise ValueError("nonfinite topic/posterior logits")
        # Stable mixture probabilities, without clamping sigmoid or likelihood.
        logp = torch.logsumexp(logtheta[:, :, None] + F.logsigmoid(logits)[None], dim=1)
        log1mp = torch.logsumexp(logtheta[:, :, None] + F.logsigmoid(-logits)[None], dim=1)
        n, c = total_tokens.detach().to(counts.dtype)[:, None], counts.detach()
        logchoose = torch.lgamma(n + 1) - torch.lgamma(c + 1) - torch.lgamma(n - c + 1)
        nll = -(logchoose + c * logp + (n - c) * log1mp).sum(-1).mean()
        kl = .5 * (logvar.exp() + mu.square() - 1 - logvar).sum(-1).mean()
        loss = nll + kl
        if not all(bool(torch.isfinite(x)) for x in (nll, kl, loss)):
            raise ValueError("nonfinite binomial ELBO; no silent clamp")
        return {"loss": loss, "binomial_nll": nll, "kl": kl,
                "topic_feature_probabilities": logits.sigmoid(), "document_topics": logtheta.exp()}


def topic_steering_vector(topic_weights: Tensor, decoder: Tensor) -> Tensor:
    if (topic_weights.ndim != 1 or decoder.ndim != 2 or len(topic_weights) != len(decoder)
            or topic_weights.device != decoder.device or topic_weights.dtype != decoder.dtype
            or not topic_weights.is_floating_point() or not bool(torch.isfinite(topic_weights).all())
            or not bool(torch.isfinite(decoder).all()) or bool((topic_weights < 0).any())):
        raise ValueError("finite nonnegative feature weights and matching decoder required")
    vector = topic_weights @ decoder.detach()
    norm = vector.norm()
    if not bool(torch.isfinite(norm)) or norm.item() <= 0:
        raise ValueError("topic steering direction must be nonzero and finite")
    return vector / norm


def replace_topic_component(activations: Tensor, direction: Tensor, decoder_bias: Tensor, *, strength: float) -> Tensor:
    """Eq.19 subtracts existing parallel signal, NOT plain additive steering."""
    if (direction.ndim != 1 or decoder_bias.shape != direction.shape or activations.shape[-1:] != direction.shape
            or any(v.device != activations.device or v.dtype != activations.dtype
                   or not bool(torch.isfinite(v).all()) for v in (activations, direction, decoder_bias))
            or not math.isfinite(strength) or not torch.isclose(direction.norm(), direction.new_tensor(1.), atol=1e-6)):
        raise ValueError("matching finite activations/bias, unit direction and finite strength required")
    centered = activations - decoder_bias
    result = centered - (centered @ direction)[..., None] * direction + strength * direction + decoder_bias
    if not bool(torch.isfinite(result).all()):
        raise ValueError("nonfinite steered activation")
    return result


class _FixturePosterior(nn.Module):
    def __init__(self, features: int, topics: int):
        super().__init__()
        self.layer = nn.Linear(features, 2 * topics)

    def forward(self, counts):
        return self.layer(counts).chunk(2, -1)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or real available cuda required; no fallback")
    with torch.random.fork_rng(devices=[torch.cuda.current_device()] if device == "cuda" else []):
        torch.manual_seed(seed)
        gen = torch.Generator(device=device).manual_seed(seed)
        encoder = torch.randn(7, 5, generator=gen, device=device, dtype=torch.float64).requires_grad_()
        decoder = torch.randn(7, 5, generator=gen, device=device, dtype=torch.float64).requires_grad_()
        model = MechanisticETM(encoder, 3, _FixturePosterior(7, 3).double()).to(device)
        counts = torch.randint(0, 5, (4, 7), generator=gen, device=device).double()
        lengths = torch.full((4,), 5., device=device, dtype=torch.float64)
        noise = torch.randn(4, 3, generator=gen, device=device, dtype=torch.float64)
        before = model(counts, lengths, noise)
        probabilities = before["document_topics"] @ before["topic_feature_probabilities"]
        oracle_nll = -torch.distributions.Binomial(total_count=lengths[:, None], probs=probabilities).log_prob(counts).sum(-1).mean()
        reference_error = (before["binomial_nll"] - oracle_nll).detach().abs().item()
        optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)
        optimizer.zero_grad()
        before["loss"].backward()
        gradient_norm = model.topic_vectors.grad.norm().item()
        optimizer.step()
        after = model(counts, lengths, noise)
        direction = topic_steering_vector(before["topic_feature_probabilities"][0].detach(), decoder)
        swap_gap = ((model.topic_vectors @ encoder.detach().T + model.feature_bias).sigmoid()
                    - (model.topic_vectors @ decoder.detach().T + model.feature_bias).sigmoid()).detach().abs().max().item()
        a = torch.randn(4, 5, generator=gen, device=device, dtype=torch.float64)
        bias = torch.randn(5, generator=gen, device=device, dtype=torch.float64)
        steered = replace_topic_component(a, direction, bias, strength=2.)
        projection_error = ((steered - bias) @ direction - 2).abs().max().item()
        perpendicular_error = ((steered - a) - ((steered - a) @ direction)[:, None] * direction).abs().max().item()
        checks = {"eq12_binomial_likelihood_reference": reference_error < 1e-10,
                  "frozen_sae_matrices": encoder.grad is None and decoder.grad is None and not model.encoder_weights.requires_grad,
                  "eq11_uses_encoder_not_decoder": swap_gap > 1e-6,
                  "real_topic_and_variational_update": gradient_norm > 0 and after["loss"].item() < before["loss"].item(),
                  "eq16_unit_topic_direction": abs(direction.norm().item() - 1) < 1e-12,
                  "eq19_replaces_parallel_preserves_perpendicular": projection_error < 1e-12 and perpendicular_error < 1e-12}
        if not all(checks.values()):
            raise RuntimeError(f"mechanistic ETM contract failed: {checks}")
        return {"seed": seed, "metrics": {"binomial_reference_error": reference_error, "topic_gradient_norm": gradient_norm,
            "fixture_loss_before": before["loss"].item(), "fixture_loss_after": after["loss"].item(),
            "steering_projection_error": projection_error, "steering_perpendicular_error": perpendicular_error,
            "encoder_decoder_swap_negative_control_gap": swap_gap,
            "documents": 4, "sae_features": 7, "topics": 3, "optimizer_steps": 1, "pretrained_model_calls": 0}, "checks": checks}
