"""
MDSA Research Paper Metrics Module

This module provides comprehensive metrics calculation for the MDSA framework,
including all formulas, methodologies, and explanations used in the research paper.

Metrics Categories:
1. Routing Accuracy Metrics (Precision, Recall, F1)
2. Latency Metrics (P50, P95, P99, Component Breakdown)
3. RAG Performance Metrics (Precision@K, Recall@K, MRR)
4. System Performance Metrics (Throughput, Memory)
5. Quality Metrics (Hallucination Rate, Task Completion)

Author: MDSA Research Team
Version: 1.0.3
"""

from .routing_metrics import (
    calculate_accuracy,
    calculate_precision,
    calculate_recall,
    calculate_f1_score,
    calculate_confusion_matrix,
    confidence_based_accuracy,
)

from .latency_metrics import (
    calculate_percentiles,
    calculate_latency_breakdown,
    calculate_throughput,
)

from .rag_metrics import (
    precision_at_k,
    recall_at_k,
    mean_reciprocal_rank,
    normalized_discounted_cumulative_gain,
)

from .formulas import METRIC_FORMULAS, METHODOLOGY_EXPLANATIONS

__all__ = [
    # Routing Metrics
    "calculate_accuracy",
    "calculate_precision",
    "calculate_recall",
    "calculate_f1_score",
    "calculate_confusion_matrix",
    "confidence_based_accuracy",
    # Latency Metrics
    "calculate_percentiles",
    "calculate_latency_breakdown",
    "calculate_throughput",
    # RAG Metrics
    "precision_at_k",
    "recall_at_k",
    "mean_reciprocal_rank",
    "normalized_discounted_cumulative_gain",
    # Documentation
    "METRIC_FORMULAS",
    "METHODOLOGY_EXPLANATIONS",
]
