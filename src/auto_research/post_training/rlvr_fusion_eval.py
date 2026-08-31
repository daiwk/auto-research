"""Official-checkpoint RLVR Fusion comparison on pinned released test data."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path
import re
import statistics

from ..checkpoint_backend import HFCausalLMBackend


LLM_FUSION_TEST_ID = "Siye01/LLM-Fusion-Test"
LLM_FUSION_TEST_REVISION = "c044cd49eaeb9e147ee5a8c001891ba5b6eb225c"
DEFAULT_CHECKPOINTS = (
    ("base", "Qwen/Qwen3-4B-Instruct-2507", "cdbee75f17c01a7cc42f958dc650907174af0554"),
    ("merge", "Siye01/Qwen3-4B-Inst-Merge", "3253439e014b7c0fca9ed3ca11e4f899e854f440"),
    ("mix", "Siye01/Qwen3-4B-Inst-Mix", "88cec4c121782d8a3af0a806b28d3c12445d824e"),
    ("mopd", "Siye01/Qwen3-4B-Inst-MOPD", "b61a9f00b77302b6e947af1215b7cb994b884c4a"),
)


@dataclass(frozen=True)
class RLVRFusionEvalConfig:
    output_dir: Path = Path("runs/rlvr-fusion-checkpoints")
    dataset_dir: Path = Path("data")
    benchmark: str = "AIME2025"
    maximum_examples: int = 10
    maximum_new_tokens: int = 1024
    seeds: tuple[int, ...] = (42, 43, 44)
    checkpoints: tuple[tuple[str, str, str], ...] = DEFAULT_CHECKPOINTS
    offline: bool = False

    def validate(self) -> None:
        if self.benchmark not in {"AIME2025", "AIME2026", "GPQA"}:
            raise ValueError("single-A100 bridge supports AIME2025, AIME2026 or GPQA")
        if min(self.maximum_examples, self.maximum_new_tokens) < 1:
            raise ValueError("evaluation sizes must be positive")
        if len(self.seeds) != 3 or len(set(self.seeds)) != 3:
            raise ValueError("RLVR Fusion comparison requires three distinct seeds")
        if {name for name, _, _ in self.checkpoints} != {"base", "merge", "mix", "mopd"}:
            raise ValueError("comparison must include base, merge, mix and mopd")
        if any(not revision for _, _, revision in self.checkpoints):
            raise ValueError("every released checkpoint must be pinned to a revision")


def run_rlvr_fusion_evaluation(
    config: RLVRFusionEvalConfig,
    *,
    rows=None,
    backend_factory=None,
) -> tuple[dict, Path]:
    config.validate()
    loaded = rows if rows is not None else _load_rows(config)
    # Hugging Face Dataset slicing returns a dict-of-columns, unlike a Python
    # sequence.  Iterate rows explicitly so both official datasets and injected
    # test fixtures preserve the same record contract.
    source_rows = [loaded[index] for index in range(min(len(loaded), config.maximum_examples))]
    if not source_rows:
        raise ValueError("RLVR Fusion evaluation selected no examples")
    factory = backend_factory or (
        lambda model_id, revision: HFCausalLMBackend(
            model_id, revision, offline=config.offline,
        )
    )
    variants = []
    for name, model_id, revision in config.checkpoints:
        backend = factory(model_id, revision)
        seed_results = []
        for seed in config.seeds:
            correct = parsed = tokens = 0
            for index, row in enumerate(source_rows):
                prompt = _prompt(backend, row)
                generation = backend.generate(
                    prompt, samples=1, max_new_tokens=config.maximum_new_tokens,
                    seed=seed * 10_000 + index, temperature=0.0,
                )
                predicted = _answer(generation.texts[0], config.benchmark)
                expected = _ground_truth(row)
                parsed += int(predicted is not None)
                correct += int(predicted == expected)
                tokens += generation.generated_tokens[0]
            seed_results.append({
                "seed": seed,
                "accuracy": correct / len(source_rows),
                "parse_rate": parsed / len(source_rows),
                "generated_tokens": tokens,
            })
        variants.append({
            "name": name,
            "model_id": model_id,
            "revision": revision,
            "metrics": {
                "accuracy": _aggregate([row["accuracy"] for row in seed_results]),
                "parse_rate": _aggregate([row["parse_rate"] for row in seed_results]),
            },
            "seed_results": seed_results,
        })
        del backend
    payload = {
        "schema_version": 1,
        "method": "rlvr-fusion",
        "config": {**asdict(config), "output_dir": str(config.output_dir), "dataset_dir": str(config.dataset_dir)},
        "variants": variants,
        "provenance": {
            "dataset_id": LLM_FUSION_TEST_ID,
            "dataset_revision": LLM_FUSION_TEST_REVISION,
            "official_code": "https://github.com/Di-viner/LLM-Fusion",
            "official_code_revision": "e314dd28cea056e617490065fc08c4aed90204f3",
        },
        "protocol": {
            "three_seed_generation": True,
            "same_examples_and_budget": True,
            "single_a100_subset_bridge": True,
            "claim_boundary": (
                "pinned official checkpoint comparison on one released benchmark subset; "
                "not the paper's eight-benchmark 32-GPU evaluation"
            ),
        },
    }
    config.output_dir.mkdir(parents=True, exist_ok=True)
    path = config.output_dir / "metrics.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload, path


def _load_rows(config):
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("RLVR Fusion checkpoint comparison requires the post-training-gpu extra") from exc
    return load_dataset(
        LLM_FUSION_TEST_ID,
        config.benchmark,
        split="test",
        revision=LLM_FUSION_TEST_REVISION,
        cache_dir=str(config.dataset_dir / "huggingface"),
        download_mode="reuse_dataset_if_exists",
    )


def _prompt(backend, row):
    messages = row.get("prompt") or [{"role": "user", "content": row.get("question", "")}]
    tokenizer = getattr(backend, "tokenizer", None)
    if tokenizer is not None and getattr(tokenizer, "chat_template", None):
        return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return "\n".join(str(item.get("content", "")) for item in messages)


def _ground_truth(row):
    reward = row.get("reward_model") or {}
    value = reward.get("ground_truth", (row.get("extra_info") or {}).get("answer"))
    return _normalize(str(value))


def _answer(text, benchmark):
    if benchmark.startswith("AIME"):
        matches = re.findall(r"\\boxed\{\s*(-?[\d,]+)\s*\}", text)
        if not matches:
            matches = re.findall(r"-?[\d,]+", text)
        return _normalize(matches[-1]) if matches else None
    matches = re.findall(r"(?:answer|choice)\s*(?:is|:)?\s*\(?([A-D])\)?", text, re.I)
    return matches[-1].upper() if matches else None


def _normalize(value):
    value = value.strip().replace(",", "")
    try:
        number = float(value)
    except ValueError:
        return value.upper()
    return str(int(number)) if number.is_integer() else f"{number:.8g}"


def _aggregate(values):
    mean = statistics.fmean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0
    radius = 1.96 * std / math.sqrt(len(values))
    return {"mean": mean, "std": std, "ci95_low": mean - radius, "ci95_high": mean + radius}
