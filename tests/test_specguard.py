"""Fixed Lean artifacts below are unit fixtures, never model capability evidence."""
from dataclasses import asdict, fields
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from auto_research.agent_research import specguard as sg

SPEC = """namespace Spec
abbrev Input := Nat
abbrev Output := Nat
def run (n : Input) : Output := n + 1
end Spec
"""
TEST = """namespace Tests
inductive Case where
  | assertion_1 : Nat → Nat → Case
-- source: assert increment(2) == 4
-- scenario: call increment on literal input 2 and compare with 4
def test : List Case := [Case.assertion_1 2 4]
end Tests
"""
CONNECTOR = """namespace Connector
def check (run : Spec.Input → Spec.Output) (c : Tests.Case) : Option Bool :=
  match c with
  | .assertion_1 n expected => some (run n == expected)
end Connector
"""


def fence(code):
    return "```lean4\n"+code+"```"


class PassingDeclarations:
    """Compiler double exercises orchestration only, not certified evidence."""
    def __init__(self):
        self.calls = []

    def compile(self, source):
        self.calls.append(source)
        theorem = "sgFormal" in source
        return sg.Check(not theorem, "fixture rejects all theorem attempts", "0"*64)


def test_disjoint_views_and_no_gold_surface():
    assert {f.name for f in fields(sg.SpecView)} == {"description", "codebase"}
    assert {f.name for f in fields(sg.TestView)} == {"tests"}
    kernel, seen = PassingDeclarations(), []
    task = sg.public_tasks()[0]

    def generate(request):
        seen.append(request)
        return fence({"spec": SPEC, "test": TEST, "connector": CONNECTOR}[request.role])

    result = sg.run_task(task, generate, kernel)
    assert result["verdict"] == "inconclusive"
    assert [r.role for r in seen] == ["spec", "test", "connector"]
    assert task.tests not in str(asdict(seen[0].view))
    assert SPEC not in str(asdict(seen[1].view))
    assert result["task_sha256"] == sg.fingerprint(asdict(task))
    assert all("request_sha256" in r for r in result["role_records"])


def test_retry_cannot_leak_previous_roles_on_generation_failure():
    seen = []

    def generate(request):
        seen.append(request)
        if request.role == "test":
            raise RuntimeError("budget exhausted")
        return fence(SPEC)

    result = sg.run_task(sg.public_tasks()[0], generate, PassingDeclarations())
    assert result["verdict"] == "inconclusive"
    assert len(seen) == 3
    assert all(not r.previous for r in seen if r.role == "test")
    assert all(SPEC not in r.feedback for r in seen if r.role == "test")
    assert result["role_records"][-1]["error"].endswith("budget exhausted")


@pytest.mark.parametrize("token", ["sorry", "axiom evil : False", "#eval 1", "unsafe def x := 0",
    "initialize pure ()", "macro foo := x", "native_decide", "set_option maxRecDepth 0",
    "end Spec\nnamespace Other", "«axiom»", "by decide", "@[extern x]"])
def test_unsafe_generated_lean_rejected(token):
    with pytest.raises(ValueError):
        sg.parse_artifact(fence(SPEC.replace("def run", token+"\ndef run")), "spec")


def test_comments_and_strings_are_not_executed_but_fences_are_unambiguous():
    safe = SPEC.replace("def run", '-- sorry axiom #eval\ndef text := "sorry axiom IO"\ndef run')
    assert sg.parse_artifact(fence(safe), "spec") == safe
    for value in (fence(SPEC)+fence(SPEC), fence(SPEC)+"```lean4\nx```", "no code"):
        with pytest.raises(ValueError):
            sg.parse_artifact(value, "spec")
    with pytest.raises(ValueError):
        sg.parse_artifact(fence(SPEC+"/-"), "spec")


def test_connector_cannot_freeze_spec_run_and_test_needs_source_scenario():
    with pytest.raises(ValueError):
        sg.parse_artifact(fence(CONNECTOR.replace("some (run n", "some (Spec.run n")), "connector")
    with pytest.raises(ValueError):
        sg.parse_artifact(fence(TEST.replace("-- source:", "-- no-source:")), "test")
    assert sg.parse_artifact(fence(CONNECTOR), "connector") == CONNECTOR


def test_nonempty_test_and_existential_kernel_contract():
    assert "Tests.test.isEmpty = false" in sg.HARNESS
    assert "¬ ∃ f : Spec.Input → Spec.Output" in sg.CONFLICT
    assert "∀ x, f x = Spec.run x" in sg.CONFLICT
    assert "sgSupported = true" in sg.CONFLICT
    assert "by decide" in sg.NO_CONFLICT
    assert not sg.axioms_ok("")
    assert not sg.axioms_ok("depends on axioms: [sorryAx]")
    assert not sg.axioms_ok("depends on axioms: [customFalse]")
    assert sg.axioms_ok("'sgFormalConflict' depends on axioms: [propext, Quot.sound]")


def test_bounded_failures_preserve_generated_response():
    seen = []

    def invalid(request):
        seen.append(request)
        return "deliberately invalid generated output"

    result = sg.run_task(sg.public_tasks()[0], invalid, PassingDeclarations())
    assert len(seen) == 2
    assert result["artifacts"] == {}
    assert result["role_records"][0]["response"] == "deliberately invalid generated output"
    assert result["verdict"] == "inconclusive"
    with pytest.raises(ValueError):
        sg.run_task(sg.public_tasks()[0], invalid, PassingDeclarations(), max_attempts=3)


def test_tasks_cover_distinct_semantic_boundaries_without_formal_gold():
    tasks = sg.public_tasks()
    assert len(tasks) == 3
    assert len({t.description for t in tasks}) == 3
    assert "if v > 0" in tasks[1].codebase and "negative" in tasks[1].description
    assert "No package-version behavior" in tasks[2].description
    assert {f.name for f in fields(sg.PublicTask)} == {"task_id", "description", "codebase", "tests"}


def test_specguard_documentation_metadata_cost_and_core_scope():
    root = Path(__file__).resolve().parents[1]
    directory = root/"docs/agent-research/2610.09159-specguard"
    text = (directory/"README.md").read_text()
    for field in ("## 论文信息", "| 论文链接 |", "| 公司/机构 |", "| 首次公开日期 |",
                  "| 原文开源代码 |", "| 本地 Adapter |", "| 本地复现代码 |"):
        assert field in text
    for value in ("2026-10-06 22:00:49 UTC", sg.UPSTREAM_COMMIT, "MATS", "Google DeepMind",
                  "### 核心公式", "```mermaid", "未报告生产线上 A/B", "自建", "inconclusive",
                  "成本过高，不复现（审查 DONE）", "没有 gold Lean", "版权归原作者所有"):
        assert value in text
    assert (directory/"assets/paper-figure-01.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    catalog = json.loads((root/"src/auto_research/paper_specs/catalog/agent-research/specguard.json").read_text())
    assert catalog["adapter"] is None and catalog["implementation_status"] == "component_only"
    assert catalog["diagnostic_only"] is True and catalog["promotion_eligible"] is False
    assert catalog["evolve_integrated"] is False and catalog["requires_gpu_validation"] is True
    assert catalog["published_at"] == "2026-10-06T22:00:49Z"


def _curator_fixture():
    """Entirely synthetic unit data; never written into documentation metrics."""
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("curate_specguard", root/"scripts/curate_specguard_component.py")
    curator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(curator)
    records = []

    class KernelDouble:
        def compile(self, source):
            return sg.Check(True, "'fixture' depends on axioms: [propext]",
                            hashlib.sha256(source.encode()).hexdigest())

    def generate(request):
        response = fence({"spec": SPEC, "test": TEST, "connector": CONNECTOR}[request.role])
        records.append({"role": request.role, "attempt": request.attempt, "seed": 42,
            "input_tokens": 10, "generated_tokens": 10, "seconds": .01,
            "actual_model_device": "cpu", "request_sha256": sg.fingerprint(asdict(request)),
            "response_sha256": hashlib.sha256(response.encode()).hexdigest()})
        return response

    tasks = sg.public_tasks()
    rows = [{"seed": 42, **sg.run_task(t, generate, KernelDouble())} for t in tasks]
    raw = {"method": "specguard", "protocol_id": sg.PROTOCOL, "upstream_commit": sg.UPSTREAM_COMMIT,
        "dataset": {"id": "self-authored-increment-micro-suite", "public_benchmark": False,
                    "revision": sg.fingerprint([asdict(t) for t in tasks])},
        "tasks": [asdict(t) for t in tasks], "evaluation_tier": "l1_mechanism",
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "full_experiment_status": "not_reproduced_high_cost", "seeds": [42],
        "source_sha256": {p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in curator.SOURCES},
        "model": {"local_files_only": True, "revision": "a"*40}, "lean": {"version": "4.24.0"},
        "actual_model_calls": 9, "actual_generated_tokens": 90, "model_records": records,
        "budget": {"max_attempts_per_role": 2, "max_calls": 18, "max_total_new_tokens": 8000,
                   "wall_seconds": 600, "max_new_tokens_per_call": 1024},
        "device": "cpu", "per_seed": rows, "code_commit": "f"*40,
        "metrics": {"task_runs": 3, "certified_conflicts": 3, "formal_agreements": 0, "inconclusive": 0}}
    # Synthetic unit data only: no real Git revision or model claim is produced.
    curator.committed_sources = lambda commit: dict(raw["source_sha256"])
    return curator, raw, KernelDouble()


def test_curator_rechecks_proof_and_model_output_linkage_on_unit_fixtures():
    curator, raw, kernel = _curator_fixture()
    assert len(curator.validate_raw(raw, kernel)) == 3
    raw["model_records"][0]["response_sha256"] = "b"*64
    with pytest.raises(ValueError, match="actual model call"):
        curator.validate_raw(raw, kernel)


@pytest.mark.parametrize("field", ["view", "certificate", "code", "metrics"])
def test_curator_rejects_tampering_and_does_not_promote_fixtures(field):
    curator, raw, kernel = _curator_fixture()
    if field == "view":
        raw["per_seed"][0]["role_records"][0]["input_sha256"] = "0"*64
    elif field == "certificate":
        raw["per_seed"][0]["certificate"] = "theorem fake : True := by trivial"
    elif field == "code":
        raw["source_sha256"] = {}
    else:
        raw["metrics"]["certified_conflicts"] = 99
    with pytest.raises(ValueError):
        curator.validate_raw(raw, kernel)


def test_curator_must_match_frozen_blob_hashes_not_only_commit_parameter():
    curator, raw, kernel = _curator_fixture()
    curator.committed_sources = lambda commit: {p: "0"*64 for p in curator.SOURCES}
    with pytest.raises(ValueError, match="frozen Git commit"):
        curator.validate_raw(raw, kernel)


def test_committed_source_reader_requires_local_commit_and_reads_both_blobs(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("frozen_specguard_curator", root/"scripts/curate_specguard_component.py")
    curator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(curator)
    calls = []

    def fake_git(argv, **kwargs):
        calls.append(argv)
        if argv[1:3] == ["cat-file", "-t"]:
            return SimpleNamespace(returncode=0, stdout="commit\n")
        return SimpleNamespace(returncode=0, stdout=argv[-1].encode())

    monkeypatch.setattr(curator.subprocess, "run", fake_git)
    frozen = "c"*40
    values = curator.committed_sources(frozen)
    assert values == {p: hashlib.sha256(f"{frozen}:{p}".encode()).hexdigest() for p in curator.SOURCES}
    assert calls == [["git", "cat-file", "-t", frozen], *(
        ["git", "show", f"{frozen}:{p}"] for p in curator.SOURCES)]
    with pytest.raises(ValueError, match="exact frozen"):
        curator.committed_sources("main")
    monkeypatch.setattr(curator.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=1, stdout=""))
    with pytest.raises(ValueError, match="unavailable"):
        curator.committed_sources(frozen)


@pytest.mark.skipif(not os.environ.get("SPECGUARD_LEAN_BIN"), reason="real Lean 4.24.0 not configured")
def test_real_lean_kernel_conflict_agreement_unsupported_and_nonvacuity():
    """Actual proof checking on hand-written unit fixtures; not an end-to-end model run."""
    kernel = sg.LeanKernel(os.environ["SPECGUARD_LEAN_BIN"])
    conflict = sg.certify(SPEC, TEST, CONNECTOR, kernel)
    assert conflict["verdict"] == "conflict", conflict
    agreement = sg.certify(SPEC, TEST.replace("assertion_1 2 4", "assertion_1 2 3"), CONNECTOR, kernel)
    assert agreement["verdict"] == "no-conflict", agreement
    unsupported = CONNECTOR.replace("some (run n == expected)", "none")
    assert sg.certify(SPEC, TEST, unsupported, kernel)["verdict"] == "inconclusive"
    empty = TEST.replace("[Case.assertion_1 2 4]", "[]")
    assert sg.certify(SPEC, empty, CONNECTOR, kernel)["verdict"] == "inconclusive"
    broken = TEST.replace("Case.assertion_1 2 4", "Case.assertion_1 missing 4")
    assert sg.certify(SPEC, broken, CONNECTOR, kernel)["verdict"] == "inconclusive"
