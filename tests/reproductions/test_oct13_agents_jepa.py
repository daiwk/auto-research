from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest
import torch

from auto_research.reproductions.near.algorithm import (
    NEARIndex, projection_residual, score_scale, unit,
)
from auto_research.reproductions.near.data import (MemoryQuery, grouped_split, load_longmemeval,
                                                 query_disjoint_shared_bank_split)
from auto_research.reproductions.near.experiment import evidence_flags
from auto_research.reproductions.beyond_final_embedding.algorithm import (
    SparseTokenIndex, multipositive_maxsim_loss, query_adapter,
)
from auto_research.reproductions.lewam.algorithm import (
    action_flow_targets, joint_loss, mot_visibility, refine_plans, sigreg,
)
from auto_research.reproductions.smolwam.algorithm import (
    RELEASED_BLOCKS, assert_release, clean_estimate, curriculum_layout, distillation_loss,
)
from auto_research.reproductions.skilldreamer.algorithm import (
    Skill, capability_context, execute_agent, hybrid_retrieval, parse_capability_assessment, prospective_skills,
)


def test_near_covariance_scale_equals_exact_population_variance():
    view = np.random.default_rng(3).normal(size=(14, 5))
    expected = np.sqrt(np.var(view @ view.T, axis=1).mean())
    assert score_scale(view) == pytest.approx(expected)


def test_near_projection_is_orthogonal_and_single_key_matches_full_fusion():
    rng = np.random.default_rng(4)
    bank = unit(rng.normal(size=(20, 8)))
    query = unit(rng.normal(size=8))
    references = unit(rng.normal(size=(20, 8)))
    residual = projection_residual(bank, references)
    assert np.max(np.abs(np.sum(residual * references, axis=1))) < 1e-12
    index = NEARIndex(depth=3, alpha=2, neighbors=4, seed=43).fit(bank)
    views = index.query_views(query)
    explicit = (index.views[0] @ views[0][0]) / index.scales[0]
    for layer in range(1, 4):
        explicit += 2 / 3 * (index.views[layer] @ views[layer][0]) / index.scales[layer]
    np.testing.assert_allclose(index.scores(query), explicit, atol=1e-10)
    assert all(len(table.anchors) <= 16 for table in index.tables)


def test_near_references_cannot_take_queries_or_labels_and_zero_alpha_is_base():
    bank = unit(np.random.default_rng(9).normal(size=(16, 4)))
    query = unit(np.ones(4))
    index = NEARIndex(alpha=0).fit(bank)
    np.testing.assert_array_equal(index.search(query), np.argsort(-(bank @ query), kind="stable")[:10])
    with pytest.raises(TypeError):
        index.fit(bank, labels=np.ones(16))
    with pytest.raises(ValueError):
        NEARIndex().fit(bank[:1])


def test_memory_loader_drops_gold_answer_and_merge_duplicate_ids(tmp_path):
    row = {"question_id": "q", "question": "What happened?", "answer": "SECRET_GOLD",
           "answer_session_ids": ["m"], "haystack_session_ids": ["m", "m"],
           "haystack_sessions": [[{"role": "user", "content": "ordinary memory"}]] * 2}
    path = tmp_path / "raw.json"
    path.write_text(json.dumps([row]))
    queries, labels = load_longmemeval(path)
    assert "SECRET_GOLD" not in repr(queries)
    assert queries[0].memory_ids == ("m",)
    assert labels == {"q": {"m"}}


def test_grouped_split_keeps_overlapping_candidate_banks_together():
    queries = [MemoryQuery(str(i), "question", ("memory",), (str(i),), str(i)) for i in range(9)]
    queries.append(MemoryQuery("overlap", "question", ("memory",), ("0",), "extra"))
    split = grouped_split(queries)
    memory_sets = [{m for q in rows for m in q.memory_ids} for rows in split.values()]
    assert all(not a.intersection(b) for i, a in enumerate(memory_sets) for b in memory_sets[i + 1:])


def test_shared_bank_split_is_explicit_query_only_and_never_weakens_strict_default():
    queries = [MemoryQuery(str(i), "question", ("shared memory",), ("shared",), "bank") for i in range(10)]
    with pytest.raises(ValueError, match="three disjoint"):
        grouped_split(queries)
    split = query_disjoint_shared_bank_split(queries)
    assert {name: len(rows) for name, rows in split.items()} == {"train": 6, "validation": 2, "test": 2}
    ids = [{q.id for q in rows} for rows in split.values()]
    assert all(not a.intersection(b) for i, a in enumerate(ids) for b in ids[i + 1:])


@pytest.mark.parametrize("requested,shared,diagnostic", [
    (False, False, False), (True, False, True), (False, True, True), (True, True, True),
])
def test_explicit_diagnostic_flag_cannot_be_promoted_even_with_strict_bank(requested, shared, diagnostic):
    result = evidence_flags({"diagnostic_only": requested}, {"shared_unlabelled_memory": shared})
    assert result == {"diagnostic_only": diagnostic, "promotion_eligible": not diagnostic}


def test_diagnostic_flag_rejects_ambiguous_string_false():
    with pytest.raises(ValueError, match="explicit boolean"):
        evidence_flags({"diagnostic_only": "false"}, {"shared_unlabelled_memory": False})


@pytest.mark.parametrize("key,slug", [
    ("near", "2610.13314-near"),
    ("beyond-final-embedding", "2610.13277-beyond-final-embedding"),
])
def test_memory_gpu_curation_keeps_protocols_separate_and_imports_only_real_metrics(key, slug, tmp_path):
    from auto_research.experiment_store.store import ExperimentStore
    from auto_research.gpu_validation import load_gpu_receipt

    root = Path(__file__).resolve().parents[2]
    path = root / "docs/reproductions" / slug / "metrics/a30-diagnostics-34148c2e.json"
    native = json.loads(path.read_text())
    assert native["schema_version"] == 2
    assert native["seeds"] == [42, 43, 44]
    assert native["strict_diagnostic_seeds"] == [42]
    assert native["evaluation_protocol"]["tier"] == "l1_mechanism"
    assert native["evaluation_protocol"]["formal_comparison"] is False
    assert native["promotion_eligible"] is False
    assert native["provenance"]["code_commit"] == "34148c2e29c01e9be7e4d5b8cbd09fd0f6016902"
    assert native["provenance"]["dataset_fingerprint"] == native["dataset"]["files"]["longmemeval_s_cleaned.json"]
    assert native["metrics"]["shared100.queries.test"] == 20
    assert native["metrics"]["strict30.queries.test"] == 2
    for record in native["records"]:
        raw = (root / record["raw_path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == record["raw_sha256"]
        result = json.loads(raw)
        assert result["diagnostic_only"] is True and result["promotion_eligible"] is False
        prefix = "shared100" if record["split_policy"] == "query-disjoint-shared-bank" else "strict30"
        for variant in ("test", "baseline"):
            for metric, value in result[variant].items():
                assert native["metrics"][f"{prefix}.seed{record['seed']}.{variant}.{metric}"] == value
        if key == "beyond-final-embedding" and record["seed"] == 43:
            assert result["selection"]["epoch"] == 0
            assert result["parameter_update_l2"] == 0
            assert len(result["training_losses"]) == 2
    with ExperimentStore(tmp_path / "experiments.sqlite") as store:
        store.import_artifact(path, root=root)
        row = store.rows(method=key)[0]
        assert row.seed == "[42, 43, 44]"
        assert row.metrics == native["metrics"]
        assert "schema_version" not in row.metrics
        assert all(metric.startswith(("shared100.", "strict30.")) for metric in row.metrics)
    artifact = f"docs/gpu-validations/oct13-{key}-a30.json"
    receipt = load_gpu_receipt(root / artifact)
    assert receipt["accelerator"]["model"] == "NVIDIA A30"
    assert receipt["provenance"]["artifact_path"] == artifact


def test_sparse_floor_aggregates_by_memory_and_preserves_unmatched_candidates():
    bank = [np.array([[1.0, 0], [0.8, 0.6]]), np.array([[0.0, 1.0]])]
    index = SparseTokenIndex(bank, np.array([[1.0, 0], [0.0, 1.0]]))
    scores = index.local_scores(np.array([[1.0, 0]]), token_budget=2)
    np.testing.assert_allclose(scores, [1.0, 0.8])
    assert index.search_count == 1
    fused = index.scores(np.array([[1.0, 0]]), np.array([0.0, 1.0]), alpha=1)
    assert fused.argmax() == 1  # global branch can return a memory with no sparse match


def test_query_adapter_is_identity_initially_preserves_norm_and_really_updates():
    torch.manual_seed(5)
    model = query_adapter(4, rank=2)
    query = torch.randn(3, 4)
    torch.testing.assert_close(model(query), query)
    memories = [torch.randn(3, 4), torch.randn(4, 4)]
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss = multipositive_maxsim_loss(model(query), memories, {1})
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    assert model.b.weight.norm() > 0
    torch.testing.assert_close(model(query).norm(dim=-1), query.norm(dim=-1))
    assert all(memory.grad is None for memory in memories)


def test_lewam_mask_blocks_indirect_clean_leakage_and_future_action_attention():
    visible = mot_visibility()
    clean, noisy, state, goal = slice(4, 9), slice(9, 19), 2, 3
    assert visible[state, clean].all()
    assert not visible[state, goal]
    assert visible[noisy, goal].all()
    assert not visible[noisy, clean].any()
    reachable = visible.to(torch.int64)
    for _ in range(4):
        reachable = ((reachable @ visible.to(torch.int64)) > 0).to(torch.int64)
    assert not reachable[noisy, clean].any()
    assert not visible[9, 10:19].any()


def test_lewam_joint_loss_has_real_flow_state_and_sigreg_gradients():
    action, noise = torch.randn(4, 2), torch.randn(4, 2)
    mixed, velocity = action_flow_targets(action, noise, torch.tensor(0.4))
    torch.testing.assert_close(mixed, noise * 0.6 + action * 0.4)
    torch.testing.assert_close(velocity, action - noise)
    latents = torch.randn(8, 4, requires_grad=True)
    regularizer = sigreg(latents, torch.randn(4, 32))
    prediction = torch.randn(4, 2, requires_grad=True)
    state = torch.randn(4, 4, requires_grad=True)
    loss = joint_loss(state, latents[:4], prediction, velocity, regularizer)
    loss.backward()
    assert all(x.grad.norm() > 0 for x in (latents, prediction, state))
    assert torch.isfinite(regularizer)


def test_lewam_refinement_retains_original_if_cost_worsens():
    plans = torch.tensor([[1.0], [0.2], [-0.7]])
    cost = lambda x: (x - 0.0).square().sum(1)
    refined, selected = refine_plans(plans, cost, steps=3)
    assert selected <= cost(plans).min()
    assert not refined.requires_grad


def test_smolwam_contract_is_real_cosmos_layout_and_distillation_not_vqa():
    release = {"model": {"trunk_blocks": list(RELEASED_BLOCKS), "n_bidir": 6,
                         "ctx_pad_to": 512, "slot_tokens": [196, 0, 28, 0, 0]}}
    assert_release(release)
    assert sum(curriculum_layout(0)) + 4 * 196 == 1764
    assert sum(curriculum_layout(1000)) + 4 * 196 == 1008
    release["model"]["trunk_blocks"] = [0, 1]
    with pytest.raises(ValueError):
        assert_release(release)
    predicted = torch.tensor([2.0], requires_grad=True)
    torch.testing.assert_close(clean_estimate(predicted, torch.tensor([1.0]), 0.5), torch.tensor([1.5]))
    loss = distillation_loss(predicted, torch.tensor([0.0]), torch.tensor([1.0]),
                             predicted, torch.tensor([0.5]), torch.tensor([1.5]))
    loss.backward()
    assert predicted.grad == 4


def test_skilldreamer_psg_has_real_generation_and_invalid_no_heuristic_fallback():
    prompts = []
    def generator(prompt):
        prompts.append(prompt)
        return ('{"capabilities":[{"name":"percentage","requirement":"compute a percentage"}],"semantic_anchors":["sale"]}'
                if len(prompts) == 1 else "# Hypothetical procedure\nCalculate the sale percentage.")
    pseudo, anchors = prospective_skills("calculate sale", generator)
    assert len(prompts) == 2 and anchors == ["sale"] and "Hypothetical" in pseudo[0]
    with pytest.raises(ValueError):
        prospective_skills("task", lambda _: "invalid")


@pytest.mark.parametrize("response", [
    '{"capabilities":[{"requirement":"arithmetic"}]}',
    '{"capabilities":[{"requirement":"arithmetic"}],"semantic_anchors":null}',
    '{"tool":"calculator","semantic_anchors":["arithmetic"]}',
    '{"capabilities":[{"name":"math","requirement":"compute"}],"semantic_anchors":[]}',
    '{"capabilities":[{"name":"math","requirement":"compute"}],"semantic_anchors":[""]}',
    '{"capabilities":[{"name":"math","requirement":""}],"semantic_anchors":["math"]}',
    '{"capabilities":[{"requirement":"compute"}],"semantic_anchors":["math"]}',
])
def test_skilldreamer_missing_psg_fields_are_countable_schema_failures(response):
    with pytest.raises(ValueError):
        prospective_skills("task without reference answer", lambda prompt: response)


def test_skilldreamer_empty_pseudo_procedure_is_not_a_retrieval_fallback():
    responses = iter(['{"capabilities":[{"name":"math","requirement":"compute"}],"semantic_anchors":["math"]}', "  "])
    with pytest.raises(ValueError, match="pseudo procedure must be nonempty"):
        prospective_skills("task", lambda _: next(responses))


def test_skilldreamer_hsr_roundrobin_and_capability_checkpoint():
    skills = [Skill(str(i), str(i), "description", "procedure") for i in range(3)]
    vectors = np.array([[1, 0], [1, 0], [0, 1], [1, 0], [0, 1], [-1, 0]], dtype=float)
    selected = hybrid_retrieval("goal", ["p1", "p2"], [], skills, lambda _: vectors, alpha=0, top_k=2)
    assert [s.id for s in selected] == ["0", "1"]
    assert "RUNTIME CAPABILITY CHECKPOINT" in capability_context("goal", [], skills, {}, 5, 8)
    assert "RUNTIME CAPABILITY CHECKPOINT" not in capability_context("goal", [], skills, {}, 4, 8)


def test_skilldreamer_policy_does_not_receive_gold_and_uses_loaded_skill_before_real_tool():
    skill = Skill("arithmetic", "Arithmetic", "calculation", "REAL_GALLERY_PROCEDURE")
    assessment = "SUBGOAL: calculate\nEVIDENCE: two given values\nCAPABILITY: verified arithmetic\nDECISION: MATCH arithmetic\nNEXT: bounded calculator action\n"
    responses = [
        assessment + '{"skill_id":"arithmetic","tool":"calculator","arguments":{"expression":"2+3"}}',
        assessment + '{"skill_id":null,"tool":"calculator","arguments":{"expression":"2+3"}}',
        assessment + '{"skill_id":null,"tool":"finish","arguments":{"answer":"5"}}',
    ]
    prompts = []
    def generate(prompt):
        prompts.append(prompt)
        return responses.pop(0)
    outcome = execute_agent("Add two and three", generate, [skill])
    assert outcome["executed_actions"] == 2
    assert outcome["submitted_answer"] == "5"
    assert outcome["loaded_skills"] == ["arithmetic"]
    assert "REAL_GALLERY_PROCEDURE" not in prompts[0]
    assert "REAL_GALLERY_PROCEDURE" in prompts[1]
    assert "Calculator result: 5" in prompts[2]
    assert all("reference_answer" not in p and "gold_plan" not in p for p in prompts)


def test_skilldreamer_action_json_alone_cannot_count_as_capability_reevaluation():
    with pytest.raises(ValueError, match="five actual"):
        parse_capability_assessment('{"tool":"finish","arguments":{"answer":"5"}}')
    outcome = execute_agent("Add two and three", lambda _: '{"tool":"finish","arguments":{"answer":"5"}}', [],
                            action_budget=1)
    assert outcome["executed_actions"] == 0
    assert outcome["submitted_answer"] is None
    assert outcome["generation_errors"] == 3


def test_offline_author_code_mirror_requires_complete_byte_provenance(tmp_path):
    import hashlib
    from auto_research.reproductions.lewam.external import PINS, verify_source
    (tmp_path / "LICENSE").write_text("MIT fixture")
    (tmp_path / "model.py").write_text("VALUE = 1\n")
    hashes = {name: hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()
              for name in ("LICENSE", "model.py")}
    manifest = {"kind": "public-resource", "public_id": "MinghaoFu/lewam",
                "revision": PINS["lewam"], "files": hashes}
    (tmp_path / "provenance.json").write_text(json.dumps(manifest))
    verify_source(tmp_path, "lewam")
    (tmp_path / "model.py").write_text("VALUE = 2\n")
    with pytest.raises(ValueError, match="checksum"):
        verify_source(tmp_path, "lewam")


def candidate_evidence(key):
    metrics = {"optimizer_updates": 2, "nonzero_gradient_updates": 2,
               "parameter_sample_delta_l2": 0.5, "updated_parameter_tensors": 1}
    if key == "lewam":
        metrics.update(train_batches=1, validation_batches=1, validation_action_loss=1.0,
            train_action_loss=1.0, train_latent_loss=1.0, train_sigreg_loss=1.0)
        evidence = {"batches": [{"training": training, "loss": 3.04, "act": 1.0, "state": 1.0, "reg": 1.0}
                                for training in (True, False)], "gradients": [1.0, 1.0]}
    else:
        metrics.update(teacher_layout_updates=1, compact_layout_updates=1, nonzero_parameter_updates=2,
            best_validation_action_l1=1.0, real_teacher_target_rows=2, teacher_vs_demo_action_l1=1.0,
            train_mean_action_l1=1.0, train_mean_world_l1=1.0, train_mean_kd_act_l1=1.0, train_mean_kd_world_l1=1.0)
        evidence = {"losses": [{"training": training, "tokens": tokens, "total": 4.0,
            "action_l1": 1.0, "world_l1": 1.0, "kd_act_l1": 1.0, "kd_world_l1": 1.0}
            for training, tokens in ((True, 1764), (True, 1008), (False, 1008))],
            "gradients": [{"tokens": tokens, "norm": 1.0, "parameter_sample_delta_l2": 0.1}
                          for tokens in (1764, 1008)]}
    return metrics, evidence


@pytest.mark.parametrize("key,files", [("lewam", ("lewam_best.pt", "lewam_config.json")),
                                      ("smolwam", ("best.pt",))])
def test_trained_robotics_candidate_is_hash_bound_seed_bound_and_immutable(tmp_path, key, files):
    from auto_research.reproductions.lewam.external import record_trained_candidate, verify_trained_candidate
    for name in files:
        (tmp_path / name).write_bytes(b"actual-output-fixture")
    metrics, evidence = candidate_evidence(key)
    candidate = record_trained_candidate(tmp_path, key, 42, files,
        {"public_id": "public-fixture", "revision": "a" * 40}, metrics, evidence)
    assert candidate["kind"] == "local-trained-candidate"
    assert verify_trained_candidate(tmp_path, key, 42, files) == candidate
    with pytest.raises(ValueError, match="identity/seed/selection"):
        verify_trained_candidate(tmp_path, key, 43, files)
    with pytest.raises(FileExistsError, match="immutable"):
        record_trained_candidate(tmp_path, key, 42, files, {}, metrics, evidence)
    tampered = {**candidate, "implementation_sha256": {"claimed-author-pin": "a" * 64}}
    (tmp_path / "training-provenance.json").write_text(json.dumps(tampered))
    with pytest.raises(ValueError, match="local implementation checksum"):
        verify_trained_candidate(tmp_path, key, 42, files)
    (tmp_path / "training-provenance.json").write_text(json.dumps(candidate))
    (tmp_path / files[0]).write_bytes(b"substituted-release")
    with pytest.raises(ValueError, match="checksum"):
        verify_trained_candidate(tmp_path, key, 42, files)


def test_trained_robotics_candidate_rejects_registration_without_real_updates(tmp_path):
    from auto_research.reproductions.lewam.external import record_trained_candidate
    with pytest.raises(ValueError, match="actual gradients and parameter updates"):
        record_trained_candidate(tmp_path, "lewam", 42, (), {},
            {"nonzero_gradient_updates": 0, "parameter_sample_delta_l2": 0})
    assert not (tmp_path / "training-provenance.json").exists()


@pytest.mark.parametrize("updates,delta", [(float("nan"), 1.0), (float("inf"), 1.0),
    (1.5, 1.0), (True, 1.0), (1, float("nan")), (1, float("inf")), (1, True), (1, -1.0)])
def test_trained_robotics_candidate_fails_closed_for_nonfinite_or_noninteger_evidence(tmp_path, updates, delta):
    from auto_research.reproductions.lewam.external import record_trained_candidate, verify_trained_candidate
    with pytest.raises(ValueError, match="actual gradients and parameter updates"):
        record_trained_candidate(tmp_path, "lewam", 42, (), {},
            {"nonzero_gradient_updates": updates, "parameter_sample_delta_l2": delta})
    metrics, evidence = candidate_evidence("lewam")
    manifest = record_trained_candidate(tmp_path, "lewam", 42, (), {}, metrics, evidence)
    manifest["metrics"] = {"nonzero_gradient_updates": updates, "parameter_sample_delta_l2": delta}
    (tmp_path / "training-provenance.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="actual update evidence"):
        verify_trained_candidate(tmp_path, "lewam", 42, ())


@pytest.mark.parametrize("key", ["lewam", "smolwam"])
@pytest.mark.parametrize("damage", ["nan_loss", "inf_gradient", "missing_loss", "missing_validation_metric"])
def test_trained_candidate_rejects_nonfinite_or_incomplete_defining_evidence(tmp_path, key, damage):
    from auto_research.reproductions.lewam.external import record_trained_candidate, verify_trained_candidate
    metrics, evidence = candidate_evidence(key)
    manifest = record_trained_candidate(tmp_path, key, 42, (), {}, metrics, evidence)
    rows = evidence["batches" if key == "lewam" else "losses"]
    loss = "state" if key == "lewam" else "kd_world_l1"
    if damage == "nan_loss":
        rows[0][loss] = float("nan")
    elif damage == "inf_gradient":
        if key == "lewam":
            evidence["gradients"][0] = float("inf")
        else:
            evidence["gradients"][0]["norm"] = float("inf")
    elif damage == "missing_loss":
        del rows[0][loss]
    else:
        del metrics["validation_action_loss" if key == "lewam" else "best_validation_action_l1"]
    other = tmp_path / "bad-training"
    other.mkdir()
    with pytest.raises(ValueError):
        record_trained_candidate(other, key, 42, (), {}, metrics, evidence)
    manifest["metrics"], manifest["training_evidence"] = metrics, evidence
    (tmp_path / "training-provenance.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        verify_trained_candidate(tmp_path, key, 42, ())


@pytest.mark.parametrize("tasks", [None, ["libero_10:2"], ["libero_goal:6", "libero_10:2"]])
def test_new_smolwam_student_cannot_use_default_or_different_training_task(tasks):
    from auto_research.reproductions.smolwam.worker import run
    with pytest.raises(ValueError, match="explicit same-training-task"):
        run({"trained_model_dir": "unread-fixture", **({"tasks": tasks} if tasks is not None else {})})


@pytest.mark.parametrize("dtype", [np.float32, np.float64])
@pytest.mark.parametrize("partial_numpy_core_shim", [False, True])
def test_libero_verified_numpy_init_states_load_weights_only_without_global_patch(
        tmp_path, dtype, partial_numpy_core_shim, monkeypatch):
    from types import SimpleNamespace
    from auto_research.reproductions.smolwam.worker import load_initial_states
    from auto_research.reproductions.lewam.external import PINS
    relative = "libero/libero/init_files/libero_goal/task.pruned_init"
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    expected = np.arange(8, dtype=dtype).reshape(2, 4)
    torch.save(expected, path)
    manifest = {"public_id": "Lifelong-Robot-Learning/LIBERO", "revision": PINS["libero"],
                "files": {relative: hashlib.sha256(path.read_bytes()).hexdigest()}}
    (tmp_path / "provenance.json").write_text(json.dumps(manifest))
    if partial_numpy_core_shim:
        # Real remote NumPy 1.26.3 exposes this incomplete compatibility shim.
        monkeypatch.setattr(np, "_core", SimpleNamespace(), raising=False)
    with torch.serialization.safe_globals([np.ndarray]):
        before = set(torch.serialization.get_safe_globals())
        actual = load_initial_states(tmp_path, SimpleNamespace(problem_folder="libero_goal", init_states_file="task.pruned_init"))
        np.testing.assert_array_equal(actual, expected)
        assert set(torch.serialization.get_safe_globals()) == before
    path.write_bytes(b"substituted-unverified-input")
    with pytest.raises(ValueError, match="checksum"):
        load_initial_states(tmp_path, SimpleNamespace(problem_folder="libero_goal", init_states_file="task.pruned_init"))


def test_libero_init_states_reject_unknown_pickle_global_even_when_byte_manifest_matches(tmp_path):
    from types import SimpleNamespace
    from auto_research.reproductions.smolwam.worker import load_initial_states
    from auto_research.reproductions.lewam.external import PINS
    relative = "libero/libero/init_files/libero_goal/task.pruned_init"
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    torch.save(Path("unknown-fixture-class"), path)
    (tmp_path / "provenance.json").write_text(json.dumps({"public_id": "Lifelong-Robot-Learning/LIBERO",
        "revision": PINS["libero"], "files": {relative: hashlib.sha256(path.read_bytes()).hexdigest()}}))
    with pytest.raises(ValueError, match="unsupported pickle globals"):
        load_initial_states(tmp_path, SimpleNamespace(problem_folder="libero_goal", init_states_file="task.pruned_init"))


def test_training_adapter_extraction_never_injects_released_student_weights(tmp_path):
    from safetensors.torch import load_file, save_file
    from auto_research.reproductions.smolwam.training import extract_latent_adapter
    expected = {"adapter.scale": torch.ones(2, 3), "adapter_inv.scale": torch.ones(2, 3)}
    source, target = tmp_path / "released.safetensors", tmp_path / "adapter.safetensors"
    save_file({**expected, "text_proj.weight": torch.ones(768, 1024), "trunk.weight": torch.ones(3)}, str(source))
    info = extract_latent_adapter(source, target, expected)
    actual = load_file(str(target))
    assert set(actual) == set(expected)
    assert info["released_trunk_text_or_student_weights_loaded"] is False
    assert info["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert info["sha256"] == hashlib.sha256(target.read_bytes()).hexdigest()
    for name in expected:
        torch.testing.assert_close(actual[name], expected[name])


@pytest.mark.parametrize("failure", ["missing_inverse", "shape", "nan", "inf", "non_adapter_template"])
def test_training_adapter_extraction_rejects_incomplete_or_invalid_native_adapter(tmp_path, failure):
    from safetensors.torch import save_file
    from auto_research.reproductions.smolwam.training import extract_latent_adapter
    expected = {"adapter.scale": torch.ones(2, 3), "adapter_inv.scale": torch.ones(2, 3)}
    state = {name: value.clone() for name, value in expected.items()}
    if failure == "missing_inverse":
        del state["adapter_inv.scale"]
    elif failure == "shape":
        state["adapter.scale"] = torch.ones(1)
    elif failure in {"nan", "inf"}:
        state["adapter.scale"][0, 0] = float(failure)
    else:
        expected["text_proj.weight"] = torch.ones(1)
    source, target = tmp_path / "released.safetensors", tmp_path / "adapter.safetensors"
    save_file(state, str(source))
    with pytest.raises(ValueError):
        extract_latent_adapter(source, target, expected)
    assert not target.exists()


@pytest.mark.parametrize("key,identifier", [("lewam", "2610.12818"), ("smolwam", "2610.13740"),
    ("near", "2610.13314"), ("beyond-final-embedding", "2610.13277"), ("skilldreamer", "2609.01642")])
def test_oct13_owned_paper_metadata_and_documentation_are_complete(key, identifier):
    from auto_research.paper_specs.schema import load_spec, validate_spec
    root = Path(__file__).resolve().parents[2]
    module = key.replace("-", "_")
    spec = load_spec(root / "src/auto_research/reproductions" / module / "paper.yaml")
    assert validate_spec(spec, root=root) == []
    assert spec.execution["requires_gpu_validation"] is True
    accelerator = "a30" if key in {"near", "beyond-final-embedding"} else "a100"
    assert spec.execution["gpu_validation_artifact"] == f"docs/gpu-validations/oct13-{key}-{accelerator}.json"
    assert spec.evolve_operators == ()  # no registry-only evolve integration claim
    readme = root / "docs/reproductions" / f"{identifier}-{key}" / "README.md"
    text = readme.read_text()
    for field in ("论文链接", "公司/机构", "首次公开日期", "原文开源代码", "Adapter", "本地复现代码"):
        assert "| " + field + " |" in text
    assert f"| 首次公开日期 | {spec.published}（arXiv v1） |" in text
    for heading in ("## 原始论文总结", "### 背景与主要改动", "### 核心公式", "### 论文离线与线上效果", "## 本地复现"):
        assert heading in text
    assert "```mermaid" in text
    assert (readme.parent / "assets/architecture.mmd").is_file()
    assert (readme.parent / "assets/source-provenance.json").is_file()
    metrics = list((readme.parent / "metrics").glob("*.json"))
    assert metrics and all(path.name in text for path in metrics)
    for path in metrics:
        if path.name in {"implementation-contract.json", "cpu-smoke-seed42.json"}:
            assert json.loads(path.read_text())["diagnostic_only"] is True
    if key == "skilldreamer":
        assert spec.published == "2026-08-28" and "不计作 2026-10 新 v1" in text
