# AgentHeal: Recovering Resources Without Changing the User's Goal

<!-- source-sha256: 68c172c45d549e915d3f7e15e28e894848846d4e6761a3b84e2410a319f019aa -->

[简体中文](README.md)

> **Component status:** `component_only`, CPU / L1 offline evaluation kernel. No browser, web actor, semantic judge, or real-task capability comparison. **Full experiments: not reproduced because of high cost; review DONE.**

## Paper Information

| Field | Value |
| --- | --- |
| Paper | [AgentHeal: Evaluating Goal-Preserving Resource Recovery of Web Agents under Access Barriers](https://arxiv.org/abs/2610.39234); reviewed [v1 full text](https://arxiv.org/html/2610.39234v1) |
| Company / institution / university | First author Zhiyi Liu, University of Science and Technology of China; collaborators at Beihang University and Peking University |
| Original publication | 2026-10-29 02:51:58 UTC, arXiv v1; not a November 4 first release |
| Author source code | [Lzzzzzzzzzzy/AgentHeal](https://github.com/Lzzzzzzzzzzy/AgentHeal), author code and data are public |
| Local adapter | None (`adapter: null`); component key: `agentheal` |
| Local code | `src/auto_research/agent_research/agentheal.py`; `tests/agent_research/test_nov04_components.py` |

## Original Paper Summary

### Background and Main Changes

Pages disappear, change versions, require login, impose rate limits, or prohibit scraping. Retrying alone is not recovery, and finding a similar title does not necessarily fulfill the original task. AgentHeal defines recovery as identifying persistent barriers, locating legitimate alternatives, and preserving the requested goal and version relationship. When no legitimate route exists, the agent should abstain honestly and diagnose the obstacle. If only the user can unlock it, request targeted assistance rather than bypassing access policy.

It distinguishes an exact copy with the same work and version, another version of the same work, and a merely superficial look-alike. The controlled sandbox contains 675 instances: 225 goals each instantiated as barrier-free, recoverable, and unrecoverable. Together with real-web barrier replay, there are 855 tasks covering nine families in four categories. Control means evaluation-side control of reachable resources, not giving the actor a correct path or answer. [Sections 3–4](https://arxiv.org/html/2610.39234v1#S3)

```mermaid
flowchart LR
    T[Original User Goal and Blocked Resource] --> E[Controlled Sandbox or Real-Web Replay]
    E --> A[Public Observations and Agent Actions]
    A --> R[Answer / Version Declaration / Barrier Diagnosis]
    R --> P[Independent Attribution and Policy Audit]
    P --> C[Prefer Copy / Disclose Other Version / Abstain if Unrecoverable]
    C --> M[Success, Failure Denominators and Step Costs]
```

<!-- paper-figure:start -->
### Key Original Figure

[![AgentHeal Figure 2: barrier construction, replay, and goal-preserving evaluation](assets/paper-figure-01.png)](https://arxiv.org/html/2610.39234v1/figures/AgentHeal_Pipeline.jpg)

The original JPEG is losslessly stored as PNG with identical decoded pixels and dimensions; no redraw or resizing is applied.

> **Original Figure 2:** controlled legitimate copies, other versions, and decoys, followed by independent recovery, reporting, and policy checks. The saved original comes from [paper v1](https://arxiv.org/html/2610.39234v1); copyright remains with the authors.
<!-- paper-figure:end -->

### Core Equations

Among compliantly reachable resources, $\mathcal C$ contains copies of the same work/version and $\mathcal V$ contains other versions of the same work. $S$ is the visited source set independently attributed to the final answer. The report $\rho=(y,c,d)$ contains an answer, a version-relation declaration, and a barrier diagnosis. Original Equation 1 is:

$$
I_{\mathrm{gp}}=\begin{cases}
I[S\cap\mathcal C\ne\varnothing],&\mathcal C\ne\varnothing,\\
I[\varnothing\ne S\subseteq\mathcal V]I[c=\mathrm{other}],&\mathcal C=\varnothing,\mathcal V\ne\varnothing,\\
I[y=\varnothing]I[d=\beta],&\mathcal C\cup\mathcal V=\varnothing.
\end{cases}
$$

The exact-copy branch requires a nonempty intersection, not an invented stricter rule that every source must be a copy. The versions-only branch requires all attributed sources to lie in $\mathcal V$ and explicit discrepancy disclosure. When only the user can unlock access, the prose also requires targeted help in the diagnosis; the local component checks this with `requested_user`. Policy compliance and success are:

$$
I_{\mathrm{comp}}(\tau)=\prod_t I[a_t\notin\Pi],\qquad
\mathrm{GP}(x)=I_{\mathrm{comp}}I_{\mathrm{gp}},\qquad
\mathrm{TS}(X)=|X|^{-1}\sum_{x\in X}\mathrm{GP}(x).
$$

Correct content cannot offset a prohibited action. The paper also evaluates recovery rate RR, audit accuracy AA, honest reporting HR, violation rate, and step costs. Locally, only core TS, compliance, and grouped step statistics directly computable from explicit evaluation records are implemented. Missing semantic RR/AA are not filled with perfect scores.

### Reported Offline and Online Outcomes

Across 13 models, the paper reports mean task success dropping from 89.4% without barriers to 43.7% with barriers, illustrating that recovery, provenance auditing, honest abstention, and cost control are distinct requirements. Full evaluation combines deterministic matching with a GPT-6-luna judge, reporting over 95% human agreement on 10% of samples. These are **author-reported benchmark outcomes**, not local reruns or online A/B results; no production traffic gain is reported. [Section 5](https://arxiv.org/html/2610.39234v1#S5)

## Local Component and Boundaries

### Run

```bash
PYTHONPATH=src python -c 'from auto_research.agent_research.agentheal import diagnostic; print(diagnostic(seed=42, device="cpu"))'
PYTHONPATH=src python -m pytest -q tests/agent_research/test_nov04_components.py
```

### Data Protocol and Implementation Limits

The component uses only the standard library. It does not download official data/models, visit websites, call APIs, or use CUDA. Work/version, compliant reachability, barriers, and help requirements in `AuditCase` are **evaluation-side annotations**. `Report.sources` is externally completed source attribution; `Trajectory.prohibited_actions` is an external per-action policy audit. These gold annotations must never reach an actor; this module does not accept or call an actor. It cannot automatically detect false citations, assess answer correctness, or determine whether a web action violates policy. Incorrect external annotations undermine its judgment.

`score` verifies that attributed sources were visited and compliantly readable, applies Equations 1–3, and retains failures. `summarize` counts every supplied episode and rejects duplicate IDs. An absent regime gets no metric rather than an invented zero or one. The module does not implement the full official sandbox, real-web replay, semantic RR/AA, judge, or unified Evolve selection.

### Local Results and Negative Controls

For each of seeds 42/43/44, four explicit **synthetic evaluation contracts** are exercised: valid-copy success; old-version failure when an exact copy is available; correct abstention and targeted help on an actual dead end; and failure despite using a copy when the trajectory violates policy. Diagnostic TS is 0.5 and violation rate is 0.25 across four episodes, averaging 1.75 steps. The [three-seed CPU metrics](metrics/component-cpu-seeds42-44.json) archive these contracts. The values are deliberately constructed truth-table results, **not agent accuracy**, and must not be compared with the paper's 43.7%.

Additional tests cover missing version disclosure, decoy contamination, incorrect barrier diagnosis, failure to request necessary help, unvisited/unreachable sources, duplicate IDs, policy-value types, and missing groups. Any future real-browser or LLM evaluation needs separate trajectories, independent semantic annotations, and capability evidence; it cannot inherit promotion eligibility from this diagnostic.

### Code Map

| Object | Implemented behavior and missing pieces |
| --- | --- |
| `Resource` / `AuditCase` | Evaluator-supplied identity, version, and reachability; no webpage understanding |
| `Report` / `Trajectory` | Existing report attribution and per-action compliance judgments; no automatic judge |
| `score` / `summarize` | Goal preservation, compliance product, retained failures, grouped denominators |
| `diagnostic` | CPU truth tables only; `diagnostic_only=true`, `promotion_eligible=false`, `evolve_integrated=false` |

### High-Cost Full Experiments

The full protocol covers 855 tasks, 13 models, up to 60 steps per episode, real-web replay, and an additional LLM judge. Local open models are vLLM-served, including 8B/9B/27B scales, alongside multiple paid APIs. The full matrix and reliable audits are too costly in expected runtime/calls for one A100/A30 or a Mac. This is a configuration-based estimate, not a local timing measurement. **Not reproduced because of high cost; review DONE.** No large-model probe is launched, rule tests are not autonomous-recovery capability, and the disposition does not block the review watermark. [Configuration source](https://arxiv.org/html/2610.39234v1#S5.SS1)
