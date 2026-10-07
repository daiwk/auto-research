"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.sweprime_agent import SWEPrimeAgent
from auto_research.agent_research.mechanisms.harness_lens_agent import HarnessLensAgent
from auto_research.agent_research.mechanisms.co_ve_mem_agent import CoVeMemAgent
from auto_research.agent_research.mechanisms.sptagent import SPTAgent

LATEST_AGENTS = {
    "swe-prime": SWEPrimeAgent,
    "harnesslens": HarnessLensAgent,
    "covemem": CoVeMemAgent,
    "spt": SPTAgent,
}
