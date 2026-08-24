"""Verified metadata and adapter factory for historical batches B04--B06."""

from __future__ import annotations

from dataclasses import dataclass

from .base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity


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
    source_location: str
    code_url: str | None = None


ENTRIES = {row.key: row for row in (
    Entry("prl-puts", "2605.16344", "A Production-Ready RL Framework for Personalized Utility Tuning with Pareto Sweeping in Pinterest Recommender Systems", "Pinterest", "2026-05-08", ("reinforcement-learning", "multi-objective-ranking", "homefeed"), "Pinterest Homefeed", "P2P impressions", .30, "1% per arm, two weeks", "Section 6.4 / Table 1"),
    Entry("ektm", "2605.05730", "Effective Knowledge Transfer for Multi-Task Recommendation Models", "Huawei Technologies", "2026-05-07", ("multi-task-learning", "knowledge-transfer", "conversion"), "commercial recommendation platform", "eCPM", 3.93, "5%→20%→50%→100% traffic", "Section 4.4.2 / Figure 3"),
    Entry("adasid", "2604.23522", "Beyond Static Collision Handling: Adaptive Semantic ID Learning for Multimodal Recommendation at Industrial Scale", "University of Electronic Science and Technology of China / Kuaishou", "2026-04-26", ("semantic-id", "multimodal-recommendation", "retrieval"), "Kuaishou e-commerce", "GPM", 1.16, "tens of millions of users, four days", "Section 5.3 / Table 3"),
    Entry("unirec-coa", "2604.12234", "UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute", "Authors did not disclose affiliation / large-scale e-commerce platform", "2026-04-14", ("generative-recommendation", "semantic-id", "preference-alignment"), "e-commerce feed and landing page", "GMV", 5.60, "20% user traffic per bucket", "Section 4.2 / Table 5"),
    Entry("uniscale", "2603.24226", "UniScale: Synergistic Entire Space Data and Model Scaling for Search Ranking", "Taobao & Tmall Group / Alibaba", "2026-03-25", ("search-ranking", "model-scaling", "entire-space-learning"), "Taobao Search", "GMV", 2.04, "5% traffic, ten days", "Section 4.5"),
    Entry("gatesid", "2603.22916", "GateSID: Adaptive Gating for Semantic-Collaborative Alignment in Cold-Start Recommendation", "Alibaba International Digital Commerce", "2026-03-24", ("semantic-id", "cold-start", "contrastive-learning"), "industrial recommendation", "GMV", 2.6, "20% traffic, two weeks", "Section 3.4"),
    Entry("aigq", "2603.19710", "AIGQ: An End-to-End Hybrid Generative Architecture for E-commerce Query Recommendation", "Taobao & Tmall Group / Alibaba", "2026-03-20", ("query-recommendation", "generative-recommendation", "reinforcement-learning"), "Taobao HintQ", "GMV", 10.68, "thirty-day A/B", "Section 5.4"),
    Entry("safro", "2603.19585", "SaFRO: Satisfaction-Aware Fusion via Dual-Relative Policy Optimization for Short-Video Search", "Kuaishou Technology", "2026-03-20", ("search-ranking", "reinforcement-learning", "multi-task-learning"), "Kuaishou Search", "watch time", .611, "10% traffic, two months", "Section 5.4 / Table 3"),
    Entry("sort-ranking", "2603.03988", "SORT: A Systematically Optimized Ranking Transformer for Industrial-scale Recommenders", "Alibaba International Digital Commerce", "2026-03-04", ("ranking", "transformer", "serving-efficiency"), "AliExpress recommendation", "orders", 6.35, "three production scenarios", "Section 4.7 / Table 5"),
    Entry("quasid", "2603.00632", "Stop Treating Collisions Equally: Qualification-Aware Semantic ID Learning for Recommendation at Industrial Scale", "University of Electronic Science and Technology of China / Kuaishou", "2026-02-28", ("semantic-id", "collision-handling", "e-commerce"), "Kuaishou e-commerce", "GMV-S2", 2.38, "5% traffic, five days", "Section 5.4"),
    Entry("gpl-prerank", "2602.20995", "Generative Pseudo-Labeling for Pre-Ranking with LLMs", "Alibaba Group / Renmin University", "2026-02-24", ("pre-ranking", "pseudo-labeling", "llm-recommendation"), "Taobao Guess What You Like", "CTR", 3.07, "hundreds of millions DAU, two weeks", "Section 4.5 / Table 4"),
    Entry("ltv-video-ranking", "2602.17058", "A Long-term Value Prediction Framework In Video Ranking", "Alibaba Group / Tsinghua University", "2026-02-19", ("ranking", "long-term-value", "debiasing"), "Taobao video ranking", "VV", 2.49, "multi-day production A/B", "Section 5.3 / Table 6"),
    Entry("rgalign-rec", "2602.12968", "RGAlign-Rec: Ranking-Guided Alignment for Latent Query Reasoning in Recommendation Systems", "Forth AI / Shopee / Singapore University of Technology and Design", "2026-02-13", ("llm-recommendation", "query-reasoning", "preference-alignment"), "production zero-query chatbot", "CTR@3 incremental over QE-Rec", .13, "large-scale online A/B", "Section 5.4 / Table 5"),
    Entry("linkedin-feed-sr", "2602.12354", "An Industrial-Scale Sequential Recommender for LinkedIn Feed Ranking", "LinkedIn", "2026-02-12", ("ranking", "sequential-recommendation", "long-sequence"), "LinkedIn Feed", "time spent", 2.10, "production A/B", "Section 7 / Table 5"),
    Entry("cadet", "2602.11410", "CADET: Context-Conditioned Ads CTR Prediction With a Decoder-Only Transformer", "LinkedIn", "2026-02-11", ("advertising", "ctr-prediction", "decoder-only-transformer"), "LinkedIn sponsored feed", "CTR", 11.04, "large-scale online A/B", "Section 5.3 / Table 3"),
    Entry("diffureason", "2602.09744", "DiffuReason: Bridging Latent Reasoning and Generative Refinement for Sequential Recommendation", "Tencent", "2026-02-10", ("generative-recommendation", "diffusion", "reinforcement-learning"), "Tencent Ads / WeChat Channels", "ad consumption", 1.1462, "20% traffic, five days", "Section 4.7"),
    Entry("sarm", "2602.09401", "SARM: LLM-Augmented Semantic Anchor for End-to-End Live-Streaming Ranking", "Institute of Information Engineering, CAS / Kuaishou", "2026-02-10", ("live-streaming", "semantic-anchor", "multimodal-recommendation"), "Kuaishou Lite live-streaming", "watch count", 1.190, "two-week A/B; subsequently fully deployed", "Section 4.4 / Table 3"),
    Entry("ml-dcn", "2602.09194", "ML-DCN: Masked Low-Rank Deep Crossing Network Towards Scalable Ads Click-through Rate Prediction at Pinterest", "Pinterest", "2026-02-09", ("advertising", "feature-crossing", "serving-efficiency"), "Pinterest Ads", "platform-wide CTR", 1.89, "production A/B at neutral cost", "Section 4.2 / Table 6"),
    Entry("rag-qac", "2602.01023", "Unifying Ranking and Generation in Query Auto-Completion via Retrieval-Augmented Generation and Multi-Objective Alignment", "Apple", "2026-02-01", ("query-auto-completion", "retrieval-augmented-generation", "preference-alignment"), "production query auto-completion", "suggestions taken", 3.46, "10% production traffic", "Section 7 / Table 3"),
)}


def build_adapter(key: str, run, render) -> ReproductionAdapter:
    row = ENTRIES[key]
    source = f"https://arxiv.org/html/{row.arxiv_id}v1"
    return ReproductionAdapter(
        key=key,
        paper=PaperMetadata(
            arxiv_id=row.arxiv_id, title=row.title, url=f"https://arxiv.org/abs/{row.arxiv_id}",
            track="recommendation", code_url=row.code_url, organization=row.organization,
            published=row.published, topics=row.topics,
            online_ab=(OnlineABEvidence(row.product, row.metric, row.lift, row.traffic,
                source_url=source, source_location=row.source_location,
                retrieved_at="2026-08-24"),),
        ),
        run=run, render=render, fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("private production data and features", "production serving stack"),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens-100K",), baseline="shared transition + content scorer",
        metrics=("Hit@10", "NDCG@10", "Fresh Hit@10", "Head share@10"),
        device_capabilities=("cpu",), infer_device_capabilities=False,
    )
