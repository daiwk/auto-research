from __future__ import annotations

import numpy as np

from .models import AgentTask


TOOLS = (
    "search", "calculator", "calendar", "maps", "weather", "mail",
    "database", "spreadsheet", "code", "browser", "files", "terminal",
)
DOMAINS = ("travel", "finance", "research", "ops", "shopping", "support")


def build_benchmark(name: str, episodes: int, seed: int) -> tuple[AgentTask, ...]:
    rng = np.random.default_rng(seed)
    tasks = []
    for index in range(episodes):
        domain = DOMAINS[index % len(DOMAINS)]
        if name == "gaia-mini":
            axis = ("level-1", "level-2", "level-3")[index % 3]
        elif name == "planbench-mini":
            axis = "cross_episode_execution"
        elif name == "scalemcp-mini":
            axis = "in_episode_execution" if index % 2 else "cross_episode_execution"
        else:
            axis = (
                "in_episode_knowledge", "cross_episode_knowledge",
                "in_episode_execution", "cross_episode_execution",
            )[index % 4]
        depth = (2 + index % 3) if name != "gaia-mini" else (2 + index % 4)
        required = tuple(
            TOOLS[(index * 3 + offset * 5) % len(TOOLS)] for offset in range(depth)
        )
        plan = tuple(f"{tool}:{domain}" for tool in required)
        nonce = int(rng.integers(100, 999))
        answer = f"{domain}-{nonce % 17}"
        distractors = tuple(
            f"{DOMAINS[(index + offset + 1) % len(DOMAINS)]}-{int(rng.integers(0, 17))}"
            for offset in range(3)
        )
        context = (
            f"{domain} case {nonce} resolves to {answer}",
            *distractors,
            f"workflow {' -> '.join(plan)}",
        )
        # Repeated families make cross-episode procedural reuse measurable.
        family = index % max(3, episodes // 10)
        tasks.append(
            AgentTask(
                task_id=f"{name}-{index:04d}",
                axis=axis,
                intent=f"{domain} family-{family}",
                context=context,
                answer=answer,
                plan=plan,
                required_tools=required,
            )
        )
    return tuple(tasks)
