# Quick Start Guide - Enhanced Medical Chatbot

Get the medical chatbot running in 5 minutes!

**IMPORTANT:** Use `enhanced_medical_chatbot_fixed.py` (not the original file).

---

## Prerequisites

✅ Python 3.10+ installed
✅ 16GB+ RAM
✅ 50GB free disk space
✅ Internet connection (for model download)

---

## Installation (3 Steps)

### 1. Install Dependencies

```bash
# Navigate to medical app directory
cd "chatbot_app/medical_app"

# Install PyTorch (CPU version)
pip install torch torchvision torchaudio

# Install other requirements
pip install transformers accelerate gradio
```

### 2. Install MDSA Framework

```bash
# Go back to root directory
cd "../.."

# Install framework
pip install -e .
```

### 3. Run the Chatbot

```bash
# Navigate to medical app
cd chatbot_app/medical_app

# Launch chatbot (USE THE FIXED VERSION!)
python enhanced_medical_chatbot_fixed.py
```

**That's it!** The chatbot will start on http://localhost:7860

---

## First Run Notes

⏱️ **First query will be slow** (10-30 seconds) - models are downloading
⏱️ **Subsequent queries are fast** (<3 seconds)
💾 **Models download to**: `~/.cache/huggingface/` (~30GB total)

---

## Quick Test

Open http://localhost:7860 in your browser and try:

```
1. "What ICD-10 code for Type 2 diabetes?"
2. "/code E11.9"
3. "What are symptoms of hypertension?"
```

---

## Available Medical SLMs

| Domain | Model | Size | Purpose |
|--------|-------|------|---------|
| Clinical Diagnosis | Meerkat-8B | 8B | Diagnosis, clinical reasoning |
| Medical Coding | MediPhi-Instruct | 4B | ICD/CPT/HCPCS codes, billing |
| Biomedical Extraction | OpenBioLLM-8B | 8B | Text analysis, entity extraction |
| Radiology Support | BioMedLM | 2.7B | Radiology reports, imaging |
| Medical Q&A | TinyLlama-Health | 1.1B | Quick definitions, simple Q&A |

---

## Common Commands

### Code Lookup
```
/code E11.9          # Look up specific ICD-10 code
/code 99213          # Look up CPT code
```

### Sample Queries

**Clinical Diagnosis**:
- "Differential diagnosis for chest pain"
- "Symptoms of COPD exacerbation"
- "Red flags for headache"

**Medical Coding**:
- "What ICD-10 code for hypertension?"
- "CPT code for office visit 30 minutes"
- "Help write medical necessity for chest X-ray"

**Entity Extraction**:
- "Extract diagnoses from: Patient has diabetes and high blood pressure"
- "Summarize this radiology report: [paste report]"

---

## Troubleshooting

### "Out of Memory" Error
**Solution**: Close other applications, or disable reasoning:
```python
# Edit enhanced_medical_chatbot.py (bottom):
create_gradio_interface(enable_reasoning=False)
```

### "Connection Refused" Error
**Solution**: Check if port 7860 is free, or use different port:
```python
# Edit enhanced_medical_chatbot.py:
demo.launch(server_port=7861)
```

### Models Download Slow
**Solution**: Models download automatically. Be patient on first run (10-30 min total).

---

## Features

✅ **5 Specialized Medical SLMs**
✅ **Dual RAG** (Global + Local knowledge bases)
✅ **Hybrid Orchestration** (Fast TinyBERT + Smart Phi-2 reasoning)
✅ **40+ Medical Codes** pre-loaded (ICD-10, CPT, HCPCS)
✅ **Clinical Guidelines** built-in
✅ **Real-time Statistics** and monitoring
✅ **Export Conversations** as JSON

---

## System Requirements Met?

Check if your system is ready:

```bash
python -c "import sys; print(f'Python: {sys.version}'); import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"
```

Expected output:
```
Python: 3.11.x (or 3.10+)
PyTorch: 2.1.x (or 2.0+)
CUDA Available: True/False
```

---

## What Happens on First Run?

1. **Framework initializes** (~5 seconds)
2. **Knowledge base loads** (~2 seconds)
3. **Domains register** (~1 second)
4. **Gradio interface starts** (~2 seconds)
5. **First query triggers model download** (~10-30 minutes)
6. **Subsequent queries are fast** (<3 seconds)

---

## GPU vs CPU Mode

**CPU Mode** (Default):
- Works on any system
- Slower inference (2-5s per query)
- Automatic INT8 quantization

**GPU Mode** (If you have NVIDIA GPU):
```python
# Edit enhanced_medical_chatbot.py:
create_gradio_interface(prefer_gpu=True)
```
- Faster inference (<1s per query)
- Requires CUDA-capable GPU (4GB+ VRAM)

---

## Next Steps

✅ Read [SETUP_AND_USAGE.md](SETUP_AND_USAGE.md) for detailed guide
✅ Check [enhanced_medical_kb.py](knowledge_base/enhanced_medical_kb.py) to add more medical codes
✅ Explore [enhanced_medical_domains.py](domains/enhanced_medical_domains.py) to customize models
✅ See main [README.md](README.md) for architecture details

---

## Need Help?

1. Check console output for error messages
2. Review [SETUP_AND_USAGE.md](SETUP_AND_USAGE.md) troubleshooting section
3. Verify all dependencies installed: `pip list | grep -E "torch|transformers|gradio"`

---

**Ready to Use!** 🏥

Your enhanced medical chatbot is production-ready with:
- 5 specialized medical SLMs
- Comprehensive medical knowledge base
- Intelligent routing and reasoning
- User-friendly Gradio interface

**Disclaimer**: For educational and support purposes only. Not a substitute for professional medical advice.

---

*Last Updated: December 7, 2025*
*MDSA Framework v1.0*
