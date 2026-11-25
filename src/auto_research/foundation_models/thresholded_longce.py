"""Fixed-v1 §6.2 Eq4 TLCE, CPU-only loss/window interface, not a recall model."""

import math

import torch
from torch import nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = False


def _validate(full, short, offsets, valid):
    if not all(isinstance(x, torch.Tensor) for x in (full, short, offsets, valid)):
        raise ValueError("tensor log-probabilities, offsets and mask required")
    if (full.ndim != 2 or not full.numel() or full.dtype not in {torch.float32, torch.float64}
            or short.dtype != full.dtype or offsets.dtype != torch.int64 or valid.dtype != torch.bool
            or any(x.shape != full.shape or x.device.type != "cpu" for x in (short, offsets, valid))
            or full.device.type != "cpu" or not valid.any()
            or not torch.isfinite(full[valid]).all() or not torch.isfinite(short[valid]).all()
            or (full[valid] > 0).any() or (short[valid] > 0).any()
            or (offsets[valid] < 0).any() or (offsets[valid] >= 512).any()):
        raise ValueError("matching finite CPU log-probs, int64 offsets in [0,512), nonempty bool mask required")


def weights(full, short, offsets, valid):
    """Detached capped ratio; invalid/padded entries have exactly zero weight."""
    _validate(full, short, offsets, valid)
    delta = torch.where(valid, full.detach() - short.detach(), 0.)
    eligible = valid & (delta > 1.) & (offsets >= 128)
    capped = torch.exp(delta.clamp(max=math.log(5.)))
    return torch.where(valid, torch.where(eligible, capped, torch.ones_like(full)), 0.)


def loss(full, short, offsets, valid):
    """Eq4; only the full-context target log-prob receives gradients."""
    w = weights(full, short, offsets, valid)
    safe_full = torch.where(valid, full, 0.)
    return -(w * safe_full).sum() / w.sum()


def context_scores(model, tokens, targets, *, window=512):
    """Run an external CPU causal model, resetting its state at every window.

    `model(sequence)` returns same-length logits and must reset state per call.
    Inputs/targets are already shifted by the caller; no answer/plan is read.
    This interface does not implement the paper's linear-attention architectures.
    """
    if (type(window) is not int or not 1 <= window <= 512
            or not isinstance(tokens, torch.Tensor) or not isinstance(targets, torch.Tensor)
            or tokens.ndim != 2 or not tokens.numel() or targets.shape != tokens.shape
            or tokens.dtype != torch.int64 or targets.dtype != torch.int64
            or tokens.device.type != "cpu" or targets.device.type != "cpu"):
        raise ValueError("matching nonempty CPU int64 sequences and window<=512 required")
    full_logits = model(tokens)
    if full_logits.device.type != "cpu":
        raise ValueError("CPU-only model required")
    full = full_logits.log_softmax(-1).gather(-1, targets[..., None]).squeeze(-1)
    with torch.no_grad():
        chunks = [model(tokens[:, start:start + window]).log_softmax(-1).gather(
            -1, targets[:, start:start + window, None]).squeeze(-1)
            for start in range(0, tokens.shape[1], window)]
        short = torch.cat(chunks, dim=1)
    offsets = (torch.arange(tokens.shape[1]) % window).expand_as(tokens)
    return full, short, offsets


class _TinyCausalModel(nn.Module):
    """Diagnostic GRU that starts with zero state per call, not a paper backbone."""

    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(9, 4)
        self.recurrent = nn.GRU(4, 4, batch_first=True)
        self.head = nn.Linear(4, 9)

    def forward(self, tokens):
        h, _ = self.recurrent(self.embedding(tokens))
        return self.head(h)


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only device required")
    with torch.random.fork_rng():
        torch.manual_seed(seed)
        model = _TinyCausalModel()
    g = torch.Generator().manual_seed(seed)
    tokens = torch.randint(0, 9, (1, 260), generator=g)
    full, short, offsets = context_scores(model, tokens, tokens.roll(-1, 1), window=130)
    valid = torch.ones_like(tokens, dtype=torch.bool)
    loss(full, short, offsets, valid).backward()
    synthetic_full = torch.tensor([[-2., -2., -2., -2.]], requires_grad=True)
    synthetic_short = torch.tensor([[-3., -4., -4., -12.]], requires_grad=True)
    synthetic_offsets = torch.tensor([[128, 127, 128, 129]])
    w = weights(synthetic_full, synthetic_short, synthetic_offsets, torch.ones(1, 4, dtype=torch.bool))
    value = loss(synthetic_full, synthetic_short, synthetic_offsets, torch.ones(1, 4, dtype=torch.bool))
    value.backward()
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": {"strict_threshold_min_context_and_cap": torch.equal(w, torch.tensor([[1., 1., 5., 5.]])),
                       "short_forward_is_detached": not short.requires_grad,
                       "weight_branch_is_detached": not w.requires_grad and synthetic_short.grad is None,
                       "normalized_full_gradient": torch.allclose(synthetic_full.grad, -w / w.sum()),
                       "short_state_resets_at_boundary": bool(torch.equal(full[:, :130], short[:, :130])
                                                                  and not torch.equal(full[:, 130:], short[:, 130:])),
                       "tiny_causal_model_has_gradient": all(p.grad is not None and torch.isfinite(p.grad).all()
                                                             for p in model.parameters())},
            "metrics": {"synthetic_loss": float(value.detach()), "synthetic_total_weight": float(w.sum()),
                        "tiny_model_loss": float(loss(full.detach(), short, offsets, valid))}}
