# Online IcePop: A pure-online mismatch mask with one update per rollout

<!-- source-sha256: ee0e0ff8ca5ea6fdb7a48acd9463b3e9ca955912aa75315a672256b9f1c5a1a3 -->

[简体中文](README.md)

> Isolated candidate-policy RL mechanism, not the source's large-model results.

## Source information

| Field | Details |
|---|---|
| Source | [Online IcePop technical note](https://zhuanlan.zhihu.com/p/1984379979035850499) |
| Institution | Ant Group Bailing Team |
| First public release | 2025-12-16 (authors' public note) |
| Author code | No standalone source released; a training-schedule variant of IcePop. |
| Local adapter | `online-icepop` |
| Local reproduction code | [`src/auto_research/post_training/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/post_training/) |

## Method and evidence

Ordinary IcePop handles training/rollout engine mismatch as well as stale policy from repeatedly updating on one rollout. Online IcePop allows only one update per batch, so the stale-policy ratio is 1 and PPO ratio/clipping are removed. Keep the IcePop two-sided mask and original in-range engine-mismatch ratio.

$$
r_t^{\rm policy}=1,\qquad \mathcal L_{\rm online}=-\mathbb E\!\left[\mathbf1[c_{\rm low}\le\rho_t^{\rm TI}\le c_{\rm high}]\,\rho_t^{\rm TI}A_t\right].
$$

The note argues that single-update scheduling prevents accumulated router shift. It is not a standalone paper and gives no independent benchmark table or production A/B.

## Local reproduction

Refresh rollout weights after every step, enforce `policy_staleness_ratio_mean=1`, disable PPO clip and retain IcePop `[0.5, 5.0]` masking.

```bash
auto-research post-train --algorithm online-icepop --dataset gsm8k-candidate --maximum-examples 256 --steps 120 --seed 42
```

[Fixed seed metrics](../../experiments/rl-papers-summary-seed42.json). One candidate group stands in for a rollout batch; no real parallel sampling or communication. This checks single-update scheduling, stale ratio removal and the engine mismatch mask together.
