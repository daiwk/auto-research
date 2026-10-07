"""Deprecated intake-batch view; edit paper_specs/catalog instead."""

from .paper_specs.catalog import legacy_records

LATEST_METHOD_PAPERS = legacy_records(
    (
        (
            ("foundation-models", "gliclass"),
            {},
            (
                "domain",
                "key",
                "title",
                "paper_url",
                "detail_path",
                "topic",
                "first_author",
                "first_author_affiliation",
                "published",
                "code",
                "adapter",
                "priority",
            ),
        ),
        (
            ("post-training", "rlcr"),
            {},
            (
                "domain",
                "key",
                "title",
                "paper_url",
                "detail_path",
                "topic",
                "first_author",
                "first_author_affiliation",
                "published",
                "code",
                "adapter",
                "priority",
            ),
        ),
        (
            ("post-training", "calibration-aware-rl"),
            {},
            (
                "domain",
                "key",
                "title",
                "paper_url",
                "detail_path",
                "topic",
                "first_author",
                "first_author_affiliation",
                "published",
                "code",
                "adapter",
                "priority",
            ),
        ),
    )
)
