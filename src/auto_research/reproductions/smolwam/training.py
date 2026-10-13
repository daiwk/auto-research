"""Offline native Cosmos-teacher KD and 1764→1008 token layout curriculum.

The author source remains untouched. Instrumentation checks actual gradients,
weights and losses; one transparent bounded-data override covers every bank row
with real teacher targets, including validation, to avoid the upstream one-task
KD filtering pitfall. No random/fabricated KD target is permitted.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

from ..lewam.external import PINS, record_trained_candidate, verify_provenance
from .algorithm import RELEASED_BLOCKS

TEACHER_REVISION = "cb689ec0e3347c13667d70a78a3447388f5c3bb8"
DEMO_REVISION = "b463cbd5d114909e4daea65eb03bed9787290042"
DEMO_FILE = "success_only/libero_goal_regen/put_the_cream_cheese_in_the_bowl_demo.hdf5"
STATS_FILE = "success_only/dataset_statistics.json"


def _cli(module, arguments):
    previous = sys.argv
    sys.argv = [module.__name__, *map(str, arguments)]
    try:
        module.main()
    finally:
        sys.argv = previous


def train(config):
    import numpy as np
    import torch
    import smolwam.teacher as teacher
    import smolwam.train.bank as bank_module
    import smolwam.train.kd_targets as kd_module
    import smolwam.train.train as train_module
    from smolwam.config import SmolWAMConfig
    from smolwam.train.data import BankDataset
    teacher_dir, data_dir = Path(config["teacher_dir"]), Path(config["training_data_dir"])
    release_dir, vae_dir = Path(config["model_dir"]), Path(config["vae_dir"])
    teacher_resource = verify_provenance(teacher_dir, teacher.TEACHER_REPO, TEACHER_REVISION,
        (teacher.TEACHER_CHECKPOINT, teacher.TEACHER_T5, teacher.TEACHER_STATS))
    dataset = verify_provenance(data_dir, "nvidia/LIBERO-Cosmos-Policy", DEMO_REVISION,
                                (DEMO_FILE, STATS_FILE))
    release = verify_provenance(release_dir, "timiiowolabi/SmolWAM",
        "c269c6e3a9c113b2b04187daf977c09486e2eadc",
        ("model.safetensors", "config.json", "text_cache.safetensors"))
    verify_provenance(vae_dir, "Wan-AI/Wan2.1-T2V-1.3B",
        "37ec512624d61f7aa208f7ea8140a131f93afc9a", ("Wan2.1_VAE.pth",))
    if not torch.cuda.is_available() or config.get("device", "cuda") != "cuda":
        raise RuntimeError("actual CUDA required; no CPU or random teacher substitution")
    import os
    os.environ["SMOLWAM_WAN_VAE"] = str(vae_dir / "Wan2.1_VAE.pth")
    run_root = Path(config["result_path"]).parent / "native-training"
    run_root.mkdir()
    bank, kd, run = run_root / "bank", run_root / "kd", run_root / "student"
    stats, adapter = data_dir / STATS_FILE, release_dir / "model.safetensors"
    original_teacher_file = teacher.teacher_file
    original_episodes = bank_module.list_episodes
    original_dataset = kd_module.BankDataset

    def local_teacher_file(filename):
        if filename not in {teacher.TEACHER_CHECKPOINT, teacher.TEACHER_T5, teacher.TEACHER_STATS}:
            raise ValueError("teacher requested an unverified offline resource")
        return teacher_dir / filename

    def bounded_episodes(*args, **kwargs):
        verified_file = (data_dir / DEMO_FILE).resolve()
        episodes = [episode for episode in original_episodes(*args, **kwargs)
                    if Path(episode["file"]).resolve() == verified_file]
        return episodes[:config.get("training_episodes", 8)]

    class AllRowsForTeacher(BankDataset):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Native val_frac=0 still drops one episode. At bounded scale it
            # would remove all student validation KD rows. Teacher inference
            # is label-free wrt split selection, so cache targets for all rows.
            self.rows = np.arange(self.meta["num_rows"], dtype=np.int64)

    teacher.teacher_file, bank_module.list_episodes = local_teacher_file, bounded_episodes
    kd_module.BankDataset = AllRowsForTeacher
    try:
        _cli(bank_module, ["--data", data_dir / "success_only", "--out", bank,
                           "--stride", 4, "--batch", config.get("bank_batch_size", 2),
                           "--workers", 0, "--device", "cuda"])
        _cli(kd_module, ["--bank", bank, "--adapter", adapter, "--stats", stats,
                         "--out", kd, "--bs", config.get("teacher_batch_size", 1),
                         "--workers", 0, "--device", "cuda"])
        kd_meta = json.loads((kd / "meta.json").read_text())
        meta = json.loads((bank / "meta.json").read_text())
        if kd_meta["n"] != meta["num_rows"]:
            raise RuntimeError("actual teacher targets must cover every bounded bank row")
        steps = config.get("training_steps", 8)
        fraction = config.get("curriculum_fraction", 0.25)
        switch = int(steps * fraction)
        if steps < 4 or not 1 < switch < steps:
            raise ValueError("both layouts need actual nonzero-lr updates; use e.g. 8 steps and fraction .25")
        arguments = train_module.parser().parse_args(list(map(str, [
            "--run", run, "--bank", bank, "--kd", kd, "--text_cache", release_dir / "text_cache.safetensors",
            "--adapter", adapter, "--stats", stats, "--init", "teacher", "--steps", steps,
            "--curriculum_frac", fraction, "--bs", config.get("training_batch_size", 1),
            "--workers", 0, "--max_rows", config.get("max_training_rows", 32), "--warmup", 1,
            "--val_every", 1, "--save_every", steps, "--device", "cuda", "--seed", config["seed"]])))
        native_builder, native_losses, native_step = train_module.build_model, train_module.compute_losses, torch.optim.AdamW.step
        models, before, losses, gradients = [], {}, [], []

        def tracked_builder(*args, **kwargs):
            model = native_builder(*args, **kwargs)
            models.append(model)
            before.update({name: p.detach().reshape(-1)[:32].cpu().clone()
                           for name, p in model.named_parameters() if p.requires_grad})
            return model

        def tracked_losses(*args, **kwargs):
            total, terms = native_losses(*args, **kwargs)
            model = models[-1]
            losses.append({"training": model.training, "tokens": model.num_tokens(),
                           **{name: float(value.detach()) for name, value in terms.items()}})
            return total, terms

        def tracked_step(optimizer, *args, **kwargs):
            samples_before = [p.detach().reshape(-1)[:32].clone()
                              for group in optimizer.param_groups for p in group["params"]]
            norm_sq = sum(float(p.grad.detach().float().square().sum())
                          for group in optimizer.param_groups for p in group["params"] if p.grad is not None)
            result = native_step(optimizer, *args, **kwargs)
            after = [p.detach().reshape(-1)[:32] for group in optimizer.param_groups for p in group["params"]]
            delta = sum(float((a - b).float().square().sum())
                        for a, b in zip(after, samples_before, strict=True)) ** 0.5
            gradients.append({"tokens": models[-1].num_tokens(), "norm": norm_sq ** 0.5,
                              "parameter_sample_delta_l2": delta})
            return result

        train_module.build_model, train_module.compute_losses = tracked_builder, tracked_losses
        torch.optim.AdamW.step = tracked_step
        try:
            best_val = train_module.train(arguments, SmolWAMConfig(trunk_blocks=RELEASED_BLOCKS))
        finally:
            train_module.build_model, train_module.compute_losses = native_builder, native_losses
            torch.optim.AdamW.step = native_step
        model = models[-1]
        changes = {name: float((p.detach().reshape(-1)[:32].cpu() - before[name]).square().sum())
                   for name, p in model.named_parameters() if name in before}
        trained = [row for row in losses if row["training"]]
        if {row["tokens"] for row in trained} != {1764, 1008}:
            raise RuntimeError("both actual teacher and compact layouts must execute")
        if {row["tokens"] for row in gradients if row["norm"] > 0 and row["parameter_sample_delta_l2"] > 0} != {1764, 1008}:
            raise RuntimeError("both layouts must prove actual nonzero-gradient parameter updates")
        if not any(not row["training"] and row["tokens"] == 1008 for row in losses):
            raise RuntimeError("nonempty actual compact-layout validation required")
        if not all(all(key in row for key in ("action_l1", "world_l1", "kd_act_l1", "kd_world_l1")) for row in trained):
            raise RuntimeError("all four actual demonstration/teacher action/future losses required")
        if sum(changes.values()) <= 0 or not (run / "best.pt").is_file() or not np.isfinite(best_val):
            raise RuntimeError("real parameter changes and validation-selected compact checkpoint required")
        metric = {"optimizer_updates": len(gradients), "teacher_layout_updates": sum(g["tokens"] == 1764 for g in gradients),
                  "compact_layout_updates": sum(g["tokens"] == 1008 for g in gradients),
                  "nonzero_parameter_updates": sum(g["parameter_sample_delta_l2"] > 0 for g in gradients),
                  "nonzero_gradient_updates": sum(g["norm"] > 0 for g in gradients),
                  "parameter_sample_delta_l2": sum(changes.values()) ** 0.5,
                  "updated_parameter_tensors": sum(v > 0 for v in changes.values()),
                  "best_validation_action_l1": float(best_val),
                  "real_teacher_target_rows": kd_meta["n"],
                  "teacher_vs_demo_action_l1": kd_meta["teacher_vs_demo_action_l1"]}
        for key in ("action_l1", "world_l1", "kd_act_l1", "kd_world_l1"):
            metric["train_mean_" + key] = float(np.mean([row[key] for row in trained]))
        candidate = record_trained_candidate(run, "smolwam", config["seed"], ("best.pt",), dataset, metric,
                                             {"losses": losses, "gradients": gradients})
        return {"paper": "smolwam", "phase": "train", "seed": config["seed"], "executed": True,
                "source_revision": PINS["smolwam"], "device": "cuda", "dataset": dataset,
                "teacher": teacher_resource, "pretrained_adapter_text": release,
                "variants": {"distillation_training": metric}, "losses": losses, "gradients": gradients,
                "trained_candidate": candidate,
                "evaluation_tier": "l2_public_dataset", "fidelity": "core_mechanism",
                "diagnostic_only": True, "promotion_eligible": False,
                "protocol": {"teacher_targets_actual_model": True, "teacher_targets_cover_validation": True,
                    "original_source_unchanged": True, "native_apis": ["smolwam.train.bank:main",
                        "smolwam.train.kd_targets:main", "smolwam.train.train:train"],
                    "episodes": meta["num_episodes"], "rows": meta["num_rows"], "steps": steps,
                    "layout_switch_step": switch, "checkpoint_selection": "compact-layout validation action L1 only",
                    "latent_adapter_retrained": False, "bert_text_cache_rebuilt": False,
                    "new_student_closed_loop_evaluated": False},
                "limitations": ["单任务、前8演示、8步课程是训练机制诊断，不是原68,830row/5000step效果复现",
                    "复用已发布latentadapter与BERTtext；未重新训练单帧/clip映射",
                    "teacher缓存全row覆盖是显式boundeddata适配，未篡改upstream pin",
                    "本阶段不自动将新student用于LIBERO能力比较"]}
    finally:
        teacher.teacher_file, bank_module.list_episodes = original_teacher_file, original_episodes
        kd_module.BankDataset = original_dataset
