"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import (
    AtomRecAgent,
    CoSkillAgent,
    MultiHarnessRLAgent,
    ObservationAgent,
    PublicObservation,
    SiLRAgent,
    read_evidence,
)

LATEST_AGENTS = {
    "atomrec": AtomRecAgent,
    "coskill": CoSkillAgent,
    "silr": SiLRAgent,
    "multi-harness-rl": MultiHarnessRLAgent,
}
