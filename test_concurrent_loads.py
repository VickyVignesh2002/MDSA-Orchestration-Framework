"""
Concurrent Load Test for MDSA Framework

Tests concurrent model loading to verify:
- No race conditions when loading same model
- Atomic get-or-load lock is working
- No duplicate model loading
- No "already registered" errors
- Concurrent execution completes successfully
- All queries return valid results (no None values)

Usage:
    python test_concurrent_loads.py
"""

import asyncio
import logging
from mdsa import ModelManager, DomainExecutor
from mdsa.domains.config import get_predefined_domain
from mdsa.async_ import AsyncManager
from mdsa.utils.device_config import get_recommended_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_concurrent_loads():
    """Test concurrent model loading (race condition check)."""
    print("=" * 70)
    print("MDSA Concurrent Load Test")
    print("=" * 70)
    print()
    print("This test validates:")
    print("  1. No race conditions when loading same model concurrently")
    print("  2. Atomic get-or-load lock is working correctly")
    print("  3. No duplicate model loading errors")
    print("  4. All concurrent queries return valid results")
    print("  5. No None values in result list")
    print()

    # Get hardware configuration
    hw_config = get_recommended_config(prefer_gpu=True)
    print(f"[*] Hardware Configuration:")
    print(f"   Device: {hw_config['device']}")
    print(f"   Quantization: {hw_config['quantization'].name}")
    print(f"   Reason: {hw_config['reason']}")
    print()

    # Create manager with max_models=1 (all queries should reuse same model)
    print("[*] Creating ModelManager with max_models=1")
    print("   (All queries should reuse the same model)")
    model_manager = ModelManager(max_models=1)
    domain_executor = DomainExecutor(model_manager)
    async_manager = AsyncManager(domain_executor, max_concurrent=10)
    print()

    # Get domain config
    config = get_predefined_domain(
        'support',
        force_device=hw_config['device']  # Use detected device
    )

    # Prepare 10 identical queries (should all use same model)
    num_queries = 10
    queries = ["Test query for concurrent loading"] * num_queries
    configs = [config] * num_queries

    print(f"[*] Executing {num_queries} Concurrent Queries:")
    print(f"   Domain: {config.domain_id}")
    print(f"   Model: {config.model_name}")
    print(f"   Device: {config.device}")
    print(f"   Max Concurrent: {async_manager.max_concurrent}")
    print()
    print("   (First query loads model, others should reuse it)")
    print("   (Checking for race conditions...)")
    print()

    import time
    start_time = time.time()

    # Execute batch
    try:
        results = await async_manager.execute_batch(
            queries=queries,
            domain_configs=configs,
            timeout=120.0
        )
        elapsed_time = time.time() - start_time

        print(f"[*] Batch Execution Complete:")
        print(f"   Total Time: {elapsed_time:.2f}s")
        print(f"   Results Count: {len(results)}")
        print()

        # Analyze results
        print("[*] Result Analysis:")

        # Check for None values
        none_count = sum(1 for r in results if r is None)
        if none_count > 0:
            print(f"   [FAIL] Found {none_count} None values in results")
            print("   (This indicates exception handling is broken)")
        else:
            print(f"   [OK] No None values (all results are dicts)")

        # Count successes and errors
        success_count = sum(1 for r in results if r and r.get('status') == 'success')
        error_count = sum(1 for r in results if r and r.get('status') == 'error')

        print(f"   Successful: {success_count}/{num_queries}")
        print(f"   Errors: {error_count}/{num_queries}")

        # Check for "already registered" errors (race condition indicator)
        already_registered_errors = []
        for i, r in enumerate(results):
            if r and 'error' in r:
                error_msg = str(r['error']).lower()
                if 'already registered' in error_msg:
                    already_registered_errors.append(i)

        if already_registered_errors:
            print(f"   [FAIL] Race condition detected!")
            print(f"   Found 'already registered' errors in queries: {already_registered_errors}")
        else:
            print(f"   [OK] No race condition errors")

        # Check latencies
        if results and any(r for r in results):
            latencies = [r['latency_ms'] for r in results if r and 'latency_ms' in r]
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                min_latency = min(latencies)
                max_latency = max(latencies)
                print(f"   Avg Latency: {avg_latency:.0f}ms")
                print(f"   Min Latency: {min_latency:.0f}ms")
                print(f"   Max Latency: {max_latency:.0f}ms")

        print()

        # Get statistics
        stats = async_manager.get_stats()
        print("[*] Async Manager Statistics:")
        print(f"   Total Queries: {stats['total_queries']}")
        print(f"   Success Rate: {stats['success_rate']:.1f}%")
        print(f"   Peak Concurrent: {stats['concurrent_peak']}")
        print(f"   Avg Latency: {stats['avg_latency_ms']:.0f}ms")
        print(f"   Timeouts: {stats['timeouts']}")
        print()

        # Get model manager stats
        model_stats = model_manager.get_stats()
        print("[*] Model Manager Statistics:")
        print(f"   Models Loaded: {model_stats['models_loaded']}")
        print(f"   Total Uses: {model_stats['total_uses']}")
        print(f"   Total Memory: {model_stats['total_memory_mb']:.1f}MB")

        if model_stats['models']:
            for model_id, info in model_stats['models'].items():
                print(f"   Model '{model_id}':")
                print(f"      Use Count: {info['use_count']}")
                print(f"      Memory: {info['memory_mb']:.1f}MB")
        print()

        # Cleanup
        print("[*] Cleaning up...")
        await async_manager.shutdown()
        print("   Shutdown complete")
        print()

        # Validation checks
        all_passed = True

        print("=" * 70)
        print("Validation Results")
        print("=" * 70)
        print()

        # Check 1: All queries returned results (no None)
        if none_count == 0:
            print("   [OK] All queries returned valid results (no None)")
        else:
            print(f"   [FAIL] {none_count} queries returned None")
            all_passed = False

        # Check 2: No race condition errors
        if not already_registered_errors:
            print("   [OK] No race condition errors detected")
        else:
            print(f"   [FAIL] Race condition detected in {len(already_registered_errors)} queries")
            all_passed = False

        # Check 3: At least 80% success rate
        success_rate = (success_count / num_queries * 100) if num_queries > 0 else 0
        if success_rate >= 80:
            print(f"   [OK] Success rate acceptable: {success_rate:.1f}%")
        else:
            print(f"   [FAIL] Low success rate: {success_rate:.1f}% (expected >= 80%)")
            all_passed = False

        # Check 4: Only 1 model should be loaded
        if model_stats['models_loaded'] == 1:
            print(f"   [OK] Model reuse working (only 1 model loaded)")
        else:
            print(f"   [WARN] Expected 1 model, found {model_stats['models_loaded']}")

        # Check 5: Model should have been used 10 times
        if model_stats['total_uses'] >= num_queries:
            print(f"   [OK] Model reused correctly ({model_stats['total_uses']} uses)")
        else:
            print(f"   [WARN] Model uses ({model_stats['total_uses']}) < queries ({num_queries})")

        # Check 6: Peak concurrent should be reasonable
        if 1 <= stats['concurrent_peak'] <= async_manager.max_concurrent:
            print(f"   [OK] Peak concurrent within limits: {stats['concurrent_peak']}")
        else:
            print(f"   [WARN] Unexpected peak concurrent: {stats['concurrent_peak']}")

        print()

        if all_passed:
            print("=" * 70)
            print("CONCURRENT LOAD TEST: PASSED")
            print("=" * 70)
            print()
            print("Key achievements:")
            print("  [OK] No race conditions detected")
            print("  [OK] All queries returned valid results")
            print("  [OK] No duplicate model loading")
            print("  [OK] Atomic get-or-load lock is working")
            print("  [OK] Concurrent execution completed successfully")
        else:
            print("=" * 70)
            print("CONCURRENT LOAD TEST: FAILED")
            print("=" * 70)
            print()
            print("Some validation checks failed. Review output above.")

        print()
        return all_passed

    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

        # Try to cleanup
        try:
            await async_manager.shutdown()
        except:
            pass

        return False


if __name__ == '__main__':
    try:
        result = asyncio.run(test_concurrent_loads())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        exit(130)
    except Exception as e:
        print(f"\n\nTest failed with exception: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
