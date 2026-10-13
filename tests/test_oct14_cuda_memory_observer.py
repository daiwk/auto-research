"""CPU observer fixtures; synthetic counters are never GPU evidence."""
import json
import hashlib
from pathlib import Path
import runpy
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]


class MemoryFixture:
    def __init__(self,fail=False):
        self.calls=[]
        self.fail=fail
    def reset_peak_memory_stats(self):self.calls.append("reset")
    def synchronize(self):
        self.calls.append("synchronize")
        if self.fail:raise RuntimeError("synthetic unavailable counter")
    def max_memory_allocated(self):return 1234
    def max_memory_reserved(self):return 5678
    def get_device_name(self):return "CPU-only counter fixture, not a GPU"


@pytest.mark.parametrize("code",[0,1,124])
def test_original_argv_forwarded_and_finally_reads_actual_api_counters(tmp_path,code):
    observe=runpy.run_path(str(ROOT/"scripts/observe_oct14_cuda_memory.py"))["observe"]
    previous=list(sys.argv)
    memory=MemoryFixture()
    arguments=["--method","grpo-difficulty-curriculum","--seed","43"]
    def entry(path,*,run_name):
        assert run_name=="__main__" and sys.argv==[path,*arguments]
        assert memory.calls==["reset"]
        raise SystemExit(code)
    output=tmp_path/"memory.json"
    assert observe(tmp_path/"original.py",arguments,output,{"core_commit":"fixture"},cuda=memory,entry_runner=entry)==code
    assert sys.argv==previous
    result=json.loads(output.read_text())
    assert result["actual_max_memory_allocated_bytes"]==1234 and result["actual_max_memory_reserved_bytes"]==5678
    assert result["core_exit_code"]==code and result["not_gpu_receipt"] is True
    assert result["peak_memory_available"] is True and memory.calls==["reset","synchronize"]


def test_no_fake_peak_if_observation_fails(tmp_path):
    observe=runpy.run_path(str(ROOT/"scripts/observe_oct14_cuda_memory.py"))["observe"]
    output=tmp_path/"memory.json"
    observe(tmp_path/"original.py",[],output,{},cuda=MemoryFixture(fail=True),entry_runner=lambda *_a,**_k:None)
    result=json.loads(output.read_text())
    assert result["peak_memory_available"] is False
    assert "actual_max_memory_reserved_bytes" not in result


def test_unexpected_core_exception_still_observed_and_propagated(tmp_path):
    observe=runpy.run_path(str(ROOT/"scripts/observe_oct14_cuda_memory.py"))["observe"]
    def entry(*_args,**_kwargs):raise ValueError("synthetic core error")
    output=tmp_path/"memory.json"
    with pytest.raises(ValueError):observe(tmp_path/"original.py",[],output,{},cuda=MemoryFixture(),entry_runner=entry)
    assert json.loads(output.read_text())["core_exit_code"]==1


@pytest.mark.parametrize("case",["valid","source","config","seed","override"])
def test_original_source_config_and_no_added_training_overrides(tmp_path,case):
    n=runpy.run_path(str(ROOT/"scripts/observe_oct14_cuda_memory.py"))
    root=tmp_path/"root"
    root.mkdir()
    f=root/"fixture.py"
    f.write_text("CPU synthetic fixture")
    config={"shared":{"train_examples":8,"steps":4,"group":8,"max_tokens":512,
        "validation_examples":4,"context_limit":4096,"learning_rate":1e-5},
        "methods":{"grpo-difficulty-curriculum":{}}}
    p=tmp_path/"config.json"
    p.write_text(json.dumps(config))
    contract={"source_commit":n["CORE_COMMIT"],"source_file_sha256":{"fixture.py":hashlib.sha256(f.read_bytes()).hexdigest()}}
    audit={"source_commit":n["CORE_COMMIT"],"source_file_sha256":contract["source_file_sha256"],
        "source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
        "execution_config_sha256":hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()}
    argv=["--method","grpo-difficulty-curriculum","--config",str(p),"--seed","43",
        "--output",str(tmp_path/"evidence"),"--variant","unfiltered"]
    if case=="source":f.write_text("modified")
    elif case=="config":audit["execution_config_sha256"]="a"*64
    elif case=="seed":argv[5]="45"
    elif case=="override":argv += ["--steps","8"]
    if case=="valid":
        flags,_=n["validate_core"](root,contract,audit,argv)
        assert flags["--seed"]=="43"
    else:
        with pytest.raises(ValueError):n["validate_core"](root,contract,audit,argv)


def _bound_fixture(tmp_path,commit):
    root=tmp_path/"root"
    root.mkdir()
    f=root/"fixture.py"
    f.write_text("CPU-only observer binding fixture")
    config={"shared":{"train_examples":8,"steps":4,"group":8,"max_tokens":512,
        "validation_examples":4,"context_limit":4096,"learning_rate":1e-5},
        "methods":{"grpo-difficulty-curriculum":{}}}
    p=tmp_path/"config.json"
    p.write_text(json.dumps(config))
    hashes={"fixture.py":hashlib.sha256(f.read_bytes()).hexdigest()}
    contract={"source_commit":commit,"source_file_sha256":hashes}
    audit={**contract,"source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
        "execution_config_sha256":hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()}
    argv=["--method","grpo-difficulty-curriculum","--config",str(p),"--seed","42",
        "--output",str(tmp_path/"output"),"--variant","unfiltered"]
    return root,contract,audit,argv


def test_hard_pin_only_precision_repaired_core():
    n=runpy.run_path(str(ROOT/"scripts/observe_oct14_cuda_memory.py"))
    assert n["CORE_COMMIT"]=="b90862754bf51b1beeb5add3f7dc2a51ca00ace4"


@pytest.mark.parametrize("seed",[42,43,44])
@pytest.mark.parametrize("variant",["unfiltered","static","fixed-medium","staged","too-hard"])
def test_exact_fifteen_original_repaired_course_arguments_allowed(tmp_path,seed,variant):
    n=runpy.run_path(str(ROOT/"scripts/observe_oct14_cuda_memory.py"))
    root,contract,audit,argv=_bound_fixture(tmp_path,"b90862754bf51b1beeb5add3f7dc2a51ca00ace4")
    argv[5]=str(seed)
    argv[9]=variant
    flags,_=n["validate_core"](root,contract,audit,argv)
    assert flags["--seed"]==str(seed) and flags["--variant"]==variant


def test_old_numerically_invalid_core_rejected_even_if_source_and_audit_match(tmp_path):
    n=runpy.run_path(str(ROOT/"scripts/observe_oct14_cuda_memory.py"))
    root,contract,audit,argv=_bound_fixture(tmp_path,"51b4718a76da286b4111c6fc7d8e003d436def72")
    argv[5]="43"
    with pytest.raises(ValueError,match="source"):
        n["validate_core"](root,contract,audit,argv)
