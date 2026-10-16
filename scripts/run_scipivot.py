"""Offline SciPIvot audit/export/score; never invokes a model or a project condition."""
import argparse
import hashlib
import json
from pathlib import Path

from auto_research.agent_research.scipivot import (
    audit_release, export_options_only, score_predictions,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("audit", "export", "score"))
    parser.add_argument("--questions", type=Path)
    parser.add_argument("--aggregates", type=Path)
    parser.add_argument("--public-dir", type=Path)
    parser.add_argument("--grader-dir", type=Path)
    parser.add_argument("--references", type=Path)
    parser.add_argument("--predictions", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "audit":
        result = audit_release(args.questions, args.aggregates)
    elif args.mode == "export":
        result = export_options_only(json.loads(args.questions.read_text()), args.public_dir, args.grader_dir)
    else:
        predictions = [json.loads(line) for line in args.predictions.read_text().splitlines() if line]
        result = score_predictions(json.loads(args.references.read_text()), predictions)
    result["manifest_ref"] = "agent-research:scipivot"
    result["seeds"] = [] if args.mode != "score" else [20261004]
    result["evaluation_protocol"] = {
        "tier": "l0_interface", "seeds": result["seeds"], "formal_comparison": False,
        "claim_policy": "Released options-only protocol/aggregate arithmetic audit, not new model capability."}
    result["provenance"] = {
        "artifact_path": str(args.output),
        "dataset_fingerprint": hashlib.sha256((args.questions or args.references).read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "implementation_sha256": hashlib.sha256((Path(__file__).resolve().parents[1] /
            "src/auto_research/agent_research/scipivot.py").read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
