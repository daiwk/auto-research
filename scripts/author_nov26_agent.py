"""Author-owned Nov26 proposal serialization; no shared-bank integration.

Prose below was reviewed against fixed full texts and the named peer READMEs.
Rerun only after reviewing any changed Chinese source; hashes are not translation.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov26-latest"
DATE = "2026-11-26"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


DATA = [
    dict(key="home", domain="agent-research", id="2611.34624", time="16:11:53",
         title="HoMe: Toward Practical Harness Optimization of Memory Systems for AI Assistants",
         author="Yifei Xu", affiliation="Shanghai Jiao Tong University",
         organizations=["Shanghai Jiao Tong University", "Alibaba Group", "Peking University"],
         code="https://github.com/agentscope-ai/ReMe/tree/7b2317584f23ba63a21cb154b961eb3dcc788e0e/plugins/home",
         code_status="作者公开ReMe的HoMe插件；已核查固定树7b2317584f23ba63a21cb154b961eb3dcc788e0e中的sampling.py与evaluation/reuse.py。",
         license="Apache-2.0", tier="l1_mechanism", topic=["Harness 与自改进", "记忆harness评价", "CPU机制组件"],
         scope="纯CPU两级case/query采样、EMA与uniform探索、未复查错误衰减、无放回/fair-share分配、选择时间戳；host批准的构建等价、完整来源指纹、最近完成祖先与一次0.6复用抽签。无LLM诊断、harness编辑、真实问答或能力评价；host验证标量不交给被测policy。",
         summary="HoMe以session级记忆差分与跨case诊断指导全harness编辑，并通过早期结构门控、两级采样和构建复用降低评价成本。",
         cost="§4.1、4.2.2与A.8：LongMemEval-S500例均值115K历史token；BEAM-1M35例×20query、均值1.04M历史token；qwen3.6-flash/qwen3.7-max API、28并发、每benchmark六候选。BEAM完整search报告10.4小时/185.2M token，非单次复用评价8分钟。完整API长rollout矩阵超单A100/A30或Mac短时预算，不下载/探跑/调用API。",
         peer="agent-research:morse", peer_path="agent-research/2611.30011-morse/README.md",
         card="agent-research/harness-and-self-improvement", page=4, figure="Figure 1", crop=[85,65,527,298]),
    dict(key="dualpm", domain="agent-research", id="2611.33612", time="01:38:15",
         title="Failure Broadens, Success Sharpens: Continual Adaptation of Tool-Use Agents Across Diverse Tasks with Dual-Polarity Memory",
         author="Tianmai M. Zhang", affiliation="University of Washington",
         organizations=["University of Washington", "Microsoft"], code=None,
         code_status="固定v1全文、arXiv及有界标题检索未找到可核实专属作者源码；TRAJECT-Bench/EvoMemBench引用代码不等于DualPM发布。",
         license=None, tier="l0_interface", topic=["记忆与技能", "双极性程序经验", "L0接口协议"],
         scope="仅L0：冻结block记忆、可见episode的reflect→draft实际typed callbacks、两极性独立维护回调、d/m/e与call-local引用校验、原子两池提交和重放拒绝。没有LLM、agent/runtime、语义grounding或记忆收益；fixture经验文本只验证接口，不是L1策略能力。",
         summary="DualPM从局部有效与无效行为起草独立极性程序经验，分块预序评价后维护容量受限的双池，整池供下一块使用。",
         cost="§3与附录D Table5：GPT-5.5任务/反思/维护、DeepSeek-V3.2裁判；四用户×200任务×4条件，每条件评价720非冷启动episode。both-on每episode162.3K加权token（其中DualPM57.2K，非raw token）；另有跨用户与四域三run外评。完整API多臂长rollout超单A100/A30或Mac短时预算，不启动完整矩阵。",
         peer="agent-research:grepmem", peer_path="agent-research/2611.25123-grepmem/README.md",
         card="agent-research/memory-and-skills", page=3, figure="Figure 1", crop=[100,76,505,320]),
    dict(key="agentic-longlive", domain="multimodal-models", id="2611.34907", time="18:54:03",
         title="Agentic LongLive: Asynchronous Agentic Memory for Long Video Generation",
         author="Shaoteng Liu", affiliation="The Chinese University of Hong Kong (CUHK)",
         organizations=["CUHK", "NVIDIA", "MIT"],
         code="https://github.com/NVlabs/LongLive/tree/main/Agentic-LongLive",
         code_status="公开作者目录/README已核实，包含agent/runtime/backends/rl；Apache-2.0。合并RL planner权重及RL数据仍标coming soon，不等于所有权重已发布。",
         license="Apache-2.0", tier=None, topic=["视频生成", "异步实体记忆", "高成本审查"],
         scope="仅review-only：固定全文、在线prompt可见性、开放环实体记忆、KV预填充与边界交换、RL训练奖励隔离、作者结果和资源成本。无本地算法、adapter/operator/command、scorer、模型/视频、metrics或GPU回执；不运行CPU mock冒充视频能力。",
         summary="Agentic LongLive在独立GPU上根据已揭示prompt准备实体文本/图像，提前prefill为attention sink，在镜头边界交换已完成版本而不等待；RL教小planner在未知未来下选择记忆。",
         cost="Figure2为六H100系统；附录B TableB1完整B200布局1DiT+2辅助+3agent，节点8×B200（180GB/卡），H3并行更大。agent为35B checker/router、4B FLUX、8B RL planner；公开README列基础视频9.4GB、encoder/VAE32GB、checker37GB、图像16GB、planner约16GB（作者大小，未下载）。56训练故事与teacher/SFT/GRPO/shared servers及多seed视频评测明显超单A100/A30或Mac，直接终态不复现。",
         peer="multimodal-models:pixvid", peer_path="multimodal-models/2611.17336-pixvid/README.md",
         card="multimodal-models/world-state-actions", page=2, figure="Figure 2", crop=[310,64,558,304]),
]


# id, level, CN question/answer/example, reviewed EN question/answer/example.
QA = {
"home": [
 ("sampling-not-ranking", "basics", "为什么自适应子集均分不能直接给候选排名？", "不同轮次覆盖和难度不同，采样又偏向旧失败。它用于找到可修复错误，不是无偏全量性能估计；选择须看共同case/query、覆盖与回归。", "教学例：A被抽到三道难题得0.6，B抽到三道易题得0.9，不能由此断言B更强。", "Why not rank candidates by adaptive-subset means?", "Rounds differ in coverage and difficulty and favor historical failures. They expose actionable errors, not unbiased full-set performance; selection needs common cases/queries, coverage and regressions.", "Teaching example: A scores 0.6 on three difficult cases and B 0.9 on three easy ones; this does not establish B is stronger."),
 ("unresolved-error-decay", "mechanism", "一次旧失败怎样在后来满分观察后降低采样影响？", "未复查错误项是log(1+错误距今轮数)/(1+错误后满分次数)。满分增加分母，但损失EMA、staleness、观察数和uniform探索仍共同决定概率。", "教学例：同一错误年龄下，零次复查项为log(4)，两次满分后为log(4)/3；不是直接删掉该case。", "How do later perfect observations reduce an old failure's influence?", "The unresolved-error term divides log(1+error age) by one plus subsequent perfect observations. EMA loss, staleness, count and uniform exploration still jointly determine probability.", "Teaching example: at the same error age, two perfect observations reduce log(4) to log(4)/3 without deleting the case."),
 ("home-versus-morse", "comparison", "HoMe与MORSE都改记忆harness，搜索边界相同吗？", "不同。HoMe围绕文件记忆的session差分归因和评价复用；MORSE让Editor在线研究并经host准入扩展视频感知服务，另有阶段性质量/延迟合同。", "教学例：修复文件检索的source多样性是HoMe方向；研究并申请OCR服务是MORSE的开放工具边界。", "Do HoMe and MORSE search the same memory-harness space?", "No. HoMe centers on file-memory session differences and evaluation reuse. MORSE adds online research and host-approved video-perception services under staged quality/latency contracts.", "Teaching example: diversifying retrieved source files fits HoMe; researching and requesting OCR expands MORSE's tool boundary."),
 ("reuse-unknown-rebuild", "implementation", "构建等价未知时为什么不能先复用再看分数？", "复用会固定旧构建，掩盖候选写入行为的变化。必须由host审查构建路径并核指纹与完成快照；未知或不兼容就重建，不能让候选自称等价。", "教学例：只改检索可获host批准复用；修改记忆schema却沿用旧快照，会漏测新构建缺陷。", "Why rebuild when construction equivalence is unknown?", "Reuse freezes old construction and can hide changed write behavior. The host must review construction paths and validate fingerprints/completed snapshots; unknown or incompatible changes rebuild.", "Teaching example: retrieval-only edits may reuse after host approval, while schema changes evaluated on old snapshots would hide construction defects."),
],
"dualpm": [
 ("local-polarity", "basics", "失败的整条轨迹只能生成失败记忆吗？", "不能这样限制。局部有效行为可以出现在最终失败轨迹，局部错误也能出现在成功轨迹；两种极性依据可见行为分别归纳，不由隐藏最终得分决定。", "教学例：正确查到联系人ID但后续漏发附件，既可记成功的ID解析，也可记失败的完整性检查。", "Can a failed episode produce only failure memories?", "No. Failed episodes can contain useful actions and successful episodes ineffective ones. Both polarities are derived independently from visible behavior, not hidden final scores.", "Teaching example: resolving a contact ID correctly but omitting an attachment supports a resolution success lesson and a completeness failure lesson."),
 ("frozen-prequential-block", "mechanism", "为什么不能把本块第一个任务的反思立即交给第二个任务？", "论文块内所有任务共享冻结的上一块记忆，整块先测试再进入反思维护。立即更新改成了逐任务在线协议，影响冷启动、比较口径与经验暴露。", "教学例：b=5时任务1到5都用M0；完成后才得到M1供任务6开始使用。", "Why not give task one's reflection immediately to task two?", "Every task in a paper block shares the previous frozen memory. The whole block is tested before reflection/maintenance; immediate updates change exposure, cold start and the evaluation protocol.", "Teaching example: with b=5, tasks one through five use M0; M1 becomes available starting at task six."),
 ("dualpm-versus-grepmem", "comparison", "DualPM容量受限是否比GrepMem更无损？", "不是同一目标。GrepMem保留原始轨迹以便grep；DualPM压缩为可迁移程序经验并可能丢掉细节。bounded memory既不保证原始细节恢复，也不证明经验有效。", "教学例：原始订单号可留在GrepMem日志；DualPM可能只保留先解析订单ID再操作的程序规则。", "Is bounded DualPM more lossless than GrepMem?", "They target different things. GrepMem retains raw trajectories for grep; DualPM abstracts transferable procedural lessons and may discard detail. Bounded memory guarantees neither detail recovery nor lesson utility.", "Teaching example: an order number may remain in GrepMem's log while DualPM retains only the procedure to resolve an order ID before acting."),
 ("lineage-not-grounding", "implementation", "通过call-local来源检查就验证了记忆真实吗？", "没有。检查只证明引用存在、同极性且容量合规；模型可能给出无效概括，来源是模型声称的lineage。本地受控回调只验证L0，不是LLM反思能力。", "教学例：一条D0确实存在，但把一次成功推广成所有任务都应跳过验证，仍可能是错误经验。", "Does valid call-local lineage establish a truthful memory?", "No. It establishes existing same-polarity references and capacity compliance, not valid generalization. Lineage is model-claimed; controlled callbacks prove L0 plumbing, not LLM reflection.", "Teaching example: D0 can exist while the lesson wrongly generalizes one success into a rule to skip all future verification."),
],
"agentic-longlive": [
 ("no-video-feedback", "basics", "memory agent为什么不读生成视频纠错？", "主协议是开放环：只读已揭示prompt，避免把生成错误写回记忆；实时已播放镜头也不能回滚。读视频是另一种消融，不是主方法输入。", "教学例：生成器画错外套颜色，主agent仍依据已揭示文本保留正确实体状态，而不是把错色学成真。", "Why does the memory agent not correct from generated video?", "The main protocol is open-loop, reading revealed prompts to avoid feeding generation errors back into memory; played shots cannot be rolled back. Reading video is a different ablation.", "Teaching example: a wrongly rendered coat color should not replace the entity state specified by the revealed prompt."),
 ("future-only-in-reward", "mechanism", "用未来标注训练奖励会让planner提前知道下一镜头吗？", "按论文隔离不会。planner只见实体bank、最近四prompt和slot预算；未来脚本供训练scorer评价选择，不能进入policy输入。oracle-next-prompt只能是破坏在线约束的上界。", "教学例：奖励可事后发现雨伞对第9镜头有用，但第8镜头policy不能读取第9条prompt来选雨伞。", "Does hindsight reward reveal the next shot to the planner?", "Not under the paper's separation. The policy sees its entity bank, four recent prompts and slot budget; future scripts belong only to reward scoring. Oracle-next-prompt is an upper bound that breaks online constraints.", "Teaching example: a scorer may later reward an umbrella useful in shot nine, but the shot-eight policy cannot read prompt nine."),
 ("memory-versus-pixels", "comparison", "Agentic LongLive与PixVid都改善视频，修改的是同一层吗？", "不是。前者冻结已有生成器并增加记忆KV和边界交换；PixVid将latent DiT迁往像素表示并训练detailer。外部一致性记忆不等于去掉VAE。", "教学例：同一个冻结latent生成器可接实体记忆；迁到像素DiT后仍需单独解决跨镜头实体记忆。", "Do Agentic LongLive and PixVid modify the same layer?", "No. The former freezes a generator and injects memory KV at boundaries; PixVid transfers latent DiT knowledge to pixels with a detailer. External consistency memory is not VAE removal.", "Teaching example: a frozen latent generator can accept entity memory, while a pixel DiT still needs a separate long-horizon memory design."),
 ("time-not-total-compute", "implementation", "约1%额外生成时间为什么不代表单卡可低成本复现？", "agent和预填充在额外GPU并行，隐藏的是关键路径延迟而非总算力。六H100示意和8×B200节点已经超出单A100/A30预算，且还需35B/4B/8B服务及完整训练评测。", "教学例：原生成器跑16秒时另外三GPU忙15秒，墙钟几乎不变，但GPU秒和下载量显著增加。", "Why does roughly 1% extra generation time not imply cheap single-GPU reproduction?", "Agent and prefill work run on extra GPUs, hiding critical-path latency rather than total compute. Six-H100/eight-B200 layouts plus 35B/4B/8B services and full training/evaluation exceed one A100/A30.", "Teaching example: three extra GPUs working for fifteen seconds during a sixteen-second shot barely change wall time but add substantial GPU-seconds and downloads."),
]}


DEEP = {
"home": dict(
 position="HoMe把文件记忆构建/检索/回答的失败用session差分追溯到harness，再用结构探索、两级采样和构建复用提高评价效率；本地只执行采样/复用，不执行诊断或优化agent。",
 tradeoff="MORSE的Editor可在线研究并经host准入扩展视频感知工具，受accuracy/efficiency阶段合同约束；HoMe固定ReMe运行时，编辑应用harness。二者评价分数与改进对象不可混为一谈。",
 title="评价预算控制不等于记忆研究能力",
 body="HoMe的EMA/staleness/count/unresolved-error与uniform项寻找可行动失败，均分不是无偏总体估计。复用须核构建等价、来源指纹和完整快照，只抽一次概率；未知必须重建。MORSE还把文献研究、外部感知服务准入和阶段性质量/延迟gate纳入完整Editor。实现采样或gate都不能替代两篇的语义agent。本地HoMe为L1数值/协议诊断，MORSE仍review-only；完整HoMe10.4h/185.2M token矩阵终态不复现。",
 en_position="HoMe localizes file-memory construction/retrieval/answer failures with session differences and improves evaluation through structural exploration, two-level sampling and reuse. The local slice executes sampling/reuse, not diagnostic or optimization agents.",
 en_tradeoff="MORSE researches and acquires host-approved video-perception tools under accuracy/efficiency contracts. HoMe fixes ReMe runtime while editing application harnesses; scores and intervention spaces are not interchangeable.",
 en_title="Evaluation budget control is not memory research capability",
 en_body="HoMe combines EMA, staleness, count, unresolved errors and uniform exploration to find actionable failures, not unbiased performance means. Reuse requires host equivalence, fingerprints and complete snapshots before one draw; unknown changes rebuild. MORSE additionally requires research, service admission and staged quality/latency gates. Sampling or gates cannot replace either semantic agent. Local HoMe is an L1 numerical/protocol diagnostic; MORSE stays review-only. The full 10.4-hour/185.2M-token HoMe campaign is terminally not reproduced."),
"dualpm": dict(
 position="DualPM有损归纳成功与失败程序经验，块内冻结、块后独立维护两池，整池进入下一块；本地只验证L0回调/来源合同，不声称LLM记忆质量。",
 tradeoff="GrepMem保留完整原始轨迹并在压缩后按需词法检索；DualPM不检索、保留的是概括规则。原日志无损、程序经验容量受限与未来行为改善是三个不同命题。",
 title="保留原始证据与抽象经验不能互相证明",
 body="DualPM局部极性不等于整轨迹标签，两次episode模型调用后每极性独立维护。冻结block保证同块无提前暴露，来源引用只是可追踪的模型声称而不是语义真实性。GrepMem的原日志与分页grep能找回摘要遗漏，但不能证明模型会检索或使用；DualPM的可迁移规则可能有效也可能错误推广。本地受控callbacks只证明L0不可变与原子合同，不是L1记忆策略或胜率；完整API矩阵成本过高终态不复现。",
 en_position="DualPM lossily abstracts success/failure procedures, freezes within-block memory, maintains the pools separately and injects the complete next-block pool. Local evidence is L0 callback/provenance compliance, not LLM memory quality.",
 en_tradeoff="GrepMem retains raw trajectories for lexical retrieval after compaction. DualPM does not retrieve and retains abstract rules. Lossless logs, bounded procedural memory and improved future behavior are different claims.",
 en_title="Retained evidence and abstract lessons do not validate each other",
 en_body="DualPM local polarity is not an episode label. Two episode-model calls precede separate polarity maintenance. Frozen blocks prevent early within-block exposure, while lineage remains model-claimed rather than semantically verified. GrepMem logs/paginated grep can recover omitted text without establishing correct model retrieval or use. DualPM rules may transfer or overgeneralize. Controlled callbacks establish only L0 immutability/atomic contracts, not L1 memory policy or success rates. The full API campaign is terminally not reproduced for cost."),
"agentic-longlive": dict(
 position="Agentic LongLive冻结视频生成器，以开放环实体记忆、后台图像绘制/预填充和边界交换保持在线一致性；planner不能看未来脚本或生成视频。",
 tradeoff="PixVid经线性对齐、噪声校准与detailer改变latent到pixel表示；它不提供LongLive的在线记忆，而LongLive的sink注入也未取消VAE。两者未跑完整矩阵，无可比本地视频指标。",
 title="隐藏关键路径延迟，不是消除总GPU成本",
 body="每镜头记忆在下一prompt到达前准备，边界只选完整prefill版本；未完成继续用旧记忆。未来标注只能用于奖励/评价，不进入planner。8B LoRA由SFT/GRPO学选择，不能拿固定recency规则替代。PixVid的像素迁移则改变生成器自身。LongLive约1%额外时间利用额外agent/辅助GPU；六H100图示、8×B200节点和35B/4B/8B模型超单卡预算。两篇本地均review-only，原图/公开mock不是复现或能力证据。",
 en_position="Agentic LongLive freezes the generator and adds open-loop entity memory, background drawing/prefill and boundary swaps. Its planner cannot read future scripts or generated video.",
 en_tradeoff="PixVid changes latent-to-pixel representation through alignment, noise calibration and a detailer. It does not supply LongLive's online memory, and sink injection does not remove the VAE. Neither full matrix ran locally; no local video metrics are comparable.",
 en_title="Hidden critical-path latency does not eliminate total GPU cost",
 en_body="Memory precedes the next prompt, boundaries select only completed prefills, and missing updates retain old memory. Future annotations are reward/evaluator-only. SFT/GRPO train the 8B selector; fixed recency is not a substitute. PixVid instead changes the generator representation. LongLive's roughly 1% added time uses extra agent/auxiliary GPUs; the six-H100 illustration, eight-B200 node and 35B/4B/8B services exceed one-card resources. Both entries are review-only: original figures/public mocks are not capability or reproduction evidence."),
}


def main():
    papers, bundle, english, proposals, reviews = {}, {}, {}, [], []
    for p in DATA:
        key, identity = p["key"], p["domain"] + ":" + p["key"]
        detail = f"{p['domain']}/{p['id']}-{key}/README.md"
        source = ROOT / ".cache/nov26-latest/agent-primary" / (p["id"] + "v1.pdf")
        folder = ROOT / "docs" / Path(detail).parent
        own_sha, source_sha = digest(folder / "README.md"), digest(source)
        implemented = p["tier"] is not None
        operator = "auto_research.agent_research." + key + ".diagnostic" if implemented else None
        command = f"PYTHONPATH=src python -c 'from auto_research.agent_research.{key} import diagnostic; print(diagnostic(42))'" if implemented else None
        spec = {
            "domain": p["domain"], "key": key, "title": p["title"],
            "paper_url": f"https://arxiv.org/abs/{p['id']}v1", "reviewed_version_url": f"https://arxiv.org/pdf/{p['id']}v1",
            "reviewed_version": "v1", "reviewed_arxiv_id": p["id"] + "v1", "detail_path": detail,
            "first_author": p["author"], "first_author_affiliation": p["affiliation"], "organizations": p["organizations"],
            "published": "2026-11-25", "published_at": f"2026-11-25T{p['time']}Z", "updated_at": f"2026-11-25T{p['time']}Z",
            "discovered_on": DATE, "reviewed_on": DATE, "announced_on": DATE,
            "code": p["code"], "code_status": p["code_status"], "code_license": p["license"], "adapter": None,
            "topic": p["topic"], "priority": "P1", "intake_class": "nov25_first_publication_discovered_nov26",
            "implementation_status": "component_only" if implemented else "deferred_high_cost", "component_implemented": implemented,
            "local_operator": operator, "local_command": command, "evaluation_tier": p["tier"] or "review_only", "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False, "requires_gpu_validation": False,
            "gpu_validation_passed": False, "gpu_validation_artifact": None, "review_done": True,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
            "review_resolution": "not_reproduced_high_cost", "deferral_reason": "成本过高，不复现（审查 DONE）；" + p["cost"],
            "automatic_retry": False, "automatic_implementation_queue": False,
            "cost_assessment": {"source": f"https://arxiv.org/pdf/{p['id']}v1", "basis": p["cost"],
                "available_resource": "one A100 or A30, or local Mac",
                "cost_type": "published_configuration_and_readonly_estimate_not_local_full_campaign_measurement",
                "decision": "成本过高，不复现（审查 DONE）；仅有界组件/接口或资料收录。",
                "local_budget": {"checkpoint_download_bytes": 0, "dataset_download_bytes": 0, "paid_api_calls": 0,
                                 "local_component_seconds_per_seed_cap": 30 if implemented else 0}},
            "summary": p["summary"], "fidelity_note": p["scope"], "method_source_sha256": source_sha,
        }
        papers[identity] = spec
        dump(folder / "assets/provenance.json", {
            "schema_version": 1, "source_url": spec["reviewed_version_url"], "source_sha256": source_sha,
            "asset_sha256": digest(folder / "assets/paper-figure-01.png"), "page": p["page"], "figure": p["figure"],
            "crop_pdf_points": p["crop"], "render_scale": 2, "reviewed_on": DATE,
            "visually_reviewed": True, "caption_preserved": True,
            "modification": "Crop unrelated text/whitespace only; scientific content unchanged.", "copyright": "Original authors"})
        sections = ["背景与主要改动", "核心公式", "论文离线与线上效果", "数据协议与代码映射", "同主题比较与边界", "完整实验与成本决定"]
        questions = []
        for qid, level, question, answer, example, eq, ea, ee in QA[key]:
            q = {"id": qid, "level": level, "question": question, "answer": answer, "example": example,
                 "source_sections": sections, "added": DATE}
            questions.append(q)
            english[f"qa/{identity}/{qid}"] = {"source_sha256": sha256(json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                "reviewed": True, "fields": {"question": eq, "answer": ea, "example": ee}}
        bundle[identity] = {"questions": questions}
        d, peer = DEEP[key], p["peer"]
        revisions = {identity: own_sha, peer: digest(ROOT / "docs" / p["peer_path"])}
        compare = questions[2]
        en_compare = english[f"qa/{identity}/{compare['id']}"]["fields"]
        proposals.append({"paper": identity, "target_card": p["card"], "source_revisions": revisions,
            "peer_membership_verified_in": f"docs/learning/topics/{p['card'].split('/')[0]}.json",
            "comparison": {"position": d["position"], "tradeoff": d["tradeoff"], "sections": sections},
            "analysis": {"title": d["title"], "body": d["body"], "papers": [identity, peer]},
            "question": {"id": "cross-nov26-" + key, **{k: compare[k] for k in ("question", "answer", "example")}, "papers": [identity, peer]},
            "update": {"date": DATE, "papers": [identity, peer], "source_revisions": revisions,
                       "summary": p["scope"] + " 完整高成本campaign终态不复现，审查DONE。"},
            "english": {"comparison": {"position": d["en_position"], "tradeoff": d["en_tradeoff"]},
                "analysis": {"title": d["en_title"], "body": d["en_body"]}, "question": en_compare,
                "update": d["en_body"] + " Review DONE; no full campaign, automatic retry or Evolve promotion."}})
        reviews.append({"identity": identity, "id": p["id"], "published_at": spec["published_at"], "updated_at": spec["updated_at"],
            "discovered_on": DATE, "announced_on": DATE, "source_url": spec["reviewed_version_url"], "source_sha256": source_sha,
            "source_revisions": revisions, "scope": p["scope"], "cost_basis": p["cost"],
            "implementation_status": spec["implementation_status"], "evaluation_tier": spec["evaluation_tier"], "review_done": True})
    dump(AUDIT / "paper-proposals-agent.json", {"schema_version": 1, "reviewed_on": DATE, "papers": papers})
    dump(AUDIT / "agent-authored-bundle.json", {"schema_version": 1, "date": DATE, "papers": bundle, "english_question_units": english})
    dump(AUDIT / "deep-dive-proposals-agent.json", {"schema_version": 1, "reviewed_on": DATE, "integration_owner": "root", "proposals": proposals})
    dump(AUDIT / "agent-review.json", {"schema_version": 1, "reviewed_on": DATE,
        "scope": "Two Nov25 first-release CPU protocol slices and one high-cost video review-only entry; finite selection, not exhaustive closure",
        "implementation_preflight_completed": True, "reviews": reviews})
    dump(AUDIT / "preflight-agent.json", {"schema_version": 1, "batch": "2026-11-26-latest-components", "owner": "agent",
        "seeds": [42,43,44], "api_calls": 0, "model_and_dataset_downloads": 0, "automatic_retry": False,
        "full_experiments_executed": False, "maximum_component_seconds_per_seed": 30,
        "components": {p["key"]: {"domain": "agent-research", "module": "agent_research/" + p["key"] + ".py",
                                    "cuda": False, "evaluation_tier": p["tier"]} for p in DATA if p["tier"]},
        "review_only": ["multimodal-models:agentic-longlive"],
        "tier_enum_verified_in": "scripts/run_nov18_latest_components.py:config accepts l0_interface and l1_mechanism"})


if __name__ == "__main__":
    main()
