"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.post_training.mechanisms.rfpo_advantages import rfpo_advantages
from auto_research.post_training.mechanisms.olive_loss import olive_loss
from auto_research.post_training.mechanisms.ross_selective_loss import ross_selective_loss
from auto_research.post_training.mechanisms.reward_aligned_weights import reward_aligned_weights
from auto_research.post_training.mechanisms.mas_role_advantage import mas_role_advantage
from auto_research.post_training.mechanisms.mas_privileged_coordination import (
    mas_privileged_coordination,
)
