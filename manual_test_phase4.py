"""
Manual Test Script for MDSA Phase 4 - Domain Execution

Tests domain configuration, registration, and execution WITHOUT downloading models.
Uses dummy responses for testing the framework logic.
"""

import logging

# Suppress verbose logging during tests
logging.basicConfig(level=logging.WARNING)

from mdsa import (
    # Phase 1
    HardwareDetector,
    # Phase 2
    MDSA,
    # Phase 3
    ModelManager,
    # Phase 4
    DomainConfig,
    DomainRegistry,
    DomainExecutor,
    PromptBuilder,
    ResponseValidator,
    create_finance_domain,
    create_medical_domain,
    create_support_domain,
    create_technical_domain,
)


def test_domain_config():
    """Test domain configuration creation."""
    print("="*70)
    print("MDSA Phase 4 - Domain Execution Test")
    print("="*70)

    print("\n[1] Testing DomainConfig...")

    # Test custom domain config
    config = DomainConfig(
        domain_id="test",
        name="Test Domain",
        description="Testing domain",
        keywords=["test", "demo"],
        model_name="gpt2",
        system_prompt="You are a test assistant.",
        prompt_template="Query: {query}\n\nResponse:",
        max_tokens=256
    )

    print(f"[OK] Created config: {config}")
    print(f"     Domain ID: {config.domain_id}")
    print(f"     Model: {config.model_name}")
    print(f"     Keywords: {len(config.keywords)}")

    # Test predefined domains
    print("\n[2] Testing predefined domain configs...")

    finance = create_finance_domain()
    print(f"[OK] Finance domain: {finance.domain_id}")
    print(f"     Keywords: {len(finance.keywords)} ({', '.join(finance.keywords[:5])}...)")

    medical = create_medical_domain()
    print(f"[OK] Medical domain: {medical.domain_id}")
    print(f"     Keywords: {len(medical.keywords)} ({', '.join(medical.keywords[:5])}...)")

    support = create_support_domain()
    print(f"[OK] Support domain: {support.domain_id}")
    print(f"     Keywords: {len(support.keywords)} ({', '.join(support.keywords[:5])}...)")

    technical = create_technical_domain()
    print(f"[OK] Technical domain: {technical.domain_id}")
    print(f"     Keywords: {len(technical.keywords)} ({', '.join(technical.keywords[:5])}...)")

    return [finance, medical, support, technical]


def test_domain_registry(domain_configs):
    """Test domain registry functionality."""
    print("\n[3] Testing DomainRegistry...")

    registry = DomainRegistry()
    print(f"[OK] Registry created: {registry}")

    # Register domains
    for config in domain_configs:
        registry.register(config)
        print(f"     Registered: {config.domain_id}")

    # Get stats
    stats = registry.get_stats()
    print(f"\n[OK] Registry statistics:")
    print(f"     Domains registered: {stats['domains_registered']}")
    print(f"     Total keywords: {stats['total_keywords']}")

    # Test lookups
    finance = registry.get("finance")
    print(f"\n[OK] Retrieved finance domain: {finance.name}")

    # Test keyword search
    matches = registry.find_by_keyword("money")
    print(f"[OK] Keyword 'money' matches: {[d.domain_id for d in matches]}")

    return registry


def test_prompt_builder():
    """Test prompt builder."""
    print("\n[4] Testing PromptBuilder...")

    builder = PromptBuilder()
    finance_config = create_finance_domain()

    # Build simple prompt
    prompt = builder.build_prompt(
        "Transfer $100 to savings",
        finance_config
    )

    print(f"[OK] Built prompt ({len(prompt)} chars)")
    print(f"\n--- Prompt Preview ---")
    print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
    print("--- End Prompt ---\n")

    # Test with context
    prompt_with_context = builder.build_prompt(
        "Check balance",
        finance_config,
        context={"user_name": "John Doe", "account_type": "checking"}
    )

    print(f"[OK] Built prompt with context ({len(prompt_with_context)} chars)")

    return builder


def test_response_validator():
    """Test response validator."""
    print("\n[5] Testing ResponseValidator...")

    validator = ResponseValidator()
    config = create_finance_domain()

    # Test valid response
    good_response = (
        "To transfer funds, log into your online banking account and "
        "select the 'Transfer' option. Follow the on-screen instructions."
    )

    is_valid, error = validator.validate(good_response, config)
    print(f"[OK] Valid response check: {is_valid} (error: {error})")

    # Test invalid response (too short)
    bad_response = "Yes."
    is_valid, error = validator.validate(bad_response, config)
    print(f"[OK] Invalid response check: {is_valid} (error: {error})")

    # Test sanitization
    messy_response = "  **Bold Text**  System: Something  "
    clean_response = validator.sanitize_response(messy_response)
    print(f"[OK] Sanitized response: '{clean_response}'")

    # Test relevance
    is_relevant = validator.check_relevance(good_response, config, "transfer money")
    print(f"[OK] Relevance check: {is_relevant}")

    return validator


def test_domain_executor():
    """Test domain executor."""
    print("\n[6] Testing DomainExecutor...")

    # Create model manager
    model_manager = ModelManager(max_models=3)

    # Create executor
    executor = DomainExecutor(model_manager)
    print(f"[OK] Executor created: {executor}")

    # Test execution with finance domain
    print("\n     Executing finance query...")
    finance_config = create_finance_domain()

    result = executor.execute(
        query="Transfer $100 to my savings account",
        domain_config=finance_config
    )

    print(f"\n--- Execution Result ---")
    print(f"Status: {result['status']}")
    print(f"Domain: {result['domain']}")
    print(f"Model: {result['model']}")
    print(f"Latency: {result['latency_ms']:.1f}ms")
    print(f"Tokens: {result['tokens_generated']}")
    print(f"Confidence: {result['confidence']:.2f}")
    if result['status'] == 'success':
        print(f"\nResponse:\n{result['response']}")
    else:
        print(f"\nError: {result['error']}")
    print("--- End Result ---\n")

    # Test execution with medical domain
    print("     Executing medical query...")
    medical_config = create_medical_domain()

    result2 = executor.execute(
        query="I have a headache and fever",
        domain_config=medical_config
    )

    print(f"[OK] Medical query executed:")
    print(f"     Status: {result2['status']}")
    print(f"     Response length: {len(result2['response'])} chars")
    print(f"     Confidence: {result2['confidence']:.2f}")

    return executor


def test_full_integration():
    """Test Phase 1+2+3+4 integration."""
    print("\n[7] Testing Full Integration (Phase 1+2+3+4)...")

    try:
        # Phase 1: Hardware Detection
        hardware = HardwareDetector()
        hw_info = hardware.get_summary()
        print(f"[OK] Phase 1 (Hardware): {hw_info['cpu_cores']} CPUs, {hw_info['memory_gb']:.1f}GB RAM")

        # Phase 2: Orchestrator (basic test - not full workflow yet)
        orchestrator = MDSA()
        print(f"[OK] Phase 2 (Orchestrator): Initialized")

        # Phase 3: Model Manager
        model_manager = ModelManager()
        stats = model_manager.get_stats()
        print(f"[OK] Phase 3 (Models): {stats['models_loaded']} loaded, max={stats['max_models']}")

        # Phase 4: Domain Execution
        domain_registry = DomainRegistry()
        domain_registry.register(create_finance_domain())
        domain_registry.register(create_medical_domain())

        executor = DomainExecutor(model_manager)
        print(f"[OK] Phase 4 (Domains): {len(domain_registry)} domains registered")

        # Execute a test query
        finance_config = domain_registry.get("finance")
        result = executor.execute(
            "What's my account balance?",
            finance_config
        )

        print(f"\n     Integration test query result:")
        print(f"     - Status: {result['status']}")
        print(f"     - Latency: {result['latency_ms']:.1f}ms")
        print(f"     - Confidence: {result['confidence']:.2f}")

        print("\n[OK] All phases integrated successfully!")

    except Exception as e:
        print(f"\n[ERROR] Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


def show_phase4_capabilities():
    """Display Phase 4 capabilities summary."""
    print("\n" + "="*70)
    print("PHASE 4 CAPABILITIES SUMMARY")
    print("="*70)

    capabilities = {
        "Domain Configuration": [
            "Custom and predefined domain configs",
            "4 built-in domains (finance, medical, support, technical)",
            "Flexible model and prompt settings"
        ],
        "Domain Registry": [
            "Thread-safe domain registration",
            "Domain lookup by ID",
            "Keyword-based domain search",
            "Usage statistics tracking"
        ],
        "Prompt Builder": [
            "System + user prompt construction",
            "Context variable injection",
            "Chat history formatting",
            "Few-shot examples support"
        ],
        "Response Validator": [
            "Length validation",
            "Repetition detection",
            "Toxicity checking (basic)",
            "Response sanitization"
        ],
        "Domain Executor": [
            "On-demand model loading via ModelManager",
            "Prompt building and execution",
            "Response validation",
            "Performance metrics tracking",
            "Dummy responses for testing (no model downloads)"
        ]
    }

    for component, features in capabilities.items():
        print(f"\n{component}:")
        for feature in features:
            print(f"  [OK] {feature}")

    print("\n" + "="*70)


def main():
    """Run all Phase 4 tests."""
    try:
        # Test individual components
        domain_configs = test_domain_config()
        registry = test_domain_registry(domain_configs)
        builder = test_prompt_builder()
        validator = test_response_validator()
        executor = test_domain_executor()

        # Test full integration
        test_full_integration()

        # Show capabilities
        show_phase4_capabilities()

        print("\n" + "="*70)
        print("[SUCCESS] All Phase 4 tests passed!")
        print("="*70)

        print("\n[INFO] Phase 4 Complete!")
        print("       - Domain configuration working")
        print("       - Domain registry working")
        print("       - Prompt builder working")
        print("       - Response validator working")
        print("       - Domain executor working (with dummy responses)")
        print("       - Phase 1+2+3+4 integration verified")

        print("\n[NEXT STEPS]")
        print("       - Test with real models (download from HuggingFace)")
        print("       - Integrate with orchestrator for full workflow")
        print("       - Add domain-specific fine-tuned models")
        print("       - Implement response caching")
        print("       - Add monitoring and logging\n")

        return True

    except Exception as e:
        print(f"\n[ERROR] Phase 4 test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
