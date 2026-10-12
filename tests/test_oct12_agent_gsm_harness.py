"""L0 fixtures only: split/gold/budget contracts, never capability evidence."""
import hashlib
import json
from pathlib import Path

import pytest
import torch

from auto_research.datasets import GSM8K_FILES, GSM8K_REVISION
from auto_research.agent_research.oct12_checkpoint import (
    Evo2Policy, GSMHarnessEvaluator, GSM_INITIAL_PROMPT, harness_source,
)
from auto_research.agent_research.oct12_evolution import HarnessNode
from auto_research.agent_research import oct12_entrypoint as entry


def holdout(root):
    # Fixture manifests emulate byte-binding, NOT actual public dataset runs.
    train = [{"question":"L0 training-only example","answer":"#### 8"}]
    validation = [{"question":"L0 question A","answer":"PRIVATE_GOLD_CANARY_A #### 12"},
                  {"question":"L0 question B","answer":"PRIVATE_GOLD_CANARY_B #### 7"}]
    for split,rows in (("train",train),("validation",validation)):
        (root/(split+".jsonl")).write_text("".join(json.dumps(r)+"\n" for r in rows))
    record = {"source_id":"openai/grade-school-math","source_revision":GSM8K_REVISION,
        "source_sha256":GSM8K_FILES["train.jsonl"],"source_split":"train","test_opened":False,
        "partition":"L0 synthetic split fixture","counts":{"train":1,"validation":2},
        "partition_sha256":{name:hashlib.sha256((root/(name+".jsonl")).read_bytes()).hexdigest()
                             for name in ("train","validation")}}
    (root/"split.json").write_text(json.dumps(record))
    return root/"validation.jsonl"


class PromptSandbox:
    def execute(self,code):
        assert code.startswith("import json\nPROMPT = ")
        # No host execution even in this fixture. Actual executor is Linux-only.
        return json.dumps({"prompt":"L0 mathematics prompt, no solution"}),"",0


class ExecutorFixture:
    def __init__(self,outputs=None,**kwargs):
        self.model = torch.nn.Linear(1,1)
        self.outputs = iter(outputs or ["Reasoning. \\boxed{12}","Incorrect. \\boxed{5}"])
        self.inputs = []
        self.max_tokens = kwargs.get("max_tokens",256)
        self.attention_backend = kwargs.get("attention_backend","eager")
    def generate(self,messages,sample=True):
        assert sample is False
        self.inputs.append(messages)
        return next(self.outputs)


def test_gsm_real_external_scorer_and_hash_only_feedback_never_expose_gold(tmp_path,monkeypatch):
    path=holdout(tmp_path)
    reads=[]
    original=Path.read_bytes
    def read_bytes(p):
        reads.append(p.name)
        assert p.name != "test.jsonl"
        return original(p)
    monkeypatch.setattr(Path,"read_bytes",read_bytes)
    original_text=Path.read_text
    def read_text(p,*args,**kwargs):
        reads.append(p.name)
        assert p.name != "test.jsonl"
        return original_text(p,*args,**kwargs)
    monkeypatch.setattr(Path,"read_text",read_text)
    executor=ExecutorFixture()
    evaluator=GSMHarnessEvaluator(executor,path,examples=2,sandbox=PromptSandbox())
    result=evaluator({"agent.py":harness_source(GSM_INITIAL_PROMPT)})
    assert result.score == .5 and result.valid and result.mechanism_ran
    assert {"train.jsonl","validation.jsonl","split.json"} <= set(reads)
    assert evaluator.dataset_provenance["verified"] and evaluator.dataset_provenance["test_read"] is False
    assert all(set(row)=={"question_sha256","correct","output_sha256"} for row in result.trace)
    assert "PRIVATE_GOLD_CANARY" not in json.dumps(executor.inputs) + json.dumps(result.trace)
    assert "Reasoning. \\boxed{12}" not in json.dumps(result.trace)
    assert evaluator.frozen_audit()=={"executor_calls":2,"executor_weights_unchanged":True}
    policy=Evo2Policy.__new__(Evo2Policy)
    messages_seen=[]
    def generate(messages,**kwargs):
        messages_seen.extend(messages)
        policy.last_truncated=False
        return "L0 prompt revision"
    policy.generate=generate
    policy.sample_choice=lambda messages,choices: (messages_seen.extend(messages) or "keep")
    node=HarnessNode("root",{"agent.py":harness_source(GSM_INITIAL_PROMPT)},result)
    policy.propose(node)
    policy.reflect(node,[])
    assert "PRIVATE_GOLD_CANARY" not in json.dumps(messages_seen)
    assert "L0 question A" not in json.dumps(messages_seen)  # proposer sees question hash only


@pytest.mark.parametrize("field,value",[("source_split","test"),("test_opened",True),
    ("source_revision","main"),("source_id","other/data"),("source_sha256","fake")])
def test_gsm_requires_official_fixed_revision_train_only_holdout(tmp_path,field,value):
    path=holdout(tmp_path);manifest=tmp_path/"split.json"
    row=json.loads(manifest.read_text());row[field]=value;manifest.write_text(json.dumps(row))
    with pytest.raises(ValueError):
        GSMHarnessEvaluator(ExecutorFixture(),path,examples=2,sandbox=PromptSandbox())


def test_gsm_rejects_digest_tampering_test_path_and_oversized_prefix(tmp_path):
    path=holdout(tmp_path)
    with pytest.raises(ValueError,match="validation.jsonl"):
        GSMHarnessEvaluator(ExecutorFixture(),tmp_path/"test.jsonl",examples=2,sandbox=PromptSandbox())
    with pytest.raises(ValueError,match="exceeds"):
        GSMHarnessEvaluator(ExecutorFixture(),path,examples=3,sandbox=PromptSandbox())
    path.write_text(path.read_text()+json.dumps({"question":"tampered","answer":"#### 1"})+"\n")
    with pytest.raises(ValueError,match="digest"):
        GSMHarnessEvaluator(ExecutorFixture(),path,examples=2,sandbox=PromptSandbox())


def test_invalid_harness_does_not_call_math_executor(tmp_path):
    class InvalidSandbox:
        def execute(self,code):return "not-json","",0
    executor=ExecutorFixture()
    evaluator=GSMHarnessEvaluator(executor,holdout(tmp_path),examples=2,sandbox=InvalidSandbox())
    result=evaluator({"agent.py":"L0 invalid harness"})
    assert not result.valid and not result.mechanism_ran and result.score==0.
    assert not executor.inputs and evaluator.calls==0


@pytest.mark.parametrize("method",[m for m in entry.METHODS if m!="evo2"])
def test_non_evo_rejects_gsm_environment_before_model_or_dataset_access(method):
    with pytest.raises(ValueError,match="only for Evo2"):
        entry.run_method(method,environment="gsm8k-harness")


@pytest.mark.parametrize("attention_backend",["eager","sdpa"])
def test_evo_gsm_entrypoint_preserves_active_gate_and_separate_executor_budget(tmp_path,monkeypatch,attention_backend):
    path=holdout(tmp_path);loads=[]
    def model(path,**kwargs):
        loads.append(kwargs)
        return ExecutorFixture(**kwargs)
    class ControllerFixture:
        def __init__(self,policy,evaluator,files,**kwargs):
            self.nodes=[HarnessNode("root",files,evaluator(files))]
        def train(self,**kwargs):
            return {"warmup":{"parameters_changed":True,"steps":[{"gradient_norm":1.}]},
                "training":[{"updated":True,"parameters_changed":True,"gradient_norm":1.}]}
    original=GSMHarnessEvaluator
    monkeypatch.setattr(entry,"GSMHarnessEvaluator",lambda *args,**kwargs:
        original(*args,**kwargs,sandbox=PromptSandbox()))
    monkeypatch.setattr(entry,"CheckpointPolicy",model)
    monkeypatch.setattr(entry,"Evo2Policy",model)
    monkeypatch.setattr(entry,"Evo2",ControllerFixture)
    monkeypatch.setattr(entry,"verify_local_checkpoint",lambda *args:{"verified_fixture_only":True})
    result=entry.run_method("evo2",checkpoint="L0-only",environment="gsm8k-harness",dataset=path,
                            evaluation_examples=2,max_tokens=768,executor_max_tokens=256,
                            attention_backend=attention_backend)
    assert [row["max_tokens"] for row in loads]==[768,256]
    assert [row["attention_backend"] for row in loads]==[attention_backend,attention_backend]
    assert result["attention_backend"]==result["executor_attention_backend"]==attention_backend
    assert result["environment"]=="gsm8k-harness" and result["evaluation_examples"]==2
    assert result["policy_max_tokens"]==768 and result["executor_max_tokens"]==256
    assert result["scores"][0]["normalized_score"]==.5 and result["diagnostic_only"]
    assert not result["capability_comparison"] and "PRIVATE_GOLD_CANARY" not in json.dumps(result)
