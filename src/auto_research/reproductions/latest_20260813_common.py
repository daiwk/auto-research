"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.reproductions.mechanisms.metastrategy_family import (
    Config,
    _score_strategy,
    _sona_model,
    _strategy_model,
    _train_sona,
    _train_strategy,
    reproduce_metastrategy,
    reproduce_sona,
)
from auto_research.reproductions.mechanisms.strategy_semantic_report import render_latest
