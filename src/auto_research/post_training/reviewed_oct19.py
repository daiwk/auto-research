"""Bounded KnowGPO credit and DIVERGE reward/evaluation protocol components.

These APIs never provide an LLM verifier, scientific-impact judge, or search
agent. Verifier/judge observations remain explicit training/evaluation inputs.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
import itertools
import math

import torch
from torch import Tensor


def accumulate_knowledge(increments: Tensor, valid_steps: Tensor) -> tuple[Tensor, Tensor]:
    """Return BEFORE and AFTER state for each step using monotone Boolean OR."""
    if increments.ndim != 3 or increments.dtype != torch.bool or increments.shape[-1] < 1:
        raise ValueError("Boolean [rollout, step, atomic condition] increments required")
    if valid_steps.shape != increments.shape[:2] or valid_steps.dtype != torch.bool:
        raise ValueError("Boolean valid-step mask must align")
    if not bool(valid_steps.any(1).all()):
        raise ValueError("each rollout must contain a valid step")
    if bool((increments & ~valid_steps[..., None]).any()):
        raise ValueError("padding cannot acquire knowledge")
    current = torch.zeros_like(increments[:, 0])
    before, after = [], []
    for turn in range(increments.shape[1]):
        before.append(current.clone())
        current = current | increments[:, turn]
        after.append(current.clone())
    return torch.stack(before, 1), torch.stack(after, 1)


def knowledge_advantages(query_ids: Sequence[str], before: Tensor, after: Tensor,
                         valid_steps: Tensor, answer_steps: Tensor, outcomes: Tensor,
                         *, omega: float = .5, epsilon: float = 1e-6
                         ) -> tuple[Tensor, dict]:
    """KnowGPO Algorithm 1: group by (query, BEFORE state), excluding answer.

    The main-text Eq.5 has an indexing ambiguity. Algorithm 1 and the authors'
    README explicitly use s[t-1]; using the AFTER state would change the method.
    Singleton/constant groups have zero process advantage. Outcomes and all
    verifier-derived state/credit are detached and are not actor observations.
    """
    if before.shape != after.shape or before.ndim != 3 or before.dtype != torch.bool or after.dtype != torch.bool:
        raise ValueError("aligned Boolean before/after knowledge states required")
    shape = before.shape[:2]
    if valid_steps.shape != shape or answer_steps.shape != shape or valid_steps.dtype != torch.bool or answer_steps.dtype != torch.bool:
        raise ValueError("aligned Boolean valid/answer step masks required")
    if bool((answer_steps & ~valid_steps).any()):
        raise ValueError("an answer cannot be a padding step")
    if len(query_ids) != shape[0] or any(not isinstance(q, str) or not q for q in query_ids):
        raise ValueError("nonempty query IDs must align with rollouts")
    if outcomes.shape != (shape[0],) or not outcomes.is_floating_point() or not torch.isfinite(outcomes).all():
        raise ValueError("finite floating rollout outcomes required")
    if not 0 <= omega <= 1 or epsilon <= 0 or not math.isfinite(omega + epsilon):
        raise ValueError("omega in [0,1] and finite epsilon>0 required")
    if not bool(valid_steps.any(1).all()) or bool((before & ~after & valid_steps[..., None]).any()):
        raise ValueError("valid steps and monotone knowledge required")
    # Validate that states really form one trajectory rather than accepting an
    # arbitrary grouping label that silently resets acquired conditions.
    for row in range(shape[0]):
        previous = torch.zeros_like(before[row, 0])
        for turn in range(shape[1]):
            if valid_steps[row, turn]:
                if not torch.equal(before[row, turn], previous):
                    raise ValueError("before-state must match preceding accumulated knowledge")
                previous = after[row, turn]
    if bool(((after != before).any(-1) & answer_steps).any()):
        raise ValueError("terminal answer steps cannot introduce search knowledge")
    episode = torch.zeros_like(outcomes)
    for query in dict.fromkeys(query_ids):
        ids = [i for i, q in enumerate(query_ids) if q == query]
        reward = outcomes.detach()[ids]
        episode[ids] = (reward - reward.mean()) / (reward.std(correction=0) + epsilon)
    gains = (after.to(outcomes.dtype) - before.to(outcomes.dtype)).sum(-1)
    process = torch.zeros_like(gains)
    groups: dict[tuple[str, tuple[bool, ...]], list[tuple[int, int]]] = {}
    for row, query in enumerate(query_ids):
        for turn in range(shape[1]):
            if valid_steps[row, turn] and not answer_steps[row, turn]:
                key = query, tuple(before[row, turn].tolist())
                groups.setdefault(key, []).append((row, turn))
    records = []
    for (query, state), positions in groups.items():
        values = torch.stack([gains[row, turn] for row, turn in positions])
        normalized = (values - values.mean()) / (values.std(correction=0) + epsilon)
        for position, value in zip(positions, normalized, strict=True):
            process[position] = value
        records.append({"query_id": query, "before_state": list(state), "positions": [list(p) for p in positions],
                        "gains": values.tolist(), "advantages": normalized.tolist()})
    combined = (1 - omega) * episode[:, None] + omega * process
    combined = torch.where(valid_steps, combined, 0.).detach()
    return combined, {"groups": records, "episode_advantages": episode.detach(),
        "step_advantages": process.detach(), "incremental_gains": gains.detach()}


def broadcast_step_advantages(step_advantages: Tensor, token_step_ids: Tensor,
                               generated_mask: Tensor) -> Tensor:
    """Broadcast only onto generated reasoning/action tokens; never observations."""
    if step_advantages.ndim != 2 or token_step_ids.ndim != 2 or token_step_ids.shape != generated_mask.shape:
        raise ValueError("step advantages and aligned token-step IDs/mask required")
    if token_step_ids.shape[0] != step_advantages.shape[0] or token_step_ids.dtype != torch.long or generated_mask.dtype != torch.bool:
        raise ValueError("long token-step IDs and Boolean generated mask required")
    if not torch.isfinite(step_advantages).all():
        raise ValueError("finite step credit required")
    selected = token_step_ids[generated_mask]
    if bool(((selected < 0) | (selected >= step_advantages.shape[1])).any()):
        raise ValueError("generated token references invalid step")
    safe_ids = torch.where(generated_mask, token_step_ids, 0)
    result = step_advantages.detach().gather(1, safe_ids)
    return torch.where(generated_mask, result, 0.)


def knowgpo_policy_loss(current_logits: Tensor, behavior_logits: Tensor,
                        reference_logits: Tensor, labels: Tensor, generated_mask: Tensor,
                        advantages: Tensor, *, clip: float = .2, kl_coefficient: float = .01
                        ) -> tuple[Tensor, dict[str, Tensor]]:
    """Clipped surrogate + actual full-vocabulary reverse KL, valid token mean."""
    if current_logits.ndim != 3 or any(x.shape != current_logits.shape for x in (behavior_logits, reference_logits)):
        raise ValueError("current/behavior/reference logits must align [batch,token,vocab]")
    shape = current_logits.shape[:2]
    if any(x.shape != shape for x in (labels, generated_mask, advantages)) or labels.dtype != torch.long or generated_mask.dtype != torch.bool:
        raise ValueError("aligned long labels, Boolean generated mask and credit required")
    if not generated_mask.any() or not 0 < clip < 1 or kl_coefficient < 0 or not math.isfinite(kl_coefficient):
        raise ValueError("generated tokens, valid clip and nonnegative finite KL coefficient required")
    if bool(((labels[generated_mask] < 0) | (labels[generated_mask] >= current_logits.shape[-1])).any()):
        raise ValueError("generated labels outside vocabulary")
    logs = []
    for index, values in enumerate((current_logits, behavior_logits.detach(), reference_logits.detach())):
        if not torch.isfinite(values[generated_mask]).all():
            raise ValueError("finite valid logits required")
        clean = torch.where(generated_mask[..., None], values, torch.zeros_like(values))
        logs.append(clean.log_softmax(-1))
        if index and logs[-1].requires_grad:
            raise RuntimeError("frozen supervision acquired gradient")
    if not torch.isfinite(advantages[generated_mask]).all():
        raise ValueError("finite valid advantages required")
    ids = torch.where(generated_mask, labels, 0)[..., None]
    chosen, old = (value.gather(-1, ids).squeeze(-1) for value in logs[:2])
    ratio = (chosen - old).exp()
    if not torch.isfinite(ratio[generated_mask]).all():
        raise ValueError("importance ratio overflow")
    advantage = torch.where(generated_mask, advantages.detach(), 0.)
    clipped = torch.minimum(ratio * advantage, ratio.clamp(1 - clip, 1 + clip) * advantage)
    kl = (logs[0].exp() * (logs[0] - logs[2])).sum(-1)
    pg = -clipped[generated_mask].mean()
    penalty = kl[generated_mask].mean()
    return pg + kl_coefficient * penalty, {"policy_loss": pg.detach(), "reverse_kl": penalty.detach()}


IDEA_FIELDS = ("problem_gap", "core_claim", "method", "inspiration")


def validate_idea_schema(cards: Sequence[Mapping[str, str]], *, expected_count: int,
                          has_think_block: bool, has_answer_block: bool,
                          problem_label_valid: Callable[[str], bool],
                          method_label_valid: Callable[[str], bool]) -> bool:
    """Structural card gate. Caller supplies the paper's taxonomy validators.

    This is not a semantic grounding check or a raw-text/XML/JSON parser.
    Empty think blocks are valid for the no-think arm; their presence is required.
    """
    if expected_count < 1 or not has_think_block or not has_answer_block or len(cards) != expected_count:
        return False
    for card in cards:
        if any(not isinstance(card.get(field), str) or not card[field].strip() for field in IDEA_FIELDS):
            return False
        if not problem_label_valid(card["problem_gap"]) or not method_label_valid(card["method"]):
            return False
    return True


def _validate_observations(quality: Sequence[float], distances: Sequence[Sequence[float]]) -> None:
    size = len(quality)
    if size < 1 or len(distances) != size or any(len(row) != size for row in distances):
        raise ValueError("nonempty quality vector and square distance observations required")
    if any(not math.isfinite(v) or not 0 <= v <= 1 for v in quality):
        raise ValueError("quality observations must be finite in [0,1]")
    for i in range(size):
        for j in range(size):
            value = distances[i][j]
            if not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError("distance observations must be finite in [0,1]")
            if (i == j and value != 0) or abs(value - distances[j][i]) > 1e-12:
                raise ValueError("symmetric distances with zero diagonal required")


def set_reward(quality: Sequence[float], distances: Sequence[Sequence[float]], *,
                schema_valid: bool, judged_token_length: int, target_length: int = 1000,
                tolerance: float = 0., slope: float = 1., cap: float = 3., bonus: float = .05
                ) -> dict[str, float | list[float]]:
    """DIVERGE Eqs.2,6,7: generation order, nearest predecessor, no discount.

    Quality/distance are explicit observations, never fabricated by string
    similarity. Length covers ONLY gap/claim/method, not inspiration or thought.
    """
    if type(judged_token_length) is not int or judged_token_length < 0 or target_length < 1:
        raise ValueError("nonnegative judged token count and positive target required")
    if any(not math.isfinite(v) or v < 0 for v in (tolerance, slope, cap, bonus)):
        raise ValueError("finite nonnegative reward configuration required")
    if not schema_valid:
        return {"reward": 0., "set_score": 0., "length_penalty": 0., "marginals": []}
    _validate_observations(quality, distances)
    marginals = [q * (min(distances[i][:i]) if i else 1.) for i, q in enumerate(quality)]
    penalty = slope * min(max(0., judged_token_length / target_length - (1 + tolerance)), cap)
    score = sum(marginals)
    return {"reward": bonus + score - penalty, "set_score": score,
            "length_penalty": penalty, "marginals": marginals}


def observe_idea_judgments(cards: Sequence[Mapping[str, str]], *, schema_valid: bool,
                           impact_judge: Callable[[Mapping[str, str], bool], bool],
                           field_distance_judge: Callable[[Mapping[str, str], Mapping[str, str]], Sequence[float]]
                           ) -> tuple[list[float], list[list[float]]]:
    """Judge interface only: double-order impact vote and three-field distance.

    impact_judge(card, reverse) returns whether the generated card wins against
    the held-out gold idea in that ordering. Gold belongs to the judge closure,
    not the generator. No judge is called for an invalid schema. No API/model
    implementation is bundled and no capability is inferred from test callbacks.
    """
    if not schema_valid:
        return [], []
    quality = []
    for card in cards:
        votes = [impact_judge(card, reverse) for reverse in (False, True)]
        if any(type(value) is not bool for value in votes):
            raise ValueError("impact judge must return a Boolean generated-idea win")
        quality.append(sum(votes) / 2)
    distance = [[0.] * len(cards) for _ in cards]
    for i in range(len(cards)):
        for j in range(i):
            fields = field_distance_judge(cards[i], cards[j])
            if len(fields) != 3 or any(not math.isfinite(v) or not 0 <= v <= 1 for v in fields):
                raise ValueError("three normalized semantic field-distance observations required")
            distance[i][j] = distance[j][i] = sum(fields) / 3
    _validate_observations(quality, distance)
    return quality, distance


def _utility_order(quality: Sequence[float], distances: Sequence[Sequence[float]],
                    order: Sequence[int], gamma: float) -> float:
    values = [gamma ** position * quality[index]
              * (min(distances[index][other] for other in order[:position]) if position else 1.)
              for position, index in enumerate(order)]
    return sum(values) / sum(gamma ** position for position in range(len(order)))


def creative_utility(quality: Sequence[float], distances: Sequence[Sequence[float]],
                      *, gamma: float = .9, exact: bool = False) -> tuple[float, tuple[int, ...]]:
    """Greedy reporting is a LOWER BOUND; exact enumeration is bounded to K<=8."""
    _validate_observations(quality, distances)
    if not math.isfinite(gamma) or not 0 < gamma <= 1:
        raise ValueError("finite gamma in (0,1] required")
    if exact:
        if len(quality) > 8:
            raise ValueError("exact enumeration is limited to eight ideas")
        orders = itertools.permutations(range(len(quality)))
        order = max(orders, key=lambda order: _utility_order(quality, distances, order, gamma))
    else:
        order_list: list[int] = []
        pending = set(range(len(quality)))
        while pending:
            next_idea = max(sorted(pending), key=lambda i: quality[i]
                * (min(distances[i][j] for j in order_list) if order_list else 1.))
            order_list.append(next_idea)
            pending.remove(next_idea)
        order = tuple(order_list)
    return _utility_order(quality, distances, order, gamma), tuple(order)
