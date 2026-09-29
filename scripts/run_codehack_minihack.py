"""Real MiniHack/CodeHack integration smoke, not the paper's LLM/RL benchmark.

Install the pinned upstream CodeHack and its custom NLE build separately.
This runner uses a seeded uniform action policy to verify primitive, skill and
mixed action spaces against an actual MiniHack episode. It never reads a task
solution or claims the original paper's zero-shot/online results.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random


UPSTREAM_CODEHACK_COMMIT = "3026cdb7378726eace9efe8ab655f1aee616844f"
UPSTREAM_BASELINES_COMMIT = "ba2c532bd505426913b82291adec455afd855df5"
UPSTREAM_NLE_WHEEL_SHA256 = "819063e40b3c1bc97e946695242b7cfe0633d61049ac44cfde53d72447948513"
SKILL_NAMES = ("explore_room", "goto_room", "open_doors", "fight_melee")
PRIMITIVE_NAMES = ("north", "south", "east", "west", "wait", "more")
OBSERVATION_KEYS = (
    "message", "blstats", "tty_chars", "tty_colors", "tty_cursor",
    "glyphs", "inv_glyphs", "inv_strs", "inv_letters", "inv_oclasses",
)


def mode_actions(mode: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if mode not in {"primitives", "skills", "mixed"}:
        raise ValueError("mode must be primitives, skills or mixed")
    return (
        SKILL_NAMES if mode != "primitives" else (),
        PRIMITIVE_NAMES if mode != "skills" else (),
    )


def run_episode(mode: str, seed: int, *, max_decisions: int, primitive_budget: int) -> dict:
    if max_decisions < 1 or primitive_budget < 1:
        raise ValueError("episode budgets must be positive")
    import gymnasium as gym
    import minihack  # noqa: F401 - registers the public MiniHack task
    from nle import nethack
    from nle_utils.wrappers import AutoMore

    from codehack.bot.panics import enemy_appeared, lost_hp
    from codehack.bot.strategies import explore_room, fight_melee, goto_room, open_doors
    from codehack.wrappers import CodeHackWrapper

    skills, primitives = mode_actions(mode)
    functions = {func.__name__: func for func in (explore_room, goto_room, open_doors, fight_melee)}
    base = gym.make(
        "MiniHack-Room-5x5-v0", observation_keys=OBSERVATION_KEYS,
        actions=nethack.ACTIONS,
    )
    # Gymnasium 1.0 no longer forwards arbitrary wrapper attributes. The
    # upstream CodeHack/NLE-utils pair still expects ``env.actions``; expose
    # the underlying public action tuple on the two local wrappers only.
    base.actions = base.unwrapped.actions
    env = AutoMore(base)
    env.actions = base.actions
    env = CodeHackWrapper(
        env, strategies=[functions[name] for name in skills],
        panics=[enemy_appeared, lost_hp], primitives=list(primitives),
        max_strategy_steps=primitive_budget,
    )
    rng = random.Random(seed)
    try:
        _, info = env.reset(seed=seed)
        available = tuple(env.action_space.strategy_names)
        if not available:
            raise RuntimeError("CodeHack exposed no actions")
        decisions = 0
        reward = 0.0
        terminated = truncated = False
        error = None
        while decisions < max_decisions:
            action = rng.choice(available)
            try:
                _, step_reward, terminated, truncated, info = env.step(action)
            except Exception as exc:  # upstream game/skill failures remain visible
                error = f"{type(exc).__name__}: {exc}"
                break
            decisions += 1
            reward += float(step_reward)
            steps = int(info["episode_extra_stats"]["env_steps"])
            if terminated or truncated or steps >= primitive_budget:
                break
        primitive_steps = int(info["episode_extra_stats"]["env_steps"])
        return {
            "mode": mode, "seed": seed, "controller": "seeded_uniform_random",
            "diagnostic_only": True, "paper_result_reproduced": False,
            "decisions": decisions, "primitive_steps": primitive_steps,
            "reward": reward, "terminated": bool(terminated),
            "truncated": bool(truncated), "error": error,
            "available_actions": list(available),
            "max_decisions": max_decisions, "primitive_budget": primitive_budget,
        }
    finally:
        env.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--max-decisions", type=int, default=10)
    parser.add_argument("--primitive-budget", type=int, default=64)
    args = parser.parse_args()
    seeds = tuple(int(value) for value in args.seeds.split(","))
    if len(set(seeds)) != len(seeds):
        parser.error("seeds must be distinct")
    episodes = [
        run_episode(mode, seed, max_decisions=args.max_decisions,
                    primitive_budget=args.primitive_budget)
        for seed in seeds for mode in ("primitives", "skills", "mixed")
    ]
    payload = {
        "schema_version": 1,
        "evidence_tier": "real_minihack_environment_smoke",
        "paper_result_reproduced": False,
        "environment": "MiniHack-Room-5x5-v0",
        "codehack_commit": UPSTREAM_CODEHACK_COMMIT,
        "baseline_repo_reference_only": UPSTREAM_BASELINES_COMMIT,
        "custom_nle_wheel_sha256": UPSTREAM_NLE_WHEEL_SHA256,
        "episodes": episodes,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    failed = sum(episode["error"] is not None for episode in episodes)
    if failed:
        raise SystemExit(f"{failed} MiniHack episodes failed; inspect the output artifact")


if __name__ == "__main__":
    main()
