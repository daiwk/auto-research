from __future__ import annotations

import json
from pathlib import Path

from .models import EvolutionResult


def _recommendation_suite_score(metrics: dict[str, float]) -> float:
    return metrics.get(
        "unirank_composite",
        metrics.get("public_composite", metrics.get("ndcg_at_10", 0.0)),
    )


def _trial_source_label(trial) -> str:
    if trial.generation == 0:
        return "初始基线"
    if trial.source_papers:
        return "论文算子：" + ", ".join(trial.source_papers)
    return "已实现白名单组合 / 调参"


def write_evolution_artifacts(result: EvolutionResult, run_dir: Path) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    result_path = run_dir / "result.json"
    temporary = run_dir / "result.json.tmp"
    temporary.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(result_path)
    (run_dir / "report.md").write_text(render_evolution_report(result), encoding="utf-8")
    (run_dir / "index.html").write_text(render_dashboard(result), encoding="utf-8")


def render_evolution_report(result: EvolutionResult) -> str:
    if result.config.model == "micro-llm":
        return _render_llm_report(result)
    if result.config.model == "micro-vlm":
        return _render_multimodal_report(result)
    if result.config.model == "vlm-checkpoint":
        return _render_checkpoint_multimodal_report(result)
    if result.config.model == "reasoning-checkpoint":
        return _render_reasoning_report(result)
    if result.config.model in {"post-training", "agent"}:
        return _render_composable_report(result)
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
        f"- 评测套件 / 晋级指标：`{result.config.benchmark_suite}` / `{result.config.fitness_metric}`",
        f"- 论文证据：{len(result.papers)} 篇，其中 {sum(p.architecture is not None for p in result.papers)} 篇映射到已验证结构算子",
    ]
    if champion and baseline:
        gain = 100 * (champion.fitness - baseline.fitness) / max(abs(baseline.fitness), 1e-12)
        lines += [
            f"- validation 冠军：`{champion.trial_id}` / `{champion.genome.architecture}`；"
            f"晋级分数 `{champion.fitness:.5f}`（相对初始模型 `{gain:+.2f}%`），"
            f"总体 NDCG@10 `{champion.validation.get('ndcg_at_10', 0.0):.5f}`，"
            f"suite composite `{_recommendation_suite_score(champion.validation):.5f}`"
        ]
    if result.baseline_test and result.champion_test:
        gain = 100 * (result.champion_test["ndcg_at_10"] - result.baseline_test["ndcg_at_10"]) / max(result.baseline_test["ndcg_at_10"], 1e-12)
        lines += [f"- 最终一次 test：NDCG@10 `{result.baseline_test['ndcg_at_10']:.5f}→{result.champion_test['ndcg_at_10']:.5f}`（`{gain:+.2f}%`）"]
    lines += [
        "",
        "## 候选来源说明",
        "",
        "- `installed-paper`：论文机制已在本仓库实现、测试，并映射到可执行结构。",
        "- `retrieved-paper`：实时检索得到、尚未晋级为可执行插件。",
        "- `generated-combination`：控制器组合已有算子或修改超参数。",
        "- `novel-proposal`：仅表示待验证的新假设，不会未经审核执行任意代码。",
        "- `evidence-only`：本轮检索到但尚无本地可执行映射，只留作研究证据。",
        "- `已实现白名单组合 / 调参`：控制器组合兼容算子或修改参数，不会现场生成任意代码。",
        "",
        "## 论文与结构映射", "", "| 论文 | 日期 | 结构算子 | 方法摘要 |", "|---|---|---|---|"
    ]
    for paper in result.papers:
        lines.append(f"| [{paper.title}]({paper.url}) | {paper.published} | `{paper.architecture or paper.candidate_origin}` | {paper.method} |")
    lines += ["", "## 每轮研究记录", ""]
    for round_ in result.rounds:
        lines += [f"### 第 {round_['generation']} 轮", "", f"- 起点：`{round_['parent']}`", "- 假设："]
        lines += [f"  - `{item['trial_id']}`：{item['rationale']}" for item in round_["hypotheses"]]
        lines += [f"- 观察：" + "；".join(
            f"`{item['trial_id']}` fitness={item['validation'].get('fitness', 0.0):.5f}, "
            f"NDCG@10={item['validation'].get('ndcg_at_10', 0.0):.5f}, "
            f"suite={_recommendation_suite_score(item['validation']):.5f} ({item['status']})"
            for item in round_["observations"]
        ), f"- 决策：{round_['decision']}", ""]
    lines += [
        "## 验证级联与研究记忆", "",
        f"- NOVA 验证记录：`{len(result.verification_records)}`；通过：`{sum(item['passed'] for item in result.verification_records)}`。",
        f"- EvoRec 成功技能：`{len(result.research_memory.get('successful_skills', []))}`；禁止方向：`{len(result.research_memory.get('forbidden_directions', []))}`。",
        "- 每代的 architecture gradient、验证失败与成功方法都保存在 `result.json`，并用于重排下一代候选结构。", "",
    ]
    lines += ["## 完整实验轨迹", "", "| Trial | 来源 | 状态 | 代 | 父代 | Architecture | Fitness | Validation NDCG@10 | Suite composite | Hit@10 | 耗时(s) | Params | Genome |", "|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for trial in result.trials:
        genome = json.dumps(trial.genome.to_dict(), ensure_ascii=False, sort_keys=True).replace("|", "\\|")
        lines.append(f"| {trial.trial_id} | {_trial_source_label(trial)} | {trial.status} | {trial.generation} | {trial.parent_id or '—'} | `{trial.genome.architecture}` | {trial.fitness:.5f} | {trial.validation.get('ndcg_at_10', 0.0):.5f} | {_recommendation_suite_score(trial.validation):.5f} | {trial.validation.get('hit_at_10', 0.0):.5f} | {trial.duration_seconds:.1f} | {trial.training.get('parameters', 0)} | `{genome}` |")
    lines += ["", "## 协议与边界", "", "- 默认使用完整公开数据集；只有显式传入 `--maximum-users/--maximum-items` 才缩小为 smoke test。", "- 每轮选择只读取 validation；test 仅在全部代际结束后对初始基线和冠军各运行一次。", "- 同一代实验可并行；失败实验保留错误信息且不参与晋级。", "- 论文只负责提出结构假设；只有已审核、已测试的算子可执行。", "- checkpoint 与原始 runs 不提交 Git；`result.json`、`report.md` 和 `index.html` 保存完整过程。", ""]
    return "\n".join(lines)


def _render_reasoning_report(result: EvolutionResult) -> str:
    champion = next(trial for trial in result.trials if trial.trial_id == result.champion_id)
    baseline = result.trials[0]
    lines = [
        "# 真实 checkpoint 推理预算自动进化报告", "", "## 结论", "",
        f"- Benchmark：`{result.config.dataset}`；固定模型："
        f"`{result.config.reasoning_model_id}` @ `{result.config.reasoning_model_revision}`。",
        "- self-consistency 只读取生成答案；gold answer 仅在选择完成后计算 accuracy。",
        f"- 冠军：`{champion.trial_id}`；samples=`{champion.genome.reasoning_samples}`，"
        f"max tokens=`{champion.genome.reasoning_max_new_tokens}`，"
        f"早停阈值=`{champion.genome.reasoning_stop_consensus}`。",
        f"- Validation accuracy `{baseline.validation['accuracy']:.4f}→"
        f"{champion.validation['accuracy']:.4f}`；tokens/example "
        f"`{baseline.validation['tokens_per_example']:.1f}→"
        f"{champion.validation['tokens_per_example']:.1f}`；latency/example "
        f"`{baseline.validation['latency_seconds_per_example']:.4f}s→"
        f"{champion.validation['latency_seconds_per_example']:.4f}s`。",
    ]
    if result.baseline_test and result.champion_test:
        lines += [
            f"- 隔离 test accuracy `{result.baseline_test['accuracy']:.4f}→"
            f"{result.champion_test['accuracy']:.4f}`；test 未参与预算选择。"
        ]
    lines += [
        "", "## 完整预算曲线", "",
        "| Trial | Samples | Max tokens | Stop consensus | Accuracy | Tokens/example | Latency/example | Calls | Cost | Fitness |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for trial in result.trials:
        values = trial.validation
        lines.append(
            f"| `{trial.trial_id}` | {trial.genome.reasoning_samples} | "
            f"{trial.genome.reasoning_max_new_tokens} | "
            f"{trial.genome.reasoning_stop_consensus:.2f} | "
            f"{values.get('accuracy', 0):.4f} | {values.get('tokens_per_example', 0):.1f} | "
            f"{values.get('latency_seconds_per_example', 0):.4f}s | "
            f"{values.get('model_calls', 0):.0f} | {values.get('estimated_cost', 0):.6f} | "
            f"{trial.fitness:.5f} |"
        )
    lines += [
        "", "## 协议与边界", "",
        "- 所有 trial 锁定同一 checkpoint revision，权重不变。",
        "- 本地 checkpoint 的 estimated cost 为 0；token、调用数和实际延迟仍完整记录。",
        "- 低样本/单 seed 是工程 smoke；正式结论使用公共 GSM8K 和 3 seeds。",
        "- checkpoint、逐条生成和运行缓存不提交 Git。", "",
    ]
    return "\n".join(lines)


def _render_multimodal_report(result: EvolutionResult) -> str:
    champion = next(
        trial for trial in result.trials if trial.trial_id == result.champion_id
    )
    baseline = result.trials[0]
    lines = [
        "# micro-VLM 多模态自动进化报告", "", "## 结论", "",
        f"- Benchmark：`{result.config.dataset}`；评测层级 "
        f"`{result.dataset_summary.get('evaluation_tier', 'unknown')}`。",
        f"- 数据来源：{result.dataset_summary.get('source', 'unknown')}；"
        f"许可说明：{result.dataset_summary.get('license', 'unknown')}。",
        f"- 调研方向：{result.config.direction}",
        f"- 数据：train `{result.dataset_summary.get('train_examples')}` / "
        f"validation `{result.dataset_summary.get('validation_examples')}` / "
        f"test `{result.dataset_summary.get('test_examples')}`。",
        f"- 冠军：`{champion.trial_id}` / `{champion.genome.architecture}`；"
        f"训练目标 `{champion.genome.multimodal_objective}`；"
        f"validation accuracy `{baseline.validation['accuracy']:.4f}→"
        f"{champion.validation['accuracy']:.4f}`；视觉依赖差值 "
        f"`{champion.validation['visual_dependency_delta']:.4f}`。",
    ]
    if result.baseline_test and result.champion_test:
        lines += [
            f"- 隔离 test：accuracy `{result.baseline_test['accuracy']:.4f}→"
            f"{result.champion_test['accuracy']:.4f}`；冠军打乱图/空白图 accuracy "
            f"`{result.champion_test['shuffled_image_accuracy']:.4f}` / "
            f"`{result.champion_test['blank_image_accuracy']:.4f}`。"
        ]
    lines += ["", "## 每轮研究记录", ""]
    for round_ in result.rounds:
        lines += [
            f"### 第 {round_['generation']} 轮", "",
            f"- 起点：`{round_['parent']}`",
            *[
                f"- `{item['trial_id']}`：{item['rationale']}"
                for item in round_["hypotheses"]
            ],
            f"- 决策：{round_['decision']}", "",
        ]
    lines += [
        "## 完整实验轨迹", "",
        "| Trial | 来源 | 结构 | 训练目标 | Accuracy | 打乱图 | 空白图 | 视觉依赖差值 | Fitness | Params |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for trial in result.trials:
        values = trial.validation
        lines.append(
            f"| `{trial.trial_id}` | {_trial_source_label(trial)} | "
            f"`{trial.genome.architecture}` | "
            f"`{trial.genome.multimodal_objective}` | "
            f"{values.get('accuracy', 0):.4f} | "
            f"{values.get('shuffled_image_accuracy', 0):.4f} | "
            f"{values.get('blank_image_accuracy', 0):.4f} | "
            f"{values.get('visual_dependency_delta', 0):.4f} | "
            f"{trial.fitness:.4f} | {trial.training.get('parameters', 0)} |"
        )
    is_synthetic = result.dataset_summary.get("evaluation_tier") == "l0_synthetic"
    lines += [
        "", "## 协议与边界", "",
        (
            "- L0 使用程序生成但真实渲染的像素图像，不是公开自然图像数据集。"
            if is_synthetic else
            f"- L1 使用 `{result.config.dataset}` 官方公开图像；任务是缩小的 object QA，不等同于开放式 VQA。"
        ),
        "- 打乱图和空白图是强制对照，用来识别只依赖问题文本的捷径。",
        "- validation 选择冠军，test 仅在全部代际结束后运行；负结果完整保留。",
        "- L0/L1 结果都不宣称通用视觉语言能力；L2/L3 仍需标准 VLM checkpoint 与 benchmark。", "",
    ]
    return "\n".join(lines)


def _render_checkpoint_multimodal_report(result: EvolutionResult) -> str:
    champion = next(
        trial for trial in result.trials if trial.trial_id == result.champion_id
    )
    baseline = result.trials[0]
    lines = [
        "# 真实 VLM checkpoint 自动进化报告", "", "## 结论", "",
        f"- Benchmark：`{result.config.dataset}`；固定模型："
        f"`{result.config.checkpoint_model_id}`。",
        f"- 请求 revision：`{result.config.checkpoint_revision}`；实际解析 revision "
        f"记录在每个 trial 的 `training.model_revision`。",
        f"- 数据：validation `{result.dataset_summary.get('validation_examples')}` / "
        f"test `{result.dataset_summary.get('test_examples')}`；validation 选择、test 隔离报告。",
        f"- 冠军：`{champion.trial_id}`；validation accuracy "
        f"`{baseline.validation['accuracy']:.4f}→{champion.validation['accuracy']:.4f}`；"
        f"parse rate `{champion.validation['parse_rate']:.4f}`。",
        f"- 冠军推理配方：prompt=`{champion.genome.checkpoint_prompt_style}`，"
        f"hint=`{champion.genome.checkpoint_use_hint}`，image size="
        f"`{champion.genome.checkpoint_image_size or 'native'}`，max new tokens="
        f"`{champion.genome.checkpoint_max_new_tokens}`。",
    ]
    if result.baseline_test and result.champion_test:
        lines += [
            f"- 隔离 test accuracy：`{result.baseline_test['accuracy']:.4f}→"
            f"{result.champion_test['accuracy']:.4f}`；该结果没有参与选择。"
        ]
    lines += ["", "## 每轮研究记录", ""]
    for round_ in result.rounds:
        lines += [
            f"### 第 {round_['generation']} 轮", "",
            f"- 起点：`{round_['parent']}`",
            *[f"- `{item['trial_id']}`：{item['rationale']}" for item in round_["hypotheses"]],
            f"- 决策：{round_['decision']}", "",
        ]
    lines += [
        "## 完整实验轨迹", "",
        "| Trial | Prompt | Hint | Image size | Tokens | Accuracy | Image | Text | Parse | Latency/example | Peak GPU MB |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for trial in result.trials:
        values = trial.validation
        lines.append(
            f"| `{trial.trial_id}` | `{trial.genome.checkpoint_prompt_style}` | "
            f"`{trial.genome.checkpoint_use_hint}` | "
            f"{trial.genome.checkpoint_image_size or 'native'} | "
            f"{trial.genome.checkpoint_max_new_tokens} | "
            f"{values.get('accuracy', 0):.4f} | {values.get('image_accuracy', 0):.4f} | "
            f"{values.get('text_accuracy', 0):.4f} | {values.get('parse_rate', 0):.4f} | "
            f"{values.get('latency_seconds_per_example', 0):.4f} | "
            f"{values.get('peak_gpu_memory_mb', 0):.1f} |"
        )
    lines += [
        "", "## 协议与边界", "",
        "- 模型权重在所有 trial 中冻结并只加载一次；进化的是可审计推理配方。",
        "- validation 是唯一晋级信号；test 仅在全部代际后比较初始基线和冠军。",
        "- checkpoint、预测明细和运行目录不提交 Git；只保存指标、revision 和复现命令。",
        "- 单 seed 或截断样本属于工程验证，不能声明稳定 benchmark 提升。", "",
    ]
    return "\n".join(lines)


def _render_composable_report(result: EvolutionResult) -> str:
    champion = next(
        trial for trial in result.trials if trial.trial_id == result.champion_id
    )
    baseline = result.trials[0]
    is_agent = result.config.model == "agent"
    lines = [
        f"# {result.config.model} 组合式自动进化报告",
        "",
        "## 结论",
        "",
        f"- 数据 / benchmark：`{result.config.dataset}`",
        f"- 调研方向：{result.config.direction}",
        f"- 代数 / population / workers：`{result.config.generations}` / "
        f"`{result.config.population}` / `{result.config.workers}`",
        f"- validation 冠军：`{champion.trial_id}`；fitness "
        f"`{baseline.fitness:.5f}→{champion.fitness:.5f}`",
    ]
    if is_agent:
        lines += [
            f"- 组合：memory=`{champion.genome.agent_memory}`，"
            f"planner=`{champion.genome.agent_planner}`，"
            f"tool policy=`{champion.genome.agent_tool_policy}`，"
            f"critic=`{champion.genome.agent_critic}`，"
            f"capacity=`{champion.genome.memory_size}`",
            f"- validation：joint success "
            f"`{champion.validation['joint_success']:.4f}`，average cost "
            f"`{champion.validation['average_cost']:.4f}`，reuse "
            f"`{champion.validation['reuse_rate']:.4f}`",
        ]
    else:
        lines += [
            f"- 组合：objective=`{champion.genome.post_training}`，"
            f"data=`{champion.genome.post_data_recipe}`，"
            f"teacher=`{champion.genome.post_teacher}`，"
            f"rollout=`{champion.genome.post_rollout}`，"
            f"learning rate=`{champion.genome.learning_rate}`，"
            f"group size=`{champion.genome.group_size}`，"
            f"steps=`{champion.genome.post_steps}`，"
            f"accumulation=`{champion.genome.gradient_accumulation}`，"
            f"precision=`{champion.genome.mixed_precision}`",
            f"- validation：accuracy `{champion.validation['accuracy']:.4f}`，"
            f"KL `{champion.validation['kl_from_reference']:.4f}`",
        ]
    lines += [
        "",
        "## 候选来源说明",
        "",
        "- 论文算子来自仓库中已实现、已测试的方法；检索到但未实现的论文不会执行。",
        "- 无论文 ID 的子代是已实现组件的组合或超参数变异，不是现场生成的新代码。",
        "",
        "## 每轮研究记录",
        "",
    ]
    for round_ in result.rounds:
        lines += [
            f"### 第 {round_['generation']} 轮",
            "",
            f"- 父代：`{round_['parent']}`",
            *[
                f"- `{item['trial_id']}`：{item['rationale']}"
                for item in round_["hypotheses"]
            ],
            f"- 决策：{round_['decision']}",
            "",
        ]
    lines += [
        "## 完整实验轨迹",
        "",
        "| Trial | 来源 | 代 | Fitness | Genome | 状态 |",
        "|---|---|---:|---:|---|---|",
    ]
    for trial in result.trials:
        genome = json.dumps(
            trial.genome.to_dict(), ensure_ascii=False, sort_keys=True
        ).replace("|", "\\|")
        lines.append(
            f"| `{trial.trial_id}` | {_trial_source_label(trial)} | {trial.generation} | "
            f"{trial.fitness:.5f} | `{genome}` | {trial.status} |"
        )
    lines += [
        "",
        "## 协议边界",
        "",
        "- 只用 validation 选择父代，test 仅在全部代际结束后运行。",
        "- 每个 trial 保存完整组合 genome、父代、失败状态和研究记忆。",
        "- 后训练使用候选策略机制评测；Agent 使用确定性 mini-suite，"
        "均不等同于前沿大模型开放式能力评测。",
        "",
    ]
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
        f"- 公共能力集：Alpaca preference `{summary.get('preference_validation', 0)}`；GSM8K candidate ranking `{summary.get('reasoning_validation', 0)}`",
        f"- 代数 / population / workers：`{result.config.generations}` / `{result.config.population}` / `{result.config.workers}`",
        f"- 评测套件 / 晋级指标：`{result.config.benchmark_suite}` / `{result.config.fitness_metric}`；test 不参与进化",
    ]
    if champion and baseline:
        reduction = 100 * (baseline.validation["perplexity"] - champion.validation["perplexity"]) / max(baseline.validation["perplexity"], 1e-12)
        lines += [
            f"- validation 冠军：`{champion.trial_id}` / `{champion.genome.architecture}`；PPL `{baseline.validation['perplexity']:.3f}→{champion.validation['perplexity']:.3f}`（降低 `{reduction:+.2f}%`），instruction loss `{champion.validation['instruction_loss']:.4f}`",
            f"- 公共能力指标：preference accuracy `{champion.validation.get('preference_accuracy', 0.0):.3f}`；GSM8K candidate Pass@1 `{champion.validation.get('reasoning_pass_at_1', 0.0):.3f}`；public composite `{champion.validation.get('public_composite', champion.fitness):.4f}`",
        ]
    if result.baseline_test and result.champion_test:
        reduction = 100 * (result.baseline_test["perplexity"] - result.champion_test["perplexity"]) / max(result.baseline_test["perplexity"], 1e-12)
        lines += [f"- 隔离 test PPL：`{result.baseline_test['perplexity']:.3f}→{result.champion_test['perplexity']:.3f}`（降低 `{reduction:+.2f}%`）"]
    lines += [
        "",
        "## 候选来源说明",
        "",
        "- 带本地算子名称的论文已经实现并通过测试，可以进入训练。",
        "- `evidence-only` 只表示本轮检索到相关论文，不会从 PDF 现场生成代码。",
        "- 无论文 ID 的子代是已实现结构、数据 recipe、后训练方法或超参数的白名单组合。",
        "",
        "## 论文证据与本地算子", "", "| 论文 | 日期 | 可执行研究维度 | 本地机制 |", "|---|---|---|---|"
    ]
    for paper in result.papers:
        lines.append(f"| [{paper.title}]({paper.url}) | {paper.published} | `{paper.architecture or 'evidence-only'}` | {paper.method} |")
    lines += ["", "## 每轮研究记录", ""]
    for round_ in result.rounds:
        lines += [f"### 第 {round_['generation']} 轮", "", f"- 起点：`{round_['parent']}`", "- 假设："]
        lines += [f"  - `{item['trial_id']}`：{item['rationale']}" for item in round_["hypotheses"]]
        observations = []
        for item in round_["observations"]:
            values = item["validation"]
            observations.append(
                f"`{item['trial_id']}` fitness={values.get('fitness', 0.0):.4f}, "
                f"PPL={values.get('perplexity', float('inf')):.3f}, "
                f"preference={values.get('preference_accuracy', 0.0):.3f}, "
                f"GSM8K Pass@1={values.get('reasoning_pass_at_1', 0.0):.3f} ({item['status']})"
            )
        lines += ["- 观察：" + "；".join(observations), f"- 决策：{round_['decision']}", ""]
    lines += [
        "## 验证级联与研究记忆", "",
        f"- NOVA 验证记录：`{len(result.verification_records)}`；通过：`{sum(item['passed'] for item in result.verification_records)}`。",
        f"- EvoRec 成功技能：`{len(result.research_memory.get('successful_skills', []))}`；禁止方向：`{len(result.research_memory.get('forbidden_directions', []))}`。",
        "- 每代结果会形成 architecture gradient，并影响后续候选结构顺序。", "",
    ]
    lines += [
        "## 完整实验轨迹", "",
        "| Trial | 来源 | 代 | Architecture | Data recipe | Post-training | Fitness | Val PPL | Preference | GSM8K Pass@1 | Params | 秒 |",
        "|---|---|---:|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for trial in result.trials:
        lines.append(
            f"| {trial.trial_id} | {_trial_source_label(trial)} | {trial.generation} | `{trial.genome.architecture}` | `{trial.genome.data_recipe}` ({trial.genome.data_mix_ratio:.2f}) | `{trial.genome.post_training}` | {trial.fitness:.4f} | {trial.validation.get('perplexity', float('inf')):.3f} | {trial.validation.get('preference_accuracy', 0.0):.3f} | {trial.validation.get('reasoning_pass_at_1', 0.0):.3f} | {trial.training.get('parameters', 0)} | {trial.duration_seconds:.1f} |"
        )
    lines += [
        "", "## 协议与边界", "",
        "- 这是 Mac 可运行的小型 decoder-only LM 研究平台，不把百万级参数本地结果称为前沿大模型能力。",
        "- WikiText-2 是标准 benchmark 数据，但本地 BPE tokenizer 不同于论文 tokenizer；PPL 只在本次同 tokenizer 实验内部公平比较。",
        "- 第一轮研究结构，第二轮研究训练数据，第三轮研究后训练；同一轮尽量冻结其他变量。",
        "- instruction loss 来自 Stanford Alpaca held-out 子集，不代表完整对话、知识、推理或安全能力。",
        "- public 套件额外用 Alpaca 构造的确定性 response preference 和 GSM8K 多候选 Pass@1；它们是固定公共能力切片，不等同于开放式生成评测。",
        "- checkpoint、tokenizer cache、数据与 raw runs 不提交 Git；JSON/Markdown/HTML 保存全部配置、负结果和失败信息。", "",
    ]
    return "\n".join(lines)


def render_dashboard(result: EvolutionResult) -> str:
    data = result.to_dict()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    title = f"{result.config.model} 自动研究"
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>body{{margin:0;background:#f5f7fb;color:#172033;font:15px system-ui,-apple-system,sans-serif}}main{{max-width:1180px;margin:auto;padding:32px}}h1{{margin:0}}.muted{{color:#65708a}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:24px 0}}.card,section{{background:white;border:1px solid #e4e8f0;border-radius:14px;padding:18px;box-shadow:0 3px 12px #1b274510}}.value{{font-size:26px;font-weight:700;margin-top:7px}}section{{margin:16px 0}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border-bottom:1px solid #edf0f5;text-align:left}}.good{{color:#087f5b}}.bad{{color:#c92a2a}}.bar{{height:9px;background:#4263eb;border-radius:6px;min-width:2px}}code{{background:#f1f3f8;padding:2px 5px;border-radius:4px}}details{{margin:10px 0}}@media(max-width:700px){{main{{padding:18px}}.scroll{{overflow:auto}}}}</style></head><body><main><h1>{title}</h1><p class="muted" id="subtitle"></p><div class="cards" id="cards"></div><section><h2>候选从哪里来</h2><p>论文算子已经在仓库实现并通过测试；<code>evidence-only</code> 论文只作为检索证据，不会执行；无论文 ID 的子代是白名单算子组合或调参，不是现场生成的新代码。</p></section><section><h2>迭代效果</h2><div class="scroll"><table><thead><tr><th>实验</th><th>来源</th><th>轮次</th><th>结构</th><th id="metric-head">主指标</th><th>相对宽度</th><th>状态</th></tr></thead><tbody id="trials"></tbody></table></div></section><section><h2>研究过程</h2><div id="rounds"></div></section><section><h2>验证级联与研究记忆</h2><div id="memory"></div></section><section><h2>论文证据</h2><div id="papers"></div></section></main>
<script>const d={payload};const esc=s=>String(s).replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));const trials=d.trials,base=trials[0],champ=trials.find(x=>x.trial_id===d.champion_id)||base,domain=d.config.model,isLLM=domain==='micro-llm',isVLM=domain==='micro-vlm',isCheckpointVLM=domain==='vlm-checkpoint',isReasoning=domain==='reasoning-checkpoint',isPost=domain==='post-training',isAgent=domain==='agent',selected=d.config.fitness_metric==='public_composite'?'Public composite':d.config.fitness_metric==='unirank_composite'?'UniRank composite':'Primary fitness';const metric=x=>Number(x.validation.fitness??x.fitness),metricLabel=selected,detail=v=>isLLM?'PPL='+Number(v.perplexity).toFixed(3)+', preference='+Number(v.preference_accuracy||0).toFixed(3)+', GSM8K='+Number(v.reasoning_pass_at_1||0).toFixed(3):isCheckpointVLM?'accuracy='+Number(v.accuracy).toFixed(3)+', parse='+Number(v.parse_rate).toFixed(3)+', latency='+Number(v.latency_seconds_per_example).toFixed(3):isReasoning?'accuracy='+Number(v.accuracy).toFixed(3)+', tokens/example='+Number(v.tokens_per_example).toFixed(1)+', latency='+Number(v.latency_seconds_per_example).toFixed(3):isVLM?'accuracy='+Number(v.accuracy).toFixed(3)+', shuffled='+Number(v.shuffled_image_accuracy).toFixed(3)+', visual delta='+Number(v.visual_dependency_delta).toFixed(3):isPost?'accuracy='+Number(v.accuracy).toFixed(3)+', KL='+Number(v.kl_from_reference).toFixed(3):isAgent?'success='+Number(v.joint_success).toFixed(3)+', cost='+Number(v.average_cost).toFixed(3)+', reuse='+Number(v.reuse_rate).toFixed(3):'NDCG@10='+Number(v.ndcg_at_10).toFixed(5)+', suite='+Number(v.unirank_composite||v.public_composite||v.ndcg_at_10).toFixed(5),source=x=>x.generation===0?'初始基线':(x.source_papers||[]).length?'论文算子 '+x.source_papers.join(', '):'白名单组合 / 调参';document.querySelector('#metric-head').textContent=metricLabel;const summary=isLLM?d.dataset_summary.train_tokens+' train tokens':isCheckpointVLM?d.dataset_summary.validation_examples+' validation examples':isReasoning?d.dataset_summary.budget_axis+' · '+d.dataset_summary.seeds.length+' seeds':isVLM?d.dataset_summary.train_examples+' rendered train images':isPost?d.dataset_summary.algorithms+' algorithms · '+d.dataset_summary.seeds.length+' seeds':isAgent?d.dataset_summary.episodes+' episodes · '+d.dataset_summary.genome_axes.join(' / '):d.dataset_summary.users+' users / '+d.dataset_summary.items+' items';document.querySelector('#subtitle').textContent=d.config.direction+' · '+d.config.dataset+' · '+summary;const gain=(metric(champ)-metric(base))/Math.max(Math.abs(metric(base)),1e-12)*100;const headline=isLLM?'PPL '+Number(champ.validation.perplexity).toFixed(3):isCheckpointVLM?'Accuracy '+Number(champ.validation.accuracy).toFixed(3):isReasoning?'Accuracy '+Number(champ.validation.accuracy).toFixed(3):isVLM?'Accuracy '+Number(champ.validation.accuracy).toFixed(3):isPost?'Accuracy '+Number(champ.validation.accuracy).toFixed(3):isAgent?'Success '+Number(champ.validation.joint_success).toFixed(3):'NDCG '+Number(champ.validation.ndcg_at_10).toFixed(5);document.querySelector('#cards').innerHTML=[['当前冠军',champ.trial_id],['冠军结构',champ.genome.architecture],[metricLabel,metric(champ).toFixed(5)],['相对基线',(gain>=0?'+':'')+gain.toFixed(2)+'%'],['总体主指标',headline],['已完成进化轮数',d.rounds.length],['实验数（含基线）',trials.length],['并行 workers',d.config.workers]].map(x=>`<div class="card"><div class="muted">${{esc(x[0])}}</div><div class="value">${{esc(x[1])}}</div></div>`).join('');const completed=trials.filter(x=>x.status==='completed'),best=Math.max(...completed.map(metric)),worst=Math.min(...completed.map(metric)),span=Math.max(best-worst,1e-12);document.querySelector('#trials').innerHTML=trials.map(x=>`<tr><td><code>${{esc(x.trial_id)}}</code></td><td>${{esc(source(x))}}</td><td>${{x.generation}}</td><td>${{esc(x.genome.architecture)}}</td><td>${{metric(x).toFixed(5)}}</td><td><div class="bar" style="width:${{Math.max(3,(metric(x)-worst)/span*100)}}%"></div></td><td class="${{x.status==='completed'?'good':'bad'}}">${{esc(x.status)}}</td></tr>`).join('');document.querySelector('#rounds').innerHTML=d.rounds.map(r=>`<details open><summary><b>第 ${{r.generation}} 轮</b> · ${{esc(r.decision)}}</summary><p><b>假设</b></p><ul>${{r.hypotheses.map(h=>`<li><code>${{esc(h.trial_id)}}</code> ${{esc(h.rationale)}}</li>`).join('')}}</ul><p><b>观察</b></p><ul>${{r.observations.map(o=>`<li>${{esc(o.trial_id)}}: fitness=${{Number(o.validation.fitness).toFixed(5)}}; ${{detail(o.validation)}} (${{esc(o.status)}})</li>`).join('')}}</ul></details>`).join('')||'<p class="muted">尚未完成第一轮。</p>';const vr=d.verification_records||[],rm=d.research_memory||{{}};document.querySelector('#memory').innerHTML=`<p>验证通过 <b>${{vr.filter(x=>x.passed).length}} / ${{vr.length}}</b>；成功技能 <b>${{(rm.successful_skills||[]).length}}</b>；禁止方向 <b>${{(rm.forbidden_directions||[]).length}}</b>。</p><details><summary>Architecture gradients</summary><ul>${{(rm.architecture_gradients||[]).map(x=>`<li><code>${{esc(x.trial_id)}}</code> ${{esc(x.architecture)}}：${{Number(x.fitness_delta).toFixed(5)}}</li>`).join('')}}</ul></details>`;document.querySelector('#papers').innerHTML=d.papers.length?'<ul>'+d.papers.map(p=>`<li><b>${{p.architecture?'可执行':'仅证据'}}</b> · <a href="${{esc(p.url)}}">${{esc(p.title)}}</a>：${{esc(p.method)}} <code>${{esc(p.architecture||'evidence-only')}}</code></li>`).join('')+'</ul>':'<p class="muted">本轮使用仓库内已实现的组合算子，没有新增外部论文候选。</p>';</script></body></html>'''
