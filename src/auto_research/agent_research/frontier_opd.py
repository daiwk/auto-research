"""Frontier-OPD Eqs.3--10 numerical selection and measured-bridge protocol.

External trajectories, state identities and teacher scores are required. No
environment replay, model, judge, reward, gold plan or OPD trainer is simulated.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/frontier-opd-a100-20261026.json"


def response_scores(student_logp: Tensor, teacher_logp: Tensor, mask: Tensor) -> tuple[Tensor, Tensor]:
    """Detached signed disagreement (Eq3), negative absolute gap (Eq8)."""
    if student_logp.ndim != 2 or min(student_logp.shape)<1 or not student_logp.is_floating_point():
        raise ValueError("nonempty floating [response,token] probabilities required")
    if teacher_logp.shape != student_logp.shape or not teacher_logp.is_floating_point() or mask.shape != student_logp.shape or mask.dtype != torch.bool:
        raise ValueError("aligned scores and Boolean mask required")
    if teacher_logp.device != student_logp.device or mask.device != student_logp.device or not bool(mask.any(1).all()):
        raise ValueError("same device and nonempty responses required")
    for values in (student_logp, teacher_logp):
        if not bool(torch.isfinite(values[mask]).all()) or bool((values[mask]>0).any()):
            raise ValueError("finite nonpositive active log probabilities required")
    dtype=torch.promote_types(student_logp.dtype,teacher_logp.dtype)
    if dtype in (torch.float16,torch.bfloat16):dtype=torch.float32
    gap=torch.where(mask,student_logp.detach().to(dtype),0.)-torch.where(mask,teacher_logp.detach().to(dtype),0.)
    return gap.sum(1)/mask.sum(1),-gap.abs().sum(1)/mask.sum(1)


@dataclass(frozen=True)
class Occurrence:
    trajectory: int
    turn: int
    node: str
    disagreement: float
    valid_actions: bool
    replayable_prefix: bool
    remaining_turns: int


@dataclass(frozen=True)
class Candidate:
    node: str
    score: float
    representative: Occurrence


def select_frontier(occurrences: list[Occurrence], *, budget: int, bridge_horizon: int = 1,
                    continuation_horizon: int = 3, min_score: float | None = None) -> list[Candidate]:
    """Trajectory means then node mean; one highest-gap replay per distinct node.

    Flags and normalized observation/action state keys come from the real
    collector. Keys do not replace retained histories. No reward/gold input.
    Equal scores follow collection order (trajectory, then turn).
    """
    if type(budget) is not int or budget<0 or type(bridge_horizon) is not int or bridge_horizon<1 or type(continuation_horizon) is not int or continuation_horizon<1:
        raise ValueError("integer nonnegative budget and positive horizons required")
    if min_score is not None and not math.isfinite(min_score):raise ValueError("finite threshold required")
    identities=set();groups={}
    for item in sorted(occurrences,key=lambda x:(x.trajectory,x.turn)):
        if type(item.trajectory) is not int or type(item.turn) is not int or min(item.trajectory,item.turn)<0:
            raise ValueError("nonnegative trajectory and turn identity required")
        identity=(item.trajectory,item.turn)
        if identity in identities:raise ValueError("duplicate occurrence identity")
        identities.add(identity)
        if type(item.valid_actions) is not bool or type(item.replayable_prefix) is not bool or type(item.remaining_turns) is not int or item.remaining_turns<0:
            raise ValueError("explicit collector validity and remaining-turn metadata required")
        eligible=(item.valid_actions and item.replayable_prefix and isinstance(item.node,str) and bool(item.node)
                  and math.isfinite(item.disagreement) and item.remaining_turns>=bridge_horizon+continuation_horizon)
        if eligible:groups.setdefault(item.node,[]).append(item)
    candidates=[]
    for node,visits in groups.items():
        by_trajectory={}
        for item in visits:by_trajectory.setdefault(item.trajectory,[]).append(item.disagreement)
        score=sum(sum(v)/len(v) for v in by_trajectory.values())/len(by_trajectory)
        if min_score is None or score>=min_score:
            # Python's max/sort preserve first occurrence on ties.
            representative=max(visits,key=lambda x:x.disagreement)
            candidates.append(Candidate(node,score,representative))
    return sorted(candidates,key=lambda x:-x.score)[:budget]


def accept_bridge(old_agreement: Tensor, new_agreement: Tensor, *, bridge_length: int,
                  continuation_horizon: int, replay_succeeded: bool, nonterminal_handoff: bool,
                  continuation_complete: bool, margin: float = 0.) -> tuple[bool, float | None]:
    """Eq9/10 on measured response scores from the SAME frozen policy pair.

    Each vector contains L_realized + H response means, including the teacher
    bridge, not only continuation. Invalid replay/handoff rejects. This does
    not establish task success or learning improvement, nor insert validation
    continuations into training; an external trainer must preserve that split.
    """
    if type(bridge_length) is not int or bridge_length<1 or type(continuation_horizon) is not int or continuation_horizon<1 or not math.isfinite(margin):
        raise ValueError("positive integer horizons and finite margin required")
    flags=(replay_succeeded,nonterminal_handoff,continuation_complete)
    if any(type(x) is not bool for x in flags):raise ValueError("explicit Boolean validity required")
    if not all(flags):return False,None
    n=bridge_length+continuation_horizon
    if old_agreement.shape != (n,) or new_agreement.shape != (n,) or old_agreement.device != new_agreement.device:
        return False,None
    if not old_agreement.is_floating_point() or not new_agreement.is_floating_point():raise ValueError("floating response agreements required")
    if not bool(torch.isfinite(old_agreement).all() & torch.isfinite(new_agreement).all()):return False,None
    if bool((old_agreement>0).any() | (new_agreement>0).any()):raise ValueError("negative absolute log-gap agreements required")
    gain=float(new_agreement.detach().mean()-old_agreement.detach().mean())
    return gain>=margin,gain


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    resolved=torch.device(device)
    if resolved.type not in ('cpu','cuda') or (resolved.type=='cuda' and not torch.cuda.is_available()):
        raise ValueError("diagnostic requires available CPU or real CUDA; no fallback")
    gen=torch.Generator(device=device).manual_seed(seed)
    student=-1-torch.rand(4,5,generator=gen,device=device,dtype=torch.float64)
    expected_signed=torch.tensor([.2,-.1,.3,-.4],device=device,dtype=torch.float64)
    teacher=student-expected_signed[:,None]
    mask=torch.tensor([[1,0,0,0,0],[1,1,0,0,0],[1,1,1,1,1],[1,1,1,0,0]],dtype=torch.bool,device=device)
    signed,agreement=response_scores(student,teacher,mask)
    items=[Occurrence(0,i,'loop',10.,True,True,8) for i in range(3)]
    items+=[Occurrence(1,0,'loop',0.,True,True,8),Occurrence(1,1,'other',6.,True,True,8)]
    candidates=select_frontier(items,budget=2)
    accepted,gain=accept_bridge(agreement,agreement,bridge_length=1,continuation_horizon=3,
        replay_succeeded=True,nonterminal_handoff=True,continuation_complete=True)
    invalid_accepted,_=accept_bridge(agreement,agreement,bridge_length=1,continuation_horizon=3,
        replay_succeeded=False,nonterminal_handoff=True,continuation_complete=True)
    return {"seed":seed,"diagnostic_only":True,"component":"frontier_opd_measured_selection_and_acceptance",
      "metrics":{"trajectory_balanced_loop_score":candidates[1].score,"selected_nodes":len(candidates),
                 "signed_score_reference_error":float((signed-expected_signed).abs().max()),
                 "agreement_reference_error":float((agreement+expected_signed.abs()).abs().max()),"matched_window_gain":gain},
      "checks":{"trajectory_balanced_not_visit_weighted":candidates[1].score==5.,
                "distinct_nodes_ranked":candidates[0].node=='other' and len({c.node for c in candidates})==2,
                "replay_representative_tie_order":candidates[1].representative.turn==0,
                "signed_not_absolute_ranking":int(signed.argmax())!=int((-agreement).argmax()),
                "equal_turn_not_token_weighting":bool(torch.allclose(agreement,-expected_signed.abs())),
                "zero_margin_equality_accepted":accepted,"frozen_scores":not signed.requires_grad,
                "invalid_replay_rejected":not invalid_accepted}}
