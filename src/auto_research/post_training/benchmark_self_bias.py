"""When LLMs Benchmark Themselves Eq.1 relative self-ranking protocol only.

No LLM-generated test set, judge, translation model or absolute accuracy claim.
The three evaluation conditions must be measured SEPARATELY by the caller.
"""
from __future__ import annotations
import torch
from torch import Tensor


def per_segment_ranks(scores: Tensor, *, higher_is_better: bool,
                       tie_policy: str) -> Tensor:
    """[segment,target,benchmark-role] -> rank1 is best, each role separately.

    Average ties are an explicit local convention; paper does not publish its
    tie handling. Callers may instead supply already measured ranks to self_bias.
    """
    if scores.ndim != 3 or scores.shape[0] < 1 or scores.shape[1] != scores.shape[2] or scores.shape[1] < 2 or not scores.is_floating_point() or not bool(torch.isfinite(scores).all()):
        raise ValueError("finite nonempty square target/benchmark-role scores required")
    if type(higher_is_better) is not bool or tie_policy != "average":
        raise ValueError("explicit direction and local average tie policy required")
    values=scores.detach().to(torch.float64)
    difference=values[:,None,:,:]-values[:,:,None,:]
    better=(difference > 0) if higher_is_better else (difference < 0)
    tied=difference == 0
    return 1 + better.sum(2).to(values.dtype) + .5*(tied.sum(2)-1)


def self_bias(rankings: Tensor) -> Tensor:
    """Eq.1: mean self rank minus leave-self-out peer mean; negative=favored."""
    if rankings.ndim != 3 or rankings.shape[0] < 1 or rankings.shape[1] != rankings.shape[2] or rankings.shape[1] < 2 or not rankings.is_floating_point():
        raise ValueError("nonempty floating [segment,target,benchmark-role] ranks required")
    m=rankings.shape[1]
    if not bool(torch.isfinite(rankings).all()) or bool(((rankings<1)|(rankings>m)).any()):
        raise ValueError("finite ranks must lie in [1,number of models]")
    average=rankings.detach().to(torch.float64).mean(0)
    own=average.diagonal()
    peers=(average.sum(1)-own)/(m-1)
    return own-peers


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    generator=torch.Generator(device=device).manual_seed(seed)
    scores=torch.rand(7,3,3,dtype=torch.float64,device=device,generator=generator)
    idx=torch.arange(3,device=device); scores[:,idx,idx]+=2.
    ranks=per_segment_ranks(scores,higher_is_better=True,tie_policy="average")
    result=self_bias(ranks)
    reference=torch.stack([ranks[:,i,i].mean()-torch.stack([ranks[:,i,j].mean() for j in range(3) if j != i]).mean() for i in range(3)])
    perm=torch.tensor([2,0,1],device=device)
    reordered=self_bias(ranks[:,perm][:,:,perm])
    transformed=per_segment_ranks(3*scores+7,higher_is_better=True,tie_policy="average")
    tied=per_segment_ranks(torch.ones(1,3,3,device=device),higher_is_better=True,tie_policy="average")
    error=float((result-reference).abs().max())
    return {"seed":seed,"diagnostic_only":True,"metrics": {
        "formula_max_abs_error":error,"mean_relative_self_bias":float(result.mean()),
        "segments":7,"models":3,"model_calls":0},"checks": {
        "leave_self_out_formula_matches":error<1e-12,
        "negative_means_self_preference":bool((result<0).all()),
        "model_role_joint_permutation_equivariant":bool(torch.allclose(reordered,result[perm])),
        "positive_score_affine_invariant":bool(torch.equal(transformed,ranks)),
        "explicit_average_ties":bool((tied==2.).all()),
        "metricx_direction_explicit":bool(torch.equal(per_segment_ranks(-scores,higher_is_better=False,tie_policy="average"),ranks)),
        "not_absolute_quality_estimate":bool((self_bias(tied)==0).all())}}
