# Enhanced Medical Chatbot - Setup & Usage Guide

Complete guide to setting up and running the production-ready medical chatbot with specialized SLMs.

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Model Download](#model-download)
4. [Running the Chatbot](#running-the-chatbot)
5. [Usage Examples](#usage-examples)
6. [Manual Testing Guide](#manual-testing-guide)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum (CPU-Only Mode)
- **RAM**: 16GB (32GB recommended for optimal performance)
- **Storage**: 50GB free space for models
- **CPU**: Modern multi-core processor (Intel i5/AMD Ryzen 5 or better)
- **OS**: Windows 10/11, Linux, or macOS

### Recommended (GPU-Accelerated)
- **GPU**: NVIDIA RTX 3050 or better with 4GB+ VRAM
- **RAM**: 16GB system RAM
- **Storage**: 50GB SSD
- **CUDA**: 11.8 or higher

---

## Installation

### Step 1: Install Python Dependencies

```bash
cd "chatbot_app/medical_app"

# Install required packages
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121  # For CUDA 12.1
# OR for CPU only:
pip install torch torchvision torchaudio

# Install other dependencies
pip install transformers>=4.35.0
pip install accelerate>=0.25.0
pip install gradio>=4.0.0
pip install bitsandbytes>=0.41.0  # For quantization (optional, GPU only)
```

### Step 2: Verify MDSA Framework Installation

```bash
cd "../.."
pip install -e .  # Install MDSA framework in editable mode
```

---

## Model Download

The specialized medical SLMs will be automatically downloaded on first use. However, you can pre-download them:

### Option 1: Automatic Download (Recommended)
Simply run the chatbot - models download automatically on first query.

### Option 2: Manual Pre-Download

Use HuggingFace CLI to download models ahead of time:

```bash
# Install HuggingFace CLI
pip install huggingface-hub

# Login (optional, but recommended for gated models)
huggingface-cli login

# Download medical models
huggingface-cli download dmis-lab/llama-3-meerkat-8b-v1.0
huggingface-cli download microsoft/MediPhi-Instruct
huggingface-cli download aaditya/Llama3-OpenBioLLM-8B
huggingface-cli download stanford-crfm/BioMedLM
huggingface-cli download selinazarzour/healthgpt-tinyllama
```

### Model Storage Locations

Models are cached in:
- **Windows**: `C:\Users\<username>\.cache\huggingface\hub`
- **Linux/Mac**: `~/.cache/huggingface/hub`

Total storage needed: ~30-40GB

---

## Running the Chatbot

### Quick Start (CPU Mode)

```bash
cd chatbot_app/medical_app
python enhanced_medical_chatbot.py
```

The chatbot will start on `http://localhost:7860`

### Advanced Options

#### Enable GPU Acceleration

Edit `enhanced_medical_chatbot.py` (bottom of file):

```python
if __name__ == "__main__":
    create_gradio_interface(
        enable_reasoning=True,
        prefer_gpu=True,  # Change to True
        share=False
    )
```

#### Create Public Link (Share with Others)

```python
create_gradio_interface(
    enable_reasoning=True,
    prefer_gpu=False,
    share=True  # Creates public gradio.app link
)
```

#### Disable Hybrid Reasoning (Faster, Less Accurate)

```python
create_gradio_interface(
    enable_reasoning=False,  # Disable Phi-2 reasoning
    prefer_gpu=False,
    share=False
)
```

### Expected Startup Output

```
[INIT] Initializing Enhanced Medical Chatbot...
[INIT] Initializing medical knowledge base...
[INIT] Registering medical domains...
  - Clinical Diagnosis (Meerkat-8B) (dmis-lab/llama-3-meerkat-8b-v1.0)
  - Medical Coding & Billing (MediPhi) (microsoft/MediPhi-Instruct)
  - Biomedical Text Analysis (OpenBioLLM) (aaditya/Llama3-OpenBioLLM-8B)
  - Medical Q&A Lite (TinyLlama) (selinazarzour/healthgpt-tinyllama)
  - Radiology Support (BioMedLM) (stanford-crfm/BioMedLM)
[INIT] Enhanced Medical Chatbot ready!
[INIT] Registered 5 specialized medical domains
[INIT] Knowledge base: 43 global documents

============================================================
🏥 ENHANCED MEDICAL CHATBOT - READY
============================================================
Hybrid Reasoning: Enabled
GPU Acceleration: Disabled (CPU only)
Registered Domains: 5
============================================================

Running on local URL:  http://127.0.0.1:7860
```

---

## Usage Examples

### Clinical Diagnosis Queries

```
User: "Patient presents with chest pain, shortness of breath, and sweating. What are the differential diagnoses?"