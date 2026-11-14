"""CPU-only replay of EnvOpt Algorithm 1's acceptance and rollback rules."""

from dataclasses import dataclass
import math
import random


REQUIRES_GPU_VALIDATION = False


def _number(value: float, name: str, *, upper: float | None = None) -> None:
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite nonnegative number")
    if upper is not None and value > upper:
        raise ValueError(f"{name} must not exceed {upper}")


def _identifier(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty identifier")


@dataclass(frozen=True)
class Trial:
    """One candidate, assessed on a training shard without its verifier."""

    environment: str
    harness: str
    cost: float
    proxy_preserved: bool

    def __post_init__(self) -> None:
        _identifier(self.environment, "environment")
        _identifier(self.harness, "harness")
        _number(self.cost, "training cost")
        if type(self.proxy_preserved) is not bool:
            raise ValueError("proxy preservation must be an explicit bool")


@dataclass(frozen=True)
class Validation:
    """Host-produced aggregates on the fixed validation tasks, not test data."""

    environment: str
    cost: float
    accuracy: float

    def __post_init__(self) -> None:
        _identifier(self.environment, "environment")
        _number(self.cost, "validation cost")
        _number(self.accuracy, "validation accuracy", upper=1)


@dataclass(frozen=True)
class Step:
    tasks: tuple[str, ...]
    start_environment: str
    start_cost: float
    trials: tuple[Trial, ...]
    validation: Validation


@dataclass(frozen=True)
class Replay:
    retained: Validation
    accepted_steps: int
    accepted_trials: int
    rollback_step: int | None


def _task_set(tasks: tuple[str, ...]) -> set[str]:
    if not isinstance(tasks, tuple) or not tasks:
        raise ValueError("task IDs must be a nonempty tuple")
    for task in tasks:
        _identifier(task, "task")
    if len(set(tasks)) != len(tasks):
        raise ValueError("duplicate task in a split")
    return set(tasks)


def select_training_environment(
    environment: str, harness: str, cost: float, trials: tuple[Trial, ...]
) -> tuple[str, int]:
    """Replay the inner rule with no validation, test or gold-answer inputs."""
    _identifier(environment, "environment")
    _identifier(harness, "harness")
    _number(cost, "initial training cost")
    accepted = 0
    for trial in trials:
        if not isinstance(trial, Trial) or trial.harness != harness:
            raise ValueError("candidate must use the fixed target harness")
        if trial.cost < cost and trial.proxy_preserved:
            environment, cost = trial.environment, trial.cost
            accepted += 1
    return environment, accepted


def replay_environment_evolution(
    baseline: Validation,
    validation_tasks: tuple[str, ...],
    harness: str,
    steps: tuple[Step, ...],
    *,
    tolerance: float,
) -> Replay:
    """Replay decisions on completed, budget-bounded records; never execute an agent."""
    _number(tolerance, "accuracy tolerance", upper=1)
    _identifier(harness, "harness")
    if not isinstance(baseline, Validation):
        raise ValueError("missing initial validation measurement")
    reserved = _task_set(validation_tasks)
    retained = baseline
    accepted_trials = 0
    for index, step in enumerate(steps, start=1):
        tasks = _task_set(step.tasks)
        if reserved & tasks:
            raise ValueError("training shards must be disjoint from each other and validation")
        reserved.update(tasks)
        if step.start_environment != retained.environment:
            raise ValueError("training baseline must be the last retained environment")
        winner, accepted = select_training_environment(
            retained.environment, harness, step.start_cost, step.trials
        )
        if not isinstance(step.validation, Validation) or step.validation.environment != winner:
            raise ValueError("validation must measure the training-selected environment")
        accepted_trials += accepted
        if (
            step.validation.cost > retained.cost
            or step.validation.accuracy < retained.accuracy - tolerance
        ):
            return Replay(retained, index - 1, accepted_trials, index)
        retained = step.validation
    return Replay(retained, len(steps), accepted_trials, None)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("EnvOpt replay is a CPU-only seeded diagnostic")
    saving = random.Random(seed).randint(1, 3)
    baseline = Validation("initial", 10, 0.875)
    first = Step(
        ("train-a",),
        "initial",
        9,
        (
            Trial("indexed", "fixed", 8, True),
            Trial("cheap-but-unreliable", "fixed", 1, False),
            Trial("ties", "fixed", 8, True),
        ),
        Validation("indexed", 10 - saving, 0.875),
    )
    second = Step(
        ("train-b",),
        "indexed",
        8,
        (Trial("overfitted", "fixed", 1, True),),
        Validation("overfitted", 1, 0.5),
    )
    result = replay_environment_evolution(
        baseline, ("validation-a",), "fixed", (first, second), tolerance=0.125
    )
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "retained_validation_cost": result.retained.cost,
            "accepted_training_trials": result.accepted_trials,
            "retained_steps": result.accepted_steps,
            "rollback_step": result.rollback_step,
        },
        "checks": {
            "strict_saving_and_proxy_filter": select_training_environment(
                "initial", "fixed", first.start_cost, first.trials
            ) == ("indexed", 1),
            "validation_rollback": result.retained == first.validation,
            "stop_on_first_regression": result.rollback_step == 2 and result.accepted_steps == 1,
        },
    }
