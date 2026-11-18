"""BATS budget/cost and external-verdict state kernel, not a search agent.

Implements equations 1-2, Budget Tracker, and Appendix B control transitions
from arXiv:2511.17006v2. Planning, semantic verification, summarization, tools,
and final answer selection must be supplied externally. No gold-answer input.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import math

REQUIRES_GPU_VALIDATION = False


def _count(value: int) -> None:
    if type(value) is not int or value < 0:
        raise ValueError("nonnegative integer count required")


@dataclass
class BudgetTracker:
    budgets: dict[str, int]
    used: dict[str, int] = field(init=False)

    def __post_init__(self):
        if not self.budgets or any(not isinstance(k, str) or not k for k in self.budgets):
            raise ValueError("named per-tool budgets required")
        self.budgets = dict(self.budgets)
        for value in self.budgets.values():
            _count(value)
        self.used = {key: 0 for key in self.budgets}

    @property
    def active(self) -> bool:
        # The original algorithm stops when ANY tool budget is exhausted.
        return all(self.used[key] < limit for key, limit in self.budgets.items())

    def record_call(self, tool: str, count: int = 1) -> None:
        _count(count)
        if tool not in self.used or not count:
            raise ValueError("known tool and positive invocation count required")
        if not self.active or self.used[tool] + count > self.budgets[tool]:
            raise ValueError("tool call exceeds the active per-question budget")
        self.used[tool] += count

    def snapshot(self) -> dict:
        return {tool: {"used": self.used[tool], "remaining": limit - self.used[tool]}
                for tool, limit in self.budgets.items()}

    def status_block(self) -> str:
        rows = [f"{tool} Budget Used: {self.used[tool]}, {tool} Budget Remaining: {limit - self.used[tool]}"
                for tool, limit in self.budgets.items()]
        return "<budget>\n" + "\n".join(rows) + "\nMake the best use of the available resources.\n</budget>"


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int
    output_tokens: int
    cached_input_tokens: int = 0

    def __post_init__(self):
        for value in (self.input_tokens, self.output_tokens, self.cached_input_tokens):
            _count(value)
        if self.cached_input_tokens > self.input_tokens:
            raise ValueError("cached input is a subset of total input, not an extra charge")


def unified_cost(usage: TokenUsage, calls: dict[str, int], *, input_price: float,
                 output_price: float, cache_price: float, tool_prices: dict[str, float]) -> float:
    """Eq.2, with explicit caller-supplied prices per token/invocation.

    Input tokens include cached input. A cached token is charged once at the
    cache price, not also at the uncached-input price. No current price assumed.
    """
    prices = [input_price, output_price, cache_price, *tool_prices.values()]
    if any(type(p) not in {int, float} or not math.isfinite(p) or p < 0 for p in prices):
        raise ValueError("finite nonnegative prices required")
    if set(calls) - set(tool_prices):
        raise ValueError("every realized tool call needs its own explicit price")
    for value in calls.values():
        _count(value)
    cost = ((usage.input_tokens - usage.cached_input_tokens) * input_price
            + usage.cached_input_tokens * cache_price + usage.output_tokens * output_price
            + sum(count * tool_prices[tool] for tool, count in calls.items()))
    if not math.isfinite(cost):
        raise ValueError("cost overflow")
    return cost


class Verdict(Enum):
    SUCCESS = "SUCCESS"
    CONTINUE = "CONTINUE"
    PIVOT = "PIVOT"


@dataclass
class BATSState:
    question: str
    tracker: BudgetTracker
    summaries: list[str] = field(default_factory=list, init=False)
    trajectory: list[str] = field(default_factory=list, init=False)
    verified_answers: list[str] = field(default_factory=list, init=False)
    last_answer: str | None = field(default=None, init=False)
    attempt: int = field(default=0, init=False)

    def __post_init__(self):
        if not isinstance(self.question, str) or not self.question:
            raise ValueError("public question required; no gold/reference field exists")

    def actor_payload(self) -> dict:
        return {"question": self.question, "budget": self.tracker.snapshot(),
                "summaries": list(self.summaries), "trajectory": list(self.trajectory)}

    def tool_observation(self, tool: str, observation: str) -> None:
        if not isinstance(observation, str):
            raise ValueError("public textual observation required")
        self.tracker.record_call(tool)
        self.trajectory.append(observation)

    def apply_external_verdict(self, answer: str, verdict: Verdict, *, summary: str | None = None,
                               compress_history: bool = False) -> None:
        """Apply, never generate, the semantic verifier's decision.

        SUCCESS/PIVOT start another attempt with the SAME remaining budgets.
        CONTINUE retains the current path, unless an external context-threshold
        check requests compression. An external summary is never synthesized.
        """
        if not self.tracker.active:
            raise ValueError("Appendix B does not begin a new iteration after any budget is exhausted")
        if not isinstance(verdict, Verdict) or not isinstance(answer, str) or not answer:
            raise ValueError("candidate and explicit external verifier enum required")
        needs_summary = verdict in {Verdict.SUCCESS, Verdict.PIVOT} or compress_history
        if needs_summary and (not isinstance(summary, str) or not summary):
            raise ValueError("external summary is required for reset/compression")
        self.last_answer = answer
        if verdict is Verdict.SUCCESS:
            if answer not in self.verified_answers:  # Appendix B uses a set.
                self.verified_answers.append(answer)
        if needs_summary:
            self.summaries.append(summary)
            self.trajectory.clear()
        if verdict in {Verdict.SUCCESS, Verdict.PIVOT}:
            self.attempt += 1

    def final_answer(self, selector=None) -> str | None:
        """External judge selects only from verifier-accepted answers; else last candidate.

        A verifier SUCCESS means accepted by that external module, not correct
        against hidden ground truth. No correctness metric is produced here.
        """
        if self.tracker.active:
            raise ValueError("BATS continues attempting until any tool budget is exhausted")
        if not self.verified_answers:
            return self.last_answer
        if selector is None:
            raise ValueError("a real external answer selector is required; no heuristic majority substitute")
        answer = selector(tuple(self.verified_answers))
        if answer not in self.verified_answers:
            raise ValueError("selector returned an answer outside the verified candidate set")
        return answer


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("BATS state/cost kernel is CPU-only")
    state = BATSState("Public teaching question", BudgetTracker({"search": 3, "browse": 2}))
    state.tool_observation("search", "A public search snippet")
    state.apply_external_verdict("candidate-one", Verdict.PIVOT, summary="External failed-path summary")
    preserved_usage = state.tracker.used["search"] == 1
    state.tool_observation("browse", "A public page excerpt")
    state.apply_external_verdict("candidate-two", Verdict.SUCCESS, summary="External supporting-path summary")
    state.tool_observation("browse", "Last allowed page")
    cost = unified_cost(TokenUsage(100, 20, 40), dict(state.tracker.used),
                        input_price=.002, output_price=.004, cache_price=.0005,
                        tool_prices={"search": .01, "browse": .02})
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"attempts": state.attempt, "verified_candidates": len(state.verified_answers),
                        "search_calls": state.tracker.used["search"], "browse_calls": state.tracker.used["browse"],
                        "unified_cost": cost},
            "checks": {"pivot_preserves_usage": preserved_usage,
                       "resets_clear_raw_trajectory": len(state.summaries) == 2,
                       "any_tool_exhaustion_stops": not state.tracker.active,
                       "external_selector_only": state.final_answer(lambda answers: answers[0]) == "candidate-two",
                       "no_gold_payload": set(state.actor_payload()) == {"question", "budget", "summaries", "trajectory"},
                       "cached_input_not_double_charged": math.isclose(cost, .27)}}
