"""CPU-only fixtures for bounded diagnosis; not execution or GPU evidence."""
import ast
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
from types import SimpleNamespace

import pytest
import torch

from auto_research.post_training.oct13_common import CostLedger
from auto_research.post_training.response_policy import GeneratedResponse

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/diagnose_oct14_post_training.py"


def namespace():
    return runpy.run_path(str(SCRIPT))


def input_fixture(tmp_path,method="synthself"):
    source=tmp_path/"source"
    source.mkdir()
    (source/"fixture.py").write_text("immutable fixture")
    train=tmp_path/"train.jsonl"
    train.write_text("\n".join(json.dumps({"question":f"question{i}","answer":"gold secret #### 2"}) for i in range(8))+"\n")
    manifest=tmp_path/"split.json"
    record={"source_split":"train","test_opened":False,"source_revision":"fixture-v1",
        "partition_sha256":{"train":hashlib.sha256(train.read_bytes()).hexdigest(),"validation":"a"*64},
        "counts":{"train":8,"validation":1}}
    manifest.write_text(json.dumps(record))
    c={"shared":{"train_path":str(train),"validation_path":str(tmp_path/"NEVER_READ.jsonl"),
            "split_manifest":str(manifest),"dataset_revision":"fixture-v1"},
        "methods":{method:namespace()["CAPS"][method].copy()}}
    contract={"source_commit":"b"*40,"source_file_sha256":{"fixture.py":hashlib.sha256((source/"fixture.py").read_bytes()).hexdigest()}}
    audit={"source_commit":contract["source_commit"],"source_file_sha256":contract["source_file_sha256"],
        "source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
        "execution_config_sha256":hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest(),
        "public_train_only_holdout":{"verified":True,"test_read":False,"partition_sha256":record["partition_sha256"]}}
    return source,c,contract,audit,hashlib.sha256(manifest.read_bytes()).hexdigest()


def test_manifest_and_train_only_no_validation_or_test_reads(tmp_path,monkeypatch):
    args=input_fixture(tmp_path)
    original=Path.read_bytes
    def guarded(path,*a,**k):
        assert "NEVER_READ" not in str(path) and "test.jsonl" not in str(path)
        return original(path,*a,**k)
    monkeypatch.setattr(Path,"read_bytes",guarded)
    c,rows,data=namespace()["validate_inputs"](*args[:4],"synthself",manifest_sha256=args[4])
    assert len(rows)==8 and c["max_tokens"]==512
    assert data["validation_content_read"] is False and data["test_content_read"] is False


@pytest.mark.parametrize("case",["caps","train-hash","manifest-hash","audit-source","audit-config","test"])
def test_source_data_or_budget_mismatch_rejected(tmp_path,case):
    source,c,contract,audit,manifest_sha=input_fixture(tmp_path)
    if case=="caps":
        c["methods"]["synthself"]["max_tokens"]=513
        audit["execution_config_sha256"]=hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest()
    elif case=="train-hash":Path(c["shared"]["train_path"]).write_text("changed")
    elif case=="manifest-hash":manifest_sha="c"*64
    elif case=="audit-source":audit["source_commit"]="c"*40
    elif case=="audit-config":audit["execution_config_sha256"]="c"*64
    else:audit["public_train_only_holdout"]["test_read"]=True
    with pytest.raises(ValueError):namespace()["validate_inputs"](source,c,contract,audit,"synthself",manifest_sha256=manifest_sha)


class Tokenizer:
    eos_token_id=0
    def __call__(self,text,**_kwargs):
        assert "gold secret" in text
        return SimpleNamespace(input_ids=[1,2,3,4])


class Policy:
    def __init__(self,teacher=False,partial=False):
        self.model=torch.nn.Linear(4,4 if teacher else 2,bias=False).requires_grad_(False)
        self.tokenizer=Tokenizer()
        self.vocabulary_sha256="same"
        self.provenance={"public_id":"fixture","revision":"fixture-v1"}
        self.teacher=teacher
        self.partial=partial
    def generate(self,messages,*,samples,max_tokens,sample):
        assert max_tokens==512 and sample is False and samples==1
        assert "gold secret" in messages[0]["content"]  # explicit construction teacher/control only
        return [GeneratedResponse((1,2) if self.partial else (1,2,0),"\\boxed{2}" if self.teacher else "\\boxed{3}",self.partial)]
    def token_statistics(self,messages,tokens):
        assert "gold secret" not in messages[0]["content"]  # no gold in student scoring prompt
        return (torch.full((len(tokens),),-1.),None)
    def prepare_lora(self,**_kwargs):
        raise AssertionError("no LoRA or SFT allowed")


@pytest.mark.parametrize("partial",[False,True])
def test_synth_bounded_16_outputs_16_nll_no_sft_and_explicit_gold_roles(monkeypatch,partial):
    n=namespace()
    function=n["diagnose_synthself"]
    monkeypatch.setitem(function.__globals__,"load_policy",lambda _config,role="student",**_kwargs:Policy(role=="teacher",partial=partial))
    rows=[{"question":"question","answer":"gold secret #### 2"} for _ in range(8)]
    ledger=CostLedger()
    result={"whole_method_gpu_validation_passed":False,"validation_content_read":False}
    function({"student_id":"Qwen/fixture-small","teacher_id":"Qwen/fixture-big"},rows,ledger,result)
    assert ledger.calls=={"offline_aligner":8,"construction_self_rewrite":8}
    assert len(result["training_rewrite_audits"])==8
    assert ledger.scored_tokens["gold_sequence_nll"]==40
    assert result["sft_executed"] is False and result["lora_updates"]==0
    assert result["whole_method_gpu_validation_passed"] is False
    constraints=result["empirical_aligner_constraints"]
    if partial:
        assert constraints["rewrite_sequence_nll"] is None and not constraints["strict_eq6_satisfied"]
        assert all(x["rewrite_scored_tokens"]==2 and not x["rewrite_canonical_eos_appended"] for x in result["training_rewrite_audits"])
        assert constraints["aligner_quality"]==constraints["self_quality"]==0.
    else:
        assert constraints["strict_eq6_satisfied"] and constraints["gold_sequence_nll"]==5.
        assert constraints["rewrite_sequence_nll"]==3.  # sum, not token mean


def test_upturn_exact_32_training_rollouts_no_eval_no_gold_in_policy(monkeypatch):
    n=namespace()
    function=n["diagnose_upturn"]
    class Reasoner(Policy):
        device="cpu"
        def __init__(self):
            super().__init__()
            self.model.config=SimpleNamespace(hidden_size=4)
        def generate(self,messages,*,samples,max_tokens,sample):
            assert "gold secret" not in str(messages)
            assert samples==4 and max_tokens==768
            return [GeneratedResponse((1,2,0),"\\boxed{2}",False) for _ in range(samples)]
        def prompt_ids(self,messages):
            assert "gold secret" not in str(messages)
            return torch.zeros((1,2),dtype=torch.long)
    monkeypatch.setitem(function.__globals__,"load_policy",lambda *_args,**_kwargs:Reasoner())
    monkeypatch.setitem(function.__globals__,"causal_response_features",lambda *_args,**_kwargs:torch.zeros(3,4))
    monkeypatch.setitem(function.__globals__,"boxed_token_position",lambda *_args:1)
    monkeypatch.setitem(function.__globals__,"paragraph_prefixes",lambda *_args,**_kwargs:[1,2])
    ledger=CostLedger()
    result={"whole_method_gpu_validation_passed":False}
    function({},[{"question":"question","answer":"gold secret #### 2"} for _ in range(8)],ledger,result)
    assert ledger.calls=={"frozen_reasoner_training":8} and ledger.encoder_calls==32
    assert len(result["training_rollout_audits"])==32 and result["eligible_failed_rollouts"]==0
    assert result["diagnosis_status"]=="insufficient-gate-data-or-eligible-rollouts"
    assert result["lora_updates"]==0 and result["whole_method_gpu_validation_passed"] is False


def test_upturn_gate20_and_zero_rescue_stops_without_budget_expansion(monkeypatch):
    n=namespace()
    function=n["diagnose_upturn"]
    class Reasoner(Policy):
        device="cpu"
        def __init__(self):
            super().__init__()
            self.model.config=SimpleNamespace(hidden_size=4)
        def generate(self,messages,*,samples,max_tokens,sample):
            assert "gold secret" not in str(messages) and samples==4 and max_tokens==768
            return [GeneratedResponse((1,2,0),"\\boxed{3}",False) for _ in range(samples)]
        def prompt_ids(self,messages):
            return torch.zeros((1,2),dtype=torch.long)
    monkeypatch.setitem(function.__globals__,"load_policy",lambda *_args,**_kwargs:Reasoner())
    monkeypatch.setitem(function.__globals__,"causal_response_features",lambda *_args,**_kwargs:torch.arange(12).reshape(3,4).float())
    monkeypatch.setitem(function.__globals__,"boxed_token_position",lambda *_args:1)
    monkeypatch.setitem(function.__globals__,"paragraph_prefixes",lambda *_args,**_kwargs:[1,2])
    monkeypatch.setitem(function.__globals__,"intervention_prefix_tokens",lambda _p,_m,tokens:tuple(tokens)+(99,))
    def rescue(_policy,messages,prefix,ledger,*,role,samples,max_tokens):
        assert "gold secret" not in str(messages) and prefix[-1]==99 and samples==2 and 0<max_tokens<768
        ledger.calls[role]=ledger.calls.get(role,0)+1
        ledger.generated_tokens[role]=ledger.generated_tokens.get(role,0)+6
        return [GeneratedResponse((1,2,0),"\\boxed{3}",False)]*2
    monkeypatch.setitem(function.__globals__,"sample_prefix",rescue)
    ledger=CostLedger()
    result={"whole_method_gpu_validation_passed":False}
    function({},[{"question":"question","answer":"gold secret #### 2"} for _ in range(8)],ledger,result)
    assert len(result["gate_training_bce"])==20
    assert len(result["position_training"])==1 and result["position_informative_groups"]==0
    assert result["diagnosis_status"]=="no-rescue-signal" and result["whole_method_gpu_validation_passed"] is False
    assert ledger.encoder_calls==32 and ledger.calls["position_rescue_training"]<=4


def test_cli_default_is_print_only_and_execute_requires_fresh_grant(tmp_path):
    args=[sys.executable,str(SCRIPT),"--method","synthself","--config","missing.json","--contract","missing.json",
          "--audit","missing.json","--source-root",str(ROOT),"--output",str(tmp_path/"unused")]
    default=subprocess.run(args,check=False,capture_output=True,text=True,cwd=ROOT)
    assert default.returncode==0 and json.loads(default.stdout)["planned_only"] is True
    blocked=subprocess.run(args+["--execute"],check=False,capture_output=True,text=True,cwd=ROOT)
    assert blocked.returncode!=0 and "fresh main-agent A100 diagnostic slot" in blocked.stderr
    assert not (tmp_path/"unused").exists()


def test_diagnosis_source_never_calls_evaluation_or_lora():
    tree=ast.parse(SCRIPT.read_text())
    forbidden={"evaluate","assess","sft_step","prepare_lora","install_lora","load_split"}
    called={node.func.id if isinstance(node.func,ast.Name) else node.func.attr
        for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,(ast.Name,ast.Attribute))}
    assert not called&forbidden
    assert namespace()["CAPS"]["upturn"]=={"train_examples":8,"group":4,"max_tokens":768,
        "gate_epochs":20,"steps":2,"cuts":4,"suffixes":2,"max_cuts":16}


def test_unfrozen_backbone_is_rejected():
    policy=Policy()
    policy.model.requires_grad_(True)
    with pytest.raises(ValueError,match="no LoRA"):
        namespace()["ensure_frozen"](policy)


@pytest.mark.parametrize("case",["wrong-root","unbound","wrong-hash","correct"])
def test_execution_entrypoint_must_be_inside_frozen_root_and_contract(tmp_path,case):
    source=tmp_path/"source"
    (source/"scripts").mkdir(parents=True)
    runner=source/"scripts/diagnose_oct14_post_training.py"
    runner.write_text("synthetic fixture, not the real runner")
    contract={"source_file_sha256":{"scripts/diagnose_oct14_post_training.py":hashlib.sha256(runner.read_bytes()).hexdigest()}}
    if case=="wrong-root":source=tmp_path/"other"
    elif case=="unbound":contract["source_file_sha256"]={}
    elif case=="wrong-hash":contract["source_file_sha256"]["scripts/diagnose_oct14_post_training.py"]="f"*64
    if case=="correct":namespace()["verify_runner_binding"](source,contract,runner_path=runner)
    else:
        with pytest.raises(ValueError):namespace()["verify_runner_binding"](source,contract,runner_path=runner)


def test_nonfinite_nll_or_gradient_never_serialized_as_usable_nan():
    raw={"diagnosis_status":"selection-signal-observed","whole_method_gpu_validation_passed":False,
        "training_rewrite_audits":[{"gold_sequence_nll":float("nan"),"rewrite_sequence_nll":float("inf")}],
        "position_training":[{"gradient_l2_norm":float("-inf")}],
        "nonfinite_gradient_detected":True,
        "nonfinite_gradient_paths":[{"json_path":"$.position_training[0].gradients","value_class":"nonfinite-gradient"}]}
    clean=namespace()["strict_finite_evidence"](raw)
    assert clean["diagnosis_status"]=="diagnostic-failed-nonfinite-output" and clean["diagnostic_outputs_usable"] is False
    assert len(clean["nonfinite_metric_paths"])==4
    assert clean["training_rewrite_audits"][0]["gold_sequence_nll"] is None
    assert clean["whole_method_gpu_validation_passed"] is False
    serialized=json.dumps(clean,allow_nan=False)
    assert ": NaN" not in serialized and ": Infinity" not in serialized
