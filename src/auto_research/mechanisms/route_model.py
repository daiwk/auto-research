"""Extracted unchanged from auto_research.foundation_latest_20260914; stable mechanism boundary."""
from __future__ import annotations

import re

def route_model(query: str, windows: list[list[str]], model_profiles: dict[str, set[str]]) -> tuple[str, dict[str, float]]:
    tokens = set(re.findall(r"[a-z0-9]+", (query + " " + " ".join(windows[-1])).lower()))
    scores = {
        name: len(tokens & profile) / max(1, len(tokens | profile))
        for name, profile in model_profiles.items()
    }
    return max(scores, key=scores.get), scores
