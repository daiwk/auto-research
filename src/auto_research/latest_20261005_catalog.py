"""Deprecated intake-batch view; edit paper_specs/catalog instead."""

from .paper_specs.catalog import legacy_records

LATEST_METHOD_PAPERS = legacy_records(
    (
        (
            ("agent-research", "depgpo"),
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
                "priority",
                "code",
                "adapter",
            ),
        ),
        (
            ("agent-research", "adastep"),
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
                "priority",
                "code",
                "adapter",
            ),
        ),
        (
            ("post-training", "follow-the-winners"),
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
                "priority",
                "code",
                "adapter",
            ),
        ),
        (
            ("post-training", "lesser"),
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
                "priority",
                "code",
                "adapter",
            ),
        ),
    )
)
