import json
import math
import hashlib
from pathlib import Path

import pytest

from auto_research.agent_research.memcon import (
    ACTIONS, MemoryEntry, MemoryState, MemCon, PolicyConfig, TabularPolicy,
    InMemoryBackend, episode_reward, run_diagnostic,
)


def test_state_bins_use_observation_not_answers():
    state = MemoryState("retrieve", step=18, physical_actions=("look", "look"),
                        objects_held=4, locations_visited=20, memory_size=60,
                        plan_available=True, task_index=16)
    assert state.key() == ("retrieve", "late", True, 2, 4, 5, True, "warm")
    assert MemoryState("q", step=7).key()[1] == "early"
    assert MemoryState("q", step=8, task_index=15).key()[1:] == (
        "mid", False, 0, 0, 0, False, "cold")
    assert {"answer", "plan", "gold"}.isdisjoint(MemoryState.__dataclass_fields__)


def test_ucb_explores_every_action_then_uses_state_local_count():
    policy = TabularPolicy()
    state = MemoryState("lookup")
    chosen = [policy.select(state)[0] for _ in ACTIONS]
    assert chosen == [0, 1, 2, 7, 3, 4, 5, 6, 8]
    key = state.key()
    before = policy.scores(key)
    for _ in range(25):
        policy.select(MemoryState("unrelated"))
    assert policy.scores(key) == before
    assert before[0] == pytest.approx(.5 + 1.4 * math.sqrt(math.log(9)))


def test_reverse_credit_is_constant_alpha_and_failure_stays_negative():
    policy = TabularPolicy(PolicyConfig(alpha=.5, gamma=.8))
    key = MemoryState("q").key()
    policy.update([(key, 0), (key, 8)], 1.)
    assert policy.q[key][0] == pytest.approx(.65)
    assert policy.q[key][8] == pytest.approx(.4)
    policy.update([(key, 0)], -1.)
    assert policy.q[key][0] == pytest.approx(-.175)
    assert episode_reward(False, steps=30) == -.5
    assert episode_reward(True, steps=0) == 1.3
    assert episode_reward(False, steps=0) == pytest.approx(-.2)


def test_backend_executes_all_operations_and_reports_effects():
    backend = InMemoryBackend()
    backend.store(MemoryEntry("1", "alpha", "alpha fact", True,
                              ("inspect shelf 3", "open box 2"), ("shared insight",)))
    backend.store(MemoryEntry("2", "alpha", "other fact", False,
                              (), ("shared insight",)))
    controller = MemCon(backend)
    controller.plans["alpha"] = ("inspect shelf [id]", "open box [id]")
    controller.begin("alpha")
    outputs = [controller.execute("alpha", step=0, action_index=i) for i in range(9)]
    assert len(outputs[0].entries) == 1
    assert len(outputs[1].entries) == 2
    assert outputs[3].plan == controller.plans["alpha"]
    assert outputs[4].query == "alpha alternative approach"
    assert outputs[5].effect == {"removed_insights": 1}
    assert outputs[6].effect == {"removed_entries": 1}
    assert outputs[8].entries == ()
    assert outputs[8].effect == {}
    assert backend.calls[2][1]["hop"] == 2
    assert backend.calls[7][1]["hop"] == 0
    reward = controller.finish(success=False, steps=30, observed_actions=("look",))
    assert reward == -.5
    assert controller.policy.updates == 1


def test_plan_is_only_stored_after_real_successful_trajectory():
    controller = MemCon(InMemoryBackend())
    controller.begin("fetch")
    controller.execute("fetch", step=0)
    controller.finish(success=False, steps=30, observed_actions=("wrong action",))
    assert "fetch" not in controller.plans
    controller.begin("fetch")
    controller.execute("fetch", step=1)
    controller.finish(success=True, steps=2, observed_actions=("inspect shelf 21", "open box 7"))
    assert controller.plans["fetch"] == ("inspect shelf [id]", "open box [id]")
    assert len(controller.backend.entries) == 2


def test_snapshot_round_trip_resumes_active_episode(tmp_path):
    controller = MemCon(InMemoryBackend())
    controller.begin("fetch")
    controller.execute("fetch", step=0)
    path = tmp_path / "state.json"
    controller.save(path)
    resumed = MemCon.load(path)
    assert resumed.policy.counts == controller.policy.counts
    assert resumed.episode == controller.episode
    assert resumed.goal_type == "fetch"
    for method in (resumed, controller):
        method.execute("fetch", step=8)
        method.finish(success=True, steps=10, observed_actions=("look", "open box 7"))
    assert resumed.snapshot() == controller.snapshot()
    corrupt = json.loads(path.read_text())
    corrupt["policy"]["counts"][0]["values"][0] = -1
    path.write_text(json.dumps(corrupt))
    with pytest.raises(ValueError):
        MemCon.load(path)


def test_optional_backend_maintenance_is_explicit_noop():
    class BareBackend:
        size = 0
        def retrieve(self, query, top_k):
            return (), ()
        def store(self, entry):
            pass
    controller = MemCon(BareBackend())
    controller.begin("q")
    assert controller.execute("q", step=0, action_index=0).entries == ()
    assert controller.execute("q", step=0, action_index=5).effect == {"unsupported": "consolidate"}


def test_link_depth_changes_actual_retrieval_and_consolidation_deduplicates():
    backend = InMemoryBackend([
        MemoryEntry("a", "fetch", "needle", True, (), ("rule", "rule"), ("b",)),
        MemoryEntry("b", "fetch", "linked observation", True),
    ])
    direct, _ = backend.retrieve("needle", top_k=2, insight_k=0, hop=1)
    deep, _ = backend.retrieve("needle", top_k=2, insight_k=0, hop=2)
    assert [e.identity for e in direct] == ["a"]
    assert [e.identity for e in deep] == ["a", "b"]
    assert backend.maintain("consolidate") == {"removed_insights": 1}


def test_binary_feedback_changes_policy_values_and_later_choices():
    policy = TabularPolicy()
    state = MemoryState("stable-context")
    choices = []
    for _ in range(200):
        index, action = policy.select(state)
        policy.update([(state.key(), index)], 1. if action.operation == "retrieve" else -.5)
        choices.append(action.operation)
    assert choices[-100:].count("retrieve") > choices[:100].count("retrieve")
    assert policy.q[state.key()][0] > policy.q[state.key()][8]


@pytest.mark.parametrize("kwargs", [
    {"alpha": 0}, {"gamma": 1.1}, {"ucb_c": -1}, {"alpha": float("nan")},
])
def test_invalid_policy_parameters_rejected(kwargs):
    with pytest.raises(ValueError):
        PolicyConfig(**kwargs)


def test_lifecycle_and_nonfinite_feedback_rejected():
    controller = MemCon(InMemoryBackend())
    with pytest.raises(RuntimeError):
        controller.execute("q", step=0)
    controller.begin("q")
    with pytest.raises(RuntimeError):
        controller.begin("q")
    with pytest.raises(ValueError):
        episode_reward(True, steps=-1)
    with pytest.raises(ValueError):
        controller.policy.update([], float("nan"))


def test_store_failure_does_not_apply_terminal_credit():
    class UnavailableBackend(InMemoryBackend):
        def store(self, entry):
            raise OSError("storage unavailable")
    controller = MemCon(UnavailableBackend())
    controller.begin("q")
    controller.execute("q", step=0)
    original = controller.policy.snapshot()
    with pytest.raises(OSError):
        controller.finish(success=True, steps=2, observed_actions=("actual attempt",))
    assert controller.policy.snapshot() == original
    assert not controller.plans and controller.goal_type == "q"


def test_cpu_diagnostic_is_reproducible_and_not_capability_result():
    result = run_diagnostic(seed=42, episodes=30)
    assert result == run_diagnostic(seed=42, episodes=30)
    assert result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "L1"
    assert result["metrics"]["policy_updates"] == 30
    assert len(result["metrics"]["action_counts"]) == 9
    assert sum(result["metrics"]["action_counts"]) == 60
    assert result["protocol"]["gold_access"] is False
    assert "answer_accuracy" not in result["metrics"]


def test_terminal_reward_mean_uses_stable_summation(monkeypatch):
    rewards = []
    original = MemCon.finish
    def finish(controller, **kwargs):
        reward = original(controller, **kwargs)
        rewards.append(reward)
        return reward
    monkeypatch.setattr(MemCon, "finish", finish)
    result = run_diagnostic(seed=42, episodes=60)
    assert len(rewards) == 60
    expected = math.fsum(rewards) / 60
    assert expected == math.fsum(reversed(rewards)) / 60
    assert result["metrics"]["mean_terminal_reward"] == expected


def test_documented_artifact_replays_and_binding_does_not_enable_gold_fixture():
    root = Path(__file__).resolve().parents[2]
    spec = json.loads((root / "src/auto_research/paper_specs/catalog/agent-research/memcon.json").read_text())
    assert spec["adapter"] is None
    assert spec["promotion_eligible"] is False
    page = (root / "docs" / spec["detail_path"]).read_text()
    for item in ("## 论文信息", "| 论文链接 |", "| 公司 / 机构 |", "| 首次公开日期 |",
                 "| 原作者代码 |", "| 本地 adapter /", "| 本地复现代码 |", "### 核心公式",
                 "### 论文离线与线上效果", "## 复现边界"):
        assert item in page
    artifact = json.loads((root / "docs" / spec["detail_path"]).parent.joinpath(
        "metrics/cpu-mechanism-seeds42-44.json").read_text())
    assert artifact["evaluation_protocol"]["formal_comparison"] is False
    source = root / "src/auto_research/agent_research/memcon.py"
    assert artifact["provenance"]["source_file_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    for row in artifact["runs"]:
        assert {"seed": row["seed"], **run_diagnostic(seed=row["seed"], episodes=60)["metrics"]} == row
