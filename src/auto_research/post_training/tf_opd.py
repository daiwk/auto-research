"""TF-OPD (2610.22236v1), independently implemented from Eqs. 1--4.

The statistics API generates with each teacher, filters before replay, and never
accepts an arbitrary covariance as evidence of end-to-end distillation. Solving
an explicitly supplied Gram remains useful as a numerical operator (L0 only).
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, Iterable
import zlib

import torch
from torch import Tensor, nn


@dataclass(frozen=True)
class TeacherRollout:
    tokens: Tensor
    prompt_length: int
    teacher_id: str
    terminated: bool
    response_text: str
    correct: bool | None = None


@torch.no_grad()
def sample_teacher_rollout(
    teacher: nn.Module, prompt: Tensor, *, teacher_id: str, eos_token_id: int,
    max_new_tokens: int, decode: Callable[[list[int]], str],
    generator: torch.Generator | None = None,
) -> TeacherRollout:
    """Real autoregressive teacher sampling; no reference solution enters here."""
    if prompt.ndim != 2 or prompt.shape[0] != 1 or not prompt.numel():
        raise ValueError("one nonempty prompt is required")
    if max_new_tokens < 1 or not teacher_id:
        raise ValueError("positive rollout budget and teacher identity required")
    previous = teacher.training
    teacher.eval()
    ids, ended = prompt.clone(), False
    try:
        for _ in range(max_new_tokens):
            token = torch.multinomial(teacher(ids)[:, -1].softmax(-1), 1, generator=generator)
            ids = torch.cat((ids, token), -1)
            if int(token.item()) == eos_token_id:
                ended = True
                break
    finally:
        teacher.train(previous)
    response = ids[0, prompt.shape[1]:].tolist()
    return TeacherRollout(ids.detach(), prompt.shape[1], teacher_id, ended, decode(response))


def retain_rollout(rollout: TeacherRollout, *, require_correct: bool = False,
                   loop_threshold: float = .05, tail_characters: int = 20_000) -> bool:
    """Natural EOS and DEFLATE loop filter (§3.4); optional external grading."""
    if not 0 < loop_threshold < 1 or tail_characters < 1:
        raise ValueError("invalid loop filter")
    if not rollout.terminated or (require_correct and rollout.correct is not True):
        return False
    tail = rollout.response_text[-tail_characters:].encode("utf-8")
    looping = bool(tail) and len(zlib.compress(tail)) / len(tail) < loop_threshold
    return not looping


@torch.no_grad()
def collect_teacher_grams(teacher: nn.Module, rollouts: Iterable[TeacherRollout], *,
                          teacher_id: str, require_correct: bool = False) -> tuple[dict, dict]:
    """Replay kept *own* sequences and collect token-normalized linear-input Grams.

    All positions of prompt and answer contribute, without padding. Shared-input
    linears yield identical Grams; a caller may deduplicate them for large models.
    Hooks are always removed, including on an exception.
    """
    linears = {name: layer for name, layer in teacher.named_modules() if isinstance(layer, nn.Linear)}
    if not linears:
        raise ValueError("teacher has no supported linear maps")
    sums, counts, handles = {}, {}, []

    def record(name, _module, inputs):
        x = inputs[0].detach().reshape(-1, inputs[0].shape[-1]).float()
        sums[name] = sums.get(name, torch.zeros(x.shape[-1], x.shape[-1], device=x.device)) + x.T @ x
        counts[name] = counts.get(name, 0) + x.shape[0]

    previous, kept, seen = teacher.training, 0, 0
    teacher.eval()
    try:
        for name, layer in linears.items():
            handles.append(layer.register_forward_pre_hook(lambda m, x, name=name: record(name, m, x)))
        for rollout in rollouts:
            seen += 1
            if rollout.teacher_id != teacher_id:
                raise ValueError("teacher statistics must replay that teacher's own rollouts")
            if not retain_rollout(rollout, require_correct=require_correct):
                continue
            if rollout.tokens.ndim != 2 or rollout.tokens.shape[0] != 1:
                raise ValueError("unpadded single-sequence replay required")
            teacher(rollout.tokens)
            kept += 1
    finally:
        for handle in handles:
            handle.remove()
        teacher.train(previous)
    if not kept:
        raise ValueError("no naturally terminated, loop-free teacher rollouts remain")
    return {name: sums[name] / counts[name] for name in linears}, {
        "seen_rollouts": seen, "kept_rollouts": kept, "layer_token_counts": counts,
        "source": "teacher_self_generated_then_teacher_forced", "correctness_filter": require_correct,
    }


@torch.no_grad()
def solve_layer(base: Tensor, teacher_weights: list[Tensor], grams: list[Tensor], *,
                weights: list[float] | None = None, alpha: float = .9,
                allow_pseudoinverse: bool = False) -> tuple[Tensor, dict]:
    """Double-precision shrink-and-solve, not inverse materialization or SGD."""
    if base.ndim != 2 or not teacher_weights or len(teacher_weights) != len(grams):
        raise ValueError("a base matrix and matching teacher matrices/Grams are required")
    weights = [1.] * len(grams) if weights is None else weights
    if len(weights) != len(grams) or any(w <= 0 for w in weights) or not 0 <= alpha <= 1:
        raise ValueError("positive domain weights and alpha in [0,1] required")
    b = base.detach().double()
    shifted, deltas = [], []
    for weight, teacher, gram in zip(weights, teacher_weights, grams, strict=True):
        if teacher.shape != base.shape or gram.shape != (base.shape[1], base.shape[1]):
            raise ValueError("incompatible teacher or Gram shape")
        g = gram.detach().to(device=base.device, dtype=torch.float64)
        if not torch.isfinite(g).all() or not torch.allclose(g, g.T, atol=1e-7, rtol=1e-5):
            raise ValueError("finite symmetric second moment required")
        if torch.linalg.eigvalsh(g).min() < -1e-6:
            raise ValueError("second moment must be positive semidefinite")
        shifted.append(weight * (alpha * g + (1 - alpha) * torch.diag_embed(g.diagonal())))
        deltas.append(teacher.detach().to(b) - b)
    system = torch.stack(shifted).sum(0)
    rhs = torch.stack([d @ g for d, g in zip(deltas, shifted, strict=True)]).sum(0)
    if allow_pseudoinverse:
        update = rhs @ torch.linalg.pinv(system, hermitian=True)
    else:
        update = torch.linalg.solve(system.T, rhs.T).T
    shares = []
    for delta, gram in zip(deltas, shifted, strict=True):
        residual = update - delta
        numerator = torch.sum((residual @ gram) * residual)
        denominator = torch.sum((delta @ gram) * delta)
        shares.append(float(numerator / denominator) if denominator > 0 else (0. if numerator == 0 else None))
    normal_equation_error = float(torch.linalg.norm(update @ system - rhs))
    return (b + update).float(), {"unreproduced_share": shares,
        "normal_equation_residual_l2": normal_equation_error, "solve_dtype": "float64",
        "storage_dtype": "float32", "pseudoinverse": allow_pseudoinverse}


@torch.no_grad()
def fuse_models(base: nn.Module, teachers: list[nn.Module], grams: list[dict], *,
                alpha: float = .9, weights: list[float] | None = None) -> tuple[nn.Module, dict]:
    """Fuse all supported linear weights; task-arithmetic all remaining tensors."""
    if not teachers or len(teachers) != len(grams):
        raise ValueError("one statistics dictionary per same-architecture teacher required")
    fused = deepcopy(base).float()
    base_state, teacher_states = base.state_dict(), [t.state_dict() for t in teachers]
    if any(set(s) != set(base_state) for s in teacher_states):
        raise ValueError("teachers must share architecture with base")
    linear_keys = {f"{name}.weight" if name else "weight": name
                   for name, layer in base.named_modules() if isinstance(layer, nn.Linear)}
    state, diagnostics = {}, {}
    for key, value in base_state.items():
        if key in linear_keys:
            name = linear_keys[key]
            state[key], diagnostics[name] = solve_layer(value, [s[key] for s in teacher_states],
                [g[name] for g in grams], weights=weights, alpha=alpha)
        elif value.is_floating_point():
            state[key] = value.float() + sum(s[key].float() - value.float() for s in teacher_states)
        elif all(torch.equal(s[key], value) for s in teacher_states):
            state[key] = value.clone()
        else:
            raise ValueError("nonfloating buffers must agree")
    fused.load_state_dict(state)
    return fused, diagnostics
