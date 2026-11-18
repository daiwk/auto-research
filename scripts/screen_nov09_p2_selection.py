"""Apply the authorized window-only P2 selection policy to a frozen review pool.

This is a deterministic title/abstract *selection* screen, not a method review,
originality verdict, affiliation-exhaustion claim, cost assessment or implementation.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from route_nov09_title_abstract import digest, load_observations, normalized


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov09-review-closure"
WINDOW = {"start": "2026-10-16", "end": "2026-11-09"}
DECISION = "not_selected_this_window_p2"
SCOPE = "title-abstract-selection"
REASON = (
    "按当前研究优先级未纳入本窗口；仅完成标题摘要选题分流，不否定新算法或公开基准。"
    "未核验方法、完整实验成本或能力，不作为全局实质性拒绝或实施交付。"
)
PROTECTED_ROUTES = {
    "official_priority", "institution_name_verify", "metadata_conflict_verify",
    "production_signals", "industrial_application",
}
NON_WAIVABLE = {
    "source_priority_flag", "source_priority_query", "source_priority_organization",
    "official_source_domain", "metadata_conflict", "frozen_industrial_route",
    "policy_protected_identity",
}
TEXT_RULES = {
    # Case-sensitive Meta and FAIR avoid equating every meta-learning/fairness paper
    # with a company. Lowercase organizations remain protected in structured fields.
    "text_organization_mention": re.compile(r"\b(?:Google|DeepMind|Alphabet|Facebook|FAIR|Meta)\b"),
    "text_production_mention": re.compile(
        r"\b(?:production|customers?|A\s*/\s*B|online experiments?|live traffic|real traffic|"
        r"full[ -]traffic|commercial traffic)\b", re.I),
    "deployment_signal": re.compile(
        r"\b(?:deployed|deployments|we deploy|in use by|used by [0-9]|"
        r"real[ -]world users|real[ -]world clients)\b", re.I),
}
ORG_FIELDS = re.compile(r"\b(?:google|deepmind|alphabet|facebook|meta|fair)\b", re.I)
OFFICIAL_DOMAINS = {
    "research.google", "deepmind.google", "research.google.com", "ai.google",
    "ai.meta.com", "research.facebook.com", "about.fb.com", "engineering.fb.com",
    "ai.facebook.com", "facebookresearch.com",
}


def read(path: Path) -> dict:
    return json.loads(path.read_bytes())


def file_ref(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def resolve_ref(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def stable_json(value: dict) -> bytes:
    # One paper per line keeps the large, independently auditable screen reviewable.
    records = value.get("records")
    if records is None:
        return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
    head = {k: v for k, v in value.items() if k != "records"}
    lines = [json.dumps(head, ensure_ascii=False, indent=2)[:-2] + ',\n  "records": [']
    lines.extend("    " + json.dumps(row, ensure_ascii=False)
                 + ("," if i + 1 < len(records) else "") for i, row in enumerate(records))
    return ("\n".join([*lines, "  ]", "}"]) + "\n").encode()


def protection_signals(row: dict, frozen_route: str, policy: dict) -> dict[str, str]:
    """Return positive signals; absence never proves an author has no affiliation."""
    combined = f"{row['title']}\n{row['abstract']}"
    signals = {key: match[0] for key, pattern in TEXT_RULES.items()
               if (match := pattern.search(combined))}
    if row.get("priority_review_required"):
        signals["source_priority_flag"] = "priority_review_required=true"
    for field, rule in (("priority_query_matches", "source_priority_query"),
                        ("priority_source_matches", "source_priority_organization")):
        if row.get(field):
            signals[rule] = json.dumps(row[field], ensure_ascii=False)
    structured = {k: row[k] for k in (
        "organization", "organizations", "affiliation", "affiliations", "author_affiliations"
    ) if row.get(k)}
    if match := ORG_FIELDS.search(json.dumps(structured, ensure_ascii=False)):
        signals["source_priority_organization"] = match[0]
    official = sorted({host for source in row.get("source_provenance", [])
                       if (host := urlsplit(source.get("source_url", "")).hostname)
                       in OFFICIAL_DOMAINS})
    official_links = re.findall(
        r"https?://(?:github\.com/(?:google-research|google-deepmind|facebookresearch|meta-llama)"
        r"|(?:[\w-]+\.)?(?:research\.google|deepmind\.google|ai\.meta\.com))[^\s<]*",
        combined, re.I)
    if official or official_links:
        signals["official_source_domain"] = ", ".join([*official, *official_links])
    if row.get("metadata_conflicts") or frozen_route == "metadata_conflict_verify":
        signals["metadata_conflict"] = "conflicting captured metadata requires original check"
    if frozen_route == "official_priority":
        signals["source_priority_flag"] = "frozen route: official_priority"
    if frozen_route == "industrial_application":
        signals["frozen_industrial_route"] = "industrial_application"
    elif frozen_route in PROTECTED_ROUTES and not signals:
        signals["source_priority_flag"] = f"frozen route: {frozen_route}"
    if row["arxiv_id"] in policy["always_protected_identities"]:
        signals["policy_protected_identity"] = policy["always_protected_identities"][row["arxiv_id"]]
    return signals


def primary_exclusions(paths: list[Path], expected: dict[str, dict]) -> tuple[set[str], list[dict]]:
    excluded: set[str] = set()
    sources = []
    for path in sorted(paths, key=file_ref):
        artifact = read(path)
        reviews = artifact.get("reviews", [])
        if not isinstance(reviews, list):
            raise ValueError(f"{path}: primary reviews must be a list")
        for row in reviews:
            if row.get("id") not in expected:
                continue
            original = expected[row["id"]]
            if (row.get("review_done") is not True
                    or row.get("fulltext_review_completed") is not True
                    or not row.get("source_url") or not row.get("source_sha256")
                    or row.get("decision") not in {"rejected", "out_of_scope", "accepted", "reviewed_deferred"}
                    or not row.get("resolution") or not row.get("reason")
                    or any(row.get(key) != original[key] for key in (
                        "revision", "title", "published", "metadata_sha256"))):
                raise ValueError(f"{row.get('id')}: cannot exclude an incomplete primary review")
            excluded.add(row["id"])
        sources.append({"path": file_ref(path), "sha256": sha256(path.read_bytes()).hexdigest()})
    return excluded, sources


def signal_clarifications(paths: list[Path]) -> tuple[dict[str, list[dict]], list[dict]]:
    result: dict[str, list[dict]] = {}
    sources = []
    for path in sorted(paths, key=file_ref):
        artifact = read(path)
        rows = artifact.get("clarifications", artifact.get("records", []))
        for row in rows:
            result.setdefault(row["id"], []).append(row)
        sources.append({"path": file_ref(path), "sha256": sha256(path.read_bytes()).hexdigest()})
    return result, sources


def apply_clarifications(row: dict, signals: dict, clarifications: list[dict]) -> tuple[dict, list]:
    retained = dict(signals)
    used = []
    for item in clarifications:
        rules = item.get("cleared_protection_rules", [])
        if not rules:
            continue
        if (not set(rules) <= TEXT_RULES.keys()
                or set(rules) & NON_WAIVABLE
                or item.get("revision") != row["revision"]
                or item.get("metadata_sha256") != row["metadata_sha256"]
                or item.get("fulltext_review_completed") is not False
                or item.get("priority_attribution_verified") is not False
                or not item.get("reason")
                or not (item.get("abstract_witness") or item.get("title_witness"))
                or any(item.get(key) and item[key].casefold() not in row[field].casefold()
                       for key, field in (("title_witness", "title"), ("abstract_witness", "abstract")))):
            raise ValueError(f"{row['arxiv_id']}: invalid or overbroad signal clarification")
        for rule in rules:
            retained.pop(rule, None)
        used.append(item)
    return retained, used


def build(source_dir: Path, frozen: dict, policy: dict, *,
          exclude_primary_json: list[Path] | None = None,
          protection_review_json: list[Path] | None = None,
          frozen_bytes: bytes | None = None, policy_bytes: bytes | None = None) -> dict:
    if (frozen["window"] != WINDOW or policy["window"] != WINDOW
            or policy["terminal_selection_decision"] != DECISION
            or policy["review_scope"] != SCOPE
            or policy["authorization"]["p2_selection_closure_allowed"] is not True
            or frozen["source_inventory_sha256"] != policy["input_inventory_sha256"]
            or frozen["frozen_pending_count"] != policy["frozen_pending_count"]
            or sha256(frozen_bytes or stable_json(frozen)).hexdigest()
            != policy["frozen_input_sha256"]):
        raise ValueError("selection input or explicit window policy does not match")
    observations, receipts = load_observations(source_dir)
    if receipts != frozen["source_receipts"]:
        raise ValueError("frozen candidate capture receipts changed")
    frozen_ids = {r[0] for r in frozen["records"]}
    if len(frozen_ids) != len(frozen["records"]):
        raise ValueError("duplicate frozen identities")
    if len(frozen_ids) != frozen["frozen_pending_count"]:
        raise ValueError("frozen count does not match identities")
    expected = {r[0]: observations[r[0], r[1]] for r in frozen["records"]}
    excluded, primary_sources = primary_exclusions(exclude_primary_json or [], expected)
    clarifications, review_sources = signal_clarifications(protection_review_json or [])
    records, protected = [], []
    for identity, revision, tracks, prior_reason, frozen_route, route_witnesses in frozen["records"]:
        if identity in excluded:
            continue
        row = observations[identity, revision]
        local_day = datetime.fromisoformat(row["published"].replace("Z", "+00:00")).astimezone(
            ZoneInfo("Asia/Shanghai")).date().isoformat()
        if not WINDOW["start"] <= local_day <= WINDOW["end"]:
            raise ValueError(f"{identity}: published date is outside the authorized local window")
        abstract = row["abstract"]
        if not abstract.strip() or not row["title"].strip():
            raise ValueError(f"{identity}: missing title or abstract cannot be selection-screened")
        original_signals = protection_signals(row, frozen_route, policy)
        signals, clarification = apply_clarifications(
            row, original_signals, clarifications.get(identity, []))
        shared = {
            "id": identity, "revision": revision, "title": row["title"],
            "published": row["published"], "tracks": tracks,
            "source_url": f"https://arxiv.org/abs/{identity}v{revision}",
            "metadata_sha256": row["metadata_sha256"],
            "abstract_sha256": digest(abstract),
            "abstract_normalized_sha256": digest(normalized(abstract)),
            "capture": row["captures"][0], "capture_sha256": receipts[row["captures"][0]],
            "route": frozen_route, "route_witnesses": route_witnesses,
            "prior_review_routing_reason": prior_reason,
            "title_witness": row["title"],
            "abstract_witness": re.split(r"(?<=[.!?])\s+", abstract, maxsplit=1)[0],
            "scope": SCOPE, "method_verified": False,
            "method_review_completed": False, "fulltext_review_completed": False,
            "high_cost": False, "implementation": False,
            "originality_not_rejected": True,
            "automatic_retry": False, "automatic_implementation_queue": False,
            "positive_signal_matches": original_signals,
            "signal_clarifications": clarification,
        }
        if signals:
            protected.append(shared | {
                "decision": "protected_pending_original_review",
                "selection_review_done": False, "protection_reasons": signals,
            })
        else:
            records.append(shared | {
                "decision": DECISION, "priority": "P2", "selection_review_done": True,
                "reason": REASON,
            })
    selected_ids, protected_ids = ({r["id"] for r in entries} for entries in (records, protected))
    if (selected_ids & protected_ids or selected_ids & excluded or protected_ids & excluded
            or selected_ids | protected_ids | excluded != frozen_ids):
        raise ValueError("selected, protected and primary-excluded IDs must partition the frozen pool")
    return {
        "schema_version": 1, "policy": "p2-selection-policy.json", "window": WINDOW,
        "input": "p2-selection-input.json",
        "input_inventory_commit": frozen["source_inventory_commit"],
        "input_inventory_sha256": frozen["source_inventory_sha256"],
        "frozen_input_sha256": sha256(frozen_bytes or stable_json(frozen)).hexdigest(),
        "policy_sha256": sha256(policy_bytes or stable_json(policy)).hexdigest(),
        "source_receipts": receipts, "scope": SCOPE,
        "method": "automated reproducible selection routing under an explicit window-only policy",
        "human_fulltext_review_claimed": False, "global_substantive_ledger_write": False,
        "originality_rejection_claimed": False, "method_or_cost_review_claimed": False,
        "counts": {"frozen_pending": len(frozen_ids), "selected_window_only": len(records),
                   "protected_pending_original": len(protected), "excluded_primary": len(excluded)},
        "counts_by_selected_route": dict(sorted(Counter(r["route"] for r in records).items())),
        "excluded_primary_sources": primary_sources,
        "signal_review_sources": review_sources,
        "excluded_primary_ids": sorted(excluded),
        "protected_ids": sorted(protected_ids), "protected_records": protected,
        "limitations": [
            "No captured priority signal is not proof of no Google/Meta affiliation. The bounded official directories, known-author checks and captured metadata define this window's priority coverage; new evidence reopens a candidate.",
            "Generic future/resource-efficient deployment motivation is not itself production A/B. Textual production/deployment signals remain visible and can only be cleared by a paper-specific, fingerprinted semantic clarification; source flags and explicit protected identities cannot be cleared this way.",
            "New algorithms and public benchmarks may be present in the P2 selection subset. This decision does not reject their originality, verify their method, assess full-experiment cost, or claim implementation.",
            "Protected records remain nonterminal until original review; a nonempty protected set must not be bypassed to advance coverage.",
        ],
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path, nargs="?", default=ROOT / ".cache/nov09-closure")
    parser.add_argument("--input", type=Path, default=AUDIT / "p2-selection-input.json")
    parser.add_argument("--policy", type=Path, default=AUDIT / "p2-selection-policy.json")
    parser.add_argument("--output", type=Path, default=AUDIT / "p2-selection-screen.json")
    parser.add_argument("--exclude-primary-json", type=Path, action="append", default=[])
    parser.add_argument("--protection-review-json", type=Path, action="append", default=[])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    existing = read(args.output) if args.check and args.output.exists() else {}
    exclude = args.exclude_primary_json or [resolve_ref(s["path"])
                                           for s in existing.get("excluded_primary_sources", [])]
    reviews = args.protection_review_json or [resolve_ref(s["path"])
                                             for s in existing.get("signal_review_sources", [])]
    result = build(args.source_dir, read(args.input), read(args.policy),
                   exclude_primary_json=exclude, protection_review_json=reviews,
                   frozen_bytes=args.input.read_bytes(), policy_bytes=args.policy.read_bytes())
    encoded = stable_json(result)
    if args.check:
        if not args.output.exists() or args.output.read_bytes() != encoded:
            raise SystemExit("P2 selection screen is stale; regenerate it with its pinned sources")
    else:
        args.output.write_bytes(encoded)
    print(json.dumps(result["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
