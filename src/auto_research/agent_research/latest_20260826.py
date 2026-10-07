"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.spoplus_plus_agent import SPOPlusPlusAgent
from auto_research.agent_research.mechanisms.skill_forge_agent import SkillForgeAgent
from auto_research.agent_research.mechanisms.aheadagent import AHEADAgent
from auto_research.agent_research.mechanisms.smithagent import SMITHAgent

LATEST_AGENTS = {
    "spo-plus-plus": SPOPlusPlusAgent,
    "skillforge": SkillForgeAgent,
    "ahead": AHEADAgent,
    "smith": SMITHAgent,
}
