"""
Test RAG via Integrated Medical Chatbot - Phase -1.4

Tests RAG functionality using the working enhanced_medical_chatbot_fixed.py
which has all imports properly configured.
"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))

# Import from the working chatbot application
import chatbot_app.medical_app.enhanced_medical_chatbot_fixed as chatbot_module


def test_rag_functionality():
    """Test RAG through the integrated chatbot"""
    print("\n" + "="*70)
    print("RAG FUNCTIONALITY TEST (via Integrated Chatbot)")
    print("="*70 + "\n")

    print("[1/5] Initializing Enhanced Medical Chatbot...")
    try:
        chatbot = chatbot_module.EnhancedMedicalChatbot(
            enable_reasoning=False,  # Disable reasoning for faster testing
            prefer_gpu=False  # Use CPU
        )
        print("  ✓ Chatbot initialized successfully\n")
    except Exception as e:
        print(f"  ✗ Failed to initialize chatbot: {e}")
        return 1

    # Test 1: Check Global RAG population
    print("[2/5] Checking Global RAG population...")
    try:
        global_rag = chatbot.dual_rag.global_rag
        doc_count = len(global_rag._documents)

        print(f"  Global RAG documents: {doc_count}")

        # Expected: 10 ICD-10 + 10 CPT + 3 HCPCS + 4 guidelines = 27
        if doc_count >= 25:  # Allow some flexibility
            print(f"  ✓ Global RAG appears populated (expected ~27 docs)\n")
            global_pass = True
        else:
            print(f"  ⚠ Global RAG may be under-populated (expected ~27 docs)\n")
            global_pass = False
    except Exception as e:
        print(f"  ✗ Error checking Global RAG: {e}\n")
        global_pass = False

    # Test 2: Check Local RAG population
    print("[3/5] Checking Local RAG population...")
    try:
        local_rags = chatbot.dual_rag.local_rags

        print(f"  Registered domains: {len(local_rags)}")

        local_pass = True
        for domain_id, local_rag in local_rags.items():
            doc_count = len(local_rag._documents)
            print(f"    - {domain_id}: {doc_count} docs")

            if doc_count == 0:
                local_pass = False

        if local_pass and len(local_rags) >= 4:
            print(f"  ✓ All Local RAGs populated\n")
        else:
            print(f"  ⚠ Some Local RAGs may be missing documents\n")
    except Exception as e:
        print(f"  ✗ Error checking Local RAG: {e}\n")
        local_pass = False

    # Test 3: Test Global RAG retrieval
    print("[4/5] Testing Global RAG retrieval...")
    test_queries = [
        "Type 2 diabetes E11.9",
        "office visit CPT 99213",
        "hypertension management"
    ]

    retrieval_pass = 0
    retrieval_total = len(test_queries)

    for query in test_queries:
        try:
            results = chatbot.dual_rag.retrieve(
                query=query,
                domain_id="medical_coding",  # Use any valid domain
                top_k=3,
                search_local=False,
                search_global=True
            )

            docs_found = len(results['global'].documents)
            latency = results['global'].retrieval_time_ms

            if docs_found > 0:
                print(f"  ✓ '{query[:35]}': {docs_found} docs ({latency:.1f}ms)")
                retrieval_pass += 1
            else:
                print(f"  ✗ '{query[:35]}': No docs found")
        except Exception as e:
            print(f"  ✗ '{query[:35]}': Error - {str(e)[:40]}")

    print(f"\n  Result: {retrieval_pass}/{retrieval_total} queries successful\n")

    # Test 4: Test combined retrieval (Local + Global)
    print("[5/5] Testing combined retrieval (Local + Global)...")

    combined_query = "diabetes ICD-10 code"

    try:
        results = chatbot.dual_rag.retrieve(
            query=combined_query,
            domain_id="medical_coding",
            top_k=3,
            search_local=True,
            search_global=True
        )

        local_docs = len(results['local'].documents)
        global_docs = len(results['global'].documents)

        print(f"  Query: '{combined_query}'")
        print(f"    - Local RAG:  {local_docs} docs")
        print(f"    - Global RAG: {global_docs} docs")
        print(f"    - Total:      {local_docs + global_docs} docs")

        if (local_docs + global_docs) > 0:
            print(f"  ✓ Combined retrieval working\n")
            combined_pass = True
        else:
            print(f"  ✗ No documents retrieved\n")
            combined_pass = False
    except Exception as e:
        print(f"  ✗ Error in combined retrieval: {e}\n")
        combined_pass = False

    # Summary
    print("="*70)
    print("TEST SUMMARY")
    print("="*70 + "\n")

    tests = [
        ("Global RAG Population", global_pass),
        ("Local RAG Population", local_pass),
        ("Global RAG Retrieval", retrieval_pass == retrieval_total),
        ("Combined Retrieval", combined_pass)
    ]

    total_passed = sum(1 for _, result in tests if result)
    total_tests = len(tests)

    for test_name, result in tests:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")

    print(f"\n  Total: {total_passed}/{total_tests} tests passed ({total_passed/total_tests*100:.1f}%)")

    if total_passed == total_tests:
        print("\n✓ ALL RAG TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠ {total_tests - total_passed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    try:
        exit_code = test_rag_functionality()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
