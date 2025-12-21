"""
Welcome Page - MDSA Dashboard

Shows installation verification and framework introduction.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Header
st.markdown('<h1 class="main-header">🎉 Welcome to MDSA Framework</h1>', unsafe_allow_html=True)

# Success Banner
st.markdown("""
<div class="success-banner">
    <h2>✅ Installation Successful!</h2>
    <p>The MDSA (Multi-Domain Small Language Model Agentic Orchestration Framework) has been successfully installed and configured.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Framework Overview
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 Framework Features")
    st.markdown("""
    ✅ **Multi-Domain Routing**
    Automatically detect and route queries to specialized domains

    ✅ **RAG Integration**
    ChromaDB vector database with Sentence Transformers

    ✅ **Tool Calling**
    Extensible tool registry with 8 built-in tools

    ✅ **LRU Model Caching**
    Intelligent model management with automatic eviction

    ✅ **Real-Time Monitoring**
    Comprehensive metrics and performance tracking

    ✅ **Free & Open Source**
    No API keys required, completely free
    """)

with col2:
    st.markdown("### 📦 System Information")

    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    st.metric("Python Version", python_version)

    # Check MDSA installation
    try:
        import mdsa
        mdsa_status = "✅ Installed"
        mdsa_color = "green"
    except ImportError:
        mdsa_status = "❌ Not Found"
        mdsa_color = "red"

    st.markdown(f"**MDSA Framework**: :{mdsa_color}[{mdsa_status}]")

    # Check dependencies
    dependencies = {
        "ChromaDB": "chromadb",
        "Sentence Transformers": "sentence_transformers",
        "Streamlit": "streamlit",
        "Torch": "torch"
    }

    st.markdown("**Dependencies**:")
    for name, module in dependencies.items():
        try:
            __import__(module)
            st.markdown(f"- {name}: :green[✅ Installed]")
        except ImportError:
            st.markdown(f"- {name}: :red[❌ Missing]")

st.markdown("---")

# Quick Start Guide
st.markdown("### 🏃 Quick Start Guide")

tab1, tab2, tab3 = st.tabs(["💬 Chatbot", "📊 Dashboard", "🔧 Configuration"])

with tab1:
    st.markdown("""
    **Start the Interactive Chatbot:**

    ```bash
    cd chatbot_app
    python chatbot.py
    ```

    **Features Available:**
    - Multi-domain question answering
    - RAG-enhanced responses from knowledge base
    - Tool calling (time, weather, calculations, etc.)
    - Conversation history tracking
    """)

with tab2:
    st.markdown("""
    **Start the Monitoring Dashboard:**

    ```bash
    cd chatbot_app
    streamlit run app.py
    ```

    **Dashboard Pages:**
    - 🏠 **Welcome**: This page - installation verification
    - 📊 **Monitor**: Real-time model and performance monitoring
    - ⚙️ **Settings**: Configuration management
    """)

with tab3:
    st.markdown("""
    **Configure Local Models:**

    Edit `chatbot.py` to use your local models:

    ```python
    chatbot = MDSAChatbot(
        model_name="llama3.2:1b",      # Your Ollama model
        max_models=2,                   # Max models in memory
        enable_rag=True,                # Enable RAG
        enable_tools=True,              # Enable tool calling
        knowledge_base_dir="./knowledge_base"
    )
    ```

    **Supported Models:**
    - HuggingFace models (gpt2, phi3, etc.)
    - Ollama models (llama3.2, qwen2.5, etc.)
    - Custom fine-tuned models
    """)

st.markdown("---")

# Available Local Models
st.markdown("### 🤖 Available Local Models")

st.info("""
**Detected Local Models:**
(These should be your Ollama/HuggingFace models)

- `llama3.2:1b` - Llama 3.2 1B parameters
- `llama3.2:3b-instruct-q4_0` - Llama 3.2 3B instruct (quantized)
- `phi3:mini` - Microsoft Phi-3 Mini
- `qwen2.5:3b-instruct` - Qwen 2.5 3B instruct
- `gpt-oss:20b-c10ud` - GPT-OSS 20B
- `gpt-oss:120b-c10ud` - GPT-OSS 120B
- `nomic-embed-text:latest` - Nomic Embed (embeddings)

**Note**: The chatbot will use these models for inference when configured.
""")

st.markdown("---")

# Knowledge Base Status
st.markdown("### 📚 Knowledge Base Status")

kb_dir = Path("./knowledge_base")
if kb_dir.exists():
    files = list(kb_dir.glob("*.txt")) + list(kb_dir.glob("*.md")) + list(kb_dir.glob("*.pdf"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Documents Found", len(files))
    with col2:
        total_size = sum(f.stat().st_size for f in files) / 1024  # KB
        st.metric("Total Size", f"{total_size:.1f} KB")
    with col3:
        st.metric("Status", "✅ Ready")

    if files:
        st.markdown("**Files:**")
        for f in files[:5]:  # Show first 5
            st.markdown(f"- `{f.name}` ({f.stat().st_size / 1024:.1f} KB)")

        if len(files) > 5:
            st.markdown(f"*... and {len(files) - 5} more files*")
else:
    st.warning("Knowledge base directory not found. Create `./knowledge_base/` and add documents.")

st.markdown("---")

# Next Steps
st.markdown("### 🎯 Next Steps")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **1. Test the Chatbot**

    Run the chatbot and ask questions:
    - "What is machine learning?"
    - "What's the current time?"
    - "Calculate 25 * 4"
    """)

with col2:
    st.markdown("""
    **2. Monitor Performance**

    Go to the Monitor page to view:
    - Model performance
    - Request statistics
    - System metrics
    """)

with col3:
    st.markdown("""
    **3. Customize**

    Add your own:
    - Domains
    - Tools
    - Knowledge base documents
    """)

st.markdown("---")

# Footer
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p><strong>MDSA Framework v1.0.0</strong></p>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>For support and documentation, visit the GitHub repository</p>
</div>
""", unsafe_allow_html=True)
