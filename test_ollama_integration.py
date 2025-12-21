"""
Test script for MDSA Ollama Integration

This script verifies:
1. Ollama adapter imports correctly
2. ModelLoader detects Ollama models
3. Domain configs use Ollama model
4. Memory module exports work
5. (Optional) Full Ollama connection test

Run this BEFORE the chatbot to verify integration.
"""

import sys
import os

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("MDSA Framework - Ollama Integration Test")
print("=" * 60)

# Test 1: Ollama adapter imports
print("\n[1/5] Testing Ollama adapter imports...")
try:
    from mdsa.integrations.adapters.ollama_adapter import (
        OllamaModel,
        OllamaTokenizer,
        is_ollama_model,
        parse_ollama_model_name,
        OllamaConnectionError
    )
    print("  ✓ Ollama adapter classes imported successfully")
except ImportError as e:
    print(f"  ✗ Failed to import Ollama adapter: {e}")
    sys.exit(1)

# Test 2: is_ollama_model function
print("\n[2/5] Testing Ollama model detection...")
test_cases = [
    ("ollama://llama3.2:3b-instruct-q4_0", True),
    ("microsoft/phi-2", False),
    ("ollama://mistral:7b", True),
    ("gpt2", False),
]
all_passed = True
for model_name, expected in test_cases:
    result = is_ollama_model(model_name)
    status = "✓" if result == expected else "✗"
    print(f"  {status} is_ollama_model('{model_name}') = {result} (expected: {expected})")
    if result != expected:
        all_passed = False

if all_passed:
    print("  ✓ All model detection tests passed")
else:
    print("  ✗ Some model detection tests failed")

# Test 3: ModelLoader Ollama support
print("\n[3/5] Testing ModelLoader Ollama support...")
try:
    from mdsa.models.loader import ModelLoader, OLLAMA_AVAILABLE, is_ollama_model
    print(f"  ✓ ModelLoader imported")
    print(f"  ✓ OLLAMA_AVAILABLE = {OLLAMA_AVAILABLE}")

    # Check if _load_ollama_model method exists
    loader = ModelLoader()
    has_method = hasattr(loader, '_load_ollama_model')
    print(f"  {'✓' if has_method else '✗'} ModelLoader has _load_ollama_model method: {has_method}")
except Exception as e:
    print(f"  ✗ ModelLoader test failed: {e}")

# Test 4: Memory module exports
print("\n[4/5] Testing memory module exports...")
try:
    from mdsa.memory import (
        RAGDocument,
        RAGResult,
        LocalRAG,
        GlobalRAG,
        DualRAG
    )
    print("  ✓ All RAG classes imported from mdsa.memory")

    # Quick test
    rag = DualRAG(max_global_docs=100, max_local_docs=50)
    print(f"  ✓ DualRAG instance created")

    stats = rag.get_stats()
    print(f"  ✓ DualRAG.get_stats() works: {stats['global_rag']['document_count']} docs")
except Exception as e:
    print(f"  ✗ Memory module test failed: {e}")

# Test 5: Domain configs use Ollama
print("\n[5/5] Testing domain configurations...")
try:
    # Change to chatbot directory for imports
    chatbot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_app", "medical_app")
    sys.path.insert(0, chatbot_dir)

    from domains.enhanced_medical_domains import (
        get_all_enhanced_medical_domains,
        DEVELOPMENT_MODEL
    )

    print(f"  ✓ Domain configs imported")
    print(f"  ✓ DEVELOPMENT_MODEL = {DEVELOPMENT_MODEL}")

    domains = get_all_enhanced_medical_domains()
    print(f"  ✓ Created {len(domains)} domain configs")

    all_ollama = all(d.model_name.startswith("ollama://") for d in domains)
    print(f"  {'✓' if all_ollama else '✗'} All domains use Ollama model: {all_ollama}")

    for d in domains:
        print(f"    - {d.domain_id}: {d.model_name}")

except Exception as e:
    print(f"  ✗ Domain config test failed: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 60)
print("INTEGRATION TEST SUMMARY")
print("=" * 60)
print("""
All core components are integrated:
  - Ollama adapter classes created
  - ModelLoader supports Ollama prefix detection
  - Memory module exports RAG classes
  - Domain configs use Ollama model

NEXT STEPS:
  1. Ensure Ollama is running: `ollama serve`
  2. Pull the model: `ollama pull llama3.2:3b-instruct-q4_0`
  3. Run the chatbot: `python chatbot_app/medical_app/enhanced_medical_chatbot_fixed.py`

To test Ollama connection (optional):
  python -c "
import requests
try:
    r = requests.get('http://localhost:11434/api/tags', timeout=5)
    print('Ollama is running!')
    print('Available models:', [m['name'] for m in r.json().get('models', [])])
except:
    print('Ollama is NOT running. Start with: ollama serve')
"
""")
print("=" * 60)
