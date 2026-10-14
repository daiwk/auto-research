"""Execute native visual JEPA + action flow + SIGReg training, bounded batches."""
from __future__ import annotations
import importlib.util
import os
from pathlib import Path

from .external import PINS, record_trained_candidate, verify_provenance


def train(config):
    import torch
    from hydra import compose, initialize_config_dir
    source = Path(config["source_root"]).resolve()
    data_dir = Path(config["data_dir"])
    dataset = verify_provenance(data_dir, "LeWAM/lewam-toolhang",
        "465df45efe1b87aead4f423d3f8670833c5ddaf4", ("toolhang.h5",))
    if not torch.cuda.is_available() or config.get("device", "cuda") != "cuda":
        raise RuntimeError("native LeWAM training receipt requires actual CUDA")
    run_dir = Path(config["result_path"]).parent / "native-training"
    os.environ["STABLEWM_HOME"] = str(Path(config["result_path"]).parent / "native-home")
    steps = config.get("train_steps_per_epoch", 4)
    epochs = config.get("train_epochs", 1)
    if steps < 0 or epochs < 1:
        raise ValueError("nonnegative batch cap (0=full native pass) and positive epochs required")
    overrides = [f"seed={config['seed']}", f"dataset_path={data_dir / 'toolhang.h5'}",
        "run_name=bounded-toolhang", f"run_dir={run_dir}", "resume=false", "data.source=h5",
        "data.load_in_ram=false", "data.num_workers=0", f"train.epochs={epochs}",
        "train.warmup_epochs=1", f"train.steps_per_epoch={steps}",
        f"train.batch_size={config.get('train_batch_size', 8)}", "train.w_act=1.0",
        "train.w_dyn=1.0", "train.w_reg=0.04", "model.action_head=flow", "model.state_head=mse"]
    with initialize_config_dir(version_base="1.3", config_dir=str(source / "configs/train")):
        cfg = compose(config_name="gr", overrides=overrides)
    spec = importlib.util.spec_from_file_location("lewam_native_training", source / "scripts/train_lewam.py")
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    builder, run_batch, optimizer_step = native.build_model, native.run_batch, torch.optim.AdamW.step
    models, before, batches, gradients = [], {}, [], []

    def tracked_builder(*args, **kwargs):
        model = builder(*args, **kwargs)
        models.append(model)
        before.update({name: param.detach().reshape(-1)[:32].cpu().clone()
                       for name, param in model.named_parameters() if param.requires_grad})
        return model

    def tracked_batch(*args, **kwargs):
        output = run_batch(*args, **kwargs)
        training = kwargs.get("train", args[-1] if args else False)
        batches.append({"training": bool(training), "loss": float(output[0].detach()), **output[1]})
        return output

    def tracked_step(optimizer, *args, **kwargs):
        norm_sq = sum(float(p.grad.detach().float().square().sum())
                      for group in optimizer.param_groups for p in group["params"] if p.grad is not None)
        gradients.append(norm_sq ** 0.5)
        return optimizer_step(optimizer, *args, **kwargs)

    native.build_model, native.run_batch, torch.optim.AdamW.step = tracked_builder, tracked_batch, tracked_step
    try:
        native.main.__wrapped__(cfg)
    finally:
        native.build_model, native.run_batch, torch.optim.AdamW.step = builder, run_batch, optimizer_step
    model = models[-1]
    changes = {name: float((param.detach().reshape(-1)[:32].cpu() - before[name]).square().sum())
               for name, param in model.named_parameters() if name in before}
    train_batches = [batch for batch in batches if batch["training"]]
    validation = [batch for batch in batches if not batch["training"]]
    if not train_batches or not validation or sum(changes.values()) <= 0 or max(gradients, default=0) <= 0:
        raise RuntimeError("native training did not prove real updates and validation")
    if not all(all(key in batch for key in ("act", "state", "reg")) for batch in train_batches):
        raise RuntimeError("all three defining LeWAM losses must actually execute")
    if not (run_dir / "lewam_best.pt").is_file():
        raise RuntimeError("validation-selected native checkpoint missing")
    metric = {"optimizer_updates": len(gradients), "nonzero_gradient_updates": sum(g > 0 for g in gradients),
              "parameter_sample_delta_l2": sum(changes.values()) ** 0.5,
              "updated_parameter_tensors": sum(change > 0 for change in changes.values()),
              "train_batches": len(train_batches), "validation_batches": len(validation),
              "validation_action_loss": sum(row["act"] for row in validation) / len(validation),
              "train_action_loss": sum(row["act"] for row in train_batches) / len(train_batches),
              "train_latent_loss": sum(row["state"] for row in train_batches) / len(train_batches),
              "train_sigreg_loss": sum(row["reg"] for row in train_batches) / len(train_batches)}
    candidate = record_trained_candidate(run_dir, "lewam", config["seed"],
        ("lewam_best.pt", "lewam_config.json"), dataset, metric, {"batches": batches, "gradients": gradients})
    return {"paper": "lewam", "phase": "train", "seed": config["seed"], "executed": True,
            "source_revision": PINS["lewam"], "device": "cuda", "dataset": dataset,
            "variants": {"joint_training": metric}, "batches": batches, "trained_candidate": candidate,
            "evaluation_tier": "l2_public_dataset", "fidelity": "core_mechanism",
            "diagnostic_only": True, "promotion_eligible": False,
            "protocol": {"native_training_api": "scripts/train_lewam.py:main.__wrapped__",
                         "epochs": epochs, "steps_per_epoch": steps,
                         "batch_size": config.get("train_batch_size", 8),
                         "train_validation": "native random valid decision-point split; no held-out test claim",
                         "checkpoint_selection": "validation action flow loss only",
                         "action_flow_latent_prediction_sigreg_executed": True,
                         "trained_candidate_closed_loop_evaluated": False},
            "limitations": ["真实联合训练，但epoch/batch预算缩小；无正式能力对照或未见轨迹test",
                            "发布策略控制和新训练candidate控制是不同实验；不自动宣称full_pipeline"]}
