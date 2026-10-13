#!/usr/bin/env python3
"""Fixed cached 7B train-only SOAR format probe, never RL or GPU receipt."""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
from pathlib import Path
import signal
import time

import torch

from diagnose_oct14_post_training import digest, strict_finite_evidence
from auto_research.oct12_public_sources import read_jsonl_mirror
from auto_research.post_training.oct13_common import CostLedger, load_policy
from auto_research.reproductions.soar import checkpoint as soar_checkpoint
from auto_research.reproductions.soar.algorithm import (
    LexicalRetriever, internal_messages, normalize, parse_step, source_observation, source_reward,
)

MANIFEST_SHA="453d2ad74f5894e8cad18b18922291aef685cfb5107220f8d11eab78500c2c5a"
POLICY_ID="Qwen/Qwen2.5-7B-Instruct"
POLICY_REVISION="bb46c15ee4bb56c5b63245ef50fd7637234d6f75"
CAPS={"training_prefix":4,"episodes_per_question":2,"max_turns":3,"response_cap":256,
      "generated_response_tokens_upper":12288,"wall_cap_seconds":300,"optimizer_updates":0}


def validate_probe_inputs(root,config,contract,audit,*,manifest_sha256=MANIFEST_SHA):
    if (audit.get("source_commit")!=contract["source_commit"] or not audit.get("source_hashes_verified")
            or audit.get("source_file_sha256")!=contract["source_file_sha256"]
            or audit.get("cuda_initialized") is not False or audit.get("model_instantiated") is not False
            or audit.get("execution_config_sha256")!=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()):
        raise ValueError("exact source-bound CPU config/resource audit required")
    for relative,expected in contract["source_file_sha256"].items():
        if digest(root/relative)!=expected:
            raise ValueError("frozen source mismatch: "+relative)
    c={**config["shared"],**config["methods"]["soar"]}
    if (c.get("teacher_id")!=POLICY_ID or c.get("teacher_revision")!=POLICY_REVISION
            or c.get("max_tokens")!=256 or c.get("max_turns")!=3 or c.get("train_examples")!=8
            or c.get("verifier")!="normalized-em"):
        raise ValueError("explicit cached 7B policy and original SOAR caps/verifier required")
    role=audit["resources"]["teacher"]
    if role.get("public_id")!=POLICY_ID or role.get("revision")!=POLICY_REVISION or not role.get("verified"):
        raise ValueError("fixed public 7B must already be byte-verified")
    if digest(c["split_manifest"])!=manifest_sha256:
        raise ValueError("predeclared tool-group training manifest SHA mismatch")
    record=json.loads(Path(c["split_manifest"]).read_text())
    verified=audit["method_specific_holdouts"]["soar"]
    if (verified.get("status")!="verified" or verified.get("tool_groups_disjoint") is not True
            or record.get("source_split")!="train" or record.get("test_opened") is not False
            or record.get("source_revision")!=c["dataset_revision"]
            or record["partition_sha256"]!=verified["holdout"]["partition_sha256"]):
        raise ValueError("preverified independent tool-group-disjoint training QA required")
    content=Path(c["train_path"]).read_bytes()
    if hashlib.sha256(content).hexdigest()!=record["partition_sha256"]["train"]:
        raise ValueError("exact complete training file SHA required")
    rows=[json.loads(line) for line in content.splitlines() if line.strip()]
    if len(rows)!=record["counts"]["train"] or len(rows)<4:
        raise ValueError("original-order four training questions required")
    if audit["soar_corpus"].get("status")!="verified" or audit["soar_corpus"].get("generation_inputs_do_not_include_qa_answers") is not True:
        raise ValueError("independent presealed corpus audit required")
    documents,corpus=read_jsonl_mirror(Path(c["corpus_path"]),"documents.jsonl",c["corpus_id"],c["corpus_revision"],"train")
    if corpus["files"]!=audit["soar_corpus"]["file_sha256"]:
        raise ValueError("actual independent KB must match the prior byte audit")
    retriever=LexicalRetriever(documents)  # rejects gold/answer fields in the independent KB
    return c,rows[:4],retriever,{"source_revision":record["source_revision"],
        "split_manifest_sha256":manifest_sha256,"train_file_sha256":record["partition_sha256"]["train"],
        "selected_training_prefix":4,"validation_content_read":False,"test_content_read":False,
        "corpus":{"public_id":corpus["public_id"],"revision":corpus["revision"],"file_sha256":corpus["files"]}}


def episode(policy,retriever,question,ledger):
    """Original SOAR SYSTEM/parse/source streams, with exactly the original caps."""
    messages=({"role":"system","content":soar_checkpoint.SYSTEM},{"role":"user","content":question})
    streams={"internal":"","external":""}
    final={"kind":"invalid"}
    valid=True
    searches=0
    audits=[]
    for turn in range(3):
        response=ledger.sample(policy,messages,role="policy_trajectory",max_tokens=256)[0]
        action=parse_step(response.text)
        injected="<information>" in response.text
        if response.truncated or injected:
            valid=False
        audits.append({"turn":turn+1,"action_kind":action["kind"],"truncated":response.truncated,
            "generated_tokens":len(response.tokens),"policy_injected_information":injected,
            "response_text_sha256":hashlib.sha256(response.text.encode()).hexdigest()})
        if action["kind"]=="answer":
            final=action
            break
        if action["kind"]!="search":
            valid=False
            break
        query=action["query"]
        recall=ledger.sample(policy,internal_messages(query),role="isolated_internal_recall",max_tokens=256)[0]
        retrieved=retriever.retrieve(query,top_k=3)
        internal=recall.text
        external="\n".join(d["text"] for d in retrieved)
        streams["internal"]+="\n"+internal
        streams["external"]+="\n"+external
        searches+=1
        audits[-1].update(recall_truncated=recall.truncated,recall_generated_tokens=len(recall.tokens),
            retrieved_documents=len(retrieved),retrieved_text_characters=len(external),
            internal_recall_context_is_query_only=True)
        messages=messages+({"role":"assistant","content":response.text},
                           {"role":"user","content":source_observation(internal,external)})
    return final,streams,valid,searches,audits


def diagnose_format(config,train,retriever,ledger,evidence,*,seed=42):
    if len(train)!=4 or seed!=42:
        raise ValueError("format probe pins original four training questions and seed42")
    policy=load_policy(config,role="teacher",seed=42)  # explicit approved 7B-as-policy probe, not silent substitution
    if any(p.requires_grad for p in policy.model.parameters()):
        raise ValueError("all 7B policy parameters must remain frozen; no LoRA or optimizer")
    rows=evidence.setdefault("training_episode_audits",[])
    for index,row in enumerate(train):
        for repeat in range(2):
            final,streams,valid,searches,turns=episode(policy,retriever,row["question"],ledger)
            # Reference answer exists ONLY here, in the external training scorer.
            correct=float(normalize(final.get("answer",""))==normalize(row["answer"])) if final["kind"]=="answer" else 0.
            with_source,parts=source_reward(final,streams,answer_correct=correct,format_valid=valid,source_coefficient=.1)
            without_source,_=source_reward(final,streams,answer_correct=correct,format_valid=valid,source_coefficient=0.)
            rows.append({"training_row":index,"repeat":repeat+1,"final_action_kind":final["kind"],
                "valid_trajectory":valid,"searches":searches,"turns":turns,**parts,
                "source_consistent_reward":with_source,"without_source_reward":without_source})
    evidence.update(checkpoint={"policy":policy.provenance},policy_role="explicit fixed cached 7B used as frozen policy",
        original_system_sha256=hashlib.sha256(soar_checkpoint.SYSTEM.encode()).hexdigest(),
        gold_access_roles={"policy_generation":"none","isolated_recall":"query only, no inherited reasoning or gold",
            "retriever":"independent presealed public descriptions only","gold":"external training normalized-EM scorer only"},
        assessment_executed=False,lora_updates=0,optimizer_updates=0,backbone_parameters_frozen=True,
        diagnosis_status="format-signal-observed" if any(r["format"] for r in rows) else "no-format-signal",
        valid_format_episodes=sum(r["format"] for r in rows),source_match_episodes=sum(r["source_match"] for r in rows),
        total_searches=sum(r["searches"] for r in rows))
    if sum(ledger.generated_tokens.values())>12288:
        raise ValueError("predeclared 12288 response-token generation bound exceeded")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("config","contract","audit","source-root","output"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--execute",action="store_true")
    parser.add_argument("--gpu-grant")
    args=parser.parse_args()
    if not args.execute:
        print(json.dumps({"planned_only":True,"caps":CAPS,"policy_id":POLICY_ID,"policy_revision":POLICY_REVISION,
            "diagnostic_only":True,"whole_method_gpu_validation_passed":False,"validation_content_read":False}))
        return 0
    if args.gpu_grant!="A100-post-training-explicit-slot":
        parser.error("fresh explicit main-agent A100 SOAR-format slot required")
    if args.output.exists():
        raise FileExistsError("format probe output is immutable")
    config=json.loads(args.config.read_text())
    contract=json.loads(args.contract.read_text())
    audit=json.loads(args.audit.read_text())
    actual=Path(__file__).resolve()
    relative="scripts/diagnose_oct14_soar_format.py"
    if actual!=(args.source_root/relative).resolve() or contract["source_file_sha256"].get(relative)!=digest(actual):
        raise ValueError("actual probe runner must be frozen-root and contract hash-bound")
    imported={}
    for operator in (load_policy,read_jsonl_mirror,LexicalRetriever,internal_messages,normalize,parse_step,
                     source_observation,source_reward,strict_finite_evidence,soar_checkpoint):
        path=Path(inspect.getfile(operator)).resolve()
        name=str(path.relative_to(args.source_root.resolve()))
        if contract["source_file_sha256"].get(name)!=digest(path):
            raise ValueError("all actual imported operators must match the frozen source contract")
        imported[name]=digest(path)
    effective,train,retriever,dataset=validate_probe_inputs(args.source_root,config,contract,audit)
    if effective.get("device")!="cuda":
        raise ValueError("approved A100 CUDA probe required")
    args.output.mkdir(parents=True,exist_ok=False)
    ledger=CostLedger()
    evidence={"artifact_kind":"train_only_soar_format_probe_not_gpu_receipt","method":"soar","seed":42,
        "diagnostic_only":True,"whole_method_gpu_validation_passed":False,"formal_comparison":False,
        "promotion_eligible":False,"validation_content_read":False,"test_content_read":False,
        "dataset":dataset,"configured_caps":CAPS,"source_commit":contract["source_commit"],
        "core_source_sha256":contract["source_file_sha256"],"actually_imported_operator_files_sha256":imported,
        "diagnostic_runner_sha256":digest(__file__),"execution_config_sha256":audit["execution_config_sha256"]}
    def timeout(_signum,_frame):
        raise TimeoutError("predeclared 300-second format-probe wall cap reached")
    previous=signal.signal(signal.SIGALRM,timeout)
    started=time.monotonic()
    signal.alarm(300)
    code=0
    try:
        accelerator=torch.cuda.get_device_name()
        if "A100" not in accelerator:
            raise ValueError("probe grant requires the actual NVIDIA A100")
        evidence["accelerator"]={"vendor":"NVIDIA","model":accelerator}
        torch.manual_seed(42)
        diagnose_format(effective,train,retriever,ledger,evidence)
    except Exception as exc:
        evidence.update(diagnosis_status="diagnostic-execution-failed",error_type=type(exc).__name__,
            error="inspect separate local runtime log; partial episode audits retained")
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
    print(json.dumps({"diagnosis_status":evidence["diagnosis_status"],"whole_method_gpu_validation_passed":False,
        "actual_elapsed_seconds":evidence["actual_elapsed_seconds"]}))
    return code


if __name__=="__main__":
    raise SystemExit(main())
