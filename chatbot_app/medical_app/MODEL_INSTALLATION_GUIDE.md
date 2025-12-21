# Medical SLM Installation Guide

Complete guide to installing and downloading all 5 specialized medical models for the Enhanced Medical Chatbot.

---

## Overview

The chatbot uses **5 specialized medical SLMs** totaling approximately **30-40GB**:

| Model | Size | Purpose | HuggingFace ID |
|-------|------|---------|----------------|
| Meerkat-8B | ~16GB | Clinical diagnosis, differential diagnosis | `dmis-lab/llama-3-meerkat-8b-v1.0` |
| MediPhi-Instruct | ~8GB | Medical coding, billing, ICD/CPT | `microsoft/MediPhi-Instruct` |
| OpenBioLLM-8B | ~16GB | Biomedical extraction, entity recognition | `aaditya/Llama3-OpenBioLLM-8B` |
| BioMedLM | ~5GB | Radiology support, clinical Q&A | `stanford-crfm/BioMedLM` |
| TinyLlama-Health | ~2GB | Quick medical definitions, edge deployment | `selinazarzour/healthgpt-tinyllama` |

---

## Installation Methods

### Method 1: Automatic Download (Recommended)

**The models download automatically on first use!**

1. **Install dependencies:**
   ```bash
   cd chatbot_app/medical_app
   pip install torch transformers accelerate gradio huggingface_hub
   ```

2. **Install MDSA framework:**
   ```bash
   cd ../..
   pip install -e .
   ```

3. **Run the chatbot:**
   ```bash
   cd chatbot_app/medical_app
   python enhanced_medical_chatbot_fixed.py
   ```

4. **First query triggers download:**
   - When you send your first medical query, the required model will download automatically
   - Progress bar shows download status
   - **First query: 10-30 minutes** (models downloading)
   - **Subsequent queries: <3 seconds**

---

### Method 2: Pre-download Models (Faster First Run)

If you want to download models ahead of time:

#### Step 1: Install HuggingFace CLI

```bash
pip install huggingface_hub
```

#### Step 2: Login to HuggingFace (Optional but Recommended)

```bash
huggingface-cli login
```

Enter your HuggingFace token when prompted. Get a token from: https://huggingface.co/settings/tokens

#### Step 3: Download Each Model

```bash
# Clinical Diagnosis - Meerkat-8B (~16GB)
huggingface-cli download dmis-lab/llama-3-meerkat-8b-v1.0

# Medical Coding - MediPhi-Instruct (~8GB)
huggingface-cli download microsoft/MediPhi-Instruct

# Biomedical Extraction - OpenBioLLM-8B (~16GB)
huggingface-cli download aaditya/Llama3-OpenBioLLM-8B

# Radiology Support - BioMedLM (~5GB)
huggingface-cli download stanford-crfm/BioMedLM

# Medical Q&A - TinyLlama-Health (~2GB)
huggingface-cli download selinazarzour/healthgpt-tinyllama
```

**Total download time:** 30-60 minutes (depending on internet speed)

---

### Method 3: Download with Python Script

Create a file `download_models.py`:

```python
"""Download all medical models ahead of time."""
from transformers import AutoModel, AutoTokenizer

models = [
    "dmis-lab/llama-3-meerkat-8b-v1.0",
    "microsoft/MediPhi-Instruct",
    "aaditya/Llama3-OpenBioLLM-8B",
    "stanford-crfm/BioMedLM",
    "selinazarzour/healthgpt-tinyllama"
]

for model_name in models:
    print(f"\n{'='*60}")
    print(f"Downloading {model_name}")
    print(f"{'='*60}")

    try:
        # Download model
        print(f"Downloading model weights...")
        model = AutoModel.from_pretrained(
            model_name,
            trust_remote_code=True
        )

        # Download tokenizer
        print(f"Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

        print(f"✓ {model_name} downloaded successfully!")

        # Clean up memory
        del model
        del tokenizer

    except Exception as e:
        print(f"✗ Error downloading {model_name}: {e}")

print("\n" + "="*60)
print("All models downloaded!")
print("="*60)
```

Run it:

```bash
python download_models.py
```

---

## Model Storage Locations

Models are cached in:

- **Windows**: `C:\Users\<username>\.cache\huggingface\hub`
- **Linux**: `~/.cache/huggingface/hub`
- **macOS**: `~/.cache/huggingface/hub`

You can change the cache directory by setting the `HF_HOME` environment variable:

```bash
# Windows PowerShell
$env:HF_HOME = "D:\huggingface_cache"

# Linux/Mac
export HF_HOME="/path/to/cache"
```

---

## System Requirements

### Minimum Requirements (CPU Mode)

- **RAM**: 16GB (32GB recommended)
- **Storage**: 50GB free space
- **CPU**: Modern multi-core (Intel i5/AMD Ryzen 5 or better)
- **Internet**: Stable connection for downloads

### Recommended Requirements (GPU Mode)

- **GPU**: NVIDIA RTX 3050+ with 4GB+ VRAM
- **RAM**: 16GB system RAM
- **Storage**: 50GB SSD
- **CUDA**: 11.8 or higher

---

## Verifying Installation

After downloading, verify models are available:

```python
from transformers import AutoTokenizer

models = [
    "dmis-lab/llama-3-meerkat-8b-v1.0",
    "microsoft/MediPhi-Instruct",
    "aaditya/Llama3-OpenBioLLM-8B",
    "stanford-crfm/BioMedLM",
    "selinazarzour/healthgpt-tinyllama"
]

for model_name in models:
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print(f"✓ {model_name}: Available")
    except Exception as e:
        print(f"✗ {model_name}: Not found")
```

---

## GPU Setup (Optional)

### Install CUDA-enabled PyTorch

If you have an NVIDIA GPU:

```bash
# For CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Verify GPU Availability

```python
import torch
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"CUDA Version: {torch.version.cuda}")
print(f"GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'}")
```

### Enable GPU in Chatbot

Edit `enhanced_medical_chatbot_fixed.py` (bottom):

```python
if __name__ == "__main__":
    create_gradio_interface(
        enable_reasoning=True,
        prefer_gpu=True,  # Change to True
        share=False
    )
```

---

## Troubleshooting

### Issue 1: "Connection Error" During Download

**Solution:**
- Check internet connection
- Try again later (HuggingFace servers may be busy)
- Use a VPN if HuggingFace is blocked in your region

### Issue 2: "Out of Memory" Error

**Solution:**
- Close other applications
- Reduce batch size in domain configs
- Use CPU mode instead of GPU mode
- Upgrade to 32GB RAM

### Issue 3: Models Download Slowly

**Solution:**
- Download models overnight
- Use pre-download method (Method 2 or 3)
- Download one model at a time

### Issue 4: "Model Not Found" After Download

**Solution:**
- Check cache directory: `~/.cache/huggingface/hub`
- Verify internet connection during download
- Delete partial downloads and re-download
- Check HuggingFace token if using gated models

### Issue 5: Insufficient Disk Space

**Solution:**
- Free up at least 50GB space
- Move cache to different drive:
  ```bash
  export HF_HOME="/path/to/larger/drive"
  ```

---

## Model-Specific Notes

### Meerkat-8B (Clinical Diagnosis)
- Based on Llama-3 architecture
- Fine-tuned on medical literature and USMLE questions
- Best for differential diagnosis and clinical reasoning
- **Download time:** ~10-15 minutes

### MediPhi-Instruct (Medical Coding)
- Specialized for ICD-10, CPT, and HCPCS codes
- Trained on medical billing and coding data
- Excellent for medical necessity statements
- **Download time:** ~5-10 minutes

### OpenBioLLM-8B (Biomedical Extraction)
- Based on Llama-3 with biomedical fine-tuning
- Extracts clinical entities and relationships
- Good for de-identification and summarization
- **Download time:** ~10-15 minutes

### BioMedLM (Radiology Support)
- Smaller model (2.7B parameters)
- Fine-tuned on radiology reports
- Fast inference for clinical Q&A
- **Download time:** ~3-5 minutes

### TinyLlama-Health (Medical Q&A Lite)
- Lightweight (1.1B parameters)
- Optimized for edge deployment
- Quick medical definitions and simple queries
- **Download time:** ~2-3 minutes

---

## Alternative: Use Smaller Models (if disk space limited)

If you don't have 50GB available, you can start with just the lightweight models:

```python
# In domains/enhanced_medical_domains.py, comment out large models:
# def get_all_enhanced_medical_domains(...):
#     return [
#         # create_clinical_diagnosis_domain(),  # Comment out (16GB)
#         # create_medical_coding_domain(),      # Comment out (8GB)
#         # create_biomedical_extraction_domain(),  # Comment out (16GB)
#         create_radiology_support_domain(),      # Keep (5GB)
#         create_lightweight_medical_qa_domain()  # Keep (2GB)
#     ]
```

This reduces storage to **~7GB** but loses some specialized capabilities.

---

## Performance Expectations

### First Run (Models Downloading)
- **Time:** 30-60 minutes
- **Network:** 30-40GB download
- **CPU Usage:** Low (just downloading)

### First Query (Models Loading)
- **Time:** 10-30 seconds
- **RAM Usage:** 8-12GB
- **CPU Usage:** High during loading

### Subsequent Queries
- **Time:** <3 seconds
- **RAM Usage:** 8-12GB (models cached)
- **CPU Usage:** Moderate

### GPU Mode (if enabled)
- **First Query:** 5-10 seconds
- **Subsequent Queries:** <1 second
- **VRAM Usage:** 4-6GB

---

## Summary Checklist

- [ ] Installed Python 3.10+
- [ ] Installed dependencies (torch, transformers, gradio)
- [ ] Installed MDSA framework (`pip install -e .`)
- [ ] Have 50GB+ free disk space
- [ ] Have stable internet connection
- [ ] Downloaded models (automatic or manual)
- [ ] Verified models with test script
- [ ] (Optional) Configured GPU if available
- [ ] Ready to run chatbot!

---

## Next Steps

Once models are installed:

1. **Run chatbot:**
   ```bash
   python enhanced_medical_chatbot_fixed.py
   ```

2. **Test with sample queries:**
   - "What ICD-10 code for Type 2 diabetes?"
   - "/code E11.9"
   - "What are symptoms of hypertension?"

3. **Check statistics tab** to see model usage

4. **Review QUICK_START.md** for full usage guide

---

## Need Help?

1. Check console output for error messages
2. Verify all dependencies: `pip list | grep -E "torch|transformers|gradio"`
3. Check model cache: `ls ~/.cache/huggingface/hub` (Linux/Mac) or `dir %USERPROFILE%\.cache\huggingface\hub` (Windows)
4. Review troubleshooting section above

---

**Happy chatting with specialized medical AI!** 🏥

*Last Updated: December 7, 2025*
*MDSA Framework v1.0*
