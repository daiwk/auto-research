from dataclasses import replace
import json
from pathlib import Path

import pytest

from auto_research.agent_research.tool_bottleneck_bench import (
    OBLIGATIONS, Sandbox, audit_discovery, compile_task, decode_records, grade_episode,
)

ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "docs/agent-research/2610.21098-tool-bottleneck-bench/validation/upstream"


def execute_public_handoffs(task, *, reverse_branches=False):
    """Diagnostic controller uses only public request and returned records."""
    sandbox = Sandbox(task)
    query = task.public()["family_id"]
    public_tools = [tool for tool in task.public()["menu"] if tool.startswith("route_main_")]
    queue, facts, sources = [(0, query)], {}, []
    while queue:
        index, query = queue.pop(0)
        locator = decode_records(sandbox.call(public_tools[index * 2], {"query": query}))[0]
        source = decode_records(sandbox.call(public_tools[index * 2 + 1], {"record_id": locator["record_id"]}))[0]
        facts.update(source["facts"])
        sources.append(source["record_id"])
        next_queries = list(enumerate(source["next_queries"], start=index + 1))
        if reverse_branches:
            next_queries.reverse()
        for index_for_query, next_query in next_queries:
            queue.append((index_for_query, next_query))
    answer = {"decision": "escalate" if facts["status"] == "overdue" and facts["commitment_date"] < "2026-10-01"
              else "do_not_escalate", "facts": facts, "sources": sources}
    return sandbox, answer


@pytest.mark.parametrize("workflow,minimum", [("low", 2), ("medium", 4), ("high", 6)])
@pytest.mark.parametrize("encoding", ["raw", "compact", "typed", "linked"])
def test_real_sandbox_executes_workflow_and_lossless_encodings(workflow, minimum, encoding):
    task = compile_task(workflow=workflow, encoding=encoding)
    sandbox, answer = execute_public_handoffs(task)
    result = grade_episode(sandbox, json.dumps(answer))
    assert task.minimum_calls == minimum
    assert result["success"] and all(result["obligations"].values())
    assert tuple(result["obligations"]) == OBLIGATIONS
    assert result["used_calls"] == minimum
    public = task.public()
    assert "facts" not in public and "decision" not in public and "records" not in public


def test_pressure_twins_keep_semantics_and_branch_order_is_not_gold_order():
    low = compile_task(workflow="low", registry_size=32, menu_size=8)
    high = compile_task(workflow="high", registry_size=2048, menu_size=128, encoding="linked")
    assert low.family_id == high.family_id and low.facts == high.facts and low.decision == high.decision
    task = compile_task(workflow="high", branching=True)
    sandbox, answer = execute_public_handoffs(task, reverse_branches=True)
    assert grade_episode(sandbox, json.dumps(answer))["success"]


def test_missing_tools_early_failure_and_truncation_keep_separate_failure_record():
    task = compile_task()
    sandbox = Sandbox(task, available_tools=[])
    sandbox.record_response(tokens=1024, completion_tokens=1024, finish_reason="length")
    result = grade_episode(sandbox, "")
    assert not result["success"]
    assert result["first_unmet_obligation"] == "availability"
    assert result["terminal_flag"] == "completion_cap"
    assert result["obligations"]["completion"] is False


def test_nine_obligations_reject_wrong_evidence_state_budget_or_forged_trace():
    task = compile_task()
    sandbox, answer = execute_public_handoffs(task)
    answer["sources"].append("unseen")
    assert grade_episode(sandbox, json.dumps(answer))["first_unmet_obligation"] == "evidence"
    sandbox, answer = execute_public_handoffs(task)
    sandbox._state[next(iter(sandbox._state))]["facts"]["status"] = "changed"
    result = grade_episode(sandbox, json.dumps(answer))
    assert not result["obligations"]["safety"] and not result["obligations"]["governance"]
    assert not result["obligations"]["workflow"]
    sandbox, answer = execute_public_handoffs(task)
    sandbox.used_tokens = 128001
    assert grade_episode(sandbox, json.dumps(answer))["terminal_flag"] == "budget_or_call_limit"
    sandbox, answer = execute_public_handoffs(task)
    sandbox._trace[1]["records"][0]["facts"]["status"] = "forged"
    assert not grade_episode(sandbox, json.dumps(answer))["obligations"]["workflow"]


def test_a_dependency_violation_fails_even_with_exact_answer():
    task = compile_task()
    sandbox = Sandbox(task)
    for step in reversed(task.steps):
        sandbox.call(step["tool"], step["arguments"])
    result = grade_episode(sandbox, json.dumps({"decision": task.decision, "facts": task.facts,
                                               "sources": [r["record_id"] for r in task.records]}))
    assert result["first_unmet_obligation"] == "workflow"


def test_official_plan_actual_rows_and_missing_response_denominator(tmp_path):
    plan = UPSTREAM / "gemini-36-flash-primary-discovery.json"
    rows = UPSTREAM / "gemini-36-flash-primary-discovery.jsonl"
    result = audit_discovery(plan, rows, resamples=100)
    assert result["planned"] == result["observed"] == 216
    assert all(row["required_tool_clusters"] == 18 for row in result["cells"].values())
    assert result["new_agent_evaluated"] is False
    lines = rows.read_text().splitlines()
    path = tmp_path / "rows.jsonl"
    path.write_text("\n".join(lines[1:]))
    missing = audit_discovery(plan, path, resamples=10)
    assert missing["planned"] == 216 and missing["observed"] == 215
    assert missing["terminal_status_counts"]["missing_response"] == 1
    path.write_text("\n".join(lines + lines[:1]))
    with pytest.raises(ValueError, match="duplicate"):
        audit_discovery(plan, path, resamples=10)


def test_distractors_are_real_empty_calls_not_evidence():
    task = compile_task()
    sandbox = Sandbox(task)
    assert decode_records(sandbox.call(task.menu[-1], {"query": task.family_id})) == []
    assert grade_episode(sandbox, "{}")["first_unmet_obligation"] == "selection"
    unavailable = replace(task, menu=task.menu[1:])
    assert grade_episode(Sandbox(unavailable), "{}")["first_unmet_obligation"] == "availability"


def test_frozen_plan_own_hash_is_verified(tmp_path):
    plan = json.loads((UPSTREAM / "gemini-36-flash-primary-discovery.json").read_text())
    plan["conditions"][0]["registry_size"] = 32
    path = tmp_path / "plan.json"
    path.write_text(json.dumps(plan))
    with pytest.raises(ValueError, match="content hash"):
        audit_discovery(path, UPSTREAM / "gemini-36-flash-primary-discovery.jsonl", resamples=10)
