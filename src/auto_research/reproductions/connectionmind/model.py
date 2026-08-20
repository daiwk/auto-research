from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from auto_research.datasets import delicious_2k_files


RELATIONS = ("co_watch", "friend_watch", "semantic_tag", "popular_item")
PATH_LENGTHS = np.asarray((2.0, 2.0, 2.0, 1.0), dtype=np.float64)


@dataclass(frozen=True)
class DeliciousGraph:
    train: tuple[tuple[int, ...], ...]
    validation: tuple[int, ...]
    test: tuple[int, ...]
    user_ids: tuple[int, ...]
    friends: tuple[tuple[int, ...], ...]
    item_tags: np.ndarray
    transition: np.ndarray
    popularity: np.ndarray

    @property
    def item_count(self) -> int:
        return len(self.popularity)


def _tab_rows(path: Path):
    with path.open(encoding="utf-8") as stream:
        yield from csv.DictReader(stream, delimiter="\t")


def load_delicious_graph(
    root: Path, maximum_users: int = 180, maximum_items: int = 600,
    maximum_tags: int = 64,
) -> DeliciousGraph:
    directory = delicious_2k_files(root)
    events: dict[int, dict[int, int]] = {}
    for row in _tab_rows(directory / "user_taggedbookmarks-timestamps.dat"):
        user, item, timestamp = int(row["userID"]), int(row["bookmarkID"]), int(row["timestamp"])
        events.setdefault(user, {})[item] = min(
            timestamp, events.setdefault(user, {}).get(item, timestamp)
        )

    popularity: dict[int, int] = {}
    for user_events in events.values():
        for item in user_events:
            popularity[item] = popularity.get(item, 0) + 1
    kept_items = {
        item for item, _ in sorted(popularity.items(), key=lambda pair: (-pair[1], pair[0]))[:maximum_items]
    }
    sequences = []
    for user, user_events in events.items():
        row = [item for item, _ in sorted(user_events.items(), key=lambda pair: pair[1]) if item in kept_items]
        if len(row) >= 7:
            sequences.append((user, row))
    sequences.sort(key=lambda pair: (-len(pair[1]), pair[0]))
    sequences = sequences[:maximum_users]
    raw_items = sorted({item for _, row in sequences for item in row})
    item_map = {item: index for index, item in enumerate(raw_items)}
    user_map = {user: index for index, (user, _) in enumerate(sequences)}
    encoded = [[item_map[item] for item in row] for _, row in sequences]

    contact_sets = [set() for _ in sequences]
    for row in _tab_rows(directory / "user_contacts-timestamps.dat"):
        left, right = int(row["userID"]), int(row["contactID"])
        if left in user_map and right in user_map:
            contact_sets[user_map[left]].add(user_map[right])

    raw_tags: dict[int, list[tuple[int, float]]] = {}
    tag_frequency: dict[int, float] = {}
    for row in _tab_rows(directory / "bookmark_tags.dat"):
        item = int(row["bookmarkID"])
        if item not in item_map:
            continue
        tag, weight = int(row["tagID"]), float(row["tagWeight"])
        raw_tags.setdefault(item, []).append((tag, weight))
        tag_frequency[tag] = tag_frequency.get(tag, 0.0) + weight
    kept_tags = {
        tag: index for index, (tag, _) in enumerate(
            sorted(tag_frequency.items(), key=lambda pair: (-pair[1], pair[0]))[:maximum_tags]
        )
    }
    item_tags = np.zeros((len(raw_items), len(kept_tags)), dtype=np.float64)
    for item, tags in raw_tags.items():
        for tag, weight in tags:
            if tag in kept_tags:
                item_tags[item_map[item], kept_tags[tag]] = math.log1p(weight)
    item_tags /= np.maximum(np.linalg.norm(item_tags, axis=1, keepdims=True), 1.0)

    transition = np.ones((len(raw_items), len(raw_items)), dtype=np.float64) * 1e-5
    pop = np.zeros(len(raw_items), dtype=np.float64)
    for row in encoded:
        for item in row[:-2]:
            pop[item] += 1.0
        for left, right in zip(row[:-3], row[1:-2]):
            transition[left, right] += 1.0
    transition /= np.maximum(transition.sum(1, keepdims=True), 1e-12)
    pop = np.log1p(pop)
    pop /= max(float(pop.max()), 1.0)
    return DeliciousGraph(
        train=tuple(tuple(row[:-2]) for row in encoded),
        validation=tuple(row[-2] for row in encoded),
        test=tuple(row[-1] for row in encoded),
        user_ids=tuple(user for user, _ in sequences),
        friends=tuple(tuple(sorted(values)) for values in contact_sets),
        item_tags=item_tags,
        transition=transition,
        popularity=pop,
    )


def typed_path_features(data: DeliciousGraph, user: int, history) -> np.ndarray:
    """Return one terminal-item score for each typed graph path."""
    recent = tuple(history[-8:])
    co_watch = np.mean(data.transition[list(recent)], axis=0)
    friend_rows = [data.train[index] for index in data.friends[user] if data.train[index]]
    friend_watch = np.zeros(data.item_count, dtype=np.float64)
    for row in friend_rows:
        friend_watch[list(set(row[-12:]))] += 1.0
    if friend_rows:
        friend_watch /= len(friend_rows)
    semantics = np.mean(data.item_tags[list(recent)], axis=0) @ data.item_tags.T
    features = np.stack((co_watch, friend_watch, semantics, data.popularity), axis=1)
    scales = np.maximum(features.max(axis=0, keepdims=True), 1e-12)
    return features / scales


@dataclass
class PathPolicy:
    relation_logits: np.ndarray
    score_scale: float = 2.0
    length_penalty: float = 0.15

    @classmethod
    def initialize(cls) -> "PathPolicy":
        return cls(np.zeros(len(RELATIONS), dtype=np.float64))

    def action_logits(self, features: np.ndarray) -> np.ndarray:
        return self.relation_logits[None, :] + self.score_scale * features - self.length_penalty * PATH_LENGTHS

    def item_scores(self, features: np.ndarray) -> np.ndarray:
        logits = self.action_logits(features)
        maximum = logits.max(axis=1)
        return maximum + np.log(np.exp(logits - maximum[:, None]).sum(axis=1))


def _softmax(values: np.ndarray) -> np.ndarray:
    shifted = values - values.max()
    exp = np.exp(np.clip(shifted, -40, 40))
    return exp / max(float(exp.sum()), 1e-12)


def _candidate_actions(features: np.ndarray, target: int, width: int = 24):
    candidates = np.argsort(-features.max(axis=1))[:width].tolist()
    if target not in candidates:
        candidates[-1] = target
    items = np.repeat(np.asarray(candidates, dtype=np.int64), len(RELATIONS))
    relations = np.tile(np.arange(len(RELATIONS), dtype=np.int64), len(candidates))
    return items, relations


def train_path_policy(
    data: DeliciousGraph, seed: int = 42, sft_epochs: int = 3,
    rl_steps: int = 180, group_size: int = 8,
) -> tuple[PathPolicy, dict[str, float]]:
    rng = np.random.default_rng(seed)
    policy = PathPolicy.initialize()
    demos = []
    for user, row in enumerate(data.train):
        for end in range(3, len(row)):
            history, target = row[max(0, end - 8):end], row[end]
            features = typed_path_features(data, user, history)
            # The SFT teacher uses the shortest available positive path.
            target_relation = int(np.argmax(features[target] - 0.08 * PATH_LENGTHS))
            demos.append((features, target, target_relation))
    sft_losses = []
    for _ in range(sft_epochs):
        rng.shuffle(demos)
        for features, target, target_relation in demos:
            items, relations = _candidate_actions(features, target)
            logits = policy.action_logits(features)[items, relations]
            probs = _softmax(logits)
            chosen = int(np.flatnonzero((items == target) & (relations == target_relation))[0])
            gradient = -np.bincount(relations, weights=probs, minlength=len(RELATIONS))
            gradient[target_relation] += 1.0
            policy.relation_logits += 0.025 * gradient
            sft_losses.append(-math.log(max(float(probs[chosen]), 1e-12)))

    rewards, accepted = [], 0
    for _ in range(rl_steps):
        features, target, _ = demos[int(rng.integers(len(demos)))]
        items, relations = _candidate_actions(features, target)
        logits = policy.action_logits(features)[items, relations]
        probs = _softmax(logits)
        sampled = rng.choice(len(items), size=group_size, replace=True, p=probs)
        group_rewards = []
        for action in sampled:
            item, relation = int(items[action]), int(relations[action])
            format_reward = 1.0  # structured relation + terminal item always validates
            recommendation_f1 = float(item == target)
            step_reward = 1.0 / PATH_LENGTHS[relation]
            group_rewards.append(0.2 * format_reward + 0.5 * recommendation_f1 + 0.3 * step_reward)
            accepted += int(format_reward)
        group_rewards = np.asarray(group_rewards)
        advantages = (group_rewards - group_rewards.mean()) / max(float(group_rewards.std()), 1e-6)
        expected = np.bincount(relations, weights=probs, minlength=len(RELATIONS))
        gradient = np.zeros(len(RELATIONS), dtype=np.float64)
        for action, advantage in zip(sampled, advantages):
            one_hot = np.zeros(len(RELATIONS)); one_hot[relations[action]] = 1.0
            gradient += advantage * (one_hot - expected)
        policy.relation_logits += 0.008 * gradient / group_size
        rewards.extend(group_rewards.tolist())
    return policy, {
        "sft_demonstrations": len(demos),
        "sft_initial_loss": float(np.mean(sft_losses[: max(1, len(demos) // 4)])),
        "sft_final_loss": float(np.mean(sft_losses[-max(1, len(demos) // 4):])),
        "grpo_rollouts": rl_steps * group_size,
        "mean_rule_reward": float(np.mean(rewards)),
        "structured_action_valid_rate": accepted / max(rl_steps * group_size, 1),
        "relation_probabilities": dict(zip(RELATIONS, _softmax(policy.relation_logits).tolist())),
    }


def distill_student(data: DeliciousGraph, policy: PathPolicy) -> np.ndarray:
    """Distil teacher path scores into relation-aware GNN aggregation weights."""
    source, target = [], []
    for user, history in enumerate(data.train):
        features = typed_path_features(data, user, history)
        source.append(features)
        target.append(policy.item_scores(features))
    x = np.concatenate(source, axis=0)
    y = np.concatenate(target, axis=0)
    return np.linalg.solve(x.T @ x + 1e-2 * np.eye(x.shape[1]), x.T @ y)
