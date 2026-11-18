"""IntentFlow fixed-index residual projection and distribution/ranking objectives.

Fused query features and teacher scores are explicit inputs. No vision backbone,
intent recognizer, teacher agent or document index is falsely instantiated.
"""

from __future__ import annotations

import torch
from torch import Tensor, nn
import torch.nn.functional as F

REQUIRES_GPU_VALIDATION = True


class QueryResidualProjection(nn.Module):
    """Eqs.18--21: one shared bottleneck per branch, six query-gated experts."""

    def __init__(
        self,
        feature_dim: int,
        embedding_dim: int,
        ranks=(8, 64),
        experts: int = 6,
        beta: float = 0.1,
    ):
        super().__init__()
        if min(feature_dim, embedding_dim, experts, *ranks) <= 0 or beta < 0:
            raise ValueError("positive dimensions/ranks and nonnegative residual scale required")
        self.base = nn.Linear(feature_dim, embedding_dim, bias=False)
        self.base.requires_grad_(False)
        self.gate = nn.Linear(feature_dim, experts, bias=False)
        self.down = nn.ModuleList(nn.Linear(feature_dim, r, bias=False) for r in ranks)
        self.up = nn.ParameterList(
            nn.Parameter(torch.zeros(experts, embedding_dim, r)) for r in ranks
        )
        self.beta = beta

    def forward(self, features: Tensor) -> Tensor:
        base = self.base(features)
        weights = self.gate(features).softmax(-1)
        residual = sum(
            torch.einsum("be,eor,br->bo", weights, up, down(features))
            for down, up in zip(self.down, self.up, strict=True)
        )
        return F.normalize(base + self.beta * base.norm(dim=-1, keepdim=True) * residual, dim=-1)


def distribution_distillation(
    student: Tensor, teacher: Tensor, valid: Tensor, temperature: float = 0.1
) -> Tensor:
    """Eq.16 in both directions; same valid sets and frozen offline teacher."""
    if (
        student.ndim != 2
        or student.shape != teacher.shape
        or valid.shape != student.shape
        or valid.dtype != torch.bool
        or temperature <= 0
        or not valid.any(0).all()
        or not valid.any(1).all()
    ):
        raise ValueError("shared candidate matrix with nonempty rows/columns required")

    def direction(s, t, m):
        logp = (s / temperature).masked_fill(~m, -torch.inf).log_softmax(-1)
        logq = (t.detach() / temperature).masked_fill(~m, -torch.inf).log_softmax(-1)
        # Explicit masking before subtraction avoids -inf - -inf NaNs.
        return (logq.exp() * (logq.masked_fill(~m, 0) - logp.masked_fill(~m, 0))).sum(-1).mean()

    return 0.5 * (direction(student, teacher, valid) + direction(student.T, teacher.T, valid.T))


def csls_correction(scores: Tensor, training_query_scores: Tensor, k: int = 10) -> Tensor:
    """Eq.24: offline document density only; no evaluation-query reference bank."""
    if (
        training_query_scores.ndim != 2
        or scores.shape[-1] != training_query_scores.shape[1]
        or type(k) is not int
        or not 1 <= k <= training_query_scores.shape[0]
    ):
        raise ValueError("training-reference-by-document matrix and valid k required")
    return scores - 0.5 * training_query_scores.topk(k, dim=0).values.mean(0)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device not in {"cpu", "cuda"}:
        raise ValueError("integer seed and explicit cpu/cuda device required")
    torch.manual_seed(seed)
    model = QueryResidualProjection(7, 5, ranks=(2, 3)).to(device)
    features = torch.randn(6, 7, device=device)
    documents = F.normalize(torch.randn(6, 5, device=device), dim=-1)
    before_documents = documents.clone()
    initial = model(features)
    initial_equal = torch.allclose(initial, F.normalize(model.base(features), dim=-1), atol=1e-7)
    teacher = torch.randn(6, 6, device=device, requires_grad=True)
    valid = ~torch.eye(6, device=device, dtype=torch.bool)
    loss = distribution_distillation(initial @ documents.T, teacher, valid)
    loss.backward()
    grad = sum(float(p.grad.abs().sum()) for p in model.up)
    with torch.no_grad():
        for p in model.up:
            p.add_(p.grad, alpha=-0.01)
    changed = not torch.allclose(initial, model(features))
    bank = torch.tensor([[1.0, 0.0], [0.8, 0.1]], device=device)
    corrected = csls_correction(torch.tensor([[1.0, 1.0]], device=device), bank, k=2)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "zero_residual_preserves_base": initial_equal,
            "actual_residual_gradient": grad > 0,
            "query_projection_changes": changed,
            "document_index_unchanged": bool(torch.equal(documents, before_documents)),
            "base_projection_frozen": model.base.weight.grad is None,
            "teacher_detached": teacher.grad is None,
            "density_correction_changes_order": bool(corrected[0, 1] > corrected[0, 0]),
        },
        "metrics": {"distillation_loss": float(loss.detach()), "residual_gradient_l1": grad},
    }
