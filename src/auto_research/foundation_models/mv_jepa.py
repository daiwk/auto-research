"""MV-JEPA token-level tiny wiring and loss diagnostic, fixed v1 Section3.

No V-JEPA checkpoint, image tokenizer, video dataset or capability benchmark is
provided. The held-out view is a teacher target, never a student/predictor input.
"""

from __future__ import annotations

import copy
import math
import random

import torch
from torch import nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


def replay_schedule(seed: int, *, multiview: int = 152, replay: int = 148) -> tuple[str, ...]:
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in (multiview, replay)):
        raise ValueError("schedule counts must be nonnegative integers")
    if multiview + replay == 0:
        raise ValueError("empty schedule")
    rows = ["multiview"] * multiview + ["replay"] * replay
    random.Random(seed).shuffle(rows)
    return tuple(rows)


def _position(indices: torch.Tensor, width: int, dtype: torch.dtype) -> torch.Tensor:
    frequencies = torch.exp(torch.arange(0, width, 2, device=indices.device, dtype=torch.float32)
                            * (-math.log(10000.0) / width))
    angles = indices.float().unsqueeze(-1) * frequencies
    return torch.stack((angles.sin(), angles.cos()), dim=-1).flatten(-2).to(dtype)


def _features(value: torch.Tensor, dimensions: int, name: str):
    if (not isinstance(value, torch.Tensor) or value.ndim != dimensions
            or not value.is_floating_point() or not all(value.shape)
            or not torch.isfinite(value).all().item()):
        raise ValueError(f"{name} must be a finite nonempty floating tensor of rank {dimensions}")


def multiview_loss(pred_context: torch.Tensor, target_context: torch.Tensor,
                   pred_heldout: torch.Tensor, target_heldout: torch.Tensor,
                   masked: torch.Tensor) -> torch.Tensor:
    """Eq4: unit token weights, normalize each example then batch-average.

    Teacher targets are detached here as well as in the encoder path. Numerical
    reductions use float32 for fp16/bf16; double inputs retain double precision.
    """
    _features(pred_context, 4, "pred_context")
    for tensor, rank, name in ((target_context, 4, "target_context"),
                               (pred_heldout, 3, "pred_heldout"), (target_heldout, 3, "target_heldout")):
        _features(tensor, rank, name)
    if (pred_context.shape != target_context.shape or pred_heldout.shape != target_heldout.shape
            or pred_context.shape[0] != pred_heldout.shape[0]
            or pred_context.shape[-1] != pred_heldout.shape[-1]
            or masked.shape != pred_context.shape[:-1] or masked.dtype != torch.bool
            or any(x.device != pred_context.device for x in
                   (target_context, pred_heldout, target_heldout, masked))):
        raise ValueError("prediction/target/mask shapes or devices do not agree")
    dtype = torch.float64 if pred_context.dtype == torch.float64 else torch.float32
    context_error = (pred_context.to(dtype) - target_context.detach().to(dtype)).abs().mean(-1)
    heldout_error = (pred_heldout.to(dtype) - target_heldout.detach().to(dtype)).abs().mean(-1)
    numerator = (context_error * masked).sum((1, 2)) + heldout_error.sum(1)
    denominator = masked.sum((1, 2)) + pred_heldout.shape[1]
    return (numerator / denominator).mean()


class _TinyEncoder(nn.Module):
    def __init__(self, input_width: int, width: int, heads: int):
        super().__init__()
        self.project = nn.Linear(input_width, width)
        self.block = nn.TransformerEncoderLayer(width, heads, width * 2, dropout=0,
                                                batch_first=True, norm_first=True)

    def forward(self, tokens: torch.Tensor, positions: torch.Tensor) -> torch.Tensor:
        projected = self.project(tokens)
        return self.block(projected + _position(positions, projected.shape[-1], projected.dtype))


class TinyMVJEPA(nn.Module):
    """Real small encoder/predictor with independently encoded context views.

    Inputs are caller-supplied token features, not pixels. The tiny 1-D position
    code is not the pretrained V-JEPA spatial/temporal positional encoding.
    """

    def __init__(self, input_width: int = 6, width: int = 8, heads: int = 2,
                 max_context_views: int = 6):
        super().__init__()
        if (width <= 0 or width % 2 or heads <= 0 or width % heads
                or input_width <= 0 or max_context_views < 1):
            raise ValueError("positive widths/heads, even width divisible by heads required")
        self.encoder = _TinyEncoder(input_width, width, heads)
        self.teacher = copy.deepcopy(self.encoder).requires_grad_(False)
        self.project = nn.Linear(width, width)
        self.predictor = nn.TransformerEncoderLayer(width, heads, width * 2, dropout=0,
                                                    batch_first=True, norm_first=True)
        self.output = nn.Linear(width, width)
        self.view_embeddings = nn.Embedding(max_context_views + 1, width)
        self.mask_context = nn.Parameter(torch.zeros(width))
        self.mask_heldout = nn.Parameter(torch.zeros(width))
        self.max_context_views = max_context_views
        self.width = width

    def _validate(self, context, masked):
        _features(context, 4, "context")
        if (context.shape[1] > self.max_context_views or context.shape[-1] != self.encoder.project.in_features
                or masked.shape != context.shape[:-1] or masked.dtype != torch.bool
                or masked.device != context.device or masked.all(-1).any().item()):
            raise ValueError("each context view needs a visible token and a matching boolean mask")

    def forward(self, context: torch.Tensor, heldout: torch.Tensor,
                masked: torch.Tensor, view_ids: torch.Tensor | None = None) -> dict[str, torch.Tensor]:
        self._validate(context, masked)
        _features(heldout, 3, "heldout")
        batch, views, tokens, _ = context.shape
        if heldout.shape != (batch, tokens, context.shape[-1]) or heldout.device != context.device:
            raise ValueError("held-out token shape/device must match context")
        if view_ids is None:
            view_ids = torch.stack([torch.randperm(self.max_context_views, device=context.device)[:views]
                                    for _ in range(batch)])
        if (view_ids.shape != (batch, views) or view_ids.dtype != torch.int64
                or view_ids.device != context.device or (view_ids < 0).any().item()
                or (view_ids >= self.max_context_views).any().item()
                or any(row.unique().numel() != views for row in view_ids)):
            raise ValueError("context view IDs must be distinct and exclude the held-out reserved ID")
        positions = torch.arange(tokens, device=context.device)
        pred_context, pred_heldout = [], []
        for b in range(batch):
            visibles, queries, indices = [], [], []
            for k in range(views):
                visible = positions[~masked[b, k]]
                missing = positions[masked[b, k]]
                z = self.encoder(context[b, k, visible].unsqueeze(0), visible)[0]
                embedding = self.view_embeddings(view_ids[b, k])
                visibles.append(self.project(z) + embedding)
                queries.append(self.mask_context + embedding + _position(missing, self.width, context.dtype))
                indices.append(missing)
            held_queries = (self.mask_heldout + self.view_embeddings.weight[self.max_context_views]
                            + _position(positions, self.width, context.dtype))
            visible_count = sum(row.shape[0] for row in visibles)
            joint = torch.cat(visibles + queries + [held_queries]).unsqueeze(0)
            predictions = self.output(self.predictor(joint))[0]
            result = context.new_zeros(views, tokens, self.width)
            offset = visible_count
            for k, missing in enumerate(indices):
                result[k, missing] = predictions[offset:offset + len(missing)]
                offset += len(missing)
            pred_context.append(result)
            pred_heldout.append(predictions[offset:offset + tokens])
        pc, ph = torch.stack(pred_context), torch.stack(pred_heldout)
        with torch.no_grad():
            target_context = F.layer_norm(self.teacher(context.flatten(0, 1), positions), (self.width,))
            target_context = target_context.view(batch, views, tokens, self.width)
            target_heldout = F.layer_norm(self.teacher(heldout, positions), (self.width,))
        loss = multiview_loss(pc, target_context, ph, target_heldout, masked)
        return {"loss": loss, "pred_context": pc, "pred_heldout": ph,
                "target_context": target_context, "target_heldout": target_heldout}

    def single_view_replay(self, tokens: torch.Tensor, masked: torch.Tensor) -> torch.Tensor:
        """Shares online encoder and predictor; caller supplies one replay mask.

        This executes a token-level replay loss, not the original image/video
        mask generators or V-JEPA2.1 visible-token distance weighting.
        """
        self._validate(tokens.unsqueeze(1), masked.unsqueeze(1))
        positions = torch.arange(tokens.shape[1], device=tokens.device)
        losses = []
        for row, mask in zip(tokens, masked, strict=True):
            visible, missing = positions[~mask], positions[mask]
            if not len(missing):
                raise ValueError("replay needs at least one masked target")
            z = self.project(self.encoder(row[visible].unsqueeze(0), visible)[0])
            queries = self.mask_context + _position(missing, self.width, row.dtype)
            pred = self.output(self.predictor(torch.cat((z, queries)).unsqueeze(0)))[0, len(visible):]
            with torch.no_grad():
                target = F.layer_norm(self.teacher(row.unsqueeze(0), positions)[0], (self.width,))[missing]
            losses.append(F.l1_loss(pred.float(), target.float()))
        return torch.stack(losses).mean()

    @torch.no_grad()
    def update_teacher(self, momentum: float = 0.99925):
        if not math.isfinite(momentum) or not 0 <= momentum <= 1:
            raise ValueError("EMA momentum must lie in [0,1]")
        for teacher, student in zip(self.teacher.parameters(), self.encoder.parameters(), strict=True):
            teacher.mul_(momentum).add_(student, alpha=1 - momentum)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    model = TinyMVJEPA().to(device)
    context = torch.randn(2, 2, 6, 6, device=device, requires_grad=True)
    heldout = torch.randn(2, 6, 6, device=device, requires_grad=True)
    masked = torch.zeros(2, 2, 6, device=device, dtype=torch.bool)
    masked[:, :, [1, 4]] = True
    view_ids = torch.tensor([[0, 1], [1, 2]], device=device)
    result = model(context, heldout, masked, view_ids)
    with torch.no_grad():
        altered_held = model(context, heldout + torch.randn_like(heldout) * 30, masked, view_ids)
        altered_context = context.detach().clone()
        altered_context[masked] += torch.randn_like(altered_context[masked]) * 30
        altered_masked = model(altered_context, heldout, masked, view_ids)
    heldout_leak = (result["pred_heldout"] - altered_held["pred_heldout"]).abs().max().item()
    masked_leak = (result["pred_heldout"] - altered_masked["pred_heldout"]).abs().max().item()
    result["loss"].backward()
    gradient = sum(p.grad.abs().sum().item() for p in model.encoder.parameters() if p.grad is not None)
    predictor_gradient = sum(p.grad.abs().sum().item() for p in model.predictor.parameters() if p.grad is not None)
    replay = model.single_view_replay(context.detach()[:, 0], masked[:, 0])
    old_teacher = next(model.teacher.parameters()).detach().clone()
    optimizer = torch.optim.SGD(model.encoder.parameters(), lr=0.01)
    optimizer.step()
    current_student = next(model.encoder.parameters()).detach().clone()
    model.update_teacher()
    expected = old_teacher * 0.99925 + current_student * 0.00075
    ema_error = (next(model.teacher.parameters()) - expected).abs().max().item()
    schedule = replay_schedule(seed)
    checks = {
        "heldout_is_target_only": heldout_leak == 0 and heldout.grad is None,
        "masked_context_tokens_cannot_reach_student": masked_leak == 0 and context.grad[masked].abs().sum().item() == 0,
        "independent_context_encoder_receives_gradient": math.isfinite(gradient) and gradient > 0,
        "joint_predictor_receives_gradient": math.isfinite(predictor_gradient) and predictor_gradient > 0,
        "teacher_frozen": all(p.grad is None and not p.requires_grad for p in model.teacher.parameters()),
        "target_layernorm_detached": not result["target_heldout"].requires_grad,
        "ema_after_online_step": ema_error < 1e-6 and not torch.equal(old_teacher, current_student),
        "exact_replay_mix": schedule.count("multiview") == 152 and schedule.count("replay") == 148,
        "shared_single_view_replay_executes": bool(torch.isfinite(replay)) and replay.item() > 0,
    }
    return {"seed": seed, "device": str(device), "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"multiview_token_l1": result["loss"].item(), "single_view_replay_l1": replay.item(),
                        "online_gradient_l1": gradient, "heldout_prediction_leak_delta": heldout_leak,
                        "masked_prediction_leak_delta": masked_leak, "ema_max_error": ema_error}, "checks": checks}
