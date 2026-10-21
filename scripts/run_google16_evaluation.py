#!/usr/bin/env python3
"""Bounded CPU demonstrations for four Google-linked evaluation components.

--fixture-demo is explicit: model callbacks in these demonstrations are authored
test doubles, never measurements of an LLM's reasoning or agent capability.
ConvApparel additionally accepts user-supplied JSON train/heldout conversations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

from auto_research.agent_research import (
    google16_convapparel as conv,
    google16_scientist_one as scientist,
    google16_simula as simula,
    google16_tfrbench as tfr,
)


def conv_demo(seed: int, document: dict | None = None) -> dict:
    def record(index, human, policy):
        return conv.Conversation(str(index), f"participant-{index}", policy, (("please blue coat thanks" if human else "certainly optimal curated attire"),), human, (("satisfaction", 0.6 if human else 0.8),))

    if document is None:
        train = [record(i, i % 2 == 0, "good") for i in range(12)]
        heldout = [record(i, i % 2 == 0, "bad") for i in range(20, 28)]
    else:
        def decode(row):
            return conv.Conversation(row["session_id"], row["participant_id"], row["policy"], tuple(row["user_turns"]), row["is_human"], tuple(sorted(row.get("annotations", {}).items())), tuple(row.get("simulator_training_sessions", ())))
        train, heldout = [decode(row) for row in document["train"]], [decode(row) for row in document["heldout"]]
    simulator_training = [conversation for conversation in train if conversation.is_human]
    if document is None:
        sessions = tuple(conversation.session_id for conversation in simulator_training)
        heldout = [replace(conversation, simulator_training_sessions=sessions) if not conversation.is_human else conversation for conversation in heldout]
    discriminator = conv.train_logistic_discriminator(train)
    report = conv.counterfactual_validation(simulator_training, heldout, discriminator, training_policy=train[0].policy, target_policy=heldout[0].policy, seed=seed)
    return {"metrics": report["hls"], "report": report, "model_calls": 0, "trained_model": "CPU logistic diagnostic, not the paper's Gemini discriminator"}


def simula_demo(seed: int) -> dict:
    budget = simula.CallBudget(80)
    taxonomy_models = simula.TaxonomyModels(
        factors=lambda instructions: ["number-range"],
        propose=lambda context: ["positive", "negative"],
        critic=lambda context, raw: raw,
        plan=lambda instructions, paths: "fixture level plan",
    )
    trees = simula.build_taxonomies("Fixture schema orchestration only", taxonomy_models, budget, depth=1)
    counter = iter(range(20))
    generation_models = simula.GenerationModels(
        strategies=lambda instructions, taxonomies: [simula.Strategy("single-factor", ("number-range",), 1)],
        scenarios=lambda instructions, mix, count: [f"fixture-{i}-{mix}" for i in range(count)],
        complexify=lambda meta: meta + " add a boundary",
        generate=lambda meta: f"authored-callback-output-{next(counter)}",
        requirements_critic=lambda meta, sample: simula.Critique(True, "authored fixture vote"),
        refine=lambda meta, sample, explanation: sample,
        correctness_critic=lambda sample: simula.Critique(True, "authored fixture correctness vote"),
        incorrectness_critic=lambda sample: simula.Critique(False, "authored independent incorrectness vote"),
    )
    report = simula.generate_dataset("Fixture schema orchestration only", trees, generation_models, budget, size=3, seed=seed)
    complexity = simula.calibrated_complexity({str(i): str(i) for i in range(6)}, lambda batch, guidance: {key: float(value) for key, value in batch}, budget, guidance="numeric fixture order, not semantic complexity", seed=seed, batch_size=3)
    return {"metrics": {"fixture_accepted_samples": len(report["samples"]), "callback_invocations": len(budget.trace), "complexity_pairs": complexity["pairwise_comparisons"]}, "report": report, "complexity": complexity, "trace": budget.trace, "model_calls": 0}


def tfr_demo(seed: int) -> dict:
    del seed
    configured = tfr.ReferenceModels(
        search=lambda view: (),
        hypotheses=lambda view: "authored fixture trend",
        verify_assumptions=lambda hypothesis, events: "fixture, not web verified",
        reason=lambda view: ("continue trend", "flat"),
        forecast=lambda view: [[5], [6]] if "trend" in view.reasoning else [[4], [4]],
        consistency=lambda trace, forecast: 4,
        diagnose=lambda candidate: "authored fixture feedback",
        summarize=lambda trace: trace,
        select=lambda candidates: min(range(len(candidates)), key=lambda index: (candidates[index].mase, -candidates[index].consistency)),
    )
    report = tfr.build_reference(history=tfr.matrix([[1], [2], [3], [4]]), target=tfr.matrix([[5], [6]]), models=configured)
    return {"metrics": {"fixture_candidates": len(report["candidates"]), "fixture_selected_mase": report["selected"]["mase"], "fixture_summary_mase": report["summary_mase"]}, "report": report, "model_calls": 0}


def scientist_demo(seed: int) -> dict:
    del seed
    values = [{"metric": "fixture_score", "value": 0.7, "stage": "validation", "unit": "fraction", "direction": "max"}]
    payload = json.dumps({"measurements": values}, sort_keys=True).encode()
    log = scientist.Artifact.from_bytes("execution-log", payload, "execution_log")
    claims = [scientist.Claim("numeric", "numerical", (log.key,), **values[0]), scientist.Claim("citation", "citation", ("missing-reference",))]
    measurement = scientist.Measurement(log.key, **values[0])
    provenance = scientist.numerical_cpr(claims, [measurement], [log], {log.key: payload})
    code, evaluator = b"fixture pure function", b"fixture canonical evaluator"
    audit = scientist.score_verification(scientist.Measurement("paper", "fixture_score", 0.7, "test", "fraction", "max"), solution=scientist.Artifact.from_bytes("solution", code, "code"), solution_bytes=code, evaluator=scientist.Artifact.from_bytes("evaluator", evaluator, "evaluator"), evaluator_bytes=evaluator, evaluate=lambda source, judge, index: scientist.Measurement("rerun", "fixture_score", 0.7, "test", "fraction", "max"))
    return {"metrics": {"fixture_numerical_cpr": provenance["cpr"], "canonical_evaluator_reruns": audit["reruns"]}, "report": {"provenance": provenance, "score_audit": audit, "i2": scientist.majority_audit([], pass_verdict="clean", fail_verdict="flagged"), "i3": scientist.reference_verification(reference_id="missing", resolve=None, disambiguate=None), "i4": scientist.majority_audit([], pass_verdict="aligned", fail_verdict="misaligned")}, "model_calls": 0}


COMPONENTS = {"convapparel": conv_demo, "simula": simula_demo, "tfrbench": tfr_demo, "scientist-one": scientist_demo}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--component", choices=COMPONENTS, required=True)
    parser.add_argument("--fixture-demo", action="store_true")
    parser.add_argument("--input", type=Path, help="ConvApparel train/heldout JSON; never sent to a model service")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.fixture_demo == bool(args.input):
        parser.error("choose exactly one of --fixture-demo and --input")
    if args.input and args.component != "convapparel":
        parser.error("external model roles use the typed Python callback API; --input is ConvApparel-only")
    if args.output.exists() or args.output.is_symlink():
        parser.error("output must be a new immutable path")
    document = json.loads(args.input.read_text()) if args.input else None
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        try:
            report = conv_demo(args.seed, document) if args.component == "convapparel" else COMPONENTS[args.component](args.seed)
            result = {"schema_version": 2, "method": args.component, "manifest_ref": f"agent-research:{args.component}", "protocol_id": f"google16-{args.component}-cpu-v1", "evaluation_tier": "l0_interface" if args.fixture_demo else "l1_mechanism", "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False, "full_experiment_status": "not_reproduced_high_cost", "seeds": [args.seed], "device": "cpu", "dataset": {"id": "self-authored-protocol-fixtures" if args.fixture_demo else "user-supplied-conversations", "public_benchmark": False, "revision": hashlib.sha256(args.input.read_bytes()).hexdigest() if args.input else "google16-evaluation-fixtures-v1"}, "fixture_demo": args.fixture_demo, "status": "completed", **report}
        except Exception as error:
            json.dump({"status": "failed", "diagnostic_only": True, "error_type": type(error).__name__, "error": str(error)}, handle, indent=2)
            handle.write("\n")
            raise
        json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"component": args.component, "status": result["status"], "metrics": result["metrics"], "fixture_demo": args.fixture_demo}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
