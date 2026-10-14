#!/usr/bin/env python3
"""Bounded frozen-7B teacher diagnosis; never a formal MBS run or GPU receipt."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata as metadata
import inspect
import json
import math
from pathlib import Path
import re
import signal
import sys
import time
from types import SimpleNamespace

ALGORITHM_COMMIT="ce4a4a34520419a50fb730d93967aaed5024fa77"
CONFIG_SHA="6717f5dd647b812e5fc6dcdcd91b3f089e2a55003bc6ee68ac76d88319a7b1df"
MANIFEST_SHA="c0b9b2424d9b497e4b7f6c0188ac0c0a9235bf151a046d559fb181f44e10bcbd"
TEACHER_ID="Qwen/Qwen2.5-7B-Instruct"
TEACHER_REVISION="bb46c15ee4bb56c5b63245ef50fd7637234d6f75"
ROOT_HASHES={4:"d38bacc8724a241927dec39e1459b3c17295f79d244c7ec4a518303968c9dc01",
    7:"a13430e732d2c1e663238de0e34daf75abd640df18ff2ab97d0d55479204c2d1",
    8:"699ab79580f3d4e07173fdf9ff3b39ab4d4aa99e3efdf92ea650753c03c27a4d"}
PRIOR_FAILURE_SHA="19c56c036b6dd87f7658c14a7c45c53065a662c920cc807532ce6bbbdba6151d"
CAPS={"training_roots":[4,7,8],"validation_prefix":4,"response_cap":1024,
    "outputs_upper":14,"generated_tokens_upper":14336,"wall_cap_seconds":600,
    "student_generation_calls":0,"optimizer_updates":0}
EXPECTED={"train_examples":16,"validation_examples":4,"max_tokens":1024,"group":4,"depth":1,
    "hard_root_limit":4,"steps":2,"teacher_attempts":2,"decomposition_retries":2,"synthesis_retries":2,
    "construction_json_schema":True,"context_limit":4096,"device":"cuda"}
RUNNER="scripts/diagnose_oct14_mbs_teacher_quality.py"
CRITICAL={"src/auto_research/post_training/response_policy.py","src/auto_research/post_training/oct13_common.py",
    "src/auto_research/reproductions/magicbeanstalk/checkpoint.py","src/auto_research/reproductions/magicbeanstalk/algorithm.py"}
DEPENDENCIES={"xgrammar":"0.2.8","apache-tvm-ffi":"0.1.11","pydantic":"2.12.5","pydantic-core":"2.41.5",
    "annotated-types":"0.7.0","typing-inspection":"0.4.2","typing-extensions":"4.15.0"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()


def verify_source_marker(root,expected):
    marker=Path(root)/".source-commit"
    if not marker.is_file() or marker.read_text().strip()!=expected:
        raise ValueError("actual immutable root .source-commit marker is missing or drifted")


def finite_evidence(value):
    paths=[]
    def clean(x,path):
        if isinstance(x,float) and not math.isfinite(x):
            paths.append(path);return None
        if isinstance(x,dict):return {k:clean(v,path+"."+k) for k,v in x.items()}
        if isinstance(x,(list,tuple)):return [clean(v,path+"["+str(i)+"]") for i,v in enumerate(x)]
        return x
    result=clean(value,"$")
    result["diagnostic_outputs_usable"]=not paths and result.get("diagnosis_status")!="diagnostic-execution-failed"
    if paths:result.update(diagnosis_status="diagnostic-failed-nonfinite-output",nonfinite_paths=paths)
    return result


def verify_runner(root,contract,audit,*,runner_path=None):
    verify_source_marker(root,contract.get("source_commit"))
    actual=Path(__file__ if runner_path is None else runner_path).resolve()
    if (actual!=(Path(root)/RUNNER).resolve() or not re.fullmatch(r"[0-9a-f]{40}",contract.get("source_commit",""))
        or contract.get("source_commit")==ALGORITHM_COMMIT
        or contract.get("source_file_sha256",{}).get(RUNNER)!=digest(actual)
        or audit.get("artifact_kind")!="read_only_cpu_resource_audit_not_gpu_receipt"
        or audit.get("source_commit")!=contract["source_commit"] or audit.get("source_hashes_verified") is not True
        or audit.get("source_file_sha256")!=contract["source_file_sha256"]
        or audit.get("cuda_initialized") is not False or audit.get("model_instantiated") is not False
        or audit.get("execution_config_sha256")!=CONFIG_SHA):
        raise ValueError("actual diagnostic entry must be frozen-root and contract SHA bound")
    for name,sha in contract["source_file_sha256"].items():
        relative=Path(name)
        if relative.is_absolute() or ".." in relative.parts or digest(Path(root)/relative)!=sha:
            raise ValueError("actual runner frozen-source bytes must match its own CPU audit")


def validate_core(root,config,contract,audit,*,expected_config_sha256=CONFIG_SHA):
    verify_source_marker(root,ALGORITHM_COMMIT)
    if (contract.get("source_commit")!=ALGORITHM_COMMIT or len(contract.get("source_file_sha256",{}))!=54
        or not CRITICAL.issubset(contract.get("source_file_sha256",{}))
        or audit.get("artifact_kind")!="read_only_cpu_resource_audit_not_gpu_receipt"
        or audit.get("source_commit")!=ALGORITHM_COMMIT or audit.get("source_hashes_verified") is not True
        or audit.get("source_file_sha256")!=contract["source_file_sha256"]
        or audit.get("cuda_initialized") is not False or audit.get("model_instantiated") is not False
        or canonical(config)!=expected_config_sha256 or audit.get("execution_config_sha256")!=expected_config_sha256):
        raise ValueError("exact ce4 operators and immutable original CPU resource/config audit required")
    for name,sha in contract["source_file_sha256"].items():
        relative=Path(name)
        if relative.is_absolute() or ".." in relative.parts or digest(Path(root)/relative)!=sha:
            raise ValueError("actual ce4 source bytes required")
    c={**config["shared"],**config["methods"]["magicbeanstalk"]}
    if any(c.get(k)!=v or type(c.get(k)) is not type(v) for k,v in EXPECTED.items()):
        raise ValueError("all original MBS budgets and explicit schema boolean must remain unchanged")
    teacher=audit["resources"]["teacher"]
    if (c.get("teacher_id")!=TEACHER_ID or c.get("teacher_revision")!=TEACHER_REVISION
        or teacher.get("verified") is not True or teacher.get("public_id")!=TEACHER_ID
        or teacher.get("revision")!=TEACHER_REVISION
        or audit["public_train_only_holdout"].get("verified") is not True
        or audit["public_train_only_holdout"].get("test_read") is not False):
        raise ValueError("fixed cached teacher and unchanged public train-only holdout required")
    directory=Path(c["teacher_path"])
    manifest=json.loads((directory/"provenance.json").read_text())
    if (manifest.get("kind")!="checkpoint" or manifest.get("public_id")!=TEACHER_ID
        or manifest.get("revision")!=TEACHER_REVISION or manifest.get("files")!=teacher.get("file_sha256")):
        raise ValueError("actual teacher public manifest must match the exact resource audit")
    for name,sha in teacher["file_sha256"].items():
        relative=Path(name)
        if relative.is_absolute() or ".." in relative.parts or digest(directory/relative)!=sha:
            raise ValueError("actual teacher checkpoint bytes drifted")
    return c


def validate_dependencies(overlay,audit):
    root=Path(overlay).resolve()
    packages=audit.get("packages",{})
    if (audit.get("cuda_initialized") is not False or audit.get("model_instantiated_by_audit") is not False
        or audit.get("dependency_modules_imported_by_audit") is not False
        or Path(audit.get("overlay_root","")).resolve()!=root or set(packages)!=set(DEPENDENCIES)
        or canonical(packages)!=audit.get("dependency_fingerprint")):
        raise ValueError("actual fixed-overlay CPU dependency audit required")
    distributions=list(metadata.Distribution.discover(path=[str(root)]))
    for name,version in DEPENDENCIES.items():
        matches=[d for d in distributions if re.sub(r"[-_.]+","-",d.metadata.get("Name","")).lower()==name]
        if len(matches)!=1 or matches[0].version!=version or packages[name].get("version")!=version:
            raise ValueError("actual fixed dependency metadata/version required")
        files=packages[name].get("package_file_sha256",{})
        if not files:raise ValueError("dependency file bytes must be recorded")
        for relative,sha in files.items():
            path=(root/relative).resolve()
            if not path.is_relative_to(root) or digest(path)!=sha:raise ValueError("actual overlay package bytes drifted")
    sys.path.insert(0,str(root))
    spec=importlib.util.find_spec("xgrammar")
    if spec is None or not Path(spec.origin).resolve().is_relative_to(root):
        raise ValueError("XGrammar must actually resolve inside the fixed overlay")
    return audit


def read_partitions(c,audit,*,expected_manifest_sha=MANIFEST_SHA):
    if digest(c["split_manifest"])!=expected_manifest_sha:raise ValueError("immutable split manifest SHA required")
    manifest=json.loads(Path(c["split_manifest"]).read_text())
    if (manifest.get("source_split")!="train" or manifest.get("test_opened") is not False
        or manifest.get("source_revision")!=c["dataset_revision"]
        or manifest["partition_sha256"]!=audit["public_train_only_holdout"]["partition_sha256"]):
        raise ValueError("fixed training/validation partition; official test must stay unopened")
    rows={}
    for name in ("train","validation"):
        content=Path(c[name+"_path"]).read_bytes()
        if hashlib.sha256(content).hexdigest()!=manifest["partition_sha256"][name]:
            raise ValueError("exact full public partition bytes required: "+name)
        rows[name]=[json.loads(line) for line in content.splitlines() if line.strip()]
        if len(rows[name])!=manifest["counts"][name] or any(not isinstance(x.get(k),str) for x in rows[name] for k in ("question","answer")):
            raise ValueError("verified complete public question/answer rows required")
    if len(rows["train"])<16 or len(rows["validation"])<4:raise ValueError("original fixed prefixes required")
    train,validation=rows["train"][:16],rows["validation"][:4]
    if any(hashlib.sha256(train[i]["question"].encode()).hexdigest()!=sha for i,sha in ROOT_HASHES.items()):
        raise ValueError("only the three actual prior ce4 hard-root questions may be probed")
    return train,validation,{"source_revision":manifest["source_revision"],"split_manifest_sha256":expected_manifest_sha,
        "partition_sha256":manifest["partition_sha256"],"validation_content_read":True,"test_content_read":False,
        "training_prefix":16,"selected_training_indices":[4,7,8],"validation_prefix":4,
        "prior_calibration_failure_sha256":PRIOR_FAILURE_SHA,"target_hardness_recalibrated":False}


def load_operators(root,contract):
    sys.path.insert(0,str(Path(root)/"src"))
    common=importlib.import_module("auto_research.post_training.oct13_common")
    checkpoint=importlib.import_module("auto_research.reproductions.magicbeanstalk.checkpoint")
    reward=importlib.import_module("auto_research.post_training.oct10_checkpoint")
    prompt=importlib.import_module("auto_research.post_training.proximal_checkpoint")
    ops=SimpleNamespace(CostLedger=common.CostLedger,load_policy=common.load_policy,
        CheckpointConstruction=checkpoint.CheckpointConstruction,Problem=checkpoint.Problem,
        construction_schema=checkpoint.construction_schema,verified_reward=reward.verified_reward,
        problem_messages=prompt.problem_messages)
    files={}
    for name,module in tuple(sys.modules.items()):
        if not name.startswith("auto_research.") or not getattr(module,"__file__",None):continue
        path=Path(inspect.getfile(module)).resolve()
        if path.suffix!=".py":continue
        relative=path.relative_to(Path(root).resolve()).as_posix()
        if relative not in contract["source_file_sha256"]:continue
        if digest(path)!=contract["source_file_sha256"][relative]:raise ValueError("actually imported operator source SHA mismatch")
        files[relative]=digest(path)
    for operator in vars(ops).values():
        path=Path(inspect.getfile(operator)).resolve()
        relative=path.relative_to(Path(root).resolve()).as_posix()
        if contract["source_file_sha256"].get(relative)!=digest(path):raise ValueError("operators must import from ce4 root, not runner source")
    return ops,files


class RecordingLedger:
    def __init__(self,ledger,evidence,*,clock=time.monotonic,partial_output=None,execution_started=None):
        self.ledger,self.evidence,self.clock=ledger,evidence,clock
        self.start=clock() if execution_started is None else execution_started
        self.partial_output=partial_output
        if partial_output is not None:Path(partial_output).mkdir(parents=True,exist_ok=False)
        evidence.update(response_audits=[],generation_attempts=[],actual_output_count=0,cost=ledger.to_dict())
    def persist(self,stage):
        if self.partial_output is None:return
        snapshot=finite_evidence({**self.evidence,"partial_snapshot":True,"not_gpu_receipt":True,
            "whole_method_gpu_validation_passed":False})
        snapshot["diagnostic_outputs_usable"]=False
        path=Path(self.partial_output)/(f"{len(self.evidence['generation_attempts']):02d}-"+stage+".json")
        with path.open("x",encoding="utf-8") as stream:
            stream.write(json.dumps(snapshot,ensure_ascii=False,indent=2,allow_nan=False)+"\n")
    def sample(self,policy,messages,*,role,samples=1,max_tokens=1024,sample=False,json_schema=None):
        e=self.evidence
        if self.clock()-self.start>=600:raise TimeoutError("600-second inner probe deadline reached")
        if samples!=1 or max_tokens!=1024 or len(e["generation_attempts"])>=14:
            raise ValueError("predeclared generation bound cannot be expanded")
        attempt={"role":role,"completed":False,"sample":sample,"max_tokens":max_tokens,
            "actual_messages":list(messages),"json_schema_constrained":json_schema is not None,
            "input_gold_scope":"training-construction-context" if json_schema is not None else "question-only-no-answer-or-trace"}
        e["generation_attempts"].append(attempt)
        e["unreturned_generation_cost_measured"]=False
        self.persist("started")
        responses=self.ledger.sample(policy,messages,role=role,samples=1,max_tokens=1024,sample=sample,json_schema=json_schema)
        for response in responses:
            e["response_audits"].append({"role":role,"sample":sample,"response_text":response.text,
                "response_token_ids":list(response.tokens),"response_text_sha256":hashlib.sha256(response.text.encode()).hexdigest(),
                "generated_tokens":len(response.tokens),"truncated":response.truncated})
        attempt.update(completed=True,actual_responses=len(responses))
        e.update(actual_output_count=len(e["response_audits"]),cost=self.ledger.to_dict(),unreturned_generation_cost_measured=True)
        self.persist("completed")
        if (len(responses)!=1 or e["actual_output_count"]>14 or any(len(r.tokens)>1024 for r in responses)
            or sum(self.ledger.generated_tokens.values())>14336):raise ValueError("actual response/output/token bound exceeded; raw retained")
        if self.clock()-self.start>=600:raise TimeoutError("600-second inner probe deadline reached")
        return responses


def diagnose_quality(config,train,validation,ops,evidence,*,policy=None,clock=time.monotonic,partial_output=None,execution_started=None):
    if len(train)!=16 or len(validation)!=4:raise ValueError("only original train16/validation4 allowed")
    evidence.update(artifact_kind="mbs_teacher_quality_diagnostic_not_gpu_receipt",method="magicbeanstalk",seed=42,diagnostic_only=True,
        not_gpu_receipt=True,whole_method_gpu_validation_passed=False,formal_comparison=False,promotion_eligible=False,
        student_generation_calls=0,lora_updates=0,optimizer_updates=0,student_instantiated=False,
        validation_content_read=True,test_content_read=False,formal_mbs_sampling_changed=False,
        scaffold_safety_executed=False,effectivity_executed=False,synthesis_executed=False,goldilocks_executed=False,
        greedy_construction_wrapper_is_diagnostic_only=True,configured_caps=CAPS,
        gold_access_roles={"root_and_child_solving":"question only; gold external scorer",
            "construction_teacher":"verified TRAIN parent trace and train answer allowed",
            "validation_teacher":"question only; validation answer external scorer"})
    ledger=RecordingLedger(ops.CostLedger(),evidence,clock=clock,partial_output=partial_output,execution_started=execution_started)
    policy=ops.load_policy(config,role="teacher",seed=42) if policy is None else policy
    if policy.optimizer is not None or any(p.requires_grad for p in policy.model.parameters()):
        raise ValueError("teacher must remain frozen; no student/LoRA/optimizer")
    evidence.update(checkpoint=policy.provenance,backbone_parameters_frozen=True,training_root_solves=[])
    verified_parent=None
    for index in (4,7,8):
        row=train[index]
        response=ledger.sample(policy,ops.problem_messages(row["question"]),role="train_root_greedy")[0]
        correct=0. if response.truncated else ops.verified_reward(response.text,row["answer"])
        evidence["training_root_solves"].append({"training_index":index,"correct":correct,
            "truncated":response.truncated,"question_sha256":hashlib.sha256(row["question"].encode()).hexdigest()})
        if index==4 and correct:verified_parent=ops.Problem(row["question"],row["answer"],response.text)
    proposal=evidence.setdefault("proposal",{"attempted":False,"verified_child_count":0,
        "reject_reason":"root4_greedy_independent_verification_failed"})
    if verified_parent is not None:
        class GreedyConstruction(ops.CheckpointConstruction):
            def teacher_json(self,instruction,context,*,operation="teacher_json"):
                schema=ops.construction_schema(operation)
                messages=({"role":"user","content":instruction+"\nOutput JSON only, without prose or code fences.\n"+
                    json.dumps(context,ensure_ascii=False)},)
                response=self.ledger.sample(self.teacher,messages,role="construction_teacher",json_schema=schema,sample=False)[0]
                sha=hashlib.sha256(json.dumps(schema,separators=(",",":"),allow_nan=False).encode()).hexdigest()
                actual=getattr(self.teacher,"last_json_schema_generation",{})
                audit=self.record_response(response,role="construction_teacher",input_gold_scope="training-construction-context",
                    operation=operation,json_schema_sha256=sha,diagnostic_greedy_override=True,parsing_completed=False)
                if actual.get("schema_sha256")!=sha or actual.get("backend")!="xgrammar-hf" or actual.get("version")!="0.2.8":
                    raise ValueError("actual ordered XGrammar 0.2.8 generation metadata required")
                try:value=None if response.truncated else json.loads(response.text)
                except json.JSONDecodeError:value=None  # No repair or inner-object extraction.
                audit.update(parsing_completed=True,parsed_json_kind=type(value).__name__,truncated=response.truncated)
                return value
        backend=GreedyConstruction(policy,None,ledger,max_tokens=1024,rollouts=4,teacher_attempts=2,construction_json_schema=True)
        evidence["construction_response_audits"]=backend.response_audits
        children=backend.propose_children(verified_parent,[])
        proposal.update(attempted=True,proposed_child_count=len(children),reject_reason=None if len(children)==2 else "invalid_or_incomplete_two_child_proposal",children=[])
        if len(children)==2:
            for child in children:
                response=ledger.sample(policy,ops.problem_messages(child.question),role="train_child_greedy")[0]
                correct=0. if response.truncated else ops.verified_reward(response.text,child.answer)
                proposal["children"].append({"question":child.question,"proposed_answer":child.answer,"proposed_trace":child.trace,
                    "independent_correct":correct,"truncated":response.truncated})
                proposal["verified_child_count"]+=int(correct)
            if proposal["verified_child_count"]<2:proposal["reject_reason"]="fewer_than_two_independently_correct_children"
    evidence["validation_profiles"]={}
    for profile,sample in (("current-t1",True),("greedy",False)):
        measurements=[]
        evidence["validation_profiles"][profile]={"completed":False,"rows":measurements,
            "sampling":{"sample":True,"temperature":1.,"top_p":1.,"top_k":0} if sample else {"sample":False}}
        for index,row in enumerate(validation):
            response=ledger.sample(policy,ops.problem_messages(row["question"]),role="validation_"+profile,sample=sample)[0]
            correct=0. if response.truncated else ops.verified_reward(response.text,row["answer"])
            measurements.append({"validation_index":index,"correct":correct,"truncated":response.truncated})
        evidence["validation_profiles"][profile].update(completed=True,accuracy=sum(x["correct"] for x in measurements)/4)
    evidence.update(diagnosis_status="completed-teacher-quality-diagnostic",formal_mbs_assessment_executed=False,
        student_assessment_executed=False,
        teacher_validation_executed=True,limitations=["Not a formal MBS run: construction uses an explicit greedy diagnostic subclass only.",
            "Four fixed validation cases compare teacher profiles; no stable gain, student training, effectivity or Goldilocks claim."])


def main():
    started=time.monotonic()
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("config","algorithm-root","algorithm-contract","algorithm-audit","source-root","contract","audit",
        "overlay-root","dependency-audit","output"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--execute",action="store_true")
    parser.add_argument("--gpu-grant")
    args=parser.parse_args()
    if not args.execute:
        print(json.dumps({"planned_only":True,"caps":CAPS,"whole_method_gpu_validation_passed":False,
            "validation_content_read_if_executed":True,"test_content_read":False}));return 0
    if args.gpu_grant!="A100-MBS-teacher-quality-explicit-slot":parser.error("new explicit A100 teacher-quality slot required")
    if args.output.exists():raise FileExistsError("diagnostic output is immutable")
    runner_contract=json.loads(args.contract.read_text())
    runner_audit=json.loads(args.audit.read_text());verify_runner(args.source_root,runner_contract,runner_audit)
    config=json.loads(args.config.read_text());contract=json.loads(args.algorithm_contract.read_text());audit=json.loads(args.algorithm_audit.read_text())
    c=validate_core(args.algorithm_root,config,contract,audit)
    train,validation,dataset=read_partitions(c,audit)
    dependencies=validate_dependencies(args.overlay_root,json.loads(args.dependency_audit.read_text()))
    ops,imported=load_operators(args.algorithm_root,contract)
    if time.monotonic()-started>=600:raise TimeoutError("CPU preflight consumed the entire 600-second invocation bound")
    args.output.mkdir(parents=True,exist_ok=False)
    evidence={"source_commit":runner_contract["source_commit"],"diagnostic_runner_sha256":digest(__file__),
        "runner_source_marker_sha256":digest(args.source_root/".source-commit"),
        "algorithm_source_marker_sha256":digest(args.algorithm_root/".source-commit"),
        "algorithm_commit":ALGORITHM_COMMIT,"algorithm_source_file_sha256":contract["source_file_sha256"],
        "actually_imported_operator_files_sha256":imported,"execution_config_sha256":CONFIG_SHA,"dataset":dataset,
        "wall_cap_seconds":600,"external_controller_wall_cap_required_seconds":600,
        "schema_dependency_binding":dependencies,"schema_dependency_audit_sha256":digest(args.dependency_audit),
        "artifact_kind":"mbs_teacher_quality_diagnostic_not_gpu_receipt","method":"magicbeanstalk","seed":42,"diagnostic_only":True,
        "not_gpu_receipt":True,"whole_method_gpu_validation_passed":False,"formal_comparison":False,
        "promotion_eligible":False,"validation_content_read":True,"test_content_read":False,
        "student_instantiated":False,"student_generation_calls":0,"lora_updates":0,"optimizer_updates":0,
        "concurrent_latency_comparison_eligible":False}
    def timeout(_signum,_frame):raise TimeoutError("600-second teacher-quality wall cap reached")
    previous=signal.signal(signal.SIGALRM,timeout)
    signal.setitimer(signal.ITIMER_REAL,max(.001,600-(time.monotonic()-started)));code=0
    try:
        import torch
        accelerator=torch.cuda.get_device_name()
        if "A100" not in accelerator:raise ValueError("actual NVIDIA A100 required")
        evidence["accelerator"]={"vendor":"NVIDIA","model":accelerator}
        torch.manual_seed(42)
        diagnose_quality(c,train,validation,ops,evidence,partial_output=args.output/"generation-partials",execution_started=started)
    except Exception as exc:
        evidence.update(diagnosis_status="diagnostic-execution-failed",error_type=type(exc).__name__,
            error="inspect runtime log; actual completed responses and pending generation audit retained")
        print(str(exc),flush=True);code=1
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous)
        evidence["actual_elapsed_seconds"]=time.monotonic()-started
        if "torch" in locals() and torch.cuda.is_initialized():
            evidence["actual_max_memory_allocated_bytes"]=torch.cuda.max_memory_allocated()
            evidence["actual_max_memory_reserved_bytes"]=torch.cuda.max_memory_reserved()
            if evidence["actual_max_memory_reserved_bytes"]>24*1024**3:
                evidence.update(diagnosis_status="diagnostic-execution-failed",teacher_memory_reserve_exceeded=True);code=1
        if evidence["actual_elapsed_seconds"]>600:
            evidence.update(diagnosis_status="diagnostic-execution-failed",wall_cap_exceeded=True);code=1
        evidence=finite_evidence(evidence)
        if not evidence["diagnostic_outputs_usable"]:code=1
        with (args.output/"diagnosis.json").open("x",encoding="utf-8") as stream:
            stream.write(json.dumps(evidence,ensure_ascii=False,indent=2,allow_nan=False)+"\n")
    return code


if __name__=="__main__":raise SystemExit(main())
