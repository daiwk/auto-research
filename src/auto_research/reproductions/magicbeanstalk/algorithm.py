"""MBS top-down effectivity and bottom-up calibrated synthesis.

Backends must perform real model calls and external verification. This module
never synthesizes targets by arithmetic substitution or reads evaluation gold.
"""
from __future__ import annotations

from dataclasses import dataclass,field
import hashlib


@dataclass(frozen=True)
class Problem:
    question:str
    answer:str
    trace:str


@dataclass
class Node:
    problem:Problem
    children:list["Node"]=field(default_factory=list)
    effectivity:list[dict]=field(default_factory=list)


def goldilocks(rewards,truncated):
    if len(rewards)<2 or len(rewards)!=len(truncated) or any(r not in (0,1) for r in rewards):
        raise ValueError("aligned actual binary outcomes and termination flags required")
    rate=sum(rewards)/len(rewards)
    return 0<rate<1 and any(r and not t for r,t in zip(rewards,truncated))


def verified_hard_seed(rewards,truncated):
    if (len(rewards)<2 or len(rewards)!=len(truncated) or any(r not in (0,1) for r in rewards)
            or any(not isinstance(flag,bool) for flag in truncated)):
        raise ValueError("aligned binary outcomes and actual boolean termination flags required")
    return not any(rewards) and not any(truncated)


class MagicBeanStalk:
    """Sections3.2-3.4; student pool is ordered weakest -> strongest."""
    def __init__(self,backend,*,depth=1,decomposition_retries=3,synthesis_retries=3):
        if min(depth,decomposition_retries,synthesis_retries)<1:
            raise ValueError("positive recursive construction budgets required")
        self.backend=backend
        self.depth=depth
        self.decomposition_retries=decomposition_retries
        self.synthesis_retries=synthesis_retries
        self.audit=[]

    def decompose(self,problem,depth=0):
        verified=self.backend.verify(problem)
        if verified is None:
            self.audit.append({"phase":"verify","accepted":False,"depth":depth,
                "reject_reason":"independent_verification_failed",
                "question_sha256":hashlib.sha256(problem.question.encode()).hexdigest()})
            return None
        node=Node(verified)
        if depth>=self.depth:
            return node
        baselines=self.backend.student_rates(verified,worked_examples=())
        zero=[i for i,rate in enumerate(baselines) if rate==0]
        if not zero:
            self.audit.append({"phase":"decomposition","accepted":False,"reason":"no empirical zero-success student"})
            return None
        # Strongest evaluated zero-success student is the last in this ordering.
        strongest_zero=max(zero)
        negative=[]
        for attempt in range(self.decomposition_retries):
            proposals=self.backend.propose_children(verified,negative)
            children=[self.backend.verify(p) for p in proposals]
            children=[p for p in children if p is not None]
            if len(children)<2:
                self.audit.append({"phase":"decomposition","attempt":attempt+1,"depth":depth,"accepted":False,
                    "reject_reason":"fewer_than_two_verified_children","proposed_children":len(proposals),
                    "verified_children":len(children)})
                negative.append(proposals)
                continue
            duplicate_or_leaking=len({child.question.strip() for child in children}) != len(children) or any(
                    child.question.strip()==verified.question.strip() or child.trace.strip()==verified.trace.strip()
                    for child in children)
            if duplicate_or_leaking or not self.backend.scaffold_safe(verified,children):
                self.audit.append({"phase":"scaffold-safety","accepted":False,"depth":depth,"attempt":attempt+1,
                    "reject_reason":"duplicate_or_parent_leaking_children" if duplicate_or_leaking else "unsafe_scaffold"})
                negative.append(proposals)
                continue
            conditioned=self.backend.student_rates(verified,worked_examples=children,
                                                    through_student=strongest_zero)
            effect=[{"student":i,"baseline":baselines[i],"conditioned":value}
                    for i,value in enumerate(conditioned)]
            effective=any(row["conditioned"]>row["baseline"] for row in effect)
            self.audit.append({"phase":"effectivity","attempt":attempt+1,"depth":depth,
                               "accepted":effective,"student_rates":effect,
                               "reject_reason":None if effective else "no_effectivity_improvement"})
            if not effective:
                negative.append(proposals)
                continue
            subtrees=[self.decompose(child,depth+1) for child in children]
            if any(child is None for child in subtrees):
                self.audit.append({"phase":"decomposition","attempt":attempt+1,"depth":depth,"accepted":False,
                    "reject_reason":"child_decomposition_failed"})
                negative.append(proposals)
                continue
            node.children=list(subtrees)
            node.effectivity=effect
            return node
        return None

    def synthesize(self,node):
        synthetic_children=[]
        for child in node.children:
            child_problem=self.synthesize(child)
            if child_problem is None:
                self.audit.append({"phase":"synthesis","accepted":False,"reject_reason":"child_synthesis_failed"})
                return None
            synthetic_children.append(child_problem)
        for attempt in range(self.synthesis_retries):
            candidate=(self.backend.compose(node,synthetic_children) if node.children
                       else self.backend.harder_leaf(node.problem))
            if candidate is None or candidate.question.strip()==node.problem.question.strip():
                self.audit.append({"phase":"synthesis","attempt":attempt+1,"accepted":False,
                    "reject_reason":"no_schema_valid_candidate" if candidate is None else "candidate_repeats_original_question"})
                continue
            verified=self.backend.verify(candidate)
            if verified is None or not self.backend.blueprint_and_novelty(node.problem,verified):
                self.audit.append({"phase":"synthesis","attempt":attempt+1,"accepted":False,
                    "reject_reason":"independent_verification_failed" if verified is None else "blueprint_or_novelty_rejected"})
                continue
            weakest=self.backend.student_rates(verified,worked_examples=(),through_student=0)[0]
            threshold=.625 if node.children else .8
            self.audit.append({"phase":"parent-synthesis" if node.children else "leaf-synthesis",
                               "attempt":attempt+1,"weakest_student_success":weakest,"threshold":threshold,
                               "accepted":weakest<=threshold,
                               "reject_reason":None if weakest<=threshold else "weakest_success_exceeds_threshold"})
            if weakest<=threshold:
                return verified
        return None

    def construct(self,seed,*,calibration=None):
        # A bounded caller may reuse its actual current-policy pre-calibration.
        # The original hard/termination gate is still enforced, never bypassed.
        seed_rewards,seed_truncated=(self.backend.target_outcomes(seed) if calibration is None else calibration)
        verified_hard=verified_hard_seed(seed_rewards,seed_truncated)
        audit={"phase":"seed-hardness-calibration","accepted":verified_hard,
               "rewards":seed_rewards,"truncated":seed_truncated}
        if calibration is not None:
            audit["actual_precalibration_reused_without_resampling"]=True
        self.audit.append(audit)
        if not verified_hard:
            return None
        tree=self.decompose(seed)
        if tree is None:
            return None
        synthetic=self.synthesize(tree)
        if synthetic is None:
            return None
        rewards,truncated=self.backend.target_outcomes(synthetic)
        accepted=goldilocks(rewards,truncated)
        self.audit.append({"phase":"target-policy-goldilocks","accepted":accepted,
                           "rewards":rewards,"truncated":truncated,
                           "reject_reason":None if accepted else "target_policy_not_goldilocks"})
        return synthetic if accepted else None
