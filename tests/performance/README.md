# MDSA Framework - Performance Benchmark Suite

## Overview

This directory contains the official performance benchmark suite used to validate metrics reported in the MDSA research paper. All benchmarks are designed to measure real-world performance and can be run on your own hardware to verify claims.

## Test Data Source

**Research Paper Reference**: All expected values come from the 10,000-query test suite described in `draft-research-paper.txt` (Lines 200-280).

**Hardware Environments**:
- **Lab Server**: A100 80GB GPU, Intel Xeon processor, 256GB RAM
- **Developer Workstation**: RTX 4090 24GB GPU, Intel i7/i9 processor, 16GB RAM+

## Benchmarks

### 1. benchmark_latency.py - End-to-End Response Latency

**Purpose**: Measure the complete request-response cycle time

**Expected Values** (from research paper):
- Median Latency: 348ms (lab server), 391ms (workstation)
- P95 Latency: 692ms (lab), 741ms (workstation)
- P99 Latency: <1,000ms (both environments)

**Component Breakdown**:
- Router: 40-60ms
- Specialist Plan: 150-240ms
- Tool Calls: 70-160ms (local)
- Validators: 20-50ms

**Run Command**:
```bash
python tests/performance/benchmark_latency.py -n 1000
```

**Output**: Results saved to `results/latency_results.json`

---

### 2. benchmark_accuracy.py - Routing Accuracy

**Purpose**: Validate domain classification accuracy on labeled queries

**Expected Values** (from research paper):
- Overall Accuracy: 94.1% across 5 domains
- High Confidence (≥0.90): 97.3% accuracy, covers 84.7% of requests
- Medium Confidence (0.85-0.90): 89.4% accuracy, covers 12.1% of requests

**Test Dataset**: 10,000 labeled queries with ground-truth domains assigned by 3 independent experts (96.8% inter-annotator agreement)

**Run Command**:
```bash
python tests/performance/benchmark_accuracy.py -n 10000
```

**Output**: Results saved to `results/accuracy_results.json`

---

### 3. benchmark_rag.py - RAG Retrieval Precision (TODO)

**Purpose**: Measure RAG retrieval quality using Precision@k metrics

**Expected Values** (from research paper):
- Precision@1: 92.1%
- Precision@3: 87.3%
- Precision@5: 81.5%

**Test Dataset**: Queries with annotated relevant documents

**Status**: To be implemented

---

### 4. benchmark_memory.py - Memory Profiling (TODO)

**Purpose**: Profile memory usage during execution

**Expected Values** (calculated from components):
- Base Memory: 410MB (framework without models)
- With Models Loaded: 910MB (TinyBERT + quantized specialists)
- Peak Memory: <80GB (single A100 GPU)

**Status**: To be implemented

---

## Running All Benchmarks

```bash
# Run all implemented benchmarks
python tests/performance/benchmark_all.py

# Or run individually
python tests/performance/benchmark_latency.py -n 1000
python tests/performance/benchmark_accuracy.py -n 10000
```

## Hardware Requirements

**Minimum**:
- CPU: 4 cores, 8GB RAM
- GPU: 8GB VRAM (e.g., RTX 3060)
- Storage: 10GB available

**Recommended** (to match research paper conditions):
- CPU: 8+ cores, 16GB+ RAM
- GPU: 16GB+ VRAM (e.g., RTX 4090, A100)
- Storage: 50GB available for models and data

## Test Data

### Creating Test Data

If test data files don't exist, benchmarks will use default sample queries. To create proper test datasets:

**1. Labeled Queries (for accuracy benchmark)**:
Create `test_data/labeled_queries.json`:
```json
[
  {"query": "How to treat hypertension?", "domain": "clinical"},
  {"query": "What is the billing code for consultation?", "domain": "billing"},
  ...
]
```

**2. Sample Queries (for latency benchmark)**:
Create `test_data/sample_queries.json`:
```json
{
  "queries": [
    "How do I treat Type 2 diabetes?",
    "What are the side effects of metformin?",
    ...
  ]
}
```

## Interpreting Results

### Latency Benchmark

**PASS Criteria**:
- Median latency within expected range (348-391ms ±20%)
- P95 latency within expected range (692-741ms ±20%)
- P99 latency < 1,200ms

**Note**: Absolute latency values depend on hardware. Different GPUs, CPUs, and RAM will produce different results, but relative component contributions should remain consistent.

### Accuracy Benchmark

**PASS Criteria**:
- Overall accuracy ≥93.0% (within ±1% of expected 94.1%)
- High confidence accuracy ≥96.0%
- No systematic domain bias (all domains within ±3% of average)

## Methodology

### Test Procedure

1. **Environment Setup**:
   - Fresh MDSA installation
   - Models loaded (TinyBERT router, Ollama specialists)
   - ChromaDB vector store initialized
   - No warm-up queries (cold start included in measurements)

2. **Query Processing**:
   - Queries processed sequentially (no batching)
   - Full pipeline execution (router → RAG → model → validators)
   - Timing measured with Python `time.perf_counter()` (microsecond precision)

3. **Statistical Analysis**:
   - Median used as primary metric (robust to outliers)
   - Percentiles (P95, P99) for tail latency
   - Standard deviation for variability

### Reproducibility

To reproduce research paper results:
1. Use identical hardware (A100 80GB or RTX 4090 24GB)
2. Run with 10,000 queries (full test suite)
3. Use quantized models (8-bit)
4. Ensure no other GPU workloads running
5. Run multiple times and average results

### Differences from Production

These benchmarks measure **research/evaluation** performance:
- **No caching**: First-time query processing only
- **No optimization**: Default framework settings
- **Cold start included**: Models loaded on first use

Production deployments with caching, warm models, and optimized settings will show better performance.

## Results Storage

All benchmark results are saved to `results/` directory as JSON files:
- `latency_results.json`: Latency statistics
- `accuracy_results.json`: Routing accuracy metrics
- `rag_results.json`: RAG precision metrics (when implemented)
- `memory_results.json`: Memory profiling data (when implemented)

## Comparison to Research Paper

The research paper (Lines 200-280 of `draft-research-paper.txt`) reports results from:
- **Test Suite**: 10,000 anonymized requests
- **Domains**: 5 IT domains (Development, Business, Finance, Marketing, Management)
- **Hardware**: A100 80GB (lab), RTX 4090 24GB (workstation)
- **Methodology**: Sequential processing, cold start included

These benchmarks replicate that methodology for verification purposes.

## Future Enhancements

- [ ] Implement `benchmark_rag.py` with annotated relevant documents
- [ ] Implement `benchmark_memory.py` with memory profiling
- [ ] Add comparative benchmarks vs LangChain/AutoGen/CrewAI (requires separate setup)
- [ ] Add throughput benchmark (concurrent requests)
- [ ] Add cache performance benchmark
- [ ] Automated test data generation scripts

## Citation

If you use these benchmarks in your research, please cite:

```bibtex
@software{mdsa_benchmarks2025,
  title = {MDSA Performance Benchmark Suite},
  author = {MDSA Contributors},
  year = {2025},
  url = {https://github.com/your-org/mdsa-framework/tree/main/tests/performance}
}
```

## License

Apache 2.0 License - Same as MDSA Framework

## Contact

For questions about benchmarks or to report issues:
- GitHub Issues: https://github.com/your-org/mdsa-framework/issues
- Documentation: https://github.com/your-org/mdsa-framework/tree/main/docs
