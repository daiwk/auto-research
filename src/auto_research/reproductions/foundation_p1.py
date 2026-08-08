"""Small public-data executions of the five foundation-model P1 mechanisms."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from auto_research.evolution.llm_data import load_llm_evolution_data
from .industrial_2026 import load_industrial_data, softmax


def _text_tokens(dataset_dir: Path):
    data = load_llm_evolution_data(
        dataset_dir, allow_network=True, vocab_size=256,
        maximum_train_tokens=80_000, maximum_eval_tokens=8_000,
        benchmark_suite="core",
    )
    return np.asarray(data.train, dtype=np.int64), np.asarray(data.validation, dtype=np.int64)


def _quantize(values, bits=4):
    bound = 2 ** (bits - 1) - 1
    scale = np.max(np.abs(values), axis=0, keepdims=True) + 1e-8
    return np.clip(np.round(values / scale * bound), -bound, bound) * scale / bound


def reproduce_clip(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 220, 360)
    rng = np.random.default_rng(seed)
    x = data.sequences.features.astype(np.float64)
    # Two observable public views: collaborative/content representation and a
    # deliberately different title/genre-style nonlinear view.
    y = np.concatenate((x[:, ::2], np.square(x[:, 1::2])), axis=1)[:, : x.shape[1]]
    split = min(280, len(x) - 40)
    wx = rng.normal(scale=0.08, size=(x.shape[1], 24))
    wy = rng.normal(scale=0.08, size=(y.shape[1], 24))
    losses = []
    for _ in range(100):
        vx, ty = x[:split] @ wx, y[:split] @ wy
        vx /= np.linalg.norm(vx, axis=1, keepdims=True) + 1e-8
        ty /= np.linalg.norm(ty, axis=1, keepdims=True) + 1e-8
        logits = vx @ ty.T / 0.10
        row = np.apply_along_axis(softmax, 1, logits)
        col = np.apply_along_axis(softmax, 0, logits)
        target = np.eye(split)
        grad = 0.5 * ((row - target) + (col - target)) / split / 0.10
        wx -= 0.04 * x[:split].T @ (grad @ ty)
        wy -= 0.04 * y[:split].T @ (grad.T @ vx)
        losses.append(float(-np.log(np.diag(row) + 1e-8).mean()))
    vx, ty = x[split:] @ wx, y[split:] @ wy
    vx /= np.linalg.norm(vx, axis=1, keepdims=True) + 1e-8
    ty /= np.linalg.norm(ty, axis=1, keepdims=True) + 1e-8
    retrieval = float(np.mean(np.argmax(vx @ ty.T, axis=1) == np.arange(len(vx))))
    random = 1.0 / max(1, len(vx))
    return {"paper": {"title": "CLIP"}, "dataset": {"name": "MovieLens-100K paired item views", "pairs": len(x)},
            "baseline": {"name": "random cross-modal retrieval", "recall_at_1": random},
            "method": {"name": "symmetric contrastive image-text encoder", "recall_at_1": retrieval},
            "relative": {"recall_at_1_points": 100 * (retrieval - random)},
            "stages": {"symmetric_infonce_updates": 100, "temperature": 0.10,
                       "initial_loss": losses[0], "final_loss": losses[-1]},
            "paper_results": {"imagenet_zero_shot_top1": 76.2, "pretraining_pairs_million": 400},
            "scope": "用 MovieLens 公开 item 的两种观测视图执行双塔、归一化和双向 InfoNCE；没有复刻 4 亿图文对。"}


def reproduce_llava(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 220, 360)
    x = data.sequences.features.astype(np.float64)
    classes = int(data.domains.max()) + 1
    labels = np.eye(classes)[data.domains]
    split = min(280, len(x) - 40)
    # Frozen vision features -> trainable projector -> frozen symbolic decoder
    # vocabulary. Ridge is the closed-form SFT optimum for this small connector.
    projector = np.linalg.solve(x[:split].T @ x[:split] + 0.1 * np.eye(x.shape[1]), x[:split].T @ labels[:split])
    logits = x[split:] @ projector
    accuracy = float(np.mean(np.argmax(logits, axis=1) == data.domains[split:]))
    baseline = float(np.max(np.bincount(data.domains[:split], minlength=classes)) / split)
    return {"paper": {"title": "LLaVA: Visual Instruction Tuning"},
            "dataset": {"name": "MovieLens-100K item-content instruction proxy", "examples": len(x)},
            "baseline": {"name": "majority response", "instruction_accuracy": baseline},
            "method": {"name": "frozen encoder + trained projector + response decoder", "instruction_accuracy": accuracy},
            "relative": {"instruction_accuracy_points": 100 * (accuracy - baseline)},
            "stages": {"frozen_vision_encoder": True, "projector_shape": list(projector.shape),
                       "visual_instruction_sft": True},
            "paper_results": {"synthetic_gpt4_relative_score_percent": 85.1, "scienceqa_accuracy": 92.53},
            "scope": "公开 item 内容向量替代图像 encoder，训练真实跨模态 projector 和 instruction 分类头；未调用 GPT-4 或复刻 LLaVA-13B。"}


def _transition(tokens, vocab=256, smoothing=0.2):
    table = np.full((vocab, vocab), smoothing, dtype=np.float64)
    np.add.at(table, (tokens[:-1] % vocab, tokens[1:] % vocab), 1.0)
    table /= table.sum(1, keepdims=True)
    return table


def reproduce_speculative_decoding(dataset_dir: Path, seed: int = 42):
    train, validation = _text_tokens(dataset_dir)
    target = _transition(train)
    # A rank-32 transition factorization is the small draft model; unlike a
    # strided corpus it approximates the same next-token task without inventing
    # non-adjacent transitions.
    left, singular, right = np.linalg.svd(target, full_matrices=False)
    draft = np.maximum((left[:, :32] * singular[:32]) @ right[:32], 1e-9)
    draft /= draft.sum(1, keepdims=True)
    prefix = int(validation[0])
    baseline, speculative = [], []
    current = prefix
    for _ in range(160):
        current = int(np.argmax(target[current]))
        baseline.append(current)
    current, target_calls, accepted = prefix, 0, 0
    while len(speculative) < len(baseline):
        proposals, state = [], current
        for _ in range(4):
            state = int(np.argmax(draft[state])); proposals.append(state)
        target_calls += 1
        for proposal in proposals:
            exact = int(np.argmax(target[current]))
            token = proposal if proposal == exact else exact
            speculative.append(token); current = token
            if proposal == exact: accepted += 1
            else: break
            if len(speculative) == len(baseline): break
    speculative = speculative[:len(baseline)]
    return {"paper": {"title": "Fast Inference via Speculative Decoding"},
            "dataset": {"name": "WikiText-2", "generated_tokens": len(baseline)},
            "baseline": {"name": "target-only greedy decoding", "target_calls": len(baseline)},
            "method": {"name": "four-token draft and exact target verification", "target_calls": target_calls},
            "relative": {"target_call_reduction_percent": 100 * (1 - target_calls / len(baseline))},
            "stages": {"draft_width": 4, "accepted_draft_tokens": accepted,
                       "exact_output_match": speculative == baseline},
            "paper_results": {"reported_speedup_x": "2-3", "distribution_preserving": True},
            "scope": "在 WikiText-2 拟合 target/draft token 模型，真实执行提议、验证和拒绝回退；target 是小型 Markov LM，不等同于 T5-XXL kernel 延迟。"}


def reproduce_awq(dataset_dir: Path, seed: int = 42):
    train, validation = _text_tokens(dataset_dir)
    rng = np.random.default_rng(seed)
    width = 32
    x = np.sin((train[:4096, None] + 1) * np.arange(1, width + 1)[None] / 37.0)
    xv = np.sin((validation[:2048, None] + 1) * np.arange(1, width + 1)[None] / 37.0)
    weight = rng.normal(scale=0.2, size=(width, width))
    reference = xv @ weight
    rtn = xv @ _quantize(weight)
    activation = np.mean(np.abs(x), axis=0) + 1e-6
    rows = []
    for alpha in np.linspace(0, 1, 11):
        scale = activation ** alpha
        quantized = _quantize(weight * scale[:, None])
        prediction = (xv / scale) @ quantized
        rows.append((float(np.mean((prediction - reference) ** 2)), float(alpha)))
    mse, alpha = min(rows)
    baseline = float(np.mean((rtn - reference) ** 2))
    return {"paper": {"title": "AWQ"}, "dataset": {"name": "WikiText-2 activation calibration", "tokens": len(x)},
            "baseline": {"name": "round-to-nearest W4", "output_mse": baseline},
            "method": {"name": "activation-aware equivalent scaling W4", "output_mse": mse},
            "relative": {"output_mse_percent": 100 * (mse - baseline) / max(baseline, 1e-12)},
            "stages": {"calibration_tokens": len(x), "bits": 4, "selected_alpha": alpha,
                       "backpropagation": False},
            "paper_results": {"tinychat_speedup_over_fp16_x": 3.0, "protected_salient_weight_percent": 1.0},
            "scope": "用 WikiText-2 激活统计搜索 AWQ 等价缩放并真实执行 W4 量化；未使用 TinyChat CUDA kernel，MSE 不代表端到端吞吐。"}


def reproduce_medusa(dataset_dir: Path, seed: int = 42):
    train, validation = _text_tokens(dataset_dir)
    transition = _transition(train)
    powers = [transition]
    for _ in range(2): powers.append(powers[-1] @ transition)
    prefix, baseline = int(validation[0]), []
    current = prefix
    for _ in range(160):
        current = int(np.argmax(transition[current])); baseline.append(current)
    current, output, calls, accepted = prefix, [], 0, []
    while len(output) < len(baseline):
        proposals = [int(np.argmax(power[current])) for power in powers]
        calls += 1
        local, state = [], current
        for proposal in proposals:
            exact = int(np.argmax(transition[state]))
            if proposal != exact: break
            local.append(proposal); state = proposal
        if not local:
            local = [int(np.argmax(transition[current]))]
        accepted.append(len(local)); output.extend(local); current = local[-1]
    output = output[:len(baseline)]
    return {"paper": {"title": "Medusa"}, "dataset": {"name": "WikiText-2", "generated_tokens": len(baseline)},
            "baseline": {"name": "single-head greedy", "backbone_calls": len(baseline)},
            "method": {"name": "three future heads + tree verification", "backbone_calls": calls},
            "relative": {"backbone_call_reduction_percent": 100 * (1 - calls / len(baseline))},
            "stages": {"medusa_heads": 3, "mean_accepted_tokens": float(np.mean(accepted)),
                       "exact_output_match": output == baseline},
            "paper_results": {"medusa1_speedup_x": 2.2, "medusa2_speedup_x": "2.3-3.6"},
            "scope": "在 WikiText-2 token 转移模型上执行多 future head、候选树和 backbone 验证；未复刻 GPU tree-attention kernel。"}


def render(result):
    baseline, method = result["baseline"], result["method"]
    metric = next(key for key in baseline if key != "name")
    return "\n".join([
        f"# {result['paper']['title']}", "", f"公开数据：{result['dataset']['name']}", "",
        f"| Variant | {metric} |", "|---|---:|",
        f"| {baseline['name']} | {baseline[metric]} |", f"| {method['name']} | {method[metric]} |", "",
        "## 复现边界", "", result["scope"], "",
    ])
