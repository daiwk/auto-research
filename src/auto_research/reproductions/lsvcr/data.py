from __future__ import annotations

import gzip
import json
from dataclasses import dataclass
from pathlib import Path

from ...datasets import amazon_beauty_5core


@dataclass(frozen=True)
class JointRow:
    item_history: tuple[int, ...]
    comment_history: tuple[int, ...]
    target_item: int
    target_comment: int


@dataclass(frozen=True)
class JointData:
    train: tuple[JointRow, ...]
    test: tuple[JointRow, ...]
    item_texts: tuple[str, ...]
    comment_texts: tuple[str, ...]


def load_joint_reviews(root: Path, maximum_users: int = 80) -> JointData:
    amazon_beauty_5core(root)
    path = root / "amazon-beauty-5core" / "reviews_Beauty_5.json.gz"
    records = []
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            records.append((row["reviewerID"], row["asin"], int(row["unixReviewTime"]), row.get("summary", ""), row.get("reviewText", "")))
    users = sorted({row[0] for row in records})[:maximum_users]
    records = [row for row in records if row[0] in set(users)]
    items = sorted({row[1] for row in records})
    item_ids = {item: index for index, item in enumerate(items)}
    item_text = {item: item for item in items}
    comments = []
    by_user = {user: [] for user in users}
    for user, item, timestamp, summary, review in records:
        comment_id = len(comments)
        comments.append((summary + ". " + review).strip()[:500] or "review")
        item_text[item] = (summary or item).strip()
        by_user[user].append((timestamp, item_ids[item], comment_id))
    train, test = [], []
    for events in by_user.values():
        events.sort()
        rows = []
        for position in range(2, len(events)):
            history = events[max(0, position - 12) : position]
            rows.append(JointRow(tuple(x[1] for x in history), tuple(x[2] for x in history), events[position][1], events[position][2]))
        if len(rows) >= 2:
            train.extend(rows[:-1])
            test.append(rows[-1])
    return JointData(tuple(train), tuple(test), tuple(item_text[item] for item in items), tuple(comments))


def instruction(data: JointData, row: JointRow, task: str) -> str:
    items = "; ".join(data.item_texts[index] for index in row.item_history[-6:])
    comments = "; ".join(data.comment_texts[index][:80] for index in row.comment_history[-4:])
    return f"User item history: {items}. User comment history: {comments}. Predict the next {task}:"
