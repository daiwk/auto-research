"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.post_training.mechanisms.tiao_credit import (
    style_debiased_dpo,
    tiao_credit,
    update_latest,
)
from auto_research.post_training.mechanisms.tiao_cuda_kernel import tiao_cuda_kernel
