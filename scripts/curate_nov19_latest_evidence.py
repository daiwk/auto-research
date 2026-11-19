"""Bind real Nov19 CPU/A100 evidence, preserving L0/L1 and immutable receipts."""

from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from oct18_frozen_sources import verify_sources
from run_nov19_latest_components import AUDIT, ROOT, config, load, source_hashes, validate_raw

_spec = importlib.util.spec_from_file_location(
    "_nov19_evidence_base", ROOT / "scripts/curate_nov18_latest_evidence.py"
)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)
_base.AUDIT = AUDIT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    frozen = load(AUDIT / "frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("execution source changed since actual run")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    raw = {d: load(AUDIT / f"raw-{d}.json") for d in ("cpu", "cuda")}
    for value in raw.values():
        validate_raw(value, frozen)
    for key, item in config()["components"].items():
        path = ROOT / f"src/auto_research/paper_specs/catalog/{item['domain']}/{key}.json"
        spec = load(path)
        if (
            spec["evaluation_tier"] != item["evaluation_tier"]
            or spec["requires_gpu_validation"] is not item["cuda"]
        ):
            raise ValueError("spec contradicts real execution scope: " + key)
        expected = f"docs/gpu-validations/{key}-a100-20261119-latest.json"
        if item["cuda"] and spec.get("gpu_validation_artifact") != expected:
            raise ValueError("wrong GPU receipt binding: " + key)
        for device in ("cpu", "cuda") if item["cuda"] else ("cpu",):
            payload = _base.metric(key, item, spec, raw[device], frozen)
            payload["dataset"]["id"] = f"synthetic:nov19-latest-{key}-component-v1"
            payload["provenance"]["dataset_fingerprint"] = (
                "sha256:"
                + hashlib.sha256(
                    json.dumps(payload["dataset"], sort_keys=True).encode()
                ).hexdigest()
            )
            _base.put(ROOT / payload["provenance"]["artifact_path"], payload, args.check)
            if device == "cuda":
                receipt = _base.receipt(key, spec, payload, frozen)
                receipt["validated_at"] = "2026-11-19"
                receipt["command"] = [
                    x.replace("run_nov18_latest_components.py", "run_nov19_latest_components.py")
                    for x in receipt["command"]
                ]
                _base.put(ROOT / expected, receipt, args.check)
        if item["cuda"]:
            if args.check and spec.get("gpu_validation_passed") is not True:
                raise ValueError("unaccepted GPU evidence: " + key)
            if not args.check:
                spec["gpu_validation_passed"] = True
                path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
    print(
        json.dumps(
            {
                "cpu_components": len(config()["components"]),
                "cuda_components": sum(x["cuda"] for x in config()["components"].values()),
                "capability_promotions": 0,
            }
        )
    )


if __name__ == "__main__":
    main()
