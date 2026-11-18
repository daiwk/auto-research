"""Paired-content token premium and non-inflatable abstention audit (2611.13441).

This CPU arithmetic component accepts external token counts/confidences. It does
not download tokenizers, train the paper's proprietary model, or infer gold labels.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable, Mapping, Sequence

REQUIRES_GPU_VALIDATION = False
UDHR_ARTICLES = (1, 2, 4, 5, 7, 8, *range(10, 31))


@dataclass(frozen=True)
class ArticleCount:
    tokens: int
    unknown_tokens: int = 0


def measure_aligned_texts(
    translated: Mapping[int, str], english: Mapping[int, str],
    tokenize: Callable[[str], Sequence[int]], *, unknown_token_id: int | None = None,
    required_articles: Sequence[int] = UDHR_ARTICLES,
) -> dict[str, object]:
    """Author script's procedure: join ordered common articles, tokenize ONCE.

Subword boundary merges mean summing independently tokenized articles need not
equal tokenizing their concatenation. No special tokens should be added by the
external tokenizer. Returned tokens, not gold answers, are the only inputs.
    """
    expected = set(required_articles)
    if not expected or len(expected) != len(required_articles):
        raise ValueError("required articles must be nonempty and unique")
    if set(translated) != expected or set(english) != expected:
        raise ValueError("both languages must cover exactly the same declared articles")
    if any(not isinstance(v, str) or not v.strip() for v in [*translated.values(), *english.values()]):
        raise ValueError("each aligned article must contain nonempty text")
    counts = []
    for articles in (translated, english):
        tokens = list(tokenize(" ".join(articles[i] for i in sorted(expected))))
        if not tokens or any(type(t) is not int for t in tokens):
            raise ValueError("tokenizer must return a nonempty sequence of integer token IDs")
        counts.append(ArticleCount(len(tokens), tokens.count(unknown_token_id)))
    result = tokenization_premium({0: counts[0]}, {0: counts[1]}, required_articles=[0])
    result["article_count"] = len(expected)
    result["tokenization_scope"] = "single-encoding-of-space-joined-ordered-articles"
    return result


def tokenization_premium(
    translated: Mapping[int, ArticleCount], english: Mapping[int, ArticleCount],
    *, required_articles: Sequence[int] = UDHR_ARTICLES,
) -> dict[str, object]:
    """Equation (1) readout: ratio of supplied total token counts, not mean ratios.

This readout cannot detect boundary merges. Use ``measure_aligned_texts`` for the
author's join-then-tokenize procedure; independently encoded per-article counts
are only a declared arithmetic diagnostic, not the original tokenizer protocol.

Any unknown token marks a cell unavailable: v1 gives no universal numeric UNK
threshold. This explicit conservative guard prevents a collapsed script from
being advertised as cheap. The caller must not silently delete failed articles.
    """
    expected = set(required_articles)
    if not expected or len(expected) != len(required_articles):
        raise ValueError("required articles must be nonempty and unique")
    if set(translated) != expected or set(english) != expected:
        raise ValueError("both languages must cover exactly the same declared articles")
    for count in [*translated.values(), *english.values()]:
        if (type(count.tokens) is not int or count.tokens <= 0
                or type(count.unknown_tokens) is not int
                or not 0 <= count.unknown_tokens <= count.tokens):
            raise ValueError("invalid token or unknown-token counts")
    source_total = sum(x.tokens for x in translated.values())
    reference_total = sum(x.tokens for x in english.values())
    unknown = sum(x.unknown_tokens for x in [*translated.values(), *english.values()])
    return {
        "premium": None if unknown else source_total / reference_total,
        "available": not bool(unknown),
        "exclusion_reason": "unknown-token-collapse-risk" if unknown else None,
        "translated_tokens": source_total, "english_tokens": reference_total,
        "unknown_tokens": unknown, "article_count": len(expected),
        "aggregation": "ratio-of-total-tokens-on-aligned-articles",
    }


def selective_audit(
    confidences: Sequence[float], correctness: Sequence[bool], *, threshold: float,
    bins: int = 10, total_energy_joules: float | None = None,
) -> dict[str, float | int | None]:
    """All-item ECE and thresholded coverage/risk; gold exists only here in scoring.

No-answer risk is unavailable, not zero. Energy must be measured across the full
evaluation, including rejected/abstained inputs; abstention cannot shrink it.
    """
    n = len(confidences)
    if not n or n != len(correctness) or bins < 1:
        raise ValueError("nonempty aligned arrays and positive bins required")
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("threshold must lie in [0,1]")
    if any(not math.isfinite(c) or not 0 <= c <= 1 for c in confidences):
        raise ValueError("confidences must lie in [0,1]")
    if any(type(c) is not bool for c in correctness):
        raise ValueError("correctness must contain booleans")
    groups: list[list[int]] = [[] for _ in range(bins)]
    for i, confidence in enumerate(confidences):
        groups[min(int(confidence * bins), bins - 1)].append(i)
    ece = sum(
        abs(sum(confidences[i] for i in group) - sum(correctness[i] for i in group)) / n
        for group in groups if group
    )
    accepted = [i for i, c in enumerate(confidences) if c >= threshold]
    correct = sum(correctness[i] for i in accepted)
    if total_energy_joules is not None and (
        not math.isfinite(total_energy_joules) or total_energy_joules <= 0
    ):
        raise ValueError("full-evaluation energy must be positive and finite")
    return {
        "examples": n, "answered": len(accepted), "correct_answered": correct,
        "coverage": len(accepted) / n,
        "risk": 1 - correct / len(accepted) if accepted else None,
        "all_item_ece": ece,
        "correct_answers_per_joule": correct / total_energy_joules if total_energy_joules else None,
    }


def diagnostic(seed: int, device: str = "cpu") -> dict[str, object]:
    if device != "cpu":
        raise ValueError("this arithmetic protocol supports CPU only")
    articles = [1, 2]
    premium = tokenization_premium(
        {1: ArticleCount(20), 2: ArticleCount(45)},
        {1: ArticleCount(10), 2: ArticleCount(30)}, required_articles=articles,
    )
    collapsed = tokenization_premium(
        {1: ArticleCount(1, 1), 2: ArticleCount(2, 1)},
        {1: ArticleCount(10), 2: ArticleCount(30)}, required_articles=articles,
    )
    confidence, gold = [0.9, 0.8, 0.6, 0.2], [True, False, True, False]
    low = selective_audit(confidence, gold, threshold=0.1, total_energy_joules=10)
    high = selective_audit(confidence, gold, threshold=0.85, total_energy_joules=10)
    none = selective_audit(confidence, gold, threshold=1.0)
    rejected = False
    try:
        tokenization_premium({1: ArticleCount(2)}, {1: ArticleCount(1), 2: ArticleCount(1)},
                             required_articles=articles)
    except ValueError:
        rejected = True
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
        "checks": {
            "ratio_of_totals_not_mean_of_ratios": premium["premium"] == 65 / 40,
            "unknown_collapse_is_not_a_favorable_premium": collapsed["premium"] is None,
            "ece_does_not_drop_abstained_items": low["all_item_ece"] == high["all_item_ece"],
            "abstention_does_not_inflate_energy_efficiency": high["correct_answers_per_joule"] <= low["correct_answers_per_joule"],
            "zero_coverage_has_no_fictitious_zero_risk": none["risk"] is None,
            "unaligned_articles_rejected": rejected,
        },
        "metrics": {
            "fixture_token_premium": premium["premium"],
            "fixture_coverage": high["coverage"],
            "fixture_all_item_ece": high["all_item_ece"],
            "fixture_correct_answers_per_joule": high["correct_answers_per_joule"],
        },
    }
