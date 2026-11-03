# PROBE: Policy Auditing and Deterministic Rescoring for Tool Agents

<!-- source-sha256: 4b9e4a22dc1d386ecf2b231bcfa47bb915e4950b10a91f26130ca89231702cf7 -->

[简体中文](README.md) · English

> `component_only` / L1 CPU mechanism diagnostic. Implements inert trace, verifier, and reward interfaces plus four standalone rule examples. No audit model was trained; neither full SkyAssist nor a real target service is integrated.

## Paper information

| Field | Details |
| --- | --- |
| Paper | [PROBE](https://arxiv.org/abs/2610.22124) |
| Affiliation | Co-first authors Kshitij Mishra and Abhijith Sharma; Mohamed bin Zayed University of Artificial Intelligence |
| First public release | 2026-10-15, arXiv v1 16:01:38 UTC; follow-up review of the 10-16 announcement |
| Authors' open-source code | [Author implementation](https://github.com/Mishrakshitij/PROBE) is publicly readable. Reuse license unconfirmed; the local code independently implements the paper. |
| Local adapter | None (`adapter: null`); component key `probe` |
| Local implementation | `src/auto_research/agent_research/probe_audit.py`; `scripts/run_oct17_supplement_agent.py` |

## Original paper summary

### Background and main changes

Completing a task does not mean complying with business or privacy policies. Final-state or harmful-text tests can also miss violations in multi-turn tool calls. PROBE trains an auditor to act as an ordinary customer interacting with a frozen target. A private verifier determines violations from the full trace. Rewards combine violations, credible customer behavior, tool-workflow progress, and policy diversity. The paper compares GRPO, DPO, and GFlowNet.

```mermaid
flowchart LR
    P[Public customer scenario] --> A[Auditor message]
    A --> T[Target with private policies and database]
    T --> H[Public dialogue]
    H --> A
    T --> X[Private tool trace]
    H --> V[Private verifier]
    X --> V
    V --> R[Violations, repeat hits, and coverage]
    J[Training-judge hits] --> D[Independent deterministic rescoring]
    H --> D
```

<!-- paper-figure:start -->
### Key figure from the paper

[![PROBE policy audit and deterministic rescoring, Figure 1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2610.22124#page=2)

> **Figure 1 from the paper:** Overall method design and key components. The figure comes from the [original paper](https://arxiv.org/abs/2610.22124), © the original authors. Select the image to see the source.
<!-- paper-figure:end -->

### Core equations

The V3 violation term in [§4 and Appendices D–F](https://arxiv.org/html/2610.22124v1) discounts repeat hits using policy severity and the number of previous hits in the episode:

$$
r_{viol}(t)=\sum_{i\in hits_t}\sigma_i d(n_i),\qquad
d(n)=\begin{cases}1&n=0\\1/2&n=1\\0&n\ge2.\end{cases}
$$

The local component implements only this term, not the full composite reward, audit RL, or semantic judge. Coverage uses the full declared policy set as its denominator. `violation_yield_per_100_episodes` counts all raw verifier hits, including repeated hits for the same policy across turns. It can exceed 100 and is not a success probability. Deduplicated episode–policy hits are reported separately as `distinct_episode_policy_yield_per_100_episodes`, not conflated with raw yield. Episodes with no hits and unsupported policies remain in the denominators.

### Reported offline and online results

SkyAssist has 20 policies, with 16 programmatic predicates and 4 mixed semantic judges at training time. The paper also evaluates unseen targets and transfer to τ-bench. **Manual verification in Appendices E/F found zero precision for the S5 judge. Fully deterministic rescoring reduced the best coverage from 60% to 55%**; the higher value is not verified capability. The authors report that multi-turn auditors discover more policies than static or zero-shot tests. That is a paper result, not a local one. No production online A/B test was reported.

## Local reproduction

```bash
PYTHONPATH=src python scripts/run_oct17_supplement_agent.py \
  --methods probe --device cpu --seeds 42,43,44 \
  --output runs/oct17-supplement-agent/probe.json
```

### Data protocol and CPU results

Each seed creates 12 inert traces with randomized repeat-turn counts and runs no tools. Four examples check required fields, confirmation of the current mutation intent, restricted destinations, and party size. They are not the paper's full 20-policy suite. A fifth explicitly unsupported semantic policy remains in the coverage denominator. Coverage is 4/5=0.8; 8/12 episodes have hits, and the 4 no-hit episodes are retained. These values describe constructed fixtures, not the safety of a target agent.

First-hit and repeat-hit rewards had 0 error against independent hand calculations. Three rounds of auditor/target callbacks actually ran, with 0 private scoring-marker exposures and 0 trained auditors. See the [CPU artifact](metrics/component-cpu-seeds42-44.json) for all values, per-seed results, and source hashes.

### Code mapping, cost, and limits

`deterministic_rescore` does not read judge hits. `violation_reward` maintains per-policy hit counts. `audit_metrics` retains unsupported policies and every episode. `audit_episode` passes only public scenarios and messages to the auditor. The target can retain its policy in a private closure, and the full trace reaches the independent grader only at the end. Trusted callbacks are an in-process data-isolation contract, not a sandbox for malicious code.

The original 4B QLoRA auditor, 30B target, multi-arm GRPO/DPO/GFlowNet training, semantic audit judge, and τ-bench capability evaluation were not implemented. The paper requires two A100-40GB GPUs per run, about 300 steps, and long multi-turn target calls. **The full experiments exceed the cost budget and were not reproduced (review complete)**. Rule predicates do not stand in for a learned auditor, and the component is not eligible for Evolve promotion.
