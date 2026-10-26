"""Independent references for scoped L1 components, never capability scores."""
import math
from dataclasses import replace
import pytest
import torch

from auto_research.post_training.opst import verification_gate, masked_divergence_mean, ema_update
from auto_research.agent_research.frontier_opd import Occurrence, response_scores, select_frontier, accept_bridge
from auto_research.post_training.mart_grpo import Event, boundary_from_event, feedback_mask, mart_grpo_loss


def test_opst_candidate_consensus_not_general_consensus_and_external_duplicates():
    fresh=torch.tensor([1,1,1,0,1],dtype=torch.bool)
    paraphrase=torch.tensor([1,1,0,1,1],dtype=torch.bool)
    matches=torch.tensor([[0,0,0],[1,1,1],[0,1,0],[0,1,0],[0,1,1]],dtype=torch.bool)
    assert verification_gate(fresh,paraphrase,matches).tolist()==[True,False,False,False,True]
    assert not verification_gate(fresh,paraphrase,matches,duplicate=torch.tensor([1,0,0,0,1],dtype=torch.bool)).any()
    with pytest.raises(ValueError):verification_gate(fresh.float(),paraphrase,matches)
    with pytest.raises(ValueError):verification_gate(fresh,paraphrase,matches[:,:0])


def test_opst_external_divergence_reduction_equal_responses_padding_nan_and_gradient():
    values=torch.tensor([[2.,4.,6.],[9.,float('nan'),float('nan')]],dtype=torch.float64,requires_grad=True)
    mask=torch.tensor([[1,1,1],[1,0,0]],dtype=torch.bool)
    loss=masked_divergence_mean(values,mask)
    assert loss.item()==6.5 and loss.item()!=pytest.approx(21/4)
    loss.backward()
    torch.testing.assert_close(values.grad,torch.tensor([[1/6,1/6,1/6],[.5,0,0]],dtype=torch.float64))
    with pytest.raises(ValueError):masked_divergence_mean(values,torch.zeros_like(mask))
    with pytest.raises(ValueError):masked_divergence_mean(-torch.ones_like(values),mask)
    x=torch.ones(2,2,dtype=torch.bfloat16,requires_grad=True)
    assert masked_divergence_mean(x,torch.ones_like(x,dtype=torch.bool)).dtype==torch.float32


def test_opst_ema_is_new_student_weight_and_detached_without_mutation():
    teacher=torch.tensor([2.,4.],requires_grad=True);student=torch.tensor([10.,20.],requires_grad=True)
    result=ema_update(teacher,student,beta=.05)
    torch.testing.assert_close(result,torch.tensor([2.4,4.8]))
    assert not result.requires_grad and teacher.tolist()==[2.,4.]
    torch.testing.assert_close(ema_update(teacher,student,beta=0),teacher)
    torch.testing.assert_close(ema_update(teacher,student,beta=1),student)
    for beta in [-.1,1.1,float('nan')]:
        with pytest.raises(ValueError):ema_update(teacher,student,beta=beta)


def test_opst_printed_mixture_counterexample_not_silently_repaired():
    # q=(0,1), p=(1,0), alpha=.8. Printed weights violate stated H(alpha).
    a=.8
    literal=-a*math.log(1-a)-(1-a)*math.log(a)
    matching=-a*math.log(a)-(1-a)*math.log(1-a)
    assert literal>matching and literal==pytest.approx(1.3321790402101223)
    assert matching==pytest.approx(.5004024235381879)


def test_frontier_signed_and_absolute_scores_normalize_within_response_ignore_padding():
    student=torch.tensor([[-1.,-3.,float('nan')],[-2.,-2.,-2.]],requires_grad=True)
    teacher=torch.tensor([[-2.,-2.,float('nan')],[-1.,-1.,-1.]],requires_grad=True)
    mask=torch.tensor([[1,1,0],[1,1,1]],dtype=torch.bool)
    signed,agreement=response_scores(student,teacher,mask)
    torch.testing.assert_close(signed,torch.tensor([0.,-1.]))
    torch.testing.assert_close(agreement,torch.tensor([-1.,-1.]))
    assert not signed.requires_grad and not agreement.requires_grad
    with pytest.raises(ValueError):response_scores(student,teacher,torch.zeros_like(mask))


def occurrence(i,t,node,d,**kwargs):
    return Occurrence(i,t,node,d,kwargs.get('valid',True),kwargs.get('replay',True),kwargs.get('remaining',8))


def test_frontier_trajectory_balancing_distinct_nodes_threshold_and_ties():
    visits=[occurrence(0,j,'loop',10) for j in range(3)]
    visits += [occurrence(1,0,'loop',0),occurrence(1,1,'other',6),occurrence(1,2,'same-trajectory',6),
               occurrence(2,0,'invalid',100,replay=False),occurrence(2,1,'short',100,remaining=3)]
    result=select_frontier(visits,budget=3)
    assert [c.node for c in result]==['other','same-trajectory','loop']
    assert result[-1].score==5 and result[-1].representative.turn==0
    assert len(select_frontier(visits,budget=5,min_score=6))==2
    negative=[occurrence(0,0,'negative',-2)]
    assert select_frontier(negative,budget=1)[0].score==-2
    assert select_frontier(negative,budget=1,min_score=0)==[]
    with pytest.raises(ValueError):select_frontier(visits+[visits[0]],budget=1)


def test_frontier_bridge_uses_realized_joint_window_and_rejects_invalid_measurements():
    flags=dict(bridge_length=1,continuation_horizon=2,replay_succeeded=True,nonterminal_handoff=True,continuation_complete=True)
    # Bridge improves joint mean despite slightly worse continuation: it is NOT
    # an assertion of continuation-alone or task-success improvement.
    old=torch.tensor([-5.,-1.,-1.]);new=torch.tensor([-.1,-1.2,-1.2])
    accepted,gain=accept_bridge(old,new,**flags)
    assert accepted and gain==pytest.approx(1.5)
    assert accept_bridge(old,old,**flags)==(True,0.)
    assert accept_bridge(old,new,**{**flags,'nonterminal_handoff':False})==(False,None)
    assert accept_bridge(old,new[:2],**flags)==(False,None)
    assert accept_bridge(old,torch.tensor([float('nan'),-1.,-1.]),**flags)==(False,None)


def test_mart_external_event_schema_identity_and_semantic_fallbacks():
    event=Event('id','failure','drop',(1,2),'none')
    assert boundary_from_event(event,episode_id='id',executed_chunks=4)==2
    for fallback in [replace(event,outcome='success'),replace(event,outcome='uncertain'),replace(event,error_type='uncertain'),replace(event,interval=None),replace(event,recovery='observed'),replace(event,recovery='uncertain')]:
        assert boundary_from_event(fallback,episode_id='id',executed_chunks=4)==3
    for invalid in [replace(event,episode_id='other'),replace(event,interval=(2,1)),replace(event,interval=(0,4)),replace(event,interval=(True,2)),replace(event,outcome='bad')]:
        with pytest.raises(ValueError):boundary_from_event(invalid,episode_id='id',executed_chunks=4)


def test_mart_mask_success_inclusive_failure_and_empty_prefix():
    ids=torch.tensor([[0,0,1,2],[0,0,1,2],[0,0,1,2]])
    valid=torch.ones_like(ids,dtype=torch.bool)
    mask=feedback_mask(torch.tensor([1.,0.,0.]),torch.tensor([-9,1,-1]),ids,valid)
    assert mask.tolist()==[[True]*4,[True,True,True,False],[False]*4]
    with pytest.raises(ValueError):feedback_mask(torch.tensor([1.,0.,0.]),torch.tensor([-9,3,-1]),ids,valid)


def test_mart_matches_independent_clipped_objective_and_original_denominator_gradient():
    current=torch.tensor([[-1.,-3.,-1.,-2.],[-1.,-1.,-2.,float('nan')]],dtype=torch.float64,requires_grad=True)
    old=torch.tensor([[-2.,-2.,-2.,-2.],[-2.,-2.,-2.,float('nan')]],dtype=torch.float64,requires_grad=True)
    advantage=torch.tensor([1.,-1.],dtype=torch.float64,requires_grad=True)
    valid=torch.tensor([[1,1,1,1],[1,1,1,0]],dtype=torch.bool)
    feedback=torch.tensor([[1,1,1,1],[1,0,0,0]],dtype=torch.bool)
    actual=mart_grpo_loss(current,old,advantage,feedback,valid)
    reference=torch.stack([-torch.minimum((current[0]-old[0].detach()).exp(),(current[0]-old[0].detach()).exp().clamp(.8,1.28)).mean(),
        torch.maximum((current[1,0]-old[1,0].detach()).exp(),(current[1,0]-old[1,0].detach()).exp().clamp(.8,1.28))/3]).mean()
    expected_grad=torch.autograd.grad(reference,current,retain_graph=True)[0]
    torch.testing.assert_close(actual,reference)
    actual.backward();torch.testing.assert_close(current.grad,expected_grad)
    assert old.grad is None and advantage.grad is None and (current.grad[1,1:]==0).all()
    zero=mart_grpo_loss(current,old,advantage,torch.zeros_like(valid),valid)
    assert zero.requires_grad and zero.item()==0


@pytest.mark.parametrize('module',[
    'auto_research.post_training.opst','auto_research.agent_research.frontier_opd','auto_research.post_training.mart_grpo'])
@pytest.mark.parametrize('seed',[42,43,44])
def test_diagnostics_are_finite_true_l1_not_capability(module,seed):
    from importlib import import_module
    result=import_module(module).diagnostic(seed)
    assert result['diagnostic_only'] is True and result['seed']==seed
    assert all(type(v) is bool and v for v in result['checks'].values())
    assert all(isinstance(v,(int,float)) and math.isfinite(v) for v in result['metrics'].values())
    with pytest.raises(ValueError):import_module(module).diagnostic(seed,device='mps')
