(() => {
  const root = document.querySelector(".ar-dashboard");
  if (!root) return;

  const domain = root.querySelector('[data-filter="domain"]');
  const query = root.querySelector('[data-filter="query"]');
  const sort = root.querySelector('[data-filter="sort"]');
  const grid = root.querySelector(".ar-dashboard__grid");
  const status = root.querySelector(".ar-dashboard__status");
  const more = root.querySelector(".ar-dashboard__more");
  const messages = {
    zh: {
      domains: {
        recommendation: "搜广推与 LLM 应用",
        "foundation-model": "基础模型",
        "system-one": "结构化决策 / System One",
        multimodal: "多模态大模型",
        "post-training": "LLM 后训练",
        agent: "Agent",
        evolution: "自动进化",
        general: "其他",
      },
      seed: (value) => `seed ${value || "—"}`,
      episodes: (count) => `${count} episodes`,
      diagnostic: "L1 机制诊断",
      diagnosticNote: "非正式能力比较，不参与模型效果排名",
      isolatedCapability: "L2.1 隔离能力评测",
      capability: "L2 能力评测",
      isolation: "无 guide/oracle · held-out test",
      formal: "三 seed 正式比较",
      nonFormal: "未满足正式比较协议",
      nonFormalQuestion: "为什么未标为正式比较？",
      nonFormalNote: "原始测量保留；正式比较需核验独立 seeds、数据和切分版本、基线、代码版本及 test 隔离。",
      saturated: "确定性 mini-suite 已饱和；三个 success=1 只表示机制合约通过，并非模型准确率 100%。",
      rawMetrics: "查看原始 smoke 指标与机制计数",
      allMetrics: (count) => `查看全部 ${count} 项指标`,
      artifact: "查看指标产物 →",
      shown: (count, total) => `展示 ${count} / ${total} 条结果`,
      empty: "没有匹配的实验",
      error: (detail) => `公开指标读取失败：${detail}`,
    },
    en: {
      domains: {
        recommendation: "Search, advertising, recommendation, and LLM applications",
        "foundation-model": "Foundation models",
        "system-one": "Structured decisions / System One",
        multimodal: "Multimodal models",
        "post-training": "LLM post-training",
        agent: "Agents",
        evolution: "Automatic evolution",
        general: "Other",
      },
      seed: englishSeed,
      episodes: (count) => `${count} ${Number(count) === 1 ? "episode" : "episodes"}`,
      diagnostic: "L1 mechanism diagnostic",
      diagnosticNote: "Not a formal capability comparison; excluded from model rankings",
      isolatedCapability: "L2.1 isolated capability evaluation",
      capability: "L2 capability evaluation",
      isolation: "No guide or oracle · held-out test",
      formal: "Formal comparison with three seeds",
      nonFormal: "Formal comparison protocol not satisfied",
      nonFormalQuestion: "Why is this not marked as a formal comparison?",
      nonFormalNote: "Original measurements are retained. Formal comparisons require verified independent seeds, dataset and split versions, baselines, code versions, and test isolation.",
      reasons: {
        capability_tier_not_established: "Capability tier not established",
        comparison_contract_missing: "Comparison contract missing",
        concept_demo: "Concept demo only",
        diagnostic_dataset: "Diagnostic dataset",
        diagnostic_or_ineligible: "Diagnostic or otherwise ineligible",
        gold_derived_evaluation: "Evaluation derived from gold labels",
        insufficient_independent_seeds: "Too few independent seeds",
        mechanism_or_contract_only: "Mechanism or contract check only",
        seed_results_not_aligned: "Seed results are not aligned",
        test_isolation_not_established: "Test isolation not established",
      },
      saturated: "The deterministic mini-suite is saturated. Three success scores of 1 establish only that the mechanism contract passed, not 100% model accuracy.",
      rawMetrics: "View raw smoke-test metrics and mechanism counts",
      allMetrics: (count) => `View all ${count} metrics`,
      artifact: "View metric artifact →",
      shown: (count, total) => `Showing ${count} of ${total} results`,
      empty: "No matching experiments",
      error: (detail) => `Could not load public metrics: ${detail}`,
    },
  }[root.dataset.lang === "en" ? "en" : "zh"];
  const labels = messages.domains;
  const priority = /ndcg|hit_at|accuracy|auc|recall|exact_match|success|reward|perplexity|loss|latency|throughput|memory/i;
  let experiments = [];
  let visible = 24;

  const escape = (value) => String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[character]);
  const pretty = (key) => key.split(".").pop().replaceAll("_", " ");
  const number = (value) => Number.isInteger(value)
    ? String(value)
    : Number(value).toPrecision(5).replace(/0+$/, "").replace(/\.$/, "");
  const metricEntries = (item) => Object.entries(item.metrics).sort((left, right) => (
    Number(priority.test(right[0])) - Number(priority.test(left[0]))
    || left[0].localeCompare(right[0])
  ));
  const artifactUrl = (path) => `https://github.com/daiwk/auto-research/blob/main/${encodeURI(path)}`;
  const metricTile = ([key, value]) => `<div><strong>${number(value)}</strong><span>${escape(pretty(key))}</span></div>`;

  function englishSeed(value) {
    if (value === "不适用（确定性审计）") return "Seed: not applicable (deterministic audit)";
    // Some archived rows serialize complete run records into the seed field.
    // Show only the explicitly recorded seeds; do not infer formal eligibility.
    if (typeof value === "string" && value.startsWith("[{'paper': ")) {
      const seeds = [...value.matchAll(/(?:\[\{|, \{)'paper': '[^']+', 'seed': (\d+),/g)]
        .map((match) => match[1]);
      if (seeds.length) return `Seeds ${[...new Set(seeds)].join(", ")} (archived runs)`;
    }
    return `Seed ${value || "—"}`;
  }

  function card(item) {
    const metrics = metricEntries(item);
    const evidence = item.evidence || {};
    const diagnostic = evidence.diagnostic_only;
    const agentDiagnostic = diagnostic && item.domain === "agent";
    const capability = item.domain === "agent" && evidence.tier === "l2_capability";
    const mechanism = Object.entries(evidence.mechanism_metrics || {})
      .sort((left, right) => right[1] - left[1] || left[0].localeCompare(right[0]));
    const primary = agentDiagnostic
      ? [...metrics.filter(([key]) => key === "average_cost"), ...mechanism].slice(0, 6)
      : metrics.slice(0, 6);
    const method = item.method.replace(/^\d{4}\.\d+-/, "").replaceAll("_", " ");
    return `<article class="ar-dashboard-card">
      <header><h3>${escape(item.title || method)}</h3><span class="ar-dashboard-card__seed">${escape(messages.seed(item.seed))}</span></header>
      <div class="ar-dashboard-card__badges"><span>${escape(labels[item.domain] || item.domain)}</span><span>${escape(method)}</span>${item.dataset ? `<span>${escape(item.dataset)}</span>` : ""}${evidence.episodes ? `<span>${escape(messages.episodes(evidence.episodes))}</span>` : ""}</div>
      ${diagnostic ? `<div class="ar-dashboard-card__evidence"><strong>${messages.diagnostic}</strong><span>${messages.diagnosticNote}</span></div>` : ""}
      ${capability ? `<div class="ar-dashboard-card__evidence ar-dashboard-card__evidence--capability"><strong>${String(item.dataset || "").includes("l2.1") ? messages.isolatedCapability : messages.capability}</strong><span>${messages.isolation} · ${evidence.formal_comparison ? messages.formal : messages.nonFormal}</span></div>` : ""}
      ${!diagnostic && evidence.eligibility_reasons?.length ? `<details><summary>${messages.nonFormalQuestion}</summary><p>${messages.nonFormalNote}</p><p>${escape(evidence.eligibility_reasons.map((reason) => messages.reasons?.[reason] || reason).join(" · "))}</p></details>` : ""}
      ${primary.length ? `<div class="ar-dashboard-card__metrics">${primary.map(metricTile).join("")}</div>` : ""}
      ${evidence.capability_metrics_saturated ? `<p class="ar-dashboard-card__notice">${messages.saturated}</p>` : ""}
      ${diagnostic ? `<details><summary>${messages.rawMetrics}</summary><div class="ar-dashboard-card__all">${[...metrics, ...mechanism].map(([key, value]) => `<div><span>${escape(key)}</span><strong>${number(value)}</strong></div>`).join("")}</div></details>` : (metrics.length > 6 ? `<details><summary>${messages.allMetrics(metrics.length)}</summary><div class="ar-dashboard-card__all">${metrics.map(([key, value]) => `<div><span>${escape(key)}</span><strong>${number(value)}</strong></div>`).join("")}</div></details>` : "")}
      <a class="ar-dashboard-card__source" href="${artifactUrl(item.path)}">${messages.artifact}</a>
    </article>`;
  }

  function render() {
    const text = query.value.trim().toLowerCase();
    const selected = experiments.filter((item) => (
      (!domain.value || item.domain === domain.value)
      && (!text || JSON.stringify(item).toLowerCase().includes(text))
    ));
    selected.sort(sort.value === "method"
      ? (a, b) => a.method.localeCompare(b.method)
      : (a, b) => a.domain.localeCompare(b.domain) || a.method.localeCompare(b.method));
    root.querySelector('[data-stat="results"]').textContent = selected.length;
    root.querySelector('[data-stat="methods"]').textContent = new Set(selected.map((item) => item.method)).size;
    root.querySelector('[data-stat="datasets"]').textContent = new Set(selected.map((item) => item.dataset).filter(Boolean)).size;
    root.querySelector('[data-stat="domains"]').textContent = new Set(selected.map((item) => item.domain)).size;
    status.textContent = selected.length ? messages.shown(Math.min(visible, selected.length), selected.length) : messages.empty;
    grid.innerHTML = selected.slice(0, visible).map(card).join("");
    more.hidden = selected.length <= visible;
  }

  fetch(new URL(root.dataset.dashboardUrl, window.location.href))
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((payload) => {
      experiments = payload.experiments;
      [...new Set(experiments.map((item) => item.domain))].sort().forEach((value) => {
        domain.insertAdjacentHTML("beforeend", `<option value="${escape(value)}">${escape(labels[value] || value)}</option>`);
      });
      render();
    })
    .catch((error) => {
      status.textContent = messages.error(error.message);
    });
  domain.addEventListener("change", () => { visible = 24; render(); });
  query.addEventListener("input", () => { visible = 24; render(); });
  sort.addEventListener("change", render);
  more.addEventListener("click", () => { visible += 24; render(); });
})();
