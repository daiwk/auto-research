"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.fuse_evaluator_agent import FuseEvaluatorAgent
from auto_research.agent_research.mechanisms.harness_bandit_agent import HarnessBanditAgent
from auto_research.agent_research.mechanisms.science_buddy_agent import ScienceBuddyAgent

LATEST_AGENTS = {
    "fuse-evaluator": FuseEvaluatorAgent,
    "harness-bandit": HarnessBanditAgent,
    "sciencebuddy": ScienceBuddyAgent,
}
