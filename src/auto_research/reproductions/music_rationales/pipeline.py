"""Offline LLM profile generation, catalog grounding, and online cache fallback."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Callable

from .data import Artist, MusicData, cf_candidates


Generate = Callable[[str], str]


@dataclass(frozen=True)
class Nomination:
    artist_id: int
    rationale: str


@dataclass(frozen=True)
class Profile:
    user_id: int
    nominations: tuple[Nomination, ...]


def _first_json_list(text: str) -> list:
    decoder = json.JSONDecoder()
    for index, character in enumerate(text):
        if character != "[":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, list):
            return value
    return []


def canonicalize(name_or_id: object, artists: dict[int, Artist]) -> int | None:
    try:
        candidate = int(name_or_id)
    except (TypeError, ValueError):
        candidate = None
    if candidate in artists:
        return candidate
    normalized = re.sub(r"\s+", " ", str(name_or_id).casefold()).strip()
    matches = [key for key, artist in artists.items()
               if re.sub(r"\s+", " ", artist.name.casefold()).strip() == normalized]
    return matches[0] if len(matches) == 1 else None


def generate_profile(data: MusicData, user: int, generate: Generate, *,
                     candidate_limit: int = 30, output_limit: int = 5) -> tuple[Profile, dict]:
    history = data.train[user]
    candidates = cf_candidates(data, user, limit=candidate_limit)
    seeds = sorted(history, key=lambda artist: (-len(data.artists[artist].tags), artist))[:12]
    seed_lines = [f"{data.artists[key].name} | {', '.join(data.artists[key].tags[:3])}"
                  for key in seeds]
    candidate_lines = [f"{key} | {data.artists[key].name} | "
                       f"{', '.join(data.artists[key].tags[:3])}"
                       for key in candidates]
    prompt = (
        "You are an artist discovery assistant. Use the listening history and public artist "
        "tags to discover artists the listener has NOT heard. From the candidate catalog, "
        "select at most five different IDs. Explain each link by naming one artist from the "
        "known list and one music tag shared with the candidate. Use ONLY the displayed "
        "artist names and tags; do not assert birthplace, nationality, career or album facts. "
        "Return ONLY a JSON array of objects with keys artist_id (integer) and rationale "
        "(one brief sentence mentioning the known artist and shared tag). Never invent an artist.\n"
        "Known artists:\n" + "\n".join(seed_lines) + "\nCandidate catalog:\n"
        + "\n".join(candidate_lines)
    )
    raw = generate(prompt)
    allowed = set(candidates)
    nominations = []
    rejected = {"invalid_entity": 0, "familiar": 0, "not_in_candidate_pool": 0,
                "empty_rationale": 0, "unsupported_rationale": 0, "duplicate": 0}
    for row in _first_json_list(raw):
        if not isinstance(row, dict):
            continue
        key = canonicalize(row.get("artist_id"), data.artists)
        if key is None:
            rejected["invalid_entity"] += 1
            continue
        if key in history:
            rejected["familiar"] += 1
            continue
        if key not in allowed:
            rejected["not_in_candidate_pool"] += 1
            continue
        rationale = str(row.get("rationale") or row.get("rational") or "").strip()
        if not rationale:
            rejected["empty_rationale"] += 1
            continue
        # A public catalog is not a factual music KG. Accept only explanations
        # whose artist and shared tag can be grounded in *displayed* data.
        lower = rationale.casefold()
        candidate_tags = {tag.casefold() for tag in data.artists[key].tags[:3]}
        supported = any(
            artist.name.casefold() in lower and any(
                tag in lower for tag in candidate_tags.intersection(
                    tag.casefold() for tag in artist.tags[:3]
                )
            )
            for seed in seeds if (artist := data.artists[seed])
        )
        if not supported:
            rejected["unsupported_rationale"] += 1
            continue
        if any(value.artist_id == key for value in nominations):
            rejected["duplicate"] += 1
            continue
        nominations.append(Nomination(key, rationale))
        if len(nominations) == output_limit:
            break
    return Profile(user, tuple(nominations)), {
        "prompt_chars": len(prompt), "candidate_count": len(candidates),
        "accepted": len(nominations), "rejected": rejected,
    }


def serve(data: MusicData, user: int, cache: dict[int, Profile], *,
          limit: int = 5) -> tuple[Nomination, ...]:
    """A live request never calls an LLM; nominations augment the CF slate."""
    cached = cache.get(user)
    slate = list(cached.nominations[:limit]) if cached else []
    seen = {row.artist_id for row in slate}
    for item in cf_candidates(data, user, limit=limit + len(slate)):
        if item not in seen:
            slate.append(Nomination(
                item, f"Listeners of your favorite artists also explored {data.artists[item].name}."
            ))
            seen.add(item)
        if len(slate) == limit:
            break
    return tuple(slate)


def annotate_baseline(data: MusicData, user: int, cache: dict[int, Profile], *,
                      limit: int = 5) -> tuple[Nomination, ...]:
    """Attach cached explanations to an unchanged CF slate (annotation-only arm)."""
    cached = cache.get(user)
    rationales = {row.artist_id: row.rationale for row in cached.nominations} if cached else {}
    return tuple(Nomination(
        item, rationales.get(
            item, f"Listeners of your favorite artists also explored {data.artists[item].name}."
        ),
    ) for item in cf_candidates(data, user, limit=limit))
