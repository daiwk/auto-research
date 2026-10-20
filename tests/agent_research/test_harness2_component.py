"""Harness² mechanics, privacy boundaries, exact budgets and persistent evidence."""
from copy import deepcopy
from dataclasses import FrozenInstanceError, fields, replace
import importlib.util
import json
from pathlib import Path
import threading
import time

import pytest

from auto_research.agent_research import harness2 as h

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("harness2_cpu_runner", ROOT / "scripts/run_harness2_component.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
curator_spec = importlib.util.spec_from_file_location("harness2_curator", ROOT / "scripts/curate_harness2_component.py")
curator = importlib.util.module_from_spec(curator_spec)
curator_spec.loader.exec_module(curator)


def task(key="task-0", domain="arithmetic"):
    return h.PublicTask(key, domain, "Apply the public request.", (("input.txt", "public material"),))


def base():
    return h.Harness((("systemprompt.md", "Follow the public task."),))


def execute(task, harness, config):
    return h.Execution(f"public execution using {harness.sha256}", harness.sha256)


def edit(context):
    tree = context.current.mapping()
    tree["memory.md"] = f"{context.stage}-{context.index}-{context.current.sha256}"
    available = context.references + context.pool
    return h.Edit(h.Harness(tuple(tree.items())), "Public execution evidence motivated this edit.", (available[0].label,))


def choose(context):
    assert not {"harness", "references", "pool", "stages", "trajectory", "labels"} & {
        field.name for field in fields(context)}
    return context.candidates[-1][0]


def reflect(context):
    candidate = next(e for e in context.evidence if e.label.startswith("domain"))
    return h.Lesson("A public recurring behavior.", "Keep an evidence-bounded procedure.",
                    ((context.evidence[0].label, candidate.label),))


def controller(**kwargs):
    options = dict(executor=execute, editor=edit, selector=choose, reflector=reflect,
                   config=h.ExecutionConfig("frozen-model-v1", "frozen-env-v1", 42, "fixed-improver-v1", base().sha256))
    options.update(kwargs)
    return h.Harness2(**options)


@pytest.mark.parametrize("mode", ["parallel", "sequential"])
@pytest.mark.parametrize("k", [1, 2, 3])
def test_published_budget_and_complete_probed_compositions(mode, k):
    result = controller(mode=mode, k=k, workers=3).run(task(), base())
    assert len(result.evidence) == 4*k
    assert len(result.stages) == 3*k
    assert len(result.finals) == k
    assert len({e.label for e in result.evidence}) == 4*k
    assert result.adopted in result.finals
    assert result.diagnostic_only and not result.promotion_eligible and not result.evolve_integrated
    for stage in result.stages:
        assert len(stage.context.references) == k
        assert stage.attempts == 1
        assert stage.context.library == ()
        if mode == "parallel":
            assert stage.context.current == base()
            if stage.context.stage == "compose":
                assert len(stage.context.pool) == 2*k
        elif stage.context.stage == "compose":
            assert len(stage.context.pool) == 3*(stage.context.index-1)+2
            if stage.context.index > 1:
                previous = next(s for s in result.stages if s.label == f"compose{stage.context.index-1}")
                assert stage.context.current == previous.edit.harness


def test_actual_probe_parallelism_and_config_identity():
    lock = threading.Lock()
    active, maximum, configurations = 0, 0, []
    config = h.ExecutionConfig("same-model", "same-environment", 43, "fixed-improver-v1", base().sha256)
    def executor(public, harness, matched):
        nonlocal active, maximum
        assert public == task()
        with lock:
            configurations.append(matched)
            active += 1
            maximum = max(maximum, active)
        time.sleep(.01)
        with lock:
            active -= 1
        return execute(public, harness, matched)
    result = controller(executor=executor, config=config, k=3, workers=3).run(task(), base())
    assert maximum == 3 and len(configurations) == 12
    assert all(value is config for value in configurations)
    assert [e.label for e in result.evidence[:3]] == ["base1", "base2", "base3"]


def test_k1_skips_selector_and_selector_never_sees_base_or_proposals():
    def forbidden(_context):
        raise AssertionError("must bypass selector at k=1")
    assert controller(selector=forbidden).run(task(), base()).selection_error == ""
    seen = []
    def select(context):
        seen.append(context)
        assert len(context.candidates) == 3
        assert all(key.startswith("candidate-") for key, _ in context.candidates)
        return context.candidates[0][0]
    result = controller(selector=select, k=3).run(task(), base())
    assert len(seen) == 1 and result.adopted.startswith("compose")


@pytest.mark.parametrize("bad", ["synthesized new deliverable", "base1", "domain1", None])
def test_selection_failure_preserves_existing_final_and_failure_evidence(bad):
    result = controller(selector=lambda _: bad, k=2).run(task(), base())
    assert result.adopted == "compose1"
    assert "failed" in result.selection_error.lower()
    adopted = next(e for e in result.evidence if e.label == result.adopted)
    assert adopted.execution.deliverable != bad


def test_no_final_does_not_fall_back_to_successful_baseline():
    count = 0
    def executor(public, harness, config):
        nonlocal count
        count += 1
        if count == 4:
            raise RuntimeError("failed final")
        return execute(public, harness, config)
    result = controller(executor=executor).run(task(), base())
    assert result.adopted is None
    assert len(result.evidence) == 4 and result.evidence[-1].execution.ok is False
    assert result.evidence[0].execution.ok
    assert result.summary()["failed_rollouts"] == 1


def test_invalid_edits_retry_once_then_keep_current_not_fake_success():
    result = controller(editor=lambda _: h.Edit(base(), "valid notes", ("future999",)), k=2).run(task(), base())
    assert len(result.stages) == 6
    assert all(s.fell_back and s.attempts == 2 and len(s.errors) == 2 for s in result.stages)
    assert all(e.harness == base() for e in result.evidence)
    assert result.summary()["editor_attempts"] == 12
    assert not result.lesson_retained
    assert result.reflection_error


def test_library_persists_full_harness_and_contrasts_without_automatic_inheritance(tmp_path):
    c = controller(k=2)
    library = h.EvidenceLibrary(tmp_path / "library.json", c.namespace)
    first = c.run(task(), base(), library=library, task_index=0)
    assert first.lesson_retained and first.library_entries_seen == 0
    restarted = h.EvidenceLibrary(library.path, c.namespace)
    second = c.run(task("task-1"), base(), library=restarted, task_index=1)
    assert second.lesson_retained and second.library_entries_seen == 1
    assert all(e.harness == base() for e in second.evidence if e.label.startswith("base"))
    for stage in second.stages:
        assert [e.task_id for e in stage.context.library] == ["task-0"]
    previous = second.stages[0].context.library[0]
    assert previous.adopted.sha256 == next(e.harness.sha256 for e in first.evidence if e.label == first.adopted)
    assert previous.evidence[0].execution.trajectory
    obj = json.loads(library.path.read_text())
    assert len(obj["entries"]) == 2
    assert all(h.fingerprint(e["entry"]) == e["sha256"] for e in obj["entries"])
    other = c.run(task("other-domain", "different"), base(), library=restarted, task_index=0)
    assert other.library_entries_seen == 0


def test_empty_or_unsupported_reflection_never_enters_library(tmp_path):
    for callback in (lambda _: None, lambda _: h.Lesson("cue", "unsupported", (("base1", "base1"),)),
                     lambda _: h.Lesson("cue", "unknown", (("base1", "future"),))):
        c = controller(reflector=callback)
        library = h.EvidenceLibrary(tmp_path / "empty.json", c.namespace)
        result = c.run(task(), base(), library=library)
        assert not result.lesson_retained and not library.path.exists()


def test_identical_execution_outputs_not_enough_to_store_lesson(tmp_path):
    c = controller(executor=lambda *_: h.Execution("same behavior", "same output"))
    library = h.EvidenceLibrary(tmp_path / "library.json", c.namespace)
    result = c.run(task(), base(), library=library)
    assert not result.lesson_retained and result.reflection_error


def test_future_repeated_and_namespace_entries_rejected(tmp_path):
    c = controller()
    library = h.EvidenceLibrary(tmp_path / "library.json", c.namespace)
    c.run(task(), base(), library=library, task_index=3)
    for current, index in ((task(), 4), (task("new"), 3), (task("new"), 2)):
        with pytest.raises(ValueError, match="current/future or repeated"):
            c.run(current, base(), library=library, task_index=index)
    for alternative in (controller(k=2), controller(mode="sequential"),
                        controller(config=h.ExecutionConfig("new-model", "frozen-env-v1", 42, "fixed-improver-v1", base().sha256)),
                        controller(config=h.ExecutionConfig("frozen-model-v1", "frozen-env-v1", 42, "changed-improver-v2", base().sha256))):
        with pytest.raises(ValueError, match="scoped"):
            alternative.run(task("new"), base(), library=library, task_index=4)


def test_library_tamper_and_concurrent_snapshot_rejected(tmp_path):
    c = controller()
    library = h.EvidenceLibrary(tmp_path / "library.json", c.namespace)
    c.run(task(), base(), library=library)
    rows, snapshot = library.before(task("next"), 1)
    changed = replace(rows[0], task_id="interloper", task_index=1)
    library.append(changed, snapshot)
    with pytest.raises(ValueError, match="changed while"):
        library.append(replace(changed, task_id="next", task_index=2), snapshot)
    obj = json.loads(library.path.read_text())
    obj["entries"][0]["entry"]["lesson"]["lesson"] = "forged lesson"
    library.path.write_text(json.dumps(obj))
    with pytest.raises(ValueError, match="integrity"):
        library.before(task("later"), 3)


@pytest.mark.parametrize("path", ["../secret.txt", "/tmp/secret.txt", "./input.txt", "a\\b", "RUBRICS.json", "gold_answer.txt"])
def test_public_source_paths_reject_traversal_and_privileged_material(path):
    with pytest.raises(ValueError):
        h.PublicTask("id", "domain", "public task", ((path, "contents"),))


@pytest.mark.parametrize("text", ["reference answer", "answer_key", "gold plan", "grading criteria", "grader_verdict"])
def test_privileged_material_cannot_enter_context_harness_or_outputs(text):
    with pytest.raises(ValueError):
        h.PublicTask("id", "domain", text)
    with pytest.raises(ValueError):
        h.Harness((("systemprompt.md", text),))
    with pytest.raises(ValueError):
        h.Execution("public trajectory", text)


def test_eight_component_surface_helpers_and_frozen_structures():
    files = (("systemprompt.md", "When needed load signed-ledger; use scripts/check.py."),
        ("guardrails.md", "public constraints"), ("memory.md", "public memory"),
        ("tools.md", "public tool guide"), ("skills/signed-ledger/SKILL.md", "---\nname: signed-ledger\ndescription: signed amounts\n---\n"),
        ("scripts/check.py", "print('public')"), ("sub_agents/checker.md", "bounded helper"),
        ("plugin/check.ts", "export default {}"))
    harness = h.Harness(files)
    assert len(harness.files) == 8
    mapping = harness.mapping()
    mapping["systemprompt.md"] = "changed copy"
    assert harness.mapping()["systemprompt.md"] != "changed copy"
    with pytest.raises(FrozenInstanceError):
        harness.files = ()
    for bad in (files + (("outside.txt", "no"),), files + (files[0],),
                (("systemprompt.md", "scripts/missing.py"),),
                (("systemprompt.md", "missing trigger"), files[4]),
                (("systemprompt.md", "{{ variable }}"),)):
        with pytest.raises(ValueError):
            h.Harness(bad)


def test_initial_harness_is_frozen_in_library_namespace():
    revised = h.Harness((("systemprompt.md", "A different base procedure."),))
    with pytest.raises(ValueError, match="initial harness differs"):
        controller().run(task(), revised)
    config = h.ExecutionConfig("frozen-model-v1", "frozen-env-v1", 42, "fixed-improver-v1", revised.sha256)
    assert controller(config=config).namespace != controller().namespace


@pytest.mark.parametrize("args", [{"k": 0}, {"k": True}, {"k": 17}, {"mode": "invented"}, {"workers": 0}, {"workers": 9}])
def test_bounded_local_budget_inputs(args):
    with pytest.raises(ValueError):
        controller(**args)


@pytest.mark.parametrize("mode", ["parallel", "sequential"])
def test_actual_python_script_rollouts_and_persistent_library(tmp_path, mode):
    result = runner.run_seed(42, mode, 2, 2, tmp_path)
    metrics = result["metrics"]
    assert metrics["actual_python_rollouts"] == 16
    assert metrics["improvement_stages"] == 12
    assert metrics["script_mechanism_post_run_checks"] == 2
    assert metrics["second_task_prior_library_entries"] == 1
    assert metrics["retained_evidence_lessons"] == 2
    assert metrics["failed_rollouts"] == 0
    for record in result["records"]:
        first, adopted = record["evidence"][0], next(e for e in record["evidence"] if e["label"] == record["summary"]["adopted"])
        assert first["execution"]["deliverable"] != adopted["execution"]["deliverable"]
        assert all("expected" not in stage["edit"]["notes"].lower() for stage in record["stages"])


def test_curated_actual_cpu_evidence_and_paper_metadata():
    path = ROOT / "docs/agent-research/2610.14224-harness2/metrics/component-cpu-seeds42-44.json"
    data = json.loads(path.read_text())
    curator.validate_curated(data)
    catalog = json.loads((ROOT / "src/auto_research/paper_specs/catalog/agent-research/harness2.json").read_text())
    assert catalog["local_operator"] == "auto_research.agent_research.harness2.Harness2"
    assert catalog["adapter"] is None and catalog["evaluation_tier"] == "l1_mechanism"
    assert not catalog["requires_gpu_validation"] and not catalog["evolve_integrated"]
    assert catalog["full_experiment_status"] == "not_reproduced_high_cost"
    assert catalog["published_at"] == "2026-10-09T18:34:25Z"
    text = (ROOT / "docs" / catalog["detail_path"]).read_text()
    assert all(token in text for token in ("## 论文信息", "原文开源代码", "本地 Adapter", "核心公式",
                                           "不复现（审查 DONE）", "assets/paper-figure-01.png"))


@pytest.mark.parametrize("mutation", ["source", "metric", "aggregate", "seeds", "tier", "promotion", "formal", "inputs"])
def test_curated_evidence_tamper_rejected(mutation):
    path = ROOT / "docs/agent-research/2610.14224-harness2/metrics/component-cpu-seeds42-44.json"
    data = deepcopy(json.loads(path.read_text()))
    if mutation == "source":
        data["provenance"]["executed_source_sha256"][next(iter(data["provenance"]["executed_source_sha256"]))] = "0"*64
    elif mutation == "metric":
        data["per_seed_mode"][0]["metrics"]["failed_rollouts"] = 1
    elif mutation == "aggregate":
        data["metrics"]["actual_python_rollouts_total"] += 1
    elif mutation == "seeds":
        data["per_seed_mode"][0]["seed"] = 43
    elif mutation == "tier":
        data["evaluation_tier"] = "l2_public_benchmark"
    elif mutation == "promotion":
        data["promotion_eligible"] = True
    elif mutation == "formal":
        data["evaluation_protocol"]["formal_comparison"] = True
    else:
        data["per_seed_mode"][0]["fixture_sha256"] = "0"*64
    with pytest.raises(ValueError):
        curator.validate_curated(data)
