"""Actual teacher-generated, independently re-solved MBS trees and RLVR."""
from __future__ import annotations

import json
import hashlib
import math
import torch

from auto_research.post_training.oct10_checkpoint import verified_reward
from auto_research.post_training.proximal_checkpoint import problem_messages
from auto_research.post_training.oct13_common import (CostLedger,ExecutionFailure,evaluate,load_policy,
    load_split,policy_gradient_step,result_payload)
from .algorithm import MagicBeanStalk,Problem,verified_hard_seed


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
        self.response_audits=[]

    def record_response(self,response,*,role,input_gold_scope,**metadata):
        """Local train-only diagnostic trace; never copied into GPU receipts."""
        audit={"role":role,"input_gold_scope":input_gold_scope,
            "response_text":response.text,"response_token_ids":list(response.tokens),
            "response_text_sha256":hashlib.sha256(response.text.encode()).hexdigest(),
            "generated_tokens":len(response.tokens),"truncated":response.truncated,**metadata}
        self.response_audits.append(audit)
        return audit

    def verify(self,problem):
        key=(problem.question,problem.answer)
        if key in self.verified_cache:
            return self.verified_cache[key]
        # Independent solving receives question ONLY, not proposed answer/trace.
        for attempt in range(self.teacher_attempts):
            response=self.ledger.sample(self.teacher,problem_messages(problem.question),
                role="construction_verification",max_tokens=self.max_tokens)[0]
            audit=self.record_response(response,role="construction_verification",
                input_gold_scope="question-only-no-answer-or-trace",attempt=attempt+1,
                question_sha256=hashlib.sha256(problem.question.encode()).hexdigest(),verification_completed=False)
            accepted=not response.truncated and bool(verified_reward(response.text,problem.answer))
            audit.update(verification_completed=True,accepted=accepted,
                reject_reason=None if accepted else ("truncated_independent_solution" if response.truncated
                                                     else "incorrect_independent_solution"))
            if accepted:
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
        for index,policy in enumerate(policies):
            role="effectivity_student" if index==0 else "effectivity_teacher"
            responses=self.ledger.sample(policy,problem_messages(query),role=role,
                                          samples=self.rollouts,max_tokens=self.max_tokens)
            rewards=[0. if r.truncated else verified_reward(r.text,problem.answer) for r in responses]
            for response,reward in zip(responses,rewards):
                self.record_response(response,role=role,
                    input_gold_scope="child-worked-examples-only-no-parent-answer-or-trace" if worked_examples
                                     else "question-only-no-answer-or-trace",
                    question_sha256=hashlib.sha256(problem.question.encode()).hexdigest(),reward=reward,
                    worked_example_count=len(worked_examples))
            rates.append(sum(rewards)/len(rewards))
        return rates

    def teacher_json(self,instruction,context,*,operation="teacher_json"):
        response=self.ledger.sample(self.teacher,({"role":"user","content":instruction+"\n"+
            "Output JSON only, without prose or code fences.\n"+json.dumps(context,ensure_ascii=False)},),
            role="construction_teacher",max_tokens=self.max_tokens)[0]
        audit=self.record_response(response,role="construction_teacher",input_gold_scope="training-construction-context",
            operation=operation,parsing_completed=False)
        value=None if response.truncated else _json(response.text)
        audit.update(parsing_completed=True,parsed_json_kind=type(value).__name__,
            reject_reason="truncated_json_response" if response.truncated else ("no_json_value" if value is None else None))
        return value

    def propose_children(self,parent,negative):
        value=self.teacher_json(
            "Identify the parent's reasoning operations and dependencies. Produce exactly two easier, independent, "
            "self-contained subproblems that collectively teach these operations. Return a JSON array of objects "
            "with question, answer and trace. Avoid prior ineffective decompositions. "
            "Each child question must explicitly state every quantity, unit, time interval, relation and assumption "
            "used in its solution. It must be solvable in isolation without the parent, other children, or the "
            "answer/trace fields. Do not rely on facts stated only elsewhere. Give a complete step-by-step trace "
            "using only that question, and put exactly one concise numerical final answer in answer. "
            "Do not disclose the parent final answer or reproduce its complete plan.",
            {"parent":vars(parent),"ineffective_decompositions":[[vars(p) for p in group if p] for group in negative]},
            operation="propose_children")
        children=[p for item in value if (p:=_problem(item)) is not None][:3] if isinstance(value,list) else []
        self.response_audits[-1].update(proposed_problem_count=len(value) if isinstance(value,list) else 0,
            schema_valid_problem_count=len(children),schema_reject_reason=None if children else "no_schema_valid_child")
        return children

    def harder_leaf(self,leaf):
        value=self.teacher_json(
            "Generate a substantively NEW, harder, self-contained problem requiring the same core operations and more "
            "reasoning steps; not a paraphrase, context rewrite or numerical substitution. Return a JSON object "
            "with question, answer and trace, with exactly one verifiable final numerical answer.",vars(leaf),
            operation="harder_leaf")
        return _problem(value)

    def scaffold_safe(self,parent,children):
        value=self.teacher_json(
            "Check that every child is a DIFFERENT independent self-contained problem. Child questions and worked "
            "solutions must teach transferable operations, not state the parent's final answer or reproduce its "
            "complete solution/plan. Return JSON boolean scaffold_safe; reject direct answer or plan leakage.",
            {"parent":vars(parent),"children":[vars(p) for p in children]},operation="scaffold_safe")
        return isinstance(value,dict) and value.get("scaffold_safe") is True

    def compose(self,node,children):
        value=self.teacher_json(
            "Combine ALL synthetic children into a substantively new parent that mirrors the ORIGINAL logical "
            "dependency pattern and abstraction. Do not simplify. Return JSON with question, answer and trace.",
            {"original_parent":vars(node.problem),"original_children":[vars(n.problem) for n in node.children],
             "synthetic_children":[vars(p) for p in children]},operation="compose")
        return _problem(value)

    def blueprint_and_novelty(self,original,candidate):
        value=self.teacher_json(
            "Judge whether the new problem preserves essential reasoning operations/dependencies and is substantively "
            "novel, NOT just a paraphrase/context rewrite/numerical substitution. Return JSON booleans "
            "blueprint_preserved and substantive_novelty.",{"original":vars(original),"candidate":vars(candidate)},
            operation="blueprint_and_novelty")
        return isinstance(value,dict) and value.get("blueprint_preserved") is True and value.get("substantive_novelty") is True

    def target_outcomes(self,problem):
        responses=self.ledger.sample(self.student,problem_messages(problem.question),role="target_calibration",
                                      samples=self.rollouts,max_tokens=self.max_tokens)
        rewards=[0. if r.truncated else verified_reward(r.text,problem.answer) for r in responses]
        for response,reward in zip(responses,rewards):
            self.record_response(response,role="target_calibration",input_gold_scope="question-only-no-answer-or-trace",
                question_sha256=hashlib.sha256(problem.question.encode()).hexdigest(),reward=reward)
        return (rewards,[r.truncated for r in responses])


def construct_paired_hard_roots(train,backend,builder,*,hard_root_limit):
    """Train-only current-policy calibration, bounded trees, matched seed roots."""
    if type(hard_root_limit) is not int or hard_root_limit<1:
        raise ValueError("positive integer hard_root_limit required")
    selected,calibrations=[],[]
    for index,row in enumerate(train):
        root=Problem(row["question"],row["answer"],"")
        rewards,truncated=backend.target_outcomes(root)
        accepted=verified_hard_seed(rewards,truncated)
        calibrations.append({"training_index":index,"accepted":accepted,
            "root_question_sha256":hashlib.sha256(root.question.encode()).hexdigest(),
            "rewards":rewards,"truncated":truncated})
        if accepted:
            selected.append((index,root,(rewards,truncated)))
            if len(selected)==hard_root_limit:
                break
    synthetic,controls,paired_indices=[],[],[]
    for index,root,calibration in selected:
        candidate=builder.construct(root,calibration=calibration)
        if candidate is not None:
            synthetic.append(candidate)
            controls.append(root)
            paired_indices.append(index)
    return synthetic,controls,{"hard_root_limit":hard_root_limit,
        "calibrated_training_candidates":len(calibrations),"calibration_audits":calibrations,
        "verified_hard_roots_selected":len(selected),"tree_construction_attempts":len(selected),
        "selected_training_root_indices":[i for i,_,_ in selected],
        "paired_rl_root_indices":paired_indices,"method_and_control_use_same_root_pairs":True,
        "precalibration_reused_without_duplicate_sampling":True}


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
    root_selection=None
    control_problems=[Problem(r["question"],r["answer"],"") for r in train]
    try:
        if config.get("hard_root_limit") is not None:
            synthetic,control_problems,root_selection=construct_paired_hard_roots(
                train,backend,builder,hard_root_limit=config["hard_root_limit"])
        else:
            for row in train:
                problem=builder.construct(Problem(row["question"],row["answer"],""))
                if problem is not None:
                    synthetic.append(problem)
    except Exception as exc:
        raise ExecutionFailure("MBS construction interrupted; actual partial trace retained",
            {"error_type":type(exc).__name__,"construction_audits":builder.audit,
             "construction_response_audits":backend.response_audits,"cost":ledger.to_dict()}) from exc
    if not synthetic:
        raise ExecutionFailure("no actual effectivity-validated, novel, verified, target-Goldilocks MBS descendant",
                               {"construction_audits":builder.audit,"construction_response_audits":backend.response_audits,
                                "hard_root_selection":root_selection,
                                "cost":ledger.to_dict()})
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
    control_training=train_rl(control,control_problems,"seed_rlvr_control")
    control_metrics=evaluate(control,validation,ledger,max_tokens=max_tokens,seed=seed+10000)
    changed=before!=student.trainable_digest()
    if not changed:
        raise ExecutionFailure("MBS descendants survived construction but actual RLVR groups supplied no nonzero advantage",
                               {"training":training,"control_training":control_training,
                                "construction_audits":builder.audit,"hard_root_selection":root_selection,
                                "construction_response_audits":backend.response_audits,
                                "cost":ledger.to_dict()})
    return result_payload("magicbeanstalk",config,seed,split,student,ledger,baseline,after,training,
        parameters_changed=changed,teacher=teacher.provenance,construction_audits=builder.audit,
        construction_response_audits=backend.response_audits,
        hard_root_selection=root_selection,
        synthetic_problem_count=len(synthetic),control={"method":"seed-rlvr","training":control_training,"metrics":control_metrics},
        limitations=["Qwen2.5 and tiny train-only GSM8K replace proprietary teacher pools and original math/finance scale.",
                     "Independent re-solving and novelty/blueprint judging use actual teacher calls, not formal proof of synthetic labels.",
                     "Depth/breadth/retries are bounded; no finance re-grounding path is advertised.",
                     "Effectivity and final target-policy Goldilocks are separate measured gates; no gate is substituted by a heuristic.",
                     "All failed construction attempts, teacher calls and recalibration tokens count toward actual cost."])
