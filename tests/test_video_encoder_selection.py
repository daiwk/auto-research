"""Conditional source selector: numerical, quota and information boundaries."""
from __future__ import annotations

import json
import importlib.util
from pathlib import Path

import pytest
import torch

from auto_research.foundation_models.video_encoder_selection import (
    CorrespondenceEdge, correspondence_graph, dpp_kernels, dpp_residual,
    greedy_source_indices, question_relevance, quotas_from_representatives,
    select_source_tokens,
)


def fixture():
    z = torch.tensor([[[2., 0., 0.], [1.9, .1, 0.], [0., 1., 0.], [0., 0., 1.]],
                      [[1.9, .2, 0.], [1.8, .3, 0.], [0., .9, .1], [0., .1, .9]]])
    positions = torch.tensor([[[t, x, y] for x, y in ((0., 0.), (.3, 0.), (0., .7), (.7, .7))]
                              for t in (0., 1.)])
    return z, positions, torch.tensor([[1., 0., 0.], [0., 1., 0.]])


def test_equations_relevance_quality_and_schur_complement_match_independent_determinants():
    z, _, questions = fixture()
    relevance = question_relevance(z, questions)
    expected = torch.tensor([[max(float(torch.dot(v, q) / v.norm() / q.norm())
                                  for q in questions) for v in frame] for frame in z], dtype=torch.float64)
    torch.testing.assert_close(relevance, expected, atol=1e-7, rtol=1e-7)
    kernels = dpp_kernels(z, relevance)
    for frame, kernel in enumerate(kernels):
        raw = z[frame].double().norm(dim=-1) * (1 + .8 * relevance[frame])
        quality = raw / raw.mean()
        unit = z[frame].double() / z[frame].double().norm(dim=-1, keepdim=True)
        reference = torch.diag(quality) @ (unit @ unit.T) @ torch.diag(quality)
        reference += .001 * quality.square().mean() * torch.eye(4, dtype=torch.float64)
        torch.testing.assert_close(kernel, reference)
        for retained in ([], [0], [0, 2]):
            residuals = dpp_residual(kernel, retained)
            old_det = float(torch.linalg.det(kernel[retained][:, retained])) if retained else 1.
            for candidate in set(range(4)) - set(retained):
                combined = retained + [candidate]
                expected = float(torch.linalg.det(kernel[combined][:, combined])) / old_det
                assert float(residuals[candidate]) == pytest.approx(expected, rel=1e-9)


def test_negative_question_relevance_is_not_clipped_to_saliency():
    score = question_relevance(torch.tensor([[[1., 0.], [0., 1.]]]), torch.tensor([[-1., 0.]]))
    assert score.tolist() == [[-1., 0.]]


def test_fixed_odd_budget_keeps_original_embeddings_positions_and_every_stream():
    z, positions, q = fixture()
    z.requires_grad_(True)
    stream = torch.arange(2 * 4 * 2).reshape(2, 4, 2)
    result = select_source_tokens(z, q, positions, torch.tensor([2, 1]), torch.ones(1),
                                  streams={"intermediate": stream})
    assert len(result.indices) == 3 == len(set(result.indices.tolist()))
    assert torch.bincount(result.indices // 4, minlength=2).tolist() == [2, 1]
    torch.testing.assert_close(result.embeddings, z.flatten(0, 1)[result.indices])
    torch.testing.assert_close(result.positions, positions.flatten(0, 1)[result.indices])
    torch.testing.assert_close(result.streams["intermediate"], stream.flatten(0, 1)[result.indices])
    assert not result.embeddings.requires_grad
    assert result.positions.tolist() == sorted(result.positions.tolist())
    assert sum(len(move["indices"]) for move in result.trace) == 3


@pytest.mark.parametrize("quotas", [[0, 0], [0, 4], [4, 4], [3, 2]])
def test_zero_full_and_asymmetric_quotas_complete_exactly(quotas):
    z, positions, q = fixture()
    result = select_source_tokens(z, q, positions, torch.tensor(quotas), torch.ones(1))
    assert len(result.indices) == sum(quotas)
    assert torch.bincount(result.indices // 4, minlength=2).tolist() == quotas


@pytest.mark.parametrize("quotas", [[-1, 2], [5, 0], [1.5, 1.5], [1]])
def test_invalid_quotas_are_not_repaired_silently(quotas):
    z, positions, q = fixture()
    with pytest.raises(ValueError, match="quota"):
        select_source_tokens(z, q, positions, torch.tensor(quotas), torch.ones(1))


def test_representative_quota_inheritance_including_clipped_duplicate_slots():
    result = quotas_from_representatives(torch.tensor([0, 0, 0, 0, 0]), frames=3,
                                         tokens_per_frame=2, budget=5)
    assert result.tolist() == [2, 2, 1]
    assert quotas_from_representatives(torch.tensor([], dtype=torch.long), frames=2,
                                       tokens_per_frame=2, budget=0).tolist() == [0, 0]
    with pytest.raises(ValueError, match="outside"):
        quotas_from_representatives(torch.tensor([9]), frames=2, tokens_per_frame=2, budget=1)


def test_pair_complementarity_is_real_and_ties_choose_singleton():
    kernels = torch.eye(2, dtype=torch.float64).repeat(2, 1, 1)
    selected, trace = greedy_source_indices(kernels, torch.tensor([1, 1]),
                                           (CorrespondenceEdge(1, 3, .8),))
    assert selected == [1, 3]
    assert len(trace) == 1 and trace[0]["score_per_token"] == pytest.approx(.8)
    selected, trace = greedy_source_indices(kernels, torch.tensor([1, 1]),
                                           (CorrespondenceEdge(1, 3, 0.),))
    assert selected == [0, 2]
    assert all(len(move["indices"]) == 1 for move in trace)


def test_dpp_rejects_duplicate_directions_in_favor_of_diversity():
    z = torch.tensor([[[1., 0.], [1., 0.], [0., 1.]]])
    kernel = dpp_kernels(z, torch.zeros(1, 3))
    selected, _ = greedy_source_indices(kernel, torch.tensor([2]), ())
    assert selected == [0, 2]


def test_correspondence_requires_mutual_margin_scene_and_spatial_gates():
    z = torch.tensor([[[1., 0.], [0., 1.]], [[.98, .2], [.2, .98]]])
    positions = torch.tensor([[[0., 0., 0.], [0., 1., 1.]],
                              [[1., .1, 0.], [1., .9, 1.]]])
    edges = correspondence_graph(z, positions, torch.ones(1))
    assert [(e.first, e.second) for e in edges] == [(0, 2), (1, 3)]
    cosine = float(torch.nn.functional.cosine_similarity(z[0, 0], z[1, 0], dim=0))
    distance = .1 / 2**.5
    expected = (cosine - .65) / .35 * max(distance / .25, 2 * (1 - cosine))
    assert edges[0].weight == pytest.approx(expected, rel=1e-6)
    assert correspondence_graph(z, positions, torch.tensor([.64])) == ()
    wrong_positions = positions.clone()
    wrong_positions[1] = positions[1].flip(0)
    assert correspondence_graph(z, wrong_positions, torch.ones(1)) == ()
    duplicate = torch.ones_like(z)
    assert correspondence_graph(duplicate, positions, torch.ones(1)) == ()


@pytest.mark.parametrize("field", ["feature", "question", "position", "scene"])
def test_nonfinite_inputs_are_rejected(field):
    z, positions, q = fixture()
    scene = torch.ones(1)
    target = {"feature": z, "question": q, "position": positions, "scene": scene}[field]
    target.flatten()[0] = float("nan")
    with pytest.raises(ValueError, match="finite"):
        select_source_tokens(z, q, positions, torch.tensor([1, 1]), scene)


def test_duplicate_source_identity_and_misaligned_stream_are_rejected():
    z, positions, q = fixture()
    positions[0, 1] = positions[0, 0]
    with pytest.raises(ValueError, match="unique"):
        select_source_tokens(z, q, positions, torch.tensor([1, 1]), torch.ones(1))
    _, positions, _ = fixture()
    with pytest.raises(ValueError, match="stream"):
        select_source_tokens(z, q, positions, torch.tensor([1, 1]), torch.ones(1),
                             streams={"bad": torch.zeros(2, 3)})


def test_no_answer_argument_or_random_feature_fallback_in_core():
    import inspect
    from auto_research.foundation_models import video_encoder_selection
    signature = inspect.signature(select_source_tokens)
    assert not {"answer", "gold", "labels", "reference"} & set(signature.parameters)
    assert "torch.randn" not in inspect.getsource(video_encoder_selection)


def script(name):
    path = Path(__file__).resolve().parents[1] / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runner_rejects_answers_instead_of_reading_them(tmp_path):
    runner = script("run_video_encoder_selection")
    manifest = {"dataset_id": "public", "dataset_revision": "sha256:public-content", "examples": [
        {"id": "1", "video": "a.mp4", "question": "What changes?", "source_url": "https://example.org/video"}
    ]}
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest))
    _, rows = runner.load_manifest(path, 1)
    assert rows[0]["video"] == tmp_path / "a.mp4"
    manifest["examples"][0]["answer"] = "never an encoder input"
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="forbidden"):
        runner.load_manifest(path, 1)


def test_runner_keeps_failure_and_success_without_retrying_or_omitting(tmp_path, monkeypatch):
    runner = script("run_video_encoder_selection")
    z, positions, q = fixture()
    class Loader:
        def extract(self, frames, question, fragments):
            assert question == "What changes?" and fragments == []
            return z, q, positions, {"source": z.clone()}
    failed, success = tmp_path / "failed.mp4", tmp_path / "success.mp4"
    success.write_bytes(b"public-video-fixture-content-hash-only")
    def decode(path, count):
        if path == failed:
            raise ValueError("retained decode failure")
        return [(None, 0, 0.), (None, 1, 1.)]
    monkeypatch.setattr(runner, "decode_frames", decode)
    examples = [{"id": str(index), "video": path, "question": "What changes?"}
                for index, path in enumerate((failed, success))]
    persisted = []
    rows = runner.run_cases(examples, Loader(), frames=2, budget=3,
                            checkpoint_save=lambda values: persisted.append([dict(row) for row in values]))
    assert [row["status"] for row in rows] == ["failed", "passed"]
    assert len(persisted[0]) == 1 and persisted[0][0]["error"] == "retained decode failure"
    assert len(persisted[1]) == 2 and persisted[1][0] == persisted[0][0]


def test_checkpoint_feature_backend_is_framewise_and_question_does_not_enter_vision():
    from types import SimpleNamespace
    from PIL import Image
    runner = script("run_video_encoder_selection")
    class Connector:
        def __call__(self, visual):
            return visual
        def pixel_shuffle(self, visual, scale):
            assert scale == 1
            return visual
    embedding = torch.nn.Embedding.from_pretrained(torch.eye(3))
    visual_calls = []
    def vision_model(*, pixel_values):
        visual_calls.append(pixel_values.clone())
        return SimpleNamespace(last_hidden_state=pixel_values.permute(0, 2, 3, 1).reshape(1, 4, 3))
    backend = runner.FrozenSmolVLMFeatures.__new__(runner.FrozenSmolVLMFeatures)
    backend.device = "cpu"
    backend.processor = SimpleNamespace(
        image_processor=SimpleNamespace(image_mean=[0., 0., 0.], image_std=[1., 1., 1.]),
        tokenizer=lambda text, **kwargs: {"input_ids": torch.tensor([[1 if text == "first" else 2]])})
    backend.model = SimpleNamespace(
        model=SimpleNamespace(vision_model=vision_model, connector=Connector()),
        config=SimpleNamespace(vision_config=SimpleNamespace(image_size=2, patch_size=1), scale_factor=1),
        get_input_embeddings=lambda: embedding)
    frames = [(Image.new("RGB", (2, 2), "red"), 0, .1), (Image.new("RGB", (2, 2), "blue"), 9, .9)]
    first = backend.extract(frames, "first", [])
    second = backend.extract(frames, "second", [])
    torch.testing.assert_close(first[0], second[0])
    assert not torch.equal(first[1], second[1])
    changed = backend.extract([frames[0], (Image.new("RGB", (2, 2), "green"), 9, .9)], "first", [])
    torch.testing.assert_close(first[0][0], changed[0][0])
    assert not torch.equal(first[0][1], changed[0][1])
    assert len(visual_calls) == 6 and all(call.shape == (1, 3, 2, 2) for call in visual_calls)
    assert first[2][:, 0, 0].tolist() == [.1, .9]


def test_curator_rejects_partial_proxy_or_misaligned_evidence():
    import copy
    runner, curator = script("run_video_encoder_selection"), script("curate_video_encoder_selection")
    z, positions, q = fixture()
    positions[..., 1:] = torch.tensor([[.25, .25], [.25, .75], [.75, .25], [.75, .75]])
    evaluation = runner.evaluate_features(z, q, positions, {"source": z.clone()}, 3)
    report = {
        "adapter_key": "video-encoder-selection", "status": "passed",
        "protocol_id": runner.PROTOCOL, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
        "promotion_eligible": False, "evolve_integrated": False,
        "checkpoint": {"id": "public/frozen", "revision": "a" * 40,
                       "content_sha256": "b" * 64, "files_sha256": {"config.json": "c" * 64}},
        "dataset": {"examples": 1},
        "protocol": {"frozen_real_image_encoder": True, "independent_frame_encoding": True,
                     "question_input_embedding_mean": True, "inference_gold_read": False,
                     "test_read": False, "training_steps": 0, "refiner_enabled": False,
                     "quota_source": "external_uniform_not_SITE",
                     "scene_statistic": "explicit_mean_pooled_visual_cosine_proxy",
                     "full_SITE_selection_reproduced": False, "video_QA_capability_evaluated": False,
                     "budget": 3, "frames": 2},
        "rows": [{"id": "1", "status": "passed", "video_sha256": "d" * 64,
                  "source_frame_indices": [0, 1], "source_timestamps": [0., 1.], **evaluation}],
    }
    assert curator.summarize(report)["examples"] == 1
    for kind in ("missing", "failed", "source", "gold", "SITE"):
        bad = copy.deepcopy(report)
        if kind == "missing":
            bad["rows"] = []
        elif kind == "failed":
            bad["rows"][0]["status"] = "failed"
        elif kind == "source":
            bad["rows"][0]["metrics"]["source_embedding_max_error"] = .1
        elif kind == "gold":
            bad["protocol"]["inference_gold_read"] = True
        else:
            bad["protocol"]["full_SITE_selection_reproduced"] = True
        with pytest.raises(ValueError):
            curator.summarize(bad)


def test_paper_metadata_and_l1_boundaries_are_explicit():
    root = Path(__file__).resolve().parents[1]
    spec = json.loads((root / "src/auto_research/paper_specs/catalog/foundation-models/video-encoder-selection.json").read_text())
    assert spec["adapter"] is None and spec["evolve_integrated"] is False
    assert spec["diagnostic_only"] is True and spec["promotion_eligible"] is False
    assert spec["published"] == "2026-10-05"
    text = (root / "docs" / spec["detail_path"]).read_text()
    for required in ("论文信息", "原作者代码", "本地复现代码", "2026-10-05", "SITE", "96 GPU", "未报告"):
        assert required in text
