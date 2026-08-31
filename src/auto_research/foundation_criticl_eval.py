"""Public-checkpoint CritICL evaluation on the official GSM8K split."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import re
import statistics

from .checkpoint_backend import (
    HFCausalLMBackend,
    SMOLLM2_135M_ID,
    SMOLLM2_135M_REVISION,
)
from .datasets import GSM8K_FILES, GSM8K_REVISION, gsm8k
from .foundation_methods import CritiqueExample, build_criticl_prompt


@dataclass(frozen=True)
class CritICLEvalConfig:
    output_dir: Path = Path("runs/criticl-checkpoint")
    dataset_dir: Path = Path("data")
    weak_model_id: str = SMOLLM2_135M_ID
    weak_model_revision: str = SMOLLM2_135M_REVISION
    weak_checkpoint_path: Path | None = None
    strong_model_id: str = SMOLLM2_135M_ID
    strong_model_revision: str = SMOLLM2_135M_REVISION
    strong_checkpoint_path: Path | None = None
    bank_examples: int = 24
    evaluation_examples: int = 12
    maximum_critiques: int = 3
    maximum_new_tokens: int = 96
    seeds: tuple[int, ...] = (42, 43, 44)
    offline: bool = False

    def validate(self) -> None:
        if min(
            self.bank_examples, self.evaluation_examples,
            self.maximum_critiques, self.maximum_new_tokens,
        ) < 1:
            raise ValueError("CritICL evaluation sizes must be positive")
        if len(self.seeds) != 3 or len(set(self.seeds)) != 3:
            raise ValueError("CritICL checkpoint evaluation requires three distinct seeds")


def run_criticl_checkpoint_evaluation(
    config: CritICLEvalConfig,
    *,
    weak_backend=None,
    strong_backend=None,
) -> tuple[dict, Path]:
    """Compare zero-shot, static CritICL and dynamic CritICL without test leakage."""
    config.validate()
    rows = gsm8k(config.dataset_dir, not config.offline)
    weak = weak_backend or HFCausalLMBackend(
        config.weak_model_id, config.weak_model_revision,
        checkpoint_path=config.weak_checkpoint_path, offline=config.offline,
    )
    strong = strong_backend or HFCausalLMBackend(
        config.strong_model_id, config.strong_model_revision,
        checkpoint_path=config.strong_checkpoint_path, offline=config.offline,
    )
    bank = _build_bank(rows["train"][: config.bank_examples], weak, config)
    heldout = rows["test"][: config.evaluation_examples]
    seed_results = []
    for seed in config.seeds:
        result = {"seed": seed}
        for mode in ("zero-shot", "static", "dynamic"):
            correct = parsed = tokens = 0
            for index, row in enumerate(heldout):
                prompt = _evaluation_prompt(row["question"], bank, mode, config)
                generated = strong.generate(
                    prompt,
                    samples=1,
                    max_new_tokens=config.maximum_new_tokens,
                    seed=seed * 10_000 + index,
                    temperature=0.0,
                )
                predicted = _last_number(generated.texts[0])
                expected = _official_answer(row["answer"])
                parsed += int(predicted is not None)
                correct += int(predicted == expected)
                tokens += generated.generated_tokens[0]
            result[mode] = {
                "accuracy": correct / len(heldout),
                "parse_rate": parsed / len(heldout),
                "generated_tokens": tokens,
                "examples": len(heldout),
            }
        seed_results.append(result)
    payload = {
        "schema_version": 1,
        "method": "criticl",
        "config": {
            **asdict(config),
            "output_dir": str(config.output_dir),
            "dataset_dir": str(config.dataset_dir),
            "weak_checkpoint_path": str(config.weak_checkpoint_path) if config.weak_checkpoint_path else None,
            "strong_checkpoint_path": str(config.strong_checkpoint_path) if config.strong_checkpoint_path else None,
        },
        "metrics": {
            mode: _aggregate([row[mode]["accuracy"] for row in seed_results])
            for mode in ("zero-shot", "static", "dynamic")
        },
        "seed_results": seed_results,
        "critbank": {
            "train_only": True,
            "attempted_examples": config.bank_examples,
            "retained_failures": len(bank),
            "failure_modes": sorted({item.failure_mode for item in bank}),
        },
        "provenance": {
            "dataset": "openai/grade-school-math official train/test JSONL",
            "dataset_revision": GSM8K_REVISION,
            "dataset_sha256": GSM8K_FILES,
            "weak_checkpoint": {"model_id": config.weak_model_id, "revision": config.weak_model_revision},
            "strong_checkpoint": {"model_id": config.strong_model_id, "revision": config.strong_model_revision},
        },
        "protocol": {
            "three_seed_evaluation": True,
            "test_used_for_critbank": False,
            "test_used_for_selection": False,
            "baselines": ["zero-shot", "CritICL-static", "CritICL-dynamic"],
            "claim_boundary": (
                "public-checkpoint GSM8K subset evaluation; heuristic failure labels replace "
                "the paper's frontier-LLM critic and are reported as such"
            ),
        },
    }
    config.output_dir.mkdir(parents=True, exist_ok=True)
    path = config.output_dir / "metrics.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload, path


def _build_bank(rows, backend, config) -> tuple[CritiqueExample, ...]:
    bank = []
    for index, row in enumerate(rows):
        generated = backend.generate(
            _base_prompt(row["question"]),
            samples=1,
            max_new_tokens=config.maximum_new_tokens,
            seed=7_000 + index,
            temperature=0.0,
        )
        response = generated.texts[0]
        expected = _official_answer(row["answer"])
        if _last_number(response) == expected:
            continue
        bank.append(CritiqueExample(
            question=row["question"],
            incorrect_response=response,
            failure_mode=_failure_mode(row["question"], response),
            critique=(
                "Re-check the requested quantities and arithmetic. A verified training-split "
                f"solution ends in {expected}; do not copy it to unrelated questions."
            ),
        ))
    if not bank:
        raise RuntimeError("weak checkpoint produced no CritBank failures")
    return tuple(bank)


def _evaluation_prompt(question, bank, mode, config):
    if mode == "zero-shot":
        return _base_prompt(question)
    prompt, _ = build_criticl_prompt(
        question,
        bank,
        mode=mode,
        maximum_examples=config.maximum_critiques,
    )
    return prompt + "\nShow concise reasoning and end with Answer: <number>."


def _base_prompt(question: str) -> str:
    return f"Problem: {question}\nShow concise reasoning and end with Answer: <number>."


def _failure_mode(question: str, response: str) -> str:
    text = f"{question} {response}".lower()
    if any(token in text for token in ("percent", "%", "rate", "ratio")):
        return "ratio_or_percentage"
    if any(token in text for token in ("hour", "minute", "mile", "meter", "dollar")):
        return "unit_conversion"
    if len(re.findall(r"[-+*/]", response)) < 1:
        return "missing_arithmetic_trace"
    return "multi_step_arithmetic"


def _official_answer(text: str) -> str:
    match = re.search(r"####\s*(-?[\d,]+(?:\.\d+)?)", text)
    if not match:
        raise ValueError("GSM8K answer is missing the official delimiter")
    return _normalize_number(match.group(1))


def _last_number(text: str) -> str | None:
    matches = re.findall(r"-?[\d,]+(?:\.\d+)?", text)
    return _normalize_number(matches[-1]) if matches else None


def _normalize_number(value: str) -> str:
    value = value.replace(",", "")
    try:
        number = float(value)
    except ValueError:
        return value
    return str(int(number)) if number.is_integer() else f"{number:.8g}"


def _aggregate(values) -> dict[str, float]:
    mean = statistics.fmean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    radius = 1.96 * std / math.sqrt(len(values))
    return {"mean": mean, "std": std, "ci95_low": mean - radius, "ci95_high": mean + radius}
