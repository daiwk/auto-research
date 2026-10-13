"""State-OPD interaction state, response allocation and Appendix D.1 loss."""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
from typing import Any, Callable, Protocol

import torch


@dataclass(frozen=True)
class Transition:
    action: dict
    observation: str


@dataclass(frozen=True)
class InteractionState:
    goal: str
    initial_observation: str
    transitions: tuple[Transition, ...] = ()

    def append(self, action, observation):
        # No prior reasoning parameter exists in the state representation.
        return InteractionState(self.goal, self.initial_observation,
                                self.transitions + (Transition(dict(action), str(observation)),))

    def teacher_messages(self, system_prompt):
        return ({"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps({
                    "goal": self.goal, "initial_observation": self.initial_observation,
                    "executed_interactions": [{"action": t.action, "observation": t.observation}
                                              for t in self.transitions],
                }, ensure_ascii=False)})


@dataclass(frozen=True)
class Sample:
    tokens: tuple[int, ...]
    text: str
    log_probabilities: torch.Tensor
    mean_full_vocabulary_entropy: float


@dataclass(frozen=True)
class ResponseRecord:
    history: tuple[dict, ...]
    state: InteractionState
    sample: Sample
    turn: int
    executed: bool


class StudentPolicy(Protocol):
    def sample(self, history: tuple[dict, ...]) -> Sample: ...


def response_allocation(entropies, *, multiplicity=4, concentration=2):
    if min(multiplicity, concentration) < 1 or not entropies:
        raise ValueError("positive reference budget and nonempty root trajectory required")
    if any(not math.isfinite(float(value)) for value in entropies):
        raise ValueError("state entropy must be finite")
    count = math.ceil(len(entropies) / concentration)
    selected = sorted(range(len(entropies)), key=lambda i: (-entropies[i], i))[:count]
    return selected, concentration * (multiplicity - 1)


def full_vocabulary_entropy(logits):
    probabilities = logits.float().softmax(-1)
    return -(probabilities * logits.float().log_softmax(-1)).sum(-1)


def sampled_k1_dual_clip(current_log_probs, teacher_log_probs, behavior_log_probs):
    """Actual experimental surrogate, not a different full-vocabulary KL loss."""
    if current_log_probs.shape != teacher_log_probs.shape or current_log_probs.shape != behavior_log_probs.shape:
        raise ValueError("same response-prefix token likelihoods must align")
    if not current_log_probs.numel():
        raise ValueError("empty response cannot be supervised")
    advantage = -(current_log_probs - teacher_log_probs.detach()).clamp(-10, 10).detach()
    ratio = (current_log_probs - behavior_log_probs.detach()).clamp(-20, 20).exp()
    base = torch.maximum(-ratio * advantage, -ratio.clamp(.8, 1.2) * advantage)
    return torch.where(advantage < 0, torch.minimum(base, -3 * advantage), base)


def pooled_loss(records: list[tuple[torch.Tensor, torch.Tensor, torch.Tensor]]):
    losses = [sampled_k1_dual_clip(*record) for record in records]
    if not losses:
        raise ValueError("root/additional response pool must be nonempty")
    return sum(value.sum() for value in losses) / sum(value.numel() for value in losses)


def parse_action(text: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    found = []
    # Reasoning can contain braces. Prefer the last valid executable schema.
    for offset, char in enumerate(text):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(text[offset:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get("tool") in {"calculator", "finish"}:
            arguments = value.get("arguments")
            if isinstance(arguments, dict):
                allowed = "expression" if value["tool"] == "calculator" else "answer"
                if isinstance(arguments.get(allowed), str):
                    found.append({"tool": value["tool"], "arguments": {allowed: arguments[allowed]}})
    if not found:
        return {"tool": "invalid", "arguments": {}}
    return found[-1]


def collect_response_pool(policy: StudentPolicy, environment, *, system_prompt, max_turns=4,
                          multiplicity=4, concentration=2,
                          action_parser: Callable[[str], dict] = parse_action):
    """Only root actions execute; additional samples never create suffixes."""
    if max_turns < 1:
        raise ValueError("positive interaction budget required")
    initial = environment.reset()
    state = InteractionState(environment.goal, initial)
    history = ({"role": "system", "content": system_prompt},
               {"role": "user", "content": environment.goal + "\nObservation: " + initial})
    roots = []
    for turn in range(max_turns):
        sample = policy.sample(history)
        if not sample.tokens:
            raise ValueError("student generated an empty root response")
        roots.append(ResponseRecord(history, state, sample, turn, True))
        action = action_parser(sample.text)
        observation, done = environment.step(action)
        state = state.append(action, observation)
        history = history + ({"role": "assistant", "content": sample.text},
                             {"role": "user", "content": "Observation: " + observation})
        if done:
            break
    selected, additional = response_allocation([r.sample.mean_full_vocabulary_entropy for r in roots],
                                               multiplicity=multiplicity, concentration=concentration)
    pool = list(roots)
    for turn in selected:
        root = roots[turn]
        for _ in range(additional):
            sample = policy.sample(root.history)  # regenerate complete reasoning and action
            if not sample.tokens:
                raise ValueError("student generated an empty additional response")
            pool.append(ResponseRecord(root.history, root.state, sample, root.turn, False))
    return pool, {"root_turns": len(roots), "selected_turns": selected,
                  "additional_responses_per_selected_state": additional,
                  "response_pool_size": len(pool), "nominal_reference_responses": multiplicity * len(roots),
                  "root_actions_executed": len(roots), "additional_actions_executed": 0,
                  "complete_response_resampling": True}
