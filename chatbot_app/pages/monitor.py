"""
Monitor Page - MDSA Dashboard

Real-time monitoring of models, requests, performance, and system info.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import json
from datetime import datetime
import sys

# Load shared metrics
metrics_file = Path("./chatbot_metrics.json")

def load_metrics():
    """Load metrics from shared file."""
    if metrics_file.exists():
        try:
            with open(metrics_file, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

metrics = load_metrics()

# Header
st.markdown('<h1 class="main-header">📊 Real-Time Monitoring</h1>', unsafe_allow_html=True)

# Auto-refresh
refresh_interval = st.sidebar.selectbox(
    "Auto-refresh interval",
    [("Off", 0), ("5 seconds", 5), ("10 seconds", 10), ("30 seconds", 30)],
    format_func=lambda x: x[0]
)[1]

if refresh_interval > 0:
    st.sidebar.info(f"Auto-refreshing every {refresh_interval} seconds")

# Check if chatbot is running
if metrics is None:
    st.warning("""
    ⚠️ **Chatbot Not Running**

    The chatbot is not currently running or no metrics are available.

    **To start the chatbot:**
    ```bash
    python chatbot.py
    ```

    **Note**: The chatbot must be running in the background for metrics to appear.
    """)
    st.stop()

# System Overview
st.markdown("### 🖥️ System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    status = metrics["system"]["status"]
    status_color = "🟢" if status == "running" else "🔴"
    st.metric("Status", f"{status_color} {status.upper()}")

with col2:
    st.metric("MDSA Version", metrics["system"]["mdsa_version"])

with col3:
    uptime = metrics["system"]["uptime_seconds"]
    uptime_str = f"{int(uptime // 60)}m {int(uptime % 60)}s" if uptime > 0 else "Just started"
    st.metric("Uptime", uptime_str)

with col4:
    last_update = datetime.fromisoformat(metrics["last_updated"])
    time_ago = (datetime.now() - last_update).total_seconds()
    st.metric("Last Update", f"{int(time_ago)}s ago")

st.markdown("---")

# Request Statistics
st.markdown("### 📈 Request Statistics")

col1, col2, col3, col4 = st.columns(4)

req = metrics["requests"]
with col1:
    st.metric("Total Requests", req["total"])

with col2:
    st.metric("Success", req["success"], delta=None, delta_color="normal")

with col3:
    st.metric("Errors", req["errors"], delta=None, delta_color="inverse")

with col4:
    success_rate = req["success_rate"]
    st.metric("Success Rate", f"{success_rate:.1f}%")

st.markdown("---")

# Performance Metrics
st.markdown("### ⚡ Performance Metrics")

perf = metrics["performance"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Avg Latency", f"{perf['avg_latency_ms']:.1f}ms")

with col2:
    st.metric("P95 Latency", f"{perf['p95_latency_ms']:.1f}ms")

with col3:
    st.metric("Avg Tokens", f"{perf['avg_tokens']:.1f}")

with col4:
    st.metric("Throughput", f"{perf['throughput_rps']:.2f} req/s")

st.markdown("---")

# Model Information
st.markdown("### 🤖 Loaded Models")

models_info = metrics["models"]
loaded_models = models_info["loaded"]

if loaded_models:
    # Model metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Models Loaded", f"{len(loaded_models)}/{models_info['max_models']}")

    with col2:
        st.metric("Total Memory", f"{models_info['total_memory_mb']:.1f} MB")

    with col3:
        avg_memory = models_info['total_memory_mb'] / len(loaded_models) if loaded_models else 0
        st.metric("Avg Memory/Model", f"{avg_memory:.1f} MB")

    # Model details table
    st.markdown("#### Model Details")

    model_data = []
    for model in loaded_models:
        model_data.append({
            "Model ID": model.get("id", "N/A"),
            "Name": model.get("name", "N/A"),
            "Memory (MB)": f"{model.get('memory_mb', 0):.1f}",
            "Uses": model.get("uses", 0),
            "Status": "✅ Active" if model.get("active", False) else "⏸️ Idle"
        })

    if model_data:
        st.dataframe(model_data, use_container_width=True)
else:
    st.info("No models currently loaded. Models will be loaded on first request.")

st.markdown("---")

# Domain Distribution
st.markdown("### 🎯 Domain Distribution")

domains = metrics["domains"]

if domains:
    # Create pie chart
    fig = px.pie(
        values=list(domains.values()),
        names=list(domains.keys()),
        title="Requests by Domain",
        hole=0.3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

    # Domain stats table
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Domain Statistics")
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / req["total"] * 100) if req["total"] > 0 else 0
            st.markdown(f"**{domain}**: {count} requests ({percentage:.1f}%)")

    with col2:
        st.markdown("#### Most Active Domain")
        if domains:
            top_domain = max(domains.items(), key=lambda x: x[1])
            st.success(f"**{top_domain[0]}** with {top_domain[1]} requests")
else:
    st.info("No domain data available yet. Make some requests to see distribution.")

st.markdown("---")

# RAG Status
st.markdown("### 📚 RAG (Retrieval-Augmented Generation)")

col1, col2, col3 = st.columns(3)

rag = metrics["rag"]

with col1:
    status_icon = "✅ Enabled" if rag["enabled"] else "❌ Disabled"
    st.metric("Status", status_icon)

with col2:
    st.metric("Documents", rag["documents"])

with col3:
    st.metric("Embedding Model", rag["embedding_model"])

if rag["enabled"]:
    st.success(f"""
    RAG is **active** with {rag['documents']} documents in the knowledge base.
    Using **{rag['embedding_model']}** for embeddings.
    """)
else:
    st.info("RAG is currently disabled. Enable it in chatbot configuration.")

st.markdown("---")

# Tools Status
st.markdown("### 🛠️ Tools & Capabilities")

col1, col2 = st.columns(2)

tools = metrics["tools"]

with col1:
    status_icon = "✅ Enabled" if tools["enabled"] else "❌ Disabled"
    st.metric("Tools Status", status_icon)

with col2:
    st.metric("Available Tools", len(tools["available"]))

if tools["enabled"] and tools["available"]:
    st.markdown("#### Registered Tools")

    # Create a nice grid of tools
    num_cols = 3
    cols = st.columns(num_cols)

    for idx, tool in enumerate(tools["available"]):
        with cols[idx % num_cols]:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{tool['name']}</h4>
                <p style="font-size: 0.9rem; color: #666;">{tool['description']}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No tools are currently available. Enable tools in chatbot configuration.")

st.markdown("---")

# Recent Requests
st.markdown("### 📝 Recent Requests")

recent = metrics.get("recent_requests", [])

if recent:
    st.markdown(f"Showing last {len(recent)} requests:")

    for req in recent[:10]:
        with st.expander(f"🔍 {req.get('query', 'N/A')[:50]}... | {req.get('timestamp', 'N/A')}"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Request Info**")
                st.markdown(f"- **Query**: {req.get('query', 'N/A')}")
                st.markdown(f"- **Domain**: {req.get('domain', 'N/A')}")
                st.markdown(f"- **Timestamp**: {req.get('timestamp', 'N/A')}")

            with col2:
                st.markdown("**Performance**")
                st.markdown(f"- **Latency**: {req.get('latency_ms', 0):.1f}ms")
                st.markdown(f"- **Tokens**: {req.get('tokens', 0)}")
                st.markdown(f"- **Status**: {req.get('status', 'unknown')}")

            st.markdown("**Response**")
            st.code(req.get('response', 'No response'), language=None)
else:
    st.info("No recent requests. Start chatting to see requests here.")

st.markdown("---")

# System Information (Detailed)
st.markdown("### 💻 System Configuration")

with st.expander("🔍 View System Details"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Python Environment**")
        st.markdown(f"- Python Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        st.markdown(f"- Platform: {sys.platform}")

        st.markdown("**Model Configuration**")
        st.markdown(f"- Max Models: {models_info['max_models']}")
        st.markdown(f"- Current Loaded: {len(loaded_models)}")
        st.markdown(f"- Total Memory: {models_info['total_memory_mb']:.1f} MB")

    with col2:
        st.markdown("**Feature Flags**")
        st.markdown(f"- RAG: {'✅' if rag['enabled'] else '❌'}")
        st.markdown(f"- Tools: {'✅' if tools['enabled'] else '❌'}")
        st.markdown(f"- Monitoring: ✅")

        st.markdown("**Framework Info**")
        st.markdown(f"- MDSA Version: {metrics['system']['mdsa_version']}")
        st.markdown(f"- Status: {metrics['system']['status']}")
        st.markdown(f"- Uptime: {uptime_str}")

# Debug Information
with st.expander("🔧 Debug Information"):
    st.json(metrics)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Monitoring active | MDSA Framework v{metrics['system']['mdsa_version']}</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh logic
if refresh_interval > 0:
    import time
    time.sleep(refresh_interval)
    st.rerun()
