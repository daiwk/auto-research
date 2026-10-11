import pytest

from auto_research.post_training.pivot_intent import banking_holdout, intent_prediction, intent_prompt, intent_reward

LABELS = ["cash_withdrawal", "cash_withdrawal_charge", "transfer"]


def test_final_field_first_valid_label_not_candidate_or_shorter_prefix():
    response = "Candidates: transfer\nIntent Category: cash_withdrawal_charge then cash_withdrawal"
    assert intent_prediction(response, LABELS) == "cash_withdrawal_charge"
    assert intent_prediction("Candidates: transfer", LABELS) is None
    assert intent_prediction("Intent Category: nonsense", LABELS) is None


def test_rewards_are_external_and_structured_without_none_success():
    response = "**Analysis:** bank query\n**Candidates:** transfer, cash_withdrawal\n**Reasoning:** transfer fits\n**Intent Category:** transfer"
    value, stats = intent_reward(response, "transfer", LABELS)
    assert value == 1.6 and stats["correct"]
    assert intent_reward(response, "cash_withdrawal", LABELS)[0] == -.4
    assert intent_reward("invalid", "transfer", LABELS)[0] == -1.5
    with pytest.raises(ValueError):
        intent_reward("invalid", "unknown", LABELS)


def test_prompt_has_no_reference_argument_or_answer_leak():
    prompt = intent_prompt("user message", LABELS)
    assert prompt.endswith("user message") and "Candidates:" in prompt
    with pytest.raises(TypeError):
        intent_prompt("user message", LABELS, answer="secret gold")


def test_class_balanced_train_only_holdout_is_deterministic_and_disjoint():
    csv = "text,category\n" + "".join(f"{label} question {i},{label}\n" for label in LABELS for i in range(4))
    first = banking_holdout(csv, LABELS, shots=2)
    assert first == banking_holdout(csv, LABELS, shots=2)
    train, valid, _ = first
    assert len(train) == 6 and len(valid) == 3
    assert not {r["question"] for r in train} & {r["question"] for r in valid}
    assert all(sum(r["answer"] == label for r in train) == 2 for label in LABELS)
