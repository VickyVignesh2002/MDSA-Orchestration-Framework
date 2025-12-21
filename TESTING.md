# MDSA Framework Testing Guide

Comprehensive guide for running tests in the MDSA framework.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Test Structure](#test-structure)
4. [Running Tests](#running-tests)
5. [Test Categories](#test-categories)
6. [Coverage Reports](#coverage-reports)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Packages

Install testing dependencies:

```bash
pip install pytest pytest-asyncio pytest-cov pytest-timeout
```

### Optional Packages (for parallel execution):

```bash
pip install pytest-xdist
```

---

## Quick Start

### Run All Tests

```bash
# From project root directory
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=mdsa --cov-report=html
```

### Run Specific Test Files

```bash
# Run only model tests
pytest tests/test_models.py

# Run only async tests
pytest tests/test_async.py

# Run only integration tests
pytest tests/test_integration.py
```

### Run by Test Category

```bash
# Run only unit tests (fast)
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only memory tests
pytest -m memory

# Run only async tests
pytest -m async

# Exclude slow tests
pytest -m "not slow"
```

---

## Test Structure

### Test Files

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_models.py           # Model loading and management tests (20+ tests)
├── test_async.py            # Async execution tests (15+ tests)
├── test_domains.py          # Domain configuration tests (15+ tests)
├── test_integration.py      # End-to-end integration tests (10+ tests)
└── test_memory.py           # Memory management tests (20+ tests)
```

### Additional Test Scripts

```
test_gpt2_quick.py           # Quick verification test with GPT-2
test_memory_stress.py        # Memory stress test
test_concurrent_loads.py     # Concurrent execution test
test_ui_manual.py            # Manual UI test with device selection
```

---

## Running Tests

### Basic Commands

```bash
# Run all tests with default settings
pytest

# Run with verbose output
pytest -v

# Run with extra test summary
pytest -ra

# Run with detailed output
pytest -vv

# Stop on first failure
pytest -x

# Run last failed tests only
pytest --lf

# Run new tests first
pytest --nf
```

### Parallel Execution

```bash
# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Run tests on 4 workers
pytest -n 4
```

### With Coverage

```bash
# Generate coverage report
pytest --cov=mdsa

# Generate HTML coverage report
pytest --cov=mdsa --cov-report=html

# Open coverage report (Windows)
start htmlcov/index.html

# Generate XML coverage report (for CI/CD)
pytest --cov=mdsa --cov-report=xml
```

### Filter by Test Names

```bash
# Run tests matching pattern
pytest -k "test_model"

# Run tests NOT matching pattern
pytest -k "not slow"

# Run multiple patterns
pytest -k "test_model or test_async"
```

---

## Test Categories

### Test Markers

Tests are categorized using pytest markers:

| Marker | Description | Example |
|--------|-------------|---------|
| `unit` | Unit tests (fast, isolated) | `@pytest.mark.unit` |
| `integration` | Integration tests (multiple components) | `@pytest.mark.integration` |
| `e2e` | End-to-end tests (full system) | `@pytest.mark.e2e` |
| `slow` | Tests that take >5 seconds | `@pytest.mark.slow` |
| `memory` | Memory management tests | `@pytest.mark.memory` |
| `concurrent` | Concurrent execution tests | `@pytest.mark.concurrent` |
| `async` | Async functionality tests | `@pytest.mark.async_` |
| `gpu` | Tests requiring GPU | `@pytest.mark.gpu` |

### Running Tests by Category

```bash
# Fast unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Memory tests only
pytest -m memory

# All except slow tests
pytest -m "not slow"

# Unit or integration tests
pytest -m "unit or integration"

# Memory tests but not slow
pytest -m "memory and not slow"
```

---

## Coverage Reports

### Generate Coverage Report

```bash
# Terminal report with missing lines
pytest --cov=mdsa --cov-report=term-missing

# HTML report (interactive)
pytest --cov=mdsa --cov-report=html

# XML report (for CI/CD tools)
pytest --cov=mdsa --cov-report=xml

# Multiple reports
pytest --cov=mdsa --cov-report=html --cov-report=term-missing
```

### View HTML Coverage Report

```bash
# Windows
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html

# Or navigate to: htmlcov/index.html in browser
```

### Coverage Threshold

The project requires **80%+ coverage**. Tests will fail if coverage drops below this threshold (configured in `pytest.ini`).

---

## Validation Tests

### Quick Verification Test

```bash
# Run quick test with GPT-2 (small model)
python test_gpt2_quick.py
```

**Expected Output:**
- No system freeze
- Memory pre-check working
- Model loads successfully
- Inference completes in ~10-30s

### Memory Stress Test

```bash
# Test memory management under stress
python test_memory_stress.py
```

**Tests:**
- LRU eviction working correctly
- Memory usage stays within safe limits
- Multiple domains load sequentially
- No memory leaks

### Concurrent Load Test

```bash
# Test concurrent execution
python test_concurrent_loads.py
```

**Tests:**
- No race conditions
- Atomic get-or-load lock working
- All queries return valid results
- No duplicate model loading

---

## Troubleshooting

### Common Issues

#### 1. Import Errors

```bash
# Ensure you're in the project root
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"

# Install package in development mode
pip install -e .
```

#### 2. Async Test Failures

```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Run with asyncio mode
pytest --asyncio-mode=auto
```

#### 3. Timeout Errors

```bash
# Increase timeout for slow tests
pytest --timeout=600

# Or disable timeout
pytest --timeout=0
```

#### 4. Memory Errors

Some tests may fail if insufficient memory available:

```bash
# Skip slow/memory-intensive tests
pytest -m "not slow and not memory"

# Run only fast unit tests
pytest -m unit
```

#### 5. GPU Tests Failing

If you don't have a GPU:

```bash
# Skip GPU tests
pytest -m "not gpu"
```

#### 6. Missing Dependencies

```bash
# Install all test dependencies
pip install pytest pytest-asyncio pytest-cov pytest-timeout psutil
```

---

## Test Performance Tips

### Speed Up Test Runs

```bash
# Run only fast tests
pytest -m "unit and not slow"

# Run in parallel
pytest -n auto

# Stop on first failure
pytest -x

# Run only failed tests from last run
pytest --lf
```

### Debug Failing Tests

```bash
# Run single test with verbose output
pytest tests/test_models.py::TestModelConfig::test_model_config_creation -vv

# Show local variables on failure
pytest --showlocals

# Enter debugger on failure
pytest --pdb

# Show print statements
pytest -s
```

---

## Continuous Integration

### Running Tests in CI/CD

```bash
# Complete test run with coverage for CI
pytest -v --cov=mdsa --cov-report=xml --cov-report=term-missing --tb=short
```

### Expected Results

- **Total Tests**: 80+ tests
- **Coverage Target**: 80%+
- **Test Duration**: ~2-5 minutes (depending on hardware and available memory)

### Success Criteria

✅ All unit tests pass
✅ Integration tests complete (may skip some if low memory)
✅ No system freezes or crashes
✅ Coverage >= 80%
✅ No memory leaks detected

---

## Additional Resources

### Configuration Files

- `pytest.ini` - Main pytest configuration
- `tests/conftest.py` - Shared fixtures and utilities
- `.coveragerc` - Coverage configuration (if created)

### Useful Commands Reference

```bash
# Show available fixtures
pytest --fixtures

# Show available markers
pytest --markers

# Collect tests without running
pytest --collect-only

# Show slowest N tests
pytest --durations=10

# Generate JUnit XML report
pytest --junitxml=results.xml
```

---

## Contact & Support

For issues with tests:
1. Check this guide first
2. Review test output for specific errors
3. Check memory availability
4. Verify all dependencies are installed
5. Try running with `-vv` for detailed output

---

**Last Updated**: 2025-12-03
**Framework Version**: 1.0
**Python Version**: 3.9+
