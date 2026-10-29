"""GUI-JEPA v1 residual-latent predictor and structural/listwise policy heads.

Bounded latent-only component, NOT a GUI agent. Screenshot/CLIP encoders, a11y
enumeration, MiniLM matchers and post-hoc rankers are external and unimplemented.
No gold action enters forward. Smaller widths preserve the defining pathway,
not the author's exact undisclosed transformer implementation or checkpoints.
"""
import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/gui-jepa-a100-20261029.json"


def _finite(x: Tensor, ndim: int) -> None:
    if (x.ndim != ndim or not 0 < x.numel() <= 1_048_576 or not x.is_floating_point()
            or not bool(torch.isfinite(x).all())):
        raise ValueError("bounded finite floating tensor required")


def sine_cosine_positions(height: int, width: int, dimensions: int, *,
                          device: str = "cpu", dtype=torch.float32) -> Tensor:
    """Explicit 2-D sine/cosine patch coordinates, no learned candidate order."""
    if (any(isinstance(v, bool) or not isinstance(v, int) or v < 1 for v in (height, width, dimensions))
            or dimensions % 4 or height * width * dimensions > 1_048_576):
        raise ValueError("positive bounded grid and width divisible by four required")
    omega = 1 / (10000 ** (torch.arange(dimensions // 4, device=device, dtype=dtype) / (dimensions // 4)))
    y, x = torch.meshgrid(torch.arange(height, device=device, dtype=dtype),
                          torch.arange(width, device=device, dtype=dtype), indexing="ij")
    xx, yy = x.flatten()[:, None] * omega, y.flatten()[:, None] * omega
    return torch.cat((xx.sin(), xx.cos(), yy.sin(), yy.cos()), -1)


class CandidateLatentPolicy(nn.Module):
    """Three real transformer layers; external observable latents only.

    The action-conditioned query attends with the screen tokens. Structural
    scoring cannot bypass the conditioned patch latents to read raw ROI/action
    features; action type only contributes the Eq.2 learned scalar bias.
    """

    def __init__(self, dimensions: int, condition_width: int, *, heads: int = 2,
                 action_width: int = 16, action_types: int = 12):
        super().__init__()
        if (any(isinstance(v, bool) or not isinstance(v, int) or v < 1
                for v in (dimensions, condition_width, heads, action_width, action_types))
                or dimensions % heads or dimensions > 256 or condition_width > 1024):
            raise ValueError("bounded dimensions divisible by head count required")
        self.dimensions, self.condition_width = dimensions, condition_width
        self.action_width, self.action_types = action_width, action_types
        self.query = nn.Parameter(torch.zeros(1, 1, dimensions))
        self.action_roi = nn.Sequential(nn.Linear(action_width + dimensions, dimensions),
                                        nn.GELU(), nn.Linear(dimensions, dimensions))
        layer = nn.TransformerEncoderLayer(dimensions, heads, 4 * dimensions,
                                            dropout=0., activation="gelu", batch_first=True)
        self.predictor = nn.TransformerEncoder(layer, 3, enable_nested_tensor=False)
        self.visual_head = nn.Sequential(nn.Linear(2 * dimensions, dimensions), nn.GELU(),
                                         nn.Linear(dimensions, dimensions))
        self.condition_head = nn.Sequential(nn.Linear(condition_width, dimensions), nn.GELU(),
                                            nn.Linear(dimensions, dimensions))
        self.scale = nn.Parameter(torch.ones(()))
        self.type_bias = nn.Embedding(action_types, 1)

    def forward(self, screen: Tensor, actions: Tensor, roi: Tensor, global_action: Tensor,
                condition: Tensor, action_type: Tensor, valid: Tensor,
                positions: Tensor, text_scores: Tensor) -> dict:
        """Return scores/conditioned patches; labels only belong to loss().

        Global actions require an empty ROI (predictor zero feature, structural
        whole-screen pool) and zero external text score. No MiniLM substitute.
        """
        for x, ndim in ((screen, 3), (actions, 3), (condition, 2),
                        (positions, 2), (text_scores, 2)):
            _finite(x, ndim)
        batch, patches, dim = screen.shape
        if (dim != self.dimensions or actions.shape[0] != batch or actions.shape[2] != self.action_width
                or condition.shape != (batch, self.condition_width) or positions.shape != (patches, dim)
                or actions.shape[1] > 128 or batch * actions.shape[1] * patches * dim > 1_048_576
                or roi.shape != actions.shape[:2] + (patches,)
                or any(x.shape != actions.shape[:2] for x in (global_action, action_type, valid, text_scores))
                or any(x.dtype != torch.bool for x in (roi, global_action, valid))
                or action_type.dtype != torch.long or not bool(valid.any(-1).all())
                or bool(((action_type < 0) | (action_type >= self.action_types)).any())
                or bool((roi.any(-1) & global_action).any())
                or bool((valid & ~global_action & ~roi.any(-1)).any())
                or bool((text_scores[global_action] != 0).any())
                or any(x.device != screen.device for x in (actions, roi, global_action, condition,
                                                           action_type, valid, positions, text_scores))
                or any(x.dtype != screen.dtype for x in (actions, condition, positions, text_scores))):
            raise ValueError("aligned observable latent/action/ROI/condition schemas required")
        candidates = actions.shape[1]
        z = screen.detach()[:, None].expand(-1, candidates, -1, -1)
        weights = roi.to(screen.dtype)
        pooled = (z * weights[..., None]).sum(-2) / weights.sum(-1).clamp_min(1)[..., None]
        query = self.query + self.action_roi(torch.cat((actions.detach(), pooled), -1)).reshape(-1, 1, dim)
        sequence = torch.cat(((z + positions.detach()).reshape(-1, patches, dim), query), 1)
        delta = self.predictor(sequence)[:, :patches].reshape(batch, candidates, patches, dim)
        conditioned = z + delta
        roi_pool = (conditioned * weights[..., None]).sum(-2) / weights.sum(-1).clamp_min(1)[..., None]
        full_pool = conditioned.mean(-2)
        roi_pool = torch.where(global_action[..., None], full_pool, roi_pool)
        visual = self.visual_head(torch.cat((roi_pool, full_pool), -1))
        goal = self.condition_head(condition.detach())[:, None]
        latent_scores = self.scale * F.cosine_similarity(visual, goal, dim=-1) + self.type_bias(action_type).squeeze(-1)
        scores = (latent_scores + text_scores.detach()).masked_fill(~valid, -torch.inf)
        return {"scores": scores, "latent_scores": latent_scores, "conditioned_latents": conditioned}


def listwise_loss(scores: Tensor, positive: Tensor, valid: Tensor, *,
                  positive_is_click: Tensor) -> Tensor:
    """Section3.5: mean weighted per-step CE, 1.5 for non-click positives."""
    if (scores.ndim != 2 or valid.shape != scores.shape or valid.dtype != torch.bool
            or positive.shape != scores.shape[:1] or positive.dtype != torch.long
            or positive_is_click.shape != positive.shape or positive_is_click.dtype != torch.bool
            or any(x.device != scores.device for x in (positive, valid, positive_is_click))
            or not bool(valid.any(-1).all()) or not bool(torch.isfinite(scores[valid]).all())
            or bool(((positive < 0) | (positive >= scores.shape[1])).any())
            or not bool(valid.gather(1, positive[:, None]).all())):
        raise ValueError("valid candidate scores and separate training-positive labels required")
    weighted = F.cross_entropy(scores.masked_fill(~valid, -torch.inf), positive, reduction="none")
    return (weighted * torch.where(positive_is_click, 1., 1.5)).mean()


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or real available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    args = {"generator": gen, "device": device, "dtype": torch.float64}
    with torch.random.fork_rng(devices=[torch.cuda.current_device()] if device == "cuda" else []):
        torch.manual_seed(seed)
        model = CandidateLatentPolicy(16, 5).to(device=device, dtype=torch.float64)
    screen = torch.randn(2, 4, 16, **args).requires_grad_()
    actions, condition = torch.randn(2, 3, 16, **args), torch.randn(2, 5, **args)
    roi = torch.tensor([[[1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 0]]] * 2, device=device, dtype=torch.bool)
    glob = torch.tensor([[0, 0, 1]] * 2, device=device, dtype=torch.bool)
    valid = torch.tensor([[1, 1, 1], [1, 0, 1]], device=device, dtype=torch.bool)
    types = torch.tensor([[0, 1, 2]] * 2, device=device)
    pos = sine_cosine_positions(2, 2, 16, device=device, dtype=torch.float64)
    text = torch.zeros(2, 3, device=device, dtype=torch.float64)
    output = model(screen, actions, roi, glob, condition, types, valid, pos, text)
    perm = torch.tensor([2, 0, 1], device=device)
    permuted = model(screen, actions[:, perm], roi[:, perm], glob[:, perm], condition,
                     types[:, perm], valid[:, perm], pos, text[:, perm])["scores"]
    mask = valid[:, perm]
    perm_error = (permuted[mask] - output["scores"][:, perm][mask]).abs().max().item()
    positive = torch.tensor([0, 2], device=device)
    clicks = torch.tensor([True, False], device=device)
    loss = listwise_loss(output["scores"], positive, valid, positive_is_click=clicks)
    logp = output["scores"].log_softmax(-1)
    reference = (-logp[0, 0] - 1.5 * logp[1, 2]) / 2
    loss_error = (loss - reference).abs().item()
    loss.backward()
    predictor_grad = sum(p.grad.norm().item() for p in model.predictor.parameters())
    head_grad = sum(p.grad.norm().item() for p in model.visual_head.parameters())
    before = {n: p.detach().clone() for n, p in model.named_parameters()}
    torch.optim.SGD(model.parameters(), lr=.001).step()
    parameter_delta = sum((p - before[n]).norm().item() for n, p in model.named_parameters())
    checks = {"three_real_transformer_layers": len(model.predictor.layers) == 3,
        "candidate_permutation_equivariant": perm_error < 1e-12,
        "invalid_candidates_cannot_be_selected": bool(torch.isneginf(output["scores"][~valid]).all()),
        "weighted_listwise_independent_reference": loss_error < 1e-12,
        "predictor_and_structural_head_receive_gradient": predictor_grad > 0 and head_grad > 0
            and math.isfinite(predictor_grad + head_grad),
        "frozen_external_screen_receives_no_gradient": screen.grad is None,
        "trainable_policy_parameters_change": parameter_delta > 0,
        "candidate_conditioned_latents_differ": not torch.allclose(output["conditioned_latents"][:, 0], output["conditioned_latents"][:, 1])}
    if not all(checks.values()):
        raise RuntimeError(f"GUI-JEPA checks failed: {checks}")
    return {"seed": seed, "metrics": {"permutation_reference_error": perm_error,
        "loss_reference_error": loss_error, "listwise_loss": loss.item(),
        "predictor_gradient_norm": predictor_grad, "structural_gradient_norm": head_grad,
        "parameter_delta": parameter_delta, "environment_interactions": 0}, "checks": checks}
