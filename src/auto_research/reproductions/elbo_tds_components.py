"""ELBO_TDS v2, Eq. 3-7 and Algorithm 1 on supplied feature vectors.

L1 only: no production feature extraction, temporal data pipeline or serving.
Augmentation handles explicit feature slots, not inferred semantic invariants.
"""
from __future__ import annotations

import math

import torch
from torch import nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


def augment_features(
    values: torch.Tensor,
    kinds: tuple[str, ...],
    *,
    views: int,
    selection_probability: float,
    statistical_radius: int,
    bucket_maxima: tuple[int, ...],
    sequence_mask_probability: float,
    categorical_dropout_probability: float,
    generator: torch.Generator,
) -> torch.Tensor:
    """Augment flattened scalar slots; sequence/category slots are embeddings.

    A global Bernoulli feature-selection mask gates each local perturbation.
    Sequence and categorical zeros are unscaled masking (not inverted dropout).
    Statistical slots must already be integer equal-width bucket IDs. Defining
    bucket boundaries or grouping multiple slots into one field is caller-owned.
    """
    if values.ndim != 2 or not values.is_floating_point() or not torch.isfinite(values).all():
        raise ValueError("finite floating [batch, feature] values required")
    if values.numel() == 0 or len(kinds) != values.shape[1] or len(bucket_maxima) != len(kinds):
        raise ValueError("nonempty values and one type/bucket maximum per slot required")
    if isinstance(views, bool) or not isinstance(views, int) or views < 1:
        raise ValueError("positive integer views required")
    if isinstance(statistical_radius, bool) or not isinstance(statistical_radius, int) or statistical_radius < 0:
        raise ValueError("nonnegative integer radius required")
    for p in (selection_probability, sequence_mask_probability, categorical_dropout_probability):
        if not math.isfinite(p) or not 0 <= p <= 1:
            raise ValueError("mask probabilities must lie in [0,1]")
    for i, kind in enumerate(kinds):
        if kind not in {"statistical", "sequential", "categorical"}:
            raise ValueError("unknown feature kind")
        maximum = bucket_maxima[i]
        if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < 0:
            raise ValueError("nonnegative integer bucket maxima required")
        if kind == "statistical" and (
            not torch.equal(values[:, i], values[:, i].round())
            or (values[:, i] < 0).any() or (values[:, i] > maximum).any()
        ):
            raise ValueError("statistical slot is not an in-range bucket ID")
    shape = (views, *values.shape)
    result = values.unsqueeze(0).expand(shape).clone()
    selected = torch.rand(shape, device=values.device, generator=generator) < selection_probability
    for i, kind in enumerate(kinds):
        slot = result[:, :, i]
        if kind == "statistical":
            noise = torch.randint(-statistical_radius, statistical_radius + 1,
                                  slot.shape, device=values.device, generator=generator)
            shifted = (slot + noise).clamp(0, bucket_maxima[i])
            result[:, :, i] = torch.where(selected[:, :, i], shifted, slot)
        else:
            probability = sequence_mask_probability if kind == "sequential" else categorical_dropout_probability
            dropped = torch.rand(slot.shape, device=values.device, generator=generator) < probability
            result[:, :, i] = torch.where(selected[:, :, i] & dropped, torch.zeros_like(slot), slot)
    return result


class ELBOTDSCore(nn.Module):
    """Twin linear encoders/decoders and a deterministic dot-product predictor.

    SSL targets are the individual supplied augmented views (Eq. 4), not a
    fabricated clean latent target. The view mean in Eq. 3 is not detached.
    """

    def __init__(self, user_dim: int, item_dim: int, latent_dim: int):
        super().__init__()
        if any(isinstance(x, bool) or not isinstance(x, int) or x < 1 for x in (user_dim, item_dim, latent_dim)):
            raise ValueError("positive integer dimensions required")
        self.user_encoder = nn.Linear(user_dim, latent_dim)
        self.item_encoder = nn.Linear(item_dim, latent_dim)
        self.user_decoder = nn.Linear(latent_dim, user_dim)
        self.item_decoder = nn.Linear(latent_dim, item_dim)

    def predict(self, users: torch.Tensor, items: torch.Tensor) -> torch.Tensor:
        """Eq. 6: deterministic means, with neither sampling nor augmentation."""
        return (self.user_encoder(users) * self.item_encoder(items)).sum(-1)

    def objective(self, users, items, labels, user_views, item_views, *, alpha, generator=None,
                  user_noise=None, item_noise=None):
        if not math.isfinite(alpha) or alpha < 0:
            raise ValueError("finite nonnegative SSL weight required")
        batch = users.shape[0] if users.ndim == 2 else 0
        if not batch or items.ndim != 2 or items.shape[0] != batch or labels.shape != (batch,):
            raise ValueError("aligned nonempty original user/item/label batches required")
        if user_views.ndim != 3 or item_views.ndim != 3 or user_views.shape[:2] != item_views.shape[:2]:
            raise ValueError("aligned [view,batch,feature] tensors required")
        if user_views.shape[0] < 1 or user_views.shape[1:] != users.shape or item_views.shape[1:] != items.shape:
            raise ValueError("views must match original feature dimensions")
        tensors = (users, items, labels, user_views, item_views)
        if any(not x.is_floating_point() or not torch.isfinite(x).all() for x in tensors):
            raise ValueError("all inputs must be finite floating tensors")
        if any(x.device != users.device or x.dtype != users.dtype for x in tensors):
            raise ValueError("all inputs must share device and dtype")
        if (labels < 0).any() or (labels > 1).any():
            raise ValueError("binary/soft labels must lie in [0,1]")
        mus = (self.user_encoder(user_views), self.item_encoder(item_views))
        noises = []
        for mu, noise in zip(mus, (user_noise, item_noise)):
            if noise is None:
                noise = torch.randn(mu.shape, dtype=mu.dtype, device=mu.device, generator=generator)
            if noise.shape != mu.shape or noise.dtype != mu.dtype or noise.device != mu.device or not torch.isfinite(noise).all():
                raise ValueError("noise must be finite and match the encoded views")
            noises.append(noise)
        zu, zi = (mu + noise for mu, noise in zip(mus, noises))
        prior = (zu - zu.mean(0, keepdim=True)).square().mean() + (zi - zi.mean(0, keepdim=True)).square().mean()
        reconstruction = F.mse_loss(self.user_decoder(zu), user_views) + F.mse_loss(self.item_decoder(zi), item_views)
        prediction = F.binary_cross_entropy_with_logits(self.predict(users, items), labels)
        return {"loss": prediction + alpha * (reconstruction + prior), "prediction": prediction,
                "reconstruction": reconstruction, "prior": prior}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Bounded real autograd with independent arithmetic and gradient controls."""
    if device not in {"cpu", "cuda"}:
        raise ValueError("device must be cpu or cuda")
    torch.manual_seed(seed)
    generator = torch.Generator(device=device).manual_seed(seed)
    model = ELBOTDSCore(4, 4, 3).to(device=device, dtype=torch.float64)
    users = torch.randn((6, 4), device=device, dtype=torch.float64, generator=generator)
    items = torch.randn((6, 4), device=device, dtype=torch.float64, generator=generator)
    users[:, 0] = torch.arange(6, device=device) % 4
    items[:, 0] = torch.arange(6, device=device) % 4
    labels = torch.tensor([0., 1., 1., 0., 1., 0.], device=device, dtype=torch.float64)
    kwargs = dict(kinds=("statistical", "sequential", "categorical", "categorical"),
                  views=3, selection_probability=0.5, statistical_radius=1, bucket_maxima=(3, 0, 0, 0),
                  sequence_mask_probability=0.5, categorical_dropout_probability=0.5, generator=generator)
    uv, iv = augment_features(users, **kwargs), augment_features(items, **kwargs)
    un = torch.randn((3, 6, 3), device=device, dtype=torch.float64, generator=generator)
    inn = torch.randn(un.shape, device=device, dtype=torch.float64, generator=generator)
    terms = model.objective(users, items, labels, uv, iv, alpha=.2, user_noise=un, item_noise=inn)
    zu, zi = model.user_encoder(uv) + un, model.item_encoder(iv) + inn
    independent_prior = sum(((z[a] - z[b]).square().mean()
                             for z in (zu, zi) for a in range(3) for b in range(3))) / 18
    same_prediction = model.objective(users, items, labels, uv + 5, iv - 3, alpha=.2,
                                      user_noise=un, item_noise=inn)["prediction"]
    zero = model.objective(users, items, labels, uv, iv, alpha=0, user_noise=un, item_noise=inn)
    no_change = augment_features(users, **(kwargs | {"selection_probability": 0}))
    before = [p.detach().clone() for p in model.parameters()]
    opt = torch.optim.SGD(model.parameters(), lr=.01)
    opt.zero_grad()
    terms["loss"].backward()
    finite_grad = all(p.grad is not None and torch.isfinite(p.grad).all().item() for p in model.parameters())
    opt.step()
    checks = {"prior_matches_pairwise_identity": bool(torch.allclose(terms["prior"], independent_prior)),
              "supervised_branch_ignores_augmented_views": bool(torch.equal(same_prediction, terms["prediction"])),
              "alpha_zero_removes_ssl": bool(torch.equal(zero["loss"], zero["prediction"])),
              "global_zero_selection_preserves_features": bool(torch.equal(no_change, users.expand(3, -1, -1))),
              "bucket_bounds_preserved": bool(((uv[:, :, 0] >= 0) & (uv[:, :, 0] <= 3)).all()),
              "all_encoder_decoder_gradients_finite": finite_grad,
              "parameters_actually_updated": all(not torch.equal(a, b) for a, b in zip(before, model.parameters()))}
    return {"evaluation_tier": "l1_mechanism", "diagnostic_only": True, "promotion_eligible": False,
            "seed": seed, "checks": checks, "metrics": {k: float(v.detach()) for k, v in terms.items()}}
