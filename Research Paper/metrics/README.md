# MDSA Framework Metrics Module

This module provides comprehensive metrics calculation for the MDSA (Multi-Domain Specialized Agentic) Framework research paper.

## Overview

The metrics module implements all evaluation metrics used to assess the MDSA framework's performance across routing accuracy, latency, RAG retrieval quality, and system performance.

## Module Structure

```
Research Paper/metrics/
├── __init__.py              # Module exports
├── routing_metrics.py       # Classification metrics (accuracy, precision, recall, F1)
├── latency_metrics.py       # Performance metrics (P50, P95, P99, throughput)
├── rag_metrics.py           # Retrieval metrics (Precision@K, Recall@K, MRR, NDCG)
├── formulas.py              # Complete formula reference and methodology
└── README.md                # This file
```

## Metrics Categories

### 1. Routing Accuracy Metrics (`routing_metrics.py`)

Evaluate TinyBERT router performance for domain classification.

| Metric | Formula | Research Paper Value |
|--------|---------|---------------------|
| **Accuracy** | `correct / total × 100` | 94.1% (IT), 60.9% (medical) |
| **Precision** | `TP / (TP + FP) × 100` | 99.2% |
| **Recall** | `TP / (TP + FN) × 100` | 94.8% |
| **F1 Score** | `2 × P × R / (P + R)` | 89.8% (macro) |

**Usage:**
```python
from metrics import calculate_accuracy, calculate_f1_score, confidence_based_accuracy

accuracy = calculate_accuracy(predictions, ground_truth)
conf_results = confidence_based_accuracy(predictions, ground_truth, confidence_scores)
```

### 2. Latency Metrics (`latency_metrics.py`)

Measure system response time characteristics.

| Metric | Formula | Research Paper Value |
|--------|---------|---------------------|
| **P50 (Median)** | 50th percentile | 348ms (lab), 391ms (workstation) |
| **P95** | 95th percentile | 692ms (lab), 741ms (workstation) |
| **P99** | 99th percentile | <1000ms |
| **Throughput** | `1000 / mean_latency` | ~8-10 QPS |

**Component Breakdown:**
- Router: 40-60ms (TinyBERT classification)
- RAG: 70-160ms (vector search)
- Model: 150-240ms (LLM inference)
- Validator: 20-50ms (pre/post checks)

**Usage:**
```python
from metrics import calculate_percentiles, calculate_throughput

percentiles = calculate_percentiles(latencies, [50, 95, 99])
throughput = calculate_throughput(latencies, concurrency=4)
```

### 3. RAG Metrics (`rag_metrics.py`)

Evaluate retrieval quality for dual RAG system.

| Metric | Formula | Research Paper Value |
|--------|---------|---------------------|
| **Precision@K** | `relevant_in_K / K` | 87.3% (dual), 76.8% (global) |
| **Recall@K** | `relevant_in_K / total_relevant` | - |
| **MRR** | `mean(1/rank_first_relevant)` | - |
| **NDCG** | `DCG / IDCG` | - |

**Usage:**
```python
from metrics import precision_at_k, dual_rag_evaluation

p_at_5 = precision_at_k(retrieved_docs, relevant_docs, k=5)
dual_metrics = dual_rag_evaluation(local_results, global_results, relevant)
```

### 4. Formulas Reference (`formulas.py`)

Complete documentation of all formulas with LaTeX representations and methodology explanations.

**Usage:**
```python
from metrics import METRIC_FORMULAS, METHODOLOGY_EXPLANATIONS

# Get formula for accuracy
accuracy_info = METRIC_FORMULAS["accuracy"]
print(accuracy_info["formula_latex"])  # LaTeX for paper
print(accuracy_info["formula_python"])  # Python implementation

# Get methodology explanation
print(METHODOLOGY_EXPLANATIONS["tinybert_routing"]["answer"])
```

## Research Paper Integration

These metrics correspond to tables in the MDSA research paper:

| Paper Table | Metrics Module |
|-------------|----------------|
| Table 1: Performance Metrics | `latency_metrics.py` |
| Table 2: Accuracy Metrics | `routing_metrics.py` |
| Section III.C: RAG Analysis | `rag_metrics.py` |

## Key Methodologies Explained

### Why TinyBERT for Routing?

1. **Speed**: 13-17ms classification vs 200-500ms for cloud LLMs
2. **Cost**: Zero marginal cost (runs locally)
3. **Accuracy**: 94.1% sufficient for domain classification
4. **Privacy**: No data sent to cloud providers

### Why Dual RAG Architecture?

1. **Local KB**: Deep domain expertise, high precision
2. **Global KB**: Broad coverage, cross-domain support
3. **Fusion**: Retrieve 5 local + 3 global, merge and re-rank
4. **Result**: 87.3% P@3 vs 76.8% global-only (+13.7%)

### Why Percentiles Instead of Mean?

1. Latency distributions are right-skewed
2. Mean can hide tail latency issues
3. P95/P99 critical for SLA guarantees
4. Example: Mean=450ms could be P50=300ms, P99=2000ms

## Benchmark Configuration

```python
BENCHMARK_CONFIG = {
    "routing_accuracy": {
        "num_queries": 10000,
        "domains": ["Development", "Business", "Finance", "Marketing", "Management"],
        "warmup_queries": 100,
    },
    "latency": {
        "num_queries": 1000,
        "runs": 5,
        "percentiles": [50, 95, 99],
    },
    "rag": {
        "num_queries": 2000,
        "local_k": 5,
        "global_k": 3,
    },
}
```

## Running Examples

Each module includes example usage in its `__main__` block:

```bash
# Run routing metrics example
python -m metrics.routing_metrics

# Run latency metrics example
python -m metrics.latency_metrics

# Run RAG metrics example
python -m metrics.rag_metrics

# Print all formulas
python -m metrics.formulas
```

## Version

- **Module Version**: 1.0.3
- **Research Paper**: MDSA: A Multi-Domain Specialized Agentic Orchestration Framework
- **Author**: MDSA Research Team
