"""Load authored, source-backed questions. Never fabricate a fallback Q&A."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path


SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def load_questions(root: Path, papers: dict[str, dict]) -> dict[str, list[dict]]:
    bank = {}
    for path in sorted((root / "docs/learning/questions").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("schema_version") != 1 or not isinstance(
            payload.get("papers"), dict
        ):
            raise ValueError(f"invalid question-bank schema: {path}")
        for identity, entry in payload["papers"].items():
            if identity not in papers:
                raise ValueError(f"unknown question-bank paper: {identity}")
            if identity in bank:
                raise ValueError(f"duplicate question-bank paper: {identity}")
            questions = entry.get("questions") if isinstance(entry, dict) else None
            if not isinstance(questions, list) or not questions:
                raise ValueError(f"paper needs authored questions: {identity}")
            source = (root / "docs" / papers[identity]["detail_path"]).read_text(encoding="utf-8")
            headings = source_headings(source)
            ids = set()
            for question in questions:
                if not isinstance(question, dict):
                    raise ValueError(f"invalid question: {identity}")
                key = question.get("id", "")
                if not isinstance(key, str) or not SLUG.fullmatch(key) or key in ids:
                    raise ValueError(f"invalid or duplicate question ID: {identity}: {key}")
                ids.add(key)
                for field in ("question", "answer", "example", "added"):
                    if not isinstance(question.get(field), str) or not question[field].strip():
                        raise ValueError(f"question needs {field}: {identity}/{key}")
                try:
                    if date.fromisoformat(question["added"]).isoformat() != question["added"]:
                        raise ValueError()
                except ValueError as error:
                    raise ValueError(f"invalid question date: {identity}/{key}") from error
                sections = question.get("source_sections")
                if not isinstance(sections, list) or not sections or any(
                    not isinstance(section, str) or section not in headings for section in sections
                ):
                    raise ValueError(f"question references missing source section: {identity}/{key}: {sections}")
            bank[identity] = questions
    return bank


def source_headings(source: str) -> set[str]:
    """Ignore fenced examples when validating provenance labels."""
    result = set()
    fence = ""
    fence_length = 0
    for line in source.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            run = marker.group(1)
            if not fence:
                fence = run[0]
                fence_length = len(run)
            elif run[0] == fence and len(run) >= fence_length and not marker.group(2).strip():
                fence = ""
            continue
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line) if not fence else None
        if match:
            result.add(match.group(1))
    return result


def question_anchor(identity: str, question_id: str) -> str:
    return "qa-" + hashlib.sha256(f"{identity}/{question_id}".encode()).hexdigest()[:16]


def question_count(cards: list[dict]) -> int:
    return sum(len(card.get("questions", [])) for card in cards)


def require_complete(cards: list[dict]) -> None:
    missing = [card["identity"] for card in cards if not card.get("questions")]
    if missing:
        raise ValueError(f"{len(missing)} papers need authored Q&A: " + ", ".join(missing[:20]))
