"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.reproductions.mechanisms.ccformer_family import (
    Config,
    _run_pair,
    _scores,
    _sequence_model,
    _train,
    reproduce_ccformer,
    reproduce_open_web_ufm,
    reproduce_rocs,
)
from auto_research.reproductions.mechanisms.reward_alignment_report import render_latest
