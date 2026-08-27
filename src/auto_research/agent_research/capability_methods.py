from __future__ import annotations

from dataclasses import dataclass, field

from .capability_models import (
    CapabilityObservation,
    CapabilityPrediction,
    ToolCaller,
    ToolFeedback,
)


CAPABILITY_METHODS = (
    "long-context", "react", "reflexion", "agent-g2", "ahead", "auso",
)


def _tool_map(observation: CapabilityObservation) -> dict[str, str]:
    return {tool.tag: tool.name for tool in observation.tools}


def _call_candidates(
    tags: tuple[str, ...], mapping: dict[str, str], call: ToolCaller,
    *, retry: bool,
) -> tuple[ToolFeedback, int]:
    retries = 0
    feedback = ToolFeedback("wrong_tool", "No candidate tool was available.")
    for tag in tags:
        tool = mapping.get(tag)
        if not tool:
            continue
        feedback = call(tool)
        if feedback.status == "transient_error" and retry:
            retries += 1
            feedback = call(tool)
        if feedback.status in {"ok", "hint"}:
            return feedback, retries
    return feedback, retries


@dataclass
class CapabilityPolicy:
    method: str
    skills: dict[str, tuple[str, ...]] = field(default_factory=dict)

    def solve(
        self, observation: CapabilityObservation, call: ToolCaller,
    ) -> CapabilityPrediction:
        if self.method not in CAPABILITY_METHODS:
            raise ValueError(f"unsupported L2 capability method: {self.method}")
        if self.method == "auso":
            return self._solve_auso(observation, call)
        mapping = _tool_map(observation)
        tags = observation.start_tags
        answer = ""
        retries = reflections = hints = 0
        while tags:
            if self.method == "long-context":
                feedback, added = _call_candidates(tags[:1], mapping, call, retry=False)
            elif self.method in {"react", "agent-g2"}:
                feedback, added = _call_candidates(tags, mapping, call, retry=True)
            else:
                if len(tags) > 1:
                    feedback = call("guide")
                    hints += 1
                    reflections += int(self.method == "reflexion")
                    tags = feedback.next_tags
                feedback, added = _call_candidates(tags, mapping, call, retry=True)
                if feedback.status not in {"ok", "hint"} and self.method == "reflexion":
                    reflections += 1
                    guide = call("guide")
                    hints += 1
                    feedback, extra = _call_candidates(
                        guide.next_tags, mapping, call, retry=True,
                    )
                    added += extra
            retries += added
            if feedback.status != "ok":
                break
            if feedback.answer:
                answer = feedback.answer
                break
            tags = feedback.next_tags
        return CapabilityPrediction(
            answer=answer,
            source=f"l2/{self.method}/observation-tool-loop",
            retries=retries,
            reflections=reflections,
            hints=hints,
        )

    def _solve_auso(
        self, observation: CapabilityObservation, call: ToolCaller,
    ) -> CapabilityPrediction:
        mapping = _tool_map(observation)
        learned = self.skills.get(observation.family)
        answer = ""
        retries = hints = 0
        used: list[str] = []
        if learned:
            for tool in learned:
                feedback = call(tool)
                if feedback.status == "transient_error":
                    retries += 1
                    feedback = call(tool)
                if feedback.status != "ok":
                    self.skills.pop(observation.family, None)
                    break
                used.append(tool)
                if feedback.answer:
                    answer = feedback.answer
                    return CapabilityPrediction(
                        answer, "l2/auso/reused-skill", retries,
                        hints=hints, skill_reuses=1,
                    )
        tags = observation.start_tags
        used = []
        while tags:
            if len(tags) > 1:
                guide = call("guide")
                hints += 1
                tags = guide.next_tags
            feedback, added = _call_candidates(tags, mapping, call, retry=True)
            retries += added
            if feedback.status != "ok":
                break
            tool = mapping[tags[0]]
            used.append(tool)
            if feedback.answer:
                answer = feedback.answer
                self.skills[observation.family] = tuple(used)
                break
            tags = feedback.next_tags
        return CapabilityPrediction(
            answer, "l2/auso/explore-internalize", retries,
            hints=hints,
        )

