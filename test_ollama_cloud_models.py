"""
Test Ollama Cloud Models for MDSA Framework

This script verifies that all 5 Ollama cloud models are:
1. Accessible and can generate responses
2. Working with the MDSA Ollama adapter
3. Support tool calling (if applicable)

Cloud Models:
- kimi-k2-thinking:cloud (Medical coding - precise reasoning)
- deepseek-v3.1:671b-cloud (Clinical diagnosis - 671B params)
- qwen3-coder:480b-cloud (Biomedical extraction - structured data)
- qwen3-vl:235b-instruct-cloud (Radiology - vision-language)
- gpt-oss:120b-cloud (Medical Q&A - general purpose)

Usage:
    python test_ollama_cloud_models.py

Prerequisites:
    - Ollama server running (ollama serve)
    - Access to cloud models (may require API key)
"""

import os
import sys
import time
import io
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from mdsa.integrations.adapters.ollama_adapter import (
    OllamaModel,
    OllamaConnectionError,
    OllamaGenerationError
)


# Cloud model definitions
CLOUD_MODELS = {
    "medical_coding": {
        "name": "kimi-k2-thinking:cloud",
        "description": "Precise reasoning for medical coding",
        "test_prompt": "What ICD-10 code should I use for Type 2 diabetes mellitus without complications?",
        "expected_contains": ["E11", "diabet"]
    },
    "clinical_diagnosis": {
        "name": "deepseek-v3.1:671b-cloud",
        "description": "Complex medical reasoning (671B params)",
        "test_prompt": "What are the differential diagnoses for a patient with chest pain and dyspnea?",
        "expected_contains": ["diagnos", "chest"]
    },
    "biomedical_extraction": {
        "name": "qwen3-coder:480b-cloud",
        "description": "Structured data extraction",
        "test_prompt": "Extract medications from this note: Patient takes metformin 500mg BID and lisinopril 10mg daily.",
        "expected_contains": ["metformin", "lisinopril"]
    },
    "radiology": {
        "name": "qwen3-vl:235b-instruct-cloud",
        "description": "Vision-language for imaging reports",
        "test_prompt": "Interpret this radiology finding: Small nodule in right upper lobe measuring 4mm.",
        "expected_contains": ["nodule", "lung"]
    },
    "medical_qa": {
        "name": "gpt-oss:120b-cloud",
        "description": "General medical Q&A",
        "test_prompt": "What is hemoglobin A1c and why is it important?",
        "expected_contains": ["hemoglobin", "diabet"]
    }
}

# Tool definition for testing tool calling
TEST_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform basic arithmetic calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The arithmetic operation to perform"
                    },
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["operation", "a", "b"]
            }
        }
    }
]


def test_model(model_info: dict, test_tools: bool = False) -> dict:
    """
    Test a single Ollama cloud model.

    Args:
        model_info: Dictionary with model configuration
        test_tools: Whether to test tool calling

    Returns:
        Dictionary with test results
    """
    model_name = model_info["name"]
    print(f"\n{'='*70}")
    print(f"Testing: {model_name}")
    print(f"Description: {model_info['description']}")
    print(f"{'='*70}")

    results = {
        "model": model_name,
        "connection": False,
        "generation": False,
        "tool_calling": None,
        "latency_ms": 0,
        "response": "",
        "error": None
    }

    try:
        # 1. Initialize model
        print(f"\n[1/4] Initializing model...")
        start_time = time.time()

        # Check for API key in environment
        api_key = os.environ.get("OLLAMA_API_KEY")
        if api_key:
            print(f"  ✓ Using API key from environment")

        model = OllamaModel(
            model_name=model_name,
            base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
            timeout=300,  # 5 minutes for cloud models
            api_key=api_key
        )
        results["connection"] = True
        print(f"  ✓ Model initialized successfully")

        # 2. Test standard generation
        print(f"\n[2/4] Testing standard text generation...")
        print(f"  Prompt: {model_info['test_prompt'][:60]}...")

        # Ollama adapter accepts string directly as input_ids
        outputs = model.generate(
            input_ids=model_info['test_prompt'],  # Pass string directly
            max_new_tokens=200,
            temperature=0.3
        )

        # Extract response text from outputs
        if outputs and len(outputs) > 0:
            response = outputs[0].text if hasattr(outputs[0], 'text') else str(outputs[0])
        else:
            response = ""

        latency_ms = (time.time() - start_time) * 1000

        results["generation"] = True
        results["latency_ms"] = round(latency_ms, 2)
        results["response"] = response

        print(f"  ✓ Generation successful")
        print(f"  ✓ Latency: {latency_ms:.2f}ms")
        print(f"  ✓ Response length: {len(response)} characters")
        print(f"\n  Response preview:")
        print(f"  {response[:200]}...")

        # Check if expected keywords are in response
        response_lower = response.lower()
        found_keywords = [
            kw for kw in model_info["expected_contains"]
            if kw.lower() in response_lower
        ]

        if found_keywords:
            print(f"  ✓ Found expected keywords: {found_keywords}")
        else:
            print(f"  ⚠ Expected keywords not found: {model_info['expected_contains']}")

        # 3. Test tool calling (optional)
        if test_tools:
            print(f"\n[3/4] Testing tool calling support...")
            try:
                tool_prompt = "What is 15 multiplied by 7? Use the calculate function."

                tool_outputs = model.generate(
                    input_ids=tool_prompt,  # Pass string directly
                    max_new_tokens=100,
                    temperature=0.1,
                    tools=TEST_TOOLS,
                    tool_choice="auto"
                )

                if tool_outputs[0].has_tool_calls():
                    tool_calls = tool_outputs[0].tool_calls
                    print(f"  ✓ Tool calling supported")
                    print(f"  ✓ Tool calls made: {len(tool_calls)}")
                    for tc in tool_calls:
                        print(f"    - Function: {tc['name']}")
                        print(f"      Arguments: {tc['arguments']}")
                    results["tool_calling"] = True
                else:
                    print(f"  ⚠ Tool calling not used (may not be supported by this model)")
                    results["tool_calling"] = False

            except Exception as e:
                print(f"  ⚠ Tool calling test failed: {str(e)}")
                results["tool_calling"] = False
        else:
            print(f"\n[3/4] Skipping tool calling test")
            results["tool_calling"] = "skipped"

        print(f"\n[4/4] Test complete ✓")

    except OllamaConnectionError as e:
        results["error"] = f"Connection error: {str(e)}"
        print(f"\n✗ Connection Error: {str(e)}")

    except OllamaGenerationError as e:
        results["error"] = f"Generation error: {str(e)}"
        print(f"\n✗ Generation Error: {str(e)}")

    except Exception as e:
        results["error"] = f"Unexpected error: {str(e)}"
        print(f"\n✗ Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()

    return results


def print_summary(all_results: list):
    """Print test summary."""
    print(f"\n\n{'='*70}")
    print(f"TEST SUMMARY")
    print(f"{'='*70}\n")

    total = len(all_results)
    connected = sum(1 for r in all_results if r["connection"])
    generated = sum(1 for r in all_results if r["generation"])
    tool_support = sum(1 for r in all_results if r["tool_calling"] is True)

    print(f"Total models tested: {total}")
    print(f"Successfully connected: {connected}/{total}")
    print(f"Successfully generated: {generated}/{total}")
    print(f"Tool calling support: {tool_support}/{total}")

    print(f"\n{'Model':<35} {'Status':<15} {'Latency':<12} {'Tools'}")
    print(f"{'-'*35} {'-'*15} {'-'*12} {'-'*8}")

    for result in all_results:
        model_name = result["model"].split(':')[0][:33]  # Shorten name
        status = "✓ Working" if result["generation"] else "✗ Failed"
        latency = f"{result['latency_ms']:.2f}ms" if result["latency_ms"] > 0 else "N/A"
        tools = "✓" if result["tool_calling"] is True else ("✗" if result["tool_calling"] is False else "-")

        print(f"{model_name:<35} {status:<15} {latency:<12} {tools}")

    # Show errors
    errors = [r for r in all_results if r["error"]]
    if errors:
        print(f"\n{'='*70}")
        print(f"ERRORS")
        print(f"{'='*70}\n")
        for result in errors:
            print(f"Model: {result['model']}")
            print(f"Error: {result['error']}\n")


def main():
    """Main test runner."""
    print(f"\n{'#'*70}")
    print(f"# Ollama Cloud Models Test Suite")
    print(f"#")
    print(f"# Testing {len(CLOUD_MODELS)} cloud models for MDSA framework")
    print(f"{'#'*70}\n")

    # Check environment
    print(f"Environment:")
    print(f"  OLLAMA_BASE_URL: {os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434 (default)')}")
    print(f"  OLLAMA_API_KEY: {'Set' if os.environ.get('OLLAMA_API_KEY') else 'Not set'}")

    # Test each model
    all_results = []
    for domain_id, model_info in CLOUD_MODELS.items():
        result = test_model(model_info, test_tools=(domain_id == "medical_coding"))  # Test tools on one model
        all_results.append(result)

        # Short pause between models
        time.sleep(1)

    # Print summary
    print_summary(all_results)

    # Exit code
    all_passed = all(r["generation"] for r in all_results)
    if all_passed:
        print(f"\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ Some tests failed. Check errors above.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\nTest interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
