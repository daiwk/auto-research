"""Stable source units for reviewed English learning content.

English strings are authored once. Renderers may reuse an English question in
its topic, the global bank, and recent additions without duplicating prose.
This module does not translate text or turn missing translations into pages.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any


TOPIC_FIELDS = ("title", "question", "takeaway", "example", "pitfall", "reading_order")
QA_FIELDS = ("question", "answer", "example")
CJK = re.compile(r"[\u3400-\u9fff]")


@dataclass(frozen=True)
class SourceUnit:
    fields: dict[str, str]
    source_sha256: str


def _unit(record: dict[str, Any], fields: tuple[str, ...]) -> SourceUnit:
    # Include non-prose context (such as levels and reference sections) in
    # provenance, but expose only translatable prose to the editor.
    serialized = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return SourceUnit(
        {key: record[key] for key in fields},
        sha256(serialized.encode("utf-8")).hexdigest(),
    )


def question_units(bank: dict[str, list[dict]]) -> dict[str, SourceUnit]:
    return {
        f"qa/{identity}/{question['id']}": _unit(question, QA_FIELDS)
        for identity, questions in bank.items() for question in questions
    }


def topic_units(themes: list[dict]) -> dict[str, SourceUnit]:
    units = {}
    for theme in themes:
        path = f"theme/{theme['id']}"
        units[path] = _unit({key: theme[key] for key in ("id", "title", "intro")}, ("title", "intro"))
        for topic in theme["topics"]:
            topic_path = f"{path}/{topic['id']}"
            # Membership and render-time counters are inherited; edits to those
            # alone do not invalidate prose that has not changed.
            units[topic_path] = _unit(
                {**{key: topic[key] for key in TOPIC_FIELDS}, "self_test": topic["self_test"]},
                TOPIC_FIELDS,
            )
            units[f"{topic_path}/self-test"] = _unit(topic["self_test"], ("question", "answer"))
    return units


def deep_dive_units(bank: dict[str, dict]) -> dict[str, SourceUnit]:
    units = {}
    for identity, record in bank.items():
        path = f"dive/{identity}"
        title = {key: record[key] for key in ("title", "thesis")}
        axes = {f"axis_{i}": axis for i, axis in enumerate(record["axes"])}
        units[path] = _unit(title | axes, tuple(title | axes))
        for row in record["comparisons"]:
            units[f"{path}/comparison/{row['paper']}"] = _unit(row, ("position", "tradeoff"))
        for i, row in enumerate(record["analysis"]):
            units[f"{path}/analysis/{i}"] = _unit(row, ("title", "body"))
        for row in record["questions"]:
            units[f"{path}/question/{row['id']}"] = _unit(row, QA_FIELDS)
        for i, row in enumerate(record["updates"]):
            units[f"{path}/update/{row['date']}/{i}"] = _unit(row, ("summary",))
    return units


def load_reviewed(directory: Path, units: dict[str, SourceUnit], *,
                  require_complete: bool = True) -> dict[str, dict[str, str]]:
    """Accept exact source-bound entries; reject unknown, stale, or draft prose."""
    localized = {}
    for path in sorted(directory.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("schema_version") != 1 or not isinstance(
            payload.get("units"), dict
        ):
            raise ValueError(f"invalid English learning source schema: {path}")
        for key, entry in payload["units"].items():
            if key not in units or key in localized:
                raise ValueError(f"unknown or duplicate English learning unit: {key}")
            source = units[key]
            if (not isinstance(entry, dict) or set(entry) != {"source_sha256", "reviewed", "fields"}
                    or entry.get("source_sha256") != source.source_sha256):
                raise ValueError(f"English learning source changed; review {key}")
            if entry["reviewed"] is not True:
                raise ValueError(f"English learning unit is not reviewed: {key}")
            fields = entry["fields"]
            if not isinstance(fields, dict) or set(fields) != set(source.fields) or any(
                not isinstance(value, str) or not value.strip() or CJK.search(value)
                for value in fields.values()
            ):
                raise ValueError(f"incomplete English learning prose: {key}")
            localized[key] = fields
    if require_complete and (missing := sorted(set(units) - set(localized))):
        raise ValueError(f"{len(missing)} English learning units missing: " + ", ".join(missing[:10]))
    return localized


def localize_questions(bank, english):
    """Inherit IDs, order, levels, dates, and source references from the canonical bank."""
    return {
        identity: [question | english[f"qa/{identity}/{question['id']}"] for question in questions]
        for identity, questions in bank.items()
    }


def localize_topics(themes, english):
    output = []
    for theme in themes:
        theme_path = f"theme/{theme['id']}"
        topics = []
        for topic in theme["topics"]:
            path = f"{theme_path}/{topic['id']}"
            topics.append(topic | english[path] | {"self_test": english[f"{path}/self-test"]})
        output.append(theme | english[theme_path] | {"topics": topics})
    return output


def localize_deep_dives(bank, english):
    output = {}
    for identity, record in bank.items():
        path = f"dive/{identity}"
        heading = english[path]
        output[identity] = record | {
            "title": heading["title"], "thesis": heading["thesis"],
            "axes": [heading[f"axis_{i}"] for i in range(len(record["axes"]))],
            "comparisons": [
                row | english[f"{path}/comparison/{row['paper']}"] for row in record["comparisons"]
            ],
            "analysis": [row | english[f"{path}/analysis/{i}"] for i, row in enumerate(record["analysis"])],
            "questions": [row | english[f"{path}/question/{row['id']}"] for row in record["questions"]],
            "updates": [row | english[f"{path}/update/{row['date']}/{i}"]
                        for i, row in enumerate(record["updates"])],
        }
    return output
