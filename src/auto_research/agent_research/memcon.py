"""MemCon v3: CPU memory-control operator, not an LLM capability evaluator.

Independent implementation of equations 5--8 and Appendix C. In contrast to
the upstream mutable main's global UCB counter, this uses the paper's
state-local decision count and prior-based ties among unvisited actions.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import inspect
import json
import math
from pathlib import Path
import random
import re
from typing import Any


@dataclass(frozen=True)
class MemoryAction:
    operation: str
    top_k: int = 0
    insight_k: int = 0
    hop: int = 0


ACTIONS = (
    MemoryAction("retrieve", 1, 3, 1),
    MemoryAction("retrieve", 2, 5, 1),
    MemoryAction("retrieve", 3, 8, 2),
    MemoryAction("plan_inject", 1, 3, 0),
    MemoryAction("re_retrieve", 2, 5, 2),
    MemoryAction("consolidate"),
    MemoryAction("forget"),
    MemoryAction("retrieve", 1, 2, 0),
    MemoryAction("noop"),
)
PRIORS = {"retrieve": .5, "plan_inject": .3, "re_retrieve": .1,
          "consolidate": 0., "forget": -.1, "noop": -.2}


@dataclass(frozen=True)
class MemoryState:
    """Only observable task/execution signals; no reference answer or plan."""
    goal_type: str
    step: int = 0
    physical_actions: tuple[str, ...] = ()
    objects_held: int = 0
    locations_visited: int = 0
    memory_size: int = 0
    plan_available: bool = False
    task_index: int = 0

    def key(self) -> tuple:
        counts = (self.step, self.objects_held, self.locations_visited,
                  self.memory_size, self.task_index)
        if (not isinstance(self.goal_type, str) or not self.goal_type
                or not all(type(n) is int and n >= 0 for n in counts)
                or type(self.plan_available) is not bool
                or not all(isinstance(action, str) for action in self.physical_actions)):
            raise ValueError("nonnegative observations and nonempty goal type required")
        stuck = len(self.physical_actions) >= 2 and self.physical_actions[-1] == self.physical_actions[-2]
        phase = "early" if self.step < 8 else "mid" if self.step < 18 else "late"
        return (self.goal_type, phase, stuck, min(self.objects_held, 2),
                min(self.locations_visited // 3, 4), min(self.memory_size // 10, 5),
                self.plan_available, "warm" if self.task_index > 15 else "cold")


@dataclass(frozen=True)
class PolicyConfig:
    alpha: float = .15
    gamma: float = .9
    ucb_c: float = 1.4
    warm_start: bool = True

    def __post_init__(self):
        if (not all(math.isfinite(x) for x in (self.alpha, self.gamma, self.ucb_c))
                or not 0 < self.alpha <= 1 or not 0 < self.gamma < 1 or self.ucb_c < 0):
            raise ValueError("finite alpha in (0,1], gamma in (0,1), c >= 0 required")


class TabularPolicy:
    def __init__(self, config: PolicyConfig | None = None):
        self.config = config or PolicyConfig()
        self.q: dict[tuple, list[float]] = {}
        self.counts: dict[tuple, list[int]] = {}
        self.updates = 0

    def _ensure(self, key):
        if key not in self.q:
            self.q[key] = [PRIORS[a.operation] if self.config.warm_start else 0. for a in ACTIONS]
            self.counts[key] = [0] * len(ACTIONS)

    def scores(self, key):
        self._ensure(key)
        total = sum(self.counts[key])
        return tuple(float("inf") if count == 0 else value + self.config.ucb_c *
                     math.sqrt(math.log(max(total, 1)) / count)
                     for value, count in zip(self.q[key], self.counts[key], strict=True))

    def record(self, key, index):
        if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < len(ACTIONS):
            raise ValueError("valid action index required")
        self._ensure(key)
        self.counts[key][index] += 1

    def select(self, state: MemoryState):
        key = state.key()
        scores = self.scores(key)
        # All infinity bonuses tie: warm-start Q, then stable action order.
        index = max(range(len(ACTIONS)), key=lambda i: (scores[i], self.q[key][i], -i))
        self.record(key, index)
        return index, ACTIONS[index]

    def update(self, episode: list[tuple[tuple, int]], reward: float):
        if not math.isfinite(reward):
            raise ValueError("finite terminal reward required")
        for offset, (key, index) in enumerate(reversed(episode)):
            self._ensure(key)
            if type(index) is not int or not 0 <= index < len(ACTIONS):
                raise ValueError("invalid recorded action")
            target = self.config.gamma ** offset * reward
            old = self.q[key][index]
            self.q[key][index] = old + self.config.alpha * (target - old)
        self.updates += 1

    def snapshot(self):
        return {"config": asdict(self.config), "updates": self.updates,
                "q": [{"key": list(k), "values": v} for k, v in sorted(self.q.items())],
                "counts": [{"key": list(k), "values": v} for k, v in sorted(self.counts.items())]}

    @classmethod
    def restore(cls, data):
        policy = cls(PolicyConfig(**data["config"]))
        for field in ("q", "counts"):
            target = getattr(policy, field)
            for row in data[field]:
                key, values = tuple(row["key"]), list(row["values"])
                if not _valid_key(key) or len(values) != 9 or key in target:
                    raise ValueError("malformed or duplicate policy row")
                if field == "q" and not all(type(v) in {int, float} and math.isfinite(v) for v in values):
                    raise ValueError("finite policy values required")
                if field == "counts" and not all(type(v) is int and v >= 0 for v in values):
                    raise ValueError("nonnegative integer counts required")
                target[key] = values
        if policy.q.keys() != policy.counts.keys() or type(data["updates"]) is not int or data["updates"] < 0:
            raise ValueError("policy rows or update count inconsistent")
        policy.updates = data["updates"]
        return policy


def _valid_key(key):
    if len(key) != 8:
        return False
    return (isinstance(key[0], str) and bool(key[0]) and key[1] in ("early", "mid", "late")
            and type(key[2]) is bool and type(key[6]) is bool and key[7] in ("cold", "warm")
            and all(type(v) is int and 0 <= v <= limit
                    for v, limit in zip(key[3:6], (2, 4, 5), strict=True)))


def episode_reward(success: bool, *, steps: int, horizon: int = 30) -> float:
    if type(success) is not bool or type(steps) is not int or type(horizon) is not int or steps < 0 or horizon <= 0:
        raise ValueError("binary feedback, nonnegative steps, positive horizon required")
    return (1. if success else -.5) + .3 * max(0., 1. - steps / horizon)


@dataclass(frozen=True)
class MemoryEntry:
    identity: str
    goal_type: str
    text: str
    success: bool
    observed_actions: tuple[str, ...] = ()
    insights: tuple[str, ...] = ()
    links: tuple[str, ...] = ()

    def __post_init__(self):
        if (not isinstance(self.identity, str) or not self.identity
                or not isinstance(self.goal_type, str) or not self.goal_type
                or not isinstance(self.text, str) or type(self.success) is not bool
                or not all(isinstance(x, str) for group in (self.observed_actions, self.insights, self.links) for x in group)):
            raise ValueError("identified observation, binary feedback, textual actions/insights/links required")


def _tokens(text):
    return set(re.findall(r"[\w]+", text.casefold()))


class InMemoryBackend:
    """Transparent lexical/linked memory substrate, not a G-Memory proxy.

Entries must originate in public observations/executed trajectories. Links
are explicitly supplied by the caller, never mined from a gold solution.
Consolidation deduplicates insights; forgetting removes failed episodes.
"""
    def __init__(self, entries=()):
        self.entries: list[MemoryEntry] = []
        self.calls: list[tuple[str, dict]] = []
        for entry in entries:
            self.store(entry)

    @property
    def size(self):
        return len(self.entries)

    def store(self, entry):
        if not isinstance(entry, MemoryEntry) or not entry.identity or any(e.identity == entry.identity for e in self.entries):
            raise ValueError("unique identified memory entry required")
        self.entries.append(entry)

    def retrieve(self, query, *, top_k, insight_k, hop):
        self.calls.append(("retrieve", {"query": query, "top_k": top_k, "insight_k": insight_k, "hop": hop}))
        wanted = _tokens(query)
        scores = {e.identity: len(wanted & _tokens(e.text + " " + e.goal_type)) for e in self.entries}
        # Optional explicitly linked retrieval: propagate query relevance.
        for _ in range(max(0, hop - 1)):
            prior = dict(scores)
            for entry in self.entries:
                for link in entry.links:
                    if link in scores:
                        scores[link] = max(scores[link], .5 * prior[entry.identity])
        ranked = sorted(self.entries, key=lambda e: (-scores[e.identity], e.identity))
        selected = tuple(e for e in ranked if scores[e.identity] > 0)[:top_k]
        insights = tuple(dict.fromkeys(i for e in selected for i in e.insights))[:insight_k]
        return selected, insights

    def maintain(self, operation):
        self.calls.append((operation, {}))
        if operation == "forget":
            before = len(self.entries)
            self.entries = [e for e in self.entries if e.success]
            return {"removed_entries": before - len(self.entries)}
        if operation != "consolidate":
            raise ValueError("unknown maintenance operation")
        seen, updated, removed = set(), [], 0
        for entry in self.entries:
            unique_list = []
            for insight in entry.insights:
                if insight not in seen:
                    unique_list.append(insight)
                    seen.add(insight)
            unique = tuple(unique_list)
            removed += len(entry.insights) - len(unique)
            updated.append(MemoryEntry(entry.identity, entry.goal_type, entry.text,
                                       entry.success, entry.observed_actions, unique, entry.links))
        self.entries = updated
        return {"removed_insights": removed}

    def snapshot(self):
        return [asdict(e) for e in self.entries]


@dataclass(frozen=True)
class MemoryContext:
    action_index: int
    query: str
    entries: tuple[MemoryEntry, ...] = ()
    insights: tuple[str, ...] = ()
    plan: tuple[str, ...] = ()
    effect: dict[str, Any] | None = None


class MemCon:
    def __init__(self, backend, policy: TabularPolicy | None = None):
        self.backend = backend
        self.policy = policy or TabularPolicy()
        self.plans: dict[str, tuple[str, ...]] = {}
        self.episode: list[tuple[tuple, int]] = []
        self.goal_type: str | None = None
        self.task_index = 0

    def begin(self, goal_type):
        if self.goal_type is not None:
            raise RuntimeError("finish current episode before beginning another")
        if not isinstance(goal_type, str) or not goal_type:
            raise ValueError("public nonempty goal type required")
        self.goal_type, self.episode = goal_type, []

    def execute(self, query: str, *, step: int, physical_actions=(), objects_held=0,
                locations_visited=0, action_index: int | None = None):
        if self.goal_type is None:
            raise RuntimeError("begin episode before memory access")
        state = MemoryState(self.goal_type, step, tuple(physical_actions), objects_held,
                            locations_visited, self.backend.size, self.goal_type in self.plans,
                            self.task_index)
        key = state.key()
        if action_index is None:
            action_index, action = self.policy.select(state)
        else:
            self.policy.record(key, action_index)
            action = ACTIONS[action_index]
        self.episode.append((key, action_index))
        entries, insights, plan, effect = (), (), (), {}
        if action.operation in {"consolidate", "forget"}:
            maintain = getattr(self.backend, "maintain", None)
            effect = maintain(action.operation) if callable(maintain) else {"unsupported": action.operation}
        elif action.operation != "noop":
            if action.operation == "re_retrieve":
                query += " alternative approach"
            params = {"top_k": action.top_k, "insight_k": action.insight_k, "hop": action.hop}
            signature = inspect.signature(self.backend.retrieve)
            if not any(p.kind == p.VAR_KEYWORD for p in signature.parameters.values()):
                params = {k: v for k, v in params.items() if k in signature.parameters}
            entries, insights = self.backend.retrieve(query, **params)
            if action.operation == "plan_inject":
                plan = self.plans.get(self.goal_type, ())
        return MemoryContext(action_index, query, tuple(entries), tuple(insights), plan, effect)

    def finish(self, *, success: bool, steps: int, observed_actions=(), horizon=30):
        if self.goal_type is None:
            raise RuntimeError("no active episode")
        reward = episode_reward(success, steps=steps, horizon=horizon)
        actions = tuple(observed_actions)
        if not all(isinstance(a, str) for a in actions):
            raise ValueError("executed actions must be strings")
        identity = f"memcon-episode-{self.task_index}"
        # Commit backend feedback before changing Q: failed storage must not
        # produce repeated terminal credit if the caller safely retries.
        self.backend.store(MemoryEntry(identity, self.goal_type, "\n".join(actions), success, actions))
        self.policy.update(self.episode, reward)
        if success and actions:
            self.plans[self.goal_type] = tuple(re.sub(r"\b\d+\b", "[id]", a) for a in actions)
        self.task_index += 1
        self.goal_type, self.episode = None, []
        return reward

    def snapshot(self):
        if not isinstance(self.backend, InMemoryBackend):
            raise TypeError("generic backend persistence belongs to its owner; use policy.snapshot")
        return {"schema_version": 1, "policy": self.policy.snapshot(),
                "plans": {k: list(v) for k, v in sorted(self.plans.items())},
                "episode": [[list(k), i] for k, i in self.episode],
                "goal_type": self.goal_type, "task_index": self.task_index,
                "backend": self.backend.snapshot()}

    def save(self, path: Path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_text(json.dumps(self.snapshot(), ensure_ascii=False, sort_keys=True) + "\n")
        temporary.replace(path)

    @classmethod
    def load(cls, path: Path):
        data = json.loads(Path(path).read_text())
        if data.get("schema_version") != 1:
            raise ValueError("unsupported MemCon snapshot")
        entries = [MemoryEntry(**{**row, "observed_actions": tuple(row["observed_actions"]),
                                 "insights": tuple(row["insights"]), "links": tuple(row["links"])})
                   for row in data["backend"]]
        controller = cls(InMemoryBackend(entries), TabularPolicy.restore(data["policy"]))
        controller.plans = {k: tuple(v) for k, v in data["plans"].items()}
        controller.episode = [(tuple(k), i) for k, i in data["episode"]]
        controller.goal_type, controller.task_index = data["goal_type"], data["task_index"]
        if type(controller.task_index) is not int or controller.task_index < 0:
            raise ValueError("invalid task index")
        if controller.goal_type is not None and (not isinstance(controller.goal_type, str) or not controller.goal_type):
            raise ValueError("invalid active goal")
        if controller.goal_type is None and controller.episode:
            raise ValueError("orphaned episode decisions")
        for key, index in controller.episode:
            if key not in controller.policy.counts or type(index) is not int or not 0 <= index < 9:
                raise ValueError("invalid active episode")
        return controller


def run_diagnostic(*, seed=42, episodes=60):
    """Controller/substrate exercise, NOT question answering or agent success.

    Feedback checks whether the actual retrieved public record is present.
    No reference plan/answer and no LLM are used. Misses remain misses.
    """
    if type(episodes) is not int or episodes <= 0:
        raise ValueError("positive episode count required")
    rng = random.Random(seed)
    backend = InMemoryBackend([MemoryEntry(f"record-{i}", "lookup", f"record_{i} observed event",
                                          True, (), ("observed event",)) for i in range(12)])
    controller = MemCon(backend)
    counts, hits, rewards = [0] * 9, 0, []
    for _ in range(episodes):
        record = rng.randrange(12)
        request = f"record_{record}"
        controller.begin("lookup")
        observations = []
        found = False
        for step in range(2):
            context = controller.execute(request, step=step, physical_actions=tuple(observations))
            counts[context.action_index] += 1
            found |= any(request in _tokens(entry.text) for entry in context.entries)
            observations.append(f"retrieve {request}")
        hits += int(found)
        rewards.append(controller.finish(success=found, steps=2, observed_actions=tuple(observations)))
    return {"schema_version": 2, "method": "memcon", "seed": seed,
            "diagnostic_only": True, "evaluation_tier": "L1",
            "protocol": {"name": "synthetic-observed-record-memory-operation-diagnostic-v1",
                         "gold_access": False, "llm_calls": 0, "episodes": episodes,
                         "feedback": "presence of requested public record in actual retrieval",
                         "data_source": "12 generated, openly observable record strings; no benchmark dataset",
                         "capability_comparison": False, "backend": "lexical-linked in-memory"},
            "metrics": {"retrieval_hit_rate": hits / episodes, "mean_terminal_reward": sum(rewards) / episodes,
                        "action_counts": counts, "policy_updates": controller.policy.updates,
                        "state_rows": len(controller.policy.q), "memory_entries": backend.size}}


def main(argv=None):
    parser = argparse.ArgumentParser(description="MemCon CPU memory-controller diagnostic (not capability benchmark)")
    parser.add_argument("--episodes", type=int, default=60)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    payload = json.dumps(run_diagnostic(seed=args.seed, episodes=args.episodes), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
