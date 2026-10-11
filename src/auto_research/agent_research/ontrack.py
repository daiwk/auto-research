"""OnTrack streaming monitor, independently implemented from 2610.12375.

No tool is executed here. References are evaluator-only inputs. Thresholds and
extractor quality must be calibrated for deployment; a verdict is not proof of
an agent's correctness. Graph recomputation is exact but not bitset-optimized.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from .ontrack_transport import diagnostic, frontier_marginal, graph_distances, gw_gradient, solve


@dataclass(frozen=True)
class Event:
    action: str
    tool: str
    arguments: str
    effect: str = ""
    parents: tuple[int, ...] = ()
    consumes: tuple[str, ...] = ()
    produces: tuple[str, ...] = ()
    errored: bool = False


@dataclass(frozen=True)
class ToolContract:
    irreversible: bool = False
    required_artifacts: tuple[str, ...] = ()


@dataclass(frozen=True)
class Reference:
    events: tuple[Event, ...]
    provenance: str = "mined"

    def __post_init__(self):
        if not self.events or self.provenance not in {"gold", "mined", "axiomatic", "planner"}:
            raise ValueError("nonempty reference and explicit provenance required")
        graph_distances([e.parents for e in self.events])


@dataclass(frozen=True)
class MonitorConfig:
    relaxation: float = .3
    entropy: float = .05
    theta: float = .35
    leak: float = .6
    match: float = .3
    grace: int = 3
    orphan_budget: float = .25
    retry_attempts: int = 2
    duplicate_similarity: float = .98
    stall_window: int = 6
    minimum_info: float = .01
    coverage_velocity: float = .01
    frontier_gap: float = .05

    def __post_init__(self):
        if not 0 <= self.theta <= 1 or min(self.relaxation, self.entropy) <= 0:
            raise ValueError("valid transport configuration required")
        if any(not 0 <= x <= 1 for x in (self.leak, self.match, self.orphan_budget,
                                         self.duplicate_similarity, self.minimum_info,
                                         self.coverage_velocity, self.frontier_gap)):
            raise ValueError("normalized thresholds required")
        if self.grace < 1 or self.stall_window < 2 or self.retry_attempts < 0:
            raise ValueError("positive lifecycle windows required")


def _distance(a, b):
    return np.clip((1 - np.asarray(a) @ np.asarray(b).T) / 2, 0, 1)


class PrefixGraph:
    """First-producer artifact ledger plus explicit retroactive edge repair."""

    def __init__(self):
        self.events: list[Event] = []
        self.parents: list[set[int]] = []
        self.producers: dict[str, int] = {}
        self.consumed: set[int] = set()

    def append(self, event):
        index = len(self.events)
        if any(not 0 <= p < index for p in event.parents):
            raise ValueError("declared parents must precede event")
        self.events.append(event)
        self.parents.append(set(event.parents))
        for artifact in event.produces:
            self.register_artifact(index, artifact)
        self._repair()

    def register_artifact(self, index, artifact):
        if not 0 <= index < len(self.events) or not artifact:
            raise ValueError("existing producer and nonempty artifact required")
        self.producers.setdefault(artifact, index)
        self._repair()

    def _repair(self):
        for child, event in enumerate(self.events):
            for artifact in event.consumes:
                parent = self.producers.get(artifact)
                if parent is not None and parent < child:
                    self.parents[child].add(parent)
                    self.consumed.add(parent)

    def ages(self):
        now = len(self.events) - 1
        return np.array([1. if i in self.consumed else min(1., (now - i) / 3)
                         for i in range(len(self.events))])

    def distances(self):
        return graph_distances(self.parents)


@dataclass
class _ReferenceState:
    reference: Reference
    action: np.ndarray
    arguments: np.ndarray
    distances: np.ndarray
    parents: list[set[int]]
    state: object = None
    marginal: np.ndarray | None = None
    active: np.ndarray | None = None
    satisfied: np.ndarray | None = None
    lookahead: float = .3
    gap_events: int = 0


class OnTrackMonitor:
    def __init__(self, embed: Callable, *, references=(), contracts=None, config=None):
        self.embed = embed
        self.config = config or MonitorConfig()
        self.contracts = dict(contracts or {})
        self.graph = PrefixGraph()
        self.action, self.arguments, self.effects = [], [], []
        self.references = []
        for ref in references:
            graph = PrefixGraph()
            for event in ref.events:
                graph.append(event)
            self.references.append(_ReferenceState(
                ref, self._embed([e.action for e in ref.events]),
                self._embed([e.arguments for e in ref.events]), graph.distances(), graph.parents))
        self.mass = 1 / np.mean([len(r.reference.events) for r in self.references]) if self.references else 1.
        self.lifecycle: dict[int, str] = {}
        self.coverage_history: list[float] = []
        self.info_history: list[float] = []
        self.best_history: list[int] = []
        self.last_losses: list[float] = []

    def _embed(self, texts):
        value = np.asarray(self.embed(texts), dtype=np.float64)
        if value.ndim != 2 or value.shape[0] != len(texts) or not np.isfinite(value).all():
            raise ValueError("finite text embedding matrix required")
        norms = np.linalg.norm(value, axis=1, keepdims=True)
        if (norms == 0).any():
            raise ValueError("nonzero text embeddings required")
        return value / norms

    def _cost(self, reference):
        tools = np.array([[float(e.tool != r.tool) for r in reference.reference.events] for e in self.graph.events])
        return .45 * _distance(self.action, reference.action) + .20 * _distance(self.arguments, reference.arguments) + .35 * tools

    def _solve(self, *, escalated=False):
        cfg = self.config
        prefix = self.graph.distances()
        losses = []
        for ref in self.references:
            previous = ref.state.coupling if ref.state is not None else np.zeros((0, len(ref.reference.events)))
            if not escalated:
                ref.marginal, ref.active, ref.satisfied = frontier_marginal(
                    ref.parents, previous, lookahead=ref.lookahead)
            # Escalation freezes the current event's lagged mask, not a new one.
            ref.state = solve(self._cost(ref), prefix, ref.distances,
                              np.full(len(prefix), self.mass), ref.marginal,
                              state=ref.state, ages=self.graph.ages(),
                              outer=10 if escalated else 1, inner=50 if escalated else 5,
                              relaxation=cfg.relaxation, entropy=cfg.entropy, theta=cfg.theta)
            losses.append(diagnostic(self._cost(ref), ref.state.coupling, prefix, ref.distances,
                                     np.full(len(prefix), self.mass), ref.marginal,
                                     relaxation=cfg.relaxation, entropy=cfg.entropy, theta=cfg.theta))
        self.last_losses = losses
        return int(np.argmin(losses))

    def _signals(self, best):
        ref = self.references[best]
        t = ref.state.coupling
        nominal = np.full(t.shape[1], 1 / t.shape[1])
        cov = t.sum(0) / nominal
        leakage = np.clip(1 - t.sum(1) / self.mass, 0, 1)
        g = np.maximum(gw_gradient(t, self.graph.distances(), ref.distances), 0.) * self.graph.ages()[:, None]
        linear = (1 - self.config.theta) * self._cost(ref) + self.config.theta * g
        matched = (t * linear).sum(1) / (t.sum(1) + 1e-12)
        return leakage, matched, float(np.minimum(cov, 1).mean())

    def gate(self, proposal):
        """Pure pre-execution check; never appends the proposal or fabricates effects."""
        contract = self.contracts.get(proposal.tool)
        if contract is None or not contract.irreversible:
            return {"verdict": "OK", "automatic_intervention": False, "reason": "reversible or unannotated tool"}
        missing = [a for a in contract.required_artifacts if a not in self.graph.producers]
        if missing:
            return {"verdict": "BLOCK", "automatic_intervention": True, "reason": "missing schema prerequisites", "missing": missing}
        if not self.references:
            return {"verdict": "OK", "automatic_intervention": False, "reason": "schema only; no reference"}
        best = int(np.argmin(self.last_losses)) if self.last_losses else 0
        ref = self.references[best]
        previous = ref.state.coupling if ref.state is not None else np.zeros((0, len(ref.reference.events)))
        _, active, satisfied = frontier_marginal(ref.parents, previous, lookahead=ref.lookahead)
        cost = .45 * _distance(self._embed([proposal.action]), ref.action)[0]
        cost += .35 * np.array([float(proposal.tool != r.tool) for r in ref.reference.events])
        target = int(cost.argmin())
        if cost[target] <= self.config.match and (active[target] or satisfied[target]):
            return {"verdict": "OK", "automatic_intervention": False, "reason": "current frontier proposal match"}
        authoritative = ref.reference.provenance in {"gold", "mined", "axiomatic"}
        return {"verdict": "BLOCK" if authoritative else "WARN", "automatic_intervention": authoritative,
                "reason": "proposal mismatch or inactive prerequisite", "reference_provenance": ref.reference.provenance}

    def _intrinsic(self):
        cfg = self.config
        event = self.graph.events[-1]
        matches = [i for i, e in enumerate(self.graph.events[:-1])
                   if e.tool == event.tool and (1 - _distance([self.action[-1]], [self.action[i]])[0, 0] * 2) >= cfg.duplicate_similarity
                   and (1 - _distance([self.arguments[-1]], [self.arguments[i]])[0, 0] * 2) >= cfg.duplicate_similarity]
        info = 1. if len(self.effects) == 1 else float(np.clip(1 - np.max(np.asarray(self.effects[:-1]) @ self.effects[-1]), 0, 1))
        if matches:
            # Only consecutive attempts of an errored equivalent call qualify.
            start = len(self.graph.events) - 2
            attempts = 0
            while start in matches and self.graph.events[start].errored:
                attempts += 1
                start -= 1
            if not (1 <= attempts <= cfg.retry_attempts):
                return "LOOP", info
        if len(self.info_history) >= cfg.stall_window - 1 and max([*self.info_history[-(cfg.stall_window - 1):], info]) < cfg.minimum_info:
            return "STALLED", info
        return "OK", info

    def _verdict(self, best, intrinsic):
        leak, match, coverage = self._signals(best)
        ref = self.references[best]
        cfg = self.config
        states = dict(self.lifecycle)
        newest = len(self.graph.events) - 1
        costs = self._cost(ref)
        for i in range(newest + 1):
            if i in self.graph.consumed:
                states[i] = "MATCHED"
                continue
            nearest = int(costs[i].argmin())
            if costs[i, nearest] <= cfg.match and not ref.active[nearest] and not ref.satisfied[nearest]:
                # Same unmasked attributes, missing causal producers.
                states[i] = "CAUSAL_INVERSION"
            elif leak[i] <= cfg.leak:
                states[i] = "MATCHED"
            elif newest - i < cfg.grace:
                states[i] = "EXPLORING"
            elif costs[i, nearest] <= cfg.match:
                states[i] = "MATCHED"
            else:
                states[i] = "ORPHAN"
        # Isolated abandoned 1–2-node branches stay bounded and non-alarming;
        # a persistent streak is not silently converted into abandonment.
        orphans = [i for i, s in states.items() if s == "ORPHAN"]
        live_streak = any(states.get(i) == "EXPLORING" for i in range(max(0, newest - 2), newest + 1))
        if not live_streak and len(orphans) <= 2 and len(orphans) * self.mass <= cfg.orphan_budget:
            for i in orphans:
                states[i] = "ABANDONED"
            orphans = []
        verdict = intrinsic
        if verdict == "OK":
            if "CAUSAL_INVERSION" in states.values():
                verdict = "CAUSAL_INVERSION"
            elif len(orphans) * self.mass > cfg.orphan_budget:
                verdict = "OFF_TRACK"
            elif len(self.coverage_history) >= cfg.stall_window and coverage - self.coverage_history[-cfg.stall_window] < cfg.coverage_velocity:
                verdict = "STALLED"
            elif match[-1] > cfg.match:
                verdict = "WARN"
            elif "EXPLORING" in states.values():
                verdict = "EXPLORING"
            elif len(self.best_history) >= 3 and best == self.best_history[-2] != self.best_history[-1]:
                verdict = "WARN"
        return verdict, states, {"leakage": float(leak[-1]), "match_cost": float(match[-1]),
                                 "coverage": coverage, "unresolved_mass": len(orphans) * self.mass}

    def admit(self, event):
        """Observe an already-executed event. Call gate() before execution yourself."""
        self.graph.append(event)
        self.action.append(self._embed([event.action])[0])
        self.arguments.append(self._embed([event.arguments])[0])
        self.effects.append(self._embed([event.effect])[0])
        intrinsic, info = self._intrinsic()
        if not self.references:
            self.info_history.append(info)
            return {"verdict": intrinsic, "automatic_intervention": intrinsic in {"LOOP", "STALLED"},
                    "transport_enabled": False, "info_gain": info, "escalated": False}
        best = self._solve()
        ref = self.references[best]
        # Persistent masked/unmasked diagnostic gap widens lookahead first.
        unmasked = solve(self._cost(ref), self.graph.distances(), ref.distances,
                         np.full(len(self.graph.events), self.mass), np.full(len(ref.reference.events), 1 / len(ref.reference.events)),
                         state=ref.state, ages=self.graph.ages(), relaxation=self.config.relaxation,
                         theta=self.config.theta, entropy=self.config.entropy)
        loss = diagnostic(self._cost(ref), unmasked.coupling, self.graph.distances(), ref.distances,
                          np.full(len(self.graph.events), self.mass), np.full(len(ref.reference.events), 1 / len(ref.reference.events)),
                          relaxation=self.config.relaxation, theta=self.config.theta, entropy=self.config.entropy)
        ref.gap_events = ref.gap_events + 1 if self.last_losses[best] - loss > self.config.frontier_gap else 0
        widened = ref.gap_events >= self.config.grace and ref.lookahead < 1
        if widened:
            ref.lookahead = min(1., ref.lookahead * 2)
            best = self._solve()
        verdict, states, signals = self._verdict(best, intrinsic)
        severe = verdict in {"LOOP", "STALLED", "OFF_TRACK", "CAUSAL_INVERSION"}
        if severe:
            best = self._solve(escalated=True)
            verdict, states, signals = self._verdict(best, intrinsic)
        confirmed_severe = verdict in {"LOOP", "STALLED", "OFF_TRACK", "CAUSAL_INVERSION"}
        self.lifecycle = states
        self.coverage_history.append(signals["coverage"])
        self.info_history.append(info)
        self.best_history.append(best)
        minimum = min(self.last_losses)
        softmin = minimum - .05 * np.log(np.mean(np.exp(-(np.array(self.last_losses) - minimum) / .05)))
        authority = self.references[best].reference.provenance in {"gold", "mined"}
        automatic = confirmed_severe and (authority or intrinsic != "OK")
        return {"verdict": verdict if authority or intrinsic != "OK" or not confirmed_severe else "WARN",
                "automatic_intervention": automatic, "transport_enabled": True, "escalated": severe,
                "frontier_stall": widened, "score": float(np.exp(-max(softmin, 0))),
                "reference": best, "reference_provenance": self.references[best].reference.provenance,
                "info_gain": info, "lifecycle": dict(states), **signals}

    def finalize(self):
        """Canonical cold batch invocation: no mask, ages, or warm-start state."""
        if not self.graph.events or not self.references:
            return {"transport_enabled": False, "score": None}
        losses = []
        for ref in self.references:
            mu = np.full(len(self.graph.events), 1 / len(self.graph.events))
            nu = np.full(len(ref.reference.events), 1 / len(ref.reference.events))
            state = solve(self._cost(ref), self.graph.distances(), ref.distances, mu, nu,
                          outer=10, inner=50, theta=self.config.theta, relaxation=self.config.relaxation,
                          entropy=self.config.entropy)
            losses.append(diagnostic(self._cost(ref), state.coupling, self.graph.distances(), ref.distances, mu, nu,
                                     theta=self.config.theta, relaxation=self.config.relaxation, entropy=self.config.entropy))
        minimum = min(losses)
        softmin = minimum - .05 * np.log(np.mean(np.exp(-(np.array(losses) - minimum) / .05)))
        return {"transport_enabled": True, "score": float(np.exp(-max(softmin, 0))), "losses": losses,
                "canonical_initialization": True, "age_weights_disabled": True, "frontier_mask_disabled": True}
