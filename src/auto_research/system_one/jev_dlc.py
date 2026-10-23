"""Jev-DLC Eq.2–12 over external frozen scorer outputs (L1, not JEV-SFT).

Only feedback after a committed prediction can update the two bounded states.
No prompt, gold evaluator record, LM, or raw interaction history is retained.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


def softmax(values):
    values = np.asarray(values, dtype=np.float64)
    exp = np.exp(values - values.max())
    return exp / exp.sum()


def pa_i(state, direction, base_margin, margin=1.0, cap=1.0):
    """Minimum-change PA-I repair, including the zero-direction case."""
    norm2 = float(direction @ direction)
    violation = max(0.0, margin - base_margin - float(state @ direction))
    tau = min(cap, violation / norm2) if norm2 > 0 else 0.0
    return state + tau * direction


@dataclass(frozen=True)
class Decision:
    event_index: int
    version: int
    choice: str
    probabilities: tuple[float, ...]


class JevDLC:
    """One user's bounded state. Ontology and projection are frozen by caller.

    ``predict`` is deliberately target-free. ``feedback`` only accepts the
    current committed Decision and a typed accept/revoke, not an evaluator row.
    Reset invalidates outstanding decisions; model/projection migration must
    use reset with new revisions rather than silently reusing state.
    """

    def __init__(self, semantic_ids, projection, *, model_revision, projection_revision):
        self.ontology = tuple(semantic_ids)
        p = np.array(projection, dtype=np.float64, copy=True)
        if not self.ontology or len(set(self.ontology)) != len(self.ontology):
            raise ValueError("fixed nonempty unique semantic ontology required")
        if p.ndim != 2 or min(p.shape) == 0 or not np.isfinite(p).all():
            raise ValueError("finite nonempty projection required")
        if not model_revision or not projection_revision:
            raise ValueError("fixed model/projection revisions required")
        p.flags.writeable = False
        self.projection = p
        self.model_revision, self.projection_revision = model_revision, projection_revision
        self.version = -1
        self.reset()

    def reset(self, *, model_revision=None, projection_revision=None):
        if model_revision is not None:
            if not model_revision:
                raise ValueError("nonempty revision required")
            self.model_revision = model_revision
        if projection_revision is not None:
            if not projection_revision:
                raise ValueError("nonempty revision required")
            self.projection_revision = projection_revision
        self.counts = np.zeros(len(self.ontology), dtype=np.int64)
        self.states = np.zeros((2, self.projection.shape[0]))
        self.log_weights = np.array([2.0, 0.0])
        self.version += 1
        self.last_event_index = -1
        self._pending = None

    def predict(self, event_index, candidate_ids, semantic_ids, logits, hidden, safe,
                *, model_revision, projection_revision):
        if (model_revision, projection_revision) != (self.model_revision, self.projection_revision):
            raise ValueError("revision mismatch: explicit reset/migration required")
        if self._pending is not None or not isinstance(event_index, int) or event_index <= self.last_event_index:
            raise ValueError("chronological predict-then-feedback required")
        ids, semantics = tuple(candidate_ids), tuple(semantic_ids)
        b, h = np.array(logits, dtype=float, copy=True), np.array(hidden, dtype=float, copy=True)
        mask = np.asarray(safe)
        n = len(ids)
        if (not n or len(set(ids)) != n or len(semantics) != n or
                any(k not in self.ontology for k in semantics) or b.shape != (n,) or
                h.shape != (n, self.projection.shape[1]) or mask.shape != (n,) or
                mask.dtype != np.bool_ or not mask.any() or not np.isfinite(b).all() or not np.isfinite(h).all()):
            raise ValueError("finite target-free slate, known semantics and nonempty boolean safe mask required")
        active = np.flatnonzero(mask)
        with np.errstate(over='ignore', invalid='ignore'):
            r = h[active] @ self.projection.T
        if not np.isfinite(r).all():
            raise ValueError("nonfinite projected representation")
        scale = np.max(np.abs(r), axis=1)
        if (scale == 0).any():
            raise ValueError("zero projected representation has no unit direction")
        # Scaled normalization avoids squaring finite ~1e308 values to inf.
        r /= scale[:, None]
        norms = np.linalg.norm(r, axis=1)
        r /= norms[:, None]
        semantic_index = np.array([self.ontology.index(semantics[i]) for i in active])
        k = len(set(semantic_index.tolist()))
        prior = 2.0 * np.log((self.counts[semantic_index] + .5) / (self.counts.sum() + .5*k))
        features = np.stack([2.0*r, r])
        base = np.stack([b[active]+prior, b[active]])
        scores = base + np.einsum('cd,cnd->cn', self.states, features)
        channels = np.stack([softmax(s) for s in scores])
        weights = softmax(self.log_weights)
        # Geometric distribution mixture equals softmax of weighted logits.
        probability = softmax(weights @ scores)
        local_choice = int(probability.argmax())
        full = np.zeros(n)
        full[active] = probability
        decision = Decision(event_index, self.version, ids[active[local_choice]], tuple(full.tolist()))
        self._pending = (decision, ids, active, semantic_index, features, base, channels, probability)
        return decision

    def feedback(self, decision, *, accepted, replacement=None):
        if self._pending is None or decision is not self._pending[0] or decision.version != self.version:
            raise ValueError("stale, replayed or uncommitted decision")
        _, ids, active, semantic_index, features, base, channels, mixture = self._pending
        chosen = next(i for i, a in enumerate(active) if ids[a] == decision.choice)
        if type(accepted) is not bool or (accepted and replacement is not None):
            raise ValueError("typed accept or revoke required")
        if accepted:
            preferred = chosen
            competitors = [i for i in range(len(active)) if i != chosen]
            rejected = max(competitors, key=lambda i: mixture[i]) if competitors else None
        else:
            if replacement == decision.choice or replacement not in [ids[i] for i in active]:
                raise ValueError("revoke replacement must be a different safe candidate")
            preferred = next(i for i, a in enumerate(active) if ids[a] == replacement)
            rejected = chosen
        # Reliability uses PRE-update expert decisions, never repaired scores.
        losses = (channels.argmax(axis=1) != preferred).astype(float)
        new_states = self.states.copy()
        if rejected is not None:
            for j in range(2):
                new_states[j] = pa_i(self.states[j], features[j, preferred]-features[j, rejected],
                                     base[j, preferred]-base[j, rejected])
        weights = .9*softmax(self.log_weights-.25*losses)+.05
        self.states = new_states
        self.counts[semantic_index[preferred]] += 1
        self.log_weights = np.log(weights)
        self.last_event_index = decision.event_index
        self.version += 1
        self._pending = None


def diagnostic(seed=42):
    rng = np.random.default_rng(seed)
    projection = rng.normal(size=(4, 7))
    learner = JevDLC(['a', 'b', 'c'], projection, model_revision='fixture-v1', projection_revision='seeded-v1')
    kwargs = dict(candidate_ids=['a', 'b', 'c'], semantic_ids=['a', 'b', 'c'], logits=[.7, .2, 3.],
                  hidden=rng.normal(size=(3, 7)), safe=[True, True, False],
                  model_revision='fixture-v1', projection_revision='seeded-v1')
    first = learner.predict(0, **kwargs)
    before = np.array(first.probabilities)
    correction = 'b' if first.choice == 'a' else 'a'
    learner.feedback(first, accepted=False, replacement=correction)
    changed = float(np.linalg.norm(learner.states))
    stale_rejected = False
    try:
        learner.feedback(first, accepted=True)
    except ValueError:
        stale_rejected = True
    second = learner.predict(1, **kwargs)
    after = np.array(second.probabilities)
    learner.feedback(second, accepted=True)
    total = int(learner.counts.sum())
    learner.reset()
    reset = learner.predict(0, **kwargs)
    state = np.array([.3, -.1])
    direction = np.array([1., -2.])
    repaired = pa_i(state, direction, -.4)
    reference = state + min(1., max(0., 1.+.4-state@direction)/(direction@direction))*direction
    return {'seed': seed, 'metrics': {'pa_reference_error': float(np.max(np.abs(repaired-reference))),
        'correction_state_norm': changed, 'future_probability_delta': float(np.max(np.abs(after-before))),
        'feedback_count': total, 'masked_probability': float(after[2]), 'model_calls': 0},
        'checks': {'pa_reference_matches': bool(np.allclose(repaired, reference)),
            'future_only_update': bool(np.max(np.abs(after-before)) > 0 and first.probabilities == tuple(before)),
            'safe_mask_is_hard': bool(after[2] == 0), 'stale_feedback_rejected': stale_rejected,
            'reset_restores_frozen_prediction': reset.probabilities == first.probabilities,
            'no_raw_history': bool(learner._pending is not None and learner.counts.sum() == 0),
            'zero_direction_passive': bool(np.array_equal(pa_i(state, np.zeros(2), -3.), state))}}
