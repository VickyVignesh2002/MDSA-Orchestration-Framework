"""
Benchmark: End-to-End Latency Measurement

Validates the measured latency values reported in the research paper:
- Median latency: 348ms (lab server), 391ms (workstation)
- P95 latency: 692ms (lab), 741ms (workstation)
- P99 latency: <1,000ms

Hardware:
- Lab Server: A100 80GB, Intel Xeon
- Workstation: RTX 4090 24GB, Intel i7/i9
"""

import time
import statistics
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from mdsa import MDSA
except ImportError:
    print("ERROR: MDSA module not found.")
    print("Please install the package: pip install -e .")
    print("Or ensure you're in the correct virtual environment.")
    MDSA = None


def load_test_queries(file_path: str = "test_data/sample_queries.json") -> List[str]:
    """Load test queries from file."""
    query_file = Path(__file__).parent / file_path

    if query_file.exists():
        with open(query_file, 'r') as f:
            data = json.load(f)
            return data.get('queries', [])

    # Default sample queries if file doesn't exist
    return [
        "How do I treat Type 2 diabetes?",
        "What are the side effects of metformin?",
        "Explain the billing code for office visit",
        "What is the procedure for insurance claims?",
        "How to handle patient complaint escalation?",
    ] * 200  # 1000 queries total


def benchmark_latency(num_queries: int = 1000, config_path: str = None) -> Dict[str, Any]:
    """
    Measure end-to-end latency for MDSA queries.

    Args:
        num_queries: Number of queries to test (default: 1000)
        config_path: Path to MDSA config file

    Returns:
        Dictionary with latency statistics
    """
    if MDSA is None:
        print("ERROR: MDSA module not available. Cannot run benchmark.")
        return {}

    print(f"Starting latency benchmark with {num_queries} queries...")
    print("=" * 60)

    # Initialize MDSA (suppress verbose logging, disable reasoning for speed)
    print("Initializing MDSA framework...")
    if config_path:
        mdsa = MDSA(config_path=config_path, log_level="WARNING", enable_reasoning=False)
    else:
        mdsa = MDSA(log_level="WARNING", enable_reasoning=False)

    # Register medical domains for testing
    print("Registering medical domains...")
    mdsa.register_domain("medical_coding", "Medical coding for ICD-10, CPT, and HCPCS codes", ["code", "coding", "diagnosis"])
    mdsa.register_domain("medical_billing", "Medical billing and charge calculation", ["billing", "charge", "payment"])
    mdsa.register_domain("claims_processing", "Claims processing and denial management", ["claims", "denial", "insurance"])
    mdsa.register_domain("appointment_scheduling", "Appointment scheduling and management", ["appointment", "schedule", "booking"])

    # Load test queries
    queries = load_test_queries()
    if len(queries) < num_queries:
        print(f"Warning: Only {len(queries)} queries available, using all.")
        num_queries = len(queries)

    # Measure latency
    latencies = []
    print(f"\nProcessing {num_queries} queries...")

    for i, query in enumerate(queries[:num_queries]):
        start = time.perf_counter()
        try:
            response = mdsa.process_request(query)
            end = time.perf_counter()
            latency_ms = (end - start) * 1000
            latencies.append(latency_ms)

            if (i + 1) % 100 == 0:
                print(f"  Processed {i + 1}/{num_queries} queries... "
                      f"Current avg: {statistics.mean(latencies):.2f}ms")
        except Exception as e:
            print(f"  Error on query {i + 1}: {e}")
            continue

    if not latencies:
        print("ERROR: No successful queries processed.")
        return {}

    # Calculate statistics
    latencies_sorted = sorted(latencies)
    n = len(latencies_sorted)

    results = {
        "num_queries": n,
        "median_ms": statistics.median(latencies),
        "mean_ms": statistics.mean(latencies),
        "stdev_ms": statistics.stdev(latencies) if n > 1 else 0,
        "min_ms": min(latencies),
        "max_ms": max(latencies),
        "p50_ms": latencies_sorted[int(n * 0.50)],
        "p95_ms": latencies_sorted[int(n * 0.95)],
        "p99_ms": latencies_sorted[int(n * 0.99)],
    }

    # Print results
    print("\n" + "=" * 60)
    print("LATENCY BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Total Queries:    {results['num_queries']}")
    print(f"Median Latency:   {results['median_ms']:.2f} ms")
    print(f"Mean Latency:     {results['mean_ms']:.2f} ms")
    print(f"Std Deviation:    {results['stdev_ms']:.2f} ms")
    print(f"Min Latency:      {results['min_ms']:.2f} ms")
    print(f"Max Latency:      {results['max_ms']:.2f} ms")
    print(f"P50 Latency:      {results['p50_ms']:.2f} ms")
    print(f"P95 Latency:      {results['p95_ms']:.2f} ms")
    print(f"P99 Latency:      {results['p99_ms']:.2f} ms")
    print("=" * 60)

    # Compare to expected values
    print("\nCOMPARISON TO RESEARCH PAPER VALUES:")
    print(f"Expected Median:  348-391 ms")
    print(f"Measured Median:  {results['median_ms']:.2f} ms")

    if 348 <= results['median_ms'] <= 391:
        print("[PASS] Median latency within expected range")
    else:
        print("[FAIL] Median latency outside expected range")

    print(f"\nExpected P95:     692-741 ms")
    print(f"Measured P95:     {results['p95_ms']:.2f} ms")

    if 692 <= results['p95_ms'] <= 741:
        print("[PASS] P95 latency within expected range")
    else:
        print("[FAIL] P95 latency outside expected range")

    # Save results
    output_file = Path(__file__).parent / "results" / "latency_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}")

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MDSA Latency Benchmark")
    parser.add_argument("-n", "--num-queries", type=int, default=1000,
                        help="Number of queries to test (default: 1000)")
    parser.add_argument("-c", "--config", type=str, default=None,
                        help="Path to MDSA config file")

    args = parser.parse_args()

    results = benchmark_latency(num_queries=args.num_queries, config_path=args.config)

    # Exit with error code if validation failed
    if results:
        median_ok = 348 <= results['median_ms'] <= 391
        p95_ok = 692 <= results['p95_ms'] <= 741

        if median_ok and p95_ok:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)
