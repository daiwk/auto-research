"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.cobraskills_agent import COBRASkillsAgent
from auto_research.agent_research.mechanisms.ecdysis_agent import EcdysisAgent
from auto_research.agent_research.mechanisms.grounded_memory_agent import GroundedMemoryAgent
from auto_research.agent_research.mechanisms.tool_grad_agent import ToolGradAgent
from auto_research.agent_research.mechanisms.promptsagent import PROMPTSAgent
from auto_research.agent_research.mechanisms.search_atlas_agent import SearchAtlasAgent
from auto_research.agent_research.mechanisms.skill_retention_agent import SkillRetentionAgent
from auto_research.agent_research.mechanisms.t1_terminal_agent import T1TerminalAgent

LATEST_AGENTS = {
    "cobra-skills": COBRASkillsAgent,
    "ecdysis": EcdysisAgent,
    "grounded-memory": GroundedMemoryAgent,
    "toolgrad": ToolGradAgent,
    "prompts": PROMPTSAgent,
    "searchatlas": SearchAtlasAgent,
    "skill-retention": SkillRetentionAgent,
    "t1-terminal-rl": T1TerminalAgent,
}
