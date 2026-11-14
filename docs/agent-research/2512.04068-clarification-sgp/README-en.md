<!-- source-sha256: bcfc3426ac9f82a6fe1cb0a77ffa9fb5c23038102618b455d222f8c46adc72f3 -->
# SGP: cost-steerable clarification and interpretation-balanced ReST selection

[简体中文](README.md)

> **component_only/L1 mechanism diagnostics, not full-model or agent capability.** The full experiment is not reproduced because of cost (review DONE); only the explicitly bounded components below execute.

## Paper information

| Field | Value |
| --- | --- |
| Paper | [Learning Steerable Clarification Policies with Collaborative Self-play](https://arxiv.org/abs/2512.04068v1), [fixed v1](https://arxiv.org/html/2512.04068v1) |
| Institution | First author Jonathan Berant, Google Research; verified priority affiliations: Google Research / Google DeepMind / Meta. Collaboration does not replace the first-listed affiliation |
| Original publication | **2025-12-03 18:49:54 UTC**; a historical repair, not a November13 first release |
| Authors' code | No verifiable dedicated author source release was found in fixed v1 or bounded official-entry checks; cited libraries and third-party replicas are not counted |
| Local adapter / key | `clarification-sgp`; `adapter=null`; no Evolve integration |
| Local code | `src/auto_research/agent_research/clarification_sgp.py` |

## Original paper

### Motivation and changes

An ambiguous query can be answered by guessing, enumerating interpretations, or first clarifying. The best action depends on turn and verbosity costs. The assistant observes numerical α and β while a simulated user privately knows the intended interpretation; an external environment scores the final dialogue.

Training does not simply take one lucky high-reward rollout. It filters low-F1 or noncompliant user trajectories, averages each action sequence within each interpretation and then across interpretations, selects the best sequence, and retains its best rollout per interpretation. Only assistant turns train the model. Semantic generation, user simulation and the three ReST rounds are absent locally.

### Architecture

```mermaid
flowchart LR
  Q[Ambiguous query and interpretation distribution] --> R[External scored self-play]
  R --> F[Validity filter]
  F --> S[Interpretation-balanced sequence means]
  S --> B[Best compatible rollout per interpretation]
  B --> T[External assistant fine-tuning]
```

<!-- paper-figure:start -->
### Key original figure

[![clarification-sgp original Figure 2](assets/paper-figure-01.png)](https://arxiv.org/html/2512.04068v1/figures/example_rollout_nano.png)

From the [original paper](https://arxiv.org/html/2512.04068v1#S3.F2); copyright remains with the original authors. These are official HTML PNG bytes without cropping, redrawing or PDF rendering. A dialogue example illustrating information separation; local code does not generate this conversation.
<!-- paper-figure:end -->

### Core equations

$$
R(\rho)=100F_1(\rho)-\alpha n_{clar}(\rho)-\beta\,words_{assistant}(\rho),\qquad
s^*=\arg\max_s\frac1{|I|}\sum_{i\in I}\operatorname{mean}_{\rho\sim(s,i)}R(\rho).
$$

Local F1 inputs and filter thresholds use 0–1; rewards explicitly use percentage points, matching v1 Tables 2–3 and the α={0,2,20}, β={0.1,0.7,5} scale. Normalizing rewards requires normalizing costs too. Only final-assistant whitespace words are charged, not user output or thoughts. Missing interpretation coverage is not fabricated. Lexical sequence/ID ties are a deterministic local convention.

### Author results

For ambiguous AmbigQA development queries, fixed v1 reports SGP reward/F1 of 6.63/19.94 versus Prompted −34.49/16.16; Pacific values are 54.32/65.73. These are full Gemma2-9B self-play/training results, not local selection capability. No production-user A/B result is reported.

## Local reproduction

### Protocol and code mapping

Rollout contains offline scores, interpretation IDs, action sequences and final-assistant word counts, not an actor gold parameter. reward computes costs; select_rollouts filters, balances interpretation means and selects one compatible best row per interpretation. Callers supply the paper's dataset-dependent F1 threshold, 0.1 for AmbigQA or 0.4 for Pacific. User-answer overlap≥0.5 mechanically filters ignored-assistant cases, not semantic correctness.

```bash
PYTHONPATH=src python -c 'from auto_research.agent_research.clarification_sgp import diagnostic; print(diagnostic(42))'
PYTHONPATH=src python -m pytest tests/test_nov13_colm_agent_components.py -q
```

### Evidence and controls

Controls cover lucky samples versus balanced means, changed choices under clarification costs, final-assistant word units, invalid actions and missing interpretation coverage. Fixed offline scores test arithmetic and selection, not dialogue strategy or generated training data.

Three-seed mechanism receipts are in [CPU metrics](metrics/component-cpu-seeds42-44.json) and the batch's frozen record. Fixed-input diagnostics are not full training, capability gain or online benefit. GPU acceptance requires actual A100/A30 evidence.

## Boundaries

No user/assistant model, token-F1 evaluator, ReST fine-tuning, development-checkpoint selection or formal dialogue benchmark is implemented. Offline evaluators may use references; evaluated assistants must not receive them. There is no actor callback here. CPU selection does not establish the full method's effectiveness.

### Full experiment not reproduced

The full configuration uses two Gemma2-9B models,192 training and64 test rollouts per query, three ReST epochs and two benchmarks. This paper/upstream configuration exceeds the current single-A100/A30-or-Mac budget. It is a source-reported configuration, not local training measurement. No cost probe, paid API, checkpoint download or full experiment was attempted. **Too costly; not reproduced (review DONE)**. Automatic retry and implementation queues remain disabled.
