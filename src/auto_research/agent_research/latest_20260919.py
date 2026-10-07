"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.evo_skill_g_u_i_agent import EvoSkillGUIAgent
from auto_research.agent_research.mechanisms.dependency_refinement_agent import (
    DependencyRefinementAgent,
)
from auto_research.agent_research.mechanisms.harness_design_study_agent import (
    HarnessDesignStudyAgent,
)
from auto_research.agent_research.mechanisms.ceramo_a_agent import CERAMoAAgent

LATEST_AGENTS = {
    "evoskill-gui": EvoSkillGUIAgent,
    "dependency-refinement": DependencyRefinementAgent,
    "harness-design-study": HarnessDesignStudyAgent,
    "cera-moa": CERAMoAAgent,
}
