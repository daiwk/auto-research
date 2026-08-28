from __future__ import annotations

from dataclasses import replace
import random

from auto_research.evolution.models import Genome
from auto_research.evolution.planner import propose


def test_dceo_evolve_mutates_causal_calibration():
    base = Genome(architecture="rankmixer_dceo")
    candidates = [
        propose(base, 1, index, ["rankmixer_dceo"], random.Random(42))[0]
        for index in range(6)
    ]
    assert len({row.dceo_causal_gain for row in candidates}) > 1
    assert len({row.dceo_temperature for row in candidates}) > 1
    assert replace(base, dceo_causal_gain=0.1) != replace(base, dceo_causal_gain=0.75)
