"""AgentPerturb single-target and paired-native-grader protocol interface.

Semantic validity comes from an independent verifier callback, never a string
similarity heuristic. This module does not generate an official benchmark.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, replace
import hashlib
import json
import math


SURFACES = {"U": "user_utterance", "P": "procedural_spec", "C": "carried_context", "T": "tool_contract"}
KINDS = frozenset({"missing", "redundant", "incorrect"})


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False).encode()).hexdigest()


@dataclass(frozen=True)
class PublicInstance:
    task_id: str
    user_utterance: str
    procedural_spec: str
    carried_context: str
    tool_contract: dict

    def __post_init__(self):
        if (not isinstance(self.task_id, str) or not self.task_id
                or any(not isinstance(getattr(self, key), str) for key in
                       ("user_utterance", "procedural_spec", "carried_context"))
                or not isinstance(self.tool_contract, dict)):
            raise ValueError("typed public interaction surfaces and task identity required")
        fingerprint(self.tool_contract)

    def surfaces(self):
        return {name: deepcopy(getattr(self, name)) for name in SURFACES.values()}


@dataclass(frozen=True)
class SemanticChecks:
    single_target: bool
    goal_preserved: bool
    solvable: bool
    executable: bool

    def passed(self):
        values = (self.single_target, self.goal_preserved, self.solvable, self.executable)
        if any(type(value) is not bool for value in values):
            raise ValueError("four explicit semantic verdicts required")
        return all(values)


@dataclass(frozen=True)
class PreparedPair:
    clean: PublicInstance
    perturbed: PublicInstance
    target: str
    kind: str
    generator_id: str
    verifier_id: str
    verifier_checks: SemanticChecks
    # Evaluator-only. Neither this record nor annotation is passed to the actor.
    evaluation_annotation: dict
    clean_sha256: str
    perturbed_sha256: str
    annotation_sha256: str

    def validate(self):
        if (self.target not in SURFACES or self.kind not in KINDS
                or type(self.clean) is not PublicInstance or type(self.perturbed) is not PublicInstance
                or self.clean.task_id != self.perturbed.task_id
                or not self.generator_id or not self.verifier_id or self.generator_id == self.verifier_id
                or type(self.verifier_checks) is not SemanticChecks or not self.verifier_checks.passed()):
            raise ValueError("valid independent matched-pair provenance required")
        before, after = self.clean.surfaces(), self.perturbed.surfaces()
        if (fingerprint(before) != self.clean_sha256 or fingerprint(after) != self.perturbed_sha256
                or fingerprint(self.evaluation_annotation) != self.annotation_sha256
                or {key for key in before if fingerprint(before[key]) != fingerprint(after[key])}
                != {SURFACES[self.target]}):
            raise ValueError("prepared pair changed after verification or has multiple changed targets")


def prepare_pair(clean: PublicInstance, *, target, kind, replacement, generator_id,
                 verifier_id, semantic_verifier, native_validator, evaluation_annotation=None):
    if type(clean) is not PublicInstance or target not in SURFACES or kind not in KINDS:
        raise ValueError("known target/type and typed public instance required")
    if (not isinstance(generator_id, str) or not generator_id or not isinstance(verifier_id, str)
            or not verifier_id or generator_id == verifier_id):
        raise ValueError("independent generator and verifier identities required")
    original = deepcopy(clean)
    field_name = SURFACES[target]
    candidate = replace(original, **{field_name: deepcopy(replacement)})
    before, after = original.surfaces(), candidate.surfaces()
    changed = {key for key in before if fingerprint(before[key]) != fingerprint(after[key])}
    if changed != {field_name}:
        raise ValueError("exactly the declared target must change")
    annotation = deepcopy(dict(evaluation_annotation or {}))
    try:
        # Isolated copies stop a verifier/validator from silently editing the retained pair.
        checks = semantic_verifier(deepcopy(original), deepcopy(candidate), target, kind,
                                   deepcopy(annotation))
        if type(checks) is not SemanticChecks or not checks.passed():
            raise ValueError("independent semantic verification rejected candidate")
        executable = native_validator(deepcopy(candidate), deepcopy(annotation))
        if type(executable) is not bool or not executable:
            raise ValueError("native validator rejected candidate")
    except Exception as error:
        raise ValueError(f"verification failed closed: {type(error).__name__}") from error
    return PreparedPair(original, candidate, target, kind, generator_id, verifier_id, checks, annotation,
                        fingerprint(before), fingerprint(after), fingerprint(annotation))


@dataclass(frozen=True)
class ActorOutput:
    answer: str
    recorded_tokens: int | None = None

    def __post_init__(self):
        if (not isinstance(self.answer, str) or (self.recorded_tokens is not None
                and (type(self.recorded_tokens) is not int or self.recorded_tokens < 0))):
            raise ValueError("answer text and nonnegative or unavailable token count required")


@dataclass(frozen=True)
class EpisodeOutcome:
    execution_status: str
    score: float | None
    recorded_tokens: int | None

    def __post_init__(self):
        if self.execution_status not in {"completed", "failed"}:
            raise ValueError("explicit execution status required")
        if self.score is not None and (type(self.score) not in (float, int)
                or not math.isfinite(self.score) or not 0 <= self.score <= 1):
            raise ValueError("native reward must be finite in [0,1] or unscored")
        if self.execution_status == "failed" and self.score is not None:
            raise ValueError("failed execution cannot have a score")
        if self.recorded_tokens is not None and (type(self.recorded_tokens) is not int
                                                or self.recorded_tokens < 0):
            raise ValueError("nonnegative or unavailable token count required")


@dataclass(frozen=True)
class PairedOutcome:
    task_id: str
    target: str
    kind: str
    clean: EpisodeOutcome
    perturbed: EpisodeOutcome

    def __post_init__(self):
        if (not self.task_id or self.target not in SURFACES or self.kind not in KINDS
                or type(self.clean) is not EpisodeOutcome or type(self.perturbed) is not EpisodeOutcome):
            raise ValueError("valid paired task/target/type and typed outcomes required")


def evaluate_pair(pair: PreparedPair, *, actor, native_grader, reference):
    """Actor sees public surfaces only, never clean+perturbed pair or annotations.

Actor/grader integrations are trusted Python callbacks, not security sandboxes.
The original native backend is supplied externally; no tool implementation or
success oracle is changed by this protocol adapter.
"""
    if type(pair) is not PreparedPair:
        raise ValueError("independently verified pair required")
    pair.validate()

    def episode(public):
        try:
            output = actor(deepcopy(public))
            if type(output) is not ActorOutput:
                raise ValueError("typed actor output required")
        except Exception:
            return EpisodeOutcome("failed", None, None)
        try:
            score = native_grader(output.answer, deepcopy(reference))
            return EpisodeOutcome("completed", score, output.recorded_tokens)
        except Exception:
            return EpisodeOutcome("completed", None, output.recorded_tokens)

    return PairedOutcome(pair.clean.task_id, pair.target, pair.kind,
                         episode(pair.clean), episode(pair.perturbed))


def paired_metrics(outcomes, *, requested_pairs):
    """Matched observed scores plus all-requested coverage and missing-score bounds.

Unlike the paper's completion-selected cohort, missing/failed pairs are never
silently removed. Bounds make no assumption about unknown native scores.
"""
    requested = tuple(requested_pairs)
    if (not requested or any(not isinstance(identity, tuple) or len(identity) != 3
            or not isinstance(identity[0], str) or not identity[0]
            or identity[1] not in SURFACES or identity[2] not in KINDS for identity in requested)
            or len(set(requested)) != len(requested)):
        raise ValueError("distinct requested task/target/type scope required")
    rows = tuple(outcomes)
    if any(type(row) is not PairedOutcome for row in rows):
        raise ValueError("typed paired outcomes required")
    identities = [(row.task_id, row.target, row.kind) for row in rows]
    if len(set(identities)) != len(rows):
        raise ValueError("duplicate task/target/type pair")
    if not set(identities) <= set(requested):
        raise ValueError("outcome outside requested pair scope")
    complete = [r for r in rows if r.clean.score is not None and r.perturbed.score is not None]
    clean_sum = sum(r.clean.score or 0 for r in rows)
    changed_sum = sum(r.perturbed.score or 0 for r in rows)
    n = len(requested)
    clean_missing = n-sum(r.clean.score is not None for r in rows)
    changed_missing = n-sum(r.perturbed.score is not None for r in rows)
    clean_mean = sum(r.clean.score for r in complete)/len(complete) if complete else None
    changed_mean = sum(r.perturbed.score for r in complete)/len(complete) if complete else None
    drop = clean_mean-changed_mean if complete else None
    return {"requested_pairs": n, "complete_scored_pairs": len(complete),
            "missing_pair_records": n-len(rows),
            "pair_coverage": len(complete)/n, "clean_unscored": clean_missing,
            "perturbed_unscored": changed_missing,
            "clean_execution_failures": sum(r.clean.execution_status == "failed" for r in rows),
            "perturbed_execution_failures": sum(r.perturbed.execution_status == "failed" for r in rows),
            "clean_native_mean_paired_observed": clean_mean,
            "perturbed_native_mean_paired_observed": changed_mean, "paired_drop_observed": drop,
            "relative_degradation_observed": drop/clean_mean if complete and clean_mean else None,
            "clean_all_requested_lower_bound": clean_sum/n,
            "clean_all_requested_upper_bound": (clean_sum+clean_missing)/n,
            "perturbed_all_requested_lower_bound": changed_sum/n,
            "perturbed_all_requested_upper_bound": (changed_sum+changed_missing)/n,
            "paired_drop_all_requested_lower_bound": (clean_sum-changed_sum-changed_missing)/n,
            "paired_drop_all_requested_upper_bound": (clean_sum+clean_missing-changed_sum)/n,
            "known_recorded_tokens_all_episodes": sum(
                (r.clean.recorded_tokens or 0)+(r.perturbed.recorded_tokens or 0) for r in rows),
            "token_capture_coverage": sum(r.recorded_tokens is not None for row in rows
                                           for r in (row.clean, row.perturbed))/(2*n)}
