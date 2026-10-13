#!/usr/bin/env python3
"""Bounded train-only SynthSelf/UPTURN diagnosis, never whole-method evidence."""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import math
from pathlib import Path
import signal
import time

import torch

from auto_research.post_training.oct10_checkpoint import verified_reward
from auto_research.post_training.oct13_common import CostLedger, causal_response_features, load_policy, sample_prefix
from auto_research.post_training.proximal_checkpoint import problem_messages
from auto_research.reproductions.progressive_contraction.algorithm import paragraph_prefixes
from auto_research.reproductions.synthself.algorithm import (
    complete_response_tokens, naturally_complete_response, rewrite_messages, select_aligner, validate_aligner,
)
from auto_research.reproductions.upturn.algorithm import (
    CorrectnessGate, PositionHead, boxed_token_position, position_loss, remaining_response_budget,
)
from auto_research.reproductions.upturn.checkpoint import intervention_prefix_tokens

MANIFEST_SHA="c0b9b2424d9b497e4b7f6c0188ac0c0a9235bf151a046d559fb181f44e10bcbd"
CAPS={"synthself":{"train_examples":8,"max_tokens":512},
      "upturn":{"train_examples":8,"group":4,"max_tokens":768,"gate_epochs":20,
                "steps":2,"cuts":4,"suffixes":2,"max_cuts":16}}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_runner_binding(source_root,contract,*,runner_path=None):
    actual=Path(__file__ if runner_path is None else runner_path).resolve()
    expected=(source_root/"scripts/diagnose_oct14_post_training.py").resolve()
    if actual!=expected or contract["source_file_sha256"].get("scripts/diagnose_oct14_post_training.py")!=digest(actual):
        raise ValueError("executed diagnostic runner must be inside and hash-bound by the approved frozen source root")


def strict_finite_evidence(evidence):
    """Preserve nonfinite metric locations as FAILED diagnostics, never NaN JSON."""
    paths=[]
    def clean(value,path):
        if isinstance(value,float) and not math.isfinite(value):
            paths.append({"json_path":path,"value_class":"nan" if math.isnan(value) else "positive-infinity" if value>0 else "negative-infinity"})
            return None
        if isinstance(value,dict):
            return {key:clean(item,path+"."+key) for key,item in value.items()}
        if isinstance(value,(list,tuple)):
            return [clean(item,path+"["+str(index)+"]") for index,item in enumerate(value)]
        return value
    result=clean(evidence,"$")
    if paths or evidence.get("nonfinite_gradient_detected"):
        result.update(diagnosis_status="diagnostic-failed-nonfinite-output",diagnostic_outputs_usable=False,
            nonfinite_metric_paths=paths+evidence.get("nonfinite_gradient_paths",[]))
    else:
        result["diagnostic_outputs_usable"]=result.get("diagnosis_status")!="diagnostic-execution-failed"
    return result


def validate_inputs(source_root,config,contract,audit,method,*,manifest_sha256=MANIFEST_SHA):
    """Read manifest and exact train bytes ONLY; validation bytes are forbidden."""
    if (audit.get("source_commit")!=contract["source_commit"] or not audit.get("source_hashes_verified")
            or audit.get("cuda_initialized") is not False or audit.get("model_instantiated") is not False
            or audit.get("source_file_sha256")!=contract["source_file_sha256"]
            or audit.get("execution_config_sha256")!=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()):
        raise ValueError("exact preverified CPU source/config audit required")
    for relative,expected in contract["source_file_sha256"].items():
        if digest(source_root/relative)!=expected:
            raise ValueError("frozen source mismatch: "+relative)
    c={**config["shared"],**config["methods"][method]}
    if any(c.get(k)!=v for k,v in CAPS[method].items()):
        raise ValueError("diagnosis fixed caps cannot be enlarged or silently changed")
    manifest=Path(c["split_manifest"])
    if digest(manifest)!=manifest_sha256:
        raise ValueError("predeclared split manifest SHA mismatch")
    record=json.loads(manifest.read_text())
    verified=audit.get("public_train_only_holdout",{})
    if (record.get("source_split")!="train" or record.get("test_opened") is not False
            or record.get("source_revision")!=c["dataset_revision"] or not verified.get("verified")
            or verified.get("test_read") is not False
            or record["partition_sha256"]!=verified["partition_sha256"]):
        raise ValueError("exact preverified training-only source manifest required")
    content=Path(c["train_path"]).read_bytes()
    if hashlib.sha256(content).hexdigest()!=record["partition_sha256"]["train"]:
        raise ValueError("complete train file SHA mismatch")
    rows=[json.loads(line) for line in content.splitlines() if line.strip()]
    if (len(rows)!=record["counts"]["train"] or len(rows)<8
            or any(not isinstance(r.get("question"),str) or not isinstance(r.get("answer"),str) for r in rows)):
        raise ValueError("real public train rows required")
    return c,rows[:8],{"source_revision":record["source_revision"],"split_manifest_sha256":manifest_sha256,
        "train_file_sha256":record["partition_sha256"]["train"],"verified_full_train_count":len(rows),
        "selected_training_prefix":8,"validation_content_read":False,"test_content_read":False}


def ensure_frozen(*policies):
    if any(p.requires_grad for policy in policies for p in policy.model.parameters()):
        raise ValueError("diagnosis must keep every backbone frozen; no LoRA allowed")


def diagnose_synthself(config,train,ledger,evidence,*,seed=42):
    if len(train)!=8 or seed!=42:
        raise ValueError("diagnosis pins the original eight training rows and seed42")
    student=load_policy(config,seed=seed)
    aligner=load_policy(config,role="teacher",seed=seed)
    own=load_policy(config,seed=seed)
    ensure_frozen(student,aligner,own)
    if student.vocabulary_sha256!=aligner.vocabulary_sha256:
        raise ValueError("exact teacher/student vocabulary required")
    validate_aligner(config["student_id"],config["teacher_id"],
        sum(p.numel() for p in student.model.parameters()),sum(p.numel() for p in aligner.model.parameters()))
    eos=student.tokenizer.eos_token_id
    measurements=evidence.setdefault("training_rewrite_audits",[])
    for index,row in enumerate(train):
        # This is the explicit TRAINING construction teacher role, not evaluated policy.
        messages=rewrite_messages(row["question"],row["answer"])
        response=ledger.sample(aligner,messages,role="offline_aligner",max_tokens=512,sample=False)[0]
        self_response=ledger.sample(own,messages,role="construction_self_rewrite",max_tokens=512,sample=False)[0]
        complete=naturally_complete_response(response.tokens,truncated=response.truncated,eos_token_id=eos)
        self_complete=naturally_complete_response(self_response.tokens,truncated=self_response.truncated,eos_token_id=eos)
        gold_original=tuple(student.tokenizer(row["answer"],add_special_tokens=False).input_ids)
        gold=complete_response_tokens(gold_original,eos_token_id=eos)
        rewrite=complete_response_tokens(response.tokens,eos_token_id=eos) if complete else response.tokens
        with torch.no_grad():
            gold_nll=float(-ledger.score(student,problem_messages(row["question"]),gold,role="gold_sequence_nll").sum())
            rewrite_nll=float(-ledger.score(student,problem_messages(row["question"]),rewrite,role="rewrite_sequence_or_partial_nll").sum())
        measurements.append({"training_row":index,"rewrite_truncated":response.truncated,
            "rewrite_natural_completion":complete,"rewrite_native_eos_count":response.tokens.count(eos),
            "rewrite_canonical_eos_appended":False,"rewrite_tokens":len(response.tokens),
            "rewrite_scored_tokens":len(rewrite),"rewrite_nll_scope":"complete_sequence" if complete else "actual_partial_diagnostic_only",
            "gold_original_tokens":len(gold_original),"gold_scored_tokens":len(gold),
            "gold_canonical_eos_appended":eos not in gold_original,"gold_scored_eos_count":gold.count(eos),
            "gold_sequence_nll":gold_nll,"rewrite_sequence_or_partial_nll":rewrite_nll,
            "rewrite_quality":verified_reward(response.text,row["answer"]) if complete else 0.,
            "self_truncated":self_response.truncated,"self_natural_completion":self_complete,
            "self_quality":verified_reward(self_response.text,row["answer"]) if self_complete else 0.})
    complete=all(x["rewrite_natural_completion"] for x in measurements)
    mean=lambda key:sum(x[key] for x in measurements)/len(measurements)
    selection=select_aligner([{"id":config["teacher_id"],"nll":mean("rewrite_sequence_or_partial_nll"),
        "quality":mean("rewrite_quality")}],gold_nll=mean("gold_sequence_nll"),self_quality=mean("self_quality")) if complete else None
    evidence.update(checkpoint={"student":student.provenance,"teacher":aligner.provenance},
        gold_access_roles={"offline_aligner":"train-only rewrite construction teacher",
            "construction_self_rewrite":"train-only construction reference control",
            "student":"external NLL targets only; no student generation or SFT executed"},
        empirical_aligner_constraints={"all_naturally_complete":complete,"selection_blocked_by_incomplete_outputs":not complete,
            "nll_reduction":"full response sequence SUM with exactly one EOS, never token mean",
            "gold_sequence_nll":mean("gold_sequence_nll"),
            "rewrite_sequence_nll":mean("rewrite_sequence_or_partial_nll") if complete else None,
            "diagnostic_actual_rewrite_or_partial_nll":mean("rewrite_sequence_or_partial_nll"),
            "aligner_quality":mean("rewrite_quality"),"self_quality":mean("self_quality"),"strict_eq6_satisfied":selection is not None},
        diagnosis_status="selection-signal-observed" if selection else "selection-blocked-or-strict-eq6-failed",
        sft_executed=False,lora_updates=0,backbone_parameters_frozen=True)


def diagnose_upturn(config,train,ledger,evidence,*,seed=42):
    if len(train)!=8 or seed!=42:
        raise ValueError("diagnosis pins the original eight training rows and seed42")
    encoder=load_policy(config,seed=seed)
    reasoner=load_policy(config,role="teacher",seed=seed)
    ensure_frozen(encoder,reasoner)
    if encoder.vocabulary_sha256!=reasoner.vocabulary_sha256:
        raise ValueError("exact reasoner/encoder vocabulary required")
    hidden=encoder.model.config.hidden_size
    position=PositionHead(hidden).to(encoder.device)
    gate=CorrectnessGate(hidden).to(encoder.device)
    pos_optimizer=torch.optim.AdamW(position.parameters(),lr=1e-3,weight_decay=0)
    gate_optimizer=torch.optim.AdamW(gate.parameters(),lr=1e-3,weight_decay=0)
    gate_train,calibration,failed=[],[],[]
    audits=evidence.setdefault("training_rollout_audits",[])
    for row_index,row in enumerate(train):
        messages=problem_messages("Write reasoning paragraphs separated by blank lines.\n"+row["question"])
        responses=ledger.sample(reasoner,messages,role="frozen_reasoner_training",samples=4,max_tokens=768)
        for response_index,response in enumerate(responses):
            prompt=reasoner.prompt_ids(messages)
            ledger.encoder_calls+=1
            ledger.encoded_input_tokens+=prompt.shape[1]+len(response.tokens)
            features=causal_response_features(encoder,messages,response.tokens,prompt_token_ids=prompt)
            correctness=0. if response.truncated else verified_reward(response.text,row["answer"])
            box=boxed_token_position(response.tokens,encoder.tokenizer)
            if box is not None:
                (calibration if row_index>=6 else gate_train).append((features[box],correctness))
            cuts=[c for c in paragraph_prefixes(response.tokens,tokenizer=reasoner.tokenizer,limit=16) if c<768]
            eligible=not correctness and len(cuts)>=2
            audits.append({"training_row":row_index,"response_index":response_index,"correctness":correctness,
                "truncated":response.truncated,"response_tokens":len(response.tokens),"boxed_answer_detected":box is not None,
                "paragraph_cut_indices":cuts,"paragraph_cut_count":len(cuts),"eligible_for_position":eligible})
            if eligible:
                failed.append((row,messages,response,features,cuts))
    evidence.update(checkpoint={"encoder":encoder.provenance,"reasoner":reasoner.provenance},
        gold_access_roles={"reasoner":"none in generation","encoder":"none in feature input",
            "gate_and_position":"external train verifier labels only, never gold text"},
        gate_training_cases=len(gate_train),gate_calibration_cases=len(calibration),eligible_failed_rollouts=len(failed),
        paragraph_boundary_protocol="decoded-character-boundaries-to-original-token-prefix-v1",lora_updates=0,
        backbone_parameters_frozen=True)
    if not gate_train or not calibration or not failed:
        evidence["diagnosis_status"]="insufficient-gate-data-or-eligible-rollouts"
        return
    inputs=torch.stack([x[0] for x in gate_train])
    labels=torch.tensor([x[1] for x in gate_train],device=encoder.device)
    history=evidence.setdefault("gate_training_bce",[])
    for _ in range(20):
        gate_optimizer.zero_grad(set_to_none=True)
        loss=torch.nn.functional.binary_cross_entropy_with_logits(gate(inputs),labels)
        loss.backward()
        gate_optimizer.step()
        history.append(float(loss.detach()))
    cal_inputs=torch.stack([x[0] for x in calibration])
    cal_labels=torch.tensor([x[1] for x in calibration],device=encoder.device)
    with torch.no_grad():
        temperatures=(.5,1.,1.38,2.)
        logits=gate(cal_inputs)
        scores=[float(torch.nn.functional.binary_cross_entropy_with_logits(logits/t,cal_labels)) for t in temperatures]
    evidence["gate_calibration_temperature"]=temperatures[min(range(4),key=lambda i:scores[i])]
    evidence["gate_training_classes"]=sorted(set(labels.tolist()))
    training=evidence.setdefault("position_training",[])
    for step in range(2):
        row,messages,response,features,cuts=failed[step%len(failed)]
        candidates=features[torch.tensor([cut-1 for cut in cuts],device=encoder.device)]
        with torch.no_grad():
            old_logits=position(candidates)
            selected=torch.multinomial(old_logits.softmax(-1),min(4,len(cuts)),replacement=False).tolist()
            old=old_logits.log_softmax(-1)[selected].detach()
        rewards=[]
        for index in selected:
            cut=cuts[index]
            prefix=intervention_prefix_tokens(reasoner,messages,response.tokens[:cut])
            revised=sample_prefix(reasoner,messages,prefix,ledger,role="position_rescue_training",samples=2,
                                  max_tokens=remaining_response_budget(768,cut))
            rewards.append(sum(0. if r.truncated else verified_reward(r.text,row["answer"]) for r in revised)/2)
        pos_optimizer.zero_grad(set_to_none=True)
        loss,audit=position_loss(position(candidates),selected,old,rewards)
        loss.backward()
        try:
            norm=torch.nn.utils.clip_grad_norm_(position.parameters(),1.,error_if_nonfinite=True)
        except RuntimeError as exc:
            if ("non-finite" in str(exc).lower() or "nonfinite" in str(exc).lower()
                    or any(p.grad is not None and not torch.isfinite(p.grad).all() for p in position.parameters())):
                evidence.update(nonfinite_gradient_detected=True,
                    nonfinite_gradient_paths=[{"json_path":"$.position_training["+str(step)+"].gradients",
                        "value_class":"nonfinite-gradient-or-norm"}])
            raise
        if float(norm)>0:
            pos_optimizer.step()
        training.append({"step":step+1,"cuts":[cuts[i] for i in selected],"loss":float(loss.detach()),
            "gradient_l2_norm":float(norm),"optimizer_update_executed":float(norm)>0,**audit})
        if not audit["nonzero_rescue_advantage"]:
            break  # retain the entropy-only update; do not invent a rescue signal or expand budget
    evidence["position_informative_groups"]=sum(x["nonzero_rescue_advantage"] for x in training)
    evidence["diagnosis_status"]="rescue-signal-observed" if evidence["position_informative_groups"] else "no-rescue-signal"


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method",choices=tuple(CAPS),required=True)
    parser.add_argument("--config",type=Path,required=True)
    parser.add_argument("--contract",type=Path,required=True)
    parser.add_argument("--audit",type=Path,required=True)
    parser.add_argument("--source-root",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--seed",type=int,choices=(42,),default=42)
    parser.add_argument("--execute",action="store_true")
    parser.add_argument("--gpu-grant")
    args=parser.parse_args()
    if not args.execute:
        print(json.dumps({"planned_only":True,"method":args.method,"caps":CAPS[args.method],"wall_cap_seconds":600,
            "diagnostic_only":True,"whole_method_gpu_validation_passed":False,"validation_content_read":False}))
        return 0
    if args.gpu_grant!="A100-post-training-explicit-slot":
        parser.error("fresh main-agent A100 diagnostic slot grant required")
    if args.output.exists():
        raise FileExistsError("diagnostic output is immutable")
    config=json.loads(args.config.read_text())
    contract=json.loads(args.contract.read_text())
    audit=json.loads(args.audit.read_text())
    verify_runner_binding(args.source_root,contract)
    effective,train,dataset=validate_inputs(args.source_root,config,contract,audit,args.method)
    operator_files={}
    for operator in (load_policy,causal_response_features,sample_prefix,paragraph_prefixes,
                     complete_response_tokens,naturally_complete_response,rewrite_messages,select_aligner,
                     validate_aligner,PositionHead,CorrectnessGate,position_loss,boxed_token_position,
                     remaining_response_budget,intervention_prefix_tokens,verified_reward,problem_messages):
        path=Path(inspect.getfile(operator)).resolve()
        try:
            relative=str(path.relative_to(args.source_root.resolve()))
        except ValueError as exc:
            raise ValueError("imported operators must come from the verified frozen source root") from exc
        actual=digest(path)
        if contract["source_file_sha256"].get(relative)!=actual:
            raise ValueError("actual imported operator source must match the approved contract")
        operator_files[relative]=actual
    if effective.get("device")!="cuda":
        raise ValueError("actual approved NVIDIA CUDA diagnostic required")
    args.output.mkdir(parents=True,exist_ok=False)
    ledger=CostLedger()
    evidence={"artifact_kind":"train_only_post_training_diagnosis_not_gpu_receipt","method":args.method,"seed":42,
        "diagnostic_only":True,"whole_method_gpu_validation_passed":False,"formal_comparison":False,
        "promotion_eligible":False,"validation_content_read":False,"test_content_read":False,
        "assessment_executed":False,"dataset":dataset,"configured_caps":CAPS[args.method],"wall_cap_seconds":600,
        "source_commit":contract["source_commit"],"core_source_sha256":contract["source_file_sha256"],
        "actually_imported_operator_files_sha256":operator_files,
        "diagnostic_runner_sha256":digest(__file__),"execution_config_sha256":audit["execution_config_sha256"]}
    def timeout(_signum,_frame):
        raise TimeoutError("predeclared 600-second wall cap reached")
    previous=signal.signal(signal.SIGALRM,timeout)
    started=time.monotonic()
    signal.alarm(600)
    code=0
    try:
        accelerator=torch.cuda.get_device_name()
        if "A100" not in accelerator:
            raise ValueError("current diagnosis grant is only for the real NVIDIA A100")
        evidence["accelerator"]={"vendor":"NVIDIA","model":accelerator}
        torch.manual_seed(42)
        (diagnose_synthself if args.method=="synthself" else diagnose_upturn)(effective,train,ledger,evidence,seed=42)
        generated=sum(ledger.generated_tokens.values())
        if generated>(8192 if args.method=="synthself" else 36848) or ledger.encoder_calls>32:
            raise ValueError("configured diagnostic generation/encoder bound exceeded")
        if not all(math.isfinite(x) for x in ledger.generated_tokens.values()):
            raise ValueError("invalid measured generation cost")
    except Exception as exc:
        evidence.update(diagnosis_status="diagnostic-execution-failed",error_type=type(exc).__name__,
                        error="inspect separate local runtime log; partial audits retained")
        print(str(exc),flush=True)
        code=1
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM,previous)
        evidence.update(actual_elapsed_seconds=time.monotonic()-started,cost=ledger.to_dict())
        evidence=strict_finite_evidence(evidence)
        if evidence.get("diagnostic_outputs_usable") is False:
            code=1
        with (args.output/"diagnosis.json").open("x") as stream:
            stream.write(json.dumps(evidence,ensure_ascii=False,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"method":args.method,"diagnosis_status":evidence["diagnosis_status"],
        "whole_method_gpu_validation_passed":False,"actual_elapsed_seconds":evidence["actual_elapsed_seconds"]}))
    return code


if __name__=="__main__":
    raise SystemExit(main())
