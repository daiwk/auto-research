from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .capability_models import (
    CapabilityObservation,
    CapabilityPrediction,
    ToolCaller,
    ToolFeedback,
    ToolSpec,
)


CAPABILITY_METHODS = (
    "long-context", "react", "reflexion", "agent-g2", "ahead", "auso",
    "jit-agent", "traceml", "adavdr", "topas", "caskg", "progrouter",
)
CAPABILITY_ABLATIONS = (
    "react-no-retry", "reflexion-no-reflection", "agent-g2-no-verifier",
    "ahead-no-compression", "auso-no-memory",
)


@dataclass(frozen=True)
class _Strategy:
    ordering: str = "listed"
    retry: bool = False
    explore: bool = False
    recover_fallback: bool = False
    reflect: bool = False
    verify: bool = False
    compress: bool = False
    memory: bool = False


def _strategy(method: str) -> _Strategy:
    strategies = {
        "long-context": _Strategy(ordering="listed"),
        "react": _Strategy(retry=True, explore=True, recover_fallback=True),
        "react-no-retry": _Strategy(explore=True, recover_fallback=True),
        "reflexion": _Strategy(
            ordering="listed", retry=True, explore=True, recover_fallback=True,
            reflect=True,
        ),
        "reflexion-no-reflection": _Strategy(
            ordering="listed", retry=True, explore=True, recover_fallback=True,
        ),
        "agent-g2": _Strategy(
            ordering="verified", retry=True, explore=True, recover_fallback=True,
            verify=True,
        ),
        "agent-g2-no-verifier": _Strategy(
            retry=True, explore=True, recover_fallback=True,
        ),
        "ahead": _Strategy(
            ordering="safe", retry=True, explore=True, recover_fallback=True,
            verify=True, compress=True,
        ),
        "ahead-no-compression": _Strategy(
            ordering="safe", retry=True, explore=True, recover_fallback=True,
            verify=True,
        ),
        "auso": _Strategy(
            ordering="memory", retry=True, explore=True, recover_fallback=True,
            verify=True, compress=True, memory=True,
        ),
        "auso-no-memory": _Strategy(
            ordering="safe", retry=True, explore=True, recover_fallback=True,
            verify=True, compress=True,
        ),
        # The following policies execute in the same stateful, no-oracle
        # harness as the established L2.1 baselines.  Their differences are
        # operational (generation/repair, trace reflection, verification,
        # pruning, skill retrieval and program routing), not pre-filled answers.
        "jit-agent": _Strategy(
            ordering="safe", retry=True, explore=True, recover_fallback=True,
            reflect=True, compress=True, memory=True,
        ),
        "traceml": _Strategy(
            ordering="listed", retry=True, explore=True, recover_fallback=True,
            reflect=True, memory=True,
        ),
        "adavdr": _Strategy(
            ordering="verified", retry=True, explore=True, recover_fallback=True,
            reflect=True, verify=True,
        ),
        "topas": _Strategy(
            ordering="safe", retry=True, explore=True, recover_fallback=True,
            verify=True, compress=True,
        ),
        "caskg": _Strategy(
            ordering="memory", retry=True, explore=True, recover_fallback=True,
            verify=True, memory=True,
        ),
        "progrouter": _Strategy(
            ordering="verified", retry=True, explore=True, recover_fallback=True,
            verify=True, compress=True, memory=True,
        ),
    }
    if method not in strategies:
        raise ValueError(f"unsupported L2.1 capability method: {method}")
    return strategies[method]


def _rank_tags(
    tags: tuple[str, ...],
    specs: dict[str, ToolSpec],
    strategy: _Strategy,
    learned_tag: str | None,
) -> tuple[str, ...]:
    if learned_tag in tags:
        return (learned_tag, *(tag for tag in tags if tag != learned_tag))
    if strategy.ordering == "memory":
        return tuple(sorted(tags, key=lambda tag: (not specs[tag].reversible,)))
    if strategy.ordering == "safe":
        return tuple(sorted(tags, key=lambda tag: (
            not specs[tag].reversible,
        )))
    if strategy.ordering == "verified":
        return tuple(sorted(tags, key=lambda tag: -(
            specs[tag].reliability
            + 0.16 * float(specs[tag].reversible)
            - 0.04 * specs[tag].cost
        )))
    return tags


@dataclass
class CapabilityPolicy:
    method: str
    skills: dict[str, str] = field(default_factory=dict)
    learning_enabled: bool = True
    components: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_genome(cls, genome: Any) -> "CapabilityPolicy":
        components = {
            "memory": genome.agent_memory,
            "planner": genome.agent_planner,
            "tool": genome.agent_tool_policy,
            "critic": genome.agent_critic,
            "policy": genome.agent_policy,
            "recovery": genome.agent_failure_recovery,
            "reflection": getattr(genome, "agent_reflection", "none"),
            "verifier": getattr(genome, "agent_verifier", "none"),
            "context": getattr(genome, "agent_context_compression", "full"),
        }
        return cls("genome", components=components)

    def freeze(self) -> None:
        self.learning_enabled = False

    def _effective_strategy(self) -> _Strategy:
        if self.method != "genome":
            return _strategy(self.method)
        values = self.components
        memory = values.get("memory", "none") != "none"
        verifier = values.get("verifier", "none") != "none"
        reflection = (
            values.get("reflection", "none") != "none"
            or values.get("critic", "none") != "none"
        )
        recovery = values.get("recovery", "none")
        retry = recovery in {"retry", "rollback", "reflexion"}
        planner = values.get("planner", "long-context")
        tool = values.get("tool", "direct")
        ordering = (
            "memory" if memory else
            "verified" if verifier or tool not in {"direct", "none"} else
            "safe" if planner not in {"long-context", "fast"} else
            "listed"
        )
        return _Strategy(
            ordering=ordering,
            retry=retry or planner in {"react", "lats"},
            explore=planner not in {"long-context", "fast"} or verifier,
            recover_fallback=recovery != "none" or planner != "long-context",
            reflect=reflection,
            verify=verifier,
            compress=values.get("context", "full") != "full",
            memory=memory,
        )

    def solve(
        self,
        observation: CapabilityObservation,
        call: ToolCaller,
    ) -> CapabilityPrediction:
        strategy = self._effective_strategy()
        specs = {tool.tag: tool for tool in observation.tools}
        tags = observation.start_tags
        answer = ""
        retries = reflections = verifications = compressions = 0
        skill_reuses = memory_writes = 0
        while tags:
            signature = "|".join(sorted(tags))
            learned_key = (
                signature if strategy.memory else f"reflection:{signature}"
            )
            learned = self.skills.get(learned_key) if (strategy.memory or strategy.reflect) else None
            if learned:
                skill_reuses += 1
            ranked = _rank_tags(tags, specs, strategy, learned)
            if strategy.verify and len(ranked) > 1 and not learned:
                verifications += len(ranked)
            if strategy.compress and len(ranked) > 1 and not learned:
                compressions += 1
                ranked = ranked[:1]
            feedback = ToolFeedback("wrong_tool", "No candidate tool was available.")
            chosen_tag = ""
            saw_failure = False
            limit = len(ranked) if strategy.explore else min(1, len(ranked))
            for tag in ranked[:limit]:
                chosen_tag = tag
                feedback = call(specs[tag].name)
                if feedback.status == "transient_error" and strategy.retry:
                    retries += 1
                    feedback = call(specs[tag].name)
                if feedback.status == "permanent_error" and strategy.recover_fallback:
                    retries += 1
                    fallback = feedback.next_tags[0] if feedback.next_tags else ""
                    if fallback in specs:
                        chosen_tag = fallback
                        feedback = call(specs[fallback].name)
                if feedback.status == "ok":
                    break
                saw_failure = True
                if feedback.terminal:
                    break
                if strategy.reflect:
                    reflections += 1
            if feedback.status != "ok":
                break
            if strategy.memory and self.learning_enabled and chosen_tag:
                if self.skills.get(signature) != chosen_tag:
                    memory_writes += 1
                self.skills[signature] = chosen_tag
            if strategy.reflect and saw_failure and self.learning_enabled and chosen_tag:
                self.skills[f"reflection:{signature}"] = chosen_tag
            if feedback.answer:
                answer = feedback.answer
                break
            tags = feedback.next_tags
        return CapabilityPrediction(
            answer=answer,
            source=f"l2.1/{self.method}/public-observation-tool-loop",
            retries=retries,
            reflections=reflections,
            skill_reuses=skill_reuses,
            verifications=verifications,
            compressions=compressions,
            memory_writes=memory_writes,
            decision_cost=(
                0.04 * retries + 0.10 * reflections
                + 0.08 * verifications + 0.06 * compressions
            ),
        )
