# 2026-10-14: independent audit of earlier post-training failures

<!-- source-sha256: bb10aeed642877fd3485231594d1e24f3dbcd786a4adb2061cdcd706d1079df6 -->

[简体中文](../../research-audits/oct14-post-failure-review.md)

## Conclusion and scope

These four seed-42 diagnostics actually ran but **did not pass the GPU validation gate**. This audit is not a passed receipt and does not rewrite failures or treat parameter changes, gate fitting, or unit tests as proof of effectiveness.

All four ran at `6aabe57a97ec3a586aac7aeea66128750f9441da`. The audit read existing result, failure, launch, and exit records, implementation, and cached paper text only. No GPU, regeneration, downloads, or train/validation/test rows were opened. Previously recorded validation aggregates and costs are historical facts, not used to select follow-ups. Official test remained unopened.

| Earlier run | Actual outcome | Independent conclusion |
| --- | --- | --- |
| MBS `magicbeanstalk-s42` | No verified-hard root; exit 1 | Four items at the fixed termination budget yielded no eligible recursive root. This is not effectivity or Goldilocks success. |
| SynthSelf `synthself-gold-control-s42` | Eq. 6 failed; exit 1 | Sequence-NLL failure is correct. Separately verify asymmetric gold/rewrite EOS treatment; model mismatch alone is not established. |
| UPTURN `upturn-7b-reasoner-s42` | Zero eligible failed rollouts; exit 1 | Tokenizer paragraph boundary bug verified. Per-response evidence missing; cannot say “7B was too strong and all answers correct.” |
| UPTURN `upturn-small-reasoner-s42` | Zero informative position groups; exit 1 | Gate trained and head weights changed, but position gradients were entropy-only, not rescue learning. |

## Frozen papers and public resource identities

Affiliations come from local specs. Algorithm checks use cached v1 sources, with no new scan.

| Method | Original | Organizations |
| --- | --- | --- |
| MagicBeanStalk | [arXiv 2610.12659v1](https://arxiv.org/abs/2610.12659v1) | NVIDIA / University of Washington / Carnegie Mellon University / Stanford University |
| SynthSelf | [arXiv 2610.13113v1](https://arxiv.org/abs/2610.13113v1) | LG AI Research / KAIST AI |
| UPTURN | [arXiv 2610.13672v1](https://arxiv.org/abs/2610.13672v1) | KAIST |

| Resource | Pinned revision / SHA256 | Purpose |
| --- | --- | --- |
| `Qwen/Qwen2.5-0.5B-Instruct` | `7ae557604adf67be50417f59c2c2f167def9a775` | MBS/SynthSelf student, UPTURN encoder and small reasoner |
| `Qwen/Qwen2.5-7B-Instruct` | `bb46c15ee4bb56c5b63245ef50fd7637234d6f75` | MBS/SynthSelf teacher/aligner and UPTURN 7B reasoner |
| `openai/grade-school-math` | `3101c7d5072418e28b9008a6636bde82a006892c` | Existing train/validation holdout derived only from official train |
| Original public train content SHA256 | `17f347dc51477c50d4efb83959dbb7c56297aba886e5544ee2aaed3024813465` | Data identity in prior results |
| Train split SHA256 | `6b8672439c8cf6f6b6e65bf5f0e515fbf4c497c9066eefb62a6a6a61ced158e3` | Fixed split of normalized-question SHAs |
| Validation split SHA256 | `2cf1119ad7b2e31e825274487ef32c073e03a8ed44f08ecd3e0366c1f40ebdb7` | Historical metadata only; no examples read |

Old context cap was 4,096. MBS used four train examples and the other runs eight; all configured four validation examples. This is not formal capability comparison. Full public checkpoint hashes remain in old results/resource audits; no weights, responses, questions, or answers copied here.

## MBS: no verified-hard roots, not successful construction

The `6aabe57a` root gate requires actual target-student rollouts all failing and untruncated: `not any(rewards) and not any(truncated)`.

| Root | Actual rewards | Truncation | Accepted |
| --- | --- | --- | --- |
| 1 | `[1,1,1,1]` | `[false,false,false,false]` | false |
| 2 | `[0,1,0,1]` | `[false,false,false,false]` | false |
| 3 | `[0,0,0,0]` | `[true,false,true,false]` | false |
| 4 | `[1,1,0,0]` | `[false,false,false,false]` | false |

Budget exhaustion is not verified hardness. No root passed; raw records only `seed-hardness-calibration`. This does not establish decomposition, effectivity, synthesis, novelty, target Goldilocks, or RLVR. The “no eligible descendant” terminal message does not prove all later stages ran.

Keep the bounded construction failure. Do not relax hardness/termination, invent answers, or relabel mixed success to obtain a passing receipt. Different source or train-only root-pool experiments require independent immutable attempts.

## SynthSelf: Eq. 6 and EOS risk

Cached fixed sources show Eqs. 4–5 **sum** token log-probabilities over complete responses and average by example, not token means. Eq. 6 requires both `L(aligner) < L(gold)` and `R(aligner) > R(self)`.

| Metric | Actual value |
| --- | ---: |
| Gold sequence NLL | 69.12544560432434 |
| Rewrite sequence NLL | 76.84697580337524 |
| Rewrite − gold sequence NLL | 7.721530199050903 |
| Aligner quality | 1.0 (8/8 verified, none truncated) |
| Self quality | 0.75 |
| Empirical constraints satisfied | false |

Quality passes; NLL does not. The script actually ran two updates each for method and gold-SFT, yet correctly preserved `failed-aligner-constraints` and exit 1. Method supervised 659 tokens per update versus 762 for control; equal epochs do not equal supervised tokens. Weight changes, token means, and truncated rewrites cannot bypass Eq. 6.

Protocol risk: `synthself/checkpoint.py` encodes gold with `add_special_tokens=False`, while `ResponsePolicy.generate` retains generated EOS. The pinned Qwen EOS is ID `151645`, `<|im_end|>`. This asymmetry can affect NLL, but aggregate records lack per-response token/NLL decomposition, so its contribution to the 7.72153 gap cannot be quantified and correction is not guaranteed to pass.

Prespecify a consistent complete-response ending convention before viewing new results. Keep sequence sums and strict inequalities; never choose whichever EOS condition passes. Preserve old failure.

## UPTURN 7B: actual paragraph-boundary misses and limits of attribution

The old failure records 24 gate-training cases, eight calibration cases, and zero eligible failed rollouts; it stopped before head training. Missing response-level correctness, truncation, true paragraph counts, and detected cuts prevent distinguishing all-correct, failure without cuttable paragraphs, and missed token boundaries.

The shared `progressive_contraction.algorithm.paragraph_prefixes`, called by UPTURN construction and evaluation, searches only an isolated `tokenizer("\n\n")` token subsequence. The paper defines decoded double-newline boundaries, not a context-independent token encoding.

CPU counterexample using the existing pinned tokenizer without loading a model:

```text
text = "First step.\n\nSecond step.\n\nFinal \\boxed{2}"
token IDs = [5338,3019,382,15666,3019,382,19357,1124,79075,90,17,92]
isolated "\n\n" token IDs = [271]
token ID 382 decodes to ".\n\n"
Actual double-newline boundaries = 2
Old paragraph_prefixes = []
Original-token cut indices should be [3,6]
```

CPU used existing `.cache/oct14-skill-public-transfer` tokenizer: `tokenizer.json` SHA256 `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539`; `tokenizer_config.json` SHA256 `5b5d4f65d0acd3b2d56a35b56d374a36cbc1c8fa5cf3b3febbbfabf22f359583`. Both match the pinned Qwen identity.

Fix contract: detect decoded double newlines, map them back to original generated-token endpoints, and retain original `tokens[:cut]` without reencoding. Sort, deduplicate, cap, and reject response-end cuts or `cut >= Lmax`. The shared helper affects Progressive Contraction too; regress both call paths. Freeze and test source before new GPU runs; the paragraph definition stays unchanged.

The bug can alter eligibility, but the CPU example does not explain every old 7B outcome. Preserve the failure and do not relabel it “7B too strong.”

## UPTURN small: entropy updates are not rescue learning

Both reasoner and encoder were fixed 0.5B. Gate made 20 BCE updates with five train and one calibration sample and binary training labels. BCE fell from `0.650352418422699` to `0.0020837492775171995`; one calibration item does not establish reliable gate quality.

| Position step | Sampled cuts | Rescue rewards / advantages | Gradient L2 | Loss |
| --- | --- | --- | ---: | ---: |
| 1 | `[197,172,442,137]` | Four zeros / four zeros | 0.000027731650334317237 | -0.0013861844781786203 |
| 2 | `[280,537]` | Two zeros / two zeros | 0.0001910477294586599 | -0.0006919213919900358 |

`position_loss` centers group rewards; both surrogates were zero, so loss was `-0.001 × entropy`. The optimizer ran and parameter digest changed, but `position_informative_groups=0`: no nonzero rescue-advantage learning. `failed-no-rescue-signal` and exit 1 were correct.

This is negative evidence on actual sampled cuts, not proof that all cuts, budgets, or reasoners always fail. Missed paragraph boundaries also limit coverage. Entropy updates and gate fitting cannot sign a rescue-learning pass.

## Verified actual costs

From prior raw `cost` and `exit.json`; generation calls are API invocations, **not response counts**. Separate limits, loading, and unexecuted stages from observed costs.

| Earlier run | Generated tokens | Scored response tokens | Frozen encoder forwards / input tokens | Wall seconds | Exit |
| --- | ---: | ---: | ---: | ---: | ---: |
| MBS | 6,282 | 0 | 0 / 0 | 85.59944366663694 | 1 |
| SynthSelf + gold control | 6,076 | 4,263 | 0 / 0 | 164.40409300103784 | 1 |
| UPTURN 7B | 7,556 | 0 | 32 / 11,220 | 79.60914537124336 | 1 |
| UPTURN small | 25,532 | 0 | 40 / 21,793 | 250.56925148144364 | 1 |

- MBS: evaluation four calls/1,541 tokens, target calibration four/4,741; no construction, rescue, or training records.
- SynthSelf: evaluation 12/4,560, aligner eight/659, self rewrite eight/857. Initial NLL scoring 1,421 tokens; method and gold-SFT together 2,842. Existing validation cost is included, not rerun.
- UPTURN 7B: training rollout eight/7,556; no rescue, gate, or position updates.
- UPTURN small: training rollout eight/13,843, rescue training six/2,241, original evaluation four/3,310, extra base four/5,246, corrected evaluation six/892. Equal maximum token budgets do not imply equal usage or time.

## One minimal bounded follow-up (not executed)

A training-only protocol proposal, not authorization, a pass, or a result. Fix the protocol, pass CPU contracts, freeze source, and obtain a GPU slot before an independent immutable attempt. Historical source bindings remain unchanged.

Keep the same eight training items, seed 42, and public revisions. No validation/test, dataset expansion, model replacement, or retries.

1. SynthSelf: eight aligner and eight self greedy rewrites, `max_tokens=512`. Prespecify exactly one EOS for complete responses on both sides and recompute Eqs. 4–6. This is construction/NLL only, with no LoRA/SFT/evaluation; it cannot replace later SFT acceptance.
2. UPTURN: after fixing cut mapping, use the same eight train items, 7B reasoner, 0.5B encoder, `group=4/max_tokens=768/max_cuts=16/cuts=4/suffixes=2`, 20 gate epochs, at most two position steps, no assessment. If eligibility remains zero or rescue advantages are all zero, record failure and stop.

Strict combined cap: 64 outputs, 45,040 generated tokens (SynthSelf ≤8,192, UPTURN ≤24,576 originals +12,272 suffixes), 32 frozen-encoder forwards (≤4,096 input tokens each), 16 sequence-NLL scores (≤4,866 response tokens: original gold 762 plus eight EOS and ≤4,096 rewrite), zero LoRA updates, 20 gate updates, at most two position steps, ≤1,200s overall. The 762 gold count comes from old aggregate, not newly reading/selecting rows. Fail on identity or length mismatch. No transferring unused budget to new settings/items. Changes require new runs; do not append trials after failure or test.

## Old raw index and SHA256

Raw files are locally ignored; no questions, answers, checkpoints, or logs committed. Paths below are relative to shared repository prefix `.cache/oct14-post-training/post-raw-attempt01/`. Hashes bind the original bytes. `launch.json` and `runtime.log` contents are not copied.

| Run/file | SHA256 |
| --- | --- |
| `magicbeanstalk-s42/launch.json` | `fc1675dc64ca98b49f5086fd8191fa9f8b07417f6df184a372787f8375e8b484` |
| `magicbeanstalk-s42/exit.json` | `a18d57f66dba8964ccc8219e56ee099bffdf24f8ce60fe78266365ce0cb69c33` |
| `magicbeanstalk-s42/runtime.log` | `f32d9cf8aff30e551a39f29c53f2b75cf21097db0c3536c0a38f406abfaa472e` |
| `magicbeanstalk-s42/evidence/failure.json` | `5fd3a7305d462e1caf2dd0c24b3898b2fb9d5c167f1bff999200f5e312099bca` |
| `synthself-gold-control-s42/launch.json` | `d1cc894c71d3c127a34a1cb8fa55b944c0085b328a98b626a51a37953502063f` |
| `synthself-gold-control-s42/exit.json` | `3bd063b3009b81675ece2d9a0ed0e10ffb6fb90e96b2a4b3877bf234f23157aa` |
| `synthself-gold-control-s42/runtime.log` | `880e4af216d08cefe784985889df3597f18d2266a1a7b25903b99a42507626c9` |
| `synthself-gold-control-s42/evidence/result.json` | `33280c1a0cc3357e15fd9d9d7e9059baa8422aef1e32608d741c94bae3d3f21f` |
| `upturn-7b-reasoner-s42/launch.json` | `267075019fae72a16e7fd3fb2c121675ee6dd22712f8f6081d0895ac6fb8ae8a` |
| `upturn-7b-reasoner-s42/exit.json` | `ed44bbcb038ac5569fa450793ec3b7f6ea862ef49096a47b422c0e0a883bf2cb` |
| `upturn-7b-reasoner-s42/runtime.log` | `7ecf87b51732d48ba4683b467cfb41e22dcbc5ae3ac4d9d308a77b9fc335cbf6` |
| `upturn-7b-reasoner-s42/evidence/failure.json` | `95fea3546302fb434623c8ca84ee9993b707a8c7d1ac124b32176c068752cb8b` |
| `upturn-small-reasoner-s42/launch.json` | `2c83fd1062bea40676741ee28e53e1d703e9718a1a11cb79536132cfd6772860` |
| `upturn-small-reasoner-s42/exit.json` | `668197efb374eecadc9571e5478b58fa2321509b1ca351212580788ca94e152a` |
| `upturn-small-reasoner-s42/runtime.log` | `6460c7e06ec1bc4c381794fa60f006b5f91a71fe551d111f6d822043fe64b857` |
| `upturn-small-reasoner-s42/evidence/result.json` | `779c3d7675edca755d5d246530f136d47440b2231544dcb3d0567275950cca87` |

The source6a execution hashes below come from the pinned maps in `launch.json`, not the later worktree.

| source6a file | SHA256 |
| --- | --- |
| `scripts/run_oct13_post_training.py` | `f482471e2c33189bcfed7c02fce0e79fb58ba9606a3a354c12ee2a63bfca8f6b` |
| `src/auto_research/post_training/oct13_common.py` | `739f276633d74a85ba790e4d6df25504bce89950c40867ed57302cde03f1ada9` |
| `src/auto_research/post_training/response_policy.py` | `e380a5b4d1d53974b973b72b7d9ad6328129dc8c9bae4d233f6c1cbdf8508bf7` |
| `src/auto_research/reproductions/magicbeanstalk/checkpoint.py` | `f509334fea6b6db2e68668bb7957e8f6e29c522e63012be440779b9346d1c9e0` |
| `src/auto_research/reproductions/synthself/checkpoint.py` | `9835b086272d9262f057a0fc0975d19ff3b84d5e1766cc234ca1e11985164891` |
| `src/auto_research/reproductions/upturn/checkpoint.py` | `83ac66cead272cb391fe27c56f838df5414712283db42f2b8088d3509de311f3` |
| `src/auto_research/reproductions/progressive_contraction/algorithm.py` | `176743356415111e3e19a26427cf59391b4b84b56697adf8d3fe3038ad0de3c1` |

Checked cached `.cache/oct13-scan/fulltext/2610.13113v1.html.html` (SHA256 `c9efb4a2c920629101e847e312be5fcc08a6adf85d47017deecae300750ef803`) and `2610.13672v1.html.html` (SHA256 `56ae1afa9358c70e86988f45a097d95e1453b8489fb11edc7c1b8b032f33d0a4`). Keep algorithms, old measurements, CPU counterexamples, and unexecuted suggestions separate. Subsequent changes or runs cannot overwrite source6a failures.
