"""Bounded Simula taxonomy/generation/critic and complexity calibration protocol.

All semantic operations are external model callbacks; no keyword heuristic is
silently substituted for reasoning. Fixed callbacks in unit demos are L0 only.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from dataclasses import dataclass, field
from statistics import mean
from typing import Callable, Mapping, Sequence


@dataclass
class CallBudget:
    max_calls: int = 100
    trace: list[dict] = field(default_factory=list)

    def call(self, role: str, callback: Callable, *args):
        if self.max_calls < 1 or len(self.trace) >= self.max_calls:
            raise RuntimeError("Simula model-call budget exhausted")
        digest = hashlib.sha256(json.dumps(args, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()
        record = {"role": role, "input_sha256": digest, "status": "started"}
        self.trace.append(record)
        try:
            result = callback(*args)
        except Exception as error:
            record.update(status="failed", error_type=type(error).__name__)
            raise
        record.update(status="completed", output_sha256=hashlib.sha256(json.dumps(result, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest())
        return result


@dataclass(frozen=True)
class NodeContext:
    instructions: str
    path: tuple[str, ...]
    siblings: tuple[str, ...]
    plan: str


@dataclass(frozen=True)
class Taxonomy:
    factor: str
    # Paths include their factor root. A tree uses unique paths, not globally
    # unique labels: repeated labels in different branches are permissible.
    leaves: tuple[tuple[str, ...], ...]

    def __post_init__(self) -> None:
        if not self.factor or not self.leaves or len(set(self.leaves)) != len(self.leaves):
            raise ValueError("nonempty taxonomy and unique leaf paths required")
        if any(not path or path[0] != self.factor or any(not part.strip() for part in path) for path in self.leaves):
            raise ValueError("taxonomy paths must start at their factor")
        if any(left != right and right[: len(left)] == left for left in self.leaves for right in self.leaves):
            raise ValueError("a leaf cannot also be an ancestor of another leaf")


@dataclass(frozen=True)
class TaxonomyModels:
    factors: Callable[[str], Sequence[str]]
    propose: Callable[[NodeContext], Sequence[str]]
    critic: Callable[[NodeContext, tuple[str, ...]], Sequence[str]]
    plan: Callable[[str, tuple[tuple[str, ...], ...]], str]


def build_taxonomies(
    instructions: str, models: TaxonomyModels, budget: CallBudget,
    *, depth: int = 2, proposals: int = 2, max_children: int = 8, max_nodes: int = 64,
) -> tuple[Taxonomy, ...]:
    """Appendix B.4: breadth-first best-of-N, independent critic, per-level plan."""
    if not instructions.strip() or not 1 <= depth <= 4 or not 1 <= proposals <= 4:
        raise ValueError("bounded nonempty taxonomy request required")
    if not 1 <= max_children <= 16 or max_nodes < 1:
        raise ValueError("positive tree budgets required")
    factors = tuple(budget.call("factor_identification", models.factors, instructions))
    if not factors or len(set(factors)) != len(factors) or any(not factor.strip() for factor in factors):
        raise ValueError("model must return unique nonempty factors")
    total_nodes, taxonomies = len(factors), []
    if total_nodes > max_nodes:
        raise ValueError("factor list exceeds node budget")
    for factor in factors:
        frontier = ((factor,),)
        plan = f"Expand the factor {factor} under the supplied instructions."
        for level in range(depth):
            next_frontier = []
            for path in frontier:
                siblings = tuple(other[-1] for other in frontier if other[:-1] == path[:-1] and other != path)
                context = NodeContext(instructions, path, siblings, plan)
                raw = tuple(dict.fromkeys(child for _ in range(proposals) for child in budget.call("taxonomy_proposal", models.propose, context)))
                refined = tuple(budget.call("taxonomy_critic", models.critic, context, raw))
                if not refined or len(refined) > max_children or len(set(refined)) != len(refined) or any(not child.strip() for child in refined):
                    raise ValueError("critic returned invalid/budget-exceeding children")
                total_nodes += len(refined)
                if total_nodes > max_nodes:
                    raise ValueError("taxonomy node budget exceeded")
                next_frontier.extend((*path, child) for child in refined)
            frontier = tuple(next_frontier)
            if level + 1 < depth:
                plan = budget.call("taxonomy_level_plan", models.plan, instructions, frontier)
                if not isinstance(plan, str) or not plan.strip():
                    raise ValueError("model level plan must be nonempty")
        taxonomies.append(Taxonomy(factor, frontier))
    return tuple(taxonomies)


@dataclass(frozen=True)
class Strategy:
    name: str
    factors: tuple[str, ...]
    weight: float


@dataclass(frozen=True)
class Critique:
    accepted: bool
    explanation: str


@dataclass(frozen=True)
class GenerationModels:
    strategies: Callable[[str, tuple[Taxonomy, ...]], Sequence[Strategy]]
    scenarios: Callable[[str, tuple[tuple[str, ...], ...], int], Sequence[str]]
    complexify: Callable[[str], str]
    generate: Callable[[str], str]
    requirements_critic: Callable[[str, str], Critique]
    refine: Callable[[str, str, str], str]
    # Both independent prompts are required for correctness-bearing tasks.
    # Their calls receive only the sample; never the other critic's verdict.
    correctness_critic: Callable[[str], Critique] | None = None
    incorrectness_critic: Callable[[str], Critique] | None = None


def generate_dataset(
    instructions: str, taxonomies: tuple[Taxonomy, ...], models: GenerationModels,
    budget: CallBudget, *, size: int = 4, seed: int = 42,
    complexity_ratio: float = 0.5, scenarios_per_mix: int = 2,
    max_attempts: int = 12, max_refinements: int = 1,
    correctness_required: bool = True,
) -> dict:
    """Appendix C plus §2.2 independent double-critic rejection sampling.

    Returns a partial dataset with an explicit budget-exhausted status if target
    size is unreachable; a bounded local run never loops indefinitely to N.
    """
    if not 1 <= size <= 128 or not 0 <= complexity_ratio <= 1 or not 1 <= scenarios_per_mix <= 8:
        raise ValueError("invalid generation budget")
    if max_attempts < 1 or not 0 <= max_refinements <= 3:
        raise ValueError("invalid retry budget")
    if correctness_required and (models.correctness_critic is None or models.incorrectness_critic is None):
        raise ValueError("independent correctness and incorrectness callbacks required")
    taxonomy_map = {taxonomy.factor: taxonomy for taxonomy in taxonomies}
    if not taxonomy_map or len(taxonomy_map) != len(taxonomies):
        raise ValueError("nonempty unique factors required")
    strategies = tuple(budget.call("sampling_strategy", models.strategies, instructions, taxonomies))
    if not strategies or any(not strategy.factors or len(set(strategy.factors)) != len(strategy.factors) or not math.isfinite(strategy.weight) or strategy.weight <= 0 or set(strategy.factors) - set(taxonomy_map) for strategy in strategies):
        raise ValueError("model strategy must select existing compatible factors with positive weights")
    rng, accepted, attempts = random.Random(seed), [], []
    seen = set()
    for _ in range(max_attempts):
        if len(accepted) >= size:
            break
        try:
            strategy = rng.choices(strategies, weights=[strategy.weight for strategy in strategies], k=1)[0]
            mix = tuple(rng.choice(taxonomy_map[factor].leaves) for factor in strategy.factors)
            scenarios = tuple(budget.call("meta_prompt_generation", models.scenarios, instructions, mix, scenarios_per_mix))
            if len(scenarios) != scenarios_per_mix or any(not scenario.strip() for scenario in scenarios):
                raise ValueError("model must return the requested nonempty scenario count")
            meta = rng.choice(scenarios)
            complexified = rng.random() < complexity_ratio
            if complexified:
                meta = budget.call("complexification", models.complexify, meta)
            if not isinstance(meta, str) or not meta.strip():
                raise ValueError("invalid meta prompt")
            sample = budget.call("sample_generation", models.generate, meta)
            valid, explanations = False, []
            for refinement in range(max_refinements + 1):
                if not isinstance(sample, str) or not sample.strip():
                    raise ValueError("generated sample must be nonempty")
                critique = budget.call("requirements_critic", models.requirements_critic, meta, sample)
                if not isinstance(critique, Critique) or type(critique.accepted) is not bool:
                    raise ValueError("critic must return a binary Critique")
                explanations.append(critique.explanation)
                if critique.accepted:
                    valid = True
                    break
                if refinement < max_refinements:
                    sample = budget.call("critic_refinement", models.refine, meta, sample, critique.explanation)
            double = []
            if valid and correctness_required:
                correct = budget.call("independent_correctness_critic", models.correctness_critic, sample)
                incorrect = budget.call("independent_incorrectness_critic", models.incorrectness_critic, sample)
                if not all(isinstance(vote, Critique) and type(vote.accepted) is bool for vote in (correct, incorrect)):
                    raise ValueError("double critics must return binary Critiques")
                # accepted means affirmation of each role's own proposition:
                # 'correct' must be true and 'incorrect' must be false.
                valid = correct.accepted and not incorrect.accepted
                double = [correct.__dict__, incorrect.__dict__]
            digest = hashlib.sha256(sample.encode()).hexdigest()
            duplicate = digest in seen
            record = {"strategy": strategy.name, "mix": mix, "meta_prompt": meta, "complexified": complexified, "sample": sample, "accepted": valid and not duplicate, "duplicate": duplicate, "requirements_explanations": explanations, "double_critic": double}
            attempts.append(record)
            if record["accepted"]:
                seen.add(digest)
                accepted.append(record)
        except RuntimeError as error:
            if str(error) != "Simula model-call budget exhausted":
                raise
            return {"status": "call_budget_exhausted", "samples": accepted, "attempts": attempts, "requested": size, "calls": len(budget.trace)}
    return {"status": "complete" if len(accepted) == size else "attempt_budget_exhausted", "samples": accepted, "attempts": attempts, "requested": size, "calls": len(budget.trace)}


def calibrated_complexity(
    samples: Mapping[str, str], score_batch: Callable[[tuple[tuple[str, str], ...], str], Mapping[str, float]],
    budget: CallBudget, *, guidance: str, appearances: int = 3, batch_size: int = 5,
    seed: int = 42, elo_k: float = 32.0,
) -> dict:
    """Appendix E.3: varied batch scores -> within-batch pairs -> global Elo.

    The paper does not fix Elo's numerical hyperparameters. We declare local
    initial rating 1000, scale 400, K=32 and seeded pair order in the output.
    """
    if not samples or not 1 <= appearances <= 20 or not 2 <= batch_size <= 32 or elo_k <= 0:
        raise ValueError("nonempty samples and bounded calibration budget required")
    if len(samples) < 2 or batch_size > len(samples):
        raise ValueError("at least two samples and batch_size <= dataset size required")
    rng = random.Random(seed)
    ids, schedule = list(samples), []
    # Every round visits every ID once, so each item appears exactly K times.
    for _ in range(appearances):
        rng.shuffle(ids)
        batches = [ids[i : i + batch_size] for i in range(0, len(ids), batch_size)]
        schedule.extend(tuple(batch) for batch in batches)
    scores = {key: [] for key in samples}
    comparisons = []
    for batch in schedule:
        values = dict(budget.call("batch_relative_complexity", score_batch, tuple((key, samples[key]) for key in batch), guidance))
        if set(values) != set(batch) or any(not math.isfinite(value) for value in values.values()):
            raise ValueError("batch scorer must return each requested finite score exactly once")
        for key in batch:
            scores[key].append(float(values[key]))
        for left, right in itertools.combinations(batch, 2):
            comparisons.append((left, right, 1.0 if values[left] > values[right] else 0.0 if values[left] < values[right] else 0.5))
    rng.shuffle(comparisons)
    ratings = {key: 1000.0 for key in samples}
    for left, right, outcome in comparisons:
        expectation = 1 / (1 + 10 ** ((ratings[right] - ratings[left]) / 400))
        change = elo_k * (outcome - expectation)
        ratings[left] += change
        ratings[right] -= change
    return {
        "scores": {key: {"raw_mean": mean(scores[key]), "elo": ratings[key], "appearances": len(scores[key])} for key in samples},
        "pairwise_comparisons": len(comparisons), "batches": len(schedule),
        "elo_initial": 1000, "elo_scale": 400, "elo_k": elo_k, "seed": seed,
    }


def ngrams(text: str, n: int = 13) -> frozenset[tuple[str, ...]]:
    words = text.lower().split()
    if n < 1:
        raise ValueError("ngram size must be positive")
    return frozenset(tuple(words[index : index + n]) for index in range(len(words) - n + 1))


def contamination_overlap(sample: str, heldout_texts: Sequence[str], *, n: int = 13) -> bool:
    """Exact normalized word n-gram overlap; reference text stays in curator only.

    This is not a claim to reproduce the paper's unspecified full Jaccard
    threshold, nor proof that short examples are uncontaminated.
    """
    sample_grams = ngrams(sample, n)
    return any(sample_grams.intersection(ngrams(reference, n)) for reference in heldout_texts)
