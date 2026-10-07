"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.auto_view_mem_agent import AutoViewMemAgent
from auto_research.agent_research.mechanisms.m_a_c_e_agent import MACEAgent
from auto_research.agent_research.mechanisms.arena_flow_agent import ArenaFlowAgent
from auto_research.agent_research.mechanisms.graph_skill_evo_agent import GraphSkillEvoAgent

LATEST_AGENTS = {
    "autoviewmem": AutoViewMemAgent,
    "mace": MACEAgent,
    "arenaflow": ArenaFlowAgent,
    "graphskillevo": GraphSkillEvoAgent,
}
