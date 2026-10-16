"""Offline SciPIvot audit/export/score; never invokes a model or a project condition."""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import sys

from auto_research.agent_research.scipivot import (
    UPSTREAM_REVISION, audit_release, export_options_only, score_predictions,
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
        references = json.loads(args.references.read_text())
        if len(references) != 248:
            parser.error("official scoring requires the full 248-case grader reference artifact")
        result = score_predictions(references, predictions)
    result["manifest_ref"] = "agent-research:scipivot"
    result["seeds"] = [] if args.mode != "score" else [20261004]
    result["deterministic"] = args.mode != "score"
    result["dataset"] = {
        "id": "SciPIvot/released-options-only", "revision": UPSTREAM_REVISION,
        "split": "official 248-case options-only release; project histories not released",
        "source_sha256": hashlib.sha256((args.questions or args.references).read_bytes()).hexdigest(),
        "input_role": "grader_reference_artifact" if args.mode == "score" else "official_questions"}
    if args.aggregates is not None:
        result["dataset"]["aggregate_sha256"] = hashlib.sha256(args.aggregates.read_bytes()).hexdigest()
    result["evaluation_protocol"] = {
        "tier": "l0_interface", "seeds": result["seeds"], "formal_comparison": False,
        "claim_policy": "Released options-only protocol/aggregate arithmetic audit, not new model capability."}
    result["provenance"] = {
        "artifact_path": str(args.output),
        "dataset_fingerprint": hashlib.sha256((args.questions or args.references).read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "implementation_sha256": hashlib.sha256((Path(__file__).resolve().parents[1] /
            "src/auto_research/agent_research/scipivot.py").read_bytes()).hexdigest()}
    result["provenance"]["command"] = "PYTHONPATH=src python scripts/run_scipivot.py " + shlex.join(sys.argv[1:])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
