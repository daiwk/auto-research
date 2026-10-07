#!/usr/bin/env python3
"""Real two-model Circle Packing search; Linux bwrap is mandatory."""

import argparse
import json
from pathlib import Path

from auto_research.agent_research.frugalevo import FrugalEvo, SearchConfig
from auto_research.agent_research.program_sandbox import CIRCLE_INITIAL, CIRCLE_TASK, ProgramSandbox
from auto_research.agent_research.search_checkpoint import (
    FrozenGenerator, LARGE_MODEL, LARGE_REVISION, SMALL_MODEL, SMALL_REVISION,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--large-checkpoint", type=Path)
    parser.add_argument("--small-checkpoint", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--budget", type=float, default=40000)
    parser.add_argument("--max-calls", type=int, default=30)
    parser.add_argument("--max-tokens", type=int, default=768)
    parser.add_argument("--seeds", default="42,43,44")
    args = parser.parse_args()
    sandbox = ProgramSandbox()
    assert sandbox.evaluate_packing(CIRCLE_INITIAL).score > 2
    large = FrozenGenerator(LARGE_MODEL, LARGE_REVISION, path=args.large_checkpoint, token_weight=2)
    small = FrozenGenerator(SMALL_MODEL, SMALL_REVISION, path=args.small_checkpoint)
    result = {"dataset": {"name": "Circle Packing n=26, FrugalEvo public mathematical objective",
                          "source": "https://github.com/chchenhui/frugalevo/tree/82f7b739110944bf3e8737db303a302a568e7327/benchmarks/math/circle_packing",
                          "revision": "82f7b739110944bf3e8737db303a302a568e7327",
                          "local_interface": "standard-library Python -> JSON coordinates; independent geometry validator"},
              "checkpoints": [large.provenance(), small.provenance()],
              "accelerator": small.torch.cuda.get_device_name(), "runs": [],
              "boundary": "public-task local checkpoint comparison; not paper API models or USD cost reproduction; larger model is not assumed better",
              "selection": "fixed settings; direct optimization of public mathematical objective; no hidden test distribution"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for seed in map(int, args.seeds.split(",")):
        for baseline in (True, False):
            config = SearchConfig(budget=args.budget, max_calls=args.max_calls,
                                  max_tokens=args.max_tokens, seed=seed)
            controller = FrugalEvo(large, small, sandbox.evaluate_packing, config)
            run = controller.run(CIRCLE_TASK, CIRCLE_INITIAL, baseline=baseline)
            result["runs"].append(run)
            args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps({"seed": seed, "method": run["method"], "spent": run["spent"],
                              "best_score": run["best"]["score"], "calls": len(run["calls"])}), flush=True)


if __name__ == "__main__":
    main()
