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
    if result.config.model == "micro-llm":
        return _render_llm_report(result)
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
        lines += [f"- 观察：" + "；".join(f"`{item['trial_id']}` NDCG@10={item['validation']['ndcg_at_10']:.5f} ({item['status']})" for item in round_["observations"]), f"- 决策：{round_['decision']}", ""]
    lines += ["## 完整实验轨迹", "", "| Trial | 状态 | 代 | 父代 | Architecture | Validation NDCG@10 | Hit@10 | 耗时(s) | Params | Genome |", "|---|---|---:|---|---|---:|---:|---:|---:|---|"]
    for trial in result.trials:
        genome = json.dumps(trial.genome.to_dict(), ensure_ascii=False, sort_keys=True).replace("|", "\\|")
        lines.append(f"| {trial.trial_id} | {trial.status} | {trial.generation} | {trial.parent_id or '—'} | `{trial.genome.architecture}` | {trial.validation['ndcg_at_10']:.5f} | {trial.validation['hit_at_10']:.5f} | {trial.duration_seconds:.1f} | {trial.training.get('parameters', 0)} | `{genome}` |")
    lines += ["", "## 协议与边界", "", "- 默认使用完整公开数据集；只有显式传入 `--maximum-users/--maximum-items` 才缩小为 smoke test。", "- 每轮选择只读取 validation；test 仅在全部代际结束后对初始基线和冠军各运行一次。", "- 同一代实验可并行；失败实验保留错误信息且不参与晋级。", "- 论文只负责提出结构假设；只有已审核、已测试的算子可执行。", "- checkpoint 与原始 runs 不提交 Git；`result.json`、`report.md` 和 `index.html` 保存完整过程。", ""]
    return "\n".join(lines)


def _render_llm_report(result: EvolutionResult) -> str:
    champion = next((trial for trial in result.trials if trial.trial_id == result.champion_id), None)
    baseline = result.trials[0] if result.trials else None
    summary = result.dataset_summary
    lines = [
        "# LLM 自动进化报告", "", "## 结论", "",
        f"- Benchmark：`{result.config.dataset}`（本地训练 BPE vocab `{summary.get('vocab_size', '—')}`）",
        f"- 调研方向：{result.config.direction}",
        f"- 数据：train `{summary.get('train_tokens', '—')}` tokens；validation `{summary.get('validation_tokens', '—')}`；test `{summary.get('test_tokens', '—')}`；instruction train/validation `{summary.get('instruction_train', '—')}/{summary.get('instruction_validation', '—')}`",
        f"- 代数 / population / workers：`{result.config.generations}` / `{result.config.population}` / `{result.config.workers}`",
        f"- 选择目标：最小化 `WikiText validation loss + 0.15 × instruction validation loss`；test 不参与进化",
    ]
    if champion and baseline:
        reduction = 100 * (baseline.validation["perplexity"] - champion.validation["perplexity"]) / max(baseline.validation["perplexity"], 1e-12)
        lines += [
            f"- validation 冠军：`{champion.trial_id}` / `{champion.genome.architecture}`；PPL `{baseline.validation['perplexity']:.3f}→{champion.validation['perplexity']:.3f}`（降低 `{reduction:+.2f}%`），instruction loss `{champion.validation['instruction_loss']:.4f}`",
        ]
    if result.baseline_test and result.champion_test:
        reduction = 100 * (result.baseline_test["perplexity"] - result.champion_test["perplexity"]) / max(result.baseline_test["perplexity"], 1e-12)
        lines += [f"- 隔离 test PPL：`{result.baseline_test['perplexity']:.3f}→{result.champion_test['perplexity']:.3f}`（降低 `{reduction:+.2f}%`）"]
    lines += ["", "## 论文证据与本地算子", "", "| 论文 | 日期 | 可执行研究维度 | 本地机制 |", "|---|---|---|---|"]
    for paper in result.papers:
        lines.append(f"| [{paper.title}]({paper.url}) | {paper.published} | `{paper.architecture or 'evidence-only'}` | {paper.method} |")
    lines += ["", "## 每轮研究记录", ""]
    for round_ in result.rounds:
        lines += [f"### 第 {round_['generation']} 轮", "", f"- 起点：`{round_['parent']}`", "- 假设："]
        lines += [f"  - `{item['trial_id']}`：{item['rationale']}" for item in round_["hypotheses"]]
        observations = []
        for item in round_["observations"]:
            values = item["validation"]
            observations.append(f"`{item['trial_id']}` PPL={values.get('perplexity', float('inf')):.3f}, instruction loss={values.get('instruction_loss', float('inf')):.4f} ({item['status']})")
        lines += ["- 观察：" + "；".join(observations), f"- 决策：{round_['decision']}", ""]
    lines += [
        "## 完整实验轨迹", "",
        "| Trial | 代 | Architecture | Data recipe | Post-training | Val PPL | Instruction loss | Params | 秒 |",
        "|---|---:|---|---|---|---:|---:|---:|---:|",
    ]
    for trial in result.trials:
        lines.append(
            f"| {trial.trial_id} | {trial.generation} | `{trial.genome.architecture}` | `{trial.genome.data_recipe}` ({trial.genome.data_mix_ratio:.2f}) | `{trial.genome.post_training}` | {trial.validation.get('perplexity', float('inf')):.3f} | {trial.validation.get('instruction_loss', float('inf')):.4f} | {trial.training.get('parameters', 0)} | {trial.duration_seconds:.1f} |"
        )
    lines += [
        "", "## 协议与边界", "",
        "- 这是 Mac 可运行的小型 decoder-only LM 研究平台，不把百万级参数本地结果称为前沿大模型能力。",
        "- WikiText-2 是标准 benchmark 数据，但本地 BPE tokenizer 不同于论文 tokenizer；PPL 只在本次同 tokenizer 实验内部公平比较。",
        "- 第一轮研究结构，第二轮研究训练数据，第三轮研究后训练；同一轮尽量冻结其他变量。",
        "- instruction loss 来自 Stanford Alpaca held-out 子集，不代表完整对话、知识、推理或安全能力。",
        "- checkpoint、tokenizer cache、数据与 raw runs 不提交 Git；JSON/Markdown/HTML 保存全部配置、负结果和失败信息。", "",
    ]
    return "\n".join(lines)


def render_dashboard(result: EvolutionResult) -> str:
    data = result.to_dict()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = f"{result.config.model} 自动研究"
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>body{{margin:0;background:#f5f7fb;color:#172033;font:15px system-ui,-apple-system,sans-serif}}main{{max-width:1180px;margin:auto;padding:32px}}h1{{margin:0}}.muted{{color:#65708a}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:24px 0}}.card,section{{background:white;border:1px solid #e4e8f0;border-radius:14px;padding:18px;box-shadow:0 3px 12px #1b274510}}.value{{font-size:26px;font-weight:700;margin-top:7px}}section{{margin:16px 0}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border-bottom:1px solid #edf0f5;text-align:left}}.good{{color:#087f5b}}.bad{{color:#c92a2a}}.bar{{height:9px;background:#4263eb;border-radius:6px;min-width:2px}}code{{background:#f1f3f8;padding:2px 5px;border-radius:4px}}details{{margin:10px 0}}@media(max-width:700px){{main{{padding:18px}}.scroll{{overflow:auto}}}}</style></head><body><main><h1>{title}</h1><p class="muted" id="subtitle"></p><div class="cards" id="cards"></div><section><h2>迭代效果</h2><div class="scroll"><table><thead><tr><th>实验</th><th>轮次</th><th>结构</th><th id="metric-head">主指标</th><th>相对宽度</th><th>状态</th></tr></thead><tbody id="trials"></tbody></table></div></section><section><h2>研究过程</h2><div id="rounds"></div></section><section><h2>论文证据</h2><div id="papers"></div></section></main>
<script>const d={payload};const esc=s=>String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));const trials=d.trials,base=trials[0],champ=trials.find(x=>x.trial_id===d.champion_id)||base,isLLM=d.config.model==='micro-llm';const metric=x=>isLLM?x.validation.perplexity:x.validation.ndcg_at_10,metricLabel=isLLM?'Validation PPL':'Validation NDCG@10';document.querySelector('#metric-head').textContent=metricLabel;document.querySelector('#subtitle').textContent=isLLM?d.config.direction+' · '+d.config.dataset+' · '+d.dataset_summary.train_tokens+' train tokens':d.config.direction+' · '+d.config.dataset+' · '+d.dataset_summary.users+' users / '+d.dataset_summary.items+' items';const gain=isLLM?(metric(base)-metric(champ))/Math.max(metric(base),1e-12)*100:(metric(champ)-metric(base))/Math.max(Math.abs(metric(base)),1e-12)*100;document.querySelector('#cards').innerHTML=[['当前冠军',champ.trial_id],['冠军结构',champ.genome.architecture],[metricLabel,metric(champ).toFixed(5)],['相对基线',(gain>=0?'+':'')+gain.toFixed(2)+'%'],['已完成进化轮数',d.rounds.length],['实验数（含基线）',trials.length],['并行 workers',d.config.workers]].map(x=>`<div class="card"><div class="muted">${{esc(x[0])}}</div><div class="value">${{esc(x[1])}}</div></div>`).join('');const completed=trials.filter(x=>x.status==='completed'),best=isLLM?Math.min(...completed.map(metric)):Math.max(...completed.map(metric));document.querySelector('#trials').innerHTML=trials.map(x=>`<tr><td><code>${{esc(x.trial_id)}}</code></td><td>${{x.generation}}</td><td>${{esc(x.genome.architecture)}}</td><td>${{metric(x).toFixed(5)}}</td><td><div class="bar" style="width:${{Math.max(0,isLLM?best/metric(x)*100:metric(x)/best*100)}}%"></div></td><td class="${{x.status==='completed'?'good':'bad'}}">${{esc(x.status)}}</td></tr>`).join('');document.querySelector('#rounds').innerHTML=d.rounds.map(r=>`<details open><summary><b>第 ${{r.generation}} 轮</b> · ${{esc(r.decision)}}</summary><p><b>假设</b></p><ul>${{r.hypotheses.map(h=>`<li><code>${{esc(h.trial_id)}}</code> ${{esc(h.rationale)}}</li>`).join('')}}</ul><p><b>观察</b></p><ul>${{r.observations.map(o=>`<li>${{esc(o.trial_id)}}: ${{isLLM?'PPL='+Number(o.validation.perplexity).toFixed(3):'NDCG@10='+Number(o.validation.ndcg_at_10).toFixed(5)}} (${{esc(o.status)}})</li>`).join('')}}</ul></details>`).join('')||'<p class="muted">尚未完成第一轮。</p>';document.querySelector('#papers').innerHTML='<ul>'+d.papers.map(p=>`<li><a href="${{esc(p.url)}}">${{esc(p.title)}}</a>：${{esc(p.method)}} <code>${{esc(p.architecture||'evidence-only')}}</code></li>`).join('')+'</ul>';</script></body></html>'''
