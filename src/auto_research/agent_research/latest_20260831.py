"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.red_evo_agent import RedEvoAgent
from auto_research.agent_research.mechanisms.a_c_e_data_agent import ACEDataAgent
from auto_research.agent_research.mechanisms.deep_repro_agent import DeepReproAgent

LATEST_AGENTS = {
    "redevoagent": RedEvoAgent,
    "ace-data": ACEDataAgent,
    "deeprepro": DeepReproAgent,
}
