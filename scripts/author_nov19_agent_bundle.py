"""Authored, reviewed five-paper Agent/RSI delivery for 2026-11-19.

No abstract-to-document generator: prose, questions and comparisons below are
individually authored against fixed v1 method sections and exact local scope.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-19"
AUDIT = ROOT / "docs/research-audits/nov19-latest"
HEADINGS = [
    "背景与主要改动",
    "核心公式",
    "数据协议与代码映射",
    "结果、负控与边界",
    "高成本完整实验",
]

FLOWS = {
    "ahe-beta": (
        "S[多轮用户会话] --> I[核实问题与需求]\n  I --> A[Architect合并与PM隐含PRD]\n  A --> E[证据包准入]\n  E --> D[RFC设计及代码审查]\n  D --> H[当前head批准后才可采用]",
        "S[Multi-turn user sessions] --> I[Verified issues and requirements]\n  I --> A[Architect consolidation and PM PRDs]\n  A --> E[Evidence-package admission]\n  E --> D[RFC design and code review]\n  D --> H[Approval bound to current head]",
    ),
    "timeout-cascades": (
        "T[原始任务] --> S[小模型尝试]\n  S --> V{时限内有效patch且测试通过}\n  V -->|是| R[仅计小模型]\n  V -->|否| L[大模型从原始状态冷启动]\n  L --> C[两段GPU小时及串行时延]",
        "T[Original task] --> S[Small-model attempt]\n  S --> V{Valid passing patch within timeout}\n  V -->|Yes| R[Charge small attempt only]\n  V -->|No| L[Large-model cold restart]\n  L --> C[Charge both attempts and latency]",
    ),
    "kaer": (
        "P[可信注册表和任务策略] --> V[验证能力和数据流]\n  V --> A[执行子任务]\n  A --> F[仅有限失败模板进入planner]\n  F --> R[七种算子修改未完成后缀]\n  R --> V",
        "P[Trusted registry and task policy] --> V[Validate capabilities and data flows]\n  V --> A[Execute subtask]\n  A --> F[Finite failure templates only to planner]\n  F --> R[Seven operators on uncompleted suffix]\n  R --> V",
    ),
    "safe-personal-rsi": (
        "H[父版本和prompt候选] --> F[搜索与重复确认反例]\n  F --> R[回滚定位及最多两次修复]\n  R --> V[局部verification]\n  V --> G[独立完整admission]\n  G -->|通过| W[采用工作版本]\n  G -->|拒绝或证据不足| H",
        "H[Parent and prompt candidate] --> F[Search and repeated confirmation]\n  F --> R[Rollback localization and up to two repairs]\n  R --> V[Local verification]\n  V --> G[Separate complete admission]\n  G -->|Pass| W[Adopt working version]\n  G -->|Reject or insufficient evidence| H",
    ),
    "rsibench-infra": (
        "B[官方baseline和固定资源] --> A[Agent跨栈优化]\n  A --> O[单一OCI层]\n  O --> S[独立Serve或Train逐rank应用同digest]\n  S --> V[不加载候选层的Benchmark]\n  V --> Q[质量门通过后端到端计时]",
        "B[Official baseline and fixed resources] --> A[Agent cross-stack optimization]\n  A --> O[Single OCI layer]\n  O --> S[Independent Serve or Train with same digest on each rank]\n  S --> V[Benchmark never loads candidate layer]\n  V --> Q[Quality gate then end-to-end timing]",
    ),
}

PAPERS = [
    dict(
        key="ahe-beta",
        id="2611.24924",
        title="Agentic Harness Engineering Beta: Requirement-Centered Evolution of Agent Harnesses",
        cn_title="AHE-Beta：让需求证据而非基准分数决定Harness演进",
        author="Jiahang Lin",
        org="Fudan University",
        published="2026-11-18T18:52:13Z",
        topic="执行框架与自改进",
        tier="l0_interface",
        peer="harness2",
        card="harness-and-self-improvement",
        peer_path="2610.14224-harness2",
        code="https://github.com/Curry09/AHE-Beta/tree/0370ec20a9ad90053a5a50ed21d491eb5480b975",
        license="MIT",
        source_locations=[
            "§3.1–3.3",
            "Algorithm1",
            "Appendix D role/evidence access",
            "Appendix E cost",
            "Appendix F human A/B",
        ],
        page=2,
        figure="Figure 1",
        crop=[100, 45, 510, 382],
        method="AHE-Beta把演进的依据从测试分数移到经过核实的用户需求。模拟用户进行多轮交互并提交问题；Triage把问题核实成可泛化需求，Architect按共同根因合并至少两个需求，PM从跨会话记录找隐含产品需求。开发者只接收被准入的需求及其证据包。",
        method_en="AHE-Beta moves evolution selection from benchmark scores to verified user requirements. A simulated user interacts over multiple turns and files issues. Triage verifies generalizable requirements, the Architect consolidates at least two requirements by root cause, and the PM identifies implicit product needs across sessions. Developers receive only admitted requirements and their evidence packages.",
        mechanism="证据包只有被引用会话的运行日志、公开任务和执行条件，用户对话、隐藏测试和grader不能传给开发者。RFC先做设计审查，代码再按验收标准审查；合并时批准必须绑定当前PR head，且RFC仍与已审设计一致。这里的“verified”是上游角色判断，不是形式正确性证明。",
        mechanism_en="The delivery package contains cited runtime logs, public tasks and execution conditions, but excludes user conversations, hidden tests and graders. Design review precedes implementation; code review checks acceptance criteria. Merge approval must bind the current PR head and the unchanged reviewed RFC. Verification is an upstream role judgment, not a formal correctness proof.",
        formula=r"A_t=(R_t\setminus C_t)\cup R_t^{con}\cup D_t,\qquad merge=admitted\land review_{design}\land review_{code}\land head_{approved}=head_{current}.",
        result="作者在38个held-out Harbor任务上报告pass@1从21.9%到33.3%，执行token减少40.8%；token不含用户模拟。盲测人类A/B有48个有效配对，其中31个偏好AHE-Beta；这是受控用户研究，不是生产流量A/B。每个演进配置只有一条演进run，不能把下游重复评测当独立演进重复。",
        result_en="On 38 held-out Harbor tasks, the paper reports pass@1 increasing from 21.9% to 33.3% and 40.8% fewer execution tokens, excluding user simulation. In a blinded human A/B study, 31 of 48 valid pairs prefer AHE-Beta. This is a controlled user study, not production traffic. Each evolution configuration contributes one evolution run; repeated downstream evaluation is not independent evolution replication.",
        local="只实现类型化Evidence/Requirement交付集、已核实合并需求的covers消解，以及绑定head与RFC的纯merge_eligible判定。没有模拟用户、Triage/Architect/PM语言判断、开发Agent或真正git合并。结构字段不保证字符串内部绝无隐藏答案，所以保持L0，不把类型检查称为语义安全。",
        local_en="The local slice implements typed Evidence/Requirement delivery, covers resolution for verified consolidations, and a pure merge_eligible decision bound to head and RFC. It does not implement user simulation, semantic Triage/Architect/PM judgments, a coding agent or actual git merging. Typed fields cannot prove their strings contain no hidden answers; this remains L0, not a semantic security claim.",
        controls="测试确认未核实的合并需求不能吞掉原需求；原始issue不能作为交付类型；证据为空、head过期、RFC变动或全套测试未完成均不能通过。无benchmark score、gold或隐藏test参数，但不提供恶意回调沙箱。",
        controls_en="Tests ensure an unverified consolidation cannot suppress original requirements; raw issues are not delivery types; empty evidence, stale heads, changed RFCs and unfinished suites cannot pass. There are no benchmark-score, gold-answer or hidden-test parameters, but no sandbox for malicious callbacks is provided.",
        cost="主N=32配置在五个修改轮记录1.92B token，六轮安排、多角色前沿API、38任务与E2B沙箱；单卡不能廉价等价替代这些调用和环境。只运行秒级CPU协议诊断。",
        cost_en="The main N=32 configuration records 1.92B tokens over five modification rounds, with a six-round schedule, multiple frontier APIs, 38 evaluation tasks and E2B sandboxes. A single GPU cannot cheaply reproduce these calls and environments. Only seconds-scale CPU protocol diagnostics run.",
        compare="Harness²按执行对照提出、组合并积累经验，且不使用rubric；AHE-Beta把跨会话需求、证据准入和head绑定审查作为演进主干。两者都不能由本地固定角色替身的通过数证明泛化能力。",
        compare_en="Harness² proposes and composes from execution contrasts and accumulates experience without rubrics. AHE-Beta instead centers cross-session requirements, evidence admission and head-bound review. Passing local fixed-role controls establishes neither method's generalization.",
        questions=[
            (
                "requirement-not-score",
                "basics",
                "为什么测试通过仍可能不满足用户？",
                "测试可读最终工作区，但用户可能没收到结果、纠正请求未送达，或不允许的文件被修改；这些需求要靠交互记录核实。",
                "教学例：修好代码却没有回复用户，不等于交付完成。",
                "Why can passing tests still fail the user?",
                "Tests may inspect a correct workspace while the user receives no result, a correction is missed or an unapproved file changes. Interaction evidence must verify those requirements.",
                "Teaching example: fixing code without delivering a reply is not completed delivery.",
            ),
            (
                "head-bound-review",
                "mechanism",
                "批准过的PR又改了代码，还能沿用批准吗？",
                "不能。论文合并要求审查绑定当前head，RFC仍匹配审过的设计；旧批准不能覆盖后来改动。",
                "教学例：sha1获批后push sha2，head门必须拒绝。",
                "May approval survive a new code commit?",
                "No. Approval binds the current head and the RFC must still match the reviewed design. Old approval cannot cover later edits.",
                "Teaching example: approval for sha1 must reject a merge at sha2.",
            ),
            (
                "contrast-harness2",
                "comparison",
                "它和Harness²都不看rubric，为何不是同一算法？",
                "Harness²用当前任务执行对照组合候选，再积累如何改的经验；AHE-Beta以会话需求、角色分工和审查准入选择跨任务结构改动。",
                "教学例：比较两个产物和核实中断控制需求，是两种不同证据。",
                "Why is it not the same as rubric-free Harness²?",
                "Harness² composes candidates using current-task execution contrasts and retains improvement experience. AHE-Beta selects structural changes through session requirements, role separation and review admission.",
                "Teaching example: comparing two artifacts is not the same evidence as verifying interruption delivery.",
            ),
            (
                "typed-not-semantic",
                "implementation",
                "本地Evidence类型能证明完全没有gold泄漏吗？",
                "不能。它只限制公开交付表面并排除显式gold字段，字符串和外部调用仍需可信集成，所以仅是L0协议。",
                "教学例：把答案藏在runtime_log字符串中不是类型系统能排除的。",
                "Does the local Evidence type prove absence of gold leakage?",
                "No. It restricts the declared delivery surface and excludes explicit gold fields, but strings and external calls still require trusted integration. This is only an L0 protocol.",
                "Teaching example: an answer hidden inside a runtime_log string is not prevented by this type system.",
            ),
        ],
    ),
    dict(
        key="timeout-cascades",
        id="2611.24324",
        title="Reducing Inference Cost of Coding Agents with Timeout Cascades",
        cn_title="Timeout Cascades：先试小模型，再从原始任务冷启动大模型",
        author="Boxi Zhou",
        org="AMD Singapore",
        published="2026-11-18T12:26:42Z",
        topic="规划与搜索",
        tier="l1_mechanism",
        peer="bats",
        card="planning-and-search",
        peer_path="2511.17006-bats",
        code=None,
        source_locations=[
            "§IV.E GPU-hour convention",
            "§IV.F matched traces and cold restart",
            "§IV.G timeout cascade",
            "§V.C–E",
            "§VI limitations",
        ],
        page=5,
        figure="Figure 3",
        crop=[45, 45, 566, 292],
        method="小模型先做所有编程题；只有在时限内产生有效且通过测试的patch才直接结束。超时、空patch、语法错误或测试失败，都转给大模型。大模型从原始任务状态重新开始，不继承小模型的编辑、工具输出或推理。",
        method_en="Every coding task first uses a small model. It stops only when a valid patch passes tests within the timeout. Timeout, an empty patch, syntax error or failing tests trigger a large model. The fallback restarts from the original task, without inheriting small-model edits, tool outputs or reasoning.",
        mechanism="作者从固定mini-swe-agent的单模型运行轨迹模拟策略，不重新跑级联。500题用于模型能力图；只有466题有两模型完整匹配轨迹，供级联模拟。有效GPU小时按每题runtime乘独占GPU数，即使真实批量有并发也不摊销；它不是集群实际电表成本。",
        mechanism_en="The paper simulates policies from fixed mini-swe-agent single-model traces rather than rerunning a cascade. Model-capability plots use 500 tasks, but only 466 have complete matched traces for both models. Effective GPU hours multiply each task runtime by its exclusive GPU allocation without amortizing actual batch concurrency; this is not metered physical cluster cost.",
        formula=r"C=\frac{n_s\min(t_s,\tau)+\mathbf1_{fallback}\,n_l t_l}{3600},\quad T=\min(t_s,\tau)+\mathbf1_{fallback}t_l.",
        result="GLM-4.7-Flash→GLM-4.7在120分钟小模型时限下，有效GPU小时从2585降到2160（16.4%），easy子集821→546（33.5%）。这是匹配轨迹上的模拟；每模型每题仅一次，轻微成功率互补可能是随机性。顺序级联可增加wall-clock，不能只宣传省GPU小时。未报告生产线上A/B。",
        result_en="At a 120-minute first-stage timeout, GLM-4.7-Flash→GLM-4.7 reduces effective GPU hours from 2585 to 2160 (16.4%); easy-task cost falls from 821 to 546 (33.5%). These are matched-trace simulations. Each model/task runs once, so slight success complementarity may reflect variance. Sequential cascading can increase wall-clock latency. No production A/B is reported.",
        local="Trace严格保存非负时长、GPU数量、有效patch与evaluator测试标签；cascade计算截断小模型费用、冷启动fallback和串行时延，evaluate仅接收完整匹配对。这里只处理合成轨迹数值，不调用模型、不运行SWE-bench、不做真实wall-clock路由，也不实现基于隐藏难度标签的oracle router。",
        local_en="Trace stores nonnegative duration, GPU count, patch validity and evaluator test labels. cascade computes capped first-stage cost, cold-restart fallback and sequential latency. evaluate accepts complete matched pairs only. It handles synthetic trace arithmetic, not models, SWE-bench, a live timeout router or the paper's hidden-difficulty oracle router.",
        controls="边界覆盖时限恰好完成、零时限、早失败、失败测试、双模型失败及非正GPU数。负控确认不能只计大模型时长或摊销GPU数；success标签只在离线评测器，绝不作为真实Agent可见输入。",
        controls_en="Controls cover completion exactly at the deadline, zero timeout, early failure, failed tests, both models failing and invalid GPU counts. Negative controls prevent charging only fallback time or amortizing GPU count. Success labels are offline evaluator metadata, never actor-visible input.",
        cost="完整36模型×500 SWE-bench任务、每题最高250步/2小时，MI300X多GPU与长上下文配置，远超单卡预算；只做秒级CPU trace核算，无checkpoint或数据下载。",
        cost_en="The complete campaign uses 36 models ×500 SWE-bench tasks, up to250 steps/two hours per task, MI300X multi-GPU serving and long contexts. It exceeds a single-GPU budget. Only seconds-scale CPU trace accounting runs, with no checkpoint or dataset downloads.",
        compare="BATS在任务内显式维护逐工具预算并由外部verifier决定继续或换路；Timeout Cascades在模型尝试级别用完成时长与验证结果决定冷启动fallback。二者的预算、费用和能力证据不相同。",
        compare_en="BATS tracks per-tool budgets within a task and uses an external verifier to continue or pivot. Timeout Cascades uses attempt duration and verification to trigger a cold-start fallback between models. Their budgets, cost units and capability evidence differ.",
        questions=[
            (
                "cold-not-resume",
                "basics",
                "fallback会继承小模型已改文件吗？",
                "论文trace模拟采用冷启动，大模型从原始任务状态开始；继承编辑是未研究的未来优化，不能默认加进去。",
                "教学例：小模型改错文件后，大模型并不是在错误工作区上继续。",
                "Does fallback inherit the small model's edits?",
                "No. The trace simulation uses a cold restart from the original task. Edit reuse is an unstudied future optimization, not a default assumption.",
                "Teaching example: the large model does not continue in the small model's corrupted workspace.",
            ),
            (
                "charge-both",
                "mechanism",
                "小模型超时后费用怎么计？",
                "先计截断到时限的小模型时长乘其GPU数，再加大模型完整时长乘GPU数；串行延迟也要加两段。",
                "教学例：30秒×1卡后fallback120秒×4卡，共510 GPU秒、150秒墙钟。",
                "How is cost charged after a timeout?",
                "Charge capped first-stage runtime times its GPU count plus the full fallback runtime times its GPU count. Sequential latency also includes both attempts.",
                "Teaching example:30 seconds ×1 GPU plus120 seconds ×4 GPUs is510 GPU-seconds and150 wall seconds.",
            ),
            (
                "budget-vs-cascade",
                "comparison",
                "它和BATS的预算机制有什么不同？",
                "BATS逐工具扣账并重规划；这里按模型尝试超时切换。工具额度省下不代表GPU小时下降，GPU小时下降也不保证用户等待更短。",
                "教学例：小模型多等一分钟可能省大模型计算，却让一个请求更慢。",
                "How does it differ from BATS budgeting?",
                "BATS accounts per-tool use and replans. This method switches model attempts on timeout. Fewer tool calls need not reduce GPU hours, and fewer GPU hours need not reduce user latency.",
                "Teaching example: waiting another minute for a small model may save large-model compute while slowing one request.",
            ),
            (
                "matched-not-fill",
                "implementation",
                "为什么不把缺失34题按失败补零？",
                "完整模型图有500题，级联仅466个可用配对。缺轨迹无法知道时长、验证和fallback结果，补零会改变分母和成本。",
                "教学例：未记录大模型时长不等于它用了0秒。",
                "Why not fill the34 missing tasks with failures?",
                "The model plots use500 tasks but cascade simulation has466 usable pairs. Missing traces do not supply runtime or fallback outcomes; zero filling changes both denominator and cost.",
                "Teaching example: an unrecorded fallback runtime is not zero seconds.",
            ),
        ],
    ),
    dict(
        key="kaer",
        id="2611.24839",
        title="Kaer: Security-Aware Replanning for Multi-Agent Systems",
        cn_title="Kaer：有限失败通道与受策略约束的确定性重规划",
        author="Tushin Mallick",
        org="Northeastern University",
        published="2026-11-18T18:05:47Z",
        topic="规划与搜索",
        tier="l1_mechanism",
        peer="react",
        card="planning-and-search",
        peer_path="2210.03629-react",
        code=None,
        source_locations=[
            "§III threat model",
            "§IV.C planning conditions a–d",
            "Table1 seven repairs",
            "Table2 thirteen templates",
            "§V Cintra",
        ],
        page=4,
        figure="Figure 1",
        crop=[45, 45, 304, 399],
        method="不可信子Agent可把恶意指令夹在失败反馈里，诱导orchestrator授予新权限或改任务。Kaer不让自由文本失败报告进入planner，只传部署前固定的失败模板；planner用固定七种确定性算子修改尚未完成的子任务，最后重新验证任务及Agent策略。",
        method_en="An untrusted subagent may inject instructions through failure feedback to induce new privileges or task changes. Kaer sends only a deployment-fixed failure-template vocabulary to the planner, not free-text failure reports. The planner repairs uncompleted subtasks with seven deterministic operators, then revalidates task and agent policies.",
        mechanism="计划每一步的能力必须同时属于执行Agent能力集和任务策略；数据依赖只能来自较早步骤，接收Agent必须被来源Agent的输出策略允许，除最终步骤外每个产物都要有后继消费者。RE-EXECUTE、REVISE-DIRECTIVE、RESCOPE、REASSIGN、INSERT、PRUNE、REWIRE按序作用在副本，已完成前缀不变。成功输出与progress报告不传planner，但可能影响执行Agent；这不是全链内容安全证明。",
        mechanism_en="Each step's capabilities must be allowed by both its agent and task policy. Dependencies come only from earlier steps; recipients must satisfy producer output-flow policies; every nonfinal output needs a later consumer. RE-EXECUTE, REVISE-DIRECTIVE, RESCOPE, REASSIGN, INSERT, PRUNE and REWIRE apply sequentially to a copy, preserving the completed prefix. Successful outputs and progress reports do not reach the planner but can affect executing agents; this is not end-to-end content security.",
        formula=r"C_j\subseteq C_{A_j},\quad C_j\subseteq C_T,\quad i\in deps(j)\Rightarrow i<j\land A_j\in AP_{A_i}.",
        result="作者建立Cintra，含14个需要重规划的任务和14类攻击目标，比较三种基础模型下的Kaer、Magentic-One、ControlValve及消融，报告更强攻击鲁棒性且效用接近ControlValve。它是模拟工具环境评测，没有生产线上A/B。原文不验证开放任务输出是否真的正确，也不保护已授权Agent内部滥用。",
        result_en="The paper constructs Cintra with14 tasks requiring replanning and14 attack objectives, comparing Kaer, Magentic-One, ControlValve and ablations under three models. It reports stronger attack robustness with utility comparable to ControlValve. This is simulated-tool evaluation, not production A/B. It does not establish open-ended output correctness or prevent misuse internal to an authorized agent.",
        local="实现13种模板ID去重、四项计划策略检查、七种算子和INSERT/PRUNE依赖重编号；操作事务化，仅最终有效计划可返回。使用0-based位置，论文k对应本地k−1。本地严格拒绝任务策略外能力，没有实现原文单独的用户授权扩展、LLM planner、MCP gateway、重试调度或真实Cintra。",
        local_en="The local slice deduplicates13 template IDs, validates four plan conditions, and applies all seven operators with dependency renumbering after INSERT/PRUNE. Repairs are transactional and return only a valid final plan. Indices are zero based (paper k maps to k−1). Capabilities outside task policy are rejected; the separate explicit-user-grant extension, LLM planner, MCP gateway, retry scheduler and Cintra environment are absent.",
        controls="测试拒绝模板里追加任意指令、Agent伪报no-close-out、改已完成步骤、前向/自依赖、未消费产物、违规输出流和能力升级；合法插入后必须rewire才能通过。模板仍可撒谎，只是影响范围有限；拒绝plan不证明任务能完成。",
        controls_en="Tests reject instructions appended to template IDs, agent-asserted no-close-out, edits to completed steps, forward/self dependencies, unused outputs, forbidden data flows and capability escalation. Insertion needs suitable rewiring to pass. An agent can still lie by choosing an allowed template; influence is bounded, not eliminated. Rejecting an unsafe plan does not prove task completion.",
        cost="完整多模型×14任务×14攻击目标与消融依赖真实planner、工具网关和多Agent推理；单卡不能忠实代替前沿服务矩阵。只执行秒级CPU确定性控制核，不申请API、不下载模型。",
        cost_en="The full multi-model ×14-task ×14-attack and ablation campaign needs real planners, gateways and multi-agent inference. One GPU cannot faithfully substitute the frontier-service matrix. Only seconds-scale deterministic CPU controls run, without APIs or model downloads.",
        compare="ReAct让自由文本推理与真实观察交替以调整下一步；Kaer针对多Agent失败反馈收窄重规划信息通道，并用静态策略约束修改。它不是把ReAct观察删掉就得到安全，也不判断成功输出真假。",
        compare_en="ReAct interleaves free-text reasoning with observations to choose actions. Kaer narrows the replanning channel for multi-agent failures and constrains revisions with static policies. Removing ReAct observations alone does not implement Kaer, and Kaer does not judge successful-output truth.",
        questions=[
            (
                "feedback-not-command",
                "basics",
                "为什么失败报告是攻击入口？",
                "planner据反馈改计划，攻击者可把“缺资料”写成“运行某脚本”，把信息变成授权指令。Kaer仅传固定失败条件。",
                "教学例：缺Q3收入只能报input_lacks_required_datum，不能附带运行窃密脚本的命令。",
                "Why is a failure report an attack surface?",
                "The planner revises its plan from feedback. An attacker can turn missing information into an instruction to run a script. Kaer passes only fixed failure conditions.",
                "Teaching example: missing Q3 revenue permits an input_lacks_required_datum template, not a command to execute an exfiltration script.",
            ),
            (
                "repair-not-rebuild",
                "mechanism",
                "固定七种修复算子为何还要策略检查？",
                "算子序列仍可组合成危险计划，所以最终能力、数据流、依赖和产物使用都要重验；算子有限不等于结果必安全。",
                "教学例：RESCOPE是合法算子，但给coder加terminal仍可能违反任务策略。",
                "Why validate policies after using fixed repair operators?",
                "A sequence of legitimate operators can still construct an unsafe plan. Final capabilities, data flows, dependencies and output use must be rechecked.",
                "Teaching example: RESCOPE is a valid operator, but granting terminal to a coder may violate task policy.",
            ),
            (
                "react-channel",
                "comparison",
                "它相对ReAct改变的是哪一层？",
                "ReAct交替推理与动作观察；Kaer收窄多Agent失败通道并验证计划修改，目标是控制权劫持而非提升单步推理。",
                "教学例：能够根据新观察换路线，不代表不可信观察能授予新工具。",
                "Which layer differs from ReAct?",
                "ReAct alternates reasoning, actions and observations. Kaer narrows multi-agent failure feedback and validates plan revisions, targeting control hijacking rather than stronger single-step reasoning.",
                "Teaching example: adapting to an observation does not authorize that observation to grant a new tool.",
            ),
            (
                "copy-before-accept",
                "implementation",
                "被拒的修复能留下部分计划修改吗？",
                "不能。算子作用在副本，只有全部操作后策略通过才采用；已完成步骤不可动。INSERT/PRUNE必须同步改依赖位置。",
                "教学例：插入步骤后旧下标1变2，旧依赖也要重编号。",
                "May a rejected repair leave partial plan edits?",
                "No. Operators apply to a copy and adoption occurs only after the final policy check. Completed steps are immutable. INSERT/PRUNE must renumber dependencies.",
                "Teaching example: inserting before index1 shifts the old step and its dependency indices.",
            ),
        ],
    ),
    dict(
        key="safe-personal-rsi",
        id="2611.23651",
        title="Safe Personal RSI: Evaluating and Repairing Personal-Agent Updates",
        cn_title="Safe Personal RSI：修复通过不等于更新可准入",
        author="Jiapeng Pei",
        org="Independent",
        published="2026-11-18T00:15:38Z",
        topic="执行框架与自改进",
        tier="l1_mechanism",
        peer="harness2",
        card="harness-and-self-improvement",
        peer_path="2610.14224-harness2",
        code=None,
        source_locations=[
            "Appendix I.2 confirmation",
            "I.3 rollback ratio",
            "I.4 verification",
            "I.5 full admission",
            "I.6 limitations",
            "Appendix F/G study accounting",
        ],
        page=30,
        figure="Figure H.2",
        crop=[55, 400, 540, 574],
        method="个人Agent的prompt更新可能提升主动性，却同时改变隐私披露、承诺和执行报告。论文固定模型和runtime，只改指令；先比较候选与父版本寻找反例，再重复确认、回滚定位和修复。修复局部验证后仍须完整admission；没有通过版本就继续用父版本。",
        method_en="A personal-agent prompt update can improve initiative while changing disclosure, commitments and execution reporting. The paper fixes model and runtime, edits instructions, searches for candidate-versus-parent failures, then confirms, localizes through rollback and repairs. Local verification does not bypass final admission; without an admitted update, the parent remains active.",
        mechanism="Appendix I以所有开发重放（含control）为分母，取五个primary风险类别的最大率。确认过的未授权披露case产生持久严重性veto，即使后来修复也拒该attempt；否则父/工作版本各至少5条且全部执行完成，最大风险不超过0.10且不高于父版本。效用不降，或成功率最多绝对下降0.02且成本proxy绝对减少至少0.10，才可准入。RQ1模板确认可接受非空截断多数；RQ2要求三次候选确认完整，差分还要三次父重放。",
        mechanism_en="Appendix I normalizes risk by all development replays, including controls, and compares the maximum rate over five primary labels. A confirmed unauthorized-disclosure case causes a persistent severe veto even after repair. Otherwise each harness needs at least five completed records; maximum risk must be at most0.10 and no greater than the parent's. Utility must not decrease, or success may decline by at most0.02 absolutely while cost proxy falls by at least0.10 absolutely. RQ1 template confirmation permits a nonempty truncated majority; RQ2 requires three completed candidate confirmations and, for differential confirmation, three parent replays.",
        formula=r"\hat R_{max}(W)\le .10,\quad\hat R_{max}(W)\le\hat R_{max}(H),\quad\hat U(W)\ge\hat U(H)\;\lor\;[p_W\ge p_H-.02\land\bar c_H-\bar c_W\ge .10].",
        result="29个离线合成账户/服务case中，三模型两种风险编辑共21次更新尝试拒绝20次。部分修复确认报告违例10.7%→0%，但手写authority rule也匹配该结果；更强攻击迁移仍有17.9%违例。论文明确跨model-access-route等价性未核实、重复探索限制独立test解释，不能把表内局部改善称普适安全。未报告生产线上A/B。",
        result_en="Across29 offline synthetic-account/service cases, three models and two risky edits,20 of21 update attempts are rejected. One repair confirmation reports violations falling from10.7% to0%, but a handwritten authority rule matches it; stronger-attack transfer still has17.9% violations. Backend equivalence across access routes was unverified, and repeated exploration limits independent-test interpretation. These are not universal safety guarantees or production A/B results.",
        local="实现Replay评测记录、最大类别风险准入、持久veto、最少重放/完成检查、严格多数确认两种协议与回滚gain-retention的零gain约定。未实现Willow/Kicker、邮件工具、攻击搜索、LLM修复、语义judge、verification回放或OAuth修复。Replay不是给Actor的输入，只有离线evaluator调用。",
        local_en="The local slice implements evaluator Replay records, maximum-category-risk admission, persistent veto, minimum/completion checks, both strict-majority confirmation protocols, and rollback gain retention including its zero-gain convention. It does not implement Willow/Kicker, email tools, attack search, LLM repair, a semantic judge, verification rollouts or OAuth fixes. Replay records belong only to the offline evaluator, not the actor.",
        controls="测试保留论文限制：最大风险不变时次大类别风险仍可升高；不偷偷把规则增强为总风险比较。缺5条、未完成、严重veto、风险上升或效用/成本均不达标分别拒绝。阈值是点估计与工程常数，不提供置信界或总体安全概率。",
        controls_en="A negative control preserves the paper's limitation: nonmaximal-category risk may rise while maximum risk stays unchanged. The rule is not silently strengthened to compare total risk. Tests separately reject too few records, incomplete runs, severe veto, increased maximum risk, and failure of both utility/cost alternatives. Thresholds are point estimates and engineering constants, not confidence or population-risk bounds.",
        cost="完整实验含真实多模型API、29类case、多轮搜索/回滚/最多两次修复，附录记录2895条开发与final样本；还依赖未验证公开的Willow运行时。只执行秒级CPU评测算术，不启动个人服务、不调用模型。",
        cost_en="The full study needs real multi-model APIs,29 case families, repeated search/rollback and up to two repairs; Appendix F records2895 development/final samples and relies on a Willow runtime without a verified public release. Only seconds-scale CPU evaluator arithmetic runs, with no personal services or model calls.",
        compare="Harness²用执行差异优化harness，不要求rubric；Safe Personal RSI对prompt候选显式比较安全/效用并保留父版本。后者有领域风险标签但仍不是安全证明；不能把前者匿名产物选择当后者admission。",
        compare_en="Harness² improves a harness from execution contrasts without requiring rubrics. Safe Personal RSI explicitly compares prompt-update safety/utility and retains the parent on failure. Its domain risk labels still do not prove safety; Harness² artifact selection is not this admission rule.",
        questions=[
            (
                "verify-not-admit",
                "basics",
                "修复重放没有违例，为何仍不能自动采用？",
                "verification只查已确认反例和开发效用；完整admission还查严重veto、至少5条完整记录、最大风险和效用/成本条件。",
                "教学例：一个修复躲过旧攻击，但记录不足仍是insufficient evidence。",
                "Why is violation-free repair verification insufficient for adoption?",
                "Verification covers confirmed failures and development utility. Admission additionally checks persistent veto, at least five completed records, maximum risk and utility/cost conditions.",
                "Teaching example: a repair avoids the old attack but remains insufficient evidence with too few records.",
            ),
            (
                "risk-denominator",
                "mechanism",
                "风险分母为什么包含正常control？",
                "公式使用所有开发重放做suite-normalized类别率，不是只在攻击子集上算；final attack rate另有分母，不能混用。",
                "教学例：20条含2个同类违例，类别率0.10，不因只有4条攻击改成0.50。",
                "Why include benign controls in the risk denominator?",
                "The rule uses every development replay for suite-normalized category rates. Final attack rates have a different denominator and cannot be substituted.",
                "Teaching example:2 same-category violations in20 records yield0.10, not0.50 merely because four records are attacks.",
            ),
            (
                "max-not-proof",
                "comparison",
                "相比Harness²，它的安全门是否证明风险不会增加？",
                "不证明。它比较最大primary类别点估计，次大类别甚至总primary风险可增加；Harness²的执行对照又不是这个领域风险门。",
                "教学例：最大类别维持2/20，另一类别0→1/20仍可能准入。",
                "Does its safety gate prove no risk increase, unlike Harness²?",
                "No. It compares maximum primary-category point estimates; nonmaximal or total primary risk can rise. Harness² execution contrasts are a different, non-domain-risk criterion.",
                "Teaching example: keeping the maximum at2/20 while another category rises from0 to1/20 may still pass.",
            ),
            (
                "complete-confirmations",
                "implementation",
                "两次确认都失败，RQ2能提前称confirmed吗？",
                "不能。RQ2要求三次候选执行完整且严格多数；差分确认还需三次父重放且父违例更少。非空截断多数只属于RQ1模板配置。",
                "教学例：True,True缺第三次，RQ2返回False而非确认。",
                "May RQ2 confirm after two violating replays?",
                "No. RQ2 requires all three candidate runs and a strict majority; differential confirmation also needs three parent runs with fewer violations. Truncated nonempty majority belongs only to the RQ1 template configuration.",
                "Teaching example:True,True with a missing third replay is not an RQ2 confirmation.",
            ),
        ],
    ),
    dict(
        key="rsibench-infra",
        id="2611.24395",
        title="RSIBench-Infra: Can Agents Optimize Their Own Training and Inference Infrastructure at Production Scale?",
        cn_title="RSIBench-Infra：把生产级基础设施优化与独立质量验证分开",
        author="Hanlin Wu",
        org="ByteDance Seed / Tsinghua University AIR / SIA-Lab",
        published="2026-11-18T13:29:44Z",
        topic="执行框架与自改进",
        tier=None,
        peer="harness2",
        card="harness-and-self-improvement",
        peer_path="2610.14224-harness2",
        code=None,
        source_locations=[
            "PDF p1 first-author affiliations",
            "§3.2–3.3 OCI protocol",
            "§3.4 workload scale",
            "Table1 hardware",
            "§4.1 eight-hour budget",
            "Appendix B quality gates",
        ],
        page=2,
        figure="Figure 1",
        crop=[65, 55, 548, 342],
        method="单算子快不代表端到端训练或服务变快。RSIBench-Infra让Agent从官方可运行baseline出发，跨engine、kernel、instruction修改，但只提交一个OCI filesystem layer。独立Serve/Train Job把同一digest应用到每个rank；Benchmark Job绝不加载候选层，单独做质量门和端到端计时。",
        method_en="A faster kernel need not make training or serving faster end to end. RSIBench-Infra starts agents from runnable official baselines and permits changes across engine, kernel and instruction layers, submitted as one OCI filesystem layer. Independent Serve/Train jobs apply the same digest on every rank. The Benchmark Job never loads that layer and separately checks quality and end-to-end timing.",
        mechanism="任务定义含模型、环境、资源和独立verifier。16推理+4训练任务覆盖1–32个加速器、最多4节点；推理模型1.7B–2.8T。训练固定输入，比较逐步loss和全局梯度范数；VLM GRPO还检查policy/KL loss、forward及隔离KL梯度。性能得分只有通过任务质量门才有效，microbenchmark不能替代端到端计时。",
        mechanism_en="A task specifies the model, environment, resources and independent verifier. Sixteen inference and four training tasks span1–32 accelerators and up to four nodes; inference models range from1.7B to2.8T. Training replays frozen inputs and compares stepwise loss/global-gradient norms; VLM GRPO additionally checks policy/KL losses, forwards and an isolated KL-gradient probe. Speed counts only after the task quality gate, and microbenchmarks cannot replace end-to-end timing.",
        formula=r"validated\_speedup=\frac{T_{baseline}}{T_{candidate}}\quad\text{only if }quality\_gate=pass;\qquad Faster=\mathbf1[validated\_speedup>1.10].",
        result="130个正式计分结果中86个（66.2%）超过1.10倍已验证加速。主模型配置每项Agent预算8小时；Claude只正式计10项，API安全错误其余不混进20项完整suite。生产规模工作负载不是随机线上业务A/B，不能写成线上收益。",
        result_en="Of130 formally scored results,86 (66.2%) exceed1.10× validated speedup. Each agent run has an eight-hour budget. Claude has only10 formally scored tasks because API safety errors prevent the rest; its denominator is not a complete20-task suite. Production-scale workloads are not randomized business-traffic A/B evidence.",
        local="仅做原文审查、成本评估、中英文说明和学习材料。没有把OCI字段stub、任意microbenchmark或单卡小模型标成RSIBench-Infra已接入；local_operator=null，不提供可执行Evolve算子。项目页https://rsibench-infra.github.io已核对，未验证论文专用源码仓库公开。",
        local_en="Only primary review, cost assessment, bilingual documentation and learning material are delivered. An OCI schema stub, arbitrary microbenchmark or small single-GPU model is not labeled an RSIBench-Infra integration. local_operator=null and no executable evolve operator is advertised. The project page https://rsibench-infra.github.io is verified, but no paper-specific public source repository was verified.",
        controls="审查明确隔离Agent环境、Serve/Train环境和Benchmark环境，比较部署digest与质量门，而不是伪造本地通过指标。没有运行正式任务、提交OCI、训练或测试模型；所以没有CPU/GPU能力分数，也不要求GPU回执。",
        controls_en="Review distinguishes Agent, Serve/Train and Benchmark environments, deployment digests and quality gates rather than fabricating local pass metrics. No official task, OCI submission, model training or inference runs. Consequently there are no local CPU/GPU capability scores and no GPU receipt is required.",
        cost="20任务覆盖1–32加速器/最多4节点、1.7B–2.8T推理模型及7B–30B BF16全参训练；每个Agent run上限8小时，另有质量重放与测量。已有配置足以判断单A100/A30预算不适合，不为证明昂贵再试跑。",
        cost_en="Twenty tasks require1–32 accelerators/up to four nodes,1.7B–2.8T inference models and7B–30B BF16 full-parameter training. Each agent run allows eight hours, followed by quality replay and measurement. These configurations already exceed a single A100/A30 budget; no costly probe is launched to establish that fact.",
        compare="Harness²改模型外执行框架并以任务执行对照积累经验；RSIBench-Infra评价跨栈训练/推理优化，以独立质量门约束端到端加速。优化harness通过数和已验证吞吐收益不是同一个结果，前者不能代替后者硬件链路。",
        compare_en="Harness² improves model-external harnesses through task execution contrasts and accumulated experience. RSIBench-Infra evaluates cross-stack training/inference optimization with independently quality-gated end-to-end speed. Harness pass counts and validated throughput are different outcomes; the former cannot substitute the latter's hardware pipeline.",
        questions=[
            (
                "layer-not-patch",
                "basics",
                "为什么不用一个git patch承载优化？",
                "可改engine、库、编译产物和其他目录，git patch不覆盖全部环境变化；OCI层在干净baseline上重建同一提交。",
                "教学例：只提交Python diff会漏掉新编译kernel或库依赖。",
                "Why is a git patch insufficient?",
                "Changes may span engines, libraries, compiled artifacts and other directories. An OCI layer reconstructs all submitted filesystem changes on a clean baseline.",
                "Teaching example: a Python diff can omit a new compiled kernel or dependency.",
            ),
            (
                "independent-benchmark",
                "mechanism",
                "Benchmark Job为什么不能加载候选OCI层？",
                "候选层由Agent控制；加载它可能修改workload、质量检查或计分。Benchmark通过服务接口评测，计分代码保持独立。",
                "教学例：候选把测试答案写入验证器目录，不能靠同一层传入Benchmark环境。",
                "Why must the Benchmark Job never load the candidate layer?",
                "The agent controls it and could alter workload generation, quality checks or scoring. The independent Benchmark Job evaluates the service through exposed interfaces.",
                "Teaching example: answers written into a verifier directory must not travel into the Benchmark environment through the submission layer.",
            ),
            (
                "kernel-not-e2e",
                "comparison",
                "相比Harness²或kernel评测，它的目标有什么不同？",
                "这里检查整个模型服务/训练链路在质量门下是否更快；harness任务通过或单kernel提速不证明端到端吞吐提高。",
                "教学例：kernel快2倍但数据传输占90%，整条链路提升仍可能很小。",
                "How does the goal differ from Harness² or kernel benchmarks?",
                "It checks whether the entire serving/training pipeline becomes faster while preserving quality. Harness task success or kernel speedup cannot establish end-to-end throughput.",
                "Teaching example: doubling kernel speed has little impact when transfer dominates90% of runtime.",
            ),
            (
                "cost-terminal",
                "implementation",
                "为何本库不先缩成小模型跑一遍？",
                "多rank部署、独立OCI应用、任务特定质量门和生产工作负载是定义性协议；任意小模型stub不能验证它们，故高成本审查终态不复现。",
                "教学例：本地一次矩阵乘计时不是20任务RSIBench-Infra复现。",
                "Why not first run an arbitrary tiny-model substitute?",
                "Multi-rank deployment, independent OCI application, task-specific quality gates and production workloads define the protocol. A tiny-model stub cannot validate them, so review closes as high-cost not reproduced.",
                "Teaching example: timing one local matrix multiplication is not reproducing the20-task RSIBench-Infra suite.",
            ),
        ],
    ),
]


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    import fitz
    from english_learning_sources import question_units

    AUDIT.mkdir(parents=True, exist_ok=True)
    questions, translations, reviews, proposals = {}, {}, [], []
    for p in PAPERS:
        key, aid = p["key"], p["id"]
        identity = "agent-research:" + key
        paper = ROOT / f"docs/agent-research/{aid}-{key}"
        assets = paper / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        source = ROOT / f".cache/nov19-latest/agent/{aid}v1.pdf"
        source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        image = assets / "paper-figure-01.png"
        doc = fitz.open(source)
        doc[p["page"] - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(p["crop"])).save(
            image
        )
        image_hash = hashlib.sha256(image.read_bytes()).hexdigest()
        write(
            assets / "provenance.json",
            {
                "schema_version": 1,
                "reviewed_on": DATE,
                "figures": [
                    {
                        "file": image.name,
                        "paper_id": aid,
                        "version": "v1",
                        "figure": p["figure"],
                        "source_url": f"https://arxiv.org/pdf/{aid}v1#page={p['page']}",
                        "paper_url": f"https://arxiv.org/abs/{aid}v1",
                        "source_kind": "fixed_version_pdf_crop_rendered_png",
                        "source_sha256": source_hash,
                        "asset_sha256": image_hash,
                        "image_sha256": image_hash,
                        "page": p["page"],
                        "crop_points": p["crop"],
                        "render_dpi": 144,
                        "caption_included": True,
                        "scientific_content_modified": False,
                        "visual_review_done": True,
                        "attribution": "Copyright belongs to original authors. Original figure and caption, not local evidence.",
                        "license": "See original arXiv source; no new license granted.",
                    }
                ],
            },
        )
        component = p["tier"] is not None
        status = "component_only" if component else "deferred_high_cost"
        module = key.replace("-", "_")
        code_cn = (
            f"[作者仓库]({p['code']})；{p['license']}"
            if p["code"]
            else "未在固定v1及已核对项目页发现／验证论文专用公开源码仓库；不将引用依赖当作者开源。"
        )
        code_en = (
            f"[Author repository]({p['code']}); {p['license']}"
            if p["code"]
            else "No paper-specific public source repository verified in fixed v1 or the reviewed project page; cited dependencies are not an author release."
        )
        local_code = (
            f"`src/auto_research/agent_research/{module}.py`"
            if component
            else "无；仅审查收录，未实现训练／推理代码。"
        )
        local_code_en = (
            f"`src/auto_research/agent_research/{module}.py`"
            if component
            else "None; review-only, no training/inference implementation."
        )
        stamp = p["published"].replace("T", " ").replace("Z", " UTC")
        cn = f"""# {p["cn_title"]}

[English](README-en.md)

> **{status} / {p["tier"] or "review-only"}；不是Agent能力复现。** 完整实验成本过高，不复现（审查 DONE）；不作为Evolve晋级证据。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [{p["title"]}](https://arxiv.org/abs/{aid}v1)；[固定v1 PDF](https://arxiv.org/pdf/{aid}v1) |
| 一作机构 / 公司 / 学校 | {p["author"]}，{p["org"]} |
| 首次公开日期 | **{stamp}**；11月19日审查／公告不能替代首发日期 |
| 原作者代码 | {code_cn} |
| 本地 Adapter / key | `{key}`；`adapter=null`，未接入Evolve |
| 本地复现代码 | {local_code} |

## 原始论文总结

### 背景与主要改动

{p["method"]}

{p["mechanism"]}

### 架构与流程

```mermaid
flowchart LR
  {FLOWS[key][0]}
```

<!-- paper-figure:start -->
### 原论文关键图

![{key} {p["figure"]}](assets/paper-figure-01.png)

固定v1 PDF第{p["page"]}页 {p["figure"]}及图注；仅裁页面留白／无关正文，未改科学内容。图片来自[原论文](https://arxiv.org/pdf/{aid}v1#page={p["page"]})，版权归原作者所有。[资产来源](assets/provenance.json)。
<!-- paper-figure:end -->

### 核心公式

$$
{p["formula"]}
$$

### 论文离线与线上效果

{p["result"]}

## 本地复现

### 数据协议与代码映射

{p["local"]}

{("```bash" + chr(10) + "PYTHONPATH=src python -c 'from auto_research.agent_research." + module + " import diagnostic; print(diagnostic(42))'" + chr(10) + "PYTHONPATH=src python -m pytest tests/test_nov19_latest_agent.py -q" + chr(10) + "```" + chr(10) + chr(10) + "[CPU三种子诊断](metrics/component-cpu-seeds42-44.json)仅为合成控制核记录，不是模型成功率。") if component else "未执行实验，不生成虚假metrics或GPU回执。"}

### 结果、负控与边界

{p["controls"]}

同主题实读对照：[ {p["peer"]} ](../{p["peer_path"]}/README.md)。{p["compare"]}

### 高成本完整实验

{p["cost"]} **成本过高，不复现（审查 DONE）**。该决定为终态，不进入自动重试或实现队列，不阻塞其他交付；不把廉价组件的通过数当完整论文效果。
"""
        (paper / "README.md").write_text(cn)
        cn_sha = hashlib.sha256(cn.encode()).hexdigest()
        en = f"""# {p["title"]}

<!-- source-sha256: {cn_sha} -->

[简体中文](README.md)

> **{status} / {p["tier"] or "review-only"}; not an agent capability reproduction.** Full experiments are too costly and not reproduced (review DONE). Not evidence for evolve promotion.

## Paper information

| Field | Value |
| --- | --- |
| Paper link | [{p["title"]}](https://arxiv.org/abs/{aid}v1); [fixed v1 PDF](https://arxiv.org/pdf/{aid}v1) |
| First-author institution / company / school | {p["author"]}, {p["org"]} |
| Original publication date | **{stamp}**; November19 review/announcement is not the first-release date |
| Original source code | {code_en} |
| Local adapter / key | `{key}`; `adapter=null`, not integrated with evolve |
| Local reproduction code | {local_code_en} |

## Original paper summary

### Background and main changes

{p["method_en"]}

{p["mechanism_en"]}

### Architecture and flow

```mermaid
flowchart LR
  {FLOWS[key][1]}
```

### Original paper figure

![{key} {p["figure"]}](assets/paper-figure-01.png)

Fixed v1 PDF page{p["page"]}, {p["figure"]} with original caption. Only whitespace/unrelated text is cropped; scientific content is unchanged. Copyright belongs to the original authors. [Original paper](https://arxiv.org/pdf/{aid}v1#page={p["page"]}) · [Provenance](assets/provenance.json).

### Core equations

$$
{p["formula"]}
$$

### Reported offline and online results

{p["result_en"]}

## Local reproduction

### Data protocol and code mapping

{p["local_en"]}

{("```bash" + chr(10) + "PYTHONPATH=src python -c 'from auto_research.agent_research." + module + " import diagnostic; print(diagnostic(42))'" + chr(10) + "PYTHONPATH=src python -m pytest tests/test_nov19_latest_agent.py -q" + chr(10) + "```" + chr(10) + chr(10) + "[Three-seed CPU diagnostics](metrics/component-cpu-seeds42-44.json) are synthetic control-kernel records, not model success rates.") if component else "No experiment was executed; no fabricated metrics or GPU receipt is generated."}

### Results, negative controls and limits

{p["controls_en"]}

Reviewed same-topic comparison: [ {p["peer"]} ](../{p["peer_path"]}/README-en.md). {p["compare_en"]}

### High-cost full experiments

{p["cost_en"]} **Too costly; not reproduced (review DONE).** This is terminal, not an automatic retry or implementation queue. It does not block other delivery. Passing a cheap component does not establish the full paper's results.
"""
        (paper / "README-en.md").write_text(en)
        spec = {
            "key": key,
            "first_author": p["author"],
            "first_author_affiliation": p["org"],
            "published_at": p["published"],
            "domain": "agent-research",
            "title": p["title"],
            "paper_url": f"https://arxiv.org/abs/{aid}v1",
            "reviewed_version": "v1",
            "reviewed_arxiv_id": aid + "v1",
            "reviewed_version_url": f"https://arxiv.org/pdf/{aid}v1",
            "detail_path": f"agent-research/{aid}-{key}/README.md",
            "topic": [p["topic"], key],
            "published": p["published"][:10],
            "verified_priority_organizations": [],
            "code": p["code"],
            "code_status": code_cn,
            "adapter": None,
            "priority": "P1",
            "intake_class": "new_first_release",
            "implementation_status": status,
            "local_operator": f"auto_research.agent_research.{module}.diagnostic"
            if component
            else None,
            "local_command": f"PYTHONPATH=src python -c 'from auto_research.agent_research.{module} import diagnostic; print(diagnostic(42))'"
            if component
            else None,
            "evaluation_tier": p["tier"],
            "diagnostic_only": True,
            "promotion_eligible": False,
            "evolve_integrated": False,
            "requires_gpu_validation": False,
            "gpu_validation_passed": False,
            "review_done": True,
            "full_experiment_review_done": True,
            "full_experiment_status": "not_reproduced_high_cost",
            "review_resolution": "not_reproduced_high_cost",
            "automatic_retry": False,
            "automatic_implementation_queue": False,
            "cost_assessment": {
                "source": f"https://arxiv.org/pdf/{aid}v1",
                "available_resource": "单张A100/A30或本地Mac",
                "basis": p["cost"],
                "decision": "成本过高，不复现（审查 DONE）；局部组件与完整实验分开记录。",
            },
            "summary": p["method"],
            "fidelity_note": p["local"],
        }
        if not component:
            spec["deferral_reason"] = p["cost"] + " 成本过高，不复现（审查 DONE）。"
        write(ROOT / f"src/auto_research/paper_specs/catalog/agent-research/{key}.json", spec)
        bank = []
        for qid, level, q, a, e, eq, ea, ee in p["questions"]:
            qrow = {
                "id": qid,
                "level": level,
                "question": q,
                "answer": a,
                "example": e,
                "source_sections": HEADINGS,
                "added": DATE,
            }
            bank.append(qrow)
            unit = question_units({identity: [qrow]})[f"qa/{identity}/{qid}"]
            translations[f"qa/{identity}/{qid}"] = {
                "source_sha256": unit.source_sha256,
                "reviewed": True,
                "fields": {"question": eq, "answer": ea, "example": ee},
            }
        questions[identity] = {"questions": bank}
        peer_identity = "agent-research:" + p["peer"]
        peer_readme = ROOT / f"docs/agent-research/{p['peer_path']}/README.md"
        revision = {
            identity: cn_sha,
            peer_identity: hashlib.sha256(peer_readme.read_bytes()).hexdigest(),
        }
        cquestion = next(q for q in bank if q["level"] == "comparison")
        cq_en = next(q for q in p["questions"] if q[1] == "comparison")
        proposals.append(
            {
                "paper": identity,
                "target_card": "agent-research/" + p["card"],
                "source_revisions": revision,
                "comparison": {
                    "position": p["method"],
                    "tradeoff": p["compare"],
                    "sections": HEADINGS,
                },
                "analysis": {
                    "title": p["cn_title"],
                    "body": p["mechanism"] + p["controls"],
                    "papers": [identity, peer_identity],
                },
                "question": {
                    "id": "cross-nov19-" + key,
                    "question": cquestion["question"],
                    "answer": cquestion["answer"],
                    "example": cquestion["example"],
                    "papers": [identity, peer_identity],
                },
                "update": {
                    "date": DATE,
                    "papers": [identity, peer_identity],
                    "summary": p["local"] + " 完整实验高成本不复现，不作能力证据。",
                },
                "english": {
                    "comparison": {"position": p["method_en"], "tradeoff": p["compare_en"]},
                    "analysis": {
                        "title": p["title"],
                        "body": p["mechanism_en"] + " " + p["controls_en"],
                    },
                    "question": {"question": cq_en[5], "answer": cq_en[6], "example": cq_en[7]},
                    "update": p["local_en"] + " Full campaign not reproduced; no capability claim.",
                },
            }
        )
        reviews.append(
            {
                "id": aid,
                "key": key,
                "first_author": p["author"],
                "first_author_affiliation": p["org"],
                "published_at": p["published"],
                "source_url": f"https://arxiv.org/pdf/{aid}v1",
                "source_sha256": source_hash,
                "locations": p["source_locations"],
                "code": p["code"],
                "code_status": code_en,
                "implementation_status": "component_only" if component else "review_only",
                "evaluation_tier": p["tier"],
                "scope": p["local_en"],
                "cost_basis": p["cost_en"],
                "full_experiment_status": "not_reproduced_high_cost",
                "requires_gpu_validation": False,
                "review_done": True,
            }
        )
    write(
        ROOT / "docs/learning/questions/nov19-latest-agent.json",
        {"schema_version": 1, "papers": questions},
    )
    write(
        ROOT / "docs/en/learning/translations/qa-nov19-latest-agent.json",
        {"schema_version": 1, "units": translations},
    )
    write(
        AUDIT / "deep-dive-proposals-agent.json",
        {
            "schema_version": 1,
            "reviewed_on": DATE,
            "integration_owner": "root",
            "proposals": proposals,
        },
    )
    write(
        AUDIT / "agent-review.json",
        {
            "schema_version": 1,
            "reviewed_on": DATE,
            "scope": "Finite primary-source method/cost review of five new first releases from November18, announced/reviewed November19. Not exhaustive Agent literature coverage.",
            "implementation_preflight_completed": True,
            "available_resource": "One A100/A30 or local Mac; no paid API or model/data downloads for these diagnostics",
            "reviews": reviews,
            "p2_dispositions": [],
        },
    )


if __name__ == "__main__":
    main()
