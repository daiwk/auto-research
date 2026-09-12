import json

import numpy as np
import pytest

from auto_research.reproductions import autolr_product


def test_checkpoint_proposals_train_validate_resume_and_test_once(tmp_path, monkeypatch):
    calls, training = [], []

    def train(data, seed, steps, **parameters):
        training.append((steps, parameters))
        return np.array([[parameters["learning_rate"]]]), {"last_loss": .1}

    def evaluate(data, scorer, target_split):
        calls.append(target_split)
        return {"ndcg_at_10": float(scorer([0])[0]), "hit_at_10": 1.0}

    proposal_rounds = []

    def generate(prompt):
        payload = json.loads(prompt.split("\n", 1)[1])
        if prompt.startswith("Propose"):
            context = payload["validation_context"]
            assert all("test" not in row["metrics"] for row in context["records"])
            proposal_rounds.append(len(context["records"]))
            return json.dumps({"proposals": [{"dimensions": 16, "learning_rate": .004 + .001 * len(context["records"]), "adapter": True}]})
        return '{"feasible":true,"score":0.5,"reason":"within scope"}'

    monkeypatch.setattr(autolr_product, "train_two_tower", train)
    monkeypatch.setattr(autolr_product, "evaluate", evaluate)
    result = autolr_product.research(None, {"sha": "fixed"}, generate, tmp_path, rounds=3, steps=5, seeds=(42,))
    assert proposal_rounds == [0, 1, 2]
    assert calls.count("test") == 1 and calls[-1] == "test"
    assert [budget for budget, _ in training] == [5, 1, 5, 1, 5, 1, 5, 5]
    assert all("execution-verified" in row["events"] for row in result["records"])
    before = len(training)
    restored = autolr_product.research(None, {"sha": "fixed"}, generate, tmp_path, rounds=3, steps=5, seeds=(42,))
    assert restored == result and len(training) == before
    with pytest.raises(ValueError, match="resume contract"):
        autolr_product.research(None, {"sha": "fixed"}, generate, tmp_path, rounds=4, steps=5, seeds=(42,))


@pytest.mark.parametrize("parameters", [
    {"dimensions": 16, "learning_rate": .003, "adapter": True, "command": "anything"},
    {"dimensions": 16, "learning_rate": float("nan"), "adapter": True},
    {"dimensions": 16, "learning_rate": .003, "adapter": "false"},
])
def test_proposals_cannot_inject_unexecuted_or_unbounded_axes(parameters):
    with pytest.raises(ValueError):
        autolr_product.parse_parameters(parameters)
