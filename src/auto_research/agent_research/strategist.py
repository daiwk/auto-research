"""Strategist blueprint/control kernels, not an LLM search or executor.

Paper: https://arxiv.org/html/2611.03618v1 (Secs. 2–3, Appendix A).
Sources are parsed, never imported or executed. Measurement records must come
from an external evaluator; the deterministic diagnostic is not agent evidence.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from hashlib import sha256
import math
from types import MappingProxyType
from typing import Mapping

REQUIRES_GPU_VALIDATION = False
TIER_WEIGHTS = MappingProxyType({"fast": 1.0, "balanced": 2.83, "complex": 6.67})


def _finite(value, *, minimum=None, maximum=None):
    if (type(value) not in (int, float) or not math.isfinite(value)
            or (minimum is not None and value < minimum)
            or (maximum is not None and value > maximum)):
        raise ValueError("finite numeric value in range required")
    return float(value)


def blueprint_hash(source: str, *, prompt_literals: tuple[str, ...] = ()) -> str:
    """AST fingerprint of execute, eliding explicitly reviewed prompt literals.

    Prompt classification is supplied by the caller, not inferred from length.
    Other strings (routing tiers, dictionary keys, patterns) and f-string
    expressions stay structural. This conservative subset does not rewrite
    prompt overrides or prove semantic equivalence.
    """
    if not isinstance(source, str) or not source.strip():
        raise ValueError("source text required")
    if (not isinstance(prompt_literals, tuple) or len(set(prompt_literals)) != len(prompt_literals)
            or any(not isinstance(x, str) or not x for x in prompt_literals)):
        raise ValueError("unique explicitly reviewed prompt strings required")
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        raise ValueError("blueprint must parse as Python") from error
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                 and node.name == "execute"]
    if len(functions) != 1:
        raise ValueError("one top-level execute(llm, task) function required")
    execute = functions[0]
    if (isinstance(execute, ast.AsyncFunctionDef) or execute.decorator_list or
            [x.arg for x in execute.args.posonlyargs + execute.args.args] != ["llm", "task"]
            or execute.args.vararg or execute.args.kwarg or execute.args.kwonlyargs
            or execute.args.defaults):
        raise ValueError("plain execute(llm, task) interface required")
    present = {node.value for node in ast.walk(execute)
               if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    if set(prompt_literals) - present:
        raise ValueError("declared prompt literal absent from execute")

    class Elide(ast.NodeTransformer):
        def visit_Constant(self, node):
            if isinstance(node.value, str) and node.value in prompt_literals:
                return ast.Constant(value="<reviewed-task-prompt>")
            return node

    # Function annotations/docstrings do not change execute-body structure.
    body = execute.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    body_tree = Elide().visit(ast.Module(body=body, type_ignores=[]))
    return sha256(ast.dump(body_tree, include_attributes=False).encode()).hexdigest()


@dataclass(frozen=True)
class Blueprint:
    name: str
    source: str
    parents: tuple[str, ...] = ()
    prompt_literals: tuple[str, ...] = ()

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.isidentifier() or self.name.startswith("_"):
            raise ValueError("public Python identifier required for blueprint")
        parents = tuple(self.parents)
        if (len(set(parents)) != len(parents) or self.name in parents
                or any(not isinstance(x, str) or not x.isidentifier() for x in parents)):
            raise ValueError("distinct prior parent identities required")
        object.__setattr__(self, "parents", parents)
        object.__setattr__(self, "prompt_literals", tuple(self.prompt_literals))
        blueprint_hash(self.source, prompt_literals=self.prompt_literals)

    @property
    def structural_hash(self):
        return blueprint_hash(self.source, prompt_literals=self.prompt_literals)


class BlueprintLibrary:
    """Append-only declared dependency DAG; no loading/execution or persistence."""

    def __init__(self):
        self._entries: dict[str, Blueprint] = {}
        self._hashes: set[str] = set()

    @property
    def entries(self):
        return MappingProxyType(dict(self._entries))

    def add(self, blueprint: Blueprint):
        if not isinstance(blueprint, Blueprint):
            raise ValueError("typed blueprint required")
        if blueprint.name in self._entries or blueprint.structural_hash in self._hashes:
            raise ValueError("duplicate blueprint identity or structure")
        if set(blueprint.parents) - self._entries.keys():
            raise ValueError("a blueprint may depend only on previously added nodes")
        self._entries[blueprint.name] = blueprint
        self._hashes.add(blueprint.structural_hash)


def hybrid_retrieval(relevance: Mapping[str, tuple[float, float]],
                     inspiration: Mapping[str, tuple[float, float]], *, k: int = 5):
    """Paper alpha=.4 score kernel, using externally measured TF-IDF/cosines.

    Does not compute embeddings or turn supplied scores into a search engine.
    Returns non-overlapping relevance and inspiration slates.
    """
    if type(k) is not int or k < 1 or set(relevance) != set(inspiration):
        raise ValueError("positive k and the same indexed library required")
    for query in (relevance, inspiration):
        for name, pair in query.items():
            if not isinstance(name, str) or not name or len(pair) != 2:
                raise ValueError("named TF-IDF/cosine pairs required")
            _finite(pair[0], minimum=0)
            _finite(pair[1], minimum=-1, maximum=1)

    def ranked(query):
        return sorted(query, key=lambda name: (-.4 * query[name][0] - .6 * query[name][1], name))

    relevant = tuple(ranked(relevance)[:k])
    adjacent = tuple(name for name in ranked(inspiration) if name not in relevant)[:k]
    return relevant, adjacent


def weighted_token_cost(calls: tuple[tuple[str, int, int], ...]) -> float:
    """Count input and output (including thinking) at paper parameter weights."""
    total = 0.0
    for tier, input_tokens, output_tokens in calls:
        if (tier not in TIER_WEIGHTS or any(type(n) is not int or n < 0 for n in (input_tokens, output_tokens))):
            raise ValueError("known tier and nonnegative integer token counts required")
        total += TIER_WEIGHTS[tier] * (input_tokens + output_tokens)
    return _finite(total, minimum=0)


@dataclass(frozen=True)
class SplitMeasurement:
    split: str
    item_ids: tuple[str, ...]
    scores: tuple[float, ...]
    costs: tuple[float, ...]

    def __post_init__(self):
        ids, scores, costs = tuple(self.item_ids), tuple(self.scores), tuple(self.costs)
        if (self.split not in {"validation", "hidden"} or not ids or
                len(set(ids)) != len(ids) or any(not isinstance(x, str) or not x for x in ids)
                or len(ids) != len(scores) or len(ids) != len(costs)):
            raise ValueError("complete distinct item records on validation or hidden required")
        scores = tuple(_finite(x, minimum=0, maximum=1) for x in scores)
        costs = tuple(_finite(x, minimum=0) for x in costs)
        if not math.isfinite(math.fsum(costs)) or math.fsum(costs) <= 0:
            raise ValueError("positive finite measured inference cost required")
        object.__setattr__(self, "item_ids", ids)
        object.__setattr__(self, "scores", scores)
        object.__setattr__(self, "costs", costs)


@dataclass(frozen=True)
class CandidateMeasurement:
    name: str
    validation: SplitMeasurement
    hidden: SplitMeasurement

    def __post_init__(self):
        if (not isinstance(self.name, str) or not self.name or
                not isinstance(self.validation, SplitMeasurement) or not isinstance(self.hidden, SplitMeasurement)
                or self.validation.split != "validation" or self.hidden.split != "hidden"
                or set(self.validation.item_ids) & set(self.hidden.item_ids)):
            raise ValueError("named candidate with disjoint validation and hidden splits required")


def paired_comparison(candidate: SplitMeasurement, reference: SplitMeasurement) -> dict[str, float | int]:
    """Questionwise difference and delta-method cost-ratio SE, not a significance claim.

    Unlike the upstream loader's intersection, this interface rejects incomplete
    coverage instead of silently dropping unmatched planned items.
    """
    if (candidate.split != reference.split or candidate.item_ids != reference.item_ids
            or len(candidate.item_ids) < 2):
        raise ValueError("at least two identical ordered paired items on the same split required")
    n = len(candidate.item_ids)
    differences = [c - r for c, r in zip(candidate.scores, reference.scores)]
    difference = math.fsum(differences) / n
    denominator = math.fsum(reference.costs)
    ratio = math.fsum(candidate.costs) / denominator
    residuals = [c - ratio * r for c, r in zip(candidate.costs, reference.costs)]
    result = {"n": n, "accuracy_delta": difference,
              "accuracy_se": math.sqrt(math.fsum((x - difference) ** 2 for x in differences) / (n - 1) / n),
              "cost_ratio": ratio,
              "cost_ratio_se": math.sqrt(math.fsum(x * x for x in residuals) * n / (n - 1)) / denominator,
              "fixed": sum(x > 0 for x in differences), "broke": sum(x < 0 for x in differences)}
    for value in result.values():
        _finite(value)
    return result


def two_percent_win(comparison: Mapping[str, float | int]) -> str | None:
    """The paper/default upstream rule: 2 percentage points vs 2% cost.

    No standard-error multiplier is used by the selected hidden_best rule;
    do not describe this deterministic tolerance rule as a confidence test.
    """
    delta = round(_finite(comparison["accuracy_delta"], minimum=-1, maximum=1), 9)
    ratio = round(_finite(comparison["cost_ratio"], minimum=0), 9)
    if delta > .02 and ratio <= 1.02:
        return "accuracy"
    if ratio < .98 and delta >= -.02:
        return "cost"
    return None


def select_paired(reference: CandidateMeasurement, candidates: tuple[CandidateMeasurement, ...], *, min_items: int = 20):
    """Win on both splits; maximize hidden accuracy delta, then minimize cost.

    Keeps the reference if none qualifies. The caller must isolate these
    evaluator records from any proposer; this API is not an information-flow
    sandbox and has no test-data argument.
    """
    if type(min_items) is not int or min_items < 2:
        raise ValueError("at least two paired items required")
    if any(len(split.item_ids) < min_items for split in (reference.validation, reference.hidden)):
        raise ValueError("reference coverage below minimum")
    names, rows = {reference.name}, []
    for candidate in candidates:
        if not isinstance(candidate, CandidateMeasurement) or candidate.name in names:
            raise ValueError("distinct typed candidate identities required")
        names.add(candidate.name)
        validation = paired_comparison(candidate.validation, reference.validation)
        hidden = paired_comparison(candidate.hidden, reference.hidden)
        rows.append({"name": candidate.name, "validation": validation, "hidden": hidden,
                     "qualifies": two_percent_win(validation) is not None and two_percent_win(hidden) is not None})
    passing = [row for row in rows if row["qualifies"]]
    passing.sort(key=lambda row: (-round(row["hidden"]["accuracy_delta"], 9), row["hidden"]["cost_ratio"], row["name"]))
    return {"pick": passing[0]["name"] if passing else reference.name,
            "pick_is_reference": not passing, "comparisons": rows}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """CPU arithmetic/contract checks with synthetic measured-arm records."""
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only component required")
    source = 'def execute(llm, task):\n    return llm("Explain the problem carefully", task)\n'
    library = BlueprintLibrary()
    library.add(Blueprint("first", source, prompt_literals=("Explain the problem carefully",)))
    duplicate_rejected = False
    try:
        library.add(Blueprint("copy", source.replace("Explain the problem carefully", "Solve the question step by step"),
                              prompt_literals=("Solve the question step by step",)))
    except ValueError:
        duplicate_rejected = True
    ids = tuple(f"v-{seed}-{i}" for i in range(20))
    hidden = tuple(f"h-{seed}-{i}" for i in range(20))
    def measured(name, score, cost):
        return CandidateMeasurement(name, SplitMeasurement("validation", ids, (score,) * 20, (cost,) * 20),
                                    SplitMeasurement("hidden", hidden, (score,) * 20, (cost,) * 20))
    reference = measured("reference", .7, 10.)
    pick = select_paired(reference, (measured("cheaper", .7, 8.), measured("worse", .6, 7.)))
    fallback = select_paired(reference, (measured("worse", .6, 7.),))
    return {"diagnostic_only": True, "device": "cpu", "seed": seed,
            "metrics": {"library_nodes": len(library.entries), "paired_items_per_split": 20,
                        "selected_cost_ratio": pick["comparisons"][0]["hidden"]["cost_ratio"]},
            "checks": {"prompt_only_duplicate_rejected": duplicate_rejected,
                       "two_split_cost_pick": pick["pick"] == "cheaper",
                       "no_qualifier_keeps_reference": fallback["pick_is_reference"],
                       "test_data_not_accepted": True}}
