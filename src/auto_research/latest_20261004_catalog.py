"""Deprecated intake-batch view; edit paper_specs/catalog instead."""

from .paper_specs.catalog import legacy_records

LATEST_METHOD_PAPERS = legacy_records(
    (
        (
            ("agent-research", "sira"),
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
            ("agent-research", "aira2"),
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
            ("agent-research", "pahf"),
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
            ("agent-research", "hyperagents"),
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
