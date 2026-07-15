# automated-w2s-research 架构采用记录

本项目曾将 [safety-research/automated-w2s-research](https://github.com/safety-research/automated-w2s-research) 作为架构参考。两者真正可以复用的是自动研究流程，而不是 weak-to-strong 任务本身。

## 结论

不直接合并上游仓库，而是采用净室、渐进式重构：只吸收适合本项目的通用架构思想，不复制上游实现和重型运行环境。

| 上游能力 | 决策 | 本地实现 |
|---|---|---|
| 每个研究想法使用独立目录 | 采用 | 继续以 `reproductions/<paper>/adapter.py` 插件作为扩展单元 |
| 统一运行配置 | 采用 | `ResearchConfig` 统一管理论文发现、实现、实验、缓存和可复现配置 |
| idea → train → evaluate 迭代循环 | 采用 | `research_loop.IterativeResearchLoop` 将自适应提案、评估和 checkpoint 回调解耦 |
| 分层结果缓存 | 缩小后采用 | 使用内容寻址、按 track/experiment 隔离的指标缓存；失败实验和 checkpoint 不缓存 |
| Agent 可读取的研究历史 | 采用 | 追加写入 `events.jsonl`，记录阶段、trial、缓存命中和完成状态 |
| 隐藏标签的远程评估器 | 保留边界，不复制实现 | 论文 adapter 只能用 validation 选型，并且 test 只评估一次；未来可用独立服务实现同一边界 |
| Claude Agent SDK 循环 | 不合并 | 与特定供应商绑定，本地优先的核心不需要它；Agent 提案以后可以接入通用 proposal 接口 |
| Flask/React 控制台 | 暂缓 | 在并发远程 worker 成为真实需求前，继续以 CLI 和不可变产物为主要界面 |
| Docker/RunPod/S3/VERL 运行栈 | 不合并 | CUDA/Linux 专用依赖与当前 Mac 优先、轻量安装的目标冲突 |

## 为什么不直接合并源码

上游环境固定了一套大型 CUDA 训练栈，包括 PyTorch、vLLM、FlashAttention、Unsloth、SGLang、Ray/VERL、RunPod 和 S3 客户端；它的启动器与自动循环还依赖 Anthropic 凭证和常驻服务。如果直接引入，会让一个基础的本地 MovieLens 实验也依赖大量与当前目标无关的基础设施。

上游 README 声明采用 MIT 许可证，但当时审查的仓库快照中没有被 Git 跟踪的 `LICENSE` 文件。因此本项目没有复制上游源码，只独立实现上述通用架构模式，并继续使用本仓库现有的 MIT 许可证。

## 扩展接口

迭代循环接收一组参数字典，以及一个负责评估的 callable：

```python
loop = IterativeResearchLoop(
    evaluate=evaluate,
    direction="maximize",
    cache=cache,
    cache_context=context,
)
trials, best = loop.run(proposals, on_trial=checkpoint)
```

默认情况下，`proposals` 来自确定性的搜索空间。`ProposalStrategy.propose(history)` 可以读取此前所有成功、失败和缓存命中记录。内置的 `CommandProposer` 通过 `AUTO_RESEARCH_MANIFEST` 与 `AUTO_RESEARCH_HISTORY` 暴露这些信息，因此 Codex、Claude 或本地 Agent 可以根据论文内容和真实实验结果生成下一个候选，而不需要修改实验执行、缓存、报告或论文 adapter。

## 产物与缓存边界

每次 topic 研究会产生：

```text
runs/<timestamp>/
├── result.json
├── report.md
└── events.jsonl
```

可复用的指标缓存位于 `.auto-research/cache/<track>/<experiment>/`，并由 Git 忽略。自定义实验命令只有在显式设置 `experiment_revision` 时才允许读取缓存，避免实验代码变化后静默复用旧结果；`force_rerun` 可以跳过缓存读取。数据集、原始日志和模型 checkpoint 始终不进入指标缓存。
