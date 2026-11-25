import pytest
import torch
from torch.nn import functional as F

from auto_research.reproductions.lazunirec_components import (
    DirectionEMA, diagnostic, gradient_evidence, ranking_to_retrieval_kd,
    sparse_expert_mix, task_lora_projection, weighted_task_loss,
)


@pytest.mark.parametrize("seed",[42,43,44])
def test_diagnostic(seed):
    assert all(diagnostic(seed)["checks"].values())


def test_low_rank_projection_and_history_bypass():
    x=torch.tensor([[1.,2.],[3.,4.],[5.,6.]])
    w=torch.eye(2)
    a=(torch.ones(1,2),2*torch.ones(1,2))
    b=(torch.ones(2,1),torch.ones(2,1))
    out=task_lora_projection(x,w,a,b,torch.tensor([-1,0,1]))
    assert torch.equal(out[0],x[0])
    assert torch.equal(out[1],x[1]+7)
    assert torch.equal(out[2],x[2]+22)


def test_private_expert_is_added_not_included_in_softmax():
    p=torch.tensor([[5.,7.]])
    shared=torch.tensor([[[2.,4.],[4.,8.],[1000.,1000.]]])
    scores=torch.tensor([[0.,0.,-100.]])
    out,weights,_=sparse_expert_mix(p,shared,scores)
    assert torch.allclose(weights,torch.full((1,2),.5))
    assert torch.allclose(out,p+torch.tensor([[3.,6.]]))


def test_gradient_moments_clamp_variance_and_cap_evidence():
    e,var=gradient_evidence(torch.tensor([1.,0.]),torch.tensor([.9,4.]),epsilon=.25,maximum=1.)
    assert torch.equal(var,torch.tensor([0.,4.]))
    assert torch.allclose(e,torch.tensor([1.,1/(4.25**.5)]))


def test_clipping_after_normalization_does_not_renormalize():
    losses=torch.tensor([2.,3.,4.],requires_grad=True)
    evidence=[torch.tensor([1e-3],requires_grad=True),torch.tensor([1.],requires_grad=True),torch.tensor([1.],requires_grad=True)]
    total,weights=weighted_task_loss(losses,evidence)
    assert torch.allclose(weights,torch.tensor([.8,1.2,1.2]))
    assert not torch.isclose(weights.mean(),torch.tensor(1.))
    total.backward()
    assert torch.equal(losses.grad,weights)
    assert all(e.grad is None for e in evidence)


def test_kd_multiplies_interest_probability_before_max_and_detaches_teacher():
    u=torch.tensor([[[1.,0.],[0.,2.]]],requires_grad=True)
    v=torch.tensor([[[1.,2.],[3.,1.]]],requires_grad=True)
    pi=torch.tensor([[.8,.2]],requires_grad=True)
    teacher=torch.tensor([[.2,.5]],requires_grad=True)
    loss,scores=ranking_to_retrieval_kd(u,v,pi,teacher,ranking_temperature=.7,retrieval_temperature=.3)
    expected=torch.tensor([[.8,2.4]])
    assert torch.allclose(scores,expected)
    log_t=F.log_softmax(teacher.detach()/.7,1)
    assert torch.allclose(loss,(log_t.exp()*(log_t-F.log_softmax(expected/.3,1))).sum())
    loss.backward()
    assert teacher.grad is None and u.grad is not None and pi.grad is not None


def test_no_cross_request_candidate_distribution():
    u=torch.ones(2,1,1)
    v=torch.tensor([[[1.],[2.]],[[3.],[4.]]])
    pi=torch.ones(2,1)
    teacher=torch.zeros(2,2)
    first,_=ranking_to_retrieval_kd(u,v,pi,teacher,retrieval_temperature=1.)
    altered=v.clone()+torch.tensor([[[0.]],[[100.]]])
    second,_=ranking_to_retrieval_kd(u,altered,pi,teacher,retrieval_temperature=1.)
    assert torch.allclose(first,second)


def test_ema_scenario_task_isolation_and_bad_inputs():
    ema=DirectionEMA()
    ema.observe("a",0,torch.tensor([1.,0.]))
    ema.observe("b",1,torch.tensor([0.,1.]))
    assert set(ema.states)=={("a",0),("b",1)}
    assert all(not t.requires_grad for pair in ema.states.values() for t in pair)
    with pytest.raises(ValueError):
        ema.observe("a",0,torch.zeros(2))
    with pytest.raises(ValueError):
        weighted_task_loss(torch.ones(1),[torch.zeros(2)])
    with pytest.raises(ValueError):
        sparse_expert_mix(torch.ones(1,2),torch.ones(1,2,2),torch.ones(1,2),k=3)
    with pytest.raises(ValueError):
        gradient_evidence(torch.ones(2),torch.ones(2),epsilon=0)
