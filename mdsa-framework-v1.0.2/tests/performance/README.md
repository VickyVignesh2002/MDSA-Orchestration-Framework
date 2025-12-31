# MDSA Framework - Performance Benchmark Suite

## Overview

This directory contains the official performance benchmark suite used to validate metrics reported in the MDSA research paper. All benchmarks are designed to measure real-world performance and can be run on your own hardware to verify claims.

## Prerequisites

Before running benchmarks, ensure the following requirements are met:

### 1. MDSA Framework Installation

**Required**: The MDSA package must be installed in editable mode:

```bash
pip install -e .
```

**Verification**:
```bash
python -c "from mdsa import MDSA; print('MDSA installed successfully')"
```

### 2. Models and Dependencies

- **TinyBERT Router**: Downloaded automatically on first run (~270MB)
  - Cached in `~/.mdsa/models/tinybert/`
  - First run will be slower due to model download

- **Python 3.9+**: Required for all dependencies

- **Hardware**: Minimum 8GB RAM, CPU-only supported (GPU optional for faster inference)

### 3. Test Data (Optional)

The benchmarks include default test queries. For custom testing:

- **Latency tests**: Create `test_data/sample_queries.json` (see template below)
- **Accuracy tests**: Create `test_data/labeled_queries.json` with ground-truth domains

**Test data templates** are provided in `test_data/` directory.

### 4. Virtual Environment (Recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

## Troubleshooting

### Import Error: "MDSA module not found"

**Problem**: Benchmarks fail with "ERROR: MDSA module not found"

**Solutions**:
1. Reinstall MDSA in editable mode:
   ```bash
   pip install -e .
   ```

2. Verify you're in the correct virtual environment:
   ```bash
   which python  # On Windows: where python
   python -c "import sys; print(sys.prefix)"
   ```

3. Check PYTHONPATH includes the project root:
   ```bash
   echo $PYTHONPATH  # On Windows: echo %PYTHONPATH%
   ```

### Model Download Issues

**Problem**: TinyBERT model fails to download

**Solutions**:
1. Check internet connection and firewall settings
2. Manually download and place in cache directory:
   ```bash
   mkdir -p ~/.mdsa/models/tinybert/
   # Download from Hugging Face: huawei-noah/TinyBERT_General_6L_768D
   ```

3. Use offline mode if models are pre-cached

### Missing Test Data

**Problem**: `FileNotFoundError` for test data files

**Solutions**:
1. Benchmarks use default queries if files don't exist
2. Create test data from templates in `test_data/` directory
3. Verify file paths are correct relative to `tests/performance/`

### Zero or Incorrect Measurements

**Problem**: Benchmarks show 0.00ms latency or 0.00% accuracy

**Solutions**:
1. Ensure MDSA initialized correctly (check for error messages)
2. Verify domains are registered before routing
3. Check that TinyBERT model loaded successfully
4. First run may require model download (slower, but not zero)

### Performance Differences from Research Paper

**Problem**: Measured values differ significantly from paper (e.g., 800ms vs 348ms)

**Expected**:
- **Hardware differences** significantly impact latency:
  - CPU-only: 2-3x slower than GPU
  - Different CPU models: ±50% variance
  - RAM speed affects model loading

- **First run penalty**: Model loading adds ~2-5 seconds once
- **Warm-up**: First 10-100 queries may be slower
- **Tolerance**: ±20% from paper values is normal on different hardware

**Not Expected (indicates issues)**:
- Latency < 100ms on CPU (too fast, likely error)
- Latency > 5 seconds (too slow, possible timeout/error)
- Accuracy < 80% (too low, check domain registration)

### Benchmark Crashes or Hangs

**Problem**: Benchmark script hangs or crashes mid-execution

**Solutions**:
1. Reduce query count for testing: `-n 100` instead of `-n 10000`
2. Check available RAM (model requires ~2GB minimum)
3. Disable reasoning mode (already done in updated benchmarks)
4. Check logs for specific error messages

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
