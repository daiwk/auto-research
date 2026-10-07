"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.sink_window_indices import (
    SinkFlexRLAgent,
    sink_window_indices,
)

LATEST_AGENTS = {"sinkflex-rl": SinkFlexRLAgent}
