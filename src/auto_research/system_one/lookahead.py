"""Code simulation + Jev evaluation from arXiv:2610.01834, Section 5.3."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .contracts import ChoiceQuestion, SystemOneRequest


class ForkableTextEnvironment(Protocol):
    def fork(self) -> "ForkableTextEnvironment": ...
    def admissible_commands(self) -> tuple[str, ...]: ...
    def step(self, command: str) -> str: ...


@dataclass(frozen=True)
class SimulatedOption:
    command: str
    observation: str
    newly_possible: tuple[str, ...]


def simulate_options(environment: ForkableTextEnvironment) -> tuple[SimulatedOption, ...]:
    """Execute each admissible action in its own copy, without reading rewards."""
    commands = tuple(environment.admissible_commands())
    if not commands or len(set(commands)) != len(commands):
        raise ValueError("admissible commands must be nonempty and unique")
    options = []
    for command in commands:
        branch = environment.fork()
        if branch is environment:
            raise ValueError("fork must isolate environment state")
        observation = branch.step(command)
        if not isinstance(observation, str):
            raise TypeError("step must return observable text, not reward/gold metadata")
        new = tuple(c for c in branch.admissible_commands() if c not in commands)
        options.append(SimulatedOption(command, observation, new))
    return tuple(options)


def choose_with_lookahead(
    environment,
    provider,
    *,
    task: str,
    observation: str,
    history: tuple[str, ...] = (),
    model: str = "jev-latest",
):
    """Provider can be TypeSafe, NanoJev, Nimble or another existing backend.

    Only observable successor descriptions enter the provider request. The
    selected command is returned; executing it on the real environment is caller-owned.
    """
    options = simulate_options(environment)
    if len(options) == 1:
        return options[0].command, options
    criteria = {
        str(i): {
            "command": option.command,
            "next observation": option.observation,
            "then newly possible": list(option.newly_possible),
        }
        for i, option in enumerate(options)
    }
    request = SystemOneRequest(
        state={"task": task, "observation": observation, "history": list(history)},
        questions={
            "action": ChoiceQuestion(
                "Choose the action whose predicted outcome advances the task.", criteria
            )
        },
        model=model,
    )
    answer = provider.decide(request).answers["action"]
    key = str(answer.value)
    if key not in criteria:
        raise ValueError("provider selected an inadmissible command")
    return options[int(key)].command, options
