"""Actual teacher-generated, independently re-solved MBS trees and RLVR."""
from __future__ import annotations

import json
import math
import torch

from auto_research.post_training.oct10_checkpoint import verified_reward
from auto_research.post_training.proximal_checkpoint import problem_messages
from auto_research.post_training.oct13_common import (CostLedger,ExecutionFailure,evaluate,load_policy,
    load_split,policy_gradient_step,result_payload)
from .algorithm import MagicBeanStalk,Problem


def _json(text):
    decoder=json.JSONDecoder()
    values=[]
    for index,character in enumerate(text):
        if character not in "[{":
            continue
        try:
            value,_=decoder.raw_decode(text[index:])
            values.append(value)
        except json.JSONDecodeError:
            continue
    return values[0] if values else None


def _problem(value):
    if not isinstance(value,dict) or not all(isinstance(value.get(k),str) and value[k].strip()
                                             for k in ("question","trace")):
        return None
    answer=value.get("answer")
    if type(answer) in (int,float):
        if isinstance(answer,float) and not math.isfinite(answer):
            return None
        answer=str(answer)
    if not isinstance(answer,str) or not answer.strip():
        return None
    return Problem(value["question"],answer,value["trace"])


class CheckpointConstruction:
    def __init__(self,teacher,student,ledger,*,max_tokens=768,rollouts=4,teacher_attempts=2):
        self.teacher,self.student,self.ledger=teacher,student,ledger
        self.max_tokens,self.rollouts,self.teacher_attempts=max_tokens,rollouts,teacher_attempts
        self.students=(student,teacher)  # scaled ordered same-family pool
        self.verified_cache={}

    def verify(self,problem):
        key=(problem.question,problem.answer)
        if key in self.verified_cache:
            return self.verified_cache[key]
        # Independent solving receives question ONLY, not proposed answer/trace.
        for _ in range(self.teacher_attempts):
            response=self.ledger.sample(self.teacher,problem_messages(problem.question),
                role="construction_verification",max_tokens=self.max_tokens)[0]
            if not response.truncated and verified_reward(response.text,problem.answer):
                verified=Problem(problem.question,problem.answer,response.text)
                self.verified_cache[key]=verified
                return verified
        return None

    def student_rates(self,problem,*,worked_examples,through_student=None):
        examples="\n\n".join("Worked example: "+p.question+"\n"+p.trace for p in worked_examples)
        # The scaffold never includes the PARENT answer or verified parent trace.
        query=(examples+"\n\nNow solve the separate parent problem:\n"+problem.question
               if examples else problem.question)
        policies=self.students if through_student is None else self.students[:through_student+1]
        rates=[]
        for policy in policies:
            responses=self.ledger.sample(policy,problem_messages(query),role="effectivity_student",
                                          samples=self.rollouts,max_tokens=self.max_tokens)
            rewards=[0. if r.truncated else verified_reward(r.text,problem.answer) for r in responses]
            rates.append(sum(rewards)/len(rewards))
        return rates

    def teacher_json(self,instruction,context):
        response=self.ledger.sample(self.teacher,({"role":"user","content":instruction+"\n"+
            "Output JSON only, without prose or code fences.\n"+json.dumps(context,ensure_ascii=False)},),
            role="construction_teacher",max_tokens=self.max_tokens)[0]
        return None if response.truncated else _json(response.text)

    def propose_children(self,parent,negative):
        value=self.teacher_json(
            "Identify the parent's reasoning operations and dependencies. Produce exactly two easier, independent, "
            "self-contained subproblems that collectively teach these operations. Return a JSON array of objects "
            "with question, answer and trace. Avoid prior ineffective decompositions.",
            {"parent":vars(parent),"ineffective_decompositions":[[vars(p) for p in group if p] for group in negative]})
        return [p for item in value if (p:=_problem(item)) is not None][:3] if isinstance(value,list) else []

    def harder_leaf(self,leaf):
        value=self.teacher_json(
            "Generate a substantively NEW, harder, self-contained problem requiring the same core operations and more "
            "reasoning steps; not a paraphrase, context rewrite or numerical substitution. Return a JSON object "
            "with question, answer and trace, with exactly one verifiable final numerical answer.",vars(leaf))
        return _problem(value)

    def scaffold_safe(self,parent,children):
        value=self.teacher_json(
            "Check that every child is a DIFFERENT independent self-contained problem. Child questions and worked "
            "solutions must teach transferable operations, not state the parent's final answer or reproduce its "
            "complete solution/plan. Return JSON boolean scaffold_safe; reject direct answer or plan leakage.",
            {"parent":vars(parent),"children":[vars(p) for p in children]})
        return isinstance(value,dict) and value.get("scaffold_safe") is True

    def compose(self,node,children):
        value=self.teacher_json(
            "Combine ALL synthetic children into a substantively new parent that mirrors the ORIGINAL logical "
            "dependency pattern and abstraction. Do not simplify. Return JSON with question, answer and trace.",
            {"original_parent":vars(node.problem),"original_children":[vars(n.problem) for n in node.children],
             "synthetic_children":[vars(p) for p in children]})
        return _problem(value)

    def blueprint_and_novelty(self,original,candidate):
        value=self.teacher_json(
            "Judge whether the new problem preserves essential reasoning operations/dependencies and is substantively "
            "novel, NOT just a paraphrase/context rewrite/numerical substitution. Return JSON booleans "
            "blueprint_preserved and substantive_novelty.",{"original":vars(original),"candidate":vars(candidate)})
        return isinstance(value,dict) and value.get("blueprint_preserved") is True and value.get("substantive_novelty") is True

    def target_outcomes(self,problem):
        responses=self.ledger.sample(self.student,problem_messages(problem.question),role="target_calibration",
                                      samples=self.rollouts,max_tokens=self.max_tokens)
        return ([0. if r.truncated else verified_reward(r.text,problem.answer) for r in responses],
                [r.truncated for r in responses])


def run(config,*,seed=42):
    train,validation,split=load_split(config)
    ledger,student=CostLedger(),load_policy(config,seed=seed)
    teacher=load_policy(config,role="teacher",seed=seed)
    max_tokens=int(config.get("max_tokens",512))
    group=int(config.get("group",4))
    if min(max_tokens,group-1,int(config.get("steps",2)),int(config.get("teacher_attempts",2)))<1:
        raise ValueError("positive construction/RLVR budget and >=2 real group outcomes required")
    backend=CheckpointConstruction(teacher,student,ledger,max_tokens=max_tokens,rollouts=group,
                                  teacher_attempts=int(config.get("teacher_attempts",2)))
    builder=MagicBeanStalk(backend,depth=int(config.get("depth",1)),
                          decomposition_retries=int(config.get("decomposition_retries",2)),
                          synthesis_retries=int(config.get("synthesis_retries",2)))
    baseline=evaluate(student,validation,ledger,max_tokens=max_tokens,seed=seed+10000)
    synthetic=[]
    for row in train:
        problem=builder.construct(Problem(row["question"],row["answer"],""))
        if problem is not None:
            synthetic.append(problem)
    if not synthetic:
        raise ExecutionFailure("no actual effectivity-validated, novel, verified, target-Goldilocks MBS descendant",
                               {"construction_audits":builder.audit,"cost":ledger.to_dict()})
    torch.manual_seed(seed)
    student.prepare_lora(learning_rate=float(config.get("learning_rate",1e-5)))
    before=student.trainable_digest()
    steps=int(config.get("steps",2))
    def train_rl(policy,problems,role):
        history=[]
        for step in range(steps):
            problem=problems[step%len(problems)]
            messages=problem_messages(problem.question)
            responses=ledger.sample(policy,messages,role=role,samples=group,max_tokens=max_tokens)
            rewards=[0. if r.truncated else verified_reward(r.text,problem.answer) for r in responses]
            audit=policy_gradient_step(policy,list(zip([messages]*group,responses)),rewards,ledger)
            history.append({"step":step+1,**audit})
        return history
    training=train_rl(student,synthetic,"mbs_rlvr")
    after=evaluate(student,validation,ledger,max_tokens=max_tokens,seed=seed+10000)
    control=load_policy(config,seed=seed)
    torch.manual_seed(seed)
    control.prepare_lora(learning_rate=float(config.get("learning_rate",1e-5)))
    control_training=train_rl(control,[Problem(r["question"],r["answer"],"") for r in train],"seed_rlvr_control")
    control_metrics=evaluate(control,validation,ledger,max_tokens=max_tokens,seed=seed+10000)
    changed=before!=student.trainable_digest()
    if not changed:
        raise ExecutionFailure("MBS descendants survived construction but actual RLVR groups supplied no nonzero advantage",
                               {"training":training,"construction_audits":builder.audit,"cost":ledger.to_dict()})
    return result_payload("magicbeanstalk",config,seed,split,student,ledger,baseline,after,training,
        parameters_changed=changed,teacher=teacher.provenance,construction_audits=builder.audit,
        synthetic_problem_count=len(synthetic),control={"method":"seed-rlvr","training":control_training,"metrics":control_metrics},
        limitations=["Qwen2.5 and tiny train-only GSM8K replace proprietary teacher pools and original math/finance scale.",
                     "Independent re-solving and novelty/blueprint judging use actual teacher calls, not formal proof of synthetic labels.",
                     "Depth/breadth/retries are bounded; no finance re-grounding path is advertised.",
                     "Effectivity and final target-policy Goldilocks are separate measured gates; no gate is substituted by a heuristic.",
                     "All failed construction attempts, teacher calls and recalibration tokens count toward actual cost."])
