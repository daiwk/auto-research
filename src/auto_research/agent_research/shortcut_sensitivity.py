"""CPU-only shortcut audits, not a safety guard or an evaluated agent.

Independent implementation of grouped label lookup and evaluation-unit metrics.
Gold labels train the explicitly capability-poor lookup diagnostic only. No tool
record is executed; benchmark text is never redistributed by this module.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import random
import re
import urllib.request

UPSTREAM_REVISION = "07b4fbe9de731f76c19bda781888db5f4c6123e7"
DATA_REVISION = "46358fa424a927a895c6c8322f99032c4eb5155e"
# SHA/size are public LFS object identities, not copied benchmark records.
ASSETS = (
    ("agentdojo/banking.json", "TS-Bench/agentdojo-traj/banking.json", 239239,
     "eb4a314845c8236ba1bbcd9855973f59279a70368b6eb31d447a4cd243086029"),
    ("agentdojo/slack.json", "TS-Bench/agentdojo-traj/slack.json", 361979,
     "08152de8cf9c39d01d58eb708f3a820a892f493841b975e09654ab904cf8a0d5"),
    ("agentdojo/travel.json", "TS-Bench/agentdojo-traj/travel.json", 1071254,
     "1935121585fb1a02662e8121fe80e78c6d89b77e0c6035ea2b75b593e3728a22"),
    ("agentdojo/workspace.json", "TS-Bench/agentdojo-traj/workspace.json", 8959525,
     "74b20a4fcd7df1c3e39a231e64860aeac8cd57ce3531728b329080abbcc862d0"),
    ("agentharm/benign_steps.json", "TS-Bench/agentharm-traj/benign_steps.json", 689251,
     "f44fce25b0ed795e3c11fadafb8d8c959d2ae4513e6e9f15e154fa4aba9bf020"),
    ("agentharm/harmful_steps.json", "TS-Bench/agentharm-traj/harmful_steps.json", 1764105,
     "6046b4f4b2e5086c98780433bddf74be542eeec910e3260b4727bf22a9a3365b"),
    ("reference/agentharm-labels.json", "guardian_test_logs/agentharm/TS-Guard/labels.json", 6581,
     "51b127b836995f3780ed42885079a8ecce725709f46f89c860cd6c7a21d67cf5"),
    ("reference/agentharm-preds.json", "guardian_test_logs/agentharm/TS-Guard/preds.json", 6581,
     "fb21f86e34bc64f3c340c731980e07b05ebec48ea55058f34ea75ae826b00a32"),
)


@dataclass(frozen=True)
class AuditRow:
    row_id: str
    domain: str
    interaction: str
    tool: str
    label: int

    def __post_init__(self):
        if not all(isinstance(x, str) and x for x in (self.row_id, self.domain, self.interaction, self.tool)):
            raise ValueError("nonempty row/domain/interaction/tool identifiers required")
        if self.label not in (0, 1):
            raise ValueError("strict binary audit labels required")


def binary_metrics(labels, predictions, weights=None) -> dict:
    """Zero-divisions are reported explicitly; no failed row is omitted."""
    labels, predictions = tuple(labels), tuple(predictions)
    if not labels or len(labels) != len(predictions) or any(x not in (0, 1) for x in labels + predictions):
        raise ValueError("matched nonempty binary arrays required")
    weights = tuple(1. for _ in labels) if weights is None else tuple(weights)
    if len(weights) != len(labels) or any(not math.isfinite(w) or w <= 0 for w in weights):
        raise ValueError("finite positive matched weights required")
    counts = {(y, p): 0. for y in (0, 1) for p in (0, 1)}
    for y, p, w in zip(labels, predictions, weights, strict=True):
        counts[y, p] += w
    tn, fp, fn, tp = (counts[k] for k in ((0, 0), (0, 1), (1, 0), (1, 1)))
    f1_denom = 2 * tp + fp + fn
    recalls = [tp / (tp + fn) if tp + fn else None, tn / (tn + fp) if tn + fp else None]
    return {"rows": len(labels), "weight_sum": sum(weights), "tp": tp, "tn": tn, "fp": fp, "fn": fn,
            "accuracy": (tp + tn) / sum(weights), "f1": 2 * tp / f1_denom if f1_denom else 0.,
            "balanced_accuracy": sum(recalls) / 2 if None not in recalls else None,
            "undefined_recall_classes": sum(r is None for r in recalls)}


def evaluation_units(rows: list[AuditRow], predictions) -> dict:
    predictions = tuple(predictions)
    sizes = Counter((r.domain, r.interaction) for r in rows)
    weights = [1 / sizes[r.domain, r.interaction] for r in rows]
    labels = [r.label for r in rows]
    return {"row": binary_metrics(labels, predictions),
            "equal_interaction": binary_metrics(labels, predictions, weights),
            "interactions": len(sizes)}


def _validate_rows(rows):
    if not rows or len({r.row_id for r in rows}) != len(rows):
        raise ValueError("nonempty audit records and unique row identifiers required")


def lookup_predictions(train: list[AuditRow], tools: list[str]) -> tuple[list[int], set[str]]:
    """Train-label majority diagnostic; inference accepts only tool names."""
    if not train:
        raise ValueError("lookup requires nonempty training fold")
    counts = defaultdict(lambda: [0, 0])
    for row in train:
        counts[row.tool.casefold()][row.label] += 1
    majority = {name: int(c[1] >= c[0]) for name, c in counts.items()}
    fallback = int(sum(r.label for r in train) * 2 >= len(train))
    return [majority.get(name.casefold(), fallback) for name in tools], set(majority)


def leave_one_domain_out(rows: list[AuditRow]) -> dict:
    _validate_rows(rows)
    domains = sorted({r.domain for r in rows})
    if len(domains) < 2:
        raise ValueError("domain holdout requires at least two domains")
    out, seen, folds = {}, {}, []
    for domain in domains:
        train, test = [r for r in rows if r.domain != domain], [r for r in rows if r.domain == domain]
        predictions, known = lookup_predictions(train, [r.tool for r in test])
        for row, pred in zip(test, predictions, strict=True):
            out[row.row_id], seen[row.row_id] = pred, row.tool.casefold() in known
        folds.append({"held_out_domain": domain, "train_rows": len(train), "test_rows": len(test),
                      "shared_interactions": 0, "test_labels_used_for_fitting": False})
    predictions = [out[r.row_id] for r in rows]
    result = {"metrics": evaluation_units(rows, predictions), "folds": folds,
              "seen_tool_fraction": sum(seen.values()) / len(rows), "predictions": predictions,
              "claim": "label predictability diagnostic, not an operational safety classifier"}
    for status in (True, False):
        selected = [(r, p) for r, p in zip(rows, predictions, strict=True) if seen[r.row_id] == status]
        result["seen" if status else "unseen"] = (
            binary_metrics([r.label for r, _ in selected], [p for _, p in selected]) if selected else None)
    return result


def grouped_lookup_cv(rows: list[AuditRow], *, folds=5, seed=42) -> dict:
    """Mixed-domain grouped CV is a stress comparison, never a deployment score."""
    _validate_rows(rows)
    groups = sorted({(r.domain, r.interaction) for r in rows})
    if not 2 <= folds <= len(groups):
        raise ValueError("2 <= folds <= interaction groups required")
    random.Random(seed).shuffle(groups)
    assignment = {g: i % folds for i, g in enumerate(groups)}
    out = {}
    for fold in range(folds):
        train = [r for r in rows if assignment[r.domain, r.interaction] != fold]
        test = [r for r in rows if assignment[r.domain, r.interaction] == fold]
        predictions, _ = lookup_predictions(train, [r.tool for r in test])
        out.update({r.row_id: p for r, p in zip(test, predictions, strict=True)})
    predictions = [out[r.row_id] for r in rows]
    return {"metrics": evaluation_units(rows, predictions), "folds": folds,
            "group": "domain+interaction", "predictions": predictions, "seed": seed}


def paired_sensitivity(original, edited, placebo, interactions) -> dict:
    """Repeated condition means; unsigned flips are not a causal effect."""
    if not original or not (len(original) == len(edited) == len(placebo) == len(interactions)):
        raise ValueError("matched nonempty base records required")
    changes, placebos = [], []
    for a, b, c in zip(original, edited, placebo, strict=True):
        if not a or not (len(a) == len(b) == len(c)) or any(x not in (0, 1) for x in (*a, *b, *c)):
            raise ValueError("matched binary repeated decisions required")
        changes.append((sum(b) - sum(a)) / len(a))
        placebos.append((sum(c) - sum(a)) / len(a))
    return {"base_count": len(changes), "interaction_clusters": len(set(interactions)),
            "signed_block_probability_change": sum(changes) / len(changes),
            "placebo_change": sum(placebos) / len(placebos),
            "placebo_adjusted_change": sum(a - b for a, b in zip(changes, placebos, strict=True)) / len(changes),
            "construct_preservation_independently_verified": False}


def _read_asset(cache: Path, asset) -> bytes:
    name, _, size, expected = asset
    path = cache / name
    if path.is_symlink() or any(p.is_symlink() for p in path.parents):
        raise ValueError("symlink cache paths are forbidden")
    if path.stat().st_size != size:
        raise ValueError(f"asset size mismatch: {name}")
    with path.open("rb") as handle:
        raw = handle.read(size + 1)
    if len(raw) != size or hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f"asset SHA-256 mismatch: {name}")
    return raw


def fetch_public_assets(cache: Path) -> None:
    """Explicit opt-in download of fixed inert public records, <= 13.2 MB total."""
    for asset in ASSETS:
        name, source, size, digest = asset
        path = cache / name
        if path.exists():
            _read_asset(cache, asset)
            continue
        if any(p.is_symlink() for p in path.parents):
            raise ValueError("symlink cache paths are forbidden")
        url = f"https://media.githubusercontent.com/media/MurrayTom/ToolSafe/{DATA_REVISION}/{source}"
        with urllib.request.urlopen(url, timeout=45) as response:
            raw = response.read(size + 1)
        if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError(f"download verification failed: {name}")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(raw)


def parse_tool(action: str) -> str:
    """Parse only an inert ReAct Action line; never eval arguments or call a tool."""
    action_lines, input_position = [], None
    prefix = r"^\s*(?:(?:\(\d+\)|\d+[.)])\s*)?\*{0,2}"
    for match in re.finditer(prefix + r"Action(?:\*{0,2})[ \t]*:[ \t]*([^\n\r]*)", action, re.IGNORECASE | re.MULTILINE):
        action_lines.append((match.start(), match.group(1).strip()))
    found = re.search(prefix + r"Action[ _]+Input(?:\*{0,2})\s*:", action, re.IGNORECASE | re.MULTILINE)
    if found:
        input_position = found.start()
    prior = [item for item in action_lines if input_position is None or item[0] < input_position]
    selected = prior[-1] if prior else action_lines[0] if action_lines else None
    if selected is None or not selected[1]:
        raise ValueError("missing tool Action line; do not silently omit this row")
    return selected[1].casefold()


def load_public_audit(cache: Path) -> tuple[list[AuditRow], list[AuditRow], list[int], list[dict]]:
    """Validate every byte before loading and return no raw benchmark text."""
    dojo, harm, source, exact_scores = [], [], [], {}
    for asset in ASSETS[:6]:
        name, path, size, digest = asset
        rows = json.loads(_read_asset(cache, asset))
        if not isinstance(rows, list):
            raise ValueError("public evaluation file must contain a JSON row list")
        for i, row in enumerate(rows):
            label = float(row["score"])
            if label not in (0., .5, 1.) or "id-interaction" not in row:
                raise ValueError("missing interaction or unsupported released label")
            domain = Path(name).stem
            record = AuditRow(f"{name}:{i}", domain, str(row["id-interaction"]),
                              parse_tool(row["current_action"]), int(label != 0))
            exact_scores[record.row_id] = label
            (dojo if name.startswith("agentdojo/") else harm).append(record)
        source.append({"source_path": path, "revision": DATA_REVISION, "sha256": digest, "bytes": size})
    # The frozen reference order is harmful_steps then benign_steps, not file
    # name sorting. Verified from the authors' REFERENCE_ORDER contract. Require
    # exact ordinal labels (0/.5/1), not just prevalence or binary agreement.
    harm = [row for domain in ("harmful_steps", "benign_steps") for row in harm if row.domain == domain]
    labels, predictions = (json.loads(_read_asset(cache, asset)) for asset in ASSETS[6:])
    if isinstance(labels, dict):
        raise ValueError("unexpected reference representation; require explicit stable alignment")
    if len(labels) != len(harm) or [float(x) for x in labels] != [exact_scores[r.row_id] for r in harm]:
        raise ValueError("released guard reference is not aligned with every AgentHarm row")
    if any(x not in (0., .5, 1.) for x in predictions):
        raise ValueError("unsupported or nonfinite frozen guard rating")
    predictions = [int(float(x) != 0) for x in predictions]
    if len(predictions) != len(harm):
        raise ValueError("guard predictions missing rows")
    source.extend({"source_path": a[1], "revision": DATA_REVISION, "sha256": a[3], "bytes": a[2]} for a in ASSETS[6:])
    return dojo, harm, predictions, source
