#!/usr/bin/env python3
"""Run fixed-definition Option-Channel evaluation on a real pinned Laya model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.system_one.contracts import ChoiceQuestion, SystemOneRequest
from auto_research.system_one.laya import LAYA_REPO_ID, LAYA_REVISION, LayaProvider
from auto_research.system_one.option_channel import evaluate_option_channel


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkpoint", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--count", type=int, default=24)
    p.add_argument("--device", default="cuda:0")
    a = p.parse_args()
    provider = LayaProvider.from_checkpoint(a.checkpoint, allow_download=False, device=a.device)

    def gate(state, instructions, criteria):
        request = SystemOneRequest(state=state, questions={"gate": ChoiceQuestion(instructions, criteria)})
        return provider.decide(request).answers["gate"].probabilities

    report = evaluate_option_channel(gate, count=a.count)
    report.update(adapter_key="option-channel-attack", diagnostic_only=True,
                  evaluation_tier="l1_mechanism",
                  checkpoint={"id": LAYA_REPO_ID, "revision": LAYA_REVISION})
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
