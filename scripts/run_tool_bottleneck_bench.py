"""Offline official discovery ITT audit (not a new agent evaluation)."""
import argparse
import hashlib
import json
from pathlib import Path

from auto_research.agent_research.tool_bottleneck_bench import audit_discovery


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--rows", type=Path, required=True)
    parser.add_argument("--resamples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit_discovery(args.plan, args.rows, resamples=args.resamples, seed=args.seed)
    result["command"] = ("PYTHONPATH=src python scripts/run_tool_bottleneck_bench.py "
                         f"--plan {args.plan} --rows {args.rows} --resamples {args.resamples} "
                         f"--seed {args.seed} --output {args.output}")
    result["manifest_ref"] = "agent-research:tool-bottleneck-bench"
    result["seeds"] = [args.seed]
    result["evaluation_protocol"] = {
        "tier": "l0_interface", "seeds": [args.seed], "formal_comparison": False,
        "claim_policy": "Official single-configuration discovery recomputation, not new Agent capability."}
    result["provenance"] = {
        "artifact_path": str(args.output),
        "dataset_fingerprint": ":".join(row["sha256"] for row in result["inputs"]),
        "command": result["command"],
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "implementation_sha256": hashlib.sha256((Path(__file__).resolve().parents[1] /
            "src/auto_research/agent_research/tool_bottleneck_bench.py").read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
