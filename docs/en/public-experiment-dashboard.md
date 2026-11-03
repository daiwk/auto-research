# Public experiment dashboard

<!-- source-sha256: a8a8a2019cc8d31f0159bc8d726a6ce605238cdc3af713879a178b7c3f5cb1d7 -->

[简体中文](../public-experiment-dashboard.md)

This dashboard brings together audited metrics committed to the repository for search, advertising, recommendation, foundation models, structured decisions, multimodal models, LLM post-training, and agents. It reads stable metrics under `docs/` only. Local checkpoints, private data, and unaudited temporary runs are not included.

!!! info "Agent results by evaluation tier"
    **L1 mechanism diagnostics** verify that mechanisms described in a paper can execute, including planning, memory, tool use, and RL credit assignment. Success metrics can saturate on a deterministic mini-suite, so they do not measure model capability and are not used to rank methods. Only L2/L3 results explicitly marked as formal comparisons can be used to compare performance.

<div class="ar-dashboard" data-lang="en" data-dashboard-url="../../assets/data/experiment-dashboard.json">
  <div class="ar-dashboard__summary" aria-live="polite">
    <article><strong data-stat="results">—</strong><span>Matching results</span></article>
    <article><strong data-stat="methods">—</strong><span>Methods</span></article>
    <article><strong data-stat="datasets">—</strong><span>Datasets</span></article>
    <article><strong data-stat="domains">—</strong><span>Research domains</span></article>
  </div>
  <div class="ar-dashboard__controls">
    <label>Domain<select data-filter="domain"><option value="">All domains</option></select></label>
    <label class="ar-dashboard__search">Search<input data-filter="query" type="search" placeholder="Method, dataset, or metric"></label>
    <label>Sort<select data-filter="sort"><option value="domain">Domain and method</option><option value="method">Method name</option></select></label>
  </div>
  <div class="ar-dashboard__status">Loading public metrics…</div>
  <section class="ar-dashboard__grid"></section>
  <button class="ar-dashboard__more" type="button" hidden>Load more</button>
</div>

## How the data is presented

- `scripts/generate_public_experiment_dashboard.py` deterministically generates the dashboard data from committed metrics.
- Formal evaluation cards prioritize key metrics such as NDCG, recall, accuracy, AUC, success rate, loss, and latency.
- Agent L1 cards show the evaluation tier, benchmark, episode count, simulated cost, and mechanism counts. Saturated success scores remain in the expandable raw record only.
- Other fields are available under “View all metrics,” rather than crowding the page with raw JSON.
- Select “View metric artifact” to open the corresponding original JSON on GitHub and trace the result back to its evidence.
