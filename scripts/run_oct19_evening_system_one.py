#!/usr/bin/env python3
"""Offline protocol fixtures and published-table arithmetic; never Jev inference."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import re
import statistics
import subprocess

from auto_research.system_one.contracts import DecisionAnswer, SystemOneResponse
from auto_research.system_one.portuguese_ir import (
    Document, confusion_agreement, evaluate_rankings, kendall_tau_b, relevance_request, rerank,
)

ROOT = Path(__file__).resolve().parents[1]
# Published aggregate counts, NOT newly generated predictions or public test data.
PUBLISHED_TABLES = {
    "Quati": [[473, 518, 48, 0], [8, 273, 107, 0], [0, 45, 268, 5], [0, 1, 178, 9]],
    "JurisTCU": [[400, 22, 6, 2], [194, 224, 86, 24], [1, 122, 195, 195], [0, 72, 80, 627]],
    "NormasTCU": [[282, 197, 34], [22, 71, 52], [11, 51, 92]],
    "Ulysses-RFCorpus": [[2991, 873, 179], [504, 696, 213], [266, 848, 1635]],
}


def diagnostic(seed: int) -> dict:
    rng = random.Random(seed)
    documents = [Document(f"d{i}", f"texto   público {i}\nconteúdo", f"Título {i}") for i in range(7)]
    rng.shuffle(documents)
    # Inert assigned scores depend only on public identity, not qrels/text semantics.
    public_scores = {document.key: int(document.key[1:]) / 10 for document in documents}
    requests = []
    def provider(request):
        requests.append(request.to_dict())
        return SystemOneResponse(request.model, {key: DecisionAnswer("noul", public_scores[key] >= .5,
            {"yes": public_scores[key], "no": 1 - public_scores[key]}, max(public_scores[key], 1 - public_scores[key]))
            for key in request.questions})
    ranked, scores = rerank("consulta pública", documents, provider, depth=5, batch_size=2, text_limit=8,
                            model="fixture-only-not-jev")
    expected = tuple(sorted((d.key for d in documents[:5]), key=lambda key: -public_scores[key])) + tuple(d.key for d in documents[5:])
    assert ranked == expected and len(scores) == 5 and len(requests) == 3
    assert all(len(d["text"]) <= 8 and d["title"].startswith("Título") for r in requests for d in r["state"]["documentos"])
    assert "gold" not in json.dumps(requests) and "qrel" not in json.dumps(requests)
    request = relevance_request("consulta", documents[0], "Quati", model="fixture-only-not-jev")
    assert tuple(request.questions[documents[0].key].criteria) == ("0", "1", "2", "3")
    rejected = 0
    for kind in ("missing", "extra", "nan", "wrong-model"):
        def malformed(req):
            answer = provider(req)
            if kind == "missing":
                return SystemOneResponse(req.model, {})
            if kind == "extra":
                return SystemOneResponse(req.model, {**answer.answers, "foreign": next(iter(answer.answers.values()))})
            if kind == "wrong-model":
                return SystemOneResponse("unknown-model", answer.answers)
            return SystemOneResponse(req.model, {key: DecisionAnswer("noul", True, {"yes": float("nan"), "no": float("nan")}, 1.) for key in req.questions})
        try:
            rerank("consulta", documents, malformed, model="fixture-only-not-jev")
        except ValueError:
            rejected += 1
    assert rejected == 4
    evaluated = evaluate_rankings({"q": ("a", "b", "c")}, {"q": {"a": 1, "b": 0, "c": 3}}, cutoff=2)
    expected_dcg = 1 / (3 + 1 / math.log2(3))
    error = abs(evaluated["ndcg_at_k_linear"] - expected_dcg)
    assert error < 1e-12 and evaluated["mrr"] == 1.
    assert kendall_tau_b({"a": 2., "b": 1., "c": 1.}, {"a": 2., "b": 1., "c": 1.}) == 1.
    trace = hashlib.sha256(json.dumps(requests, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return {"metrics": {"batched_ranking_reference_errors": int(ranked != expected),
                "invalid_response_negative_controls_rejected": rejected, "linear_ndcg_reference_max_error": error,
                "scored_candidates": 5, "provider_has_gold_access": False, "real_backend_used": False,
                "language_model_evaluated": False}, "request_trace_sha256": trace}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu",), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    if not seeds or len(set(seeds)) != len(seeds) or len(seeds) > 8 or any(not 0 <= s < 2**32 for s in seeds):
        parser.error("1..8 distinct uint32 seeds required")
    if args.code_commit and not re.fullmatch(r"[0-9a-f]{40}", args.code_commit):
        parser.error("full lowercase commit required")
    if args.output.exists():
        parser.error("immutable output required")
    rows = [{"seed": seed, **diagnostic(seed)} for seed in seeds]
    sources = [Path(__file__).resolve(), ROOT / "src/auto_research/system_one/portuguese_ir.py",
               ROOT / "src/auto_research/system_one/contracts.py"]
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    payload = {"schema_version": 1, "code_commit": commit, "device": "cpu", "seeds": seeds, "accelerator": "CPU",
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "components": {"jev-portuguese-ir": {"dataset": {"id": "synthetic-portuguese-ir-protocol-fixture",
            "revision": "oct19-evening-portuguese-ir-v1", "capability_benchmark": False}, "per_seed": rows,
            "metrics": {key: statistics.mean(row["metrics"][key] for row in rows) for key in rows[0]["metrics"]
                        if type(rows[0]["metrics"][key]) in (int, float)},
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost"}},
        "published_table_arithmetic": {"source_url": "https://arxiv.org/html/2610.23346v1",
            "tables": {name: confusion_agreement(matrix) for name, matrix in PUBLISHED_TABLES.items()},
            "new_model_inference": False},
        "executed_source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "components": list(payload["components"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
