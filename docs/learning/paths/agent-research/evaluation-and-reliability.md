---
hide:
  - toc
---

<!-- Generated learning path; edit docs/learning/topics/*.json. -->

# 评测与可靠性：如何知道真的做对了

[Agent](index.md) / 172 个问题 · 43 篇论文

先看问题，想一想，再展开答案。这里持续积累本子主题各篇论文的问答，一篇论文也可以追加多个问题。

<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12" data-learning-unit="问">
<div class="ar-learning-controls">
<label for="learning-search">搜索问题
<input id="learning-search" type="search" data-learning-search placeholder="搜索问题、论文或机制"></label>
</div>
<div class="ar-learning-levels" role="group" aria-label="学习层次">
<span>学习层次</span>
<button type="button" data-learning-level="" aria-pressed="true">全部</button>
<button type="button" data-learning-level="basics" aria-pressed="false">基础理解</button>
<button type="button" data-learning-level="mechanism" aria-pressed="false">核心机制</button>
<button type="button" data-learning-level="comparison" aria-pressed="false">方法对比</button>
<button type="button" data-learning-level="implementation" aria-pressed="false">实现细节</button>
</div>
<p class="ar-learning-status" data-learning-status role="status">172 个问题 · 43 篇论文</p>
<noscript>已显示全部问题；启用 JavaScript 后可搜索和筛选。</noscript>
<div class="ar-learning-grid">
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:physical-engineering-exam" data-paper-title="PLE: Physical-Engineering&#x27;s Last Exam" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PLE: Physical-Engineering&#x27;s Last Exam Agent Google Cloud AI Research 2026-10-21 PLE把专业工程工作组织为85项长时任务，覆盖结构、土木、电气及机械；输入是多格式项目文件，输出是可审查的工程产物。任务由专家编写，或经Creator–Solver迭代后由专家复核；裁判与参考解不向solver暴露。正文、实验及附录已读，最新公开提交协议另按固定代码版本核验。本地只执行配置、产物检查与给定外部评分的聚合；图中的独立grader仍是未运行的外部步骤。不会把合成文件当作真实工程结果。 因此成本过高，不复现（审查 DONE），不下载任务镜像/大权重、不启动昂贵试跑或自动重试。10月23日官方代码固定29项public dev、56项hidden test。任务配置的原始YAML SHA256为 c36cab6f0f3a1ab613e5b507e13dad80f56d3eec370019969965f5a32edaed1e，对应配置内数据revision为 535cf0a8af68126e3f00a1441cf736754a0cda4b。测试夹具仅含公开配置转成的JSON，不含题目环境、grader、参考解或任务答案。  公开评测协议 工程产物验收与来源隔离 Agent 评测与可靠性：如何知道真的做对了 PLE 为什么要求提交可审查工程产物，而不只生成一段回答？ 长时工程任务包含多格式输入、约束和成果文件，最终要核验实际产物满足要求。benchmark通过专家或独立grader评价，不能把流畅文字当成已完成设计。 示意：提交一个说明文档，并不自动证明相应工程文件真实存在或通过约束。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-physical-engineering-exam-2277e47a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-98b62ddbf22d1aa8">PLE 为什么要求提交可审查工程产物，而不只生成一段回答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aphysical-engineering-exam">PLE: Physical-Engineering&#x27;s Last Exam</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长时工程任务包含多格式输入、约束和成果文件，最终要核验实际产物满足要求。benchmark通过专家或独立grader评价，不能把流畅文字当成已完成设计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>提交一个说明文档，并不自动证明相应工程文件真实存在或通过约束。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30537v1">原论文</a> · <a href="../../../../agent-research/2610.30537-physical-engineering-exam/">实现解读</a> · <a href="#qa-98b62ddbf22d1aa8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:physical-engineering-exam" data-paper-title="PLE: Physical-Engineering&#x27;s Last Exam" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PLE: Physical-Engineering&#x27;s Last Exam Agent Google Cloud AI Research 2026-10-21 PLE把专业工程工作组织为85项长时任务，覆盖结构、土木、电气及机械；输入是多格式项目文件，输出是可审查的工程产物。任务由专家编写，或经Creator–Solver迭代后由专家复核；裁判与参考解不向solver暴露。正文、实验及附录已读，最新公开提交协议另按固定代码版本核验。本地只执行配置、产物检查与给定外部评分的聚合；图中的独立grader仍是未运行的外部步骤。不会把合成文件当作真实工程结果。 因此成本过高，不复现（审查 DONE），不下载任务镜像/大权重、不启动昂贵试跑或自动重试。10月23日官方代码固定29项public dev、56项hidden test。任务配置的原始YAML SHA256为 c36cab6f0f3a1ab613e5b507e13dad80f56d3eec370019969965f5a32edaed1e，对应配置内数据revision为 535cf0a8af68126e3f00a1441cf736754a0cda4b。测试夹具仅含公开配置转成的JSON，不含题目环境、grader、参考解或任务答案。  公开评测协议 工程产物验收与来源隔离 Agent 评测与可靠性：如何知道真的做对了 约束型任务为什么用硬门 G 切断目标分，而非让目标优化抵消硬约束失败？ 工程产物可能目标值漂亮却违反必须满足的条件，硬门要求全部硬约束通过才计算那部分收益。约束比例仍提供分项信息，完整任务分母保留缺失项为零；本地评分聚合只消费外部裁判，不具备判断物理可行性或专业规范的独立能力。 例如设计重量很低但关键承载条件失败，不能让轻量化高分抵消硬失败；缺交产物也不能从平均分里删掉。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-481c8954021f31c4">约束型任务为什么用硬门 G 切断目标分，而非让目标优化抵消硬约束失败？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aphysical-engineering-exam">PLE: Physical-Engineering&#x27;s Last Exam</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工程产物可能目标值漂亮却违反必须满足的条件，硬门要求全部硬约束通过才计算那部分收益。约束比例仍提供分项信息，完整任务分母保留缺失项为零；本地评分聚合只消费外部裁判，不具备判断物理可行性或专业规范的独立能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如设计重量很低但关键承载条件失败，不能让轻量化高分抵消硬失败；缺交产物也不能从平均分里删掉。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30537v1">原论文</a> · <a href="../../../../agent-research/2610.30537-physical-engineering-exam/">实现解读</a> · <a href="#qa-481c8954021f31c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:physical-engineering-exam" data-paper-title="PLE: Physical-Engineering&#x27;s Last Exam" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PLE: Physical-Engineering&#x27;s Last Exam Agent Google Cloud AI Research 2026-10-21 PLE把专业工程工作组织为85项长时任务，覆盖结构、土木、电气及机械；输入是多格式项目文件，输出是可审查的工程产物。任务由专家编写，或经Creator–Solver迭代后由专家复核；裁判与参考解不向solver暴露。正文、实验及附录已读，最新公开提交协议另按固定代码版本核验。本地只执行配置、产物检查与给定外部评分的聚合；图中的独立grader仍是未运行的外部步骤。不会把合成文件当作真实工程结果。 因此成本过高，不复现（审查 DONE），不下载任务镜像/大权重、不启动昂贵试跑或自动重试。10月23日官方代码固定29项public dev、56项hidden test。任务配置的原始YAML SHA256为 c36cab6f0f3a1ab613e5b507e13dad80f56d3eec370019969965f5a32edaed1e，对应配置内数据revision为 535cf0a8af68126e3f00a1441cf736754a0cda4b。测试夹具仅含公开配置转成的JSON，不含题目环境、grader、参考解或任务答案。  公开评测协议 工程产物验收与来源隔离 Agent 评测与可靠性：如何知道真的做对了 PLE 约束型硬门评分，与只按目标值连续打分有什么不同？ 硬约束不满足时G=0，目标优化分被切断，不能用更高目标值抵消违反约束。专家rubric及特殊site/MEP grader又有独立规则，不能用一个通式替代所有任务。 示意：目标效率再高，只要一个硬约束失败，也不能继续获得那0.6GO′项。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c6c2ac1e4e4e940d">PLE 约束型硬门评分，与只按目标值连续打分有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aphysical-engineering-exam">PLE: Physical-Engineering&#x27;s Last Exam</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>硬约束不满足时G=0，目标优化分被切断，不能用更高目标值抵消违反约束。专家rubric及特殊site/MEP grader又有独立规则，不能用一个通式替代所有任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>目标效率再高，只要一个硬约束失败，也不能继续获得那0.6GO′项。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30537v1">原论文</a> · <a href="../../../../agent-research/2610.30537-physical-engineering-exam/">实现解读</a> · <a href="#qa-c6c2ac1e4e4e940d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:physical-engineering-exam" data-paper-title="PLE: Physical-Engineering&#x27;s Last Exam" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PLE: Physical-Engineering&#x27;s Last Exam Agent Google Cloud AI Research 2026-10-21 PLE把专业工程工作组织为85项长时任务，覆盖结构、土木、电气及机械；输入是多格式项目文件，输出是可审查的工程产物。任务由专家编写，或经Creator–Solver迭代后由专家复核；裁判与参考解不向solver暴露。正文、实验及附录已读，最新公开提交协议另按固定代码版本核验。本地只执行配置、产物检查与给定外部评分的聚合；图中的独立grader仍是未运行的外部步骤。不会把合成文件当作真实工程结果。 因此成本过高，不复现（审查 DONE），不下载任务镜像/大权重、不启动昂贵试跑或自动重试。10月23日官方代码固定29项public dev、56项hidden test。任务配置的原始YAML SHA256为 c36cab6f0f3a1ab613e5b507e13dad80f56d3eec370019969965f5a32edaed1e，对应配置内数据revision为 535cf0a8af68126e3f00a1441cf736754a0cda4b。测试夹具仅含公开配置转成的JSON，不含题目环境、grader、参考解或任务答案。  公开评测协议 工程产物验收与来源隔离 Agent 评测与可靠性：如何知道真的做对了 PLE 聚合结果时，为什么必须保留全部任务分母与缺失项？ 每run按完整任务集平均，缺失评分记0，再对三个run均值求平均；只对已成功提交项求均值会虚高。本地只接外部grader结果和产物字节，不独立认证物理或法规正确性。 示意：85项只完成10项，不能把这10项的平均分直接报告为完整benchmark均值。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-721a9cf4dbf5ae04">PLE 聚合结果时，为什么必须保留全部任务分母与缺失项？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aphysical-engineering-exam">PLE: Physical-Engineering&#x27;s Last Exam</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每run按完整任务集平均，缺失评分记0，再对三个run均值求平均；只对已成功提交项求均值会虚高。本地只接外部grader结果和产物字节，不独立认证物理或法规正确性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>85项只完成10项，不能把这10项的平均分直接报告为完整benchmark均值。</p>
<p class="ar-learning-sources">依据：核心公式、离线验收接口；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.30537v1">原论文</a> · <a href="../../../../agent-research/2610.30537-physical-engineering-exam/">实现解读</a> · <a href="#qa-721a9cf4dbf5ae04">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scope-replay" data-paper-title="SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning Agent Peking University 2026-10-16 修改机器人控制程序可能修好新场景却破坏旧场景。SCOPE 从开发执行证据建立失败前沿图，区分有证据支持、被反驳和未知检查，按局部修补、阶段重设或策略重生成继续搜索。它记录过去成功实例的完整 API tape，在候选源变化时，抽取至多三个历史见证进行本地有状态重放；重放有分歧的实例才可能安排稀疏真实环境诊断。§3 原论文 Figure 2 是有状态 API 重放与认证图；Figure 1 是整体搜索流程。需保留二者区别。原图由本批统一资源流程处理。 完整实验成本过高，不复现（审查 DONE）；不实现视觉 critic、失败前沿图、LLM repair 或真实环境诊断。component_only / L1 CPU 状态重放组件；不是机器人 Agent、完整程序搜索或 held-out 能力评测。真实执行可信 Python 回调的 API 记录与重放：有限标量、字符串键 dict、list、tuple，包含可变容器别名、循环引用、API 返回值指向既有容器、原地副作用和白名单内建异常。前后状态来自同一对象身份表；不能用逐项 deepcopy 破坏别名。另对最终公共状态做保守匹配，防止最后一次 API 之后的本地修改被误认证。  规划、推理与工具使用 有状态重放与实例认证 Agent 评测与可靠性：如何知道真的做对了 SCOPE 为什么保存成功执行的有状态 API tape？ 修改程序后重新跑所有旧场景很贵，完整tape保留请求、前后公共状态及返回/异常，可在同一记录实例上重放候选，帮助发现需要进一步真实诊断的分歧。 示意：一个旧成功场景可先用完整API交互证据检查，而不立即重新启动机器人环境。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-scope-replay-4a09ab7b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-27c3a63c95f1b011">SCOPE 为什么保存成功执行的有状态 API tape？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascope-replay">SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>修改程序后重新跑所有旧场景很贵，完整tape保留请求、前后公共状态及返回/异常，可在同一记录实例上重放候选，帮助发现需要进一步真实诊断的分歧。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个旧成功场景可先用完整API交互证据检查，而不立即重新启动机器人环境。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23128">原论文</a> · <a href="../../../../agent-research/2610.23128-scope-replay/">实现解读</a> · <a href="#qa-27c3a63c95f1b011">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scope-replay" data-paper-title="SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning Agent Peking University 2026-10-16 修改机器人控制程序可能修好新场景却破坏旧场景。SCOPE 从开发执行证据建立失败前沿图，区分有证据支持、被反驳和未知检查，按局部修补、阶段重设或策略重生成继续搜索。它记录过去成功实例的完整 API tape，在候选源变化时，抽取至多三个历史见证进行本地有状态重放；重放有分歧的实例才可能安排稀疏真实环境诊断。§3 原论文 Figure 2 是有状态 API 重放与认证图；Figure 1 是整体搜索流程。需保留二者区别。原图由本批统一资源流程处理。 完整实验成本过高，不复现（审查 DONE）；不实现视觉 critic、失败前沿图、LLM repair 或真实环境诊断。component_only / L1 CPU 状态重放组件；不是机器人 Agent、完整程序搜索或 held-out 能力评测。真实执行可信 Python 回调的 API 记录与重放：有限标量、字符串键 dict、list、tuple，包含可变容器别名、循环引用、API 返回值指向既有容器、原地副作用和白名单内建异常。前后状态来自同一对象身份表；不能用逐项 deepcopy 破坏别名。另对最终公共状态做保守匹配，防止最后一次 API 之后的本地修改被误认证。  规划、推理与工具使用 有状态重放与实例认证 Agent 评测与可靠性：如何知道真的做对了 API tape 重放成功，为什么不能当作所有输入的程序等价证明或候选接纳门？ 重放只检查记录实例在给定状态、返回和异常下是否一致，未见输入仍未知。它用于选择值得真实环境诊断的差异，不决定成功候选必须回滚；原生环境成功才更新 accepted program，重放分歧也只是证据差异，不能直接记成环境失败。 例如旧案例的返回顺序与新程序不同，可触发重点复测；若新程序已在真实环境完成当前任务，不能仅因旧 tape 不兼容就擅自拒绝。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9bb2e7154e6a7783">API tape 重放成功，为什么不能当作所有输入的程序等价证明或候选接纳门？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascope-replay">SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重放只检查记录实例在给定状态、返回和异常下是否一致，未见输入仍未知。它用于选择值得真实环境诊断的差异，不决定成功候选必须回滚；原生环境成功才更新 accepted program，重放分歧也只是证据差异，不能直接记成环境失败。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如旧案例的返回顺序与新程序不同，可触发重点复测；若新程序已在真实环境完成当前任务，不能仅因旧 tape 不兼容就擅自拒绝。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23128">原论文</a> · <a href="../../../../agent-research/2610.23128-scope-replay/">实现解读</a> · <a href="#qa-9bb2e7154e6a7783">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scope-replay" data-paper-title="SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning Agent Peking University 2026-10-16 修改机器人控制程序可能修好新场景却破坏旧场景。SCOPE 从开发执行证据建立失败前沿图，区分有证据支持、被反驳和未知检查，按局部修补、阶段重设或策略重生成继续搜索。它记录过去成功实例的完整 API tape，在候选源变化时，抽取至多三个历史见证进行本地有状态重放；重放有分歧的实例才可能安排稀疏真实环境诊断。§3 原论文 Figure 2 是有状态 API 重放与认证图；Figure 1 是整体搜索流程。需保留二者区别。原图由本批统一资源流程处理。 完整实验成本过高，不复现（审查 DONE）；不实现视觉 critic、失败前沿图、LLM repair 或真实环境诊断。component_only / L1 CPU 状态重放组件；不是机器人 Agent、完整程序搜索或 held-out 能力评测。真实执行可信 Python 回调的 API 记录与重放：有限标量、字符串键 dict、list、tuple，包含可变容器别名、循环引用、API 返回值指向既有容器、原地副作用和白名单内建异常。前后状态来自同一对象身份表；不能用逐项 deepcopy 破坏别名。另对最终公共状态做保守匹配，防止最后一次 API 之后的本地修改被误认证。  规划、推理与工具使用 有状态重放与实例认证 Agent 评测与可靠性：如何知道真的做对了 SCOPE 的重放分歧，与真实环境执行失败是同一种结论吗？ 不是。分歧说明候选与记录见证不匹配或不可用，是后续搜索证据；真实环境失败需要实际执行。未知不能当失败，重放也不是对所有输入的程序等价证明。 示意：新程序多查询了一次API，可能导致tape分歧，但尚不能据此断定环境任务失败。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-47affe69bc9f6270">SCOPE 的重放分歧，与真实环境执行失败是同一种结论吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascope-replay">SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。分歧说明候选与记录见证不匹配或不可用，是后续搜索证据；真实环境失败需要实际执行。未知不能当失败，重放也不是对所有输入的程序等价证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新程序多查询了一次API，可能导致tape分歧，但尚不能据此断定环境任务失败。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23128">原论文</a> · <a href="../../../../agent-research/2610.23128-scope-replay/">实现解读</a> · <a href="#qa-47affe69bc9f6270">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scope-replay" data-paper-title="SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning Agent Peking University 2026-10-16 修改机器人控制程序可能修好新场景却破坏旧场景。SCOPE 从开发执行证据建立失败前沿图，区分有证据支持、被反驳和未知检查，按局部修补、阶段重设或策略重生成继续搜索。它记录过去成功实例的完整 API tape，在候选源变化时，抽取至多三个历史见证进行本地有状态重放；重放有分歧的实例才可能安排稀疏真实环境诊断。§3 原论文 Figure 2 是有状态 API 重放与认证图；Figure 1 是整体搜索流程。需保留二者区别。原图由本批统一资源流程处理。 完整实验成本过高，不复现（审查 DONE）；不实现视觉 critic、失败前沿图、LLM repair 或真实环境诊断。component_only / L1 CPU 状态重放组件；不是机器人 Agent、完整程序搜索或 held-out 能力评测。真实执行可信 Python 回调的 API 记录与重放：有限标量、字符串键 dict、list、tuple，包含可变容器别名、循环引用、API 返回值指向既有容器、原地副作用和白名单内建异常。前后状态来自同一对象身份表；不能用逐项 deepcopy 破坏别名。另对最终公共状态做保守匹配，防止最后一次 API 之后的本地修改被误认证。  规划、推理与工具使用 有状态重放与实例认证 Agent 评测与可靠性：如何知道真的做对了 SCOPE 重放时只比较 API 名称和返回值，足以恢复有状态执行吗？ 还要匹配请求及前状态，并恢复后状态突变、异常与共享引用，完整消费tape且无额外外部调用。accepted program由原生环境成功更新，不能私自把replay改成接纳/回滚门。 示意：两个对象共享同一列表，重放若复制成两个独立列表，即使当前返回值相同也改变后续行为。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3e999aba71132c35">SCOPE 重放时只比较 API 名称和返回值，足以恢复有状态执行吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascope-replay">SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Peking University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>还要匹配请求及前状态，并恢复后状态突变、异常与共享引用，完整消费tape且无额外外部调用。accepted program由原生环境成功更新，不能私自把replay改成接纳/回滚门。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个对象共享同一列表，重放若复制成两个独立列表，即使当前返回值相同也改变后续行为。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.23128">原论文</a> · <a href="../../../../agent-research/2610.23128-scope-replay/">实现解读</a> · <a href="#qa-3e999aba71132c35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-perturb" data-paper-title="AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations Agent The Hong Kong University of Science and Technology (Guangzhou) 2026-10-15 Agent 失败不一定来自模型推理：用户请求缺信息、技能规范过时、历史上下文出错和工具说明漂移都可能沿轨迹传播。AgentPerturb 交叉组织四个目标——用户请求、过程规范、继承上下文、工具契约 ——与缺失、冗余、错误三类扰动，得到12个家族。每对只改一个目标，其余三个、后端和成功 oracle 不变。原文 §3、附录 F 候选不能因为“JSON合法”就入选：与生成器独立的语义 verifier 必须确认单目标、目标不变、仍可求解、可执行四项全部通过，再结合原生 validator。 原文完整配置为10个前沿模型×2真实环境×25任务×12类扰动，单任务可达200轮、约30分钟上限，还需生成/语义验证 API，成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现扰动边界、独立验证与配对记录，不生成官方任务，不声称语法检查能够证明语义保持。每 seed 在无外部副作用的算术/工具契约 fixture 上实际执行全部12家族，actor 只解析公开输入，grader 单独判分。独立的领域 verifier 拒绝改变真实目标的编辑；语法-only负对照会错误放行这些编辑。  公共评测与协议 交互输入扰动与稳健性 Agent 评测与可靠性：如何知道真的做对了 AgentPerturb 为什么一次只扰动 U、P、C、T 中一个目标？ 用户请求、过程规范、历史上下文和工具契约是不同输入面。固定其它输入、后端和成功oracle，才可更清楚观察某类扰动影响；同时修改多个目标会混入额外变化。 示意：只改工具说明而保持用户需求与工具实现不变，才接近一次单目标配对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-agent-perturb-def3e837" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-e8ad67ecaea38b3c">AgentPerturb 为什么一次只扰动 U、P、C、T 中一个目标？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-perturb">AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong University of Science and Technology (Guangzhou)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>用户请求、过程规范、历史上下文和工具契约是不同输入面。固定其它输入、后端和成功oracle，才可更清楚观察某类扰动影响；同时修改多个目标会混入额外变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只改工具说明而保持用户需求与工具实现不变，才接近一次单目标配对。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21624">原论文</a> · <a href="../../../../agent-research/2610.21624-agent-perturb/">实现解读</a> · <a href="#qa-e8ad67ecaea38b3c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-perturb" data-paper-title="AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations Agent The Hong Kong University of Science and Technology (Guangzhou) 2026-10-15 Agent 失败不一定来自模型推理：用户请求缺信息、技能规范过时、历史上下文出错和工具说明漂移都可能沿轨迹传播。AgentPerturb 交叉组织四个目标——用户请求、过程规范、继承上下文、工具契约 ——与缺失、冗余、错误三类扰动，得到12个家族。每对只改一个目标，其余三个、后端和成功 oracle 不变。原文 §3、附录 F 候选不能因为“JSON合法”就入选：与生成器独立的语义 verifier 必须确认单目标、目标不变、仍可求解、可执行四项全部通过，再结合原生 validator。 原文完整配置为10个前沿模型×2真实环境×25任务×12类扰动，单任务可达200轮、约30分钟上限，还需生成/语义验证 API，成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现扰动边界、独立验证与配对记录，不生成官方任务，不声称语法检查能够证明语义保持。每 seed 在无外部副作用的算术/工具契约 fixture 上实际执行全部12家族，actor 只解析公开输入，grader 单独判分。独立的领域 verifier 拒绝改变真实目标的编辑；语法-only负对照会错误放行这些编辑。  公共评测与协议 交互输入扰动与稳健性 Agent 评测与可靠性：如何知道真的做对了 为什么扰动候选通过 JSON 检查后，还必须独立确认目标不变且仍可求解？ 结构合法只保证可解析，扰动可能不小心换了任务或删掉必需信息到无法恢复。单目标语义验证保持其他因素、后端与 oracle 不变，才能解释性能差来自交互压力；缺失评分要报告配对覆盖和界限，不能删掉失败对后宣称鲁棒性良好。 例如只改工具说明措辞应不改工具真实行为；若同时移除唯一必需工具，失败就混入不可解性，不能当同一扰动效果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-0b56c1b86c3904f6">为什么扰动候选通过 JSON 检查后，还必须独立确认目标不变且仍可求解？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-perturb">AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong University of Science and Technology (Guangzhou)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>结构合法只保证可解析，扰动可能不小心换了任务或删掉必需信息到无法恢复。单目标语义验证保持其他因素、后端与 oracle 不变，才能解释性能差来自交互压力；缺失评分要报告配对覆盖和界限，不能删掉失败对后宣称鲁棒性良好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只改工具说明措辞应不改工具真实行为；若同时移除唯一必需工具，失败就混入不可解性，不能当同一扰动效果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21624">原论文</a> · <a href="../../../../agent-research/2610.21624-agent-perturb/">实现解读</a> · <a href="#qa-0b56c1b86c3904f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-perturb" data-paper-title="AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations Agent The Hong Kong University of Science and Technology (Guangzhou) 2026-10-15 Agent 失败不一定来自模型推理：用户请求缺信息、技能规范过时、历史上下文出错和工具说明漂移都可能沿轨迹传播。AgentPerturb 交叉组织四个目标——用户请求、过程规范、继承上下文、工具契约 ——与缺失、冗余、错误三类扰动，得到12个家族。每对只改一个目标，其余三个、后端和成功 oracle 不变。原文 §3、附录 F 候选不能因为“JSON合法”就入选：与生成器独立的语义 verifier 必须确认单目标、目标不变、仍可求解、可执行四项全部通过，再结合原生 validator。 原文完整配置为10个前沿模型×2真实环境×25任务×12类扰动，单任务可达200轮、约30分钟上限，还需生成/语义验证 API，成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现扰动边界、独立验证与配对记录，不生成官方任务，不声称语法检查能够证明语义保持。每 seed 在无外部副作用的算术/工具契约 fixture 上实际执行全部12家族，actor 只解析公开输入，grader 单独判分。独立的领域 verifier 拒绝改变真实目标的编辑；语法-only负对照会错误放行这些编辑。  公共评测与协议 交互输入扰动与稳健性 Agent 评测与可靠性：如何知道真的做对了 AgentPerturb 的语法检查与独立语义 verifier，分别能证明什么？ 语法合法只说明输入可解析，不能证明任务目标保持、仍可求解。候选还需独立语义verifier确认单目标、目标不变、可解和可执行，再结合原生validator；本地算术verifier不代表任意自然语言等价证明。 示意：JSON完全合法，但把“求和”改成“求积”仍改变了目标，不能当稳健性扰动。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5b7e2047d62548dd">AgentPerturb 的语法检查与独立语义 verifier，分别能证明什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-perturb">AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong University of Science and Technology (Guangzhou)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>语法合法只说明输入可解析，不能证明任务目标保持、仍可求解。候选还需独立语义verifier确认单目标、目标不变、可解和可执行，再结合原生validator；本地算术verifier不代表任意自然语言等价证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>JSON完全合法，但把“求和”改成“求积”仍改变了目标，不能当稳健性扰动。</p>
<p class="ar-learning-sources">依据：背景与主要改动、真实性、gold 隔离与成本；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21624">原论文</a> · <a href="../../../../agent-research/2610.21624-agent-perturb/">实现解读</a> · <a href="#qa-5b7e2047d62548dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agent-perturb" data-paper-title="AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations Agent The Hong Kong University of Science and Technology (Guangzhou) 2026-10-15 Agent 失败不一定来自模型推理：用户请求缺信息、技能规范过时、历史上下文出错和工具说明漂移都可能沿轨迹传播。AgentPerturb 交叉组织四个目标——用户请求、过程规范、继承上下文、工具契约 ——与缺失、冗余、错误三类扰动，得到12个家族。每对只改一个目标，其余三个、后端和成功 oracle 不变。原文 §3、附录 F 候选不能因为“JSON合法”就入选：与生成器独立的语义 verifier 必须确认单目标、目标不变、仍可求解、可执行四项全部通过，再结合原生 validator。 原文完整配置为10个前沿模型×2真实环境×25任务×12类扰动，单任务可达200轮、约30分钟上限，还需生成/语义验证 API，成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现扰动边界、独立验证与配对记录，不生成官方任务，不声称语法检查能够证明语义保持。每 seed 在无外部副作用的算术/工具契约 fixture 上实际执行全部12家族，actor 只解析公开输入，grader 单独判分。独立的领域 verifier 拒绝改变真实目标的编辑；语法-only负对照会错误放行这些编辑。  公共评测与协议 交互输入扰动与稳健性 Agent 评测与可靠性：如何知道真的做对了 计算 AgentPerturb 成对下降时，可以删掉没有评分的请求吗？ 已评分配对子集可计算C、P和Delta，但必须另报全部请求分母上的覆盖率和未知上下界。缺失记录仍属未知，原生部分奖励也不能为凑统一口径擅自二值化。 示意：计划100对仅60对有双侧评分，不能只报这60对的下降而隐去40对缺失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1a5927032c165b95">计算 AgentPerturb 成对下降时，可以删掉没有评分的请求吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagent-perturb">AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The Hong Kong University of Science and Technology (Guangzhou)</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>已评分配对子集可计算C、P和Delta，但必须另报全部请求分母上的覆盖率和未知上下界。缺失记录仍属未知，原生部分奖励也不能为凑统一口径擅自二值化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>计划100对仅60对有双侧评分，不能只报这60对的下降而隐去40对缺失。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21624">原论文</a> · <a href="../../../../agent-research/2610.21624-agent-perturb/">实现解读</a> · <a href="#qa-1a5927032c165b95">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:disagreement-routing" data-paper-title="Disagreement-Guided Weak-to-Strong Routing" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Disagreement-Guided Weak-to-Strong Routing Agent University of Pennsylvania 2026-10-15 “弱模型可能答错”不等于“强模型能补救”。原文用弱强分歧减去强模型自身分歧，估计升级调用的增益。离线只需对模型回答/动作做等价性比较，不需要判断哪个回答正确；测试时仅运行弱模型的表示和两个轻量 probe，路由决定升级时才查询强模型。原图出处：原论文 Figure 1。 完整 8B 弱模型、多个强模型、每步 K=10、WebShop 数千任务和多预算长 rollout 在单 A100/A30/Mac 下成本过高，成本过高，不复现（审查 DONE）。component_only / CPU 诊断：实现论文目标估计、两个真实拟合的 probe 和 validation 阈值合同。合成表示不是 LLM hidden state，不把机制检查写成 BFCL/WebShop 能力提升；不进入 Evolve。每 seed 生成 128 个独立合成 prompt-vector，80 train / 24 validation / 24 test；每 prompt 两个弱响应、12 个强响应采样。  专家模型编排 Agent 评测与可靠性：如何知道真的做对了 弱模型不确定，为什么不等于应当升级强模型？ 若强模型在同一问题上也高度分歧，升级可能并无稳定收益。方法用弱强分歧减去强模型自身分歧，学习升级价值；离线比较回答等价性，不需要正确答案标签。 示意：两个模型都在多个选项间摇摆，弱模型犹豫本身不足以证明强模型能补救。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-disagreement-routing-3ad2d018" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9fda6925705b314c">弱模型不确定，为什么不等于应当升级强模型？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adisagreement-routing">Disagreement-Guided Weak-to-Strong Routing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若强模型在同一问题上也高度分歧，升级可能并无稳定收益。方法用弱强分歧减去强模型自身分歧，学习升级价值；离线比较回答等价性，不需要正确答案标签。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个模型都在多个选项间摇摆，弱模型犹豫本身不足以证明强模型能补救。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22245">原论文</a> · <a href="../../../../agent-research/2610.22245-disagreement-routing/">实现解读</a> · <a href="#qa-9fda6925705b314c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:disagreement-routing" data-paper-title="Disagreement-Guided Weak-to-Strong Routing" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Disagreement-Guided Weak-to-Strong Routing Agent University of Pennsylvania 2026-10-15 “弱模型可能答错”不等于“强模型能补救”。原文用弱强分歧减去强模型自身分歧，估计升级调用的增益。离线只需对模型回答/动作做等价性比较，不需要判断哪个回答正确；测试时仅运行弱模型的表示和两个轻量 probe，路由决定升级时才查询强模型。原图出处：原论文 Figure 1。 完整 8B 弱模型、多个强模型、每步 K=10、WebShop 数千任务和多预算长 rollout 在单 A100/A30/Mac 下成本过高，成本过高，不复现（审查 DONE）。component_only / CPU 诊断：实现论文目标估计、两个真实拟合的 probe 和 validation 阈值合同。合成表示不是 LLM hidden state，不把机制检查写成 BFCL/WebShop 能力提升；不进入 Evolve。每 seed 生成 128 个独立合成 prompt-vector，80 train / 24 validation / 24 test；每 prompt 两个弱响应、12 个强响应采样。  专家模型编排 Agent 评测与可靠性：如何知道真的做对了 为什么要从弱强分歧里减去强模型自身分歧？ 弱强不同可能因为强模型也不稳定，而非升级能纠正弱模型。用不同采样索引估计强模型自分歧，扣除这部分后更接近调用增益线索；分数可为负，并非成功概率，测试时应只跑弱表示与 probe，决定升级后才付强模型调用成本。 例如强模型自己两次答案都相反，弱强分歧很高不一定值得升级；若强模型内部一致而与弱模型不同，信号才更明确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-15d5ca65c5b0168c">为什么要从弱强分歧里减去强模型自身分歧？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adisagreement-routing">Disagreement-Guided Weak-to-Strong Routing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>弱强不同可能因为强模型也不稳定，而非升级能纠正弱模型。用不同采样索引估计强模型自分歧，扣除这部分后更接近调用增益线索；分数可为负，并非成功概率，测试时应只跑弱表示与 probe，决定升级后才付强模型调用成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如强模型自己两次答案都相反，弱强分歧很高不一定值得升级；若强模型内部一致而与弱模型不同，信号才更明确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22245">原论文</a> · <a href="../../../../agent-research/2610.22245-disagreement-routing/">实现解读</a> · <a href="#qa-15d5ca65c5b0168c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:disagreement-routing" data-paper-title="Disagreement-Guided Weak-to-Strong Routing" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Disagreement-Guided Weak-to-Strong Routing Agent University of Pennsylvania 2026-10-15 “弱模型可能答错”不等于“强模型能补救”。原文用弱强分歧减去强模型自身分歧，估计升级调用的增益。离线只需对模型回答/动作做等价性比较，不需要判断哪个回答正确；测试时仅运行弱模型的表示和两个轻量 probe，路由决定升级时才查询强模型。原图出处：原论文 Figure 1。 完整 8B 弱模型、多个强模型、每步 K=10、WebShop 数千任务和多预算长 rollout 在单 A100/A30/Mac 下成本过高，成本过高，不复现（审查 DONE）。component_only / CPU 诊断：实现论文目标估计、两个真实拟合的 probe 和 validation 阈值合同。合成表示不是 LLM hidden state，不把机制检查写成 BFCL/WebShop 能力提升；不进入 Evolve。每 seed 生成 128 个独立合成 prompt-vector，80 train / 24 validation / 24 test；每 prompt 两个弱响应、12 个强响应采样。  专家模型编排 Agent 评测与可靠性：如何知道真的做对了 校正路由分数与弱强模型的原始分歧概率，有什么值域差异？ 原始分歧目标是概率，校正分数是两个probe输出之差，可以为负，不能截到[0,1]。多个弱响应先取response分歧预测的最小值，再减prompt层面的强模型自身分歧。 示意：弱强分歧0.2、强模型自身分歧0.5时，校正值可为−0.3。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0f7410df12418bd1">校正路由分数与弱强模型的原始分歧概率，有什么值域差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adisagreement-routing">Disagreement-Guided Weak-to-Strong Routing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始分歧目标是概率，校正分数是两个probe输出之差，可以为负，不能截到[0,1]。多个弱响应先取response分歧预测的最小值，再减prompt层面的强模型自身分歧。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>弱强分歧0.2、强模型自身分歧0.5时，校正值可为−0.3。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22245">原论文</a> · <a href="../../../../agent-research/2610.22245-disagreement-routing/">实现解读</a> · <a href="#qa-0f7410df12418bd1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:disagreement-routing" data-paper-title="Disagreement-Guided Weak-to-Strong Routing" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Disagreement-Guided Weak-to-Strong Routing Agent University of Pennsylvania 2026-10-15 “弱模型可能答错”不等于“强模型能补救”。原文用弱强分歧减去强模型自身分歧，估计升级调用的增益。离线只需对模型回答/动作做等价性比较，不需要判断哪个回答正确；测试时仅运行弱模型的表示和两个轻量 probe，路由决定升级时才查询强模型。原图出处：原论文 Figure 1。 完整 8B 弱模型、多个强模型、每步 K=10、WebShop 数千任务和多预算长 rollout 在单 A100/A30/Mac 下成本过高，成本过高，不复现（审查 DONE）。component_only / CPU 诊断：实现论文目标估计、两个真实拟合的 probe 和 validation 阈值合同。合成表示不是 LLM hidden state，不把机制检查写成 BFCL/WebShop 能力提升；不进入 Evolve。每 seed 生成 128 个独立合成 prompt-vector，80 train / 24 validation / 24 test；每 prompt 两个弱响应、12 个强响应采样。  专家模型编排 Agent 评测与可靠性：如何知道真的做对了 估计强模型自身分歧时，为什么必须排除同一采样与自身的配对？ 应使用K_s(K_s−1)个不同索引有序配对；对角self-pair必然一致，会压低分歧估计。推理阈值只从validation校准，测试分布变化时不承诺精确路由配额。 示意：两个强响应只有两个交叉有序对，不能把两个自配对也放入分母。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-53c4ea46a8f59ec0">估计强模型自身分歧时，为什么必须排除同一采样与自身的配对？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adisagreement-routing">Disagreement-Guided Weak-to-Strong Routing</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Pennsylvania</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>应使用K_s(K_s−1)个不同索引有序配对；对角self-pair必然一致，会压低分歧估计。推理阈值只从validation校准，测试分布变化时不承诺精确路由配额。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个强响应只有两个交叉有序对，不能把两个自配对也放入分母。</p>
<p class="ar-learning-sources">依据：核心公式、代码映射与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22245">原论文</a> · <a href="../../../../agent-research/2610.22245-disagreement-routing/">实现解读</a> · <a href="#qa-53c4ea46a8f59ec0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gacc-bench" data-paper-title="GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models Agent Fudan University 2026-10-15 长期上下文压缩常在具体后续问题尚未知时执行，但用户可能已给出高层目标。GACC-Bench 按 context–goal 组织多道后续问题，压缩器只能看到来源、目标和预算；固定 reader 用同一压缩记忆逐题回答，再由固定 judge 对照原文和参考答案评分，检验是否保全整组目标证据。 其长来源、多问题和多模型调用总成本高，成本过高，不复现（审查 DONE）；evaluation_protocol_interface / L1 CPU 合同诊断。接口可接真实 compressor、reader、judge 和 tokenizer；本轮仅固定 token-ID/规则 fixture，没有运行官方数据或 LLM，不声称实现了新的压缩模型。每 seed 初始化两段小字符串来源、四个目标、12 个问题。规则 compressor 只挑目标所在行，规则 reader 只解析已保留字段，fixture judge 做精确比较；这三者不是 LLM。  公共评测与协议 上下文压缩 Agent 评测与可靠性：如何知道真的做对了 GACC-Bench 为什么让一份压缩记忆回答同一目标下的多道问题？ 压缩时具体后续问题未知，只有高层目标可见；共用一次记忆才能检验整组目标证据是否保留。若每看一道题就重新压缩，就变成面向已知问题的信息提取。 示意：为出差目标压缩资料后，应同时能回答交通和住宿问题，而不是每题重做摘要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-gacc-bench-1c3f337b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9a0c53ebe99d3d58">GACC-Bench 为什么让一份压缩记忆回答同一目标下的多道问题？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agacc-bench">GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>压缩时具体后续问题未知，只有高层目标可见；共用一次记忆才能检验整组目标证据是否保留。若每看一道题就重新压缩，就变成面向已知问题的信息提取。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>为出差目标压缩资料后，应同时能回答交通和住宿问题，而不是每题重做摘要。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21893">原论文</a> · <a href="../../../../agent-research/2610.21893-gacc-bench/">实现解读</a> · <a href="#qa-9a0c53ebe99d3d58">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gacc-bench" data-paper-title="GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models Agent Fudan University 2026-10-15 长期上下文压缩常在具体后续问题尚未知时执行，但用户可能已给出高层目标。GACC-Bench 按 context–goal 组织多道后续问题，压缩器只能看到来源、目标和预算；固定 reader 用同一压缩记忆逐题回答，再由固定 judge 对照原文和参考答案评分，检验是否保全整组目标证据。 其长来源、多问题和多模型调用总成本高，成本过高，不复现（审查 DONE）；evaluation_protocol_interface / L1 CPU 合同诊断。接口可接真实 compressor、reader、judge 和 tokenizer；本轮仅固定 token-ID/规则 fixture，没有运行官方数据或 LLM，不声称实现了新的压缩模型。每 seed 初始化两段小字符串来源、四个目标、12 个问题。规则 compressor 只挑目标所在行，规则 reader 只解析已保留字段，fixture judge 做精确比较；这三者不是 LLM。  公共评测与协议 上下文压缩 Agent 评测与可靠性：如何知道真的做对了 同一 context–goal–budget 为什么只生成一次记忆供所有后续问题复用？ 压缩时只知高层目标，不知具体问题，复用能检验一份记忆是否保全整组所需证据。若逐题重压缩，压缩器已获得额外查询信息，任务就变了；严格 token 截断、零预算空记忆与不补 padding 也决定 reader 的真实输入，不能只报名义预算。 例如目标是了解一次项目决策，后续分别问日期和原因，应读同一份预先压缩记忆，而非每题再偷取原文做定向摘要。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2f9e0b46e42d85cd">同一 context–goal–budget 为什么只生成一次记忆供所有后续问题复用？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agacc-bench">GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>压缩时只知高层目标，不知具体问题，复用能检验一份记忆是否保全整组所需证据。若逐题重压缩，压缩器已获得额外查询信息，任务就变了；严格 token 截断、零预算空记忆与不补 padding 也决定 reader 的真实输入，不能只报名义预算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如目标是了解一次项目决策，后续分别问日期和原因，应读同一份预先压缩记忆，而非每题再偷取原文做定向摘要。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21893">原论文</a> · <a href="../../../../agent-research/2610.21893-gacc-bench/">实现解读</a> · <a href="#qa-2f9e0b46e42d85cd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gacc-bench" data-paper-title="GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models Agent Fudan University 2026-10-15 长期上下文压缩常在具体后续问题尚未知时执行，但用户可能已给出高层目标。GACC-Bench 按 context–goal 组织多道后续问题，压缩器只能看到来源、目标和预算；固定 reader 用同一压缩记忆逐题回答，再由固定 judge 对照原文和参考答案评分，检验是否保全整组目标证据。 其长来源、多问题和多模型调用总成本高，成本过高，不复现（审查 DONE）；evaluation_protocol_interface / L1 CPU 合同诊断。接口可接真实 compressor、reader、judge 和 tokenizer；本轮仅固定 token-ID/规则 fixture，没有运行官方数据或 LLM，不声称实现了新的压缩模型。每 seed 初始化两段小字符串来源、四个目标、12 个问题。规则 compressor 只挑目标所在行，规则 reader 只解析已保留字段，fixture judge 做精确比较；这三者不是 LLM。  公共评测与协议 上下文压缩 Agent 评测与可靠性：如何知道真的做对了 GACC 的 Micro 高而 Macro 为零，可能是什么情况？ Micro按全部问题统计正确比例，Macro要求一个目标下所有问题都正确才计1。每组都漏一道关键题时，逐题正确率仍可较高，整目标完整率却为0；两者不能互换。 示意：两个目标各3题都答对2题，Micro是2/3，Macro仍为0。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-12efa2fcece6bb35">GACC 的 Micro 高而 Macro 为零，可能是什么情况？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agacc-bench">GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Micro按全部问题统计正确比例，Macro要求一个目标下所有问题都正确才计1。每组都漏一道关键题时，逐题正确率仍可较高，整目标完整率却为0；两者不能互换。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个目标各3题都答对2题，Micro是2/3，Macro仍为0。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21893">原论文</a> · <a href="../../../../agent-research/2610.21893-gacc-bench/">实现解读</a> · <a href="#qa-12efa2fcece6bb35">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gacc-bench" data-paper-title="GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models Agent Fudan University 2026-10-15 长期上下文压缩常在具体后续问题尚未知时执行，但用户可能已给出高层目标。GACC-Bench 按 context–goal 组织多道后续问题，压缩器只能看到来源、目标和预算；固定 reader 用同一压缩记忆逐题回答，再由固定 judge 对照原文和参考答案评分，检验是否保全整组目标证据。 其长来源、多问题和多模型调用总成本高，成本过高，不复现（审查 DONE）；evaluation_protocol_interface / L1 CPU 合同诊断。接口可接真实 compressor、reader、judge 和 tokenizer；本轮仅固定 token-ID/规则 fixture，没有运行官方数据或 LLM，不声称实现了新的压缩模型。每 seed 初始化两段小字符串来源、四个目标、12 个问题。规则 compressor 只挑目标所在行，规则 reader 只解析已保留字段，fixture judge 做精确比较；这三者不是 LLM。  公共评测与协议 上下文压缩 Agent 评测与可靠性：如何知道真的做对了 GACC 压缩输出超预算或预算向下取整为零时，应怎样给 reader 输入？ 按固定tokenizer将输出取前L个token再decode；不重生成、不补齐，L为0就传空memory。缓存还要绑定来源、目标、tokenizer及compressor版本，避免跨配置误用记忆。 示意：来源仅3token、保留率0.2时L=0，不能擅自保留1token改善得分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ce582aebb12bcffd">GACC 压缩输出超预算或预算向下取整为零时，应怎样给 reader 输入？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agacc-bench">GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Fudan University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>按固定tokenizer将输出取前L个token再decode；不重生成、不补齐，L为0就传空memory。缓存还要绑定来源、目标、tokenizer及compressor版本，避免跨配置误用记忆。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>来源仅3token、保留率0.2时L=0，不能擅自保留1token改善得分。</p>
<p class="ar-learning-sources">依据：核心公式、代码映射、成本与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21893">原论文</a> · <a href="../../../../agent-research/2610.21893-gacc-bench/">实现解读</a> · <a href="#qa-ce582aebb12bcffd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-decomposition" data-paper-title="Harness-Delta Attribution: Dissecting Gains From Harness Evolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Harness-Delta Attribution: Dissecting Gains From Harness Evolution Agent Amazon 2026-10-15 同一个冻结模型的 Harness 可以靠更多推理算力，也可以靠基准捷径涨分。甚至 held-out 数据也可能共享相同捷径。HDA 先对 baseline/evolved 的逐样本差做双侧 paired bootstrap；收益不显著时停止归因。显著时，构造算力匹配 baseline 与移除已检测捷径的 evolved，且两种控制的构造都需要任务相关人审。方法 §3 原图建议：原论文 Figure 2，PDF 第3页，四臂及三类差值关系。 原文25配置跨模型/演化框架/任务，含 SWE-bench 容器与多轮昂贵重评估，完整矩阵成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现归因算子和控制接纳，不自动证明 Harness 可泛化。接口要求四臂 item ID 顺序完全一致、逐样本有限分数、Harness SHA256 和同单位平均推理成本；控制必须携带人审者与依据。CPU 内核实际重采样10,000次，计算区间、双侧 p 值、原始差值、展示份额及数值恒等式误差。算力匹配容差是本地显式参数，不是假定原论文常数。没有人审、错配样本、错配预算一律拒绝；零增益/噪声对照不归因。  公共评测与协议 Harness进化归因与过拟合审计 Agent 评测与可靠性：如何知道真的做对了 HDA 为什么先检验 evolved 相对 baseline 的配对收益？ 如果观测增益可能只是噪声，继续分解算力、捷径和剩余项没有可靠起点。方法先做双侧paired bootstrap，显著后才构造算力匹配与捷径中和控制；两个控制均需任务相关人审。 示意：同一组任务两次波动了少量分数，不能直接宣布其中多少来自泛化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-harness-decomposition-8f77338c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ee85cdcc7ef9364a">HDA 为什么先检验 evolved 相对 baseline 的配对收益？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-decomposition">Harness-Delta Attribution: Dissecting Gains From Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amazon</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>如果观测增益可能只是噪声，继续分解算力、捷径和剩余项没有可靠起点。方法先做双侧paired bootstrap，显著后才构造算力匹配与捷径中和控制；两个控制均需任务相关人审。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一组任务两次波动了少量分数，不能直接宣布其中多少来自泛化。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22466">原论文</a> · <a href="../../../../agent-research/2610.22466-harness-decomposition/">实现解读</a> · <a href="#qa-ee85cdcc7ef9364a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-decomposition" data-paper-title="Harness-Delta Attribution: Dissecting Gains From Harness Evolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Harness-Delta Attribution: Dissecting Gains From Harness Evolution Agent Amazon 2026-10-15 同一个冻结模型的 Harness 可以靠更多推理算力，也可以靠基准捷径涨分。甚至 held-out 数据也可能共享相同捷径。HDA 先对 baseline/evolved 的逐样本差做双侧 paired bootstrap；收益不显著时停止归因。显著时，构造算力匹配 baseline 与移除已检测捷径的 evolved，且两种控制的构造都需要任务相关人审。方法 §3 原图建议：原论文 Figure 2，PDF 第3页，四臂及三类差值关系。 原文25配置跨模型/演化框架/任务，含 SWE-bench 容器与多轮昂贵重评估，完整矩阵成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现归因算子和控制接纳，不自动证明 Harness 可泛化。接口要求四臂 item ID 顺序完全一致、逐样本有限分数、Harness SHA256 和同单位平均推理成本；控制必须携带人审者与依据。CPU 内核实际重采样10,000次，计算区间、双侧 p 值、原始差值、展示份额及数值恒等式误差。算力匹配容差是本地显式参数，不是假定原论文常数。没有人审、错配样本、错配预算一律拒绝；零增益/噪声对照不归因。  公共评测与协议 Harness进化归因与过拟合审计 Agent 评测与可靠性：如何知道真的做对了 HDA 的残余 G 为什么只能视作泛化改进上界，而不是直接的迁移证据？ 算力匹配减掉额外计算，已检测捷径中和再剥离一部分过拟合，但未发现捷径仍可能留在残余里。控制构造需要任务相关人审，且先确认原收益显著才归因；代数分解保证账目一致，不保证每项已被完整因果识别或适用于新分布。 例如去掉已知文件名捷径后仍涨分，也可能还利用隐藏目录顺序；不能把剩下全部提升都宣称是真正通用推理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c188a5254d4945dd">HDA 的残余 G 为什么只能视作泛化改进上界，而不是直接的迁移证据？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-decomposition">Harness-Delta Attribution: Dissecting Gains From Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amazon</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>算力匹配减掉额外计算，已检测捷径中和再剥离一部分过拟合，但未发现捷径仍可能留在残余里。控制构造需要任务相关人审，且先确认原收益显著才归因；代数分解保证账目一致，不保证每项已被完整因果识别或适用于新分布。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如去掉已知文件名捷径后仍涨分，也可能还利用隐藏目录顺序；不能把剩下全部提升都宣称是真正通用推理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22466">原论文</a> · <a href="../../../../agent-research/2610.22466-harness-decomposition/">实现解读</a> · <a href="#qa-c188a5254d4945dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-decomposition" data-paper-title="Harness-Delta Attribution: Dissecting Gains From Harness Evolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Harness-Delta Attribution: Dissecting Gains From Harness Evolution Agent Amazon 2026-10-15 同一个冻结模型的 Harness 可以靠更多推理算力，也可以靠基准捷径涨分。甚至 held-out 数据也可能共享相同捷径。HDA 先对 baseline/evolved 的逐样本差做双侧 paired bootstrap；收益不显著时停止归因。显著时，构造算力匹配 baseline 与移除已检测捷径的 evolved，且两种控制的构造都需要任务相关人审。方法 §3 原图建议：原论文 Figure 2，PDF 第3页，四臂及三类差值关系。 原文25配置跨模型/演化框架/任务，含 SWE-bench 容器与多轮昂贵重评估，完整矩阵成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现归因算子和控制接纳，不自动证明 Harness 可泛化。接口要求四臂 item ID 顺序完全一致、逐样本有限分数、Harness SHA256 和同单位平均推理成本；控制必须携带人审者与依据。CPU 内核实际重采样10,000次，计算区间、双侧 p 值、原始差值、展示份额及数值恒等式误差。算力匹配容差是本地显式参数，不是假定原论文常数。没有人审、错配样本、错配预算一律拒绝；零增益/噪声对照不归因。  公共评测与协议 Harness进化归因与过拟合审计 Agent 评测与可靠性：如何知道真的做对了 HDA 中的剩余 G，为什么不能直接叫作已证明的泛化收益？ G是中和已发现捷径后相对算力匹配baseline的差值，还可能含未识别捷径；因此只是泛化改进上界。O也只覆盖检测且能中和的机制，属于过拟合下界估计。 示意：移除一种答案泄漏后仍有收益，并不能排除另一个尚未检查的捷径。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6815b896a61e9666">HDA 中的剩余 G，为什么不能直接叫作已证明的泛化收益？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-decomposition">Harness-Delta Attribution: Dissecting Gains From Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amazon</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>G是中和已发现捷径后相对算力匹配baseline的差值，还可能含未识别捷径；因此只是泛化改进上界。O也只覆盖检测且能中和的机制，属于过拟合下界估计。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>移除一种答案泄漏后仍有收益，并不能排除另一个尚未检查的捷径。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22466">原论文</a> · <a href="../../../../agent-research/2610.22466-harness-decomposition/">实现解读</a> · <a href="#qa-6815b896a61e9666">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-decomposition" data-paper-title="Harness-Delta Attribution: Dissecting Gains From Harness Evolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Harness-Delta Attribution: Dissecting Gains From Harness Evolution Agent Amazon 2026-10-15 同一个冻结模型的 Harness 可以靠更多推理算力，也可以靠基准捷径涨分。甚至 held-out 数据也可能共享相同捷径。HDA 先对 baseline/evolved 的逐样本差做双侧 paired bootstrap；收益不显著时停止归因。显著时，构造算力匹配 baseline 与移除已检测捷径的 evolved，且两种控制的构造都需要任务相关人审。方法 §3 原图建议：原论文 Figure 2，PDF 第3页，四臂及三类差值关系。 原文25配置跨模型/演化框架/任务，含 SWE-bench 容器与多轮昂贵重评估，完整矩阵成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现归因算子和控制接纳，不自动证明 Harness 可泛化。接口要求四臂 item ID 顺序完全一致、逐样本有限分数、Harness SHA256 和同单位平均推理成本；控制必须携带人审者与依据。CPU 内核实际重采样10,000次，计算区间、双侧 p 值、原始差值、展示份额及数值恒等式误差。算力匹配容差是本地显式参数，不是假定原论文常数。没有人审、错配样本、错配预算一律拒绝；零增益/噪声对照不归因。  公共评测与协议 Harness进化归因与过拟合审计 Agent 评测与可靠性：如何知道真的做对了 HDA 展示百分比前，能把负的原始 T、O 或 G 截成零吗？ 原始带符号差值必须保留并满足Delta=T+O+G。展示份额另按规则截断，不能回写原始归因；四臂还必须逐item对齐、成本单位一致并提供人审控制依据。 示意：中和某机制反而涨分时，负O是应保存的结果，不应为了饼图好看改成0。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-375a2b1209b0dd6d">HDA 展示百分比前，能把负的原始 T、O 或 G 截成零吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-decomposition">Harness-Delta Attribution: Dissecting Gains From Harness Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Amazon</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始带符号差值必须保留并满足Delta=T+O+G。展示份额另按规则截断，不能回写原始归因；四臂还必须逐item对齐、成本单位一致并提供人审控制依据。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>中和某机制反而涨分时，负O是应保存的结果，不应为了饼图好看改成0。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现与边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22466">原论文</a> · <a href="../../../../agent-research/2610.22466-harness-decomposition/">实现解读</a> · <a href="#qa-375a2b1209b0dd6d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:librarian-agents" data-paper-title="Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries Agent Stanford University 2026-10-15 常规 RAG 每次查询后才检索，重复探索跨文档关系。Librarian 在还未看到评测问题时，由可学习 builder 把原始语料组织成可复用层级文件系统；固定 answerer 后续导航，必要时沿 provenance 回退到 raw docs。CreateFile、MergeFiles、Delete、Stop 形成有限 horizon MDP，Delete 永远不能删原文。 单 A100/A30 或本地 Mac、零 API/训练预算下，成本过高，不复现（审查 DONE）。adapter: null，仅诊断，不允许 Evolve 晋级。本地为 evaluation_protocol_interface：真实文件系统/provenance 合同与官方 compact score records 的 CPU 复算。没有训练 RL builder，没有以静态摘要替代论文核心模型；adapter: null，仅诊断，不允许 Evolve 晋级。官方 revision 455ac88c81c639c10a8404464dabf71a7fbb563e；  公共评测与协议 层级记忆与预见式工作区 Agent 评测与可靠性：如何知道真的做对了 Librarian 为什么在不知道具体后续问题时先整理工作区？ 同一语料会被多次查询，提前建立层级文件与原文来源可复用跨文档整理成本。builder只能看语料，后续由固定answerer导航，不能依据测试问题预先写入答案。 示意：先整理一个项目的资料目录，再回答多位用户的问题，而非看到题目才为它定制目录。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-librarian-agents-828f2c36" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a670d1d22123a010">Librarian 为什么在不知道具体后续问题时先整理工作区？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alibrarian-agents">Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一语料会被多次查询，提前建立层级文件与原文来源可复用跨文档整理成本。builder只能看语料，后续由固定answerer导航，不能依据测试问题预先写入答案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先整理一个项目的资料目录，再回答多位用户的问题，而非看到题目才为它定制目录。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22273">原论文</a> · <a href="../../../../agent-research/2610.22273-librarian-agents/">实现解读</a> · <a href="#qa-a670d1d22123a010">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:librarian-agents" data-paper-title="Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries Agent Stanford University 2026-10-15 常规 RAG 每次查询后才检索，重复探索跨文档关系。Librarian 在还未看到评测问题时，由可学习 builder 把原始语料组织成可复用层级文件系统；固定 answerer 后续导航，必要时沿 provenance 回退到 raw docs。CreateFile、MergeFiles、Delete、Stop 形成有限 horizon MDP，Delete 永远不能删原文。 单 A100/A30 或本地 Mac、零 API/训练预算下，成本过高，不复现（审查 DONE）。adapter: null，仅诊断，不允许 Evolve 晋级。本地为 evaluation_protocol_interface：真实文件系统/provenance 合同与官方 compact score records 的 CPU 复算。没有训练 RL builder，没有以静态摘要替代论文核心模型；adapter: null，仅诊断，不允许 Evolve 晋级。官方 revision 455ac88c81c639c10a8404464dabf71a7fbb563e；  公共评测与协议 层级记忆与预见式工作区 Agent 评测与可靠性：如何知道真的做对了 builder 尚未看到评测问题，为什么不能按已知问题把层级文件系统专门整理成答案索引？ 目标是预先组织可复用工作区，固定 answerer 后续面对未知查询导航。提前看题会把整理变成针对答案的检索捷径，失去跨问题价值；来源回退还要保留原文，Delete 不得删除原始语料，一般成本公式也不能冒称主训练实际用了非零成本 shaping。 例如先按公司和日期整理资料可供多种问题使用；若提前知道要问某数字并只把它写在首页，评测就不再检验通用整理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3498243647684558">builder 尚未看到评测问题，为什么不能按已知问题把层级文件系统专门整理成答案索引？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alibrarian-agents">Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是预先组织可复用工作区，固定 answerer 后续面对未知查询导航。提前看题会把整理变成针对答案的检索捷径，失去跨问题价值；来源回退还要保留原文，Delete 不得删除原始语料，一般成本公式也不能冒称主训练实际用了非零成本 shaping。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先按公司和日期整理资料可供多种问题使用；若提前知道要问某数字并只把它写在首页，评测就不再检验通用整理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22273">原论文</a> · <a href="../../../../agent-research/2610.22273-librarian-agents/">实现解读</a> · <a href="#qa-3498243647684558">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:librarian-agents" data-paper-title="Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries Agent Stanford University 2026-10-15 常规 RAG 每次查询后才检索，重复探索跨文档关系。Librarian 在还未看到评测问题时，由可学习 builder 把原始语料组织成可复用层级文件系统；固定 answerer 后续导航，必要时沿 provenance 回退到 raw docs。CreateFile、MergeFiles、Delete、Stop 形成有限 horizon MDP，Delete 永远不能删原文。 单 A100/A30 或本地 Mac、零 API/训练预算下，成本过高，不复现（审查 DONE）。adapter: null，仅诊断，不允许 Evolve 晋级。本地为 evaluation_protocol_interface：真实文件系统/provenance 合同与官方 compact score records 的 CPU 复算。没有训练 RL builder，没有以静态摘要替代论文核心模型；adapter: null，仅诊断，不允许 Evolve 晋级。官方 revision 455ac88c81c639c10a8404464dabf71a7fbb563e；  公共评测与协议 层级记忆与预见式工作区 Agent 评测与可靠性：如何知道真的做对了 Librarian 的一般成本效用，与论文主训练实际奖励相同吗？ 不同。一般式包含构建、token和读取惩罚，但主训练这些成本系数实际为0、gamma为1，并每8个builder turns探测answerability变化及终止正确性。不能把可定义的成本项写成已用的训练shaping。 示意：公式里出现token成本，不代表该次训练因多读一个文件就被扣分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-7e1a1b0a38505cf3">Librarian 的一般成本效用，与论文主训练实际奖励相同吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alibrarian-agents">Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不同。一般式包含构建、token和读取惩罚，但主训练这些成本系数实际为0、gamma为1，并每8个builder turns探测answerability变化及终止正确性。不能把可定义的成本项写成已用的训练shaping。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>公式里出现token成本，不代表该次训练因多读一个文件就被扣分。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22273">原论文</a> · <a href="../../../../agent-research/2610.22273-librarian-agents/">实现解读</a> · <a href="#qa-7e1a1b0a38505cf3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:librarian-agents" data-paper-title="Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries Agent Stanford University 2026-10-15 常规 RAG 每次查询后才检索，重复探索跨文档关系。Librarian 在还未看到评测问题时，由可学习 builder 把原始语料组织成可复用层级文件系统；固定 answerer 后续导航，必要时沿 provenance 回退到 raw docs。CreateFile、MergeFiles、Delete、Stop 形成有限 horizon MDP，Delete 永远不能删原文。 单 A100/A30 或本地 Mac、零 API/训练预算下，成本过高，不复现（审查 DONE）。adapter: null，仅诊断，不允许 Evolve 晋级。本地为 evaluation_protocol_interface：真实文件系统/provenance 合同与官方 compact score records 的 CPU 复算。没有训练 RL builder，没有以静态摘要替代论文核心模型；adapter: null，仅诊断，不允许 Evolve 晋级。官方 revision 455ac88c81c639c10a8404464dabf71a7fbb563e；  公共评测与协议 层级记忆与预见式工作区 Agent 评测与可靠性：如何知道真的做对了 Librarian 删除一个合成节点后，怎样保留原文可追溯性？ Delete只归档合成节点，保留raw docs和历史来源，并提升子节点；cold load还需验证hash、层级和磁盘内容。本地落实文件系统合同与冻结结果复算，没有训练learned builder。 示意：删掉一个摘要目录，原始文件及被合并子目录的来源仍应可以找到。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-58d87f3603156920">Librarian 删除一个合成节点后，怎样保留原文可追溯性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alibrarian-agents">Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Stanford University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Delete只归档合成节点，保留raw docs和历史来源，并提升子节点；cold load还需验证hash、层级和磁盘内容。本地落实文件系统合同与冻结结果复算，没有训练learned builder。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>删掉一个摘要目录，原始文件及被合并子目录的来源仍应可以找到。</p>
<p class="ar-learning-sources">依据：文件系统合同与代码映射；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22273">原论文</a> · <a href="../../../../agent-research/2610.22273-librarian-agents/">实现解读</a> · <a href="#qa-58d87f3603156920">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:probe" data-paper-title="PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents Agent Mohamed bin Zayed University of Artificial Intelligence 2026-10-15 任务完成并不等于按业务/隐私政策完成；只测试最终状态或有害文本也可能漏掉多轮工具调用中的违规。PROBE 训练扮演正常客户的 auditor，与冻结 target 交互，私有 verifier 从完整 trace 判断违规；奖励综合违规、可信客户行为、工具流程进展和策略多样性，比较 GRPO、DPO 和 GFlowNet。 成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。只实现惰性 trace/verifier/reward 接口和四个独立规则示例；没有训练审计模型，也没有接入完整 SkyAssist 或真实目标服务。每 seed 构造 12 条惰性 trace，随机化重复轮数，不执行任何工具。四个示例核验 required fields、当前 mutation intent 的确认、限制目的地及人数；它们不是原文完整 20 策略套件。第五个明确 unsupported 的语义策略留在 coverage 分母。  公共评测与协议 Agent RL Agent 评测与可靠性：如何知道真的做对了 PROBE 为什么把任务完成与遵守业务政策分开审计？ 最终状态或有害文本检查可能漏掉多轮工具流程中的违规。auditor与冻结target交互，私有verifier从完整trace检查政策，观察可信客户行为、流程进展与覆盖，而非只看回答语气。 示意：任务结果看似完成，过程中仍可能缺少规定确认或出现未请求状态变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-probe-e4f99af8" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-97c88a4c09786eec">PROBE 为什么把任务完成与遵守业务政策分开审计？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprobe">PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终状态或有害文本检查可能漏掉多轮工具流程中的违规。auditor与冻结target交互，私有verifier从完整trace检查政策，观察可信客户行为、流程进展与覆盖，而非只看回答语气。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>任务结果看似完成，过程中仍可能缺少规定确认或出现未请求状态变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22124">原论文</a> · <a href="../../../../agent-research/2610.22124-probe/">实现解读</a> · <a href="#qa-97c88a4c09786eec">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:probe" data-paper-title="PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents Agent Mohamed bin Zayed University of Artificial Intelligence 2026-10-15 任务完成并不等于按业务/隐私政策完成；只测试最终状态或有害文本也可能漏掉多轮工具调用中的违规。PROBE 训练扮演正常客户的 auditor，与冻结 target 交互，私有 verifier 从完整 trace 判断违规；奖励综合违规、可信客户行为、工具流程进展和策略多样性，比较 GRPO、DPO 和 GFlowNet。 成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。只实现惰性 trace/verifier/reward 接口和四个独立规则示例；没有训练审计模型，也没有接入完整 SkyAssist 或真实目标服务。每 seed 构造 12 条惰性 trace，随机化重复轮数，不执行任何工具。四个示例核验 required fields、当前 mutation intent 的确认、限制目的地及人数；它们不是原文完整 20 策略套件。第五个明确 unsupported 的语义策略留在 coverage 分母。  公共评测与协议 Agent RL Agent 评测与可靠性：如何知道真的做对了 为什么违规奖励对同一政策重复命中递减，却仍保留原始 yield 统计？ 递减训练奖励防止 auditor 靠反复触发同一漏洞刷分，鼓励覆盖更多政策；原始 yield 则描述实际命中事件，可超过每百 episode 一百次。两种统计对象不同，去重覆盖和事件总量应分列，局部奖励实现也不等于完成整套审计 RL。 例如一段对话连续三次触发同一违规，训练可依次少奖或不奖，但事件日志仍应记录三次，不能为去重而丢原始证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bbf997d26ce06409">为什么违规奖励对同一政策重复命中递减，却仍保留原始 yield 统计？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprobe">PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>递减训练奖励防止 auditor 靠反复触发同一漏洞刷分，鼓励覆盖更多政策；原始 yield 则描述实际命中事件，可超过每百 episode 一百次。两种统计对象不同，去重覆盖和事件总量应分列，局部奖励实现也不等于完成整套审计 RL。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一段对话连续三次触发同一违规，训练可依次少奖或不奖，但事件日志仍应记录三次，不能为去重而丢原始证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22124">原论文</a> · <a href="../../../../agent-research/2610.22124-probe/">实现解读</a> · <a href="#qa-bbf997d26ce06409">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:probe" data-paper-title="PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents Agent Mohamed bin Zayed University of Artificial Intelligence 2026-10-15 任务完成并不等于按业务/隐私政策完成；只测试最终状态或有害文本也可能漏掉多轮工具调用中的违规。PROBE 训练扮演正常客户的 auditor，与冻结 target 交互，私有 verifier 从完整 trace 判断违规；奖励综合违规、可信客户行为、工具流程进展和策略多样性，比较 GRPO、DPO 和 GFlowNet。 成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。只实现惰性 trace/verifier/reward 接口和四个独立规则示例；没有训练审计模型，也没有接入完整 SkyAssist 或真实目标服务。每 seed 构造 12 条惰性 trace，随机化重复轮数，不执行任何工具。四个示例核验 required fields、当前 mutation intent 的确认、限制目的地及人数；它们不是原文完整 20 策略套件。第五个明确 unsupported 的语义策略留在 coverage 分母。  公共评测与协议 Agent RL Agent 评测与可靠性：如何知道真的做对了 原始 violation yield、episode-policy 去重 yield 与 coverage，为何不能互换？ 原始yield可重复计同一政策跨turn命中，可能超过每百episode的100；去重yield去掉episode内政策重复，coverage分母是声明政策全集。它们分别描述命中量与范围，不是同一个成功概率。 示意：一个episode三次命中同一policy，原始命中3、去重命中1，覆盖仍只增加一种政策。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d1e3f83fa2deaa51">原始 violation yield、episode-policy 去重 yield 与 coverage，为何不能互换？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprobe">PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原始yield可重复计同一政策跨turn命中，可能超过每百episode的100；去重yield去掉episode内政策重复，coverage分母是声明政策全集。它们分别描述命中量与范围，不是同一个成功概率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个episode三次命中同一policy，原始命中3、去重命中1，覆盖仍只增加一种政策。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22124">原论文</a> · <a href="../../../../agent-research/2610.22124-probe/">实现解读</a> · <a href="#qa-d1e3f83fa2deaa51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:probe" data-paper-title="PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents Agent Mohamed bin Zayed University of Artificial Intelligence 2026-10-15 任务完成并不等于按业务/隐私政策完成；只测试最终状态或有害文本也可能漏掉多轮工具调用中的违规。PROBE 训练扮演正常客户的 auditor，与冻结 target 交互，私有 verifier 从完整 trace 判断违规；奖励综合违规、可信客户行为、工具流程进展和策略多样性，比较 GRPO、DPO 和 GFlowNet。 成本过高，不复现（审查 DONE）。component_only / L1 CPU 机制诊断。只实现惰性 trace/verifier/reward 接口和四个独立规则示例；没有训练审计模型，也没有接入完整 SkyAssist 或真实目标服务。每 seed 构造 12 条惰性 trace，随机化重复轮数，不执行任何工具。四个示例核验 required fields、当前 mutation intent 的确认、限制目的地及人数；它们不是原文完整 20 策略套件。第五个明确 unsupported 的语义策略留在 coverage 分母。  公共评测与协议 Agent RL Agent 评测与可靠性：如何知道真的做对了 PROBE 重复命中衰减需要在哪里重置 policy 计数？ 文档n_i是本episode已有命中数，首次权重1、第二次1/2、之后0；新episode应重新计。统计原始yield时又不能沿用此衰减删除命中，无命中和unsupported政策仍留在分母。 示意：上一episode已命中两次，不应让下一episode该policy的第一次命中奖励变成0。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b4ae230241e88d90">PROBE 重复命中衰减需要在哪里重置 policy 计数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aprobe">PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Mohamed bin Zayed University of Artificial Intelligence</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档n_i是本episode已有命中数，首次权重1、第二次1/2、之后0；新episode应重新计。统计原始yield时又不能沿用此衰减删除命中，无命中和unsupported政策仍留在分母。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>上一episode已命中两次，不应让下一episode该policy的第一次命中奖励变成0。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22124">原论文</a> · <a href="../../../../agent-research/2610.22124-probe/">实现解读</a> · <a href="#qa-b4ae230241e88d90">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scipivot" data-paper-title="SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents Agent University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核） 2026-10-15 26 个跨六科学领域项目、六个月人类纠偏记录构成 248 个关键决策：一个选项是原 LLM 方案，另一个为人类纠正方案。评测器选择更适当的后续研究计划，不是预测项目最终成功。构建 reference 可以看后续记录，但被测模型最多只能看纠偏前项目状态，不能看未来轨迹、正确标签或方案来源身份。 完整实验成本过高，不复现（审查 DONE），full_experiment_status: not_reproduced_high_cost。adapter: null，evaluation_protocol_interface，仅诊断，不晋级 Evolve。本地只接入已发布的 options-only：公开输入与 grader references 分离、双顺序计划、严格解析、完整失败分母、case 等权与 bootstrap。没有调用模型、没有完整项目记录，也没有本地科学研究能力分数。adapter: null，evaluation_protocol_interface，仅诊断，不晋级 Evolve。  公共评测与协议 科学研究判断与纠偏 Agent 评测与可靠性：如何知道真的做对了 SciPIvot 让模型判断的是研究纠偏选择，还是项目最终能否成功？ 它用纠偏前项目状态和两个后续方案，评价哪一个更适当；reference来自后续人类纠偏，但被测模型不能看到未来轨迹或方案来源身份。它不是最终项目成功预测。 示意：选择眼下更合理的下一步，并不保证六个月后的整个研究项目一定成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-scipivot-7482a1e6" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-011920e64c2ec0a1">SciPIvot 让模型判断的是研究纠偏选择，还是项目最终能否成功？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascipivot">SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它用纠偏前项目状态和两个后续方案，评价哪一个更适当；reference来自后续人类纠偏，但被测模型不能看到未来轨迹或方案来源身份。它不是最终项目成功预测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>选择眼下更合理的下一步，并不保证六个月后的整个研究项目一定成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21082">原论文</a> · <a href="../../../../agent-research/2610.21082-scipivot/">实现解读</a> · <a href="#qa-011920e64c2ec0a1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scipivot" data-paper-title="SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents Agent University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核） 2026-10-15 26 个跨六科学领域项目、六个月人类纠偏记录构成 248 个关键决策：一个选项是原 LLM 方案，另一个为人类纠正方案。评测器选择更适当的后续研究计划，不是预测项目最终成功。构建 reference 可以看后续记录，但被测模型最多只能看纠偏前项目状态，不能看未来轨迹、正确标签或方案来源身份。 完整实验成本过高，不复现（审查 DONE），full_experiment_status: not_reproduced_high_cost。adapter: null，evaluation_protocol_interface，仅诊断，不晋级 Evolve。本地只接入已发布的 options-only：公开输入与 grader references 分离、双顺序计划、严格解析、完整失败分母、case 等权与 bootstrap。没有调用模型、没有完整项目记录，也没有本地科学研究能力分数。adapter: null，evaluation_protocol_interface，仅诊断，不晋级 Evolve。  公共评测与协议 科学研究判断与纠偏 Agent 评测与可靠性：如何知道真的做对了 为什么交换选项位置后要重开独立会话，并按 case 而非两次回答重采样？ 位置交换用于检查选择是否稳定，独立会话避免第一次回答污染第二次；两种顺序仍来自同一项目决策，不能当成两个独立样本。被测模型只能看纠偏前状态，后续记录可用于构建参考，却不能作为输入，更不能暴露哪项来自人类或原 LLM。 例如同一计划甲乙分别放 A/B 和 B/A，若在同一会话里连问，模型可能记住先前选择而非重新判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9fb1bddc37dbff1d">为什么交换选项位置后要重开独立会话，并按 case 而非两次回答重采样？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascipivot">SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>位置交换用于检查选择是否稳定，独立会话避免第一次回答污染第二次；两种顺序仍来自同一项目决策，不能当成两个独立样本。被测模型只能看纠偏前状态，后续记录可用于构建参考，却不能作为输入，更不能暴露哪项来自人类或原 LLM。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一计划甲乙分别放 A/B 和 B/A，若在同一会话里连问，模型可能记住先前选择而非重新判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21082">原论文</a> · <a href="../../../../agent-research/2610.21082-scipivot/">实现解读</a> · <a href="#qa-9fb1bddc37dbff1d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scipivot" data-paper-title="SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents Agent University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核） 2026-10-15 26 个跨六科学领域项目、六个月人类纠偏记录构成 248 个关键决策：一个选项是原 LLM 方案，另一个为人类纠正方案。评测器选择更适当的后续研究计划，不是预测项目最终成功。构建 reference 可以看后续记录，但被测模型最多只能看纠偏前项目状态，不能看未来轨迹、正确标签或方案来源身份。 完整实验成本过高，不复现（审查 DONE），full_experiment_status: not_reproduced_high_cost。adapter: null，evaluation_protocol_interface，仅诊断，不晋级 Evolve。本地只接入已发布的 options-only：公开输入与 grader references 分离、双顺序计划、严格解析、完整失败分母、case 等权与 bootstrap。没有调用模型、没有完整项目记录，也没有本地科学研究能力分数。adapter: null，evaluation_protocol_interface，仅诊断，不晋级 Evolve。  公共评测与协议 科学研究判断与纠偏 Agent 评测与可靠性：如何知道真的做对了 交换 options 顺序，与把同 case 的两次回答当两个独立样本有什么区别？ 双顺序用于测并抵消位置偏好，但两次仍属于同一case，需先形成case分数再按case重采样。独立计数会夸大样本量并低估相关性。 示意：一个case的AB与BA两次判断，不等于两个不同研究决策案例。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-0843c04e300f78ca">交换 options 顺序，与把同 case 的两次回答当两个独立样本有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascipivot">SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>双顺序用于测并抵消位置偏好，但两次仍属于同一case，需先形成case分数再按case重采样。独立计数会夸大样本量并低估相关性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个case的AB与BA两次判断，不等于两个不同研究决策案例。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21082">原论文</a> · <a href="../../../../agent-research/2610.21082-scipivot/">实现解读</a> · <a href="#qa-0843c04e300f78ca">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:scipivot" data-paper-title="SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents Agent University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核） 2026-10-15 26 个跨六科学领域项目、六个月人类纠偏记录构成 248 个关键决策：一个选项是原 LLM 方案，另一个为人类纠正方案。评测器选择更适当的后续研究计划，不是预测项目最终成功。构建 reference 可以看后续记录，但被测模型最多只能看纠偏前项目状态，不能看未来轨迹、正确标签或方案来源身份。 完整实验成本过高，不复现（审查 DONE），full_experiment_status: not_reproduced_high_cost。adapter: null，evaluation_protocol_interface，仅诊断，不晋级 Evolve。本地只接入已发布的 options-only：公开输入与 grader references 分离、双顺序计划、严格解析、完整失败分母、case 等权与 bootstrap。没有调用模型、没有完整项目记录，也没有本地科学研究能力分数。adapter: null，evaluation_protocol_interface，仅诊断，不晋级 Evolve。  公共评测与协议 科学研究判断与纠偏 Agent 评测与可靠性：如何知道真的做对了 SciPIvot 的原 questions 文件为什么不能直接挂给被测 Agent？ 官方源含references，可信ingestion需按allowlist导出仅id与两个选项，grader私有参考另存。模型会话彼此独立，不能读取仓库或未来记录绕过options-only边界。 示意：把完整questions.json作为上下文，即使提示“不看reference”也未实现数据隔离。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-dbb80695c86f30d7">SciPIvot 的原 questions 文件为什么不能直接挂给被测 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ascipivot">SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>官方源含references，可信ingestion需按allowlist导出仅id与两个选项，grader私有参考另存。模型会话彼此独立，不能读取仓库或未来记录绕过options-only边界。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把完整questions.json作为上下文，即使提示“不看reference”也未实现数据隔离。</p>
<p class="ar-learning-sources">依据：背景与主要改动、已发布数据与来源；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21082">原论文</a> · <a href="../../../../agent-research/2610.21082-scipivot/">实现解读</a> · <a href="#qa-dbb80695c86f30d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:shortcut-sensitivity" data-paper-title="Shortcut Sensitivity in Agent-Safety Evaluations" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Shortcut Sensitivity in Agent-Safety Evaluations Agent Kontext 2026-10-15 Agent 安全评测会把轨迹长度、工具名、来源标记和重复交互带入输入。高分有时来自这些构造特征，未必测到了真正的风险判断。论文建立三级推断阶梯：①线索能否预测标签；②线索与 guard 决策是否相关；③仅改变线索的配对干预是否改变决策。前一级只能提出下一级的检查目标，不能自动推导“模型走了捷径”。原图出处：原文 Figure 1：三级 shortcut audit。 单 A100/A30/Mac 无相应 API/多模型预算且整体成本仍高，成本过高，不复现（审查 DONE）。本地是 component_only / CPU 机制诊断，不是安全 guard。本地是 component_only / CPU 机制诊断，不是安全 guard。读标签的工具名查表只用于证明 benchmark 标签可预测性，不能作为 Agent、安全检测能力或 Evolve 晋级证据。  公共评测与协议 Agent 评测与可靠性：如何知道真的做对了 Shortcut Sensitivity 为什么先检查评测输入里的构造线索？ 工具名、长度、来源标记和重复交互可能带来可预测标签的捷径，使高分未必体现真正风险判断。研究分开审计标签可预测性、guard关联及构念保持的配对干预。 示意：某工具名总出现在unsafe样本里，模型可能仅靠名字取得好成绩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-shortcut-sensitivity-1f4bb949" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-53510aaefacc8ed3">Shortcut Sensitivity 为什么先检查评测输入里的构造线索？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ashortcut-sensitivity">Shortcut Sensitivity in Agent-Safety Evaluations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kontext</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具名、长度、来源标记和重复交互可能带来可预测标签的捷径，使高分未必体现真正风险判断。研究分开审计标签可预测性、guard关联及构念保持的配对干预。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某工具名总出现在unsafe样本里，模型可能仅靠名字取得好成绩。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22243">原论文</a> · <a href="../../../../agent-research/2610.22243-shortcut-sensitivity/">实现解读</a> · <a href="#qa-53510aaefacc8ed3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:shortcut-sensitivity" data-paper-title="Shortcut Sensitivity in Agent-Safety Evaluations" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Shortcut Sensitivity in Agent-Safety Evaluations Agent Kontext 2026-10-15 Agent 安全评测会把轨迹长度、工具名、来源标记和重复交互带入输入。高分有时来自这些构造特征，未必测到了真正的风险判断。论文建立三级推断阶梯：①线索能否预测标签；②线索与 guard 决策是否相关；③仅改变线索的配对干预是否改变决策。前一级只能提出下一级的检查目标，不能自动推导“模型走了捷径”。原图出处：原文 Figure 1：三级 shortcut audit。 单 A100/A30/Mac 无相应 API/多模型预算且整体成本仍高，成本过高，不复现（审查 DONE）。本地是 component_only / CPU 机制诊断，不是安全 guard。本地是 component_only / CPU 机制诊断，不是安全 guard。读标签的工具名查表只用于证明 benchmark 标签可预测性，不能作为 Agent、安全检测能力或 Evolve 晋级证据。  公共评测与协议 Agent 评测与可靠性：如何知道真的做对了 工具名能预测标签，为什么还不能断言 guard 使用了这个捷径？ 第一层只说明数据构造存在相关线索，第二层检查 guard 决策相关性，第三层保持其余条件只改线索，才更接近行为依赖证据。配对效应还需控制随机不一致与安慰剂，不能把相关性、无符号翻转率和有符号效应混成同一结论。 例如危险样本常用某工具名，只训练名字查表能高分；要证明 guard 走捷径，还需改名不改行为并观察其决策是否改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-fb9c6ae3c3a0bb7e">工具名能预测标签，为什么还不能断言 guard 使用了这个捷径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ashortcut-sensitivity">Shortcut Sensitivity in Agent-Safety Evaluations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kontext</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>第一层只说明数据构造存在相关线索，第二层检查 guard 决策相关性，第三层保持其余条件只改线索，才更接近行为依赖证据。配对效应还需控制随机不一致与安慰剂，不能把相关性、无符号翻转率和有符号效应混成同一结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如危险样本常用某工具名，只训练名字查表能高分；要证明 guard 走捷径，还需改名不改行为并观察其决策是否改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22243">原论文</a> · <a href="../../../../agent-research/2610.22243-shortcut-sensitivity/">实现解读</a> · <a href="#qa-fb9c6ae3c3a0bb7e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:shortcut-sensitivity" data-paper-title="Shortcut Sensitivity in Agent-Safety Evaluations" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Shortcut Sensitivity in Agent-Safety Evaluations Agent Kontext 2026-10-15 Agent 安全评测会把轨迹长度、工具名、来源标记和重复交互带入输入。高分有时来自这些构造特征，未必测到了真正的风险判断。论文建立三级推断阶梯：①线索能否预测标签；②线索与 guard 决策是否相关；③仅改变线索的配对干预是否改变决策。前一级只能提出下一级的检查目标，不能自动推导“模型走了捷径”。原图出处：原文 Figure 1：三级 shortcut audit。 单 A100/A30/Mac 无相应 API/多模型预算且整体成本仍高，成本过高，不复现（审查 DONE）。本地是 component_only / CPU 机制诊断，不是安全 guard。本地是 component_only / CPU 机制诊断，不是安全 guard。读标签的工具名查表只用于证明 benchmark 标签可预测性，不能作为 Agent、安全检测能力或 Evolve 晋级证据。  公共评测与协议 Agent 评测与可靠性：如何知道真的做对了 线索能预测标签、关联 guard 决策、配对干预效应，三者可直接互相推出吗？ 不能。前两项提示进一步测试目标，配对干预还需只改变线索而保持风险构念，并控制随机guard和格式安慰剂。相关性不足以断言模型实际使用了捷径。 示意：一个工具名与unsafe相关，但删掉名字后guard决策不变，证据仍不足以说它靠该名字判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ac8c0a7f5918e56a">线索能预测标签、关联 guard 决策、配对干预效应，三者可直接互相推出吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ashortcut-sensitivity">Shortcut Sensitivity in Agent-Safety Evaluations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kontext</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。前两项提示进一步测试目标，配对干预还需只改变线索而保持风险构念，并控制随机guard和格式安慰剂。相关性不足以断言模型实际使用了捷径。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个工具名与unsafe相关，但删掉名字后guard决策不变，证据仍不足以说它靠该名字判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22243">原论文</a> · <a href="../../../../agent-research/2610.22243-shortcut-sensitivity/">实现解读</a> · <a href="#qa-ac8c0a7f5918e56a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:shortcut-sensitivity" data-paper-title="Shortcut Sensitivity in Agent-Safety Evaluations" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Shortcut Sensitivity in Agent-Safety Evaluations Agent Kontext 2026-10-15 Agent 安全评测会把轨迹长度、工具名、来源标记和重复交互带入输入。高分有时来自这些构造特征，未必测到了真正的风险判断。论文建立三级推断阶梯：①线索能否预测标签；②线索与 guard 决策是否相关；③仅改变线索的配对干预是否改变决策。前一级只能提出下一级的检查目标，不能自动推导“模型走了捷径”。原图出处：原文 Figure 1：三级 shortcut audit。 单 A100/A30/Mac 无相应 API/多模型预算且整体成本仍高，成本过高，不复现（审查 DONE）。本地是 component_only / CPU 机制诊断，不是安全 guard。本地是 component_only / CPU 机制诊断，不是安全 guard。读标签的工具名查表只用于证明 benchmark 标签可预测性，不能作为 Agent、安全检测能力或 Evolve 晋级证据。  公共评测与协议 Agent 评测与可靠性：如何知道真的做对了 等 interaction 权重的 F1，为什么不能先算各 interaction 的 F1 再平均？ 文档先给每步1/n_g权重，累加加权TP/TN/FP/FN再算F1；F1是非线性比值，平均各组F1是另一口径。配对signed effect也不能替换成unsigned flip-rate。 示意：长交互不能仅因步骤多就在混淆矩阵里占更多总权重。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3e1e7f6f866b6b9b">等 interaction 权重的 F1，为什么不能先算各 interaction 的 F1 再平均？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Ashortcut-sensitivity">Shortcut Sensitivity in Agent-Safety Evaluations</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Kontext</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档先给每步1/n_g权重，累加加权TP/TN/FP/FN再算F1；F1是非线性比值，平均各组F1是另一口径。配对signed effect也不能替换成unsigned flip-rate。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>长交互不能仅因步骤多就在混淆矩阵里占更多总权重。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.22243">原论文</a> · <a href="../../../../agent-research/2610.22243-shortcut-sensitivity/">实现解读</a> · <a href="#qa-3e1e7f6f866b6b9b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tool-bottleneck-bench" data-paper-title="ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets Agent University of Osaka 2026-10-15 工具 Agent 的失败不只取决于模型：工具目录、可见菜单、工作流和返回记录编码会与 token/call/turn 上限交互。论文固定请求、事实和决策，分别操纵注册目录 R、可见菜单 V、认证工作流 W、返回状态 D。原协议有 36 个 family、12 个企业意图；routed menu 使用真值辅助缩窄，不能视为无需 oracle 的能力方案。 成本过高，不复现（审查 DONE），full_experiment_status: not_reproduced_high_cost。单测中的无模型 public-handoff controller 只是 sandbox/合同诊断，不是论文 Agent。本地为 evaluation_protocol_interface：有限任务编译器、真实状态沙箱、九义务 exact grader，以及一组官方历史行的 CPU 复算。adapter: null、diagnostic_only: true、promotion_eligible: false、evolve_integrated: false；没有评测新的 Agent。  公共评测与协议 工具 Agent 与 harness 预算 Agent 评测与可靠性：如何知道真的做对了 ToolBottleneckBench 为什么控制工具目录、菜单、工作流与返回编码？ 工具Agent失败可能来自系统接口与预算交互，而非单纯模型能力。固定任务事实和决策后分别操纵R/V/W/D，才能更清楚观察哪类压力与结果相关。 示意：模型相同，但可见菜单更长可能增加选择成本，不能直接归因于模型推理变差。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-tool-bottleneck-bench-4ca26883" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f2dd236615f6ba3b">ToolBottleneckBench 为什么控制工具目录、菜单、工作流与返回编码？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atool-bottleneck-bench">ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Osaka</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>工具Agent失败可能来自系统接口与预算交互，而非单纯模型能力。固定任务事实和决策后分别操纵R/V/W/D，才能更清楚观察哪类压力与结果相关。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模型相同，但可见菜单更长可能增加选择成本，不能直接归因于模型推理变差。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21098">原论文</a> · <a href="../../../../agent-research/2610.21098-tool-bottleneck-bench/">实现解读</a> · <a href="#qa-f2dd236615f6ba3b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tool-bottleneck-bench" data-paper-title="ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets Agent University of Osaka 2026-10-15 工具 Agent 的失败不只取决于模型：工具目录、可见菜单、工作流和返回记录编码会与 token/call/turn 上限交互。论文固定请求、事实和决策，分别操纵注册目录 R、可见菜单 V、认证工作流 W、返回状态 D。原协议有 36 个 family、12 个企业意图；routed menu 使用真值辅助缩窄，不能视为无需 oracle 的能力方案。 成本过高，不复现（审查 DONE），full_experiment_status: not_reproduced_high_cost。单测中的无模型 public-handoff controller 只是 sandbox/合同诊断，不是论文 Agent。本地为 evaluation_protocol_interface：有限任务编译器、真实状态沙箱、九义务 exact grader，以及一组官方历史行的 CPU 复算。adapter: null、diagnostic_only: true、promotion_eligible: false、evolve_integrated: false；没有评测新的 Agent。  公共评测与协议 工具 Agent 与 harness 预算 Agent 评测与可靠性：如何知道真的做对了 为什么把失败记作“首个未满足义务”，不等于已经完成因果归因？ 义务顺序提供一致标签，但后面还可能有其他失败，首个检查项未通过并不能证明它是唯一根因。固定请求事实再操纵目录、菜单、工作流和返回状态才能研究压力影响；真值辅助 routed menu 属诊断条件，不能被当无需 oracle 的部署能力。 例如工具没检索到先标可用性失败，参数逻辑也许同样错误；修复第一项后才可能暴露第二项，标签顺序不是因果证明。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-c5fe57bc8a85b2fa">为什么把失败记作“首个未满足义务”，不等于已经完成因果归因？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atool-bottleneck-bench">ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Osaka</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>义务顺序提供一致标签，但后面还可能有其他失败，首个检查项未通过并不能证明它是唯一根因。固定请求事实再操纵目录、菜单、工作流和返回状态才能研究压力影响；真值辅助 routed menu 属诊断条件，不能被当无需 oracle 的部署能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具没检索到先标可用性失败，参数逻辑也许同样错误；修复第一项后才可能暴露第二项，标签顺序不是因果证明。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21098">原论文</a> · <a href="../../../../agent-research/2610.21098-tool-bottleneck-bench/">实现解读</a> · <a href="#qa-c5fe57bc8a85b2fa">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tool-bottleneck-bench" data-paper-title="ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets Agent University of Osaka 2026-10-15 工具 Agent 的失败不只取决于模型：工具目录、可见菜单、工作流和返回记录编码会与 token/call/turn 上限交互。论文固定请求、事实和决策，分别操纵注册目录 R、可见菜单 V、认证工作流 W、返回状态 D。原协议有 36 个 family、12 个企业意图；routed menu 使用真值辅助缩窄，不能视为无需 oracle 的能力方案。 成本过高，不复现（审查 DONE），full_experiment_status: not_reproduced_high_cost。单测中的无模型 public-handoff controller 只是 sandbox/合同诊断，不是论文 Agent。本地为 evaluation_protocol_interface：有限任务编译器、真实状态沙箱、九义务 exact grader，以及一组官方历史行的 CPU 复算。adapter: null、diagnostic_only: true、promotion_eligible: false、evolve_integrated: false；没有评测新的 Agent。  公共评测与协议 工具 Agent 与 harness 预算 Agent 评测与可靠性：如何知道真的做对了 原协议真值辅助的 routed menu，与无需 oracle 的生产路由器有什么差别？ 真值辅助缩窄菜单属于受控评测条件，不证明实际系统能自动找到同样菜单。它可用来定位瓶颈，但不能当成已经实现的无oracle能力方案。 示意：预先知道正确工具再只展示它，与部署时从大目录自主检索正确工具不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-868224bb54ceef90">原协议真值辅助的 routed menu，与无需 oracle 的生产路由器有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atool-bottleneck-bench">ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Osaka</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>真值辅助缩窄菜单属于受控评测条件，不证明实际系统能自动找到同样菜单。它可用来定位瓶颈，但不能当成已经实现的无oracle能力方案。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>预先知道正确工具再只展示它，与部署时从大目录自主检索正确工具不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21098">原论文</a> · <a href="../../../../agent-research/2610.21098-tool-bottleneck-bench/">实现解读</a> · <a href="#qa-868224bb54ceef90">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tool-bottleneck-bench" data-paper-title="ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets Agent University of Osaka 2026-10-15 工具 Agent 的失败不只取决于模型：工具目录、可见菜单、工作流和返回记录编码会与 token/call/turn 上限交互。论文固定请求、事实和决策，分别操纵注册目录 R、可见菜单 V、认证工作流 W、返回状态 D。原协议有 36 个 family、12 个企业意图；routed menu 使用真值辅助缩窄，不能视为无需 oracle 的能力方案。 成本过高，不复现（审查 DONE），full_experiment_status: not_reproduced_high_cost。单测中的无模型 public-handoff controller 只是 sandbox/合同诊断，不是论文 Agent。本地为 evaluation_protocol_interface：有限任务编译器、真实状态沙箱、九义务 exact grader，以及一组官方历史行的 CPU 复算。adapter: null、diagnostic_only: true、promotion_eligible: false、evolve_integrated: false；没有评测新的 Agent。  公共评测与协议 工具 Agent 与 harness 预算 Agent 评测与可靠性：如何知道真的做对了 目录压力 ITT 中，未检索到工具或基础设施失败的请求能从分母删除吗？ 不能。计划分母应保留这些失败，否则只在可用请求上算选择率会虚高。还需区分首个未满足义务标签和另列的终止原因，二者都不能自动充当因果归因。 示意：100次计划只有80次取得候选菜单，应在完整100次口径里报告结果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d4a1b13e4351da91">目录压力 ITT 中，未检索到工具或基础设施失败的请求能从分母删除吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atool-bottleneck-bench">ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Osaka</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。计划分母应保留这些失败，否则只在可用请求上算选择率会虚高。还需区分首个未满足义务标签和另列的终止原因，二者都不能自动充当因果归因。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>100次计划只有80次取得候选菜单，应在完整100次口径里报告结果。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.21098">原论文</a> · <a href="../../../../agent-research/2610.21098-tool-bottleneck-bench/">实现解读</a> · <a href="#qa-d4a1b13e4351da91">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:alpha-diana" data-paper-title="AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks Agent Hong Kong Baptist University 2026-10-14 同一模型装进不同 Harness 后，提示、工具、恢复策略和记忆都会影响结果。只报告成功任务或平均 token，容易把丢失评分、运行失败、反复重试的成本掩盖掉。AlphaDiana 用统一任务、采样和资源政策比较完整的“模型—Harness”系统，同时保留各 Harness 的原生执行方式。原文 §2、附录 A–B 本地保留四项可独立执行的协议： 原文多模型、多 Harness、多任务矩阵使用 16×A100-80GB，并包含27B/31B模型和远程模型，完整实验成本过高，不复现（审查 DONE）。这些是合成协议诊断，不是新模型能力或真实tokenizer费用。evaluation_protocol_interface / L1 CPU。实现记录、状态和计量合同，不实现新的推理 Agent，不冒充官方 benchmark 接入。CPU fixture 让 actor 从公开算式计算答案，单独 grader 持有 reference；注入执行失败、评分中断和错误答案，实际运行重试、状态管理和汇总。  公共评测与协议 Harness 配对测量与状态隔离 Agent 评测与可靠性：如何知道真的做对了 AlphaDiana 为什么分开记录执行状态与评分状态？ 程序运行成功并不保证grader给出了有效判定；评分中断属于未知而非自动正确或错误。分离状态并保留完整计划分母，才能看见执行失败、缺失评分及真实覆盖率。 示意：工具完成了操作，但评测器超时，这个样本应标未评分，不能从报告消失。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-alpha-diana-d2460928" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-aab95853f7796c15">AlphaDiana 为什么分开记录执行状态与评分状态？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aalpha-diana">AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong Baptist University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>程序运行成功并不保证grader给出了有效判定；评分中断属于未知而非自动正确或错误。分离状态并保留完整计划分母，才能看见执行失败、缺失评分及真实覆盖率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工具完成了操作，但评测器超时，这个样本应标未评分，不能从报告消失。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20675">原论文</a> · <a href="../../../../agent-research/2610.20675-alpha-diana/">实现解读</a> · <a href="#qa-aab95853f7796c15">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:alpha-diana" data-paper-title="AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks Agent Hong Kong Baptist University 2026-10-14 同一模型装进不同 Harness 后，提示、工具、恢复策略和记忆都会影响结果。只报告成功任务或平均 token，容易把丢失评分、运行失败、反复重试的成本掩盖掉。AlphaDiana 用统一任务、采样和资源政策比较完整的“模型—Harness”系统，同时保留各 Harness 的原生执行方式。原文 §2、附录 A–B 本地保留四项可独立执行的协议： 原文多模型、多 Harness、多任务矩阵使用 16×A100-80GB，并包含27B/31B模型和远程模型，完整实验成本过高，不复现（审查 DONE）。这些是合成协议诊断，不是新模型能力或真实tokenizer费用。evaluation_protocol_interface / L1 CPU。实现记录、状态和计量合同，不实现新的推理 Agent，不冒充官方 benchmark 接入。CPU fixture 让 actor 从公开算式计算答案，单独 grader 持有 reference；注入执行失败、评分中断和错误答案，实际运行重试、状态管理和汇总。  公共评测与协议 Harness 配对测量与状态隔离 Agent 评测与可靠性：如何知道真的做对了 重试为什么只增加 attempt，而不增加逻辑样本分母或挑最好的一次？ 同一 task/sample 的重试仍是在解决同一请求，多算分母或挑最好记录会改变采样含义并隐藏失败成本。报告取最新记录、总成本累加所有 attempt，运行状态与评分状态分开；未评分是未知，不应伪装正确或从计划样本中静默删除。 例如同题先超时再成功，两次 token 都计成本，但样本仍是一份；不能只留下便宜的成功日志，让第一次尝试仿佛没发生。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-5990e05270ed514c">重试为什么只增加 attempt，而不增加逻辑样本分母或挑最好的一次？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aalpha-diana">AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong Baptist University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一 task/sample 的重试仍是在解决同一请求，多算分母或挑最好记录会改变采样含义并隐藏失败成本。报告取最新记录、总成本累加所有 attempt，运行状态与评分状态分开；未评分是未知，不应伪装正确或从计划样本中静默删除。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同题先超时再成功，两次 token 都计成本，但样本仍是一份；不能只留下便宜的成功日志，让第一次尝试仿佛没发生。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20675">原论文</a> · <a href="../../../../agent-research/2610.20675-alpha-diana/">实现解读</a> · <a href="#qa-5990e05270ed514c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:alpha-diana" data-paper-title="AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks Agent Hong Kong Baptist University 2026-10-14 同一模型装进不同 Harness 后，提示、工具、恢复策略和记忆都会影响结果。只报告成功任务或平均 token，容易把丢失评分、运行失败、反复重试的成本掩盖掉。AlphaDiana 用统一任务、采样和资源政策比较完整的“模型—Harness”系统，同时保留各 Harness 的原生执行方式。原文 §2、附录 A–B 本地保留四项可独立执行的协议： 原文多模型、多 Harness、多任务矩阵使用 16×A100-80GB，并包含27B/31B模型和远程模型，完整实验成本过高，不复现（审查 DONE）。这些是合成协议诊断，不是新模型能力或真实tokenizer费用。evaluation_protocol_interface / L1 CPU。实现记录、状态和计量合同，不实现新的推理 Agent，不冒充官方 benchmark 接入。CPU fixture 让 actor 从公开算式计算答案，单独 grader 持有 reference；注入执行失败、评分中断和错误答案，实际运行重试、状态管理和汇总。  公共评测与协议 Harness 配对测量与状态隔离 Agent 评测与可靠性：如何知道真的做对了 重试后选最新 attempt，与选最好 attempt 会产生什么评测差异？ 同一逻辑样本的重试不增加分母，协议按最新状态报告；挑最好结果会把多次机会变成隐含选择优势。成本则累计所有attempt，不能只算被展示的最后一次。 示意：先成功后重试失败，按最新协议不能回捞第一次成功，却只报告一次执行成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f7a972d5c6d3a5f6">重试后选最新 attempt，与选最好 attempt 会产生什么评测差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aalpha-diana">AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong Baptist University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一逻辑样本的重试不增加分母，协议按最新状态报告；挑最好结果会把多次机会变成隐含选择优势。成本则累计所有attempt，不能只算被展示的最后一次。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先成功后重试失败，按最新协议不能回捞第一次成功，却只报告一次执行成本。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20675">原论文</a> · <a href="../../../../agent-research/2610.20675-alpha-diana/">实现解读</a> · <a href="#qa-f7a972d5c6d3a5f6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:alpha-diana" data-paper-title="AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks Agent Hong Kong Baptist University 2026-10-14 同一模型装进不同 Harness 后，提示、工具、恢复策略和记忆都会影响结果。只报告成功任务或平均 token，容易把丢失评分、运行失败、反复重试的成本掩盖掉。AlphaDiana 用统一任务、采样和资源政策比较完整的“模型—Harness”系统，同时保留各 Harness 的原生执行方式。原文 §2、附录 A–B 本地保留四项可独立执行的协议： 原文多模型、多 Harness、多任务矩阵使用 16×A100-80GB，并包含27B/31B模型和远程模型，完整实验成本过高，不复现（审查 DONE）。这些是合成协议诊断，不是新模型能力或真实tokenizer费用。evaluation_protocol_interface / L1 CPU。实现记录、状态和计量合同，不实现新的推理 Agent，不冒充官方 benchmark 接入。CPU fixture 让 actor 从公开算式计算答案，单独 grader 持有 reference；注入执行失败、评分中断和错误答案，实际运行重试、状态管理和汇总。  公共评测与协议 Harness 配对测量与状态隔离 Agent 评测与可靠性：如何知道真的做对了 AlphaDiana 何时必须让完整 tokens/correct 返回未知？ 没有已确认正确样本、任一attempt缺token，或请求样本尚无执行记录时，完整成本为None。已知token与覆盖率可以单列，但不能把部分计量补成完整推理成本。 示意：两次尝试只记录了一次token，即使最终正确，也不能声称已知道完整每正确样本成本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-4b3a77db599905fc">AlphaDiana 何时必须让完整 tokens/correct 返回未知？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aalpha-diana">AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Hong Kong Baptist University</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有已确认正确样本、任一attempt缺token，或请求样本尚无执行记录时，完整成本为None。已知token与覆盖率可以单列，但不能把部分计量补成完整推理成本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两次尝试只记录了一次token，即使最终正确，也不能声称已知道完整每正确样本成本。</p>
<p class="ar-learning-sources">依据：核心公式、无 gold 边界与限制；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20675">原论文</a> · <a href="../../../../agent-research/2610.20675-alpha-diana/">实现解读</a> · <a href="#qa-4b3a77db599905fc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coda" data-paper-title="Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents Agent Alibaba Token Hub, Alibaba Group 2026-10-14 策略与技能库共同训练后的最高成绩可能依赖技能原有措辞，一旦部署后技能被改写就退化。CODA 不把 delivered bank 的峰值当唯一结果，而是在相同任务上评估 T1 意义保持改写、T2 内容缺失、T3 误导内容及 no-skill anchor。原文 §3–4、附录 E要求先在原始库检索一次，固定选中集合和 retrieval-side 字段，只替换内容；不能重新检索引入额外混杂。 完整评测需要四类训练后的策略／技能对、五个真实环境和多种扰动重复，整体对单 A100/A30 或 Mac 成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现内容改写边界和配对指标，不重训共进化策略，不生成“语义保持”保证。每 seed 生成 32 个二值结果 fixture，在全部六条件上保留同一 ID 集合，实际执行内容字段替换和配对计算。独立计数验证全分母 RR；负对照故意改成条件分母，保存偏差。拒绝漏任务、修改检索字段和改写未选中技能。结果见 CPU 产物，不代表任何策略的真实稳健性。  公共评测与协议 技能漂移与共进化稳健性 Agent 评测与可靠性：如何知道真的做对了 CODA 为什么在改写技能前先冻结原始检索集合？ 它要审计策略对已交付技能内容和措辞的依赖，而重新检索还会改变选中技能与排序。固定retrieval-side字段只替换内容，才能减少检索变化对结果的混杂。 示意：改写一个技能后若它不再被检索到，无法分清是措辞依赖还是检索召回变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-coda-3d28333f" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-9cb6ac979ccc11bc">CODA 为什么在改写技能前先冻结原始检索集合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoda">Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Token Hub, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它要审计策略对已交付技能内容和措辞的依赖，而重新检索还会改变选中技能与排序。固定retrieval-side字段只替换内容，才能减少检索变化对结果的混杂。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>改写一个技能后若它不再被检索到，无法分清是措辞依赖还是检索召回变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20845">原论文</a> · <a href="../../../../agent-research/2610.20845-coda/">实现解读</a> · <a href="#qa-9cb6ac979ccc11bc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coda" data-paper-title="Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents Agent Alibaba Token Hub, Alibaba Group 2026-10-14 策略与技能库共同训练后的最高成绩可能依赖技能原有措辞，一旦部署后技能被改写就退化。CODA 不把 delivered bank 的峰值当唯一结果，而是在相同任务上评估 T1 意义保持改写、T2 内容缺失、T3 误导内容及 no-skill anchor。原文 §3–4、附录 E要求先在原始库检索一次，固定选中集合和 retrieval-side 字段，只替换内容；不能重新检索引入额外混杂。 完整评测需要四类训练后的策略／技能对、五个真实环境和多种扰动重复，整体对单 A100/A30 或 Mac 成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现内容改写边界和配对指标，不重训共进化策略，不生成“语义保持”保证。每 seed 生成 32 个二值结果 fixture，在全部六条件上保留同一 ID 集合，实际执行内容字段替换和配对计算。独立计数验证全分母 RR；负对照故意改成条件分母，保存偏差。拒绝漏任务、修改检索字段和改写未选中技能。结果见 CPU 产物，不代表任何策略的真实稳健性。  公共评测与协议 技能漂移与共进化稳健性 Agent 评测与可靠性：如何知道真的做对了 对技能内容做意义保持改写时，为什么必须固定原始检索选中集合？ 重新检索会同时改变拿到哪些技能，无法区分策略依赖措辞还是检索器排名变化。先固定选中身份及检索字段，只替换内容，才能更集中测技能表达的脆弱性；意义等价也不能靠字符串相似度证明，整体成功率不变仍可能隐藏双向 outcome flip。 例如把同一流程改写为同义句，应仍提供原来三份技能；若改写后换了另外三份，性能变化就不再只由措辞导致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e2716653480cf5c0">对技能内容做意义保持改写时，为什么必须固定原始检索选中集合？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoda">Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Token Hub, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重新检索会同时改变拿到哪些技能，无法区分策略依赖措辞还是检索器排名变化。先固定选中身份及检索字段，只替换内容，才能更集中测技能表达的脆弱性；意义等价也不能靠字符串相似度证明，整体成功率不变仍可能隐藏双向 outcome flip。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把同一流程改写为同义句，应仍提供原来三份技能；若改写后换了另外三份，性能变化就不再只由措辞导致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20845">原论文</a> · <a href="../../../../agent-research/2610.20845-coda/">实现解读</a> · <a href="#qa-e2716653480cf5c0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coda" data-paper-title="Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents Agent Alibaba Token Hub, Alibaba Group 2026-10-14 策略与技能库共同训练后的最高成绩可能依赖技能原有措辞，一旦部署后技能被改写就退化。CODA 不把 delivered bank 的峰值当唯一结果，而是在相同任务上评估 T1 意义保持改写、T2 内容缺失、T3 误导内容及 no-skill anchor。原文 §3–4、附录 E要求先在原始库检索一次，固定选中集合和 retrieval-side 字段，只替换内容；不能重新检索引入额外混杂。 完整评测需要四类训练后的策略／技能对、五个真实环境和多种扰动重复，整体对单 A100/A30 或 Mac 成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现内容改写边界和配对指标，不重训共进化策略，不生成“语义保持”保证。每 seed 生成 32 个二值结果 fixture，在全部六条件上保留同一 ID 集合，实际执行内容字段替换和配对计算。独立计数验证全分母 RR；负对照故意改成条件分母，保存偏差。拒绝漏任务、修改检索字段和改写未选中技能。结果见 CPU 产物，不代表任何策略的真实稳健性。  公共评测与协议 技能漂移与共进化稳健性 Agent 评测与可靠性：如何知道真的做对了 CODA 为什么除 aggregate success rate 外还看逐任务 CR？ 总成功率可被双向翻转抵消：一些原成功任务失败、另一些原失败任务成功，总数不变。CR比较同一任务两条件结果一致性，并用重复未扰动运行作为随机噪声参照。 示意：两个任务的成败完全互换，总成功率仍为50%，但CR为0。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-de7e1d0ed3d16d8a">CODA 为什么除 aggregate success rate 外还看逐任务 CR？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoda">Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Token Hub, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>总成功率可被双向翻转抵消：一些原成功任务失败、另一些原失败任务成功，总数不变。CR比较同一任务两条件结果一致性，并用重复未扰动运行作为随机噪声参照。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个任务的成败完全互换，总成功率仍为50%，但CR为0。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20845">原论文</a> · <a href="../../../../agent-research/2610.20845-coda/">实现解读</a> · <a href="#qa-de7e1d0ed3d16d8a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coda" data-paper-title="Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents Agent Alibaba Token Hub, Alibaba Group 2026-10-14 策略与技能库共同训练后的最高成绩可能依赖技能原有措辞，一旦部署后技能被改写就退化。CODA 不把 delivered bank 的峰值当唯一结果，而是在相同任务上评估 T1 意义保持改写、T2 内容缺失、T3 误导内容及 no-skill anchor。原文 §3–4、附录 E要求先在原始库检索一次，固定选中集合和 retrieval-side 字段，只替换内容；不能重新检索引入额外混杂。 完整评测需要四类训练后的策略／技能对、五个真实环境和多种扰动重复，整体对单 A100/A30 或 Mac 成本过高，不复现（审查 DONE）。evaluation_protocol_interface / L1 CPU。实现内容改写边界和配对指标，不重训共进化策略，不生成“语义保持”保证。每 seed 生成 32 个二值结果 fixture，在全部六条件上保留同一 ID 集合，实际执行内容字段替换和配对计算。独立计数验证全分母 RR；负对照故意改成条件分母，保存偏差。拒绝漏任务、修改检索字段和改写未选中技能。结果见 CPU 产物，不代表任何策略的真实稳健性。  公共评测与协议 技能漂移与共进化稳健性 Agent 评测与可靠性：如何知道真的做对了 CODA 的 RR 分母应是 no-skill 成功任务数吗？ 不是。RR统计no-skill与扰动技能两条件都成功的任务，占全部相同任务的比例。条件成功任务分母会改变定义；输入还须保留所有条件的相同ID集合，拒绝漏任务。 示意：100题中no-skill成功20题、交集10题，RR是10%，而非50%。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-8ba5c0af97c6efeb">CODA 的 RR 分母应是 no-skill 成功任务数吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoda">Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Alibaba Token Hub, Alibaba Group</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。RR统计no-skill与扰动技能两条件都成功的任务，占全部相同任务的比例。条件成功任务分母会改变定义；输入还须保留所有条件的相同ID集合，拒绝漏任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>100题中no-skill成功20题、交集10题，RR是10%，而非50%。</p>
<p class="ar-learning-sources">依据：核心公式、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20845">原论文</a> · <a href="../../../../agent-research/2610.20845-coda/">实现解读</a> · <a href="#qa-8ba5c0af97c6efeb">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ctxgap" data-paper-title="What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports Agent Tencent 2026-10-14 编码 Agent 的最终报告可能“听起来完整”，却不足以让用户恢复真实任务状态。CTXGAP 不用任务完成率替代信息质量，而是从执行记录抽取原子事实，生成有参考答案的探针，在同一问题上比较只读累积报告的观察者、读取完整执行视图的观察者，以及直接询问执行 Agent 的条件。重要事实的类别权重防止“多生成简单问题”稀释遗漏。37 个主任务包含 148 个检查点、4,855 个探针，其中 4,799 个有效；公开文本探针及公开执行材料只是子集。 完整私有执行视图和大规模模型调用不在本轮复现范围：成本过高，不复现（审查 DONE）。本地完成的是官方冻结数值表的 CPU 复算与公开评测协议接口，不是新 Agent 的能力评测。完整私有执行视图和大规模模型调用不在本轮复现范围：成本过高，不复现（审查 DONE）。冻结统计复算：只下载五份固定数值表（约 1.65 MB），逐文件 SHA256 核验。按作者 reproduce_all.py 的统计口径独立组织复算；10,000 次聚类 bootstrap、固定 seed 0，结果与固定版本 data/reproduced_all.json 逐项相同。没有调用模型、没有下载完整轨迹。  公共评测与协议 任务状态可恢复性与报告审计 Agent 评测与可靠性：如何知道真的做对了 CTXGAP 测量的报告信息差距，与任务完成率有什么不同？ 它在同一探针上比较累积报告观察者和完整执行视图观察者，测用户能否恢复真实任务状态。任务可能已完成但报告漏掉关键事实，反之报告详尽也不保证任务成功。 示意：代码已修好，但报告未说某个检查没有运行，用户仍无法准确判断验收状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-ctxgap-b6a0f849" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-47dcbdce30974399">CTXGAP 测量的报告信息差距，与任务完成率有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Actxgap">What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它在同一探针上比较累积报告观察者和完整执行视图观察者，测用户能否恢复真实任务状态。任务可能已完成但报告漏掉关键事实，反之报告详尽也不保证任务成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>代码已修好，但报告未说某个检查没有运行，用户仍无法准确判断验收状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20003">原论文</a> · <a href="../../../../agent-research/2610.20003-ctxgap/">实现解读</a> · <a href="#qa-47dcbdce30974399">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ctxgap" data-paper-title="What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports Agent Tencent 2026-10-14 编码 Agent 的最终报告可能“听起来完整”，却不足以让用户恢复真实任务状态。CTXGAP 不用任务完成率替代信息质量，而是从执行记录抽取原子事实，生成有参考答案的探针，在同一问题上比较只读累积报告的观察者、读取完整执行视图的观察者，以及直接询问执行 Agent 的条件。重要事实的类别权重防止“多生成简单问题”稀释遗漏。37 个主任务包含 148 个检查点、4,855 个探针，其中 4,799 个有效；公开文本探针及公开执行材料只是子集。 完整私有执行视图和大规模模型调用不在本轮复现范围：成本过高，不复现（审查 DONE）。本地完成的是官方冻结数值表的 CPU 复算与公开评测协议接口，不是新 Agent 的能力评测。完整私有执行视图和大规模模型调用不在本轮复现范围：成本过高，不复现（审查 DONE）。冻结统计复算：只下载五份固定数值表（约 1.65 MB），逐文件 SHA256 核验。按作者 reproduce_all.py 的统计口径独立组织复算；10,000 次聚类 bootstrap、固定 seed 0，结果与固定版本 data/reproduced_all.json 逐项相同。没有调用模型、没有下载完整轨迹。  公共评测与协议 任务状态可恢复性与报告审计 Agent 评测与可靠性：如何知道真的做对了 公开执行材料为什么不能重命名为 T_full 来复算完整报告差距？ 原完整视图包含部分不公开推理或记忆证据，公开子集缺这些事实，观察者能力和可回答问题范围会改变。同题配对与重要原子权重用于衡量报告遗漏，仍须区分公共与完整条件；按 task/run 聚类也避免把同任务大量探针当独立样本。 例如某端口只记录在私有记忆里，公开日志没有；用公开日志观察者答不出，不能说它代表原论文完整执行视图的上限。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-823db16c649a2ab8">公开执行材料为什么不能重命名为 T_full 来复算完整报告差距？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Actxgap">What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原完整视图包含部分不公开推理或记忆证据，公开子集缺这些事实，观察者能力和可回答问题范围会改变。同题配对与重要原子权重用于衡量报告遗漏，仍须区分公共与完整条件；按 task/run 聚类也避免把同任务大量探针当独立样本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如某端口只记录在私有记忆里，公开日志没有；用公开日志观察者答不出，不能说它代表原论文完整执行视图的上限。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与统计单位；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20003">原论文</a> · <a href="../../../../agent-research/2610.20003-ctxgap/">实现解读</a> · <a href="#qa-823db16c649a2ab8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ctxgap" data-paper-title="What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports Agent Tencent 2026-10-14 编码 Agent 的最终报告可能“听起来完整”，却不足以让用户恢复真实任务状态。CTXGAP 不用任务完成率替代信息质量，而是从执行记录抽取原子事实，生成有参考答案的探针，在同一问题上比较只读累积报告的观察者、读取完整执行视图的观察者，以及直接询问执行 Agent 的条件。重要事实的类别权重防止“多生成简单问题”稀释遗漏。37 个主任务包含 148 个检查点、4,855 个探针，其中 4,799 个有效；公开文本探针及公开执行材料只是子集。 完整私有执行视图和大规模模型调用不在本轮复现范围：成本过高，不复现（审查 DONE）。本地完成的是官方冻结数值表的 CPU 复算与公开评测协议接口，不是新 Agent 的能力评测。完整私有执行视图和大规模模型调用不在本轮复现范围：成本过高，不复现（审查 DONE）。冻结统计复算：只下载五份固定数值表（约 1.65 MB），逐文件 SHA256 核验。按作者 reproduce_all.py 的统计口径独立组织复算；10,000 次聚类 bootstrap、固定 seed 0，结果与固定版本 data/reproduced_all.json 逐项相同。没有调用模型、没有下载完整轨迹。  公共评测与协议 任务状态可恢复性与报告审计 Agent 评测与可靠性：如何知道真的做对了 CTXGAP 的重要性加权准确率，与把所有探针等权平均有何区别？ 某类别探针越多，不应仅因此压过重要事实更集中的类别。权重以类别重要原子事实数除以探针数，先累加加权分数再归一化；等权平均容易被大量简单或相似问题稀释遗漏。 示意：为一条琐碎日志生成很多题，不应掩盖一个关键验收事实未被报告。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c679357bfb66ed89">CTXGAP 的重要性加权准确率，与把所有探针等权平均有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Actxgap">What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>某类别探针越多，不应仅因此压过重要事实更集中的类别。权重以类别重要原子事实数除以探针数，先累加加权分数再归一化；等权平均容易被大量简单或相似问题稀释遗漏。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>为一条琐碎日志生成很多题，不应掩盖一个关键验收事实未被报告。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与统计单位；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20003">原论文</a> · <a href="../../../../agent-research/2610.20003-ctxgap/">实现解读</a> · <a href="#qa-c679357bfb66ed89">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ctxgap" data-paper-title="What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports Agent Tencent 2026-10-14 编码 Agent 的最终报告可能“听起来完整”，却不足以让用户恢复真实任务状态。CTXGAP 不用任务完成率替代信息质量，而是从执行记录抽取原子事实，生成有参考答案的探针，在同一问题上比较只读累积报告的观察者、读取完整执行视图的观察者，以及直接询问执行 Agent 的条件。重要事实的类别权重防止“多生成简单问题”稀释遗漏。37 个主任务包含 148 个检查点、4,855 个探针，其中 4,799 个有效；公开文本探针及公开执行材料只是子集。 完整私有执行视图和大规模模型调用不在本轮复现范围：成本过高，不复现（审查 DONE）。本地完成的是官方冻结数值表的 CPU 复算与公开评测协议接口，不是新 Agent 的能力评测。完整私有执行视图和大规模模型调用不在本轮复现范围：成本过高，不复现（审查 DONE）。冻结统计复算：只下载五份固定数值表（约 1.65 MB），逐文件 SHA256 核验。按作者 reproduce_all.py 的统计口径独立组织复算；10,000 次聚类 bootstrap、固定 seed 0，结果与固定版本 data/reproduced_all.json 逐项相同。没有调用模型、没有下载完整轨迹。  公共评测与协议 任务状态可恢复性与报告审计 Agent 评测与可靠性：如何知道真的做对了 CTXGAP 的置信区间为什么按 task/run 重采样而不是按探针独立重采样？ 同一任务探针共享执行和报告条件，并非独立样本；需聚类且保持条件配对。类别权重和任务等权汇总也要保留，不能用pooled准确率差替换主任务等权差距。 示意：一个任务生成100个相似探针，不能被当作100个独立任务来缩小区间。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-ef131aa02e4eacc2">CTXGAP 的置信区间为什么按 task/run 重采样而不是按探针独立重采样？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Actxgap">What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Tencent</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同一任务探针共享执行和报告条件，并非独立样本；需聚类且保持条件配对。类别权重和任务等权汇总也要保留，不能用pooled准确率差替换主任务等权差距。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一个任务生成100个相似探针，不能被当作100个独立任务来缩小区间。</p>
<p class="ar-learning-sources">依据：核心公式与统计单位；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.20003">原论文</a> · <a href="../../../../agent-research/2610.20003-ctxgap/">实现解读</a> · <a href="#qa-ef131aa02e4eacc2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autoformbench" data-paper-title="AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics Agent FAIR at Meta 2026-10-13 AutoformBench 不只要求补一个孤立证明，而是让 Agent 在固定 Lean/Mathlib 上构造支撑高级数学命题的定义、辅助引理和证明。341 个任务来自 24 个数学来源，共有 1,155 个需要完成的证明义务；一个任务只有全部义务均通过可信验证才算成功。最容易混淆的是两个不同实验条件：论文排行榜向 Agent 提供非形式化原文（source-present）；公开仓库则发布不含教材摘录/参考证明的 source-free 工作区。 原研究的九类 frontier 模型、341 题长轨迹及教材/工具链准备超出单张 A100/A30 或本地 Mac 的低成本预算，成本过高，不复现（审查 DONE）。本轮真实读取官方任务清单和已有结果，未运行 Lean、Harbor、模型推理或付费 API；本页是 CPU 评测协议接口，不是模型/Agent 能力复现。本轮真实读取官方任务清单和已有结果，未运行 Lean、Harbor、模型推理或付费 API；不提供本地 source-free 成功率，不接入 Evolve 晋级。在项目根目录、已安装项目的 Python 环境中运行：  形式化数学 Agent 评测协议与结果导入 Agent 评测与可靠性：如何知道真的做对了 AutoformBench为什么要求任务内所有证明义务通过？ 高级形式化需定义、辅助引理和最终证明协同成立，单独补一个片段不足。可信Lean/Mathlib验证全部义务才算任务成功，不能按局部通过数替代成功率。 例如主结论过了但依赖引理仍留sorry，整题尚未完成。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-autoformbench-7806e713" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d1e8b44a41b19cb0">AutoformBench为什么要求任务内所有证明义务通过？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautoformbench">AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>高级形式化需定义、辅助引理和最终证明协同成立，单独补一个片段不足。可信Lean/Mathlib验证全部义务才算任务成功，不能按局部通过数替代成功率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如主结论过了但依赖引理仍留sorry，整题尚未完成。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://github.com/facebookresearch/autoformbench/blob/af1aa38fd44e019e566bce0b5a168609a886d8e6/paper.pdf">原论文</a> · <a href="../../../../agent-research/autoformbench/">实现解读</a> · <a href="#qa-d1e8b44a41b19cb0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autoformbench" data-paper-title="AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics Agent FAIR at Meta 2026-10-13 AutoformBench 不只要求补一个孤立证明，而是让 Agent 在固定 Lean/Mathlib 上构造支撑高级数学命题的定义、辅助引理和证明。341 个任务来自 24 个数学来源，共有 1,155 个需要完成的证明义务；一个任务只有全部义务均通过可信验证才算成功。最容易混淆的是两个不同实验条件：论文排行榜向 Agent 提供非形式化原文（source-present）；公开仓库则发布不含教材摘录/参考证明的 source-free 工作区。 原研究的九类 frontier 模型、341 题长轨迹及教材/工具链准备超出单张 A100/A30 或本地 Mac 的低成本预算，成本过高，不复现（审查 DONE）。本轮真实读取官方任务清单和已有结果，未运行 Lean、Harbor、模型推理或付费 API；本页是 CPU 评测协议接口，不是模型/Agent 能力复现。本轮真实读取官方任务清单和已有结果，未运行 Lean、Harbor、模型推理或付费 API；不提供本地 source-free 成功率，不接入 Evolve 晋级。在项目根目录、已安装项目的 Python 环境中运行：  形式化数学 Agent 评测协议与结果导入 Agent 评测与可靠性：如何知道真的做对了 source-present 与 source-free 为什么不能仅凭相同 task ID 直接比较分数？ 可见材料不同会改变形式化难度：原文或参考论证提供定义与思路，公开无来源工作区则要求更多自主构建。两者即使目标同名也不是同一信息条件，所有证明义务还必须一起通过；失败、超预算或基础设施行不能从固定任务分母里静默删掉。 例如同一个高等数学命题，一组能读教材证明、另一组只有 Lean 骨架，成绩差不应直接归因模型强弱，而要先匹配来源条件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-e4b095973d365cfd">source-present 与 source-free 为什么不能仅凭相同 task ID 直接比较分数？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautoformbench">AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可见材料不同会改变形式化难度：原文或参考论证提供定义与思路，公开无来源工作区则要求更多自主构建。两者即使目标同名也不是同一信息条件，所有证明义务还必须一起通过；失败、超预算或基础设施行不能从固定任务分母里静默删掉。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同一个高等数学命题，一组能读教材证明、另一组只有 Lean 骨架，成绩差不应直接归因模型强弱，而要先匹配来源条件。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://github.com/facebookresearch/autoformbench/blob/af1aa38fd44e019e566bce0b5a168609a886d8e6/paper.pdf">原论文</a> · <a href="../../../../agent-research/autoformbench/">实现解读</a> · <a href="#qa-e4b095973d365cfd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autoformbench" data-paper-title="AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics Agent FAIR at Meta 2026-10-13 AutoformBench 不只要求补一个孤立证明，而是让 Agent 在固定 Lean/Mathlib 上构造支撑高级数学命题的定义、辅助引理和证明。341 个任务来自 24 个数学来源，共有 1,155 个需要完成的证明义务；一个任务只有全部义务均通过可信验证才算成功。最容易混淆的是两个不同实验条件：论文排行榜向 Agent 提供非形式化原文（source-present）；公开仓库则发布不含教材摘录/参考证明的 source-free 工作区。 原研究的九类 frontier 模型、341 题长轨迹及教材/工具链准备超出单张 A100/A30 或本地 Mac 的低成本预算，成本过高，不复现（审查 DONE）。本轮真实读取官方任务清单和已有结果，未运行 Lean、Harbor、模型推理或付费 API；本页是 CPU 评测协议接口，不是模型/Agent 能力复现。本轮真实读取官方任务清单和已有结果，未运行 Lean、Harbor、模型推理或付费 API；不提供本地 source-free 成功率，不接入 Evolve 晋级。在项目根目录、已安装项目的 Python 环境中运行：  形式化数学 Agent 评测协议与结果导入 Agent 评测与可靠性：如何知道真的做对了 AutoformBench与给定全部定义后只补一个孤立Lean证明，有何任务范围区别？ 这里还要求构造支撑命题的定义与辅助引理，并完成任务内全部证明义务；孤立证明补全通常已固定更多形式化上下文。两者都可能通过Lean验证，但需要自主完成的形式化工作不同，不能只因同用验证器就合并成功率。 教学例子：若缺少一个适当定义，Agent需先形式化该定义并证明辅助引理；只填最后一个by证明块没有完成整项任务。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9943b69a42b057f3">AutoformBench与给定全部定义后只补一个孤立Lean证明，有何任务范围区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautoformbench">AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里还要求构造支撑命题的定义与辅助引理，并完成任务内全部证明义务；孤立证明补全通常已固定更多形式化上下文。两者都可能通过Lean验证，但需要自主完成的形式化工作不同，不能只因同用验证器就合并成功率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>若缺少一个适当定义，Agent需先形式化该定义并证明辅助引理；只填最后一个by证明块没有完成整项任务。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://github.com/facebookresearch/autoformbench/blob/af1aa38fd44e019e566bce0b5a168609a886d8e6/paper.pdf">原论文</a> · <a href="../../../../agent-research/autoformbench/">实现解读</a> · <a href="#qa-9943b69a42b057f3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:autoformbench" data-paper-title="AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics Agent FAIR at Meta 2026-10-13 AutoformBench 不只要求补一个孤立证明，而是让 Agent 在固定 Lean/Mathlib 上构造支撑高级数学命题的定义、辅助引理和证明。341 个任务来自 24 个数学来源，共有 1,155 个需要完成的证明义务；一个任务只有全部义务均通过可信验证才算成功。最容易混淆的是两个不同实验条件：论文排行榜向 Agent 提供非形式化原文（source-present）；公开仓库则发布不含教材摘录/参考证明的 source-free 工作区。 原研究的九类 frontier 模型、341 题长轨迹及教材/工具链准备超出单张 A100/A30 或本地 Mac 的低成本预算，成本过高，不复现（审查 DONE）。本轮真实读取官方任务清单和已有结果，未运行 Lean、Harbor、模型推理或付费 API；本页是 CPU 评测协议接口，不是模型/Agent 能力复现。本轮真实读取官方任务清单和已有结果，未运行 Lean、Harbor、模型推理或付费 API；不提供本地 source-free 成功率，不接入 Evolve 晋级。在项目根目录、已安装项目的 Python 环境中运行：  形式化数学 Agent 评测协议与结果导入 Agent 评测与可靠性：如何知道真的做对了 AutoformBench接口能把失败、超预算或基础设施错行删掉吗？ 不能，要保留完整固定任务集合及实际CSV成本，名义上限不等于统一实花。接口导入已产生verdict不代表本次真实Harbor运行，未执行就需明确计划状态。 例如只统计成功启动的任务，会把环境失败从分母洗掉并抬高成绩。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-3c1b69021b889269">AutoformBench接口能把失败、超预算或基础设施错行删掉吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aautoformbench">AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，要保留完整固定任务集合及实际CSV成本，名义上限不等于统一实花。接口导入已产生verdict不代表本次真实Harbor运行，未执行就需明确计划状态。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只统计成功启动的任务，会把环境失败从分母洗掉并抬高成绩。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://github.com/facebookresearch/autoformbench/blob/af1aa38fd44e019e566bce0b5a168609a886d8e6/paper.pdf">原论文</a> · <a href="../../../../agent-research/autoformbench/">实现解读</a> · <a href="#qa-3c1b69021b889269">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:clasharness" data-paper-title="CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline Agent Google / Emory University（共同署名） 2026-10-13 多个 Agent 共享文件、网页和任务上下文时，其他参与者可能给出错误事实、过期状态或矛盾指令。CLASHarness 要求被测 Agent 依据可见环境核对信息并完成任务，而不只是识别一段文字冲突。核心不是随机插入干扰，而是先确定任务真实状态，再用参考执行验证任务确实可解。八阶段管线先生成共享世界、角色规则与多轮场景；在每轮固定真实值，构造参考执行计划并在隔离环境实际执行，从轨迹效果编译确定性和语义检查，最后做一致性、视觉和渲染验收。前轮状态带入后轮，要求区分应遵循的用户意图与有冲突的 peer 消息。 完整原实验成本过高，不复现（审查 DONE）。缺清单时只报 observed-check 诊断，完整成功值为 null。本地提供固定版本参考资料导入、审计校验和外部 verdict 聚合接口。没有运行计算机使用 Agent，也没有重建完整多轮环境；官方分数不当作本地能力。完整原实验成本过高，不复现（审查 DONE）。固定参考导入：四个官方 JSON，合计不足 0.6 MB，固定 commit 与 SHA256；重算标签计数、306 项保守并集、死轮次数和精选行完整性。没有下载默认 8.5 GB 任务/轨迹包，没有运行模型。  公共评测与协议 多 Agent 冲突与计算机使用 Agent 评测与可靠性：如何知道真的做对了 CLASHarness 为什么先执行参考计划，再让被测 Agent 处理冲突消息？ 参考执行用于确认任务在固定真实状态下确实可解，并从执行效果编译检查。否则被测失败可能来自场景自身矛盾，而不是处理peer错误事实、过期状态或冲突指令的能力。 示意：别人声称文件已更新，评测仍需先确定文件真实状态和可完成目标。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-clasharness-f0eec5c3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-5739ffdb20a3b64a">CLASHarness 为什么先执行参考计划，再让被测 Agent 处理冲突消息？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aclasharness">CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Emory University（共同署名）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>参考执行用于确认任务在固定真实状态下确实可解，并从执行效果编译检查。否则被测失败可能来自场景自身矛盾，而不是处理peer错误事实、过期状态或冲突指令的能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>别人声称文件已更新，评测仍需先确定文件真实状态和可完成目标。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19128">原论文</a> · <a href="../../../../agent-research/2610.19128-clasharness/">实现解读</a> · <a href="#qa-5739ffdb20a3b64a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:clasharness" data-paper-title="CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline Agent Google / Emory University（共同署名） 2026-10-13 多个 Agent 共享文件、网页和任务上下文时，其他参与者可能给出错误事实、过期状态或矛盾指令。CLASHarness 要求被测 Agent 依据可见环境核对信息并完成任务，而不只是识别一段文字冲突。核心不是随机插入干扰，而是先确定任务真实状态，再用参考执行验证任务确实可解。八阶段管线先生成共享世界、角色规则与多轮场景；在每轮固定真实值，构造参考执行计划并在隔离环境实际执行，从轨迹效果编译确定性和语义检查，最后做一致性、视觉和渲染验收。前轮状态带入后轮，要求区分应遵循的用户意图与有冲突的 peer 消息。 完整原实验成本过高，不复现（审查 DONE）。缺清单时只报 observed-check 诊断，完整成功值为 null。本地提供固定版本参考资料导入、审计校验和外部 verdict 聚合接口。没有运行计算机使用 Agent，也没有重建完整多轮环境；官方分数不当作本地能力。完整原实验成本过高，不复现（审查 DONE）。固定参考导入：四个官方 JSON，合计不足 0.6 MB，固定 commit 与 SHA256；重算标签计数、306 项保守并集、死轮次数和精选行完整性。没有下载默认 8.5 GB 任务/轨迹包，没有运行模型。  公共评测与协议 多 Agent 冲突与计算机使用 Agent 评测与可靠性：如何知道真的做对了 为什么生成冲突场景前要固定真实状态并执行参考计划证明任务可解？ 否则失败可能只是场景自相矛盾或界面不可操作，而非 Agent 不会处理 peer 冲突。可执行参考建立真实状态、允许目标和检查义务，再检验被测者能否依据环境完成；空 required 集合或缺失 verdict 不能自动算成功，公平性调整也应预先声明。 例如 peer 声称文件已删除，真实文件仍在且参考操作可完成任务；这样才可测 Agent 是否核对环境，而非面对无解场景。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8c034b18ddbd1802">为什么生成冲突场景前要固定真实状态并执行参考计划证明任务可解？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aclasharness">CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Emory University（共同署名）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>否则失败可能只是场景自相矛盾或界面不可操作，而非 Agent 不会处理 peer 冲突。可执行参考建立真实状态、允许目标和检查义务，再检验被测者能否依据环境完成；空 required 集合或缺失 verdict 不能自动算成功，公平性调整也应预先声明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 peer 声称文件已删除，真实文件仍在且参考操作可完成任务；这样才可测 Agent 是否核对环境，而非面对无解场景。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式与公平性口径；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19128">原论文</a> · <a href="../../../../agent-research/2610.19128-clasharness/">实现解读</a> · <a href="#qa-8c034b18ddbd1802">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:clasharness" data-paper-title="CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline Agent Google / Emory University（共同署名） 2026-10-13 多个 Agent 共享文件、网页和任务上下文时，其他参与者可能给出错误事实、过期状态或矛盾指令。CLASHarness 要求被测 Agent 依据可见环境核对信息并完成任务，而不只是识别一段文字冲突。核心不是随机插入干扰，而是先确定任务真实状态，再用参考执行验证任务确实可解。八阶段管线先生成共享世界、角色规则与多轮场景；在每轮固定真实值，构造参考执行计划并在隔离环境实际执行，从轨迹效果编译确定性和语义检查，最后做一致性、视觉和渲染验收。前轮状态带入后轮，要求区分应遵循的用户意图与有冲突的 peer 消息。 完整原实验成本过高，不复现（审查 DONE）。缺清单时只报 observed-check 诊断，完整成功值为 null。本地提供固定版本参考资料导入、审计校验和外部 verdict 聚合接口。没有运行计算机使用 Agent，也没有重建完整多轮环境；官方分数不当作本地能力。完整原实验成本过高，不复现（审查 DONE）。固定参考导入：四个官方 JSON，合计不足 0.6 MB，固定 commit 与 SHA256；重算标签计数、306 项保守并集、死轮次数和精选行完整性。没有下载默认 8.5 GB 任务/轨迹包，没有运行模型。  公共评测与协议 多 Agent 冲突与计算机使用 Agent 评测与可靠性：如何知道真的做对了 CLASHarness 的完整成功与部分检查通过率，为何需要分别报告？ 完整成功要求非空required清单已验证且每项通过，部分比例只反映其中多少检查通过。没有检查不能按空合取宣布成功，只有部分verdict也不足以证明整任务通过。 示意：4项必需检查过了3项，部分比例75%，完整成功仍为否。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bf253b82e67b2178">CLASHarness 的完整成功与部分检查通过率，为何需要分别报告？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aclasharness">CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Emory University（共同署名）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整成功要求非空required清单已验证且每项通过，部分比例只反映其中多少检查通过。没有检查不能按空合取宣布成功，只有部分verdict也不足以证明整任务通过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>4项必需检查过了3项，部分比例75%，完整成功仍为否。</p>
<p class="ar-learning-sources">依据：核心公式与公平性口径；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19128">原论文</a> · <a href="../../../../agent-research/2610.19128-clasharness/">实现解读</a> · <a href="#qa-bf253b82e67b2178">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:clasharness" data-paper-title="CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline Agent Google / Emory University（共同署名） 2026-10-13 多个 Agent 共享文件、网页和任务上下文时，其他参与者可能给出错误事实、过期状态或矛盾指令。CLASHarness 要求被测 Agent 依据可见环境核对信息并完成任务，而不只是识别一段文字冲突。核心不是随机插入干扰，而是先确定任务真实状态，再用参考执行验证任务确实可解。八阶段管线先生成共享世界、角色规则与多轮场景；在每轮固定真实值，构造参考执行计划并在隔离环境实际执行，从轨迹效果编译确定性和语义检查，最后做一致性、视觉和渲染验收。前轮状态带入后轮，要求区分应遵循的用户意图与有冲突的 peer 消息。 完整原实验成本过高，不复现（审查 DONE）。缺清单时只报 observed-check 诊断，完整成功值为 null。本地提供固定版本参考资料导入、审计校验和外部 verdict 聚合接口。没有运行计算机使用 Agent，也没有重建完整多轮环境；官方分数不当作本地能力。完整原实验成本过高，不复现（审查 DONE）。固定参考导入：四个官方 JSON，合计不足 0.6 MB，固定 commit 与 SHA256；重算标签计数、306 项保守并集、死轮次数和精选行完整性。没有下载默认 8.5 GB 任务/轨迹包，没有运行模型。  公共评测与协议 多 Agent 冲突与计算机使用 Agent 评测与可靠性：如何知道真的做对了 CLASHarness 公平性降级检查时，为什么不能按列表位置关联记录？ 策略用原始task_id/check_index标识，将指定required项改为diagnostic；不同判定类别要取集合并集。列表重排或重复标签若按位置处理，会错误删除检查或重复计算。 示意：同一check同时属于两种争议类别，也只能在降级集合中出现一次。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-751859fe4985dd0e">CLASHarness 公平性降级检查时，为什么不能按列表位置关联记录？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aclasharness">CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google / Emory University（共同署名）</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>策略用原始task_id/check_index标识，将指定required项改为diagnostic；不同判定类别要取集合并集。列表重排或重复标签若按位置处理，会错误删除检查或重复计算。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一check同时属于两种争议类别，也只能在降级集合中出现一次。</p>
<p class="ar-learning-sources">依据：核心公式与公平性口径；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.19128">原论文</a> · <a href="../../../../agent-research/2610.19128-clasharness/">实现解读</a> · <a href="#qa-751859fe4985dd0e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ontrack" data-paper-title="OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport Agent Cribl AI 2026-10-08 Agent 最终失败时，单个答案分数解释不了中间发生了什么。OnTrack 把事件组织成带依赖边的图，将当前执行前缀和成功参考轨迹作非平衡结构化对齐；无参考时则明确退化为循环、重试和信息停滞检测。 未运行官方 SWE-bench 容器或重新生成 Agent 轨迹；本地实现是公开日志回放监控，不执行日志命令，也不是 Agent 解题成功率或生产安全认证。运行器下载固定版本的公开 sailplane/swe-agent-trajs（约 92 MB）和 all-MiniLM-L6-v2。嵌入和监控均为 CPU 路径，无需 GPU。轨迹里的命令始终作为不可信文本，不会执行。缓存默认在 .cache/ontrack-public。  Agent 安全 实时轨迹监控与非平衡最优传输 Agent 评测与可靠性：如何知道真的做对了 OnTrack 为什么将轨迹建成依赖图，而不只比较动作文字？ 动作先后与产物依赖共同决定是否偏离任务，独立分支可能有不同合法顺序。结构化非平衡对齐允许前缀与参考不完全匹配；没有参考时只能明确退化为循环、重试和停滞信号。 示意：先准备两个互不依赖的文件，交换顺序不应仅因索引不同就被判偏离。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-ontrack-56d9bc62" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-23e3166f678480f8">OnTrack 为什么将轨迹建成依赖图，而不只比较动作文字？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aontrack">OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cribl AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>动作先后与产物依赖共同决定是否偏离任务，独立分支可能有不同合法顺序。结构化非平衡对齐允许前缀与参考不完全匹配；没有参考时只能明确退化为循环、重试和停滞信号。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先准备两个互不依赖的文件，交换顺序不应仅因索引不同就被判偏离。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12375">原论文</a> · <a href="../../../../agent-research/2610.12375-ontrack/">实现解读</a> · <a href="#qa-23e3166f678480f8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ontrack" data-paper-title="OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport Agent Cribl AI 2026-10-08 Agent 最终失败时，单个答案分数解释不了中间发生了什么。OnTrack 把事件组织成带依赖边的图，将当前执行前缀和成功参考轨迹作非平衡结构化对齐；无参考时则明确退化为循环、重试和信息停滞检测。 未运行官方 SWE-bench 容器或重新生成 Agent 轨迹；本地实现是公开日志回放监控，不执行日志命令，也不是 Agent 解题成功率或生产安全认证。运行器下载固定版本的公开 sailplane/swe-agent-trajs（约 92 MB）和 all-MiniLM-L6-v2。嵌入和监控均为 CPU 路径，无需 GPU。轨迹里的命令始终作为不可信文本，不会执行。缓存默认在 .cache/ontrack-public。  Agent 安全 实时轨迹监控与非平衡最优传输 Agent 评测与可靠性：如何知道真的做对了 事件不断增加时，为什么不把旧前缀节点质量每次改成 1/t？ 重缩放会让历史节点的权重仅因来了新事件而变化，混淆实际对齐进展与归一化效应。固定前缀质量、流式 warm-start 和结构耦合保留时间比较语义；准备干预时还要扩大求解预算重判，不可逆动作门不能依赖过期缓存前沿。 例如新增一次日志读取不应自动削弱此前关键编辑的质量；否则监控分数变化可能只是分母改变，而非行为真的偏离。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-655da0c786f78c79">事件不断增加时，为什么不把旧前缀节点质量每次改成 1/t？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aontrack">OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cribl AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>重缩放会让历史节点的权重仅因来了新事件而变化，混淆实际对齐进展与归一化效应。固定前缀质量、流式 warm-start 和结构耦合保留时间比较语义；准备干预时还要扩大求解预算重判，不可逆动作门不能依赖过期缓存前沿。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新增一次日志读取不应自动削弱此前关键编辑的质量；否则监控分数变化可能只是分母改变，而非行为真的偏离。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12375">原论文</a> · <a href="../../../../agent-research/2610.12375-ontrack/">实现解读</a> · <a href="#qa-655da0c786f78c79">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ontrack" data-paper-title="OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport Agent Cribl AI 2026-10-08 Agent 最终失败时，单个答案分数解释不了中间发生了什么。OnTrack 把事件组织成带依赖边的图，将当前执行前缀和成功参考轨迹作非平衡结构化对齐；无参考时则明确退化为循环、重试和信息停滞检测。 未运行官方 SWE-bench 容器或重新生成 Agent 轨迹；本地实现是公开日志回放监控，不执行日志命令，也不是 Agent 解题成功率或生产安全认证。运行器下载固定版本的公开 sailplane/swe-agent-trajs（约 92 MB）和 all-MiniLM-L6-v2。嵌入和监控均为 CPU 路径，无需 GPU。轨迹里的命令始终作为不可信文本，不会执行。缓存默认在 .cache/ontrack-public。  Agent 安全 实时轨迹监控与非平衡最优传输 Agent 评测与可靠性：如何知道真的做对了 OnTrack 的早期探索宽限与结束时最终对齐，为什么不能用完全相同权重？ 在线新节点有年龄折扣并受前沿掩码约束，避免过早惩罚探索；终结时冷启动并移除这两类权重，检查完整轨迹。把在线宽限保留到最终评分会掩盖未解决偏离。 示意：刚创建的临时产物可有探索宽限，但任务结束仍未被使用时需要完整审查。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-d5d972834c027596">OnTrack 的早期探索宽限与结束时最终对齐，为什么不能用完全相同权重？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aontrack">OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cribl AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>在线新节点有年龄折扣并受前沿掩码约束，避免过早惩罚探索；终结时冷启动并移除这两类权重，检查完整轨迹。把在线宽限保留到最终评分会掩盖未解决偏离。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>刚创建的临时产物可有探索宽限，但任务结束仍未被使用时需要完整审查。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12375">原论文</a> · <a href="../../../../agent-research/2610.12375-ontrack/">实现解读</a> · <a href="#qa-d5d972834c027596">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:ontrack" data-paper-title="OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport Agent Cribl AI 2026-10-08 Agent 最终失败时，单个答案分数解释不了中间发生了什么。OnTrack 把事件组织成带依赖边的图，将当前执行前缀和成功参考轨迹作非平衡结构化对齐；无参考时则明确退化为循环、重试和信息停滞检测。 未运行官方 SWE-bench 容器或重新生成 Agent 轨迹；本地实现是公开日志回放监控，不执行日志命令，也不是 Agent 解题成功率或生产安全认证。运行器下载固定版本的公开 sailplane/swe-agent-trajs（约 92 MB）和 all-MiniLM-L6-v2。嵌入和监控均为 CPU 路径，无需 GPU。轨迹里的命令始终作为不可信文本，不会执行。缓存默认在 .cache/ontrack-public。  Agent 安全 实时轨迹监控与非平衡最优传输 Agent 评测与可靠性：如何知道真的做对了 OnTrack 每来一个事件，能把已有节点质量从 1/m 重设为 1/t 吗？ 不能。代理节点按固定前缀质量1/m_bar分配，逐步重缩放会改变旧节点质量和泄漏口径。不可逆动作还需在执行前用当前coupling重算前沿；planner参考仅能告警，不能自动停机。 示意：新增一个无关事件不应仅因分母变化，让所有旧事件的质量被动下降。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cba62001fc682760">OnTrack 每来一个事件，能把已有节点质量从 1/m 重设为 1/t 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aontrack">OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Cribl AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。代理节点按固定前缀质量1/m_bar分配，逐步重缩放会改变旧节点质量和泄漏口径。不可逆动作还需在执行前用当前coupling重算前沿；planner参考仅能告警，不能自动停机。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>新增一个无关事件不应仅因分母变化，让所有旧事件的质量被动下降。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12375">原论文</a> · <a href="../../../../agent-research/2610.12375-ontrack/">实现解读</a> · <a href="#qa-cba62001fc682760">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:option-channel-attack" data-paper-title="One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails Agent University of Southern California 2026-10-08 类型化模型对调用方给定的选项输出概率，但选项名字本身也进入模型输入。保持动作、可信策略定义不变，仅把允许选项换成误导性标签，就可能让本来正确的拒绝变成放行。论文把危险的 fail-open 与妨碍使用的 fail-closed 分开评价。 当前原始报告和归档协议均明确为 L1 合成守门诊断。真实 Laya checkpoint 的安全机制诊断，不是 Agent 任务成功率或生产安全认证。六种合成策略，每种校准/评测各 24 条，校准 seed=42、评测 seed=43；只在校准集从 escalate/deny/stop/lantern 选标签。A100 上运行公开 Laya checkpoint。没有调用真实外部工具，也没有执行被测动作。  Agent 安全 类型化守门模型 Agent 评测与可靠性：如何知道真的做对了 Option-Channel Attack 为什么只改选项标签也可能改变守门结果？ 类型化输出的候选名称同时是模型输入，误导标签会影响模型如何将固定动作映射到允许或拒绝。攻击保持动作与可信策略定义不变，暴露的是选项命名通道的脆弱性。 示意：允许和拒绝的实际含义没变，但调用方提供的名称可能诱导模型选错对应动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-option-channel-attack-6cce967b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-33342ffea93fc28c">Option-Channel Attack 为什么只改选项标签也可能改变守门结果？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aoption-channel-attack">One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>类型化输出的候选名称同时是模型输入，误导标签会影响模型如何将固定动作映射到允许或拒绝。攻击保持动作与可信策略定义不变，暴露的是选项命名通道的脆弱性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>允许和拒绝的实际含义没变，但调用方提供的名称可能诱导模型选错对应动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12292">原论文</a> · <a href="../../../../agent-research/2610.12292-option-channel-attack/">实现解读</a> · <a href="#qa-33342ffea93fc28c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:option-channel-attack" data-paper-title="One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails Agent University of Southern California 2026-10-08 类型化模型对调用方给定的选项输出概率，但选项名字本身也进入模型输入。保持动作、可信策略定义不变，仅把允许选项换成误导性标签，就可能让本来正确的拒绝变成放行。论文把危险的 fail-open 与妨碍使用的 fail-closed 分开评价。 当前原始报告和归档协议均明确为 L1 合成守门诊断。真实 Laya checkpoint 的安全机制诊断，不是 Agent 任务成功率或生产安全认证。六种合成策略，每种校准/评测各 24 条，校准 seed=42、评测 seed=43；只在校准集从 escalate/deny/stop/lantern 选标签。A100 上运行公开 Laya checkpoint。没有调用真实外部工具，也没有执行被测动作。  Agent 安全 类型化守门模型 Agent 评测与可靠性：如何知道真的做对了 动作和可信政策不变，只改选项标签，为什么仍可能改变 guard 的放行决定？ 标签同样进入模型输入，语义暗示会影响类型化输出读出，即使底层动作没变。评测要把危险误放行与无害误拒绝分开，并在干净输入正确拒绝的禁止集合上算条件攻击率；分母为空应未定义，不能记零来假装防御完美。 例如禁止动作仍是同一调用，却把“拒绝”选项改成误导性名称；模型可能因标签理解变化选错，但不代表政策本身改变。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7e849af5852a4fa5">动作和可信政策不变，只改选项标签，为什么仍可能改变 guard 的放行决定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aoption-channel-attack">One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>标签同样进入模型输入，语义暗示会影响类型化输出读出，即使底层动作没变。评测要把危险误放行与无害误拒绝分开，并在干净输入正确拒绝的禁止集合上算条件攻击率；分母为空应未定义，不能记零来假装防御完美。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如禁止动作仍是同一调用，却把“拒绝”选项改成误导性名称；模型可能因标签理解变化选错，但不代表政策本身改变。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12292">原论文</a> · <a href="../../../../agent-research/2610.12292-option-channel-attack/">实现解读</a> · <a href="#qa-7e849af5852a4fa5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:option-channel-attack" data-paper-title="One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails Agent University of Southern California 2026-10-08 类型化模型对调用方给定的选项输出概率，但选项名字本身也进入模型输入。保持动作、可信策略定义不变，仅把允许选项换成误导性标签，就可能让本来正确的拒绝变成放行。论文把危险的 fail-open 与妨碍使用的 fail-closed 分开评价。 当前原始报告和归档协议均明确为 L1 合成守门诊断。真实 Laya checkpoint 的安全机制诊断，不是 Agent 任务成功率或生产安全认证。六种合成策略，每种校准/评测各 24 条，校准 seed=42、评测 seed=43；只在校准集从 escalate/deny/stop/lantern 选标签。A100 上运行公开 Laya checkpoint。没有调用真实外部工具，也没有执行被测动作。  Agent 安全 类型化守门模型 Agent 评测与可靠性：如何知道真的做对了 fail-open 与 fail-closed 为什么不能合并成一个安全准确率？ fail-open放行本应禁止的动作，fail-closed拒绝本应允许的动作，风险和可用性方向不同。条件攻击成功率还只看原本干净输入正确拒绝的集合，不能代替全体错误率。 示意：把所有动作都拒绝可能减少危险放行，却会让合法任务无法使用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-1c21f0da9acb53da">fail-open 与 fail-closed 为什么不能合并成一个安全准确率？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aoption-channel-attack">One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>fail-open放行本应禁止的动作，fail-closed拒绝本应允许的动作，风险和可用性方向不同。条件攻击成功率还只看原本干净输入正确拒绝的集合，不能代替全体错误率。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把所有动作都拒绝可能减少危险放行，却会让合法任务无法使用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12292">原论文</a> · <a href="../../../../agent-research/2610.12292-option-channel-attack/">实现解读</a> · <a href="#qa-1c21f0da9acb53da">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:option-channel-attack" data-paper-title="One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails Agent University of Southern California 2026-10-08 类型化模型对调用方给定的选项输出概率，但选项名字本身也进入模型输入。保持动作、可信策略定义不变，仅把允许选项换成误导性标签，就可能让本来正确的拒绝变成放行。论文把危险的 fail-open 与妨碍使用的 fail-closed 分开评价。 当前原始报告和归档协议均明确为 L1 合成守门诊断。真实 Laya checkpoint 的安全机制诊断，不是 Agent 任务成功率或生产安全认证。六种合成策略，每种校准/评测各 24 条，校准 seed=42、评测 seed=43；只在校准集从 escalate/deny/stop/lantern 选标签。A100 上运行公开 Laya checkpoint。没有调用真实外部工具，也没有执行被测动作。  Agent 安全 类型化守门模型 Agent 评测与可靠性：如何知道真的做对了 干净输入没有一个正确拒绝样本时，条件 ASR 应记多少？ 条件分母为空，ASR未定义，不能写0或1。paired bootstrap每次重采样也要重算条件分母；攻击标签先在校准集选择，再在独立评测集测量，避免挑结果。 示意：原来就全部错误放行的模型，没有“从正确拒绝变成放行”的可用条件样本。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c4bff9ac6252201f">干净输入没有一个正确拒绝样本时，条件 ASR 应记多少？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aoption-channel-attack">One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Southern California</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>条件分母为空，ASR未定义，不能写0或1。paired bootstrap每次重采样也要重算条件分母；攻击标签先在校准集选择，再在独立评测集测量，避免挑结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>原来就全部错误放行的模型，没有“从正确拒绝变成放行”的可用条件样本。</p>
<p class="ar-learning-sources">依据：核心公式、代码映射与复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.12292">原论文</a> · <a href="../../../../agent-research/2610.12292-option-channel-attack/">实现解读</a> · <a href="#qa-c4bff9ac6252201f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:specguard" data-paper-title="SpecGuard: Proving a Task Is Broken Before the Agent Cheats" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SpecGuard: Proving a Task Is Broken Before the Agent Cheats Agent MATS 2026-10-06 当测试意外或恶意违背任务描述，coding agent 可能修改测试或硬编码结果，而不是报告任务不可满足。SpecGuard 在编码前拆开两个信息来源：SpecAgent 只看描述与源码、完全不看测试；TestAgent 独立翻译测试；Certifier 对齐两侧语义，由 Lean kernel 核验冲突证明。不能忠实表达或对齐时允许 inconclusive。论文 §3–4 完整多模型全基准实验：成本过高，不复现（审查 DONE）；忠实缩小的 component_only / L1 micro-suite。保留真实模型生成与真实 Lean kernel，不用手写规范或固定模型输出替代核心过程。完整多模型全基准实验：成本过高，不复现（审查 DONE）；这不等于小范围实验已取得论文效果。先准备已有的小型 coding checkpoint 和官方 Lean 4.24.0 二进制；不需要 Mathlib、REPL、Docker 或训练数据。  Agent 安全 形式化验证 任务规范与测试冲突 Agent 评测与可靠性：如何知道真的做对了 SpecGuard 为什么不让 SpecAgent 看测试？ 测试可能与可信任务描述冲突；若意图规范抄自测试，后续证明只会确认测试自身。SpecAgent只看描述与源码，TestAgent独立翻译测试，再连接两侧语义并由Lean检查冲突。 示意：描述要求加一，测试却要求2变4，不能把“2变4”先写进任务规范。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-specguard-31696f7e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7b4123e304451411">SpecGuard 为什么不让 SpecAgent 看测试？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspecguard">SpecGuard: Proving a Task Is Broken Before the Agent Cheats</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MATS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>测试可能与可信任务描述冲突；若意图规范抄自测试，后续证明只会确认测试自身。SpecAgent只看描述与源码，TestAgent独立翻译测试，再连接两侧语义并由Lean检查冲突。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>描述要求加一，测试却要求2变4，不能把“2变4”先写进任务规范。</p>
<p class="ar-learning-sources">依据：背景与主要改动、数据协议；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.09159">原论文</a> · <a href="../../../../agent-research/2610.09159-specguard/">实现解读</a> · <a href="#qa-7b4123e304451411">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:specguard" data-paper-title="SpecGuard: Proving a Task Is Broken Before the Agent Cheats" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SpecGuard: Proving a Task Is Broken Before the Agent Cheats Agent MATS 2026-10-06 当测试意外或恶意违背任务描述，coding agent 可能修改测试或硬编码结果，而不是报告任务不可满足。SpecGuard 在编码前拆开两个信息来源：SpecAgent 只看描述与源码、完全不看测试；TestAgent 独立翻译测试；Certifier 对齐两侧语义，由 Lean kernel 核验冲突证明。不能忠实表达或对齐时允许 inconclusive。论文 §3–4 完整多模型全基准实验：成本过高，不复现（审查 DONE）；忠实缩小的 component_only / L1 micro-suite。保留真实模型生成与真实 Lean kernel，不用手写规范或固定模型输出替代核心过程。完整多模型全基准实验：成本过高，不复现（审查 DONE）；这不等于小范围实验已取得论文效果。先准备已有的小型 coding checkpoint 和官方 Lean 4.24.0 二进制；不需要 Mathlib、REPL、Docker 或训练数据。  Agent 安全 形式化验证 任务规范与测试冲突 Agent 评测与可靠性：如何知道真的做对了 为什么 SpecAgent 完全不看测试，Lean 证明通过后仍可能是 inconclusive？ 不看测试让意图规范独立于可能错误或恶意的测试要求，Certifier 再检查两侧冲突。但形式证明只针对翻译和 connector 表达，若无法忠实对齐自然语言语义，就不能把 kernel 通过解释为原任务已被证明损坏，必须保留未确定结果。 例如题意要求排序，测试却要求反序，可分别形式化后证明冲突；若“稳定排序”含义翻译不清，不能仅凭一个有限证明就下结论。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-837e8a2527eb3a28">为什么 SpecAgent 完全不看测试，Lean 证明通过后仍可能是 inconclusive？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspecguard">SpecGuard: Proving a Task Is Broken Before the Agent Cheats</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MATS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不看测试让意图规范独立于可能错误或恶意的测试要求，Certifier 再检查两侧冲突。但形式证明只针对翻译和 connector 表达，若无法忠实对齐自然语言语义，就不能把 kernel 通过解释为原任务已被证明损坏，必须保留未确定结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如题意要求排序，测试却要求反序，可分别形式化后证明冲突；若“稳定排序”含义翻译不清，不能仅凭一个有限证明就下结论。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.09159">原论文</a> · <a href="../../../../agent-research/2610.09159-specguard/">实现解读</a> · <a href="#qa-837e8a2527eb3a28">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:specguard" data-paper-title="SpecGuard: Proving a Task Is Broken Before the Agent Cheats" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SpecGuard: Proving a Task Is Broken Before the Agent Cheats Agent MATS 2026-10-06 当测试意外或恶意违背任务描述，coding agent 可能修改测试或硬编码结果，而不是报告任务不可满足。SpecGuard 在编码前拆开两个信息来源：SpecAgent 只看描述与源码、完全不看测试；TestAgent 独立翻译测试；Certifier 对齐两侧语义，由 Lean kernel 核验冲突证明。不能忠实表达或对齐时允许 inconclusive。论文 §3–4 完整多模型全基准实验：成本过高，不复现（审查 DONE）；忠实缩小的 component_only / L1 micro-suite。保留真实模型生成与真实 Lean kernel，不用手写规范或固定模型输出替代核心过程。完整多模型全基准实验：成本过高，不复现（审查 DONE）；这不等于小范围实验已取得论文效果。先准备已有的小型 coding checkpoint 和官方 Lean 4.24.0 二进制；不需要 Mathlib、REPL、Docker 或训练数据。  Agent 安全 形式化验证 任务规范与测试冲突 Agent 评测与可靠性：如何知道真的做对了 Lean kernel 验证了冲突证书，是否等于证明原始自然语言任务必然冲突？ 证书证明生成的规范与测试约束之间没有共同实现，但不自动证明两份翻译忠实。语义连接、意图提取错误仍会影响结论，无法表达或对齐时应允许inconclusive。 示意：把“加一”误译成“加二”后获得的形式证明，不能替原任务背书。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-55dce45e534cd4ad">Lean kernel 验证了冲突证书，是否等于证明原始自然语言任务必然冲突？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspecguard">SpecGuard: Proving a Task Is Broken Before the Agent Cheats</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MATS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>证书证明生成的规范与测试约束之间没有共同实现，但不自动证明两份翻译忠实。语义连接、意图提取错误仍会影响结论，无法表达或对齐时应允许inconclusive。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>把“加一”误译成“加二”后获得的形式证明，不能替原任务背书。</p>
<p class="ar-learning-sources">依据：核心公式、结果与验收边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.09159">原论文</a> · <a href="../../../../agent-research/2610.09159-specguard/">实现解读</a> · <a href="#qa-55dce45e534cd4ad">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:specguard" data-paper-title="SpecGuard: Proving a Task Is Broken Before the Agent Cheats" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SpecGuard: Proving a Task Is Broken Before the Agent Cheats Agent MATS 2026-10-06 当测试意外或恶意违背任务描述，coding agent 可能修改测试或硬编码结果，而不是报告任务不可满足。SpecGuard 在编码前拆开两个信息来源：SpecAgent 只看描述与源码、完全不看测试；TestAgent 独立翻译测试；Certifier 对齐两侧语义，由 Lean kernel 核验冲突证明。不能忠实表达或对齐时允许 inconclusive。论文 §3–4 完整多模型全基准实验：成本过高，不复现（审查 DONE）；忠实缩小的 component_only / L1 micro-suite。保留真实模型生成与真实 Lean kernel，不用手写规范或固定模型输出替代核心过程。完整多模型全基准实验：成本过高，不复现（审查 DONE）；这不等于小范围实验已取得论文效果。先准备已有的小型 coding checkpoint 和官方 Lean 4.24.0 二进制；不需要 Mathlib、REPL、Docker 或训练数据。  Agent 安全 形式化验证 任务规范与测试冲突 Agent 评测与可靠性：如何知道真的做对了 SpecGuard 的 A100 回执 passed，能说明真实模型端到端成功了吗？ 不能。归档小模型运行3项均inconclusive，冲突证书0，且在Spec阶段停止；passed只表示真实CUDA执行和来源核验。手写Lean实例通过仅验证机械机制，不可替代模型输出。 示意：GPU命令跑通且保存了失败轨迹，仍不等于TestAgent和connector阶段已被真实模型走通。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-a583d933cd754ee0">SpecGuard 的 A100 回执 passed，能说明真实模型端到端成功了吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspecguard">SpecGuard: Proving a Task Is Broken Before the Agent Cheats</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · MATS</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。归档小模型运行3项均inconclusive，冲突证书0，且在Spec阶段停止；passed只表示真实CUDA执行和来源核验。手写Lean实例通过仅验证机械机制，不可替代模型输出。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>GPU命令跑通且保存了失败轨迹，仍不等于TestAgent和connector阶段已被真实模型走通。</p>
<p class="ar-learning-sources">依据：结果与验收边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.09159">原论文</a> · <a href="../../../../agent-research/2610.09159-specguard/">实现解读</a> · <a href="#qa-a583d933cd754ee0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:defa" data-paper-title="DeFA: Dependency-Guided Failure Attribution for LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="DeFA: Dependency-Guided Failure Attribution for LLM Agents Agent Qwen DianJin Team, Alibaba Cloud Computing 2026-10-01 融合 protocol relation 和语义依赖构造 event dependency graph，再从违规事件逆向追踪 source 与下游影响，形成 failure propagation graph 并定位 decisive error。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  失败归因 依赖图 技能进化 Agent 评测与可靠性：如何知道真的做对了 DeFA 为什么要从最终违规沿依赖边反向追踪？ 最终报错节点可能只是上游错误传播的受害者。方法结合protocol关系与语义依赖形成事件图，逆向寻找来源并保留下游传播子图和责任Agent，帮助区分触发位置与决定性错误。 示意：部署失败源于更早写错配置，最后一个执行部署的Agent未必是错误源。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-defa-2f35dc42" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-51e5a476da3647c4">DeFA 为什么要从最终违规沿依赖边反向追踪？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adefa">DeFA: Dependency-Guided Failure Attribution for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Qwen DianJin Team, Alibaba Cloud Computing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最终报错节点可能只是上游错误传播的受害者。方法结合protocol关系与语义依赖形成事件图，逆向寻找来源并保留下游传播子图和责任Agent，帮助区分触发位置与决定性错误。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>部署失败源于更早写错配置，最后一个执行部署的Agent未必是错误源。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01256">原论文</a> · <a href="../../../../agent-research/2610.01256-defa/">实现解读</a> · <a href="#qa-51e5a476da3647c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:defa" data-paper-title="DeFA: Dependency-Guided Failure Attribution for LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="DeFA: Dependency-Guided Failure Attribution for LLM Agents Agent Qwen DianJin Team, Alibaba Cloud Computing 2026-10-01 融合 protocol relation 和语义依赖构造 event dependency graph，再从违规事件逆向追踪 source 与下游影响，形成 failure propagation graph 并定位 decisive error。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  失败归因 依赖图 技能进化 Agent 评测与可靠性：如何知道真的做对了 为什么定位 decisive error 要保留依赖传播子图，而不是只标最后一个失败动作？ 最后失败可能由早期错误事实、参数或跨 Agent 消息导致，逆向依赖把责任源和受影响节点连接起来。协议关系提供结构，语义依赖补信息流，二者结合才能更具体解释传播；启发式最大错误分仍需证据，不是自动获得完整因果证明。 例如最后部署失败来自最早读取了旧配置，单责怪部署命令会漏掉源头；传播图可指出旧字段怎样一路传到错误参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-6828861af8c1cd51">为什么定位 decisive error 要保留依赖传播子图，而不是只标最后一个失败动作？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adefa">DeFA: Dependency-Guided Failure Attribution for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Qwen DianJin Team, Alibaba Cloud Computing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最后失败可能由早期错误事实、参数或跨 Agent 消息导致，逆向依赖把责任源和受影响节点连接起来。协议关系提供结构，语义依赖补信息流，二者结合才能更具体解释传播；启发式最大错误分仍需证据，不是自动获得完整因果证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最后部署失败来自最早读取了旧配置，单责怪部署命令会漏掉源头；传播图可指出旧字段怎样一路传到错误参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01256">原论文</a> · <a href="../../../../agent-research/2610.01256-defa/">实现解读</a> · <a href="#qa-6828861af8c1cd51">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:defa" data-paper-title="DeFA: Dependency-Guided Failure Attribution for LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="DeFA: Dependency-Guided Failure Attribution for LLM Agents Agent Qwen DianJin Team, Alibaba Cloud Computing 2026-10-01 融合 protocol relation 和语义依赖构造 event dependency graph，再从违规事件逆向追踪 source 与下游影响，形成 failure propagation graph 并定位 decisive error。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  失败归因 依赖图 技能进化 Agent 评测与可靠性：如何知道真的做对了 DeFA 的 decisive error 选择，与直接挑最后一次报错有什么区别？ 文档在违规节点的祖先集合内按error量选择，并保留责任及传播关系。最后事件仅是时间位置，未必承载导致失败的依赖；图上选择仍依赖输入关系与error定义，不等于独立因果证明。 示意：最后的重试超时可能只是结果，真正决定性错误在更早生成的错误参数。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-fb7cdb92ee87b5d4">DeFA 的 decisive error 选择，与直接挑最后一次报错有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adefa">DeFA: Dependency-Guided Failure Attribution for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Qwen DianJin Team, Alibaba Cloud Computing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>文档在违规节点的祖先集合内按error量选择，并保留责任及传播关系。最后事件仅是时间位置，未必承载导致失败的依赖；图上选择仍依赖输入关系与error定义，不等于独立因果证明。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>最后的重试超时可能只是结果，真正决定性错误在更早生成的错误参数。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01256">原论文</a> · <a href="../../../../agent-research/2610.01256-defa/">实现解读</a> · <a href="#qa-fb7cdb92ee87b5d4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:defa" data-paper-title="DeFA: Dependency-Guided Failure Attribution for LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="DeFA: Dependency-Guided Failure Attribution for LLM Agents Agent Qwen DianJin Team, Alibaba Cloud Computing 2026-10-01 融合 protocol relation 和语义依赖构造 event dependency graph，再从违规事件逆向追踪 source 与下游影响，形成 failure propagation graph 并定位 decisive error。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。执行依赖反向传播与 decisive-error 选择；不使用 gold plan/answer，不运行多模态 judge。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  失败归因 依赖图 技能进化 Agent 评测与可靠性：如何知道真的做对了 DeFA 构建传播图时，为什么不能只保存事件文字而丢弃依赖与责任？ 公式候选集由Ancestor(V)决定，缺边会漏掉上游来源，错边会引入无关事件。应保留protocol/语义依赖、事件ID、error量与responsible agent；本地不读gold plan也不运行多模态judge。 示意：两个Agent先后写文件，必须知道失败消费了哪个版本，才能追到相关写入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e222262e26ccc6c9">DeFA 构建传播图时，为什么不能只保存事件文字而丢弃依赖与责任？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Adefa">DeFA: Dependency-Guided Failure Attribution for LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Qwen DianJin Team, Alibaba Cloud Computing</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式候选集由Ancestor(V)决定，缺边会漏掉上游来源，错边会引入无关事件。应保留protocol/语义依赖、事件ID、error量与responsible agent；本地不读gold plan也不运行多模态judge。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>两个Agent先后写文件，必须知道失败消费了哪个版本，才能追到相关写入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01256">原论文</a> · <a href="../../../../agent-research/2610.01256-defa/">实现解读</a> · <a href="#qa-e222262e26ccc6c9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pace-capability" data-paper-title="PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents Agent 原文首页未列第一作者机构 2026-10-01 在每次工具副作用发生前，根据认证请求编译出的 authority 与输入 provenance 同时检查 effect；入库时安全不代表执行时可信。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 安全 工具权限 provenance Agent 评测与可靠性：如何知道真的做对了 PACE 为什么在工具副作用发生前检查能力与来源？ 资料入库时可信，不表示当前调用有权执行所有动作。方法根据认证请求形成authority，并结合输入provenance在每次effect发生前检查，防止低信任内容扩张执行权限。 示意：网页里出现“发送文件”文字，不等于用户已授权发送文件。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-pace-capability-eec90992" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ea936171a3e8d4b0">PACE 为什么在工具副作用发生前检查能力与来源？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apace-capability">PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>资料入库时可信，不表示当前调用有权执行所有动作。方法根据认证请求形成authority，并结合输入provenance在每次effect发生前检查，防止低信任内容扩张执行权限。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>网页里出现“发送文件”文字，不等于用户已授权发送文件。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01349">原论文</a> · <a href="../../../../agent-research/2610.01349-pace-capability/">实现解读</a> · <a href="#qa-ea936171a3e8d4b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pace-capability" data-paper-title="PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents Agent 原文首页未列第一作者机构 2026-10-01 在每次工具副作用发生前，根据认证请求编译出的 authority 与输入 provenance 同时检查 effect；入库时安全不代表执行时可信。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 安全 工具权限 provenance Agent 评测与可靠性：如何知道真的做对了 为什么记忆入库时安全，不能保证其内容在工具执行时有 authority？ 入库检查只处理当时内容，执行还要根据认证请求限制实际副作用，并追踪输入来源是否可信。provenance 与 authority 同时满足才放行，避免不可信记忆借合法工具越权；文本声称被授权不能代替系统认证，也不能只在写库时检查一次。 例如网页文字被存入记忆后要求删除文件，入库未发现危险不代表用户授权删除；执行前仍须核对 effect 和来源。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-5ab360b3ac4766b4">为什么记忆入库时安全，不能保证其内容在工具执行时有 authority？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apace-capability">PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>入库检查只处理当时内容，执行还要根据认证请求限制实际副作用，并追踪输入来源是否可信。provenance 与 authority 同时满足才放行，避免不可信记忆借合法工具越权；文本声称被授权不能代替系统认证，也不能只在写库时检查一次。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如网页文字被存入记忆后要求删除文件，入库未发现危险不代表用户授权删除；执行前仍须核对 effect 和来源。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01349">原论文</a> · <a href="../../../../agent-research/2610.01349-pace-capability/">实现解读</a> · <a href="#qa-5ab360b3ac4766b4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pace-capability" data-paper-title="PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents Agent 原文首页未列第一作者机构 2026-10-01 在每次工具副作用发生前，根据认证请求编译出的 authority 与输入 provenance 同时检查 effect；入库时安全不代表执行时可信。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 安全 工具权限 provenance Agent 评测与可靠性：如何知道真的做对了 PACE 的 capability 检查与 provenance 检查，能只选其中一个吗？ 允许条件是effect属于authority且provenance可信。权限范围约束能做什么，来源检查约束当前调用依据是否可信；满足一侧不自动满足另一侧，二者是合取而非替代关系。 示意：某工具通常允许读文件，也不代表来自不可信页面的这次读请求应被放行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9838b220b0dc8012">PACE 的 capability 检查与 provenance 检查，能只选其中一个吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apace-capability">PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>允许条件是effect属于authority且provenance可信。权限范围约束能做什么，来源检查约束当前调用依据是否可信；满足一侧不自动满足另一侧，二者是合取而非替代关系。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某工具通常允许读文件，也不代表来自不可信页面的这次读请求应被放行。</p>
<p class="ar-learning-sources">依据：核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01349">原论文</a> · <a href="../../../../agent-research/2610.01349-pace-capability/">实现解读</a> · <a href="#qa-9838b220b0dc8012">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:pace-capability" data-paper-title="PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents Agent 原文首页未列第一作者机构 2026-10-01 在每次工具副作用发生前，根据认证请求编译出的 authority 与输入 provenance 同时检查 effect；入库时安全不代表执行时可信。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。执行 pre-effect capability/provenance gate；不运行浏览器或系统工具。本地对照口径：基线为机制关闭或默认状态，实验组执行定义性算子；L1 不报告正式相对提升，百分比不适用。  Agent 安全 工具权限 provenance Agent 评测与可靠性：如何知道真的做对了 PACE 可以先执行工具，再用日志补做 gate 吗？ 不能。pre-effect gate必须在副作用前得到完整effect集合并与authority、provenance比较；事后记录只能审计，无法撤销已发生的影响。本地仅执行选择协议，不运行系统工具或浏览器。 示意：邮件已经发送之后才发现来源不可信，已经失去执行前阻断的作用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-5b7efda99a1c0174">PACE 可以先执行工具，再用日志补做 gate 吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Apace-capability">PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能。pre-effect gate必须在副作用前得到完整effect集合并与authority、provenance比较；事后记录只能审计，无法撤销已发生的影响。本地仅执行选择协议，不运行系统工具或浏览器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>邮件已经发送之后才发现来源不可信，已经失去执行前阻断的作用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01349">原论文</a> · <a href="../../../../agent-research/2610.01349-pace-capability/">实现解读</a> · <a href="#qa-5b7efda99a1c0174">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:safe-self-improvement" data-paper-title="Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover Agent 原文首页未列第一作者机构 2026-10-01 把检测、当前可执行实现选择和下一轮编辑源分开；所有候选必须对当前条件重新验证，若无候选通过则回滚 founder，而不是继续运行已失败 incumbent。 未调用论文编辑模型，也未复现 Amazon Bedrock 实验。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  RSI 安全 验证 回滚 Agent 评测与可靠性：如何知道真的做对了 Safe Self-Improvement 为什么区分下一轮编辑源与当前运行实现？ 一个程序可以提供有用的编辑起点，却不满足当前执行条件。方法将检测、当前可执行选择、下一轮编辑源分开，所有候选对当前条件重新验证，防止历史通过记录掩盖现在的失败。 示意：旧版本的某段代码值得借鉴，不代表整个旧版本今天仍可直接运行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-safe-self-improvement-450abfd4" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-62d68c3d6cbc7b8d">Safe Self-Improvement 为什么区分下一轮编辑源与当前运行实现？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asafe-self-improvement">Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>一个程序可以提供有用的编辑起点，却不满足当前执行条件。方法将检测、当前可执行选择、下一轮编辑源分开，所有候选对当前条件重新验证，防止历史通过记录掩盖现在的失败。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>旧版本的某段代码值得借鉴，不代表整个旧版本今天仍可直接运行。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01073">原论文</a> · <a href="../../../../agent-research/2610.01073-safe-self-improvement/">实现解读</a> · <a href="#qa-62d68c3d6cbc7b8d">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:safe-self-improvement" data-paper-title="Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover Agent 原文首页未列第一作者机构 2026-10-01 把检测、当前可执行实现选择和下一轮编辑源分开；所有候选必须对当前条件重新验证，若无候选通过则回滚 founder，而不是继续运行已失败 incumbent。 未调用论文编辑模型，也未复现 Amazon Bedrock 实验。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  RSI 安全 验证 回滚 Agent 评测与可靠性：如何知道真的做对了 为什么当前可执行版本与下一轮编辑源要分开选择？ 最有改进潜力的编辑父本未必在当前条件下安全可运行，运行版本必须重新验证后从合格集合选。无候选通过时回到 founder，而不是继续使用已经失败的 incumbent；恢复执行与继续搜索是两项职责，不能把历史曾通过当成永久有效资格。 例如新环境使现任版本检查失败，仍可保留它作分析编辑来源，但实际任务应切到当前验证合格版本或执行 founder 回滚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-48504ee29677188e">为什么当前可执行版本与下一轮编辑源要分开选择？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asafe-self-improvement">Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>最有改进潜力的编辑父本未必在当前条件下安全可运行，运行版本必须重新验证后从合格集合选。无候选通过时回到 founder，而不是继续使用已经失败的 incumbent；恢复执行与继续搜索是两项职责，不能把历史曾通过当成永久有效资格。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如新环境使现任版本检查失败，仍可保留它作分析编辑来源，但实际任务应切到当前验证合格版本或执行 founder 回滚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01073">原论文</a> · <a href="../../../../agent-research/2610.01073-safe-self-improvement/">实现解读</a> · <a href="#qa-48504ee29677188e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:safe-self-improvement" data-paper-title="Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover Agent 原文首页未列第一作者机构 2026-10-01 把检测、当前可执行实现选择和下一轮编辑源分开；所有候选必须对当前条件重新验证，若无候选通过则回滚 founder，而不是继续运行已失败 incumbent。 未调用论文编辑模型，也未复现 Amazon Bedrock 实验。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  RSI 安全 验证 回滚 Agent 评测与可靠性：如何知道真的做对了 没有候选通过时回滚 founder，与继续运行 incumbent 有何差异？ 公式只在当前有效集合内取最高分；集合为空就走founder rollback。继续使用已失败incumbent会绕过当前验证；回滚是恢复协议，并不自动证明founder在任意新条件下绝对安全。 示意：评分最高的候选若当前验证失败，也不能因为过去领先而留在执行位。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-83fc9f453ef86614">没有候选通过时回滚 founder，与继续运行 incumbent 有何差异？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asafe-self-improvement">Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>公式只在当前有效集合内取最高分；集合为空就走founder rollback。继续使用已失败incumbent会绕过当前验证；回滚是恢复协议，并不自动证明founder在任意新条件下绝对安全。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>评分最高的候选若当前验证失败，也不能因为过去领先而留在执行位。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01073">原论文</a> · <a href="../../../../agent-research/2610.01073-safe-self-improvement/">实现解读</a> · <a href="#qa-83fc9f453ef86614">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:safe-self-improvement" data-paper-title="Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover Agent 原文首页未列第一作者机构 2026-10-01 把检测、当前可执行实现选择和下一轮编辑源分开；所有候选必须对当前条件重新验证，若无候选通过则回滚 founder，而不是继续运行已失败 incumbent。 未调用论文编辑模型，也未复现 Amazon Bedrock 实验。复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。执行当前验证与 founder fallback 选择协议；未调用论文编辑模型，也未复现 Amazon Bedrock 实验。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  RSI 安全 验证 回滚 Agent 评测与可靠性：如何知道真的做对了 Safe Self-Improvement 可以直接复用候选上轮通过的布尔标记吗？ 不能把旧验证状态当当前有效集，应绑定本轮条件重新检查，再在通过者中选分数最高者。本地执行验证与founder回退选择，未调用论文编辑模型或复现Bedrock实验。 示意：工具权限或任务条件改变后，旧的passed不能无条件带入新一轮。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-c9e0f5c5a680555c">Safe Self-Improvement 可以直接复用候选上轮通过的布尔标记吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asafe-self-improvement">Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文首页未列第一作者机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能把旧验证状态当当前有效集，应绑定本轮条件重新检查，再在通过者中选分数最高者。本地执行验证与founder回退选择，未调用论文编辑模型或复现Bedrock实验。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>工具权限或任务条件改变后，旧的passed不能无条件带入新一轮。</p>
<p class="ar-learning-sources">依据：背景与主要改动、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.01073">原论文</a> · <a href="../../../../agent-research/2610.01073-safe-self-improvement/">实现解读</a> · <a href="#qa-c9e0f5c5a680555c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:veriharness" data-paper-title="VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks Agent Google Cloud AI Research 2026-10-01 同一基础模型得到 workspace、证据工具和可复用验证技能；disagreement resolver 查证冲突 claim，consensus challenger 主动质疑共同 claim 和遗漏要求。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 验证 证据工具 长程任务 Agent 评测与可靠性：如何知道真的做对了 VeriHarness 为什么除了消解分歧，还要主动挑战共识？ 多个回答一致仍可能共同缺证据或遗漏要求。disagreement resolver查证冲突claim，consensus challenger质疑共同claim与遗漏，两者配合证据工具和workspace，避免把一致性当正确性。 示意：三个Agent都引用同一条未经核验的说法，一致投票仍需要查证。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-veriharness-6d6ee53b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f8826a9c4da28bf9">VeriHarness 为什么除了消解分歧，还要主动挑战共识？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Averiharness">VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>多个回答一致仍可能共同缺证据或遗漏要求。disagreement resolver查证冲突claim，consensus challenger质疑共同claim与遗漏，两者配合证据工具和workspace，避免把一致性当正确性。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三个Agent都引用同一条未经核验的说法，一致投票仍需要查证。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00972">原论文</a> · <a href="../../../../agent-research/2610.00972-veriharness/">实现解读</a> · <a href="#qa-f8826a9c4da28bf9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:veriharness" data-paper-title="VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks Agent Google Cloud AI Research 2026-10-01 同一基础模型得到 workspace、证据工具和可复用验证技能；disagreement resolver 查证冲突 claim，consensus challenger 主动质疑共同 claim 和遗漏要求。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 验证 证据工具 长程任务 Agent 评测与可靠性：如何知道真的做对了 多个验证者达成共识后，为什么还需要 consensus challenger？ 共同结论也可能来自共享错误或共同遗漏，只有处理显式分歧无法发现所有人都没检查的要求。challenger 主动质疑共识与缺口，resolver 则针对冲突取证，职责互补；支持与反驳应来自证据工具，而不是把赞同票数当作真值。 例如三名审查者都只看页面截图，没人检查下载文件；challenger 可提出产物遗漏问题，即使原讨论完全没有分歧。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2be905d50052cea6">多个验证者达成共识后，为什么还需要 consensus challenger？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Averiharness">VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>共同结论也可能来自共享错误或共同遗漏，只有处理显式分歧无法发现所有人都没检查的要求。challenger 主动质疑共识与缺口，resolver 则针对冲突取证，职责互补；支持与反驳应来自证据工具，而不是把赞同票数当作真值。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如三名审查者都只看页面截图，没人检查下载文件；challenger 可提出产物遗漏问题，即使原讨论完全没有分歧。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00972">原论文</a> · <a href="../../../../agent-research/2610.00972-veriharness/">实现解读</a> · <a href="#qa-2be905d50052cea6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:veriharness" data-paper-title="VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks Agent Google Cloud AI Research 2026-10-01 同一基础模型得到 workspace、证据工具和可复用验证技能；disagreement resolver 查证冲突 claim，consensus challenger 主动质疑共同 claim 和遗漏要求。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 验证 证据工具 长程任务 Agent 评测与可靠性：如何知道真的做对了 VeriHarness 的证据支持评分，与简单多数投票有什么区别？ 投票统计意见数量，文档评分同时考虑支持证据、与共识相关的矛盾及claim数量惩罚。更多人同意或写更多claim都不自动增加可验证性；本地fixture checker也不是论文真实工具环境。 示意：一条有证据的精确结论，可能比十条共同重复却互相矛盾的断言更值得保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ce48a1617a5b524b">VeriHarness 的证据支持评分，与简单多数投票有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Averiharness">VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>投票统计意见数量，文档评分同时考虑支持证据、与共识相关的矛盾及claim数量惩罚。更多人同意或写更多claim都不自动增加可验证性；本地fixture checker也不是论文真实工具环境。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一条有证据的精确结论，可能比十条共同重复却互相矛盾的断言更值得保留。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00972">原论文</a> · <a href="../../../../agent-research/2610.00972-veriharness/">实现解读</a> · <a href="#qa-ce48a1617a5b524b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:veriharness" data-paper-title="VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks Agent Google Cloud AI Research 2026-10-01 同一基础模型得到 workspace、证据工具和可复用验证技能；disagreement resolver 查证冲突 claim，consensus challenger 主动质疑共同 claim 和遗漏要求。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。执行证据支持、冲突和共识挑战选择；fixture checker 不等同论文的真实工具环境。本地对照口径：基线为机制关闭或默认状态，实验组为开启对应核心算子；相对百分比不适用。本批指标只验证不变量、梯度或状态转换，不表示论文规模效果。  Agent 验证 证据工具 长程任务 Agent 评测与可靠性：如何知道真的做对了 实现 VeriHarness 的 claim 数量惩罚时，为什么要保留 claim 拆分口径？ score包含epsilon乘claim数，拆分或合并同一内容会改变惩罚。应同时保留支持、矛盾和claim计数，才能解释选择；不能把fixture判定器的输出宣传成已核验真实世界事实。 示意：一句话拆成三条断言后长度惩罚会变，比较候选时必须使用一致的拆分规则。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b27b377f2f75b895">实现 VeriHarness 的 claim 数量惩罚时，为什么要保留 claim 拆分口径？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Averiharness">VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>score包含epsilon乘claim数，拆分或合并同一内容会改变惩罚。应同时保留支持、矛盾和claim计数，才能解释选择；不能把fixture判定器的输出宣传成已核验真实世界事实。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一句话拆成三条断言后长度惩罚会变，比较候选时必须使用一致的拆分规则。</p>
<p class="ar-learning-sources">依据：核心公式、复现边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2610.00972">原论文</a> · <a href="../../../../agent-research/2610.00972-veriharness/">实现解读</a> · <a href="#qa-b27b377f2f75b895">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:user-proxy-bench" data-paper-title="UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training Agent 原文未列机构 2026-09-29 UFS 与 agent task reward 独立：每个 episode 的所有适用 user-contract criteria 必须全部通过，episode 才计 1。重点审计 premature disclosure，即用户模拟器在 agent 请求之前就泄露私有字段；这可能维持任务成功，却让 agent 少做本应评测的信息收集。 复现级别：L1 评测机制。复现级别：L1 评测机制。实现严格 User Fidelity Score 与 premature disclosure 审计；不运行闭源 proxy。本地实现 Eq. (1) 的 all-criteria product，并按时间顺序审计 request/disclosure。它只接收 rubric pass/fail 和公开交互事件，不把私有 blueprint 暴露给被评 agent；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 375 个企业任务和七种 proxy。  Agent 评测 用户模拟器 信息泄漏审计 Agent 评测与可靠性：如何知道真的做对了 UserProxyBench 为什么把用户模拟器保真度与 Agent 任务奖励分开？ 模拟器可能提前泄露私有字段，让Agent少做信息收集却仍完成任务。独立UFS检查用户契约是否全部满足，避免把被简化任务上的高reward误认成真实交互能力。 示意：Agent还没问订单号，模拟用户就主动给出隐藏订单信息，任务成功也不能说明澄清能力充分。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-user-proxy-bench-da315c41" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bb83180f6993ea13">UserProxyBench 为什么把用户模拟器保真度与 Agent 任务奖励分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Auser-proxy-bench">UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>模拟器可能提前泄露私有字段，让Agent少做信息收集却仍完成任务。独立UFS检查用户契约是否全部满足，避免把被简化任务上的高reward误认成真实交互能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>Agent还没问订单号，模拟用户就主动给出隐藏订单信息，任务成功也不能说明澄清能力充分。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38043">原论文</a> · <a href="../../../../agent-research/2609.38043-userproxybench/">实现解读</a> · <a href="#qa-bb83180f6993ea13">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:user-proxy-bench" data-paper-title="UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training Agent 原文未列机构 2026-09-29 UFS 与 agent task reward 独立：每个 episode 的所有适用 user-contract criteria 必须全部通过，episode 才计 1。重点审计 premature disclosure，即用户模拟器在 agent 请求之前就泄露私有字段；这可能维持任务成功，却让 agent 少做本应评测的信息收集。 复现级别：L1 评测机制。复现级别：L1 评测机制。实现严格 User Fidelity Score 与 premature disclosure 审计；不运行闭源 proxy。本地实现 Eq. (1) 的 all-criteria product，并按时间顺序审计 request/disclosure。它只接收 rubric pass/fail 和公开交互事件，不把私有 blueprint 暴露给被评 agent；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 375 个企业任务和七种 proxy。  Agent 评测 用户模拟器 信息泄漏审计 Agent 评测与可靠性：如何知道真的做对了 为什么用户模拟器提前透露私有字段，可能提高任务成功却降低 UFS？ Agent 原本应主动询问信息，模拟器抢先给出就绕过了被测的信息收集能力。UFS 单独检查每 episode 全部适用用户合同，而非复用任务回报，能暴露这种捷径；任务完成和用户扮演忠实是两条不同证据，不能只看成功率就认定模拟器好。 例如 Agent 尚未问订单号，模拟用户已主动报出，退款容易成功；但评测不再检验 Agent 是否知道何时询问关键字段。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-b9940179a02b78e4">为什么用户模拟器提前透露私有字段，可能提高任务成功却降低 UFS？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Auser-proxy-bench">UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Agent 原本应主动询问信息，模拟器抢先给出就绕过了被测的信息收集能力。UFS 单独检查每 episode 全部适用用户合同，而非复用任务回报，能暴露这种捷径；任务完成和用户扮演忠实是两条不同证据，不能只看成功率就认定模拟器好。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如 Agent 尚未问订单号，模拟用户已主动报出，退款容易成功；但评测不再检验 Agent 是否知道何时询问关键字段。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38043">原论文</a> · <a href="../../../../agent-research/2609.38043-userproxybench/">实现解读</a> · <a href="#qa-b9940179a02b78e4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:user-proxy-bench" data-paper-title="UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training Agent 原文未列机构 2026-09-29 UFS 与 agent task reward 独立：每个 episode 的所有适用 user-contract criteria 必须全部通过，episode 才计 1。重点审计 premature disclosure，即用户模拟器在 agent 请求之前就泄露私有字段；这可能维持任务成功，却让 agent 少做本应评测的信息收集。 复现级别：L1 评测机制。复现级别：L1 评测机制。实现严格 User Fidelity Score 与 premature disclosure 审计；不运行闭源 proxy。本地实现 Eq. (1) 的 all-criteria product，并按时间顺序审计 request/disclosure。它只接收 rubric pass/fail 和公开交互事件，不把私有 blueprint 暴露给被评 agent；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 375 个企业任务和七种 proxy。  Agent 评测 用户模拟器 信息泄漏审计 Agent 评测与可靠性：如何知道真的做对了 UFS 的 all-criteria product 与逐条件平均通过率有什么区别？ 每个episode所有适用条件都通过才计1，一项失败就使该episode为0；逐条件平均允许其它通过项抵消关键违规，是另一种口径。最终仍须把UFS与任务reward分别报告。 示意：10项适用条件通过9项，逐项平均为90%，该episode的严格UFS仍为0。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-29e12f69eb102a9b">UFS 的 all-criteria product 与逐条件平均通过率有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Auser-proxy-bench">UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每个episode所有适用条件都通过才计1，一项失败就使该episode为0；逐条件平均允许其它通过项抵消关键违规，是另一种口径。最终仍须把UFS与任务reward分别报告。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>10项适用条件通过9项，逐项平均为90%，该episode的严格UFS仍为0。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38043">原论文</a> · <a href="../../../../agent-research/2609.38043-userproxybench/">实现解读</a> · <a href="#qa-29e12f69eb102a9b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:user-proxy-bench" data-paper-title="UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training Agent 原文未列机构 2026-09-29 UFS 与 agent task reward 独立：每个 episode 的所有适用 user-contract criteria 必须全部通过，episode 才计 1。重点审计 premature disclosure，即用户模拟器在 agent 请求之前就泄露私有字段；这可能维持任务成功，却让 agent 少做本应评测的信息收集。 复现级别：L1 评测机制。复现级别：L1 评测机制。实现严格 User Fidelity Score 与 premature disclosure 审计；不运行闭源 proxy。本地实现 Eq. (1) 的 all-criteria product，并按时间顺序审计 request/disclosure。它只接收 rubric pass/fail 和公开交互事件，不把私有 blueprint 暴露给被评 agent；三种子机制结果见 metrics/mechanism-seeds42-44.json。未运行 375 个企业任务和七种 proxy。  Agent 评测 用户模拟器 信息泄漏审计 Agent 评测与可靠性：如何知道真的做对了 审计 premature disclosure 时，为什么必须保留 request 与 disclosure 时间顺序？ 是否过早披露取决于相关请求是否先发生，不能只看字段最后有没有出现。本地按公开交互事件与rubric判定，私有blueprint留在评测侧；未执行原文企业任务和闭源proxy矩阵。 示意：同一字段在被询问之后给出和之前给出，最终文本相同，保真判定却不同。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f4ac506d1471107c">审计 premature disclosure 时，为什么必须保留 request 与 disclosure 时间顺序？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Auser-proxy-bench">UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · 原文未列机构</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>是否过早披露取决于相关请求是否先发生，不能只看字段最后有没有出现。本地按公开交互事件与rubric判定，私有blueprint留在评测侧；未执行原文企业任务和闭源proxy矩阵。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一字段在被询问之后给出和之前给出，最终文本相同，保真判定却不同。</p>
<p class="ar-learning-sources">依据：背景与主要改动、本地复现；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.38043">原论文</a> · <a href="../../../../agent-research/2609.38043-userproxybench/">实现解读</a> · <a href="#qa-f4ac506d1471107c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:certified-selective-eval" data-paper-title="Certified Selective Automation of LLM Agent Evaluation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Certified Selective Automation of LLM Agent Evaluation Agent Independent Researcher 2026-09-28 按任务簇而非轨迹独立假设做 bootstrap，给自动判断区域的错误率建立上置信界，只有证书低于预算才自动接管。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent 评测 选择性自动化 统计证书 Agent 评测与可靠性：如何知道真的做对了 选择性自动评测为什么允许一部分交给人工？ 目标是在可证错误预算内自动处理可靠区域，而不是所有轨迹一律机器裁决。上置信界未达标时保留人工或其他评估，覆盖率与风险需一起报告。 例如简单任务自动判，证据模糊的任务仍交审查，不能只报自动部分准确率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-certified-selective-eval-1bfcfcb0" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-03ef9bb812f4f600">选择性自动评测为什么允许一部分交给人工？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acertified-selective-eval">Certified Selective Automation of LLM Agent Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>目标是在可证错误预算内自动处理可靠区域，而不是所有轨迹一律机器裁决。上置信界未达标时保留人工或其他评估，覆盖率与风险需一起报告。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如简单任务自动判，证据模糊的任务仍交审查，不能只报自动部分准确率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34320">原论文</a> · <a href="../../../../agent-research/2609.34320-certified-selective-eval/">实现解读</a> · <a href="#qa-03ef9bb812f4f600">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:certified-selective-eval" data-paper-title="Certified Selective Automation of LLM Agent Evaluation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Certified Selective Automation of LLM Agent Evaluation Agent Independent Researcher 2026-09-28 按任务簇而非轨迹独立假设做 bootstrap，给自动判断区域的错误率建立上置信界，只有证书低于预算才自动接管。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent 评测 选择性自动化 统计证书 Agent 评测与可靠性：如何知道真的做对了 为什么自动评分区域的错误证书要按任务簇 bootstrap，而非把所有轨迹当独立样本？ 同任务多条轨迹共享难度与结构，独立抽样会低估相关性和不确定性。按簇重采样为自动判断区域建立错误率上界，只有低于预算才接管，其余保留人工或外部评估；低平均错误不等于任何阈值都可认证，证书还受校准分布与选择规则限制。 例如一个任务生成一百条近似轨迹，不能当一百份独立成功证据压窄区间；应把这批一起作为任务簇处理。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-1a0d4910bf52da75">为什么自动评分区域的错误证书要按任务簇 bootstrap，而非把所有轨迹当独立样本？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acertified-selective-eval">Certified Selective Automation of LLM Agent Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同任务多条轨迹共享难度与结构，独立抽样会低估相关性和不确定性。按簇重采样为自动判断区域建立错误率上界，只有低于预算才接管，其余保留人工或外部评估；低平均错误不等于任何阈值都可认证，证书还受校准分布与选择规则限制。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一个任务生成一百条近似轨迹，不能当一百份独立成功证据压窄区间；应把这批一起作为任务簇处理。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34320">原论文</a> · <a href="../../../../agent-research/2609.34320-certified-selective-eval/">实现解读</a> · <a href="#qa-1a0d4910bf52da75">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:certified-selective-eval" data-paper-title="Certified Selective Automation of LLM Agent Evaluation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Certified Selective Automation of LLM Agent Evaluation Agent Independent Researcher 2026-09-28 按任务簇而非轨迹独立假设做 bootstrap，给自动判断区域的错误率建立上置信界，只有证书低于预算才自动接管。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent 评测 选择性自动化 统计证书 Agent 评测与可靠性：如何知道真的做对了 选择性评测用错误率上置信界，比仅用自动区域的经验错误率多控制什么？ 经验错误率只总结已观察样本，上置信界还反映有限证据下的不确定性。只有界低于预算才自动接管，证据不足时即使暂时零错，也可能继续交人工。它控制的是选定自动区域的风险证据，不能承诺每条自动判断绝不出错。 教学例子：某小区域暂未发现错误，样本仍很少；经验值为零不代表错误上界已足够低，覆盖率不能据此随意扩大。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a5b687bab96bef57">选择性评测用错误率上置信界，比仅用自动区域的经验错误率多控制什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acertified-selective-eval">Certified Selective Automation of LLM Agent Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>经验错误率只总结已观察样本，上置信界还反映有限证据下的不确定性。只有界低于预算才自动接管，证据不足时即使暂时零错，也可能继续交人工。它控制的是选定自动区域的风险证据，不能承诺每条自动判断绝不出错。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某小区域暂未发现错误，样本仍很少；经验值为零不代表错误上界已足够低，覆盖率不能据此随意扩大。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34320">原论文</a> · <a href="../../../../agent-research/2609.34320-certified-selective-eval/">实现解读</a> · <a href="#qa-a5b687bab96bef57">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:certified-selective-eval" data-paper-title="Certified Selective Automation of LLM Agent Evaluation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Certified Selective Automation of LLM Agent Evaluation Agent Independent Researcher 2026-09-28 按任务簇而非轨迹独立假设做 bootstrap，给自动判断区域的错误率建立上置信界，只有证书低于预算才自动接管。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。执行 task-cluster bootstrap certificate；mini-suite 证书不代表论文语料覆盖率。三种子诊断见 metrics/mechanism-seeds42-44.json。其中 diagnostic_only=true，不能进入正式能力排名。  Agent 评测 选择性自动化 统计证书 Agent 评测与可靠性：如何知道真的做对了 本地bootstrap证书可以直接宣称论文语料覆盖率吗？ 不能，mini-suite只验证聚类抽样和上界接管条件。任务身份、自动区域与错误标签应固定可追溯，置信上界而非点错误率需落在预算内才接管。 例如样本错率低但上界仍高，不能提前宣布满足误判预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-20ce56f5e0218ac3">本地bootstrap证书可以直接宣称论文语料覆盖率吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acertified-selective-eval">Certified Selective Automation of LLM Agent Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Independent Researcher</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，mini-suite只验证聚类抽样和上界接管条件。任务身份、自动区域与错误标签应固定可追溯，置信上界而非点错误率需落在预算内才接管。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如样本错率低但上界仍高，不能提前宣布满足误判预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.34320">原论文</a> · <a href="../../../../agent-research/2609.34320-certified-selective-eval/">实现解读</a> · <a href="#qa-20ce56f5e0218ac3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-design-study" data-paper-title="An Empirical Study of Harness Design for Coding Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="An Empirical Study of Harness Design for Coding Agents Agent University of Massachusetts Amherst 2026-09-17 固定底层执行循环，分别控制 planning、action space 与 context management，隔离 coding-agent harness 中真正影响效果和成本的因素。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。  编程 Agent Harness 设计 Agent 评测与可靠性：如何知道真的做对了 Harness设计研究中的harness，具体包含模型之外的哪些决定？ 它组织模型怎样计划、能使用什么动作空间，以及怎样管理上下文，再通过底层循环执行任务。这些是模型外的工作流程选择，不是替换一套模型权重。先识别可改动的harness组件，才能理解为何同一模型也会因执行方式不同而表现变化。 教学例子：同一编码模型可以一次只看到文件片段，也可以获得压缩后的多文件上下文；这属于harness设置变化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-harness-design-study-2ead25c3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0cbb02b7c2b56112">Harness设计研究中的harness，具体包含模型之外的哪些决定？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-design-study">An Empirical Study of Harness Design for Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Massachusetts Amherst</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它组织模型怎样计划、能使用什么动作空间，以及怎样管理上下文，再通过底层循环执行任务。这些是模型外的工作流程选择，不是替换一套模型权重。先识别可改动的harness组件，才能理解为何同一模型也会因执行方式不同而表现变化。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同一编码模型可以一次只看到文件片段，也可以获得压缩后的多文件上下文；这属于harness设置变化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20804">原论文</a> · <a href="../../../../agent-research/2609.20804-harness-design-study/">实现解读</a> · <a href="#qa-0cbb02b7c2b56112">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-design-study" data-paper-title="An Empirical Study of Harness Design for Coding Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="An Empirical Study of Harness Design for Coding Agents Agent University of Massachusetts Amherst 2026-09-17 固定底层执行循环，分别控制 planning、action space 与 context management，隔离 coding-agent harness 中真正影响效果和成本的因素。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。  编程 Agent Harness 设计 Agent 评测与可靠性：如何知道真的做对了 固定底层执行循环后分别改 planning、action space 与 context，为什么更能解释 harness 收益？ 完整框架对比常同时改变多个因素，无法判断涨分来自更多推理、易用动作还是更好状态管理。保持循环不变并单独控制组件，减少混杂，再分别看效果与成本；组件参考实现或统计合同并不等于已经运行原文大规模编码任务。 例如只把文件编辑接口换成精确替换，其他提示与预算不变，才能更集中评价动作空间，而非把同时换模型的收益一起算入。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d229d83150e67e88">固定底层执行循环后分别改 planning、action space 与 context，为什么更能解释 harness 收益？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-design-study">An Empirical Study of Harness Design for Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Massachusetts Amherst</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>完整框架对比常同时改变多个因素，无法判断涨分来自更多推理、易用动作还是更好状态管理。保持循环不变并单独控制组件，减少混杂，再分别看效果与成本；组件参考实现或统计合同并不等于已经运行原文大规模编码任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如只把文件编辑接口换成精确替换，其他提示与预算不变，才能更集中评价动作空间，而非把同时换模型的收益一起算入。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20804">原论文</a> · <a href="../../../../agent-research/2609.20804-harness-design-study/">实现解读</a> · <a href="#qa-d229d83150e67e88">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-design-study" data-paper-title="An Empirical Study of Harness Design for Coding Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="An Empirical Study of Harness Design for Coding Agents Agent University of Massachusetts Amherst 2026-09-17 固定底层执行循环，分别控制 planning、action space 与 context management，隔离 coding-agent harness 中真正影响效果和成本的因素。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。  编程 Agent Harness 设计 Agent 评测与可靠性：如何知道真的做对了 规划更详细与工具动作空间更丰富为什么不能合成一个提升结论？ 二者影响成本和行为的路径不同，组合变化无法说明各自贡献。需有受控因素对照，且交互效应可能存在，不能把一次组合收益全归某一组件。 例如同时加计划和新工具后成功，尚不知道主要帮助来自哪里。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-874a1ff3f39097e6">规划更详细与工具动作空间更丰富为什么不能合成一个提升结论？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-design-study">An Empirical Study of Harness Design for Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Massachusetts Amherst</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>二者影响成本和行为的路径不同，组合变化无法说明各自贡献。需有受控因素对照，且交互效应可能存在，不能把一次组合收益全归某一组件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如同时加计划和新工具后成功，尚不知道主要帮助来自哪里。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20804">原论文</a> · <a href="../../../../agent-research/2609.20804-harness-design-study/">实现解读</a> · <a href="#qa-874a1ff3f39097e6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harness-design-study" data-paper-title="An Empirical Study of Harness Design for Coding Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="An Empirical Study of Harness Design for Coding Agents Agent University of Massachusetts Amherst 2026-09-17 固定底层执行循环，分别控制 planning、action space 与 context management，隔离 coding-agent harness 中真正影响效果和成本的因素。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。本地实现可控 harness 因子，不把 mini-suite 当作 SWE-bench 或 Terminal-Bench 结果。  编程 Agent Harness 设计 Agent 评测与可靠性：如何知道真的做对了 本地可控harness因素是否等于跑完SWE-bench？ 不是，当前mini-suite只验证因素与控制流。模型版本、预算和工具协议需固定，实际基准题和执行证据未运行就不能报告相应能力分数。 例如模拟一个工具动作成功，不能换算成真实仓库修复成功率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-fe97b28686a5cbea">本地可控harness因素是否等于跑完SWE-bench？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharness-design-study">An Empirical Study of Harness Design for Coding Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Massachusetts Amherst</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，当前mini-suite只验证因素与控制流。模型版本、预算和工具协议需固定，实际基准题和执行证据未运行就不能报告相应能力分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模拟一个工具动作成功，不能换算成真实仓库修复成功率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.20804">原论文</a> · <a href="../../../../agent-research/2609.20804-harness-design-study/">实现解读</a> · <a href="#qa-fe97b28686a5cbea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:fuse-evaluator" data-paper-title="Verifiable Social Reasoning for LLM Assistants" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Verifiable Social Reasoning for LLM Assistants Agent Google Research / Hebrew University of Jerusalem / University of Cambridge 2026-09-15 用隐藏动机可验证的多 Agent 模拟评测用户转述、framing bias 与社会推理。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent 评测 社会推理 Agent 评测与可靠性：如何知道真的做对了 FUSE是在训练一个社交Agent，还是在提供可核验的社会推理评测环境？ 这里讨论的是评测：在多Agent模拟中设置可验证的隐藏动机，观察助手如何理解用户转述和社会情境。隐藏状态为评分提供依据，并不是直接交给受测助手的答案。实现评测模拟或本地核，也不意味着已经训练出更好的社会推理模型。 教学例子：模拟里知道甲的真实意图，助手只读用户转述后作判断；评测器随后核对，而非先把意图告诉助手。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-fuse-evaluator-e12e2808" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-64902b38498f512a">FUSE是在训练一个社交Agent，还是在提供可核验的社会推理评测环境？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afuse-evaluator">Verifiable Social Reasoning for LLM Assistants</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / Hebrew University of Jerusalem / University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>这里讨论的是评测：在多Agent模拟中设置可验证的隐藏动机，观察助手如何理解用户转述和社会情境。隐藏状态为评分提供依据，并不是直接交给受测助手的答案。实现评测模拟或本地核，也不意味着已经训练出更好的社会推理模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>模拟里知道甲的真实意图，助手只读用户转述后作判断；评测器随后核对，而非先把意图告诉助手。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17496">原论文</a> · <a href="../../../../agent-research/2609.17496-fuse-evaluator/">实现解读</a> · <a href="#qa-64902b38498f512a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:fuse-evaluator" data-paper-title="Verifiable Social Reasoning for LLM Assistants" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Verifiable Social Reasoning for LLM Assistants Agent Google Research / Hebrew University of Jerusalem / University of Cambridge 2026-09-15 用隐藏动机可验证的多 Agent 模拟评测用户转述、framing bias 与社会推理。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent 评测 社会推理 Agent 评测与可靠性：如何知道真的做对了 隐藏动机可验证的模拟，为什么比只看用户转述是否流畅更适合测社会推理？ 转述可能带偏见或遗漏，流畅回应未必识别各方真实目标。模拟环境保留不向被测者公开的动机与事件条件，评分侧据此检查推断，而非用表面措辞一致度代替；隐藏参考只能给验证器，固定逻辑 fixture 也不能冒充多 Agent 的真实语义交互。 例如用户把同事拒绝请求说成敌意，模拟真因可能是资源冲突；评测应看助手是否据可见证据区分，而非附和转述。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-8a95517ba8ccb520">隐藏动机可验证的模拟，为什么比只看用户转述是否流畅更适合测社会推理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afuse-evaluator">Verifiable Social Reasoning for LLM Assistants</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / Hebrew University of Jerusalem / University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>转述可能带偏见或遗漏，流畅回应未必识别各方真实目标。模拟环境保留不向被测者公开的动机与事件条件，评分侧据此检查推断，而非用表面措辞一致度代替；隐藏参考只能给验证器，固定逻辑 fixture 也不能冒充多 Agent 的真实语义交互。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如用户把同事拒绝请求说成敌意，模拟真因可能是资源冲突；评测应看助手是否据可见证据区分，而非附和转述。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17496">原论文</a> · <a href="../../../../agent-research/2609.17496-fuse-evaluator/">实现解读</a> · <a href="#qa-8a95517ba8ccb520">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:fuse-evaluator" data-paper-title="Verifiable Social Reasoning for LLM Assistants" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Verifiable Social Reasoning for LLM Assistants Agent Google Research / Hebrew University of Jerusalem / University of Cambridge 2026-09-15 用隐藏动机可验证的多 Agent 模拟评测用户转述、framing bias 与社会推理。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent 评测 社会推理 Agent 评测与可靠性：如何知道真的做对了 framing bias评测与普通问答准确率有什么区别？ 表述框架可能引导归因，即使事实相同；对照转述与隐藏状态可测社会判断偏移。模拟行为不是所有真人关系，不能从小状态机推广全面社交理解。 例如把同一迟到描述为敷衍或遇堵，框架可能改变助手判断。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5e2c04c08d3994d6">framing bias评测与普通问答准确率有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afuse-evaluator">Verifiable Social Reasoning for LLM Assistants</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / Hebrew University of Jerusalem / University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>表述框架可能引导归因，即使事实相同；对照转述与隐藏状态可测社会判断偏移。模拟行为不是所有真人关系，不能从小状态机推广全面社交理解。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如把同一迟到描述为敷衍或遇堵，框架可能改变助手判断。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17496">原论文</a> · <a href="../../../../agent-research/2609.17496-fuse-evaluator/">实现解读</a> · <a href="#qa-5e2c04c08d3994d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:fuse-evaluator" data-paper-title="Verifiable Social Reasoning for LLM Assistants" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Verifiable Social Reasoning for LLM Assistants Agent Google Research / Hebrew University of Jerusalem / University of Cambridge 2026-09-15 用隐藏动机可验证的多 Agent 模拟评测用户转述、framing bias 与社会推理。本地 reference kernel 保留决定性门控、权重或状态转换，并输出可审计中间量，以便与相邻方法在统一预算下比较。 复现级别：L1 核心机制诊断。复现级别：L1 核心机制诊断。本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。本地只执行 observation-safe 评测状态机；没有调用 12 个外部 LLM。三种子结果见 metrics/mechanism-seeds42-44.json。统一 receipt 标记 diagnostic_only=true，不会被公开看板当成完整能力提升。  Agent 评测 社会推理 Agent 评测与可靠性：如何知道真的做对了 fuse-evaluator本地执行了哪些边界，是否调用十二外部LLM？ 只执行observation-safe评测状态机，未调用该外部模型矩阵。公开观察与私有动机分开投影，不能把包含gold字段的内部对象直接传给代理回调。 例如评分器知道真实关系，不代表助手输入也能拿到这列。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-e135e56517048e10">fuse-evaluator本地执行了哪些边界，是否调用十二外部LLM？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afuse-evaluator">Verifiable Social Reasoning for LLM Assistants</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Research / Hebrew University of Jerusalem / University of Cambridge</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>只执行observation-safe评测状态机，未调用该外部模型矩阵。公开观察与私有动机分开投影，不能把包含gold字段的内部对象直接传给代理回调。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如评分器知道真实关系，不代表助手输入也能拿到这列。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.17496">原论文</a> · <a href="../../../../agent-research/2609.17496-fuse-evaluator/">实现解读</a> · <a href="#qa-e135e56517048e10">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:silr" data-paper-title="SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents Agent Institute of Science Tokyo 2026-09-03 系统已经违规时，安全门不能简单拒绝所有仍不安全的动作，而要允许逐步恢复。SiLR 先 shadow-execute 提案，再比较每个受约束分支的严重度；只有在乘积序上不恶化的动作可进入真实环境，同一结构信号还能作为 GRPO 过程奖励。 复现级别：CPU 准入算子。复现级别：CPU 准入算子。ShadowGate 在真实传入的 simulator 深拷贝上执行动作，比较逐分支严重度；legacy 文本 mini-suite 没有 simulator，不生成安全或过程奖励结论。本实现不替代真实系统 simulator；没有确定性、覆盖充分的 verifier 时不能据此宣称安全。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Structure-preserving verifier and reward Agent 评测与可靠性：如何知道真的做对了 SiLR的shadow-execute是在真实执行出错后撤销动作吗？ 不是。它先在影子执行路径评估提案造成的状态，再由安全门决定是否进入真实环境。提案评估与真实副作用必须分开；若先真正执行再检查，就无法据同一门控声称阻止了违规动作，尤其是不能撤销的副作用。 教学例子：先模拟一项配置修改会触及哪些约束，再决定是否提交；不是实际改坏配置后才检查并尝试回滚。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-silr-f498d510" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-0f68f6731f7ec1f4">SiLR的shadow-execute是在真实执行出错后撤销动作吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asilr">SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Science Tokyo</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。它先在影子执行路径评估提案造成的状态，再由安全门决定是否进入真实环境。提案评估与真实副作用必须分开；若先真正执行再检查，就无法据同一门控声称阻止了违规动作，尤其是不能撤销的副作用。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>先模拟一项配置修改会触及哪些约束，再决定是否提交；不是实际改坏配置后才检查并尝试回滚。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04629">原论文</a> · <a href="../../../../agent-research/2609.04629-silr/">实现解读</a> · <a href="#qa-0f68f6731f7ec1f4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:silr" data-paper-title="SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents Agent Institute of Science Tokyo 2026-09-03 系统已经违规时，安全门不能简单拒绝所有仍不安全的动作，而要允许逐步恢复。SiLR 先 shadow-execute 提案，再比较每个受约束分支的严重度；只有在乘积序上不恶化的动作可进入真实环境，同一结构信号还能作为 GRPO 过程奖励。 复现级别：CPU 准入算子。复现级别：CPU 准入算子。ShadowGate 在真实传入的 simulator 深拷贝上执行动作，比较逐分支严重度；legacy 文本 mini-suite 没有 simulator，不生成安全或过程奖励结论。本实现不替代真实系统 simulator；没有确定性、覆盖充分的 verifier 时不能据此宣称安全。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Structure-preserving verifier and reward Agent 评测与可靠性：如何知道真的做对了 系统已违规时，为什么安全门不能把所有仍不完全安全的动作都拒绝？ 恢复可能需要经过尚有残余风险的中间状态，全拒绝会让系统被锁死。SiLR 先 shadow-execute，再要求每个受约束分支的严重度都不恶化，允许逐步改善；只看一个总分可能掩盖某分支变坏，shadow 结果也仍需对应真实执行合同。 例如两个权限问题中先撤销一个，另一个暂时保留，整体尚未完全安全却是有效恢复；不能要求一步消除全部问题才允许动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-2e48dd4d8eb6dd50">系统已违规时，为什么安全门不能把所有仍不完全安全的动作都拒绝？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asilr">SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Science Tokyo</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>恢复可能需要经过尚有残余风险的中间状态，全拒绝会让系统被锁死。SiLR 先 shadow-execute，再要求每个受约束分支的严重度都不恶化，允许逐步改善；只看一个总分可能掩盖某分支变坏，shadow 结果也仍需对应真实执行合同。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两个权限问题中先撤销一个，另一个暂时保留，整体尚未完全安全却是有效恢复；不能要求一步消除全部问题才允许动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04629">原论文</a> · <a href="../../../../agent-research/2609.04629-silr/">实现解读</a> · <a href="#qa-2e48dd4d8eb6dd50">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:silr" data-paper-title="SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents Agent Institute of Science Tokyo 2026-09-03 系统已经违规时，安全门不能简单拒绝所有仍不安全的动作，而要允许逐步恢复。SiLR 先 shadow-execute 提案，再比较每个受约束分支的严重度；只有在乘积序上不恶化的动作可进入真实环境，同一结构信号还能作为 GRPO 过程奖励。 复现级别：CPU 准入算子。复现级别：CPU 准入算子。ShadowGate 在真实传入的 simulator 深拷贝上执行动作，比较逐分支严重度；legacy 文本 mini-suite 没有 simulator，不生成安全或过程奖励结论。本实现不替代真实系统 simulator；没有确定性、覆盖充分的 verifier 时不能据此宣称安全。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Structure-preserving verifier and reward Agent 评测与可靠性：如何知道真的做对了 乘积序与把多个违规程度加成一分有什么差别？ 向量逐分支不恶化禁止用一处改善补偿另一处恶化，标量总分可能掩盖这种交换。约束结构必须保留，不能用某个权重总和声称等价安全门。 例如省了存储却扩大权限，总分下降也不满足每分支都不恶化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-28c3f5f612d987c1">乘积序与把多个违规程度加成一分有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asilr">SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Science Tokyo</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>向量逐分支不恶化禁止用一处改善补偿另一处恶化，标量总分可能掩盖这种交换。约束结构必须保留，不能用某个权重总和声称等价安全门。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如省了存储却扩大权限，总分下降也不满足每分支都不恶化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04629">原论文</a> · <a href="../../../../agent-research/2609.04629-silr/">实现解读</a> · <a href="#qa-28c3f5f612d987c1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:silr" data-paper-title="SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents Agent Institute of Science Tokyo 2026-09-03 系统已经违规时，安全门不能简单拒绝所有仍不安全的动作，而要允许逐步恢复。SiLR 先 shadow-execute 提案，再比较每个受约束分支的严重度；只有在乘积序上不恶化的动作可进入真实环境，同一结构信号还能作为 GRPO 过程奖励。 复现级别：CPU 准入算子。复现级别：CPU 准入算子。ShadowGate 在真实传入的 simulator 深拷贝上执行动作，比较逐分支严重度；legacy 文本 mini-suite 没有 simulator，不生成安全或过程奖励结论。本实现不替代真实系统 simulator；没有确定性、覆盖充分的 verifier 时不能据此宣称安全。旧版直接返回评测标签，原准确率/计划成功率作废。入口现在只接收 task_id、intent、context；读取 answer、plan 或隐藏 required_tools 会在回归测试中报错。  Structure-preserving verifier and reward Agent 评测与可靠性：如何知道真的做对了 SiLR的shadow执行可以用不可靠模拟器替代真实效果吗？ 不能据此宣称安全，准入依赖确定且覆盖充分的验证器。先shadow再比较状态，再真实执行；未建真实simulator时，本地只验证结构化判据与过程信号。 例如模拟没建模删除副作用，向量看似不变也可能遗漏真实风险。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-f4644d5aa5ea7b39">SiLR的shadow执行可以用不可靠模拟器替代真实效果吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asilr">SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Institute of Science Tokyo</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能据此宣称安全，准入依赖确定且覆盖充分的验证器。先shadow再比较状态，再真实执行；未建真实simulator时，本地只验证结构化判据与过程信号。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模拟没建模删除副作用，向量看似不变也可能遗漏真实风险。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2609.04629">原论文</a> · <a href="../../../../agent-research/2609.04629-silr/">实现解读</a> · <a href="#qa-f4644d5aa5ea7b39">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:redevoagent" data-paper-title="RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution Agent City University of Hong Kong 2026-08-27 RedEvoAgent 不直接检索冗长攻击轨迹，而把跨案例经验蒸馏成可读技能；只归因真正决定成败的工具，并且新技能必须在留出验证集上优于 incumbent 才能晋级。 复现级别：核心机制 + deterministic mini-suite。复现级别：核心机制 + deterministic mini-suite。实现工具效果画像、Deciding-Tool Attribution 和 held-out validation ratchet。未对真实产品 Agent 执行越权攻击；mini-suite 只验证安全的技能更新控制流。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300；关键价值是 validation ratchet/归因计数，而非简单任务的满分。  红队技能进化 Agent 评测与可靠性：如何知道真的做对了 RedEvoAgent为什么把经验蒸馏成技能而非保存完整轨迹？ 长轨迹噪声和上下文成本高，抽象可读技能更利复用；工具归因只聚焦真正决定成败环节。抽象仍可能丢细节，技能需留出验证后晋级。 例如从一次长排查中提炼先验证权限边界，而不整段复制所有无关尝试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-redevoagent-15b9a312" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-ca939019ba0967a7">RedEvoAgent为什么把经验蒸馏成技能而非保存完整轨迹？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aredevoagent">RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>长轨迹噪声和上下文成本高，抽象可读技能更利复用；工具归因只聚焦真正决定成败环节。抽象仍可能丢细节，技能需留出验证后晋级。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如从一次长排查中提炼先验证权限边界，而不整段复制所有无关尝试。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27439">原论文</a> · <a href="../../../../agent-research/2608.27439-redevoagent/">实现解读</a> · <a href="#qa-ca939019ba0967a7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:redevoagent" data-paper-title="RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution Agent City University of Hong Kong 2026-08-27 RedEvoAgent 不直接检索冗长攻击轨迹，而把跨案例经验蒸馏成可读技能；只归因真正决定成败的工具，并且新技能必须在留出验证集上优于 incumbent 才能晋级。 复现级别：核心机制 + deterministic mini-suite。复现级别：核心机制 + deterministic mini-suite。实现工具效果画像、Deciding-Tool Attribution 和 held-out validation ratchet。未对真实产品 Agent 执行越权攻击；mini-suite 只验证安全的技能更新控制流。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300；关键价值是 validation ratchet/归因计数，而非简单任务的满分。  红队技能进化 Agent 评测与可靠性：如何知道真的做对了 为什么经验技能晋级要在留出集优于 incumbent，而非只看原攻击轨迹成功？ 原轨迹只能证明一次情境有效，技能抽象可能过拟合措辞或误把无关工具当关键因素。留出比较检验复用价值，严格提升才替换现任，避免持续累加低质经验；可读技能与真实执行之间仍需验证，本地筛选器不能代替完整评测行为。 例如一条审计经验只在某个样例有效，换同类新场景失效，就不应仅凭原日志成功把它升级为默认技能。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-f7faccca6551b9dd">为什么经验技能晋级要在留出集优于 incumbent，而非只看原攻击轨迹成功？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aredevoagent">RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原轨迹只能证明一次情境有效，技能抽象可能过拟合措辞或误把无关工具当关键因素。留出比较检验复用价值，严格提升才替换现任，避免持续累加低质经验；可读技能与真实执行之间仍需验证，本地筛选器不能代替完整评测行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一条审计经验只在某个样例有效，换同类新场景失效，就不应仅凭原日志成功把它升级为默认技能。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27439">原论文</a> · <a href="../../../../agent-research/2608.27439-redevoagent/">实现解读</a> · <a href="#qa-f7faccca6551b9dd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:redevoagent" data-paper-title="RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution Agent City University of Hong Kong 2026-08-27 RedEvoAgent 不直接检索冗长攻击轨迹，而把跨案例经验蒸馏成可读技能；只归因真正决定成败的工具，并且新技能必须在留出验证集上优于 incumbent 才能晋级。 复现级别：核心机制 + deterministic mini-suite。复现级别：核心机制 + deterministic mini-suite。实现工具效果画像、Deciding-Tool Attribution 和 held-out validation ratchet。未对真实产品 Agent 执行越权攻击；mini-suite 只验证安全的技能更新控制流。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300；关键价值是 validation ratchet/归因计数，而非简单任务的满分。  红队技能进化 Agent 评测与可靠性：如何知道真的做对了 RedEvoAgent只归因决定成败的工具，与给整条成功轨迹的所有工具记功有什么区别？ 整条轨迹成功不说明每次工具调用都有贡献，等额记功会把无关步骤也固化成技能。决定性归因尝试保留真正改变攻击结果的工具经验，减少技能库噪声。这里比较信用对象，不能把一次归因分数当成已识别的普遍因果规律。 教学例子：轨迹先查一份无关页面，后用关键工具触发结果；成功标签不应让前一次无关查询自动成为必需技能。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-e61370a89e35777a">RedEvoAgent只归因决定成败的工具，与给整条成功轨迹的所有工具记功有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aredevoagent">RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>整条轨迹成功不说明每次工具调用都有贡献，等额记功会把无关步骤也固化成技能。决定性归因尝试保留真正改变攻击结果的工具经验，减少技能库噪声。这里比较信用对象，不能把一次归因分数当成已识别的普遍因果规律。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>轨迹先查一份无关页面，后用关键工具触发结果；成功标签不应让前一次无关查询自动成为必需技能。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27439">原论文</a> · <a href="../../../../agent-research/2608.27439-redevoagent/">实现解读</a> · <a href="#qa-e61370a89e35777a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:redevoagent" data-paper-title="RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution Agent City University of Hong Kong 2026-08-27 RedEvoAgent 不直接检索冗长攻击轨迹，而把跨案例经验蒸馏成可读技能；只归因真正决定成败的工具，并且新技能必须在留出验证集上优于 incumbent 才能晋级。 复现级别：核心机制 + deterministic mini-suite。复现级别：核心机制 + deterministic mini-suite。实现工具效果画像、Deciding-Tool Attribution 和 held-out validation ratchet。未对真实产品 Agent 执行越权攻击；mini-suite 只验证安全的技能更新控制流。planbench-mini、120 episodes：joint success 1.0000、average cost 0.4300；关键价值是 validation ratchet/归因计数，而非简单任务的满分。  红队技能进化 Agent 评测与可靠性：如何知道真的做对了 RedEvoAgent本地是否已对真实产品执行红队攻击？ 没有，安全mini-suite只验证归因与技能更新控制流。公开产物回放不等于新外部攻击，技能来源、评估切分与替换证据需要记录，不把日志重放当真实执行。 例如加载已有结果文件，只说明能读协议，不说明刚完成一次攻击。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-1e193e5815d941ea">RedEvoAgent本地是否已对真实产品执行红队攻击？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aredevoagent">RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · City University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，安全mini-suite只验证归因与技能更新控制流。公开产物回放不等于新外部攻击，技能来源、评估切分与替换证据需要记录，不把日志重放当真实执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如加载已有结果文件，只说明能读协议，不说明刚完成一次攻击。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.27439">原论文</a> · <a href="../../../../agent-research/2608.27439-redevoagent/">实现解读</a> · <a href="#qa-1e193e5815d941ea">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spec-driven-tests" data-paper-title="Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation Agent Google 2026-08-17 直接让模型编写单元测试，可能遗漏输入边界或隐含的行为约定。本文先让Agent读取修复后的源码，写出每个代码单元的描述、前置条件、后置条件与测试建议；把条件标为已测试或未测试，保存为.spec.md，之后才允许生成测试。中间可由开发者修订规范；论文自动比较没有启用人工干预。 成本过高，不复现（审查 DONE）。L1协议诊断，不是代码Agent能力复现。三seed的确定性小整数fixture检查阶段顺序、公共字段隔离、相同测试双执行、非法源码修改拒绝、编译错误负控及按bug汇总。回调并非LLM，actual_llm_calls=0；其通过只是协议工作正常，不是Agent成功率。CPU诊断指标 Specification保存唯一代码单元及D/Pre/Post/Sug，输出Markdown；未测试条件须有建议。本地结构校验比论文提示约束更严格，但不把它当语义正确性证明。  工具使用 代码 Agent 与测试 Agent 评测与可靠性：如何知道真的做对了 规范驱动测试里的Pre、Post和Sug分别是什么，测试建议能代替行为契约吗？ Pre约束调用前应满足的条件，Post描述满足前提后应得到的行为，Sug提示怎样验证这些条件。建议不是函数契约本身；先把合法输入与预期结果写清，再标出已测和未测部分，才能判断生成测试遗漏了什么。 教学例子：排序函数的Pre可限制输入可比较，Post要求结果有序且元素不变，Sug再建议检查重复值和空列表。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-spec-driven-tests-4c06eb29" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-f1fb84391154bc6c">规范驱动测试里的Pre、Post和Sug分别是什么，测试建议能代替行为契约吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspec-driven-tests">Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>Pre约束调用前应满足的条件，Post描述满足前提后应得到的行为，Sug提示怎样验证这些条件。建议不是函数契约本身；先把合法输入与预期结果写清，再标出已测和未测部分，才能判断生成测试遗漏了什么。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>排序函数的Pre可限制输入可比较，Post要求结果有序且元素不变，Sug再建议检查重复值和空列表。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17177v1">原论文</a> · <a href="../../../../agent-research/2608.17177-spec-driven-tests/">实现解读</a> · <a href="#qa-f1fb84391154bc6c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spec-driven-tests" data-paper-title="Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation Agent Google 2026-08-17 直接让模型编写单元测试，可能遗漏输入边界或隐含的行为约定。本文先让Agent读取修复后的源码，写出每个代码单元的描述、前置条件、后置条件与测试建议；把条件标为已测试或未测试，保存为.spec.md，之后才允许生成测试。中间可由开发者修订规范；论文自动比较没有启用人工干预。 成本过高，不复现（审查 DONE）。L1协议诊断，不是代码Agent能力复现。三seed的确定性小整数fixture检查阶段顺序、公共字段隔离、相同测试双执行、非法源码修改拒绝、编译错误负控及按bug汇总。回调并非LLM，actual_llm_calls=0；其通过只是协议工作正常，不是Agent成功率。CPU诊断指标 Specification保存唯一代码单元及D/Pre/Post/Sug，输出Markdown；未测试条件须有建议。本地结构校验比论文提示约束更严格，但不把它当语义正确性证明。  工具使用 代码 Agent 与测试 Agent 评测与可靠性：如何知道真的做对了 先写前后置条件再生成测试，为什么能暴露直接写单测时的覆盖盲点？ 规范把每个代码单元的输入限制与应保证行为显式列出，再标记已测未测条件，测试生成才有可检查的覆盖目标。它仍来源于读取源码与解释，不能自动保证规范忠实；论文自动比较没有人工修订，也不应把可选开发者步骤算成已执行条件。 例如函数要求空输入返回空列表，规范可把它列为未测后置条件；直接模仿现有正常样例写测试可能一直漏掉边界。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d27f4aa512ac8b25">先写前后置条件再生成测试，为什么能暴露直接写单测时的覆盖盲点？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspec-driven-tests">Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>规范把每个代码单元的输入限制与应保证行为显式列出，再标记已测未测条件，测试生成才有可检查的覆盖目标。它仍来源于读取源码与解释，不能自动保证规范忠实；论文自动比较没有人工修订，也不应把可选开发者步骤算成已执行条件。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如函数要求空输入返回空列表，规范可把它列为未测后置条件；直接模仿现有正常样例写测试可能一直漏掉边界。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17177v1">原论文</a> · <a href="../../../../agent-research/2608.17177-spec-driven-tests/">实现解读</a> · <a href="#qa-d27f4aa512ac8b25">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spec-driven-tests" data-paper-title="Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation Agent Google 2026-08-17 直接让模型编写单元测试，可能遗漏输入边界或隐含的行为约定。本文先让Agent读取修复后的源码，写出每个代码单元的描述、前置条件、后置条件与测试建议；把条件标为已测试或未测试，保存为.spec.md，之后才允许生成测试。中间可由开发者修订规范；论文自动比较没有启用人工干预。 成本过高，不复现（审查 DONE）。L1协议诊断，不是代码Agent能力复现。三seed的确定性小整数fixture检查阶段顺序、公共字段隔离、相同测试双执行、非法源码修改拒绝、编译错误负控及按bug汇总。回调并非LLM，actual_llm_calls=0；其通过只是协议工作正常，不是Agent成功率。CPU诊断指标 Specification保存唯一代码单元及D/Pre/Post/Sug，输出Markdown；未测试条件须有建议。本地结构校验比论文提示约束更严格，但不把它当语义正确性证明。  工具使用 代码 Agent 与测试 Agent 评测与可靠性：如何知道真的做对了 fixed-source输入与向测试生成器暴露历史bug有什么区别？ 原流程只读修复后源码和公开需求，buggy版本由私有评价器使用。给出旧补丁或bug位置会改变任务难度，不能当同协议测试发现能力。 例如知道哪行曾经错过，可轻易定向写测试，却不是独立契约推导。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-6cc9079f0e3f1ce6">fixed-source输入与向测试生成器暴露历史bug有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspec-driven-tests">Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>原流程只读修复后源码和公开需求，buggy版本由私有评价器使用。给出旧补丁或bug位置会改变任务难度，不能当同协议测试发现能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如知道哪行曾经错过，可轻易定向写测试，却不是独立契约推导。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17177v1">原论文</a> · <a href="../../../../agent-research/2608.17177-spec-driven-tests/">实现解读</a> · <a href="#qa-6cc9079f0e3f1ce6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:spec-driven-tests" data-paper-title="Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation Agent Google 2026-08-17 直接让模型编写单元测试，可能遗漏输入边界或隐含的行为约定。本文先让Agent读取修复后的源码，写出每个代码单元的描述、前置条件、后置条件与测试建议；把条件标为已测试或未测试，保存为.spec.md，之后才允许生成测试。中间可由开发者修订规范；论文自动比较没有启用人工干预。 成本过高，不复现（审查 DONE）。L1协议诊断，不是代码Agent能力复现。三seed的确定性小整数fixture检查阶段顺序、公共字段隔离、相同测试双执行、非法源码修改拒绝、编译错误负控及按bug汇总。回调并非LLM，actual_llm_calls=0；其通过只是协议工作正常，不是Agent成功率。CPU诊断指标 Specification保存唯一代码单元及D/Pre/Post/Sug，输出Markdown；未测试条件须有建议。本地结构校验比论文提示约束更严格，但不把它当语义正确性证明。  工具使用 代码 Agent 与测试 Agent 评测与可靠性：如何知道真的做对了 编译失败或修改被测源码算成功检出bug吗？ 都不算。相同测试先在fixed编译通过，在buggy编译成功后出现真实断言失败才检出；非法文件修改使运行作废，审计需外部可信diff，不能信模型自报。 例如故意写不存在API导致旧版编译错，不是有效回归测试。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b7c7b70e668e862c">编译失败或修改被测源码算成功检出bug吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aspec-driven-tests">Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>都不算。相同测试先在fixed编译通过，在buggy编译成功后出现真实断言失败才检出；非法文件修改使运行作废，审计需外部可信diff，不能信模型自报。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如故意写不存在API导致旧版编译错，不是有效回归测试。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.17177v1">原论文</a> · <a href="../../../../agent-research/2608.17177-spec-driven-tests/">实现解读</a> · <a href="#qa-b7c7b70e668e862c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnessopt-bench" data-paper-title="HarnessOpt-Bench: Evaluating LLMs at Harness Optimization" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="HarnessOpt-Bench: Evaluating LLMs at Harness Optimization Agent Scale AI 2026-08-06 主题：Harness 优化评测。在固定 target-evaluation 预算下，让优化器修改 prompt、工具、控制流和记忆；隐藏测试集与可信执行环境隔离搜索反馈，保留候选版本以供审计。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness 优化评测算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness 优化评测 Agent 评测与可靠性：如何知道真的做对了 HarnessOpt-Bench允许优化器改哪些东西，是重新训练底层模型吗？ 搜索对象是prompt、工具、控制流与记忆等harness组件，评测关注在规定目标评估预算内改进这些组件的能力。不能把任意底层模型重训、增加隐藏训练数据也默认为同一搜索空间；候选版本与允许改动范围都应留痕。 教学例子：优化器可试不同上下文压缩策略并评估；若偷偷换更强底座，收益便不能全归于harness优化。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-harnessopt-bench-502f5ddb" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-b32f7ffe5fc0c451">HarnessOpt-Bench允许优化器改哪些东西，是重新训练底层模型吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnessopt-bench">HarnessOpt-Bench: Evaluating LLMs at Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Scale AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>搜索对象是prompt、工具、控制流与记忆等harness组件，评测关注在规定目标评估预算内改进这些组件的能力。不能把任意底层模型重训、增加隐藏训练数据也默认为同一搜索空间；候选版本与允许改动范围都应留痕。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>优化器可试不同上下文压缩策略并评估；若偷偷换更强底座，收益便不能全归于harness优化。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06301">原论文</a> · <a href="../../../../agent-research/2608.06301-harnessopt-bench/">实现解读</a> · <a href="#qa-b32f7ffe5fc0c451">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnessopt-bench" data-paper-title="HarnessOpt-Bench: Evaluating LLMs at Harness Optimization" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="HarnessOpt-Bench: Evaluating LLMs at Harness Optimization Agent Scale AI 2026-08-06 主题：Harness 优化评测。在固定 target-evaluation 预算下，让优化器修改 prompt、工具、控制流和记忆；隐藏测试集与可信执行环境隔离搜索反馈，保留候选版本以供审计。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness 优化评测算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness 优化评测 Agent 评测与可靠性：如何知道真的做对了 为什么评测 harness 优化器要固定 target-evaluation 预算，而不只比较最终最高分？ 更多评测本身就提供更多搜索机会，不控预算会混淆优化能力与资源投入。隐藏测试隔离候选选择，可信环境及版本档案支持审计改了什么；报告相对收益还需注意基线尺度，不能把搜索反馈里见过的最佳候选成绩当最终未见表现。 例如一套优化器试一千次、另一套只试十次，即便前者最后更高，也不能直接说明更会优化；应先匹配评测调用预算。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-3dd81229ff5366d7">为什么评测 harness 优化器要固定 target-evaluation 预算，而不只比较最终最高分？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnessopt-bench">HarnessOpt-Bench: Evaluating LLMs at Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Scale AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>更多评测本身就提供更多搜索机会，不控预算会混淆优化能力与资源投入。隐藏测试隔离候选选择，可信环境及版本档案支持审计改了什么；报告相对收益还需注意基线尺度，不能把搜索反馈里见过的最佳候选成绩当最终未见表现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一套优化器试一千次、另一套只试十次，即便前者最后更高，也不能直接说明更会优化；应先匹配评测调用预算。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06301">原论文</a> · <a href="../../../../agent-research/2608.06301-harnessopt-bench/">实现解读</a> · <a href="#qa-3dd81229ff5366d7">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnessopt-bench" data-paper-title="HarnessOpt-Bench: Evaluating LLMs at Harness Optimization" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="HarnessOpt-Bench: Evaluating LLMs at Harness Optimization Agent Scale AI 2026-08-06 主题：Harness 优化评测。在固定 target-evaluation 预算下，让优化器修改 prompt、工具、控制流和记忆；隐藏测试集与可信执行环境隔离搜索反馈，保留候选版本以供审计。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness 优化评测算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness 优化评测 Agent 评测与可靠性：如何知道真的做对了 开放搜索反馈与隐藏test为何必须分离？ 优化过程会利用可见反馈选版本，隐藏集用于最终泛化。若每次搜索都看test，就把基准变成调参集，得分提高不能解释为新任务能力。 例如试几十版后按测试最高挑一版，会高估未见效果。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-726b6cc81a06976f">开放搜索反馈与隐藏test为何必须分离？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnessopt-bench">HarnessOpt-Bench: Evaluating LLMs at Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Scale AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>优化过程会利用可见反馈选版本，隐藏集用于最终泛化。若每次搜索都看test，就把基准变成调参集，得分提高不能解释为新任务能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如试几十版后按测试最高挑一版，会高估未见效果。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06301">原论文</a> · <a href="../../../../agent-research/2608.06301-harnessopt-bench/">实现解读</a> · <a href="#qa-726b6cc81a06976f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:harnessopt-bench" data-paper-title="HarnessOpt-Bench: Evaluating LLMs at Harness Optimization" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="HarnessOpt-Bench: Evaluating LLMs at Harness Optimization Agent Scale AI 2026-08-06 主题：Harness 优化评测。在固定 target-evaluation 预算下，让优化器修改 prompt、工具、控制流和记忆；隐藏测试集与可信执行环境隔离搜索反馈，保留候选版本以供审计。 复现级别：核心机制 mini-suite。复现级别：核心机制 mini-suite。本地实现执行论文特有的 Harness 优化评测算子；不把确定性小型评测写成论文完整复现。复现论文特有的状态、信用或选择算子，而非只改方法名。稳定指标保存在本论文目录的 metrics/planbench-mini-seed42.json，不提交 checkpoint 或原始运行目录。  Harness 优化评测 Agent 评测与可靠性：如何知道真的做对了 本地候选注册能替代可信执行与版本审计吗？ 不能，需要真实预算计数、候选快照与隔离执行，未运行原模型或环境不能冒称benchmark成绩。相对提升公式在基线近零时需明确epsilon而非隐改分母。 例如配置列表新增一个名字，不代表优化器已经实际改并测试它。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b98c65c6671a3fc9">本地候选注册能替代可信执行与版本审计吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aharnessopt-bench">HarnessOpt-Bench: Evaluating LLMs at Harness Optimization</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Scale AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，需要真实预算计数、候选快照与隔离执行，未运行原模型或环境不能冒称benchmark成绩。相对提升公式在基线近零时需明确epsilon而非隐改分母。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如配置列表新增一个名字，不代表优化器已经实际改并测试它。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2608.06301">原论文</a> · <a href="../../../../agent-research/2608.06301-harnessopt-bench/">实现解读</a> · <a href="#qa-b98c65c6671a3fc9">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:finance-harness-protocol" data-paper-title="FinanceHarness: Autonomous Financial Deep Research Framework" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="FinanceHarness: Autonomous Financial Deep Research Framework Agent Google Cloud AI Research 2026-07-30 FinanceHarness 围绕时点限定的搜索环境组织金融工具、分层加载技能与报告证据；FinanceGym 再把评分分为截止日前可检索的证据和只能在截止日后核实的预测。Agent 只能看到问题与截止日，thesis、评分 rubric、未来证据留在提交后的评测器。 完整实验成本过高，不复现（审查 DONE）；诊断使用历史/当日/未来/未知日期构造负控，另验证 live-web 审计会使运行无效，以及 1 条/3 条 rubric 的两题应均分为 0.5 而非 0.25；L1 纯 CPU 协议组件，diagnostic only，不是金融调研 Agent 能力，不提供投资建议。完整实验成本过高，不复现（审查 DONE）；无能力 adapter、未接入 Evolve。PointInTimeStore 保留外部检索排名，但过滤未来/日期未知文档，read 再独立检查，防止跳过搜索直接读未来材料。提交检查记录 live-web 使用或未读引用；触发后不可评分。  评测与可验证Agent 时点隔离与深度调研 Agent 评测与可靠性：如何知道真的做对了 FinanceGym的rubric分数3，是3%的成功率吗？ 不是。单个rubric采用0到4的五级评分，3只是该尺度上的等级。题内先按四分满分归一，才能与其他题共同平均；分数解释仍取决于具体rubric。不要把原始等级、题目归一分和整体Outcome当成同一个量。 教学例子：教学用一题两个rubric分别3分和1分，题内归一分是(3+1)/(4×2)=0.5，不是4%或两题命中率。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-finance-harness-protocol-8c1ac9fa" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bbb3ce54beabf3be">FinanceGym的rubric分数3，是3%的成功率吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afinance-harness-protocol">FinanceHarness: Autonomous Financial Deep Research Framework</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。单个rubric采用0到4的五级评分，3只是该尺度上的等级。题内先按四分满分归一，才能与其他题共同平均；分数解释仍取决于具体rubric。不要把原始等级、题目归一分和整体Outcome当成同一个量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>教学用一题两个rubric分别3分和1分，题内归一分是(3+1)/(4×2)=0.5，不是4%或两题命中率。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27853v1">原论文</a> · <a href="../../../../agent-research/2607.27853-finance-harness-protocol/">实现解读</a> · <a href="#qa-bbb3ce54beabf3be">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:finance-harness-protocol" data-paper-title="FinanceHarness: Autonomous Financial Deep Research Framework" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="FinanceHarness: Autonomous Financial Deep Research Framework Agent Google Cloud AI Research 2026-07-30 FinanceHarness 围绕时点限定的搜索环境组织金融工具、分层加载技能与报告证据；FinanceGym 再把评分分为截止日前可检索的证据和只能在截止日后核实的预测。Agent 只能看到问题与截止日，thesis、评分 rubric、未来证据留在提交后的评测器。 完整实验成本过高，不复现（审查 DONE）；诊断使用历史/当日/未来/未知日期构造负控，另验证 live-web 审计会使运行无效，以及 1 条/3 条 rubric 的两题应均分为 0.5 而非 0.25；L1 纯 CPU 协议组件，diagnostic only，不是金融调研 Agent 能力，不提供投资建议。完整实验成本过高，不复现（审查 DONE）；无能力 adapter、未接入 Evolve。PointInTimeStore 保留外部检索排名，但过滤未来/日期未知文档，read 再独立检查，防止跳过搜索直接读未来材料。提交检查记录 live-web 使用或未读引用；触发后不可评分。  评测与可验证Agent 时点隔离与深度调研 Agent 评测与可靠性：如何知道真的做对了 截止日后可核实的预测，为什么必须留在提交后的评测器而非给研究 Agent？ 研究输入只能使用截止日前已可检索证据，未来材料若提前出现会把预测变成复述。thesis 与 rubric 也留在评分侧，分题归一后再平均以免题目条目数改变权重；时点泄漏使运行无效，不是随意记零或删行后继续汇总。 例如报告预测下一季度趋势，后来公布的业绩只能在提交后核查，不能倒填进截止日前证据包让模型看似提前判断正确。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9ffeae55e9d1c6ba">截止日后可核实的预测，为什么必须留在提交后的评测器而非给研究 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afinance-harness-protocol">FinanceHarness: Autonomous Financial Deep Research Framework</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究输入只能使用截止日前已可检索证据，未来材料若提前出现会把预测变成复述。thesis 与 rubric 也留在评分侧，分题归一后再平均以免题目条目数改变权重；时点泄漏使运行无效，不是随意记零或删行后继续汇总。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如报告预测下一季度趋势，后来公布的业绩只能在提交后核查，不能倒填进截止日前证据包让模型看似提前判断正确。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27853v1">原论文</a> · <a href="../../../../agent-research/2607.27853-finance-harness-protocol/">实现解读</a> · <a href="#qa-9ffeae55e9d1c6ba">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:finance-harness-protocol" data-paper-title="FinanceHarness: Autonomous Financial Deep Research Framework" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="FinanceHarness: Autonomous Financial Deep Research Framework Agent Google Cloud AI Research 2026-07-30 FinanceHarness 围绕时点限定的搜索环境组织金融工具、分层加载技能与报告证据；FinanceGym 再把评分分为截止日前可检索的证据和只能在截止日后核实的预测。Agent 只能看到问题与截止日，thesis、评分 rubric、未来证据留在提交后的评测器。 完整实验成本过高，不复现（审查 DONE）；诊断使用历史/当日/未来/未知日期构造负控，另验证 live-web 审计会使运行无效，以及 1 条/3 条 rubric 的两题应均分为 0.5 而非 0.25；L1 纯 CPU 协议组件，diagnostic only，不是金融调研 Agent 能力，不提供投资建议。完整实验成本过高，不复现（审查 DONE）；无能力 adapter、未接入 Evolve。PointInTimeStore 保留外部检索排名，但过滤未来/日期未知文档，read 再独立检查，防止跳过搜索直接读未来材料。提交检查记录 live-web 使用或未读引用；触发后不可评分。  评测与可验证Agent 时点隔离与深度调研 Agent 评测与可靠性：如何知道真的做对了 逐题等权与把全部rubric混平均有什么差别？ 每题rubric数不同，直接混平均让细项多的题占更多权重；先按题归一再平均保留题级比较。论文五级评分也不能自改为任意连续满分。 例如十条标准的题不应自动比两条标准的题重要五倍。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-a30f6f4a0d087a4a">逐题等权与把全部rubric混平均有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afinance-harness-protocol">FinanceHarness: Autonomous Financial Deep Research Framework</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>每题rubric数不同，直接混平均让细项多的题占更多权重；先按题归一再平均保留题级比较。论文五级评分也不能自改为任意连续满分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如十条标准的题不应自动比两条标准的题重要五倍。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27853v1">原论文</a> · <a href="../../../../agent-research/2607.27853-finance-harness-protocol/">实现解读</a> · <a href="#qa-a30f6f4a0d087a4a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:finance-harness-protocol" data-paper-title="FinanceHarness: Autonomous Financial Deep Research Framework" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="FinanceHarness: Autonomous Financial Deep Research Framework Agent Google Cloud AI Research 2026-07-30 FinanceHarness 围绕时点限定的搜索环境组织金融工具、分层加载技能与报告证据；FinanceGym 再把评分分为截止日前可检索的证据和只能在截止日后核实的预测。Agent 只能看到问题与截止日，thesis、评分 rubric、未来证据留在提交后的评测器。 完整实验成本过高，不复现（审查 DONE）；诊断使用历史/当日/未来/未知日期构造负控，另验证 live-web 审计会使运行无效，以及 1 条/3 条 rubric 的两题应均分为 0.5 而非 0.25；L1 纯 CPU 协议组件，diagnostic only，不是金融调研 Agent 能力，不提供投资建议。完整实验成本过高，不复现（审查 DONE）；无能力 adapter、未接入 Evolve。PointInTimeStore 保留外部检索排名，但过滤未来/日期未知文档，read 再独立检查，防止跳过搜索直接读未来材料。提交检查记录 live-web 使用或未读引用；触发后不可评分。  评测与可验证Agent 时点隔离与深度调研 Agent 评测与可靠性：如何知道真的做对了 金融协议发现时点泄漏后能把该行计零继续报均分吗？ 不能，运行应判无效而非静默删行或置零。文档publication_date必须不晚于cutoff，thesis、rubric与未来证据不可给Agent；这是评测时点协议而非投资建议。 例如工具偶然搜出事后文章，不能假装只是模型答错了一题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-aebea6d3c661cc2f">金融协议发现时点泄漏后能把该行计零继续报均分吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Afinance-harness-protocol">FinanceHarness: Autonomous Financial Deep Research Framework</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，运行应判无效而非静默删行或置零。文档publication_date必须不晚于cutoff，thesis、rubric与未来证据不可给Agent；这是评测时点协议而非投资建议。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具偶然搜出事后文章，不能假装只是模型答错了一题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.27853v1">原论文</a> · <a href="../../../../agent-research/2607.27853-finance-harness-protocol/">实现解读</a> · <a href="#qa-aebea6d3c661cc2f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:os-shepherd" data-paper-title="OSReward / OS-Shepherd" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="OSReward / OS-Shepherd Agent The University of Hong Kong 2026-07-30 电脑操作 Agent 需要 reward model 判断完整轨迹是否真的完成任务，但普通 accuracy 会掩盖“几乎全判成功”的宽松偏差。OSReward 汇集 Windows、macOS、Ubuntu、Android 的人工验证任务与轨迹，同时发布 Hard 和 Multi 子集；统一报告 success recall、fail recall 与两者均值 balanced accuracy，并用 OS-Shepherd-100K 训练开放 9B/35B judge。 本页实现论文的 success/fail 双类召回、balanced accuracy 与 leniency 审计协议；确定性 mini-suite 不冒充官方人工标注轨迹或 OS-Shepherd 模型训练。本地没有下载官方截图轨迹或训练 9B/35B VLM judge，只把论文最重要的评测契约变成可执行基础设施。结果不能与官方模型表直接比较。本地 osreward-mini 覆盖四个平台与四类任务，显式区分“界面有活动”“有完成证据”和“仍有未完成要求”。判分器不能只信 Agent 的成功声明；  CUA Reward 评测 Agent 评测与可靠性：如何知道真的做对了 OS-Shepherd在电脑任务里扮演操作Agent，还是判断轨迹成败的judge？ 它是评估完整电脑操作轨迹是否成功的judge；执行点击、输入等动作的是受评操作Agent。OSReward提供人工验证任务与轨迹，用于检查这类奖励模型。先区分执行者与评分者，才能避免把judge识别成功的能力误称作自行完成任务。 教学例子：操作Agent尝试保存文件，judge根据轨迹判断是否真的保存；judge判对并不代表它执行过保存动作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-os-shepherd-3f53da9c" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-08f584e8368a5348">OS-Shepherd在电脑任务里扮演操作Agent，还是判断轨迹成败的judge？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aos-shepherd">OSReward / OS-Shepherd</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它是评估完整电脑操作轨迹是否成功的judge；执行点击、输入等动作的是受评操作Agent。OSReward提供人工验证任务与轨迹，用于检查这类奖励模型。先区分执行者与评分者，才能避免把judge识别成功的能力误称作自行完成任务。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>操作Agent尝试保存文件，judge根据轨迹判断是否真的保存；judge判对并不代表它执行过保存动作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28609">原论文</a> · <a href="../../../../agent-research/2607.28609-osreward/">实现解读</a> · <a href="#qa-08f584e8368a5348">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:os-shepherd" data-paper-title="OSReward / OS-Shepherd" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="OSReward / OS-Shepherd Agent The University of Hong Kong 2026-07-30 电脑操作 Agent 需要 reward model 判断完整轨迹是否真的完成任务，但普通 accuracy 会掩盖“几乎全判成功”的宽松偏差。OSReward 汇集 Windows、macOS、Ubuntu、Android 的人工验证任务与轨迹，同时发布 Hard 和 Multi 子集；统一报告 success recall、fail recall 与两者均值 balanced accuracy，并用 OS-Shepherd-100K 训练开放 9B/35B judge。 本页实现论文的 success/fail 双类召回、balanced accuracy 与 leniency 审计协议；确定性 mini-suite 不冒充官方人工标注轨迹或 OS-Shepherd 模型训练。本地没有下载官方截图轨迹或训练 9B/35B VLM judge，只把论文最重要的评测契约变成可执行基础设施。结果不能与官方模型表直接比较。本地 osreward-mini 覆盖四个平台与四类任务，显式区分“界面有活动”“有完成证据”和“仍有未完成要求”。判分器不能只信 Agent 的成功声明；  CUA Reward 评测 Agent 评测与可靠性：如何知道真的做对了 为什么普通 accuracy 会掩盖“几乎全判成功”的 reward model？ 若成功样本占多数，宽松裁判把所有轨迹判成功也可能得到不错总准确率，却漏掉真实失败。分别报告 success recall、fail recall 及其均值能揭示两类能力；跨系统与困难子集还需真实验证标签，不能把几条接口诊断当开放 judge 的能力测量。 例如九成样本成功，全判成功有九成 accuracy，但 fail recall 为零，balanced accuracy 只有一半，暴露对失败完全失明。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-dc27e01fb888a3e5">为什么普通 accuracy 会掩盖“几乎全判成功”的 reward model？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aos-shepherd">OSReward / OS-Shepherd</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>若成功样本占多数，宽松裁判把所有轨迹判成功也可能得到不错总准确率，却漏掉真实失败。分别报告 success recall、fail recall 及其均值能揭示两类能力；跨系统与困难子集还需真实验证标签，不能把几条接口诊断当开放 judge 的能力测量。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如九成样本成功，全判成功有九成 accuracy，但 fail recall 为零，balanced accuracy 只有一半，暴露对失败完全失明。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28609">原论文</a> · <a href="../../../../agent-research/2607.28609-osreward/">实现解读</a> · <a href="#qa-dc27e01fb888a3e5">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:os-shepherd" data-paper-title="OSReward / OS-Shepherd" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="OSReward / OS-Shepherd Agent The University of Hong Kong 2026-07-30 电脑操作 Agent 需要 reward model 判断完整轨迹是否真的完成任务，但普通 accuracy 会掩盖“几乎全判成功”的宽松偏差。OSReward 汇集 Windows、macOS、Ubuntu、Android 的人工验证任务与轨迹，同时发布 Hard 和 Multi 子集；统一报告 success recall、fail recall 与两者均值 balanced accuracy，并用 OS-Shepherd-100K 训练开放 9B/35B judge。 本页实现论文的 success/fail 双类召回、balanced accuracy 与 leniency 审计协议；确定性 mini-suite 不冒充官方人工标注轨迹或 OS-Shepherd 模型训练。本地没有下载官方截图轨迹或训练 9B/35B VLM judge，只把论文最重要的评测契约变成可执行基础设施。结果不能与官方模型表直接比较。本地 osreward-mini 覆盖四个平台与四类任务，显式区分“界面有活动”“有完成证据”和“仍有未完成要求”。判分器不能只信 Agent 的成功声明；  CUA Reward 评测 Agent 评测与可靠性：如何知道真的做对了 judge看末五状态加文本历史，与只看最终截图有什么差别？ 终态截图可能缺少过程和隐性任务条件，历史补证据；但更长输入也带噪声。规定观察协议不同，不能换成任意摘要后仍把分数与原表直接比。 例如窗口最后打开不代表中间文件修改真的保存。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-54e6b7d5ed63c0ae">judge看末五状态加文本历史，与只看最终截图有什么差别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aos-shepherd">OSReward / OS-Shepherd</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>终态截图可能缺少过程和隐性任务条件，历史补证据；但更长输入也带噪声。规定观察协议不同，不能换成任意摘要后仍把分数与原表直接比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如窗口最后打开不代表中间文件修改真的保存。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28609">原论文</a> · <a href="../../../../agent-research/2607.28609-osreward/">实现解读</a> · <a href="#qa-54e6b7d5ed63c0ae">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:os-shepherd" data-paper-title="OSReward / OS-Shepherd" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="OSReward / OS-Shepherd Agent The University of Hong Kong 2026-07-30 电脑操作 Agent 需要 reward model 判断完整轨迹是否真的完成任务，但普通 accuracy 会掩盖“几乎全判成功”的宽松偏差。OSReward 汇集 Windows、macOS、Ubuntu、Android 的人工验证任务与轨迹，同时发布 Hard 和 Multi 子集；统一报告 success recall、fail recall 与两者均值 balanced accuracy，并用 OS-Shepherd-100K 训练开放 9B/35B judge。 本页实现论文的 success/fail 双类召回、balanced accuracy 与 leniency 审计协议；确定性 mini-suite 不冒充官方人工标注轨迹或 OS-Shepherd 模型训练。本地没有下载官方截图轨迹或训练 9B/35B VLM judge，只把论文最重要的评测契约变成可执行基础设施。结果不能与官方模型表直接比较。本地 osreward-mini 覆盖四个平台与四类任务，显式区分“界面有活动”“有完成证据”和“仍有未完成要求”。判分器不能只信 Agent 的成功声明；  CUA Reward 评测 Agent 评测与可靠性：如何知道真的做对了 OSReward本地是否训练了开放9B或35B视觉judge？ 没有，也未下载官方截图轨迹，只实现评测契约。预测verdict与人工标签在评分端汇合，类分母为空应明示，不把自动填充值当真实balanced accuracy。 例如一批没有失败任务，就无法从这批估出正常失败recall。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-833109ee45e06251">OSReward本地是否训练了开放9B或35B视觉judge？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aos-shepherd">OSReward / OS-Shepherd</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · The University of Hong Kong</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，也未下载官方截图轨迹，只实现评测契约。预测verdict与人工标签在评分端汇合，类分母为空应明示，不把自动填充值当真实balanced accuracy。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如一批没有失败任务，就无法从这批估出正常失败recall。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.28609">原论文</a> · <a href="../../../../agent-research/2607.28609-osreward/">实现解读</a> · <a href="#qa-833109ee45e06251">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentdebugx" data-paper-title="AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents Agent University of Illinois Urbana-Champaign 2026-07-21 AgentDebugX 在不可变原始轨迹外叠加 Detect、Attribute、Recover、Rerun 产物。DeepDebug 先全局读，再按单/多 Agent 结构独立定位；候选不一致时交叉质询，最终给出责任步骤、证据和具体建议。修复只生成建议，实际重跑仍经过人或 policy gate；不会从导入日志擅自重放任意外部工具。 完整实验成本过高，不复现（审查 DONE），不会自动重试或进入实现队列。完整配方需要 9B/27B 模型、多轮 Gemini 诊断/搜索、GAIA 工具重跑及多种修复对照；仅研究资料，没有可执行本地 adapter、模型指标或 Evolve 集成。完整实验成本过高，不复现（审查 DONE），不会自动重试或进入实现队列。本地仅核对正文 §3/4 和 Appendix C、固定作者仓库及原图。完整配方需要 9B/27B 模型、多轮 Gemini 诊断/搜索、GAIA 工具重跑及多种修复对照；DeepDebug 约 5 次模型调用，在 25 条样本上平均 12.8K token/诊断。  自进化与经验复用 轨迹调试与因果归因 Agent 评测与可靠性：如何知道真的做对了 AgentDebugX为什么保留不可变原始轨迹再叠诊断？ 失败定位需要完整事件顺序和证据，重写旧日志会掩盖真实行为。Detect、Attribute、Recover和Rerun分别产物可追溯，症状步骤不直接等于根因。 例如工具报错发生在后一步，根因可能是前面传参错误。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-agentdebugx-4b7d80dc" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-a6920629fc1f372f">AgentDebugX为什么保留不可变原始轨迹再叠诊断？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentdebugx">AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>失败定位需要完整事件顺序和证据，重写旧日志会掩盖真实行为。Detect、Attribute、Recover和Rerun分别产物可追溯，症状步骤不直接等于根因。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如工具报错发生在后一步，根因可能是前面传参错误。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与评测边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18754v1">原论文</a> · <a href="../../../../agent-research/2607.18754-agentdebugx/">实现解读</a> · <a href="#qa-a6920629fc1f372f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentdebugx" data-paper-title="AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents Agent University of Illinois Urbana-Champaign 2026-07-21 AgentDebugX 在不可变原始轨迹外叠加 Detect、Attribute、Recover、Rerun 产物。DeepDebug 先全局读，再按单/多 Agent 结构独立定位；候选不一致时交叉质询，最终给出责任步骤、证据和具体建议。修复只生成建议，实际重跑仍经过人或 policy gate；不会从导入日志擅自重放任意外部工具。 完整实验成本过高，不复现（审查 DONE），不会自动重试或进入实现队列。完整配方需要 9B/27B 模型、多轮 Gemini 诊断/搜索、GAIA 工具重跑及多种修复对照；仅研究资料，没有可执行本地 adapter、模型指标或 Evolve 集成。完整实验成本过高，不复现（审查 DONE），不会自动重试或进入实现队列。本地仅核对正文 §3/4 和 Appendix C、固定作者仓库及原图。完整配方需要 9B/27B 模型、多轮 Gemini 诊断/搜索、GAIA 工具重跑及多种修复对照；DeepDebug 约 5 次模型调用，在 25 条样本上平均 12.8K token/诊断。  自进化与经验复用 轨迹调试与因果归因 Agent 评测与可靠性：如何知道真的做对了 为什么修复建议不能自动从导入日志重放任意外部工具？ 日志是观察资料，可能过时、缺权限或包含有副作用的调用；检测归因与授权执行应分开。不可变原轨迹上叠加假设和建议，真实重跑经人或 policy gate 后形成独立证据；诊断器若有参考答案等特权输入，也必须与无答案在线能力明确区分。 例如日志里有删除临时目录命令，调试器不能仅因导入了它就重新执行；应先建议修复，再由有权限的运行流程决定。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-762711639f7eb829">为什么修复建议不能自动从导入日志重放任意外部工具？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentdebugx">AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>日志是观察资料，可能过时、缺权限或包含有副作用的调用；检测归因与授权执行应分开。不可变原轨迹上叠加假设和建议，真实重跑经人或 policy gate 后形成独立证据；诊断器若有参考答案等特权输入，也必须与无答案在线能力明确区分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如日志里有删除临时目录命令，调试器不能仅因导入了它就重新执行；应先建议修复，再由有权限的运行流程决定。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与评测边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18754v1">原论文</a> · <a href="../../../../agent-research/2607.18754-agentdebugx/">实现解读</a> · <a href="#qa-762711639f7eb829">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentdebugx" data-paper-title="AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents Agent University of Illinois Urbana-Champaign 2026-07-21 AgentDebugX 在不可变原始轨迹外叠加 Detect、Attribute、Recover、Rerun 产物。DeepDebug 先全局读，再按单/多 Agent 结构独立定位；候选不一致时交叉质询，最终给出责任步骤、证据和具体建议。修复只生成建议，实际重跑仍经过人或 policy gate；不会从导入日志擅自重放任意外部工具。 完整实验成本过高，不复现（审查 DONE），不会自动重试或进入实现队列。完整配方需要 9B/27B 模型、多轮 Gemini 诊断/搜索、GAIA 工具重跑及多种修复对照；仅研究资料，没有可执行本地 adapter、模型指标或 Evolve 集成。完整实验成本过高，不复现（审查 DONE），不会自动重试或进入实现队列。本地仅核对正文 §3/4 和 Appendix C、固定作者仓库及原图。完整配方需要 9B/27B 模型、多轮 Gemini 诊断/搜索、GAIA 工具重跑及多种修复对照；DeepDebug 约 5 次模型调用，在 25 条样本上平均 12.8K token/诊断。  自进化与经验复用 轨迹调试与因果归因 Agent 评测与可靠性：如何知道真的做对了 Who&amp;When提供reference answer意味着怎样的比较边界？ 该诊断条件允许任务答案但不提供责任Agent或步骤，是with-ground-truth定位协议。不能省略答案特权后宣称它是无答案在线智能体能力对比。 例如知道目标结果有助发现偏离，但仍不等于知道谁最先犯错。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-ceae50a35c7df48b">Who&amp;When提供reference answer意味着怎样的比较边界？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentdebugx">AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>该诊断条件允许任务答案但不提供责任Agent或步骤，是with-ground-truth定位协议。不能省略答案特权后宣称它是无答案在线智能体能力对比。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如知道目标结果有助发现偏离，但仍不等于知道谁最先犯错。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与评测边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18754v1">原论文</a> · <a href="../../../../agent-research/2607.18754-agentdebugx/">实现解读</a> · <a href="#qa-ceae50a35c7df48b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:agentdebugx" data-paper-title="AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents Agent University of Illinois Urbana-Champaign 2026-07-21 AgentDebugX 在不可变原始轨迹外叠加 Detect、Attribute、Recover、Rerun 产物。DeepDebug 先全局读，再按单/多 Agent 结构独立定位；候选不一致时交叉质询，最终给出责任步骤、证据和具体建议。修复只生成建议，实际重跑仍经过人或 policy gate；不会从导入日志擅自重放任意外部工具。 完整实验成本过高，不复现（审查 DONE），不会自动重试或进入实现队列。完整配方需要 9B/27B 模型、多轮 Gemini 诊断/搜索、GAIA 工具重跑及多种修复对照；仅研究资料，没有可执行本地 adapter、模型指标或 Evolve 集成。完整实验成本过高，不复现（审查 DONE），不会自动重试或进入实现队列。本地仅核对正文 §3/4 和 Appendix C、固定作者仓库及原图。完整配方需要 9B/27B 模型、多轮 Gemini 诊断/搜索、GAIA 工具重跑及多种修复对照；DeepDebug 约 5 次模型调用，在 25 条样本上平均 12.8K token/诊断。  自进化与经验复用 轨迹调试与因果归因 Agent 评测与可靠性：如何知道真的做对了 AgentDebugX生成修复建议后能自动重放日志工具吗？ 不能，实际重跑经过人或policy gate，不能从导入日志擅自执行任意外部命令。闭环结果需修后独立轨迹真实评分；memory或Error Hub收益未被原文评估。 例如日志含删除命令，诊断器可以建议修正，不应直接再次运行。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-68e7cd5de654ac2b">AgentDebugX生成修复建议后能自动重放日志工具吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aagentdebugx">AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，实际重跑经过人或policy gate，不能从导入日志擅自执行任意外部命令。闭环结果需修后独立轨迹真实评分；memory或Error Hub收益未被原文评估。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如日志含删除命令，诊断器可以建议修正，不应直接再次运行。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心机制与评测边界；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2607.18754v1">原论文</a> · <a href="../../../../agent-research/2607.18754-agentdebugx/">实现解读</a> · <a href="#qa-68e7cd5de654ac2b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:logact" data-paper-title="LogAct: Enabling Agentic Reliability via Shared Logs" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="LogAct: Enabling Agentic Reliability via Shared Logs Agent Meta 2026-04-09 LogAct 将 Agent 拆成 Driver、Voter、Decider 和 Executor，用持久共享日志记录意图、独立投票、commit/abort和执行结果，只有达到批准条件的已提交动作才能执行。它将安全审查与动作执行解耦，并保留崩溃后的不确定状态；外部副作用恢复仍需要明确的幂等或事务契约，不能只凭对话记录盲目重放。 模型具体身份、内部系统和完整复现费用无法用本轮单 A100/A30 或 Mac 的短时预算确定，依成本门槛标为成本过高，不复现（审查 DONE），不探测付费接口、不展开多机或长轨迹实验。DurableLogAct 用单机 SQLite 的 WAL、synchronous=FULL 和事务，将意图/投票/决策/执行状态与追加日志共同落盘。策略和 bus identity 在创建时固定，重开数据库不能悄悄降低 quorum；同一个 intent ID 也不能绑定另一动作。每个逻辑 Agent 至多一个未完成意图，失败未决会阻止后续意图越过它。  工具调用与环境执行 动作投票、持久提交与故障恢复 Agent 评测与可靠性：如何知道真的做对了 LogAct为什么把投票提交与执行分开？ 意图、审查与commit持久记录后才允许执行，让授权判断与外部副作用解耦，并可审计崩溃状态。对话里说同意不等于已有可信持久commit。 例如先写入批准结果，再让执行器调用支付接口。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-logact-bec0d56e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-db41d8cd460b9232">LogAct为什么把投票提交与执行分开？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alogact">LogAct: Enabling Agentic Reliability via Shared Logs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>意图、审查与commit持久记录后才允许执行，让授权判断与外部副作用解耦，并可审计崩溃状态。对话里说同意不等于已有可信持久commit。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如先写入批准结果，再让执行器调用支付接口。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07988v1">原论文</a> · <a href="../../../../agent-research/2604.07988-logact/">实现解读</a> · <a href="#qa-db41d8cd460b9232">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:logact" data-paper-title="LogAct: Enabling Agentic Reliability via Shared Logs" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="LogAct: Enabling Agentic Reliability via Shared Logs Agent Meta 2026-04-09 LogAct 将 Agent 拆成 Driver、Voter、Decider 和 Executor，用持久共享日志记录意图、独立投票、commit/abort和执行结果，只有达到批准条件的已提交动作才能执行。它将安全审查与动作执行解耦，并保留崩溃后的不确定状态；外部副作用恢复仍需要明确的幂等或事务契约，不能只凭对话记录盲目重放。 模型具体身份、内部系统和完整复现费用无法用本轮单 A100/A30 或 Mac 的短时预算确定，依成本门槛标为成本过高，不复现（审查 DONE），不探测付费接口、不展开多机或长轨迹实验。DurableLogAct 用单机 SQLite 的 WAL、synchronous=FULL 和事务，将意图/投票/决策/执行状态与追加日志共同落盘。策略和 bus identity 在创建时固定，重开数据库不能悄悄降低 quorum；同一个 intent ID 也不能绑定另一动作。每个逻辑 Agent 至多一个未完成意图，失败未决会阻止后续意图越过它。  工具调用与环境执行 动作投票、持久提交与故障恢复 Agent 评测与可靠性：如何知道真的做对了 动作已在共享日志 commit，崩溃后为什么仍不能无条件再次执行？ 日志提交说明批准意图，不一定能确定外部副作用是否已经发生；崩溃可能出现在调用成功但回执未写入之间。恢复需幂等键或事务契约区分未执行与已执行，独立投票也只控制批准过程，不能凭对话记录保证外部 exactly-once。 例如付款调用成功后进程崩溃，日志没有结果；直接重放可能重复扣款，应依赖幂等或事务查询，而非只看 commit 状态。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-219db6899dfab0c3">动作已在共享日志 commit，崩溃后为什么仍不能无条件再次执行？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alogact">LogAct: Enabling Agentic Reliability via Shared Logs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>日志提交说明批准意图，不一定能确定外部副作用是否已经发生；崩溃可能出现在调用成功但回执未写入之间。恢复需幂等键或事务契约区分未执行与已执行，独立投票也只控制批准过程，不能凭对话记录保证外部 exactly-once。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如付款调用成功后进程崩溃，日志没有结果；直接重放可能重复扣款，应依赖幂等或事务查询，而非只看 commit 状态。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07988v1">原论文</a> · <a href="../../../../agent-research/2604.07988-logact/">实现解读</a> · <a href="#qa-219db6899dfab0c3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:logact" data-paper-title="LogAct: Enabling Agentic Reliability via Shared Logs" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="LogAct: Enabling Agentic Reliability via Shared Logs Agent Meta 2026-04-09 LogAct 将 Agent 拆成 Driver、Voter、Decider 和 Executor，用持久共享日志记录意图、独立投票、commit/abort和执行结果，只有达到批准条件的已提交动作才能执行。它将安全审查与动作执行解耦，并保留崩溃后的不确定状态；外部副作用恢复仍需要明确的幂等或事务契约，不能只凭对话记录盲目重放。 模型具体身份、内部系统和完整复现费用无法用本轮单 A100/A30 或 Mac 的短时预算确定，依成本门槛标为成本过高，不复现（审查 DONE），不探测付费接口、不展开多机或长轨迹实验。DurableLogAct 用单机 SQLite 的 WAL、synchronous=FULL 和事务，将意图/投票/决策/执行状态与追加日志共同落盘。策略和 bus identity 在创建时固定，重开数据库不能悄悄降低 quorum；同一个 intent ID 也不能绑定另一动作。每个逻辑 Agent 至多一个未完成意图，失败未决会阻止后续意图越过它。  工具调用与环境执行 动作投票、持久提交与故障恢复 Agent 评测与可靠性：如何知道真的做对了 LogAct的k-of-N批准，与必须等所有投票返回后才能决定有什么区别？ 本地固定批准条件允许达到k票即提交；若已批准数加未投票数仍不足k，则可提前拒绝。它不必等待无力改变结果的剩余票，且同一Voter不能重复计票。这是固定阈值下的决策性质，不代表已实现所有动态审批策略。 教学例子：三位Voter要求两票，前两票都批准即可提交；前两票都拒绝时，最后一票也无法凑足两票。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-c65844ffb886b1c4">LogAct的k-of-N批准，与必须等所有投票返回后才能决定有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alogact">LogAct: Enabling Agentic Reliability via Shared Logs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>本地固定批准条件允许达到k票即提交；若已批准数加未投票数仍不足k，则可提前拒绝。它不必等待无力改变结果的剩余票，且同一Voter不能重复计票。这是固定阈值下的决策性质，不代表已实现所有动态审批策略。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>三位Voter要求两票，前两票都批准即可提交；前两票都拒绝时，最后一票也无法凑足两票。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07988v1">原论文</a> · <a href="../../../../agent-research/2604.07988-logact/">实现解读</a> · <a href="#qa-c65844ffb886b1c4">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:logact" data-paper-title="LogAct: Enabling Agentic Reliability via Shared Logs" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="LogAct: Enabling Agentic Reliability via Shared Logs Agent Meta 2026-04-09 LogAct 将 Agent 拆成 Driver、Voter、Decider 和 Executor，用持久共享日志记录意图、独立投票、commit/abort和执行结果，只有达到批准条件的已提交动作才能执行。它将安全审查与动作执行解耦，并保留崩溃后的不确定状态；外部副作用恢复仍需要明确的幂等或事务契约，不能只凭对话记录盲目重放。 模型具体身份、内部系统和完整复现费用无法用本轮单 A100/A30 或 Mac 的短时预算确定，依成本门槛标为成本过高，不复现（审查 DONE），不探测付费接口、不展开多机或长轨迹实验。DurableLogAct 用单机 SQLite 的 WAL、synchronous=FULL 和事务，将意图/投票/决策/执行状态与追加日志共同落盘。策略和 bus identity 在创建时固定，重开数据库不能悄悄降低 quorum；同一个 intent ID 也不能绑定另一动作。每个逻辑 Agent 至多一个未完成意图，失败未决会阻止后续意图越过它。  工具调用与环境执行 动作投票、持久提交与故障恢复 Agent 评测与可靠性：如何知道真的做对了 本地LogAct的quorum和崩溃恢复怎样处理？ 固定N命名voter至少k同意，同voter去重且不可改票；started无Result默认不重试。仅明确幂等并显式recover、排除仍活跃执行器后才用稳定key恢复，不支持任意动态策略语言。 例如两次同人投票不能当两票，已提交也不意味着未知副作用可随意再做。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b73e475fbcd5cecd">本地LogAct的quorum和崩溃恢复怎样处理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alogact">LogAct: Enabling Agentic Reliability via Shared Logs</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>固定N命名voter至少k同意，同voter去重且不可改票；started无Result默认不重试。仅明确幂等并显式recover、排除仍活跃执行器后才用稳定key恢复，不支持任意动态策略语言。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如两次同人投票不能当两票，已提交也不意味着未知副作用可随意再做。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.07988v1">原论文</a> · <a href="../../../../agent-research/2604.07988-logact/">实现解读</a> · <a href="#qa-b73e475fbcd5cecd">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tfrbench" data-paper-title="TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems Agent Google Cloud AI Research / University of Kentucky 2026-04-07 预测值接近真值不保证推理有根据，流畅推理也可能导致错误预测。论文联合 Search、Reason、Forecast、Verify、Summary 构建数值与推理同时合格的参考轨迹。标签参与参考筛选与反馈，因此这个构建过程不能直接作为留出能力成绩。原文 Algorithm 1 完整实验成本过高，不复现（审查 DONE）。CPU 评分与参考构建协议，当前仅 L0 固定回调验证。有标签参考构建不是无泄露预测评测。完整实验成本过高，不复现（审查 DONE）。ForecastView 只含 history、reasoning、horizon、description，不包含未来 target。未来值由 OutcomeEvaluator 持有。Python 回调是受信任代码，不是安全沙箱，不能阻止外部 callback 自行读取文件或闭包中的目标值；接真实模型时还要审计提供方信息流。  Agent 评测 时间序列预测推理 Agent 评测与可靠性：如何知道真的做对了 TFRBench为什么同时验数值误差与推理一致性？ 预测接近可能靠偶然，解释流畅也可能预测错，参考轨迹需两条都合格。构建时用标签筛选与反馈，因此参考制作过程不能直接算留出能力成绩。 例如碰巧猜中趋势却无证据，与有根据但数值偏差大，均不完整合格。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-tfrbench-2bbb3dcd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-98893c798861ce4a">TFRBench为什么同时验数值误差与推理一致性？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atfrbench">TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / University of Kentucky</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>预测接近可能靠偶然，解释流畅也可能预测错，参考轨迹需两条都合格。构建时用标签筛选与反馈，因此参考制作过程不能直接算留出能力成绩。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如碰巧猜中趋势却无证据，与有根据但数值偏差大，均不完整合格。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05364">原论文</a> · <a href="../../../../agent-research/2604.05364-tfrbench/">实现解读</a> · <a href="#qa-98893c798861ce4a">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tfrbench" data-paper-title="TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems Agent Google Cloud AI Research / University of Kentucky 2026-04-07 预测值接近真值不保证推理有根据，流畅推理也可能导致错误预测。论文联合 Search、Reason、Forecast、Verify、Summary 构建数值与推理同时合格的参考轨迹。标签参与参考筛选与反馈，因此这个构建过程不能直接作为留出能力成绩。原文 Algorithm 1 完整实验成本过高，不复现（审查 DONE）。CPU 评分与参考构建协议，当前仅 L0 固定回调验证。有标签参考构建不是无泄露预测评测。完整实验成本过高，不复现（审查 DONE）。ForecastView 只含 history、reasoning、horizon、description，不包含未来 target。未来值由 OutcomeEvaluator 持有。Python 回调是受信任代码，不是安全沙箱，不能阻止外部 callback 自行读取文件或闭包中的目标值；接真实模型时还要审计提供方信息流。  Agent 评测 时间序列预测推理 Agent 评测与可靠性：如何知道真的做对了 长推理轨迹达到参考门槛，为什么摘要还要单独预测并再次过门？ 摘要可能省掉决定预测的关键证据或条件，不能继承原轨迹的正确性。数值误差与推理一致性共同约束参考，且标签参与筛选只说明构建质量，不是留出能力成绩；历史尺度为零时指标未定义，应拒绝而非加任意 epsilon 制造良好结果。 例如长轨迹解释季节变化并预测正确，摘要只剩“趋势向上”后重新预测可能失准，需要独立验证压缩是否保留了依据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9748b5565a2ace11">长推理轨迹达到参考门槛，为什么摘要还要单独预测并再次过门？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atfrbench">TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / University of Kentucky</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>摘要可能省掉决定预测的关键证据或条件，不能继承原轨迹的正确性。数值误差与推理一致性共同约束参考，且标签参与筛选只说明构建质量，不是留出能力成绩；历史尺度为零时指标未定义，应拒绝而非加任意 epsilon 制造良好结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如长轨迹解释季节变化并预测正确，摘要只剩“趋势向上”后重新预测可能失准，需要独立验证压缩是否保留了依据。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05364">原论文</a> · <a href="../../../../agent-research/2604.05364-tfrbench/">实现解读</a> · <a href="#qa-9748b5565a2ace11">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tfrbench" data-paper-title="TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems Agent Google Cloud AI Research / University of Kentucky 2026-04-07 预测值接近真值不保证推理有根据，流畅推理也可能导致错误预测。论文联合 Search、Reason、Forecast、Verify、Summary 构建数值与推理同时合格的参考轨迹。标签参与参考筛选与反馈，因此这个构建过程不能直接作为留出能力成绩。原文 Algorithm 1 完整实验成本过高，不复现（审查 DONE）。CPU 评分与参考构建协议，当前仅 L0 固定回调验证。有标签参考构建不是无泄露预测评测。完整实验成本过高，不复现（审查 DONE）。ForecastView 只含 history、reasoning、horizon、description，不包含未来 target。未来值由 OutcomeEvaluator 持有。Python 回调是受信任代码，不是安全沙箱，不能阻止外部 callback 自行读取文件或闭包中的目标值；接真实模型时还要审计提供方信息流。  Agent 评测 时间序列预测推理 Agent 评测与可靠性：如何知道真的做对了 TFRBench的MASE与直接比较不同序列的MAE，尺度解释有什么区别？ MASE用历史季节差分的平均绝对变化归一化预测误差，使门槛相对于该序列的历史尺度定义。原始MAE仍带各序列单位，不能直接跨量纲比较。MASE小于一是数值准入条件，还需独立的一致性门槛；历史尺度为零时公式未定义。 教学例子：同样差10，在高波动销量和近乎恒定温度里含义不同；先按各自历史季节变化归一，才有规定尺度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-da5746f15012a652">TFRBench的MASE与直接比较不同序列的MAE，尺度解释有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atfrbench">TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / University of Kentucky</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>MASE用历史季节差分的平均绝对变化归一化预测误差，使门槛相对于该序列的历史尺度定义。原始MAE仍带各序列单位，不能直接跨量纲比较。MASE小于一是数值准入条件，还需独立的一致性门槛；历史尺度为零时公式未定义。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>同样差10，在高波动销量和近乎恒定温度里含义不同；先按各自历史季节变化归一，才有规定尺度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05364">原论文</a> · <a href="../../../../agent-research/2604.05364-tfrbench/">实现解读</a> · <a href="#qa-da5746f15012a652">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:tfrbench" data-paper-title="TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems Agent Google Cloud AI Research / University of Kentucky 2026-04-07 预测值接近真值不保证推理有根据，流畅推理也可能导致错误预测。论文联合 Search、Reason、Forecast、Verify、Summary 构建数值与推理同时合格的参考轨迹。标签参与参考筛选与反馈，因此这个构建过程不能直接作为留出能力成绩。原文 Algorithm 1 完整实验成本过高，不复现（审查 DONE）。CPU 评分与参考构建协议，当前仅 L0 固定回调验证。有标签参考构建不是无泄露预测评测。完整实验成本过高，不复现（审查 DONE）。ForecastView 只含 history、reasoning、horizon、description，不包含未来 target。未来值由 OutcomeEvaluator 持有。Python 回调是受信任代码，不是安全沙箱，不能阻止外部 callback 自行读取文件或闭包中的目标值；接真实模型时还要审计提供方信息流。  Agent 评测 时间序列预测推理 Agent 评测与可靠性：如何知道真的做对了 TFRBench历史季节尺度为零时能加epsilon给高分吗？ 不能，MASE未定义应拒绝该样本；参考准入严格MASE小于一且S至少四。复合排序权重需显式，本地策略不是作者唯一指定公式，未来真值只给评分器。 例如常量历史无差分尺度，不能人为造一个分母再声称正常误差可比。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-52b59b4d02f11ef2">TFRBench历史季节尺度为零时能加epsilon给高分吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Atfrbench">TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research / University of Kentucky</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，MASE未定义应拒绝该样本；参考准入严格MASE小于一且S至少四。复合排序权重需显式，本地策略不是作者唯一指定公式，未来真值只给评分器。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如常量历史无差分尺度，不能人为造一个分母再声称正常误差可比。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2604.05364">原论文</a> · <a href="../../../../agent-research/2604.05364-tfrbench/">实现解读</a> · <a href="#qa-52b59b4d02f11ef2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:convapparel" data-paper-title="ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders Agent Google 2026-02-18 模拟用户能完成购物目标，不等于像真人。论文将验证拆成三条互补证据：PLSA 比较行为分布；HLS 检查训练过的真假对话判别器能否识别模拟；反事实验证把仅在一种推荐策略下训练的模拟器放到另一策略下。PLSA 的全称是 Population-Level Statistical Alignment，不是同名主题模型。原文 §4 完整实验成本过高，不复现（审查 DONE）。本地为 CPU evaluation_protocol_interface，不是完整模拟器复现。公开固定刺激只检验 L0 接口；完整实验成本过高，不复现（审查 DONE）。也可传 --input conversations.json 代替 --fixture-demo：JSON 顶层为 train 与 heldout 数组，每行有 session_id、participant_id、policy、user_turns、布尔 is_human、可选 annotations。  Agent 评测 用户模拟器与分布对齐 Agent 评测与可靠性：如何知道真的做对了 ConvApparel的PLSA是在训练同名主题模型吗？ 不是。此处PLSA全称为Population-Level Statistical Alignment，检查模拟人群与真人的行为分布是否接近；本地统计核使用KS距离与带并列处理的MWU。它比较群体分布，不会逐条证明每段模拟对话都是真实的人类行为。 教学例子：比较真人与模拟者的对话轮数分布，是群体行为对齐检查，并非从购物文本学习若干隐含主题。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-convapparel-e8aab87b" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-bed15d23c527866b">ConvApparel的PLSA是在训练同名主题模型吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aconvapparel">ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是。此处PLSA全称为Population-Level Statistical Alignment，检查模拟人群与真人的行为分布是否接近；本地统计核使用KS距离与带并列处理的MWU。它比较群体分布，不会逐条证明每段模拟对话都是真实的人类行为。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>比较真人与模拟者的对话轮数分布，是群体行为对齐检查，并非从购物文本学习若干隐含主题。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16938">原论文</a> · <a href="../../../../agent-research/2602.16938-convapparel/">实现解读</a> · <a href="#qa-bed15d23c527866b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:convapparel" data-paper-title="ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders Agent Google 2026-02-18 模拟用户能完成购物目标，不等于像真人。论文将验证拆成三条互补证据：PLSA 比较行为分布；HLS 检查训练过的真假对话判别器能否识别模拟；反事实验证把仅在一种推荐策略下训练的模拟器放到另一策略下。PLSA 的全称是 Population-Level Statistical Alignment，不是同名主题模型。原文 §4 完整实验成本过高，不复现（审查 DONE）。本地为 CPU evaluation_protocol_interface，不是完整模拟器复现。公开固定刺激只检验 L0 接口；完整实验成本过高，不复现（审查 DONE）。也可传 --input conversations.json 代替 --fixture-demo：JSON 顶层为 train 与 heldout 数组，每行有 session_id、participant_id、policy、user_turns、布尔 is_human、可选 annotations。  Agent 评测 用户模拟器与分布对齐 Agent 评测与可靠性：如何知道真的做对了 为什么模拟购物目标成功，并不能证明用户模拟器像真人？ 任务成功只反映与当前推荐策略配合完成目标，模拟器可能语气、行为分布或响应规律都不真实。群体统计、训练过的真假判别与跨策略反事实分别检查不同维度，互相不能替代；HLS 是判别器真人概率，不是购物成功率或人类真实认可。 例如模拟用户每次立刻接受第一款商品，目标完成很快，却不像真人反复比较；换另一推荐策略时还可能完全失效。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-cd3497205b271356">为什么模拟购物目标成功，并不能证明用户模拟器像真人？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aconvapparel">ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务成功只反映与当前推荐策略配合完成目标，模拟器可能语气、行为分布或响应规律都不真实。群体统计、训练过的真假判别与跨策略反事实分别检查不同维度，互相不能替代；HLS 是判别器真人概率，不是购物成功率或人类真实认可。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如模拟用户每次立刻接受第一款商品，目标完成很快，却不像真人反复比较；换另一推荐策略时还可能完全失效。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16938">原论文</a> · <a href="../../../../agent-research/2602.16938-convapparel/">实现解读</a> · <a href="#qa-cd3497205b271356">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:convapparel" data-paper-title="ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders Agent Google 2026-02-18 模拟用户能完成购物目标，不等于像真人。论文将验证拆成三条互补证据：PLSA 比较行为分布；HLS 检查训练过的真假对话判别器能否识别模拟；反事实验证把仅在一种推荐策略下训练的模拟器放到另一策略下。PLSA 的全称是 Population-Level Statistical Alignment，不是同名主题模型。原文 §4 完整实验成本过高，不复现（审查 DONE）。本地为 CPU evaluation_protocol_interface，不是完整模拟器复现。公开固定刺激只检验 L0 接口；完整实验成本过高，不复现（审查 DONE）。也可传 --input conversations.json 代替 --fixture-demo：JSON 顶层为 train 与 heldout 数组，每行有 session_id、participant_id、policy、user_turns、布尔 is_human、可选 annotations。  Agent 评测 用户模拟器与分布对齐 Agent 评测与可靠性：如何知道真的做对了 ConvApparel跨推荐策略验证，与在生成模拟数据的同一策略下验证有什么区别？ 同策略验证可能只说明模拟器适应了熟悉的交互环境；跨策略把在一种策略下训练的模拟器放到另一策略，观察行为规律能否迁移。它补充分布相似和真假判别证据，但仍不是对所有真实部署策略的泛化保证。 教学例子：只在偏热门的推荐器下训练模拟器，再放到偏探索的推荐器中，检查它是否仍呈现合理购物反应。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-bf4fa51f825f70b0">ConvApparel跨推荐策略验证，与在生成模拟数据的同一策略下验证有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aconvapparel">ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>同策略验证可能只说明模拟器适应了熟悉的交互环境；跨策略把在一种策略下训练的模拟器放到另一策略，观察行为规律能否迁移。它补充分布相似和真假判别证据，但仍不是对所有真实部署策略的泛化保证。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>只在偏热门的推荐器下训练模拟器，再放到偏探索的推荐器中，检查它是否仍呈现合理购物反应。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16938">原论文</a> · <a href="../../../../agent-research/2602.16938-convapparel/">实现解读</a> · <a href="#qa-bf4fa51f825f70b0">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:convapparel" data-paper-title="ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders Agent Google 2026-02-18 模拟用户能完成购物目标，不等于像真人。论文将验证拆成三条互补证据：PLSA 比较行为分布；HLS 检查训练过的真假对话判别器能否识别模拟；反事实验证把仅在一种推荐策略下训练的模拟器放到另一策略下。PLSA 的全称是 Population-Level Statistical Alignment，不是同名主题模型。原文 §4 完整实验成本过高，不复现（审查 DONE）。本地为 CPU evaluation_protocol_interface，不是完整模拟器复现。公开固定刺激只检验 L0 接口；完整实验成本过高，不复现（审查 DONE）。也可传 --input conversations.json 代替 --fixture-demo：JSON 顶层为 train 与 heldout 数组，每行有 session_id、participant_id、policy、user_turns、布尔 is_human、可选 annotations。  Agent 评测 用户模拟器与分布对齐 Agent 评测与可靠性：如何知道真的做对了 PLSA在这里是主题模型吗，本地统计如何留痕？ 不是，是Population-Level Statistical Alignment。本地小样本精确置换，大样本定种子加一修正Monte Carlo，是明示选择；HLS判别器应独立训练验证，不能用金标回填预测。 例如KS距离计算通过，只证明统计核，不证明模拟器已和真人一致。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-18442e94ba96dd81">PLSA在这里是主题模型吗，本地统计如何留痕？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aconvapparel">ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不是，是Population-Level Statistical Alignment。本地小样本精确置换，大样本定种子加一修正Monte Carlo，是明示选择；HLS判别器应独立训练验证，不能用金标回填预测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如KS距离计算通过，只证明统计核，不证明模拟器已和真人一致。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.16938">原论文</a> · <a href="../../../../agent-research/2602.16938-convapparel/">实现解读</a> · <a href="#qa-18442e94ba96dd81">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:causal-armor" data-paper-title="CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution Agent Google Cloud AI Research 2026-02-08 在高权限动作前，分别去掉用户请求与不可信工具段，比较同一个动作的似然变化。工具段的归因高于用户时，只清洗命中段，再遮蔽首个命中点后的 assistant 内容并重新提案。§3–4、Algorithm 1 完整实验：成本过高，不复现（审查 DONE）。CPU 诊断记录 component_only / L1。真实似然算子与安全失败的干预接口，不是已验证的注入检测器。完整实验：成本过高，不复现（审查 DONE）。7 项 CPU 契约测试通过：LOO 分离、动作长度归一化、margin 严格边界、选择性清洗、历史遮蔽、缺回调扣留和非高权限跳过。固定 fixture 仅验证公式，不计算安全准确率。CPU 诊断记录  Agent 安全 提示注入防御 因果归因 Agent 评测与可靠性：如何知道真的做对了 CausalArmor为什么在高权限动作前比较用户与工具归因？ 不可信工具内容可能支配提案，留一消融测同一动作似然变化，工具归因超过用户时选择性清洗并重新提案。它是干预前诊断，不直接执行原动作。 例如网页文字诱导删除文件，原用户并没要求该操作。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-causal-armor-73cc1cba" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-94b3dc3d98d854cc">CausalArmor为什么在高权限动作前比较用户与工具归因？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acausal-armor">CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不可信工具内容可能支配提案，留一消融测同一动作似然变化，工具归因超过用户时选择性清洗并重新提案。它是干预前诊断，不直接执行原动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如网页文字诱导删除文件，原用户并没要求该操作。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07918">原论文</a> · <a href="../../../../agent-research/2602.07918-causal-armor/">实现解读</a> · <a href="#qa-94b3dc3d98d854cc">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:causal-armor" data-paper-title="CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution Agent Google Cloud AI Research 2026-02-08 在高权限动作前，分别去掉用户请求与不可信工具段，比较同一个动作的似然变化。工具段的归因高于用户时，只清洗命中段，再遮蔽首个命中点后的 assistant 内容并重新提案。§3–4、Algorithm 1 完整实验：成本过高，不复现（审查 DONE）。CPU 诊断记录 component_only / L1。真实似然算子与安全失败的干预接口，不是已验证的注入检测器。完整实验：成本过高，不复现（审查 DONE）。7 项 CPU 契约测试通过：LOO 分离、动作长度归一化、margin 严格边界、选择性清洗、历史遮蔽、缺回调扣留和非高权限跳过。固定 fixture 仅验证公式，不计算安全准确率。CPU 诊断记录  Agent 安全 提示注入防御 因果归因 Agent 评测与可靠性：如何知道真的做对了 去掉不可信工具段后动作似然下降，为什么还不能直接称作因果安全证明？ 留一消融是操作性归因，表明该段影响同一动作概率，但删除也可能改变上下文结构或移走合法证据。方法与用户请求归因比较，只清洗命中段，再遮蔽受污染后续并重新提案；阈值方向与重算流程需保持原义，单个低用户归因不是攻击结论。 例如网页某段既含必要数值也含可疑指令，删段使动作概率下降不全是恶意影响；还需比较来源与具体动作的关系。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-58882c2ee223a900">去掉不可信工具段后动作似然下降，为什么还不能直接称作因果安全证明？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acausal-armor">CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>留一消融是操作性归因，表明该段影响同一动作概率，但删除也可能改变上下文结构或移走合法证据。方法与用户请求归因比较，只清洗命中段，再遮蔽受污染后续并重新提案；阈值方向与重算流程需保持原义，单个低用户归因不是攻击结论。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如网页某段既含必要数值也含可疑指令，删段使动作概率下降不全是恶意影响；还需比较来源与具体动作的关系。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07918">原论文</a> · <a href="../../../../agent-research/2602.07918-causal-armor/">实现解读</a> · <a href="#qa-58882c2ee223a900">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:causal-armor" data-paper-title="CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution Agent Google Cloud AI Research 2026-02-08 在高权限动作前，分别去掉用户请求与不可信工具段，比较同一个动作的似然变化。工具段的归因高于用户时，只清洗命中段，再遮蔽首个命中点后的 assistant 内容并重新提案。§3–4、Algorithm 1 完整实验：成本过高，不复现（审查 DONE）。CPU 诊断记录 component_only / L1。真实似然算子与安全失败的干预接口，不是已验证的注入检测器。完整实验：成本过高，不复现（审查 DONE）。7 项 CPU 契约测试通过：LOO 分离、动作长度归一化、margin 严格边界、选择性清洗、历史遮蔽、缺回调扣留和非高权限跳过。固定 fixture 仅验证公式，不计算安全准确率。CPU 诊断记录  Agent 安全 提示注入防御 因果归因 Agent 评测与可靠性：如何知道真的做对了 CausalArmor定点清洗命中工具段，与把全部工具结果删空有何不同？ 定点方案保留未命中的信息，只清洗被标记段，并遮蔽首个命中点之后可能已受影响的assistant内容再提案。全删会连合法证据一起丢失，改变可用上下文。清洗后仍需重新评估提案，不能认为删过文本就自动得到安全动作。 教学例子：检索结果一段夹带指令时，清洗该段并撤去之后受其影响的草稿；其余正常检索证据可继续保留。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-4f8a4f14c30948ed">CausalArmor定点清洗命中工具段，与把全部工具结果删空有何不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acausal-armor">CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>定点方案保留未命中的信息，只清洗被标记段，并遮蔽首个命中点之后可能已受影响的assistant内容再提案。全删会连合法证据一起丢失，改变可用上下文。清洗后仍需重新评估提案，不能认为删过文本就自动得到安全动作。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>检索结果一段夹带指令时，清洗该段并撤去之后受其影响的草稿；其余正常检索证据可继续保留。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07918">原论文</a> · <a href="../../../../agent-research/2602.07918-causal-armor/">实现解读</a> · <a href="#qa-4f8a4f14c30948ed">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:causal-armor" data-paper-title="CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution Agent Google Cloud AI Research 2026-02-08 在高权限动作前，分别去掉用户请求与不可信工具段，比较同一个动作的似然变化。工具段的归因高于用户时，只清洗命中段，再遮蔽首个命中点后的 assistant 内容并重新提案。§3–4、Algorithm 1 完整实验：成本过高，不复现（审查 DONE）。CPU 诊断记录 component_only / L1。真实似然算子与安全失败的干预接口，不是已验证的注入检测器。完整实验：成本过高，不复现（审查 DONE）。7 项 CPU 契约测试通过：LOO 分离、动作长度归一化、margin 严格边界、选择性清洗、历史遮蔽、缺回调扣留和非高权限跳过。固定 fixture 仅验证公式，不计算安全准确率。CPU 诊断记录  Agent 安全 提示注入防御 因果归因 Agent 评测与可靠性：如何知道真的做对了 CausalArmor缺少sanitizer或重新提案回调时怎么办？ 扣留动作并标intervention_required，不伪造清洗或重跑；命中后遮蔽首点之后assistant内容。τ增大标更多段，负号不可写反，最终动作仍须正常授权执行。 例如没有真实清洗器时不能删个字符串就宣称防护闭环成功。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-581064307ea1ff67">CausalArmor缺少sanitizer或重新提案回调时怎么办？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acausal-armor">CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Google Cloud AI Research</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>扣留动作并标intervention_required，不伪造清洗或重跑；命中后遮蔽首点之后assistant内容。τ增大标更多段，负号不可写反，最终动作仍须正常授权执行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如没有真实清洗器时不能删个字符串就宣称防护闭环成功。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.07918">原论文</a> · <a href="../../../../agent-research/2602.07918-causal-armor/">实现解读</a> · <a href="#qa-581064307ea1ff67">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:airs-bench" data-paper-title="AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents Agent FAIR at Meta / University of Oxford 2026-02-06 以问题、数据集、指标和人工SOTA定义20个任务。Agent自行提出方法、实现训练、分析实验并修订，不提供基线解法；协议区分Agent、搜索scaffold与运行harness，比较顺序MLGym和树搜索AIRA-dojo。原文§3–5 成本过高，不复现（审查 DONE）；Google/Meta优先补漏资料。成本过高，不复现（审查 DONE）；任务规范收录不等于已接入benchmark。原文每次运行24小时、独占1张H200，20个任务；附录D还列每任务10至20次运行。单A100/A30或Mac下，成本过高，不复现（审查 DONE）。原文附录C–D  自动研究 研究Agent评测协议 Agent 评测与可靠性：如何知道真的做对了 AIRS-Bench要求研究Agent交付一段方法建议就够了吗？ 不够。任务要求从问题、数据集与指标出发，提出方法、实现训练、分析实验并修订，考查端到端研究过程。Agent、搜索scaffold与执行harness是不同层，不能把一段听起来合理的研究计划当成已完成实验或任务结果。 教学例子：提出“换一种损失”只是起点；还需实际实现、运行并根据允许的实验反馈决定是否修订。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-airs-bench-3e226cbd" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-7d73d79eb709b84b">AIRS-Bench要求研究Agent交付一段方法建议就够了吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aairs-bench">AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不够。任务要求从问题、数据集与指标出发，提出方法、实现训练、分析实验并修订，考查端到端研究过程。Agent、搜索scaffold与执行harness是不同层，不能把一段听起来合理的研究计划当成已完成实验或任务结果。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>提出“换一种损失”只是起点；还需实际实现、运行并根据允许的实验反馈决定是否修订。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06855">原论文</a> · <a href="../../../../agent-research/2602.06855-airs-bench/">实现解读</a> · <a href="#qa-7d73d79eb709b84b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:airs-bench" data-paper-title="AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents Agent FAIR at Meta / University of Oxford 2026-02-06 以问题、数据集、指标和人工SOTA定义20个任务。Agent自行提出方法、实现训练、分析实验并修订，不提供基线解法；协议区分Agent、搜索scaffold与运行harness，比较顺序MLGym和树搜索AIRA-dojo。原文§3–5 成本过高，不复现（审查 DONE）；Google/Meta优先补漏资料。成本过高，不复现（审查 DONE）；任务规范收录不等于已接入benchmark。原文每次运行24小时、独占1张H200，20个任务；附录D还列每任务10至20次运行。单A100/A30或Mac下，成本过高，不复现（审查 DONE）。原文附录C–D  自动研究 研究Agent评测协议 Agent 评测与可靠性：如何知道真的做对了 为什么只给问题、数据与指标，而不直接给基线解法，更能测研究 Agent？ 研究过程包括提出方法、实现训练、分析实验和修订，给出完整基线方案会缩小自主设计部分。协议还要区分 Agent、搜索 scaffold 与运行 harness，避免把外层树搜索收益全归模型；任务上人工 SOTA 是参照，不是行动者可偷读的答案脚本。 例如给分类数据与评分规则，让 Agent 自己决定模型和实验；若已提供最佳训练代码，评测更接近执行脚本而非研究设计。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-a7d53ec839366385">为什么只给问题、数据与指标，而不直接给基线解法，更能测研究 Agent？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aairs-bench">AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>研究过程包括提出方法、实现训练、分析实验和修订，给出完整基线方案会缩小自主设计部分。协议还要区分 Agent、搜索 scaffold 与运行 harness，避免把外层树搜索收益全归模型；任务上人工 SOTA 是参照，不是行动者可偷读的答案脚本。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如给分类数据与评分规则，让 Agent 自己决定模型和实验；若已提供最佳训练代码，评测更接近执行脚本而非研究设计。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06855">原论文</a> · <a href="../../../../agent-research/2602.06855-airs-bench/">实现解读</a> · <a href="#qa-a7d53ec839366385">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:airs-bench" data-paper-title="AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents Agent FAIR at Meta / University of Oxford 2026-02-06 以问题、数据集、指标和人工SOTA定义20个任务。Agent自行提出方法、实现训练、分析实验并修订，不提供基线解法；协议区分Agent、搜索scaffold与运行harness，比较顺序MLGym和树搜索AIRA-dojo。原文§3–5 成本过高，不复现（审查 DONE）；Google/Meta优先补漏资料。成本过高，不复现（审查 DONE）；任务规范收录不等于已接入benchmark。原文每次运行24小时、独占1张H200，20个任务；附录D还列每任务10至20次运行。单A100/A30或Mac下，成本过高，不复现（审查 DONE）。原文附录C–D  自动研究 研究Agent评测协议 Agent 评测与可靠性：如何知道真的做对了 顺序MLGym与树搜索AIRA-dojo比较为什么需固定预算？ 搜索组织影响试错覆盖和成本，无限树分支可消耗更多评估。固定资源和标签隔离才能评估scaffold差异，任务指标不同也不能直接相加成统一分数。 例如多跑十倍候选得到更好模型，不应全部归因于搜索方法本身。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-58a3a38594282860">顺序MLGym与树搜索AIRA-dojo比较为什么需固定预算？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aairs-bench">AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>搜索组织影响试错覆盖和成本，无限树分支可消耗更多评估。固定资源和标签隔离才能评估scaffold差异，任务指标不同也不能直接相加成统一分数。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如多跑十倍候选得到更好模型，不应全部归因于搜索方法本身。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06855">原论文</a> · <a href="../../../../agent-research/2602.06855-airs-bench/">实现解读</a> · <a href="#qa-58a3a38594282860">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:airs-bench" data-paper-title="AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents Agent FAIR at Meta / University of Oxford 2026-02-06 以问题、数据集、指标和人工SOTA定义20个任务。Agent自行提出方法、实现训练、分析实验并修订，不提供基线解法；协议区分Agent、搜索scaffold与运行harness，比较顺序MLGym和树搜索AIRA-dojo。原文§3–5 成本过高，不复现（审查 DONE）；Google/Meta优先补漏资料。成本过高，不复现（审查 DONE）；任务规范收录不等于已接入benchmark。原文每次运行24小时、独占1张H200，20个任务；附录D还列每任务10至20次运行。单A100/A30或Mac下，成本过高，不复现（审查 DONE）。原文附录C–D  自动研究 研究Agent评测协议 Agent 评测与可靠性：如何知道真的做对了 AIRS-Bench评测脚本可见意味着test标签也可读吗？ 不意味着，提交预测后由隔离test评分，候选选择只用允许验证反馈。原文部分任务超过SOTA不是本地成绩，未执行完整研究训练不能报告已复现。 例如知道评分函数是准确率，不代表可以读取每个测试样本正确类。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-b06e8ae9651a392c">AIRS-Bench评测脚本可见意味着test标签也可读吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Aairs-bench">AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · FAIR at Meta / University of Oxford</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不意味着，提交预测后由隔离test评分，候选选择只用允许验证反馈。原文部分任务超过SOTA不是本地成绩，未执行完整研究训练不能报告已复现。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如知道评分函数是准确率，不代表可以读取每个测试样本正确类。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2602.06855">原论文</a> · <a href="../../../../agent-research/2602.06855-airs-bench/">实现解读</a> · <a href="#qa-b06e8ae9651a392c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:lifeagentbench" data-paper-title="LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning Agent University of California San Diego 2026-01-20 LifeAgentBench 用可执行 SQL / 程序在饮食、睡眠、活动和情绪记录上生成确定性答案，覆盖长期窗口、跨维度与跨用户任务。LifeAgent 是另一个工具推理基线：先分解子问题，维护证据缓存与中间统计，再根据新证据修订计划并合成回答，不能把 benchmark scorer 当成该 Agent。 完整实验成本过高，不复现（审查 DONE）。它不是临床诊断、治疗或医疗决策系统。仅研究资料，未实现 LifeAgent 或运行 benchmark。完整实验成本过高，不复现（审查 DONE）。它不是临床诊断、治疗或医疗决策系统。正文 Appendix E 明确开放模型推理约 300–500 GPU 小时；含 70B 的较大模型使用 4×A6000，另有闭源 API 和多轮工具基线。这不是单次小样本推理可以重现的整套比较。完整实验成本过高，不复现（审查 DONE）；不下载生活记录、权重或大数据，不运行推理，也不生成本地 metrics / GPU receipt。后续不会自动重试。  评测与可验证Agent 长期异构记录推理 Agent 评测与可靠性：如何知道真的做对了 LifeAgentBench的长期生活记录，为什么不只是对一条事件做分类？ 任务在饮食、睡眠、活动和情绪等记录上提出跨时间窗口、跨维度或跨用户的问题，通常要先取齐有关证据再计算或比较。输入中的一条记录不足以代表整个问题，记录筛选与统计的范围就是答案条件的一部分。 教学例子：比较某周活动与睡眠的关系，需要同一用户该周两类记录；读到一天步数便直接答复会漏掉证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-lifeagentbench-23550dc3" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-d90e5f74c4f4986f">LifeAgentBench的长期生活记录，为什么不只是对一条事件做分类？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alifeagentbench">LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>任务在饮食、睡眠、活动和情绪等记录上提出跨时间窗口、跨维度或跨用户的问题，通常要先取齐有关证据再计算或比较。输入中的一条记录不足以代表整个问题，记录筛选与统计的范围就是答案条件的一部分。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>比较某周活动与睡眠的关系，需要同一用户该周两类记录；读到一天步数便直接答复会漏掉证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.13880v1">原论文</a> · <a href="../../../../agent-research/2601.13880-lifeagentbench/">实现解读</a> · <a href="#qa-d90e5f74c4f4986f">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:lifeagentbench" data-paper-title="LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning Agent University of California San Diego 2026-01-20 LifeAgentBench 用可执行 SQL / 程序在饮食、睡眠、活动和情绪记录上生成确定性答案，覆盖长期窗口、跨维度与跨用户任务。LifeAgent 是另一个工具推理基线：先分解子问题，维护证据缓存与中间统计，再根据新证据修订计划并合成回答，不能把 benchmark scorer 当成该 Agent。 完整实验成本过高，不复现（审查 DONE）。它不是临床诊断、治疗或医疗决策系统。仅研究资料，未实现 LifeAgent 或运行 benchmark。完整实验成本过高，不复现（审查 DONE）。它不是临床诊断、治疗或医疗决策系统。正文 Appendix E 明确开放模型推理约 300–500 GPU 小时；含 70B 的较大模型使用 4×A6000，另有闭源 API 和多轮工具基线。这不是单次小样本推理可以重现的整套比较。完整实验成本过高，不复现（审查 DONE）；不下载生活记录、权重或大数据，不运行推理，也不生成本地 metrics / GPU receipt。后续不会自动重试。  评测与可验证Agent 长期异构记录推理 Agent 评测与可靠性：如何知道真的做对了 SQL scorer 能算出确定答案，为什么不等于已实现 LifeAgent 的工具推理？ scorer 持有规则与记录来验证最终答案，不承担分解问题、检索证据、维护中间统计和修订计划。基准与工具基线的职责不同，不能让行动者直接读参考计算或把通过字段检查当成长期健康记录推理；这里只说明数据任务协议，不提供健康决策建议。 例如验证器能计算一周平均睡眠，Agent 仍须自己选时间窗、查询记录并核对缺失项；调用参考答案函数会绕过这些步骤。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-d23f60fee3459ab1">SQL scorer 能算出确定答案，为什么不等于已实现 LifeAgent 的工具推理？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alifeagentbench">LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>scorer 持有规则与记录来验证最终答案，不承担分解问题、检索证据、维护中间统计和修订计划。基准与工具基线的职责不同，不能让行动者直接读参考计算或把通过字段检查当成长期健康记录推理；这里只说明数据任务协议，不提供健康决策建议。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如验证器能计算一周平均睡眠，Agent 仍须自己选时间窗、查询记录并核对缺失项；调用参考答案函数会绕过这些步骤。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.13880v1">原论文</a> · <a href="../../../../agent-research/2601.13880-lifeagentbench/">实现解读</a> · <a href="#qa-d23f60fee3459ab1">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:lifeagentbench" data-paper-title="LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning Agent University of California San Diego 2026-01-20 LifeAgentBench 用可执行 SQL / 程序在饮食、睡眠、活动和情绪记录上生成确定性答案，覆盖长期窗口、跨维度与跨用户任务。LifeAgent 是另一个工具推理基线：先分解子问题，维护证据缓存与中间统计，再根据新证据修订计划并合成回答，不能把 benchmark scorer 当成该 Agent。 完整实验成本过高，不复现（审查 DONE）。它不是临床诊断、治疗或医疗决策系统。仅研究资料，未实现 LifeAgent 或运行 benchmark。完整实验成本过高，不复现（审查 DONE）。它不是临床诊断、治疗或医疗决策系统。正文 Appendix E 明确开放模型推理约 300–500 GPU 小时；含 70B 的较大模型使用 4×A6000，另有闭源 API 和多轮工具基线。这不是单次小样本推理可以重现的整套比较。完整实验成本过高，不复现（审查 DONE）；不下载生活记录、权重或大数据，不运行推理，也不生成本地 metrics / GPU receipt。后续不会自动重试。  评测与可验证Agent 长期异构记录推理 Agent 评测与可靠性：如何知道真的做对了 SQL可执行、证据完整与最终正确有什么区别？ 可执行只说明语法和运行，EX在其分母上查证据完整，Acc|EX再看完整证据条件的答案。混用分母会掩盖推理或检索问题。 例如查询能跑但少筛了一位用户，仍未取全所需证据。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-5961b103e689800b">SQL可执行、证据完整与最终正确有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alifeagentbench">LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>可执行只说明语法和运行，EX在其分母上查证据完整，Acc|EX再看完整证据条件的答案。混用分母会掩盖推理或检索问题。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如查询能跑但少筛了一位用户，仍未取全所需证据。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.13880v1">原论文</a> · <a href="../../../../agent-research/2601.13880-lifeagentbench/">实现解读</a> · <a href="#qa-5961b103e689800b">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:lifeagentbench" data-paper-title="LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning Agent University of California San Diego 2026-01-20 LifeAgentBench 用可执行 SQL / 程序在饮食、睡眠、活动和情绪记录上生成确定性答案，覆盖长期窗口、跨维度与跨用户任务。LifeAgent 是另一个工具推理基线：先分解子问题，维护证据缓存与中间统计，再根据新证据修订计划并合成回答，不能把 benchmark scorer 当成该 Agent。 完整实验成本过高，不复现（审查 DONE）。它不是临床诊断、治疗或医疗决策系统。仅研究资料，未实现 LifeAgent 或运行 benchmark。完整实验成本过高，不复现（审查 DONE）。它不是临床诊断、治疗或医疗决策系统。正文 Appendix E 明确开放模型推理约 300–500 GPU 小时；含 70B 的较大模型使用 4×A6000，另有闭源 API 和多轮工具基线。这不是单次小样本推理可以重现的整套比较。完整实验成本过高，不复现（审查 DONE）；不下载生活记录、权重或大数据，不运行推理，也不生成本地 metrics / GPU receipt。后续不会自动重试。  评测与可验证Agent 长期异构记录推理 Agent 评测与可靠性：如何知道真的做对了 只读SQL与Context Prompting怎样隔离gold？ 前者模型先生成允许查询，执行结果再回给模型；后者先按用户筛公开证据，金标都在评分端。数字按规定分段容差，多项需同项数匹配，不能改substring凑通过。 例如回答包含正确词但还多列错误项，不应因子串命中就算全对。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-d7e908d939e49c24">只读SQL与Context Prompting怎样隔离gold？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Alifeagentbench">LifeAgentBench: Benchmarking LLMs for Long-Horizon, Cross-Dimensional Lifestyle Health Reasoning</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California San Diego</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者模型先生成允许查询，执行结果再回给模型；后者先按用户筛公开证据，金标都在评分端。数字按规定分段容差，多项需同项数匹配，不能改substring凑通过。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如回答包含正确词但还多列错误项，不应因子串命中就算全对。</p>
<p class="ar-learning-sources">依据：背景与主要改动；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.13880v1">原论文</a> · <a href="../../../../agent-research/2601.13880-lifeagentbench/">实现解读</a> · <a href="#qa-d7e908d939e49c24">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coreflect" data-paper-title="CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation Agent University of Illinois Urbana-Champaign 2026-01-18 Sec.2.1–2.5 / Appendix G：953条通过真实LLM一致性检查的persona-scenario；planner/simulator/evaluator/analyzer是核心语义模型。只写JSON状态机、对给定数字求均值或手工替换rubric都不能复现其核心，因此不强建低成本heuristic adapter。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  Agent评测与自进化 对话模拟与rubric共演化 Agent 评测与可靠性：如何知道真的做对了 CoReflect里的planner、simulator、evaluator、analyzer分别产生什么？ planner组织模拟任务，simulator形成对话交互，evaluator按当前标准评价，analyzer从评价与反馈中提炼反思，再影响下一轮任务和标准。这些是语义模型职责，不是四个JSON字段；本地未用手写规则假冒这些核心模块。 教学例子：某轮对话暴露评判标准含糊，analyzer提炼问题，后续再调整rubric并规划能检验该问题的新情境。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-coreflect-7d1f277e" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-73a0fa96c34acc53">CoReflect里的planner、simulator、evaluator、analyzer分别产生什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoreflect">CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>planner组织模拟任务，simulator形成对话交互，evaluator按当前标准评价，analyzer从评价与反馈中提炼反思，再影响下一轮任务和标准。这些是语义模型职责，不是四个JSON字段；本地未用手写规则假冒这些核心模块。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某轮对话暴露评判标准含糊，analyzer提炼问题，后续再调整rubric并规划能检验该问题的新情境。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12208v1">原论文</a> · <a href="../../../../agent-research/2601.12208-coreflect/">实现解读</a> · <a href="#qa-73a0fa96c34acc53">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coreflect" data-paper-title="CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation Agent University of Illinois Urbana-Champaign 2026-01-18 Sec.2.1–2.5 / Appendix G：953条通过真实LLM一致性检查的persona-scenario；planner/simulator/evaluator/analyzer是核心语义模型。只写JSON状态机、对给定数字求均值或手工替换rubric都不能复现其核心，因此不强建低成本heuristic adapter。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  Agent评测与自进化 对话模拟与rubric共演化 Agent 评测与可靠性：如何知道真的做对了 为什么只更新 rubric 字符串或对给定分数求均值，不能复现 CoReflect 的反思共演化？ 核心需要语义 planner 生成情境、simulator 产生对话、evaluator 评价，再由 analyzer 依据理由发现不足并同时改任务与准则。机械状态转移只实现外壳，没有这些语义判断与真实交互证据；原方法公式用于解释流程，不能被当成本地模块已运行。 例如分析器应发现某类同理心评价遗漏再产生新情境，手工把权重从一改成二并不会自动获得这类语义反思能力。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-9336a21730fbc0d6">为什么只更新 rubric 字符串或对给定分数求均值，不能复现 CoReflect 的反思共演化？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoreflect">CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>核心需要语义 planner 生成情境、simulator 产生对话、evaluator 评价，再由 analyzer 依据理由发现不足并同时改任务与准则。机械状态转移只实现外壳，没有这些语义判断与真实交互证据；原方法公式用于解释流程，不能被当成本地模块已运行。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如分析器应发现某类同理心评价遗漏再产生新情境，手工把权重从一改成二并不会自动获得这类语义反思能力。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12208v1">原论文</a> · <a href="../../../../agent-research/2601.12208-coreflect/">实现解读</a> · <a href="#qa-9336a21730fbc0d6">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coreflect" data-paper-title="CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation Agent University of Illinois Urbana-Champaign 2026-01-18 Sec.2.1–2.5 / Appendix G：953条通过真实LLM一致性检查的persona-scenario；planner/simulator/evaluator/analyzer是核心语义模型。只写JSON状态机、对给定数字求均值或手工替换rubric都不能复现其核心，因此不强建低成本heuristic adapter。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  Agent评测与自进化 对话模拟与rubric共演化 Agent 评测与可靠性：如何知道真的做对了 CoReflect的persona-scenario一致性检查，与仅保证样本JSON格式合法有什么区别？ 格式合法只保证字段可读，不能证明人物设定与情境在语义上相容。原文保留经过真实LLM一致性检查的persona-scenario；该筛选是任务质量的一部分。合法状态机或人为打分并不能补上缺失的语义检查与反思模型。 教学例子：字段齐全却把人物设为“无法上网”又要求其刚完成网络预约，JSON仍合法，语义一致性却需要核验。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-27514a4a3c2740e3">CoReflect的persona-scenario一致性检查，与仅保证样本JSON格式合法有什么区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoreflect">CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>格式合法只保证字段可读，不能证明人物设定与情境在语义上相容。原文保留经过真实LLM一致性检查的persona-scenario；该筛选是任务质量的一部分。合法状态机或人为打分并不能补上缺失的语义检查与反思模型。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>字段齐全却把人物设为“无法上网”又要求其刚完成网络预约，JSON仍合法，语义一致性却需要核验。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12208v1">原论文</a> · <a href="../../../../agent-research/2601.12208-coreflect/">实现解读</a> · <a href="#qa-27514a4a3c2740e3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:coreflect" data-paper-title="CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation Agent University of Illinois Urbana-Champaign 2026-01-18 Sec.2.1–2.5 / Appendix G：953条通过真实LLM一致性检查的persona-scenario；planner/simulator/evaluator/analyzer是核心语义模型。只写JSON状态机、对给定数字求均值或手工替换rubric都不能复现其核心，因此不强建低成本heuristic adapter。 完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。状态：仅文献与成本收录，没有可执行能力adapter，不以heuristic冒充核心模型。完整实验：成本过高，不复现（审查 DONE），不下载权重/数据、不自动重试。此为用户指定的历史会议补漏，不是本日新发表。本轮不提供可运行模型、loss包装或伪测试。库里已有通用KL/RL/统计工具并不构成本文核心流程；原文语义模型、API多轮生成或大规模训练不能用手工规则替换。仅保存经过核验的方法、资源、源码状态与原图，终态为 not_reproduced_high_cost。后续不得自动移回待训练队列。  Agent评测与自进化 对话模拟与rubric共演化 Agent 评测与可靠性：如何知道真的做对了 CoReflect本地是否实现953场景和完整语义模块？ 没有，目前文献收录，不强造低成本heuristic adapter。JSON状态机或对给定数字求均值不能代替真实LLM检查与对话生成，公式只解释原方法。 例如循环次数增加不能证明评价器真的学会新判断维度。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-16d199a59b834d14">CoReflect本地是否实现953场景和完整语义模块？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Acoreflect">CoReflect: A Reflective Co-Evolution Framework for Improving Conversational Evaluation</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of Illinois Urbana-Champaign</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>没有，目前文献收录，不强造低成本heuristic adapter。JSON状态机或对给定数字求均值不能代替真实LLM检查与对话生成，公式只解释原方法。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如循环次数增加不能证明评价器真的学会新判断维度。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2601.12208v1">原论文</a> · <a href="../../../../agent-research/2601.12208-coreflect/">实现解读</a> · <a href="#qa-16d199a59b834d14">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sopbench-protocol" data-paper-title="SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints Agent University of California, Santa Barbara 2025-03-11 SOPBench 将服务规范写成有向约束图：Agent 必须先调用 helper 检验必要条件，再执行服务。它不仅核对最终数据库是否正确，还检查服务本身是否被允许、必要验证是否真正且按要求发生，防止“猜中结果”绕过流程。 完整实验成本过高，不复现（审查 DONE）；诊断只检查构造轨迹的顺序、错误用户、错误状态及 oracle 负控，报告 fixture 数，不报模型成功率。L1 纯 CPU 协议组件，diagnostic only，不是模型能力或七域环境复现。完整实验成本过高，不复现（审查 DONE）；未接入 Evolve。Rule 以嵌套表达式表示约束；evaluate_trace 对每一次服务调用只看其之前的 helper 前缀，并将三项检查联合。参考约束真值、oracle 最终状态都只由轨迹提交后的评测器使用，没有传给任何被测策略。拒绝服务可以通过，但必须与 oracle 的数据库结果一致；  工具使用与环境 SOP约束与程序验收 Agent 评测与可靠性：如何知道真的做对了 SOPBench里的服务约束图，节点是在记录聊天步骤，还是规定服务前要验证什么？ 它把服务连接到约束，再把约束连接到可执行的helper验证；结构表达服务何时被允许以及需要哪些前置检查，不是按聊天轮数排列的摘要。先找到服务依赖的约束，才能知道Agent该验证什么，而非只看最后回复是否顺畅。 教学例子：某项服务要求先核验资格，图中应能沿服务找到资格约束和对应helper，而不是只出现一句“我已检查”。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-sopbench-protocol-97674f6a" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-8304d284c96dd917">SOPBench里的服务约束图，节点是在记录聊天步骤，还是规定服务前要验证什么？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asopbench-protocol">SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>它把服务连接到约束，再把约束连接到可执行的helper验证；结构表达服务何时被允许以及需要哪些前置检查，不是按聊天轮数排列的摘要。先找到服务依赖的约束，才能知道Agent该验证什么，而非只看最后回复是否顺畅。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>某项服务要求先核验资格，图中应能沿服务找到资格约束和对应helper，而不是只出现一句“我已检查”。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.08669v1">原论文</a> · <a href="../../../../agent-research/2503.08669-sopbench-protocol/">实现解读</a> · <a href="#qa-8304d284c96dd917">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sopbench-protocol" data-paper-title="SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints Agent University of California, Santa Barbara 2025-03-11 SOPBench 将服务规范写成有向约束图：Agent 必须先调用 helper 检验必要条件，再执行服务。它不仅核对最终数据库是否正确，还检查服务本身是否被允许、必要验证是否真正且按要求发生，防止“猜中结果”绕过流程。 完整实验成本过高，不复现（审查 DONE）；诊断只检查构造轨迹的顺序、错误用户、错误状态及 oracle 负控，报告 fixture 数，不报模型成功率。L1 纯 CPU 协议组件，diagnostic only，不是模型能力或七域环境复现。完整实验成本过高，不复现（审查 DONE）；未接入 Evolve。Rule 以嵌套表达式表示约束；evaluate_trace 对每一次服务调用只看其之前的 helper 前缀，并将三项检查联合。参考约束真值、oracle 最终状态都只由轨迹提交后的评测器使用，没有传给任何被测策略。拒绝服务可以通过，但必须与 oracle 的数据库结果一致；  工具使用与环境 SOP约束与程序验收 Agent 评测与可靠性：如何知道真的做对了 数据库最终状态正确，为什么仍可能在 SOPBench 判失败？ 服务还需被允许，必要 helper 验证也要实际且按规定顺序发生。And、Or 与 Chain 表达不同前提逻辑，不能仅凭猜中结果绕过流程；完整通过要求资格、数据库与程序共同成立，把三者合并成最终状态检查会遗漏协议遵循能力。 例如退款金额碰巧正确，但 Agent 没先验证订单资格，仍违反 SOP；Chain 要求先查资格再操作，事后补查不能抵消。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-bf216373788d6b3c">数据库最终状态正确，为什么仍可能在 SOPBench 判失败？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asopbench-protocol">SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>服务还需被允许，必要 helper 验证也要实际且按规定顺序发生。And、Or 与 Chain 表达不同前提逻辑，不能仅凭猜中结果绕过流程；完整通过要求资格、数据库与程序共同成立，把三者合并成最终状态检查会遗漏协议遵循能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如退款金额碰巧正确，但 Agent 没先验证订单资格，仍违反 SOP；Chain 要求先查资格再操作，事后补查不能抵消。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.08669v1">原论文</a> · <a href="../../../../agent-research/2503.08669-sopbench-protocol/">实现解读</a> · <a href="#qa-bf216373788d6b3c">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sopbench-protocol" data-paper-title="SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints Agent University of California, Santa Barbara 2025-03-11 SOPBench 将服务规范写成有向约束图：Agent 必须先调用 helper 检验必要条件，再执行服务。它不仅核对最终数据库是否正确，还检查服务本身是否被允许、必要验证是否真正且按要求发生，防止“猜中结果”绕过流程。 完整实验成本过高，不复现（审查 DONE）；诊断只检查构造轨迹的顺序、错误用户、错误状态及 oracle 负控，报告 fixture 数，不报模型成功率。L1 纯 CPU 协议组件，diagnostic only，不是模型能力或七域环境复现。完整实验成本过高，不复现（审查 DONE）；未接入 Evolve。Rule 以嵌套表达式表示约束；evaluate_trace 对每一次服务调用只看其之前的 helper 前缀，并将三项检查联合。参考约束真值、oracle 最终状态都只由轨迹提交后的评测器使用，没有传给任何被测策略。拒绝服务可以通过，但必须与 oracle 的数据库结果一致；  工具使用与环境 SOP约束与程序验收 Agent 评测与可靠性：如何知道真的做对了 And、Or与Chain约束对验证顺序有什么不同？ And要求各条件但不强制子次序，Or允许已验真分支，Chain要求前后顺序。把三者统一为无序集合会放过先执行后检查等流程违规。 例如身份核验后才可转账，是Chain，而非事后补验证也能凑齐。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-f5c9691726e12bb8">And、Or与Chain约束对验证顺序有什么不同？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asopbench-protocol">SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>And要求各条件但不强制子次序，Or允许已验真分支，Chain要求前后顺序。把三者统一为无序集合会放过先执行后检查等流程违规。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如身份核验后才可转账，是Chain，而非事后补验证也能凑齐。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.08669v1">原论文</a> · <a href="../../../../agent-research/2503.08669-sopbench-protocol/">实现解读</a> · <a href="#qa-f5c9691726e12bb8">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:sopbench-protocol" data-paper-title="SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints Agent University of California, Santa Barbara 2025-03-11 SOPBench 将服务规范写成有向约束图：Agent 必须先调用 helper 检验必要条件，再执行服务。它不仅核对最终数据库是否正确，还检查服务本身是否被允许、必要验证是否真正且按要求发生，防止“猜中结果”绕过流程。 完整实验成本过高，不复现（审查 DONE）；诊断只检查构造轨迹的顺序、错误用户、错误状态及 oracle 负控，报告 fixture 数，不报模型成功率。L1 纯 CPU 协议组件，diagnostic only，不是模型能力或七域环境复现。完整实验成本过高，不复现（审查 DONE）；未接入 Evolve。Rule 以嵌套表达式表示约束；evaluate_trace 对每一次服务调用只看其之前的 helper 前缀，并将三项检查联合。参考约束真值、oracle 最终状态都只由轨迹提交后的评测器使用，没有传给任何被测策略。拒绝服务可以通过，但必须与 oracle 的数据库结果一致；  工具使用与环境 SOP约束与程序验收 Agent 评测与可靠性：如何知道真的做对了 SOPBench helper调用记录能由Agent自报替代吗？ 不能，procedure_complete需可信执行轨迹，验证必须真实发生且时序满足图。gold状态只供评分，不向代理泄露；当前协议组件不等于完整生产服务Agent能力。 例如回答我已验证不代表日志里真的有有效helper调用。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-cd44b09f931686f2">SOPBench helper调用记录能由Agent自报替代吗？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Asopbench-protocol">SOPBench: Evaluating Language Agents at Following Standard Operating Procedures and Constraints</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · University of California, Santa Barbara</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，procedure_complete需可信执行轨迹，验证必须真实发生且时序满足图。gold状态只供评分，不向代理泄露；当前协议组件不等于完整生产服务Agent能力。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如回答我已验证不代表日志里真的有有效helper调用。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2503.08669v1">原论文</a> · <a href="../../../../agent-research/2503.08669-sopbench-protocol/">实现解读</a> · <a href="#qa-cd44b09f931686f2">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gaia" data-paper-title="GAIA" data-learning-pending="false" data-level="basics" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="GAIA Agent Meta AI 2023-11-21 以 466 个真实问题联合考查推理、多模态、网页浏览与工具使用，采用精确短答案和三级难度。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。gaia-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.4000。  通用 Agent 评测 Agent 评测与可靠性：如何知道真的做对了 GAIA每题的提交对象是完整推理长文，还是可核对的最终短答案？ 评分对象是最终答案，经规定的规范化后与金标精确比较；完成题目仍可能需要浏览网页、读图与调用工具。先区分求解过程与提交格式，才能理解为什么写了很多合理步骤也未必获得最终命中，格式失败也不能掩盖为推理成功。 教学例子：题目要求一个人名时，提交应给可核对的人名；大段搜索过程里没有明确最终答案，不能自动算命中。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<span id="paper-agent-research-gaia-62649810" class="ar-learning-paper-anchor"></span>
<p class="ar-learning-level">基础理解</p>
<h2 id="qa-802c89c175ab9d3e">GAIA每题的提交对象是完整推理长文，还是可核对的最终短答案？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agaia">GAIA</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>评分对象是最终答案，经规定的规范化后与金标精确比较；完成题目仍可能需要浏览网页、读图与调用工具。先区分求解过程与提交格式，才能理解为什么写了很多合理步骤也未必获得最终命中，格式失败也不能掩盖为推理成功。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>题目要求一个人名时，提交应给可核对的人名；大段搜索过程里没有明确最终答案，不能自动算命中。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2311.12983">原论文</a> · <a href="../../../../agent-research/2311.12983-gaia/">实现解读</a> · <a href="#qa-802c89c175ab9d3e">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gaia" data-paper-title="GAIA" data-learning-pending="false" data-level="mechanism" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="GAIA Agent Meta AI 2023-11-21 以 466 个真实问题联合考查推理、多模态、网页浏览与工具使用，采用精确短答案和三级难度。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。gaia-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.4000。  通用 Agent 评测 Agent 评测与可靠性：如何知道真的做对了 精确短答案为什么仍能考查多工具推理，而不只是记忆问答？ 简短输出只是评分接口，得到答案可能需要浏览、多模态理解、计算与跨来源核对。规范化匹配把终点判断变得明确，却不显示中间证据质量，也不能独立解释失败来自哪一步；答对率需与真实执行轨迹区分，参考短答案不能提前进 Agent 提示。 例如最终只输出一个年份，但需要先从图片识别人名，再浏览资料查事件并核对时间；短输出并不代表求解过程简单。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">核心机制</p>
<h2 id="qa-7f1f7590b48a18a3">精确短答案为什么仍能考查多工具推理，而不只是记忆问答？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agaia">GAIA</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>简短输出只是评分接口，得到答案可能需要浏览、多模态理解、计算与跨来源核对。规范化匹配把终点判断变得明确，却不显示中间证据质量，也不能独立解释失败来自哪一步；答对率需与真实执行轨迹区分，参考短答案不能提前进 Agent 提示。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如最终只输出一个年份，但需要先从图片识别人名，再浏览资料查事件并核对时间；短输出并不代表求解过程简单。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2311.12983">原论文</a> · <a href="../../../../agent-research/2311.12983-gaia/">实现解读</a> · <a href="#qa-7f1f7590b48a18a3">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gaia" data-paper-title="GAIA" data-learning-pending="false" data-level="comparison" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="GAIA Agent Meta AI 2023-11-21 以 466 个真实问题联合考查推理、多模态、网页浏览与工具使用，采用精确短答案和三级难度。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。gaia-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.4000。  通用 Agent 评测 Agent 评测与可靠性：如何知道真的做对了 GAIA的规范化精确匹配，与让模型裁判按语义给分有何区别？ 前者按固定规范化后的答案相等关系计算命中，后者需要额外裁判判断表达是否等义。两种评分器的容错与偏差不同，不能未经说明用语义裁判放宽匹配后仍报告同一GAIA分数。规范化也应是预先固定规则，而非看到金标后临时改写预测。 教学例子：一种规则只处理允许的表面形式差异；若另请模型把一段模糊描述判为等义，就是更换了验收器。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">方法对比</p>
<h2 id="qa-9451bc182cb840df">GAIA的规范化精确匹配，与让模型裁判按语义给分有何区别？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agaia">GAIA</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>前者按固定规范化后的答案相等关系计算命中，后者需要额外裁判判断表达是否等义。两种评分器的容错与偏差不同，不能未经说明用语义裁判放宽匹配后仍报告同一GAIA分数。规范化也应是预先固定规则，而非看到金标后临时改写预测。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>一种规则只处理允许的表面形式差异；若另请模型把一段模糊描述判为等义，就是更换了验收器。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2311.12983">原论文</a> · <a href="../../../../agent-research/2311.12983-gaia/">实现解读</a> · <a href="#qa-9451bc182cb840df">问题链接</a></p>
</details>
</article>
<article class="ar-learning-card ar-learning-qa" data-learning-card data-identity="agent-research:gaia" data-paper-title="GAIA" data-learning-pending="false" data-level="implementation" data-domain="agent-research" data-theme="agent-research" data-topic="agent-research/evaluation-and-reliability" data-search="GAIA Agent Meta AI 2023-11-21 以 466 个真实问题联合考查推理、多模态、网页浏览与工具使用，采用精确短答案和三级难度。 保真度：核心机制复现。保真度：核心机制复现。本页不把确定性 mini-suite 冒充原论文完整 benchmark。本地只验证论文特有目标、状态更新或评测协议；没有复刻原论文大模型、多卡训练、私有环境或完整公开 benchmark，因而只报告机制验证。gaia-mini、120 episodes、seed 42：joint success 1.0000，average cost 1.4000。  通用 Agent 评测 Agent 评测与可靠性：如何知道真的做对了 GAIA normalize能否在看gold后任意放宽？ 不能，应固定允许的规范化和题集合，gold只在评分器出现。当前本地只验证接口或协议，没有完整真实网页和多模态任务运行，不能报告原基准成绩。 例如仅因错答案含正确子串就改匹配规则，会改变评测定义。 2026-10-27">
<p class="ar-learning-card__domain"><a href="./">Agent / 评测与可靠性：如何知道真的做对了</a></p>
<p class="ar-learning-level">实现细节</p>
<h2 id="qa-38f78acc30af0647">GAIA normalize能否在看gold后任意放宽？</h2>
<p class="ar-learning-paper"><a href="../../../all/?paper=agent-research%3Agaia">GAIA</a></p>
<p class="ar-learning-card__meta">问答新增：2026-10-27 · Meta AI</p>
<details class="ar-learning-answer"><summary>展开答案与例子</summary>
<p><strong>答案：</strong>不能，应固定允许的规范化和题集合，gold只在评分器出现。当前本地只验证接口或协议，没有完整真实网页和多模态任务运行，不能报告原基准成绩。</p>
<p class="ar-learning-example"><strong>教学例子：</strong>例如仅因错答案含正确子串就改匹配规则，会改变评测定义。</p>
<p class="ar-learning-sources">依据：背景与主要改动、核心公式；例子用于解释机制。</p>
<p class="ar-learning-card__links"><a href="https://arxiv.org/abs/2311.12983">原论文</a> · <a href="../../../../agent-research/2311.12983-gaia/">实现解读</a> · <a href="#qa-38f78acc30af0647">问题链接</a></p>
</details>
</article>
</div>
<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>
</div>


<details class="ar-learning-guide" markdown="1"><summary>主题导读与阅读路线</summary>

## 先想一个问题

怎样区分模型成功、环境碰巧放行、评分器偏差和不安全的越权？

## 记住这一点

先固定任务、可见输入、允许动作、成功条件和预算，再讨论分数。GAIA 用需要推理与工具的真实问题考查端到端结果；扰动协议进一步控制某个输入因素变化，检验系统是否仍完成同一目标。安全评估还要问动作是否有依据、有权限，不能仅以最终答案正确为由放过越权。评分器与 actor 的信息边界是协议的一部分。

## 一个例子

给同一任务做两次运行，只改变工具说明中的一个无关冗余字段，其余后端、数据和成功条件都固定，才能研究这类扰动的影响。如果改动顺带删掉必要参数，任务已不可解，就不能简单把失败计为“不稳健”。若评分过程超时，应同时报告已评分结果和未评分数量，而非删掉未知样本。

## 什么时候要小心

语法合法不代表语义保持，模拟器高分也不等于真人或生产效果。库里的 GAIA mini-suite 和 AgentPerturb CPU 协议接口不是官方完整 benchmark 接入；安全夹具也不证明真实攻击防御率。只做文献和成本审查的条目不能出现在已验证能力清单。

## 先读这几篇

先读 GAIA，明确端到端任务与难度；再读 AgentPerturb，理解单因素、目标保持和独立验证的配对评测。阅读每篇本地边界，分别识别官方任务、CPU协议诊断和未运行部分。

1. [GAIA](../../../agent-research/2311.12983-gaia/README.md) · [原论文](https://arxiv.org/abs/2311.12983)
2. [AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations](../../../agent-research/2610.21624-agent-perturb/README.md) · [原论文](https://arxiv.org/abs/2610.21624)

## 自测一下

100项任务中只完成80项评分，其中60项成功；可以只报告75%成功率并省略剩余20项吗？

??? note "展开参考答案"

    应说明75%是已评分子集的条件成功率，同时保留完整100项分母与20项未知结果。若任务同权，整体成功率目前只能界定在60%到80%之间。进一步归因需要区分执行失败、评分中断和真正任务错误。

</details>

[跨主题搜索全部问答](../../all.md) · [最近新增](../../recent.md)
