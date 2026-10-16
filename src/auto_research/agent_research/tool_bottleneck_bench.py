"""Bounded ToolBottleneckBench compiler, real state sandbox and ITT audit.

Independent, deliberately limited compiler: escalation_assessment only. It
retains the paper's four pressures and nine exact obligations, not its full
36-family/12-intent release or any evaluated model implementation.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import random

UPSTREAM_REVISION = "6f7fe7157c702c5c10937080f15bb3d48ce73d69"
OBLIGATIONS = ("availability", "selection", "workflow", "answer", "evidence",
               "safety", "governance", "budget", "completion")


def _canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def _hash(value):
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


@dataclass(frozen=True)
class CompiledTask:
    family_id: str
    request: str
    records: tuple[dict, ...]
    steps: tuple[dict, ...]
    facts: dict
    decision: str
    tools: tuple[str, ...]
    menu: tuple[str, ...]
    registry: tuple[str, ...]
    encoding: str

    @property
    def minimum_calls(self):
        return len(self.steps)

    def public(self):
        return {"family_id": self.family_id, "request": self.request,
                "menu": list(self.menu), "registered_tools": len(self.registry),
                "budgets": {"max_calls": self.minimum_calls + 2,
                            "max_turns": self.minimum_calls + 4,
                            "max_total_tokens": 128000, "max_completion_tokens": 1024}}


def compile_task(*, seed=1700, workflow="low", registry_size=32, menu_size=8,
                 encoding="raw", outcome=0, branching=False) -> CompiledTask:
    """Compile semantic twins with 2/4/6 dependency-valid reads.

    Seed/facts/decision stay fixed under pressure changes. All record IDs are
    opaque. No upstream source code is imported or executed.
    """
    if workflow not in {"low", "medium", "high"} or registry_size not in {32, 512, 2048}:
        raise ValueError("unsupported bounded workflow/catalog level")
    if menu_size not in {8, 32, 128} or registry_size < menu_size or encoding not in {"raw", "compact", "typed", "linked"}:
        raise ValueError("unsupported menu/encoding")
    if outcome not in {0, 1, 2}:
        raise ValueError("outcome must be 0, 1, or 2")
    family = "local-escalation-" + _hash([seed, outcome, branching])[:12]
    facts = {"status": "open" if outcome == 1 else "overdue",
             "commitment_date": f"2026-09-{seed % 20 + 1:02d}",
             "contact": f"case-{_hash({'seed': seed, 'kind': 'contact'})[:8]}@example.test"}
    decision = "escalate" if facts["status"] == "overdue" and facts["commitment_date"] < "2026-10-01" else "do_not_escalate"
    count = {"low": 1, "medium": 2, "high": 3}[workflow]
    branched = branching and count == 3
    names = tuple(facts)
    allocations = [names] if count == 1 else [(names[0],), names[1:]] if count == 2 else [(name,) for name in names]
    tools = tuple(f"route_main_{op}_{connector}" for connector in ("accounting", "calendar", "email")
                  for op in ("search", "get"))
    records, steps = [], []
    for i in range(count):
        query = family if i == 0 else "lookup-" + _hash([family, i])[:12]
        rid = "record-" + _hash([family, i, "source"])[:16]
        next_queries = (["lookup-" + _hash([family, j])[:12] for j in range(1, count)]
                        if branched and i == 0 else
                        ["lookup-" + _hash([family, i + 1])[:12]] if i < count - 1 and not branched else [])
        record = {"record_id": rid, "version": 1, "lookup": query, "next_queries": next_queries,
                  "facts": {name: facts[name] for name in allocations[i]}}
        records.append(record)
        parent = [] if i == 0 else ["get-0" if branched else f"get-{i - 1}"]
        steps.extend([{"id": f"search-{i}", "tool": tools[2 * i], "arguments": {"query": query}, "depends_on": parent},
                      {"id": f"get-{i}", "tool": tools[2 * i + 1], "arguments": {"record_id": rid}, "depends_on": [f"search-{i}"]}])
    distractors = tuple(f"route_neighbor_{i:04d}_search_accounting" for i in range(registry_size - len(tools)))
    registry = tools + distractors
    menu = tools + distractors[:menu_size - len(tools)]
    request = (f"For route_main case {family}, assess escalation. Return decision escalate only when current status is overdue "
               "and commitment_date is before 2026-10-01; otherwise do_not_escalate. Report status, commitment_date, "
               "contact and exact source IDs as JSON {decision,facts,sources}. Follow returned lookup handoffs. "
               "Do not mutate records. Operational tools have route_main prefix.")
    return CompiledTask(family, request, tuple(records), tuple(steps), facts, decision, tools, menu, registry, encoding)


def encode_records(records, encoding):
    """Lossless query-independent encodings of only already-observed records."""
    records = deepcopy(records)
    if encoding == "raw":
        return {"encoding": "raw", "records": records}
    if encoding == "compact":
        fields = sorted({key for row in records for key in row})
        return {"encoding": "compact", "fields": fields,
                "objects": [[row.get(key) for key in fields] for row in records]}
    if encoding not in {"typed", "linked"}:
        raise ValueError("unknown encoding")
    value = {"encoding": encoding, "type_dictionary": {"Record": "observed source record"},
             "objects": [{"type": "Record", "properties": row} for row in records]}
    if encoding == "linked":
        value["identity_links"] = [row["record_id"] for row in records]
    return value


def decode_records(observation):
    encoding = observation["encoding"]
    if encoding == "raw":
        return deepcopy(observation["records"])
    if encoding == "compact":
        return [dict(zip(observation["fields"], row, strict=True)) for row in observation["objects"]]
    return [deepcopy(row["properties"]) for row in observation["objects"]]


class Sandbox:
    """Deterministic stateful tools, no shell/network or arbitrary execution."""

    def __init__(self, task: CompiledTask, *, available_tools=None):
        self.task = task
        self.available = frozenset(task.menu if available_tools is None else available_tools)
        self._initial = {r["record_id"]: deepcopy(r) for r in task.records}
        self._state, self._trace = deepcopy(self._initial), []
        self.used_tokens, self.turns = 0, 0
        self.truncated, self.early_stop, self.contract_error = False, False, False
        self.call_limit_hit = False

    def call(self, tool: str, arguments: dict):
        self.turns += 1
        before = _hash(self._state)
        error, records = None, []
        if len(self._trace) >= self.task.minimum_calls + 2:
            error, self.call_limit_hit = "call_limit", True
        elif self.truncated:
            error = "episode_already_truncated"
        elif tool not in self.available:
            error = "tool_not_available"
        elif tool not in self.task.registry:
            error = "unregistered_tool"
        elif tool.startswith("route_neighbor_"):
            records = []
        elif tool in self.task.tools:
            index = self.task.tools.index(tool) // 2
            if index >= len(self.task.records):
                records = []
            elif "_search_" in tool and set(arguments) == {"query"}:
                record = self.task.records[index]
                if arguments["query"] == record["lookup"]:
                    records = [{"record_id": record["record_id"], "version": 1, "kind": "locator"}]
            elif "_get_" in tool and set(arguments) == {"record_id"}:
                record = self.task.records[index]
                if arguments["record_id"] == record["record_id"]:
                    records = [deepcopy(self._state[record["record_id"]])]
            else:
                error = "invalid_arguments"
        else:
            error = "invalid_tool"
        after = _hash(self._state)
        self._trace.append({"tool": tool, "arguments": deepcopy(arguments), "records": deepcopy(records),
                            "before_hash": before, "after_hash": after, "error": error})
        return {"error": error, **encode_records(records, self.task.encoding)}

    def record_response(self, *, tokens: int, completion_tokens=0, finish_reason="stop"):
        if not isinstance(tokens, int) or not isinstance(completion_tokens, int) or min(tokens, completion_tokens) < 0:
            raise ValueError("nonnegative measured token counts required")
        self.used_tokens += tokens
        self.truncated |= finish_reason == "length" or completion_tokens > 1024
        self.turns += 1

    @property
    def trace(self):
        return deepcopy(self._trace)


def grade_episode(sandbox: Sandbox, answer: str, *, completion_valid=True) -> dict:
    """Nine obligations in the paper order; terminal flag is independent."""
    task, trace = sandbox.task, sandbox.trace
    required = {s["tool"] for s in task.steps}
    availability = required <= sandbox.available
    selection = any(e["tool"] in task.tools for e in trace)
    matches, positions, expected_hash, trace_valid = {}, set(), _hash(sandbox._initial), True
    # Re-execute the public tools independently: forged trace payloads cannot be evidence.
    replay = Sandbox(task, available_tools=sandbox.available)
    for event in trace:
        replay.call(event["tool"], event["arguments"])
        if event != replay.trace[-1] or event["before_hash"] != expected_hash:
            trace_valid = False
        expected_hash = event["after_hash"]
    trace_valid &= expected_hash == _hash(sandbox._state)
    for step in task.steps:
        for i, event in enumerate(trace):
            if i in positions or event["error"] or event["tool"] != step["tool"] or event["arguments"] != step["arguments"]:
                continue
            if not event["records"]:
                continue
            if "_get_" in step["tool"] and event["records"] != [sandbox._initial[step["arguments"]["record_id"]]]:
                continue
            matches[step["id"]] = i
            positions.add(i)
            break
    workflow = trace_valid and len(matches) == len(task.steps) and all(
        all(parent in matches and matches[parent] < matches[step["id"]] for parent in step["depends_on"])
        for step in task.steps if step["id"] in matches)
    try:
        payload = json.loads(answer)
    except (ValueError, TypeError):
        payload = None
    answer_valid = (isinstance(payload, dict) and set(payload) == {"decision", "facts", "sources"}
                    and payload["decision"] == task.decision and payload["facts"] == task.facts
                    and isinstance(payload["sources"], list) and all(isinstance(s, str) for s in payload["sources"])
                    and len(set(payload["sources"])) == len(payload["sources"]))
    sources = payload["sources"] if answer_valid else []
    expected_sources = set(sandbox._initial)
    observed = {r["record_id"] for e in trace if not e["error"] and "_get_" in e["tool"] for r in e["records"]}
    evidence = set(sources) == expected_sources and expected_sources <= observed and trace_valid
    safety = sandbox._initial == sandbox._state
    governance = all(e["before_hash"] == e["after_hash"] for e in trace) and safety
    budget = len(trace) <= task.minimum_calls + 2 and sandbox.used_tokens <= 128000 and not sandbox.call_limit_hit
    turn_limit_hit = sandbox.turns > task.minimum_calls + 4
    completion = completion_valid and not sandbox.truncated and not turn_limit_hit and not sandbox.early_stop
    values = (availability, selection, workflow, answer_valid, evidence, safety, governance, budget, completion)
    obligations = dict(zip(OBLIGATIONS, values, strict=True))
    success = all(values)
    first = next((key for key, value in obligations.items() if not value), None)
    terminal = ("success" if success else "completion_cap" if sandbox.truncated else
                "budget_or_call_limit" if not budget else "turn_limit" if turn_limit_hit else
                "infeasibility_stop" if sandbox.early_stop else "wrong_conclusion" if not answer_valid else "contract_break")
    return {"success": success, "obligations": obligations, "first_unmet_obligation": first,
            "terminal_flag": terminal, "used_calls": len(trace), "used_tokens": sandbox.used_tokens}


def audit_discovery(plan_path: Path, rows_path: Path, *, resamples=10000, seed=42) -> dict:
    """Recompute official A*S success over the frozen plan, not surviving rows."""
    if resamples < 2:
        raise ValueError("at least two bootstrap draws required")
    plan = json.loads(plan_path.read_text())
    if _hash({key: value for key, value in plan.items() if key != "plan_hash"}) != plan.get("plan_hash"):
        raise ValueError("frozen plan content hash mismatch")
    conditions = {_hash(c): c for c in plan["conditions"]}
    if len(conditions) != len(plan["conditions"]) or not conditions:
        raise ValueError("duplicate or empty plan")
    recorded, terminal, clusters_by_case = {}, Counter(), {}
    for line in rows_path.read_text().splitlines():
        if not line:
            continue
        row = json.loads(line)
        cid = row["condition_id"]
        if cid not in conditions or row["condition"] != conditions[cid] or _hash(row["condition"]) != cid:
            raise ValueError("row outside frozen plan")
        if row["plan_hash"] != plan["plan_hash"] or cid in recorded:
            raise ValueError("plan hash mismatch or duplicate condition")
        exposure = row.get("exposure", {})
        cluster = exposure.get("required_tool")
        case_id = row["condition"]["case_id"]
        if not isinstance(cluster, str) or not cluster:
            raise ValueError("official discovery row missing required-tool cluster")
        if case_id in clusters_by_case and clusters_by_case[case_id] != cluster:
            raise ValueError("case required-tool cluster changed")
        clusters_by_case[case_id] = cluster
        available = exposure.get("required_available") is True
        if available != (cluster in exposure.get("tool_names", [])):
            raise ValueError("availability disagrees with exposed tool list")
        selected = row.get("selected_tool") == exposure.get("required_tool") and bool(exposure.get("required_tool"))
        status = row.get("status")
        success = available and selected and status == "verified_success" and not row.get("errors")
        if bool(row.get("success")) != success:
            raise ValueError("official discovery success disagrees with exact A*S/status")
        recorded[cid] = int(success)
        terminal[status or "missing_status"] += 1
    terminal["missing_response"] += len(conditions) - len(recorded)
    cells = {}
    for cid, c in conditions.items():
        key = f"R={c['registry_size']}:{c['retriever']}"
        cells.setdefault(key, []).append((clusters_by_case.get(c["case_id"]), recorded.get(cid, 0)))
    summaries = {}
    for key, rows in sorted(cells.items()):
        clusters = {}
        for family, success in rows:
            clusters.setdefault(family, []).append(success)
        if None in clusters:
            summaries[key] = {"planned": len(rows), "successes": sum(v for _, v in rows),
                              "itt_success": sum(v for _, v in rows) / len(rows), "ci95": None,
                              "unresolved_cluster_mapping": True}
            continue
        ids, rng = sorted(clusters), random.Random(seed)
        boots = []
        for _ in range(resamples):
            sample = [v for _ in ids for v in clusters[rng.choice(ids)]]
            boots.append(sum(sample) / len(sample))
        boots.sort()
        summaries[key] = {"planned": len(rows), "successes": sum(v for _, v in rows),
                          "itt_success": sum(v for _, v in rows) / len(rows),
                          "ci95": [boots[int(.025 * resamples)], boots[int(.975 * resamples) - 1]],
                          "required_tool_clusters": len(ids)}
    return {"schema_version": 2, "implementation_status": "evaluation_protocol_interface",
            "evidence_kind": "official_single_configuration_discovery_recomputation",
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "new_agent_evaluated": False, "upstream_revision": UPSTREAM_REVISION,
            "regrading_scope": "availability/selection/recorded terminal status; original full execution traces not imported",
            "planned": len(conditions), "observed": len(recorded),
            "successes": sum(recorded.values()), "itt_success": sum(recorded.values()) / len(conditions),
            "terminal_status_counts": dict(terminal), "cells": summaries,
            "bootstrap": {"unit": "required_tool_within_cell", "resamples": resamples, "seed": seed},
            "plan_hash": plan["plan_hash"],
            "inputs": [{"file": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in (plan_path, rows_path)]}
