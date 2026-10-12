"""Run explicitly configured October agent checkpoints or paired trace audits."""
import argparse
import json
from pathlib import Path
from auto_research.agent_research.oct12_entrypoint import METHODS, run_method


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=METHODS, required=True)
    parser.add_argument("--checkpoint")
    parser.add_argument("--checkpoint-id")
    parser.add_argument("--checkpoint-revision")
    parser.add_argument("--executor-checkpoint")
    parser.add_argument("--executor-id")
    parser.add_argument("--executor-revision")
    parser.add_argument("--query-checkpoint")
    parser.add_argument("--tool-checkpoint")
    for role in ("query","tool"):
        parser.add_argument("--"+role+"-checkpoint-id")
        parser.add_argument("--"+role+"-checkpoint-revision")
    parser.add_argument("--dataset", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--rounds", type=int, default=2)
    parser.add_argument("--group-size", type=int, default=2)
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--train-steps", type=int, default=2)
    arguments = vars(parser.parse_args())
    output = arguments.pop("output")
    if output.exists():
        raise ValueError("choose a new immutable result path")
    try:
        result = run_method(**arguments)
    except (RuntimeError,ValueError,OSError) as error:
        result = {"status":"failed","failure_reason":str(error),"method":arguments["method"],
                  "seed":arguments["seed"],"diagnostic_only":True,"capability_comparison":False}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key not in
                      {"audit", "graph", "history", "outputs", "skills"}}, ensure_ascii=False))
    if result.get("status") == "failed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
