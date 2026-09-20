from __future__ import annotations

import csv
import json

import pytest

from auto_research.protocols import get_protocol
from auto_research.evolution import EvolutionConfig, Genome
from auto_research.evolution.system_one import SystemOneEvolutionEvaluator
from auto_research.system_one import (
    ChoiceQuestion,
    LocalDecisionModel,
    LocalSystemOneProvider,
    NoulQuestion,
    ScoreQuestion,
    SystemOneBenchmarkConfig,
    SystemOneRequest,
    TypeSafeHTTPProvider,
    run_system_one_benchmark,
)
from auto_research.system_one.local import DecisionTrainingExample


def test_contracts_cover_choice_score_and_noul_without_generated_answers():
    model = LocalDecisionModel(32, seed=7)
    response = LocalSystemOneProvider(model).decide(SystemOneRequest(
        state="The transfer has not arrived",
        questions={
            "route": ChoiceQuestion("Route this ticket", {"card": "card issue", "transfer": "bank transfer"}),
            "urgency": ScoreQuestion("Rate urgency", {"1": "low", "2": "high"}),
            "escalate": NoulQuestion("The ticket requires escalation"),
        },
    ))
    assert set(response.answers) == {"route", "urgency", "escalate"}
    assert response.answers["route"].value in {"card", "transfer"}
    assert isinstance(response.answers["urgency"].value, float)
    assert isinstance(response.answers["escalate"].value, bool)
    for answer in response.answers.values():
        assert sum(answer.probabilities.values()) == pytest.approx(1.0)


def test_online_provider_keeps_secret_in_header_and_validates_question_ids():
    captured = {}

    def transport(url, headers, body, timeout):
        captured.update(url=url, headers=headers, body=json.loads(body), timeout=timeout)
        return {
            "model": "jev-1.13.0",
            "answers": {"route": {"type": "choice", "choice": "transfer", "confidence": 0.7,
                                      "probabilities": {"card": 0.2, "transfer": 0.8}}},
            "usage": {"input_tokens": 10, "output_tokens": 4},
        }

    provider = TypeSafeHTTPProvider("secret", transport=transport)
    response = provider.decide(SystemOneRequest("late transfer", {
        "route": ChoiceQuestion("route", {"card": "card", "transfer": "transfer"})
    }))
    assert response.answers["route"].value == "transfer"
    assert captured["headers"]["authorization"] == "Bearer secret"
    assert "secret" not in json.dumps(captured["body"])


def test_local_training_improves_tiny_dynamic_candidate_task():
    criteria = {"card": "card payment", "cash": "cash withdrawal"}
    rows = (
        DecisionTrainingExample("cash machine kept my cash", "intent", criteria, "cash"),
        DecisionTrainingExample("cash withdrawal fee", "intent", criteria, "cash"),
        DecisionTrainingExample("card payment reversed", "intent", criteria, "card"),
        DecisionTrainingExample("card payment declined", "intent", criteria, "card"),
    )
    model = LocalDecisionModel(64, architecture="rival_attention", objective="hybrid", seed=3)
    before = sum(max(model.predict(row.state, row.instructions, row.criteria), key=model.predict(row.state, row.instructions, row.criteria).get) == row.target for row in rows)
    model.fit(rows, steps=400, learning_rate=0.15, seed=3)
    after = sum(max(model.predict(row.state, row.instructions, row.criteria), key=model.predict(row.state, row.instructions, row.criteria).get) == row.target for row in rows)
    assert after >= before
    assert after == len(rows)


def test_banking77_benchmark_writes_three_seed_public_artifact(tmp_path):
    dataset = tmp_path / "data"
    dataset.mkdir()
    train = [
        ("cash withdrawal fee", "cash_withdrawal"),
        ("cash machine issue", "cash_withdrawal"),
        ("card payment declined", "card_payment"),
        ("card charged twice", "card_payment"),
    ]
    test = [
        ("withdraw cash", "cash_withdrawal"),
        ("cash fee", "cash_withdrawal"),
        ("payment card", "card_payment"),
        ("card decline", "card_payment"),
    ]
    for name, rows in (("train.csv", train), ("test.csv", test)):
        with (dataset / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(("text", "category"))
            writer.writerows(rows)
    result, run_dir = run_system_one_benchmark(SystemOneBenchmarkConfig(
        dataset_dir=dataset, output_dir=tmp_path / "runs", dimensions=32,
        steps=120, seeds=(1, 2, 3), allow_network=False,
        maximum_train_examples=None, maximum_eval_examples=None,
    ))
    assert len(result["runs"]) == 3
    assert result["dataset_summary"]["test_isolation"] is True
    assert (run_dir / "result.json").exists()
    assert get_protocol("foundation.banking77.system_one.v1").primary_metric == "accuracy"


def test_system_one_evolve_operator_executes_instead_of_only_registering(tmp_path):
    directory = tmp_path / "data" / "system-one"
    directory.mkdir(parents=True)
    rows = {
        "train.csv": [("cash withdrawal fee", "cash"), ("card declined", "card")],
        "test.csv": [
            ("cash machine", "cash"), ("withdraw fee", "cash"),
            ("card payment", "card"), ("payment declined", "card"),
        ],
    }
    for name, data in rows.items():
        with (directory / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(("text", "category"))
            writer.writerows(data)
    config = EvolutionConfig(
        model="system-one", dataset="banking77", dataset_dir=tmp_path / "data",
        steps=30, seeds=(42,), maximum_examples=2, allow_network=False,
    )
    evaluator = SystemOneEvolutionEvaluator(config, tmp_path)
    trial = evaluator.evaluate(
        "g1-t1", 1, None,
        Genome(architecture="system-one:rival-hybrid", dimensions=32, learning_rate=0.1),
        ("2507.16806", "2601.13284"), "proper-scoring comparison",
    )
    assert trial.status == "completed"
    assert trial.training["test_read_during_selection"] is False
    assert "accuracy" in trial.validation and "brier" in trial.validation
