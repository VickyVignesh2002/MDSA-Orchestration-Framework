"""
Settings Page - MDSA Dashboard

Configuration and settings management.
"""

import streamlit as st
from pathlib import Path
import json

# Header
st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)

st.markdown("### 🔧 Configuration Options")

# Model Settings
st.markdown("#### 🤖 Model Configuration")

model_name = st.text_input(
    "Default Model",
    value="gpt2",
    help="HuggingFace model name or Ollama model (e.g., 'llama3.2:1b')"
)

max_models = st.slider(
    "Maximum Models in Memory",
    min_value=1,
    max_value=5,
    value=2,
    help="Number of models to keep in LRU cache"
)

st.markdown("---")

# RAG Settings
st.markdown("#### 📚 RAG Settings")

enable_rag = st.checkbox("Enable RAG", value=True)

if enable_rag:
    kb_dir = st.text_input(
        "Knowledge Base Directory",
        value="./knowledge_base",
        help="Directory containing your documents"
    )

    embedding_model = st.selectbox(
        "Embedding Model",
        ["all-MiniLM-L6-v2", "all-mpnet-base-v2", "nomic-embed-text"],
        help="Sentence Transformers model for embeddings"
    )

st.markdown("---")

# Tools Settings
st.markdown("#### 🛠️ Tools Configuration")

enable_tools = st.checkbox("Enable Tool Calling", value=True)

if enable_tools:
    st.multiselect(
        "Active Tools",
        ["get_current_time", "calculate", "search_web", "get_weather",
         "word_count", "extract_urls", "convert_units"],
        default=["get_current_time", "calculate", "search_web", "get_weather"]
    )

st.markdown("---")

# Performance Settings
st.markdown("#### ⚡ Performance Settings")

col1, col2 = st.columns(2)

with col1:
    max_tokens = st.number_input(
        "Max Tokens per Response",
        min_value=50,
        max_value=500,
        value=150,
        step=10
    )

with col2:
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

st.markdown("---")

# Save Configuration
if st.button("💾 Save Configuration", type="primary"):
    config = {
        "model_name": model_name,
        "max_models": max_models,
        "enable_rag": enable_rag,
        "embedding_model": embedding_model if enable_rag else None,
        "knowledge_base_dir": kb_dir if enable_rag else None,
        "enable_tools": enable_tools,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    # Save to file
    config_file = Path("./chatbot_config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    st.success("✅ Configuration saved successfully!")
    st.info("Restart the chatbot for changes to take effect.")

st.markdown("---")

# Current Configuration
st.markdown("### 📋 Current Configuration")

config_file = Path("./chatbot_config.json")
if config_file.exists():
    with open(config_file, 'r') as f:
        current_config = json.load(f)

    st.json(current_config)
else:
    st.info("No saved configuration found. Using defaults.")

st.markdown("---")

# Advanced Settings
with st.expander("🔬 Advanced Settings"):
    st.markdown("#### Logging")

    log_level = st.selectbox(
        "Log Level",
        ["DEBUG", "INFO", "WARNING", "ERROR"],
        index=1
    )

    st.markdown("#### Monitoring")

    metrics_window = st.number_input(
        "Metrics Window Size",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100,
        help="Number of requests to keep in metrics"
    )

    st.markdown("#### Cache")

    if st.button("🗑️ Clear Model Cache"):
        st.warning("This will unload all models from memory.")
        st.info("Feature not yet implemented - restart chatbot to clear cache.")

    if st.button("🗑️ Clear Metrics"):
        metrics_file = Path("./chatbot_metrics.json")
        if metrics_file.exists():
            metrics_file.unlink()
            st.success("Metrics cleared!")
        else:
            st.info("No metrics file found.")

st.markdown("---")

# System Info
st.markdown("### 💻 System Information")

import sys
import platform

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Python**")
    st.markdown(f"- Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    st.markdown(f"- Platform: {sys.platform}")

with col2:
    st.markdown("**System**")
    st.markdown(f"- OS: {platform.system()}")
    st.markdown(f"- Architecture: {platform.machine()}")

st.markdown("---")

# Footer
from datetime import datetime

st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p>Settings Page | MDSA Framework v1.0.0</p>
    <p>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
