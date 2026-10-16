"""Recompute released Librarian compact records; no training or model calls."""
import argparse
import hashlib
import json
from pathlib import Path

from auto_research.agent_research.librarian_agents import recompute_records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, required=True)
    parser.add_argument("--resamples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=19105)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = recompute_records(args.records, resamples=args.resamples, seed=args.seed)
    result["command"] = ("PYTHONPATH=src python scripts/run_librarian_agents.py --records "
                         f"{args.records} --resamples {args.resamples} --seed {args.seed} --output {args.output}")
    result["manifest_ref"] = "agent-research:librarian-agents"
    result["seeds"] = [args.seed]
    result["evaluation_protocol"] = {
        "tier": "l0_interface", "seeds": [args.seed], "formal_comparison": False,
        "claim_policy": "Official compact records recomputation; bootstrap seed is not a new trained model seed."}
    result["provenance"] = {
        "artifact_path": str(args.output), "dataset_fingerprint": result["input_sha256"],
        "command": result["command"],
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "implementation_sha256": hashlib.sha256((Path(__file__).resolve().parents[1] /
            "src/auto_research/agent_research/librarian_agents.py").read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"scores": result["scores"], "paired_statistics": result["paired_statistics"]}))


if __name__ == "__main__":
    main()
