"""Inside-JEPA Eqs. 1--4 and five-arm gradient routing (arXiv:2610.31194v1).

Independent L1 mechanism, not a video benchmark or released checkpoint. Inputs
are externally supplied frozen 512-d crop features, boxes and object/hand types.
The paper does not specify the box-MLP topology, relation activation or inverse
head topology: callers supply these explicitly, not an invented official model.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/inside-jepa-a100-20261025.json"
ARMS = ("PRED", "INV-S", "INV-Z", "INV-R", "INV-SHUF")


def box_fourier_features(boxes: Tensor) -> Tensor:
    """Raw normalized xyxy plus sin/cos(2**k*pi*coordinate), k=0..3."""
    if boxes.ndim != 3 or boxes.shape[-1] != 4 or not boxes.is_floating_point():
        raise ValueError("boxes must be floating [batch, entities, 4] xyxy")
    if not bool(torch.isfinite(boxes).all()) or bool(((boxes < 0) | (boxes > 1)).any()):
        raise ValueError("box coordinates must be finite and normalized to [0,1]")
    if bool((boxes[..., 2:] < boxes[..., :2]).any()):
        raise ValueError("box ends must not precede starts")
    frequencies = 2 ** torch.arange(4, device=boxes.device, dtype=boxes.dtype) * math.pi
    angles = boxes[..., :, None] * frequencies
    return torch.cat((boxes, angles.sin().flatten(-2), angles.cos().flatten(-2)), -1)


@dataclass(frozen=True)
class RelationalState:
    r: Tensor
    s: Tensor

    @property
    def z(self) -> Tensor:
        return torch.cat((self.r.flatten(1), self.s.flatten(1)), -1)


class RelationalStateEncoder(nn.Module):
    """128-d entities, 32-d latents, K=8/16 sigmoid ordered-pair channels.

    ``box_mlp`` maps 36 Fourier features to 128 dimensions. ``pair_activation``
    is the explicitly chosen activation between the paper's 512->256->K pair
    layers. Neither supplied choice is claimed to match an unreleased model.
    Four entity slots are retained, including constant-zero diagonal/padding.
    """
    def __init__(self, box_mlp: nn.Module, pair_activation: nn.Module, *, channels: int = 8):
        super().__init__()
        if channels not in (8, 16):
            raise ValueError("paper uses K=8 or K=16")
        self.channels = channels
        self.box_mlp = box_mlp
        self.appearance = nn.Linear(512, 128)
        self.entity_type = nn.Embedding(2, 128)
        self.entity_norm = nn.LayerNorm(128)
        self.entity_projection = nn.Linear(128, 32, bias=False)
        self.latent_norm = nn.LayerNorm(32)
        self.relation = nn.Sequential(nn.Linear(512, 256), pair_activation,
                                      nn.Linear(256, channels))

    @property
    def state_dimension(self) -> int:
        return 4 * 32 + 4 * 4 * self.channels

    def forward(self, features: Tensor, boxes: Tensor, entity_types: Tensor,
                valid: Tensor) -> RelationalState:
        if (features.ndim != 3 or features.shape[1:] != (4, 512)
                or not features.is_floating_point() or features.shape[0] < 1):
            raise ValueError("external frozen crop features must be [batch,4,512]")
        if features.shape[0] > 64:
            raise ValueError("cost gate: at most 64 frame pairs per component call")
        expected = features.shape[:2]
        if boxes.shape != (*expected, 4) or boxes.device != features.device or boxes.dtype != features.dtype:
            raise ValueError("boxes must match feature shape, dtype and device")
        if (entity_types.shape != expected or entity_types.dtype != torch.long
                or entity_types.device != features.device
                or bool(((entity_types < 0) | (entity_types > 1)).any())):
            raise ValueError("entity_types must be matching-device int64 0(object)/1(hand)")
        if (valid.shape != expected or valid.dtype != torch.bool or valid.device != features.device
                or bool((valid.sum(-1) < 2).any())):
            raise ValueError("valid must select 2..4 shared entities in each frame")
        if not bool(torch.isfinite(features).all()):
            raise ValueError("features must be finite")
        geometry = self.box_mlp(box_fourier_features(boxes))
        if geometry.shape != (*expected, 128):
            raise ValueError("supplied box_mlp must output [batch,4,128]")
        # phi is frozen; gradients flow through f, geometry and the type embedding.
        entities = self.entity_norm(self.appearance(features.detach()) + geometry
                                    + self.entity_type(entity_types))
        r = self.latent_norm(self.entity_projection(entities)) * valid[..., None]
        left = entities[:, :, None, :].expand(-1, -1, 4, -1)
        right = entities[:, None, :, :].expand(-1, 4, -1, -1)
        pair_features = torch.cat((left, right, left - right, left * right), -1)
        pair_valid = valid[:, :, None] & valid[:, None, :]
        pair_valid = pair_valid & ~torch.eye(4, dtype=torch.bool, device=features.device)[None]
        s = self.relation(pair_features).sigmoid() * pair_valid[..., None]
        if not bool(torch.isfinite(r).all()) or not bool(torch.isfinite(s).all()):
            raise ValueError("nonfinite encoded state")
        return RelationalState(r, s)


class InsideJEPA(nn.Module):
    """JEPA plus inverse loss; target is EMA, inverse future is ONLINE.

    ``inverse_head(current, future)`` must return action logits or controls. Its
    input width is 16*K, full state_dimension, or 128 for INV-S/Z/R respectively.
    INV-SHUF requires an explicit batch permutation, used ONLY as inverse target.
    Target updates are explicit: call ``update_target`` after an optimizer step.
    """
    def __init__(self, encoder: RelationalStateEncoder, *, arm: str,
                 action_size: int, inverse_head: nn.Module | None = None,
                 continuous_actions: bool = False, action_conditioned: bool = True,
                 ema_momentum: float = .996):
        super().__init__()
        if arm not in ARMS or not isinstance(action_size, int) or not 1 <= action_size <= 256:
            raise ValueError("known arm and integer action size in [1,256] required")
        if not math.isfinite(ema_momentum) or not 0 <= ema_momentum < 1:
            raise ValueError("EMA momentum must be in [0,1)")
        if (arm == "PRED") != (inverse_head is None):
            raise ValueError("PRED has no inverse head; every inverse arm requires an explicit head")
        self.encoder, self.target_encoder = encoder, deepcopy(encoder)
        self.target_encoder.requires_grad_(False)
        self.target_encoder.eval()
        self.arm, self.action_size = arm, action_size
        self.continuous_actions = continuous_actions
        self.action_conditioned = action_conditioned
        self.ema_momentum = ema_momentum
        self.inverse_head = inverse_head
        self.action_embedding = ((nn.Linear(action_size, 64) if continuous_actions
                                  else nn.Embedding(action_size, 64))
                                 if action_conditioned else None)
        dimension = encoder.state_dimension
        self.predictor = nn.Sequential(nn.Linear(dimension + 64 * action_conditioned, 512),
                                       nn.GELU(), nn.Linear(512, dimension))

    def train(self, mode: bool = True):
        super().train(mode)
        self.target_encoder.eval()
        return self

    def _validate_actions(self, actions: Tensor, batch: int, reference: Tensor) -> None:
        if actions.device != reference.device:
            raise ValueError("actions and state must share device")
        if self.continuous_actions:
            if (actions.shape != (batch, self.action_size) or actions.dtype != reference.dtype
                    or not bool(torch.isfinite(actions).all())):
                raise ValueError("controls must be finite [batch,action_size] with state dtype")
        elif (actions.shape != (batch,) or actions.dtype != torch.long
              or bool(((actions < 0) | (actions >= self.action_size)).any())):
            raise ValueError("discrete actions must be int64 [batch] class indices")

    def predict(self, state: RelationalState, actions: Tensor) -> Tensor:
        self._validate_actions(actions, state.r.shape[0], state.r)
        inputs = state.z
        if self.action_embedding is not None:
            inputs = torch.cat((inputs, self.action_embedding(actions)), -1)
        return self.predictor(inputs)

    def inverse_inputs(self, state: RelationalState) -> Tensor:
        if self.arm in ("INV-S", "INV-SHUF"):
            return state.s.flatten(1)
        if self.arm == "INV-R":
            return state.r.flatten(1)
        if self.arm == "INV-Z":
            return state.z
        raise ValueError("PRED has no inverse inputs")

    def losses(self, start: dict[str, Tensor], future: dict[str, Tensor], actions: Tensor, *,
               inverse_permutation: Tensor | None = None) -> dict[str, Tensor]:
        if not torch.equal(start["valid"], future["valid"]):
            raise ValueError("frame pair must use the same shared entity slots")
        current = self.encoder(**start)
        batch = current.r.shape[0]
        self._validate_actions(actions, batch, current.r)
        if self.arm == "INV-SHUF":
            if (inverse_permutation is None or inverse_permutation.device != actions.device
                    or inverse_permutation.shape != (batch,) or inverse_permutation.dtype != torch.long
                    or not torch.equal(inverse_permutation.sort().values,
                                       torch.arange(batch, device=actions.device))
                    or torch.equal(inverse_permutation, torch.arange(batch, device=actions.device))):
                raise ValueError("INV-SHUF requires an explicit nonidentity batch permutation")
        elif inverse_permutation is not None:
            raise ValueError("inverse permutation belongs only to INV-SHUF")
        with torch.no_grad():
            target = self.target_encoder(**future).z
        prediction = self.predict(current, actions)  # true action, including INV-SHUF
        # Per-example squared L2 norm, then batch mean; not elementwise mean.
        forward_loss = (prediction - target).square().sum(-1).mean()
        inverse_loss = forward_loss.new_zeros(())
        if self.inverse_head is not None:
            online_future = self.encoder(**future)  # no detach, NOT the EMA encoder
            output = self.inverse_head(self.inverse_inputs(current), self.inverse_inputs(online_future))
            if output.shape != (batch, self.action_size) or not bool(torch.isfinite(output).all()):
                raise ValueError("inverse head must return finite [batch,action_size]")
            inverse_targets = actions if inverse_permutation is None else actions[inverse_permutation]
            inverse_loss = ((output - inverse_targets).square().sum(-1).mean()
                            if self.continuous_actions else F.cross_entropy(output, inverse_targets))
        # lambda_inv=1, shared across the five arms, as in the paper.
        return {"loss": forward_loss + inverse_loss, "forward": forward_loss, "inverse": inverse_loss}

    @torch.no_grad()
    def update_target(self) -> None:
        online = dict(self.encoder.named_parameters())
        for name, parameter in self.target_encoder.named_parameters():
            parameter.mul_(self.ema_momentum).add_(online[name], alpha=1 - self.ema_momentum)
        for target, source in zip(self.target_encoder.buffers(), self.encoder.buffers(), strict=True):
            target.copy_(source)


class _DiagnosticInverse(nn.Module):
    """Local test head, NOT a claimed author architecture."""
    def __init__(self, width: int, outputs: int):
        super().__init__()
        self.linear = nn.Linear(2 * width, outputs)

    def forward(self, current: Tensor, future: Tensor) -> Tensor:
        return self.linear(torch.cat((current, future), -1))


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Bounded generated-feature train/gradient diagnostic; no images/weights."""
    if device not in ("cpu", "cuda"):
        raise ValueError("diagnostic device must be cpu or cuda")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA unavailable; CPU fallback forbidden")
    devices = [torch.cuda.current_device()] if device == "cuda" else []
    with torch.random.fork_rng(devices=devices):
        torch.manual_seed(seed)
        generator = torch.Generator(device=device).manual_seed(seed)
        features = torch.randn(4, 4, 512, generator=generator, device=device)
        xy = torch.rand(4, 4, 2, generator=generator, device=device) * .7
        boxes = torch.cat((xy, xy + .2), -1)
        valid = torch.tensor([[1, 1, 1, 0]] * 4, device=device, dtype=torch.bool)
        kinds = torch.tensor([[0, 1, 0, 0]] * 4, device=device, dtype=torch.long)
        start = dict(features=features, boxes=boxes, entity_types=kinds, valid=valid)
        future = {**start, "features": features + .1 * torch.randn(features.shape, generator=generator, device=device),
                  "boxes": boxes + .02}
        actions = torch.arange(4, device=device)
        encoder = RelationalStateEncoder(nn.Sequential(nn.Linear(36, 128), nn.GELU(),
                                                       nn.Linear(128, 128)), nn.GELU()).to(device)
        model = InsideJEPA(encoder, arm="INV-S", action_size=4,
                           inverse_head=_DiagnosticInverse(128, 4)).to(device)
        current, later = model.encoder(**start), model.encoder(**future)
        inverse = F.cross_entropy(model.inverse_head(current.s.flatten(1), later.s.flatten(1)), actions)
        grad_current, grad_future = torch.autograd.grad(inverse, (current.s, later.s))
        before = model.losses(start, future, actions)
        old_online = [p.detach().clone() for p in model.encoder.parameters()]
        old_target = [p.detach().clone() for p in model.target_encoder.parameters()]
        optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad),
                                      lr=2e-4, weight_decay=1e-4)
        optimizer.zero_grad()
        before["loss"].backward()
        target_no_gradient = all(p.grad is None and not p.requires_grad for p in model.target_encoder.parameters())
        optimizer.step()
        after = model.losses(start, future, actions)
        model.update_target()
        ema_error = max(float((target - (.996 * old + .004 * online)).detach().abs().max())
                        for target, old, online in zip(model.target_encoder.parameters(), old_target,
                                                       model.encoder.parameters(), strict=True))
        # The shuffled control changes only inverse labels, never P's action.
        model.arm = "INV-SHUF"
        shuffled = model.losses(start, future, actions,
                                inverse_permutation=torch.tensor([1, 2, 3, 0], device=device))
        model.arm = "INV-S"
        unshuffled = model.losses(start, future, actions)
        shuffled_forward_error = float((shuffled["forward"] - unshuffled["forward"]).detach().abs())
        shuffled_inverse_gap = float((shuffled["inverse"] - unshuffled["inverse"]).detach().abs())
        arm_gradient_norms = {}
        for arm in ARMS:
            r0, r1 = torch.randn(4, 4, 32, generator=generator, device=device, requires_grad=True), torch.randn(4, 4, 32, generator=generator, device=device, requires_grad=True)
            s0, s1 = torch.rand(4, 4, 4, 8, generator=generator, device=device, requires_grad=True), torch.rand(4, 4, 4, 8, generator=generator, device=device, requires_grad=True)
            if arm == "PRED":
                arm_gradient_norms[arm] = 0.
                continue
            width = 128 if arm in ("INV-S", "INV-SHUF", "INV-R") else 256
            model.arm = arm
            head = _DiagnosticInverse(width, 4).to(device)
            targets = actions.roll(1) if arm == "INV-SHUF" else actions
            loss = F.cross_entropy(head(model.inverse_inputs(RelationalState(r0, s0)),
                                        model.inverse_inputs(RelationalState(r1, s1))), targets)
            gs = torch.autograd.grad(loss, (s0, s1), allow_unused=True)
            arm_gradient_norms[arm] = sum(float(g.norm()) for g in gs if g is not None)
        model.arm = "INV-S"
        state = model.encoder(**start)
        diagonal = torch.arange(4, device=device)
        checks = {
            "online_current_and_future_inverse_gradients": float(grad_current.norm()) > 0 and float(grad_future.norm()) > 0,
            "ema_target_is_stop_gradient": target_no_gradient,
            "ema_update_matches_0996": ema_error < 1e-6,
            "ordered_pair_padding_and_diagonal_constant": bool((state.s[:, diagonal, diagonal] == 0).all()) and bool((state.s[:, 3] == 0).all()) and bool((state.s[:, :, 3] == 0).all()),
            "four_slot_state_dimension_256": state.z.shape == (4, 256),
            "inverse_r_no_direct_channel_gradient": arm_gradient_norms["INV-R"] == 0,
            "s_z_shuf_have_channel_gradients": all(arm_gradient_norms[a] > 0 for a in ("INV-S", "INV-Z", "INV-SHUF")),
            "shuffled_inverse_keeps_true_prediction_action": shuffled_forward_error == 0 and shuffled_inverse_gap > 1e-6,
            "actual_online_optimizer_update": any(not torch.equal(a, b) for a, b in zip(old_online, model.encoder.parameters(), strict=True)),
            "finite_nonincreasing_fixture_loss": bool(torch.isfinite(after["loss"])) and float(after["loss"].detach()) < float(before["loss"].detach()),
        }
        if not all(checks.values()):
            raise RuntimeError(f"Inside-JEPA defining contract failed: {checks}")
        return {"seed": seed, "metrics": {
            "forward_loss_before": float(before["forward"].detach()),
            "inverse_loss_before": float(before["inverse"].detach()),
            "fixture_loss_before": float(before["loss"].detach()),
            "fixture_loss_after": float(after["loss"].detach()),
            "current_channel_inverse_gradient_norm": float(grad_current.norm()),
            "future_channel_inverse_gradient_norm": float(grad_future.norm()),
            "ema_max_abs_error": ema_error,
            "inv_r_direct_channel_gradient_norm": arm_gradient_norms["INV-R"],
            "inv_s_direct_channel_gradient_norm": arm_gradient_norms["INV-S"],
            "inv_z_direct_channel_gradient_norm": arm_gradient_norms["INV-Z"],
            "inv_shuf_direct_channel_gradient_norm": arm_gradient_norms["INV-SHUF"],
            "shuffled_forward_max_abs_error": shuffled_forward_error,
            "shuffled_inverse_loss_gap": shuffled_inverse_gap,
            "batch": 4, "entity_slots": 4, "crop_feature_dimension": 512,
            "state_dimension": 256, "optimizer_steps": 1}, "checks": checks}
