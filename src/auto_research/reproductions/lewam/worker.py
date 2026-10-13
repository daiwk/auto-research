"""Execute actual author LeWAM encoder/MoT/policy/planner and ToolHang env."""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time

from .external import PINS, verify_provenance


def _jsonable(value):
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(x) for x in value]
    if hasattr(value, "tolist"):
        return value.tolist()
    return value


def run(config):
    if config.get("phase") == "train":
        from .training import train
        return train(config)
    import torch
    import stable_worldmodel as swm
    import stable_worldmodel.data.formats.hdf5  # noqa: F401
    from hydra import compose, initialize_config_dir
    from omegaconf import OmegaConf
    from lewam.eval.episodes import get_dataset, img_transform, sample_eval_episodes
    from lewam.eval.build import build_policy
    from lewam.models.lewam import build_model
    source = Path(config["source_root"]).resolve()
    model_dir, data_dir = Path(config["model_dir"]), Path(config["data_dir"])
    model_provenance = verify_provenance(model_dir, "LeWAM/lewam-toolhang",
        "39512799122797828f13c29071d3d797852ce9b5", ("lewam_best.pt", "lewam_config.json"))
    data_provenance = verify_provenance(data_dir, "LeWAM/lewam-toolhang",
        "465df45efe1b87aead4f423d3f8670833c5ddaf4", ("toolhang.h5",))
    device = config.get("device", "cuda")
    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA required by this run; no CPU substitution")
    torch.manual_seed(config["seed"])
    model_cfg = json.loads((model_dir / "lewam_config.json").read_text())
    if model_cfg.get("action_head") != "flow" or model_cfg.get("goal_type") == "none":
        raise ValueError("released goal-conditioned flow checkpoint required")
    model_cfg.setdefault("action_dim", int(model_cfg["fs"]) * int(model_cfg["action_raw_dim"]))
    model = build_model(model_cfg)
    model.load_state_dict(torch.load(model_dir / "lewam_best.pt", map_location="cpu", weights_only=True))
    model = model.to(device).eval().requires_grad_(False)
    spec = importlib.util.spec_from_file_location("lewam_author_eval", source / "scripts/eval_lewam.py")
    author = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    variants, starts_receipt = {}, None
    with tempfile.TemporaryDirectory(prefix="lewam-offline-") as temporary:
        home = Path(temporary)
        (home / "datasets").mkdir()
        (home / "datasets/toolhang.h5").symlink_to((data_dir / "toolhang.h5").resolve())
        os.environ["STABLEWM_HOME"] = str(home)
        for variant in config.get("variants", ["reactive", "best_of_k", "grad"]):
            if variant not in {"reactive", "best_of_k", "grad"}:
                raise ValueError("unknown LeWAM comparison variant")
            overrides = [f"seed={config['seed']}", "policy=offline-fixed",
                         f"eval.num_eval={config.get('episodes', 2)}",
                         f"eval.goal_offset_steps={config.get('goal_offset', 50)}",
                         f"eval.eval_budget={config.get('action_budget', 100)}",
                         f"eval.num_proposals={config.get('proposals', 4)}",
                         f"eval.grad_steps={config.get('gradient_steps', 5)}", "eval.grad_tr=0.01",
                         "eval.mode=" + ("lewam_policy" if variant == "reactive" else "lewam_plan")]
            if variant != "reactive":
                overrides.append("eval.plan_mode=" + variant)
            with initialize_config_dir(version_base="1.3", config_dir=str(source / "configs/eval")):
                cfg = compose(config_name="toolhang", overrides=overrides)
            cfg.world.env_meta = str(source / cfg.world.env_meta)
            cfg.world.max_episode_steps = 2 * cfg.eval.eval_budget
            author.register_env(cfg.world.env_name)
            dataset = get_dataset("toolhang", list(cfg.dataset.keys_to_cache), str(home))
            episodes, starts, offsets = sample_eval_episodes(dataset, cfg.eval.num_eval,
                config["seed"], cfg.eval.goal_offset_steps)
            starts_receipt = {"episodes": episodes, "starts": starts,
                              "goal_offset": cfg.eval.goal_offset_steps}
            transform = {"pixels": img_transform(cfg.eval.img_size), "goal": img_transform(cfg.eval.img_size)}
            policy = build_policy(cfg.eval, model, model_cfg, config["seed"], transform, offsets)
            world = swm.World(**cfg.world, image_shape=(224, 224))
            world.set_policy(policy)
            beginning = time.perf_counter()
            try:
                metric = world.evaluate(dataset=dataset, start_steps=starts,
                    goal_offset=cfg.eval.goal_offset_steps, eval_budget=cfg.eval.eval_budget,
                    episodes_idx=episodes, callables=OmegaConf.to_container(cfg.eval.callables, resolve=True),
                    video=False)
            finally:
                if hasattr(world, "close"):
                    world.close()
            variants[variant] = {"metrics": _jsonable(metric), "wall_seconds": time.perf_counter() - beginning}
    return {"paper": "lewam", "seed": config["seed"], "executed": True, "device": device,
            "source_revision": PINS["lewam"], "checkpoint": model_provenance, "dataset": data_provenance,
            "variants": variants, "sampled_starts": starts_receipt,
            "evaluation_tier": "l2_public_dataset", "fidelity": "core_mechanism",
            "diagnostic_only": True, "promotion_eligible": False,
            "protocol": {"non_holdout": True, "goal_from_training_episodes": True,
                         "paper_training_reexecuted": False, "public_checkpoint_executed": True,
                         "proposals": config.get("proposals", 4), "gradient_steps": config.get("gradient_steps", 5),
                         "episodes": config.get("episodes", 2)},
            "limitations": ["原公开checkpoint训练集目标协议，不能视为test隔离比较",
                            "原论文50epoch训练未重执行；候选数/规划更新/episode数缩小"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.request.read_text())
    result = run(config)
    Path(config["result_path"]).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
