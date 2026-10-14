"""CPU-only profile/isolation guards, not evidence of an MBS GPU success."""
import json

import pytest

from auto_research.post_training.oct13_common import CostLedger,ExecutionFailure
from auto_research.post_training.response_policy import GeneratedResponse
from auto_research.reproductions.magicbeanstalk import checkpoint
from auto_research.reproductions.magicbeanstalk.algorithm import MagicBeanStalk,Problem


class Policy:
    def __init__(self,text="\\boxed{7}"):
        self.text=text;self.calls=[]
    def generate(self,messages,**kwargs):
        self.calls.append((messages,kwargs))
        return [GeneratedResponse((1,2),self.text,False)]*kwargs["samples"]


def test_default_teacher_profile_remains_stochastic_and_audits_actual_sample():
    teacher=Policy('{"scaffold_safe":false}')
    backend=checkpoint.CheckpointConstruction(teacher,Policy(),CostLedger())
    assert backend.construction_teacher_sample is True
    assert backend.teacher_json("unchanged instruction",{},operation="scaffold_safe")=={"scaffold_safe":False}
    assert teacher.calls[-1][1]["sample"] is True
    assert backend.response_audits[-1]["sample"] is True


@pytest.mark.parametrize("sample",[True,False])
def test_explicit_profile_only_controls_independent_teacher_and_json_calls(sample):
    teacher,student=Policy(),Policy()
    backend=checkpoint.CheckpointConstruction(teacher,student,CostLedger(),rollouts=4,
        construction_teacher_sample=sample)
    p=Problem("public question","7","PRIVATE_PARENT_GOLD_TRACE")
    assert backend.verify(p) is not None
    teacher.text='{"scaffold_safe":false}'
    assert backend.teacher_json("unchanged teacher task",{"train_gold":"PRIVATE_TRAIN_GOLD"},operation="scaffold_safe")=={"scaffold_safe":False}
    assert [call[1]["sample"] for call in teacher.calls]==[sample,sample]
    assert [r["sample"] for r in backend.response_audits]==[sample,sample]
    assert "PRIVATE_PARENT_GOLD_TRACE" not in str(teacher.calls[0][0])
    assert "PRIVATE_TRAIN_GOLD" in str(teacher.calls[1][0])
    teacher.text="\\boxed{7}"
    backend.student_rates(p,worked_examples=())
    backend.target_outcomes(p)
    for messages,kwargs in teacher.calls[2:]+student.calls:
        assert kwargs["sample"] is True and kwargs["samples"]==4
        assert "json_schema" not in kwargs and "PRIVATE_PARENT_GOLD_TRACE" not in str(messages)
        assert "PRIVATE_TRAIN_GOLD" not in str(messages)
    assert all(r["sample"] is True for r in backend.response_audits[2:])


@pytest.mark.parametrize("value",["false",0,1,None,[],{}])
def test_constructor_requires_a_real_boolean(value):
    with pytest.raises(ValueError,match="explicit boolean"):
        checkpoint.CheckpointConstruction(None,None,CostLedger(),construction_teacher_sample=value)


@pytest.mark.parametrize("value",["false",0,1,None,[],{}])
def test_run_rejects_bad_teacher_profile_before_data_or_models(monkeypatch,value):
    def forbidden(*_args,**_kwargs):pytest.fail("invalid profile must fail before any data/model loading")
    monkeypatch.setattr(checkpoint,"load_split",forbidden)
    monkeypatch.setattr(checkpoint,"load_policy",forbidden)
    with pytest.raises(ValueError,match="explicit boolean"):
        checkpoint.run({"construction_teacher_sample":value})


@pytest.mark.parametrize("profile",[None,True,False])
def test_run_forwards_default_or_explicit_profile_without_changing_budgets(monkeypatch,profile):
    captured=[]
    class Backend:
        response_audits=[]
        def __init__(self,*args,**kwargs):captured.append(kwargs)
    class Builder:
        audit=[]
        def __init__(self,*args,**kwargs):self.budgets=kwargs
        def construct(self,_problem):return None
    monkeypatch.setattr(checkpoint,"CheckpointConstruction",Backend)
    monkeypatch.setattr(checkpoint,"MagicBeanStalk",Builder)
    monkeypatch.setattr(checkpoint,"load_split",lambda _config:([{"question":"q","answer":"7"}],[],{}))
    monkeypatch.setattr(checkpoint,"load_policy",lambda *_args,**_kwargs:object())
    monkeypatch.setattr(checkpoint,"evaluate",lambda *_args,**_kwargs:{"accuracy":0.})
    config={"max_tokens":1024,"group":4,"teacher_attempts":2,"steps":2,"depth":1,
        "decomposition_retries":2,"synthesis_retries":2}
    if profile is not None:config["construction_teacher_sample"]=profile
    with pytest.raises(ExecutionFailure,match="no actual effectivity"):
        checkpoint.run(config)
    assert captured[0]["construction_teacher_sample"] is (True if profile is None else profile)
    assert (captured[0]["max_tokens"],captured[0]["rollouts"],captured[0]["teacher_attempts"])==(1024,4,2)


def test_greedy_profile_keeps_two_failed_verifier_attempts_and_does_not_accept_wrong_answer():
    teacher=Policy("\\boxed{99}")
    backend=checkpoint.CheckpointConstruction(teacher,Policy(),CostLedger(),teacher_attempts=2,
        construction_teacher_sample=False)
    assert backend.verify(Problem("q","7","gold plan")) is None
    assert len(teacher.calls)==2 and all(c[1]["sample"] is False for c in teacher.calls)
    assert all(r["accepted"] is False and r["reject_reason"]=="incorrect_independent_solution" for r in backend.response_audits)


def test_sampling_profile_cannot_force_scaffold_or_novelty_true():
    teacher=Policy('{"scaffold_safe":false}')
    backend=checkpoint.CheckpointConstruction(teacher,Policy(),CostLedger(),construction_teacher_sample=False)
    parent=Problem("parent","7","parent trace")
    children=[Problem("child-a","1","one"),Problem("child-b","2","two")]
    assert backend.scaffold_safe(parent,children) is False
    teacher.text='{"blueprint_preserved":true,"substantive_novelty":false}'
    assert backend.blueprint_and_novelty(parent,children[0]) is False


def test_greedy_verified_children_still_need_real_scaffold_check_before_effectivity(monkeypatch):
    teacher=Policy('{"scaffold_safe":false}')
    backend=checkpoint.CheckpointConstruction(teacher,Policy(),CostLedger(),construction_teacher_sample=False)
    parent=Problem("different parent","624","complete parent solution")
    # Correct child labels alone do not certify safety: this case is rejected by
    # the unchanged live safety operator, rather than a test forcing acceptance.
    children=[Problem("independent weekly question","6","weekly solution"),
        Problem("independent annual question","312","annual solution")]
    monkeypatch.setattr(backend,"verify",lambda p:p)
    monkeypatch.setattr(backend,"propose_children",lambda *_args:children)
    monkeypatch.setattr(backend,"student_rates",lambda *_args,**kwargs:pytest.fail("conditioned test must not execute")
        if kwargs["worked_examples"] else [0.,1.])
    builder=MagicBeanStalk(backend,depth=1,decomposition_retries=2,synthesis_retries=2)
    assert builder.decompose(parent) is None
    assert len(teacher.calls)==2 and all(c[1]["sample"] is False for c in teacher.calls)
    assert all(x["phase"]=="scaffold-safety" and x["accepted"] is False for x in builder.audit)
    assert "complete parent solution" in str(teacher.calls[0][0])  # teacher-side safety context only
    assert json.loads(teacher.text)["scaffold_safe"] is False
