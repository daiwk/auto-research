from __future__ import annotations

import json
from pathlib import Path

from .store import ExperimentStore


def dashboard_payload(database: Path) -> list[dict]:
    with ExperimentStore(database) as store:
        rows = store.rows()
    return [
        {
            "path": row.path, "domain": row.domain, "method": row.method,
            "dataset": row.dataset, "seed": row.seed, "created_at": row.created_at,
            "metrics": row.metrics,
        }
        for row in rows
    ]


def write_dashboard(database: Path, output: Path) -> Path:
    payload = dashboard_payload(database)
    template = """<!doctype html>
<html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Auto Research 实验看板</title><style>
:root{--ink:#172033;--muted:#647086;--line:#e2e6ef;--primary:#4557c8;--bg:#f5f7fb}
*{box-sizing:border-box}body{font:15px/1.55 system-ui,-apple-system,sans-serif;margin:0;background:var(--bg);color:var(--ink)}
main{max-width:1440px;margin:auto;padding:36px 28px 60px}.eyebrow{color:var(--primary);font-weight:750;letter-spacing:.08em;text-transform:uppercase}
h1{font-size:clamp(30px,4vw,48px);margin:4px 0 8px}.muted{color:var(--muted)}
.summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:26px 0}.summary article,.experiment{background:white;border:1px solid var(--line);border-radius:16px;box-shadow:0 8px 24px rgba(31,43,85,.05)}
.summary article{padding:17px}.summary strong{display:block;font-size:26px}.controls{position:sticky;top:0;z-index:2;display:flex;gap:12px;flex-wrap:wrap;padding:14px 0;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px)}
select,input{min-height:44px;padding:9px 13px;border:1px solid #cdd4e1;border-radius:10px;background:white;font:inherit}input{flex:1;min-width:240px}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.experiment{padding:18px;min-width:0}.head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.title{font-size:18px;font-weight:750;overflow-wrap:anywhere}.badges{display:flex;gap:7px;flex-wrap:wrap;margin:9px 0 14px}.badge{padding:3px 9px;border-radius:999px;background:#eef0ff;color:#3547af;font-size:12px}
.metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.metric{padding:10px;border-radius:10px;background:#f7f8fc;min-width:0}.metric b{display:block;font-size:16px}.metric span{display:block;color:var(--muted);font-size:11px;overflow-wrap:anywhere}
details{margin-top:12px}summary{cursor:pointer;color:var(--primary);font-weight:650}.all{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:5px 12px;margin-top:10px}.all div{display:flex;justify-content:space-between;gap:8px;border-bottom:1px dashed var(--line);overflow-wrap:anywhere}.path{margin-top:12px;color:var(--muted);font:12px/1.4 ui-monospace,monospace;overflow-wrap:anywhere}
.empty{text-align:center;padding:50px;color:var(--muted)}button{display:block;margin:22px auto 0;padding:10px 18px;border:0;border-radius:10px;background:var(--primary);color:white;font-weight:700;cursor:pointer}
@media(max-width:900px){.grid{grid-template-columns:1fr}.summary{grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){main{padding:24px 14px}.metrics,.all{grid-template-columns:1fr}.summary{grid-template-columns:1fr 1fr}}
</style></head><body><main><div class="eyebrow">Auto Research · Evidence</div><h1>统一实验看板</h1><div class="muted">跨论文复现、Evolve、后训练、Agent 与多模态实验。指标以卡片呈现，完整字段按需展开。</div>
<section class="summary"><article><strong id="count">0</strong><span>当前结果</span></article><article><strong id="methods">0</strong><span>方法</span></article><article><strong id="datasets">0</strong><span>数据集</span></article><article><strong id="domains">0</strong><span>研究领域</span></article></section>
<div class="controls"><select id="domain"><option value="">全部领域</option></select><input id="query" placeholder="搜索方法、数据集或指标"><select id="sort"><option value="recent">最近记录</option><option value="method">方法名称</option></select></div><section class="grid" id="rows"></section><button id="more" hidden>加载更多</button>
<script>const data=__DATA__;const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const priority=/ndcg|hit_at|accuracy|auc|recall|exact_match|success|reward|perplexity|loss|latency|throughput|memory/i;let visible=24;
const pretty=k=>k.split('.').pop().replaceAll('_',' ');const number=v=>Number.isInteger(v)?String(v):Number(v).toPrecision(5).replace(/0+$/,'').replace(/\\.$/,'');
function selected(r){const d=domain.value,q=query.value.toLowerCase();return(!d||r.domain===d)&&(!q||JSON.stringify(r).toLowerCase().includes(q))}
function metricEntries(r){return Object.entries(r.metrics).sort((a,b)=>Number(priority.test(b[0]))-Number(priority.test(a[0]))||a[0].localeCompare(b[0]))}
function card(r){const metrics=metricEntries(r),top=metrics.slice(0,6);return `<article class="experiment"><div class="head"><div class="title">${esc(r.method)}</div><span class="muted">${esc(r.seed||'—')}</span></div><div class="badges"><span class="badge">${esc(r.domain)}</span>${r.dataset?`<span class="badge">${esc(r.dataset)}</span>`:''}</div><div class="metrics">${top.map(([k,v])=>`<div class="metric"><b>${number(v)}</b><span>${esc(pretty(k))}</span></div>`).join('')}</div>${metrics.length>6?`<details><summary>查看全部 ${metrics.length} 项指标</summary><div class="all">${metrics.map(([k,v])=>`<div><span>${esc(k)}</span><b>${number(v)}</b></div>`).join('')}</div></details>`:''}<div class="path">${esc(r.path)}</div></article>`}
function render(){let rows=data.filter(selected);if(sort.value==='method')rows.sort((a,b)=>a.method.localeCompare(b.method));count.textContent=rows.length;methods.textContent=new Set(rows.map(r=>r.method)).size;datasets.textContent=new Set(rows.map(r=>r.dataset).filter(Boolean)).size;domains.textContent=new Set(rows.map(r=>r.domain)).size;document.querySelector('#rows').innerHTML=rows.length?rows.slice(0,visible).map(card).join(''):'<div class="empty">没有匹配的实验</div>';more.hidden=rows.length<=visible}
[...new Set(data.map(r=>r.domain))].sort().forEach(v=>domain.insertAdjacentHTML('beforeend',`<option>${esc(v)}</option>`));domain.onchange=()=>{visible=24;render()};query.oninput=()=>{visible=24;render()};sort.onchange=render;more.onclick=()=>{visible+=24;render()};render();</script></main></body></html>"""
    document = template.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    return output
