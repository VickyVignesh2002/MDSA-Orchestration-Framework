"""
Simple RAG Functionality Test - Phase -1.4

Direct testing of RAG system without full MDSA imports.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Direct imports to avoid __init__.py issues
from mdsa.memory.dual_rag import DualRAG
from chatbot_app.medical_app.knowledge_base.enhanced_medical_kb import (
    initialize_medical_knowledge_base,
    ICD10_CODES,
    CPT_CODES,
    HCPCS_CODES,
    CLINICAL_GUIDELINES,
    CODING_DOMAIN_KNOWLEDGE,
    DIAGNOSIS_DOMAIN_KNOWLEDGE,
    RADIOLOGY_DOMAIN_KNOWLEDGE
)


def test_rag_system():
    """Test RAG system functionality"""
    print("\n" + "="*70)
    print("SIMPLE RAG FUNCTIONALITY TEST")
    print("="*70 + "\n")

    # Initialize
    print("[1/7] Initializing Dual RAG system...")
    dual_rag = DualRAG(max_global_docs=10000, max_local_docs=1000)
    print("  ✓ DualRAG initialized\n")

    # Populate
    print("[2/7] Populating medical knowledge base...")
    initialize_medical_knowledge_base(dual_rag)
    print("  ✓ Knowledge base populated\n")

    # Test 1: Check Global RAG population
    print("[3/7] Checking Global RAG population...")
    stats = dual_rag.get_stats()
    global_docs = stats['global_rag']['document_count']
    expected_docs = len(ICD10_CODES) + len(CPT_CODES) + len(HCPCS_CODES) + len(CLINICAL_GUIDELINES)

    print(f"  Expected: {expected_docs} documents")
    print(f"  Actual:   {global_docs} documents")

    if global_docs == expected_docs:
        print(f"  ✓ Global RAG correctly populated")
    else:
        print(f"  ✗ Document count mismatch!")

    print(f"\n  Breakdown:")
    print(f"    - ICD-10 codes:  {len(ICD10_CODES)}")
    print(f"    - CPT codes:     {len(CPT_CODES)}")
    print(f"    - HCPCS codes:   {len(HCPCS_CODES)}")
    print(f"    - Guidelines:    {len(CLINICAL_GUIDELINES)}")
    print(f"    - Total:         {expected_docs}\n")

    # Test 2: Test Global RAG retrieval
    print("[4/7] Testing Global RAG retrieval...")

    test_queries = [
        ("ICD-10", "Type 2 diabetes mellitus E11"),
        ("CPT", "office visit established patient"),
        ("HCPCS", "triamcinolone injection"),
        ("Guideline", "diabetes management HbA1c")
    ]

    passed = 0
    total = len(test_queries)

    for category, query in test_queries:
        result = dual_rag.global_rag.retrieve(query, top_k=3)
        docs_found = len(result.documents)
        latency = result.retrieval_time_ms

        if docs_found > 0:
            print(f"  ✓ {category}: Found {docs_found} docs ({latency:.1f}ms) - '{query[:35]}'")
            passed += 1
        else:
            print(f"  ✗ {category}: No docs found - '{query[:35]}'")

    print(f"\n  Result: {passed}/{total} queries successful ({passed/total*100:.1f}%)\n")

    # Test 3: Check Local RAG population
    print("[5/7] Checking Local RAG population...")

    expected_local = {
        "medical_coding": len(CODING_DOMAIN_KNOWLEDGE),
        "clinical_diagnosis": len(DIAGNOSIS_DOMAIN_KNOWLEDGE),
        "radiology_support": len(RADIOLOGY_DOMAIN_KNOWLEDGE),
        "biomedical_extraction": len(CODING_DOMAIN_KNOWLEDGE)
    }

    local_stats = stats['local_rags']
    all_correct = True

    for domain_id, expected_count in expected_local.items():
        if domain_id in local_stats:
            actual_count = local_stats[domain_id]['document_count']
            if actual_count == expected_count:
                print(f"  ✓ {domain_id}: {actual_count} docs")
            else:
                print(f"  ✗ {domain_id}: Expected {expected_count}, got {actual_count}")
                all_correct = False
        else:
            print(f"  ✗ {domain_id}: Not registered")
            all_correct = False

    if all_correct:
        print(f"\n  ✓ All Local RAGs correctly populated\n")
    else:
        print(f"\n  ✗ Some Local RAGs incorrectly populated\n")

    # Test 4: Test Local RAG retrieval
    print("[6/7] Testing Local RAG retrieval...")

    local_tests = [
        ("medical_coding", "ICD-10 coding best practices"),
        ("clinical_diagnosis", "differential diagnosis approach"),
        ("radiology_support", "chest imaging CPT codes")
    ]

    local_passed = 0
    local_total = len(local_tests)

    for domain_id, query in local_tests:
        result = dual_rag.retrieve(
            query=query,
            domain_id=domain_id,
            top_k=3,
            search_local=True,
            search_global=False
        )

        docs_found = len(result['local'].documents)
        latency = result['local'].retrieval_time_ms

        if docs_found > 0:
            print(f"  ✓ {domain_id}: Found {docs_found} docs ({latency:.1f}ms)")
            local_passed += 1
        else:
            print(f"  ✗ {domain_id}: No docs found")

    print(f"\n  Result: {local_passed}/{local_total} queries successful ({local_passed/local_total*100:.1f}%)\n")

    # Test 5: Test privacy isolation
    print("[7/7] Testing privacy isolation...")

    # Coding-specific query should NOT be found in diagnosis domain
    query = "ICD-10 coding best practices"

    coding_result = dual_rag.retrieve(
        query=query,
        domain_id="medical_coding",
        top_k=3,
        search_local=True,
        search_global=False
    )

    diagnosis_result = dual_rag.retrieve(
        query=query,
        domain_id="clinical_diagnosis",
        top_k=3,
        search_local=True,
        search_global=False
    )

    coding_docs = len(coding_result['local'].documents)
    diagnosis_docs = len(diagnosis_result['local'].documents)

    print(f"  Query: '{query}'")
    print(f"    - medical_coding Local RAG:    {coding_docs} docs")
    print(f"    - clinical_diagnosis Local RAG: {diagnosis_docs} docs")

    if coding_docs > 0 and diagnosis_docs == 0:
        print(f"  ✓ Privacy isolation working correctly\n")
        privacy_pass = True
    else:
        print(f"  ✗ Privacy isolation failed!\n")
        privacy_pass = False

    # Summary
    print("="*70)
    print("TEST SUMMARY")
    print("="*70 + "\n")

    all_tests = [
        ("Global RAG Population", global_docs == expected_docs),
        ("Global RAG Retrieval", passed == total),
        ("Local RAG Population", all_correct),
        ("Local RAG Retrieval", local_passed == local_total),
        ("Privacy Isolation", privacy_pass)
    ]

    total_passed = sum(1 for _, result in all_tests if result)
    total_tests = len(all_tests)

    for test_name, result in all_tests:
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
        exit_code = test_rag_system()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
