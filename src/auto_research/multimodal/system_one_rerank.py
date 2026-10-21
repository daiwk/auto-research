"""One-forward multimodal choice readout from arXiv:2610.28435 v1.

This is a checkpoint-backed inference component, not a supplied-score ranker.
The caller loads a trusted, pinned VLM and processor; this module never downloads
weights, generates text, or supplies an answer to the model.  A smaller backbone
is an L1 mechanism diagnostic, not the paper's 27B benchmark reproduction.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
from io import BytesIO
import math
import random
import re
from typing import Any, Mapping, Sequence


PAPER_ID = "2610.28435v1"
UPSTREAM_REVISION = "f7c9a5a110dc9e1e4c7c1550c8938212e5ae3f27"
MAX_CANDIDATES = 16
PAPER_MAX_PIXELS = 1800 * 32 * 32
CHOICE_QUESTION = "Which candidate best matches the query, following the instruction?"


@dataclass(frozen=True)
class MultimodalInput:
    """Only model-visible text/images; no relevance labels or benchmark metadata."""

    text: str = ""
    images: tuple[Any, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.text, str) or not isinstance(self.images, tuple):
            raise TypeError("text must be a string and images a tuple of PIL images")
        if not self.text.strip() and not self.images:
            raise ValueError("a model input must contain text or an image")


@dataclass(frozen=True)
class RerankCandidate:
    identifier: str
    content: MultimodalInput

    def __post_init__(self) -> None:
        if not isinstance(self.identifier, str) or not self.identifier.strip():
            raise ValueError("candidate identifiers must be non-empty strings")
        if type(self.content) is not MultimodalInput:
            raise TypeError("candidate content must be an explicit MultimodalInput")


@dataclass(frozen=True)
class RerankCase:
    identifier: str
    query: MultimodalInput
    candidates: tuple[RerankCandidate, ...]
    instruction: str


@dataclass(frozen=True)
class RerankResult:
    candidate_ids: tuple[str, ...]
    ranked_ids: tuple[str, ...]
    ranked_indices: tuple[int, ...]
    # Only the top-K candidates have choice probabilities; tail scores are absent.
    probabilities: tuple[float, ...] | None
    rerank_depth: int
    forward_passes: int
    autoregressive_decode_steps: int
    prompt_tokens: int
    label_token_ids: tuple[int, ...]
    restricted_probability_mass: float | None
    image_provenance: tuple[Mapping[str, Any], ...]
    fallback_used: bool = False
    failure_type: str | None = None
    input_ids_sha256: str | None = None
    selected_logits_sha256: str | None = None


def _text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _image(image: Any, max_pixels: int) -> tuple[Any, dict[str, Any]]:
    from PIL import Image

    if not isinstance(image, Image.Image):
        raise TypeError("image inputs must be decoded PIL images, not paths or URLs")
    rgb = image.convert("RGB")
    original_size = rgb.size
    if rgb.width * rgb.height > max_pixels:
        factor = math.sqrt(max_pixels / (rgb.width * rgb.height))
        size = (max(1, int(rgb.width * factor)), max(1, int(rgb.height * factor)))
        rgb = rgb.resize(size, Image.Resampling.BICUBIC)
    # Paper Appendix B transmits RGB JPEG quality 90; retain that input contract
    # even for the in-process backend, without network or filesystem transport.
    encoded = BytesIO()
    rgb.save(encoded, format="JPEG", quality=90)
    payload = encoded.getvalue()
    with Image.open(BytesIO(payload)) as decoded:
        ready = decoded.convert("RGB").copy()
    return ready, {
        "original_size": list(original_size),
        "processed_size": list(ready.size),
        "jpeg_quality": 90,
        "jpeg_sha256": hashlib.sha256(payload).hexdigest(),
    }


def build_choice_content(
    query: MultimodalInput,
    candidates: Sequence[RerankCandidate],
    instruction: str,
    *,
    max_pixels: int = PAPER_MAX_PIXELS,
) -> tuple[list[dict[str, Any]], list[Any], tuple[Mapping[str, Any], ...]]:
    """Build Appendix A's images-first, A-P-labelled user turn."""
    if type(query) is not MultimodalInput:
        raise TypeError("query must be an explicit MultimodalInput")
    if not isinstance(instruction, str) or not instruction.strip():
        raise ValueError("a non-empty task instruction is required")
    if not 2 <= len(candidates) <= MAX_CANDIDATES:
        raise ValueError("the choice prompt supports 2 to 16 candidates")
    if isinstance(max_pixels, bool) or not isinstance(max_pixels, int) or max_pixels < 1:
        raise ValueError("max_pixels must be a positive integer")
    if any(type(candidate) is not RerankCandidate for candidate in candidates):
        raise TypeError("candidates must be explicit RerankCandidate values")
    if len({candidate.identifier for candidate in candidates}) != len(candidates):
        raise ValueError("candidate identifiers must be unique")

    content: list[dict[str, Any]] = []
    images: list[Any] = []
    provenance: list[Mapping[str, Any]] = []

    def append_input(item: MultimodalInput) -> None:
        for image in item.images:
            ready, metadata = _image(image, max_pixels)
            content.append({"type": "image"})
            images.append(ready)
            provenance.append(metadata)
        if item.text.strip():
            content.append({"type": "text", "text": _text(item.text)})

    content.append({"type": "text", "text": f"Instruction: {_text(instruction)}\nQuery:"})
    append_input(query)
    content.append({"type": "text", "text": "\nCandidates:"})
    for index, candidate in enumerate(candidates):
        content.append({"type": "text", "text": f"\nCandidate {chr(65 + index)}:"})
        append_input(candidate.content)
    last = chr(64 + len(candidates))
    content.append({"type": "text", "text": (
        f"\n{CHOICE_QUESTION} Answer with the letter of the best candidate only (A-{last})."
    )})
    return content, images, tuple(provenance)


def _label_ids(tokenizer: Any, count: int) -> tuple[int, ...]:
    ids = []
    for index in range(count):
        label = chr(65 + index)
        encoded = tokenizer.encode(label, add_special_tokens=False)
        if len(encoded) != 1 or isinstance(encoded[0], bool) or not isinstance(encoded[0], int):
            raise ValueError(f"label {label!r} must encode to exactly one integer token")
        if encoded[0] < 0 or encoded[0] == getattr(tokenizer, "unk_token_id", None):
            raise ValueError(f"label {label!r} has an invalid/unknown token")
        ids.append(encoded[0])
    if len(set(ids)) != count:
        raise ValueError("candidate labels must map to distinct tokens")
    return tuple(ids)


class ForwardVLMReranker:
    """Read a real supplied VLM's first-answer logits without text generation.

    No fake backend or scores argument is accepted.  ``on_error='keep_first_stage'``
    explicitly preserves the original order and has no fabricated probabilities.
    """

    def __init__(self, processor: Any, model: Any, *, device: str | None = None) -> None:
        self.processor = processor
        self.model = model
        self.device = device or str(next(model.parameters()).device)

    def rank(
        self,
        query: MultimodalInput,
        candidates: Sequence[RerankCandidate],
        *,
        instruction: str,
        depth: int = MAX_CANDIDATES,
        on_error: str = "raise",
    ) -> RerankResult:
        import torch

        if isinstance(depth, bool) or not isinstance(depth, int) or not 2 <= depth <= 16:
            raise ValueError("depth must be an integer in [2, 16]")
        if on_error not in {"raise", "keep_first_stage"}:
            raise ValueError("on_error must be raise or keep_first_stage")
        if any(type(candidate) is not RerankCandidate for candidate in candidates):
            raise TypeError("candidates must be explicit RerankCandidate values")
        identities = tuple(candidate.identifier for candidate in candidates)
        if len(set(identities)) != len(identities):
            raise ValueError("candidate identifiers must be unique")
        if len(candidates) < 2:
            return RerankResult(identities, identities, tuple(range(len(candidates))),
                                None, len(candidates), 0, 0, 0, (), None, ())
        count = min(depth, len(candidates))
        calls, prompt_tokens = 0, 0
        label_ids: tuple[int, ...] = ()
        provenance: tuple[Mapping[str, Any], ...] = ()
        try:
            content, images, provenance = build_choice_content(query, candidates[:count], instruction)
            label_ids = _label_ids(self.processor.tokenizer, count)
            prompt = self.processor.apply_chat_template(
                [{"role": "user", "content": content}], tokenize=False,
                add_generation_prompt=True, enable_thinking=False,
            )
            kwargs: dict[str, Any] = {"text": prompt, "return_tensors": "pt"}
            if images:
                kwargs["images"] = images
            batch = self.processor(**kwargs)
            batch = {key: value.to(self.device) if hasattr(value, "to") else value
                     for key, value in batch.items()}
            input_ids = batch.get("input_ids")
            if input_ids is None or input_ids.ndim != 2 or input_ids.shape[0] != 1:
                raise ValueError("the readout requires one unpadded prompt")
            prompt_tokens = int(input_ids.shape[1])
            if not prompt_tokens:
                raise ValueError("empty model prompt")
            input_hash = hashlib.sha256(
                input_ids.detach().cpu().contiguous().numpy().tobytes()
            ).hexdigest()
            mask = batch.get("attention_mask")
            if mask is not None and int(mask[0, -1]) != 1:
                raise ValueError("the last position must be an attended answer prefix")
            was_training = self.model.training
            self.model.eval()
            try:
                with torch.inference_mode():
                    calls += 1
                    output = self.model(**batch, use_cache=False)
            finally:
                self.model.train(was_training)
            logits = output.logits
            if logits.ndim != 3 or logits.shape[0] != 1 or logits.shape[1] < 1:
                raise ValueError("model logits must have shape [1, sequence, vocabulary]")
            last = logits[0, -1].detach().float()
            if not torch.isfinite(last).all() or max(label_ids) >= last.numel():
                raise ValueError("model logits are non-finite or omit a label token")
            selected = last[list(label_ids)]
            probabilities = tuple(float(value) for value in selected.softmax(-1).cpu())
            mass = float((selected.logsumexp(0) - last.logsumexp(0)).exp().cpu())
            if not all(math.isfinite(value) for value in probabilities) or not math.isfinite(mass):
                raise ValueError("non-finite choice probabilities")
            # Python's stable original-index secondary key is Appendix B's tie rule.
            order = tuple(sorted(range(count), key=lambda index: (-probabilities[index], index)))
            order += tuple(range(count, len(candidates)))
            return RerankResult(
                identities, tuple(identities[index] for index in order), order,
                probabilities, count, calls, 0, prompt_tokens, label_ids, mass, provenance,
                input_ids_sha256=input_hash,
                selected_logits_sha256=hashlib.sha256(
                    selected.cpu().contiguous().numpy().tobytes()
                ).hexdigest(),
            )
        except Exception as error:
            if on_error == "raise":
                raise
            return RerankResult(
                identities, identities, tuple(range(len(candidates))), None, count,
                calls, 0, prompt_tokens, label_ids, None, provenance, True,
                type(error).__name__,
            )


def diagnostic(seed: int, device: str, model: Any, processor: Any) -> dict[str, Any]:
    """Small real-CUDA VLM readout, using only generated geometric RGB images.

    These are no benchmark examples and no accuracy is claimed.  The seed changes
    image layouts, not a training replicate.  The parent runner records the
    already loaded public checkpoint's immutable revision and source provenance.
    """
    import torch
    from PIL import Image, ImageDraw

    if not torch.cuda.is_available() or torch.device(device).type != "cuda":
        raise RuntimeError("the checkpoint diagnostic requires a real CUDA device")
    if next(model.parameters()).device.type != "cuda":
        raise ValueError("the caller must supply a real model already loaded on CUDA")
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    rng = random.Random(seed)
    candidates = []
    for index in range(4):
        image = Image.new("RGB", (96, 96), (245, 245, 245))
        draw = ImageDraw.Draw(image)
        left, top = rng.randrange(4, 24), rng.randrange(4, 24)
        right, bottom = rng.randrange(50, 92), rng.randrange(50, 92)
        color = tuple(rng.randrange(20, 230) for _ in range(3))
        draw.rectangle((left, top, right, bottom), fill=color)
        candidates.append(RerankCandidate(f"generated-{index}", MultimodalInput(images=(image,))))
    # Tail records make the preservation contract observable; neither is sent to
    # the VLM because this bounded component reranks only the first four records.
    candidates.extend((
        RerankCandidate("unreranked-tail-0", MultimodalInput("Tail candidate zero.")),
        RerankCandidate("unreranked-tail-1", MultimodalInput("Tail candidate one.")),
    ))
    result = ForwardVLMReranker(processor, model, device=device).rank(
        MultimodalInput("Find the image containing a large blue region."), candidates,
        instruction="Rank the candidate images by relevance to the query.", depth=4,
    )
    probabilities = result.probabilities
    if probabilities is None:
        raise RuntimeError("the checkpoint forward did not return candidate probabilities")
    metrics = {
        "vlm_forward_passes": float(result.forward_passes),
        "autoregressive_decode_steps": float(result.autoregressive_decode_steps),
        "prompt_tokens": float(result.prompt_tokens),
        "image_count": float(len(result.image_provenance)),
        "choice_normalization_error": abs(sum(probabilities) - 1.0),
        "choice_entropy": -sum(p * math.log(p) for p in probabilities if p > 0),
        "restricted_probability_mass": float(result.restricted_probability_mass),
    }
    checks = {
        "finite_metrics": all(math.isfinite(value) for value in metrics.values()),
        "one_real_vlm_forward": result.forward_passes == 1 and not result.fallback_used,
        "no_autoregressive_decoding": result.autoregressive_decode_steps == 0,
        "four_distinct_single_token_labels": len(set(result.label_token_ids)) == 4,
        "images_processed": len(result.image_provenance) == 4,
        "four_distinct_image_payloads": len({
            item["jpeg_sha256"] for item in result.image_provenance
        }) == 4,
        "normalized_choice_probabilities": metrics["choice_normalization_error"] < 1e-5,
        "tail_preserved": result.ranked_ids[-2:] == ("unreranked-tail-0", "unreranked-tail-1"),
        "input_output_hashes_recorded": bool(result.input_ids_sha256 and result.selected_logits_sha256),
    }
    return {
        "seed": seed, "metrics": metrics, "checks": checks,
        "result": asdict(result),
        "protocol": {
            "dataset": "generated_geometric_rgb_images_no_external_data",
            "image_size": [96, 96], "query_and_candidate_gold_fields": False,
            "checkpoint_loaded_by_caller": True, "pretrained_model_forward_calls": 1,
            "diagnostic_only": True, "promotion_eligible": False,
            "evolve_integrated": False, "accuracy_claim": False,
            "sampling_seeds_not_training_replicates": True,
        },
    }


def run_checkpoint_cases(
    processor: Any,
    model: Any,
    cases: Sequence[RerankCase],
    *,
    checkpoint_id: str,
    checkpoint_revision: str,
    dataset: Mapping[str, Any],
    seed: int,
    device: str = "cuda",
) -> dict[str, Any]:
    """Independent bounded CUDA runner for a caller's already loaded checkpoint.

    The caller owns public-data selection and provenance; no labels are accepted
    by ``RerankCase``.  This function measures execution, not retrieval accuracy.
    Run seeds separately; repeated frozen-model seeds are not training replicates.
    """
    import torch

    if not torch.cuda.is_available() or torch.device(device).type != "cuda":
        raise RuntimeError("the advertised checkpoint diagnostic requires real CUDA")
    if next(model.parameters()).device.type != "cuda":
        raise ValueError("the caller must load the real model on CUDA")
    if not checkpoint_id or re.fullmatch(r"[0-9a-f]{40}", checkpoint_revision) is None:
        raise ValueError("checkpoint id and immutable 40-character revision are required")
    if not cases or len(cases) > 16:
        raise ValueError("the bounded diagnostic supports 1 to 16 public cases")
    if any(type(case) is not RerankCase for case in cases):
        raise TypeError("cases must be explicit RerankCase values without gold metadata")
    if any(not case.query.images and not any(c.content.images for c in case.candidates)
           for case in cases):
        raise ValueError("every CUDA diagnostic case must actually contain an image")
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    ranker = ForwardVLMReranker(processor, model, device=device)
    rows = []
    for case in cases:
        result = ranker.rank(case.query, case.candidates, instruction=case.instruction)
        if result.forward_passes != 1 or result.fallback_used:
            raise RuntimeError("each diagnostic case must execute one successful VLM forward")
        rows.append({"case_id": case.identifier, **asdict(result)})
    return {
        "schema_version": 1,
        "adapter_key": "system-one-rerank",
        "evaluation_tier": "l1_mechanism",
        "diagnostic_only": True,
        "promotion_eligible": False,
        "evolve_integrated": False,
        "full_experiment_status": "not_reproduced_high_cost",
        "full_experiment_review_done": True,
        "paper": PAPER_ID,
        "upstream_revision": UPSTREAM_REVISION,
        "checkpoint": {"model_id": checkpoint_id, "revision": checkpoint_revision},
        "dataset": dict(dataset),
        "seed": seed,
        "rows": rows,
        "metrics": {
            "executed_cases": len(rows),
            "vlm_forward_passes": sum(row["forward_passes"] for row in rows),
            "autoregressive_decode_steps": 0,
            "choice_normalization_max_error": max(
                abs(sum(row["probabilities"]) - 1.0) for row in rows
            ),
        },
        "accelerator": torch.cuda.get_device_name(torch.device(device)),
        "limitations": [
            "L1 checkpoint-backed readout only; no capability or latency comparison",
            "No 27B/Qwen benchmark or JEV decision-head training reproduction",
            "Frozen-model seeds are not independent training replicates",
            "No gold relevance labels enter the model; no test-based selection",
        ],
    }
