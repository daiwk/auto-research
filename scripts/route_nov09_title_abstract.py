"""Route the frozen November pending pool without creating terminal decisions."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import urlsplit

from screen_nov09_scope import MODES, RUNS, TRACKS, read


RULES = (
    ("production_signals", r"\b(?:online A[/–-]B|production A[/–-]B|live traffic|online controlled experiment|"
     r"real traffic|full.traffic|production traffic|fully deployed|online deployment)\b"),
    ("industrial_application", r"\b(?:recommender systems?|generative recommendation|recommendation systems?|"
     r"industrial recommendation|click.through rate|conversion rate|ad auctions?|ad ranking|"
     r"commercial search|e.commerce search|feed ranking|sponsored search|computational advertising)\b"),
    ("post_training", r"\b(?:GRPO|PPO|RLVR|RLHF|OPSD|OPD|on.policy distillation|on.policy self.distillation|"
     r"policy gradients?|process reward|reward models?|preference optimization|post.training|"
     r"credit assignment|verifiable rewards?|DPO|parameter.efficient fine.tuning)\b"),
    ("agent_world_model", r"\b(?:JEPA|JEV|world models?|action.conditioned|vision.language.action|VLA|"
     r"world.action|latent dynamics|embodied agents?)\b"),
    ("agent_mechanism", r"\b(?:agentic|LLM agents?|multi.agent|agent[- ]harness\w*|tool[- ]use|tool[- ]calling|"
     r"agent memory|agent planning|agent skills?|self.evolution|recursive self.improvement|"
     r"coding agents?|agent scaffolding|computer.use|long.horizon agent)\b"),
    ("foundation_method", r"\b(?:KV cache|speculative decoding|pretraining|pre.training|"
     r"mixture.of.experts|scaling laws?|long.context|token compression|linear attention|"
     r"language model architecture|model merging|activation steering|state.space models?|"
     r"multimodal (?:models?|representation)|diffusion language models?|flow language models?)\b"),
    ("evaluation_or_analysis", r"\b(?:benchmark|benchmarking|evaluation|audit|test suite|"
     r"empirical study|systematic review|survey)\b"),
    ("model_mention", r"\b(?:LLMs?|VLMs?|large language models?|vision.language models?|foundation models?|"
     r"multimodal|transformers?|generative AI|neural networks?)\b"),
    ("specialist_topic", r"\b(?:clinical|electrocardiogram|ultrasound|x.ray|mammography|"
     r"microscopy|hyperspectral|crop yield|hydrology|seismic|fluid dynamics|satellite imagery|"
     r"voltage|vehicular|wireless|circuit|power grid|robot kinematics|control theory|"
     r"molecular dynamics|astronomy|gravitational|climate|traffic flow|medical|agricultur\w*)\b"),
)
COMPILED = [(key, re.compile(pattern, re.I)) for key, pattern in RULES]
ORG = re.compile(r"\b(?:Google Research|Google DeepMind|DeepMind|Google Labs|Google Cloud|Meta AI|"
                 r"Meta FAIR|Meta Platforms|Meta Superintelligence Labs|Meta Reality Labs)\b", re.I)
OFFICIAL_DOMAINS = {"research.google", "deepmind.google", "research.google.com", "ai.google",
                    "ai.meta.com", "research.facebook.com", "about.fb.com", "engineering.fb.com"}


def normalized(value: str) -> str:
    """Ignore punctuation/case only, not missing words or reworded abstracts."""
    return " ".join(re.findall(r"[^\W_]+", unicodedata.normalize("NFKC", value).casefold()))


def digest(text: str) -> str:
    return sha256(text.encode()).hexdigest()


def route(row: dict) -> tuple[str, dict[str, str]]:
    title, abstract = row["title"], row["abstract"]
    combined = f"{title}\n{abstract}"
    reasons = {
        key: match[0] for key, pattern in COMPILED if (match := pattern.search(combined)) is not None
    }
    official = sorted(
        {host for ref in row.get("source_provenance", []) if
         (host := urlsplit(ref.get("source_url", "")).hostname) in OFFICIAL_DOMAINS}
    )
    if (official or row.get("priority_source_matches") or row.get("priority_query_matches")
            or row.get("priority_review_required")):
        reasons["institutional_source_or_priority_query"] = ", ".join(
            sorted({*official, *row.get("priority_source_matches", []), *row.get("priority_query_matches", [])})
        ) or "priority review flag"
        return "official_priority", reasons
    if match := ORG.search(combined):
        reasons["institution_mention_not_affiliation"] = match[0]
        return "institution_name_verify", reasons
    for lane in ("production_signals", "industrial_application", "post_training", "agent_world_model",
                 "agent_mechanism", "foundation_method", "evaluation_or_analysis", "model_mention",
                 "specialist_topic"):
        if lane in reasons:
            return lane, reasons
    return "unclear_needs_reading", reasons


def load_observations(source_dir: Path) -> tuple[dict, dict]:
    observations: dict = {}
    receipts = {}
    for run in RUNS:
        for track in TRACKS:
            for prefix in MODES.values():
                path = source_dir / run / f"{track}-paper-candidates" / f"paper-{prefix}-{track}.json"
                key = path.relative_to(source_dir).as_posix()
                receipts[key] = sha256(path.read_bytes()).hexdigest()
                for row in read(path)["candidates"]:
                    identity = row["arxiv_id"]
                    rev = row["revision"]
                    existing = observations.get((identity, rev))
                    if existing is None:
                        observations[identity, rev] = row | {"captures": [key]}
                        continue
                    old_title, title = normalized(existing["title"]), normalized(row["title"])
                    same_abstract = normalized(existing["abstract"]) == normalized(row["abstract"])
                    if same_abstract and title.startswith(old_title + " "):
                        # An announcement header can be a prefix of the Atom title.
                        existing.update({k: row[k] for k in ("title", "abstract", "metadata_sha256")})
                        existing["captures"].insert(0, key)
                    elif not (same_abstract and (old_title == title or old_title.startswith(title + " "))):
                        existing.setdefault("metadata_conflicts", []).append(
                            {"capture": key, "metadata_sha256": row["metadata_sha256"], "title": row["title"]}
                        )
                    existing["captures"].append(key)
                    existing["priority_review_required"] |= row["priority_review_required"]
                    for field in ("source_provenance", "priority_source_matches", "priority_query_matches"):
                        existing[field] += [value for value in row[field] if value not in existing[field]]
    return observations, receipts


def build(source_dir: Path, input_bytes: bytes) -> dict:
    prior = json.loads(input_bytes)
    queue = {r[0]: r for rows in prior["pending_identities_by_local_first_publication"].values() for r in rows}
    observations, receipts = load_observations(source_dir)
    if receipts != {
        f"{r['run_id']}/{r['artifact_name']}/{r['file']}": r["artifact_sha256"]
        for r in prior["capture_receipts"]
    }:
        raise ValueError("candidate sources do not match frozen receipts")
    newest = {}
    for identity, revision in observations:
        newest[identity] = max(newest.get(identity, 0), revision)
    by_title = defaultdict(dict)
    by_abstract = defaultdict(list)
    normalized_titles = {}
    for identity, revision in newest.items():
        row = observations[identity, revision]
        title_key, abstract_key = normalized(row["title"]), normalized(row["abstract"])
        if title_key and abstract_key:
            abstract_hash = digest(abstract_key)
            by_title[title_key][identity] = abstract_hash
            normalized_titles[identity] = title_key
            if len(abstract_key.split()) >= 30:
                by_abstract[abstract_hash].append(identity)
    groups = []
    for title_key, match in sorted(by_title.items()):
        if len(match) < 2 or not set(match).intersection(queue):
            continue
        abstract_groups = defaultdict(list)
        for identity, abstract in match.items():
            abstract_groups[abstract].append(identity)
        groups.append({
            "title_key": title_key, "ids": sorted(match),
            "identical_abstract_groups": sorted(sorted(ids) for ids in abstract_groups.values() if len(ids) > 1),
            "decision": "check_publisher_identity_before_merging",
        })
    abstract_only_groups = [
        {"abstract_normalized_sha256": abstract_hash, "ids": sorted(ids),
         "decision": "check_publisher_identity_before_merging"}
        for abstract_hash, ids in sorted(by_abstract.items())
        if len({normalized_titles[i] for i in ids}) > 1 and set(ids).intersection(queue)
    ]
    group_lookup = {identity: group["ids"] for group in groups for identity in group["ids"]}
    records = []
    capture_observations = 0
    for identity, (_, revision, tracks, _) in sorted(queue.items()):
        row = observations[identity, revision]
        capture_observations += len(set(row["captures"]))
        lane, witnesses = route(row)
        if row.get("metadata_conflicts") and lane != "official_priority":
            lane = "metadata_conflict_verify"
        records.append({
            "id": identity, "revision": revision, "title": row["title"], "published": row["published"],
            "tracks": tracks, "metadata_sha256": row["metadata_sha256"],
            "abstract_normalized_sha256": digest(normalized(row["abstract"])),
            "capture": row["captures"][0], "route": lane, "witnesses": witnesses,
            **({"metadata_conflicts": row["metadata_conflicts"]} if row.get("metadata_conflicts") else {}),
            **({"title_match": group_lookup[identity]} if identity in group_lookup else {}),
        })
    return {
        "schema_version": 1, "method": "exact canonical arXiv revision, normalized-title/abstract and witness routing",
        "eligibility_or_cost_inferred": False, "terminal_decisions_created": 0,
        "input_inventory_sha256": sha256(input_bytes).hexdigest(), "source_receipts": receipts,
        "count": len(records), "capture_observations_at_routed_revision": capture_observations,
        "repeat_observations_collapsed": capture_observations - len(records),
        "counts_by_route": dict(sorted(Counter(r["route"] for r in records).items())),
        "duplicate_title_leads": groups, "duplicate_abstract_only_leads": abstract_only_groups, "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.source_dir, args.inventory.read_bytes())
    # Preserve one concise line per candidate for PR review and future diffs.
    records = result.pop("records")
    header = json.dumps(result, ensure_ascii=False, indent=2)
    lines = [header[:-2] + ',\n  "records": [']
    lines += ["    " + json.dumps(row, ensure_ascii=False) + ("," if i + 1 < len(records) else "")
              for i, row in enumerate(records)]
    lines += ["  ]", "}"]
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("count", "counts_by_route", "duplicate_title_leads",
                                             "duplicate_abstract_only_leads")},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
