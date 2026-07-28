from pathlib import Path
from typing import Any

import numpy as np

from ..rec_utils import load_movielens_sequences, ranking_metrics, summarize_runs
from .model import LLMResearchAgent, candidate_space, train_candidate


def reproduce_self_evolving_rec(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    all_items = np.arange(data.item_count)
    candidates = candidate_space()
    baseline_candidate = candidates[0]
    agent = LLMResearchAgent()
    baseline_runs, selected_runs, selected_names, journals = [], [], [], []
    for run_seed in (seed, seed + 1, seed + 2):
        baseline_model = train_candidate(data, baseline_candidate, run_seed)
        baseline_validation = ranking_metrics(
            data, lambda history: baseline_model.scores(history[-1], all_items),
            target="validation",
        )
        trials = [{
            "generation": 0,
            "candidate": baseline_candidate.name,
            "validation_ndcg_at_10": baseline_validation["ndcg_at_10"],
            "proposed_by": "human baseline",
        }]
        trained = {baseline_candidate.name: baseline_model}
        proposals = []
        for generation in range(1, 5):
            candidate, decision = agent.propose(candidates, trials)
            model = train_candidate(data, candidate, run_seed)
            metric = ranking_metrics(
                data, lambda history, model=model: model.scores(history[-1], all_items),
                target="validation",
            )
            trained[candidate.name] = model
            trials.append({
                "generation": generation,
                "candidate": candidate.name,
                "validation_ndcg_at_10": metric["ndcg_at_10"],
                "proposed_by": agent.model_name,
            })
            proposals.append(decision)
        promoted = max(trials, key=lambda row: row["validation_ndcg_at_10"])["candidate"]
        selected_names.append(promoted)
        journals.append({
            "seed": run_seed, "trials": trials, "llm_decisions": proposals,
            "promoted": promoted,
        })
        baseline_runs.append(ranking_metrics(
            data, lambda history: baseline_model.scores(history[-1], all_items)
        ))
        selected_model = trained[promoted]
        selected_runs.append(ranking_metrics(
            data, lambda history: selected_model.scores(history[-1], all_items)
        ))
    results = {
        "human_baseline": summarize_runs(baseline_runs),
        "llm_agent_promoted": summarize_runs(selected_runs),
    }
    return {
        "paper": {"arxiv_id": "2602.10226", "title": "Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents", "url": "https://arxiv.org/abs/2602.10226", "track": "recommendation"},
        "dataset": "MovieLens 100K (offline validation feedback plus untouched test holdout)",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": [seed, seed + 1, seed + 2], "llm_agent": agent.model_name, "generations_per_seed": 4, "search_space_size": len(candidates), "promoted_candidates": selected_names},
        "experiment_journal": journals,
        "results": results,
        "ndcg_gain_percent": 100 * (results["llm_agent_promoted"]["ndcg_at_10"] - results["human_baseline"]["ndcg_at_10"]) / max(results["human_baseline"]["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"rmsprop_youtube_percent": 0.06, "rmsprop_surface_percent": 0.12, "glu_youtube_percent": 0.06, "glu_surface_percent": 0.14, "reward_youtube_percent": 0.03, "reward_surface_percent": 0.13},
        "scope": "Core-mechanism reproduction: a local instruction LLM reads the experiment journal, proposes untried executable edits, receives validation feedback and promotes a final model before isolated test. Google production A/B infrastructure is unavailable and not reproduced.",
    }
