"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.procedural_graph_agent import ProceduralGraphAgent
from auto_research.agent_research.mechanisms.event_tree import EventTree, MemForestAgent
from auto_research.agent_research.mechanisms.feedback_scaffold_agent import FeedbackScaffoldAgent
from auto_research.agent_research.mechanisms.mapleagent import MAPLEAgent

LATEST_AGENTS = {
    "procedural-graphs": ProceduralGraphAgent,
    "memforest": MemForestAgent,
    "feedback-scaffold": FeedbackScaffoldAgent,
    "maple": MAPLEAgent,
}
