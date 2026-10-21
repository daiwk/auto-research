"""Agent S4 population control and asymmetric-feedback contracts (2610.28601v1).

Implements the paper's control plane, not its LLM builder, GUI execution,
virtual machines or benchmark. Callbacks are trusted Python, not a sandbox.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from pathlib import PurePosixPath
import random
from typing import Callable


def _text(value: str) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError("nonempty plain text required")
    return value


@dataclass(frozen=True)
class Repository:
    """Immutable repository content; this module never execs its source text."""

    files: tuple[tuple[str, str], ...]
    knowledge: tuple[str, ...] = ()

    def __post_init__(self):
        if type(self.files) is not tuple or not self.files or len(self.files) > 64:
            raise ValueError("one to 64 immutable source files required")
        names = []
        for item in self.files:
            if type(item) is not tuple or len(item) != 2:
                raise ValueError("file name and source pairs required")
            name, source = item
            _text(name)
            _text(source)
            if (PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts
                    or "\\" in name or name != str(PurePosixPath(name))):
                raise ValueError("normalized relative repository paths required")
            names.append(name)
        if len(set(names)) != len(names):
            raise ValueError("duplicate repository file")
        if type(self.knowledge) is not tuple:
            raise ValueError("immutable knowledge tuple required")
        for note in self.knowledge:
            _text(note)

    @property
    def digest(self) -> str:
        # Length framing makes embedded separators unambiguous.
        fields = [value for item in sorted(self.files) for value in item] + list(self.knowledge)
        encoded = b"".join(len(value.encode()).to_bytes(8, "big") + value.encode() for value in fields)
        return hashlib.sha256(encoded).hexdigest()


def _repository(value: Repository) -> Repository:
    if type(value) is not Repository:
        raise ValueError("exact Repository required")
    # Drop any dynamically attached caller metadata, including gold/score fields.
    return Repository(tuple((name, source) for name, source in value.files), tuple(value.knowledge))


@dataclass(frozen=True)
class PublicTask:
    task_id: str
    instruction: str

    def __post_init__(self):
        _text(self.task_id)
        _text(self.instruction)


@dataclass(frozen=True)
class PublicTrajectory:
    task_id: str
    events: tuple[str, ...]
    final_output: str

    def __post_init__(self):
        _text(self.task_id)
        if type(self.events) is not tuple or any(type(event) is not str for event in self.events):
            raise ValueError("plain public event strings required")
        if type(self.final_output) is not str:
            raise ValueError("plain final output required")


@dataclass(frozen=True)
class Lineage:
    variant_id: str
    parent_ids: tuple[str, ...]
    operator: str


@dataclass(frozen=True)
class ParentExperience:
    variant_id: str
    repository: Repository
    training_trajectories: tuple[PublicTrajectory, ...]


@dataclass(frozen=True)
class BuilderContext:
    operator: str
    parents: tuple[ParentExperience, ...]
    lineage: tuple[Lineage, ...]


@dataclass(frozen=True)
class SelectionSummary:
    """Controller-side audit only; never part of BuilderContext."""

    variant_id: str
    mean_validation: float
    full_success_rate: float
    evaluation_rounds: int
    parent_eligible: bool


@dataclass
class _Variant:
    repository: Repository
    training: tuple[PublicTrajectory, ...]
    validation_rounds: list[tuple[float, ...]]
    eligible: bool = True


TaskAgent = Callable[[Repository, PublicTask], PublicTrajectory]
ValidationGrader = Callable[[PublicTask, PublicTrajectory], float]
Builder = Callable[[BuilderContext], Repository]


class Population:
    """Algorithm 1: seed, tournament, mutation/crossover, evaluate, retain.

    Training has no grader calls. Validation data/scores/trajectories do not
    enter the builder view. Parent IDs necessarily convey indirect selection
    information, as in the paper. No test-set evaluation is performed here.
    """

    def __init__(self, seed_repository: Repository, *, training_tasks: tuple[PublicTask, ...],
                 validation_tasks: tuple[PublicTask, ...], task_agent: TaskAgent,
                 validation_grader: ValidationGrader, seed: int = 42,
                 benchmark: str = "osworld_v2"):
        if type(seed) is not int or not 0 <= seed < 2**32:
            raise ValueError("uint32 seed required")
        if benchmark not in ("osworld_v2", "scienceboard"):
            raise ValueError("supported benchmark score contract required")
        self._train = self._tasks(training_tasks)
        self._validation = self._tasks(validation_tasks)
        if {t.task_id for t in self._train} & {t.task_id for t in self._validation}:
            raise ValueError("training and validation task IDs must be disjoint")
        if not callable(task_agent) or not callable(validation_grader):
            raise ValueError("trusted task agent and private validation grader required")
        self._agent, self._grader = task_agent, validation_grader
        self._rng, self.benchmark = random.Random(seed), benchmark
        self._variants: dict[str, _Variant] = {}
        self._lineage: list[Lineage] = []
        repository = _repository(seed_repository)
        training, scores = self._evaluate(repository)
        self._variants["v0"] = _Variant(repository, training, [scores])
        self._lineage.append(Lineage("v0", (), "seed"))

    @staticmethod
    def _tasks(tasks):
        if type(tasks) is not tuple or not tasks or any(type(task) is not PublicTask for task in tasks):
            raise ValueError("nonempty immutable public-task tuple required")
        cloned = tuple(PublicTask(task.task_id, task.instruction) for task in tasks)
        if len({task.task_id for task in cloned}) != len(cloned):
            raise ValueError("duplicate task ID")
        return cloned

    def _rollout(self, repository, task):
        result = self._agent(_repository(repository), PublicTask(task.task_id, task.instruction))
        if type(result) is not PublicTrajectory or result.task_id != task.task_id:
            raise ValueError("task agent must return its exact public trajectory type and ID")
        return PublicTrajectory(result.task_id, tuple(result.events), result.final_output)

    def _validation_scores(self, repository):
        scores = []
        for task in self._validation:
            trajectory = self._rollout(repository, task)
            score = self._grader(PublicTask(task.task_id, task.instruction), trajectory)
            if type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1:
                raise ValueError("finite validation score in [0, 1] required; missing is not zero")
            score = float(score)
            if self.benchmark == "scienceboard" and score not in (0., 1.):
                raise ValueError("ScienceBoard requires binary success scores")
            scores.append(1. if math.isclose(score, 1., rel_tol=0., abs_tol=1e-12) else score)
        return tuple(scores)

    def _evaluate(self, repository):
        training = tuple(self._rollout(repository, task) for task in self._train)
        return training, self._validation_scores(repository)

    def _summary(self, key):
        variant = self._variants[key]
        values = tuple(value for scores in variant.validation_rounds for value in scores)
        return SelectionSummary(key, sum(values) / len(values),
            sum(value == 1. for value in values) / len(values),
            len(variant.validation_rounds), variant.eligible)

    @property
    def summaries(self) -> tuple[SelectionSummary, ...]:
        return tuple(self._summary(key) for key in self._variants)

    @property
    def lineage(self) -> tuple[Lineage, ...]:
        return tuple(Lineage(item.variant_id, tuple(item.parent_ids), item.operator) for item in self._lineage)

    def _tournament(self, exclude=()):
        eligible = [key for key, variant in self._variants.items() if variant.eligible and key not in exclude]
        if not eligible:
            raise ValueError("no eligible parent")
        if len(eligible) == 1:
            return eligible[0]
        a, b = self._rng.sample(eligible, 2)
        sa, sb = self._summary(a).mean_validation, self._summary(b).mean_validation
        return a if sa > sb else b if sb > sa else self._rng.choice((a, b))

    def advance(self, builder: Builder, *, operator: str | None = None) -> str:
        if not callable(builder):
            raise ValueError("trusted builder callback required")
        if operator is None:
            operator = "mutation" if len(self._lineage) % 2 else "crossover"
        if operator not in ("mutation", "crossover"):
            raise ValueError("mutation or crossover required")
        if operator == "crossover" and sum(v.eligible for v in self._variants.values()) < 2:
            raise ValueError("crossover requires two distinct eligible parents")
        first = self._tournament()
        parents = (first,) if operator == "mutation" else (first, self._tournament((first,)))
        experience = tuple(ParentExperience(key, _repository(self._variants[key].repository),
            tuple(PublicTrajectory(t.task_id, tuple(t.events), t.final_output)
                  for t in self._variants[key].training)) for key in parents)
        context = BuilderContext(operator, experience, self.lineage)
        repository = _repository(builder(context))
        training, scores = self._evaluate(repository)
        key = f"v{len(self._lineage)}"
        # Retain even a lower-scoring descendant. Failures above do not mutate population.
        self._variants[key] = _Variant(repository, training, [scores])
        self._lineage.append(Lineage(key, parents, operator))
        return key

    def prune_lowest(self, count: int) -> tuple[str, ...]:
        if type(count) is not int or count < 0:
            raise ValueError("nonnegative prune count required")
        eligible = [key for key, variant in self._variants.items() if variant.eligible]
        # Paper/upstream keep the population when the request would remove all parents.
        if count >= len(eligible):
            return ()
        ranked = sorted(eligible, key=lambda key: (self._summary(key).mean_validation, key))
        removed = tuple(ranked[:count])
        for key in removed:
            self._variants[key].eligible = False
        return removed

    def denoise_top(self, count: int = 3) -> tuple[str, ...]:
        if type(count) is not int or count < 1:
            raise ValueError("positive leader count required")
        ranked = sorted((key for key, value in self._variants.items() if value.eligible),
            key=lambda key: (-self._summary(key).mean_validation, key))[:count]
        # Pin leaders first and commit all results only after every evaluation succeeds.
        staged = [(key, self._validation_scores(self._variants[key].repository)) for key in ranked]
        for key, scores in staged:
            self._variants[key].validation_rounds.append(scores)
        return tuple(ranked)

    def selected(self) -> tuple[str, Repository]:
        # Pruning disables parent selection, not a frozen candidate's eligibility
        # for the final paper-specific criterion over the recorded population.
        recorded = list(self._variants)
        if self.benchmark == "osworld_v2":
            key = max(recorded, key=lambda item: (self._summary(item).full_success_rate,
                self._summary(item).mean_validation))
        else:
            key = max(recorded, key=lambda item: self._summary(item).mean_validation)
        return key, _repository(self._variants[key].repository)
