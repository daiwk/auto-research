"""LoopRoute control kernel, arXiv:2611.25363v1 §3 and Appendix C.

This executes the router state machine, not Jev, an LLM or a benchmark agent.
Public-state adapters and ALFWorld's trusted 'new information' flag are external.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
import hashlib
import json

REQUIRES_GPU_VALIDATION = False
FIELDS = {"alfworld": {"facts", "admissible_actions"},
          "mapreader": {"action_response", "room_description", "inventory"},
          "textworld": {"room_description", "inventory", "candidate_commands"}}


def public_state_key(benchmark: str, fields: Mapping) -> str:
    if benchmark not in FIELDS or set(fields) != FIELDS[benchmark]:
        raise ValueError("exact benchmark public-state fields required; history/step are excluded")
    values = dict(fields)
    if benchmark == "alfworld":
        actions = values["admissible_actions"]
        if not isinstance(actions, (list, tuple)) or not all(isinstance(x, str) for x in actions):
            raise ValueError("admissible action strings required")
        values["admissible_actions"] = sorted(actions)
    raw = json.dumps(values, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                     allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest()


@dataclass(frozen=True)
class Decision:
    policy: str
    state_key: str
    proposal: str | None
    intercepted: bool


class LoopRouter:
    def __init__(self, benchmark: str, threshold: int = 2, takeover_budget: int = 2):
        if benchmark not in FIELDS:
            raise ValueError("supported benchmark adapter required")
        if type(threshold) is not int or threshold < 1 or type(takeover_budget) is not int or takeover_budget < 1:
            raise ValueError("positive integer threshold and takeover budget required")
        self.benchmark, self.threshold, self.takeover_budget = benchmark, threshold, takeover_budget
        self.counts: Counter[tuple[str, str]] = Counter()
        self.remaining = 0
        self.pending: Decision | None = None
        self.terminated = False

    def route(self, state_key: str, proposal: str | None = None) -> Decision:
        if self.terminated or self.pending is not None:
            raise RuntimeError("record the pending execution, or start a new router after termination")
        if not isinstance(state_key, str) or not state_key:
            raise ValueError("nonempty public state key required")
        if self.remaining:
            if proposal is not None:
                raise ValueError("do not call the decision model during LLM takeover")
            decision = Decision("llm", state_key, None, False)
        else:
            if not isinstance(proposal, str) or not proposal:
                raise ValueError("decision-model proposal required under normal control")
            trigger = self.counts[state_key, proposal] >= self.threshold
            if trigger:
                self.remaining = self.takeover_budget
            decision = Decision("llm" if trigger else "decision", state_key, proposal, trigger)
        self.pending = decision
        return decision

    def record_execution(self, action: str, *, new_information: bool = False,
                         terminated: bool = False) -> None:
        """Only executed actions update counters; rejected proposals never do."""
        if self.pending is None:
            raise RuntimeError("no pending routed decision")
        if not isinstance(action, str) or not action:
            raise ValueError("executed action required")
        if type(new_information) is not bool or type(terminated) is not bool:
            raise ValueError("strict transition flags required")
        if new_information and self.benchmark != "alfworld":
            raise ValueError("new-information reset belongs only to ALFWorld")
        d = self.pending
        if d.policy == "decision" and action != d.proposal:
            raise ValueError("executed decision action must match the nonintercepted proposal")
        if self.benchmark != "alfworld" or d.policy == "decision":
            self.counts[d.state_key, action] += 1
        if d.policy == "llm":
            self.remaining -= 1
        if self.benchmark == "alfworld" and (new_information or (d.policy == "llm" and self.remaining == 0)):
            self.counts.clear()
        if terminated:
            self.remaining = 0
            self.terminated = True
        self.pending = None


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    r = LoopRouter("alfworld")
    for _ in range(2):
        assert r.route("same-public-state", "look").policy == "decision"
        r.record_execution("look")
    intercepted = r.route("same-public-state", "look")
    count_at_interception = r.counts["same-public-state", "look"]
    r.record_execution("open")
    followup = r.route("changed-state")
    r.record_execution("take")
    resumed = r.route("changed-state", "look")
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"third_proposal_intercepted_before_execution": intercepted.intercepted,
                       "interception_not_counted": count_at_interception == 2,
                       "exact_two_action_takeover": followup.policy == "llm" and resumed.policy == "decision",
                       "alfworld_takeover_reset": not r.counts},
            "metrics": {"controlled_intercepted_proposals": 1,
                        "controlled_llm_actions": 2, "controlled_environment_actions": 4}}
