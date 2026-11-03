# Local closeout checkpoint, 2026-10-13

<!-- source-sha256: e6093e0f78040314bf01fd3698e381c36430b0fc79664cdea23b0171bc414670 -->

[简体中文](../../research-audits/oct13-local-closeout.md)

This page preserves the October 13 network-pause checkpoint. The user explicitly resumed GPU work on October 14.
A100/A30 connections and relevant public resources were verified, and actual runs continued under the [GPU TODO](../../research-audits/oct13-gpu-todo.md).
This is neither final acceptance of all 19 papers nor a claim that all CI checks passed.

## Local work preserved

- Fixed scope for 19 papers, independent adapters/entry points, Chinese metadata, core mechanisms, and local limits.
- New figures and method screenshots use pinned original versions, consistent asset names, source byte SHA, page/crop settings, and Chinese captions. Papers without architecture figures use algorithm blocks or method excerpts; redraws are not represented as originals.
- Completed UxSID's three catalog views, 19 expected registry keys, and generated README, manifest, catalogs, and public dashboard.
- GPPO/TAPO retain actual independent GRPO controls, paired differences, and six real optimizer updates. DoubleCat retains negative results such as all-whitespace collapse across three seeds.
- Pin revisions only for the 19 papers actually checked; do not default others to v1, advance the review watermark, or claim exhaustive sources.
- Preserved label-access role inventory and isolation tools; neither is capability or GPU acceptance evidence.

## Actual checks

| Check | Observed result and scope |
| --- | --- |
| Full `python -m pytest` | Fixed five initial catalog/README/figure contract failures. An October 14 intermediate run had 2021 passes and two dashboard failures. After fixing and freezing source: **2034 passed, 24 warnings, 308.15 seconds** |
| Targeted public dashboard | Eight passed. Filter boolean implementation contracts with no numerical measurement, retain original contracts and index counts, and support `public_id` dataset labels. Both fixes are included in the full passing run |
| Source regressions before GPU resumption | 68 passed for ReplaySSM, NEAR/Beyond, MBS, and dashboard, including GDN all-rejected empty history, forced nonpromotable diagnostics, and separate teacher/student costs |
| Failed and related contracts rerun | 59 passed: docs navigation, registry, original figures, README sync, metric migration, math formatting, GPU curation, and isolation tools |
| CV-OPD/OAL algorithm reruns | 12 passed. Both start at seed 42; dedicated formula cases use seeds 2/11 respectively. L0 behavior contracts only, not multiseed capability experiments |
| Compilation / Ruff / whitespace | Passed |
| Paper specs check/validate | Passed |
| Fidelity inventory | Auxiliary inventory matches 140 files; not a full semantic proof |
| Metrics v2 migration | 763 artifacts, zero changes pending; raw measurements and diagnostic tiers unchanged |
| Platform completion audit | Passed metadata contracts; does not verify missing GPU artifacts are complete |
| Discovery/implementation reconciliation | Exit 0; no watermark advancement |
| Isolated base wheel | Built/installed offline with cache. Metadata/help/init passed without optional ML runtime imports |
| MkDocs strict | Passed. Twelve new repository code links now point to GitHub rather than nonexistent site paths |
| GPU evidence gate | LeWAM, SmolWAM, and one curriculum seed verified; six papers still missing, so gate failed. Other curriculum arms/seeds remained incomplete; old snapshots and entry points are not substitutes |
| New-snapshot regression | 110 passed on `0f5dca9f`: skill JSON schema, robot training candidates and isolated loading, MBS paired root budget, and four curation tools. Ruff and diff checks passed |
| Full new-snapshot rerun | Only failure was State-OPD metadata hardcoding the old receipt date. Explicitly switched to October 14 three-arm receipt and nine-run/source constraints; 12 targeted checks passed. Full rerun still needed on the final fix |
| SkillDreamer defining-path gate | Curator rejects each seed lacking actual CSI, real gallery loading, or tool execution, and checks episode and aggregate counts. Eight curation regressions passed; not a GPU pass |
| Subsequent full regression | `32f873e7`: **2148 passed, 24 warnings, 274.05 seconds**. Later SmolWAM NumPy/adapter-only fixes passed 81 targeted world-model/LeWAM checks, not final full-snapshot acceptance |
| Bounded post-training diagnostics and curriculum | Frozen diagnostic entry `51b4718a`; 55 diagnosis, curriculum curation, and post-spec checks passed. Train-only diagnostic, not a full-method capability receipt |
| New artifacts and dashboard regressions | A new nested dataset-protocol label case failed then passed. Dashboard/catalog/model spec/post spec/negative results 48 passed; world-model curation/negative results/dashboard 42 passed; SOAR train-only format probe 13 passed. None substitutes for GPU runs |
| Full continuation checks | After world-model, post-training diagnostic, and metric integration, **2245 passed, 24 warnings, 294.48 seconds**. Later probes still need targeted checks. Ruff, compilation, and 140-file inventory passed; 779 artifacts, zero migrations. Six GPU gaps remained |
| Complete first-seed results | SynthSelf/UPTURN/Contraction seed-42 native and receipts independently rederived from raw, checking respectively 53/53/52 frozen Git source files. 36 curation tests covered wall-clock limits, actual validation count, EOS, effective gradients, and mechanism gates |
| Later interface fixes | 52 lead-review checks for strict SkillDreamer prompts and new probe source binding, plus 47 checks for MBS/SOAR response logs and contracts. CPU fixtures are not additional GPU runs |
| Docs and metrics at checkpoint | Strict build passed in 10.21 seconds; 787 metrics, zero migrations, 740 dashboard entries. MBS, SkillDreamer, and SOAR receipts still missing |
| Subsequent full regression | Prompt binding, response traces, and three-seed curation: **2372 passed, 24 warnings, 281.20 seconds**. Predates the group-advantage numerical fix and does not replace its final full rerun |
| Equal-reward numerical fix | Nine new cases initially failed. After repair, 40 numerical checks and 116 including related contracts passed. Independent review confirmed real reward gaps still produce gradients and updates. New CUDA check pending; stopped only the old A30 curriculum queue and preserved affected results/interruption records |
| Intermediate full regression failures | 2412 passed, 17 failed, 24 warnings, 276.84 seconds. All 17 were new observer-binding tests collected before updating the old entry point, not a full pass. On `92c20818`, 27 observer and 40 numerical checks passed; final full rerun still needed |
| Independent three-seed raw recomputation | Recurated SynthSelf/Contraction native artifacts and individual receipts from actual raw. UPTURN native/cohort matches raw field by field for passing 42/43 and failing 44; 71 tests passed. Descriptive three-seed statistics are not three UPTURN mechanism passes |
| Independent older curriculum failure audit | Raw records confirm eight finished, two interrupted, and five unstarted. Public negative audit matches. Do not remove spurious updates to issue a pass or change old raw |
| Stable snapshot full rerun | On `5c863ab8` with synced dashboard/manifest: **2474 passed, 24 warnings, 285.02 seconds**. Ruff, compile, 140-file inventory, README sync, spec check/validate, and platform audit passed; 793 metrics, zero migration; strict docs 10.80 seconds. Later curators/observers/results need checks; GPU gaps remained |
| SOAR three seeds and five curriculum runs at seed 42 | Lead review recalculated native/receipts from six actual SOAR runs and stage-native from five post-fix curriculum seed-42 runs; fields matched. 85 curation/spec tests passed. No curriculum three-seed receipt at this stage; retained negatives and exact-zero groups. MBS/Skill still unaccepted |
| Stable optional-format snapshot | `f92413aa`: 178 lead-review tests, then **2698 passed, 24 warnings, 292.33 seconds**. Independently replayed three actual MBS failures and eight SkillDreamer no-submission validations; 84 related Skill checks passed. Negative evidence is not a GPU pass |
| Actual CPU grammar backend | On A100 system, verified 54 frozen files and public student/teacher weights byte by byte. XGrammar 0.2.8 compiled five operation schemas using actual Qwen tokenizer/vocab 152064; no CUDA initialization or model load. A separate MBS CUDA attempt uses the new source and same budget; CPU compilation is not that result |
| Minimal install and protocol sync | New base wheel passed metadata/help/init in a disposable no-ML environment without optional XGrammar/TVM-FFI imports. Of 800 metrics, six needed migration: three UTF-8 only and three `claim_policy` additions. Values, evidence tiers, and raw SHAs unchanged; generators fixed together |
| Targeted protocol-fix checks | 142 curation/migration and 113 curriculum receipt/dashboard/catalog checks passed. Zero migrations for 800 artifacts; platform, specs, README sync, and discovery closure passed; strict docs 10.46 seconds. Receipt factory accepts only 15 actual runs; fixtures did not sign a receipt. GPU gaps remained |
| Fifteen actual post-fix curriculum runs | Independently replayed five arms × seeds 42/43/44 field by field and verified 54 algorithm files and observer bindings. 151 real updates and 38 exact skips of equal-reward groups; new A30 three-seed receipt saved. 101 targeted curriculum/MBS checks passed. Preserve negatives and earlier native artifacts |
| Field order and stable full suite | `ce4a4a34` order fix passed 128 lead-review checks and 47 launcher fixtures. Real CPU grammar accepted question-first and rejected answer-first. Stable full **2750 passed, 24 warnings, 297.50 seconds**; includes f924 negative curation and 15 curriculum receipts, not later attempt07 curation |
| Two actual MBS format-constrained failures | f924 and ce4 CUDA runs both exited 1; valid JSON is not a valid descendant. 36728/36425 generated tokens and zero RL updates. Retain raw responses, costs, and independent sources; no passing receipts. MBS and SkillDreamer still missing |
| attempt07 lead review and full rerun | 35 drift negatives omitted the actual validator call. Added rejection assertions; 111 negative evidence and 153 schema/migration/dashboard checks passed. Two schema-negative natives independently replayed from nine actual sources each and 54 Git files, field-equal. Stable full **2787 passed, 24 warnings, 276.28 seconds** |
| New negative-result generation | 803 metric artifacts, zero migrations; attempt07 UTF-8 formatting only, unchanged JSON values. Dashboard 756; manifest/catalog/platform/spec/README/discovery/140-file checks passed. Strict docs 10.71 seconds. Only MBS and SkillDreamer GPU gaps remained, not all CI green |
| Short teacher diagnostic and Skill curator fixes | `dd54035d` independent teacher entry plus `ac5807dd` strict seven-field recomputation, actual environment steps/failure cost, and pre-write validation. Stable full **2878 passed, 24 warnings, 304.79 seconds**. Actual seed-42 fields/calls/environment counts independently verified; 43/44 still running and fixtures not used for receipts |
| Teacher sampling configuration isolation | `4c4710cd` leaves default randomness unchanged; False only changes teacher independent solving/JSON. 21 new cases, **174 related passes**. Full run explicitly bound inner source, exited 0 with 24 warnings; double-quiet output had no count, and later collect-only includes new curation tests. No full MBS GPU result from this source; keep scaffold, effectivity, Goldilocks, and effective-update gates |
| Incorrect test entry source | Initial full run omitted `PYTHONPATH=src`, importing an older outer editable installation and causing 126 collection errors, not branch algorithm outcomes. Reran bound to current inner source without changing dependencies or weakening tests |
| Independent public teacher diagnostic curation | 96 targeted checks. 14 actual responses/3876 tokens matched frozen runner, 54 core Git files, ten source SHAs, and 28 call snapshots, sanitized field by field. Zero student generation and optimizer steps. Public native is not a GPU pass; four validation cases are not stable gains |
| Greedy path launcher and real CPU check | 84 launch/drift/process-group isolation checks. On A100, reverified 54 source files, seven student and eleven teacher files, and train-only split byte by byte. Five-operation new-source CPU compilation passed without CUDA. Only False was added, with unchanged data/retries/steps/tokens/wall budgets; full GPU had not run yet |
| Teacher protocol and docs sync | New native adds seed and actual dataset fingerprint with unchanged values/source SHAs. 804 metrics, zero migration, 757 dashboard entries; manifest/catalog synced; 73 checks passed. Strict build 10.52 seconds does not replace two missing receipts |
| Independent full SkillDreamer three-seed check | Recomputed same-source 42/43/44 three-arm outcomes, seven fields, raw/trace SHAs, CSI, actual skill loading, and successful environment operations. 1931 responses/195501 tokens; method 348 CSI, 44 loads, 285 successful calculator calls, zero submissions. Three-seed mechanism receipt passed contract and 108 curator/observer checks, without capability or efficiency claims |
| Real MBS negative result on new profile | `4c4710cd` A100 seed 42 alone exited 1 naturally, 314.887 seconds/34814 tokens. Root 4 baseline student 25%/teacher 100%; two other roots independently solved incorrectly, with no descendants or RL. Replay matched all 77 responses and construction audits. Sanitized failed native saved, no passing receipt; 43/44 unstarted, pool expansion awaited user choice |
| New tooling full regression and link repair | Initial full 2988 passed, one failed, 24 warnings, 312.56 seconds; new MBS negative artifact lacked README link. Added it and passed 11 docs contracts, then **2989 passed, 24 warnings, 293.95 seconds**. Local JUnit retained; prior exit 1 and failed MBS acceptance unchanged |
| Source-role inventory and generation sync | Only MBS checkpoint line numbers changed; 140 access expressions/scopes/fingerprints unchanged. Regenerated after review. 806 metrics, zero migration, 759 dashboard entries; specs/platform/README/discovery passed without watermark movement. Latest strict 10.75 seconds; only MBS GPU evidence missing |
| Final local regression after cost deferral | Delivery source `636e5e885ef1d1b7dc5086ed0b55a323de641d35`: **2994 passed, 24 warnings, 354.20 seconds**; JUnit confirms zero failures/errors/skips. Ruff, compileall, 140-file source inventory, specs, platform audit, and active CUDA gate passed. 32 targeted tests cover nonrunnable deferral, original spec preservation, and rejection of missing active receipts. 806 metrics, zero migrations, 759 dashboard entries, manifest/catalog regenerate without drift. Isolated base wheel installs only NumPy and passes metadata/help/init; MBS unregistered. CI verified separately; local/L1 checks are not gains |

Early full passing results bind source `34148c2e29c01e9be7e4d5b8cbd09fd0f6016902`. Later full and targeted checks are listed separately above; source changes require relevant new verification.
**Latest delivery decision (2026-10-14):** The user deferred full MBS and added a mandatory cost gate. Its unchanged CUDA spec is archived as `deferred-spec.json`, removed from active registry/batch reproduction/public runners, and marked too costly, not reproduced for now, pending acceptance in catalog and details. No invented receipt, disabled gate, or rewritten failure. Delivered 18 active mechanism implementations; the unified GPU gate actually exited 0. The 32 new tests cover nonrunnable deferral and rejection of missing receipts for active adapters. Source and prior real artifacts remain; watermark stays October 12.

Check the final PR's CI independently on GitHub; local success is not merge readiness. Earlier gaps and pending choices in the table are historical and do not supersede the latest decision above.
Original execution snapshot was `ccad3e679787f6f5383b8bd3dd1c7b58e7c8c5d0`; local tools/docs closeout was committed afterward.

## Cleanup and retention

The built site, base wheel, disposable install environment, and six page/SVG previews can be regenerated and were cleaned after checks.
Retain committed original figures, actual results including failures, GPU receipts, source checks, pinned PDFs, and public data/weights for resuming GPU work.
Preserve the user's outer workspace changes, do not recreate `uv.lock`, and do not clear whole caches.

Continuation check on 2026-10-14: temporary site, base wheel, disposable environment, and six previews were cleaned,
freeing about 346 MiB. Two original PDFs and public resources remained. The interruption lost no source or results.
After this strict build, cleaned about 299 MiB of regenerable output without removing public resources or results.
A subsequent strict build passed in 10.47 seconds and its ~302 MiB temporary site was cleaned. Later results prose still needs the final snapshot build; intermediate checks are not final CI.
After strict docs for complete first seeds and new negatives, removed `.cache/oct14-docs-site-05250ae2`, freeing about 303 MiB. Raw failures, public resources, active runs, and source archives remain.
After strict docs for `5c863ab8` three-seed results and MBS prompts, removed `.cache/oct14-docs-site-5c863ab8`, freeing about 304 MiB without removing data, weights, raw failures, or run directories.
After isolated `f92413aa` base-wheel verification, removed the disposable wheel and venv, about 45 MiB. Immutable sources, public resources, active runs, and failure evidence remain.
After protocol sync and new negatives built strictly, removed about 305 MiB of site output, not actual results, public weights, or active runs.
After strict docs for two schema failures and full curriculum, removed `.cache/oct14-docs-site-ce4-negative`, about 306 MiB. Raw responses, failures, and reusable public resources remain.
After strict docs for the short teacher diagnostic, removed `.cache/oct14-docs-site-quality-6cf83b0e`, about 306 MiB. Active GPU results, failures, public weights, and frozen sources remain.
After strict docs for full SkillDreamer and new MBS negatives, removed `.cache/oct14-docs-site-skill-mbs-closure`, another ~306 MiB. All actual raw, failures, public resources, and immutable source archives remain.

After the mandatory-cost-rule strict build, cleaned about 306 MiB of separate temporary output. Final delivery also cleaned a 306 MiB check-only site, ~3.1 MiB wheel, and ~42 MiB base environment (~351 MiB total). Reports, failures, frozen source, and reusable public data/weights remain.
After matching three staged SkillDreamer raw copies to committed bytes, cleaned `.cache/oct14-skill-full7b-curation-47f0e9ce`, about 5.6 MiB. Original observer/trace/launcher directories and committed raw remain.

## Next resumption order

1. After the user explicitly resumes GPU work, recheck actual source and public-resource SHAs. Unknown transfers are not successes.
2. Follow GPU TODO for the two missing receipts at this checkpoint. Default three-seed plans for SynthSelf, Contraction, SOAR, and repaired curriculum ran; UPTURN ran three seeds but 44 failed. Verify actual runner arguments and budgets behind unified adapters.
3. Issue source-bound receipts only for actual completed runs or explicitly preserved failure boundaries; old receipts do not validate new algorithms.
4. Regenerate and check catalogs/metrics, run full pytest, GPU gate, and CI, then submit the planned single PR without automatically merging or deploying.
