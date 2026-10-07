"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.mechanisms.quantized_block import (
    QuantizedBlock,
    dequantize_blocks,
    windowed_key_quantize,
)
from auto_research.mechanisms.modality_value_rotate import modality_value_rotate
from auto_research.mechanisms.sensenova_patch_targets import sensenova_patch_targets
from auto_research.mechanisms.multi_expert_opd import multi_expert_opd
from auto_research.mechanisms.frames_on_demand import frames_on_demand
from auto_research.mechanisms.repetition_regularization import repetition_regularization
from auto_research.mechanisms.soft_musec_update import soft_musec_update
from auto_research.mechanisms.similarity_contracting_windows import similarity_contracting_windows
from auto_research.mechanisms.route_model import route_model
