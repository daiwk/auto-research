# Option-Channel Attack: Misleading Labels Can Bypass Agent Guardrails

<!-- source-sha256: e3bed2e957d08d768de8ec5883c6b17716d118ce1f5821976d7d0561625e8a93 -->

[简体中文](README.md)

> A real Laya checkpoint security diagnostic, not agent task success or a production safety certification.

## Paper information

| Field | Value |
| --- | --- |
| Paper | [One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails](https://arxiv.org/abs/2610.12292) |
| Affiliation | University of Southern California; first author Seyedarmin Azizi |
| First public release | 2026-10-08 (arXiv v1) |
| Authors' code | [Released](https://github.com/ArminAzizi98/option-channel-attack); independent local implementation |
| Adapter | `option-channel-attack` |
| Local code | `src/auto_research/system_one/option_channel.py`; `scripts/run_option_channel.py` |

## Original paper

### Background and contribution

Typed models score caller-provided options, whose names are themselves inputs. With action and trusted policy fixed, replacing only the allow label can convert a correct denial into approval. Evaluate dangerous fail-open separately from fail-closed usability failures.

```mermaid
flowchart LR
 F[Fixed action and policy] --> C[Clean options] --> E[Correct clean denials]
 F --> L[Choose labels on calibration] --> A[Held-out attack]
 E --> R[Conditional ASR]
 A --> R
```

<!-- paper-figure:start -->
### Key figure from the paper

[![Option-Channel Attack, original Figure 1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2610.12292#page=3)

The typed model receives both state and labeled, defined options. The attack changes option labels rather than state. From the [paper](https://arxiv.org/abs/2610.12292); copyright belongs to the authors.
<!-- paper-figure:end -->

### Core equation and paper results

Let $E$ be prohibited examples correctly denied on clean input. $ASR_{open}=|\{i\in E:\text{attack allows}\}|/|E|$. Empty $E$ is undefined, not zero or one. Paired bootstrap recomputes the denominator in each resample.

The [paper](https://arxiv.org/html/2610.12292v1) studies seven open-weight models. Four that include labels in inputs show 93%–100% fail-open with misleading allow labels. This neither shows every agent is unsafe nor reports the local single-model run. No live A/B was reported.

## Local reproduction

Six synthetic policies, 24 calibration and 24 evaluation examples per policy, seeds 42/43. Select only on calibration from `escalate/deny/stop/lantern`. A public Laya checkpoint ran on A100 without real external tool calls or executing evaluated actions.

```bash
python scripts/run_option_channel.py --checkpoint checkpoints/laya \
  --device cuda:0 --count 24 --output runs/option-channel-42-43.json
```

### Data and results

Inputs are action text, fixed policy definitions, and option names; gold enters only external scoring. `exfil` fail-open rose 0.1667→0.5833; 10 clean denials give ASR=0.5, 95% paired interval [0.1667,0.8333]. Clean `secret` and `escape_or_exfil` already allowed everything, so ASR is undefined. Denominators as small as 1 make ASR=1 nongeneralizable. See [metrics](metrics/laya-a100.json) and [GPU receipt](../../gpu-validations/option-channel-attack-a100-20261011.json).

### Code and limits

`guard_items` makes auditable balanced synthetic data, not verbatim GuardBench. `score_items` fixes action/policy; `attack_metrics/paired_asr_interval` separate error directions and preserve undefined denominators. Controls add irrelevant log noise or restore trusted option names. The latter recovers clean behavior without proving robust defense.

No full author label scan, seven-model comparison, or real prompt injection/jailbreak/harmful-content datasets. The early runner's erroneous `diagnostic_only=false` was corrected and rerun on A100. Raw output and archive now describe L1 synthetic guardrail diagnostics, with no Evolve promotion.
