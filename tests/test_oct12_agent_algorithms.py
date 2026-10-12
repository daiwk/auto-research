"""L0 contracts only: fixtures below are never agent capability evidence."""
import copy
import json
from types import SimpleNamespace
import numpy as np
import pytest
import torch
from torch import nn

from auto_research.agent_research.oct12_evolution import (
    Edit, Evaluation, Evo2, HarnessNode, Janus, Trajectory, apply_edits,
    bradley_terry, parent_distribution, recover_prefix, retained_pool, RSIAnything,
)
from auto_research.agent_research.oct12_checkpoint import Evo2Policy, make_factorized_predictor
from auto_research.agent_research.oct12_memory_tools import (
    DiscountedLinUCB, T2Mem, WorkflowOutcome, audit_workflows,
)


def test_edit_authority_and_recovery_keep_only_valid_prefix():
    files = {"agent.py": "x = 1\ny = 2\n"}
    with pytest.raises(ValueError, match="authorized"):
        apply_edits(files, [Edit("../../secret", "x = 1", "x = 3")])
    calls = []
    def resume(current, prefix):
        calls.append((current, prefix))
        return [Edit("agent.py", "y = 2", "y = 4")]
    result, edits, recovered = recover_prefix(files,
        [Edit("agent.py", "x = 1", "x = 3"), Edit("agent.py", "y = 2", "y = (")], resume)
    assert recovered and result["agent.py"] == "x = 3\ny = 4\n"
    assert len(edits) == 2 and len(calls[0][1]) == 1
    assert files["agent.py"] == "x = 1\ny = 2\n"


def test_tree_distribution_retains_root_elites_and_repairs():
    nodes = [HarnessNode("root", {}, Evaluation(.5, ()))]+[
        HarnessNode(str(i), {}, Evaluation(score, ()), "root", 1)
        for i, score in enumerate((0., .1, .4, .6, .9, 1.))]
    pool = retained_pool(nodes, per_depth=4)
    assert len(pool) == 5
    assert {"4", "5"} <= {node.identifier for node in pool}
    assert any(node.evaluation.score < .9 for node in pool if node.parent)
    probability = parent_distribution(nodes)
    assert probability["root"] == .2
    assert sum(probability.values()) == pytest.approx(1.)
    assert probability["0"] > probability["2"]


class EvoFixture:
    def __init__(self):
        self.snapshots = 0
        self.training = []
    def propose(self, parent, directive, donor):
        old = parent.files["agent.py"].strip()
        return "fixture edit", [Edit("agent.py", old, old + "\n# edit")], [{"role":"user","content":"source"}], False
    def continue_edits(self, *args):
        raise AssertionError("unused")
    def reflect(self, candidate, strategies):
        return {"action":"keep"}, "keep", [{"role":"user","content":"observed feedback"}], False
    def extract_strategy(self, parent, child):
        return "L0 fixture strategy"
    def snapshot(self):
        self.snapshots += 1
        return copy.copy(self)
    def revision_directive(self, candidate): return "L0 fixture directive"
    def sft(self, rows, steps):
        assert {row.role for row in rows} == {"proposer", "reflector"}
        return {"fixture_only":True}
    def interleaved_grpo(self, proposer, reflector, round_id):
        assert len(proposer) == len(reflector) == 2
        self.training.append(round_id)
        return {"fixture_only":True}


def test_evo2_refreshes_frozen_counterpart_once_per_round_and_never_reads_test():
    policy = EvoFixture()
    controller = Evo2(policy, lambda files: Evaluation(.5, ({"executed":True},)),
                      {"agent.py":"x = 1\n"})
    controller.train(warmup_iterations=1, rounds=2, steps=2)
    assert policy.snapshots == 2 and policy.training == [0,0,1,1]
    with pytest.raises(ValueError, match="validation"):
        Evo2(policy, lambda _:None, {}, split="test")


def test_bradley_terry_soft_preferences_not_realized_scores():
    values = bradley_terry(3, [(0,1,.9),(1,2,.8),(0,2,.95)])
    assert values[0] > values[1] > values[2]
    assert bradley_terry(2, [(0,1,.5)]) == [.5,.5]


class JanusFixture:
    def proposals(self, graph, skills, remaining, count):
        return [{"proposal":str(i),"parents":["root"]} for i in range(count)]
    def preference(self, a, b, criterion, graph, skills, remaining):
        assert all("evidence" not in node for node in graph if node["status"] != "executed")
        return .75
    def exploration_weights(self, *args): return 1.,2.
    def debate(self, proposal, *args): return proposal
    def evolve_skills(self, skills, graph, strategy):
        assert any(node.get("evidence",{}).get("score") == 99 for node in graph)
        return {key:"observed experiment" for key in skills}


def test_janus_stores_forecasts_before_real_execution_and_updates_all_skill_sets():
    def execute(proposal, graph, skills):
        selected = next(node for node in graph if node["status"] == "open")
        assert "predictions" in selected and "evidence" not in selected
        return {"score":99}
    result = Janus(JanusFixture(), execute, initial_evidence={"score":0}).run(budget=1,candidates=3)
    assert sum(node["status"] == "pruned" for node in result["graph"]) == 2
    assert set(result["skills"]) == {"intra","cross","prediction","exploration","coordination"}


def test_factorized_predictor_has_nonconstant_predictions_and_latent_gradients():
    model = make_factorized_predictor(8,"cpu")
    a,b = torch.randn(8),torch.randn(8)
    first,latent,factors = model(a,b)
    second,_,_ = model(b,a)
    assert first != second
    loss = first.square()+latent.square().mean()+factors.square().mean()
    loss.backward()
    assert all(parameter.grad is not None for parameter in model.parameters())
    assert sum(parameter.grad.abs().sum() for parameter in model.parameters()) > 0


class NeuralFixture(nn.Module):
    def __init__(self):
        super().__init__()
        self.attn = nn.Module()
        self.attn.q_proj = nn.Linear(8,128)
        self.attn.v_proj = nn.Linear(8,128)
    def forward(self):
        x = torch.ones(1,8)
        return (self.attn.q_proj(x)+self.attn.v_proj(x)).log_softmax(-1)[0]


def test_evo2_warmup_and_interleaved_role_losses_have_real_gradients():
    policy = Evo2Policy.__new__(Evo2Policy)
    policy.model, policy.device, policy.max_tokens = NeuralFixture(),"cpu",32
    policy.continuation = lambda messages,target: policy.model()[torch.tensor([ord(c)%128 for c in target])]
    prompt = ({"role":"user","content":"L0 fixture, no gold"},)
    rows = [Trajectory("proposer","A",prompt,"a",0.,True),
            Trajectory("reflector","local",prompt,"keep",0.,True)]
    sft = policy.sft(rows,steps=1)
    assert sft["steps"][0]["gradient_norm"] > 0
    groups = [[Trajectory(role,"A",prompt,"a",1.,True),
               Trajectory(role,"A",prompt,"b",0.,True)] for role in ("proposer","reflector")]
    before = [p.detach().clone() for p in policy.model.parameters() if p.requires_grad]
    result = policy.interleaved_grpo(*groups,round_id=0)
    assert result["updated"] and result["gradient_norm"] > 0
    assert [group["advantages"] for group in result["groups"]] == [[.5,-.5],[.5,-.5]]
    after = [p for p in policy.model.parameters() if p.requires_grad]
    assert any(not torch.equal(a,b) for a,b in zip(before,after))
    truncated = [Trajectory("proposer","A",prompt,"a",1.,True,True),
                 Trajectory("proposer","A",prompt,"b",0.,True,True)]
    assert policy.interleaved_grpo(truncated,truncated,round_id=1)["updated"] is False


def test_discounted_bandit_updates_selected_arm_only_and_reacts_to_failure():
    bandit = DiscountedLinUCB({"a":.9,"b":.8},2,weights=(0,1,0))
    context = np.array([1.,0.])
    old_a = bandit.a["b"].copy()
    old_b = bandit.b["b"].copy()
    before = bandit.b["a"][0]/bandit.a["a"][0]
    bandit.update("a",context,0)
    assert bandit.b["a"][0]/bandit.a["a"][0] < before
    np.testing.assert_array_equal(bandit.a["b"],old_a)
    np.testing.assert_array_equal(bandit.b["b"],old_b)


class RetentionFixture:
    def candidates(self,context,workflow,count):
        return ["good","bad"] if workflow == "old" else ["new-good","new-bad"]
    def predict(self,predictor,context,candidate):
        if predictor == "adapted":
            return .9 if candidate in {"good","new-bad"} else .1
        return .2 if candidate.endswith("good") else .1
    def version(self,item): return item
    def revise_workflow(self,workflow,history): return "new"
    def adapt(self,predictor,records,steps):
        assert all(row.split == "train" for row in records)
        return "adapted",{"fixture_only":True}


def test_rsi_component_acceptance_does_not_bypass_pair_compatibility_rollback():
    controller = RSIAnything(RetentionFixture(),lambda context,candidate:
        Evaluation(float(candidate.endswith("good")),({"observation":"actual fixture execution"},)),
        initial_workflow="old",predictor="initial")
    result = controller.run(["training-a","training-b"],["validation-a"],rounds=1)
    audit = result["audit"][0]
    assert audit["policy_component_accepted"] and audit["model_component_accepted"]
    assert audit["pair_accepted"] is False
    assert controller.workflow == "old" and controller.predictor == "initial"
    with pytest.raises(ValueError,match="disjoint"):
        controller.run(["same"],["same"])


def test_rsi_pair_gate_rejects_prediction_regression_even_when_utility_ties():
    class PredictionRegression(RetentionFixture):
        def predict(self,predictor,context,candidate):
            if predictor == "adapted":
                return .9 if candidate == "new-bad" else .1 if candidate.endswith("good") else 0.
            return .2 if candidate.endswith("good") else .1
    controller = RSIAnything(PredictionRegression(),lambda context,candidate:
        Evaluation(0.,({"observation":"L0 fixture"},)),
        initial_workflow="old",predictor="initial",error_threshold=.001)
    audit = controller.run(["training-a","training-b"],["validation"],rounds=1)["audit"][0]
    assert audit["policy_component_accepted"] and audit["model_component_accepted"]
    assert audit["pair_validation_score"] == audit["old_validation_score"] == 0
    assert audit["proposed_pair_prediction_error"] > audit["old_pair_prediction_error"]
    assert audit["pair_accepted"] is False
    assert controller.workflow == "old" and controller.predictor == "initial"


class MemoryFixture:
    def __init__(self): self.actions = iter(("ReadRaw","SearchMeta","Answer"))
    def generate(self,messages,sample=False):
        payload = json.loads(messages[0]["content"])
        assert "answer" not in payload
        if "session" in payload: return payload["session"]
        return "query-conditioned observed memory"
    def embedding(self,text): return torch.tensor([1.,float("second" in text)])
    def sample_choice(self,messages,choices):
        return next(self.actions) if "Answer" in choices else choices[0]


def test_t2mem_sources_seen_only_and_search_does_not_repeat_metadata():
    memory = T2Mem(MemoryFixture(),{"0":"first event","1":"second event","2":"third event"},top_k=1,max_steps=3)
    result = memory.answer("query")
    assert result["trace"][0]["raw_source_id"] in result["trace"][0]["observed_ids"]
    assert len(result["seen_metadata"]) == 2
    assert result["construction_steps"] == 3


def test_jev_audit_includes_failed_attempts_in_delivery_cost():
    rows = [WorkflowOutcome("a",0,"base",True,1,2,2),
            WorkflowOutcome("b",0,"base",True,1,2,2),
            WorkflowOutcome("a",0,"new",True,.1,1,1),
            WorkflowOutcome("b",0,"new",False,.1,10,5,True,True)]
    result = audit_workflows(rows)
    assert result["configurations"]["new"]["cost_per_success"] == 6
    assert result["matched_success_pairs"] == 1
    assert result["configurations"]["new"]["failure_cost_share"] == pytest.approx(5/6)
    with pytest.raises(ValueError,match="unmatched"):
        audit_workflows(rows[:-1])
