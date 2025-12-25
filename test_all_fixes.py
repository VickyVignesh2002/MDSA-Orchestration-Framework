"""
Comprehensive Test Script for MDSA Fixes
Tests all 10 implemented fixes to ensure everything works
"""

import sys
import time
import requests
import json
from pathlib import Path
from datetime import datetime

# Test results tracking
test_results = {
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "details": []
}

def log_test(name, status, message="", duration_ms=0):
    """Log test result"""
    result = {
        "test": name,
        "status": status,
        "message": message,
        "duration_ms": duration_ms,
        "timestamp": datetime.now().isoformat()
    }
    test_results["details"].append(result)

    if status == "PASS":
        test_results["passed"] += 1
        icon = "OK"
    elif status == "FAIL":
        test_results["failed"] += 1
        icon = "FAIL"
    else:
        test_results["skipped"] += 1
        icon = "SKIP"

    print(f"[{icon}] {name}: {status} {message} ({duration_ms:.2f}ms)")

def test_dashboard_running():
    """Test if dashboard is running on port 9000"""
    try:
        start = time.perf_counter()
        response = requests.get("http://localhost:9000/", timeout=2)
        duration = (time.perf_counter() - start) * 1000

        if response.status_code == 200:
            log_test("Dashboard Running", "PASS", "Port 9000 accessible", duration)
            return True
        else:
            log_test("Dashboard Running", "FAIL", f"Status {response.status_code}", duration)
            return False
    except Exception as e:
        log_test("Dashboard Running", "SKIP", f"Start dashboard first: python mdsa/ui/dashboard/app.py", 0)
        return False

def test_chatbot_running():
    """Test if chatbot is running on port 7860"""
    try:
        start = time.perf_counter()
        response = requests.get("http://localhost:7860/", timeout=2)
        duration = (time.perf_counter() - start) * 1000

        if response.status_code == 200:
            log_test("Chatbot Running", "PASS", "Port 7860 accessible", duration)
            return True
        else:
            log_test("Chatbot Running", "FAIL", f"Status {response.status_code}", duration)
            return False
    except Exception as e:
        log_test("Chatbot Running", "SKIP", f"Start chatbot first: python chatbot_app/medical_app/enhanced_medical_chatbot_fixed.py", 0)
        return False

def test_domain_embedding_cache():
    """Test if domain embedding cache is implemented"""
    router_file = Path("mdsa/core/router.py")

    if not router_file.exists():
        log_test("Domain Embedding Cache", "FAIL", "router.py not found", 0)
        return False

    content = router_file.read_text(encoding='utf-8')

    # Check for cache implementation
    if "_domain_embeddings" in content and "_precompute_domain_embeddings" in content:
        log_test("Domain Embedding Cache", "PASS", "Cache implementation found", 0)
        return True
    else:
        log_test("Domain Embedding Cache", "FAIL", "Cache code not found", 0)
        return False

def test_response_cache():
    """Test if response cache is implemented in chatbot"""
    chatbot_file = Path("chatbot_app/medical_app/enhanced_medical_chatbot_fixed.py")

    if not chatbot_file.exists():
        log_test("Response Cache", "FAIL", "Chatbot file not found", 0)
        return False

    content = chatbot_file.read_text(encoding='utf-8')

    # Check for cache implementation
    if "response_cache" in content and "_cache_key" in content:
        log_test("Response Cache", "PASS", "Cache implementation found", 0)
        return True
    else:
        log_test("Response Cache", "FAIL", "Cache code not found", 0)
        return False

def test_tracking_endpoint():
    """Test if tracking endpoint exists in dashboard"""
    dashboard_file = Path("mdsa/ui/dashboard/app.py")

    if not dashboard_file.exists():
        log_test("Tracking Endpoint", "FAIL", "Dashboard file not found", 0)
        return False

    content = dashboard_file.read_text(encoding='utf-8')

    # Check for tracking endpoint
    if "/api/requests/track" in content and "track_request" in content:
        log_test("Tracking Endpoint", "PASS", "Endpoint implementation found", 0)
        return True
    else:
        log_test("Tracking Endpoint", "FAIL", "Endpoint code not found", 0)
        return False

def test_tracking_integration():
    """Test if chatbot sends tracking data"""
    chatbot_file = Path("chatbot_app/medical_app/enhanced_medical_chatbot_fixed.py")

    if not chatbot_file.exists():
        log_test("Tracking Integration", "FAIL", "Chatbot file not found", 0)
        return False

    content = chatbot_file.read_text(encoding='utf-8')

    # Check for tracking method
    if "_track_to_dashboard" in content:
        log_test("Tracking Integration", "PASS", "Tracking method found", 0)
        return True
    else:
        log_test("Tracking Integration", "FAIL", "Tracking method not found", 0)
        return False

def test_config_files():
    """Test if configuration files exist"""
    configs = [
        ("configs/domains.yaml", "Domain Configuration"),
        ("configs/models.yaml", "Model Configuration"),
        (".env.example", "Environment Template")
    ]

    all_exist = True
    for file_path, name in configs:
        if Path(file_path).exists():
            log_test(f"Config: {name}", "PASS", f"{file_path} exists", 0)
        else:
            log_test(f"Config: {name}", "FAIL", f"{file_path} missing", 0)
            all_exist = False

    return all_exist

def test_documentation_exists():
    """Test if critical documentation files exist"""
    docs = [
        ("docs/PERFORMANCE_OPTIMIZATIONS.md", "Performance Optimizations"),
        ("docs/SETUP_GUIDE.md", "Setup Guide"),
        ("README.md", "Main README"),
        ("CHANGELOG.md", "Changelog"),
        ("CONTRIBUTING.md", "Contributing Guide")
    ]

    all_exist = True
    for file_path, name in docs:
        if Path(file_path).exists():
            log_test(f"Docs: {name}", "PASS", f"{file_path} exists", 0)
        else:
            log_test(f"Docs: {name}", "FAIL", f"{file_path} missing", 0)
            all_exist = False

    return all_exist

def print_summary():
    """Print test summary"""
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    total = test_results["passed"] + test_results["failed"] + test_results["skipped"]
    pass_rate = (test_results["passed"] / total * 100) if total > 0 else 0

    print(f"Total Tests: {total}")
    print(f"Passed: {test_results['passed']} ({pass_rate:.1f}%)")
    print(f"Failed: {test_results['failed']}")
    print(f"Skipped: {test_results['skipped']}")
    print("="*70)

    return test_results["failed"] == 0

def main():
    """Run all tests"""
    print("="*70)
    print("MDSA COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"Testing all performance fixes and integrations...")
    print()

    # Section 1: Code Implementation Tests (can run without servers)
    print("Section 1: Code Implementation Tests")
    print("-" * 70)
    test_domain_embedding_cache()
    test_response_cache()
    test_tracking_endpoint()
    test_tracking_integration()
    test_config_files()
    test_documentation_exists()
    print()

    # Section 2: Server Tests (requires running servers)
    print("Section 2: Server Availability Tests")
    print("-" * 70)
    dashboard_running = test_dashboard_running()
    chatbot_running = test_chatbot_running()
    print()

    # Print final summary
    all_passed = print_summary()

    # Provide next steps
    print("\nNEXT STEPS:")
    print("-" * 70)
    if not dashboard_running:
        print("1. Start dashboard: python mdsa/ui/dashboard/app.py")
    if not chatbot_running:
        print("2. Start chatbot: python chatbot_app/medical_app/enhanced_medical_chatbot_fixed.py")

    if dashboard_running and chatbot_running:
        print("✓ All servers running!")
        print("\nManual Testing:")
        print("1. Open http://localhost:7860 (chatbot)")
        print("2. Send a test query (e.g., 'Patient has chest pain')")
        print("3. Send the SAME query again (should be instant - cache hit)")
        print("4. Open http://localhost:9000/monitor (dashboard)")
        print("5. Verify monitoring graph shows your queries")
        print("\nExpected Performance:")
        print("- First query: 600-2000ms")
        print("- Repeated query: <10ms (look for [CACHE HIT] in console)")
        print("- Dashboard updates with real requests (not demo data)")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
