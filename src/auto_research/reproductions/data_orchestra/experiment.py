from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

import numpy as np

from auto_research.datasets import wikitext_2
from auto_research.evolution.llm_data import load_llm_evolution_data
from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.runtime import device_for

from ..llm_training import (
    evaluate_language_model,
    require_torch,
    seed_everything,
    train_language_model,
)
from .model import (
    ACTIONS,
    OPERATIONS,
    apply_operation,
    build_orchestrator,
    decide,
    programmatic_teacher,
    text_features,
)


def _blocks(text: str, maximum=1800):
    # WikiText uses blank lines containing a single space, so literal "\n\n"
    # is not a valid paragraph delimiter.
    values = [
        block.strip()
        for block in re.split(r"\n\s*\n", text)
        if block.strip()
    ]
    return values[:maximum]


def _train_orchestrator(blocks, seed, torch):
    seed_everything(seed, torch)
    features = np.stack([text_features(block) for block in blocks])
    labels = np.asarray([programmatic_teacher(block) for block in blocks])
    split = np.arange(len(blocks)) % 5 != 0
    device = device_for(torch)
    model = build_orchestrator(features.shape[1]).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-3)
    rng = np.random.default_rng(seed)
    groups = {
        key: np.flatnonzero(
            split
            & (labels[:, 0] == key[0])
            & ((labels[:, 1] == key[1]) if key[0] == 2 else True)
        )
        for key in {(int(action), int(operation)) for action, operation in labels}
    }
    groups = {key: value for key, value in groups.items() if len(value)}
    losses = []
    for _ in range(90):
        # The paper explicitly prevents the majority "leave unchanged" route
        # from starving rare rewrite programs. Balance action/operation routes
        # in the tiny local policy-training set for the same reason.
        per_group = max(8, 96 // len(groups))
        indices = np.concatenate(
            [
                rng.choice(values, per_group, replace=True)
                for values in groups.values()
            ]
        )
        values = torch.tensor(features[indices], device=device)
        action, operation = model(values)
        action_loss = torch.nn.functional.cross_entropy(
            action, torch.tensor(labels[indices, 0], device=device)
        )
        clean = labels[indices, 0] == 2
        operation_loss = torch.nn.functional.cross_entropy(
            operation[clean],
            torch.tensor(labels[indices[clean], 1], device=device),
        )
        loss = action_loss + operation_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    held_out = np.flatnonzero(~split)
    with torch.inference_mode():
        action, operation = model(
            torch.tensor(features[held_out], device=device)
        )
        action_accuracy = float(
            (
                action.argmax(-1).cpu().numpy() == labels[held_out, 0]
            ).mean()
        )
        clean = labels[held_out, 0] == 2
        operation_accuracy = float(
            (
                operation.argmax(-1).cpu().numpy()[clean]
                == labels[held_out, 1][clean]
            ).mean()
        )
    return model, {
        "initial_loss": float(np.mean(losses[:10])),
        "final_loss": float(np.mean(losses[-10:])),
        "held_out_action_accuracy": action_accuracy,
        "held_out_operation_accuracy": operation_accuracy,
    }


def _orchestrate(model, blocks, torch):
    output, actions, operations, confidences = [], Counter(), Counter(), []
    for block in blocks:
        decision = decide(model, block, torch)
        actions[decision.action] += 1
        confidences.append(decision.confidence)
        if decision.action == "drop":
            continue
        if decision.action == "untouched":
            output.append(block)
        else:
            operations[decision.operation] += 1
            output.append(apply_operation(block, decision.operation))
    return "\n\n".join(output), {
        "actions": dict(actions),
        "operations": dict(operations),
        "mean_confidence": float(np.mean(confidences)),
    }


def _static_clean(blocks):
    return "\n\n".join(
        apply_operation(block, "normalize")
        for block in blocks
        if len(block) >= 50
    )


def reproduce_data_orchestra(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    raw_text = wikitext_2(dataset_dir, True)
    blocks = _blocks(raw_text["train"])
    orchestrator, orchestration_training = _train_orchestrator(blocks, seed, torch)
    orchestrated, decisions = _orchestrate(orchestrator, blocks, torch)
    static = _static_clean(blocks)

    data = load_llm_evolution_data(
        dataset_dir,
        True,
        vocab_size=1024,
        maximum_train_tokens=180_000,
        maximum_eval_tokens=24_000,
    )
    from tokenizers import Tokenizer

    tokenizer = Tokenizer.from_file(str(data.tokenizer_path))
    token_sets = {
        "Raw": data.train[:150_000],
        "Static cleaner": np.asarray(
            tokenizer.encode(static).ids[:150_000], dtype=np.int64
        ),
        "DataOrchestra": np.asarray(
            tokenizer.encode(orchestrated).ids[:150_000], dtype=np.int64
        ),
    }
    minimum = min(map(len, token_sets.values()))
    token_sets = {name: values[:minimum] for name, values in token_sets.items()}
    config = MicroLMConfig(
        vocab_size=data.vocab_size,
        dimensions=72,
        layers=2,
        heads=4,
        sequence_length=64,
        expansion=3,
    )
    variants = {}
    for name, tokens in token_sets.items():
        seed_everything(seed, torch)
        model = build_micro_lm("llama_modern", config)
        training = train_language_model(
            model,
            tokens,
            steps=55,
            batch_size=6,
            length=config.sequence_length,
            learning_rate=7e-4,
            seed=seed,
            torch=torch,
        )
        evaluation = evaluate_language_model(
            model,
            data.test,
            length=config.sequence_length,
            batches=32,
            torch=torch,
        )
        variants[name] = {**training, **evaluation, "train_tokens": len(tokens)}
    baseline, method = variants["Raw"], variants["DataOrchestra"]
    return {
        "paper": {
            "arxiv_id": "2607.24717",
            "title": "DataOrchestra: Learning to Orchestrate Per-Example Curation of Pretraining Data",
            "url": "https://arxiv.org/abs/2607.24717",
            "organization": "Fudan University / Shanghai Jiao Tong University / SII-GAIR",
        },
        "dataset": {
            "name": "WikiText-2",
            "source_blocks": len(blocks),
            "train_tokens_per_variant": minimum,
            "test_tokens": len(data.test),
        },
        "setup": {
            "seed": seed,
            "steps_per_model": 55,
            "same_tokens_steps_optimizer_architecture": True,
            "actions": list(ACTIONS),
            "cleaning_operations": list(OPERATIONS),
        },
        "orchestrator_training": orchestration_training,
        "decisions": decisions,
        "variants": variants,
        "relative": {
            "perplexity_reduction_vs_raw_percent": 100
            * (baseline["perplexity"] - method["perplexity"])
            / baseline["perplexity"]
        },
        "paper_results": {
            "0.5B_raw_average": 37.63,
            "0.5B_dataorchestra_average": 39.99,
            "1.5B_raw_average": 39.87,
            "1.5B_dataorchestra_average": 42.44,
            "7B_raw_average": 44.79,
            "7B_dataorchestra_average": 47.66,
        },
        "scope": (
            "实际训练逐文档 orchestrator，在 drop/untouched/clean 之间路由，并为 clean "
            "选择 normalize/deduplicate/wiki/repair 操作；随后以相同 token、step、优化器"
            "和 Llama-style 小模型预算比较 raw、固定清洗与 orchestration 预训练。"
            "程序化质量教师替代论文 LLM 合成决策，WikiText-2 替代 20B/30B token 多语料。"
        ),
    }
