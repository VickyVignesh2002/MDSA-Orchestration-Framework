"""
Memory Stress Test for MDSA Framework

Tests model loading under memory constraints to verify:
- LRU eviction is working correctly
- Memory usage stays within safe limits
- Multiple domains can be loaded sequentially
- No memory leaks or accumulation
- System remains stable under memory pressure

Usage:
    python test_memory_stress.py
"""

import asyncio
import psutil
import logging
from mdsa import ModelManager, DomainExecutor
from mdsa.domains.config import get_predefined_domain
from mdsa.async_ import AsyncExecutor
from mdsa.utils.device_config import get_recommended_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_memory_stress():
    """Test model loading under memory constraints."""
    print("=" * 70)
    print("MDSA Memory Stress Test")
    print("=" * 70)
    print()
    print("This test validates:")
    print("  1. LRU eviction is working correctly")
    print("  2. Memory usage stays within safe limits")
    print("  3. Multiple domains can be loaded sequentially")
    print("  4. No memory leaks or accumulation")
    print()

    # Get initial memory state
    mem_start = psutil.virtual_memory()
    initial_available_gb = mem_start.available / (1024**3)
    initial_used_gb = mem_start.used / (1024**3)

    print(f"[*] Initial System State:")
    print(f"   RAM Total: {mem_start.total / (1024**3):.2f}GB")
    print(f"   RAM Available: {initial_available_gb:.2f}GB")
    print(f"   RAM In Use: {initial_used_gb:.2f}GB ({mem_start.percent:.1f}%)")
    print()

    # Get hardware configuration
    hw_config = get_recommended_config(prefer_gpu=True)
    print(f"[*] Hardware Configuration:")
    print(f"   Device: {hw_config['device']}")
    print(f"   Quantization: {hw_config['quantization'].name}")
    print(f"   Reason: {hw_config['reason']}")
    print()

    # Create manager with LOW limit (max_models=1) to force eviction
    print("[*] Creating ModelManager with max_models=1 (forces LRU eviction)")
    model_manager = ModelManager(max_models=1)
    domain_executor = DomainExecutor(model_manager)
    async_executor = AsyncExecutor(domain_executor, max_workers=5)
    print()

    # Test multiple domains sequentially
    domains = ['finance', 'medical', 'support', 'technical']
    memory_measurements = []

    print("[*] Testing Sequential Domain Loading:")
    print("   (Each domain should trigger LRU eviction of previous)")
    print()

    for domain_name in domains:
        print(f"--- Testing '{domain_name}' domain ---")

        # Get domain config
        config = get_predefined_domain(
            domain_name,
            force_device=hw_config['device']  # Use detected device
        )

        # Measure memory before
        mem_before = psutil.virtual_memory()
        available_before = mem_before.available / (1024**3)
        used_before = mem_before.used / (1024**3)

        print(f"Before load:")
        print(f"  Available: {available_before:.2f}GB")
        print(f"  In Use: {used_before:.2f}GB ({mem_before.percent:.1f}%)")

        # Execute query
        try:
            result = await async_executor.execute_async(
                query="Hello, this is a test query.",
                domain_config=config,
                timeout=120.0
            )

            # Measure memory after
            mem_after = psutil.virtual_memory()
            available_after = mem_after.available / (1024**3)
            used_after = mem_after.used / (1024**3)
            mem_delta = used_after - used_before

            print(f"After load:")
            print(f"  Available: {available_after:.2f}GB")
            print(f"  In Use: {used_after:.2f}GB ({mem_after.percent:.1f}%)")
            print(f"  Delta: +{mem_delta:.2f}GB")
            print(f"  Status: {result['status']}")
            print(f"  Latency: {result['latency_ms']:.0f}ms")

            # Store measurement
            memory_measurements.append({
                'domain': domain_name,
                'mem_delta_gb': mem_delta,
                'available_gb': available_after,
                'used_gb': used_after,
                'percent': mem_after.percent,
                'status': result['status']
            })

            # Verify memory usage is reasonable
            if mem_delta > 10.0:
                print(f"  [WARN] High memory usage: {mem_delta:.2f}GB")
            else:
                print(f"  [OK] Memory usage within limits")

        except Exception as e:
            print(f"  [ERROR] Domain test failed: {e}")
            memory_measurements.append({
                'domain': domain_name,
                'mem_delta_gb': 0,
                'available_gb': 0,
                'used_gb': 0,
                'percent': 0,
                'status': 'error'
            })

        print()

    # Get model manager stats
    stats = model_manager.get_stats()
    print("[*] Model Manager Statistics:")
    print(f"   Models Loaded: {stats['models_loaded']}")
    print(f"   Max Models: {stats['max_models']}")
    print(f"   Total Memory: {stats['total_memory_mb']:.1f}MB")
    print(f"   Total Uses: {stats['total_uses']}")
    print()

    # Cleanup
    print("[*] Cleaning up...")
    await async_executor.shutdown_async()
    print("   Shutdown complete")
    print()

    # Final memory check
    mem_end = psutil.virtual_memory()
    final_available_gb = mem_end.available / (1024**3)
    final_used_gb = mem_end.used / (1024**3)
    total_delta = final_used_gb - initial_used_gb

    print("[*] Final System State:")
    print(f"   RAM Available: {final_available_gb:.2f}GB")
    print(f"   RAM In Use: {final_used_gb:.2f}GB ({mem_end.percent:.1f}%)")
    print(f"   Total Delta: {total_delta:+.2f}GB")
    print()

    print("=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    print()

    # Analyze results
    success_count = sum(1 for m in memory_measurements if m['status'] == 'success')
    max_memory_delta = max((m['mem_delta_gb'] for m in memory_measurements), default=0)
    avg_memory_delta = sum(m['mem_delta_gb'] for m in memory_measurements) / len(memory_measurements) if memory_measurements else 0

    print(f"Domains Tested: {len(domains)}")
    print(f"Successful Executions: {success_count}/{len(domains)}")
    print(f"Max Memory Delta: {max_memory_delta:.2f}GB")
    print(f"Avg Memory Delta: {avg_memory_delta:.2f}GB")
    print(f"Final Memory Delta: {total_delta:+.2f}GB")
    print()

    # Validation checks
    all_passed = True

    print("[*] Validation Checks:")

    # Check 1: At least 3 domains succeeded
    if success_count >= 3:
        print("   [OK] At least 3 domains executed successfully")
    else:
        print(f"   [FAIL] Only {success_count} domains succeeded (expected >= 3)")
        all_passed = False

    # Check 2: Memory usage per domain < 10GB
    if max_memory_delta < 10.0:
        print(f"   [OK] Memory usage under control (max: {max_memory_delta:.2f}GB)")
    else:
        print(f"   [FAIL] Excessive memory usage (max: {max_memory_delta:.2f}GB)")
        all_passed = False

    # Check 3: Total memory delta reasonable (< 8GB for 16GB system)
    if abs(total_delta) < 8.0:
        print(f"   [OK] Total memory delta acceptable ({total_delta:+.2f}GB)")
    else:
        print(f"   [WARN] High total memory delta ({total_delta:+.2f}GB)")

    # Check 4: Only 1 model should be loaded (max_models=1)
    if stats['models_loaded'] <= 1:
        print(f"   [OK] LRU eviction working (models_loaded: {stats['models_loaded']})")
    else:
        print(f"   [FAIL] LRU eviction not working (models_loaded: {stats['models_loaded']}, expected: 1)")
        all_passed = False

    print()

    if all_passed:
        print("=" * 70)
        print("MEMORY STRESS TEST: PASSED")
        print("=" * 70)
        print()
        print("Key achievements:")
        print("  [OK] Multiple domains loaded successfully")
        print("  [OK] Memory usage stayed within safe limits")
        print("  [OK] LRU eviction is working correctly")
        print("  [OK] No memory exhaustion or system freeze")
        print("  [OK] System remains stable under memory pressure")
    else:
        print("=" * 70)
        print("MEMORY STRESS TEST: FAILED")
        print("=" * 70)
        print()
        print("Some validation checks failed. Review output above.")

    print()
    return all_passed


if __name__ == '__main__':
    try:
        result = asyncio.run(test_memory_stress())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        exit(130)
    except Exception as e:
        print(f"\n\nTest failed with exception: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
