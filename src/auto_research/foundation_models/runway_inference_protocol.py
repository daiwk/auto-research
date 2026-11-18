"""CPU-only Runway cache/SLA/cost protocol; does not run NVIDIA AIPerf.

The full configuration is hashed, conservatively also including engine config.
The paper instead isolates engine changes with a fresh experiment path.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import math
from typing import Callable

REQUIRES_GPU_VALIDATION = False


def cache_key(configuration: dict) -> str:
    required = {"dataset", "dataset_revision", "instance", "model", "model_revision", "engine",
                "engine_version", "input_length", "output_length", "concurrency", "streaming",
                "aiperf_extra_args", "benchmark_duration", "custom_dataset_type", "warmup",
                "engine_configuration"}
    if required - configuration.keys():
        raise ValueError(f"missing configuration: {sorted(required - configuration.keys())}")
    encoded = json.dumps(configuration, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256(encoded.encode()).hexdigest()


def result_for_cell(configuration: dict, cache: dict, measure: Callable[[dict], dict] | None = None,
                    *, only_cache: bool = False, no_cache: bool = False) -> tuple[dict, bool]:
    if only_cache and no_cache:
        raise ValueError("only_cache and no_cache conflict")
    key = cache_key(configuration)
    if not no_cache and key in cache:
        return deepcopy(cache[key]), True
    if only_cache:
        raise KeyError(f"no matching measurement: {key}")
    if measure is None:
        raise ValueError("a measurement adapter is required on a cache miss")
    result = measure(deepcopy(configuration))
    if not isinstance(result, dict):
        raise ValueError("measurement adapter must return its raw result dictionary")
    cache[key] = deepcopy(result)
    return deepcopy(result), False


def evaluate_sla(measurements: dict[str, tuple[float, str]], thresholds: list[dict]) -> dict:
    """Fail closed on missing/unit-mismatched data; warnings are not critical failures."""
    if not thresholds:
        raise ValueError("an explicit nonempty SLA is required")
    verdicts = []
    for rule in thresholds:
        if rule.get("operator") not in ("<=", ">=") or rule.get("severity") not in ("critical", "warning"):
            raise ValueError("unsupported SLA rule")
        limit = rule["value"]
        if not math.isfinite(limit):
            raise ValueError("finite SLA threshold required")
        item = measurements.get(rule["metric"])
        valid = item is not None and len(item) == 2 and item[1] == rule["unit"] and math.isfinite(item[0])
        passed = bool(valid and (item[0] <= limit if rule["operator"] == "<=" else item[0] >= limit))
        verdicts.append({"metric": rule["metric"], "severity": rule["severity"], "passed": passed,
                         "reason": "compared" if valid else "missing_or_wrong_unit"})
    return {"accepted": all(v["passed"] for v in verdicts if v["severity"] == "critical"),
            "rules": verdicts}


def cost_per_successful_request(hourly_price: float, duration_seconds: float, completed_requests: int) -> float:
    if (not math.isfinite(hourly_price) or hourly_price < 0 or not math.isfinite(duration_seconds)
            or duration_seconds <= 0 or type(completed_requests) is not int or completed_requests <= 0):
        raise ValueError("finite price, positive duration and positive completed request count required")
    result = (hourly_price / 3600) * (duration_seconds / completed_requests)
    if not math.isfinite(result):
        raise ValueError("cost arithmetic exceeded finite floating-point range")
    return result


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU only")
    config = dict(dataset="teaching", dataset_revision="fixture-v1", instance="not-a-real-instance",
                  model="fixture", model_revision="v1", engine="fixture", engine_version="1",
                  input_length=10, output_length=5, concurrency=2, streaming=True, aiperf_extra_args=[],
                  benchmark_duration=60, custom_dataset_type="text", warmup=1, engine_configuration={})
    calls = []
    cache = {}
    result_for_cell(config, cache, lambda c: calls.append(c) or {"fixture_only": True})
    _, hit = result_for_cell(config, cache, only_cache=True)
    changed = {**config, "engine_configuration": {"changed": True}}
    rejected = evaluate_sla({"p95": (2000.0, "ms")}, [
        {"metric": "p95", "operator": "<=", "value": 2.5, "unit": "s", "severity": "critical"}
    ])
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"cache_hit_skips_callback": hit and len(calls) == 1,
                       "engine_change_invalidates_cache": cache_key(config) != cache_key(changed),
                       "unit_mismatch_fails_closed": not rejected["accepted"],
                       "cost_uses_seconds_per_hour": math.isclose(cost_per_successful_request(6, 60, 100), .001)},
            "metrics": {"teaching_cost_per_request": cost_per_successful_request(6, 60, 100),
                        "teaching_measurement_calls": len(calls)}}
