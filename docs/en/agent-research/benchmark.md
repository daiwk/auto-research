# Shared agent evaluation protocol

<!-- source-sha256: ee4113856971cb5e6a61999c158c826d434a28bc6da00a872921105fdeedb1b0 -->

[简体中文](../../agent-research/benchmark.md)

Compare context, knowledge acquisition, and tool maintenance costs as well as final success. Current mini-suites rerun on Mac and Linux CPU. Real LLM executors can use the same metric interface.

## Evaluation matrix

| Benchmark | Main capability | Local tasks | Key metrics |
|---|---|---|---|
| `evomem-mini` | Within- and cross-episode knowledge and execution memory | Four EvoMem task quadrants | Joint success, acquisition cost, memory size |
| `planbench-mini` | Verifiable planning and procedure reuse | Structured action sequences | Plan success, mean cost, reused plans |
| `scalemcp-mini` | Dynamic tools under limited context | Multi-turn tool routing | Task success, context cost, evictions |
| `swebench-local` | Locate, edit, test, and revise code | Temporary Python repositories and actual unittest | Resolved rate, commands and edits, feedback rounds, reuse |
| `osreward-mini` | Computer-use reward scoring and leniency | Completed/incomplete evidence traces across four platforms | Success/failure recall, balanced accuracy, leniency |
| `toolroute-l2.1` | Isolated planning, tool feedback, and recovery without a guide/oracle | Disjoint train/validation/test families, longer test paths | Answer accuracy, plan F1, recovery, invalid/irreversible rate, cost |

The first three and `osreward-mini` are deterministic local mini-suites. `swebench-local` executes actual code but uses local micro fixtures, not official SWE-bench Lite. `osreward-mini` reproduces metric and evidence-checking protocols, not the official 1,019 screenshot traces.

`toolroute-l2.1` is separate from L1. Policies see no reference answer, plan, or route and no guide reveals the correct tag. Select on validation and evaluate test after all generations. See [L2.1 protocol and three-seed results](capability-benchmark.md).

## Fair comparison

- Fix 120 episodes and seed 42, with the same task sequence across methods and controls.
- `long-context` keeps uncompressed history and accumulates cost by retained context units.
- At equal success, compare mean cost and method diagnostics. Cost alone does not predict real LLM behavior.
- Save per-step traces and mark writes, retrievals, escalations, reuse, and evictions.
- External model calls must record model, sampling, token cost, retries, and cache hits.
- Initial code benchmark repositories must genuinely fail. Success comes only from regression exit status with command output retained.

## Stable results

| Method and benchmark | joint success | Mean cost | Diagnostic |
|---|---:|---:|---|
| Long-context · EvoMem mini | 1.0000 | 64.5000 | History grows linearly |
| U-Mem · EvoMem mini | 1.0000 | 3.0500 | memory size 12 |
| LEGOMem · PlanBench mini | 1.0000 | 1.1200 | reused plans 108 |
| MemTool · ScaleMCP mini | 1.0000 | 1.9812 | tool evictions 200 |
| ReAct · ScaleMCP mini | 1.0000 | 3.0000 | reasoning/actions 360/360 |
| Reflexion · PlanBench mini | 0.9000 | 1.1000 | reflections 12 |
| Voyager · PlanBench mini | 1.0000 | 1.1200 | skills created/reused 12/108 |
| Tree of Thoughts · PlanBench mini | 1.0000 | 2.5000 | expanded/backtracked 1200/480 |
| LATS · PlanBench mini | 1.0000 | 4.0000 | rollouts/reflections 480/360 |
| Toolformer · ScaleMCP mini | 1.0000 | 3.0000 | accepted/candidate calls 360/540 |
| Self-Refine · PlanBench mini | 1.0000 | 2.0000 | feedback/refinement 120/120 |
| ReWOO · PlanBench mini | 1.0000 | 3.5000 | plans/worker calls 120/360 |
| AutoGen · PlanBench mini | 1.0000 | 3.0000 | agent messages/critic rounds 360/120 |
| PEARL · PlanBench mini | 1.0000 | 1.1200 | explorations/updates/reuse 24/12/108 |
| MRKL · ScaleMCP mini | 1.0000 | 1.2500 | router/symbolic calls 360/170 |
| HuggingGPT · PlanBench mini | 1.0000 | 2.3500 | model matches/edges 360/240 |
| Generative Agents · EvoMem mini | 1.0000 | 1.7900 | retrieved/reflections 354/30 |
| MemGPT · EvoMem mini | 1.0000 | 0.9200 | writes/page-ins/interrupts 108/96/108 |
| WebGPT · ScaleMCP mini | 1.0000 | 3.0000 | references/candidates 600/240 |
| SayCan · PlanBench mini | 1.0000 | 3.3750 | checks/filtered 1350/790 |
| PAL · ScaleMCP mini | 1.0000 | 1.4000 | programs/interpreter calls 120/120 |
| ART · PlanBench mini | 1.0000 | 1.5500 | retrievals/pauses/updates 108/360/12 |
| OS-Shepherd protocol · OSReward mini | 1.0000 BalAcc | 2 evidence checks | sRec/fRec 1.0000/1.0000; leniency 0 |

Artifacts: [base mini-suites](../../experiments/agent-mini-suites-seed42.json), [classic methods](../../experiments/classic-agent-mini-suites-seed42.json), [code sandbox](../../experiments/agent-code-sandbox-seed42.json), [classic gaps](../../experiments/p0-missing-agent-mini-suites-seed42.json), and [P1 candidates](../../experiments/p1-agent-candidates-mini-suites-seed42.json).

## Commands and artifacts

```bash
auto-research agent-eval --method voyager \
  --benchmark planbench-mini --episodes 120 --seed 42

auto-research agent-eval --method swe-agent \
  --benchmark swebench-local --episodes 12 --seed 42

auto-research agent-eval --method os-shepherd \
  --benchmark osreward-mini --episodes 120 --seed 42

auto-research agent-capability \
  --methods long-context,react,reflexion,agent-g2,ahead,auso \
  --episodes 60 --seeds 42,43,44
```

Outputs in `runs/agent-research/<method>-<benchmark>-seed<seed>/` contain episode traces, `metrics.json`, and Chinese `report.md`.

## Acceptance for new methods

Require unit tests, corresponding mini-suite or real sandbox, stable metrics, and strict MkDocs build. Explain missing private environments, paid APIs, or human judges and prefer public benchmark adapters. Deterministic scores are not the paper's results.

## Agentic RL and continual memory diagnostics

Alongside success and cost, retain SEED hindsight skills and dense credit, CAST solver queries and turn credit, TurnOPD rollout savings, HiSkill nodes/edges and AtomicOp reuse, and UniMem episodic/parametric routing and consolidation. Match episodes, memory budget, and seed within a benchmark.

CAM-DF reports total candidate and exposed tools, exposure reduction, cost-aware stopping, and regret-weighted labels. SkillRise reports skill-document edits, cross-task reuse, and downstream credit separately. Key-value memory alone is not cross-task skill evolution.

Search-R1 reports searches, masked retrieval tokens, and outcome updates. RAGEN reports rollouts/filtering, critic baseline, Echo Trap probes, and gradient clipping. 100% deterministic mini-suite success shows executable control flow, not actual search or game results.

LOOP reports leave-one-out updates, old-trace reuse, and token clipping. WebAgent-R1 reports compressed tokens, parallel complete trajectories, and M-GRPO updates. MUA-RL records simulated user turns, intent corrections, real tool responses, and final rewards. See [fixed-seed metrics](../../experiments/omitted-agentic-rl-opd-seed42.json). This is not AppWorld, WebArena-Lite, TAU2, or BFCL.
