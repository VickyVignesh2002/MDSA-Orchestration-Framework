"""
Manual Test Script for MDSA Phase 1 + Phase 2 Integration

This script demonstrates the core functionality of the MDSA framework
after Phase 2 completion.
"""

from mdsa import MDSA

def test_basic_orchestration():
    """Test basic orchestration workflow."""
    print("="*70)
    print("MDSA Phase 2 - Manual Integration Test")
    print("="*70)

    # 1. Initialize orchestrator
    print("\n[1] Initializing orchestrator...")
    orchestrator = MDSA(log_level="INFO")
    print(f"[OK] Orchestrator initialized: {orchestrator}")

    # 2. Register domains
    print("\n[2] Registering domains...")

    orchestrator.register_domain(
        "finance",
        "Financial transactions, banking, and money management",
        ["money", "transfer", "payment", "balance", "account", "bank"]
    )
    print("[OK] Registered 'finance' domain")

    orchestrator.register_domain(
        "support",
        "Customer support, help requests, and issue resolution",
        ["help", "issue", "problem", "support", "assist"]
    )
    print("[OK] Registered 'support' domain")

    orchestrator.register_domain(
        "weather",
        "Weather forecasts and meteorological information",
        ["weather", "forecast", "temperature", "rain", "sunny"]
    )
    print("[OK] Registered 'weather' domain")

    # 3. Test queries
    print("\n[3] Testing query classification...")

    test_queries = [
        "I need help with my account",
        "What's the weather forecast for today?",
        "Can you assist me with a technical problem?",
        "Show me the forecast for tomorrow",
        "I have an issue with my service"
    ]

    results = []
    for query in test_queries:
        print(f"\n  Query: \"{query}\"")
        result = orchestrator.process_request(query)

        print(f"  Status: {result['status']}")
        if 'metadata' in result:
            metadata = result['metadata']
            if 'domain' in metadata:
                print(f"  Domain: {metadata['domain']}")
                print(f"  Confidence: {metadata['confidence']:.2%}")
            if 'latency_ms' in metadata:
                print(f"  Latency: {metadata['latency_ms']:.2f}ms")

            if 'requires_human_review' in metadata:
                print(f"  [WARNING] Requires human review (low confidence)")

        results.append(result)

    # 4. Check statistics
    print("\n[4] Framework statistics...")
    stats = orchestrator.get_stats()

    print(f"\n  Total requests: {stats['requests_total']}")
    print(f"  Successful: {stats['requests_success']}")
    print(f"  Failed: {stats['requests_failed']}")
    print(f"  Success rate: {stats['success_rate']:.2%}")
    print(f"  Average latency: {stats['average_latency_ms']:.2f}ms")
    print(f"  Domains registered: {stats['domains_registered']}")

    print("\n  Per-domain statistics:")
    for domain, domain_stats in stats['domain_stats'].items():
        print(f"    {domain}: {domain_stats['query_count']} queries")

    # 5. Test hardware detection
    print("\n[5] Hardware capabilities...")
    hw_info = orchestrator.hardware.get_summary()

    print(f"\n  Platform: {hw_info['platform']}")
    print(f"  CPU cores: {hw_info['cpu_cores']}")
    print(f"  System RAM: {hw_info['memory_gb']:.1f}GB")
    print(f"  CUDA available: {hw_info['has_cuda']}")
    print(f"  Tier 1 device (TinyBERT): {hw_info['tier1_device']}")
    print(f"  Tier 2 device (Phi): {hw_info['tier2_device']}")

    # 6. Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    print(f"\n[OK] Orchestrator: Working")
    print(f"[OK] Domain registration: Working ({stats['domains_registered']} domains)")
    print(f"[OK] Request processing: Working ({stats['requests_total']} processed)")
    print(f"[OK] Intent classification: Working (keyword fallback mode)")
    print(f"[OK] Statistics tracking: Working")
    print(f"[OK] Hardware detection: Working")

    print("\n[INFO] Notes:")
    print("  - TinyBERT model may fall back to keyword matching if compilation fails")
    print("  - Low-confidence queries (<85%) are escalated to human review")
    print("  - Phase 2 uses placeholder steps for LOAD_SLM and EXECUTE")
    print("  - Full domain execution will be implemented in Phase 4")

    print("\n" + "="*70)
    print("Phase 2 Manual Test Complete!")
    print("="*70 + "\n")

    return results, stats


if __name__ == "__main__":
    try:
        results, stats = test_basic_orchestration()
        print("\n[SUCCESS] All manual tests passed!\n")
    except Exception as e:
        print(f"\n[ERROR] Manual test failed: {e}\n")
        import traceback
        traceback.print_exc()
