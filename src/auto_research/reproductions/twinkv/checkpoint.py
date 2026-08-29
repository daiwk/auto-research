"""Real-checkpoint TwinKV evaluation on public long-context text."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
import time
from typing import Any

from .model import repair_retained_indices, streaming_retained_indices


@dataclass(frozen=True)
class CheckpointConfig:
    output: Path
    model_id: str = "Qwen/Qwen3-4B"
    revision: str = "main"
    model_path: Path | None = None
    dataset_id: str = "Salesforce/wikitext"
    dataset_config: str = "wikitext-2-raw-v1"
    dataset_revision: str = "main"
    split: str = "test"
    examples: int = 3
    sequence_length: int = 2048
    compression_ratio: float = 0.5
    threshold: float = 0.85
    local_window: int = 32
    sink_tokens: int = 4
    recent_tokens: int = 64
    seed: int = 42


def _cache_layers(cache) -> list[tuple[Any, Any]]:
    if hasattr(cache, "layers"):
        return [(layer.keys, layer.values) for layer in cache.layers]
    if hasattr(cache, "key_cache"):
        return list(zip(cache.key_cache, cache.value_cache))
    return list(cache)


def _attention_output(query, keys, values, indices, torch):
    selected_keys = keys[indices].float()
    selected_values = values[indices].float()
    scores = selected_keys @ query.float() / (keys.shape[-1] ** 0.5)
    weights = torch.softmax(scores, dim=0)
    return weights @ selected_values


def evaluate_layer(keys, values, config: CheckpointConfig, torch) -> dict[str, float]:
    """Compare equal-budget StreamingLLM/TwinKV attention reconstruction."""
    # [batch, heads, sequence, dimension] -> first sample, averaged over heads.
    keys = keys[0]
    values = values[0]
    retained_tokens = max(
        config.sink_tokens + 1,
        round(keys.shape[-2] * (1 - config.compression_ratio)),
    )
    retained_tokens = min(retained_tokens, keys.shape[-2])
    baseline = streaming_retained_indices(
        keys.shape[-2], retained_tokens, sink_tokens=config.sink_tokens,
    ).to(keys.device)
    full = torch.arange(keys.shape[-2], device=keys.device)
    baseline_cosines, method_cosines, swaps = [], [], []
    started = time.perf_counter()
    for head in range(keys.shape[0]):
        repaired, diagnostics = repair_retained_indices(
            keys[head], baseline, threshold=config.threshold,
            local_window=config.local_window, sink_tokens=config.sink_tokens,
            recent_tokens=min(config.recent_tokens, retained_tokens - config.sink_tokens),
        )
        # The next-token query is represented by the last cached key.  This
        # isolates eviction quality without conflating decoding randomness.
        query = keys[head, -1]
        target = _attention_output(query, keys[head], values[head], full, torch)
        baseline_output = _attention_output(
            query, keys[head], values[head], baseline, torch,
        )
        method_output = _attention_output(
            query, keys[head], values[head], repaired, torch,
        )
        baseline_cosines.append(float(torch.nn.functional.cosine_similarity(
            target, baseline_output, dim=0,
        ).cpu()))
        method_cosines.append(float(torch.nn.functional.cosine_similarity(
            target, method_output, dim=0,
        ).cpu()))
        swaps.append(diagnostics.swaps)
    elapsed = time.perf_counter() - started
    return {
        "baseline_attention_cosine": statistics.fmean(baseline_cosines),
        "twinkv_attention_cosine": statistics.fmean(method_cosines),
        "swaps_mean": statistics.fmean(swaps),
        "repair_seconds": elapsed,
        "retained_tokens": retained_tokens,
        "kv_bytes": int(retained_tokens * keys.shape[0] * keys.shape[-1] * 2 * keys.element_size()),
    }


def run_checkpoint(config: CheckpointConfig) -> dict[str, Any]:
    import torch
    from datasets import load_dataset
    from huggingface_hub import dataset_info, model_info
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not 0 <= config.compression_ratio < 1:
        raise ValueError("compression_ratio must be in [0, 1)")
    torch.manual_seed(config.seed)
    device = torch.device("cuda")
    revision = config.revision if config.model_path else model_info(
        config.model_id, revision=config.revision,
    ).sha
    dataset_revision = dataset_info(
        config.dataset_id, revision=config.dataset_revision,
    ).sha
    source = str(config.model_path or config.model_id)
    tokenizer = AutoTokenizer.from_pretrained(
        source, revision=revision, local_files_only=config.model_path is not None,
    )
    model = AutoModelForCausalLM.from_pretrained(
        source, revision=revision, torch_dtype=torch.bfloat16,
        local_files_only=config.model_path is not None,
    ).to(device).eval()
    dataset = load_dataset(
        config.dataset_id, config.dataset_config, revision=dataset_revision,
        split=config.split,
    )
    corpus = "\n".join(row["text"] for row in dataset if row["text"].strip())
    tokens = tokenizer(corpus, return_tensors="pt", add_special_tokens=False)["input_ids"][0]
    needed = config.examples * config.sequence_length
    if len(tokens) < needed:
        raise ValueError(f"dataset has {len(tokens)} tokens, need {needed}")
    torch.cuda.reset_peak_memory_stats(device)
    records = []
    for index in range(config.examples):
        input_ids = tokens[index * config.sequence_length:(index + 1) * config.sequence_length]
        input_ids = input_ids.unsqueeze(0).to(device)
        torch.cuda.synchronize()
        started = time.perf_counter()
        with torch.inference_mode():
            output = model(input_ids=input_ids, use_cache=True)
        torch.cuda.synchronize()
        prefill_seconds = time.perf_counter() - started
        layers = _cache_layers(output.past_key_values)
        # Evaluate early/middle/late layers; all heads are retained.
        selected = sorted({0, len(layers) // 2, len(layers) - 1})
        layer_metrics = [
            evaluate_layer(layers[layer][0], layers[layer][1], config, torch)
            for layer in selected
        ]
        records.append({
            "prefill_seconds": prefill_seconds,
            "layers": selected,
            "baseline_attention_cosine": statistics.fmean(
                row["baseline_attention_cosine"] for row in layer_metrics
            ),
            "twinkv_attention_cosine": statistics.fmean(
                row["twinkv_attention_cosine"] for row in layer_metrics
            ),
            "repair_seconds": sum(row["repair_seconds"] for row in layer_metrics),
            "swaps_mean": statistics.fmean(row["swaps_mean"] for row in layer_metrics),
            "retained_tokens": layer_metrics[0]["retained_tokens"],
            "kv_bytes_per_layer": layer_metrics[0]["kv_bytes"],
        })
    mean = lambda key: statistics.fmean(float(row[key]) for row in records)
    payload = {
        "schema_version": 3,
        "method": "twinkv-real-checkpoint-kv-repair",
        "dataset": {"name": config.dataset_id, "config": config.dataset_config,
                    "revision": dataset_revision, "examples": config.examples},
        "checkpoint": {"model_id": config.model_id, "revision": revision},
        "setup": {**asdict(config), "output": str(config.output), "model_path": None},
        "metrics": {
            "baseline_attention_cosine_mean": mean("baseline_attention_cosine"),
            "twinkv_attention_cosine_mean": mean("twinkv_attention_cosine"),
            "cosine_delta": mean("twinkv_attention_cosine") - mean("baseline_attention_cosine"),
            "prefill_seconds_mean": mean("prefill_seconds"),
            "repair_seconds_mean": mean("repair_seconds"),
            "swaps_mean": mean("swaps_mean"),
            "retained_tokens": records[0]["retained_tokens"],
            "kv_bytes_per_layer": records[0]["kv_bytes_per_layer"],
            "peak_gpu_memory_mb": torch.cuda.max_memory_allocated(device) / 1024**2,
        },
        "records": records,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Real Qwen3 KV tensors and public WikiText-2 contexts; reconstruction diagnostic, not full LongBench generation.",
    }
    config.output.parent.mkdir(parents=True, exist_ok=True)
    config.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-id", default=CheckpointConfig.model_id)
    parser.add_argument("--revision", default="main")
    parser.add_argument("--model-path", type=Path)
    parser.add_argument("--dataset-id", default=CheckpointConfig.dataset_id)
    parser.add_argument("--dataset-config", default=CheckpointConfig.dataset_config)
    parser.add_argument("--dataset-revision", default="main")
    parser.add_argument("--split", default="test")
    parser.add_argument("--examples", type=int, default=3)
    parser.add_argument("--sequence-length", type=int, default=2048)
    parser.add_argument("--compression-ratio", type=float, default=.5)
    parser.add_argument("--threshold", type=float, default=.85)
    parser.add_argument("--local-window", type=int, default=32)
    parser.add_argument("--sink-tokens", type=int, default=4)
    parser.add_argument("--recent-tokens", type=int, default=64)
    parser.add_argument("--seed", type=int, default=42)
    payload = run_checkpoint(CheckpointConfig(**vars(parser.parse_args())))
    print(json.dumps(payload["metrics"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
