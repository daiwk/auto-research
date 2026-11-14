"""Instruct-to-Act v1 replay-segment labels and BC/stop training losses.

No Dreamer/RSSM, VLM annotation, policy, planner or environment bridge is supplied.
"""
import math
from numbers import Real

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/instruct-to-act-a100-20261113.json"


def interval_labels(length: int, intervals):
    """Inclusive zero-based, non-overlapping intervals; completion only at end.

    Annotations refer to one already logged episode. Instruction text/embeddings
    must come from a real external annotator, not fabricated here.
    """
    if type(length) is not int or length < 1:
        raise ValueError("positive logged-episode length required")
    annotated, completion = [False] * length, [False] * length
    for interval in intervals:
        if not isinstance(interval, (tuple, list)) or len(interval) != 2:
            raise ValueError("explicit inclusive interval pairs required")
        start, end = interval
        if any(type(x) is not int for x in interval) or not 0 <= start <= end < length:
            raise ValueError("interval outside one logged episode")
        if any(annotated[start:end+1]):
            raise ValueError("annotation intervals must not overlap")
        annotated[start:end+1] = [True] * (end-start+1)
        completion[end] = True
    return tuple(annotated), tuple(completion)


def instruction_losses(action_log_probs, stop_logits, annotated, completion, valid, *, bc_weight=1.):
    """Section3.4 sum BC on annotated actions + sum stop BCE on valid steps.

    Unannotated valid steps have completion=false and remain stop negatives.
    Padding is excluded by valid. Model/value/actor losses are NOT replaced.
    """
    import torch
    import torch.nn.functional as F
    tensors = (action_log_probs, stop_logits, annotated, completion, valid)
    if not all(isinstance(x, torch.Tensor) for x in tensors) or action_log_probs.ndim != 2 or any(x.shape != action_log_probs.shape for x in tensors):
        raise ValueError("matching actual [episode,step] tensors required")
    if not action_log_probs.is_floating_point() or not stop_logits.is_floating_point() or any(x.dtype != torch.bool for x in (annotated, completion, valid)):
        raise ValueError("floating log-probabilities/logits and boolean masks required")
    if any(x.device != action_log_probs.device for x in tensors) or not torch.isfinite(action_log_probs).all() or not torch.isfinite(stop_logits).all():
        raise ValueError("finite tensors on one actual device required")
    if (action_log_probs > 0).any() or (annotated & ~valid).any() or (completion & ~annotated).any() or not valid.any():
        raise ValueError("valid masks, log probabilities<=0, and annotated-only completion required")
    if isinstance(bc_weight, bool) or not isinstance(bc_weight, Real) or not math.isfinite(bc_weight) or bc_weight < 0:
        raise ValueError("finite nonnegative BC weight required")
    bc = -bc_weight * action_log_probs[annotated].sum()
    stop = F.binary_cross_entropy_with_logits(stop_logits[valid], completion[valid].to(stop_logits.dtype), reduction="sum")
    return {"bc":bc,"stop":stop,"total":bc+stop}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    import torch
    if type(seed) is not int or device not in ("cpu", "cuda"):
        raise ValueError("integer seed and explicit cpu/cuda required")
    torch.manual_seed(seed)
    labels, ends = interval_labels(4, [(0,1)])
    logits = torch.tensor([[[1.,0.],[1.,0.],[1.,0.],[1.,0.]]], device=device, requires_grad=True)
    action_log_probs = torch.log_softmax(logits, dim=-1)[...,0]
    stop_logits = torch.zeros((1,4), device=device, requires_grad=True)
    annotated = torch.tensor([labels], device=device)
    completion = torch.tensor([ends], device=device)
    valid = torch.tensor([[True,True,True,False]], device=device)
    losses = instruction_losses(action_log_probs, stop_logits, annotated, completion, valid, bc_weight=.5)
    losses["total"].backward()
    checks = {"actual_tensor_device":logits.device.type == device,
              "completion_only_interval_end":ends == (False,True,False,False),
              "bc_not_unannotated_or_padding":bool((logits.grad[0,2:] == 0).all()),
              "unannotated_stop_negative":bool(stop_logits.grad[0,2] > 0),
              "end_stop_positive":bool(stop_logits.grad[0,1] < 0),
              "padding_stop_zero":bool(stop_logits.grad[0,3] == 0),
              "exact_sum_reduction":math.isclose(losses["stop"].item(), 3*math.log(2), rel_tol=1e-5)}
    return {"seed":seed,"diagnostic_only":True,"evaluation_tier":"l1_mechanism","execution_device":logits.device.type,
            "checks":checks,"metrics":{"bc_loss":losses["bc"].item(),"stop_loss":losses["stop"].item(),"total_loss":losses["total"].item(),"annotated_steps":2}}
