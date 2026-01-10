"""
MDSA Framework: Complete Metrics Formulas and Methodology Documentation

This file provides a comprehensive reference of all metrics used in the
MDSA research paper, including formulas, rationale, and methodology.

=== DOCUMENT STRUCTURE ===
1. METRIC_FORMULAS: LaTeX formulas for all metrics
2. METHODOLOGY_EXPLANATIONS: Why we use each method
3. BENCHMARK_METHODOLOGY: How benchmarks were conducted

Author: MDSA Research Team
Version: 1.0.3
"""

# =============================================================================
# METRIC FORMULAS - LaTeX representations for research paper
# =============================================================================

METRIC_FORMULAS = {
    # =========================================================================
    # ROUTING ACCURACY METRICS
    # =========================================================================

    "accuracy": {
        "name": "Classification Accuracy",
        "formula_latex": r"Accuracy = \frac{\sum_{i=1}^{N} \mathbf{1}[y_i = \hat{y}_i]}{N} \times 100\%",
        "formula_python": "accuracy = (correct_predictions / total_predictions) * 100",
        "description": "Percentage of queries correctly classified to their domain",
        "research_paper_value": "94.1% (IT domains), 60.9% (medical domains)",
        "table_reference": "Table 2: Overall Accuracy",
    },

    "precision": {
        "name": "Precision (Positive Predictive Value)",
        "formula_latex": r"Precision = \frac{TP}{TP + FP} \times 100\%",
        "formula_python": "precision = (true_positives / (true_positives + false_positives)) * 100",
        "description": "Proportion of positive predictions that are correct",
        "interpretation": "When router predicts domain D, how often is it right?",
        "research_paper_value": "99.2% overall precision",
        "table_reference": "Table 2: Overall Precision",
    },

    "recall": {
        "name": "Recall (Sensitivity, True Positive Rate)",
        "formula_latex": r"Recall = \frac{TP}{TP + FN} \times 100\%",
        "formula_python": "recall = (true_positives / (true_positives + false_negatives)) * 100",
        "description": "Proportion of actual positives correctly identified",
        "interpretation": "Of queries that SHOULD go to domain D, how many DO go there?",
        "research_paper_value": "94.8% post-execution recall",
        "table_reference": "Table 2: Post-Execution Recall",
    },

    "f1_score": {
        "name": "F1 Score (Harmonic Mean)",
        "formula_latex": r"F1 = \frac{2 \times Precision \times Recall}{Precision + Recall}",
        "formula_python": "f1 = 2 * (precision * recall) / (precision + recall)",
        "description": "Harmonic mean of precision and recall",
        "why_harmonic": "Penalizes extreme imbalances; F1=50% when P=99%, R=1%",
        "research_paper_value": "Macro-averaged F1 = 89.8%",
        "table_reference": "Table 2: Per-domain F1 scores",
    },

    "confidence_routing": {
        "name": "Domain Classification Decision",
        "formula_latex": r"d^* = \arg\max_{i=1..N} p(d_i|q)",
        "formula_python": "predicted_domain = max(domains, key=lambda d: probability[d])",
        "description": "Select domain with highest probability",
        "threshold_logic": r"Route if $\max p(d_i|q) \geq \tau$, else fallback",
        "research_paper_value": "tau = 0.85 for auto-routing",
    },

    # =========================================================================
    # LATENCY METRICS
    # =========================================================================

    "percentile_latency": {
        "name": "Percentile Latency (P50, P95, P99)",
        "formula_latex": r"P_k = \text{Value below which } k\% \text{ of observations fall}",
        "formula_python": "p95 = sorted_latencies[int(0.95 * len(latencies))]",
        "description": "Distribution-aware latency measurement",
        "interpretation": {
            "P50": "Typical user experience (median)",
            "P95": "Worst-case for 95% of users",
            "P99": "Edge-case latency for SLA guarantees",
        },
        "research_paper_values": {
            "P50_lab": "348ms",
            "P50_workstation": "391ms",
            "P95_lab": "692ms",
            "P95_workstation": "741ms",
            "P99": "<1000ms",
        },
        "table_reference": "Table 1: Latency Metrics",
    },

    "throughput": {
        "name": "Throughput (Queries Per Second)",
        "formula_latex": r"QPS = \frac{1000}{Mean\_Latency_{ms}}",
        "formula_python": "qps = 1000 / mean_latency_ms",
        "with_concurrency": r"QPS_{concurrent} = C \times \frac{1000}{Mean\_Latency_{ms}}",
        "littles_law": r"Throughput = \frac{Concurrency}{Mean\_Response\_Time}",
        "description": "Number of requests system can handle per second",
        "research_paper_value": "~8-10 QPS estimated",
        "table_reference": "Table 1: Throughput",
    },

    "latency_breakdown": {
        "name": "Component Latency Breakdown",
        "formula_latex": r"Total = Router + RAG + Model + Validator + Overhead",
        "components": {
            "router": "40-60ms (TinyBERT classification)",
            "rag": "70-160ms (vector search + aggregation)",
            "model": "150-240ms (LLM inference)",
            "validator": "20-50ms (pre/post checks)",
        },
        "research_paper_value": "Total = 348-391ms",
        "table_reference": "Table 1: Latency Component Breakdown",
    },

    # =========================================================================
    # RAG METRICS
    # =========================================================================

    "precision_at_k": {
        "name": "Precision@K",
        "formula_latex": r"P@K = \frac{|Retrieved@K \cap Relevant|}{K} \times 100\%",
        "formula_python": "p_at_k = len(set(retrieved[:k]) & relevant) / k * 100",
        "description": "Fraction of top-K retrieved documents that are relevant",
        "interpretation": "If K=5 and P@5=80%, then 4 of 5 retrieved docs are relevant",
        "research_paper_value": "P@3 = 87.3% (dual RAG), 76.8% (global-only)",
        "table_reference": "Section III.C",
    },

    "recall_at_k": {
        "name": "Recall@K",
        "formula_latex": r"R@K = \frac{|Retrieved@K \cap Relevant|}{|Relevant|} \times 100\%",
        "formula_python": "r_at_k = len(set(retrieved[:k]) & relevant) / len(relevant) * 100",
        "description": "Fraction of all relevant documents in top-K",
        "interpretation": "If R@5=60%, we've captured 60% of relevant knowledge",
    },

    "mean_reciprocal_rank": {
        "name": "Mean Reciprocal Rank (MRR)",
        "formula_latex": r"MRR = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{rank_i}",
        "formula_python": "mrr = sum(1/rank for rank in first_relevant_ranks) / num_queries",
        "description": "Average of reciprocal of rank of first relevant result",
        "interpretation": "MRR=0.5 means first relevant doc at position 2 on average",
    },

    "ndcg": {
        "name": "Normalized Discounted Cumulative Gain (NDCG)",
        "formula_latex": r"NDCG@K = \frac{DCG@K}{IDCG@K}, \quad DCG@K = \sum_{i=1}^{K} \frac{rel_i}{\log_2(i+1)}",
        "formula_python": "ndcg = dcg / idcg",
        "description": "Position-weighted relevance score normalized by ideal ranking",
        "interpretation": "NDCG=0.8 means ranking is 80% as good as optimal",
    },

    # =========================================================================
    # COMPLEXITY AND ROUTING METRICS
    # =========================================================================

    "complexity_score": {
        "name": "Query Complexity Score",
        "formula_latex": r"complexity(q) = \alpha \cdot (1 - \max_i p(d_i|q)) + \beta \cdot length(q)",
        "formula_python": "complexity = alpha * (1 - max_confidence) + beta * len(query.split())",
        "description": "Determines if query routes to specialist or reasoning model",
        "threshold_logic": r"If $complexity(q) > \theta$, route to reasoning model",
        "default_values": {"alpha": 0.7, "beta": 0.3, "theta": 0.5},
    },

    "embedding_similarity": {
        "name": "Cosine Similarity (Embedding Cache)",
        "formula_latex": r"sim(q_1, q_2) = \frac{e(q_1) \cdot e(q_2)}{||e(q_1)|| \cdot ||e(q_2)||}",
        "formula_python": "similarity = np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))",
        "description": "Measures semantic similarity between query embeddings",
        "cache_threshold": "If similarity > 0.95, use cached domain classification",
    },

    # =========================================================================
    # QUALITY METRICS
    # =========================================================================

    "hallucination_rate": {
        "name": "Hallucination Rate",
        "formula_latex": r"Hallucination\_Rate = \frac{False\_Statements}{Total\_Statements} \times 100\%",
        "description": "Percentage of generated statements not supported by knowledge base",
        "research_paper_value": "<1.0%",
        "measurement": "Manual review of 500 responses by domain experts",
        "table_reference": "Table 2: Hallucination Rate",
    },

    "task_completion": {
        "name": "Task Completion Accuracy",
        "formula_latex": r"Completion = \frac{Successful\_Tasks}{Total\_Tasks} \times 100\%",
        "description": "Percentage of tasks completed successfully per domain rubric",
        "research_paper_values": {
            "Development": "92.1%",
            "Business": "89.3%",
            "Finance": "86.4%",
            "Marketing": "90.2%",
            "Management": "91.0%",
        },
        "table_reference": "Table 2: Task Completion by Domain",
    },

    "safe_execution_rate": {
        "name": "Safe Execution Rate",
        "formula_latex": r"Safe\_Rate = \frac{Requests\_Passing\_Validators}{Total\_Requests} \times 100\%",
        "description": "Percentage of requests that pass all validators without rollback",
        "research_paper_value": "99.1%",
        "table_reference": "Table 2: Safe Execution Rate",
    },
}


# =============================================================================
# METHODOLOGY EXPLANATIONS - Why we use each method
# =============================================================================

METHODOLOGY_EXPLANATIONS = {
    # =========================================================================
    # WHY TINYBERT FOR ROUTING?
    # =========================================================================

    "tinybert_routing": {
        "question": "Why use TinyBERT instead of larger models for routing?",
        "answer": """
TinyBERT (67M parameters) is chosen for domain classification because:

1. SPEED: Classification in 13-17ms (CPU) vs 200-500ms for cloud LLMs
   - 10-30x faster than GPT-3.5/Claude for classification
   - Enables real-time routing without user-perceived delay

2. COST: Zero marginal cost (runs locally)
   - No API calls = no per-request charges
   - Important for high-volume production systems

3. ACCURACY: Sufficient for domain classification
   - 94.1% accuracy on IT domains (low semantic overlap)
   - 60.9% accuracy on medical domains (high overlap)
   - Classification doesn't need generation capability

4. DISTILLATION ADVANTAGE:
   - TinyBERT distilled from BERT-base, retains classification ability
   - 10x smaller but 97% of BERT's NLU capability
   - Published research: Jiao et al. (2020) TinyBERT paper

5. PRIVACY: All data stays local
   - No query content sent to cloud providers
   - Critical for healthcare, finance, legal domains
        """,
        "research_paper_section": "Section II.B, Section III.A",
    },

    # =========================================================================
    # WHY DUAL RAG?
    # =========================================================================

    "dual_rag_architecture": {
        "question": "Why use both Global and Local knowledge bases?",
        "answer": """
The dual RAG architecture addresses different retrieval needs:

GLOBAL KNOWLEDGE BASE (10,000+ documents):
- Broad coverage across all domains
- Handles cross-domain queries (e.g., "how does billing affect coding?")
- Fallback when domain classification uncertain
- Contains general organizational knowledge

LOCAL KNOWLEDGE BASES (1,000 docs per domain):
- Deep domain expertise
- Higher precision for in-domain queries
- Faster retrieval (smaller search space)
- Domain-specific terminology and context

FUSION STRATEGY:
- Retrieve k1=5 from local, k2=3 from global
- Merge with deduplication
- Re-rank by relevance score
- Result: 87.3% P@3 vs 76.8% global-only (13.7% improvement)

WHY NOT SINGLE KB?
- Single global KB dilutes domain expertise
- Single local KB misses cross-domain context
- Dual approach gets best of both worlds
        """,
        "research_paper_section": "Section III.C",
    },

    # =========================================================================
    # WHY THESE SPECIFIC METRICS?
    # =========================================================================

    "metric_selection": {
        "question": "Why these specific metrics instead of others?",
        "answer": """
Each metric serves a specific evaluation purpose:

ACCURACY vs PRECISION/RECALL/F1:
- Accuracy: Overall performance (intuitive for stakeholders)
- Precision: Reliability of positive predictions
- Recall: Coverage of true positives
- F1: Balance when classes are imbalanced

PERCENTILES vs MEAN LATENCY:
- Mean is skewed by outliers
- P50 represents typical experience
- P95/P99 critical for SLA guarantees
- Example: Mean=450ms could be P50=300ms, P99=2000ms

PRECISION@K vs RECALL@K:
- P@K: Quality of retrieved context (noise in LLM prompt)
- R@K: Coverage of relevant information
- Trade-off: Higher K = higher recall, lower precision

MRR vs NDCG:
- MRR: Important when only first result matters (factoid QA)
- NDCG: Important when multiple results matter (research queries)
- We use both for comprehensive evaluation

CONFIDENCE-BASED ACCURACY:
- Stratifies accuracy by model confidence
- Enables automatic vs manual review thresholds
- Production systems set tau based on this analysis
        """,
        "research_paper_section": "Section V",
    },

    # =========================================================================
    # BENCHMARK METHODOLOGY
    # =========================================================================

    "benchmark_methodology": {
        "question": "How were the benchmarks conducted?",
        "answer": """
HARDWARE CONFIGURATIONS:
- Lab Server: NVIDIA A100 80GB, Intel Xeon, 256GB RAM
- Workstation: NVIDIA RTX 4090 24GB, Intel Core i9, 64GB RAM
- CPU-Only: Intel 12-core, 16GB RAM (Phase 2 tests)

TEST DATASET:
- 10,000 queries across 5 domains
- Ground truth from 3 domain experts (96.8% agreement)
- Stratified sampling for domain balance

WARMUP PROTOCOL:
- First 100 queries excluded (cold start)
- Model loading, JIT compilation, cache warming
- Production-realistic conditions

MEASUREMENT:
- time.perf_counter() for nanosecond precision
- 5 independent runs, results averaged
- Outliers NOT removed (real conditions)
- 95% bootstrap confidence intervals

REPRODUCIBILITY:
- Random seed fixed (42)
- Hardware specs documented
- Code and data will be released
        """,
        "research_paper_section": "Section V.A",
    },

    # =========================================================================
    # STATISTICAL SIGNIFICANCE
    # =========================================================================

    "statistical_approach": {
        "question": "How do we ensure statistical significance?",
        "answer": """
SAMPLE SIZE JUSTIFICATION:
- 10,000 queries provides statistical power
- 95% confidence intervals for all metrics
- Standard error < 0.5% for accuracy

INTER-ANNOTATOR AGREEMENT:
- 3 independent domain experts labeled queries
- Cohen's Kappa = 0.92 (excellent agreement)
- Majority vote for ground truth

MULTIPLE RUNS:
- 5 independent benchmark runs
- Results averaged to reduce variance
- Standard deviation reported

BOOTSTRAP CONFIDENCE INTERVALS:
- 1000 bootstrap samples
- 95% CI for key metrics
- Accounts for non-normal distributions

SIGNIFICANCE TESTING:
- Paired t-test for latency comparisons
- McNemar's test for accuracy differences
- p < 0.05 threshold for significance
        """,
        "research_paper_section": "Section V.A, Appendix",
    },
}


# =============================================================================
# BENCHMARK CONFIGURATION
# =============================================================================

BENCHMARK_CONFIG = {
    "routing_accuracy": {
        "num_queries": 10000,
        "domains": ["Development", "Business", "Finance", "Marketing", "Management"],
        "confidence_bins": {
            "high": (0.90, 1.01),
            "medium": (0.85, 0.90),
            "low": (0.0, 0.85),
        },
        "warmup_queries": 100,
    },

    "latency": {
        "num_queries": 1000,
        "warmup_queries": 100,
        "runs": 5,
        "percentiles": [50, 95, 99],
        "hardware": {
            "lab": "NVIDIA A100 80GB, Intel Xeon, 256GB RAM",
            "workstation": "NVIDIA RTX 4090 24GB, Intel Core i9, 64GB RAM",
            "cpu_only": "Intel 12-core, 16GB RAM, Windows 11",
        },
    },

    "rag": {
        "num_queries": 2000,
        "local_k": 5,
        "global_k": 3,
        "relevance_scale": [0, 1, 2],  # irrelevant, partial, highly relevant
        "annotators": 3,
        "agreement_threshold": 0.90,
    },
}


# =============================================================================
# PRETTY PRINTING
# =============================================================================

def print_all_formulas():
    """Print all formulas in readable format."""
    print("=" * 80)
    print("MDSA FRAMEWORK: COMPLETE METRICS REFERENCE")
    print("=" * 80)

    for category in ["accuracy", "precision", "recall", "f1_score",
                     "percentile_latency", "throughput",
                     "precision_at_k", "mean_reciprocal_rank", "ndcg"]:
        if category in METRIC_FORMULAS:
            metric = METRIC_FORMULAS[category]
            print(f"\n{metric['name']}")
            print("-" * 40)
            print(f"Formula: {metric['formula_latex']}")
            print(f"Python:  {metric['formula_python']}")
            if 'research_paper_value' in metric:
                print(f"Paper:   {metric['research_paper_value']}")
            print()


def print_methodology(topic: str = None):
    """Print methodology explanations."""
    if topic and topic in METHODOLOGY_EXPLANATIONS:
        exp = METHODOLOGY_EXPLANATIONS[topic]
        print(f"\nQ: {exp['question']}")
        print(exp['answer'])
        print(f"\nReference: {exp['research_paper_section']}")
    else:
        print("Available topics:")
        for key in METHODOLOGY_EXPLANATIONS:
            print(f"  - {key}")


if __name__ == "__main__":
    print_all_formulas()
    print("\n" + "=" * 80)
    print("METHODOLOGY EXPLANATIONS")
    print("=" * 80)
    print_methodology("tinybert_routing")
