"""Five Oct-16 announcement algorithms, exposed as non-promotable components.

No pretrained model, benchmark, judge or environment is hidden in this module.
Callers own actual sampling, frozen-model scoring and training-only verifiers.
Paper equations are implemented independently from the bounded diagnostic runner.
"""
from __future__ import annotations

import math
from collections.abc import Sequence

import torch
from torch import Tensor


def _finite(value: Tensor, name: str) -> None:
    if not bool(torch.isfinite(value).all()):
        raise ValueError(f"{name} must be finite")


def _mask(mask: Tensor) -> None:
    if mask.ndim != 2 or mask.dtype != torch.bool or not bool(mask.any(1).all()):
        raise ValueError("mask must be bool [batch, token], with a valid token in every row")


def _logits(logits: Tensor, mask: Tensor) -> Tensor:
    _mask(mask)
    if logits.ndim != 3 or logits.shape[:2] != mask.shape or logits.shape[-1] < 2:
        raise ValueError("logits must be [batch, token, vocabulary>=2]")
    if logits.device != mask.device or not logits.is_floating_point():
        raise ValueError("logits and mask must share device and logits must be floating")
    _finite(logits[mask], "valid logits")
    # Sanitize before softmax, so masked NaN padding also has zero gradient.
    return torch.where(mask[..., None], logits, torch.zeros_like(logits)).log_softmax(-1)


def token_log_probs(logits: Tensor, labels: Tensor, mask: Tensor) -> Tensor:
    logp = _logits(logits, mask)
    if labels.shape != mask.shape or labels.dtype != torch.long or labels.device != mask.device:
        raise ValueError("labels must be long [batch, token] on the mask device")
    if bool(((labels[mask] < 0) | (labels[mask] >= logits.shape[-1])).any()):
        raise ValueError("valid labels outside vocabulary")
    chosen = logp.gather(-1, torch.where(mask, labels, 0)[..., None]).squeeze(-1)
    return torch.where(mask, chosen, 0.)


def group_advantages(rewards: Tensor, *, epsilon: float = 1e-6) -> Tensor:
    """Group-relative population normalization; axis 1 is the rollout group."""
    if rewards.ndim not in (2, 3) or rewards.shape[1] < 2 or not epsilon > 0:
        raise ValueError("rewards must be [problem, group>=2, optional reward] and epsilon>0")
    _finite(rewards, "rewards")
    values = rewards.detach()
    return (values - values.mean(1, keepdim=True)) / (values.std(1, correction=0, keepdim=True) + epsilon)


def policy_surrogate(current: Tensor, behavior: Tensor, mask: Tensor, advantages: Tensor,
                     *, clip: float = .2) -> Tensor:
    """Per-response mean clipped policy loss; all supervision is detached."""
    _mask(mask)
    if not 0 < clip < 1 or any(v.shape != mask.shape for v in (current, behavior, advantages)):
        raise ValueError("aligned token arrays and 0<clip<1 required")
    for name, value in (("current", current), ("behavior", behavior), ("advantages", advantages)):
        _finite(value[mask], name)
    current = torch.where(mask, current, 0.)
    old = torch.where(mask, behavior.detach(), 0.)
    advantage = torch.where(mask, advantages.detach(), 0.)
    ratio = (current - old).exp()
    _finite(ratio[mask], "importance ratios")
    objective = torch.minimum(ratio * advantage, ratio.clamp(1 - clip, 1 + clip) * advantage)
    return -(objective.sum(1) / mask.sum(1)).mean()


def elect_anchor(probe_logp: Tensor, base_logp: Tensor, mask: Tensor) -> tuple[int, Tensor]:
    """TAG Eq.5: pooled per-generated-token MC reverse KL under each probe.

    Inputs must be scored on trajectories sampled from each independently trained
    probe, NOT from the base. Finite-sample estimates may be negative; do not clamp
    or substitute forward KL. Probes are discarded before joint optimization.
    """
    if probe_logp.ndim != 3 or probe_logp.shape != base_logp.shape or mask.shape != probe_logp.shape:
        raise ValueError("probe/base scores and mask must be [channel, batch, token]")
    if mask.dtype != torch.bool or not bool(mask.flatten(1).any(1).all()):
        raise ValueError("every probe requires sampled valid tokens")
    _finite(probe_logp[mask], "probe scores")
    _finite(base_logp[mask], "base scores")
    ratios = torch.where(mask, probe_logp.detach() - base_logp.detach(), 0.)
    estimates = ratios.sum((1, 2)) / mask.sum((1, 2))
    return int(estimates.argmin()), estimates


def tag_reward(rewards: Tensor, anchor: int, weights: Tensor | None = None) -> Tensor:
    """TAG Eq.6, including its denominator (not an additive reward heuristic)."""
    if rewards.ndim < 2 or rewards.shape[-1] < 2 or not 0 <= anchor < rewards.shape[-1]:
        raise ValueError("at least two reward channels and a valid anchor required")
    _finite(rewards, "rewards")
    if bool(((rewards < 0) | (rewards > 1)).any()):
        raise ValueError("TAG rewards must lie in [0,1]")
    weights = torch.ones(rewards.shape[-1], device=rewards.device, dtype=rewards.dtype) if weights is None else weights
    if weights.shape != (rewards.shape[-1],) or weights.device != rewards.device:
        raise ValueError("one weight per reward channel on the reward device required")
    _finite(weights, "weights")
    if bool((weights < 0).any()):
        raise ValueError("nonnegative auxiliary weights required")
    weights = weights.detach().clone()
    weights[anchor] = 0
    return rewards[..., anchor].detach() * (1 + (rewards.detach() * weights).sum(-1)) / (1 + weights.sum())


def mrtpo_advantages(reward_advantages: Tensor, all_logits: Tensor, omitted_logits: Tensor,
                     mask: Tensor, *, beta: float = .5, step: int = 10,
                     warmup: int = 10, epsilon: float = 1e-8) -> tuple[Tensor, dict[str, Tensor]]:
    """MRTPO Eqs.5--8: leave-one-out JS, mean preservation, bound, whitening.

    all_logits come from the frozen behavior policy under *all* verifier blocks;
    omitted_logits[:,k] differ by exactly block k, on identical response prefixes.
    A zero-information/empty block falls back to uniform weights for that reward.
    """
    if not 0 <= beta < 1 or step < 0 or warmup < 1 or epsilon <= 0:
        raise ValueError("beta in [0,1), nonnegative step and positive warmup/epsilon required")
    all_logp = _logits(all_logits.detach(), mask)
    if reward_advantages.ndim != 2 or reward_advantages.shape[0] != mask.shape[0]:
        raise ValueError("reward advantages must be [batch, reward]")
    batch, channels = reward_advantages.shape
    if channels < 1 or omitted_logits.shape != (batch, channels, *all_logits.shape[1:]):
        raise ValueError("omitted logits must be [batch, reward, token, vocabulary]")
    _finite(reward_advantages, "reward advantages")
    omitted_logp = torch.stack([_logits(omitted_logits[:, k].detach(), mask) for k in range(channels)], 1)
    p, q = all_logp[:, None].exp(), omitted_logp.exp()
    mixture_log = torch.logaddexp(all_logp[:, None], omitted_logp) - math.log(2.)
    js = .5 * ((p * (all_logp[:, None] - mixture_log)).sum(-1)
               + (q * (omitted_logp - mixture_log)).sum(-1))
    relevance = (js.clamp_min(0.) / math.log(2.)).clamp_max(1.).sqrt()
    relevance = torch.where(mask[:, None], relevance, 0.)
    average = relevance.sum(-1, keepdim=True) / mask.sum(1)[:, None, None]
    normalized = torch.where(average > epsilon, relevance / average.clamp_min(epsilon), torch.ones_like(relevance))
    u = min(step / warmup, 1.)
    strength = beta * (3 * u * u - 2 * u * u * u)
    weights = torch.where(mask[:, None], 1 - strength + strength * normalized, 0.)
    advantage = reward_advantages.detach()
    uniform = advantage.sum(1)[:, None].expand_as(mask)
    assigned = (advantage[..., None] * weights).sum(1)
    realloc = torch.where(mask, assigned - uniform, 0.)
    denominator = realloc.square().sum()
    numerator = torch.where(mask, uniform.square(), 0.).sum()
    scale = torch.minimum(torch.ones_like(numerator), (numerator / denominator.clamp_min(epsilon)).sqrt())
    bounded = torch.where(mask, uniform + scale * realloc, 0.)
    std = bounded[mask].std(correction=0)
    whitened = bounded / (std + epsilon)
    return whitened.detach(), {"weights": weights, "relevance": relevance, "bounded": bounded,
                              "uniform": torch.where(mask, uniform, 0.), "bound_scale": scale, "batch_std": std}


def route_teachers(student_logits: Tensor, teacher_logits: Tensor, mask: Tensor,
                   *, criterion: str = "hellinger", temperature: float = .1,
                   student_features: Tensor | None = None,
                   teacher_features: Tensor | None = None) -> tuple[Tensor, Tensor]:
    """Token-level hard/soft routing; returns log arithmetic mixture and weights.

    Entropy uses -H(teacher), Hellinger uses -H(student,teacher), and feature
    matching uses negative squared distance (only for aligned hidden spaces).
    All teacher distributions, student routing scores, and routing weights detach.
    """
    if not math.isfinite(temperature) or temperature < 0:
        raise ValueError("finite nonnegative temperature required")
    student = _logits(student_logits.detach(), mask)
    if teacher_logits.ndim != 4 or teacher_logits.shape[1:] != student_logits.shape or teacher_logits.shape[0] < 1:
        raise ValueError("teachers must be [teacher, batch, token, vocabulary]")
    teachers = torch.stack([_logits(value.detach(), mask) for value in teacher_logits])
    if criterion == "entropy":
        scores = (teachers.exp() * teachers).sum(-1)
    elif criterion == "hellinger":
        scores = -(.5 * (teachers.exp().sqrt() - student.exp().sqrt()[None]).square().sum(-1)).clamp_min(0).sqrt()
    elif criterion == "features":
        if student_features is None or teacher_features is None:
            raise ValueError("aligned student and teacher features required")
        if student_features.shape[:2] != mask.shape or teacher_features.shape != (len(teachers), *student_features.shape):
            raise ValueError("aligned student and teacher feature shapes required")
        _finite(student_features[mask], "student features")
        _finite(teacher_features[:, mask], "teacher features")
        scores = -(teacher_features.detach() - student_features.detach()[None]).square().sum(-1)
    else:
        raise ValueError("criterion must be entropy, hellinger or features")
    scores = torch.where(mask[None], scores, 0.)
    if temperature == 0:
        indices = scores.argmax(0)
        weights = torch.nn.functional.one_hot(indices, len(teachers)).movedim(-1, 0).to(teachers)
    else:
        weights = (scores / temperature).softmax(0)
    target = torch.logsumexp(teachers + weights.clamp_min(torch.finfo(weights.dtype).tiny).log()[..., None], 0)
    return target.detach(), weights.detach()


def routed_opd_loss(student_logits: Tensor, target_logp: Tensor, labels: Tensor,
                    mask: Tensor) -> Tensor:
    """Paper Eq.35 sampled-token semi-gradient, not an undetached KL proxy."""
    student = token_log_probs(student_logits, labels, mask)
    if target_logp.shape != student_logits.shape:
        raise ValueError("target distribution must align with student")
    _finite(target_logp[mask], "target log distribution")
    chosen = target_logp.detach().gather(-1, torch.where(mask, labels, 0)[..., None]).squeeze(-1)
    advantage = torch.where(mask, chosen - student.detach(), 0.)
    return -(advantage * student).sum(1).div(mask.sum(1)).mean()


def information_gains(answer_logp: Tensor, answer_mask: Tensor, *, epsilon: float = 1e-3) -> Tensor:
    """IG-OPD Eq.3: teacher answer probes only, never actor-visible answers.

    Context axis contains initial context and context after each search result;
    append an explicit zero for the final synthesis turn at the call site.
    """
    if answer_logp.ndim != 3 or answer_mask.shape != answer_logp.shape or answer_mask.dtype != torch.bool:
        raise ValueError("answer scores/mask must be [batch, initial+search contexts, answer token]")
    if answer_logp.shape[1] < 2 or not bool(answer_mask.any(-1).all()) or epsilon <= 0:
        raise ValueError("initial and post-search probes, nonempty answers and epsilon>0 required")
    _finite(answer_logp[answer_mask], "answer probe log probabilities")
    if bool((answer_logp[answer_mask] > 0).any()):
        raise ValueError("answer log probabilities cannot be positive")
    average = torch.where(answer_mask, answer_logp.detach(), 0.).sum(-1) / answer_mask.sum(-1)
    potential = torch.logaddexp(average, torch.full_like(average, math.log(epsilon)))
    return potential[:, 1:] - potential[:, :-1]


def ig_calibrated_advantages(student_logp: Tensor, teacher_logp: Tensor, mask: Tensor,
                              turn_ids: Tensor, gains: Tensor, decision_mask: Tensor,
                              *, strength: float = .1, alpha_max: float = 10.,
                              step: int = 1, ramp_steps: int = 60,
                              epsilon: float = 1e-6) -> tuple[Tensor, dict[str, Tensor]]:
    """IG-OPD Eqs.4--9. IQC is OUTSIDE the ITC factor and formatting mask."""
    _mask(mask)
    if any(value.shape != mask.shape for value in (student_logp, teacher_logp, turn_ids, decision_mask)):
        raise ValueError("token scores, turn IDs and decision mask must align")
    if turn_ids.dtype != torch.long or decision_mask.dtype != torch.bool or bool((decision_mask & ~mask).any()):
        raise ValueError("long turn IDs and policy-only boolean decision mask required")
    if gains.ndim != 2 or gains.shape[0] != mask.shape[0] or strength < 0 or alpha_max < 0 or step < 0 or ramp_steps < 1 or epsilon <= 0:
        raise ValueError("valid batch gains and nonnegative calibration configuration required")
    for name, value in (("student", student_logp[mask]), ("teacher", teacher_logp[mask]), ("gains", gains)):
        _finite(value, name)
    if bool(((turn_ids[mask] < 0) | (turn_ids[mask] >= gains.shape[1])).any()):
        raise ValueError("valid token has invalid turn ID")
    gains = gains.detach()
    rms = gains.square().mean().sqrt().clamp_min(epsilon)
    scores = 1 + strength * torch.tanh(gains.abs() / rms)
    shares = scores / scores.sum(1, keepdim=True)
    alpha = alpha_max * .5 * (1 - math.cos(math.pi * min(step / ramp_steps, 1.)))
    base = teacher_logp.detach() - student_logp.detach()
    itc, iqc = torch.zeros_like(base), torch.zeros_like(base)
    for turn in range(gains.shape[1]):
        members = mask & (turn_ids == turn)
        counts = members.sum(1)
        if not bool((counts > 0).all()):
            raise ValueError("each row must represent every turn, including final synthesis")
        decisions = members & decision_mask
        decision_counts = decisions.sum(1)
        if bool(((decision_counts == 0) & (gains[:, turn] != 0)).any()):
            raise ValueError("nonzero information gain needs an action-critical decision token")
        factor = mask.sum(1) * shares[:, turn] / counts
        itc = itc + torch.where(members, factor[:, None] * base, 0.)
        credit = alpha * gains[:, turn] / decision_counts.clamp_min(1)
        iqc = iqc + torch.where(decisions, credit[:, None], 0.)
    return (itc + iqc).detach(), {"itc": itc, "iqc": iqc, "turn_shares": shares,
                                "alpha": torch.as_tensor(alpha, dtype=gains.dtype, device=gains.device)}


def note_has_answer(note_tokens: Sequence[int], reference_tokens: Sequence[int]) -> bool:
    """Exact subsequence leak screen for token diagnostics, NOT semantic safety.

    Natural-language RSHD additionally needs its semantic/malformed-note screen.
    The reference is supplied to this training-only screen, never to the writer.
    """
    if not reference_tokens:
        raise ValueError("nonempty reference answer required")
    note, answer = tuple(note_tokens), tuple(reference_tokens)
    return any(note[i:i + len(answer)] == answer for i in range(len(note) - len(answer) + 1))


def admit_note(original_rewards: Sequence[float], replay_rewards: Sequence[float],
                *, valid: bool, leaks_answer: bool) -> bool:
    """Strict fresh-replay improvement over the SAME original group, Alg.1."""
    if not original_rewards or not replay_rewards:
        raise ValueError("original group and fresh replay outcomes required")
    if any(value not in (0, 1) for value in (*original_rewards, *replay_rewards)):
        raise ValueError("binary verifier outcomes required")
    return (valid and not leaks_answer
            and sum(replay_rewards) / len(replay_rewards) > sum(original_rewards) / len(original_rewards))


def rshd_aux_loss(plain_logits: Tensor, note_logits: Tensor, labels: Tensor,
                  mask: Tensor, admitted: Tensor, *, cap: float = 2.) -> tuple[Tensor, Tensor]:
    """RSHD Eq.4: all tokens of admitted replays, including zero-lift tokens."""
    if admitted.shape != (mask.shape[0],) or admitted.dtype != torch.bool or not math.isfinite(cap) or cap <= 0:
        raise ValueError("boolean per-replay admission and positive finite cap required")
    student = token_log_probs(plain_logits, labels, mask)
    teacher = token_log_probs(note_logits.detach(), labels, mask)
    active = mask & admitted[:, None]
    weights = torch.where(active, (teacher - student.detach()).clamp(0, cap), 0.).detach()
    return -(weights * student).sum() / active.sum().clamp_min(1), weights
