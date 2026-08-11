from __future__ import annotations

import json
from pathlib import Path
import pickle

import numpy as np

import pytest

from auto_research.cli import main
from auto_research.multimodal.benchmarks import (
    run_cifar10_benchmark, run_public_benchmark, score_benchmark,
)


def test_scienceqa_official_directory_and_multi_seed_random_baseline(tmp_path):
    annotation_dir = tmp_path / "scienceqa"
    annotation_dir.mkdir()
    (annotation_dir / "problems.json").write_text(json.dumps({
        "1": {"choices": ["red", "blue"], "answer": 0, "image": "1.png"},
        "2": {"choices": ["hot", "cold"], "answer": 1},
    }))
    (annotation_dir / "pid_splits.json").write_text(json.dumps({"test": ["1", "2"]}))
    result = run_public_benchmark(
        "scienceqa", annotation_dir, (42, 43, 44), baseline="random"
    )
    assert result.evaluated_examples == 2
    assert result.aggregate_metrics["accuracy"]["n"] == 3
    assert result.to_dict()["formal_comparison"] is False
    assert result.to_dict()["schema_version"] == 2
    assert result.to_dict()["evaluation_tier"] == "l2_public_benchmark"
    assert len(result.metadata["annotations_sha256"]) == 64


def test_multi_seed_predictions_must_be_independent_files(tmp_path):
    annotations = tmp_path / "pope.json"
    predictions = tmp_path / "predictions.json"
    annotations.write_text(json.dumps([{"question_id": 1, "answer": "yes"}]))
    predictions.write_text(json.dumps([{"id": 1, "prediction": "yes"}]))
    with pytest.raises(ValueError, match=r"requires \{seed\}"):
        run_public_benchmark(
            "pope", annotations, (1, 2, 3), predictions=str(predictions)
        )


def test_public_benchmark_can_score_the_same_fixed_subset_as_prediction(tmp_path):
    annotations = tmp_path / "scienceqa.json"
    predictions = tmp_path / "predictions.jsonl"
    annotations.write_text(json.dumps({
        str(index): {
            "split": "test", "question": "pick", "choices": ["x", "y"],
            "answer": index % 2,
        }
        for index in range(5)
    }))
    predictions.write_text("\n".join(
        json.dumps({"id": str(index), "prediction": index % 2})
        for index in range(3)
    ))
    result = run_public_benchmark(
        "scienceqa", annotations, (42,), predictions=str(predictions),
        maximum_examples=3,
    )
    assert result.evaluated_examples == 3
    assert result.aggregate_metrics["accuracy"]["mean"] == 1.0
    assert result.metadata["maximum_examples"] == 3


def test_scienceqa_accepts_choice_letters_and_reports_visual_slice():
    metrics, count = score_benchmark(
        "scienceqa",
        {"1": {"split": "test", "choices": ["x", "y"], "answer": 1, "image": "1.png"}},
        [{"id": "1", "prediction": "B"}],
    )
    assert count == 1
    assert metrics["accuracy"] == 1.0
    assert metrics["image_accuracy"] == 1.0
    assert metrics["parse_rate"] == 1.0


def test_pope_reports_official_binary_metrics():
    metrics, count = score_benchmark(
        "pope",
        [
            {"question_id": 1, "answer": "yes"},
            {"question_id": 2, "answer": "no"},
            {"question_id": 3, "answer": "yes"},
            {"question_id": 4, "answer": "no"},
        ],
        [
            {"id": 1, "prediction": "Yes."},
            {"id": 2, "prediction": "yes"},
            {"id": 3, "prediction": "no"},
            {"id": 4, "prediction": "no"},
        ],
    )
    assert count == 4
    assert metrics == {
        "accuracy": 0.5,
        "precision": 0.5,
        "recall": 0.5,
        "f1": 0.5,
        "yes_ratio": 0.5,
        "parse_rate": 1.0,
    }


def test_invalid_generated_answer_counts_as_wrong_instead_of_aborting():
    metrics, count = score_benchmark(
        "pope",
        [{"question_id": 1, "answer": "no"}],
        [{"id": 1, "prediction": "__invalid__"}],
    )
    assert count == 1
    assert metrics["accuracy"] == 0.0
    assert metrics["parse_rate"] == 0.0


@pytest.mark.parametrize("benchmark", ["coco-retrieval", "flickr30k-retrieval"])
def test_karpathy_retrieval_scores_both_directions(benchmark):
    annotations = {"images": [
        {"split": "test", "imgid": 10, "sentences": [{"sentid": 100}, {"sentid": 101}]},
        {"split": "test", "imgid": 20, "sentences": [{"sentid": 200}, {"sentid": 201}]},
    ]}
    predictions = [
        {"image_id": 10, "ranked_text_ids": [100, 200, 101, 201]},
        {"image_id": 20, "ranked_text_ids": [100, 200, 101, 201]},
        {"text_id": 100, "ranked_image_ids": [10, 20]},
        {"text_id": 101, "ranked_image_ids": [20, 10]},
        {"text_id": 200, "ranked_image_ids": [10, 20]},
        {"text_id": 201, "ranked_image_ids": [20, 10]},
    ]
    metrics, count = score_benchmark(benchmark, annotations, predictions)
    assert count == 6
    assert metrics["i2t_recall_at_1"] == 0.5
    assert metrics["i2t_recall_at_5"] == 1.0
    assert metrics["t2i_recall_at_1"] == 0.5
    assert metrics["mean_recall"] == pytest.approx(5 / 6)


def test_multimodal_eval_cli_writes_machine_and_human_reports(tmp_path):
    annotations = tmp_path / "pope.jsonl"
    annotations.write_text(
        '\n'.join(json.dumps(row) for row in [
            {"question_id": "q1", "answer": "yes"},
            {"question_id": "q2", "answer": "no"},
        ]) + '\n'
    )
    output = tmp_path / "runs"
    assert main([
        "multimodal-eval", "--benchmark", "pope",
        "--annotations", str(annotations), "--baseline", "random",
        "--seeds", "1,2,3", "--output-dir", str(output),
    ]) == 0
    run_dir = next(output.iterdir())
    payload = json.loads((run_dir / "metrics.json").read_text())
    assert payload["formal_comparison"] is False
    assert "not a model capability" in payload["claim_policy"]
    assert "random baseline" in (run_dir / "report.md").read_text()


def test_cifar_runner_is_l1_and_keeps_per_seed_results(tmp_path):
    extracted = tmp_path / "cifar10" / "cifar-10-batches-py"
    extracted.mkdir(parents=True)
    rng = np.random.default_rng(9)
    for filename in [*(f"data_batch_{index}" for index in range(1, 6)), "test_batch"]:
        with (extracted / filename).open("wb") as handle:
            pickle.dump({
                b"data": rng.integers(0, 256, size=(20, 3072), dtype=np.uint8),
                b"labels": (np.arange(20) % 10).tolist(),
            }, handle)
    result = run_cifar10_benchmark(
        tmp_path, (1, 2, 3), steps=1, maximum_examples=40,
        dimensions=32, batch_size=4, allow_network=False,
    )
    assert result.evaluation_tier == "l1_public_images"
    assert len(result.seed_results) == 3
    assert [row["seed"] for row in result.seed_results] == [1, 2, 3]
    assert result.aggregate_metrics["test_accuracy"]["n"] == 3
    assert result.metadata["train_examples"] == 40


def test_committed_cifar_metrics_are_auditable():
    path = Path(__file__).parents[1] / (
        "docs/multimodal-models/metrics/cifar10-qa-seeds42-44.json"
    )
    payload = json.loads(path.read_text())
    assert payload["schema_version"] == 2
    assert payload["seeds"] == [42, 43, 44]
    assert payload["formal_comparison"] is True
    assert payload["metadata"]["dataset_checksum_md5"] == "c58f30108f718f92721af3b95e74349a"
    assert payload["aggregate_metrics"]["test_accuracy"]["mean"] == pytest.approx(0.1943333348)
    assert payload["provenance"]["artifact_path"] == str(path.relative_to(path.parents[3]))
