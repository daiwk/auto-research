"""Spec-driven test-generation protocol (2608.17177), not an LLM agent.

Callbacks are trusted integrations, not a process sandbox. The public generation
view contains fixed source only: no buggy source, patch, commit or gold test.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


def _text(value):
    if type(value) is not str or not value.strip():
        raise ValueError("nonempty plain string required")
    return value


@dataclass(frozen=True)
class Condition:
    description: str
    tested: bool = False
    test_reference: str | None = None

    def __post_init__(self):
        _text(self.description)
        if type(self.tested) is not bool or (self.tested and not self.test_reference):
            raise ValueError("tested conditions require an existing test reference")
        if self.test_reference is not None:
            _text(self.test_reference)


@dataclass(frozen=True)
class Contract:
    unit: str
    description: str
    preconditions: tuple[Condition, ...]
    postconditions: tuple[Condition, ...]
    suggestions: tuple[str, ...]

    def __post_init__(self):
        _text(self.unit)
        _text(self.description)
        for conditions in (self.preconditions, self.postconditions):
            if type(conditions) is not tuple or any(type(c) is not Condition for c in conditions):
                raise ValueError("immutable condition tuple required")
        if not self.preconditions and not self.postconditions:
            raise ValueError("at least one inferred condition required")
        if type(self.suggestions) is not tuple:
            raise ValueError("immutable suggestions required")
        for suggestion in self.suggestions:
            _text(suggestion)
        if any(not c.tested for c in self.preconditions + self.postconditions) and not self.suggestions:
            raise ValueError("untested conditions need targeted suggestions")


@dataclass(frozen=True)
class Specification:
    contracts: tuple[Contract, ...]

    def __post_init__(self):
        if (type(self.contracts) is not tuple or not self.contracts
                or any(type(c) is not Contract for c in self.contracts)
                or len({c.unit for c in self.contracts}) != len(self.contracts)):
            raise ValueError("nonempty unique immutable contracts required")

    def markdown(self) -> str:
        lines = ["# Behavioral specification"]
        for contract in self.contracts:
            lines += ["", f"## {contract.unit}", "", contract.description]
            for title, conditions in (("Preconditions", contract.preconditions), ("Postconditions", contract.postconditions)):
                lines += ["", f"### {title}", ""]
                lines += [f"- [{'x' if c.tested else ' '}] {c.description}"
                          + (f" ({c.test_reference})" if c.test_reference else "") for c in conditions]
            lines += ["", "### Test suggestions", ""] + [f"- {s}" for s in contract.suggestions]
        return "\n".join(lines) + "\n"


@dataclass(frozen=True)
class FixedSourceView:
    source: str
    requirements: str = ""
    existing_tests: str = ""

    def __post_init__(self):
        _text(self.source)
        if type(self.requirements) is not str or type(self.existing_tests) is not str:
            raise ValueError("plain public context required")


@dataclass(frozen=True)
class GeneratedSuite:
    code: str
    modified_existing_paths: tuple[str, ...] = ()

    def __post_init__(self):
        _text(self.code)
        if type(self.modified_existing_paths) is not tuple:
            raise ValueError("immutable modification audit required")
        for path in self.modified_existing_paths:
            _text(path)


@dataclass(frozen=True)
class Execution:
    built: bool
    passed: bool
    failed_tests: tuple[str, ...] = ()

    def __post_init__(self):
        if type(self.built) is not bool or type(self.passed) is not bool:
            raise ValueError("explicit build/test outcomes required")
        if type(self.failed_tests) is not tuple or any(type(t) is not str or not t for t in self.failed_tests):
            raise ValueError("failed test identifiers required")
        if self.passed and (not self.built or self.failed_tests):
            raise ValueError("passing execution cannot fail build or tests")


@dataclass(frozen=True)
class Evaluation:
    valid: bool
    passes_fixed: bool
    detects_bug: bool
    reason: str

    def __post_init__(self):
        if any(type(value) is not bool for value in (self.valid, self.passes_fixed, self.detects_bug)):
            raise ValueError("explicit boolean evaluation outcomes required")
        if (self.passes_fixed and not self.valid) or (self.detects_bug and not self.passes_fixed):
            raise ValueError("detection requires a valid fixed-passing run")
        _text(self.reason)


def generate(view: FixedSourceView, extract: Callable, synthesize: Callable,
             curate: Callable | None = None) -> tuple[Specification, GeneratedSuite]:
    """Phase I must finish before II; optional human curation sits between."""
    if type(view) is not FixedSourceView:
        raise ValueError("exact public fixed-source view required")
    clean = FixedSourceView(view.source, view.requirements, view.existing_tests)
    spec = extract(clean)
    if type(spec) is not Specification:
        raise ValueError("phase I must produce a structured specification")
    if curate is not None:
        spec = curate(spec)
        if type(spec) is not Specification:
            raise ValueError("curation must preserve specification type")
    suite = synthesize(clean, spec)
    if type(suite) is not GeneratedSuite:
        raise ValueError("phase II must produce an audited test suite")
    return spec, suite


def evaluate(suite: GeneratedSuite, fixed_source: str, buggy_source: str, executor: Callable,
             *, allowed_existing_paths: tuple[str, ...] = ()) -> Evaluation:
    """Private evaluator runs identical tests on fixed then buggy source.

    Integrations must collect modification paths from a trusted filesystem audit,
    not an agent's self-report. This function never executes generated Python.
    """
    if type(suite) is not GeneratedSuite:
        raise ValueError("exact audited suite required")
    _text(fixed_source)
    _text(buggy_source)
    if type(allowed_existing_paths) is not tuple or any(type(p) is not str or not p for p in allowed_existing_paths):
        raise ValueError("explicit immutable existing-path allowlist required")
    if set(suite.modified_existing_paths) - set(allowed_existing_paths):
        return Evaluation(False, False, False, "modified-protected-source")
    fixed = executor(fixed_source, suite.code)
    if type(fixed) is not Execution:
        raise ValueError("executor must return explicit outcomes")
    if not fixed.built or not fixed.passed:
        return Evaluation(True, False, False, "fixed-build-or-test-failure")
    buggy = executor(buggy_source, suite.code)
    if type(buggy) is not Execution:
        raise ValueError("executor must return explicit outcomes")
    detects = buggy.built and not buggy.passed and bool(buggy.failed_tests)
    return Evaluation(True, True, detects, "detected" if detects else "no-test-failure-on-buggy")


def pass_detect_at_k(runs: tuple[tuple[Evaluation, ...], ...], k: int) -> dict[str, float]:
    """Observed per-bug any-success at k; not a combinatorial pass@k estimator."""
    if type(k) is not int or k < 1 or type(runs) is not tuple or not runs:
        raise ValueError("positive k and nonempty immutable bug groups required")
    if any(type(group) is not tuple or len(group) < k or any(type(r) is not Evaluation for r in group) for group in runs):
        raise ValueError("each bug needs at least k explicit run outcomes")
    return {"pass_at_k": sum(any(r.valid and r.passes_fixed for r in group[:k]) for group in runs) / len(runs),
            "detect_at_k": sum(any(r.valid and r.passes_fixed and r.detects_bug for r in group[:k]) for group in runs) / len(runs)}
