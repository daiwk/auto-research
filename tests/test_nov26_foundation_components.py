import json
import math

import numpy as np
import pytest
import torch

from auto_research.foundation_models import rap, duomi


@pytest.mark.parametrize('module',[rap,duomi])
@pytest.mark.parametrize('seed',[42,43,44])
def test_diagnostic_contract(module,seed):
    result = module.diagnostic(seed)
    assert result['seed'] == seed and result['device'] == 'cpu'
    assert result['evaluation_tier'] == 'l1_mechanism' and result['diagnostic_only'] is True
    assert module.REQUIRES_GPU_VALIDATION is False
    assert result['checks'] and all(type(v) is bool and v for v in result['checks'].values())
    assert all(type(v) in (float,int) and math.isfinite(v) for v in result['metrics'].values())
    json.dumps(result,allow_nan=False)
    with pytest.raises(ValueError): module.diagnostic(seed,'cuda')


def test_rap_nonunit_curvature_anchor_and_same_ray():
    r=np.array([0.,.2,1.,2.])
    x=rap.polar_to_lorentz(r,np.tile([1.,0.,0.],(4,1)),curvature=.3)
    y=rap.project_rap(x,np.array([[2.,1.,0.],[0.,1.,1.]]),curvature=.3)
    assert np.allclose(rap.lorentz_to_polar(y,curvature=.3)[0],r,atol=1e-12)
    assert np.allclose(rap.pairwise_distance(y,curvature=.3),np.abs(r[:,None]-r[None,:]),atol=1e-7)


def test_rap_rejects_projection_kernel_invalid_manifold_and_nonfinite():
    x=rap.polar_to_lorentz([1.],[[1.,0.]])
    with pytest.raises(ValueError): rap.project_rap(x,[[0.,1.]])
    with pytest.raises(ValueError): rap.project_rap([[1.,1.,0.]],[[1.,0.]])
    with pytest.raises(ValueError): rap.project_rap(x,[[float('nan'),0.]])
    with pytest.raises(ValueError): rap.polar_to_lorentz([1.],[[2.,0.]])
    with pytest.raises(ValueError): rap.polar_to_lorentz([1.],[[1.,0.]],curvature=0)


def test_rap_large_radius_duplicates_and_same_ray_regression():
    # Previously a positive 1-u@u residual yielded off-diagonal distances
    # 3.33567789 for duplicates and 2.70891464 for a .001 radial difference.
    u=np.array([-.6370261718724837,.6054639418752776,.19470884074042197,
                -.3156568318899905,.1318040638054588,-.19446817569865765,
                -.0938671750895791,.16142823204922757])
    radii=np.array([20.,20.,20.001,20.00000001])
    x=rap.polar_to_lorentz(radii,np.tile(u,(len(radii),1)))
    actual=rap.pairwise_distance(x)
    expected=np.abs(radii[:,None]-radii[None,:])
    assert actual[0,1] == actual[1,0] == 0
    np.testing.assert_allclose(actual,expected,atol=1e-12,rtol=1e-7)
    assert actual[0,3] > 0  # The half-angle formula retains sub-cosh-resolution gaps.
    np.testing.assert_array_equal(actual,actual.T)


def test_rap_large_radius_small_angular_separation_is_not_erased():
    theta=1e-8
    u=np.array([[1.,0.],[np.cos(theta),np.sin(theta)]])
    x=rap.polar_to_lorentz([20.,20.],u)
    # Equal-radius identity: sinh(d/2)=sinh(r)*sin(theta/2).
    expected=2*np.arcsinh(np.sinh(20.)*np.sin(theta/2))
    np.testing.assert_allclose(rap.pairwise_distance(x)[0,1],expected,atol=1e-12)


def test_duomi_group_before_threshold_and_padding():
    # One group violates the marginal threshold while the pooled distribution
    # cancels. A loss thresholded after global averaging would incorrectly be 0.
    a=torch.tensor([[[20.,-20.]]]*8+[[[-20.,20.]]]*8,dtype=torch.float64,requires_grad=True)
    b=-a
    valid=torch.ones(16,1,dtype=torch.bool)
    loss,stats=duomi.duomi_penalty(a,b,valid,g_max=.1,d_min=0,d_max=1)
    p,q=a.softmax(-1),b.softmax(-1)
    assert duomi.jsd_bits(p.mean((0,1)),q.mean((0,1))) == 0
    assert loss > .08 and torch.all(stats['g'] > .99)
    padded_a=torch.cat([a,torch.full_like(a,1000)],dim=1)
    padded_b=torch.cat([b,torch.full_like(b,-1000)],dim=1)
    mask=torch.cat([valid,torch.zeros_like(valid)],dim=1)
    padded_loss,_=duomi.duomi_penalty(padded_a,padded_b,mask,g_max=.1,d_min=0,d_max=1)
    assert torch.equal(loss,padded_loss)


def test_duomi_soft_gradients_and_hard_overlap_are_not_conflated():
    a=torch.tensor([[[3.,2.,1.]]]*8,dtype=torch.float64,requires_grad=True)
    b=torch.tensor([[[3.,2.,-1.]]]*8,dtype=torch.float64,requires_grad=True)
    valid=torch.ones(8,1,dtype=torch.bool)
    loss,stats=duomi.duomi_penalty(a,b,valid,d_min=.5,d_max=.8)
    assert torch.equal(a.topk(2).indices,b.topk(2).indices)
    assert stats['d'].item() > 0
    loss.backward()
    assert a.grad[...,2].abs().sum() > 0 and b.grad[...,2].abs().sum() > 0


def test_duomi_paired_shared_pool_interface_and_rejections():
    model=duomi.PairedSharedExperts(width=4,experts=4,top_k=2).double()
    output,logits,picks=model(torch.randn(8,2,4,dtype=torch.float64))
    assert output.shape == (8,2,4) and len(logits) == len(picks) == 2
    assert len(list(model.experts)) == 4
    assert model.routers[0].weight.data_ptr() != model.routers[1].weight.data_ptr()
    mask=torch.ones(8,2,dtype=torch.bool)
    with pytest.raises(ValueError): duomi.duomi_penalty(logits[0][:7],logits[1][:7],mask[:7])
    with pytest.raises(ValueError): duomi.duomi_penalty(*logits,torch.zeros_like(mask))
    with pytest.raises(ValueError): duomi.duomi_penalty(*logits,mask,d_min=.5,d_max=.1)
    with pytest.raises(ValueError): duomi.duomi_penalty(*logits,mask,temperature=0)
