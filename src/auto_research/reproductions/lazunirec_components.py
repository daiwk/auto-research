"""Fixed LazUnirec v1 Eq7/10--17 bounded differentiable components.

Not the complete five-layer model, condition router, data pipeline or serving
system. Explicit tensors are caller-provided; no user logs or gold policies.
"""
import math

import torch
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


def _tensor(value, ndim=None):
    if (not isinstance(value, torch.Tensor) or not value.is_floating_point()
            or not value.numel() or (ndim is not None and value.ndim != ndim)
            or not torch.isfinite(value).all()):
        raise ValueError("nonempty finite floating tensor with expected rank required")
    return value


def _matched(*values):
    for value in values:
        _tensor(value)
    if any(x.device != values[0].device or x.dtype != values[0].dtype for x in values):
        raise ValueError("matched device and dtype required")


def task_lora_projection(tokens, shared, low_a, low_b, tasks):
    """Eq7, torch linear convention. -1=history/trigger, 0=retrieval,1=ranking.

    Each task can use a different rank; `low_a` and `low_b` are pairs. This
    function does not invent attention masking, normalization or serving KV.
    """
    _tensor(tokens,2)
    _tensor(shared,2)
    if (not isinstance(low_a,(tuple,list)) or not isinstance(low_b,(tuple,list))
            or len(low_a)!=2 or len(low_b)!=2):
        raise ValueError("two task-private LoRA factor pairs required")
    _matched(tokens,shared,*low_a,*low_b)
    if (tasks.dtype!=torch.long or tasks.device!=tokens.device or tasks.shape!=(tokens.shape[0],)
            or not torch.isin(tasks,torch.tensor([-1,0,1],device=tasks.device)).all()
            or tokens.shape[1]!=shared.shape[1]):
        raise ValueError("aligned task identifiers and shared projection required")
    base=F.linear(tokens,shared)
    result=base
    for task,(a,b) in enumerate(zip(low_a,low_b,strict=True)):
        if a.ndim!=2 or b.ndim!=2 or a.shape[1]!=tokens.shape[1] or b.shape!=(shared.shape[0],a.shape[0]):
            raise ValueError("compatible task-private LoRA dimensions required")
        result=torch.where((tasks==task)[:,None],base+F.linear(F.linear(tokens,a),b),result)
    return _tensor(result,2)


def sparse_expert_mix(private_output, shared_outputs, scores, *, k=2):
    """Eq10/11: private output plus top-k renormalized SHARED outputs.

    Scores are supplied by a condition router, which is outside this slice;
    adding a task-private expert is not averaging it into the shared softmax.
    """
    _tensor(private_output,2)
    _tensor(shared_outputs,3)
    _tensor(scores,2)
    _matched(private_output,shared_outputs,scores)
    if (type(k) is not int or not 1<=k<=scores.shape[1]
            or shared_outputs.shape!=(scores.shape[0],scores.shape[1],private_output.shape[1])
            or private_output.shape[0]!=scores.shape[0]):
        raise ValueError("aligned expert tensors and valid top-k required")
    chosen_scores,indices=scores.topk(k,dim=1)
    weights=chosen_scores.softmax(dim=1)
    chosen=shared_outputs.gather(1,indices[:,:,None].expand(-1,-1,shared_outputs.shape[2]))
    output=private_output+(weights[:,:,None]*chosen).sum(1)
    return _tensor(output,2),weights,indices


def gradient_evidence(first_moment,second_moment,*,epsilon=1e-8,maximum=100.):
    """Eq12; explicit stored EMA moments. Epsilon/cap are local choices."""
    _matched(first_moment,second_moment)
    if (first_moment.shape!=second_moment.shape or (second_moment<0).any()
            or not math.isfinite(epsilon) or not math.isfinite(maximum)
            or epsilon<=0 or maximum<=0):
        raise ValueError("matched EMA shapes and positive finite stability constants required")
    variance=(second_moment.detach()-first_moment.detach().square()).clamp_min(0)
    evidence=(variance+epsilon).rsqrt().clamp_max(maximum)
    return _tensor(evidence),_tensor(variance)


class DirectionEMA:
    """Explicit zero-initialized, no-bias-correction reference for normalized g.

    The paper gives decay.99, but not a unique initialization or normalization
    norm. Here L2 normalization and zero initialization are declared choices;
    observations are already-probed gradients, not a full training scheduler.
    """
    def __init__(self,*,decay=.99):
        if not math.isfinite(decay) or not 0<=decay<1:
            raise ValueError("EMA decay in [0,1) required")
        self.decay=decay
        self.states={}

    def observe(self,scenario,task,gradient):
        _tensor(gradient,1)
        if not isinstance(scenario,str) or not scenario or task not in (0,1):
            raise ValueError("explicit scenario and retrieval/ranking task required")
        norm=gradient.detach().norm()
        if not torch.isfinite(norm) or norm==0:
            raise ValueError("a nonzero finite gradient direction is required")
        direction=gradient.detach()/norm
        key=(scenario,task)
        m,v=self.states.get(key,(torch.zeros_like(direction),torch.zeros_like(direction)))
        _matched(m,v,direction)
        if m.shape!=direction.shape:
            raise ValueError("probe dimensions changed within a scenario/task")
        m=self.decay*m+(1-self.decay)*direction
        v=self.decay*v+(1-self.decay)*direction.square()
        self.states[key]=(m.detach(),v.detach())
        return gradient_evidence(m,v)[0]


def weighted_task_loss(losses,evidence,*,clip=(.8,1.2)):
    """Eq13/14 plus §4.1.4 clipping AFTER batch reliability normalization.

    `evidence` is a sequence of per-observation probed vectors, aligned with
    task/scenario losses in this mini-batch. Clipping does not renormalize the
    batch again; its final mean can differ from one. Weights are detached.
    """
    _tensor(losses,1)
    if not isinstance(evidence,(list,tuple)) or len(evidence)!=len(losses):
        raise ValueError("one evidence vector per loss required")
    reliability=[]
    for value in evidence:
        _matched(losses,value)
        if (value<=0).any():
            raise ValueError("strictly positive evidence required")
        mean=value.detach().mean()
        reliability.append(1-1/(1+mean))
    r=torch.stack(reliability)
    if (r<=0).any() or not torch.isfinite(r).all():
        raise ValueError("reliability is numerically unresolved")
    weights=r/r.mean()
    if clip is not None:
        if (not isinstance(clip,(tuple,list)) or len(clip)!=2
                or not all(math.isfinite(x) for x in clip) or not 0<clip[0]<=clip[1]):
            raise ValueError("positive ordered finite clipping bounds required")
        weights=weights.clamp(*clip)
    weights=weights.detach()
    return _tensor((weights*losses).sum()),weights


def ranking_to_retrieval_kd(interests,items,interest_probabilities,teacher_logits,*,
                            ranking_temperature=.5,retrieval_temperature=.01):
    """Eq15--17 request-local max(pi * inner-product), teacher->student KL.

    Inputs represent one aligned request group per batch item. Padding/masks
    and interest-probability generation are not guessed; pass genuine lists
    with the same number of candidates in a batch, never cross-request pools.
    """
    _tensor(interests,3)
    _tensor(items,3)
    _tensor(interest_probabilities,2)
    _tensor(teacher_logits,2)
    _matched(interests,items,interest_probabilities,teacher_logits)
    if (interests.shape[0]!=items.shape[0] or interests.shape[2]!=items.shape[2]
            or interest_probabilities.shape!=interests.shape[:2]
            or teacher_logits.shape!=items.shape[:2]
            or (interest_probabilities<0).any()
            or not torch.allclose(interest_probabilities.sum(1),torch.ones_like(interest_probabilities[:,0]),atol=1e-6,rtol=1e-6)
            or not all(math.isfinite(t) and t>0 for t in (ranking_temperature,retrieval_temperature))):
        raise ValueError("aligned request tensors, normalized interest probabilities and positive temperatures required")
    scores=(interest_probabilities[:,:,None]*(interests@items.transpose(1,2))).max(dim=1).values
    student_log=F.log_softmax(scores/retrieval_temperature,dim=1)
    teacher_log=F.log_softmax(teacher_logits.detach()/ranking_temperature,dim=1)
    loss=F.kl_div(student_log,teacher_log,log_target=True,reduction="none").sum(1).mean()
    return _tensor(loss),_tensor(scores,2)


def diagnostic(seed=42,device="cpu"):
    if type(seed) is not int or device not in ("cpu","cuda"):
        raise ValueError("integer seed and CPU/CUDA device required")
    gen=torch.Generator().manual_seed(seed)
    def rand(*shape,grad=False):
        return torch.randn(*shape,generator=gen,dtype=torch.float64).to(device).requires_grad_(grad)
    x,w=rand(4,5),rand(3,5,grad=True)
    a=(rand(2,5,grad=True),rand(3,5,grad=True))
    b=(rand(3,2,grad=True),rand(3,3,grad=True))
    tasks=torch.tensor([-1,0,1,-1],device=device)
    projected=task_lora_projection(x,w,a,b,tasks)
    history_ok=torch.equal(projected[tasks==-1],F.linear(x,w)[tasks==-1])
    projected[tasks==0].square().sum().backward()
    private_isolation=all(torch.count_nonzero(v.grad)==0 for v in (a[1],b[1]))
    p,shared=rand(2,3,grad=True),rand(2,4,3,grad=True)
    routing=torch.tensor([[4.,2.,1.,0.],[0.,1.,2.,4.]],device=device,dtype=torch.float64,requires_grad=True)
    mixed,weights,indices=sparse_expert_mix(p,shared,routing)
    mixed.square().sum().backward()
    selection=torch.zeros_like(routing,dtype=torch.bool).scatter(1,indices,True)
    no_unselected=torch.count_nonzero(shared.grad[~selection])==0
    direction=torch.tensor([1.,0.],device=device,dtype=torch.float64)
    stable,variable=DirectionEMA(decay=.8),DirectionEMA(decay=.8)
    for step in range(50):
        e_stable=stable.observe("s",0,direction)
        e_variable=variable.observe("s",0,direction*((-1)**step))
    loss_inputs=torch.tensor([2.,3.],device=device,dtype=torch.float64,requires_grad=True)
    total,task_weights=weighted_task_loss(loss_inputs,[e_stable,e_variable])
    total.backward()
    interests,items=rand(2,3,4,grad=True),rand(2,5,4,grad=True)
    pi=rand(2,3).softmax(1).detach().requires_grad_(True)
    teacher=rand(2,5,grad=True)
    kd,_=ranking_to_retrieval_kd(interests,items,pi,teacher)
    kd.backward()
    checks={"history_uses_shared_projection_only":bool(history_ok),
        "task_private_gradients_do_not_cross":bool(private_isolation),
        "unselected_shared_experts_receive_zero_gradient":bool(no_unselected),
        "selected_shared_weights_sum_to_one":bool(torch.allclose(weights.sum(1),torch.ones_like(weights[:,0]))),
        "stable_direction_gets_higher_reliability":bool(e_stable.mean()>e_variable.mean()),
        "reliability_weights_detached_and_loss_gradient_correct":bool(not task_weights.requires_grad and torch.allclose(loss_inputs.grad,task_weights)),
        "ranking_teacher_is_detached":teacher.grad is None,
        "retrieval_interests_and_probabilities_train":bool(interests.grad.abs().sum()>0 and pi.grad.abs().sum()>0)}
    return {"seed":seed,"diagnostic_only":True,"evaluation_tier":"l1_mechanism","checks":checks,
        "metrics":{"synthetic_kd_loss":float(kd.item()),"stable_evidence_mean":float(e_stable.mean().item()),
                   "fluctuating_evidence_mean":float(e_variable.mean().item()),"clipped_task_weight_mean":float(task_weights.mean().item()),
                   "retrieval_gradient_norm":float(interests.grad.norm().item())}}
