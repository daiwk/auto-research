import math

import pytest
import torch

from auto_research.reproductions.state_opd.algorithm import (
    InteractionState, Sample, collect_response_pool, full_vocabulary_entropy,
    pooled_loss, response_allocation, sampled_k1_dual_clip,
)
from auto_research.reproductions.state_opd.environment import ArithmeticEnvironment, calculate


def test_teacher_state_omits_only_prior_reasoning_not_executed_evidence():
    state = InteractionState("public goal", "first obs").append(
        {"tool": "calculator", "arguments": {"expression": "2+3"}}, "5")
    messages = state.teacher_messages("system")
    assert "2+3" in messages[1]["content"] and '"5"' in messages[1]["content"]
    assert "reasoning" not in messages[1]["content"]
    assert "answer" not in messages[1]["content"]


def test_calculator_executes_real_arithmetic_but_no_generated_code():
    assert calculate("(8+2)*3/2") == 15
    with pytest.raises(ValueError):
        calculate("__import__('os').system('anything')")
    environment = ArithmeticEnvironment("What is 8+2?")
    assert "reference" in environment.reset()
    observation, done = environment.step({"tool": "calculator", "arguments": {"expression": "8+2"}})
    assert observation == "Calculator result: 10" and not done
    observation, done = environment.step({"tool": "finish", "arguments": {"answer": "incorrect answer"}})
    assert done and "correctness feedback" in observation
    assert environment.finished_answer == "incorrect answer"


def test_entropy_is_full_vocabulary_not_selected_token_surprisal():
    entropy = full_vocabulary_entropy(torch.zeros(2, 10))
    assert torch.allclose(entropy, torch.full((2,), math.log(10)))


def test_response_budget_uses_ceiling_and_actual_entropy_ranking():
    selected, additional = response_allocation([.1, .5, .3], multiplicity=4, concentration=2)
    assert selected == [1, 2]
    assert additional == 6
    with pytest.raises(ValueError, match="finite"):
        response_allocation([float("nan")])


def test_additional_actions_do_not_execute_and_regenerate_full_responses():
    class Environment:
        goal = "public goal"
        executed = 0
        def reset(self):
            return "initial"
        def step(self, action):
            self.executed += 1
            return "5", False
    class Policy:
        calls = []
        def sample(self, history):
            self.calls.append(history)
            return Sample((1, 2), 'Private reasoning\n{"tool":"calculator","arguments":{"expression":"2+3"}}',
                          torch.tensor([-1., -2.]), float(len(self.calls)))
    env, policy = Environment(), Policy()
    pool, audit = collect_response_pool(policy, env, system_prompt="system", max_turns=3,
                                       multiplicity=4, concentration=2)
    assert env.executed == 3
    assert len(pool) == 15
    assert sum(record.executed for record in pool) == 3
    assert audit["additional_actions_executed"] == 0
    assert audit["selected_turns"] == [2, 1]
    assert pool[3].history == pool[2].history
    assert "Private reasoning" in str(pool[2].history)
    assert "Private reasoning" not in str(pool[2].state.teacher_messages("system"))


def test_loss_is_global_token_mean_and_scores_are_fixed():
    current = torch.tensor([.01, -.3], requires_grad=True)
    teacher = torch.tensor([-.2, -.4], requires_grad=True)
    old = torch.tensor([0., -.2], requires_grad=True)
    first = sampled_k1_dual_clip(current, teacher, old)
    second = sampled_k1_dual_clip(current[:1], teacher[:1], old[:1])
    actual = pooled_loss([(current, teacher, old), (current[:1], teacher[:1], old[:1])])
    assert torch.allclose(actual, (first.sum() + second.sum()) / 3)
    actual.backward()
    assert current.grad.abs().sum() > 0
    assert teacher.grad is None and old.grad is None


@pytest.mark.parametrize("variant", ["state", "state-no-expansion", "full-history-opd"])
def test_checkpoint_controls_execute_independent_roots_and_keep_teacher_role_boundary(monkeypatch,variant):
    from auto_research.reproductions.state_opd import checkpoint
    from auto_research.post_training.response_policy import GeneratedResponse
    class Policy:
        vocabulary_sha256="same-vocabulary"
        provenance={"public_id":"diagnostic-fixture"}
        def __init__(self,*,public_id,**kwargs):
            self.model=torch.nn.Linear(1,1,bias=False)
            self.model.weight.data.fill_(.1 if public_id=="student" else .2)
            self.model.requires_grad_(public_id=="student")
            self.public_id=public_id
            self.contexts=[]
            instances.append(self)
        def generate(self,messages,**kwargs):
            return [GeneratedResponse((1,2),'Private student reasoning {"tool":"calculator","arguments":{"expression":"2+3"}}',False)]
        def token_statistics(self,messages,tokens,*,entropy=False):
            self.contexts.append(messages)
            return -1+self.model.weight.reshape(())*torch.tensor(tokens,dtype=torch.float32),torch.ones(len(tokens)) if entropy else None
        def prepare_lora(self,**kwargs):
            self.optimizer=torch.optim.AdamW(self.model.parameters(),lr=.01)
        def trainable_digest(self):
            return str(float(self.model.weight.detach()))
    instances=[]
    monkeypatch.setattr(checkpoint,"ResponsePolicy",Policy)
    monkeypatch.setattr(checkpoint,"validate_holdout",lambda *args,**kwargs:{"verified":True})
    monkeypatch.setattr(checkpoint,"load_public_rows",lambda _: [{"question":"public arithmetic","answer":"777"}])
    result=checkpoint.run_state_opd(student_path="fixture",teacher_path="fixture",student_id="student",teacher_id="teacher",
        student_revision="fixture",teacher_revision="fixture",train_path="fixture",validation_path="fixture",
        split_manifest="fixture",dataset_revision="fixture",device="cpu",steps=1,max_turns=2,multiplicity=2,
        concentration=2,validation_examples=1,variant=variant)
    assert result["parameters_changed"] and result["execution_status"]=="passed"
    audit=result["trajectory_audits"][0]
    assert audit["additional_actions_executed"]==0
    assert audit["root_actions_executed"]==(4 if variant=="full-history-opd" else 2)
    teacher=instances[1]
    assert "777" not in str(teacher.contexts)
    inherited="Private student reasoning" in str(teacher.contexts)
    assert inherited==(variant=="full-history-opd")
    assert result["protocol"]["reference_independent_root_trajectories"]==(2 if variant=="full-history-opd" else 1)
