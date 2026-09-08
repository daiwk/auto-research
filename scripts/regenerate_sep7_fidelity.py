"""Replace invalid September 7 diagnostics by executing corrected CPU paths."""
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess

from auto_research.agent_research import AgentResearchConfig, AgentResearchRunner
from auto_research.reproductions.latest_20260907 import reproduce
from auto_research.reproductions.industrial_2026 import load_industrial_data


ROOT = Path(__file__).resolve().parents[1]


def main():
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    seeds = [42, 43, 44]
    data = load_industrial_data(ROOT / "data")
    fingerprint = hashlib.sha256(json.dumps({"train": data.sequences.train,
        "validation": data.sequences.validation, "test": data.sequences.test},
        default=lambda x: x.tolist(), sort_keys=True).encode()).hexdigest()
    entries = {"allecompanion": "reproductions/2609.05063-allecompanion",
               "autolr": "reproductions/2609.04871-autolr",
               "atomrec": "agent-research/2609.04882-atomrec",
               "coskill": "agent-research/2609.04865-coskill",
               "silr": "agent-research/2609.04629-silr",
               "multi-harness-rl": "agent-research/2609.04518-multi-harness-rl"}
    for method, directory in entries.items():
        recommendation = directory.startswith("reproductions")
        filename = "movielens-100k-seeds42-44.json" if recommendation else "mini-suite-seeds42-44.json"
        path = ROOT / "docs" / directory / "metrics" / filename
        runs = []
        for seed in seeds:
            if recommendation:
                result = reproduce(method, ROOT / "data", seed)
            else:
                result, _ = AgentResearchRunner(AgentResearchConfig(
                    method=method, benchmark="evomem-mini", episodes=120,
                    memory_size=24, seed=seed, output_dir=ROOT / "runs/agent-research")).run()
                result = asdict(result)
            runs.append(result)
        payload = {"schema_version": 2, "method": method,
            "dataset": "MovieLens 100K" if recommendation else "evomem-mini",
            "seeds": seeds, "runs": runs,
            "manifest_ref": f"reproduction:{method}" if recommendation else "agent-research:evomem-mini-seeds42-44",
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": seeds,
                "formal_comparison": False,
                "claim_policy": "CPU mechanism diagnostic; no production or LLM capability claim"},
            "provenance": {"commit": commit, "artifact_path": str(path.relative_to(ROOT)),
                "dataset_fingerprint": fingerprint if recommendation else "evomem-mini-generator-seeds42-44-120-episodes",
                "command": "PYTHONPATH=src python scripts/regenerate_sep7_fidelity.py"},
            "correction": "Previous heuristic/oracle-based result withdrawn; this artifact executes corrected paths."}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        print(method, "regenerated", flush=True)


if __name__ == "__main__":
    main()
