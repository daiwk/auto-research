"""CPU-only transparent conversation compaction, independently implemented.

Preserve prose, mark removed material, and recover exact archived payloads.
This is not the Pi extension or a model-based context_lookup implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

PAPER_REVISION = "2610.20116v1"
UPSTREAM_PAPER_COMMIT = "6b970d3"
MAX_INPUT_BYTES = 16 * 1024 * 1024
RESULT_METADATA_FIELDS = (
    "tool_call_id", "toolCallId", "toolName", "isError",
    "exitCode", "cancelled", "truncated", "excludeFromContext",
)


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def load_session(path: Path, *, leaf_id: str | None = None) -> list[dict]:
    """Read messages JSON or the selected ancestry of a Pi JSONL session.

    Never combines sibling branches. Unknown metadata events participate in
    ancestry but are not rendered as model messages. No source code is executed.
    """
    if path.is_symlink() or path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("session must be a regular file of at most 16 MiB")
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        messages = json.loads(raw)
    else:
        records = [json.loads(line) for line in raw.splitlines() if line.strip()]
        by_id = {row["id"]: row for row in records if isinstance(row.get("id"), str)}
        if len(by_id) != sum(isinstance(row.get("id"), str) for row in records):
            raise ValueError("duplicate session event IDs")
        if by_id:
            current = leaf_id if leaf_id is not None else next(reversed(by_id))
            branch, visited = [], set()
            while current is not None:
                if current in visited or current not in by_id:
                    raise ValueError("cyclic or missing session parent")
                visited.add(current)
                row = by_id[current]
                branch.append(row)
                current = row.get("parentId")
            records = list(reversed(branch))
        elif leaf_id is not None:
            raise ValueError("leaf selection requires session event IDs")
        messages = []
        for index, row in enumerate(records):
            message = row.get("message") if row.get("type") == "message" else row
            if isinstance(message, dict) and "role" in message:
                messages.append({**message, "id": row.get("id", f"message-{index}")})
    if not isinstance(messages, list) or not messages:
        raise ValueError("session contains no messages")
    normalized = []
    for index, message in enumerate(messages):
        if not isinstance(message, dict) or message.get("role") not in {
            "system", "user", "assistant", "tool", "toolResult", "bashExecution",
        }:
            raise ValueError("unsupported message role")
        if not isinstance(message.get("content", ""), (str, list)):
            raise ValueError("message content must be text or blocks")
        normalized.append({**message, "id": str(message.get("id", f"message-{index}"))})
    if len({message["id"] for message in normalized}) != len(normalized):
        raise ValueError("duplicate message IDs")
    return normalized


@dataclass(frozen=True)
class Checkpoint:
    messages: tuple[dict, ...]
    recovery: dict[str, dict]
    source_sha256: str
    prose_retained: int
    prose_dropped: int
    input_characters: int
    output_characters: int

    def recover(self, key: str) -> Any:
        """Exact archived retrieval, not an LLM answer or a success verdict."""
        row = self.recovery[key]
        if digest(row["payload"]) != row["sha256"]:
            raise ValueError("recovery payload hash mismatch")
        return row["payload"]

    def to_dict(self) -> dict:
        return {"schema_version": 1, "kind": "transparent_compaction_component",
                "messages": list(self.messages), "recovery": self.recovery,
                "source_sha256": self.source_sha256,
                "metrics": {"prose_blocks_retained": self.prose_retained,
                            "prose_blocks_explicitly_dropped": self.prose_dropped,
                            "input_characters": self.input_characters,
                            "output_characters": self.output_characters,
                            "recovery_items": len(self.recovery)},
                "model_calls": 0, "capability_score": None,
                "promotion_eligible": False}


def compact(messages: list[dict], *, max_prose_characters: int | None = None,
            recovery_archive: dict[str, dict] | None = None) -> Checkpoint:
    """Preserve user/assistant/system prose; archive thinking and tool output.

    A finite prose cap is opt-in and visibly drops oldest complete blocks, never
    silently truncates or paraphrases. It is NOT a tokenizer/context-fit promise.
    """
    if max_prose_characters is not None and (
        type(max_prose_characters) is not int or max_prose_characters < 0
    ):
        raise ValueError("prose cap must be a nonnegative integer or None")
    recovery: dict[str, dict] = json.loads(json.dumps(recovery_archive or {}, ensure_ascii=False))
    rendered, prose_locations = [], []
    ids = [str(row.get("id", f"message-{index}")) for index, row in enumerate(messages)]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate message IDs")

    def archive(message_id: str, label: str, payload: Any) -> dict:
        key = f"{message_id}:{label}"
        if key in recovery:
            raise ValueError("duplicate recovery identity")
        recovery[key] = {"payload": payload, "sha256": digest(payload)}
        return {"type": "omission", "reason": label, "recovery_key": key,
                "sha256": recovery[key]["sha256"]}

    for index, message in enumerate(messages):
        role = message["role"]
        message_id = str(message.get("id", f"message-{index}"))
        if role not in {"system", "user", "assistant", "tool", "toolResult", "bashExecution"}:
            raise ValueError("unsupported message role")
        content = message.get("content", message.get("output", ""))
        blocks = [{"type": "text", "text": content}] if isinstance(content, str) else content
        if not isinstance(blocks, list):
            raise ValueError("invalid content")
        output = {"id": message_id, "role": role, "content": []}
        for offset, block in enumerate(blocks):
            if not isinstance(block, dict):
                raise ValueError("content block must be an object")
            kind = block.get("type")
            if kind == "omission":
                key = block.get("recovery_key")
                if key not in recovery or block.get("sha256") != recovery[key]["sha256"] or (
                    digest(recovery[key]["payload"]) != block["sha256"]
                ):
                    raise ValueError("omission has no matching verified recovery archive")
                output["content"].append(dict(block))
            elif role in {"tool", "toolResult", "bashExecution"}:
                output["content"].append(archive(message_id, f"tool-output-{offset}", block))
            elif kind == "text" and isinstance(block.get("text"), str):
                output["content"].append(dict(block))
                prose_locations.append((output["content"], len(output["content"]) - 1, message_id))
            elif kind in {"toolCall", "tool_call"}:
                output["content"].append(dict(block))
            else:
                output["content"].append(archive(message_id, f"{kind or 'unknown'}-{offset}", block))
        if message.get("tool_calls"):
            output["tool_calls"] = message["tool_calls"]
        # Pi and OpenAI-style sessions use different pairing field names.
        # Preserve explicit False values and execution status even when the
        # potentially large output body is replaced by a recovery marker.
        for field in RESULT_METADATA_FIELDS:
            if field in message:
                output[field] = message[field]
        if role == "bashExecution":
            output["command"] = message.get("command", "")
        rendered.append(output)
    total = sum(len(blocks[offset]["text"]) for blocks, offset, _ in prose_locations)
    dropped = 0
    if max_prose_characters is not None:
        for blocks, offset, message_id in prose_locations:
            if total <= max_prose_characters:
                break
            block = blocks[offset]
            total -= len(block["text"])
            blocks[offset] = archive(message_id, f"cap-prose-{offset}", block)
            dropped += 1
    return Checkpoint(tuple(rendered), recovery, digest(messages),
                      len(prose_locations) - dropped, dropped,
                      len(json.dumps(messages, ensure_ascii=False)),
                      len(json.dumps(rendered, ensure_ascii=False)))


def recompact(checkpoint: Checkpoint, new_messages: list[dict],
              *, max_prose_characters: int | None = None) -> Checkpoint:
    """Retain existing recovery identities through subsequent compactions."""
    return compact([*checkpoint.messages, *new_messages],
                   max_prose_characters=max_prose_characters,
                   recovery_archive=checkpoint.recovery)
