from types import SimpleNamespace

import numpy as np
import pytest
import torch

from auto_research.agent_research.methods import build_agent
from auto_research.agent_research.sep7_mechanisms import (
    AtomicMemory, HierarchicalSkills, ShadowGate, relative_credit,
    policy_objective, joint_skill_objective, gigpo_credit,
)
from auto_research.reproductions.sep7_models import CategoryTwoTower, EvidenceController


class PoisonedTask:
    task_id, intent = "public", "travel task"
    context = ("travel case 123 resolves to grounded", "workflow search -> verify")

    @property
    def answer(self):
        raise AssertionError("gold answer accessed")

    @property
    def plan(self):
        raise AssertionError("gold plan accessed")

    @property
    def required_tools(self):
        raise AssertionError("oracle required tools accessed")


@pytest.mark.parametrize("method", ["atomrec", "coskill", "silr", "multi-harness-rl"])
def test_agent_never_reads_gold_fields(method):
    agent = build_agent(method, 12, np.random.default_rng(42))
    answer, plan, _ = agent.solve(PoisonedTask(), 0)
    assert answer == "grounded" and plan == ("search", "verify")
    assert agent.policy_updates == 0
    # Same public input, changed gold fields: predictions remain identical.
    task = SimpleNamespace(task_id="public", intent="travel task", context=PoisonedTask.context,
                           answer="wrong", plan=("wrong",))
    other = build_agent(method, 12, np.random.default_rng(42))
    assert other.solve(task, 0)[:2] == (answer, plan)


def test_atomic_graph_has_real_paths_and_eviction():
    memory = AtomicMemory(3)
    for i, content in enumerate(("camera lens", "lens tripod", "tripod travel")):
        memory.write(str(i), content, i)
    _, paths = memory.retrieve("camera", top_k=1, hops=2)
    assert ("0", "1", "2") in paths
    memory.write("0", "camera portrait", 4)
    assert memory.notes["0"].revisions == [(0, "camera lens")]
    memory.write("3", "portrait", 5)
    assert len(memory.notes) == 3
    assert all(note.links <= memory.notes.keys() for note in memory.notes.values())


def test_skills_verify_private_edits_before_promotion():
    skills = HierarchicalSkills()
    skills.stage("task", ["bad"])
    assert not skills.bundles
    assert not skills.verify("task", lambda bundle: float(bundle == ["good"]), baseline=0)
    skills.stage("task", ["good"])
    assert skills.verify("task", lambda bundle: float(bundle == ["good"]), baseline=0)
    assert skills.bundles == {"task": ["good"]}


class Simulator:
    def __init__(self):
        self.state = np.array([2., 0.])

    def apply(self, action):
        self.state = np.array(action, dtype=float)


def test_silr_rejects_scalar_trap_without_mutating_live_state():
    gate = ShadowGate(Simulator(), lambda sim: sim.state)
    assert gate.propose([.9, .9]) == ("FAIL", -1)
    np.testing.assert_equal(gate.simulator.state, [2, 0])
    assert gate.propose([1, 0])[0] == "SAFE_PROGRESS"
    assert gate.propose([0, 0])[0] == "PASS"


def test_harness_grouping_changes_credit_and_updates_parameters():
    rewards = [0, 0, 1, 1]
    within = relative_credit(rewards, ["t"]*4, ["a", "a", "b", "b"])
    cross = relative_credit(rewards, ["t"]*4, ["a", "a", "b", "b"], "cross")
    np.testing.assert_equal(within, 0)
    np.testing.assert_allclose(cross, [-1, -1, 1, 1])
    logits = torch.nn.Parameter(torch.zeros(4))
    before = logits.detach().clone()
    optimizer = torch.optim.SGD([logits], lr=.1)
    policy_objective(logits, before, cross).backward()
    optimizer.step()
    assert not torch.equal(logits, before)
    assert logits[2] > logits[0]


def test_shared_policy_receives_both_role_gradients():
    shared = torch.nn.Linear(2, 2, bias=False)
    logits = shared(torch.eye(2))
    logs = logits.log_softmax(-1)
    loss = joint_skill_objective(logs[0], logs[1], logs[0].detach(), logs[1].detach(),
                                [1, -1], [-1, 1])
    loss.backward()
    assert torch.count_nonzero(shared.weight.grad) == 4


def test_gigpo_separates_state_groups_and_skill_edits():
    credit = gigpo_credit([0, 1, 0, 1], [1, 1, 0, 1], ["t"]*4,
                          ["s1", "s1", "s2", "s2"])
    np.testing.assert_allclose(credit, [-1, 1, -2, 2], atol=1e-6)
    skills = HierarchicalSkills()
    skills.bundles = {"a": ["search"], "b": ["unrelated"]}
    skills.edit("a", "update", 0, "verify")
    assert skills.bundles["a"] == ["search"]
    assert skills.verify("a", lambda bundle: float(bundle == ["verify"]), baseline=0)
    assert skills.lineage["a"] == [["search"]]
    assert skills.retrieve_step("a", "unrelated") == "verify"


def test_category_adapter_reconstruction_and_shared_encoder_train():
    torch.manual_seed(42)
    model = CategoryTwoTower(4, 3, dim=8)
    features, categories = torch.randn(6, 4), torch.tensor([0, 1, 2, 0, 1, 2])
    source, target = torch.tensor([0, 1, 2]), torch.tensor([3, 4, 5])
    loss = model.objective(features, categories, source, target, torch.arange(6))
    loss.backward()
    for module in (model.encoder, model.adapter, model.category, model.reconstruction):
        assert any(p.grad is not None and p.grad.abs().sum() > 0 for p in module.parameters())
    q1 = model.query(features[:1], categories[:1], torch.tensor([1]))
    q2 = model.query(features[:1], categories[:1], torch.tensor([2]))
    assert not torch.allclose(q1, q2)


def test_controller_guardrails_resume_and_human_authority(tmp_path):
    reference = {"ndcg_at_10": .2, "hit_at_10": .3}
    path = tmp_path / "ledger.json"
    controller = EvidenceController(reference, path)
    candidate = {"key": "a", "evidence": "paper", "reviews": [
        {"score": 1, "feasible": True}, {"score": 0, "feasible": True}]}
    assert controller.select([candidate]) == candidate
    row = controller.evaluate(candidate, lambda _: {"ndcg_at_10": .4, "hit_at_10": .1},
                              {"hit_at_10": .3})
    assert row["verdict"] == "rejected"
    restored = EvidenceController(reference, path)
    assert restored.incumbent == "baseline" and restored.select([candidate]) is None
    candidate = {**candidate, "key": "b"}
    row = restored.evaluate(candidate, lambda _: {"ndcg_at_10": .4, "hit_at_10": .4},
                            {"hit_at_10": .3})
    assert row["verdict"] == "packaged-for-human-review" and not row["online_authorized"]
    assert restored.reference == reference
