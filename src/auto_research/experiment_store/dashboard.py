from __future__ import annotations

import html
import json
from pathlib import Path

from .store import ExperimentStore


def write_dashboard(database: Path, output: Path) -> Path:
    with ExperimentStore(database) as store:
        rows = store.rows()
    domains = sorted({row.domain for row in rows})
    payload = [
        {
            "path": row.path, "domain": row.domain, "method": row.method,
            "dataset": row.dataset, "seed": row.seed, "created_at": row.created_at,
            "metrics": row.metrics,
        }
        for row in rows
    ]
    options = "".join(f'<option value="{html.escape(value)}">{html.escape(value)}</option>' for value in domains)
    document = f"""<!doctype html>
<html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Auto Research 实验看板</title>
<style>
body{{font:15px system-ui;margin:0;background:#f6f7fb;color:#172033}}main{{max-width:1500px;margin:auto;padding:28px}}
h1{{margin:0 0 8px}}.controls{{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}}
select,input{{padding:9px 12px;border:1px solid #ccd3e0;border-radius:8px;background:white}}
.card{{background:white;border:1px solid #e2e5ec;border-radius:12px;padding:16px;overflow:auto}}
table{{border-collapse:collapse;width:100%;table-layout:fixed}}th,td{{padding:10px;border-bottom:1px solid #e8eaf0;text-align:left;vertical-align:top;overflow-wrap:anywhere}}
th:nth-child(1){{width:10%}}th:nth-child(2){{width:14%}}th:nth-child(3){{width:12%}}th:nth-child(4){{width:8%}}th:nth-child(5){{width:40%}}
code{{white-space:normal}}.muted{{color:#647086}}@media(max-width:800px){{th:nth-child(4),td:nth-child(4){{display:none}}}}
</style><main><h1>统一实验看板</h1><div class="muted">跨论文复现、Evolve、后训练、Agent 与多模态实验；数据来自本地 SQLite 索引。</div>
<div class="controls"><select id="domain"><option value="">全部领域</option>{options}</select><input id="query" placeholder="筛选方法、数据集或指标"></div>
<div class="card"><table><thead><tr><th>领域</th><th>方法</th><th>数据集</th><th>Seed</th><th>指标</th><th>产物</th></tr></thead><tbody id="rows"></tbody></table></div>
<script>const data={json.dumps(payload, ensure_ascii=False)};const esc=s=>String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function render(){{const d=document.querySelector('#domain').value,q=document.querySelector('#query').value.toLowerCase();document.querySelector('#rows').innerHTML=data.filter(r=>(!d||r.domain===d)&&(!q||JSON.stringify(r).toLowerCase().includes(q))).map(r=>`<tr><td>${{esc(r.domain)}}</td><td>${{esc(r.method)}}</td><td>${{esc(r.dataset)}}</td><td>${{esc(r.seed)}}</td><td><code>${{esc(JSON.stringify(r.metrics))}}</code></td><td><code>${{esc(r.path)}}</code></td></tr>`).join('')}}
document.querySelector('#domain').onchange=render;document.querySelector('#query').oninput=render;render();</script></main></html>"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    return output
