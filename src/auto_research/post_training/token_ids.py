"""Normalize token IDs across Transformers tokenizer return types."""

from collections.abc import Mapping


def token_ids(encoded) -> list[int]:
    """Accept lists, tokenizers.Encoding and Transformers BatchEncoding."""
    if isinstance(encoded, Mapping):
        encoded = encoded["input_ids"]
    elif hasattr(encoded, "ids"):
        encoded = encoded.ids
    if hasattr(encoded, "tolist"):
        encoded = encoded.tolist()
    if not isinstance(encoded, (list, tuple)) or not encoded:
        raise ValueError("tokenizer returned no token IDs")
    if isinstance(encoded[0], (list, tuple)):
        if len(encoded) != 1:
            raise ValueError("expected a single prompt")
        encoded = encoded[0]
    if not encoded or any(not isinstance(value, int) or isinstance(value, bool) for value in encoded):
        raise ValueError("tokenizer returned non-integer token IDs")
    return list(encoded)
