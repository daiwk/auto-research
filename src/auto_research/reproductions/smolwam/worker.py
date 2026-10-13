"""Execute real SmolWAM 0.88B checkpoint in closed-loop LIBERO, offline."""
from __future__ import annotations
import argparse
from collections import deque
import json
import os
from pathlib import Path
import sys
import time

from ..lewam.external import PINS, verify_provenance, verify_source, verify_trained_candidate
from .algorithm import assert_release


def load_initial_states(libero_root: Path, task):
    """Verified LIBERO NumPy states with weights-only, narrowly scoped globals."""
    import importlib
    import numpy as np
    import pickle
    import torch
    relative = Path("libero/libero/init_files") / task.problem_folder / task.init_states_file
    path = (libero_root / relative).resolve()
    if not path.is_relative_to(libero_root.resolve()):
        raise ValueError("initial states must stay inside verified LIBERO resources")
    # The worker has verified the complete mirror before this function. Recheck
    # this exact input against its public byte manifest before deserialization.
    if not (libero_root / ".git").exists():
        verify_provenance(libero_root, "Lifelong-Robot-Learning/LIBERO", PINS["libero"],
                          (relative.as_posix(),))
    else:
        verify_source(libero_root, "libero")
    # NumPy 1.26 exposes a partial np._core compatibility shim without
    # multiarray; importing the concrete module also works on NumPy 2.x.
    reconstruct = importlib.import_module("numpy.core.multiarray")._reconstruct
    allowed = [(reconstruct, "numpy.core.multiarray._reconstruct"),
               (reconstruct, "numpy._core.multiarray._reconstruct"), np.ndarray, np.dtype,
               np.dtypes.Float32DType, np.dtypes.Float64DType]
    existing = set(torch.serialization.get_safe_globals())
    additions = [value for value in allowed if value not in existing]
    try:
        with torch.serialization.safe_globals(additions):
            states = np.asarray(torch.load(path, map_location="cpu", weights_only=True))
    except pickle.UnpicklingError as exc:
        raise ValueError("LIBERO initial states use unsupported pickle globals") from exc
    if states.ndim != 2 or not all(states.shape) or not np.issubdtype(states.dtype, np.number) or not np.isfinite(states).all():
        raise ValueError("finite nonempty numeric LIBERO initial states required")
    return states


def run(config):
    if config.get("phase") == "train":
        from .training import train
        return train(config)
    if "trained_model_dir" in config and config.get("tasks") != ["libero_goal:6"]:
        raise ValueError("this bounded trained student requires explicit same-training-task libero_goal:6")
    import numpy as np
    import torch
    from smolwam import SmolWAM
    from smolwam.envs.libero import (NUM_STEPS_WAIT, TASK_MAX_STEPS, benchmark_suite,
        dummy_action, make_env, policy_observation, seed_everything)
    model_dir, vae_dir = Path(config["model_dir"]), Path(config["vae_dir"])
    model_provenance = verify_provenance(model_dir, "timiiowolabi/SmolWAM",
        "c269c6e3a9c113b2b04187daf977c09486e2eadc",
        ("config.json", "model.safetensors", "text_cache.safetensors"))
    vae_provenance = verify_provenance(vae_dir, "Wan-AI/Wan2.1-T2V-1.3B",
        "37ec512624d61f7aa208f7ea8140a131f93afc9a", ("Wan2.1_VAE.pth",))
    assert_release(json.loads((model_dir / "config.json").read_text()))
    libero_root = Path(config["libero_root"]).resolve()
    verify_source(libero_root, "libero")
    sys.path.insert(0, str(libero_root))
    for directory in ("assets", "bddl_files", "init_files"):
        if not (libero_root / "libero/libero" / directory).is_dir():
            raise FileNotFoundError(f"offline LIBERO {directory} is required")
    paths = {"benchmark_root": libero_root / "libero/libero",
             "bddl_files": libero_root / "libero/libero/bddl_files",
             "init_states": libero_root / "libero/libero/init_files",
             "assets": libero_root / "libero/libero/assets", "datasets": libero_root / "libero/datasets"}
    cfg_dir = Path(config["result_path"]).parent / "libero-config"
    cfg_dir.mkdir()
    (cfg_dir / "config.yaml").write_text("".join(f"{key}: {path}\n" for key, path in paths.items()))
    os.environ["LIBERO_CONFIG_PATH"] = str(cfg_dir)
    os.environ["SMOLWAM_WAN_VAE"] = str(vae_dir / "Wan2.1_VAE.pth")
    device = config.get("device", "cuda")
    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable; no CPU substitution")
    policy = SmolWAM.from_pretrained(model_dir, device=device, dtype="bf16" if device.startswith("cuda") else "fp32")
    candidate = None
    if "trained_model_dir" in config:
        from smolwam.config import SmolWAMConfig
        from smolwam.policy import load_model
        trained_dir = Path(config["trained_model_dir"])
        candidate = verify_trained_candidate(trained_dir, "smolwam", config["seed"], ("best.pt",))
        checkpoint = torch.load(trained_dir / "best.pt", map_location="cpu", weights_only=True)
        trained_cfg = SmolWAMConfig.from_dict(checkpoint["config"])
        assert_release({"model": trained_cfg.to_dict()})
        # Keep the same verified VAE/text/normalization; replace all student weights,
        # including its frozen adapters, with the actual native selected state.
        policy.model = load_model(trained_cfg, checkpoint["model"], device, policy.dtype)
        policy.config = policy.model.cfg
    variants, latencies = {"smolwam": [], "noop": []}, []
    for task_spec in config.get("tasks", ["libero_10:2"]):
        suite_name, task_id = task_spec.split(":")
        suite = benchmark_suite(suite_name)
        task = suite.get_task(int(task_id))
        initial_states = load_initial_states(libero_root, task)
        for trial in range(config.get("trials", 2)):
            initial_id = (config["seed"] + trial) % len(initial_states)
            for variant in ("smolwam", "noop"):
                env, instruction = make_env(task)
                seed_everything(config["seed"])
                env.reset()
                obs = env.set_init_state(initial_states[initial_id])
                queue, steps, success, calls = deque(), 0, False, 0
                limit = config.get("action_budget", TASK_MAX_STEPS[suite_name])
                start = time.perf_counter()
                try:
                    for _ in range(NUM_STEPS_WAIT):
                        obs, _, _, _ = env.step(dummy_action())
                    while steps < limit:
                        if not queue:
                            if variant == "smolwam":
                                seed_everything(0)  # original deterministic per-query fixed-noise convention
                                observation = policy_observation(obs)
                                actions, future = policy.predict_action(observation, instruction, return_future=True)
                                if actions.shape != (16, 7) or tuple(future.shape) != (2, 16, 28, 28):
                                    raise ValueError("actual action/world output contract violated")
                                if not np.isfinite(actions).all() or not torch.isfinite(future).all():
                                    raise ValueError("nonfinite policy output")
                                queue.extend(actions)
                                latencies.append(policy.last_timing["total"])
                                calls += 1
                            else:
                                queue.extend([dummy_action()] * 16)
                        obs, _, done, _ = env.step(np.asarray(queue.popleft(), dtype=np.float64).tolist())
                        steps += 1
                        if done:
                            success = True
                            break
                finally:
                    env.close()
                variants[variant].append({"task": task_spec, "initial_state_id": initial_id,
                    "success": success, "actions_executed": steps, "policy_queries": calls,
                    "wall_seconds": time.perf_counter() - start})
    summary = {name: {"success_rate": float(np.mean([x["success"] for x in rows])),
                       "episodes": len(rows), "actions_executed": sum(x["actions_executed"] for x in rows)}
               for name, rows in variants.items()}
    return {"paper": "smolwam", "seed": config["seed"], "executed": True, "device": device,
            "source_revision": PINS["smolwam"], "checkpoint": model_provenance, "vae": vae_provenance,
            "trained_candidate": candidate,
            "dataset": {"public_id": "Lifelong-Robot-Learning/LIBERO", "revision": PINS["libero"],
                        "resources": ["libero/libero/assets", "libero/libero/bddl_files", "libero/libero/init_files"]},
            "variants": summary, "episodes": variants,
            "latency_seconds_mean": float(np.mean(latencies)),
            "evaluation_tier": "l2_public_dataset", "fidelity": "core_mechanism",
            "diagnostic_only": candidate is not None, "promotion_eligible": False,
            "protocol": {"tasks": config.get("tasks", ["libero_10:2"]), "trials": config.get("trials", 2),
                         "chunk_actions": 16, "initial_wait_actions": NUM_STEPS_WAIT,
                         "nonofficial_benchmark": True, "world_head_executed": True,
                         "teacher_distillation_retrained": candidate is not None,
                         "layout_curriculum_retrained": candidate is not None,
                         "new_student_closed_loop_evaluated": candidate is not None},
            "limitations": ["bounded LIBERO task/init-state subset; not paper's 400 episodes",
                            "actual world latents executed but not scored against true future",
                            "no teacher latency/success comparison; trained candidate remains a bounded diagnostic",
                            "weights: NVIDIA One-Way Noncommercial License; code: Apache-2.0"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.request.read_text())
    Path(config["result_path"]).write_text(json.dumps(run(config), ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
