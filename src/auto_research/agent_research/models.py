from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


METHODS = (
    "long-context",
    "react",
    "reflexion",
    "voyager",
    "tree-of-thoughts",
    "lats",
    "toolformer",
    "self-refine",
    "rewoo",
    "autogen",
    "pearl",
    "u-mem",
    "legomem",
    "memtool",
    "mrkl",
    "hugginggpt",
    "generative-agents",
    "memgpt",
    "webgpt",
    "saycan",
    "pal",
    "art",
    "metagpt",
    "critic",
    "agent-lightning",
    "swe-agent",
    "openhands",
    "seed",
    "cast",
    "turn-opd",
    "search-r1",
    "ragen",
    "loop",
    "webagent-r1",
    "mua-rl",
    "hiskill",
    "unimem",
    "cam-df",
    "skillrise",
)
BENCHMARKS = (
    "evomem-mini", "planbench-mini", "scalemcp-mini", "swebench-local",
)


@dataclass(frozen=True)
class AgentResearchConfig:
    method: str
    benchmark: str = "evomem-mini"
    episodes: int = 120
    memory_size: int = 24
    seed: int = 42
    output_dir: Path = Path("runs/agent-research")

    def __post_init__(self) -> None:
        if self.method not in METHODS:
            raise ValueError(f"method must be one of {', '.join(METHODS)}")
        if self.benchmark not in BENCHMARKS:
            raise ValueError(f"benchmark must be one of {', '.join(BENCHMARKS)}")
        if self.episodes < 12 or self.memory_size < 2:
            raise ValueError("episodes must be >= 12 and memory-size must be >= 2")


@dataclass(frozen=True)
class AgentTask:
    task_id: str
    axis: str
    intent: str
    context: tuple[str, ...]
    answer: str
    plan: tuple[str, ...]
    required_tools: tuple[str, ...]


@dataclass
class AgentResearchResult:
    method: str
    benchmark: str
    metrics: dict[str, float]
    axis_metrics: dict[str, float]
    diagnostics: dict[str, Any]
    trace: list[dict[str, Any]] = field(default_factory=list)
