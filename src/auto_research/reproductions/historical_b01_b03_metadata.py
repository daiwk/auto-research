"""Verified metadata and adapter factory for historical batches B01--B03."""

from __future__ import annotations

from dataclasses import dataclass

from .base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)


@dataclass(frozen=True)
class Entry:
    key: str
    arxiv_id: str
    title: str
    organization: str
    published: str
    topics: tuple[str, ...]
    product: str
    metric: str
    lift: float
    traffic: str
    code_url: str | None = None


ENTRIES = {
    row.key: row for row in (
        Entry("dynamic-codebook", "2608.21012", "From a Static Multi-Level Small Semantic Codebook to a Dynamic Single-Level Large Semantic Codebook for Generative Recommendation", "Kuaishou Technology", "2026-08-21", ("generative-recommendation", "semantic-id", "serving-efficiency"), "Kuaishou", "primary consumption", .792, "2.5% traffic, 5 days"),
        Entry("netflix-mediafm", "2608.18322", "Multimedia Asset Personalization via Multimodal Embeddings at Netflix", "Netflix", "2026-08-18", ("multimodal-recommendation", "content-understanding", "cold-start"), "Netflix Search", "playthrough rate", .36, "Search canvas A/B"),
        Entry("ogr", "2608.17613", "Once Generated, Ranked: End-to-End Generative Slate Recommendation with Unified Semantic-Collaborative IDs", "Kuaishou Technology", "2026-08-18", ("generative-recommendation", "slate-ranking", "semantic-id", "reinforcement-learning"), "Kuaishou", "Effective Views", 1.120, "3% production traffic"),
        Entry("inthq", "2608.09634", "IntHQ: Task-Interactive Hierarchical Query on Dual-Stream Representations for Generative Recommendation", "Amap / Alibaba", "2026-08-10", ("multi-task-learning", "generative-recommendation", "long-sequence"), "Amap", "UVCTR", 1.60, "20% per bucket, 7 days"),
        Entry("pushdualgen", "2608.07989", "PushDualGen: Enabling LLMs to Generate Semantic IDs with Interpretable Copy for Industrial Push Recommendation", "Kuaishou Technology", "2026-08-08", ("generative-recommendation", "semantic-id", "llm-recommendation", "push"), "Kuaishou Push", "effective play rate", 8.50, "15% traffic, 150M users, 14 days"),
        Entry("recharness", "2607.29241", "RecHarness: A Bandit-Routed Agentic Harness for Self-Evolving Recommender Systems", "Huazhong Agricultural University (Kuaishou internship)", "2026-07-31", ("auto-research", "bandit", "ranking"), "short-video advertising", "ADVV", 2.084, "10% traffic, 7 days", "https://github.com/6lyc/RecHarness"),
        Entry("gala", "2607.29213", "GALA: Generative Aligned Learning for Adaptive Multimodal Representation in the Taobao Shangou Recommender System", "Rajax Network Technology / Taobao Shangou / Alibaba", "2026-07-31", ("multimodal-recommendation", "representation-alignment", "reinforcement-learning"), "Taobao Shangou", "order volume", .55, "randomized traffic split"),
        Entry("feedback-policy", "2607.27789", "From Understanding to Action: Feedback-Grounded Policy Discovery for Generative Recommendation", "Huazhong Agricultural University (Kuaishou internship)", "2026-07-30", ("generative-recommendation", "policy-optimization", "distillation"), "Kuaishou advertising", "Revenue", 4.506, "large-scale online A/B"),
        Entry("real-estate-rerank", "2607.14835", "LLM-Based Re-Ranking for Real Estate Search", "QuintoAndar", "2026-07-16", ("search-ranking", "llm-reranking", "content-understanding"), "QuintoAndar conversational search", "CTR", 5.3, "production A/B"),
        Entry("adaptive-ad-load", "2607.14418", "Adaptive Ad Load Design for Sponsored Search Markets: Evidence, Theory, and Deployment", "University of Washington", "2026-07-15", ("advertising", "constrained-optimization", "marketplace"), "Android app-store sponsored search", "revenue", 36.8, "66-day randomized field experiment"),
        Entry("guess-where-you-go", "2607.26073", "Guess Where You Go: Generative Next Point-of-Interest Recommendation in Amap", "Amap / Alibaba", "2026-07-13", ("generative-recommendation", "next-poi", "semantic-id", "reinforcement-learning"), "Amap homepage", "P-CTR", 5.83, "one-month A/B", "https://github.com/alibaba/SimCIT"),
        Entry("genpage", "2606.31031", "GenPage: Towards End-to-End Generative Homepage Construction at Netflix", "Netflix", "2026-06-30", ("generative-recommendation", "page-generation", "reinforcement-learning"), "Netflix homepage", "core engagement", .24, "online A/B; p<0.001"),
        Entry("journeyformer", "2606.19108", "JourneyFormer: Encoding Airbnb Guest Journey with Sequence Modeling", "Airbnb", "2026-06-17", ("search-ranking", "sequence-modeling", "long-sequence"), "Airbnb Search", "bookers", .55, "3-week A/B; p<0.01"),
        Entry("l2rec", "2605.26717", "L2Rec: Towards Dual-View Understanding of LLMs for Personalized Recommendation", "NetEase Cloud Music", "2026-05-26", ("llm-recommendation", "parameter-efficient-tuning", "multi-view"), "homepage feed", "CTR", 9.24, "6% user traffic, one month; p<0.01"),
        Entry("qgs", "2605.25514", "From Item-Only to Query-Item: Query-Conditioned Generative Search with QGS in Quark", "University of Science and Technology of China / Alibaba", "2026-05-25", ("generative-search", "search-ranking", "long-sequence"), "Quark Search", "CTR", .62, "2% traffic, 7 days"),
        Entry("tubifm", "2605.23702", "TubiFM: Unified Item, Carousel, and Search Ranking for Streaming Discovery", "Tubi", "2026-05-22", ("foundation-model", "multi-task-learning", "search-ranking"), "Tubi Search", "total viewing time", 3.9, "production A/B; p<0.05"),
        Entry("pearl-percentile", "2605.21752", "PEARL: Unbiased Percentile Estimation via Contrastive Learning for Industrial-Scale Livestream Recommendation", "TikTok", "2026-05-20", ("ranking", "contrastive-learning", "debiasing"), "livestream platform", "Watch Duration", 2.10, "week-long online A/B"),
        Entry("dadf", "2605.17863", "DADF: A Distribution-Aware Debiasing Framework for Watch-Time Regression in Recommender Systems", "Kuaishou Technology", "2026-05-18", ("ranking", "watch-time", "debiasing"), "Kuaishou full ranking", "average time spent per device", .649, "7-day A/B, then 100% traffic", "https://github.com/liuzhao09/DADF"),
    )
}


def build_adapter(key: str, run, render) -> ReproductionAdapter:
    row = ENTRIES[key]
    source = f"https://arxiv.org/html/{row.arxiv_id}v1"
    return ReproductionAdapter(
        key=key,
        paper=PaperMetadata(
            arxiv_id=row.arxiv_id,
            title=row.title,
            url=f"https://arxiv.org/abs/{row.arxiv_id}",
            track="recommendation",
            code_url=row.code_url,
            organization=row.organization,
            published=row.published,
            topics=row.topics,
            online_ab=(OnlineABEvidence(
                row.product, row.metric, row.lift, row.traffic,
                source_url=source,
                source_location="paper online evaluation section",
                retrieved_at="2026-08-24",
            ),),
        ),
        run=run,
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("private production data and features", "production serving stack"),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens-100K",),
        baseline="shared transition + content scorer",
        metrics=("Hit@10", "NDCG@10", "Fresh Hit@10", "Head share@10"),
        device_capabilities=("cpu",),
        infer_device_capabilities=False,
    )
