"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.post_training.mechanisms.dependency_shaped_rewards import (
    dependency_shaped_rewards,
)
from auto_research.post_training.mechanisms.range_grpo_advantages import range_grpo_advantages
from auto_research.post_training.mechanisms.fault_terminal_redistribution import (
    fault_terminal_redistribution,
)
from auto_research.post_training.mechanisms.where_opd_loss import where_opd_loss
