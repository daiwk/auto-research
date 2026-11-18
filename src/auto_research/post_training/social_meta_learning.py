"""SML v1 successful-dialogue student-only SFT and Q-priming probability.

The teacher, rollouts, Q-generation, online GRPO and trained LLM are absent.
These are real differentiable training operators, not conversational capability.
"""
import math

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/social-meta-learning-a100-20261113.json"


def q_priming_probability(turn_index: int, *, incorrect: bool) -> float:
    """Eq.4, with an explicit caller-supplied nonnegative exponent t."""
    if type(turn_index) is not int or turn_index < 0 or type(incorrect) is not bool:
        raise ValueError("nonnegative turn exponent and explicit incorrect boolean required")
    return .75 ** turn_index if incorrect else 0.


def successful_student_loss(logits, targets, student_mask, successful):
    """Offline SML: mean CE only on student tokens in successful dialogues.

    Token-mean reduction is an explicit local convention; the paper specifies
    successful-dialogue filtering/student turns, not a unique batching reduction.
    Teacher token targets and unsuccessful trajectories receive zero gradient.
    """
    import torch
    import torch.nn.functional as F
    if not all(isinstance(x, torch.Tensor) for x in (logits, targets, student_mask, successful)):
        raise ValueError("actual tensors required")
    if logits.ndim != 3 or targets.shape != logits.shape[:2] or student_mask.shape != targets.shape or successful.shape != (logits.shape[0],):
        raise ValueError("expected [dialogue,token,vocab], [dialogue,token], [dialogue] shapes")
    if logits.shape[-1] < 2 or not logits.is_floating_point() or targets.dtype != torch.long or student_mask.dtype != torch.bool or successful.dtype != torch.bool:
        raise ValueError("floating logits, long targets and boolean masks required")
    if any(x.device != logits.device for x in (targets, student_mask, successful)) or not torch.isfinite(logits).all():
        raise ValueError("finite tensors on one actual device required")
    selected = student_mask & successful[:, None]
    if not selected.any():
        raise ValueError("no successful student training tokens")
    labels = targets[selected]
    if (labels < 0).any() or (labels >= logits.shape[-1]).any():
        raise ValueError("selected student target outside vocabulary")
    return F.cross_entropy(logits[selected], labels, reduction="mean")


def diagnostic(seed: int, device: str = "cpu") -> dict:
    import torch
    if type(seed) is not int or device not in ("cpu", "cuda"):
        raise ValueError("integer seed and explicit cpu/cuda required")
    torch.manual_seed(seed)
    logits = torch.tensor([[[2.,0.],[0.,2.],[2.,0.]], [[0.,2.],[2.,0.],[0.,2.]]], device=device, requires_grad=True)
    targets = torch.tensor([[0,1,0],[1,0,1]], device=device)
    mask = torch.tensor([[True,False,True],[True,True,True]], device=device)
    success = torch.tensor([True,False], device=device)
    loss = successful_student_loss(logits, targets, mask, success)
    loss.backward()
    checks = {"real_tensor_device":logits.device.type == device,
              "student_tokens_receive_gradient":bool(logits.grad[0,0].abs().sum() > 0),
              "teacher_tokens_excluded":bool((logits.grad[0,1] == 0).all()),
              "failed_dialogue_excluded":bool((logits.grad[1] == 0).all()),
              "exact_successful_ce":math.isclose(loss.item(), math.log1p(math.exp(-2)), rel_tol=1e-5),
              "q_priming_failed_only":q_priming_probability(2, incorrect=True) == .5625 and q_priming_probability(2, incorrect=False) == 0.}
    return {"seed":seed,"diagnostic_only":True,"evaluation_tier":"l1_mechanism","checks":checks,
            "execution_device":logits.device.type,"metrics":{"student_sft_loss":loss.item(),"selected_student_tokens":2,"q_probability_t2":.5625}}
