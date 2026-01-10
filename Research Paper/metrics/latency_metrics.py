"""
Latency Performance Metrics for MDSA Framework

This module implements all latency and throughput metrics used to evaluate
the MDSA framework's performance characteristics.

=== WHY WE CALCULATE THESE METRICS ===

1. PERCENTILES (P50, P95, P99): Distribution-aware latency measurement.
   - P50 (median): Typical user experience
   - P95: Worst-case for 95% of users
   - P99: Edge-case latency, important for SLA guarantees

2. COMPONENT BREAKDOWN: Identifies bottlenecks in the pipeline.
   - Router latency: TinyBERT classification time
   - RAG latency: Knowledge retrieval time
   - Model latency: LLM inference time
   - Validator latency: Pre/post execution checks

3. THROUGHPUT: Queries per second the system can handle.
   - Critical for capacity planning
   - Determines hardware requirements

=== METHODOLOGY ===

Test Configuration:
- 10,000 synthetic queries across 5 domains
- Lab Server: NVIDIA A100 80GB, Intel Xeon
- Workstation: NVIDIA RTX 4090 24GB, Intel Core i9
- Warmup: First 100 queries excluded (cold start)
- Measurement: time.perf_counter() for nanosecond precision

Statistical Analysis:
- Outliers NOT removed (real production conditions)
- Bootstrap confidence intervals (95%)
- Multiple runs averaged (5 runs)

Author: MDSA Research Team
"""

from typing import List, Dict, Tuple, Optional
import statistics
import time
from dataclasses import dataclass


@dataclass
class LatencyResult:
    """Container for latency measurement results."""
    min_ms: float
    max_ms: float
    mean_ms: float
    median_ms: float
    stdev_ms: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    count: int


def calculate_percentiles(latencies: List[float],
                          percentiles: List[int] = [50, 95, 99]) -> Dict[str, float]:
    """
    Calculate latency percentiles from raw timing data.

    Formula:
        P_k = Value below which k% of observations fall

        For P95 with N samples:
        - Sort latencies ascending
        - P95 index = ceil(0.95 * N)
        - P95 = latencies[P95_index]

    Why These Percentiles:

        P50 (Median):
        - Represents "typical" user experience
        - Robust to outliers unlike mean
        - Research Paper: 348ms (lab), 391ms (workstation)

        P95 (95th Percentile):
        - Captures tail latency for most users
        - Standard SLA metric (e.g., "95% of requests under 700ms")
        - Research Paper: 692ms (lab), 741ms (workstation)

        P99 (99th Percentile):
        - Worst 1% of requests
        - Critical for high-traffic systems (1% of 1M = 10K slow requests)
        - Research Paper: <1000ms target

    Why Not Mean:
        - Latency distributions are typically right-skewed
        - Mean = 450ms could mean P50=300ms but P99=2000ms
        - Percentiles give full distribution picture

    Research Paper Reference:
        - Table 1: "Median Latency (Lab Server): 348ms"
        - Table 1: "P95 Latency (Lab): 692ms"
        - Section V.D: Latency distribution analysis

    Args:
        latencies: List of latency values in milliseconds
        percentiles: List of percentile values to calculate (e.g., [50, 95, 99])

    Returns:
        Dictionary mapping "p{N}_ms" to percentile values
    """
    if not latencies:
        return {f"p{p}_ms": 0.0 for p in percentiles}

    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)

    results = {}
    for p in percentiles:
        # Nearest-rank method
        idx = int((p / 100) * n)
        # Clamp to valid range
        idx = min(idx, n - 1)
        results[f"p{p}_ms"] = sorted_latencies[idx]

    return results


def calculate_latency_statistics(latencies: List[float]) -> LatencyResult:
    """
    Calculate comprehensive latency statistics.

    Formulas:
        Mean = Sum(latencies) / N
        Variance = Sum((x_i - mean)^2) / (N-1)  [sample variance]
        StdDev = sqrt(Variance)

    Why Each Statistic:

        Min/Max:
        - Identify best and worst case scenarios
        - Max helps identify cold-start or GC pauses
        - Research Paper: Max <1000ms for P99

        Mean:
        - Overall average (used for throughput estimation)
        - Less useful than percentiles for skewed distributions

        Standard Deviation:
        - Measures consistency of response times
        - Low stdev = predictable performance
        - High stdev = variable user experience

    Args:
        latencies: List of latency values in milliseconds

    Returns:
        LatencyResult dataclass with all statistics
    """
    if not latencies:
        return LatencyResult(0, 0, 0, 0, 0, 0, 0, 0, 0)

    sorted_lat = sorted(latencies)
    n = len(sorted_lat)

    return LatencyResult(
        min_ms=min(latencies),
        max_ms=max(latencies),
        mean_ms=statistics.mean(latencies),
        median_ms=statistics.median(latencies),
        stdev_ms=statistics.stdev(latencies) if n > 1 else 0,
        p50_ms=sorted_lat[int(0.50 * n)] if n > 0 else 0,
        p95_ms=sorted_lat[int(0.95 * n)] if n > 0 else 0,
        p99_ms=sorted_lat[int(0.99 * n)] if n > 0 else 0,
        count=n
    )


def calculate_latency_breakdown(total_latencies: List[float],
                                 router_latencies: List[float],
                                 rag_latencies: List[float],
                                 model_latencies: List[float],
                                 validator_latencies: List[float]) -> Dict[str, Dict[str, float]]:
    """
    Calculate per-component latency breakdown.

    Formula:
        Total = Router + RAG + Model + Validator + Overhead

        Component_Percentage = (Component_Mean / Total_Mean) * 100

    Why Component Breakdown:

        1. ROUTER TIME (40-60ms projected):
           - TinyBERT classification latency
           - Fast component, validates SLM routing approach
           - Phase 2 measured: 12.75ms median (CPU-only)

        2. RAG RETRIEVAL TIME (70-160ms projected):
           - Vector similarity search + result aggregation
           - Scales with knowledge base size
           - Optimization target: ChromaDB indexing

        3. MODEL INFERENCE TIME (150-240ms projected):
           - Domain specialist LLM generation
           - Largest component, depends on model size
           - Ollama with quantized models

        4. VALIDATOR TIME (20-50ms projected):
           - Schema validation + safety checks
           - Fast, ensures output quality
           - Small overhead for high reliability

    Bottleneck Identification:
        - If Router > 100ms: Consider model distillation
        - If RAG > 200ms: Optimize vector indices, reduce top-K
        - If Model > 500ms: Use smaller quantized model
        - If Validator > 100ms: Simplify validation rules

    Research Paper Reference:
        - Table 1: Component latency breakdown
        - Section V.D: "Router contributes only 11% of total latency"

    Args:
        total_latencies: End-to-end latency for each request
        router_latencies: TinyBERT classification time
        rag_latencies: Knowledge retrieval time
        model_latencies: LLM inference time
        validator_latencies: Validation overhead time

    Returns:
        Dictionary with per-component statistics and percentages
    """
    components = {
        "total": total_latencies,
        "router": router_latencies,
        "rag": rag_latencies,
        "model": model_latencies,
        "validator": validator_latencies
    }

    results = {}
    total_mean = statistics.mean(total_latencies) if total_latencies else 1

    for name, latencies in components.items():
        if latencies:
            stats = calculate_latency_statistics(latencies)
            results[name] = {
                "mean_ms": stats.mean_ms,
                "median_ms": stats.median_ms,
                "p95_ms": stats.p95_ms,
                "percentage_of_total": (stats.mean_ms / total_mean) * 100 if total_mean > 0 else 0
            }
        else:
            results[name] = {
                "mean_ms": 0,
                "median_ms": 0,
                "p95_ms": 0,
                "percentage_of_total": 0
            }

    return results


def calculate_throughput(latencies: List[float],
                         concurrency: int = 1) -> Dict[str, float]:
    """
    Calculate system throughput from latency measurements.

    Formula:
        Throughput (QPS) = 1000 / Mean_Latency_ms  [single-threaded]

        With concurrency:
        Throughput (QPS) = Concurrency * (1000 / Mean_Latency_ms)

        Using Little's Law:
        Throughput = Concurrency / Mean_Response_Time

    Why This Metric:

        1. CAPACITY PLANNING:
           - How many requests can we serve per second?
           - Determines required hardware for target load
           - Research Paper: ~8-10 QPS estimated

        2. COST ANALYSIS:
           - QPS * cost_per_request = operational cost
           - Compare against cloud API pricing

        3. SCALABILITY:
           - Linear scaling with concurrency?
           - Identify CPU vs memory bottlenecks

    Formula Derivation:
        - If mean latency = 125ms, one thread processes 8 req/sec
        - With 4 threads (if parallelizable): 32 req/sec
        - Actual scaling depends on I/O vs CPU bound nature

    Research Paper Reference:
        - Table 1: "Requests/Second: ~8-10"
        - Section V.E: Throughput analysis

    Args:
        latencies: List of latency values in milliseconds
        concurrency: Number of concurrent workers/threads

    Returns:
        Dictionary with throughput metrics
    """
    if not latencies:
        return {
            "requests_per_second": 0,
            "requests_per_minute": 0,
            "requests_per_hour": 0,
            "mean_latency_ms": 0
        }

    mean_latency = statistics.mean(latencies)

    # Avoid division by zero
    if mean_latency <= 0:
        mean_latency = 1

    # QPS = 1000ms / mean_latency_ms (for single thread)
    qps_single = 1000 / mean_latency
    qps_concurrent = qps_single * concurrency

    return {
        "requests_per_second": qps_concurrent,
        "requests_per_minute": qps_concurrent * 60,
        "requests_per_hour": qps_concurrent * 3600,
        "mean_latency_ms": mean_latency,
        "theoretical_max_qps": 1000 / min(latencies) if latencies else 0,
        "concurrency": concurrency
    }


def calculate_cold_start_overhead(latencies: List[float],
                                   warmup_queries: int = 10) -> Dict[str, float]:
    """
    Calculate cold start overhead vs warmed-up latency.

    Formula:
        Cold_Start_Overhead = Mean(first N queries) / Mean(remaining queries)

    Why This Metric:

        1. MODEL LOADING:
           - First query loads TinyBERT into memory
           - GPU kernels are JIT-compiled
           - Caches are cold

        2. PRODUCTION IMPACT:
           - After restart, first users experience high latency
           - Warmup strategies (pre-query) can mitigate

        3. BENCHMARK ACCURACY:
           - Must exclude cold start for fair comparison
           - Research Paper: First 100 queries excluded

    Research Paper Reference:
        - Section V.D: "First query latency: 2000-8000ms"
        - Section V.D: "Warmed median latency: 12.75ms"

    Args:
        latencies: Full list of latencies including cold start
        warmup_queries: Number of initial queries considered "cold"

    Returns:
        Dictionary with cold vs warm latency comparison
    """
    if len(latencies) <= warmup_queries:
        return {
            "cold_mean_ms": statistics.mean(latencies) if latencies else 0,
            "warm_mean_ms": 0,
            "overhead_ratio": 1.0,
            "warmup_queries": len(latencies)
        }

    cold_latencies = latencies[:warmup_queries]
    warm_latencies = latencies[warmup_queries:]

    cold_mean = statistics.mean(cold_latencies)
    warm_mean = statistics.mean(warm_latencies)

    return {
        "cold_mean_ms": cold_mean,
        "warm_mean_ms": warm_mean,
        "overhead_ratio": cold_mean / warm_mean if warm_mean > 0 else float('inf'),
        "cold_p95_ms": sorted(cold_latencies)[int(0.95 * len(cold_latencies))],
        "warm_p95_ms": sorted(warm_latencies)[int(0.95 * len(warm_latencies))],
        "warmup_queries": warmup_queries
    }


def calculate_latency_stability(latencies: List[float],
                                 window_size: int = 100) -> Dict[str, float]:
    """
    Calculate latency stability using coefficient of variation.

    Formula:
        CV = (StdDev / Mean) * 100

        Lower CV = more consistent latency

    Why This Metric:

        1. USER EXPERIENCE:
           - Consistent latency feels faster than variable
           - Users notice latency spikes more than averages

        2. SLA COMPLIANCE:
           - Low CV = predictable SLA guarantees
           - High CV = harder to set reliable thresholds

        3. SYSTEM HEALTH:
           - Rising CV indicates degradation
           - Sudden CV spike = potential issue

    Interpretation:
        - CV < 20%: Very stable
        - CV 20-50%: Moderate variability
        - CV > 50%: High variability (investigate)

    Args:
        latencies: List of latency measurements
        window_size: Window for rolling statistics

    Returns:
        Dictionary with stability metrics
    """
    if not latencies or len(latencies) < 2:
        return {
            "coefficient_of_variation": 0,
            "mean_ms": 0,
            "stdev_ms": 0,
            "stability_rating": "insufficient_data"
        }

    mean = statistics.mean(latencies)
    stdev = statistics.stdev(latencies)
    cv = (stdev / mean) * 100 if mean > 0 else 0

    if cv < 20:
        rating = "very_stable"
    elif cv < 50:
        rating = "moderate"
    else:
        rating = "high_variability"

    return {
        "coefficient_of_variation": cv,
        "mean_ms": mean,
        "stdev_ms": stdev,
        "stability_rating": rating
    }


# Example usage
if __name__ == "__main__":
    import random

    # Simulate latency data
    random.seed(42)

    # Simulate cold start + warmed latencies
    cold_start = [random.gauss(3000, 500) for _ in range(10)]  # First 10 slow
    warm_latencies = [random.gauss(15, 3) for _ in range(990)]  # Rest fast
    all_latencies = cold_start + warm_latencies

    print("=" * 60)
    print("MDSA LATENCY METRICS EXAMPLE")
    print("=" * 60)

    # Percentiles
    percentiles = calculate_percentiles(all_latencies, [50, 95, 99])
    print("\nPercentile Latencies:")
    for key, value in percentiles.items():
        print(f"  {key}: {value:.2f}ms")

    # Full statistics
    stats = calculate_latency_statistics(all_latencies)
    print(f"\nFull Statistics:")
    print(f"  Mean: {stats.mean_ms:.2f}ms")
    print(f"  Median: {stats.median_ms:.2f}ms")
    print(f"  StdDev: {stats.stdev_ms:.2f}ms")
    print(f"  P95: {stats.p95_ms:.2f}ms")

    # Cold start analysis
    cold_analysis = calculate_cold_start_overhead(all_latencies, warmup_queries=10)
    print(f"\nCold Start Analysis:")
    print(f"  Cold Mean: {cold_analysis['cold_mean_ms']:.2f}ms")
    print(f"  Warm Mean: {cold_analysis['warm_mean_ms']:.2f}ms")
    print(f"  Overhead Ratio: {cold_analysis['overhead_ratio']:.1f}x")

    # Throughput
    throughput = calculate_throughput(warm_latencies, concurrency=1)
    print(f"\nThroughput (warmed, single-thread):")
    print(f"  Requests/Second: {throughput['requests_per_second']:.1f}")

    # Stability
    stability = calculate_latency_stability(warm_latencies)
    print(f"\nLatency Stability:")
    print(f"  CV: {stability['coefficient_of_variation']:.1f}%")
    print(f"  Rating: {stability['stability_rating']}")
