from dataclasses import replace
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch

from auto_research.post_training.oct12_objectives import (
    BoundaryAssessment, actor_loss, boundary_selection, branch_forks, cast_credit,
    credit_chunks, decoded_alignment, preventive_projection, project_teacher_scores,
    protocol_boundary_loss, rank_normalize, road_credit, selective_anchor,
)
from auto_research.post_training.oct12_checkpoint import (
    OBJECTIVES, ModelRole, boundary_train, branch_step, cast_step, initial_policy, judge_boundary,
    load_role, math_protocol_constraints, normalize_objective, parse_boundary_response, reference_logp, road_step,
    run_adapter, run_checkpoint, sample_path,
)
from auto_research.post_training.oct10_checkpoint import install_lora


def test_branch_selector_uses_both_signals_and_respects_eligibility():
    logits = torch.tensor([[10.,0.,0.],[0.,0.,0.],[10.,0.,0.]])
    student = torch.tensor([-1.,-1.,-1.])
    teacher = torch.tensor([-8.,-1.,-2.])
    eligible = torch.ones(3,dtype=torch.bool)
    assert branch_forks(logits,student,teacher,eligible,budget=1,alpha=1,window=1)[0]==[1]
    assert branch_forks(logits,student,teacher,eligible,budget=1,alpha=0,window=1)[0]==[0]
    eligible[0] = False
    assert branch_forks(logits,student,teacher,eligible,budget=1,alpha=0,window=1)[0]==[2]
    assert branch_forks(logits,student,teacher,eligible,budget=0)[0]==[]
    assert torch.equal(rank_normalize(torch.ones(3)),torch.full((3,),.5))


def test_shared_prefix_mask_removes_its_gradient_and_keeps_fork_token():
    current = torch.zeros(1,5,requires_grad=True)
    mask = torch.tensor([[False,False,True,True,True]])
    actor_loss(current,torch.zeros_like(current),torch.ones_like(current),mask).backward()
    assert torch.equal(current.grad[0,:2],torch.zeros(2))
    assert (current.grad[0,2:]<0).all()


def test_pbr_encourages_good_events_and_suppresses_bad_events():
    logits = torch.zeros(2,4,requires_grad=True)
    protocol_boundary_loss(logits,[(0,(3,),True),(1,(2,),False)]).backward()
    assert logits.grad[0,3]<0 and logits.grad[1,2]>0
    assert protocol_boundary_loss(logits,[])==0


def test_actual_decoded_chunks_many_to_many_and_unreliable_regions():
    student = {1:"a",2:"b",3:"c",4:"\ufffd"}
    teacher = {9:"ab",8:"c",7:"bad"}
    chunks = decoded_alignment([1,2,3],[9,8],lambda ids:"".join(student[i] for i in ids),
                               lambda ids:"".join(teacher[i] for i in ids))
    assert chunks==[((0,1),(0,)),((2,),(1,))]
    projected,aligned = project_teacher_scores(4,torch.tensor([-2.,-3.]),chunks)
    assert projected.tolist()==[-1.,-1.,-3.,0.]
    assert aligned.tolist()==[True,True,True,False]
    assert credit_chunks(aligned,2)==[[0,1],[2]]
    assert decoded_alignment([4],[7],lambda ids:"\ufffd",lambda ids:"bad")==[]
    assert decoded_alignment([1],[9],lambda ids:"  a\n",lambda ids:"a")==[((0,),(0,))]


def test_cast_credit_preserves_gap_and_uses_uncertainty_and_smoothness():
    student = torch.tensor([-3.,-3.,-3.,-3.],requires_grad=True)
    teacher = torch.tensor([-2.,-2.,-2.,-6.],requires_grad=True)
    entropy = torch.tensor([1.,2.,1.,1.],requires_grad=True)
    credit,weights = cast_credit(student,teacher,entropy,[[0,1,2,3]])
    assert credit.sum()==pytest.approx(float((teacher-student).detach().sum()))
    assert weights.sum()==pytest.approx(1.) and weights[1]>weights[0]>weights[3]
    assert not credit.requires_grad and not weights.requires_grad
    constant,_ = cast_credit(torch.full((3,),-2.),torch.full((3,),-1.),torch.ones(3),[[0,1,2]])
    assert torch.allclose(constant,torch.ones(3))


def test_selective_anchor_only_constrains_unaligned_and_initial_reference_detached():
    current = torch.tensor([-1.,-2.],requires_grad=True)
    initial = torch.tensor([-2.,-3.],requires_grad=True)
    loss = selective_anchor(current,initial,torch.tensor([False,True]))
    loss.backward()
    assert current.grad[0]==0 and current.grad[1]!=0 and initial.grad is None
    assert selective_anchor(current,initial,torch.zeros(2,dtype=torch.bool))==0


def test_road_auxiliary_teacher_controls_token_credit_and_preserves_norm():
    current = torch.zeros(1,2)
    routed = torch.tensor([[2.,2.]])
    auxiliary = torch.tensor([[2.,-2.]])
    advantage,coefficient = road_credit(current,routed,auxiliary,current)
    assert coefficient[0,0]>1>coefficient[0,1]
    assert advantage[0,0]>advantage[0,1]
    target,peer = torch.tensor([1.,1.]),torch.tensor([-1.,0.])
    projected,alpha = preventive_projection(target,peer,retention=.5)
    assert alpha==1 and torch.allclose(projected,torch.tensor([0.,1.]))
    opposing,alpha = preventive_projection(torch.tensor([2.,0.]),torch.tensor([-1.,0.]),retention=.4)
    assert torch.allclose(opposing,torch.tensor([.8,0.])) and alpha==pytest.approx(.6)
    assert (projected*peer).sum()>=0
    assert preventive_projection(target,target)[1]==0


def test_boundary_rechecks_mastered_replay_and_acquires_new_frontier():
    assessment = BoundaryAssessment("old",.1,.9,.9,True,True,.9,.8,True)
    first = boundary_selection([assessment,replace(assessment,question="new")],set(),budget=2,replay_quota=1)
    assert {a.question for a in first}=={"old","new"}
    changed = [replace(assessment,student_score=.9),replace(assessment,question="new"),
               replace(assessment,question="next",quality=1.)]
    second = boundary_selection(changed,{"old","new"},budget=2,replay_quota=1)
    assert [a.question for a in second]==["new","next"]
    assert not replace(assessment,expert_score=.4).accepted()
    assert not replace(assessment,clear=False).accepted()


class TinyTokenizer:
    chat_template = None
    eos_token_id = 0
    pad_token_id = 0
    all_special_ids = [0]

    def __init__(self,shift=0):
        self.shift=shift

    def __call__(self,text,return_tensors="pt",add_special_tokens=True):
        values = [((ord(char)-32+self.shift)%63)+1 for char in text] or [1]
        return SimpleNamespace(input_ids=torch.tensor([values]))

    def decode(self,ids,**kwargs):
        return "".join(chr(((int(i)-1-self.shift)%63)+32) for i in ids if int(i)!=0)

    def get_vocab(self):
        return {str(i):(i+self.shift)%64 for i in range(64)}


class TinyLM(torch.nn.Module):
    """Real causal token model for optimizer-path tests, not capability evidence."""
    def __init__(self):
        super().__init__()
        self.embedding=torch.nn.Embedding(64,8)
        self.attention=torch.nn.Module()
        self.attention.q_proj=torch.nn.Linear(8,8)
        self.attention.v_proj=torch.nn.Linear(8,8)
        self.head=torch.nn.Linear(8,64)
        with torch.no_grad():
            self.head.bias[0]=-20.  # Fixed-length runtime fixture, not a reward.

    def forward(self,input_ids,use_cache=False):
        h=self.embedding(input_ids).cumsum(1)
        h=torch.tanh(self.attention.q_proj(h)+self.attention.v_proj(h))
        return SimpleNamespace(logits=self.head(h))

    def generate(self,prompt,max_new_tokens,do_sample,**kwargs):
        ids=prompt.clone()
        for _ in range(max_new_tokens):
            logits=self(ids).logits[:,-1]
            token=torch.multinomial(logits.softmax(-1),1) if do_sample else logits.argmax(-1,keepdim=True)
            ids=torch.cat((ids,token),-1)
            if int(token[0])==0:
                break
        return ids


def role(seed,shift=0,trainable=False):
    torch.manual_seed(seed)
    model=TinyLM().eval()
    model.requires_grad_(False)
    if trainable:
        install_lora(model,rank=2)
    return ModelRole(model,TinyTokenizer(shift),{"id":f"test-model-{seed}","revision":"fixture"},"cpu")


def test_real_branch_optimizer_runs_student_branches_and_excludes_shared_prefix():
    student,teacher=role(1,trainable=True),role(2)
    params=[p for p in student.model.parameters() if p.requires_grad]
    before=[p.detach().clone() for p in params]
    result=branch_step(student,teacher,"Q",torch.optim.SGD(params,lr=.1),max_tokens=5,
                       forks=2,continuations=2,pbr_weight=1.,min_fork_gap=1)
    assert result["branches"]==4 and result["response_tokens"]>0
    assert result["shared_prefix_tokens_excluded"]>0
    assert any(not torch.equal(p,old) for p,old in zip(params,before))
    assert all(p.grad is None for p in teacher.model.parameters())


def test_real_cast_cross_tokenizer_and_reference_restore():
    student,teacher=role(3,trainable=True),role(4,shift=1)
    params=[p for p in student.model.parameters() if p.requires_grad]
    result=cast_step(student,teacher,"Q",torch.optim.SGD(params,lr=.1),max_tokens=5,
                     group=2,credit_size=3,kl_weight=.1)
    assert result["aligned_tokens"]>0 and result["alignment_chunks"]>0
    saved=[p.detach().clone() for p in params]
    with pytest.raises(RuntimeError),initial_policy(student.model):
        raise RuntimeError("check restoration on failure")
    assert all(torch.equal(p,old) for p,old in zip(params,saved))
    ids,_=sample_path(student,"Q",3)
    assert not reference_logp(student,ids).requires_grad


def test_real_road_applies_two_domain_optimizer_update():
    student,teacher,auxiliary=role(5,trainable=True),role(6),role(7)
    params=[p for p in student.model.parameters() if p.requires_grad]
    before=[p.detach().clone() for p in params]
    result=road_step(student,[teacher,auxiliary],[{"question":"A"},{"question":"B"}],
                     torch.optim.SGD(params,lr=.1),max_tokens=4,retention=.5)
    assert result["target_domains"]==2 and result["gradient_l2"]>0
    assert any(not torch.equal(p,old) for p,old in zip(params,before))


def test_boundary_lifecycle_has_priming_refresh_replay_fresh_teacher_and_real_sft(monkeypatch):
    """Diagnostic solver/judge fixtures exercise orchestration, not capabilities."""
    import auto_research.post_training.oct12_checkpoint as runtime
    student,teacher,expert,analyzer=role(11,trainable=True),role(12),role(13),role(14)
    calls=[]
    rows=[{"question":q,"answer":"#### 7"} for q in ("prime","A","B","C")]
    def sample(model,question,max_tokens,**kwargs):
        assert question in {"prime","A","B","C"}  # Never a gold-augmented prompt.
        calls.append((model.identity["id"],question))
        text="#### 8" if question=="prime" else "#### 7"
        ids=model.tokenizer(text).input_ids
        return torch.cat((torch.tensor([[1]]),ids),-1),1
    assessment_calls=[]
    def judge(model,question,reference,student_text,expert_text,max_tokens,*,return_diagnostic=False):
        assessment_calls.append(question)
        round_index=(len(assessment_calls)-1)//3
        mastered=round_index==1 and question=="A"
        expert_score=.1 if round_index==0 and question=="C" else .9
        assessment=BoundaryAssessment(question,.9 if mastered else .1,expert_score,.9,True,True,.9,.9,True)
        raw=json.dumps({name:getattr(assessment,name) for name in
                       ("student_score","expert_score","quality","context_score","completeness",
                        "clear","answerable","recommended")})
        _,diagnostic=parse_boundary_response(question,raw,truncated=False)
        return (assessment,diagnostic) if return_diagnostic else assessment
    monkeypatch.setattr(runtime,"sample_path",sample)
    monkeypatch.setattr(runtime,"judge_boundary",judge)
    params=[p for p in student.model.parameters() if p.requires_grad]
    before=[p.detach().clone() for p in params]
    history=boundary_train(student,teacher,expert,analyzer,rows,torch.optim.SGD(params,lr=.1),
        max_tokens=16,priming_examples=1,rounds=2,pool_examples=3,acquisition=2,replay_quota=1,
        teacher_rollouts=2,analyzer_tokens=128)
    assert history[0]["stage"]=="priming"  # Incorrect trajectory was not filtered.
    evolution=history[1:]
    assert [item["optimizer_steps"] for item in evolution]==[2,2]
    assert evolution[0]["selected_question_sha256"]!=evolution[1]["selected_question_sha256"]
    assert assessment_calls==["A","B","C","A","B","C"]
    assert all(event["analyzer_parse_failure_classes"]=={} for event in evolution)
    assert all(event["analyzer_budget_exhaustions"]==0 for event in evolution)
    assert sum(identifier==teacher.identity["id"] for identifier,_ in calls)==9
    assert any(not torch.equal(p,old) for p,old in zip(params,before))


def test_analyzer_parse_failures_are_not_replaced_by_constant_rewards(monkeypatch):
    import auto_research.post_training.oct12_checkpoint as runtime
    monkeypatch.setattr(runtime,"sample_path",lambda *args,**kwargs:(None,0))
    monkeypatch.setattr(runtime,"decoded_response",lambda *args:"invalid judge response")
    assert judge_boundary(None,"Q","#### 7","student","expert",64) is None


def boundary_json(**changes):
    record={"student_score":.1,"expert_score":.9,"quality":.9,"context_score":.9,
            "completeness":.8,"clear":True,"answerable":True,"recommended":True}
    record.update(changes)
    return json.dumps(record)


@pytest.mark.parametrize("raw,expected",[
    ("analysis with no JSON", "no_complete_flat_json_candidate"),
    ('{"student_score": broken}', "json_decode_error"),
    ('{"student_score": 0.1}', "missing_required_fields"),
    (boundary_json(quality="not a score"), "invalid_score_type_or_value"),
    (boundary_json(expert_score=1.01), "score_out_of_range_or_nonfinite"),
    (boundary_json(quality=float("nan")), "score_out_of_range_or_nonfinite"),
    (boundary_json(recommended="true"), "non_boolean_flag"),
])
def test_boundary_parse_failures_are_precise_hashed_and_never_repaired(raw,expected):
    import hashlib
    assessment,diagnostic=parse_boundary_response("Q",raw,response_tokens=64,token_budget=64,truncated=True)
    assert assessment is None and diagnostic["parse_failure_class"]==expected
    assert diagnostic["response_sha256"]==hashlib.sha256(raw.encode()).hexdigest()
    assert diagnostic["truncated"] is True and diagnostic["response_tokens"]==64
    assert raw not in json.dumps(diagnostic)


@pytest.mark.parametrize("changes",[
    {"expert_score":.64},{"student_score":.5},{"expert_score":.65,"student_score":.46},
    {"quality":.69},{"context_score":.69},{"clear":False},{"answerable":False},
])
def test_boundary_valid_json_does_not_relax_original_acceptance_thresholds(changes):
    assessment,diagnostic=parse_boundary_response("Q",boundary_json(**changes))
    assert assessment is not None and not assessment.accepted()
    assert diagnostic["parse_failure_class"] is None  # Selection rejection is not a parse failure.


@pytest.mark.parametrize("emitted,expected",[([2,3,4],True),([2,3,0],False),([2,3],False)])
def test_boundary_judge_diagnostics_keep_gold_model_text_private_and_track_budget(monkeypatch,emitted,expected):
    import auto_research.post_training.oct12_checkpoint as runtime
    analyzer=SimpleNamespace(tokenizer=SimpleNamespace(eos_token_id=0),
                             model=SimpleNamespace(generation_config=SimpleNamespace(eos_token_id=[0,9])))
    received=[]
    def generate(model,prompt,max_tokens,**kwargs):
        received.append(prompt)
        return torch.tensor([[1]+emitted]),1
    raw="sensitive-model-prelude\n"+boundary_json()
    monkeypatch.setattr(runtime,"sample_path",generate)
    monkeypatch.setattr(runtime,"decoded_response",lambda *args:raw)
    assessment,diagnostic=judge_boundary(analyzer,"question","reference-secret", "student-secret",
        "expert-secret",3,return_diagnostic=True)
    assert assessment.accepted() and diagnostic["truncated"] is expected
    assert diagnostic["response_tokens"]==len(emitted) and diagnostic["token_budget"]==3
    assert "reference-secret" in received[0]  # External training judge only.
    serialized=json.dumps(diagnostic)
    assert all(secret not in serialized for secret in
               ("reference-secret","student-secret","expert-secret","sensitive-model-prelude"))


def test_boundary_all_parse_failures_keep_real_priming_but_no_fake_evolution(monkeypatch):
    """Real tiny SFT + deliberately invalid analyzer fixture; no capability evidence."""
    import auto_research.post_training.oct12_checkpoint as runtime
    student,teacher,expert,analyzer=role(91,trainable=True),role(92),role(93),role(94)
    original_decode=runtime.decoded_response
    invalid='{"student_score": 0.1'  # Incomplete output is never repaired into a judgment.
    monkeypatch.setattr(runtime,"decoded_response",lambda model,*args:invalid if model is analyzer
                        else original_decode(model,*args))
    rows=[{"question":question,"answer":"#### 9876"} for question in ("prime","A","B","C","D")]
    params=[p for p in student.model.parameters() if p.requires_grad]
    before=[p.detach().clone() for p in params]
    history=boundary_train(student,teacher,expert,analyzer,rows,torch.optim.SGD(params,lr=.1),
        max_tokens=2,priming_examples=1,rounds=2,pool_examples=4,acquisition=2,replay_quota=1,
        teacher_rollouts=2,analyzer_tokens=2)
    assert history[0]["stage"]=="priming"
    assert any(not torch.equal(p,old) for p,old in zip(params,before))
    evolution=history[1:]
    assert len(evolution)==2 and sum(event["analyzer_parse_failures"] for event in evolution)==8
    assert all(event["optimizer_steps"]==event["selected_questions"]==0 for event in evolution)
    assert all(event["analyzer_parse_failure_classes"]=={"no_complete_flat_json_candidate":4}
               for event in evolution)
    assert all(len(event["analyzer_parse_diagnostics"])==4 for event in evolution)
    serialized=json.dumps(evolution)
    assert invalid not in serialized and "#### 9876" not in serialized


def test_boundary_real_judge_prompt_requires_all_eight_typed_fields_without_score_examples(monkeypatch):
    """L0 captures the actual production judge prompt; it is not a model/GPU run."""
    import auto_research.post_training.oct12_checkpoint as runtime
    received=[]
    def capture(model,prompt,max_tokens,**kwargs):
        received.append((prompt,max_tokens,kwargs))
        return None,0
    monkeypatch.setattr(runtime,"sample_path",capture)
    monkeypatch.setattr(runtime,"decoded_response",lambda *args:boundary_json(recommended=False))
    assessment,diagnostic=judge_boundary(None,"fixture-question","reference-secret","student-secret",
        "expert-secret",768,return_diagnostic=True)
    prompt,budget,kwargs=received[0]
    schema_text,evidence_text=prompt.split("JSON Schema:\n",1)[1].split("\nInput evidence:\n",1)
    schema=json.loads(schema_text)
    scores={"student_score","expert_score","quality","context_score","completeness"}
    flags={"clear","answerable","recommended"}
    assert schema["$schema"]=="https://json-schema.org/draft/2020-12/schema"
    assert schema["type"]=="object" and schema["additionalProperties"] is False
    assert set(schema["required"])==set(schema["properties"])==scores|flags
    assert all({key:schema["properties"][name][key] for key in ("type","minimum","maximum")}
               =={"type":"number","minimum":0,"maximum":1} for name in scores)
    assert all(set(schema["properties"][name])=={"type","minimum","maximum","description"}
               for name in scores)
    assert all(schema["properties"][name]["type"]=="boolean" for name in flags)
    assert "genuine recommendation" in schema["properties"]["recommended"]["description"]
    assert all(forbidden not in schema_text for forbidden in ('"default"','"const"','"enum"','"examples"'))
    assert '"recommended": true' not in prompt and '"recommended": false' not in prompt
    assert json.loads(evidence_text)=={"question":"fixture-question","reference":"reference-secret",
        "student_response":"student-secret","expert_response":"expert-secret"}
    assert budget==768 and kwargs=={"greedy":True}
    assert assessment.recommended is False and diagnostic["parse_failure_class"] is None


def test_boundary_real_judge_prompt_separates_qa_validity_from_student_trajectory_quality(monkeypatch):
    """L0 semantic contract from paper Section 3.2/F.3, not judge calibration or GPU evidence."""
    import auto_research.post_training.oct12_checkpoint as runtime
    received=[]
    monkeypatch.setattr(runtime,"sample_path",lambda model,prompt,*args,**kwargs:
                        (received.append(prompt) or (None,0)))
    monkeypatch.setattr(runtime,"decoded_response",lambda *args:boundary_json())
    judge_boundary(None,"fixture-question","reference-secret","student-secret","expert-secret",768)
    prompt=received[0]
    schema_text,evidence_text=prompt.split("JSON Schema:\n",1)[1].split("\nInput evidence:\n",1)
    properties=json.loads(schema_text)["properties"]
    descriptions={name:prop["description"] for name,prop in properties.items()}
    assert "actual student_response" in descriptions["student_score"]
    assert "actual expert_response" in descriptions["expert_score"]
    assert "independently" in descriptions["student_score"]
    assert "independently" in descriptions["expert_score"]
    assert all(term in descriptions["quality"] for term in
               ("QA pair","question clarity","answerability","reference correctness","training usefulness"))
    assert "student being wrong or incomplete" in descriptions["quality"]
    assert "question" in descriptions["clear"] and "not the student's response" in descriptions["clear"]
    assert "question" in descriptions["answerable"] and "not whether the student solved it" in descriptions["answerable"]
    assert "no external context is provided or needed" in descriptions["context_score"]
    assert "judge must report 1.0 by definition" in descriptions["context_score"]
    assert "not student correctness" in descriptions["context_score"]
    assert "actual student_response" in descriptions["completeness"]
    assert "ranking" in descriptions["completeness"]
    assert "not a hard acceptance gate" in descriptions["recommended"]
    assert "not an override" in descriptions["recommended"]
    assert "No separate external context is provided in this input" in prompt
    assert "role names do not imply that the expert is better" in prompt
    assert "Do not adjust scores to satisfy the filters" in prompt
    for criterion in ("expert_score >= 0.65","student_score < 0.50",
                      "expert_score - student_score >= 0.20","quality >= 0.70",
                      "context_score >= 0.70","clear and answerable"):
        assert criterion in prompt
    assert json.loads(evidence_text)=={"question":"fixture-question","reference":"reference-secret",
        "student_response":"student-secret","expert_response":"expert-secret"}
    assert all(forbidden not in schema_text for forbidden in ('"default"','"const"','"enum"','"examples"'))


@pytest.mark.parametrize("changes",[
    {"expert_score":.64},{"student_score":.5},{"expert_score":.65,"student_score":.46},
    {"quality":.69},{"context_score":.2},{"clear":False},{"answerable":False},
])
def test_boundary_semantic_prompt_keeps_original_gate_rejections_and_never_fills_context(monkeypatch,changes):
    import auto_research.post_training.oct12_checkpoint as runtime
    monkeypatch.setattr(runtime,"sample_path",lambda *args,**kwargs:(None,0))
    monkeypatch.setattr(runtime,"decoded_response",lambda *args:boundary_json(**changes))
    assessment,diagnostic=judge_boundary(None,"Q","reference","student","expert",768,
                                       return_diagnostic=True)
    assert diagnostic["parse_failure_class"] is None and assessment is not None
    assert not assessment.accepted()
    for name,value in changes.items():
        assert getattr(assessment,name)==value  # Judge output is not repaired or forced to pass.


def test_boundary_recommendation_and_completeness_are_ranking_only_not_extra_gates(monkeypatch):
    import auto_research.post_training.oct12_checkpoint as runtime
    monkeypatch.setattr(runtime,"sample_path",lambda *args,**kwargs:(None,0))
    monkeypatch.setattr(runtime,"decoded_response",lambda *args:boundary_json(recommended=False,completeness=0.))
    assessment=judge_boundary(None,"Q","reference","student","expert",768)
    assert assessment.accepted() and assessment.recommended is False and assessment.completeness==0.
    assert boundary_selection([assessment],set(),budget=1,replay_quota=0)==[assessment]


def test_boundary_completed_old_response_missing_recommended_still_fails_with_no_alias_or_repair(monkeypatch):
    import auto_research.post_training.oct12_checkpoint as runtime
    record=json.loads(boundary_json())
    record.pop("recommended")
    for substitute in (None,"recommendation","is_recommended","accepted_recommendation"):
        raw=json.dumps({**record,**({substitute:True} if substitute else {})})
        monkeypatch.setattr(runtime,"sample_path",lambda *args,**kwargs:(torch.tensor([[1,2,0]]),1))
        monkeypatch.setattr(runtime,"decoded_response",lambda *args:raw)
        assessment,diagnostic=judge_boundary(SimpleNamespace(tokenizer=SimpleNamespace(eos_token_id=0)),
            "Q","reference","student","expert",768,return_diagnostic=True)
        assert assessment is None and diagnostic["parse_failure_class"]=="missing_required_fields"
        assert diagnostic["missing_required_fields"]==["recommended"]
        assert diagnostic["truncated"] is False


def test_load_role_rejects_arbitrary_directory_before_model_loading(tmp_path):
    with pytest.raises(ValueError,match="safe checkpoint"):
        load_role(tmp_path,"public/model","a"*40,"cpu")


def test_load_role_requires_local_manifest_hashes_before_model_loading(tmp_path):
    import hashlib
    config=tmp_path/"config.json"
    config.write_text("{}")
    manifest={"kind":"checkpoint","public_id":"public/model","revision":"a"*40,
              "files":{"config.json":hashlib.sha256(config.read_bytes()).hexdigest(),
                       "model.safetensors":"0"*64}}
    (tmp_path/"model.safetensors").write_bytes(b"arbitrary local weights")
    (tmp_path/"provenance.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError,match="SHA256 mismatch"):
        load_role(tmp_path,"public/model","a"*40,"cpu")


def test_pbr_detects_boxed_completion_without_gold():
    tokenizer=SimpleNamespace(eos_token_id=0,decode=lambda ids,**kwargs:"")
    tokenizer.decode=lambda ids,**kwargs:"\\boxed{7}" if len(ids)>=3 else "reasoning"
    assert math_protocol_constraints(tokenizer,[1,2,3,4],prompt_length=5)==[(7,(0,),True)]
    assert math_protocol_constraints(tokenizer,[1,2,3,4],prompt_length=5,fork=8)==[]


def test_adapter_requires_real_checkpoint_config_and_rejects_test_input(tmp_path):
    with pytest.raises(ValueError,match="real checkpoint"):
        run_adapter("cast-opd",tmp_path,42)
    (tmp_path/"oct12-cast-opd.json").write_text(json.dumps({"test_path":"secret.jsonl"}))
    with pytest.raises(ValueError,match="forbidden test"):
        run_adapter("cast-opd",tmp_path,42)


def test_cast_namespace_is_canonical_and_legacy_agent_cast_catalog_is_unchanged():
    root=Path(__file__).resolve().parents[1]
    assert OBJECTIVES == ("branch-opd","cast-opd","road-mopd","boundary-evo")
    assert normalize_objective("cast") == normalize_objective("cast-opd") == "cast-opd"
    with pytest.raises(ValueError,match="invalid October"):
        normalize_objective("unrelated-cast")
    legacy=json.loads((root/"src/auto_research/paper_specs/catalog/agent-research/cast.json").read_text())
    current=json.loads((root/"src/auto_research/paper_specs/catalog/post-training/cast-opd.json").read_text())
    assert legacy["key"] == "cast" and legacy["paper_url"].endswith("2607.25308")
    assert current["key"] == "cast-opd" and current["paper_url"].endswith("2610.13257")
    assert current["title"].startswith("CAST:")
    assert not (root/"src/auto_research/paper_specs/catalog/post-training/cast.json").exists()
    assert not (root/"src/auto_research/reproductions/cast/paper.yaml").exists()
    spec=json.loads((root/"src/auto_research/reproductions/cast_opd/paper.yaml").read_text())
    assert spec["key"] == "cast-opd"
    assert spec["adapter_module"] == "auto_research.reproductions.cast_opd.adapter"
    assert spec["local_code"] == "src/auto_research/reproductions/cast_opd"
    assert spec["documentation"] == "docs/reproductions/2610.13257-cast-opd/README.md"


@pytest.mark.parametrize("objective",["cast","cast-opd"])
def test_cast_runtime_alias_enters_actual_loss_and_outputs_canonical_key(tmp_path,monkeypatch,objective):
    """Tiny optimizer fixture validates branch binding, not public-model capability."""
    import auto_research.post_training.oct12_checkpoint as runtime
    train=tmp_path/"train.jsonl"
    valid=tmp_path/"validation.jsonl"
    train.write_text(json.dumps({"question":"train Q","answer":"#### 7"})+"\n")
    valid.write_text(json.dumps({"question":"valid Q","answer":"#### 9"})+"\n")
    monkeypatch.setattr(runtime,"validate_holdout",lambda *args,**kwargs:{
        "verified":True,"source_id":"unit-fixture-only","test_read":False})
    monkeypatch.setattr(runtime,"load_role",lambda path,*args:role(
        51 if path=="student" else 52,shift=0 if path=="student" else 1))
    real_cast=runtime.cast_step
    calls=[]
    def record_loss(*args,**kwargs):
        calls.append(args[2])
        return real_cast(*args,**kwargs)
    def forbidden_road(*args,**kwargs):
        pytest.fail("a CAST spelling must never fall through to the Road loss")
    monkeypatch.setattr(runtime,"cast_step",record_loss)
    monkeypatch.setattr(runtime,"road_step",forbidden_road)
    output=tmp_path/"result.json"
    result=run_checkpoint(objective=objective,student_path="student",student_id="fixture/student",
        student_revision="a"*40,teacher_path="teacher",teacher_id="fixture/teacher",teacher_revision="b"*40,
        train_path=train,validation_path=valid,dataset_revision="c"*40,split_manifest=tmp_path/"fixture-split.json",
        output=output,steps=1,group=2,max_tokens=4,validation_examples=1,device="cpu")
    assert calls == ["train Q"]
    assert result["adapter_key"] == json.loads(output.read_text())["adapter_key"] == "cast-opd"
    assert result["metrics"]["aligned_tokens"] > 0
    assert result["metrics"]["adapter_parameter_delta_l2"] > 0
    assert "projected_tensors" not in result["metrics"]
    assert not result["gold_in_rollout"] and not result["test_read"]


@pytest.mark.parametrize("objective",["cast","cast-opd"])
def test_cast_alias_keeps_heterogeneous_tokenizer_requirement(tmp_path,monkeypatch,objective):
    import auto_research.post_training.oct12_checkpoint as runtime
    monkeypatch.setattr(runtime,"validate_holdout",lambda *args,**kwargs:{"verified":True})
    monkeypatch.setattr(runtime,"load_public_rows",lambda *args:[{"question":"Q","answer":"#### 7"}])
    monkeypatch.setattr(runtime,"load_role",lambda *args:role(1))
    with pytest.raises(ValueError,match="actual cross-tokenizer"):
        run_checkpoint(objective=objective,student_path="student",student_id="fixture/student",
            student_revision="a"*40,teacher_path="teacher",teacher_id="fixture/teacher",teacher_revision="b"*40,
            train_path=tmp_path/"train",validation_path=tmp_path/"valid",dataset_revision="c"*40,
            split_manifest=tmp_path/"split",output=tmp_path/"out",device="cpu")
    assert not (tmp_path/"out").exists()


@pytest.mark.parametrize("configured_objective",[None,"cast","cast-opd"])
def test_canonical_cast_adapter_config_binds_paths_seed_and_output_key(tmp_path,monkeypatch,configured_objective):
    import auto_research.post_training.oct12_checkpoint as runtime
    config={"student_path":"checkpoints/student","train_path":"train.jsonl","output":"run.json","seed":999}
    if configured_objective is not None:
        config["objective"]=configured_objective
    (tmp_path/"oct12-cast-opd.json").write_text(json.dumps(config))
    captured=[]
    def diagnostic_run(**kwargs):
        captured.append(kwargs)
        return {"schema_version":1,"adapter_key":kwargs["objective"],"diagnostic_only":True}
    monkeypatch.setattr(runtime,"run_checkpoint",diagnostic_run)
    result=run_adapter("cast-opd",tmp_path,42)
    assert result["adapter_key"] == "cast-opd" and "schema_version" not in result
    assert captured[0]["objective"] == "cast-opd" and captured[0]["seed"] == 42
    assert captured[0]["student_path"] == tmp_path/"checkpoints/student"
    assert captured[0]["train_path"] == tmp_path/"train.jsonl"
    assert captured[0]["output"] == tmp_path/"run.json"


def test_adapter_rejects_old_key_file_foreign_objective_and_wrong_result_binding(tmp_path,monkeypatch):
    import auto_research.post_training.oct12_checkpoint as runtime
    (tmp_path/"oct12-cast.json").write_text(json.dumps({"objective":"cast"}))
    with pytest.raises(ValueError,match="canonical objective key"):
        run_adapter("cast",tmp_path,42)
    with pytest.raises(ValueError,match="real checkpoint"):
        run_adapter("cast-opd",tmp_path,42)
    canonical=tmp_path/"oct12-cast-opd.json"
    canonical.write_text(json.dumps({"objective":"branch-opd"}))
    with pytest.raises(ValueError,match="adapter objective mismatch"):
        run_adapter("cast-opd",tmp_path,42)
    canonical.write_text(json.dumps({"objective":"cast-opd"}))
    monkeypatch.setattr(runtime,"run_checkpoint",lambda **kwargs:{"adapter_key":"cast"})
    with pytest.raises(ValueError,match="result adapter key differs"):
        run_adapter("cast-opd",tmp_path,42)


@pytest.mark.parametrize("spelling",["cast","cast-opd"])
def test_cli_alias_normalizes_before_dispatch_without_loading_model(monkeypatch,spelling):
    import importlib.util
    script=Path(__file__).resolve().parents[1]/"scripts/run_oct12_post_training.py"
    spec=importlib.util.spec_from_file_location("oct12_post_training_cli_fixture",script)
    cli=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    captured=[]
    monkeypatch.setattr(cli,"run_checkpoint",lambda **kwargs:captured.append(kwargs))
    args=["--objective",spelling]
    for flag in ("student-path","student-id","teacher-path","teacher-id","train-path",
                 "validation-path","split-manifest","output"):
        args.extend(["--"+flag,"fixture"])
    for flag in ("student-revision","teacher-revision","dataset-revision"):
        args.extend(["--"+flag,"a"*40])
    cli.main(args)
    assert captured[0]["objective"] == "cast-opd"


def test_solver_interface_and_gold_isolation():
    import inspect
    assert "reference" not in inspect.signature(sample_path).parameters
    source=inspect.getsource(branch_step)+inspect.getsource(cast_step)+inspect.getsource(road_step)
    assert "answer" not in source and "verified_reward" not in source
    assert "gold" not in inspect.getsource(sample_path)


@pytest.mark.parametrize("key,id",[("branch-opd","2610.13481"),("cast-opd","2610.13257"),
                                  ("road-mopd","2610.13521"),("boundary-evo","2610.13285")])
def test_paper_metadata_and_original_evidence_complete(key,id):
    root=Path(__file__).resolve().parents[1]
    spec=json.loads((root/f"src/auto_research/reproductions/{key.replace('-','_')}/paper.yaml").read_text())
    catalog=json.loads((root/f"src/auto_research/paper_specs/catalog/post-training/{key}.json").read_text())
    assert catalog["adapter"] == {"spec_key": key}
    assert spec["published"]==catalog["published"]=="2026-10-09"
    assert spec["upstream_code"] and spec["organization"] and spec["execution"]["requires_gpu_validation"]
    text=(root/spec["documentation"]).read_text()
    for label in ("论文链接","公司/机构","首次公开日期","原文开源代码","Adapter",
                  "本地复现代码","原始论文总结","核心公式","论文离线与线上效果","复现边界"):
        assert label in text
    evidence=json.loads((root/f"docs/reproductions/{id}-{key}/paper-results.json").read_text())
    assert evidence["paper_reported"] is True and evidence["measured_locally"] is False
    assert (root/f"docs/reproductions/{id}-{key}/assets/paper-figure-01.png").is_file()
