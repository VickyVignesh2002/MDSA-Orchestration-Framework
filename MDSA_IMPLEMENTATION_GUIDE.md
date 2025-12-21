# MDSA Framework - Complete Implementation Guide

**Version**: 1.0.0
**Date**: 2025-12-11
**Framework**: Multi-Domain Small Language Model Agentic Orchestration Framework

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start (3 Steps)](#quick-start-3-steps)
4. [Core Concepts](#core-concepts)
5. [Framework Architecture](#framework-architecture)
6. [Integration Examples](#integration-examples)
7. [Advanced Features](#advanced-features)
8. [Project Structure](#project-structure)
9. [Configuration Best Practices](#configuration-best-practices)
10. [Deployment Guide](#deployment-guide)
11. [Troubleshooting](#troubleshooting)
12. [API Reference](#api-reference)

---

## Overview

MDSA is a production-ready Python framework for orchestrating domain-specialized small language models. It provides:

- **Hybrid Orchestration**: TinyBERT for intent routing + Phi-2 for complex reasoning
- **Dual RAG System**: Global knowledge base + domain-specific local knowledge
- **Multi-Model Support**: Integrate Ollama cloud models or local models
- **Framework Agnostic**: Works with FastAPI, Flask, Gradio, Streamlit
- **Production Ready**: Built-in monitoring, metrics, and error handling

### Key Features

- Intent-based domain routing with 95%+ accuracy
- Privacy-preserving local RAG per domain
- Tool calling and workflow orchestration
- Real-time monitoring and metrics dashboard
- Automatic model quantization and optimization
- Hardware-aware execution (CPU/GPU)

---

## Prerequisites

### System Requirements

**Minimum**:
- Python 3.9+
- 8GB RAM
- 20GB disk space
- CPU only (slower inference)

**Recommended**:
- Python 3.10+
- 16GB RAM
- 50GB disk space
- GPU with 8GB VRAM (NVIDIA CUDA)

**Optimal**:
- Python 3.11+
- 32GB RAM
- 100GB disk space
- GPU with 24GB VRAM

### Software Dependencies

```bash
# Core dependencies
pip install transformers>=4.35.0
pip install torch>=2.0.0
pip install sentence-transformers>=2.2.0
pip install chromadb>=0.4.0

# API frameworks (choose based on your needs)
pip install fastapi>=0.104.0
pip install uvicorn[standard]>=0.24.0
pip install gradio>=6.0.0
pip install streamlit>=1.28.0
pip install flask>=3.0.0

# Additional utilities
pip install pydantic>=2.5.0
pip install ollama>=0.1.0
pip install python-dotenv>=1.0.0
pip install numpy>=1.24.0
```

### Optional Dependencies

```bash
# For GPU acceleration
pip install accelerate>=0.24.0

# For quantization
pip install bitsandbytes>=0.41.0

# For monitoring UI
pip install plotly>=5.17.0
pip install dash>=2.14.0
```

---

## Quick Start (3 Steps)

### Step 1: Initialize MDSA Orchestrator

```python
from mdsa.core.orchestrator import TinyBERTOrchestrator

# Create orchestrator instance
orchestrator = TinyBERTOrchestrator(
    intent_model_path="model-best-tinybert",  # Your trained TinyBERT model
    reasoning_model_path="microsoft/phi-2",     # Phi-2 for complex reasoning
    device="auto",                              # Auto-detect GPU/CPU
    use_reasoning_threshold=0.7                 # Trigger reasoning for low confidence
)

print("Orchestrator initialized successfully!")
```

### Step 2: Register Your Domains

```python
from mdsa.domains import DomainConfig

# Define a domain
customer_support = DomainConfig(
    name="customer_support",
    description="Handle customer inquiries, complaints, and support tickets",
    model_name="ollama://llama3:8b",  # Any Ollama model
    keywords=["help", "support", "issue", "problem", "complaint"],
    system_prompt="You are a helpful and empathetic customer support agent. Provide clear, professional assistance.",
    max_tokens=500,
    temperature=0.7
)

# Register with orchestrator
orchestrator.register_domain(
    name=customer_support.name,
    description=customer_support.description,
    keywords=customer_support.keywords
)

print(f"Domain '{customer_support.name}' registered successfully!")
```

### Step 3: Process User Requests

```python
# Process a user message
result = orchestrator.process_request(
    message="My order #12345 is delayed. Can you help me track it?",
    context={
        "user_id": "user_001",
        "session_id": "sess_abc123",
        "order_id": "12345"
    }
)

# Extract results
print(f"Response: {result['response']}")
print(f"Domain: {result['domain']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Reasoning Used: {result.get('used_reasoning', False)}")
```

**Output**:
```
Response: I'd be happy to help you track your order #12345...
Domain: customer_support
Confidence: 94.23%
Reasoning Used: False
```

---

## Core Concepts

### 1. Orchestrator

The **TinyBERTOrchestrator** is the central component that:
- Routes user queries to appropriate domains
- Triggers reasoning model for complex queries
- Manages model lifecycle and execution
- Collects metrics and handles errors

### 2. Domains

**Domains** are specialized areas of functionality, each with:
- Dedicated SLM (Small Language Model)
- Domain-specific prompt templates
- Custom keywords for routing
- Optional local RAG knowledge base

### 3. Dual RAG System

**DualRAG** provides two-tier knowledge retrieval:

**Global RAG**:
- Shared knowledge across all domains
- Company-wide policies, FAQs, general info
- Accessible by all domain models

**Local RAG**:
- Domain-specific knowledge
- Private to each domain for data isolation
- Medical records, financial data, etc.

### 4. Intent Router

The **IntentRouter** uses TinyBERT to classify user intent:
- 14M parameter model for fast inference (<10ms)
- Fine-tuned on domain-specific intents
- Returns confidence scores for routing decisions

### 5. Reasoning Model

**Phi-2** (2.7B parameters) handles:
- Complex multi-step reasoning
- Ambiguous queries requiring clarification
- Cross-domain queries
- Triggered when intent confidence < threshold

---

## Framework Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Request                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              TinyBERTOrchestrator                            │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ IntentRouter │───▶│ DomainRouter │───▶│ ModelManager │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│           │                                      │           │
│           ▼                                      ▼           │
│  ┌──────────────┐                      ┌──────────────┐    │
│  │   Phi-2      │                      │ Domain SLMs  │    │
│  │  Reasoning   │                      │ (Ollama)     │    │
│  └──────────────┘                      └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      DualRAG                                 │
│  ┌──────────────┐              ┌──────────────┐            │
│  │  Global RAG  │              │  Local RAG   │            │
│  │ (Shared KB)  │              │ (Per Domain) │            │
│  └──────────────┘              └──────────────┘            │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Response + Metadata                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Integration Examples

### Example 1: FastAPI REST API

**File**: `main.py`

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mdsa.core.orchestrator import TinyBERTOrchestrator
import uvicorn

# Initialize FastAPI
app = FastAPI(title="MDSA API", version="1.0.0")

# Initialize orchestrator (singleton)
orchestrator = TinyBERTOrchestrator(
    intent_model_path="model-best-tinybert",
    reasoning_model_path="microsoft/phi-2",
    device="auto"
)

# Register domains
orchestrator.register_domain(
    name="customer_support",
    description="Handle customer inquiries",
    keywords=["help", "support", "issue"]
)

# Request model
class ChatRequest(BaseModel):
    message: str
    user_id: str = None
    context: dict = {}

# Response model
class ChatResponse(BaseModel):
    response: str
    domain: str
    confidence: float
    latency_ms: float

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process chat message"""
    try:
        result = orchestrator.process_request(
            message=request.message,
            context={**request.context, "user_id": request.user_id}
        )
        return ChatResponse(
            response=result["response"],
            domain=result["domain"],
            confidence=result["confidence"],
            latency_ms=result.get("latency_ms", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    stats = orchestrator.get_stats()
    return {
        "status": "healthy",
        "requests_total": stats["requests_total"],
        "domains_registered": stats["domains_registered"]
    }

@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    return orchestrator.get_stats()

# Run server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Run**:
```bash
python main.py
# Or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Test**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need help with my order", "user_id": "user_001"}'
```

---

### Example 2: Gradio Web UI

**File**: `app_gradio.py`

```python
import gradio as gr
from mdsa.core.orchestrator import TinyBERTOrchestrator

# Initialize orchestrator
orchestrator = TinyBERTOrchestrator(
    intent_model_path="model-best-tinybert",
    reasoning_model_path="microsoft/phi-2",
    device="auto"
)

# Register domains
orchestrator.register_domain(
    name="customer_support",
    description="Customer support and inquiries",
    keywords=["help", "support", "issue", "problem"]
)

# Chat function
def chat(message, history):
    """Process message and return response"""
    if not message.strip():
        return history

    # Process request
    result = orchestrator.process_request(message=message)

    # Append to history in Gradio 6.1.0 format
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": result["response"]})

    return history

# Create interface
with gr.Blocks(title="MDSA Chatbot") as demo:
    gr.Markdown("# MDSA Multi-Domain Chatbot")

    chatbot = gr.Chatbot(
        label="Conversation",
        height=500,
        avatar_images=(None, "🤖")
    )

    msg = gr.Textbox(
        label="Your message",
        placeholder="Type your message here...",
        lines=2
    )

    send_btn = gr.Button("Send", variant="primary")
    clear_btn = gr.Button("Clear")

    # Event handlers
    send_btn.click(
        fn=chat,
        inputs=[msg, chatbot],
        outputs=[chatbot]
    ).then(
        lambda: "",
        outputs=[msg]
    )

    msg.submit(
        fn=chat,
        inputs=[msg, chatbot],
        outputs=[chatbot]
    ).then(
        lambda: "",
        outputs=[msg]
    )

    clear_btn.click(lambda: [], outputs=[chatbot])

# Launch
demo.launch(server_name="0.0.0.0", server_port=7860)
```

**Run**:
```bash
python app_gradio.py
```

---

### Example 3: Flask Application

**File**: `app_flask.py`

```python
from flask import Flask, request, jsonify, render_template_string
from mdsa.core.orchestrator import TinyBERTOrchestrator

app = Flask(__name__)

# Initialize orchestrator
orchestrator = TinyBERTOrchestrator(
    intent_model_path="model-best-tinybert",
    reasoning_model_path="microsoft/phi-2",
    device="auto"
)

# Register domains
orchestrator.register_domain(
    name="customer_support",
    description="Handle customer inquiries",
    keywords=["help", "support", "issue"]
)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MDSA Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        #chat-container { border: 1px solid #ddd; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #e3f2fd; text-align: right; }
        .bot { background: #f5f5f5; text-align: left; }
        #input-container { display: flex; gap: 10px; }
        #message-input { flex: 1; padding: 10px; }
        #send-button { padding: 10px 20px; background: #2196F3; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>MDSA Multi-Domain Chatbot</h1>
    <div id="chat-container"></div>
    <div id="input-container">
        <input type="text" id="message-input" placeholder="Type your message...">
        <button id="send-button">Send</button>
    </div>

    <script>
        const chatContainer = document.getElementById('chat-container');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');

        function addMessage(content, isUser) {
            const div = document.createElement('div');
            div.className = `message ${isUser ? 'user' : 'bot'}`;
            div.textContent = content;
            chatContainer.appendChild(div);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage(message, true);
            messageInput.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                const data = await response.json();
                addMessage(data.response, false);
            } catch (error) {
                addMessage('Error: ' + error.message, false);
            }
        }

        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    """Render chat interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/chat", methods=["POST"])
def chat():
    """Process chat message"""
    data = request.json
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    try:
        result = orchestrator.process_request(message=message)
        return jsonify({
            "response": result["response"],
            "domain": result["domain"],
            "confidence": result["confidence"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/metrics")
def metrics():
    """Get system metrics"""
    return jsonify(orchestrator.get_stats())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

**Run**:
```bash
python app_flask.py
# Or
flask run --host=0.0.0.0 --port=5000
```

---

### Example 4: Streamlit Dashboard

**File**: `app_streamlit.py`

```python
import streamlit as st
from mdsa.core.orchestrator import TinyBERTOrchestrator

# Page config
st.set_page_config(page_title="MDSA Chatbot", page_icon="🤖", layout="wide")

# Initialize orchestrator (cached)
@st.cache_resource
def get_orchestrator():
    orch = TinyBERTOrchestrator(
        intent_model_path="model-best-tinybert",
        reasoning_model_path="microsoft/phi-2",
        device="auto"
    )
    orch.register_domain(
        name="customer_support",
        description="Customer support",
        keywords=["help", "support"]
    )
    return orch

orchestrator = get_orchestrator()

# Title
st.title("🤖 MDSA Multi-Domain Chatbot")

# Sidebar - Metrics
with st.sidebar:
    st.header("System Metrics")
    stats = orchestrator.get_stats()
    st.metric("Total Requests", stats["requests_total"])
    st.metric("Success Rate", f"{stats['success_rate']:.1%}")
    st.metric("Avg Latency", f"{stats['average_latency_ms']:.1f}ms")
    st.metric("Domains", stats["domains_registered"])

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = orchestrator.process_request(message=prompt)
            response = result["response"]
            st.markdown(response)

            # Show metadata
            with st.expander("View Metadata"):
                st.json({
                    "domain": result["domain"],
                    "confidence": f"{result['confidence']:.2%}",
                    "latency_ms": result.get("latency_ms", 0)
                })

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
```

**Run**:
```bash
streamlit run app_streamlit.py
```

---

## Advanced Features

### 1. Adding RAG System

```python
from mdsa.core.dual_rag import DualRAG

# Initialize DualRAG
rag = DualRAG(
    global_collection_name="company_knowledge",
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    persist_directory="./chroma_db"
)

# Add global documents (shared across all domains)
global_docs = [
    {
        "content": "Our company return policy allows returns within 30 days of purchase.",
        "metadata": {"type": "policy", "category": "returns"}
    },
    {
        "content": "Customer service hours are Monday-Friday, 9 AM to 5 PM EST.",
        "metadata": {"type": "info", "category": "hours"}
    },
    {
        "content": "We offer free shipping on orders over $50.",
        "metadata": {"type": "policy", "category": "shipping"}
    }
]
rag.add_global_documents(global_docs)

# Add domain-specific documents
support_docs = [
    {
        "content": "For order tracking issues, first check the tracking number in the confirmation email.",
        "metadata": {"type": "guide", "priority": "high"}
    },
    {
        "content": "If package is lost, contact carrier first, then customer service.",
        "metadata": {"type": "guide", "priority": "medium"}
    }
]
rag.add_local_documents(domain="customer_support", documents=support_docs)

# Query RAG (retrieves from both global and local)
results = rag.query(
    query="What is your return policy?",
    domain="customer_support",
    top_k=3,
    use_local=True,
    use_global=True
)

for doc in results:
    print(f"Content: {doc['content']}")
    print(f"Score: {doc['score']:.3f}")
    print(f"Source: {doc['metadata']}")
    print("---")
```

### 2. Tool Registration and Execution

```python
from mdsa.tools import Tool, ToolRegistry

# Create tool registry
registry = ToolRegistry()

# Define a tool
def get_order_status(order_id: str) -> dict:
    """Get order status by ID"""
    # Mock implementation
    return {
        "order_id": order_id,
        "status": "In Transit",
        "estimated_delivery": "2025-12-15",
        "tracking_number": "1Z999AA1234567890"
    }

# Register tool
tool = Tool(
    name="get_order_status",
    description="Retrieve the current status of an order by ID",
    function=get_order_status,
    parameters={
        "order_id": {"type": "string", "description": "The order ID to lookup"}
    }
)
registry.register(tool)

# Execute tool
result = registry.execute("get_order_status", order_id="ORD-12345")
print(result)
```

### 3. Custom Domain with Tools

```python
from mdsa.domains import DomainConfig

# Create domain with tools
order_tracking_domain = DomainConfig(
    name="order_tracking",
    description="Track and manage customer orders",
    model_name="ollama://llama3:8b",
    keywords=["order", "tracking", "delivery", "shipment"],
    system_prompt="""You are an order tracking assistant.
Use the get_order_status tool to retrieve order information.
Provide clear, helpful responses about order status and delivery.""",
    tools=["get_order_status"],  # Reference to registered tools
    max_tokens=300,
    temperature=0.5
)

# Register domain
orchestrator.register_domain(
    name=order_tracking_domain.name,
    description=order_tracking_domain.description,
    keywords=order_tracking_domain.keywords
)
```

### 4. Monitoring and Metrics

```python
# Get comprehensive statistics
stats = orchestrator.get_stats()

print(f"Total Requests: {stats['requests_total']}")
print(f"Successful: {stats['requests_success']}")
print(f"Failed: {stats['requests_failed']}")
print(f"Success Rate: {stats['success_rate']:.2%}")
print(f"Average Latency: {stats['average_latency_ms']:.2f}ms")
print(f"Domains Registered: {stats['domains_registered']}")

# Domain-specific stats
print("\nDomain Statistics:")
for domain, count in stats['domain_stats'].items():
    print(f"  {domain}: {count} requests")

# Message bus stats
bus_stats = stats['message_bus']
print(f"\nMessage Bus: {bus_stats['total_messages']} messages")
print(f"Active Subscribers: {bus_stats['active_subscribers']}")
```

---

## Project Structure

### Recommended Structure

```
your_project/
├── main.py                      # Application entry point
├── config.py                    # Configuration management
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── domains/                     # Domain definitions
│   ├── __init__.py
│   ├── customer_support.py
│   ├── order_tracking.py
│   └── technical_support.py
├── knowledge_base/              # RAG documents
│   ├── global/
│   │   ├── policies.json
│   │   ├── faqs.json
│   │   └── company_info.json
│   └── local/
│       ├── customer_support/
│       ├── order_tracking/
│       └── technical_support/
├── models/                      # Downloaded models
│   ├── model-best-tinybert/
│   └── phi-2/
├── tools/                       # Custom tools
│   ├── __init__.py
│   ├── order_tools.py
│   └── crm_tools.py
├── tests/                       # Unit tests
│   ├── test_orchestrator.py
│   ├── test_domains.py
│   └── test_rag.py
├── logs/                        # Application logs
└── chroma_db/                   # ChromaDB persistence
```

### Example config.py

```python
import os
from dotenv import load_dotenv
from mdsa.utils import ConfigLoader

load_dotenv()

class Config:
    # Model paths
    INTENT_MODEL_PATH = os.getenv("INTENT_MODEL_PATH", "./models/model-best-tinybert")
    REASONING_MODEL_PATH = os.getenv("REASONING_MODEL_PATH", "microsoft/phi-2")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    # Ollama configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Hardware
    DEVICE = os.getenv("DEVICE", "auto")  # auto, cuda, cpu

    # RAG configuration
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    GLOBAL_COLLECTION_NAME = os.getenv("GLOBAL_COLLECTION_NAME", "global_knowledge")

    # Orchestrator settings
    USE_REASONING_THRESHOLD = float(os.getenv("USE_REASONING_THRESHOLD", "0.7"))
    DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "500"))
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))

    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "./logs")
```

### Example .env

```env
# Model Configuration
INTENT_MODEL_PATH=./models/model-best-tinybert
REASONING_MODEL_PATH=microsoft/phi-2
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Ollama
OLLAMA_BASE_URL=http://localhost:11434

# Hardware
DEVICE=auto

# RAG
CHROMA_PERSIST_DIR=./chroma_db
GLOBAL_COLLECTION_NAME=company_knowledge

# Orchestrator
USE_REASONING_THRESHOLD=0.7
DEFAULT_MAX_TOKENS=500
DEFAULT_TEMPERATURE=0.7

# API
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_DIR=./logs
```

---

## Configuration Best Practices

### 1. Environment Variables

Always use environment variables for sensitive configuration:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Good - from environment
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# ❌ Bad - hardcoded
OLLAMA_API_KEY = "sk-abcd1234"
DATABASE_URL = "postgresql://user:pass@localhost/db"
```

### 2. Model Selection

Choose models based on use case:

| Use Case | Model | Parameters | VRAM | Latency |
|----------|-------|------------|------|---------|
| Intent Classification | TinyBERT | 14M | 1GB | <10ms |
| Simple QA | Ollama Phi-2 | 2.7B | 4GB | 50-100ms |
| Complex Reasoning | Ollama Llama-3 | 8B | 8GB | 200-500ms |
| Multi-modal | Ollama Qwen-VL | 235B | 24GB | 1-2s |

### 3. Resource Management

```python
from mdsa.utils import HardwareDetector

# Detect available hardware
detector = HardwareDetector()
print(f"GPU Available: {detector.has_gpu()}")
print(f"GPU Memory: {detector.gpu_memory_gb():.1f} GB")
print(f"Recommended Device: {detector.get_recommended_device()}")

# Configure based on hardware
if detector.has_gpu() and detector.gpu_memory_gb() >= 8:
    device = "cuda"
    batch_size = 16
else:
    device = "cpu"
    batch_size = 4

orchestrator = TinyBERTOrchestrator(
    intent_model_path="model-best-tinybert",
    reasoning_model_path="microsoft/phi-2",
    device=device
)
```

### 4. Error Handling

```python
import logging
from mdsa.utils import setup_logger

# Setup logging
logger = setup_logger("mdsa_app", level=logging.INFO, log_dir="./logs")

try:
    result = orchestrator.process_request(message="Test message")
except Exception as e:
    logger.error(f"Request processing failed: {str(e)}", exc_info=True)
    # Handle error gracefully
    result = {
        "response": "I'm sorry, I encountered an error. Please try again.",
        "domain": "error",
        "confidence": 0.0
    }
```

---

## Deployment Guide

### 1. Docker Deployment

**Dockerfile**:

```dockerfile
FROM python:3.11-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose ports
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:

```yaml
version: '3.8'

services:
  mdsa-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - INTENT_MODEL_PATH=/models/model-best-tinybert
      - DEVICE=cpu
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - ./models:/models
      - ./chroma_db:/app/chroma_db
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  ollama_data:
```

**Build and run**:

```bash
docker-compose up -d
```

### 2. Kubernetes Deployment

**deployment.yaml**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mdsa-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mdsa-api
  template:
    metadata:
      labels:
        app: mdsa-api
    spec:
      containers:
      - name: mdsa-api
        image: your-registry/mdsa-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DEVICE
          value: "cpu"
        - name: OLLAMA_BASE_URL
          value: "http://ollama-service:11434"
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        volumeMounts:
        - name: models
          mountPath: /models
        - name: chroma-db
          mountPath: /app/chroma_db
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: models-pvc
      - name: chroma-db
        persistentVolumeClaim:
          claimName: chroma-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: mdsa-api-service
spec:
  selector:
    app: mdsa-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 3. Production Checklist

- [ ] Use production ASGI server (Gunicorn + Uvicorn workers)
- [ ] Enable HTTPS/TLS encryption
- [ ] Set up monitoring and alerting (Prometheus, Grafana)
- [ ] Configure log aggregation (ELK stack, CloudWatch)
- [ ] Implement rate limiting and authentication
- [ ] Set up CI/CD pipeline
- [ ] Configure auto-scaling based on load
- [ ] Regular model updates and retraining
- [ ] Database backups for RAG data
- [ ] Security scanning and vulnerability patching

---

## Troubleshooting

### Common Issues

#### 1. ImportError: cannot import name 'RequestLogger'

**Error**:
```
ImportError: cannot import name 'RequestLogger' from 'mdsa.monitoring'
```

**Fix**:
```python
# ❌ Wrong
from mdsa.monitoring import RequestLogger, MetricsCollector

# ✅ Correct
from mdsa.monitoring import MonitoringService, RequestMetric
```

#### 2. AttributeError: 'TinyBERTOrchestrator' object has no attribute 'get_statistics'

**Error**:
```
AttributeError: 'TinyBERTOrchestrator' object has no attribute 'get_statistics'
```

**Fix**:
```python
# ❌ Wrong
stats = orchestrator.get_statistics()

# ✅ Correct
stats = orchestrator.get_stats()
```

#### 3. Gradio Message Format Error

**Error**:
```
gradio.exceptions.Error: "Data incompatible with messages format"
```

**Fix**:
```python
# ❌ Wrong (old tuple format)
history.append((user_message, bot_response))

# ✅ Correct (dictionary format for Gradio 6.1.0+)
history.append({"role": "user", "content": user_message})
history.append({"role": "assistant", "content": bot_response})
```

#### 4. Ollama Connection Refused

**Error**:
```
requests.exceptions.ConnectionError: Connection refused
```

**Fix**:
```bash
# Start Ollama server
ollama serve

# Test connection
curl http://localhost:11434/api/tags

# Pull required model
ollama pull llama3:8b
```

#### 5. CUDA Out of Memory

**Error**:
```
torch.cuda.OutOfMemoryError: CUDA out of memory
```

**Fix**:
```python
# Option 1: Use smaller model
orchestrator = TinyBERTOrchestrator(
    reasoning_model_path="microsoft/phi-2",  # 2.7B instead of 7B+
    device="cuda"
)

# Option 2: Enable quantization
from mdsa.models import QuantizationType

orchestrator = TinyBERTOrchestrator(
    reasoning_model_path="microsoft/phi-2",
    device="cuda",
    quantization=QuantizationType.INT8  # Reduce memory usage
)

# Option 3: Use CPU
orchestrator = TinyBERTOrchestrator(
    reasoning_model_path="microsoft/phi-2",
    device="cpu"
)
```

---

## API Reference

### TinyBERTOrchestrator

```python
class TinyBERTOrchestrator:
    def __init__(
        self,
        intent_model_path: str,
        reasoning_model_path: str = "microsoft/phi-2",
        device: str = "auto",
        use_reasoning_threshold: float = 0.7,
        quantization: Optional[QuantizationType] = None
    ):
        """
        Initialize MDSA Orchestrator.

        Args:
            intent_model_path: Path to TinyBERT model for intent classification
            reasoning_model_path: Path or Hugging Face model ID for reasoning
            device: Device to use ('auto', 'cuda', 'cpu')
            use_reasoning_threshold: Confidence threshold to trigger reasoning model
            quantization: Optional quantization type (INT8, INT4)
        """

    def register_domain(
        self,
        name: str,
        description: str,
        keywords: List[str],
        model_name: Optional[str] = None
    ) -> None:
        """Register a new domain."""

    def process_request(
        self,
        message: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Process user request and return response.

        Args:
            message: User input message
            context: Optional context dictionary

        Returns:
            Dict containing:
                - response: Generated response text
                - domain: Detected domain name
                - confidence: Routing confidence score
                - latency_ms: Processing time in milliseconds
                - used_reasoning: Whether reasoning model was used
        """

    def get_stats(self) -> Dict[str, Any]:
        """
        Get orchestrator statistics.

        Returns:
            Dict containing:
                - requests_total: Total requests processed
                - requests_success: Successful requests
                - requests_failed: Failed requests
                - success_rate: Success rate (0.0-1.0)
                - average_latency_ms: Average latency in milliseconds
                - domains_registered: Number of registered domains
                - domain_stats: Per-domain request counts
        """
```

### DualRAG

```python
class DualRAG:
    def __init__(
        self,
        global_collection_name: str = "global_knowledge",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        persist_directory: str = "./chroma_db"
    ):
        """Initialize Dual RAG system."""

    def add_global_documents(self, documents: List[Dict]) -> None:
        """Add documents to global knowledge base."""

    def add_local_documents(
        self,
        domain: str,
        documents: List[Dict]
    ) -> None:
        """Add documents to domain-specific local knowledge base."""

    def query(
        self,
        query: str,
        domain: Optional[str] = None,
        top_k: int = 5,
        use_local: bool = True,
        use_global: bool = True
    ) -> List[Dict]:
        """
        Query RAG system for relevant documents.

        Args:
            query: Search query
            domain: Domain name for local RAG
            top_k: Number of results to return
            use_local: Whether to search local RAG
            use_global: Whether to search global RAG

        Returns:
            List of documents with content, score, and metadata
        """
```

---

## Conclusion

This guide covers the complete implementation of the MDSA framework for any project. Key takeaways:

1. **Quick Start**: Initialize orchestrator, register domains, process requests (3 steps)
2. **Framework Agnostic**: Works with FastAPI, Flask, Gradio, Streamlit
3. **Production Ready**: Built-in monitoring, error handling, and deployment guides
4. **Flexible Architecture**: Dual RAG, tool calling, custom domains
5. **Well Documented**: Troubleshooting, API reference, and examples

For more information:
- GitHub: https://github.com/your-org/mdsa
- Documentation: https://mdsa.readthedocs.io
- Issues: https://github.com/your-org/mdsa/issues

**Next Steps**:
1. Follow Quick Start to build your first MDSA application
2. Choose integration example (FastAPI/Flask/Gradio/Streamlit)
3. Add RAG system for domain knowledge
4. Deploy to production using Docker/Kubernetes
5. Monitor and optimize based on metrics

Happy building with MDSA! 🚀
