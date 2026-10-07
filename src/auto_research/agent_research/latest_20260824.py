"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.action_information import AUSOAgent, action_information
from auto_research.agent_research.mechanisms.agent_x_agent import AgentXAgent

LATEST_AGENTS = {"auso": AUSOAgent, "agentx": AgentXAgent}
