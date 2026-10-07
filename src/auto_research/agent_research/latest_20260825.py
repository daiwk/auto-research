"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.agent_g2_agent import AgentG2Agent
from auto_research.agent_research.mechanisms.auto_saddler_agent import AutoSaddlerAgent

LATEST_AGENTS = {"agent-g2": AgentG2Agent, "autosaddler": AutoSaddlerAgent}
