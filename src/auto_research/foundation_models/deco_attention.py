"""DeCo v1 principal residual compensation; CPU numerical emulation only.

Eqs1--6 and25 are evaluated on decoded low-precision values with FP64 products.
No NVFP4 MMA, CuTe kernel, I-ExpCast, PV quantization or hardware speedup exists.
"""
from __future__ import annotations

import math
import numpy as np

REQUIRES_GPU_VALIDATION=False
E2M1=np.array([0.,.5,1.,1.5,2.,3.,4.,6.])
E4M3=np.array([m*2.**-9 for m in range(8)]+[(1+m/8)*2.**(e-7) for e in range(1,15) for m in range(8)]+[(1+m/8)*256 for m in range(7)])
# Deliberately bounded FP64 reference, not all finite IEEE-754 magnitudes.
# This keeps Eq25's group-scale division and raw Gram products representable.
MIN_NONZERO_MATRIX_MAX=2.**-400
MAX_MATRIX_MAX=2.**400


def _matrix(x):
    a=np.asarray(x,dtype=np.float64)
    if a.ndim!=2 or min(a.shape)<1 or not np.isfinite(a).all():raise ValueError('finite nonempty CPU matrix required')
    maximum=float(np.abs(a).max())
    if maximum and not MIN_NONZERO_MATRIX_MAX<=maximum<=MAX_MATRIX_MAX:
        raise ValueError('matrix max-absolute value must be zero or in [2**-400, 2**400]')
    return a


def _matmul(left,right):
    """Fail explicitly if a finite supported input produces an unsafe product."""
    try:
        with np.errstate(over='raise',invalid='raise'):
            result=left@right
    except FloatingPointError as exc:
        raise ValueError('unrepresentable FP64 matrix product') from exc
    if not np.isfinite(result).all():raise ValueError('unrepresentable FP64 matrix product')
    return result


def round_codebook(x,levels):
    """Symmetric nearest-even rounding, finite values only; code parity breaks ties."""
    x=np.asarray(x,dtype=np.float64)
    if not np.isfinite(x).all():raise ValueError('finite values required')
    a=np.abs(x)
    hi=np.searchsorted(levels,a,side='left').clip(0,len(levels)-1)
    lo=np.maximum(hi-1,0)
    dl,dh=a-levels[lo],levels[hi]-a
    chosen=np.where((dl<dh)|((dl==dh)&(lo%2==0)),lo,hi)
    return np.copysign(levels[chosen],x)


def nvfp4_round(x,*,block_size=16):
    """Eq25 E2M1 elements, unsigned E4M3 block scales, power-of-two group scale.

    One input matrix is one channel group of one head. No packed FP4 storage.
    Matrix max-absolute magnitude must be zero or in [2**-400, 2**400].
    """
    x=_matrix(x)
    if type(block_size)!=int or block_size<1 or x.shape[1]%block_size:raise ValueError('whole channel blocks required')
    maximum=float(np.abs(x).max())
    group_scale=1. if maximum==0 else 2.**math.ceil(math.log2(maximum/(6*448)))
    blocks=x.reshape(x.shape[0],-1,block_size)
    sigma=round_codebook(np.abs(blocks).max(-1)/(6*group_scale),E4M3)
    scale=group_scale*sigma
    normalized=np.divide(blocks,scale[:,:,None],out=np.zeros_like(blocks),where=scale[:,:,None]!=0)
    decoded=scale[:,:,None]*round_codebook(normalized,E2M1)
    return decoded.reshape(x.shape),{'group_scale':group_scale,'block_scales':sigma}


def hadamard(width,*,seed=42):
    if type(width)!=int or width<1 or width&(width-1):raise ValueError('power-of-two width required')
    h=np.ones((1,1))
    while len(h)<width:h=np.block([[h,h],[h,-h]])
    signs=np.random.default_rng(seed).choice([-1.,1.],size=width)
    return signs[:,None]*h/math.sqrt(width)


def principal_basis(q,k,*,rank,seed=42,sample_indices=None):
    """Eq6 raw ROTATED sample Gram, each normalized by its own trace.

    The caller supplies explicit stratified indices for mixed audio/text/video.
    With no strata, homogeneous tokens are uniformly sampled without replacement.
    """
    q,k=_matrix(q),_matrix(k)
    if q.shape!=k.shape or type(rank)!=int or rank<1 or rank>q.shape[1]:raise ValueError('aligned shapes and valid rank required')
    count=min(len(q),max(math.ceil(len(q)/256),2*rank))
    indices=np.random.default_rng(seed).choice(len(q),size=count,replace=False) if sample_indices is None else np.asarray(sample_indices)
    if indices.ndim!=1 or indices.dtype.kind not in 'iu' or not len(indices) or len(np.unique(indices))!=len(indices) or (indices<0).any() or (indices>=len(q)).any():
        raise ValueError('unique valid sampled row indices required')
    g=np.zeros((q.shape[1],q.shape[1]))
    for a in (q[indices],k[indices]):
        gram=_matmul(a.T,a)
        trace=float(np.trace(gram))
        if not math.isfinite(trace):raise ValueError('unrepresentable raw Gram trace')
        if trace>0:g+=gram/trace
    _,vectors=np.linalg.eigh(g)
    return vectors[:,-rank:],indices


def prepare(q,k,*,rank=16,seed=42,sample_indices=None):
    """Algorithm1 Q/K part including rotation and quantized extra channels."""
    q,k=_matrix(q),_matrix(k)
    if q.shape!=k.shape or q.shape[1]%16 or rank%16:raise ValueError('aligned Q/K and 16-channel base/extra groups required')
    h=hadamard(q.shape[1],seed=seed)
    qr,kr=_matmul(q,h),_matmul(k,h)
    b,indices=principal_basis(qr,kr,rank=rank,seed=seed,sample_indices=sample_indices)
    qhat,qscale=nvfp4_round(qr);khat,kscale=nvfp4_round(kr)
    dq,dk=qr-qhat,kr-khat
    qside,_=nvfp4_round(_matmul(dq,b));kprincipal,_=nvfp4_round(_matmul(khat,b))
    qprincipal,_=nvfp4_round(_matmul(qhat,b));kside,_=nvfp4_round(_matmul(dk,b))
    qe=np.concatenate([qhat,qside,qprincipal],axis=1)
    ke=np.concatenate([khat,kprincipal,kside],axis=1)
    return {'q_extended':qe,'k_extended':ke,'q_rotated':qr,'k_rotated':kr,'q_quantized':qhat,'k_quantized':khat,
            'basis':b,'sample_indices':indices,'q_scale':qscale,'k_scale':kscale,
            'q_side':_matmul(qside,kprincipal.T),'k_side':_matmul(qprincipal,kside.T)}


def compensated_attention(q,k,v,*,rank=16,seed=42):
    """Actual FP64 softmax/readout of the emulated compensated score matrix.

    Attention scale stays sqrt(ORIGINAL head width), not extended width.
    V/softmax are not quantized and no online-kernel rescaling is simulated.
    """
    p=prepare(q,k,rank=rank,seed=seed);v=_matrix(v)
    if len(v)!=len(p['k_extended']):raise ValueError('one V row per key required')
    scores=_matmul(p['q_extended'],p['k_extended'].T)/math.sqrt(p['q_rotated'].shape[1])
    probabilities=np.exp(scores-scores.max(axis=1,keepdims=True))
    probabilities/=probabilities.sum(axis=1,keepdims=True)
    return _matmul(probabilities,v),p


def diagnostic(seed:int,device='cpu'):
    if type(seed)!=int or seed<0 or device!='cpu':raise ValueError('nonnegative seed and CPU-only emulation required')
    rng=np.random.default_rng(seed)
    q=rng.normal(size=(64,32));k=rng.normal(size=(64,32));v=rng.normal(size=(64,8))
    out,p=compensated_attention(q,k,v,rank=16,seed=seed)
    qr,kr=p['q_rotated'],p['k_rotated'];qh,kh=p['q_quantized'],p['k_quantized']
    dq,dk=qr-qh,kr-kh
    extended=p['q_extended']@p['k_extended'].T
    explicit=qh@kh.T+p['q_side']+p['k_side']
    product_error=float(np.abs(extended-explicit).max())
    decomposition_error=float(np.abs(qr@kr.T-(qh@kh.T+dq@kh.T+qh@dk.T+dq@dk.T)).max())
    # At full rank BEFORE extra-channel rounding, only the second-order residual remains.
    b,_=principal_basis(qr,kr,rank=32,seed=seed)
    first_order=qh@kh.T+(dq@b)@(kh@b).T+(qh@b)@(dk@b).T
    remainder_error=float(np.abs(qr@kr.T-first_order-dq@dk.T).max())
    relative=lambda a:float(np.linalg.norm(a-qr@kr.T)/np.linalg.norm(qr@kr.T))
    return {'seed':seed,'device':device,'evaluation_tier':'l1_mechanism','diagnostic_only':True,
            'checks':{'extended_dot_is_two_sided_compensation':product_error<1e-11,
                      'exact_residual_decomposition':decomposition_error<1e-11,
                      'full_rank_drops_only_second_order_before_requantization':remainder_error<1e-11,
                      'basis_is_orthonormal':bool(np.allclose(p['basis'].T@p['basis'],np.eye(16),atol=1e-12)),
                      'small_sequence_sample_floor':len(p['sample_indices'])==32,
                      'real_softmax_output_finite':bool(np.isfinite(out).all())},
            'metrics':{'extended_product_max_abs_error':product_error,'residual_decomposition_max_abs_error':decomposition_error,
                       'full_rank_remainder_max_abs_error':remainder_error,'uncompensated_score_relative_error':relative(qh@kh.T),
                       'compensated_score_relative_error':relative(extended),'sampled_tokens':len(p['sample_indices']),
                       'original_channels':32,'extended_channels':64,'native_fp4_kernel_calls':0}}
