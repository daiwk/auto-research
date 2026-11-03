# Recent paper scan: 2026-09-26

<!-- source-sha256: 62045e3d6dfdcbcccbcb1323c17141fecaf9e1dd076b9585502fdd819f722a5a -->

[简体中文](../recent-paper-scan-20260926.md)

First publication September 20–26, 2026 with two days of overlap across industrial search/ads/recommendation, foundations, post-training, agents, multimodal and System One. Google/Meta receive priority full-text checks. The export API returned HTTP 406, so candidate search and official abstracts/HTML were checked individually. **Neither exhaustive paging nor an automatic watermark advance.** Keep unimplemented records pending until code, public comparison and docs are done; author online metrics are not repository offline results.

| Priority | Paper | Paper evidence and mechanism | Local state |
|---|---|---|---|
| P0 | [Google/YouTube Light Heads](../reproductions/2609.25433-light-heads/README-en.md) (2609.25433, Sep 21) | Gradient-isolated shallow heads, resets, cross-model configuration; §5.2 engagement +0.03%, low-quality exposure −0.40%, vertical +13.83% | Dynamic injection, isolation and two ablations; three-seed MovieLens, negative reset result retained |
| P0 | [Google/YouTube Music LLM Rationales](../reproductions/2609.23877-music-rationales/README-en.md) (2609.23877, Sep 20) | Async LLM profiles, candidates and rationales, KG canonicalization, offline judge, online fallback; §4 two-week multi-arm A/B | Last.fm and real 7B/A100 offline generation, catalog/rationale checks, nomination vs explanation-only and cache fallback; test hit 0.38 vs CF 0.40, not online rationale effectiveness |
| P0 | [UNIQUE](../reproductions/2609.23718-unique/README-en.md) (2609.23718, Sep 20) | Flat quantization, early fusion, isolated target attention and joint loss; §4.4 one-week full-traffic A/B: watch duration +0.96%, distribution +1.08%, retention +0.70% | Three-seed KuaiRand-Pure joint/ablation experiment on CTR-AUC and code coverage; no stable lift |
| P0 | [MuSeR](../reproductions/2609.23677-muser/README-en.md) (2609.23677, Sep 20) | Hierarchical compression, multiple interest queries, alignment; online DAU +0.26%, session duration +0.89% | KuaiRand multi-interest training and full-catalog ablation; public labels proxy private LLM/BGE semantics |
| P1 | [Meta layered engagement evaluation](../agent-research/layered-engagement-protocol.md) (2609.25408, Sep 21) | Labels → classifier → online calibration; eight post-freeze experiments, 113 comparisons and F1 81.1% | Pre-exposure freeze gate, paired bootstrap and decision intervals; no private scorer/coefficients/public paired A/B, not paper effectiveness |

An eligible industrial P0 is not automatically implemented. Preserve defining mechanisms, fair public baselines, validation/test isolation, metadata, figures and actual metrics. Disclose inaccessible private production paths instead of renaming heuristics. Continue overlap from September 20 until API-equivalent full paging and terminal diffs recover.
