"""CPU contract fixtures for the frozen format probe, never capability evidence."""
import ast
import hashlib
import json
from pathlib import Path
import runpy

import pytest
import torch

from auto_research.post_training.oct13_common import CostLedger
from auto_research.post_training.response_policy import GeneratedResponse
from auto_research.reproductions.soar.algorithm import LexicalRetriever
from auto_research.reproductions.soar.checkpoint import SYSTEM

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/diagnose_oct14_soar_format.py"


def namespace(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT/"scripts"))
    return runpy.run_path(str(SCRIPT))


class Policy:
    def __init__(self,invalid=False,truncated=False):
        self.model=torch.nn.Linear(2,2).requires_grad_(False)
        self.provenance={"public_id":"fixture","revision":"fixture-v1"}
        self.messages=[]
        self.invalid=invalid
        self.truncated=truncated
    def generate(self,messages,*,samples,max_tokens,sample):
        assert samples==1 and max_tokens==256 and sample is True
        assert "PRIVATE_GOLD" not in str(messages)
        self.messages.append(messages)
        if messages[0]["role"]=="system" and messages[0]["content"]!=SYSTEM:
            assert len(messages)==2 and messages[-1]["content"]=="public tool"
            text="1. Public internal fact."
        elif self.invalid:
            text="not the required format"
        elif len(messages)==2:
            assert messages[0]["content"]==SYSTEM
            text="<think>retrieve</think><search>public tool</search>"
        else:
            assert "external:" in messages[-1]["content"]
            text="<information_source>external</information_source><answer>AttributeOne</answer>"
        return [GeneratedResponse((1,2,3),text,self.truncated)]
    def prepare_lora(self,**_kwargs):
        raise AssertionError("no LoRA allowed")


def retriever():
    return LexicalRetriever([{"text":"public tool attribute AttributeOne", "source_url":"https://example.org/public"}])


@pytest.mark.parametrize("invalid,truncated",[(False,False),(True,False),(False,True)])
def test_eight_episodes_original_system_caps_and_external_gold_role(monkeypatch,invalid,truncated):
    n=namespace(monkeypatch)
    f=n["diagnose_format"]
    policy=Policy(invalid=invalid,truncated=truncated)
    def load(_config,*,role,seed):
        assert role=="teacher" and seed==42
        return policy
    monkeypatch.setitem(f.__globals__,"load_policy",load)
    ledger=CostLedger()
    result={"whole_method_gpu_validation_passed":False,"validation_content_read":False}
    f({},[{"question":"public question","answer":"AttributeOne"}]*4,retriever(),ledger,result)
    assert len(result["training_episode_audits"])==8
    assert result["optimizer_updates"]==result["lora_updates"]==0 and result["assessment_executed"] is False
    assert result["whole_method_gpu_validation_passed"] is False and result["validation_content_read"] is False
    assert result["original_system_sha256"]==hashlib.sha256(SYSTEM.encode()).hexdigest()
    assert sum(ledger.generated_tokens.values())<=12288
    if invalid or truncated:
        assert result["valid_format_episodes"]==0 and result["source_match_episodes"]==0
    else:
        assert result["valid_format_episodes"]==result["source_match_episodes"]==8
        assert ledger.calls=={"policy_trajectory":16,"isolated_internal_recall":8}
        assert all(x["source_consistent_reward"]==x["without_source_reward"]==1. for x in result["training_episode_audits"])


def test_gold_marker_is_never_seen_by_policy_recall_or_retriever(monkeypatch):
    n=namespace(monkeypatch)
    f=n["diagnose_format"]
    policy=Policy()
    monkeypatch.setitem(f.__globals__,"load_policy",lambda *_args,**_kwargs:policy)
    ledger=CostLedger()
    result={}
    f({},[{"question":"public question","answer":"PRIVATE_GOLD"}]*4,retriever(),ledger,result)
    assert all(x["answer"]==0. for x in result["training_episode_audits"])
    assert all(x["format"]==x["source_match"]==1. for x in result["training_episode_audits"])
    assert all("PRIVATE_GOLD" not in str(m) for m in policy.messages)


def test_exact_three_turn_cap_no_forced_answer(monkeypatch):
    n=namespace(monkeypatch)
    class SearchOnly(Policy):
        def generate(self,messages,*,samples,max_tokens,sample):
            assert max_tokens==256 and samples==1
            return [GeneratedResponse((1,2,3),"<search>public tool</search>",False)]
    ledger=CostLedger()
    final,_,_,searches,turns=n["episode"](SearchOnly(),retriever(),"question",ledger)
    assert final["kind"]=="invalid" and searches==3 and len(turns)==3
    assert ledger.calls=={"policy_trajectory":3,"isolated_internal_recall":3}


def input_fixture(tmp_path,n):
    root=tmp_path/"source"
    root.mkdir()
    (root/"fixture.py").write_text("immutable fixture")
    train=tmp_path/"train.jsonl"
    train.write_text("\n".join(json.dumps({"question":str(i),"answer":"PRIVATE_GOLD"}) for i in range(8))+"\n")
    manifest=tmp_path/"split.json"
    record={"source_split":"train","test_opened":False,"source_revision":"fixture-v1",
        "partition_sha256":{"train":hashlib.sha256(train.read_bytes()).hexdigest(),"validation":"a"*64},
        "counts":{"train":8,"validation":4}}
    manifest.write_text(json.dumps(record))
    config={"shared":{"teacher_id":n["POLICY_ID"],"teacher_revision":n["POLICY_REVISION"]},
        "methods":{"soar":{"train_examples":8,"max_tokens":256,"max_turns":3,"verifier":"normalized-em",
            "split_manifest":str(manifest),"train_path":str(train),"validation_path":str(tmp_path/"NEVER_READ"),
            "dataset_revision":"fixture-v1","corpus_path":str(tmp_path/"kb"),"corpus_id":"fixture-public", "corpus_revision":"fixture-v1"}}}
    contract={"source_commit":"b"*40,"source_file_sha256":{"fixture.py":hashlib.sha256((root/"fixture.py").read_bytes()).hexdigest()}}
    audit={"source_commit":contract["source_commit"],"source_file_sha256":contract["source_file_sha256"],
        "source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
        "execution_config_sha256":hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest(),
        "resources":{"teacher":{"public_id":n["POLICY_ID"],"revision":n["POLICY_REVISION"],"verified":True}},
        "method_specific_holdouts":{"soar":{"status":"verified","tool_groups_disjoint":True,
            "holdout":{"partition_sha256":record["partition_sha256"]}}},
        "soar_corpus":{"status":"verified","generation_inputs_do_not_include_qa_answers":True,"file_sha256":{"documents.jsonl":"c"*64}}}
    return root,config,contract,audit,hashlib.sha256(manifest.read_bytes()).hexdigest()


def test_probe_reads_exact_train_and_presealed_kb_never_validation(tmp_path,monkeypatch):
    n=namespace(monkeypatch)
    args=input_fixture(tmp_path,n)
    f=n["validate_probe_inputs"]
    def mirror(_path,_file,_id,_revision,_split):
        return [{"text":"public tool attribute", "source_url":"https://example.org/public"}],{
            "files":{"documents.jsonl":"c"*64},"public_id":"fixture-public","revision":"fixture-v1"}
    monkeypatch.setitem(f.__globals__,"read_jsonl_mirror",mirror)
    _,rows,_,dataset=f(*args[:4],manifest_sha256=args[4])
    assert len(rows)==4 and dataset["validation_content_read"] is False
    assert dataset["test_content_read"] is False


@pytest.mark.parametrize("case",["model","caps","train","audit","manifest","kb-labels"])
def test_changed_model_budget_data_or_gold_kb_rejected(tmp_path,monkeypatch,case):
    n=namespace(monkeypatch)
    root,c,contract,audit,sha=input_fixture(tmp_path,n)
    if case=="model":c["shared"]["teacher_revision"]="other"
    elif case=="caps":c["methods"]["soar"]["max_tokens"]=257
    elif case=="train":Path(c["methods"]["soar"]["train_path"]).write_text("changed")
    elif case=="audit":audit["cuda_initialized"]=True
    elif case=="manifest":sha="d"*64
    audit["execution_config_sha256"]=hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest()
    f=n["validate_probe_inputs"]
    monkeypatch.setitem(f.__globals__,"read_jsonl_mirror",lambda *_args:([
        {"text":"public text","source_url":"https://example.org/public","gold":"PRIVATE_GOLD"}],
        {"files":{"documents.jsonl":"c"*64},"public_id":"fixture-public","revision":"fixture-v1"}))
    with pytest.raises(ValueError):f(root,c,contract,audit,manifest_sha256=sha)


def test_no_rl_sft_evaluation_calls_and_original_helpers_reused(monkeypatch):
    tree=ast.parse(SCRIPT.read_text())
    forbidden={"evaluate","assess","load_split","prepare_lora","optimizer_step","policy_gradient_step","sft_step"}
    called={node.func.id if isinstance(node.func,ast.Name) else node.func.attr
        for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,(ast.Name,ast.Attribute))}
    assert not called&forbidden
    assert {"parse_step","source_reward","internal_messages","source_observation"}<=called
    assert namespace(monkeypatch)["CAPS"]["generated_response_tokens_upper"]==12288
