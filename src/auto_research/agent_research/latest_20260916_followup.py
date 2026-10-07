"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.repo_atlas_agent import RepoAtlasAgent
from auto_research.agent_research.mechanisms.interactive_memory_agent import InteractiveMemoryAgent

LATEST_AGENTS = {"repoatlas": RepoAtlasAgent, "interactive-memory": InteractiveMemoryAgent}
