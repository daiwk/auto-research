"""CoSkill's sequential roles and deferred, reset-based skill verification.

Generation is injected and receives public text only. The same callable is
used by both roles; checkpoint training lives outside the environment boundary.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
import json
from typing import Callable

import numpy as np

from .capability_models import CapabilityObservation, ToolFeedback
from .sep7_mechanisms import HierarchicalSkills


@dataclass
class Decision:
    role: str
    prompt: str
    completion: str
    anchor: str
    trajectory: str
    task: str
    reward: float = 0.0
    episode_return: float = 0.0
    base_skill: str = ""


@dataclass
class Attempt:
    reward: float
    decisions: list[Decision]
    edits: list[dict] = field(default_factory=list)
    trace: list[dict] = field(default_factory=list)


def parse_object(text: str) -> dict:
    text = text.strip()
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("action must be a JSON object")
    return value


def attempt(
    observation: CapabilityObservation,
    call: Callable[[str], ToolFeedback],
    generate: Callable[[str, str], str],
    bundle: list,
    trajectory: str,
    *,
    edit: bool,
    max_turns: int = 12,
    similarity=None,
) -> Attempt:
    # No task/answer/plan object crosses this API. Terminal evidence can only
    # be obtained from a real call to the supplied environment.
    history, decisions, edits = [], [], []
    tags = observation.start_tags
    reward = 0.0
    base_skill = json.dumps(bundle, sort_keys=True)
    for _ in range(max_turns):
        state = json.dumps({"tags": tags, "history": history}, sort_keys=True)
        active = max(bundle, key=lambda child: similarity(state, str(child))) if bundle and similarity else (
            max(bundle, key=lambda child: len(set(str(child).split()) & set(state.split()))) if bundle else None)
        public = {
            "request": observation.request, "tags": tags,
            "tools": [asdict(tool) for tool in observation.tools],
            "history": history, "step_skill": active,
        }
        prompt = (
            'Choose the next tool using current evidence tags. Return only '
            'JSON {"tool":"name"}. Never invent tool results.\n'
            + json.dumps(public)
        )
        completion = generate("reasoning", prompt)
        reasoning = Decision("reasoning", prompt, completion,
                             json.dumps([observation.request, tags]),
                             trajectory, observation.task_id, base_skill=base_skill)
        decisions.append(reasoning)
        try:
            tool = parse_object(completion)["tool"]
            if not isinstance(tool, str):
                raise ValueError("tool must be text")
            feedback = call(tool)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            feedback = ToolFeedback("invalid_action", "Invalid tool action JSON.")
            tool = ""
        transition = {"tool": tool, "feedback": asdict(feedback)}
        reasoning.reward = float(feedback.status == "ok" and feedback.terminal)
        reward += reasoning.reward
        history.append(transition)
        if edit:
            meta_prompt = (
                'Improve the active child skill using this observed transition. '
                'Return only JSON with operation insert/update/delete/keep, '
                'index (for update/delete), and procedure (for insert/update). '
                'Do not predict verification outcomes.\n'
                + json.dumps({"state": public, "transition": transition, "children": bundle})
            )
            meta_text = generate("editing", meta_prompt)
            decisions.append(Decision(
                "editing", meta_prompt, meta_text,
                json.dumps([observation.request, tags, active], sort_keys=True),
                trajectory + ":edits", observation.task_id, base_skill=base_skill,
            ))
            try:
                edits.append(parse_object(meta_text))
            except (ValueError, json.JSONDecodeError):
                edits.append({"operation": "invalid"})
        if feedback.terminal:
            break
        if feedback.next_tags:
            tags = feedback.next_tags
    for decision in decisions:
        if decision.role == "reasoning":
            decision.episode_return = reward
    return Attempt(reward, decisions, edits, history)


def collect_group(observation, reset, generate, skills: HierarchicalSkills,
                  *, group_size=2, verification_attempts=2, max_turns=12):
    """reset() returns a fresh tool callable for the SAME training task.

    All group rollouts share a frozen base bundle. Only the best verified edit
    is promoted, after the group is complete; no rollout sees a sibling edit.
    """
    if group_size < 2 or verification_attempts < 1:
        raise ValueError("relative credit needs >=2 rollouts and >=1 verification")
    key = skills.retrieve(observation.request) or observation.request
    base = deepcopy(skills.bundles.get(key, []))
    decisions, candidates, records = [], [], []
    for index in range(group_size):
        baseline = attempt(observation, reset(), generate, base,
                           f"{observation.task_id}:{index}:base", edit=True,
                           max_turns=max_turns, similarity=skills.similarity)
        private = HierarchicalSkills(skills.capacity, skills.similarity)
        private.bundles[key] = deepcopy(base)
        valid = True
        for proposal in baseline.edits:
            try:
                private.edit(key, proposal.get("operation"), proposal.get("index"),
                             proposal.get("procedure"))
            except (ValueError, TypeError):
                valid = False
        edited = private.pending.get(key, deepcopy(base))
        verification = [attempt(
            observation, reset(), generate, edited,
            f"{observation.task_id}:{index}:verify:{number}", edit=False,
            max_turns=max_turns, similarity=skills.similarity,
        ) for number in range(verification_attempts)]
        delta = float(np.mean([row.reward for row in verification]) - baseline.reward)
        for decision in baseline.decisions:
            if decision.role == "editing":
                decision.episode_return = delta
                decision.reward = delta
        decisions.extend(baseline.decisions)
        for row in verification:
            decisions.extend(row.decisions)
        eligible = valid and edited != base and delta > 0
        if eligible:
            candidates.append((delta, index, deepcopy(edited)))
        records.append({"baseline": baseline.reward,
                        "verification": [row.reward for row in verification],
                        "delta": delta, "eligible": eligible,
                        "trace": baseline.trace, "edits": baseline.edits})
    if candidates:
        _, _, best = max(candidates, key=lambda row: (row[0], -row[1]))
        skills.lineage.setdefault(key, []).append(base)
        skills.bundles[key] = best
        while len(skills.bundles) > skills.capacity:
            del skills.bundles[next(iter(skills.bundles))]
    return decisions, records


def role_advantages(decisions: list[Decision], step_weight=1.0) -> np.ndarray:
    """Normalize unique episodes, not length-weighted repeated returns.

    Role, task and editing base bundle define the episode group. Step groups
    additionally condition on the role-specific public anchor state.
    """
    groups = {}
    for index, item in enumerate(decisions):
        key = (item.role, item.task, item.base_skill if item.role == "editing" else "")
        groups.setdefault(key, []).append(index)
    result = np.zeros(len(decisions))
    for indices in groups.values():
        episodes = {}
        for index in indices:
            row = decisions[index]
            if row.trajectory in episodes and episodes[row.trajectory] != row.episode_return:
                raise ValueError("inconsistent episode return")
            episodes[row.trajectory] = row.episode_return
        values = np.asarray(list(episodes.values()))
        episode_adv = dict(zip(episodes, (values - values.mean()) / (values.std() + 1e-8)))
        anchors = {}
        for index in indices:
            result[index] = episode_adv[decisions[index].trajectory]
            anchors.setdefault(decisions[index].anchor, []).append(index)
        for members in anchors.values():
            # Monte-Carlo return-to-go is valid with terminal-only task reward;
            # editing receives the deferred verified improvement.
            values = np.asarray([decisions[i].episode_return for i in members])
            local = (values - values.mean()) / (values.std() + 1e-8)
            result[members] += step_weight * local
    return result
