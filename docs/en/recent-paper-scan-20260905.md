# Recent paper scan and implementation: 2026-09-05

<!-- source-sha256: 2eb5841c44cd7c9dd13c3777bb3ecc7214e539d3df14af1addec3d6d3b446e94 -->

[简体中文](../recent-paper-scan-20260905.md)

## Scope and evidence

August 31–September 5, 2026 across industrial search/ads/recommendation, foundation/multimodal, post-training and agents. Broad queries returned 37/297/96/208 candidates respectively. Hits are not implementation plans; irrelevant titles, surveys, applications and papers without independent public experiments receive terminal ledger decisions. Full text is checked for A/B, rollout and deployment, irrespective of the abstract. Google Research/DeepMind official sources had no qualifying new paper; Meta Publications returned HTTP 500, so official-site search supplemented it and the source failure remains recorded.

| Track | Paper | Priority | Entry evidence and local method |
|---|---|---|---|
| Industrial recommendation | [ReST](../reproductions/2609.01240-rest/README-en.md) | P0 | One-week A/B, core revenue +11.93%, full rollout; dual-gated sequence and shared prefix |
| Industrial recommendation | [TGR](../reproductions/2609.00986-tgr/README-en.md) | P0 | Multi-surface A/B/full launch; CCFormer, hierarchical generation and reason tokens |
| Industrial recommendation | [CAMIE](../reproductions/2608.30255-camie/README-en.md) | P0 | Snap DPA aggregate CTR/CVR gains and deployment; co-engagement multimodal embeddings |
| Industrial recommendation | [SetMIR](../reproductions/2608.30251-setmir/README-en.md) | P0 | Production retrieval CVR +3.1%; interest sets, presence and query NMS |
| Post-training | [GAPO](../post-training/2609.00444-gapo/README.md) | P1 | Official code and public math/code benchmarks; group-adaptive clipping |
| Agent | [DRACO](../agent-research/2609.04094-draco/README.md) | P1 | Official code, AppWorld/Tau-Bench; dynamic rubrics and closed-form step credit |

All have metadata, method, original figures, equations, code, metrics, boundaries and Evolve mapping. Four industrial papers use three-seed MovieLens-100K, and GAPO/DRACO use deterministic mini-suites.

## Resource update: 2026-09-06

- [Random Attention](../reproductions/2609.03430-random-attention/README-en.md): core, equal-budget Qwen checkpoint KV test on A100 and Evolve.
- [Lngram v2](../reproductions/2609.03426-lngram-v2/README-en.md): discrete routing, memory readout, counterfactual gradients, real VLM hidden states on A100 and Evolve.
- [CORAL](../reproductions/2609.02730-coral/README-en.md): reversed abstract-level rejection after multiple full-text A/B/deployment confirmations; implemented.
- [RecEvolve](../reproductions/2609.01622-recevolve/README-en.md): recovered by arXiv-ID-month late-arrival scan; multi-round controller implemented.

Other hits have terminal [ledger](../paper-discovery-ledger.json) decisions. Continue from **2026-09-05** using API public dates, announcement overlap and arXiv ID month to catch revisions, delays and late indexing.
