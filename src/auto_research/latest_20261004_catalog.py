"""Meta official-source reconciliation backfill reviewed on 2026-10-04."""

from __future__ import annotations


def _paper(key, title, arxiv_id, slug, topic, author, affiliation, *, code=None, published):
    return {
        "domain": "agent-research",
        "key": key,
        "title": title,
        "paper_url": f"https://arxiv.org/abs/{arxiv_id}",
        "detail_path": f"agent-research/{arxiv_id}-{slug}/README.md",
        "topic": topic,
        "first_author": author,
        "first_author_affiliation": affiliation,
        "published": published,
        "code": code,
        "adapter": key,
        "priority": "P0",
    }


LATEST_METHOD_PAPERS = (
    _paper(
        "sira", "Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval",
        "2605.06647", "sira", ["Agent 检索", "语料感知查询扩展", "BM25"],
        "Zeyu Yang", "Meta Superintelligence Labs / Rice University（工作完成于 Meta）",
        code="https://github.com/facebookresearch/sira", published="2026-05-07",
    ),
    _paper(
        "aira2", "AIRA2: Overcoming Bottlenecks in AI Research Agents",
        "2603.26499", "aira2", ["AI 研究 Agent", "异步进化", "隐藏一致评测"],
        "Karen Hambardzumyan", "FAIR at Meta / University College London",
        published="2026-03-27",
    ),
    _paper(
        "pahf", "Learning Personalized Agents from Human Feedback",
        "2602.16173", "pahf", ["个性化 Agent", "显式记忆", "双通道反馈"],
        "Kaiqu Liang", "Meta Superintelligence Labs / Princeton University（工作完成于 Meta）",
        code="https://github.com/facebookresearch/PAHF", published="2026-02-18",
    ),
    _paper(
        "hyperagents", "HyperAgents", "2603.19461", "hyperagents",
        ["RSI", "开放式进化", "元认知自修改"],
        "Jenny Zhang", "University of British Columbia",
        code="https://github.com/facebookresearch/hyperagents", published="2026-03-19",
    ),
)
