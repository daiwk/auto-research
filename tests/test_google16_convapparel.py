from dataclasses import fields, replace

import pytest

from auto_research.agent_research.google16_convapparel import (
    Conversation,
    DiscriminatorView,
    alignment_test,
    behavior_metrics,
    counterfactual_validation,
    evaluate_hls,
    ks_statistic,
    mann_whitney_u,
    plsa,
    train_logistic_discriminator,
)


def conversation(index, human=True, policy="good", text=None, participant=None):
    return Conversation(str(index), participant or f"p{index}", policy, (text or ("please blue coat thanks" if human else "certainly optimal curated attire"),), human, (("satisfaction", 0.7 if human else 0.9),))


def test_plsa_is_population_alignment_and_exact_statistics_include_ties():
    assert ks_statistic([1, 1, 2], [1, 2, 2]) == pytest.approx(1 / 3)
    assert mann_whitney_u([1, 2], [2, 3]) == 0.5
    result = alignment_test([0, 0], [1, 1])
    assert result["ks"] == 1
    assert result["ks_pvalue"] == pytest.approx(2 / 6)
    assert result["mwu_pvalue"] == pytest.approx(2 / 6)
    assert result["pvalue_method"] == "exact_permutation"
    assert alignment_test([1, 1], [1, 1])["ks_pvalue"] == 1


def test_permutation_fallback_is_seeded_with_plus_one_correction():
    first = alignment_test(range(6), range(6, 12), exact_limit=1, permutations=19, seed=7)
    assert first == alignment_test(range(6), range(6, 12), exact_limit=1, permutations=19, seed=7)
    assert first["ks_pvalue"] >= 1 / 20


def test_basic_statistics_do_not_invent_latent_experience_labels():
    c = Conversation("a", "p", "good", ("one two", "three"), True)
    assert behavior_metrics(c) == {"turns_per_session": 2.0, "words_per_user_turn": 1.5}
    with pytest.raises(ValueError, match="same annotation schema"):
        plsa([c], [conversation("b", False)])


def test_trained_cpu_discriminator_generalizes_fixture_styles_but_is_not_paper_model():
    train = [conversation(i, i % 2 == 0) for i in range(12)]
    heldout = [conversation(i, i % 2 == 0, "bad") for i in range(20, 26)]
    simulator_training = [c for c in train if c.is_human]
    sessions = tuple(c.session_id for c in simulator_training)
    heldout = [replace(c, simulator_training_sessions=sessions) if not c.is_human else c for c in heldout]
    model = train_logistic_discriminator(train)
    result = counterfactual_validation(simulator_training, heldout, model, training_policy="good", target_policy="bad")
    assert result["hls"]["discriminator_accuracy"] == 1
    assert result["hls"]["brier_score"] < 0.1
    assert result["diagnostic_only"]
    assert result["discriminator_backend"] == "cpu_bag_of_words_logistic_not_paper_gemini"


def test_hls_callback_does_not_receive_gold_or_source_metadata():
    seen = []

    def score(view):
        seen.append(view)
        return 0.4

    result = evaluate_hls([conversation(1), conversation(2, False)], score)
    assert result["simulated_hls"] == 0.4
    assert all(type(view) is DiscriminatorView for view in seen)
    assert {field.name for field in fields(DiscriminatorView)} == {"user_turns"}


def test_session_participant_and_counterfactual_policy_leakage_rejected():
    train = [conversation(1), conversation(2, False)]
    model = train_logistic_discriminator(train)
    with pytest.raises(ValueError, match="training identity"):
        evaluate_hls(train, model)
    with pytest.raises(ValueError, match="participant_id leakage"):
        counterfactual_validation([train[0]], [conversation(3, participant="p1"), conversation(4, False)], model, training_policy="good", target_policy="bad")
    with pytest.raises(ValueError, match="unseen target"):
        counterfactual_validation([train[0]], [conversation(3), conversation(4, False)], model, training_policy="good", target_policy="bad")
    with pytest.raises(ValueError, match="human probability"):
        evaluate_hls([conversation(3), conversation(4, False)], lambda view: float("nan"))


def test_cross_policy_validation_does_not_confuse_discriminator_and_simulator_training():
    train = [conversation(1), conversation(2, False)]
    model = train_logistic_discriminator(train)
    heldout = [conversation(3, True, "bad"), conversation(4, False, "bad")]
    with pytest.raises(ValueError, match="simulator training provenance"):
        counterfactual_validation([train[0]], heldout, model, training_policy="good", target_policy="bad")
    with pytest.raises(ValueError, match="human source-policy"):
        counterfactual_validation(train, heldout, model, training_policy="good", target_policy="bad")
