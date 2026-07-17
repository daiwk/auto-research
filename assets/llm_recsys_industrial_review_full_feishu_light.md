# Recommendation and Large Models in Research and Industry / 推荐系统与大模型全面综述

Author: GPT-5.5  
Date: 2026-07-17  
Local source: `llm_recsys_industrial_review_full_en.tex`, `llm_recsys_industrial_review_full_zh.tex`

> This is the expanded survey version. The full PDF/LaTeX versions contain the complete 250+ item annotated catalog. For Feishu readability, this document keeps the full narrative, evidence tables, thematic paper maps, and a grouped catalog summary instead of writing one very large 250-row table.

> 这是扩展版综述。完整 PDF/LaTeX 版本包含 250+ 条逐条 annotated catalog。为了提升飞书可读性并避免超大表格写入超时，飞书版保留完整正文、证据表、主题论文地图和分组目录摘要，不再写入单个 250 行大表。

## English Version

# Scope, Evidence Tiers, and Survey Method

The phrase “recommendation plus large models” now covers several different technologies. It may refer to a BERT-style encoder used to represent news articles, a T5-style text-to-text model such as P5, a LLaMA-style model tuned for binary preference prediction, a multimodal LLM that extracts product attributes, a semantic-ID generator for retrieval, a trillion-parameter sequential transducer for ranking, or an agent that plans multi-step interaction with a user. These systems have different failure modes and very different deployment costs. Treating them as one category hides the engineering decisions that matter most.

This survey uses three evidence tiers.

1.  **Tier 1: public online evidence.** The source reports production A/B or live experiment results. These cases are the strongest evidence for industrial value, although the metrics and baselines are still not directly comparable.

2.  **Tier 2: production-oriented but incomplete online disclosure.** The source is industrial, uses real logs, or describes deployment architecture, but does not disclose full online A/B results. These works are valuable for architecture and systems lessons but should not be counted as proven online wins.

3.  **Tier 3: academic and pre-production research.** The work advances modeling, alignment, evaluation, robustness, fairness, or data methods, usually on public datasets. These papers define the technical frontier and frequently precede later deployment, but their offline gains should not be confused with production impact.

The time span is broad. We start from neural collaborative filtering, Wide&Deep, YouTube DNN, DIN, DIEN, SASRec, BERT4Rec, and DLRM, because these systems explain why the industrial recommender stack looks the way it does. We then follow the shift to pre-trained language models and LLMs: P5, M6-Rec, TALLRec, Chat-REC, InstructRec, ReLLa, CoLLM, LLaRA, A-LLMRec, TIGER, HSTU, PLUM, SIGMA, RecGPT, and many others. The latest papers included in the paper map are from July 2026, including LBR for length bias, multimodal memory-enhanced agent collaboration, LLM-based offline evaluation, connected-TV agentic recommendation, and controllability-centric evaluation.

# Historical Background: Why Recommendation Did Not Simply Become NLP

## The industrial recommendation stack

Industrial recommenders are multi-stage systems. Retrieval or candidate generation narrows a corpus of millions or billions of items. Pre-ranking and ranking score candidates under tight latency budgets. Re-ranking or slate optimization balances diversity, novelty, fairness, revenue, inventory, creator or merchant health, and policy constraints. Feature stores, streaming logs, online learning, ANN indexes, experimentation platforms, and guardrails are as important as the neural model itself.

This stack grew around sparse IDs, dense features, and behavior logs. Wide&Deep and DeepFM made cross features and dense embeddings practical for CTR prediction. YouTube DNN candidate generation showed how large-scale retrieval could be framed as multiclass classification over a huge corpus. DIN and DIEN emphasized target attention and evolving user interest. SASRec and BERT4Rec brought transformer sequence modeling to sequential recommendation. DLRM and its industrial descendants scaled sparse embedding tables and feature interaction networks. These models are not obsolete. They remain the serving substrate into which many LLM-based methods are inserted.

## What language models add

Language models add four capabilities that classical ID recommenders do not naturally have.

- **Semantic abstraction.** A product title, review, query, image caption, video transcript, or user self-description can be mapped into a space where cold-start and cross-domain transfer become easier.

- **Instruction following.** Recommendation tasks can be expressed as prompts: predict whether a user will like an item, rank a candidate list, explain a recommendation, ask a clarifying question, or generate a search query.

- **World knowledge and reasoning.** LLMs can infer seasonal intent, substitute/complement relations, event-driven preferences, and high-level attributes not explicitly present in interaction logs.

- **Text generation and interaction.** LLMs can produce explanations, summaries, conversational turns, synthetic user profiles, and natural-language critiques of recommendation results.

At the same time, recommenders impose requirements that general LLMs do not satisfy by default: calibrated scores, low latency, huge catalogs, frequent item churn, counterfactual evaluation, business constraints, and stable online experimentation. Much of the literature can be read as attempts to reconcile these two worlds.

# A Taxonomy of Large-Model Recommendation

## LLM as feature engineer

The simplest and most deployable role is feature engineering. A frozen or lightly tuned LLM extracts item tags, user profiles, intent summaries, review aspects, query rewrites, graph edges, or synthetic samples. Examples include TagGPT, LLM4KGC, KAR, HKFR, RLMRec, LLMRec with graph augmentation, CUP, SINGLE, LLMHG, Llama4Rec, ONCE, MINT, RecPrompt, BEQUE, and Agent4Ranking. The model is not asked to score every candidate online; it generates artifacts that can be cached and consumed by conventional retrieval or ranking systems.

This is why LLM-as-enhancer is often industrially attractive. It localizes risk. If the generated attribute is noisy, the downstream ranker can learn to ignore it; if the LLM is expensive, generation can run offline; if a policy rule changes, the feature pipeline can be audited separately.

## LLM as encoder

Pre-trained language models can encode text-rich items and user histories. This line starts before the current LLM wave: U-BERT, UNBERT, PLM-NR, Pyramid-ERNIE, ERNIE-RS, CTR-BERT, Tiny-NewsRec, RecFormer, UniSRec, VQ-Rec, MISSRec, PMMRec, and many news, job, software, and tourism recommenders. Later work adds larger LLM embeddings, instruction-tuned encoders, or adapters.

Encoder approaches fit industrial stacks because embeddings can be precomputed, indexed, distilled, and combined with ID embeddings. Their limitation is that they often capture content similarity better than collaborative preference. This is the semantic-collaborative gap that motivates CoLLM, LLaRA, A-LLMRec, LLM2BERT4Rec, LC-Rec, ControlRec, and related alignment methods.

## LLM as scorer or ranker

Another line turns recommendation into language classification or ranking. TALLRec expresses user history and a candidate item as an instruction and asks the LLM to answer yes/no. InstructRec and RecRanker use instruction tuning. SetwiseRank and listwise LLM rankers use comparative prompting to rank candidate sets. ReLLa retrieves relevant behavior snippets before prompting an LLM, while LlamaRec uses a two-stage retrieval-then-rank design. These systems are attractive for controllability and cold-start reasoning, but raw LLM scoring is usually too slow and poorly calibrated for large industrial ranking.

## LLM as generator

Generative recommendation treats the output item, item ID, semantic ID, query, explanation, or slate as a generated sequence. P5 and M6-Rec framed multiple recommendation tasks as language processing. GPT4Rec, GenRec, BIGRec, PALR, LightLM, LLaRA, LC-Rec, IDGenRec, TIGER, and many semantic-ID systems extend this idea. The key design question is the output vocabulary: textual item titles are human-readable but ambiguous and hard to ground; numeric IDs are precise but semantically empty; semantic IDs offer a compact compromise.

## Large recommendation models and sequential transducers

Not all large recommendation models are LLMs. Meta’s HSTU-based Generative Recommenders reformulate industrial recommendation as sequential transduction over user actions and scale to 1.5 trillion parameters, reporting a 12.4% online A/B improvement and power-law scaling with compute . Meituan’s MTFM builds a multi-scenario recommendation foundation model with heterogeneous tokens . These models borrow from the language-model scaling playbook but are trained on action streams, sparse IDs, and recommender objectives.

## Agentic and conversational recommenders

Agentic recommenders use LLMs for planning, tool use, memory, self-reflection, or multi-agent collaboration. Chat-REC and conversational systems explore interactive recommendation. MACRec, AgentCF, iAgent, RecMind, RecGPT-V2, MMEACR, LLM-as-a-judge slate recommenders, and connected-TV agentic systems extend this direction. The promise is richer preference elicitation and better explanations. The industrial challenge is predictable behavior, latency, user safety, and evaluation.

# Core Academic Milestones

## P5 and the text-to-text unification idea

P5, or Pretrain, Personalized Prompt, and Predict, was a milestone because it made the argument that recommendation tasks can be unified as text-to-text learning . Rating prediction, sequential recommendation, explanation generation, review summarization, and direct recommendation can share the same language-model objective. P5 did not solve industrial serving, but it changed how researchers thought about task unification.

## M6-Rec and open-ended industrial pretraining

M6-Rec extended a large generative pre-trained language model to recommendation and argued that industrial recommenders need open-ended support for multiple domains, tasks, and modalities . It converted recommendation tasks into language understanding or generation tasks and emphasized sample-efficient downstream adaptation. It is an important bridge between academic LLM4Rec and industrial foundation models.

## TALLRec and instruction tuning for preference prediction

TALLRec demonstrated that LLaMA-style instruction tuning with LoRA can align an LLM to recommendation data . Its yes/no formulation is simple but influential. It also exposed a recurring limitation: language-model semantics and collaborative preference are not the same thing. Later methods improve this with collaborative embeddings, retrieval augmentation, rationale distillation, or semantic IDs.

## TIGER and semantic-ID generative retrieval

TIGER, “Recommender Systems with Generative Retrieval,” reframed retrieval as generating item identifiers . Instead of nearest-neighbor search over embeddings, the model decodes a semantic ID learned from item content. This idea inspired a large family: P5-ID, LC-Rec, IDGenRec, LETTER, RPG, differentiable semantic IDs, variable-length semantic IDs, SIDInspector, PLUM, SIGMA, AKT-Rec, and Gryphon. The central questions are collision, validity, calibration, cold-start generalization, and efficient constrained decoding.

## Collaborative alignment methods

CoLLM, LLaRA, A-LLMRec, LC-Rec, ControlRec, CLLM4Rec, and related methods try to inject collaborative signals into language models. They differ in mechanism: projection of collaborative embeddings into token space, adapters, item token learning, contrastive alignment, or two-stage grounding. This family exists because pure text semantics often fails on behavior-driven preference.

## RAG and long-history understanding

ReLLa and RALLRec show that LLMs need retrieval to handle lifelong behavior. Long user histories contain both signal and noise. A retrieval step selects relevant behaviors before prompting or encoding. AIR, RecGPT-V2, and RecGPT-Mobile industrialize a similar insight: compress the user’s history into task-relevant intent representations before ranking.

## Evaluation, fairness, and robustness

Recent work studies whether LLM recommenders are stable, fair, calibrated, and controllable. STELLA argues that LLM recommenders can be unstable. FaiRLLM, RECLLM, fairness surveys, provider fairness studies, job recommendation bias analyses, and demographic bias studies show that LLMs inherit and sometimes amplify social and popularity biases. LBR, submitted in July 2026, targets length bias in LLM-based recommendation. LLM-based offline evaluation and controllability-centric agent evaluation show that evaluation itself is changing.

# Industrial Systems with Public Online Evidence

Table <a href="#tab:ab" data-reference-type="ref" data-reference="tab:ab">1</a> summarizes industrial cases where public sources disclose online A/B or live-experiment metrics. These results should not be compared as if they were from one benchmark. They differ in traffic, baseline maturity, product surface, metric definitions, and time horizon. Still, they show which patterns have crossed the production barrier.


| System | Platform | Large-model role | Public online result | Source |
|:---|:---|:---|:---|:---|
| System | Platform | Large-model role | Public online result | Source |
| HSTU / Generative Recommenders | Meta large internet platform | Sequential transduction architecture for retrieval/ranking over action streams. | 1.5T-parameter GRs report **+12.4%** online A/B topline improvement; HSTU is 5.3x–15.2x faster than FlashAttention2 Transformers on 8192-length sequences. |  |
| ReLand | Alipay | LLM insights injected through a controllable reasoning pool. | Deployed since Jan. 2024; **+3.19% CTR** and **+1.08% CVR**. |  |
| LLM-KERec | Alipay | Inferential knowledge graph built with LLM assistance. | One-month A/B with 10% traffic: **+6.24%** conversion, **+6.45% GMV**, **+10.07%** conversion across three scenarios. |  |
| MTFM | Meituan | Multi-scenario recommendation foundation model. | SQS: **+1.89% CTR**, **+2.46% UV_CTCVR**, **+2.98% orders**, **-5 ms**. PHF: **+1.53% CTR**, **+1.03% UV_CTCVR**, **+1.45% orders**, **-6 ms**. |  |
| SIGMA | AliExpress | Semantic-grounded instruction-driven generative multi-task recommender. | Two-week A/B with 5% traffic: **+2.80% order volume**, **+3.84% conversion**, **+7.84% GMV**, **+2.47% purchased category breadth**. |  |
| SORT-Gen | Taobao | Generative list-level multi-objective re-ranking. | Two-week A/B on Baiyibutie: **+4.13% CLICK** and **+8.10% GMV**. |  |
| AIR | Kuaishou | Offline LLM atomic intents with online target-aware retrieval. | 5.08% traffic: **+1.043% paid orders**, **+3.446% GMV**, **+3.662% GPM**, **+1.254% OPM**; about 400x throughput gain over direct LLM invocation. |  |
| Taiji | Kuaishou Ads | LLM-as-enhancer with preference reasoning and Pareto reward alignment. | One-week A/B, 10%/10% split: **+2.83% ADVV**, **+3.30% revenue**; long-tail users **+5.26% ADVV**, **+5.32% revenue**. |  |
| PLUM | YouTube | Gemini-family pre-trained LM adapted to semantic-ID generative retrieval. | Live experiments adding PLUM over LEM+: LFV **+0.76% panel CTR**, **+0.80% views**; Shorts **+4.96% panel CTR**, **+0.39% views**; satisfaction positive. |  |
| AKT-Rec | Tmall | MLLM/LLM semantic IDs with asymmetric head-to-tail transfer. | Two-week A/B, 10%/10% split: **+2.73% clicks**, **+2.76% CTR**, **+1.7% CTCVR**, **+3.47% GMV**. |  |
| RecGPT | Taobao | Hundred-billion-scale intent-centric reasoning model. | Public summaries report online **+9.47% IPV** and **+6.33% CTR**, with diversity and merchant-side benefits. |  |
| RecGPT-V2 | Taobao | Hierarchical multi-agent intent reasoning and agentic judge/reward. | Two-week A/B against RecGPT-V1. Item scenario reports **+3.64% IPV**, **+3.01% CTR**, **+3.39% GMV**, **+3.47% ATC**, **+11.46% NER**. |  |

Public industrial online evidence for large-model recommendation.

# Industrial and Production-Oriented Systems without Full Public A/B

Many important industrial systems do not disclose public A/B metrics. They still shape the field because they describe architecture, training pipelines, system bottlenecks, and deployment assumptions.

- **M6-Rec and M6-like e-commerce foundation models** argue for unified generative modeling across product, content, and user-generated domains.

- **BEQUE and Taobao query rewriting** show how LLMs can generate long-tail query rewrites for search/recommendation, often as offline or nearline expansions.

- **RecGPT-Mobile** moves a lightweight intent agent onto the user device, preserving privacy and immediacy while leaving large retrieval/ranking in the cloud.

- **Large Language Model as Universal Retriever** explores whether one LLM-based retriever can serve multiple industrial retrieval objectives.

- **Gryphon** adds item-level scoring to semantic-ID generation in an industrial music service, addressing sequence-score calibration and SID collisions.

- **RecBase, OneMall, GPR, RankGR, and related large recommender models** aim to pretrain or align one model across multiple recommendation surfaces, though public online evidence varies.

- **Meta GEM and ads foundation-model discussions** suggest a move toward shared ads recommendation backbones and accelerated experimentation, but public third-party blog claims should be treated as contextual unless paired with primary technical reports.

- **Google/YouTube product and research announcements** around Gemini and creator/advertiser matching show how multimodal foundation models are entering adjacent recommendation-like matching tasks; PLUM remains the clearest public technical evidence for YouTube recommendation A/B impact.

# Technical Themes

## Semantic IDs and the discrete bottleneck

Semantic IDs solve one problem while creating several new ones. They compress rich item semantics into a short discrete code that can be generated by an autoregressive model. This makes retrieval look like language decoding and enables zero-shot or cold-start generalization when the ID is tied to content. But codes can collide, become unbalanced, overfit to modality artifacts, or produce invalid outputs. Recent work responds with residual quantization, learnable item tokenization, differentiable semantic IDs, variable-length IDs, unordered long IDs, parallel decoding, qualification-aware collision handling, adaptive collision handling, and diagnostic resources such as SIDInspector.

## Collaborative signal alignment

LLMs know language; recommenders know behavior. Alignment methods try to prevent one from washing out the other. Some methods project collaborative embeddings into language-model token space. Others train adapters or LoRA modules. Some use contrastive objectives to align item texts with co-clicks. Semantic-ID methods often build the ID from both content and collaborative signals. Industrial systems such as PLUM and AKT-Rec show that this alignment is not optional: content-only semantics is rarely enough for high-stakes recommendation.

## Long histories and memory

Large context windows do not automatically solve lifelong behavior modeling. User histories include stale, contradictory, accidental, and context-dependent interactions. ReLLa, RALLRec, AIR, RecGPT-V2, RecGPT-Mobile, HLLM-style hierarchical methods, and MMEACR-style multimodal memory agents all reflect the same insight: retrieve and compress the relevant parts of history before the large model or ranker sees them.

## Reranking, slate optimization, and multi-objective learning

Large models are useful beyond top-1 relevance. SORT-Gen models list-level multi-objective re-ranking. LLM-based diversity re-ranking and explanation-aware re-ranking optimize properties of the whole slate. RecGPT-V2 includes novelty exposure rate. SIGMA includes purchased category breadth. Taiji balances semantic and collaborative reward. The research frontier is moving from item scoring toward controllable slate generation under business constraints.

## Multimodal recommendation

Modern items are multimodal: product images, titles, reviews, videos, audio, transcripts, comments, creator metadata, and live-stream context. VIP5, MM-Rec, MISSRec, PMMRec, LLMs in multimodal recommender surveys, AKT-Rec, PLUM, and MMEACR all show different ways to combine modalities. The hard part is not simply using a vision-language model; it is deciding which modality should dominate under which user intent and how to keep multimodal features fresh and policy-safe.

## Agents, interaction, and user simulators

Agentic recommenders can ask questions, revise assumptions, call tools, simulate users, critique slates, and maintain memory. Agent4Rec, RecMind, MACRec, AgentCF, iAgent, MMEACR, LLM-based group recommenders, connected-TV agents, and LLM-as-a-judge evaluation systems show this shift. The main risk is that agents are harder to evaluate than rankers. A ranker returns a score; an agent may change the user’s preference statement, ask a question, or hallucinate a constraint.

# Problem-Oriented Reading Guide

The literature is easier to navigate when organized by the problem a practitioner or researcher is trying to solve. The same model family can be appropriate in one setting and wasteful in another.

## Cold start and long tail

Cold-start and long-tail settings are the most natural entry point for LLMs. Traditional ID embeddings are weak when an item has few exposures or a user has little history. Content-rich LLM representations, semantic IDs, and multimodal encoders can transfer information from item titles, product images, descriptions, reviews, transcripts, and co-occurring entities. In this setting, the most relevant works include P5, M6-Rec, TIGER, UniSRec, VQ-Rec, MISSRec, PMMRec, AKT-Rec, PLUM, GenCDR, and semantic-ID diagnostics. The industrial lesson is to avoid content-only features as a final answer: cold-start content semantics should be fused with whatever collaborative evidence is available, even if it is weak. AKT-Rec is important because it explicitly avoids harming head IDs while helping tail IDs; this is a common production concern because improving the tail at the expense of head traffic can reduce total business value.

## Cross-domain transfer

Cross-domain recommendation benefits from LLMs when domains have semantic overlap but sparse direct interactions. Examples include content-to-commerce, search-to-recommendation, short-video-to-product, and query-to-item transfer. AIR, SIGMA, MTFM, S&R Foundation, Uni-CTR, PCDR, and GenCDR illustrate different solutions. A practical design choice is whether to align domains into a shared embedding space, a shared semantic-ID vocabulary, a shared user-intent memory, or a shared multi-scenario transformer. Shared representations improve transfer, but can also create negative transfer when domains optimize different objectives. Production systems therefore often use mixture, gating, adapters, or scenario-specific subgraphs rather than a single unconditioned representation.

## Text-rich and multimodal items

News, e-commerce, local services, jobs, short videos, music, books, and creator/advertiser matching are text-rich or multimodal. PLM-NR, MM-Rec, VIP5, MISSRec, PMMRec, PLUM, AKT-Rec, and MMEACR are representative. For these scenarios, LLMs and MLLMs are valuable not only because they produce better item embeddings, but because they expose interpretable attributes: topic, brand, style, seasonality, audience, intent, safety category, and substitutability. This interpretability matters in industry because recommendation teams need debugging handles. A black-box embedding may improve NDCG; a generated attribute can explain why a model started over-serving a trend or under-serving a merchant class.

## Ads and commercial recommendation

Ads recommendation has stronger calibration, auction, and multi-stakeholder constraints than many organic recommendation tasks. A ranking model must estimate action probabilities and values, not merely choose semantically plausible items. This is why LLMs appear first as feature producers or alignment modules in ads systems. Taiji reports ADVV and revenue gains, while HSTU and GEM-like discussions point toward large shared backbones for ads ranking. In ads, an LLM-generated candidate or explanation is insufficient unless it can be tied to calibrated advertiser value, budget pacing, policy constraints, and user experience guardrails. The right question is not whether an LLM can understand an ad, but whether its semantic signal improves calibrated value prediction without destabilizing the marketplace.

## Short-video and feed recommendation

Short-video and feed systems combine rapid trends, multimodal content, creator ecosystems, long user histories, and high feedback volume. HSTU, PLUM, AIR, RecGPT, RecGPT-Mobile, and related systems are important here. These systems show two opposite but compatible directions: very large action-sequence models that learn directly from behavior, and semantic-intent systems that compress content and context. The practical architecture may use both: a high-throughput action model for the main ranking signal and LLM-derived intent or content features for cold-start, diversity, explanation, or cross-domain transfer.

## Conversational and agentic recommendation

Conversational recommendation is not only “chat plus ranking.” A conversational system must decide when to ask, when to recommend, how to remember, how to recover from wrong assumptions, and how to ground recommendations in available inventory. Chat-REC, RecMind, MACRec, AgentCF, iAgent, MMEACR, RecGPT-V2, and CTV agentic recommendation illustrate the design space. For production, the hardest issue is evaluation. An agent can produce a fluent dialogue while steering the user toward unavailable or unsafe items. Grounding, tool constraints, and audit logs are therefore as important as model quality.

## Evaluation and user simulation

LLM-as-judge and user-simulation systems are attractive because online A/B tests are expensive. But they should be treated as pre-A/B filters, not replacements for real traffic. A simulator can test whether a system follows constraints, whether an explanation is coherent, whether generated IDs are valid, and whether a slate satisfies a known preference profile. It cannot reliably estimate long-term retention, marketplace dynamics, creator incentives, or fatigue without calibration against real user behavior. The best use of LLM evaluation is layered: offline labels and counterfactual estimators, LLM-based diagnostic judgments, small-scale human review, shadow traffic, then controlled online experiments.

# Deep Dives on Representative Paradigms

## Instruction-tuned LLM recommenders

Instruction-tuned recommenders such as TALLRec and InstructRec are conceptually simple: convert recommendation data into instruction-response pairs and fine-tune an LLM. Their strength is flexibility. The same model can answer whether a user likes an item, explain the choice, or adapt to a natural-language constraint. Their weakness is that recommendation labels are not naturally language labels. A yes/no answer may be easy to train but hard to calibrate as CTR or CVR. The candidate set may also be artificially small in offline experiments. In production, instruction-tuned LLM rankers are more plausible as rerankers, weak-user specialists, explanation modules, or feature generators than as the primary scorer for millions of candidates.

This paradigm is still important because it established the data interface between recommender logs and LLM training. Once user histories and item metadata are serialized into instructions, one can add rationales, retrieved behaviors, collaborative embeddings, business constraints, or safety rules. Much of the later literature can be understood as improving the naive instruction template: better grounding, better collaborative alignment, better retrieval, better output constraints, or better distillation.

## Semantic-ID generative retrieval

Semantic-ID retrieval is one of the most distinctive LLM-era ideas. It changes the retrieval problem from “score all items or search nearest neighbors” to “generate a discrete code that maps to items.” This creates an elegant connection to language modeling but raises several design choices.

First, how should IDs be constructed? Content-only IDs generalize to new items but may ignore collaborative behavior. Collaborative IDs capture behavior but struggle with cold start. Hybrid IDs try to use both. Second, should IDs be fixed or learned end-to-end? Fixed IDs stabilize the target vocabulary, while differentiable or learnable IDs can adapt to task objectives. Third, how should collisions be handled? A collision can be useful if it groups substitutes, but harmful if it merges unrelated items. Fourth, how should decoding be constrained? Unconstrained generation can produce invalid IDs; prefix trees, sparse transition matrices, or post-verification are needed at scale. Fifth, how should generated IDs be scored? Accumulated token likelihood may not equal item relevance, motivating systems such as Gryphon that add item-level scoring.

The industrial significance of semantic IDs is that they make language-model-style generation compatible with retrieval infrastructure. PLUM demonstrates this at YouTube scale; SIGMA and AKT-Rec show related ideas in e-commerce. The remaining question is whether semantic-ID generation can consistently beat strong approximate nearest-neighbor retrieval after accounting for freshness, invalid outputs, and serving cost.

## LLM-as-enhancer and semantic feature stores

LLM-as-enhancer systems are likely to remain the most common industrial pattern. The LLM produces a semantic artifact; a conventional recommender consumes it. This pattern includes user profiles, item attributes, query rewrites, graph edges, atomic intents, explanations, reward features, and semantic IDs. It works because it respects the existing production stack. Feature stores, rankers, monitors, and A/B platforms do not need to be redesigned around free-form generation.

However, LLM-generated artifacts require their own lifecycle. They need schema definitions, freshness policies, validation rules, drift monitors, backfills, and rollback mechanisms. If a product taxonomy changes, a generated tag can become stale. If a prompt changes, feature distributions can shift. If the LLM provider changes, downstream model calibration can move. Treating semantic artifacts as ordinary features is not enough; they are generated features with prompt and model provenance.

## Recommendation-native foundation models

HSTU and MTFM show a different route: instead of adapting a general LLM, build a large model around recommendation data. This route is attractive when the platform has massive action logs and enough infrastructure to train and serve very large models. It avoids some semantic-collaborative mismatch because the model is trained directly on behavior. It also preserves the possibility of scaling laws over recommendation compute.

The cost is engineering complexity. Recommendation-native foundation models must handle high-cardinality sparse features, non-stationary item vocabularies, streaming updates, long histories, multi-objective labels, and low-latency serving. HSTU introduces architectural changes and inference amortization; MTFM uses heterogeneous tokens and scenario-specific subgraphs. These models are closer to building a new recommender platform than adding an LLM component.

## Agentic recommenders

Agentic recommenders are appealing because they can represent a user’s task, not only the user’s historical clicks. A shopping user may say, “I need a gift for a colleague under a budget,” and an agent can ask clarifying questions, retrieve candidates, reason about constraints, and explain trade-offs. RecGPT-V2 brings this idea into Taobao-style feed recommendation through hierarchical expert agents. MMEACR and connected-TV agents show how memory and multimodal context can be added.

The main research challenge is that agentic recommendation blurs the boundary between recommendation, search, dialogue, and decision support. The main industrial challenge is safety. An agent that interacts with users can manipulate preferences, over-personalize, hallucinate availability, reveal private inferences, or create inconsistent experiences. Agentic systems need grounded tools, bounded action spaces, conversation policies, and evaluation beyond ranking metrics.

# How to Read Blogs, Technical Reports, and Vendor Claims

The user specifically asked to include official technology blogs such as Google or Meta where useful. These sources are valuable but must be read differently from peer-reviewed or arXiv papers. This survey uses four evidence grades.

1.  **Primary technical paper with online metrics.** Example: HSTU, PLUM, MTFM, SIGMA, AIR, Taiji, AKT-Rec. These can support claims about online gains, while still requiring attention to baseline and metric definitions.

2.  **Primary technical report or product paper without complete online disclosure.** Example: some RecGPT, RecGPT-Mobile, large retriever, or foundation-model reports. These can support architecture claims but not necessarily quantified business impact.

3.  **Official company blog.** Useful for product context, deployment framing, and strategic direction. Blogs often omit baselines, traffic splits, statistical tests, and guardrails, so they should not be the sole source for precise A/B claims unless they provide enough experimental detail.

4.  **Third-party blog or commentary.** Useful for interpretation and discovery, but claims must be traced back to primary sources before being treated as evidence. For example, third-party posts about YouTube semantic IDs or Meta GEM help identify trends, but the survey should ground quantitative claims in PLUM or HSTU-style primary documents.

This evidence discipline matters because recommendation is unusually sensitive to metrics. A 0.5% lift on a huge surface can be valuable; a 5% lift on a weak offline subset may disappear online. Without traffic allocation, duration, baseline, and guardrails, a headline number is not enough.

# Why Many Academic LLM4Rec Methods Do Not Directly Land Online

Many academic LLM recommender papers are useful but not deployable as written. The gap is not a lack of creativity; it is a mismatch between benchmark assumptions and production constraints.

**Candidate-set size.** Many LLM ranker experiments rank tens or hundreds of candidates. Industrial retrieval and ranking may consider millions or billions of items across stages. Methods that call an LLM per candidate rarely survive this scale.

**Label semantics.** Offline datasets often treat observed interactions as positives and sampled items as negatives. In production, unobserved items may be unseen, unavailable, policy-blocked, already consumed, or simply not exposed. LLM evaluation can make this worse if it judges semantic plausibility rather than actual user response.

**Temporal leakage.** LLMs are pretrained on public corpora and may know item popularity or descriptions from after the training period of a benchmark. Recommendation benchmarks need careful temporal splits and leakage checks.

**Catalog grounding.** A generated title is not a recommendation unless it maps to an available item. Academic text-generation metrics often ignore inventory, duplicates, seller constraints, price changes, and regional availability.

**Latency and cost.** A method that improves NDCG with a 7B model may be unusable if it adds tens of milliseconds to a critical ranking path. Industrial papers that report latency or throughput are therefore especially valuable.

**Guardrails.** CTR or NDCG can improve while diversity, satisfaction, fairness, creator exposure, or policy safety deteriorates. Real deployments need multi-metric scorecards.

**Operational drift.** Prompts, LLM versions, taxonomy definitions, item catalogs, and user behavior all drift. A generated feature pipeline must be monitored like a model, not like static metadata.

# Recommended Evaluation Protocol

A robust evaluation protocol for LLM-enhanced recommendation should be staged.

1.  **Artifact validation.** Check generated tags, semantic IDs, query rewrites, and intent summaries for validity, coverage, safety, and drift.

2.  **Offline ranking evaluation.** Use temporal splits, multiple negative sampling schemes, and segment-level metrics for cold-start, long-tail, new users, and heavy users.

3.  **Counterfactual and replay checks.** Use inverse propensity or doubly robust estimators where logging propensities are available; avoid treating missing exposure as negative preference.

4.  **LLM diagnostic evaluation.** Use LLM judges only for bounded checks such as explanation coherence, constraint satisfaction, and semantic coverage. Calibrate these judgments against human and behavioral data.

5.  **Shadow deployment.** Run the model on live traffic without affecting exposure to measure latency, invalid outputs, feature drift, and candidate overlap.

6.  **Online A/B.** Start with small traffic, clear guardrails, and segment analysis. Include business metrics, user metrics, ecosystem metrics, and system metrics.

7.  **Long-term holdout.** Measure retention, fatigue, diversity, creator/merchant health, and policy outcomes over longer windows.

The key principle is that LLM-specific evaluation should add gates, not remove the need for online experimentation. A recommender changes user behavior and ecosystem incentives; only live experiments can measure the full feedback loop.

# Evaluation: Offline, Online, and LLM-as-Judge

Offline recommendation evaluation is already difficult because missing labels are not negative labels. LLMs add new complications: prompt order sensitivity, output-format failures, invalid item generation, position bias, length bias, popularity bias, hallucination, and preference drift. Recent work proposes LLM-based preference induction for offline top-N evaluation, A/B agents, user simulators, controllability-centric evaluation with collaborative agents, and LLM-as-a-judge for slate recommendation.

These tools are useful, but they should not replace online experiments. They are best treated as intermediate gates: useful for catching invalid outputs, unsafe explanations, poor diversity, or obvious preference mismatch before exposing users to a system. Online A/B remains the standard for business impact, and long-term holdouts remain necessary for retention and ecosystem health.

# Deployment Patterns

## Offline large-model artifact generation

The safest deployment pattern is offline artifact generation. LLMs generate tags, semantic IDs, intent summaries, user profiles, graph edges, or synthetic samples. These artifacts are validated, cached, and used by conventional rankers. ReLand, LLM-KERec, AIR, AKT-Rec, and many feature-engineering papers follow this route.

## Nearline and incremental inference

Nearline inference updates features or candidates every few minutes or hours. SIGMA aggregates users’ latest behaviors at minute-level intervals and uses incremental inference with cached KV states. This pattern improves freshness without putting full LLM inference into every request.

## Candidate-pool augmentation

PLUM adds generated candidates to the existing YouTube retrieval pool rather than replacing the whole retrieval stack. This is a common production strategy: introduce a new retriever as one channel, control its quota, and let downstream rankers and guardrails determine final exposure.

## On-device intent agents

RecGPT-Mobile points to a privacy-preserving future: a small on-device LLM summarizes immediate context or predicts the next query, while the cloud handles global retrieval and ranking. This reduces server cost and privacy risk, but creates model update, device heterogeneity, and safety challenges.

## Full large recommender models

HSTU and MTFM show that large-scale recommendation-native models can produce online gains. They require deep systems work: attention variants, feature tokenization, micro-batching, cache reuse, subgraph serving, distributed training, and monitoring. These are not simple LLM API integrations.

# Risks and Failure Modes

- **Semantic-collaborative mismatch.** A language model may recommend semantically plausible items that users do not click or buy.

- **Calibration failure.** LLM probabilities or token scores are not calibrated CTR/CVR/GMV estimates.

- **Invalid generation.** Generated item IDs, semantic IDs, or titles may not map to available catalog items.

- **Popularity and exposure bias.** LLMs may reproduce common web popularity or platform exposure patterns.

- **Length and position bias.** Longer item descriptions, longer prompts, or earlier candidate positions can receive unfair advantage.

- **Privacy leakage.** User summaries and explanations may expose sensitive behavior.

- **Safety and policy drift.** Generated explanations or query rewrites can violate policy even when the underlying item is safe.

- **Staleness.** Offline semantic artifacts can become stale when products, trends, or user contexts change.

- **Cost opacity.** Offline AUC gains can disappear when model latency, GPU cost, or index refresh cost is included.

# A Practical Playbook

For a team building an LLM-enhanced recommender, the evidence suggests the following sequence.

1.  Identify the bottleneck: cold start, long tail, cross-domain transfer, content understanding, search-query generation, slate diversity, explanation, or long-history compression.

2.  Choose the large-model role: artifact generator, encoder, scorer, candidate generator, reranker, judge, reward model, simulator, or agent.

3.  Convert LLM output into recommender-native objects: embeddings, semantic IDs, item tags, graph edges, generated candidates, intent memories, or reward features.

4.  Keep a strong production baseline and introduce the large-model component as an augmenting channel first.

5.  Validate invalid-output rate, hallucination, policy safety, calibration, diversity, and latency before A/B.

6.  Run online A/B with target metrics and guardrails. Segment long-tail, cold-start, new users, heavy users, creators/merchants, and safety-sensitive categories.

7.  Preserve long-term holdouts or delayed metrics for retention, satisfaction, and ecosystem health.

# Open Problems

**Unified reporting.** Public industrial papers should report traffic split, duration, baseline maturity, target metrics, guardrails, latency, cost, and segment effects. Without this, A/B results are hard to interpret.

**Semantic cache freshness.** Offline LLM artifacts are cheap at serving time but can become stale. Systems need freshness-aware semantic caches and update policies.

**Score calibration.** Generative likelihoods, LLM judgments, and semantic rewards must be mapped to business-calibrated scores.

**Constrained decoding at scale.** Generative retrieval needs fast prefix constraints, validity checks, and collision handling for billion-item catalogs.

**Long-term value.** Short-term CTR can conflict with retention, trust, merchant fairness, creator health, and content diversity.

**On-device recommendation.** Local intent agents may improve privacy and immediacy, but they introduce device resource limits and distributed safety concerns.

**LLM-based evaluation.** LLM judges can expand labels and simulate users, but they must be calibrated against real behavior and not become circular evaluators of LLM recommenders.

# Conclusion

The field is no longer about whether LLMs can recommend. They can, but raw LLM recommendation is rarely the industrial answer. The stronger conclusion is that large models become useful when their semantic, generative, multimodal, or reasoning capabilities are converted into controllable recommender-system objects. The most convincing public deployments either augment the existing stack with LLM-derived artifacts or build recommendation-native large models with careful serving design. Academic work continues to expand the design space, especially in semantic IDs, collaborative alignment, agentic interaction, fairness, and evaluation. The next major progress will likely come from systems that combine these ideas: foundation-scale user/action models, grounded semantic IDs, real-time intent memory, calibrated business objectives, and evaluation protocols that measure long-term ecosystem value rather than only short-term clicks.

# Paper and System Map

This appendix is a structured map rather than an exhaustive bibliography. It groups more than two hundred related works, systems, and technical reports by their primary contribution. Many works belong to multiple categories; they are placed where they are most useful for navigation.

## Classical and Pre-LLM Neural Recommendation Foundations

| Cluster | Representative works | Why they matter |
|:---|:---|:---|
| Cluster | Representative works | Why they matter |
| Industrial retrieval and ranking | Wide&Deep; DeepFM; YouTube DNN; DLRM; Monolith; PinnerSage; PinnerFormer; MIND; ComiRec; TwinBERT; DSSM; TDM/JTM | Define multi-stage retrieval/ranking, sparse feature interaction, large embedding tables, and serving constraints that LLM methods must integrate with. |
| Interest modeling | DIN; DIEN; DSIN; SIM; ETA; MIMN; M2GRL; BST; MIND; HPMN | Establish target attention, evolving interests, session dynamics, and long-history compression before LLMs. |
| Sequential recommendation | GRU4Rec; Caser; SASRec; BERT4Rec; S3-Rec; CL4SRec; DuoRec; FDSA; FEARec; RecFormer | Provide the transformer sequence modeling foundation that later generative recommenders scale. |
| Multimodal and content recommendation | VBPR; MMGCN; GRCN; LATTICE; MM-Rec; MISSRec; PMMRec; CLIP4Rec; VIP5 | Show how images, text, audio, and metadata support cold-start and cross-domain transfer. |
| Knowledge and graph recommendation | RippleNet; KGAT; KGIN; KGCN; LightGCN; PinSage; GraphRec; HKFR; KG-enhanced conversational recommenders | Prefigure LLM knowledge extraction and graph augmentation. |
| Conversational recommendation | ReDial; TG-ReDial; KBRD; CR-Walker; UniCRS; MESE; TCP; C2-CRS; Chat-REC | Provide interaction protocols and evaluation concerns for agentic recommendation. |

## LLM for Feature Engineering and Data Augmentation

| Subtopic | Representative works | Summary |
|:---|:---|:---|
| Subtopic | Representative works | Summary |
| User/item feature augmentation | LLM4KGC; TagGPT; ICPC; KAR; PIE; LGIR; GIRL; LLM-Rec; HKFR; LLaMA-E; EcomGPT; TF-DCon; RLMRec; LLMRec; LLMRG; CUP; SINGLE; SAGCN; UEM; LLMHG; Llama4Rec; LLM4Vis; LoRec | LLMs extract tags, aspects, user interests, knowledge, and concise profiles. The output is usually cached and passed to conventional models. |
| Sample and query generation | GReaT; ONCE; AnyPredict; DPLLM; MINT; Agent4Rec; RecPrompt; PO4ISR; BEQUE; Agent4Ranking; PopNudge; RecInter | LLMs generate synthetic interactions, narrative preferences, long-tail query rewrites, or simulated interactions. |
| Knowledge extraction | KAR; TRAWL; HKFR; LLM-KERec; ReLand; LLMRG; LlamaRec-LKG-RAG; LKPNR; DOKE | The LLM is used as a knowledge producer rather than a direct ranker. |
| Industrial artifact generation | ReLand; LLM-KERec; AIR; AKT-Rec; Taiji; RecGPT; RecGPT-Mobile | The strongest production pattern: generate or compress semantic artifacts offline/nearline, then serve with standard retrieval/ranking infrastructure. |

## LLM and PLM Encoders for Recommendation

| Subtopic | Representative works | Summary |
|:---|:---|:---|
| Subtopic | Representative works | Summary |
| Text-rich item encoding | U-BERT; UNBERT; PLM-NR; Pyramid-ERNIE; ERNIE-RS; CTR-BERT; SuKD; PREC; Tiny-NewsRec; PLM4Tag; TwHIN-BERT; RecFormer; TBIN; Social-LLM | Encoders improve item/user representation when metadata and text are central. |
| Cross-domain and transferable encoders | ZESRec; UniSRec; TransRec; VQ-Rec; IDRec vs MoRec; S&R Foundation; MISSRec; UFIN; PMMRec; Uni-CTR; PCDR | Use language or multimodal embeddings to transfer across domains and cold-start scenarios. |
| LLM embeddings and adapters | LLM2BERT4Rec; LLM4ARec; UEM; CollabContext; SSNA; KERL; LLMRS; LLMHG; HLLM; HLLM-style item/user hierarchies | Use frozen embeddings, adapters, or hierarchical LLMs to represent user histories and item content. |
| Industrial encoders | PLUM item semantic representations; AKT-Rec MLLM semantic clusters; MTFM heterogeneous tokens; Meta HSTU action tokens | The encoder is redesigned around production data streams, not only natural language. |

## LLM Scoring, Ranking, and Instruction Tuning

| Subtopic | Representative works | Summary |
|:---|:---|:---|
| Subtopic | Representative works | Summary |
| Prompted scoring and rankers | LMRecSys; Zero-shot GPT; BookGPT; PALR; LLMRanker; SetwiseRank; LiT5; LlamaRec; LLM4Rerank; LLM as explainable re-ranker | Use LLMs to score or rank candidate sets; strong for analysis and small candidate pools, costly for full ranking. |
| Instruction tuning | TALLRec; InstructRec; GenRec; BIGRec; DEALRec; RecRanker; Recommendation as Instruction Following; Aligning LLMs with Recommendation Knowledge; RDRec | Align LLMs to recommendation labels and tasks through instructions, LoRA, or distillation. |
| Collaborative alignment | CoLLM; LLaRA; A-LLMRec; CLLM4Rec; LC-Rec; ControlRec; FLIP; ClickPrompt; Llama4Rec; iLoRA; CALRec | Inject ID/collaborative signals into language models to reduce semantic-collaborative mismatch. |
| Retrieval-augmented ranking | ReLLa; RALLRec; LlamaRec-LKG-RAG; CRAG; retrieval-augmented conversational recommendation | Retrieve relevant user history, knowledge, or candidates before LLM scoring. |
| Incremental and efficient tuning | POD; LSAT; E4SRec; LightLM; MoLoRec/RecCocktail; instruction distillation; decoding acceleration frameworks | Reduce compute, improve incremental updates, and make LLM rankers more deployable. |

## Generative Recommendation and Semantic IDs

| Subtopic | Representative works | Summary |
|:---|:---|:---|
| Subtopic | Representative works | Summary |
| Task unification | P5; M6-Rec; InstructRec; VIP5; UP5; P5-ID; RecSysLLM; UPSR | Convert multiple recommendation tasks into language modeling or instruction-following tasks. |
| Semantic-ID retrieval | TIGER; P5-ID; How to Index Item IDs; LC-Rec; IDGenRec; LETTER; Semantic IDs for Joint Search and Recommendation; GenCDR; GLASS; DaV-Gen | Generate item identifiers rather than scores; aims at unified retrieval and generation. |
| Semantic-ID diagnostics and improvements | Generative Recommendation with Semantic IDs handbook; Differentiable Semantic ID; Variable-Length Semantic IDs; Generating Long Semantic IDs in Parallel; SIDInspector; Qualification-Aware SID; Adaptive Collision Handling; Expressiveness Limits; LBR | Address collision, invalid outputs, length bias, scalability, and calibration. |
| Industrial semantic-ID systems | PLUM; SIGMA; AKT-Rec; AIR intent IDs; Taiji semantic features; Gryphon; YouTube SemanticID discussions | Show how semantic IDs enter real retrieval and ranking systems. |
| Diffusion and alternative generation | Diffusion recommendation surveys; continuous-token diffusion; session generative recommendation; POI semantic-ID generation; chain-of-recommendation | Broaden generation beyond autoregressive text/ID decoding. |

## Agentic, Conversational, and Interactive Recommendation

| Subtopic | Representative works | Summary |
|:---|:---|:---|
| Subtopic | Representative works | Summary |
| Conversational recommendation | TG-ReDial; KBRD; UniCRS; MESE; Chat-REC; Large Language Models as Zero-Shot Conversational Recommenders; retrieval-augmented CRS | Natural-language preference elicitation and explanation. |
| Agents for recommendation | Agent4Rec; AgentCF; MACRec; RecMind; iAgent; MMEACR; connected-TV agentic recommendation; group recommender LLM agents; controllability-centric collaborative agents | Use planning, memory, reflection, tool calls, and multi-agent collaboration. |
| User simulation and A/B agents | A/B Agent; RecInter; generative agents in recommendation; LLM user preference induction; LLM-as-a-judge slate recommendation | Simulate users, expand labels, or evaluate slates before online tests. |
| Industrial agentic systems | RecGPT; RecGPT-V2; RecGPT-Mobile; Ranking Engineer Agent style ads tooling; creator/advertiser matching with Gemini-like models | Use agents for intent reasoning, engineering productivity, or matching workflows. |

## Trustworthy, Fair, Robust, and Safe LLM Recommendation

| Subtopic | Representative works | Summary |
|:---|:---|:---|
| Subtopic | Representative works | Summary |
| Fairness and bias | FaiRLLM; RECLLM; job recommendation demographic bias; fairness in LLM-based recommender systems survey; provider fairness in news recommendation; popularity bias studies | Study demographic, provider, exposure, recency, and popularity biases. |
| Robustness and poisoning | LoRec; STELLA; exact and efficient unlearning for LLM recommendation; incremental learning; memorization behavior in generative recommendation | Address instability, privacy, poisoning, and memorization. |
| Explainability | XRec; RecExplainer; explanation generation surveys; uncertainty-aware explainable recommendation; coherent natural-language explanations | LLMs can explain, but explanations must be faithful and safe. |
| Privacy and on-device | DPLLM; RecGPT-Mobile; federated content representation; privacy-preserving local LLM recommenders | Reduce central exposure of user histories and sensitive profiles. |
| Evaluation and controllability | LLM-as-a-judge; user preference induction; controllability-centric evaluation; A/B Agent; length bias reduction; position-bias-aware reranking | Evaluate behavior beyond static offline labels. |

# Extended Annotated Literature Catalog

The full annotated catalog with 250+ works is preserved in the PDF and LaTeX source. For Feishu readability, this document keeps the thematic maps above and summarizes the catalog by area instead of writing a single 250-row table.

- Classical and pre-LLM neural recommendation: Wide&Deep, YouTube DNN, DIN/DIEN, SASRec/BERT4Rec, DLRM, Monolith, PinnerSage/PinnerFormer, graph and conversational recommenders.
- LLM feature engineering and data augmentation: TagGPT, KAR, HKFR, RLMRec, LLMRec, CUP, SINGLE, LLMHG, ONCE, MINT, BEQUE, Agent4Ranking, and related systems.
- LLM/PLM encoders and cross-domain models: U-BERT, UNBERT, PLM-NR, ERNIE-RS, RecFormer, UniSRec, VQ-Rec, MISSRec, PMMRec, Uni-CTR, PCDR.
- LLM scoring/ranking and instruction tuning: TALLRec, InstructRec, ReLLa, SetwiseRank, LlamaRec, CoLLM, LLaRA, A-LLMRec, RecRanker, DEALRec, RecExplainer.
- Generative recommendation and semantic IDs: P5, M6-Rec, TIGER, P5-ID, LC-Rec, IDGenRec, LETTER, RPG, differentiable/variable-length semantic IDs, PLUM, SIGMA, AKT-Rec, Gryphon.
- Agentic/conversational recommendation: Chat-REC, Agent4Rec, AgentCF, MACRec, RecMind, iAgent, RecGPT-V2, MMEACR, connected-TV agentic recommendation.
- Trustworthy and evaluation work: FaiRLLM, RECLLM, STELLA, LoRec, LBR, A/B Agent, LLM-as-a-judge, user preference induction, controllability-centric evaluation.


# Primary References

H.-T. Cheng et al. Wide & Deep Learning for Recommender Systems. DLRS, 2016.

P. Covington, J. Adams, and E. Sargin. Deep Neural Networks for YouTube Recommendations. RecSys, 2016.

G. Zhou et al. Deep Interest Network for Click-Through Rate Prediction. KDD, 2018.

W.-C. Kang and J. McAuley. Self-Attentive Sequential Recommendation. ICDM, 2018.

F. Sun et al. BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer. CIKM, 2019.

M. Naumov et al. Deep Learning Recommendation Model for Personalization and Recommendation Systems. arXiv:1906.00091, 2019.

S. Geng, S. Liu, Z. Fu, Y. Ge, and Y. Zhang. Recommendation as Language Processing: A Unified Pretrain, Personalized Prompt and Predict Paradigm. RecSys, 2022.

Z. Cui, J. Ma, C. Zhou, J. Zhou, and H. Yang. M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems. arXiv:2205.08084, 2022.

K. Bao et al. TALLRec: An Effective and Efficient Tuning Framework to Align Large Language Model with Recommendation. RecSys, 2023.

Y. Gao et al. Chat-REC: Towards Interactive and Explainable LLMs-Augmented Recommender System. arXiv:2303.14524, 2023.

Z. Lin et al. How Can Recommender Systems Benefit from Large Language Models: A Survey. ACM TOIS, 2024.

J. Li et al. Towards Next-Generation LLM-based Recommender Systems: A Survey and Beyond. arXiv:2410.19744, 2024.

L. Lin et al. Large Language Models for Generative Recommendation: A Survey and Visionary Discussions. LREC-COLING, 2024.

S. Rajput et al. Recommender Systems with Generative Retrieval. NeurIPS, 2023.

Y. Lin et al. ReLLa: Retrieval-enhanced Large Language Models for Lifelong Sequential Behavior Comprehension in Recommendation. WWW, 2024.

Y. Zhang et al. Collaborative Large Language Model for Recommender Systems. WWW, 2024.

J. Liao et al. LLaRA: Large Language-Recommendation Assistant. SIGIR, 2024.

J. Zhai et al. Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations. arXiv:2402.17152, 2024.

L. Yu, Z. Liu, Z. Zhang, J. Zhou, and J. Chen. ReLand: Integrating Large Language Models’ Insights into Industrial Recommenders via a Controllable Reasoning Pool. RecSys, 2024.

Q. Zhao, H. Qian, Z. Liu, G.-D. Zhang, and L. Gu. Breaking the Barrier: Utilizing Large Language Models for Industrial Recommendation Systems through an Inferential Knowledge Graph. CIKM, 2024. arXiv:2402.13750.

Meituan MTFM Team. MTFM: A Scalable and Alignment-free Foundation Model for Industrial Recommendation in Meituan. arXiv:2602.11235, 2026.

D. Sun, Y. Liu, J. Zhou, X. Liu, C. Yu, Y. Li, H. Yu, and J. Zhang. SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress. arXiv:2602.22913, 2026.

Y. Meng, C. Guo, Y. Cao, T. Liu, and B. Zheng. A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao. arXiv:2505.07197, 2025.

Y. Chen et al. Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations. arXiv:2606.10357, 2026.

Kuaishou Taiji Team. Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation. arXiv:2606.03866, 2026.

A. Tsai et al. PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations. arXiv:2510.07784, 2025.

C. Yan et al. From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs. arXiv:2605.23310, 2026.

RecGPT Team. RecGPT Technical Report. arXiv:2507.22879, 2025.

RecGPT Team. RecGPT-V2 Technical Report. arXiv:2512.14503, 2025.

B. Zhang et al. RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation. arXiv:2605.04726, 2026.

Anonymous/Authors. LBR: Towards Mitigating Length Bias in Large Language Models for Recommendation. arXiv:2607.04270, 2026.

Authors. Seeing and Reflecting: Multimodal Memory-Enhanced Agent Collaboration for Recommendation. arXiv:2607.07108, 2026.

Authors. An LLM-powered Agentic Recommendation System for Connected TV Content Discovery. arXiv:2607.09988, 2026.

Authors. User Preference Induction with LLMs for Offline Top-N Recommendation Evaluation. arXiv:2607.11354, 2026.

J. Zhou et al. Can We Steer the Black-Box? Towards Controllability-Centric Evaluation of Recommender Systems with Collaborative Agents. arXiv:2607.13418, 2026.


## 中文版

# 范围、证据分层与综述方法

“推荐 + 大模型”已经不是一个单一技术概念。它可能指 BERT 风格编码器用于新闻表示，也可能指 P5 这类 T5 文本到文本推荐模型、TALLRec 这类 LLaMA 偏好判断模型、多模态 LLM 抽取商品属性、语义 ID 生成式召回、万亿参数级用户行为序列 transducer，或者能与用户多轮交互的推荐智能体。这些系统的失效模式和部署成本差异极大，不能简单合并讨论。

本文采用三层证据划分：

1.  **第一层：公开线上证据。** 来源明确报告生产 A/B 或 live experiment 结果。这是工业价值最强证据，但不同平台的指标和 baseline 仍不可直接横比。

2.  **第二层：生产导向但线上披露不完整。** 来源来自工业场景、真实日志或部署架构，但没有完整公开线上 A/B 数字。它们对架构和系统设计有价值，但不能当作已证实的线上收益。

3.  **第三层：学术与预生产研究。** 主要在公开数据集上推进建模、对齐、评测、鲁棒、公平或数据方法。它们定义技术前沿，但离线收益不能等同于线上收益。

时间范围从 2016 年左右的 Wide&Deep、YouTube DNN、DIN、DIEN、SASRec、BERT4Rec、DLRM 等神经推荐基础开始，因为这些模型解释了工业推荐系统的链路形态。随后追踪到 P5、M6-Rec、TALLRec、Chat-REC、InstructRec、ReLLa、CoLLM、LLaRA、A-LLMRec、TIGER、HSTU、PLUM、SIGMA、RecGPT 等 LLM4Rec 和 large recommender model。最新纳入的工作覆盖到 2026 年 7 月，包括 LBR 长度偏差、多模态记忆增强智能体协作、LLM 离线评测、CTV agentic recommendation 和 controllability-centric evaluation。

# 历史背景：为什么推荐没有简单变成 NLP

## 工业推荐链路

工业推荐通常是多阶段系统。召回把数百万或数十亿 item 缩小到候选集；粗排和精排在严格延迟预算下打分；重排或 slate optimization 同时平衡多样性、新颖性、公平、收入、库存、创作者或商家健康和政策约束。Feature store、流式日志、在线学习、ANN 索引、实验平台和 guardrail 与神经模型同样重要。

这套链路围绕稀疏 ID、稠密特征和行为日志发展而来。Wide&Deep 和 DeepFM 让交叉特征与 embedding 结合成为 CTR 预测主流；YouTube DNN 展示了大规模召回如何被建模为巨大语料上的多分类；DIN/DIEN 强调 target attention 与兴趣演化；SASRec/BERT4Rec 将 Transformer 引入序列推荐；DLRM 及其工业后继扩展了稀疏 embedding table 和特征交互网络。这些模型并没有过时。多数 LLM 推荐方法仍然嵌入这套 serving substrate。

## 语言模型带来的增量能力

语言模型相对传统 ID 推荐增加了四类能力：

- **语义抽象。** 商品标题、评论、query、图片 caption、视频 transcript 或用户自述可以被映射到更易迁移的语义空间。

- **指令跟随。** 推荐任务可以写成 prompt：判断用户是否喜欢 item、排序候选列表、解释推荐、追问澄清或生成搜索 query。

- **世界知识和推理。** LLM 能推断季节性意图、替代/互补关系、事件驱动偏好和行为日志中没有显式记录的高层属性。

- **文本生成和交互。** LLM 可以生成解释、摘要、会话轮次、合成用户画像和推荐结果 critique。

但推荐系统也有通用 LLM 默认不满足的要求：校准分数、低延迟、巨大 item corpus、频繁 item 更新、反事实评估、业务约束和稳定线上实验。大量研究本质上是在调和这两个世界。

# 大模型推荐分类

## LLM 作为特征工程器

最容易落地的角色是特征工程。冻结或轻微微调的 LLM 生成 item tag、用户画像、意图摘要、review aspect、query rewrite、图边或合成样本。代表工作包括 TagGPT、LLM4KGC、KAR、HKFR、RLMRec、LLMRec with graph augmentation、CUP、SINGLE、LLMHG、Llama4Rec、ONCE、MINT、RecPrompt、BEQUE 和 Agent4Ranking。这类方法通常不要求 LLM 在线给每个候选打分，而是让 LLM 生成可缓存资产，再由传统召回/排序消费。

这解释了为什么 LLM-as-enhancer 在工业上很有吸引力：风险局部化。如果生成属性有噪声，下游 ranker 可以学习忽略；如果 LLM 昂贵，可以离线跑；如果政策规则变化，特征生成链路也可以单独审计。

## LLM 或 PLM 作为编码器

预训练语言模型可以编码文本丰富的 item 和用户历史。这条线早于当前 LLM 浪潮：U-BERT、UNBERT、PLM-NR、Pyramid-ERNIE、ERNIE-RS、CTR-BERT、Tiny-NewsRec、RecFormer、UniSRec、VQ-Rec、MISSRec、PMMRec 以及许多新闻、招聘、软件和旅游推荐。后续工作引入更大的 LLM embedding、instruction-tuned encoder 或 adapter。

编码器方法适合工业链路，因为 embedding 可以预计算、索引、蒸馏并与 ID embedding 组合。局限是内容相似不等于协同偏好。这正是 CoLLM、LLaRA、A-LLMRec、LLM2BERT4Rec、LC-Rec、ControlRec 等对齐方法试图解决的 semantic-collaborative gap。

## LLM 作为 scorer 或 ranker

另一条路线把推荐写成语言分类或排序任务。TALLRec 把用户历史和候选 item 写成 instruction，让 LLM 回答 yes/no。InstructRec 和 RecRanker 做 instruction tuning。SetwiseRank 和 listwise LLM ranker 用比较式 prompt 排序候选集。ReLLa 在 prompt 前检索相关行为片段，LlamaRec 使用两阶段 retrieve-then-rank。它们在可控性和冷启动推理上有吸引力，但原生 LLM scoring 对大规模工业排序通常太慢且校准不足。

## LLM 作为生成器

生成式推荐把输出 item、item ID、语义 ID、query、解释或 slate 视为生成序列。P5 和 M6-Rec 将多种推荐任务统一为语言处理；GPT4Rec、GenRec、BIGRec、PALR、LightLM、LLaRA、LC-Rec、IDGenRec、TIGER 等进一步扩展。关键问题是输出词表：item title 可读但歧义大；数值 ID 精确但没有语义；语义 ID 则在紧凑性和语义性之间折中。

## Large recommendation models 与序列 transducer

并非所有大推荐模型都是 LLM。Meta 的 HSTU-based Generative Recommenders 把工业推荐建模为用户行为序列 transduction，扩展到 1.5T 参数，并报告 12.4% 线上 A/B 提升及随 compute 的 power-law scaling 。美团 MTFM 则构建跨多场景的推荐基础模型 。这些模型借鉴语言模型 scaling 思路，但训练对象是 action stream、稀疏 ID 和推荐目标。

## 智能体与会话推荐

Agentic recommender 使用 LLM 做规划、工具调用、记忆、自反思或多智能体协作。Chat-REC 和会话推荐系统探索交互推荐；MACRec、AgentCF、iAgent、RecMind、RecGPT-V2、MMEACR、LLM-as-a-judge slate recommender 和 connected-TV agentic system 将这一方向继续推进。优势是更丰富的偏好澄清和解释；工业挑战是行为可预测、延迟、安全和评估。

# 核心学术里程碑

## P5：文本到文本统一范式

P5（Pretrain, Personalized Prompt, and Predict）是一个里程碑，因为它明确提出推荐任务可以统一为 text-to-text learning 。评分预测、序列推荐、解释生成、评论摘要和直接推荐可以共享同一语言模型目标。P5 没有解决工业 serving，但改变了研究者对任务统一的理解。

## M6-Rec：开放式工业预训练

M6-Rec 将大规模生成式预训练语言模型扩展到推荐，强调工业推荐需要支持多域、多任务、多模态和开放式适配 。它把推荐任务转成语言理解或生成任务，并强调样本高效下游适配，是学术 LLM4Rec 与工业基础模型之间的重要桥梁。

## TALLRec：instruction tuning 推荐

TALLRec 展示了用 LoRA 对 LLaMA 类模型进行推荐 instruction tuning 的可行性 。其 yes/no 偏好判断形式很简单，但影响很大。它也暴露了一个反复出现的问题：语言语义和协同行为偏好不是同一件事。后续方法通过协同 embedding、检索增强、rationale distillation 或语义 ID 来缓解这个问题。

## TIGER 与语义 ID 生成式召回

TIGER 把召回重写为生成 item identifier 。模型不再在 embedding 空间中做近邻检索，而是解码从 item 内容中学习到的 semantic ID。这启发了 P5-ID、LC-Rec、IDGenRec、LETTER、RPG、differentiable semantic ID、variable-length semantic ID、SIDInspector、PLUM、SIGMA、AKT-Rec、Gryphon 等大量工作。核心问题包括 collision、validity、calibration、cold-start generalization 和高效 constrained decoding。

## 协同信号对齐

CoLLM、LLaRA、A-LLMRec、LC-Rec、ControlRec、CLLM4Rec 等方法试图把协同信号注入语言模型。机制包括将协同 embedding 投影到 token 空间、adapter/LoRA、item token learning、contrastive alignment 或两阶段 grounding。这一族方法存在的原因很明确：纯文本语义不足以刻画行为驱动偏好。

## RAG 与长历史理解

ReLLa 和 RALLRec 表明 LLM 需要检索来处理 lifelong behavior。长用户历史里既有信号，也有过时、冲突、偶然和上下文依赖的噪声。ReLLa、RALLRec、AIR、RecGPT-V2、RecGPT-Mobile、HLLM 类层次方法和 MMEACR 类多模态记忆智能体都反映了同一洞察：在大模型或 ranker 看见历史之前，先检索并压缩相关部分。

## 评测、公平和鲁棒

近期工作研究 LLM 推荐是否稳定、公平、校准和可控。STELLA 指出 LLM 推荐可能不稳定。FaiRLLM、RECLLM、公平综述、provider fairness、招聘推荐偏差和 demographic bias 研究表明，LLM 会继承甚至放大社会和流行度偏差。2026 年 7 月的 LBR 针对 LLM 推荐中的长度偏差。LLM-based offline evaluation 和 controllability-centric agent evaluation 表明评测本身也在变化。

# 公开线上 A/B 的工业系统

表 <a href="#tab:ab-zh" data-reference-type="ref" data-reference="tab:ab-zh">1</a> 汇总公开披露线上 A/B 或 live-experiment 指标的工业案例。不同系统的流量、baseline 成熟度、产品场景、指标定义和时间窗口都不同，不能当成同一 benchmark 横比；但它们说明哪些模式已经跨过生产门槛。


| 系统 | 平台 | 大模型角色 | 公开线上结果 | 来源 |
|:---|:---|:---|:---|:---|
| 系统 | 平台 | 大模型角色 | 公开线上结果 | 来源 |
| HSTU / Generative Recommenders | Meta 大型互联网平台 | 针对用户行为流的序列 transduction 架构。 | 1.5T 参数 GR 报告 **+12.4%** 线上 A/B topline 提升；HSTU 在 8192 长度序列上比 FlashAttention2 Transformer 快 5.3x–15.2x。 |  |
| ReLand | 支付宝 | LLM 洞察通过 controllable reasoning pool 注入。 | 2024 年 1 月部署后：**+3.19% CTR**、**+1.08% CVR**。 |  |
| LLM-KERec | 支付宝 | LLM 辅助构建 inferential knowledge graph。 | 10% 流量、一个月 A/B：三个场景分别有 **+6.24%** 转化、**+6.45% GMV**、**+10.07%** 转化。 |  |
| MTFM | 美团 | 多场景推荐基础模型。 | SQS：**+1.89% CTR**、**+2.46% UV_CTCVR**、**+2.98% 订单**、**-5 ms**；PHF：**+1.53% CTR**、**+1.03% UV_CTCVR**、**+1.45% 订单**、**-6 ms**。 |  |
| SIGMA | AliExpress | 语义增强、指令驱动的生成式多任务推荐。 | 5% 流量、两周 A/B：**+2.80% 订单量**、**+3.84% 转化**、**+7.84% GMV**、**+2.47% 购买类目广度**。 |  |
| SORT-Gen | 淘宝 | 生成式列表级多目标重排。 | 百亿补贴两周 A/B：**+4.13% CLICK**、**+8.10% GMV**。 |  |
| AIR | 快手 | 离线 LLM atomic intent + 在线 target-aware retrieval。 | 5.08% 流量：**+1.043% paid orders**、**+3.446% GMV**、**+3.662% GPM**、**+1.254% OPM**；相对直接调用 LLM 约 400x 吞吐提升。 |  |
| Taiji | 快手广告 | LLM-as-enhancer + preference reasoning + Pareto reward alignment。 | 一周 A/B，10%/10%：**+2.83% ADVV**、**+3.30% revenue**；长尾用户 **+5.26% ADVV**、**+5.32% revenue**。 |  |
| PLUM | YouTube | Gemini 系列预训练 LM 适配为语义 ID 生成式召回。 | 在 LEM+ 上加入 PLUM：长视频 **+0.76% panel CTR**、**+0.80% views**；Shorts **+4.96% panel CTR**、**+0.39% views**；满意度为正。 |  |
| AKT-Rec | 天猫 | MLLM/LLM 语义 ID + 非对称 head-to-tail 迁移。 | 两周 A/B，10%/10%：**+2.73% clicks**、**+2.76% CTR**、**+1.7% CTCVR**、**+3.47% GMV**。 |  |
| RecGPT | 淘宝 | 百亿级 intent-centric reasoning model。 | 公开摘要报告线上 **+9.47% IPV**、**+6.33% CTR**，同时改善多样性和商家侧收益。 |  |
| RecGPT-V2 | 淘宝 | 层次多智能体意图推理与 agentic judge/reward。 | 两周 A/B 对比 RecGPT-V1。Item 场景报告 **+3.64% IPV**、**+3.01% CTR**、**+3.39% GMV**、**+3.47% ATC**、**+11.46% NER**。 |  |

有公开线上证据的大模型推荐工业案例。

# 工业导向但公开 A/B 不完整的系统

很多重要工业系统没有完整公开 A/B 数字，但它们仍然影响领域，因为它们公开了架构、训练流水线、系统瓶颈和部署假设。

- **M6-Rec 和 M6 类电商基础模型** 强调跨商品、内容和 UGC 域的统一生成式建模。

- **BEQUE 和淘宝 query rewrite** 展示了 LLM 如何为搜索/推荐生成长尾 query rewrite，通常作为离线或近线扩展。

- **RecGPT-Mobile** 将轻量意图 agent 放到用户设备上，兼顾隐私和即时上下文，而云端继续负责全局召回和排序。

- **Large Language Model as Universal Retriever** 探索一个 LLM-based retriever 是否能服务多种工业召回目标。

- **Gryphon** 在工业音乐服务中把 item-level scoring 加到 semantic-ID generation 上，处理 sequence-score calibration 和 SID collision。

- **RecBase、OneMall、GPR、RankGR 等 large recommender models** 试图在多个推荐 surface 上预训练或对齐一个模型，但公开线上证据程度不同。

- **Meta GEM 与广告 foundation model 讨论** 暗示广告推荐 backbone 共享和实验加速趋势；但第三方博客说法若缺少一手技术报告，应作为工程背景而不是主证据。

- **Google/YouTube 围绕 Gemini 和 creator/advertiser matching 的产品/研究公告** 显示多模态基础模型正在进入类似推荐的匹配任务；PLUM 仍是 YouTube 推荐 A/B 效果最清楚的公开技术证据。

# 关键技术主题

## 语义 ID 与离散瓶颈

语义 ID 解决一个问题，也带来若干新问题。它把丰富 item 语义压缩成短离散码，由自回归模型生成，使召回看起来像语言解码，并在 ID 与内容绑定时提供零样本或冷启动泛化。但 code 可能 collision、不均衡、过拟合某个模态，或生成无效输出。近期工作用 residual quantization、learnable item tokenization、differentiable semantic ID、variable-length ID、unordered long ID、parallel decoding、qualification-aware collision handling、adaptive collision handling 和 SIDInspector 等方法回应这些问题。

## 协同信号对齐

LLM 懂语言，推荐系统懂行为。对齐方法试图避免二者互相冲掉。一些方法把 collaborative embedding 投影到语言模型 token 空间；一些训练 adapter 或 LoRA；一些用 contrastive objective 对齐 item 文本和 co-click；语义 ID 方法往往同时用内容和协同信号构造 ID。PLUM 和 AKT-Rec 等工业系统说明，这种对齐不是可选项：纯内容语义很难支撑高风险推荐。

## 长历史与记忆

大 context window 不自动解决 lifelong behavior modeling。用户历史包含过时、冲突、偶然和上下文依赖交互。ReLLa、RALLRec、AIR、RecGPT-V2、RecGPT-Mobile、HLLM 类层次方法和 MMEACR 类多模态记忆 agent 都体现了同一原则：在大模型或 ranker 使用历史之前，先检索并压缩相关部分。

## 重排、slate optimization 与多目标

大模型不只服务 top-1 relevance。SORT-Gen 建模列表级多目标重排；LLM diversity re-ranking 和 explanation-aware re-ranking 优化整页推荐；RecGPT-V2 纳入 NER；SIGMA 纳入 purchased category breadth；Taiji 平衡 semantic reward 与 collaborative reward。研究前沿正在从 item scoring 转向带业务约束的可控 slate generation。

## 多模态推荐

现代 item 是多模态的：商品图、标题、评论、视频、音频、transcript、评论、创作者元数据和直播上下文。VIP5、MM-Rec、MISSRec、PMMRec、LLM multimodal recommender survey、AKT-Rec、PLUM 和 MMEACR 展示了不同融合方式。难点不只是使用视觉语言模型，而是判断在何种用户意图下哪种模态应该主导，以及如何保持多模态特征新鲜且安全。

## Agents、交互和用户模拟

Agentic recommender 可以提问、修正假设、调用工具、模拟用户、critique slate 并维护记忆。Agent4Rec、RecMind、MACRec、AgentCF、iAgent、MMEACR、LLM group recommender、connected-TV agent 和 LLM-as-a-judge evaluation 系统体现了这一转向。主要风险是 agent 比 ranker 更难评估：ranker 返回分数，而 agent 可能改变用户偏好表述、追问问题或幻觉约束。

# 问题导向阅读指南

如果按实践问题而不是模型名字来读文献，脉络会更清楚。同一种模型在一个场景中可能合适，在另一个场景中可能完全浪费。

## 冷启动和长尾

冷启动和长尾是 LLM 最自然的切入点。传统 ID embedding 在 item 曝光很少或用户历史很短时很弱，而内容丰富的 LLM 表示、语义 ID 和多模态编码器可以从标题、商品图、描述、评论、transcript 和共现实体中迁移信息。相关工作包括 P5、M6-Rec、TIGER、UniSRec、VQ-Rec、MISSRec、PMMRec、AKT-Rec、PLUM、GenCDR 和 semantic-ID diagnostics。工业经验是不要把 content-only feature 当作终点：冷启动内容语义应该和可用的协同证据融合，即使协同证据很弱。AKT-Rec 的价值在于它显式避免“帮长尾但伤头部”，这是生产系统非常常见的顾虑，因为头部流量受损可能抵消长尾收益。

## 跨域迁移

当不同域有语义重叠但直接交互稀疏时，LLM 对跨域推荐特别有用。典型场景包括内容到电商、搜索到推荐、短视频到商品、query 到 item。AIR、SIGMA、MTFM、S&R Foundation、Uni-CTR、PCDR 和 GenCDR 展示了不同方案。实践设计的关键是共享什么：共享 embedding 空间、共享 semantic-ID 词表、共享用户 intent memory，还是共享多场景 transformer。共享表示能提升迁移，但当不同域优化目标不一致时也会产生负迁移。因此生产系统常使用 mixture、gating、adapter 或 scenario-specific subgraph，而不是无条件共享一个表示。

## 文本丰富和多模态 item

新闻、电商、本地服务、招聘、短视频、音乐、图书和 creator/advertiser matching 都是文本丰富或多模态场景。PLM-NR、MM-Rec、VIP5、MISSRec、PMMRec、PLUM、AKT-Rec 和 MMEACR 都有代表性。在这些场景里，LLM/MLLM 的价值不只是更好的 item embedding，还包括暴露可解释属性：主题、品牌、风格、季节性、受众、意图、安全类别和替代关系。工业上这很重要，因为推荐团队需要 debugging handle。黑盒 embedding 可能提升 NDCG，但生成属性可以解释为什么模型突然过度分发某个趋势或低估某类商家。

## 广告和商业推荐

广告推荐比很多自然推荐有更强的校准、拍卖和多方约束。排序模型不仅要选语义合理的 item，还要估计 action probability 和 value。因此 LLM 在广告系统中往往先作为 feature producer 或 alignment module 出现。Taiji 报告了 ADVV 和 revenue 收益，HSTU 和 GEM 类讨论则指向广告排序共享大 backbone。在广告里，LLM 生成候选或解释并不够，除非它能与校准 advertiser value、预算 pacing、policy constraint 和用户体验 guardrail 绑定。真正的问题不是 LLM 能不能理解广告，而是它的语义信号能否改善校准价值预测且不扰乱 marketplace。

## 短视频和 feed 推荐

短视频和 feed 系统同时面对快速趋势、多模态内容、创作者生态、长用户历史和高反馈量。HSTU、PLUM、AIR、RecGPT、RecGPT-Mobile 等系统都很重要。它们展示了两条相反但可兼容的方向：一种是直接从行为中学习的超大 action-sequence model；另一种是压缩内容和上下文的 semantic-intent 系统。实践架构可能同时使用二者：高吞吐 action model 作为主排序信号，LLM-derived intent/content feature 用于冷启动、多样性、解释或跨域迁移。

## 会话和智能体推荐

会话推荐不是“聊天 + 排序”这么简单。系统必须决定何时追问、何时推荐、如何记忆、如何从错误假设中恢复，以及如何把推荐 grounded 到可用库存。Chat-REC、RecMind、MACRec、AgentCF、iAgent、MMEACR、RecGPT-V2 和 CTV agentic recommendation 展示了这一设计空间。生产中最难的是评测：agent 可以生成流畅对话，同时把用户引向不可用或不安全 item。Grounding、tool constraint 和 audit log 与模型质量同样重要。

## 评测和用户模拟

LLM-as-judge 与用户模拟系统很有吸引力，因为线上 A/B 成本高。但它们应该被视为 pre-A/B filter，而不是真实流量替代品。Simulator 可以测试系统是否遵守约束、解释是否一致、生成 ID 是否有效、slate 是否满足已知偏好画像。但如果不与真实用户行为校准，它无法可靠估计长期留存、marketplace dynamics、创作者激励或疲劳。LLM 评测最好的使用方式是分层 gate：离线标签和反事实估计、LLM 诊断判断、小规模人工 review、shadow traffic，最后才是受控线上实验。

# 代表范式深挖

## Instruction-tuned LLM 推荐

TALLRec 和 InstructRec 这类 instruction-tuned recommender 思路很简单：把推荐数据转成 instruction-response pair，然后微调 LLM。优点是灵活，同一个模型可以判断用户是否喜欢 item、解释原因，或适配自然语言约束。弱点是推荐标签并不是天然语言标签。Yes/no 输出易训练，却很难校准成 CTR/CVR；离线候选集也可能被人为缩小。在生产中，instruction-tuned LLM ranker 更适合作为 reranker、弱用户 specialist、解释模块或特征生成器，而不是百万候选的主 scorer。

这一范式仍然重要，因为它建立了推荐日志与 LLM 训练之间的数据接口。一旦用户历史和 item metadata 被序列化成 instruction，就可以加入 rationale、retrieved behavior、collaborative embedding、业务约束或安全规则。很多后续工作都可以理解为对朴素 instruction template 的改进：更好的 grounding、更好的协同对齐、更好的检索、更好的输出约束或更好的蒸馏。

## 语义 ID 生成式召回

语义 ID 召回是 LLM 时代最有辨识度的想法之一。它把召回问题从“给所有 item 打分或做近邻搜索”改成“生成能映射到 item 的离散 code”。这让召回与语言建模产生优雅连接，但也带来一系列设计选择。

第一，ID 应如何构造？Content-only ID 对新 item 泛化好，但可能忽略协同行为；collaborative ID 捕捉行为但冷启动弱；hybrid ID 试图兼顾。第二，ID 应固定还是端到端学习？固定 ID 稳定目标词表，differentiable/learnable ID 可以适配任务目标。第三，collision 应如何处理？如果 collision 聚合同类替代品，它可能有益；如果合并无关 item，它会有害。第四，decoding 如何约束？无约束生成会产生无效 ID；十亿级目录需要 prefix tree、sparse transition matrix 或 post-verification。第五，生成 ID 如何打分？累计 token likelihood 不一定等于 item relevance，因此 Gryphon 等系统加入 item-level scoring。

语义 ID 的工业意义在于，它让语言模型式 generation 能兼容召回基础设施。PLUM 在 YouTube 规模展示了这一点；SIGMA 和 AKT-Rec 在电商中展示了相关思路。剩下的问题是：在计入 freshness、invalid output 和 serving cost 后，语义 ID 生成能否持续超过强 ANN 召回。

## LLM-as-enhancer 和语义特征库

LLM-as-enhancer 很可能仍是最常见工业模式。LLM 产生语义资产，传统推荐系统消费这些资产。资产可以是 user profile、item attribute、query rewrite、graph edge、atomic intent、explanation、reward feature 或 semantic ID。它有效，是因为尊重既有生产链路：feature store、ranker、monitor 和 A/B platform 不需要围绕自由生成重写。

但 LLM 生成资产也需要自己的生命周期：schema、freshness policy、validation rule、drift monitor、backfill 和 rollback。如果商品 taxonomy 改变，生成 tag 可能过时；如果 prompt 改变，feature distribution 会漂移；如果 LLM provider 改变，下游校准也会移动。不能把语义资产仅当作普通 feature，它们是带 prompt 和模型 provenance 的 generated feature。

## Recommendation-native foundation model

HSTU 和 MTFM 展示了另一条路线：不是适配通用 LLM，而是围绕推荐数据构建大模型。当平台有海量 action log 和足够训练/服务基础设施时，这条路线很有吸引力。因为模型直接在行为上训练，它能避免部分 semantic-collaborative mismatch，并保留推荐 compute scaling law 的可能性。

代价是系统复杂度。Recommendation-native foundation model 必须处理高基数稀疏特征、非平稳 item 词表、流式更新、长历史、多目标标签和低延迟服务。HSTU 引入架构改造和 inference amortization；MTFM 使用异构 token 和场景 subgraph。这更像构建新的推荐平台，而不是加一个 LLM 组件。

## Agentic recommender

Agentic recommender 的吸引力在于它可以表示用户任务，而不仅是历史点击。购物用户可能说“我要给同事买预算内礼物”，agent 可以追问、检索候选、推理约束并解释 trade-off。RecGPT-V2 通过层次 expert agent 将这一思路带入淘宝 feed 推荐；MMEACR 和 CTV agent 展示了记忆与多模态上下文如何加入。

主要研究挑战是 agentic recommendation 模糊了推荐、搜索、对话和决策支持的边界。主要工业挑战是安全：与用户交互的 agent 可能操纵偏好、过度个性化、幻觉库存、泄露隐私推断或造成体验不一致。Agentic 系统需要 grounded tool、bounded action space、conversation policy 和超越 ranking metric 的评测。

# 如何阅读博客、技术报告和厂商声明

官方技术博客（例如 Google、Meta、YouTube 等）很有价值，但需要和论文区别阅读。本文使用四级证据：

1.  **带线上指标的一手技术论文。** 例如 HSTU、PLUM、MTFM、SIGMA、AIR、Taiji、AKT-Rec。它们可支持线上收益判断，但仍要看 baseline 和指标定义。

2.  **线上披露不完整的一手技术报告或产品论文。** 例如部分 RecGPT、RecGPT-Mobile、大 retriever 或 foundation-model 报告。它们可支持架构判断，但不一定能支持量化业务收益。

3.  **官方公司博客。** 适合补充产品背景、部署方向和战略脉络。博客通常缺少 baseline、流量分配、显著性检验和 guardrail，不应单独作为精确 A/B 证据。

4.  **第三方博客或评论。** 适合发现线索和理解趋势，但量化 claim 必须回溯到一手来源。比如 YouTube semantic ID 或 Meta GEM 的第三方解读可用于识别趋势，但定量结论应落到 PLUM 或 HSTU 这类一手文档。

这套证据纪律很重要，因为推荐系统对指标非常敏感。巨大 surface 上 0.5% 的提升可能很有价值；弱离线子集上的 5% 提升也可能线上消失。没有流量分配、实验周期、baseline 和 guardrail 的 headline number 不够。

# 为什么很多学术 LLM4Rec 方法不能直接线上落地

很多学术 LLM 推荐论文有价值，但不能按原样部署。问题不在于想法不够好，而是 benchmark 假设和生产约束不匹配。

**候选规模。** 很多 LLM ranker 实验只排序几十或几百个候选。工业召回/排序在不同阶段可能面对百万到十亿 item。每个候选调用 LLM 的方法很难过规模关。

**标签语义。** 离线数据常把观测交互当正样本、采样 item 当负样本。生产里，未观测 item 可能是未曝光、不可用、被 policy block、已消费或仅仅没有机会展示。若 LLM 评测判断的是语义合理性而不是真实用户响应，这个问题会更严重。

**时间泄漏。** LLM 预训练语料可能包含 benchmark 训练期之后的 item 流行度或描述。推荐 benchmark 需要严格 temporal split 和 leakage check。

**目录 grounding。** 生成一个标题不等于推荐，除非它能映射到当前可用 item。学术文本生成指标常忽略库存、重复、卖家约束、价格变化和地域可用性。

**延迟和成本。** 用 7B 模型提升 NDCG 的方法，如果在关键排序链路增加数十毫秒，就可能完全不可用。因此报告 latency/throughput 的工业论文尤其有价值。

**Guardrail。** CTR 或 NDCG 提升可能伴随多样性、满意度、公平、创作者曝光或 policy safety 下降。真实部署需要多指标 scorecard。

**运维漂移。** Prompt、LLM 版本、taxonomy、item catalog 和用户行为都会漂移。Generated feature pipeline 必须像模型一样监控，而不是像静态元数据一样处理。

# 推荐评测协议

LLM-enhanced recommendation 的稳健评测应分阶段进行。

1.  **资产验证。** 检查生成 tag、semantic ID、query rewrite 和 intent summary 的有效性、覆盖、安全和漂移。

2.  **离线排序评测。** 使用 temporal split、多种负采样方案，以及冷启动、长尾、新用户和重度用户分段指标。

3.  **反事实和 replay 检查。** 有 logging propensity 时使用 IPS 或 doubly robust estimator，避免把缺失曝光当负偏好。

4.  **LLM 诊断评测。** LLM judge 只用于 bounded check，如解释一致性、约束满足和语义覆盖，并用人工与行为数据校准。

5.  **Shadow deployment。** 在真实流量上空跑，不影响曝光，用于测延迟、无效输出、特征漂移和候选重叠。

6.  **线上 A/B。** 从小流量开始，设置明确 guardrail 和分段分析，同时看业务、用户、生态和系统指标。

7.  **长期 holdout。** 更长周期测留存、疲劳、多样性、创作者/商家健康和 policy outcome。

核心原则是：LLM 特有评测应该增加 gate，而不是替代线上实验。推荐系统会改变用户行为和生态激励，完整反馈环只能通过 live experiment 测量。

# 评测：离线、线上与 LLM-as-Judge

推荐离线评测本来就困难，因为缺失标签不是负样本。LLM 又增加了 prompt 顺序敏感、输出格式失败、无效 item 生成、position bias、length bias、popularity bias、幻觉和偏好漂移等问题。近期工作提出了 LLM-based preference induction、A/B agent、用户模拟、controllability-centric evaluation 和 LLM-as-a-judge for slate recommendation。

这些工具有用，但不能替代线上实验。它们更适合作为中间 gate：在真实用户暴露前捕捉无效输出、不安全解释、多样性差或明显偏好不匹配。线上 A/B 仍然是业务影响的标准，长期 holdout 对留存和生态健康也仍然必要。

# 部署模式

## 离线大模型资产生成

最稳妥的部署模式是离线资产生成。LLM 生成 tag、semantic ID、intent summary、user profile、graph edge 或合成样本。这些资产经过验证、缓存，再被传统 ranker 使用。ReLand、LLM-KERec、AIR、AKT-Rec 和大量 feature-engineering 论文都遵循这条路线。

## 近线与增量推理

近线推理以分钟或小时级更新特征或候选。SIGMA 聚合用户最近行为，在分钟级触发带 KV cache 的增量推理。这种模式在不把完整 LLM 放入每个请求的情况下提升新鲜度。

## 候选池增强

PLUM 不是替换 YouTube 整个召回栈，而是在现有候选池中加入生成候选。这是常见生产策略：把新 retriever 作为一个 channel 引入，控制 quota，再由下游 ranker 和 guardrail 决定最终曝光。

## 端侧意图 agent

RecGPT-Mobile 指向隐私保护方向：小型端侧 LLM 总结即时上下文或预测下一 query，云端处理全局召回和排序。它降低服务器成本和隐私风险，但带来模型更新、设备异构和安全挑战。

## 完整 large recommender model

HSTU 和 MTFM 表明 recommendation-native 大模型可以带来线上收益，但需要深度系统工程：attention 变体、feature tokenization、micro-batching、cache reuse、subgraph serving、分布式训练和监控。这不是简单接一个 LLM API。

# 风险与失效模式

- **语义-协同不匹配。** 语言模型可能推荐语义上合理但用户不会点击或购买的 item。

- **校准失败。** LLM 概率或 token score 不是校准过的 CTR/CVR/GMV 估计。

- **无效生成。** 生成的 item ID、semantic ID 或标题可能映射不到当前可用商品。

- **流行度和曝光偏差。** LLM 可能复现 web 流行度或平台曝光模式。

- **长度和位置偏差。** 更长描述、更长 prompt 或更靠前 candidate 可能获得不公平优势。

- **隐私泄漏。** 用户摘要和解释可能暴露敏感行为。

- **安全与政策漂移。** 即使底层 item 安全，生成解释或 query rewrite 也可能违反政策。

- **陈旧性。** 离线语义资产在商品、趋势或用户上下文变化后可能过时。

- **成本不透明。** 若纳入延迟、GPU 成本和索引刷新，离线 AUC 收益可能消失。

# 实践 Playbook

构建 LLM-enhanced recommender 的团队可以按如下顺序推进：

1.  明确瓶颈：冷启动、长尾、跨域迁移、内容理解、搜索 query 生成、slate diversity、解释或长历史压缩。

2.  选择大模型角色：资产生成器、编码器、scorer、候选生成器、reranker、judge、reward model、simulator 或 agent。

3.  将 LLM 输出转成推荐系统原生对象：embedding、semantic ID、item tag、graph edge、generated candidate、intent memory 或 reward feature。

4.  保留强生产 baseline，并先把大模型组件作为增强 channel 引入。

5.  A/B 前验证无效输出率、幻觉、policy safety、校准、多样性和延迟。

6.  线上实验同时看目标指标和 guardrail，并分段分析长尾、冷启动、新用户、重度用户、创作者/商家和安全敏感类目。

7.  保留长期 holdout 或延迟指标，用于评估留存、满意度和生态健康。

# 开放问题

**统一报告。** 工业论文应报告流量分配、实验周期、baseline 成熟度、目标指标、guardrail、延迟、成本和分段效果。否则 A/B 结果很难解释。

**语义缓存新鲜度。** 离线 LLM 资产服务时便宜，但可能过时。系统需要 freshness-aware semantic cache 和更新策略。

**分数校准。** 生成似然、LLM judgment 和 semantic reward 必须映射到业务校准分数。

**大规模 constrained decoding。** 生成式召回需要对十亿级目录进行快速前缀约束、有效性检查和 collision 处理。

**长期价值。** 短期 CTR 可能与留存、信任、商家公平、创作者健康和内容多样性冲突。

**端侧推荐。** 本地 intent agent 可能改善隐私和即时性，但引入设备资源和分布式安全问题。

**LLM-based evaluation。** LLM judge 可以扩展标签和模拟用户，但必须用真实行为校准，不能变成 LLM 推荐系统的循环自评。

# 结论

这个领域已经不再是“LLM 能不能推荐”。LLM 可以推荐，但原生 LLM 推荐通常不是工业答案。更强的结论是：当大模型的语义、生成、多模态或推理能力被转化为可控的推荐系统对象时，它才真正有用。最有说服力的公开部署要么用 LLM 派生资产增强现有链路，要么构建带细致 serving 设计的 recommendation-native 大模型。学术界仍在扩展设计空间，尤其是语义 ID、协同对齐、智能体交互、公平和评测。下一阶段的突破很可能来自这些方向的结合：基础模型级用户/行为建模、grounded semantic ID、实时 intent memory、校准业务目标，以及衡量长期生态价值而非仅短期点击的评测协议。

# 论文与系统地图

本附录是结构化导航而非穷尽 bibliography。它按主要贡献归类 200 多篇相关论文、系统和技术报告。许多工作可归入多个类别，这里按最便于阅读的位置放置。

## 经典与 Pre-LLM 神经推荐基础

| 类别 | 代表工作 | 作用 |
|:---|:---|:---|
| 类别 | 代表工作 | 作用 |
| 工业召回与排序 | Wide&Deep; DeepFM; YouTube DNN; DLRM; Monolith; PinnerSage; PinnerFormer; MIND; ComiRec; TwinBERT; DSSM; TDM/JTM | 定义多阶段召回/排序、稀疏特征交互、大 embedding table 和 serving 约束。 |
| 兴趣建模 | DIN; DIEN; DSIN; SIM; ETA; MIMN; M2GRL; BST; MIND; HPMN | 在 LLM 之前建立 target attention、兴趣演化、session dynamics 和长历史压缩。 |
| 序列推荐 | GRU4Rec; Caser; SASRec; BERT4Rec; S3-Rec; CL4SRec; DuoRec; FDSA; FEARec; RecFormer | 为后续生成式推荐提供 transformer sequence modeling 基础。 |
| 多模态与内容推荐 | VBPR; MMGCN; GRCN; LATTICE; MM-Rec; MISSRec; PMMRec; CLIP4Rec; VIP5 | 说明图像、文本、音频和元数据如何支撑冷启动和跨域迁移。 |
| 知识与图推荐 | RippleNet; KGAT; KGIN; KGCN; LightGCN; PinSage; GraphRec; HKFR; KG-enhanced conversational recommenders | 预示 LLM 知识抽取和图增强推荐。 |
| 会话推荐 | ReDial; TG-ReDial; KBRD; CR-Walker; UniCRS; MESE; TCP; C2-CRS; Chat-REC | 为 agentic recommendation 提供交互协议和评测问题。 |

## LLM 特征工程与数据增强

| 子方向 | 代表工作 | 摘要 |
|:---|:---|:---|
| 子方向 | 代表工作 | 摘要 |
| 用户/item 特征增强 | LLM4KGC; TagGPT; ICPC; KAR; PIE; LGIR; GIRL; LLM-Rec; HKFR; LLaMA-E; EcomGPT; TF-DCon; RLMRec; LLMRec; LLMRG; CUP; SINGLE; SAGCN; UEM; LLMHG; Llama4Rec; LLM4Vis; LoRec | LLM 抽取标签、aspect、用户兴趣、知识和简洁画像；输出通常被缓存并交给传统模型。 |
| 样本与 query 生成 | GReaT; ONCE; AnyPredict; DPLLM; MINT; Agent4Rec; RecPrompt; PO4ISR; BEQUE; Agent4Ranking; PopNudge; RecInter | LLM 生成合成交互、叙事偏好、长尾 query rewrite 或模拟交互。 |
| 知识抽取 | KAR; TRAWL; HKFR; LLM-KERec; ReLand; LLMRG; LlamaRec-LKG-RAG; LKPNR; DOKE | LLM 是知识生产者，而不是直接 ranker。 |
| 工业资产生成 | ReLand; LLM-KERec; AIR; AKT-Rec; Taiji; RecGPT; RecGPT-Mobile | 最强生产范式：离线/近线生成或压缩语义资产，再用标准召回/排序服务。 |

## LLM/PLM 编码器

| 子方向 | 代表工作 | 摘要 |
|:---|:---|:---|
| 子方向 | 代表工作 | 摘要 |
| 文本 item 编码 | U-BERT; UNBERT; PLM-NR; Pyramid-ERNIE; ERNIE-RS; CTR-BERT; SuKD; PREC; Tiny-NewsRec; PLM4Tag; TwHIN-BERT; RecFormer; TBIN; Social-LLM | 当 metadata 和文本关键时，编码器提升 item/user 表示。 |
| 跨域与迁移编码 | ZESRec; UniSRec; TransRec; VQ-Rec; IDRec vs MoRec; S&R Foundation; MISSRec; UFIN; PMMRec; Uni-CTR; PCDR | 用语言或多模态 embedding 支持跨域和冷启动。 |
| LLM embedding 与 adapter | LLM2BERT4Rec; LLM4ARec; UEM; CollabContext; SSNA; KERL; LLMRS; LLMHG; HLLM | 使用冻结 embedding、adapter 或层次 LLM 表示用户历史和 item 内容。 |
| 工业编码器 | PLUM item semantic representations; AKT-Rec MLLM semantic clusters; MTFM heterogeneous tokens; Meta HSTU action tokens | 编码器围绕生产行为流重构，而不是只围绕自然语言。 |

## LLM Scoring、Ranking 与 Instruction Tuning

| 子方向 | 代表工作 | 摘要 |
|:---|:---|:---|
| 子方向 | 代表工作 | 摘要 |
| Prompted scoring/ranking | LMRecSys; Zero-shot GPT; BookGPT; PALR; LLMRanker; SetwiseRank; LiT5; LlamaRec; LLM4Rerank; LLM as explainable re-ranker | 用 LLM 对候选打分或排序；适合分析和小候选集，全量工业排序成本高。 |
| Instruction tuning | TALLRec; InstructRec; GenRec; BIGRec; DEALRec; RecRanker; Recommendation as Instruction Following; Aligning LLMs with Recommendation Knowledge; RDRec | 通过 instruction、LoRA 或 distillation 将 LLM 对齐到推荐标签和任务。 |
| 协同对齐 | CoLLM; LLaRA; A-LLMRec; CLLM4Rec; LC-Rec; ControlRec; FLIP; ClickPrompt; Llama4Rec; iLoRA; CALRec | 注入 ID/协同行为信号，减少语义-协同 mismatch。 |
| 检索增强排序 | ReLLa; RALLRec; LlamaRec-LKG-RAG; CRAG; retrieval-augmented conversational recommendation | LLM scoring 前检索相关用户历史、知识或候选。 |
| 高效微调 | POD; LSAT; E4SRec; LightLM; MoLoRec/RecCocktail; instruction distillation; decoding acceleration frameworks | 降低计算、支持增量更新，让 LLM ranker 更可部署。 |

## 生成式推荐与语义 ID

| 子方向 | 代表工作 | 摘要 |
|:---|:---|:---|
| 子方向 | 代表工作 | 摘要 |
| 任务统一 | P5; M6-Rec; InstructRec; VIP5; UP5; P5-ID; RecSysLLM; UPSR | 将多种推荐任务转成 language modeling 或 instruction following。 |
| 语义 ID 召回 | TIGER; P5-ID; How to Index Item IDs; LC-Rec; IDGenRec; LETTER; Semantic IDs for Joint Search and Recommendation; GenCDR; GLASS; DaV-Gen | 生成 item identifier，而不是打分；目标是统一召回和生成。 |
| 语义 ID 改进与诊断 | Generative Recommendation with Semantic IDs handbook; Differentiable Semantic ID; Variable-Length Semantic IDs; Generating Long Semantic IDs in Parallel; SIDInspector; Qualification-Aware SID; Adaptive Collision Handling; Expressiveness Limits; LBR | 处理 collision、无效输出、长度偏差、扩展性和校准。 |
| 工业语义 ID 系统 | PLUM; SIGMA; AKT-Rec; AIR intent IDs; Taiji semantic features; Gryphon; YouTube SemanticID discussions | 展示语义 ID 如何进入真实召回和排序。 |
| 扩散与其他生成范式 | Diffusion recommendation surveys; continuous-token diffusion; session generative recommendation; POI semantic-ID generation; chain-of-recommendation | 将生成式推荐扩展到自回归文本/ID 之外。 |

## 智能体、会话与交互推荐

| 子方向 | 代表工作 | 摘要 |
|:---|:---|:---|
| 子方向 | 代表工作 | 摘要 |
| 会话推荐 | TG-ReDial; KBRD; UniCRS; MESE; Chat-REC; Large Language Models as Zero-Shot Conversational Recommenders; retrieval-augmented CRS | 自然语言偏好澄清和解释。 |
| 推荐智能体 | Agent4Rec; AgentCF; MACRec; RecMind; iAgent; MMEACR; connected-TV agentic recommendation; group recommender LLM agents; controllability-centric collaborative agents | 使用规划、记忆、反思、工具调用和多智能体协作。 |
| 用户模拟与 A/B agent | A/B Agent; RecInter; generative agents in recommendation; LLM user preference induction; LLM-as-a-judge slate recommendation | 在线实验前模拟用户、扩展标签或评估 slate。 |
| 工业 agentic 系统 | RecGPT; RecGPT-V2; RecGPT-Mobile; Ranking Engineer Agent style ads tooling; creator/advertiser matching with Gemini-like models | 将 agent 用于意图推理、工程效率或匹配流程。 |

## 可信、公平、鲁棒与安全

| 子方向 | 代表工作 | 摘要 |
|:---|:---|:---|
| 子方向 | 代表工作 | 摘要 |
| 公平与偏差 | FaiRLLM; RECLLM; job recommendation demographic bias; fairness in LLM-based recommender systems survey; provider fairness in news recommendation; popularity bias studies | 研究人口属性、provider、曝光、recency 和 popularity bias。 |
| 鲁棒与隐私 | LoRec; STELLA; exact and efficient unlearning for LLM recommendation; incremental learning; memorization behavior in generative recommendation | 处理不稳定、隐私、投毒和记忆化。 |
| 解释性 | XRec; RecExplainer; explanation generation surveys; uncertainty-aware explainable recommendation; coherent natural-language explanations | LLM 可以解释，但解释必须 faithful 和 safe。 |
| 隐私与端侧 | DPLLM; RecGPT-Mobile; federated content representation; privacy-preserving local LLM recommenders | 减少集中暴露用户历史和敏感画像。 |
| 评测与可控 | LLM-as-a-judge; user preference induction; controllability-centric evaluation; A/B Agent; length bias reduction; position-bias-aware reranking | 在静态离线标签之外评估推荐行为。 |

# 扩展逐条文献目录

完整的 250+ 条逐条 annotated catalog 保留在 PDF 和 LaTeX 源文件中。为了提升飞书可读性并避免单个超大表写入超时，飞书文档保留上面的主题地图，并在这里按方向概括目录。

- 经典与 Pre-LLM 神经推荐：Wide&Deep、YouTube DNN、DIN/DIEN、SASRec/BERT4Rec、DLRM、Monolith、PinnerSage/PinnerFormer、图推荐和会话推荐。
- LLM 特征工程与数据增强：TagGPT、KAR、HKFR、RLMRec、LLMRec、CUP、SINGLE、LLMHG、ONCE、MINT、BEQUE、Agent4Ranking 等。
- LLM/PLM 编码器与跨域模型：U-BERT、UNBERT、PLM-NR、ERNIE-RS、RecFormer、UniSRec、VQ-Rec、MISSRec、PMMRec、Uni-CTR、PCDR。
- LLM scoring/ranking 与 instruction tuning：TALLRec、InstructRec、ReLLa、SetwiseRank、LlamaRec、CoLLM、LLaRA、A-LLMRec、RecRanker、DEALRec、RecExplainer。
- 生成式推荐与语义 ID：P5、M6-Rec、TIGER、P5-ID、LC-Rec、IDGenRec、LETTER、RPG、differentiable/variable-length semantic IDs、PLUM、SIGMA、AKT-Rec、Gryphon。
- 智能体与会话推荐：Chat-REC、Agent4Rec、AgentCF、MACRec、RecMind、iAgent、RecGPT-V2、MMEACR、connected-TV agentic recommendation。
- 可信与评测：FaiRLLM、RECLLM、STELLA、LoRec、LBR、A/B Agent、LLM-as-a-judge、user preference induction、controllability-centric evaluation。


# 主要参考文献


99 H.-T. Cheng et al. Wide & Deep Learning for Recommender Systems. DLRS, 2016. P. Covington, J. Adams, and E. Sargin. Deep Neural Networks for YouTube Recommendations. RecSys, 2016. G. Zhou et al. Deep Interest Network for Click-Through Rate Prediction. KDD, 2018. W.-C. Kang and J. McAuley. Self-Attentive Sequential Recommendation. ICDM, 2018. F. Sun et al. BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer. CIKM, 2019. M. Naumov et al. Deep Learning Recommendation Model for Personalization and Recommendation Systems. arXiv:1906.00091, 2019. S. Geng et al. Recommendation as Language Processing: A Unified Pretrain, Personalized Prompt and Predict Paradigm. RecSys, 2022. Z. Cui et al. M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems. arXiv:2205.08084, 2022. K. Bao et al. TALLRec: An Effective and Efficient Tuning Framework to Align Large Language Model with Recommendation. RecSys, 2023. Y. Gao et al. Chat-REC: Towards Interactive and Explainable LLMs-Augmented Recommender System. arXiv:2303.14524, 2023. Z. Lin et al. How Can Recommender Systems Benefit from Large Language Models: A Survey. ACM TOIS, 2024. J. Li et al. Towards Next-Generation LLM-based Recommender Systems: A Survey and Beyond. arXiv:2410.19744, 2024. L. Lin et al. Large Language Models for Generative Recommendation: A Survey and Visionary Discussions. LREC-COLING, 2024. S. Rajput et al. Recommender Systems with Generative Retrieval. NeurIPS, 2023. Y. Lin et al. ReLLa: Retrieval-enhanced Large Language Models for Lifelong Sequential Behavior Comprehension in Recommendation. WWW, 2024. Y. Zhang et al. Collaborative Large Language Model for Recommender Systems. WWW, 2024. J. Liao et al. LLaRA: Large Language-Recommendation Assistant. SIGIR, 2024. J. Zhai et al. Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations. arXiv:2402.17152, 2024. L. Yu et al. ReLand: Integrating Large Language Models’ Insights into Industrial Recommenders via a Controllable Reasoning Pool. RecSys, 2024. Q. Zhao et al. Breaking the Barrier: Utilizing Large Language Models for Industrial Recommendation Systems through an Inferential Knowledge Graph. CIKM, 2024. Meituan MTFM Team. MTFM: A Scalable and Alignment-free Foundation Model for Industrial Recommendation in Meituan. arXiv:2602.11235, 2026. D. Sun et al. SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress. arXiv:2602.22913, 2026. Y. Meng et al. A Generative Re-ranking Model for List-level Multi-objective Optimization at Taobao. arXiv:2505.07197, 2025. Y. Chen et al. Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations. arXiv:2606.10357, 2026. Kuaishou Taiji Team. Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation. arXiv:2606.03866, 2026. A. Tsai et al. PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations. arXiv:2510.07784, 2025. C. Yan et al. From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs. arXiv:2605.23310, 2026. RecGPT Team. RecGPT Technical Report. arXiv:2507.22879, 2025. RecGPT Team. RecGPT-V2 Technical Report. arXiv:2512.14503, 2025. B. Zhang et al. RecGPT-Mobile: On-Device Large Language Models for User Intent Understanding in Taobao Feed Recommendation. arXiv:2605.04726, 2026. LBR: Towards Mitigating Length Bias in Large Language Models for Recommendation. arXiv:2607.04270, 2026. Seeing and Reflecting: Multimodal Memory-Enhanced Agent Collaboration for Recommendation. arXiv:2607.07108, 2026. An LLM-powered Agentic Recommendation System for Connected TV Content Discovery. arXiv:2607.09988, 2026. User Preference Induction with LLMs for Offline Top-N Recommendation Evaluation. arXiv:2607.11354, 2026. J. Zhou et al. Can We Steer the Black-Box? Towards Controllability-Centric Evaluation of Recommender Systems with Collaborative Agents. arXiv:2607.13418, 2026.
