"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.agent_research.mechanisms.evo_harness_r_l_agent import EvoHarnessRLAgent
from auto_research.agent_research.mechanisms.va_g_agent import VaGAgent
from auto_research.agent_research.mechanisms.g_s_e_agent import GSEAgent
from auto_research.agent_research.mechanisms.c_i_p_o_agent import CIPOAgent
from auto_research.agent_research.mechanisms.state2_state_agent import State2StateAgent
from auto_research.agent_research.mechanisms.harness_opt_bench_agent import HarnessOptBenchAgent
from auto_research.agent_research.mechanisms.code_grep_agent import CodeGrepAgent
from auto_research.agent_research.mechanisms.memory_c_p_t_agent import MemoryCPTAgent
from auto_research.agent_research.mechanisms.hind_search_agent import HindSearchAgent

LATEST_AGENTS = {
    "evoharness-rl": EvoHarnessRLAgent,
    "vag": VaGAgent,
    "gse": GSEAgent,
    "cipo": CIPOAgent,
    "state2state": State2StateAgent,
    "harnessopt-bench": HarnessOptBenchAgent,
    "codegrep": CodeGrepAgent,
    "memorycpt": MemoryCPTAgent,
    "hindsearch": HindSearchAgent,
}
