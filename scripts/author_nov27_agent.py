"""Serialize reviewed Nov27 Agent proposals; never edit shared catalog/banks."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov27-latest"
DATE = "2026-11-27"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


PAPERS = [
 dict(key="compaction-authorization", module="compaction_authorization", id="2611.32194", published_at="2026-11-24T08:44:15Z", announced=None,
      title="LLM Agent Authorization Across Context Compaction", author="Zeming Fei", institution="University of Technology Sydney",
      organizations=["University of Technology Sydney", "National University of Singapore", "University of New South Wales"],
      code="https://anonymous.4open.science/r/LLM-Agent-Authorization-Across-Context-Compaction-504E/",
      code_status="固定PDF直接链接作者匿名artifact；实际读取README及exp_full/e59_gate_completeness/witness_gate_v3.py。无已核许可证，不复制源码；作者原始输出及专有prompt未随仓发布。",
      status="not_reproduced_high_cost", full_review=True,
      scope="真实HMAC-SHA256 occurrence/sequence分域、精确UTF-8与长度前缀framing、完整有序计数、fresh session/boundary及SQLite持久消费。只释放认证原文，不执行LLM授权语义或真实Agent攻击；可信入口/key/counter隔离是外部前提。1MiB/有符号计数为本地准入，不承诺可用性或生产安全。",
      summary="把Agent摘要上下文与授权器原始请求输入分开；可信入口见证、完整有序commit和当前计数阻止来源伪造、取消省略和重放，而不是凭内容识别注入。",
      cost="PDF Table1/§5.6/附录B：319episodes/1472summaries、192ASB pairs、18prompt/11harness、100+1008livecompactions、320frontier summaries×2generators、40+80gate episodes/eight attacks；GPT-4o/mini/frontier API与72B generator等。完整API/live多臂矩阵超单A100/A30或Mac有界预算；仅CPU小报文协议。作者0.25–0.40ms验证时间不是本地实测。",
      decision="成本过高，不复现（审查 DONE）；仅承接小型CPU认证协议。",
      peer="agent-research:runtime-tickets", peer_path="agent-research/2611.03772-runtime-tickets/README.md", card="tools-and-collaboration",
      page=4, figure="Figure 2", crop=[50,76,562,352]),
 dict(key="budgeted-submapl", module="budgeted_submapl", id="2611.34211", published_at="2026-11-25T11:35:43Z", announced="2026-11-26",
      title="Compute-Aware Submodular Online Learning in Open Multi-Agent Systems", author="Jing Liu", institution="East China University of Science and Technology",
      organizations=["East China University of Science and Technology", "University of Padova"], code=None,
      code_status="固定v1全文/arXiv入口及有界精确标题搜索未找到专属作者实现；不把第三方论文列表当作者代码。",
      status="not_run_scope_limited", full_review=False,
      scope="固定active-domain的clipped sqrt包含分配、精确Q依赖舍入、独立joint-action采样、仅所选坐标oracle查询、IPW与log-space KL更新；真归一化子模coverage小函数与评估侧期望控制。无LLM Agent、动态迁移M、完整环境/观察策略表，未伪造高成本终态。",
      summary="在当前边际收益未知时按policy/budget分配包含概率，固定基数依赖舍入保边缘，逆概率校正被查询反事实边际，再KL mirror-ascent；不以完整gain表偷选查询。",
      cost="PDF§6：30×30 grid、≤5agents/最多45坐标、T200、三权重场/三schedule/20heldoutseeds，多个beta及constantQ3。没有大模型/外部数据/已报告昂贵硬件，无总wall-clock；query数量不是实测速度。完整模拟可能可负担，本轮未承接，迁移映射与5/9action环境差异未消歧，不探跑或硬标高成本。",
      decision="组件范围完成；完整便宜模拟/迁移未承接，not_run_scope_limited，非高成本延期。",
      peer="agent-research:ooas", peer_path="agent-research/2611.30405-ooas/README.md", card="agent-policy-learning",
      page=7, figure="Algorithm 1", crop=[85,88,525,251]),
]

QA = {
"compaction-authorization": [
 ("request-not-summary", "basics", "为什么把摘要移出user角色还不够？", "这能移除摘要的伪授权，但也可能丢掉用户较早给出的限制。门让授权器拿完整原始用户序列，agent仍可读摘要；来源完整性与摘要内容真假是不同问题。", "教学例：用户先指定账户A、后来只说继续付款；只保留后一句会失去A，而完整见证序列仍保留它。", "Why is moving a summary out of the user role insufficient?", "It removes summary-derived authority but may also lose earlier user constraints. The gate supplies complete original turns to authorization while the agent keeps the summary; attribution integrity is distinct from factual truth.", "Teaching example: a user first specifies account A and later says continue payment; retaining only the latter loses A, while the witnessed sequence preserves it."),
 ("completeness-after-cancellation", "mechanism", "每条都有有效MAC，为什么仍要当前计数？", "单条MAC只证明这些出现曾被可信入口签发，不证明后来没有取消。gate要求完整有序1..m且m等于入口当前计数，省略后来的用户turn就失败关闭。", "教学例：许可是counter1，取消是counter2；只带合法counter1不能通过m=2的完整性检查。", "Why require the current count if every record has a valid MAC?", "Individual MACs establish issuance, not absence of later cancellations. The gate requires counters one through m in order and m equal to current ingress count, rejecting omitted later turns.", "Teaching example: permission at counter one cannot pass alone when cancellation at counter two makes the trusted count two."),
 ("input-versus-effect", "comparison", "该门与RuntimeTickets保护的是同一边界吗？", "不是。本文保护策略生成前的原始授权输入；RuntimeTickets在真实副作用前核冻结recipient/object/budget合同。原文完整不证明策略语义正确，合法发送也不证明摘要来源真实。", "教学例：认证用户原句后生成器仍可能错误放宽recipient，需要下层ticket核具体交付，而不是把MAC当语义理解。", "Does this gate protect the same boundary as RuntimeTickets?", "No. It protects authorization input before policy synthesis; RuntimeTickets checks frozen recipient/object/budget contracts before effects. Intact originals do not prove correct policy semantics or authenticate summaries through valid sends.", "Teaching example: a generator can still broaden recipients after reading authentic text, requiring effect-level ticket checks rather than treating MACs as semantic understanding."),
 ("trusted-state-assumptions", "implementation", "用了HMAC库就能阻止同进程Agent改授权吗？", "不能。可信入口必须真实归因，keys/counters/issuer要在Agent权限外。该本地库验证协议和重放持久状态，不提供恶意Python隔离，也不保证门失败后的可用性。", "教学例：Agent若可直接调用ingest并传USER，等于拿到签发权，破坏论文前提；私有字段命名不构成沙箱。", "Does an HMAC library stop an in-process agent from changing authority?", "No. Ingress attribution must be truthful and keys, counters and issuance outside agent access. The local library tests protocol/persistent replay state, not malicious-Python isolation or availability after failure.", "Teaching example: letting an agent call ingest with USER grants issuing power and violates the assumptions; private attribute names are not a sandbox."),
],
"budgeted-submapl": [
 ("query-not-action-budget", "basics", "查询预算Q限制的是执行动作还是梯度反馈？", "限制当前轮可评估的agent-action反事实边际数量；所有active agent仍各采样一个执行action。未查询坐标估计为0不是实际收益为0，也不是停止该agent。", "教学例：两agent各两action共4坐标，Q=2只问2个边际，但两agent仍各执行一个动作。", "Does query budget Q limit executed actions or feedback?", "It limits evaluated counterfactual agent-action marginals in a round. Every active agent still samples an action; zero estimates for unqueried coordinates neither imply zero utility nor stop that agent.", "Teaching example: two agents with two actions have four coordinates; Q=2 queries two marginals while both agents still act."),
 ("dependent-rounding-marginals", "mechanism", "为什么不能直接按rho做普通加权无放回抽样？", "rho是每坐标被包含的边缘概率，不是任意抽样权重。IPW无偏要求E[Z]=rho且总数恰好Q；成对依赖舍入同时保两者，普通加权抽样一般改变边缘概率。", "教学例：rho=(0.2,0.8)、Q=1，第一坐标必须恰以0.2概率入选；分母不能随便换成未校准的权重。", "Why not use ordinary weighted sampling without replacement?", "Rho specifies inclusion marginals, not arbitrary weights. Unbiased IPW requires E[Z]=rho and exactly Q selections; pairwise dependent rounding preserves both, while generic weighted sampling usually changes marginals.", "Teaching example: rho=(0.2,0.8), Q=1 requires the first coordinate's inclusion probability to be exactly 0.2, not an uncalibrated weight."),
 ("coordinate-versus-task-event", "comparison", "SubMAPL与OOAS的重要性权重可互换吗？", "不可。前者观察被查询的反事实边际，按坐标包含概率校正；OOAS只观察任务总反馈，按共享noise产生的整任务同臂事件概率校正hint残差。两者反馈可见性和更新器都不同。", "教学例：一任务中切过臂时OOAS残差归因全0；SubMAPL同轮选中的两坐标仍各按自己的rho更新。", "Can SubMAPL and OOAS interchange importance weights?", "No. SubMAPL observes queried counterfactual marginals and corrects coordinate inclusion; OOAS sees task aggregates and corrects hint residuals by a shared-noise whole-task same-arm event. Feedback and updates differ.", "Teaching example: switching arms zeroes OOAS residual attribution, while two queried SubMAPL coordinates still receive their own inclusion-corrected updates."),
 ("scope-not-high-cost", "implementation", "数值内核通过就能说完整open-system模拟完成吗？", "不能。动态迁移M在本篇未给正式定义，完整观察表和环境没实现；原文也不足以把便宜模拟判高成本。应保留scope-limited/false full-review，不补猜或伪造终态。", "教学例：固定两agent测试Q精确，不等于重现agent离开再加入时历史logit如何迁移，也不等于20seed覆盖曲线。", "Does a passing numerical kernel complete the open-system simulation?", "No. The paper defers formal migration M and the local slice lacks its environment/observation table. Nor is the small simulation demonstrably expensive. Keep scope-limited/false full review rather than inventing migration or a cost terminal.", "Teaching example: exact Q with two fixed agents does not reproduce retained logits across departures/returns or twenty-seed coverage curves."),
]}

DEEP = {
"compaction-authorization": (
 "在策略生成前，以入口见证、完整有序列表commit和当前计数绑定用户原始授权文本；agent的摘要工作上下文不参与授权归因。",
 "RuntimeTickets在副作用前核收件者、对象和预算合同，HMAC审计链不自证前缀完整；本文当前计数拒绝取消省略，却不提供对象validator或安全策略语义。",
 "认证来源不替代语义授权，副作用合同不替代请求完整性",
 "两条输入必须分开：摘要服务Agent任务，认证原文服务授权器。occurrence MAC、顺序commit、current count/fresh boundary缺一会留echo/replay/omission缝隙。持久counter测试只在keys/state/issuer可信的前提内成立，SQLite不是Agent隔离。RuntimeTickets则冻结host收紧合同并在effect前审计，callback不确定不重发；它本地的审计链不证明被截短前缀完整。两层可组合但没有本地LLM攻击成功率；完整多模型/live矩阵高成本不复现。",
 "Authenticate original user text before policy synthesis using ingress witnesses, an ordered complete commitment and current count. The agent's summary context supplies no authority.",
 "RuntimeTickets checks recipient/object/budget before effects; its audit HMAC chain does not establish prefix completeness. Current-count checks reject omitted cancellations here but supply neither object validators nor semantic policy safety.",
 "Authenticated origins do not replace semantic authorization or effect contracts",
 "Separate agent summaries from authenticated authorizer input. Occurrence MACs, ordered commitments and current-count/fresh-boundary checks jointly close echo, replay and omission gaps. Persistent-counter tests assume protected keys/state/issuance; SQLite is not agent isolation. RuntimeTickets freezes host-restricting effect contracts, audits before callbacks and avoids retries under uncertainty, but its local chain does not prove complete prefixes. The layers compose without local LLM attack-rate evidence. The full multi-model/live matrix is terminally not reproduced for cost."),
"budgeted-submapl": (
 "固定域多agent分类策略在收益未知前分配rho，依赖舍入精确Q后只问所选边际，IPW与KL更新保留实际预算化策略学习。",
 "OOAS只见aggregate任务回报与逐turn hint，使用共享Exp噪声和整任务同臂概率；本篇可查询反事实坐标。重要性分母、反馈粒度与FTRL/KL更新不可替换。",
 "预算反馈的无偏性取决于采样事件，不是统一的1/p技巧",
 "SubMAPL的rho是边缘包含概率，固定基数依赖舍入须保E[Z]=rho，query选择不能偷看当前gain或联合action。IPW后在每agent simplex做KL mirror-ascent，sqrt分配最小化二阶矩上界而非保证胜率。OOAS全任务共享noise使同臂事件概率不等于边缘概率乘积，切臂时不归因残差。两者本地都是有限数学核，非LLM Agent。SubMAPL迁移/环境尚未承接且无证据高成本，完整状态保留scope-limited/false full-review，不能制造高成本DONE。",
 "Before gains are observed, fixed-domain categorical policies allocate rho, round to exactly Q queries, obtain only selected marginals and execute IPW/KL updates.",
 "OOAS sees aggregate task feedback and turn hints under shared exponential noise/whole-task same-arm events. This paper can query counterfactual coordinates; denominators, feedback granularity and FTRL/KL updates are not interchangeable.",
 "Unbiased budgeted feedback depends on the sampling event, not a generic 1/p trick",
 "SubMAPL rho denotes inclusion marginals: fixed-cardinality dependent rounding must preserve E[Z]=rho, and querying cannot inspect current gains or sampled joint actions. IPW precedes per-agent KL ascent; square-root allocation optimizes a second-moment bound, not success rates. OOAS shared noise makes whole-task same-arm probability differ from products of marginals and assigns no residual after switching. Both local entries are finite mathematical kernels, not LLM agents. SubMAPL migration/environment are unaccepted without high-cost evidence, so full status remains scope-limited with false full review rather than a fabricated cost-DONE terminal."),
}


def main():
    papers, bundle, english, proposals, reviews = {}, {}, {}, [], []
    for p in PAPERS:
        key, identity = p['key'], 'agent-research:' + p['key']
        detail=f"agent-research/{p['id']}-{key}/README.md"
        folder=ROOT/'docs'/Path(detail).parent
        primary=ROOT/'.cache/nov27-latest/agent-primary'/(p['id']+'v1.pdf')
        source_hash=digest(primary)
        spec={"domain":"agent-research","key":key,"title":p['title'],"paper_url":f"https://arxiv.org/abs/{p['id']}v1",
              "reviewed_version_url":f"https://arxiv.org/pdf/{p['id']}v1","reviewed_version":"v1","reviewed_arxiv_id":p['id']+'v1',
              "detail_path":detail,"first_author":p['author'],"first_author_affiliation":p['institution'],"organizations":p['organizations'],
              "published":p['published_at'][:10],"published_at":p['published_at'],"updated_at":p['published_at'],
              "announced_on":p['announced'],"discovered_on":DATE,"reviewed_on":DATE,
              "code":p['code'],"code_status":p['code_status'],"code_license":None,"adapter":None,
              "topic":["工具与协作","认证请求完整性"] if key=='compaction-authorization' else ["Agent策略学习","预算化多智能体协调数学核"],
              "priority":"P1","intake_class":"uncataloged_overlap_first_release_not_today","implementation_status":"component_only",
              "component_implemented":True,"local_operator":f"auto_research.agent_research.{p['module']}.diagnostic",
              "local_command":f"PYTHONPATH=src python -c 'from auto_research.agent_research.{p['module']} import diagnostic; print(diagnostic(42))'",
              "evaluation_tier":"l1_mechanism","diagnostic_only":True,"promotion_eligible":False,"evolve_integrated":False,
              "requires_gpu_validation":False,"gpu_validation_passed":False,"gpu_validation_artifact":None,
              "review_done":True,"full_experiment_status":p['status'],"full_experiment_review_done":p['full_review'],
              "review_resolution":"not_reproduced_high_cost" if p['full_review'] else "component_scope_complete",
              "deferral_reason":p['decision'],"automatic_retry":False,"automatic_implementation_queue":False,
              "cost_assessment":{"source":f"https://arxiv.org/pdf/{p['id']}v1","basis":p['cost'],
                  "available_resource":"one A100 or A30, or local Mac","cost_type":"published_configuration_and_readonly_scope_estimate_not_local_full_measurement",
                  "decision":p['decision'],"local_budget":{"checkpoint_download_bytes":0,"dataset_download_bytes":0,"paid_api_calls":0,"local_component_seconds_per_seed_cap":30}},
              "summary":p['summary'],"fidelity_note":p['scope'],"method_source_sha256":source_hash}
        papers[identity]=spec
        dump(folder/'assets/provenance.json',{"schema_version":1,"source_url":spec['reviewed_version_url'],"source_sha256":source_hash,
             "asset_sha256":digest(folder/'assets/paper-figure-01.png'),"page":p['page'],"figure":p['figure'],"crop_pdf_points":p['crop'],
             "render_scale":2,"reviewed_on":DATE,"visually_reviewed":True,"caption_preserved":True,
             "modification":"Crop unrelated text/whitespace only; scientific content unchanged.","copyright":"Original authors"})
        sections=["背景与主要改动","核心公式","论文离线与线上效果","数据协议与代码映射","结果、负控与边界","同主题比较与边界","完整实验与成本决定"]
        questions=[]
        for qid,level,q,a,e,eq,ea,ee in QA[key]:
            question={"id":qid,"level":level,"question":q,"answer":a,"example":e,"source_sections":sections,"added":DATE}
            questions.append(question)
            english[f"qa/{identity}/{qid}"]={"source_sha256":sha256(json.dumps(question,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                                           "reviewed":True,"fields":{"question":eq,"answer":ea,"example":ee}}
        bundle[identity]={"questions":questions}
        revisions={identity:digest(folder/'README.md'),p['peer']:digest(ROOT/'docs'/p['peer_path'])}
        pos,trade,title,body,epos,etrade,etitle,ebody=DEEP[key]
        comparison=questions[2]
        proposals.append({"paper":identity,"target_card":"agent-research/"+p['card'],"source_revisions":revisions,
            "peer_membership_verified_in":"docs/learning/topics/agent-research.json",
            "comparison":{"position":pos,"tradeoff":trade,"sections":sections},
            "analysis":{"title":title,"body":body,"papers":[identity,p['peer']]},
            "question":{"id":"cross-nov27-"+key,**{k:comparison[k] for k in ('question','answer','example')},"papers":[identity,p['peer']]},
            "update":{"date":DATE,"papers":[identity,p['peer']],"source_revisions":revisions,"summary":p['scope']+' '+p['decision']},
            "english":{"comparison":{"position":epos,"tradeoff":etrade},"analysis":{"title":etitle,"body":ebody},
                "question":english[f"qa/{identity}/{comparison['id']}"]['fields'],"update":ebody}})
        reviews.append({"identity":identity,"id":p['id'],"published_at":p['published_at'],"announced_on":p['announced'],"discovered_on":DATE,
                        "source_url":spec['reviewed_version_url'],"source_sha256":source_hash,"source_revisions":revisions,
                        "scope":p['scope'],"cost_basis":p['cost'],"full_experiment_status":p['status'],
                        "full_experiment_review_done":p['full_review'],"review_done":True})
    dump(AUDIT/'paper-proposals-agent.json',{"schema_version":1,"reviewed_on":DATE,"papers":papers})
    dump(AUDIT/'agent-authored-bundle.json',{"schema_version":1,"date":DATE,"papers":bundle,"english_question_units":english})
    dump(AUDIT/'deep-dive-proposals-agent.json',{"schema_version":1,"reviewed_on":DATE,"integration_owner":"root","proposals":proposals})
    dump(AUDIT/'agent-primary-review.json',{"schema_version":1,"reviewed_on":DATE,"implementation_preflight_completed":True,
        "scope":"Two uncataloged Nov24/25 overlap CPU mechanisms, no today's-first-release/exhaustive coverage claim", "reviews":reviews})


if __name__=='__main__':
    main()
