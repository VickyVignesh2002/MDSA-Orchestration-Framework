# MDSA Chatbot - Quick Start Guide

## 🚀 What's New

### ✅ Fixed Issues
1. **RAG Knowledge Base Loading** - Now properly loads documents from `knowledge_base/` directory
2. **Dashboard Live Data** - New shared metrics system shows real-time chatbot data
3. **Multi-Page Dashboard** - Welcome, Monitor, and Settings pages
4. **Ollama Model Support** - Configuration guide for local Ollama models

### 🆕 New Features
1. **Welcome Page** - Installation verification and system overview
2. **Monitor Page** - Real-time model monitoring, performance metrics, and system info
3. **Settings Page** - Configuration management
4. **Shared Metrics** - Dashboard now shows live data from chatbot

---

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **MDSA Framework** installed (`pip install -e ..` from parent directory)
3. **Dependencies** installed (`pip install -r requirements.txt`)
4. **(Optional) Ollama** installed for local models

---

## 🏃 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd chatbot_app
pip install -r requirements.txt
```

### Step 2: Start the Chatbot

```bash
python chatbot.py
```

The chatbot will:
- ✅ Load the MDSA framework
- ✅ Initialize RAG with knowledge base from `./knowledge_base/`
- ✅ Register 7 tools (time, calculator, weather, etc.)
- ✅ Start writing metrics for the dashboard

### Step 3: Open the Dashboard (in another terminal)

```bash
streamlit run app.py
```

Then open: **http://localhost:8501**

The dashboard will show:
- 🏠 **Welcome** - Installation verification
- 📊 **Monitor** - Real-time model monitoring
- ⚙️ **Settings** - Configuration

---

## 🤖 Using Local Ollama Models

If you have Ollama installed with models like `llama3.2:1b`, `phi3:mini`, `qwen2.5:3b-instruct`, you can configure the chatbot to use them.

### Option 1: Edit chatbot.py directly

Open [chatbot.py](chatbot.py) and change line 422:

```python
# Before (uses HuggingFace GPT-2)
chatbot = MDSAChatbot(
    model_name="gpt2",
    ...
)

# After (uses your Ollama model)
chatbot = MDSAChatbot(
    model_name="llama3.2:1b",  # or "phi3:mini", "qwen2.5:3b-instruct"
    ...
)
```

### Option 2: Create a custom launcher

Create a file `chatbot_ollama.py`:

```python
from chatbot import MDSAChatbot

# Use your preferred Ollama model
chatbot = MDSAChatbot(
    model_name="llama3.2:3b-instruct-q4_0",  # Your best model
    max_models=2,
    enable_rag=True,
    enable_tools=False,  # Disable tools for smaller models
    knowledge_base_dir="./knowledge_base"
)

chatbot.interactive_mode()
```

Then run:
```bash
python chatbot_ollama.py
```

### Your Available Models

Based on your list, you have:
- `llama3.2:1b` - Fast, good for general chat
- `llama3.2:3b-instruct-q4_0` - Better quality, still fast
- `phi3:mini` - Microsoft Phi-3, great for reasoning
- `qwen2.5:3b-instruct` - Qwen 2.5, good multilingual support
- `gpt-oss:20b-c10ud` - Large model for complex tasks
- `gpt-oss:120b-c10ud` - Very large, best quality (slow)
- `nomic-embed-text:latest` - For embeddings (RAG)

**Recommended for Chatbot**: `llama3.2:3b-instruct-q4_0` or `phi3:mini`

---

## 📚 Adding Knowledge to RAG

### Method 1: Add Files to knowledge_base/

Simply place `.txt`, `.md`, or `.pdf` files in the `knowledge_base/` directory:

```bash
cp your_document.txt knowledge_base/
cp research_paper.pdf knowledge_base/
```

Restart the chatbot to load new documents.

### Method 2: Add Knowledge Programmatically

In the chatbot (after initialization):

```python
chatbot.add_knowledge("Your custom knowledge here", source="manual")

# Or from a file
chatbot.add_knowledge_file("path/to/document.pdf")
```

### Example: Test RAG

1. Add content to `knowledge_base/sample_knowledge.txt`
2. Restart chatbot: `python chatbot.py`
3. Ask: "What is the MDSA framework?"
4. The chatbot should respond using the knowledge base!

---

## 📊 Understanding the Dashboard

### Welcome Page (http://localhost:8501)

Shows:
- ✅ Installation status
- ✅ System information
- ✅ Available local models
- ✅ Knowledge base status
- ✅ Quick start guide

### Monitor Page

Shows **real-time** data:
- **System Overview**: Status, version, uptime
- **Request Statistics**: Total requests, success rate, errors
- **Performance Metrics**: Latency (avg, P95), tokens, throughput
- **Loaded Models**: Which models are in memory, memory usage
- **Domain Distribution**: Pie chart of requests by domain
- **RAG Status**: Documents loaded, embedding model
- **Tools Status**: Available tools list
- **Recent Requests**: Last 10 requests with details

**Note**: Dashboard updates automatically when chatbot is running!

### Settings Page

Configure:
- Model selection
- Max models in memory
- RAG settings
- Tool settings
- Performance parameters

---

## 🛠️ Troubleshooting

### Issue 1: RAG says "No relevant context found"

**Cause**: Knowledge base not loaded or query doesn't match documents.

**Fix**:
```bash
# Check if knowledge_base/ exists
ls knowledge_base/

# Make sure chatbot.py has knowledge_base_dir parameter
# Line 426 should be:
knowledge_base_dir="./knowledge_base"
```

### Issue 2: Dashboard shows empty/no data

**Cause**: Chatbot not running or shared metrics not working.

**Fix**:
1. Make sure chatbot is running: `python chatbot.py`
2. Make a few queries to generate data
3. Refresh dashboard
4. Check for `chatbot_metrics.json` file:
```bash
cat chatbot_metrics.json  # Should show JSON data
```

### Issue 3: Tool calling generates errors

**Cause**: GPT-2 (small model) struggles with tool calling syntax.

**Fix** (for Ollama models):
```python
# Disable tools for small models (< 3B parameters)
chatbot = MDSAChatbot(
    model_name="llama3.2:1b",
    enable_tools=False,  # Disable tools
    ...
)

# Enable tools for larger models (>= 3B parameters)
chatbot = MDSAChatbot(
    model_name="llama3.2:3b-instruct-q4_0",
    enable_tools=True,  # Enable tools
    ...
)
```

### Issue 4: Model not found

**Cause**: Model name incorrect or Ollama not configured.

**Fix**:
```bash
# List your Ollama models
ollama list

# Use exact model name from the list
# Example: If list shows "llama3.2:3b-instruct-q4_0"
# Use: model_name="llama3.2:3b-instruct-q4_0"
```

---

## 🎯 Recommended Configurations

### For Fast Responses (1-2B models)

```python
chatbot = MDSAChatbot(
    model_name="llama3.2:1b",
    max_models=2,
    enable_rag=True,
    enable_tools=False,  # Small models struggle with tools
    knowledge_base_dir="./knowledge_base"
)
```

### For Quality Responses (3B+ models)

```python
chatbot = MDSAChatbot(
    model_name="llama3.2:3b-instruct-q4_0",
    max_models=2,
    enable_rag=True,
    enable_tools=True,
    knowledge_base_dir="./knowledge_base"
)
```

### For Best Quality (20B+ models)

```python
chatbot = MDSAChatbot(
    model_name="gpt-oss:20b-c10ud",
    max_models=1,  # Large models use more memory
    enable_rag=True,
    enable_tools=True,
    knowledge_base_dir="./knowledge_base"
)
```

---

## 📈 Testing the Complete System

### Test 1: Basic Chat

```bash
python chatbot.py
```

```
You: Hello, how are you?
Bot: [Response from model]

You: What is a black hole?
Bot: [Should use RAG to respond about black holes from knowledge base]
```

### Test 2: RAG Integration

```bash
You: Tell me about the MDSA framework
Bot: [Should respond using knowledge from sample_knowledge.txt]
```

If it says "No relevant context found", check:
1. `knowledge_base/sample_knowledge.txt` exists
2. Chatbot was restarted after adding files
3. Query matches content in knowledge base

### Test 3: Dashboard

1. Start chatbot: `python chatbot.py`
2. Make 2-3 queries
3. Open dashboard: `streamlit run app.py`
4. Go to Monitor page
5. You should see:
   - Total requests: 2-3
   - Models loaded: 1
   - Recent requests showing your queries

---

## 🎉 Success Checklist

- [ ] Chatbot starts without errors
- [ ] RAG loads documents from knowledge_base/
- [ ] Queries get responses from the model
- [ ] Dashboard shows welcome page
- [ ] Dashboard monitor page shows live data
- [ ] Metrics file (`chatbot_metrics.json`) is created
- [ ] Models are listed in dashboard
- [ ] Recent requests appear in dashboard

If all checks pass, **you're ready to use the MDSA chatbot!** 🎉

---

## 📞 Next Steps

1. **Add your documents** to `knowledge_base/`
2. **Configure your preferred Ollama model**
3. **Customize domains** in `chatbot.py` for your use case
4. **Add custom tools** in `tools.py`
5. **Monitor performance** using the dashboard

Happy chatting! 🤖✨
