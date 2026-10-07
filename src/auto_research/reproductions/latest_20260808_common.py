"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.reproductions.mechanisms.gryphon_v2_family import (
    Config,
    _model,
    _score,
    _train_degr,
    _train_gryphon,
    _train_teacher,
    reproduce_degr,
    reproduce_gryphon_v2,
)
from auto_research.reproductions.mechanisms.compressed_sequence_report import render_latest
