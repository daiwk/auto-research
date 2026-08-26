# 公开实验看板

这里汇总仓库中已经审计并提交的论文复现、基础模型、多模态、LLM 后训练与 Agent 指标。公开页面只读取 `docs/` 下的稳定指标，不包含本地 checkpoint、私有数据或尚未审计的临时运行。

<div class="ar-dashboard" data-dashboard-url="../assets/data/experiment-dashboard.json">
  <div class="ar-dashboard__summary" aria-live="polite">
    <article><strong data-stat="results">—</strong><span>当前结果</span></article>
    <article><strong data-stat="methods">—</strong><span>方法</span></article>
    <article><strong data-stat="datasets">—</strong><span>数据集</span></article>
    <article><strong data-stat="domains">—</strong><span>研究领域</span></article>
  </div>
  <div class="ar-dashboard__controls">
    <label>领域<select data-filter="domain"><option value="">全部领域</option></select></label>
    <label class="ar-dashboard__search">搜索<input data-filter="query" type="search" placeholder="方法、数据集或指标"></label>
    <label>排序<select data-filter="sort"><option value="domain">领域与方法</option><option value="method">方法名称</option></select></label>
  </div>
  <div class="ar-dashboard__status">正在读取公开指标……</div>
  <section class="ar-dashboard__grid"></section>
  <button class="ar-dashboard__more" type="button" hidden>加载更多</button>
</div>

## 数据口径

- 页面数据由 `scripts/generate_public_experiment_dashboard.py` 从已提交指标确定性生成；
- 每张卡片优先展示 NDCG、Recall、Accuracy、AUC、成功率、Loss、延迟等核心指标；
- 其余字段折叠在“查看全部指标”中，避免用一整段 JSON 挤压页面；
- 点击“查看指标产物”可回到 GitHub 中对应的原始 JSON，结论仍可追溯。
