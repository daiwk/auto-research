"""MART-GRPO external event mapping and original-denominator masked Eq15.

No event-localization VLM, robot simulator, rollout policy or martingale
unbiasedness is supplied by this independent L1 numerical component.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/mart-grpo-a100-20261026.json"


@dataclass(frozen=True)
class Event:
    episode_id: str
    outcome: str
    error_type: str
    interval: tuple[int,int] | None
    recovery: str


def boundary_from_event(event: Event, *, episode_id: str, executed_chunks: int) -> int:
    """Eq14 for an externally localized FAILED training rollout.

    Caller must invoke its frozen event model on the completed executed rollout,
    never infer boundaries from gold plans or feed events into evaluated actors.
    Invalid schema/identity raises; valid uncertain semantics keep full feedback.
    Success rollouts bypass event inference in the external training loop.
    """
    if type(executed_chunks) is not int or executed_chunks<1:raise ValueError("positive executed chunk count required")
    if not isinstance(event,Event) or not isinstance(episode_id,str) or not episode_id or event.episode_id!=episode_id:
        raise ValueError("event/episode identity mismatch")
    if event.outcome not in ('failure','success','uncertain') or event.recovery not in ('none','observed','uncertain') or not isinstance(event.error_type,str) or not event.error_type.strip():
        raise ValueError("malformed externally validated event schema")
    if event.interval is not None:
        if not isinstance(event.interval,tuple) or len(event.interval)!=2 or any(type(i) is not int for i in event.interval):raise ValueError("two integer interval endpoints required")
        lower,upper=event.interval
        if not 0<=lower<=upper<executed_chunks:raise ValueError("event interval outside executed rollout")
    localized=(event.outcome=='failure' and event.error_type.lower() not in ('none','unknown','uncertain','no clear error')
               and event.interval is not None and event.recovery=='none')
    return event.interval[1] if localized else executed_chunks-1


def feedback_mask(rewards: Tensor, boundaries: Tensor, chunk_ids: Tensor, valid: Tensor) -> Tensor:
    """Eq2: successful rows unchanged; failed rows retain chunks <= B inclusive."""
    if chunk_ids.ndim!=2 or min(chunk_ids.shape)<1 or chunk_ids.dtype!=torch.long or valid.shape!=chunk_ids.shape or valid.dtype!=torch.bool:
        raise ValueError("aligned [rollout,token] chunk ids and Boolean original token mask required")
    n=chunk_ids.shape[0]
    if rewards.shape!=(n,) or boundaries.shape!=(n,) or boundaries.dtype!=torch.long:
        raise ValueError("one binary reward and int64 boundary per rollout required")
    if any(t.device!=chunk_ids.device for t in (valid,rewards,boundaries)) or not bool(valid.any(1).all()):raise ValueError("same device and nonempty original responses required")
    if not bool(torch.isfinite(rewards).all()) or not bool(((rewards==0)|(rewards==1)).all()):raise ValueError("binary terminal rewards required")
    if bool((chunk_ids[valid]<0).any()):raise ValueError("nonnegative active chunk ids required")
    last=torch.where(valid,chunk_ids,-1).max(1).values
    failed=rewards.detach()==0
    if bool(((boundaries[failed]<-1)|(boundaries[failed]>last[failed])).any()):raise ValueError("failure boundary outside executed chunks")
    return (valid & ((rewards.detach()==1)[:,None] | (chunk_ids<=boundaries[:,None]))).detach()


def mart_grpo_loss(current_logp: Tensor, old_logp: Tensor, advantages: Tensor,
                   feedback: Tensor, original_valid: Tensor, *, epsilon_minus: float=.2,
                   epsilon_plus: float=.28) -> Tensor:
    """Negative Eq15, fixed mask/advantages, ORIGINAL valid-token denominator.

    Advantages are externally computed over the FULL mixed-outcome rollout
    groups (sample std, epsilon=1e-6 in Appendix D.2). The event model never
    changes rewards, group membership, trajectory normalization or rollout end.
    """
    if not math.isfinite(epsilon_minus) or not 0<epsilon_minus<1 or not math.isfinite(epsilon_plus) or epsilon_plus<=0:
        raise ValueError("valid asymmetric clipping bounds required")
    if current_logp.ndim!=2 or min(current_logp.shape)<1 or not current_logp.is_floating_point() or old_logp.shape!=current_logp.shape or not old_logp.is_floating_point():raise ValueError("aligned floating [rollout,token] log probabilities required")
    if advantages.shape!=current_logp.shape[:1] or not advantages.is_floating_point():raise ValueError("one floating full-group advantage per rollout required")
    if feedback.shape!=current_logp.shape or original_valid.shape!=current_logp.shape or feedback.dtype!=torch.bool or original_valid.dtype!=torch.bool:raise ValueError("aligned Boolean masks required")
    if any(t.device!=current_logp.device for t in (old_logp,advantages,feedback,original_valid)):raise ValueError("one device required")
    if not bool(original_valid.any(1).all()) or bool((feedback & ~original_valid).any()):raise ValueError("nonempty original responses and feedback subset required")
    if not bool(torch.isfinite(advantages).all()):raise ValueError("finite full-group advantages required")
    for p in (current_logp,old_logp):
        if not bool(torch.isfinite(p[original_valid]).all()) or bool((p[original_valid]>0).any()):raise ValueError("finite nonpositive original response log probabilities required")
    dtype=torch.promote_types(current_logp.dtype,old_logp.dtype)
    if dtype in (torch.float16,torch.bfloat16):dtype=torch.float32
    advantage=advantages.detach().to(dtype)[:,None]
    active=feedback & (advantage!=0)
    log_ratio=torch.where(active,current_logp.to(dtype),0.)-torch.where(active,old_logp.detach().to(dtype),0.)
    clipped=torch.where(advantage>=0,log_ratio.clamp_max(math.log1p(epsilon_plus)),log_ratio.clamp_min(math.log1p(-epsilon_minus)))
    objective=torch.where(active,clipped.exp()*advantage,0.)
    if not bool(torch.isfinite(objective).all()):raise ValueError("importance objective not representable")
    return -(objective.sum(1)/original_valid.sum(1)).mean()


def diagnostic(seed: int=42, device: str='cpu') -> dict:
    resolved=torch.device(device)
    if resolved.type not in ('cpu','cuda') or (resolved.type=='cuda' and not torch.cuda.is_available()):
        raise ValueError("diagnostic requires available CPU or real CUDA; no fallback")
    gen=torch.Generator(device=device).manual_seed(seed)
    logits=torch.randn(2,4,3,generator=gen,device=device,dtype=torch.float64,requires_grad=True)
    current=logits.log_softmax(-1)[...,0]
    old=current.detach().clone().requires_grad_()
    advantage=torch.tensor([1.,-1.],device=device,dtype=torch.float64,requires_grad=True)
    valid=torch.ones(2,4,dtype=torch.bool,device=device)
    chunks=torch.arange(4,device=device).expand(2,-1)
    boundary=boundary_from_event(Event('failed','failure','drop',(1,2),'none'),episode_id='failed',executed_chunks=4)
    feedback=feedback_mask(torch.tensor([1.,0.],device=device),torch.tensor([3,boundary],device=device),chunks,valid)
    loss=mart_grpo_loss(current,old,advantage,feedback,valid)
    ratio=current.exp()/old.detach().exp()
    a=advantage.detach()[:,None]*feedback
    reference=-torch.minimum(ratio*a,ratio.clamp(.8,1.28)*a).sum(1).div(4).mean()
    ref_grad=torch.autograd.grad(reference,logits,retain_graph=True)[0]
    loss.backward()
    error=float((loss.detach()-reference.detach()).abs())
    grad_error=float((logits.grad-ref_grad).abs().max())
    return {"seed":seed,"diagnostic_only":True,"component":"mart_grpo_external_event_mask_original_denominator_loss",
      "metrics":{"masked_loss":float(loss.detach()),"reference_error":error,"gradient_reference_error":grad_error,
                 "gradient_norm":float(logits.grad.norm()),"retained_failure_fraction":float(feedback[1].sum()/valid[1].sum())},
      "checks":{"original_denominator_reference":error<1e-12,"gradient_matches_reference":grad_error<1e-12,
                "inclusive_upper_event_boundary":boundary==2 and bool(feedback[1,:3].all()) and not bool(feedback[1,3]),
                "success_feedback_preserved":bool(feedback[0].all()),"failure_suffix_zero_gradient":bool((logits.grad[1,3]==0).all()),
                "old_policy_and_advantage_detached":old.grad is None and advantage.grad is None,
                "recovered_event_full_feedback":boundary_from_event(Event('failed','failure','drop',(1,2),'observed'),episode_id='failed',executed_chunks=4)==3}}
