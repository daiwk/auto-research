"""Pinned Bespoke Nimble checkpoint provider for the System One contract."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
from typing import Any, Mapping, Protocol

from .contracts import (
    ChoiceQuestion,
    DecisionAnswer,
    NoulQuestion,
    ScoreQuestion,
    SystemOneRequest,
    SystemOneResponse,
)


NIMBLE_REPO_ID = "bespokelabs/Bespoke-Nimble-9B"
NIMBLE_REVISION = "594dfdcfb6f94e3d0c0db7535180d3c71689169a"
NIMBLE_BASE_MODEL = "Qwen/Qwen3.5-9B"
NIMBLE_BASE_REVISION = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"
NIMBLE_ADAPTER_SHA256 = (
    "ba7e28acb97f973e80fa51f3aa6fc6f75ea4081b89632ed45d8e5f3a1d7bfa6b"
)


class NimbleScorer(Protocol):
    def score(
        self,
        context: str,
        schema: Mapping[str, Any],
        score_fields: tuple[str, ...] = (),
    ) -> Mapping[str, Any]: ...


class NimbleProvider:
    """Map Nimble's bounded candidate scorer onto provider-neutral decisions."""

    def __init__(
        self,
        scorer: NimbleScorer,
        *,
        temperature: float = 1.0,
        checkpoint_revision: str = NIMBLE_REVISION,
    ) -> None:
        if not math.isfinite(temperature) or temperature <= 0.0:
            raise ValueError("Nimble temperature must be a finite positive number")
        self.scorer = scorer
        self.temperature = float(temperature)
        self.checkpoint_revision = checkpoint_revision

    @classmethod
    def from_checkpoint(
        cls,
        checkpoint_dir: Path | None = None,
        *,
        base_model_dir: Path | None = None,
        allow_download: bool = True,
        revision: str = NIMBLE_REVISION,
        device: str = "cuda:0",
        precision: str = "bf16",
        temperature: float = 1.0,
    ) -> "NimbleProvider":
        if revision != NIMBLE_REVISION:
            raise ValueError("Nimble revision must remain pinned to the audited commit")
        root = _snapshot(
            checkpoint_dir,
            allow_download=allow_download,
            repo_id=NIMBLE_REPO_ID,
            revision=revision,
            patterns=(
                "adapter_config.json",
                "adapter_model.safetensors",
                "inference.py",
                "parallel_schema.py",
                "schema_config.json",
                "tokenizer.json",
                "tokenizer_config.json",
                "chat_template.jinja",
            ),
        )
        _assert_sha256(
            root / "adapter_model.safetensors",
            NIMBLE_ADAPTER_SHA256,
            "Nimble adapter",
        )
        scorer = _TorchNimbleScorer(
            root,
            base_model_dir=base_model_dir,
            allow_download=allow_download,
            device=device,
            precision=precision,
        )
        return cls(
            scorer,
            temperature=temperature,
            checkpoint_revision=revision,
        )

    def decide(self, decision: SystemOneRequest) -> SystemOneResponse:
        context = (
            decision.state
            if isinstance(decision.state, str)
            else json.dumps(decision.state, ensure_ascii=False, sort_keys=True)
        )
        score_fields = tuple(
            key for key, question in decision.questions.items()
            if isinstance(question, ScoreQuestion)
        )
        schema, score_labels = _nimble_schema(decision)
        raw = self.scorer.score(context, schema, score_fields=score_fields)
        fields = raw.get("fields")
        if not isinstance(fields, Mapping) or set(fields) != set(decision.questions):
            raise ValueError("Nimble response fields do not match request")
        answers: dict[str, DecisionAnswer] = {}
        for key, question in decision.questions.items():
            item = fields[key]
            if not isinstance(item, Mapping):
                raise ValueError(f"Nimble answer {key!r} must be an object")
            probabilities = _temperature_probabilities(
                item, self.temperature, key
            )
            if isinstance(question, NoulQuestion):
                checked = _probabilities(probabilities, ("false", "true"), key)
                answers[key] = DecisionAnswer(
                    "noul",
                    checked["true"] >= 0.5,
                    {"no": checked["false"], "yes": checked["true"]},
                    max(checked.values()),
                )
            elif isinstance(question, ChoiceQuestion):
                labels = tuple(question.criteria)
                checked = _probabilities(probabilities, labels, key)
                winner = max(checked, key=checked.get)
                answers[key] = DecisionAnswer(
                    "choice", winner, checked, max(checked.values())
                )
            elif isinstance(question, ScoreQuestion):
                labels = tuple(question.criteria)
                indexed = _probabilities(
                    probabilities, tuple(str(i) for i in range(len(labels))), key
                )
                checked = {
                    label: indexed[str(index)]
                    for index, label in enumerate(labels)
                }
                levels = [_numeric_level(label, i) for i, label in enumerate(labels)]
                expected = sum(
                    checked[label] * level
                    for label, level in zip(labels, levels, strict=True)
                )
                answers[key] = DecisionAnswer(
                    "score", float(expected), checked, max(checked.values())
                )
                if tuple(score_labels[key]) != labels:
                    raise ValueError(f"Nimble score labels changed for {key!r}")
            else:  # pragma: no cover
                raise TypeError(f"unsupported Nimble question: {type(question)!r}")
        return SystemOneResponse(
            model=f"nimble:{NIMBLE_REPO_ID}@{self.checkpoint_revision}",
            answers=answers,
            usage={"output_tokens": 0},
        )


class _TorchNimbleScorer:
    """Faithful CUDA scorer with an explicit offline base-model path."""

    def __init__(
        self,
        adapter_dir: Path,
        *,
        base_model_dir: Path | None,
        allow_download: bool,
        device: str,
        precision: str,
    ) -> None:
        if precision != "bf16":
            raise ValueError("the audited Nimble checkpoint path requires bf16")
        try:
            import torch
            from peft import PeftModel
            from transformers import AutoTokenizer, Qwen3_5ForConditionalGeneration
        except ImportError as exc:  # pragma: no cover - optional GPU dependencies
            raise RuntimeError(
                "Install auto-research[system-one-gpu] for Nimble"
            ) from exc
        target = torch.device(device)
        if target.type != "cuda" or not torch.cuda.is_available():
            raise RuntimeError("the audited Nimble path requires an NVIDIA CUDA device")
        if not torch.cuda.is_bf16_supported():
            raise RuntimeError("the selected CUDA device does not support bf16")
        contract = json.loads((adapter_dir / "schema_config.json").read_text())
        if (
            contract.get("task") != "schema_candidate_classification_v1"
            or contract.get("model") != NIMBLE_BASE_MODEL
            or contract.get("revision") != NIMBLE_BASE_REVISION
        ):
            raise ValueError("Nimble checkpoint contract does not match the audited base")
        source = adapter_dir / "parallel_schema.py"
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if digest != contract.get("prompt_code_sha256"):
            raise ValueError("Nimble prompt source hash does not match schema_config.json")
        self.schema = _load_module(source, "auto_research_nimble_schema")
        base = (
            str(Path(base_model_dir).expanduser().resolve())
            if base_model_dir is not None
            else NIMBLE_BASE_MODEL
        )
        if base_model_dir is None and not allow_download:
            raise FileNotFoundError("offline Nimble requires --base-model-dir")
        self.tokenizer = AutoTokenizer.from_pretrained(
            adapter_dir, local_files_only=True
        )
        model = Qwen3_5ForConditionalGeneration.from_pretrained(
            base,
            revision=None if base_model_dir is not None else NIMBLE_BASE_REVISION,
            local_files_only=base_model_dir is not None or not allow_download,
            dtype=torch.bfloat16,
            attn_implementation="sdpa",
        ).to(target)
        model.config.use_cache = False
        self.model = PeftModel.from_pretrained(
            model, adapter_dir, local_files_only=True
        ).eval()
        self.device = target
        self.max_length = int(contract["max_length"])
        self.torch = torch

    def score(self, context, schema, score_fields=()):
        prepared = self.schema.prepare_prompts(
            self.tokenizer, context, schema, self.max_length
        )
        fields = {}
        score_fields = set(score_fields)
        with self.torch.inference_mode(), self.torch.autocast(
            "cuda", dtype=self.torch.bfloat16
        ):
            for index, name in enumerate(prepared.names):
                input_ids = self.torch.tensor(
                    [prepared.full_ids[index]], device=self.device
                )
                candidate_ids = self.torch.tensor(
                    prepared.candidate_ids[index], device=self.device
                )
                logits = self.model(
                    input_ids=input_ids,
                    attention_mask=self.torch.ones_like(input_ids),
                    use_cache=False,
                    logits_to_keep=1,
                ).logits[0, -1].float().index_select(0, candidate_ids)
                choices = prepared.choices[index]
                keys = [self.schema.choice_key(value) for value in choices]
                fields[name] = {
                    "logits": dict(zip(keys, logits.double().cpu().tolist(), strict=True)),
                    "scores": dict(zip(
                        keys,
                        logits.double().softmax(-1).cpu().tolist(),
                        strict=True,
                    )),
                }
                if name in score_fields:
                    fields[name]["expected_score"] = sum(
                        int(value) * probability
                        for value, probability in zip(
                            choices,
                            fields[name]["scores"].values(),
                            strict=True,
                        )
                    )
        return {"fields": fields}


def _snapshot(path, *, allow_download, repo_id, revision, patterns):
    if path is not None:
        root = Path(path).expanduser().resolve()
    else:
        if not allow_download:
            raise FileNotFoundError(f"offline mode requires a local {repo_id} snapshot")
        try:
            from huggingface_hub import snapshot_download
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install auto-research[system-one-gpu]") from exc
        root = Path(snapshot_download(
            repo_id=repo_id,
            revision=revision,
            token=False,
            allow_patterns=list(patterns),
        ))
    if not root.is_dir():
        raise FileNotFoundError(f"checkpoint directory not found: {root}")
    return root


def _assert_sha256(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"{label} weight is missing: {path}")
    with path.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    if digest != expected:
        raise ValueError(f"{label} weight SHA256 does not match the audited checkpoint")


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load source module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _text(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value
    if value is not None:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return fallback


def _nimble_schema(decision: SystemOneRequest):
    schema: dict[str, Any] = {}
    score_labels: dict[str, tuple[str, ...]] = {}
    for key, question in decision.questions.items():
        description = _text(question.instructions, "Evaluate this structured decision.")
        if isinstance(question, NoulQuestion):
            schema[key] = {"type": "boolean", "description": description}
        elif isinstance(question, ChoiceQuestion):
            labels = list(question.criteria)
            schema[key] = {
                "type": "enum",
                "description": description,
                "choices": labels,
                "choice_descriptions": {
                    label: _text(question.criteria[label], label) for label in labels
                },
            }
        elif isinstance(question, ScoreQuestion):
            labels = tuple(question.criteria)
            values = [str(index) for index in range(len(labels))]
            schema[key] = {
                "type": "enum",
                "description": description,
                "choices": values,
                "choice_descriptions": {
                    value: _text(question.criteria[label], label)
                    for value, label in zip(values, labels, strict=True)
                },
            }
            score_labels[key] = labels
        else:  # pragma: no cover
            raise TypeError(f"unsupported Nimble question: {type(question)!r}")
    return schema, score_labels


def _temperature_probabilities(item, temperature, question_id):
    logits = item.get("logits")
    if isinstance(logits, Mapping) and logits:
        keys = list(logits)
        values = [float(logits[key]) / temperature for key in keys]
        if any(not math.isfinite(value) for value in values):
            raise ValueError(f"Nimble answer {question_id!r} contains invalid logits")
        pivot = max(values)
        exp = [math.exp(value - pivot) for value in values]
        total = sum(exp)
        return {key: value / total for key, value in zip(keys, exp, strict=True)}
    scores = item.get("scores") or item.get("probabilities")
    if temperature != 1.0:
        raise ValueError("Nimble temperature search requires checkpoint logits")
    if not isinstance(scores, Mapping):
        raise ValueError(f"Nimble answer {question_id!r} has no probability map")
    return dict(scores)


def _probabilities(raw, expected, question_id):
    if set(raw) != set(expected):
        raise ValueError(
            f"Nimble answer {question_id!r} probability labels do not match request"
        )
    result = {key: float(raw[key]) for key in expected}
    if any(not math.isfinite(value) or not 0 <= value <= 1 for value in result.values()):
        raise ValueError(f"Nimble answer {question_id!r} has invalid probabilities")
    if not math.isclose(sum(result.values()), 1.0, abs_tol=1e-5):
        raise ValueError(f"Nimble answer {question_id!r} probabilities do not sum to one")
    return result


def _numeric_level(label: str, fallback: int) -> float:
    try:
        return float(label)
    except ValueError:
        return float(fallback)
