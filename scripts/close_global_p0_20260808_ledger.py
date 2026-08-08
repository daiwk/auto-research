#!/usr/bin/env python3
"""Close every P0 item in the 2026-08-08 global audit after implementation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/paper-discovery-ledger.json"
IMPLEMENTED = {
    "2604.25291": ("glorank", "reproductions/2604.25291-glorank/README.md"),
    "2604.07420": ("dual-rerank", "reproductions/2604.07420-dual-rerank/README.md"),
    "2603.02999": ("oneranker", "reproductions/2603.02999-oneranker/README.md"),
    "2506.07261": ("radar", "reproductions/2506.07261-radar/README.md"),
    "2511.12518": ("dualgr", "reproductions/2511.12518-dualgr/README.md"),
    "2508.20400": ("mpformer", "reproductions/2508.20400-mpformer/README.md"),
    "2603.03770": ("hap", "reproductions/2603.03770-hap/README.md"),
    "2509.18091": ("onepiece", "reproductions/2509.18091-onepiece/README.md"),
    "2509.21179": ("intsr", "reproductions/2509.21179-intsr/README.md"),
    "2406.09021": ("cdm", "reproductions/2406.09021-cdm/README.md"),
    "2406.07932": ("cwm", "reproductions/2406.07932-cwm/README.md"),
    "2104.09864": ("rope", "reproductions/2104.09864-rope/README.md"),
    "2108.12409": ("alibi", "reproductions/2108.12409-alibi/README.md"),
    "2305.13245": ("gqa", "reproductions/2305.13245-gqa/README.md"),
    "2411.13676": ("hymba", "reproductions/2411.13676-hymba/README.md"),
    "2502.13189": ("moba", "reproductions/2502.13189-moba/README.md"),
    "2305.10429": ("doremi", "reproductions/2305.10429-doremi/README.md"),
    "2403.16952": ("data-mixing-laws", "reproductions/2403.16952-data-mixing-laws/README.md"),
    "2412.09871": ("blt", "reproductions/2412.09871-blt/README.md"),
    "2309.00267": ("rlaif", "post-training/2309.00267-rlaif/README.md"),
    "2305.20050": ("process-supervision", "post-training/2305.20050-process-supervision/README.md"),
    "2312.08935": ("math-shepherd", "post-training/2312.08935-math-shepherd/README.md"),
    "2401.10020": ("self-rewarding", "post-training/2401.10020-self-rewarding/README.md"),
    "2504.14945": ("luffy", "post-training/2504.14945-luffy/README.md"),
    "2504.16084": ("ttrl", "post-training/2504.16084-ttrl/README.md"),
    "2505.03335": ("absolute-zero", "post-training/2505.03335-absolute-zero/README.md"),
    "2505.19590": ("intuitor", "post-training/2505.19590-intuitor/README.md"),
    "2506.13585": ("cispo", "post-training/2506.13585-cispo/README.md"),
    "2506.24119": ("spiral", "post-training/2506.24119-spiral/README.md"),
    "2605.12969": ("conspo", "post-training/2605.12969-conspo/README.md"),
    "2504.03160": ("deepresearcher", "agent-research/2504.03160-deepresearcher/README.md"),
    "2504.11536": ("retool", "agent-research/2504.11536-retool/README.md"),
    "2504.13958": ("toolrl", "agent-research/2504.13958-toolrl/README.md"),
    "2512.17102": ("sage", "agent-research/2512.17102-sage/README.md"),
    "2602.02474": ("memskill", "agent-research/2602.02474-memskill/README.md"),
    "2603.18743": ("memento-skills", "agent-research/2603.18743-memento-skills/README.md"),
    "2604.07791": ("searl", "agent-research/2604.07791-searl/README.md"),
    "2511.16043": ("agent0", "agent-research/2511.16043-agent0/README.md"),
}


def main() -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    batch = next(item for item in data["batches"] if item["batch"] == "2026-08-08-global-theme-gap-review")
    changed = set()
    for candidate in batch["candidates"]:
        if candidate["priority"] != "P0":
            continue
        key, doc = IMPLEMENTED[candidate["id"]]
        candidate.update(status="implemented", key=key, doc=doc)
        candidate.pop("reason", None)
        changed.add(candidate["id"])
    missing = set(IMPLEMENTED) - changed
    if missing:
        raise RuntimeError(f"P0 ids absent from global ledger: {sorted(missing)}")
    LEDGER.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
