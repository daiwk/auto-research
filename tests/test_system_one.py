from __future__ import annotations

import csv
import json
from types import SimpleNamespace

import pytest

from auto_research.protocols import get_protocol
from auto_research.evolution import EvolutionConfig, Genome
from auto_research.evolution.system_one import SystemOneEvolutionEvaluator
from auto_research.evolution.report import render_dashboard, render_evolution_report
from auto_research.system_one import (
    ChoiceQuestion,
    LocalDecisionModel,
    LocalSystemOneProvider,
    NoulQuestion,
    NANOJEV_REVISION,
    NanoJevProvider,
    NimbleProvider,
    LayaProvider,
    ScoreQuestion,
    SystemOneBenchmarkConfig,
    SystemOneRequest,
    TypeSafeHTTPProvider,
    run_system_one_benchmark,
    evaluate_public_decisions,
    load_public_decisions,
    split_public_decisions,
)
from auto_research.system_one.local import DecisionTrainingExample


class FakeNanoJevPredictor:
    def __init__(self):
        self.payload = None
        self.options = None

    def predict(self, payload, *, batch_questions=0, temperature=1.0):
        self.payload = payload
        self.options = (batch_questions, temperature)
        return {
            "execution": {
                "candidate_paths": 7,
                "forward_passes": 1,
                "autoregressive_decode_steps": 0,
            },
            "states": [{
                "id": "request",
                "answers": {
                    "route": {
                        "type": "choice",
                        "probabilities": {"card": 0.2, "transfer": 0.8},
                        "choice": "transfer",
                    },
                    "urgency": {
                        "type": "score",
                        "probabilities": {"0": 0.25, "1": 0.75},
                        "score": 0.75,
                    },
                    "escalate": {
                        "type": "boolean",
                        "probabilities": {"false": 0.4, "true": 0.6},
                        "p_true": 0.6,
                    },
                },
            }],
        }


class FakeNimbleScorer:
    def __init__(self):
        self.context = None
        self.schema = None

    def score(self, context, schema, score_fields=()):
        self.context, self.schema = context, schema
        return {"fields": {
            "route": {"logits": {"card": -1.0, "transfer": 2.0}},
            "urgency": {"logits": {"0": -1.0, "1": 1.0}},
            "escalate": {"logits": {"false": -0.5, "true": 0.5}},
        }}


class FakeLayaAgent:
    def __init__(self):
        self.state = None
        self.questions = None

    def system_one(self, state, questions):
        self.state, self.questions = state, questions
        return {"answers": {
            "route": {"probabilities": {"card": 0.1, "transfer": 0.9}},
            "urgency": {"probabilities": {"0": 0.2, "1": 0.8}},
            "escalate": {"noul": 0.7},
        }, "usage": {"forward_passes": 1}}


@pytest.mark.parametrize("provider", [
    NimbleProvider(FakeNimbleScorer()),
    LayaProvider(FakeLayaAgent()),
])
def test_open_checkpoint_providers_map_all_types_without_gold(provider):
    request = SystemOneRequest(
        {"message": "The transfer has not arrived"},
        {
            "route": ChoiceQuestion("Route", {"card": "card", "transfer": "transfer"}),
            "urgency": ScoreQuestion("Urgency", {"1": "low", "2": "high"}),
            "escalate": NoulQuestion("Escalate"),
        },
    )
    response = provider.decide(request)
    assert response.answers["route"].value == "transfer"
    assert response.answers["urgency"].value > 1.5
    assert response.answers["escalate"].value is True
    captured = getattr(provider, "scorer", getattr(provider, "agent", None))
    assert "gold" not in json.dumps(vars(captured)).lower()


def test_public_suite_keeps_references_out_of_requests_and_splits_by_family(tmp_path):
    records = [
        {
            "id": "choice-1", "domain": "intent", "family": "family-a",
            "input": {"state": "late transfer", "questions": {"decision": {
                "type": "choice", "instructions": "route", "criteria": {
                    "card": "card", "transfer": "transfer"}}}},
            "reference": {"target": "transfer", "human_reviewed": True},
        },
        {
            "id": "noul-1", "domain": "safety", "family": "family-b",
            "input": {"state": "unsafe", "questions": {"decision": {
                "type": "noul", "instructions": "escalate"}}},
            "reference": {"target": True, "human_reviewed": True},
        },
        {
            "id": "score-1", "domain": "quality", "family": "family-c",
            "input": {"state": "excellent", "questions": {"decision": {
                "type": "score", "instructions": "quality", "criteria": ["low", "high"]}}},
            "reference": {"target": 1, "human_reviewed": True},
        },
    ]
    path = tmp_path / "suite.jsonl"
    path.write_text("\n".join(json.dumps(row) for row in records) + "\n")
    rows = load_public_decisions(path)
    validation, test = split_public_decisions(rows)
    assert {row.family for row in validation}.isdisjoint({row.family for row in test})
    assert "reference" not in json.dumps(rows[0].request.to_dict()).lower()

    class PerfectProvider:
        def decide(self, request):
            key, question = next(iter(request.questions.items()))
            if isinstance(question, ChoiceQuestion):
                answer = {"type": "choice", "choice": "transfer", "probabilities": {"card": 0.0, "transfer": 1.0}}
            elif isinstance(question, NoulQuestion):
                answer = {"type": "noul", "noul": 1.0}
            else:
                answer = {"type": "score", "score": 1.0, "probabilities": {"0": 0.0, "1": 1.0}}
            from auto_research.system_one import SystemOneResponse
            return SystemOneResponse.from_payload({"model": "perfect", "answers": {key: answer}})

    metrics = evaluate_public_decisions(PerfectProvider(), rows, 0.8)
    assert metrics["accuracy"] == 1.0
    assert set(metrics["by_type"]) == {"choice", "noul", "score"}


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


def test_nanojev_provider_maps_all_typed_questions_without_gold_or_decoding():
    predictor = FakeNanoJevPredictor()
    provider = NanoJevProvider(
        predictor, temperature=0.9, batch_questions=3
    )
    response = provider.decide(SystemOneRequest(
        state={"message": "The transfer has not arrived"},
        questions={
            "route": ChoiceQuestion(
                "Route this ticket", {"card": "card issue", "transfer": "bank transfer"}
            ),
            "urgency": ScoreQuestion("Rate urgency", {"1": "low", "2": "high"}),
            "escalate": NoulQuestion("The ticket requires escalation"),
        },
    ))
    questions = predictor.payload["states"][0]["questions"]
    assert questions["escalate"]["type"] == "boolean"
    assert questions["urgency"]["criteria"] == ["low", "high"]
    assert "gold" not in json.dumps(predictor.payload).lower()
    assert response.answers["route"].value == "transfer"
    assert response.answers["urgency"].value == pytest.approx(1.75)
    assert response.answers["escalate"].value is True
    assert response.usage == {
        "candidate_paths": 7,
        "forward_passes": 1,
        "autoregressive_decode_steps": 0,
    }
    assert response.model.endswith(f"@{NANOJEV_REVISION}")
    assert predictor.options == (3, 0.9)


def test_nanojev_provider_rejects_probability_labels_that_do_not_match_request():
    class BrokenPredictor:
        def predict(self, payload, **kwargs):
            return {
                "states": [{
                    "id": "request",
                    "answers": {"route": {
                        "type": "choice",
                        "probabilities": {"unexpected": 1.0},
                    }},
                }],
            }

    provider = NanoJevProvider(BrokenPredictor())
    with pytest.raises(ValueError, match="probability labels"):
        provider.decide(SystemOneRequest(
            "late transfer",
            {"route": ChoiceQuestion("route", {"card": "card", "transfer": "transfer"})},
        ))


def test_system_one_config_keeps_nanojev_checkpoint_revision_immutable():
    config = SystemOneBenchmarkConfig(backend="nanojev")
    config.validate()
    assert config.checkpoint_revision is None


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


def test_system_one_checkpoint_operators_are_only_executable_with_real_paths(tmp_path, monkeypatch):
    records = []
    for index, family in enumerate(("a", "b", "c", "d")):
        records.append({
            "id": str(index), "domain": "routing", "family": family,
            "input": {"state": "late transfer", "questions": {"decision": {
                "type": "choice", "instructions": "route",
                "criteria": {"card": "card", "transfer": "transfer"}}}},
            "reference": {"target": "transfer", "human_reviewed": True},
        })
    suite = tmp_path / "suite.jsonl"
    suite.write_text("\n".join(json.dumps(row) for row in records) + "\n")
    checkpoint = tmp_path / "nimble"
    checkpoint.mkdir()
    config = EvolutionConfig(
        model="system-one", dataset="system-one-public",
        system_one_public_data=suite, system_one_nimble_checkpoint=checkpoint,
        direction="compare public checkpoints", allow_network=False,
    )
    evaluator = SystemOneEvolutionEvaluator(config, tmp_path)
    assert evaluator.executable_operators == ("system-one:nimble",)

    class PerfectProvider:
        def decide(self, request):
            key = next(iter(request.questions))
            from auto_research.system_one import SystemOneResponse
            return SystemOneResponse.from_payload({
                "model": "fake-nimble", "answers": {key: {
                    "type": "choice", "choice": "transfer",
                    "probabilities": {"card": 0.1, "transfer": 0.9},
                }},
            })

    monkeypatch.setattr(evaluator, "_load_external_provider", lambda *args: PerfectProvider())
    trial = evaluator.evaluate(
        "g1-t1", 1, None,
        Genome(architecture="system-one:nimble", system_one_temperature=0.7),
        ("2508.07662",), "real checkpoint comparison",
    )
    assert trial.training["external_checkpoint"] is True
    assert trial.validation["accuracy"] == 1.0


def test_formal_public_suite_uses_explicit_calibration_test_and_ood(tmp_path):
    from auto_research.system_one.public_suite import load_public_decision_splits

    rows = []
    for split in ("calibration", "test", "ood"):
        rows.append({
            "id": split, "domain": "routing", "family": f"family-{split}",
            "source": f"source-{split}", "split": split,
            "input": {"state": "late transfer", "questions": {"decision": {
                "type": "choice", "instructions": "route",
                "criteria": {"card": "card", "transfer": "transfer"}}}},
            "reference": {"target": "transfer", "human_reviewed": True},
        })
    path = tmp_path / "formal.jsonl"
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
    splits = load_public_decision_splits(path)
    assert [row.id for row in splits.calibration] == ["calibration"]
    assert [row.id for row in splits.test] == ["test"]
    assert [row.id for row in splits.ood] == ["ood"]


def test_formal_public_suite_rejects_incomplete_explicit_splits(tmp_path):
    from auto_research.system_one.public_suite import load_public_decision_splits

    path = tmp_path / "broken.jsonl"
    path.write_text(json.dumps({
        "id": "only-calibration", "split": "calibration",
        "input": {"state": "x", "questions": {"decision": {
            "type": "noul", "instructions": "yes?"}}},
        "reference": {"target": True},
    }) + "\n")
    with pytest.raises(ValueError, match="calibration and test"):
        load_public_decision_splits(path)


def test_formal_public_suite_rejects_modified_data(tmp_path):
    from auto_research.system_one.public_suite import load_public_decision_splits

    path = tmp_path / "formal.jsonl"
    path.write_text("{}\n")
    path.with_suffix(".manifest.json").write_text(json.dumps({
        "dataset_sha256": "0" * 64,
    }))
    with pytest.raises(ValueError, match="SHA256"):
        load_public_decision_splits(path)


def test_system_one_public_baseline_uses_configured_checkpoint(tmp_path):
    from auto_research.evolution.providers import get_provider

    data = tmp_path / "public.jsonl"
    data.write_text("{}\n", encoding="utf-8")
    config = EvolutionConfig(
        model="system-one",
        dataset="system-one-public",
        system_one_public_data=data,
        system_one_nimble_checkpoint=tmp_path / "nimble",
    )
    baseline = get_provider("system-one").baseline_factory(config)
    assert baseline.architecture == "system-one:nimble"


def test_system_one_aggregate_ignores_breakdown_dicts():
    from auto_research.system_one.benchmark import _aggregate_runs

    aggregate = _aggregate_runs([
        {"test": {"accuracy": 0.75, "by_type": {"choice": 0.75}}},
        {"test": {"accuracy": 0.25, "by_type": {"choice": 0.25}}},
    ])
    assert aggregate == {"accuracy_mean": 0.5, "accuracy_std": 0.25}


def test_nimble_checkpoint_hash_verifier_fails_closed(tmp_path):
    from auto_research.system_one.nimble import _assert_sha256

    weight = tmp_path / "adapter_model.safetensors"
    weight.write_bytes(b"tampered")
    with pytest.raises(ValueError, match="SHA256"):
        _assert_sha256(weight, "0" * 64, "Nimble adapter")


def test_system_one_reports_do_not_assume_recommendation_metrics():
    trial = SimpleNamespace(
        trial_id="g0-t0", generation=0, genome=Genome(architecture="system-one:nimble"),
        fitness=0.6, validation={"accuracy": 0.75, "coverage": 0.8, "score_mae": 0.3},
        status="completed", source_papers=(),
    )
    result = SimpleNamespace(
        config=SimpleNamespace(model="system-one", dataset="system-one-public",
                               system_one_public_data="data/system-one/public.jsonl"),
        dataset_summary={"validation_examples": 60, "test_examples": 60, "ood_examples": 80},
        trials=[trial], champion_id="g0-t0", rounds=[],
        baseline_test={"accuracy": 0.7, "ood_accuracy": 0.6},
        champion_test={"accuracy": 0.7, "ood_accuracy": 0.6},
    )
    report = render_evolution_report(result)
    dashboard = render_dashboard(result)
    assert "OOD：60 / 60 / 80" in report
    assert "ood_accuracy" in report
    assert "NDCG" not in report + dashboard
    assert "Coverage" in dashboard
