"""L0/L1 behavior contracts; fixtures here are NOT checkpoint capability evidence."""
from __future__ import annotations

from types import SimpleNamespace
import math

import pytest
import torch

from auto_research.post_training.oct13_common import (CostLedger,causal_response_features,
    policy_gradient_step,sample_prefix)
from auto_research.post_training.response_policy import GeneratedResponse
from auto_research.reproductions.magicbeanstalk.algorithm import MagicBeanStalk,Problem,goldilocks
from auto_research.reproductions.magicbeanstalk.checkpoint import CheckpointConstruction,_problem
from auto_research.reproductions.synthself.algorithm import rewrite_messages,select_aligner,validate_aligner
from auto_research.reproductions.grpo_difficulty_curriculum.algorithm import (
    BANDS,PlateauSchedule,band_gate,difficulty_dynamics)
from auto_research.reproductions.progressive_contraction.algorithm import (
    contract_teacher_pool,monte_carlo_uncertainty,normalized_response_nll,paragraph_prefixes,route_student)
from auto_research.reproductions.upturn.algorithm import (PositionHead,CorrectnessGate,boxed_token_position,
    calibrated_gate,intervention_messages,position_loss,remaining_response_budget)
from auto_research.reproductions.soar.algorithm import (LexicalRetriever,internal_messages,
    parse_step,source_match,source_observation,source_reward)


class DiagnosticConstruction:
    def __init__(self,effective=True,target_rewards=(0,1)):
        self.effective=effective
        self.target_rewards=target_rewards
        self.composed_children=[]
    def verify(self,p):
        return p
    def student_rates(self,p,*,worked_examples,through_student=None):
        if p.question.startswith("new"):
            return [.5]
        rates=[0.,.5] if not worked_examples else ([.5,.5] if self.effective else [0.,.5])
        return rates if through_student is None else rates[:through_student+1]
    def propose_children(self,p,negative):
        return [Problem("child-a","2","child trace"),Problem("child-b","3","child trace")]
    def harder_leaf(self,p):
        return Problem("new "+p.question,"4","new independent leaf trace")
    def scaffold_safe(self,parent,children):
        return True
    def compose(self,node,children):
        self.composed_children.append(children)
        return Problem("new composed parent","9","new parent trace")
    def blueprint_and_novelty(self,original,candidate):
        return True
    def target_outcomes(self,p):
        return (list(self.target_rewards),[False,False]) if p.question.startswith("new") else ([0,0],[False,False])


def test_mbs_runs_top_down_effectivity_then_bottom_up_child_composition():
    backend=DiagnosticConstruction()
    builder=MagicBeanStalk(backend)
    result=builder.construct(Problem("hard parent","7","verified root"))
    assert result.question=="new composed parent"
    assert len(backend.composed_children[0])==2
    assert all(p.question.startswith("new child") for p in backend.composed_children[0])
    phases=[row["phase"] for row in builder.audit]
    assert phases[:2]==["seed-hardness-calibration","effectivity"] and phases[-1]=="target-policy-goldilocks"


def test_mbs_effectivity_does_not_replace_final_target_goldilocks():
    builder=MagicBeanStalk(DiagnosticConstruction(target_rewards=(1,1)))
    assert builder.construct(Problem("hard parent","7","trace")) is None
    assert builder.audit[1]["accepted"] and not builder.audit[-1]["accepted"]
    builder=MagicBeanStalk(DiagnosticConstruction(effective=False),decomposition_retries=2)
    assert builder.construct(Problem("hard parent","7","trace")) is None
    assert len([r for r in builder.audit if r["phase"]=="effectivity"])==2


def test_mbs_requires_a_complete_correct_solution_and_mixed_outcomes():
    assert goldilocks([0,1],[False,False])
    assert not goldilocks([0,1],[False,True])
    assert not goldilocks([0,0],[False,False])


def test_mbs_budget_truncation_is_not_a_verified_hard_seed():
    backend=DiagnosticConstruction()
    backend.target_outcomes=lambda p:([0,0],[True,False])
    builder=MagicBeanStalk(backend)
    assert builder.construct(Problem("hard parent","7","trace")) is None
    assert builder.audit==[{"phase":"seed-hardness-calibration","accepted":False,
                           "rewards":[0,0],"truncated":[True,False]}]


def test_mbs_json_numeric_answers_are_valid_serialization_not_fabricated_labels():
    assert _problem({"question":"public synthetic question","answer":7,"trace":"worked trace"}).answer=="7"
    assert _problem({"question":"public synthetic question","answer":float("nan"),"trace":"worked trace"}) is None
    assert _problem({"question":"public synthetic question","answer":True,"trace":"worked trace"}) is None


def test_mbs_effectivity_prompt_never_contains_parent_gold_or_parent_plan():
    class Policy:
        def __init__(self): self.messages=[]
        def generate(self,messages,**kwargs):
            self.messages.append(messages)
            return [GeneratedResponse((1,),"\\boxed{1}",False)]*kwargs.get("samples",1)
    teacher,student=Policy(),Policy()
    backend=CheckpointConstruction(teacher,student,CostLedger(),rollouts=2)
    parent=Problem("parent public question","999","SECRET PARENT PLAN")
    backend.student_rates(parent,worked_examples=[Problem("separate child","2","Child worked solution 2")])
    payload=str(student.messages)
    assert "999" not in payload and "SECRET PARENT PLAN" not in payload
    assert "separate child" in payload


def test_mbs_effectivity_costs_separate_teacher_and_student_tokens():
    class Policy:
        def __init__(self,length): self.length=length
        def generate(self,messages,**kwargs):
            return [GeneratedResponse(tuple(range(self.length)),"\\boxed{1}",False)]*kwargs["samples"]
    ledger=CostLedger()
    backend=CheckpointConstruction(Policy(5),Policy(2),ledger,rollouts=3)
    problem=Problem("public training question","1","verified train-only trace")
    assert backend.student_rates(problem,worked_examples=())==[1.,1.]
    assert ledger.generated_tokens=={"effectivity_student":6,"effectivity_teacher":15}
    assert ledger.calls=={"effectivity_student":1,"effectivity_teacher":1}
    assert backend.student_rates(problem,worked_examples=(),through_student=0)==[1.]
    assert ledger.generated_tokens=={"effectivity_student":12,"effectivity_teacher":15}
    assert ledger.calls=={"effectivity_student":2,"effectivity_teacher":1}


def test_synthself_aligner_family_quality_and_distribution_constraints():
    validate_aligner("Qwen/Qwen2.5-0.5B-Instruct","Qwen/Qwen2.5-7B-Instruct",5,70)
    with pytest.raises(ValueError,match="same-family"):
        validate_aligner("Qwen/Qwen2.5-0.5B","google/gemma-7B",5,70)
    with pytest.raises(ValueError,match="larger"):
        validate_aligner("Qwen/Qwen2.5-7B","Qwen/Qwen2.5-0.5B",70,5)
    candidates=[{"id":"a","nll":.8,"quality":.6},{"id":"b","nll":.7,"quality":.8}]
    assert select_aligner(candidates,gold_nll=1.,self_quality=.6)["id"]=="b"
    assert select_aligner(candidates,gold_nll=.7,self_quality=.6) is None
    assert "Keep the SAME final answer" in rewrite_messages("train question","train demo")[0]["content"]


def test_curriculum_paper_bands_and_current_outcomes_not_problem_length():
    assert len(BANDS)==5
    assert band_gate([1,1,1,1,0,0,0,0],BANDS[2])
    assert not band_gate([1]*8,BANDS[2])
    assert band_gate([0]*8,(0.,.125))
    assert not band_gate([0]*8,BANDS[4])
    for rewards in ([0,1],[0,0]):
        assert band_gate(rewards,(0.,1.))


def test_curriculum_plateau_uses_two_diagnostics_and_noise_tolerance():
    schedule=PlateauSchedule()
    assert schedule.observe(.5)=="new-best"
    assert schedule.observe(.505)=="keep"
    assert schedule.observe(.49)=="advance"
    assert schedule.stage==1
    assert schedule.observe(.6)=="new-best"
    assert schedule.observe(.63)=="new-best"
    assert schedule.stale_evaluations==0


def test_nonmonotonic_difficulty_dynamics_retain_round_trip_motion():
    audit=difficulty_dynamics([[0.,1.],[.5,.5],[0.,0.]])
    assert audit["span"]==[.5,1.]
    assert audit["total_variation"]==[1.,1.]
    assert audit["extra_round_trip_variation"]==[.5,0.]


def test_contraction_uses_actual_mc_outcomes_not_teacher_confidence():
    assert monte_carlo_uncertainty([0,1])["uncertainty"]==1.
    assert monte_carlo_uncertainty([1,1])["uncertainty"]==0.
    assert monte_carlo_uncertainty([0,0])["uncertainty"]==0.
    profiles=[[monte_carlo_uncertainty([0,0])],[monte_carlo_uncertainty([0,1])]]
    selected,scores=contract_teacher_pool(profiles,.5)
    assert selected==[1] and scores==[0.,1.]
    with pytest.raises(ValueError,match="zero"):
        contract_teacher_pool(profiles,.1)


def test_student_routing_is_current_length_normalized_nll():
    assert normalized_response_nll(torch.tensor([-1.,-1.]))==1.
    assert normalized_response_nll(torch.tensor([-1.]*10))==1.
    assert route_student([1.,3.,2.],1)==[1]
    assert route_student([4.,1.,2.],1)==[0]
    assert paragraph_prefixes((1,9,9,2,9,9,3),(9,9),limit=3)==[3,6]


def test_mcrt_samples_exact_open_assistant_prefix_and_charges_teacher_tokens():
    class Model:
        def eval(self): return self
        def generate(self,ids,**kwargs):
            self.seen=ids.tolist()
            return torch.cat((ids,torch.tensor([[4,0]])),dim=-1).repeat(kwargs["num_return_sequences"],1)
    model=Model()
    tokenizer=SimpleNamespace(eos_token_id=0,pad_token_id=0,decode=lambda ids,**kw:"answer")
    policy=SimpleNamespace(prompt_ids=lambda _:torch.tensor([[7,8]]),device="cpu",context_limit=32,
                           model=model,tokenizer=tokenizer)
    ledger=CostLedger()
    responses=sample_prefix(policy,({"role":"user","content":"public question"},),(9,10),ledger,samples=3,max_tokens=8)
    assert model.seen==[[7,8,9,10]]
    assert all(r.tokens==(4,0) and not r.truncated for r in responses)
    assert ledger.generated_tokens["teacher_profile"]==6


def test_frozen_causal_encoder_prefix_features_do_not_see_discarded_suffix():
    class Backbone:
        def __call__(self,ids,**kwargs):
            return SimpleNamespace(last_hidden_state=ids.float().cumsum(-1)[...,None])
    class Model:
        model=Backbone()
        def eval(self): return self
    encoder=SimpleNamespace(prompt_ids=lambda _:torch.tensor([[1]]),device="cpu",context_limit=32,model=Model())
    first=causal_response_features(encoder,[],(2,3,4))
    second=causal_response_features(encoder,[],(2,3,999))
    assert torch.equal(first[:2],second[:2]) and not first.requires_grad


def test_upturn_real_heads_detach_encoder_and_receive_rescue_gradient():
    torch.manual_seed(42)
    features=torch.randn(3,8,requires_grad=True)
    head=PositionHead(8,width=4)
    logits=head(features)
    old=logits.detach().log_softmax(-1)[:2]
    loss,audit=position_loss(logits,[0,1],old,[0.,1.],entropy_beta=0.)
    loss.backward()
    assert audit["advantages"]==[-.5,.5]
    assert audit["nonzero_rescue_advantage"]
    assert features.grad is None
    assert sum(float(p.grad.abs().sum()) for p in head.parameters())>0
    gate=CorrectnessGate(8,width=4)
    gate_loss=torch.nn.functional.binary_cross_entropy_with_logits(gate(features),torch.tensor([0.,1.,0.]))
    gate_loss.backward()
    assert features.grad is None


def test_upturn_new_user_turn_budget_and_unclosed_think_handling():
    messages=intervention_messages(({"role":"user","content":"public question"},),"<think>retained reasoning")
    assert [m["role"] for m in messages]==["user","assistant","user"]
    assert messages[1]["content"].endswith("</think>")
    assert messages[2]["content"]=="Resolve this concisely."
    assert remaining_response_budget(512,200)==312
    with pytest.raises(ValueError): remaining_response_budget(512,512)
    assert calibrated_gate(torch.tensor(9.),parseable=False)==0


def test_upturn_new_user_turn_preserves_exact_original_cut_tokens():
    from auto_research.reproductions.upturn.checkpoint import intervention_prefix_tokens
    from auto_research.post_training.oct13_common import ExecutionFailure
    class Tokenizer:
        chat_template="diagnostic-chat-template"
        def decode(self,tokens,**kwargs):
            return "".join(chr(x) for x in tokens)
        def __call__(self,text,**kwargs):
            return SimpleNamespace(input_ids=list(map(ord,text)))
        def apply_chat_template(self,messages,**kwargs):
            text="user:"+messages[0]["content"]+"assistant:"
            if len(messages)>1:
                text+=messages[1]["content"]+"<end>user:"+messages[2]["content"]+"assistant:"
            return text
    reasoner=SimpleNamespace(tokenizer=Tokenizer())
    messages=({"role":"user","content":"public question"},)
    prefix=tuple(map(ord,"retained reasoning\n\n"))
    combined=intervention_prefix_tokens(reasoner,messages,prefix)
    assert combined[:len(prefix)]==prefix
    assert "<end>user:Resolve this concisely.assistant:" in reasoner.tokenizer.decode(combined[len(prefix):])
    original=reasoner.tokenizer.apply_chat_template
    reasoner.tokenizer.apply_chat_template=lambda messages,**kwargs:original(messages,**kwargs).replace("assistant:","changed:") if len(messages)>1 else original(messages,**kwargs)
    with pytest.raises(ExecutionFailure,match="open-assistant prefix"):
        intervention_prefix_tokens(reasoner,messages,prefix)


def test_box_position_uses_original_tokens_and_last_parseable_box():
    tokenizer=SimpleNamespace(decode=lambda tokens,**kwargs:"".join(chr(x) for x in tokens))
    text="old \\boxed{2}, new \\boxed{3}"
    tokens=tuple(map(ord,text))
    assert boxed_token_position(tokens,tokenizer)==text.rfind("\\boxed")
    assert boxed_token_position(tuple(map(ord,"no final box")),tokenizer) is None


def test_soar_internal_recall_is_isolated_and_source_matching_is_declared():
    messages=internal_messages("atomic public query")
    assert messages[-1]["content"]=="atomic public query"
    assert "previous" not in str(messages) and "external" not in str(messages)
    observation=source_observation("internal Beijing","external Shanghai")
    assert "internal: internal Beijing" in observation and "external: external Shanghai" in observation
    final=parse_step("<information_source>external</information_source><answer>Beijing</answer>")
    reward,parts=source_reward(final,{"internal":"Beijing","external":"Shanghai"},answer_correct=1.)
    assert parts=={"answer":1.,"format":1.,"source_match":0.}
    assert reward==pytest.approx(1.2/1.3)
    final["source"]="internal"
    reward,parts=source_reward(final,{"internal":"Beijing","external":"Shanghai"},answer_correct=1.)
    assert parts["source_match"]==1. and reward==pytest.approx(1.)


def test_soar_real_retriever_rejects_label_corpus_and_ambiguous_actions():
    with pytest.raises(ValueError,match="labels"):
        LexicalRetriever([{"text":"evidence","answer":"gold"}])
    retriever=LexicalRetriever([{"text":"Earth orbits the Sun","source_url":"https://en.wikipedia.org/wiki/Earth"},
                               {"text":"A triangle has three sides","source_url":"https://en.wikipedia.org/wiki/Triangle"}])
    assert "triangle" in retriever.retrieve("triangle",1)[0]["text"]
    assert parse_step("<search>x</search><answer>y</answer>")["kind"]=="invalid"
    assert source_match("cat","A cat is here") and not source_match("cat","cats")


def test_real_parameter_update_and_zero_advantage_do_not_use_weight_decay_as_evidence():
    class Toy(torch.nn.Module):
        def __init__(self):
            super().__init__();self.weight=torch.nn.Parameter(torch.tensor(.1))
    class Policy:
        device="cpu"
        def __init__(self):
            self.model=Toy();self.optimizer=torch.optim.AdamW(self.model.parameters(),lr=.01)
        def token_statistics(self,messages,tokens):
            return -1+self.model.weight*torch.tensor(tokens,dtype=torch.float32),None
    policy=Policy();ledger=CostLedger()
    group=[([{"role":"user","content":"public"}],GeneratedResponse((i,),"answer",False)) for i in (1,2)]
    old=[torch.tensor([-1.]),torch.tensor([-1.])]
    before=policy.model.weight.detach().clone()
    audit=policy_gradient_step(policy,group,[0.,1.],ledger,behavior_log_probs=old)
    assert audit["optimizer_update_executed"] and not torch.equal(before,policy.model.weight)
    before=policy.model.weight.detach().clone()
    audit=policy_gradient_step(policy,group,[0.,0.],ledger,behavior_log_probs=old)
    assert not audit["optimizer_update_executed"] and torch.equal(before,policy.model.weight)


def test_synthself_checkpoint_isolates_gold_to_offline_builders_and_sft_targets(monkeypatch):
    from auto_research.reproductions.synthself import checkpoint
    policies=[]
    class Policy:
        vocabulary_sha256="diagnostic-vocabulary"
        device="cpu"
        provenance={"public_id":"diagnostic-fixture"}
        def __init__(self,role):
            self.role=role
            self.model=torch.nn.Linear(1,2 if role=="teacher" else 1,bias=False)
            self.model.requires_grad_(False)
            self.messages=[]
            self.tokenizer=lambda text,**kwargs:SimpleNamespace(input_ids=[1,2,1,2])
            self.tokenizer.eos_token_id=0
        def generate(self,messages,**kwargs):
            self.messages.append(messages)
            return [GeneratedResponse((1,2,0),"\\boxed{997}" if self.role=="teacher" else "\\boxed{13}",False)]
        def token_statistics(self,messages,tokens):
            return -2+self.model.weight.mean()*torch.tensor(tokens,dtype=torch.float32),None
        def prepare_lora(self,**kwargs):
            self.model.requires_grad_(True)
            self.optimizer=torch.optim.AdamW(self.model.parameters(),lr=.01)
        def trainable_digest(self):
            return str(self.model.weight.detach().tolist())
    def load(config,*,role="student",seed=42):
        p=Policy(role);policies.append(p);return p
    monkeypatch.setattr(checkpoint,"load_policy",load)
    train=[{"question":"public train question","answer":"997"}]
    validation=[{"question":"public acquisition question","answer":"13"},
                {"question":"public retention question","answer":"17"}]
    monkeypatch.setattr(checkpoint,"load_split",lambda config:(train,validation,{"verified":True}))
    result=checkpoint.run({"student_id":"Qwen/Qwen2.5-0.5B-Instruct","teacher_id":"Qwen/Qwen2.5-7B-Instruct",
                           "device":"cpu","epochs":1,"max_tokens":8},seed=42)
    assert result["parameters_changed"]
    assert "997" not in str(policies[0].messages)  # trained/evaluated student
    assert "997" in str(policies[1].messages)      # external train-only aligner
    assert "997" in str(policies[2].messages)      # separate frozen self-construction teacher
    assert "997" not in str(policies[3].messages)  # gold-SFT control generation
    assert result["protocol"]["gold_in_student_generation"] is False


def test_staged_curriculum_cannot_advance_without_actual_effective_update(monkeypatch):
    from auto_research.reproductions.grpo_difficulty_curriculum import checkpoint
    class Policy:
        device="cpu"
        provenance={"public_id":"diagnostic-fixture"}
        def __init__(self):
            self.model=torch.nn.Linear(1,1,bias=False)
        def prepare_lora(self,**kwargs):
            self.optimizer=torch.optim.AdamW(self.model.parameters(),lr=.01)
        def trainable_digest(self):
            return str(self.model.weight.detach().tolist())
        def generate(self,messages,**kwargs):
            return [GeneratedResponse((1,),"\\boxed{0}",False)]*kwargs["samples"]
        def token_statistics(self,messages,tokens):
            return torch.tensor([-1.]),None
    policy=Policy()
    monkeypatch.setattr(checkpoint,"load_policy",lambda *args,**kwargs:policy)
    monkeypatch.setattr(checkpoint,"load_split",lambda config:([
        {"question":"public question","answer":"999"}], [{"question":"heldout question","answer":"3"}], {"verified":True}))
    monkeypatch.setattr(checkpoint,"evaluate",lambda *args,**kwargs:{"accuracy":0.,"examples":1})
    result=checkpoint.run({"device":"cpu","variant":"staged","steps":4,"group":4},seed=42)
    assert not result["parameters_changed"]
    assert result["execution_status"]=="failed-no-effective-updates"
    assert all(row["transition"]=="no-effective-updates" and row["band"]==BANDS[0] for row in result["training"])
