"""L0 backend/binding tests only; no GPU or bit-exact equivalence claim."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch

from auto_research.agent_research.oct12_checkpoint import CheckpointPolicy
from auto_research.agent_research import oct12_entrypoint as entry


@pytest.mark.parametrize("backend",["eager","sdpa"])
def test_real_transformers_load_binding_receives_explicit_attention_backend(monkeypatch,backend):
    from transformers import AutoModelForCausalLM,AutoTokenizer,Qwen2Config,Qwen2ForCausalLM
    calls=[]
    def load(checkpoint,**kwargs):
        calls.append((checkpoint,kwargs))
        config=Qwen2Config(vocab_size=128,hidden_size=32,intermediate_size=64,
            num_hidden_layers=2,num_attention_heads=4,num_key_value_heads=2,attention_dropout=0.)
        config._attn_implementation=kwargs["attn_implementation"]
        return Qwen2ForCausalLM(config)  # genuine tiny model, random L0 weights
    monkeypatch.setattr(AutoModelForCausalLM,"from_pretrained",load)
    monkeypatch.setattr(AutoTokenizer,"from_pretrained",lambda *args,**kwargs:SimpleNamespace())
    policy=CheckpointPolicy("L0-no-download",device="cpu",attention_backend=backend)
    assert calls[0][1]["attn_implementation"]==backend
    assert calls[0][1]["local_files_only"] and calls[0][1]["trust_remote_code"] is False
    assert calls[0][1]["use_safetensors"] and policy.attention_backend==backend
    logits=policy.model(torch.tensor([[1,2,3]]),use_cache=False).logits
    assert logits.shape==(1,3,128) and torch.isfinite(logits).all()


def test_backend_invalid_is_rejected_before_checkpoint_load():
    with pytest.raises(ValueError,match="eager or sdpa"):
        CheckpointPolicy("L0-no-download",attention_backend="flash_attention_2")
    with pytest.raises(ValueError,match="eager or sdpa"):
        entry.run_method("janus",attention_backend="automatic")


def cli_module():
    path=Path(__file__).resolve().parents[1]/"scripts/run_oct12_agents.py"
    spec=importlib.util.spec_from_file_location("oct12_attention_cli_fixture",path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("explicit,expected",[(None,"eager"),("sdpa","sdpa")])
def test_cli_eager_default_and_explicit_sdpa_forwarding(tmp_path,monkeypatch,explicit,expected):
    module=cli_module();calls=[]
    monkeypatch.setattr(module,"run_method",lambda **kwargs:
        (calls.append(kwargs) or {"status":"L0-fixture-only","diagnostic_only":True}))
    args=["run_oct12_agents.py","--method","janus","--output",str(tmp_path/"l0-only.json")]
    if explicit:args.extend(["--attention-backend",explicit])
    monkeypatch.setattr("sys.argv",args)
    module.main()
    assert calls[0]["attention_backend"]==expected


def test_cli_invalid_backend_never_calls_runtime(tmp_path,monkeypatch):
    module=cli_module()
    def no_runtime(**kwargs):raise AssertionError("invalid CLI backend reached runtime")
    monkeypatch.setattr(module,"run_method",no_runtime)
    monkeypatch.setattr("sys.argv",["run_oct12_agents.py","--method","janus","--output",
        str(tmp_path/"l0-only.json"),"--attention-backend","automatic"])
    with pytest.raises(SystemExit) as error:module.main()
    assert error.value.code==2 and not (tmp_path/"l0-only.json").exists()


def test_janus_settings_forward_sdpa_and_record_loaded_backend_without_changing_budget(monkeypatch):
    loads=[]
    class BackendFixture:
        def __init__(self,path,**kwargs):
            loads.append(kwargs)
            self.attention_backend=kwargs["attention_backend"]
        def execute(self,*args):raise AssertionError("L0 fake controller never executes real trial")
    class ControllerFixture:
        def __init__(self,backend,execute,**kwargs):pass
        def run(self,**kwargs):return {"L0_requested_budget":kwargs}
    monkeypatch.setattr(entry,"JanusBackend",BackendFixture)
    monkeypatch.setattr(entry,"Janus",ControllerFixture)
    monkeypatch.setattr(entry,"ProgramSandbox",lambda:SimpleNamespace(
        evaluate_packing=lambda code:SimpleNamespace(score=0.,feedback="L0-only")))
    monkeypatch.setattr(entry,"verify_local_checkpoint",lambda *args:{"L0_only":True})
    result=entry.run_method("janus",checkpoint="L0-no-download",attention_backend="sdpa",
        rounds=2,group_size=3,max_tokens=1536)
    assert loads[0]["attention_backend"]=="sdpa" and loads[0]["max_tokens"]==1536
    assert result["attention_backend"]=="sdpa"
    assert result["L0_requested_budget"]=={"budget":2,"candidates":3}
    assert result["diagnostic_only"] and not result["capability_comparison"]
