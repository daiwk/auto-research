"""Extracted unchanged from auto_research.agent_research.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def apply_context_file(context: str, edits, *, maximum_characters: int):
    """CLM context-as-a-file: unrestricted replace/append with an explicit budget."""
    if maximum_characters < 1:
        raise ValueError("maximum_characters must be positive")
    value = context
    for edit in edits:
        operation = edit["operation"]
        if operation == "replace":
            old = edit["old"]
            if old not in value:
                raise ValueError("replace target is absent from context")
            value = value.replace(old, edit["new"], 1)
        elif operation == "append":
            value += edit["text"]
        else:
            raise ValueError(f"unknown context edit: {operation}")
    if len(value) > maximum_characters:
        value = value[-maximum_characters:]
    return value
