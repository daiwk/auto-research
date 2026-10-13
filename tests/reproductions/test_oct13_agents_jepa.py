from __future__ import annotations

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
        return ('{"capabilities":[{"requirement":"compute a percentage"}],"semantic_anchors":["sale"]}'
                if len(prompts) == 1 else "# Hypothetical procedure\nCalculate the sale percentage.")
    pseudo, anchors = prospective_skills("calculate sale", generator)
    assert len(prompts) == 2 and anchors == ["sale"] and "Hypothetical" in pseudo[0]
    with pytest.raises(ValueError):
        prospective_skills("task", lambda _: "invalid")


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


@pytest.mark.parametrize("key,identifier", [("lewam", "2610.12818"), ("smolwam", "2610.13740"),
    ("near", "2610.13314"), ("beyond-final-embedding", "2610.13277"), ("skilldreamer", "2609.01642")])
def test_oct13_owned_paper_metadata_and_documentation_are_complete(key, identifier):
    from auto_research.paper_specs.schema import load_spec, validate_spec
    root = Path(__file__).resolve().parents[2]
    module = key.replace("-", "_")
    spec = load_spec(root / "src/auto_research/reproductions" / module / "paper.yaml")
    assert validate_spec(spec, root=root) == []
    assert spec.execution["requires_gpu_validation"] is True
    assert spec.execution["gpu_validation_artifact"] == f"docs/gpu-validations/oct13-{key}-a100.json"
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
