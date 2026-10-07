"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.transition import Transition, graphhca_credit
from auto_research.agent_research.mechanisms.harness_proposer import HarnessProposer, adapt_harness
from auto_research.agent_research.mechanisms.time_evolving_memory import time_evolving_memory
from auto_research.agent_research.mechanisms.multi_memory_grpo_objective import (
    multi_memory_grpo_objective,
)
from auto_research.agent_research.mechanisms.video_rsi_accept import video_rsi_accept
