"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.s_p_o_plus_plus_agent import SPOPlusPlusAgent
from auto_research.agent_research.mechanisms.skill_forge_agent import SkillForgeAgent
from auto_research.agent_research.mechanisms.a_h_e_a_d_agent import AHEADAgent
from auto_research.agent_research.mechanisms.s_m_i_t_h_agent import SMITHAgent

LATEST_AGENTS = {
    "spo-plus-plus": SPOPlusPlusAgent,
    "skillforge": SkillForgeAgent,
    "ahead": AHEADAgent,
    "smith": SMITHAgent,
}
