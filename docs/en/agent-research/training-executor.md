# Trainable agent policies and real executors

<!-- source-sha256: 4826a7ae8936fc85531626bf1d6960aa141e4841b9923c2156bc00565bc395fa -->

[简体中文](../../agent-research/training-executor.md)

This guide covers `AG-001` and `AG-002`. It advances earlier deterministic mechanism simulations to two executable tiers.

## Agent Lightning → checkpoint policy

`agent-policy-train` partitions rollouts into prompt, failed patch, and successful patch spans. Failed transitions receive negative credit and successful ones receive positive credit. Pairwise causal-LM loss updates a pinned SmolLM2 policy. Before and after training, the model scores both patches, writes its chosen patch to a temporary repository, and actually runs `python -m unittest -q`.

```bash
auto-research agent-policy-train \
  --model-id HuggingFaceTB/SmolLM2-135M-Instruct \
  --steps 6 --episodes 6 --learning-rate 1e-5 \
  --device cuda --output-dir runs/agent-lightning-policy
```

This verifies the Agent Lightning path that decouples execution traces and training and propagates transition credit to a trainable policy. The micro fixture is not official SWE-bench and does not demonstrate real-world software engineering generalization.

Three real backward steps on A30 produced 6 credit updates and losses of `0.5013 / 0.4724 / 0.6142`. Joint success was `1.0` before and after training. The bridge runs, but the saturated three-task suite shows no capability gain. See the [stable summary](../../experiments/roadmap-4-7.json).

## Budget-matched executor matrix

`agent-matrix` shares repositories, issues, tests, and a maximum of four subprocesses per episode across methods. It records success, actual commands, file edits, reuse, and cost.

```bash
auto-research agent-matrix \
  --methods direct,critic,agent-lightning,swe-agent,openhands \
  --episodes 12 --seeds 42,43,44
```

The matrix does not mix different foundation models or API pricing. Current policies do not call external LLMs; comparisons are about controller and executor mechanisms. A real-checkpoint matrix must fix model revision, context length, generation tokens, and tool-call limits throughout.

Across 12 episodes × 3 seeds, direct joint success is `0.0`. CRITIC, Agent Lightning, SWE-agent, and OpenHands each reach `1.0`, with mean costs of `4.0 / 3.625 / 2.5 / 2.5`, respectively. Agent Lightning's cross-task reuse is `0.75`. These results reveal controller cost and reuse differences, not a large code-benchmark ranking.
