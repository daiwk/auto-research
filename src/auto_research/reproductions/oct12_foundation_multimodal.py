"""Public-data diagnostic runners for MSAR, Orthros, DualQuant, WOVEN, UMRM.

No metrics are fixtures, and no reported paper metric is returned as a local
measurement. CUDA receipts are produced by the separate validation workflow.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path

import torch
from torch import nn
from torch.nn import functional as F

from auto_research.foundation_models.oct12_mechanisms import (
    DualQuantLinear, MSARLM, OrthrosLM, TinyTransformerLM,
)
from auto_research.oct12_public_sources import checkpoint_source, recorded_verified_files, verify_offline_manifest

WIKITEXT_REVISION = "b08601e04326c79dfdd32d625aee71d232d685c3"
SMOLLM_REVISION = "93efa2f097d58c2a74874c7e644dbc9b0cee75a2"
SMOLLM_CHECKPOINT = "HuggingFaceTB/SmolLM2-135M"


def load_public_text(dataset_dir: Path, train_bytes: int = 32768,
                     eval_bytes: int = 4096) -> tuple[dict[str, torch.Tensor], dict]:
    """Official split preservation; no vocabulary fitted on eval splits.

    Optional files are mirrors of the SAME public split, not an alternative
    fixture dataset. Their SHA256 is always recorded, and the caller must
    provide provenance.json identifying source and revision when mirroring.
    """
    dataset_dir = Path(dataset_dir)
    local = all((dataset_dir / f"{s}.txt").exists() for s in ("train", "validation", "test"))
    if local:
        provenance = verify_offline_manifest(dataset_dir, "Salesforce/wikitext", WIKITEXT_REVISION, "dataset")
        if provenance.get("configuration") != "wikitext-2-raw-v1" or not all(
            f"{s}.txt" in provenance["files"] for s in ("train", "validation", "test")):
            raise ValueError("local mirror must hash all THREE official raw-v1 splits")
        source = None
    else:
        from datasets import load_dataset
        source = load_dataset("Salesforce/wikitext", "wikitext-2-raw-v1",
                              revision=WIKITEXT_REVISION, cache_dir=str(dataset_dir), streaming=True)
    tokens, hashes, counts = {}, {}, {}
    for split in ("train", "validation", "test"):
        budget = train_bytes if split == "train" else eval_bytes
        if local:
            raw = (dataset_dir / f"{split}.txt").read_bytes()[:budget]
        else:
            pieces, size = [], 0
            for row in source[split]:
                piece = (row["text"] + "\n").encode("utf-8")
                pieces.append(piece)
                size += len(piece)
                if size >= budget:
                    break
            raw = b"".join(pieces)[:budget]
        tokens[split] = torch.tensor(list(raw), dtype=torch.long)
        hashes[split], counts[split] = hashlib.sha256(raw).hexdigest(), len(raw)
    return tokens, {"name": "Salesforce/wikitext", "configuration": "wikitext-2-raw-v1",
                    "revision": WIKITEXT_REVISION, "tokenization": "UTF-8 byte vocabulary (256)",
                    "split_sha256": hashes, "split_tokens": counts, "official_splits": True,
                    "offline_source_verification": recorded_verified_files(dataset_dir) if local else None}


def train_lm(model: nn.Module, tokens: torch.Tensor, steps: int, seed: int,
             length: int = 64, batch_size: int = 2, lr: float = 2e-3) -> list[float]:
    if steps < 1 or len(tokens) <= length:
        raise ValueError("positive steps and sufficient training tokens are required")
    generator = torch.Generator().manual_seed(seed)
    device = next(model.parameters()).device
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    losses = []
    model.train()
    for _ in range(steps):
        starts = torch.randint(len(tokens) - length, (batch_size,), generator=generator)
        rows = torch.stack([tokens[i:i + length + 1] for i in starts]).to(device)
        optimizer.zero_grad(set_to_none=True)
        loss = F.cross_entropy(model(rows[:, :-1]).flatten(0, 1), rows[:, 1:].flatten())
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach()))
    return losses


@torch.no_grad()
def byte_nll(model: nn.Module, tokens: torch.Tensor, length: int = 64) -> float:
    device = next(model.parameters()).device
    model.eval()
    total, count = 0.0, 0
    for offset in range(0, len(tokens) - length, length):
        row = tokens[offset:offset + length + 1][None].to(device)
        loss = F.cross_entropy(model(row[:, :-1]).flatten(0, 1), row[:, 1:].flatten(), reduction="sum")
        total, count = total + float(loss), count + length
    if not count:
        raise ValueError("evaluation split has no complete sequence")
    return total / count


def run_foundation_training(paper: str, dataset_dir: Path, seed: int = 42, *,
                            device: str = "cpu", steps: int = 40, width: int = 64,
                            layers: int = 2, sequence_length: int = 64,
                            window: int = 16, train_bytes: int = 32768,
                            eval_bytes: int = 4096) -> dict:
    if paper not in {"msar", "orthros"}:
        raise ValueError("training runner supports msar and orthros")
    torch.manual_seed(seed)
    tokens, data = load_public_text(dataset_dir, train_bytes, eval_bytes)
    baseline = TinyTransformerLM(width=width, layers=layers).to(device)
    # Shared initial embedding, branch, norm and head parameters, NOT outcomes.
    if paper == "msar":
        method = MSARLM(width=width, layers=layers, block_size=2).to(device)
        method.load_state_dict(copy.deepcopy(baseline.state_dict()), strict=False)
        conversion_steps, shared_pretraining = 0, []
    else:
        conversion_steps = max(1, steps // 4)
        shared_pretraining = train_lm(baseline, tokens["train"], conversion_steps, seed,
                                      sequence_length)
        method = OrthrosLM.from_transformer(baseline, window)
    baseline_trace = train_lm(baseline, tokens["train"], steps, seed + 1, sequence_length)
    method_trace = train_lm(method, tokens["train"], steps, seed + 1, sequence_length)
    validation = {"baseline": byte_nll(baseline, tokens["validation"], sequence_length),
                  "method": byte_nll(method, tokens["validation"], sequence_length)}
    # Fixed-budget protocol: no architecture, epoch or HP chosen on test.
    test = {"baseline": byte_nll(baseline, tokens["test"], sequence_length),
            "method": byte_nll(method, tokens["test"], sequence_length)}
    cache_check = None
    if paper == "orthros":
        prefix = tokens["validation"][:sequence_length][None].to(device)
        with torch.no_grad():
            expected = method(prefix)
            first, states = method.prefill(prefix[:, :sequence_length // 2])
            incremental = [first]
            for i in range(sequence_length // 2, sequence_length):
                out, states = method.decode(prefix[:, i:i + 1], states)
                incremental.append(out)
            actual = torch.cat(incremental, dim=1)
            err = float((actual - expected[:, sequence_length // 2 - 1:]).abs().max())
            cache_check = {"batch_vs_cached_max_abs_error": err,
                           "cache_tokens_per_layer": [s.key.shape[-2] for s in states],
                           "prefill_global_output_positions": 1,
                           "base_prefill_window": window,
                           "agreement_atol": 1e-4, "passed": err < 1e-4}
            if not cache_check["passed"]:
                raise RuntimeError("Orthros cached execution disagrees with training forward")
    return {"paper": {"key": paper}, "seed": seed, "dataset": data,
            "evaluation_tier": "L1", "fidelity": "core_mechanism", "diagnostic_only": True,
            "baseline": {"name": "matched dense causal Transformer", "test_byte_nll": test["baseline"]},
            "method": {"name": paper, "test_byte_nll": test["method"]},
            "validation": validation,
            "stages": {"training_steps_per_variant": steps, "sequence_length": sequence_length,
                       "width": width, "layers": layers, "shared_conversion_pretrain_steps": conversion_steps,
                       "initialization": "from scratch; real trainable PyTorch attention/SwiGLU LM",
                       "baseline_parameters": sum(p.numel() for p in baseline.parameters()),
                       "method_parameters": sum(p.numel() for p in method.parameters()),
                       "training_loss_first_last": {"baseline": [baseline_trace[0], baseline_trace[-1]],
                                                    "method": [method_trace[0], method_trace[-1]]},
                       "cache": cache_check, "shared_pretrain_loss": shared_pretraining[-1:]},
            "scope": "公开 WikiText byte-LM 机制诊断；不复刻论文大模型、预训练数据、kernel 或论文吞吐。"}


@torch.no_grad()
def hf_nll(model: nn.Module, ids: torch.Tensor, length: int = 128) -> float:
    device = next(model.parameters()).device
    total, count = 0.0, 0
    for start in range(0, ids.shape[1] - 1, length):
        row = ids[:, start:start + length + 1].to(device)
        if row.shape[1] < 2:
            continue
        logits = model(input_ids=row[:, :-1], use_cache=False).logits
        total += float(F.cross_entropy(logits.float().flatten(0, 1), row[:, 1:].flatten(), reduction="sum"))
        count += row.shape[1] - 1
    if not count:
        raise ValueError("empty evaluation corpus")
    return total / count


def run_dualquant(dataset_dir: Path, seed: int = 42, *, device: str = "cpu",
                   checkpoint: str = SMOLLM_CHECKPOINT, checkpoint_revision: str = SMOLLM_REVISION,
                   iterations: int = 15, max_linear_layers: int = 4,
                   scale_format: str = "bf16", eval_bytes: int = 4096,
                   checkpoint_path: Path | None = None) -> dict:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    torch.manual_seed(seed)
    tokens, data = load_public_text(dataset_dir, eval_bytes, eval_bytes)
    source, source_args, checkpoint_hashes = checkpoint_source(checkpoint, checkpoint_revision, checkpoint_path)
    tokenizer = AutoTokenizer.from_pretrained(source, **source_args)
    model = AutoModelForCausalLM.from_pretrained(source, **source_args,
                                                torch_dtype=torch.float32).to(device).eval()
    ids = {s: tokenizer(bytes(tokens[s].tolist()).decode("utf-8", errors="replace"),
                        return_tensors="pt", add_special_tokens=False).input_ids
           for s in ("validation", "test")}
    original = {s: hf_nll(model, ids[s]) for s in ids}
    selected = [(name, module) for name, module in model.named_modules()
                if isinstance(module, nn.Linear) and name != "lm_head"]
    if max_linear_layers > 0:
        selected = selected[:max_linear_layers]
    if not selected:
        raise ValueError("checkpoint contains no supported nn.Linear module")
    module_names, weight_errors, histories = [], {"rtn": [], "dual": []}, []
    saved = []
    for name, linear in selected:
        parent_path, child = name.rsplit(".", 1) if "." in name else ("", name)
        parent = model.get_submodule(parent_path)
        rtn = DualQuantLinear(linear, iterations=iterations, scale_format=scale_format, dual=False)
        dual = DualQuantLinear(linear, iterations=iterations, scale_format=scale_format, dual=True)
        module_names.append(name)
        weight_errors["rtn"].append(rtn.weight_mse())
        weight_errors["dual"].append(dual.weight_mse())
        histories.extend(h for _, _, _, h in dual.tiles)
        saved.append((parent, child, rtn, dual))
    for parent, child, rtn, _ in saved:
        setattr(parent, child, rtn)
    rtn_scores = {s: hf_nll(model, ids[s]) for s in ids}
    for parent, child, _, dual in saved:
        setattr(parent, child, dual)
    dual_scores = {s: hf_nll(model, ids[s]) for s in ids}
    return {"paper": {"key": "dualquant"}, "seed": seed, "dataset": data,
            "checkpoint": {"name": checkpoint, "revision": checkpoint_revision,
                           "offline_source_verification": checkpoint_hashes},
            "evaluation_tier": "L1", "fidelity": "core_mechanism", "diagnostic_only": True,
            "baseline": {"name": "single-scale INT4 W+A reference", "test_nll": rtn_scores["test"]},
            "method": {"name": "weight-only BCD dual-scale W+A reference", "test_nll": dual_scores["test"]},
            "full_precision": original, "validation": {"rtn": rtn_scores["validation"],
                                                          "dual": dual_scores["validation"]},
            "weight_mse_per_module": weight_errors,
            "stages": {"calibration_examples": 0, "activation_quantization": True,
                       "weight_only_scale_optimization": True, "iterations": iterations,
                       "group_size": 32, "tile_rows": 128, "scale_format": scale_format,
                       "quantized_modules": module_names, "quantized_module_count": len(module_names),
                       "supported_formats": ["INT4/BF16-scales", "MXINT4/E8M0-scales"],
                       "native_fp4_or_int4_acceleration": False,
                       "tile_objective_first_last": [[h[0], h[-1]] for h in histories]},
            "scope": "公开 checkpoint 上指定线性层的 W4A4 software simulation；不声称全模型量化、低位存储或 A100 原生 FP4 加速。"}


def reproduce_msar(dataset_dir: Path, seed: int = 42):
    return run_foundation_training("msar", dataset_dir, seed)


def reproduce_orthros(dataset_dir: Path, seed: int = 42):
    return run_foundation_training("orthros", dataset_dir, seed)


def reproduce_dualquant(dataset_dir: Path, seed: int = 42):
    return run_dualquant(dataset_dir, seed)


def reproduce_woven(dataset_dir: Path, seed: int = 42):
    from auto_research.multimodal.oct12_reward_transition import run_woven
    return run_woven(dataset_dir, seed)


def reproduce_umrm(dataset_dir: Path, seed: int = 42):
    from auto_research.multimodal.oct12_reward_transition import run_umrm
    return run_umrm(dataset_dir, seed)


def render(result: dict) -> str:
    return "\n".join([f"# {result['paper']['key']} 公开数据机制诊断", "",
                      "L1 / core_mechanism / diagnostic_only=true。单 seed 不支持稳定提升结论。", "",
                      "## 本地结果", "", "```json",
                      json.dumps({"baseline": result["baseline"], "method": result["method"]},
                                 ensure_ascii=False, indent=2), "```", "",
                      "## 复现边界", "", result["scope"], ""])
