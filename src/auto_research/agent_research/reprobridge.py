"""ReproBridge's evaluator-side compatibility and four-part evidence contracts.

This is not an LLM Reproducer or semantic Auditor. File hashes and timestamps
provide mechanical checks, not proof that an untrusted executor ran a program.
Private reference observations are never included in the actor-facing task.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import re
import statistics

REQUIRES_GPU_VALIDATION = False
VIOLATION_CLASSES = frozenset({
    "copied_measurement", "substituted_instrument", "altered_operand",
    "outcome_selection", "wrong_statistic",
})


def _text(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("nonempty text required")
    return value


def _finite(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("finite scalar measurement required")
    return float(value)


def _hash(value: str, size: int = 64) -> str:
    if not isinstance(value, str) or not re.fullmatch(f"[0-9a-f]{{{size}}}", value):
        raise ValueError("immutable lowercase hexadecimal digest required")
    return value


@dataclass(frozen=True)
class ActorTask:
    """Only the experiment identity/procedure is exposed, not evaluator targets."""
    identity: str
    paper_url: str
    raw_commit: str
    dataset: str
    model: str
    procedure: str
    metric: str
    reporting_statistic: str

    def __post_init__(self):
        for value in (self.identity, self.paper_url, self.dataset, self.model,
                      self.procedure, self.metric, self.reporting_statistic):
            _text(value)
        _hash(self.raw_commit, 40)


@dataclass(frozen=True)
class Reference:
    """Private evaluator state: exactly five independently verified observations."""
    observations: tuple[float, ...]
    coverage: float = .95

    def __post_init__(self):
        values = tuple(_finite(x) for x in self.observations)
        if len(values) != 5 or isinstance(self.coverage, bool) or not 0 < self.coverage < 1:
            raise ValueError("five observations and a probability coverage required")
        object.__setattr__(self, "observations", values)

    @property
    def interval(self) -> tuple[float, float]:
        # Exact Eq.1 prediction interval, not a CI for the reference mean.
        from scipy.stats import t

        mean = statistics.mean(self.observations)
        radius = max(float(t.ppf((1 + self.coverage) / 2, 4))
                     * statistics.stdev(self.observations) * math.sqrt(1 + 1 / 5),
                     .01 * abs(mean))
        bounds = mean - radius, mean + radius
        if not all(math.isfinite(x) for x in bounds):
            raise ValueError("reference scale produces nonfinite compatibility bounds")
        return bounds

    def compatible(self, value: float) -> bool:
        lower, upper = self.interval
        return lower <= _finite(value) <= upper


@dataclass(frozen=True)
class Artifact:
    """The four delivered components must be explicit, separately hashed files."""
    code: tuple[str, str]
    environment: tuple[str, str]
    launcher: tuple[str, str]
    guide: tuple[str, str]

    def __post_init__(self):
        paths = []
        for item in (self.code, self.environment, self.launcher, self.guide):
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError("each artifact component needs path and SHA256")
            paths.append(_text(item[0]))
            _hash(item[1])
        if len(set(paths)) != 4:
            raise ValueError("four distinct component paths required")

    def verify(self, directory: Path) -> None:
        for path, digest in (self.code, self.environment, self.launcher, self.guide):
            _verified_file(directory, path, digest)


def _verified_file(directory: Path, name: str, digest: str) -> Path:
    root = Path(directory).resolve()
    candidate = root / _text(name)
    if Path(name).is_absolute() or not candidate.resolve().is_relative_to(root):
        raise ValueError("artifact must remain inside its run directory")
    if not candidate.is_file() or hashlib.sha256(candidate.read_bytes()).hexdigest() != _hash(digest):
        raise ValueError("missing or changed file-backed evidence")
    return candidate


@dataclass(frozen=True)
class ExecutionRecord:
    """Claimed execution evidence, to be independently inspected after the run."""
    code_commit: str
    script: tuple[str, str]
    environment: tuple[str, str]
    output: tuple[str, str]
    value_path: tuple[str, ...]
    run_started_ns: int
    run_finished_ns: int
    extracted_ns: int

    def __post_init__(self):
        _hash(self.code_commit, 40)
        for pair in (self.script, self.environment, self.output):
            if not isinstance(pair, tuple) or len(pair) != 2:
                raise ValueError("path/hash evidence pairs required")
            _text(pair[0])
            _hash(pair[1])
        if not self.value_path or any(not isinstance(x, str) or not x for x in self.value_path):
            raise ValueError("explicit JSON measurement location required")
        times = (self.run_started_ns, self.run_finished_ns, self.extracted_ns)
        if any(type(x) is not int or x < 0 for x in times) or not times[0] <= times[1] <= times[2]:
            raise ValueError("execution must precede measurement extraction")


def read_measurement(directory: Path, task: ActorTask, record: ExecutionRecord) -> float:
    """Check pinned bytes, code identity, output freshness, and actual JSON value.

    This does not authenticate shell execution, semantic correctness of scripts,
    or an executor-controlled clock. Those require the independent Auditor.
    """
    if not isinstance(task, ActorTask) or not isinstance(record, ExecutionRecord):
        raise ValueError("typed public task and evaluator execution record required")
    if record.code_commit != task.raw_commit:
        raise ValueError("execution does not match the pinned task code")
    for pair in (record.script, record.environment):
        _verified_file(directory, *pair)
    output = _verified_file(directory, *record.output)
    if not record.run_started_ns <= output.stat().st_mtime_ns <= record.run_finished_ns:
        raise ValueError("output is not fresh within this claimed execution")
    value = json.loads(output.read_text(encoding="utf-8"))
    try:
        for key in record.value_path:
            value = value[key]
    except (KeyError, TypeError) as exc:
        raise ValueError("measurement location is absent") from exc
    return _finite(value)


@dataclass(frozen=True)
class Finding:
    category: str
    evidence_location: str
    material_effect: bool
    refutation_failed: bool | None

    def __post_init__(self):
        if self.category not in VIOLATION_CLASSES or type(self.material_effect) is not bool:
            raise ValueError("eligible violation and explicit materiality required")
        _text(self.evidence_location)
        if self.refutation_failed is not None and type(self.refutation_failed) is not bool:
            raise ValueError("explicit failed/successful/uncertain refutation required")

    @property
    def invalidates(self) -> bool:
        return self.material_effect and self.refutation_failed is True


def evaluate(value: float, reference: Reference, findings: tuple[Finding, ...] = ()) -> dict:
    """Evaluator-only numerical verdict plus externally supported audit findings.

    Suspicion, a numerical mismatch, or an unresolved finding is not itself a
    proven integrity violation. This function does not synthesize audit findings.
    """
    if not isinstance(reference, Reference) or any(not isinstance(f, Finding) for f in findings):
        raise ValueError("private typed reference and localized findings required")
    compatible = reference.compatible(value)
    invalidated = any(f.invalidates for f in findings)
    return {"numerically_compatible": compatible, "invalidated": invalidated,
            "uncertain_findings": sum(f.refutation_failed is None for f in findings),
            "criterion_passed": compatible and not invalidated,
            "semantic_auditor_executed": False}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Synthetic scoring truth table, not research reproduction capability."""
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only component required")
    reference = Reference((.98, .99, 1., 1.01, 1.02))
    valid = evaluate(1., reference)
    too_good = evaluate(10., reference)
    invalid = evaluate(1., reference, (Finding("copied_measurement", "trace:line7", True, True),))
    uncertain = evaluate(1., reference, (Finding("wrong_statistic", "script:line8", True, None),))
    low, high = reference.interval
    return {"seed": seed, "device": "cpu", "diagnostic_only": True,
            "evaluation_tier": "l1_mechanism",
            "metrics": {"interval_lower": low, "interval_upper": high,
                        "truth_table_cases": 4, "uncertain_findings": uncertain["uncertain_findings"]},
            "checks": {"two_sided_compatibility": valid["criterion_passed"] and not too_good["criterion_passed"],
                       "material_refuted_violation_invalidates": not invalid["criterion_passed"],
                       "uncertainty_not_automatic_invalidation": uncertain["criterion_passed"],
                       "reference_not_in_actor_fields": "observations" not in ActorTask.__dataclass_fields__,
                       "not_a_semantic_auditor": not valid["semantic_auditor_executed"]}}
