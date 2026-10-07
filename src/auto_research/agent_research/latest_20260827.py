"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.jitagent import JITAgent
from auto_research.agent_research.mechanisms.trace_m_l_agent import TraceMLAgent
from auto_research.agent_research.mechanisms.ada_v_d_r_agent import AdaVDRAgent
from auto_research.agent_research.mechanisms.topasagent import TOPASAgent
from auto_research.agent_research.mechanisms.ca_s_k_g_agent import CaSKGAgent
from auto_research.agent_research.mechanisms.prog_router_agent import ProgRouterAgent

LATEST_AGENTS = {
    "jit-agent": JITAgent,
    "traceml": TraceMLAgent,
    "adavdr": AdaVDRAgent,
    "topas": TOPASAgent,
    "caskg": CaSKGAgent,
    "progrouter": ProgRouterAgent,
}
