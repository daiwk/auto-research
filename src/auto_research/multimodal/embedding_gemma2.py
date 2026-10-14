"""Official EmbeddingGemma 2 inference: pinned weights, masked mean + MRL.

No training recipe is reproduced and no replacement encoder is used when the
upstream model architecture is unavailable in the installed Transformers.
"""
from __future__ import annotations

import re
from pathlib import Path

MODEL_ID = "google/embeddinggemma-2"
REVISION = "914f7f89142e33e77833254d9c9b90c3cef7303b"
TRANSFORMERS_SOURCE_REVISION = "28034545c35acac05793695bd5c878f66e6b544e"
WEIGHTS_SHA256 = "197a32965d4b1105faf060417baa899e193fb73cd401f42ec9295234d5553d79"


def checkpoint_inputs(directory):
    """Include SentencePiece and chat templates as well as JSON/weights."""
    from auto_research.oct12_public_sources import checkpoint_input_files
    root = Path(directory)
    files = checkpoint_input_files(root)
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts[:2] != (".cache", "huggingface") and path.is_file() and path.suffix in {".model", ".jinja"}:
            files[relative.as_posix()] = path
    return files


def masked_mean(hidden, mask, *, dimensions=768):
    import torch
    if hidden.ndim != 3 or mask.shape != hidden.shape[:2]:
        raise ValueError("hidden tokens and processor attention mask must align")
    if dimensions not in (128, 256, 512, 768) or dimensions > hidden.shape[-1]:
        raise ValueError("EmbeddingGemma 2 requires a supported MRL prefix")
    weights = mask.to(torch.float32)[..., None]
    counts = weights.sum(1)
    if not torch.isfinite(hidden).all() or not (counts > 0).all():
        raise ValueError("nonfinite output or empty attention mask")
    vector = (hidden.float() * weights).sum(1) / counts
    # Always slice before final normalization; normalization before slicing
    # alone yields non-unit vectors and changes cosine/ranking semantics.
    vector = vector[..., :dimensions]
    if not (vector.norm(dim=-1) > 0).all():
        raise ValueError("zero embedding cannot support cosine retrieval")
    return torch.nn.functional.normalize(vector, dim=-1)


class EmbeddingGemma2Encoder:
    def __init__(self, processor, model, *, device="cpu", dimensions=768):
        self.processor, self.model = processor, model
        self.device, self.dimensions = device, dimensions

    @classmethod
    def load(cls, *, checkpoint_path=None, revision=REVISION, device="cpu", dimensions=768):
        if not re.fullmatch(r"[a-f0-9]{40}", revision):
            raise ValueError("use an immutable official checkpoint revision, not main/latest")
        import torch
        from transformers import AutoConfig, AutoModel, AutoProcessor
        from transformers.models.auto.configuration_auto import CONFIG_MAPPING
        if "embedding_gemma2" not in CONFIG_MAPPING:
            raise RuntimeError("installed Transformers lacks EmbeddingGemma2; use the documented pinned upstream source, not a substitute model")
        from auto_research.oct12_public_sources import checkpoint_source
        source, pinned, manifest = checkpoint_source(MODEL_ID, revision, checkpoint_path)
        if checkpoint_path is not None:
            if not set(checkpoint_inputs(checkpoint_path)) <= set(manifest["file_sha256"]):
                raise ValueError("all tokenizer and template inputs must be hash-verified")
            if revision == REVISION and manifest["file_sha256"].get("model.safetensors") != WEIGHTS_SHA256:
                raise ValueError("official pinned weights SHA256 mismatch")
        kwargs = {**pinned, "trust_remote_code": False}
        config = AutoConfig.from_pretrained(source, **kwargs)
        if config.model_type != "embedding_gemma2":
            raise ValueError("checkpoint is not the official EmbeddingGemma 2 architecture")
        # Text+vision retrieval does not instantiate the unused audio tower.
        config.audio_config = None
        processor = AutoProcessor.from_pretrained(source, **kwargs)
        model = AutoModel.from_pretrained(source, config=config, dtype=torch.float32,
                                         attn_implementation="eager", **kwargs).to(device).eval()
        model.requires_grad_(False)
        return cls(processor, model, device=device, dimensions=dimensions)

    def encode(self, *, texts=None, images=None, role="query", batch_size=4):
        import torch
        if (texts is None) == (images is None) or role not in ("query", "document") or batch_size < 1:
            raise ValueError("one input modality and a valid role/batch required")
        inputs = texts if texts is not None else images
        if not inputs:
            raise ValueError("no examples")
        vectors = []
        for start in range(0, len(inputs), batch_size):
            rows = inputs[start:start + batch_size]
            if texts is not None:
                prefix = "task: search result | query: " if role == "query" else "title: none | text: "
                batch = self.processor(text=[prefix + text for text in rows], padding=True,
                                       truncation=True, max_length=256, return_tensors="pt")
            else:
                # A flat image list means ONE interleaved multi-image example
                # upstream. Nested singletons preserve retrieval sample axes.
                batch = self.processor(images=[[image] for image in rows], padding=True, return_tensors="pt",
                                       max_soft_tokens=70)
            batch = {key: value.to(self.device) if isinstance(value, torch.Tensor) else value
                     for key, value in batch.items()}
            with torch.inference_mode():
                output = self.model(**batch)
            vector = masked_mean(output.last_hidden_state, batch["attention_mask"], dimensions=self.dimensions)
            if len(vector) != len(rows):
                raise ValueError("processor/model collapsed distinct retrieval samples")
            vectors.append(vector.cpu())
        return torch.cat(vectors)


def retrieval_recall(image_vectors, text_vectors, text_image_ids, image_ids):
    """Multi-positive paired retrieval; do not assume one caption per image."""
    import torch
    if (image_vectors.ndim != 2 or text_vectors.ndim != 2
            or len(image_vectors) != len(image_ids) or not image_ids
            or image_vectors.shape[1] != text_vectors.shape[1]
            or not torch.isfinite(image_vectors).all() or not torch.isfinite(text_vectors).all()):
        raise ValueError("finite paired embedding matrices with matching dimensions required")
    if len(set(image_ids)) != len(image_ids) or len(text_image_ids) != len(text_vectors):
        raise ValueError("unique images and a paired caption map required")
    if set(text_image_ids) != set(image_ids):
        raise ValueError("every image needs captions; no unmapped caption allowed")
    scores = image_vectors @ text_vectors.T
    text_ids = torch.tensor([image_ids.index(identity) for identity in text_image_ids])
    image_ranks, text_ranks = [], []
    for i in range(len(image_ids)):
        order = torch.argsort(scores[i], descending=True, stable=True)
        image_ranks.append(int((text_ids[order] == i).nonzero()[0]) + 1)
    for j in range(len(text_image_ids)):
        order = torch.argsort(scores[:, j], descending=True, stable=True)
        text_ranks.append(int((order == text_ids[j]).nonzero()[0]) + 1)
    return {f"{direction}.recall_at_{k}": sum(rank <= k for rank in ranks) / len(ranks)
            for direction, ranks in (("image_to_text", image_ranks), ("text_to_image", text_ranks))
            for k in (1, 5, 10)}
