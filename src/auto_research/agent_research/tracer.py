"""CPU transition trie with a genuinely learned contextual/empirical blend.

The caller supplies frozen context and registry embeddings. This module does not
claim a language model, official benchmark artifact, or end-to-end tool agent.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math

import numpy as np

EPSILON = 1e-12
TEMPERATURE_FLOOR = 1e-3


def _vector(value):
    out = np.asarray(value, dtype=np.float64)
    if out.ndim != 1 or not len(out) or not np.isfinite(out).all():
        raise ValueError("finite nonempty context vector required")
    return out


def _cosine(a, b):
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denominator) if denominator else 0.


def _sigmoid(x):
    return float(np.exp(-np.logaddexp(0., -x)))


def _softmax(x):
    values = np.exp(x - np.max(x))
    return values / values.sum()


@dataclass(frozen=True)
class TrainingStep:
    trajectory_id: str
    prefix: tuple[str, ...]
    context: tuple[float, ...]
    query_words: int
    prior_turns: int
    next_tool: str

    def __post_init__(self):
        if (not isinstance(self.trajectory_id, str) or not self.trajectory_id
                or not isinstance(self.next_tool, str) or not self.next_tool or not isinstance(self.prefix, tuple)):
            raise ValueError("trajectory ID, next tool and immutable prefix required")
        if (not isinstance(self.query_words, int) or not isinstance(self.prior_turns, int)
                or self.query_words < 0 or self.prior_turns < 0):
            raise ValueError("nonnegative query and history counts required")
        _vector(self.context)


class TransitionIndex:
    def __init__(self, steps: list[TrainingStep], registry: dict[str, tuple[float, ...]]):
        if not steps or not registry:
            raise ValueError("nonempty training steps and public tool registry required")
        self.registry = {key: _vector(value).copy() for key, value in sorted(registry.items())}
        dimensions = {len(v) for v in self.registry.values()}
        if len(dimensions) != 1:
            raise ValueError("registry embedding dimensions differ")
        self.dimension = dimensions.pop()
        self.trajectory_ids = frozenset(s.trajectory_id for s in steps)
        self.edges = defaultdict(lambda: defaultdict(list))
        for step in steps:
            if step.next_tool not in self.registry or any(t not in self.registry for t in step.prefix):
                raise ValueError("unregistered historical tool")
            if len(step.context) != self.dimension:
                raise ValueError("context/registry embedding dimension mismatch")
            self.edges[step.prefix][step.next_tool].append(np.asarray(step.context, dtype=np.float64))

    def signals(self, prefix, context, query_words, prior_turns):
        context = _vector(context)
        if (len(context) != self.dimension or not isinstance(query_words, int) or not isinstance(prior_turns, int)
                or query_words < 0 or prior_turns < 0):
            raise ValueError("invalid inference context or counts")
        children = self.edges.get(tuple(prefix))
        if not children:
            return None
        tools = tuple(sorted(children))
        counts = np.array([len(children[t]) for t in tools], dtype=np.float64)
        empirical = counts / counts.sum()
        similarities = np.array([_cosine(context, np.mean(children[t], 0)) for t in tools])
        rectified = np.maximum(similarities, 0.)
        contextual = rectified / rectified.sum() if rectified.sum() else np.full(len(tools), 1 / len(tools))
        ordered = np.sort(empirical)[::-1]
        features = np.array([ordered[0] - (ordered[1] if len(ordered) > 1 else 0.),
                             math.log(max(1., counts[int(np.argmax(similarities))])),
                             float(similarities.max()), query_words, prior_turns])
        return tools, np.log(empirical + EPSILON), np.log(np.maximum(contextual, EPSILON)), features

    def global_search(self, context, k):
        context = _vector(context)
        if len(context) != self.dimension:
            raise ValueError("context/registry embedding dimension mismatch")
        return tuple(sorted(self.registry, key=lambda t: (-_cosine(context, self.registry[t]), t))[:k])

    def global_tools(self, count):
        """Optional Tracer+G: largest training-prefix entropy, name tie-break."""
        if not 0 <= count <= len(self.registry):
            raise ValueError("invalid global tool count")
        by_tool = defaultdict(list)
        for children in self.edges.values():
            for tool, contexts in children.items():
                by_tool[tool].append(len(contexts))
        entropies = {}
        for tool, counts in by_tool.items():
            p = np.asarray(counts) / sum(counts)
            entropies[tool] = float(-(p * np.log2(p)).sum())
        return tuple(sorted(entropies, key=lambda t: (-entropies[t], t))[:count])


@dataclass(frozen=True)
class CrossfitExample:
    features: np.ndarray
    empirical_log: np.ndarray
    contextual_log: np.ndarray
    target: int
    target_trajectory: str
    index_trajectories: frozenset[str]


def crossfit_examples(steps, registry, *, seed=42, folds=5):
    """Each supervised step sees an index excluding its entire trajectory."""
    groups = sorted({s.trajectory_id for s in steps})
    if not 2 <= folds <= len(groups):
        raise ValueError("need >=2 disjoint trajectory folds")
    np.random.default_rng(seed).shuffle(groups)
    membership = {group: i % folds for i, group in enumerate(groups)}
    examples, missing = [], 0
    for fold in range(folds):
        index = TransitionIndex([s for s in steps if membership[s.trajectory_id] != fold], registry)
        for step in steps:
            if membership[step.trajectory_id] != fold:
                continue
            assert step.trajectory_id not in index.trajectory_ids
            signals = index.signals(step.prefix, step.context, step.query_words, step.prior_turns)
            if signals is None or step.next_tool not in signals[0]:
                missing += 1
                continue
            tools, p, likelihood, features = signals
            examples.append(CrossfitExample(features, p, likelihood, tools.index(step.next_tool),
                                            step.trajectory_id, index.trajectory_ids))
    return examples, {"planned_steps": len(steps), "trainable_steps": len(examples),
                      "unseen_prefix_or_child_steps": missing, "trajectory_overlap": 0}


@dataclass(frozen=True)
class BlendHead:
    parameters: np.ndarray
    mean: np.ndarray
    scale: np.ndarray

    def values(self, features):
        z = np.append((np.asarray(features) - self.mean) / self.scale, 1.)
        w = _sigmoid(self.parameters[0] @ z)
        temperature = float(np.logaddexp(0., self.parameters[1] @ z) + TEMPERATURE_FLOOR)
        return w, temperature, z


def loss_and_gradient(parameters, standardized_features, examples, *, l2=1e-3):
    """Analytical NumPy gradient of Eq.4, independently finite-difference tested."""
    gradient = np.zeros_like(parameters)
    loss = 0.
    for z, example in zip(standardized_features, examples, strict=True):
        w = _sigmoid(parameters[0] @ z)
        t_raw = parameters[1] @ z
        temperature = float(np.logaddexp(0., t_raw) + TEMPERATURE_FLOOR)
        difference = example.empirical_log - example.contextual_log
        numerator = example.contextual_log + w * difference
        logits = numerator / temperature
        probabilities = _softmax(logits)
        loss += float(np.logaddexp.reduce(logits) - logits[example.target])
        derivative = probabilities.copy()
        derivative[example.target] -= 1
        gradient[0] += np.dot(derivative, difference) / temperature * w * (1 - w) * z
        gradient[1] += np.dot(derivative, -numerator) / temperature**2 * _sigmoid(t_raw) * z
    loss /= len(examples)
    gradient /= len(examples)
    loss += l2 * float(np.square(parameters[:, :-1]).sum())
    gradient[:, :-1] += 2 * l2 * parameters[:, :-1]
    return loss, gradient


def fit_blend(examples, *, seed=42, epochs=200, learning_rate=.05):
    if not examples or not 1 <= epochs <= 500 or not math.isfinite(learning_rate) or learning_rate <= 0:
        raise ValueError("nonempty crossfit examples and bounded optimization settings required")
    for example in examples:
        if example.target_trajectory in example.index_trajectories:
            raise ValueError("training trajectory leaked into trie or edge memory")
    x = np.stack([e.features for e in examples])
    mean, scale = x.mean(0), x.std(0)
    scale = np.where(scale < 1e-12, 1., scale)
    z = np.column_stack(((x - mean) / scale, np.ones(len(x))))
    parameters = np.random.default_rng(seed).normal(0, .01, (2, 6))
    initial, _ = loss_and_gradient(parameters, z, examples)
    original = parameters.copy()
    m, v = np.zeros_like(parameters), np.zeros_like(parameters)
    for epoch in range(1, epochs + 1):
        _, gradient = loss_and_gradient(parameters, z, examples)
        m, v = .9 * m + .1 * gradient, .999 * v + .001 * gradient**2
        parameters -= learning_rate * (m / (1 - .9**epoch)) / (np.sqrt(v / (1 - .999**epoch)) + 1e-8)
    final, _ = loss_and_gradient(parameters, z, examples)
    return BlendHead(parameters, mean, scale), {"initial_crossfit_nll": initial, "final_crossfit_nll": final,
            "parameter_delta_l2": float(np.linalg.norm(parameters - original)), "epochs": epochs,
            "features": ["prior_margin", "log_top_edge_support", "R_top1", "query_words", "prior_turns"]}


@dataclass(frozen=True)
class TracerRetriever:
    index: TransitionIndex
    head: BlendHead
    confidence_gate: float = .20
    global_extension: tuple[str, ...] = ()

    def retrieve(self, prefix, context, *, query_words, prior_turns, k=5):
        if not 1 <= k <= len(self.index.registry) or not 0 <= self.confidence_gate <= 1:
            raise ValueError("valid registry budget and confidence gate required")
        if any(t not in self.index.registry for t in self.global_extension):
            raise ValueError("global extension contains an unknown tool")
        signals = self.index.signals(prefix, context, query_words, prior_turns)
        fallback, confidence, w, temperature = signals is None, None, None, None
        if signals is not None:
            tools, empirical, contextual, features = signals
            w, temperature, _ = self.head.values(features)
            logits = ((1 - w) * contextual + w * empirical) / temperature
            confidence = float(_softmax(logits).max())
            fallback = confidence < self.confidence_gate
            selected = tuple(tools[i] for i in sorted(range(len(tools)), key=lambda i: (-logits[i], tools[i]))[:k])
        if fallback:
            selected = self.index.global_search(context, k)
        selected = tuple(dict.fromkeys((*selected, *self.global_extension)))
        return {"tools": selected, "used_global_fallback": fallback, "confidence": confidence,
                "empirical_weight": w, "temperature": temperature,
                "base_budget": k, "returned_count": len(selected)}


def fit_tracer(steps, registry, *, seed=42, epochs=200, folds=5):
    examples, coverage = crossfit_examples(steps, registry, seed=seed, folds=folds)
    head, training = fit_blend(examples, seed=seed, epochs=epochs)
    return TracerRetriever(TransitionIndex(steps, registry), head), {**coverage, **training}
