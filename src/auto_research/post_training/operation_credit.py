"""OpCredit (2610.21345v1), Eqs. 1--12: operation-level training credit.

No KGQA agent or Freebase benchmark is impersonated here. Gold neighborhoods
are confined to post-rollout credit functions and never enter policy input.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Mapping

import torch
from torch import Tensor

PHASES = frozenset(("entity_direction", "relation", "answer"))
RolloutKey = tuple[str, str]


@dataclass(frozen=True)
class VisibleKGState:
    question: str
    active_entity: str
    visited_entities: frozenset[str]
    remaining_budget: int
    phase: str
    visible_entities: tuple[str, ...] = ()

    def __post_init__(self):
        if (not self.question or not self.active_entity or not isinstance(self.remaining_budget, int)
                or self.remaining_budget < 0 or self.phase not in PHASES):
            raise ValueError("question/entity, nonnegative budget and known decision phase required")
        if not isinstance(self.visited_entities, frozenset):
            raise ValueError("visited entity IDs must form a frozen set")
        if any(not isinstance(e, str) or not e for e in self.visited_entities | frozenset(self.visible_entities)):
            raise ValueError("visible entities must have nonempty string IDs")

    def policy_observation(self) -> dict:
        """Whitelisted actor-visible data; there is deliberately no gold argument."""
        result = asdict(self)
        result["visited_entities"] = sorted(self.visited_entities)
        return result


@dataclass(frozen=True)
class OperationRecord:
    trajectory_id: str
    state: VisibleKGState
    operation: str
    token_indices: tuple[int, ...]
    before_frontier: tuple[str | None, ...] | None = None
    after_frontier: tuple[str | None, ...] | None = None

    def __post_init__(self):
        if not self.trajectory_id or not self.operation or not self.token_indices:
            raise ValueError("trajectory, operation and generated decision span required")
        if len(set(self.token_indices)) != len(self.token_indices) or any(not isinstance(i, int) or i < 0 for i in self.token_indices):
            raise ValueError("decision token positions must be unique and nonnegative")

    @property
    def rollout_key(self) -> RolloutKey:
        return self.state.question, self.trajectory_id

    @property
    def context_key(self) -> tuple:
        s = self.state
        return (s.question, s.active_entity, s.visited_entities, s.remaining_budget, s.phase)


@dataclass(frozen=True)
class TrainingNeighborhood:
    gold_answers: frozenset[str]
    one_hop_neighbors: frozenset[str]

    def __post_init__(self):
        if any(not isinstance(s, frozenset) for s in (self.gold_answers, self.one_hop_neighbors)):
            raise ValueError("training-only answer and neighbor IDs must form frozen sets")
        if any(not isinstance(entity, str) or not entity for entity in self.gold_answers | self.one_hop_neighbors):
            raise ValueError("training-only entity IDs must be nonempty strings")


def branch_outcome_credit(records: list[OperationRecord], rewards: Mapping[RolloutKey, float],
                           *, epsilon: float = 1e-6, std_correction: int = 0,
                           device: str | torch.device = "cpu",
                           dtype: torch.dtype = torch.float64) -> tuple[Tensor, dict]:
    """Context/operation support sets contain *unique trajectory indices*.

    Sigma is computed across all same-question rollouts, not just a context.
    Eq.1 leaves the std convention implicit; this API exposes it (default:
    population std). Zero local contrast falls back to trajectory advantage.
    """
    if not records or not rewards or not math.isfinite(epsilon) or epsilon <= 0 or std_correction not in (0, 1):
        raise ValueError("records, rewards, positive epsilon and std correction 0/1 required")
    if not dtype.is_floating_point:
        raise ValueError("credits require a floating-point dtype")
    if any(not math.isfinite(float(v)) for v in rewards.values()):
        raise ValueError("terminal rewards must be finite")
    if any(record.rollout_key not in rewards for record in records):
        raise ValueError("every recorded trajectory needs its terminal reward")
    groups: dict[str, list[float]] = {}
    for (question, trajectory), reward in rewards.items():
        if not question or not trajectory:
            raise ValueError("nonempty question and trajectory IDs required")
        groups.setdefault(question, []).append(float(reward))
    stats = {}
    for question, values in groups.items():
        if len(values) <= std_correction:
            raise ValueError("insufficient same-question rollouts for std convention")
        mean = sum(values) / len(values)
        std = math.sqrt(sum((x - mean) ** 2 for x in values) / (len(values) - std_correction))
        stats[question] = mean, std
    context_support, operation_support = {}, {}
    for record in records:
        context_support.setdefault(record.context_key, set()).add(record.rollout_key)
        operation_support.setdefault((record.context_key, record.operation), set()).add(record.rollout_key)
    credits, fallback = [], 0
    for record in records:
        keys = context_support[record.context_key]
        op_keys = operation_support[(record.context_key, record.operation)]
        q = sum(float(rewards[k]) for k in op_keys) / len(op_keys)
        v = sum(float(rewards[k]) for k in keys) / len(keys)
        mean, std = stats[record.state.question]
        difference = q - v
        fallback += difference == 0
        value = difference if difference != 0 else float(rewards[record.rollout_key]) - mean
        credits.append(value / (std + epsilon))
    result = torch.tensor(credits, device=device, dtype=dtype)
    if not torch.isfinite(result).all():
        raise ValueError("credits are not representable in requested dtype")
    return result, {
        "context_support_sizes": [len(context_support[r.context_key]) for r in records],
        "operation_support_sizes": [len(operation_support[(r.context_key, r.operation)]) for r in records],
        "fallback_decisions": fallback, "std_correction": std_correction}


def frontier_transition_credit(record: OperationRecord,
                                neighborhood: TrainingNeighborhood) -> tuple[float, bool]:
    """Appendix D.2: unavailable/empty/unresolved frontiers suppress only FTC."""
    before, after = record.before_frontier, record.after_frontier
    if not neighborhood.gold_answers or not before or not after or any(e is None or e == "" for e in before + after):
        return 0., False

    def potential(frontier):
        return max(2 if e in neighborhood.gold_answers else 1 if e in neighborhood.one_hop_neighbors else 0
                   for e in frontier)

    return float(potential(after) - potential(before)), True


def align_decision_credits(records: list[OperationRecord], rollout_keys: list[RolloutKey],
                           generated_mask: Tensor, boc: Tensor, ftc: Tensor) -> tuple[Tensor, Tensor]:
    """Decision spans must exactly partition generated tokens, excluding tools."""
    if generated_mask.ndim != 2 or generated_mask.dtype != torch.bool or not generated_mask.any(-1).all():
        raise ValueError("nonempty generated-token mask per trajectory required")
    if len(rollout_keys) != generated_mask.shape[0] or len(set(rollout_keys)) != len(rollout_keys):
        raise ValueError("one unique rollout key per mask row required")
    if boc.shape != (len(records),) or ftc.shape != boc.shape or not torch.isfinite(boc).all() or not torch.isfinite(ftc).all():
        raise ValueError("one finite BOC and FTC value per decision required")
    rows = {key: i for i, key in enumerate(rollout_keys)}
    outcome = torch.zeros_like(generated_mask, dtype=boc.dtype)
    transition = torch.zeros_like(outcome)
    coverage = torch.zeros_like(generated_mask, dtype=torch.int64)
    for i, record in enumerate(records):
        if record.rollout_key not in rows:
            raise ValueError("decision refers to an unknown rollout")
        row = rows[record.rollout_key]
        for token in record.token_indices:
            if token >= generated_mask.shape[1] or not generated_mask[row, token] or coverage[row, token]:
                raise ValueError("decision spans overlap or include observation/padding/out-of-range tokens")
            outcome[row, token] = boc[i].detach()
            transition[row, token] = ftc[i].detach()
            coverage[row, token] += 1
    if not torch.equal(coverage, generated_mask.long()):
        raise ValueError("decision spans must cover every generated token exactly once")
    return outcome.detach(), transition.detach()


def operation_policy_loss(current_logits: Tensor, old_logits: Tensor, reference_logits: Tensor,
                           labels: Tensor, generated_mask: Tensor, boc: Tensor, ftc: Tensor,
                           *, clip_ratio: float = .2, dual_clip: float = 3., auxiliary_weight: float = .1,
                           kl_weight: float = .002, entropy_weight: float = .001) -> tuple[Tensor, dict[str, Tensor]]:
    """Dual-clipped BOC + signed FTC likelihood + exact categorical KL/entropy.

    Each term is token-mean within a trajectory then trajectory-mean. The paper
    specifies KL regularization but not its estimator; full-vocabulary exact
    KL(p_current || p_frozen_SFT) is used here, without a sampled-KL proxy.
    Old policy, SFT reference, and collected credits are always stop-gradient.
    """
    if current_logits.ndim != 3 or old_logits.shape != current_logits.shape or reference_logits.shape != current_logits.shape:
        raise ValueError("matching (B,T,V) current/old/frozen-reference logits required")
    shape = current_logits.shape[:-1]
    if generated_mask.shape != shape or generated_mask.dtype != torch.bool or not generated_mask.any(-1).all():
        raise ValueError("nonempty boolean generated-token mask per trajectory required")
    if labels.shape != shape or labels.dtype != torch.long or boc.shape != shape or ftc.shape != shape:
        raise ValueError("matching long labels and token-aligned BOC/FTC required")
    constants = (clip_ratio, dual_clip, auxiliary_weight, kl_weight, entropy_weight)
    if not all(math.isfinite(v) for v in constants) or not 0 < clip_ratio < 1 or dual_clip <= 1 or min(constants[2:]) < 0:
        raise ValueError("invalid clipping or nonnegative objective weights")
    if ((labels[generated_mask] < 0) | (labels[generated_mask] >= current_logits.shape[-1])).any():
        raise ValueError("valid token label outside vocabulary")
    cleaned = []
    for logits in (current_logits, old_logits.detach(), reference_logits.detach()):
        if not logits.is_floating_point() or not torch.isfinite(logits[generated_mask]).all():
            raise ValueError("finite floating-point valid logits required")
        cleaned.append(logits.masked_fill(~generated_mask.unsqueeze(-1), 0).log_softmax(-1))
    advantages = []
    for credit in (boc.detach(), ftc.detach()):
        if not torch.isfinite(credit[generated_mask]).all():
            raise ValueError("finite valid credits required")
        advantages.append(credit.masked_fill(~generated_mask, 0))
    outcome, transition = advantages
    logp, old_logp, reference_logp = cleaned
    token_ids = labels.masked_fill(~generated_mask, 0).unsqueeze(-1)
    chosen = logp.gather(-1, token_ids).squeeze(-1)
    log_ratio = chosen - old_logp.gather(-1, token_ids).squeeze(-1)
    if (log_ratio[generated_mask] > math.log(torch.finfo(log_ratio.dtype).max) - 1).any():
        raise ValueError("policy ratio must have a representable exponential")
    ratio = log_ratio.exp()
    surrogate = torch.minimum(ratio * outcome, ratio.clamp(1 - clip_ratio, 1 + clip_ratio) * outcome)
    dual = torch.where(outcome < 0, torch.maximum(surrogate, dual_clip * outcome), surrogate)

    def mean_trajectories(values):
        return (values.masked_fill(~generated_mask, 0).sum(-1) / generated_mask.sum(-1)).mean()

    policy = -mean_trajectories(dual)
    progress = -mean_trajectories(transition * chosen)
    kl = mean_trajectories((logp.exp() * (logp - reference_logp)).sum(-1))
    entropy = -mean_trajectories((logp.exp() * logp).sum(-1))
    total = policy + auxiliary_weight * progress + kl_weight * kl - entropy_weight * entropy
    if not torch.isfinite(total):
        raise ValueError("nonfinite joint objective")
    return total, {"boc_loss": policy.detach(), "ftc_loss": progress.detach(),
                   "reference_kl": kl.detach(), "entropy": entropy.detach()}
