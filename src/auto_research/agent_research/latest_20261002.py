"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.curriculum_arm import CurriculumArm
from auto_research.agent_research.mechanisms.active_saddler_choice import active_saddler_choice
from auto_research.agent_research.mechanisms.safe_self_improvement_select import (
    safe_self_improvement_select,
)
from auto_research.agent_research.mechanisms.veriharness_select import veriharness_select
from auto_research.agent_research.mechanisms.non_destructive_memory import NonDestructiveMemory
from auto_research.agent_research.mechanisms.defa_decisive_error import defa_decisive_error
from auto_research.agent_research.mechanisms.flowright_hierarchical_credit import (
    flowright_hierarchical_credit,
)
