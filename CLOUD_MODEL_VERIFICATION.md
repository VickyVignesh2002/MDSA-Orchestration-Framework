# Ollama Cloud Models Verification - Phase -1.2

**Date**: December 11, 2025
**Status**: ✅ **CONFIGURATION VERIFIED** | ⏳ **TESTING PENDING**
**Phase**: -1.2 (Verify Ollama Cloud Models)

---

## 📋 Overview

This document summarizes the verification of all 5 Ollama cloud models configured in the MDSA framework for the Enhanced Medical Chatbot application.

**Objectives**:
1. ✅ Verify all 5 cloud models are properly configured
2. ✅ Verify Ollama adapter supports tool calling and authentication
3. ⏳ Test live connectivity to all cloud models
4. ⏳ Verify tool calling functionality
5. ⏳ Document test results and performance metrics

---

## ✅ Configuration Verification (COMPLETE)

### 1. Cloud Models Configuration

**File**: [chatbot_app/medical_app/domains/enhanced_medical_domains.py](chatbot_app/medical_app/domains/enhanced_medical_domains.py)

All 5 medical domains are properly configured with Ollama cloud models:

| Domain | Model | Parameters | Purpose |
|--------|-------|------------|---------|
| **Medical Coding** | `ollama://kimi-k2-thinking:cloud` | Thinking-optimized | ICD-10, CPT, HCPCS coding with reasoning |
| **Clinical Diagnosis** | `ollama://deepseek-v3.1:671b-cloud` | 671B params | Complex clinical reasoning and diagnosis |
| **Biomedical Extraction** | `ollama://qwen3-coder:480b-cloud` | 480B params | Structured data extraction from medical text |
| **Radiology Support** | `ollama://qwen3-vl:235b-instruct-cloud` | 235B vision-language | Radiology reports and imaging analysis |
| **Medical Q&A Lite** | `ollama://gpt-oss:120b-cloud` | 120B params | Quick medical questions and definitions |

**Configuration Details** (lines 28-32):
```python
# Cloud model constants
CLOUD_MEDICAL_CODING_MODEL = "ollama://kimi-k2-thinking:cloud"
CLOUD_CLINICAL_MODEL = "ollama://deepseek-v3.1:671b-cloud"
CLOUD_BIOMEDICAL_MODEL = "ollama://qwen3-coder:480b-cloud"
CLOUD_RADIOLOGY_MODEL = "ollama://qwen3-vl:235b-instruct-cloud"
CLOUD_QA_LITE_MODEL = "ollama://gpt-oss:120b-cloud"
```

**Common Configuration**:
- All domains use `device = "ollama"` (server-side execution)
- All domains use `model_tier = ModelTier.TIER1` (high-tier cloud models)
- All domains have `device_strategy = DeviceStrategy.PREFER_GPU` (cloud GPU execution)

### 2. Ollama Adapter Capabilities

**File**: [mdsa/integrations/adapters/ollama_adapter.py](mdsa/integrations/adapters/ollama_adapter.py)

#### ✅ API Key Authentication (lines 259-268)
```python
def __init__(
    self,
    model_name: str,
    base_url: str = "http://localhost:11434",
    timeout: int = 120,
    api_key: Optional[str] = None  # ✅ Supports API key
):
```

**Environment Variable Support**:
- `OLLAMA_API_KEY` - API key for cloud model access
- `OLLAMA_BASE_URL` - Custom Ollama server endpoint (default: http://localhost:11434)

#### ✅ Tool Calling Support (lines 364-641)

The adapter has full tool calling implementation:

**1. Tool Calling Parameters** (lines 364-366):
```python
def generate(
    self,
    input_ids: Optional[Any] = None,
    max_new_tokens: int = 512,
    temperature: float = 0.7,
    tools: Optional[List[Dict]] = None,  # ✅ Tools parameter
    tool_choice: str = "auto",  # ✅ Tool selection strategy
    **kwargs
):
```

**2. Tool Calling Implementation** (lines 521-626):
- Uses `/api/chat` endpoint when tools are provided
- Supports `tool_choice`: "auto", "none", or specific tool name
- Returns `OllamaGeneratedOutput` with `tool_calls` list
- Each tool call includes: `id`, `name`, `arguments` (JSON)

**3. Tool Call Format**:
```python
{
    "id": "call_abc123",
    "name": "calculate",
    "arguments": {"operation": "add", "a": 5, "b": 3}
}
```

**4. Autonomous Tool Selection**:
- Models can detect when to use tools based on query
- No explicit tool triggering required
- Models parse tool definitions and select appropriate tool

---

## 🧪 Test Script: `test_ollama_cloud_models.py`

**File**: [test_ollama_cloud_models.py](test_ollama_cloud_models.py) (328 lines)

### Test Coverage

#### 1. Model Connectivity Tests (All 5 Models)

Each model is tested with domain-specific prompts:

| Model | Test Prompt | Expected Keywords |
|-------|-------------|-------------------|
| **kimi-k2-thinking:cloud** | "What ICD-10 code for Type 2 diabetes without complications?" | "E11", "diabet" |
| **deepseek-v3.1:671b-cloud** | "Differential diagnoses for chest pain and dyspnea?" | "diagnos", "chest" |
| **qwen3-coder:480b-cloud** | "Extract medications: Patient takes metformin 500mg BID..." | "metformin", "lisinopril" |
| **qwen3-vl:235b-instruct-cloud** | "Interpret: Small nodule in right upper lobe 4mm" | "nodule", "lung" |
| **gpt-oss:120b-cloud** | "What is hemoglobin A1c and why important?" | "hemoglobin", "diabet" |

#### 2. Tool Calling Test (Medical Coding Model)

Tests autonomous tool calling with a calculator tool:

**Tool Definition**:
```python
{
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Perform basic arithmetic calculations",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operation", "a", "b"]
        }
    }
}
```

**Test Prompt**: "What is 15 multiplied by 7? Use the calculate function."

**Expected Behavior**:
- Model detects need for calculation
- Calls `calculate` function with correct arguments
- Returns tool call with: `{"name": "calculate", "arguments": {"operation": "multiply", "a": 15, "b": 7}}`

#### 3. Test Metrics

For each model, the script measures:
- **Connection Success**: Can initialize model
- **Generation Success**: Can generate responses
- **Latency**: Response time in milliseconds (target: <5000ms for cloud models)
- **Tool Calling**: Whether model supports and uses tools
- **Keyword Validation**: Response contains expected medical terms

---

## 🚀 Running the Tests

### Prerequisites

1. **Ollama Server Running**:
   ```bash
   ollama serve
   ```

2. **API Key (if required)**:
   ```bash
   # Windows
   set OLLAMA_API_KEY=your_api_key_here

   # Linux/Mac
   export OLLAMA_API_KEY=your_api_key_here
   ```

3. **Custom Ollama Endpoint (optional)**:
   ```bash
   # Windows
   set OLLAMA_BASE_URL=https://your-cloud-endpoint.com

   # Linux/Mac
   export OLLAMA_BASE_URL=https://your-cloud-endpoint.com
   ```

### Run Tests

```bash
# From project root
python test_ollama_cloud_models.py
```

### Expected Output

```
######################################################################
# Ollama Cloud Models Test Suite
#
# Testing 5 cloud models for MDSA framework
######################################################################

Environment:
  OLLAMA_BASE_URL: http://localhost:11434 (default)
  OLLAMA_API_KEY: Set

======================================================================
Testing: kimi-k2-thinking:cloud
Description: Precise reasoning for medical coding
======================================================================

[1/4] Initializing model...
  ✓ Using API key from environment
  ✓ Model initialized successfully

[2/4] Testing standard text generation...
  Prompt: What ICD-10 code should I use for Type 2 diabetes melli...
  ✓ Generation successful
  ✓ Latency: 3456.78ms
  ✓ Response length: 245 characters

  Response preview:
  For Type 2 diabetes mellitus without complications, the correct ICD-10 code is E11.9. This code represents Type 2 diabetes mellitus without complications. The E11 category covers Type 2 diabetes, and the .9 specifi...

  ✓ Found expected keywords: ['E11', 'diabet']

[3/4] Testing tool calling support...
  ✓ Tool calling supported
  ✓ Tool calls made: 1
    - Function: calculate
      Arguments: {"operation": "multiply", "a": 15, "b": 7}

[4/4] Test complete ✓

... (tests for remaining 4 models)

======================================================================
TEST SUMMARY
======================================================================

Total models tested: 5
Successfully connected: 5/5
Successfully generated: 5/5
Tool calling support: 1/5

Model                               Status          Latency      Tools
----------------------------------- --------------- ------------ --------
kimi-k2-thinking                    ✓ Working       3456.78ms    ✓
deepseek-v3.1                       ✓ Working       4123.45ms    -
qwen3-coder                         ✓ Working       3890.12ms    -
qwen3-vl                            ✓ Working       4567.89ms    -
gpt-oss                             ✓ Working       2345.67ms    -

✓ All tests passed!
```

---

## 📊 Expected Test Results

### Success Criteria

| Metric | Target | Critical |
|--------|--------|----------|
| **Connection Rate** | 5/5 (100%) | ✅ Yes |
| **Generation Rate** | 5/5 (100%) | ✅ Yes |
| **Average Latency** | <5000ms per model | ⚠️ Monitor |
| **Keyword Match** | ≥80% of expected keywords found | ✅ Yes |
| **Tool Calling** | ≥1 model supports tools | ✅ Yes |

### Interpreting Results

#### ✅ All Tests Pass
- All 5 models connect successfully
- All 5 models generate relevant responses
- Latency reasonable (<5s per model)
- Tool calling works on at least one model
- **Action**: Mark Phase -1.2 complete, proceed to Phase -1.3

#### ⚠️ Partial Success
- Some models connect, others fail
- **Action**:
  1. Check OLLAMA_API_KEY is valid
  2. Verify models are available in cloud
  3. Check network connectivity
  4. Review error messages for specific issues

#### ❌ All Tests Fail
- No models connect
- **Action**:
  1. Verify Ollama server is running: `ollama list`
  2. Check OLLAMA_BASE_URL is correct
  3. Test local Ollama: `ollama run llama2 "Hello"`
  4. Check firewall/network settings

---

## 🐛 Troubleshooting

### Error: "Connection refused"

**Cause**: Ollama server not running

**Fix**:
```bash
# Start Ollama server
ollama serve
```

### Error: "Unauthorized" or "API key invalid"

**Cause**: Missing or invalid API key

**Fix**:
```bash
# Set API key
set OLLAMA_API_KEY=your_actual_api_key

# Re-run tests
python test_ollama_cloud_models.py
```

### Error: "Model not found"

**Cause**: Cloud model not available in your Ollama instance

**Fix**:
```bash
# Pull cloud models (if available)
ollama pull kimi-k2-thinking:cloud
ollama pull deepseek-v3.1:671b-cloud
# ... etc
```

**Note**: Cloud models may require special access or subscription.

### Error: "Timeout"

**Cause**: Model taking too long to respond (>5 minutes)

**Fix**:
1. Increase timeout in test script (line 146): `timeout=600`
2. Check network connection
3. Try smaller/faster model first

### Tool Calling Not Working

**Expected**: Tool calling may only work on specific models (like kimi-k2-thinking:cloud)

**Verification**:
- Check if response contains tool_calls in metadata
- Review model capabilities documentation
- Not all models support tool calling

---

## 📋 Verification Checklist

### Configuration ✅
- [x] All 5 cloud models defined in enhanced_medical_domains.py
- [x] All domains use `device="ollama"`
- [x] All domains use `ModelTier.TIER1`
- [x] Ollama adapter supports API key authentication
- [x] Ollama adapter supports tool calling

### Testing ⏳
- [ ] Run test_ollama_cloud_models.py
- [ ] All 5 models connect successfully
- [ ] All 5 models generate responses
- [ ] Responses contain expected keywords
- [ ] At least 1 model supports tool calling
- [ ] Latency acceptable (<5s per model)
- [ ] No critical errors

### Documentation ⏳
- [ ] Record test results
- [ ] Document any issues found
- [ ] Create performance benchmark table
- [ ] Take screenshots of working tests

---

## 🎯 Next Steps

### After Tests Pass

**Proceed to Phase -1.3: Test Autonomous Tool Calling**
- Create 3 test tools (calculator, weather lookup, code execution)
- Test tools with all compatible models
- Verify autonomous tool selection
- Test tool result processing

**Proceed to Phase -1.4: Verify RAG Functionality**
- Test Global RAG retrieval (ICD-10, CPT, HCPCS)
- Test Local RAG for all 5 domains
- Verify privacy isolation
- Test RAG context injection

### If Tests Fail

1. **Document Failures**: Note which models failed and error messages
2. **Fallback Plan**: Consider using local models temporarily
3. **Contact Support**: Reach out to Ollama support for cloud model access
4. **Adjust Timeline**: May need to delay EduAI implementation

---

## 📝 Test Results (To Be Filled)

**Test Date**: _____________
**Tester**: _____________
**Environment**: _____________

| Model | Connected | Generated | Latency (ms) | Tool Calling | Notes |
|-------|-----------|-----------|--------------|--------------|-------|
| kimi-k2-thinking:cloud | ☐ Yes ☐ No | ☐ Yes ☐ No | _____ | ☐ Yes ☐ No | |
| deepseek-v3.1:671b-cloud | ☐ Yes ☐ No | ☐ Yes ☐ No | _____ | ☐ Yes ☐ No | |
| qwen3-coder:480b-cloud | ☐ Yes ☐ No | ☐ Yes ☐ No | _____ | ☐ Yes ☐ No | |
| qwen3-vl:235b-instruct-cloud | ☐ Yes ☐ No | ☐ Yes ☐ No | _____ | ☐ Yes ☐ No | |
| gpt-oss:120b-cloud | ☐ Yes ☐ No | ☐ Yes ☐ No | _____ | ☐ Yes ☐ No | |

**Overall Pass/Fail**: ☐ PASS ☐ FAIL

**Issues Found**:
```
[List any issues here]
```

**Performance Notes**:
```
[Record performance observations]
```

---

## 🔗 Related Documentation

- [DASHBOARD_FIX_SUMMARY.md](DASHBOARD_FIX_SUMMARY.md) - Dashboard connectivity fix (Phase -1.1)
- [CLOUD_MODEL_CONFIGURATION.md](CLOUD_MODEL_CONFIGURATION.md) - Original cloud model setup
- [test_ollama_cloud_models.py](test_ollama_cloud_models.py) - Test script
- [chatbot_app/medical_app/domains/enhanced_medical_domains.py](chatbot_app/medical_app/domains/enhanced_medical_domains.py) - Domain configurations
- [mdsa/integrations/adapters/ollama_adapter.py](mdsa/integrations/adapters/ollama_adapter.py) - Ollama adapter implementation

---

**Status**: ✅ **CONFIGURATION VERIFIED** | ⏳ **AWAITING TEST EXECUTION**

**Next Action**: Run `python test_ollama_cloud_models.py` to verify live connectivity

---

*Last Updated*: December 11, 2025
*Author*: Claude Sonnet 4.5
*Phase*: -1.2 (Verify Ollama Cloud Models)
