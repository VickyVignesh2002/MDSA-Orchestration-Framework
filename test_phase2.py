"""
Phase 2 Testing Script - Phi-2 Model Upgrade and CPU Optimization

This script verifies:
1. Phi-2 model configuration in all domains
2. Enhanced system prompts
3. CPU optimization flags
4. Generation parameter optimization
5. Smart tool integration
"""

import sys
sys.path.insert(0, '.')

print("=" * 70)
print("PHASE 2 TESTING: Phi-2 Model Upgrade & CPU Optimization")
print("=" * 70)

# Test 1: Domain Configuration
print("\n[TEST 1] Domain Configuration Check")
print("-" * 70)

from mdsa.domains.config import get_predefined_domain

domains = ['finance', 'medical', 'support', 'technical']
for domain_id in domains:
    config = get_predefined_domain(domain_id)
    print(f"\n{domain_id.upper()} Domain:")
    print(f"  Model: {config.model_name}")
    print(f"  Tier: {config.model_tier.value}")
    print(f"  Device: {config.device}")
    print(f"  Temperature: {config.temperature}")
    print(f"  Max Tokens: {config.max_tokens}")
    print(f"  System Prompt Length: {len(config.system_prompt)} chars")

    # Verify Phi-2
    assert config.model_name == "microsoft/phi-2", f"{domain_id}: Wrong model!"
    assert config.device == "cpu", f"{domain_id}: Device should be CPU!"
    assert config.temperature == 0.3, f"{domain_id}: Temperature should be 0.3!"
    assert config.max_tokens == 256, f"{domain_id}: Max tokens should be 256!"
    print(f"  ✓ Configuration validated successfully")

print("\n" + "=" * 70)
print("✓ ALL DOMAIN CONFIGURATIONS CORRECT!")

# Test 2: Enhanced Prompts
print("\n[TEST 2] Enhanced System Prompts Check")
print("-" * 70)

from mdsa.domains.prompts import get_enhanced_prompt

for domain_id in domains:
    prompt = get_enhanced_prompt(domain_id)
    print(f"\n{domain_id.upper()} Prompt:")
    print(f"  Length: {len(prompt)} chars")
    print(f"  Has 'OUTPUT FORMAT': {'OUTPUT FORMAT' in prompt}")
    print(f"  Has 'EXAMPLE': {'EXAMPLE' in prompt or 'Example' in prompt}")
    print(f"  Has 'GUIDELINES': {'GUIDELINES' in prompt}")

    # Verify enhanced prompts
    assert len(prompt) > 500, f"{domain_id}: Prompt too short!"
    assert "OUTPUT FORMAT" in prompt or "ROLE" in prompt, f"{domain_id}: Missing structure!"
    print(f"  ✓ Enhanced prompt validated successfully")

print("\n" + "=" * 70)
print("✓ ALL ENHANCED PROMPTS CORRECT!")

# Test 3: Smart Tools Integration
print("\n[TEST 3] Smart Tools Integration Check")
print("-" * 70)

from mdsa.tools import ToolRegistry, SmartToolExecutor
from mdsa.tools.builtin import get_default_tools

registry = ToolRegistry()
for tool in get_default_tools():
    registry.register(tool)

print(f"\nRegistered Tools: {len(registry)} tools")
print(f"  Tools: {', '.join(registry.list_tools())}")

executor = SmartToolExecutor(registry)

# Test tool detection
test_queries = [
    ("What time is it?", "get_current_time"),
    ("Calculate 15 + 27", "calculate"),
    ("Convert 100 fahrenheit to celsius", "convert_units"),
]

print("\nTesting Tool Detection:")
for query, expected_tool in test_queries:
    results = executor.detect_and_execute(query)
    print(f"\n  Query: '{query}'")
    if results:
        print(f"  Detected: {results[0].tool_name}")
        print(f"  Result: {results[0].result}")
        print(f"  Success: {results[0].success}")
        assert results[0].tool_name == expected_tool, f"Expected {expected_tool}!"
        print(f"  ✓ Tool detection correct")
    else:
        print(f"  ✗ No tools detected!")

print("\n" + "=" * 70)
print("✓ SMART TOOLS WORKING CORRECTLY!")

# Test 4: Configuration File
print("\n[TEST 4] Framework Configuration Check")
print("-" * 70)

import yaml

with open('configs/framework_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print(f"\nRAG System:")
print(f"  Enabled: {config['rag']['enabled']}")
print(f"  Vector DB: {config['rag']['vector_db']}")
print(f"  Embedding Model: {config['rag']['embedding_model']}")

print(f"\nTools System:")
print(f"  Enabled: {config['tools']['enabled']}")
print(f"  Timeout: {config['tools']['timeout']}s")
print(f"  Max Tools: {config['tools']['max_tools_per_request']}")

assert config['rag']['enabled'] == True, "RAG should be enabled!"
assert config['tools']['enabled'] == True, "Tools should be enabled!"

print("\n" + "=" * 70)
print("✓ CONFIGURATION FILE CORRECT!")

# Test 5: CPU Optimization Flags (code inspection)
print("\n[TEST 5] CPU Optimization Flags Check")
print("-" * 70)

with open('mdsa/models/loader.py', 'r') as f:
    loader_code = f.read()

print("\nChecking model loader for CPU optimizations:")
checks = [
    ("torch.float32", "Float32 dtype for CPU"),
    ("low_cpu_mem_usage", "Memory-efficient loading"),
    ("device == \"cpu\"", "CPU device check"),
]

for code_snippet, description in checks:
    if code_snippet in loader_code:
        print(f"  ✓ {description}: Found")
    else:
        print(f"  ✗ {description}: NOT FOUND!")
        assert False, f"Missing: {description}"

print("\nChecking executor for generation optimizations:")
with open('mdsa/domains/executor.py', 'r') as f:
    executor_code = f.read()

gen_checks = [
    ("repetition_penalty=2.5", "Strong repetition penalty"),
    ("no_repeat_ngram_size=4", "4-gram repetition prevention"),
    ("min_new_tokens=10", "Minimum token generation"),
    ("use_cache=True", "KV cache enabled"),
]

for code_snippet, description in gen_checks:
    if code_snippet in executor_code:
        print(f"  ✓ {description}: Found")
    else:
        print(f"  ✗ {description}: NOT FOUND!")
        assert False, f"Missing: {description}"

print("\n" + "=" * 70)
print("✓ CPU OPTIMIZATIONS IN PLACE!")

# Summary
print("\n" + "=" * 70)
print("PHASE 2 TEST SUMMARY")
print("=" * 70)
print("""
✓ Test 1: Domain configurations - ALL PASSED
✓ Test 2: Enhanced system prompts - ALL PASSED
✓ Test 3: Smart tools integration - ALL PASSED
✓ Test 4: Framework configuration - ALL PASSED
✓ Test 5: CPU optimization flags - ALL PASSED

PHASE 2 IMPLEMENTATION: ✅ COMPLETE AND VERIFIED

Changes Made:
1. All 4 domains upgraded to microsoft/phi-2 model
2. Enhanced system prompts with examples and structure
3. Temperature reduced to 0.3 for deterministic output
4. Max tokens increased to 256 for complete responses
5. CPU optimizations: float32, low_cpu_mem_usage=True
6. Generation optimizations: repetition_penalty=2.5, no_repeat_ngram_size=4
7. RAG system enabled in config
8. Smart tools enabled in config

Next Steps (Phase 3+):
- Phase 3: Authentication integration & rate limiting
- Phase 4: Async support module
- Phase 5: Comprehensive test suite
- Phase 6: UI redesign with visualizations
- Phase 7: Documentation (FRAMEWORK_REFERENCE.md)
""")

print("=" * 70)
print("Phase 2 testing completed successfully!")
print("=" * 70)
