"""Choice-only capability protocol from arXiv:2610.11978.

This reproduces the evaluation protocol, not the closed Jev checkpoint or the
paper's vendor scores. Gold references never enter provider requests.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping, Sequence

from .contracts import ChoiceQuestion, SystemOneRequest


BENCHMARKS = {
    "mmlu-pro": "knowledge", "mmlu-redux": "knowledge", "mmlu": "knowledge",
    "gpqa-diamond": "knowledge", "c-eval": "knowledge", "hellaswag": "knowledge",
    "winogrande": "knowledge", "truthfulqa": "knowledge",
    "arc-challenge": "reasoning", "mathqa": "reasoning", "aqua-rat": "reasoning",
    "mmlu-prox": "multilingual", "mmmlu": "multilingual",
}


@dataclass(frozen=True)
class CapabilityItem:
    identifier: str
    benchmark: str
    question: str
    options: Mapping[str, str]
    target: str
    language: str = "en"
    split: str = "test"

    def __post_init__(self):
        if self.benchmark not in BENCHMARKS:
            raise ValueError("benchmark is not one of the paper's 13 tasks")
        if self.target not in self.options or len(self.options) < 2:
            raise ValueError("invalid multiple-choice reference")
        if not self.identifier or not self.question or not self.language:
            raise ValueError("identifier, question and language must be nonempty")
        if self.split not in {"calibration", "test"}:
            raise ValueError("only calibration/test records are supported")

    def request(self) -> SystemOneRequest:
        return SystemOneRequest(
            state={"question": self.question},
            questions={"answer": ChoiceQuestion("Choose the best answer.", dict(self.options))},
        )


def evaluate_capability(provider, items: Sequence[CapabilityItem]) -> dict:
    """One inference per item, macro grouping, explicit missing-task coverage."""
    if not items or any(item.split != "test" for item in items):
        raise ValueError("evaluation requires a nonempty isolated test split")
    if len({item.identifier for item in items}) != len(items):
        raise ValueError("duplicate evaluation identifiers")
    groups: dict[tuple[str, str], list[bool]] = {}
    predictions = []
    for item in items:
        response = provider.decide(item.request())
        answer = response.answers.get("answer")
        valid = answer is not None and answer.type == "choice" and answer.value in item.options
        correct = bool(valid and answer.value == item.target)
        groups.setdefault((item.benchmark, item.language), []).append(correct)
        predictions.append({
            "id": item.identifier, "prediction": answer.value if valid else None,
            "valid": valid, "correct": correct,
        })
    results = []
    for (benchmark, language), correct in sorted(groups.items()):
        n, successes = len(correct), sum(correct)
        p = successes / n
        # Wilson interval remains nonzero even with all-correct/all-wrong samples.
        z = 1.959963984540054
        denominator = 1 + z * z / n
        center = (p + z * z / (2 * n)) / denominator
        radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
        results.append({"benchmark": benchmark, "category": BENCHMARKS[benchmark],
                        "language": language, "examples": n, "accuracy": p,
                        "accuracy_ci95": [center - radius, center + radius]})
    covered = {row["benchmark"] for row in results}
    summaries = []
    for benchmark in sorted(covered):
        rows = [row for row in results if row["benchmark"] == benchmark]
        total = sum(row["examples"] for row in rows)
        weighted = sum(row["accuracy"] * row["examples"] for row in rows) / total
        multilingual = benchmark in {"mmlu-prox", "mmmlu"}
        # Paper Appendix A uses language-level macro averaging for translations;
        # unequal language sample counts must not silently weight one language.
        accuracy = sum(row["accuracy"] for row in rows) / len(rows) if multilingual else weighted
        expected = {"mmlu-prox": 29, "mmmlu": 14}.get(benchmark, 1)
        summaries.append({"benchmark": benchmark, "accuracy": accuracy,
                          "aggregation": "language macro" if multilingual else "item weighted",
                          "item_weighted_accuracy": weighted, "examples": total,
                          "evaluated_languages": sorted(row["language"] for row in rows),
                          "expected_language_count": expected,
                          "complete_language_count": len(rows) == expected})
    return {
        "schema_version": 2, "paper": "2610.11978", "protocol": "single-run Choice",
        "results": results, "benchmark_summary": summaries, "predictions": predictions,
        "coverage": {"covered": sorted(covered), "missing": sorted(set(BENCHMARKS) - covered)},
        "claim_policy": "measured selected-backend scores; no substitution for closed Jev results",
        "test_used_for_selection": False,
    }


def frontier_comparison(scores: Sequence[Mapping]) -> dict:
    """Keep directly measured and heterogeneous published scores separate."""
    import statistics

    result = {}
    for benchmark in BENCHMARKS:
        measured, reported = [], []
        for row in scores:
            if row.get("benchmark") != benchmark:
                continue
            accuracy = float(row["accuracy"])
            if not math.isfinite(accuracy) or not 0 <= accuracy <= 1:
                raise ValueError("scores must be finite proportions, not percentages")
            kind = row.get("provenance")
            if kind not in {"measured", "published"} or not row.get("source"):
                raise ValueError("every comparison score requires provenance/source")
            (measured if kind == "measured" else reported).append(accuracy)
        if measured or reported:
            result[benchmark] = {
                "measured_median": statistics.median(measured) if measured else None,
                "measured_models": len(measured), "published_scores": reported,
                "published_comparison_only": True,
            }
    return result
