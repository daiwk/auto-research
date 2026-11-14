"""ECG shared representation and exact RAG fine-tuning loss (2604.14403).

Only the differentiable representation/loss kernel is implemented. There is no
pretrained decoder, corpus index, answer generator or on-device latency claim.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/ecg-rag-a100-20261113.json"


class GatedProjection(nn.Module):
    """Appendix A.1: four scalar-gated residual layers; final projection is signed.

    The paper says a large positive gate bias, not an exact number. Five is a
    documented local initialization, not a recovered unpublished hyperparameter.
    """
    def __init__(self, dimension: int, gate_bias: float = 5.):
        super().__init__()
        if dimension < 1 or not math.isfinite(gate_bias):
            raise ValueError("positive dimension and finite gate bias required")
        self.norms = nn.ModuleList([nn.LayerNorm(dimension) for _ in range(4)])
        self.projections = nn.ModuleList([nn.Linear(dimension, dimension) for _ in range(4)])
        self.gates = nn.ModuleList([nn.Linear(dimension, 1) for _ in range(4)])
        for gate in self.gates:
            nn.init.constant_(gate.bias, gate_bias)

    def forward(self, hidden: Tensor) -> Tensor:
        for i, (norm, projection, gate) in enumerate(zip(self.norms, self.projections, self.gates, strict=True)):
            projected = projection(norm(hidden))
            hidden = torch.sigmoid(gate(hidden)) * hidden + (F.relu(projected) if i < 3 else projected)
        return hidden


class SharedRepresentation(nn.Module):
    """Store only E_ret; undo sqrt(d) scaling before the compression projection."""
    def __init__(self, dimension: int):
        super().__init__()
        self.dimension = dimension
        self.retrieval = GatedProjection(dimension)
        self.compression = GatedProjection(dimension)

    def encode(self, embedding_hidden: Tensor) -> Tensor:
        return self.retrieval(embedding_hidden) / math.sqrt(self.dimension)

    def compress(self, stored_retrieval: Tensor) -> Tensor:
        return self.compression(stored_retrieval * math.sqrt(self.dimension))


def mean_maxsim(query: Tensor, documents: Tensor) -> Tensor:
    """[B,Q,D] x [B,K,T,D] -> [B,K], mean over queries, max over document tokens."""
    if query.ndim != 3 or documents.ndim != 4 or query.shape[0] != documents.shape[0] or query.shape[-1] != documents.shape[-1] or min(query.shape[1], documents.shape[1], documents.shape[2]) < 1:
        raise ValueError("nonempty compatible multi-vector batches required")
    return torch.einsum("bqd,bktd->bkqt", query, documents).amax(dim=-1).mean(dim=-1)


def joint_loss(student_logits: Tensor, teacher_logits: Tensor, scores: Tensor,
               teacher_scores: Tensor, positive: Tensor, hard_negative_mask: Tensor,
               temperature: Tensor, alpha: Tensor, token_mask: Tensor | None = None) -> dict[str, Tensor]:
    """Appendix B.5.1, averaged over questions; FKL sums answer-token KLs.

    Teacher logits and relevance scores are detached. The temperature and alpha
    remain trainable. Every candidate is in the InfoNCE denominator; only the
    declared hard negatives enter teacher margin MSE.
    """
    if student_logits.ndim != 3 or student_logits.shape != teacher_logits.shape:
        raise ValueError("matching [batch,tokens,vocabulary] logits required")
    batch = student_logits.shape[0]
    if scores.ndim != 2 or scores.shape != teacher_scores.shape or scores.shape[0] != batch or positive.shape != (batch,) or positive.dtype != torch.long or hard_negative_mask.shape != scores.shape or hard_negative_mask.dtype != torch.bool:
        raise ValueError("compatible relevance arrays, long positives and boolean hard mask required")
    if positive.device != scores.device or bool(((positive < 0) | (positive >= scores.shape[1])).any()):
        raise ValueError("positive index outside candidate support")
    if temperature.numel() != 1 or alpha.numel() != 1 or not bool(torch.isfinite(temperature).all()) or not bool(temperature > 0):
        raise ValueError("finite positive scalar temperature required")
    arrays = [student_logits, teacher_logits, scores, teacher_scores, alpha]
    if any(not bool(torch.isfinite(x).all()) or x.device != scores.device for x in arrays):
        raise ValueError("finite same-device values required")
    if bool(hard_negative_mask.gather(1, positive[:, None]).any()) or bool((hard_negative_mask.sum(dim=1) == 0).any()):
        raise ValueError("every question needs hard negatives excluding its positive")
    if token_mask is None:
        token_mask = torch.ones(student_logits.shape[:2], dtype=torch.bool, device=student_logits.device)
    if token_mask.shape != student_logits.shape[:2] or token_mask.dtype != torch.bool or bool((token_mask.sum(dim=1) == 0).any()):
        raise ValueError("nonempty per-question answer mask required")
    teacher_logp = teacher_logits.detach().log_softmax(dim=-1)
    token_kl = (teacher_logp.exp() * (teacher_logp - student_logits.log_softmax(dim=-1))).sum(dim=-1)
    generation = (token_kl * token_mask).sum(dim=-1).mean()
    contrastive = F.cross_entropy(scores / temperature, positive)
    delta_s = scores.gather(1, positive[:, None]) - scores
    frozen_teacher = teacher_scores.detach()
    delta_t = frozen_teacher.gather(1, positive[:, None]) - frozen_teacher
    margin = (((delta_s - alpha * delta_t).square() * hard_negative_mask).sum(dim=1) / hard_negative_mask.sum(dim=1)).mean()
    return {"total": generation + contrastive + margin, "generation": generation, "contrastive": contrastive, "margin": margin}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    target = torch.device(device)
    if target.type not in {"cpu", "cuda"}:
        raise ValueError("CPU/CUDA required")
    with torch.random.fork_rng(devices=[] if target.type == "cpu" else [target.index or torch.cuda.current_device()]):
        torch.manual_seed(seed)
        model = SharedRepresentation(4).to(target)
        hidden = torch.randn(2, 3, 3, 4, device=target)
        stored = model.encode(hidden)
        compressed = model.compress(stored)
        scores = mean_maxsim(stored[:, 0], stored)
        teacher = torch.randn(2, 2, 5, device=target, requires_grad=True)
        logits = compressed[:, :2, :2].mean(dim=2) @ torch.randn(4, 5, device=target)
        t_scores = torch.randn(2, 3, device=target, requires_grad=True)
        tau = torch.tensor(1., device=target, requires_grad=True)
        alpha = torch.tensor(.5, device=target, requires_grad=True)
        positive = torch.tensor([0, 1], device=target)
        hard = torch.tensor([[False, True, False], [True, False, True]], device=target)
        loss = joint_loss(logits, teacher, scores, t_scores, positive, hard, tau, alpha)
        loss["total"].backward()
        grad = sum(float(p.grad.abs().sum()) for p in model.parameters() if p.grad is not None)
        checks = {"shared_projection_receives_gradients": grad > 0,
                  "teacher_is_frozen": teacher.grad is None and t_scores.grad is None,
                  "alpha_and_temperature_trainable": alpha.grad is not None and tau.grad is not None,
                  "finite_components": all(bool(torch.isfinite(x)) for x in loss.values()),
                  "requested_device": stored.device.type == target.type,
                  "compression_depends_on_stored_retrieval": compressed.grad_fn is not None}
        return {"seed": seed, "device": str(target), "metrics": {**{k + "_loss": float(v.detach()) for k, v in loss.items()}, "projection_gradient_l1": grad}, "checks": checks,
                "diagnostic_only": True, "evaluation_tier": "l1_mechanism"}
