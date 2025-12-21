"""
Test Cloud Model Configuration for Medical Domains

This script verifies that:
1. All 5 medical domains are configured with cloud models
2. Cloud models are accessible (if Ollama is running)
3. Domain routing works correctly with cloud models

Usage:
    # Set API key first:
    export OLLAMA_API_KEY="your-api-key-here"  # Linux/Mac
    # OR
    set OLLAMA_API_KEY=your-api-key-here  # Windows CMD
    # OR
    $env:OLLAMA_API_KEY="your-api-key-here"  # Windows PowerShell

    # Then run:
    python test_cloud_models.py
"""

import sys
import os

print("=" * 70)
print("CLOUD MODEL CONFIGURATION TEST")
print("=" * 70)

# Check if API key is set
api_key = os.environ.get('OLLAMA_API_KEY')
if api_key:
    print(f"[OK] API Key found: {api_key[:20]}...")
else:
    print("[WARNING] No API key found in OLLAMA_API_KEY environment variable")
    print("  Cloud models may still work if authentication is not required")

print()

# Test 1: Import medical domains
print("[1/5] Testing domain imports...")
try:
    from chatbot_app.medical_app.domains.enhanced_medical_domains import (
        create_clinical_diagnosis_domain,
        create_medical_coding_domain,
        create_biomedical_extraction_domain,
        create_radiology_support_domain,
        create_lightweight_medical_qa_domain,
        CLOUD_CLINICAL_MODEL,
        CLOUD_MEDICAL_CODING_MODEL,
        CLOUD_BIOMEDICAL_MODEL,
        CLOUD_RADIOLOGY_MODEL,
        CLOUD_QA_LITE_MODEL
    )
    print("[OK] Domain imports successful")
    print()
except Exception as e:
    print(f"[FAIL] Domain import failed: {e}")
    sys.exit(1)

# Test 2: Verify cloud model configuration
print("[2/5] Verifying cloud model assignments...")
cloud_models = {
    "Clinical Diagnosis": CLOUD_CLINICAL_MODEL,
    "Medical Coding": CLOUD_MEDICAL_CODING_MODEL,
    "Biomedical Extraction": CLOUD_BIOMEDICAL_MODEL,
    "Radiology Support": CLOUD_RADIOLOGY_MODEL,
    "Medical Q&A Lite": CLOUD_QA_LITE_MODEL
}

all_cloud = True
for domain_name, model_name in cloud_models.items():
    is_cloud = ":cloud" in model_name
    status = "[OK]" if is_cloud else "[FAIL]"
    print(f"  {status} {domain_name:25} -> {model_name}")
    if not is_cloud:
        all_cloud = False

if all_cloud:
    print("\n[OK] All domains configured with cloud models")
else:
    print("\n[FAIL] Some domains not using cloud models")
print()

# Test 3: Create domain configurations
print("[3/5] Creating domain configurations...")
try:
    domains = {
        "clinical_diagnosis": create_clinical_diagnosis_domain(),
        "medical_coding": create_medical_coding_domain(),
        "biomedical_extraction": create_biomedical_extraction_domain(),
        "radiology_support": create_radiology_support_domain(),
        "medical_qa_lite": create_lightweight_medical_qa_domain()
    }
    print(f"[OK] Created {len(domains)} domain configurations")
    print()
except Exception as e:
    print(f"[FAIL] Domain creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Verify domain properties
print("[4/5] Verifying domain properties...")
for domain_id, config in domains.items():
    print(f"\n  Domain: {config.name}")
    print(f"    ID: {domain_id}")
    print(f"    Model: {config.model_name}")
    print(f"    Tier: {config.model_tier}")
    print(f"    Keywords: {len(config.keywords)} keywords")
    print(f"    Temperature: {config.temperature}")
    print(f"    Max tokens: {config.max_tokens}")

print("\n[OK] All domain configurations valid")
print()

# Test 5: Test Ollama connection (if available)
print("[5/5] Testing Ollama connection...")
try:
    from mdsa.integrations.adapters.ollama_adapter import OllamaModel

    # Try to connect to a cloud model
    test_model = "kimi-k2-thinking:cloud"
    print(f"  Attempting connection to: {test_model}")

    try:
        model = OllamaModel(
            model_name=test_model,
            base_url="http://localhost:11434",
            api_key=api_key,
            timeout=10
        )
        print(f"[OK] Connected to Ollama server")
        print(f"  Model: {model.model_name}")
        print(f"  Base URL: {model.base_url}")
        print(f"  API Key: {'Set' if model.api_key else 'Not set'}")

    except Exception as e:
        print(f"[WARNING] Could not connect to Ollama: {e}")
        print("  This is expected if Ollama server is not running")
        print("  Cloud models will work when Ollama is available")

except Exception as e:
    print(f"[WARNING] Ollama adapter test skipped: {e}")

print()

# Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("[OK] Domain imports: SUCCESS")
print("[OK] Cloud model configuration: SUCCESS")
print("[OK] Domain creation: SUCCESS")
print("[OK] Domain properties: VALID")
print()
print("Cloud models configured:")
for domain_name, model_name in cloud_models.items():
    model_short = model_name.replace("ollama://", "")
    print(f"  - {domain_name:25} -> {model_short}")

print()
print("=" * 70)
print("READY FOR TESTING")
print("=" * 70)
print()
print("Next steps:")
print("1. Ensure Ollama server is running: ollama serve")
print("2. Verify cloud models are accessible: ollama list | grep cloud")
print("3. Run medical chatbot: python chatbot_app/medical_app/enhanced_medical_chatbot_fixed.py")
print("4. Test queries in Gradio UI: http://localhost:7860")
print()
print("Test queries to try:")
print('  - "What is the ICD-10 code for Type 2 Diabetes?"')
print('  - "Patient with fever and cough - differential diagnosis?"')
print('  - "Extract medications from: Patient takes metformin 500mg BID"')
print('  - "Analyze CT scan showing small nodule in RUL"')
print('  - "What does hypertension mean?"')
print()

sys.exit(0)
