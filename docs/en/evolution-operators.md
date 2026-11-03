<!-- source-sha256: 26ddc4ffb3cf866b773e30e755e78023d0f6f0348e88bd8de401517e55f7da51 -->

# Evolve operator compatibility graph

[简体中文](../evolution-operators.md) · [Evolution protocol](model-evolution.md)

Evolve candidates are more than strings. All paper-derived architectures, training objectives, data strategies, memory, planning, tools, critics, policies, and recovery strategies go into a common `OperatorSpec` registry. Each entry declares:

- The source paper and research domain.
- Compatible models and genome slots.
- Prerequisites and explicit conflicts.
- Whether it can be combined with other operators in the same slot.
- Relative compute, memory, and latency costs.

The planner filters candidates for compatibility before assembling the candidate set. This prevents it from applying a recommender architecture to an LLM-only model, placing an agent memory operator in a post-training objective slot, or picking mutually exclusive operators for a slot that does not allow composition.

## Usage

```bash
# List all paper operators.
auto-research operators list

# Check operator compatibility and resource budgets.
auto-research operators check \
  --model agent \
  --operators memory:u-mem,planner:react,tool:toolformer \
  --max-compute 6 --max-memory 6 --max-latency 6

# Export a machine-readable graph for dashboards or external candidate generators.
auto-research operators export --output runs/operator-graph.json
```

Agent operators in `memory/planner/tool/critic/policy/recovery` occupy separate slots and can be combined. DPO and GRPO both occupy the post-training `objective` slot, so selecting them side by side is rejected. An unrecognized local candidate can still be checked in single-operator mode. To become an installed paper operator, it must go through candidate staging, deterministic tests, and manual promotion.

## Boundary with live retrieval

Live paper retrieval only produces `retrieved-design-only` candidates. Similar titles do not make a paper eligible for the executable graph. An operator has executable provenance and a compatibility contract only if its paper method is already implemented and mapped in the repository, or its code has passed candidate promotion. Reports therefore distinguish operators from implemented papers, ideas from live retrieval, and composition hypotheses for the current round.
