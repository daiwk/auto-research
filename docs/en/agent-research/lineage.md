# Agent paper lineage and open gaps

<!-- source-sha256: 614ee1d31fe685d329f302439f03ac93785a83f02470dc05468428ce37a58884 -->

[简体中文](../../agent-research/lineage.md)

This audit covers reasoning and action, reflection, planning search, tool learning, multi-agent orchestration, lifelong learning, and 2026 planning RL. Latest boundary check in this snapshot: **2026-08-08**.

## Coverage

| Lineage | Representative methods | Status | Repository coverage |
|---|---|---|---|
| Reasoning and action | ReAct, ReWOO | Implemented | Stepwise interaction; separate Planner, Worker, and Solver |
| Self-improvement | Self-Refine, Reflexion | Implemented | In-episode refinement and cross-trial verbal reflection |
| Explicit search | Tree of Thoughts, LATS | Implemented | BFS thought tree; MCTS with environmental feedback |
| Tool learning | Toolformer, PEARL | Implemented | Self-supervised tool labels; tool exploration and planner RL |
| Multi-agent orchestration | AutoGen, MetaGPT | Implemented | Role messages, handoffs, termination, software SOP, and role artifacts |
| Lifelong learning and memory | Voyager, U-Mem, LEGOMem, MemTool, HiSkill, UniMem, SkillRise | Implemented | Skills, knowledge, procedures, tools, hierarchy, cross-task skill documents, and episodic-to-parametric memory |
| External feedback | CRITIC | Implemented | Actual failed patch, test feedback, and revision |
| Agent RL and OPD | Agent Lightning, Search-R1, RAGEN, LOOP, WebAgent-R1, MUA-RL, SEED, CAST, TurnOPD | Implemented | Search, web, long-horizon and multi-turn user RL, trajectory stabilization, hindsight skills, turn credit, and dynamic rollout budgets |
| Software engineering | SWE-agent, OpenHands | Implemented locally | Real temporary repositories, edits, commands, and regression tests |
| CUA reward evaluation | OSReward / OS-Shepherd | Protocol mini-suite | Success/failure recall, balanced accuracy, and leniency |
| Modular specialists | MRKL, HuggingGPT | Implemented | Neurosymbolic routing, model matching, and dependency-graph execution |
| Classic long-term state | Generative Agents, MemGPT | Implemented | Memory scoring/reflection; virtual-context paging |
| Browsing and citation | WebGPT | Deterministic implementation | Browser actions, evidence citations, and rejection sampling |
| Embodied skill grounding | SayCan | Simulation | Language relevance times skill affordance |
| Program and tool reasoning | PAL, ART | Implemented | Symbolic interpreter; task-library lookup and tool pausing |
| Deep research and tool RL | DeepResearcher, ReTool, ToolRL | Implemented | Citation rewards, interleaved tool reasoning, and selection, arguments, and execution feedback |
| Skill consolidation and self-evolution | SAGE, MemSkill, Memento-Skills, SEARL | Implemented | Skill generation/revision, memory-to-skill, versioning, and policy/tool-graph evolution |
| Zero-data multi-agent curriculum | Agent0 | Implemented | Self-generated tasks, executor voting, and capability-frontier curriculum |
| Step-level RL and public evaluation | Agent-R1, CAMEL, ToolBench, GAIA | Implemented | Transition context and credit, role-play, tool-instruction retrieval, and three-tier general assistant mini-suite |

## Completed planned capabilities

Eight additional P0 algorithms were implemented: DeepResearcher, ReTool, ToolRL, SAGE, MemSkill, Memento-Skills, SEARL, and Agent0. These cover deep research, tool RL, skill consolidation, self-evolution, and multi-agent curricula in the compositional Evolve genome. See the [all-domain gap audit](../full-domain-gap-review-20260808.md).

Four P1 items were also implemented: Agent-R1, CAMEL, ToolBench/ToolLLM, and GAIA. `gaia-mini` checks the public protocol and tool evidence chain, not the official 466-question leaderboard.

| Environment | Status | Evidence or limits |
|---|---|---|
| Agent Lightning LLM RL | Trainable policy connected | [PR #116](https://github.com/daiwk/auto-research/pull/116): SmolLM2 pairwise updates, transition credit, actual code executor |
| Compositional Agent Evolve | Complete | [PR #117](https://github.com/daiwk/auto-research/pull/117): seven axes of memory, planner, tool, critic, policy, recovery, and capacity, with three-seed promotion |
| Official SWE-bench Lite, full ToolHop, actual browser | Deferred by the user | Needs official containers, model-call budget, isolated sandbox, networking, and credential policy; not called integrated |

## Conclusion

Covered classic lines include reasoning/action, search, reflection, neurosymbolic and specialist orchestration, multi-agent systems, long-term memory, virtual context, planner RL, trainable LLM policies, and real code execution. The `swebench-local` controlled fixture remains bounded. No static P0/P1 remains open in this scope. Further work comes from dynamic discovery or resumption of the deferred environments.

LOOP's long-horizon leave-one-out PPO and replay, WebAgent-R1's context compression and parallel complete-trace M-GRPO, and MUA-RL's simulated clarification and real tools cover complementary mechanisms. They enter unified Evolve as `critic`, `planner`, or `tool` operators.
