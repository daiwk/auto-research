(() => {
  const root = document.querySelector(".ar-dashboard");
  if (!root) return;

  const domain = root.querySelector('[data-filter="domain"]');
  const query = root.querySelector('[data-filter="query"]');
  const sort = root.querySelector('[data-filter="sort"]');
  const grid = root.querySelector(".ar-dashboard__grid");
  const status = root.querySelector(".ar-dashboard__status");
  const more = root.querySelector(".ar-dashboard__more");
  const labels = {
    recommendation: "搜广推与 LLM 应用",
    "foundation-model": "基础模型",
    multimodal: "多模态大模型",
    "post-training": "LLM 后训练",
    agent: "Agent",
    evolution: "自动进化",
    general: "其他",
  };
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

  function card(item) {
    const metrics = metricEntries(item);
    const primary = metrics.slice(0, 6);
    const method = item.method.replace(/^\d{4}\.\d+-/, "").replaceAll("_", " ");
    return `<article class="ar-dashboard-card">
      <header><h3>${escape(item.title || method)}</h3><span class="ar-dashboard-card__seed">seed ${escape(item.seed || "—")}</span></header>
      <div class="ar-dashboard-card__badges"><span>${escape(labels[item.domain] || item.domain)}</span><span>${escape(method)}</span>${item.dataset ? `<span>${escape(item.dataset)}</span>` : ""}</div>
      <div class="ar-dashboard-card__metrics">${primary.map(([key, value]) => `<div><strong>${number(value)}</strong><span>${escape(pretty(key))}</span></div>`).join("")}</div>
      ${metrics.length > 6 ? `<details><summary>查看全部 ${metrics.length} 项指标</summary><div class="ar-dashboard-card__all">${metrics.map(([key, value]) => `<div><span>${escape(key)}</span><strong>${number(value)}</strong></div>`).join("")}</div></details>` : ""}
      <a class="ar-dashboard-card__source" href="${artifactUrl(item.path)}">查看指标产物 →</a>
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
    status.textContent = selected.length ? `展示 ${Math.min(visible, selected.length)} / ${selected.length} 条结果` : "没有匹配的实验";
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
      status.textContent = `公开指标读取失败：${error.message}`;
    });
  domain.addEventListener("change", () => { visible = 24; render(); });
  query.addEventListener("input", () => { visible = 24; render(); });
  sort.addEventListener("change", render);
  more.addEventListener("click", () => { visible += 24; render(); });
})();
