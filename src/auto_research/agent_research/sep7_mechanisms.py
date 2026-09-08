"""CPU-compatible mechanisms with explicit simulator and rollout dependencies.

These kernels never manufacture task outcomes or access benchmark gold labels.
"""
from copy import deepcopy
from dataclasses import dataclass, field
import math

import numpy as np

from .method_families.base import _tokens


@dataclass
class AtomicNote:
    key: str
    content: str
    timestamp: int
    links: set[str] = field(default_factory=set)
    revisions: list[tuple[int, str]] = field(default_factory=list)


class AtomicMemory:
    """Bounded graph with revision history and multi-hop evidence paths.

    Lexical similarity is an explicit local substitute for the paper's LM.
    Callers can inject semantic similarity from a real text encoder.
    """
    def __init__(self, capacity, similarity=None):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity, self.notes = capacity, {}
        self.similarity = similarity or self.lexical_similarity

    @staticmethod
    def lexical_similarity(left, right):
        a, b = _tokens(left), _tokens(right)
        return len(a & b) / max(len(a | b), 1)

    def write(self, key, content, timestamp):
        if key in self.notes:
            note = self.notes[key]
            note.revisions.append((note.timestamp, note.content))
            note.content, note.timestamp = content, timestamp
            for other in self.notes.values():
                other.links.discard(key)
            note.links.clear()
        else:
            note = self.notes[key] = AtomicNote(key, content, timestamp)
        neighbors = sorted((self.similarity(content, other.content), other.key)
                           for other in self.notes.values() if other.key != key)
        for similarity, neighbor in neighbors[-3:]:
            if similarity > 0:
                note.links.add(neighbor)
                self.notes[neighbor].links.add(key)
        while len(self.notes) > self.capacity:
            victim = min(self.notes, key=lambda k: (self.notes[k].timestamp, k))
            del self.notes[victim]
            for other in self.notes.values():
                other.links.discard(victim)

    def retrieve(self, query, hops=2, top_k=3):
        scores = sorted(((self.similarity(query, n.content), n.key)
                         for n in self.notes.values()), reverse=True)
        paths = [(key,) for score, key in scores[:top_k] if score > 0]
        visited, frontier = {p[0] for p in paths}, list(paths)
        for _ in range(hops):
            next_frontier = []
            for path in frontier:
                for key in sorted(self.notes[path[-1]].links):
                    if key not in visited:
                        visited.add(key)
                        next_frontier.append((*path, key))
            paths.extend(next_frontier)
            frontier = next_frontier
        return [self.notes[p[-1]] for p in paths], paths


class HierarchicalSkills:
    """Task-to-step bundles; edits stay private until post-edit execution."""
    def __init__(self, capacity=24):
        self.capacity, self.bundles, self.pending = capacity, {}, {}

    def retrieve(self, query):
        scores = [(AtomicMemory.lexical_similarity(query, key), key) for key in self.bundles]
        return max(scores)[1] if scores and max(scores)[0] > 0 else None

    def stage(self, task, children):
        self.pending[task] = deepcopy(children)

    def verify(self, task, execute, baseline, attempts=2):
        if attempts < 1:
            raise ValueError("verification attempts must be positive")
        candidate = self.pending.pop(task)
        # execute must reset the task per call and execute the private bundle.
        rewards = [float(execute(deepcopy(candidate))) for _ in range(attempts)]
        if not all(math.isfinite(r) for r in rewards):
            raise ValueError("nonfinite verification reward")
        if np.mean(rewards) <= baseline:
            return False
        self.bundles[task] = candidate
        while len(self.bundles) > self.capacity:
            del self.bundles[next(iter(self.bundles))]
        return True


class ShadowGate:
    """SiLR componentwise admission on a deep copy of a trusted simulator."""
    def __init__(self, simulator, severity):
        self.simulator, self.severity = simulator, severity

    def propose(self, action):
        before = np.asarray(self.severity(self.simulator), dtype=float)
        shadow = deepcopy(self.simulator)
        try:
            shadow.apply(action)
            after = np.asarray(self.severity(shadow), dtype=float)
        except (ValueError, KeyError, TypeError):
            return "FAIL", -1.0
        if (before.shape != after.shape or not np.isfinite(before).all()
                or not np.isfinite(after).all() or (before < 0).any()
                or (after < 0).any() or (after > before).any()):
            return "FAIL", -1.0
        self.simulator = shadow
        if not (after > 0).any():
            return "PASS", 1.0
        return "SAFE_PROGRESS", float((before - after).sum() / max(before.sum(), 1e-12))


def relative_credit(rewards, tasks, harnesses, mode="within"):
    """Multi-Harness RL equations 1–2, using an identical batch for both arms."""
    rewards = np.asarray(rewards, dtype=float)
    if mode not in {"within", "cross"} or not (len(rewards) == len(tasks) == len(harnesses)):
        raise ValueError("invalid grouping contract")
    if not np.isfinite(rewards).all():
        raise ValueError("nonfinite reward")
    groups = {}
    for i, (task, harness) in enumerate(zip(tasks, harnesses)):
        groups.setdefault((task, harness) if mode == "within" else (task,), []).append(i)
    advantages = np.zeros_like(rewards)
    for indices in groups.values():
        values = rewards[indices]
        advantages[indices] = (values - values.mean()) / (values.std() + 1e-8)
    return advantages


def policy_objective(log_probs, old_log_probs, advantages, clip=0.2):
    """Differentiable clipped group-relative objective shared by both arms."""
    import torch
    advantage = torch.as_tensor(advantages, device=log_probs.device, dtype=log_probs.dtype).detach()
    if log_probs.shape != old_log_probs.shape or log_probs.shape != advantage.shape:
        raise ValueError("rollout tensors must have equal shapes")
    ratio = (log_probs - old_log_probs.detach()).exp()
    return -torch.minimum(ratio * advantage, ratio.clamp(1-clip, 1+clip) * advantage).mean()


def joint_skill_objective(reasoning_log_probs, editing_log_probs, old_reasoning,
                          old_editing, reasoning_advantage, verified_edit_advantage):
    """Shared-backbone joint loss; editor credit must come from verification.

    Callers supply executed group/state advantages (e.g. GiGPO); this kernel
    does not replace delayed verification with the edit-triggering reward.
    """
    return (policy_objective(reasoning_log_probs, old_reasoning, reasoning_advantage)
            + policy_objective(editing_log_probs, old_editing, verified_edit_advantage)) / 2
