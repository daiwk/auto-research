from typing import Any


def render(result: dict[str, Any]) -> str:
    setup = result["setup"]
    lines = [
        f"# {result['paper']['title']}",
        "",
        f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}",
        "",
        "## Local full-parameter CPT/SFT ablation",
        "",
        "| Variant | LLM init | CPT | CPT final loss | SFT final loss | Recall@10 | NDCG@10 | Valid SID |",
        "|---|:---:|:---:|---:|---:|---:|---:|---:|",
    ]
    for name, row in result["results"].items():
        cpt_loss = "—" if row["cpt_loss"] is None else f"{row['cpt_loss']['final']:.4f}"
        lines.append(
            f"| {name} | {'yes' if row['pretrained_llm'] else 'no'} | "
            f"{'yes' if row['cpt'] else 'no'} | {cpt_loss} | "
            f"{row['sft_loss']['final']:.4f} | {row['recall_at_10']:.4f} | "
            f"{row['ndcg_at_10']:.4f} | {row['valid_sid_rate']:.2%} |"
        )
    effects = result["effects"]
    lines += [
        "",
        f"CPT Recall@10 delta: random init **{effects['cpt_recall_gain_random_init']:+.4f}**, "
        f"LLM init **{effects['cpt_recall_gain_llm_init']:+.4f}**. "
        f"LLM-init delta after CPT: **{effects['llm_init_recall_gain_with_cpt']:+.4f}**.",
    ]
    lines += [
        "",
        "## Actual local training setup",
        "",
        f"- Base LM: `{setup['base_model']}`; all parameters updated (no LoRA).",
        f"- SID: multi-resolution `{setup['sid_cardinalities']}`; catalog uniqueness {setup['sid_uniqueness']:.2%}.",
        f"- RQ-VAE: warm-up loss {setup['sid_training']['warmup_initial_loss']:.4f} → {setup['sid_training']['warmup_final_loss']:.4f}; joint SID-v2 loss {setup['sid_training']['rqvae_initial_loss']:.4f} → {setup['sid_training']['rqvae_final_loss']:.4f}.",
        f"- CPT: {setup['cpt_examples']} examples, exactly 50% behavior and 50% SID-text metadata; {setup['cpt_steps']} optimizer steps.",
        f"- SFT: {setup['sft_examples']} next-SID completions with prompt loss masked; {setup['sft_steps']} optimizer steps; LR={setup['learning_rate']:.0e}.",
        f"- Serving simulation: token-level constrained beam search, beam={setup['beam_size']}.",
        "",
        "## Paper's production A/B evidence",
        "",
    ]
    ab = result["paper_online_ab"]
    lines.append(
        f"YouTube LFV engaged users/panel CTR: **+{ab['lfv_engaged_users_percent']:.2f}% / "
        f"+{ab['lfv_panel_ctr_percent']:.2f}%**; Shorts: **+{ab['shorts_engaged_users_percent']:.2f}% / "
        f"+{ab['shorts_panel_ctr_percent']:.2f}%**."
    )
    lines += ["", "## Reproduction boundary", "", result["scope"], ""]
    return "\n".join(lines)
