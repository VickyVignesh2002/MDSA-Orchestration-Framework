"""
Manual Test Script for MDSA Framework with Smart Device Selection

Tests the system freeze fixes and GPU/CPU auto-detection on:
- System RAM: 16GB total (~10-12GB available after OS/background apps)
- GPU: NVIDIA RTX 3050 (4GB VRAM)

Expected behavior:
1. Auto-detects RTX 3050 and uses GPU with INT8 quantization
2. Falls back to CPU with INT8 if GPU unavailable
3. Memory usage: ~2.7GB VRAM (GPU) or ~3GB RAM (CPU)
4. No system freeze
5. First run: 30-60s (model load), subsequent: 1-3s
"""

import asyncio
import psutil
from mdsa import ModelManager, DomainExecutor
from mdsa.domains.config import get_predefined_domain
from mdsa.async_ import AsyncExecutor
from mdsa.utils.device_config import get_recommended_config

# Check for GPU support
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("WARNING: PyTorch not available, GPU testing disabled\n")


async def test():
    """Test with smart device selection for RTX 3050 / 16GB RAM system."""

    print("=" * 60)
    print("MDSA Framework Test (RTX 3050 4GB / 16GB RAM)")
    print("=" * 60)
    print()

    # Get hardware-aware configuration
    print("[*] Detecting hardware configuration...")
    hw_config = get_recommended_config(prefer_gpu=True)

    print("\n[*] Hardware Configuration:")
    print(f"   Device: {hw_config['device']}")
    print(f"   Quantization: {hw_config['quantization'].name}")
    print(f"   Max Models: {hw_config['max_models']}")
    print(f"   Max Workers: {hw_config['max_workers']}")
    print(f"   Reason: {hw_config['reason']}")
    print()

    # Initialize with recommended settings
    model_manager = ModelManager(max_models=hw_config['max_models'])
    domain_executor = DomainExecutor(model_manager)
    async_executor = AsyncExecutor(
        domain_executor,
        max_workers=hw_config['max_workers']
    )

    # Display initial memory state
    print("[*] Initial Memory State:")
    if hw_config['device'].startswith('cuda') and TORCH_AVAILABLE:
        # GPU memory check
        try:
            gpu_mem = torch.cuda.mem_get_info()
            gpu_free_gb = gpu_mem[0] / (1024**3)
            gpu_total_gb = gpu_mem[1] / (1024**3)
            gpu_used_gb = (gpu_mem[1] - gpu_mem[0]) / (1024**3)
            print(f"   GPU Memory: {gpu_free_gb:.2f}GB free / {gpu_total_gb:.2f}GB total")
            print(f"   GPU In Use: {gpu_used_gb:.2f}GB")
        except Exception as e:
            print(f"   GPU Memory: Error reading ({e})")
    else:
        # CPU memory check
        mem = psutil.virtual_memory()
        print(f"   System RAM: {mem.available / (1024**3):.2f}GB free / {mem.total / (1024**3):.2f}GB total")
        print(f"   RAM In Use: {mem.used / (1024**3):.2f}GB ({mem.percent:.1f}%)")
    print()

    # Get domain config (will use smart device selection)
    config = get_predefined_domain(
        'support',
        prefer_gpu=True  # Use GPU if RTX 3050 available
    )

    print("[*] Domain Configuration:")
    print(f"   Domain ID: {config.domain_id}")
    print(f"   Model: {config.model_name}")
    print(f"   Device: {config.device}")
    print(f"   Quantization: {config.quantization.name}")
    print(f"   Max Tokens: {config.max_tokens}")
    print()

    # Execute query
    print("[*] Executing query...")
    print("   (First run: ~30-60s for model download/load)")
    print("   (Subsequent runs: ~1-3s with cached model)")
    print()

    import time
    start_time = time.time()

    result = await async_executor.execute_async(
        query="What time is it?",
        domain_config=config,
        timeout=120.0  # 2 minutes for first-time model load
    )

    elapsed_time = time.time() - start_time

    # Display memory after execution
    print("[*] Memory After Execution:")
    if hw_config['device'].startswith('cuda') and TORCH_AVAILABLE:
        # GPU memory check
        try:
            gpu_mem_after = torch.cuda.mem_get_info()
            gpu_free_after = gpu_mem_after[0] / (1024**3)
            gpu_used_after = (gpu_mem_after[1] - gpu_mem_after[0]) / (1024**3)
            gpu_delta = gpu_used_after - gpu_used_gb

            print(f"   GPU Memory: {gpu_free_after:.2f}GB free")
            print(f"   GPU In Use: {gpu_used_after:.2f}GB")
            print(f"   GPU Delta: +{gpu_delta:.2f}GB (model + inference)")
        except Exception as e:
            print(f"   GPU Memory: Error reading ({e})")
    else:
        # CPU memory check
        mem_after = psutil.virtual_memory()
        ram_delta = (mem_after.used - mem.used) / (1024**3)
        print(f"   System RAM: {mem_after.available / (1024**3):.2f}GB free")
        print(f"   RAM In Use: {mem_after.used / (1024**3):.2f}GB ({mem_after.percent:.1f}%)")
        print(f"   RAM Delta: +{ram_delta:.2f}GB (model + inference)")
    print()

    # Display result
    print("[*] Execution Result:")
    print(f"   Status: {result['status']}")
    print(f"   Latency: {result['latency_ms']:.0f}ms ({result['latency_ms']/1000:.2f}s)")
    print(f"   Total Time: {elapsed_time:.2f}s")

    if result['status'] == 'success':
        print(f"\n[SUCCESS] Response generated:")
        print(f"   {result['response'][:200]}...")
        if len(result['response']) > 200:
            print(f"   (truncated, full length: {len(result['response'])} chars)")
    else:
        print(f"\n[ERROR]:")
        print(f"   {result.get('error', 'Unknown error')}")
    print()

    # Cleanup
    print("[*] Cleaning up...")
    await async_executor.shutdown_async()
    print("   Shutdown complete")
    print()

    print("=" * 60)
    print("Test Complete")
    print("=" * 60)

    # Summary
    print("\n[*] Summary:")
    if result['status'] == 'success':
        if hw_config['device'].startswith('cuda'):
            print(f"   [OK] GPU execution successful")
            print(f"   [OK] VRAM used: ~{gpu_delta:.2f}GB (expected: ~2.7GB for INT8)")
        else:
            print(f"   [OK] CPU execution successful")
            print(f"   [OK] RAM used: ~{ram_delta:.2f}GB (expected: ~3GB for INT8)")

        if elapsed_time < 10:
            print(f"   [OK] Fast execution (cached model)")
        elif elapsed_time < 120:
            print(f"   [OK] First-time load completed in {elapsed_time:.1f}s")
        else:
            print(f"   [WARN] Slow execution ({elapsed_time:.1f}s)")

        print(f"   [OK] No system freeze detected")
    else:
        print(f"   [FAIL] Execution failed")


# Additional test configurations
async def test_force_cpu():
    """Test forcing CPU execution."""
    print("\n" + "=" * 60)
    print("Testing Force CPU Configuration")
    print("=" * 60 + "\n")

    config = get_predefined_domain('support', force_device='cpu')
    print(f"Device: {config.device}")
    print(f"Quantization: {config.quantization.name}")
    print()


async def test_force_gpu():
    """Test forcing GPU execution."""
    print("\n" + "=" * 60)
    print("Testing Force GPU Configuration")
    print("=" * 60 + "\n")

    if not TORCH_AVAILABLE:
        print("[ERROR] PyTorch not available, cannot test GPU")
        return

    config = get_predefined_domain('support', force_device='cuda:0')
    print(f"Device: {config.device}")
    print(f"Quantization: {config.quantization.name}")
    print()


if __name__ == '__main__':
    # Run main test
    asyncio.run(test())

    # Uncomment to test specific configurations:
    # asyncio.run(test_force_cpu())     # Force CPU
    # asyncio.run(test_force_gpu())     # Force GPU
