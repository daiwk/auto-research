import math

from auto_research.experiments import matrix_factorization_rmse, ngram_perplexity


def test_ngram_perplexity_is_finite():
    text = ("to be or not to be, that is the question.\n" * 500)
    value = ngram_perplexity(text, {"order": 3, "alpha": 0.1, "train_chars": 12000})
    assert value > 1
    assert math.isfinite(value)


def test_matrix_factorization_is_deterministic():
    ratings = [
        (user, item, float(1 + (user + item) % 5), index)
        for index, (user, item) in enumerate(
            ([(u, i) for u in range(1, 8) for i in range(1, 9)]) * 3
        )
    ]
    params = {"factors": 3, "learning_rate": 0.01, "regularization": 0.05, "epochs": 2}
    first = matrix_factorization_rmse(ratings, params, seed=7)
    second = matrix_factorization_rmse(ratings, params, seed=7)
    assert first == second
    assert math.isfinite(first)
