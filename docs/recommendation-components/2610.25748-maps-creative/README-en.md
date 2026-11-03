# MAPS: A four-agent feedback loop for personalized video ads

<!-- source-sha256: 1f8f592330a2045072c76511614cfe29f7a04c10ed6898c8fee3516061181597 -->

[简体中文](README.md)

> Research reference only. The full system was reviewed and not reproduced because of cost. Generic GRPO or a weighted sum of three scores is not a substitute for the video advertising system.

## Paper information

| Field | Details |
| --- | --- |
| Paper links | [arXiv 2610.25748v1](https://arxiv.org/abs/2610.25748v1); [pinned PDF](https://arxiv.org/pdf/2610.25748v1) |
| Original title | MAPS: A Multi-Agent Personalized Script-Driven Video Advertising System Enhanced by Reinforcement Learning |
| Company / institution | First author Zhongyu Wang: Beihang University (first listed), Kuaishou Technology. Co-first authors Chen Zuo and Qingxuan Sun are at Kuaishou. |
| First public release | 2026-10-19 04:00:27 UTC; arXiv announcement on October 20 |
| Author code | No verifiable author repository found in the paper or on arXiv during this review. Kling-Omni is an external generation service, not an open-source implementation. |
| Local adapter / stable key | `maps-creative`, reference key; `adapter: null` |
| Local implementation | None. Documentation and catalog entry only: `src/auto_research/paper_specs/catalog/recommendation/maps-creative.json`. |

## Paper summary

### Background and main changes

Retrieving ads from a fixed inventory cannot adapt promptly to individual preferences and feedback. MAPS assigns four agents: Profile extracts the user profile, Scripter writes the storyboard, Director calls video generation, and Reflector attributes feedback. Reflector distinguishes a profile problem from a script problem and routes the smallest appropriate edit. Profiles cover not only interests, but also presentation preferences and decision tendencies.

Scripter first learns the script structure with supervised fine-tuning (SFT). A mixed reward then combines structural validity, personalized preference, and consistency with product facts; training uses GRPO-style within-group normalization. The defining system is the combination of language models, video generation, and a private feedback environment, not a standalone reward equation.

~~~mermaid
flowchart LR
  H[Interaction history] --> P[Profile]
  P --> S[Scripter storyboard]
  I[Product facts and assets] --> S
  S --> D[Director / Kling-Omni]
  D --> V[Video ad creative]
  V --> F[User interaction feedback]
  F --> R[Reflector attributes feedback and makes minimal edits]
  R --> P
  R --> S
~~~

Figure 2 shows the four-agent system; Figure 3 shows the script training pipeline.

<!-- paper-figure:start -->
### Original paper figure

[![Paper Figure 2: the four-agent personalized video ad loop](assets/paper-figure-01.png)](https://arxiv.org/html/2610.25748v1/maps_framework.png)

> **Paper Figure 2:** The Profile, Scripter, Director, and Reflector loop for ad creative. The figure depicts the full system; the video model and online feedback loop are not reproduced locally. From the [original paper](https://arxiv.org/abs/2610.25748v1); copyright remains with the authors. Click the image to open its source.
<!-- paper-figure:end -->

### Core equations

$$
R=.3R_{struct}+.4R_{pers}+.3R_{prod},\qquad
A_k=\frac{R_k-\bar R}{\sigma_R+\epsilon}.
$$

The paper describes the RL objective as advantage-weighted log likelihood minus a KL penalty relative to the SFT policy. The structural reward covers format, completeness, character consistency across scenes, and physical plausibility. LLM judges score personalization and product consistency. This reference does not replace those semantic judges with keyword counts.

### Offline and online results reported in the paper

PCG and PCI each use an offline matrix of 50 users × 5 products, covering generation quality, preference, product consistency, and other dimensions. In Kuaishou's specific ad setting, Section 4.3 / Table 3 reports online gains versus GRM of +2.87% CTR, +2.74% CVR, and +9.85% ARPU; the gains versus DLRM are +4.88%, +4.01%, and +12.89%, respectively. That section gives neither traffic fraction nor trial duration. The study cannot be described as full-traffic or assigned a duration, but its quantitative online evidence meets the catalog's inclusion threshold.

## Local reproduction and cost decision

Profile and Reflector use Qwen3-VL-32B; Scripter uses an 8B model. SFT runs for 20 epochs with a maximum of 8,192 tokens, followed by 5,000 RL steps. The paper uses eight H100 GPUs. Director depends on Kling-Omni, and the feedback loop depends on the production system. The full matrix was reviewed and not reproduced within the single-A100/A30 or Mac budget. There is no local model, evaluation metric, or GPU receipt, and the entry is not queued for automatic retry or Evolve.
