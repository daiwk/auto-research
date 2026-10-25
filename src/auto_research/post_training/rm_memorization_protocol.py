"""What do RMs Memorize? Eq.1--2 score aggregation and user-leakage guard.

External model runs and their frozen inclusion manifests are mandatory inputs.
No RM is replaced with a feature heuristic, no retraining is claimed. We do NOT
implement Appendix B's underspecified cooccurrence-search algorithm.
"""
from __future__ import annotations
import torch
from torch import Tensor


def counterfactual_memorization(reward_margins: Tensor, train_membership: Tensor,
                                user_ids: Tensor, *, train_runs: int = 20,
                                test_runs: int = 5) -> dict[str, Tensor]:
    """[pair,run] Bradley-Terry margins and inclusion, paired by stable run IDs.

    All pairs of the same user must have identical train/test membership in each
    run. Default 20+5 follows the 25-run paper; the 3B check used 8+2 explicitly.
    TM and TG are averages of sigmoid margins, NOT sigmoid of mean margins.
    """
    if type(train_runs) is not int or type(test_runs) is not int or min(train_runs,test_runs) < 1:
        raise ValueError("positive integer train/test run counts required")
    if reward_margins.ndim != 2 or reward_margins.shape[0] < 1 or reward_margins.shape[1] != train_runs+test_runs or not reward_margins.is_floating_point():
        raise ValueError("complete floating [pair,run] margin matrix required")
    if not bool(torch.isfinite(reward_margins).all()):
        raise ValueError("all observed run margins must be finite")
    if train_membership.shape != reward_margins.shape or train_membership.dtype != torch.bool:
        raise ValueError("aligned Boolean training-membership manifest required")
    if user_ids.shape != (reward_margins.shape[0],) or user_ids.dtype != torch.long:
        raise ValueError("one int64 user ID per preference pair required")
    if any(t.device != reward_margins.device for t in (train_membership,user_ids)):
        raise ValueError("protocol inputs must share device")
    if not bool((train_membership.sum(1) == train_runs).all()):
        raise ValueError("each pair needs exactly the declared in/out counts")
    for user in torch.unique(user_ids):
        rows = train_membership[user_ids == user]
        if not bool((rows == rows[0]).all()):
            raise ValueError("user-level leakage: a user's pairs disagree on inclusion")
    dtype = torch.float32 if reward_margins.dtype in (torch.float16,torch.bfloat16) else reward_margins.dtype
    probabilities = reward_margins.detach().to(dtype).sigmoid()
    tm = torch.where(train_membership,probabilities,0.).sum(1)/train_runs
    tg = torch.where(~train_membership,probabilities,0.).sum(1)/test_runs
    return {"training_memorization":tm,"testing_generalization":tg,"counterfactual_memorization":tm-tg}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    generator=torch.Generator(device=device).manual_seed(seed)
    users=torch.tensor([0,0,1,1],device=device)
    membership=torch.ones(4,25,dtype=torch.bool,device=device)
    membership[:2,:5]=False
    membership[2:,5:10]=False
    margins=torch.randn(4,25,dtype=torch.float64,device=device,generator=generator).requires_grad_()
    result=counterfactual_memorization(margins,membership,users)
    probability=margins.detach().sigmoid()
    expected_tm=torch.stack([probability[i][membership[i]].mean() for i in range(4)])
    expected_tg=torch.stack([probability[i][~membership[i]].mean() for i in range(4)])
    error=max(float((result["training_memorization"]-expected_tm).abs().max()),float((result["testing_generalization"]-expected_tg).abs().max()))
    leak=membership.clone(); leak[1,0]=True;leak[1,6]=False
    rejected=False
    try: counterfactual_memorization(margins,leak,users)
    except ValueError: rejected=True
    permutation=torch.randperm(25,generator=generator,device=device)
    permuted=counterfactual_memorization(margins[:,permutation],membership[:,permutation],users)
    return {"seed":seed,"diagnostic_only":True,"metrics": {
        "formula_max_abs_error":error,"pairs":4,"observed_runs":25,
        "mean_counterfactual_memorization":float(result["counterfactual_memorization"].mean()),"model_calls":0},"checks": {
        "conditional_probability_means_match":error < 1e-12,
        "cm_is_tm_minus_tg":bool(torch.equal(result["counterfactual_memorization"],result["training_memorization"]-result["testing_generalization"])),
        "user_level_leakage_rejected":rejected,
        "joint_run_permutation_invariant":bool(torch.allclose(permuted["counterfactual_memorization"],result["counterfactual_memorization"])),
        "frozen_external_model_scores":not result["counterfactual_memorization"].requires_grad and margins.grad is None}}
