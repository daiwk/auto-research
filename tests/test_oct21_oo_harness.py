from dataclasses import FrozenInstanceError, asdict
import hashlib
import json
import runpy
from pathlib import Path
import struct

import pytest

from auto_research.agent_research.oo_harness import (
    Action, Harness, HarnessDiscovery, PublicTask, ToolObservation,
)


class WriteGuard(Harness):
    def verify_before_finish(self, task, observations):
        parent = super().verify_before_finish(task, observations)
        return parent or (None if any(item.mutated for item in observations) else "Write first.")


class Child(WriteGuard):
    def system_prompt(self, task):
        return super().system_prompt(task) + " Child prompt."


def discovery():
    value = HarnessDiscovery(Harness, discovery_task_ids=("train",), heldout_task_ids=("test",))
    value.add_cluster("writes", 0.2, task_ids=("train",))
    value.consider("guard", WriteGuard, parent_key="base", cluster="writes", score=0.5,
        checks_passed=True, mechanism="write guard")
    return value


def test_executable_inheritance_changes_actual_tool_execution_and_ablation_does_not():
    task = PublicTask("test", "Write the publicly observed value.")
    def actor(context):
        if not context.observations:
            return Action("finish", "premature")
        if not any(item.mutated for item in context.observations):
            return Action("tool", "public-value", "write")
        return Action("finish", "finished")
    calls = []
    result = Child().run(task, actor=actor,
        tools=lambda tool, value: calls.append((tool, value)) or ToolObservation(tool, "written", True))
    negative = Harness().run(task, actor=actor, tools=lambda *_: pytest.fail("not called"))
    assert calls == [("write", "public-value")] and result.finish_rejections == 1
    assert result.actor_calls == 3 and negative.actor_calls == 1 and negative.observations == ()


def test_cluster_acceptance_requires_strict_gain_and_checks_and_preserves_rejections():
    value = discovery()
    equal = value.consider("equal", Child, parent_key="guard", cluster="writes", score=0.5,
        checks_passed=True, mechanism="equal score")
    failed = value.consider("failed", Child, parent_key="guard", cluster="writes", score=0.9,
        checks_passed=False, mechanism="failed checks")
    accepted = value.consider("child", Child, parent_key="guard", cluster="writes", score=0.8,
        checks_passed=True, mechanism="child prompt")
    assert not equal.accepted and not failed.accepted and accepted.accepted
    assert len(value.outcomes) == 4
    # Inactive guard remains an ancestor but is not a deployment candidate.
    assert [item.key for item in value.freeze().catalogue] == ["base", "child"]


@pytest.mark.parametrize("score", [True, float("nan"), float("inf"), -0.1, 1.1])
def test_invalid_scores_are_not_accepted(score):
    value = discovery()
    with pytest.raises(ValueError):
        value.consider("child", Child, parent_key="guard", cluster="writes", score=score,
            checks_passed=True, mechanism="candidate")


def test_disjoint_split_and_cluster_boundary_and_unknown_router_selection():
    with pytest.raises(ValueError, match="disjoint"):
        HarnessDiscovery(Harness, discovery_task_ids=("same",), heldout_task_ids=("same",))
    value = discovery()
    with pytest.raises(ValueError, match="discovery"):
        value.add_cluster("leak", 0., task_ids=("test",))
    frozen = value.freeze()
    with pytest.raises(ValueError, match="held-out"):
        frozen.deploy(PublicTask("train", "public"), actor=lambda _: Action("finish", "a"),
            tool_factory=lambda: lambda *_: None, router=lambda _: "base")
    with pytest.raises(ValueError, match="active"):
        frozen.deploy(PublicTask("test", "public"), actor=lambda _: Action("finish", "a"),
            tool_factory=lambda: lambda *_: None, router=lambda _: "hidden-discovery-score")


def test_frozen_router_view_excludes_grades_and_base_result_is_reused_once():
    value = discovery()
    frozen = value.freeze(routing_lessons=("public routing lesson",))
    # A later discovery update cannot enter the frozen catalogue or lessons.
    value.consider("later", Child, parent_key="guard", cluster="writes", score=0.9,
        checks_passed=True, mechanism="later candidate")
    states, views, actor_views = [], [], []
    def factory():
        states.append({})
        return lambda tool, payload: ToolObservation(tool, payload)
    def actor(view):
        actor_views.append(view)
        return Action("finish", "public final")
    def router(view):
        views.append(view)
        return "base"
    result = frozen.deploy(PublicTask("test", "public instruction"), actor=actor,
        tool_factory=factory, router=router)
    assert result.base_reused and result.total_actor_calls == len(actor_views) == len(states) == 1
    assert set(asdict(views[0])) == {"task", "base_run", "catalogue", "lessons"}
    assert "later" not in {item.key for item in views[0].catalogue}
    assert not hasattr(views[0], "score") and not hasattr(views[0], "outcomes")
    with pytest.raises(FrozenInstanceError):
        views[0].lessons = ()


def test_specialist_gets_a_fresh_initial_environment_and_method_edits_fail_closed():
    frozen = discovery().freeze()
    states = []
    def factory():
        state = []
        states.append(state)
        return lambda tool, payload: state.append(payload) or ToolObservation(tool, "written", True)
    def actor(view):
        return Action("tool", "value", "write") if not view.observations else Action("finish", "done")
    result = frozen.deploy(PublicTask("test", "write"), actor=actor, tool_factory=factory,
        router=lambda _: "guard")
    assert not result.base_reused and states == [["value"], ["value"]] and states[0] is not states[1]
    old = WriteGuard.verify_before_finish
    try:
        WriteGuard.verify_before_finish = lambda *_: None
        with pytest.raises(ValueError, match="changed"):
            frozen.deploy(PublicTask("test", "write"), actor=actor, tool_factory=factory, router=lambda _: "guard")
    finally:
        WriteGuard.verify_before_finish = old


def test_turn_limit_and_unavailable_tools_do_not_silently_succeed():
    task = PublicTask("test", "public")
    result = WriteGuard().run(task, actor=lambda _: Action("finish", "premature"),
        tools=lambda *_: pytest.fail("not called"), max_turns=3)
    assert result.final_answer is None and result.actor_calls == result.finish_rejections == 3
    with pytest.raises(ValueError, match="unavailable"):
        Harness().run(task, actor=lambda _: Action("tool", "payload", "shell"), tools=lambda *_: None)


def test_runner_diagnostic_uses_actual_component_and_records_negative_control():
    runner = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_oct21_oo_harness.py"))
    row = runner["diagnostic"](42)
    assert row["metrics"]["observed_guarded_writes"] == 8
    assert row["metrics"]["removed_guard_control_writes"] == 0
    assert row["metrics"]["equal_score_candidates_rejected"] == 1
    assert row["metrics"]["actual_llm_calls"] == 0


def test_paper_metadata_first_author_and_real_figure_have_honest_cost_boundary():
    root = Path(__file__).resolve().parents[1]
    row = json.loads((root / "src/auto_research/paper_specs/catalog/agent-research/oo-harness.json").read_text())
    assert row["first_author_affiliation"] == "University of Illinois Urbana-Champaign"
    assert "Google" in row["authorship_note"] and row["published_at"] == "2026-10-20T15:32:52Z"
    assert row["implementation_status"] == "component_only" and row["requires_gpu_validation"] is False
    assert row["review_done"] and row["full_experiment_status"] == "not_reproduced_high_cost"
    assert row["diagnostic_only"] and not row["promotion_eligible"] and not row["evolve_integrated"]
    detail = root / "docs" / row["detail_path"]
    text = detail.read_text()
    for label in ("论文链接", "公司/机构", "首次公开日期", "原文开源代码", "本地 Adapter", "本地复现代码",
                  "成本过高，不复现（审查 DONE）", "不是完整论文复现"):
        assert label in text
    provenance = json.loads((detail.parent / "assets/provenance.json").read_text())
    image = (detail.parent / "assets" / provenance["asset"]).read_bytes()
    assert hashlib.sha256(image).hexdigest() == provenance["asset_sha256"]
    width, height = struct.unpack(">II", image[16:24])
    assert len(image) > 5000 and width >= 400 and height >= 140
