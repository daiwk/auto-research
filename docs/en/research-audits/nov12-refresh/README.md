# November 12 official-source recheck: SensorWM backfill and priority protection

[简体中文](../../../research-audits/nov12-refresh/README.md)
<!-- source-sha256: 34533478c54de97f1fb6c914a98058ca22771703de2e5dc7088c2b235063f326 -->

No new arXiv announcement was established. The eight official `new` pages are **byte-identical** to the prior captures and still display November 11. The same announcement is not recounted, and discovery dates do not replace original publication dates. The [source delta](../../../research-audits/nov12-refresh/source-coverage.json) and [official-lead review](../../../research-audits/nov12-refresh/priority-review.json) retain evidence and coverage limits separately.

## One historical Google backfill

[SensorWM / Personalized health coaching](../../../multimodal-models/2611.08568-sensorwm-planning/README-en.md) was first published on **November 5, 2026**. Google's November 11 blog triggered this primary-source recheck. Its old `not_selected_p2` entry was a title-and-abstract selection screen, not a method, cost, or experiment review. This delivery preserves that frozen record and adds a P0 backfill supported by verified author affiliations.

The full work includes second-order action-conditioned latent dynamics, joint-encoder rollout/path/SIGReg training, and paired evaluation of LLM plans grounded in conditional projections. The local implementation covers only **CPU ranking arithmetic from Eqs.55–56**:

- Compute benefit from externally supplied future status-quo and candidate endpoints, rather than substituting the current observation for the future control.
- Compute effort using the individual's historical standard deviations and three floors; retain externally feasible candidates with benefit strictly greater than 0.1.
- Return candidate IDs and mathematical scores, not health advice, health-age estimates, or clinical safety decisions.

No SensorWM encoder, transition model, forecast endpoints, candidate grid, or coaching Agent is provided locally. The blog's 125 scenarios do not specify the unpublished grid parameters. Conditional projections learned from observational data are not identified causal intervention effects.

## Cost and evidence boundaries

The complete experiments depend on private Fitbit records from 96,957 people spanning about 2.28 million person-weeks, access-controlled WEAR-ME data, paired generation, and repeated model/expert evaluations. The paper does not disclose total accelerator hours; no local duration is invented. The complete campaign is **high cost, not reproduced, review DONE**. No large resources, trial training, automatic retries, or Evolve integration are introduced.

The CPU arithmetic kernel was executed with seeds 42, 43, and 44. Seeds only permute explicit fixture candidates; they are not independent clinical samples. Evidence remains `l1_mechanism` / `diagnostic_only`, not a world-model, medical, or Agent capability comparison. This directory contains the frozen-source proof and raw execution; see the [component artifact](../../../multimodal-models/2611.08568-sensorwm-planning/metrics/component-cpu-seeds42-44.json).

```bash
PYTHONPATH=src python scripts/run_sensorwm_planning.py --check
```

This checks the committed source/execution/metric chain without uncommitted web caches or full paper experiments. There is no CUDA path, so no A100/A30 receipt is fabricated.

## Official-source priority protection

New regressions first reproduced two URL variants failing to reopen old P2 selections: `www.research.google` and `research.meta.ai`. The implementation now normalizes only the exact `www.` prefix and recognizes Meta's current official domain. Lookalike domains, similar repository names, and an abstract mentioning “meta-learning” do not establish institutional priority.

This is a **full-text review signal**, not proof of affiliation, eligibility, code release, deployment, or A/B evidence. The historical SensorWM snapshot lacks complete institutional provenance; these domain omissions cannot be asserted as its sole historical cause.

The verified upstream link `Google-Health/consumer-health-research` also reproduced a missing repository-owner signal. Only the exact `google-health` owner now recalls Google review; lookalikes such as `not-google-health` remain excluded. This does not establish that SensorWM source code has been released there.

## Leads not counted as new papers

- Google's CKM companion reuses existing LSM-V2 methods. The inspected text did not establish a new independently reusable general algorithm or public benchmark, so it is outside this repository's method-selection scope. This does not dismiss its medical research value.
- Meta's RL-R CHAT November 5 entry is a license-change notice; its page has an earlier date. It is not counted as a new paper, and its complete method was not re-reviewed.
- Unconfirmed leads in Google's 2027 directory are archived as source exceptions when a fixed original manuscript cannot be identified. The directory year is not assumed to be a first-publication year; dates, costs, and implementation work are not invented.

See the [official-lead review](../../../research-audits/nov12-refresh/priority-review.json) for precise source and reading boundaries. This bounded delivery is **not an institution-wide or whole-window census**. The review watermark remains **November 9, 2026**.
