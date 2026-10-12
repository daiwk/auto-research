"""Explicit experiment entrypoints; CUDA runs remain L1 diagnostics."""
from __future__ import annotations
from dataclasses import asdict
import json
import hashlib
import math
from pathlib import Path
import re

from .oct12_checkpoint import (CheckpointPolicy, Evo2Policy, HarnessEvaluator, GSMHarnessEvaluator,
    INITIAL_PROMPT, GSM_INITIAL_PROMPT, ATTENTION_BACKENDS,
    JanusBackend, RSIBackend, harness_source, make_factorized_predictor)
from .oct12_evolution import Evaluation, Evo2, Janus, RSIAnything
from .oct12_memory_tools import DualEncoder, RATED, T2Mem, WorkflowOutcome, audit_workflows
from .program_sandbox import CIRCLE_INITIAL, CIRCLE_TASK, ProgramSandbox
from .oct12_provenance import verify_local_checkpoint


METHODS = ("evo2", "rsi-anything", "janus", "t2mem", "rated", "jev-workflow")
ENVIRONMENTS = ("circle-packing", "gsm8k-harness")


def active_grpo_update(row):
    """Parameter drift from historical optimizer state is not new learning."""
    return bool(row.get("updated") and row.get("parameters_changed") and
                math.isfinite(row.get("gradient_norm",0.)) and row.get("gradient_norm",0.) > 0.)


def active_sft_update(row):
    return bool(row.get("parameters_changed") and any(
        math.isfinite(step.get("gradient_norm",0.)) and step.get("gradient_norm",0.) > 0.
        for step in row.get("steps",[])))


def load_jsonl(path):
    if path is None:
        raise ValueError("this method requires an explicit public dataset")
    rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
    if not rows:
        raise ValueError("empty dataset")
    return rows


def run_method(method, *, checkpoint=None, dataset=None, device="cpu", seed=42,
               rounds=2, group_size=2, max_tokens=256, train_steps=2,
               query_checkpoint=None, tool_checkpoint=None,checkpoint_id=None,checkpoint_revision=None,
               executor_checkpoint=None,executor_id=None,executor_revision=None,
               query_checkpoint_id=None,query_checkpoint_revision=None,
               tool_checkpoint_id=None,tool_checkpoint_revision=None,
               environment="circle-packing",evaluation_examples=8,executor_max_tokens=None,
               attention_backend="eager"):
    if method not in METHODS:
        raise ValueError("unknown October agent method")
    if attention_backend not in ATTENTION_BACKENDS:
        raise ValueError("attention_backend must be eager or sdpa")
    if attention_backend != "eager" and method in {"rated","jev-workflow"}:
        raise ValueError("attention_backend selection is supported only by causal-checkpoint agent paths")
    if environment not in ENVIRONMENTS or (environment != "circle-packing" and method != "evo2"):
        raise ValueError("non-default environment is supported only for Evo2")
    if executor_max_tokens is not None and (method != "evo2" or executor_max_tokens < 1):
        raise ValueError("positive executor_max_tokens is supported only for Evo2")
    if method not in {"rated", "jev-workflow"} and not checkpoint:
        raise ValueError("local checkpoint required")
    settings = {"device": device, "seed": seed, "max_tokens": max_tokens,
                "attention_backend":attention_backend}
    actual_attention_backend = None
    provenance = {}
    if method not in {"rated","jev-workflow"}:
        provenance["policy"] = verify_local_checkpoint(checkpoint,checkpoint_id,checkpoint_revision)
    if method == "evo2":
        executor_checkpoint = executor_checkpoint or checkpoint
        provenance["executor"] = verify_local_checkpoint(executor_checkpoint,
            executor_id or checkpoint_id,executor_revision or checkpoint_revision)
    if method == "rated":
        provenance["query_encoder"] = verify_local_checkpoint(query_checkpoint,
            query_checkpoint_id,query_checkpoint_revision)
        provenance["tool_encoder"] = verify_local_checkpoint(tool_checkpoint,
            tool_checkpoint_id,tool_checkpoint_revision)
    if method == "evo2":
        policy = Evo2Policy(checkpoint, **settings)
        executor = CheckpointPolicy(executor_checkpoint, **{**settings,
            "max_tokens":executor_max_tokens if executor_max_tokens is not None else max_tokens})
        actual_attention_backend = policy.attention_backend
        if environment == "gsm8k-harness":
            evaluator = GSMHarnessEvaluator(executor,dataset,examples=evaluation_examples)
            initial_prompt = GSM_INITIAL_PROMPT
        else:
            evaluator,initial_prompt = HarnessEvaluator(executor),INITIAL_PROMPT
        controller = Evo2(policy, evaluator, {"agent.py": harness_source(initial_prompt)}, seed=seed)
        result = controller.train(warmup_iterations=2, rounds=rounds, group_size=group_size,
                                  steps=train_steps)
        result.update(evaluator.frozen_audit())
        if not active_sft_update(result["warmup"]) or not any(
                active_grpo_update(row) for row in result["training"]):
            result["status"] = "failed"
            result["failure_reason"] = "Evo2 did not complete active SFT and GRPO parameter updates"
        result["environment"] = "gsm8k-harness" if environment == "gsm8k-harness" else "public-circle-packing-26"
        result["policy_max_tokens"] = max_tokens
        result["executor_max_tokens"] = executor.max_tokens
        result["executor_attention_backend"] = executor.attention_backend
        if environment == "gsm8k-harness":
            result["dataset"] = evaluator.dataset_provenance
            result["evaluation_examples"] = evaluator.evaluation_examples
            result["validation_selection"] = "first N rows of verified train-only validation partition; no test read"
        result["harness_restriction"] = "executable source edits limited to arbitrary generated PROMPT"
        result["scores"] = [{"id": node.identifier, "normalized_score": node.evaluation.score,
            "raw_geometry_score": next((t["raw_geometry_score"] for t in node.evaluation.trace
                                         if "raw_geometry_score" in t), None),
            "external_feedback":[t.get("feedback",t.get("error")) for t in node.evaluation.trace],
            "generated_program_sha256":next((hashlib.sha256(t["generated_program"].encode()).hexdigest()
                for t in node.evaluation.trace if "generated_program" in t),None)} for node in controller.nodes]
        if environment == "gsm8k-harness":
            for item,node in zip(result["scores"],controller.nodes):
                item["external_scoring_trace"] = list(node.evaluation.trace)
    elif method == "rsi-anything":
        backend = RSIBackend(checkpoint, **settings)
        actual_attention_backend = backend.attention_backend
        sandbox = ProgramSandbox()
        dimension = backend.embedding(CIRCLE_TASK).numel()
        predictor = make_factorized_predictor(dimension, device)
        def verify(context, code):
            evaluated = sandbox.evaluate_packing(code)
            return Evaluation(min(1., evaluated.score / math.sqrt(26 / math.pi)),
                ({"raw_geometry_score": evaluated.score, "feedback": evaluated.feedback},))
        controller = RSIAnything(backend, verify, initial_workflow=INITIAL_PROMPT, predictor=predictor)
        # Declared context variants are separate model inputs, not official
        # generalization partitions; no task answer or solved packing is supplied.
        result = controller.run([CIRCLE_TASK + "\nTraining context: geometric solver exploration."],
            [CIRCLE_TASK + "\nValidation context: independently verify all 26 constraints."],
            rounds=rounds, candidates=group_size, adaptation_steps=train_steps)
        result["environment"] = "public-circle-packing-26"
        result["split_limitation"] = "single-task context partition; not independent capability validation"
    elif method == "janus":
        backend = JanusBackend(checkpoint, **settings)
        actual_attention_backend = backend.attention_backend
        initial = ProgramSandbox().evaluate_packing(CIRCLE_INITIAL)
        controller = Janus(backend, backend.execute, initial_evidence={"score": initial.score,
                                                                     "feedback": initial.feedback})
        result = controller.run(budget=rounds, candidates=group_size)
        result["environment"] = "public-circle-packing-26"
    elif method == "t2mem":
        backend = CheckpointPolicy(checkpoint, **settings)
        actual_attention_backend = backend.attention_backend
        outputs = []
        for row in load_jsonl(dataset):
            if not row.get("source_revision") or not isinstance(row.get("question"), str):
                raise ValueError("memory records require public source_revision and question")
            sessions = row["sessions"]
            if isinstance(sessions, list):
                sessions = {str(i): item if isinstance(item, str) else json.dumps(item)
                            for i, item in enumerate(sessions)}
            memory = T2Mem(backend, sessions, top_k=2, max_steps=rounds)
            output = memory.answer(row["question"])
            # Gold only reaches this post-generation scorer, never T2Mem.
            if "answer" in row:
                gold = set(re.findall(r"\w+", str(row["answer"]).lower()))
                predicted = set(re.findall(r"\w+", output["answer"].lower()))
                overlap = len(gold & predicted)
                output["external_token_f1"] = 2 * overlap / max(1, len(gold) + len(predicted))
            outputs.append(output)
        result = {"queries": len(outputs), "outputs": outputs,
                  "scoring_limitation": "external token F1, not original LLM-judge accuracy"}
    elif method == "rated":
        payload = json.loads(Path(dataset).read_text())
        if not payload.get("source_revision"):
            raise ValueError("public tool dataset revision required")
        if not query_checkpoint or not tool_checkpoint:
            raise ValueError("two local semantic encoder checkpoints required")
        encoder = DualEncoder(query_checkpoint, tool_checkpoint, device=device, seed=seed)
        training = encoder.fit(payload["pairs"], steps=train_steps)
        sandbox = ProgramSandbox()
        tools = payload["tools"]
        def execute(identifier, query):
            tool = tools[identifier]
            if "code" not in tool:
                raise ValueError("execution requires explicitly authorized safe local tool binding")
            code = "QUERY = " + repr(query) + "\n" + tool["code"]
            output, error, status = sandbox.execute(code)
            if error.startswith("bwrap:") or "Operation not permitted" in error:
                raise RuntimeError("sandbox setup failed: " + error)
            # Execution correctness is trusted process+schema evidence; no tool's
            # self-declared reward is used. Semantic match is separately scored.
            try:
                valid_output = isinstance(json.loads(output), dict)
            except ValueError:
                valid_output = False
            return {"success": status == 0 and valid_output, "error": error if status else None}
        queries = payload["queries"]
        if any(row.get("split") != "test" for row in queries):
            raise ValueError("final retrieval stream must be explicit isolated test split")
        train_queries = {row["query"] for row in payload["pairs"]}
        if train_queries & {row["query"] for row in queries}:
            raise ValueError("train/test queries overlap")
        controller = RATED(encoder, tools, execute)
        result = controller.run(queries)
        result["contrastive_training"] = training
        result["execution_binding"] = "approved local tool source in Linux bubblewrap; not original production APIs"
        if all("reference_tool" in row for row in queries):
            result["external_semantic_recall_at_1"] = sum(
                record["selected"] in (row["reference_tool"] if isinstance(row["reference_tool"],list)
                    else [row["reference_tool"]]) for record, row in
                zip(result["history"], queries)) / len(queries)
    else:
        rows = load_jsonl(dataset)
        result = audit_workflows([WorkflowOutcome(**row) for row in rows])
        result["source"] = "caller-supplied actual measured execution records"
    result.update({"method": method, "seed": seed, "diagnostic_only": True,
        "evaluation_tier": "L1", "device": device, "checkpoint": provenance,
        "attention_backend":actual_attention_backend,
        "capability_comparison": False, "evolve_promotion_eligible": False})
    return result


def reproduce_config(key, dataset_dir, seed):
    config = json.loads((Path(dataset_dir) / "oct12.json").read_text())
    if config.pop("method", key) != key:
        raise ValueError("configuration method differs from adapter key")
    if config.get("dataset") and not Path(config["dataset"]).is_absolute():
        config["dataset"] = str(Path(dataset_dir) / config["dataset"])
    return run_method(key, seed=seed, **config)


def render_result(result):
    return "# October agent runtime diagnostic\n\n> L1 diagnostic; not original-paper capability evidence.\n\n```json\n" + json.dumps(
        result, ensure_ascii=False, indent=2) + "\n```\n"
