"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.post_training.mechanisms.carm_response_mask import carm_response_mask
from auto_research.post_training.mechanisms.group_mass_cap import group_mass_cap
from auto_research.post_training.mechanisms.gradient_aligned_rejected_weights import (
    gradient_aligned_rejected_weights,
)
from auto_research.post_training.mechanisms.sharpo_segment_advantages import (
    sharpo_segment_advantages,
)
from auto_research.post_training.mechanisms.token_level_video_credit import token_level_video_credit
from auto_research.post_training.mechanisms.sharpening_tax import sharpening_tax
from auto_research.post_training.mechanisms.lego_opd_teacher import lego_opd_teacher
from auto_research.post_training.mechanisms.drift_opd_loss import drift_opd_loss
