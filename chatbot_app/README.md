# MDSA Chatbot Application

**Multi-Domain Chatbot with RAG, Tool Calling, and Real-time Monitoring**

All components are **FREE and OPEN SOURCE** - no API keys required!

---

## 🎯 Features

✅ **MDSA Framework Integration**
- Multi-domain routing with automatic domain detection
- Uses local models from your machine (no API keys!)
- Supports ANY HuggingFace model

✅ **RAG (Retrieval-Augmented Generation)**
- ChromaDB for vector storage (free, open-source)
- Sentence Transformers for embeddings (free)
- Supports PDF, TXT, MD files
- Persistent storage

✅ **Tool Calling**
- 8+ built-in tools (time, calculator, weather, web search, etc.)
- DuckDuckGo for web search (no API key)
- wttr.in for weather (no API key)
- Easy to add custom tools

✅ **Real-time Monitoring**
- Streamlit dashboard with live metrics
- Request logging and performance tracking
- Model monitoring (memory, latency, throughput)
- Export to JSON/CSV

---

## 📦 Installation

### 1. Install Dependencies

```bash
cd chatbot_app
pip install -r requirements.txt
```

This will install:
- MDSA framework (from parent directory)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- Streamlit (dashboard)
- Other utilities

### 2. Verify Installation

```bash
python -c "import chromadb; import streamlit; print('All dependencies installed!')"
```

---

## 🚀 Quick Start

### Option 1: Interactive Chat Mode

```bash
python chatbot.py
```

This starts an interactive terminal chatbot where you can:
- Chat naturally
- Use tools automatically
- Get RAG-enhanced responses
- View statistics with `/stats`

### Option 2: Python API

```python
from chatbot import MDSAChatbot

# Create chatbot
chatbot = MDSAChatbot(
    model_name="gpt2",  # Or ANY HuggingFace model!
    max_models=2,
    enable_rag=True,
    enable_tools=True
)

# Chat
result = chatbot.chat("What is the MDSA framework?")
print(result['response'])

# View stats
stats = chatbot.get_stats()
print(stats)
```

### Option 3: Monitoring Dashboard

```bash
streamlit run dashboard.py
```

Opens a web dashboard at `http://localhost:8501` with:
- Real-time metrics
- Latency distribution
- Domain distribution
- Model status
- Recent requests

---

## 📚 Knowledge Base

### Add Documents

The chatbot uses RAG to enhance responses with your own documents.

#### Add a Directory

```bash
# Add all files from knowledge_base/
# Supports: .txt, .md, .pdf
```

The chatbot automatically loads from `knowledge_base/` directory.

#### Add Individual Files

```python
# In your code
chatbot.add_knowledge_file("path/to/document.pdf")
chatbot.add_knowledge_file("path/to/document.txt")
```

#### Add Text Directly

```python
chatbot.add_knowledge(
    "Your custom knowledge here...",
    source="manual_entry"
)
```

---

## 🛠️ Available Tools

The chatbot has these built-in tools:

1. **get_current_time** - Get current date/time
2. **calculate** - Perform math calculations
3. **search_web** - Search using DuckDuckGo (free!)
4. **get_weather** - Get weather for a city (free!)
5. **word_count** - Count words in text
6. **extract_urls** - Extract URLs from text
7. **convert_units** - Convert between units (temperature, distance, weight)

### Using Tools

Tools are called automatically when needed. For example:

```
You: What's the weather in London?
Bot: [Automatically calls get_weather tool]
     Weather in London: 15°C, Cloudy, Humidity: 75%
```

Or manually trigger:

```
You: Calculate 25 * 4
Bot: [Calls calculate tool]
     Result: 100
```

---

## 🧪 Testing

### Run All Tests

```bash
python test_chatbot.py
```

This tests:
- ✅ Basic chat functionality
- ✅ RAG integration
- ✅ Tool calling
- ✅ Monitoring and metrics
- ✅ Model management

### Test Individual Components

```python
# Test RAG only
from rag_engine import RAGEngine

rag = RAGEngine()
rag.add_directory("./knowledge_base")
results = rag.search("MDSA framework")
print(results)
```

```python
# Test tools only
from tools import ToolRegistry

tools = ToolRegistry()
result = tools.call("get_current_time")
print(result)
```

---

## 📊 Monitoring Dashboard

### Start Dashboard

```bash
streamlit run dashboard.py
```

### Features

- **Overview Metrics**: Total requests, success rate, latency, models loaded
- **Latency Distribution**: Histogram of request latencies with P50/P95/P99
- **Domain Distribution**: Pie chart showing requests by domain
- **Model Performance**: Loaded models and memory usage
- **Success vs Errors**: Bar chart of successful vs failed requests
- **Throughput**: Requests per second
- **Recent Requests**: Table of last 10 requests with details

### Screenshot Example

```
┌─────────────────────────────────────────────────┐
│ MDSA Chatbot Monitoring Dashboard              │
├─────────────────────────────────────────────────┤
│ Total Requests: 150  │  Success Rate: 95.3%     │
│ Avg Latency: 245ms   │  Models Loaded: 2/3      │
├──────────────┬──────────────────────────────────┤
│  Latency     │  Domain Distribution             │
│  Graph       │  Pie Chart                       │
└──────────────┴──────────────────────────────────┘
```

---

## 🔧 Configuration

### Chatbot Settings

```python
chatbot = MDSAChatbot(
    model_name="gpt2",           # ANY HuggingFace model
    max_models=2,                 # Max models in memory
    enable_rag=True,              # Enable/disable RAG
    enable_tools=True,            # Enable/disable tools
    knowledge_base_dir="./kb"     # Knowledge base directory
)
```

### RAG Settings

```python
from rag_engine import RAGEngine

rag = RAGEngine(
    collection_name="my_kb",      # Collection name
    persist_directory="./db",     # Where to store DB
    embedding_model="all-MiniLM-L6-v2"  # Embedding model
)
```

### Domain Settings

Edit in `chatbot.py`:

```python
domains['custom'] = DomainConfig(
    domain_id="custom",
    domain_name="Custom Domain",
    keywords=["custom", "keywords"],
    model_name="microsoft/phi-2",  # Use different model
    max_tokens=200,
    temperature=0.7
)
```

---

## 🎨 Custom Tools

### Add Your Own Tool

```python
from tools import ToolRegistry

registry = ToolRegistry()

@registry.register("my_tool", "Description of my tool")
def my_custom_tool(arg1: str, arg2: int) -> str:
    """Your tool implementation."""
    return f"Processed {arg1} with {arg2}"

# Use it
result = registry.call("my_tool", arg1="test", arg2=42)
```

---

## 📁 Project Structure

```
chatbot_app/
├── chatbot.py              # Main chatbot application
├── rag_engine.py           # RAG with ChromaDB
├── tools.py                # Tool calling registry
├── dashboard.py            # Streamlit monitoring dashboard
├── test_chatbot.py         # End-to-end tests
├── requirements.txt        # Dependencies
├── knowledge_base/         # Knowledge base documents
│   └── sample_knowledge.txt
├── chroma_db/              # ChromaDB storage (created on first run)
└── README.md               # This file
```

---

## 🔍 Troubleshooting

### Issue: ModuleNotFoundError for chromadb

```bash
pip install chromadb sentence-transformers
```

### Issue: Slow model loading

- Use smaller models: `model_name="gpt2"` (124M params)
- Enable quantization:
  ```python
  from mdsa import QuantizationType
  config.quantization = QuantizationType.INT8
  ```

### Issue: Out of memory

- Reduce `max_models`: `max_models=1`
- Use smaller embedding model in RAG
- Enable quantization

### Issue: Dashboard not loading

```bash
# Reinstall Streamlit
pip install --upgrade streamlit

# Run with specific port
streamlit run dashboard.py --server.port 8502
```

---

## 📈 Performance Tips

1. **Use Appropriate Models**:
   - Small tasks: `gpt2` (124M)
   - Better quality: `microsoft/phi-2` (2.7B)
   - Best (if you have RAM): `mistralai/Mistral-7B`

2. **Enable Quantization**:
   ```python
   config.quantization = QuantizationType.INT8  # Reduces memory by ~75%
   ```

3. **Optimize RAG**:
   - Use smaller embedding models
   - Limit `n_results` in searches
   - Set appropriate `max_length` for context

4. **Monitor Performance**:
   - Use the dashboard to identify bottlenecks
   - Check P95/P99 latencies
   - Monitor model memory usage

---

## 🎯 Use Cases

### 1. Technical Support Bot

```python
chatbot = MDSAChatbot(
    model_name="microsoft/phi-2",
    enable_rag=True,
    knowledge_base_dir="./tech_docs"
)

# Automatically uses technical documentation via RAG
result = chatbot.chat("How do I install Python packages?")
```

### 2. Customer Service Bot

```python
chatbot = MDSAChatbot(
    model_name="gpt2",
    enable_tools=True,
    knowledge_base_dir="./faq"
)

# Uses FAQ + tools for weather, time, calculations
result = chatbot.chat("What's the status of my order?")
```

### 3. Personal Assistant

```python
chatbot = MDSAChatbot(
    enable_rag=True,
    enable_tools=True
)

# Full capabilities: RAG + Tools
result = chatbot.chat("Remind me about my meeting and show the weather")
```

---

## 🚀 Next Steps

1. **Add More Knowledge**:
   - Put your documents in `knowledge_base/`
   - Supports PDF, TXT, MD files

2. **Customize Domains**:
   - Edit `chatbot.py` to add custom domains
   - Use different models for different domains

3. **Add Custom Tools**:
   - Edit `tools.py` to add your own tools
   - Integrate with your APIs/services

4. **Deploy**:
   - Run dashboard on a server
   - Set up monitoring in production
   - Export metrics to Prometheus/Grafana

---

## 📄 License

Apache 2.0 - Same as MDSA Framework

---

## 🙏 Credits

Built with:
- **MDSA Framework** - Multi-domain orchestration
- **ChromaDB** - Vector database
- **Sentence Transformers** - Embeddings
- **Streamlit** - Dashboard
- **HuggingFace** - Models

All components are FREE and OPEN SOURCE!

---

**Ready to build amazing chatbots!** 🤖✨
