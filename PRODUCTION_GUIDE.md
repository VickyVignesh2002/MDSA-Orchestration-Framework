# MDSA Production Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Using ANY HuggingFace Model](#using-any-huggingface-model)
3. [Visualization & Monitoring](#visualization--monitoring)
4. [Using MDSA in Your Projects](#using-mdsa-in-your-projects)
5. [Plug and Play Models](#plug-and-play-models)
6. [Sharing & Publishing](#sharing--publishing)

---

## Installation

### Install from Local Directory

```bash
# Development mode (editable install)
pip install -e .

# Or standard install
pip install .
```

### Install from Wheel File (for sharing)

```bash
# Build the wheel
python setup.py bdist_wheel

# This creates: dist/mdsa-1.0.0-py3-none-any.whl

# Share this file with friends, they can install:
pip install mdsa-1.0.0-py3-none-any.whl
```

### Install with Optional Features

```bash
# With quantization support (for INT4/INT8 models)
pip install .[quantization]

# With web dashboard
pip install .[web]

# With development tools
pip install .[dev]

# Everything
pip install .[all]
```

### Verify Installation

```bash
# Show welcome page
python -m mdsa

# Or use the CLI command
mdsa
```

---

## Using ANY HuggingFace Model

**MDSA is NOT limited to predefined models!** You can use ANY model from HuggingFace or your custom models.

### Example 1: Microsoft Phi-2

```python
from mdsa import DomainConfig, DomainExecutor, ModelManager

# Create domain with Phi-2 model
phi_domain = DomainConfig(
    domain_id="general",
    domain_name="General Assistant",
    keywords=["help", "question", "info"],
    model_name="microsoft/phi-2",  # ANY HuggingFace model!
    max_tokens=256,
    temperature=0.7
)

manager = ModelManager()
executor = DomainExecutor(manager)

result = executor.execute("Explain quantum computing", phi_domain)
print(result['response'])
```

### Example 2: Mistral 7B

```python
mistral_domain = DomainConfig(
    domain_id="coding",
    domain_name="Code Assistant",
    keywords=["code", "programming", "debug"],
    model_name="mistralai/Mistral-7B-Instruct-v0.1",
    max_tokens=512,
    temperature=0.4
)

result = executor.execute("Write a Python function to sort a list", mistral_domain)
```

### Example 3: Custom Fine-tuned Model

```python
# Use your own fine-tuned model
custom_domain = DomainConfig(
    domain_id="legal",
    domain_name="Legal Assistant",
    keywords=["contract", "legal", "law"],
    model_name="your-username/legal-llm-finetuned",  # Your model!
    max_tokens=384,
    temperature=0.3
)
```

### Example 4: Domain-Specific Models

```python
# BioGPT for medical
bio_domain = DomainConfig(
    domain_id="medical",
    model_name="microsoft/biogpt",
    keywords=["medical", "health", "symptom"]
)

# FinBERT for finance
finance_domain = DomainConfig(
    domain_id="finance",
    model_name="ProsusAI/finbert",
    keywords=["stock", "finance", "trading"]
)

# CodeGen for programming
code_domain = DomainConfig(
    domain_id="coding",
    model_name="Salesforce/codegen-350M-mono",
    keywords=["code", "function", "debug"]
)
```

### Example 5: Quantized Models for Low Memory

```python
from mdsa import QuantizationType, ModelTier

# Use INT8 quantization for large models
large_model = DomainConfig(
    domain_id="general",
    model_name="meta-llama/Llama-2-7b-hf",
    quantization=QuantizationType.INT8,  # Reduce memory by ~75%
    tier=ModelTier.TIER1  # High priority
)
```

### Model Discovery

Find models on HuggingFace: https://huggingface.co/models

Filter by:
- **Task**: text-generation, text2text-generation
- **Size**: 124M (small) to 70B (large)
- **Domain**: medical, legal, finance, code, etc.

---

## Visualization & Monitoring

### Option 1: Python Monitoring (Built-in)

```python
from mdsa import RequestLogger, MetricsCollector, DomainExecutor, ModelManager
from mdsa.domains import create_finance_domain
import time

# Setup
manager = ModelManager()
executor = DomainExecutor(manager)
logger = RequestLogger(max_logs=1000)
metrics = MetricsCollector(window_size=500)

finance = create_finance_domain()

# Execute queries with monitoring
queries = [
    "What is my balance?",
    "Transfer $500 to savings",
    "Show recent transactions"
]

for query in queries:
    result = executor.execute(query, finance)

    # Log the request
    logger.log_request(
        request_id=f"req_{int(time.time())}",
        query=query,
        domain=result['domain'],
        model=result['model'],
        response=result['response'],
        status=result['status'],
        error=result['error'],
        latency_ms=result['latency_ms'],
        tokens_generated=result['tokens_generated'],
        confidence=result['confidence']
    )

    # Record metrics
    metrics.record_request(
        latency_ms=result['latency_ms'],
        tokens_generated=result['tokens_generated'],
        confidence=result['confidence'],
        domain=result['domain'],
        model=result['model'],
        status=result['status']
    )

# View statistics
stats = logger.get_stats()
print(f"Total Requests: {stats['total_requests']}")
print(f"Success Rate: {stats['success_rate_percent']:.1f}%")

summary = metrics.get_summary()
print(f"Avg Latency: {summary['avg_latency_ms']:.1f}ms")
print(f"P95 Latency: {summary['p95_latency_ms']:.1f}ms")
print(f"P99 Latency: {summary['p99_latency_ms']:.1f}ms")

# Export logs
logger.export_logs("logs.json", format="json")
logger.export_logs("logs.csv", format="csv")
```

### Option 2: Streamlit Dashboard (Real-time)

Create `dashboard.py`:

```python
import streamlit as st
import plotly.graph_objects as go
from mdsa import RequestLogger, MetricsCollector
import time

st.set_page_config(page_title="MDSA Monitoring", layout="wide")
st.title("MDSA Real-time Monitoring Dashboard")

# Initialize (use singleton pattern for production)
if 'logger' not in st.session_state:
    st.session_state.logger = RequestLogger(max_logs=10000)
    st.session_state.metrics = MetricsCollector(window_size=1000)

logger = st.session_state.logger
metrics = st.session_state.metrics

# Metrics Overview
col1, col2, col3, col4 = st.columns(4)

stats = logger.get_stats()
summary = metrics.get_summary()

with col1:
    st.metric("Total Requests", stats['total_requests'])
with col2:
    st.metric("Success Rate", f"{stats['success_rate_percent']:.1f}%")
with col3:
    st.metric("Avg Latency", f"{summary.get('avg_latency_ms', 0):.1f}ms")
with col4:
    throughput = metrics.get_throughput(window_seconds=60)
    st.metric("Throughput", f"{throughput:.2f} req/s")

# Latency Chart
st.subheader("Latency Distribution")
recent_logs = logger.get_recent_logs(count=100)
if recent_logs:
    latencies = [log.latency_ms for log in recent_logs]
    fig = go.Figure(data=[go.Histogram(x=latencies, nbinsx=20)])
    fig.update_layout(xaxis_title="Latency (ms)", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

# Per-Domain Metrics
st.subheader("Per-Domain Performance")
domain_metrics = metrics.get_domain_metrics()
if domain_metrics:
    domain_data = []
    for domain, data in domain_metrics.items():
        if isinstance(data, dict):
            domain_data.append({
                'Domain': domain,
                'Requests': data.get('requests', 0),
                'Avg Latency': f"{data.get('avg_latency_ms', 0):.1f}ms",
                'Error Rate': f"{data.get('error_rate_percent', 0):.1f}%"
            })
    st.table(domain_data)

# Recent Requests
st.subheader("Recent Requests")
recent = logger.get_recent_logs(count=10)
for log in recent:
    with st.expander(f"{log.request_id} - {log.domain} ({log.status})"):
        st.write(f"**Query:** {log.query}")
        st.write(f"**Response:** {log.response[:200]}...")
        st.write(f"**Latency:** {log.latency_ms:.1f}ms | **Confidence:** {log.confidence:.2f}")

# Auto-refresh
st.button("Refresh", key="refresh")
```

Run the dashboard:

```bash
pip install .[web]
streamlit run dashboard.py
```

### Option 3: Prometheus Metrics (Production)

Create `prometheus_exporter.py`:

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from mdsa import MetricsCollector
import time

# Define metrics
REQUEST_COUNT = Counter('mdsa_requests_total', 'Total requests', ['domain', 'status'])
REQUEST_LATENCY = Histogram('mdsa_request_latency_ms', 'Request latency', ['domain'])
ACTIVE_MODELS = Gauge('mdsa_active_models', 'Number of loaded models')

def export_to_prometheus(metrics: MetricsCollector):
    """Export MDSA metrics to Prometheus."""
    summary = metrics.get_summary()

    # Update gauges
    ACTIVE_MODELS.set(summary.get('active_models', 0))

    # Domain metrics
    for domain, data in metrics.get_domain_metrics().items():
        if isinstance(data, dict):
            REQUEST_COUNT.labels(domain=domain, status='success').inc(
                data.get('requests', 0) - data.get('errors', 0)
            )
            REQUEST_COUNT.labels(domain=domain, status='error').inc(
                data.get('errors', 0)
            )

# Start Prometheus server
start_http_server(8000)
print("Prometheus metrics available at http://localhost:8000")

# Keep running
while True:
    time.sleep(15)
```

Integrate with Grafana for beautiful dashboards!

---

## Using MDSA in Your Projects

### Project 1: Multi-Domain Chatbot

```python
from mdsa import ModelManager, DomainExecutor
from mdsa.domains import (
    create_finance_domain,
    create_medical_domain,
    create_support_domain
)

class MDSAChatbot:
    def __init__(self):
        self.manager = ModelManager(max_models=2)
        self.executor = DomainExecutor(self.manager)

        # Register domains
        self.domains = {
            'finance': create_finance_domain(),
            'medical': create_medical_domain(),
            'support': create_support_domain()
        }

    def chat(self, user_query: str, domain: str = None):
        """Process user query."""
        if domain:
            config = self.domains[domain]
        else:
            # Auto-detect domain from query
            config = self._detect_domain(user_query)

        result = self.executor.execute(user_query, config)
        return result['response']

    def _detect_domain(self, query: str):
        """Simple domain detection."""
        query_lower = query.lower()
        for domain_config in self.domains.values():
            if any(kw in query_lower for kw in domain_config.keywords):
                return domain_config
        return self.domains['support']  # Default

# Usage
bot = MDSAChatbot()
print(bot.chat("What's my account balance?"))  # Auto-routes to finance
print(bot.chat("I have a headache"))  # Auto-routes to medical
```

### Project 2: FastAPI Server

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mdsa import ModelManager, DomainExecutor, RequestLogger, MetricsCollector
from mdsa.domains import create_finance_domain
import uvicorn
import uuid
import time

app = FastAPI(title="MDSA API")

# Initialize
manager = ModelManager()
executor = DomainExecutor(manager)
logger = RequestLogger(max_logs=10000)
metrics = MetricsCollector()

# Domains
finance_domain = create_finance_domain()

class QueryRequest(BaseModel):
    query: str
    domain: str = "finance"

class QueryResponse(BaseModel):
    request_id: str
    response: str
    status: str
    latency_ms: float
    confidence: float

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a domain-specific query."""
    request_id = str(uuid.uuid4())

    # Execute
    result = executor.execute(request.query, finance_domain)

    # Log
    logger.log_request(
        request_id=request_id,
        query=request.query,
        domain=result['domain'],
        model=result['model'],
        response=result['response'],
        status=result['status'],
        error=result['error'],
        latency_ms=result['latency_ms'],
        tokens_generated=result['tokens_generated'],
        confidence=result['confidence']
    )

    # Metrics
    metrics.record_request(
        latency_ms=result['latency_ms'],
        tokens_generated=result['tokens_generated'],
        confidence=result['confidence'],
        domain=result['domain'],
        model=result['model'],
        status=result['status']
    )

    return QueryResponse(
        request_id=request_id,
        response=result['response'],
        status=result['status'],
        latency_ms=result['latency_ms'],
        confidence=result['confidence']
    )

@app.get("/metrics")
async def get_metrics():
    """Get performance metrics."""
    return metrics.get_summary()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    stats = manager.get_stats()
    return {
        "status": "healthy",
        "models_loaded": stats['models_loaded'],
        "memory_usage_gb": stats['total_memory_gb']
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run the server:

```bash
pip install fastapi uvicorn
python server.py

# Test:
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is my balance?"}'
```

### Project 3: Document Analysis Pipeline

```python
from mdsa import ModelManager, DomainConfig, DomainExecutor
from typing import List
import json

class DocumentAnalyzer:
    def __init__(self):
        self.manager = ModelManager(max_models=3)
        self.executor = DomainExecutor(self.manager)

        # Multiple specialized domains
        self.summarizer = DomainConfig(
            domain_id="summarize",
            model_name="facebook/bart-large-cnn",
            keywords=["summarize"]
        )

        self.classifier = DomainConfig(
            domain_id="classify",
            model_name="distilbert-base-uncased",
            keywords=["classify", "category"]
        )

        self.qa = DomainConfig(
            domain_id="qa",
            model_name="deepset/roberta-base-squad2",
            keywords=["question", "answer"]
        )

    def analyze_document(self, text: str) -> dict:
        """Full document analysis pipeline."""
        results = {}

        # Summarize
        summary_result = self.executor.execute(
            f"Summarize: {text}",
            self.summarizer
        )
        results['summary'] = summary_result['response']

        # Classify topic
        classify_result = self.executor.execute(
            f"Classify the topic: {text}",
            self.classifier
        )
        results['topic'] = classify_result['response']

        return results

# Usage
analyzer = DocumentAnalyzer()
doc = "Long financial report text here..."
analysis = analyzer.analyze_document(doc)
print(json.dumps(analysis, indent=2))
```

---

## Plug and Play Models

Test different models easily:

### Test Script: `test_models.py`

```python
from mdsa import ModelManager, DomainConfig, DomainExecutor
import time

def test_model(model_name: str, query: str):
    """Test any model with a query."""
    print(f"\n{'='*70}")
    print(f"Testing: {model_name}")
    print(f"{'='*70}")

    manager = ModelManager()
    executor = DomainExecutor(manager)

    config = DomainConfig(
        domain_id="test",
        domain_name=f"Test {model_name}",
        keywords=["test"],
        model_name=model_name,
        max_tokens=128,
        temperature=0.7
    )

    start = time.time()
    result = executor.execute(query, config)
    elapsed = time.time() - start

    print(f"Query: {query}")
    print(f"Response: {result['response']}")
    print(f"Status: {result['status']}")
    print(f"Latency: {elapsed:.2f}s")
    print(f"Tokens: {result['tokens_generated']}")
    print(f"Confidence: {result['confidence']:.2f}")

    return result

# Test different models
models_to_test = [
    "gpt2",                                    # Small, fast
    "microsoft/phi-2",                         # Medium, smart
    "EleutherAI/gpt-neo-125M",                # Alternative small model
    "facebook/opt-350m",                       # Facebook's model
    "bigscience/bloom-560m",                   # Multilingual
]

query = "Explain machine learning in simple terms"

for model in models_to_test:
    try:
        test_model(model, query)
    except Exception as e:
        print(f"Error with {model}: {e}")
```

Run:

```bash
python test_models.py
```

### Quick Model Swap

```python
# Original
finance = create_finance_domain()  # Uses gpt2

# Swap to better model - just change model_name!
from mdsa import DomainConfig

finance_upgraded = DomainConfig(
    domain_id="finance",
    domain_name="Finance Assistant",
    keywords=["balance", "account", "transfer", "payment"],
    model_name="microsoft/phi-2",  # ← Changed this!
    max_tokens=128,
    temperature=0.5
)

# Everything else works the same
result = executor.execute("What's my balance?", finance_upgraded)
```

---

## Sharing & Publishing

### Share with Friends (Wheel File)

```bash
# 1. Build the wheel
python setup.py bdist_wheel

# 2. Share the file in dist/
# dist/mdsa-1.0.0-py3-none-any.whl

# 3. Your friend installs:
pip install mdsa-1.0.0-py3-none-any.whl

# 4. They can use immediately:
python -m mdsa  # Shows welcome page
```

### Publish to PyPI (Public)

```bash
# 1. Install tools
pip install twine

# 2. Build distributions
python setup.py sdist bdist_wheel

# 3. Check the package
twine check dist/*

# 4. Upload to TestPyPI first (recommended)
twine upload --repository testpypi dist/*

# 5. Test installation
pip install --index-url https://test.pypi.org/simple/ mdsa

# 6. If everything works, upload to real PyPI
twine upload dist/*

# 7. Now anyone can install:
pip install mdsa
```

### Private PyPI Server

For internal use:

```bash
# Use devpi or PyPI server
pip install devpi-server
devpi-init
devpi-server

# Upload
twine upload --repository-url http://localhost:3141 dist/*

# Install
pip install --index-url http://localhost:3141/simple mdsa
```

### GitHub Releases

```bash
# 1. Tag version
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 2. Create release on GitHub
# Attach: dist/mdsa-1.0.0-py3-none-any.whl

# 3. Users install from GitHub
pip install https://github.com/yourusername/mdsa/releases/download/v1.0.0/mdsa-1.0.0-py3-none-any.whl
```

---

## Quick Reference

### Customization Checklist

- ✅ **Models**: ANY HuggingFace model (35k+ options)
- ✅ **Domains**: Custom keywords, prompts, validators
- ✅ **Hardware**: Auto-detects GPU/CPU, configurable
- ✅ **Memory**: Quantization (INT4, INT8, FP16)
- ✅ **Monitoring**: Logs, metrics, exports
- ✅ **Integration**: Python API, REST API, CLI

### Common Use Cases

1. **Multi-domain chatbot**: Route queries to specialized models
2. **Document analysis**: Summarize, classify, extract
3. **API server**: FastAPI/Flask with MDSA backend
4. **Research**: Compare models, benchmark performance
5. **Production**: Monitor, log, scale with metrics

### Resources

- HuggingFace Models: https://huggingface.co/models
- Transformers Docs: https://huggingface.co/docs/transformers
- MDSA Examples: See `examples/` directory

---

**Ready to build with MDSA!** 🚀
