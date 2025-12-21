"""
Test RAG Functionality - Phase -1.4

Comprehensive testing of Global RAG and Local RAG systems:
1. Verify Global RAG populated with medical codes and guidelines
2. Test Global RAG retrieval (ICD-10, CPT, HCPCS)
3. Verify Local RAG populated for all domains
4. Test Local RAG domain-specific retrieval
5. Verify privacy isolation between domains
6. Test combined Local + Global retrieval
7. Measure retrieval performance

Usage:
    python test_rag_functionality.py

Expected Results:
    - Global RAG: 27 documents (10 ICD-10, 10 CPT, 3 HCPCS, 4 guidelines)
    - Local RAG per domain: 2-3 documents each
    - Retrieval latency: <50ms per query
    - Privacy: Domains cannot access other domains' Local RAG
"""

import sys
from pathlib import Path
from typing import Dict, List
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from mdsa.memory.dual_rag import DualRAG, RAGResult
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


# Test queries for different code types
TEST_QUERIES = {
    "icd10": [
        "Type 2 diabetes mellitus E11",
        "hypertension ICD-10 code",
        "COPD exacerbation",
        "chest pain diagnosis code",
        "chronic kidney disease stage 3"
    ],
    "cpt": [
        "office visit established patient",
        "comprehensive metabolic panel",
        "ECG electrocardiogram",
        "chest X-ray 2 views",
        "hemoglobin A1c test"
    ],
    "hcpcs": [
        "triamcinolone injection",
        "annual wellness visit",
        "blood glucose test strips"
    ],
    "guidelines": [
        "diabetes management HbA1c",
        "hypertension blood pressure target",
        "COPD exacerbation treatment",
        "chest pain evaluation workup"
    ],
    "domain_specific": {
        "medical_coding": [
            "ICD-10 coding best practices",
            "CPT modifiers",
            "medical necessity documentation"
        ],
        "clinical_diagnosis": [
            "differential diagnosis approach",
            "red flags chest pain headache"
        ],
        "radiology_support": [
            "chest imaging CPT codes",
            "radiology report structure"
        ],
        "biomedical_extraction": [
            "ICD-10 coding principles",
            "medical necessity"
        ]
    }
}


class RAGFunctionalityTester:
    """Comprehensive RAG testing suite"""

    def __init__(self):
        """Initialize RAG system and populate knowledge base"""
        print("[INIT] Initializing Dual RAG system...")
        self.dual_rag = DualRAG(max_global_docs=10000, max_local_docs=1000)

        print("[INIT] Populating medical knowledge base...")
        initialize_medical_knowledge_base(self.dual_rag)

        print("[INIT] RAG system ready!\n")

        # Test results storage
        self.results = {
            "global_rag_tests": [],
            "local_rag_tests": [],
            "privacy_tests": [],
            "performance_tests": [],
            "combined_tests": []
        }

    def run_all_tests(self):
        """Execute all RAG tests"""
        print("="*70)
        print("RAG FUNCTIONALITY TEST SUITE")
        print("="*70 + "\n")

        # Test 1: Verify Global RAG Population
        print("[TEST 1/7] Verifying Global RAG Population...")
        self.test_global_rag_population()
        print()

        # Test 2: Test Global RAG Retrieval
        print("[TEST 2/7] Testing Global RAG Retrieval...")
        self.test_global_rag_retrieval()
        print()

        # Test 3: Verify Local RAG Population
        print("[TEST 3/7] Verifying Local RAG Population...")
        self.test_local_rag_population()
        print()

        # Test 4: Test Local RAG Retrieval
        print("[TEST 4/7] Testing Local RAG Domain-Specific Retrieval...")
        self.test_local_rag_retrieval()
        print()

        # Test 5: Test Privacy Isolation
        print("[TEST 5/7] Testing Privacy Isolation Between Domains...")
        self.test_privacy_isolation()
        print()

        # Test 6: Test Combined Retrieval
        print("[TEST 6/7] Testing Combined Local + Global Retrieval...")
        self.test_combined_retrieval()
        print()

        # Test 7: Performance Testing
        print("[TEST 7/7] Testing Retrieval Performance...")
        self.test_retrieval_performance()
        print()

        # Print summary
        self.print_summary()

    def test_global_rag_population(self):
        """Test 1: Verify Global RAG is populated correctly"""
        stats = self.dual_rag.get_stats()
        global_stats = stats['global_rag']

        expected_docs = len(ICD10_CODES) + len(CPT_CODES) + len(HCPCS_CODES) + len(CLINICAL_GUIDELINES)
        actual_docs = global_stats['document_count']

        print(f"  Expected documents: {expected_docs}")
        print(f"  Actual documents:   {actual_docs}")

        if actual_docs == expected_docs:
            print(f"  ✓ Global RAG correctly populated")
            self.results["global_rag_tests"].append(("Population", True, f"{actual_docs} docs"))
        else:
            print(f"  ✗ Document count mismatch!")
            self.results["global_rag_tests"].append(("Population", False, f"Expected {expected_docs}, got {actual_docs}"))

        # Breakdown
        print(f"\n  Breakdown:")
        print(f"    - ICD-10 codes:       {len(ICD10_CODES)}")
        print(f"    - CPT codes:          {len(CPT_CODES)}")
        print(f"    - HCPCS codes:        {len(HCPCS_CODES)}")
        print(f"    - Clinical guidelines: {len(CLINICAL_GUIDELINES)}")
        print(f"    - Total:              {expected_docs}")

    def test_global_rag_retrieval(self):
        """Test 2: Test retrieval from Global RAG"""
        test_categories = {
            "ICD-10": TEST_QUERIES["icd10"],
            "CPT": TEST_QUERIES["cpt"],
            "HCPCS": TEST_QUERIES["hcpcs"],
            "Guidelines": TEST_QUERIES["guidelines"]
        }

        total_tests = 0
        passed_tests = 0

        for category, queries in test_categories.items():
            print(f"\n  Testing {category} retrieval:")
            for query in queries:
                result = self.dual_rag.global_rag.retrieve(
                    query=query,
                    top_k=3,
                    requesting_domain="test"
                )

                total_tests += 1
                found_docs = len(result.documents)

                if found_docs > 0:
                    print(f"    ✓ '{query[:40]}...' → {found_docs} docs ({result.retrieval_time_ms:.1f}ms)")
                    passed_tests += 1
                    self.results["global_rag_tests"].append((category, True, query))
                else:
                    print(f"    ✗ '{query[:40]}...' → No documents found")
                    self.results["global_rag_tests"].append((category, False, query))

        print(f"\n  Results: {passed_tests}/{total_tests} queries successful ({passed_tests/total_tests*100:.1f}%)")

    def test_local_rag_population(self):
        """Test 3: Verify Local RAG populated for all domains"""
        stats = self.dual_rag.get_stats()
        local_stats = stats['local_rags']

        expected_domains = {
            "medical_coding": len(CODING_DOMAIN_KNOWLEDGE),
            "clinical_diagnosis": len(DIAGNOSIS_DOMAIN_KNOWLEDGE),
            "radiology_support": len(RADIOLOGY_DOMAIN_KNOWLEDGE),
            "biomedical_extraction": len(CODING_DOMAIN_KNOWLEDGE)  # Shares coding knowledge
        }

        print(f"  Expected domains: {len(expected_domains)}")
        print(f"  Actual domains:   {len(local_stats)}")
        print()

        all_correct = True
        for domain_id, expected_count in expected_domains.items():
            if domain_id in local_stats:
                actual_count = local_stats[domain_id]['document_count']
                if actual_count == expected_count:
                    print(f"    ✓ {domain_id}: {actual_count} docs")
                    self.results["local_rag_tests"].append((domain_id, True, f"{actual_count} docs"))
                else:
                    print(f"    ✗ {domain_id}: Expected {expected_count}, got {actual_count}")
                    self.results["local_rag_tests"].append((domain_id, False, f"Expected {expected_count}, got {actual_count}"))
                    all_correct = False
            else:
                print(f"    ✗ {domain_id}: Domain not registered")
                self.results["local_rag_tests"].append((domain_id, False, "Not registered"))
                all_correct = False

        if all_correct:
            print(f"\n  ✓ All domains correctly populated")
        else:
            print(f"\n  ✗ Some domains have incorrect population")

    def test_local_rag_retrieval(self):
        """Test 4: Test domain-specific retrieval from Local RAG"""
        total_tests = 0
        passed_tests = 0

        for domain_id, queries in TEST_QUERIES["domain_specific"].items():
            print(f"\n  Testing {domain_id} Local RAG:")

            for query in queries:
                try:
                    result = self.dual_rag.retrieve(
                        query=query,
                        domain_id=domain_id,
                        top_k=3,
                        search_local=True,
                        search_global=False  # Only search local
                    )

                    total_tests += 1
                    found_docs = len(result['local'].documents)

                    if found_docs > 0:
                        print(f"    ✓ '{query[:35]}...' → {found_docs} docs ({result['local'].retrieval_time_ms:.1f}ms)")
                        passed_tests += 1
                        self.results["local_rag_tests"].append((f"{domain_id}_retrieval", True, query))
                    else:
                        print(f"    ✗ '{query[:35]}...' → No documents found")
                        self.results["local_rag_tests"].append((f"{domain_id}_retrieval", False, query))

                except Exception as e:
                    print(f"    ✗ Error: {str(e)}")
                    self.results["local_rag_tests"].append((f"{domain_id}_retrieval", False, str(e)))
                    total_tests += 1

        print(f"\n  Results: {passed_tests}/{total_tests} queries successful ({passed_tests/total_tests*100:.1f}%)")

    def test_privacy_isolation(self):
        """Test 5: Verify domains cannot access other domains' Local RAG"""
        print("  Testing cross-domain access prevention:")

        # Try to access medical_coding's local RAG from clinical_diagnosis
        query = "ICD-10 coding best practices"  # Specific to medical_coding

        # This query should find results in medical_coding's Local RAG
        coding_result = self.dual_rag.retrieve(
            query=query,
            domain_id="medical_coding",
            top_k=3,
            search_local=True,
            search_global=False
        )

        # But should NOT find results in clinical_diagnosis's Local RAG
        diagnosis_result = self.dual_rag.retrieve(
            query=query,
            domain_id="clinical_diagnosis",
            top_k=3,
            search_local=True,
            search_global=False
        )

        coding_docs = len(coding_result['local'].documents)
        diagnosis_docs = len(diagnosis_result['local'].documents)

        print(f"    - medical_coding Local RAG:    {coding_docs} docs found")
        print(f"    - clinical_diagnosis Local RAG: {diagnosis_docs} docs found")

        if coding_docs > 0 and diagnosis_docs == 0:
            print(f"    ✓ Privacy isolation working correctly")
            self.results["privacy_tests"].append(("Isolation", True, "Domains isolated"))
        else:
            print(f"    ✗ Privacy isolation failed!")
            self.results["privacy_tests"].append(("Isolation", False, "Cross-domain access detected"))

        # Test Global RAG is accessible by both
        print(f"\n  Testing Global RAG accessibility:")
        global_query = "Type 2 diabetes mellitus"

        coding_global = self.dual_rag.retrieve(
            query=global_query,
            domain_id="medical_coding",
            top_k=3,
            search_local=False,
            search_global=True
        )

        diagnosis_global = self.dual_rag.retrieve(
            query=global_query,
            domain_id="clinical_diagnosis",
            top_k=3,
            search_local=False,
            search_global=True
        )

        coding_global_docs = len(coding_global['global'].documents)
        diagnosis_global_docs = len(diagnosis_global['global'].documents)

        print(f"    - medical_coding → Global RAG:    {coding_global_docs} docs")
        print(f"    - clinical_diagnosis → Global RAG: {diagnosis_global_docs} docs")

        if coding_global_docs > 0 and diagnosis_global_docs > 0:
            print(f"    ✓ Global RAG accessible by all domains")
            self.results["privacy_tests"].append(("Global Access", True, "All domains can access"))
        else:
            print(f"    ✗ Global RAG access issue")
            self.results["privacy_tests"].append(("Global Access", False, "Access blocked"))

    def test_combined_retrieval(self):
        """Test 6: Test combined Local + Global retrieval"""
        print("  Testing combined retrieval (Local + Global):")

        test_cases = [
            ("medical_coding", "diabetes ICD-10 code E11"),
            ("clinical_diagnosis", "chest pain differential diagnosis"),
            ("radiology_support", "chest X-ray CPT code")
        ]

        for domain_id, query in test_cases:
            result = self.dual_rag.retrieve(
                query=query,
                domain_id=domain_id,
                top_k=3,
                search_local=True,
                search_global=True
            )

            local_docs = len(result['local'].documents)
            global_docs = len(result['global'].documents)
            total_docs = local_docs + global_docs

            local_time = result['local'].retrieval_time_ms
            global_time = result['global'].retrieval_time_ms

            print(f"\n    Domain: {domain_id}")
            print(f"    Query: '{query}'")
            print(f"    - Local RAG:  {local_docs} docs ({local_time:.1f}ms)")
            print(f"    - Global RAG: {global_docs} docs ({global_time:.1f}ms)")
            print(f"    - Total:      {total_docs} docs")

            if total_docs > 0:
                self.results["combined_tests"].append((domain_id, True, f"{total_docs} docs"))
            else:
                self.results["combined_tests"].append((domain_id, False, "No docs found"))

    def test_retrieval_performance(self):
        """Test 7: Measure retrieval performance"""
        print("  Performance benchmarks (target: <50ms per query):\n")

        queries = [
            "diabetes ICD-10",
            "office visit CPT",
            "chest pain evaluation",
            "hypertension management"
        ]

        # Test Global RAG performance
        print("    Global RAG:")
        global_times = []
        for query in queries:
            start = time.time()
            result = self.dual_rag.global_rag.retrieve(query, top_k=5)
            latency_ms = (time.time() - start) * 1000
            global_times.append(latency_ms)

            status = "✓" if latency_ms < 50 else "⚠"
            print(f"      {status} {latency_ms:.2f}ms - '{query}'")

        avg_global = sum(global_times) / len(global_times)
        print(f"      Average: {avg_global:.2f}ms")

        # Test Local RAG performance
        print("\n    Local RAG (medical_coding):")
        local_times = []
        for query in queries:
            start = time.time()
            result = self.dual_rag.local_rags["medical_coding"].retrieve(query, top_k=5)
            latency_ms = (time.time() - start) * 1000
            local_times.append(latency_ms)

            status = "✓" if latency_ms < 50 else "⚠"
            print(f"      {status} {latency_ms:.2f}ms - '{query}'")

        avg_local = sum(local_times) / len(local_times)
        print(f"      Average: {avg_local:.2f}ms")

        # Store performance results
        if avg_global < 50 and avg_local < 50:
            self.results["performance_tests"].append(("Latency", True, f"Global: {avg_global:.1f}ms, Local: {avg_local:.1f}ms"))
        else:
            self.results["performance_tests"].append(("Latency", False, f"Exceeds 50ms target"))

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70 + "\n")

        # Count total passed/failed
        all_results = (
            self.results["global_rag_tests"] +
            self.results["local_rag_tests"] +
            self.results["privacy_tests"] +
            self.results["combined_tests"] +
            self.results["performance_tests"]
        )

        total_tests = len(all_results)
        passed_tests = sum(1 for _, passed, _ in all_results if passed)

        print(f"Total tests: {total_tests}")
        print(f"Passed:      {passed_tests}")
        print(f"Failed:      {total_tests - passed_tests}")
        print(f"Success rate: {passed_tests/total_tests*100:.1f}%\n")

        # Category breakdown
        categories = [
            ("Global RAG Tests", self.results["global_rag_tests"]),
            ("Local RAG Tests", self.results["local_rag_tests"]),
            ("Privacy Tests", self.results["privacy_tests"]),
            ("Combined Retrieval Tests", self.results["combined_tests"]),
            ("Performance Tests", self.results["performance_tests"])
        ]

        for category_name, category_results in categories:
            if category_results:
                passed = sum(1 for _, p, _ in category_results if p)
                total = len(category_results)
                print(f"{category_name}: {passed}/{total} passed")

        # Show failures
        failures = [r for r in all_results if not r[1]]
        if failures:
            print(f"\n{'='*70}")
            print("FAILURES")
            print("="*70 + "\n")
            for test_name, _, details in failures:
                print(f"  ✗ {test_name}: {details}")

        # Overall status
        print(f"\n{'='*70}")
        if passed_tests == total_tests:
            print("✓ ALL TESTS PASSED!")
        else:
            print(f"⚠ {total_tests - passed_tests} TEST(S) FAILED")
        print("="*70)


def main():
    """Main test runner"""
    print("\n" + "#"*70)
    print("# RAG Functionality Test Suite")
    print("#")
    print("# Verifying Dual RAG System (Global + Local)")
    print("#"*70 + "\n")

    try:
        tester = RAGFunctionalityTester()
        tester.run_all_tests()

        # Exit code based on results
        all_results = (
            tester.results["global_rag_tests"] +
            tester.results["local_rag_tests"] +
            tester.results["privacy_tests"] +
            tester.results["combined_tests"] +
            tester.results["performance_tests"]
        )

        all_passed = all(passed for _, passed, _ in all_results)
        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
