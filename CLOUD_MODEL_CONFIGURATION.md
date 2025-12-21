# Cloud Model Configuration for Medical Domains

## ✅ Implementation Complete

All 5 medical domains have been successfully configured with Ollama cloud models optimized for their specific capabilities.

---

## 🎯 Cloud Model Assignments

### 1. Medical Coding & Billing
**Model:** `kimi-k2-thinking:cloud`
- **Why:** Precise reasoning capabilities for accurate ICD-10/CPT code mapping
- **Strengths:** Structured thinking, logical inference, code validation
- **Domain:** `medical_coding`
- **Keywords:** icd, cpt, billing, claims, denial, medical necessity

### 2. Clinical Diagnosis
**Model:** `deepseek-v3.1:671b-cloud` (671B parameters)
- **Why:** Largest model with most comprehensive medical reasoning
- **Strengths:** Differential diagnosis, complex clinical reasoning, USMLE-level knowledge
- **Domain:** `clinical_diagnosis`
- **Keywords:** diagnosis, differential, symptoms, clinical reasoning, patient

### 3. Biomedical Text Extraction
**Model:** `qwen3-coder:480b-cloud` (480B parameters)
- **Why:** Optimized for structured extraction and data parsing
- **Strengths:** Entity extraction, JSON formatting, de-identification, clinical note parsing
- **Domain:** `biomedical_extraction`
- **Keywords:** extract, entity, medication, lab, clinical note, de-identify

### 4. Radiology Support
**Model:** `qwen3-vl:235b-instruct-cloud` (235B parameters)
- **Why:** Vision-language model for imaging report analysis
- **Strengths:** Visual understanding, radiology terminology, multimodal reasoning
- **Domain:** `radiology_support`
- **Keywords:** radiology, imaging, x-ray, ct, mri, report, findings

### 5. Medical Q&A Lite
**Model:** `gpt-oss:120b-cloud` (120B parameters)
- **Why:** General-purpose model for basic medical questions
- **Strengths:** Fast responses, simple explanations, medical terminology
- **Domain:** `medical_qa_lite`
- **Keywords:** what is, explain, define, meaning, medical term

---

## 📊 Model Comparison

| Domain | Model | Size | Tier | Specialty |
|--------|-------|------|------|-----------|
| Medical Coding | kimi-k2-thinking:cloud | Thinking-optimized | TIER1 | Precise reasoning |
| Clinical Diagnosis | deepseek-v3.1:671b-cloud | 671B | TIER1 | Complex reasoning |
| Biomedical Extraction | qwen3-coder:480b-cloud | 480B | TIER1 | Structured extraction |
| Radiology Support | qwen3-vl:235b-instruct-cloud | 235B | TIER1 | Vision-language |
| Medical Q&A | gpt-oss:120b-cloud | 120B | TIER1 | General purpose |

---

## 🔧 Changes Made

### File: `chatbot_app/medical_app/domains/enhanced_medical_domains.py`

**Lines 23-32:** Defined cloud model constants
```python
CLOUD_MEDICAL_CODING_MODEL = "ollama://kimi-k2-thinking:cloud"
CLOUD_CLINICAL_MODEL = "ollama://deepseek-v3.1:671b-cloud"
CLOUD_BIOMEDICAL_MODEL = "ollama://qwen3-coder:480b-cloud"
CLOUD_RADIOLOGY_MODEL = "ollama://qwen3-vl:235b-instruct-cloud"
CLOUD_QA_LITE_MODEL = "ollama://gpt-oss:120b-cloud"
```

**Updated Domains:**
- Line 68: Clinical Diagnosis → `CLOUD_CLINICAL_MODEL`
- Line 121: Medical Coding → `CLOUD_MEDICAL_CODING_MODEL`
- Line 175: Biomedical Extraction → `CLOUD_BIOMEDICAL_MODEL`
- Line 280: Radiology Support → `CLOUD_RADIOLOGY_MODEL`
- Line 227: Medical Q&A Lite → `CLOUD_QA_LITE_MODEL`

**Model Tier Updates:**
- All domains upgraded from `ModelTier.TIER2` → `ModelTier.TIER1` (cloud models are high-tier)

---

## 🚀 Testing the Configuration

### Step 1: Start Ollama Server
Ensure your Ollama server is running and has access to cloud models:
```bash
ollama serve
```

### Step 2: Verify Cloud Model Access
Check that cloud models are available:
```bash
ollama list | grep cloud
```

You should see:
- kimi-k2-thinking:cloud
- deepseek-v3.1:671b-cloud
- qwen3-coder:480b-cloud
- qwen3-vl:235b-instruct-cloud
- gpt-oss:120b-cloud

### Step 3: Test Medical Chatbot
```bash
python chatbot_app/medical_app/enhanced_medical_chatbot_fixed.py
```

Open http://localhost:7860 and test queries:

**Medical Coding:**
```
"What is the ICD-10 code for Type 2 Diabetes?"
→ Should route to medical_coding (kimi-k2-thinking:cloud)
```

**Clinical Diagnosis:**
```
"Patient with fever, cough, and fatigue. What's the differential diagnosis?"
→ Should route to clinical_diagnosis (deepseek-v3.1:671b-cloud)
```

**Biomedical Extraction:**
```
"Extract medications from: Patient takes metformin 500mg BID and lisinopril 10mg QD"
→ Should route to biomedical_extraction (qwen3-coder:480b-cloud)
```

**Radiology Support:**
```
"Analyze this CT scan report: Small nodule in RUL measuring 4mm"
→ Should route to radiology_support (qwen3-vl:235b-instruct-cloud)
```

**Medical Q&A:**
```
"What does hypertension mean?"
→ Should route to medical_qa_lite (gpt-oss:120b-cloud)
```

### Step 4: Test Tool Calling
```bash
python test_ollama_tools.py
```

This will verify that cloud models support:
- Standard text generation
- Tool/function calling (if model supports it)
- API key authentication

---

## 🔐 Authentication (if required)

If your cloud Ollama setup requires API keys, the MDSA adapter now supports authentication:

### Option 1: Environment Variable
```bash
export OLLAMA_API_KEY="your-api-key-here"
```

### Option 2: Direct Configuration
Edit domain kwargs to include API key:
```python
DomainConfig(
    domain_id="medical_coding",
    model_name="ollama://kimi-k2-thinking:cloud",
    kwargs={
        'ollama_api_key': 'your-api-key-here',
        'ollama_base_url': 'https://your-cloud-endpoint.com',
        'ollama_timeout': 300
    }
)
```

---

## 📈 Expected Benefits

### Performance:
- **Accuracy:** Higher with larger, specialized cloud models
- **Latency:** Depends on cloud endpoint (typically 1-5 seconds)
- **Reliability:** Cloud infrastructure handles load balancing

### Resource Usage:
- **Client Memory:** Minimal (~50MB vs ~3GB for local models)
- **GPU Requirements:** None (inference on cloud servers)
- **Scalability:** Unlimited concurrent requests (cloud handles scaling)

### Quality:
- **Medical Coding:** More precise code suggestions (kimi thinking model)
- **Clinical Diagnosis:** Better differential diagnosis (671B parameters)
- **Extraction:** More accurate entity recognition (qwen coder)
- **Radiology:** Better understanding of imaging reports (vision-language)
- **Q&A:** More comprehensive answers (120B general model)

---

## 🔄 Fallback Strategy

The MDSA framework automatically handles failures:

1. **Primary:** Try cloud model
2. **Fallback:** If cloud unavailable, escalate to general orchestrator
3. **Keyword Routing:** Use keyword-based routing as last resort

Configure fallback in orchestrator:
```python
orchestrator = TinyBERTOrchestrator(
    enable_fallback=True,
    fallback_confidence_threshold=0.80  # Lowered from 0.85
)
```

---

## 📝 Monitoring

Track cloud model performance via the MDSA dashboard:

```bash
python mdsa/ui/dashboard/app.py
```

Open http://localhost:5000/monitor to see:
- **Latency by Domain:** Which cloud models respond fastest
- **Request Distribution:** Which domains are most used
- **Success Rate:** Cloud model reliability

---

## ✅ Status

**Configuration:** ✅ Complete
**Tool Calling Support:** ✅ Added to framework
**API Authentication:** ✅ Supported
**Testing:** ⏳ Pending (next task)

**Ready for:** End-to-end testing with medical chatbot

---

## 🎯 Next Steps

1. ✅ Cloud model configuration - COMPLETE
2. ⏳ Test medical chatbot with cloud models and tool calling - **NEXT**
3. ⏳ Create EduAI project structure
4. ⏳ Implement EduAI domains with cloud models
5. ⏳ Write comprehensive documentation

---

**Last Updated:** 2025-12-10
**Modified Files:**
- `chatbot_app/medical_app/domains/enhanced_medical_domains.py`
- `mdsa/integrations/adapters/ollama_adapter.py` (tool calling support)
- `mdsa/core/orchestrator.py` (confidence threshold)
