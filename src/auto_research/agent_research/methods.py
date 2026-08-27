from __future__ import annotations

import numpy as np

from .method_families.base import BaseAgent
from .method_families.planning import LongContextAgent, ReActAgent, ReflexionAgent, VoyagerAgent, TreeOfThoughtsAgent, LATSAgent, ToolformerAgent, SelfRefineAgent, ReWOOAgent, AutoGenAgent, PEARLAgent
from .method_families.memory import UMemAgent, LegoMemAgent, MemToolAgent, MRKLAgent, HuggingGPTAgent, GenerativeAgentsAgent, MemGPTAgent, WebGPTAgent, SayCanAgent, PALAgent, ARTAgent
from .method_families.rl import SEEDAgent, CASTAgent, TurnOPDAgent, SearchR1Agent, RAGENAgent, LOOPAgent, WebAgentR1Agent, MUARLAgent, HiSkillAgent, UniMemAgent, CAMDFAgent, SkillRiseAgent, GiGPOAgent, StepPOAgent, TAPOAgent, GRSDAgent, EnvACEAgent, AgentOPSDAgent, OCSDAgent, VerMemAgent, CoEvoMemAgent


def build_agent(method: str, capacity: int, rng: np.random.Generator) -> BaseAgent:
    from .p0_20260808 import P0_AGENTS
    from .p1_20260808 import P1_AGENTS
    from .latest_20260809 import LATEST_AGENTS
    from .latest_20260813 import LATEST_AGENTS as LATEST_20260813_AGENTS
    from .latest_20260824 import LATEST_AGENTS as LATEST_20260824_AGENTS
    from .latest_20260825 import LATEST_AGENTS as LATEST_20260825_AGENTS
    from .latest_20260826 import LATEST_AGENTS as LATEST_20260826_AGENTS
    from .latest_20260827 import LATEST_AGENTS as LATEST_20260827_AGENTS
    from .historical_b10_b11 import HISTORICAL_AGENTS

    classes = {
        "long-context": LongContextAgent,
        "react": ReActAgent,
        "reflexion": ReflexionAgent,
        "voyager": VoyagerAgent,
        "tree-of-thoughts": TreeOfThoughtsAgent,
        "lats": LATSAgent,
        "toolformer": ToolformerAgent,
        "self-refine": SelfRefineAgent,
        "rewoo": ReWOOAgent,
        "autogen": AutoGenAgent,
        "pearl": PEARLAgent,
        "u-mem": UMemAgent,
        "legomem": LegoMemAgent,
        "memtool": MemToolAgent,
        "mrkl": MRKLAgent,
        "hugginggpt": HuggingGPTAgent,
        "generative-agents": GenerativeAgentsAgent,
        "memgpt": MemGPTAgent,
        "webgpt": WebGPTAgent,
        "saycan": SayCanAgent,
        "pal": PALAgent,
        "art": ARTAgent,
        "seed": SEEDAgent,
        "cast": CASTAgent,
        "turn-opd": TurnOPDAgent,
        "search-r1": SearchR1Agent,
        "ragen": RAGENAgent,
        "loop": LOOPAgent,
        "webagent-r1": WebAgentR1Agent,
        "mua-rl": MUARLAgent,
        "hiskill": HiSkillAgent,
        "unimem": UniMemAgent,
        "cam-df": CAMDFAgent,
        "skillrise": SkillRiseAgent,
        "gigpo": GiGPOAgent,
        "steppo": StepPOAgent,
        "tapo": TAPOAgent,
        "grsd": GRSDAgent,
        "envace": EnvACEAgent,
        "agent-opsd": AgentOPSDAgent,
        "ocsd": OCSDAgent,
        "vermem": VerMemAgent,
        "coevo-mem": CoEvoMemAgent,
        **P0_AGENTS,
        **P1_AGENTS,
        **LATEST_AGENTS,
        **LATEST_20260813_AGENTS,
        **LATEST_20260824_AGENTS,
        **LATEST_20260825_AGENTS,
        **LATEST_20260826_AGENTS,
        **LATEST_20260827_AGENTS,
        **HISTORICAL_AGENTS,
    }
    return classes[method](capacity, rng)
