from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


PLACEHOLDER = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")
FEATURE_TYPES = {"text", "embedding", "combo", "sequence"}
COMPONENT_TYPES = {"preprocessor", "projector", "merger"}


@dataclass(frozen=True)
class PromptConfig:
    template: str
    features: tuple[dict[str, Any], ...]

    @classmethod
    def load(cls, template_path: Path, feature_path: Path) -> "PromptConfig":
        template_payload = json.loads(template_path.read_text(encoding="utf-8"))
        feature_payload = json.loads(feature_path.read_text(encoding="utf-8"))
        config = cls(template_payload["template"], tuple(feature_payload["features"]))
        config.validate()
        return config

    def validate(self) -> None:
        placeholders = PLACEHOLDER.findall(self.template)
        names = [feature["feature_name"] for feature in self.features]
        if len(names) != len(set(names)):
            raise ValueError("feature_name values must be unique")
        if set(placeholders) != set(names):
            raise ValueError(
                f"template/features mismatch: placeholders={placeholders}, features={names}"
            )
        for feature in self.features:
            _validate_feature(feature)

    @property
    def fingerprint(self) -> str:
        return json.dumps(
            {"template": self.template, "features": self.features}, sort_keys=True
        )


class PromptCompiler:
    """Compile both training and serving prompts from the same two JSON files."""

    def __init__(self, config: PromptConfig):
        self.config = config
        self.by_name = {feature["feature_name"]: feature for feature in config.features}

    def compile(
        self,
        row: dict[str, Any],
        encode_text: Callable[[str], Any],
        encode_embedding: Callable[[Any], Any],
        merge: Callable[[list[Any], dict[str, Any]], Any],
    ) -> list[Any]:
        output: list[Any] = []
        cursor = 0
        for match in PLACEHOLDER.finditer(self.config.template):
            if match.start() > cursor:
                output.append(encode_text(self.config.template[cursor : match.start()]))
            output.extend(
                _compile_feature(
                    self.by_name[match.group(1)], row, encode_text, encode_embedding, merge
                )
            )
            cursor = match.end()
        if cursor < len(self.config.template):
            output.append(encode_text(self.config.template[cursor:]))
        return output


def _validate_feature(feature: dict[str, Any]) -> None:
    kind = feature.get("feature_type")
    if kind not in FEATURE_TYPES:
        raise ValueError(f"unsupported feature_type: {kind}")
    for key in COMPONENT_TYPES & feature.keys():
        if not isinstance(feature[key], dict) or "type" not in feature[key]:
            raise ValueError(f"{key} must contain a type")
    if kind in {"combo", "sequence"}:
        children = feature.get("features")
        if not children:
            raise ValueError(f"{kind} feature needs child features")
        for child in children:
            _validate_feature(child)


def _compile_feature(feature, row, encode_text, encode_embedding, merge):
    kind = feature["feature_type"]
    if kind == "text":
        value = str(row.get(feature.get("expression", feature["feature_name"]), ""))
        preprocessor = feature.get("preprocessor", {})
        if preprocessor.get("type") == "lowercase":
            value = value.lower()
        maximum = preprocessor.get("params", {}).get("max_characters")
        if maximum:
            value = value[: int(maximum)]
        values = [encode_text(value)]
    elif kind == "embedding":
        values = [encode_embedding(row[feature.get("expression", feature["feature_name"])])]
    elif kind == "combo":
        children = []
        for child in feature["features"]:
            children.extend(_compile_feature(child, row, encode_text, encode_embedding, merge))
        values = [merge(children, feature["merger"])]
    else:
        source = row[feature.get("expression", feature["feature_name"])]
        maximum = int(feature.get("max_length", len(source)))
        values = []
        for index in range(max(0, len(source) - maximum), len(source)):
            scoped = dict(row)
            for child in _descendants(feature["features"]):
                expression = child.get("expression", child["feature_name"])
                candidate = row.get(expression)
                scoped[expression] = candidate[index] if isinstance(candidate, (list, tuple)) else candidate
            item_values = []
            for child in feature["features"]:
                item_values.extend(_compile_feature(child, scoped, encode_text, encode_embedding, merge))
            values.extend(item_values)
    if feature.get("merger") and kind not in {"combo"}:
        values = [merge(values, feature["merger"])]
    return values


def _descendants(features):
    for feature in features:
        yield feature
        yield from _descendants(feature.get("features", ()))
