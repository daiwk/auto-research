"""FLINT fixed-budget pooling and MaxSim (arXiv:2610.27273v1).

The independent implementation follows Sec. 2, Fig. 1 and the authors' MIT
implementation at 3b3f3e37d34e32ca5c92cc5b66e3f778ae4210ec. Inputs are
already-encoded token vectors, not a replacement for a trained text backbone.
"""
from __future__ import annotations

import math
from typing import Literal

import torch
from torch import Tensor, nn
from torch.nn import functional as F


Side = Literal["query", "doc"]
UPSTREAM_REVISION = "3b3f3e37d34e32ca5c92cc5b66e3f778ae4210ec"


class FlintLatentPool(nn.Module):
    """Shared pre-LN cross-attention/FFN with distinct query/document latents.

    ``attention_mask`` is boolean with True for a valid token. Every row must
    contain at least one valid token: an empty context has no attention
    distribution and is rejected instead of silently producing NaNs. No latent
    self-attention or post-residual normalization is added.
    """

    def __init__(self, dim: int = 768, num_latents: int = 32, num_heads: int = 8,
                 ff_ratio: float = 4.0, dropout: float = 0.1) -> None:
        super().__init__()
        if (not all(isinstance(x, int) and not isinstance(x, bool) and x > 0
                    for x in (dim, num_latents, num_heads))
                or dim % num_heads):
            raise ValueError("positive integer dimensions and dim divisible by num_heads required")
        if not math.isfinite(ff_ratio) or ff_ratio <= 0 or int(dim * ff_ratio) < 1:
            raise ValueError("ff_ratio must define a positive finite feed-forward width")
        if not math.isfinite(dropout) or not 0 <= dropout < 1:
            raise ValueError("dropout must be finite in [0, 1)")
        self.dim = dim
        self.num_latents = num_latents
        self.num_heads = num_heads
        self.query_latents = nn.Parameter(torch.randn(num_latents, dim) * 0.02)
        self.doc_latents = nn.Parameter(torch.randn(num_latents, dim) * 0.02)
        self.norm_latents_cross = nn.LayerNorm(dim)
        self.norm_context_cross = nn.LayerNorm(dim)
        self.cross_attn = nn.MultiheadAttention(dim, num_heads, dropout=dropout, batch_first=True)
        self.norm_ff = nn.LayerNorm(dim)
        self.ff = nn.Sequential(nn.Linear(dim, int(dim * ff_ratio)), nn.GELU(),
                                nn.Linear(int(dim * ff_ratio), dim), nn.Dropout(dropout))
        self.dropout = nn.Dropout(dropout)

    def forward(self, token_embeddings: Tensor, attention_mask: Tensor | None = None,
                *, side: Side = "doc") -> Tensor:
        if side not in {"query", "doc"}:
            raise ValueError("side must be query or doc")
        x = token_embeddings
        if (x.ndim != 3 or min(x.shape) < 1 or x.shape[-1] != self.dim
                or not x.is_floating_point() or not bool(torch.isfinite(x).all())):
            raise ValueError("finite nonempty floating (batch, tokens, dim) input required")
        if attention_mask is None:
            attention_mask = torch.ones(x.shape[:2], dtype=torch.bool, device=x.device)
        if (attention_mask.shape != x.shape[:2] or attention_mask.dtype != torch.bool
                or attention_mask.device != x.device):
            raise ValueError("attention_mask must be boolean (batch, tokens) on the input device")
        if not bool(attention_mask.any(dim=1).all()):
            raise ValueError("each context must contain at least one unmasked token")
        parameter = self.query_latents if side == "query" else self.doc_latents
        latents = parameter.unsqueeze(0).expand(x.shape[0], -1, -1)
        context = self.norm_context_cross(x)
        attention, _ = self.cross_attn(
            self.norm_latents_cross(latents), context, context,
            key_padding_mask=~attention_mask, need_weights=False,
        )
        hidden = latents + self.dropout(attention)
        return hidden + self.ff(self.norm_ff(hidden))


def flint_maxsim(query_vectors: Tensor, document_vectors: Tensor) -> Tensor:
    """Eq. 2, aligned query/document batches, sum(query) of max(document).

    Inputs are projected vectors; this function does not silently normalize,
    average, take the reverse maximum, or build an all-pairs corpus index.
    """
    q, d = query_vectors, document_vectors
    if (q.ndim != 3 or d.ndim != 3 or min(q.shape) < 1 or min(d.shape) < 1
            or q.shape[0] != d.shape[0] or q.shape[-1] != d.shape[-1]
            or not q.is_floating_point() or not d.is_floating_point()
            or q.device != d.device or q.dtype != d.dtype
            or not bool(torch.isfinite(q).all()) or not bool(torch.isfinite(d).all())):
        raise ValueError("finite aligned floating query/document batches with matching dtype/device required")
    return (q @ d.transpose(-1, -2)).max(dim=-1).values.sum(dim=-1)


class FlintFixedBudgetRetrieval(nn.Module):
    """Pooling, bias-free projection, L2 normalization and aligned MaxSim.

    ModernBERT uses a shared projection; BERT has separate query/document
    projections (Appendix B and official code clarify the main-text shorthand).
    This module deliberately contains no tokenizer, backbone or PLAID index.
    """

    def __init__(self, dim: int = 768, num_latents: int = 32, num_heads: int = 8,
                 ff_ratio: float = 4.0, dropout: float = 0.1,
                 projection_dim: int = 128, *, shared_projection: bool = True) -> None:
        super().__init__()
        if not isinstance(projection_dim, int) or isinstance(projection_dim, bool) or projection_dim < 1:
            raise ValueError("projection_dim must be a positive integer")
        if not isinstance(shared_projection, bool):
            raise ValueError("shared_projection must be boolean")
        self.pool = FlintLatentPool(dim, num_latents, num_heads, ff_ratio, dropout)
        self.query_projection = nn.Linear(dim, projection_dim, bias=False)
        self.document_projection = (self.query_projection if shared_projection
                                    else nn.Linear(dim, projection_dim, bias=False))

    def encode(self, token_embeddings: Tensor, attention_mask: Tensor | None = None,
               *, side: Side = "doc") -> Tensor:
        vectors = self.pool(token_embeddings, attention_mask, side=side)
        projection = self.query_projection if side == "query" else self.document_projection
        return F.normalize(projection(vectors), p=2, dim=-1)

    def forward(self, query_tokens: Tensor, document_tokens: Tensor,
                query_mask: Tensor | None = None, document_mask: Tensor | None = None) -> Tensor:
        return flint_maxsim(self.encode(query_tokens, query_mask, side="query"),
                            self.encode(document_tokens, document_mask, side="doc"))


def run_flint_diagnostic(*, seed: int = 42, device: str = "cpu") -> dict[str, object]:
    """Small generated-input forward/backward diagnostic; no retrieval claim.

    CUDA requests fail if unavailable rather than falling back to CPU. The
    caller must record source commit/hash and real GPU evidence separately.
    """
    target = torch.device(device)
    if target.type not in {"cpu", "cuda"}:
        raise ValueError("diagnostic device must be cpu or cuda")
    if target.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is unavailable")
    with torch.random.fork_rng(devices=[] if target.type == "cpu" else [target.index or 0]):
        torch.manual_seed(seed)
        model = FlintFixedBudgetRetrieval(dim=16, num_latents=4, num_heads=4, ff_ratio=2,
                                         dropout=0, projection_dim=8).to(target)
        query = torch.randn(3, 7, 16, device=target, requires_grad=True)
        document = torch.randn(3, 11, 16, device=target, requires_grad=True)
        qmask = torch.ones(3, 7, device=target, dtype=torch.bool)
        dmask = torch.ones(3, 11, device=target, dtype=torch.bool)
        qmask[:, -2:] = False
        dmask[:, -3:] = False
        scores = model(query, document, qmask, dmask)
        loss = (scores - torch.tensor([1., -1., .5], device=target)).square().mean()
        loss.backward()
        gradients = [p.grad for p in model.parameters() if p.requires_grad]
        with torch.no_grad():
            changed = query.detach().clone()
            changed[~qmask] = 1000
            mask_error = (model(changed, document.detach(), qmask, dmask) - scores.detach()).abs().max()
            q = model.encode(query.detach(), qmask, side="query")
            d = model.encode(document.detach(), dmask, side="doc")
        return {"seed": seed, "device": str(target), "evaluation_tier": "l1_mechanism",
                "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
                "upstream_revision": UPSTREAM_REVISION, "pretrained_checkpoint": None,
                "dataset": "generated-token-vectors", "batch_size": 3,
                "query_vectors": q.shape[1], "document_vectors": d.shape[1],
                "pairwise_comparisons_per_pair": q.shape[1] * d.shape[1],
                "loss": float(loss.detach()), "mean_score": float(scores.detach().mean()),
                "all_parameter_gradients_finite": all(
                    g is not None and bool(torch.isfinite(g).all()) for g in gradients),
                "parameter_gradient_norm": sum(float(g.norm()) for g in gradients if g is not None),
                "query_gradient_norm": float(query.grad.norm()),
                "document_gradient_norm": float(document.grad.norm()),
                "masked_query_gradient_max": float(query.grad[~qmask].abs().max()),
                "masked_document_gradient_max": float(document.grad[~dmask].abs().max()),
                "masked_content_score_error": float(mask_error),
                "normalization_max_error": float((q.norm(dim=-1) - 1).abs().max()),
                "full_experiment_status": "not_reproduced_high_cost"}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict[str, object]:
    """Scalar/check interface for the source-frozen multi-component runner."""
    result = run_flint_diagnostic(seed=seed, device=device)
    metrics = {key: float(result[key]) for key in (
        "loss", "mean_score", "parameter_gradient_norm", "query_gradient_norm",
        "document_gradient_norm", "masked_query_gradient_max", "masked_document_gradient_max",
        "masked_content_score_error", "normalization_max_error", "query_vectors",
        "document_vectors", "pairwise_comparisons_per_pair",
    )}
    checks = {
        "all_parameter_gradients_finite": result["all_parameter_gradients_finite"],
        "all_metrics_finite": all(math.isfinite(value) for value in metrics.values()),
        "input_and_parameter_gradients_nonzero": all(metrics[key] > 0 for key in (
            "parameter_gradient_norm", "query_gradient_norm", "document_gradient_norm")),
        "masked_inputs_have_zero_gradient": metrics["masked_query_gradient_max"] == 0
        and metrics["masked_document_gradient_max"] == 0,
        "masked_content_invariant": metrics["masked_content_score_error"] < 1e-5,
        "projected_vectors_l2_normalized": metrics["normalization_max_error"] < 1e-5,
        "fixed_symmetric_vector_budget": metrics["query_vectors"] == metrics["document_vectors"] == 4,
    }
    return {"seed": seed, "metrics": metrics, "checks": checks}
