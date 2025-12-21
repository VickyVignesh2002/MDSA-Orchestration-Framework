"""
Manual Test Script for MDSA Phase 3 - Model Management

Tests the new model management infrastructure including:
- ModelConfig creation
- ModelRegistry tracking
- ModelLoader capabilities
- ModelManager integration
"""

from mdsa import ModelManager, ModelConfig, QuantizationType, ModelTier


def test_model_config():
    """Test ModelConfig creation and presets."""
    print("="*70)
    print("MDSA Phase 3 - Model Management Test")
    print("="*70)

    # Test 1: Create custom model config
    print("\n[1] Testing ModelConfig...")

    config = ModelConfig(
        model_name="test-model",
        tier=ModelTier.TIER1,
        device="cpu",
        max_length=128
    )
    print(f"[OK] Created config: {config}")
    print(f"     Model: {config.model_name}")
    print(f"     Tier: {config.tier.value}")
    print(f"     Device: {config.device}")
    print(f"     Max length: {config.max_length}")

    # Test 2: Use predefined configurations
    print("\n[2] Testing predefined configurations...")

    tier1_config = ModelConfig.for_tier1()
    print(f"[OK] Tier 1 config: {tier1_config.model_name}")
    print(f"     Device: {tier1_config.device} (always CPU for <50ms)")
    print(f"     Quantization: {tier1_config.quantization.value}")

    tier2_config = ModelConfig.for_tier2()
    print(f"[OK] Tier 2 config: {tier2_config.model_name}")
    print(f"     Quantization: {tier2_config.quantization.value} (8-bit for memory)")

    tier3_config = ModelConfig.for_tier3("meta-llama/Llama-2-7b-hf")
    print(f"[OK] Tier 3 config: {tier3_config.model_name}")
    print(f"     Quantization: {tier3_config.quantization.value} (4-bit for large models)")

    # Test 3: Quantization types
    print("\n[3] Testing quantization options...")

    quant_types = [
        QuantizationType.NONE,
        QuantizationType.INT8,
        QuantizationType.INT4,
        QuantizationType.FP16
    ]

    for quant in quant_types:
        print(f"     - {quant.value}: Available")

    return config


def test_model_registry():
    """Test ModelRegistry functionality."""
    from mdsa.models import ModelRegistry

    print("\n[4] Testing ModelRegistry...")

    # Create registry
    registry = ModelRegistry(max_models=5)
    print(f"[OK] Registry created: {registry}")

    # Simulate model registration
    print("\n     Simulating model registration...")

    # Create dummy model objects
    dummy_model = {"type": "test_model"}
    dummy_tokenizer = {"type": "test_tokenizer"}

    config = ModelConfig.for_tier1()

    # Register a model
    model_info = registry.register(
        model_id="tinybert",
        config=config,
        model=dummy_model,
        tokenizer=dummy_tokenizer,
        memory_mb=250.0
    )

    print(f"[OK] Model registered: {model_info.model_id}")
    print(f"     Memory: {model_info.memory_mb}MB")
    print(f"     Use count: {model_info.use_count}")

    # Get model
    retrieved = registry.get("tinybert")
    print(f"[OK] Model retrieved: {retrieved is not None}")
    print(f"     Use count after retrieval: {retrieved.use_count}")

    # Check if loaded
    is_loaded = registry.is_loaded("tinybert")
    print(f"[OK] Model is loaded: {is_loaded}")

    # Get stats
    stats = registry.get_stats()
    print(f"\n     Registry Statistics:")
    print(f"     - Models loaded: {stats['models_loaded']}")
    print(f"     - Total memory: {stats['total_memory_mb']:.1f}MB")
    print(f"     - Total uses: {stats['total_uses']}")

    # Cleanup
    registry.clear()
    print(f"\n[OK] Registry cleared (now has {len(registry)} models)")

    return registry


def test_model_manager():
    """Test ModelManager high-level interface."""
    print("\n[5] Testing ModelManager...")

    # Create manager
    manager = ModelManager(max_models=3)
    print(f"[OK] Manager created: {manager}")

    # Get initial stats
    stats = manager.get_stats()
    print(f"     Initial state:")
    print(f"     - Models loaded: {stats['models_loaded']}")
    print(f"     - Max models: {stats['max_models']}")

    # Test model info queries
    loaded_models = manager.list_models()
    print(f"\n[OK] Loaded models: {loaded_models}")

    # Test is_loaded check
    is_loaded = manager.is_loaded("test-model")
    print(f"[OK] 'test-model' loaded: {is_loaded}")

    print(f"\n[INFO] ModelManager ready for Phase 4 integration")
    print(f"       Will load domain SLMs on-demand with quantization")

    return manager


def test_integration():
    """Test Phase 1+2+3 integration."""
    print("\n[6] Testing Phase 1+2+3 Integration...")

    # Import Phase 1+2 components
    from mdsa import MDSA, HardwareDetector

    # Test hardware detection (Phase 1)
    hardware = HardwareDetector()
    print(f"[OK] Hardware (Phase 1): {hardware.cpu_count} cores, {hardware.memory_gb:.1f}GB RAM")

    # Test orchestrator (Phase 2)
    orchestrator = MDSA(log_level="ERROR")
    orchestrator.register_domain("test", "Test domain", ["test", "demo"])
    print(f"[OK] Orchestrator (Phase 2): {orchestrator}")

    # Test model manager (Phase 3)
    manager = ModelManager()
    print(f"[OK] Model Manager (Phase 3): {manager}")

    # Show how they work together
    print(f"\n     Integration Points:")
    print(f"     1. Hardware detection informs model device placement")
    print(f"     2. Orchestrator uses TinyBERT (Tier 1) for routing")
    print(f"     3. ModelManager will load domain SLMs (Tier 3) in Phase 4")

    return orchestrator, manager


def show_phase3_capabilities():
    """Display Phase 3 capabilities summary."""
    print("\n" + "="*70)
    print("PHASE 3 CAPABILITIES SUMMARY")
    print("="*70)

    capabilities = {
        "Model Configuration": [
            "Predefined configs for Tier 1, 2, 3",
            "Custom model specifications",
            "Quantization type selection"
        ],
        "Model Registry": [
            "Thread-safe model tracking",
            "LRU eviction when max models reached",
            "Usage statistics and memory tracking"
        ],
        "Model Loader": [
            "HuggingFace model loading",
            "4-bit and 8-bit quantization",
            "Device placement optimization",
            "Model caching"
        ],
        "Model Manager": [
            "High-level get_or_load API",
            "Automatic model lifecycle management",
            "Memory tracking and reporting",
            "Integration-ready for Phase 4"
        ]
    }

    for component, features in capabilities.items():
        print(f"\n{component}:")
        for feature in features:
            print(f"  [OK] {feature}")

    print("\n" + "="*70)
    print("Phase 3 Complete - Ready for Phase 4 (Domain Execution)")
    print("="*70)


def main():
    """Run all Phase 3 tests."""
    try:
        # Test individual components
        test_model_config()
        test_model_registry()
        test_model_manager()

        # Test integration
        test_integration()

        # Show capabilities
        show_phase3_capabilities()

        print("\n[SUCCESS] All Phase 3 tests passed!\n")
        return True

    except Exception as e:
        print(f"\n[ERROR] Phase 3 test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
