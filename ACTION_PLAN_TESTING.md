# MDSA Testing - Action Plan

## ✅ What's Been Fixed (Just Now)

1. **Dashboard initialization error** - Fixed in [app.py:97-126](mdsa/ui/dashboard/app.py#L97-L126)
2. **Missing HTML templates** - Created welcome.html and monitor.html
3. **Comprehensive testing script** - Created test_mdsa_comprehensive.py

---

## 🚨 CRITICAL: Do These First (Required Before Testing)

### Action 1: Restart Ollama (Fix 500 Error)

**Current Error:**
```
Ollama API error: 500 Server Error: Internal Server Error
```

**Solution:**
```bash
# Kill existing Ollama process
taskkill /F /IM ollama.exe

# Restart Ollama
ollama serve

# Verify model is available (in new terminal)
ollama list
# Should show: llama3.2:3b-instruct-q4_0
```

**Why:** Ollama server crashed and needs restart.

---

### Action 2: Install PyTorch with CUDA (Enable GPU)

**Current Issue:** PyTorch not detecting your RTX 3050 GPU (4GB)

**Current Status:**
```
has_cuda: False
device: cpu
```

**Solution:**
```bash
# Uninstall current PyTorch
pip uninstall torch torchvision torchaudio

# Install PyTorch with CUDA 11.8 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Verify Installation:**
```python
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

**Expected Output:**
```
CUDA Available: True
GPU: NVIDIA GeForce RTX 3050 Laptop GPU
```

**Why:** Your RTX 3050 GPU will significantly speed up model inference (5-10x faster).

---

### Action 3: Populate Knowledge Base (If Not Done)

**Check if needed:**
```bash
python chatbot_app/medical_app/populate_coding_knowledge.py
```

**Expected Output:** Should show "Knowledge base population completed successfully!"

**If errors occur:** They were already fixed, just run it.

---

## 🧪 Run Comprehensive Tests

Once Actions 1-3 are complete:

```bash
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"
python test_mdsa_comprehensive.py
```

---

## 📊 What the Test Script Checks

### Test 1: Orchestrator Initialization
- ✅ TinyBERTOrchestrator starts correctly
- ✅ All 5 domains registered
- ✅ Router, state manager, and components initialized

### Test 2: RAG Retrieval (Global and Local)
- ✅ Global RAG retrieves general medical knowledge
- ✅ Local RAG retrieves domain-specific knowledge
- ✅ RAG statistics show document counts

### Test 3: Multi-Domain Routing
- ✅ Routes to medical_coding domain
- ✅ Routes to clinical_diagnosis domain
- ✅ Routes to medical_qa_lite domain
- ✅ Routes to biomedical_extraction domain
- ✅ Routes to radiology_support domain
- ✅ Successfully routes to at least 2 different domains

### Test 4: Smart Orchestration (NOT Keyword-Based)
- ✅ Uses TinyBERT ML model for routing
- ✅ Routes based on semantic understanding, not just keywords
- ✅ Tests with tricky queries that don't have obvious keywords
- ✅ Verifies routing method is ML-based, not "fallback_keyword"

### Test 5: Tool Calling Functionality
- ✅ Claim Validator tool executes
- ✅ Returns denial risk scores
- ✅ Provides recommendations
- ✅ Code lookup tool works
- ✅ Can filter codes by type (ICD-10, CPT)

### Test 6: End-to-End Query Processing
- ✅ Full query processing pipeline works
- ✅ Returns proper response structure
- ✅ Includes domain, status, and response
- ✅ Tests multiple query types

### Test 7: System Health Checks
- ✅ PyTorch with CUDA availability
- ✅ Ollama server running
- ✅ Required model (llama3.2) available
- ✅ All required packages installed

---

## 📈 Expected Test Results

### Ideal Outcome (After Fixes):
```
Total Tests: ~30-35
✅ Passed: 30-35
❌ Failed: 0
Pass Rate: 100%

🎉 ALL TESTS PASSED!
✅ Ready to proceed with Directory Restructure
```

### If Tests Fail:
The script will tell you exactly what failed and why. Common issues:
- Ollama not running → See Action 1
- GPU not detected → See Action 2
- Knowledge base empty → See Action 3

---

## 🎯 After Tests Pass

Once you see "ALL TESTS PASSED", we proceed with:

### Next Step: Directory Restructure

**What will be restructured:**
```
Current (Messy):
version_1/
├── 30+ .md files in root
├── 15+ test_*.py files
├── mdsa/ (framework)
└── chatbot_app/ (example)

Target (Professional):
mdsa-framework/
├── mdsa/              # Core package
├── examples/          # Moved from chatbot_app/
├── tests/             # All test files
├── docs/              # All .md files
├── scripts/           # Utilities
└── setup.py           # Pip installable
```

**Benefits:**
- Clean root directory
- Professional structure
- Pip installable: `pip install mdsa`
- Ready for PyPI publication

---

## 🚀 Quick Start (Copy-Paste Commands)

### Terminal 1: Restart Ollama
```bash
taskkill /F /IM ollama.exe
ollama serve
```

### Terminal 2: Install CUDA PyTorch & Run Tests
```bash
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"

# Install PyTorch with CUDA
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify GPU
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Run comprehensive tests
python test_mdsa_comprehensive.py
```

### Terminal 3: Test Gradio UI (Optional, Parallel)
```bash
cd "j:\ME CSE\Sem III\Research Paper\MDSA Orcherstartion Framework\MDSA\version_1"
python chatbot_app/medical_app/enhanced_medical_chatbot_fixed.py
# Open http://localhost:7860
```

---

## 📊 Test Results Output

Results are saved to: `test_results.json`

**Sample output:**
```json
{
  "timestamp": "2025-12-10T10:30:00",
  "tests_passed": 32,
  "tests_failed": 0,
  "results": [
    {
      "test": "Orchestrator initialization",
      "passed": true,
      "details": "Domains: True, Router: True, State: True"
    },
    ...
  ]
}
```

---

## ⏱️ Estimated Time

| Action | Time |
|--------|------|
| Restart Ollama | 1 min |
| Install CUDA PyTorch | 5-10 min |
| Run comprehensive tests | 2-5 min |
| **Total** | **10-15 min** |

---

## 🐛 Troubleshooting

### Issue: "CUDA not available" after PyTorch install
**Solution:**
1. Check NVIDIA drivers: `nvidia-smi`
2. Verify CUDA version compatibility (your GPU supports CUDA 11.8)
3. Restart Python kernel/terminal

### Issue: Ollama models not loading
**Solution:**
```bash
ollama pull llama3.2:3b-instruct-q4_0
```

### Issue: Import errors during tests
**Solution:**
```bash
pip install sentence-transformers transformers fastapi uvicorn gradio
```

---

## ✅ Success Criteria

You're ready for Directory Restructure when:

- [x] Ollama server running without 500 errors
- [x] GPU detected and CUDA available
- [x] All 30+ tests passing
- [x] RAG retrieval working (global and local)
- [x] Multi-domain routing working
- [x] Smart orchestration using ML (not keywords)
- [x] Tool calling functional
- [x] End-to-end queries processing successfully

---

**Status:** ✅ Test script ready, waiting for you to complete Actions 1-3

**Next:** Run test_mdsa_comprehensive.py after completing the 3 actions above
