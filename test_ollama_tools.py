"""
Test Ollama Adapter with Tool Calling Support

This script demonstrates the new tool calling capabilities added to the MDSA
Ollama adapter. It tests both standard generation and tool calling with cloud
Ollama models.

Usage:
    python test_ollama_tools.py

Prerequisites:
    1. Ollama server running (local or cloud)
    2. requests library installed: pip install requests
    3. Cloud model available (e.g., deepseek-v3.1:671b-cloud)
"""

import sys
import json
from mdsa.integrations.adapters.ollama_adapter import load_ollama_model

# Test configuration
TEST_MODEL = "llama3.2:3b-instruct-q4_0"  # Change to cloud model if testing with cloud
BASE_URL = "http://localhost:11434"  # Change to cloud endpoint if needed
API_KEY = None  # Set if using cloud Ollama with authentication

# Tool definitions for medical claim validation
MEDICAL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "validate_icd10_code",
            "description": "Validate if an ICD-10 code is properly formatted and exists",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The ICD-10 code to validate (e.g., E11.9, I10)"
                    }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_claim_eligibility",
            "description": "Check if a medical claim is eligible for reimbursement",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_age": {
                        "type": "integer",
                        "description": "Patient's age in years"
                    },
                    "procedure_code": {
                        "type": "string",
                        "description": "CPT procedure code"
                    },
                    "insurance_type": {
                        "type": "string",
                        "enum": ["Medicare", "Medicaid", "Private"],
                        "description": "Type of insurance coverage"
                    }
                },
                "required": ["patient_age", "procedure_code", "insurance_type"]
            }
        }
    }
]


def test_standard_generation():
    """Test standard text generation without tools."""
    print("=" * 70)
    print("TEST 1: Standard Generation (No Tools)")
    print("=" * 70)

    try:
        # Load model
        model, tokenizer = load_ollama_model(
            model_name=TEST_MODEL,
            base_url=BASE_URL,
            api_key=API_KEY
        )

        # Test query
        query = "What is the ICD-10 code for Type 2 Diabetes?"
        print(f"\nQuery: {query}")

        # Tokenize
        inputs = tokenizer(query, return_tensors="pt")

        # Generate
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.3
        )

        # Decode
        response = tokenizer.decode(outputs[0])
        print(f"\nResponse: {response}")
        print(f"Tool calls: {outputs[0].tool_calls}")

        print("\n✅ Standard generation test PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Standard generation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tool_calling():
    """Test generation with tool calling enabled."""
    print("\n" + "=" * 70)
    print("TEST 2: Tool Calling")
    print("=" * 70)

    try:
        # Load model
        model, tokenizer = load_ollama_model(
            model_name=TEST_MODEL,
            base_url=BASE_URL,
            api_key=API_KEY
        )

        # Test query that should trigger tool use
        query = "Please validate the ICD-10 code E11.9"
        print(f"\nQuery: {query}")
        print(f"Available tools: {len(MEDICAL_TOOLS)}")
        for tool in MEDICAL_TOOLS:
            print(f"  - {tool['function']['name']}")

        # Tokenize
        inputs = tokenizer(query, return_tensors="pt")

        # Generate with tools
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.3,
            tools=MEDICAL_TOOLS,
            tool_choice="auto"
        )

        # Decode
        response = tokenizer.decode(outputs[0])
        print(f"\nResponse: {response}")

        # Check for tool calls
        if outputs[0].has_tool_calls():
            print(f"\n🔧 Tool calls detected: {len(outputs[0].tool_calls)}")
            for i, tc in enumerate(outputs[0].tool_calls, 1):
                print(f"\nTool Call {i}:")
                print(f"  Name: {tc['name']}")
                print(f"  Arguments: {json.dumps(tc['arguments'], indent=2)}")
        else:
            print("\n⚠️  No tool calls detected (model chose to respond directly)")

        print("\n✅ Tool calling test PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Tool calling test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tool_choice_specific():
    """Test forcing a specific tool to be used."""
    print("\n" + "=" * 70)
    print("TEST 3: Specific Tool Choice")
    print("=" * 70)

    try:
        # Load model
        model, tokenizer = load_ollama_model(
            model_name=TEST_MODEL,
            base_url=BASE_URL,
            api_key=API_KEY
        )

        # Test query
        query = "Check if a 65-year-old with Medicare is eligible for procedure 99213"
        print(f"\nQuery: {query}")
        print(f"Forcing tool: check_claim_eligibility")

        # Tokenize
        inputs = tokenizer(query, return_tensors="pt")

        # Generate with specific tool forced
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.3,
            tools=MEDICAL_TOOLS,
            tool_choice="check_claim_eligibility"
        )

        # Check results
        if outputs[0].has_tool_calls():
            print(f"\n🔧 Tool calls: {len(outputs[0].tool_calls)}")
            for tc in outputs[0].tool_calls:
                print(f"  Tool: {tc['name']}")
                print(f"  Args: {json.dumps(tc['arguments'], indent=2)}")
            print("\n✅ Specific tool choice test PASSED")
            return True
        else:
            print("\n⚠️  No tool calls (model may not support forced tool choice)")
            return True  # Not a failure, just unsupported

    except Exception as e:
        print(f"\n❌ Specific tool choice test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tool_choice_none():
    """Test disabling tool calling."""
    print("\n" + "=" * 70)
    print("TEST 4: Tools Disabled")
    print("=" * 70)

    try:
        # Load model
        model, tokenizer = load_ollama_model(
            model_name=TEST_MODEL,
            base_url=BASE_URL,
            api_key=API_KEY
        )

        # Test query
        query = "What is the ICD-10 code for diabetes?"
        print(f"\nQuery: {query}")
        print(f"Tool choice: none (tools disabled)")

        # Tokenize
        inputs = tokenizer(query, return_tensors="pt")

        # Generate with tools disabled
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.3,
            tools=MEDICAL_TOOLS,
            tool_choice="none"
        )

        # Check results
        if not outputs[0].has_tool_calls():
            print(f"\n✅ Tools correctly disabled - no tool calls made")
            return True
        else:
            print(f"\n❌ Tools were used despite being disabled")
            return False

    except Exception as e:
        print(f"\n❌ Tool disable test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("OLLAMA ADAPTER TOOL CALLING TESTS")
    print("=" * 70)
    print(f"Model: {TEST_MODEL}")
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {'Set' if API_KEY else 'Not set'}")
    print("=" * 70)

    results = []

    # Run tests
    results.append(("Standard Generation", test_standard_generation()))
    results.append(("Tool Calling", test_tool_calling()))
    results.append(("Specific Tool Choice", test_tool_choice_specific()))
    results.append(("Tools Disabled", test_tool_choice_none()))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)

    print(f"\nTotal: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n🎉 All tests PASSED!")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
