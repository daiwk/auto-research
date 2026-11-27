import math

import numpy as np
import pytest
import torch

from auto_research.foundation_models import integral_deltanet as integral
from auto_research.foundation_models import deco_attention as deco


@pytest.mark.parametrize('module',[integral,deco])
@pytest.mark.parametrize('seed',[42,43,44])
def test_cpu_diagnostic_contract(module,seed):
    out=module.diagnostic(seed)
    assert out['seed']==seed and out['device']=='cpu'
    assert out['evaluation_tier']=='l1_mechanism' and out['diagnostic_only']
    assert not module.REQUIRES_GPU_VALIDATION
    assert all(type(v) is bool and v for v in out['checks'].values()),out
    assert all(type(v) in (float,int) and math.isfinite(v) for v in out['metrics'].values())
    with pytest.raises(ValueError):module.diagnostic(seed,'cuda')


def test_integral_resume_and_channel_gate_extremes():
    q=torch.tensor([[1.,0.],[0.,1.],[1.,1.]],dtype=torch.float64)
    k=torch.nn.functional.normalize(q,dim=-1);v=q.clone()
    one=torch.ones_like(q);zero=torch.zeros_like(q)
    # alpha=1,beta=1 gives DeltaNet. lambda=0 leaves X at zero.
    output,states=integral.recurrent(q,k,v,one,one,one,zero,zero)
    assert torch.equal(output,zero)
    assert torch.equal(states[1],torch.zeros(2,2,dtype=q.dtype))
    args=[q,k,v,one,one,one,one,one]
    full,final=integral.recurrent(*args)
    prefix,mid=integral.recurrent(*(a[:1] for a in args))
    suffix,end=integral.chunkwise(*(a[1:] for a in args),states=mid,chunk_size=1)
    torch.testing.assert_close(torch.cat([prefix,suffix]),full)
    for a,b in zip(final,end):torch.testing.assert_close(a,b)
    assert torch.equal(end[0],end[1])


def test_integral_channel_readout_is_not_scalar_mix():
    q=torch.ones(1,2,dtype=torch.float64);k=q/np.sqrt(2);v=q
    one=torch.ones_like(q);zero=torch.zeros_like(q)
    # Frozen incoming S/X, no write/decay. gamma chooses different states by key channel.
    s=torch.tensor([[1.,10.],[3.,20.]],dtype=q.dtype)
    x=torch.tensor([[100.,2.],[200.,4.]],dtype=q.dtype)
    gamma=torch.tensor([[1.,0.]],dtype=q.dtype)
    out,_=integral.recurrent(q,k,v,one,zero,zero,zero,gamma,states=(s,x))
    torch.testing.assert_close(out,torch.tensor([[3.,7.]],dtype=q.dtype))
    with pytest.raises(ValueError):integral.recurrent(q,k,v,one*2,zero,zero,zero,gamma)


def test_nvfp4_rounding_codebooks_scales_and_ties():
    x=np.tile(np.array([0,.25,.75,1.25,1.75,2.5,3.5,5.,-5.,6.,0,0,0,0,0,0]),(1,1))
    expected=np.array([0,0,1,1,2,2,4,4,-4,6,0,0,0,0,0,0])
    np.testing.assert_array_equal(deco.round_codebook(x,deco.E2M1)[0],expected)
    decoded,scales=deco.nvfp4_round(np.zeros((2,16)))
    assert not decoded.any() and not scales['block_scales'].any()
    decoded,scales=deco.nvfp4_round(np.arange(32.).reshape(2,16))
    assert scales['group_scale']==2.**math.ceil(math.log2(31/(6*448)))
    assert np.isin(scales['block_scales'],deco.E4M3).all()
    norm=np.divide(decoded.reshape(2,1,16),scales['group_scale']*scales['block_scales'][:,:,None])
    assert np.isin(np.abs(norm),deco.E2M1).all()


def test_deco_basis_uses_trace_normalized_raw_grams_and_rotation():
    rng=np.random.default_rng(5);q=rng.normal(size=(64,32));k=100*rng.normal(size=(64,32))
    b,_=deco.principal_basis(q,k,rank=8,sample_indices=np.arange(64))
    scaled,_=deco.principal_basis(q*100,k*.001,rank=8,sample_indices=np.arange(64))
    np.testing.assert_allclose(b@b.T,scaled@scaled.T,atol=1e-11)
    h=deco.hadamard(32,seed=5)
    np.testing.assert_allclose((q@h)@(k@h).T,q@k.T,atol=1e-10)
    with pytest.raises(ValueError):deco.prepare(q,k,rank=3)
    with pytest.raises(ValueError):deco.principal_basis(q,k,rank=33)
    with pytest.raises(ValueError):deco.principal_basis(q,k,rank=8,sample_indices=[1,1])


def test_deco_requantizes_compensation_and_keeps_original_softmax_scale():
    rng=np.random.default_rng(19)
    q=rng.normal(size=(64,32));k=rng.normal(size=(64,32));v=rng.normal(size=(64,4))
    output,p=deco.compensated_attention(q,k,v,rank=16)
    scores=p['q_extended']@p['k_extended'].T/np.sqrt(32)
    probabilities=np.exp(scores-scores.max(1,keepdims=True));probabilities/=probabilities.sum(1,keepdims=True)
    np.testing.assert_allclose(output,probabilities@v,atol=1e-12)
    dq=p['q_rotated']-p['q_quantized']
    assert not np.allclose(p['q_extended'][:,32:48],dq@p['basis'])
    # A zero head has finite zero compensation, not a trace-normalization NaN.
    zero,_=deco.compensated_attention(np.zeros_like(q),np.zeros_like(k),v,rank=16)
    np.testing.assert_allclose(zero,np.tile(v.mean(0),(len(q),1)),atol=1e-12)


@pytest.mark.parametrize('value',[np.nextafter(0.,1.),np.finfo(np.float64).max])
def test_deco_rejects_out_of_range_finite_magnitudes_without_nan(value):
    matrix=np.full((4,16),value)
    with pytest.raises(ValueError,match='max-absolute value'):
        deco.nvfp4_round(matrix)
    with pytest.raises(ValueError,match='max-absolute value'):
        deco.principal_basis(matrix,matrix,rank=4)


@pytest.mark.parametrize('value',[2.**-400,2.**400])
def test_deco_declared_numeric_endpoints_remain_finite(value):
    matrix=np.full((4,16),value)
    decoded,_=deco.nvfp4_round(matrix)
    basis,_=deco.principal_basis(matrix,matrix,rank=4)
    assert np.isfinite(decoded).all() and np.isfinite(basis).all()
