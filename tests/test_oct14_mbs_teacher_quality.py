"""CPU-only guards for a diagnostic, not evidence of a new GPU validation."""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
from types import SimpleNamespace

import pytest

from auto_research.post_training.oct10_checkpoint import verified_reward
from auto_research.post_training.oct13_common import CostLedger
from auto_research.post_training.proximal_checkpoint import problem_messages
from auto_research.post_training.response_policy import GeneratedResponse
from auto_research.reproductions.magicbeanstalk import checkpoint

ROOT=Path(__file__).resolve().parents[1]
M=runpy.run_path(str(ROOT/"scripts/diagnose_oct14_mbs_teacher_quality.py"))
OPS=SimpleNamespace(CheckpointConstruction=checkpoint.CheckpointConstruction,Problem=checkpoint.Problem,
    construction_schema=checkpoint.construction_schema,CostLedger=CostLedger,
    verified_reward=verified_reward,problem_messages=problem_messages)


class Policy:
    optimizer=None
    provenance={"public_id":M["TEACHER_ID"],"revision":M["TEACHER_REVISION"]}
    model=SimpleNamespace(parameters=lambda:iter([SimpleNamespace(requires_grad=False)]))
    def __init__(self,*,bad_root=False,bad_json=False,truncated=False,crash_at=None,oversize=False):
        self.calls=[];self.bad_root=bad_root;self.bad_json=bad_json;self.truncated=truncated
        self.crash_at=crash_at;self.oversize=oversize
    def generate(self,messages,*,samples,max_tokens,sample,json_schema=None):
        self.calls.append((messages,sample,json_schema))
        if self.crash_at==len(self.calls):raise RuntimeError("CPU fixture generation interruption")
        if json_schema:
            self.last_json_schema_generation={"backend":"xgrammar-hf","version":"0.2.8",
                "schema_sha256":hashlib.sha256(json.dumps(json_schema,separators=(",",":"),allow_nan=False).encode()).hexdigest()}
            text='[{"question":"CHILD-A","trace":"One item.","answer":"1"},{"question":"CHILD-B","trace":"Two items.","answer":"2"}]'
            if self.bad_json:text='prefix '+text
        else:
            q=messages[0]["content"]
            answer="2" if "CHILD-B" in q else "0" if self.bad_root and "TRAIN-4" in q else "72" if "TRAIN-" in q else "1"
            text="\\boxed{"+answer+"}"
        return [GeneratedResponse(tuple(range(1025 if self.oversize else 3)),text,self.truncated)]


def rows():
    return ([{"question":f"TRAIN-{i}","answer":"TRAIN-GOLD-SECRET #### 72"} for i in range(16)],
        [{"question":f"VALIDATION-{i}","answer":"VAL-GOLD-SECRET #### 1"} for i in range(4)])


def run(policy,*,evidence=None,clock=None):
    evidence={} if evidence is None else evidence
    kwargs={} if clock is None else {"clock":clock}
    M["diagnose_quality"]({},*rows(),OPS,evidence,policy=policy,**kwargs)
    return evidence


def test_fourteen_outputs_and_explicit_greedy_wrapper_preserve_gold_roles():
    p=Policy();e=run(p)
    assert e["actual_output_count"]==14 and e["lora_updates"]==e["student_generation_calls"]==0
    assert e["whole_method_gpu_validation_passed"] is False and e["not_gpu_receipt"] is True
    assert e["validation_content_read"] is True and e["test_content_read"] is False
    assert [x["training_index"] for x in e["training_root_solves"]]==[4,7,8]
    assert e["formal_mbs_sampling_changed"] is False
    assert e["greedy_construction_wrapper_is_diagnostic_only"] is True
    assert not any(e[k+"_executed"] for k in ("scaffold_safety","effectivity","synthesis","goldilocks"))
    assert e["proposal"]["verified_child_count"]==2
    assert e["validation_profiles"]["current-t1"]["accuracy"]==1.
    assert e["validation_profiles"]["greedy"]["accuracy"]==1.
    assert sum(sample for _,sample,_ in p.calls)==4
    for messages,_,schema in p.calls:
        text=json.dumps(messages)
        assert "VAL-GOLD-SECRET" not in text
        if schema:assert "TRAIN-GOLD-SECRET" in text
        else:assert "TRAIN-GOLD-SECRET" not in text
    assert all(x["response_text_sha256"]==hashlib.sha256(x["response_text"].encode()).hexdigest()
        and len(x["response_token_ids"])==x["generated_tokens"] for x in e["response_audits"])


def test_root4_failure_blocks_proposal_but_keeps_validation_and_other_roots():
    e=run(Policy(bad_root=True))
    assert e["actual_output_count"]==11
    assert e["proposal"]["attempted"] is False
    assert e["proposal"]["reject_reason"]=="root4_greedy_independent_verification_failed"


def test_invalid_json_is_not_repaired_or_inner_object_extracted():
    e=run(Policy(bad_json=True))
    assert e["actual_output_count"]==12
    assert e["proposal"]["verified_child_count"]==0
    assert e["construction_response_audits"][0]["parsed_json_kind"]=="NoneType"


def test_truncated_solve_cannot_be_scored_as_correct_or_used_for_construction():
    e=run(Policy(truncated=True))
    assert not any(x["correct"] for x in e["training_root_solves"])
    assert e["proposal"]["attempted"] is False
    assert all(p["accuracy"]==0 for p in e["validation_profiles"].values())


def test_generation_exception_keeps_actual_completed_responses_and_pending_role():
    e={}
    with pytest.raises(RuntimeError):run(Policy(crash_at=2),evidence=e)
    assert e["response_audits"][0]["response_text"]=="\\boxed{72}"
    assert e["generation_attempts"][1]["completed"] is False
    assert e["unreturned_generation_cost_measured"] is False


def test_response_over_cap_is_preserved_but_rejected():
    e={}
    with pytest.raises(ValueError,match="bound"):run(Policy(oversize=True),evidence=e)
    assert e["response_audits"][0]["generated_tokens"]==1025


def test_deadline_blocks_next_call_without_fabricating_output():
    e={};times=iter([0.,601.])
    with pytest.raises(TimeoutError):run(Policy(),evidence=e,clock=lambda:next(times))
    assert not e["response_audits"]


def test_frozen_teacher_guard_rejects_any_optimizer_or_trainable_parameter():
    p=Policy();p.optimizer=object()
    with pytest.raises(ValueError,match="frozen"):run(p)


@pytest.mark.parametrize("field,value",[("algorithm_commit","0"*40),("source_hashes_verified",False),
    ("cuda_initialized",True),("model_instantiated",True),("execution_config_sha256","0"*64)])
def test_core_cpu_audit_binding_rejects_wrong_commit_hash_or_runtime_state(tmp_path,field,value):
    config,contract,audit=inputs(tmp_path)
    audit[field if field!="algorithm_commit" else "source_commit"]=value
    with pytest.raises(ValueError):M["validate_core"](tmp_path,config,contract,audit,
        expected_config_sha256=M["canonical"](config))


def inputs(tmp_path):
    (tmp_path/".source-commit").write_text(M["ALGORITHM_COMMIT"]+"\n")
    hashes={}
    names=sorted(M["CRITICAL"])+[f"src/operator-{i}.py" for i in range(50)]
    for name in names:
        p=tmp_path/name;p.parent.mkdir(exist_ok=True,parents=True);p.write_text("CPU-only source fixture")
        hashes[str(p.relative_to(tmp_path))]=M["digest"](p)
    teacher=tmp_path/"teacher";teacher.mkdir();(teacher/"config.json").write_text("{}")
    files={"config.json":M["digest"](teacher/"config.json")}
    (teacher/"provenance.json").write_text(json.dumps({"kind":"checkpoint","public_id":M["TEACHER_ID"],
        "revision":M["TEACHER_REVISION"],"files":files}))
    shared={"teacher_id":M["TEACHER_ID"],"teacher_revision":M["TEACHER_REVISION"],"device":"cuda","context_limit":4096,
        "teacher_path":str(teacher)}
    settings={"train_examples":16,"validation_examples":4,"max_tokens":1024,"group":4,"depth":1,
        "hard_root_limit":4,"steps":2,"teacher_attempts":2,"decomposition_retries":2,"synthesis_retries":2,
        "construction_json_schema":True}
    config={"shared":shared,"methods":{"magicbeanstalk":settings}}
    contract={"source_commit":M["ALGORITHM_COMMIT"],"source_file_sha256":hashes}
    audit={**contract,"artifact_kind":"read_only_cpu_resource_audit_not_gpu_receipt",
        "source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
        "execution_config_sha256":M["canonical"](config),"resources":{"teacher":{"verified":True,
            "public_id":M["TEACHER_ID"],"revision":M["TEACHER_REVISION"],"file_sha256":files}},
        "public_train_only_holdout":{"verified":True,"test_read":False}}
    return config,contract,audit


@pytest.mark.parametrize("field,value",[("max_tokens",1025),("train_examples",32),("hard_root_limit",8),
    ("teacher_attempts",3),("construction_json_schema","true"),("validation_examples",8)])
def test_original_caps_cannot_be_changed_even_with_rehashed_config(tmp_path,field,value):
    config,contract,audit=inputs(tmp_path)
    config["methods"]["magicbeanstalk"][field]=value;audit["execution_config_sha256"]=M["canonical"](config)
    with pytest.raises(ValueError):M["validate_core"](tmp_path,config,contract,audit,
        expected_config_sha256=M["canonical"](config))


def test_nonfinite_partial_evidence_is_json_safe_and_failed():
    result=M["finite_evidence"]({"measurement":float("nan")})
    assert result["measurement"] is None and result["diagnostic_outputs_usable"] is False
    json.dumps(result,allow_nan=False)


def test_wrong_runner_root_or_unbound_digest_cannot_execute(tmp_path):
    p=tmp_path/"scripts/diagnose_oct14_mbs_teacher_quality.py";p.parent.mkdir();p.write_text("CPU-only runner")
    contract={"source_commit":"a"*40,"source_file_sha256":{str(p.relative_to(tmp_path)):M["digest"](p)}}
    (tmp_path/".source-commit").write_text(contract["source_commit"]+"\n")
    audit={**contract,"artifact_kind":"read_only_cpu_resource_audit_not_gpu_receipt",
        "source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
        "execution_config_sha256":M["CONFIG_SHA"]}
    M["verify_runner"](tmp_path,contract,audit,runner_path=p)
    with pytest.raises(ValueError):M["verify_runner"](tmp_path,contract,audit,runner_path=Path(__file__))
    contract["source_file_sha256"][str(p.relative_to(tmp_path))]="0"*64
    with pytest.raises(ValueError):M["verify_runner"](tmp_path,contract,audit,runner_path=p)


def test_completed_responses_and_pending_attempt_are_on_disk_before_finally(tmp_path):
    evidence={}
    with pytest.raises(RuntimeError):
        M["diagnose_quality"]({},*rows(),OPS,evidence,policy=Policy(crash_at=2),partial_output=tmp_path/"partial")
    completed=json.loads((tmp_path/"partial/01-completed.json").read_text())
    pending=json.loads((tmp_path/"partial/02-started.json").read_text())
    assert completed["response_audits"][0]["response_text"]=="\\boxed{72}"
    assert pending["generation_attempts"][1]["completed"] is False
    assert pending["unreturned_generation_cost_measured"] is False
    assert completed["diagnostic_outputs_usable"] is False


def test_actual_teacher_bytes_are_rechecked_not_only_old_audit_claim(tmp_path):
    config,contract,audit=inputs(tmp_path)
    (tmp_path/"teacher/config.json").write_text("changed bytes")
    with pytest.raises(ValueError,match="bytes"):
        M["validate_core"](tmp_path,config,contract,audit,expected_config_sha256=M["canonical"](config))


@pytest.mark.parametrize("field,value",[("source_commit","b"*40),("source_hashes_verified",False),
    ("cuda_initialized",True),("model_instantiated",True),("execution_config_sha256","0"*64)])
def test_runner_cpu_audit_must_match_frozen_marker_and_actual_bytes(tmp_path,field,value):
    p=tmp_path/M["RUNNER"];p.parent.mkdir();p.write_text("CPU-only marker")
    contract={"source_commit":"a"*40,"source_file_sha256":{M["RUNNER"]:M["digest"](p)}}
    (tmp_path/".source-commit").write_text(contract["source_commit"]+"\n")
    audit={**contract,"artifact_kind":"read_only_cpu_resource_audit_not_gpu_receipt",
        "source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
        "execution_config_sha256":M["CONFIG_SHA"]};audit[field]=value
    with pytest.raises(ValueError):M["verify_runner"](tmp_path,contract,audit,runner_path=p)


def partitions(tmp_path,monkeypatch):
    train,validation=rows()
    hashes={}
    for name,data in (("train",train),("validation",validation)):
        p=tmp_path/(name+".jsonl");p.write_text("\n".join(json.dumps(x) for x in data)+"\n")
        hashes[name]=M["digest"](p)
    manifest={"source_split":"train","test_opened":False,"source_revision":"fixed-public",
        "partition_sha256":hashes,"counts":{"train":16,"validation":4}}
    p=tmp_path/"split.json";p.write_text(json.dumps(manifest))
    c={"split_manifest":str(p),"train_path":str(tmp_path/"train.jsonl"),"validation_path":str(tmp_path/"validation.jsonl"),
        "test_path":str(tmp_path/"TEST-MUST-NOT-OPEN"),"dataset_revision":"fixed-public"}
    audit={"public_train_only_holdout":{"partition_sha256":hashes}}
    monkeypatch.setitem(M["read_partitions"].__globals__,"ROOT_HASHES",
        {i:hashlib.sha256(train[i]["question"].encode()).hexdigest() for i in (4,7,8)})
    return c,audit,M["digest"](p)


def test_exact_train_validation_prefixes_opened_but_never_test(tmp_path,monkeypatch):
    c,audit,sha=partitions(tmp_path,monkeypatch)
    train,validation,proof=M["read_partitions"](c,audit,expected_manifest_sha=sha)
    assert (len(train),len(validation))==(16,4)
    assert proof["validation_content_read"] is True and proof["test_content_read"] is False
    assert proof["target_hardness_recalibrated"] is False


@pytest.mark.parametrize("case",["train-bytes","val-bytes","manifest","revision","root"])
def test_partition_drift_or_changed_root_cannot_be_selected(tmp_path,monkeypatch,case):
    c,audit,sha=partitions(tmp_path,monkeypatch)
    if case=="train-bytes":(tmp_path/"train.jsonl").write_text("changed")
    elif case=="val-bytes":(tmp_path/"validation.jsonl").write_text("changed")
    elif case=="manifest":sha="0"*64
    elif case=="revision":c["dataset_revision"]="other"
    else:monkeypatch.setitem(M["read_partitions"].__globals__,"ROOT_HASHES",{4:"0"*64})
    with pytest.raises(ValueError):M["read_partitions"](c,audit,expected_manifest_sha=sha)


def overlay(tmp_path):
    packages={}
    for name,version in M["DEPENDENCIES"].items():
        module=name.replace("-","_")+".py";p=tmp_path/module;p.write_text("# CPU fixture, not imported\n")
        info=tmp_path/(name.replace("-","_")+"-"+version+".dist-info");info.mkdir()
        (info/"METADATA").write_text("Metadata-Version: 2.1\nName: "+name+"\nVersion: "+version+"\n")
        files={module:M["digest"](p),str((info/"METADATA").relative_to(tmp_path)):M["digest"](info/"METADATA")}
        packages[name]={"version":version,"package_file_sha256":files}
    return {"overlay_root":str(tmp_path),"cuda_initialized":False,"model_instantiated_by_audit":False,
        "dependency_modules_imported_by_audit":False,"packages":packages,"dependency_fingerprint":M["canonical"](packages)}


def test_overlay_versions_and_package_bytes_are_rechecked_without_import(tmp_path,monkeypatch):
    monkeypatch.setattr(sys,"path",list(sys.path))
    audit=overlay(tmp_path)
    assert M["validate_dependencies"](tmp_path,audit)==audit


@pytest.mark.parametrize("case",["version","bytes","fingerprint","cuda"])
def test_overlay_drift_cannot_be_accepted(tmp_path,case):
    audit=overlay(tmp_path)
    if case=="version":(tmp_path/"xgrammar-0.2.8.dist-info/METADATA").write_text("Name: xgrammar\nVersion: 0.2.9\n")
    elif case=="bytes":(tmp_path/"xgrammar.py").write_text("changed")
    elif case=="fingerprint":audit["dependency_fingerprint"]="0"*64
    else:audit["cuda_initialized"]=True
    with pytest.raises(ValueError):M["validate_dependencies"](tmp_path,audit)


def test_only_one_teacher_loader_is_called_and_no_student_is_instantiated():
    calls=[]
    def loader(config,*,role,seed):calls.append((role,seed));return Policy()
    ops=SimpleNamespace(**vars(OPS),load_policy=loader)
    e={};M["diagnose_quality"]({},*rows(),ops,e)
    assert calls==[("teacher",42)] and e["actual_output_count"]==14
    assert e["student_instantiated"] is False and e["optimizer_updates"]==0


@pytest.mark.parametrize("execute",[False,True])
def test_cli_print_only_or_missing_grant_never_reads_or_loads_models(execute):
    args=[sys.executable,str(ROOT/M["RUNNER"])]
    for name in ("config","algorithm-root","algorithm-contract","algorithm-audit","source-root","contract","audit",
        "overlay-root","dependency-audit","output"):args.extend(["--"+name,"missing-"+name])
    if execute:args.append("--execute")
    result=subprocess.run(args,text=True,capture_output=True,check=False)
    if execute:assert result.returncode!=0 and "new explicit" in result.stderr
    else:assert result.returncode==0 and '"planned_only": true' in result.stdout


def test_new_runner_cannot_claim_old_algorithm_commit_even_with_matching_fake_audit(tmp_path):
    p=tmp_path/M["RUNNER"];p.parent.mkdir();p.write_text("CPU-only new marker")
    contract={"source_commit":M["ALGORITHM_COMMIT"],"source_file_sha256":{M["RUNNER"]:M["digest"](p)}}
    (tmp_path/".source-commit").write_text(contract["source_commit"]+"\n")
    audit={**contract,"artifact_kind":"read_only_cpu_resource_audit_not_gpu_receipt","source_hashes_verified":True,
        "cuda_initialized":False,"model_instantiated":False,"execution_config_sha256":M["CONFIG_SHA"]}
    with pytest.raises(ValueError):M["verify_runner"](tmp_path,contract,audit,runner_path=p)


@pytest.mark.parametrize("role,case",[(r,c) for r in ("runner","algorithm") for c in ("missing","drift")])
def test_both_immutable_root_markers_are_read_and_must_match_exact_commits(tmp_path,role,case):
    if role=="algorithm":
        config,contract,audit=inputs(tmp_path)
        call=lambda:M["validate_core"](tmp_path,config,contract,audit,expected_config_sha256=M["canonical"](config))
    else:
        p=tmp_path/M["RUNNER"];p.parent.mkdir();p.write_text("CPU-only marker guard")
        contract={"source_commit":"a"*40,"source_file_sha256":{M["RUNNER"]:M["digest"](p)}}
        audit={**contract,"artifact_kind":"read_only_cpu_resource_audit_not_gpu_receipt","source_hashes_verified":True,
            "cuda_initialized":False,"model_instantiated":False,"execution_config_sha256":M["CONFIG_SHA"]}
        (tmp_path/".source-commit").write_text(contract["source_commit"]+"\n")
        call=lambda:M["verify_runner"](tmp_path,contract,audit,runner_path=p)
    marker=tmp_path/".source-commit"
    if case=="missing":marker.unlink()
    else:marker.write_text("0"*40+"\n")
    with pytest.raises(ValueError,match="marker"):call()
