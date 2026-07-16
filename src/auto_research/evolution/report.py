from __future__ import annotations

import json
from pathlib import Path

from .models import EvolutionResult


def write_evolution_artifacts(result: EvolutionResult, run_dir: Path) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "result.json").write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run_dir / "report.md").write_text(render_evolution_report(result), encoding="utf-8")
    (run_dir / "index.html").write_text(render_dashboard(result), encoding="utf-8")


def render_evolution_report(result: EvolutionResult) -> str:
    champion = next((trial for trial in result.trials if trial.trial_id == result.champion_id), None)
    baseline = result.trials[0] if result.trials else None
    lines = [
        f"# 模型自动进化报告：{result.config.model}", "",
        "## 结论", "",
        f"- 数据集：`{result.config.dataset}`",
        f"- 调研方向：{result.config.direction or '未指定'}",
        f"- 数据规模：{result.dataset_summary.get('users', '—')} users / {result.dataset_summary.get('items', '—')} items / {result.dataset_summary.get('train_events', '—')} train events；固定评估 cohort {result.dataset_summary.get('evaluation_users', '—')} users",
        f"- 并行度：`{result.config.workers}` workers",
        f"- 代数 / 每代子代：`{result.config.generations}` / `{result.config.population}`",
        f"- 论文证据：{len(result.papers)} 篇，其中 {sum(p.architecture is not None for p in result.papers)} 篇映射到已验证结构算子",
    ]
    if champion and baseline:
        gain = 100 * (champion.fitness - baseline.fitness) / max(abs(baseline.fitness), 1e-12)
        lines += [f"- validation 冠军：`{champion.trial_id}` / `{champion.genome.architecture}` / NDCG@10 `{champion.fitness:.5f}`（相对初始 RankMixer `{gain:+.2f}%`）"]
    if result.baseline_test and result.champion_test:
        gain = 100 * (result.champion_test["ndcg_at_10"] - result.baseline_test["ndcg_at_10"]) / max(result.baseline_test["ndcg_at_10"], 1e-12)
        lines += [f"- 最终一次 test：NDCG@10 `{result.baseline_test['ndcg_at_10']:.5f}→{result.champion_test['ndcg_at_10']:.5f}`（`{gain:+.2f}%`）"]
    lines += ["", "## 论文与结构映射", "", "| 论文 | 日期 | 结构算子 | 方法摘要 |", "|---|---|---|---|"]
    for paper in result.papers:
        lines.append(f"| [{paper.title}]({paper.url}) | {paper.published} | `{paper.architecture or 'evidence-only'}` | {paper.method} |")
    lines += ["", "## 每轮研究记录", ""]
    for round_ in result.rounds:
        lines += [f"### 第 {round_['generation']} 轮", "", f"- 起点：`{round_['parent']}`", "- 假设："]
        lines += [f"  - `{item['trial_id']}`：{item['rationale']}" for item in round_["hypotheses"]]
        lines += [f"- 观察：" + "；".join(f"`{item['trial_id']}` NDCG@10={item['ndcg_at_10']:.5f} ({item['status']})" for item in round_["observations"]), f"- 决策：{round_['decision']}", ""]
    lines += ["## 完整实验轨迹", "", "| Trial | 状态 | 代 | 父代 | Architecture | Validation NDCG@10 | Hit@10 | 耗时(s) | Params | Genome |", "|---|---|---:|---|---|---:|---:|---:|---:|---|"]
    for trial in result.trials:
        genome = json.dumps(trial.genome.to_dict(), ensure_ascii=False, sort_keys=True).replace("|", "\\|")
        lines.append(f"| {trial.trial_id} | {trial.status} | {trial.generation} | {trial.parent_id or '—'} | `{trial.genome.architecture}` | {trial.validation['ndcg_at_10']:.5f} | {trial.validation['hit_at_10']:.5f} | {trial.duration_seconds:.1f} | {trial.training.get('parameters', 0)} | `{genome}` |")
    lines += ["", "## 协议与边界", "", "- 默认使用完整公开数据集；只有显式传入 `--maximum-users/--maximum-items` 才缩小为 smoke test。", "- 每轮选择只读取 validation；test 仅在全部代际结束后对初始基线和冠军各运行一次。", "- 同一代实验可并行；失败实验保留错误信息且不参与晋级。", "- 论文只负责提出结构假设；只有已审核、已测试的算子可执行。", "- checkpoint 与原始 runs 不提交 Git；`result.json`、`report.md` 和 `index.html` 保存完整过程。", ""]
    return "\n".join(lines)


def render_dashboard(result: EvolutionResult) -> str:
    data = result.to_dict()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = f"{result.config.model} 自动研究"
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>body{{margin:0;background:#f5f7fb;color:#172033;font:15px system-ui,-apple-system,sans-serif}}main{{max-width:1180px;margin:auto;padding:32px}}h1{{margin:0}}.muted{{color:#65708a}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:24px 0}}.card,section{{background:white;border:1px solid #e4e8f0;border-radius:14px;padding:18px;box-shadow:0 3px 12px #1b274510}}.value{{font-size:26px;font-weight:700;margin-top:7px}}section{{margin:16px 0}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border-bottom:1px solid #edf0f5;text-align:left}}.good{{color:#087f5b}}.bad{{color:#c92a2a}}.bar{{height:9px;background:#4263eb;border-radius:6px;min-width:2px}}code{{background:#f1f3f8;padding:2px 5px;border-radius:4px}}details{{margin:10px 0}}@media(max-width:700px){{main{{padding:18px}}.scroll{{overflow:auto}}}}</style></head><body><main><h1>{title}</h1><p class="muted" id="subtitle"></p><div class="cards" id="cards"></div><section><h2>迭代效果</h2><div class="scroll"><table><thead><tr><th>实验</th><th>轮次</th><th>结构</th><th>NDCG@10</th><th>相对宽度</th><th>状态</th></tr></thead><tbody id="trials"></tbody></table></div></section><section><h2>研究过程</h2><div id="rounds"></div></section><section><h2>论文证据</h2><div id="papers"></div></section></main>
<script>const d={payload};const esc=s=>String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));const trials=d.trials,base=trials[0],champ=trials.find(x=>x.trial_id===d.champion_id)||base;document.querySelector('#subtitle').textContent=d.config.direction+' · '+d.config.dataset+' · '+d.dataset_summary.users+' users / '+d.dataset_summary.items+' items';const gain=(champ.fitness-base.fitness)/Math.max(Math.abs(base.fitness),1e-12)*100;document.querySelector('#cards').innerHTML=[['当前冠军',champ.trial_id],['冠军结构',champ.genome.architecture],['Validation NDCG@10',champ.fitness.toFixed(5)],['相对基线',(gain>=0?'+':'')+gain.toFixed(2)+'%'],['实验数',trials.length],['并行 workers',d.config.workers]].map(x=>`<div class="card"><div class="muted">${{esc(x[0])}}</div><div class="value">${{esc(x[1])}}</div></div>`).join('');const max=Math.max(...trials.filter(x=>x.status==='completed').map(x=>x.fitness),.00001);document.querySelector('#trials').innerHTML=trials.map(x=>`<tr><td><code>${{esc(x.trial_id)}}</code></td><td>${{x.generation}}</td><td>${{esc(x.genome.architecture)}}</td><td>${{x.fitness.toFixed(5)}}</td><td><div class="bar" style="width:${{Math.max(0,x.fitness/max*100)}}%"></div></td><td class="${{x.status==='completed'?'good':'bad'}}">${{esc(x.status)}}</td></tr>`).join('');document.querySelector('#rounds').innerHTML=d.rounds.map(r=>`<details open><summary><b>第 ${{r.generation}} 轮</b> · ${{esc(r.decision)}}</summary><p><b>假设</b></p><ul>${{r.hypotheses.map(h=>`<li><code>${{esc(h.trial_id)}}</code> ${{esc(h.rationale)}}</li>`).join('')}}</ul><p><b>观察</b></p><ul>${{r.observations.map(o=>`<li>${{esc(o.trial_id)}}: NDCG@10=${{o.ndcg_at_10.toFixed(5)}} (${{esc(o.status)}})</li>`).join('')}}</ul></details>`).join('')||'<p class="muted">尚未完成第一轮。</p>';document.querySelector('#papers').innerHTML='<ul>'+d.papers.map(p=>`<li><a href="${{esc(p.url)}}">${{esc(p.title)}}</a>：${{esc(p.method)}} <code>${{esc(p.architecture||'evidence-only')}}</code></li>`).join('')+'</ul>';</script></body></html>'''
