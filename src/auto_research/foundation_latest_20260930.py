"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.mechanisms.leapquant_compress import (
    _symmetric_quantize,
    leapquant_compress,
    leapquant_window,
)
from auto_research.mechanisms.lifetime_weight import lifetime_weight
from auto_research.mechanisms.stepquant_bit_allocation import stepquant_bit_allocation
from auto_research.mechanisms.stepquant_dual_axis import stepquant_dual_axis
from auto_research.mechanisms.chinese_jev_objective import chinese_jev_objective
from auto_research.mechanisms.chinese_jev_head import ChineseJevHead
from auto_research.mechanisms.masked_block_average import (
    MultiScaleGLA,
    causal_hold_upsample,
    fuse_scales,
    gated_linear_recurrence,
    masked_block_average,
)
