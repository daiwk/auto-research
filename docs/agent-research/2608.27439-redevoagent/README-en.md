# RedEvoAgent: Evolve red-team skills from experience

<!-- source-sha256: 307c8890d0b36d94ab59d687674e42eebfa235d4e953ec921d2ccc38e8afc288 -->

[简体中文](README.md)

> Deterministic tool profiles, deciding-tool attribution and held-out validation ratchet.

## Paper information

| Field | Details |
|---|---|
| Paper | [Paper or original source](https://arxiv.org/abs/2608.27439) |
| Institution | City University of Hong Kong (first-listed first-author affiliation). |
| First public release | 2026-08-27 (arXiv v1) |
| Author code | No public author code found as of 2026-08-31. |
| Local adapter or method key | `redevoagent` |
| Local reproduction code | [`src/auto_research/agent_research/latest_20260831.py`](https://github.com/daiwk/auto-research/blob/main/src/auto_research/agent_research/latest_20260831.py) |

## Paper method and evidence

Distill cross-case experience into readable skills rather than retrieving long attack traces. Attribute only decisive tools and promote skills only if held-out validation beats the incumbent.

```mermaid
flowchart LR
  A[Cross-case tool outcomes] --> B[Attribute deciding tools]
  B[Attribute deciding tools] --> C[Test candidate skill on held-out validation]
  C[Test candidate skill on held-out validation] --> D[Keep only if incumbent is beaten]
```

<!-- paper-figure:start -->
### Original paper figure

[![RedEvoAgent paper figure](assets/paper-figure-01.png)](https://arxiv.org/html/2608.27439v1/fig1_overview.png)

Figure 1 shows experience-driven skill evolution. From the [original paper](https://arxiv.org/abs/2608.27439); copyright remains with the authors.
<!-- paper-figure:end -->

### Core equation

$$
s_{new}=\begin{cases}
s_c,&Eval(s_c)>Eval(s_{inc})\\
s_{inc},&\text{otherwise.}
\end{cases}
$$

### Reported results

No paper benchmark score is claimed locally.

## Local reproduction

PlanBench mini, 120 episodes: joint success **1.0000**, mean cost **0.4300**; attribution and validation ratchet counts matter more than saturation. [Metrics](metrics/planbench-mini-seed42.json). `public-agent-artifact-eval --method redevoagent` accepts pinned sanitized Agent Security Bench / AgentHarm-compatible exports (split, tool trace, success only), fits profiles on train, ratchets on validation, then locks test with a same-budget three-seed random-skill control. No jailbreak, real target, harmful prompt publication, or author artifact/score; only schema and safe replay evidence.
