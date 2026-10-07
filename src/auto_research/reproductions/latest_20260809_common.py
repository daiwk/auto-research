"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.reproductions.mechanisms.reproduce_kgd import (
    _foundation_payload,
    _rec_payload,
    _rng,
    _safe_normalize,
    _transition_scores,
    reproduce_bakron,
    reproduce_dblast,
    reproduce_hilp,
    reproduce_hrpo,
    reproduce_kgd,
    reproduce_llm_ts_prior,
    reproduce_macro,
    reproduce_qevict,
    reproduce_twitch_mor,
)
from auto_research.reproductions.mechanisms.reproduce_dme import (
    _run_industrial,
    reproduce_dme,
    reproduce_spear,
    reproduce_steps,
)
from auto_research.reproductions.mechanisms.generative_slate_report import render_latest
