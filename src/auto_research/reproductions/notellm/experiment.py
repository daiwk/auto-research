import os
from pathlib import Path

from ..llm_rec_data import load_text_ctr_data
from ..rec_utils import load_movielens_sequences, transitions
from .model import NoteLLMConfig, build_model, embed_all, i2i_metrics, prompts, require_backend, train


def reproduce_notellm(dataset_dir: Path, seed: int = 42):
    torch, _, _ = require_backend()
    config = NoteLLMConfig(steps=int(os.environ.get("AUTO_RESEARCH_NOTELLM_STEPS", "40")))
    sequence_data = load_movielens_sequences(dataset_dir)
    text_data = load_text_ctr_data(dataset_dir)
    texts = prompts(text_data.titles, text_data.genres)
    model, tokenizer = build_model(config)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu"); model.to(device)
    baseline = i2i_metrics(embed_all(model, tokenizer, texts), sequence_data)
    pairs = tuple(map(tuple, transitions(sequence_data.train).tolist()))
    training = train(model, tokenizer, texts, text_data.genres, pairs, config, seed)
    method = i2i_metrics(embed_all(model, tokenizer, texts), sequence_data)
    return {
        "paper": {"arxiv_id": "2403.01744", "title": "NoteLLM: A Retrievable Large Language Model for Note Recommendation", "url": "https://arxiv.org/abs/2403.01744", "track": "recommendation"},
        "dataset": "MovieLens 100K title/genre and co-occurrence pairs",
        "setup": {"seed": seed, "steps": config.steps, "model": config.model_name, "pairs": len(pairs)},
        "results": {"frozen_compression_embedding": baseline, "notellm_gcl_csft": method},
        "training": training,
        "paper_online_ab": {"ctr_percent": 16.20, "comments_percent": 1.10, "weekly_publishers_percent": 0.41, "new_note_comments_percent": 3.58},
        "scope": "Executes a note-compression special token in a real seq2seq LM, behavior co-occurrence GCL, category-generating CSFT, and I2I retrieval from the learned compression state.",
    }
